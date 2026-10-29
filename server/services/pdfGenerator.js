// Dalal Machine Tools Agency Pvt. Ltd.
// Professional Industrial Machinery Specification Sheet & Quotation Engine
// Version: 1.0 | Print-Ready Vector Typography | A4 Precision Standard

const db = require('../db');

function generateSpecSheetHtml(machine, quotationOptions = {}) {
  const specs = machine.specs || {};
  const isCustom = Boolean(machine.isCustom);
  const dateStr = new Date().toLocaleDateString('en-IN', {
    day: '2-digit',
    month: 'short',
    year: 'numeric'
  });

  const quoteRefNo = quotationOptions.quoteNo || `DMTA-QT-${new Date().getFullYear()}-${machine.id || 'GEN'}`;
  const buyerName = quotationOptions.buyerName || 'Valued Industrial Client';
  const buyerCompany = quotationOptions.buyerCompany || 'Procurement & Engineering Division';
  const customPrice = quotationOptions.price || machine.priceText || 'Price On Request (CIF / Ex-Works)';

  // Build spec rows
  const specRowsHtml = Object.entries(specs).map(([key, val]) => `
    <tr>
      <td class="spec-label">${escapeHtml(key)}</td>
      <td class="spec-value"><strong>${escapeHtml(String(val))}</strong></td>
    </tr>
  `).join('');

  return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Specification Sheet & Quotation - ${escapeHtml(machine.name)} | Dalal Machine Tools</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;600&display=swap" rel="stylesheet">
  <style>
    @page {
      size: A4 portrait;
      margin: 12mm 14mm 14mm 14mm;
    }
    *, *::before, *::after {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }
    body {
      font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
      color: #0f172a;
      background: #f8fafc;
      padding: 24px 20px;
      line-height: 1.5;
      font-size: 13px;
    }
    .print-controls-bar {
      max-width: 800px;
      margin: 0 auto 16px auto;
      background: #0f172a;
      color: #ffffff;
      padding: 12px 20px;
      border-radius: 12px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      box-shadow: 0 10px 25px -5px rgba(15, 23, 42, 0.3);
    }
    .print-btn {
      background: #f89d13;
      color: #000000;
      border: none;
      padding: 8px 18px;
      border-radius: 8px;
      font-weight: 700;
      font-size: 13px;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 8px;
      transition: background 0.2s;
    }
    .print-btn:hover { background: #e08b0b; }
    
    .doc-page {
      max-width: 800px;
      margin: 0 auto;
      background: #ffffff;
      border: 1px solid #e2e8f0;
      border-radius: 14px;
      padding: 36px 40px;
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
      position: relative;
    }

    /* Header */
    .doc-header {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      border-bottom: 2px solid #0f172a;
      padding-bottom: 18px;
      margin-bottom: 20px;
    }
    .doc-brand h1 {
      font-size: 21px;
      font-weight: 800;
      color: #0f172a;
      letter-spacing: -0.4px;
      text-transform: uppercase;
    }
    .doc-brand p {
      font-size: 11.5px;
      color: #64748b;
      margin-top: 3px;
      font-weight: 500;
    }
    .partner-pill {
      display: inline-block;
      background: #fef3c7;
      border: 1px solid #fde68a;
      color: #92400e;
      font-size: 10px;
      font-weight: 700;
      padding: 3px 8px;
      border-radius: 9999px;
      margin-top: 6px;
      text-transform: uppercase;
    }
    .doc-ref-box {
      text-align: right;
      font-size: 11.5px;
    }
    .doc-ref-no {
      font-family: 'JetBrains Mono', monospace;
      font-weight: 700;
      color: #0f172a;
      font-size: 13px;
    }
    .doc-date { color: #64748b; margin-top: 2px; }

    /* Machine Title Banner */
    .machine-hero {
      background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
      border: 1px solid #cbd5e1;
      border-radius: 12px;
      padding: 16px 20px;
      margin-bottom: 22px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .machine-hero-title {
      font-size: 18px;
      font-weight: 800;
      color: #0f172a;
      line-height: 1.3;
    }
    .machine-hero-meta {
      font-size: 12px;
      color: #475569;
      margin-top: 4px;
    }
    .status-badge {
      background: #ecfdf5;
      color: #065f46;
      border: 1px solid #a7f3d0;
      padding: 6px 14px;
      border-radius: 9999px;
      font-size: 11px;
      font-weight: 700;
      text-transform: uppercase;
      white-space: nowrap;
    }

    /* Two-Column Grid: Image & Key Metrics */
    .grid-2col {
      display: grid;
      grid-template-columns: 1.1fr 1fr;
      gap: 24px;
      margin-bottom: 22px;
    }
    .machine-photo-frame {
      border: 1px solid #e2e8f0;
      border-radius: 10px;
      overflow: hidden;
      background: #0f172a;
      height: 230px;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    .machine-photo-frame img {
      width: 100%;
      height: 100%;
      object-fit: cover;
    }
    
    .quick-specs-table {
      width: 100%;
      border-collapse: collapse;
      font-size: 12px;
    }
    .quick-specs-table th {
      text-align: left;
      padding: 7px 10px;
      background: #f1f5f9;
      border-bottom: 1px solid #cbd5e1;
      color: #475569;
      font-size: 11px;
      text-transform: uppercase;
    }
    .quick-specs-table td {
      padding: 7px 10px;
      border-bottom: 1px solid #f1f5f9;
    }
    .quick-specs-table tr:last-child td { border-bottom: none; }

    /* Technical Specifications Table */
    .section-heading {
      font-size: 13.5px;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      color: #0f172a;
      border-bottom: 1.5px solid #0f172a;
      padding-bottom: 6px;
      margin-bottom: 10px;
      display: flex;
      justify-content: space-between;
    }
    .specs-table {
      width: 100%;
      border-collapse: collapse;
      margin-bottom: 22px;
      font-size: 12px;
    }
    .specs-table td {
      padding: 8px 12px;
      border: 1px solid #e2e8f0;
    }
    .spec-label {
      background: #f8fafc;
      width: 38%;
      color: #475569;
      font-weight: 600;
    }
    .spec-value {
      color: #0f172a;
    }

    /* Commercial Quotation Box */
    .quote-box {
      background: #fefce8;
      border: 1.5px solid #fef08a;
      border-radius: 10px;
      padding: 14px 18px;
      margin-bottom: 20px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .quote-label {
      font-size: 11.5px;
      color: #854d0e;
      font-weight: 700;
      text-transform: uppercase;
    }
    .quote-val {
      font-size: 17px;
      font-weight: 800;
      color: #713f12;
      margin-top: 2px;
    }
    .quote-terms {
      text-align: right;
      font-size: 11px;
      color: #a16207;
    }

    /* Sign-Off Footer */
    .doc-footer {
      border-top: 1px solid #cbd5e1;
      padding-top: 16px;
      margin-top: 24px;
      display: flex;
      justify-content: space-between;
      align-items: flex-end;
      font-size: 11px;
      color: #64748b;
    }
    .footer-address {
      line-height: 1.6;
    }
    .stamp-box {
      text-align: right;
    }
    .signature-title {
      font-weight: 700;
      color: #0f172a;
      font-size: 12px;
    }
    .stamp-badge {
      display: inline-block;
      margin-top: 6px;
      border: 1.5px dashed #059669;
      color: #059669;
      font-weight: 800;
      font-size: 10px;
      padding: 4px 12px;
      border-radius: 6px;
      text-transform: uppercase;
    }

    @media print {
      body {
        background: #ffffff;
        padding: 0;
      }
      .print-controls-bar {
        display: none !important;
      }
      .doc-page {
        border: none;
        box-shadow: none;
        padding: 0;
        border-radius: 0;
      }
    }
  </style>
</head>
<body>

  <!-- Screen-Only Action Bar -->
  <div class="print-controls-bar">
    <div>
      <strong>Industrial Machinery Specification & Official Quotation Sheet</strong>
      <div style="font-size:11px; color:#94a3b8; margin-top:2px;">Dalal Machine Tools Agency Pvt. Ltd. &bull; Ref: ${escapeHtml(quoteRefNo)}</div>
    </div>
    <div style="display:flex; gap:10px;">
      <button type="button" class="print-btn" onclick="window.print();">
        🖨️ Print / Save as PDF
      </button>
      <button type="button" style="background:#334155; color:#fff; border:none; padding:8px 14px; border-radius:8px; cursor:pointer;" onclick="window.close();">
        Close
      </button>
    </div>
  </div>

  <!-- Document Page (A4 Form Factor) -->
  <div class="doc-page">

    <!-- Header Letterhead -->
    <header class="doc-header">
      <div class="doc-brand">
        <h1>DALAL MACHINE TOOLS</h1>
        <p>Heavy Metal Forming & Metal Cutting Machinery Import Specialist</p>
        <span class="partner-pill">Technical Partner: OMPI India LLP (Clutch & Brake Systems)</span>
      </div>
      <div class="doc-ref-box">
        <div class="doc-ref-no">${escapeHtml(quoteRefNo)}</div>
        <div class="doc-date">Date: ${escapeHtml(dateStr)}</div>
        <div style="color:#059669; font-weight:700; margin-top:4px;">In Stock Pune Yard</div>
      </div>
    </header>

    <!-- Machine Overview Banner -->
    <div class="machine-hero">
      <div>
        <div class="machine-hero-title">${escapeHtml(machine.name)}</div>
        <div class="machine-hero-meta">
          Machine ID: <strong>${escapeHtml(machine.id || 'N/A')}</strong> &bull; 
          Make: <strong>${escapeHtml(machine.make || 'N/A')}</strong> &bull; 
          Year: <strong>${escapeHtml(String(machine.year || 'Operational'))}</strong>
        </div>
      </div>
      <div class="status-badge">${escapeHtml(machine.condition || 'Operational Ready')}</div>
    </div>

    <!-- Image + Quick Technical Parameters -->
    <div class="grid-2col">
      <div class="machine-photo-frame">
        <img src="/${escapeHtml(machine.image || 'images/dalal/cframe_press_pune.jpg')}" alt="${escapeHtml(machine.name)}" onerror="this.src='/images/dalal/cframe_press_pune.jpg'">
      </div>
      <div>
        <table class="quick-specs-table">
          <thead>
            <tr><th colspan="2">Primary Engineering Parameters</th></tr>
          </thead>
          <tbody>
            <tr><td>Category</td><td><strong>${escapeHtml(machine.categoryName || machine.category || 'Machinery')}</strong></td></tr>
            <tr><td>Section</td><td><strong>${escapeHtml((machine.section || 'forming').toUpperCase())}</strong></td></tr>
            <tr><td>Rated Tonnage</td><td><strong>${escapeHtml(machine.tonnage ? machine.tonnage + ' Ton' : 'Standard')}</strong></td></tr>
            <tr><td>Staging Location</td><td><strong>${escapeHtml(machine.location || 'Pune Warehouse, India')}</strong></td></tr>
            <tr><td>Power Trial</td><td><strong style="color:#059669;">Available Under Live Power</strong></td></tr>
            <tr><td>Clutch System</td><td><strong>${escapeHtml(isCustom ? 'Custom OMPI Italy High Torque' : 'Standard Mechanical/Pneumatic')}</strong></td></tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Detailed Technical Specifications -->
    <div class="section-heading">
      <span>Comprehensive Technical Specifications</span>
      <span style="font-size:11px; font-weight:600; color:#64748b;">Factory Audited</span>
    </div>
    <table class="specs-table">
      <tbody>
        ${specRowsHtml.length > 0 ? specRowsHtml : `
          <tr><td class="spec-label">Machine Configuration</td><td class="spec-value">Heavy-duty industrial rigid frame design with precision die guidance.</td></tr>
          <tr><td class="spec-label">Lubrication System</td><td class="spec-value">Centralized motorized automatic pressure lubrication.</td></tr>
          <tr><td class="spec-label">Inspection Status</td><td class="spec-value">Physical geometric alignment and load-bearing test completed by Dalal technical staff.</td></tr>
        `}
      </tbody>
    </table>

    <!-- Commercial Quotation Terms -->
    <div class="quote-box">
      <div>
        <div class="quote-label">Indicative Commercial Offer (${escapeHtml(buyerName)})</div>
        <div class="quote-val">${escapeHtml(customPrice)}</div>
      </div>
      <div class="quote-terms">
        <div><strong>Delivery:</strong> Immediate Ex-Stock / High Seas Transfer</div>
        <div><strong>Inspection:</strong> Power Trial at Pune Yard by Appointment</div>
        <div><strong>Payment:</strong> Letter of Credit (LC) / Wire Transfer</div>
      </div>
    </div>

    <!-- Official Stamp & Contact Footer -->
    <footer class="doc-footer">
      <div class="footer-address">
        <strong>Dalal Machine Tools Agency Pvt. Ltd.</strong><br>
        Registered Office: Commerce Centre, Tardeo, Mumbai - 400034, India.<br>
        Pune Facility: In Stock Machinery Yard, Chakan Industrial Corridor, Pune.<br>
        Direct Phone: +91 9821232131 &bull; Direct Email: dalalmachine@gmail.com
      </div>
      <div class="stamp-box">
        <div class="signature-title">Mr. Vinit Dalal</div>
        <div style="font-size:11px; color:#64748b;">Managing Director</div>
        <div class="stamp-badge">Authorized Industrial Quotation</div>
      </div>
    </footer>

  </div>

</body>
</html>`;
}

function escapeHtml(str) {
  if (str === null || str === undefined) return '';
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}

module.exports = {
  generateSpecSheetHtml
};
