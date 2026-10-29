// Dalal Machine Tools Agency Pvt. Ltd.
// Enterprise In-Memory Micro-Cache & High-Performance Accelerator Engine
// Version: 1.0 | Sub-5ms API Latency | Top 1% High-Throughput Standard

const crypto = require('crypto');

class CacheEngine {
  constructor() {
    this.cache = new Map(); // key -> { data, etag, contentType, expiresAt, hits }
    this.stats = {
      hits: 0,
      misses: 0,
      invalidations: 0,
      createdCount: 0
    };
  }

  /**
   * Generate high-speed SHA-256 ETag from data
   */
  generateETag(data) {
    const str = typeof data === 'string' ? data : JSON.stringify(data);
    return '"' + crypto.createHash('sha256').update(str).digest('hex').substring(0, 24) + '"';
  }

  /**
   * Set key in cache with TTL (in seconds)
   */
  set(key, data, ttlSeconds = 60, contentType = 'application/json') {
    const etag = this.generateETag(data);
    const expiresAt = Date.now() + (ttlSeconds * 1000);
    this.cache.set(key, {
      data,
      etag,
      contentType,
      expiresAt,
      hits: 0,
      cachedAt: new Date().toISOString()
    });
    this.stats.createdCount++;
  }

  /**
   * Retrieve cached entry
   */
  get(key) {
    const entry = this.cache.get(key);
    if (!entry) {
      this.stats.misses++;
      return null;
    }

    // Check expiration
    if (Date.now() > entry.expiresAt) {
      this.cache.delete(key);
      this.stats.misses++;
      return null;
    }

    entry.hits++;
    this.stats.hits++;
    return entry;
  }

  /**
   * Invalidate specific key or prefix pattern
   */
  invalidate(pattern = null) {
    if (!pattern) {
      const count = this.cache.size;
      this.cache.clear();
      this.stats.invalidations += count;
      return count;
    }

    let deleted = 0;
    for (const key of this.cache.keys()) {
      if (typeof pattern === 'string' && key.startsWith(pattern)) {
        this.cache.delete(key);
        deleted++;
      } else if (pattern instanceof RegExp && pattern.test(key)) {
        this.cache.delete(key);
        deleted++;
      }
    }
    this.stats.invalidations += deleted;
    return deleted;
  }

  /**
   * Express Middleware for High-Speed Micro-Caching with ETag 304 Support
   */
  middleware(ttlSeconds = 60) {
    return (req, res, next) => {
      // Only cache safe GET / HEAD requests
      if (req.method !== 'GET' && req.method !== 'HEAD') {
        return next();
      }

      // Do NOT cache authenticated admin sessions or sensitive queries
      if (req.headers['authorization'] || req.cookies?.admin_token) {
        return next();
      }

      const cacheKey = req.originalUrl || req.url;
      const cached = this.get(cacheKey);

      if (cached) {
        res.setHeader('X-Cache-Engine', 'HIT-IN-MEMORY');
        res.setHeader('ETag', cached.etag);
        res.setHeader('Vary', 'Accept-Encoding');
        res.setHeader('Cache-Control', `public, max-age=${Math.max(1, Math.floor((cached.expiresAt - Date.now()) / 1000))}`);

        // Check Conditional Request (If-None-Match)
        const clientETag = req.headers['if-none-match'];
        if (clientETag && (clientETag === cached.etag || clientETag === `W/${cached.etag}`)) {
          return res.status(304).end(); // 0 byte transfer! Instant 304 Not Modified
        }

        res.setHeader('Content-Type', cached.contentType);
        return res.send(cached.data);
      }

      // Cache Miss: Intercept res.send / res.json
      res.setHeader('X-Cache-Engine', 'MISS');
      const originalSend = res.send.bind(res);

      res.send = (body) => {
        // Only cache 200 OK responses
        if (res.statusCode === 200 && body) {
          const contentType = res.getHeader('Content-Type') || 'application/json';
          this.set(cacheKey, body, ttlSeconds, contentType);
          const newETag = this.generateETag(body);
          res.setHeader('ETag', newETag);
        }
        return originalSend(body);
      };

      next();
    };
  }

  /**
   * Telemetry stats for Developer Console
   */
  getTelemetry() {
    const totalRequests = this.stats.hits + this.stats.misses;
    const hitRatio = totalRequests > 0 ? ((this.stats.hits / totalRequests) * 100).toFixed(1) : '100.0';
    return {
      entriesCached: this.cache.size,
      hits: this.stats.hits,
      misses: this.stats.misses,
      hitRatio: `${hitRatio}%`,
      invalidations: this.stats.invalidations,
      uptime: process.uptime()
    };
  }
}

// Global Singleton Instance
const cacheEngine = new CacheEngine();

module.exports = cacheEngine;

