// Dalal Admin Portal - Shared Core JavaScript Library

const AdminCore = {
  getToken: () => {
    return localStorage.getItem('admin_token') || null;
  },

  getUser: () => {
    try {
      const u = localStorage.getItem('admin_user');
      return u ? JSON.parse(u) : null;
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

    // Populate user pill in UI
    document.addEventListener('DOMContentLoaded', () => {
      AdminCore.initUI(user);
    });

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

    function toggleMenu(e) {
      if (e) e.stopPropagation();
      if (window.innerWidth <= 992) {
        if (sidebar) sidebar.classList.toggle('open');
      } else {
        document.body.classList.toggle('sidebar-collapsed');
        const isCollapsed = document.body.classList.contains('sidebar-collapsed');
        try { localStorage.setItem('dalal_sidebar_collapsed', isCollapsed ? '1' : '0'); } catch (err) {}
      }
    }

    if (toggleBtn) toggleBtn.addEventListener('click', toggleMenu);
    if (collapseIcon) collapseIcon.addEventListener('click', toggleMenu);

    // Close on mobile backdrop tap
    document.addEventListener('click', (e) => {
      if (window.innerWidth <= 992 && sidebar && sidebar.classList.contains('open')) {
        if (!sidebar.contains(e.target) && toggleBtn && !toggleBtn.contains(e.target)) {
          sidebar.classList.remove('open');
        }
      }
    });

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
      if (res.status === 401 || res.status === 403) {
        if (res.status === 401) {
          AdminCore.clearSession();
          window.location.href = '/admin/index.html';
        }
      }
      const data = await res.json();
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
  }
};
