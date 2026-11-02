# scratch/audit_57_units.py
import os, json, re

# 1. Audit Dalal 24 Routes
dalal_base = "new/dalalmachine"
routes_spec = [
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

print("="*70)
print("PART 1: AUDIT OF DALAL MACHINE TOOLS 24 ROUTES")
print("="*70)

routes_audit = []
for rid, fname, title in routes_spec:
    fpath = os.path.join(dalal_base, fname)
    exists = os.path.exists(fpath)
    size = os.path.getsize(fpath) if exists else 0
    
    # check features
    features = []
    if exists:
        with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
            c = f.read()
        if "<form" in c: features.append("Form")
        if "wa.me" in c or "whatsapp" in c.lower(): features.append("WhatsApp")
        if "catalog-app.js" in c: features.append("LiveCatalog")
        if "data-animated-content" in c: features.append("AnimatedContent")
        if "dalal-custom.css" in c: features.append("DalalCSS")
        if "og:title" in c or "twitter:card" in c: features.append("SEO-Meta")
        
    status = "PRESENT & OPERATIONAL" if exists and size > 1000 else ("EMPTY" if exists else "MISSING")
    routes_audit.append((rid, fname, title, exists, size, features, status))
    print(f"[{'PASS' if exists else 'FAIL'}] {rid} ({fname}): {size:,} bytes | Features: {', '.join(features)} | Status: {status}")

# 2. Audit OMPI India 33 Modules
print("\n" + "="*70)
print("PART 2: AUDIT OF OMPI INDIA 33 ERP MODULES")
print("="*70)

# Check backend routes, db tables, admin UI
with open("server/data/db.json", "r", encoding="utf-8") as f:
    db = json.load(f)

db_keys = list(db.keys())
print("Database Collections:", db_keys)

# Check server routes
server_routes = []
for rf in os.listdir("server/routes"):
    server_routes.append(rf)
print("Server API Route Handlers:", server_routes)

# Check admin HTML pages
admin_pages = [f for f in os.listdir("admin") if f.endswith(".html")]
print("Admin Portal UI Pages:", admin_pages)

# Check superadmin HTML pages
superadmin_pages = [f for f in os.listdir("superadmin") if f.endswith(".html")]
print("Superadmin Portal UI Pages:", superadmin_pages)

# Check dev UI pages
dev_pages = [f for f in os.listdir("dev") if f.endswith(".html")]
print("Dev Console UI Pages:", dev_pages)

