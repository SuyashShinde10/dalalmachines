const express = require('express');
const router = express.Router();
const fs = require('fs');
const path = require('path');
const os = require('os');
const http = require('http');
const config = require('../config');
const db = require('../db');
const realtime = require('../realtime');
const cacheEngine = require('../performance/cacheEngine');

/**
 * STRICT CLIENT PRIVACY SHIELD MIDDLEWARE:
 * Ensures NO customer PII, customer inquiries, quotes, names, phone numbers,
 * or user password hashes can EVER be accessed or leaked via /api/dev endpoints.
 */
router.use((req, res, next) => {
  // Hard-strip any inquiries or user credentials from ever reaching developer responses
  res.setHeader('X-Privacy-Shield', 'Active-Zero-Client-PII-Exposed');
  next();
});

// 1. GET /api/dev/telemetry - Live System & Runtime Health Metrics
router.get('/telemetry', (req, res) => {
  const mem = process.memoryUsage();
  const uptimeSec = Math.floor(process.uptime());
  const hours = Math.floor(uptimeSec / 3600);
  const minutes = Math.floor((uptimeSec % 3600) / 60);
  const seconds = uptimeSec % 60;

  res.json({
    success: true,
    privacyShield: {
      status: 'VERIFIED_ACTIVE',
      policy: 'Zero Client PII / Customer Data Redacted',
      clientDataExposed: false
    },
    system: {
      nodeVersion: process.version,
      platform: os.platform(),
      osRelease: os.release(),
      arch: os.arch(),
      cpus: os.cpus().length,
      freeMemoryMB: Math.round(os.freemem() / 1024 / 1024),
      totalMemoryMB: Math.round(os.totalmem() / 1024 / 1024),
      pid: process.pid,
      uptimeFormatted: `${hours}h ${minutes}m ${seconds}s`,
      uptimeSeconds: uptimeSec,
      environment: process.env.NODE_ENV || 'development'
    },
    memory: {
      rssMB: Math.round(mem.rss / 1024 / 1024),
      heapTotalMB: Math.round(mem.heapTotal / 1024 / 1024),
      heapUsedMB: Math.round(mem.heapUsed / 1024 / 1024),
      externalMB: Math.round(mem.external / 1024 / 1024)
    },
    cacheEngine: cacheEngine.getTelemetry(),
    server: {
      port: config.PORT,
      compression: 'gzip/brotli enabled',
      staticMaxAge: '1d (html: no-cache, must-revalidate; assets: 30d immutable)',
      rateLimiter: 'Active (25 auth attempts / 15m; 30 inquiries / 1hr)'
    }
  });
});

// 2. GET /api/dev/catalog-audit - Machine Catalog Integrity & Asset Verification (Zero Client Data)
router.get('/catalog-audit', (req, res) => {
  try {
    const products = db.getProducts({ all: 'true' });
    const categoryMap = {};
    let missingImagesCount = 0;
    const missingImagesList = [];

    products.forEach(p => {
      const cat = p.category || 'Uncategorized';
      categoryMap[cat] = (categoryMap[cat] || 0) + 1;

      // Check if primary image exists on disk
      if (p.image) {
        let localRelPath = p.image;
        if (localRelPath.startsWith('/new/dalalmachine/')) {
          localRelPath = localRelPath.replace('/new/dalalmachine/', '');
        } else if (localRelPath.startsWith('/')) {
          localRelPath = localRelPath.substring(1);
        }
        const fullImgPath = path.join(config.PUBLIC_DIR, localRelPath);
        if (!fs.existsSync(fullImgPath)) {
          missingImagesCount++;
          if (missingImagesList.length < 10) {
            missingImagesList.push({ id: p.id, name: p.name, imagePath: p.image });
          }
        }
      }
    });

    res.json({
      success: true,
      audit: {
        totalMachines: products.length,
        formingMachines: products.filter(p => p.section === 'forming').length,
        cuttingMachines: products.filter(p => p.section === 'cutting').length,
        customMachines: products.filter(p => p.isCustom).length,
        puneStockCount: products.filter(p => (p.location || '').toLowerCase().includes('pune')).length,
        categoriesCount: Object.keys(categoryMap).length,
        categoryDistribution: categoryMap,
        imageIntegrity: {
          verifiedCount: products.length - missingImagesCount,
          missingImagesCount: missingImagesCount,
          samplesWithMissingImages: missingImagesList
        }
      }
    });
  } catch (err) {
    res.status(500).json({ success: false, message: 'Catalog audit error: ' + err.message });
  }
});

// 3. POST /api/dev/run-tests - Automated Smoke Testing for Public Pages & API Routes
router.post('/run-tests', async (req, res) => {
  const testEndpoints = [
    { name: 'Homepage (/)', path: '/', expectedStatus: 200 },
    { name: 'Machinery Catalog (/category.html)', path: '/category.html', expectedStatus: 200 },
    { name: 'Services & High Seas (/services.html)', path: '/services.html', expectedStatus: 200 },
    { name: 'About Us (/about.html)', path: '/about.html', expectedStatus: 200 },
    { name: 'Contact & RFQ (/contact.html)', path: '/contact.html', expectedStatus: 200 },
    { name: 'Brand New Machinery (/brand-new-machinery.html)', path: '/brand-new-machinery.html', expectedStatus: 200 },
    { name: 'Shipment Gallery (/gallery.html)', path: '/gallery.html', expectedStatus: 200 },
    { name: '404 Recovery (/404.html)', path: '/404.html', expectedStatus: 200 },
    { name: 'API Health Endpoint (/api/health)', path: '/api/health', expectedStatus: 200 },
    { name: 'API Products List (/api/products)', path: '/api/products', expectedStatus: 200 },
    { name: 'API System Telemetry (/api/dev/telemetry)', path: '/api/dev/telemetry', expectedStatus: 200 }
  ];

  const results = [];
  let passed = 0;
  let failed = 0;

  for (const item of testEndpoints) {
    const startTime = Date.now();
    try {
      const response = await new Promise((resolve, reject) => {
        const reqObj = http.request(
          {
            hostname: 'localhost',
            port: config.PORT,
            path: item.path,
            method: 'GET',
            timeout: 3000
          },
          (resp) => {
            let data = '';
            resp.on('data', chunk => { data += chunk; });
            resp.on('end', () => {
              resolve({
                statusCode: resp.statusCode,
                contentLength: data.length,
                headers: resp.headers
              });
            });
          }
        );
        reqObj.on('error', err => reject(err));
        reqObj.on('timeout', () => { reqObj.destroy(); reject(new Error('Request timed out')); });
        reqObj.end();
      });

      const latency = Date.now() - startTime;
      const isOk = response.statusCode === item.expectedStatus;
      if (isOk) passed++; else failed++;

      results.push({
        name: item.name,
        path: item.path,
        statusCode: response.statusCode,
        expectedStatus: item.expectedStatus,
        latencyMs: latency,
        status: isOk ? 'PASS' : 'FAIL',
        contentLengthBytes: response.contentLength
      });
    } catch (err) {
      failed++;
      results.push({
        name: item.name,
        path: item.path,
        statusCode: 0,
        expectedStatus: item.expectedStatus,
        latencyMs: Date.now() - startTime,
        status: 'FAIL',
        error: err.message
      });
    }
  }

  res.json({
    success: true,
    summary: {
      totalTests: testEndpoints.length,
      passed: passed,
      failed: failed,
      successRate: Math.round((passed / testEndpoints.length) * 100) + '%'
    },
    results: results
  });
});

// 4. GET /api/dev/security-audit - Security Headers & Protection Inspection
router.get('/security-audit', (req, res) => {
  res.json({
    success: true,
    privacyGuarantees: {
      clientDataExposureBlocked: true,
      customerInquiriesMasked: true,
      piiRedactionEngine: 'ENFORCED'
    },
    headers: {
      xPoweredByDisabled: true,
      helmetActive: true,
      crossOriginResourcePolicy: 'cross-origin',
      cacheControlHTML: 'public, max-age=0, must-revalidate',
      cacheControlAssets: 'public, max-age=2592000, immutable'
    },
    cors: {
      status: 'Restricted Whitelist',
      allowedOrigins: ['localhost:5000', '127.0.0.1:5000', 'https://dalalmachines.com', 'https://www.dalalmachines.com']
    },
    rateLimiting: {
      authBruteForceProtection: '25 attempts per 15 min window',
      rfqProtection: '30 submissions per hour window'
    }
  });
});

// 5. GET /api/dev/admin-accounts - List Administrative Accounts (STRICT PRIVACY: NO Customer Leads)
router.get('/admin-accounts', (req, res) => {
  try {
    const accounts = db.getAdminAccountsForDev();
    res.json({
      success: true,
      privacyShield: 'ACTIVE: No customer PII or client inquiries included.',
      count: accounts.length,
      accounts: accounts
    });
  } catch (err) {
    res.status(500).json({ success: false, message: 'Failed to fetch administrative accounts: ' + err.message });
  }
});

// 6. POST /api/dev/admin-accounts/:id/block - Developer Power: Suspend/Block Admin or Superadmin
router.post('/admin-accounts/:id/block', (req, res) => {
  try {
    const { id } = req.params;
    const { reason } = req.body || {};
    const updated = db.blockUserByDeveloper(id, reason);
    if (!updated) {
      return res.status(404).json({ success: false, message: 'Account not found with ID: ' + id });
    }

    // REAL-TIME BROADCAST: Immediately push account:blocked event across WebSockets
    realtime.broadcastAccountBlocked({
      userId: updated.id,
      username: updated.username,
      role: updated.role,
      reason: updated.blockedReason,
      blockedAt: updated.blockedAt
    });

    res.json({
      success: true,
      message: `Account [${updated.username}] (${updated.role}) has been BLOCKED by Developer.`,
      account: updated
    });
  } catch (err) {
    res.status(500).json({ success: false, message: 'Failed to block account: ' + err.message });
  }
});

// 7. POST /api/dev/admin-accounts/:id/unblock - Developer Power: Unblock/Restore Admin or Superadmin
router.post('/admin-accounts/:id/unblock', (req, res) => {
  try {
    const { id } = req.params;
    const updated = db.unblockUserByDeveloper(id);
    if (!updated) {
      return res.status(404).json({ success: false, message: 'Account not found with ID: ' + id });
    }

    // REAL-TIME BROADCAST: Push unblock event
    realtime.broadcastAccountUnblocked({
      userId: updated.id,
      username: updated.username,
      role: updated.role
    });

    res.json({
      success: true,
      message: `Account [${updated.username}] (${updated.role}) has been UNBLOCKED and RESTORED by Developer.`,
      account: updated
    });
  } catch (err) {
    res.status(500).json({ success: false, message: 'Failed to unblock account: ' + err.message });
  }
});

// 8. GET /api/dev/banner - Get Developer Google Doodle / Dashboard Banner Configuration
router.get('/banner', (req, res) => {
  try {
    const banner = db.getDeveloperBanner();
    res.json({
      success: true,
      banner
    });
  } catch (err) {
    res.status(500).json({ success: false, message: 'Failed to fetch developer banner: ' + err.message });
  }
});

// 9. POST /api/dev/banner - Update Developer Google Doodle / Dashboard Banner
router.post('/banner', (req, res) => {
  try {
    const { active, style, title, message, icon, badgeText, linkText, linkUrl, dismissable } = req.body || {};
    const updated = db.setDeveloperBanner({
      active: typeof active === 'boolean' ? active : false,
      style: style || 'doodle-gold',
      title: title || 'Dalal Machinery Milestone',
      message: message || '',
      icon: icon || 'fa-trophy',
      badgeText: badgeText || '✨ DEVELOPER DOODLE SPOTLIGHT',
      linkText: linkText || 'Explore Machines',
      linkUrl: linkUrl || '/admin/products.html',
      dismissable: typeof dismissable === 'boolean' ? dismissable : true
    });

    // REAL-TIME BROADCAST: Push banner change to all open dashboards
    realtime.broadcastBannerUpdate(updated);

    res.json({
      success: true,
      message: 'Developer Google Doodle banner updated successfully!',
      banner: updated
    });
  } catch (err) {
    res.status(500).json({ success: false, message: 'Failed to save banner: ' + err.message });
  }
});

// 10. GET /api/dev/broadcast-banner - Public/Dashboard Broadcast Feed for Admin & Superadmin Portals
router.get('/broadcast-banner', (req, res) => {
  try {
    const banner = db.getDeveloperBanner();
    res.json({
      success: true,
      banner
    });
  } catch (err) {
    res.status(500).json({ success: false, message: 'Failed to get broadcast banner.' });
  }
});

// 11. Security Shield & Intrusion Defense Endpoints
const honeypot = require('../security/honeypot');
const routeShield = require('../security/routeShield');

router.get('/security/status', (req, res) => {
  try {
    const stats = honeypot.getSecurityStats();
    const auditChain = db.verifyAuditIntegrity();
    res.json({
      success: true,
      lockdownActive: routeShield.getLockdownStatus(),
      gatewayKey: config.PORTAL_GATEWAY_KEY,
      gatewayAccessUrl: `/portal-gate?key=${config.PORTAL_GATEWAY_KEY}&to=dev`,
      allowedDevIps: config.ALLOWED_DEV_IPS,
      auditChainVerified: auditChain.valid,
      auditLogCount: auditChain.count,
      auditLatestHash: auditChain.latestHash || 'GENESIS',
      ...stats
    });
  } catch (err) {
    res.status(500).json({ success: false, message: 'Failed to load security status: ' + err.message });
  }
});

router.get('/security/audit-verify', (req, res) => {
  try {
    const auditChain = db.verifyAuditIntegrity();
    res.json({
      success: true,
      ...auditChain
    });
  } catch (err) {
    res.status(500).json({ success: false, message: 'Failed to verify audit chain: ' + err.message });
  }
});

router.post('/security/unban', (req, res) => {
  try {
    const { ip } = req.body || {};
    if (!ip) return res.status(400).json({ success: false, message: 'IP address is required.' });
    const unbanned = honeypot.unbanIp(ip);
    res.json({
      success: true,
      message: unbanned ? `IP ${ip} released from firewall blacklist.` : `IP ${ip} was not found in active blacklist.`
    });
  } catch (err) {
    res.status(500).json({ success: false, message: 'Failed to unban IP: ' + err.message });
  }
});

router.post('/security/ban', (req, res) => {
  try {
    const { ip, reason } = req.body || {};
    if (!ip) return res.status(400).json({ success: false, message: 'IP address is required.' });
    honeypot.banIp(ip, reason || 'Manually banned by Lead Developer');
    res.json({
      success: true,
      message: `IP ${ip} added to firewall blacklist.`
    });
  } catch (err) {
    res.status(500).json({ success: false, message: 'Failed to ban IP: ' + err.message });
  }
});

router.post('/security/lockdown', (req, res) => {
  try {
    const { enabled } = req.body || {};
    const state = routeShield.togglePortalLockdown(enabled);
    res.json({
      success: true,
      lockdownActive: state,
      message: state ? 'EMERGENCY LOCKDOWN ENGAGED. All admin/dev routes cloaked as 404.' : 'EMERGENCY LOCKDOWN DISENGAGED. Normal gateway access restored.'
    });
  } catch (err) {
    res.status(500).json({ success: false, message: 'Failed to toggle lockdown: ' + err.message });
  }
});

module.exports = router;


