const fs = require('fs');
const path = require('path');
const config = require('../config');
const db = require('../db');

// In-memory cache of blacklist and events
let blacklist = [];
let securityEvents = [];
let violationCounts = new Map(); // ip -> { count, lastSeen }

function loadData() {
  try {
    if (fs.existsSync(config.BLACKLIST_FILE)) {
      blacklist = JSON.parse(fs.readFileSync(config.BLACKLIST_FILE, 'utf8'));
    } else {
      blacklist = [];
    }
  } catch (e) {
    console.error('[Security] Error loading blacklist:', e.message);
    blacklist = [];
  }

  try {
    if (fs.existsSync(config.SECURITY_EVENTS_FILE)) {
      securityEvents = JSON.parse(fs.readFileSync(config.SECURITY_EVENTS_FILE, 'utf8'));
    } else {
      securityEvents = [];
    }
  } catch (e) {
    console.error('[Security] Error loading security events:', e.message);
    securityEvents = [];
  }
}

function saveBlacklist() {
  try {
    const tmp = config.BLACKLIST_FILE + '.tmp';
    fs.writeFileSync(tmp, JSON.stringify(blacklist, null, 2), 'utf8');
    fs.renameSync(tmp, config.BLACKLIST_FILE);
  } catch (e) {
    console.error('[Security] Error saving blacklist:', e.message);
  }
}

function saveSecurityEvents() {
  try {
    // Keep last 500 events
    if (securityEvents.length > 500) {
      securityEvents = securityEvents.slice(-500);
    }
    const tmp = config.SECURITY_EVENTS_FILE + '.tmp';
    fs.writeFileSync(tmp, JSON.stringify(securityEvents, null, 2), 'utf8');
    fs.renameSync(tmp, config.SECURITY_EVENTS_FILE);
  } catch (e) {
    console.error('[Security] Error saving security events:', e.message);
  }
}

// Initial load
loadData();

function cleanIp(ip) {
  if (!ip) return '127.0.0.1';
  if (ip.startsWith('::ffff:')) return ip.replace('::ffff:', '');
  if (ip === '::1') return '127.0.0.1';
  return ip;
}

function getClientIp(req) {
  const forwarded = req.headers['x-forwarded-for'];
  if (forwarded) {
    const parts = forwarded.split(',');
    return cleanIp(parts[0].trim());
  }
  return cleanIp(req.socket.remoteAddress || req.ip || '127.0.0.1');
}

function isIpBlacklisted(ip) {
  const normalized = cleanIp(ip);
  const now = Date.now();
  const entry = blacklist.find(b => b.ip === normalized);
  if (!entry) return false;

  // Check if ban expired
  if (entry.expiresAt && now > entry.expiresAt) {
    // remove expired
    blacklist = blacklist.filter(b => b.ip !== normalized);
    saveBlacklist();
    return false;
  }
  return true;
}

function banIp(ip, reason = 'Automated intrusion trigger', durationMs = config.BAN_DURATION_MS) {
  const normalized = cleanIp(ip);
  // Do not ban localhost in development
  if (normalized === '127.0.0.1' && process.env.NODE_ENV !== 'production') {
    console.warn(`[Security] Localhost probe detected from ${normalized} (${reason}) - Bypassing local ban in dev mode.`);
    return false;
  }

  const existing = blacklist.find(b => b.ip === normalized);
  const banRecord = {
    ip: normalized,
    reason,
    bannedAt: new Date().toISOString(),
    expiresAt: Date.now() + durationMs,
    bannedBy: 'AUTOSHIELD_HONEYPOT'
  };

  if (existing) {
    Object.assign(existing, banRecord);
  } else {
    blacklist.push(banRecord);
  }

  saveBlacklist();

  // Log in system db audit logs
  db.addLog({
    userId: 'secops_autoshield',
    username: 'SecOps AutoShield',
    role: 'system',
    action: 'IP_BLACKLISTED',
    target: 'FIREWALL',
    details: `IP ${normalized} auto-banned for 24h. Reason: ${reason}`
  });

  return true;
}

function unbanIp(ip) {
  const normalized = cleanIp(ip);
  const initialLen = blacklist.length;
  blacklist = blacklist.filter(b => b.ip !== normalized);
  if (blacklist.length !== initialLen) {
    saveBlacklist();
    db.addLog({
      userId: 'secops_autoshield',
      username: 'Lead System Developer',
      role: 'developer',
      action: 'IP_UNBANNED',
      target: 'FIREWALL',
      details: `IP ${normalized} released from blacklist by developer.`
    });
    return true;
  }
  return false;
}

function recordSecurityEvent(event) {
  const enriched = {
    id: 'evt_' + Date.now() + '_' + Math.random().toString(36).substr(2, 5),
    timestamp: new Date().toISOString(),
    ...event
  };
  securityEvents.push(enriched);
  saveSecurityEvents();

  // Emit to Developer Room via realtime if available
  try {
    const realtime = require('../realtime');
    realtime.emitToDeveloper('security:intrusion_alert', enriched);
  } catch (err) {
    // realtime might be starting up
  }

  return enriched;
}

function getSecurityStats() {
  const now = Date.now();
  // Filter active bans
  const activeBans = blacklist.filter(b => !b.expiresAt || b.expiresAt > now);
  return {
    totalEvents: securityEvents.length,
    activeBansCount: activeBans.length,
    activeBans: activeBans.slice(-20),
    recentEvents: securityEvents.slice(-25).reverse()
  };
}

// Middleware: Drops connection / 403 for blacklisted IPs
function blacklistGuardMiddleware(req, res, next) {
  const ip = getClientIp(req);
  if (isIpBlacklisted(ip)) {
    res.setHeader('Connection', 'close');
    return res.status(403).send('<html><body style="font-family:sans-serif;text-align:center;padding:50px;"><h2>403 Forbidden</h2><p>Access blocked by Dalal Machine Tools SecOps Firewall due to suspicious activity.</p></body></html>');
  }
  next();
}

// Honeypot Trap Handler
function honeypotHandler(req, res) {
  const ip = getClientIp(req);
  const userAgent = req.headers['user-agent'] || 'Unknown';
  const pathAttempt = req.originalUrl || req.path;

  // Track violations
  let current = violationCounts.get(ip) || { count: 0, lastSeen: Date.now() };
  current.count += 1;
  current.lastSeen = Date.now();
  violationCounts.set(ip, current);

  const isAggressive = current.count >= 3 || pathAttempt.includes('.env') || pathAttempt.includes('phpmyadmin');
  let autoBanned = false;

  if (isAggressive) {
    autoBanned = banIp(ip, `Probing honeypot trap: ${pathAttempt} (${current.count} attempts)`);
  }

  // Record Event
  recordSecurityEvent({
    type: 'HONEYPOT_PROBE',
    severity: isAggressive ? 'HIGH' : 'MEDIUM',
    ip,
    path: pathAttempt,
    method: req.method,
    userAgent,
    autoBanned,
    message: `Unauthorized scanner probed deceptive route: ${pathAttempt}`
  });

  // Always return the legitimate, official Dalal 404 page
  res.status(404);
  const page404 = path.join(config.PUBLIC_DIR, '404.html');
  if (fs.existsSync(page404)) {
    return res.sendFile(page404);
  }
  return res.send('404 Not Found');
}

module.exports = {
  getClientIp,
  isIpBlacklisted,
  banIp,
  unbanIp,
  recordSecurityEvent,
  getSecurityStats,
  blacklistGuardMiddleware,
  honeypotHandler
};

