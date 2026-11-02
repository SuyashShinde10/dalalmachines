with open('scratch/build_balanced_master_spec.py', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Give cards 13px 16px padding and 11px margin-bottom so pages 3 & 4 have 55-65pt buffer
text = text.replace('margin-bottom: 14px;\n      padding: 15px 18px;', 'margin-bottom: 11px;\n      padding: 13px 16px;')

# 2. Enrich Page 32
old_p32_body = """      <!-- Implementation Summary & Phasing Table -->
      <div style="background:#f8fafc; border:1.5px solid #cbd5e1; border-radius:7px; padding:10px 14px; margin-bottom:10px;">
        <div style="font-size:9.0pt; font-weight:800; color:#0f172a; text-transform:uppercase; margin-bottom:4px;">
          Commercial Phasing &amp; Proposed Delivery Milestones
        </div>
        <table style="width:100%; border-collapse:collapse; font-size:8.4pt; line-height:1.38; color:#334155;">
          <thead>
            <tr style="background:#0f172a; color:#ffffff; text-align:left;">
              <th style="padding:4px 8px;">Milestone Phase</th>
              <th style="padding:4px 8px;">Proposed Scope of Delivery</th>
              <th style="padding:4px 8px;">Status</th>
            </tr>
          </thead>
          <tbody>
            <tr style="border-bottom:1px solid #e2e8f0; background:#ffffff;">
              <td style="padding:5px 8px; font-weight:700;">Phase 1 (Kickoff Scope)</td>
              <td style="padding:5px 8px;">Dalal 24 Public Pages &bull; Staff Admin Portal &bull; Director Console &bull; Core Quoting Tools</td>
              <td style="padding:5px 8px; font-weight:700; color:#b45309;">TO COMMENCE UPON SIGN-OFF</td>
            </tr>
            <tr style="background:#ffffff;">
              <td style="padding:5px 8px; font-weight:700;">Phase 2 (ERP Rollout)</td>
              <td style="padding:5px 8px;">OMPI Standalone ERP Modules (7 Monthly Sprints: Customer 360, Italy POs, BOM, Godown Bins, GSTR-1)</td>
              <td style="padding:5px 8px; font-weight:700; color:#64748b;">SCHEDULED SPRINT ROADMAP</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Non-Disclosure Confirmation & Executive Sign-Off -->
      <div style="border:1.5px solid #e11d48; background:#fff1f2; border-radius:7px; padding:10px 14px; margin-bottom:10px;">
        <div style="font-size:8.8pt; font-weight:800; color:#9f1239; text-transform:uppercase; margin-bottom:2px;">
          &#128274; Confidentiality &amp; Pre-Commencement Approval Acknowledgment
        </div>
        <p style="font-size:8.3pt; line-height:1.4; color:#4c0519;">
          This master specification represents the proprietary intellectual property and proposed operational architecture of Dalal Machine Tools Agency Pvt. Ltd. and OMPI India LLP. Work has not commenced. External sharing, copying, or forwarding without written authorization is strictly forbidden.
        </p>
      </div>

      <!-- Signatures Grid -->
      <div style="display:grid; grid-template-columns:1fr 1fr; gap:14px; border-top:1.5px solid #0f172a; padding-top:8px;">
        <div style="font-size:8.5pt; line-height:1.38; color:#334155;">
          <strong>Accepted &amp; Approved to Commence Work:</strong><br><br>
          __________________________________________<br>
          <strong>Mr. Vinit Dalal</strong> &bull; Managing Director / Partner
        </div>
        <div style="font-size:8.5pt; line-height:1.38; color:#334155; text-align:right;">
          <strong>Submitted by Principal Software Consultant:</strong><br><br>
          __________________________________________<br>
          <strong>Suyash Shinde</strong> &bull; Pimpri, Pune, Maharashtra
        </div>
      </div>"""

new_p32_body = """      <!-- Implementation Summary & Phasing Table -->
      <div style="background:#f8fafc; border:1.5px solid #cbd5e1; border-radius:7px; padding:10px 14px; margin-bottom:11px;">
        <div style="font-size:9.0pt; font-weight:800; color:#0f172a; text-transform:uppercase; margin-bottom:5px;">
          Commercial Phasing &amp; Proposed Delivery Milestones
        </div>
        <table style="width:100%; border-collapse:collapse; font-size:8.4pt; line-height:1.38; color:#334155;">
          <thead>
            <tr style="background:#0f172a; color:#ffffff; text-align:left;">
              <th style="padding:5px 8px;">Milestone Phase</th>
              <th style="padding:5px 8px;">Proposed Scope of Delivery</th>
              <th style="padding:5px 8px;">Timeline &amp; Status</th>
            </tr>
          </thead>
          <tbody>
            <tr style="border-bottom:1px solid #e2e8f0; background:#ffffff;">
              <td style="padding:5px 8px; font-weight:700;">Phase 1 (Kickoff Scope)</td>
              <td style="padding:5px 8px;">Dalal 24 Public Pages &bull; Staff Admin Portal &bull; WhatsApp Lead Routing &bull; Quoting Tools</td>
              <td style="padding:5px 8px; font-weight:700; color:#b45309;">TO COMMENCE UPON SIGN-OFF</td>
            </tr>
            <tr style="border-bottom:1px solid #e2e8f0; background:#f8fafc;">
              <td style="padding:5px 8px; font-weight:700;">Phase 2 (OMPI Core ERP)</td>
              <td style="padding:5px 8px;">OMPI Customer Master &bull; Italian SKU Catalog &bull; Landed Pricing &bull; Godown Stock Tracker</td>
              <td style="padding:5px 8px; font-weight:700; color:#475569;">MONTH 1-2 SPRINT ROADMAP</td>
            </tr>
            <tr style="background:#ffffff;">
              <td style="padding:5px 8px; font-weight:700;">Phase 3 (Enterprise Control)</td>
              <td style="padding:5px 8px;">Workshop Overhaul Job Cards &bull; GST Invoicing &bull; Port Demurrage Shield &bull; MD Command Desk</td>
              <td style="padding:5px 8px; font-weight:700; color:#475569;">MONTH 3-4 SPRINT ROADMAP</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Formal Authorization & Commencement Terms Box -->
      <div style="background:#ffffff; border:1.5px solid #0f172a; border-radius:7px; padding:10px 14px; margin-bottom:10px;">
        <div style="font-size:8.8pt; font-weight:800; color:#0f172a; text-transform:uppercase; margin-bottom:4px;">
          Formal Commencement Authorization &amp; Quality Acceptance Terms
        </div>
        <p style="font-size:8.3pt; line-height:1.42; color:#334155;">
          By formal execution below, executive leadership authorizes the commencement of Milestone Phase 1. Development will strictly adhere to the operational specifications detailed across this 57-unit master document. Each phase requires structured shop floor acceptance testing prior to commercial release.
        </p>
      </div>

      <!-- Non-Disclosure Confirmation & Executive Sign-Off -->
      <div style="border:1.5px solid #e11d48; background:#fff1f2; border-radius:7px; padding:9px 14px; margin-bottom:10px;">
        <div style="font-size:8.6pt; font-weight:800; color:#9f1239; text-transform:uppercase; margin-bottom:2px;">
          &#128274; Confidentiality &amp; Proprietary Architecture Covenant
        </div>
        <p style="font-size:8.2pt; line-height:1.38; color:#4c0519;">
          This master specification represents the proprietary intellectual property and proposed operational architecture of Dalal Machine Tools Agency Pvt. Ltd. and OMPI India LLP. External sharing, copying, forwarding, or unauthorized reproduction without prior written approval is strictly prohibited by law.
        </p>
      </div>

      <!-- Signatures Grid -->
      <div style="display:grid; grid-template-columns:1fr 1fr; gap:16px; border-top:1.5px solid #0f172a; padding-top:10px;">
        <div style="font-size:8.5pt; line-height:1.4; color:#334155;">
          <strong>Accepted &amp; Approved to Commence Work:</strong><br><br>
          __________________________________________<br>
          <strong>Mr. Vinit Dalal</strong> &bull; Managing Director / Partner<br>
          <span style="font-size:7.8pt; color:#64748b;">Dalal Machine Tools Agency Pvt. Ltd. &amp; OMPI India LLP</span>
        </div>
        <div style="font-size:8.5pt; line-height:1.4; color:#334155; text-align:right;">
          <strong>Submitted by Principal Software Consultant:</strong><br><br>
          __________________________________________<br>
          <strong>Suyash Shinde</strong> &bull; Principal Software Consultant<br>
          <span style="font-size:7.8pt; color:#64748b;">Pimpri, Pune, Maharashtra, India</span>
        </div>
      </div>"""

if old_p32_body in text:
    text = text.replace(old_p32_body, new_p32_body)
    print("Enriched Page 32 perfectly!")
else:
    print("Could not find old_p32_body")

with open('scratch/build_balanced_master_spec.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("Saved scratch/build_balanced_master_spec.py")

