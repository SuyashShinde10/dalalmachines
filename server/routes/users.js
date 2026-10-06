const express = require('express');
const router = express.Router();
const db = require('../db');
const { requireSuperAdmin } = require('../middleware/auth');

// All routes here require Super Admin role
router.use(...requireSuperAdmin);

// GET /api/users (List all users)
router.get('/', (req, res) => {
  const users = db.getUsers();
  res.json({ success: true, count: users.length, users });
});

// POST /api/users (Create new user)
router.post('/', (req, res) => {
  const { username, email, password, role, name } = req.body;
  if (!username || !email || !password) {
    return res.status(400).json({ success: false, message: 'Username, email, and password are required.' });
  }

  if (password.length < 8) {
    return res.status(400).json({ success: false, message: 'Password must be at least 8 characters long.' });
  }

  // Check if username or email already exists
  const existing = db.getUserByUsernameOrEmail(username) || db.getUserByUsernameOrEmail(email);
  if (existing) {
    return res.status(400).json({ success: false, message: 'A user with that username or email already exists.' });
  }

  try {
    const created = db.createUser({ username, email, password, role, name }, req.user);
    res.status(201).json({ success: true, message: 'User account created successfully.', user: created });
  } catch (err) {
    res.status(500).json({ success: false, message: err.message });
  }
});

// PUT /api/users/:id (Update user / reset password / toggle active)
router.put('/:id', (req, res) => {
  const user = db.getUserById(req.params.id);
  if (!user) {
    return res.status(404).json({ success: false, message: 'User not found.' });
  }
  if (req.body.password && req.body.password.length < 8) {
    return res.status(400).json({ success: false, message: 'Password must be at least 8 characters long.' });
  }

  // Check if changing role from superadmin and it's the last superadmin
  if (req.body.role && req.body.role !== 'superadmin' && user.role === 'superadmin') {
    const superAdmins = db.getUsers().filter(u => u.role === 'superadmin' && u.active);
    if (superAdmins.length <= 1 && superAdmins[0].id === user.id) {
      return res.status(400).json({ success: false, message: 'Cannot demote the last active super admin.' });
    }
  }

  try {
    const updated = db.updateUser(req.params.id, req.body, req.user);
    res.json({ success: true, message: 'User updated successfully.', user: updated });
  } catch (err) {
    res.status(500).json({ success: false, message: err.message });
  }
});

// DELETE /api/users/:id (Delete user)
router.delete('/:id', (req, res) => {
  if (req.params.id === req.user.id) {
    return res.status(400).json({ success: false, message: 'You cannot delete your own account while logged in.' });
  }

  const user = db.getUserById(req.params.id);
  if (!user) {
    return res.status(404).json({ success: false, message: 'User not found.' });
  }

  if (user.role === 'superadmin') {
    const superAdmins = db.getUsers().filter(u => u.role === 'superadmin');
    if (superAdmins.length <= 1) {
      return res.status(400).json({ success: false, message: 'Cannot delete the last super admin account.' });
    }
  }

  const ok = db.deleteUser(req.params.id, req.user);
  if (ok) {
    res.json({ success: true, message: `User ${user.username} deleted successfully.` });
  } else {
    res.status(500).json({ success: false, message: 'Failed to delete user.' });
  }
});

module.exports = router;
