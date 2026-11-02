import re

# 1. Update new/dalalmachine/js/catalog-app.js
js_path = 'new/dalalmachine/js/catalog-app.js'
with open(js_path, 'r', encoding='utf-8') as f:
    js_content = f.read()

# Pattern matching the card template in catalog-app.js
old_thumb_and_header = """            <span class="machine-location-pill">${locIcon} ${m.location}</span>
            <span class="machine-stock-badge">ID: ${m.id}</span>
          </div>
          <div class="machine-info-content">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;">
              <div class="machine-cat-label" style="margin-bottom:0;">${m.categoryName} &bull; ${m.make}</div>
              <label style="font-size:11.5px; font-weight:600; color:#64748b; cursor:pointer; margin:0; display:inline-flex; align-items:center; gap:4px;">
                <input type="checkbox" onchange="toggleCompareMachine('${m.id}')" ${isCompared ? 'checked' : ''} style="cursor:pointer; accent-color:#f89d13;"> Compare
              </label>
            </div>
            <h4 class="machine-title" title="${m.name}">${m.name}</h4>"""

new_thumb_and_header = """            <span class="machine-location-pill">${locIcon} ${m.location}</span>
            <span class="machine-stock-badge">ID: ${m.id}</span>
            <label class="machine-thumb-compare" title="Add to Machine Comparison">
              <input type="checkbox" onchange="toggleCompareMachine('${m.id}')" ${isCompared ? 'checked' : ''}>
              <span>Compare</span>
            </label>
          </div>
          <div class="machine-info-content">
            <div class="machine-cat-label">${m.categoryName} &bull; ${m.make}</div>
            <h4 class="machine-title" title="${m.name}">${m.name}</h4>"""

if old_thumb_and_header in js_content:
    js_content = js_content.replace(old_thumb_and_header, new_thumb_and_header)
    print("Replaced thumb and header in catalog-app.js (LF)")
elif old_thumb_and_header.replace('\n', '\r\n') in js_content:
    js_content = js_content.replace(old_thumb_and_header.replace('\n', '\r\n'), new_thumb_and_header.replace('\n', '\r\n'))
    print("Replaced thumb and header in catalog-app.js (CRLF)")
else:
    print("WARNING: old_thumb_and_header not found in catalog-app.js")

# Also update model-val class on model spec-item
old_model_item = """              <div class="spec-item" title="${m.model || '-'}">
                <span class="label"><i class="fa fa-hashtag"></i> Model</span>
                <span class="val">${m.model || '-'}</span>
              </div>"""

new_model_item = """              <div class="spec-item" title="${m.model || '-'}">
                <span class="label"><i class="fa fa-hashtag"></i> Model</span>
                <span class="val model-val">${m.model || '-'}</span>
              </div>"""

if old_model_item in js_content:
    js_content = js_content.replace(old_model_item, new_model_item)
    print("Replaced model item in catalog-app.js (LF)")
elif old_model_item.replace('\n', '\r\n') in js_content:
    js_content = js_content.replace(old_model_item.replace('\n', '\r\n'), new_model_item.replace('\n', '\r\n'))
    print("Replaced model item in catalog-app.js (CRLF)")
else:
    print("WARNING: old_model_item not found in catalog-app.js")

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(js_content)


# 2. Update new/dalalmachine/css/dalal-custom.css
css_path = 'new/dalalmachine/css/dalal-custom.css'
with open(css_path, 'r', encoding='utf-8') as f:
    css_content = f.read()

old_css_block = """.machine-specs-grid {
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

new_css_block = """.machine-specs-grid {
  display: grid !important;
  grid-template-columns: 1.15fr 0.85fr !important;
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
  padding: 9px 12px !important;
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
  font-size: 13px !important;
  font-weight: 700 !important;
  line-height: 1.25 !important;
  display: block !important;
  white-space: normal !important;
  word-break: break-word !important;
  overflow: visible !important;
  text-overflow: clip !important;
}
.spec-item span.val.model-val {
  font-size: 12.5px !important;
  letter-spacing: -0.2px !important;
}
.spec-item span.val.status-val {
  color: #16a34a !important;
  font-weight: 700 !important;
  display: inline-flex !important;
  align-items: center !important;
  gap: 4px !important;
  white-space: nowrap !important;
}
.spec-item span.val.status-val i {
  color: #16a34a !important;
  font-size: 11px !important;
}

/* Glassmorphic Compare Pill on thumbnail */
.machine-thumb-compare {
  position: absolute !important;
  bottom: 10px !important;
  right: 10px !important;
  background: rgba(15, 23, 42, 0.85) !important;
  backdrop-filter: blur(6px) !important;
  -webkit-backdrop-filter: blur(6px) !important;
  border: 1px solid rgba(255, 255, 255, 0.22) !important;
  color: #ffffff !important;
  font-size: 11px !important;
  font-weight: 600 !important;
  padding: 4px 9px !important;
  border-radius: 4px !important;
  cursor: pointer !important;
  display: inline-flex !important;
  align-items: center !important;
  gap: 5px !important;
  margin: 0 !important;
  z-index: 3 !important;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.25) !important;
  transition: all 0.2s ease !important;
}
.machine-thumb-compare:hover {
  background: rgba(15, 23, 42, 0.96) !important;
  border-color: #f89d13 !important;
  color: #f89d13 !important;
}
.machine-thumb-compare input[type="checkbox"] {
  accent-color: #f89d13 !important;
  cursor: pointer !important;
  margin: 0 !important;
  width: 13px !important;
  height: 13px !important;
}"""

if old_css_block in css_content:
    css_content = css_content.replace(old_css_block, new_css_block)
    print("Replaced CSS block in dalal-custom.css (LF)")
elif old_css_block.replace('\n', '\r\n') in css_content:
    css_content = css_content.replace(old_css_block.replace('\n', '\r\n'), new_css_block.replace('\n', '\r\n'))
    print("Replaced CSS block in dalal-custom.css (CRLF)")
else:
    print("WARNING: old_css_block not found in dalal-custom.css")

with open(css_path, 'w', encoding='utf-8') as f:
    f.write(css_content)

print("Updated both files successfully!")

