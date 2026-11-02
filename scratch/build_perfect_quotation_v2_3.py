# scratch/build_perfect_quotation_v2_3.py
import os
import subprocess
import shutil
import fitz

def build_perfect_html():
    css = """
    @page {
      size: A4 portrait;
      margin: 0;
    }
    * {
      box-sizing: border-box;
      -webkit-print-color-adjust: exact;
      print-color-adjust: exact;
    }
    body {
      margin: 0;
      padding: 0;
      font-family: Arial, "Helvetica Neue", Helvetica, sans-serif;
      color: #1f2937;
      background: #e5e7eb;
    }
    .page {
      width: 210mm;
      height: 297mm;
      margin: 0 auto;
      background: #ffffff;
      page-break-after: always;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      position: relative;
    }
    .page-1 {
      padding: 11mm 16mm 10mm 16mm;
      font-size: 8.0pt;
      line-height: 1.32;
    }
    .page-2 {
      padding: 10mm 16mm 9.5mm 16mm;
      font-size: 7.8pt;
      line-height: 1.28;
    }
    .page-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 7.3pt;
      color: #6b7280;
      border-bottom: 1px solid #e5e7eb;
      padding-bottom: 3.5px;
      margin-bottom: 6px;
    }
    .page-footer {
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 7.3pt;
      color: #6b7280;
      border-top: 1px solid #e5e7eb;
      padding-top: 3.5px;
      margin-top: 5px;
    }
    .content-area {
      flex: 1;
      display: flex;
      flex-direction: column;
    }
    h1.doc-title {
      font-size: 15.5pt;
      font-weight: 700;
      color: #17365d;
      margin: 0 0 3px 0;
      line-height: 1.22;
      letter-spacing: -0.2px;
    }
    .doc-meta {
      font-size: 7.6pt;
      line-height: 1.36;
      color: #374151;
      margin-bottom: 6px;
      background: #f8fafc;
      padding: 5px 10px;
      border-radius: 4px;
      border-left: 3.5px solid #17365d;
    }
    h2.section-heading {
      font-size: 9.6pt;
      font-weight: 700;
      color: #17365d;
      border-bottom: 1.5px solid #17365d;
      padding-bottom: 2px;
      margin: 6px 0 4px 0;
      line-height: 1.2;
    }
    .page-2 h2.section-heading {
      font-size: 9.3pt;
      margin: 5px 0 3.0px 0;
      padding-bottom: 1.5px;
    }
    p.section-sub {
      margin: 0 0 4px 0;
      font-size: 7.6pt;
      line-height: 1.30;
      color: #4b5563;
    }
    table.quotation-table {
      width: 100%;
      border-collapse: collapse;
      margin-bottom: 6px;
      font-size: 7.8pt;
      line-height: 1.26;
    }
    .page-2 table.quotation-table {
      margin-bottom: 4.0px;
      font-size: 7.5pt;
      line-height: 1.22;
    }
    table.quotation-table th {
      background: #17365d;
      color: #ffffff;
      font-weight: 700;
      text-align: left;
      padding: 3.6px 6px;
      border: 1px solid #17365d;
      font-size: 7.7pt;
    }
    .page-2 table.quotation-table th {
      padding: 2.8px 5.5px;
      font-size: 7.5pt;
    }
    table.quotation-table td {
      border: 1px solid #d1d5db;
      padding: 3.4px 6px;
      vertical-align: middle;
      color: #1f2937;
    }
    .page-2 table.quotation-table td {
      padding: 2.8px 5.5px;
    }
    table.quotation-table tr:nth-child(even) td {
      background: #f9fafb;
    }
    .col-center {
      text-align: center;
    }
    .col-right {
      text-align: right;
    }
    .col-price {
      text-align: right;
      font-weight: 700;
      font-family: Consolas, "Liberation Mono", Menlo, Courier, monospace;
      font-size: 8.0pt;
      color: #0f172a;
      white-space: nowrap;
    }
    .page-2 .col-price {
      font-size: 7.7pt;
    }
    .subtotal-row td {
      background: #17365d !important;
      color: #ffffff !important;
      font-weight: 700;
      font-size: 8.0pt;
      border: 1px solid #17365d !important;
      padding: 4.0px 6.5px;
    }
    .subtotal-row .col-price {
      color: #ffffff !important;
      font-size: 8.3pt;
    }
    .grand-total-row td {
      background: #047857 !important;
      color: #ffffff !important;
      font-weight: 800;
      font-size: 8.2pt;
      border: 1px solid #047857 !important;
      padding: 3.6px 6.5px;
    }
    .grand-total-row .col-price {
      color: #ffffff !important;
      font-size: 8.5pt;
    }
    .free-badge {
      display: inline-block;
      background: #047857;
      color: #ffffff;
      font-size: 6.8pt;
      font-weight: 700;
      padding: 1.2px 6.0px;
      border-radius: 3px;
      text-transform: uppercase;
      letter-spacing: 0.3px;
      white-space: nowrap;
    }
    .group-tag {
      display: inline-block;
      background: #e0e7ff;
      color: #1e40af;
      font-size: 6.6pt;
      font-weight: 700;
      padding: 1px 4.5px;
      border-radius: 2px;
      margin-right: 4px;
      text-transform: uppercase;
      letter-spacing: 0.2px;
      white-space: nowrap;
      vertical-align: middle;
    }
    .terms-card {
      background: #f8fafc;
      border: 1px solid #e2e8f0;
      border-left: 3.5px solid #17365d;
      border-radius: 4px;
      padding: 6px 9px;
      margin-bottom: 4px;
    }
    ul.terms-list {
      margin: 0;
      padding-left: 14px;
      font-size: 7.2pt;
      line-height: 1.28;
      color: #374151;
    }
    ul.terms-list li {
      margin-bottom: 2.2px;
    }
    ul.terms-list li:last-child {
      margin-bottom: 0;
    }
    ul.terms-list strong {
      color: #17365d;
    }
    .notice-box {
      background: #eff6ff;
      border: 1px solid #bfdbfe;
      border-radius: 4px;
      padding: 4.5px 9px;
      font-size: 7.1pt;
      line-height: 1.26;
      color: #1e40af;
      text-align: center;
    }
    """

    def make_header():
        return """
        <div class="page-header">
          <span>Dalal Machine Tools Agency &amp; OMPI India | Commercial Quotation &bull; v2.3</span>
          <span>REF: QUOTE-2026-DALAL-OMPI-760K</span>
        </div>
        """

    def make_footer(page_num):
        return f"""
        <div class="page-footer">
          <span>Confidential &bull; Commercial Scope, Retainer Schedule &amp; Complimentary Deliverables &bull; Valid Through 14 Nov 2026</span>
          <span>Page {page_num} of 2</span>
        </div>
        """

    # PAGE 1: Modules Breakdown for System 1 & System 2 (Harmonized with Scope doc v2.5)
    p1 = f"""
    <div class="page page-1">
      {make_header()}
      <div class="content-area">
        <h1 class="doc-title">Commercial Quotation: Module-Wise Cost Breakdown</h1>
        <div class="doc-meta">
          <strong>Engagement:</strong> Unified Digital Showroom Platform &amp; OMPI Industrial ERP Suite (57 Total Functional Units)<br>
          <strong>Client Entities:</strong> Dalal Machine Tools Agency Pvt. Ltd. &amp; OMPI India LLP &bull; Attn: <strong>Mr. Vinit Dalal</strong>, Managing Director / Partner<br>
          <strong>Consultant:</strong> Suyash Shinde, Principal Software Consultant, Pune &bull; <strong>Issue Date:</strong> 2 November 2026 &bull; <strong>Validity:</strong> 15 Days (Through 14 Nov 2026)
        </div>

        <h2 class="section-heading">1. System 1: Dalal Machine Tools Agency Pvt. Ltd. (Public Platform &amp; Inbound Engine)</h2>
        <p class="section-sub">Scope: 24 Functional Units (22 Public Showroom Pages + 2 Staff Admin Desks) &bull; Delivery: Weeks 1 to 8 (Months 1 to 2)</p>

        <table class="quotation-table">
          <thead>
            <tr>
              <th style="width: 5%;" class="col-center">No.</th>
              <th style="width: 44%;">Module / Functional Deliverable</th>
              <th style="width: 33%;">Operational Scope &amp; Deliverables Breakdown</th>
              <th style="width: 18%;" class="col-right">Price (INR)</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td class="col-center">1</td>
              <td><strong>Machinery Showroom &amp; Category Catalog</strong></td>
              <td>26 machine categories, stock filters, yard authenticity showcase (6 Units: Routes 01–06)</td>
              <td class="col-price">&#8377; 35,000</td>
            </tr>
            <tr>
              <td class="col-center">2</td>
              <td><strong>Machine Detail Sheets &amp; Video Trials</strong></td>
              <td>Tonnage, stroke, bed specs, unedited running video links per machine (4 Units: Routes 07–10)</td>
              <td class="col-price">&#8377; 30,000</td>
            </tr>
            <tr>
              <td class="col-center">3</td>
              <td><strong>Instant Quotation Engine &amp; WhatsApp Leads</strong></td>
              <td>60-sec formal proposal PDF download + direct WhatsApp lead routing (3 Units: Routes 11–13)</td>
              <td class="col-price">&#8377; 35,000</td>
            </tr>
            <tr>
              <td class="col-center">4</td>
              <td><strong>Press Tonnage &amp; Sizing Assistant</strong></td>
              <td>Interactive component force calculation formula for plant buyers (3 Units: Routes 14–16)</td>
              <td class="col-price">&#8377; 25,000</td>
            </tr>
            <tr>
              <td class="col-center">5</td>
              <td><strong>High Seas Sales &amp; Import FAQs Portal</strong></td>
              <td>Procedural guidance, customs documentation &amp; GST ITC explainers (3 Units: Routes 17–19)</td>
              <td class="col-price">&#8377; 20,000</td>
            </tr>
            <tr>
              <td class="col-center">6</td>
              <td><strong>Company Profile, Stockyard &amp; Visit Booking</strong></td>
              <td>Corporate legacy, Pune yard map, client visit calendar scheduler (3 Units: Routes 20–22)</td>
              <td class="col-price">&#8377; 25,000</td>
            </tr>
            <tr>
              <td class="col-center">7</td>
              <td><strong>Staff Operations Console &amp; RFQ Lead Desk</strong></td>
              <td>Internal machine spec manager, stock toggles, buyer RFQ inbox (2 Units: Admin Desks 23–24)</td>
              <td class="col-price">&#8377; 30,000</td>
            </tr>
            <tr class="subtotal-row">
              <td colspan="3"><strong>SUBTOTAL: SYSTEM 1 (DALAL MACHINE TOOLS AGENCY PVT. LTD. &bull; 24 UNITS)</strong></td>
              <td class="col-price">&#8377; 2,00,000</td>
            </tr>
          </tbody>
        </table>

        <h2 class="section-heading" style="margin-top: 6px;">2. System 2: OMPI India LLP (Industrial Operations &amp; Precision Clutch ERP)</h2>
        <p class="section-sub">Scope: 33 Specialized Operations Modules in 7 Functional Groups &bull; Delivery: Weeks 9 to 32 | 7 Monthly Sprints (Months 3 to 8)</p>

        <table class="quotation-table" style="margin-bottom: 0;">
          <thead>
            <tr>
              <th style="width: 5%;" class="col-center">No.</th>
              <th style="width: 44%;">Functional Group &amp; Module Scope (Scope Doc v2.5 Harmonized)</th>
              <th style="width: 33%;">Operational Scope &amp; Deliverables Breakdown</th>
              <th style="width: 18%;" class="col-right">Price (INR)</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td class="col-center">1</td>
              <td><span class="group-tag">Group 1</span><strong>Sales and Customers</strong></td>
              <td>Customer profiles, 15-digit GSTIN, OMPI catalog, Euro pricing, quick quotes, deal board, press matcher (MOD 01–06: 6 Modules)</td>
              <td class="col-price">&#8377; 1,00,000</td>
            </tr>
            <tr>
              <td class="col-center">2</td>
              <td><span class="group-tag">Group 2</span><strong>Inventory and Godown</strong></td>
              <td>Pune stock tracker, shipments, low-stock alerts, transfer challans, bin locator, trial tracker (MOD 07–12: 6 Modules)</td>
              <td class="col-price">&#8377; 90,000</td>
            </tr>
            <tr>
              <td class="col-center">3</td>
              <td><span class="group-tag">Group 3</span><strong>Procurement and Costing</strong></td>
              <td>International POs, port clearance tracker, landed cost sheet, supplier delivery records (MOD 13–16: 4 Modules)</td>
              <td class="col-price">&#8377; 75,000</td>
            </tr>
            <tr>
              <td class="col-center">4</td>
              <td><span class="group-tag">Group 4</span><strong>Workshop and Overhauls</strong></td>
              <td>Reconditioning job cards, clutch retrofit work orders, pre-dispatch QC sheet, site handover checklist (MOD 17–20: 4 Modules)</td>
              <td class="col-price">&#8377; 70,000</td>
            </tr>
            <tr>
              <td class="col-center">5</td>
              <td><span class="group-tag">Group 5</span><strong>Accounts and GST</strong></td>
              <td>GST tax invoices (CGST/SGST/IGST), payment ledger &amp; ageing, vendor remittances, margins, GST return summary (MOD 21–25: 5 Modules)</td>
              <td class="col-price">&#8377; 85,000</td>
            </tr>
            <tr>
              <td class="col-center">6</td>
              <td><span class="group-tag">Group 6</span><strong>Sales Operations and Service</strong></td>
              <td>Field visit logger, quotation follow-up reminders, maintenance contract ledger, breakdown helpdesk, feedback (MOD 26–30: 5 Modules)</td>
              <td class="col-price">&#8377; 80,000</td>
            </tr>
            <tr>
              <td class="col-center">7</td>
              <td><span class="group-tag">Group 7</span><strong>Control and Security</strong></td>
              <td>Staff access &amp; RBAC permissions, activity audit history &amp; backups, Managing Director's desk (MOD 31–33: 3 Modules)</td>
              <td class="col-price">&#8377; 60,000</td>
            </tr>
            <tr class="subtotal-row">
              <td colspan="3"><strong>SUBTOTAL: SYSTEM 2 (OMPI INDIA LLP &bull; 33 MODULES IN 7 GROUPS)</strong></td>
              <td class="col-price">&#8377; 5,60,000</td>
            </tr>
          </tbody>
        </table>
      </div>
      {make_footer(1)}
    </div>
    """

    # PAGE 2: Total Summary, Complimentary Value, Retainer Plan & Governance
    p2 = f"""
    <div class="page page-2">
      {make_header()}
      <div class="content-area">
        <h2 class="section-heading" style="margin-top: 0;">3. Total Project Investment Summary</h2>
        <table class="quotation-table">
          <thead>
            <tr>
              <th style="width: 32%;">Entity / System</th>
              <th style="width: 38%;">Scope of Deliverables</th>
              <th style="width: 14%;" class="col-center">Schedule</th>
              <th style="width: 16%;" class="col-right">Total (INR)</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><strong>Dalal Machine Tools Agency Pvt. Ltd.</strong></td>
              <td>System 1: Public Machinery Platform &bull; 24 Units</td>
              <td class="col-center">Weeks 1–8</td>
              <td class="col-price">&#8377; 2,00,000</td>
            </tr>
            <tr>
              <td><strong>OMPI India LLP</strong></td>
              <td>System 2: Industrial ERP Management Suite &bull; 33 Modules</td>
              <td class="col-center">Weeks 9–32</td>
              <td class="col-price">&#8377; 5,60,000</td>
            </tr>
            <tr class="grand-total-row">
              <td colspan="3"><strong>TOTAL COMBINED TURNKEY INVESTMENT (57 FUNCTIONAL UNITS)</strong></td>
              <td class="col-price">&#8377; 7,60,000</td>
            </tr>
          </tbody>
        </table>

        <h2 class="section-heading">4. Complimentary Value Deliverables (Included in Fee at &#8377;0 / FREE)</h2>
        <table class="quotation-table">
          <thead>
            <tr>
              <th style="width: 49%;">Complimentary Service / Value Asset</th>
              <th style="width: 27%;">Industry Market Value</th>
              <th style="width: 24%;" class="col-center">Engagement Fee</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><strong>In-Scope Technical Maintenance &amp; Bug Remediation:</strong> Continuous defect remediation for all 57 units across the full 8-month lifecycle + 30-day post-handover warranty.</td>
              <td>&#8377; 2,40,000 (Est.)</td>
              <td class="col-center"><span class="free-badge">INCLUDED (FREE)</span></td>
            </tr>
            <tr>
              <td><strong>On-Premise Local LAN Architecture Setup:</strong> Zero recurring third-party cloud user subscription fees; high-speed office yard local network configuration.</td>
              <td>&#8377; 2,50,000+ / Yr</td>
              <td class="col-center"><span class="free-badge">INCLUDED (FREE)</span></td>
            </tr>
            <tr>
              <td><strong>Staff Onboarding, Role Training &amp; Video Walkthroughs:</strong> 12 hours of structured staff training at Pune yard + comprehensive PDF User Training Manual.</td>
              <td>&#8377; 75,000 (Est.)</td>
              <td class="col-center"><span class="free-badge">INCLUDED (FREE)</span></td>
            </tr>
            <tr>
              <td><strong>Google SEO, AI Search (GEO) /llms.txt &amp; Schema:</strong> Rich search metadata, XML sitemaps, robots.txt &amp; AI-crawler optimization for buyer discovery.</td>
              <td>&#8377; 60,000 (Est.)</td>
              <td class="col-center"><span class="free-badge">INCLUDED (FREE)</span></td>
            </tr>
            <tr>
              <td><strong>Automated 3-Tier Rolling Disaster Recovery:</strong> Automated local and external scheduled database snapshots protecting critical business records.</td>
              <td>&#8377; 40,000 (Est.)</td>
              <td class="col-center"><span class="free-badge">INCLUDED (FREE)</span></td>
            </tr>
            <tr>
              <td><strong>1-Click Excel / CSV Leads &amp; Inventory Exporter:</strong> Instant offline data downloads with column filters &amp; UTF-8 BOM encoding across all tables.</td>
              <td>&#8377; 30,000 (Est.)</td>
              <td class="col-center"><span class="free-badge">INCLUDED (FREE)</span></td>
            </tr>
            <tr style="background: #f0fdf4;">
              <td colspan="2" style="font-weight: 700; color: #065f46;">TOTAL COMPLIMENTARY VALUE DELIVERED TO CLIENT AT ZERO EXTRA CHARGE</td>
              <td class="col-center" style="font-weight: 800; color: #047857; font-size: 7.8pt;">&#8377; 6,95,000+ FREE</td>
            </tr>
          </tbody>
        </table>

        <h2 class="section-heading">5. Agreed Retainer Payment Schedule: &#8377; 2.0L Advance + 7 Monthly Sprints @ &#8377; 80,000/mo</h2>
        <table class="quotation-table">
          <thead>
            <tr>
              <th style="width: 15%;" class="col-center">Sprint / Month</th>
              <th style="width: 49%;">Core Deliverable &amp; Operational Milestone Trigger (Scope Doc v2.5 Aligned)</th>
              <th style="width: 20%;" class="col-center">Invoiced Entity</th>
              <th style="width: 16%;" class="col-right">Amount (INR)</th>
            </tr>
          </thead>
          <tbody>
            <tr style="background: #eff6ff;">
              <td class="col-center"><strong>Advance (M1)</strong></td>
              <td><strong>Contract Execution &amp; Phase 1 Kickoff:</strong> Complete Dalal Web Platform (24 Units: Routes 01–24), Public Showroom, Instant Quoting &amp; WhatsApp Desk</td>
              <td class="col-center" style="font-size: 7.1pt;">Dalal Machine Tools Agency Pvt. Ltd.</td>
              <td class="col-price" style="color: #1e3a8a;">&#8377; 2,00,000</td>
            </tr>
            <tr>
              <td class="col-center"><strong>Month 2</strong></td>
              <td>OMPI Sprint 1 (Group 1: MOD 01–06): Customer Profiles, GSTIN, OMPI Catalog, Euro Pricing, Quick Quotes &amp; Deal Board</td>
              <td class="col-center" style="font-size: 7.1pt;">OMPI India LLP</td>
              <td class="col-price">&#8377; 80,000</td>
            </tr>
            <tr>
              <td class="col-center"><strong>Month 3</strong></td>
              <td>OMPI Sprint 2 (Group 2: MOD 07–12): Pune Stock Tracker, Shipments, Low-Stock Alerts, Transfer Challans &amp; Bin Locator</td>
              <td class="col-center" style="font-size: 7.1pt;">OMPI India LLP</td>
              <td class="col-price">&#8377; 80,000</td>
            </tr>
            <tr>
              <td class="col-center"><strong>Month 4</strong></td>
              <td>OMPI Sprint 3 (Group 3: MOD 13–16): International POs to Italy, Port Clearance Tracker &amp; Landed Cost Calculation Sheet</td>
              <td class="col-center" style="font-size: 7.1pt;">OMPI India LLP</td>
              <td class="col-price">&#8377; 80,000</td>
            </tr>
            <tr>
              <td class="col-center"><strong>Month 5</strong></td>
              <td>OMPI Sprint 4 (Group 4: MOD 17–20): Reconditioning Job Cards, Clutch Retrofit Orders, QC Inspection &amp; Site Handover</td>
              <td class="col-center" style="font-size: 7.1pt;">OMPI India LLP</td>
              <td class="col-price">&#8377; 80,000</td>
            </tr>
            <tr>
              <td class="col-center"><strong>Month 6</strong></td>
              <td>OMPI Sprint 5 (Group 5: MOD 21–25): GST Tax Invoices (CGST/SGST/IGST), Payment Ageing Ledgers &amp; Remittance Tracking</td>
              <td class="col-center" style="font-size: 7.1pt;">OMPI India LLP</td>
              <td class="col-price">&#8377; 80,000</td>
            </tr>
            <tr>
              <td class="col-center"><strong>Month 7</strong></td>
              <td>OMPI Sprint 6 (Group 6: MOD 26–30): Field Visit Logger, Follow-Up Reminders, AMC Ledger &amp; Breakdown Help Desk</td>
              <td class="col-center" style="font-size: 7.1pt;">OMPI India LLP</td>
              <td class="col-price">&#8377; 80,000</td>
            </tr>
            <tr>
              <td class="col-center"><strong>Month 8</strong></td>
              <td>OMPI Sprint 7 (Group 7: MOD 31–33): Staff RBAC Permissions, Backups, Managing Director's Desk &amp; Turnkey Handover</td>
              <td class="col-center" style="font-size: 7.1pt;">OMPI India LLP</td>
              <td class="col-price">&#8377; 80,000</td>
            </tr>
            <tr class="grand-total-row">
              <td colspan="3"><strong>TOTAL ENGAGEMENT INVESTMENT (&#8377; 2,00,000 ADVANCE + 7 &times; &#8377; 80,000)</strong></td>
              <td class="col-price">&#8377; 7,60,000</td>
            </tr>
          </tbody>
        </table>

        <h2 class="section-heading">6. Commercial Terms, Governance &amp; Operational Guidelines</h2>
        <div class="terms-card">
          <ul class="terms-list">
            <li><strong>Separate Corporate Invoicing &amp; Bank Accounts:</strong> Distinct invoices raised for <em>Dalal Machine Tools Agency Pvt. Ltd.</em> (&#8377; 2,00,000) and <em>OMPI India LLP</em> (&#8377; 5,60,000 across 7 monthly sprints @ &#8377; 80,000/mo) for clean tax accounting &amp; direct GST Input Tax Credit (ITC).</li>
            <li><strong>Direct Pass-Through Billing (Zero Agency Markups):</strong> Third-party subscriptions—cloud server hosting (AWS/Render), corporate domains, WhatsApp Cloud API conversations, and government GST portal API gateways—are billed directly to Client accounts at actual cost.</li>
            <li><strong>Project Timeline &amp; Client Content Prerequisite:</strong> The 8-month development cycle commences upon contract execution, mobilization advance clearance, and handover of baseline machine data and media. Client review delays adjust subsequent sprint deadlines proportionally.</li>
            <li><strong>7-Day Deemed Acceptance Governance:</strong> Client shall review sprint demos within 7 calendar days. Absence of a written defect punch-list within 7 days constitutes formal sprint progress sign-off.</li>
            <li><strong>Turnkey Warranty &amp; Source Code Ownership:</strong> Continuous in-scope maintenance covers all delivered modules across the 8-month lifecycle. Following final go-live at Month 8, an umbrella 30-day post-handover warranty covers all 57 units. 100% custom source code and database schema ownership transfer to Client upon completion of final commercial settlement.</li>
          </ul>
        </div>

        <div class="notice-box">
          <strong>Exploratory Quotation Notice:</strong> This breakdown provides indicative commercial scheduling and module costs for budgeting and alignment. Formal commercial contract execution, legal warranties, and intellectual property assignment shall be governed exclusively by the Master Services Agreement (MSA).
        </div>
      </div>
      {make_footer(2)}
    </div>
    """

    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Dalal &amp; OMPI: Module-Wise Commercial Quotation</title>
  <style>{css}</style>
</head>
<body>
  {p1}
  {p2}
</body>
</html>
"""
    return full_html

if __name__ == "__main__":
    html_content = build_perfect_html()
    output_html = "DALAL_AND_OMPI_COMMERCIAL_QUOTATION_BREAKDOWN.html"
    with open(output_html, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Generated HTML: {output_html} ({len(html_content):,} bytes)")

    output_pdf = "DALAL_AND_OMPI_COMMERCIAL_QUOTATION_BREAKDOWN.pdf"
    edge_paths = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"
    ]
    edge_bin = next(p for p in edge_paths if os.path.exists(p))

    abs_html = os.path.abspath(output_html)
    abs_pdf = os.path.abspath(output_pdf)
    cmd = [
        edge_bin,
        "--headless=new",
        "--disable-gpu",
        "--run-all-compositor-stages-before-draw",
        "--no-pdf-header-footer",
        f"--print-to-pdf={abs_pdf}",
        f"file:///{abs_html}"
    ]
    print("Rendering Commercial Quotation PDF via Edge...")
    subprocess.run(cmd, check=True)
    print(f"PDF Generated: {abs_pdf} ({os.path.getsize(abs_pdf):,} bytes)")

    # Audit with PyMuPDF
    doc = fitz.open(abs_pdf)
    print(f"--- PyMuPDF Audit: Total Pages = {len(doc)} ---")
    for i, page in enumerate(doc):
        rect = page.rect
        blocks = page.get_text("blocks")
        bottom_most = 0
        for b in blocks:
            if b[4].strip() and "Page " not in b[4] and "Confidential" not in b[4]:
                if b[3] > bottom_most:
                    bottom_most = b[3]
        gap = rect.height - bottom_most
        print(f"Page {i+1:02d}: bottom content y={bottom_most:.1f} | page height={rect.height:.1f} | gap={gap:.1f}pt")
        pix = page.get_pixmap(dpi=150)
        pix.save(f"scratch/quotation_page_{i+1:02d}.png")

    # Sync to artifacts
    art_dir = r"C:\Users\91940\.gemini\antigravity\brain\75a30f5c-ccbc-43b7-9b59-6c8c1ab99b62"
    for fname in [output_html, output_pdf]:
        dst = os.path.join(art_dir, fname)
        shutil.copyfile(fname, dst)
        print(f"Synced {fname} to artifacts ({os.path.getsize(dst):,} bytes)")
