// Dalal Machine Tools Agency Pvt. Ltd. - Super Admin Executive Core Library

const SuperAdminCore = {
  getToken: () => localStorage.getItem('superadmin_token') || null,
  getUser: () => {
    try {
      const u = localStorage.getItem('superadmin_user');
      return u ? JSON.parse(u) : null;
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

  requireSuperAdmin: async () => {
    const token = SuperAdminCore.getToken();
    const user = SuperAdminCore.getUser();

    if (!token || !user || user.role !== 'superadmin') {
      SuperAdminCore.clearSession();
      window.location.href = '/superadmin/index.html';
      return null;
    }

    document.addEventListener('DOMContentLoaded', () => {
      SuperAdminCore.initUI(user);
    });

    return user;
  },

  initUI: (user) => {
    const nameEl = document.getElementById('sa-user-name');
    const avatarEl = document.getElementById('sa-user-avatar');
    if (nameEl) nameEl.textContent = user.name || user.username;
    if (avatarEl) avatarEl.textContent = (user.name || user.username).charAt(0).toUpperCase();

    // Toggle button
    const toggleBtn = document.getElementById('sa-btn-toggle');
    const sidebar = document.querySelector('.sa-sidebar');
    if (toggleBtn && sidebar) {
      toggleBtn.addEventListener('click', () => sidebar.classList.toggle('open'));
      document.addEventListener('click', (e) => {
        if (!sidebar.contains(e.target) && !toggleBtn.contains(e.target) && sidebar.classList.contains('open')) {
          sidebar.classList.remove('open');
        }
      });
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
      if (res.status === 401 || res.status === 403) {
        SuperAdminCore.clearSession();
        window.location.href = '/superadmin/index.html';
      }
      return await res.json();
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
  }
};
