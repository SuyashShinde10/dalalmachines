# scratch/build_all_32_pages.py
import os, subprocess, shutil

print("Building complete 32-page plain language executive guide...")

# 24 Dalal Routes Data
dalal_routes = [
    # Page 2
    {
        "id": "ROUTE-01",
        "title": "Homepage & Industrial Asset Portal",
        "path": "/index.html",
        "audience": "Industrial Plant Owners, Factory Directors, Forging Heads",
        "sees": "A professional machinery showroom showing heavy presses currently standing in the Pune stockyard. Buyers can see clear machine photos, tonnage ratings, inspection videos, and a direct WhatsApp button to chat with Mr. Vinit Dalal.",
        "benefit": "Eliminates buyer skepticism. Factory owners see real physical stock in Pune (not fake broker ads), establishing immediate trust for high-value deals from Rs. 50 Lakh to Rs. 4 Crore.",
        "feature": "1-Click WhatsApp RFQ button pre-filled with the exact machine model and capacity."
    },
    {
        "id": "ROUTE-02",
        "title": "Corporate Profile & Heritage Dossier",
        "path": "/about.html",
        "audience": "Corporate Procurement Heads, Bank Valuers, Joint-Venture Partners",
        "sees": "The 50-year engineering heritage of the Dalal family, photos of the Mumbai registered office and Pune warehouse yard, and details of the official technical partnership with OMPI Italy.",
        "benefit": "Proves corporate legitimacy and long-term financial stability, assuring plant owners that their advance payments and multi-crore machinery orders are in trustworthy hands.",
        "feature": "Visual timeline highlighting 5 decades of heavy machinery installations across India."
    },
    # Page 3
    {
        "id": "ROUTE-03",
        "title": "Import, Rigging & Retrofit Engineering",
        "path": "/services.html",
        "audience": "Plant Maintenance Heads, Factory Engineers, Project Directors",
        "sees": "A simple guide to heavy press services: overseas dismantling, port customs clearance, multi-axle trailer transport, foundation pit construction, and Italian pneumatic clutch retrofits.",
        "benefit": "Shows buyers that Dalal provides end-to-end support—not just selling the machine, but installing it on their factory floor, testing it under load, and guaranteeing spare parts.",
        "feature": "7-point plain English FAQ explaining how High Seas Sales save time and customs duty."
    },
    {
        "id": "ROUTE-04",
        "title": "Machinery Catalog & Parametric Search",
        "path": "/category.html",
        "audience": "Factory Sourcing Managers, Purchase Officers",
        "sees": "A clean, searchable directory of all 26 machine types (Forging Presses, Mechanical Presses, Hydraulic Presses, Horizontal Boring Machines) with instant tonnage filters.",
        "benefit": "Allows purchasing teams to find the exact tonnage and machine type they need in seconds without having to scroll through hundreds of irrelevant listings.",
        "feature": "Instant tonnage filter buttons (Under 500 Tons, 500T to 1,000 Tons, 1,000T to 4,000 Tons)."
    },
    # Page 4
    {
        "id": "ROUTE-05",
        "title": "Machine Engineering Dossier (PDP)",
        "path": "/product.html",
        "audience": "Chief Technical Officers, Toolroom Managers, Plant Heads",
        "sees": "An in-depth technical sheet for each press: exact tonnage, ram stroke, bed dimensions, motor horsepower, country of make, live power inspection video, and ready-to-download quotation.",
        "benefit": "Gives plant technical heads every measurement and spec needed to confirm the press will fit their factory space, foundation pit, and forging dies.",
        "feature": "1-Click Download of an official, print-ready PDF machine quotation with full specs."
    },
    {
        "id": "ROUTE-06",
        "title": "Brand New Machinery & Turnkey Lines",
        "path": "/brand-new-machinery.html",
        "audience": "Tier-1 Automotive Suppliers, High-Volume Manufacturing Plants",
        "sees": "Brand-new industrial machinery lines supplied with manufacturer warranty, complete European safety standards, and factory commissioning support.",
        "benefit": "Captures top-tier automotive companies that have strict internal corporate policies requiring brand-new equipment with factory guarantees rather than used machinery.",
        "feature": "Inquiry form specifically for custom-engineered new production lines."
    },
    # Page 5
    {
        "id": "ROUTE-07",
        "title": "Shipment, Yard & Rigging Photo Archive",
        "path": "/gallery.html",
        "audience": "Factory Auditors, Sourcing Committees, Managing Directors",
        "sees": "A photographic gallery showing heavy 1,000-ton to 4,000-ton presses being lifted by giant hydraulic cranes, transported on 64-wheel trailers, and parked in the Pune stockyard.",
        "benefit": "Irrefutable proof of capability. Seeing real photos of heavy equipment handling eliminates any doubt about Dalal's ability to safely deliver massive machines.",
        "feature": "Filterable photo albums categorized by press tonnage and transport stages."
    },
    {
        "id": "ROUTE-08",
        "title": "Headquarters, Yard & Direct RFQ Portal",
        "path": "/contact.html",
        "audience": "Procurement Directors, Visiting Engineering Teams",
        "sees": "Interactive Google Map locations for both the Mumbai Registered Office (Tardeo) and the Pune Stockyard (Chakan), with direct phone numbers and a visit booking form.",
        "benefit": "Makes it effortless for serious corporate buyers to schedule an in-person physical inspection and see the machines run under live electric power before paying.",
        "feature": "Direct appointment booking console to schedule a live power trial in Pune."
    },
    # Page 6
    {
        "id": "ROUTE-09",
        "title": "Express Plant Breakdown RFQ Console",
        "path": "/contact-2.html",
        "audience": "Plant Managers facing an urgent machine breakdown",
        "sees": "A fast, streamlined emergency request form asking only for required press tonnage, bed size, and delivery urgency, designed to be filled out in 30 seconds.",
        "benefit": "Captures high-priority hot leads whose production line has stopped and who have an urgent budget approved to buy a replacement press immediately.",
        "feature": "Instant high-priority notification sent directly to the Managing Director's WhatsApp."
    },
    {
        "id": "ROUTE-10",
        "title": "Import Compliance & Legal FAQs Guide",
        "path": "/faqs.html",
        "audience": "Chief Financial Officers (CFOs), Company Legal & Tax Advisors",
        "sees": "Clear, plain-English legal explanations of High Seas Sales, 100% GST input tax credit (ITC) claims, Customs Bill of Entry procedures, and live power inspection trials.",
        "benefit": "Removes legal and taxation fears from company accountants, providing clear documentation that speeds up corporate board approvals.",
        "feature": "7 interactive question accordions addressing customs duty and GST compliance."
    },
    # Page 7
    {
        "id": "ROUTE-11",
        "title": "Client Endorsements & Factory Proof",
        "path": "/testimonial.html",
        "audience": "Managing Directors, Capital Investment Committees",
        "sees": "Verified customer reviews, factory photos, and installation case studies from leading automotive forging and stamping plants across Pune, Rajkot, Chennai, and Delhi NCR.",
        "benefit": "Strong social proof showing that India's top automotive component manufacturers trust Dalal Machine Tools for their critical press lines.",
        "feature": "Customer testimonials displaying verified plant locations and installed machine tonnages."
    },
    {
        "id": "ROUTE-12",
        "title": "High Seas CIF Tariffs & Cost Breakdown",
        "path": "/pricing.html",
        "audience": "Finance Directors, Plant Owners, Purchasing Heads",
        "sees": "A transparent financial comparison showing how buying directly from port on High Seas saves 8% to 15% compared to purchasing machines delivered to local dealer yards.",
        "benefit": "Clearly explains pricing logic and demonstrates how buyers avoid double taxation, port demurrage, and middlemen markups.",
        "feature": "Interactive cost savings calculator showing estimated cash savings based on machine value."
    },
    # Page 8
    {
        "id": "ROUTE-13",
        "title": "Industrial Journal & Forging Hub",
        "path": "/blog.html",
        "audience": "Plant Maintenance Engineers, Toolroom Supervisors",
        "sees": "Practical engineering articles on press maintenance, how to prevent crankshaft fractures, press leveling methods, and pneumatic clutch upgrade benefits.",
        "benefit": "Positions Dalal and OMPI as technical experts rather than just traders, attracting organic visits from factory engineers across India.",
        "feature": "Searchable technical article library organized by maintenance topic."
    },
    {
        "id": "ROUTE-14",
        "title": "Lead Engineering Article: Clutch Upgrade",
        "path": "/blog-single.html",
        "audience": "Maintenance Managers, Factory Modernization Teams",
        "sees": "An easy-to-understand visual guide explaining why old mechanical dog clutches cause costly downtime and how converting to OMPI pneumatic clutches increases safety and speed.",
        "benefit": "Directly generates inquiries for OMPI clutch retrofit projects by showing factory heads how an upgrade pays for itself within 6 months.",
        "feature": "Step-by-step conversion timeline and before-and-after production rate comparison."
    },
    # Page 9
    {
        "id": "ROUTE-15",
        "title": "2500T Turnkey Overhaul Case Study",
        "path": "/blog-large-image.html",
        "audience": "Plant Directors, Heavy Forging Plant Heads",
        "sees": "A complete photo-story of a massive 2,500-ton Russian forging press being dismantled in Europe, shipped to India, overhauled in Pune, and commissioned in a live plant.",
        "benefit": "Shows prospective buyers that Dalal has the technical capability to handle massive multi-crore plant overhauls smoothly without risk.",
        "feature": "Chronological project timeline showing precision bed machining and foundation pit checks."
    },
    {
        "id": "ROUTE-16",
        "title": "Project Portfolio & Installation Archive",
        "path": "/projects.html",
        "audience": "EPC Contractors, Factory Expansion Teams",
        "sees": "A comprehensive showcase of past plant installations, on-site boring jobs, and heavy transport projects completed for forging plants across India.",
        "benefit": "Provides irrefutable proof of execution across diverse industries (Automotive, Defense, Railway, Heavy Engineering).",
        "feature": "Searchable project grid with filters for press tonnage and client industry."
    },
    # Page 10
    {
        "id": "ROUTE-17",
        "title": "120-Ton Heavy Press Transport Detail",
        "path": "/projects-single.html",
        "audience": "Factory Logistics Heads, Plant Engineers",
        "sees": "A detailed technical report showing how a giant 120-ton press frame was unloaded, brought inside a tight factory shed, and lowered into its foundation pit.",
        "benefit": "Assures factory owners that even the heaviest machines will be transported and positioned safely without damaging factory floors or roofs.",
        "feature": "Illustrated engineering breakdown of hydraulic strand-jacking and low-bed trailer delivery."
    },
    {
        "id": "ROUTE-18",
        "title": "Sector-Wise Plant Modernization",
        "path": "/projects-modern.html",
        "audience": "Automotive Tier-1 Plant Managers",
        "sees": "Specialized press automation services, automated coil feeding lines, and die-cushion upgrades tailored specifically for automotive parts manufacturing.",
        "benefit": "Attracts high-value plant modernization projects from automotive component manufacturers looking to boost daily output.",
        "feature": "Checklist of press automation upgrades with expected cycle time improvements."
    },
    # Page 11
    {
        "id": "ROUTE-19",
        "title": "Filterable Project Case Study Library",
        "path": "/projects-with-filter.html",
        "audience": "Capital Sourcing Committees, Plant Valuers",
        "sees": "A searchable project library where buyers can view only past installations matching their required tonnage (Under 500T, 500T to 1500T, or 1500T+).",
        "benefit": "Allows a factory owner looking for a specific press size to see exact proof of similar machines Dalal has successfully installed.",
        "feature": "1-click tonnage filter that instantly updates the displayed project case studies."
    },
    {
        "id": "ROUTE-20",
        "title": "Tooling, Bolster Plates & Spares Shop",
        "path": "/shop.html",
        "audience": "Spare Parts Purchasing Officers, Toolroom Heads",
        "sees": "A catalog of high-wear press spare parts: bolster plates, tie-rod nuts, pneumatic valves, hydraulic cylinders, and clutch friction pads.",
        "benefit": "Creates recurring monthly spare parts revenue from existing factories even after their initial machine purchase.",
        "feature": "Stock status tags showing which critical spare parts are ready for immediate dispatch from Pune."
    },
    # Page 12
    {
        "id": "ROUTE-21",
        "title": "Spare Part Technical Specification Page",
        "path": "/shop-single.html",
        "audience": "Toolroom Engineers, Maintenance Supervisors",
        "sees": "Detailed specifications for spare parts including steel grade (EN8, EN19, 42CrMo4), surface hardening, exact dimensions, and drawing inquiry options.",
        "benefit": "Guarantees that spare components will fit the customer's exact press model without needing costly on-site modifications.",
        "feature": "Direct button to request technical drawing verification before ordering."
    },
    {
        "id": "ROUTE-22",
        "title": "Multi-Item RFQ Package Cart",
        "path": "/shoping-cart.html",
        "audience": "Plant Sourcing Managers, Purchase Officers",
        "sees": "A simple list where buyers can bundle multiple machines, spare parts, and clutch conversion kits into one single quotation request.",
        "benefit": "Increases deal size by making it easy for factories to purchase a complete package (Press + OMPI Clutch + Spare Parts) in one go.",
        "feature": "Consolidated package summary with a 1-click WhatsApp quote button for the whole order."
    },
    # Page 13
    {
        "id": "ROUTE-23",
        "title": "Formal Procurement Proposal Submission",
        "path": "/checkout.html",
        "audience": "Corporate Purchasing Executives, Finance Teams",
        "sees": "A professional procurement form where buyers enter their company name, 15-digit GSTIN, factory delivery address, and expected delivery timeline.",
        "benefit": "Delivers pre-qualified, serious corporate inquiries with complete billing and delivery details directly to the sales team.",
        "feature": "Automated GST number verification ensuring official corporate inquiries."
    },
    {
        "id": "ROUTE-24",
        "title": "Smart Error Recovery & Alternative Stock",
        "path": "/404.html",
        "audience": "Any visitor who clicks an outdated or mistyped link",
        "sees": "Instead of a broken blank page, a helpful screen that suggests active presses currently in stock with a search bar and direct WhatsApp assistance.",
        "benefit": "Prevents potential customers from leaving the site and converts broken link visits into real machinery inquiries.",
        "feature": "Automatic display of top 3 currently available presses in the Pune stockyard."
    }
]

# 33 OMPI ERP Modules Data
ompi_modules = [
    # Engine 1: Sales & Commercial (Modules 1-10)
    {
        "id": "ERP-MOD-01",
        "title": "Client Records & GST Credit Master",
        "engine": "Engine 1: Sales & Customer Pipeline",
        "role": "Sales Executives, Accounts Manager",
        "does": "Maintains a central profile for every client factory: verified 15-digit GSTIN, multiple delivery godown addresses, authorized contact persons, and approved credit limits.",
        "benefit": "Stops costly billing errors, prevents dispatching goods to companies with overdue payments, and ensures tax invoices match GST portal records.",
        "feature": "Automated GST number validation and company ledger outstanding summary.",
        "is_live": True
    },
    {
        "id": "ERP-MOD-02",
        "title": "OMPI Technical Catalog & SKU Master",
        "engine": "Engine 1: Sales & Customer Pipeline",
        "role": "Technical Sales Engineers",
        "does": "Organizes all Italian pneumatic clutch-brakes, rotating unions, and friction discs by bore size, torque capacity, and dimensional cross-references.",
        "benefit": "Allows sales representatives to find the exact replacement clutch model in 10 seconds without needing to search through paper product catalogs.",
        "feature": "Quick lookup connecting press brand names with suitable OMPI clutch models.",
        "is_live": True
    },
    {
        "id": "ERP-MOD-03",
        "title": "Import Currency & Landed Pricing Engine",
        "engine": "Engine 1: Sales & Customer Pipeline",
        "role": "Commercial Manager, Managing Director",
        "does": "Calculates selling prices in Indian Rupees based on current Euro exchange rates, ocean shipping costs, customs duty, and minimum profit margins.",
        "benefit": "Protects company profits against sudden currency fluctuations between the Euro and the Rupee during the 4 to 8 weeks of ocean shipping.",
        "feature": "Automated price calculation incorporating daily exchange rates and port handling fees.",
        "is_live": True
    },
    {
        "id": "ERP-MOD-04",
        "title": "Fast-Quote 60-Second PDF Generator",
        "engine": "Engine 1: Sales & Customer Pipeline",
        "role": "Sales Representatives",
        "does": "Compiles professional, branded quotation letters complete with machine photos, dimensions, prices, and payment terms in under 60 seconds.",
        "benefit": "Allows your team to send an official proposal while the customer is still on the phone, beating competitors who take 2 to 3 days to send a quote.",
        "feature": "1-click generation of print-ready A4 PDF proposals with official company signature.",
        "is_live": True
    },
    {
        "id": "ERP-MOD-05",
        "title": "Customer Inquiry Visual Pipeline",
        "engine": "Engine 1: Sales & Customer Pipeline",
        "role": "Sales Team, Managing Director",
        "does": "Displays all incoming customer inquiries on a visual stage board: New Lead -> Sized -> Quoted -> PO Awaited -> Deal Won -> Delivered.",
        "benefit": "Gives the Managing Director complete visibility over every active deal so no high-value customer inquiry is ever forgotten or neglected.",
        "feature": "Visual stage cards with color-coded alerts for inquiries needing fast follow-up.",
        "is_live": True
    },
    {
        "id": "ERP-MOD-06",
        "title": "Press & Clutch Compatibility Matrix",
        "engine": "Engine 1: Sales & Customer Pipeline",
        "role": "Technical Sourcing Engineers",
        "does": "Cross-indexes leading press makes (Aida, Schuler, Godrej, Voronezh, Li Chin) with the exact OMPI clutch-brake combination required for bolt-on installation.",
        "benefit": "Enables sales reps to confidently advise plant owners on the exact clutch required without waiting for on-site engineer measurements.",
        "feature": "AI Technical Matchmaker providing 98% accurate clutch recommendations for known press models.",
        "is_live": True
    },
    {
        "id": "ERP-MOD-07",
        "title": "Profit Margin & Discount Protection",
        "engine": "Engine 1: Sales & Customer Pipeline",
        "role": "Managing Director, Finance Head",
        "does": "Enforces a strict minimum profit floor (e.g. 22%) and automatically blocks sales representatives from offering discounts without Managing Director sign-off.",
        "benefit": "Guarantees healthy commercial profitability and prevents junior sales reps from giving away company margins to close easy deals.",
        "feature": "Password-protected discount override approval requiring Director authorization.",
        "is_live": False
    },
    {
        "id": "ERP-MOD-08",
        "title": "Proforma Invoice (PI) Generator",
        "engine": "Engine 1: Sales & Customer Pipeline",
        "role": "Accounts Executive",
        "does": "Issues formal proforma invoices with clearly stated milestone payment terms: 30% Advance, 50% Against Dispatch, and 20% Post-Installation.",
        "benefit": "Ensures clean payment terms before any machinery leaves the yard, safeguarding company cash flow and preventing uncollected retention dues.",
        "feature": "Pre-formatted payment milestone schedule with company RTGS/NEFT banking details.",
        "is_live": False
    },
    {
        "id": "ERP-MOD-09",
        "title": "Sales Order & Warehouse Stock Hold",
        "engine": "Engine 1: Sales & Customer Pipeline",
        "role": "Sales Operations, Godown Keeper",
        "does": "Converts approved quotes into active ERP sales orders and automatically locks the selected machine or clutch unit in the godown ledger.",
        "benefit": "Eliminates embarrassing double-selling mistakes where two different sales reps try to sell the same warehouse unit to two different clients.",
        "feature": "Automated status switch changing machine from 'Available' to 'Under Commercial Hold'.",
        "is_live": False
    },
    {
        "id": "ERP-MOD-10",
        "title": "WhatsApp & Email Quote Dispatcher",
        "engine": "Engine 1: Sales & Customer Pipeline",
        "role": "Sales Operations",
        "does": "Sends official quotation PDFs and inspection photos directly to the client's WhatsApp and email with a personalized, professional cover message.",
        "benefit": "Achieves 90% higher open and response rates than traditional email, allowing immediate conversation with busy factory decision-makers.",
        "feature": "Direct WhatsApp notification dispatch with pre-filled machine reference numbers.",
        "is_live": True
    },
    # Engine 2: Italy Purchase & Landed Costing (Modules 11-17)
    {
        "id": "ERP-MOD-11",
        "title": "Assembly Parts Breakdown (BOM)",
        "engine": "Engine 2: Purchase & Landed Cost",
        "role": "Assembly Workshop Supervisor",
        "does": "Maintains an exact parts list for each clutch assembly down to every friction pad, seal kit, return spring, and dual pneumatic safety valve.",
        "benefit": "Ensures the workshop never gets stuck mid-assembly due to a missing 500-rupee seal kit on a 15-lakh clutch order.",
        "feature": "Exploded assembly parts tree showing part numbers and godown shelf locations.",
        "is_live": False
    },
    {
        "id": "ERP-MOD-12",
        "title": "Italy Import Purchase Order (PO)",
        "engine": "Engine 2: Purchase & Landed Cost",
        "role": "Import Procurement Manager",
        "does": "Generates formal international purchase orders in Euros formatted to OMPI Italy OEM specifications, tracking sea container schedules.",
        "benefit": "Eliminates ordering mistakes, provides proper dockets for bank foreign remittances, and tracks production lead times in Modena, Italy.",
        "feature": "Euro purchase order generator with OEM drawing codes and expected ocean shipment dates.",
        "is_live": False
    },
    {
        "id": "ERP-MOD-13",
        "title": "Total Landed Cost & Customs Calculator",
        "engine": "Engine 2: Purchase & Landed Cost",
        "role": "Commercial Manager, Accountant",
        "does": "Calculates the true total cost of imported units including Basic Customs Duty (7.5%), Social Welfare Surcharge, IGST (18%), and port clearing charges.",
        "benefit": "Shows the exact landed cost per unit in Rupees so management knows the true profit margin before quoting clients.",
        "feature": "Automated import duty calculator compliant with current Indian Customs tariff rules.",
        "is_live": True
    },
    {
        "id": "ERP-MOD-14",
        "title": "Sea Container & Shipping Tracker",
        "engine": "Engine 2: Purchase & Landed Cost",
        "role": "Logistics Coordinator",
        "does": "Tracks ocean containers from Italy ports (Genoa, La Spezia) through JNPT Nhava Sheva, logging Bill of Lading numbers and port arrival dates.",
        "benefit": "Prevents expensive port container demurrage and detention charges by preparing customs papers before the ship berths.",
        "feature": "Container milestone timeline with 14-day free-time tracking alerts.",
        "is_live": False
    },
    {
        "id": "ERP-MOD-15",
        "title": "Technical CAD & GA Drawing Archive",
        "engine": "Engine 2: Purchase & Landed Cost",
        "role": "Design Engineers, Service Team",
        "does": "A secure central archive of certified CAD blueprints and general arrangement (GA) drawings for factory foundation and clutch retrofit fitting.",
        "benefit": "Allows client engineering teams to prepare foundation bolts and air supply lines weeks before the machinery physically arrives.",
        "feature": "Downloadable certified drawings organized by press model and clutch series.",
        "is_live": False
    },
    {
        "id": "ERP-MOD-16",
        "title": "Clutch Sizing & Torque Calculator",
        "engine": "Engine 2: Purchase & Landed Cost",
        "role": "Application Engineers",
        "does": "Calculates the required clutch torque based on press flywheel speed, motor horsepower, and available factory compressed air pressure (5.5 to 6.0 bar).",
        "benefit": "Guarantees that the installed clutch will never slip, overheat, or fail during continuous heavy forging operations.",
        "feature": "Engineered sizing calculation matching press flywheel inertia to the correct OMPI model.",
        "is_live": False
    },
    {
        "id": "ERP-MOD-17",
        "title": "HSN Tax Code & Customs Tariff Master",
        "engine": "Engine 2: Purchase & Landed Cost",
        "role": "Company Accountant, Tax Advisor",
        "does": "Central master of all 8-digit government tax codes (HSN 8483, 8462, 6813) with current GST rates and customs duty classifications.",
        "benefit": "Prevents customs audit penalties and ensures client accounts receive 100% legitimate GST input tax credits without dispute.",
        "feature": "Pre-configured HSN catalog with verified GST and customs duty rates.",
        "is_live": False
    },
    # Engine 3: Godown Stock & Spare Parts (Modules 18-25)
    {
        "id": "ERP-MOD-18",
        "title": "Real-Time Godown & Stock Ledger",
        "engine": "Engine 3: Godown & Spares Inventory",
        "role": "Godown Keeper, Inventory Manager",
        "does": "Tracks every machine, clutch assembly, and spare part across the Pune Warehouse and Chakan staging facilities by rack and bin location.",
        "benefit": "Sales staff can instantly check stock availability without needing to walk into the warehouse or call the godown supervisor.",
        "feature": "Live stock counter with instant search by category, tonnage, or part number.",
        "is_live": True
    },
    {
        "id": "ERP-MOD-19",
        "title": "Friction Plates & Wear Parts Tracker",
        "engine": "Engine 3: Godown & Spares Inventory",
        "role": "Spare Parts In-Charge",
        "does": "Keeps batch-level tracking of high-wear consumable parts: friction lining materials, thickness tolerances, and reorder levels.",
        "benefit": "Guarantees that when a forging plant calls with a worn brake lining during a breakdown, replacement parts are ready for immediate dispatch.",
        "feature": "Batch tracking with thickness wear tolerance limits and reorder thresholds.",
        "is_live": False
    },
    {
        "id": "ERP-MOD-20",
        "title": "Laser Serial Number & Heat Traceability",
        "engine": "Engine 3: Godown & Spares Inventory",
        "role": "Quality Inspector",
        "does": "Records the unique laser-etched serial number on every imported Italian clutch along with metallurgical heat certificates and test sheets.",
        "benefit": "Proves 100% genuine Italian origin to clients and enables fast warranty verification if a component ever needs factory inspection.",
        "feature": "Searchable serial number registry linked to Italian factory birth certificates.",
        "is_live": False
    },
    {
        "id": "ERP-MOD-21",
        "title": "Inward Quality Inspection (GRN Engine)",
        "engine": "Engine 3: Godown & Spares Inventory",
        "role": "Quality Control Engineer",
        "does": "A formal inspection protocol for incoming shipments checking crate condition, shaft runout, and pneumatic pressure leak decay before stock entry.",
        "benefit": "Catches any transit damage immediately so insurance claims can be filed before goods are accepted into company stock.",
        "feature": "Digital Goods Receipt Note (GRN) with photo upload and pressure test checklist.",
        "is_live": False
    },
    {
        "id": "ERP-MOD-22",
        "title": "Delivery Challan & Dispatch Paperwork",
        "engine": "Engine 3: Godown & Spares Inventory",
        "role": "Dispatch Supervisor",
        "does": "Generates statutory Rule 55 delivery challans and e-Way Bill pre-flight packets for transport trucks moving heavy machinery across state borders.",
        "benefit": "Prevents transport trucks from being stopped or impounded by state highway tax authorities due to missing transit documentation.",
        "feature": "1-click generation of statutory delivery challans with driver and vehicle details.",
        "is_live": False
    },
    {
        "id": "ERP-MOD-23",
        "title": "Workshop Repair & Service Ledger",
        "engine": "Engine 3: Godown & Spares Inventory",
        "role": "Service Center Head",
        "does": "Maintains digital job cards for clutch overhauls, flywheel resurfacing, brake relining, and 100-cycle live load bench testing in Pune.",
        "benefit": "Provides a documented engineering service history for every refurbished unit, proving quality to skeptical plant managers.",
        "feature": "Job card tracker recording technician hours, replaced parts, and test results.",
        "is_live": False
    },
    {
        "id": "ERP-MOD-24",
        "title": "Scrap & Damaged Parts Disposal",
        "engine": "Engine 3: Godown & Spares Inventory",
        "role": "Inventory Manager, Accountant",
        "does": "Formally logs unserviceable trade-in clutches and worn brake linings for scrap sale, recording GST tax reversal entries in accounting books.",
        "benefit": "Keeps the godown free of unserviceable clutter while ensuring company tax books remain 100% clean and audit-ready.",
        "feature": "Scrap write-off log with weight certificates and scrap sale invoice linkage.",
        "is_live": False
    },
    {
        "id": "ERP-MOD-25",
        "title": "Low Stock Warning & Reorder Timer",
        "engine": "Engine 3: Godown & Spares Inventory",
        "role": "Procurement Head",
        "does": "Automatically alerts management when fast-moving spare parts fall below safety thresholds, factoring in the 8-to-12 week Italy manufacturing time.",
        "benefit": "Prevents costly stockouts of critical spares, ensuring the company never loses an urgent order due to lack of inventory.",
        "feature": "Automated email/dashboard alerts triggered when stock hits reorder minimums.",
        "is_live": False
    },
    # Engine 4: Bills, GST Taxes, Money & Security (Modules 26-33)
    {
        "id": "ERP-MOD-26",
        "title": "GST Tax Invoice Generator",
        "engine": "Engine 4: Finance, GST & Security",
        "role": "Finance Department",
        "does": "Generates government-compliant B2B tax invoices with CGST, SGST, IGST tax breakdown, 8-digit HSN classification, and digital payment QR codes.",
        "benefit": "Produces clean, professional bills that corporate accounts departments process without delays or tax queries.",
        "feature": "Automated tax calculation and PDF invoice generation with corporate branding.",
        "is_live": False
    },
    {
        "id": "ERP-MOD-27",
        "title": "GSTR-1 Tax Return Exporter",
        "engine": "Engine 4: Finance, GST & Security",
        "role": "Chartered Accountant, Tax Head",
        "does": "Exports monthly sales records in the exact JSON and Excel formats required by the government GST portal, matching bank deposits.",
        "benefit": "Saves 3 to 4 days of tedious manual data entry for your accountant every month and eliminates GST reconciliation mismatches.",
        "feature": "1-click GST portal export button matching monthly bank receipts.",
        "is_live": False
    },
    {
        "id": "ERP-MOD-28",
        "title": "Customer Outstanding & Milestones",
        "engine": "Engine 4: Finance, GST & Security",
        "role": "Accounts Receivable Executive",
        "does": "Tracks pending customer payments against delivery and installation milestones, preventing machinery handover before payments are cleared.",
        "benefit": "Ensures that balance amounts and installation retention payments are collected promptly without capital remaining stuck.",
        "feature": "Customer outstanding ledger showing advance received, balance due, and dispatch status.",
        "is_live": False
    },
    {
        "id": "ERP-MOD-29",
        "title": "Payment Due Reminders & Overdue Tracker",
        "engine": "Engine 4: Finance, GST & Security",
        "role": "Credit Control Team",
        "does": "Categorizes pending bills by age (30, 60, 90+ days overdue) and sends polite, automated WhatsApp and email payment reminders to client finance teams.",
        "benefit": "Accelerates payment recovery, cuts debtor collection days, and protects company bank liquidity.",
        "feature": "Automated payment reminder escalation with attached PDF ledger statement.",
        "is_live": False
    },
    {
        "id": "ERP-MOD-30",
        "title": "Staff Access Roles & Permissions",
        "engine": "Engine 4: Finance, GST & Security",
        "role": "Managing Director, System Admin",
        "does": "Enforces strict permissions so staff members only see information relevant to their role (Sales reps see quotes; Godown staff see stock; Directors see profit).",
        "benefit": "Prevents unauthorized employees from seeing sensitive profit margins, confidential supplier costs, or executive financial reports.",
        "feature": "Role-based permission matrix separating Sales, Workshop, Accounts, and Executive access.",
        "is_live": True
    },
    {
        "id": "ERP-MOD-31",
        "title": "Tamper-Proof Audit History Log",
        "engine": "Engine 4: Finance, GST & Security",
        "role": "Internal Auditor, Managing Director",
        "does": "Permanently logs every user login, price change, quotation modification, and invoice cancellation with the exact user name, time, and computer address.",
        "benefit": "Total internal transparency; no staff member can secretly change prices, offer unauthorized discounts, or delete customer records without a trace.",
        "feature": "Cryptographic tamper-proof audit trail with over 316 verified historical records.",
        "is_live": True
    },
    {
        "id": "ERP-MOD-32",
        "title": "Daily Auto Local & Cloud Backup",
        "engine": "Engine 4: Finance, GST & Security",
        "role": "Operations Head, IT Lead",
        "does": "Automatically saves a complete snapshot of all company records, customer inquiries, and stock ledgers every night to both local and secure offsite storage.",
        "benefit": "Guarantees zero data loss even in the event of computer hardware failure, power cuts, accidental deletion, or internet outages.",
        "feature": "Automated nightly backup engine with verified recovery test snapshots.",
        "is_live": True
    },
    {
        "id": "ERP-MOD-33",
        "title": "Managing Director Business Dashboard",
        "engine": "Engine 4: Finance, GST & Security",
        "role": "Managing Director",
        "does": "A high-level executive dashboard showing total monthly revenue, gross profit margins, inventory turnover speed, and top client concentrations on one screen.",
        "benefit": "Gives the business owner total commercial clarity in 30 seconds every morning without needing to ask staff for manual reports.",
        "feature": "Live KPI tiles showing active inquiries, stock value, and month-to-date sales figures.",
        "is_live": True
    }
]

print(f"OMPI Modules configured: {len(ompi_modules)}")
