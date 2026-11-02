# scratch/perfect_all_32_pages.py
import re

with open('scratch/build_balanced_master_spec.py', 'r', encoding='utf-8') as f:
    code = f.read()

# Add governance bar right after feature-strip in render_card
old_card_end = """          <div class="feature-strip">
            <strong>Key Management Feature:</strong> {item['feature']}
          </div>
        </div>"""

new_card_end = """          <div class="feature-strip">
            <strong>Key Management Feature:</strong> {item['feature']}
          </div>
          <div style="display:flex; justify-content:space-between; align-items:center; background:#f8fafc; border:1px solid #e2e8f0; border-radius:4px; padding:3.5px 10px; margin-top:6px; font-size:7.8pt; color:#475569;">
            <div><strong>Quality Assurance Gate:</strong> Functional Quality Test Prior to Shop Floor Deployment</div>
            <div><strong>Pre-Commencement Status:</strong> Proposed Scope &bull; Pending Formal Sign-Off</div>
          </div>
        </div>"""

if old_card_end in code:
    code = code.replace(old_card_end, new_card_end)
    print("Added governance bar to render_card")
else:
    print("Could not find exact old_card_end string")

# Now let's enrich Page 14 (Architecture map) to fill more vertical space
old_p14_note = """      <!-- Confidentiality Warning Banner -->
      <div style="border:1.5px solid #dc2626; background:#fef2f2; border-radius:7px; padding:9px 14px;">
        <p style="font-size:8.4pt; line-height:1.4; color:#991b1b;">
          <strong>&#128274; STRICT CONFIDENTIALITY NOTICE:</strong> This architectural blueprint contains proprietary commercial operating systems and confidential pricing logic. External distribution is strictly forbidden.
        </p>
      </div>"""

new_p14_note = """      <!-- Key Operational Highlights Box -->
      <div style="background:#ffffff; border:1.5px solid #cbd5e1; border-radius:7px; padding:10px 14px; margin-bottom:10px;">
        <div style="font-size:8.8pt; font-weight:800; color:#0f172a; text-transform:uppercase; margin-bottom:4px;">
          Core Business Advantages to be Delivered Upon Implementation
        </div>
        <div style="display:grid; grid-template-columns:1fr 1fr; gap:8px; font-size:8.3pt; line-height:1.38; color:#334155;">
          <div style="background:#f8fafc; padding:6px 9px; border-radius:4px; border-left:3px solid #0284c7;">
            <strong>Real-Time Godown Reservation Lock:</strong> Stops accidental double-selling of high-demand presses and clutch models across simultaneous sales calls.
          </div>
          <div style="background:#f8fafc; padding:6px 9px; border-radius:4px; border-left:3px solid #0284c7;">
            <strong>Landed Import Margin Protection:</strong> Calculates exact landed cost in Indian Rupees including Euro conversion, sea freight, customs duty, and port handling.
          </div>
          <div style="background:#f8fafc; padding:6px 9px; border-radius:4px; border-left:3px solid #0284c7;">
            <strong>100% Clean GST Tax Invoices:</strong> Automatically validates client 15-digit GSTIN, ensuring zero input tax credit disputes or delayed client payments.
          </div>
          <div style="background:#f8fafc; padding:6px 9px; border-radius:4px; border-left:3px solid #0284c7;">
            <strong>Executive 360-Degree Control:</strong> Provides Mr. Vinit Dalal with real-time operational visibility over sales leads, godown inventory, and cash collections.
          </div>
        </div>
      </div>

      <!-- Confidentiality Warning Banner -->
      <div style="border:1.5px solid #dc2626; background:#fef2f2; border-radius:7px; padding:8px 14px;">
        <p style="font-size:8.3pt; line-height:1.38; color:#991b1b;">
          <strong>&#128274; STRICT CONFIDENTIALITY NOTICE:</strong> This architectural blueprint contains proprietary commercial operating systems and confidential pricing logic. External distribution is strictly forbidden.
        </p>
      </div>"""

if old_p14_note in code:
    code = code.replace(old_p14_note, new_p14_note)
    print("Enriched Page 14 architecture map")

# Save updated script
with open('scratch/build_balanced_master_spec.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("Saved scratch/build_balanced_master_spec.py")

