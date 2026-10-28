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
      });
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

