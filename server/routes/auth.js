const express = require('express');
const router = express.Router();
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const config = require('../config');
const db = require('../db');
const { authenticateToken, requireSuperAdmin } = require('../middleware/auth');
const totp = require('../security/totp');
const {
  checkAccountLockout,
  recordFailedLogin,
  recordSuccessfulLogin,
  generateClientFingerprint
} = require('../security/defenseInDepth');

// POST /api/auth/login
router.post('/login', async (req, res) => {
  const { identifier, password, totpCode } = req.body;
  if (!identifier || !password) {
    return res.status(400).json({ success: false, message: 'Please provide username/email and password.' });
  }

  // 1. Check Account-Level Lockout (Brute-Force & Credential Stuffing Defense)
  const lockout = checkAccountLockout(identifier);
  if (lockout.locked) {
    return res.status(429).json({
      success: false,
      locked: true,
      remainingSeconds: lockout.remainingSeconds,
      message: `Account is temporarily locked due to excessive failed attempts. Try again in ${lockout.remainingSeconds} seconds.`
    });
  }

  const user = db.getUserByUsernameOrEmail(identifier);
  if (!user) {
    await recordFailedLogin(identifier, req);
    return res.status(401).json({ success: false, message: 'Invalid credentials. User not found.' });
  }

  if (user.blockedByDeveloper) {
    return res.status(403).json({
      success: false,
      blockedByDeveloper: true,
      blockedReason: user.blockedReason || 'This account has been suspended by the Lead System Developer.',
      blockedAt: user.blockedAt || null,
      role: user.role,
      message: `ACCOUNT SUSPENDED: This ${user.role} account has been blocked by the System Developer. Reason: ${user.blockedReason || 'Administrative suspension'}. Contact system developer for clearance.`
    });
  }

  if (!user.active) {
    return res.status(403).json({ success: false, message: 'Your account has been deactivated. Contact super admin.' });
  }

  const isMatch = bcrypt.compareSync(password, user.passwordHash);
  if (!isMatch) {
    await recordFailedLogin(identifier, req);
    return res.status(401).json({ success: false, message: 'Invalid password. Please try again.' });
  }

  // 2-Factor Authentication (TOTP / Google Authenticator) Check
  if (user.twoFactorEnabled && user.twoFactorSecret) {
    if (!totpCode) {
      const tempToken = jwt.sign(
        { tempId: user.id, requires2fa: true },
        config.JWT_SECRET,
        { expiresIn: '5m' }
      );
      return res.json({
        success: true,
        require2fa: true,
        tempToken,
        message: 'Two-Factor Authentication required. Enter the 6-digit code from Google Authenticator.'
      });
    }

    const isValidOtp = totp.verifyTotp(user.twoFactorSecret, totpCode) ||
      (user.twoFactorRecoveryCode && user.twoFactorRecoveryCode === totpCode.trim());

    if (!isValidOtp) {
      await recordFailedLogin(identifier, req);
      return res.status(401).json({ success: false, message: 'Invalid 2FA code or backup recovery code.' });
    }
  }

  // Clear failure records on successful login
  recordSuccessfulLogin(identifier);

  // Update last login
  db.updateUserLoginTimestamp(user.id);

  // Generate client device fingerprint (Anti-Session-Replay)
  const fp = generateClientFingerprint(req);

  // Sign JWT with client device fingerprint
  const token = jwt.sign(
    {
      id: user.id,
      username: user.username,
      email: user.email,
      role: user.role,
      fp
    },
    config.JWT_SECRET,
    { expiresIn: config.JWT_EXPIRY }
  );

  // Set HTTP-only cookie as well for easy browser navigation
  const isHttps = req.secure || req.headers['x-forwarded-proto'] === 'https';
  res.cookie('admin_token', token, {
    httpOnly: true,
    maxAge: 7 * 24 * 60 * 60 * 1000,
    sameSite: 'lax',
    secure: isHttps,
    path: '/'
  });

  if (user.role === 'superadmin' || user.role === 'developer') {
    res.cookie('superadmin_token', token, {
      httpOnly: true,
      maxAge: 7 * 24 * 60 * 60 * 1000,
      sameSite: 'lax',
      secure: isHttps,
      path: '/'
    });
  }

  db.addLog({
    userId: user.id,
    username: user.username,
    role: user.role,
    action: 'USER_LOGIN',
    target: 'AUTH',
    details: `User logged in successfully from ${req.ip || 'local'}`
  });

  const { passwordHash, ...safeUser } = user;
  return res.json({
    success: true,
    message: 'Login successful.',
    token,
    user: safeUser
  });
});

// GET /api/auth/me
router.get('/me', authenticateToken, (req, res) => {
  const user = db.getUserById(req.user.id);
  if (!user) {
    return res.status(404).json({ success: false, message: 'User not found' });
  }
  const { passwordHash, twoFactorSecret, ...safeUser } = user;
  return res.json({
    success: true,
    user: {
      ...safeUser,
      twoFactorEnabled: Boolean(user.twoFactorEnabled)
    }
  });
});

// POST /api/auth/2fa/generate (Superadmin Setup RFC 6238 2FA)
router.post('/2fa/generate', authenticateToken, (req, res) => {
  const user = db.getUserById(req.user.id);
  if (!user) return res.status(404).json({ success: false, message: 'User not found.' });

  const generated = totp.generateSecret(user.username, 'Dalal Machine Tools');
  res.json({
    success: true,
    secret: generated.secret,
    qrUrl: generated.qrUrl,
    uri: generated.uri,
    recoveryCode: generated.recoveryCode
  });
});

// POST /api/auth/2fa/verify-and-enable
router.post('/2fa/verify-and-enable', authenticateToken, (req, res) => {
  const { secret, token, recoveryCode } = req.body;
  if (!secret || !token) {
    return res.status(400).json({ success: false, message: 'Secret and 6-digit TOTP token are required.' });
  }

  const isValid = totp.verifyTotp(secret, token);
  if (!isValid) {
    return res.status(400).json({ success: false, message: 'Invalid 6-digit code. Check your Authenticator app and system clock.' });
  }

  db.setUser2FA(req.user.id, { enabled: true, secret, recoveryCode }, req.user);
  res.json({
    success: true,
    message: 'Two-Factor Authentication successfully activated. Master Console is now secured with RFC 6238 TOTP.',
    twoFactorEnabled: true
  });
});

// POST /api/auth/2fa/disable
router.post('/2fa/disable', authenticateToken, (req, res) => {
  const { password, token } = req.body;
  const user = db.getUserById(req.user.id);
  if (!user) return res.status(404).json({ success: false, message: 'User not found.' });

  if (password) {
    const isMatch = bcrypt.compareSync(password, user.passwordHash);
    if (!isMatch) return res.status(401).json({ success: false, message: 'Incorrect password.' });
  } else if (token) {
    const isValid = totp.verifyTotp(user.twoFactorSecret, token);
    if (!isValid) return res.status(401).json({ success: false, message: 'Invalid 2FA token.' });
  } else {
    return res.status(400).json({ success: false, message: 'Password or 2FA token required to disable 2FA.' });
  }

  db.setUser2FA(req.user.id, { enabled: false, secret: null, recoveryCode: null }, req.user);
  res.json({
    success: true,
    message: 'Two-Factor Authentication deactivated.',
    twoFactorEnabled: false
  });
});

// POST /api/auth/logout
router.post('/logout', (req, res) => {
  res.clearCookie('admin_token', { path: '/' });
  res.clearCookie('superadmin_token', { path: '/' });
  res.clearCookie(config.GATEWAY_COOKIE_NAME, { path: '/' });
  return res.json({ success: true, message: 'Logged out successfully.' });
});

// PUT /api/auth/profile
router.put('/profile', authenticateToken, (req, res) => {
  const { name, email, currentPassword, newPassword } = req.body;
  const user = db.getUserById(req.user.id);

  if (newPassword) {
    if (newPassword.length < 8) {
      return res.status(400).json({ success: false, message: 'New password must be at least 8 characters long.' });
    }
    if (!currentPassword) {
      return res.status(400).json({ success: false, message: 'Current password required to set a new password.' });
    }
    const isMatch = bcrypt.compareSync(currentPassword, user.passwordHash);
    if (!isMatch) {
      return res.status(400).json({ success: false, message: 'Current password is incorrect.' });
    }
  }

  const updated = db.updateUser(req.user.id, {
    name,
    email,
    password: newPassword || undefined
  }, req.user);

  return res.json({ success: true, message: 'Profile updated successfully.', user: updated });
});

module.exports = router;
