const { Server } = require('socket.io');
const jwt = require('jsonwebtoken');
const config = require('./config');

let io = null;

function initRealtime(server) {
  io = new Server(server, {
    cors: {
      origin: '*',
      methods: ['GET', 'POST']
    },
    serveClient: true, // serves /socket.io/socket.io.js
    pingInterval: 10000,
    pingTimeout: 5000
  });

  io.on('connection', (socket) => {
    // Default room for all public pages
    socket.join('public');

    // Handle authentication / role registration
    socket.on('auth:register', (data) => {
      try {
        if (!data) return;

        // Developer mode registration
        if (data.mode === 'developer') {
          socket.join('developer');
          socket.emit('registered', { room: 'developer', status: 'connected' });
          return;
        }

        // Token verification for Admin & Super Admin
        if (data.token) {
          const decoded = jwt.verify(data.token, config.JWT_SECRET);
          socket.userId = decoded.id;
          socket.userRole = decoded.role;
          socket.username = decoded.username;

          // Check if user is ALREADY blocked in database!
          const db = require('./db');
          const user = db.getUserById(decoded.id);
          if (user && user.blockedByDeveloper) {
            console.warn(`[WebSocket] Blocked user ${user.username} connected. Immediately emitting auth:account_blocked!`);
            socket.emit('auth:account_blocked', {
              userId: user.id,
              username: user.username,
              role: user.role,
              reason: user.blockedReason || 'Suspended by Lead System Developer.',
              blockedAt: user.blockedAt || new Date().toISOString()
            });
            return;
          }

          // Join dedicated user channel and role room
          socket.join(`user:${decoded.id}`);
          socket.join(`user:${decoded.username}`);
          socket.join(decoded.role); // 'admin' or 'superadmin'

          socket.emit('registered', { 
            room: decoded.role, 
            userId: decoded.id, 
            username: decoded.username,
            status: 'connected' 
          });
        }
      } catch (err) {
        // Token invalid or expired
        socket.emit('registered', { status: 'unauthenticated' });
      }
    });

    socket.on('disconnect', () => {
      // Clean disconnect
    });
  });

  // Stream lightweight live telemetry to developer console every 3 seconds
  setInterval(() => {
    if (!io) return;
    const mem = process.memoryUsage();
    io.to('developer').emit('telemetry:tick', {
      uptimeSeconds: Math.floor(process.uptime()),
      memory: {
        rssMB: (mem.rss / (1024 * 1024)).toFixed(1),
        heapUsedMB: (mem.heapUsed / (1024 * 1024)).toFixed(1),
        heapTotalMB: (mem.heapTotal / (1024 * 1024)).toFixed(1)
      },
      activeSockets: io.engine ? io.engine.clientsCount : 0,
      timestamp: new Date().toISOString()
    });
  }, 3000);

  console.log('[WebSocket] Real-Time Engine initialized with Socket.IO on port ' + config.PORT);
  return io;
}

function getIO() {
  return io;
}

// 1. Account Blocked Event - Instant Revocation & Alert
function broadcastAccountBlocked({ userId, username, role, reason, blockedAt }) {
  if (!io) return;
  const payload = {
    userId,
    username,
    role,
    reason: reason || 'Suspended by Lead System Developer for operational and security review.',
    blockedAt: blockedAt || new Date().toISOString()
  };

  console.log(`[WebSocket] 🚨 BROADCASTING ACCOUNT BLOCKED: ${username} (${userId})`);
  // Broadcast to all sockets and target rooms for 100% delivery guarantee
  io.emit('auth:account_blocked', payload);
  io.to(`user:${userId}`).emit('auth:account_blocked', payload);
  io.to(`user:${username}`).emit('auth:account_blocked', payload);
  io.to('developer').emit('dev:account_status_changed', { ...payload, status: 'BLOCKED' });
}

// 2. Account Unblocked Event - Instant Restoration
function broadcastAccountUnblocked({ userId, username, role }) {
  if (!io) return;
  const payload = {
    userId,
    username,
    role,
    unblockedAt: new Date().toISOString()
  };

  console.log(`[WebSocket] ✅ BROADCASTING ACCOUNT UNBLOCKED: ${username} (${userId})`);
  io.emit('auth:account_unblocked', payload);
  io.to(`user:${userId}`).emit('auth:account_unblocked', payload);
  io.to('developer').emit('dev:account_status_changed', { ...payload, status: 'UNBLOCKED' });
}

// 3. Google Doodle / Announcement Banner Broadcast - Instant Update
function broadcastBannerUpdate(bannerConfig) {
  if (!io) return;
  io.emit('doodle:banner_broadcast', bannerConfig);
  io.to('developer').emit('dev:banner_status_ack', { 
    active: bannerConfig.active, 
    style: bannerConfig.style,
    timestamp: new Date().toISOString() 
  });
}

// 4. Catalog / Inventory Synchronized
function broadcastCatalogUpdate({ action, product, totalMachines }) {
  if (!io) return;
  const payload = {
    action: action || 'UPDATED',
    product: product ? { id: product.id, name: product.name, section: product.section, status: product.status } : null,
    totalMachines: totalMachines || null,
    timestamp: new Date().toISOString()
  };

  io.emit('catalog:inventory_synced', payload);
}

// 5. New Buyer Inquiry / RFQ (STRICT PRIVACY: ONLY Admin & Superadmin, NEVER Developer!)
function broadcastInquiry({ id, machineName, company, timestamp }) {
  if (!io) return;
  // Send ONLY to staff admin and superadmin rooms
  const staffPayload = {
    id,
    machineName: machineName || 'Heavy Machinery RFQ',
    company: company || 'Enterprise Buyer',
    timestamp: timestamp || new Date().toISOString()
  };
  io.to('admin').emit('inquiry:new_lead', staffPayload);
  io.to('superadmin').emit('inquiry:new_lead', staffPayload);
  // NOTE: Developer channel is intentionally EXCLUDED to maintain Zero-PII privacy!
}

// 6. Inquiry Status Updated (Admin / Super Admin room sync)
function broadcastInquiryStatusChanged({ id, status, updatedBy }) {
  if (!io) return;
  const payload = { id, status, updatedBy, timestamp: new Date().toISOString() };
  io.to('admin').emit('inquiry:status_changed', payload);
  io.to('superadmin').emit('inquiry:status_changed', payload);
}

// 7. Security & Activity Audit Log Stream
function broadcastLogEntry(entry) {
  if (!io) return;
  // Stream to Super Admin live forensic console
  io.to('superadmin').emit('audit:log_entry', entry);

  // Send sanitized (non-PII) version to developer console
  if (entry.action && (entry.action.startsWith('USER_') || entry.action.startsWith('SYS_') || entry.action.startsWith('BANNER_') || entry.action.startsWith('CATALOG_'))) {
    io.to('developer').emit('dev:audit_event', {
      timestamp: entry.timestamp,
      action: entry.action,
      username: entry.username,
      target: entry.target
    });
  }
}

// 8. Administrative User Account Changed (Created / Updated / Deleted)
function broadcastUserChange({ action, user }) {
  if (!io) return;
  const payload = {
    action,
    user: user ? { id: user.id, username: user.username, role: user.role, name: user.name, active: user.active } : null,
    timestamp: new Date().toISOString()
  };
  io.to('superadmin').emit('user:status_changed', payload);
  io.to('developer').emit('dev:account_status_changed', payload);
}

module.exports = {
  initRealtime,
  getIO,
  broadcastAccountBlocked,
  broadcastAccountUnblocked,
  broadcastBannerUpdate,
  broadcastCatalogUpdate,
  broadcastInquiry,
  broadcastInquiryStatusChanged,
  broadcastLogEntry,
  broadcastUserChange
};

