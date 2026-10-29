const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const compression = require('compression');
const { rateLimit } = require('express-rate-limit');
const cookieParser = require('cookie-parser');
const fs = require('fs');
const path = require('path');
const http = require('http');
const config = require('./config');
const db = require('./db');
const realtime = require('./realtime');

const authRoutes = require('./routes/auth');
const productRoutes = require('./routes/products');
const inquiryRoutes = require('./routes/inquiries');
const userRoutes = require('./routes/users');
const logRoutes = require('./routes/logs');
const systemRoutes = require('./routes/system');
const aiRoutes = require('./routes/ai');
const devRoutes = require('./routes/dev');
const seoRoutes = require('./routes/seo');

// Enterprise SecOps & Concealment Engine
const honeypot = require('./security/honeypot');
const gateway = require('./security/gateway');
const routeShield = require('./security/routeShield');
const defenseInDepth = require('./security/defenseInDepth');
const cacheEngine = require('./performance/cacheEngine');

const app = express();

// 1. Gzip/Brotli Compression & Disable information disclosure
app.use(compression());
app.disable('x-powered-by');

// 2. Bank-Grade HTTP Security Headers & CSP Level 3 Defense
app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      scriptSrc: ["'self'", "'unsafe-inline'", "'unsafe-eval'", "https://cdnjs.cloudflare.com", "https://fonts.googleapis.com", "https://cdn.socket.io", "https://cdn.jsdelivr.net"],
      styleSrc: ["'self'", "'unsafe-inline'", "https://fonts.googleapis.com", "https://cdnjs.cloudflare.com"],
      fontSrc: ["'self'", "https://fonts.gstatic.com", "https://cdnjs.cloudflare.com", "data:"],
      imgSrc: ["'self'", "data:", "blob:", "https:"],
      connectSrc: ["'self'", "ws:", "wss:", "http:", "https:"],
      frameSrc: ["'self'", "https://www.google.com", "https://maps.google.com"],
      frameAncestors: ["'none'"],
      baseUri: ["'self'"],
      formAction: ["'self'"]
    }
  },
  crossOriginEmbedderPolicy: false,
  crossOriginOpenerPolicy: { policy: "same-origin-allow-popups" },
  crossOriginResourcePolicy: { policy: "cross-origin" },
  hsts: { maxAge: 63072000, includeSubDomains: true, preload: true },
  frameguard: { action: "deny" },
  noSniff: true,
  referrerPolicy: { policy: "strict-origin-when-cross-origin" }
}));

// Restrict sensitive hardware APIs (Permissions-Policy)
app.use((req, res, next) => {
  res.setHeader('Permissions-Policy', 'camera=(), microphone=(), geolocation=(), payment=()');
  next();
});

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

// 4a. Deep Recursive Request Sanitization & Prototype Pollution Guard
app.use(defenseInDepth.deepSanitizeMiddleware);

// 4b. CSRF & State-Changing Mutation Guard
app.use('/api', defenseInDepth.csrfGuardMiddleware);

// 4c. SecOps Firewall: Drop traffic from actively blacklisted IPs
app.use(honeypot.blacklistGuardMiddleware);

// 4d. Authorized Staff Portal Gateway Endpoints (Secret Key Gatekeeper)
app.get('/portal-gate', gateway.handleGatewayEntry);
app.post('/portal-gate', gateway.handleGatewayEntry);
app.get('/portal-exit', gateway.handleGatewayRevoke);

// 4d2. PWA Manifest & Service Worker Endpoints (Offline Warehouse Mode)
app.get('/manifest.json', (req, res) => {
  res.sendFile(path.join(config.PUBLIC_DIR, 'manifest.json'));
});
app.get('/sw.js', (req, res) => {
  res.setHeader('Content-Type', 'application/javascript');
  res.setHeader('Service-Worker-Allowed', '/');
  res.sendFile(path.join(config.PUBLIC_DIR, 'sw.js'));
});

// 4d3. Dynamic Dynamic XML Sitemap & Robots.txt Engine (GEO/AEO/SEO)
app.use('/', seoRoutes);

// 4e. Honeypot Deception Traps: Detect & auto-ban scanners probing common attack paths
const honeypotPatterns = [
  /^\/wp-(admin|login|includes|content)/i,
  /^\/administrator/i,
  /^\/admin\.php/i,
  /^\/(cpanel|phpmyadmin|pma|mysql|dbadmin)/i,
  /^\/(\.env|\.git|config\.json|web\.config|xmlrpc\.php)/i,
  /^\/(actuator|shell|cmd)/i
];
app.use((req, res, next) => {
  const p = req.path.toLowerCase();
  for (const pattern of honeypotPatterns) {
    if (pattern.test(p)) {
      return honeypot.honeypotHandler(req, res);
    }
  }
  next();
});

// 4b. Enforce Zero-Cache on all Administrative, Developer, & API Portals (Instant Duplex Sync)
app.use((req, res, next) => {
  const p = req.path.toLowerCase();
  if (p.startsWith('/admin') || p.startsWith('/superadmin') || p.startsWith('/dev') || p.startsWith('/api')) {
    res.setHeader('Cache-Control', 'no-store, no-cache, must-revalidate, proxy-revalidate, max-age=0');
    res.setHeader('Pragma', 'no-cache');
    res.setHeader('Expires', '0');
  }
  next();
});

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

// 6. High-Performance Static File Serving with Precision Cache Strategy
const staticOptions = {
  etag: true,
  lastModified: true,
  maxAge: '1d',
  setHeaders: (res, filePath) => {
    // Admin, Superadmin, and Dev portals must NEVER be cached to ensure instant real-time synchronization
    const normalized = filePath.replace(/\\/g, '/');
    if (normalized.includes('/admin/') || normalized.includes('/superadmin/') || normalized.includes('/dev/')) {
      res.setHeader('Cache-Control', 'no-store, no-cache, must-revalidate, proxy-revalidate');
      res.setHeader('Pragma', 'no-cache');
      res.setHeader('Expires', '0');
      return;
    }

    if (/\.html$/i.test(filePath)) {
      res.setHeader('Cache-Control', 'public, max-age=0, must-revalidate');
    } else if (/\.(jpg|jpeg|png|gif|webp|svg|ico|woff|woff2|ttf|eot)$/i.test(filePath)) {
      res.setHeader('Cache-Control', 'public, max-age=2592000, immutable'); // 30 days cache for immutable assets
    } else if (/\.(css|js)$/i.test(filePath)) {
      res.setHeader('Cache-Control', 'public, max-age=86400, stale-while-revalidate=604800');
    }
  }
};

// 6. Transparent High-Speed WebP Content Negotiation
app.use((req, res, next) => {
  if (req.method !== 'GET' && req.method !== 'HEAD') return next();
  const accept = req.headers['accept'] || '';
  if (!accept.includes('image/webp')) return next();
  
  if (/\.(jpe?g|png)$/i.test(req.path)) {
    let relPath = req.path;
    if (relPath.startsWith('/new/dalalmachine/')) relPath = relPath.replace('/new/dalalmachine/', '');
    else if (relPath.startsWith('/new/Machinery/')) relPath = relPath.replace('/new/Machinery/', '');
    else if (relPath.startsWith('/')) relPath = relPath.substring(1);

    const webpRel = relPath.replace(/\.(jpe?g|png)$/i, '.webp');
    const candidatePath = path.join(config.PUBLIC_DIR, webpRel);

    if (fs.existsSync(candidatePath)) {
      res.setHeader('Content-Type', 'image/webp');
      res.setHeader('Vary', 'Accept');
      res.setHeader('Cache-Control', 'public, max-age=2592000, immutable');
      return res.sendFile(candidatePath);
    }
  }
  next();
});

app.use('/uploads', express.static(config.UPLOADS_DIR, staticOptions));

// 6b. Pre-Flight Route Shield: Cloaks /admin, /superadmin, and /dev as HTTP 404 to all unauthorized visitors
app.use(routeShield.routeShieldMiddleware);

app.use('/admin', express.static(config.ADMIN_DIR, staticOptions));
app.use('/superadmin', express.static(config.SUPERADMIN_DIR, staticOptions));
app.use('/dev', express.static(config.DEV_DIR, staticOptions));
app.use('/new/dalalmachine', express.static(config.PUBLIC_DIR, staticOptions));
app.use('/new/Machinery', express.static(config.PUBLIC_DIR, staticOptions)); // backward compatibility alias
app.use('/', express.static(config.PUBLIC_DIR, staticOptions));

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

app.get('/dev', (req, res) => {
  res.sendFile(path.join(config.DEV_DIR, 'index.html'));
});

// 8. API Routes with Rate Limiting Guards
app.use('/api/auth/login', authLimiter);
app.use('/api/auth', authRoutes);
app.use('/api/products', productRoutes);
app.use('/api/inquiries', inquiryLimiter, inquiryRoutes);
app.use('/api/users', userRoutes);
app.use('/api/logs', logRoutes);
app.get('/api/system/developer-banner', (req, res) => {
  res.json({ success: true, banner: db.getDeveloperBanner() });
});
app.use('/api/system', systemRoutes);
app.use('/api/ai', aiRoutes);
app.use('/api/dev', devRoutes);

// Health check endpoint
app.get('/api/health', (req, res) => {
  res.json({
    status: 'ok',
    timestamp: new Date().toISOString(),
    uptime: process.uptime()
  });
});

// 9. Standard 404 Fallback for any unknown path
app.use((req, res) => {
  res.status(404);
  const page404 = path.join(config.PUBLIC_DIR, '404.html');
  if (fs.existsSync(page404)) {
    return res.sendFile(page404);
  }
  return res.send('404 Not Found');
});

// Global Error Handler
app.use((err, req, res, next) => {
  console.error('Unhandled server error:', err);
  res.status(err.status || 500).json({
    success: false,
    message: err.message || 'Internal server error occurred.'
  });
});

// Start Server with Real-Time WebSockets Engine
const PORT = config.PORT;
const server = http.createServer(app);
realtime.initRealtime(server);

server.listen(PORT, () => {
  console.log(`=======================================================`);
  console.log(` Dalal Machine Tools - Fullstack Backend & Admin Portal `);
  console.log(`=======================================================`);
  console.log(` Web Server:    http://localhost:${PORT}/`);
  console.log(` Admin Portal:  http://localhost:${PORT}/admin/`);
  console.log(` WebSockets:    Socket.IO Active on ws://localhost:${PORT}/`);
  console.log(` API Endpoint:  http://localhost:${PORT}/api/health`);
  console.log(` Security:      Helmet ON, RateLimiter ON, /hub REMOVED `);
  console.log(`=======================================================`);

  // Automated Keep-Alive Heartbeat (Prevents Render Free Tier 15-min Sleep)
  const keepAliveUrl = process.env.RENDER_EXTERNAL_URL || process.env.KEEP_ALIVE_URL;
  if (keepAliveUrl) {
    console.log(`[KeepAlive] Render 24/7 Anti-Sleep engine activated for: ${keepAliveUrl}`);
    setInterval(() => {
      fetch(`${keepAliveUrl}/api/health`)
        .then(res => res.json())
        .then(data => {
          console.log(`[KeepAlive] Heartbeat ping sent at ${new Date().toLocaleTimeString()} - Health: ${data.status}`);
        })
        .catch(err => {
          console.warn(`[KeepAlive] Ping warning: ${err.message}`);
        });
    }, 10 * 60 * 1000); // Pings every 10 minutes (Render sleep timeout is 15 mins)
  }
});

module.exports = { app, server };
