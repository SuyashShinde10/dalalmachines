# 04 - Machine Catalog & Technical Data Schema

> Comprehensive catalog data architecture for **Dalal Machine Tools Agency Pvt. Ltd.**, containing complete specification structures for all Metal Forming and Metal Cutting machinery lines.

---

## 🏗 1. Machine Data Model Schema (JSON Specification)

Each machine in the catalog follows a strict engineering data model to support faceted filtering, comparison, and quotation requests:

```json
{
  "id": "forming-001",
  "slug": "voronezh-k8542-1600-ton-hot-forging-press",
  "title": "Voronezh K8542 1600 Ton Hot Forging Press",
  "category": "metal-forming",
  "subCategory": "hot-forging-press",
  "make": "Voronezh (TMP)",
  "model": "K8542",
  "yearOfManufacture": 1988,
  "condition": "Excellent - Inspected Under Power",
  "location": "Warehouse, Europe",
  "availability": "Ready Stock - Immediate Dispatch",
  "primarySpecs": {
    "nominalForceTons": 1600,
    "nominalForceKn": 16000,
    "ramStrokeMm": 300,
    "strokesPerMinute": 85,
    "shutHeightMm": 750,
    "bedDimensionsMm": "1200 x 1200",
    "ramDimensionsMm": "1000 x 1000",
    "mainMotorPowerKw": 90,
    "totalWeightTons": 85
  },
  "features": [
    "Equipped with pneumatic clutch & brake unit",
    "Upper and lower ejector mechanisms installed",
    "Automatic centralized grease lubrication system",
    "Original Russian & English electrical and foundation manuals available"
  ],
  "verificationStatus": {
    "seenUnderPower": true,
    "foundationDrawingsAvailable": true,
    "serviceHistoryDocumented": true,
    "highSeasSalesEligible": true
  },
  "media": {
    "thumbnail": "assets/images/machines/voronezh-k8542-thumb.jpg",
    "gallery": [
      "assets/images/machines/voronezh-k8542-front.jpg",
      "assets/images/machines/voronezh-k8542-bed.jpg",
      "assets/images/machines/voronezh-k8542-motor.jpg",
      "assets/images/machines/voronezh-k8542-drawing.jpg"
    ],
    "videoInspectionUrl": "https://www.youtube.com/embed/inspection-demo-1"
  }
}
```

---

## 🔨 2. Metal Forming Machinery Categories & Featured Inventory

### Category 1: Hot Forging Presses
*High-tonnage mechanical crank and eccentric presses for automotive and aerospace forgings.*

| Model | Make | Capacity | Stroke | Shut Height | Bed Size | Status |
|---|---|---|---|---|---|---|
| **K8542** | Voronezh (TMP) | **1,600 Ton** | 300 mm | 750 mm | 1200 x 1200 mm | European Stock |
| **K8544** | Voronezh (TMP) | **2,500 Ton** | 350 mm | 850 mm | 1400 x 1400 mm | Under Power |
| **K8546** | Voronezh (TMP) | **4,000 Ton** | 400 mm | 1000 mm | 1650 x 1650 mm | Ready Europe |
| **LZK-2500** | SMERAL Trnava | **2,500 Ton** | 320 mm | 820 mm | 1340 x 1400 mm | European Stock |
| **Maxipres 4000** | National Machinery | **4,000 Ton** | 380 mm | 950 mm | 1600 x 1600 mm | High Seas |
| **SP 6300** | Eumuco | **6,300 Ton** | 450 mm | 1150 mm | 1900 x 1900 mm | On Request |

---

### Category 2: Knuckle Joint Presses
*Precision cold & warm coining, sizing, and heading machines with high bottom dead-center dwelling force.*

| Model | Make | Tonnage | Stroke | SPM | Bed Size | Notes |
|---|---|---|---|---|---|---|
| **KB8338** | Kalinin / Russia | **630 Ton** | 130 mm | 50 | 710 x 710 mm | Heavy coining |
| **KB8340** | Kalinin / Russia | **1,000 Ton** | 150 mm | 40 | 800 x 800 mm | Under power |
| **K8342** | Voronezh | **1,600 Ton** | 170 mm | 32 | 1000 x 1000 mm | European stock |
| **Maypres OKN 320** | Maypres | **320 Ton** | 60 mm | 60 | 600 x 600 mm | Precision sizing |

---

### Category 3: Pneumatic & Counterblow Forging Hammers
*High kinetic energy hammers for open-die and closed-die forging of complex steel alloys.*

| Model | Make | Tup Weight / Energy | Blows/Min | Table Dimensions | Drive |
|---|---|---|---|---|---|
| **L-12** | Banning | **2,500 kg Tup** | 90 bpm | 1100 x 900 mm | Pneumatic |
| **DG-20** | Beche | **200 kJ Energy** | Counterblow | 1400 x 1200 mm | Steam/Air |
| **KH-40** | Lasco | **4,000 kg Tup** | 80 bpm | 1300 x 1000 mm | Hydraulic Drop |

---

### Category 4: Friction Screw Presses
| Model | Make | Force (kN) | Screw Dia | Stroke | Daylight |
|---|---|---|---|---|---|
| **F-1736** | Kalinin | **4,000 kN (400T)** | 220 mm | 450 mm | 750 mm |
| **F-1738** | Kalinin | **6,300 kN (630T)** | 280 mm | 500 mm | 850 mm |
| **Osterwalder 1000** | Osterwalder | **10,000 kN (1000T)** | 360 mm | 600 mm | 1050 mm |

---

### Additional Forming Lines Represented:
- **Mechanical Sheet Metal Presses**: Single action & double action crank presses (Aida, Komatsu, Erfurt).
- **Hydraulic Deep Drawing Presses**: 500T to 5,000T (Siempelkamp, Schuler, Pagnoni).
- **Trimming Presses**: Dedicated crank trimming & punch presses (SMERAL, Kalinin).
- **Cold Forging Presses & Forging Rolls**: High-speed pre-forming rolls (Eumuco Reduroll).
- **Horizontal Forging Upsetters**: 2" to 7" bar upsetting machines (National, Ajax).
- **Open Die Forging Presses & Manipulators**: Hydraulic free-forging column presses up to 5,000T paired with 10-ton to 40-ton rail-bound or mobile forging manipulators (Dango & Dienenthal, Glama).

---

## ⚙️ 3. Metal Cutting Machinery Categories & Inventory

### Category 1: Horizontal Boring & Milling Machines (HBM)
*Heavy-duty spindle boring machines for large engine blocks, turbine housings, and fabrications.*

| Machine Name | Make | Spindle Dia | X-Travel | Y-Travel | Table Size | Spindle Speed |
|---|---|---|---|---|---|---|
| **Tos W9A** | TOS Varnsdorf | **90 mm** | 1250 mm | 1000 mm | 1000 x 1120 mm | 1400 RPM |
| **Tos W100A** | TOS Varnsdorf | **100 mm** | 1600 mm | 1120 mm | 1250 x 1250 mm | 1120 RPM |
| **Skoda W160 HC** | Skoda | **160 mm** | 3000 mm | 2000 mm | Floor plate type | Heavy duty |
| **Pama Speedram 2** | Pama | **160 mm** | 6000 mm | 3000 mm | CNC Hydrostatic | CNC retrofit |

---

### Category 2: Vertical Turning Lathes (VTL / Boring Mills)
| Machine Model | Make | Table Diameter | Max Swing | Max Height | Max Workpiece Wt |
|---|---|---|---|---|---|
| **1516 (1L532)** | Sedin / Russia | **1,400 mm** | 1,600 mm | 1,000 mm | 8,000 kg |
| **1525** | Sedin / Russia | **2,250 mm** | 2,500 mm | 1,600 mm | 16,000 kg |
| **Dorries VCE 280** | Dorries Scharmann | **2,800 mm** | 3,200 mm | 2,000 mm | 25,000 kg (CNC) |
| **Titan SC 33** | Titan Romania | **3,000 mm** | 3,300 mm | 2,200 mm | 30,000 kg |

---

### Category 3: Machining Centres (VMC & HMC) & Gear Cutting
- **Vertical Machining Centres (VMC)**: 3-axis to 5-axis heavy duty box-way centers (Mazak VTC, Doosan Mynx, DMG MORI NVX).
- **Horizontal Machining Centres (HMC)**: Dual pallet heavy metal cutting machines (Makino A88, Mori Seiki NH6300).
- **Gear Hobbing & Shaping**: Pfauter P900, TOS FO-10, Liebherr L1200 gear hobbers up to Module 16, and Fellows / Stanko gear shapers.
- **Heavy Duty Lathes**: Slant bed CNC turning centers & heavy manual oil country hollow-spindle lathes.

---

## 📑 4. Brand New Machinery Lines
- Modern CNC Slant Bed Turning Centers
- High-Speed Hydraulic Sheet Metal & Forging Presses
- Customized Automated Die Spray & Lubrication Systems
- Turnkey Automation: Robotic Loading/Unloading Systems for Forging Cells
