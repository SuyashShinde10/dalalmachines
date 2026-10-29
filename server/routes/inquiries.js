const express = require('express');
const router = express.Router();
const db = require('../db');
const realtime = require('../realtime');
const { requireAdmin } = require('../middleware/auth');
const { dispatchInquiryAlerts } = require('../notifications/alertEngine');

// POST /api/inquiries (Public from Contact & PDP forms)
router.post('/', async (req, res) => {
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

  // REAL-TIME BROADCAST: Notify operations staff immediately (Zero PII to Developer)
  realtime.broadcastInquiry({
    id: inquiry.id,
    machineName: inquiry.machineName,
    company: inquiry.company,
    timestamp: inquiry.createdAt
  });

  // DISPATCH ALERTS: Instant WhatsApp lead payload & staff notification
  const alertInfo = await dispatchInquiryAlerts(inquiry);

  res.status(201).json({
    success: true,
    message: 'Thank you! Your quotation request has been submitted to Dalal Machine Tools.',
    inquiryId: inquiry.id,
    whatsappContactUrl: alertInfo.whatsappUrl
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

  realtime.broadcastInquiryStatusChanged({ id: updated.id, status: updated.status, updatedBy: req.user.username });
  res.json({ success: true, message: 'Inquiry status updated.', inquiry: updated });
});

module.exports = router;
