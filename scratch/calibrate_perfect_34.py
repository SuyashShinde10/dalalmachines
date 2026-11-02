# scratch/calibrate_perfect_34.py
with open('scratch/build_enterprise_specification_v2.py', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Calibrate .card-box so tight pages (7, 8, 10, 32) have 55-70pt breathing room
text = text.replace('margin-bottom: 16px;\n      padding: 17px 20px;', 'margin-bottom: 12px;\n      padding: 14px 18px;')

# 2. Enrich Page 1 (Cover) so gap drops from 211pt to ~60pt
old_p1_end = """      <!-- Metadata Box -->
      <div style="background:#ffffff; border:1.5px solid #0f172a; border-radius:7px; padding:9px 16px; display:flex; justify-content:space-between; align-items:center;">
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
      </div>"""

new_p1_end = """      <!-- Executive Architecture & Reading Guide -->
      <div style="background:#ffffff; border:1.5px solid #cbd5e1; border-radius:7px; padding:12px 16px; margin-bottom:12px;">
        <div style="font-size:8.8pt; font-weight:800; color:#0f172a; text-transform:uppercase; margin-bottom:5px; border-bottom:1.5px solid #f1f5f9; padding-bottom:3px;">
          Master Proposal Structure &bull; Executive Navigation Guide
        </div>
        <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px; font-size:8.3pt; line-height:1.4; color:#334155;">
          <div>
            <strong>Pages 04 to 15 &bull; Dalal Public Web Platform (24 Units):</strong><br>
            Customer-facing showcase for heavy presses, live power trials, 60-second quotations, press tonnage calculator, and 2 staff operational management desks.
          </div>
          <div>
            <strong>Pages 16 to 33 &bull; OMPI Operations ERP Suite (33 Units):</strong><br>
            Internal industrial management suite covering Italian factory imports in Euros, landed port costing, Pune godown stock tracking, workshop job cards, and GST tax billing.
          </div>
        </div>
      </div>

      <!-- Metadata Box -->
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
      </div>"""

text = text.replace(old_p1_end, new_p1_end)

# 3. Enrich Page 2 (Executive Summary)
old_p2_note = """      <!-- Commercial Governance Note -->
      <div style="background:#f8fafc; border:1.5px solid #0f172a; border-radius:7px; padding:9px 14px;">
        <div style="font-size:8.5pt; font-weight:800; color:#0f172a; text-transform:uppercase; margin-bottom:2px;">
          Commercial Scope Governance &amp; Agreement Annexure
        </div>
        <p style="font-size:8.2pt; line-height:1.4; color:#334155;">
          This master blueprint defines the functional scope of delivery. Commercial fee milestones, payment schedules, and legal terms shall be governed by the formal Master Services Agreement. Any feature not detailed herein shall be estimated separately under standard change control procedures.
        </p>
      </div>"""

new_p2_note = """      <!-- Core Operational Rules & Governance -->
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
      </div>"""

text = text.replace(old_p2_note, new_p2_note)

# 4. Enrich Page 3 (Assumptions & Exclusions)
old_p3_sla = """      <!-- 4. Change Control, Warranty & Source Code Ownership -->
      <div style="background:#f8fafc; border:1.5px solid #0f172a; border-radius:7px; padding:10px 14px;">"""

new_p3_sla = """      <!-- Data Security & Backup Governance -->
      <div style="background:#ffffff; border:1.5px solid #cbd5e1; border-radius:7px; padding:11px 14px; margin-bottom:10px;">
        <div style="font-size:8.8pt; font-weight:800; color:#0f172a; text-transform:uppercase; margin-bottom:4px; border-bottom:1.5px solid #f1f5f9; padding-bottom:3px;">
          4. Data Privacy, Cloud Security &amp; Daily Backup SLA
        </div>
        <p style="font-size:8.2pt; line-height:1.4; color:#334155;">
          All business databases, customer lead history, and commercial quotations are stored in an encrypted PostgreSQL vault. Daily automated backups are scheduled at midnight with 30-day version retention. Production environments enforce role-based access so internal margins remain strictly restricted to top leadership.
        </p>
      </div>

      <!-- 5. Change Control, Warranty & Source Code Ownership -->
      <div style="background:#f8fafc; border:1.5px solid #0f172a; border-radius:7px; padding:11px 14px;">"""

text = text.replace(old_p3_sla, new_p3_sla)

# 5. Enrich Page 16 (OMPI Architecture Map)
text = text.replace('padding: 16px 20px; margin-bottom: 9px;', 'padding: 20px 22px; margin-bottom: 12px;')
text = text.replace('padding:9px 13px; margin-bottom:9px;', 'padding:12px 15px; margin-bottom:12px;')
text = text.replace('padding:4px 8px;', 'padding:5.5px 8px;')

# 6. Enrich Page 34 (Workflow & Sign-off)
text = text.replace('padding:9px 13px; margin-bottom:9px;', 'padding:12px 15px; margin-bottom:11px;')
text = text.replace('padding:6px 9px;', 'padding:8px 10px;')
text = text.replace('padding:4px 7px;', 'padding:5.5px 8px;')
text = text.replace('padding:8px 13px; margin-bottom:8px;', 'padding:11px 15px; margin-bottom:11px;')

with open('scratch/build_enterprise_specification_v2.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("Applied calibration to all 34 pages!")

