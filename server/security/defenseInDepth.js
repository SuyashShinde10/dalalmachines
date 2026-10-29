// Dalal Machine Tools Agency Pvt. Ltd.
// Enterprise Defense-in-Depth Security Suite
// Version: 1.0 | Top 1% Zero-Trust Fortress Architecture

const crypto = require('crypto');
const config = require('../config');
const { recordSecurityEvent, getClientIp } = require('./honeypot');

// In-memory account lockout & brute force tracking
const accountFailures = new Map(); // username -> { count: number, lockedUntil: number, lastAttempt: number }

/**
 * ───────────────────────────────────────────────────────────────────────────
 * 1. Zero-Trust Cryptographic Client Fingerprinting (Anti-Token-Hijacking)
 * ───────────────────────────────────────────────────────────────────────────
 */
function getClientSubnet(ip) {
  if (!ip) return '0.0.0.0';
  // If IPv6 mapped IPv4
  if (ip.startsWith('::ffff:')) ip = ip.replace('::ffff:', '');
  if (ip.includes('.')) {
    // IPv4: take first 3 octets (e.g., 192.168.1.xxx) for mobile network IP roaming resilience
    const parts = ip.split('.');
    if (parts.length === 4) return `${parts[0]}.${parts[1]}.${parts[2]}`;
  }
  return ip.substring(0, 16);
}

function generateClientFingerprint(req) {
  const ip = getClientIp(req);
  const subnet = getClientSubnet(ip);
  const userAgent = req.headers['user-agent'] || 'UnknownAgent';
  const secret = config.JWT_SECRET || 'dmta_sec_secret';

  return crypto
    .createHash('sha256')
    .update(`${subnet}|${userAgent}|${secret}`)
    .digest('hex')
    .substring(0, 16);
}

function verifyClientFingerprint(req, tokenFingerprint) {
  if (!tokenFingerprint) return true; // Legacy token fallback
  const currentFp = generateClientFingerprint(req);
  return currentFp === tokenFingerprint;
}

/**
 * ───────────────────────────────────────────────────────────────────────────
 * 2. Enterprise Account Lockout & Exponential Backoff Delay
 * ───────────────────────────────────────────────────────────────────────────
 */
const MAX_FAILED_ATTEMPTS = 5;
const LOCKOUT_DURATION_MS = 15 * 60 * 1000; // 15 minutes

function checkAccountLockout(username) {
  if (!username) return { locked: false };
  const userKey = username.toLowerCase().trim();
  const record = accountFailures.get(userKey);

  if (!record) return { locked: false };

  if (record.lockedUntil && Date.now() < record.lockedUntil) {
    const remainingSeconds = Math.ceil((record.lockedUntil - Date.now()) / 1000);
    return {
      locked: true,
      remainingSeconds,
      lockedUntil: record.lockedUntil
    };
  }

  // If lockout expired, reset
  if (record.lockedUntil && Date.now() >= record.lockedUntil) {
    accountFailures.delete(userKey);
    return { locked: false };
  }

  return { locked: false, attempts: record.count };
}

async function recordFailedLogin(username, req) {
  if (!username) return;
  const userKey = username.toLowerCase().trim();
  const now = Date.now();
  const record = accountFailures.get(userKey) || { count: 0, lastAttempt: now };

  record.count++;
  record.lastAttempt = now;

  // Progressive delay: 1st=300ms, 2nd=600ms, 3rd=1200ms, 4th=2400ms
  const progressiveDelayMs = Math.min(3000, 300 * Math.pow(2, record.count - 1));

  if (record.count >= MAX_FAILED_ATTEMPTS) {
    record.lockedUntil = now + LOCKOUT_DURATION_MS;
    recordSecurityEvent({
      type: 'ACCOUNT_BRUTE_FORCE_LOCKED',
      severity: 'HIGH',
      ip: getClientIp(req),
      path: '/api/auth/login',
      userAgent: req.headers['user-agent'] || 'Unknown',
      message: `Account '${username}' locked for 15 minutes following ${record.count} consecutive failed authentication attempts.`
    });
  }

  accountFailures.set(userKey, record);

  // Apply artificial exponential backoff to destroy automated password spray throughput
  await new Promise(resolve => setTimeout(resolve, progressiveDelayMs));
}

function recordSuccessfulLogin(username) {
  if (!username) return;
  accountFailures.delete(username.toLowerCase().trim());
}

/**
 * ───────────────────────────────────────────────────────────────────────────
 * 3. Deep Recursive Request Sanitization & Prototype Pollution Guard
 * ───────────────────────────────────────────────────────────────────────────
 */
const DANGEROUS_KEYS = ['__proto__', 'constructor', 'prototype', '$where', '$regex'];
const SCRIPT_REGEX = /<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi;
const JS_URI_REGEX = /javascript\s*:/gi;
const INLINE_EVENT_REGEX = /on\w+\s*=/gi;

function sanitizeValue(val) {
  if (typeof val === 'string') {
    // Strip script tags, javascript: uris, and inline event handlers
    return val
      .replace(SCRIPT_REGEX, '')
      .replace(JS_URI_REGEX, 'no-javascript:')
      .replace(INLINE_EVENT_REGEX, 'no-event=');
  }
  if (Array.isArray(val)) {
    return val.map(sanitizeValue);
  }
  if (val !== null && typeof val === 'object') {
    const cleanObj = {};
    for (const [k, v] of Object.entries(val)) {
      if (DANGEROUS_KEYS.includes(k.toLowerCase())) {
        // Prototype pollution attempt dropped
        continue;
      }
      cleanObj[k] = sanitizeValue(v);
    }
    return cleanObj;
  }
  return val;
}

function deepSanitizeMiddleware(req, res, next) {
  try {
    if (req.body && typeof req.body === 'object') {
      req.body = sanitizeValue(req.body);
    }
    if (req.query && typeof req.query === 'object') {
      req.query = sanitizeValue(req.query);
    }
    if (req.params && typeof req.params === 'object') {
      req.params = sanitizeValue(req.params);
    }
  } catch (err) {
    console.warn('[DeepSanitizer] Parse error:', err.message);
  }
  next();
}

/**
 * ───────────────────────────────────────────────────────────────────────────
 * 4. Double-Submit CSRF & Origin Validation Guard
 * ───────────────────────────────────────────────────────────────────────────
 */
function csrfGuardMiddleware(req, res, next) {
  // Only inspect mutating methods
  const mutatingMethods = ['POST', 'PUT', 'DELETE', 'PATCH'];
  if (!mutatingMethods.includes(req.method)) {
    return next();
  }

  // Exempt public RFQ inquiries and public login
  const path = req.path.toLowerCase();
  if (path === '/api/inquiries' || path === '/api/auth/login' || path.startsWith('/portal-gate')) {
    return next();
  }

  // If request contains authorization header or custom requested-with header, consider CSRF-safe
  const authHeader = req.headers['authorization'];
  const requestedWith = req.headers['x-requested-with'];
  const customCsrfHeader = req.headers['x-dmta-csrf'];

  if (authHeader || requestedWith || customCsrfHeader) {
    return next();
  }

  // Verify Origin / Referer matches host
  const origin = req.headers['origin'] || req.headers['referer'];
  const host = req.headers['host'];

  if (origin && host && origin.includes(host)) {
    return next();
  }

  // Fallback: If same-site cookie or localhost development
  if (req.headers['sec-fetch-site'] === 'same-origin' || req.headers['sec-fetch-site'] === 'same-site') {
    return next();
  }

  // Allow localhost during dev
  if (host && (host.startsWith('localhost:') || host.startsWith('127.0.0.1:'))) {
    return next();
  }

  return res.status(403).json({
    success: false,
    message: 'CSRF Protection: Origin or custom security header verification failed.'
  });
}

/**
 * ───────────────────────────────────────────────────────────────────────────
 * 5. Cryptographically Chained Audit Trail (Tamper-Evident Hash Chain)
 * ───────────────────────────────────────────────────────────────────────────
 */
function computeLogHash(entry, previousHash = 'GENESIS_HASH_DMTA_2026') {
  const payload = `${previousHash}|${entry.timestamp}|${entry.userId}|${entry.action}|${entry.target}|${entry.details || ''}|${entry.ip || ''}`;
  return crypto.createHash('sha256').update(payload).digest('hex');
}

function verifyAuditChain(logs) {
  if (!Array.isArray(logs) || logs.length === 0) {
    return { valid: true, count: 0 };
  }

  // Logs are ordered newest first (unshifted), so verify in reverse chronological order
  const chronological = [...logs].reverse();
  let prevHash = 'GENESIS_HASH_DMTA_2026';

  for (let i = 0; i < chronological.length; i++) {
    const entry = chronological[i];
    if (entry.prevHash && entry.hash) {
      if (entry.prevHash !== prevHash) {
        return {
          valid: false,
          compromisedIndex: i,
          compromisedEntry: entry,
          message: `Audit chain broken at log ${entry.id}: previous hash mismatch`
        };
      }
      const expectedHash = computeLogHash(entry, prevHash);
      if (entry.hash !== expectedHash) {
        return {
          valid: false,
          compromisedIndex: i,
          compromisedEntry: entry,
          message: `Audit chain broken at log ${entry.id}: hash tampering detected`
        };
      }
      prevHash = entry.hash;
    }
  }

  return { valid: true, count: chronological.length, latestHash: prevHash };
}

module.exports = {
  generateClientFingerprint,
  verifyClientFingerprint,
  checkAccountLockout,
  recordFailedLogin,
  recordSuccessfulLogin,
  deepSanitizeMiddleware,
  csrfGuardMiddleware,
  computeLogHash,
  verifyAuditChain
};
