# scratch/build_balanced_master_spec.py
"""
Elite Enterprise Master Specification Generator
Produces 32-Page Balanced, Highly Professional, Non-Technical Master Proposal.
- Exactly 32 Pages (A4)
- 100% Plain Business English (Zero developer jargon)
- Framed strictly as 'Pre-Commencement Scope Proposal' (Work has not yet started)
- Strict confidentiality notices on every page
- Beautiful card layout with 3 tangible deliverables per card
- Perfectly fills every A4 page from top to bottom (ZERO awkward blank white voids!)
"""

import os, sys, subprocess, shutil, pymupdf

print("Starting generation of 32-page balanced master specification...")

# 24 Dalal Machinery Routes
dalal_routes = [
    # Page 2
    {
        "id": "ROUTE-01",
        "title": "Homepage & Machinery Showroom",
        "path": "Planned Route: /index.html",
        "audience": "Industrial Plant Owners, Factory Directors, Forging Sourcing Heads",
        "focus": "High-Value Machine Sizing, Yard Authenticity & Instant Trust",
        "does": "A modern digital machinery showroom presenting heavy forging and stamping presses available for sale. Customers will see clear high-resolution photographs, verified machine tonnages, live video power trials, and a direct WhatsApp button to speak directly with Mr. Vinit Dalal. Eliminates buyer hesitation before calling.",
        "benefit": "Eliminates buyer skepticism. Factory owners see that machines are physically present in the Pune stockyard (not fake broker listings), establishing instant trust for deals from Rs. 50 Lakh to Rs. 4 Crore. Protects corporate brand credibility against unauthorized market brokers.",
        "deliverables": ["Live Power Inspection Videos", "Direct WhatsApp Sizing RFQ", "Pune Yard Physical Verification"],
        "feature": "1-Click WhatsApp inquiry button pre-filled with the exact machine model, capacity, and Pune warehouse stock status."
    },
    {
        "id": "ROUTE-02",
        "title": "Company Heritage & Facility Dossier",
        "path": "Planned Route: /about.html",
        "audience": "Corporate Procurement Heads, Bank Valuers, Joint-Venture Partners",
        "focus": "50-Year Engineering Heritage & Official Italian Partnership",
        "does": "Presents the 50-year engineering heritage of the Dalal family, authentic photos of the Mumbai registered corporate office and Pune warehouse stockyard, and formal details of the official technical partnership with OMPI Italy. Proves company stability and capability to corporate buyers.",
        "benefit": "Proves corporate legitimacy and financial stability, assuring plant owners that their advance payments and multi-crore machinery orders are in trustworthy, experienced hands. Protects brand equity and qualifies corporate vendor registrations with Tier-1 auto manufacturers.",
        "deliverables": ["50-Year Heritage Timeline", "Pune Yard Facility Tour", "OMPI Italy Partnership Certificate"],
        "feature": "Visual timeline highlighting 5 decades of heavy machinery supply across India with official Italian engineering certification."
    },
    # Page 3
    {
        "id": "ROUTE-03",
        "title": "Import, Rigging & Engineering Services",
        "path": "Planned Route: /services.html",
        "audience": "Plant Maintenance Heads, Factory Engineers, Project Directors",
        "focus": "Turnkey Heavy Rigging, Customs Clearance & Foundation Works",
        "does": "A comprehensive, easy-to-follow guide explaining Dalal's turnkey technical services: overseas machine dismantling in Europe, customs clearance at Nhava Sheva port, heavy transport on 64-wheel hydraulic trailers, foundation pit engineering, and Italian pneumatic clutch retrofitting.",
        "benefit": "Proves that Dalal is a full-service machinery solutions partner rather than just an equipment trader. Assures factory owners that the heavy press will be safely transported, professionally erected, and successfully tested under full electrical power on their shop floor.",
        "deliverables": ["Nhava Sheva Customs Clearance Guide", "Heavy Transport Hydraulic Trailer Logistics", "Turnkey Civil Foundation Blueprints"],
        "feature": "Clear 7-point FAQ explaining how High Seas Sales save time and customs duty, backed by expert technical advice."
    },
    {
        "id": "ROUTE-04",
        "title": "Machinery Catalog & Search Directory",
        "path": "Planned Route: /category.html",
        "audience": "Factory Sourcing Managers, Purchase Officers, Plant Sizing Teams",
        "focus": "26 Machine Categories with Instant Tonnage & Brand Filtering",
        "does": "A clean, searchable directory of all 26 machine types (Mechanical Forging Presses, Hydraulic Stamping Presses, Friction Screw Presses, Horizontal Boring Machines) equipped with instant tonnage filters, manufacturer filters (Russia, Germany, Japan), and Pune stock filters.",
        "benefit": "Allows busy factory purchase officers to locate the exact tonnage, bed dimensions, and machine type they need in under 10 seconds, eliminating frustrating telephone delays and preventing potential buyers from leaving for competitors.",
        "deliverables": ["Instant Tonnage Range Filtering", "Country of Make Categorization", "Pune Godown Ready-Stock Locator"],
        "feature": "Interactive tonnage sliders (Under 500T, 500T-1000T, 1000T-4000T) with real-time stock availability updates."
    },
    # Page 4
    {
        "id": "ROUTE-05",
        "title": "Machine Technical Details Sheet (PDP)",
        "path": "Planned Route: /product.html",
        "audience": "Chief Technical Officers, Toolroom Managers, Plant Heads",
        "focus": "Full Dimensional Specifications, Die Clearance & Video Proof",
        "does": "A comprehensive technical sheet for every press: tonnage, stroke, bed dimensions, motor HP, country of make, civil foundation needs, power trial video, and a 1-click button to download an official formal quotation.",
        "benefit": "Gives plant technical heads every measurement to confirm the press fits their tooling dies and factory ceiling, accelerating capital budget approvals from the board.",
        "deliverables": ["High-Definition Die Clearance Schematics", "Live Motor Running & Ram Cycling Video", "1-Click PDF Machine Quotation Download"],
        "feature": "Instant A4 technical spec sheet download with official Dalal branding, ready for internal executive committee presentation."
    },
    {
        "id": "ROUTE-06",
        "title": "Brand New Factory Machinery Lines",
        "path": "Planned Route: /brand-new-machinery.html",
        "audience": "Tier-1 Automotive Suppliers, High-Volume Manufacturing Plants",
        "focus": "Factory-Fresh Production Lines with European Warranty",
        "does": "A dedicated showcase of brand-new heavy industrial presses engineered to European safety standards, with manufacturer warranty, touch automation, and factory commissioning.",
        "benefit": "Captures top-tier automotive suppliers whose internal policies prohibit buying used equipment, opening high-margin contracts for brand-new machinery.",
        "deliverables": ["European CE Safety Certification Details", "Multi-Year Factory Warranty Terms", "Turnkey Automated Production Line Sizing"],
        "feature": "Direct RFQ inquiry system for custom-engineered new production lines tailored to exact automotive stamping specifications."
    },
    # Page 5
    {
        "id": "ROUTE-07",
        "title": "Shipment, Yard & Rigging Photo Gallery",
        "path": "Planned Route: /gallery.html",
        "audience": "Factory Auditors, Sourcing Committees, Managing Directors",
        "focus": "Visual Proof of 4,000-Ton Rigging & Stockyard Scale",
        "does": "A high-impact photographic and video gallery showcasing heavy 1,000-ton to 4,000-ton forging presses being hoisted by 250-ton hydraulic cranes, secured onto multi-axle trailers, cleared at Indian ports, and installed inside customer forging facilities.",
        "benefit": "Provides undeniable visual proof of heavy engineering capability. Seeing real photographs of massive equipment handling completely eliminates buyer anxiety regarding Dalal's ability to safely deliver giant industrial machinery.",
        "deliverables": ["Port Hoisting & Crane Operation Photos", "64-Wheel Trailer Transit Documentation", "Customer Plant Installation Case Studies"],
        "feature": "Filterable gallery sorted by press tonnage, equipment manufacturer, and heavy rigging stage."
    },
    {
        "id": "ROUTE-08",
        "title": "Headquarters, Yard & Direct RFQ Portal",
        "path": "Planned Route: /contact.html",
        "audience": "Procurement Directors, Visiting Engineering Teams",
        "focus": "Direct Executive Access & Pune Yard Trial Scheduling",
        "does": "Interactive Google Map location guides for both the Mumbai Registered Corporate Office (Tardeo) and the Pune Heavy Warehouse Stockyard (Chakan), complete with direct telephone lines, executive emails, and an online appointment booking console.",
        "benefit": "Makes it effortless for serious corporate buyers to schedule an in-person physical inspection in Pune and witness the machine operating under live electric power prior to releasing substantial commercial advance payments.",
        "deliverables": ["Interactive Map to Mumbai & Pune Facilities", "Live Power Trial Appointment Booking", "Direct Director Telephone & Email Access"],
        "feature": "Direct visit booking console allowing plant engineers to reserve a dedicated 2-hour technical power trial in Pune."
    },
    # Page 6
    {
        "id": "ROUTE-09",
        "title": "Express Breakdown RFQ Console",
        "path": "Planned Route: /contact-2.html",
        "audience": "Plant Managers facing an urgent machine breakdown",
        "focus": "Emergency Machine Sizing & Rapid Replacement Dispatch",
        "does": "An emergency request console asking only 3 essential questions: required press tonnage, bed size, and delivery urgency. Specifically optimized for mobile phones so a factory manager on the shop floor can submit an urgent inquiry in 30 seconds.",
        "benefit": "Captures critical emergency replacement leads when a competitor's press has cracked its frame or suffered catastrophic clutch failure, enabling Dalal to close fast, high-margin machinery deals from existing Pune stock.",
        "deliverables": ["30-Second Mobile-Friendly Request Form", "Instant Priority Alert to Director WhatsApp", "Guaranteed 2-Hour Stock Availability Response"],
        "feature": "Automated high-priority alert routed directly to the Managing Director's personal phone for instant emergency response."
    },
    {
        "id": "ROUTE-10",
        "title": "Import Compliance & Legal FAQs Guide",
        "path": "Planned Route: /faqs.html",
        "audience": "Chief Financial Officers (CFOs), Company Legal & Tax Advisors",
        "focus": "High Seas Sales Law, Customs Bill of Entry & 100% GST Credit",
        "does": "Clear, plain-English legal explanations of High Seas Sales contracts, 100% GST input tax credit (ITC) claims, Customs Bill of Entry procedures, and live power inspection trials, answering every commercial question CFOs ask.",
        "benefit": "Removes legal and taxation hesitation from company accountants, providing clear documentation that speeds up corporate board approvals and saves the client up to 10% on customs clearance duties.",
        "deliverables": ["High Seas Sales Legal Procedure Explainer", "Step-by-Step GST Input Tax Credit Guide", "Chartered Engineer Valuation Inspection FAQ"],
        "feature": "Interactive accordion explaining tax documentation, customs procedures, and warranty terms without confusing legal jargon."
    },
    # Page 7
    {
        "id": "ROUTE-11",
        "title": "Customer Quotation Download Portal",
        "path": "Planned Route: /quotation.html",
        "audience": "Procurement Heads, Commercial Executives, Factory Accountants",
        "focus": "Secure PDF Proposal Retrieval with Official Terms",
        "does": "A secure digital portal where prospective buyers can review and download their personalized formal commercial quotation letters, complete with machine photographs, technical tolerances, payment terms, and official Dalal signatures.",
        "benefit": "Eliminates delays caused by lost email attachments and ensures corporate purchase committees review the authentic, officially authorized quotation, preventing pricing miscommunications.",
        "deliverables": ["Authorized Quotation PDF Retrieval", "Complete Commercial Payment Milestones", "Machine Technical Dimensional Blueprints"],
        "feature": "Secure document retrieval with automatic email confirmation and direct WhatsApp proposal delivery."
    },
    {
        "id": "ROUTE-12",
        "title": "Power Trial Video Showcase Center",
        "path": "Planned Route: /video-trials.html",
        "audience": "Plant Technical Directors, Maintenance Heads, Chief Engineers",
        "focus": "Live Electrical Load Trials, Ram Cycling & Flywheel Tests",
        "does": "A dedicated video library presenting unedited, high-definition videos of heavy forging and mechanical presses undergoing live electric power trials at the Pune yard, showing smooth flywheel rotation, clutch engagement, and ram cycling.",
        "benefit": "Provides conclusive technical verification that machines are in excellent mechanical health, saving out-of-state buyers from Gujarat, Tamil Nadu, and Punjab the time and expense of an in-person journey before making an offer.",
        "deliverables": ["High-Definition Unedited Trial Footage", "Sound & Vibration Analysis Visuals", "Clutch-Brake Instant Stopping Verification"],
        "feature": "Categorized video player with searchable machine models, tonnages, and test dates."
    },
    # Page 8
    {
        "id": "ROUTE-13",
        "title": "Machinery Comparison & Sizing Tool",
        "path": "Planned Route: /compare.html",
        "audience": "Toolroom Heads, Production Planners, Industrial Engineers",
        "focus": "Side-by-Side Sizing of Bed Size, Stroke & Tonnage",
        "does": "An intuitive side-by-side comparison screen allowing plant engineers to compare up to 3 machines simultaneously on critical engineering factors: pressing tonnage, stroke length, bolster dimensions, motor power, and pricing.",
        "benefit": "Empowers factory engineers to make informed technical sizing decisions, ensuring they invest in the exact press model that matches their automotive forging dies and production volume requirements.",
        "deliverables": ["Side-by-Side Technical Comparison Grid", "Die Compatibility Dimensional Matcher", "1-Click Comparison Export to PDF"],
        "feature": "Interactive side-by-side spec comparison highlighting key differences in die space, speed, and tonnage."
    },
    {
        "id": "ROUTE-14",
        "title": "Used Press Valuation & Buyback Request",
        "path": "Planned Route: /sell-machine.html",
        "audience": "Factory Owners Upgrading Plants, Liquidators, Plant Heads",
        "focus": "Surplus Machine Liquidation & Fair Market Cash Offers",
        "does": "A streamlined valuation portal where manufacturing plants looking to sell or trade in surplus heavy presses can submit machine specifications, photographs, nameplate details, and asking prices directly to Dalal's acquisition team.",
        "benefit": "Builds a continuous proprietary pipeline of high-quality machinery acquisitions across India, enabling Dalal to buy presses below market value directly from plant owners before competitors even learn they are for sale.",
        "deliverables": ["Simple Machine Photo & Nameplate Uploader", "Instant Valuation Preliminary Assessment", "Fair Market Cash Offer or Trade-in Credit"],
        "feature": "Structured submission form collecting essential press details (make, year, tonnage, operational condition) in 2 minutes."
    },
    # Page 9
    {
        "id": "ROUTE-15",
        "title": "Press Tonnage & Sizing Calculator",
        "path": "Planned Route: /calculator.html",
        "audience": "Manufacturing Sourcing Teams, New Plant Setup Heads",
        "focus": "Automated Tonnage Estimation from Component Dimensions",
        "does": "A simple interactive calculator where plant engineers enter their forged component dimensions, material type (steel, brass, aluminum), and production process to immediately calculate the recommended press tonnage.",
        "benefit": "Educates prospective clients and positions Dalal as the premier technical authority in the industry, guiding buyers to inquire about the exact machine capacity they truly need and reducing quotation revisions.",
        "deliverables": ["Instant Forging Force Requirement Formula", "Recommended Press Models in Stock", "Direct WhatsApp Sizing Consultation"],
        "feature": "Interactive formula that suggests suitable in-stock machines based on calculated tonnage requirements."
    },
    {
        "id": "ROUTE-16",
        "title": "High Seas Sales Compliance Center",
        "path": "Planned Route: /high-seas.html",
        "audience": "Corporate CFOs, Commercial Directors, Tax Consultants",
        "focus": "Legal Documentation, Port Handling & Customs Clearance",
        "does": "A transparent documentation center detailing the exact legal workflow for High Seas Sales agreements, including transfer of title before Indian customs frontiers, customs documentation, Bill of Lading endorsements, and port clearance.",
        "benefit": "Demystifies the import process for first-time machinery importers, giving corporate legal and tax teams the confidence that all transactions strictly adhere to Indian Customs and GST regulations.",
        "deliverables": ["Sample High Seas Sales Agreement Template", "Nhava Sheva Port Clearance Timeline", "Customs Duty Optimization Checklist"],
        "feature": "Downloadable legal procedure guide and document checklist approved by maritime trade counsel."
    },
    # Page 10
    {
        "id": "ROUTE-17",
        "title": "Pune Warehouse Live Stockyard Camera",
        "path": "Planned Route: /live-yard.html",
        "audience": "Prospective Buyers, Out-of-State Clients, Corporate Committees",
        "focus": "Real-Time Yard Visibility & Physical Stock Verification",
        "does": "A secure portal offering authorized clients scheduled live video access to view the Pune stockyard in real time, inspect machinery rows, and observe workshop cranes operating on heavy equipment.",
        "benefit": "Provides ultimate transparency, completely separating Dalal from internet brokers who list machinery they do not own. Demonstrates massive physical capital and builds unmatched credibility.",
        "deliverables": ["Scheduled Live Video Stream Access", "Yard Inventory Layout Map", "Instant Guided Virtual Inspection"],
        "feature": "Secure time-limited viewing tokens for serious buyers to inspect machines remotely with a live yard engineer."
    },
    {
        "id": "ROUTE-18",
        "title": "Client Delivery & Installation Track Record",
        "path": "Planned Route: /track-record.html",
        "audience": "Board-Level Decision Makers, Foreign Joint Ventures",
        "focus": "500+ Successful Press Deliveries Across India",
        "does": "An executive portfolio showcasing major heavy machine deliveries completed for prominent automotive forge plants, railway component suppliers, and defense contractors across Pune, Rajkot, Chennai, and Jamshedpur.",
        "benefit": "Leverages powerful social proof and industry references to win major corporate contracts, reassuring enterprise risk committees that Dalal has successfully executed hundreds of multi-crore machinery installations.",
        "deliverables": ["Verified Automotive Tier-1 Case Studies", "Client Testimonial Letters & Commendations", "Geographic Delivery Map Covering All India"],
        "feature": "Interactive delivery map highlighting machines installed across major industrial manufacturing hubs in India."
    },
    # Page 11
    {
        "id": "ROUTE-19",
        "title": "Machinery Spare Parts & Accessories Center",
        "path": "Planned Route: /spare-parts.html",
        "audience": "Maintenance Engineers, Plant Storekeepers, Purchase Teams",
        "focus": "Original Italian Clutches, Rotating Unions & Friction Discs",
        "does": "A dedicated catalog of essential replacement components: genuine Italian OMPI pneumatic clutch-brakes, rotating unions, friction linings, counterbalance seals, and hydraulic overload seals.",
        "benefit": "Generates recurring, high-margin aftermarket revenue from the existing installed base of machinery in India, while guaranteeing Dalal's machine buyers that replacement wear parts are always in stock in Pune.",
        "deliverables": ["Genuine OMPI Italian Spare Parts Directory", "Dimensional Cross-Reference Guide", "Express Same-Day Dispatch from Pune Godown"],
        "feature": "Quick SKU search matching machine make and clutch bore size with immediate dispatch availability."
    },
    {
        "id": "ROUTE-20",
        "title": "European Machinery Sourcing Hotline",
        "path": "Planned Route: /sourcing.html",
        "audience": "Industrialists seeking specific foreign machinery models",
        "focus": "Custom Sourcing from Germany, Italy & Eastern Europe",
        "does": "A specialized custom sourcing desk where clients can request specific heavy equipment not currently in Indian stock (e.g., 2,500T Eumuco wedge press, 4,000T Voronezh press, or Schuler transfer line) from European partners.",
        "benefit": "Enables Dalal to broker and import multi-crore machinery packages without committing working capital up front, earning substantial consulting and trade commissions.",
        "deliverables": ["Direct Access to European Plant Liquidations", "Overseas On-Site Technical Inspection Report", "Complete Import & Logistics Cost Projection"],
        "feature": "Dedicated sourcing request form with guaranteed 48-hour preliminary search across European machinery yards."
    },
    # Page 12
    {
        "id": "ROUTE-21",
        "title": "Custom Press Modernization & Rebuilding",
        "path": "Planned Route: /modernization.html",
        "audience": "Factory Owners seeking to boost production on older presses",
        "focus": "Clutch Retrofits, PLC Automation & Safety Upgrades",
        "does": "An engineering showcase explaining how Dalal transforms slow, outdated mechanical rolling-key presses into high-speed, modern production lines by retrofitting Italian OMPI pneumatic clutch-brakes and modern electrical safety controls.",
        "benefit": "Opens high-margin modernization contracts for factory owners who cannot afford to buy new machinery but desperately need to comply with factory inspector safety standards and increase production output.",
        "deliverables": ["Pneumatic Clutch Conversion Engineering Plan", "Dual-Hand Safety Control & Light Curtain Specs", "Production Output & Speed Improvement Metrics"],
        "feature": "Before-and-after modernization case studies with certified productivity increase data."
    },
    {
        "id": "ROUTE-22",
        "title": "Annual Maintenance & Support Contracts (AMC)",
        "path": "Planned Route: /maintenance.html",
        "audience": "Plant Maintenance Managers, Operations Directors",
        "focus": "Preventative Maintenance, Clutch Audits & Emergency Visits",
        "does": "A clear presentation of Dalal's annual maintenance programs, including scheduled quarterly pneumatic clutch inspections, flywheel bearing checks, hydraulic pressure audits, and priority emergency breakdown callouts.",
        "benefit": "Converts one-time machinery buyers into long-term retainer clients, smoothing out cash flow with predictable recurring annual maintenance revenue and ensuring customer machinery runs without breakdowns.",
        "deliverables": ["Quarterly 40-Point Press Inspection Schedule", "Priority 24-Hour Emergency Breakdown Dispatch", "Discounted Spare Parts & Consumables Schedule"],
        "feature": "Service contract selector allowing clients to choose Bronze, Silver, or Gold maintenance coverage."
    },
    # Page 13
    {
        "id": "ROUTE-23",
        "title": "Staff Inventory Administration Console",
        "path": "Planned Route: /admin/products.html",
        "audience": "Dalal Inventory Managers, Commercial Officers",
        "focus": "Internal Stock Management, Technical Specs & Pricing",
        "does": "A secure internal staff portal allowing Dalal's operations team to add new presses to the website, update machine pricing, upload fresh power trial videos, mark machines as 'Under Commercial Hold', and manage specifications.",
        "benefit": "Eliminates the need for external website developers for everyday operations. Your team can list a newly arrived machine in 3 minutes from a phone or laptop, making it immediately visible to buyers across India.",
        "deliverables": ["3-Minute Machine Listing & Photo Uploader", "Instant Commercial Hold & Sold Status Toggle", "Internal Cost vs. Selling Price Margin Calculator"],
        "feature": "Role-secured administrative dashboard with instant synchronization across public catalog and WhatsApp buttons."
    },
    {
        "id": "ROUTE-24",
        "title": "Customer RFQ & Quotation Inbox Console",
        "path": "Planned Route: /admin/inquiries.html",
        "audience": "Sales Team, Managing Director, Commercial Head",
        "focus": "Lead Tracking, AI Lead Scoring & Proposal Dispatch",
        "does": "A centralized operational inbox capturing all incoming customer inquiries from the website, WhatsApp, and email, displaying customer factory name, machine required, delivery urgency, and quotation history.",
        "benefit": "Ensures zero lost customer leads. Every inquiry is tracked until closed, enabling management to monitor sales representative follow-ups, speed up quotation response times, and dramatically increase deal closing rates.",
        "deliverables": ["Centralized Inquiry Feed with Status Tracking", "1-Click WhatsApp Lead Chat Initialization", "Instant Customer Proposal History & Notes"],
        "feature": "Color-coded lead cards with automated follow-up reminders and direct quotation generator."
    }
]

# 33 OMPI Industrial Operations Modules
ompi_modules = [
    # Page 15
    {
        "id": "ERP-MOD-01",
        "title": "Client Records & GST Credit Master",
        "engine": "Engine 1: Sales & Customer Pipeline",
        "role": "Sales Executives, Accounts Manager",
        "focus": "Centralized Customer Directory & Tax Compliance",
        "does": "Maintains a central profile for every client factory: verified 15-digit GSTIN, multiple delivery godown addresses, authorized purchase managers, and approved commercial credit limits. Updates in real time.",
        "benefit": "Stops costly billing errors, prevents dispatching valuable goods to companies with overdue payments, and ensures tax invoices strictly match GST portal records to prevent input tax credit disputes.",
        "deliverables": ["Real-Time 15-Digit GSTIN Portal Verification", "Multi-Godown Delivery Address Registry", "Automated Commercial Credit Limit Lockout"],
        "feature": "Automated GST number verification and real-time company ledger outstanding summary."
    },
    {
        "id": "ERP-MOD-02",
        "title": "OMPI Technical Catalog & SKU Master",
        "engine": "Engine 1: Sales & Customer Pipeline",
        "role": "Technical Sales Engineers",
        "focus": "Italian Clutch-Brake Specifications & Sizing",
        "does": "Organizes all Italian pneumatic clutch-brakes, rotating unions, and friction discs by bore size, torque capacity, operating air pressure, and manufacturer dimensional cross-references. Instant search.",
        "benefit": "Allows sales representatives to identify the exact replacement clutch model in 10 seconds without searching through heavy Italian paper catalogs, providing instant answers to clients.",
        "deliverables": ["Complete Italian OMPI Engineering Database", "Bore Size & Torque Capacity Cross-Index", "Alternative Model & Replacement Sizing Matrix"],
        "feature": "Quick lookup connecting machine brand names (Aida, Schuler, Godrej) with suitable OMPI clutch models."
    },
    # Page 16
    {
        "id": "ERP-MOD-03",
        "title": "Import Currency & Landed Pricing Engine",
        "engine": "Engine 1: Sales & Customer Pipeline",
        "role": "Commercial Manager, Managing Director",
        "focus": "Euro/INR Exchange Rate & Duty Surcharge Calculation",
        "does": "Calculates selling prices in Indian Rupees based on live Euro exchange rates, ocean shipping costs, customs duty percentages, port clearance fees, and minimum profit margins required by management.",
        "benefit": "Protects company profits against sudden currency fluctuations between the Euro and Rupee during the 4 to 8 weeks of ocean shipping, ensuring quotes remain profitable under all market conditions.",
        "deliverables": ["Automated Euro to INR Exchange Rate Converter", "Port Surcharge & Customs Duty Multiplier", "Minimum Gross Margin Threshold Protection"],
        "feature": "Automated price calculation incorporating daily exchange rates and port handling fees."
    },
    {
        "id": "ERP-MOD-04",
        "title": "Fast-Quote 60-Second PDF Generator",
        "engine": "Engine 1: Sales & Customer Pipeline",
        "role": "Sales Representatives, Commercial Staff",
        "focus": "Instant Branded Quotations & WhatsApp Dispatch",
        "does": "Compiles professional, branded quotation letters complete with machine photos, technical dimensions, prices, and payment terms in under 60 seconds, ready for immediate dispatch.",
        "benefit": "Allows your sales team to deliver an official proposal while the customer is still on the telephone, beating competitors who take 2 to 3 days to send a quote and capturing early buyer commitment.",
        "deliverables": ["1-Click Professional A4 PDF Proposal Generator", "Pre-Configured Payment Terms & Validity Dates", "Automated WhatsApp & Email Dispatch System"],
        "feature": "1-click generation of print-ready A4 PDF proposals with official company signature."
    },
    # Page 17
    {
        "id": "ERP-MOD-05",
        "title": "Customer Inquiry Visual Pipeline",
        "engine": "Engine 1: Sales & Customer Pipeline",
        "role": "Sales Team, Managing Director",
        "focus": "Visual Deal Progression from Lead to Payment",
        "does": "Displays all incoming customer inquiries on a visual stage board: New Lead, Quoted, Power Trial Scheduled, Price Negotiation, Commercial Hold, and Deal Closed. Drag-and-drop simplicity.",
        "benefit": "Gives the Managing Director complete visibility over every active deal so no high-value inquiry is forgotten or neglected by sales staff, directly increasing deal closure percentages.",
        "deliverables": ["Visual Kanban Deal Pipeline Board", "Stalled Lead Alerts & Stagnation Warnings", "Sales Rep Deal Assignment & Ownership"],
        "feature": "Visual stage cards with color-coded alerts for inquiries that have not been followed up in 48 hours."
    },
    {
        "id": "ERP-MOD-06",
        "title": "Press & Clutch Compatibility Matrix",
        "engine": "Engine 1: Sales & Customer Pipeline",
        "role": "Technical Sourcing Engineers",
        "focus": "Historical Press Model Sizing & Engineering Match",
        "does": "Cross-indexes leading press makes (Aida, Schuler, Godrej, Voronezh, Li Chin) with the correct OMPI clutch model, flywheel mounting dimensions, and required operating air pressure.",
        "benefit": "Enables sales reps to confidently advise plant owners on the exact clutch retrofit needed for their machine without waiting for engineering consultations, building immediate customer confidence.",
        "deliverables": ["Automated Machinery Make-to-Clutch Matcher", "Flywheel Bore & Mounting Clearance Charts", "Operating Air Pressure & Torque Recommendations"],
        "feature": "Pre-configured compatibility lookup providing accurate recommendations in 5 seconds."
    },
    # Page 18
    {
        "id": "ERP-MOD-07",
        "title": "Pune Godown Live Stock Tracker",
        "engine": "Engine 2: Inventory & Warehouse Master",
        "role": "Godown Storekeeper, Operations Head",
        "focus": "Real-Time Stock Counts, Reservations & Location",
        "does": "Tracks every clutch, friction disc, and heavy press physically present in the Pune warehouse, including exact godown shelf location, arrival date, condition, and commercial reservation status.",
        "benefit": "Prevents the embarrassing commercial disaster of promising a clutch or machine to a client when it was already sold or reserved by another sales representative earlier that morning.",
        "deliverables": ["Real-Time Physical vs Available Stock Counts", "Temporary Customer Commercial Reservation Lock", "Bin Location & Shelf Mapping for Rapid Dispatch"],
        "feature": "Real-time stock reservation lock preventing double-selling of in-demand inventory."
    },
    {
        "id": "ERP-MOD-08",
        "title": "High-Seas In-Transit Shipment Tracker",
        "engine": "Engine 2: Inventory & Warehouse Master",
        "role": "Logistics Officer, Commercial Manager",
        "focus": "Container Tracking from Genoa to Nhava Sheva",
        "does": "Monitors shipping containers from the moment they depart Italy or European ports, tracking vessel names, estimated arrival at Nhava Sheva (JNPT), and customs clearance progress.",
        "benefit": "Enables accurate delivery promises to clients awaiting imported machinery and prevents expensive port demurrage penalties by preparing customs clearance documentation well before vessel berthing.",
        "deliverables": ["Container Tracking & ETA Milestone Alerts", "Port Clearance Documentation Status Tracker", "Pre-Arrival Customer Delivery Scheduling"],
        "feature": "Automated countdown tracking container vessel arrival dates and customs clearance deadlines."
    },
    # Page 19
    {
        "id": "ERP-MOD-09",
        "title": "Automated Re-Order Alert Engine",
        "engine": "Engine 2: Inventory & Warehouse Master",
        "role": "Purchasing Manager, Storekeeper",
        "focus": "Minimum Stock Thresholds & Automatic Reorder Triggers",
        "does": "Constantly monitors warehouse stock against predefined minimum threshold levels and automatically generates a suggested restocking order when fast-moving friction discs or seals run low.",
        "benefit": "Ensures Dalal never turns away an emergency breakdown client due to being out of stock on common wear parts, protecting customer loyalty and recurring parts profits.",
        "deliverables": ["Automated Low-Stock Threshold Notifications", "Suggested Re-Order Quantity Calculator", "Supplier Lead Time Buffer Estimation"],
        "feature": "Automated alert notifications sent when fast-moving clutch spares reach minimum stock thresholds."
    },
    {
        "id": "ERP-MOD-10",
        "title": "Multi-Godown Stock Transfer Note",
        "engine": "Engine 2: Inventory & Warehouse Master",
        "role": "Logistics Dispatcher, Storekeeper",
        "focus": "Official Transfer Documentation Between Warehouses",
        "does": "Generates official transfer delivery challans whenever equipment or spare parts move between the Chakan warehouse, Tardeo office, customer trial premises, or third-party engineering workshops.",
        "benefit": "Prevents stock loss and inventory discrepancies during transit, providing legal documentation required by highway GST authorities to avoid transit seizure and vehicle impounding.",
        "deliverables": ["Official Inter-Godown Delivery Challan Generator", "E-Way Bill Integration Data Sheet", "In-Transit Goods Reconciliation Ledger"],
        "feature": "1-click generation of GST-compliant delivery challans for inter-facility equipment movement."
    },
    # Page 20
    {
        "id": "ERP-MOD-11",
        "title": "Barcoded Godown Bin & Shelf Locator",
        "engine": "Engine 2: Inventory & Warehouse Master",
        "role": "Godown Storekeeper, Warehouse Staff",
        "focus": "Physical Shelf Organization & Quick Item Picking",
        "does": "Assigns unique rack, row, and shelf coordinates to every small clutch spare, seal kit, and rotating union, accessible via mobile phone scanning or quick search at the godown desk.",
        "benefit": "Reduces picking and packing time from 30 minutes to under 2 minutes, ensuring orders are packed and dispatched on courier vehicles before daily parcel cutoff times.",
        "deliverables": ["Godown Rack & Bin Coordinate Mapping", "Mobile-Friendly Shelf Search Interface", "Fast Item Picking Route Optimization"],
        "feature": "Search tool directing warehouse staff to the exact rack and shelf location of any spare part."
    },
    {
        "id": "ERP-MOD-12",
        "title": "Consignment Stock & Customer Trial Ledger",
        "engine": "Engine 2: Inventory & Warehouse Master",
        "role": "Sales Manager, Accounts Manager",
        "focus": "Temporary Equipment Handover & Return Management",
        "does": "Tracks clutch units or testing instruments provided to customer factories on a 15-day trial or consignment basis, monitoring return due dates, condition upon return, and conversion to sale.",
        "benefit": "Stops equipment leakage and forgotten company property at customer factories, automatically reminding sales representatives to either invoice the client or arrange immediate retrieval.",
        "deliverables": ["Customer Trial Equipment Master Registry", "15-Day Return Expiration Alerts", "Trial-to-Invoice Conversion Workflow"],
        "feature": "Automated reminder alerts for consignment stock approaching the end of authorized trial periods."
    },
    # Page 21
    {
        "id": "ERP-MOD-13",
        "title": "Italy Factory Purchase Order Engine",
        "engine": "Engine 3: Procurement & Landed Costing",
        "role": "Commercial Head, Managing Director",
        "focus": "Formal International PO Generation in Euros",
        "does": "Creates formal international purchase orders in Euros addressed to OMPI Italy, complete with official Italian part numbers, agreed export discounts, shipping marks, and HS codes.",
        "benefit": "Eliminates ordering mistakes with the Italian factory, speeds up export manufacturing, and ensures imported documentation matches Indian Customs requirements for smooth port clearance.",
        "deliverables": ["International Purchase Order PDF Generator", "Official Italian Part Number & HS Code Matcher", "Supplier Confirmation & Lead Time Tracker"],
        "feature": "Direct generation of international purchase orders with dual English/Italian commercial terminology."
    },
    {
        "id": "ERP-MOD-14",
        "title": "Customs Clearing & Port Demurrage Shield",
        "engine": "Engine 3: Procurement & Landed Costing",
        "role": "Logistics Manager, Customs Broker",
        "focus": "Port Clearance Milestones & Penalty Avoidance",
        "does": "Tracks customs clearance milestones at Nhava Sheva port, alerting the commercial team to free storage expiry dates, container detention deadlines, and customs duty payment milestones.",
        "benefit": "Saves Dalal lakhs of rupees annually in catastrophic port demurrage and shipping line container detention penalties by enforcing on-time document submission and vehicle booking.",
        "deliverables": ["Free Storage Expiry Countdown Dashboard", "Shipping Line Container Detention Tracker", "Customs Duty Assessment & Payment Alert"],
        "feature": "Demurrage risk dashboard highlighting shipments within 48 hours of incurring daily port fines."
    },
    # Page 22
    {
        "id": "ERP-MOD-15",
        "title": "Landed Surcharge Costing Sheet",
        "engine": "Engine 3: Procurement & Landed Costing",
        "role": "Senior Accountant, Commercial Head",
        "focus": "True Unit Cost Allocation (Freight, Duty, Clearing)",
        "does": "Calculates the true landed cost of every imported batch by distributing ocean freight, insurance, customs basic duty, social welfare surcharge, and port clearing charges across individual items.",
        "benefit": "Reveals the true mathematical cost of every SKU, ensuring Dalal never underprices products or misjudges margins, keeping company pricing profitable and commercially competitive.",
        "deliverables": ["Proportional Expense Allocation Matrix", "True Unit Cost Calculation Engine", "Margin Variance & Profitability Reporting"],
        "feature": "Comprehensive landed cost calculator allocating shared container shipping fees across individual spare parts."
    },
    {
        "id": "ERP-MOD-16",
        "title": "Supplier Performance & Lead Time Tracker",
        "engine": "Engine 3: Procurement & Landed Costing",
        "role": "Managing Director, Purchasing Head",
        "focus": "Vendor Delivery Accuracy & Lead Time Trends",
        "does": "Records promised delivery dates versus actual dispatch dates for European and domestic suppliers, tracking manufacturing delays, shipping transit times, and packaging quality.",
        "benefit": "Gives management hard data during annual commercial negotiations with overseas partners, securing better delivery guarantees, warranty compensation, and commercial credit terms.",
        "deliverables": ["Supplier Delivery Timeliness Scorecards", "Historical Lead Time Trend Analytics", "Transit Delay & Defect Rate Reporting"],
        "feature": "Supplier reliability scorecards rating manufacturers on dispatch speed and packaging quality."
    },
    # Page 23
    {
        "id": "ERP-MOD-17",
        "title": "Factory Reconditioning & Overhaul Log",
        "engine": "Engine 4: Workshop & Engineering Overhaul",
        "role": "Workshop Foreman, Mechanical Engineers",
        "focus": "Job Cards, Replacement Parts & Labor Hours",
        "does": "Maintains a digital job card for every used machine entering the Pune workshop: records dismantling steps, replacement parts used, machinist labor hours, and component repairs.",
        "benefit": "Establishes accurate restoration cost accounting, prevents mechanical shortcuts, and creates a certified repair history that commands premium selling prices from prospective buyers.",
        "deliverables": ["Digital Workshop Job Card & Task Tracker", "Replacement Spares & Material Consumption Log", "Mechanic Labor Hours & Direct Cost Ledger"],
        "feature": "Digital job card logging every mechanical overhaul step and component replacement with technician signatures."
    },
    {
        "id": "ERP-MOD-18",
        "title": "Clutch Retrofit Engineering Work Order",
        "engine": "Engine 4: Workshop & Engineering Overhaul",
        "role": "Application Engineers, Workshop Team",
        "focus": "Technical Machining Dimensions & Air Valve Specs",
        "does": "Provides step-by-step engineering instructions for installing an OMPI pneumatic clutch onto a customer's existing mechanical press: flywheel boring dimensions, keyway depths, and valve mounting.",
        "benefit": "Eliminates machining mistakes and mechanical rework, ensuring flawless on-site installation and preventing clutch overheating or slipping during full-power production runs.",
        "deliverables": ["Flywheel Boring & Keyway Machining Specs", "Dual Air Valve & Piping Flow Diagrams", "Pre-Commissioning Mechanical Checklists"],
        "feature": "Printable technical work orders with detailed dimensional tolerances for workshop machinists."
    },
    # Page 24
    {
        "id": "ERP-MOD-19",
        "title": "Live Power Test & Geometry Sheet",
        "engine": "Engine 4: Workshop & Engineering Overhaul",
        "role": "Quality Inspector, Technical Director",
        "focus": "Dial Gauge Alignment, Stroke Testing & Defect Log",
        "does": "Records geometrical inspection data for every overhauled press: bed parallelism, ram squareness dial indicator readings, motor amperage draw under idle/load, and clutch stopping times.",
        "benefit": "Provides irrefutable technical documentation proving machine precision to corporate buyers, completely preventing post-delivery disputes and warranty rejection claims.",
        "deliverables": ["Bed Parallelism Dial Gauge Inspection Sheet", "Clutch Stopping Time & Safety Reaction Log", "Official Dalal Machine Inspection Certificate"],
        "feature": "Standardized inspection certificate generator showing verified machine tolerances and electrical trial results."
    },
    {
        "id": "ERP-MOD-20",
        "title": "Client Site Rigging & Handover Certificate",
        "engine": "Engine 4: Workshop & Engineering Overhaul",
        "role": "Field Commissioning Engineer, Client Head",
        "focus": "Foundation Leveling, Trial Stamping & Sign-Off",
        "does": "A mobile-friendly sign-off protocol used by Dalal engineers during final machine installation at the buyer's factory: confirms levelness, trial stamping, and customer acceptance signatures.",
        "benefit": "Triggers final payment release by obtaining unambiguous formal customer acceptance, protecting Dalal from delayed settlement of final 10% to 20% commercial retention funds.",
        "deliverables": ["Mobile-Friendly Commissioning Protocol", "Digital Client Acceptance Signature Capture", "Automatic Accounts Notification for Final Invoicing"],
        "feature": "Digital handover certificate capture with photo uploads of the installed machine on the customer's factory floor."
    },
    # Page 25
    {
        "id": "ERP-MOD-21",
        "title": "GST Tax Invoice & E-Way Bill Generator",
        "engine": "Engine 5: Accounting & GST Governance",
        "role": "Accounts Manager, Billing Clerk",
        "focus": "Legal Tax Billing, HSN Codes & E-Way Bill Data",
        "does": "Generates legally compliant tax invoices for machinery sales, spare parts, and service labor with automatic calculation of CGST, SGST, IGST, correct HSN codes, and transport E-Way Bill data.",
        "benefit": "Eliminates tax calculation errors, prevents costly GST audits and fines, and ensures buyers receive immaculate tax invoices that allow 100% input tax credit without government delays.",
        "deliverables": ["Automated Multi-Rate GST Tax Invoice Generator", "HSN Code & Tax Category Validation Engine", "E-Way Bill Transport Data Format Generator"],
        "feature": "1-click generation of professional GST tax invoices with automatic tax rate calculation based on client state."
    },
    {
        "id": "ERP-MOD-22",
        "title": "Client Payment Ledger & Aging Tracker",
        "engine": "Engine 5: Accounting & GST Governance",
        "role": "Commercial Manager, Managing Director",
        "focus": "Outstanding Receivables, Payment Terms & Alerts",
        "does": "Tracks customer payment milestones (advance payment, pre-dispatch clearance, final commissioning balance), categorizing outstanding dues by age: 30, 60, and 90+ days overdue.",
        "benefit": "Guarantees that no machine is loaded onto transport trailers before agreed advance and pre-dispatch payments are fully cleared in Dalal's bank account, protecting company cash flow.",
        "deliverables": ["Customer Payment Aging Analysis Dashboard", "Pre-Dispatch Commercial Clearance Indicator", "Automated Friendly Payment Reminder Letters"],
        "feature": "Color-coded payment ledger preventing warehouse dispatch until pre-dispatch payment criteria are verified."
    },
    # Page 26
    {
        "id": "ERP-MOD-23",
        "title": "Vendor Expense & Overseas Wire Log",
        "engine": "Engine 5: Accounting & GST Governance",
        "role": "Senior Accountant, Finance Director",
        "focus": "Overseas Remittances, Shipping Bills & A2 Records",
        "does": "Maintains an organized digital record of all payments made to overseas manufacturers, customs clearing agents, crane operators, transport contractors, and local repair vendors.",
        "benefit": "Simplifies bank audits and FEMA compliance for overseas foreign exchange remittances (Form A2), ensuring your banking facility remains in flawless standing with foreign exchange regulators.",
        "deliverables": ["Bank Form A2 & Overseas Remittance Log", "Vendor Expense Verification & PO Matching", "Authorized Corporate Payment Approval Workflow"],
        "feature": "Centralized foreign exchange payment repository linking bank SWIFT confirmations to foreign supplier invoices."
    },
    {
        "id": "ERP-MOD-24",
        "title": "Monthly P&L & Gross Margin Dashboard",
        "engine": "Engine 5: Accounting & GST Governance",
        "role": "Managing Director, Partners",
        "focus": "Monthly Profitability, Machine Margin & Overhead",
        "does": "Aggregates revenue and direct costs across all transactions, presenting monthly gross profit per machine, spare parts profitability, and company operating overheads at a glance.",
        "benefit": "Gives the business owners clear, real-time financial truth, allowing informed decisions on capital reinvestment, inventory expansion, and pricing adjustments without waiting for year-end books.",
        "deliverables": ["Real-Time Gross Margin Analytics per Machine", "Spare Parts Division Profitability Breakdown", "Monthly Overhead & Cash Flow Forecasting"],
        "feature": "Executive financial overview dashboard showing true profitability per business line in real time."
    },
    # Page 27
    {
        "id": "ERP-MOD-25",
        "title": "GSTR-1 & ITC-04 Compliance Assistant",
        "engine": "Engine 5: Accounting & GST Governance",
        "role": "Accounts Manager, Tax Consultant",
        "focus": "GST Return Preparation & Job Work Tracking",
        "does": "Pre-formats all monthly sales invoices, credit notes, and job-work delivery challans (ITC-04 for goods sent to external workshops) for direct import into government GST accounting software.",
        "benefit": "Saves your accounting team dozens of hours of tedious manual data entry every month and eliminates filing errors that trigger tax notices, interest penalties, and frozen tax credits.",
        "deliverables": ["Monthly GSTR-1 Sales Data Reconciliation Sheet", "ITC-04 Job Work Outward & Inward Ledger", "Tax Variance Detection & Correction Engine"],
        "feature": "Automated monthly tax summary pre-formatted for seamless reconciliation with your CA's accounting system."
    },
    {
        "id": "ERP-MOD-26",
        "title": "Sales Rep Daily Visit & Inquiry Logger",
        "engine": "Engine 6: Sales Force & Customer Service",
        "role": "Field Sales Engineers, Sales Head",
        "focus": "Client Factory Visits, Machinery Needs & Follow-Ups",
        "does": "A mobile-friendly logging tool for sales engineers visiting manufacturing clusters in Pune, Sanand, Aurangabad, and Rajkot to record client plant visits, machinery requirements, and follow-up dates.",
        "benefit": "Builds institutional company memory. When a sales employee resigns, all customer relationships, active discussions, and machinery needs remain securely preserved in Dalal's database.",
        "deliverables": ["Mobile Client Factory Visit Log", "Competitor Machinery Identification Matrix", "Scheduled Actionable Follow-Up Reminders"],
        "feature": "Mobile-optimized visit logging interface allowing sales reps to record client discussions in 60 seconds."
    },
    # Page 28
    {
        "id": "ERP-MOD-27",
        "title": "Commercial Proposal Follow-Up Alert",
        "engine": "Engine 6: Sales Force & Customer Service",
        "role": "Sales Team, Managing Director",
        "focus": "Automated Follow-Up Reminders on Active Quotes",
        "does": "Monitors all outstanding quotations sent to customers and automatically reminds the assigned sales representative to follow up via phone or WhatsApp at 3, 7, and 14-day intervals.",
        "benefit": "Prevents quotes from going cold and keeps Dalal top-of-mind while the customer's purchase committee evaluates options, directly recovering potentially lost high-value deals.",
        "deliverables": ["Automated Follow-Up Reminder Dashboard", "Pre-Drafted Professional WhatsApp Follow-Up Templates", "Quotation Win/Loss Reason Analytics"],
        "feature": "Automated alerts reminding sales staff to follow up on pending proposals before competitors intervene."
    },
    {
        "id": "ERP-MOD-28",
        "title": "Annual Maintenance Contract (AMC) Ledger",
        "engine": "Engine 6: Sales Force & Customer Service",
        "role": "Service Coordinator, Accounts Manager",
        "focus": "Preventative Service Schedules & Contract Renewals",
        "does": "Tracks all active maintenance contracts, scheduling preventative quarterly inspection visits, tracking engineer time spent on site, and alerting the commercial team 30 days before renewal.",
        "benefit": "Maximizes contract renewal rates and prevents missed inspection visits, protecting your reputation for reliability and securing dependable recurring annual service income.",
        "deliverables": ["Quarterly Service Visit Schedule Calendar", "30-Day Contract Expiration & Renewal Alerts", "Service Engineer Shop Floor Time & Parts Log"],
        "feature": "Automated service schedule calendar tracking upcoming preventive maintenance visits across all client plants."
    },
    # Page 29
    {
        "id": "ERP-MOD-29",
        "title": "Machine Breakdown Ticket Desk",
        "engine": "Engine 6: Sales Force & Customer Service",
        "role": "Service Engineers, Support Coordinator",
        "focus": "Customer Breakdown Logging & Technician Dispatch",
        "does": "Logs urgent customer breakdown calls, assigns the closest available technical engineer, tracks replacement part dispatch from Pune, and monitors repair progress until the machine is running.",
        "benefit": "Dramatically reduces factory downtime for your clients during emergencies, turning stressful crisis situations into long-term customer loyalty and word-of-mouth industry praise.",
        "deliverables": ["Priority Breakdown Ticket Creation Console", "Service Engineer Dispatch & GPS Proximity", "Resolution Verification & Customer Sign-Off"],
        "feature": "High-priority support desk dispatching service engineers to machine breakdown emergencies within hours."
    },
    {
        "id": "ERP-MOD-30",
        "title": "Customer Feedback & Quality Scoring",
        "engine": "Engine 6: Sales Force & Customer Service",
        "role": "Managing Director, Quality Head",
        "focus": "Post-Installation Satisfaction & Review Capture",
        "does": "Automatically sends a brief 3-question satisfaction survey to the factory owner 30 days after machine commissioning, rating machine performance, delivery speed, and engineer professionalism.",
        "benefit": "Detects customer dissatisfaction early before it damages relationships, identifies standout employees for recognition, and collects glowing testimonials for the public website.",
        "deliverables": ["Automated 3-Question Customer Satisfaction Survey", "Early Warning Dissatisfaction Escalation Alert", "Verified Customer Testimonial Capture for Marketing"],
        "feature": "Automated satisfaction survey collecting client ratings and generating verified testimonial quotes."
    },
    # Page 30
    {
        "id": "ERP-MOD-31",
        "title": "Staff Role & Security Permissions",
        "engine": "Engine 7: Executive Intelligence & Control",
        "role": "Managing Director, System Administrator",
        "focus": "Role-Based Security & Confidential Margin Protection",
        "does": "Controls exactly what each employee can see and do: sales reps can view quotes and stocks but cannot see supplier purchase prices; storekeepers can update inventory but cannot view margins.",
        "benefit": "Protects trade secrets, prevents unauthorized changes to company data, and ensures confidential supplier margins and pricing models remain strictly restricted to top business owners.",
        "deliverables": ["Granular Role-Based Access Permission Matrix", "Multi-Factor Secure Authentication System", "Strict Separation of Sales and Purchasing Financial Data"],
        "feature": "Security control console allowing the Managing Director to customize employee data permissions in seconds."
    },
    {
        "id": "ERP-MOD-32",
        "title": "Automated Cloud Backup & Audit Vault",
        "engine": "Engine 7: Executive Intelligence & Control",
        "role": "System Administrator, Managing Director",
        "focus": "Daily Encrypted Backups & Immutable Change History",
        "does": "Creates encrypted daily backups of all customer files, quotations, stock records, and financial transactions, while logging every price change, stock deduction, and user login in an immutable audit vault.",
        "benefit": "Eliminates the catastrophic threat of data loss from hardware failure or accidental deletion, providing complete peace of mind that company operational records are permanently safe.",
        "deliverables": ["Automated Daily Encrypted Cloud Database Backups", "Immutable Tamper-Proof User Activity Audit Trail", "Rapid Disaster Recovery Restoration Protocol"],
        "feature": "Automated audit vault recording every price modification, stock adjustment, and proposal creation."
    },
    # Page 31
    {
        "id": "ERP-MOD-33",
        "title": "Managing Director's Executive Control Desk",
        "engine": "Engine 7: Executive Intelligence & Control",
        "role": "Mr. Vinit Dalal, Company Partners",
        "focus": "Unified Business Dashboard (Sales, Cash, Godown & Staff)",
        "does": "An executive mobile and desktop command center presenting complete business health: total inquiries this month, active high-value quotations, Pune warehouse stock value, and cash collected.",
        "benefit": "Gives the business owner total command over company operations from anywhere in the world, enabling confident strategic decisions based on real-time financial facts rather than guesswork.",
        "deliverables": ["Real-Time Total Business Command Center", "Active Pipeline Value & Cash Inflow Projections", "Executive KPI Metrics & Daily Operational Summary"],
        "feature": "Real-time command center providing a 360-degree executive view of sales, godown stock, and profit margins."
    }
]

print(f"Loaded {len(dalal_routes)} Dalal Routes and {len(ompi_modules)} OMPI Modules.")

# Let's define the CSS and Layout Generators
def build_html_document():
    css = """
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
      font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      color: #0f172a;
      background: #ffffff;
      font-size: 10.0pt;
      line-height: 1.50;
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
      position: relative;
    }
    .page-content {
      flex: 1;
      display: flex;
      flex-direction: column;
    }

    /* Corporate Header */
    .header-bar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 2.5px solid #0f172a;
      border-top: 4px solid #d97706;
      padding: 5px 0;
      margin-bottom: 6px;
    }
    .brand-title {
      font-size: 11.8pt;
      font-weight: 800;
      color: #0f172a;
      letter-spacing: -0.2px;
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
      font-size: 7.6pt;
      color: #475569;
      line-height: 1.35;
    }

    /* Strict Confidentiality Bar */
    .confidential-bar {
      background: #fef2f2;
      border: 1.5px solid #dc2626;
      border-radius: 5px;
      padding: 4.5px 10px;
      margin-bottom: 7px;
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
      letter-spacing: 0.4px;
    }

    /* Section Subheader */
    .section-header {
      background: #0f172a;
      color: #ffffff;
      padding: 5.5px 12px;
      border-radius: 5px;
      margin-bottom: 9px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .section-title {
      font-size: 9.0pt;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.3px;
    }
    .section-tag {
      font-size: 7.6pt;
      font-weight: 700;
      background: #f59e0b;
      color: #0f172a;
      padding: 2px 8px;
      border-radius: 3px;
    }

    /* Standard Card Box (2 per page, calibrated height to fill canvas gracefully) */
    .card-box {
      border: 1.5px solid #cbd5e1;
      border-radius: 8px;
      background: #ffffff;
      margin-bottom: 8px;
      padding: 10px 14px;
      box-shadow: 0 1px 3px rgba(0,0,0,0.03);
    }
    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 1.5px solid #e2e8f0;
      padding-bottom: 6px;
      margin-bottom: 7px;
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
      font-size: 11.2pt;
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
      margin-bottom: 7px;
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
      margin-bottom: 8px;
    }
    .grid-label {
      font-size: 8.0pt;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.3px;
      color: #475569;
      margin-bottom: 2px;
      border-bottom: 1px solid #f1f5f9;
      padding-bottom: 2px;
    }
    .grid-text {
      font-size: 9.3pt;
      line-height: 1.44;
      color: #334155;
    }
    .deliverables-box {
      background: #f8fafc;
      border: 1px solid #e2e8f0;
      border-radius: 5px;
      padding: 4px 8px;
      margin-bottom: 5px;
    }
    .deliverables-title {
      font-size: 7.6pt;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.4px;
      color: #64748b;
      margin-bottom: 3px;
    }
    .deliverables-grid {
      display: grid;
      grid-template-columns: 1fr 1fr 1fr;
      gap: 8px;
    }
    .deliverable-item {
      font-size: 8.1pt;
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
      padding: 7.5px 12px;
      font-size: 8.6pt;
      line-height: 1.38;
      color: #1e40af;
    }
    .feature-strip strong {
      color: #1e3a8a;
    }

    /* Corporate Footer */
    .footer-bar {
      border-top: 1.5px solid #cbd5e1;
      padding-top: 4.5px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 7.5pt;
      color: #64748b;
      margin-top: auto;
    }
    .confidential-watermark {
      font-weight: 800;
      color: #dc2626;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }
    """

    def make_header(subtitle):
        return f"""
        <div class="header-bar">
          <div>
            <div class="brand-title">DALAL MACHINE TOOLS AGENCY &amp; OMPI INDIA</div>
            <div class="brand-subtitle">{subtitle}</div>
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
        """

    def make_footer(page_num):
        return f"""
        <div class="footer-bar">
          <div><strong>Dalal Machine Tools Agency Pvt. Ltd. &amp; OMPI India LLP</strong> &bull; Commercial Operations Blueprint</div>
          <div class="confidential-watermark">&#128274; CONFIDENTIAL &bull; STRICTLY NOT FOR SHARING</div>
          <div>Page {page_num} of 32</div>
        </div>
        """

    def render_card(item, is_route=True):
        scope_tag = "&#9675; TO BE BUILT: SYSTEM 1" if is_route else "&#9675; TO BE BUILT: SYSTEM 2"
        badge_meta = f"Planned Route: {item['path'].split(': ')[-1]}" if is_route else item['engine']
        target_label = "Primary Business Audience" if is_route else "Responsible Staff Role"
        target_val = item['audience'] if is_route else item['role']
        focus_val = item.get('focus', 'Operational Governance & Efficiency')
        what_label = "What This Web Page Will Do Once Built" if is_route else "What This Management Tool Will Do Once Built"
        what_text = item['does'] if not is_route else item['does']
        
        deliverables_html = ""
        for d in item.get('deliverables', ['Standard Operational Deliverable', 'Verified Process Automation', 'Executive Control Mechanism']):
            deliverables_html += f"""
            <div class="deliverable-item">
              <svg fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/></svg>
              <span>{d}</span>
            </div>
            """

        return f"""
        <div class="card-box">
          <div class="card-header">
            <div>
              <span class="badge-id">{item['id']}</span>
              <span class="card-title">{item['title']}</span>
              <span class="card-status">{scope_tag}</span>
            </div>
            <div style="font-family:'JetBrains Mono',monospace; font-size:7.8pt; color:#b45309; background:#fffbeb; padding:2px 8px; border:1px solid #fef3c7; border-radius:3px;">
              {badge_meta}
            </div>
          </div>
          <div class="meta-row">
            <div><strong>{target_label}:</strong> {target_val}</div>
            <div><strong>Operational Focus:</strong> {focus_val}</div>
          </div>
          <div class="simple-grid">
            <div>
              <div class="grid-label">{what_label}</div>
              <div class="grid-text">{what_text}</div>
            </div>
            <div>
              <div class="grid-label">Business Value &amp; Commercial Risk It Prevents</div>
              <div class="grid-text">{item['benefit']}</div>
            </div>
          </div>
          <div class="deliverables-box">
            <div class="deliverables-title">Key Tangible System Capabilities (To Be Built)</div>
            <div class="deliverables-grid">
              {deliverables_html}
            </div>
          </div>
          <div class="feature-strip">
            <strong>Key Management Feature:</strong> {item['feature']}
          </div>
          <div style="display:flex; justify-content:space-between; align-items:center; background:#f8fafc; border:1px solid #e2e8f0; border-radius:4px; padding:3.5px 10px; margin-top:6px; font-size:7.8pt; color:#475569;">
            <div><strong>Quality Assurance Gate:</strong> Functional Quality Test Prior to Shop Floor Deployment</div>
            <div><strong>Pre-Commencement Status:</strong> Proposed Scope &bull; Pending Formal Sign-Off</div>
          </div>
        </div>
        """

    # HTML Shell
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Dalal &amp; OMPI 57 Master Specification &bull; Pre-Commencement Scope Blueprint</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;700&display=swap" rel="stylesheet">
  <style>
    {css}
  </style>
</head>
<body>
"""

    # PAGE 1: EXECUTIVE COVER PAGE
    html += f"""
  <div class="page">
    <div class="page-content">
      {make_header("PRE-COMMENCEMENT MASTER ARCHITECTURAL SCOPE BLUEPRINT &bull; 57 PLANNED UNITS")}

      <!-- Hero Header Box -->
      <div style="background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); color: #ffffff; border-radius: 8px; padding: 22px 24px; margin-bottom: 12px; border-left: 6px solid #d97706; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);">
        <div style="font-size: 8.5pt; font-weight: 800; color: #f59e0b; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 4px;">
          Executive Strategy &bull; Pre-Commencement Architecture Proposal
        </div>
        <div style="font-size: 19.0pt; font-weight: 800; line-height: 1.25; margin-bottom: 8px;">
          Unified Digital Ecosystem &amp; Enterprise Operations Suite
        </div>
        <div style="font-size: 10.5pt; line-height: 1.50; color: #cbd5e1;">
          Comprehensive 57-Point Operational Blueprint for <strong>Dalal Machine Tools Agency Pvt. Ltd.</strong> and <strong>OMPI India LLP</strong>. Engineered in plain business English for executive leadership, plant owners, and commercial heads.
        </div>
      </div>

      <!-- Pre-Commencement Declaration Alert -->
      <div style="background:#fffbeb; border:2px solid #f59e0b; border-radius:7px; padding:12px 16px; margin-bottom:12px;">
        <div style="font-size:9.5pt; font-weight:800; color:#b45309; text-transform:uppercase; margin-bottom:3px; display:flex; align-items:center; gap:6px;">
          &#9888; Official Notice: Pre-Commencement Scope Document (Work Not Started)
        </div>
        <p style="font-size:9.0pt; line-height:1.45; color:#78350f;">
          This document serves as the formal architectural proposal detailing exactly what will be built upon mutual agreement and contract signing. <strong>No development or programming work has commenced yet.</strong> This master dossier details all 24 public/administrative web pages for Dalal and 33 operational ERP modules for OMPI India to align business goals before project kickoff.
        </p>
      </div>

      <!-- 4 Pillars Grid -->
      <div style="display:grid; grid-template-columns:1fr 1fr; gap:11px; margin-bottom:12px;">
        <div style="background:#f8fafc; border:1.5px solid #cbd5e1; border-radius:7px; padding:12px 14px;">
          <div style="font-size:9.2pt; font-weight:800; color:#0f172a; text-transform:uppercase; margin-bottom:3px; border-bottom:1.5px solid #e2e8f0; padding-bottom:3px;">
            System 1: Dalal Machinery Platform (24 Units)
          </div>
          <p style="font-size:8.8pt; line-height:1.42; color:#334155;">
            High-impact machinery showroom, live video power trials, 60-second quotation downloads, press tonnage calculators, and real-time WhatsApp inquiry dispatch designed to capture multi-crore machinery buyers across India.
          </p>
        </div>
        <div style="background:#f8fafc; border:1.5px solid #cbd5e1; border-radius:7px; padding:12px 14px;">
          <div style="font-size:9.2pt; font-weight:800; color:#0f172a; text-transform:uppercase; margin-bottom:3px; border-bottom:1.5px solid #e2e8f0; padding-bottom:3px;">
            System 2: OMPI Operations ERP Suite (33 Units)
          </div>
          <p style="font-size:8.8pt; line-height:1.42; color:#334155;">
            End-to-end industrial management system covering Italian factory purchase orders, landed container costing, barcoded godown inventory, workshop machine overhauls, GST tax compliance, and Director intelligence.
          </p>
        </div>
      </div>

      <!-- Confidentiality & Non-Disclosure Governance Box -->
      <div style="border:1.5px solid #e11d48; background:#fff1f2; border-radius:7px; padding:12px 16px; margin-bottom:12px;">
        <div style="font-size:9.2pt; font-weight:800; color:#9f1239; text-transform:uppercase; margin-bottom:3px; display:flex; align-items:center; gap:6px;">
          &#128274; Strict Non-Disclosure &amp; Proprietary Ownership Covenant
        </div>
        <p style="font-size:8.8pt; line-height:1.45; color:#4c0519;">
          This master specification represents the proprietary intellectual property and commercial operational methods of Dalal Machine Tools Agency Pvt. Ltd. and OMPI India LLP. <strong>Strictly confidential and strictly not for sharing.</strong> Any unauthorized distribution, reproduction, copying, or disclosure to external parties, competitors, or third-party developers without prior written authorization is strictly prohibited.
        </p>
      </div>

      <!-- Strategic Document Orientation & Governance Box -->
      <div style="background:#ffffff; border:1.5px solid #cbd5e1; border-radius:7px; padding:11px 16px; margin-bottom:11px;">
        <div style="font-size:8.8pt; font-weight:800; color:#0f172a; text-transform:uppercase; margin-bottom:5px; border-bottom:1.5px solid #f1f5f9; padding-bottom:3px;">
          Master Proposal Structure &bull; How Executive Leadership Should Review This Document
        </div>
        <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px; font-size:8.4pt; line-height:1.4; color:#334155;">
          <div>
            <strong>Pages 02 to 13: Dalal Public Web Ecosystem</strong><br>
            24 customer-facing pages engineered to build trust with plant owners, show live power trials, generate 60-second quotations, and capture high-value machinery inquiries.
          </div>
          <div>
            <strong>Pages 14 to 31: OMPI Operations ERP Suite</strong><br>
            33 operational management modules designed to eliminate inventory errors, manage Italian imports in Euros, handle GST billing, and give the Managing Director real-time control.
          </div>
        </div>
      </div>

      <!-- Key Project Metadata Box -->
      <div style="background:#ffffff; border:1.5px solid #0f172a; border-radius:7px; padding:9px 16px; display:flex; justify-content:space-between; align-items:center;">
        <div>
          <span style="font-size:7.8pt; color:#64748b; font-weight:700; text-transform:uppercase;">Principal Client:</span><br>
          <strong style="font-size:9.6pt; color:#0f172a;">Mr. Vinit Dalal</strong> &bull; Managing Director / Partner
        </div>
        <div>
          <span style="font-size:7.8pt; color:#64748b; font-weight:700; text-transform:uppercase;">Scope Architecture:</span><br>
          <strong style="font-size:9.6pt; color:#0f172a;">57 Proposed Units</strong> &bull; 0 Lines Code Written
        </div>
        <div>
          <span style="font-size:7.8pt; color:#64748b; font-weight:700; text-transform:uppercase;">Prepared by Consultant:</span><br>
          <strong style="font-size:9.6pt; color:#0f172a;">Suyash Shinde</strong> &bull; Pimpri, Pune
        </div>
      </div>
    </div>
    {make_footer(1)}
  </div>
"""

    # PAGES 2 TO 13: DALAL 24 ROUTES (2 PER PAGE)
    for i in range(12):
        page_num = i + 2
        r1 = dalal_routes[i * 2]
        r2 = dalal_routes[i * 2 + 1]

        html += f"""
  <div class="page">
    <div class="page-content">
      {make_header("SYSTEM 1: DALAL MACHINERY PUBLIC PLATFORM &bull; PROPOSED SCOPE")}

      <div class="section-header">
        <span class="section-title">Dalal Web Presence Scope &bull; Pages {i*2+1:02d} &amp; {i*2+2:02d} of 24 (To Be Engineered)</span>
        <span class="section-tag">Public Client Gateway</span>
      </div>

      {render_card(r1, is_route=True)}
      {render_card(r2, is_route=True)}
    </div>
    {make_footer(page_num)}
  </div>
"""

    # PAGE 14: OMPI SYSTEM ARCHITECTURE MAP
    html += f"""
  <div class="page">
    <div class="page-content">
      {make_header("SYSTEM 2: OMPI INDUSTRIAL OPERATIONS SUITE &bull; ARCHITECTURAL MAP")}

      <!-- Hero Transition Banner -->
      <div style="background: linear-gradient(135deg, #1e3a8a 0%, #0f172a 100%); color: #ffffff; border-radius: 8px; padding: 14px 18px; margin-bottom: 8px; border-left: 6px solid #38bdf8; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);">
        <div style="font-size: 8.5pt; font-weight: 800; color: #38bdf8; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 4px;">
          Operations Master Engine &bull; 33 Specialized Functional Modules
        </div>
        <div style="font-size: 17.5pt; font-weight: 800; line-height: 1.25; margin-bottom: 6px;">
          OMPI India Industrial Operations &amp; ERP Management Suite
        </div>
        <div style="font-size: 10.0pt; line-height: 1.50; color: #e2e8f0;">
          A standalone operational backbone built to manage Italian import supply chains, Pune godown stock, workshop press reconditioning, GST tax governance, and executive oversight.
        </div>
      </div>

      <!-- 7 Functional Engines Table -->
      <div style="background:#ffffff; border:1.5px solid #cbd5e1; border-radius:7px; padding:8px 12px; margin-bottom:8px;">
        <div style="font-size:9.2pt; font-weight:800; color:#0f172a; text-transform:uppercase; margin-bottom:6px; border-bottom:1.5px solid #f1f5f9; padding-bottom:3px;">
          The 7 Core Operational Engines to be Engineered (Modules 01 to 33)
        </div>
        <table style="width:100%; border-collapse:collapse; font-size:8.6pt; line-height:1.4; color:#334155;">
          <thead>
            <tr style="background:#0f172a; color:#ffffff; text-align:left;">
              <th style="padding:3.5px 7px;">Operational Engine</th>
              <th style="padding:3.5px 7px;">Planned Modules</th>
              <th style="padding:3.5px 7px;">Core Business Responsibility</th>
            </tr>
          </thead>
          <tbody>
            <tr style="border-bottom:1px solid #e2e8f0; background:#ffffff;">
              <td style="padding:3.5px 7px; font-weight:700; color:#0f172a;">Engine 1: Sales &amp; Pipeline</td>
              <td style="padding:3.5px 7px; font-weight:600; color:#b45309;">Modules 01 to 06</td>
              <td style="padding:3.5px 7px;">Client records, Italian SKU master, 60-second quote generator, deal pipeline.</td>
            </tr>
            <tr style="border-bottom:1px solid #e2e8f0; background:#f8fafc;">
              <td style="padding:3.5px 7px; font-weight:700; color:#0f172a;">Engine 2: Inventory &amp; Godown</td>
              <td style="padding:3.5px 7px; font-weight:600; color:#b45309;">Modules 07 to 12</td>
              <td style="padding:3.5px 7px;">Live Pune stock, in-transit containers, re-order alerts, shelf bin coordinates.</td>
            </tr>
            <tr style="border-bottom:1px solid #e2e8f0; background:#ffffff;">
              <td style="padding:3.5px 7px; font-weight:700; color:#0f172a;">Engine 3: Procurement &amp; Costing</td>
              <td style="padding:3.5px 7px; font-weight:600; color:#b45309;">Modules 13 to 16</td>
              <td style="padding:3.5px 7px;">Italy POs in Euros, port demurrage shield, true landed costing, supplier scores.</td>
            </tr>
            <tr style="border-bottom:1px solid #e2e8f0; background:#f8fafc;">
              <td style="padding:3.5px 7px; font-weight:700; color:#0f172a;">Engine 4: Workshop &amp; Overhauls</td>
              <td style="padding:3.5px 7px; font-weight:600; color:#b45309;">Modules 17 to 20</td>
              <td style="padding:3.5px 7px;">Job cards, pneumatic clutch retrofit orders, power trials, site handover certificates.</td>
            </tr>
            <tr style="border-bottom:1px solid #e2e8f0; background:#ffffff;">
              <td style="padding:3.5px 7px; font-weight:700; color:#0f172a;">Engine 5: Accounting &amp; GST</td>
              <td style="padding:3.5px 7px; font-weight:600; color:#b45309;">Modules 21 to 25</td>
              <td style="padding:3.5px 7px;">GST tax invoices, client payment aging, wire remittances, monthly gross profit.</td>
            </tr>
            <tr style="border-bottom:1px solid #e2e8f0; background:#f8fafc;">
              <td style="padding:3.5px 7px; font-weight:700; color:#0f172a;">Engine 6: Sales Force &amp; Service</td>
              <td style="padding:3.5px 7px; font-weight:600; color:#b45309;">Modules 26 to 30</td>
              <td style="padding:3.5px 7px;">Field visit logs, quote follow-ups, AMC maintenance contracts, breakdown tickets.</td>
            </tr>
            <tr style="background:#ffffff;">
              <td style="padding:3.5px 7px; font-weight:700; color:#0f172a;">Engine 7: Executive Intelligence</td>
              <td style="padding:3.5px 7px; font-weight:600; color:#b45309;">Modules 31 to 33</td>
              <td style="padding:3.5px 7px;">Staff role permissions, daily automated cloud backups, MD real-time command desk.</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Pre-Commencement Status Confirmation -->
      <div style="background:#fffbeb; border:1.5px solid #f59e0b; border-radius:7px; padding:7px 12px; margin-bottom:7px;">
        <div style="font-size:9.0pt; font-weight:800; color:#b45309; text-transform:uppercase; margin-bottom:2px;">
          &#9888; Scope Status: Planned Architecture &bull; Zero Lines Built
        </div>
        <p style="font-size:8.6pt; line-height:1.42; color:#78350f;">
          The 33 modules detailed on the subsequent 17 pages represent the complete operational roadmap for OMPI India LLP. Each module is specified with its intended user role, operational workflow, commercial risk prevention, and key management features. Work has not yet begun.
        </p>
      </div>

      <!-- Key Operational Highlights Box -->
      <div style="background:#ffffff; border:1.5px solid #cbd5e1; border-radius:7px; padding:7px 12px; margin-bottom:7px;">
        <div style="font-size:8.8pt; font-weight:800; color:#0f172a; text-transform:uppercase; margin-bottom:4px;">
          Core Business Advantages to be Delivered Upon Implementation
        </div>
        <div style="display:grid; grid-template-columns:1fr 1fr; gap:8px; font-size:8.3pt; line-height:1.38; color:#334155;">
          <div style="background:#f8fafc; padding:6px 9px; border-radius:4px; border-left:3px solid #0284c7;">
            <strong>Real-Time Godown Reservation Lock:</strong> Stops accidental double-selling of high-demand presses and clutch models across simultaneous sales calls.
          </div>
          <div style="background:#f8fafc; padding:6px 9px; border-radius:4px; border-left:3px solid #0284c7;">
            <strong>Landed Import Margin Protection:</strong> Calculates exact landed cost in Indian Rupees including Euro conversion, sea freight, customs duty, and port handling.
          </div>
          <div style="background:#f8fafc; padding:6px 9px; border-radius:4px; border-left:3px solid #0284c7;">
            <strong>100% Clean GST Tax Invoices:</strong> Automatically validates client 15-digit GSTIN, ensuring zero input tax credit disputes or delayed client payments.
          </div>
          <div style="background:#f8fafc; padding:6px 9px; border-radius:4px; border-left:3px solid #0284c7;">
            <strong>Executive 360-Degree Control:</strong> Provides Mr. Vinit Dalal with real-time operational visibility over sales leads, godown inventory, and cash collections.
          </div>
        </div>
      </div>

      <!-- Confidentiality Warning Banner -->
      <div style="border:1.5px solid #dc2626; background:#fef2f2; border-radius:7px; padding:6px 12px;">
        <p style="font-size:8.3pt; line-height:1.38; color:#991b1b;">
          <strong>&#128274; STRICT CONFIDENTIALITY NOTICE:</strong> This architectural blueprint contains proprietary commercial operating systems and confidential pricing logic. External distribution is strictly forbidden.
        </p>
      </div>
    </div>
    {make_footer(14)}
  </div>
"""

    # PAGES 15 TO 30: OMPI MODULES 01 TO 32 (2 PER PAGE)
    for i in range(16):
        page_num = i + 15
        m1 = ompi_modules[i * 2]
        m2 = ompi_modules[i * 2 + 1]

        html += f"""
  <div class="page">
    <div class="page-content">
      {make_header("SYSTEM 2: OMPI INDUSTRIAL OPERATIONS &amp; ERP SUITE &bull; PROPOSED SCOPE")}

      <div class="section-header">
        <span class="section-title">OMPI Management Engines Scope &bull; Modules {i*2+1:02d} &amp; {i*2+2:02d} of 33 (To Be Engineered)</span>
        <span class="section-tag">{m1['engine'].split(':')[0]}</span>
      </div>

      {render_card(m1, is_route=False)}
      {render_card(m2, is_route=False)}
    </div>
    {make_footer(page_num)}
  </div>
"""

    # PAGE 31: MODULE 33 (MD DASHBOARD) + STAFF OPERATIONS PORTALS
    m33 = ompi_modules[32]
    html += f"""
  <div class="page">
    <div class="page-content">
      {make_header("SYSTEM 2: EXECUTIVE MANAGEMENT &amp; CONTROL CONSOLES &bull; PROPOSED SCOPE")}

      <div class="section-header">
        <span class="section-title">OMPI Management Engine &bull; Module 33 of 33 &amp; Control Desks (To Be Engineered)</span>
        <span class="section-tag">Executive Business Control</span>
      </div>

      {render_card(m33, is_route=False)}

      <!-- Operations Consoles Summary Box -->
      <div class="card-box" style="margin-top:2px;">
        <div class="card-header">
          <div>
            <span class="badge-id">PORTALS</span>
            <span class="card-title">Staff Operations &amp; Departmental Control Workspaces</span>
            <span class="card-status">&#9675; TO BE BUILT: SYSTEM 2</span>
          </div>
          <div style="font-family:'JetBrains Mono',monospace; font-size:7.8pt; color:#b45309; background:#fffbeb; padding:2px 8px; border:1px solid #fef3c7; border-radius:3px;">
            Departmental Consoles
          </div>
        </div>
        <div class="meta-row">
          <div><strong>Primary Users:</strong> Sales Reps, Warehouse Storekeepers, Workshop Engineers, Senior Accountants</div>
          <div><strong>Security Governance:</strong> Strict Role-Based Data Isolation</div>
        </div>
        <div style="display:grid; grid-template-columns:1fr 1fr; gap:9px; font-size:8.6pt; line-height:1.4; color:#334155; margin-bottom:7px;">
          <div style="background:#f8fafc; padding:6px 9px; border-radius:4px; border-left:3px solid #d97706;">
            <strong>1. Sales Workspace:</strong> Lead inbox, 60-second quote generator, customer follow-up alerts, and WhatsApp message sender.
          </div>
          <div style="background:#f8fafc; padding:6px 9px; border-radius:4px; border-left:3px solid #d97706;">
            <strong>2. Godown Console:</strong> Pune live stock tracker, shelf coordinates, delivery challans, and container tracking.
          </div>
          <div style="background:#f8fafc; padding:6px 9px; border-radius:4px; border-left:3px solid #d97706;">
            <strong>3. Accounts Desk:</strong> GST tax billing, customer payment aging, overseas wire records, and monthly profit summary.
          </div>
          <div style="background:#f8fafc; padding:6px 9px; border-radius:4px; border-left:3px solid #d97706;">
            <strong>4. Workshop Portal:</strong> Press overhaul job cards, clutch retrofit work orders, power test sheets, and handover sign-offs.
          </div>
        </div>
        <div class="feature-strip" style="margin-bottom:7px;">
          <strong>Key Management Feature:</strong> Total role-based permission control ensuring employees only access tools essential for their daily duties.
        </div>
        <div style="display:flex; justify-content:space-between; align-items:center; background:#f8fafc; border:1px solid #e2e8f0; border-radius:4px; padding:4px 10px; font-size:7.8pt; color:#475569;">
          <div><strong>Enterprise Security Standard:</strong> Encrypted Database Vault &bull; Tamper-Proof Financial Ledger</div>
          <div><strong>Implementation Phase:</strong> Phase 2 Rollout upon Executive Sign-Off</div>
        </div>
      </div>
    </div>
    {make_footer(31)}
  </div>
"""

    # PAGE 32: THE PROPOSED BUYER JOURNEY, ROADMAP & SIGN-OFF
    html += f"""
  <div class="page">
    <div class="page-content">
      {make_header("SYSTEM INTEGRATION &bull; PROPOSED 6-STEP PROCESS &amp; KICKOFF SIGN-OFF")}

      <div class="section-header">
        <span class="section-title">How Both Systems Will Work Together &bull; From Customer Inquiry to Delivery</span>
        <span class="section-tag">Proposed Commercial Workflow</span>
      </div>

      <!-- 6-Step Workflow Box -->
      <div style="background:#ffffff; border:1.5px solid #cbd5e1; border-radius:7px; padding:7px 12px; margin-bottom:7px;">
        <div style="font-size:9.2pt; font-weight:800; color:#0f172a; text-transform:uppercase; margin-bottom:6px; border-bottom:1.5px solid #f1f5f9; padding-bottom:3px;">
          The Seamless 6-Step Business Process to be Engineered (Inquiry to Payment)
        </div>
        <div style="display:grid; grid-template-columns:1fr 1fr; gap:9px; font-size:8.6pt; line-height:1.4; color:#334155;">
          <div style="background:#f8fafc; padding:7px 10px; border-radius:4px; border-left:3.5px solid #d97706;">
            <strong>Step 1: Customer Inquires Online</strong><br>
            A plant head finds a 1,600T press on the website and clicks the WhatsApp inquiry button with his company details.
          </div>
          <div style="background:#f8fafc; padding:7px 10px; border-radius:4px; border-left:3.5px solid #d97706;">
            <strong>Step 2: Instant Technical Sizing</strong><br>
            The system automatically matches the press with the exact Italian OMPI pneumatic clutch required for the job.
          </div>
          <div style="background:#f8fafc; padding:7px 10px; border-radius:4px; border-left:3.5px solid #d97706;">
            <strong>Step 3: 60-Second Quotation Sent</strong><br>
            An official proposal PDF with machine photos, specs, and price is sent directly to the customer's WhatsApp.
          </div>
          <div style="background:#f8fafc; padding:7px 10px; border-radius:4px; border-left:3.5px solid #d97706;">
            <strong>Step 4: Machine Locked in Godown</strong><br>
            Once the client confirms, the press is marked 'Under Commercial Hold' so it cannot be sold to anyone else.
          </div>
          <div style="background:#f8fafc; padding:7px 10px; border-radius:4px; border-left:3.5px solid #d97706;">
            <strong>Step 5: Pune Workshop Overhaul &amp; Rigging</strong><br>
            The machine undergoes live power trials, foundation check, and is dispatched on low-bed trailers to the buyer's factory.
          </div>
          <div style="background:#f8fafc; padding:7px 10px; border-radius:4px; border-left:3.5px solid #d97706;">
            <strong>Step 6: Official GST Invoicing &amp; Backup</strong><br>
            Clean tax bills are issued, GST records are updated for your accountant, and all transaction history is securely saved.
          </div>
        </div>
      </div>

      <!-- Implementation Summary & Phasing Table -->
      <div style="background:#f8fafc; border:1.5px solid #cbd5e1; border-radius:7px; padding:10px 14px; margin-bottom:11px;">
        <div style="font-size:9.0pt; font-weight:800; color:#0f172a; text-transform:uppercase; margin-bottom:5px;">
          Commercial Phasing &amp; Proposed Delivery Milestones
        </div>
        <table style="width:100%; border-collapse:collapse; font-size:8.4pt; line-height:1.38; color:#334155;">
          <thead>
            <tr style="background:#0f172a; color:#ffffff; text-align:left;">
              <th style="padding:5px 8px;">Milestone Phase</th>
              <th style="padding:5px 8px;">Proposed Scope of Delivery</th>
              <th style="padding:5px 8px;">Timeline &amp; Status</th>
            </tr>
          </thead>
          <tbody>
            <tr style="border-bottom:1px solid #e2e8f0; background:#ffffff;">
              <td style="padding:5px 8px; font-weight:700;">Phase 1 (Kickoff Scope)</td>
              <td style="padding:5px 8px;">Dalal 24 Public Pages &bull; Staff Admin Portal &bull; WhatsApp Lead Routing &bull; Quoting Tools</td>
              <td style="padding:5px 8px; font-weight:700; color:#b45309;">TO COMMENCE UPON SIGN-OFF</td>
            </tr>
            <tr style="border-bottom:1px solid #e2e8f0; background:#f8fafc;">
              <td style="padding:5px 8px; font-weight:700;">Phase 2 (OMPI Core ERP)</td>
              <td style="padding:5px 8px;">OMPI Customer Master &bull; Italian SKU Catalog &bull; Landed Pricing &bull; Godown Stock Tracker</td>
              <td style="padding:5px 8px; font-weight:700; color:#475569;">MONTH 1-2 SPRINT ROADMAP</td>
            </tr>
            <tr style="background:#ffffff;">
              <td style="padding:5px 8px; font-weight:700;">Phase 3 (Enterprise Control)</td>
              <td style="padding:5px 8px;">Workshop Overhaul Job Cards &bull; GST Invoicing &bull; Port Demurrage Shield &bull; MD Command Desk</td>
              <td style="padding:5px 8px; font-weight:700; color:#475569;">MONTH 3-4 SPRINT ROADMAP</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Formal Authorization & Commencement Terms Box -->
      <div style="background:#ffffff; border:1.5px solid #0f172a; border-radius:7px; padding:10px 14px; margin-bottom:10px;">
        <div style="font-size:8.8pt; font-weight:800; color:#0f172a; text-transform:uppercase; margin-bottom:4px;">
          Formal Commencement Authorization &amp; Quality Acceptance Terms
        </div>
        <p style="font-size:8.3pt; line-height:1.42; color:#334155;">
          By formal execution below, executive leadership authorizes the commencement of Milestone Phase 1. Development will strictly adhere to the operational specifications detailed across this 57-unit master document. Each phase requires structured shop floor acceptance testing prior to commercial release.
        </p>
      </div>

      <!-- Non-Disclosure Confirmation & Executive Sign-Off -->
      <div style="border:1.5px solid #e11d48; background:#fff1f2; border-radius:7px; padding:9px 14px; margin-bottom:10px;">
        <div style="font-size:8.6pt; font-weight:800; color:#9f1239; text-transform:uppercase; margin-bottom:2px;">
          &#128274; Confidentiality &amp; Proprietary Architecture Covenant
        </div>
        <p style="font-size:8.2pt; line-height:1.38; color:#4c0519;">
          This master specification represents the proprietary intellectual property and proposed operational architecture of Dalal Machine Tools Agency Pvt. Ltd. and OMPI India LLP. External sharing, copying, forwarding, or unauthorized reproduction without prior written approval is strictly prohibited by law.
        </p>
      </div>

      <!-- Signatures Grid -->
      <div style="display:grid; grid-template-columns:1fr 1fr; gap:16px; border-top:1.5px solid #0f172a; padding-top:10px;">
        <div style="font-size:8.5pt; line-height:1.4; color:#334155;">
          <strong>Accepted &amp; Approved to Commence Work:</strong><br><br>
          __________________________________________<br>
          <strong>Mr. Vinit Dalal</strong> &bull; Managing Director / Partner<br>
          <span style="font-size:7.8pt; color:#64748b;">Dalal Machine Tools Agency Pvt. Ltd. &amp; OMPI India LLP</span>
        </div>
        <div style="font-size:8.5pt; line-height:1.4; color:#334155; text-align:right;">
          <strong>Submitted by Principal Software Consultant:</strong><br><br>
          __________________________________________<br>
          <strong>Suyash Shinde</strong> &bull; Principal Software Consultant<br>
          <span style="font-size:7.8pt; color:#64748b;">Pimpri, Pune, Maharashtra, India</span>
        </div>
      </div>
    </div>
    {make_footer(32)}
  </div>
</body>
</html>
"""
    return html

# Generate HTML
html_content = build_html_document()
output_html = "DALAL_AND_OMPI_57_PAGES_AND_MODULES_MASTER_SPECIFICATION.html"
with open(output_html, "w", encoding="utf-8") as f:
    f.write(html_content)
print(f"Generated HTML: {output_html} ({os.path.getsize(output_html):,} bytes)")

# Also write to simple guide name
simple_html = "DALAL_AND_OMPI_57_EXECUTIVE_CLIENT_GUIDE_SIMPLE.html"
with open(simple_html, "w", encoding="utf-8") as f:
    f.write(html_content)

# Render to PDF via Edge Headless
edge = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
pdf_path = os.path.abspath('DALAL_AND_OMPI_57_PAGES_AND_MODULES_MASTER_SPECIFICATION.pdf')
simple_pdf = os.path.abspath('DALAL_AND_OMPI_57_EXECUTIVE_CLIENT_GUIDE_SIMPLE.pdf')
url = f'file:///{os.path.abspath(output_html).replace("\\", "/")}'

cmd = [
    edge,
    '--headless',
    '--disable-gpu',
    f'--print-to-pdf={pdf_path}',
    '--no-pdf-header-footer',
    url
]
print(f"Rendering PDF via Edge...")
subprocess.run(cmd, capture_output=True)

if os.path.exists(pdf_path):
    print(f"PDF Generated: {pdf_path} ({os.path.getsize(pdf_path):,} bytes)")
    shutil.copyfile(pdf_path, simple_pdf)
    
    # Copy to artifact folder
    artifact_dir = r'C:\Users\91940\.gemini\antigravity\brain\75a30f5c-ccbc-43b7-9b59-6c8c1ab99b62'
    shutil.copyfile(pdf_path, os.path.join(artifact_dir, 'DALAL_AND_OMPI_57_PAGES_AND_MODULES_MASTER_SPECIFICATION.pdf'))
    shutil.copyfile(pdf_path, os.path.join(artifact_dir, 'DALAL_AND_OMPI_57_EXECUTIVE_CLIENT_GUIDE_SIMPLE.pdf'))
    shutil.copyfile(simple_html, os.path.join(artifact_dir, 'DALAL_AND_OMPI_57_EXECUTIVE_CLIENT_GUIDE_SIMPLE.html'))
    print("Copied all files to artifact directory.")

    # Audit all 32 pages with PyMuPDF
    doc = pymupdf.open(pdf_path)
    print(f"--- PyMuPDF Audit: Total Pages = {len(doc)} ---")
    for i, p in enumerate(doc):
        blocks = p.get_text('blocks')
        content_blocks = [b for b in blocks if b[3] < 790]
        max_y = max([b[3] for b in content_blocks]) if content_blocks else 0
        footer_block = [b for b in blocks if b[3] >= 790]
        min_footer_y = min([b[1] for b in footer_block]) if footer_block else 800
        gap = min_footer_y - max_y
        status = "OK (PERFECT)" if 40 <= gap <= 130 else ("WARNING: TOO EMPTY" if gap > 130 else "CRITICAL: OVERFLOW RISK")
        print(f"Page {i+1:02d}: content y={max_y:5.1f} | footer y={min_footer_y:5.1f} | gap={gap:5.1f}pt -> {status}")
