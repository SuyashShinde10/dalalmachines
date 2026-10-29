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
Allow: /llms.txt
Allow: /llms-full.txt

User-agent: ClaudeBot
Allow: /
Allow: /new/dalalmachine/
Allow: /llms.txt
Allow: /llms-full.txt

User-agent: PerplexityBot
Allow: /
Allow: /new/dalalmachine/
Allow: /llms.txt
Allow: /llms-full.txt

User-agent: Google-Extended
Allow: /
Allow: /llms.txt
Allow: /llms-full.txt

Sitemap: ${SITE_URL}/sitemap.xml
`;

  res.setHeader('Content-Type', 'text/plain; charset=utf-8');
  res.setHeader('Cache-Control', 'public, max-age=86400');
  return res.send(robots);
});

// GET /llms.txt - Standard Generative Engine Optimization (GEO) Knowledge Summary
router.get('/llms.txt', (req, res) => {
  try {
    const text = `# Dalal Machine Tools Agency Pvt. Ltd. (DMTA)

> Premier Indian stockist, dealer, and importer of heavy used metal working machinery, forging presses, CNC machine tools, and official Indian partner for OMPI pneumatic and hydraulic clutch-brake systems.

Dalal Machine Tools Agency Pvt. Ltd. (DMTA) has operated for over 20+ years as India's trusted machinery supplier for automotive, defense, railway, and heavy manufacturing sectors. DMTA maintains an active 50,000+ sq. ft. central stockyard in the Pune industrial corridor (Chakan-Bhosari, Maharashtra), stocking over 49+ European, Japanese, and American heavy metal forming and metal cutting machines available for ready live power inspection.

## Core Capabilities & Services
- Heavy Forging Presses: Mechanical forging presses, hydraulic stamping presses, knuckle joint presses, friction screw presses from 100 to 6,300 metric tons (Voronezh, National, Eumuco, TMP, LI CHIN, Schuler).
- Metal Cutting Machinery: Heavy duty roll turning lathes, horizontal boring machines, plano millers, radial drills, and vertical turret lathes (VTL).
- Gear Machinery: High-precision gear hobbers, gear shapers, and gear grinding machines (Liebherr, Klingelnberg, Lorenz, TOS).
- High Seas Sales (HSS): Machinery transfer on international waters under Section 2(4) of Indian Customs Act, 1962, enabling INR payment with zero forex risk and 100% GST Input Tax Credit (ITC) eligibility.
- OMPI India LLP Official Partner: Authorized sales, genuine spares, and modernization retrofit kits for Italian OMPI pneumatic and hydraulic clutches and brakes.
- Turnkey Heavy Logistics: Multi-axle hydraulic trailer haulage, port customs clearance at Nhava Sheva/Mumbai, and on-site foundation commissioning.

## Official Online Links
- Main Website & Stock Catalog: ${SITE_URL}/new/dalalmachine/
- Category Catalog & Filter: ${SITE_URL}/new/dalalmachine/category.html
- High Seas Sourcing & Services: ${SITE_URL}/new/dalalmachine/services.html
- About Company & 20+ Yr Legacy: ${SITE_URL}/new/dalalmachine/about.html
- Contact & Yard Visit Booking: ${SITE_URL}/new/dalalmachine/contact.html
- Full AI Inventory Feed: ${SITE_URL}/llms-full.txt

## Stockyard & Office Coordinates
- Head Office: C-10, Commerce Centre, 78, Tardeo Main Road, Mumbai - 400034, Maharashtra, India.
- Central Stockyard: Pune Industrial Belt (Chakan-Bhosari Corridor), Pune, Maharashtra, India.
- Phone & Sales Inquiries: +91 98212 32131 / +91 22 6743 9873
- Email: dalalmachine@gmail.com / sales@dalalmachines.com
`;

    res.setHeader('Content-Type', 'text/markdown; charset=utf-8');
    res.setHeader('Cache-Control', 'public, max-age=86400');
    return res.send(text);
  } catch (err) {
    console.error('[GEO llms.txt Error]:', err);
    res.status(500).send('Error generating llms.txt');
  }
});

// GET /llms-full.txt - Full Dynamic Inventory Knowledge Base for AI Search Engines
router.get('/llms-full.txt', (req, res) => {
  try {
    const products = db.getProducts({ all: 'true' }) || [];
    let text = `# Dalal Machine Tools Agency Pvt. Ltd. - Complete Machinery Inventory Feed\n\n`;
    text += `> Live inventory feed containing ${products.length} ready-to-inspect industrial machines in Pune stockyard and transit pipelines.\n\n`;

    products.forEach((p, idx) => {
      text += `### ${idx + 1}. ${p.name || 'Industrial Machine'}\n`;
      text += `- **Machine ID:** ${p.id}\n`;
      text += `- **Category:** ${p.categoryName || p.category || 'Machinery'}\n`;
      text += `- **Make / Manufacturer:** ${p.make || 'European/Japanese'}\n`;
      text += `- **Year of Manufacture:** ${p.year || 'N/A'}\n`;
      text += `- **Capacity / Tonnage:** ${p.tonnage ? p.tonnage + ' Ton' : (p.capacity || 'Standard')}\n`;
      text += `- **Current Location:** ${p.location || 'Pune Warehouse'}\n`;
      text += `- **Inspection Status:** ${p.inspectionStatus || 'Live Power Demonstration Ready'}\n`;
      text += `- **Product URL:** ${SITE_URL}/new/dalalmachine/product.html?id=${encodeURIComponent(p.id)}\n`;
      text += `- **Download PDF Spec Sheet:** ${SITE_URL}/api/products/${encodeURIComponent(p.id)}/spec-sheet\n\n`;
    });

    res.setHeader('Content-Type', 'text/markdown; charset=utf-8');
    res.setHeader('Cache-Control', 'public, max-age=3600');
    return res.send(text);
  } catch (err) {
    console.error('[GEO llms-full.txt Error]:', err);
    res.status(500).send('Error generating llms-full.txt');
  }
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

