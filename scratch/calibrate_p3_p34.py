# scratch/calibrate_p3_p34.py
with open('scratch/build_enterprise_specification_v2.py', 'r', encoding='utf-8') as f:
    text = f.read()

# Fix numbering on Page 3
text = text.replace('4. Change Request Policy, Warranty &amp; Source Code Ownership', '5. Change Request Policy, Warranty &amp; Source Code Ownership')

# Enrich Page 3 boxes padding and text
old_p3_box1 = '''      <!-- 1. Third Party Subscriptions Box -->
      <div style="background:#ffffff; border:1.5px solid #cbd5e1; border-radius:7px; padding:15px 18px; margin-bottom:13px;">'''
new_p3_box1 = '''      <!-- 1. Third Party Subscriptions Box -->
      <div style="background:#ffffff; border:1.5px solid #cbd5e1; border-radius:7px; padding:15px 18px; margin-bottom:13px;">'''
# Let's enrich box 3 and 4
old_p3_content = '''      <!-- 3. Client Content & Data Responsibilities -->
      <div style="background:#ffffff; border:1.5px solid #cbd5e1; border-radius:7px; padding:15px 18px; margin-bottom:13px;">
        <div style="font-size:9.0pt; font-weight:800; color:#0f172a; text-transform:uppercase; margin-bottom:4px; border-bottom:1.5px solid #f1f5f9; padding-bottom:3px;">
          3. Content, Data &amp; Legal Text Responsibilities
        </div>
        <p style="font-size:8.3pt; line-height:1.4; color:#334155;">
          The timely delivery of the software depends on the Client providing required data and media: (a) High-resolution machinery photos, nameplate data, and power trial video links; (b) Italian OMPI catalog spreadsheets and dimensional cross-indexes; (c) High Seas Sales contracts and legal text vetted by Client's chartered accountant or maritime counsel.
        </p>
      </div>'''

new_p3_content = '''      <!-- 3. Client Content & Data Responsibilities -->
      <div style="background:#ffffff; border:1.5px solid #cbd5e1; border-radius:7px; padding:14px 18px; margin-bottom:12px;">
        <div style="font-size:9.0pt; font-weight:800; color:#0f172a; text-transform:uppercase; margin-bottom:4px; border-bottom:1.5px solid #f1f5f9; padding-bottom:3px;">
          3. Content, Data &amp; Legal Text Responsibilities (Client Deliverables)
        </div>
        <p style="font-size:8.4pt; line-height:1.45; color:#334155;">
          The timely delivery of the software suite depends on the Client providing required business assets: (a) High-resolution machinery photographs, nameplate specifications, and power trial video links for Pune stock; (b) Italian OMPI catalog spreadsheets, technical dimensional diagrams, and price cross-indexes; (c) High Seas Sales agreements and legal declaration text vetted by the Client's chartered accountant or maritime trade counsel.
        </p>
      </div>'''
text = text.replace(old_p3_content, new_p3_content)

p3_security_target = '''      <!-- Data Security & Backup Governance -->
      <div style="background:#ffffff; border:1.5px solid #cbd5e1; border-radius:7px; padding:11px 14px; margin-bottom:10px;">
        <div style="font-size:8.8pt; font-weight:800; color:#0f172a; text-transform:uppercase; margin-bottom:4px; border-bottom:1.5px solid #f1f5f9; padding-bottom:3px;">
          4. Data Privacy, Cloud Security &amp; Daily Backup SLA
        </div>
        <p style="font-size:8.2pt; line-height:1.4; color:#334155;">
          All business databases, customer lead history, and commercial quotations are stored in an encrypted PostgreSQL vault. Daily automated backups are scheduled at midnight with 30-day version retention. Production environments enforce role-based access so internal margins remain strictly restricted to top leadership.
        </p>
      </div>'''

p3_security_replacement = '''      <!-- 4. Data Security & Backup Governance -->
      <div style="background:#ffffff; border:1.5px solid #cbd5e1; border-radius:7px; padding:13px 18px; margin-bottom:12px;">
        <div style="font-size:9.0pt; font-weight:800; color:#0f172a; text-transform:uppercase; margin-bottom:4px; border-bottom:1.5px solid #f1f5f9; padding-bottom:3px;">
          4. Data Privacy, Cloud Security &amp; Daily Automated Backup SLA
        </div>
        <p style="font-size:8.4pt; line-height:1.45; color:#334155;">
          All business databases, customer lead history, and commercial quotations are stored in an encrypted PostgreSQL relational database. Daily automated snapshots are executed at midnight with a 30-day version retention policy. Production environments enforce role-based permission boundaries so internal landing costs and margin spreadsheets remain strictly restricted to executive management.
        </p>
      </div>'''
text = text.replace(p3_security_target, p3_security_replacement)

# Page 3 box 5
old_p3_box5 = '''      <!-- 5. Change Control, Warranty & Source Code Ownership -->
      <div style="background:#f8fafc; border:1.5px solid #0f172a; border-radius:7px; padding:11px 14px;">'''
new_p3_box5 = '''      <!-- 5. Change Control, Warranty & Source Code Ownership -->
      <div style="background:#f8fafc; border:1.5px solid #0f172a; border-radius:7px; padding:14px 18px;">'''
text = text.replace(old_p3_box5, new_p3_box5)

# Page 34 enrichment
old_p34_wf = '''      <!-- 6-Step Workflow Box -->
      <div style="background:#ffffff; border:1.5px solid #cbd5e1; border-radius:7px; padding:12px 15px; margin-bottom:12px;">'''
new_p34_wf = '''      <!-- 6-Step Workflow Box -->
      <div style="background:#ffffff; border:1.5px solid #cbd5e1; border-radius:7px; padding:14px 18px; margin-bottom:14px;">'''
text = text.replace(old_p34_wf, new_p34_wf)

old_p34_phasing = '''      <!-- Phasing Table -->
      <div style="background:#f8fafc; border:1.5px solid #cbd5e1; border-radius:7px; padding:12px 15px; margin-bottom:12px;">
        <div style="font-size:8.8pt; font-weight:800; color:#0f172a; text-transform:uppercase; margin-bottom:4px;">
          Delivery Milestones &amp; Implementation Phasing
        </div>
        <table style="width:100%; border-collapse:collapse; font-size:8.2pt; line-height:1.36; color:#334155;">
          <thead>
            <tr style="background:#0f172a; color:#ffffff; text-align:left;">
              <th style="padding:5.5px 8px;">Milestone Phase</th>
              <th style="padding:5.5px 8px;">Scope of Deliverables</th>
              <th style="padding:5.5px 8px;">Estimated Duration</th>
              <th style="padding:5.5px 8px;">Status</th>
            </tr>
          </thead>
          <tbody>
            <tr style="border-bottom:1px solid #e2e8f0; background:#ffffff;">
              <td style="padding:5.5px 8px; font-weight:700;">Phase 1: Dalal Platform</td>
              <td style="padding:5.5px 8px;">22 Public Web Pages &bull; 2 Staff Desks &bull; WhatsApp Lead Routing &bull; Quoting Tools</td>
              <td style="padding:5.5px 8px; font-weight:600;">4 to 6 Weeks</td>
              <td style="padding:5.5px 8px; font-weight:700; color:#b45309;">TO COMMENCE UPON SIGN-OFF</td>
            </tr>
            <tr style="border-bottom:1px solid #e2e8f0; background:#f8fafc;">
              <td style="padding:5.5px 8px; font-weight:700;">Phase 2: OMPI Core ERP</td>
              <td style="padding:5.5px 8px;">Customer Master &bull; Italian SKU Catalog &bull; Landed Costing &bull; Stock Tracker</td>
              <td style="padding:5.5px 8px; font-weight:600;">8 to 10 Weeks</td>
              <td style="padding:5.5px 8px; font-weight:600; color:#475569;">MONTH 2-3 SPRINT</td>
            </tr>
            <tr style="background:#ffffff;">
              <td style="padding:5.5px 8px; font-weight:700;">Phase 3: Operations &amp; Control</td>
              <td style="padding:5.5px 8px;">Workshop Overhaul Job Cards &bull; GST Invoicing &bull; Port Tracking &bull; MD Command Desk</td>
              <td style="padding:5.5px 8px; font-weight:600;">8 to 10 Weeks</td>
              <td style="padding:5.5px 8px; font-weight:600; color:#475569;">MONTH 4-5 SPRINT</td>
            </tr>
          </tbody>
        </table>
      </div>'''

new_p34_phasing = '''      <!-- Phasing Table -->
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
text = text.replace(old_p34_phasing, new_p34_phasing)

old_p34_disc = '''      <!-- Scope Approval Disclaimer -->
      <div style="background:#ffffff; border:1.5px solid #0f172a; border-radius:7px; padding:11px 15px; margin-bottom:11px;">
        <div style="font-size:8.4pt; font-weight:800; color:#0f172a; text-transform:uppercase; margin-bottom:2px;">
          Scope Blueprint Approval &amp; Agreement Annexure Acknowledgment
        </div>
        <p style="font-size:8.0pt; line-height:1.38; color:#334155;">
          Execution below constitutes mutual approval of the functional architecture defined across this 57-unit master specification (Annexure A). Commercial fees, payment milestones, third-party subscriptions, and legal terms shall be governed exclusively by the formal Master Services Agreement.
        </p>
      </div>'''

new_p34_disc = '''      <!-- Scope Approval Disclaimer -->
      <div style="background:#ffffff; border:1.5px solid #0f172a; border-radius:7px; padding:13px 18px; margin-bottom:14px;">
        <div style="font-size:8.8pt; font-weight:800; color:#0f172a; text-transform:uppercase; margin-bottom:3px;">
          Scope Blueprint Approval &amp; Agreement Annexure Acknowledgment
        </div>
        <p style="font-size:8.2pt; line-height:1.42; color:#334155;">
          Execution below constitutes mutual formal approval of the functional scope and architecture defined across this 57-unit master specification document (Scope Annexure A). Commercial fees, payment milestones, third-party subscription disbursements, and contractual terms shall be governed exclusively by the formal Master Services Agreement.
        </p>
      </div>'''
text = text.replace(old_p34_disc, new_p34_disc)

old_p34_sigs = '''      <!-- Separate Dual Entity Sign-Off Blocks -->
      <div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:10px; border-top:1.5px solid #0f172a; padding-top:8px;">
        <div style="font-size:8.1pt; line-height:1.35; color:#334155;">
          <strong>Scope Approved for Dalal Agency:</strong><br><br>
          __________________________________<br>
          <strong>Mr. Vinit Dalal</strong> &bull; Managing Director<br>
          <span style="font-size:7.6pt; color:#64748b;">Dalal Machine Tools Agency Pvt. Ltd.</span>
        </div>
        <div style="font-size:8.1pt; line-height:1.35; color:#334155;">
          <strong>Scope Approved for OMPI India:</strong><br><br>
          __________________________________<br>
          <strong>Authorized Signatory</strong> &bull; Partner<br>
          <span style="font-size:7.6pt; color:#64748b;">OMPI India LLP</span>
        </div>
        <div style="font-size:8.1pt; line-height:1.35; color:#334155; text-align:right;">
          <strong>Submitted by Consultant:</strong><br><br>
          __________________________________<br>
          <strong>Suyash Shinde</strong> &bull; Solutions Architect<br>
          <span style="font-size:7.6pt; color:#64748b;">Pimpri, Pune, Maharashtra</span>
        </div>
      </div>'''

new_p34_sigs = '''      <!-- Separate Dual Entity Sign-Off Blocks -->
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
text = text.replace(old_p34_sigs, new_p34_sigs)

with open('scratch/build_enterprise_specification_v2.py', 'w', encoding='utf-8') as f:
    f.write(text)

print('Updated build_enterprise_specification_v2.py successfully!')

