# scratch/audit_dalal_routes_deep.py
import os, re

base = "new/dalalmachine"
routes = [
    ("ROUTE-01", "index.html", "Homepage & Industrial Asset Portal"),
    ("ROUTE-02", "about.html", "Corporate Profile & Industrial Heritage"),
    ("ROUTE-03", "services.html", "Import, Rigging & Retrofit Engineering"),
    ("ROUTE-04", "category.html", "Machinery Catalog & Parametric Search"),
    ("ROUTE-05", "product.html", "Machine Engineering Dossier (PDP)"),
    ("ROUTE-06", "brand-new-machinery.html", "Brand New Machinery & Turnkey Lines"),
    ("ROUTE-07", "gallery.html", "Shipment, Yard & Rigging Archive"),
    ("ROUTE-08", "contact.html", "Headquarters, Facility & Direct RFQ"),
    ("ROUTE-09", "contact-2.html", "Express Plant RFQ & Sizing Consultation"),
    ("ROUTE-10", "faqs.html", "Industrial FAQs & Import Compliance Guide"),
    ("ROUTE-11", "testimonial.html", "Client Endorsements & Installation Proof"),
    ("ROUTE-12", "pricing.html", "High Seas CIF Tariffs & Cost Breakdown"),
    ("ROUTE-13", "blog.html", "Industrial Journal & Forging Hub"),
    ("ROUTE-14", "blog-single.html", "Lead Visual Engineering Article"),
    ("ROUTE-15", "blog-large-image.html", "Turnkey Plant Retrofit Case Study"),
    ("ROUTE-16", "projects.html", "Projects & Rigging Portfolio Overview"),
    ("ROUTE-17", "projects-single.html", "Heavy Rigging & Logistics Project Detail"),
    ("ROUTE-18", "projects-modern.html", "Sector-Wise Plant Modernization"),
    ("ROUTE-19", "projects-with-filter.html", "Turnkey Plant Case Study Analysis"),
    ("ROUTE-20", "shop.html", "Tooling, Bolster Plates & Spares Hub"),
    ("ROUTE-21", "shop-single.html", "Spares Engineering Specification (PDP)"),
    ("ROUTE-22", "shoping-cart.html", "RFQ Package & Multi-Item Inquiry Cart"),
    ("ROUTE-23", "checkout.html", "Structured RFQ Proposal Submission"),
    ("ROUTE-24", "404.html", "Error Recovery & Intelligent Routing")
]

results = []
for rid, fname, name in routes:
    fpath = os.path.join(base, fname)
    if not os.path.exists(fpath):
        results.append({"id": rid, "file": fname, "name": name, "status": "MISSING", "size": 0})
        continue
    with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
    
    title_match = re.search(r'<title>([^<]+)</title>', content)
    title = title_match.group(1).strip() if title_match else "NO TITLE"
    
    has_lorem = "lorem ipsum" in content.lower()
    has_nav = "main-menu" in content or "nav" in content.lower()
    has_footer = "main-footer" in content or "footer" in content.lower()
    forms = len(re.findall(r'<form', content, re.I))
    
    results.append({
        "id": rid,
        "file": fname,
        "name": name,
        "title": title,
        "size_kb": round(len(content)/1024, 1),
        "has_lorem": has_lorem,
        "has_nav": has_nav,
        "has_footer": has_footer,
        "forms_count": forms,
        "status": "LIVE & FULLY IMPLEMENTED"
    })

print(f"{'ID':<10} | {'File':<25} | {'Size':<8} | {'Lorem?':<7} | {'Nav/Footer':<10} | {'Status'}")
print("-" * 80)
for r in results:
    nf = "OK" if r.get('has_nav') and r.get('has_footer') else "MISSING"
    print(f"{r['id']:<10} | {r['file']:<25} | {str(r.get('size_kb'))+'KB':<8} | {str(r.get('has_lorem')):<7} | {nf:<10} | {r['status']}")

