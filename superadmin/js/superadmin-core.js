// Dalal Machine Tools Agency Pvt. Ltd. - Super Admin Executive Core Library

const SuperAdminCore = {
  getToken: () => localStorage.getItem('superadmin_token') || null,
  getUser: () => {
    try {
      const u = localStorage.getItem('superadmin_user');
      if (u) return JSON.parse(u);
      const token = localStorage.getItem('superadmin_token');
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
    localStorage.setItem('superadmin_token', token);
    localStorage.setItem('superadmin_user', JSON.stringify(user));
  },

  clearSession: () => {
    localStorage.removeItem('superadmin_token');
    localStorage.removeItem('superadmin_user');
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

  requireSuperAdmin: async () => {
    const token = SuperAdminCore.getToken();
    const user = SuperAdminCore.getUser();

    if (!token || !user || user.role !== 'superadmin') {
      SuperAdminCore.clearSession();
      window.location.href = '/superadmin/index.html';
      return null;
    }

    // Connect real-time WebSocket engine immediately
    SuperAdminCore.initRealtime();

    // Verify session validity with server in real-time
    try {
      const meRes = await fetch('/api/auth/me', {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      const meData = await meRes.json().catch(() => ({}));
      if (meRes.status === 403 && meData.blockedByDeveloper) {
        SuperAdminCore.triggerInstantLockout(meData);
        return null;
      }
      if (!meRes.ok && meRes.status === 401) {
        SuperAdminCore.clearSession();
        window.location.href = '/superadmin/index.html';
        return null;
      }
    } catch (err) {}

    // Populate user pill in UI
    SuperAdminCore.initUI(user);

    // Start 4-second background heartbeat as secondary defense line
    SuperAdminCore.startSecurityHeartbeat();

    return user;
  },
  // Alias for backward compatibility
  requireAuth: async () => {
    return await SuperAdminCore.requireSuperAdmin();
  },

  initUI: (user) => {
    const nameEl = document.getElementById('sa-user-name');
    const avatarEl = document.getElementById('sa-user-avatar');
    if (nameEl) nameEl.textContent = user.name || user.username;
    if (avatarEl) avatarEl.textContent = (user.name || user.username).charAt(0).toUpperCase();

    // Toggle button
    // Universal Side Menu Toggle (Desktop Collapse + Mobile Drawer)
    const toggleBtn = document.getElementById('sa-btn-toggle');
    const sidebar = document.querySelector('.sa-sidebar');

    let backdrop = document.querySelector('.sa-mobile-backdrop');
    if (!backdrop) {
      backdrop = document.createElement('div');
      backdrop.className = 'sa-mobile-backdrop';
      document.body.appendChild(backdrop);
    }

    function toggleSaMenu(e) {
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
        document.body.classList.toggle('sa-sidebar-collapsed');
        const isCollapsed = document.body.classList.contains('sa-sidebar-collapsed');
        try { localStorage.setItem('dalal_sa_sidebar_collapsed', isCollapsed ? '1' : '0'); } catch (err) {}
      }
    }

    if (toggleBtn) toggleBtn.addEventListener('click', toggleSaMenu);
    backdrop.addEventListener('click', () => {
      if (sidebar) sidebar.classList.remove('open');
      backdrop.classList.remove('active');
    });

    // Close on backdrop tap for mobile
    document.addEventListener('click', (e) => {
      if (window.innerWidth <= 992 && sidebar && sidebar.classList.contains('open')) {
        if (!sidebar.contains(e.target) && toggleBtn && !toggleBtn.contains(e.target)) {
          sidebar.classList.remove('open');
          backdrop.classList.remove('active');
        }
      }
    });

    // Auto-close drawer on navigation link tap
    if (sidebar) {
      sidebar.querySelectorAll('a').forEach(a => {
        a.addEventListener('click', () => {
          if (window.innerWidth <= 992) {
            sidebar.classList.remove('open');
            backdrop.classList.remove('active');
          }
        });
      });

      // Add close button inside mobile drawer header
      const saHeader = sidebar.querySelector('.sa-sidebar-header');
      if (saHeader && !saHeader.querySelector('.sa-drawer-close')) {
        const closeBtn = document.createElement('button');
        closeBtn.className = 'sa-drawer-close';
        closeBtn.innerHTML = '&times;';
        closeBtn.title = 'Close Navigation Menu';
        closeBtn.addEventListener('click', (e) => {
          e.stopPropagation();
          sidebar.classList.remove('open');
          backdrop.classList.remove('active');
        });
        saHeader.appendChild(closeBtn);
      }
    }

    // Close on Escape key
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && sidebar && sidebar.classList.contains('open')) {
        sidebar.classList.remove('open');
        backdrop.classList.remove('active');
      }
    });

    // ── Auto-Inject Enterprise SuperAdmin Mobile Bottom Navigation Bar ──
    if (!document.querySelector('.sa-mobile-bottom-nav')) {
      const pathname = window.location.pathname.toLowerCase();
      const isDashboard = pathname.includes('dashboard') || pathname.endsWith('/superadmin') || pathname.endsWith('/superadmin/');
      const isUsers = pathname.includes('users');
      const isLogs = pathname.includes('logs');
      const isSettings = pathname.includes('settings');

      const bottomNav = document.createElement('nav');
      bottomNav.className = 'sa-mobile-bottom-nav';
      bottomNav.setAttribute('aria-label', 'SuperAdmin Mobile Navigation');
      bottomNav.innerHTML = `
        <a href="/superadmin/dashboard.html" class="sa-bottom-nav-item ${isDashboard ? 'active' : ''}">
          <i class="fa fa-tachometer"></i>
          <span>Dashboard</span>
        </a>
        <a href="/superadmin/users.html" class="sa-bottom-nav-item ${isUsers ? 'active' : ''}">
          <i class="fa fa-users"></i>
          <span>Users</span>
        </a>
        <a href="/superadmin/logs.html" class="sa-bottom-nav-item ${isLogs ? 'active' : ''}">
          <i class="fa fa-shield"></i>
          <span>Sec Logs</span>
        </a>
        <a href="/superadmin/settings.html" class="sa-bottom-nav-item ${isSettings ? 'active' : ''}">
          <i class="fa fa-database"></i>
          <span>Sync Engine</span>
        </a>
        <a href="javascript:void(0)" id="sa-bottom-nav-menu-btn" class="sa-bottom-nav-item">
          <i class="fa fa-bars"></i>
          <span>Menu</span>
        </a>
      `;
      document.body.appendChild(bottomNav);

      document.getElementById('sa-bottom-nav-menu-btn')?.addEventListener('click', (e) => {
        toggleSaMenu(e);
      });
    }

    // Restore desktop preference
    if (window.innerWidth > 992 && localStorage.getItem('dalal_sa_sidebar_collapsed') === '1') {
      document.body.classList.add('sa-sidebar-collapsed');
    }

    // Logout buttons
    document.querySelectorAll('.sa-btn-logout').forEach(btn => {
      btn.addEventListener('click', SuperAdminCore.logout);
    });
  },

  logout: async () => {
    try {
      await fetch('/api/auth/logout', { method: 'POST' });
    } catch (e) {}
    SuperAdminCore.clearSession();
    window.location.href = '/superadmin/index.html';
  },

  api: async (url, options = {}) => {
    const token = SuperAdminCore.getToken();
    const headers = options.headers || {};
    if (token) headers['Authorization'] = `Bearer ${token}`;
    if (!(options.body instanceof FormData) && !headers['Content-Type']) {
      headers['Content-Type'] = 'application/json';
    }
    options.headers = headers;

    try {
      const res = await fetch(url, options);
      const data = await res.json().catch(() => ({}));

      if ((res.status === 401 || res.status === 403) && !url.includes('/api/auth/login')) {
        if (res.status === 403 && data.blockedByDeveloper) {
          SuperAdminCore.triggerInstantLockout(data);
          return data;
        }
        if (res.status === 401) {
          SuperAdminCore.clearSession();
          window.location.href = '/superadmin/index.html';
          return data;
        }
      }
      return data;
    } catch (err) {
      console.error('Super Admin API Error:', err);
      return { success: false, message: err.message || 'Network request failed' };
    }
  },

  toast: (msg, type = 'success') => {
    let container = document.getElementById('sa-toast-container');
    if (!container) {
      container = document.createElement('div');
      container.id = 'sa-toast-container';
      document.body.appendChild(container);
    }
    const toast = document.createElement('div');
    toast.className = 'sa-toast';
    const icon = type === 'success' ? 'fa-check-circle' : 'fa-exclamation-triangle';
    toast.innerHTML = `<i class="fa ${icon}" style="color: ${type === 'success' ? 'var(--sa-gold)' : 'var(--sa-danger)'}"></i><span>${msg}</span>`;
    container.appendChild(toast);
    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transform = 'translateY(10px)';
      setTimeout(() => toast.remove(), 250);
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
      const badge = SuperAdminCore.escapeHTML(b.badgeText || '✨ DEVELOPER DOODLE SPOTLIGHT');
      const title = SuperAdminCore.escapeHTML(b.title || 'Dalal System Broadcast');
      const desc = SuperAdminCore.escapeHTML(b.message || '');
      const linkText = SuperAdminCore.escapeHTML(b.linkText || 'Explore');
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
              <button type="button" class="doodle-close-btn" title="Dismiss banner" onclick="SuperAdminCore.dismissDeveloperBanner()">
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
    if (SuperAdminCore._realtimeInitialized) return;
    SuperAdminCore._realtimeInitialized = true;

    function connectSocket() {
      if (typeof io === 'undefined') return;
      if (SuperAdminCore.socket) return;

      const socket = io({
        reconnection: true,
        reconnectionAttempts: Infinity,
        reconnectionDelay: 1000
      });
      SuperAdminCore.socket = socket;

      socket.on('connect', () => {
        console.log('[RealTime] SuperAdmin connected to WebSocket server via id:', socket.id);
        const token = SuperAdminCore.getToken();
        if (token) {
          socket.emit('auth:register', { token });
        }
      });

      // 1. CRITICAL SECURITY EVENT: Super Admin Account Blocked by Developer
      socket.on('auth:account_blocked', (payload) => {
        console.warn('[RealTime] Received account:blocked event in SuperAdmin:', payload);
        const currentUser = SuperAdminCore.getUser();
        if (!currentUser) return;

        if (payload.userId === currentUser.id || payload.username === currentUser.username) {
          SuperAdminCore.triggerInstantLockout(payload);
        }
      });

      // 2. CRITICAL EVENT: Real-Time Google Doodle Broadcast
      socket.on('doodle:banner_broadcast', (bannerData) => {
        console.log('[RealTime] SuperAdmin received Doodle Banner broadcast:', bannerData);
        SuperAdminCore.applyLiveDoodleBanner(bannerData);
      });

      // 3. EVENT: Catalog Synchronized
      socket.on('catalog:inventory_synced', (data) => {
        SuperAdminCore.toast(`Catalog Sync: Machine ${data.product ? data.product.name : ''} (${data.action.toLowerCase()})`);
        if (typeof loadMasterData === 'function') loadMasterData();
      });

      // 4. EVENT: New Buyer Inquiry
      socket.on('inquiry:new_lead', (data) => {
        SuperAdminCore.playNotificationChime();
        SuperAdminCore.toast(`🔔 New Buyer RFQ: ${data.machineName || 'Machinery Lead'} (${data.company || 'Enterprise'})`, 'info');
        if (typeof loadMasterData === 'function') loadMasterData();
      });

      // 5. EVENT: Inquiry Status Updated Across Sessions
      socket.on('inquiry:status_changed', (data) => {
        if (typeof loadMasterData === 'function') loadMasterData();
      });

      // 6. EVENT: Administrative Accounts Changed
      socket.on('user:status_changed', (data) => {
        if (typeof loadMasterData === 'function') loadMasterData();
        if (typeof loadUsers === 'function') loadUsers();
      });
    }

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

  triggerInstantLockout: (payload) => {
    if (document.getElementById('realtime-lockout-overlay')) return;
    SuperAdminCore.clearSession();

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

    document.body.style.overflow = 'hidden';
    const mainWrapper = document.querySelector('.sa-wrapper') || document.body;
    mainWrapper.style.filter = 'blur(6px) grayscale(50%)';
    mainWrapper.style.pointerEvents = 'none';

    const overlay = document.createElement('div');
    overlay.id = 'realtime-lockout-overlay';
    overlay.style.cssText = `
      position: fixed;
      inset: 0;
      z-index: 9999999;
      background: rgba(15, 23, 42, 0.9);
      backdrop-filter: blur(14px);
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 20px;
      font-family: 'Plus Jakarta Sans', sans-serif;
    `;

    const reason = SuperAdminCore.escapeHTML(payload.reason || 'Master executive account suspended by System Developer.');
    const dateFormatted = payload.blockedAt ? new Date(payload.blockedAt).toLocaleString() : 'Just now';

    overlay.innerHTML = `
      <div style="background: #ffffff; border-radius: 28px; width: 100%; max-width: 520px; padding: 40px 36px; box-shadow: 0 30px 60px -15px rgba(220, 38, 38, 0.4), 0 0 0 2px #ef4444; text-align: center; pointer-events: auto;">
        <div style="width: 80px; height: 80px; border-radius: 50%; background: #fee2e2; color: #dc2626; display: inline-flex; align-items: center; justify-content: center; font-size: 38px; margin-bottom: 20px; box-shadow: 0 0 0 10px rgba(239, 68, 68, 0.15); animation: pulseAlert 2s infinite;">
          <i class="fa fa-ban"></i>
        </div>
        
        <h2 style="font-size: 22px; font-weight: 800; color: #991b1b; letter-spacing: -0.5px; margin-bottom: 8px; text-transform: uppercase;">
          Master Authorization Revoked
        </h2>
        
        <p style="font-size: 14px; color: #475569; line-height: 1.5; margin-bottom: 20px;">
          Your <strong>Super Admin</strong> account has been placed on administrative quarantine by the Lead System Developer. Active credentials revoked in real-time.
        </p>

        <div style="background: #fef2f2; border: 1.5px dashed #f87171; border-radius: 14px; padding: 16px; margin-bottom: 24px; text-align: left;">
          <div style="font-size: 11px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.6px; color: #b91c1c; margin-bottom: 4px;">
            <i class="fa fa-shield"></i> Developer Suspension Order:
          </div>
          <div style="font-size: 13.5px; font-weight: 600; color: #7f1d1d; line-height: 1.45;">
            ${reason}
          </div>
          <div style="font-size: 11.5px; color: #991b1b; margin-top: 8px;">
            <strong>Revocation Time:</strong> ${dateFormatted}
          </div>
        </div>

        <div style="display: flex; flex-direction: column; gap: 10px;">
          <button type="button" id="btn-sa-lockout-redirect" style="width: 100%; background: #dc2626; color: #ffffff; border: none; border-radius: 12px; padding: 14px; font-size: 14px; font-weight: 700; cursor: pointer;">
            Return to Master Login (<span id="sa-lockout-countdown">8</span>s)
          </button>
          <div style="font-size: 12px; color: #64748b;">
            Developer console intervention required to unfreeze master authority.
          </div>
        </div>
      </div>
    `;

    document.documentElement.appendChild(overlay);

    let secRemaining = 8;
    const cdEl = document.getElementById('sa-lockout-countdown');
    const timer = setInterval(() => {
      secRemaining--;
      if (cdEl) cdEl.textContent = secRemaining;
      if (secRemaining <= 0) {
        clearInterval(timer);
        window.location.href = `/superadmin/index.html?blocked=1&reason=${encodeURIComponent(payload.reason || '')}`;
      }
    }, 1000);

    const btn = document.getElementById('btn-sa-lockout-redirect');
    if (btn) {
      btn.addEventListener('click', () => {
        clearInterval(timer);
        window.location.href = `/superadmin/index.html?blocked=1&reason=${encodeURIComponent(payload.reason || '')}`;
      });
    }
  },

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
    const badge = SuperAdminCore.escapeHTML(b.badgeText || '✨ DEVELOPER DOODLE SPOTLIGHT');
    const title = SuperAdminCore.escapeHTML(b.title || 'Dalal System Broadcast');
    const desc = SuperAdminCore.escapeHTML(b.message || '');
    const linkText = SuperAdminCore.escapeHTML(b.linkText || 'Explore');
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
            <button type="button" class="doodle-close-btn" title="Dismiss banner" onclick="SuperAdminCore.dismissDeveloperBanner()">
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
      osc.frequency.setValueAtTime(587.33, ctx.currentTime);
      osc.frequency.setValueAtTime(880, ctx.currentTime + 0.12);
      gain.gain.setValueAtTime(0.2, ctx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.4);
      osc.connect(gain);
      gain.connect(ctx.destination);
      osc.start();
      osc.stop(ctx.currentTime + 0.42);
    } catch (e) {}
  },

  startSecurityHeartbeat: () => {
    if (SuperAdminCore._heartbeatTimer) return;
    SuperAdminCore._heartbeatTimer = setInterval(async () => {
      const token = SuperAdminCore.getToken();
      if (!token) {
        clearInterval(SuperAdminCore._heartbeatTimer);
        return;
      }
      try {
        const res = await fetch('/api/auth/me', {
          headers: { 'Authorization': `Bearer ${token}` }
        });
        const data = await res.json().catch(() => ({}));
        if (res.status === 403 && data.blockedByDeveloper) {
          clearInterval(SuperAdminCore._heartbeatTimer);
          SuperAdminCore.triggerInstantLockout(data);
        }
      } catch (e) {}
    }, 4000);
  },

  // ==========================================================================
  // SUPER ADMIN UI-MATCHED SKELETON COMPONENT ENGINE
  // ==========================================================================
  renderTableSkeleton: (tbodyEl, columns = 5, rows = 5) => {
    if (typeof tbodyEl === 'string') tbodyEl = document.getElementById(tbodyEl);
    if (!tbodyEl) return;
    let html = '';
    for (let r = 0; r < rows; r++) {
      html += '<tr class="sa-skeleton-row">';
      for (let c = 0; c < columns; c++) {
        if (c === 0) {
          html += '<td><div class="sa-skeleton-shimmer sa-skeleton-text" style="width: 80px;"></div></td>';
        } else if (c === 1) {
          html += '<td><div class="sa-skeleton-shimmer sa-skeleton-title" style="width: ' + (50 + (r % 3) * 15) + '%;"></div></td>';
        } else if (c === columns - 1) {
          html += '<td><div class="sa-skeleton-shimmer sa-skeleton-btn"></div></td>';
        } else if (c === columns - 2) {
          html += '<td><div class="sa-skeleton-shimmer sa-skeleton-pill"></div></td>';
        } else {
          html += '<td><div class="sa-skeleton-shimmer sa-skeleton-text" style="width: ' + (45 + (r % 2) * 25) + '%;"></div></td>';
        }
      }
      html += '</tr>';
    }
    tbodyEl.innerHTML = html;
  },

  renderKpiSkeleton: (elementIds = []) => {
    elementIds.forEach(id => {
      const el = document.getElementById(id);
      if (el) el.innerHTML = '<span class="sa-skeleton-shimmer sa-skeleton-kpi"></span>';
    });
  }
};
