# Update contact.html
contact_path = 'new/dalalmachine/contact.html'
with open(contact_path, 'r', encoding='utf-8') as f:
    c = f.read()

target = """                        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px; margin-bottom:10px;">
                            <span style="color:#f89d13; font-family:'Rajdhani'; font-size:14px; font-weight:700; text-transform:uppercase; letter-spacing:1px;">Send an Inquiry</span>
                            <div style="display:inline-flex; align-items:center; gap:6px; background:#ecfdf5; border:1px solid #a7f3d0; color:#065f46; font-size:12px; font-weight:600; padding:4px 12px; border-radius:16px;">
                                <i class="fa fa-clock-o" style="color:#10b981;"></i> Avg. RFQ Response: &lt; 2 Hours
                            </div>
                        </div>"""

replacement = """                        <div style="margin-bottom:10px;">
                            <span style="color:#f89d13; font-family:'Rajdhani'; font-size:14px; font-weight:700; text-transform:uppercase; letter-spacing:1px;">Send an Inquiry</span>
                        </div>"""

if target in c:
    c = c.replace(target, replacement)
    print("Replaced in contact.html (LF)")
elif target.replace('\n', '\r\n') in c:
    c = c.replace(target.replace('\n', '\r\n'), replacement.replace('\n', '\r\n'))
    print("Replaced in contact.html (CRLF)")
else:
    print("WARNING: target not found in contact.html")

with open(contact_path, 'w', encoding='utf-8') as f:
    f.write(c)

# Update product.html
product_path = 'new/dalalmachine/product.html'
with open(product_path, 'r', encoding='utf-8') as f:
    p = f.read()

p_target = "Direct inquiry saved to our official system. Mr. Vinit Dalal will review and respond with comprehensive commercial terms within 2 hours."
p_repl = "Direct inquiry saved to our official system. Mr. Vinit Dalal will review and respond with comprehensive commercial terms and technical documentation."

if p_target in p:
    p = p.replace(p_target, p_repl)
    print("Replaced in product.html")
else:
    print("WARNING: p_target not found in product.html")

with open(product_path, 'w', encoding='utf-8') as f:
    f.write(p)

