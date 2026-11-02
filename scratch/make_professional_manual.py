# -*- coding: utf-8 -*-
import os, sys, subprocess, shutil

out_html = "d:/st.ourhtmldemo.com/DALAL_AND_OMPI_57_PAGES_AND_MODULES_MASTER_SPECIFICATION.html"
out_pdf = "d:/st.ourhtmldemo.com/DALAL_AND_OMPI_57_PAGES_AND_MODULES_MASTER_SPECIFICATION.pdf"

# --- 24 DALAL CUSTOMER & OPERATIONS ROUTES DATA ---
routes = [
    # Page 2: Routes 1 to 4
    (
        "ROUTE-01", "Homepage & Industrial Asset Portal", "/index.html", "Plant Owners, Forging Heads, Auto Tier-1 Directors",
        "Capital equipment transactions (Rs. 50 Lakh to Rs. 4.5 Crore) fail at discovery when portals lack verifiable physical yard inventory. This endpoint establishes operational authenticity, proving physical machine availability in Pune and eliminating broker disintermediation.",
        "User lands via organic/direct acquisition -> filters by tonnage classification (<500T, 500T-1000T, 1000T+) -> evaluates technical specifications -> generates real-time CIF port vs Pune yard cost comparison -> initiates structured WhatsApp RFQ to Managing Director.",
        [
            ("Live Yard Ground Indicators", "Visual indicators verifying physical ground positioning at Pune Stockyard for immediate power-on inspection."),
            ("Precision Hairline Spec Grid", "2x2 mathematical crosshair layout displaying Tonnage, Manufacture Year, Model Code, and Yard Inspection status."),
            ("CIF High Seas Comparison", "Analytical financial matrix demonstrating 8% to 15% landed duty savings via direct High Seas port clearance."),
            ("Floating Compare Selector", "Lightweight selection mechanism supporting 4-press comparative evaluation across stroke, daylight, and bed area.")
        ],
        "machine_id, category_id, tonnage_tons, stroke_mm, daylight_mm, motor_hp, mfg_year, origin_oem, ground_status"
    ),
    (
        "ROUTE-02", "Corporate Profile & Industrial Heritage", "/about.html", "Bank Valuers, Joint Venture Audit Teams, CFOs",
        "Institutional capital purchase approvals require formal corporate verification, audited leadership credentials, and physical facility documentation to satisfy bank asset financing and statutory compliance audits.",
        "Presents corporate credentials of Dalal Machine Tools Agency Pvt. Ltd., Managing Director Mr. Vinit Dalal's engineering background, dual office locations (Mumbai Tardeo & Pune Stockyard), and technical partnership with OMPI Italy.",
        [
            ("Corporate Governance Dossier", "Official incorporation profile, executive management oversight, and statutory tax compliance credentials."),
            ("Facility Infrastructure Dossier", "Detailed profile of Pune Industrial Machinery Yard supporting 50-ton overhead crane handling and trial pits."),
            ("OMPI Italy Technical Alliance", "Official documentation of technical authorization for Italian pneumatic clutch-brake sales, retrofits, and spares."),
            ("Machinery Sourcing Network", "Operational map illustrating European and Asian industrial dismantling and direct high-seas import pipelines.")
        ],
        "corporate_cin, registered_office_tardeo, stockyard_pune_corridor, ompi_partnership_id, valuer_inspection_protocol"
    ),
    (
        "ROUTE-03", "Import, Rigging & Retrofit Engineering", "/services.html", "Plant Maintenance Managers, Chief Engineers",
        "Heavy forging and stamping presses cannot operate safely with obsolete mechanical dog clutches. Buyers require turnkey engineering assurance covering foundation pits, crankshaft boring, and pneumatic clutch modernization.",
        "Catalogs industrial engineering services: OMPI pneumatic clutch conversions, press alignment audits, high-tonnage multi-axle rigging, foundation pit excavation, and genuine Italian spare parts provisioning.",
        [
            ("Clutch Modernization Specs", "Engineering comparative analysis between rigid dog clutches and modern OMPI fail-safe pneumatic clutch-brakes."),
            ("5-Stage Commissioning SOP", "Standard operating sequence: Yard audit -> Crankshaft machining -> Pneumatics -> PLC safety interlock -> 100-cycle trial."),
            ("Crankshaft Alignment Standards", "Tolerancing standards for journal re-machining and runout limits (<0.05mm) verified with dial indicators."),
            ("Emergency Spares Support", "Guaranteed dispatch protocols for high-wear friction discs, dual safety valves, and rotary unions from Pune stock.")
        ],
        "service_tier, machine_serial_ref, clutch_model_ref, crankshaft_bore_mm, flywheel_inertia_gd2, runout_tolerance"
    ),
    (
        "ROUTE-04", "Machinery Catalog & Parametric Search", "/category.html", "Procurement Directors, Sourcing Managers",
        "Machinery procurement teams operate under rigid production requirements (exact stroke, tonnage, bed dimensions). Flat product lists create excessive search friction and delayed sourcing decisions.",
        "Multi-facet parametric search filtering across 26 industrial machinery categories (Hot Forging, Mechanical Stamping, Hydraulic Presses, Horizontal Borers) with client-side sub-second response times.",
        [
            ("26 Industrial Categories", "Granular categorization spanning closed-die forging, knuckle joint coining, C-frame, borer, and shears."),
            ("Tonnage Filter Chips", "Fast-action parametric filters segmenting inventory into <500T, 500T-1000T, and 1000T-4000T heavy forging presses."),
            ("Origin OEM Categorization", "Direct grouping by premier global builders including Aida, Schuler, TMP Voronezh, Komatsu, and Erfurt."),
            ("Real-Time Availability Filter", "Instant toggle isolating ready stock in Pune Yard from European staging hubs and transit consignments.")
        ],
        "category_slug, tonnage_min_max, bed_width_min, stroke_min, oem_filter, location_filter, active_record_count"
    ),

    # Page 3: Routes 5 to 8
    (
        "ROUTE-05", "Machine Engineering Dossier (PDP)", "/product.html", "Chief Technical Officers, Tooling Engineers",
        "Technical directors will not approve RFQs without comprehensive mechanical specifications, electrical load requirements, dimensional drawings, and foundation pit clearance profiles.",
        "Detailed engineering presentation of individual machinery units. Displays high-resolution photography, dimensional tables, motor requirements, inspection certificates, and direct WhatsApp RFQ dispatch.",
        [
            ("Comprehensive Spec Matrix", "Complete mechanical parameters: Capacity, Stroke, Daylight, Shut Height, Bed Dimensions, SPM, Motor kW."),
            ("Yard Inspection Certificate", "Detailed technical condition report covering gear teeth wear, clutch lining thickness, and bed flatness."),
            ("Direct WhatsApp RFQ Payload", "Pre-populates exact Machine ID, Model, Tonnage, and Make into direct WhatsApp messaging to Managing Director."),
            ("Dimensional Clearance Profile", "Outlines total press height, pit depth, overhead crane clearance, and total shipping weight in metric tons.")
        ],
        "sku_id, oem_make, model_code, nominal_force_tons, stroke_mm, daylight_mm, bed_l_w_mm, spm_range, total_weight_tons"
    ),
    (
        "ROUTE-06", "Brand New Machinery & Turnkey Lines", "/brand-new-machinery.html", "Industrial Investors, High-Volume Tier-1 Plants",
        "High-volume automotive tier-1 suppliers with multi-year OEM contracts frequently require brand-new, zero-hour machinery backed by manufacturer warranties rather than reconditioned assets.",
        "Showcases new heavy machinery lines, progressive stamping presses, and automated forging cells sourced directly from global manufacturing partners with full factory warranties.",
        [
            ("Turnkey Stamping Cells", "Complete integrated production cells including automated decoilers, straighteners, and servo feeder lines."),
            ("Factory Warranty Protocols", "12-month to 24-month OEM performance guarantees covering main drive gears, eccentric shafts, and electrics."),
            ("Custom Foundation Engineering", "Engineering support for foundation pit design, dynamic load isolation pads, and vibration dampeners."),
            ("Automated Die Change Systems", "Integrated hydraulic die clamping, rolling bolster tracks, and quick-change tooling mechanisms.")
        ],
        "line_id, press_type, capacity_tons, feeder_width_mm, spm_max, oem_warranty_months, foundation_drawing_ref"
    ),
    (
        "ROUTE-07", "Shipment, Yard & Rigging Archive", "/gallery.html", "Logistics Managers, Insurance Underwriters, Plant Heads",
        "Third-party inspection agencies and corporate buyers demand verified physical evidence of heavy transport capability, safe handling of 50-to-200-ton press frames, and yard storage conditions.",
        "Photographic and video archive documenting heavy press rigging, hydraulic gantry lifting, multi-axle hydraulic trailer transport, and physical stock in the Pune warehouse yard.",
        [
            ("Heavy Rigging Case Studies", "High-tonnage documentation showing hydraulic strand-jacking, tilt-up operations, and pit lowering."),
            ("Multi-Axle Transport Records", "Visual records of heavy hydraulic trailer transit from Nhava Sheva (JNPT) to Pune and customer factories."),
            ("Pune Yard Storage Verification", "High-bay overhead crane footage confirming covered, moisture-protected storage of mechanical press inventory."),
            ("OEM Component Inspection", "Close-up visual audits of gear teeth profiles, flywheel bearings, and refurbished pneumatic clutch assemblies.")
        ],
        "logistics_job_id, tare_weight_tons, axle_count, rigger_team_id, jnpt_clearance_date, yard_arrival_timestamp"
    ),
    (
        "ROUTE-08", "Headquarters, Facility & Direct RFQ", "/contact.html", "Procurement Executives, Factory Owners, Sourcing Directors",
        "Inbound capital machinery inquiries must be authenticated and routed immediately to senior leadership. Generic web forms create lead drop-off and delayed technical consultations.",
        "Dual headquarters validation interface (Mumbai Registered Office & Pune Stockyard) featuring a 40px padded B2B quotation console pre-configured to notify Managing Director Mr. Vinit Dalal directly.",
        [
            ("Dual Facility Verification", "Mumbai Tardeo registered corporate office address and Pune industrial stockyard GPS navigation coordinates."),
            ("Direct Executive Routing", "Inquiry form pre-configured to dispatch instant SMS and WhatsApp notifications directly to executive leadership."),
            ("Technical Parameter Capture", "Structured input fields capturing required press tonnage, bed dimensions, delivery target, and application type."),
            ("Physical Trial Appointment", "Direct calendar scheduling for on-site power-on machinery inspection and dry-cycle testing at Pune Yard.")
        ],
        "lead_name, company_name, gstin, phone, email, machine_category_interest, required_tonnage, preferred_trial_date"
    ),

    # Page 4: Routes 9 to 12
    (
        "ROUTE-09", "Express Plant RFQ & Sizing Consultation", "/contact-2.html", "Emergency Maintenance Teams, Plant Project Heads",
        "Production line breakdown situations and urgent capacity expansions demand fast-track technical sizing without navigating comprehensive multi-step forms.",
        "Streamlined quotation interface optimized for mobile and rapid technical intake, capturing critical press breakdown parameters and immediate delivery constraints.",
        [
            ("Rapid Intake Form", "Minimal-friction input fields capturing plant location, current press tonnage, and immediate delivery deadlines."),
            ("Technical Specification Upload", "Direct attachment portal for plant foundation drawings, broken component photos, and component blueprints."),
            ("Emergency Spare Part Triage", "Specialized intake for emergency clutch-brake replacements, friction linings, and dual safety valves."),
            ("Direct Executive Hotline", "Direct one-touch phone and WhatsApp communication channels to engineering management.")
        ],
        "rapid_rfq_id, urgency_level_code, required_delivery_days, press_make_model, drawing_upload_url, phone_verified"
    ),
    (
        "ROUTE-10", "Industrial FAQs & Import Compliance Guide", "/faqs.html", "CFOs, Corporate Legal Counsel, Import Managers",
        "High Seas Sales and heavy machinery imports involve complex GST regulations, customs clearance procedures, and trial logistics that require formal compliance guidance.",
        "Authoritative knowledge base providing comprehensive guidance on High Seas Sales agreements under Section 2(4) of CST Act, Bill of Entry documentation, GST ITC eligibility, and trial logistics.",
        [
            ("High Seas Agreement Protocol", "Step-by-step breakdown of title transfer while goods are on high seas to avoid intermediate sales tax."),
            ("GST Input Credit Compliance", "Documentation requirements for seamless 18% GST input tax credit (ITC) claiming on capital asset purchase."),
            ("Customs Valuation & Bill of Entry", "Guidance on Basic Customs Duty (BCD), Social Welfare Surcharge (SWS), and IGST assessment at Nhava Sheva."),
            ("On-Site Trial & Inspection Rights", "Legal protocols governing buyer's right to live power trials and dimensional verification before dispatch.")
        ],
        "faq_category, legal_statute_ref, gst_compliance_rule, customs_tariff_heading, trial_terms_clause"
    ),
    (
        "ROUTE-11", "Client Endorsements & Installation Proof", "/testimonial.html", "Corporate Investment Committees, Factory Directors",
        "Capital investment committees require third-party peer validation from reputable forging, stamping, and automotive component plants before allocating multi-crore budgets.",
        "Curated portfolio of authenticated client endorsements, completion certificates, and project sign-offs from plant heads across key manufacturing hubs (Pune, Rajkot, Chennai, NCR).",
        [
            ("Automotive Tier-1 Case Studies", "Verified installation summaries from tier-1 stampers manufacturing structural chassis and body panels."),
            ("Heavy Forge Shop Endorsements", "Performance validations from closed-die forging plants running 1600T to 2500T hot forging presses."),
            ("Clutch Retrofit Testimonials", "Operational reports documenting 40% reduction in maintenance downtime following OMPI pneumatic conversions."),
            ("Repeat Buyer Tracking", "Highlighting multi-year client relationships and repeat machinery acquisitions across industrial conglomerates.")
        ],
        "testimonial_id, client_company, plant_location, machine_purchased_ref, commissioning_year, client_head_designation"
    ),
    (
        "ROUTE-12", "High Seas CIF Tariffs & Cost Breakdown", "/pricing.html", "Finance Directors, Plant Valuers, Sourcing Heads",
        "Large industrial buyers need complete financial transparency to evaluate the cost advantages of direct import (CIF/High Seas) versus purchasing local yard stock.",
        "Analytical financial model comparing CIF direct port shipments against local stockyard deliveries, detailing Basic Customs Duty, port handling, freight, and net landed costs.",
        [
            ("Comparative Cost Engine", "Side-by-side cost breakdown: Ex-Europe price -> Ocean Freight -> Customs Duty -> Port Clearing -> Net Landed."),
            ("8% to 15% Cost Savings Proof", "Clear financial modeling demonstrating direct savings realized through High Seas title transfer."),
            ("Port Handling & Demurrage Buffer", "Transparent schedule of port handling, container de-stuffing, and crane offloading fees at JNPT."),
            ("Working Capital & Milestone Schedule", "Cash flow projection comparing LC-backed import financing against milestone payments for yard stock.")
        ],
        "cif_quote_id, base_currency_eur, exchange_rate_inr, ocean_freight_usd, bcd_percent, igst_percent, port_clearing_inr"
    ),

    # Page 5: Routes 13 to 16
    (
        "ROUTE-13", "Industrial Journal & Forging Hub", "/blog.html", "Maintenance Engineers, Tooling Designers, Plant Heads",
        "Search engines and plant engineers actively research solutions for mechanical press maintenance, clutch conversion economics, and foundation engineering.",
        "Technical engineering publication platform hosting in-depth articles on metal forming technology, preventive maintenance protocols, and modern press automation.",
        [
            ("Engineering Article Archive", "Peer-reviewed technical guides on press tonnage calculation, die cushion sizing, and lubrication maintenance."),
            ("Retrofit Economic Analyses", "Data-driven studies evaluating payback periods for pneumatic clutch retrofits versus dog clutch failures."),
            ("Safety Compliance Standards", "Analysis of EN 692 and OSHA press safety standards, focusing on dual valve monitoring and light curtain integration."),
            ("Industry Trend Reports", "Market updates on global heavy press availability, European industrial auctions, and scrap steel economics.")
        ],
        "article_id, title_slug, author_credentials, category_tag, read_time_mins, publication_date, primary_keyword"
    ),
    (
        "ROUTE-14", "Lead Visual Engineering Article", "/blog-single.html", "Mechanical Maintenance Heads, Safety Officers",
        "Maintenance teams require rigorous, step-by-step technical blueprints when executing mechanical-to-pneumatic clutch conversions in-house or via Dalal engineering.",
        "Deep-dive technical article providing comprehensive mechanical calculations, flywheel machining tolerances, pneumatic circuit schematics, and PLC safety interlock wiring.",
        [
            ("Flywheel Inertia Calculations", "Mathematical formulas for calculating flywheel rotational energy (GD2) and required clutch torque rating."),
            ("Crankshaft Machining Tolerances", "Dimensional guidelines for turning crankshaft journals to match OMPI clutch bore tolerances (H7/g6)."),
            ("Pneumatic Circuit Schematics", "Piping diagrams specifying accumulator volume, dual-valve exhaust ports, and operating pressure ranges (5.5-6.0 bar)."),
            ("Electrical Interlock Protocols", "Control logic integration connecting press emergency stops, rotary cams, and clutch dual-valve monitoring.")
        ],
        "article_slug, technical_topic_id, torque_formula_ref, schematic_drawing_url, safety_standard_ref"
    ),
    (
        "ROUTE-15", "Turnkey Plant Retrofit Case Study", "/blog-large-image.html", "Project Directors, Capital Investment Committees",
        "Proves execution capability on multi-ton forging press overhauls through detailed photographic documentation and verified operational metrics.",
        "Visual case study documenting the complete overhaul of a 2500T hot forging press from European factory decommissioning to live Pune commissioning.",
        [
            ("Decommissioning & Rigging Log", "Visual log showing European factory dismantling, match-marking of parts, and containerized packing."),
            ("Pune Yard Reconditioning", "Photographic documentation of ultrasonic crack detection, eccentric bushing replacement, and gear teeth inspection."),
            ("OMPI Clutch-Brake Installation", "Detailed shots of the pneumatic clutch-brake unit mounted to the primary drive shaft with rotary union."),
            ("Production Trial Sign-Off", "Final production verification showing 100-cycle dry run, tonnage load cell testing, and commercial handover.")
        ],
        "case_study_id, machine_tonnage, client_sector, overhaul_duration_weeks, ultrasonic_test_cert_id, handover_signoff_date"
    ),
    (
        "ROUTE-16", "Projects & Rigging Portfolio Overview", "/projects.html", "EPC Contractors, Factory Expansion Teams",
        "Demonstrates breadth of completed industrial installations, plant relocations, and modernization projects across diverse manufacturing sectors.",
        "Comprehensive project directory showcasing executed heavy machinery installations, crankshaft re-boring operations, and turnkey press modernizations.",
        [
            ("Multi-Sector Project Grid", "Filterable overview covering automotive, heavy forging, railway component, and defense manufacturing installations."),
            ("Capacity Classification", "Categorization spanning light stamping (<300T), medium press lines (300T-1000T), and heavy forging (1000T-4000T)."),
            ("Scope of Work Summary", "Clear breakdown of deliverables: supply, transport, foundation engineering, electrical panel, or OMPI retrofit."),
            ("Geographic Execution Map", "Documented track record of executed installations across Maharashtra, Gujarat, Tamil Nadu, and NCR.")
        ],
        "project_id, sector_code, press_capacity_range, execution_scope, site_location_city, completion_year"
    ),

    # Page 6: Routes 17 to 20
    (
        "ROUTE-17", "Heavy Rigging & Logistics Project Detail", "/projects-single.html", "Rigging Engineers, Transport Contractors, Plant Heads",
        "Validates technical competency in handling indivisible 80-to-150-ton machine components requiring specialized hydraulic gantry lifting and route permits.",
        "Detailed engineering case study examining the transportation and installation of a 120-ton press frame, detailing axle load distribution and rigging methodology.",
        [
            ("Axle Load Calculations", "Mathematical distribution of 120-ton payload across 8-axle hydraulic puller trailers to comply with NHAI norms."),
            ("Hydraulic Gantry Setup", "Step-by-step rigging protocol using 200-ton hydraulic gantries for vertical lifting and foundation pit lowering."),
            ("Foundation Bolt Grouting", "Specification of non-shrink epoxy grout mixes and torque settings for anchor tie-rods holding press uprights."),
            ("Route Obstacle Management", "Logistics protocol managing state transit permits, bridge load clearances, and overhead wire lifting.")
        ],
        "project_ref, component_weight_tons, trailer_axle_config, gantry_capacity_tons, grout_compressive_strength_mpa"
    ),
    (
        "ROUTE-18", "Sector-Wise Plant Modernization", "/projects-modern.html", "Automotive Tier-1 Heads, White Goods Plant Managers",
        "Automotive and appliance manufacturers require customized press line automation (coil handling, servo feeds, transfer systems) to achieve required parts-per-minute targets.",
        "Presents specialized press automation solutions, coil feeder lines, and die-cushion upgrades tailored specifically for automotive sheet metal stampers.",
        [
            ("Automotive Stamping Upgrades", "Integration of servo feed systems, mechanical transfer bars, and optical sheet sensors on mechanical press lines."),
            ("Hydraulic Die Cushion Control", "Digital proportional pressure controls on bed die cushions to prevent sheet thinning and tearing during deep draw."),
            ("Energy Efficiency Upgrades", "Main motor drive upgrades with Variable Frequency Drives (VFD) reducing idle power consumption by up to 25%."),
            ("Line Synchronization", "Interlocking tandem press lines with automated intermediate conveyor belts and pick-and-place robots.")
        ],
        "sector_id, automation_type, cycle_time_seconds, feeder_width_range_mm, energy_reduction_percent, plc_brand"
    ),
    (
        "ROUTE-19", "Turnkey Plant Case Study Analysis", "/projects-with-filter.html", "Capital Expenditure Committees, Technical Directors",
        "Enables plant engineering directors to filter completed projects by tonnage classes matching their exact upcoming plant expansion scope.",
        "Interactive, filterable case study console allowing technical comparison of executed projects across tonnage categories, application types, and delivery models.",
        [
            ("Parametric Project Filter", "Multi-tag filtering isolating projects by tonnage (<500T, 500T-1500T, >1500T), OEM make, and conversion type."),
            ("Comparative Delivery Timelines", "Benchmarking project execution times: sourcing, maritime shipping, yard overhaul, and final plant handover."),
            ("Cost-Benefit ROI Modeling", "Verified client payback metrics showing capital cost savings compared to acquiring new machinery lines."),
            ("Downloadable Project Dossiers", "One-click access to complete project summaries with before/after photography and client sign-off records.")
        ],
        "filter_category, tonnage_band, oem_brand, overhaul_scope, roi_payback_months, pdf_download_url"
    ),
    (
        "ROUTE-20", "Tooling, Bolster Plates & Spares Hub", "/shop.html", "Purchase Officers, Mechanical Maintenance Engineers",
        "Emergency production stoppages require fast procurement of press accessories, wear parts, and tooling components without navigating machinery catalogs.",
        "Industrial spares catalog indexing bolster plates, tie-rod nuts, hydraulic overload pumps, safety dual valves, and pneumatic rotary unions.",
        [
            ("Comprehensive Spares Index", "Direct inventory access to high-wear consumables: friction discs, return springs, air seals, and valves."),
            ("Dimensional Specification Search", "Filter tooling spares by bolster dimensions, T-slot profiles, clamping slots, and pin hole configurations."),
            ("Ready-Stock Availability", "Live warehouse stock indicators confirming items ready for immediate dispatch from the Pune central warehouse."),
            ("Direct RFQ Cart Integration", "Enables maintenance engineers to assemble multi-part spare RFQ packages for bulk pricing quotes.")
        ],
        "spare_category_id, sku_code, material_grade, stock_quantity_pune, lead_time_days, application_press_type"
    ),

    # Page 7: Routes 21 to 24
    (
        "ROUTE-21", "Spares Engineering Specification (PDP)", "/shop-single.html", "Mechanical Maintenance Heads, Tool Room Engineers",
        "Tool room and maintenance engineers cannot order mechanical spares without verifying shaft diameters, spline profiles, metallurgy, and hardness ratings.",
        "Detailed spare component engineering dossier displaying dimensional CAD diagrams, material test certificates, hardening specifications, and stock status.",
        [
            ("CAD Dimensional Schemas", "Precision dimensional drawings showing bore tolerances, keyway dimensions, and mounting bolt PCDs."),
            ("Metallurgical Hardness Specs", "Material certification (EN8/EN19/42CrMo4) with core and surface induction hardening specifications (52-58 HRC)."),
            ("Press Compatibility Index", "Cross-reference list mapping the spare part to compatible press models (e.g. Aida 250T, Voronezh 2500T)."),
            ("Immediate Dispatch Trigger", "Single-click quotation trigger pre-populating part SKU, required quantity, and emergency dispatch request.")
        ],
        "part_sku, steel_grade, core_hardness_hrc, surface_treatment, bore_diameter_mm, spline_count, weight_kg, compatibility_oem"
    ),
    (
        "ROUTE-22", "RFQ Package & Multi-Item Inquiry Cart", "/shoping-cart.html", "Procurement Executives, Factory Sourcing Teams",
        "Industrial buyers frequently bundle multiple machinery lines, spare bolsters, and replacement clutch units into a single consolidated corporate RFQ.",
        "Consolidated procurement cart aggregating machinery lines, retrofit packages, and spare parts into a single structured commercial inquiry.",
        [
            ("Consolidated Line-Item List", "Review selected machinery, tooling accessories, and OMPI clutch models in a single unified view."),
            ("Quantity & Scope Customization", "Adjust required quantities and specify auxiliary scopes: supply only, supply + freight, or complete turnkey commissioning."),
            ("Commercial Holding Protocol", "Allows buyer to request a 48-hour commercial hold on ready-stock machinery while internal approvals finalize."),
            ("Seamless Checkout Handshake", "Direct transition to the structured commercial proposal submission console with pre-filled line items.")
        ],
        "cart_id, session_token, item_sku_list, scope_of_work_code, hold_requested_bool, total_line_items_count"
    ),
    (
        "ROUTE-23", "Structured RFQ Proposal Submission", "/checkout.html", "Chief Financial Officers, Senior Purchase Executives",
        "Formal B2B machinery procurement requires company tax identification (GSTIN), plant delivery addresses, and delivery timeline parameters.",
        "Commercial RFQ submission console capturing verified company tax credentials, plant unloading specifications, and formal procurement terms.",
        [
            ("Corporate Tax Validation", "Captures and validates 15-digit GSTIN, ensuring tax jurisdiction and proper B2B quotation documentation."),
            ("Plant Delivery & Crane Setup", "Records delivery address, unloading bay clearance, and availability of overhead cranes for safe de-stuffing."),
            ("Commercial Payment Terms", "Allows selection of preferred transaction structure: 100% Ex-Pune Yard, LC-backed High Seas, or Milestone Billing."),
            ("Instant PDF & Dispatch", "Generates structured procurement inquiry payload and dispatches instant copy to buyer and Dalal management.")
        ],
        "rfq_formal_id, buyer_gstin, delivery_facility_address, crane_capacity_tons, payment_preference, delivery_deadline_date"
    ),
    (
        "ROUTE-24", "Error Recovery & Intelligent Routing", "/404.html", "Any System Visitor, Mobile Sourcing Teams",
        "Broken external bookmarks, expired machinery listings, or sold inventory links cause immediate visitor abandonment if met with a generic error page.",
        "Intelligent error recovery console that analyzes the broken URL request, extracts probable machine keywords, and displays matching in-stock presses.",
        [
            ("Parametric Search Fallback", "Extracts URL parameters (e.g. 'forging', '1600T') to suggest currently available active machinery alternatives."),
            ("Top In-Stock Machinery Cards", "Displays 3 top-priority, ready-stock forging and stamping presses currently available in the Pune yard."),
            ("Direct Executive Support", "Instant WhatsApp button pre-configured to query Mr. Vinit Dalal regarding unlisted or upcoming inventory."),
            ("Full Catalog Redirection", "One-click navigation back to the 26-category machinery catalog and engineering search engine.")
        ],
        "requested_uri, parsed_keyword_tokens, suggested_category_slug, suggested_machine_id_list, recovery_click_event"
    )
]

# --- 33 OMPI INDUSTRIAL ERP MODULES DATA ---
modules = [
    # Page 8: Modules 1 to 3
    (
        "ERP-MOD-01", "Client Master & Credit Term Profiler", "Engine 1: Commercial Sales Pipeline", "Sales Directors, Financial Controllers",
        "Machinery and clutch transactions involve multi-plant corporate buyers. Operating without verified GSTINs and approved credit limits creates severe bad debt exposure and GST input credit disputes.",
        "Maintains verified corporate profiles of machinery buyers, validated 15-digit GSTINs, plant delivery addresses, allocated credit limits, and approved milestone payment templates (e.g., 30% Advance, 50% Against Dispatch, 20% Post-Installation).",
        [
            ("GSTIN Auto-Validation", "Verifies state jurisdiction codes and active tax status to prevent GST input credit rejection."),
            ("Receivables Limit Sentinel", "Blocks quote generation if client's outstanding accounts receivable exceeds their credit limit threshold."),
            ("Multi-Plant Address Book", "Maintains distinct plant addresses across industrial corridors (Pune, NCR, Chennai, Rajkot) with GST mapping.")
        ],
        "client_id, corporate_name, gstin_15, credit_limit_inr, credit_days, default_milestone_template_id, ledger_balance_inr",
        "SO Conversion (Mod 09), Invoice Engine (Mod 26)"
    ),
    (
        "ERP-MOD-02", "OMPI Technical Catalog & SKU Master", "Engine 1: Commercial Sales Pipeline", "Applications Engineers, Sales Managers",
        "Clutch-brake selections require precise engineering alignment. Selling mismatched torque models leads to catastrophic flywheel slippage or press drive-train fractures.",
        "Authoritative master repository of all Italian OMPI pneumatic clutch-brake combinations, single-acting clutches, rotary unions, and friction discs. Indexes torque ratings, shaft bores, air pressures, and CAD references.",
        [
            ("Torque & Pressure Ratings", "Indexes dynamic torque capacities from 250 Nm to 120,000 Nm across operating pressures of 5.5 to 6.0 bar."),
            ("Bore & Spline Specifications", "Specifies standard and maximum allowable bore dimensions, keyway profiles, and spline pitch standards."),
            ("Component Cross-Referencing", "Maps complete clutch-brake assemblies to internal BOM wear parts: friction discs, return springs, and seal kits.")
        ],
        "sku_code, model_series, nominal_torque_nm, max_operating_bar, min_shaft_bore_mm, max_shaft_bore_mm, cad_drawing_id",
        "Torque Sizing (Mod 16), Multi-Level BOM (Mod 11)"
    ),
    (
        "ERP-MOD-03", "Multi-Currency Landed Pricing Engine", "Engine 1: Commercial Sales Pipeline", "Commercial Managers, Managing Director",
        "OMPI units are imported from Italy in EUR. Setting domestic INR sale prices without tracking daily EUR/INR spot rates and customs duties causes severe gross margin erosion.",
        "Calculates landed costs and domestic selling prices in real time. Incorporates European OEM list prices in EUR, daily exchange rates, sea freight surcharges, Basic Customs Duty (7.5%), and target gross margins.",
        [
            ("Real-Time Exchange Hedging", "Integrates daily EUR/INR spot rates with configurable currency volatility buffer percentages."),
            ("Dynamic Customs Factoring", "Calculates landed duty: BCD (7.5%), Social Welfare Surcharge (10% of BCD), and IGST (18%)."),
            ("Margin Protection Algorithms", "Automatically calculates minimum selling price based on mandatory gross margin floor (default: 22%).")
        ],
        "sku_id, ex_factory_eur, spot_rate_eur_inr, ocean_freight_inr, bcd_amount_inr, landed_cost_inr, base_selling_price_inr",
        "Fast-Quote (Mod 04), Landed Cost Calculator (Mod 13)"
    ),

    # Page 9: Modules 4 to 6
    (
        "ERP-MOD-04", "Fast-Quote 60s PDF Engine", "Engine 1: Commercial Sales Pipeline", "Sales Engineers, Commercial Executives",
        "Delayed quotation response times cause industrial buyers to source alternative solutions. Manual quotation assembly leads to typographical pricing errors.",
        "Generates formal, branded technical quotation PDFs in under 60 seconds. Pulls verified SKU specifications, CAD outline drawings, commercial terms, and multi-tier pricing into a customer-ready proposal.",
        [
            ("Automated PDF Compilation", "Combines technical specifications, line-item pricing, and warranty terms into a formal proposal document."),
            ("CAD Outline Drawing Embed", "Automatically attaches certified dimensional diagrams matching the selected clutch model and bore size."),
            ("Milestone Payment Terms", "Includes standardized commercial terms: 30% Advance, 50% Against Dispatch, 20% Post-Installation.")
        ],
        "quote_id, client_id, sku_items_json, total_quoted_amount, discount_percent, pdf_blob_url, validity_date",
        "WhatsApp Dispatcher (Mod 10), RFQ Pipeline (Mod 05)"
    ),
    (
        "ERP-MOD-05", "RFQ Lifecycle & Visual Pipeline", "Engine 1: Commercial Sales Pipeline", "Sales Directors, Business Development Heads",
        "Unmonitored sales inquiries result in lost deals. Sales management lacks visibility into quotation bottlenecks and commercial closure rates.",
        "Visual Kanban board tracking inquiries across 6 operational stages: Inbound RFQ -> Sized -> Quoted -> PO Awaited -> Won / Lost -> Commissioned. Provides pipeline valuation and conversion analytics.",
        [
            ("6-Stage Visual Kanban", "Drag-and-drop workflow tracking inquiry progression with stage duration monitoring."),
            ("Bottleneck Aging Alerts", "Flags quotes remaining in 'PO Awaited' for more than 7 days for automated management escalation."),
            ("Pipeline Valuation Metrics", "Computes total weighted pipeline value across active stages to forecast monthly cash flows.")
        ],
        "rfq_id, current_stage_code, inquiry_date, assigned_sales_rep, total_pipeline_value_inr, win_probability_percent",
        "Fast-Quote (Mod 04), Sales Order Conversion (Mod 09)"
    ),
    (
        "ERP-MOD-06", "Machine Compatibility & Retrofit Matrix", "Engine 1: Commercial Sales Pipeline", "Applications Engineers, Field Technicians",
        "Specifying clutches for retrofits without checking press flywheel dimensions leads to expensive mounting errors, misaligned adaptors, and project delays.",
        "Technical compatibility engine mapping legacy mechanical press models (Aida, Schuler, TMP Voronezh, Godrej) to the precise OMPI pneumatic clutch-brake replacement model and adaptor plate specs.",
        [
            ("Legacy Press OEM Database", "Cross-indexes 100+ mechanical press models with their original flywheel speeds, stroke lengths, and tonnage."),
            ("Adaptor Plate Blueprinting", "Specifies required intermediate mounting flange dimensions, bolt pitch circles (PCD), and drive pin configurations."),
            ("Shaft Extension Calculator", "Calculates required crankshaft extension length and keyway depth for secure hub mounting.")
        ],
        "matrix_id, press_oem, press_model, nominal_tonnage, flywheel_rpm, recommended_ompi_sku, adaptor_plate_drawing_id",
        "Torque Sizing Calculator (Mod 16), Fast-Quote (Mod 04)"
    ),

    # Page 10: Modules 7 to 9
    (
        "ERP-MOD-07", "Customer Discount & Margin Matrix", "Engine 1: Commercial Sales Pipeline", "Managing Director, Financial Controllers",
        "Uncontrolled sales discounting erodes profitability on imported capital machinery. Transparent pricing structures are essential for distributor relationships.",
        "Enforces role-based discounting rules and minimum gross margin thresholds. Restricts sales engineer discounting to pre-authorized bands and requires MD approval for exceptional terms.",
        [
            ("Role-Based Discount Bands", "Sales Reps: max 3%; Sales Managers: max 7%; Managing Director authorization required for >7%."),
            ("Gross Margin Floor Sentinel", "Hard automated lock preventing quote submission if projected gross margin drops below 22%."),
            ("Distributor Tier Pricing", "Maintains distinct price schedules for authorized regional distributors versus direct end-user forge shops.")
        ],
        "rule_id, user_role, max_discount_percent, min_margin_floor_percent, md_override_required_bool, tier_level",
        "Fast-Quote Engine (Mod 04), Audit Log (Mod 31)"
    ),
    (
        "ERP-MOD-08", "Proforma Invoice (PI) Generator", "Engine 1: Commercial Sales Pipeline", "Accounts Officers, Commercial Managers",
        "Commercial purchase orders cannot be finalized without formal statutory proforma invoices detailing tax rates, milestone payment terms, and bank RTGS details.",
        "Generates statutory Proforma Invoices with HSN-classified line items, applicable GST calculations (CGST+SGST or IGST), and specific bank remittance instructions.",
        [
            ("Statutory HSN Mapping", "Applies 8-digit HSN codes (8483 for clutches, 6813 for friction discs) with correct GST percentages."),
            ("Milestone Payment Triggers", "Calculates advance payment amounts and specifies dispatch and installation payment milestones."),
            ("Remittance Banking Instructions", "Embeds verified corporate bank account details (IFSC, Account Number) and RTGS/NEFT routing instructions.")
        ],
        "pi_id, quote_ref_id, buyer_gstin, hsn_code, taxable_amount, cgst_amount, sgst_amount, igst_amount, total_pi_inr",
        "Sales Order Engine (Mod 09), Invoice Engine (Mod 26)"
    ),
    (
        "ERP-MOD-09", "Sales Order (SO) Conversion Engine", "Engine 1: Commercial Sales Pipeline", "Commercial Managers, Warehouse Supervisors",
        "Failing to formalize accepted quotations into confirmed sales orders leads to double-booking warehouse stock, misaligned delivery dates, and lost customer trust.",
        "Converts confirmed client purchase orders and advance payments into active ERP Sales Orders. Immediately locks inventory in the warehouse bin ledger and dispatches procurement triggers.",
        [
            ("Stock Allocation & Reservation", "Automatically transitions matching stock items from 'Available' to 'Allocated' in the Warehouse Bin Ledger."),
            ("PO Reconciliation Check", "Verifies buyer's formal Purchase Order amount and terms against the issued Proforma Invoice."),
            ("Production & Rigging Handshake", "Triggers work orders to the engineering workshop if adaptor machining or shaft boring is required.")
        ],
        "so_id, client_po_number, po_date, quote_ref, allocated_sku_list, advance_received_amount, planned_dispatch_date",
        "Stock Ledger (Mod 18), Delivery Challan (Mod 22)"
    ),

    # Page 11: Modules 10 to 12
    (
        "ERP-MOD-10", "WhatsApp & Email Quote Dispatcher", "Engine 1: Commercial Sales Pipeline", "Sales Coordinators, Applications Engineers",
        "Quotes sent exclusively via email frequently get lost in corporate spam filters or experience delayed review by mobile plant decision-makers.",
        "Automated communications engine that dispatches formal quotation PDFs, Proforma Invoices, and order confirmations via verified WhatsApp Business API and email simultaneously.",
        [
            ("Dual-Channel Delivery", "Simultaneous transmission of PDF proposals via encrypted WhatsApp Business channel and corporate email."),
            ("Delivery & Read Receipts", "Tracks WhatsApp message delivery status and document download events to notify the sales team in real time."),
            ("Interactive Follow-up Triggers", "Enables client to accept quote, request technical revisions, or schedule a phone conference with a single click.")
        ],
        "dispatch_id, document_type, recipient_phone, recipient_email, whatsapp_delivery_status, read_timestamp, pdf_url",
        "Fast-Quote (Mod 04), Proforma Invoice (Mod 08)"
    ),
    (
        "ERP-MOD-11", "Multi-Level Bill of Materials (BOM)", "Engine 2: Engineering BOM & Italy Imports", "Engineering Designers, Production Managers",
        "Assembling complete pneumatic clutch-brake retrofits without indented BOM hierarchies causes component shortages during on-site commissioning.",
        "Maintains multi-level engineering BOM structures for complete clutch assemblies, detailing sub-assemblies, friction blocks, return springs, air cylinders, rotary seals, and dual safety valves.",
        [
            ("Indented Hierarchy Management", "Multi-tier component trees linking top-level clutch assemblies to internal wear parts and hardware."),
            ("Standard Component Mapping", "Links commercial hardware (O-rings, circlips, fasteners) to local Indian standard procurement sources."),
            ("Revision Control Architecture", "Tracks engineering drawing changes and component revisions with formal engineering change orders (ECO).")
        ],
        "bom_id, parent_sku, sub_component_sku, quantity_per_assembly, unit_of_measure, drawing_ref, eco_revision_number",
        "Italy Import PO (Mod 12), Stock Ledger (Mod 18)"
    ),
    (
        "ERP-MOD-12", "Italy Import Purchase Order (PO)", "Engine 2: Engineering BOM & Italy Imports", "Procurement Directors, Import Managers",
        "Procuring machinery components from European OEMs requires precise part numbers, currency conversion schedules, and container freight consolidation.",
        "Generates formal international purchase orders formatted to OMPI Italy OEM specifications. Tracks itemized pricing in EUR, sea freight container consolidation schedules, and factory lead times.",
        [
            ("OEM Specification Format", "Exports standardized PO documentation matching OMPI Italy engineering part numbers and nomenclature."),
            ("Container Consolidation", "Groups multiple stock replenishment and project-specific orders into 20ft/40ft maritime shipping containers."),
            ("Milestone Payment Tracking", "Tracks export LC milestones or CAD (Cash Against Documents) payment terms with foreign supplier banks.")
        ],
        "po_id, supplier_id, order_date, total_amount_eur, incoterms_code, container_size, promised_ex_factory_date",
        "Landed Cost Engine (Mod 13), Shipment Ledger (Mod 14)"
    ),

    # Page 12: Modules 13 to 15
    (
        "ERP-MOD-13", "Landed Cost & Customs Duty Calculator", "Engine 2: Engineering BOM & Italy Imports", "Commercial Accountants, Import Managers",
        "Inaccurate estimation of customs duty, exchange fluctuations, and port demurrage leads to underpriced contracts and depleted operational cash flows.",
        "Calculates true landed cost per SKU upon arrival at Nhava Sheva (JNPT). Incorporates CIF value, Basic Customs Duty (BCD), Social Welfare Surcharge (SWS), IGST, port clearing, and inland freight.",
        [
            ("Statutory Duty Computation", "Applies current tariff formulas: BCD @ 7.5%, SWS @ 10% of BCD, and Integrated GST @ 18% on assessable value."),
            ("Port Handling Allocation", "Distributes container handling, CFS charges, and customs broker fees across individual SKUs by weight/value."),
            ("Unit Cost Recalculation", "Updates weighted-average inventory valuation in the financial ledger upon customs clearance.")
        ],
        "calculation_id, po_ref, boe_number, cif_inr, bcd_inr, sws_inr, igst_inr, port_charges_inr, final_unit_landed_cost",
        "Multi-Currency Pricing (Mod 03), Stock Ledger (Mod 18)"
    ),
    (
        "ERP-MOD-14", "Shipment & Bill of Lading (BL) Ledger", "Engine 2: Engineering BOM & Italy Imports", "Logistics Coordinators, Customs Clearance Agents",
        "Misplaced shipping documents and unmonitored maritime transit lead to heavy container detention charges and production downtime at customer plants.",
        "Tracks shipping containers from European ports (Genoa, La Spezia) through maritime transit to Nhava Sheva (JNPT). Manages Bill of Lading records, customs clearing milestones, and yard deliveries.",
        [
            ("Container Tracking Milestones", "Logs shipment stages: Departed Port -> Ocean Transit -> Arrived JNPT -> Customs Cleared -> In Yard."),
            ("Statutory Document Vault", "Stores digital copies of Bill of Lading, Commercial Invoice, Packing List, and Certificate of Origin."),
            ("Detention Warning System", "Calculates free days at port and triggers alerts 72 hours before container detention charges begin.")
        ],
        "shipment_id, bl_number, shipping_line, container_number, departure_port, eta_jnpt_date, customs_cleared_date",
        "Landed Cost Engine (Mod 13), Inward GRN (Mod 21)"
    ),
    (
        "ERP-MOD-15", "Technical Drawing & GA Repository", "Engine 2: Engineering BOM & Italy Imports", "Engineering Draughtsmen, Field Service Technicians",
        "Using unverified or superseded machinery drawings during on-site installation leads to mismatched mounting holes, incorrect air piping, and commissioning failure.",
        "Centralized document management repository housing certified CAD drawings, General Arrangement (GA) blueprints, dimensional schematics, and pneumatic piping layouts.",
        [
            ("Certified Blueprint Archive", "Stores high-resolution PDFs and DXF/DWG vector drawings for all OMPI standard assemblies and custom adaptors."),
            ("Strict Version Control", "Ensures field engineers access only the latest engineering revision with clear revision changelogs."),
            ("Field Mobile Access", "Enables on-site service engineers to view mechanical drawings and torque specifications on mobile devices.")
        ],
        "drawing_id, drawing_number, sku_ref, file_format, cad_revision, approved_by_engineer, upload_timestamp",
        "Fast-Quote Engine (Mod 04), Reconditioning Ledger (Mod 23)"
    ),

    # Page 13: Modules 16 to 18
    (
        "ERP-MOD-16", "Torque & Pressure Sizing Calculator", "Engine 2: Engineering BOM & Italy Imports", "Senior Applications Engineers, Technical Directors",
        "Under-sizing clutch torque causes excessive slipping, premature friction lining burn, and safety brake failure. Over-sizing damages press drive shafts.",
        "Mathematical engineering calculator sizing required clutch-brake torque based on flywheel moment of inertia (GD2), press strokes per minute (SPM), air pressure, and safety factors.",
        [
            ("Inertia & Torque Equations", "Calculates required dynamic torque using standard engineering formulas: T = (GD2 * n) / (375 * t)."),
            ("Operating Pressure Derating", "Calculates available braking torque across variable shop air pressures from 4.5 bar to 6.0 bar."),
            ("Emergency Stop Angle Compliance", "Verifies that the selected brake stops press slide within required safety angles (<15 degrees of rotation).")
        ],
        "calc_id, press_tonnage, flywheel_inertia_gd2, spm_speed, air_pressure_bar, calculated_torque_nm, selected_sku",
        "Catalog Master (Mod 02), Fast-Quote (Mod 04)"
    ),
    (
        "ERP-MOD-17", "Import Duty & HSN Tariff Master", "Engine 2: Engineering BOM & Italy Imports", "Commercial Accountants, Tax Compliance Officers",
        "Misclassifying imported industrial machinery components under incorrect HSN codes results in customs penalties, confiscation, and lost GST input tax credits.",
        "Centralized statutory repository of 8-digit HSN codes, customs tariff headings, Basic Customs Duty rates, Social Welfare Surcharge formulas, and GST classifications.",
        [
            ("8-Digit HSN Repository", "Maintains certified classifications: 8483 (clutches/shafts), 6813 (friction material), 8462 (machine tools)."),
            ("Statutory Rate History", "Maintains chronological history of notification changes by CBIC for duty rate audits."),
            ("FTA Exemption Mapping", "Identifies applicable concessional duty notifications and Free Trade Agreement rules of origin.")
        ],
        "hsn_code, tariff_heading_description, bcd_rate_percent, sws_rate_percent, igst_rate_percent, notification_ref",
        "Landed Cost Calculator (Mod 13), GST Tax Invoice (Mod 26)"
    ),
    (
        "ERP-MOD-18", "Real-Time Stock Ledger & Bin Management", "Engine 3: Spares Inventory & Warehouse Hub", "Warehouse Managers, Storekeepers, Inventory Auditors",
        "Inaccurate inventory records lead to missed dispatch deadlines, unrecorded stock shrinkage, and double-ordering of high-value imported assemblies.",
        "Perpetual inventory tracking engine managing multi-location stock across Pune Central Warehouse, Chakan Staging Yard, and transit consignments. Tracks exact rack, shelf, and bin locations.",
        [
            ("Multi-Yard Bin Architecture", "Specifies exact physical bin locations (e.g. Rack B, Shelf 3, Bin 12) for every SKU in inventory."),
            ("Perpetual Stock Ledger", "Real-time updates of On-Hand, Allocated, In-Transit, and Available inventory upon every transaction."),
            ("Stock Discrepancy Audits", "Supports physical stock reconciliation workflows with barcode verification and variance logging.")
        ],
        "bin_id, sku_code, warehouse_code, rack_shelf_bin, quantity_on_hand, quantity_allocated, quantity_available",
        "Sales Order Engine (Mod 09), GRN Engine (Mod 21)"
    ),

    # Page 14: Modules 19 to 21
    (
        "ERP-MOD-19", "Friction Disc & Wear Parts Tracker", "Engine 3: Spares Inventory & Warehouse Hub", "Tool Room Heads, Spares Inventory Managers",
        "Friction linings wear down during normal press operation. Lack of batch-level wear tracking leads to unexpected press slippage, tool breakage, and unplanned plant downtime.",
        "Tracks friction disc inventories, wear tolerances, friction coefficient ratings, and replacement intervals for press maintenance teams across client manufacturing sites.",
        [
            ("Batch Thickness Tracking", "Logs exact friction pad thickness (mm) and replacement wear-limit thresholds (minimum 3mm)."),
            ("Friction Coefficient Index", "Catalogs static and dynamic friction coefficients for dry-running and oil-immersed applications."),
            ("Automated Re-Lining Alerts", "Flags client installations approaching critical operational hours for proactive replacement scheduling.")
        ],
        "disc_batch_id, clutch_model_ref, pad_thickness_mm, min_safe_thickness_mm, friction_material_type, stock_pieces",
        "Stock Ledger (Mod 18), Reconditioning Ledger (Mod 23)"
    ),
    (
        "ERP-MOD-20", "Serial Number & Heat Code Traceability", "Engine 3: Spares Inventory & Warehouse Hub", "Quality Assurance Engineers, Warranty Officers",
        "Failure to track individual serial numbers prevents validation of warranty claims and makes root-cause metallurgical investigations impossible.",
        "Assigns and tracks unique laser-etched serial numbers and metallurgical heat codes for every imported OMPI clutch unit from Italian factory dispatch to client commissioning.",
        [
            ("Individual Serial Numbering", "Logs unique serial numbers etched on clutch drive hubs and brake housings for complete lifecycle tracking."),
            ("Metallurgical Heat Records", "Links shaft components to mill test certificates verifying chemical composition and tensile strength."),
            ("Warranty Lifecycle Tracking", "Records exact commissioning date and validates warranty status against operational failure reports.")
        ],
        "serial_number, sku_code, heat_treatment_code, mill_test_cert_id, invoice_ref, commissioning_date, warranty_expiry_date",
        "GRN Engine (Mod 21), Reconditioning Ledger (Mod 23)"
    ),
    (
        "ERP-MOD-21", "Inward Material Inspection (GRN Engine)", "Engine 3: Spares Inventory & Warehouse Hub", "Quality Control Inspectors, Receiving Supervisors",
        "Accepting damaged imports or components with machining runout into stock contaminates inventory and results in failed on-site machine installations.",
        "Standardized quality control protocol for incoming consignments from Italy and domestic fabricators. Verifies dimensions, runout, pressure integrity, and generates formal Goods Receipt Notes.",
        [
            ("Mandatory Inspection Checklist", "Digital QC workflow: visual finish, dimensional checks, thread pitch, and pneumatic leak test."),
            ("Crankshaft Runout Protocol", "Verifies radial runout tolerances (<0.05mm) using calibrated dial indicators before stock acceptance."),
            ("Defect Quarantine Protocol", "Automatically isolates non-conforming items to a quarantine bin and triggers rejection notices.")
        ],
        "grn_id, po_ref, shipment_ref, items_received_count, items_accepted_count, items_quarantined_count, qc_inspector_id",
        "Stock Ledger (Mod 18), Invoice Engine (Mod 26)"
    ),

    # Page 15: Modules 22 to 24
    (
        "ERP-MOD-22", "Outward Delivery Challan & Dispatch", "Engine 3: Spares Inventory & Warehouse Hub", "Logistics Officers, Dispatch Supervisors",
        "Transporting multi-ton industrial machinery components without statutory delivery challans and e-Way bills leads to vehicle impoundment and heavy GST penalties.",
        "Generates statutory Delivery Challans under GST Rule 55 for job work, client demonstration, or final supply. Pre-configures e-Way Bill documentation and packing lists.",
        [
            ("Rule 55 Delivery Challan", "Generates compliant challans with mandatory tax declarations, transporter details, and vehicle numbers."),
            ("e-Way Bill Data Pre-Flight", "Prepares Part A and Part B payload data formatted for automated portal upload before vehicle departure."),
            ("Packing List Generation", "Details individual crate dimensions, gross weight, net weight, and lifting center of gravity for safe rigging.")
        ],
        "challan_id, so_ref, transport_vehicle_number, eway_bill_number, gross_weight_kg, package_count, dispatch_timestamp",
        "Sales Order Engine (Mod 09), Invoice Engine (Mod 26)"
    ),
    (
        "ERP-MOD-23", "Reconditioning & Service Center Ledger", "Engine 3: Spares Inventory & Warehouse Hub", "Workshop Superintendents, Lead Service Technicians",
        "Unmonitored reconditioning of customer clutch units leads to component loss, untracked labor costs, and failure to perform required pressure hold tests.",
        "Manages internal workshop service jobs for clutch overhauls, flywheel re-machining, and brake relining. Tracks labor hours, replacement parts consumed, and test-bench sign-offs.",
        [
            ("Service Job Card Protocol", "Issues itemized job cards tracking disassembly, cleaning, replacement parts, and re-assembly."),
            ("100-Cycle Pressure Test", "Mandatory bench testing: checks pneumatic seal integrity at 6 bar pressure over 100 continuous test cycles."),
            ("Reconditioning Cost Summary", "Calculates total job cost: replacement parts consumed + skilled machining hours + testing overhead.")
        ],
        "job_card_id, client_id, incoming_clutch_serial, work_scope_code, parts_consumed_json, labor_hours, test_bench_pass_bool",
        "Stock Ledger (Mod 18), Invoice Engine (Mod 26)"
    ),
    (
        "ERP-MOD-24", "Scrap & Dead Stock Management", "Engine 3: Spares Inventory & Warehouse Hub", "Warehouse Managers, Finance Directors",
        "Holding unserviceable worn friction pads and damaged castings distorts warehouse valuation and blocks valuable storage space.",
        "Formal workflow for surveying, classifying, writing off, and disposing of unserviceable metal scrap and obsolete wear items. Enforces GST input credit reversal accounting.",
        [
            ("Scrap Classification Protocol", "Categorizes scrap into ferrous iron, copper alloy, and hazardous composite friction material."),
            ("Statutory GST Reversal", "Automatically calculates required GST input credit reversal on written-off inventory per Section 17(5)(h)."),
            ("Weight Bridge Disposal Log", "Records weighbridge slips, disposal vendor invoices, and authorization sign-offs from executive management.")
        ],
        "scrap_id, sku_code, write_off_quantity, book_value_inr, scrap_realized_inr, gst_reversal_amount, approval_signoff_id",
        "Stock Ledger (Mod 18), Financial Ledger (Mod 28)"
    ),

    # Page 16: Modules 25 to 27
    (
        "ERP-MOD-25", "Automated Re-Order Alerts & Lead Time Engine", "Engine 3: Spares Inventory & Warehouse Hub", "Procurement Managers, Storekeepers",
        "Because European manufacturing and sea transit require 8 to 12 weeks, stockouts of critical friction linings cause prolonged client factory shutdowns.",
        "Calculates minimum re-order thresholds based on historical consumption velocity, seasonal demand, and vendor lead times. Automatically generates replenishment PO drafts.",
        [
            ("Dynamic Re-Order Formula", "Reorder Level = (Average Daily Usage * Maximum Lead Time Days) + Safety Buffer Stock."),
            ("Lead Time Tracking", "Maintains empirical vendor lead times for Italian shipments (8 weeks) and local machining (2 weeks)."),
            ("Automated PO Draft Generation", "Generates consolidated replenishment purchase order drafts when stock drops below safety thresholds.")
        ],
        "sku_code, avg_monthly_consumption, lead_time_days, safety_stock_units, calculated_reorder_point, po_draft_triggered_bool",
        "Stock Ledger (Mod 18), Italy Import PO (Mod 12)"
    ),
    (
        "ERP-MOD-26", "GST Tax Invoice Engine", "Engine 4: Financial Ledger & Governance", "Accounts Managers, Financial Controllers",
        "Errors in tax rates, customer GSTINs, or invoice formatting result in GST compliance notices, customer payment delays, and blocked input tax credits.",
        "Generates statutory B2B Tax Invoices fully compliant with Indian GST laws. Enforces correct CGST+SGST or IGST classification, 8-digit HSN codes, and milestone payment terms.",
        [
            ("Automated Tax Determination", "Applies CGST (9%) + SGST (9%) for intra-state Maharashtra, or IGST (18%) for inter-state transactions."),
            ("IRN & QR Code Readiness", "Formatted to integrate seamlessly with the government e-Invoicing portal for automated IRN generation."),
            ("Sales Order Line Mapping", "Pulls line items directly from confirmed Sales Orders to eliminate manual transcription discrepancies.")
        ],
        "invoice_id, so_ref_id, invoice_date, buyer_gstin, place_of_supply, taxable_value, cgst, sgst, igst, total_invoice_inr",
        "GSTR-1 Exporter (Mod 27), Accounts Receivable (Mod 28)"
    ),
    (
        "ERP-MOD-27", "GSTR-1 Reconciliation Exporter", "Engine 4: Financial Ledger & Governance", "Tax Accountants, Statutory Auditors",
        "Manual reconciliation of monthly outward supplies against the GST portal is slow and error-prone, creating mismatches between financial ledgers and GSTR-3B filings.",
        "Compiles all outward supply invoices, credit notes, and advance adjustments into verified JSON and Excel upload files formatted for direct GSTR-1 portal filing.",
        [
            ("One-Click GSTR-1 File Generation", "Exports monthly sales register directly into standard GSTN JSON format for immediate portal upload."),
            ("HSN Summary Table 12", "Aggregates total taxable values and tax splits per 8-digit HSN code to satisfy statutory Table 12 reporting."),
            ("Reconciliation Error Pre-Check", "Pre-validates GSTIN formats, tax rate percentages, and state codes to prevent portal rejection.")
        ],
        "filing_month, total_b2b_invoices, gross_taxable_value, total_cgst_filed, total_sgst_filed, total_igst_filed, portal_status",
        "GST Tax Invoice (Mod 26), Audit Log (Mod 31)"
    ),

    # Page 17: Modules 28 to 30
    (
        "ERP-MOD-28", "Accounts Receivable & Milestone Tracking", "Engine 4: Financial Ledger & Governance", "Credit Controllers, Finance Directors",
        "Machinery projects run on milestone billing (Advance, Dispatch, Commissioning). Failure to link payment stages results in uncollected retention balances.",
        "Monitors outstanding customer balances against physical machinery delivery and commissioning milestones. Tracks bank RTGS payments, withholding tax (TDS), and aging balances.",
        [
            ("Milestone Completion Sentinel", "Blocks dispatch challan creation if the contractually required 50% dispatch payment is unverified."),
            ("TDS & Advance Reconciliation", "Reconciles customer TDS deductions under Section 194Q and matches advance receipts with bank entries."),
            ("Real-Time Client Ledger", "Provides real-time statement of account displaying invoices, receipts, credit notes, and outstanding balances.")
        ],
        "ar_ledger_id, client_id, invoice_ref, milestone_stage_name, invoice_amount, amount_collected, balance_outstanding, tds_inr",
        "Invoice Engine (Mod 26), Payment Reminders (Mod 29)"
    ),
    (
        "ERP-MOD-29", "Overdue Aging & Payment Reminder Hub", "Engine 4: Financial Ledger & Governance", "Credit Controllers, Sales Coordinators",
        "Passive debt collection causes working capital shortages. Delayed follow-ups increase the probability of bad debts in machinery retrofits.",
        "Aging analysis engine classifying outstanding receivables into 0-30, 31-60, 61-90, and 90+ days. Automatically dispatches polite, progressive WhatsApp and email reminders.",
        [
            ("Aging Schedule Classification", "Categorizes outstanding balances into standard aging buckets with automated risk scoring."),
            ("Progressive Reminder Templates", "Automated escalation: Friendly reminder at 7 days -> Formal notice at 30 days -> Management alert at 60 days."),
            ("Sales Team Warning Flag", "Flags overdue client accounts across the commercial pipeline to prevent taking new orders from defaulters.")
        ],
        "aging_bucket_code, client_id, total_overdue_inr, oldest_invoice_days, reminders_sent_count, last_reminder_timestamp",
        "Accounts Receivable (Mod 28), Audit Log (Mod 31)"
    ),
    (
        "ERP-MOD-30", "Role-Based Access Control (RBAC)", "Engine 4: Financial Ledger & Governance", "System Administrators, Managing Director",
        "Granting unrestricted system access creates internal fraud risks, unauthorized quotation discounting, and accidental deletion of financial records.",
        "Enforces strict least-privilege role-based access security across Sales, Engineering, Warehouse, Accounts, and Executive tiers. Manages user sessions and permission sets.",
        [
            ("Granular Privilege Matrix", "Defines read, create, edit, and approve permissions for each functional module across user roles."),
            ("Executive Approval Safeguards", "Restricts sensitive actions (e.g. invoice cancellation, margin overrides) exclusively to Managing Director."),
            ("Two-Factor Authentication", "Secures user authentication with multi-factor verification for remote or mobile administrative access.")
        ],
        "user_id, login_username, role_title, permission_bitmask, active_session_token, mfa_enabled_bool, last_login_ip",
        "Immutable Audit Log (Mod 31), LAN Backup (Mod 32)"
    ),

    # Page 18: Modules 31 to 33
    (
        "ERP-MOD-31", "Immutable Security Audit Log", "Engine 4: Financial Ledger & Governance", "Internal Auditors, Managing Director",
        "Without immutable audit trails, internal fraud, back-dated quotations, unauthorized price edits, and deleted records cannot be detected or proven.",
        "Append-only, tamper-proof logging engine capturing every critical ERP action: logins, quotation edits, discount approvals, invoice generation, and master edits with timestamps and IP addresses.",
        [
            ("Tamper-Proof Audit Records", "Appends SHA-256 cryptographic hashes to transaction log entries to guarantee tamper-evident integrity."),
            ("Critical Operation Monitoring", "Logs specific before/after values for modified selling prices, approved credit limits, and stock write-offs."),
            ("Forensic Security Exporter", "Generates immutable compliance audit reports for statutory auditors and management reviews.")
        ],
        "log_id, timestamp_utc, user_id, action_code, target_entity, before_state_hash, after_state_hash, client_ip_address",
        "RBAC Engine (Mod 30), Executive MIS (Mod 33)"
    ),
    (
        "ERP-MOD-32", "On-Premise LAN Backup & Snapshot", "Engine 4: Financial Ledger & Governance", "IT Systems Engineers, Operations Managers",
        "Relying solely on external cloud systems without local snapshots leaves the warehouse and workshop vulnerable to internet downtime and catastrophic data loss.",
        "Automated backup utility executing periodic encrypted snapshots of the local ERP database to on-premise Network Attached Storage (NAS) and encrypted secondary cloud archives.",
        [
            ("Automated Nightly Snapshots", "Executes automated zero-downtime database snapshots every 24 hours with strict checksum validation."),
            ("Redundant Local Archival", "Maintains dual backups on the primary server and an isolated local Network Attached Storage (NAS) drive."),
            ("Disaster Recovery Protocol", "Standard operating recovery scripts enabling complete database restoration in under 15 minutes.")
        ],
        "snapshot_id, backup_timestamp, database_size_mb, storage_path, md5_checksum, offsite_sync_status, restore_tested_date",
        "Security Audit Log (Mod 31), Executive MIS (Mod 33)"
    ),
    (
        "ERP-MOD-33", "Executive MIS & Analytics Dashboard", "Engine 4: Financial Ledger & Governance", "Managing Director, Board of Directors",
        "Executive leadership requires real-time business intelligence covering revenue, inventory holding costs, gross margins, and pipeline velocity without compiling spreadsheets.",
        "Executive reporting console visualizing key commercial metrics: monthly turnover, landed margin realization, stock turnover ratio, overdue debt risk, and top client concentrations.",
        [
            ("Revenue & Margin Realization", "Visualizes monthly invoiced revenue compared against realized gross margins across all machine and clutch lines."),
            ("Inventory Holding Velocity", "Calculates inventory turnover ratios, isolating slow-moving machinery assets and fast-moving clutch spares."),
            ("Cash Flow Forecasting", "Projects 30-day and 60-day cash inflows based on confirmed milestone payment dates and active sales pipeline.")
        ],
        "report_period, monthly_revenue_inr, realized_gross_margin_percent, stock_turnover_ratio, total_receivables_inr, active_pipeline_inr",
        "Sales Order Engine (Mod 09), Accounts Receivable (Mod 28)"
    )
]

print(f"Data initialized: {len(routes)} routes, {len(modules)} modules.")

