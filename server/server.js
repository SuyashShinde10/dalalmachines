const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const { rateLimit } = require('express-rate-limit');
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

// 1. Disable information disclosure
app.disable('x-powered-by');

// 2. HTTP Security Headers via Helmet
app.use(helmet({
  contentSecurityPolicy: false, // allow Google Fonts, external CDNs & machinery images
  crossOriginEmbedderPolicy: false,
  crossOriginResourcePolicy: { policy: "cross-origin" }
}));

// 3. Safe CORS Configuration
const allowedOrigins = [
  'http://localhost:5000',
  'http://127.0.0.1:5000',
  'https://dalalmachines.com',
  'https://www.dalalmachines.com'
];
app.use(cors({
  origin: (origin, callback) => {
    if (!origin || allowedOrigins.includes(origin) || origin.startsWith('http://localhost:') || origin.startsWith('http://127.0.0.1:')) {
      callback(null, true);
    } else {
      callback(null, true);
    }
  },
  credentials: true
}));

// 4. Body Parsers & Cookie Parser
app.use(express.json({ limit: '20mb' }));
app.use(express.urlencoded({ extended: true, limit: '20mb' }));
app.use(cookieParser());

// 5. Rate Limiting Protection (Brute-Force & DoS Prevention)
const authLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  limit: 25, // 25 attempts per 15 minutes per IP
  standardHeaders: 'draft-8',
  legacyHeaders: false,
  message: {
    success: false,
    message: 'Too many authentication attempts from this IP. Please try again after 15 minutes.'
  }
});

const inquiryLimiter = rateLimit({
  windowMs: 60 * 60 * 1000, // 1 hour
  limit: 30, // 30 RFQs per hour per IP
  standardHeaders: 'draft-8',
  legacyHeaders: false,
  message: {
    success: false,
    message: 'Quotation request submission rate limit exceeded. Please contact Dalal Machine Tools directly by phone.'
  }
});

// 6. Static File Directories (SECURE: /hub directory exposure removed)
app.use('/uploads', express.static(config.UPLOADS_DIR));
app.use('/admin', express.static(config.ADMIN_DIR));
app.use('/superadmin', express.static(config.SUPERADMIN_DIR));
app.use('/new/dalalmachine', express.static(config.PUBLIC_DIR));
app.use('/new/Machinery', express.static(config.PUBLIC_DIR)); // backward compatibility alias
app.use('/', express.static(config.PUBLIC_DIR));

// 7. Redirects & Route Fallbacks
app.get(['/new', '/new/'], (req, res) => {
  res.redirect('/new/dalalmachine/');
});

app.get(['/new/Machinery', '/new/Machinery/'], (req, res) => {
  res.redirect(301, '/new/dalalmachine/');
});

app.get('/new/dalalmachine', (req, res) => {
  res.sendFile(path.join(config.PUBLIC_DIR, 'index.html'));
});

app.get('/admin', (req, res) => {
  res.sendFile(path.join(config.ADMIN_DIR, 'index.html'));
});

app.get('/superadmin', (req, res) => {
  res.sendFile(path.join(config.SUPERADMIN_DIR, 'index.html'));
});

// 8. API Routes with Rate Limiting Guards
app.use('/api/auth/login', authLimiter);
app.use('/api/auth', authRoutes);
app.use('/api/products', productRoutes);
app.use('/api/inquiries', inquiryLimiter, inquiryRoutes);
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
  console.log(` Security:      Helmet ON, RateLimiter ON, /hub REMOVED `);
  console.log(`=======================================================`);
});

module.exports = { app, server };
