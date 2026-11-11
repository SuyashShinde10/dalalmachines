const express = require('express');
const router = express.Router();
const path = require('path');
const jwt = require('jsonwebtoken');
const config = require('../config');
const db = require('../db');
const realtime = require('../realtime');
const cacheEngine = require('../performance/cacheEngine');
const { requireAdmin, requireSuperAdmin } = require('../middleware/auth');
const upload = require('../middleware/upload');
const { generateSpecSheetHtml } = require('../services/pdfGenerator');

function isSuperAdminRequest(req) {
  let token = null;
  const authHeader = req.headers['authorization'];
  if (authHeader && authHeader.startsWith('Bearer ')) {
    token = authHeader.split(' ')[1];
  } else if (req.cookies && req.cookies.superadmin_token) {
    token = req.cookies.superadmin_token;
  }
  if (!token) return false;
  try {
    const decoded = jwt.verify(token, config.JWT_SECRET);
    return decoded && decoded.role === 'superadmin';
  } catch (e) {
    return false;
  }
}

function sanitizeProductForViewer(product, isSuperAdmin) {
  if (!product) return null;
  if (isSuperAdmin) {
    const pCost = product.procurementCost || 0;
    const fPrice = product.floorPrice || 0;
    const marginPercent = pCost > 0 ? Math.round(((fPrice - pCost) / pCost) * 100) : 25;
    return {
      ...product,
      marginPercent
    };
  }
  // Strip confidential MD margin & procurement cost from public visitors & staff admins
  const { procurementCost, floorPrice, ...safeProduct } = product;
  return safeProduct;
}

// GET /api/products (Public or Admin with In-Memory Micro-Cache)
router.get('/', cacheEngine.middleware(30), (req, res) => {
  const { section, category, location, query, status, all } = req.query;
  const isSuperAdmin = isSuperAdminRequest(req);
  
  const filters = { section, category, location, query };
  if (status) {
    filters.status = status;
  } else if (all !== 'true') {
    // By default public only sees active machines
    filters.status = 'active';
  }

  const list = db.getProducts(filters).map(p => sanitizeProductForViewer(p, isSuperAdmin));
  res.json({
    success: true,
    count: list.length,
    products: list
  });
});

// GET /api/products/categories
router.get('/categories', cacheEngine.middleware(60), (req, res) => {
  res.json({
    success: true,
    categories: db.getCategories()
  });
});

// GET /api/products/:id
router.get('/:id', cacheEngine.middleware(30), (req, res) => {
  const product = db.getProductById(req.params.id);
  if (!product) {
    return res.status(404).json({ success: false, message: 'Machine not found.' });
  }
  const isSuperAdmin = isSuperAdminRequest(req);
  res.json({ success: true, product: sanitizeProductForViewer(product, isSuperAdmin) });
});

// GET /api/products/:id/spec-sheet (1-Click Printable PDF Spec Sheet & Official Quotation)
router.get('/:id/spec-sheet', (req, res) => {
  const product = db.getProductById(req.params.id);
  if (!product) {
    return res.status(404).send('Machine listing not found.');
  }
  const buyerName = req.query.buyer || req.query.client || 'Valued Industrial Client';
  const price = req.query.price || product.priceText || 'Price On Request';
  const quoteNo = req.query.quoteNo;

  const html = generateSpecSheetHtml(product, { buyerName, price, quoteNo });
  res.setHeader('Content-Type', 'text/html; charset=utf-8');
  res.send(html);
});

// POST /api/products/upload (Image / PDF Upload)
router.post('/upload', requireAdmin, upload.single('file'), (req, res) => {
  if (!req.file) {
    return res.status(400).json({ success: false, message: 'No file uploaded.' });
  }
  const fileUrl = `/uploads/${req.file.filename}`;
  res.json({
    success: true,
    message: 'File uploaded successfully.',
    url: fileUrl,
    filename: req.file.filename,
    mimetype: req.file.mimetype,
    size: req.file.size
  });
});

// POST /api/products (Create Standard or Custom Machine)
router.post('/', requireAdmin, (req, res) => {
  const { name, section, category } = req.body;
  if (!name || !section || !category) {
    return res.status(400).json({ 
      success: false, 
      message: 'Machine Name, Section (forming/cutting), and Category are required.' 
    });
  }

  try {
    const created = db.createProduct(req.body, req.user);
    realtime.broadcastCatalogUpdate({ action: 'CREATED', product: created });
    res.status(201).json({
      success: true,
      message: `${created.isCustom ? 'Custom' : 'Standard'} machine created successfully.`,
      product: created
    });
  } catch (err) {
    res.status(500).json({ success: false, message: err.message });
  }
});

// PUT /api/products/:id (Update Machine)
router.put('/:id', requireAdmin, (req, res) => {
  const existing = db.getProductById(req.params.id);
  if (!existing) {
    return res.status(404).json({ success: false, message: 'Machine not found.' });
  }

  try {
    const updated = db.updateProduct(req.params.id, req.body, req.user);
    realtime.broadcastCatalogUpdate({ action: 'UPDATED', product: updated });
    res.json({
      success: true,
      message: 'Machine details updated successfully.',
      product: updated
    });
  } catch (err) {
    res.status(500).json({ success: false, message: err.message });
  }
});

// DELETE /api/products/:id (Delete Machine)
router.delete('/:id', requireAdmin, (req, res) => {
  const existing = db.getProductById(req.params.id);
  if (!existing) {
    return res.status(404).json({ success: false, message: 'Machine not found.' });
  }

  const success = db.deleteProduct(req.params.id, req.user);
  if (success) {
    realtime.broadcastCatalogUpdate({ action: 'DELETED', product: existing });
    res.json({ success: true, message: `Machine ${existing.name} (${existing.id}) deleted successfully.` });
  } else {
    res.status(500).json({ success: false, message: 'Failed to delete machine.' });
  }
});

// PATCH /api/products/:id/confidential-pricing (Superadmin Only - MD Confidential Margin & Floor Price)
router.patch('/:id/confidential-pricing', requireSuperAdmin, (req, res) => {
  const existing = db.getProductById(req.params.id);
  if (!existing) {
    return res.status(404).json({ success: false, message: 'Machine not found.' });
  }

  const { procurementCost, floorPrice, targetPrice, inspectionVideos } = req.body;
  const updated = db.updateConfidentialPricing(req.params.id, {
    procurementCost,
    floorPrice,
    targetPrice,
    inspectionVideos
  }, req.user);

  cacheEngine.invalidate('/api/products');
  res.json({
    success: true,
    message: `Confidential floor price (₹${updated.floorPrice}) & procurement margins updated for ${updated.name}`,
    product: sanitizeProductForViewer(updated, true)
  });
});

// GET /api/products/:id/inspection-vault (Private Live Power Trial Inspection Videos)
router.get('/:id/inspection-vault', requireAdmin, (req, res) => {
  const product = db.getProductById(req.params.id);
  if (!product) {
    return res.status(404).json({ success: false, message: 'Machine not found.' });
  }

  res.json({
    success: true,
    machineId: product.id,
    machineName: product.name,
    inspectionVideos: product.inspectionVideos || []
  });
});

module.exports = router;
