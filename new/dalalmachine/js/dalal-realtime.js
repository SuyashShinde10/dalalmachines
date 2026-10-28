// Dalal Machine Tools - Public Website Real-Time WebSocket Synchronization Client
(function() {
  function initPublicRealtime() {
    if (typeof io === 'undefined') {
      const script = document.createElement('script');
      script.src = '/socket.io/socket.io.js';
      script.onload = connectPublicSocket;
      script.onerror = () => {
        const cdn = document.createElement('script');
        cdn.src = 'https://cdn.socket.io/4.8.1/socket.io.min.js';
        cdn.onload = connectPublicSocket;
        document.head.appendChild(cdn);
      };
      document.head.appendChild(script);
    } else {
      connectPublicSocket();
    }
  }

  function connectPublicSocket() {
    try {
      const socket = io({ reconnection: true });
      socket.on('connect', () => {
        socket.emit('auth:register', { mode: 'public' });
      });

      // Live Google Doodle Announcement Bar across Public Website
      socket.on('doodle:banner_broadcast', (banner) => {
        applyPublicBanner(banner);
      });

      // Live Machinery Catalog Synchronized across Website
      socket.on('catalog:inventory_synced', (data) => {
        console.log('[PublicWS] Live Catalog Sync Event:', data);
        showPublicSyncToast(data);

        // Notify page scripts
        window.dispatchEvent(new CustomEvent('dalal:catalog_synced', { detail: data }));

        // If category.html has active dynamic filter, re-render
        if (typeof window.renderCategoryMachines === 'function') {
          window.renderCategoryMachines();
        }
      });

      // Initial check for active doodle banner
      fetch('/api/system/developer-banner')
        .then(r => r.json())
        .then(d => {
          if (d.success && d.banner) applyPublicBanner(d.banner);
        })
        .catch(() => {});
    } catch (e) {
      console.debug('Public WebSocket offline:', e);
    }
  }

  function applyPublicBanner(banner) {
    let topSlot = document.getElementById('public-doodle-banner-slot');
    if (!topSlot) {
      topSlot = document.createElement('div');
      topSlot.id = 'public-doodle-banner-slot';
      document.body.prepend(topSlot);
    }

    if (!banner || !banner.active) {
      topSlot.style.display = 'none';
      topSlot.innerHTML = '';
      return;
    }

    topSlot.style.display = 'block';
    topSlot.innerHTML = `
      <div style="background: linear-gradient(90deg, #0f172a 0%, #1e293b 50%, #0f172a 100%); color: #ffffff; padding: 10px 20px; font-size: 13px; font-weight: 600; display: flex; align-items: center; justify-content: space-between; border-bottom: 2px solid #f59e0b; box-shadow: 0 4px 12px rgba(0,0,0,0.15); z-index: 9999; position: relative;">
        <div style="display: flex; align-items: center; gap: 10px; margin: 0 auto; flex-wrap: wrap; justify-content: center;">
          <span style="background: #f59e0b; color: #000; padding: 2px 10px; border-radius: 9999px; font-size: 10.5px; font-weight: 800; text-transform: uppercase;">
            ${banner.badgeText || 'ANNOUNCEMENT'}
          </span>
          <span><strong>${banner.title}:</strong> ${banner.message || ''}</span>
          ${banner.linkUrl ? `<a href="${banner.linkUrl}" style="color: #f59e0b; text-decoration: underline; margin-left: 6px; font-weight: 700;">${banner.linkText || 'Learn More &rarr;'}</a>` : ''}
        </div>
        <button onclick="this.parentElement.style.display='none'" style="background:none; border:none; color:#94a3b8; font-size:18px; cursor:pointer; line-height:1;" title="Dismiss">&times;</button>
      </div>
    `;
  }

  function showPublicSyncToast(data) {
    let toast = document.getElementById('dalal-live-sync-toast');
    if (!toast) {
      toast = document.createElement('div');
      toast.id = 'dalal-live-sync-toast';
      toast.style.cssText = 'position:fixed; bottom:24px; left:24px; z-index:99999; background:#0f172a; color:#f8fafc; border:1px solid #334155; border-left:4px solid #10b981; border-radius:12px; padding:12px 18px; font-size:13px; font-family:"Plus Jakarta Sans",sans-serif; box-shadow:0 20px 25px -5px rgba(0,0,0,0.3); display:flex; align-items:center; gap:10px; transition:all 0.3s cubic-bezier(0.16,1,0.3,1); opacity:0; transform:translateY(16px);';
      document.body.appendChild(toast);
    }
    const machineName = data.product ? data.product.name : 'Machinery inventory';
    const action = data.action ? data.action.toLowerCase() : 'updated';
    toast.innerHTML = `<span style="color:#10b981; font-size:16px;">⚡</span> <div><strong style="color:#ffffff;">Live Stock Update:</strong> ${machineName} <span style="color:#94a3b8; font-size:11px;">(${action})</span></div>`;
    toast.style.opacity = '1';
    toast.style.transform = 'translateY(0)';
    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transform = 'translateY(16px)';
    }, 4000);
  }
    } catch (e) {
      console.debug('Public WebSocket offline:', e);
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initPublicRealtime);
  } else {
    initPublicRealtime();
  }
})();

