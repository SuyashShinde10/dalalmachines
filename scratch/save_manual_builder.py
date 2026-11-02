import os, sys

# Python script to generate the authoritative, comprehensive 57-Unit Master Manual
# covering all 24 Dalal Web Routes and all 33 OMPI India ERP Modules in pristine English.

html_start = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Dalal & OMPI India — Master Systems, Pages & Modular Architecture Manual (24 Routes + 33 ERP Modules)</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Barlow:wght@600;700;800;900&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@500;600;700&display=swap" rel="stylesheet">
<style>
  @page {
    size: A4;
    margin: 12mm 14mm 14mm 14mm;
  }
  * {
    box-sizing: border-box;
    -webkit-print-color-adjust: exact !important;
    print-color-adjust: exact !important;
  }
  body {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    color: #1e293b;
    background: #ffffff;
    line-height: 1.5;
    font-size: 8.8pt;
    margin: 0;
    padding: 0;
  }
  h1, h2, h3, h4, h5 {
    font-family: 'Barlow', sans-serif;
    color: #0f172a;
    margin-top: 0;
    letter-spacing: -0.3px;
  }
  .page-break {
    page-break-after: always;
    break-after: page;
  }
  .avoid-break {
    page-break-inside: avoid;
    break-inside: avoid;
  }
  
  /* Cover Header */
  .cover-box {
    border: 2px solid #0f172a;
    border-radius: 8px;
    padding: 22px 26px;
    margin-bottom: 18px;
    background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
    position: relative;
  }
  .cover-box::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 6px;
    height: 100%;
    background: #f89d13;
    border-top-left-radius: 6px;
    border-bottom-left-radius: 6px;
  }
  .doc-badge {
    display: inline-block;
    background: #0f172a;
    color: #f89d13;
    font-family: 'JetBrains Mono', monospace;
    font-size: 7.5pt;
    font-weight: 700;
    padding: 3px 8px;
    border-radius: 4px;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 8px;
  }
  .doc-title {
    font-size: 19pt;
    font-weight: 900;
    color: #0f172a;
    line-height: 1.2;
    margin: 0 0 6px;
  }
  .doc-subtitle {
    font-size: 10.5pt;
    color: #475569;
    font-weight: 500;
    margin: 0 0 14px;
  }
  .meta-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
    border-top: 1px solid #cbd5e1;
    padding-top: 10px;
    font-size: 8pt;
  }
  .meta-item strong {
    display: block;
    color: #64748b;
    font-size: 7pt;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 2px;
  }
  
  /* System Banner */
  .system-banner {
    background: #0f172a;
    color: #ffffff;
    padding: 10px 16px;
    border-radius: 6px;
    margin: 18px 0 14px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .system-banner h2 {
    color: #ffffff;
    font-size: 13pt;
    margin: 0;
    font-weight: 800;
  }
  .system-banner span {
    color: #f89d13;
    font-family: 'JetBrains Mono', monospace;
    font-size: 8pt;
    font-weight: 600;
  }

  /* Unit Card */
  .unit-card {
    border: 1px solid #e2e8f0;
    border-radius: 6px;
    padding: 12px 14px;
    margin-bottom: 14px;
    background: #ffffff;
    box-shadow: 0 1px 2px rgba(0,0,0,0.02);
  }
  .unit-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1.5px solid #f1f5f9;
    padding-bottom: 6px;
    margin-bottom: 8px;
  }
  .unit-id {
    font-family: 'JetBrains Mono', monospace;
    font-weight: 700;
    font-size: 8.5pt;
    color: #f89d13;
    background: #0f172a;
    padding: 2px 7px;
    border-radius: 4px;
    margin-right: 8px;
  }
  .unit-title {
    font-size: 11pt;
    font-weight: 800;
    color: #0f172a;
  }
  .unit-route {
    font-family: 'JetBrains Mono', monospace;
    font-size: 7.8pt;
    background: #f1f5f9;
    color: #334155;
    padding: 2px 6px;
    border-radius: 4px;
    border: 1px solid #cbd5e1;
  }
  .persona-badge {
    font-size: 7.5pt;
    font-weight: 600;
    color: #1e3a8a;
    background: #eff6ff;
    border: 1px solid #bfdbfe;
    padding: 1px 6px;
    border-radius: 4px;
    margin-left: 8px;
  }

  .unit-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
    margin-bottom: 8px;
  }
  .unit-box {
    background: #f8fafc;
    border: 1px solid #edf2f7;
    border-radius: 4px;
    padding: 8px 10px;
  }
  .unit-box.why {
    background: #fffbeb;
    border-color: #fef3c7;
  }
  .unit-box-title {
    font-size: 7.8pt;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 3px;
    display: flex;
    align-items: center;
    gap: 4px;
  }
  .unit-box-title.why-title {
    color: #b45309;
  }
  .unit-box-title.what-title {
    color: #0f172a;
  }
  .unit-box p {
    margin: 0;
    font-size: 8.2pt;
    color: #334155;
    line-height: 1.45;
  }

  .unit-features {
    background: #fafcff;
    border: 1px solid #e8eef5;
    border-radius: 4px;
    padding: 6px 10px;
    font-size: 8pt;
  }
  .unit-features-title {
    font-size: 7.5pt;
    font-weight: 800;
    text-transform: uppercase;
    color: #475569;
    letter-spacing: 0.4px;
    margin-bottom: 4px;
  }
  .unit-features ul {
    margin: 0;
    padding-left: 14px;
  }
  .unit-features li {
    margin-bottom: 2px;
    color: #334155;
  }
  .unit-features li strong {
    color: #0f172a;
  }
  
  .footer-note {
    border-top: 1px solid #cbd5e1;
    padding-top: 6px;
    margin-top: 12px;
    display: flex;
    justify-content: space-between;
    font-size: 7.5pt;
    color: #94a3b8;
  }
</style>
</head>
<body>

<!-- COVER HEADER -->
<div class="cover-box">
  <div class="doc-badge">Enterprise Technical Specification &bull; Full Industrial Scope</div>
  <h1 class="doc-title">Dalal Machine Tools &amp; OMPI India ERP</h1>
  <div class="doc-subtitle">Complete Architecture, Pages &amp; Modular Breakdown (24 Customer Web Routes + 33 Industrial ERP Modules)</div>
  
  <div class="meta-grid">
    <div class="meta-item">
      <strong>Corporate Entities</strong>
      Dalal Machine Tools Agency Pvt. Ltd.<br>OMPI India LLP
    </div>
    <div class="meta-item">
      <strong>Principal Architect</strong>
      Suyash Shinde<br>
      Pimpri, Pune &bull; +91 96070 28594
    </div>
    <div class="meta-item">
      <strong>Scope Classification</strong>
      57 Complete Functional Units (24 Routes + 33 ERP Engines)
    </div>
    <div class="meta-item">
      <strong>Engineering Standard</strong>
      Full Production-Grade &bull; Zero Dummy Fluff
    </div>
  </div>
</div>

<div class="unit-box" style="margin-bottom: 14px; background:#eff6ff; border-color:#bfdbfe;">
  <p style="font-size: 8.5pt; color:#1e3a8a; line-height:1.5;">
    <strong>Architectural Premise &amp; Tone Directive:</strong> This manual provides an exhaustive, authoritative technical breakdown of every customer web page, internal operations screen, and ERP software module across both organizations. Every item is documented with its business justification (<em>Why it exists / Problem solved</em>), its operational mechanics (<em>What it does / Workflow executed</em>), its functional feature matrix, and the quantitative enterprise value it delivers.
  </p>
</div>
"""

# Let's define the 24 Dalal routes
dalal_routes_data = [
    (
        "ROUTE 01", "Homepage & Heavy Machinery Authority Portal", "index.html", "Plant Owners, Forging Heads",
        "Heavy machinery buyers (forging plant directors, stamping heads, auto Tier-1 managers) require instant credibility. If a portal looks like a synthetic paper broker, buyers leave immediately. This page exists to establish verified physical stockyard capability in Pune, prove heavy press ownership, and eliminate inquiry friction.",
        "Serves as the high-ticket acquisition engine. Features real-time Pune stockyard indicators, instant tonnage filtering, high-seas CIF pricing comparison matrices, world-class OEM showcases (Aida, Schuler, Voronezh), and direct WhatsApp RFQ triggers pre-populating machine specifications.",
        [
            ("Live Radar Stockyard Indicators", "Pulsing green radar dots verifying physical ground availability in Pune Stockyard for immediate power trials."),
            ("Precision Crosshair Spec Grid", "2x2 mathematical hairline grid showing Capacity, Mfg. Year, Model, and Inspected status with zero text wrapping."),
            ("High Seas CIF Financial Matrix", "Comparative analytical table illustrating 8%–15% landed cost savings on direct port shipments versus local yard stock."),
            ("Floating Thumbnail Compare Pill", "Glassmorphic checkbox enabling 4-press comparison without crowding category or make typography."),
            ("Instant WhatsApp RFQ Trigger", "Direct integration pre-populating Machine ID, tonnage, and make into a WhatsApp chat to Mr. Vinit Dalal.")
        ]
    ),
    (
        "ROUTE 02", "About Company & Industrial Heritage", "about.html", "Corporate Committees, Bank Valuers",
        "Institutional buyers, foreign joint ventures, and capital asset financing banks require verifiable corporate legitimacy, leadership accountability, and physical facility proof before approving multi-crore machinery purchases.",
        "Presents the corporate profile of Dalal Machine Tools Agency Pvt. Ltd., leadership by Managing Director Mr. Vinit Dalal, Mumbai Registered Office (Commerce Centre, Tardeo), Pune warehouse stockyard, and technical partnership with OMPI India LLP.",
        [
            ("Executive Leadership Profile", "Detailed credentials of Managing Director Mr. Vinit Dalal overseeing technical evaluation and import logistics."),
            ("Facility Infrastructure Dossier", "Photographic and operational verification of the Pune Industrial Machinery Stockyard for live inspection."),
            ("OMPI Technical Alliance Matrix", "Documentation of authorization for Italian pneumatic clutch-brake conversions, sales, and spares provisioning.")
        ]
    ),
    (
        "ROUTE 03", "Import, Rigging & Retrofit Services", "services.html", "Maintenance Heads, Plant Engineers",
        "Heavy presses require expert foundation engineering, heavy transport logistics, and pneumatic clutch safety modernization. Buyers need assurance that Dalal provides turn-key installation rather than just selling unserviced iron.",
        "Catalogs specialized engineering services: OMPI pneumatic clutch retrofitting, on-site mechanical press alignment, high-tonnage trailer rigging, foundation pit engineering, and genuine Italian spare parts support.",
        [
            ("Before & After Retrofit Gallery", "Side-by-side engineering comparison of obsolete mechanical dog clutches versus modern OMPI pneumatic clutch-brakes."),
            ("Turn-Key Installation Milestones", "Step-by-step service delivery: Yard audit -> Crankshaft machining -> Pneumatics -> PLC interlock -> 100-cycle trial."),
            ("Service Audit Request Dispatcher", "Specialized inquiry form capturing press model, crankshaft dimensions, and plant location for immediate service quotes.")
        ]
    ),
    (
        "ROUTE 04", "Used Machinery Catalog & Multi-Facet Search", "category.html", "Procurement Officers, Plant Managers",
        "Factory procurement teams do not browse general listings; they seek specific parameters (e.g., 1600T Knuckle Joint Press, 110mm Boring Machine). Blind scrolling causes buyer bounce. This page provides high-speed parametric filtering.",
        "Executes client-side real-time filtering across 26 industrial categories (15 Metal Forming + 11 Metal Cutting), tonnage bands, manufacturer makes, and stockyard locations. Features instant Grid/Table layout toggling and side-by-side comparison modals.",
        [
            ("26 Category Hierarchical Sidebar", "15 Metal Forming categories (Hot Forging, C-Frame, Hydraulic) + 11 Metal Cutting categories with live stock counters."),
            ("Tonnage Range Filter Chips", "One-touch segmentation: Under 500T, 500T–1000T, 1000T–3000T, and 3000T+ for heavy forging requirements."),
            ("Grid vs. Tabular Excel View Toggle", "Enables visual photo-card view for plant directors and dense parameter-table view for procurement analysts."),
            ("Multi-Machine Comparison Engine", "Compares up to 4 selected machines side-by-side across 10 certified engineering parameters simultaneously.")
        ]
    ),
    (
        "ROUTE 05", "Machine Engineering Dossier & PDP", "product.html", "Chief Technical Officers (CTOs), Works Managers",
        "Before a factory director travels to Pune or sanctions a 20% advance, their engineering team must verify mechanical dimensions (Stroke, Die Height, Bolster Bed Area, Motor HP). This page acts as an unassailable digital technical dossier.",
        "Renders multi-angle high-resolution photo/video evidence, certified 10-parameter specification matrix, physical inspection readiness status, high-seas CIF quotation forms, and related machinery recommendations.",
        [
            ("Certified Technical Specification Table", "Verified factory data: Tonnage, Stroke Length, Continuous SPM, Bolster Bed Size, Slide Dimensions, Motor KW."),
            ("Yard Inspection Trial Badge", "Status flag certifying whether power is connected for live trial at Pune Stockyard or in bonded transit."),
            ("Direct Machine RFQ Engine", "Captures company name, mobile, and technical inquiries, notifying Mr. Vinit Dalal via secure database and WhatsApp.")
        ]
    ),
    (
        "ROUTE 06", "Brand New Machinery & Turnkey Press Lines", "brand-new-machinery.html", "Defence Suppliers, Tier-1 Auto OEMs",
        "Major automotive suppliers and government defence forge shops often operate under corporate mandates prohibiting second-hand equipment. Dalal partners with global OEMs (DMT & ECAI) to capture new multi-crore plant supply contracts.",
        "Showcases factory-new automated forging press lines, knuckle joint extrusion presses, and hydraulic trim presses with CE certification, manufacturer warranties, and turn-key plant consultation.",
        [
            ("Turn-Key Automated Forging Line Specs", "Full line architecture: Induction Billet Heater -> Forging Press -> Trimming Press -> Robotic Manipulator."),
            ("CE Conformity & Warranty Documentation", "Comprehensive breakdown of European CE safety standards, dual pneumatic valves, and manufacturer warranty coverage.")
        ]
    ),
    (
        "ROUTE 07", "Shipment, Yard & Machine Rigging Archive", "gallery.html", "Commercial Lenders, Plant Inspectors",
        "Heavy machinery transactions require visual proof of past import success. Buyers want to see heavy 50-ton presses being unloaded, rigged, and delivered to Indian factories.",
        "Visual media archive displaying physical arrivals at Pune Stockyard, customs de-stuffing at Mumbai port, heavy multi-axle trailer transport, and successful client plant installations.",
        [
            ("Categorized Visual Tagging", "Filter media by: Pune Yard Stock, Port De-Stuffing, Heavy Rigging, On-Site Commissioning."),
            ("Machine Identity Verification", "Each photo references the specific Machine ID and OEM Make for complete authenticity.")
        ]
    ),
    (
        "ROUTE 08", "Headquarters, Facility & Direct Quotation Portal", "contact.html", "Plant Owners, Logistics Transporters",
        "Provides total logistics and administrative clarity. Transporters moving heavy low-bed trailers need exact expressway route guidance, visiting hours, and direct access to leadership.",
        "Presents Mumbai Registered Office (Tardeo) and Pune Industrial Machinery Stockyard, interactive dual Google Map switcher, visiting guidelines, and a spacious 38px-padded secure quotation request form.",
        [
            ("Interactive Dual Map Switcher", "One-click toggle between Mumbai Headquarters and Pune Machinery Stockyard maps."),
            ("38px Padded Secure Quotation Card", "Mathematically balanced RFQ card with Honeypot anti-spam protection and input focus halos."),
            ("Direct to MD Leadership Badge", "Legitimate trust indicator confirming that quotation requests are routed directly to Managing Director Mr. Vinit Dalal.")
        ]
    ),
    (
        "ROUTE 09", "Express Plant RFQ & Sizing Consultation", "contact-2.html", "Urgent Breakdown Buyers, Project Leads",
        "When an automotive stamping line suffers a catastrophic crankshaft failure, the plant loses lakhs of rupees per day. They require an expedited RFQ channel to secure emergency replacement presses.",
        "Streamlined single-purpose emergency quotation page. Captures press type, required tonnage, bed size constraints, and target delivery timeframe for immediate stock matching.",
        [
            ("Emergency Replacement Selector", "Checkbox priority flagging: Immediate Stockyard Pickup (<48 Hours) vs. High Seas Import."),
            ("Direct Mobile & WhatsApp Link", "Instant hotlink to executive direct lines for round-the-clock emergency procurement triage.")
        ]
    ),
    (
        "ROUTE 10", "Industrial FAQs & Import Compliance Guide", "faqs.html", "CFOs, Customs Logistics Managers",
        "Importing heavy capital goods involves complex customs tariffs, high-seas sales agreements, GST input tax credits, and port clearance procedures. An authoritative FAQ eliminates buyer hesitation.",
        "Answers technical, financial, and legal questions regarding High Seas Sales agreements, Bill of Lading transfers, live inspection trials at Pune yard, and warranty terms.",
        [
            ("High Seas Legal Explanation", "Clarifies Section 5(2) of the CST Act regarding tax savings on transfers prior to customs clearance."),
            ("Inspection & Trial Protocol", "Explains safety prerequisites, electrical test bench capabilities, and booking appointments at Pune Stockyard.")
        ]
    ),
    (
        "ROUTE 11", "Client Endorsements & Installation Proof", "testimonial.html", "Board Members, Procurement Committees",
        "Industrial purchases of ₹50 Lakh to ₹5 Crore require social proof from recognizable industry peers (forging units, auto-component makers, electrical stamping plants).",
        "Catalogs verified case testimonials from plant directors across Chakan, Aurangabad, Rajkot, and Jamshedpur detailing machine reliability, delivery accuracy, and OMPI clutch performance.",
        [
            ("Sector-Wise Client Testimonials", "Testimonials categorized by: Automotive Forging, Stamping & Sheet Metal, Heavy Engineering, Precision Tooling."),
            ("Delivered Machine Verification", "Lists specific machine model and tonnage delivered to each client for unassailable credibility.")
        ]
    ),
    (
        "ROUTE 12", "High Seas CIF Tariffs & Cost Breakdown", "pricing.html", "Financial Controllers, Accounts Directors",
        "Buyers need complete transparency regarding why Dalal's High Seas Sales model is commercially superior to importing directly from foreign auction brokers.",
        "Presents transparent cost breakdown matrices comparing Direct Foreign Import, Local Reseller Pricing, and Dalal High Seas Sales (CIF Nhava Sheva / Mumbai Port).",
        [
            ("Landed Cost Parameter Matrix", "Itemizes Foreign Purchase Cost, Ocean Freight, Customs Duty (7.5%), Port Handling, and Local Transport."),
            ("Working Capital Advantage", "Demonstrates how Dalal absorbs international foreign exchange currency risk during sea transit.")
        ]
    ),
    (
        "ROUTE 13", "Industrial Journal & Forging Technology Hub", "blog.html", "Production Engineers, Plant Heads",
        "Generates organic search visibility (SEO/AEO) for high-intent keywords (e.g., 'converting mechanical press to pneumatic clutch', 'high seas machinery import India').",
        "Features technical articles, whitepapers, and market reports on metal forming technology, press maintenance, hydraulic vs. mechanical press selection, and OMPI clutch retrofits.",
        [
            ("Technical Engineering Whitepapers", "Deep-dive articles explaining flywheel kinetic energy, stopping angles, and pneumatic valve response times."),
            ("Search Engine Citability Markup", "Structured JSON-LD schema ensuring articles rank in Google Search and AI answer engines.")
        ]
    ),
    (
        "ROUTE 14", "Lead Visual Engineering Article", "blog-single.html", "Senior Technical Specialists",
        "Provides in-depth technical analysis on specific engineering topics, such as mechanical clutch failure root cause analysis or crankshaft alignment tolerances.",
        "Long-form editorial layout with high-resolution schematic diagrams, mechanical drawings, torque calculation formulas, and downloadable technical PDF links.",
        [
            ("Schematic Visual Breakouts", "Annotated mechanical drawings showing air inlet rotary unions, friction linings, and dual solenoid valves."),
            ("Contextual Consultation CTA", "Inline banner prompting readers to book an on-site technical inspection for their press line.")
        ]
    ),
    (
        "ROUTE 15", "Turnkey Plant Retrofit Case Study", "blog-large-image.html", "Corporate Investors, Factory Owners",
        "Demonstrates complete plant modernization capability through an exhaustive, photo-documented case study of an entire forge shop overhaul.",
        "Details a real-world case study: 2500-ton Russian forging press overhaul, installation of OMPI combined clutch-brake, PLC integration, and 30% cycle speed improvement.",
        [
            ("Project Timeline & Milestones", "Chronological documentation: De-commissioning -> Shaft machining -> Installation -> 100-cycle trial -> Handover."),
            ("Quantitative Performance Results", "Data points proving SPM increase, air consumption reduction, and 100% elimination of operator safety incidents.")
        ]
    ),
    (
        "ROUTE 16", "Projects & Rigging Portfolio Overview", "projects.html", "Project Directors, Logistics Heads",
        "Showcases Dalal's multi-ton rigging and turnkey machinery delivery capability across industrial corridors throughout India.",
        "Interactive project grid filtered by project type: Heavy Press Rigging, Turnkey Forging Plant Setup, CNC Machine Import, and OMPI Clutch Modernization.",
        [
            ("Tonnage & Location Filter", "Filter past projects by tonnage capacity (Up to 4000T) and geographical cluster (Pune, NCR, Gujarat, Tamil Nadu)."),
            ("Project Summary Cards", "Key project metrics: Machine Make, Tonnage, Execution Timeline, and Scope of Rigging.")
        ]
    ),
    (
        "ROUTE 17", "Heavy Rigging & Logistics Project Detail", "projects-single.html", "Logistics Managers, Safety Officers",
        "Documents the specialized transport and precision offloading of extreme-tonnage single-piece press frames (40T–120T) requiring multi-axle hydraulic trailers.",
        "Technical narrative covering road permits, hydraulic gantry crane lifting, foundation pit positioning, and millimeter-accurate anchor bolt alignment.",
        [
            ("Rigging Equipment Specifications", "Details hydraulic strand jacks, multi-axle trailers, and crane configurations used for heavy positioning."),
            ("Safety & Compliance Checklist", "Zero-incident safety certification and factory inspectorate compliance documentation.")
        ]
    ),
    (
        "ROUTE 18", "Sector-Wise Plant Modernization", "projects-modern.html", "Automotive, Aerospace & Defence Heads",
        "Industrial buyers need to know that Dalal understands their specific sector requirements (e.g., auto chassis stamping vs. railway axle forging).",
        "Categorizes past deliveries and installations by industrial sector: Automotive Tier-1, Railway Forging, Aerospace Components, and Electrical Stampings.",
        [
            ("Industry-Specific Standards", "Highlights compliance with ISO/TS automotive standards and defence manufacturing tolerances."),
            ("Sector Equipment Matrix", "Recommended press types, stroke lengths, and die space configurations tailored to each industry.")
        ]
    ),
    (
        "ROUTE 19", "Turnkey Plant Case Study Analysis", "projects-with-filter.html", "Factory Expansion Committees",
        "Enables expansion planners to review comprehensive case studies filtered by machine type, budget range, and commissioning timeframe.",
        "Searchable case repository demonstrating how Dalal sourced, imported, refurbished, and commissioned complete machinery lines within target budgets.",
        [
            ("Parametric Case Search", "Filter by Machine Type (Coining, Forging, Trimming) and OEM Brand (Schuler, Komatsu, Voronezh)."),
            ("Commercial Cost Efficiency Analysis", "Compares turnkey delivered price against the cost of purchasing new European equipment.")
        ]
    ),
    (
        "ROUTE 20", "Tooling, Bolster Plates & Spares Hub", "shop.html", "Store Managers, Tool Room Heads",
        "Presses cannot run without bolster plates, pneumatic friction discs, rotary unions, and dual valves. Dalal provides authentic spare components.",
        "Digital catalog of mechanical press tooling, replacement bolster plates, hydraulic overload cylinders, and genuine OMPI spare parts.",
        [
            ("Sub-Assembly & Spares Categories", "Categorized into: Clutch Friction Plates, Rotary Unions, Dual Safety Valves, Hydraulic Overload Systems."),
            ("Live Inventory Availability", "Real-time stock indicators showing whether spares are ready for immediate Pune yard dispatch.")
        ]
    ),
    (
        "ROUTE 21", "Spares Technical Specification Detail", "shop-single.html", "Maintenance Engineers, Store Keepers",
        "Ordering the wrong friction disc diameter or rotary union thread pitch causes costly return shipments. Maintenance engineers need precise mechanical drawings.",
        "Provides exact dimensional specs, friction coefficient ratings, air pressure tolerances, and machine compatibility lists for individual spare parts.",
        [
            ("Dimensional CAD Schematic", "Technical drawing detailing outer diameter, spline count, lining thickness, and bolt circle diameter."),
            ("Compatible Press Reference List", "Cross-references spare part SKUs against compatible press makes (Godrej, Aida, Komatsu, Voronezh).")
        ]
    ),
    (
        "ROUTE 22", "RFQ Package & Multi-Item Inquiry Cart", "shoping-cart.html", "Procurement Officers, Plant Managers",
        "Industrial buyers frequently inquire about a complete machinery package (e.g., 1 Forging Press + 1 Trimming Press + 2 Spare Friction Lining Sets).",
        "Enables buyers to bundle multiple machines and spare parts into a single consolidated inquiry package for volume quotation negotiations.",
        [
            ("Package Summary Ledger", "Displays selected equipment with photo, machine ID, capacity, and selected destination port/yard."),
            ("Direct RFQ Export", "Converts the package into a structured PDF inquiry or pre-filled multi-item WhatsApp RFQ.")
        ]
    ),
    (
        "ROUTE 23", "Structured RFQ Proposal Submission", "checkout.html", "Corporate Buyers, Purchase Heads",
        "Large enterprises require formalized quotation requests with plant delivery addresses, GSTIN numbers, and target commissioning dates.",
        "Captures complete buyer corporate data: Company Name, Factory Location, GSTIN, Target Delivery Timeline, and Preferred Commercial Terms (Ex-Pune Yard vs. CIF Nhava Sheva).",
        [
            ("GSTIN Auto-Validation", "Validates corporate tax registration and automatically suggests state-specific logistics corridors."),
            ("Encrypted Data Handshake", "Directly ingests RFQs into the Dalal Staff Console and generates confirmation receipts.")
        ]
    ),
    (
        "ROUTE 24", "Error Recovery & Intelligent Machinery Routing", "404.html", "All Lost Site Visitors",
        "When buyers follow outdated links or sold machinery bookmarks, landing on a blank 404 error page causes immediate site exit.",
        "Intelligent error recovery screen. Automatically analyzes the broken URL and suggests the closest matching active machinery categories and top ready-stock presses.",
        [
            ("Parametric Alternative Suggestions", "Displays 3 active in-stock heavy presses matching the user's probable search intent."),
            ("Quick Search & Direct Assistance", "Integrated search bar and one-click WhatsApp button to ask Mr. Vinit Dalal about specific unlisted stock.")
        ]
    )
]

# Let's define the 33 OMPI ERP modules
ompi_modules_data = [
    # Engine 1: Commercial Sales (01 to 10)
    (
        "MOD 01", "Client Master & Credit Term Profiler", "Engine 1: Commercial Sales", "Sales Directors, Financial Controllers",
        "Forge shops and auto component plants operate on complex corporate structures with distinct plant locations and strict credit terms. Selling without verified GSTIN and credit limits leads to bad debts and GST input tax credit disputes.",
        "Maintains verified corporate profiles of machinery buyers, validated 15-digit GSTINs, delivery plant addresses, allocated credit limits, and approved payment milestone templates (e.g., 30% Advance, 50% Against Dispatch, 20% Post-Installation).",
        [
            ("Corporate GSTIN Validator", "Verifies state codes and tax compliance status to ensure flawless B2B tax invoicing."),
            ("Credit Limit & Ledger Balance Sentinel", "Automatically flags sales orders if a client's outstanding accounts receivable exceeds approved limits."),
            ("Multi-Plant Delivery Address Book", "Stores distinct delivery locations for tier-1 suppliers with plants across Pune, NCR, and Chennai.")
        ]
    ),
    (
        "MOD 02", "OMPI Technical Catalog & SKU Master", "Engine 1: Commercial Sales", "Sales Engineers, Technical Estimators",
        "OMPI Italy manufactures hundreds of combined clutch-brake variations (flange-mounted, shaft-mounted, hydraulic, spring-applied). Pricing from outdated Excel sheets results in quoting obsolete models or wrong torque ratings.",
        "Parametric technical database of all OMPI Italy assemblies and components: Pneumatic Clutches, Hydraulic Brakes, Rotary Unions, Friction Discs, and Mac Safety Valves with certified torque ratings, air pressure requirements, and dimensional drawings.",
        [
            ("Parametric Engineering Lookup", "Filter models by Torque Capacity (Nm), Max Flywheel RPM, Operating Air Pressure (Bar), and Bore Diameter."),
            ("Bilingual Nomenclature Mapping", "Maps Italian factory part numbers to internal Indian ERP SKUs for seamless import ordering."),
            ("Digital Drawing Attachment", "Directly attaches certified 2D General Arrangement (GA) drawings and 3D CAD step files to each SKU.")
        ]
    ),
    (
        "MOD 03", "Multi-Currency Pricing Engine", "Engine 1: Commercial Sales", "Commercial Directors, Finance Managers",
        "OMPI units are imported in Euros (EUR) while sold to Indian factories in Rupees (INR). Unhedged currency fluctuations can completely wipe out sales margins between the date of quotation and the date of import delivery.",
        "Calculates real-time commercial pricing by factoring base EUR catalog rates, forward currency hedging buffers, customs duty tariffs, ocean freight markups, and minimum gross margin percentages.",
        [
            ("Dynamic EUR to INR Pegging", "Configurable base exchange rate with automated currency volatility buffer alerts."),
            ("Gross Margin Floor Sentinel", "Prevents sales executives from issuing quotations that fall below company gross margin thresholds."),
            ("Validity Period Lock", "Automatically sets 30-day price validity expirations on quotations to protect against currency devaluations.")
        ]
    ),
    (
        "MOD 04", "Fast-Quote PDF Generator", "Engine 1: Commercial Sales", "Frontline Sales Engineers",
        "Plant procurement heads demand formal, professionally formatted technical quotations. Delaying quotation delivery by 2 days allows local non-standard clutch re-builders to capture the contract.",
        "Generates formal, branded PDF quotations in under 60 seconds. Auto-populates OMPI corporate headers, client GSTIN, technical specifications, torque curves, dimensional drawings, and commercial terms.",
        [
            ("1-Click PDF Engine", "Compiles formatted PDF documents with high-resolution drawings and commercial terms."),
            ("Technical Curve Embedding", "Includes clutch dynamic torque curves and air volume consumption charts for plant engineering review."),
            ("Automated Revision Control", "Tracks quotation revisions (Rev 0, Rev 1, Rev 2) preserving full audit history of commercial negotiations.")
        ]
    ),
    (
        "MOD 05", "RFQ Lifecycle & Visual Pipeline", "Engine 1: Commercial Sales", "Managing Director, Sales Heads",
        "Inquiries received across WhatsApp, phone calls, and email get lost when managed informally. High-ticket industrial deals take 3–6 months to close and require disciplined stage-by-stage follow-up.",
        "Visual Kanban and tabular sales pipeline tracking inquiries across 6 discrete milestones: New RFQ -> Technical Sizing Review -> Quote Dispatched -> Commercial Negotiation -> Proforma Issued -> Confirmed Sales Order.",
        [
            ("Visual Kanban Stage Cards", "Drag-and-drop opportunity cards with deal value, client name, and days in stage indicators."),
            ("Follow-up Aging Alerts", "Automated alerts for quotations with no customer contact after 7, 14, and 21 days."),
            ("Win/Loss Analytics Log", "Records reasons for lost deals (price, delivery timeline, competitor) to refine sales strategy.")
        ]
    ),
    (
        "MOD 06", "Machine Compatibility & Retrofit Matrix", "Engine 1: Commercial Sales", "Mechanical Application Engineers",
        "Matching an Italian clutch to an Indian or foreign press (Godrej, Aida, Komatsu, Voronezh) requires checking crankshaft diameter, flywheel bore, and torque. Sizing errors cause press failure or clutch burnout.",
        "Algorithmic compatibility matrix mapping press capacity, flywheel inertia, and RPM against recommended OMPI models. Recommends necessary shaft machining or adapter flange specifications.",
        [
            ("Press Make Compatibility Registry", "Pre-mapped compatibility templates for 50+ common mechanical press brands operating in India."),
            ("Shaft Stress & Torque Verification", "Calculates whether press crankshaft can safely absorb the instantaneous braking torque of the clutch."),
            ("Adapter Flange Sizing Output", "Generates required adapter plate dimensions to bridge Italian mounting holes to existing press flywheels.")
        ]
    ),
    (
        "MOD 07", "Customer Discount & Margin Matrix", "Engine 1: Commercial Sales", "Managing Director, Sales Executives",
        "Discounts cannot be handed out arbitrarily. OEM press builders buying 20 units per year require different discount structures than end-user forge shops buying 1 replacement lining set.",
        "Enforces tiered discount rules based on buyer classification (OEM Press Builder, Tier-1 Forge Shop, Authorized Service Center, End-User) and order volume.",
        [
            ("Tiered Category Rules", "Automatically applies approved discount tiers while locking maximum allowable sales executive discretion."),
            ("Two-Tier Approval Workflow", "Discounts exceeding standard tiers require digital authorization from Managing Director Mr. Vinit Dalal."),
            ("Net Profit Visibility", "Displays net profit margin in real time before sales staff submit quotes for approval.")
        ]
    ),
    (
        "MOD 08", "Proforma Invoice (PI) Generator", "Engine 1: Commercial Sales", "Commercial Sales Accountants",
        "Indian manufacturing enterprises require formal Proforma Invoices with statutory bank details, HSN codes, and milestone breakdowns to initiate corporate advance payments.",
        "Generates statutory Proforma Invoices with complete payment schedule breakdown (e.g., 30% Advance with PO, 50% Pro-forma against inspection/dispatch, 20% post-commissioning).",
        [
            ("Statutory Bank Wire Details", "Pre-printed RTGS/NEFT banking coordinates, IFSC code, and branch details for swift corporate payment."),
            ("Advance Payment Tracking", "Links incoming bank UTR transaction numbers directly to the Proforma Invoice record.")
        ]
    ),
    (
        "MOD 09", "Sales Order (SO) Conversion Engine", "Engine 1: Commercial Sales", "Operations Managers, Warehouse Storekeepers",
        "Once a client pays an advance, the commercial agreement must be permanently locked into an operational Sales Order. Allowing sales staff to edit terms after advance receipt causes supply chain chaos.",
        "One-click conversion of approved Proforma Invoices into confirmed, immutable Sales Orders. Freezes agreed commercial prices and automatically triggers material reservation in the warehouse.",
        [
            ("Inventory Stock Reservation", "Immediately reserves matching serialized clutch units or allocates them against incoming Italy shipments."),
            ("Production & Machining Trigger", "Automatically generates engineering work orders if customized adapter plates or boring are required."),
            ("Immutable Contract Freeze", "Locks commercial pricing to prevent accidental or unauthorized alterations post-advance receipt.")
        ]
    ),
    (
        "MOD 10", "WhatsApp & Email Quote Dispatcher", "Engine 1: Commercial Sales", "Field Sales Executives",
        "Procurement directors in forge shops operate via WhatsApp on plant floors. Email-only communication delays responses. Integrated dispatch ensures instant proposal receipt.",
        "Automated PDF quotation delivery via verified WhatsApp API and corporate SMTP email. Tracks document delivery, open status, and direct customer replies.",
        [
            ("Automated PDF Attachment", "Attaches clean technical quotation PDF and dimensional drawings directly to a WhatsApp message."),
            ("Standardized Corporate Message Templates", "Enforces professional communication standards across all sales engineer communications."),
            ("Dispatch Audit Log", "Records exact timestamp, recipient phone number, and delivery status in the client CRM record.")
        ]
    ),
    # Engine 2: Engineering BOM & Italy Landed Cost (11 to 17)
    (
        "MOD 11", "Multi-Level Bill of Materials (BOM)", "Engine 2: Engineering & Imports", "Technical Directors, Assembly Heads",
        "A combined pneumatic clutch-brake is a precision mechanical assembly of castings, friction discs, return springs, piston seals, and pneumatic valves. Tracking them without a structured BOM causes assembly line stoppages.",
        "Maintains multi-level hierarchical Bill of Materials (BOM) linking parent clutch assemblies to sub-assemblies (piston group, brake group) and serviceable wear components (friction blocks, seal kits).",
        [
            ("Parent-Child Component Tree", "Visual tree structure showing complete component breakdown from casting to smallest O-ring."),
            ("Wear Part Flagging", "Flags high-turnover friction plates and seals for automated re-order buffer calculations."),
            ("Engineering Revision Tracking", "Maintains historical engineering changes across Italian OEM design updates.")
        ]
    ),
    (
        "MOD 12", "Italy Import Purchase Order (PO)", "Engine 2: Engineering & Imports", "Import Logistics Managers",
        "Ordering from OMPI S.r.l. in Modena, Italy requires precise Italian OEM part codes, international Incoterms (FOB/CIF), and Euro currency specifications to avoid customs documentation discrepancies.",
        "Automates generation of formal Purchase Orders in EUR formatted specifically for OMPI Italy. Tracks factory order acknowledgment numbers, manufacturing lead times, and dispatch readiness.",
        [
            ("Automated Factory Order Formatting", "Generates compliant European purchase orders with exact Italian manufacturing SKUs."),
            ("Lead-Time Milestone Tracking", "Monitors factory production milestones from raw casting to CNC machining and pressure testing."),
            ("PO Revision Management", "Records changes in shipment schedules or container batch allocations.")
        ]
    ),
    (
        "MOD 13", "Landed Cost & Customs Duty Calculator", "Engine 2: Engineering & Imports", "Cost Accountants, Logistics Directors",
        "Customs valuation in India involves complex compounding calculations: Basic Customs Duty (BCD), Social Welfare Surcharge (SWS), Integrated GST (IGST), and ocean freight. Errors lead to under-pricing or unexpected tax audits.",
        "Algorithmic cost buildup engine calculating complete landed cost per unit: Ex-Works EUR -> Sea/Air Freight -> Insurance -> Assessable Value -> BCD (7.5%) -> SWS (10%) -> Port Clearance -> Inland Freight -> Net Landed Cost in INR.",
        [
            ("Customs Formula Automation", "Calculates assessable value and compounding duties in accordance with Indian Customs regulations."),
            ("Proportionate Duty Allocation", "Allocates shared container freight across individual clutch units based on gross weight and value."),
            ("Unit Cost Freezing", "Establishes exact landed baseline cost in INR for accurate gross profit tracking on every invoice.")
        ]
    ),
    (
        "MOD 14", "Shipment & Bill of Lading (BL) Ledger", "Engine 2: Engineering & Imports", "Import Managers, CHA Coordinators",
        "Shipments from Genoa/La Spezia to Nhava Sheva (JNPT) port take 25–35 days at sea. Tracking container status is essential for scheduling plant deliveries and avoiding demurrage penalties.",
        "International shipping ledger tracking Bill of Lading (BL) numbers, container IDs, vessel tracking, shipping line ETAs, port arrivals, customs assessment dates, and out-of-charge orders.",
        [
            ("Port Demurrage Sentinel", "Alerts logistics staff 72 hours before container free-time expires at JNPT port to prevent detention charges."),
            ("Bill of Entry (BOE) Linkage", "Links customs BOE numbers and duty payment challans directly to the import shipment record."),
            ("CHA Clearance Milestone Tracker", "Tracks customs broker milestones: Filing -> Assessment -> Duty Payment -> Physical Exam -> Gate Out.")
        ]
    ),
    (
        "MOD 15", "Technical Drawing & GA Repository", "Engine 2: Engineering & Imports", "Design Engineers, Tool Room Managers",
        "Factory tool rooms and machine builders need dimensional drawings to prepare press flywheels and crankshafts before the imported clutch arrives in India.",
        "Centralized encrypted repository of OMPI Italy General Arrangement (GA) drawings, CAD 2D/3D step models, and electrical wiring schematics for dual safety valves.",
        [
            ("Searchable Drawing Index", "Instant lookup by Clutch Model, Flywheel Bore, or Press Brand."),
            ("Secure Client Drawing Sharing", "Generates watermarked, expiring PDF drawing links for plant engineering teams."),
            ("Wiring Schematic Library", "Provides electrical wiring diagrams for interlocking OMPI dual solenoid valves with plant PLC panels.")
        ]
    ),
    (
        "MOD 16", "Torque & Pneumatic Pressure Sizing Calculator", "Engine 2: Engineering & Imports", "Senior Application Engineers",
        "A clutch operating with insufficient air pressure (e.g., 4 bar instead of 5.5 bar) slips, generates extreme friction heat, and burns out within days. Technical sizing must verify dynamic torque.",
        "Interactive formula calculator computing static torque (Nm), dynamic torque under load, stopping angle in degrees, thermal energy dissipation (Joules/hour), and required pneumatic air volume per engagement.",
        [
            ("Stopping Time Calculation", "Verifies compliance with Indian factory safety inspectorate standards (<0.20 second emergency stop)."),
            ("Thermal Capacity Verification", "Calculates whether heat generated during continuous stamping cycles exceeds permissible clutch limits."),
            ("Pneumatic Line Sizing Helper", "Recommends exact pipe diameter and air reservoir tank capacity to prevent pressure drops.")
        ]
    ),
    (
        "MOD 17", "Import Duty & HSN Tariff Master", "Engine 2: Engineering & Imports", "Customs Compliance Officers",
        "Classifying industrial goods under incorrect HSN codes triggers customs confiscation, penalties, and loss of input tax credits. Clutches and presses have distinct customs classifications.",
        "Statutory repository of customs tariff codes (HSN 84836090 for clutches/shaft couplings, HSN 84812000 for pneumatic valves) with applicable BCD, IGST, and anti-dumping notification histories.",
        [
            ("Tariff Rule Master", "Maintains current BCD, SWS, and GST rates mapped to each product classification."),
            ("Customs Notification History", "Tracks government duty amendments and exemption notifications for capital machinery imports.")
        ]
    ),
    # Engine 3: Spares Inventory & Multi-Yard Hub (18 to 25)
    (
        "MOD 18", "Real-Time Stock Ledger & Bin Management", "Engine 3: Warehouse Operations", "Warehouse In-Charge, Storekeepers",
        "Losing track of high-value clutch assemblies in a busy warehouse results in delayed dispatches, ghost inventory, and capital tied up in misplaced stock.",
        "Maintains real-time physical bin and rack tracking at Bhosari/Pune central warehouse. Tracks live on-hand quantity, allocated stock, transit stock, and bin locations (Rack/Row/Bin).",
        [
            ("Multi-Bin Location Engine", "Pinpoints exact physical shelf location of every clutch model and spare component."),
            ("Live Inventory Valuation", "Continuously recalculates total warehouse inventory value based on FIFO landed costs."),
            ("Physical vs. Book Stock Audit", "Facilitates monthly rolling cycle counts with automated variance reporting.")
        ]
    ),
    (
        "MOD 19", "Friction Disc & Wear Parts Tracker", "Engine 3: Warehouse Operations", "Spare Parts Managers",
        "Friction linings, sintered bronze plates, and piston seals are high-wear recurring revenue items. Running out of stock causes client presses to halt, damaging OMPI's reputation.",
        "Dedicated inventory sub-system monitoring wear parts. Tracks stock by lining thickness, outer diameter, spline tooth count, and friction material formulation.",
        [
            ("Lining Wear Index", "Records wear rate data to predict when clients will require replacement friction disc sets."),
            ("Fast-Moving Spares Threshold", "Maintains safety stock buffers for top-selling friction disc sizes to ensure same-day dispatch.")
        ]
    ),
    (
        "MOD 20", "Serial Number & Heat Code Traceability", "Engine 3: Warehouse Operations", "Quality Control Inspectors",
        "If a client reports a clutch failure, OMPI must trace the unit back to its Italian manufacturing batch, casting heat code, and assembly test certificate to determine warranty validity.",
        "Maintains complete genealogy of every clutch assembly: Italian factory serial number, import Bill of Entry, client delivery date, and warranty registration.",
        [
            ("Laser-Etched Serial Registry", "Scans and indexes serial numbers during inward goods receipt at Pune warehouse."),
            ("Factory Test Certificate Linkage", "Attaches OMPI Italy hydraulic pressure and torque test reports to the serial number record.")
        ]
    ),
    (
        "MOD 21", "Inward Material Inspection (GRN Engine)", "Engine 3: Warehouse Operations", "Goods Inward QC Officers",
        "Imported sea cargo can suffer transit moisture damage, cracked castings, or missing components. Accepting damaged crates without inspection makes it impossible to claim marine insurance.",
        "Digital Goods Receipt Note (GRN) generator. Guides storekeepers through physical damage inspection, packing list verification against Italy PO, and quality quarantine tagging.",
        [
            ("Damage Reporting & Photographic Upload", "Captures photos of damaged wooden crates or rust spots to initiate insurance claims."),
            ("Quarantine Hold Workflow", "Prevents uninspected or damaged items from being allocated to customer sales orders.")
        ]
    ),
    (
        "MOD 22", "Outward Delivery Challan & Dispatch", "Engine 3: Warehouse Operations", "Dispatch Logistics In-Charge",
        "Moving high-value equipment without statutory documentation violates Indian GST Rule 48, risking vehicle impoundment and heavy fines by commercial tax officers.",
        "Generates statutory GST Delivery Challans (Form GST DRC-07) for moving clutches to client factories for trial, machining fitment, or warranty replacement.",
        [
            ("Statutory Challan Formatting", "Complies with GST rules: Displays serial numbers, HSN code, driver license, vehicle number, and purpose."),
            ("Serial Number Outward Binding", "Permanently binds dispatched serial numbers to the customer delivery challan record.")
        ]
    ),
    (
        "MOD 23", "Reconditioning & Service Center Ledger", "Engine 3: Warehouse Operations", "Workshop Technicians, Service Managers",
        "Many client units are returned to the Pune workshop for relining, new piston seals, and re-torque calibration. Tracking repair costs ensures service profitability.",
        "Logs maintenance workflows for returned clutches: Disassembly, inspection, ultrasonic cleaning, friction relining, seal kit installation, and static pressure recalibration.",
        [
            ("Repair Cost & Spares Ledger", "Tracks exact parts and technician labor hours consumed during reconditioning to generate service bills."),
            ("Recalibration Test Certificate", "Generates pressure test certificates certifying the reconditioned clutch is ready for factory service.")
        ]
    ),
    (
        "MOD 24", "Scrap & Dead Stock Management", "Engine 3: Warehouse Operations", "Finance Controllers, Plant Auditors",
        "Worn-out friction linings and damaged housings occupy valuable warehouse floor space and distort balance sheet valuations if not formally decommissioned.",
        "Governs segregation, valuation write-offs, and controlled disposal of worn-out friction plates, obsolete seal kits, and scrap castings.",
        [
            ("De-accessioning Workflow", "Requires multi-signature approval from Operations Manager and Finance Director before scrap write-off."),
            ("Scrap Sales Accounting", "Records scrap metal disposal weights and revenues in accordance with tax requirements.")
        ]
    ),
    (
        "MOD 25", "Automated Re-Order Alerts & Lead Time Engine", "Engine 3: Warehouse Operations", "Procurement Planners",
        "Sea shipments from Italy take 6–8 weeks. If re-orders are not placed before stock reaches minimum levels, the warehouse runs dry, causing lost sales.",
        "Calculates dynamic re-order points (ROP) based on average monthly consumption, safety buffer stock, and supplier lead times from Modena, Italy.",
        [
            ("Predictive ROP Calculation", "Formula: (Average Daily Usage x 60-day Lead Time) + Safety Stock buffer."),
            ("1-Click Italy Re-Order Draft", "Automatically consolidates depleted SKUs into a draft Purchase Order ready for review.")
        ]
    ),
    # Engine 4: Financial Ledger & Governance (26 to 33)
    (
        "MOD 26", "GST Tax Invoice Engine", "Engine 4: Financial Ledger", "Accounts Executives, Billing Heads",
        "Industrial machinery and spare parts require precise GST invoicing. Errors in GSTIN, SAC/HSN codes, or state tax splitting lead to client payment delays and audit penalties.",
        "Generates statutory B2B Tax Invoices with validated HSN codes (8483 for clutches, 8462 for presses), automatic CGST/SGST (18% intra-state) or IGST (18% inter-state) calculation, and QR code integration.",
        [
            ("Intra/Inter-State Tax Splitting", "Auto-detects buyer state from GSTIN: Splits 9% CGST + 9% SGST for Maharashtra or 18% IGST outside."),
            ("IRN & E-Invoice Integration", "Prepares data payloads for government E-Invoicing portal submission and invoice QR code printing."),
            ("Serial Number Invoicing", "Prints exact unit serial numbers on the invoice for foolproof manufacturer warranty enforcement.")
        ]
    ),
    (
        "MOD 27", "GSTR-1 Reconciliation Exporter", "Engine 4: Financial Ledger", "Chief Accountants, External Auditors",
        "Reconciling monthly sales manually for GST filing is time-consuming and error-prone. Mismatches between books and the GST portal trigger automatic scrutiny notices.",
        "Exports monthly sales data with one click into government GST Portal-compliant JSON and Excel formats matching Table 4A (B2B Sales), Table 9B (Credit/Debit Notes), and Table 12 (HSN Summary).",
        [
            ("GST Portal Compliant JSON Export", "Directly uploadable to the GSTN portal without manual re-keying or data conversion."),
            ("HSN Summary Reconciler", "Consolidates total quantities and taxable values per HSN code with zero mathematical variance.")
        ]
    ),
    (
        "MOD 28", "Accounts Receivable & Milestone Tracking", "Engine 4: Financial Ledger", "Credit Managers, Managing Director",
        "High-ticket deals operate on staged milestone payments. Failing to collect the 50% pre-dispatch payment before releasing a clutch causes severe cash flow blockages.",
        "Tracks customer payments against contractual milestones: 30% Advance with PO, 50% Proforma before dispatch, and 20% post-commissioning / 30-day trial.",
        [
            ("Milestone Payment Gate", "Locks warehouse dispatch documentation until the accounts module confirms receipt of the dispatch payment."),
            ("Bank UTR Reconciliation", "Matches electronic bank transfer reference numbers against outstanding invoice balances.")
        ]
    ),
    (
        "MOD 29", "Overdue Aging & Payment Reminder Hub", "Engine 4: Financial Ledger", "Recovery Officers, Commercial Executives",
        "Accounts receivable aging past 60 days in the manufacturing sector often turns into bad debt. Systematic follow-up ensures timely working capital rotation.",
        "Automated debtor aging matrix segregating receivables into 0–30, 31–60, 61–90, and 90+ day buckets. Generates standardized payment reminder letters and logs collection calls.",
        [
            ("Aging Bucket Visualization", "Interactive ledger showing total outstanding amounts color-coded by aging severity."),
            ("1-Click WhatsApp & Email Reminders", "Dispatches polite, firm payment reminder notices with invoice copy attached directly to client finance desks.")
        ]
    ),
    (
        "MOD 30", "Role-Based Access Control (RBAC)", "Engine 4: Governance & SecOps", "System Administrators, Managing Director",
        "Confidential Italian landed costs, customer profit margins, and financial balance sheets must not be visible to workshop staff, storekeepers, or junior sales engineers.",
        "Enforces granular Role-Based Access Control (RBAC) across 4 operational tiers: Managing Director (Full Access), Operations Manager (Stock & Dispatch), Sales Executive (Quotes only, cost hidden), and Storekeeper (Inventory receipts only).",
        [
            ("Granular Module Permissions", "Controls Create, Read, Update, Delete (CRUD) rights independently for every screen."),
            ("Cost Margin Masking", "Automatically masks Italian landed costs and gross profit percentages on junior staff screens.")
        ]
    ),
    (
        "MOD 31", "Immutable Security Audit Log", "Engine 4: Governance & SecOps", "Chief Technology Officers, Compliance Officers",
        "Unauthorized price discounts, inventory write-offs, or invoice alterations can cause severe revenue leakage if not permanently tracked.",
        "Tamper-proof, append-only security log recording every transaction: User ID, Timestamp, IP Address, Action Performed, and Before/After data values.",
        [
            ("Un-deletable Audit Database", "Audit logs are cryptographically sealed and cannot be modified or deleted even by system administrators."),
            ("Price Override Alerts", "Sends an immediate alert to Mr. Vinit Dalal whenever a sales quotation price is manually modified.")
        ]
    ),
    (
        "MOD 32", "On-Premise LAN Backup & Snapshot", "Engine 4: Governance & SecOps", "IT Operations Managers",
        "Hardware crashes or ransomware attacks on workshop computers can destroy years of critical inventory, serial number tracking, and financial history.",
        "Automated rolling backup engine. Executes daily encrypted database snapshots to local secondary SSD storage and exports encrypted cloud archive copies.",
        [
            ("Automated Nightly Backup Cron", "Executes zero-downtime database snapshots at midnight without interrupting daytime operations."),
            ("1-Click Disaster Recovery", "Enables full system restoration on new server hardware in under 15 minutes in case of hardware failure.")
        ]
    ),
    (
        "MOD 33", "Executive MIS & Analytics Dashboard", "Engine 4: Governance & SecOps", "Managing Director Mr. Vinit Dalal",
        "Leadership needs real-time business telemetry to make strategic decisions on capital allocation, Italy shipment volumes, and sales staffing.",
        "Executive business intelligence console: Monthly revenue growth, gross profit margins by machine type, sales rep performance, and inventory turnover ratios.",
        [
            ("Real-Time Gross Margin Analytics", "Visualizes actual gross profit earned after accounting for all customs duties, freight, and commissions."),
            ("Inventory Velocity Trends", "Identifies fast-moving clutch models versus slow-moving stock to optimize future Italy procurement.")
        ]
    )
]

# Let's write the HTML builder
with open('d:/st.ourhtmldemo.com/scratch/build_57_manual.py', 'w', encoding='utf-8') as f:
    f.write('''import os

from build_manual_data import html_start, dalal_routes_data, ompi_modules_data

body_parts = [html_start]

# PART 1: DALAL MACHINE TOOLS AGENCY (24 ROUTES)
body_parts.append("""
<div class="system-banner">
  <h2>SYSTEM 1: DALAL MACHINE TOOLS AGENCY WEB PLATFORM</h2>
  <span>ALL 24 CUSTOMER &amp; OPERATIONS ROUTES</span>
</div>
""")

for i, (rid, title, path, persona, why, what, features) in enumerate(dalal_routes_data, 1):
    feat_rows = ""
    for fname, fdesc in features:
        feat_rows += f"<li><strong>{fname}:</strong> {fdesc}</li>"
    
    card_html = f"""
<div class="unit-card avoid-break">
  <div class="unit-header">
    <div>
      <span class="unit-id">{rid}</span>
      <span class="unit-title">{title}</span>
      <span class="persona-badge">{persona}</span>
    </div>
    <span class="unit-route">{path}</span>
  </div>
  <div class="unit-grid">
    <div class="unit-box why">
      <div class="unit-box-title why-title">&#9658; Why It Exists (Business Purpose &amp; Rationale)</div>
      <p>{why}</p>
    </div>
    <div class="unit-box">
      <div class="unit-box-title what-title">&#9658; What It Does (Operational Mechanics)</div>
      <p>{what}</p>
    </div>
  </div>
  <div class="unit-features">
    <div class="unit-features-title">Core Functional Components &amp; Technical Tools:</div>
    <ul>
      {feat_rows}
    </ul>
  </div>
</div>
"""
    body_parts.append(card_html)
    if i in [3, 7, 11, 15, 19, 23]:
        body_parts.append('<div class="page-break"></div>')

body_parts.append('<div class="page-break"></div>')

# PART 2: OMPI INDIA LLP ERP (33 MODULES)
body_parts.append("""
<div class="system-banner" style="background:#1e3a8a;">
  <h2>SYSTEM 2: OMPI INDIA LLP INDUSTRIAL OPERATIONS &amp; ERP SUITE</h2>
  <span>ALL 33 MODULAR ENGINES &amp; SUBSYSTEMS</span>
</div>
""")

for j, (mid, title, engine, persona, why, what, features) in enumerate(ompi_modules_data, 1):
    feat_rows = ""
    for fname, fdesc in features:
        feat_rows += f"<li><strong>{fname}:</strong> {fdesc}</li>"
    
    card_html = f"""
<div class="unit-card avoid-break">
  <div class="unit-header">
    <div>
      <span class="unit-id" style="background:#1e3a8a;">{mid}</span>
      <span class="unit-title">{title}</span>
      <span class="persona-badge" style="color:#065f46; background:#ecfdf5; border-color:#a7f3d0;">{engine}</span>
      <span class="persona-badge">{persona}</span>
    </div>
    <span class="unit-route">ERP System Subsystem</span>
  </div>
  <div class="unit-grid">
    <div class="unit-box why">
      <div class="unit-box-title why-title">&#9658; Why It Exists (Business Purpose &amp; Rationale)</div>
      <p>{why}</p>
    </div>
    <div class="unit-box">
      <div class="unit-box-title what-title">&#9658; What It Does (Operational Mechanics)</div>
      <p>{what}</p>
    </div>
  </div>
  <div class="unit-features">
    <div class="unit-features-title">Core Sub-Modules, Algorithms &amp; Automation Features:</div>
    <ul>
      {feat_rows}
    </ul>
  </div>
</div>
"""
    body_parts.append(card_html)
    if j in [3, 7, 11, 15, 19, 23, 27, 31]:
        body_parts.append('<div class="page-break"></div>')

# PART 3: INTER-CONNECTIVITY & SUMMARY MATRIX
body_parts.append("""
<div class="page-break"></div>
<div class="system-banner" style="background:#0f172a;">
  <h2>COMPLETE SYSTEM MATRIX &amp; LIFECYCLE HANDSHAKE</h2>
  <span>CROSS-SYSTEM REAL-TIME INTEGRATION</span>
</div>

<div class="unit-card avoid-break">
  <p style="font-size:8.8pt; color:#334155; line-height:1.55; margin-bottom:12px;">
    The table below establishes the operational handshake between <strong>Dalal Machine Tools Agency</strong> (the inbound capital equipment acquisition engine) and <strong>OMPI India LLP</strong> (the precision engineering, landed costing, and lifecycle spares engine):
  </p>
  <table style="width:100%; border-collapse:collapse; font-size:8.2pt; border:1px solid #cbd5e1;">
    <thead>
      <tr style="background:#f1f5f9; color:#0f172a;">
        <th style="padding:8px 10px; border:1px solid #cbd5e1; text-align:left; width:15%;">Lifecycle Phase</th>
        <th style="padding:8px 10px; border:1px solid #cbd5e1; text-align:left; width:40%;">System 1: Dalal Machine Tools Web Platform</th>
        <th style="padding:8px 10px; border:1px solid #cbd5e1; text-align:left; width:40%;">System 2: OMPI India LLP Industrial ERP</th>
        <th style="padding:8px 10px; border:1px solid #cbd5e1; text-align:center; width:5%;">Sync</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td style="padding:6px 10px; border:1px solid #cbd5e1; font-weight:700;">1. Inbound Ingestion</td>
        <td style="padding:6px 10px; border:1px solid #cbd5e1;">Buyer inquires on <strong>Catalog (Route 04)</strong> or submits RFQ on <strong>Product Detail (Route 05)</strong> with exact press tonnage.</td>
        <td style="padding:6px 10px; border:1px solid #cbd5e1;">Inquiry auto-logged in <strong>RFQ Pipeline (Module 05)</strong>. System verifies customer GSTIN in <strong>Client Master (Module 01)</strong>.</td>
        <td style="padding:6px 10px; border:1px solid #cbd5e1; text-align:center; font-weight:700; color:#10b981;">&#10142;</td>
      </tr>
      <tr style="background:#f8fafc;">
        <td style="padding:6px 10px; border:1px solid #cbd5e1; font-weight:700;">2. Technical Sizing</td>
        <td style="padding:6px 10px; border:1px solid #cbd5e1;">Buyer verifies physical stockyard ground readiness in Pune via <strong>Live Radar Indicators</strong>.</td>
        <td style="padding:6px 10px; border:1px solid #cbd5e1;">Engineer inputs flywheel RPM &amp; air pressure into <strong>Torque Sizing Calculator (Module 16)</strong>; outputs certified OMPI model.</td>
        <td style="padding:6px 10px; border:1px solid #cbd5e1; text-align:center; font-weight:700; color:#10b981;">&#10142;</td>
      </tr>
      <tr>
        <td style="padding:6px 10px; border:1px solid #cbd5e1; font-weight:700;">3. Costing &amp; Quote</td>
        <td style="padding:6px 10px; border:1px solid #cbd5e1;">Dalal staff uses <strong>Lead Triage Console (Route 07)</strong> to fire instant WhatsApp technical proposal.</td>
        <td style="padding:6px 10px; border:1px solid #cbd5e1;"><strong>Landed Cost Engine (Module 13)</strong> checks EUR exchange rate; <strong>Fast-Quote (Module 04)</strong> issues formal branded PDF.</td>
        <td style="padding:6px 10px; border:1px solid #cbd5e1; text-align:center; font-weight:700; color:#10b981;">&#10142;</td>
      </tr>
      <tr style="background:#f8fafc;">
        <td style="padding:6px 10px; border:1px solid #cbd5e1; font-weight:700;">4. Inventory Lock</td>
        <td style="padding:6px 10px; border:1px solid #cbd5e1;">Machine marked as "Under Commercial Hold" in public catalog.</td>
        <td style="padding:6px 10px; border:1px solid #cbd5e1;"><strong>Serial Registry (Module 20)</strong> reserves laser-etched clutch unit in <strong>Warehouse Bin Ledger (Module 18)</strong>.</td>
        <td style="padding:6px 10px; border:1px solid #cbd5e1; text-align:center; font-weight:700; color:#10b981;">&#10142;</td>
      </tr>
      <tr>
        <td style="padding:6px 10px; border:1px solid #cbd5e1; font-weight:700;">5. Field Retrofit</td>
        <td style="padding:6px 10px; border:1px solid #cbd5e1;">Client accesses <strong>Services Portal (Route 03)</strong> to review crankshaft boring &amp; foundation milestones.</td>
        <td style="padding:6px 10px; border:1px solid #cbd5e1;">Service engineer executes <strong>5-Stage Job Card (Module 23)</strong>, logging runout gauge readings (&lt;0.05mm) with photos.</td>
        <td style="padding:6px 10px; border:1px solid #cbd5e1; text-align:center; font-weight:700; color:#10b981;">&#10142;</td>
      </tr>
      <tr style="background:#f8fafc;">
        <td style="padding:6px 10px; border:1px solid #cbd5e1; font-weight:700;">6. Invoicing &amp; AMC</td>
        <td style="padding:6px 10px; border:1px solid #cbd5e1;">Machine marked "Sold"; installation photo added to <strong>Shipment Archive (Route 07)</strong>.</td>
        <td style="padding:6px 10px; border:1px solid #cbd5e1;"><strong>Invoice Engine (Module 26)</strong> issues B2B Tax Invoice; <strong>GSTR-1 (Module 27)</strong> reconciles; <strong>AMC (Module 29)</strong> initiates recurring spares cycle.</td>
        <td style="padding:6px 10px; border:1px solid #cbd5e1; text-align:center; font-weight:700; color:#10b981;">&#10004;</td>
      </tr>
    </tbody>
  </table>
</div>

<div class="footer-note">
  <div><strong>Dalal Machine Tools Agency Pvt. Ltd. &amp; OMPI India LLP</strong> &bull; Complete Systems, Pages &amp; Modular Architecture Manual</div>
  <div>Architect: Suyash Shinde &bull; Pimpri, Pune &bull; +91 96070 28594</div>
</div>

</body>
</html>
""")

final_html = "".join(body_parts)
out_path = 'd:/st.ourhtmldemo.com/DALAL_AND_OMPI_57_PAGES_AND_MODULES_MASTER_SPECIFICATION.html'
with open(out_path, 'w', encoding='utf-8') as f:
    f.write(final_html)
print(f"Generated {out_path} successfully!")
''')
print("Wrote scratch/build_57_manual.py")

