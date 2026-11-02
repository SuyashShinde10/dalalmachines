# -*- coding: utf-8 -*-
import os, sys, subprocess, shutil
from make_professional_manual import routes, modules, out_html, out_pdf

print("Assembling 20-page professional manual...")

total_pages = 20

def get_page_header(page_title="MASTER SYSTEMS, PAGES & MODULAR ARCHITECTURE BLUEPRINT"):
    return f"""
    <div class="header-bar">
      <div>
        <div class="brand-title">DALAL MACHINE TOOLS AGENCY &amp; OMPI INDIA</div>
        <div class="brand-subtitle">{page_title}</div>
      </div>
      <div class="doc-meta">
        <strong>Doc Ref:</strong> ARCH-DOC-2026-DALAL-OMPI-57<br>
        <strong>Classification:</strong> Confidential &amp; Proprietary<br>
        <strong>Revision:</strong> v2.0 (Engineering Baseline)
      </div>
    </div>
"""

def get_page_footer(page_num):
    return f"""
    <div class="doc-footer">
      <div><strong>Dalal Machine Tools Agency Pvt. Ltd. &bull; OMPI India LLP</strong></div>
      <div>Page {page_num} of {total_pages} &bull; Master Systems &amp; Modular Architecture Manual &bull; Commercial Baseline</div>
      <div>Architect: <strong>Suyash Shinde</strong> (+91 96070 28594)</div>
    </div>
"""

pages_html = []

# ==============================================================================
# PAGE 1: EXECUTIVE BRIEF, PARTIES & HIGH-LEVEL ARCHITECTURE
# ==============================================================================
p1_content = f"""
  <div class="page">
    <div class="page-content">
      {get_page_header("SYSTEM ARCHITECTURE & OPERATIONAL BLUEPRINT")}
      
      <!-- Party Identification Block -->
      <div style="display:grid; grid-template-columns:1fr 1fr; gap:7px; background:#f8fafc; border:1.2px solid #cbd5e1; border-radius:4px; padding:6px 8px; margin-bottom:6px;">
        <div style="font-size:7.1pt; line-height:1.26; color:#334155;">
          <div style="font-size:6.8pt; font-weight:800; color:#0f172a; text-transform:uppercase; letter-spacing:0.4px; margin-bottom:2px;">
            Commercial Operating Entity (System 1)
          </div>
          <strong>Dalal Machine Tools Agency Pvt. Ltd.</strong><br>
          C-10, 3rd Floor, Commerce Centre, 78, Tardeo Main Road, Mumbai &ndash; 400034<br>
          <strong>Stockyard:</strong> Pune Industrial Machinery Yard, Pune Corridor, Maharashtra<br>
          <strong>Executive Leadership:</strong> Mr. Vinit Dalal, Managing Director
        </div>
        <div style="font-size:7.1pt; line-height:1.26; color:#334155;">
          <div style="font-size:6.8pt; font-weight:800; color:#0f172a; text-transform:uppercase; letter-spacing:0.4px; margin-bottom:2px;">
            Precision Engineering &amp; ERP Entity (System 2)
          </div>
          <strong>OMPI India LLP</strong> (Technical Alliance with OMPI S.r.l., Italy)<br>
          Precision Pneumatic Clutch-Brakes, Rotary Unions &amp; High-Tonnage Retrofits<br>
          <strong>Central Warehouse &amp; Service:</strong> Pune Central Spares Staging Hub<br>
          <strong>Technical Authorizations:</strong> Exclusive Sales, Reconditioning &amp; Spares
        </div>
      </div>

      <!-- Lead Architect Profile -->
      <div style="display:flex; justify-content:space-between; align-items:center; background:#f0fdf4; border:1.2px solid #86efac; border-radius:4px; padding:4.5px 8px; margin-bottom:6px;">
        <div>
          <span style="font-size:6.4pt; font-weight:800; color:#166534; text-transform:uppercase; letter-spacing:0.4px;">Principal Systems Architect &amp; Delivery Consultant</span>
          <div style="font-size:8.2pt; font-weight:800; color:#0f172a;">Suyash Shinde</div>
          <div style="font-size:6.8pt; color:#334155;">Systems Architecture, High-Tonnage Industrial Workflows &amp; Enterprise ERP Systems</div>
        </div>
        <div style="text-align:right; font-size:6.8pt; color:#166534; line-height:1.25;">
          <strong>Location:</strong> Pimpri, Pune, Maharashtra<br>
          <strong>Phone:</strong> +91 96070 28594 &bull; <strong>Email:</strong> suyashshinde360@gmail.com
        </div>
      </div>

      <!-- Executive Architectural Summary -->
      <div style="margin-bottom:6px;">
        <div style="font-size:7.2pt; font-weight:800; color:#0f172a; text-transform:uppercase; letter-spacing:0.3px; margin-bottom:2px; border-left:3px solid #d97706; padding-left:5px;">
          Executive Architecture Summary
        </div>
        <p style="font-size:7.2pt; line-height:1.28; color:#334155; margin-bottom:4px;">
          This architectural specification defines the operational topology, data flow contracts, and functional interfaces for the dual-system technology modernization of <strong>Dalal Machine Tools Agency Pvt. Ltd.</strong> and <strong>OMPI India LLP</strong>. High-value capital equipment acquisitions (&pound;50,000 to &euro;500,000 equivalent) require verifiable trust, strict engineering compliance, and flawless post-sales lifecycle execution. This blueprint coordinates two synchronized platforms to eliminate dealer disintermediation, protect landed gross margins, and enforce statutory tax compliance.
        </p>
      </div>

      <!-- Scope Breakdown Grid -->
      <div class="summary-grid">
        <div class="summary-item">
          <div class="summary-label">System 1: Dalal Web Platform</div>
          <div class="summary-val">24 Routes</div>
          <div style="font-size:6.5pt; color:#475569; margin-top:1px;">Client-facing portal, 26-category search, machine dossiers &amp; RFQ pipeline.</div>
        </div>
        <div class="summary-item">
          <div class="summary-label">System 2: OMPI Industrial ERP</div>
          <div class="summary-val">33 Modules</div>
          <div style="font-size:6.5pt; color:#475569; margin-top:1px;">Landed costing, multi-level BOM, multi-yard inventory &amp; GST ledger.</div>
        </div>
        <div class="summary-item accent">
          <div class="summary-label">Total Engineering Scope</div>
          <div class="summary-val" style="color:#065f46;">57 Units</div>
          <div style="font-size:6.5pt; color:#065f46; margin-top:1px;">Full end-to-end commercial, engineering, inventory, and legal integration.</div>
        </div>
      </div>

      <!-- Multi-Tier Architecture Overview -->
      <div style="border:1.2px solid #cbd5e1; border-radius:4px; padding:6px 8px; background:#ffffff; margin-bottom:6px;">
        <div style="font-size:7.2pt; font-weight:800; color:#0f172a; text-transform:uppercase; letter-spacing:0.3px; margin-bottom:3.5px; border-bottom:1px solid #e2e8f0; padding-bottom:2px;">
          Multi-Tier Enterprise Architecture Topology
        </div>
        <div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:6px; font-size:6.8pt; line-height:1.25;">
          <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:3px; padding:4px 6px;">
            <strong style="color:#0f172a; display:block; margin-bottom:2px;">Tier 1: Presentation &amp; Discovery</strong>
            Semantic HTML5, CSS Grid, high-performance client-side parametric search, WebP visual assets, and WhatsApp Business API endpoints. Zero-dependency architecture ensuring sub-second rendering across factory mobile devices.
          </div>
          <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:3px; padding:4px 6px;">
            <strong style="color:#0f172a; display:block; margin-bottom:2px;">Tier 2: Business &amp; Sizing Engine</strong>
            Mathematical torque calculation ($GD^2$ inertia models), dynamic landed duty engine (Basic Customs Duty, SWS, IGST), 60-second PDF compilation, and indented Bill of Materials lifecycle management.
          </div>
          <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:3px; padding:4px 6px;">
            <strong style="color:#0f172a; display:block; margin-bottom:2px;">Tier 3: Persistence &amp; Governance</strong>
            Role-Based Access Control (RBAC) matrix, tamper-evident SHA-256 audit log, perpetual FIFO inventory bin ledger, automated nightly snapshots, and GSTR-1 compliant statutory tax accounting.
          </div>
        </div>
      </div>

      <!-- Document Control Table -->
      <div>
        <table class="matrix-table" style="font-size:6.8pt;">
          <thead>
            <tr>
              <th style="width:20%;">Document ID</th>
              <th style="width:20%;">Effective Date</th>
              <th style="width:20%;">Jurisdiction</th>
              <th style="width:20%;">Target Production</th>
              <th style="width:20%;">Classification</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><strong>ARCH-DOC-2026-57</strong></td>
              <td>November 1, 2026</td>
              <td>Pune / Mumbai, India</td>
              <td>FY 2026&ndash;2027</td>
              <td style="color:#b45309; font-weight:700;">RESTRICTED / COMMERCIAL</td>
            </tr>
          </tbody>
        </table>
      </div>

    </div>
    {get_page_footer(1)}
  </div>
"""
pages_html.append(p1_content)

# ==============================================================================
# PAGES 2 TO 7: DALAL MACHINE TOOLS WEB PLATFORM (24 ROUTES - 4 PER PAGE)
# ==============================================================================
for p_idx in range(6):
    page_num = p_idx + 2
    r_batch = routes[p_idx * 4 : (p_idx + 1) * 4]
    
    cards_html = ""
    for (r_id, r_title, r_path, r_persona, r_why, r_what, r_feats, r_schema) in r_batch:
        feat_items = ""
        for fname, fdesc in r_feats:
            feat_items += f'<div class="route-feature-item"><strong>{fname}:</strong> {fdesc}</div>'
            
        cards_html += f"""
      <div class="route-card">
        <div class="route-card-header">
          <span class="route-id-badge">{r_id}</span>
          <span class="route-title">{r_title}</span>
          <span class="route-path">{r_path}</span>
          <span class="route-persona">{r_persona}</span>
        </div>
        <div class="route-grid">
          <div class="route-col">
            <div class="col-label">Business Objective &amp; Risk Mitigated</div>
            <p style="color:#334155;">{r_why}</p>
          </div>
          <div class="route-col">
            <div class="col-label">Operational Workflow &amp; User Journey</div>
            <p style="color:#334155;">{r_what}</p>
          </div>
        </div>
        <div class="route-features">
          {feat_items}
        </div>
        <div style="margin-top:2.5px; padding-top:2px; border-top:1px solid #f1f5f9; font-family:'JetBrains Mono',monospace; font-size:6.2pt; color:#64748b;">
          <strong style="color:#0f172a;">Data Payload / Entities:</strong> {r_schema}
        </div>
      </div>
"""

    p_html = f"""
  <div class="page">
    <div class="page-content">
      {get_page_header("SYSTEM 1: DALAL CUSTOMER &amp; OPERATIONS PLATFORM")}
      
      <div class="section-header">
        <span class="section-title">Dalal Web Platform Specification &bull; Routes {p_idx*4 + 1:02d} to {(p_idx+1)*4:02d} of 24</span>
        <span class="section-tag">High-Ticket Asset Acquisition Engine</span>
      </div>

      {cards_html}

    </div>
    {get_page_footer(page_num)}
  </div>
"""
    pages_html.append(p_html)

# ==============================================================================
# PAGES 8 TO 18: OMPI INDUSTRIAL ERP (33 MODULES - 3 PER PAGE)
# ==============================================================================
for m_idx in range(11):
    page_num = m_idx + 8
    m_batch = modules[m_idx * 3 : (m_idx + 1) * 3]
    
    cards_html = ""
    for (m_id, m_title, m_engine, m_roles, m_why, m_sop, m_feats, m_schema, m_downstream) in m_batch:
        feat_items = ""
        for fname, fdesc in m_feats:
            feat_items += f'<div style="margin-bottom:1.5px;"><strong>{fname}:</strong> {fdesc}</div>'
            
        cards_html += f"""
      <div class="module-card">
        <div class="module-card-header">
          <span class="module-id-badge">{m_id}</span>
          <span class="module-title">{m_title}</span>
          <span class="module-engine">{m_engine}</span>
          <span class="module-roles">{m_roles}</span>
        </div>
        <div class="module-grid">
          <div>
            <div class="col-label">Business Purpose &amp; Governance Policy</div>
            <p style="color:#334155;">{m_why}</p>
          </div>
          <div>
            <div class="col-label">Standard Operating Procedure (SOP) &amp; Execution Flow</div>
            <p style="color:#334155;">{m_sop}</p>
          </div>
        </div>
        <div style="margin-top:3px; padding-top:2.5px; border-top:1px dashed #e2e8f0; font-size:6.9pt; line-height:1.24; color:#334155;">
          {feat_items}
        </div>
        <div class="module-spec-box">
          <div class="module-spec-grid">
            <div>
              <strong style="color:#0f172a; text-transform:uppercase; font-size:5.8pt; display:block;">Database Schema Attributes:</strong>
              <span style="font-family:'JetBrains Mono',monospace; font-size:6.0pt; color:#475569;">{m_schema}</span>
            </div>
            <div>
              <strong style="color:#0f172a; text-transform:uppercase; font-size:5.8pt; display:block;">Subsystem Classification:</strong>
              <span style="color:#1e3a8a; font-weight:700;">{m_engine}</span>
            </div>
            <div>
              <strong style="color:#0f172a; text-transform:uppercase; font-size:5.8pt; display:block;">Downstream Integration Triggers:</strong>
              <span style="color:#065f46; font-weight:700;">{m_downstream}</span>
            </div>
          </div>
        </div>
      </div>
"""

    p_html = f"""
  <div class="page">
    <div class="page-content">
      {get_page_header("SYSTEM 2: OMPI INDIA INDUSTRIAL OPERATIONS &amp; ERP SUITE")}
      
      <div class="section-header blue">
        <span class="section-title">OMPI India ERP Module Specification &bull; Modules {m_idx*3 + 1:02d} to {(m_idx+1)*3:02d} of 33</span>
        <span class="section-tag">Precision Engineering &amp; Landed Costing Engine</span>
      </div>

      {cards_html}

    </div>
    {get_page_footer(page_num)}
  </div>
"""
    pages_html.append(p_html)

# ==============================================================================
# PAGE 19: CROSS-SYSTEM LIFECYCLE HANDSHAKE MATRIX
# ==============================================================================
p19_content = f"""
  <div class="page">
    <div class="page-content">
      {get_page_header("CROSS-SYSTEM INTEGRATION ARCHITECTURE")}
      
      <div class="section-header" style="background:#0f172a;">
        <span class="section-title">End-to-End Industrial Lifecycle Synchronization Matrix</span>
        <span class="section-tag">Bi-Directional Handshake Contract</span>
      </div>

      <p style="font-size:7.2pt; line-height:1.28; color:#334155; margin-bottom:5px;">
        The table below defines the formal operational handshake between <strong>Dalal Machine Tools Agency</strong> (the inbound asset acquisition engine) and <strong>OMPI India LLP</strong> (the precision engineering, landed costing, and spares lifecycle engine). Each milestone executes an automated or governed state transition ensuring physical stock verification, credit limit enforcement, and statutory tax reconciliation.
      </p>

      <table class="matrix-table" style="font-size:6.9pt;">
        <thead>
          <tr>
            <th style="width:14%;">Lifecycle Stage</th>
            <th style="width:38%;">System 1: Dalal Machine Tools Web Platform</th>
            <th style="width:38%;">System 2: OMPI India Industrial ERP</th>
            <th style="width:10%; text-align:center;">Sync Protocol</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td style="font-weight:700; color:#0f172a;">1. Inbound Ingestion &amp; Triage</td>
            <td>Buyer submits inquiry on <strong>Catalog (/category.html)</strong> or <strong>Dossier (/product.html)</strong> specifying required tonnage, stroke, and bed dimensions.</td>
            <td>Lead auto-logged in <strong>RFQ Pipeline (Mod 05)</strong>. System verifies corporate GSTIN against <strong>Client Master (Mod 01)</strong> and validates credit limits.</td>
            <td style="text-align:center; font-weight:700; color:#047857;">API / Webhook</td>
          </tr>
          <tr>
            <td style="font-weight:700; color:#0f172a;">2. Engineering Sizing &amp; Audit</td>
            <td>Buyer evaluates ground availability via <strong>Live Radar Indicators</strong>; selects press for comparative specification analysis.</td>
            <td>Applications Engineer inputs flywheel RPM, inertia ($GD^2$), and air pressure into <strong>Torque Sizing Calculator (Mod 16)</strong>; selects matching OMPI model.</td>
            <td style="text-align:center; font-weight:700; color:#047857;">State Lock</td>
          </tr>
          <tr>
            <td style="font-weight:700; color:#0f172a;">3. Costing &amp; Quote Dispatch</td>
            <td>Sales rep triggers instant proposal payload via WhatsApp pre-population from <strong>Contact Portal (/contact.html)</strong>.</td>
            <td><strong>Landed Cost Engine (Mod 13)</strong> checks EUR exchange rate; <strong>Fast-Quote (Mod 04)</strong> generates formal branded PDF with CAD drawing in 60s.</td>
            <td style="text-align:center; font-weight:700; color:#047857;">Automated PDF</td>
          </tr>
          <tr>
            <td style="font-weight:700; color:#0f172a;">4. Inventory Reservation</td>
            <td>Machinery asset status updated to "Commercial Hold" on public catalog to prevent duplicate buyer inquiries.</td>
            <td><strong>Sales Order Engine (Mod 09)</strong> locks clutch unit in <strong>Warehouse Bin Ledger (Mod 18)</strong>; generates reservation tag in <strong>Serial Registry (Mod 20)</strong>.</td>
            <td style="text-align:center; font-weight:700; color:#047857;">FIFO Lock</td>
          </tr>
          <tr>
            <td style="font-weight:700; color:#0f172a;">5. Workshop Retrofit &amp; QA</td>
            <td>Buyer monitors modernization milestones (crankshaft machining, pit preparation) on <strong>Services Portal (/services.html)</strong>.</td>
            <td>Workshop Superintendent executes <strong>Service Job Card (Mod 23)</strong>: verifies runout (&lt;0.05mm), conducts 100-cycle pressure hold test, and issues QC certificate.</td>
            <td style="text-align:center; font-weight:700; color:#047857;">QC Sign-off</td>
          </tr>
          <tr>
            <td style="font-weight:700; color:#0f172a;">6. Dispatch, Tax &amp; AMC</td>
            <td>Press marked as "Sold &amp; Commissioned"; high-resolution installation photography archived to <strong>Gallery (/gallery.html)</strong>.</td>
            <td><strong>Invoice Engine (Mod 26)</strong> issues B2B Tax Invoice; <strong>GSTR-1 (Mod 27)</strong> reconciles outward supplies; <strong>AMC Engine (Mod 29)</strong> initiates recurring spares cycle.</td>
            <td style="text-align:center; font-weight:700; color:#047857;">Statutory Close</td>
          </tr>
        </tbody>
      </table>

      <!-- API Data Contract Summary Box -->
      <div style="margin-top:6px; border:1.2px solid #cbd5e1; border-radius:4px; padding:6px 8px; background:#f8fafc;">
        <div style="font-size:7.0pt; font-weight:800; color:#0f172a; text-transform:uppercase; letter-spacing:0.3px; margin-bottom:3px;">
          Data Exchange Protocol &amp; Webhook Envelope Schema
        </div>
        <div style="font-family:'JetBrains Mono',monospace; font-size:6.1pt; color:#334155; line-height:1.24;">
          <strong>POST /api/v2/ingest/rfq:</strong> &#123; "event_id": "EV-9921", "source_route": "/product.html", "machine_sku": "TMP-K8544-2500T", "buyer_name": "Rajiv Sharma", "company_name": "Acme Forgings Pvt Ltd", "phone": "+919820000000", "gstin": "27AAACA1234A1Z5", "tonnage_interest": 2500, "timestamp_utc": "2026-11-01T10:30:00Z" &#125;<br>
          <strong>RESPONSE:</strong> &#123; "status": "QUEUED", "rfq_id": "RFQ-2026-1044", "assigned_engineer": "Applications Team Pune", "credit_status": "APPROVED", "quote_eta_mins": 15 &#125;
        </div>
      </div>

    </div>
    {get_page_footer(19)}
  </div>
"""
pages_html.append(p19_content)

# ==============================================================================
# PAGE 20: INFRASTRUCTURE, ZERO-TRUST SECURITY & FORMAL SIGN-OFF
# ==============================================================================
p20_content = f"""
  <div class="page">
    <div class="page-content">
      {get_page_header("GOVERNANCE, RELIABILITY &amp; FORMAL SIGN-OFF")}
      
      <div class="section-header" style="background:#0f172a;">
        <span class="section-title">Enterprise Security, Governance &amp; Operational Acceptance</span>
        <span class="section-tag">Statutory &amp; Technical Sign-Off</span>
      </div>

      <!-- 4-Quadrant Governance Grid -->
      <div style="display:grid; grid-template-columns:1fr 1fr; gap:6px; margin-bottom:6px;">
        <div style="background:#ffffff; border:1.2px solid #cbd5e1; border-radius:4px; padding:5px 7px;">
          <div style="font-size:6.8pt; font-weight:800; color:#0f172a; text-transform:uppercase; border-bottom:1px solid #e2e8f0; padding-bottom:2px; margin-bottom:2.5px;">
            1. LAN-First Resilience &amp; Deployment Topology
          </div>
          <p style="font-size:6.7pt; line-height:1.24; color:#334155;">
            The system operates on a hybrid architecture. The public web platform is hosted on high-availability cloud infrastructure with global CDN caching. The OMPI industrial ERP executes primarily on a localized on-premise local area network (LAN) server within the Pune facility, guaranteeing uninterrupted warehouse and workshop operations during internet connectivity failures.
          </p>
        </div>
        <div style="background:#ffffff; border:1.2px solid #cbd5e1; border-radius:4px; padding:5px 7px;">
          <div style="font-size:6.8pt; font-weight:800; color:#0f172a; text-transform:uppercase; border-bottom:1px solid #e2e8f0; padding-bottom:2px; margin-bottom:2.5px;">
            2. Cryptographic Security &amp; Immutable Audit Trail
          </div>
          <p style="font-size:6.7pt; line-height:1.24; color:#334155;">
            Role-Based Access Control (RBAC) enforces strict least-privilege permissions across 5 operational tiers (Sales, Engineering, Warehouse, Finance, Executive). All price adjustments, discount overrides, and invoice cancellations generate append-only transaction logs secured with SHA-256 cryptographic hashes, guaranteeing tamper-evident auditability.
          </p>
        </div>
        <div style="background:#ffffff; border:1.2px solid #cbd5e1; border-radius:4px; padding:5px 7px;">
          <div style="font-size:6.8pt; font-weight:800; color:#0f172a; text-transform:uppercase; border-bottom:1px solid #e2e8f0; padding-bottom:2px; margin-bottom:2.5px;">
            3. Statutory Tax &amp; Customs Compliance
          </div>
          <p style="font-size:6.7pt; line-height:1.24; color:#334155;">
            Fully harmonized with Indian Customs and GST regulations. Automatic verification of 8-digit HSN codes (8483 for clutches, 6813 for friction materials, 8462 for machine tools). Generates compliant B2B tax invoices with CGST/SGST/IGST breakdowns, Rule 55 delivery challans, and one-click JSON exports for direct GSTR-1 portal filing.
          </p>
        </div>
        <div style="background:#ffffff; border:1.2px solid #cbd5e1; border-radius:4px; padding:5px 7px;">
          <div style="font-size:6.8pt; font-weight:800; color:#0f172a; text-transform:uppercase; border-bottom:1px solid #e2e8f0; padding-bottom:2px; margin-bottom:2.5px;">
            4. Disaster Recovery &amp; Redundant Snapshots
          </div>
          <p style="font-size:6.7pt; line-height:1.24; color:#334155;">
            Automated zero-downtime database snapshots execute every 24 hours to an isolated Network Attached Storage (NAS) array. Nightly encrypted archives are transmitted to a secondary off-site location. Disaster recovery protocols are tested quarterly, providing a Recovery Point Objective (RPO) of &lt;24 hours and a Recovery Time Objective (RTO) of &lt;15 minutes.
          </p>
        </div>
      </div>

      <!-- Formal Acceptance & Sign-off Block -->
      <div style="border:1.2px solid #0f172a; border-radius:4px; padding:6px 8px; background:#f8fafc; margin-top:4px;">
        <div style="font-size:7.0pt; font-weight:800; color:#0f172a; text-transform:uppercase; letter-spacing:0.4px; margin-bottom:2px;">
          Formal Architectural Acceptance &amp; Production Release Sign-Off
        </div>
        <p style="font-size:6.7pt; color:#475569; margin-bottom:6px; line-height:1.22;">
          The functional specifications, page routes, and ERP module behaviors described across this 20-page document represent the agreed baseline between the commercial operating entities and the lead technical consultant.
        </p>

        <div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:7px;">
          <div style="border:1px dashed #94a3b8; border-radius:3px; padding:4px 6px; background:#ffffff;">
            <div style="font-size:6.2pt; font-weight:800; color:#64748b; text-transform:uppercase;">Commercial Operating Entity</div>
            <div style="font-size:7.2pt; font-weight:700; color:#0f172a; margin-top:1px;">Dalal Machine Tools Agency Pvt. Ltd.</div>
            <div style="margin-top:16px; border-top:1px solid #0f172a; padding-top:2px; font-size:6.2pt; color:#475569;">
              <strong>Mr. Vinit Dalal</strong><br>
              Managing Director &bull; Date: _______________
            </div>
          </div>
          <div style="border:1px dashed #94a3b8; border-radius:3px; padding:4px 6px; background:#ffffff;">
            <div style="font-size:6.2pt; font-weight:800; color:#64748b; text-transform:uppercase;">Precision Engineering Partner</div>
            <div style="font-size:7.2pt; font-weight:700; color:#0f172a; margin-top:1px;">OMPI India LLP</div>
            <div style="margin-top:16px; border-top:1px solid #0f172a; padding-top:2px; font-size:6.2pt; color:#475569;">
              <strong>Authorized Signatory</strong><br>
              Operations Director &bull; Date: _______________
            </div>
          </div>
          <div style="border:1px dashed #94a3b8; border-radius:3px; padding:4px 6px; background:#ffffff;">
            <div style="font-size:6.2pt; font-weight:800; color:#64748b; text-transform:uppercase;">Principal Systems Architect</div>
            <div style="font-size:7.2pt; font-weight:700; color:#0284c7; margin-top:1px;">Suyash Shinde</div>
            <div style="margin-top:16px; border-top:1px solid #0f172a; padding-top:2px; font-size:6.2pt; color:#475569;">
              <strong>Suyash Shinde</strong><br>
              Pimpri, Pune &bull; Date: November 1, 2026
            </div>
          </div>
        </div>
      </div>

    </div>
    {get_page_footer(20)}
  </div>
"""
pages_html.append(p20_content)

full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Dalal Machine Tools &amp; OMPI India - Master Systems Architecture Specification (24 Routes + 33 ERP Modules)</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;600;700&display=swap" rel="stylesheet">
  <style>
    @page {{
      size: A4 portrait;
      margin: 7mm 9mm 7mm 9mm;
    }}
    *, *::before, *::after {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}
    body {{
      font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      color: #0f172a;
      background: #ffffff;
      font-size: 7.8pt;
      line-height: 1.29;
      -webkit-print-color-adjust: exact;
      print-color-adjust: exact;
    }}
    .page {{
      height: 283mm;
      max-height: 283mm;
      overflow: hidden;
      box-sizing: border-box;
      position: relative;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      page-break-after: always;
      break-after: page;
      padding: 1px 0;
    }}
    .page:last-child {{
      page-break-after: avoid;
      break-after: avoid;
    }}
    .page-content {{
      flex: 1;
    }}

    /* Corporate Header */
    .header-bar {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 2px solid #0f172a;
      border-top: 3px solid #d97706;
      padding-top: 3px;
      padding-bottom: 3.5px;
      margin-bottom: 5px;
    }}
    .brand-title {{
      font-size: 11.2pt;
      font-weight: 800;
      color: #0f172a;
      letter-spacing: -0.3px;
      text-transform: uppercase;
    }}
    .brand-subtitle {{
      font-size: 6.7pt;
      font-weight: 700;
      color: #b45309;
      text-transform: uppercase;
      letter-spacing: 0.6px;
      margin-top: 1px;
    }}
    .doc-meta {{
      text-align: right;
      font-size: 6.5pt;
      color: #64748b;
      line-height: 1.25;
    }}
    .doc-meta strong {{
      color: #0f172a;
      font-weight: 700;
    }}

    /* Section Header */
    .section-header {{
      background: #0f172a;
      color: #ffffff;
      padding: 3.5px 7px;
      border-radius: 3px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 4.5px;
    }}
    .section-header.blue {{
      background: #1e3a8a;
    }}
    .section-title {{
      font-size: 8.0pt;
      font-weight: 800;
      letter-spacing: 0.4px;
      text-transform: uppercase;
    }}
    .section-tag {{
      font-size: 6.3pt;
      font-weight: 700;
      color: #f59e0b;
      letter-spacing: 0.5px;
      text-transform: uppercase;
    }}

    /* Route Cards (4 per page) */
    .route-card {{
      background: #ffffff;
      border: 1.2px solid #cbd5e1;
      border-radius: 4px;
      padding: 4.5px 6.5px;
      margin-bottom: 4px;
    }}
    .route-card-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 1px solid #e2e8f0;
      padding-bottom: 2px;
      margin-bottom: 2.5px;
    }}
    .route-id-badge {{
      background: #0f172a;
      color: #ffffff;
      font-size: 6.1pt;
      font-weight: 800;
      padding: 1.5px 4.5px;
      border-radius: 2.5px;
      text-transform: uppercase;
      letter-spacing: 0.4px;
      font-family: 'JetBrains Mono', monospace;
    }}
    .route-title {{
      font-size: 7.9pt;
      font-weight: 800;
      color: #0f172a;
      margin-left: 5px;
      flex: 1;
    }}
    .route-path {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 6.4pt;
      color: #b45309;
      font-weight: 700;
      background: #fef3c7;
      padding: 1px 4.5px;
      border-radius: 2px;
    }}
    .route-persona {{
      font-size: 6.2pt;
      color: #475569;
      background: #f1f5f9;
      padding: 1px 4.5px;
      border-radius: 2px;
      margin-left: 4px;
      font-weight: 600;
    }}
    .route-grid {{
      display: grid;
      grid-template-columns: 1.05fr 1fr;
      gap: 5.5px;
      font-size: 7.1pt;
      line-height: 1.26;
    }}
    .col-label {{
      font-size: 6.1pt;
      font-weight: 800;
      text-transform: uppercase;
      color: #64748b;
      letter-spacing: 0.3px;
      margin-bottom: 1px;
    }}
    .route-features {{
      margin-top: 2.5px;
      padding-top: 2px;
      border-top: 1px dashed #e2e8f0;
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 4px;
      font-size: 6.9pt;
      line-height: 1.23;
    }}
    .route-feature-item strong {{
      color: #0f172a;
      font-weight: 700;
    }}

    /* Module Cards (3 per page) */
    .module-card {{
      background: #ffffff;
      border: 1.2px solid #cbd5e1;
      border-radius: 4px;
      padding: 5px 7px;
      margin-bottom: 4.5px;
    }}
    .module-card-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 1px solid #e2e8f0;
      padding-bottom: 2.5px;
      margin-bottom: 3px;
    }}
    .module-id-badge {{
      background: #1e3a8a;
      color: #ffffff;
      font-size: 6.3pt;
      font-weight: 800;
      padding: 1.5px 5px;
      border-radius: 2.5px;
      text-transform: uppercase;
      letter-spacing: 0.4px;
      font-family: 'JetBrains Mono', monospace;
    }}
    .module-title {{
      font-size: 8.1pt;
      font-weight: 800;
      color: #0f172a;
      margin-left: 6px;
      flex: 1;
    }}
    .module-engine {{
      font-size: 6.2pt;
      color: #065f46;
      background: #ecfdf5;
      border: 1px solid #a7f3d0;
      padding: 1px 4.5px;
      border-radius: 2px;
      font-weight: 700;
      text-transform: uppercase;
    }}
    .module-roles {{
      font-size: 6.2pt;
      color: #475569;
      background: #f1f5f9;
      padding: 1px 4.5px;
      border-radius: 2px;
      margin-left: 4px;
      font-weight: 600;
    }}
    .module-grid {{
      display: grid;
      grid-template-columns: 1.1fr 1fr;
      gap: 6px;
      font-size: 7.1pt;
      line-height: 1.26;
    }}
    .module-spec-box {{
      margin-top: 3px;
      background: #f8fafc;
      border: 1px solid #e2e8f0;
      border-radius: 3px;
      padding: 3px 5px;
      font-size: 6.8pt;
      line-height: 1.23;
    }}
    .module-spec-grid {{
      display: grid;
      grid-template-columns: 1.1fr 0.9fr 1fr;
      gap: 4px;
    }}

    /* Running Footer */
    .doc-footer {{
      border-top: 1px solid #e2e8f0;
      padding-top: 2.5px;
      font-size: 6.3pt;
      color: #64748b;
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-top: 2px;
    }}
    .doc-footer strong {{
      color: #0f172a;
    }}

    /* Callouts & Grids */
    .summary-grid {{
      display: grid;
      grid-template-columns: 1fr 1fr 1.25fr;
      gap: 6px;
      margin-top: 4px;
      margin-bottom: 5px;
    }}
    .summary-item {{
      background: #f8fafc;
      border: 1px solid #e2e8f0;
      border-left: 3px solid #0f172a;
      border-radius: 3px;
      padding: 3.5px 5.5px;
    }}
    .summary-item.accent {{
      border-left-color: #059669;
      background: #f0fdf4;
    }}
    .summary-label {{
      font-size: 6.1pt;
      font-weight: 700;
      color: #64748b;
      text-transform: uppercase;
      letter-spacing: 0.4px;
    }}
    .summary-val {{
      font-size: 9.0pt;
      font-weight: 800;
      color: #0f172a;
      margin-top: 1px;
      font-family: 'JetBrains Mono', monospace;
    }}
    table.matrix-table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 6.9pt;
      margin-top: 3px;
    }}
    table.matrix-table th, table.matrix-table td {{
      border: 1px solid #cbd5e1;
      padding: 2.5px 4.5px;
      text-align: left;
      vertical-align: middle;
    }}
    table.matrix-table th {{
      background: #0f172a;
      color: #ffffff;
      font-size: 6.4pt;
      text-transform: uppercase;
      font-weight: 700;
    }}
    table.matrix-table tr:nth-child(even) td {{
      background: #f8fafc;
    }}
  </style>
</head>
<body>
{"".join(pages_html)}
</body>
</html>
"""

with open(out_html, 'w', encoding='utf-8') as f:
    f.write(full_html)

print(f"Generated {out_html} ({len(pages_html)} pages in HTML).")

