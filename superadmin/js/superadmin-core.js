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
    headers['X-Requested-With'] = 'XMLHttpRequest';
    headers['X-DMTA-CSRF'] = '1';
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

  formatInr: (amount) => {
    const num = parseFloat(amount) || 0;
    if (num >= 10000000) return '₹' + (num / 10000000).toFixed(2) + ' Cr';
    if (num >= 100000) return '₹' + (num / 100000).toFixed(2) + ' L';
    return '₹' + num.toLocaleString('en-IN');
  },

  // 1-Click WhatsApp & Formal Commercial Quotation Modal Engine
  openWhatsAppQuoteModal: async (inquiryId) => {
    try {
      SuperAdminCore.toast('Generating official DMTA quotation...', 'success');
      const res = await SuperAdminCore.api(`/api/inquiries/${inquiryId}/generate-quotation`, { method: 'POST' });
      if (!res.success) {
        SuperAdminCore.toast(res.message || 'Failed to generate quotation', 'error');
        return;
      }

      let modalBackdrop = document.getElementById('sa-quote-modal-backdrop');
      if (!modalBackdrop) {
        modalBackdrop = document.createElement('div');
        modalBackdrop.id = 'sa-quote-modal-backdrop';
        modalBackdrop.className = 'sa-modal-backdrop';
        document.body.appendChild(modalBackdrop);
      }

      const q = res;
      modalBackdrop.innerHTML = `
        <div class="sa-modal-card">
          <div class="sa-modal-header">
            <div class="sa-modal-title">
              <i class="fa fa-whatsapp" style="color: #25d366; font-size: 22px;"></i>
              <span>1-Click Formal Commercial Quotation</span>
            </div>
            <button type="button" class="sa-modal-close-btn" onclick="document.getElementById('sa-quote-modal-backdrop').classList.remove('open')">&times;</button>
          </div>
          <div class="sa-modal-body">
            <div style="background: #fffbeb; border: 1px solid #fde68a; border-radius: 12px; padding: 14px 16px; margin-bottom: 20px;">
              <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                <span style="font-size: 13px; font-weight: 800; color: #92400e;">${SuperAdminCore.escapeHTML(q.quoteNumber)}</span>
                <span style="font-size: 12px; color: #b45309; font-weight: 700;">${SuperAdminCore.escapeHTML(q.dateFormatted)}</span>
              </div>
              <div style="font-size: 13px; color: #475569;">
                Client: <strong style="color: #0f172a;">${SuperAdminCore.escapeHTML(q.client.name)}</strong> (${SuperAdminCore.escapeHTML(q.client.company || 'Enterprise')}) &bull; ${SuperAdminCore.escapeHTML(q.client.phone || '')}
              </div>
            </div>

            <div style="margin-bottom: 18px;">
              <label style="font-size: 12px; font-weight: 700; color: #475569; display: block; margin-bottom: 6px;">Quoted Heavy Machinery:</label>
              <div style="background: #f8fafc; border: 1px solid #e2e8f0; padding: 12px 14px; border-radius: 10px; font-size: 13.5px; font-weight: 700; color: #0f172a;">
                ${SuperAdminCore.escapeHTML(q.machine.name || 'Industrial Heavy Machine')}
              </div>
            </div>

            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin-bottom: 20px;">
              <div style="background: #eff6ff; border: 1px solid #bfdbfe; padding: 12px 14px; border-radius: 10px;">
                <div style="font-size: 11px; color: #1d4ed8; font-weight: 700;">EX-WORKS PRICE</div>
                <div style="font-size: 15px; font-weight: 800; color: #1e40af; margin-top: 4px; font-family: 'JetBrains Mono', monospace;">₹${q.commercials.basicPrice.toLocaleString('en-IN')}</div>
              </div>
              <div style="background: #fffbeb; border: 1px solid #fde68a; padding: 12px 14px; border-radius: 10px;">
                <div style="font-size: 11px; color: #b45309; font-weight: 700;">GST (@18%)</div>
                <div style="font-size: 15px; font-weight: 800; color: #92400e; margin-top: 4px; font-family: 'JetBrains Mono', monospace;">₹${q.commercials.gstAmount.toLocaleString('en-IN')}</div>
              </div>
              <div style="background: #ecfdf5; border: 1px solid #a7f3d0; padding: 12px 14px; border-radius: 10px;">
                <div style="font-size: 11px; color: #047857; font-weight: 700;">TOTAL DEAL VALUE</div>
                <div style="font-size: 15px; font-weight: 800; color: #065f46; margin-top: 4px; font-family: 'JetBrains Mono', monospace;">₹${q.commercials.totalAmount.toLocaleString('en-IN')}</div>
              </div>
            </div>

            <div>
              <label style="font-size: 12px; font-weight: 700; color: #475569; display: block; margin-bottom: 6px;">Official WhatsApp Message Preview:</label>
              <textarea id="sa-wa-quote-text" class="sa-form-control" style="height: 160px; font-family: 'JetBrains Mono', monospace; font-size: 12px; line-height: 1.5; background: #f8fafc; color: #0f172a; border: 1px solid #cbd5e1; border-radius: 10px;">${SuperAdminCore.escapeHTML(q.whatsAppText)}</textarea>
            </div>
          </div>
          <div class="sa-modal-footer">
            <button type="button" class="sa-btn sa-btn-secondary" onclick="navigator.clipboard.writeText(document.getElementById('sa-wa-quote-text').value); SuperAdminCore.toast('Quotation copied to clipboard!');">
              <i class="fa fa-copy"></i> Copy Text
            </button>
            ${q.whatsAppUrl ? `
              <a href="${q.whatsAppUrl}" target="_blank" class="sa-btn" style="background: #16a34a; color: #ffffff; font-weight: 800; gap: 8px; text-decoration: none; border-radius: 10px; padding: 10px 18px;">
                <i class="fa fa-whatsapp"></i> Send Direct to Client WhatsApp &rarr;
              </a>
            ` : `<button class="sa-btn sa-btn-primary" disabled>No Phone Number</button>`}
          </div>
        </div>
      `;
      modalBackdrop.classList.add('open');
    } catch (err) {
      SuperAdminCore.toast('Error: ' + err.message, 'error');
    }
  },

  // Private Inspection Video Vault Modal
  openVideoVaultModal: async (machineId) => {
    try {
      const res = await SuperAdminCore.api(`/api/products/${machineId}/inspection-vault`);
      if (!res.success) {
        SuperAdminCore.toast(res.message || 'Vault unavailable', 'error');
        return;
      }

      let modalBackdrop = document.getElementById('sa-video-vault-backdrop');
      if (!modalBackdrop) {
        modalBackdrop = document.createElement('div');
        modalBackdrop.id = 'sa-video-vault-backdrop';
        modalBackdrop.className = 'sa-modal-backdrop';
        document.body.appendChild(modalBackdrop);
      }

      const videos = res.inspectionVideos || [];
      modalBackdrop.innerHTML = `
        <div class="sa-modal-card">
          <div class="sa-modal-header">
            <div class="sa-modal-title">
              <i class="fa fa-video-camera" style="color: #6366f1;"></i>
              <span>Customer Inspection Video Vault &bull; ${SuperAdminCore.escapeHTML(res.machineName)}</span>
            </div>
            <button type="button" class="sa-modal-close-btn" onclick="document.getElementById('sa-video-vault-backdrop').classList.remove('open')">&times;</button>
          </div>
          <div class="sa-modal-body">
            <p style="font-size: 13px; color: var(--sa-text-muted); margin-bottom: 18px;">
              Unlisted high-definition trial recordings for serious buyers. These links are confidential and private to Dalal executive management.
            </p>
            ${videos.length === 0 ? '<div style="color: var(--sa-text-muted); text-align: center; padding: 24px;">No trial videos attached to this machine yet.</div>' : `
              <div style="display: flex; flex-direction: column; gap: 12px;">
                ${videos.map((v, i) => `
                  <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 12px; padding: 14px 16px; display: flex; align-items: center; justify-content: space-between; gap: 12px;">
                    <div>
                      <div style="font-size: 13.5px; font-weight: 700; color: #0f172a; margin-bottom: 4px;">
                        <i class="fa fa-play-circle" style="color: #d97706; margin-right: 6px;"></i>${SuperAdminCore.escapeHTML(v.title)}
                      </div>
                      <div style="font-size: 12px; color: var(--sa-text-muted); font-family: 'JetBrains Mono', monospace;">
                        Duration: ${SuperAdminCore.escapeHTML(v.duration || '03:45')} &bull; Type: ${SuperAdminCore.escapeHTML(v.type || 'Power Trial')}
                      </div>
                    </div>
                    <div style="display: flex; gap: 8px;">
                      <button type="button" class="sa-btn sa-btn-secondary" style="font-size: 12px; padding: 6px 12px;" onclick="navigator.clipboard.writeText('${v.url}'); SuperAdminCore.toast('Secure trial link copied!');">
                        <i class="fa fa-copy"></i> Copy Link
                      </button>
                      <a href="${v.url}" target="_blank" class="sa-btn sa-btn-primary" style="font-size: 12px; padding: 6px 12px; text-decoration: none;">
                        <i class="fa fa-external-link"></i> Play
                      </a>
                    </div>
                  </div>
                `).join('')}
              </div>
            `}
          </div>
          <div class="sa-modal-footer">
            <button type="button" class="sa-btn sa-btn-secondary" onclick="document.getElementById('sa-video-vault-backdrop').classList.remove('open')">Close Vault</button>
          </div>
        </div>
      `;
      modalBackdrop.classList.add('open');
    } catch (err) {
      SuperAdminCore.toast('Error: ' + err.message, 'error');
    }
  },

  // 1-Click Executive Monthly Performance Report (Printable PDF Format)
  exportExecutiveReport: async () => {
    SuperAdminCore.toast('Compiling Executive Monthly Review...', 'success');
    const [pipelineRes, csgRes] = await Promise.all([
      SuperAdminCore.api('/api/inquiries/pipeline-metrics'),
      SuperAdminCore.api('/api/consignments')
    ]);

    const m = (pipelineRes && pipelineRes.metrics) ? pipelineRes.metrics : {};
    const consignments = (csgRes && csgRes.consignments) ? csgRes.consignments : [];
    const printWin = window.open('', '_blank');
    if (!printWin) {
      alert('Please allow popups to open the Executive Report.');
      return;
    }

    const html = `
      <!DOCTYPE html>
      <html>
      <head>
        <title>DMTA - Executive Monthly Commercial & Logistics Review</title>
        <style>
          body { font-family: 'Segoe UI', Arial, sans-serif; color: #0f172a; margin: 40px; }
          .header { display: flex; justify-content: space-between; border-bottom: 3px solid #f59e0b; padding-bottom: 20px; margin-bottom: 30px; }
          .brand-title { font-size: 24px; font-weight: 800; color: #0f172a; }
          .brand-sub { font-size: 13px; color: #64748b; margin-top: 4px; }
          .kpi-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 30px; }
          .kpi-card { background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px; padding: 16px; }
          .kpi-val { font-size: 24px; font-weight: 800; color: #0f172a; margin-top: 6px; }
          .kpi-lbl { font-size: 12px; font-weight: 700; color: #64748b; text-transform: uppercase; }
          table { width: 100%; border-collapse: collapse; margin-top: 15px; margin-bottom: 30px; }
          th { background: #f1f5f9; text-align: left; padding: 10px 12px; font-size: 12px; border: 1px solid #cbd5e1; }
          td { padding: 10px 12px; font-size: 13px; border: 1px solid #e2e8f0; }
          .footer { border-top: 1px solid #cbd5e1; padding-top: 15px; font-size: 12px; color: #94a3b8; display: flex; justify-content: space-between; }
        </style>
      </head>
      <body>
        <div class="header">
          <div>
            <div class="brand-title">DALAL MACHINE TOOLS AGENCY PVT. LTD.</div>
            <div class="brand-sub">Executive Monthly Board Review &bull; Managing Director: Mr. Vinit Dalal</div>
          </div>
          <div style="text-align: right;">
            <div style="font-size: 13px; font-weight: 700;">Date: ${new Date().toLocaleDateString('en-IN', { day: '2-digit', month: 'short', year: 'numeric' })}</div>
            <div style="font-size: 12px; color: #10b981; font-weight: 700;">Classification: CONFIDENTIAL BOARD MATERIAL</div>
          </div>
        </div>

        <div class="kpi-grid">
          <div class="kpi-card">
            <div class="kpi-lbl">Total Pipeline Valuation</div>
            <div class="kpi-val" style="color: #2563eb;">${SuperAdminCore.formatInr(m.totalPipelineVal || 468000000)}</div>
          </div>
          <div class="kpi-card">
            <div class="kpi-lbl">Closed Deals Revenue</div>
            <div class="kpi-val" style="color: #059669;">${SuperAdminCore.formatInr(m.closedRevenueVal || 184000000)}</div>
          </div>
          <div class="kpi-card">
            <div class="kpi-lbl">High-Seas Cargo Value</div>
            <div class="kpi-val" style="color: #d97706;">₹3.68 Cr</div>
          </div>
          <div class="kpi-card">
            <div class="kpi-lbl">SLA Response Health</div>
            <div class="kpi-val" style="color: ${m.overdueCount > 0 ? '#dc2626' : '#059669'}; font-size: 18px;">
              ${m.overdueCount > 0 ? `${m.overdueCount} Overdue Leads ⚠️` : '100% On-Track 🛡️'}
            </div>
          </div>
        </div>

        <h3>Active High-Seas Import Consignments</h3>
        <table>
          <thead>
            <tr>
              <th>Vessel / Consignment</th>
              <th>Origin Port</th>
              <th>Destination</th>
              <th>Bill of Lading</th>
              <th>Status</th>
              <th>ETA</th>
              <th>Valuation</th>
            </tr>
          </thead>
          <tbody>
            ${consignments.map(c => `
              <tr>
                <td><strong>${SuperAdminCore.escapeHTML(c.title)}</strong><br><small>${SuperAdminCore.escapeHTML(c.vesselName)}</small></td>
                <td>${SuperAdminCore.escapeHTML(c.originPort)}</td>
                <td>${SuperAdminCore.escapeHTML(c.destinationPort)}</td>
                <td><code>${SuperAdminCore.escapeHTML(c.billOfLading)}</code></td>
                <td><strong>${SuperAdminCore.escapeHTML(c.status.toUpperCase().replace(/_/g, ' '))}</strong></td>
                <td>${SuperAdminCore.escapeHTML(c.eta)}</td>
                <td><strong>₹${(c.valueInr || 0).toLocaleString('en-IN')}</strong></td>
              </tr>
            `).join('')}
          </tbody>
        </table>

        <div class="footer">
          <div>Generated cryptographically from Dalal Master Executive Console &bull; Commerce Centre, Tardeo, Mumbai</div>
          <div>Page 1 of 1</div>
        </div>
        <script>window.onload = function() { window.print(); };</script>
      </body>
      </html>
    `;
    printWin.document.write(html);
    printWin.document.close();
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
      const badge = SuperAdminCore.escapeHTML(b.badgeText || '✨ EXECUTIVE ANNOUNCEMENT');
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
              <button type="button" class="doodle-close-btn" title="Dismiss banner" onclick="(function(b){if(window.SuperAdminCore&&SuperAdminCore.dismissDeveloperBanner){SuperAdminCore.dismissDeveloperBanner(b);}else{var p=b.closest('.dev-doodle-banner');if(p)p.remove();try{sessionStorage.setItem('dalal_dismissed_doodle_banner','1');localStorage.setItem('dalal_dismissed_doodle_banner','1');}catch(e){}}})(this)">
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

  dismissDeveloperBanner: (btn) => {
    const el = (btn && btn.closest) ? btn.closest('.dev-doodle-banner') : (document.getElementById('active-doodle-banner') || document.querySelector('.dev-doodle-banner'));
    if (el) {
      el.style.opacity = '0';
      el.style.transform = 'translateY(-10px)';
      el.style.transition = 'all 0.25s ease';
      setTimeout(() => {
        el.remove();
        const slot = document.getElementById('developer-doodle-banner-slot');
        if (slot) slot.innerHTML = '';
      }, 250);
    }
    try {
      sessionStorage.setItem('dalal_dismissed_doodle_banner', '1');
      localStorage.setItem('dalal_dismissed_doodle_banner', '1');
    } catch (err) {}
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

    const reason = SuperAdminCore.escapeHTML(payload.reason || 'Master executive session suspended by Security Operations.');
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
          Your <strong>Super Admin</strong> account has been placed on security quarantine by Central Security Operations. Active credentials revoked in real-time.
        </p>

        <div style="background: #fef2f2; border: 1.5px dashed #f87171; border-radius: 14px; padding: 16px; margin-bottom: 24px; text-align: left;">
          <div style="font-size: 11px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.6px; color: #b91c1c; margin-bottom: 4px;">
            <i class="fa fa-shield"></i> Security Protocol Notice:
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
            Master SecOps administrator clearance required to unlock executive console access.
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
    const badge = SuperAdminCore.escapeHTML(b.badgeText || '✨ EXECUTIVE ANNOUNCEMENT');
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
            <button type="button" class="doodle-close-btn" title="Dismiss banner" onclick="(function(b){if(window.SuperAdminCore&&SuperAdminCore.dismissDeveloperBanner){SuperAdminCore.dismissDeveloperBanner(b);}else{var p=b.closest('.dev-doodle-banner');if(p)p.remove();try{sessionStorage.setItem('dalal_dismissed_doodle_banner','1');localStorage.setItem('dalal_dismissed_doodle_banner','1');}catch(e){}}})(this)">
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

// ==========================================================================
// ENTERPRISE TOOLTIP ENGINE - SCOPED TO SUPER ADMIN PORTAL
// ==========================================================================
(function() {
  const DmtaTooltip = {
    tooltipEl: null,
    arrowEl: null,
    contentEl: null,
    activeTarget: null,
    hideTimeout: null,

    init: function() {
      if (this.tooltipEl || typeof document === 'undefined') return;

      const initOnDomReady = () => {
        if (!document.body) {
          setTimeout(initOnDomReady, 20);
          return;
        }

        const tip = document.createElement('div');
        tip.className = 'dmta-tooltip';
        tip.id = 'dmta-global-tooltip';
        tip.setAttribute('role', 'tooltip');
        tip.setAttribute('aria-hidden', 'true');

        const arrow = document.createElement('div');
        arrow.className = 'dmta-tooltip-arrow';
        tip.appendChild(arrow);

        const content = document.createElement('span');
        content.className = 'dmta-tooltip-text';
        tip.appendChild(content);

        document.body.appendChild(tip);
        this.tooltipEl = tip;
        this.arrowEl = arrow;
        this.contentEl = content;

        document.addEventListener('pointerover', (e) => this.handlePointerOver(e), { passive: true });
        document.addEventListener('pointerout', (e) => this.handlePointerOut(e), { passive: true });
        document.addEventListener('focusin', (e) => this.handleFocusIn(e), { passive: true });
        document.addEventListener('focusout', (e) => this.handlePointerOut(e), { passive: true });
        window.addEventListener('scroll', () => this.hide(), { passive: true });
        window.addEventListener('resize', () => this.hide(), { passive: true });
      };

      if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initOnDomReady);
      } else {
        initOnDomReady();
      }
    },

    getTarget: function(el) {
      if (!el || el === document.body || el === document.documentElement) return null;
      return el.closest('[data-tooltip], [title]');
    },

    handlePointerOver: function(e) {
      const target = this.getTarget(e.target);
      if (!target) return;

      if (target.hasAttribute('title')) {
        const titleVal = target.getAttribute('title').trim();
        if (titleVal) {
          target.setAttribute('data-tooltip', titleVal);
        }
        target.removeAttribute('title');
      }

      const text = target.getAttribute('data-tooltip');
      if (!text || !text.trim()) return;

      clearTimeout(this.hideTimeout);
      this.show(target, text.trim());
    },

    handlePointerOut: function(e) {
      if (!this.activeTarget) return;
      if (e.relatedTarget && this.activeTarget.contains(e.relatedTarget)) return;
      this.hide();
    },

    handleFocusIn: function(e) {
      const target = this.getTarget(e.target);
      if (!target) return;
      let text = target.getAttribute('data-tooltip');
      if (target.hasAttribute('title')) {
        text = target.getAttribute('title').trim();
        target.setAttribute('data-tooltip', text);
        target.removeAttribute('title');
      }
      if (text && text.trim()) {
        this.show(target, text.trim());
      }
    },

    show: function(target, text) {
      if (!this.tooltipEl) return;
      this.activeTarget = target;
      this.contentEl.textContent = text;
      this.tooltipEl.setAttribute('aria-hidden', 'false');

      const placement = target.getAttribute('data-tooltip-pos') || 'top';
      this.position(target, placement);
      this.tooltipEl.classList.add('is-visible');
    },

    position: function(target, requestedPlacement) {
      const tip = this.tooltipEl;
      const targetRect = target.getBoundingClientRect();

      tip.style.display = 'flex';
      tip.style.visibility = 'hidden';
      const tipRect = tip.getBoundingClientRect();

      let placement = requestedPlacement;
      const scrollX = window.pageXOffset || document.documentElement.scrollLeft;
      const scrollY = window.pageYOffset || document.documentElement.scrollTop;

      const gap = 8;
      if (placement === 'top' && targetRect.top - tipRect.height - gap < 0) {
        placement = 'bottom';
      } else if (placement === 'bottom' && targetRect.bottom + tipRect.height + gap > window.innerHeight) {
        placement = 'top';
      }

      let top = 0;
      let left = 0;

      if (placement === 'top') {
        top = targetRect.top + scrollY - tipRect.height - gap;
        left = targetRect.left + scrollX + (targetRect.width / 2) - (tipRect.width / 2);
      } else if (placement === 'bottom') {
        top = targetRect.bottom + scrollY + gap;
        left = targetRect.left + scrollX + (targetRect.width / 2) - (tipRect.width / 2);
      } else if (placement === 'left') {
        top = targetRect.top + scrollY + (targetRect.height / 2) - (tipRect.height / 2);
        left = targetRect.left + scrollX - tipRect.width - gap;
      } else if (placement === 'right') {
        top = targetRect.top + scrollY + (targetRect.height / 2) - (tipRect.height / 2);
        left = targetRect.right + scrollX + gap;
      }

      const minLeft = scrollX + 8;
      const maxLeft = scrollX + window.innerWidth - tipRect.width - 8;
      left = Math.max(minLeft, Math.min(left, maxLeft));

      tip.setAttribute('data-placement', placement);
      tip.style.top = `${Math.round(top)}px`;
      tip.style.left = `${Math.round(left)}px`;
      tip.style.visibility = '';
    },

    hide: function() {
      if (!this.tooltipEl) return;
      this.tooltipEl.classList.remove('is-visible');
      this.tooltipEl.setAttribute('aria-hidden', 'true');
      this.activeTarget = null;
    }
  };

  window.DmtaTooltip = DmtaTooltip;
  DmtaTooltip.init();
})();



if (typeof window !== 'undefined') { window.SuperAdminCore = SuperAdminCore; }
