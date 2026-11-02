# scratch/calibrate_all_pages.py
with open('scratch/build_balanced_master_spec.py', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Adjust Page 14 so it has comfortable breathing room (not 11pt, but ~50pt)
text = text.replace('padding: 20px 22px; margin-bottom: 12px;', 'padding: 14px 18px; margin-bottom: 8px;')
text = text.replace('padding:11px 14px; margin-bottom:11px;', 'padding:8px 12px; margin-bottom:8px;')
text = text.replace('padding:5px 8px;', 'padding:3.5px 7px;')
text = text.replace('padding:10px 14px; margin-bottom:10px;', 'padding:7px 12px; margin-bottom:7px;')
text = text.replace('padding:10px 14px; margin-bottom:11px;', 'padding:7px 12px; margin-bottom:7px;')
text = text.replace('padding:8px 14px;', 'padding:6px 12px;')

# 2. Enrich Page 1 (Cover) to fill ~700pt
old_p1_end = """      <!-- Key Project Metadata Box -->
      <div style="background:#ffffff; border:1.5px solid #0f172a; border-radius:7px; padding:10px 16px; display:flex; justify-content:space-between; align-items:center;">
        <div>
          <span style="font-size:8.0pt; color:#64748b; font-weight:700; text-transform:uppercase;">Principal Client:</span><br>
          <strong style="font-size:9.8pt; color:#0f172a;">Mr. Vinit Dalal</strong> &bull; Managing Director / Partner
        </div>
        <div>
          <span style="font-size:8.0pt; color:#64748b; font-weight:700; text-transform:uppercase;">Scope Architecture:</span><br>
          <strong style="font-size:9.8pt; color:#0f172a;">57 Proposed Units</strong> &bull; 0 Lines Code Written
        </div>
        <div>
          <span style="font-size:8.0pt; color:#64748b; font-weight:700; text-transform:uppercase;">Prepared by Consultant:</span><br>
          <strong style="font-size:9.8pt; color:#0f172a;">Suyash Shinde</strong> &bull; Pimpri, Pune
        </div>
      </div>"""

new_p1_end = """      <!-- Strategic Document Orientation & Governance Box -->
      <div style="background:#ffffff; border:1.5px solid #cbd5e1; border-radius:7px; padding:11px 16px; margin-bottom:11px;">
        <div style="font-size:8.8pt; font-weight:800; color:#0f172a; text-transform:uppercase; margin-bottom:5px; border-bottom:1.5px solid #f1f5f9; padding-bottom:3px;">
          Master Proposal Structure &bull; How Executive Leadership Should Review This Document
        </div>
        <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px; font-size:8.4pt; line-height:1.4; color:#334155;">
          <div>
            <strong>Pages 02 to 13: Dalal Public Web Ecosystem</strong><br>
            24 customer-facing pages engineered to build trust with plant owners, show live power trials, generate 60-second quotations, and capture high-value machinery inquiries.
          </div>
          <div>
            <strong>Pages 14 to 31: OMPI Operations ERP Suite</strong><br>
            33 operational management modules designed to eliminate inventory errors, manage Italian imports in Euros, handle GST billing, and give the Managing Director real-time control.
          </div>
        </div>
      </div>

      <!-- Key Project Metadata Box -->
      <div style="background:#ffffff; border:1.5px solid #0f172a; border-radius:7px; padding:9px 16px; display:flex; justify-content:space-between; align-items:center;">
        <div>
          <span style="font-size:7.8pt; color:#64748b; font-weight:700; text-transform:uppercase;">Principal Client:</span><br>
          <strong style="font-size:9.6pt; color:#0f172a;">Mr. Vinit Dalal</strong> &bull; Managing Director / Partner
        </div>
        <div>
          <span style="font-size:7.8pt; color:#64748b; font-weight:700; text-transform:uppercase;">Scope Architecture:</span><br>
          <strong style="font-size:9.6pt; color:#0f172a;">57 Proposed Units</strong> &bull; 0 Lines Code Written
        </div>
        <div>
          <span style="font-size:7.8pt; color:#64748b; font-weight:700; text-transform:uppercase;">Prepared by Consultant:</span><br>
          <strong style="font-size:9.6pt; color:#0f172a;">Suyash Shinde</strong> &bull; Pimpri, Pune
        </div>
      </div>"""

if old_p1_end in text:
    text = text.replace(old_p1_end, new_p1_end)
    print("Enriched Page 1 Cover")

# 3. Enrich Page 31
old_p31_end = """        <div class="feature-strip">
          <strong>Key Management Feature:</strong> Total role-based permission control ensuring employees only access tools essential for their daily duties.
        </div>
      </div>"""

new_p31_end = """        <div class="feature-strip" style="margin-bottom:7px;">
          <strong>Key Management Feature:</strong> Total role-based permission control ensuring employees only access tools essential for their daily duties.
        </div>
        <div style="display:flex; justify-content:space-between; align-items:center; background:#f8fafc; border:1px solid #e2e8f0; border-radius:4px; padding:4px 10px; font-size:7.8pt; color:#475569;">
          <div><strong>Enterprise Security Standard:</strong> Encrypted Database Vault &bull; Tamper-Proof Financial Ledger</div>
          <div><strong>Implementation Phase:</strong> Phase 2 Rollout upon Executive Sign-Off</div>
        </div>
      </div>"""

if old_p31_end in text:
    text = text.replace(old_p31_end, new_p31_end)
    print("Enriched Page 31")

# 4. Enrich Page 32 (Milestones & Sign-off)
old_p32_table = """            <tr style="border-bottom:1px solid #e2e8f0; background:#ffffff;">
              <td style="padding:5px 8px; font-weight:700;">Phase 1 (Kickoff Scope)</td>
              <td style="padding:5px 8px;">Dalal 24 Public Pages &bull; Staff Admin Portal &bull; Director Console &bull; Core Quoting Tools</td>
              <td style="padding:5px 8px; font-weight:700; color:#b45309;">TO COMMENCE UPON SIGN-OFF</td>
            </tr>
            <tr style="background:#ffffff;">
              <td style="padding:5px 8px; font-weight:700;">Phase 2 (ERP Rollout)</td>
              <td style="padding:5px 8px;">OMPI Standalone ERP Modules (7 Monthly Sprints: Customer 360, Italy POs, BOM, Godown Bins, GSTR-1)</td>
              <td style="padding:5px 8px; font-weight:700; color:#64748b;">SCHEDULED SPRINT ROADMAP</td>
            </tr>"""

new_p32_table = """            <tr style="border-bottom:1px solid #e2e8f0; background:#ffffff;">
              <td style="padding:5px 8px; font-weight:700;">Phase 1 (Kickoff Scope)</td>
              <td style="padding:5px 8px;">Dalal 24 Public Pages &bull; Staff Admin Portal &bull; WhatsApp Lead Routing &bull; Quoting Tools</td>
              <td style="padding:5px 8px; font-weight:700; color:#b45309;">TO COMMENCE UPON SIGN-OFF</td>
            </tr>
            <tr style="border-bottom:1px solid #e2e8f0; background:#f8fafc;">
              <td style="padding:5px 8px; font-weight:700;">Phase 2 (OMPI Core ERP)</td>
              <td style="padding:5px 8px;">OMPI Customer Master &bull; Italian SKU Catalog &bull; Landed Pricing &bull; Godown Stock Tracker</td>
              <td style="padding:5px 8px; font-weight:700; color:#64748b;">MONTH 1-2 SPRINT</td>
            </tr>
            <tr style="background:#ffffff;">
              <td style="padding:5px 8px; font-weight:700;">Phase 3 (Enterprise Control)</td>
              <td style="padding:5px 8px;">Workshop Overhaul Job Cards &bull; GST Invoicing &bull; Port Demurrage Shield &bull; MD Command Desk</td>
              <td style="padding:5px 8px; font-weight:700; color:#64748b;">MONTH 3-4 SPRINT</td>
            </tr>"""

if old_p32_table in text:
    text = text.replace(old_p32_table, new_p32_table)
    print("Enriched Page 32 Phasing Table")

with open('scratch/build_balanced_master_spec.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("Saved scratch/build_balanced_master_spec.py")

