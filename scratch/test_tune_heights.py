with open('scratch/build_enterprise_specification_v2.py', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update card CSS to give rich, generous padding and typography
text = text.replace('font-size: 9.8pt;\n      line-height: 1.45;', 'font-size: 10.0pt;\n      line-height: 1.50;')
text = text.replace('margin-bottom: 9px;\n      padding: 11px 15px;', 'margin-bottom: 16px;\n      padding: 17px 20px;')
text = text.replace('font-size: 11.0pt;', 'font-size: 12.0pt;')
text = text.replace('font-size: 9.3pt;\n      line-height: 1.42;', 'font-size: 9.6pt;\n      line-height: 1.48;')
text = text.replace('padding: 4px 8px;\n      margin-bottom: 6px;', 'padding: 8px 12px;\n      margin-bottom: 9px;')
text = text.replace('padding: 5px 10px;\n      font-size: 8.5pt;\n      line-height: 1.38;', 'padding: 8px 14px;\n      font-size: 8.8pt;\n      line-height: 1.44;')
text = text.replace('padding: 4px 10px;\n      border-radius: 4px;\n      border-left: 3.5px solid #0284c7;', 'padding: 6px 12px;\n      border-radius: 4px;\n      border-left: 3.5px solid #0284c7;')

# 2. Add phase/verification tag inside render_card (specific to Dalal vs OMPI)
old_card_end = """          <div class="feature-strip">
            <strong>Key Management Feature:</strong> {item['feature']}
          </div>
        </div>"""

new_card_end = """          <div class="feature-strip">
            <strong>Key Management Feature:</strong> {item['feature']}
          </div>
          <div style="display:flex; justify-content:space-between; align-items:center; background:#f8fafc; border:1px solid #e2e8f0; border-radius:4px; padding:4px 12px; margin-top:8px; font-size:7.8pt; color:#475569;">
            <div><strong>Planned Milestone:</strong> {('Phase 1 (Dalal Machinery Launch)' if is_route else 'Phase 2 &bull; 3 (OMPI Operations Rollout)')}</div>
            <div><strong>Verification Criteria:</strong> Functional UAT &amp; Data Review prior to commercial release</div>
          </div>
        </div>"""

text = text.replace(old_card_end, new_card_end)

# 3. For Page 2 (Executive Summary): increase padding and spacings
text = text.replace('padding:11px 15px; margin-bottom:10px;', 'padding:15px 18px; margin-bottom:14px;')
text = text.replace('padding:4.5px 8px;', 'padding:6px 10px;')
text = text.replace('padding:5px 8px;', 'padding:7px 10px;')
text = text.replace('padding:10px 13px;', 'padding:14px 16px;')

# 4. For Page 3 (Assumptions & Exclusions): increase padding and spacings
text = text.replace('padding:10px 14px; margin-bottom:9px;', 'padding:15px 18px; margin-bottom:13px;')
text = text.replace('padding:6px 9px;', 'padding:8px 12px;')

with open('scratch/build_enterprise_specification_v2.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("Tuned styles for build_enterprise_specification_v2.py")

