const express = require('express');
const router = express.Router();
const db = require('../db');
const { requireAdmin } = require('../middleware/auth');

// POST /api/inquiries (Public from Contact & PDP forms)
router.post('/', (req, res) => {
  const { name, email, phone, company, machineId, machineName, message } = req.body;
  if (!name || (!email && !phone)) {
    return res.status(400).json({ success: false, message: 'Please provide your name and contact phone or email.' });
  }

  const inquiry = db.createInquiry({
    name,
    email,
    phone,
    company,
    machineId,
    machineName,
    message
  });

  res.status(201).json({
    success: true,
    message: 'Thank you! Your quotation request has been submitted to Dalal Machine Tools.',
    inquiryId: inquiry.id
  });
});

// GET /api/inquiries (Admin & Super Admin)
router.get('/', requireAdmin, (req, res) => {
  const list = db.getInquiries();
  res.json({ success: true, count: list.length, inquiries: list });
});

// PUT /api/inquiries/:id (Update Status)
router.put('/:id', requireAdmin, (req, res) => {
  const { status } = req.body;
  if (!['new', 'contacted', 'quoted', 'closed'].includes(status)) {
    return res.status(400).json({ success: false, message: 'Invalid status value.' });
  }

  const updated = db.updateInquiryStatus(req.params.id, status, req.user);
  if (!updated) {
    return res.status(404).json({ success: false, message: 'Inquiry not found.' });
  }

  res.json({ success: true, message: 'Inquiry status updated.', inquiry: updated });
});

module.exports = router;
