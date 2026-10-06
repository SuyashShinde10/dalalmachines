const jwt = require('jsonwebtoken');
const config = require('../config');
const db = require('../db');

function authenticateToken(req, res, next) {
  let token = null;

  // Check Authorization header: Bearer <token>
  const authHeader = req.headers['authorization'];
  if (authHeader && authHeader.startsWith('Bearer ')) {
    token = authHeader.split(' ')[1];
  } else if (req.cookies && req.cookies.admin_token) {
    token = req.cookies.admin_token;
  }

  if (!token) {
    return res.status(401).json({ success: false, message: 'Authentication required. Please log in.' });
  }

  try {
    const decoded = jwt.verify(token, config.JWT_SECRET);
    // Verify user still exists and is active in DB
    const user = db.getUserById(decoded.id);
    if (!user || !user.active) {
      return res.status(403).json({ success: false, message: 'User account is inactive or not found.' });
    }
    req.user = {
      id: user.id,
      username: user.username,
      email: user.email,
      name: user.name,
      role: user.role
    };
    next();
  } catch (err) {
    return res.status(403).json({ success: false, message: 'Invalid or expired session token.' });
  }
}

function requireRole(allowedRoles) {
  return (req, res, next) => {
    if (!req.user) {
      return res.status(401).json({ success: false, message: 'Unauthorized' });
    }
    if (!allowedRoles.includes(req.user.role)) {
      return res.status(403).json({ 
        success: false, 
        message: `Forbidden: Requires one of [${allowedRoles.join(', ')}] permissions.` 
      });
    }
    next();
  };
}

const requireAdmin = [authenticateToken, requireRole(['admin', 'superadmin'])];
const requireSuperAdmin = [authenticateToken, requireRole(['superadmin'])];

module.exports = {
  authenticateToken,
  requireRole,
  requireAdmin,
  requireSuperAdmin
};
