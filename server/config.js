const path = require('path');

module.exports = {
  PORT: process.env.PORT || 5000,
  JWT_SECRET: process.env.JWT_SECRET || 'dalal_machinery_super_secure_jwt_secret_2026_9482!',
  JWT_EXPIRY: '7d',
  DATA_DIR: path.join(__dirname, 'data'),
  DB_FILE: path.join(__dirname, 'data', 'db.json'),
  UPLOADS_DIR: path.join(__dirname, 'data', 'uploads'),
  PUBLIC_DIR: path.join(__dirname, '..', 'new', 'Machinery'),
  ADMIN_DIR: path.join(__dirname, '..', 'admin'),
  SUPERADMIN_DIR: path.join(__dirname, '..', 'superadmin'),
  CATALOG_JS_PATH: path.join(__dirname, '..', 'new', 'Machinery', 'js', 'catalog-data.js')
};
