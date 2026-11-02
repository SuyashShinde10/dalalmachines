# scratch/build_clean_executive_spec.py
import os, subprocess, shutil

print("Assembling all 32 pages of the Simple Plain-Language Executive Guide...")

# Helper functions for card generation
def make_header(subtitle, doc_ref="EXEC-GUIDE-2026-DALAL-OMPI-57"):
    return f"""
    <div class="header-bar">
      <div>
        <div class="brand-title">DALAL MACHINE TOOLS AGENCY &amp; OMPI INDIA</div>
        <div class="brand-subtitle">{subtitle}</div>
      </div>
      <div class="doc-meta">
        <strong>Doc Ref:</strong> {doc_ref}<br>
        <strong>Classification:</strong> Strictly Confidential &amp; Proprietary<br>
        <strong>Language Edition:</strong> Plain Business English (Non-Technical)
      </div>
    </div>
    <div class="confidential-bar">
      <div>&#9888; STRICTLY CONFIDENTIAL: PROPRIETARY BUSINESS BLUEPRINT &bull; FOR INTERNAL MANAGEMENT USE ONLY</div>
      <div class="confidential-tag">DO NOT SHARE OR DISTRIBUTE</div>
    </div>
"""

def make_footer(page_num, total_pages=32):
    return f"""
    <div class="footer-bar">
      <div><strong>Dalal Machine Tools Agency Pvt. Ltd. &amp; OMPI India LLP</strong> &bull; Commercial Operations</div>
      <div class="confidential-watermark">CONFIDENTIAL &bull; STRICTLY NOT FOR SHARING</div>
      <div>Page {page_num} of {total_pages}</div>
    </div>
"""

def make_route_card(rid, title, path, audience, what_buyer_sees, business_benefit, key_feature, is_live=True):
    status_badge = '<span class="card-status status-live">&#10003; LIVE &amp; ACTIVE</span>' if is_live else '<span class="card-status status-phase2">PHASE 2 ROADMAP</span>'
    return f"""
      <div class="card-box">
        <div class="card-header">
          <div>
            <span class="badge-id">{rid}</span>
            <span class="card-title">{title}</span>
            {status_badge}
          </div>
          <div class="card-path">{path}</div>
        </div>
        <div style="font-size:7.5pt; color:#64748b; font-weight:700; margin-bottom:5px;">
          <strong>Target User / Audience:</strong> {audience}
        </div>
        <div class="simple-grid">
          <div>
            <div class="grid-label">What The Customer Sees on Screen</div>
            <div class="grid-text">{what_buyer_sees}</div>
          </div>
          <div>
            <div class="grid-label">Why It Exists &amp; How It Brings Business</div>
            <div class="grid-text">{business_benefit}</div>
          </div>
        </div>
        <div class="feature-strip">
          <strong>Key Business Feature:</strong> {key_feature}
        </div>
      </div>
"""

def make_module_card(mid, title, engine, role, what_it_does, business_benefit, key_feature, is_live=True):
    status_badge = '<span class="card-status status-live">&#10003; LIVE IN SYSTEM</span>' if is_live else '<span class="card-status status-phase2">PHASE 2 DEPLOYMENT</span>'
    return f"""
      <div class="card-box">
        <div class="card-header">
          <div>
            <span class="badge-id">{mid}</span>
            <span class="card-title">{title}</span>
            {status_badge}
          </div>
          <div style="font-size:7.4pt; font-weight:700; color:#b45309; background:#fffbeb; padding:2px 6px; border:1px solid #fef3c7; border-radius:3px;">{engine}</div>
        </div>
        <div style="font-size:7.5pt; color:#64748b; font-weight:700; margin-bottom:5px;">
          <strong>Responsible Staff Role:</strong> {role}
        </div>
        <div class="simple-grid">
          <div>
            <div class="grid-label">What This Module Does in Daily Work</div>
            <div class="grid-text">{what_it_does}</div>
          </div>
          <div>
            <div class="grid-label">Business Value &amp; Risk Prevented</div>
            <div class="grid-text">{business_benefit}</div>
          </div>
        </div>
        <div class="feature-strip">
          <strong>Key Operation:</strong> {key_feature}
        </div>
      </div>
"""

print("Helper functions ready.")
