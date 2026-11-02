# -*- coding: utf-8 -*-
import os, sys, subprocess, shutil

out_html = "d:/st.ourhtmldemo.com/CLIENT_DISCOVERY_MEETING_PLAYBOOK_AND_QUESTIONS.html"
out_pdf = "d:/st.ourhtmldemo.com/CLIENT_DISCOVERY_MEETING_PLAYBOOK_AND_QUESTIONS.pdf"

total_pages = 4

def get_header(title="EXECUTIVE CLIENT MEETING PLAYBOOK &amp; DISCOVERY QUESTION BANK"):
    return f"""
    <div class="header-bar">
      <div>
        <div class="brand-title">DALAL MACHINE TOOLS AGENCY &amp; OMPI INDIA</div>
        <div class="brand-subtitle">{title}</div>
      </div>
      <div class="doc-meta">
        <strong>Doc Ref:</strong> PLAYBOOK-2026-DISCOVERY<br>
        <strong>Meeting Target:</strong> Mr. Vinit Dalal, MD<br>
        <strong>Architect:</strong> Suyash Shinde (+91 96070 28594)
      </div>
    </div>
"""

def get_footer(page_num):
    return f"""
    <div class="doc-footer">
      <div><strong>Executive Meeting Playbook &bull; Dalal Machine Tools Agency Pvt. Ltd. &amp; OMPI India LLP</strong></div>
      <div>Page {page_num} of {total_pages} &bull; Strategic Discovery Baseline &bull; Confidential</div>
      <div>Consultant: <strong>Suyash Shinde</strong> (Pimpri, Pune)</div>
    </div>
"""

pages = []

# ==============================================================================
# PAGE 1: MEETING METADATA, AGENDA & STRATEGIC TALKING POINTS
# ==============================================================================
p1 = f"""
  <div class="page">
    <div class="page-content">
      {get_header("STRATEGIC MEETING AGENDA &amp; EXECUTIVE FRAMING")}
      
      <!-- Meeting Metadata Block -->
      <div style="display:grid; grid-template-columns:1.2fr 1fr; gap:10px; background:#f8fafc; border:1.5px solid #cbd5e1; border-radius:6px; padding:8px 12px; margin-bottom:10px;">
        <div style="font-size:8.6pt; line-height:1.38; color:#334155;">
          <div style="font-size:7.6pt; font-weight:800; color:#0f172a; text-transform:uppercase; letter-spacing:0.5px; margin-bottom:2px;">
            Target Client Stakeholders
          </div>
          <strong style="color:#0f172a; font-size:9.4pt;">Mr. Vinit Dalal</strong>, Managing Director<br>
          <strong>Dalal Machine Tools Agency Pvt. Ltd.</strong> (Mumbai &bull; Pune)<br>
          <strong>OMPI India LLP</strong> (Technical Alliance with OMPI S.r.l., Italy)
        </div>
        <div style="font-size:8.6pt; line-height:1.38; color:#334155;">
          <div style="font-size:7.6pt; font-weight:800; color:#0f172a; text-transform:uppercase; letter-spacing:0.5px; margin-bottom:2px;">
            Lead Technical Consultant
          </div>
          <strong style="color:#0284c7; font-size:9.4pt;">Suyash Shinde</strong>, Principal Systems Architect<br>
          <strong>Phone:</strong> +91 96070 28594 &bull; <strong>Email:</strong> suyashshinde360@gmail.com<br>
          <strong>Scope:</strong> Dual-Platform Architecture (24 Routes + 33 Modules)
        </div>
      </div>

      <!-- 4-Phase Meeting Flow Matrix -->
      <div style="border:1.5px solid #0f172a; border-radius:6px; padding:7px 10px; background:#ffffff; margin-bottom:10px;">
        <div style="font-size:8.4pt; font-weight:800; color:#0f172a; text-transform:uppercase; letter-spacing:0.5px; margin-bottom:4px; border-bottom:1px solid #e2e8f0; padding-bottom:3px;">
          Meeting Strategy &amp; Time Allocation Flow (45&ndash;60 Minutes)
        </div>
        <div style="display:grid; grid-template-columns:1fr 1fr 1fr 1fr; gap:6px; font-size:8.0pt; line-height:1.32;">
          <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:4px; padding:5px 7px;">
            <strong style="color:#b45309; display:block; font-size:8.2pt;">Phase 1: 00&ndash;10 Mins</strong>
            <strong>Strategic Framing:</strong> Introduce dual-engine concept (Public Ingestion vs. Internal ERP Ops); set discovery goals.
          </div>
          <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:4px; padding:5px 7px;">
            <strong style="color:#0f172a; display:block; font-size:8.2pt;">Phase 2: 10&ndash;25 Mins</strong>
            <strong>Dalal Web Engine:</strong> Walk through 24 routes, physical yard trust, 2x2 spec grid, and direct WhatsApp RFQ routing.
          </div>
          <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:4px; padding:5px 7px;">
            <strong style="color:#1e3a8a; display:block; font-size:8.2pt;">Phase 3: 25&ndash;45 Mins</strong>
            <strong>OMPI ERP &amp; Landed Cost:</strong> Deep-dive on EUR customs calculation, 60s quotes, BOM, and warehouse bin tracking.
          </div>
          <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:4px; padding:5px 7px;">
            <strong style="color:#047857; display:block; font-size:8.2pt;">Phase 4: 45&ndash;60 Mins</strong>
            <strong>Phasing &amp; Sign-Off:</strong> Align on Phase 1 Web launch vs. Phase 2 ERP rollout; agree on milestone schedule.
          </div>
        </div>
      </div>

      <!-- The 5 Strategic Talking Points -->
      <div class="section-header" style="background:#0f172a; margin-bottom:6px;">
        <span class="section-title">The 5 Strategic Talking Points to Establish Authority</span>
        <span class="section-tag">Value Proposition Framing</span>
      </div>

      <div style="display:grid; grid-template-columns:1fr 1fr; gap:8px;">
        <div style="background:#ffffff; border:1.2px solid #cbd5e1; border-radius:5px; padding:7px 9px;">
          <strong style="font-size:8.6pt; color:#0f172a; display:block; margin-bottom:2px;">1. Physical Stockyard Reality vs. Synthetic Brokers</strong>
          <p style="font-size:8.2pt; line-height:1.32; color:#334155;">
            Explain that online buyers distrust generic listings. Dalal's portal proves physical ownership in Pune yard within 5 seconds via live ground indicators, dimensional crosshair grids, and verified inspection certificates.
          </p>
        </div>
        <div style="background:#ffffff; border:1.2px solid #cbd5e1; border-radius:5px; padding:7px 9px;">
          <strong style="font-size:8.6pt; color:#0f172a; display:block; margin-bottom:2px;">2. High Seas CIF vs. Pune Yard Cost Modeling</strong>
          <p style="font-size:8.2pt; line-height:1.32; color:#334155;">
            Institutional buyers want financial options. Show how Route 12 transparently illustrates the 8%&ndash;15% landed cost savings on direct port shipments (Section 2(4) CST title transfer) versus local yard-delivered stock.
          </p>
        </div>
        <div style="background:#ffffff; border:1.2px solid #cbd5e1; border-radius:5px; padding:7px 9px;">
          <strong style="font-size:8.6pt; color:#0f172a; display:block; margin-bottom:2px;">3. 60-Second Fast-Quote vs. 2-Day Manual Quotations</strong>
          <p style="font-size:8.2pt; line-height:1.32; color:#334155;">
            Manual quotes take 24&ndash;48 hours and risk margin errors. ERP Module 04 compiles CAD outline drawings, EUR spot rates, customs duty, and milestone payment terms into a branded proposal PDF in under 60 seconds.
          </p>
        </div>
        <div style="background:#ffffff; border:1.2px solid #cbd5e1; border-radius:5px; padding:7px 9px;">
          <strong style="font-size:8.6pt; color:#0f172a; display:block; margin-bottom:2px;">4. EUR Fluctuation &amp; Landed Duty Hedging</strong>
          <p style="font-size:8.2pt; line-height:1.32; color:#334155;">
            OMPI units imported from Italy risk margin loss under currency volatility. Landed Cost Engine (Module 13) calculates Basic Customs Duty (7.5%), SWS (10%), IGST (18%), and port clearing with dynamic exchange buffers.
          </p>
        </div>
      </div>

      <div style="background:#f0fdf4; border:1.2px solid #86efac; border-radius:5px; padding:6px 10px; margin-top:8px;">
        <strong style="font-size:8.6pt; color:#166534;">5. Milestone Billing &amp; Retention Bad-Debt Sentinel:</strong>
        <span style="font-size:8.2pt; color:#334155; margin-left:4px;">
          Heavy presses and retrofits operate on staggered milestones (30% Advance, 50% Dispatch, 20% Post-Installation). ERP Module 28 blocks Rule 55 delivery challans and e-Way bills until dispatch payments are officially verified in the ledger.
        </span>
      </div>

    </div>
    {get_footer(1)}
  </div>
"""
pages.append(p1)

# ==============================================================================
# PAGE 2: QUESTIONS CATEGORY A (WEB PLATFORM) & CATEGORY B (CLUTCH SIZING)
# ==============================================================================
p2 = f"""
  <div class="page">
    <div class="page-content">
      {get_header("DISCOVERY QUESTIONS &bull; WEB PLATFORM &amp; CLUTCH SIZING")}
      
      <!-- Category A -->
      <div class="section-header" style="background:#0f172a; margin-bottom:7px;">
        <span class="section-title">Category A: Dalal Machinery Web Platform &amp; Inbound Leads (Routes 01&ndash;24)</span>
        <span class="section-tag">High-Ticket Buyer Acquisition</span>
      </div>

      <!-- Question 1 -->
      <div class="question-card">
        <div class="question-header">
          <span class="q-badge">Question 01</span>
          <span class="q-title">Inbound RFQ Triage &amp; WhatsApp Lead Routing Protocol</span>
        </div>
        <div class="q-verbatim">
          &ldquo;Vinit ji, abhi jab koi client 1600T ya 2500T press ke liye website par inquiry submit karta hai, toh lead flow kiske paas jana chahiye? Direct aapke personal WhatsApp par instant notify ho, ya pehle aapke sales coordinator ko filter karke formal proposal aapko review karwana chahiye?&rdquo;
        </div>
        <div class="q-intent">
          <strong>Architectural Intent:</strong> Determines lead notification logic for Routes 01, 05, and 08. Identifies whether to pre-fill direct WhatsApp chat to the MD or trigger an internal multi-recipient CRM webhook.
        </div>
      </div>

      <!-- Question 2 -->
      <div class="question-card">
        <div class="question-header">
          <span class="q-badge">Question 02</span>
          <span class="q-title">High Seas Sales (CIF) vs. Pune Yard Pricing Transparency</span>
        </div>
        <div class="q-verbatim">
          &ldquo;Aapke kitne percent clients direct Europe/Asia se High Seas import lena prefer karte hain versus Pune Yard ready-stock purchase? Kya hume har machine PDP par dono pricing options (Ex-Yard Pune vs High Seas CIF JNPT) publically dikhana hai ya sirf requested RFQ par reveal karna hai?&rdquo;
        </div>
        <div class="q-intent">
          <strong>Architectural Intent:</strong> Configures commercial visibility on Route 12 (Pricing) and Route 05 (Machine PDP). Establishes whether CIF calculations are public or behind an authenticated RFQ gate.
        </div>
      </div>

      <!-- Question 3 -->
      <div class="question-card">
        <div class="question-header">
          <span class="q-badge">Question 03</span>
          <span class="q-title">Pune Stockyard Physical Inspection &amp; Power Trial Appointments</span>
        </div>
        <div class="q-verbatim">
          &ldquo;Pune yard me power-on machine trial lene ke liye buyer ka screening protocol kya hai? Kya visitor direct calendar slot book kar sakta hai, ya pehle company ka GSTIN aur preliminary technical requirement verify hona mandatory hai?&rdquo;
        </div>
        <div class="q-intent">
          <strong>Architectural Intent:</strong> Locks down form validation rules for Route 08 (Contact) and Route 09 (Express RFQ). Prevents unauthorized access or non-serious visitors from blocking inspection slots.
        </div>
      </div>

      <!-- Category B -->
      <div class="section-header blue" style="margin-top:10px; margin-bottom:7px;">
        <span class="section-title">Category B: OMPI Italy Clutches &amp; Engineering Calculations (Modules 01&ndash;17)</span>
        <span class="section-tag">Precision Engineering Engine</span>
      </div>

      <!-- Question 4 -->
      <div class="question-card">
        <div class="question-header">
          <span class="q-badge" style="background:#1e3a8a;">Question 04</span>
          <span class="q-title">Clutch Sizing &amp; Torque Calculation Inputs ($GD^2$ Models)</span>
        </div>
        <div class="q-verbatim">
          &ldquo;Jab koi customer mechanical press retrofit ke liye OMPI clutch demand karta hai, toh aapke technical engineer ko press ka flywheel inertia ($GD^2$), SPM aur air pressure client se mil jata hai, ya aapki team on-site physical measurement audit karti hai?&rdquo;
        </div>
        <div class="q-intent">
          <strong>Architectural Intent:</strong> Validates calculation inputs for ERP Module 16 (Torque &amp; Pressure Sizing Calculator). Configures default safety derating formulas for variable factory air pressures (4.5 to 6.0 bar).
        </div>
      </div>

      <!-- Question 5 -->
      <div class="question-card">
        <div class="question-header">
          <span class="q-badge" style="background:#1e3a8a;">Question 05</span>
          <span class="q-title">Italian Consignment Lead Times &amp; Minimum Spares Buffer</span>
        </div>
        <div class="q-verbatim">
          &ldquo;OMPI Italy se PO place karne ke baad sea consignment Nhava Sheva (JNPT) pahunchne me standard kitna time lagta hai? (8 weeks ya 12 weeks?) Aur friction pads ya seal kits jaise high-wear items ka minimum safety buffer stock kitna rakhna chahiye?&rdquo;
        </div>
        <div class="q-intent">
          <strong>Architectural Intent:</strong> Sets automated threshold parameters for ERP Module 25 (Automated Re-Order Alert MRP) and maritime tracking schedules in Module 14 (Shipment &amp; Bill of Lading Ledger).
        </div>
      </div>

    </div>
    {get_footer(2)}
  </div>
"""
pages.append(p2)

# ==============================================================================
# PAGE 3: QUESTIONS CATEGORY C (WORKSHOP), D (FINANCE) & E (INFRASTRUCTURE)
# ==============================================================================
p3 = f"""
  <div class="page">
    <div class="page-content">
      {get_header("DISCOVERY QUESTIONS &bull; WORKSHOP, FINANCE &amp; GOVERNANCE")}
      
      <!-- Category C -->
      <div class="section-header" style="background:#0f172a; margin-bottom:7px;">
        <span class="section-title">Category C: Workshop Operations, Reconditioning &amp; Spares (Modules 18&ndash;25)</span>
        <span class="section-tag">Warehouse &amp; Quality Control Hub</span>
      </div>

      <!-- Question 6 -->
      <div class="question-card">
        <div class="question-header">
          <span class="q-badge">Question 06</span>
          <span class="q-title">Workshop Job Cards &amp; Dial Gauge Runout Tolerances</span>
        </div>
        <div class="q-verbatim">
          &ldquo;Aapke Pune service center me jab koi clutch reconditioning ya crankshaft turning hoti hai, toh QC clearance ke liye kya runout standard follow hota hai? (&lt;0.05mm?) Kya technician ko 100-cycle pressure hold test ki report sign karke upload karna mandatory karna hai?&rdquo;
        </div>
        <div class="q-intent">
          <strong>Architectural Intent:</strong> Sets digital quality checklist parameters for ERP Module 23 (Reconditioning Ledger) and Module 21 (Inward GRN Engine) to ensure full warranty compliance.
        </div>
      </div>

      <!-- Question 7 -->
      <div class="question-card">
        <div class="question-header">
          <span class="q-badge">Question 07</span>
          <span class="q-title">Multi-Location Stock Segmentation &amp; Bin Tracking</span>
        </div>
        <div class="q-verbatim">
          &ldquo;Stock physically kitni jagah divide rehta hai? (Pune Central Warehouse, Chakan Staging Yard, ya on-site client locations?) Kya storekeeper ko bin-level tracking (Rack, Shelf, Bin) chahiye ya overall warehouse count kafi hai?&rdquo;
        </div>
        <div class="q-intent">
          <strong>Architectural Intent:</strong> Structures the multi-location perpetual inventory model in ERP Module 18 (Real-Time Stock Ledger &amp; Bin Management).
        </div>
      </div>

      <!-- Category D -->
      <div class="section-header blue" style="margin-top:10px; margin-bottom:7px;">
        <span class="section-title">Category D: Financial Governance, Milestones &amp; GST Compliance (Modules 26&ndash;33)</span>
        <span class="section-tag">Ledger &amp; Tax Governance</span>
      </div>

      <!-- Question 8 -->
      <div class="question-card">
        <div class="question-header">
          <span class="q-badge" style="background:#1e3a8a;">Question 08</span>
          <span class="q-title">Commercial Discount Hierarchy &amp; Gross Margin Floors</span>
        </div>
        <div class="q-verbatim">
          &ldquo;Sales engineer ko quotation banate waqt kitna percent discount dene ki authority hai? Aur kya 22% ya 20% gross margin se neeche quote lock ho jana chahiye jab tak aap (MD) personally approve na karein?&rdquo;
        </div>
        <div class="q-intent">
          <strong>Architectural Intent:</strong> Configures permission bitmasks in ERP Module 07 (Customer Discount Matrix) and sets hard approval thresholds to prevent margin slippage.
        </div>
      </div>

      <!-- Question 9 -->
      <div class="question-card">
        <div class="question-header">
          <span class="q-badge" style="background:#1e3a8a;">Question 09</span>
          <span class="q-title">Payment Milestone Locks on Delivery Challan &amp; e-Way Bills</span>
        </div>
        <div class="q-verbatim">
          &ldquo;Machinery aur clutch dispatch ke waqt kya rule hai? (Example: 30% advance, 50% before loading/dispatch, 20% after installation). Kya ERP me rule banayein ki jab tak accounts team 50% payment received mark na kare, tab tak Rule 55 Delivery Challan aur e-Way Bill print na ho sake?&rdquo;
        </div>
        <div class="q-intent">
          <strong>Architectural Intent:</strong> Enforces automated dispatch blocks in ERP Module 22 (Outward Delivery Challan) and Module 28 (Accounts Receivable Sentinel) to eliminate bad debt.
        </div>
      </div>

      <!-- Question 10 -->
      <div class="question-card">
        <div class="question-header">
          <span class="q-badge" style="background:#1e3a8a;">Question 10</span>
          <span class="q-title">Accounting Software Integration &amp; GSTR-1 Reconciliation</span>
        </div>
        <div class="q-verbatim">
          &ldquo;Aapki accounts team abhi Tally, Busy ya koi aur software use karti hai GSTR-1 aur balance sheet ke liye? Kya ERP se direct one-click JSON/Excel export chahiye jise wo direct GST portal ya apne CA ko bhej sakein?&rdquo;
        </div>
        <div class="q-intent">
          <strong>Architectural Intent:</strong> Formats data export schemas in ERP Module 26 (GST Tax Invoice) and Module 27 (GSTR-1 Reconciliation Exporter) for accounting compatibility.
        </div>
      </div>

    </div>
    {get_footer(3)}
  </div>
"""
pages.append(p3)

# ==============================================================================
# PAGE 4: OBJECTION HANDLING, CHEAT-SHEET & ACTION CHECKLIST
# ==============================================================================
p4 = f"""
  <div class="page">
    <div class="page-content">
      {get_header("OBJECTION HANDLING &amp; ACTION PROTOCOL")}
      
      <!-- Objection Handling Table -->
      <div class="section-header" style="background:#0f172a; margin-bottom:7px;">
        <span class="section-title">Executive Objection Handling Matrix &bull; Real-Time Strategic Responses</span>
        <span class="section-tag">Consulting Authority</span>
      </div>

      <table class="matrix-table" style="font-size:8.3pt; margin-bottom:10px;">
        <thead>
          <tr>
            <th style="width:32%; padding:6px 8px;">Potential Client Question / Concern</th>
            <th style="width:68%; padding:6px 8px;">Suyash's Strategic Architectural Response</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td style="font-weight:700; color:#0f172a; padding:7px 9px;">
              &ldquo;Website toh simple honi chahiye, itne 24 pages ki kya zaroorat hai?&rdquo;
            </td>
            <td style="padding:7px 9px; line-height:1.36;">
              &ldquo;Vinit ji, simple brochure websites 5-ton presses ke local broker banati hain. Dalal 2000T&ndash;4000T heavy forging presses deal karta hai jahan deal size &pound;100k se &euro;500k hoti hai. Institutional buyer aur bank valuers ko jab tak engineering specs, ground stock verification aur OMPI technical capabilities nahi dikhegi, wo Pune aane ka decision nahi lenge.&rdquo;
            </td>
          </tr>
          <tr>
            <td style="font-weight:700; color:#0f172a; padding:7px 9px;">
              &ldquo;ERP hum baad me sochenge, pehle sirf website live karte hain.&rdquo;
            </td>
            <td style="padding:7px 9px; line-height:1.36;">
              &ldquo;Bilkul theek approach hai Vinit ji. Isliye humne pure scope ko 2 distinct phases me plan kiya hai: Phase 1 me Dalal ke 24 Web Routes live honge jo inbound RFQs layenge, aur Phase 2 me OMPI ke core modules (Costing, Invoicing, Spares) rollout honge. Aaj meeting me hum sirf architecture validate kar rahe hain taaki kal jakar rebuild na karna pade.&rdquo;
            </td>
          </tr>
          <tr>
            <td style="font-weight:700; color:#0f172a; padding:7px 9px;">
              &ldquo;Total implementation cost aur timeline kya rahegi?&rdquo;
            </td>
            <td style="padding:7px 9px; line-height:1.36;">
              &ldquo;Hamare paas complete 57 units ka modular architecture blueprint ready hai. Phase 1 (Dalal Web Platform) 3 se 4 weeks me production-ready deploy ho jayega. ERP modules sprint-wise roll out honge. Aaj ke discovery inputs ke basis par hum exact milestone commercial schedule agree kar lenge.&rdquo;
            </td>
          </tr>
        </tbody>
      </table>

      <!-- Pre-Meeting Readiness Checklist -->
      <div style="border:1.5px solid #cbd5e1; border-radius:6px; padding:8px 12px; background:#f8fafc; margin-bottom:10px;">
        <div style="font-size:8.6pt; font-weight:800; color:#0f172a; text-transform:uppercase; letter-spacing:0.5px; margin-bottom:5px; border-bottom:1px solid #e2e8f0; padding-bottom:3px;">
          Pre-Meeting Preparation Checklist (What to Carry Tomorrow)
        </div>
        <div style="display:grid; grid-template-columns:1fr 1fr; gap:8px; font-size:8.2pt; line-height:1.35;">
          <div style="background:#ffffff; border:1px solid #e2e8f0; border-radius:4px; padding:6px 8px;">
            <strong style="color:#0f172a; display:block; margin-bottom:2px;">1. Master Specification Manual:</strong>
            Carry a printed copy or iPad with <strong>DALAL_AND_OMPI_57_PAGES_AND_MODULES_MASTER_SPECIFICATION.pdf</strong> (32 Pages, Large Font) to show complete architectural preparedness.
          </div>
          <div style="background:#ffffff; border:1px solid #e2e8f0; border-radius:4px; padding:6px 8px;">
            <strong style="color:#0f172a; display:block; margin-bottom:2px;">2. Live Interactive Prototype:</strong>
            Have <strong>index.html</strong> and <strong>category.html</strong> loaded locally on laptop browser to demonstrate 2x2 crosshair spec grids, compare selectors, and instant WhatsApp payloads.
          </div>
          <div style="background:#ffffff; border:1px solid #e2e8f0; border-radius:4px; padding:6px 8px;">
            <strong style="color:#0f172a; display:block; margin-bottom:2px;">3. Note-Taking Discipline:</strong>
            Actively note specific HSN codes, average order values, and credit terms in front of the client. This reinforces your position as a seasoned Principal Architect.
          </div>
          <div style="background:#ffffff; border:1px solid #e2e8f0; border-radius:4px; padding:6px 8px;">
            <strong style="color:#0f172a; display:block; margin-bottom:2px;">4. Clear Closing Next Steps:</strong>
            Conclude the meeting by agreeing to send an updated Scope of Work (SOW) and Phase 1 delivery milestone contract within 24 hours based on their answers.
          </div>
        </div>
      </div>

      <!-- Action Footer Box -->
      <div style="background:#0f172a; color:#ffffff; border-radius:6px; padding:8px 12px; display:flex; justify-content:space-between; align-items:center;">
        <div>
          <div style="font-size:7.4pt; font-weight:800; color:#f59e0b; text-transform:uppercase; letter-spacing:0.5px;">Client Consultation Baseline</div>
          <div style="font-size:9.0pt; font-weight:700; margin-top:1px;">Prepared for On-Site Executive Alignment &bull; Dalal &amp; OMPI India</div>
        </div>
        <div style="text-align:right; font-size:8.0pt; color:#94a3b8;">
          Architect: <strong style="color:#ffffff;">Suyash Shinde</strong><br>
          +91 96070 28594 &bull; Pimpri, Pune
        </div>
      </div>

    </div>
    {get_footer(4)}
  </div>
"""
pages.append(p4)

# ==============================================================================
# MASTER HTML WRAPPER
# ==============================================================================
full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Dalal &amp; OMPI India - Executive Client Meeting Playbook &amp; Discovery Questions</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;600;700&display=swap" rel="stylesheet">
  <style>
    @page {{
      size: A4 portrait;
      margin: 8mm 10mm 8mm 10mm;
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
      font-size: 9.2pt;
      line-height: 1.40;
      -webkit-print-color-adjust: exact;
      print-color-adjust: exact;
    }}
    .page {{
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
      border-top: 3.5px solid #d97706;
      padding-top: 4px;
      padding-bottom: 5px;
      margin-bottom: 8px;
    }}
    .brand-title {{
      font-size: 13.0pt;
      font-weight: 800;
      color: #0f172a;
      letter-spacing: -0.3px;
      text-transform: uppercase;
    }}
    .brand-subtitle {{
      font-size: 8.2pt;
      font-weight: 700;
      color: #b45309;
      text-transform: uppercase;
      letter-spacing: 0.8px;
      margin-top: 2px;
    }}
    .doc-meta {{
      text-align: right;
      font-size: 7.8pt;
      color: #64748b;
      line-height: 1.35;
    }}
    .doc-meta strong {{
      color: #0f172a;
      font-weight: 700;
    }}

    /* Section Header */
    .section-header {{
      background: #0f172a;
      color: #ffffff;
      padding: 5px 10px;
      border-radius: 4px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 8px;
    }}
    .section-header.blue {{
      background: #1e3a8a;
    }}
    .section-title {{
      font-size: 9.6pt;
      font-weight: 800;
      letter-spacing: 0.4px;
      text-transform: uppercase;
    }}
    .section-tag {{
      font-size: 8.0pt;
      font-weight: 700;
      color: #f59e0b;
      letter-spacing: 0.6px;
      text-transform: uppercase;
    }}

    /* Question Cards */
    .question-card {{
      background: #ffffff;
      border: 1.3px solid #cbd5e1;
      border-radius: 5px;
      padding: 7px 10px;
      margin-bottom: 7px;
    }}
    .question-header {{
      display: flex;
      align-items: center;
      margin-bottom: 3.5px;
    }}
    .q-badge {{
      background: #0f172a;
      color: #ffffff;
      font-size: 7.6pt;
      font-weight: 800;
      padding: 2px 6px;
      border-radius: 3px;
      text-transform: uppercase;
      letter-spacing: 0.4px;
      font-family: 'JetBrains Mono', monospace;
      margin-right: 7px;
    }}
    .q-title {{
      font-size: 9.6pt;
      font-weight: 800;
      color: #0f172a;
    }}
    .q-verbatim {{
      background: #f8fafc;
      border-left: 3.5px solid #d97706;
      padding: 5px 8px;
      border-radius: 3px;
      font-size: 8.8pt;
      font-weight: 600;
      color: #0f172a;
      line-height: 1.35;
      margin-bottom: 3.5px;
    }}
    .q-intent {{
      font-size: 8.0pt;
      color: #475569;
      line-height: 1.30;
    }}
    .q-intent strong {{
      color: #0f172a;
    }}

    /* Running Footer */
    .doc-footer {{
      border-top: 1.5px solid #e2e8f0;
      padding-top: 4px;
      font-size: 7.8pt;
      color: #64748b;
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-top: 4px;
    }}
    .doc-footer strong {{
      color: #0f172a;
    }}

    /* Matrix Table */
    table.matrix-table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 8.2pt;
      margin-top: 4px;
    }}
    table.matrix-table th, table.matrix-table td {{
      border: 1px solid #cbd5e1;
      padding: 4px 7px;
      text-align: left;
      vertical-align: middle;
    }}
    table.matrix-table th {{
      background: #0f172a;
      color: #ffffff;
      font-size: 7.6pt;
      text-transform: uppercase;
      font-weight: 700;
      letter-spacing: 0.4px;
    }}
    table.matrix-table tr:nth-child(even) td {{
      background: #f8fafc;
    }}
  </style>
</head>
<body>
{"".join(pages)}
</body>
</html>
"""

with open(out_html, 'w', encoding='utf-8') as f:
    f.write(full_html)

print(f"Generated {out_html} ({len(pages)} pages).")

