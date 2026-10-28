const crypto = require('crypto');
const path = require('path');
const fs = require('fs');
const config = require('../config');
const { recordSecurityEvent, getClientIp } = require('./honeypot');

function signPass(payload) {
  const data = JSON.stringify(payload);
  const hmac = crypto.createHmac('sha256', config.GATEWAY_COOKIE_SECRET).update(data).digest('hex');
  return Buffer.from(data).toString('base64url') + '.' + hmac;
}

function verifyPassToken(tokenStr) {
  if (!tokenStr || typeof tokenStr !== 'string') return false;
  const parts = tokenStr.split('.');
  if (parts.length !== 2) return false;

  const [b64Data, expectedHmac] = parts;
  try {
    const rawData = Buffer.from(b64Data, 'base64url').toString('utf8');
    const actualHmac = crypto.createHmac('sha256', config.GATEWAY_COOKIE_SECRET).update(rawData).digest('hex');
    
    // Constant-time comparison
    if (!crypto.timingSafeEqual(Buffer.from(expectedHmac, 'hex'), Buffer.from(actualHmac, 'hex'))) {
      return false;
    }

    const payload = JSON.parse(rawData);
    if (!payload.exp || Date.now() > payload.exp) {
      return false;
    }
    return payload;
  } catch (e) {
    return false;
  }
}

function hasValidGatewayPass(req) {
  const token = req.cookies && req.cookies[config.GATEWAY_COOKIE_NAME];
  if (!token) return false;
  return !!verifyPassToken(token);
}

function handleGatewayEntry(req, res) {
  const ip = getClientIp(req);
  const providedKey = (req.query && req.query.key) || (req.body && req.body.key) || '';
  const destination = (req.query && req.query.to) || (req.body && req.body.to) || 'admin';

  if (!providedKey || providedKey !== config.PORTAL_GATEWAY_KEY) {
    recordSecurityEvent({
      type: 'INVALID_GATEWAY_KEY_ATTEMPT',
      severity: 'HIGH',
      ip,
      path: req.originalUrl,
      userAgent: req.headers['user-agent'] || 'Unknown',
      message: `Failed portal gateway authorization attempt with key: ${providedKey ? '***MASKED***' : 'EMPTY'}`
    });

    // Cloak response as genuine 404 Not Found
    res.status(404);
    const page404 = path.join(config.PUBLIC_DIR, '404.html');
    if (fs.existsSync(page404)) {
      return res.sendFile(page404);
    }
    return res.send('404 Not Found');
  }

  // Key is valid! Issue signed 12-hour gateway cookie
  const payload = {
    authorized: true,
    grantedAt: Date.now(),
    exp: Date.now() + (12 * 60 * 60 * 1000), // 12 hours
    ip
  };
  const token = signPass(payload);

  res.cookie(config.GATEWAY_COOKIE_NAME, token, {
    httpOnly: true,
    sameSite: 'lax',
    maxAge: 12 * 60 * 60 * 1000
  });

  recordSecurityEvent({
    type: 'GATEWAY_ACCESS_GRANTED',
    severity: 'INFO',
    ip,
    path: req.originalUrl,
    message: `Authorized staff member successfully unlocked portal gateway. Heading to: ${destination}`
  });

  // Redirect to target destination
  if (destination === 'dev') {
    return res.redirect('/dev/');
  } else if (destination === 'superadmin') {
    return res.redirect('/superadmin/');
  } else {
    return res.redirect('/admin/');
  }
}

function handleGatewayRevoke(req, res) {
  res.clearCookie(config.GATEWAY_COOKIE_NAME);
  res.clearCookie('admin_token');
  res.redirect('/?gateway_session_closed=true');
}

module.exports = {
  signPass,
  verifyPassToken,
  hasValidGatewayPass,
  handleGatewayEntry,
  handleGatewayRevoke
};
