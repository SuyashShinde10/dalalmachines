# scratch/generate_executive_client_guide.py
import os, subprocess, shutil

print("Writing full 32-page plain-language specification generator...")

pages_data = []

# Page 1: Executive Cover & Non-Disclosure Notice
p1 = """
    <div class="header-bar">
      <div>
        <div class="brand-title">DALAL MACHINE TOOLS AGENCY &amp; OMPI INDIA</div>
        <div class="brand-subtitle">EXECUTIVE BUSINESS GUIDE &bull; 57 OPERATIONAL SYSTEMS &amp; MODULES</div>
      </div>
      <div class="doc-meta">
        <strong>Doc Ref:</strong> EXEC-GUIDE-2026-DALAL-OMPI-57<br>
        <strong>Classification:</strong> Strictly Confidential &amp; Proprietary<br>
        <strong>Language Edition:</strong> Plain Business English (Non-Technical)
      </div>
    </div>
    
    <div class="confidential-bar">
      <div>&#9888; STRICTLY CONFIDENTIAL &bull; PROPRIETARY BUSINESS INTELLECTUAL PROPERTY &bull; NOT FOR EXTERNAL SHARING</div>
      <div class="confidential-tag">STRICTLY PRIVATE</div>
    </div>

    <!-- Legal Non-Disclosure Notice -->
    <div style="background:#fff1f2; border:2px solid #e11d48; border-radius:6px; padding:10px 14px; margin-bottom:12px;">
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
    <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px; background:#f8fafc; border:1.5px solid #cbd5e1; border-radius:6px; padding:10px 12px; margin-bottom:12px;">
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
    <div style="background:#ffffff; border:1.5px solid #e2e8f0; border-radius:6px; padding:10px 12px; margin-bottom:12px;">
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
"""

pages_data.append(p1)
print("Page 1 ready.")

