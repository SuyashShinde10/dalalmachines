const express = require('express');
const router = express.Router();
const path = require('path');
const db = require('../db');
const realtime = require('../realtime');
const cacheEngine = require('../performance/cacheEngine');
const { requireAdmin } = require('../middleware/auth');
const upload = require('../middleware/upload');
const { generateSpecSheetHtml } = require('../services/pdfGenerator');

// GET /api/products (Public or Admin with In-Memory Micro-Cache)
router.get('/', cacheEngine.middleware(30), (req, res) => {
  const { section, category, location, query, status, all } = req.query;
  
  const filters = { section, category, location, query };
  if (status) {
    filters.status = status;
  } else if (all !== 'true') {
    // By default public only sees active machines
    filters.status = 'active';
  }

  const list = db.getProducts(filters);
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
  res.json({ success: true, product });
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

module.exports = router;
