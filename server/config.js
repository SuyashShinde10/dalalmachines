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
  DATA_DIR: path.join(__dirname, 'data'),
  DB_FILE: path.join(__dirname, 'data', 'db.json'),
  UPLOADS_DIR: path.join(__dirname, 'data', 'uploads'),
  PUBLIC_DIR: path.join(__dirname, '..', 'new', 'dalalmachine'),
  ADMIN_DIR: path.join(__dirname, '..', 'admin'),
  SUPERADMIN_DIR: path.join(__dirname, '..', 'superadmin'),
  CATALOG_JS_PATH: path.join(__dirname, '..', 'new', 'dalalmachine', 'js', 'catalog-data.js')
};
