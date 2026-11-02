import os

from build_manual_data import html_start, dalal_routes_data, ompi_modules_data

body_parts = [html_start]

# PART 1: DALAL MACHINE TOOLS AGENCY (24 ROUTES)
body_parts.append("""
<div class="system-banner">
  <h2>SYSTEM 1: DALAL MACHINE TOOLS AGENCY WEB PLATFORM</h2>
  <span>ALL 24 CUSTOMER &amp; OPERATIONS ROUTES</span>
</div>
""")

for i, (rid, title, path, persona, why, what, features) in enumerate(dalal_routes_data, 1):
    feat_rows = ""
    for fname, fdesc in features:
        feat_rows += f"<li><strong>{fname}:</strong> {fdesc}</li>"
    
    card_html = f"""
<div class="unit-card avoid-break">
  <div class="unit-header">
    <div>
      <span class="unit-id">{rid}</span>
      <span class="unit-title">{title}</span>
      <span class="persona-badge">{persona}</span>
    </div>
    <span class="unit-route">{path}</span>
  </div>
  <div class="unit-grid">
    <div class="unit-box why">
      <div class="unit-box-title why-title">&#9658; Why It Exists (Business Purpose &amp; Rationale)</div>
      <p>{why}</p>
    </div>
    <div class="unit-box">
      <div class="unit-box-title what-title">&#9658; What It Does (Operational Mechanics)</div>
      <p>{what}</p>
    </div>
  </div>
  <div class="unit-features">
    <div class="unit-features-title">Core Functional Components &amp; Technical Tools:</div>
    <ul>
      {feat_rows}
    </ul>
  </div>
</div>
"""
    body_parts.append(card_html)
    if i in [3, 7, 11, 15, 19, 23]:
        body_parts.append('<div class="page-break"></div>')

body_parts.append('<div class="page-break"></div>')

# PART 2: OMPI INDIA LLP ERP (33 MODULES)
body_parts.append("""
<div class="system-banner" style="background:#1e3a8a;">
  <h2>SYSTEM 2: OMPI INDIA LLP INDUSTRIAL OPERATIONS &amp; ERP SUITE</h2>
  <span>ALL 33 MODULAR ENGINES &amp; SUBSYSTEMS</span>
</div>
""")

for j, (mid, title, engine, persona, why, what, features) in enumerate(ompi_modules_data, 1):
    feat_rows = ""
    for fname, fdesc in features:
        feat_rows += f"<li><strong>{fname}:</strong> {fdesc}</li>"
    
    card_html = f"""
<div class="unit-card avoid-break">
  <div class="unit-header">
    <div>
      <span class="unit-id" style="background:#1e3a8a;">{mid}</span>
      <span class="unit-title">{title}</span>
      <span class="persona-badge" style="color:#065f46; background:#ecfdf5; border-color:#a7f3d0;">{engine}</span>
      <span class="persona-badge">{persona}</span>
    </div>
    <span class="unit-route">ERP System Subsystem</span>
  </div>
  <div class="unit-grid">
    <div class="unit-box why">
      <div class="unit-box-title why-title">&#9658; Why It Exists (Business Purpose &amp; Rationale)</div>
      <p>{why}</p>
    </div>
    <div class="unit-box">
      <div class="unit-box-title what-title">&#9658; What It Does (Operational Mechanics)</div>
      <p>{what}</p>
    </div>
  </div>
  <div class="unit-features">
    <div class="unit-features-title">Core Sub-Modules, Algorithms &amp; Automation Features:</div>
    <ul>
      {feat_rows}
    </ul>
  </div>
</div>
"""
    body_parts.append(card_html)
    if j in [3, 7, 11, 15, 19, 23, 27, 31]:
        body_parts.append('<div class="page-break"></div>')

# PART 3: INTER-CONNECTIVITY & SUMMARY MATRIX
body_parts.append("""
<div class="page-break"></div>
<div class="system-banner" style="background:#0f172a;">
  <h2>COMPLETE SYSTEM MATRIX &amp; LIFECYCLE HANDSHAKE</h2>
  <span>CROSS-SYSTEM REAL-TIME INTEGRATION</span>
</div>

<div class="unit-card avoid-break">
  <p style="font-size:8.8pt; color:#334155; line-height:1.55; margin-bottom:12px;">
    The table below establishes the operational handshake between <strong>Dalal Machine Tools Agency</strong> (the inbound capital equipment acquisition engine) and <strong>OMPI India LLP</strong> (the precision engineering, landed costing, and lifecycle spares engine):
  </p>
  <table style="width:100%; border-collapse:collapse; font-size:8.2pt; border:1px solid #cbd5e1;">
    <thead>
      <tr style="background:#f1f5f9; color:#0f172a;">
        <th style="padding:8px 10px; border:1px solid #cbd5e1; text-align:left; width:15%;">Lifecycle Phase</th>
        <th style="padding:8px 10px; border:1px solid #cbd5e1; text-align:left; width:40%;">System 1: Dalal Machine Tools Web Platform</th>
        <th style="padding:8px 10px; border:1px solid #cbd5e1; text-align:left; width:40%;">System 2: OMPI India LLP Industrial ERP</th>
        <th style="padding:8px 10px; border:1px solid #cbd5e1; text-align:center; width:5%;">Sync</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td style="padding:6px 10px; border:1px solid #cbd5e1; font-weight:700;">1. Inbound Ingestion</td>
        <td style="padding:6px 10px; border:1px solid #cbd5e1;">Buyer inquires on <strong>Catalog (Route 04)</strong> or submits RFQ on <strong>Product Detail (Route 05)</strong> with exact press tonnage.</td>
        <td style="padding:6px 10px; border:1px solid #cbd5e1;">Inquiry auto-logged in <strong>RFQ Pipeline (Module 05)</strong>. System verifies customer GSTIN in <strong>Client Master (Module 01)</strong>.</td>
        <td style="padding:6px 10px; border:1px solid #cbd5e1; text-align:center; font-weight:700; color:#10b981;">&#10142;</td>
      </tr>
      <tr style="background:#f8fafc;">
        <td style="padding:6px 10px; border:1px solid #cbd5e1; font-weight:700;">2. Technical Sizing</td>
        <td style="padding:6px 10px; border:1px solid #cbd5e1;">Buyer verifies physical stockyard ground readiness in Pune via <strong>Live Radar Indicators</strong>.</td>
        <td style="padding:6px 10px; border:1px solid #cbd5e1;">Engineer inputs flywheel RPM &amp; air pressure into <strong>Torque Sizing Calculator (Module 16)</strong>; outputs certified OMPI model.</td>
        <td style="padding:6px 10px; border:1px solid #cbd5e1; text-align:center; font-weight:700; color:#10b981;">&#10142;</td>
      </tr>
      <tr>
        <td style="padding:6px 10px; border:1px solid #cbd5e1; font-weight:700;">3. Costing &amp; Quote</td>
        <td style="padding:6px 10px; border:1px solid #cbd5e1;">Dalal staff uses <strong>Lead Triage Console (Route 07)</strong> to fire instant WhatsApp technical proposal.</td>
        <td style="padding:6px 10px; border:1px solid #cbd5e1;"><strong>Landed Cost Engine (Module 13)</strong> checks EUR exchange rate; <strong>Fast-Quote (Module 04)</strong> issues formal branded PDF.</td>
        <td style="padding:6px 10px; border:1px solid #cbd5e1; text-align:center; font-weight:700; color:#10b981;">&#10142;</td>
      </tr>
      <tr style="background:#f8fafc;">
        <td style="padding:6px 10px; border:1px solid #cbd5e1; font-weight:700;">4. Inventory Lock</td>
        <td style="padding:6px 10px; border:1px solid #cbd5e1;">Machine marked as "Under Commercial Hold" in public catalog.</td>
        <td style="padding:6px 10px; border:1px solid #cbd5e1;"><strong>Serial Registry (Module 20)</strong> reserves laser-etched clutch unit in <strong>Warehouse Bin Ledger (Module 18)</strong>.</td>
        <td style="padding:6px 10px; border:1px solid #cbd5e1; text-align:center; font-weight:700; color:#10b981;">&#10142;</td>
      </tr>
      <tr>
        <td style="padding:6px 10px; border:1px solid #cbd5e1; font-weight:700;">5. Field Retrofit</td>
        <td style="padding:6px 10px; border:1px solid #cbd5e1;">Client accesses <strong>Services Portal (Route 03)</strong> to review crankshaft boring &amp; foundation milestones.</td>
        <td style="padding:6px 10px; border:1px solid #cbd5e1;">Service engineer executes <strong>5-Stage Job Card (Module 23)</strong>, logging runout gauge readings (&lt;0.05mm) with photos.</td>
        <td style="padding:6px 10px; border:1px solid #cbd5e1; text-align:center; font-weight:700; color:#10b981;">&#10142;</td>
      </tr>
      <tr style="background:#f8fafc;">
        <td style="padding:6px 10px; border:1px solid #cbd5e1; font-weight:700;">6. Invoicing &amp; AMC</td>
        <td style="padding:6px 10px; border:1px solid #cbd5e1;">Machine marked "Sold"; installation photo added to <strong>Shipment Archive (Route 07)</strong>.</td>
        <td style="padding:6px 10px; border:1px solid #cbd5e1;"><strong>Invoice Engine (Module 26)</strong> issues B2B Tax Invoice; <strong>GSTR-1 (Module 27)</strong> reconciles; <strong>AMC (Module 29)</strong> initiates recurring spares cycle.</td>
        <td style="padding:6px 10px; border:1px solid #cbd5e1; text-align:center; font-weight:700; color:#10b981;">&#10004;</td>
      </tr>
    </tbody>
  </table>
</div>

<div class="footer-note">
  <div><strong>Dalal Machine Tools Agency Pvt. Ltd. &amp; OMPI India LLP</strong> &bull; Complete Systems, Pages &amp; Modular Architecture Manual</div>
  <div>Architect: Suyash Shinde &bull; Pimpri, Pune &bull; +91 96070 28594</div>
</div>

</body>
</html>
""")

final_html = "".join(body_parts)
out_path = 'd:/st.ourhtmldemo.com/DALAL_AND_OMPI_57_PAGES_AND_MODULES_MASTER_SPECIFICATION.html'
with open(out_path, 'w', encoding='utf-8') as f:
    f.write(final_html)
print(f"Generated {out_path} successfully!")
