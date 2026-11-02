
    // Tab Switching matching Admin Portal patterns
    function showDevTab(tabName, linkEl) {
      document.querySelectorAll('.tab-section').forEach(sec => sec.classList.remove('active'));
      document.querySelectorAll('.sidebar-nav .nav-link').forEach(link => link.classList.remove('active'));

      const targetSection = document.getElementById('tab-' + tabName);
      if (targetSection) targetSection.classList.add('active');

      if (linkEl) {
        linkEl.classList.add('active');
      } else {
        const found = Array.from(document.querySelectorAll('.sidebar-nav .nav-link')).find(l => l.getAttribute('href') === '#' + tabName);
        if (found) found.classList.add('active');
      }

      const titles = {
        'vitals': 'System Vitals & Architecture Telemetry',
        'governance': 'Staff & Administrative Account Governance (Developer Controls)',
        'doodle': 'Google Doodle & Dashboard Banner Studio',
        'tests': 'Automated Smoke Tests Runner',
        'api': 'Interactive API Workbench',
        'catalog': 'Machinery Catalog & Asset Health',
        'security': 'SecOps & Security Headers'
      };
      if (titles[tabName]) {
        document.getElementById('topbar-current-section').textContent = titles[tabName];
      }

      if (tabName === 'vitals') fetchTelemetry();
      if (tabName === 'governance') fetchAdminAccounts();
      if (tabName === 'doodle') fetchBannerConfig();
      if (tabName === 'catalog') fetchCatalogAudit();
      if (tabName === 'api') executeApiWorkbench();
      if (tabName === 'security') fetchSecurityStatus();

      // Mobile: Auto-close sidebar drawer upon tab selection
      if (window.innerWidth <= 992) {
        const sidebar = document.querySelector('.admin-sidebar');
        const backdrop = document.querySelector('.admin-mobile-backdrop');
        if (sidebar) sidebar.classList.remove('open');
        if (backdrop) backdrop.classList.remove('active');
      }

      // Update active state in mobile bottom navigation
      document.querySelectorAll('.dev-bottom-nav-item').forEach(item => {
        item.classList.remove('active');
        if (item.getAttribute('data-tab') === tabName) {
          item.classList.add('active');
        }
      });
    }

    // ── Universal Mobile Sidebar Drawer & Backdrop System ──
    const toggleBtn = document.getElementById('btn-sidebar-toggle');
    const sidebar = document.querySelector('.admin-sidebar');

    let backdrop = document.querySelector('.admin-mobile-backdrop');
    if (!backdrop) {
      backdrop = document.createElement('div');
      backdrop.className = 'admin-mobile-backdrop';
      document.body.appendChild(backdrop);
    }

    function toggleDevMenu(e) {
      if (e) e.stopPropagation();
      if (window.innerWidth <= 992) {
        if (sidebar) {
          sidebar.classList.toggle('open');
          backdrop.classList.toggle('active', sidebar.classList.contains('open'));
        }
      } else {
        document.body.classList.toggle('sidebar-collapsed');
      }
    }

    if (toggleBtn) toggleBtn.addEventListener('click', toggleDevMenu);
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

    // Close on Escape key
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && sidebar && sidebar.classList.contains('open')) {
        sidebar.classList.remove('open');
        backdrop.classList.remove('active');
      }
    });

    // Add close button to sidebar header for mobile
    const sidebarHeader = sidebar ? sidebar.querySelector('.sidebar-header') : null;
    if (sidebarHeader && !sidebarHeader.querySelector('.sidebar-drawer-close')) {
      const closeBtn = document.createElement('button');
      closeBtn.className = 'sidebar-drawer-close';
      closeBtn.innerHTML = '&times;';
      closeBtn.title = 'Close Navigation Menu';
      closeBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        if (sidebar) sidebar.classList.remove('open');
        if (backdrop) backdrop.classList.remove('active');
      });
      sidebarHeader.appendChild(closeBtn);
    }

    // ── Auto-Inject Dev Mobile Bottom Navigation Bar ──
    if (!document.querySelector('.dev-mobile-bottom-nav')) {
      const devBottomNav = document.createElement('nav');
      devBottomNav.className = 'dev-mobile-bottom-nav';
      devBottomNav.setAttribute('aria-label', 'Developer Console Navigation');
      devBottomNav.innerHTML = `
        <a href="javascript:void(0)" class="dev-bottom-nav-item active" data-tab="vitals" onclick="showDevTab('vitals');">
          <i class="fa fa-tachometer"></i>
          <span>Vitals</span>
        </a>
        <a href="javascript:void(0)" class="dev-bottom-nav-item" data-tab="security" onclick="showDevTab('security');">
          <i class="fa fa-shield"></i>
          <span>SecOps</span>
        </a>
        <a href="javascript:void(0)" class="dev-bottom-nav-item" data-tab="governance" onclick="showDevTab('governance');">
          <i class="fa fa-users"></i>
          <span>Accounts</span>
        </a>
        <a href="javascript:void(0)" class="dev-bottom-nav-item" data-tab="api" onclick="showDevTab('api');">
          <i class="fa fa-terminal"></i>
          <span>API Bench</span>
        </a>
        <a href="javascript:void(0)" id="dev-bottom-nav-menu-btn" class="dev-bottom-nav-item">
          <i class="fa fa-bars"></i>
          <span>Menu</span>
        </a>
      `;
      document.body.appendChild(devBottomNav);

      document.getElementById('dev-bottom-nav-menu-btn')?.addEventListener('click', (e) => {
        toggleDevMenu(e);
      });
    }

    // 1. Telemetry Loader
    let baseUptimeSec = 0;
    let uptimeTimer = null;

    async function fetchTelemetry(isManual) {
      try {
        const res = await fetch('/api/dev/telemetry');
        const data = await res.json();
        if (!data.success) return;

        document.getElementById('kpi-node-version').textContent = data.system.nodeVersion;
        document.getElementById('kpi-os-desc').textContent = `${data.system.platform} (${data.system.arch}) &bull; ${data.system.cpus} CPUs`;
        document.getElementById('kpi-pid').textContent = data.system.pid;
        document.getElementById('kpi-memory').textContent = `${data.memory.rssMB} MB`;
        document.getElementById('kpi-heap-desc').textContent = `Heap: ${data.memory.heapUsedMB} MB / ${data.memory.heapTotalMB} MB`;

        baseUptimeSec = data.system.uptimeSeconds;
        renderUptime();
        if (!uptimeTimer) {
          uptimeTimer = setInterval(() => {
            baseUptimeSec++;
            renderUptime();
          }, 1000);
        }

        if (isManual) {
          alert('System telemetry refreshed successfully!');
        }
      } catch (err) {
        console.error('Telemetry error:', err);
      }
    }

    function renderUptime() {
      const h = Math.floor(baseUptimeSec / 3600);
      const m = Math.floor((baseUptimeSec % 3600) / 60);
      const s = baseUptimeSec % 60;
      document.getElementById('kpi-uptime').textContent = `${h}h ${m}m ${s}s`;
    }

    // 2. Smoke Tests Runner
    async function runSmokeTests() {
      const btn = document.getElementById('btn-run-tests');
      const tbody = document.getElementById('smoke-tests-tbody');

      btn.disabled = true;
      btn.innerHTML = '<i class="fa fa-spinner fa-spin"></i> Executing Smoke Tests...';
      tbody.innerHTML = '<tr><td colspan="6" style="text-align:center; padding: 24px; color: var(--text-muted);"><i class="fa fa-spinner fa-spin fa-2x"></i><br><br>Testing 11 Public Routes & APIs...</td></tr>';

      try {
        const res = await fetch('/api/dev/run-tests', { method: 'POST' });
        const data = await res.json();

        btn.disabled = false;
        btn.innerHTML = '<i class="fa fa-play"></i> Re-Run All 11 Tests';

        if (!data.success) {
          tbody.innerHTML = '<tr><td colspan="6" style="text-align:center; color: #dc2626;">Test run failed.</td></tr>';
          return;
        }

        document.getElementById('test-total-count').textContent = data.summary.totalTests;
        document.getElementById('test-passed-count').textContent = data.summary.passed;
        document.getElementById('test-failed-count').textContent = data.summary.failed;
        document.getElementById('test-success-rate').textContent = data.summary.successRate;

        tbody.innerHTML = data.results.map(r => {
          const isPass = r.status === 'PASS';
          return `
            <tr>
              <td><strong>${r.name}</strong></td>
              <td><code>${r.path}</code></td>
              <td>${r.expectedStatus} OK</td>
              <td><span style="color:${isPass ? '#059669' : '#dc2626'}; font-weight:700;">${r.statusCode} ${isPass ? 'OK' : 'ERR'}</span></td>
              <td>${r.latencyMs} ms</td>
              <td>
                <span class="status-pill ${isPass ? 'active' : 'inactive'}">
                  <span class="status-dot ${isPass ? 'green' : 'red'}"></span>
                  <span>${r.status}</span>
                </span>
              </td>
            </tr>
          `;
        }).join('');
      } catch (err) {
        btn.disabled = false;
        btn.innerHTML = '<i class="fa fa-play"></i> Re-Run Tests';
        tbody.innerHTML = '<tr><td colspan="6" style="text-align:center; color: #dc2626;">Error running tests: ' + err.message + '</td></tr>';
      }
    }

    // 3. API Workbench
    async function executeApiWorkbench() {
      const endpoint = document.getElementById('api-select').value;
      const statusEl = document.getElementById('api-wb-status');
      const latencyEl = document.getElementById('api-wb-latency');
      const outputPre = document.getElementById('api-wb-output');

      outputPre.textContent = 'Calling ' + endpoint + '...';
      const t0 = performance.now();

      try {
        const res = await fetch(endpoint);
        const t1 = performance.now();
        const latency = Math.round(t1 - t0);

        statusEl.textContent = `${res.status} ${res.statusText || 'OK'}`;
        statusEl.style.color = res.ok ? '#059669' : '#dc2626';
        latencyEl.textContent = `${latency} ms`;

        const json = await res.json();
        outputPre.textContent = JSON.stringify(json, null, 2);
      } catch (err) {
        statusEl.textContent = 'ERROR';
        statusEl.style.color = '#dc2626';
        outputPre.textContent = 'Network or server error: ' + err.message;
      }
    }

    function copyWorkbenchJson() {
      const txt = document.getElementById('api-wb-output').textContent;
      navigator.clipboard.writeText(txt).then(() => {
        alert('Response JSON copied to clipboard!');
      });
    }

    // 4. Catalog Audit
    async function fetchCatalogAudit() {
      try {
        const res = await fetch('/api/dev/catalog-audit');
        const data = await res.json();
        if (!data.success) return;

        const a = data.audit;
        document.getElementById('cat-audit-total').textContent = a.totalMachines;
        document.getElementById('cat-audit-pune').textContent = a.puneStockCount;
        document.getElementById('cat-audit-images').textContent = `${a.imageIntegrity.verifiedCount} / ${a.totalMachines}`;
        document.getElementById('cat-audit-cats').textContent = a.categoriesCount;
        document.getElementById('sidebar-machines-count').textContent = a.totalMachines;

        const grid = document.getElementById('catalog-category-grid');
        grid.innerHTML = '';
        for (const [cat, cnt] of Object.entries(a.categoryDistribution)) {
          const item = document.createElement('div');
          item.style.cssText = 'background:#ffffff; border:1px solid #e2e8f0; border-radius:8px; padding:10px 14px; display:flex; justify-content:space-between; align-items:center; font-size:13px;';
          item.innerHTML = `<span style="font-weight:600; color:#1e293b;">${cat}</span><span style="font-family:'JetBrains Mono', monospace; font-weight:700; color:#d97706; background:#fef3c7; padding:2px 8px; border-radius:4px;">${cnt}</span>`;
          grid.appendChild(item);
        }
      } catch (err) {
        console.error('Catalog audit error:', err);
      }
    }

    // 5. Staff Account Governance (Developer Master Override)
    let targetBlockUserId = null;

    async function fetchAdminAccounts() {
      const tbody = document.getElementById('admin-accounts-tbody');
      tbody.innerHTML = `
        <tr>
          <td><div class="dev-skeleton-shimmer" style="height:18px; width:140px; margin-bottom:4px;"></div><div class="dev-skeleton-shimmer" style="height:12px; width:180px;"></div></td>
          <td><div class="dev-skeleton-shimmer" style="height:24px; width:110px; border-radius:999px;"></div></td>
          <td><div class="dev-skeleton-shimmer" style="height:24px; width:100px; border-radius:999px;"></div></td>
          <td><div class="dev-skeleton-shimmer" style="height:14px; width:160px;"></div></td>
          <td><div class="dev-skeleton-shimmer" style="height:32px; width:120px; border-radius:8px;"></div></td>
        </tr>
      `;

      try {
        const res = await fetch('/api/dev/admin-accounts');
        const data = await res.json();
        if (!data.success) {
          tbody.innerHTML = `<tr><td colspan="5" style="text-align:center; color:#dc2626;">Error: ${data.message}</td></tr>`;
          return;
        }

        let blockedCount = 0;
        tbody.innerHTML = data.accounts.map(acc => {
          const isBlocked = acc.blockedByDeveloper;
          if (isBlocked) blockedCount++;

          const roleBadge = acc.role === 'superadmin' 
            ? '<span class="status-pill new" style="background:#f5f3ff; color:#7c3aed; border:1px solid #ddd6fe;"><i class="fa fa-shield"></i> SUPER ADMIN</span>'
            : '<span class="status-pill contacted" style="background:#eff6ff; color:#2563eb; border:1px solid #bfdbfe;"><i class="fa fa-cogs"></i> STAFF ADMIN</span>';

          const statusBadge = isBlocked
            ? '<span class="status-pill inactive" style="background:#fef2f2; color:#b91c1c; border:1px solid #fecaca;"><span class="status-dot red"></span>SUSPENDED BY DEV</span>'
            : '<span class="status-pill active"><span class="status-dot green"></span>ACTIVE</span>';

          const suspensionInfo = isBlocked
            ? `<div style="font-size:12px; color:#991b1b; line-height:1.4;"><strong>Reason:</strong> ${escapeHtml(acc.blockedReason)}<br><small style="color:#64748b;">Blocked: ${acc.blockedAt ? new Date(acc.blockedAt).toLocaleString() : 'Recent'}</small></div>`
            : '<span style="color:#94a3b8; font-size:12px;">Normal operations</span>';

          const actionBtn = isBlocked
            ? `<button class="btn-primary" style="background:#059669; border-color:#059669; font-size:12px; padding:6px 14px;" onclick="unblockAccount('${acc.id}', '${escapeHtml(acc.username)}');" data-tooltip="Restore staff member login access"><i class="fa fa-unlock"></i> Unblock / Restore</button>`
            : `<button class="btn-secondary" style="color:#dc2626; border-color:#fca5a5; font-size:12px; padding:6px 14px;" onclick="openBlockModal('${acc.id}', '${escapeHtml(acc.username)}', '${acc.role}');" data-tooltip="Developer Killswitch: Instantly suspend staff account & terminate session"><i class="fa fa-ban"></i> Suspend Account</button>`;

          return `
            <tr>
              <td>
                <div style="font-weight:700; color:var(--text-main); font-size:13.5px;">${escapeHtml(acc.name || acc.username)}</div>
                <div style="font-family:'JetBrains Mono', monospace; font-size:11.5px; color:var(--text-muted);">@${escapeHtml(acc.username)} &bull; ${escapeHtml(acc.email)}</div>
              </td>
              <td>${roleBadge}</td>
              <td>${statusBadge}</td>
              <td>${suspensionInfo}</td>
              <td>${actionBtn}</td>
            </tr>
          `;
        }).join('');

        const badge = document.getElementById('sidebar-blocked-badge');
        if (badge) {
          badge.textContent = blockedCount > 0 ? `${blockedCount} Blocked` : 'All Active';
          badge.style.background = blockedCount > 0 ? '#fee2e2' : '#ecfdf5';
          badge.style.color = blockedCount > 0 ? '#b91c1c' : '#047857';
        }
      } catch (err) {
        tbody.innerHTML = `<tr><td colspan="5" style="text-align:center; color:#dc2626;">Network error loading accounts.</td></tr>`;
      }
    }

    function openBlockModal(id, username, role) {
      targetBlockUserId = id;
      document.getElementById('block-modal-target-user').textContent = username;
      document.getElementById('block-modal-target-role').textContent = role.toUpperCase();
      document.getElementById('modal-block-account').style.display = 'flex';
    }

    function closeBlockModal() {
      targetBlockUserId = null;
      document.getElementById('modal-block-account').style.display = 'none';
    }

    async function confirmBlockAccount() {
      if (!targetBlockUserId) return;
      const reason = document.getElementById('block-reason-input').value.trim() || 'Suspended by Lead Developer';
      const btn = document.getElementById('btn-confirm-block');
      btn.disabled = true;
      btn.innerHTML = '<i class="fa fa-spinner fa-spin"></i> Suspending...';

      try {
        const res = await fetch(`/api/dev/admin-accounts/${targetBlockUserId}/block`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ reason })
        });
        const data = await res.json();
        btn.disabled = false;
        btn.innerHTML = '<i class="fa fa-ban"></i> Confirm Suspend';
        closeBlockModal();

        if (data.success) {
          alert(data.message);
          fetchAdminAccounts();
        } else {
          alert('Failed to suspend account: ' + data.message);
        }
      } catch (err) {
        btn.disabled = false;
        btn.innerHTML = '<i class="fa fa-ban"></i> Confirm Suspend';
        alert('Network error while suspending account.');
      }
    }

    async function unblockAccount(id, username) {
      if (!confirm(`Are you sure you want to restore and unblock [${username}]?`)) return;

      try {
        const res = await fetch(`/api/dev/admin-accounts/${id}/unblock`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' }
        });
        const data = await res.json();
        if (data.success) {
          alert(data.message);
          fetchAdminAccounts();
        } else {
          alert('Failed to unblock account: ' + data.message);
        }
      } catch (err) {
        alert('Network error unblocking account.');
      }
    }

    // 6. Google Doodle & Dashboard Banner Studio
    async function fetchBannerConfig() {
      try {
        const res = await fetch('/api/dev/banner');
        const data = await res.json();
        if (data.success && data.banner) {
          document.getElementById('banner-toggle-active').checked = Boolean(data.banner.active);
          document.getElementById('banner-style-select').value = data.banner.style || 'doodle-gold';
          document.getElementById('banner-icon-select').value = data.banner.icon || 'fa-trophy';
          document.getElementById('banner-badge-input').value = data.banner.badgeText || '✨ DEVELOPER DOODLE SPOTLIGHT';
          document.getElementById('banner-title-input').value = data.banner.title || 'Dalal Machinery Milestone';
          document.getElementById('banner-link-text').value = data.banner.linkText || 'Explore Machines';
          document.getElementById('banner-link-url').value = data.banner.linkUrl || '/admin/products.html';
          document.getElementById('banner-msg-input').value = data.banner.message || '';
          document.getElementById('banner-dismissable-check').checked = data.banner.dismissable !== false;

          updateDoodleLivePreview();
          updateSidebarBannerBadge(data.banner.active);
        }
      } catch (err) {
        console.error('Failed to load banner config:', err);
      }
    }

    function updateSidebarBannerBadge(isActive) {
      const b = document.getElementById('sidebar-banner-status');
      if (b) {
        b.textContent = isActive ? 'Live Active' : 'Off';
        b.style.background = isActive ? '#ecfdf5' : '#f1f5f9';
        b.style.color = isActive ? '#047857' : '#64748b';
      }
    }

    function updateDoodleLivePreview() {
      const active = document.getElementById('banner-toggle-active').checked;
      const styleClass = document.getElementById('banner-style-select').value;
      const iconClass = document.getElementById('banner-icon-select').value;
      const badge = escapeHtml(document.getElementById('banner-badge-input').value || '✨ DEVELOPER DOODLE SPOTLIGHT');
      const title = escapeHtml(document.getElementById('banner-title-input').value || 'Milestone Announcement');
      const msg = escapeHtml(document.getElementById('banner-msg-input').value || '');
      const linkText = escapeHtml(document.getElementById('banner-link-text').value || 'Explore');
      const linkUrl = document.getElementById('banner-link-url').value;
      const dismissable = document.getElementById('banner-dismissable-check').checked;

      const previewBox = document.getElementById('doodle-live-preview-box');
      const pill = document.getElementById('doodle-preview-pill');
      const pillText = document.getElementById('doodle-live-status-text');

      if (active) {
        pill.className = 'status-pill active';
        pillText.textContent = 'BROADCAST ACTIVE ON DASHBOARDS';
      } else {
        pill.className = 'status-pill inactive';
        pillText.textContent = 'BROADCAST DISABLED';
      }

      previewBox.innerHTML = `
        <div class="dev-doodle-banner ${styleClass}" style="margin-bottom:0;">
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
              ${msg ? `<div class="doodle-desc">${msg}</div>` : ''}
            </div>
          </div>
          <div class="doodle-right">
            ${linkUrl && linkText ? `
              <a href="javascript:void(0)" class="doodle-btn">
                <span>${linkText}</span>
                <i class="fa fa-arrow-right"></i>
              </a>
            ` : ''}
            ${dismissable ? `
              <button type="button" class="doodle-close-btn" title="Simulate dismiss">
                <i class="fa fa-times"></i>
              </button>
            ` : ''}
          </div>
        </div>
      `;
    }

    async function saveDeveloperBanner(e) {
      e.preventDefault();
      const btn = document.getElementById('btn-save-banner');
      btn.disabled = true;
      btn.innerHTML = '<i class="fa fa-spinner fa-spin"></i> Broadcasting...';

      const payload = {
        active: document.getElementById('banner-toggle-active').checked,
        style: document.getElementById('banner-style-select').value,
        icon: document.getElementById('banner-icon-select').value,
        badgeText: document.getElementById('banner-badge-input').value.trim(),
        title: document.getElementById('banner-title-input').value.trim(),
        message: document.getElementById('banner-msg-input').value.trim(),
        linkText: document.getElementById('banner-link-text').value.trim(),
        linkUrl: document.getElementById('banner-link-url').value.trim(),
        dismissable: document.getElementById('banner-dismissable-check').checked
      };

      try {
        const res = await fetch('/api/dev/banner', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });
        const data = await res.json();
        btn.disabled = false;
        btn.innerHTML = '<i class="fa fa-paper-plane"></i> Save & Broadcast Doodle';

        if (data.success) {
          alert('Google Doodle Banner saved and broadcasted successfully to all Dashboards!');
          updateSidebarBannerBadge(payload.active);
        } else {
          alert('Error saving banner: ' + data.message);
        }
      } catch (err) {
        btn.disabled = false;
        btn.innerHTML = '<i class="fa fa-paper-plane"></i> Save & Broadcast Doodle';
        alert('Network error saving banner.');
      }
    }

    function escapeHtml(str) {
      if (!str) return '';
      return String(str)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#39;');
    }

    // 7. Developer Real-Time WebSocket Engine
    let devSocket = null;
    function initDevRealtime() {
      if (typeof io === 'undefined') {
        const script = document.createElement('script');
        script.src = '/socket.io/socket.io.js';
        script.onload = setupDevSocket;
        script.onerror = () => {
          const cdn = document.createElement('script');
          cdn.src = 'https://cdn.socket.io/4.8.1/socket.io.min.js';
          cdn.onload = setupDevSocket;
          document.head.appendChild(cdn);
        };
        document.head.appendChild(script);
      } else {
        setupDevSocket();
      }
    }

    function setupDevSocket() {
      if (devSocket) return;
      devSocket = io({ reconnection: true });

      const badge = document.getElementById('ws-status-badge');
      const dot = document.getElementById('ws-status-dot');
      const text = document.getElementById('ws-status-text');

      devSocket.on('connect', () => {
        if (dot) dot.style.background = '#10b981';
        if (text) text.textContent = 'WS: Connected (Duplex)';
        if (badge) {
          badge.style.background = '#ecfdf5';
          badge.style.borderColor = '#a7f3d0';
          badge.style.color = '#047857';
        }
        devSocket.emit('auth:register', { mode: 'developer' });
      });

      devSocket.on('disconnect', () => {
        if (dot) dot.style.background = '#ef4444';
        if (text) text.textContent = 'WS: Disconnected';
        if (badge) {
          badge.style.background = '#fef2f2';
          badge.style.borderColor = '#fca5a5';
          badge.style.color = '#b91c1c';
        }
      });

      // Live listen to account status changes from any session
      devSocket.on('dev:account_status_changed', (data) => {
        console.log('[DevWS] Account status changed:', data);
        fetchAdminAccounts();
      });

      // Live listen to catalog changes
      devSocket.on('catalog:inventory_synced', () => {
        fetchCatalogAudit();
      });

      // Live listen to real-time telemetry vitals tick
      devSocket.on('telemetry:tick', (data) => {
        if (!data) return;
        const memEl = document.getElementById('kpi-memory');
        const heapEl = document.getElementById('kpi-heap-desc');
        if (memEl && data.memory) memEl.textContent = `${data.memory.rssMB} MB`;
        if (heapEl && data.memory) heapEl.textContent = `Heap: ${data.memory.heapUsedMB} MB / ${data.memory.heapTotalMB} MB • Active Sockets: ${data.activeSockets}`;
        if (data.uptimeSeconds !== undefined) {
          baseUptimeSec = data.uptimeSeconds;
          renderUptime();
        }
      });

      // Live listen to security intrusion alerts
      devSocket.on('security:intrusion_alert', (evt) => {
        console.warn('[SecOps Alert] Intrusion detected:', evt);
        fetchSecurityStatus();
      });
    }

    // SecOps & Firewall Management Logic
    let currentSecurityData = null;

    async function fetchSecurityStatus() {
      try {
        const res = await fetch('/api/dev/security/status');
        const data = await res.json();
        if (!data.success) return;
        currentSecurityData = data;

        // Update Key & Gateway URL
        const keyEl = document.getElementById('sec-gateway-key');
        if (keyEl) keyEl.textContent = data.gatewayKey || 'dmta-ops-2026';

        // Update Banned Count
        const countEl = document.getElementById('sec-banned-count');
        if (countEl) countEl.textContent = `${data.activeBansCount || 0} Banned IP${data.activeBansCount === 1 ? '' : 's'}`;

        // Update Lockdown Status
        const lockStatusEl = document.getElementById('sec-lockdown-status');
        const lockBtn = document.getElementById('btn-toggle-lockdown');
        const lockCard = document.getElementById('sec-lockdown-card');
        if (data.lockdownActive) {
          if (lockStatusEl) {
            lockStatusEl.textContent = 'ENGAGED • 404 CLOAK';
            lockStatusEl.style.color = '#dc2626';
          }
          if (lockBtn) {
            lockBtn.innerHTML = '<i class="fa fa-unlock"></i> Disengage Lockdown';
            lockBtn.style.background = '#dc2626';
            lockBtn.style.color = '#ffffff';
          }
          if (lockCard) lockCard.style.background = '#fef2f2';
        } else {
          if (lockStatusEl) {
            lockStatusEl.textContent = 'DISENGAGED (NORMAL)';
            lockStatusEl.style.color = '#10b981';
          }
          if (lockBtn) {
            lockBtn.innerHTML = '<i class="fa fa-power-off"></i> Engage Lockdown';
            lockBtn.style.background = '';
            lockBtn.style.color = '#dc2626';
          }
          if (lockCard) lockCard.style.background = '';
        }

        // Render Blacklist Table
        const blTbody = document.getElementById('sec-blacklist-tbody');
        if (blTbody) {
          if (!data.activeBans || data.activeBans.length === 0) {
            blTbody.innerHTML = '<tr><td colspan="5" style="text-align:center; color:#64748b; padding:20px;">No malicious IPs currently blacklisted. All systems nominal.</td></tr>';
          } else {
            blTbody.innerHTML = data.activeBans.map(b => `
              <tr>
                <td><code style="background:#fee2e2; color:#991b1b; padding:2px 6px; border-radius:4px; font-weight:700;">${b.ip}</code></td>
                <td><span style="font-size:12.5px; color:#475569;">${b.reason || 'Intrusion probe'}</span></td>
                <td><span style="font-size:12px; color:#64748b;">${new Date(b.bannedAt).toLocaleTimeString()}</span></td>
                <td><span style="font-size:12px; color:#64748b;">${b.expiresAt ? new Date(b.expiresAt).toLocaleTimeString() : 'Permanent'}</span></td>
                <td>
                  <button type="button" class="btn-secondary" style="padding:4px 8px; font-size:11px;" onclick="unbanIp('${b.ip}')">
                    <i class="fa fa-unlock"></i> Unban
                  </button>
                </td>
              </tr>
            `).join('');
          }
        }

        // Render Security Probes Table
        const evTbody = document.getElementById('sec-events-tbody');
        if (evTbody) {
          if (!data.recentEvents || data.recentEvents.length === 0) {
            evTbody.innerHTML = '<tr><td colspan="6" style="text-align:center; color:#64748b; padding:20px;">No intrusion probes detected yet.</td></tr>';
          } else {
            evTbody.innerHTML = data.recentEvents.map(e => `
              <tr>
                <td><span style="font-size:11.5px; color:#64748b;">${new Date(e.timestamp).toLocaleTimeString()}</span></td>
                <td><code style="font-size:12px;">${e.ip}</code></td>
                <td><code style="font-size:12px; color:#b45309;">${e.path || '/'}</code></td>
                <td><span class="status-pill active" style="background:${e.severity === 'HIGH' ? '#fee2e2' : '#fef3c7'}; color:${e.severity === 'HIGH' ? '#991b1b' : '#92400e'};">${e.severity}</span></td>
                <td>${e.autoBanned ? '<span style="color:#dc2626; font-weight:700;">YES (Banned)</span>' : '<span style="color:#059669;">NO</span>'}</td>
                <td><span style="font-size:12px; color:#475569;">${e.message || 'Probe logged'}</span></td>
              </tr>
            `).join('');
          }
        }
      } catch (err) {
        console.error('Failed to load security status:', err);
      }
    }

    function copyGatewayLink() {
      const key = (currentSecurityData && currentSecurityData.gatewayKey) || 'dmta-ops-2026';
      const fullUrl = `${window.location.origin}/portal-gate?key=${key}&to=dev`;
      navigator.clipboard.writeText(fullUrl).then(() => {
        const fb = document.getElementById('gateway-copy-feedback');
        if (fb) {
          fb.style.display = 'inline';
          setTimeout(() => { fb.style.display = 'none'; }, 3000);
        }
      });
    }

    async function toggleLockdown() {
      const currentState = currentSecurityData ? currentSecurityData.lockdownActive : false;
      const targetState = !currentState;
      const confirmMsg = targetState
        ? 'WARNING: You are about to engage EMERGENCY PORTAL LOCKDOWN. All admin, superadmin, and dev URLs will return HTTP 404 to all users except developer session. Proceed?'
        : 'Lift Emergency Portal Lockdown and restore standard gateway operations?';
      if (!confirm(confirmMsg)) return;

      try {
        const res = await fetch('/api/dev/security/lockdown', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ enabled: targetState })
        });
        const data = await res.json();
        alert(data.message);
        fetchSecurityStatus();
      } catch (err) {
        alert('Failed to toggle lockdown: ' + err.message);
      }
    }

    async function unbanIp(ip) {
      if (!confirm(`Release IP ${ip} from firewall blacklist?`)) return;
      try {
        const res = await fetch('/api/dev/security/unban', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ ip })
        });
        const data = await res.json();
        alert(data.message);
        fetchSecurityStatus();
      } catch (err) {
        alert('Failed to unban IP: ' + err.message);
      }
    }

    async function manualBanIp() {
      const input = document.getElementById('manual-ban-ip');
      const ip = input ? input.value.trim() : '';
      if (!ip) return alert('Please enter an IP address to ban.');
      try {
        const res = await fetch('/api/dev/security/ban', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ ip, reason: 'Manual ban from Developer SecOps panel' })
        });
        const data = await res.json();
        alert(data.message);
        if (input) input.value = '';
        fetchSecurityStatus();
      } catch (err) {
        alert('Failed to ban IP: ' + err.message);
      }
    }

    // Startup
    document.addEventListener('DOMContentLoaded', () => {
      initDevRealtime();
      fetchTelemetry();
      fetchCatalogAudit();
      fetchAdminAccounts();
      fetchBannerConfig();
      fetchSecurityStatus();
      executeApiWorkbench();
    });
  