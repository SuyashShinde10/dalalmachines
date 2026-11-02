# scratch/render_clean_guide.py
import os, sys, subprocess, shutil

sys.path.append(os.path.abspath('scratch'))
from build_all_32_pages import dalal_routes, ompi_modules

print("Compiling all 32 pages into HTML and rendering to PDF...")

# Base CSS and styling
html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Dalal Machine Tools & OMPI India - Executive Plain-Language Business Guide (57 Systems & Modules)</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;600;700&display=swap" rel="stylesheet">
  <style>
    @page {
      size: A4 portrait;
      margin: 8mm 10mm 8mm 10mm;
    }
    *, *::before, *::after {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }
    body {
      font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      color: #0f172a;
      background: #ffffff;
      font-size: 9.0pt;
      line-height: 1.36;
      -webkit-print-color-adjust: exact;
      print-color-adjust: exact;
    }
    .page {
      height: 281mm;
      max-height: 281mm;
      overflow: hidden;
      box-sizing: border-box;
      position: relative;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      page-break-after: always;
      break-after: page;
      padding: 1px 0;
    }
    .page:last-child {
      page-break-after: avoid;
      break-after: avoid;
    }
    .page-content {
      flex: 1;
    }

    /* Corporate Header */
    .header-bar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 2px solid #0f172a;
      border-top: 3.5px solid #d97706;
      padding-top: 4px;
      padding-bottom: 4px;
      margin-bottom: 5px;
    }
    .brand-title {
      font-size: 10.5pt;
      font-weight: 800;
      color: #0f172a;
      letter-spacing: -0.2px;
    }
    .brand-subtitle {
      font-size: 7.2pt;
      font-weight: 700;
      color: #b45309;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }
    .doc-meta {
      text-align: right;
      font-size: 6.8pt;
      color: #475569;
      line-height: 1.25;
    }

    /* Strict Confidentiality Alert Bar */
    .confidential-bar {
      background: #fef2f2;
      border: 1.5px solid #dc2626;
      border-radius: 4px;
      padding: 3.5px 8px;
      margin-bottom: 6px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 7.1pt;
      font-weight: 700;
      color: #991b1b;
    }
    .confidential-tag {
      background: #b91c1c;
      color: #ffffff;
      padding: 1.5px 6px;
      border-radius: 3px;
      text-transform: uppercase;
      font-size: 6.6pt;
      letter-spacing: 0.5px;
      font-weight: 800;
    }

    /* Section Subheaders */
    .section-header {
      background: #0f172a;
      color: #ffffff;
      padding: 4px 8px;
      border-radius: 4px;
      margin-bottom: 6px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .section-title {
      font-size: 8.0pt;
      font-weight: 800;
      letter-spacing: 0.3px;
      text-transform: uppercase;
    }
    .section-tag {
      font-size: 6.8pt;
      font-weight: 700;
      background: #f59e0b;
      color: #0f172a;
      padding: 1px 6px;
      border-radius: 3px;
    }

    /* Standard Card Box (Exactly 2 per page) */
    .card-box {
      border: 1.5px solid #cbd5e1;
      border-radius: 6px;
      background: #ffffff;
      margin-bottom: 6px;
      padding: 7px 9px;
    }
    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 1.5px solid #e2e8f0;
      padding-bottom: 4px;
      margin-bottom: 5px;
    }
    .badge-id {
      background: #0f172a;
      color: #ffffff;
      padding: 2px 6px;
      border-radius: 3px;
      font-size: 7.2pt;
      font-weight: 800;
      font-family: 'JetBrains Mono', monospace;
      margin-right: 5px;
    }
    .card-title {
      font-size: 9.2pt;
      font-weight: 800;
      color: #0f172a;
    }
    .card-path {
      font-family: 'JetBrains Mono', monospace;
      font-size: 7.0pt;
      color: #b45309;
      font-weight: 700;
      background: #fffbeb;
      padding: 1.5px 5px;
      border: 1px solid #fef3c7;
      border-radius: 3px;
    }
    .card-status {
      font-size: 6.8pt;
      font-weight: 700;
      padding: 1.5px 5px;
      border-radius: 3px;
      margin-left: 5px;
    }
    .status-live {
      background: #dcfce7;
      color: #15803d;
      border: 1px solid #bbf7d0;
    }
    .status-phase2 {
      background: #fef3c7;
      color: #b45309;
      border: 1px solid #fde68a;
    }

    /* Simple 2-Column Content Grid */
    .simple-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 7px;
      margin-bottom: 5px;
    }
    .grid-label {
      font-size: 7.1pt;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.3px;
      color: #475569;
      margin-bottom: 2px;
      border-bottom: 1px solid #f1f5f9;
      padding-bottom: 1.5px;
    }
    .grid-text {
      font-size: 8.3pt;
      line-height: 1.34;
      color: #334155;
    }

    /* Highlight Feature Box */
    .feature-strip {
      background: #f8fafc;
      border: 1px solid #e2e8f0;
      border-radius: 4px;
      padding: 4px 7px;
      font-size: 7.9pt;
      line-height: 1.34;
      color: #1e293b;
    }
    .feature-strip strong {
      color: #0f172a;
    }

    /* Corporate Footer */
    .footer-bar {
      border-top: 1px solid #cbd5e1;
      padding-top: 3.5px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 6.6pt;
      color: #64748b;
      margin-top: auto;
    }
    .confidential-watermark {
      font-weight: 800;
      color: #dc2626;
      letter-spacing: 0.5px;
      text-transform: uppercase;
    }
  </style>
</head>
<body>
"""

def make_header(subtitle):
    return f"""
    <div class="header-bar">
      <div>
        <div class="brand-title">DALAL MACHINE TOOLS AGENCY &amp; OMPI INDIA</div>
        <div class="brand-subtitle">{subtitle}</div>
      </div>
      <div class="doc-meta">
        <strong>Doc Ref:</strong> EXEC-GUIDE-2026-DALAL-OMPI-57<br>
        <strong>Classification:</strong> Strictly Confidential &amp; Proprietary<br>
        <strong>Edition:</strong> Plain Business English (Zero Technical Jargon)
      </div>
    </div>
    <div class="confidential-bar">
      <div>&#9888; STRICTLY CONFIDENTIAL &bull; FOR INTERNAL MANAGEMENT USE ONLY &bull; EXTERNAL SHARING PROHIBITED</div>
      <div class="confidential-tag">STRICTLY PRIVATE</div>
    </div>
"""

def make_footer(page_num):
    return f"""
    <div class="footer-bar">
      <div><strong>Dalal Machine Tools Agency Pvt. Ltd. &amp; OMPI India LLP</strong> &bull; Commercial Operations</div>
      <div class="confidential-watermark">&#128274; CONFIDENTIAL &bull; STRICTLY NOT FOR SHARING</div>
      <div>Page {page_num} of 32</div>
    </div>
"""

def make_route_card(r):
    return f"""
      <div class="card-box">
        <div class="card-header">
          <div>
            <span class="badge-id">{r['id']}</span>
            <span class="card-title">{r['title']}</span>
            <span class="card-status status-live">&#10003; LIVE &amp; ACTIVE</span>
          </div>
          <div class="card-path">{r['path']}</div>
        </div>
        <div style="font-size:7.4pt; color:#64748b; font-weight:700; margin-bottom:4px;">
          <strong>Target User / Audience:</strong> {r['audience']}
        </div>
        <div class="simple-grid">
          <div>
            <div class="grid-label">What The Customer Sees on Screen</div>
            <div class="grid-text">{r['sees']}</div>
          </div>
          <div>
            <div class="grid-label">Why It Exists &amp; How It Brings Business</div>
            <div class="grid-text">{r['benefit']}</div>
          </div>
        </div>
        <div class="feature-strip">
          <strong>Key Business Feature:</strong> {r['feature']}
        </div>
      </div>
"""

def make_module_card(m):
    status_badge = '<span class="card-status status-live">&#10003; LIVE IN SYSTEM</span>' if m['is_live'] else '<span class="card-status status-phase2">PHASE 2 DEPLOYMENT</span>'
    return f"""
      <div class="card-box">
        <div class="card-header">
          <div>
            <span class="badge-id">{m['id']}</span>
            <span class="card-title">{m['title']}</span>
            {status_badge}
          </div>
          <div style="font-size:7.2pt; font-weight:700; color:#b45309; background:#fffbeb; padding:1.5px 5px; border:1px solid #fef3c7; border-radius:3px;">{m['engine']}</div>
        </div>
        <div style="font-size:7.4pt; color:#64748b; font-weight:700; margin-bottom:4px;">
          <strong>Responsible Staff Role:</strong> {m['role']}
        </div>
        <div class="simple-grid">
          <div>
            <div class="grid-label">What This Module Does in Daily Work</div>
            <div class="grid-text">{m['does']}</div>
          </div>
          <div>
            <div class="grid-label">Business Value &amp; Risk Prevented</div>
            <div class="grid-text">{m['benefit']}</div>
          </div>
        </div>
        <div class="feature-strip">
          <strong>Key Operation:</strong> {m['feature']}
        </div>
      </div>
"""

# PAGE 1: COVER & NON-DISCLOSURE NOTICE
html += f"""
  <div class="page">
    <div class="page-content">
      {make_header("EXECUTIVE BUSINESS GUIDE &bull; 57 OPERATIONAL SYSTEMS &amp; MODULES")}

      <!-- Legal Non-Disclosure Notice -->
      <div style="background:#fff1f2; border:2px solid #e11d48; border-radius:6px; padding:10px 14px; margin-bottom:10px;">
        <div style="font-size:9.2pt; font-weight:800; color:#9f1239; text-transform:uppercase; margin-bottom:4px; display:flex; align-items:center; gap:6px;">
          <span>&#128274; LEGAL NON-DISCLOSURE &amp; ANTI-SHARING COVENANT</span>
        </div>
        <p style="font-size:8.4pt; line-height:1.42; color:#4c0519; margin-bottom:4px;">
          <strong>Notice to Reader:</strong> This document contains highly confidential business operational workflows, pricing mechanisms, supply chain strategies, and commercial system architectures developed exclusively for the leadership and operational management of <strong>Dalal Machine Tools Agency Pvt. Ltd.</strong> and <strong>OMPI India LLP</strong>.
        </p>
        <p style="font-size:8.2pt; line-height:1.4; color:#881337;">
          <strong>Strict Restriction:</strong> Copying, photographing, forwarding, distributing, or sharing this document (in whole or in part) with any third party, competitor, external broker, or unauthorized personnel without the written consent of the Managing Director is <strong>strictly prohibited</strong> and constitutes a violation of proprietary business rights.
        </p>
      </div>

      <!-- Company Profiles Grid -->
      <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px; background:#f8fafc; border:1.5px solid #cbd5e1; border-radius:6px; padding:10px 12px; margin-bottom:10px;">
        <div style="font-size:8.6pt; line-height:1.4; color:#334155;">
          <div style="font-size:8.0pt; font-weight:800; color:#0f172a; text-transform:uppercase; letter-spacing:0.5px; margin-bottom:3px;">
            Operating Entity 1: Heavy Machinery
          </div>
          <strong style="font-size:9.5pt; color:#0f172a;">Dalal Machine Tools Agency Pvt. Ltd.</strong><br>
          Commerce Centre, Tardeo, Mumbai &bull; Pune Stockyard, Chakan<br>
          <strong>Core Business:</strong> Inbound Acquisition, High Seas Sales, Overhaul &amp; Turnkey Commissioning of Heavy Forging Presses (100T to 6,300T).
        </div>
        <div style="font-size:8.6pt; line-height:1.4; color:#334155;">
          <div style="font-size:8.0pt; font-weight:800; color:#0f172a; text-transform:uppercase; letter-spacing:0.5px; margin-bottom:3px;">
            Operating Entity 2: Precision Clutches
          </div>
          <strong style="font-size:9.5pt; color:#0f172a;">OMPI India LLP</strong><br>
          Pimpri-Chinchwad / Chakan Industrial Corridor, Pune<br>
          <strong>Core Business:</strong> Sole Indian Representative for OMPI s.r.l. (Italy) &bull; Pneumatic Clutch-Brake Modernization, Rotary Unions &amp; Spares.
        </div>
      </div>

      <!-- Document Purpose & How To Read -->
      <div style="background:#ffffff; border:1.5px solid #e2e8f0; border-radius:6px; padding:9px 12px; margin-bottom:10px;">
        <div style="font-size:8.8pt; font-weight:800; color:#0f172a; text-transform:uppercase; margin-bottom:4px; border-bottom:1px solid #f1f5f9; padding-bottom:3px;">
          Purpose of This Business Guide (Written in 100% Plain Language)
        </div>
        <p style="font-size:8.5pt; line-height:1.42; color:#334155; margin-bottom:6px;">
          This document explains every single page on the website and every single management tool in the company in <strong>simple, everyday business words</strong>. There are no confusing technical terms, developer jargon, or complicated computer codes here. It explains:
        </p>
        <div style="display:grid; grid-template-columns:1fr 1fr; gap:8px; font-size:8.2pt; line-height:1.38; color:#1e293b;">
          <div style="background:#f1f5f9; padding:6px 9px; border-radius:4px;">
            <strong style="color:#0f172a;">Part 1: The 24 Website Pages (Dalal Machinery)</strong><br>
            What customers see on screen, how it builds buyer trust, and how it brings multi-crore machinery inquiries directly to your phone.
          </div>
          <div style="background:#f1f5f9; padding:6px 9px; border-radius:4px;">
            <strong style="color:#0f172a;">Part 2: The 33 Management Tools (OMPI Operations)</strong><br>
            How your team manages customer quotes, Italy imports, godown spare parts, GST bills, and money payments without mistakes.
          </div>
        </div>
      </div>

      <!-- Summary Box -->
      <div style="background:#fffbeb; border:1.5px solid #f59e0b; border-radius:6px; padding:8px 12px; font-size:8.3pt; line-height:1.4; color:#78350f;">
        <strong>Executive Summary:</strong> Both companies now possess a world-class digital acquisition showroom (System 1) and an organized industrial operations system (System 2). When a factory owner inquires for a press, the system automatically checks the right Italian clutch, generates a formal quotation letter with photos in 60 seconds, and alerts the Managing Director on WhatsApp.
      </div>
    </div>
    {make_footer(1)}
  </div>
"""

# PAGES 2 TO 13: DALAL 24 ROUTES (2 PER PAGE)
for i in range(12):
    page_num = i + 2
    r1 = dalal_routes[i * 2]
    r2 = dalal_routes[i * 2 + 1]
    
    html += f"""
  <div class="page">
    <div class="page-content">
      {make_header("SYSTEM 1: DALAL MACHINERY PUBLIC PLATFORM")}
      
      <div class="section-header">
        <span class="section-title">Dalal Web Platform &bull; Routes {i*2+1:02d} &amp; {i*2+2:02d} of 24</span>
        <span class="section-tag">High-Ticket Asset Acquisition</span>
      </div>

      {make_route_card(r1)}
      {make_route_card(r2)}
    </div>
    {make_footer(page_num)}
  </div>
"""

# PAGE 14: OMPI OPERATIONS SUITE OVERVIEW
html += f"""
  <div class="page">
    <div class="page-content">
      {make_header("SYSTEM 2: OMPI INDIA INDUSTRIAL OPERATIONS SUITE")}

      <div class="section-header">
        <span class="section-title">OMPI Operations Suite Overview &bull; The 4 Business Engines</span>
        <span class="section-tag">Internal Company ERP System</span>
      </div>

      <div style="background:#ffffff; border:1.5px solid #cbd5e1; border-radius:6px; padding:10px 12px; margin-bottom:10px;">
        <div style="font-size:9.0pt; font-weight:800; color:#0f172a; text-transform:uppercase; margin-bottom:4px; border-bottom:1px solid #f1f5f9; padding-bottom:3px;">
          How OMPI Operations Management Works in Daily Practice
        </div>
        <p style="font-size:8.6pt; line-height:1.42; color:#334155; margin-bottom:8px;">
          While Dalal Machine Tools operates as the <strong>public digital showroom</strong> that brings in inquiries from factory owners, OMPI India operates the <strong>internal management system</strong>. It organizes everything that happens after an inquiry arrives: quoting prices, sizing clutches, placing orders with Italy, tracking sea shipments, managing godown inventory, and collecting customer payments.
        </p>

        <!-- 4 Engines Grid -->
        <div style="display:grid; grid-template-columns:1fr 1fr; gap:9px;">
          <div style="background:#f8fafc; border:1px solid #cbd5e1; border-radius:5px; padding:7px 10px;">
            <div style="font-size:8.2pt; font-weight:800; color:#0f172a; text-transform:uppercase; margin-bottom:2px;">
              Engine 1: Sales &amp; Customer Quotes (10 Tools)
            </div>
            <p style="font-size:8.1pt; line-height:1.36; color:#475569;">
              Stores client GST records, sizes the right clutch, generates official PDF proposals in 60 seconds, and tracks deals from new inquiry to advance payment.
            </p>
          </div>
          <div style="background:#f8fafc; border:1px solid #cbd5e1; border-radius:5px; padding:7px 10px;">
            <div style="font-size:8.2pt; font-weight:800; color:#0f172a; text-transform:uppercase; margin-bottom:2px;">
              Engine 2: Italy Purchase &amp; Import Cost (7 Tools)
            </div>
            <p style="font-size:8.1pt; line-height:1.36; color:#475569;">
              Creates Euro purchase orders for OMPI Italy, calculates total landed customs duty in Rupees, and tracks sea containers from Genoa to Nhava Sheva.
            </p>
          </div>
          <div style="background:#f8fafc; border:1px solid #cbd5e1; border-radius:5px; padding:7px 10px;">
            <div style="font-size:8.2pt; font-weight:800; color:#0f172a; text-transform:uppercase; margin-bottom:2px;">
              Engine 3: Godown Stock &amp; Spare Parts (8 Tools)
            </div>
            <p style="font-size:8.1pt; line-height:1.36; color:#475569;">
              Shows live godown stock in Pune and Chakan, tracks high-wear brake friction pads, records serial numbers, and creates truck delivery passes.
            </p>
          </div>
          <div style="background:#f8fafc; border:1px solid #cbd5e1; border-radius:5px; padding:7px 10px;">
            <div style="font-size:8.2pt; font-weight:800; color:#0f172a; text-transform:uppercase; margin-bottom:2px;">
              Engine 4: Bills, GST Taxes, Money &amp; Safety (8 Tools)
            </div>
            <p style="font-size:8.1pt; line-height:1.36; color:#475569;">
              Generates official GST bills, exports GSTR-1 for your accountant in 1 click, tracks customer balance payments, and saves automatic daily backups.
            </p>
          </div>
        </div>
      </div>

      <!-- Phasing & Deployment Reality -->
      <div style="background:#fffbeb; border:1.5px solid #f59e0b; border-radius:6px; padding:9px 12px; margin-bottom:10px;">
        <div style="font-size:8.5pt; font-weight:800; color:#78350f; text-transform:uppercase; margin-bottom:3px;">
          Current Implementation Status: What is Live vs. Phased Rollout
        </div>
        <p style="font-size:8.2pt; line-height:1.4; color:#92400e;">
          <strong>10 Core Tools Are Already Live:</strong> The 60-second PDF quotation engine, AI clutch matching, inquiry pipeline tracking, WhatsApp quote sender, machine inventory stock tracking, staff access security, and nightly backups are already functioning in the system.<br>
          <strong>Deep ERP Tools (Phase 2):</strong> Specialized tools like Euro purchase orders, multi-level parts breakdown, laser serial tracking, and GSTR-1 tax export are fully architected in this document and scheduled for rollout across 7 monthly sprints as agreed in the Master SOW contract.
        </p>
      </div>

      <!-- Security Notice -->
      <div style="background:#f1f5f9; border:1.5px solid #cbd5e1; border-radius:6px; padding:8px 12px; font-size:8.2pt; line-height:1.38; color:#334155;">
        <strong>Data Safety Commitment:</strong> All company inquiries, customer phone numbers, supplier costs, and pricing records are strictly protected. Staff members only see what their job requires, and complete backups are automatically saved every night.
      </div>
    </div>
    {make_footer(14)}
  </div>
"""

# PAGES 15 TO 30: OMPI MODULES 01 TO 32 (2 PER PAGE = 16 PAGES)
for i in range(16):
    page_num = i + 15
    m1 = ompi_modules[i * 2]
    m2 = ompi_modules[i * 2 + 1]
    
    html += f"""
  <div class="page">
    <div class="page-content">
      {make_header("SYSTEM 2: OMPI INDUSTRIAL OPERATIONS &amp; ERP SUITE")}
      
      <div class="section-header">
        <span class="section-title">OMPI Management Engines &bull; Modules {i*2+1:02d} &amp; {i*2+2:02d} of 33</span>
        <span class="section-tag">{m1['engine'].split(':')[0]}</span>
      </div>

      {make_module_card(m1)}
      {make_module_card(m2)}
    </div>
    {make_footer(page_num)}
  </div>
"""

# PAGE 31: MODULE 33 (OWNER DASHBOARD) + ADMIN CONSOLES
m33 = ompi_modules[32]
html += f"""
  <div class="page">
    <div class="page-content">
      {make_header("SYSTEM 2: EXECUTIVE MANAGEMENT &amp; CONTROL CONSOLES")}
      
      <div class="section-header">
        <span class="section-title">OMPI Management Engine &bull; Module 33 of 33 &amp; Operations Consoles</span>
        <span class="section-tag">Executive Business Control</span>
      </div>

      {make_module_card(m33)}

      <!-- Operations Consoles Summary Box -->
      <div class="card-box" style="margin-top:4px;">
        <div class="card-header">
          <div>
            <span class="badge-id">PORTALS</span>
            <span class="card-title">Staff Operations &amp; Director Control Consoles</span>
            <span class="card-status status-live">&#10003; 100% LIVE IN SYSTEM</span>
          </div>
          <div class="card-path">/admin &bull; /superadmin &bull; /dev</div>
        </div>
        <div class="simple-grid" style="margin-top:4px;">
          <div>
            <div class="grid-label">Staff Operations Desk (/admin)</div>
            <div class="grid-text">
              Where your sales team manages customer RFQs, views AI lead scores, sends WhatsApp quotes, and updates machinery availability without touching code.
            </div>
          </div>
          <div>
            <div class="grid-label">Managing Director Governance (/superadmin)</div>
            <div class="grid-text">
              Gives the business owner total control over staff passwords, user permissions, company contact settings, and complete unalterable business history logs.
            </div>
          </div>
        </div>
        <div class="feature-strip">
          <strong>Security Guarantee:</strong> Both administrative consoles are completely cloaked from the public web with secure secret passkeys, ensuring zero unauthorized access.
        </div>
      </div>
    </div>
    {make_footer(31)}
  </div>
"""

# PAGE 32: THE COMPLETE BUYER JOURNEY, ROADMAP & SIGN-OFF
html += f"""
  <div class="page">
    <div class="page-content">
      {make_header("SYSTEM INTEGRATION &bull; 6-STEP BUYER JOURNEY &amp; SIGN-OFF")}

      <div class="section-header">
        <span class="section-title">How Both Systems Work Together &bull; From Inquiry to Delivery</span>
        <span class="section-tag">Unified Commercial Flow</span>
      </div>

      <!-- 6-Step Workflow Box -->
      <div style="background:#ffffff; border:1.5px solid #cbd5e1; border-radius:6px; padding:9px 12px; margin-bottom:10px;">
        <div style="font-size:8.8pt; font-weight:800; color:#0f172a; text-transform:uppercase; margin-bottom:6px; border-bottom:1px solid #f1f5f9; padding-bottom:3px;">
          The Seamless 6-Step Business Process (Inquiry to Payment)
        </div>
        <div style="display:grid; grid-template-columns:1fr 1fr; gap:8px; font-size:8.1pt; line-height:1.36; color:#334155;">
          <div style="background:#f8fafc; padding:6px 8px; border-radius:4px; border-left:3px solid #d97706;">
            <strong>Step 1: Customer Inquires Online</strong><br>
            A plant head finds a 1,600T press on the website and clicks the WhatsApp inquiry button with his company details.
          </div>
          <div style="background:#f8fafc; padding:6px 8px; border-radius:4px; border-left:3px solid #d97706;">
            <strong>Step 2: Instant Technical Sizing</strong><br>
            The system automatically matches the press with the exact Italian OMPI pneumatic clutch required for the job.
          </div>
          <div style="background:#f8fafc; padding:6px 8px; border-radius:4px; border-left:3px solid #d97706;">
            <strong>Step 3: 60-Second Quotation Sent</strong><br>
            An official proposal PDF with machine photos, specs, and price is sent directly to the customer's WhatsApp.
          </div>
          <div style="background:#f8fafc; padding:6px 8px; border-radius:4px; border-left:3px solid #d97706;">
            <strong>Step 4: Machine Locked in Godown</strong><br>
            Once the client confirms, the press is marked 'Under Commercial Hold' so it cannot be sold to anyone else.
          </div>
          <div style="background:#f8fafc; padding:6px 8px; border-radius:4px; border-left:3px solid #d97706;">
            <strong>Step 5: Pune Workshop Overhaul &amp; Rigging</strong><br>
            The machine undergoes live power trials, foundation check, and is dispatched on low-bed trailers to the buyer's factory.
          </div>
          <div style="background:#f8fafc; padding:6px 8px; border-radius:4px; border-left:3px solid #d97706;">
            <strong>Step 6: Official GST Invoicing &amp; Backup</strong><br>
            Clean tax bills are issued, GST records are updated for your accountant, and all transaction history is securely saved.
          </div>
        </div>
      </div>

      <!-- Implementation Summary & Phasing Table -->
      <div style="background:#f8fafc; border:1.5px solid #cbd5e1; border-radius:6px; padding:8px 12px; margin-bottom:10px;">
        <div style="font-size:8.4pt; font-weight:800; color:#0f172a; text-transform:uppercase; margin-bottom:4px;">
          Commercial Phasing &amp; Implementation Summary
        </div>
        <table style="width:100%; border-collapse:collapse; font-size:7.8pt; line-height:1.3; color:#334155;">
          <thead>
            <tr style="background:#0f172a; color:#ffffff; text-align:left;">
              <th style="padding:3px 6px;">Delivery Phase</th>
              <th style="padding:3px 6px;">Scope of Work</th>
              <th style="padding:3px 6px;">Operational State</th>
            </tr>
          </thead>
          <tbody>
            <tr style="border-bottom:1px solid #e2e8f0; background:#f0fdf4;">
              <td style="padding:3px 6px; font-weight:700;">Phase 1 (Current)</td>
              <td style="padding:3px 6px;">Dalal 24 Public Pages &bull; Staff Admin Portal &bull; Superadmin Console &bull; 10 Shared Core Engines</td>
              <td style="padding:3px 6px; font-weight:700; color:#15803d;">100% COMPLETE &amp; LIVE</td>
            </tr>
            <tr style="border-bottom:1px solid #e2e8f0; background:#fffbeb;">
              <td style="padding:3px 6px; font-weight:700;">Phase 2 (Roadmap)</td>
              <td style="padding:3px 6px;">OMPI Standalone ERP Modules (7 Monthly Sprints: Customer 360, Italy POs, BOM, Godown Bins, GSTR-1)</td>
              <td style="padding:3px 6px; font-weight:700; color:#b45309;">FULLY ARCHITECTED FOR ROLLOUT</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Non-Disclosure Confirmation & Executive Sign-Off -->
      <div style="border:1.5px solid #e11d48; background:#fff1f2; border-radius:6px; padding:8px 12px; margin-bottom:8px;">
        <div style="font-size:8.2pt; font-weight:800; color:#9f1239; text-transform:uppercase; margin-bottom:2px;">
          &#128274; Confidentiality &amp; Property Protection Acknowledgment
        </div>
        <p style="font-size:7.8pt; line-height:1.34; color:#4c0519;">
          This master specification represents the proprietary intellectual property and operational blueprint of Dalal Machine Tools Agency Pvt. Ltd. and OMPI India LLP. External sharing, publishing, or reproduction without written authorization is strictly forbidden.
        </p>
      </div>

      <!-- Signatures Grid -->
      <div style="display:grid; grid-template-columns:1fr 1fr; gap:12px; border-top:1.5px solid #0f172a; padding-top:6px;">
        <div style="font-size:8.0pt; line-height:1.3; color:#334155;">
          <strong>For Dalal Machine Tools Agency Pvt. Ltd. &amp; OMPI India:</strong><br><br>
          __________________________________________<br>
          <strong>Mr. Vinit Dalal</strong> &bull; Managing Director / Partner
        </div>
        <div style="font-size:8.0pt; line-height:1.3; color:#334155; text-align:right;">
          <strong>Prepared by Principal Software Consultant:</strong><br><br>
          __________________________________________<br>
          <strong>Suyash Shinde</strong> &bull; Pimpri, Pune, Maharashtra
        </div>
      </div>
    </div>
    {make_footer(32)}
  </div>
</body>
</html>
"""

# Write HTML file
output_html = "DALAL_AND_OMPI_57_PAGES_AND_MODULES_MASTER_SPECIFICATION.html"
with open(output_html, "w", encoding="utf-8") as f:
    f.write(html)
print(f"Successfully generated HTML: {output_html} ({os.path.getsize(output_html):,} bytes)")

# Also write to dedicated clean filename
simple_html = "DALAL_AND_OMPI_57_EXECUTIVE_CLIENT_GUIDE_SIMPLE.html"
with open(simple_html, "w", encoding="utf-8") as f:
    f.write(html)
print(f"Also saved copy to: {simple_html}")

# Render to PDF using Edge Headless
edge = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
pdf_path = os.path.abspath('DALAL_AND_OMPI_57_PAGES_AND_MODULES_MASTER_SPECIFICATION.pdf')
simple_pdf_path = os.path.abspath('DALAL_AND_OMPI_57_EXECUTIVE_CLIENT_GUIDE_SIMPLE.pdf')
url = f'file:///{os.path.abspath(output_html).replace("\\", "/")}'

cmd = [
    edge,
    '--headless',
    '--disable-gpu',
    f'--print-to-pdf={pdf_path}',
    '--no-pdf-header-footer',
    url
]
print(f"Rendering PDF via Edge: {pdf_path}...")
res = subprocess.run(cmd, capture_output=True, text=True)

if os.path.exists(pdf_path):
    sz = os.path.getsize(pdf_path)
    print(f"PDF Successfully Generated: {pdf_path} ({sz / 1024:.1f} KB)")
    
    # Copy to simple_pdf_path
    shutil.copyfile(pdf_path, simple_pdf_path)
    print(f"Saved copy to: {simple_pdf_path}")
    
    # Copy to artifact directory
    artifact_dir = r'C:\Users\91940\.gemini\antigravity\brain\75a30f5c-ccbc-43b7-9b59-6c8c1ab99b62'
    dst1 = os.path.join(artifact_dir, 'DALAL_AND_OMPI_57_PAGES_AND_MODULES_MASTER_SPECIFICATION.pdf')
    dst2 = os.path.join(artifact_dir, 'DALAL_AND_OMPI_57_EXECUTIVE_CLIENT_GUIDE_SIMPLE.pdf')
    dst_html = os.path.join(artifact_dir, 'DALAL_AND_OMPI_57_EXECUTIVE_CLIENT_GUIDE_SIMPLE.html')
    
    shutil.copyfile(pdf_path, dst1)
    shutil.copyfile(pdf_path, dst2)
    shutil.copyfile(simple_html, dst_html)
    print(f"Copied all files to artifact directory: {artifact_dir}")
else:
    print("PDF Generation failed!")
    print("Stderr:", res.stderr)

