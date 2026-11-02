# scratch/generate_enlarged_spec.py
import os, sys, subprocess, shutil

print("Generating 32-Page Large-Font Pre-Commencement Executive Specification...")

# Define the 24 Routes of Dalal (Planned to be built)
dalal_routes = [
    # Page 2
    {
        "id": "ROUTE-01",
        "title": "Homepage & Machinery Showroom",
        "path": "Planned Route: /index.html",
        "audience": "Industrial Plant Owners, Factory Directors, Forging Heads",
        "sees": "A modern machinery showroom presenting heavy presses available for sale. Customers will see clear photographs, machine tonnages, video power trials, and a direct WhatsApp button to speak with Mr. Vinit Dalal.",
        "benefit": "Eliminates buyer skepticism. Factory owners see that machines are physically present in the Pune stockyard (not fake broker listings), establishing instant trust for deals from Rs. 50 Lakh to Rs. 4 Crore.",
        "feature": "1-Click WhatsApp inquiry button pre-filled with the exact machine model and capacity."
    },
    {
        "id": "ROUTE-02",
        "title": "Company Heritage & Facility Dossier",
        "path": "Planned Route: /about.html",
        "audience": "Corporate Procurement Heads, Bank Valuers, Joint-Venture Partners",
        "sees": "The 50-year engineering heritage of the Dalal family, photos of the Mumbai registered office and Pune warehouse yard, and details of the official technical partnership with OMPI Italy.",
        "benefit": "Proves corporate legitimacy and financial stability, assuring plant owners that their advance payments and multi-crore machinery orders are in trustworthy, experienced hands.",
        "feature": "Visual timeline highlighting 5 decades of heavy machinery supply across India."
    },
    # Page 3
    {
        "id": "ROUTE-03",
        "title": "Import, Rigging & Engineering Services",
        "path": "Planned Route: /services.html",
        "audience": "Plant Maintenance Heads, Factory Engineers, Project Directors",
        "sees": "A simple guide to heavy press services: overseas dismantling, port customs clearance, multi-axle trailer transport, foundation pit construction, and Italian pneumatic clutch retrofits.",
        "benefit": "Shows buyers that Dalal provides end-to-end support—not just selling the machine, but installing it on their factory floor, testing it under load, and guaranteeing spare parts.",
        "feature": "Clear 7-point FAQ explaining how High Seas Sales save time and customs duty."
    },
    {
        "id": "ROUTE-04",
        "title": "Machinery Catalog & Search Directory",
        "path": "Planned Route: /category.html",
        "audience": "Factory Sourcing Managers, Purchase Officers",
        "sees": "A clean, searchable directory of all 26 machine types (Forging Presses, Mechanical Presses, Hydraulic Presses, Horizontal Boring Machines) with instant tonnage filters.",
        "benefit": "Allows purchasing teams to find the exact tonnage and machine type they need in seconds without having to scroll through hundreds of irrelevant listings.",
        "feature": "Instant tonnage filter buttons (Under 500 Tons, 500T to 1,000 Tons, 1,000T to 4,000 Tons)."
    },
    # Page 4
    {
        "id": "ROUTE-05",
        "title": "Machine Technical Details Sheet (PDP)",
        "path": "Planned Route: /product.html",
        "audience": "Chief Technical Officers, Toolroom Managers, Plant Heads",
        "sees": "An in-depth technical sheet for each press: exact tonnage, ram stroke, bed dimensions, motor horsepower, country of make, live power inspection video, and ready-to-download quotation.",
        "benefit": "Gives plant technical heads every measurement and spec needed to confirm the press will fit their factory space, foundation pit, and forging dies.",
        "feature": "1-Click Download of an official, print-ready PDF machine quotation with full specs."
    },
    {
        "id": "ROUTE-06",
        "title": "Brand New Factory Machinery Lines",
        "path": "Planned Route: /brand-new-machinery.html",
        "audience": "Tier-1 Automotive Suppliers, High-Volume Manufacturing Plants",
        "sees": "Brand-new industrial machinery lines supplied with manufacturer warranty, complete European safety standards, and factory commissioning support.",
        "benefit": "Captures top-tier automotive companies that have strict internal corporate policies requiring brand-new equipment with factory guarantees rather than used machinery.",
        "feature": "Inquiry form specifically for custom-engineered new production lines."
    },
    # Page 5
    {
        "id": "ROUTE-07",
        "title": "Shipment, Yard & Rigging Photo Gallery",
        "path": "Planned Route: /gallery.html",
        "audience": "Factory Auditors, Sourcing Committees, Managing Directors",
        "sees": "A photographic gallery showing heavy 1,000-ton to 4,000-ton presses being lifted by giant hydraulic cranes, transported on 64-wheel trailers, and parked in the Pune stockyard.",
        "benefit": "Irrefutable proof of capability. Seeing real photos of heavy equipment handling eliminates any doubt about Dalal's ability to safely deliver massive machines.",
        "feature": "Filterable photo albums categorized by press tonnage and transport stages."
    },
    {
        "id": "ROUTE-08",
        "title": "Headquarters, Yard & Direct RFQ Portal",
        "path": "Planned Route: /contact.html",
        "audience": "Procurement Directors, Visiting Engineering Teams",
        "sees": "Interactive Google Map locations for both the Mumbai Registered Office (Tardeo) and the Pune Stockyard (Chakan), with direct phone numbers and a visit booking form.",
        "benefit": "Makes it effortless for serious corporate buyers to schedule an in-person physical inspection and see the machines run under live electric power before paying.",
        "feature": "Direct appointment booking console to schedule a live power trial in Pune."
    },
    # Page 6
    {
        "id": "ROUTE-09",
        "title": "Express Breakdown RFQ Console",
        "path": "Planned Route: /contact-2.html",
        "audience": "Plant Managers facing an urgent machine breakdown",
        "sees": "A fast, streamlined emergency request form asking only for required press tonnage, bed size, and delivery urgency, designed to be filled out in 30 seconds.",
        "benefit": "Captures high-priority hot leads whose production line has stopped and who have an urgent budget approved to buy a replacement press immediately.",
        "feature": "Instant high-priority notification sent directly to the Managing Director's WhatsApp."
    },
    {
        "id": "ROUTE-10",
        "title": "Import Compliance & Legal FAQs Guide",
        "path": "Planned Route: /faqs.html",
        "audience": "Chief Financial Officers (CFOs), Company Legal & Tax Advisors",
        "sees": "Clear, plain-English legal explanations of High Seas Sales, 100% GST input tax credit (ITC) claims, Customs Bill of Entry procedures, and live power inspection trials.",
        "benefit": "Removes legal and taxation fears from company accountants, providing clear documentation that speeds up corporate board approvals.",
        "feature": "7 interactive question accordions addressing customs duty and GST compliance."
    },
    # Page 7
    {
        "id": "ROUTE-11",
        "title": "Client Endorsements & Factory Proof",
        "path": "Planned Route: /testimonial.html",
        "audience": "Managing Directors, Capital Investment Committees",
        "sees": "Verified customer reviews, factory photos, and installation case studies from leading automotive forging and stamping plants across Pune, Rajkot, Chennai, and Delhi NCR.",
        "benefit": "Strong social proof showing that India's top automotive component manufacturers trust Dalal Machine Tools for their critical press lines.",
        "feature": "Customer testimonials displaying verified plant locations and installed machine tonnages."
    },
    {
        "id": "ROUTE-12",
        "title": "High Seas Tariffs & Cost Savings Guide",
        "path": "Planned Route: /pricing.html",
        "audience": "Finance Directors, Plant Owners, Purchasing Heads",
        "sees": "A transparent financial comparison showing how buying directly from port on High Seas saves 8% to 15% compared to purchasing machines delivered to local dealer yards.",
        "benefit": "Clearly explains pricing logic and demonstrates how buyers avoid double taxation, port demurrage, and middlemen markups.",
        "feature": "Interactive cost savings calculator showing estimated cash savings based on machine value."
    },
    # Page 8
    {
        "id": "ROUTE-13",
        "title": "Industrial Journal & Forging News Hub",
        "path": "Planned Route: /blog.html",
        "audience": "Plant Maintenance Engineers, Toolroom Supervisors",
        "sees": "Practical engineering articles on press maintenance, how to prevent crankshaft fractures, press leveling methods, and pneumatic clutch upgrade benefits.",
        "benefit": "Positions Dalal and OMPI as technical experts rather than just traders, attracting organic visits from factory engineers across India.",
        "feature": "Searchable technical article library organized by maintenance topic."
    },
    {
        "id": "ROUTE-14",
        "title": "Pneumatic Clutch Conversion Guide",
        "path": "Planned Route: /blog-single.html",
        "audience": "Maintenance Managers, Factory Modernization Teams",
        "sees": "An easy-to-understand visual guide explaining why old mechanical dog clutches cause costly downtime and how converting to OMPI pneumatic clutches increases safety and speed.",
        "benefit": "Directly generates inquiries for OMPI clutch retrofit projects by showing factory heads how an upgrade pays for itself within 6 months.",
        "feature": "Step-by-step conversion timeline and before-and-after production rate comparison."
    },
    # Page 9
    {
        "id": "ROUTE-15",
        "title": "2500T Turnkey Overhaul Case Study",
        "path": "Planned Route: /blog-large-image.html",
        "audience": "Plant Directors, Heavy Forging Plant Heads",
        "sees": "A complete photo-story of a massive 2,500-ton Russian forging press being dismantled in Europe, shipped to India, overhauled in Pune, and commissioned in a live plant.",
        "benefit": "Shows prospective buyers that Dalal has the technical capability to handle massive multi-crore plant overhauls smoothly without risk.",
        "feature": "Chronological project timeline showing precision bed machining and foundation pit checks."
    },
    {
        "id": "ROUTE-16",
        "title": "Project Portfolio & Installation Archive",
        "path": "Planned Route: /projects.html",
        "audience": "EPC Contractors, Factory Expansion Teams",
        "sees": "A comprehensive showcase of past plant installations, on-site boring jobs, and heavy transport projects completed for forging plants across India.",
        "benefit": "Provides irrefutable proof of execution across diverse industries (Automotive, Defense, Railway, Heavy Engineering).",
        "feature": "Searchable project grid with filters for press tonnage and client industry."
    },
    # Page 10
    {
        "id": "ROUTE-17",
        "title": "120-Ton Heavy Press Transport Detail",
        "path": "Planned Route: /projects-single.html",
        "audience": "Factory Logistics Heads, Plant Engineers",
        "sees": "A detailed technical report showing how a giant 120-ton press frame was unloaded, brought inside a tight factory shed, and lowered into its foundation pit.",
        "benefit": "Assures factory owners that even the heaviest machines will be transported and positioned safely without damaging factory floors or roofs.",
        "feature": "Illustrated engineering breakdown of hydraulic strand-jacking and low-bed trailer delivery."
    },
    {
        "id": "ROUTE-18",
        "title": "Automotive Sector Plant Modernization",
        "path": "Planned Route: /projects-modern.html",
        "audience": "Automotive Tier-1 Plant Managers",
        "sees": "Specialized press automation services, automated coil feeding lines, and die-cushion upgrades tailored specifically for automotive parts manufacturing.",
        "benefit": "Attracts high-value plant modernization projects from automotive component manufacturers looking to boost daily output.",
        "feature": "Checklist of press automation upgrades with expected cycle time improvements."
    },
    # Page 11
    {
        "id": "ROUTE-19",
        "title": "Filterable Case Study Library",
        "path": "Planned Route: /projects-with-filter.html",
        "audience": "Capital Sourcing Committees, Plant Valuers",
        "sees": "A searchable project library where buyers can view only past installations matching their required tonnage (Under 500T, 500T to 1500T, or 1500T+).",
        "benefit": "Allows a factory owner looking for a specific press size to see exact proof of similar machines Dalal has successfully installed.",
        "feature": "1-click tonnage filter that instantly updates the displayed project case studies."
    },
    {
        "id": "ROUTE-20",
        "title": "Tooling, Bolster Plates & Spares Shop",
        "path": "Planned Route: /shop.html",
        "audience": "Spare Parts Purchasing Officers, Toolroom Heads",
        "sees": "A catalog of high-wear press spare parts: bolster plates, tie-rod nuts, pneumatic valves, hydraulic cylinders, and clutch friction pads.",
        "benefit": "Creates recurring monthly spare parts revenue from existing factories even after their initial machine purchase.",
        "feature": "Stock status tags showing which critical spare parts are ready for immediate dispatch from Pune."
    },
    # Page 12
    {
        "id": "ROUTE-21",
        "title": "Spare Part Engineering Specifications",
        "path": "Planned Route: /shop-single.html",
        "audience": "Toolroom Engineers, Maintenance Supervisors",
        "sees": "Detailed specifications for spare parts including steel grade (EN8, EN19, 42CrMo4), surface hardening, exact dimensions, and drawing inquiry options.",
        "benefit": "Guarantees that spare components will fit the customer's exact press model without needing costly on-site modifications.",
        "feature": "Direct button to request technical drawing verification before ordering."
    },
    {
        "id": "ROUTE-22",
        "title": "Multi-Item RFQ Package Inquiry Cart",
        "path": "Planned Route: /shoping-cart.html",
        "audience": "Plant Sourcing Managers, Purchase Officers",
        "sees": "A simple list where buyers can bundle multiple machines, spare parts, and clutch conversion kits into one single quotation request.",
        "benefit": "Increases deal size by making it easy for factories to purchase a complete package (Press + OMPI Clutch + Spare Parts) in one go.",
        "feature": "Consolidated package summary with a 1-click WhatsApp quote button for the whole order."
    },
    # Page 13
    {
        "id": "ROUTE-23",
        "title": "Formal Procurement Proposal Submission",
        "path": "Planned Route: /checkout.html",
        "audience": "Corporate Purchasing Executives, Finance Teams",
        "sees": "A professional procurement form where buyers enter their company name, 15-digit GSTIN, factory delivery address, and expected delivery timeline.",
        "benefit": "Delivers pre-qualified, serious corporate inquiries with complete billing and delivery details directly to the sales team.",
        "feature": "Automated GST number verification ensuring official corporate inquiries."
    },
    {
        "id": "ROUTE-24",
        "title": "Smart Error Recovery & Alternative Stock",
        "path": "Planned Route: /404.html",
        "audience": "Any visitor who clicks an outdated or mistyped link",
        "sees": "Instead of a broken blank page, a helpful screen that suggests active presses currently in stock with a search bar and direct WhatsApp assistance.",
        "benefit": "Prevents potential customers from leaving the site and converts broken link visits into real machinery inquiries.",
        "feature": "Automatic display of top 3 currently available presses in the Pune stockyard."
    }
]

# Define the 33 Modules of OMPI (Planned to be built)
ompi_modules = [
    # Engine 1: Sales & Commercial (Modules 1-10)
    {
        "id": "ERP-MOD-01",
        "title": "Client Records & GST Credit Master",
        "engine": "Engine 1: Sales & Customer Pipeline",
        "role": "Sales Executives, Accounts Manager",
        "does": "Will maintain a central profile for every client factory: verified 15-digit GSTIN, multiple delivery godown addresses, authorized contact persons, and approved credit limits.",
        "benefit": "Stops costly billing errors, prevents dispatching goods to companies with overdue payments, and ensures tax invoices match GST portal records.",
        "feature": "Automated GST number validation and company ledger outstanding summary."
    },
    {
        "id": "ERP-MOD-02",
        "title": "OMPI Technical Catalog & SKU Master",
        "engine": "Engine 1: Sales & Customer Pipeline",
        "role": "Technical Sales Engineers",
        "does": "Will organize all Italian pneumatic clutch-brakes, rotating unions, and friction discs by bore size, torque capacity, and dimensional cross-references.",
        "benefit": "Allows sales representatives to find the exact replacement clutch model in 10 seconds without needing to search through paper product catalogs.",
        "feature": "Quick lookup connecting press brand names with suitable OMPI clutch models."
    },
    {
        "id": "ERP-MOD-03",
        "title": "Import Currency & Landed Pricing Engine",
        "engine": "Engine 1: Sales & Customer Pipeline",
        "role": "Commercial Manager, Managing Director",
        "does": "Will calculate selling prices in Indian Rupees based on current Euro exchange rates, ocean shipping costs, customs duty, and minimum profit margins.",
        "benefit": "Protects company profits against sudden currency fluctuations between the Euro and the Rupee during the 4 to 8 weeks of ocean shipping.",
        "feature": "Automated price calculation incorporating daily exchange rates and port handling fees."
    },
    {
        "id": "ERP-MOD-04",
        "title": "Fast-Quote 60-Second PDF Generator",
        "engine": "Engine 1: Sales & Customer Pipeline",
        "role": "Sales Representatives",
        "does": "Will compile professional, branded quotation letters complete with machine photos, dimensions, prices, and payment terms in under 60 seconds.",
        "benefit": "Allows your team to send an official proposal while the customer is still on the phone, beating competitors who take 2 to 3 days to send a quote.",
        "feature": "1-click generation of print-ready A4 PDF proposals with official company signature."
    },
    {
        "id": "ERP-MOD-05",
        "title": "Customer Inquiry Visual Pipeline",
        "engine": "Engine 1: Sales & Customer Pipeline",
        "role": "Sales Team, Managing Director",
        "does": "Will display all incoming customer inquiries on a visual stage board: New Lead -> Sized -> Quoted -> PO Awaited -> Deal Won -> Delivered.",
        "benefit": "Gives the Managing Director complete visibility over every active deal so no high-value customer inquiry is ever forgotten or neglected.",
        "feature": "Visual stage cards with color-coded alerts for inquiries needing fast follow-up."
    },
    {
        "id": "ERP-MOD-06",
        "title": "Press & Clutch Compatibility Matrix",
        "engine": "Engine 1: Sales & Customer Pipeline",
        "role": "Technical Sourcing Engineers",
        "does": "Will cross-index leading press makes (Aida, Schuler, Godrej, Voronezh, Li Chin) with the exact OMPI clutch-brake combination required for bolt-on installation.",
        "benefit": "Enables sales reps to confidently advise plant owners on the exact clutch required without waiting for on-site engineer measurements.",
        "feature": "Pre-configured compatibility lookup providing accurate clutch recommendations for known press models."
    },
    {
        "id": "ERP-MOD-07",
        "title": "Profit Margin & Discount Protection",
        "engine": "Engine 1: Sales & Customer Pipeline",
        "role": "Managing Director, Finance Head",
        "does": "Will enforce a strict minimum profit floor (e.g. 22%) and automatically block sales representatives from offering discounts without Managing Director sign-off.",
        "benefit": "Guarantees healthy commercial profitability and prevents junior sales reps from giving away company margins to close easy deals.",
        "feature": "Password-protected discount override approval requiring Director authorization."
    },
    {
        "id": "ERP-MOD-08",
        "title": "Proforma Invoice (PI) Generator",
        "engine": "Engine 1: Sales & Customer Pipeline",
        "role": "Accounts Executive",
        "does": "Will issue formal proforma invoices with clearly stated milestone payment terms: 30% Advance, 50% Against Dispatch, and 20% Post-Installation.",
        "benefit": "Ensures clean payment terms before any machinery leaves the yard, safeguarding company cash flow and preventing uncollected retention dues.",
        "feature": "Pre-formatted payment milestone schedule with company RTGS/NEFT banking details."
    },
    {
        "id": "ERP-MOD-09",
        "title": "Sales Order & Warehouse Stock Hold",
        "engine": "Engine 1: Sales & Customer Pipeline",
        "role": "Sales Operations, Godown Keeper",
        "does": "Will convert approved quotes into active ERP sales orders and automatically lock the selected machine or clutch unit in the godown ledger.",
        "benefit": "Eliminates embarrassing double-selling mistakes where two different sales reps try to sell the same warehouse unit to two different clients.",
        "feature": "Automated status switch changing machine from 'Available' to 'Under Commercial Hold'."
    },
    {
        "id": "ERP-MOD-10",
        "title": "WhatsApp & Email Quote Dispatcher",
        "engine": "Engine 1: Sales & Customer Pipeline",
        "role": "Sales Operations",
        "does": "Will send official quotation PDFs and inspection photos directly to the client's WhatsApp and email with a personalized, professional cover message.",
        "benefit": "Achieves 90% higher open and response rates than traditional email, allowing immediate conversation with busy factory decision-makers.",
        "feature": "Direct WhatsApp notification dispatch with pre-filled machine reference numbers."
    },
    # Engine 2: Italy Purchase & Landed Costing (Modules 11-17)
    {
        "id": "ERP-MOD-11",
        "title": "Assembly Parts Breakdown (BOM)",
        "engine": "Engine 2: Purchase & Landed Cost",
        "role": "Assembly Workshop Supervisor",
        "does": "Will maintain an exact parts list for each clutch assembly down to every friction pad, seal kit, return spring, and dual pneumatic safety valve.",
        "benefit": "Ensures the workshop never gets stuck mid-assembly due to a missing 500-rupee seal kit on a 15-lakh clutch order.",
        "feature": "Exploded assembly parts tree showing part numbers and godown shelf locations."
    },
    {
        "id": "ERP-MOD-12",
        "title": "Italy Import Purchase Order (PO)",
        "engine": "Engine 2: Purchase & Landed Cost",
        "role": "Import Procurement Manager",
        "does": "Will generate formal international purchase orders in Euros formatted to OMPI Italy OEM specifications, tracking sea container schedules.",
        "benefit": "Eliminates ordering mistakes, provides proper dockets for bank foreign remittances, and tracks production lead times in Modena, Italy.",
        "feature": "Euro purchase order generator with OEM drawing codes and expected ocean shipment dates."
    },
    {
        "id": "ERP-MOD-13",
        "title": "Total Landed Cost & Customs Calculator",
        "engine": "Engine 2: Purchase & Landed Cost",
        "role": "Commercial Manager, Accountant",
        "does": "Will calculate the true total cost of imported units including Basic Customs Duty (7.5%), Social Welfare Surcharge, IGST (18%), and port clearing charges.",
        "benefit": "Shows the exact landed cost per unit in Rupees so management knows the true profit margin before quoting clients.",
        "feature": "Automated import duty calculator compliant with current Indian Customs tariff rules."
    },
    {
        "id": "ERP-MOD-14",
        "title": "Sea Container & Shipping Tracker",
        "engine": "Engine 2: Purchase & Landed Cost",
        "role": "Logistics Coordinator",
        "does": "Will track ocean containers from Italy ports (Genoa, La Spezia) through JNPT Nhava Sheva, logging Bill of Lading numbers and port arrival dates.",
        "benefit": "Prevents expensive port container demurrage and detention charges by preparing customs papers before the ship berths.",
        "feature": "Container milestone timeline with 14-day free-time tracking alerts."
    },
    {
        "id": "ERP-MOD-15",
        "title": "Technical CAD & GA Drawing Archive",
        "engine": "Engine 2: Purchase & Landed Cost",
        "role": "Design Engineers, Service Team",
        "does": "Will provide a secure central archive of certified CAD blueprints and general arrangement drawings for factory foundation and clutch retrofit fitting.",
        "benefit": "Allows client engineering teams to prepare foundation bolts and air supply lines weeks before the machinery physically arrives.",
        "feature": "Downloadable certified drawings organized by press model and clutch series."
    },
    {
        "id": "ERP-MOD-16",
        "title": "Clutch Sizing & Torque Calculator",
        "engine": "Engine 2: Purchase & Landed Cost",
        "role": "Application Engineers",
        "does": "Will calculate the required clutch torque based on press flywheel speed, motor horsepower, and available factory compressed air pressure (5.5 to 6.0 bar).",
        "benefit": "Guarantees that the installed clutch will never slip, overheat, or fail during continuous heavy forging operations.",
        "feature": "Engineered sizing calculation matching press flywheel speed to the correct OMPI model."
    },
    {
        "id": "ERP-MOD-17",
        "title": "HSN Tax Code & Customs Tariff Master",
        "engine": "Engine 2: Purchase & Landed Cost",
        "role": "Company Accountant, Tax Advisor",
        "does": "Will serve as a central master of all 8-digit government tax codes (HSN 8483, 8462, 6813) with current GST rates and customs duty classifications.",
        "benefit": "Prevents customs audit penalties and ensures client accounts receive 100% legitimate GST input tax credits without dispute.",
        "feature": "Pre-configured HSN catalog with verified GST and customs duty rates."
    },
    # Engine 3: Godown Stock & Spare Parts (Modules 18-25)
    {
        "id": "ERP-MOD-18",
        "title": "Real-Time Godown & Stock Ledger",
        "engine": "Engine 3: Godown & Spares Inventory",
        "role": "Godown Keeper, Inventory Manager",
        "does": "Will track every machine, clutch assembly, and spare part across the Pune Warehouse and Chakan staging facilities by rack and bin location.",
        "benefit": "Sales staff can instantly check stock availability without needing to walk into the warehouse or call the godown supervisor.",
        "feature": "Live stock counter with instant search by category, tonnage, or part number."
    },
    {
        "id": "ERP-MOD-19",
        "title": "Friction Plates & Wear Parts Tracker",
        "engine": "Engine 3: Godown & Spares Inventory",
        "role": "Spare Parts In-Charge",
        "does": "Will maintain batch-level tracking of high-wear consumable parts: friction lining materials, thickness tolerances, and reorder levels.",
        "benefit": "Guarantees that when a forging plant calls with a worn brake lining during a breakdown, replacement parts are ready for immediate dispatch.",
        "feature": "Batch tracking with thickness wear tolerance limits and reorder thresholds."
    },
    {
        "id": "ERP-MOD-20",
        "title": "Laser Serial Number & Heat Traceability",
        "engine": "Engine 3: Godown & Spares Inventory",
        "role": "Quality Inspector",
        "does": "Will record the unique laser-etched serial number on every imported Italian clutch along with metallurgical heat certificates and test sheets.",
        "benefit": "Proves 100% genuine Italian origin to clients and enables fast warranty verification if a component ever needs factory inspection.",
        "feature": "Searchable serial number registry linked to Italian factory birth certificates."
    },
    {
        "id": "ERP-MOD-21",
        "title": "Inward Quality Inspection (GRN Engine)",
        "engine": "Engine 3: Godown & Spares Inventory",
        "role": "Quality Control Engineer",
        "does": "Will provide a formal inspection protocol for incoming shipments checking crate condition, shaft runout, and air pressure leak decay before stock entry.",
        "benefit": "Catches any transit damage immediately so insurance claims can be filed before goods are accepted into company stock.",
        "feature": "Digital Goods Receipt Note (GRN) with photo upload and pressure test checklist."
    },
    {
        "id": "ERP-MOD-22",
        "title": "Delivery Challan & Dispatch Paperwork",
        "engine": "Engine 3: Godown & Spares Inventory",
        "role": "Dispatch Supervisor",
        "does": "Will generate statutory Rule 55 delivery challans and e-Way Bill pre-flight packets for transport trucks moving heavy machinery across state borders.",
        "benefit": "Prevents transport trucks from being stopped or impounded by state highway tax authorities due to missing transit documentation.",
        "feature": "1-click generation of statutory delivery challans with driver and vehicle details."
    },
    {
        "id": "ERP-MOD-23",
        "title": "Workshop Repair & Service Ledger",
        "engine": "Engine 3: Godown & Spares Inventory",
        "role": "Service Center Head",
        "does": "Will maintain digital job cards for clutch overhauls, flywheel resurfacing, brake relining, and live test-bench trials in Pune.",
        "benefit": "Provides a documented engineering service history for every refurbished unit, proving quality to skeptical plant managers.",
        "feature": "Job card tracker recording technician hours, replaced parts, and test results."
    },
    {
        "id": "ERP-MOD-24",
        "title": "Scrap & Damaged Parts Disposal",
        "engine": "Engine 3: Godown & Spares Inventory",
        "role": "Inventory Manager, Accountant",
        "does": "Will formally log unserviceable trade-in clutches and worn brake linings for scrap sale, recording GST tax reversal entries in accounting books.",
        "benefit": "Keeps the godown free of unserviceable clutter while ensuring company tax books remain 100% clean and audit-ready.",
        "feature": "Scrap write-off log with weight certificates and scrap sale invoice linkage."
    },
    {
        "id": "ERP-MOD-25",
        "title": "Low Stock Warning & Reorder Timer",
        "engine": "Engine 3: Godown & Spares Inventory",
        "role": "Procurement Head",
        "does": "Will automatically alert management when fast-moving spare parts fall below safety thresholds, factoring in the 8-to-12 week Italy manufacturing time.",
        "benefit": "Prevents costly stockouts of critical spares, ensuring the company never loses an urgent order due to lack of inventory.",
        "feature": "Automated email/dashboard alerts triggered when stock hits reorder minimums."
    },
    # Engine 4: Bills, GST Taxes, Money & Security (Modules 26-33)
    {
        "id": "ERP-MOD-26",
        "title": "GST Tax Invoice Generator",
        "engine": "Engine 4: Finance, GST & Security",
        "role": "Finance Department",
        "does": "Will generate government-compliant B2B tax invoices with CGST, SGST, IGST tax breakdown, 8-digit HSN classification, and digital payment QR codes.",
        "benefit": "Produces clean, professional bills that corporate accounts departments process without delays or tax queries.",
        "feature": "Automated tax calculation and PDF invoice generation with corporate branding."
    },
    {
        "id": "ERP-MOD-27",
        "title": "GSTR-1 Tax Return Exporter",
        "engine": "Engine 4: Finance, GST & Security",
        "role": "Chartered Accountant, Tax Head",
        "does": "Will export monthly sales records in the exact JSON and Excel formats required by the government GST portal, matching bank deposits.",
        "benefit": "Saves 3 to 4 days of tedious manual data entry for your accountant every month and eliminates GST reconciliation mismatches.",
        "feature": "1-click GST portal export button matching monthly bank receipts."
    },
    {
        "id": "ERP-MOD-28",
        "title": "Customer Outstanding & Milestones",
        "engine": "Engine 4: Finance, GST & Security",
        "role": "Accounts Receivable Executive",
        "does": "Will track pending customer payments against delivery and installation milestones, preventing machinery handover before payments are cleared.",
        "benefit": "Ensures that balance amounts and installation retention payments are collected promptly without capital remaining stuck.",
        "feature": "Customer outstanding ledger showing advance received, balance due, and dispatch status."
    },
    {
        "id": "ERP-MOD-29",
        "title": "Payment Due Reminders & Overdue Tracker",
        "engine": "Engine 4: Finance, GST & Security",
        "role": "Credit Control Team",
        "does": "Will categorize pending bills by age (30, 60, 90+ days overdue) and send polite, automated WhatsApp and email payment reminders to client finance teams.",
        "benefit": "Accelerates payment recovery, cuts debtor collection days, and protects company bank liquidity.",
        "feature": "Automated payment reminder escalation with attached PDF ledger statement."
    },
    {
        "id": "ERP-MOD-30",
        "title": "Staff Access Roles & Permissions",
        "engine": "Engine 4: Finance, GST & Security",
        "role": "Managing Director, System Admin",
        "does": "Will enforce strict permissions so staff members only see information relevant to their role (Sales reps see quotes; Godown staff see stock; Directors see profit).",
        "benefit": "Prevents unauthorized employees from seeing sensitive profit margins, confidential supplier costs, or executive financial reports.",
        "feature": "Role-based permission matrix separating Sales, Workshop, Accounts, and Executive access."
    },
    {
        "id": "ERP-MOD-31",
        "title": "Tamper-Proof Audit History Log",
        "engine": "Engine 4: Finance, GST & Security",
        "role": "Internal Auditor, Managing Director",
        "does": "Will permanently log every user login, price change, quotation modification, and invoice cancellation with the exact user name, time, and computer record.",
        "benefit": "Total internal transparency; no staff member can secretly change prices, offer unauthorized discounts, or delete customer records without a trace.",
        "feature": "Complete unchangeable history log recording every staff action with date and time stamp."
    },
    {
        "id": "ERP-MOD-32",
        "title": "Daily Auto Local & Cloud Backup",
        "engine": "Engine 4: Finance, GST & Security",
        "role": "Operations Head, IT Lead",
        "does": "Will automatically save a complete snapshot of all company records, customer inquiries, and stock ledgers every night to both local and secure offsite storage.",
        "benefit": "Guarantees zero data loss even in the event of computer hardware failure, power cuts, accidental deletion, or internet outages.",
        "feature": "Automated nightly backup system with zero manual effort required."
    },
    {
        "id": "ERP-MOD-33",
        "title": "Managing Director Business Dashboard",
        "engine": "Engine 4: Finance, GST & Security",
        "role": "Managing Director",
        "does": "Will provide a high-level executive dashboard showing total monthly revenue, gross profit margins, inventory turnover speed, and top client concentrations on one screen.",
        "benefit": "Gives the business owner total commercial clarity in 30 seconds every morning without needing to ask staff for manual reports.",
        "feature": "Live business summary tiles showing active inquiries, stock value, and month-to-date sales figures."
    }
]

print("Building HTML with enlarged typography and pre-commencement framing...")

# HTML Header with enlarged typography (10.2pt body, large titles, high-legibility layout)
html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Dalal Machine Tools & OMPI India - Pre-Commencement Master Business Blueprint (57 Proposed Systems & Modules)</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@600;700&display=swap" rel="stylesheet">
  <style>
    @page {
      size: A4 portrait;
      margin: 8mm 10mm 8mm 10mm;
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
      font-size: 10.2pt;
      line-height: 1.45;
      -webkit-print-color-adjust: exact;
      print-color-adjust: exact;
    }
    .page {
      height: 281mm;
      max-height: 281mm;
      overflow: hidden;
      box-sizing: border-box;
      position: relative;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      page-break-after: always;
      break-after: page;
      padding: 1px 0;
    }
    .page:last-child {
      page-break-after: avoid;
      break-after: avoid;
    }
    .page-content {
      flex: 1;
    }

    /* Corporate Header */
    .header-bar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 2.5px solid #0f172a;
      border-top: 4px solid #d97706;
      padding-top: 5px;
      padding-bottom: 5px;
      margin-bottom: 6px;
    }
    .brand-title {
      font-size: 11.8pt;
      font-weight: 800;
      color: #0f172a;
      letter-spacing: -0.2px;
    }
    .brand-subtitle {
      font-size: 8.2pt;
      font-weight: 700;
      color: #b45309;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }
    .doc-meta {
      text-align: right;
      font-size: 7.6pt;
      color: #475569;
      line-height: 1.3;
    }

    /* Strict Confidentiality & Pre-Commencement Warning Bar */
    .confidential-bar {
      background: #fef2f2;
      border: 1.5px solid #dc2626;
      border-radius: 4px;
      padding: 4.5px 9px;
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
      padding: 2px 7px;
      border-radius: 3px;
      text-transform: uppercase;
      font-size: 7.2pt;
      letter-spacing: 0.5px;
      font-weight: 800;
    }

    /* Section Subheaders */
    .section-header {
      background: #0f172a;
      color: #ffffff;
      padding: 5px 9px;
      border-radius: 4px;
      margin-bottom: 7px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .section-title {
      font-size: 9.0pt;
      font-weight: 800;
      letter-spacing: 0.3px;
      text-transform: uppercase;
    }
    .section-tag {
      font-size: 7.6pt;
      font-weight: 700;
      background: #f59e0b;
      color: #0f172a;
      padding: 2px 7px;
      border-radius: 3px;
    }

    /* Standard Card Box (2 per page, enlarged and legible) */
    .card-box {
      border: 1.5px solid #cbd5e1;
      border-radius: 6px;
      background: #ffffff;
      margin-bottom: 7px;
      padding: 9px 12px;
    }
    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 1.5px solid #e2e8f0;
      padding-bottom: 5px;
      margin-bottom: 6px;
    }
    .badge-id {
      background: #0f172a;
      color: #ffffff;
      padding: 2px 7px;
      border-radius: 3px;
      font-size: 8.2pt;
      font-weight: 800;
      font-family: 'JetBrains Mono', monospace;
      margin-right: 6px;
    }
    .card-title {
      font-size: 10.6pt;
      font-weight: 800;
      color: #0f172a;
    }
    .card-path {
      font-family: 'JetBrains Mono', monospace;
      font-size: 7.8pt;
      color: #b45309;
      font-weight: 700;
      background: #fffbeb;
      padding: 2px 7px;
      border: 1px solid #fef3c7;
      border-radius: 3px;
    }
    .card-status {
      font-size: 7.6pt;
      font-weight: 700;
      padding: 2px 7px;
      border-radius: 3px;
      margin-left: 6px;
      background: #f1f5f9;
      color: #334155;
      border: 1px solid #cbd5e1;
    }

    /* Simple 2-Column Content Grid */
    .simple-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 10px;
      margin-bottom: 6px;
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
      font-size: 9.4pt;
      line-height: 1.42;
      color: #334155;
    }

    /* Highlight Feature Box */
    .feature-strip {
      background: #f8fafc;
      border: 1px solid #e2e8f0;
      border-radius: 4px;
      padding: 5px 9px;
      font-size: 8.9pt;
      line-height: 1.4;
      color: #1e293b;
    }
    .feature-strip strong {
      color: #0f172a;
    }

    /* Corporate Footer */
    .footer-bar {
      border-top: 1.5px solid #cbd5e1;
      padding-top: 4px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 7.4pt;
      color: #64748b;
      margin-top: auto;
    }
    .confidential-watermark {
      font-weight: 800;
      color: #dc2626;
      letter-spacing: 0.5px;
      text-transform: uppercase;
    }
  </style>
</head>
<body>
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

def make_route_card(r):
    return f"""
      <div class="card-box">
        <div class="card-header">
          <div>
            <span class="badge-id">{r['id']}</span>
            <span class="card-title">{r['title']}</span>
            <span class="card-status">&#9675; TO BE BUILT: SYSTEM 1</span>
          </div>
          <div class="card-path">{r['path']}</div>
        </div>
        <div style="font-size:8.0pt; color:#64748b; font-weight:700; margin-bottom:5px;">
          <strong>Target User / Audience:</strong> {r['audience']}
        </div>
        <div class="simple-grid">
          <div>
            <div class="grid-label">What Will Be Built on Screen for Customers</div>
            <div class="grid-text">{r['sees']}</div>
          </div>
          <div>
            <div class="grid-label">Why It Will Be Built &amp; How It Will Bring Deals</div>
            <div class="grid-text">{r['benefit']}</div>
          </div>
        </div>
        <div class="feature-strip">
          <strong>Key Capability to be Engineered:</strong> {r['feature']}
        </div>
      </div>
"""

def make_module_card(m):
    return f"""
      <div class="card-box">
        <div class="card-header">
          <div>
            <span class="badge-id">{m['id']}</span>
            <span class="card-title">{m['title']}</span>
            <span class="card-status">&#9675; TO BE BUILT: SYSTEM 2</span>
          </div>
          <div style="font-size:7.8pt; font-weight:700; color:#b45309; background:#fffbeb; padding:2px 7px; border:1px solid #fef3c7; border-radius:3px;">{m['engine']}</div>
        </div>
        <div style="font-size:8.0pt; color:#64748b; font-weight:700; margin-bottom:5px;">
          <strong>Responsible Staff Role:</strong> {m['role']}
        </div>
        <div class="simple-grid">
          <div>
            <div class="grid-label">What This Management Tool Will Do Once Built</div>
            <div class="grid-text">{m['does']}</div>
          </div>
          <div>
            <div class="grid-label">Business Value &amp; Commercial Risk It Prevents</div>
            <div class="grid-text">{m['benefit']}</div>
          </div>
        </div>
        <div class="feature-strip">
          <strong>Key Management Feature:</strong> {m['feature']}
        </div>
      </div>
"""

# PAGE 1: COVER & PRE-COMMENCEMENT STATEMENT
html += f"""
  <div class="page">
    <div class="page-content">
      {make_header("PRE-COMMENCEMENT ARCHITECTURAL MASTER BLUEPRINT &bull; 57 PROPOSED UNITS")}

      <!-- Pre-Commencement Notice Banner -->
      <div style="background:#fffbeb; border:2px solid #f59e0b; border-radius:6px; padding:11px 14px; margin-bottom:10px;">
        <div style="font-size:10.0pt; font-weight:800; color:#b45309; text-transform:uppercase; margin-bottom:4px; display:flex; align-items:center; gap:6px;">
          <span>&#9888; IMPORTANT PRE-PROJECT STATEMENT: DEVELOPMENT WORK NOT YET STARTED</span>
        </div>
        <p style="font-size:9.2pt; line-height:1.44; color:#78350f; margin-bottom:4px;">
          <strong>Notice of Scope Baseline:</strong> This document represents the complete, pre-commencement architectural specification of the <strong>57 pages, operational modules, and management tools</strong> proposed to be engineered for <strong>Dalal Machine Tools Agency Pvt. Ltd.</strong> and <strong>OMPI India LLP</strong>.
        </p>
        <p style="font-size:9.0pt; line-height:1.42; color:#92400e;">
          <strong>Work Status:</strong> Currently, software development work has <strong>NOT</strong> commenced. This document details the exact functional scope, layout design, and operational workflows that will be constructed, tested, and delivered upon formal client sign-off and project kickoff.
        </p>
      </div>

      <!-- Legal Non-Disclosure Notice -->
      <div style="background:#fff1f2; border:2px solid #e11d48; border-radius:6px; padding:10px 14px; margin-bottom:10px;">
        <div style="font-size:9.5pt; font-weight:800; color:#9f1239; text-transform:uppercase; margin-bottom:3px; display:flex; align-items:center; gap:6px;">
          <span>&#128274; STRICT CONFIDENTIALITY &amp; ANTI-SHARING COVENANT</span>
        </div>
        <p style="font-size:8.9pt; line-height:1.42; color:#4c0519; margin-bottom:3px;">
          <strong>Restricted Distribution:</strong> This document contains proprietary business logic, pricing workflows, supply chain formulas, and commercial system designs prepared exclusively for the private review of the Managing Director and partners.
        </p>
        <p style="font-size:8.7pt; line-height:1.4; color:#881337;">
          <strong>Sharing Strictly Prohibited:</strong> Copying, photographing, forwarding, or sharing this document with any third party, competitor, external broker, or unauthorized personnel is <strong>strictly prohibited</strong>.
        </p>
      </div>

      <!-- Company Profiles Grid -->
      <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px; background:#f8fafc; border:1.5px solid #cbd5e1; border-radius:6px; padding:9px 12px; margin-bottom:10px;">
        <div style="font-size:8.9pt; line-height:1.4; color:#334155;">
          <div style="font-size:8.0pt; font-weight:800; color:#0f172a; text-transform:uppercase; letter-spacing:0.5px; margin-bottom:2px;">
            Target System 1: Heavy Machinery Platform
          </div>
          <strong style="font-size:10.0pt; color:#0f172a;">Dalal Machine Tools Agency Pvt. Ltd.</strong><br>
          Commerce Centre, Tardeo, Mumbai &bull; Pune Stockyard, Chakan<br>
          <strong>Proposed Scope:</strong> High-ticket digital acquisition platform (24 pages) for heavy forging presses (100T to 6,300T) with direct WhatsApp inquiry capture.
        </div>
        <div style="font-size:8.9pt; line-height:1.4; color:#334155;">
          <div style="font-size:8.0pt; font-weight:800; color:#0f172a; text-transform:uppercase; letter-spacing:0.5px; margin-bottom:2px;">
            Target System 2: Precision Clutches &amp; ERP
          </div>
          <strong style="font-size:10.0pt; color:#0f172a;">OMPI India LLP</strong><br>
          Pimpri-Chinchwad / Chakan Industrial Corridor, Pune<br>
          <strong>Proposed Scope:</strong> Complete 33-module operations suite managing Italian imports, Euro currency pricing, warehouse stock, and GST invoicing.
        </div>
      </div>

      <!-- Summary Box -->
      <div style="background:#f1f5f9; border:1.5px solid #cbd5e1; border-radius:6px; padding:9px 12px; font-size:8.8pt; line-height:1.42; color:#1e293b;">
        <strong>How to Review This Guide:</strong> Everything in this guide is written in plain, non-technical English. It details exactly what your customers will see on screen, how inquiries will reach your phone, and how your team will manage orders, godown stock, and money collections without errors once the system is built.
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
        <span class="section-title">Dalal Web Platform Scope &bull; Pages {i*2+1:02d} &amp; {i*2+2:02d} of 24 (To Be Engineered)</span>
        <span class="section-tag">Proposed Phase 1 Build</span>
      </div>

      {make_route_card(r1)}
      {make_route_card(r2)}
    </div>
    {make_footer(page_num)}
  </div>
"""

# PAGE 14: OMPI OPERATIONS SUITE OVERVIEW
html += f"""
  <div class="page">
    <div class="page-content">
      {make_header("SYSTEM 2: OMPI INDUSTRIAL OPERATIONS SUITE &bull; PROPOSED SCOPE")}

      <div class="section-header">
        <span class="section-title">OMPI Management Suite Overview &bull; The 4 Business Engines to be Built</span>
        <span class="section-tag">Proposed Operations Suite</span>
      </div>

      <div style="background:#ffffff; border:1.5px solid #cbd5e1; border-radius:6px; padding:10px 12px; margin-bottom:10px;">
        <div style="font-size:9.5pt; font-weight:800; color:#0f172a; text-transform:uppercase; margin-bottom:4px; border-bottom:1.5px solid #f1f5f9; padding-bottom:3px;">
          What the OMPI Management System Will Do for Your Company
        </div>
        <p style="font-size:9.0pt; line-height:1.44; color:#334155; margin-bottom:8px;">
          While Dalal Machine Tools will act as your <strong>public digital showroom</strong> that attracts factory owners, OMPI India will operate as your <strong>internal business management system</strong>. It will organize everything that happens after an inquiry arrives: quoting prices, sizing clutches, placing orders with Italy, tracking sea shipments, managing godown stock, and collecting customer payments.
        </p>

        <!-- 4 Engines Grid -->
        <div style="display:grid; grid-template-columns:1fr 1fr; gap:9px;">
          <div style="background:#f8fafc; border:1px solid #cbd5e1; border-radius:5px; padding:8px 10px;">
            <div style="font-size:8.6pt; font-weight:800; color:#0f172a; text-transform:uppercase; margin-bottom:3px;">
              Engine 1: Sales &amp; Customer Quotes (10 Tools)
            </div>
            <p style="font-size:8.5pt; line-height:1.38; color:#475569;">
              Will store client GST records, size the right clutch, generate official PDF proposals in 60 seconds, and track deals from new inquiry to advance payment.
            </p>
          </div>
          <div style="background:#f8fafc; border:1px solid #cbd5e1; border-radius:5px; padding:8px 10px;">
            <div style="font-size:8.6pt; font-weight:800; color:#0f172a; text-transform:uppercase; margin-bottom:3px;">
              Engine 2: Italy Purchase &amp; Import Cost (7 Tools)
            </div>
            <p style="font-size:8.5pt; line-height:1.38; color:#475569;">
              Will create Euro purchase orders for OMPI Italy, calculate total landed customs duty in Rupees, and track sea containers from Genoa to Nhava Sheva.
            </p>
          </div>
          <div style="background:#f8fafc; border:1px solid #cbd5e1; border-radius:5px; padding:8px 10px;">
            <div style="font-size:8.6pt; font-weight:800; color:#0f172a; text-transform:uppercase; margin-bottom:3px;">
              Engine 3: Godown Stock &amp; Spare Parts (8 Tools)
            </div>
            <p style="font-size:8.5pt; line-height:1.38; color:#475569;">
              Will show live godown stock in Pune and Chakan, track high-wear brake friction pads, record serial numbers, and create truck delivery passes.
            </p>
          </div>
          <div style="background:#f8fafc; border:1px solid #cbd5e1; border-radius:5px; padding:8px 10px;">
            <div style="font-size:8.6pt; font-weight:800; color:#0f172a; text-transform:uppercase; margin-bottom:3px;">
              Engine 4: Bills, GST Taxes, Money &amp; Safety (8 Tools)
            </div>
            <p style="font-size:8.5pt; line-height:1.38; color:#475569;">
              Will generate official GST bills, export GSTR-1 for your accountant in 1 click, track customer balance payments, and save automatic daily backups.
            </p>
          </div>
        </div>
      </div>

      <!-- Phasing & Development Roadmap Statement -->
      <div style="background:#fffbeb; border:1.5px solid #f59e0b; border-radius:6px; padding:10px 12px; margin-bottom:10px;">
        <div style="font-size:9.0pt; font-weight:800; color:#78350f; text-transform:uppercase; margin-bottom:3px;">
          Proposed Phased Delivery Roadmap (Upon Project Commencement)
        </div>
        <p style="font-size:8.6pt; line-height:1.42; color:#92400e;">
          <strong>Phase 1 Delivery Scope:</strong> The 24 public website pages, staff inquiry inbox, 60-second PDF proposal generator, and stock tracking tools will be engineered and launched first.<br>
          <strong>Phase 2 Delivery Scope:</strong> In-depth ERP tools (Euro purchase orders, multi-level parts breakdown, laser serial tracking, and GSTR-1 export) will be delivered across 7 monthly sprints as agreed in the Master SOW contract.
        </p>
      </div>

      <!-- Security Notice -->
      <div style="background:#f1f5f9; border:1.5px solid #cbd5e1; border-radius:6px; padding:8px 12px; font-size:8.6pt; line-height:1.4; color:#334155;">
        <strong>Data Safety Standard to be Built:</strong> All company inquiries, customer phone numbers, supplier costs, and pricing records will be password-protected. Staff members will only see what their job requires, and complete backups will be automatically saved every night.
      </div>
    </div>
    {make_footer(14)}
  </div>
"""

# PAGES 15 TO 30: OMPI MODULES 01 TO 32 (2 PER PAGE = 16 PAGES)
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

      {make_module_card(m1)}
      {make_module_card(m2)}
    </div>
    {make_footer(page_num)}
  </div>
"""

# PAGE 31: MODULE 33 (OWNER DASHBOARD) + ADMIN CONSOLES
m33 = ompi_modules[32]
html += f"""
  <div class="page">
    <div class="page-content">
      {make_header("SYSTEM 2: EXECUTIVE MANAGEMENT &amp; CONTROL CONSOLES &bull; PROPOSED SCOPE")}
      
      <div class="section-header">
        <span class="section-title">OMPI Management Engine &bull; Module 33 of 33 &amp; Control Desks (To Be Engineered)</span>
        <span class="section-tag">Executive Business Control</span>
      </div>

      {make_module_card(m33)}

      <!-- Operations Consoles Summary Box -->
      <div class="card-box" style="margin-top:4px;">
        <div class="card-header">
          <div>
            <span class="badge-id">PORTALS</span>
            <span class="card-title">Staff Operations &amp; Director Control Consoles (To Be Built)</span>
            <span class="card-status">&#9675; TO BE BUILT: MANAGEMENT DESKS</span>
          </div>
          <div class="card-path">Planned Portals: /admin &bull; /superadmin</div>
        </div>
        <div class="simple-grid" style="margin-top:5px;">
          <div>
            <div class="grid-label">Planned Staff Operations Desk (/admin)</div>
            <div class="grid-text">
              Where your sales team will manage customer RFQs, view inquiry details, send pre-filled WhatsApp quotes, and update machine availability without touching code.
            </div>
          </div>
          <div>
            <div class="grid-label">Planned Managing Director Console (/superadmin)</div>
            <div class="grid-text">
              Will give the business owner total control over staff passwords, user permissions, company contact settings, and complete unalterable business history logs.
            </div>
          </div>
        </div>
        <div class="feature-strip">
          <strong>Security Guarantee to be Built:</strong> Both administrative consoles will be completely cloaked from the public web with secure secret passkeys, ensuring zero unauthorized access.
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
      <div style="background:#ffffff; border:1.5px solid #cbd5e1; border-radius:6px; padding:9px 12px; margin-bottom:10px;">
        <div style="font-size:9.2pt; font-weight:800; color:#0f172a; text-transform:uppercase; margin-bottom:6px; border-bottom:1.5px solid #f1f5f9; padding-bottom:3px;">
          The Seamless 6-Step Business Process to be Engineered (Inquiry to Payment)
        </div>
        <div style="display:grid; grid-template-columns:1fr 1fr; gap:9px; font-size:8.5pt; line-height:1.38; color:#334155;">
          <div style="background:#f8fafc; padding:7px 9px; border-radius:4px; border-left:3.5px solid #d97706;">
            <strong>Step 1: Customer Inquires Online</strong><br>
            A plant head finds a 1,600T press on the website and clicks the WhatsApp inquiry button with his company details.
          </div>
          <div style="background:#f8fafc; padding:7px 9px; border-radius:4px; border-left:3.5px solid #d97706;">
            <strong>Step 2: Instant Technical Sizing</strong><br>
            The system automatically matches the press with the exact Italian OMPI pneumatic clutch required for the job.
          </div>
          <div style="background:#f8fafc; padding:7px 9px; border-radius:4px; border-left:3.5px solid #d97706;">
            <strong>Step 3: 60-Second Quotation Sent</strong><br>
            An official proposal PDF with machine photos, specs, and price is sent directly to the customer's WhatsApp.
          </div>
          <div style="background:#f8fafc; padding:7px 9px; border-radius:4px; border-left:3.5px solid #d97706;">
            <strong>Step 4: Machine Locked in Godown</strong><br>
            Once the client confirms, the press is marked 'Under Commercial Hold' so it cannot be sold to anyone else.
          </div>
          <div style="background:#f8fafc; padding:7px 9px; border-radius:4px; border-left:3.5px solid #d97706;">
            <strong>Step 5: Pune Workshop Overhaul &amp; Rigging</strong><br>
            The machine undergoes live power trials, foundation check, and is dispatched on low-bed trailers to the buyer's factory.
          </div>
          <div style="background:#f8fafc; padding:7px 9px; border-radius:4px; border-left:3.5px solid #d97706;">
            <strong>Step 6: Official GST Invoicing &amp; Backup</strong><br>
            Clean tax bills are issued, GST records are updated for your accountant, and all transaction history is securely saved.
          </div>
        </div>
      </div>

      <!-- Implementation Summary & Phasing Table -->
      <div style="background:#f8fafc; border:1.5px solid #cbd5e1; border-radius:6px; padding:9px 12px; margin-bottom:10px;">
        <div style="font-size:8.8pt; font-weight:800; color:#0f172a; text-transform:uppercase; margin-bottom:4px;">
          Commercial Phasing &amp; Proposed Delivery Milestones
        </div>
        <table style="width:100%; border-collapse:collapse; font-size:8.3pt; line-height:1.35; color:#334155;">
          <thead>
            <tr style="background:#0f172a; color:#ffffff; text-align:left;">
              <th style="padding:4px 7px;">Milestone Phase</th>
              <th style="padding:4px 7px;">Proposed Scope of Delivery</th>
              <th style="padding:4px 7px;">Status</th>
            </tr>
          </thead>
          <tbody>
            <tr style="border-bottom:1px solid #e2e8f0; background:#ffffff;">
              <td style="padding:4px 7px; font-weight:700;">Phase 1 (Kickoff Scope)</td>
              <td style="padding:4px 7px;">Dalal 24 Public Pages &bull; Staff Admin Portal &bull; Director Console &bull; Core Quoting Tools</td>
              <td style="padding:4px 7px; font-weight:700; color:#b45309;">TO COMMENCE UPON SIGN-OFF</td>
            </tr>
            <tr style="border-bottom:1px solid #e2e8f0; background:#ffffff;">
              <td style="padding:4px 7px; font-weight:700;">Phase 2 (ERP Rollout)</td>
              <td style="padding:4px 7px;">OMPI Standalone ERP Modules (7 Monthly Sprints: Customer 360, Italy POs, BOM, Godown Bins, GSTR-1)</td>
              <td style="padding:4px 7px; font-weight:700; color:#64748b;">SCHEDULED SPRINT ROADMAP</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Non-Disclosure Confirmation & Executive Sign-Off -->
      <div style="border:1.5px solid #e11d48; background:#fff1f2; border-radius:6px; padding:9px 12px; margin-bottom:9px;">
        <div style="font-size:8.6pt; font-weight:800; color:#9f1239; text-transform:uppercase; margin-bottom:2px;">
          &#128274; Confidentiality &amp; Pre-Commencement Approval Acknowledgment
        </div>
        <p style="font-size:8.2pt; line-height:1.38; color:#4c0519;">
          This master specification represents the proprietary intellectual property and proposed operational architecture of Dalal Machine Tools Agency Pvt. Ltd. and OMPI India LLP. Work has not commenced. External sharing, copying, or forwarding without written authorization is strictly forbidden.
        </p>
      </div>

      <!-- Signatures Grid -->
      <div style="display:grid; grid-template-columns:1fr 1fr; gap:12px; border-top:1.5px solid #0f172a; padding-top:7px;">
        <div style="font-size:8.4pt; line-height:1.35; color:#334155;">
          <strong>Accepted &amp; Approved to Commence Work:</strong><br><br>
          __________________________________________<br>
          <strong>Mr. Vinit Dalal</strong> &bull; Managing Director / Partner
        </div>
        <div style="font-size:8.4pt; line-height:1.35; color:#334155; text-align:right;">
          <strong>Submitted by Principal Software Consultant:</strong><br><br>
          __________________________________________<br>
          <strong>Suyash Shinde</strong> &bull; Pimpri, Pune, Maharashtra
        </div>
      </div>
    </div>
    {make_footer(32)}
  </div>
</body>
</html>
"""

# Write HTML file
output_html = "DALAL_AND_OMPI_57_PAGES_AND_MODULES_MASTER_SPECIFICATION.html"
with open(output_html, "w", encoding="utf-8") as f:
    f.write(html)
print(f"Generated HTML: {output_html} ({os.path.getsize(output_html):,} bytes)")

# Write copy to dedicated clean filename
simple_html = "DALAL_AND_OMPI_57_EXECUTIVE_CLIENT_GUIDE_SIMPLE.html"
with open(simple_html, "w", encoding="utf-8") as f:
    f.write(html)
print(f"Saved copy to: {simple_html}")

# Render to PDF using Edge Headless
edge = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
pdf_path = os.path.abspath('DALAL_AND_OMPI_57_PAGES_AND_MODULES_MASTER_SPECIFICATION.pdf')
simple_pdf_path = os.path.abspath('DALAL_AND_OMPI_57_EXECUTIVE_CLIENT_GUIDE_SIMPLE.pdf')
url = f'file:///{os.path.abspath(output_html).replace("\\", "/")}'

cmd = [
    edge,
    '--headless',
    '--disable-gpu',
    f'--print-to-pdf={pdf_path}',
    '--no-pdf-header-footer',
    url
]
print(f"Rendering PDF via Edge: {pdf_path}...")
res = subprocess.run(cmd, capture_output=True, text=True)

if os.path.exists(pdf_path):
    sz = os.path.getsize(pdf_path)
    print(f"PDF Successfully Generated: {pdf_path} ({sz / 1024:.1f} KB)")
    
    # Copy to simple_pdf_path
    shutil.copyfile(pdf_path, simple_pdf_path)
    print(f"Saved copy to: {simple_pdf_path}")
    
    # Copy to artifact directory
    artifact_dir = r'C:\Users\91940\.gemini\antigravity\brain\75a30f5c-ccbc-43b7-9b59-6c8c1ab99b62'
    dst1 = os.path.join(artifact_dir, 'DALAL_AND_OMPI_57_PAGES_AND_MODULES_MASTER_SPECIFICATION.pdf')
    dst2 = os.path.join(artifact_dir, 'DALAL_AND_OMPI_57_EXECUTIVE_CLIENT_GUIDE_SIMPLE.pdf')
    dst_html = os.path.join(artifact_dir, 'DALAL_AND_OMPI_57_EXECUTIVE_CLIENT_GUIDE_SIMPLE.html')
    
    shutil.copyfile(pdf_path, dst1)
    shutil.copyfile(pdf_path, dst2)
    shutil.copyfile(simple_html, dst_html)
    print(f"Copied all files to artifact directory: {artifact_dir}")
else:
    print("PDF Generation failed!")
    print("Stderr:", res.stderr)

