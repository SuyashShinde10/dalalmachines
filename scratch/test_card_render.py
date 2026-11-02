import subprocess, os, pymupdf

def test_card_height():
    test_html = """<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;700&display=swap" rel="stylesheet">
  <style>
    @page {
      size: A4 portrait;
      margin: 10mm 12mm 10mm 12mm;
    }
    *, *::before, *::after {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }
    body {
      font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
      color: #0f172a;
      background: #ffffff;
      font-size: 10.0pt;
      line-height: 1.48;
      -webkit-print-color-adjust: exact;
      print-color-adjust: exact;
    }
    .page {
      height: 277mm;
      max-height: 277mm;
      overflow: hidden;
      box-sizing: border-box;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      page-break-after: always;
      break-after: page;
    }
    .page-content {
      flex: 1;
      display: flex;
      flex-direction: column;
    }
    .header-bar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 2.5px solid #0f172a;
      border-top: 4px solid #d97706;
      padding: 5px 0;
      margin-bottom: 7px;
    }
    .brand-title {
      font-size: 12.0pt;
      font-weight: 800;
      color: #0f172a;
    }
    .brand-subtitle {
      font-size: 8.5pt;
      font-weight: 700;
      color: #b45309;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }
    .doc-meta {
      text-align: right;
      font-size: 7.8pt;
      color: #475569;
      line-height: 1.35;
    }
    .confidential-bar {
      background: #fef2f2;
      border: 1.5px solid #dc2626;
      border-radius: 5px;
      padding: 5px 10px;
      margin-bottom: 8px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 7.8pt;
      font-weight: 700;
      color: #991b1b;
    }
    .confidential-tag {
      background: #b91c1c;
      color: #ffffff;
      padding: 2.5px 8px;
      border-radius: 3px;
      text-transform: uppercase;
      font-size: 7.2pt;
      font-weight: 800;
    }
    .section-header {
      background: #0f172a;
      color: #ffffff;
      padding: 6px 12px;
      border-radius: 5px;
      margin-bottom: 10px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .section-title {
      font-size: 9.2pt;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.3px;
    }
    .section-tag {
      font-size: 7.8pt;
      font-weight: 700;
      background: #f59e0b;
      color: #0f172a;
      padding: 2px 8px;
      border-radius: 3px;
    }
    .card-box {
      border: 1.5px solid #cbd5e1;
      border-radius: 8px;
      background: #ffffff;
      margin-bottom: 11px;
      padding: 13px 16px;
      box-shadow: 0 1px 3px rgba(0,0,0,0.03);
    }
    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 1.5px solid #e2e8f0;
      padding-bottom: 6px;
      margin-bottom: 8px;
    }
    .badge-id {
      background: #0f172a;
      color: #ffffff;
      padding: 3px 8px;
      border-radius: 4px;
      font-size: 8.5pt;
      font-weight: 800;
      font-family: 'JetBrains Mono', monospace;
      margin-right: 8px;
    }
    .card-title {
      font-size: 11.5pt;
      font-weight: 800;
      color: #0f172a;
    }
    .card-status {
      font-size: 7.6pt;
      font-weight: 700;
      padding: 2.5px 8px;
      border-radius: 3px;
      margin-left: 8px;
      background: #fffbeb;
      color: #b45309;
      border: 1px solid #fef3c7;
    }
    .meta-row {
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 8.2pt;
      color: #475569;
      margin-bottom: 8px;
      background: #f8fafc;
      padding: 4px 10px;
      border-radius: 4px;
      border-left: 3.5px solid #0284c7;
    }
    .meta-row strong {
      color: #0f172a;
    }
    .simple-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 12px;
      margin-bottom: 9px;
    }
    .grid-label {
      font-size: 8.2pt;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.3px;
      color: #475569;
      margin-bottom: 3px;
      border-bottom: 1px solid #f1f5f9;
      padding-bottom: 2px;
    }
    .grid-text {
      font-size: 9.4pt;
      line-height: 1.45;
      color: #334155;
    }
    .deliverables-box {
      background: #f8fafc;
      border: 1px solid #e2e8f0;
      border-radius: 5px;
      padding: 6px 10px;
      margin-bottom: 8px;
    }
    .deliverables-title {
      font-size: 7.8pt;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.4px;
      color: #64748b;
      margin-bottom: 4px;
    }
    .deliverables-grid {
      display: grid;
      grid-template-columns: 1fr 1fr 1fr;
      gap: 8px;
    }
    .deliverable-item {
      font-size: 8.2pt;
      color: #1e293b;
      font-weight: 600;
      display: flex;
      align-items: center;
      gap: 5px;
    }
    .deliverable-item svg {
      width: 13px;
      height: 13px;
      color: #16a34a;
      flex-shrink: 0;
    }
    .feature-strip {
      background: #eff6ff;
      border: 1px solid #bfdbfe;
      border-radius: 5px;
      padding: 6px 10px;
      font-size: 8.8pt;
      line-height: 1.4;
      color: #1e40af;
    }
    .feature-strip strong {
      color: #1e3a8a;
    }
    .footer-bar {
      border-top: 1.5px solid #cbd5e1;
      padding-top: 5px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 7.6pt;
      color: #64748b;
      margin-top: auto;
    }
    .confidential-watermark {
      font-weight: 800;
      color: #dc2626;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }
  </style>
</head>
<body>
  <div class="page">
    <div class="page-content">
      <div class="header-bar">
        <div>
          <div class="brand-title">DALAL MACHINE TOOLS AGENCY &amp; OMPI INDIA</div>
          <div class="brand-subtitle">SYSTEM 1: DALAL MACHINERY PUBLIC PLATFORM &bull; PROPOSED SCOPE</div>
        </div>
        <div class="doc-meta">
          <strong>Doc Ref:</strong> SCOPE-PLAN-2026-DALAL-OMPI-57<br>
          <strong>Status:</strong> Pre-Commencement Scope Blueprint<br>
          <strong>Language:</strong> Plain Business English (Non-Technical)
        </div>
      </div>
      <div class="confidential-bar">
        <div>&#9888; STRICTLY CONFIDENTIAL &bull; PRE-COMMENCEMENT MASTER PLAN &bull; WORK NOT COMMENCED &bull; DO NOT SHARE</div>
        <div class="confidential-tag">STRICTLY PRIVATE</div>
      </div>
      
      <div class="section-header">
        <span class="section-title">Dalal Web Presence Scope &bull; Pages 01 &amp; 02 of 24 (To Be Engineered)</span>
        <span class="section-tag">Public Client Gateway</span>
      </div>

      <!-- Card 1 -->
      <div class="card-box">
        <div class="card-header">
          <div>
            <span class="badge-id">ROUTE-01</span>
            <span class="card-title">Homepage &amp; Machinery Showroom</span>
            <span class="card-status">&#9675; TO BE BUILT: SYSTEM 1</span>
          </div>
          <div style="font-family:'JetBrains Mono',monospace; font-size:8.0pt; color:#b45309; background:#fffbeb; padding:2px 8px; border:1px solid #fef3c7; border-radius:3px;">
            Planned Route: /index.html
          </div>
        </div>
        <div class="meta-row">
          <div><strong>Primary Business Audience:</strong> Industrial Plant Owners, Factory Directors, Forging Sourcing Heads</div>
          <div><strong>Core Focus:</strong> High-Value Machine Sizing &amp; Trust</div>
        </div>
        <div class="simple-grid">
          <div>
            <div class="grid-label">What This Web Page Will Do Once Built</div>
            <div class="grid-text">
              A modern digital machinery showroom presenting heavy presses available for sale. Customers will see clear high-resolution photographs, verified machine tonnages, live video power trials, and a direct WhatsApp button to speak directly with Mr. Vinit Dalal. Eliminates buyer hesitation before calling.
            </div>
          </div>
          <div>
            <div class="grid-label">Business Value &amp; Commercial Risk It Prevents</div>
            <div class="grid-text">
              Eliminates buyer skepticism. Factory owners see that machines are physically present in the Pune stockyard (not fake broker listings), establishing instant trust for deals from Rs. 50 Lakh to Rs. 4 Crore. Protects corporate brand credibility against unauthorized market brokers.
            </div>
          </div>
        </div>
        <div class="deliverables-box">
          <div class="deliverables-title">Key Tangible System Capabilities (To Be Built)</div>
          <div class="deliverables-grid">
            <div class="deliverable-item">
              <svg fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/></svg>
              <span>Live Power Inspection Videos</span>
            </div>
            <div class="deliverable-item">
              <svg fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/></svg>
              <span>Direct WhatsApp Sizing RFQ</span>
            </div>
            <div class="deliverable-item">
              <svg fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/></svg>
              <span>Pune Yard Physical Verification</span>
            </div>
          </div>
        </div>
        <div class="feature-strip">
          <strong>Key Management Feature:</strong> 1-Click WhatsApp inquiry button pre-filled with the exact machine model and capacity.
        </div>
      </div>

      <!-- Card 2 -->
      <div class="card-box">
        <div class="card-header">
          <div>
            <span class="badge-id">ROUTE-02</span>
            <span class="card-title">Company Heritage &amp; Facility Dossier</span>
            <span class="card-status">&#9675; TO BE BUILT: SYSTEM 1</span>
          </div>
          <div style="font-family:'JetBrains Mono',monospace; font-size:8.0pt; color:#b45309; background:#fffbeb; padding:2px 8px; border:1px solid #fef3c7; border-radius:3px;">
            Planned Route: /about.html
          </div>
        </div>
        <div class="meta-row">
          <div><strong>Primary Business Audience:</strong> Corporate Procurement Heads, Bank Valuers, Joint-Venture Partners</div>
          <div><strong>Core Focus:</strong> 50-Year Heritage &amp; Partnership Authority</div>
        </div>
        <div class="simple-grid">
          <div>
            <div class="grid-label">What This Web Page Will Do Once Built</div>
            <div class="grid-text">
              Presents the 50-year engineering heritage of the Dalal family, authentic photos of the Mumbai registered corporate office and Pune warehouse stockyard, and formal details of the official technical partnership with OMPI Italy. Proves company stability and capability to corporate buyers.
            </div>
          </div>
          <div>
            <div class="grid-label">Business Value &amp; Commercial Risk It Prevents</div>
            <div class="grid-text">
              Proves corporate legitimacy and financial stability, assuring plant owners that their advance payments and multi-crore machinery orders are in trustworthy, experienced hands. Protects brand equity and qualifies corporate vendor registrations with Tier-1 auto manufacturers.
            </div>
          </div>
        </div>
        <div class="deliverables-box">
          <div class="deliverables-title">Key Tangible System Capabilities (To Be Built)</div>
          <div class="deliverables-grid">
            <div class="deliverable-item">
              <svg fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/></svg>
              <span>50-Year Heritage Timeline</span>
            </div>
            <div class="deliverable-item">
              <svg fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/></svg>
              <span>Pune Yard Facility Tour</span>
            </div>
            <div class="deliverable-item">
              <svg fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/></svg>
              <span>OMPI Italy Partnership Certificate</span>
            </div>
          </div>
        </div>
        <div class="feature-strip">
          <strong>Key Management Feature:</strong> Visual timeline highlighting 5 decades of heavy machinery supply across India.
        </div>
      </div>

    </div>
    <div class="footer-bar">
      <div><strong>Dalal Machine Tools Agency Pvt. Ltd. &amp; OMPI India LLP</strong> &bull; Commercial Operations Blueprint</div>
      <div class="confidential-watermark">&#128274; CONFIDENTIAL &bull; STRICTLY NOT FOR SHARING</div>
      <div>Page 2 of 32</div>
    </div>
  </div>
</body>
</html>"""
    
    with open('scratch/test_page.html', 'w', encoding='utf-8') as f:
        f.write(test_html)
    
    edge = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
    pdf = os.path.abspath('scratch/test_page.pdf')
    url = f'file:///{os.path.abspath("scratch/test_page.html").replace("\\", "/")}'
    cmd = [edge, '--headless', '--disable-gpu', f'--print-to-pdf={pdf}', '--no-pdf-header-footer', url]
    subprocess.run(cmd, capture_output=True)
    
    doc = pymupdf.open(pdf)
    print(f"Total pages rendered: {len(doc)}")
    for i, p in enumerate(doc):
        blocks = p.get_text('blocks')
        content_blocks = [b for b in blocks if b[3] < 790]
        max_y = max([b[3] for b in content_blocks]) if content_blocks else 0
        footer_block = [b for b in blocks if b[3] >= 790]
        min_footer_y = min([b[1] for b in footer_block]) if footer_block else 800
        print(f"Page {i+1}: max content y = {max_y:.1f} / 842pt, footer at {min_footer_y:.1f}pt (Empty space: {min_footer_y - max_y:.1f}pt)")

test_card_height()
