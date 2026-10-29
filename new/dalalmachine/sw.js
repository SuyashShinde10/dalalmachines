// Dalal Machine Tools Agency Pvt. Ltd.
// Enterprise Offline Service Worker & PWA Accelerator
// Version: 1.0 | Offline Warehouse Catalog Mode

const CACHE_NAME = 'dmta-app-shell-v1';
const CATALOG_CACHE = 'dmta-catalog-cache-v1';

const STATIC_ASSETS = [
  '/',
  '/new/dalalmachine/',
  '/new/dalalmachine/css/style.css',
  '/new/dalalmachine/css/responsive.css',
  '/new/dalalmachine/images/logo-dalal.png',
  '/new/dalalmachine/images/favicon.png',
  '/manifest.json'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(STATIC_ASSETS).catch(err => {
        console.warn('[SW] Non-critical cache asset failed:', err);
      });
    }).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.map((key) => {
          if (key !== CACHE_NAME && key !== CATALOG_CACHE) {
            return caches.delete(key);
          }
        })
      );
    }).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (event) => {
  const url = new URL(event.request.url);

  // 1. Never cache admin/superadmin/dev portals or POST mutations
  if (
    url.pathname.startsWith('/admin') ||
    url.pathname.startsWith('/superadmin') ||
    url.pathname.startsWith('/dev') ||
    url.pathname.startsWith('/portal-gate') ||
    event.request.method !== 'GET'
  ) {
    return;
  }

  // 2. Catalog API Offline Cache (Stale-While-Revalidate)
  if (url.pathname === '/api/products' || url.pathname.startsWith('/api/products/')) {
    event.respondWith(
      caches.open(CATALOG_CACHE).then((cache) => {
        return fetch(event.request)
          .then((networkResponse) => {
            if (networkResponse.status === 200) {
              cache.put(event.request, networkResponse.clone());
            }
            return networkResponse;
          })
          .catch(() => {
            // Offline fallback from cache
            return cache.match(event.request).then(cached => {
              if (cached) return cached;
              return new Response(JSON.stringify({ success: true, offline: true, products: [] }), {
                headers: { 'Content-Type': 'application/json' }
              });
            });
          });
      })
    );
    return;
  }

  // 3. Static Assets: Cache-First with Network Fallback
  event.respondWith(
    caches.match(event.request).then((cached) => {
      if (cached) return cached;
      return fetch(event.request).then((response) => {
        if (response.status === 200 && (url.pathname.endsWith('.css') || url.pathname.endsWith('.js') || url.pathname.endsWith('.webp') || url.pathname.endsWith('.png'))) {
          const clone = response.clone();
          caches.open(CACHE_NAME).then(c => c.put(event.request, clone));
        }
        return response;
      });
    })
  );
});

