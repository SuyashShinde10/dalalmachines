const express = require('express');
const cors = require('cors');
const cookieParser = require('cookie-parser');
const path = require('path');
const config = require('./config');

const authRoutes = require('./routes/auth');
const productRoutes = require('./routes/products');
const inquiryRoutes = require('./routes/inquiries');
const userRoutes = require('./routes/users');
const logRoutes = require('./routes/logs');
const systemRoutes = require('./routes/system');

const app = express();

// Middlewares
app.use(cors());
app.use(express.json({ limit: '20mb' }));
app.use(express.urlencoded({ extended: true, limit: '20mb' }));
app.use(cookieParser());

// Static File Directories
app.use('/uploads', express.static(config.UPLOADS_DIR));
app.use('/admin', express.static(config.ADMIN_DIR));
app.use('/', express.static(config.PUBLIC_DIR));

// API Routes
app.use('/api/auth', authRoutes);
app.use('/api/products', productRoutes);
app.use('/api/inquiries', inquiryRoutes);
app.use('/api/users', userRoutes);
app.use('/api/logs', logRoutes);
app.use('/api/system', systemRoutes);

// Health check endpoint
app.get('/api/health', (req, res) => {
  res.json({
    status: 'ok',
    timestamp: new Date().toISOString(),
    uptime: process.uptime()
  });
});

// Default admin route fallback
app.get('/admin', (req, res) => {
  res.sendFile(path.join(config.ADMIN_DIR, 'index.html'));
});

// Global Error Handler
app.use((err, req, res, next) => {
  console.error('Unhandled server error:', err);
  res.status(err.status || 500).json({
    success: false,
    message: err.message || 'Internal server error occurred.'
  });
});

// Start Server
const PORT = config.PORT;
const server = app.listen(PORT, () => {
  console.log(`=======================================================`);
  console.log(` Dalal Machine Tools - Fullstack Backend & Admin Portal `);
  console.log(`=======================================================`);
  console.log(` Web Server:    http://localhost:${PORT}/`);
  console.log(` Admin Portal:  http://localhost:${PORT}/admin/`);
  console.log(` API Endpoint:  http://localhost:${PORT}/api/health`);
  console.log(`=======================================================`);
});

module.exports = { app, server };
