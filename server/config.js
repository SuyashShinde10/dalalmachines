const path = require('path');

const isProduction = process.env.NODE_ENV === 'production';
const jwtSecret = process.env.JWT_SECRET || 'dalal_machinery_super_secure_jwt_secret_2026_9482!';

if (isProduction && (!process.env.JWT_SECRET || process.env.JWT_SECRET.length < 32)) {
  console.warn('⚠️ SECURITY WARNING: Strong random JWT_SECRET must be set in production environment variables.');
}

module.exports = {
  PORT: process.env.PORT || 5000,
  JWT_SECRET: jwtSecret,
  JWT_EXPIRY: process.env.JWT_EXPIRY || '7d',
  
  // Data Paths
  DATA_DIR: path.join(__dirname, 'data'),
  DB_FILE: path.join(__dirname, 'data', 'db.json'),
  UPLOADS_DIR: path.join(__dirname, 'data', 'uploads'),
  PUBLIC_DIR: path.join(__dirname, '..', 'new', 'dalalmachine'),
  ADMIN_DIR: path.join(__dirname, '..', 'admin'),
  SUPERADMIN_DIR: path.join(__dirname, '..', 'superadmin'),
  DEV_DIR: path.join(__dirname, '..', 'dev'),
  CATALOG_JS_PATH: path.join(__dirname, '..', 'new', 'dalalmachine', 'js', 'catalog-data.js'),

  // Enterprise Security Architecture & URL Cloaking Controls
  PORTAL_GATEWAY_KEY: process.env.PORTAL_GATEWAY_KEY || 'dmta-ops-2026',
  GATEWAY_COOKIE_NAME: 'dmta_gate_pass',
  GATEWAY_COOKIE_SECRET: process.env.GATEWAY_COOKIE_SECRET || 'dmta_secret_gate_sign_key_9941',
  ALLOWED_DEV_IPS: (process.env.ALLOWED_DEV_IPS || '127.0.0.1,::1,::ffff:127.0.0.1,localhost,*').split(',').map(s => s.trim().toLowerCase()),
  SECURITY_EVENTS_FILE: path.join(__dirname, 'data', 'security_events.json'),
  BLACKLIST_FILE: path.join(__dirname, 'data', 'blacklist.json'),
  HONEYPOT_ENABLED: process.env.HONEYPOT_ENABLED !== 'false',
  MAX_FAILED_LOGIN_ATTEMPTS: 5,
  BAN_DURATION_MS: 24 * 60 * 60 * 1000 // 24 hours
};
