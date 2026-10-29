const fs = require('fs');
const path = require('path');
const config = require('../config');

const BACKUP_DIR = path.join(config.DATA_DIR, 'backups');
const MAX_BACKUPS = 30; // Keep last 30 daily snapshots

// Ensure backups directory exists
if (!fs.existsSync(BACKUP_DIR)) {
  fs.mkdirSync(BACKUP_DIR, { recursive: true });
}

/**
 * Creates a timestamped daily backup snapshot of db.json
 */
function createDailyBackup() {
  try {
    const dbPath = config.DB_FILE;
    if (!fs.existsSync(dbPath)) return null;

    const today = new Date().toISOString().split('T')[0];
    const backupFileName = `db_backup_${today}.json`;
    const backupFilePath = path.join(BACKUP_DIR, backupFileName);

    // Copy current db.json to backup file
    fs.copyFileSync(dbPath, backupFilePath);

    // Prune old backups older than MAX_BACKUPS
    pruneOldBackups();

    return { success: true, fileName: backupFileName, path: backupFilePath };
  } catch (err) {
    console.error('[BackupEngine Error]:', err.message);
    return { success: false, error: err.message };
  }
}

/**
 * Prunes backups keeping only the most recent MAX_BACKUPS files
 */
function pruneOldBackups() {
  try {
    const files = fs.readdirSync(BACKUP_DIR)
      .filter(f => f.startsWith('db_backup_') && f.endsWith('.json'))
      .map(f => ({
        name: f,
        time: fs.statSync(path.join(BACKUP_DIR, f)).mtime.getTime()
      }))
      .sort((a, b) => b.time - a.time);

    if (files.length > MAX_BACKUPS) {
      const toDelete = files.slice(MAX_BACKUPS);
      toDelete.forEach(file => {
        fs.unlinkSync(path.join(BACKUP_DIR, file.name));
      });
    }
  } catch (err) {
    console.error('[BackupEngine Prune Error]:', err.message);
  }
}

/**
 * Returns a list of all existing backup files with metadata
 */
function listBackups() {
  try {
    if (!fs.existsSync(BACKUP_DIR)) return [];
    return fs.readdirSync(BACKUP_DIR)
      .filter(f => f.startsWith('db_backup_') && f.endsWith('.json'))
      .map(f => {
        const filePath = path.join(BACKUP_DIR, f);
        const stats = fs.statSync(filePath);
        return {
          fileName: f,
          sizeBytes: stats.size,
          sizeKb: (stats.size / 1024).toFixed(1) + ' KB',
          createdAt: stats.mtime.toISOString()
        };
      })
      .sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt));
  } catch (err) {
    console.error('[BackupEngine List Error]:', err.message);
    return [];
  }
}

// Run immediate snapshot on boot and schedule every 24 hours
createDailyBackup();
setInterval(createDailyBackup, 24 * 60 * 60 * 1000);

module.exports = {
  createDailyBackup,
  listBackups,
  BACKUP_DIR
};
