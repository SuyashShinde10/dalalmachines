const express = require('express');
const router = express.Router();
const db = require('../db');
const { requireSuperAdmin } = require('../middleware/auth');

router.use(...requireSuperAdmin);

// GET /api/system/stats
router.get('/stats', (req, res) => {
  const products = db.getProducts({ all: 'true' });
  const formingCount = products.filter(p => p.section === 'forming').length;
  const cuttingCount = products.filter(p => p.section === 'cutting').length;
  const customCount = products.filter(p => p.isCustom).length;
  const users = db.getUsers();
  const inquiries = db.getInquiries();
  const newInquiries = inquiries.filter(i => i.status === 'new').length;

  res.json({
    success: true,
    stats: {
      totalMachines: products.length,
      formingMachines: formingCount,
      cuttingMachines: cuttingCount,
      customMachines: customCount,
      puneStock: products.filter(p => (p.location || '').toLowerCase().includes('pune')).length,
      totalUsers: users.length,
      adminCount: users.filter(u => u.role === 'admin').length,
      superAdminCount: users.filter(u => u.role === 'superadmin').length,
      totalInquiries: inquiries.length,
      newInquiries: newInquiries,
      uptimeSeconds: Math.floor(process.uptime()),
      memoryUsageMB: Math.round(process.memoryUsage().rss / 1024 / 1024),
      nodeVersion: process.version
    }
  });
});

// GET /api/system/settings
router.get('/settings', (req, res) => {
  res.json({ success: true, settings: db.getSettings() });
});

// PUT /api/system/settings
router.put('/settings', (req, res) => {
  const updated = db.updateSettings(req.body, req.user);
  res.json({ success: true, message: 'Settings saved successfully.', settings: updated });
});

// GET /api/system/backup (Download Latest DB snapshot)
router.get('/backup', (req, res) => {
  const backup = db.getBackup();
  res.setHeader('Content-Type', 'application/json');
  res.setHeader('Content-Disposition', `attachment; filename=dalal_backup_${Date.now()}.json`);
  res.send(JSON.stringify(backup, null, 2));
});

// GET /api/system/backups (List rolling daily backups)
router.get('/backups', (req, res) => {
  const backupEngine = require('../services/backupEngine');
  res.json({ success: true, backups: backupEngine.listBackups() });
});

// POST /api/system/backups/create (Trigger immediate manual backup)
router.post('/backups/create', (req, res) => {
  const backupEngine = require('../services/backupEngine');
  const result = backupEngine.createDailyBackup();
  if (result && result.success) {
    res.json({ success: true, message: 'Backup created successfully.', backup: result.fileName });
  } else {
    res.status(500).json({ success: false, message: 'Failed to create backup: ' + (result ? result.error : 'Unknown error') });
  }
});

// GET /api/system/backups/download/:filename (Download specific backup file)
router.get('/backups/download/:filename', (req, res) => {
  const path = require('path');
  const fs = require('fs');
  const backupEngine = require('../services/backupEngine');
  const safeFilename = path.basename(req.params.filename);
  const targetPath = path.join(backupEngine.BACKUP_DIR, safeFilename);

  if (!fs.existsSync(targetPath)) {
    return res.status(404).json({ success: false, message: 'Backup file not found.' });
  }

  res.setHeader('Content-Type', 'application/json');
  res.setHeader('Content-Disposition', `attachment; filename="${safeFilename}"`);
  res.sendFile(targetPath);
});

// POST /api/system/restore
router.post('/restore', (req, res) => {
  try {
    db.restoreBackup(req.body, req.user);
    res.json({ success: true, message: 'Database restored successfully from backup.' });
  } catch (err) {
    res.status(400).json({ success: false, message: 'Restore failed: ' + err.message });
  }
});

// POST /api/system/sync-static
router.post('/sync-static', (req, res) => {
  try {
    db.syncToCatalogJs();
    res.json({ 
      success: true, 
      message: 'Successfully exported active database inventory to new/dalalmachine/js/catalog-data.js!' 
    });
  } catch (err) {
    res.status(500).json({ success: false, message: 'Sync failed: ' + err.message });
  }
});

module.exports = router;
