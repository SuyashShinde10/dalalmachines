const fs = require('fs');
const path = require('path');

// 1. Update index.html
const indexPath = path.join(__dirname, '..', 'new', 'dalalmachine', 'index.html');
let index = fs.readFileSync(indexPath, 'utf8');

if (!index.includes('dalal-ai.css')) {
  index = index.replace(
    '<link href="css/dalal-custom.css?v=5.6" rel="stylesheet">',
    '<link href="css/dalal-custom.css?v=5.6" rel="stylesheet">\r\n  <link href="css/dalal-ai.css?v=3.0" rel="stylesheet">'
  );
}

if (!index.includes('#organization')) {
  const orgJsonLd = `  <!-- Schema.org JSON-LD Organization & WebSite for SEO/AEO -->
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@graph": [
      {
        "@type": "Organization",
        "@id": "https://dalalmachines.com/#organization",
        "name": "Dalal Machine Tools Agency Pvt. Ltd.",
        "alternateName": ["Dalal Machine Tools", "Dalal Machinery", "DMTA"],
        "url": "https://dalalmachines.com",
        "logo": {
          "@type": "ImageObject",
          "url": "https://dalalmachines.com/new/dalalmachine/images/logo-dalal.png"
        },
        "description": "Premier Indian importer, stockist, and distributor of heavy metal forming forging presses and CNC machine tools with OMPI India technical clutch-brake partnership.",
        "founder": { "@type": "Person", "name": "Mr. Dalal" },
        "foundingDate": "1985",
        "address": {
          "@type": "PostalAddress",
          "streetAddress": "C-10, Commerce Centre, 78, Tardeo Main Road",
          "addressLocality": "Mumbai",
          "addressRegion": "Maharashtra",
          "postalCode": "400034",
          "addressCountry": "IN"
        },
        "contactPoint": [
          { "@type": "ContactPoint", "telephone": "+91-9821232131", "contactType": "sales", "areaServed": "IN", "availableLanguage": ["English", "Hindi", "Gujarati", "Marathi"] },
          { "@type": "ContactPoint", "telephone": "+91-22-67439873", "contactType": "customer service", "areaServed": "IN" }
        ]
      },
      {
        "@type": "WebSite",
        "@id": "https://dalalmachines.com/#website",
        "url": "https://dalalmachines.com",
        "name": "Dalal Machine Tools Agency",
        "publisher": { "@id": "https://dalalmachines.com/#organization" },
        "potentialAction": {
          "@type": "SearchAction",
          "target": "https://dalalmachines.com/new/dalalmachine/category.html?query={search_term_string}",
          "query-input": "required name=search_term_string"
        }
      }
    ]
  }
  </script>\r\n\r\n`;
  index = index.replace('<!-- Schema.org JSON-LD FAQ Structure for SEO/AEO -->', orgJsonLd + '<!-- Schema.org JSON-LD FAQ Structure for SEO/AEO -->');
}

if (!index.includes('dalal-ai.js')) {
  index = index.replace(
    '<script src="js/dalal-realtime.js?v=5.0"></script>',
    '<script src="js/dalal-realtime.js?v=5.0"></script>\r\n<script src="js/dalal-ai.js?v=4.0"></script>'
  );
}
fs.writeFileSync(indexPath, index, 'utf8');
console.log('index.html updated successfully.');

// 2. Update category.html
const catPath = path.join(__dirname, '..', 'new', 'dalalmachine', 'category.html');
let cat = fs.readFileSync(catPath, 'utf8');

if (!cat.includes('manifest.json')) {
  cat = cat.replace(
    '<link rel="shortcut icon" href="images/favicon.png" type="image/x-icon">',
    '<link rel="manifest" href="/manifest.json">\r\n  <meta name="theme-color" content="#0f172a">\r\n  <link rel="shortcut icon" href="images/favicon.png" type="image/x-icon">'
  );
}

if (!cat.includes('dalal-ai.css')) {
  cat = cat.replace(
    '<link href="css/dalal-custom.css?v=5.0" rel="stylesheet">',
    '<link href="css/dalal-custom.css?v=5.0" rel="stylesheet">\r\n  <link href="css/dalal-ai.css?v=3.0" rel="stylesheet">'
  );
}

// Add AI Matchmaker button under search input if not present
if (!cat.includes('id="ai-matchmaker-btn"')) {
  const matchmakerBtn = `                        <div class="input-group">
                            <input type="text" id="machine-search-input" class="form-control" placeholder="Search make, model, ton..." style="height:42px; font-size:13px;" aria-label="Search machinery">
                            <div class="input-group-append">
                                <span class="input-group-text" style="background:#f89d13; color:#111;"><i class="fa fa-search"></i></span>
                            </div>
                        </div>
                        <button type="button" id="ai-matchmaker-btn" class="btn btn-sm btn-block" style="margin-top:10px; background:linear-gradient(135deg, #0f172a, #1e293b); color:#f89d13; font-weight:700; border:1px solid rgba(248,157,19,0.5); border-radius:6px; padding:8px 12px; font-size:12.5px; display:flex; align-items:center; justify-content:center; gap:8px; cursor:pointer;">
                          <i class="fa fa-magic"></i> AI Machinery Matchmaker
                        </button>`;
  cat = cat.replace(
    /<div class="input-group">[\s\S]*?<input type="text" id="machine-search-input"[\s\S]*?<\/div>[\s\S]*?<\/div>/,
    matchmakerBtn
  );
}

if (!cat.includes('dalal-ai.js')) {
  cat = cat.replace(
    '<script src="js/dalal-realtime.js?v=5.0"></script>',
    '<script src="js/dalal-realtime.js?v=5.0"></script>\r\n<script src="js/dalal-ai.js?v=4.0"></script>'
  );
}

fs.writeFileSync(catPath, cat, 'utf8');
console.log('category.html updated successfully.');

// 3. Update product.html
const prodPath = path.join(__dirname, '..', 'new', 'dalalmachine', 'product.html');
let prod = fs.readFileSync(prodPath, 'utf8');

if (!prod.includes('manifest.json')) {
  prod = prod.replace(
    '<link rel="shortcut icon" href="images/favicon.png" type="image/x-icon">',
    '<link rel="manifest" href="/manifest.json">\r\n  <meta name="theme-color" content="#0f172a">\r\n  <link rel="shortcut icon" href="images/favicon.png" type="image/x-icon">'
  );
}

if (!prod.includes('dalal-ai.css')) {
  prod = prod.replace(
    '<link href="css/dalal-custom.css?v=5.0" rel="stylesheet">',
    '<link href="css/dalal-custom.css?v=5.0" rel="stylesheet">\r\n  <link href="css/dalal-ai.css?v=3.0" rel="stylesheet">'
  );
}

if (!prod.includes('dalal-ai.js')) {
  prod = prod.replace(
    '<div class="mobile-sticky-bar"',
    '<script src="/socket.io/socket.io.js"></script>\r\n<script src="js/dalal-ai.js?v=4.0"></script>\r\n<div class="mobile-sticky-bar"'
  );
}

// Update printMachineSpecSheet to use backend PDF engine
if (prod.includes('function printMachineSpecSheet() {')) {
  const newPrintFunc = `    function printMachineSpecSheet() {
        const urlParams = new URLSearchParams(window.location.search);
        const mId = urlParams.get('id');
        if (mId) {
            window.open(\`/api/products/\${encodeURIComponent(mId)}/spec-sheet\`, '_blank');
            return;
        }
        window.print();
    }`;
  prod = prod.replace(
    /function printMachineSpecSheet\(\) \{[\s\S]*?printWindow\.print\(\);\s*\}/,
    newPrintFunc
  );
}

// Inject Product Schema in populatePDP
if (!prod.includes('dalal-product-schema') && prod.includes('function populatePDP(item) {')) {
  const schemaInjection = `function populatePDP(item) {
        if (!item) return;

        // Enterprise Schema.org Product Structured Data
        let schemaEl = document.getElementById('dalal-product-schema');
        if (!schemaEl) {
            schemaEl = document.createElement('script');
            schemaEl.id = 'dalal-product-schema';
            schemaEl.type = 'application/ld+json';
            document.head.appendChild(schemaEl);
        }
        schemaEl.textContent = JSON.stringify({
            "@context": "https://schema.org/",
            "@type": "Product",
            "name": item.name,
            "image": [
                new URL(item.image, window.location.origin).href
            ],
            "description": \`\${item.name} manufactured by \${item.make} (\${item.year || 'Operational'}). Industrial metal working machinery with \${item.tonnage ? item.tonnage + ' Ton capacity' : 'precision machining'} located at \${item.location}.\`,
            "sku": item.id,
            "mpn": item.model || item.id,
            "brand": {
                "@type": "Brand",
                "name": item.make || "Industrial Leader"
            },
            "offers": {
                "@type": "Offer",
                "url": window.location.href,
                "priceCurrency": "INR",
                "price": "Call for Quotation",
                "priceValidUntil": "2027-12-31",
                "itemCondition": item.condition && item.condition.toLowerCase().includes('refurbished') ? "https://schema.org/RefurbishedCondition" : "https://schema.org/UsedCondition",
                "availability": "https://schema.org/InStock",
                "seller": {
                    "@type": "Organization",
                    "name": "Dalal Machine Tools Agency Pvt. Ltd."
                }
            }
        }, null, 2);`;
  prod = prod.replace('function populatePDP(item) {\n        if (!item) return;', schemaInjection);
  prod = prod.replace('function populatePDP(item) {\r\n        if (!item) return;', schemaInjection);
}

fs.writeFileSync(prodPath, prod, 'utf8');
console.log('product.html updated successfully.');

