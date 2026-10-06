# Dalal Machines - Modern Industrial UI Redesign Project
> Re-engineering [Dalal Machine Tools Agency Pvt. Ltd.](https://www.dalalmachines.com/) with the elite UI/UX of the ThemeForest **Machinery – Factory & Industrial Business** template.

---

## 📌 Executive Summary & Audit Overview

Following an exhaustive audit of all 17 accessible pages, 26 machinery categories (16 Metal Forming, 10 Metal Cutting), 49 catalogued machines, and the dated logistics shipment archive of **Dalal Machine Tools Agency Pvt. Ltd.** (Led by Mr. Vinit Dalal, Managing Director, Commerce Centre, Tardeo, Mumbai), this repository provides:

1. **8 Core Production HTML/CSS Templates** replicating the modern industrial aesthetic of ThemeForest Item #22422413 (*Machinery – Factory & Industrial Business*).
2. **Prominent Top-Right Integration** for technical partner **[OMPI India LLP](https://www.ompiindia.com/) – Clutch & Brake Units** across all headers, top-bars, and machine detail pages.
3. **Comprehensive 8 Real Photographic Assets** depicting actual forging presses, CNC boring machines, multi-axle port transport trailers, warehouse storage yards in Pune, and OMPI pneumatic clutch & brake units (no generic placeholders).
4. **Advanced Typography & Kinetic Text Animations** utilizing Google Fonts (*Barlow*, *Inter*, *Rajdhani*), hero title cross-fade reveals, animated KPI count-ups, and interactive High Seas Sales savings calculator.
5. **Comprehensive 6-Part Architectural `.md` Documentation Suite** addressing all 15 defects identified in the legacy site audit.

---

## 🚀 The 8 Core Production HTML Templates

| Template File | Page Type & URL Pattern | Purpose & Key Features Included |
|---|---|---|
| [`index.html`](file:///d:/Experiment/index.html) | **Homepage** (`/`) | Industrial Hero Carousel, Overlapping 4-Pillar Features (Europe Stock, Power Test, High Seas INR, Port-to-Door Delivery), 20+ Years KPI counters, Services Grid, Featured Machines, High Seas Comparison Table, and top-right **OMPI India LLP** link. |
| [`about.html`](file:///d:/Experiment/about.html) | **About Us** (`/about`) | Detailed company profile, 20+ years legacy, Managing Director profile of Mr. Vinit Dalal, global sourcing network map (Germany, Russia, Thailand, Poland, Pune), and customer assurance credentials. |
| [`services.html`](file:///d:/Experiment/services.html) | **Turnkey Services & Import** (`/services`) | The 6 Pillars of machinery import, European live power inspection breakdown, port logistics clearance, and an **interactive High Seas Sales INR / GST savings calculator**. |
| [`category.html`](file:///d:/Experiment/category.html) | **Category & Sidebar Grid** (`/metal-forming-machinery`, `/metal-cutting-machinery`, `/[category-slug]`) | 2-column layout with 280px sticky sidebar containing all **16 Metal Forming** & **10 Metal Cutting** categories, location filters (Pune, Europe, Thailand, Vietnam), sort dropdown, and machine cards with real photography. |
| [`product.html`](file:///d:/Experiment/product.html) | **Individual Machine PDP** (`/[product-slug]`, e.g. `/li-chin-200-ton`) | 4-level breadcrumb, high-res gallery with interactive thumbnail switcher, standardized meta-data grid (Make, Model, Machine No, Year, Location), bulleted technical specification list, embedded RFQ form, and OMPI India partner card. |
| [`gallery.html`](file:///d:/Experiment/gallery.html) | **Logistics & Sourcing Archive** (`/pages/gallery/index/15` ... `/120`) | Chronological photographic log of real machine shipments (July 2026 National 1000T in Thailand, June 2026 Russian Knuckle Joint for Jamshedpur, March 2026 Komatsu in Poland, Nhava Sheva Port crane offloading, etc.) with route tags and 9-page pagination. |
| [`contact.html`](file:///d:/Experiment/contact.html) | **Contact & Registered Office** (`/pages/contact`) | Zero PHP warnings! Registered office card (Commerce Centre, Tardeo, Mumbai), Mr. Vinit Dalal MD card, phones, direct emails, embedded Google Map, and validated WhatsApp inquiry form. |
| [`404.html`](file:///d:/Experiment/404.html) | **Industrial Error Page** (`/404.html`) | Professional industrial error page resolving old dead links (`/pages/usedmachine/view/54`, `/tos2.html`), with quick recovery links back to Forming and Cutting categories. |

---

## 📸 Photorealistic Imagery Assets (`assets/images/`)

| File Name | Description & Visual Subject |
|---|---|
| `hero_forging_press.jpg` | Heavy-duty 2,500 Ton Voronezh hot forging mechanical press in operation |
| `cnc_boring_machine.jpg` | TOS Varnsdorf horizontal boring and milling machine with revolving table |
| `logistics_heavy_transport.jpg` | Multi-axle modular hydraulic heavy-haul trailer carrying heavy industrial machinery |
| `cframe_press_pune.jpg` | 200 Ton C-Frame mechanical stamping press in Pune warehouse |
| `knuckle_coining_press.jpg` | 1,000 Ton Knuckle Joint coining and sizing press |
| `ompi_clutch_brake_unit.jpg` | Combined pneumatic clutch & brake unit for OMPI India LLP |
| `pune_warehouse_yard.jpg` | Spacious industrial machine stock warehouse in Pune with overhead gantry crane |
| `port_crane_logistics.jpg` | Container quay cranes offloading heavy machine crates at Nhava Sheva JNPT port |

---

## 🔗 Technical Partner Integration: OMPI India LLP

As instructed, a prominent link for **OMPI India LLP** has been integrated on the **top-right side** of the website header and top utility bar:

- **Target URL**: [https://www.ompiindia.com/](https://www.ompiindia.com/)
- **Display Wording**: `OMPI India LLP – Clutch & Brake Units`
- **Visual Design**: High-contrast amber badge (`ASSOCIATE`) + gold border pill with external link icon, ensuring visiting industrial buyers immediately recognize OMPI India LLP's role in supplying premium press Clutch & Brake units.
- **Placement**:
  1. Top-Right of the 44px Utility Top-Bar on every page.
  2. Top-Right of the Sticky Header right alongside the "Request a Quote" CTA button.
  3. Contextual cross-promotion on press Product Detail Pages (`product.html`) and the Contact page (`contact.html`).

---

## 🗂 Architectural Documentation Suite Index

| File | Document Name | Purpose & Content |
|---|---|---|
| [`01_DESIGN_SYSTEM.md`](file:///d:/Experiment/01_DESIGN_SYSTEM.md) | **Design System & UI Guidelines** | Industrial color palette (Safety Amber `#FFB400`, Deep Charcoal `#141B22`, Slate Gray), Google Fonts (*Barlow*, *Inter*, *Rajdhani*), keyframe animations, chamfered buttons, badges (*Seen Under Power*, *Europe Stock*), and responsive breakpoints. |
| [`02_INFORMATION_ARCHITECTURE.md`](file:///d:/Experiment/02_INFORMATION_ARCHITECTURE.md) | **Information Architecture & Sitemap** | Full 4-level navigation hierarchy, 26 category routing matrix, and a 301 redirection table resolving duplicate and broken legacy URLs. |
| [`03_COMPONENT_SPECIFICATIONS.md`](file:///d:/Experiment/03_COMPONENT_SPECIFICATIONS.md) | **UI Component Specifications** | Detailed technical breakdown of Topbar with OMPI link, Mega Menu, Hero Slider, KPI Counters, Machine Cards, 6-Step Import Chain, and WhatsApp RFQ modal. |
| [`04_MACHINE_CATALOG_DATA.md`](file:///d:/Experiment/04_MACHINE_CATALOG_DATA.md) | **Machine Catalog & Data Schema** | Standardized data model fixing legacy schema flaws: unique Machine IDs (P00031, P00007), standardized Make vs Manufacturer, Year, Location, and detailed specs. |
| [`05_PAGE_TEMPLATES_WIREFRAMES.md`](file:///d:/Experiment/05_PAGE_TEMPLATES_WIREFRAMES.md) | **Page Layouts & Wireframes** | Section-by-section DOM wireframes for all page templates including the left sidebar category filter and PDP spec dossier. |
| [`06_IMPLEMENTATION_PLAN.md`](file:///d:/Experiment/06_IMPLEMENTATION_PLAN.md) | **Step-by-Step Implementation Plan** | Production execution plan from frontend structure to dynamic PHP/CMS integration and SEO schema deployment. |

---

## 🛠 Asset Architecture

```
d:/Experiment/
├── assets/
│   ├── css/
│   │   └── style.css                   /* Design system, animations, Barlow/Inter typography, responsive queries */
│   ├── js/
│   │   └── main.js                     /* Carousel, catalog filtering, KPI counter, RFQ, High Seas calculator */
│   └── images/
│       ├── cframe_press_pune.jpg       /* Real 200T C-frame press */
│       ├── cnc_boring_machine.jpg      /* Real TOS horizontal boring machine */
│       ├── hero_forging_press.jpg      /* Real 2500T hot forging press */
│       ├── knuckle_coining_press.jpg   /* Real 1000T knuckle joint coining press */
│       ├── logistics_heavy_transport.jpg/* Real multi-axle trailer transport */
│       ├── ompi_clutch_brake_unit.jpg  /* Real OMPI pneumatic clutch & brake */
│       ├── port_crane_logistics.jpg    /* Real Nhava Sheva port crane unloading */
│       └── pune_warehouse_yard.jpg     /* Real Pune machine warehouse yard */
├── index.html                          /* 1. Master Homepage */
├── about.html                          /* 2. Company Profile & Legacy */
├── services.html                       /* 3. Turnkey Import & High Seas Savings Calculator */
├── category.html                       /* 4. Category Sidebar Filter + Machine Grid */
├── product.html                        /* 5. Product Detail Spec Dossier (PDP) */
├── gallery.html                        /* 6. Logistics & Sourcing Photo Log */
├── contact.html                        /* 7. Mumbai Office & Error-Free Form */
├── 404.html                            /* 8. Professional 404 Error Page */
├── 01_DESIGN_SYSTEM.md
├── 02_INFORMATION_ARCHITECTURE.md
├── 03_COMPONENT_SPECIFICATIONS.md
├── 04_MACHINE_CATALOG_DATA.md
├── 05_PAGE_TEMPLATES_WIREFRAMES.md
├── 06_IMPLEMENTATION_PLAN.md
└── README.md
```
