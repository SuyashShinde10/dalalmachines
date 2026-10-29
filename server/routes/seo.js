const express = require('express');
const router = express.Router();
const db = require('../db');

/**
 * Enterprise SEO & AI Crawler Optimization Engine
 * Generates dynamic sitemap.xml and robots.txt based on active database inventory.
 */

// Canonical Base URL
const SITE_URL = process.env.SITE_URL || 'https://dalalmachines.com';

// GET /sitemap.xml
router.get('/sitemap.xml', (req, res) => {
  try {
    const products = db.getProducts({ all: 'true' }) || [];
    const categories = db.getCategories() || [];
    const now = new Date().toISOString().split('T')[0];

    // Core static landing pages
    const staticPages = [
      { loc: `${SITE_URL}/`, priority: '1.0', changefreq: 'daily' },
      { loc: `${SITE_URL}/new/dalalmachine/`, priority: '1.0', changefreq: 'daily' },
      { loc: `${SITE_URL}/new/dalalmachine/category.html`, priority: '0.9', changefreq: 'daily' },
      { loc: `${SITE_URL}/new/dalalmachine/services.html`, priority: '0.8', changefreq: 'weekly' },
      { loc: `${SITE_URL}/new/dalalmachine/about.html`, priority: '0.8', changefreq: 'monthly' },
      { loc: `${SITE_URL}/new/dalalmachine/gallery.html`, priority: '0.7', changefreq: 'weekly' },
      { loc: `${SITE_URL}/new/dalalmachine/contact.html`, priority: '0.8', changefreq: 'monthly' }
    ];

    let xml = `<?xml version="1.0" encoding="UTF-8"?>\n`;
    xml += `<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"\n`;
    xml += `        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">\n`;

    // 1. Static Pages
    staticPages.forEach(p => {
      xml += `  <url>\n`;
      xml += `    <loc>${p.loc}</loc>\n`;
      xml += `    <lastmod>${now}</lastmod>\n`;
      xml += `    <changefreq>${p.changefreq}</changefreq>\n`;
      xml += `    <priority>${p.priority}</priority>\n`;
      xml += `  </url>\n`;
    });

    // 2. Category Pages
    categories.forEach(cat => {
      const catId = typeof cat === 'string' ? cat : (cat.id || cat.slug);
      if (!catId) return;
      xml += `  <url>\n`;
      xml += `    <loc>${SITE_URL}/new/dalalmachine/category.html?category=${encodeURIComponent(catId)}</loc>\n`;
      xml += `    <lastmod>${now}</lastmod>\n`;
      xml += `    <changefreq>weekly</changefreq>\n`;
      xml += `    <priority>0.75</priority>\n`;
      xml += `  </url>\n`;
    });

    // 3. Dynamic Product Pages (All 49+ inventory machines)
    products.forEach(p => {
      if (!p.id) return;
      const lastModDate = (p.updatedAt || p.createdAt || now).split('T')[0];
      const prodUrl = `${SITE_URL}/new/dalalmachine/product.html?id=${encodeURIComponent(p.id)}`;
      xml += `  <url>\n`;
      xml += `    <loc>${prodUrl}</loc>\n`;
      xml += `    <lastmod>${lastModDate}</lastmod>\n`;
      xml += `    <changefreq>weekly</changefreq>\n`;
      xml += `    <priority>0.85</priority>\n`;
      if (p.image) {
        const fullImg = p.image.startsWith('http') ? p.image : `${SITE_URL}/new/dalalmachine/${p.image.replace(/^\/+/, '')}`;
        xml += `    <image:image>\n`;
        xml += `      <image:loc>${fullImg}</image:loc>\n`;
        xml += `      <image:title>${escapeXml(p.name || 'Industrial Machine')}</image:title>\n`;
        xml += `    </image:image>\n`;
      }
      xml += `  </url>\n`;
    });

    xml += `</urlset>`;

    res.setHeader('Content-Type', 'application/xml; charset=utf-8');
    res.setHeader('Cache-Control', 'public, max-age=3600, stale-while-revalidate=86400');
    return res.send(xml);
  } catch (err) {
    console.error('[SEO Sitemap Error]:', err);
    res.status(500).send('Error generating sitemap.xml');
  }
});

// GET /robots.txt
router.get('/robots.txt', (req, res) => {
  const robots = `# Dalal Machine Tools Agency Pvt. Ltd. - Production Robots.txt
User-agent: *
Allow: /
Allow: /new/dalalmachine/
Allow: /uploads/
Allow: /manifest.json
Allow: /api/products/*/spec-sheet
Disallow: /admin
Disallow: /admin/
Disallow: /superadmin
Disallow: /superadmin/
Disallow: /dev
Disallow: /dev/
Disallow: /api/
Disallow: /portal-gate
Disallow: /portal-exit

# AI Crawlers & LLM Search Engine Access (GEO/AEO Indexing)
User-agent: GPTBot
Allow: /
Allow: /new/dalalmachine/

User-agent: ClaudeBot
Allow: /
Allow: /new/dalalmachine/

User-agent: PerplexityBot
Allow: /
Allow: /new/dalalmachine/

User-agent: Google-Extended
Allow: /

Sitemap: ${SITE_URL}/sitemap.xml
`;

  res.setHeader('Content-Type', 'text/plain; charset=utf-8');
  res.setHeader('Cache-Control', 'public, max-age=86400');
  return res.send(robots);
});

function escapeXml(unsafe) {
  if (!unsafe) return '';
  return String(unsafe).replace(/[<>&'"]/g, c => {
    switch (c) {
      case '<': return '&lt;';
      case '>': return '&gt;';
      case '&': return '&amp;';
      case '\'': return '&apos;';
      case '"': return '&quot;';
      default: return c;
    }
  });
}

module.exports = router;

