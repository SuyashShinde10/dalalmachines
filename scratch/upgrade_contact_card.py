# Upgrade contact-form-card in CSS and HTML
css_path = 'new/dalalmachine/css/dalal-custom.css'
with open(css_path, 'r', encoding='utf-8') as f:
    css = f.read()

# 1. Update .contact-form-card CSS rule to include proper padding and input styling
old_css_elevation = """.contact-info-card,
.contact-form-card {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  box-shadow: 0 10px 28px -3px rgba(15, 23, 42, 0.10), 0 3px 8px -1px rgba(15, 23, 42, 0.05) !important;
  transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}"""

new_css_elevation = """.contact-info-card {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  box-shadow: 0 10px 28px -3px rgba(15, 23, 42, 0.10), 0 3px 8px -1px rgba(15, 23, 42, 0.05) !important;
  transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}

.contact-form-card {
  background: #ffffff !important;
  border: 1px solid #e2e8f0 !important;
  border-radius: 10px !important;
  padding: 38px 40px !important;
  box-shadow: 0 10px 28px -3px rgba(15, 23, 42, 0.10), 0 3px 8px -1px rgba(15, 23, 42, 0.05) !important;
  transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}

.contact-form-card .form-control {
  border: 1px solid #cbd5e1 !important;
  border-radius: 6px !important;
  transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
}

.contact-form-card .form-control:focus {
  border-color: #f89d13 !important;
  box-shadow: 0 0 0 3px rgba(248, 157, 19, 0.15) !important;
  outline: none !important;
}"""

if old_css_elevation in css:
    css = css.replace(old_css_elevation, new_css_elevation)
    print("Updated CSS elevation rules (LF)")
elif old_css_elevation.replace('\n', '\r\n') in css:
    css = css.replace(old_css_elevation.replace('\n', '\r\n'), new_css_elevation.replace('\n', '\r\n'))
    print("Updated CSS elevation rules (CRLF)")
else:
    print("WARNING: old_css_elevation not found in dalal-custom.css")

with open(css_path, 'w', encoding='utf-8') as f:
    f.write(css)


# 2. Update contact.html
contact_path = 'new/dalalmachine/contact.html'
with open(contact_path, 'r', encoding='utf-8') as f:
    html = f.read()

old_html_card = """                <!-- Form Column -->
                <div class="col-lg-7 col-md-12">
                    <div class="contact-form-card" data-animated-content="true" data-direction="vertical" data-distance="40" data-duration="0.7">
                        <div style="margin-bottom:10px;">
                            <span style="color:#f89d13; font-family:'Rajdhani'; font-size:14px; font-weight:700; text-transform:uppercase; letter-spacing:1px;">Send an Inquiry</span>
                        </div>
                        <h3 style="font-family:'Barlow'; font-size:26px; font-weight:800; color:#1b212f; margin:0 0 20px;">Direct Quotation & Machinery Requirement</h3>

                        <form id="contact-inquiry-form" onsubmit="event.preventDefault(); submitInquiry();">
                            <!-- Anti-bot honeypot -->
                            <input type="text" id="form-hp" name="_hp_company" style="display:none;" tabindex="-1" autocomplete="off">

                            <div class="row">
                                <div class="col-md-6 form-group">
                                    <label for="form-name" style="font-size:13px; font-weight:600; color:#334155;">Your Full Name *</label>
                                    <input type="text" id="form-name" class="form-control" required style="height:46px; font-size:14px;" placeholder="e.g. Rajiv Sharma">
                                </div>
                                <div class="col-md-6 form-group">
                                    <label for="form-company" style="font-size:13px; font-weight:600; color:#334155;">Company Name *</label>
                                    <input type="text" id="form-company" class="form-control" required style="height:46px; font-size:14px;" placeholder="e.g. Acme Forgings Pvt Ltd">
                                </div>
                                <div class="col-md-6 form-group">
                                    <label for="form-phone" style="font-size:13px; font-weight:600; color:#334155;">Phone / Mobile Number *</label>
                                    <input type="tel" id="form-phone" class="form-control" required style="height:46px; font-size:14px;" placeholder="+91 98200 00000">
                                    <div id="phone-validation-msg" class="form-validation-error">Please enter a valid phone number with STD or country code.</div>
                                </div>
                                <div class="col-md-6 form-group">
                                    <label for="form-email" style="font-size:13px; font-weight:600; color:#334155;">Email Address *</label>
                                    <input type="email" id="form-email" class="form-control" required style="height:46px; font-size:14px;" placeholder="rajiv@acmeforge.com">
                                </div>
                                <div class="col-12 form-group">
                                    <label for="form-machine-type" style="font-size:13px; font-weight:600; color:#334155;">Interested Machine Type or Tonnage Required</label>
                                    <select id="form-machine-type" class="form-control" style="height:46px; font-size:14px;">
                                        <option value="Hot Forging Press (1000T - 6300T)">Hot Forging Press (1000T - 6300T)</option>
                                        <option value="C-Frame Stamping Press (80T - 250T)">C-Frame Stamping Press (80T - 250T)</option>
                                        <option value="Knuckle Joint Coining Press">Knuckle Joint Coining Press</option>
                                        <option value="CNC Horizontal Boring Machine">CNC Horizontal Boring Machine</option>
                                        <option value="OMPI Clutch-Brake Retrofitting">OMPI Clutch-Brake Retrofitting</option>
                                        <option value="Brand New Forging Line (DMT / ECAI)">Brand New Forging Line (DMT / ECAI)</option>
                                        <option value="Other Heavy Machinery">Other Heavy Machinery</option>
                                    </select>
                                </div>
                                <div class="col-12 form-group">
                                    <label for="form-message" style="font-size:13px; font-weight:600; color:#334155;">Detailed Technical Requirements / Message</label>
                                    <textarea id="form-message" class="form-control" rows="4" placeholder="Mention required bed size, stroke, daylight, preferred make, delivery timeline..." style="font-size:14px;"></textarea>
                                </div>
                                <div class="col-12">
                                    <button type="submit" class="theme-btn btn-style-one" style="padding:14px 32px; background:#f89d13; color:#111; font-weight:700; border:none; width:100%;">
                                        <i class="fa fa-paper-plane"></i> Submit Quotation &amp; Notify on WhatsApp
                                    </button>
                                    <p style="font-size:12px; color:#64748b; margin-top:10px; text-align:center;">
                                        <i class="fa fa-lock" style="color:#10b981;"></i> Your inquiry is securely saved to our database and instantly notified to MD Mr. Vinit Dalal.
                                    </p>
                                </div>
                            </div>
                        </form>
                    </div>
                </div>"""

new_html_card = """                <!-- Form Column -->
                <div class="col-lg-7 col-md-12">
                    <div class="contact-form-card" data-animated-content="true" data-direction="vertical" data-distance="40" data-duration="0.7">
                        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px; margin-bottom:8px;">
                            <span style="color:#f89d13; font-family:'Rajdhani',sans-serif; font-size:13px; font-weight:700; text-transform:uppercase; letter-spacing:1.5px;">Send an Inquiry</span>
                            <span style="font-size:12px; color:#16a34a; font-weight:700; background:#f0fdf4; border:1px solid #bbf7d0; padding:4px 12px; border-radius:20px; display:inline-flex; align-items:center; gap:6px;">
                                <i class="fa fa-shield"></i> Direct to Managing Director
                            </span>
                        </div>
                        <h3 style="font-family:'Barlow',sans-serif; font-size:26px; font-weight:800; color:#1b212f; margin:0 0 8px;">Direct Quotation &amp; Machinery Requirement</h3>
                        <p style="font-size:13.5px; color:#64748b; margin:0 0 22px; line-height:1.5;">Fill out your machinery requirements below for ready stock inspection or CIF import terms.</p>

                        <form id="contact-inquiry-form" onsubmit="event.preventDefault(); submitInquiry();">
                            <!-- Anti-bot honeypot -->
                            <input type="text" id="form-hp" name="_hp_company" style="display:none;" tabindex="-1" autocomplete="off">

                            <div class="row">
                                <div class="col-md-6 form-group" style="margin-bottom:18px;">
                                    <label for="form-name" style="font-size:13px; font-weight:700; color:#1e293b; display:block; margin-bottom:6px;">Your Full Name <span style="color:#ef4444;">*</span></label>
                                    <input type="text" id="form-name" class="form-control" required style="height:48px; font-size:14px; border:1px solid #cbd5e1; border-radius:6px; padding:10px 14px;" placeholder="e.g. Rajiv Sharma">
                                </div>
                                <div class="col-md-6 form-group" style="margin-bottom:18px;">
                                    <label for="form-company" style="font-size:13px; font-weight:700; color:#1e293b; display:block; margin-bottom:6px;">Company / Factory Name <span style="color:#ef4444;">*</span></label>
                                    <input type="text" id="form-company" class="form-control" required style="height:48px; font-size:14px; border:1px solid #cbd5e1; border-radius:6px; padding:10px 14px;" placeholder="e.g. Acme Forgings Pvt Ltd">
                                </div>
                                <div class="col-md-6 form-group" style="margin-bottom:18px;">
                                    <label for="form-phone" style="font-size:13px; font-weight:700; color:#1e293b; display:block; margin-bottom:6px;">Phone / WhatsApp Number <span style="color:#ef4444;">*</span></label>
                                    <input type="tel" id="form-phone" class="form-control" required style="height:48px; font-size:14px; border:1px solid #cbd5e1; border-radius:6px; padding:10px 14px;" placeholder="+91 98200 00000">
                                    <div id="phone-validation-msg" class="form-validation-error">Please enter a valid phone number with STD or country code.</div>
                                </div>
                                <div class="col-md-6 form-group" style="margin-bottom:18px;">
                                    <label for="form-email" style="font-size:13px; font-weight:700; color:#1e293b; display:block; margin-bottom:6px;">Email Address <span style="color:#ef4444;">*</span></label>
                                    <input type="email" id="form-email" class="form-control" required style="height:48px; font-size:14px; border:1px solid #cbd5e1; border-radius:6px; padding:10px 14px;" placeholder="rajiv@acmeforge.com">
                                </div>
                                <div class="col-12 form-group" style="margin-bottom:18px;">
                                    <label for="form-machine-type" style="font-size:13px; font-weight:700; color:#1e293b; display:block; margin-bottom:6px;">Interested Machine Type or Tonnage Required</label>
                                    <select id="form-machine-type" class="form-control" style="height:48px; font-size:14px; border:1px solid #cbd5e1; border-radius:6px; padding:10px 14px; cursor:pointer;">
                                        <option value="Hot Forging Press (1000T - 6300T)">Hot Forging Press (1000T - 6300T)</option>
                                        <option value="C-Frame Stamping Press (80T - 250T)">C-Frame Stamping Press (80T - 250T)</option>
                                        <option value="Knuckle Joint Coining Press">Knuckle Joint Coining Press</option>
                                        <option value="CNC Horizontal Boring Machine">CNC Horizontal Boring Machine</option>
                                        <option value="OMPI Clutch-Brake Retrofitting">OMPI Clutch-Brake Retrofitting</option>
                                        <option value="Brand New Forging Line (DMT / ECAI)">Brand New Forging Line (DMT / ECAI)</option>
                                        <option value="Other Heavy Machinery">Other Heavy Machinery</option>
                                    </select>
                                </div>
                                <div class="col-12 form-group" style="margin-bottom:22px;">
                                    <label for="form-message" style="font-size:13px; font-weight:700; color:#1e293b; display:block; margin-bottom:6px;">Detailed Technical Requirements / Message</label>
                                    <textarea id="form-message" class="form-control" rows="4" placeholder="Mention required bed size, stroke, daylight, preferred make, delivery timeline..." style="font-size:14px; border:1px solid #cbd5e1; border-radius:6px; padding:12px 14px; line-height:1.6;"></textarea>
                                </div>
                                <div class="col-12">
                                    <button type="submit" class="theme-btn btn-style-one" style="padding:15px 32px; background:#f89d13; color:#111; font-weight:800; font-size:15px; border:none; width:100%; border-radius:6px; cursor:pointer; box-shadow:0 4px 14px rgba(248,157,19,0.3); display:flex; align-items:center; justify-content:center; gap:10px; transition:all 0.2s ease;">
                                        <i class="fa fa-paper-plane" style="font-size:16px;"></i> Submit Quotation &amp; Notify on WhatsApp
                                    </button>
                                    <p style="font-size:12.5px; color:#64748b; margin-top:12px; margin-bottom:0; text-align:center; display:flex; align-items:center; justify-content:center; gap:6px;">
                                        <i class="fa fa-lock" style="color:#10b981;"></i> Your inquiry is securely saved to our database and instantly notified to MD Mr. Vinit Dalal.
                                    </p>
                                </div>
                            </div>
                        </form>
                    </div>
                </div>"""

if old_html_card in html:
    html = html.replace(old_html_card, new_html_card)
    print("Updated contact.html (LF)")
elif old_html_card.replace('\n', '\r\n') in html:
    html = html.replace(old_html_card.replace('\n', '\r\n'), new_html_card.replace('\n', '\r\n'))
    print("Updated contact.html (CRLF)")
else:
    print("WARNING: old_html_card not found in contact.html")

with open(contact_path, 'w', encoding='utf-8') as f:
    f.write(html)

print("Card upgrade complete!")

