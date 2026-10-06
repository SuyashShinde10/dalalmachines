const express = require('express');
const router = express.Router();
const db = require('../db');
const { requireSuperAdmin } = require('../middleware/auth');

router.use(...requireSuperAdmin);

// GET /api/logs (Activity logs)
router.get('/', (req, res) => {
  const limit = parseInt(req.query.limit) || 200;
  const logs = db.getLogs(limit);
  res.json({ success: true, count: logs.length, logs });
});

module.exports = router;
