import re

# 1. Update js/catalog-app.js
js_path = 'new/dalalmachine/js/catalog-app.js'
with open(js_path, 'r', encoding='utf-8') as f:
    js_content = f.read()

old_specs_block = """            <div class="machine-specs-grid">
              <div class="spec-item" title="${m.tonnage > 0 ? m.tonnage + ' Tons' : 'Precision CNC'}">
                <span class="label">Capacity / Tonnage</span>
                <span class="val">${m.tonnage > 0 ? m.tonnage + ' Tons' : 'Precision CNC'}</span>
              </div>
              <div class="spec-item" title="${m.year || 'Standard'}">
                <span class="label">Mfg. Year</span>
                <span class="val">${m.year || 'Standard'}</span>
              </div>
              <div class="spec-item" title="${m.model || '-'}">
                <span class="label">Model Code</span>
                <span class="val">${m.model || '-'}</span>
              </div>
              <div class="spec-item" title="Inspected & Ready for Live Trial">
                <span class="label">Ready Status</span>
                <span class="val" style="color: #16a34a;"><i class="fa fa-check-circle" style="font-size:11px; margin-right:2px;"></i> Inspected</span>
              </div>
            </div>"""

new_specs_block = """            <div class="machine-specs-grid">
              <div class="spec-item" title="${m.tonnage > 0 ? m.tonnage + ' Tons' : 'Precision CNC'}">
                <span class="label"><i class="fa fa-balance-scale"></i> Capacity</span>
                <span class="val">${m.tonnage > 0 ? m.tonnage + ' Tons' : 'Precision CNC'}</span>
              </div>
              <div class="spec-item" title="${m.year || 'Standard'}">
                <span class="label"><i class="fa fa-calendar"></i> Mfg. Year</span>
                <span class="val">${m.year || 'Standard'}</span>
              </div>
              <div class="spec-item" title="${m.model || '-'}">
                <span class="label"><i class="fa fa-hashtag"></i> Model</span>
                <span class="val">${m.model || '-'}</span>
              </div>
              <div class="spec-item" title="Inspected & Ready for Live Demonstration">
                <span class="label"><i class="fa fa-shield"></i> Status</span>
                <span class="val status-val"><i class="fa fa-check-circle"></i> Inspected</span>
              </div>
            </div>"""

if old_specs_block in js_content:
    js_content = js_content.replace(old_specs_block, new_specs_block)
    print("Replaced old_specs_block in catalog-app.js (LF)")
elif old_specs_block.replace('\n', '\r\n') in js_content:
    js_content = js_content.replace(old_specs_block.replace('\n', '\r\n'), new_specs_block.replace('\n', '\r\n'))
    print("Replaced old_specs_block in catalog-app.js (CRLF)")
else:
    print("WARNING: old_specs_block not matched directly in catalog-app.js")

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(js_content)

# 2. Update css/dalal-custom.css
css_path = 'new/dalalmachine/css/dalal-custom.css'
with open(css_path, 'r', encoding='utf-8') as f:
    css_content = f.read()

old_css_rule = """.machine-specs-grid {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(0, 1fr);
  gap: 8px 12px;
  background: #f8fafc;
  border: 1px solid #edf2f7;
  padding: 10px 12px;
  border-radius: 6px;
  margin-bottom: 14px;
  font-size: 12px;
  height: auto !important;
  min-height: 98px !important;
  max-height: none !important;
  overflow: visible !important;
  flex-shrink: 0;
}
.spec-item {
  min-width: 0 !important;
  overflow: visible !important;
}
.spec-item span.label {
  color: #64748b;
  font-size: 10.5px;
  font-weight: 500;
  display: block;
  white-space: normal !important;
  overflow: visible !important;
  text-overflow: clip !important;
  margin-bottom: 2px;
}
.spec-item span.val {
  color: #1e293b;
  font-weight: 600;
  font-size: 12px;
  display: block;
  white-space: normal !important;
  overflow: visible !important;
  text-overflow: clip !important;
  word-break: break-word !important;
}"""

new_css_rule = """.machine-specs-grid {
  display: grid !important;
  grid-template-columns: 1fr 1fr !important;
  background: #f8fafc !important;
  border: 1px solid #e2e8f0 !important;
  border-radius: 8px !important;
  overflow: hidden !important;
  margin-bottom: 16px !important;
  padding: 0 !important;
  height: auto !important;
  min-height: auto !important;
  max-height: none !important;
  flex-shrink: 0 !important;
  box-shadow: inset 0 1px 2px rgba(15, 23, 42, 0.02) !important;
}
.spec-item {
  padding: 10px 14px !important;
  display: flex !important;
  flex-direction: column !important;
  justify-content: center !important;
  min-width: 0 !important;
  border-bottom: 1px solid #edf2f7 !important;
  background: #ffffff !important;
  transition: background 0.2s ease !important;
}
.spec-item:nth-child(odd) {
  border-right: 1px solid #edf2f7 !important;
}
.spec-item:nth-child(3),
.spec-item:nth-child(4) {
  border-bottom: none !important;
}
.spec-item:hover {
  background: #fafcff !important;
}
.spec-item span.label {
  color: #64748b !important;
  font-size: 10px !important;
  font-weight: 700 !important;
  text-transform: uppercase !important;
  letter-spacing: 0.5px !important;
  margin-bottom: 3px !important;
  display: flex !important;
  align-items: center !important;
  gap: 5px !important;
  white-space: nowrap !important;
  overflow: hidden !important;
  text-overflow: ellipsis !important;
  line-height: 1.2 !important;
}
.spec-item span.label i {
  color: #94a3b8 !important;
  font-size: 10px !important;
  width: 12px !important;
  text-align: center !important;
}
.spec-item span.val {
  color: #0f172a !important;
  font-size: 13.5px !important;
  font-weight: 700 !important;
  line-height: 1.25 !important;
  display: block !important;
  white-space: nowrap !important;
  overflow: hidden !important;
  text-overflow: ellipsis !important;
}
.spec-item span.val.status-val {
  color: #16a34a !important;
  font-weight: 700 !important;
  display: inline-flex !important;
  align-items: center !important;
  gap: 4px !important;
}
.spec-item span.val.status-val i {
  color: #16a34a !important;
  font-size: 11px !important;
}"""

if old_css_rule in css_content:
    css_content = css_content.replace(old_css_rule, new_css_rule)
    print("Replaced old_css_rule in dalal-custom.css (LF)")
elif old_css_rule.replace('\n', '\r\n') in css_content:
    css_content = css_content.replace(old_css_rule.replace('\n', '\r\n'), new_css_rule.replace('\n', '\r\n'))
    print("Replaced old_css_rule in dalal-custom.css (CRLF)")
else:
    print("WARNING: old_css_rule not matched directly in dalal-custom.css")

# Also update responsive rule around line 3160
old_resp_rule = """.machine-specs-grid {
    height: auto !important;
    min-height: auto !important;
    max-height: none !important;
    gap: 8px !important;
    margin-bottom: 14px !important;
  }"""

new_resp_rule = """.machine-specs-grid {
    height: auto !important;
    min-height: auto !important;
    max-height: none !important;
    padding: 0 !important;
    margin-bottom: 14px !important;
  }"""

if old_resp_rule in css_content:
    css_content = css_content.replace(old_resp_rule, new_resp_rule)
    print("Replaced old_resp_rule in dalal-custom.css (LF)")
elif old_resp_rule.replace('\n', '\r\n') in css_content:
    css_content = css_content.replace(old_resp_rule.replace('\n', '\r\n'), new_resp_rule.replace('\n', '\r\n'))
    print("Replaced old_resp_rule in dalal-custom.css (CRLF)")

with open(css_path, 'w', encoding='utf-8') as f:
    f.write(css_content)

print("Files updated successfully!")

