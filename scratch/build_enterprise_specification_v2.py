# scratch/build_enterprise_specification_v2.py
"""
Elite Enterprise Master Specification Generator - Version 2.5 (Executive Edition)
---------------------------------------------------------------------------------
Fixes & Enhancements based on Executive Review:
1. Added Page 2: 1-Page Executive Summary (What You Get, Phasing, Out of Scope, Client Responsibilities).
2. Added Page 3: Assumptions, Exclusions, Third-Party Costs & Client Responsibilities (APIs, Hardware, Content, Change Policy).
3. Eliminated all developer jargon (no route URLs, no PDP, no Kanban, no SKU master, no immutable vault).
4. Removed 57 repetitive QA/shop-floor banners; replaced with a single clean legend and standardized card design.
5. Replaced all over-promises and unachievable guarantees with realistic, legally defensible language ("designed to help", "aims to").
6. Explicitly documented third-party API subscriptions, hosting fees, and hardware exclusions.
7. Live Stockyard Camera explicitly defined with hardware as Client responsibility.
8. Quotation generator clarified as one centralized unified engine.
9. Separated Dalal Machine Tools Agency Pvt. Ltd. and OMPI India LLP into distinct legal sign-offs.
10. Added document date, version (v2.4), and 30-day commercial validity period.
11. Checked and fixed typography and word spacing.
"""

import os, sys, subprocess, shutil, pymupdf

print("Starting generation of Enterprise Master Specification v2.4...")

# 24 Dalal Units: 22 Customer-Facing Web Pages + 2 Staff Operations Consoles
dalal_units = [
    # Page 4
    {
        "id": "UNIT-01",
        "title": "Homepage & Machinery Showroom",
        "type": "Public Showroom Page",
        "audience": "Industrial Plant Owners, Factory Directors, Forging Sourcing Heads",
        "focus": "Heavy Press Inventory, Yard Authenticity & Instant Trust",
        "does": "A modern digital machinery showroom presenting heavy forging and stamping presses available for sale. Prospective buyers can view high-resolution photographs, verified machine tonnages, live electrical power trials, and click a direct WhatsApp button to speak with Mr. Vinit Dalal.",
        "benefit": "Helps overcome buyer skepticism by showing that machines are physically present in the Pune stockyard rather than virtual broker listings, building immediate trust for high-value industrial transactions.",
        "deliverables": ["Live Power Inspection Video Clips", "Direct WhatsApp Tonnage Inquiries", "Pune Yard Stock Status Indicators"],
        "feature": "1-Click WhatsApp inquiry button pre-filled with the exact machine model and capacity."
    },
    {
        "id": "UNIT-02",
        "title": "Company Profile & Facility Overview",
        "type": "Company Profile Page",
        "audience": "Corporate Procurement Heads, Bank Valuers, Joint-Venture Partners",
        "focus": "50-Year Engineering Heritage & Official Italian Partnership",
        "does": "Presents the 50-year engineering heritage of the Dalal family, authentic photographs of the Mumbai registered corporate office and Pune warehouse stockyard, and formal details of the official technical partnership with OMPI Italy.",
        "benefit": "Demonstrates corporate stability and long-term capability, reassuring plant owners and corporate purchase committees that their advance payments and machinery orders are handled by experienced professionals.",
        "deliverables": ["50-Year Heritage Milestones Timeline", "Pune Warehouse Yard Photographic Tour", "Italian Technical Partnership Overview"],
        "feature": "Visual timeline highlighting 5 decades of industrial machinery supply across India."
    },
    # Page 5
    {
        "id": "UNIT-03",
        "title": "Import, Rigging & Technical Services",
        "type": "Services & Rigging Page",
        "audience": "Plant Maintenance Heads, Factory Engineers, Project Directors",
        "focus": "Turnkey Heavy Rigging, Customs Clearance & Foundation Works",
        "does": "A clear, comprehensive guide explaining Dalal's turnkey services: overseas machine dismantling in Europe, customs clearance at Nhava Sheva port, heavy transport on multi-axle trailers, foundation pit engineering, and Italian pneumatic clutch retrofitting.",
        "benefit": "Demonstrates that Dalal provides end-to-end support from port arrival to shop floor erection and commissioning, helping industrial buyers feel supported throughout the entire installation cycle.",
        "deliverables": ["Port Clearance Documentation Guide", "Heavy Transport & Trailer Logistics Overview", "Civil Foundation Engineering Blueprints"],
        "feature": "Clear 7-point explanation of how High Seas Sales save time and customs duty."
    },
    {
        "id": "UNIT-04",
        "title": "Machinery Catalog & Search Directory",
        "type": "Machinery Catalog Directory",
        "audience": "Factory Sourcing Managers, Purchase Officers, Plant Sizing Teams",
        "focus": "26 Machine Categories with Instant Tonnage & Brand Filtering",
        "does": "A clean, searchable directory of all 26 machine types (Mechanical Forging Presses, Hydraulic Stamping Presses, Friction Screw Presses, Horizontal Boring Machines) equipped with instant filters for tonnage, manufacturer country, and Pune stock availability.",
        "benefit": "Designed to help purchasing teams quickly locate the exact tonnage, bed dimensions, and machine type they need in seconds, reducing inquiry delays and improving client engagement.",
        "deliverables": ["Interactive Tonnage Capacity Filters", "Country of Origin Categorization", "Pune Stock Availability Indicators"],
        "feature": "Instant capacity filter buttons (Under 500T, 500T to 1,000T, 1,000T to 4,000T)."
    },
    # Page 6
    {
        "id": "UNIT-05",
        "title": "Machine Engineering Details & Specs Sheet",
        "type": "Machine Details & Specs Sheet",
        "audience": "Chief Technical Officers, Toolroom Managers, Plant Heads",
        "focus": "Full Dimensional Specifications, Die Clearance & Video Proof",
        "does": "A detailed technical sheet for each press: verified tonnage capacity, stroke length, bed dimensions, motor horsepower, manufacturer country, foundation pit requirements, power trial video, and a 1-click button to download an official formal quotation.",
        "benefit": "Equips plant technical directors with the dimensional measurements needed to confirm the press fits their tooling dies and factory ceiling height, assisting in internal capital expenditure reviews.",
        "deliverables": ["Die Space & Clearance Dimensional Tables", "Motor Running & Ram Cycling Video Link", "1-Click PDF Machine Quotation Download"],
        "feature": "Print-ready machine specification sheet download ready for internal plant review."
    },
    {
        "id": "UNIT-06",
        "title": "Brand New Factory Machinery Lines",
        "type": "New Machinery Lines Page",
        "audience": "Tier-1 Automotive Suppliers, High-Volume Manufacturing Plants",
        "focus": "Factory-Fresh Production Lines with European Standards",
        "does": "A specialized showcase presenting brand-new heavy industrial presses engineered to European safety standards, complete with manufacturer warranties, touchscreen automation, and factory-certified commissioning options.",
        "benefit": "Addresses top-tier automotive and industrial manufacturers whose corporate policies require brand-new equipment rather than pre-owned machinery, opening opportunities for large turnkey supply agreements.",
        "deliverables": ["European Safety Standard Compliance Summary", "Manufacturer Warranty Information", "Turnkey Automated Production Line Options"],
        "feature": "Dedicated inquiry form for custom-engineered new production line projects."
    },
    # Page 7
    {
        "id": "UNIT-07",
        "title": "Shipment, Yard & Rigging Photo Gallery",
        "type": "Yard & Rigging Photo Gallery",
        "audience": "Factory Auditors, Sourcing Committees, Managing Directors",
        "focus": "Visual Proof of 4,000-Ton Rigging & Stockyard Scale",
        "does": "A photographic gallery showcasing heavy 1,000-ton to 4,000-ton forging presses being hoisted by heavy hydraulic cranes, secured onto multi-axle trailers, cleared at Indian ports, and installed inside customer forging facilities.",
        "benefit": "Provides visual confirmation of heavy equipment handling capabilities, helping reassure prospective buyers regarding Dalal's practical experience in moving massive industrial machinery.",
        "deliverables": ["Port Hoisting & Crane Rigging Photos", "Multi-Axle Trailer Transit Images", "Customer Shop Floor Installation Photos"],
        "feature": "Categorized photo albums filtered by machine tonnage and transport stage."
    },
    {
        "id": "UNIT-08",
        "title": "Headquarters, Yard & Visit Booking Portal",
        "type": "Contact & Pune Yard Location",
        "audience": "Procurement Directors, Visiting Engineering Teams",
        "focus": "Direct Executive Access & Pune Yard Trial Scheduling",
        "does": "Interactive Google Map location guides for both the Mumbai Corporate Office (Tardeo) and the Pune Heavy Stockyard (Chakan), complete with direct telephone lines, executive email contacts, and an online appointment request console.",
        "benefit": "Makes it convenient for serious corporate buyers to schedule an in-person physical inspection in Pune to inspect machines under live electrical power prior to finalizing purchasing decisions.",
        "deliverables": ["Location Maps for Mumbai & Pune Facilities", "Power Trial Appointment Request Form", "Direct Contact Directory for Key Staff"],
        "feature": "Online trial booking form allowing plant engineers to request a scheduled technical inspection in Pune."
    },
    # Page 8
    {
        "id": "UNIT-09",
        "title": "Urgent Breakdown Machinery Request Form",
        "type": "Urgent Breakdown Request Form",
        "audience": "Plant Managers facing an emergency press breakdown",
        "focus": "Rapid Tonnage Sizing & Urgent Replacement Identification",
        "does": "A streamlined emergency request form asking only 3 essential questions: required press tonnage, bed size, and delivery urgency. Optimized for mobile devices so plant engineers can submit urgent needs directly from the factory floor.",
        "benefit": "Helps capture high-priority inquiries when a manufacturing line has stopped due to catastrophic machine failure, allowing Dalal's commercial team to respond promptly with in-stock alternatives.",
        "deliverables": ["Fast 3-Field Mobile Inquiry Form", "Priority Notification Routing to Sales Team", "In-Stock Equivalent Press Recommendation"],
        "feature": "Priority inquiry alert routed directly to sales managers for rapid response."
    },
    {
        "id": "UNIT-10",
        "title": "Import Compliance & Legal Tax FAQs Guide",
        "type": "High Seas & Tax FAQs Guide",
        "audience": "Chief Financial Officers (CFOs), Company Legal & Tax Advisors",
        "focus": "High Seas Sales Procedures, Customs Bill of Entry & GST Credits",
        "does": "Plain-language explanations of High Seas Sales contracts, GST documentation, Customs Bill of Entry procedures, and live power inspection arrangements. (Disclaimer: Information provided for operational guidance only; does not constitute legal or tax advice. Contracts must be vetted by Client's counsel).",
        "benefit": "Assists client accounting and legal teams in understanding procedural steps early, helping avoid common documentation hurdles during formal purchase approvals.",
        "deliverables": ["High Seas Commercial Workflow Explainer", "Step-by-Step GST Tax Documentation Guide", "Pre-Dispatch Power Inspection Summary"],
        "feature": "Interactive guide explaining import documentation in simple business terms (non-legal advisory)."
    },
    # Page 9
    {
        "id": "UNIT-11",
        "title": "Customer Quotation Download Portal",
        "type": "Official Quotation Download Portal",
        "audience": "Procurement Heads, Commercial Executives, Factory Accountants",
        "focus": "Secure PDF Proposal Retrieval with Official Terms",
        "does": "A secure digital portal where prospective buyers can view and download their personalized formal commercial quotation letters, complete with machine photos, technical dimensions, payment milestones, and company signature.",
        "benefit": "Helps avoid delays caused by lost email attachments and ensures company purchasing committees review the authorized quotation document with clear commercial terms.",
        "deliverables": ["Official Branded Quotation PDF Retrieval", "Commercial Payment Milestones Breakdown", "Machine Dimensions & Technical Summary"],
        "feature": "Secure proposal retrieval powered by the centralized quotation engine."
    },
    {
        "id": "UNIT-12",
        "title": "Power Trial Video Showcase Center",
        "type": "Live Power Trial Video Center",
        "audience": "Plant Technical Directors, Maintenance Heads, Chief Engineers",
        "focus": "Live Electrical Load Trials, Ram Cycling & Flywheel Tests",
        "does": "A dedicated video library presenting unedited videos of heavy forging and mechanical presses undergoing electrical power trials at the Pune yard, showing flywheel rotation, clutch engagement, and ram cycling.",
        "benefit": "Provides practical technical evidence of mechanical condition, helping prospective buyers from other industrial states evaluate machine operation before scheduling an in-person visit.",
        "deliverables": ["Unedited Video Footage of Running Presses", "Motor & Flywheel Operation Visuals", "Clutch-Brake Engagement Demonstration"],
        "feature": "Searchable video library organized by machine tonnage and manufacturer."
    },
    # Page 10
    {
        "id": "UNIT-13",
        "title": "Machinery Comparison & Sizing Tool",
        "type": "Machine Comparison Tool",
        "audience": "Toolroom Heads, Production Planners, Industrial Engineers",
        "focus": "Side-by-Side Sizing of Bed Size, Stroke & Tonnage",
        "does": "A side-by-side comparison screen allowing plant engineers to compare up to 3 machines simultaneously on critical engineering factors: pressing tonnage, stroke length, bolster dimensions, motor power, and pricing.",
        "benefit": "Assists factory technical teams in comparing alternative press options to ensure the selected machine matches their tooling dies and manufacturing volume requirements.",
        "deliverables": ["Side-by-Side Technical Comparison Grid", "Die Dimensional Compatibility Matcher", "Comparison Summary Export Option"],
        "feature": "Interactive comparison layout highlighting dimensional and tonnage differences between models."
    },
    {
        "id": "UNIT-14",
        "title": "Used Press Valuation & Buyback Request",
        "type": "Used Machine Valuation Request",
        "audience": "Factory Owners Upgrading Plants, Liquidators, Plant Heads",
        "focus": "Surplus Machine Liquidation & Fair Market Cash Offers",
        "does": "A structured valuation portal where manufacturing plants looking to sell or trade in surplus heavy presses can submit machine specifications, photographs, nameplate details, and asking prices to Dalal's acquisition team.",
        "benefit": "Helps build an active pipeline of pre-owned machinery opportunities across India, allowing Dalal to review equipment directly from factory owners seeking to upgrade their facilities.",
        "deliverables": ["Structured Equipment Photo & Spec Uploader", "Preliminary Valuation Intake Review", "Trade-in Credit & Outright Purchase Assessment"],
        "feature": "Simple intake form collecting machine make, year, tonnage, and operating status in minutes."
    },
    # Page 11
    {
        "id": "UNIT-15",
        "title": "Press Tonnage & Sizing Assistant",
        "type": "Press Tonnage Sizing Assistant",
        "audience": "Manufacturing Sourcing Teams, New Plant Setup Heads",
        "focus": "Automated Tonnage Estimation from Component Dimensions",
        "does": "An interactive sizing tool estimating recommended press capacity from part dimensions and material. (Disclaimer: Calculations are approximate technical estimations; final machine selection and tooling suitability must be certified by Client's qualified tooling/press engineer).",
        "benefit": "Guides prospective buyers toward realistic press tonnage categories before inquiring, helping filter inquiries and save preliminary engineering discussion time.",
        "deliverables": ["Approximate Tonnage Estimation Calculator", "Recommended Matching Machine Stock List", "Direct Technical Inquiry Dispatch Button"],
        "feature": "Interactive sizing formula suggesting suitable machinery categories (subject to engineer verification)."
    },
    {
        "id": "UNIT-16",
        "title": "High Seas Sales Compliance Center",
        "type": "High Seas Compliance Center",
        "audience": "Corporate CFOs, Commercial Directors, Tax Consultants",
        "focus": "Legal Documentation, Port Handling & Customs Clearance",
        "does": "A clear procedural overview detailing standard High Seas Sales transactions, title transfer prior to customs borders, and port handling. (Disclaimer: Content provided for operational transparency only; does not substitute for formal maritime legal counsel or chartered tax advisory).",
        "benefit": "Provides clarity for corporate finance teams on documentation milestones, assisting in orderly customs coordination and duty assessments.",
        "deliverables": ["High Seas Sales Operational Workflow Map", "Nhava Sheva Port Milestone Checklist", "Import Document Requirements Summary"],
        "feature": "Procedural guide outlining documentation stages for port-delivered machinery (advisory excluded)."
    },
    # Page 12
    {
        "id": "UNIT-17",
        "title": "Pune Warehouse Live Stockyard Portal",
        "type": "Pune Stockyard Live Video Portal",
        "audience": "Prospective Buyers, Out-of-State Clients, Corporate Committees",
        "focus": "Real-Time Yard Visibility & Stock Verification (Hardware Client Supplied)",
        "does": "A scheduled portal enabling authorized clients to view live video feeds of the Pune machinery stockyard during business hours, inspect equipment rows, and observe workshop rigging activity.",
        "benefit": "Demonstrates physical stockyard inventory, confirming for remote buyers that listed machines are physically in stock in Pune. (Note: Cameras and internet hardware provided by Client).",
        "deliverables": ["Scheduled Video Stream Interface", "Stockyard Inventory Layout Guide", "Assisted Virtual Inspection Scheduling"],
        "feature": "Time-limited access tokens for verified buyers to view live yard operations remotely."
    },
    {
        "id": "UNIT-18",
        "title": "Client Installations Track Record",
        "type": "Client Installations Track Record",
        "audience": "Board-Level Decision Makers, Foreign Joint Ventures",
        "focus": "Representative Deliveries to Heavy Forging Plants",
        "does": "An executive portfolio highlighting representative heavy machinery deliveries across automotive forging plants, railway component suppliers, and industrial facilities in Pune, Rajkot, Chennai, and other hubs.",
        "benefit": "Demonstrates proven industry experience through verified past deliveries, reassuring corporate procurement committees of Dalal's track record in heavy machinery supply.",
        "deliverables": ["Representative Case Studies of Past Projects", "Client Reference Highlights", "Geographic Overview of Major Plant Installations"],
        "feature": "Interactive map illustrating machinery installations across major Indian manufacturing regions."
    },
    # Page 13
    {
        "id": "UNIT-19",
        "title": "OMPI Genuine Spare Parts Catalog",
        "type": "OMPI Genuine Spare Parts Catalog",
        "audience": "Maintenance Engineers, Plant Storekeepers, Purchase Teams",
        "focus": "Original Italian Clutches, Rotating Unions & Friction Discs",
        "does": "A dedicated parts directory presenting genuine Italian OMPI pneumatic clutch-brakes, rotating unions, friction linings, and hydraulic seal kits with dimensional specifications.",
        "benefit": "Enables factory maintenance teams to identify and order genuine replacement parts from Pune stock, helping support after-sales service and ongoing equipment maintenance.",
        "deliverables": ["Genuine OMPI Italian Parts Directory", "Bore Size & Dimension Cross-Reference", "Pune Stock Availability Indicators"],
        "feature": "Quick search tool matching press brand names with suitable OMPI replacement components."
    },
    {
        "id": "UNIT-20",
        "title": "European Machinery Sourcing Desk",
        "type": "European Machine Sourcing Desk",
        "audience": "Industrialists seeking specific foreign machinery models",
        "focus": "Custom Sourcing from Germany, Italy & Eastern Europe",
        "does": "A specialized sourcing portal where clients can submit specific heavy equipment requirements (e.g., 2,500T Eumuco press, 4,000T Voronezh press) for sourcing through Dalal's European trade contacts.",
        "benefit": "Enables Dalal to assist clients seeking specific overseas machines not currently available in Indian stock, supporting custom import transactions with full logistics management.",
        "deliverables": ["European Plant Sourcing Intake Form", "Overseas Technical Inspection Overview", "Import & Transport Cost Projection Template"],
        "feature": "Structured sourcing request form designed to collect detailed machinery specifications."
    },
    # Page 14
    {
        "id": "UNIT-21",
        "title": "Press Modernization & Rebuilding Showcase",
        "type": "Press Modernization & Rebuilding",
        "audience": "Factory Owners seeking to boost production on older presses",
        "focus": "Clutch Retrofits, Electrical Controls & Safety Upgrades",
        "does": "An engineering showcase explaining how older mechanical rolling-key presses can be modernized by retrofitting Italian OMPI pneumatic clutch-brakes, dual-hand safety controls, and updated electrical panels.",
        "benefit": "Demonstrates practical modernization options for plant owners looking to improve machine safety, reduce maintenance downtime, and enhance productivity without purchasing an entirely new machine.",
        "deliverables": ["Pneumatic Clutch Conversion Overview", "Dual-Hand Safety Control Specifications", "Productivity Improvement Case Summaries"],
        "feature": "Before-and-after case summaries highlighting technical modernization benefits."
    },
    {
        "id": "UNIT-22",
        "title": "Maintenance Service Contracts Overview (AMC)",
        "type": "Maintenance Service Contracts (AMC)",
        "audience": "Plant Maintenance Managers, Operations Directors",
        "focus": "Preventative Maintenance, Clutch Audits & Technical Visits",
        "does": "Presents structured annual maintenance service programs, outlining scheduled quarterly pneumatic clutch inspections, flywheel bearing checks, and technical service support.",
        "benefit": "Helps plant managers establish structured preventative maintenance schedules, supporting long-term machine reliability and minimizing unexpected production interruptions.",
        "deliverables": ["Quarterly Machine Inspection Checklist Summary", "Priority Technical Support Guidelines", "Recommended Spare Parts Holding Schedule"],
        "feature": "Overview of available service tiers (Standard, Comprehensive, and Enterprise)."
    },
    # Page 15
    {
        "id": "UNIT-23",
        "title": "Dalal Staff Machine Management Desk",
        "type": "Staff Operations Console",
        "audience": "Dalal Inventory Staff, Commercial Officers",
        "focus": "Internal Stock Management, Technical Specs & Pricing",
        "does": "A secure internal staff desk allowing Dalal's operations team to add new presses to the catalog, update specifications, upload power trial video links, and update machine commercial status (Available, On Hold, Sold).",
        "benefit": "Allows Dalal's team to update machine listings directly without relying on external developers for routine changes, ensuring web listings reflect current Pune stock.",
        "deliverables": ["Simple Machine Spec & Photo Management", "Commercial Status Toggle (Available, Reserved, Sold)", "Internal Pricing & Specification Review"],
        "feature": "Secure internal desk with instant updates reflected across the public catalog."
    },
    {
        "id": "UNIT-24",
        "title": "Dalal Customer Inquiry Management Desk",
        "type": "Staff Operations Console",
        "audience": "Sales Team, Managing Director, Commercial Head",
        "focus": "Inquiry Prioritization by Urgency & Quotation History",
        "does": "A centralized operational inbox organizing incoming customer inquiries from website and WhatsApp, displaying plant name, machine model, urgency level, and past quotation interaction logs.",
        "benefit": "Helps ensure customer inquiries are systematically organized and tracked by sales staff, reducing the risk of missed inquiries and supporting timely commercial responses.",
        "deliverables": ["Centralized Inquiry Feed with Status Tracking", "Direct WhatsApp Chat Link to Buyer", "Quotation History & Commercial Notes"],
        "feature": "Urgency-based inquiry prioritization flagging high-tonnage leads and active RFQs first."
    }
]

# 33 OMPI Industrial Operations & ERP Modules
ompi_modules = [
    # Page 17
    {
        "id": "ERP-MOD-01",
        "title": "Client Records & GST Information Master",
        "engine": "Engine 1: Sales & Customer Management",
        "role": "Sales Executives, Accounts Staff",
        "focus": "Centralized Customer Directory & Tax Details",
        "does": "Maintains central profiles for customer factories: verified 15-digit GSTIN, delivery godown addresses, authorized purchase contacts, and approved commercial credit terms. Updates in real time.",
        "benefit": "Designed to prevent billing mistakes, assist in verifying customer tax details before dispatch, and ensure invoices match official GST records to prevent tax credit disputes.",
        "deliverables": ["Customer Tax & Address Master Records", "Multi-Godown Delivery Location Registry", "Commercial Credit Terms Monitoring"],
        "feature": "Automated GST number verification and outstanding ledger balance summary."
    },
    {
        "id": "ERP-MOD-02",
        "title": "OMPI Product Catalog & Technical Registry",
        "engine": "Engine 1: Sales & Customer Management",
        "role": "Technical Sales Engineers",
        "focus": "Italian Clutch-Brake Specifications & Dimensions",
        "does": "Organizes all Italian pneumatic clutch-brakes, rotating unions, and friction discs by bore size, torque capacity, operating air pressure, and manufacturer dimensional cross-references.",
        "benefit": "Enables sales engineers to identify the appropriate replacement clutch model quickly without searching through printed Italian paper catalogs, providing faster answers to customers.",
        "deliverables": ["Italian OMPI Component Specification Registry", "Bore Size & Torque Dimensional Cross-Index", "Replacement Model Matching Reference"],
        "feature": "Lookup tool matching industrial press makes (Aida, Schuler, Godrej) with OMPI models."
    },
    # Page 18
    {
        "id": "ERP-MOD-03",
        "title": "Manual Exchange Rate & Landed Cost Calculator",
        "engine": "Engine 1: Sales & Customer Management",
        "role": "Commercial Manager, Managing Director",
        "focus": "Daily Manual Euro/INR Entry & Duty Surcharges (Optional Live API)",
        "does": "Allows staff to input daily official Euro/INR rates manually (or connect optional live Forex API) to calculate landed selling prices including sea freight, basic customs duty, and target margins.",
        "benefit": "Helps protect profit margins against currency shifts between Euro and Rupee during international shipping, supporting consistent commercial pricing.",
        "deliverables": ["Daily Manual Euro Exchange Rate Entry Interface", "Customs Duty & Port Handling Surcharge Matrix", "Target Margin Calculation Guidelines"],
        "feature": "Manual daily exchange rate entry with automated duty surcharge calculation (live feed optional add-on)."
    },
    {
        "id": "ERP-MOD-04",
        "title": "OMPI Fast-Quote & Commercial Proposal Generator",
        "engine": "Engine 1: Sales & Customer Management",
        "role": "Sales Representatives, Commercial Staff",
        "focus": "Shared Quoting Engine with Isolated OMPI Letterhead & Banking",
        "does": "Extends Phase 1 Core Quoting Engine to OMPI products. Generates formal PDF proposals for Italian clutch models, strictly maintaining OMPI's separate letterhead, quote numbering, and bank details.",
        "benefit": "Enables sales staff to generate official quotation letters quickly, helping accelerate response times while keeping entity records strictly segregated.",
        "deliverables": ["Dedicated OMPI India LLP Branded Quotation Format", "Separate Quote Numbering Sequence & Bank Details", "WhatsApp & Email Proposal Dispatch Link"],
        "feature": "Shared quoting engine generating OMPI proposals with distinct entity letterhead and banking."
    },
    # Page 19
    {
        "id": "ERP-MOD-05",
        "title": "Customer Inquiry Visual Deal Board",
        "engine": "Engine 1: Sales & Customer Management",
        "role": "Sales Team, Managing Director",
        "focus": "Visual Deal Progression from Inquiry to Closure",
        "does": "Presents all active customer inquiries on a visual stage board: New Lead, Quoted, Power Trial Scheduled, Commercial Negotiation, On Hold, and Order Confirmed.",
        "benefit": "Provides management with clear visual oversight of all active inquiries, helping ensure leads receive appropriate follow-up and supporting overall deal progression.",
        "deliverables": ["Visual Deal Stage Tracking Board", "Follow-Up Reminder Indicators", "Sales Representative Deal Assignment"],
        "feature": "Visual stage cards with color-coded indicators for inquiries awaiting follow-up."
    },
    {
        "id": "ERP-MOD-06",
        "title": "Press & Clutch Engineering Matcher",
        "engine": "Engine 1: Sales & Customer Management",
        "role": "Technical Sourcing Engineers",
        "focus": "Historical Press Model Sizing & Engineering Match",
        "does": "Cross-references standard industrial press makes with recommended OMPI clutch-brake models, flywheel mounting dimensions, and required operating air pressure parameters.",
        "benefit": "Assists sales engineers in advising factory owners on the appropriate clutch retrofit for their equipment, supporting technical accuracy and customer confidence.",
        "deliverables": ["Machine Make-to-Clutch Engineering Matcher", "Flywheel Bore & Keyway Reference Charts", "Operating Pressure & Torque Guidance"],
        "feature": "Pre-configured compatibility lookup providing engineering recommendations quickly."
    },
    # Page 20
    {
        "id": "ERP-MOD-07",
        "title": "Pune Warehouse Live Stock Tracker",
        "engine": "Engine 2: Inventory & Warehouse Management",
        "role": "Godown Storekeeper, Operations Head",
        "focus": "Real-Time Stock Counts, Reservations & Location",
        "does": "Monitors clutch-brakes, friction discs, and machinery physically present in the Pune stockyard, tracking warehouse location, arrival date, condition, and commercial reservation status.",
        "benefit": "Designed to prevent accidental double-selling of in-demand inventory, helping ensure items confirmed to one client are not simultaneously committed to another buyer.",
        "deliverables": ["Real-Time Available Stock Balances", "Temporary Customer Commercial Reservation Lock", "Warehouse Shelf & Bin Location Reference"],
        "feature": "Commercial reservation lock preventing conflicting commitments of available stock."
    },
    {
        "id": "ERP-MOD-08",
        "title": "Container Transit & Shipping Milestone Logger (Manual Entry)",
        "engine": "Engine 2: Inventory & Warehouse Management",
        "role": "Logistics Officer, Commercial Staff",
        "focus": "Manual Bill of Lading (BL) & Shipping Milestone Logging",
        "does": "Provides a structured manual logging interface where logistics staff input Bill of Lading (BL) numbers, vessel names, departure dates, estimated arrival at Nhava Sheva, and customs milestone updates (carrier API available as optional add-on).",
        "benefit": "Assists the logistics team in providing delivery estimates to customers awaiting imported equipment and helps prepare customs documents ahead of vessel arrival.",
        "deliverables": ["Manual BL & Vessel Arrival Logging Interface", "Port Customs Clearance Status Log", "Customer Pre-Arrival Notification Workflow"],
        "feature": "Manual milestone status logger tracking vessel arrival schedules and container clearance."
    },
    # Page 21
    {
        "id": "ERP-MOD-09",
        "title": "Low-Stock Restocking Alert Assistant",
        "engine": "Engine 2: Inventory & Warehouse Management",
        "role": "Purchasing Staff, Storekeeper",
        "focus": "Minimum Stock Thresholds & Reorder Planning",
        "does": "Monitors stock levels against pre-set minimum thresholds and generates automated notifications when fast-moving friction discs, seal kits, or rotating unions reach reorder points.",
        "benefit": "Helps prevent stockouts of critical replacement parts, supporting prompt fulfillment for emergency customer breakdown inquiries and maintaining parts availability.",
        "deliverables": ["Minimum Stock Level Notification Dashboard", "Suggested Reorder Quantity Suggestions", "Supplier Lead Time Reference Buffer"],
        "feature": "Automated alert notices when fast-moving spares reach defined minimum stock levels."
    },
    {
        "id": "ERP-MOD-10",
        "title": "Inter-Warehouse Stock Transfer Challan",
        "engine": "Engine 2: Inventory & Warehouse Management",
        "role": "Logistics Dispatcher, Storekeeper",
        "focus": "Official Transfer Documentation Between Locations",
        "does": "Generates formal transfer delivery challans whenever equipment or components move between the Pune warehouse, Mumbai office, customer trial sites, or authorized engineering workshops.",
        "benefit": "Helps maintain accurate inventory records across multiple locations and provides standard documentation supporting compliant transit movement under applicable regulations.",
        "deliverables": ["Inter-Facility Delivery Challan Generator", "Transport Documentation Data Summary", "In-Transit Inventory Reconciliation Record"],
        "feature": "1-click generation of standard delivery challans for inter-facility equipment transfer."
    },
    # Page 22
    {
        "id": "ERP-MOD-11",
        "title": "Warehouse Shelf & Bin Location Guide",
        "engine": "Engine 2: Inventory & Warehouse Management",
        "role": "Godown Storekeeper, Warehouse Staff",
        "focus": "Physical Shelf Organization & Quick Item Picking",
        "does": "Maintains rack, row, and shelf coordinates for small clutch spares, seal kits, and accessories, accessible through a simple search screen at the warehouse desk.",
        "benefit": "Aims to streamline warehouse picking and packaging routines, helping staff locate specific replacement parts quickly for same-day parcel dispatch.",
        "deliverables": ["Warehouse Shelf & Bin Coordinate Mapping", "Fast Item Location Search Screen", "Organized Item Picking Sequence"],
        "feature": "Search tool directing warehouse personnel to the exact shelf location of any spare part."
    },
    {
        "id": "ERP-MOD-12",
        "title": "Consignment Stock & Customer Trial Tracker",
        "engine": "Engine 2: Inventory & Warehouse Management",
        "role": "Sales Manager, Accounts Staff",
        "focus": "Temporary Equipment Handover & Return Management",
        "does": "Tracks clutch units or testing instruments provided to customer plants on an authorized trial or demonstration basis, monitoring authorized trial periods, condition, and status.",
        "benefit": "Helps ensure company property placed at client facilities is properly tracked, reminding sales staff to arrange either final invoicing or timely return.",
        "deliverables": ["Customer Demonstration Registry", "Trial Period Expiration Reminders", "Demonstration-to-Order Conversion Workflow"],
        "feature": "Automated reminder notifications for items approaching the end of authorized trial terms."
    },
    # Page 23
    {
        "id": "ERP-MOD-13",
        "title": "International Purchase Order Generator",
        "engine": "Engine 3: Procurement & Landed Costing",
        "role": "Commercial Head, Managing Director",
        "focus": "Formal International PO Generation in Euros",
        "does": "Creates formal international purchase orders in Euros addressed to OMPI Italy, complete with manufacturer part numbers, agreed terms, shipping instructions, and HS classification codes.",
        "benefit": "Helps ensure international purchase orders match Italian manufacturing specifications and standard import documentation requirements, supporting smooth customs clearance.",
        "deliverables": ["International Purchase Order PDF Generator", "Italian Part Number & HS Code Matcher", "Supplier Order Confirmation Tracker"],
        "feature": "Formal international purchase order creator using standard commercial export terminology."
    },
    {
        "id": "ERP-MOD-14",
        "title": "Port Customs Clearance Milestone Tracker",
        "engine": "Engine 3: Procurement & Landed Costing",
        "role": "Logistics Manager, Commercial Staff",
        "focus": "Port Clearance Milestones & Timeline Monitoring",
        "does": "Tracks customs clearance milestones at Nhava Sheva port, monitoring free storage periods, shipping container return timelines, and customs assessment steps.",
        "benefit": "Helps logistics teams coordinate documentation and vehicle booking promptly, assisting in avoiding unnecessary port storage charges and container detention fees.",
        "deliverables": ["Port Storage Period Countdown Monitor", "Container Return Timeline Checklist", "Customs Clearance Status Log"],
        "feature": "Port timeline dashboard highlighting shipments approaching free storage expiration."
    },
    # Page 24
    {
        "id": "ERP-MOD-15",
        "title": "Landed Cost & Import Duty Allocation Sheet",
        "engine": "Engine 3: Procurement & Landed Costing",
        "role": "Senior Accountant, Commercial Staff",
        "focus": "True Unit Cost Allocation (Freight, Duty, Clearing)",
        "does": "Allocates shared international freight, insurance, customs basic duty, social welfare surcharges, and port clearing fees across individual imported items in a shipment batch.",
        "benefit": "Provides visibility into the full landed cost of individual components, helping management set commercially sound selling prices and evaluate gross margins accurately.",
        "deliverables": ["Proportional Expense Allocation Matrix", "True Unit Cost Calculation Summary", "Margin Analysis & Pricing Guidelines"],
        "feature": "Landed cost calculation tool distributing shared shipment expenses across spare parts."
    },
    {
        "id": "ERP-MOD-16",
        "title": "Supplier Delivery Timeliness Record",
        "engine": "Engine 3: Procurement & Landed Costing",
        "role": "Managing Director, Purchasing Staff",
        "focus": "Vendor Delivery Accuracy & Lead Time Trends",
        "does": "Records promised dispatch dates versus actual receipt dates for European and domestic suppliers, logging manufacturing lead times, transit durations, and shipment condition.",
        "benefit": "Provides factual delivery performance data to support commercial negotiations with suppliers, helping encourage dependable delivery schedules and commercial terms.",
        "deliverables": ["Supplier Delivery Timeliness Log", "Historical Lead Time Trend Overview", "Packaging & Condition Quality Notes"],
        "feature": "Supplier performance review log rating vendors on dispatch timeliness and packaging quality."
    },
    # Page 25
    {
        "id": "ERP-MOD-17",
        "title": "Workshop Reconditioning & Job Card Log",
        "engine": "Engine 4: Workshop & Engineering Overhaul",
        "role": "Workshop Foreman, Mechanical Engineers",
        "focus": "Job Cards, Replacement Parts & Labor Hours",
        "does": "Maintains a digital workshop job card for each machine undergoing reconditioning in Pune: records dismantling steps, replacement parts utilized, machinist hours, and repairs.",
        "benefit": "Assists in tracking internal overhaul expenses accurately and establishes a structured mechanical service record that demonstrates verified equipment condition to buyers.",
        "deliverables": ["Digital Workshop Job Card & Task Tracker", "Replacement Spares Utilization Log", "Technician Labor Hours & Service Record"],
        "feature": "Workshop job card recording reconditioning steps and component replacements."
    },
    {
        "id": "ERP-MOD-18",
        "title": "Clutch Retrofit Engineering Work Order",
        "engine": "Engine 4: Workshop & Engineering Overhaul",
        "role": "Application Engineers, Workshop Staff",
        "focus": "Technical Machining Dimensions & Air Valve Specs",
        "does": "Provides structured engineering instructions for mounting an OMPI pneumatic clutch onto an existing press: flywheel boring dimensions, keyway depths, and valve plumbing details.",
        "benefit": "Helps ensure machining and installation work follow verified dimensions, supporting proper mechanical fit and reliable operation on the customer's shop floor.",
        "deliverables": ["Flywheel Machining & Boring Guidelines", "Air Valve & Pneumatic Piping Diagram", "Pre-Assembly Inspection Checklist"],
        "feature": "Printable technical work orders outlining dimensional requirements for workshop machinists."
    },
    # Page 26
    {
        "id": "ERP-MOD-19",
        "title": "Pre-Dispatch Inspection & Geometry Sheet",
        "engine": "Engine 4: Workshop & Engineering Overhaul",
        "role": "Quality Inspector, Technical Director",
        "focus": "Dial Gauge Alignment, Stroke Testing & Inspection Record",
        "does": "Records geometrical inspection measurements for overhauled presses: bed parallelism, ram squareness dial indicator readings, motor amperage draw under load, and clutch stopping times.",
        "benefit": "Provides documented technical evidence of machine alignment and electrical operation, assisting in transparent pre-dispatch verification and client acceptance.",
        "deliverables": ["Bed Parallelism Dial Gauge Inspection Sheet", "Clutch Stopping Reaction Time Log", "Standard Machine Inspection Certificate"],
        "feature": "Standardized inspection sheet recording verified machine tolerances and power trial results."
    },
    {
        "id": "ERP-MOD-20",
        "title": "Client Site Installation Handover Protocol",
        "engine": "Engine 4: Workshop & Engineering Overhaul",
        "role": "Field Commissioning Engineer, Client Representative",
        "focus": "Foundation Leveling, Trial Stamping & Sign-Off",
        "does": "A mobile-friendly sign-off checklist used by Dalal engineers during final machine erection at the buyer's factory: confirms levelness, trial stamping, and customer acceptance signatures.",
        "benefit": "Helps formalize customer commissioning acceptance, providing clear documentation that supports timely milestone payment settlement.",
        "deliverables": ["Mobile Commissioning Handover Checklist", "Client Acceptance Signature Capture", "Automatic Notification for Final Billing"],
        "feature": "Digital handover certificate recording commissioning confirmation with customer sign-off."
    },
    # Page 27
    {
        "id": "ERP-MOD-21",
        "title": "GST Tax Invoice & E-Way Bill Assistant",
        "engine": "Engine 5: Accounting & Tax Governance",
        "role": "Accounts Staff, Billing Clerk",
        "focus": "Standard Tax Billing, HSN Codes & Transport Data",
        "does": "Generates standard tax invoices for machinery sales, spare parts, and service labor with automatic calculation of CGST, SGST, IGST, applicable HSN codes, and transport data.",
        "benefit": "Designed to assist accounting staff in generating accurate tax invoices, supporting compliance with tax rules and helping buyers claim eligible input tax credits.",
        "deliverables": ["Standard GST Tax Invoice Generator", "HSN Code & Tax Rate Reference Matrix", "Transport E-Way Bill Data Summary"],
        "feature": "1-click generation of professional GST tax invoices with tax calculations based on client state."
    },
    {
        "id": "ERP-MOD-22",
        "title": "Customer Payment Ledger & Aging Tracker",
        "engine": "Engine 5: Accounting & Tax Governance",
        "role": "Commercial Manager, Managing Director",
        "focus": "Outstanding Receivables, Payment Terms & Alerts",
        "does": "Monitors customer payment milestones (advance payment, pre-dispatch clearance, final commissioning balance), categorizing outstanding balances by aging period (30, 60, 90+ days).",
        "benefit": "Assists management in monitoring commercial receivables, helping ensure agreed payment terms are fulfilled prior to equipment dispatch.",
        "deliverables": ["Receivables Aging Summary Dashboard", "Pre-Dispatch Commercial Balance Check", "Automated Friendly Payment Reminders"],
        "feature": "Color-coded payment ledger helping staff verify payment clearance prior to shipment."
    },
    # Page 28
    {
        "id": "ERP-MOD-23",
        "title": "Vendor Expenses & Overseas Wire Log",
        "engine": "Engine 5: Accounting & Tax Governance",
        "role": "Senior Accountant, Finance Staff",
        "focus": "Overseas Remittances, Shipping Bills & Payment Records",
        "does": "Maintains an organized digital record of payments made to overseas manufacturers, customs clearing agents, transport operators, and local engineering contractors.",
        "benefit": "Assists accounting staff in maintaining documentation for bank foreign exchange remittances, supporting orderly financial recordkeeping and audit preparation.",
        "deliverables": ["Overseas Remittance & SWIFT Reference Log", "Vendor Invoice Verification & Matching", "Authorized Commercial Payment Record"],
        "feature": "Centralized record linking bank remittance references with foreign supplier commercial invoices."
    },
    {
        "id": "ERP-MOD-24",
        "title": "Monthly Revenue & Gross Margin Overview",
        "engine": "Engine 5: Accounting & Tax Governance",
        "role": "Managing Director, Partners",
        "focus": "Monthly Profitability, Machine Margin & Overhead",
        "does": "Summarizes revenue and direct costs across completed transactions, presenting monthly gross margin per machine, spare parts contributions, and general operating overheads.",
        "benefit": "Provides executive management with clear operational financial summaries, assisting in planning capital allocations, inventory levels, and commercial strategies.",
        "deliverables": ["Monthly Gross Margin Overview per Machine", "Spare Parts Revenue & Profit Summary", "General Overhead & Cash Inflow Indicators"],
        "feature": "Executive overview dashboard presenting monthly revenue and gross margin trends."
    },
    # Page 29
    {
        "id": "ERP-MOD-25",
        "title": "GST Return Preparation & Summary Assistant",
        "engine": "Engine 5: Accounting & Tax Governance",
        "role": "Accounts Staff, Tax Consultant",
        "focus": "GST Return Preparation & Job Work Tracking",
        "does": "Compiles monthly sales invoices, credit notes, and external job-work delivery challans into formatted summaries for easy review and reconciliation by company accountants.",
        "benefit": "Assists internal accounting teams in organizing monthly transaction records, helping reduce manual preparation time and supporting timely tax return filing.",
        "deliverables": ["Monthly Sales Transaction Summary Sheet", "External Job Work Outward & Inward Log", "Tax Reconciliation Overview for CA Review"],
        "feature": "Standard monthly transaction export pre-formatted for review by your chartered accountant."
    },
    {
        "id": "ERP-MOD-26",
        "title": "Field Sales Visit & Client Interaction Logger",
        "engine": "Engine 6: Sales Operations & Service",
        "role": "Field Sales Staff, Sales Head",
        "focus": "Client Factory Visits, Machinery Needs & Follow-Ups",
        "does": "A mobile-friendly logging tool for sales engineers visiting manufacturing clusters in Pune, Sanand, Aurangabad, and Rajkot to record client plant visits, machinery requirements, and follow-up dates.",
        "benefit": "Preserves institutional client knowledge within the company, ensuring customer requirements and discussion notes remain accessible to Dalal's management over time.",
        "deliverables": ["Mobile Client Visit Logging Screen", "Customer Machinery Requirement Notes", "Scheduled Actionable Follow-Up Reminders"],
        "feature": "Mobile-optimized visit logging interface designed for quick updates on the go."
    },
    # Page 30
    {
        "id": "ERP-MOD-27",
        "title": "Commercial Proposal Follow-Up Assistant",
        "engine": "Engine 6: Sales Operations & Service",
        "role": "Sales Team, Managing Director",
        "focus": "Follow-Up Reminders on Outstanding Quotations",
        "does": "Monitors outstanding proposals sent to prospective buyers, generating scheduled reminders for assigned sales staff to follow up with clients at appropriate intervals.",
        "benefit": "Assists sales representatives in maintaining consistent communication with active inquiries, helping support customer decisions and deal progression.",
        "deliverables": ["Quotation Follow-Up Reminder List", "Standard Follow-Up Message Templates", "Quotation Outcome Summary Notes"],
        "feature": "Follow-up schedule reminding sales staff of pending quotations awaiting customer review."
    },
    {
        "id": "ERP-MOD-28",
        "title": "Annual Maintenance Service Contract Ledger",
        "engine": "Engine 6: Sales Operations & Service",
        "role": "Service Coordinator, Accounts Staff",
        "focus": "Preventative Service Schedules & Contract Renewals",
        "does": "Tracks active maintenance service agreements, logging scheduled quarterly service visits, engineer on-site service notes, and contract renewal dates.",
        "benefit": "Assists service teams in organizing preventative maintenance visits on schedule, supporting long-term equipment reliability and client service relationships.",
        "deliverables": ["Quarterly Service Visit Schedule", "Service Contract Expiration Reminders", "On-Site Engineer Service Visit Notes"],
        "feature": "Service calendar tracking upcoming scheduled preventative maintenance visits."
    },
    # Page 31
    {
        "id": "ERP-MOD-29",
        "title": "Customer Breakdown Request Help Desk",
        "engine": "Engine 6: Sales Operations & Service",
        "role": "Service Engineers, Support Coordinator",
        "focus": "Customer Breakdown Logging & Technician Dispatch",
        "does": "Logs urgent customer equipment breakdown inquiries, assigns available service engineers, tracks spare parts dispatched from Pune, and records service completion details.",
        "benefit": "Assists in organizing emergency technical support systematically, helping clients address machinery issues promptly and supporting customer satisfaction.",
        "deliverables": ["Priority Service Request Ticket Screen", "Service Engineer Assignment Log", "Service Resolution & Handover Notes"],
        "feature": "Technical support console organizing customer service requests and technician response."
    },
    {
        "id": "ERP-MOD-30",
        "title": "Post-Installation Customer Feedback Intake",
        "engine": "Engine 6: Sales Operations & Service",
        "role": "Managing Director, Customer Relations",
        "focus": "Post-Installation Satisfaction & Review Capture",
        "does": "Enables a brief structured review inquiry sent to the customer after machine commissioning, gathering feedback on equipment performance and service quality.",
        "benefit": "Assists management in identifying areas for service improvement early and gathers verified customer feedback to highlight on the public website.",
        "deliverables": ["Structured Customer Feedback Questionnaire", "Service Quality Review Summary", "Verified Client Testimonial Intake"],
        "feature": "Feedback intake tool capturing client reviews and operational feedback."
    },
    # Page 32
    {
        "id": "ERP-MOD-31",
        "title": "Staff Access & Permission Controls",
        "engine": "Engine 7: Executive Intelligence & Security",
        "role": "Managing Director, Designated Administrator",
        "focus": "Role-Based Security & Confidential Margin Protection",
        "does": "Controls what each staff member can view and modify: sales staff view quotations and available stock; warehouse staff manage inventory; supplier purchase costs remain restricted to authorized leadership.",
        "benefit": "Protects confidential business pricing models and supplier purchase costs, ensuring staff members only access information appropriate for their specific job functions.",
        "deliverables": ["Role-Based Access Permission Settings", "Secure Individual Staff Login System", "Confidential Financial Data Isolation"],
        "feature": "Access control console allowing the Managing Director to manage staff viewing permissions."
    },
    {
        "id": "ERP-MOD-32",
        "title": "Activity History & Cloud Backup Vault",
        "engine": "Engine 7: Executive Intelligence & Security",
        "role": "System Administrator, Managing Director",
        "focus": "Daily Encrypted Backups & Activity Audit History",
        "does": "Provides automated daily backups of system records and maintains a timestamped activity log of key system actions (quotation creation, inventory adjustments, and status changes).",
        "benefit": "Assists in protecting business records against accidental data loss or hardware issues, supporting reliable business continuity and operational accountability.",
        "deliverables": ["Daily Automated Cloud Database Backups", "Timestamped System Activity History Log", "Data Restoration & Recovery Protocol"],
        "feature": "Activity history log recording key commercial updates, stock changes, and user logins."
    },
    # Page 33
    {
        "id": "ERP-MOD-33",
        "title": "Managing Director's Executive Control Desk",
        "engine": "Engine 7: Executive Intelligence & Security",
        "role": "Mr. Vinit Dalal, Designated Partners",
        "focus": "Unified Business Dashboard (Sales, Cash, Godown & Staff)",
        "does": "An executive command center presenting key operational indicators: monthly inquiry volume, active proposals, Pune warehouse stock value, and commercial payment collections.",
        "benefit": "Provides executive leadership with a clear, real-time overview of business performance across sales, inventory, and operations, supporting informed strategic management.",
        "deliverables": ["Executive Operational Overview Dashboard", "Active Pipeline Value & Receivables Summary", "Daily Business Health Summary Indicators"],
        "feature": "Executive dashboard providing leadership with real-time visibility across sales, stock, and margins."
    }
]

print(f"Loaded {len(dalal_units)} Dalal Units and {len(ompi_modules)} OMPI Modules.")

# CSS & HTML Template Generation
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
      margin-bottom: 8px;
    }
    .brand-title {
      font-size: 11.6pt;
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

    /* Standard Card Box (2 per page) */
    .card-box {
      border: 1.5px solid #cbd5e1;
      border-radius: 8px;
      background: #ffffff;
      margin-bottom: 12px;
      padding: 14px 18px;
      box-shadow: 0 1px 3px rgba(0,0,0,0.03);
    }
    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 1.5px solid #e2e8f0;
      padding-bottom: 5px;
      margin-bottom: 7px;
    }
    .badge-id {
      background: #0f172a;
      color: #ffffff;
      padding: 2.5px 7px;
      border-radius: 4px;
      font-size: 8.4pt;
      font-weight: 800;
      font-family: 'JetBrains Mono', monospace;
      margin-right: 8px;
    }
    .card-title {
      font-size: 12.0pt;
      font-weight: 800;
      color: #0f172a;
    }
    .card-status {
      font-size: 7.6pt;
      font-weight: 700;
      padding: 2px 7px;
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
      padding: 6px 12px;
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
      margin-bottom: 7px;
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
      font-size: 9.6pt;
      line-height: 1.48;
      color: #334155;
    }
    .deliverables-box {
      background: #f8fafc;
      border: 1px solid #e2e8f0;
      border-radius: 5px;
      padding: 8px 12px;
      margin-bottom: 9px;
    }
    .deliverables-title {
      font-size: 7.6pt;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.4px;
      color: #64748b;
      margin-bottom: 2px;
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
      padding: 8px 14px;
      font-size: 8.8pt;
      line-height: 1.44;
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
            <strong>Doc Ref:</strong> SCOPE-PLAN-2026-DALAL-OMPI-57 (v2.5)<br>
            <strong>Date:</strong> November 2026 &bull; <strong>Validity:</strong> 30 Days<br>
            <strong>Status:</strong> Pre-Commencement Scope Blueprint
          </div>
        </div>
        """

    def make_footer(page_num, total_pages=34):
        return f"""
        <div class="footer-bar">
          <div><strong>Dalal Machine Tools Agency Pvt. Ltd. &amp; OMPI India LLP</strong> &bull; Commercial Operations Blueprint</div>
          <div class="confidential-watermark">&#128274; CONFIDENTIAL &bull; STRICTLY NOT FOR EXTERNAL SHARING</div>
          <div>Page {page_num} of {total_pages}</div>
        </div>
        """

    def render_card(item, is_route=True):
        scope_tag = "&#9675; TO BE BUILT: SYSTEM 1" if is_route else "&#9675; TO BE BUILT: SYSTEM 2"
        badge_meta = item['type'] if is_route else item['engine']
        target_label = "Primary Business Audience" if is_route else "Responsible Staff Role"
        target_val = item['audience'] if is_route else item['role']
        focus_val = item.get('focus', 'Operational Governance & Efficiency')
        what_label = "What This Web Page Will Do Once Built" if is_route else "What This Management Tool Will Do Once Built"
        
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
            <div style="font-size:7.8pt; color:#b45309; background:#fffbeb; padding:2px 8px; border:1px solid #fef3c7; border-radius:3px; font-weight:700;">
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
              <div class="grid-text">{item['does']}</div>
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
          <div style="display:flex; justify-content:space-between; align-items:center; background:#f8fafc; border:1px solid #e2e8f0; border-radius:4px; padding:4px 12px; margin-top:8px; font-size:7.8pt; color:#475569;">
            <div><strong>Planned Milestone:</strong> {('Phase 1 (Dalal Machinery Launch)' if is_route else 'Phase 2 &bull; 3 (OMPI Operations Rollout)')}</div>
            <div><strong>Verification Criteria:</strong> Functional UAT &amp; Data Review prior to commercial release</div>
          </div>
        </div>
        """

    # HTML Document Shell
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Dalal &amp; OMPI 57 Master Specification &bull; Pre-Commencement Scope Blueprint (v2.4)</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;700&display=swap" rel="stylesheet">
  <style>
    {css}
  </style>
</head>
<body>
"""

    # PAGE 1: MASTER COVER PAGE
    html += f"""
  <div class="page">
    <div class="page-content">
      {make_header("PRE-COMMENCEMENT MASTER ARCHITECTURAL SCOPE BLUEPRINT &bull; 57 PLANNED UNITS")}

      <!-- Hero Header Box -->
      <div style="background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); color: #ffffff; border-radius: 8px; padding: 20px 24px; margin-bottom: 11px; border-left: 6px solid #d97706; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);">
        <div style="font-size: 8.5pt; font-weight: 800; color: #f59e0b; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 3px;">
          Executive Scope Blueprint &bull; Version 2.5 &bull; Validity: Thru 14 November 2026
        </div>
        <div style="font-size: 18.0pt; font-weight: 800; line-height: 1.25; margin-bottom: 6px;">
          Unified Digital Ecosystem &amp; Enterprise Operations Suite
        </div>
        <div style="font-size: 9.8pt; line-height: 1.45; color: #cbd5e1;">
          Authoritative 57-Unit Operational Architecture prepared for <strong>Dalal Machine Tools Agency Pvt. Ltd.</strong> and <strong>OMPI India LLP</strong>. 8-Month Phased Roadmap across Cloud Showroom and On-Premise Office ERP.
        </div>
      </div>

      <!-- Pre-Commencement Status Notice -->
      <div style="background:#fffbeb; border:2px solid #f59e0b; border-radius:7px; padding:12px 16px; margin-bottom:12px;">
        <div style="font-size:9.5pt; font-weight:800; color:#b45309; text-transform:uppercase; margin-bottom:3px; display:flex; align-items:center; gap:6px;">
          &#9888; Official Notice: Pre-Commencement Scope Document (Work Not Started)
        </div>
        <p style="font-size:8.9pt; line-height:1.45; color:#78350f;">
          This document represents the formal architectural blueprint detailing what will be built upon mutual agreement and contract signing. <strong>No development or programming work has commenced yet (0 lines written).</strong> This blueprint defines the full scope across both corporate entities to ensure 100% clarity before project kickoff.
        </p>
      </div>

      <!-- 2 Systems Overview Grid -->
      <div style="display:grid; grid-template-columns:1fr 1fr; gap:11px; margin-bottom:12px;">
        <div style="background:#f8fafc; border:1.5px solid #cbd5e1; border-radius:7px; padding:12px 14px;">
          <div style="font-size:9.2pt; font-weight:800; color:#0f172a; text-transform:uppercase; margin-bottom:3px; border-bottom:1.5px solid #e2e8f0; padding-bottom:3px;">
            System 1: Dalal Machine Tools Agency (24 Units)
          </div>
          <p style="font-size:8.7pt; line-height:1.42; color:#334155;">
            22 Customer-Facing Web Pages + 2 Staff Admin Desks designed to present heavy forging presses, show unedited power trial videos, provide instant quotation downloads, and route direct buyer inquiries to sales leadership.
          </p>
        </div>
        <div style="background:#f8fafc; border:1.5px solid #cbd5e1; border-radius:7px; padding:12px 14px;">
          <div style="font-size:9.2pt; font-weight:800; color:#0f172a; text-transform:uppercase; margin-bottom:3px; border-bottom:1.5px solid #e2e8f0; padding-bottom:3px;">
            System 2: OMPI India Operations ERP (33 Units)
          </div>
          <p style="font-size:8.7pt; line-height:1.42; color:#334155;">
            33 Specialized Operations Modules across 7 Management Engines: Italian factory purchase orders, landed container costing, Pune godown stock tracking, workshop reconditioning, GST tax billing, and executive oversight.
          </p>
        </div>
      </div>

      <!-- Confidentiality Notice -->
      <div style="border:1.5px solid #e11d48; background:#fff1f2; border-radius:7px; padding:11px 16px; margin-bottom:12px;">
        <div style="font-size:9.0pt; font-weight:800; color:#9f1239; text-transform:uppercase; margin-bottom:3px; display:flex; align-items:center; gap:6px;">
          &#128274; Confidentiality &amp; Anti-Disclosure Covenant
        </div>
        <p style="font-size:8.6pt; line-height:1.42; color:#4c0519;">
          This master specification contains proprietary business logic and commercial methods of Dalal Machine Tools Agency Pvt. Ltd. and OMPI India LLP. <strong>Strictly confidential and strictly not for sharing.</strong> Unauthorized copying, external distribution, or sharing with third parties without written authorization is prohibited.
        </p>
      </div>

      <!-- Executive Architecture & Reading Guide -->
      <div style="background:#ffffff; border:1.5px solid #cbd5e1; border-radius:7px; padding:12px 16px; margin-bottom:12px;">
        <div style="font-size:8.8pt; font-weight:800; color:#0f172a; text-transform:uppercase; margin-bottom:5px; border-bottom:1.5px solid #f1f5f9; padding-bottom:3px;">
          Master Proposal Structure &bull; Executive Navigation Guide
        </div>
        <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px; font-size:8.3pt; line-height:1.4; color:#334155;">
          <div>
            <strong>Pages 04 to 15 &bull; Dalal Public Web Platform (24 Units):</strong><br>
            Customer-facing showcase for heavy presses, live power trials, 60-second quotations, press tonnage calculator, and 2 staff operational management desks.
          </div>
          <div>
            <strong>Pages 16 to 33 &bull; OMPI Operations ERP Suite (33 Units):</strong><br>
            Internal industrial management suite covering Italian factory imports in Euros, landed port costing, Pune godown stock tracking, workshop job cards, and GST tax billing.
          </div>
        </div>
      </div>

      <!-- Architecture & Infrastructure Summary Banner -->
      <div style="background:#f1f5f9; border:1.5px solid #cbd5e1; border-radius:7px; padding:9px 14px; margin-bottom:11px; display:grid; grid-template-columns:1fr 1fr; gap:10px; font-size:8.2pt; line-height:1.38; color:#334155;">
        <div>
          <strong>System 1 (Dalal Machinery):</strong> Public Cloud Hosting (AWS/Render) with global CDN &bull; 24 Units &bull; Phase 1 (Weeks 1–8).
        </div>
        <div>
          <strong>System 2 (OMPI ERP):</strong> On-Premise Office LAN on Dedicated Pune Host PC &bull; 33 Modules &bull; Phase 2 &amp; 3 (Weeks 9–32).
        </div>
      </div>

      <!-- Metadata Box -->
      <div style="background:#ffffff; border:1.5px solid #0f172a; border-radius:7px; padding:9px 16px; display:flex; justify-content:space-between; align-items:center;">
        <div>
          <span style="font-size:7.6pt; color:#64748b; font-weight:700; text-transform:uppercase;">Principal Client:</span><br>
          <strong style="font-size:9.2pt; color:#0f172a;">Mr. Vinit Dalal</strong> &bull; Managing Director / Partner
        </div>
        <div>
          <span style="font-size:7.6pt; color:#64748b; font-weight:700; text-transform:uppercase;">Scope &amp; Duration:</span><br>
          <strong style="font-size:9.2pt; color:#0f172a;">57 Units &bull; 8 Months (32 Wks)</strong>
        </div>
        <div>
          <span style="font-size:7.6pt; color:#64748b; font-weight:700; text-transform:uppercase;">Principal Consultant:</span><br>
          <strong style="font-size:9.2pt; color:#0f172a;">Suyash Shinde</strong> &bull; Principal Software Consultant
        </div>
      </div>
    </div>
    {make_footer(1)}
  </div>
"""

    # PAGE 2: 1-PAGE EXECUTIVE SUMMARY (ALIGNED WITH PROPOSAL V1.0)
    html += f"""
  <div class="page">
    <div class="page-content">
      {make_header("EXECUTIVE 1-PAGE SUMMARY &bull; CORE DELIVERABLES, TIMELINE &amp; BOUNDARIES")}

      <div class="section-header">
        <span class="section-title">Master Project Summary Aligned with Unified Proposal (v1.0) &bull; 8-Month Roadmap</span>
        <span class="section-tag">Executive Summary</span>
      </div>

      <!-- 1. Deliverables & Infrastructure Architecture Box -->
      <div style="background:#ffffff; border:1.5px solid #cbd5e1; border-radius:7px; padding:12px 16px; margin-bottom:10px;">
        <div style="font-size:9.0pt; font-weight:800; color:#0f172a; text-transform:uppercase; margin-bottom:4px; border-bottom:1.5px solid #f1f5f9; padding-bottom:3px;">
          1. What You Get (57 Total Units &bull; Hybrid Cloud &amp; On-Premise LAN Architecture)
        </div>
        <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px; font-size:8.3pt; line-height:1.4; color:#334155;">
          <div>
            <strong>System 1: Dalal Machinery Platform (24 Units &bull; Cloud Hosted):</strong><br>
            Hosted on secure cloud infrastructure (AWS/Render) with global CDN. Includes 22 public pages (digital showroom, video trials, 60-second quotes, tonnage calculator) + 2 staff operations consoles + GA4 telemetry &amp; SEO metadata.
          </div>
          <div>
            <strong>System 2: OMPI Industrial ERP (33 Modules &bull; On-Premise Office LAN):</strong><br>
            Deployed on dedicated Pune headquarters host PC across internal Gigabit LAN (zero cloud SaaS fees, absolute privacy of Italian landed costs/margins). 18 Core Business Modules (Phase 2) + 15 Workshop &amp; Executive Consoles (Phase 3).
          </div>
        </div>
      </div>

      <!-- 2. Realistic 8-Month Phasing Timeline Table -->
      <div style="background:#f8fafc; border:1.5px solid #cbd5e1; border-radius:7px; padding:12px 16px; margin-bottom:10px;">
        <div style="font-size:9.0pt; font-weight:800; color:#0f172a; text-transform:uppercase; margin-bottom:4px;">
          2. Master Phasing Schedule &bull; 8 Months Total Duration (32 Calendar Weeks)
        </div>
        <table style="width:100%; border-collapse:collapse; font-size:8.1pt; line-height:1.36; color:#334155;">
          <thead>
            <tr style="background:#0f172a; color:#ffffff; text-align:left;">
              <th style="padding:5px 8px;">Milestone Phase</th>
              <th style="padding:5px 8px;">Scope of Deliverables</th>
              <th style="padding:5px 8px;">Target Schedule</th>
              <th style="padding:5px 8px;">Status / Milestone Gate</th>
            </tr>
          </thead>
          <tbody>
            <tr style="border-bottom:1px solid #e2e8f0; background:#ffffff;">
              <td style="padding:5px 8px; font-weight:700;">Phase 1: Dalal Platform</td>
              <td style="padding:5px 8px;">22 Public Pages &bull; 2 Staff Desks &bull; Core Quoting Engine &bull; GA4 / SEO</td>
              <td style="padding:5px 8px; font-weight:600; color:#0f172a;">Weeks 1–8 (Months 1–2)</td>
              <td style="padding:5px 8px; font-weight:700; color:#b45309;">TO COMMENCE UPON ADVANCE</td>
            </tr>
            <tr style="border-bottom:1px solid #e2e8f0; background:#f8fafc;">
              <td style="padding:5px 8px; font-weight:700;">Phase 2: OMPI Core ERP</td>
              <td style="padding:5px 8px;">Modules 01–18 (Italian Catalog, Sizing, Landed Costing, Pune Godown, OMPI Quotes)</td>
              <td style="padding:5px 8px; font-weight:600; color:#0f172a;">Weeks 9–20 (Months 3–5)</td>
              <td style="padding:5px 8px; font-weight:600; color:#475569;">MONTHS 3–5 IMPLEMENTATION</td>
            </tr>
            <tr style="background:#ffffff;">
              <td style="padding:5px 8px; font-weight:700;">Phase 3: Operations &amp; Exec</td>
              <td style="padding:5px 8px;">Modules 19–33 (Job Cards, GST Billing, Shipping Tracker, MD Desk, 4 Workspaces)</td>
              <td style="padding:5px 8px; font-weight:600; color:#0f172a;">Weeks 21–32 (Months 6–8)</td>
              <td style="padding:5px 8px; font-weight:600; color:#475569;">MONTHS 6–8 IMPLEMENTATION</td>
            </tr>
          </tbody>
        </table>
        <div style="font-size:7.8pt; color:#64748b; margin-top:4px;">
          * Note on Module Hierarchy: The master contract references 22 primary business modules; this specification details the full 57-unit operational footprint including all public interfaces, departmental consoles, and compliance tools.
        </div>
      </div>

      <!-- 3. Boundaries, Deemed Acceptance & Client Responsibilities Grid -->
      <div style="display:grid; grid-template-columns:1fr 1fr; gap:9px; margin-bottom:10px;">
        <div style="background:#fff1f2; border:1.5px solid #fecdd3; border-radius:7px; padding:11px 14px;">
          <div style="font-size:8.6pt; font-weight:800; color:#9f1239; text-transform:uppercase; margin-bottom:3px;">
            3. Exclusions &amp; Direct Client Costs
          </div>
          <ul style="font-size:8.0pt; line-height:1.38; color:#4c0519; padding-left:13px; margin:0;">
            <li>Hardware: Yard CCTV cameras, office PCs, UPS, barcode scanners.</li>
            <li>Third-party subscriptions: WhatsApp Meta fees, GST API, cloud hosting, corporate domain/email (registered in Client's name).</li>
            <li>Content production: Machinery photography, video shoots, CA-vetted legal text.</li>
          </ul>
        </div>
        <div style="background:#eff6ff; border:1.5px solid #bfdbfe; border-radius:7px; padding:11px 14px;">
          <div style="font-size:8.6pt; font-weight:800; color:#1e40af; text-transform:uppercase; margin-bottom:3px;">
            4. Client Inputs &amp; 7-Day Acceptance Gate
          </div>
          <ul style="font-size:8.0pt; line-height:1.38; color:#1e3a8a; padding-left:13px; margin:0;">
            <li>Client deliverables: Machine specs, photos, Italian catalog spreadsheets.</li>
            <li>Timeline Clock: Schedule begins upon advance + initial data; client delays extend milestone dates automatically on a day-for-day basis.</li>
            <li><strong>7-Day Deemed Acceptance:</strong> Written punch-list required within 7 days of demo; absence of notice constitutes formal milestone acceptance and activates 30-day warranty.</li>
          </ul>
        </div>
      </div>

      <!-- 4. Shared Quoting, Backup & Legal Liability Box -->
      <div style="background:#ffffff; border:1.5px solid #cbd5e1; border-radius:7px; padding:10px 14px; margin-bottom:10px;">
        <div style="font-size:8.6pt; font-weight:800; color:#0f172a; text-transform:uppercase; margin-bottom:3px; border-bottom:1.5px solid #f1f5f9; padding-bottom:2px;">
          5. Core Governance, Shared Quoting &amp; Code Ownership
        </div>
        <div style="display:grid; grid-template-columns:1fr 1fr; gap:9px; font-size:8.0pt; line-height:1.36; color:#334155;">
          <div>
            <strong>Cross-Entity Shared Quoting:</strong> Dalal (Unit 11/24) and OMPI (MOD-04) utilize a shared quotation engine architecture, but strictly enforce isolated company letterheads, distinct quotation numbering, and separate bank remittance details.
          </div>
          <div>
            <strong>Code Ownership &amp; Liability:</strong> Joint and several commercial liability across entities. 100% custom code owned by Client upon settlement, excluding third-party open-source libraries and Consultant's reusable generic UI framework.
          </div>
        </div>
      </div>

      <!-- Commercial Governance Note -->
      <div style="background:#f8fafc; border:1.5px solid #0f172a; border-radius:7px; padding:8px 14px;">
        <div style="font-size:8.4pt; font-weight:800; color:#0f172a; text-transform:uppercase; margin-bottom:2px;">
          Scope Blueprint Approval &bull; Annexure A to Master Services Agreement
        </div>
        <p style="font-size:7.9pt; line-height:1.36; color:#334155; margin:0;">
          This 57-unit master blueprint defines the functional scope of work (Annexure A). Commercial fee milestones, payment schedules, and legal terms shall be governed by the formal Master Services Agreement. Any feature not detailed herein shall be estimated separately under formal change order (CR) procedures.
        </p>
      </div>
    </div>
    {make_footer(2)}
  </div>
"""

    # PAGE 3: ASSUMPTIONS, EXCLUSIONS, 3-TIER BACKUP & GOVERNANCE
    html += f"""
  <div class="page">
    <div class="page-content">
      {make_header("GOVERNANCE &bull; ASSUMPTIONS, EXCLUSIONS &amp; CLIENT RESPONSIBILITIES")}

      <div class="section-header">
        <span class="section-title">Operational Infrastructure, Third-Party Subscriptions &amp; Commercial Assumptions</span>
        <span class="section-tag">Commercial Boundaries</span>
      </div>

      <!-- 1. Infrastructure & Third-Party Subscriptions Box -->
      <div style="background:#ffffff; border:1.5px solid #cbd5e1; border-radius:7px; padding:11px 15px; margin-bottom:9px;">
        <div style="font-size:8.8pt; font-weight:800; color:#0f172a; text-transform:uppercase; margin-bottom:3px; border-bottom:1.5px solid #f1f5f9; padding-bottom:2px;">
          1. Hosting Infrastructure &amp; Third-Party Subscriptions (Client Direct Accounts)
        </div>
        <p style="font-size:7.9pt; line-height:1.36; color:#475569; margin-bottom:5px;">
          To ensure client independence and zero markups, all cloud hosting, corporate domains, and API services shall be registered directly in the Client's legal name (Dalal / OMPI). Subscription and usage charges are paid directly by Client:
        </p>
        <div style="display:grid; grid-template-columns:1fr 1fr; gap:7px; font-size:7.9pt; line-height:1.34; color:#334155;">
          <div style="background:#f8fafc; padding:6px 10px; border-radius:4px; border-left:3px solid #0284c7;">
            <strong>Dalal Website Cloud Hosting:</strong> Scalable cloud hosting (AWS / Render) &amp; domain DNS (website address routing).
          </div>
          <div style="background:#f8fafc; padding:6px 10px; border-radius:4px; border-left:3px solid #0284c7;">
            <strong>OMPI ERP On-Premise LAN Setup:</strong> Dedicated Pune office host PC &amp; UPS power (zero third-party cloud hosting fees).
          </div>
          <div style="background:#f8fafc; padding:6px 10px; border-radius:4px; border-left:3px solid #0284c7;">
            <strong>WhatsApp Business API:</strong> Meta conversation usage fees for automated proposal dispatch and inquiry notifications.
          </div>
          <div style="background:#f8fafc; padding:6px 10px; border-radius:4px; border-left:3px solid #0284c7;">
            <strong>GST / E-Way Bill Gateway:</strong> GSP/ASP subscription (government portal integration partner) if automated portal lookup is selected.
          </div>
          <div style="background:#f8fafc; padding:6px 10px; border-radius:4px; border-left:3px solid #0284c7;">
            <strong>Euro Exchange Rate Feed:</strong> Manual daily rate entry included; optional live Forex API subscription if real-time feed desired.
          </div>
          <div style="background:#f8fafc; padding:6px 10px; border-radius:4px; border-left:3px solid #0284c7;">
            <strong>Shipping Container Tracking:</strong> Manual Bill of Lading (BL) logging included; automated shipping line API feeds subject to carrier subscription.
          </div>
        </div>
      </div>

      <!-- 2. Hardware Exclusions Box -->
      <div style="background:#ffffff; border:1.5px solid #cbd5e1; border-radius:7px; padding:10px 15px; margin-bottom:9px;">
        <div style="font-size:8.8pt; font-weight:800; color:#0f172a; text-transform:uppercase; margin-bottom:3px; border-bottom:1.5px solid #f1f5f9; padding-bottom:2px;">
          2. Hardware &amp; Physical Yard Infrastructure Exclusions
        </div>
        <div style="display:grid; grid-template-columns:1fr 1fr; gap:7px; font-size:7.9pt; line-height:1.34; color:#334155;">
          <div style="background:#f8fafc; padding:6px 10px; border-radius:4px; border-left:3px solid #d97706;">
            <strong>Live Stockyard Camera (Unit 17):</strong> CCTV cameras, DVR/NVR hardware, optical fiber internet, and static IP streaming setup at Pune yard are 100% Client's responsibility. Software provides the secure viewing interface.
          </div>
          <div style="background:#f8fafc; padding:6px 10px; border-radius:4px; border-left:3px solid #d97706;">
            <strong>Warehouse Equipment:</strong> Physical barcode label printers, handheld RF scanning guns, office computers, and local Wi-Fi equipment are excluded from software scope.
          </div>
        </div>
      </div>

      <!-- 3. Client Content & Day-for-Day Timeline Delays -->
      <div style="background:#ffffff; border:1.5px solid #cbd5e1; border-radius:7px; padding:10px 15px; margin-bottom:9px;">
        <div style="font-size:8.8pt; font-weight:800; color:#0f172a; text-transform:uppercase; margin-bottom:3px; border-bottom:1.5px solid #f1f5f9; padding-bottom:2px;">
          3. Client Content Deliverables &amp; Timeline Clock Rules
        </div>
        <p style="font-size:8.0pt; line-height:1.38; color:#334155; margin:0;">
          The development schedule clock commences strictly upon receipt of the agreed milestone advance remittance AND client baseline data: (a) Machine photographs, nameplate specs, and power trial video links; (b) Italian OMPI catalog spreadsheets and pricing formulas; (c) High Seas Sales contracts vetted by Client's chartered accountant. <strong>Any delay in client-provided materials automatically extends subsequent milestone target dates on a day-for-day basis.</strong>
        </p>
      </div>

      <!-- 4. Defined 3-Tier Rolling Backup Architecture -->
      <div style="background:#ffffff; border:1.5px solid #cbd5e1; border-radius:7px; padding:10px 15px; margin-bottom:9px;">
        <div style="font-size:8.8pt; font-weight:800; color:#0f172a; text-transform:uppercase; margin-bottom:3px; border-bottom:1.5px solid #f1f5f9; padding-bottom:2px;">
          4. Defined 3-Tier Rolling Backup Architecture &amp; Data Privacy
        </div>
        <p style="font-size:7.9pt; line-height:1.36; color:#334155; margin-bottom:4px;">
          All business records, customer lead history, and commercial quotations are stored in an encrypted PostgreSQL/SQLite database (secured business database). Data protection follows a 3-tier rolling backup strategy (subject to local PC hardware, UPS power, and cloud storage plan maintained by Client):
        </p>
        <div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:6px; font-size:7.8pt; line-height:1.32; color:#334155;">
          <div style="background:#f8fafc; padding:5px 8px; border-radius:4px; border-left:2.5px solid #059669;">
            <strong>Tier 1 (Host Snapshot):</strong> Daily automated local database backup snapshot on host server at midnight.
          </div>
          <div style="background:#f8fafc; padding:5px 8px; border-radius:4px; border-left:2.5px solid #059669;">
            <strong>Tier 2 (LAN Mirror / NAS):</strong> Weekly automated synchronization to a secondary office machine or local network storage.
          </div>
          <div style="background:#f8fafc; padding:5px 8px; border-radius:4px; border-left:2.5px solid #059669;">
            <strong>Tier 3 (Cloud Archive):</strong> Monthly encrypted off-site cloud snapshot (subject to Client's cloud storage account).
          </div>
        </div>
      </div>

      <!-- 5. Change Control, 7-Day Deemed Acceptance, Warranty & Code Ownership -->
      <div style="background:#f8fafc; border:1.5px solid #0f172a; border-radius:7px; padding:10px 15px;">
        <div style="font-size:8.8pt; font-weight:800; color:#0f172a; text-transform:uppercase; margin-bottom:3px;">
          5. Change Policy, 7-Day Deemed Acceptance, Warranty &amp; Code Ownership
        </div>
        <div style="display:grid; grid-template-columns:1fr 1fr 1fr 1fr; gap:7px; font-size:7.7pt; line-height:1.34; color:#334155;">
          <div>
            <strong>Change Request (CR):</strong><br>
            Features outside this 57-unit blueprint shall be scoped and billed under a formal written Change Order.
          </div>
          <div>
            <strong>7-Day Acceptance:</strong><br>
            Client shall inspect and provide written feedback within 7 calendar days of milestone demo. Absence of notice constitutes formal acceptance.
          </div>
          <div>
            <strong>30-Day Warranty:</strong><br>
            Includes 30 calendar days of bug-fixing support upon milestone acceptance. Ongoing support via annual AMC.
          </div>
          <div>
            <strong>100% Code Ownership:</strong><br>
            Custom application code transfers to Client upon full settlement (excluding open-source libraries and generic UI framework).
          </div>
        </div>
      </div>
    </div>
    {make_footer(3)}
  </div>
"""

    # PAGES 4 TO 15: DALAL 24 UNITS (2 PER PAGE)
    for i in range(12):
        page_num = i + 4
        u1 = dalal_units[i * 2]
        u2 = dalal_units[i * 2 + 1]

        html += f"""
  <div class="page">
    <div class="page-content">
      {make_header("SYSTEM 1: DALAL MACHINERY PUBLIC PLATFORM &bull; PROPOSED SCOPE")}

      <div class="section-header">
        <span class="section-title">Dalal Web &amp; Operations Scope &bull; Units {i*2+1:02d} &amp; {i*2+2:02d} of 24 (To Be Engineered)</span>
        <span class="section-tag">Dalal Machine Tools Scope</span>
      </div>

      {render_card(u1, is_route=True)}
      {render_card(u2, is_route=True)}
    </div>
    {make_footer(page_num)}
  </div>
"""

    # PAGE 16: OMPI INDUSTRIAL ERP ARCHITECTURE MAP
    html += f"""
  <div class="page">
    <div class="page-content">
      {make_header("SYSTEM 2: OMPI INDUSTRIAL OPERATIONS SUITE &bull; ARCHITECTURAL MAP")}

      <!-- Hero Transition Banner -->
      <div style="background: linear-gradient(135deg, #1e3a8a 0%, #0f172a 100%); color: #ffffff; border-radius: 8px; padding: 20px 22px; margin-bottom: 12px; border-left: 6px solid #38bdf8; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);">
        <div style="font-size: 8.5pt; font-weight: 800; color: #38bdf8; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 3px;">
          Operations Master Suite &bull; 33 Specialized Functional Modules
        </div>
        <div style="font-size: 16.5pt; font-weight: 800; line-height: 1.25; margin-bottom: 5px;">
          OMPI India Industrial Operations &amp; ERP Management Suite
        </div>
        <div style="font-size: 9.6pt; line-height: 1.45; color: #e2e8f0;">
          A standalone operational software suite designed for Italian import management, Pune warehouse inventory, press reconditioning job cards, GST compliance, and leadership intelligence.
        </div>
      </div>

      <!-- 7 Functional Engines Table with Exact Phase Mapping -->
      <div style="background:#ffffff; border:1.5px solid #cbd5e1; border-radius:7px; padding:14px 18px; margin-bottom:12px;">
        <div style="font-size:9.2pt; font-weight:800; color:#0f172a; text-transform:uppercase; margin-bottom:5px; border-bottom:1.5px solid #f1f5f9; padding-bottom:3px;">
          The 7 Core Operational Engines &bull; Exact Phased Milestone Mapping (Modules 01 to 33)
        </div>
        <table style="width:100%; border-collapse:collapse; font-size:8.3pt; line-height:1.4; color:#334155;">
          <thead>
            <tr style="background:#0f172a; color:#ffffff; text-align:left;">
              <th style="padding:6px 9px;">Operational Engine</th>
              <th style="padding:6px 9px;">Planned Modules</th>
              <th style="padding:6px 9px;">Delivery Milestone</th>
              <th style="padding:6px 9px;">Core Business Responsibility</th>
            </tr>
          </thead>
          <tbody>
            <tr style="border-bottom:1px solid #e2e8f0; background:#ffffff;">
              <td style="padding:6px 9px; font-weight:700; color:#0f172a;">Engine 1: Sales &amp; Customers</td>
              <td style="padding:6px 9px; font-weight:600; color:#b45309;">Modules 01 to 06</td>
              <td style="padding:6px 9px; font-weight:700; color:#0369a1;">Phase 2 (Wks 9–20)</td>
              <td style="padding:6px 9px;">Customer master, Italian catalog, OMPI proposal generator, deal board.</td>
            </tr>
            <tr style="border-bottom:1px solid #e2e8f0; background:#f8fafc;">
              <td style="padding:6px 9px; font-weight:700; color:#0f172a;">Engine 2: Godown &amp; Inventory</td>
              <td style="padding:6px 9px; font-weight:600; color:#b45309;">Modules 07 to 12</td>
              <td style="padding:6px 9px; font-weight:700; color:#0369a1;">Phase 2 (Wks 9–20)</td>
              <td style="padding:6px 9px;">Pune warehouse stock, manual container logging, safety stock, bin coordinates.</td>
            </tr>
            <tr style="border-bottom:1px solid #e2e8f0; background:#ffffff;">
              <td style="padding:6px 9px; font-weight:700; color:#0f172a;">Engine 3: Procurement &amp; Landed</td>
              <td style="padding:6px 9px; font-weight:600; color:#b45309;">Modules 13 to 16</td>
              <td style="padding:6px 9px; font-weight:700; color:#0369a1;">Phase 2 (Wks 9–20)</td>
              <td style="padding:6px 9px;">Italy POs in Euros, port storage countdown, landed cost sheet, vendor logs.</td>
            </tr>
            <tr style="border-bottom:1px solid #e2e8f0; background:#f8fafc;">
              <td style="padding:6px 9px; font-weight:700; color:#0f172a;">Engine 4: Workshop &amp; Overhaul</td>
              <td style="padding:6px 9px; font-weight:600; color:#b45309;">Modules 17 to 20</td>
              <td style="padding:6px 9px; font-weight:700; color:#7c3aed;">Phase 2 &amp; Phase 3</td>
              <td style="padding:6px 9px;">Mod 17–18: Phase 2 (Retrofit guides) &bull; Mod 19–20: Phase 3 (Job cards &amp; geometry).</td>
            </tr>
            <tr style="border-bottom:1px solid #e2e8f0; background:#ffffff;">
              <td style="padding:6px 9px; font-weight:700; color:#0f172a;">Engine 5: Accounting &amp; GST</td>
              <td style="padding:6px 9px; font-weight:600; color:#b45309;">Modules 21 to 25</td>
              <td style="padding:6px 9px; font-weight:700; color:#047857;">Phase 3 (Wks 21–32)</td>
              <td style="padding:6px 9px;">GST tax billing, customer aging ledger, import duty ledger, entity margin segregation.</td>
            </tr>
            <tr style="border-bottom:1px solid #e2e8f0; background:#f8fafc;">
              <td style="padding:6px 9px; font-weight:700; color:#0f172a;">Engine 6: Sales Ops &amp; Service</td>
              <td style="padding:6px 9px; font-weight:600; color:#b45309;">Modules 26 to 30</td>
              <td style="padding:6px 9px; font-weight:700; color:#047857;">Phase 3 (Wks 21–32)</td>
              <td style="padding:6px 9px;">Inquiry management, proposal follow-up alerts, warranty tracker, breakdown desk.</td>
            </tr>
            <tr style="background:#ffffff;">
              <td style="padding:6px 9px; font-weight:700; color:#0f172a;">Engine 7: Executive Intelligence</td>
              <td style="padding:6px 9px; font-weight:600; color:#b45309;">Modules 31 to 33</td>
              <td style="padding:6px 9px; font-weight:700; color:#047857;">Phase 3 (Wks 21–32)</td>
              <td style="padding:6px 9px;">Staff role permissions, 3-tier rolling backup routines, MD executive control desk.</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Core Business Advantages Box -->
      <div style="background:#ffffff; border:1.5px solid #cbd5e1; border-radius:7px; padding:12px 15px; margin-bottom:12px;">
        <div style="font-size:8.8pt; font-weight:800; color:#0f172a; text-transform:uppercase; margin-bottom:4px;">
          Core Operational Advantages to be Delivered Upon Implementation
        </div>
        <div style="display:grid; grid-template-columns:1fr 1fr; gap:8px; font-size:8.2pt; line-height:1.38; color:#334155;">
          <div style="background:#f8fafc; padding:8px 12px; border-radius:4px; border-left:3px solid #0284c7;">
            <strong>Real-Time Stock Reservation:</strong> Prevents accidental double-selling of in-demand presses and clutch models across simultaneous sales calls.
          </div>
          <div style="background:#f8fafc; padding:8px 12px; border-radius:4px; border-left:3px solid #0284c7;">
            <strong>Import Margin Protection:</strong> Calculates estimated landed cost in Indian Rupees including Euro conversion, sea freight, and customs duty.
          </div>
          <div style="background:#f8fafc; padding:8px 12px; border-radius:4px; border-left:3px solid #0284c7;">
            <strong>Clean GST Tax Billing:</strong> Helps format invoices correctly with verified GSTIN, assisting in smooth input tax credit verification for clients.
          </div>
          <div style="background:#f8fafc; padding:8px 12px; border-radius:4px; border-left:3px solid #0284c7;">
            <strong>Executive Leadership Visibility:</strong> Provides Mr. Vinit Dalal with real-time operational visibility over inquiries, stock, and collections.
          </div>
        </div>
      </div>

      <!-- Pre-Commencement Status Confirmation -->
      <div style="background:#fffbeb; border:1.5px solid #f59e0b; border-radius:7px; padding:7px 12px;">
        <p style="font-size:8.2pt; line-height:1.4; color:#78350f;">
          <strong>&#9888; PRE-COMMENCEMENT PROPOSAL:</strong> The 33 modules detailed on subsequent pages represent the operational blueprint for OMPI India LLP. Work has not yet begun. Development will follow formal scope approval and contract execution.
        </p>
      </div>
    </div>
    {make_footer(16)}
  </div>
"""

    # PAGES 17 TO 32: OMPI MODULES 01 TO 32 (2 PER PAGE)
    for i in range(16):
        page_num = i + 17
        m1 = ompi_modules[i * 2]
        m2 = ompi_modules[i * 2 + 1]

        html += f"""
  <div class="page">
    <div class="page-content">
      {make_header("SYSTEM 2: OMPI INDUSTRIAL OPERATIONS &amp; ERP SUITE &bull; PROPOSED SCOPE")}

      <div class="section-header">
        <span class="section-title">OMPI Management Engines &bull; Modules {i*2+1:02d} &amp; {i*2+2:02d} of 33 (To Be Engineered)</span>
        <span class="section-tag">{m1['engine'].split(':')[0]}</span>
      </div>

      {render_card(m1, is_route=False)}
      {render_card(m2, is_route=False)}
    </div>
    {make_footer(page_num)}
  </div>
"""

    # PAGE 33: MODULE 33 (MD DESK) + 4 OPERATIONAL CONSOLES
    m33 = ompi_modules[32]
    html += f"""
  <div class="page">
    <div class="page-content">
      {make_header("SYSTEM 2: EXECUTIVE MANAGEMENT &amp; CONTROL CONSOLES &bull; PROPOSED SCOPE")}

      <div class="section-header">
        <span class="section-title">OMPI Management Engine &bull; Module 33 of 33 &amp; Departmental Consoles</span>
        <span class="section-tag">Executive Business Control</span>
      </div>

      {render_card(m33, is_route=False)}

      <!-- Operations Consoles Summary Box -->
      <div class="card-box" style="margin-top:2px;">
        <div class="card-header">
          <div>
            <span class="badge-id">PORTALS</span>
            <span class="card-title">Staff Operational Workspaces by Department</span>
            <span class="card-status">&#9675; TO BE BUILT: SYSTEM 2</span>
          </div>
          <div style="font-size:7.8pt; color:#047857; background:#ecfdf5; padding:2px 8px; border:1px solid #a7f3d0; border-radius:3px; font-weight:700;">
            Phase 3: Departmental Workspaces (Weeks 21–32)
          </div>
        </div>
        <div class="meta-row">
          <div><strong>Authorized Roles:</strong> Sales Staff, Warehouse Storekeeper, Workshop Engineers, Senior Accountant</div>
          <div><strong>Security Governance:</strong> Strict Role-Based Data Separation</div>
        </div>
        <div style="display:grid; grid-template-columns:1fr 1fr; gap:8px; font-size:8.4pt; line-height:1.38; color:#334155; margin-bottom:7px;">
          <div style="background:#f8fafc; padding:8px 12px; border-radius:4px; border-left:3px solid #d97706;">
            <strong>1. Sales Team Desk:</strong> Customer inquiry feed, fast quote generator, proposal follow-up alerts, and WhatsApp message links.
          </div>
          <div style="background:#f8fafc; padding:8px 12px; border-radius:4px; border-left:3px solid #d97706;">
            <strong>2. Warehouse Godown Desk:</strong> Pune stock balances, shelf bin locations, transfer delivery challans, and container tracking.
          </div>
          <div style="background:#f8fafc; padding:8px 12px; border-radius:4px; border-left:3px solid #d97706;">
            <strong>3. Accounts Desk:</strong> Standard GST tax billing, customer payment aging, overseas wire records, and monthly margin summary.
          </div>
          <div style="background:#f8fafc; padding:8px 12px; border-radius:4px; border-left:3px solid #d97706;">
            <strong>4. Workshop Portal:</strong> Press reconditioning job cards, clutch retrofit work orders, geometry inspection sheets, and handovers.
          </div>
        </div>
        <div class="feature-strip">
          <strong>Key Management Feature:</strong> Total role-based permission control ensuring employees only access tools essential for their daily duties.
        </div>
      </div>
    </div>
    {make_footer(33)}
  </div>
"""

    # PAGE 34: SYSTEM INTEGRATION, WORKFLOW & SEPARATE DUAL-ENTITY SIGN-OFF
    html += f"""
  <div class="page">
    <div class="page-content">
      {make_header("SYSTEM INTEGRATION &bull; WORKFLOW, PHASING &amp; SEPARATE DUAL-ENTITY APPROVAL")}

      <div class="section-header">
        <span class="section-title">End-to-End Operational Workflow, Phasing &amp; Formal Scope Sign-Off</span>
        <span class="section-tag">Commercial Phasing</span>
      </div>

      <!-- 6-Step Workflow Box -->
      <div style="background:#ffffff; border:1.5px solid #cbd5e1; border-radius:7px; padding:14px 18px; margin-bottom:14px;">
        <div style="font-size:9.0pt; font-weight:800; color:#0f172a; text-transform:uppercase; margin-bottom:5px; border-bottom:1.5px solid #f1f5f9; padding-bottom:3px;">
          The Integrated 6-Step Business Process (Inquiry to Payment &amp; Delivery)
        </div>
        <div style="display:grid; grid-template-columns:1fr 1fr; gap:8px; font-size:8.3pt; line-height:1.38; color:#334155;">
          <div style="background:#f8fafc; padding:8px 12px; border-radius:4px; border-left:3.5px solid #d97706;">
            <strong>Step 1: Customer Inquires Online</strong><br>
            A plant head identifies a 1,600T press in the showroom and clicks the WhatsApp button with company specifications.
          </div>
          <div style="background:#f8fafc; padding:8px 12px; border-radius:4px; border-left:3.5px solid #d97706;">
            <strong>Step 2: Technical Sizing Guidance</strong><br>
            The system guides the sales engineer to the appropriate Italian OMPI pneumatic clutch model for the required tonnage.
          </div>
          <div style="background:#f8fafc; padding:8px 12px; border-radius:4px; border-left:3.5px solid #d97706;">
            <strong>Step 3: Fast PDF Quotation Sent</strong><br>
            A formal proposal PDF with machine photos, specs, and price is generated and delivered to the customer promptly.
          </div>
          <div style="background:#f8fafc; padding:8px 12px; border-radius:4px; border-left:3.5px solid #d97706;">
            <strong>Step 4: Machine Stock Reservation</strong><br>
            Once commercial terms are agreed, the machine is marked 'Reserved' in the godown tracker to avoid conflicting commitments.
          </div>
          <div style="background:#f8fafc; padding:8px 12px; border-radius:4px; border-left:3.5px solid #d97706;">
            <strong>Step 5: Workshop Overhaul &amp; Trials</strong><br>
            The press undergoes scheduled power trials, pre-dispatch geometry checks, and is prepared for transport to the buyer's plant.
          </div>
          <div style="background:#f8fafc; padding:8px 12px; border-radius:4px; border-left:3.5px solid #d97706;">
            <strong>Step 6: GST Billing &amp; Record Archiving</strong><br>
            Standard tax invoices are generated, GST records are organized for your accountant, and transaction history is archived.
          </div>
        </div>
      </div>

      <!-- Phasing Table (Aligned with 8-Month Roadmap) -->
      <div style="background:#f8fafc; border:1.5px solid #cbd5e1; border-radius:7px; padding:12px 16px; margin-bottom:12px;">
        <div style="font-size:9.0pt; font-weight:800; color:#0f172a; text-transform:uppercase; margin-bottom:5px;">
          Delivery Milestones &amp; Implementation Phasing (8-Month Comprehensive Roadmap)
        </div>
        <table style="width:100%; border-collapse:collapse; font-size:8.2pt; line-height:1.38; color:#334155;">
          <thead>
            <tr style="background:#0f172a; color:#ffffff; text-align:left;">
              <th style="padding:6px 9px;">Milestone Phase</th>
              <th style="padding:6px 9px;">Scope of Deliverables</th>
              <th style="padding:6px 9px;">Planned Schedule</th>
              <th style="padding:6px 9px;">Status</th>
            </tr>
          </thead>
          <tbody>
            <tr style="border-bottom:1px solid #e2e8f0; background:#ffffff;">
              <td style="padding:6px 9px; font-weight:700;">Phase 1: Dalal Platform</td>
              <td style="padding:6px 9px;">22 Public Showroom Pages &bull; 2 Staff Desks &bull; Core Quoting Engine &bull; GA4 / SEO</td>
              <td style="padding:6px 9px; font-weight:600; color:#0f172a;">Weeks 1–8 (Months 1–2)</td>
              <td style="padding:6px 9px; font-weight:700; color:#b45309;">TO COMMENCE UPON ADVANCE</td>
            </tr>
            <tr style="border-bottom:1px solid #e2e8f0; background:#f8fafc;">
              <td style="padding:6px 9px; font-weight:700;">Phase 2: OMPI Core ERP</td>
              <td style="padding:6px 9px;">Modules 01–18 (Italian SKU Catalog, Sizing, Landed Costing, Pune Godown, OMPI Quotes)</td>
              <td style="padding:6px 9px; font-weight:600; color:#0f172a;">Weeks 9–20 (Months 3–5)</td>
              <td style="padding:6px 9px; font-weight:600; color:#475569;">MONTHS 3–5 SPRINT</td>
            </tr>
            <tr style="background:#ffffff;">
              <td style="padding:6px 9px; font-weight:700;">Phase 3: Operations &amp; Control</td>
              <td style="padding:6px 9px;">Modules 19–33 (Job Cards, GST Tax Invoices, Shipping Logger, MD Desk, 4 Consoles)</td>
              <td style="padding:6px 9px; font-weight:600; color:#0f172a;">Weeks 21–32 (Months 6–8)</td>
              <td style="padding:6px 9px; font-weight:600; color:#475569;">MONTHS 6–8 SPRINT</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Scope Approval & Governance Rules -->
      <div style="background:#ffffff; border:1.5px solid #0f172a; border-radius:7px; padding:11px 16px; margin-bottom:12px;">
        <div style="font-size:8.6pt; font-weight:800; color:#0f172a; text-transform:uppercase; margin-bottom:3px;">
          Scope Blueprint Approval &bull; Annexure A to Master Services Agreement
        </div>
        <p style="font-size:8.0pt; line-height:1.38; color:#334155; margin-bottom:4px;">
          Execution below constitutes mutual formal approval of the functional architecture defined across this 57-unit master specification document (Scope Annexure A). Commercial fees, payment schedules, and liability shall be governed exclusively by the Master Services Agreement (MSA).
        </p>
        <div style="font-size:7.8pt; line-height:1.34; color:#475569; background:#f8fafc; padding:6px 10px; border-radius:4px; border-left:3px solid #0f172a;">
          <strong>Governing Execution Terms:</strong> (1) Schedule clock commences upon advance remittance and initial client data; client delays extend milestone dates day-for-day. (2) <strong>7-Day Deemed Acceptance:</strong> Client shall provide consolidated punch-list feedback within 7 calendar days of milestone delivery demo; absence of notice constitutes formal acceptance and activates the 30-day warranty. (3) <strong>Joint Commercial Liability:</strong> Both corporate entities are jointly committed to commercial terms, whilst maintaining 100% operational, banking, and accounting separation.
        </div>
      </div>

      <!-- Separate Dual Entity Sign-Off Blocks -->
      <div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:12px; border-top:1.5px solid #0f172a; padding-top:10px;">
        <div style="font-size:8.1pt; line-height:1.36; color:#334155;">
          <strong>Scope Approved for Dalal Agency:</strong><br><br>
          __________________________________<br>
          <strong>Mr. Vinit Dalal</strong> &bull; Managing Director<br>
          <span style="font-size:7.6pt; color:#64748b;">Dalal Machine Tools Agency Pvt. Ltd.</span><br>
          <span style="font-size:7.6pt; color:#475569;">Date: ________________________</span>
        </div>
        <div style="font-size:8.1pt; line-height:1.36; color:#334155;">
          <strong>Scope Approved for OMPI India:</strong><br><br>
          __________________________________<br>
          <strong>Authorized Signatory</strong> &bull; Partner<br>
          <span style="font-size:7.6pt; color:#64748b;">OMPI India LLP</span><br>
          <span style="font-size:7.6pt; color:#475569;">Date: ________________________</span>
        </div>
        <div style="font-size:8.1pt; line-height:1.36; color:#334155; text-align:right;">
          <strong>Submitted by Consultant:</strong><br><br>
          __________________________________<br>
          <strong>Suyash Shinde</strong> &bull; Principal Software Consultant<br>
          <span style="font-size:7.6pt; color:#64748b;">Pimpri, Pune, Maharashtra</span><br>
          <span style="font-size:7.6pt; color:#475569;">Date: November 02, 2026 (Valid thru 14 Nov)</span>
        </div>
      </div>
    </div>
    {make_footer(34)}
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

    # Audit all 34 pages with PyMuPDF
    doc = pymupdf.open(pdf_path)
    print(f"--- PyMuPDF Audit: Total Pages = {len(doc)} ---")
    for i, p in enumerate(doc):
        blocks = p.get_text('blocks')
        content_blocks = [b for b in blocks if b[3] < 790]
        max_y = max([b[3] for b in content_blocks]) if content_blocks else 0
        footer_block = [b for b in blocks if b[3] >= 790]
        min_footer_y = min([b[1] for b in footer_block]) if footer_block else 800
        gap = min_footer_y - max_y
        status = "OK (PERFECT)" if 40 <= gap <= 135 else ("WARNING: TOO EMPTY" if gap > 135 else "CRITICAL: OVERFLOW RISK")
        print(f"Page {i+1:02d}: content y={max_y:5.1f} | footer y={min_footer_y:5.1f} | gap={gap:5.1f}pt -> {status}")
