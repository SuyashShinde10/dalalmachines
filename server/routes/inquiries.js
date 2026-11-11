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

// GET /api/inquiries/pipeline-metrics (Executive Pipeline Telemetry)
router.get('/pipeline-metrics', requireAdmin, (req, res) => {
  try {
    const metrics = db.getExecutivePipelineMetrics();
    res.json({ success: true, metrics });
  } catch (err) {
    res.status(500).json({ success: false, message: err.message });
  }
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
  const validStages = ['new', 'contacted', 'quoted', 'closed', 'power_trial_requested', 'quotation_sent', 'under_negotiation', 'deal_closed', 'deal_lost'];
  if (!validStages.includes(status)) {
    return res.status(400).json({ success: false, message: 'Invalid status value.' });
  }

  const updated = db.updateInquiryStatus(req.params.id, status, req.user);
  if (!updated) {
    return res.status(404).json({ success: false, message: 'Inquiry not found.' });
  }

  realtime.broadcastInquiryStatusChanged({ id: updated.id, status: updated.status, updatedBy: req.user.username });
  res.json({ success: true, message: 'Inquiry status updated.', inquiry: updated });
});

// PATCH /api/inquiries/:id/pipeline (Executive Pipeline Stage & Valuation)
router.patch('/:id/pipeline', requireAdmin, (req, res) => {
  const { pipelineStage, estimatedValue, notes, inspectionVideoLinks, isVipDeal } = req.body;
  const updated = db.updateInquiryPipeline(req.params.id, {
    pipelineStage,
    estimatedValue,
    notes,
    inspectionVideoLinks,
    isVipDeal
  }, req.user);

  if (!updated) {
    return res.status(404).json({ success: false, message: 'Inquiry not found.' });
  }

  realtime.broadcastInquiryStatusChanged({ id: updated.id, status: updated.pipelineStage, updatedBy: req.user.username });
  res.json({ success: true, message: 'Pipeline stage & valuation updated.', inquiry: updated });
});

// PATCH /api/inquiries/:id/assign (Staff Lead Assignment & SLA Tracker)
router.patch('/:id/assign', requireAdmin, (req, res) => {
  const { staffId, staffName } = req.body;
  if (!staffId || !staffName) {
    return res.status(400).json({ success: false, message: 'Please provide staffId and staffName.' });
  }

  const updated = db.assignInquiry(req.params.id, staffId, staffName, req.user);
  if (!updated) {
    return res.status(404).json({ success: false, message: 'Inquiry not found.' });
  }

  res.json({ success: true, message: `Lead successfully assigned to ${staffName}.`, inquiry: updated });
});

// POST /api/inquiries/:id/generate-quotation (1-Click WhatsApp & Formal Commercial Quote Generator)
router.post('/:id/generate-quotation', requireAdmin, (req, res) => {
  const inq = db.getInquiries().find(i => i.id === req.params.id);
  if (!inq) {
    return res.status(404).json({ success: false, message: 'Inquiry not found.' });
  }

  const machine = inq.machineId ? db.getProductById(inq.machineId) : null;
  const quotePrice = req.body.quotedPrice || inq.estimatedValue || (machine ? machine.targetPrice : 3500000);
  const gstRate = 18;
  const quotedPriceNum = parseFloat(quotePrice) || 3500000;
  const gstAmount = Math.round(quotedPriceNum * (gstRate / 100));
  const totalAmount = quotedPriceNum + gstAmount;

  const quoteNumber = 'DMTA-QT-' + new Date().getFullYear() + '-' + inq.id.replace('inq_', '').toUpperCase();
  const dateFormatted = new Date().toLocaleDateString('en-IN', { day: '2-digit', month: 'short', year: 'numeric' });

  // Clean WhatsApp Pre-Filled Commercial Message Text
  const waText = [
    `*DALAL MACHINE TOOLS AGENCY PVT. LTD.*`,
    `_Official Commercial Quotation Ref: ${quoteNumber}_`,
    ``,
    `*Dear ${inq.name || 'Valued Client'} (${inq.company || 'Enterprise'}),*`,
    `Thank you for consulting Dalal Machine Tools Agency Pvt. Ltd. (Est. 1985).`,
    ``,
    `*Quotation Details:*`,
    `• *Machinery:* ${machine ? machine.name : inq.machineName || 'Industrial Heavy Machine'}`,
    `• *Make / Model:* ${machine ? (machine.make + ' / ' + machine.model) : 'As Inspected'}`,
    `• *Tonnage / Capacity:* ${machine && machine.tonnage ? machine.tonnage + ' Ton' : 'Standard'}`,
    `• *Condition:* Operational / Ready for Power Trial`,
    `• *Location:* In Stock Yard (Pune / Bhiwandi)`,
    ``,
    `*Commercial Terms:*`,
    `• *Ex-Works Basic Price:* ₹${quotedPriceNum.toLocaleString('en-IN')}`,
    `• *GST (@18%):* ₹${gstAmount.toLocaleString('en-IN')}`,
    `• *Total Value:* ₹${totalAmount.toLocaleString('en-IN')}`,
    `• *Payment Terms:* 30% Advance, 70% Before Dispatch on Live Power Trial Inspection`,
    ``,
    `*Live Power Trial Video:*`,
    machine && machine.inspectionVideos && machine.inspectionVideos.length > 0
      ? machine.inspectionVideos[0].url
      : 'https://dalalmachines.com/inspection-vault/' + (machine ? machine.id : 'DMTA'),
    ``,
    `For technical clarifications, consult Managing Director Mr. Vinit Dalal: +91 9821232131`,
    `Commerce Centre, Tardeo, Mumbai - 400034`
  ].join('\n');

  const cleanPhone = (inq.phone || '').replace(/[^0-9]/g, '');
  const waUrl = cleanPhone ? `https://api.whatsapp.com/send?phone=${cleanPhone}&text=${encodeURIComponent(waText)}` : null;

  // Update inquiry to 'quotation_sent'
  db.updateInquiryPipeline(inq.id, { pipelineStage: 'quotation_sent', estimatedValue: quotedPriceNum }, req.user);

  res.json({
    success: true,
    quoteNumber,
    dateFormatted,
    client: { name: inq.name, company: inq.company, phone: inq.phone, email: inq.email, city: inq.city },
    machine: machine ? { id: machine.id, name: machine.name, make: machine.make, model: machine.model, tonnage: machine.tonnage } : { name: inq.machineName },
    commercials: {
      basicPrice: quotedPriceNum,
      gstRate,
      gstAmount,
      totalAmount
    },
    whatsAppText: waText,
    whatsAppUrl: waUrl
  });
});

module.exports = router;
