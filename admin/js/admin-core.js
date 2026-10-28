// Dalal Admin Portal - Shared Core JavaScript Library

const AdminCore = {
  getToken: () => {
    return localStorage.getItem('admin_token') || null;
  },

  getUser: () => {
    try {
      const u = localStorage.getItem('admin_user');
      if (u) return JSON.parse(u);
      const token = localStorage.getItem('admin_token');
      if (token) {
        const parts = token.split('.');
        if (parts.length === 3) {
          const payload = JSON.parse(atob(parts[1]));
          return { id: payload.id, username: payload.username, role: payload.role };
        }
      }
      return null;
    } catch (e) {
      return null;
    }
  },

  setSession: (token, user) => {
    localStorage.setItem('admin_token', token);
    localStorage.setItem('admin_user', JSON.stringify(user));
  },

  clearSession: () => {
    localStorage.removeItem('admin_token');
    localStorage.removeItem('admin_user');
  },

  escapeHTML: (str) => {
    if (str === null || str === undefined) return '';
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;');
  },

  // Auth Guard: Call at top of protected admin pages
  requireAuth: async (requiredRole = null) => {
    const token = AdminCore.getToken();
    const user = AdminCore.getUser();

    if (!token || !user) {
      AdminCore.clearSession();
      window.location.href = '/admin/index.html';
      return null;
    }

    if (requiredRole && user.role !== requiredRole && user.role !== 'superadmin') {
      alert('Access Restricted: You need ' + requiredRole + ' privileges to access this page.');
      window.location.href = '/admin/dashboard.html';
      return null;
    }

    // Connect real-time socket immediately
    AdminCore.initRealtime();

    // Verify session validity with server in real-time
    try {
      const meRes = await fetch('/api/auth/me', {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      const meData = await meRes.json().catch(() => ({}));
      if (meRes.status === 403 && meData.blockedByDeveloper) {
        AdminCore.triggerInstantLockout(meData);
        return null;
      }
      if (!meRes.ok && meRes.status === 401) {
        AdminCore.clearSession();
        window.location.href = '/admin/index.html';
        return null;
      }
    } catch (err) {}

    // Populate user pill in UI
    AdminCore.initUI(user);

    // Start 10-second background heartbeat as secondary defense line
    AdminCore.startSecurityHeartbeat();

    return user;
  },

  initUI: (user) => {
    // Populate user info
    const nameEl = document.getElementById('sidebar-user-name');
    const roleEl = document.getElementById('sidebar-user-role');
    const avatarEl = document.getElementById('sidebar-user-avatar');

    if (nameEl) nameEl.textContent = user.name || user.username;
    if (roleEl) roleEl.textContent = user.role.toUpperCase();
    if (avatarEl) avatarEl.textContent = (user.name || user.username).charAt(0).toUpperCase();

    // Universal Side Menu Toggle (Desktop Collapse + Mobile Drawer)
    const toggleBtn = document.getElementById('btn-sidebar-toggle');
    const collapseIcon = document.querySelector('.sidebar-collapse-icon');
    const sidebar = document.querySelector('.admin-sidebar');

    let backdrop = document.querySelector('.admin-mobile-backdrop');
    if (!backdrop) {
      backdrop = document.createElement('div');
      backdrop.className = 'admin-mobile-backdrop';
      document.body.appendChild(backdrop);
    }

    function toggleMenu(e) {
      if (e) e.stopPropagation();
      if (window.innerWidth <= 992) {
        if (sidebar) {
          sidebar.classList.toggle('open');
          if (sidebar.classList.contains('open')) {
            backdrop.classList.add('active');
          } else {
            backdrop.classList.remove('active');
          }
        }
      } else {
        document.body.classList.toggle('sidebar-collapsed');
        const isCollapsed = document.body.classList.contains('sidebar-collapsed');
        try { localStorage.setItem('dalal_sidebar_collapsed', isCollapsed ? '1' : '0'); } catch (err) {}
      }
    }

    if (toggleBtn) toggleBtn.addEventListener('click', toggleMenu);
    if (collapseIcon) collapseIcon.addEventListener('click', toggleMenu);
    backdrop.addEventListener('click', () => {
      if (sidebar) sidebar.classList.remove('open');
      backdrop.classList.remove('active');
    });

    // Close on tap outside
    document.addEventListener('click', (e) => {
      if (window.innerWidth <= 992 && sidebar && sidebar.classList.contains('open')) {
        if (!sidebar.contains(e.target) && toggleBtn && !toggleBtn.contains(e.target)) {
          sidebar.classList.remove('open');
          backdrop.classList.remove('active');
        }
      }
    });

    // Close drawer when a navigation link is clicked
    if (sidebar) {
      sidebar.querySelectorAll('a').forEach(a => {
        a.addEventListener('click', () => {
          if (window.innerWidth <= 992) {
            sidebar.classList.remove('open');
            backdrop.classList.remove('active');
          }
        });
      });
    }

    // Restore desktop collapsed preference
    if (window.innerWidth > 992 && localStorage.getItem('dalal_sidebar_collapsed') === '1') {
      document.body.classList.add('sidebar-collapsed');
    }

    // Logout buttons
    document.querySelectorAll('.btn-logout').forEach(btn => {
      btn.addEventListener('click', AdminCore.logout);
    });
  },

  logout: async () => {
    try {
      await fetch('/api/auth/logout', { method: 'POST' });
    } catch (e) {}
    AdminCore.clearSession();
    window.location.href = '/admin/index.html';
  },

  // Authenticated API Fetch
  api: async (url, options = {}) => {
    const token = AdminCore.getToken();
    const headers = options.headers || {};

    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    if (!(options.body instanceof FormData) && !headers['Content-Type']) {
      headers['Content-Type'] = 'application/json';
    }

    options.headers = headers;

    try {
      const res = await fetch(url, options);
      const data = await res.json().catch(() => ({}));

      if ((res.status === 401 || res.status === 403) && !url.includes('/api/auth/login')) {
        if (res.status === 403 && data.blockedByDeveloper) {
          AdminCore.triggerInstantLockout(data);
          return data;
        }
        if (res.status === 401) {
          AdminCore.clearSession();
          window.location.href = '/admin/index.html';
          return data;
        }
      }
      return data;
    } catch (err) {
      console.error('API Fetch error:', err);
      return { success: false, message: err.message || 'Network error occurred.' };
    }
  },

  // Toast Notification
  toast: (message, type = 'success') => {
    let container = document.getElementById('toast-container');
    if (!container) {
      container = document.createElement('div');
      container.id = 'toast-container';
      document.body.appendChild(container);
    }

    const toast = document.createElement('div');
    toast.className = `toast-msg ${type}`;
    const icon = type === 'success' ? 'fa-check-circle' : type === 'error' ? 'fa-exclamation-circle' : 'fa-info-circle';
    toast.innerHTML = `<i class="fa ${icon}"></i> <span>${message}</span>`;
    container.appendChild(toast);

    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transform = 'translateY(10px)';
      setTimeout(() => toast.remove(), 300);
    }, 3500);
  },

  // Google Doodle & Developer Broadcast Banner Loader
  loadDeveloperBanner: async (slotId = 'developer-doodle-banner-slot') => {
    try {
      const slot = document.getElementById(slotId);
      if (!slot) return;
      if (sessionStorage.getItem('dalal_dismissed_doodle_banner') === '1') return;

      const res = await fetch('/api/dev/broadcast-banner');
      const data = await res.json();
      if (!data.success || !data.banner || !data.banner.active) {
        slot.innerHTML = '';
        return;
      }

      const b = data.banner;
      const styleClass = b.style || 'doodle-gold';
      const iconClass = b.icon || 'fa-trophy';
      const badge = AdminCore.escapeHTML(b.badgeText || '✨ DEVELOPER DOODLE SPOTLIGHT');
      const title = AdminCore.escapeHTML(b.title || 'Dalal System Broadcast');
      const desc = AdminCore.escapeHTML(b.message || '');
      const linkText = AdminCore.escapeHTML(b.linkText || 'Explore');
      const linkUrl = b.linkUrl ? encodeURI(b.linkUrl) : '';
      const dismissable = b.dismissable !== false;

      slot.innerHTML = `
        <div class="dev-doodle-banner ${styleClass}" id="active-doodle-banner">
          <div class="doodle-left">
            <div class="doodle-icon-circle">
              <i class="fa ${iconClass}"></i>
            </div>
            <div>
              <div class="doodle-badge">
                <i class="fa fa-sparkles"></i>
                <span>${badge}</span>
              </div>
              <div class="doodle-title">${title}</div>
              ${desc ? `<div class="doodle-desc">${desc}</div>` : ''}
            </div>
          </div>
          <div class="doodle-right">
            ${linkUrl && linkText ? `
              <a href="${linkUrl}" class="doodle-btn">
                <span>${linkText}</span>
                <i class="fa fa-arrow-right"></i>
              </a>
            ` : ''}
            ${dismissable ? `
              <button type="button" class="doodle-close-btn" title="Dismiss banner" onclick="AdminCore.dismissDeveloperBanner()">
                <i class="fa fa-times"></i>
              </button>
            ` : ''}
          </div>
        </div>
      `;
    } catch (e) {
      console.debug('No active developer doodle banner:', e.message);
    }
  },

  dismissDeveloperBanner: () => {
    const el = document.getElementById('active-doodle-banner');
    if (el) {
      el.style.opacity = '0';
      el.style.transform = 'translateY(-10px)';
      el.style.transition = 'all 0.25s ease';
      setTimeout(() => el.remove(), 250);
    }
    try { sessionStorage.setItem('dalal_dismissed_doodle_banner', '1'); } catch (err) {}
  },

  // ==========================================================================
  // REAL-TIME WEBSOCKET SYNCHRONIZATION ENGINE (Socket.IO)
  // ==========================================================================
  initRealtime: () => {
    if (AdminCore._realtimeInitialized) return;
    AdminCore._realtimeInitialized = true;

    function connectSocket() {
      if (typeof io === 'undefined') return;
      if (AdminCore.socket) return;

      const socket = io({
        reconnection: true,
        reconnectionAttempts: Infinity,
        reconnectionDelay: 1000
      });
      AdminCore.socket = socket;

      socket.on('connect', () => {
        console.log('[RealTime] Connected to Dalal WebSocket server via id:', socket.id);
        const token = AdminCore.getToken();
        if (token) {
          socket.emit('auth:register', { token });
        }
      });

      // 1. CRITICAL SECURITY EVENT: Account Blocked by Developer
      socket.on('auth:account_blocked', (payload) => {
        console.warn('[RealTime] Received account:blocked event:', payload);
        const currentUser = AdminCore.getUser();
        if (!currentUser) return;

        // If target matches this session's userId or username
        if (payload.userId === currentUser.id || payload.username === currentUser.username) {
          AdminCore.triggerInstantLockout(payload);
        }
      });

      // 2. CRITICAL EVENT: Real-Time Google Doodle Broadcast
      socket.on('doodle:banner_broadcast', (bannerData) => {
        console.log('[RealTime] Received Doodle Banner broadcast:', bannerData);
        AdminCore.applyLiveDoodleBanner(bannerData);
      });

      // 3. EVENT: Catalog Synchronized
      socket.on('catalog:inventory_synced', (data) => {
        console.log('[RealTime] Catalog synced:', data);
        AdminCore.toast(`Catalog Update: Machine ${data.product ? data.product.name : ''} (${data.action.toLowerCase()})`);
        if (typeof loadDashboardData === 'function') loadDashboardData();
        if (typeof loadProducts === 'function') loadProducts();
      });

      // 4. EVENT: New Buyer Inquiry (RFQ) - Live Alert
      socket.on('inquiry:new_lead', (data) => {
        console.log('[RealTime] New Buyer Inquiry received:', data);
        AdminCore.playNotificationChime();
        AdminCore.toast(`🔔 New Buyer RFQ: ${data.machineName || 'Machinery Lead'} (${data.company || 'Enterprise'})`, 'info');
        const badge = document.getElementById('badge-inquiries-count');
        if (badge) {
          const count = parseInt(badge.textContent, 10) || 0;
          badge.textContent = count + 1;
        }
        if (typeof loadInquiries === 'function') loadInquiries();
      });
    }

    // Dynamic loader for Socket.IO client script
    if (typeof io === 'undefined') {
      const script = document.createElement('script');
      script.src = '/socket.io/socket.io.js';
      script.onload = connectSocket;
      script.onerror = () => {
        const cdn = document.createElement('script');
        cdn.src = 'https://cdn.socket.io/4.8.1/socket.io.min.js';
        cdn.onload = connectSocket;
        document.head.appendChild(cdn);
      };
      document.head.appendChild(script);
    } else {
      connectSocket();
    }
  },

  // High-Priority Instant Security Lockout Screen
  triggerInstantLockout: (payload) => {
    if (document.getElementById('realtime-lockout-overlay')) return;
    // 1. Immediately wipe session tokens
    AdminCore.clearSession();

    // 2. Play warning audio siren
    try {
      const ctx = new (window.AudioContext || window.webkitAudioContext)();
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();
      osc.type = 'sawtooth';
      osc.frequency.setValueAtTime(440, ctx.currentTime);
      osc.frequency.exponentialRampToValueAtTime(220, ctx.currentTime + 0.4);
      gain.gain.setValueAtTime(0.3, ctx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.4);
      osc.connect(gain);
      gain.connect(ctx.destination);
      osc.start();
      osc.stop(ctx.currentTime + 0.45);
    } catch (e) {}

    // 3. Freeze page scroll & blur background
    document.body.style.overflow = 'hidden';
    const mainWrapper = document.querySelector('.admin-wrapper') || document.body;
    mainWrapper.style.filter = 'blur(6px) grayscale(50%)';
    mainWrapper.style.pointerEvents = 'none';

    // 4. Inject Full-Screen High-Security Lockout Overlay
    const overlay = document.createElement('div');
    overlay.id = 'realtime-lockout-overlay';
    overlay.style.cssText = `
      position: fixed;
      inset: 0;
      z-index: 9999999;
      background: rgba(15, 23, 42, 0.88);
      backdrop-filter: blur(12px);
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 20px;
      font-family: 'Plus Jakarta Sans', sans-serif;
      animation: modalFadeIn 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    `;

    const reason = AdminCore.escapeHTML(payload.reason || 'Account suspended by Lead System Developer for operational review.');
    const dateFormatted = payload.blockedAt ? new Date(payload.blockedAt).toLocaleString() : 'Just now';

    overlay.innerHTML = `
      <div style="background: #ffffff; border-radius: 28px; width: 100%; max-width: 520px; padding: 40px 36px; box-shadow: 0 30px 60px -15px rgba(220, 38, 38, 0.35), 0 0 0 2px #ef4444; text-align: center; pointer-events: auto;">
        <div style="width: 80px; height: 80px; border-radius: 50%; background: #fee2e2; color: #dc2626; display: inline-flex; align-items: center; justify-content: center; font-size: 38px; margin-bottom: 20px; box-shadow: 0 0 0 10px rgba(239, 68, 68, 0.15); animation: pulseAlert 2s infinite;">
          <i class="fa fa-ban"></i>
        </div>
        
        <h2 style="font-size: 22px; font-weight: 800; color: #991b1b; letter-spacing: -0.5px; margin-bottom: 8px; text-transform: uppercase;">
          Access Revoked in Real-Time
        </h2>
        
        <p style="font-size: 14px; color: #475569; line-height: 1.5; margin-bottom: 20px;">
          Your <strong>${AdminCore.escapeHTML(payload.role || 'Staff')}</strong> account has been suspended by the Lead System Developer. Active credentials have been terminated immediately.
        </p>

        <div style="background: #fef2f2; border: 1.5px dashed #f87171; border-radius: 14px; padding: 16px; margin-bottom: 24px; text-align: left;">
          <div style="font-size: 11px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.6px; color: #b91c1c; margin-bottom: 4px;">
            <i class="fa fa-shield"></i> Developer Suspension Note:
          </div>
          <div style="font-size: 13.5px; font-weight: 600; color: #7f1d1d; line-height: 1.45;">
            ${reason}
          </div>
          <div style="font-size: 11.5px; color: #991b1b; margin-top: 8px;">
            <strong>Revocation Time:</strong> ${dateFormatted}
          </div>
        </div>

        <div style="display: flex; flex-direction: column; gap: 10px;">
          <button type="button" id="btn-lockout-redirect" style="width: 100%; background: #dc2626; color: #ffffff; border: none; border-radius: 12px; padding: 14px; font-size: 14px; font-weight: 700; cursor: pointer; transition: all 0.2s;">
            Return to Login Portal (<span id="lockout-countdown">8</span>s)
          </button>
          <div style="font-size: 12px; color: #64748b;">
            Contact Lead System Developer (SecOps) via Developer Console for account clearance.
          </div>
        </div>
      </div>
      <style>
        @keyframes pulseAlert {
          0%, 100% { transform: scale(1); box-shadow: 0 0 0 10px rgba(239, 68, 68, 0.15); }
          50% { transform: scale(1.05); box-shadow: 0 0 0 18px rgba(239, 68, 68, 0.25); }
        }
        @keyframes modalFadeIn {
          from { opacity: 0; transform: scale(0.95); }
          to { opacity: 1; transform: scale(1); }
        }
      </style>
    `;

    document.documentElement.appendChild(overlay);

    let secRemaining = 8;
    const cdEl = document.getElementById('lockout-countdown');
    const timer = setInterval(() => {
      secRemaining--;
      if (cdEl) cdEl.textContent = secRemaining;
      if (secRemaining <= 0) {
        clearInterval(timer);
        window.location.href = `/admin/index.html?blocked=1&reason=${encodeURIComponent(payload.reason || '')}`;
      }
    }, 1000);

    const btn = document.getElementById('btn-lockout-redirect');
    if (btn) {
      btn.addEventListener('click', () => {
        clearInterval(timer);
        window.location.href = `/admin/index.html?blocked=1&reason=${encodeURIComponent(payload.reason || '')}`;
      });
    }
  },

  // Live Apply or Remove Google Doodle Banner without reloading page
  applyLiveDoodleBanner: (b) => {
    const slot = document.getElementById('developer-doodle-banner-slot');
    if (!slot) return;

    if (!b || !b.active) {
      const existing = document.getElementById('active-doodle-banner');
      if (existing) {
        existing.style.opacity = '0';
        existing.style.transform = 'translateY(-12px)';
        setTimeout(() => { existing.remove(); slot.innerHTML = ''; }, 300);
      }
      return;
    }

    const styleClass = b.style || 'doodle-gold';
    const iconClass = b.icon || 'fa-trophy';
    const badge = AdminCore.escapeHTML(b.badgeText || '✨ DEVELOPER DOODLE SPOTLIGHT');
    const title = AdminCore.escapeHTML(b.title || 'Dalal System Broadcast');
    const desc = AdminCore.escapeHTML(b.message || '');
    const linkText = AdminCore.escapeHTML(b.linkText || 'Explore');
    const linkUrl = b.linkUrl ? encodeURI(b.linkUrl) : '';
    const dismissable = b.dismissable !== false;

    slot.innerHTML = `
      <div class="dev-doodle-banner ${styleClass}" id="active-doodle-banner" style="animation: doodleSlideIn 0.35s cubic-bezier(0.16, 1, 0.3, 1);">
        <div class="doodle-left">
          <div class="doodle-icon-circle">
            <i class="fa ${iconClass}"></i>
          </div>
          <div>
            <div class="doodle-badge">
              <i class="fa fa-sparkles"></i>
              <span>${badge}</span>
            </div>
            <div class="doodle-title">${title}</div>
            ${desc ? `<div class="doodle-desc">${desc}</div>` : ''}
          </div>
        </div>
        <div class="doodle-right">
          ${linkUrl && linkText ? `
            <a href="${linkUrl}" class="doodle-btn">
              <span>${linkText}</span>
              <i class="fa fa-arrow-right"></i>
            </a>
          ` : ''}
          ${dismissable ? `
            <button type="button" class="doodle-close-btn" title="Dismiss banner" onclick="AdminCore.dismissDeveloperBanner()">
              <i class="fa fa-times"></i>
            </button>
          ` : ''}
        </div>
      </div>
    `;
  },

  playNotificationChime: () => {
    try {
      const ctx = new (window.AudioContext || window.webkitAudioContext)();
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();
      osc.type = 'sine';
      osc.frequency.setValueAtTime(587.33, ctx.currentTime); // D5
      osc.frequency.setValueAtTime(880, ctx.currentTime + 0.12); // A5
      gain.gain.setValueAtTime(0.2, ctx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.4);
      osc.connect(gain);
      gain.connect(ctx.destination);
      osc.start();
      osc.stop(ctx.currentTime + 0.42);
    } catch (e) {}
  },

  startSecurityHeartbeat: () => {
    if (AdminCore._heartbeatTimer) return;
    AdminCore._heartbeatTimer = setInterval(async () => {
      const token = AdminCore.getToken();
      if (!token) {
        clearInterval(AdminCore._heartbeatTimer);
        return;
      }
      try {
        const res = await fetch('/api/auth/me', {
          headers: { 'Authorization': `Bearer ${token}` }
        });
        const data = await res.json().catch(() => ({}));
        if (res.status === 403 && data.blockedByDeveloper) {
          clearInterval(AdminCore._heartbeatTimer);
          AdminCore.triggerInstantLockout(data);
        }
      } catch (e) {}
    }, 4000);
  }
};
