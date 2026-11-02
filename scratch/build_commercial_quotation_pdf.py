# scratch/build_commercial_quotation_pdf.py
import os
import subprocess
import shutil
import fitz

def build_quotation_html():
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
      padding: 12mm 16mm 11mm 16mm;
      font-size: 8.1pt;
      line-height: 1.34;
    }
    .page-2 {
      padding: 9.5mm 15mm 9.0mm 15mm;
      font-size: 7.7pt;
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
      margin-bottom: 7px;
    }
    .page-footer {
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 7.3pt;
      color: #6b7280;
      border-top: 1px solid #e5e7eb;
      padding-top: 3.5px;
      margin-top: 6px;
    }
    .content-area {
      flex: 1;
      display: flex;
      flex-direction: column;
    }
    h1.doc-title {
      font-size: 16.0pt;
      font-weight: 700;
      color: #17365d;
      margin: 0 0 3px 0;
      line-height: 1.22;
      letter-spacing: -0.2px;
    }
    .doc-meta {
      font-size: 7.7pt;
      line-height: 1.38;
      color: #374151;
      margin-bottom: 7px;
      background: #f8fafc;
      padding: 6px 10px;
      border-radius: 4px;
      border-left: 3.5px solid #17365d;
    }
    h2.section-heading {
      font-size: 9.8pt;
      font-weight: 700;
      color: #17365d;
      border-bottom: 1.5px solid #17365d;
      padding-bottom: 2px;
      margin: 6px 0 4px 0;
      line-height: 1.2;
    }
    .page-2 h2.section-heading {
      font-size: 9.3pt;
      margin: 5.5px 0 3.0px 0;
      padding-bottom: 1.5px;
    }
    p {
      margin: 0 0 4px 0;
      font-size: 7.9pt;
      line-height: 1.32;
      color: #374151;
    }
    table.quotation-table {
      width: 100%;
      border-collapse: collapse;
      margin-bottom: 6px;
      font-size: 7.9pt;
      line-height: 1.28;
    }
    .page-2 table.quotation-table {
      margin-bottom: 4.0px;
      font-size: 7.5pt;
      line-height: 1.24;
    }
    table.quotation-table th {
      background: #17365d;
      color: #ffffff;
      font-weight: 700;
      text-align: left;
      padding: 3.8px 6px;
      border: 1px solid #17365d;
      font-size: 7.8pt;
    }
    .page-2 table.quotation-table th {
      padding: 2.8px 5.5px;
      font-size: 7.5pt;
    }
    table.quotation-table td {
      border: 1px solid #d1d5db;
      padding: 3.6px 6px;
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
      font-size: 8.1pt;
      border: 1px solid #17365d !important;
      padding: 4.2px 6.5px;
    }
    .subtotal-row .col-price {
      color: #ffffff !important;
      font-size: 8.4pt;
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
      padding: 1.2px 5.0px;
      border-radius: 3px;
      text-transform: uppercase;
      letter-spacing: 0.3px;
    }
    .terms-box {
      background: #f8fafc;
      border-left: 3.5px solid #17365d;
      padding: 4.5px 8.5px;
      font-size: 7.2pt;
      line-height: 1.28;
      color: #374151;
      margin-bottom: 4.5px;
    }
    .terms-box strong {
      color: #1e3a8a;
    }
    """

    def make_header():
        return """
        <div class="page-header">
          <span>Dalal Machine Tools Agency &amp; OMPI India | Commercial Quotation &bull; v2.0</span>
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

    p1 = f"""
    <div class="page page-1">
      {make_header()}
      <div class="content-area">
        <h1 class="doc-title">Commercial Quotation: Module-Wise Cost Breakdown</h1>
        <div class="doc-meta">
          <strong>Engagement:</strong> Unified Digital Showroom Platform &amp; OMPI Industrial ERP Suite (57 Total Units)<br>
          <strong>Client Entities:</strong> Dalal Machine Tools Agency Pvt. Ltd. &amp; OMPI India LLP &bull; Attn: <strong>Mr. Vinit Dalal</strong>, Managing Director / Partner<br>
          <strong>Consultant:</strong> Suyash Shinde, Principal Software Consultant, Pune &bull; <strong>Validity:</strong> 15 Days (Through 14 Nov 2026)
        </div>

        <h2 class="section-heading">1. System 1: Dalal Machine Tools Agency Pvt. Ltd. (Public Platform &amp; Inbound Engine)</h2>
        <p style="font-size: 7.8pt; margin-bottom: 3.5px;">Scope: 22 Public Showroom Pages + 2 Staff Admin Desks &bull; Delivery: Phase 1 (Weeks 1 to 8 &bull; Months 1 to 2)</p>

        <table class="quotation-table">
          <thead>
            <tr>
              <th style="width: 5%;" class="col-center">No.</th>
              <th style="width: 39%;">Module / Deliverable</th>
              <th style="width: 38%;">Operational Scope &amp; Key Deliverable</th>
              <th style="width: 18%;" class="col-right">Price (INR)</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td class="col-center">1</td>
              <td><strong>Machinery Showroom &amp; Category Catalog</strong></td>
              <td>26 machine categories, stock filters, yard authenticity showcase</td>
              <td class="col-price">&#8377; 35,000</td>
            </tr>
            <tr>
              <td class="col-center">2</td>
              <td><strong>Machine Detail Sheets &amp; Video Trials</strong></td>
              <td>Tonnage, stroke, bed specs, unedited running video links per machine</td>
              <td class="col-price">&#8377; 30,000</td>
            </tr>
            <tr>
              <td class="col-center">3</td>
              <td><strong>Instant Quotation Engine &amp; WhatsApp Leads</strong></td>
              <td>60-sec formal proposal PDF download + direct WhatsApp lead routing</td>
              <td class="col-price">&#8377; 35,000</td>
            </tr>
            <tr>
              <td class="col-center">4</td>
              <td><strong>Press Tonnage &amp; Sizing Assistant</strong></td>
              <td>Interactive component force calculation formula for plant buyers</td>
              <td class="col-price">&#8377; 25,000</td>
            </tr>
            <tr>
              <td class="col-center">5</td>
              <td><strong>High Seas Sales &amp; Import FAQs Portal</strong></td>
              <td>Procedural guidance, customs documentation &amp; GST ITC explainers</td>
              <td class="col-price">&#8377; 20,000</td>
            </tr>
            <tr>
              <td class="col-center">6</td>
              <td><strong>Staff Operations Console &amp; RFQ Lead Desk</strong></td>
              <td>Internal machine spec manager, stock toggles, buyer RFQ inbox</td>
              <td class="col-price">&#8377; 30,000</td>
            </tr>
            <tr>
              <td class="col-center">7</td>
              <td><strong>SEO Architecture &amp; GA4 Buyer Telemetry</strong></td>
              <td>Technical SEO metadata, Google Analytics 4 tracking &amp; search index</td>
              <td class="col-price">&#8377; 25,000</td>
            </tr>
            <tr class="subtotal-row">
              <td colspan="3"><strong>SUBTOTAL: SYSTEM 1 (DALAL MACHINE TOOLS AGENCY PVT. LTD.)</strong></td>
              <td class="col-price">&#8377; 2,00,000</td>
            </tr>
          </tbody>
        </table>

        <h2 class="section-heading" style="margin-top: 7px;">2. System 2: OMPI India LLP (Industrial Operations &amp; Precision Clutch ERP)</h2>
        <p style="font-size: 7.8pt; margin-bottom: 3.5px;">Scope: 33 Specialized Operations Modules in 7 Groups &bull; Delivery: Phase 2 &amp; Phase 3 (Weeks 9 to 32 &bull; Months 3 to 8)</p>

        <table class="quotation-table" style="margin-bottom: 0;">
          <thead>
            <tr>
              <th style="width: 5%;" class="col-center">No.</th>
              <th style="width: 39%;">Module / Deliverable</th>
              <th style="width: 38%;">Operational Scope &amp; Key Deliverable</th>
              <th style="width: 18%;" class="col-right">Price (INR)</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td class="col-center">1</td>
              <td><strong>Customer Master &amp; GST Directory</strong></td>
              <td>Verified 15-digit GSTIN, delivery godowns, commercial credit terms</td>
              <td class="col-price">&#8377; 40,000</td>
            </tr>
            <tr>
              <td class="col-center">2</td>
              <td><strong>Italian OMPI Product &amp; SKU Master</strong></td>
              <td>Clutch-brakes, rotating unions, friction discs by bore size &amp; torque</td>
              <td class="col-price">&#8377; 50,000</td>
            </tr>
            <tr>
              <td class="col-center">3</td>
              <td><strong>Landed Costing &amp; Euro/INR Calculator</strong></td>
              <td>Customs duty, ocean freight, port clearing, daily Euro exchange entry</td>
              <td class="col-price">&#8377; 65,000</td>
            </tr>
            <tr>
              <td class="col-center">4</td>
              <td><strong>OMPI Fast-Quote &amp; Proposal Generator</strong></td>
              <td>Shared quoting engine with OMPI letterhead &amp; separate bank details</td>
              <td class="col-price">&#8377; 45,000</td>
            </tr>
            <tr>
              <td class="col-center">5</td>
              <td><strong>Enquiry Deal Board &amp; Follow-Up Assistant</strong></td>
              <td>Visual deal pipeline (New, Quoted, Trial, Won) + follow-up alerts</td>
              <td class="col-price">&#8377; 40,000</td>
            </tr>
            <tr>
              <td class="col-center">6</td>
              <td><strong>Press-to-Clutch Sizing Matcher</strong></td>
              <td>Technical lookup matching industrial press makes with OMPI models</td>
              <td class="col-price">&#8377; 35,000</td>
            </tr>
            <tr>
              <td class="col-center">7</td>
              <td><strong>Pune Godown Stock &amp; Reservation Locker</strong></td>
              <td>Live stock balances, shelf bin locator, anti-double-selling stock lock</td>
              <td class="col-price">&#8377; 55,000</td>
            </tr>
            <tr>
              <td class="col-center">8</td>
              <td><strong>International PO &amp; Shipping Milestone Logger</strong></td>
              <td>Euro POs to Italy, Bill of Lading (BL) &amp; customs milestone tracker</td>
              <td class="col-price">&#8377; 45,000</td>
            </tr>
            <tr>
              <td class="col-center">9</td>
              <td><strong>Workshop Overhauls &amp; Reconditioning Cards</strong></td>
              <td>Digital job cards, clutch retrofit work orders, geometry trial logs</td>
              <td class="col-price">&#8377; 55,000</td>
            </tr>
            <tr>
              <td class="col-center">10</td>
              <td><strong>GST Tax Invoicing &amp; Payment Ageing Ledger</strong></td>
              <td>CGST/SGST/IGST tax invoices, 30/60/90-day payment ageing tracker</td>
              <td class="col-price">&#8377; 50,000</td>
            </tr>
            <tr>
              <td class="col-center">11</td>
              <td><strong>Breakdown Helpdesk &amp; Service AMC Tracker</strong></td>
              <td>Urgent breakdown calls, engineer dispatch, AMC quarterly calendar</td>
              <td class="col-price">&#8377; 40,000</td>
            </tr>
            <tr>
              <td class="col-center">12</td>
              <td><strong>Staff Access, On-Premise LAN &amp; 3-Tier Backups</strong></td>
              <td>Role permissions, local server setup, automated daily snapshots</td>
              <td class="col-price">&#8377; 40,000</td>
            </tr>
            <tr class="subtotal-row">
              <td colspan="3"><strong>SUBTOTAL: SYSTEM 2 (OMPI INDIA LLP)</strong></td>
              <td class="col-price">&#8377; 5,60,000</td>
            </tr>
          </tbody>
        </table>
      </div>
      {make_footer(1)}
    </div>
    """

    p2 = f"""
    <div class="page page-2">
      {make_header()}
      <div class="content-area">
        <h2 class="section-heading" style="margin-top: 0;">3. Total Project Investment Summary</h2>
        <table class="quotation-table" style="margin-bottom: 4.0px;">
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
        <table class="quotation-table" style="margin-bottom: 4.0px;">
          <thead>
            <tr>
              <th style="width: 49%;">Complimentary Service / Value Asset</th>
              <th style="width: 27%;">Industry Market Value</th>
              <th style="width: 24%;" class="col-center">Engagement Fee</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><strong>In-Scope Technical Maintenance &amp; Bug Remediation:</strong> Defect fixing for agreed 33 modules during 8-month lifecycle + 30-day post-handover warranty.</td>
              <td>&#8377; 2,40,000 (Est.)</td>
              <td class="col-center"><span class="free-badge">INCLUDED (&#8377;0)</span></td>
            </tr>
            <tr>
              <td><strong>On-Premise Local LAN Architecture Setup:</strong> Zero recurring third-party cloud user subscription fees; high-speed office yard access.</td>
              <td>&#8377; 2,50,000+ / Yr</td>
              <td class="col-center"><span class="free-badge">INCLUDED (&#8377;0)</span></td>
            </tr>
            <tr>
              <td><strong>Staff Onboarding, Role Training &amp; Video Walkthroughs:</strong> 12 hours of structured staff training at Pune yard + PDF Training Manual.</td>
              <td>&#8377; 75,000 (Est.)</td>
              <td class="col-center"><span class="free-badge">INCLUDED (&#8377;0)</span></td>
            </tr>
            <tr>
              <td><strong>Google SEO, AI Search (GEO) /llms.txt &amp; Schema:</strong> Rich search metadata, XML sitemaps, robots.txt &amp; buyer discovery optimization.</td>
              <td>&#8377; 60,000 (Est.)</td>
              <td class="col-center"><span class="free-badge">INCLUDED (&#8377;0)</span></td>
            </tr>
            <tr>
              <td><strong>Automated 3-Tier Rolling Disaster Recovery:</strong> Automated local &amp; external database snapshots protecting critical business records.</td>
              <td>&#8377; 40,000 (Est.)</td>
              <td class="col-center"><span class="free-badge">INCLUDED (&#8377;0)</span></td>
            </tr>
            <tr>
              <td><strong>1-Click Excel / CSV Leads &amp; Inventory Exporter:</strong> Instant offline data downloads with column filters &amp; UTF-8 BOM encoding.</td>
              <td>&#8377; 30,000 (Est.)</td>
              <td class="col-center"><span class="free-badge">INCLUDED (&#8377;0)</span></td>
            </tr>
            <tr style="background: #f0fdf4;">
              <td colspan="2" style="font-weight: 700; color: #065f46;">TOTAL COMPLIMENTARY VALUE DELIVERED TO CLIENT AT ZERO EXTRA CHARGE</td>
              <td class="col-center" style="font-weight: 800; color: #047857; font-size: 7.6pt;">&#8377; 6,95,000+ FREE</td>
            </tr>
          </tbody>
        </table>

        <h2 class="section-heading">5. Agreed Retainer Payment Schedule: &#8377;2.0L Advance + 7 Monthly Sprints @ &#8377;80,000/mo</h2>
        <table class="quotation-table" style="margin-bottom: 4.0px;">
          <thead>
            <tr>
              <th style="width: 14%;" class="col-center">Sprint / Month</th>
              <th style="width: 50%;">Core Deliverable &amp; Operational Milestone Trigger</th>
              <th style="width: 20%;" class="col-center">Invoiced Entity</th>
              <th style="width: 16%;" class="col-right">Amount (INR)</th>
            </tr>
          </thead>
          <tbody>
            <tr style="background: #eff6ff;">
              <td class="col-center"><strong>Advance (M1)</strong></td>
              <td><strong>Contract Execution &amp; Phase 1 Kickoff:</strong> Complete Dalal Web Platform (24 Units), Public Showroom, Instant Quoting &amp; WhatsApp Desk</td>
              <td class="col-center" style="font-size: 7.0pt;">Dalal Machine Tools Agency Pvt. Ltd.</td>
              <td class="col-price" style="color: #1e3a8a;">&#8377; 2,00,000</td>
            </tr>
            <tr>
              <td class="col-center"><strong>Month 2</strong></td>
              <td>OMPI Core ERP Sprint 1: Customer Master, 15-Digit GST Directory &amp; Enquiry Pipeline</td>
              <td class="col-center" style="font-size: 7.0pt;">OMPI India LLP</td>
              <td class="col-price">&#8377; 80,000</td>
            </tr>
            <tr>
              <td class="col-center"><strong>Month 3</strong></td>
              <td>OMPI Core ERP Sprint 2: Costing Sheets, Fast Multi-Revision PDF Quotation Engine</td>
              <td class="col-center" style="font-size: 7.0pt;">OMPI India LLP</td>
              <td class="col-price">&#8377; 80,000</td>
            </tr>
            <tr>
              <td class="col-center"><strong>Month 4</strong></td>
              <td>OMPI Core ERP Sprint 3: Supplier POs &amp; Italy Landed Cost Engine (EUR/INR FX + Customs)</td>
              <td class="col-center" style="font-size: 7.0pt;">OMPI India LLP</td>
              <td class="col-price">&#8377; 80,000</td>
            </tr>
            <tr>
              <td class="col-center"><strong>Month 5</strong></td>
              <td>OMPI Core ERP Sprint 4: Spares &amp; SKU Warehouse Inventory, Pune Godown Bin Locator</td>
              <td class="col-center" style="font-size: 7.0pt;">OMPI India LLP</td>
              <td class="col-price">&#8377; 80,000</td>
            </tr>
            <tr>
              <td class="col-center"><strong>Month 6</strong></td>
              <td>OMPI Operations Sprint 5: Digital Job Work Cards, Clutch Retrofit Orders &amp; QC Logs</td>
              <td class="col-center" style="font-size: 7.0pt;">OMPI India LLP</td>
              <td class="col-price">&#8377; 80,000</td>
            </tr>
            <tr>
              <td class="col-center"><strong>Month 7</strong></td>
              <td>OMPI Operations Sprint 6: GST Sales Invoicing, Credit/Debit Notes &amp; Payment Ageing</td>
              <td class="col-center" style="font-size: 7.0pt;">OMPI India LLP</td>
              <td class="col-price">&#8377; 80,000</td>
            </tr>
            <tr>
              <td class="col-center"><strong>Month 8</strong></td>
              <td>OMPI Operations Sprint 7: Final Handover, LAN Multi-User Setup, Training &amp; Sign-Off</td>
              <td class="col-center" style="font-size: 7.0pt;">OMPI India LLP</td>
              <td class="col-price">&#8377; 80,000</td>
            </tr>
            <tr class="grand-total-row">
              <td colspan="3"><strong>TOTAL ENGAGEMENT INVESTMENT (&#8377;2,00,000 ADVANCE + 7 &times; &#8377;80,000)</strong></td>
              <td class="col-price">&#8377; 7,60,000</td>
            </tr>
          </tbody>
        </table>

        <h2 class="section-heading">6. Commercial Governance &amp; Invoicing Terms</h2>
        <div class="terms-box">
          &bull; <strong>Separate Entity Invoicing:</strong> Invoices raised independently for <em>Dalal Machine Tools Agency Pvt. Ltd.</em> (&#8377;2,00,000) and <em>OMPI India LLP</em> (&#8377;5,60,000 in 7 monthly sprints @ &#8377;80,000/mo) for clean tax accounting &amp; direct GST ITC.<br>
          &bull; <strong>Pass-Through Billing (No Markups):</strong> Third-party cloud hosting, domains, WhatsApp API fees, and GST gateway usage are billed directly to Client accounts at actuals.<br>
          &bull; <strong>7-Day Deemed Acceptance Rule:</strong> Client reviews sprint deliverables within 7 calendar days of deployment; absence of written defect punch-list constitutes formal acceptance.<br>
          &bull; <strong>Warranty &amp; Code Ownership:</strong> 30 calendar days defect fix warranty included per sprint. 100% custom source code transfers upon full settlement.
        </div>

        <h2 class="section-heading">7. Commercial Acceptance &amp; Formal Authorization</h2>
        <p style="font-size: 7.3pt; margin-bottom: 3.0px;">Execution below constitutes formal acceptance of the commercial quotation and payment terms governed by the Master Services Agreement.</p>

        <table class="quotation-table" style="margin-bottom: 0;">
          <thead>
            <tr>
              <th style="width: 33.3%;">For Dalal Machine Tools Agency Pvt. Ltd.</th>
              <th style="width: 33.3%;">For OMPI India LLP</th>
              <th style="width: 33.4%;">Consultant / Solutions Architect</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td style="padding: 2.5px 5px;">
                <span style="font-size: 6.8pt; color: #6b7280; text-transform: uppercase;">Authorised Representative</span><br>
                <strong>Mr. Vinit Dalal</strong>, Managing Director
              </td>
              <td style="padding: 2.5px 5px;">
                <span style="font-size: 6.8pt; color: #6b7280; text-transform: uppercase;">Authorised Representative</span><br>
                <strong>Authorised Signatory</strong>, Designated Partner
              </td>
              <td style="padding: 2.5px 5px;">
                <span style="font-size: 6.8pt; color: #6b7280; text-transform: uppercase;">Principal Consultant</span><br>
                <strong>Suyash Shinde</strong>, Principal Consultant
              </td>
            </tr>
            <tr>
              <td style="height: 48px; vertical-align: top; color: #9ca3af; font-size: 7.0pt;">
                Signature / Company Seal
              </td>
              <td style="height: 48px; vertical-align: top; color: #9ca3af; font-size: 7.0pt;">
                Signature / Company Seal
              </td>
              <td style="height: 48px; vertical-align: top; color: #9ca3af; font-size: 7.0pt;">
                Signature
              </td>
            </tr>
            <tr>
              <td style="padding: 2.2px 5px; font-size: 7.0pt;">Date: _________________</td>
              <td style="padding: 2.2px 5px; font-size: 7.0pt;">Date: _________________</td>
              <td style="padding: 2.2px 5px; font-size: 7.0pt;">Date: <strong>2 November 2026</strong></td>
            </tr>
          </tbody>
        </table>
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
    html_content = build_quotation_html()
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
