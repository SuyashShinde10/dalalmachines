const path = require('path');
const fs = require('fs');
const jwt = require('jsonwebtoken');
const config = require('../config');
const db = require('../db');
const { hasValidGatewayPass } = require('./gateway');
const { getClientIp, recordSecurityEvent } = require('./honeypot');
const { verifyClientFingerprint } = require('./defenseInDepth');

// In-memory runtime lockdown state
global.PORTAL_LOCKDOWN = false;

function isDevIpAllowed(req) {
  if (config.ALLOWED_DEV_IPS.includes('*')) return true;
  const ip = getClientIp(req);
  return config.ALLOWED_DEV_IPS.includes(ip) || config.ALLOWED_DEV_IPS.includes(ip.toLowerCase());
}

function sendCloaked404(res, req, reason = 'Unauthorized path probe') {
  res.status(404);
  const page404 = path.join(config.PUBLIC_DIR, '404.html');
  if (fs.existsSync(page404)) {
    return res.sendFile(page404);
  }
  return res.send('404 Not Found');
}

function getAuthenticatedUser(req) {
  let token = null;
  const authHeader = req.headers['authorization'];
  if (authHeader && authHeader.startsWith('Bearer ')) {
    token = authHeader.split(' ')[1];
  } else if (req.cookies && req.cookies.admin_token) {
    token = req.cookies.admin_token;
  } else if (req.cookies && req.cookies.superadmin_token) {
    token = req.cookies.superadmin_token;
  }

  if (!token) return null;

  try {
    const decoded = jwt.verify(token, config.JWT_SECRET);
    if (decoded.fp && !verifyClientFingerprint(req, decoded.fp)) {
      return null; // Stolen token fingerprint mismatch: drop privileges immediately
    }
    const user = db.getUserById(decoded.id);
    if (!user || !user.active) return null;
    return user;
  } catch (err) {
    return null;
  }
}

function routeShieldMiddleware(req, res, next) {
  const p = req.path.toLowerCase();

  const isAdminPath = p === '/admin' || p.startsWith('/admin/');
  const isSuperAdminPath = p === '/superadmin' || p.startsWith('/superadmin/');
  const isDevPath = p === '/dev' || p.startsWith('/dev/');
  const isDevApiPath = (p === '/api/dev' || p.startsWith('/api/dev/')) && p !== '/api/dev/broadcast-banner';

  // If not accessing protected admin/dev/superadmin panels or developer APIs, continue normally
  if (!isAdminPath && !isSuperAdminPath && !isDevPath && !isDevApiPath) {
    return next();
  }

  // 0. Static assets (CSS, JS, images, fonts) must ALWAYS be served so login screens and dashboards render with full styling
  const isStaticAsset = /\.(css|js|png|jpg|jpeg|gif|svg|ico|woff|woff2|ttf|eot|map)$/i.test(p);
  if (isStaticAsset) {
    return next();
  }

  const user = getAuthenticatedUser(req);
  const hasGatePass = hasValidGatewayPass(req);
  const ip = getClientIp(req);
  const isLocalOrWhitelisted = isDevIpAllowed(req);

  // 1. Emergency Lockdown Enforcement
  if (global.PORTAL_LOCKDOWN) {
    if (!user || user.role !== 'superadmin') {
      return sendCloaked404(res, req, 'Emergency Portal Lockdown Active');
    }
  }

  // 2. Complete Obscurity Gate
  // Only external, non-whitelisted requests without login or gate pass get cloaked as 404
  if (!isLocalOrWhitelisted && !user && !hasGatePass) {
    recordSecurityEvent({
      type: 'CLOAKED_ROUTE_PROBE',
      severity: 'LOW',
      ip,
      path: req.originalUrl,
      userAgent: req.headers['user-agent'] || 'Unknown',
      message: `Unauthorized visitor or scanner probed protected panel without gateway passkey: ${req.originalUrl}`
    });
    return sendCloaked404(res, req, 'Missing gateway pass');
  }

  // 3. Developer Console & Developer API Security Layer
  if (isDevPath || isDevApiPath) {
    if (!isDevIpAllowed(req)) {
      recordSecurityEvent({
        type: 'DEV_IP_RESTRICTION_BLOCKED',
        severity: 'HIGH',
        ip,
        path: req.originalUrl,
        message: `IP ${ip} attempted to access developer endpoint but is not in ALLOWED_DEV_IPS whitelist.`
      });
      return sendCloaked404(res, req, 'IP not whitelisted for developer endpoint');
    }

    if (user && (user.role === 'superadmin' || user.username === 'developer')) {
      return next();
    }

    if (hasGatePass || isLocalOrWhitelisted) {
      return next();
    }

    return sendCloaked404(res, req, 'Developer auth required');
  }

  // 4. Superadmin Portal Security Layer
  if (isSuperAdminPath) {
    // If logged in as staff admin (not superadmin), conceal superadmin as 404
    if (user && user.role !== 'superadmin') {
      return sendCloaked404(res, req, 'Role mismatch: admin probing superadmin');
    }
    // Allow static assets, login page, and panels through so superadmin-core.js handles auth/redirect gracefully
    return next();
  }

  // 5. Admin Portal Security Layer
  if (isAdminPath) {
    // Check if user is suspended by developer
    if (user && user.blockedByDeveloper) {
      if (!p.endsWith('index.html') && p !== '/admin' && p !== '/admin/') {
        return res.redirect('/admin/index.html?suspended=true');
      }
    }
    return next();
  }

  next();
}

function togglePortalLockdown(enable) {
  global.PORTAL_LOCKDOWN = !!enable;
  db.addLog({
    userId: 'secops_lead',
    username: 'Lead System Developer',
    role: 'developer',
    action: global.PORTAL_LOCKDOWN ? 'PORTAL_LOCKDOWN_ENGAGED' : 'PORTAL_LOCKDOWN_LIFTED',
    target: 'SECURITY',
    details: `Emergency portal lockdown was ${global.PORTAL_LOCKDOWN ? 'ACTIVATED (All administrative routes cloaked as 404)' : 'DEACTIVATED (Normal gateway access restored)'}`
  });
  return global.PORTAL_LOCKDOWN;
}

function getLockdownStatus() {
  return global.PORTAL_LOCKDOWN;
}

module.exports = {
  routeShieldMiddleware,
  togglePortalLockdown,
  getLockdownStatus,
  sendCloaked404
};
