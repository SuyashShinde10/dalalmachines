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

// GET /api/inquiries/export/csv (1-Click CSV/Excel Download for Laptop Storage)
router.get('/export/csv', requireAdmin, (req, res) => {
  try {
    const inquiries = db.getInquiries() || [];

    // Helper to escape CSV values
    const escapeCsv = (val) => {
      if (val === null || val === undefined) return '""';
      const str = String(val).replace(/"/g, '""');
      return `"${str}"`;
    };

    const headers = [
      'Inquiry ID',
      'Date & Time',
      'Buyer Name',
      'Company Name',
      'Phone Number',
      'Email Address',
      'Machine Requested',
      'Message / Requirement',
      'Lead Status'
    ];

    let csvContent = '\uFEFF' + headers.join(',') + '\r\n';

    inquiries.forEach(inq => {
      const row = [
        escapeCsv(inq.id || ''),
        escapeCsv(inq.createdAt ? new Date(inq.createdAt).toLocaleString('en-IN', { timeZone: 'Asia/Kolkata' }) : ''),
        escapeCsv(inq.name || ''),
        escapeCsv(inq.company || 'N/A'),
        escapeCsv(inq.phone || 'N/A'),
        escapeCsv(inq.email || 'N/A'),
        escapeCsv(inq.machineName || inq.machineId || 'General Inquiry'),
        escapeCsv((inq.message || '').replace(/[\r\n]+/g, ' ')),
        escapeCsv((inq.status || 'new').toUpperCase())
      ];
      csvContent += row.join(',') + '\r\n';
    });

    const dateStr = new Date().toISOString().split('T')[0];
    res.setHeader('Content-Type', 'text/csv; charset=utf-8');
    res.setHeader('Content-Disposition', `attachment; filename="dalal_leads_export_${dateStr}.csv"`);
    return res.send(csvContent);
  } catch (err) {
    console.error('[CSV Export Error]:', err);
    res.status(500).json({ success: false, message: 'Failed to export CSV: ' + err.message });
  }
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
