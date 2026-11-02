# scratch/apply_comprehensive_v2_5_fixes.py
import re

with open('scratch/build_enterprise_specification_v2.py', 'r', encoding='utf-8') as f:
    text = f.read()

# -------------------------------------------------------------
# 1. Update dalal_units: UNIT-10, UNIT-15, UNIT-16, UNIT-24
# -------------------------------------------------------------

# UNIT-10: Add legal/tax disclaimer
u10_old = '''        "id": "UNIT-10",
        "title": "Import Compliance & Legal Tax FAQs Guide",
        "type": "High Seas & Tax FAQs Guide",
        "audience": "Chief Financial Officers (CFOs), Company Legal & Tax Advisors",
        "focus": "High Seas Sales Procedures, Customs Bill of Entry & GST Credits",
        "does": "Plain-language explanations of High Seas Sales contracts, GST input tax credit (ITC) documentation, Customs Bill of Entry procedures, and live power inspection arrangements, addressing common commercial questions.",
        "benefit": "Provides clear information for client accountants and legal teams, addressing procedural concerns early and helping streamline formal corporate purchase approvals.",
        "deliverables": ["High Seas Sales Commercial Process Explainer", "Step-by-Step GST Tax Invoice Guidance", "Pre-Dispatch Inspection FAQ Summary"],
        "feature": "Interactive accordion explaining tax documentation and customs clearance procedures in simple terms."'''

u10_new = '''        "id": "UNIT-10",
        "title": "Import Compliance & Legal Tax FAQs Guide",
        "type": "High Seas & Tax FAQs Guide",
        "audience": "Chief Financial Officers (CFOs), Company Legal & Tax Advisors",
        "focus": "High Seas Sales Procedures, Customs Bill of Entry & GST Credits",
        "does": "Plain-language explanations of High Seas Sales contracts, GST documentation, Customs Bill of Entry procedures, and live power inspection arrangements. (Disclaimer: Information provided for operational guidance only; does not constitute legal or tax advice. Contracts must be vetted by Client's counsel).",
        "benefit": "Assists client accounting and legal teams in understanding procedural steps early, helping avoid common documentation hurdles during formal purchase approvals.",
        "deliverables": ["High Seas Commercial Workflow Explainer", "Step-by-Step GST Tax Documentation Guide", "Pre-Dispatch Power Inspection Summary"],
        "feature": "Interactive guide explaining import documentation in simple business terms (non-legal advisory)."'''

text = text.replace(u10_old, u10_new)

# UNIT-15: Add sizing disclaimer
u15_old = '''        "id": "UNIT-15",
        "title": "Press Tonnage & Sizing Assistant",
        "type": "Press Tonnage Sizing Assistant",
        "audience": "Manufacturing Sourcing Teams, New Plant Setup Heads",
        "focus": "Automated Tonnage Estimation from Component Dimensions",
        "does": "An interactive sizing guide where plant engineers enter their forged component dimensions, material type (steel, brass, aluminum), and production process to calculate an approximate recommended press capacity.",
        "benefit": "Guides prospective buyers toward appropriate press capacities before submitting an inquiry, helping ensure inquiries match realistic technical requirements.",
        "deliverables": ["Approximate Forging Force Calculation Formula", "Recommended Machine Models from Stock", "Direct WhatsApp Sizing Inquiry Button"],
        "feature": "Interactive formula suggesting suitable in-stock machinery based on estimated tonnage."'''

u15_new = '''        "id": "UNIT-15",
        "title": "Press Tonnage & Sizing Assistant",
        "type": "Press Tonnage Sizing Assistant",
        "audience": "Manufacturing Sourcing Teams, New Plant Setup Heads",
        "focus": "Automated Tonnage Estimation from Component Dimensions",
        "does": "An interactive sizing tool estimating recommended press capacity from part dimensions and material. (Disclaimer: Calculations are approximate technical estimations; final machine selection and tooling suitability must be certified by Client's qualified tooling/press engineer).",
        "benefit": "Guides prospective buyers toward realistic press tonnage categories before inquiring, helping filter inquiries and save preliminary engineering discussion time.",
        "deliverables": ["Approximate Tonnage Estimation Calculator", "Recommended Matching Machine Stock List", "Direct Technical Inquiry Dispatch Button"],
        "feature": "Interactive sizing formula suggesting suitable machinery categories (subject to engineer verification)."'''

text = text.replace(u15_old, u15_new)

# UNIT-16: Add customs disclaimer
u16_old = '''        "id": "UNIT-16",
        "title": "High Seas Sales Compliance Center",
        "type": "High Seas Compliance Center",
        "audience": "Corporate CFOs, Commercial Directors, Tax Consultants",
        "focus": "Legal Documentation, Port Handling & Customs Clearance",
        "does": "A clear procedural overview detailing the standard workflow for High Seas Sales transactions, including title transfer prior to customs frontiers, required shipping documents, and port clearance steps.",
        "benefit": "Provides transparency for corporate finance and tax departments, helping them understand the legal structure and duty benefits of port-delivered machinery transactions.",
        "deliverables": ["High Seas Sales Transaction Flow Overview", "Nhava Sheva Port Clearance Milestones", "Import Document Checklist for Buyers"],
        "feature": "Procedural guide outlining documentation requirements for High Seas machinery import."'''

u16_new = '''        "id": "UNIT-16",
        "title": "High Seas Sales Compliance Center",
        "type": "High Seas Compliance Center",
        "audience": "Corporate CFOs, Commercial Directors, Tax Consultants",
        "focus": "Legal Documentation, Port Handling & Customs Clearance",
        "does": "A clear procedural overview detailing standard High Seas Sales transactions, title transfer prior to customs borders, and port handling. (Disclaimer: Content provided for operational transparency only; does not substitute for formal maritime legal counsel or chartered tax advisory).",
        "benefit": "Provides clarity for corporate finance teams on documentation milestones, assisting in orderly customs coordination and duty assessments.",
        "deliverables": ["High Seas Sales Operational Workflow Map", "Nhava Sheva Port Milestone Checklist", "Import Document Requirements Summary"],
        "feature": "Procedural guide outlining documentation stages for port-delivered machinery (advisory excluded)."'''

text = text.replace(u16_old, u16_new)

# UNIT-24: Fix "smart" -> "urgency-based"
u24_old = '''        "id": "UNIT-24",
        "title": "Dalal Customer Inquiry Management Desk",
        "type": "Staff Operations Console",
        "audience": "Sales Team, Managing Director, Commercial Head",
        "focus": "Lead Tracking, Priority Sorting & Quotation History",
        "does": "A centralized operational inbox capturing incoming customer inquiries from the website and WhatsApp, displaying customer company name, machine requested, delivery urgency, and quotation history.",
        "benefit": "Helps ensure customer inquiries are systematically organized and tracked by sales staff, reducing the risk of missed inquiries and supporting timely commercial responses.",
        "deliverables": ["Centralized Inquiry Feed with Status Tracking", "Direct WhatsApp Chat Link to Buyer", "Quotation History & Commercial Notes"],
        "feature": "Smart inquiry priority sorting highlighting urgent inquiries for prompt sales attention."'''

u24_new = '''        "id": "UNIT-24",
        "title": "Dalal Customer Inquiry Management Desk",
        "type": "Staff Operations Console",
        "audience": "Sales Team, Managing Director, Commercial Head",
        "focus": "Inquiry Prioritization by Urgency & Quotation History",
        "does": "A centralized operational inbox organizing incoming customer inquiries from website and WhatsApp, displaying plant name, machine model, urgency level, and past quotation interaction logs.",
        "benefit": "Helps ensure customer inquiries are systematically organized and tracked by sales staff, reducing the risk of missed inquiries and supporting timely commercial responses.",
        "deliverables": ["Centralized Inquiry Feed with Status Tracking", "Direct WhatsApp Chat Link to Buyer", "Quotation History & Commercial Notes"],
        "feature": "Urgency-based inquiry prioritization flagging high-tonnage leads and active RFQs first."'''

text = text.replace(u24_old, u24_new)

# -------------------------------------------------------------
# 2. Update ompi_modules: ERP-MOD-03, ERP-MOD-04, ERP-MOD-08
# -------------------------------------------------------------

# ERP-MOD-03: Euro rate manual entry + optional live feed
m03_old = '''        "id": "ERP-MOD-03",
        "title": "Import Currency & Landed Pricing Calculator",
        "engine": "Engine 1: Sales & Customer Management",
        "role": "Commercial Manager, Managing Director",
        "focus": "Euro/INR Exchange Rate & Duty Surcharge Calculation",
        "does": "Calculates estimated selling prices in Indian Rupees based on current Euro exchange rates, ocean shipping costs, customs basic duty, port clearance charges, and target commercial margins.",
        "benefit": "Helps protect profit margins against currency shifts between the Euro and Rupee during international shipping, supporting consistent and sustainable commercial pricing.",
        "deliverables": ["Euro to INR Cost Conversion Calculator", "Customs Duty & Port Handling Surcharge Matrix", "Target Margin Calculation Guidelines"],
        "feature": "Automated landed cost calculation incorporating daily exchange rates and port charges."'''

m03_new = '''        "id": "ERP-MOD-03",
        "title": "Manual Exchange Rate & Landed Cost Calculator",
        "engine": "Engine 1: Sales & Customer Management",
        "role": "Commercial Manager, Managing Director",
        "focus": "Daily Manual Euro/INR Entry & Duty Surcharge Matrix (Optional Live API)",
        "does": "Enables commercial staff to input daily official Euro/INR rates manually (or via optional live Forex API subscription if provided by Client) to calculate landed selling prices including sea freight, basic customs duty, and target margins.",
        "benefit": "Helps protect profit margins against currency shifts between the Euro and Rupee during international shipping, supporting consistent and sustainable commercial pricing.",
        "deliverables": ["Daily Manual Euro Exchange Rate Entry Interface", "Customs Duty & Port Handling Surcharge Matrix", "Target Margin Calculation Guidelines"],
        "feature": "Manual daily exchange rate entry with automated duty surcharge calculation (live feed optional add-on)."'''

text = text.replace(m03_old, m03_new)

# ERP-MOD-04: Cross-entity quoting with isolated letterhead & banking
m04_old = '''        "id": "ERP-MOD-04",
        "title": "Fast-Quote Proposal PDF Generator",
        "engine": "Engine 1: Sales & Customer Management",
        "role": "Sales Representatives, Commercial Staff",
        "focus": "Standard Branded Proposals & WhatsApp Dispatch",
        "does": "Compiles formal commercial quotation letters complete with machine photos, dimensional specifications, pricing, and standard payment terms using Dalal's central quoting engine.",
        "benefit": "Enables sales staff to generate and send official quotation letters while discussing requirements with prospective buyers, helping accelerate response times and customer decisions.",
        "deliverables": ["Standard A4 PDF Quotation Generator", "Pre-Configured Payment Terms & Validity Dates", "WhatsApp & Email Proposal Dispatch Link"],
        "feature": "1-click generation of print-ready formal A4 PDF quotations with official signature."'''

m04_new = '''        "id": "ERP-MOD-04",
        "title": "OMPI Fast-Quote & Commercial Proposal Generator",
        "engine": "Engine 1: Sales & Customer Management",
        "role": "Sales Representatives, Commercial Staff",
        "focus": "Shared Quoting Architecture with Isolated OMPI Letterhead & Banking",
        "does": "Extends the Phase 1 Centralized Quoting Engine to OMPI India LLP products. Generates formal PDF proposals for Italian clutch models and sizing data, strictly maintaining OMPI India LLP's distinct letterhead, sequential quote numbering, and independent bank details.",
        "benefit": "Enables sales staff to generate and send official quotation letters while discussing requirements with prospective buyers, helping accelerate response times and customer decisions.",
        "deliverables": ["Dedicated OMPI India LLP Branded Quotation Format", "Separate Quote Numbering Sequence & Bank Details", "WhatsApp & Email Proposal Dispatch Link"],
        "feature": "Shared quoting engine generating OMPI proposals with distinct entity letterhead and banking."'''

text = text.replace(m04_old, m04_new)

# ERP-MOD-08: Container tracking manual entry
m08_old = '''        "id": "ERP-MOD-08",
        "title": "In-Transit Shipping Container Tracker",
        "engine": "Engine 2: Inventory & Warehouse Management",
        "role": "Logistics Officer, Commercial Staff",
        "focus": "Container Tracking from European Ports to Nhava Sheva",
        "does": "Tracks imported shipments from European departure to arrival at Nhava Sheva (JNPT), recording vessel details, estimated arrival dates, and customs clearance status.",
        "benefit": "Assists the logistics team in providing delivery estimates to customers awaiting imported equipment and helps prepare customs documents ahead of vessel arrival.",
        "deliverables": ["Container Transit Milestone Records", "Customs Clearance Status Log", "Customer Pre-Arrival Notification Workflow"],
        "feature": "Milestone tracker monitoring container vessel arrival schedules and clearance steps."'''

m08_new = '''        "id": "ERP-MOD-08",
        "title": "Container Transit & Shipping Milestone Logger (Manual Entry)",
        "engine": "Engine 2: Inventory & Warehouse Management",
        "role": "Logistics Officer, Commercial Staff",
        "focus": "Manual Bill of Lading (BL) & Shipping Milestone Logging",
        "does": "Provides a structured manual logging interface where logistics staff input Bill of Lading (BL) numbers, vessel names, departure dates, estimated arrival at Nhava Sheva, and customs milestone updates (carrier API available as optional add-on).",
        "benefit": "Assists the logistics team in providing delivery estimates to customers awaiting imported equipment and helps prepare customs documents ahead of vessel arrival.",
        "deliverables": ["Manual BL & Vessel Arrival Logging Interface", "Port Customs Clearance Status Log", "Customer Pre-Arrival Notification Workflow"],
        "feature": "Manual milestone status logger tracking vessel arrival schedules and container clearance."'''

text = text.replace(m08_old, m08_new)

# -------------------------------------------------------------
# 3. Update render_card: Explicit Phase 1, Phase 2, Phase 3 mapping
# -------------------------------------------------------------
old_render_milestone = '''          <div style="display:flex; justify-content:space-between; align-items:center; background:#f8fafc; border:1px solid #e2e8f0; border-radius:4px; padding:4px 12px; margin-top:8px; font-size:7.8pt; color:#475569;">
            <div><strong>Planned Milestone:</strong> {('Phase 1 (Dalal Machinery Launch)' if is_route else 'Phase 2 &bull; 3 (OMPI Operations Rollout)')}</div>
            <div><strong>Verification Criteria:</strong> Functional UAT &amp; Data Review prior to commencement</div>
          </div>'''

new_render_milestone = '''          <div style="display:flex; justify-content:space-between; align-items:center; background:#f8fafc; border:1px solid #e2e8f0; border-radius:4px; padding:4px 12px; margin-top:8px; font-size:7.8pt; color:#475569;">
            <div><strong>Planned Milestone:</strong> {('Phase 1: Dalal Platform (Weeks 1–8 • Months 1–2)' if is_route else ('Phase 2: OMPI Core ERP (Weeks 9–20 • Months 3–5)' if int(item['id'].replace('ERP-MOD-', '')) <= 18 else 'Phase 3: Operations & Executive Control (Weeks 21–32 • Months 6–8)'))}</div>
            <div><strong>Verification Criteria:</strong> Functional UAT &amp; 7-Day Review Gate</div>
          </div>'''

text = text.replace(old_render_milestone, new_render_milestone)

# -------------------------------------------------------------
# 4. Update PAGE 1: Cover Page (Validity 14 Nov, Designation, Hybrid Hosting, 8-Month Roadmap)
# -------------------------------------------------------------
old_p1_hero = '''      <!-- Hero Header Box -->
      <div style="background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); color: #ffffff; border-radius: 8px; padding: 22px 24px; margin-bottom: 12px; border-left: 6px solid #d97706; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);">
        <div style="font-size: 8.5pt; font-weight: 800; color: #f59e0b; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 4px;">
          Executive Proposal &bull; Pre-Commencement Architecture Blueprint (Version 2.4)
        </div>
        <div style="font-size: 18.5pt; font-weight: 800; line-height: 1.25; margin-bottom: 8px;">
          Unified Digital Ecosystem &amp; Enterprise Operations Suite
        </div>
        <div style="font-size: 10.2pt; line-height: 1.45; color: #cbd5e1;">
          Authoritative 57-Unit Operational Architecture prepared for <strong>Dalal Machine Tools Agency Pvt. Ltd.</strong> and <strong>OMPI India LLP</strong>. Written in plain business language for executive review and operational alignment.
        </div>
      </div>'''

new_p1_hero = '''      <!-- Hero Header Box -->
      <div style="background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); color: #ffffff; border-radius: 8px; padding: 20px 24px; margin-bottom: 11px; border-left: 6px solid #d97706; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);">
        <div style="font-size: 8.5pt; font-weight: 800; color: #f59e0b; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 3px;">
          Executive Scope Blueprint &bull; Version 2.5 &bull; Validity: Thru 14 November 2026
        </div>
        <div style="font-size: 18.0pt; font-weight: 800; line-height: 1.25; margin-bottom: 6px;">
          Unified Digital Ecosystem &amp; Enterprise Operations Suite
        </div>
        <div style="font-size: 9.8pt; line-height: 1.45; color: #cbd5e1;">
          Authoritative 57-Unit Operational Architecture prepared for <strong>Dalal Machine Tools Agency Pvt. Ltd.</strong> and <strong>OMPI India LLP</strong>. 8-Month Phased Roadmap across Cloud Showroom and On-Premise Office ERP.
        </div>
      </div>'''

text = text.replace(old_p1_hero, new_p1_hero)

old_p1_meta = '''      <!-- Metadata Box -->
      <div style="background:#ffffff; border:1.5px solid #0f172a; border-radius:7px; padding:10px 16px; display:flex; justify-content:space-between; align-items:center;">
        <div>
          <span style="font-size:7.8pt; color:#64748b; font-weight:700; text-transform:uppercase;">Principal Client:</span><br>
          <strong style="font-size:9.5pt; color:#0f172a;">Mr. Vinit Dalal</strong> &bull; Managing Director / Partner
        </div>
        <div>
          <span style="font-size:7.8pt; color:#64748b; font-weight:700; text-transform:uppercase;">Scope Architecture:</span><br>
          <strong style="font-size:9.5pt; color:#0f172a;">57 Proposed Units</strong> &bull; Pre-Commencement Proposal
        </div>
        <div>
          <span style="font-size:7.8pt; color:#64748b; font-weight:700; text-transform:uppercase;">Prepared by Consultant:</span><br>
          <strong style="font-size:9.5pt; color:#0f172a;">Suyash Shinde</strong> &bull; Principal Software Consultant
        </div>
      </div>'''

new_p1_meta = '''      <!-- Architecture & Infrastructure Summary Banner -->
      <div style="background:#f1f5f9; border:1.5px solid #cbd5e1; border-radius:7px; padding:9px 14px; margin-bottom:11px; display:grid; grid-template-columns:1fr 1fr; gap:10px; font-size:8.2pt; line-height:1.38; color:#334155;">
        <div>
          <strong>System 1 (Dalal Machinery):</strong> Public Cloud Hosting (AWS/Render) with global CDN &bull; 24 Units &bull; Phase 1 (Weeks 1–8).
        </div>
        <div>
          <strong>System 2 (OMPI ERP):</strong> On-Premise Office LAN on Dedicated Pune Host PC &bull; 33 Modules &bull; Phase 2 &amp; 3 (Weeks 9–32).
        </div>
      </div>

      <!-- Metadata Box -->
      <div style="background:#ffffff; border:1.5px solid #0f172a; border-radius:7px; padding:9px 16px; display:flex; justify-content:space-between; align-items:center;">
        <div>
          <span style="font-size:7.6pt; color:#64748b; font-weight:700; text-transform:uppercase;">Principal Client:</span><br>
          <strong style="font-size:9.2pt; color:#0f172a;">Mr. Vinit Dalal</strong> &bull; Managing Director / Partner
        </div>
        <div>
          <span style="font-size:7.6pt; color:#64748b; font-weight:700; text-transform:uppercase;">Scope &amp; Duration:</span><br>
          <strong style="font-size:9.2pt; color:#0f172a;">57 Units &bull; 8 Months (32 Wks)</strong>
        </div>
        <div>
          <span style="font-size:7.6pt; color:#64748b; font-weight:700; text-transform:uppercase;">Principal Consultant:</span><br>
          <strong style="font-size:9.2pt; color:#0f172a;">Suyash Shinde</strong> &bull; Principal Software Consultant
        </div>
      </div>'''

text = text.replace(old_p1_meta, new_p1_meta)

# Update doc header ref
text = text.replace('SCOPE-PLAN-2026-DALAL-OMPI-57 (v2.4)', 'SCOPE-PLAN-2026-DALAL-OMPI-57 (v2.5)')
text = text.replace('Version 2.4', 'Version 2.5')

# -------------------------------------------------------------
# 5. Update PAGE 2: 1-Page Executive Summary
# -------------------------------------------------------------
old_p2 = '''    # PAGE 2: 1-PAGE EXECUTIVE SUMMARY (NEW)
    html += f"""
  <div class="page">
    <div class="page-content">
      {make_header("EXECUTIVE 1-PAGE SUMMARY &bull; CORE DELIVERABLES, TIMELINE &amp; BOUNDARIES")}

      <div class="section-header">
        <span class="section-title">At-A-Glance Master Project Summary for Executive Leadership</span>
        <span class="section-tag">Executive Brief</span>
      </div>

      <!-- What You Get Box -->
      <div style="background:#ffffff; border:1.5px solid #cbd5e1; border-radius:7px; padding:15px 18px; margin-bottom:14px;">
        <div style="font-size:9.2pt; font-weight:800; color:#0f172a; text-transform:uppercase; margin-bottom:5px; border-bottom:1.5px solid #f1f5f9; padding-bottom:3px;">
          1. What You Get (The Complete 57-Unit Deliverable)
        </div>
        <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px; font-size:8.6pt; line-height:1.42; color:#334155;">
          <div>
            <strong>System 1: Dalal Public Platform (24 Units)</strong><br>
            A high-credibility machinery acquisition platform: 22 customer pages (showroom, live trial videos, 60-second quotation download, press tonnage sizing, High Seas FAQs) + 2 internal desks (machine spec manager &amp; customer RFQ inbox).
          </div>
          <div>
            <strong>System 2: OMPI Industrial ERP (33 Units)</strong><br>
            A dedicated operational software suite: 33 specialized modules covering Italian POs in Euros, landed port costing, Pune godown stock reservation, workshop overhaul job cards, GST tax invoices, and real-time Director command desk.
          </div>
        </div>
      </div>

      <!-- Realistic Phasing Timeline Table -->
      <div style="background:#f8fafc; border:1.5px solid #cbd5e1; border-radius:7px; padding:15px 18px; margin-bottom:14px;">
        <div style="font-size:9.2pt; font-weight:800; color:#0f172a; text-transform:uppercase; margin-bottom:5px;">
          2. Realistic Delivery Phasing &amp; Implementation Schedule
        </div>
        <table style="width:100%; border-collapse:collapse; font-size:8.4pt; line-height:1.4; color:#334155;">
          <thead>
            <tr style="background:#0f172a; color:#ffffff; text-align:left;">
              <th style="padding:6px 10px;">Milestone Phase</th>
              <th style="padding:6px 10px;">Scope of Deliverables</th>
              <th style="padding:6px 10px;">Target Duration</th>
              <th style="padding:6px 10px;">Commercial Status</th>
            </tr>
          </thead>
          <tbody>
            <tr style="border-bottom:1px solid #e2e8f0; background:#ffffff;">
              <td style="padding:7px 10px; font-weight:700;">Phase 1: Dalal Platform</td>
              <td style="padding:7px 10px;">22 Public Pages &bull; 2 Staff Desks &bull; Core Quotation Engine</td>
              <td style="padding:7px 10px; font-weight:600; color:#0f172a;">4 to 6 Weeks</td>
              <td style="padding:7px 10px; font-weight:700; color:#b45309;">TO COMMENCE UPON SIGN-OFF</td>
            </tr>
            <tr style="border-bottom:1px solid #e2e8f0; background:#f8fafc;">
              <td style="padding:7px 10px; font-weight:700;">Phase 2: OMPI Core ERP</td>
              <td style="padding:7px 10px;">Customer 360 &bull; Italian SKU Master &bull; Landed Cost &bull; Stock Tracker</td>
              <td style="padding:7px 10px; font-weight:600; color:#0f172a;">8 to 10 Weeks</td>
              <td style="padding:7px 10px; font-weight:600; color:#475569;">MONTH 2-3 SPRINT</td>
            </tr>
            <tr style="background:#ffffff;">
              <td style="padding:7px 10px; font-weight:700;">Phase 3: Advanced Operations</td>
              <td style="padding:7px 10px;">Workshop Job Cards &bull; GST Invoicing &bull; Port Tracking &bull; MD Command Desk</td>
              <td style="padding:7px 10px; font-weight:600; color:#0f172a;">8 to 10 Weeks</td>
              <td style="padding:7px 10px; font-weight:600; color:#475569;">MONTH 4-5 SPRINT</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Boundaries & Client Responsibilities Grid -->
      <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px; margin-bottom:10px;">
        <div style="background:#fff1f2; border:1.5px solid #fecdd3; border-radius:7px; padding:14px 16px;">
          <div style="font-size:8.8pt; font-weight:800; color:#9f1239; text-transform:uppercase; margin-bottom:3px;">
            3. What is NOT Included (Out of Scope)
          </div>
          <ul style="font-size:8.2pt; line-height:1.42; color:#4c0519; padding-left:14px; margin:0;">
            <li>Hardware (CCTV cameras, servers, PCs, barcode scanners).</li>
            <li>Third-party API &amp; cloud subscription fees (WhatsApp Meta fees, GST portal GSP fees, cloud hosting, domain).</li>
            <li>Content production (shooting videos, drafting legal agreements).</li>
          </ul>
        </div>
        <div style="background:#eff6ff; border:1.5px solid #bfdbfe; border-radius:7px; padding:14px 16px;">
          <div style="font-size:8.8pt; font-weight:800; color:#1e40af; text-transform:uppercase; margin-bottom:3px;">
            4. What Client Must Provide
          </div>
          <ul style="font-size:8.2pt; line-height:1.42; color:#1e3a8a; padding-left:14px; margin:0;">
            <li>Machinery specifications, stock photos &amp; power trial videos.</li>
            <li>Italian OMPI parts catalog dimension sheets and pricing rules.</li>
            <li>CA-vetted legal agreement templates &amp; tax guidance.</li>
            <li>Timely user acceptance testing (UAT) sign-off on delivered phases.</li>
          </ul>
        </div>
      </div>

      <!-- Core Operational Rules & Governance -->
      <div style="background:#ffffff; border:1.5px solid #cbd5e1; border-radius:7px; padding:11px 15px; margin-bottom:11px;">
        <div style="font-size:8.8pt; font-weight:800; color:#0f172a; text-transform:uppercase; margin-bottom:4px; border-bottom:1.5px solid #f1f5f9; padding-bottom:3px;">
          5. Core Operational Principles &amp; Quality Standards
        </div>
        <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px; font-size:8.2pt; line-height:1.38; color:#334155;">
          <div>
            <strong>Single Unified Quoting Engine:</strong> Quotation letters generated across website download (Unit 11), staff RFQ inbox (Unit 24), and OMPI ERP (MOD-04) share a single unified format.
          </div>
          <div>
            <strong>Separate Entity Accounting:</strong> Dalal Machine Tools Agency Pvt. Ltd. and OMPI India LLP maintain completely separate legal records, invoices, and bank remittance logs.
          </div>
        </div>
      </div>

      <!-- Commercial Governance Note -->
      <div style="background:#f8fafc; border:1.5px solid #0f172a; border-radius:7px; padding:10px 15px;">
        <div style="font-size:8.6pt; font-weight:800; color:#0f172a; text-transform:uppercase; margin-bottom:3px;">
          Commercial Scope Governance &amp; Agreement Annexure
        </div>
        <p style="font-size:8.2pt; line-height:1.4; color:#334155;">
          This master blueprint defines the functional scope of delivery. Commercial fee milestones, payment schedules, and legal terms shall be governed by the formal Master Services Agreement. Any feature not detailed herein shall be estimated separately under standard change control procedures.
        </p>
      </div>
    </div>
    {make_footer(2)}
  </div>
"""'''

new_p2 = '''    # PAGE 2: 1-PAGE EXECUTIVE SUMMARY (ALIGNED WITH PROPOSAL V1.0)
    html += f"""
  <div class="page">
    <div class="page-content">
      {make_header("EXECUTIVE 1-PAGE SUMMARY &bull; CORE DELIVERABLES, TIMELINE &amp; BOUNDARIES")}

      <div class="section-header">
        <span class="section-title">Master Project Summary Aligned with Unified Proposal (v1.0) &bull; 8-Month Roadmap</span>
        <span class="section-tag">Executive Summary</span>
      </div>

      <!-- 1. Deliverables & Infrastructure Architecture Box -->
      <div style="background:#ffffff; border:1.5px solid #cbd5e1; border-radius:7px; padding:12px 16px; margin-bottom:10px;">
        <div style="font-size:9.0pt; font-weight:800; color:#0f172a; text-transform:uppercase; margin-bottom:4px; border-bottom:1.5px solid #f1f5f9; padding-bottom:3px;">
          1. What You Get (57 Total Units &bull; Hybrid Cloud &amp; On-Premise LAN Architecture)
        </div>
        <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px; font-size:8.3pt; line-height:1.4; color:#334155;">
          <div>
            <strong>System 1: Dalal Machinery Platform (24 Units &bull; Cloud Hosted):</strong><br>
            Hosted on secure cloud infrastructure (AWS/Render) with global CDN. Includes 22 public pages (digital showroom, video trials, 60-second quotes, tonnage calculator) + 2 staff operations consoles + GA4 telemetry &amp; SEO metadata.
          </div>
          <div>
            <strong>System 2: OMPI Industrial ERP (33 Modules &bull; On-Premise Office LAN):</strong><br>
            Deployed on dedicated Pune headquarters host PC across internal Gigabit LAN (zero cloud SaaS fees, absolute privacy of Italian landed costs/margins). 18 Core Business Modules (Phase 2) + 15 Workshop &amp; Executive Consoles (Phase 3).
          </div>
        </div>
      </div>

      <!-- 2. Realistic 8-Month Phasing Timeline Table -->
      <div style="background:#f8fafc; border:1.5px solid #cbd5e1; border-radius:7px; padding:12px 16px; margin-bottom:10px;">
        <div style="font-size:9.0pt; font-weight:800; color:#0f172a; text-transform:uppercase; margin-bottom:4px;">
          2. Master Phasing Schedule &bull; 8 Months Total Duration (32 Calendar Weeks)
        </div>
        <table style="width:100%; border-collapse:collapse; font-size:8.1pt; line-height:1.36; color:#334155;">
          <thead>
            <tr style="background:#0f172a; color:#ffffff; text-align:left;">
              <th style="padding:5px 8px;">Milestone Phase</th>
              <th style="padding:5px 8px;">Scope of Deliverables</th>
              <th style="padding:5px 8px;">Target Schedule</th>
              <th style="padding:5px 8px;">Status / Milestone Gate</th>
            </tr>
          </thead>
          <tbody>
            <tr style="border-bottom:1px solid #e2e8f0; background:#ffffff;">
              <td style="padding:5px 8px; font-weight:700;">Phase 1: Dalal Platform</td>
              <td style="padding:5px 8px;">22 Public Pages &bull; 2 Staff Desks &bull; Core Quoting Engine &bull; GA4 / SEO</td>
              <td style="padding:5px 8px; font-weight:600; color:#0f172a;">Weeks 1–8 (Months 1–2)</td>
              <td style="padding:5px 8px; font-weight:700; color:#b45309;">TO COMMENCE UPON ADVANCE</td>
            </tr>
            <tr style="border-bottom:1px solid #e2e8f0; background:#f8fafc;">
              <td style="padding:5px 8px; font-weight:700;">Phase 2: OMPI Core ERP</td>
              <td style="padding:5px 8px;">Modules 01–18 (Italian Catalog, Sizing, Landed Costing, Pune Godown, OMPI Quotes)</td>
              <td style="padding:5px 8px; font-weight:600; color:#0f172a;">Weeks 9–20 (Months 3–5)</td>
              <td style="padding:5px 8px; font-weight:600; color:#475569;">MONTHS 3–5 IMPLEMENTATION</td>
            </tr>
            <tr style="background:#ffffff;">
              <td style="padding:5px 8px; font-weight:700;">Phase 3: Operations &amp; Exec</td>
              <td style="padding:5px 8px;">Modules 19–33 (Job Cards, GST Billing, Shipping Tracker, MD Desk, 4 Workspaces)</td>
              <td style="padding:5px 8px; font-weight:600; color:#0f172a;">Weeks 21–32 (Months 6–8)</td>
              <td style="padding:5px 8px; font-weight:600; color:#475569;">MONTHS 6–8 IMPLEMENTATION</td>
            </tr>
          </tbody>
        </table>
        <div style="font-size:7.8pt; color:#64748b; margin-top:4px;">
          * Note on Module Hierarchy: The master contract references 22 primary business modules; this specification details the full 57-unit operational footprint including all public interfaces, departmental consoles, and compliance tools.
        </div>
      </div>

      <!-- 3. Boundaries, Deemed Acceptance & Client Responsibilities Grid -->
      <div style="display:grid; grid-template-columns:1fr 1fr; gap:9px; margin-bottom:10px;">
        <div style="background:#fff1f2; border:1.5px solid #fecdd3; border-radius:7px; padding:11px 14px;">
          <div style="font-size:8.6pt; font-weight:800; color:#9f1239; text-transform:uppercase; margin-bottom:3px;">
            3. Exclusions &amp; Direct Client Costs
          </div>
          <ul style="font-size:8.0pt; line-height:1.38; color:#4c0519; padding-left:13px; margin:0;">
            <li>Hardware: Yard CCTV cameras, office PCs, UPS, barcode scanners.</li>
            <li>Third-party subscriptions: WhatsApp Meta fees, GST API, cloud hosting, corporate domain/email (registered in Client's name).</li>
            <li>Content production: Machinery photography, video shoots, CA-vetted legal text.</li>
          </ul>
        </div>
        <div style="background:#eff6ff; border:1.5px solid #bfdbfe; border-radius:7px; padding:11px 14px;">
          <div style="font-size:8.6pt; font-weight:800; color:#1e40af; text-transform:uppercase; margin-bottom:3px;">
            4. Client Inputs &amp; 7-Day Acceptance Gate
          </div>
          <ul style="font-size:8.0pt; line-height:1.38; color:#1e3a8a; padding-left:13px; margin:0;">
            <li>Client deliverables: Machine specs, photos, Italian catalog spreadsheets.</li>
            <li>Timeline Clock: Schedule begins upon advance + initial data; client delays extend milestone dates automatically on a day-for-day basis.</li>
            <li><strong>7-Day Deemed Acceptance:</strong> Written punch-list required within 7 days of demo; absence of notice constitutes formal milestone acceptance and activates 30-day warranty.</li>
          </ul>
        </div>
      </div>

      <!-- 4. Shared Quoting, Backup & Legal Liability Box -->
      <div style="background:#ffffff; border:1.5px solid #cbd5e1; border-radius:7px; padding:10px 14px; margin-bottom:10px;">
        <div style="font-size:8.6pt; font-weight:800; color:#0f172a; text-transform:uppercase; margin-bottom:3px; border-bottom:1.5px solid #f1f5f9; padding-bottom:2px;">
          5. Core Governance, Shared Quoting &amp; Code Ownership
        </div>
        <div style="display:grid; grid-template-columns:1fr 1fr; gap:9px; font-size:8.0pt; line-height:1.36; color:#334155;">
          <div>
            <strong>Cross-Entity Shared Quoting:</strong> Dalal (Unit 11/24) and OMPI (MOD-04) utilize a shared quotation engine architecture, but strictly enforce isolated company letterheads, distinct quotation numbering, and separate bank remittance details.
          </div>
          <div>
            <strong>Code Ownership &amp; Liability:</strong> Joint and several commercial liability across entities. 100% custom code owned by Client upon settlement, excluding third-party open-source libraries and Consultant's reusable generic UI framework.
          </div>
        </div>
      </div>

      <!-- Commercial Governance Note -->
      <div style="background:#f8fafc; border:1.5px solid #0f172a; border-radius:7px; padding:8px 14px;">
        <div style="font-size:8.4pt; font-weight:800; color:#0f172a; text-transform:uppercase; margin-bottom:2px;">
          Scope Blueprint Approval &bull; Annexure A to Master Services Agreement
        </div>
        <p style="font-size:7.9pt; line-height:1.36; color:#334155; margin:0;">
          This 57-unit master blueprint defines the functional scope of work (Annexure A). Commercial fee milestones, payment schedules, and legal terms shall be governed by the formal Master Services Agreement. Any feature not detailed herein shall be estimated separately under formal change order (CR) procedures.
        </p>
      </div>
    </div>
    {make_footer(2)}
  </div>
"""'''

text = text.replace(old_p2, new_p2)

# -------------------------------------------------------------
# 6. Update PAGE 3: Assumptions, Exclusions, 3-Tier Backup & Legal Protections
# -------------------------------------------------------------
old_p3 = '''    # PAGE 3: ASSUMPTIONS, EXCLUSIONS & THIRD-PARTY COSTS (NEW)
    html += f"""
  <div class="page">
    <div class="page-content">
      {make_header("GOVERNANCE &bull; ASSUMPTIONS, EXCLUSIONS &amp; CLIENT RESPONSIBILITIES")}

      <div class="section-header">
        <span class="section-title">Commercial Boundaries, External Subscriptions &amp; Technical Assumptions</span>
        <span class="section-tag">Legal &amp; Operational Boundaries</span>
      </div>

      <!-- 1. Third Party Subscriptions Box -->
      <div style="background:#ffffff; border:1.5px solid #cbd5e1; border-radius:7px; padding:15px 18px; margin-bottom:13px;">
        <div style="font-size:9.0pt; font-weight:800; color:#0f172a; text-transform:uppercase; margin-bottom:4px; border-bottom:1.5px solid #f1f5f9; padding-bottom:3px;">
          1. Third-Party API Subscriptions &amp; Cloud Expenses (Client Direct Account)
        </div>
        <p style="font-size:8.3pt; line-height:1.4; color:#475569; margin-bottom:6px;">
          The software suite connects to official external services. All third-party subscription fees, usage charges, and government gateway fees are payable directly by the Client (Dalal / OMPI):
        </p>
        <div style="display:grid; grid-template-columns:1fr 1fr; gap:8px; font-size:8.2pt; line-height:1.38; color:#334155;">
          <div style="background:#f8fafc; padding:8px 12px; border-radius:4px; border-left:3px solid #0284c7;">
            <strong>WhatsApp Business API:</strong> Meta conversation usage fees for automated proposal dispatch and inquiry notifications.
          </div>
          <div style="background:#f8fafc; padding:8px 12px; border-radius:4px; border-left:3px solid #0284c7;">
            <strong>GST / E-Way Bill Gateway:</strong> Third-party GSP/ASP API subscription required for automated 15-digit GSTIN portal validation.
          </div>
          <div style="background:#f8fafc; padding:8px 12px; border-radius:4px; border-left:3px solid #0284c7;">
            <strong>Cloud Hosting &amp; Backups:</strong> Secure cloud server hosting (Render / AWS), managed PostgreSQL database, and cloud backup storage.
          </div>
          <div style="background:#f8fafc; padding:8px 12px; border-radius:4px; border-left:3px solid #0284c7;">
            <strong>Corporate Domain &amp; Email:</strong> Domain name renewal, DNS management, and business email services (Google Workspace / Microsoft 365).
          </div>
        </div>
      </div>

      <!-- 2. Hardware Exclusions Box -->
      <div style="background:#ffffff; border:1.5px solid #cbd5e1; border-radius:7px; padding:15px 18px; margin-bottom:13px;">
        <div style="font-size:9.0pt; font-weight:800; color:#0f172a; text-transform:uppercase; margin-bottom:4px; border-bottom:1.5px solid #f1f5f9; padding-bottom:3px;">
          2. Hardware &amp; Physical Infrastructure Exclusions
        </div>
        <div style="display:grid; grid-template-columns:1fr 1fr; gap:8px; font-size:8.3pt; line-height:1.38; color:#334155;">
          <div style="background:#f8fafc; padding:8px 12px; border-radius:4px; border-left:3px solid #d97706;">
            <strong>Live Stockyard Camera (Unit 17):</strong> CCTV cameras, DVR/NVR hardware, optical fiber internet, and static IP streaming setup at Pune yard are 100% Client's responsibility. Software provides the secure viewing interface.
          </div>
          <div style="background:#f8fafc; padding:8px 12px; border-radius:4px; border-left:3px solid #d97706;">
            <strong>Warehouse Equipment:</strong> Physical barcode label printers, handheld scanning guns, office computers, and local Wi-Fi equipment are excluded from software scope.
          </div>
        </div>
      </div>

      <!-- 3. Client Content & Data Responsibilities -->
      <div style="background:#ffffff; border:1.5px solid #cbd5e1; border-radius:7px; padding:14px 18px; margin-bottom:12px;">
        <div style="font-size:9.0pt; font-weight:800; color:#0f172a; text-transform:uppercase; margin-bottom:4px; border-bottom:1.5px solid #f1f5f9; padding-bottom:3px;">
          3. Content, Data &amp; Legal Text Responsibilities (Client Deliverables)
        </div>
        <p style="font-size:8.4pt; line-height:1.45; color:#334155;">
          The timely delivery of the software suite depends on the Client providing required business assets: (a) High-resolution machinery photographs, nameplate specifications, and power trial video links for Pune stock; (b) Italian OMPI catalog spreadsheets, technical dimensional diagrams, and price cross-indexes; (c) High Seas Sales agreements and legal declaration text vetted by the Client's chartered accountant or maritime trade counsel.
        </p>
      </div>

      <!-- 4. Data Security & Backup Governance -->
      <div style="background:#ffffff; border:1.5px solid #cbd5e1; border-radius:7px; padding:13px 18px; margin-bottom:12px;">
        <div style="font-size:9.0pt; font-weight:800; color:#0f172a; text-transform:uppercase; margin-bottom:4px; border-bottom:1.5px solid #f1f5f9; padding-bottom:3px;">
          4. Data Privacy, Cloud Security &amp; Daily Automated Backup SLA
        </div>
        <p style="font-size:8.4pt; line-height:1.45; color:#334155;">
          All business databases, customer lead history, and commercial quotations are stored in an encrypted PostgreSQL relational database. Daily automated snapshots are executed at midnight with a 30-day version retention policy. Production environments enforce role-based permission boundaries so internal landing costs and margin spreadsheets remain strictly restricted to executive management.
        </p>
      </div>

      <!-- 5. Change Control, Warranty & Source Code Ownership -->
      <div style="background:#f8fafc; border:1.5px solid #0f172a; border-radius:7px; padding:14px 18px;">
        <div style="font-size:9.0pt; font-weight:800; color:#0f172a; text-transform:uppercase; margin-bottom:4px;">
          5. Change Request Policy, Warranty &amp; Source Code Ownership
        </div>
        <div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:8px; font-size:8.1pt; line-height:1.38; color:#334155;">
          <div>
            <strong>Change Request Policy:</strong><br>
            Features not detailed in this 57-unit blueprint will be scoped and billed under a formal Change Order (CR).
          </div>
          <div>
            <strong>30-Day Post-Launch Warranty:</strong><br>
            Includes 30 calendar days of bug-fixing support after milestone release. Ongoing maintenance available via AMC.
          </div>
          <div>
            <strong>100% Code Ownership:</strong><br>
            Full intellectual property and complete source code ownership transfer to Client upon full commercial settlement.
          </div>
        </div>
      </div>
    </div>
    {make_footer(3)}
  </div>
"""'''

new_p3 = '''    # PAGE 3: ASSUMPTIONS, EXCLUSIONS, 3-TIER BACKUP & GOVERNANCE
    html += f"""
  <div class="page">
    <div class="page-content">
      {make_header("GOVERNANCE &bull; ASSUMPTIONS, EXCLUSIONS &amp; CLIENT RESPONSIBILITIES")}

      <div class="section-header">
        <span class="section-title">Operational Infrastructure, Third-Party Subscriptions &amp; Commercial Assumptions</span>
        <span class="section-tag">Commercial Boundaries</span>
      </div>

      <!-- 1. Infrastructure & Third-Party Subscriptions Box -->
      <div style="background:#ffffff; border:1.5px solid #cbd5e1; border-radius:7px; padding:11px 15px; margin-bottom:9px;">
        <div style="font-size:8.8pt; font-weight:800; color:#0f172a; text-transform:uppercase; margin-bottom:3px; border-bottom:1.5px solid #f1f5f9; padding-bottom:2px;">
          1. Hosting Infrastructure &amp; Third-Party Subscriptions (Client Direct Accounts)
        </div>
        <p style="font-size:7.9pt; line-height:1.36; color:#475569; margin-bottom:5px;">
          To ensure client independence and zero markups, all cloud hosting, corporate domains, and API services shall be registered directly in the Client's legal name (Dalal / OMPI). Subscription and usage charges are paid directly by Client:
        </p>
        <div style="display:grid; grid-template-columns:1fr 1fr; gap:7px; font-size:7.9pt; line-height:1.34; color:#334155;">
          <div style="background:#f8fafc; padding:6px 10px; border-radius:4px; border-left:3px solid #0284c7;">
            <strong>Dalal Website Cloud Hosting:</strong> Scalable cloud hosting (AWS / Render) &amp; domain DNS (website address routing).
          </div>
          <div style="background:#f8fafc; padding:6px 10px; border-radius:4px; border-left:3px solid #0284c7;">
            <strong>OMPI ERP On-Premise LAN Setup:</strong> Dedicated Pune office host PC &amp; UPS power (zero third-party cloud hosting fees).
          </div>
          <div style="background:#f8fafc; padding:6px 10px; border-radius:4px; border-left:3px solid #0284c7;">
            <strong>WhatsApp Business API:</strong> Meta conversation usage fees for automated proposal dispatch and inquiry notifications.
          </div>
          <div style="background:#f8fafc; padding:6px 10px; border-radius:4px; border-left:3px solid #0284c7;">
            <strong>GST / E-Way Bill Gateway:</strong> GSP/ASP subscription (government portal integration partner) if automated portal lookup is selected.
          </div>
          <div style="background:#f8fafc; padding:6px 10px; border-radius:4px; border-left:3px solid #0284c7;">
            <strong>Euro Exchange Rate Feed:</strong> Manual daily rate entry included; optional live Forex API subscription if real-time feed desired.
          </div>
          <div style="background:#f8fafc; padding:6px 10px; border-radius:4px; border-left:3px solid #0284c7;">
            <strong>Shipping Container Tracking:</strong> Manual Bill of Lading (BL) logging included; automated shipping line API feeds subject to carrier subscription.
          </div>
        </div>
      </div>

      <!-- 2. Hardware Exclusions Box -->
      <div style="background:#ffffff; border:1.5px solid #cbd5e1; border-radius:7px; padding:10px 15px; margin-bottom:9px;">
        <div style="font-size:8.8pt; font-weight:800; color:#0f172a; text-transform:uppercase; margin-bottom:3px; border-bottom:1.5px solid #f1f5f9; padding-bottom:2px;">
          2. Hardware &amp; Physical Yard Infrastructure Exclusions
        </div>
        <div style="display:grid; grid-template-columns:1fr 1fr; gap:7px; font-size:7.9pt; line-height:1.34; color:#334155;">
          <div style="background:#f8fafc; padding:6px 10px; border-radius:4px; border-left:3px solid #d97706;">
            <strong>Live Stockyard Camera (Unit 17):</strong> CCTV cameras, DVR/NVR hardware, optical fiber internet, and static IP streaming setup at Pune yard are 100% Client's responsibility. Software provides the secure viewing interface.
          </div>
          <div style="background:#f8fafc; padding:6px 10px; border-radius:4px; border-left:3px solid #d97706;">
            <strong>Warehouse Equipment:</strong> Physical barcode label printers, handheld RF scanning guns, office computers, and local Wi-Fi equipment are excluded from software scope.
          </div>
        </div>
      </div>

      <!-- 3. Client Content & Day-for-Day Timeline Delays -->
      <div style="background:#ffffff; border:1.5px solid #cbd5e1; border-radius:7px; padding:10px 15px; margin-bottom:9px;">
        <div style="font-size:8.8pt; font-weight:800; color:#0f172a; text-transform:uppercase; margin-bottom:3px; border-bottom:1.5px solid #f1f5f9; padding-bottom:2px;">
          3. Client Content Deliverables &amp; Timeline Clock Rules
        </div>
        <p style="font-size:8.0pt; line-height:1.38; color:#334155; margin:0;">
          The development schedule clock commences strictly upon receipt of the agreed milestone advance remittance AND client baseline data: (a) Machine photographs, nameplate specs, and power trial video links; (b) Italian OMPI catalog spreadsheets and pricing formulas; (c) High Seas Sales contracts vetted by Client's chartered accountant. <strong>Any delay in client-provided materials automatically extends subsequent milestone target dates on a day-for-day basis.</strong>
        </p>
      </div>

      <!-- 4. Defined 3-Tier Rolling Backup Architecture -->
      <div style="background:#ffffff; border:1.5px solid #cbd5e1; border-radius:7px; padding:10px 15px; margin-bottom:9px;">
        <div style="font-size:8.8pt; font-weight:800; color:#0f172a; text-transform:uppercase; margin-bottom:3px; border-bottom:1.5px solid #f1f5f9; padding-bottom:2px;">
          4. Defined 3-Tier Rolling Backup Architecture &amp; Data Privacy
        </div>
        <p style="font-size:7.9pt; line-height:1.36; color:#334155; margin-bottom:4px;">
          All business records, customer lead history, and commercial quotations are stored in an encrypted PostgreSQL/SQLite database (secured business database). Data protection follows a 3-tier rolling backup strategy (subject to local PC hardware, UPS power, and cloud storage plan maintained by Client):
        </p>
        <div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:6px; font-size:7.8pt; line-height:1.32; color:#334155;">
          <div style="background:#f8fafc; padding:5px 8px; border-radius:4px; border-left:2.5px solid #059669;">
            <strong>Tier 1 (Host Snapshot):</strong> Daily automated local database backup snapshot on host server at midnight.
          </div>
          <div style="background:#f8fafc; padding:5px 8px; border-radius:4px; border-left:2.5px solid #059669;">
            <strong>Tier 2 (LAN Mirror / NAS):</strong> Weekly automated synchronization to a secondary office machine or local network storage.
          </div>
          <div style="background:#f8fafc; padding:5px 8px; border-radius:4px; border-left:2.5px solid #059669;">
            <strong>Tier 3 (Cloud Archive):</strong> Monthly encrypted off-site cloud snapshot (subject to Client's cloud storage account).
          </div>
        </div>
      </div>

      <!-- 5. Change Control, 7-Day Deemed Acceptance, Warranty & Code Ownership -->
      <div style="background:#f8fafc; border:1.5px solid #0f172a; border-radius:7px; padding:10px 15px;">
        <div style="font-size:8.8pt; font-weight:800; color:#0f172a; text-transform:uppercase; margin-bottom:3px;">
          5. Change Policy, 7-Day Deemed Acceptance, Warranty &amp; Code Ownership
        </div>
        <div style="display:grid; grid-template-columns:1fr 1fr 1fr 1fr; gap:7px; font-size:7.7pt; line-height:1.34; color:#334155;">
          <div>
            <strong>Change Request (CR):</strong><br>
            Features outside this 57-unit blueprint shall be scoped and billed under a formal written Change Order.
          </div>
          <div>
            <strong>7-Day Acceptance:</strong><br>
            Client shall inspect and provide written feedback within 7 calendar days of milestone demo. Absence of notice constitutes formal acceptance.
          </div>
          <div>
            <strong>30-Day Warranty:</strong><br>
            Includes 30 calendar days of bug-fixing support upon milestone acceptance. Ongoing support via annual AMC.
          </div>
          <div>
            <strong>100% Code Ownership:</strong><br>
            Custom application code transfers to Client upon full settlement (excluding open-source libraries and generic UI framework).
          </div>
        </div>
      </div>
    </div>
    {make_footer(3)}
  </div>
"""'''

text = text.replace(old_p3, new_p3)

# -------------------------------------------------------------
# 7. Update PAGE 16: OMPI Architecture Map (Add Phase Mapping column)
# -------------------------------------------------------------
old_p16_table = '''      <!-- 7 Functional Engines Table -->
      <div style="background:#ffffff; border:1.5px solid #cbd5e1; border-radius:7px; padding:12px 15px; margin-bottom:12px;">
        <div style="font-size:9.0pt; font-weight:800; color:#0f172a; text-transform:uppercase; margin-bottom:5px; border-bottom:1.5px solid #f1f5f9; padding-bottom:3px;">
          The 7 Core Operational Engines to be Engineered (Modules 01 to 33)
        </div>
        <table style="width:100%; border-collapse:collapse; font-size:8.4pt; line-height:1.38; color:#334155;">
          <thead>
            <tr style="background:#0f172a; color:#ffffff; text-align:left;">
              <th style="padding:5.5px 8px;">Operational Engine</th>
              <th style="padding:5.5px 8px;">Planned Modules</th>
              <th style="padding:5.5px 8px;">Core Business Responsibility</th>
            </tr>
          </thead>
          <tbody>
            <tr style="border-bottom:1px solid #e2e8f0; background:#ffffff;">
              <td style="padding:5.5px 8px; font-weight:700; color:#0f172a;">Engine 1: Sales &amp; Customer Mgmt</td>
              <td style="padding:5.5px 8px; font-weight:600; color:#b45309;">Modules 01 to 06</td>
              <td style="padding:5.5px 8px;">Client records, Italian SKU master, fast quotation generator, deal visual board.</td>
            </tr>
            <tr style="border-bottom:1px solid #e2e8f0; background:#f8fafc;">
              <td style="padding:5.5px 8px; font-weight:700; color:#0f172a;">Engine 2: Inventory &amp; Godown</td>
              <td style="padding:5.5px 8px; font-weight:600; color:#b45309;">Modules 07 to 12</td>
              <td style="padding:5.5px 8px;">Pune live stock, container tracking, restocking alerts, warehouse shelf bin coordinates.</td>
            </tr>
            <tr style="border-bottom:1px solid #e2e8f0; background:#ffffff;">
              <td style="padding:5.5px 8px; font-weight:700; color:#0f172a;">Engine 3: Procurement &amp; Costing</td>
              <td style="padding:5.5px 8px; font-weight:600; color:#b45309;">Modules 13 to 16</td>
              <td style="padding:5.5px 8px;">Italy POs in Euros, port storage milestone tracker, landed cost sheet, vendor logs.</td>
            </tr>
            <tr style="border-bottom:1px solid #e2e8f0; background:#f8fafc;">
              <td style="padding:5.5px 8px; font-weight:700; color:#0f172a;">Engine 4: Workshop &amp; Overhauls</td>
              <td style="padding:5.5px 8px; font-weight:600; color:#b45309;">Modules 17 to 20</td>
              <td style="padding:5.5px 8px;">Job cards, clutch retrofit instructions, pre-dispatch geometry sheets, site handovers.</td>
            </tr>
            <tr style="border-bottom:1px solid #e2e8f0; background:#ffffff;">
              <td style="padding:5.5px 8px; font-weight:700; color:#0f172a;">Engine 5: Accounting &amp; GST</td>
              <td style="padding:5.5px 8px; font-weight:600; color:#b45309;">Modules 21 to 25</td>
              <td style="padding:5.5px 8px;">GST tax invoices, customer payment aging, overseas wire records, monthly margins.</td>
            </tr>
            <tr style="border-bottom:1px solid #e2e8f0; background:#f8fafc;">
              <td style="padding:5.5px 8px; font-weight:700; color:#0f172a;">Engine 6: Sales Operations &amp; AMC</td>
              <td style="padding:5.5px 8px; font-weight:600; color:#b45309;">Modules 26 to 30</td>
              <td style="padding:5.5px 8px;">Field visit logs, quote follow-ups, AMC maintenance contracts, breakdown desk.</td>
            </tr>
            <tr style="background:#ffffff;">
              <td style="padding:5.5px 8px; font-weight:700; color:#0f172a;">Engine 7: Executive Intelligence</td>
              <td style="padding:5.5px 8px; font-weight:600; color:#b45309;">Modules 31 to 33</td>
              <td style="padding:5.5px 8px;">Staff role permissions, daily automated cloud backups, MD real-time command desk.</td>
            </tr>
          </tbody>
        </table>
      </div>'''

new_p16_table = '''      <!-- 7 Functional Engines Table with Exact Phase Mapping -->
      <div style="background:#ffffff; border:1.5px solid #cbd5e1; border-radius:7px; padding:14px 18px; margin-bottom:12px;">
        <div style="font-size:9.2pt; font-weight:800; color:#0f172a; text-transform:uppercase; margin-bottom:5px; border-bottom:1.5px solid #f1f5f9; padding-bottom:3px;">
          The 7 Core Operational Engines &bull; Exact Phased Milestone Mapping (Modules 01 to 33)
        </div>
        <table style="width:100%; border-collapse:collapse; font-size:8.3pt; line-height:1.4; color:#334155;">
          <thead>
            <tr style="background:#0f172a; color:#ffffff; text-align:left;">
              <th style="padding:6px 9px;">Operational Engine</th>
              <th style="padding:6px 9px;">Planned Modules</th>
              <th style="padding:6px 9px;">Delivery Milestone</th>
              <th style="padding:6px 9px;">Core Business Responsibility</th>
            </tr>
          </thead>
          <tbody>
            <tr style="border-bottom:1px solid #e2e8f0; background:#ffffff;">
              <td style="padding:6px 9px; font-weight:700; color:#0f172a;">Engine 1: Sales &amp; Customers</td>
              <td style="padding:6px 9px; font-weight:600; color:#b45309;">Modules 01 to 06</td>
              <td style="padding:6px 9px; font-weight:700; color:#0369a1;">Phase 2 (Wks 9–20)</td>
              <td style="padding:6px 9px;">Customer master, Italian catalog, OMPI proposal generator, deal board.</td>
            </tr>
            <tr style="border-bottom:1px solid #e2e8f0; background:#f8fafc;">
              <td style="padding:6px 9px; font-weight:700; color:#0f172a;">Engine 2: Godown &amp; Inventory</td>
              <td style="padding:6px 9px; font-weight:600; color:#b45309;">Modules 07 to 12</td>
              <td style="padding:6px 9px; font-weight:700; color:#0369a1;">Phase 2 (Wks 9–20)</td>
              <td style="padding:6px 9px;">Pune warehouse stock, manual container logging, safety stock, bin coordinates.</td>
            </tr>
            <tr style="border-bottom:1px solid #e2e8f0; background:#ffffff;">
              <td style="padding:6px 9px; font-weight:700; color:#0f172a;">Engine 3: Procurement &amp; Landed</td>
              <td style="padding:6px 9px; font-weight:600; color:#b45309;">Modules 13 to 16</td>
              <td style="padding:6px 9px; font-weight:700; color:#0369a1;">Phase 2 (Wks 9–20)</td>
              <td style="padding:6px 9px;">Italy POs in Euros, port storage countdown, landed cost sheet, vendor logs.</td>
            </tr>
            <tr style="border-bottom:1px solid #e2e8f0; background:#f8fafc;">
              <td style="padding:6px 9px; font-weight:700; color:#0f172a;">Engine 4: Workshop &amp; Overhaul</td>
              <td style="padding:6px 9px; font-weight:600; color:#b45309;">Modules 17 to 20</td>
              <td style="padding:6px 9px; font-weight:700; color:#7c3aed;">Phase 2 &amp; Phase 3</td>
              <td style="padding:6px 9px;">Mod 17–18: Phase 2 (Retrofit guides) &bull; Mod 19–20: Phase 3 (Job cards &amp; geometry).</td>
            </tr>
            <tr style="border-bottom:1px solid #e2e8f0; background:#ffffff;">
              <td style="padding:6px 9px; font-weight:700; color:#0f172a;">Engine 5: Accounting &amp; GST</td>
              <td style="padding:6px 9px; font-weight:600; color:#b45309;">Modules 21 to 25</td>
              <td style="padding:6px 9px; font-weight:700; color:#047857;">Phase 3 (Wks 21–32)</td>
              <td style="padding:6px 9px;">GST tax billing, customer aging ledger, import duty ledger, entity margin segregation.</td>
            </tr>
            <tr style="border-bottom:1px solid #e2e8f0; background:#f8fafc;">
              <td style="padding:6px 9px; font-weight:700; color:#0f172a;">Engine 6: Sales Ops &amp; Service</td>
              <td style="padding:6px 9px; font-weight:600; color:#b45309;">Modules 26 to 30</td>
              <td style="padding:6px 9px; font-weight:700; color:#047857;">Phase 3 (Wks 21–32)</td>
              <td style="padding:6px 9px;">Inquiry management, proposal follow-up alerts, warranty tracker, breakdown desk.</td>
            </tr>
            <tr style="background:#ffffff;">
              <td style="padding:6px 9px; font-weight:700; color:#0f172a;">Engine 7: Executive Intelligence</td>
              <td style="padding:6px 9px; font-weight:600; color:#b45309;">Modules 31 to 33</td>
              <td style="padding:6px 9px; font-weight:700; color:#047857;">Phase 3 (Wks 21–32)</td>
              <td style="padding:6px 9px;">Staff role permissions, 3-tier rolling backup routines, MD executive control desk.</td>
            </tr>
          </tbody>
        </table>
      </div>'''

text = text.replace(old_p16_table, new_p16_table)

# -------------------------------------------------------------
# 8. Update PAGE 33: Departmental Workspaces box
# -------------------------------------------------------------
old_p33_badge = '''          <div style="font-size:7.8pt; color:#b45309; background:#fffbeb; padding:2px 8px; border:1px solid #fef3c7; border-radius:3px; font-weight:700;">
            Departmental Workspaces
          </div>'''

new_p33_badge = '''          <div style="font-size:7.8pt; color:#047857; background:#ecfdf5; padding:2px 8px; border:1px solid #a7f3d0; border-radius:3px; font-weight:700;">
            Phase 3: Departmental Workspaces (Weeks 21–32)
          </div>'''

text = text.replace(old_p33_badge, new_p33_badge)

# -------------------------------------------------------------
# 9. Update PAGE 34: 8-Month Schedule, Deemed Acceptance, Dual Sign-off with Title Fix
# -------------------------------------------------------------
old_p34_phasing = '''      <!-- Phasing Table -->
      <div style="background:#f8fafc; border:1.5px solid #cbd5e1; border-radius:7px; padding:14px 18px; margin-bottom:14px;">
        <div style="font-size:9.2pt; font-weight:800; color:#0f172a; text-transform:uppercase; margin-bottom:6px;">
          Delivery Milestones &amp; Implementation Phasing
        </div>
        <table style="width:100%; border-collapse:collapse; font-size:8.4pt; line-height:1.42; color:#334155;">
          <thead>
            <tr style="background:#0f172a; color:#ffffff; text-align:left;">
              <th style="padding:7px 10px;">Milestone Phase</th>
              <th style="padding:7px 10px;">Scope of Deliverables</th>
              <th style="padding:7px 10px;">Estimated Duration</th>
              <th style="padding:7px 10px;">Status</th>
            </tr>
          </thead>
          <tbody>
            <tr style="border-bottom:1px solid #e2e8f0; background:#ffffff;">
              <td style="padding:7px 10px; font-weight:700;">Phase 1: Dalal Platform</td>
              <td style="padding:7px 10px;">22 Public Web Pages &bull; 2 Staff Desks &bull; WhatsApp Lead Routing &bull; Quoting Tools</td>
              <td style="padding:7px 10px; font-weight:600;">4 to 6 Weeks</td>
              <td style="padding:7px 10px; font-weight:700; color:#b45309;">TO COMMENCE UPON SIGN-OFF</td>
            </tr>
            <tr style="border-bottom:1px solid #e2e8f0; background:#f8fafc;">
              <td style="padding:7px 10px; font-weight:700;">Phase 2: OMPI Core ERP</td>
              <td style="padding:7px 10px;">Customer Master &bull; Italian SKU Catalog &bull; Landed Costing &bull; Stock Tracker</td>
              <td style="padding:7px 10px; font-weight:600;">8 to 10 Weeks</td>
              <td style="padding:7px 10px; font-weight:600; color:#475569;">MONTH 2-3 SPRINT</td>
            </tr>
            <tr style="background:#ffffff;">
              <td style="padding:7px 10px; font-weight:700;">Phase 3: Operations &amp; Control</td>
              <td style="padding:7px 10px;">Workshop Overhaul Job Cards &bull; GST Invoicing &bull; Port Tracking &bull; MD Command Desk</td>
              <td style="padding:7px 10px; font-weight:600;">8 to 10 Weeks</td>
              <td style="padding:7px 10px; font-weight:600; color:#475569;">MONTH 4-5 SPRINT</td>
            </tr>
          </tbody>
        </table>
      </div>'''

new_p34_phasing = '''      <!-- Phasing Table (Aligned with 8-Month Roadmap) -->
      <div style="background:#f8fafc; border:1.5px solid #cbd5e1; border-radius:7px; padding:12px 16px; margin-bottom:12px;">
        <div style="font-size:9.0pt; font-weight:800; color:#0f172a; text-transform:uppercase; margin-bottom:5px;">
          Delivery Milestones &amp; Implementation Phasing (8-Month Comprehensive Roadmap)
        </div>
        <table style="width:100%; border-collapse:collapse; font-size:8.2pt; line-height:1.38; color:#334155;">
          <thead>
            <tr style="background:#0f172a; color:#ffffff; text-align:left;">
              <th style="padding:6px 9px;">Milestone Phase</th>
              <th style="padding:6px 9px;">Scope of Deliverables</th>
              <th style="padding:6px 9px;">Planned Schedule</th>
              <th style="padding:6px 9px;">Status</th>
            </tr>
          </thead>
          <tbody>
            <tr style="border-bottom:1px solid #e2e8f0; background:#ffffff;">
              <td style="padding:6px 9px; font-weight:700;">Phase 1: Dalal Platform</td>
              <td style="padding:6px 9px;">22 Public Showroom Pages &bull; 2 Staff Desks &bull; Core Quoting Engine &bull; GA4 / SEO</td>
              <td style="padding:6px 9px; font-weight:600; color:#0f172a;">Weeks 1–8 (Months 1–2)</td>
              <td style="padding:6px 9px; font-weight:700; color:#b45309;">TO COMMENCE UPON ADVANCE</td>
            </tr>
            <tr style="border-bottom:1px solid #e2e8f0; background:#f8fafc;">
              <td style="padding:6px 9px; font-weight:700;">Phase 2: OMPI Core ERP</td>
              <td style="padding:6px 9px;">Modules 01–18 (Italian SKU Catalog, Sizing, Landed Costing, Pune Godown, OMPI Quotes)</td>
              <td style="padding:6px 9px; font-weight:600; color:#0f172a;">Weeks 9–20 (Months 3–5)</td>
              <td style="padding:6px 9px; font-weight:600; color:#475569;">MONTHS 3–5 SPRINT</td>
            </tr>
            <tr style="background:#ffffff;">
              <td style="padding:6px 9px; font-weight:700;">Phase 3: Operations &amp; Control</td>
              <td style="padding:6px 9px;">Modules 19–33 (Job Cards, GST Tax Invoices, Shipping Logger, MD Desk, 4 Consoles)</td>
              <td style="padding:6px 9px; font-weight:600; color:#0f172a;">Weeks 21–32 (Months 6–8)</td>
              <td style="padding:6px 9px; font-weight:600; color:#475569;">MONTHS 6–8 SPRINT</td>
            </tr>
          </tbody>
        </table>
      </div>'''

text = text.replace(old_p34_phasing, new_p34_phasing)

old_p34_disc = '''      <!-- Scope Approval Disclaimer -->
      <div style="background:#ffffff; border:1.5px solid #0f172a; border-radius:7px; padding:13px 18px; margin-bottom:14px;">
        <div style="font-size:8.8pt; font-weight:800; color:#0f172a; text-transform:uppercase; margin-bottom:3px;">
          Scope Blueprint Approval &amp; Agreement Annexure Acknowledgment
        </div>
        <p style="font-size:8.2pt; line-height:1.42; color:#334155;">
          Execution below constitutes mutual formal approval of the functional scope and architecture defined across this 57-unit master specification document (Scope Annexure A). Commercial fees, payment milestones, third-party subscription disbursements, and contractual terms shall be governed exclusively by the formal Master Services Agreement.
        </p>
      </div>'''

new_p34_disc = '''      <!-- Scope Approval & Governance Rules -->
      <div style="background:#ffffff; border:1.5px solid #0f172a; border-radius:7px; padding:11px 16px; margin-bottom:12px;">
        <div style="font-size:8.6pt; font-weight:800; color:#0f172a; text-transform:uppercase; margin-bottom:3px;">
          Scope Blueprint Approval &bull; Annexure A to Master Services Agreement
        </div>
        <p style="font-size:8.0pt; line-height:1.38; color:#334155; margin-bottom:4px;">
          Execution below constitutes mutual formal approval of the functional architecture defined across this 57-unit master specification document (Scope Annexure A). Commercial fees, payment schedules, and liability shall be governed exclusively by the Master Services Agreement (MSA).
        </p>
        <div style="font-size:7.8pt; line-height:1.34; color:#475569; background:#f8fafc; padding:6px 10px; border-radius:4px; border-left:3px solid #0f172a;">
          <strong>Governing Execution Terms:</strong> (1) Schedule clock commences upon advance remittance and initial client data; client delays extend milestone dates day-for-day. (2) <strong>7-Day Deemed Acceptance:</strong> Client shall provide consolidated punch-list feedback within 7 calendar days of milestone delivery demo; absence of notice constitutes formal acceptance and activates the 30-day warranty. (3) <strong>Joint Commercial Liability:</strong> Both corporate entities are jointly committed to commercial terms, whilst maintaining 100% operational, banking, and accounting separation.
        </div>
      </div>'''

text = text.replace(old_p34_disc, new_p34_disc)

old_p34_sigs = '''      <!-- Separate Dual Entity Sign-Off Blocks -->
      <div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:14px; border-top:1.5px solid #0f172a; padding-top:12px;">
        <div style="font-size:8.3pt; line-height:1.4; color:#334155;">
          <strong>Scope Approved for Dalal Agency:</strong><br><br>
          __________________________________<br>
          <strong>Mr. Vinit Dalal</strong> &bull; Managing Director<br>
          <span style="font-size:7.8pt; color:#64748b;">Dalal Machine Tools Agency Pvt. Ltd.</span><br>
          <span style="font-size:7.8pt; color:#475569;">Date: ________________________</span>
        </div>
        <div style="font-size:8.3pt; line-height:1.4; color:#334155;">
          <strong>Scope Approved for OMPI India:</strong><br><br>
          __________________________________<br>
          <strong>Authorized Signatory</strong> &bull; Partner<br>
          <span style="font-size:7.8pt; color:#64748b;">OMPI India LLP</span><br>
          <span style="font-size:7.8pt; color:#475569;">Date: ________________________</span>
        </div>
        <div style="font-size:8.3pt; line-height:1.4; color:#334155; text-align:right;">
          <strong>Submitted by Consultant:</strong><br><br>
          __________________________________<br>
          <strong>Suyash Shinde</strong> &bull; Solutions Architect<br>
          <span style="font-size:7.8pt; color:#64748b;">Pimpri, Pune, Maharashtra</span><br>
          <span style="font-size:7.8pt; color:#475569;">Date: November 02, 2026</span>
        </div>
      </div>'''

new_p34_sigs = '''      <!-- Separate Dual Entity Sign-Off Blocks -->
      <div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:12px; border-top:1.5px solid #0f172a; padding-top:10px;">
        <div style="font-size:8.1pt; line-height:1.36; color:#334155;">
          <strong>Scope Approved for Dalal Agency:</strong><br><br>
          __________________________________<br>
          <strong>Mr. Vinit Dalal</strong> &bull; Managing Director<br>
          <span style="font-size:7.6pt; color:#64748b;">Dalal Machine Tools Agency Pvt. Ltd.</span><br>
          <span style="font-size:7.6pt; color:#475569;">Date: ________________________</span>
        </div>
        <div style="font-size:8.1pt; line-height:1.36; color:#334155;">
          <strong>Scope Approved for OMPI India:</strong><br><br>
          __________________________________<br>
          <strong>Authorized Signatory</strong> &bull; Partner<br>
          <span style="font-size:7.6pt; color:#64748b;">OMPI India LLP</span><br>
          <span style="font-size:7.6pt; color:#475569;">Date: ________________________</span>
        </div>
        <div style="font-size:8.1pt; line-height:1.36; color:#334155; text-align:right;">
          <strong>Submitted by Consultant:</strong><br><br>
          __________________________________<br>
          <strong>Suyash Shinde</strong> &bull; Principal Software Consultant<br>
          <span style="font-size:7.6pt; color:#64748b;">Pimpri, Pune, Maharashtra</span><br>
          <span style="font-size:7.6pt; color:#475569;">Date: November 02, 2026 (Valid thru 14 Nov)</span>
        </div>
      </div>'''

text = text.replace(old_p34_sigs, new_p34_sigs)

# Standardize any remaining "Solutions Architect" in text
text = text.replace('Solutions Architect', 'Principal Software Consultant')

with open('scratch/build_enterprise_specification_v2.py', 'w', encoding='utf-8') as f:
    f.write(text)

print('Successfully applied all Version 2.5 fixes!')

