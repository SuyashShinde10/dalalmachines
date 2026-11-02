import subprocess, os

html = '''<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
<style>
  body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #0b1329; padding: 30px; margin: 0; }
  .wrapper { display: flex; gap: 24px; justify-content: center; flex-wrap: wrap; }
  .col { width: 370px; }

  .machine-item-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 10px;
    overflow: hidden;
    box-shadow: 0 4px 20px -2px rgba(15, 23, 42, 0.08);
    display: flex;
    flex-direction: column;
  }
  .machine-thumb-box {
    position: relative;
    width: 100%;
    height: 220px;
    background: #0f172a;
    overflow: hidden;
  }
  .machine-thumb-box img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
  }
  .machine-location-pill {
    position: absolute;
    top: 12px;
    left: 12px;
    background: rgba(15, 23, 42, 0.85);
    color: #fff;
    padding: 4px 10px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 600;
    backdrop-filter: blur(4px);
    display: inline-flex;
    align-items: center;
    gap: 6px;
    z-index: 2;
  }
  .live-radar-dot {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: #22c55e;
    box-shadow: 0 0 6px #22c55e;
  }
  .machine-stock-badge {
    position: absolute;
    top: 12px;
    right: 12px;
    background: #f89d13;
    color: #000;
    font-weight: 800;
    padding: 3px 8px;
    border-radius: 4px;
    font-size: 11px;
    z-index: 2;
  }

  /* Compare Pill on thumbnail */
  .machine-thumb-compare {
    position: absolute;
    bottom: 12px;
    right: 12px;
    background: rgba(15, 23, 42, 0.85);
    backdrop-filter: blur(6px);
    border: 1px solid rgba(255, 255, 255, 0.25);
    color: #ffffff;
    font-size: 11px;
    font-weight: 600;
    padding: 4px 10px;
    border-radius: 4px;
    cursor: pointer;
    display: inline-flex;
    align-items: center;
    gap: 6px;
    margin: 0;
    z-index: 2;
  }
  .machine-thumb-compare input[type="checkbox"] {
    accent-color: #f89d13;
    cursor: pointer;
    margin: 0;
    width: 13px;
    height: 13px;
  }

  .machine-info-content {
    padding: 18px 20px 20px;
    display: flex;
    flex-direction: column;
    flex: 1;
  }
  .machine-cat-label {
    font-size: 11.5px;
    font-weight: 700;
    color: #f89d13;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    line-height: 1.4;
    margin-bottom: 6px;
  }
  .machine-title {
    font-size: 16.5px;
    font-weight: 700;
    color: #0f172a;
    margin: 0 0 14px;
    line-height: 1.35;
    min-height: 44px;
  }

  /* DESIGN 1: Asymmetric 2x2 (1.2fr 0.8fr) with full text wrapping */
  .grid-v1 {
    display: grid;
    grid-template-columns: 1.2fr 0.8fr;
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    overflow: hidden;
    margin-bottom: 16px;
  }
  .grid-v1 .spec-item {
    padding: 10px 12px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    background: #ffffff;
    border-bottom: 1px solid #edf2f7;
    min-width: 0;
  }
  .grid-v1 .spec-item:nth-child(odd) {
    border-right: 1px solid #edf2f7;
  }
  .grid-v1 .spec-item:nth-child(3), .grid-v1 .spec-item:nth-child(4) {
    border-bottom: none;
  }
  .grid-v1 .spec-item .label {
    color: #64748b;
    font-size: 10px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 3px;
    display: flex;
    align-items: center;
    gap: 5px;
    white-space: nowrap;
  }
  .grid-v1 .spec-item .label i {
    color: #94a3b8;
    font-size: 10px;
    width: 12px;
  }
  .grid-v1 .spec-item .val {
    color: #0f172a;
    font-size: 13px;
    font-weight: 700;
    line-height: 1.25;
    white-space: normal; /* Full text! */
    word-break: break-word; /* Never cut off! */
  }
  .grid-v1 .spec-item .val.status-val {
    color: #16a34a;
    display: inline-flex;
    align-items: center;
    gap: 4px;
  }

  /* DESIGN 2: Clean 3-Tier Layout (Specs + Full-Width Model Bar + Status) */
  .grid-v2 {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    overflow: hidden;
    margin-bottom: 16px;
  }
  .grid-v2-top {
    display: grid;
    grid-template-columns: 1fr 1fr;
    border-bottom: 1px solid #edf2f7;
  }
  .grid-v2-top .spec-item {
    padding: 9px 12px;
    display: flex;
    flex-direction: column;
    justify-content: center;
  }
  .grid-v2-top .spec-item:first-child {
    border-right: 1px solid #edf2f7;
  }
  .grid-v2-bottom {
    display: grid;
    grid-template-columns: 1.2fr 0.8fr;
    background: #fafcff;
  }
  .grid-v2-bottom .spec-item {
    padding: 9px 12px;
    display: flex;
    flex-direction: column;
    justify-content: center;
  }
  .grid-v2-bottom .spec-item:first-child {
    border-right: 1px solid #edf2f7;
  }
  .grid-v2 .label {
    color: #64748b;
    font-size: 10px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 2px;
    display: flex;
    align-items: center;
    gap: 5px;
  }
  .grid-v2 .label i {
    color: #94a3b8;
    font-size: 10px;
    width: 12px;
  }
  .grid-v2 .val {
    color: #0f172a;
    font-size: 13px;
    font-weight: 700;
    line-height: 1.25;
    white-space: normal;
    word-break: break-word;
  }
  .grid-v2 .val.status-val {
    color: #16a34a;
    display: inline-flex;
    align-items: center;
    gap: 4px;
  }

  .machine-card-footer {
    display: flex;
    gap: 8px;
    align-items: center;
    margin-top: auto;
  }
  .btn-view-details {
    flex: 1;
    background: #0f172a;
    color: #fff;
    text-align: center;
    padding: 10px 14px;
    border-radius: 6px;
    font-size: 13px;
    font-weight: 600;
    text-decoration: none;
  }
  .btn-rfq-whatsapp {
    width: 42px;
    height: 42px;
    background: #25d366;
    color: #fff;
    border-radius: 6px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
    text-decoration: none;
  }
</style>
</head>
<body>
<div class="wrapper">

  <!-- Card 1: Custom 4000T with HD-4000-SPECIAL -->
  <div class="col">
    <div style="color:#94a3b8; font-weight:700; margin-bottom:8px; text-align:center;">Card 1: HD-4000-SPECIAL (Fully Visible)</div>
    <div class="machine-item-card">
      <div class="machine-thumb-box">
        <img src="file:///d:/st.ourhtmldemo.com/new/dalalmachine/images/dalal/hero_forging_press.jpg">
        <span class="machine-location-pill"><span class="live-radar-dot"></span> In Stock PUNE (Audited Live)</span>
        <span class="machine-stock-badge">ID: P00099-CUST</span>
        <label class="machine-thumb-compare">
          <input type="checkbox"> Compare
        </label>
      </div>
      <div class="machine-info-content">
        <div class="machine-cat-label">Hot Forging Press &bull; Schuler / Dalal Custom Rebuild</div>
        <h4 class="machine-title">Custom 4000T Hydraulic Closed Die Forging Press with OMPI Clutch</h4>
        <div class="grid-v1">
          <div class="spec-item">
            <span class="label"><i class="fa fa-balance-scale"></i> Capacity</span>
            <span class="val">4000 Tons</span>
          </div>
          <div class="spec-item">
            <span class="label"><i class="fa fa-calendar"></i> Mfg. Year</span>
            <span class="val">2024</span>
          </div>
          <div class="spec-item">
            <span class="label"><i class="fa fa-hashtag"></i> Model</span>
            <span class="val">HD-4000-SPECIAL</span>
          </div>
          <div class="spec-item">
            <span class="label"><i class="fa fa-shield"></i> Status</span>
            <span class="val status-val"><i class="fa fa-check-circle"></i> Inspected</span>
          </div>
        </div>
        <div class="machine-card-footer">
          <a href="#" class="btn-view-details">Full Specifications &rarr;</a>
          <a href="#" class="btn-rfq-whatsapp"><i class="fa fa-whatsapp"></i></a>
        </div>
      </div>
    </div>
  </div>

  <!-- Card 2: Russian 2500T with K8544 / KB8544 -->
  <div class="col">
    <div style="color:#94a3b8; font-weight:700; margin-bottom:8px; text-align:center;">Card 2: K8544 / KB8544 (Fully Visible)</div>
    <div class="machine-item-card">
      <div class="machine-thumb-box">
        <img src="file:///d:/st.ourhtmldemo.com/new/dalalmachine/images/dalal/hero_forging_press.jpg">
        <span class="machine-location-pill"><span class="live-radar-dot"></span> In Stock PUNE</span>
        <span class="machine-stock-badge">ID: P00008</span>
        <label class="machine-thumb-compare">
          <input type="checkbox"> Compare
        </label>
      </div>
      <div class="machine-info-content">
        <div class="machine-cat-label">Hot Forging Press &bull; TMP Voronezh (Russia)</div>
        <h4 class="machine-title">2500T RUSSIAN TMP-VORONEZH Hot Forging Press</h4>
        <div class="grid-v1">
          <div class="spec-item">
            <span class="label"><i class="fa fa-balance-scale"></i> Capacity</span>
            <span class="val">2500 Tons</span>
          </div>
          <div class="spec-item">
            <span class="label"><i class="fa fa-calendar"></i> Mfg. Year</span>
            <span class="val">1988</span>
          </div>
          <div class="spec-item">
            <span class="label"><i class="fa fa-hashtag"></i> Model</span>
            <span class="val">K8544 / KB8544</span>
          </div>
          <div class="spec-item">
            <span class="label"><i class="fa fa-shield"></i> Status</span>
            <span class="val status-val"><i class="fa fa-check-circle"></i> Inspected</span>
          </div>
        </div>
        <div class="machine-card-footer">
          <a href="#" class="btn-view-details">Full Specifications &rarr;</a>
          <a href="#" class="btn-rfq-whatsapp"><i class="fa fa-whatsapp"></i></a>
        </div>
      </div>
    </div>
  </div>

</div>
</body>
</html>
'''

with open('scratch/test_compare_and_model.html', 'w', encoding='utf-8') as f:
    f.write(html)

edge = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
out = r'd:\st.ourhtmldemo.com\scratch\test_compare_and_model.png'
cmd = [edge, '--headless', '--disable-gpu', f'--screenshot={out}', '--window-size=900,750', 'file:///d:/st.ourhtmldemo.com/scratch/test_compare_and_model.html']
subprocess.run(cmd)
print('Screenshot generated:', os.path.exists(out))

