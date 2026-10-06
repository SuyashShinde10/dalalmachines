const express = require('express');
const router = express.Router();
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const config = require('../config');
const db = require('../db');
const { authenticateToken } = require('../middleware/auth');

// POST /api/auth/login
router.post('/login', (req, res) => {
  const { identifier, password } = req.body;
  if (!identifier || !password) {
    return res.status(400).json({ success: false, message: 'Please provide username/email and password.' });
  }

  const user = db.getUserByUsernameOrEmail(identifier);
  if (!user) {
    return res.status(401).json({ success: false, message: 'Invalid credentials. User not found.' });
  }

  if (!user.active) {
    return res.status(403).json({ success: false, message: 'Your account has been deactivated. Contact super admin.' });
  }

  const isMatch = bcrypt.compareSync(password, user.passwordHash);
  if (!isMatch) {
    return res.status(401).json({ success: false, message: 'Invalid password. Please try again.' });
  }

  // Update last login
  db.updateUserLoginTimestamp(user.id);

  // Sign JWT
  const token = jwt.sign(
    {
      id: user.id,
      username: user.username,
      email: user.email,
      role: user.role
    },
    config.JWT_SECRET,
    { expiresIn: config.JWT_EXPIRY }
  );

  // Set HTTP-only cookie as well for easy browser navigation
  res.cookie('admin_token', token, {
    httpOnly: true,
    maxAge: 7 * 24 * 60 * 60 * 1000,
    sameSite: 'lax'
  });

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
  const { passwordHash, ...safeUser } = user;
  return res.json({ success: true, user: safeUser });
});

// POST /api/auth/logout
router.post('/logout', (req, res) => {
  res.clearCookie('admin_token');
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
