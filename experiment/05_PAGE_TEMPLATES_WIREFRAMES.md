# 05 - Page Layout Templates & Wireframes

> Detailed structural wireframes and HTML layout templates for all primary pages of the **Dalal Machine Tools Agency Pvt. Ltd.** website, engineered according to the ThemeForest **Machinery** template design patterns.

---

## 🖥 1. Homepage Template (`index.html`)

### Structural Layout Architecture

```
+-----------------------------------------------------------------------------------+
| 1. TOP UTILITY BAR: Phone | Email | WhatsApp | Mumbai Office Address | Hours     |
+-----------------------------------------------------------------------------------+
| 2. MAIN HEADER: Logo + Brand Tagline | Mega Menu Navigation | [REQUEST A QUOTE]   |
+-----------------------------------------------------------------------------------+
| 3. HERO SLIDER (Industrial Background + Bold Typography + Dual CTAs + Badges)     |
+-----------------------------------------------------------------------------------+
| 4. FEATURE STRIP (Overlapping 4 Cards: Stock Abroad, Power Test, High Seas, CIF) |
+-----------------------------------------------------------------------------------+
| 5. ABOUT COMPANY SECTION (2-Col: Left Image Collage / Right Story + 4 KPI Counters)|
+-----------------------------------------------------------------------------------+
| 6. CORE SERVICES GRID (6 Cards: Sourcing, Inspection, High Seas, CIF, Port, Door) |
+-----------------------------------------------------------------------------------+
| 7. FILTERABLE MACHINE CATALOG (Tabs: Forming, Cutting, Heavy Presses | 6 Cards)   |
+-----------------------------------------------------------------------------------+
| 8. HIGH SEAS SALES EXPLAINER (Comparison Matrix: Dalal High Seas vs. Direct Import)|
+-----------------------------------------------------------------------------------+
| 9. INSPECTION GUARANTEE BANNER ("Seen Under Power with Foundation Drawings")      |
+-----------------------------------------------------------------------------------+
| 10. CLIENT CASE STUDIES / PAST DELIVERY MILESTONES (Automotive, Defense, Forging)  |
+-----------------------------------------------------------------------------------+
| 11. INDUSTRIAL RFQ FORM SECTION (Machine Type, Tonnage, Company, Contact, City)   |
+-----------------------------------------------------------------------------------+
| 12. FOOTER (Company Bio, Quick Links, Categories, Mumbai Card, Google Map Link)   |
+-----------------------------------------------------------------------------------+
```

---

## 📋 2. Used Machinery Catalog Template (`used-machines.html`)

### Faceted Sidebar & Grid Wireframe

```
+-----------------------------------------------------------------------------------+
| PAGE BANNER: "USED METAL FORMING & CUTTING MACHINERY" | Breadcrumb: Home > Catalog|
+-----------------------------------------------------------------------------------+
| [ SIDEBAR: 300px ]                    | [ MAIN CONTENT AREA: Flexible Grid ]      |
|                                       |                                           |
| 1. Search by Keyword [Input]          | Header: Showing 1-12 of 48 Machines       |
|                                       | Sort By: [ Tonnage: High to Low ▾ ]       |
| 2. Machinery Category (Checkbox list) | Active Filter Badges: [Hot Forging x]     |
|    [x] Hot Forging Presses            |-------------------------------------------|
|    [ ] Knuckle Joint Presses          | [MACHINE CARD 1]  [MACHINE CARD 2]        |
|    [ ] Horizontal Boring              | Voronezh 2500T    TOS W100A Boring        |
|    [ ] Machining Centres (VMC)        | European Stock    Under Power             |
|                                       | Specs: 2500T/350  Specs: 100mm Spindle    |
| 3. Tonnage Range Slider               | [Specs] [Inquire] [Specs] [Inquire]       |
|    [=====●=============] 500T - 6300T |-------------------------------------------|
|                                       | [MACHINE CARD 3]  [MACHINE CARD 4]        |
| 4. Inspection Status                  | Kalinin 1000T     Sedin 1525 VTL          |
|    [x] Seen Under Power               | Knuckle Joint     2500mm Swing            |
|    [ ] Drawings Available             | [Specs] [Inquire] [Specs] [Inquire]       |
|                                       |-------------------------------------------|
| 5. Location                           | PAGINATION: [ < Prev ] [ 1 ] [ 2 ] [ Next >]|
|    [x] European Warehouse             |                                           |
|    [ ] Transit / High Seas            |                                           |
+-----------------------------------------------------------------------------------+
```

---

## 🔍 3. Single Machine Detail View (`machine-detail.html`)

### Detailed Engineering View

```
+-----------------------------------------------------------------------------------+
| BREADCRUMB: Home > Used Machines > Metal Forming > Voronezh K8542 1600 Ton        |
+-----------------------------------------------------------------------------------+
| [ LEFT: MEDIA & VIDEO (60%) ]           | [ RIGHT: COMMERCIAL & SPECS (40%) ]     |
|                                         |                                         |
| +-------------------------------------+ | # VORONEZH K8542 1600 TON               |
| | MAIN HI-RES PRODUCT VIEWER          | | Heavy Hot Forging Crank Press           |
| | (Zoom on hover, full screen)        | |                                         |
| +-------------------------------------+ | Badges: [1,600 TON] [SEEN UNDER POWER]  |
|                                         |                                         |
| [Thumb 1] [Thumb 2] [Thumb 3] [Drawing] | KEY PARAMETERS QUICK BOX:               |
|                                         | - Nominal Force: 1600 Ton (16000 kN)    |
| [ ▶ VIDEO: TEST RUN UNDER POWER ]       | - Stroke of Slide: 300 mm               |
| Live recording at European facility     | - Shut Height: 750 mm                   |
| showing clutch engagement and ram cycle | - Bed Dimensions: 1200 x 1200 mm        |
|                                         | - Location: Ready Stock, Europe         |
|                                         |                                         |
|                                         | [ REQUEST INSTANT PRICE QUOTATION ]     |
|                                         | [ CHAT ON WHATSAPP (+91 9821232131) ]   |
|                                         | [ DOWNLOAD FOUNDATION DRAWING (PDF) ]   |
+-----------------------------------------------------------------------------------+
| TABBED SPECIFICATION DOSSIER:                                                     |
| [ Tab 1: Detailed Specifications ] [ Tab 2: Foundation & GA ] [ Tab 3: Terms ]    |
|-----------------------------------------------------------------------------------|
| Parameter                       | Specification Value                             |
|---------------------------------|-------------------------------------------------|
| Manufacturer / Make             | Voronezh Heavy Press Plant (TMP, Russia)        |
| Model                           | K8542                                           |
| Year of Construction            | 1988                                            |
| Number of Continuous Strokes    | 85 / min                                        |
| Adjustment of Slide             | 15 mm                                           |
| Upper / Lower Ejector Stroke    | Upper: 50 mm / Lower: 140 mm                    |
| Main Electric Motor Power       | 90 kW, 1480 RPM                                 |
| Overall Dimensions (L x W x H)  | 3,850 mm x 3,100 mm x 6,450 mm                  |
| Total Weight of Machine         | Approx. 85,000 kg (85 Metric Tons)              |
+-----------------------------------------------------------------------------------+
| HIGH SEAS PURCHASE BENEFITS FOR THIS MACHINE:                                     |
| * Purchase directly in Indian Rupees (INR)                                        |
| * Bill of Entry filed directly in your company name for full GST credit claim     |
| * Complete CIF shipping and Nhava Sheva customs cleared by Dalal Machines team   |
+-----------------------------------------------------------------------------------+
```

---

## 🛠 4. Services Page (`services.html`)

A 6-section deep dive detailing the six pillars of Dalal Machines' operation:
1. **Worldwide Sourcing Network**: Partnerships in Germany, Italy, Czech Republic, and Russia.
2. **On-Site Inspection Under Power**: Verifying machine kinematics, hydraulic pressure, ram parallelism, and electrical cabinets under live power.
3. **High Seas Sales Agreement**: Legally explaining how Indian manufacturers benefit from purchasing on High Seas terms (no FX exposure, GST input availability, complete customs documentation).
4. **CIF International Maritime Logistics**: Special vessel chartering, break-bulk cargo handling for presses up to 6,300 tons.
5. **Port Clearance at Nhava Sheva & Mumbai Port**: Expedited customs documentation, bill of entry issuance.
6. **Turnkey Heavy Transportation**: Multi-axle hydraulic trailers delivering directly to customer factory foundation pits.

---

## 📞 5. Contact & RFQ Center (`contact.html`)

### Layout
- **Left Column**: Registered Office details:
  - `Dalal Machine Tools Agency Pvt. Ltd.`
  - `C-10, 3rd Floor, Commerce Centre, 78, Tardeo Main Road, Mumbai - 400034, India`
  - Tel: `+91-22-67439873` / Mobile: `+91 9821232131`
  - Email: `dalalmachine@gmail.com`
  - Business Hours & Emergency Contact
- **Right Column**: Comprehensive Inquiry & RFQ Form:
  - Company Name & City / State
  - Contact Person & Designation
  - Phone / WhatsApp & Email
  - Machine Type of Interest (Dropdown populated from catalog)
  - Required Capacity / Tonnage & Target Stroke
  - Budget & Delivery Timeline Preference
  - Specific Requirement Details (Textarea)
- **Full Width Bottom**: Interactive Google Map centered on Commerce Centre, Tardeo, Mumbai.
