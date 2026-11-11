const express = require('express');
const router = express.Router();
const db = require('../db');
const realtime = require('../realtime');
const { requireAdmin, requireSuperAdmin } = require('../middleware/auth');

// GET /api/consignments (Admin & Superadmin view active High-Seas consignments)
router.get('/', requireAdmin, (req, res) => {
  const consignments = db.getConsignments();
  res.json({
    success: true,
    count: consignments.length,
    consignments
  });
});

// GET /api/consignments/:id
router.get('/:id', requireAdmin, (req, res) => {
  const csg = db.getConsignmentById(req.params.id);
  if (!csg) {
    return res.status(404).json({ success: false, message: 'Consignment not found.' });
  }
  res.json({ success: true, consignment: csg });
});

// POST /api/consignments (Superadmin Only - Create New Import Shipment)
router.post('/', requireSuperAdmin, (req, res) => {
  const { title, originPort, destinationPort, vesselName, containerNumbers, billOfLading, status, eta, totalMachines, valueInr } = req.body;
  if (!title || !originPort) {
    return res.status(400).json({ success: false, message: 'Shipment title and origin port are required.' });
  }

  try {
    const created = db.createConsignment(req.body, req.user);
    res.status(201).json({
      success: true,
      message: `High-Seas shipment ${created.title} created successfully.`,
      consignment: created
    });
  } catch (err) {
    res.status(500).json({ success: false, message: err.message });
  }
});

// PATCH /api/consignments/:id (Superadmin Only - Update Logistics Progress)
router.patch('/:id', requireSuperAdmin, (req, res) => {
  const updated = db.updateConsignment(req.params.id, req.body, req.user);
  if (!updated) {
    return res.status(404).json({ success: false, message: 'Consignment not found.' });
  }

  res.json({
    success: true,
    message: `Consignment status updated to ${updated.status}.`,
    consignment: updated
  });
});

// DELETE /api/consignments/:id (Superadmin Only)
router.delete('/:id', requireSuperAdmin, (req, res) => {
  const success = db.deleteConsignment(req.params.id, req.user);
  if (!success) {
    return res.status(404).json({ success: false, message: 'Consignment not found.' });
  }

  res.json({ success: true, message: 'Consignment deleted successfully.' });
});

module.exports = router;
