# 01 - Design System & UI Specifications

> **Aesthetic Foundation**: Engineered to replicate the bold, authoritative industrial look of the ThemeForest **Machinery – Factory & Industrial Business** template while representing **Dalal Machine Tools Agency Pvt. Ltd.** as a heavy machinery powerhouse.

---

## 🎨 1. Color Palette Tokens

The color scheme balances high-visibility **Industrial Amber/Gold** with **Heavy Machine Charcoal** and **Steel Slate**, creating an unmistakably authentic engineering atmosphere.

### CSS Custom Properties (`:root`)

```css
:root {
  /* Brand Primary - Industrial Safety Amber / Golden Yellow */
  --color-primary: #ffb400;
  --color-primary-hover: #e09e00;
  --color-primary-light: #fff8e6;
  --color-primary-dark: #b88200;

  /* Brand Secondary - Deep Industrial Charcoal / Foundry Black */
  --color-secondary: #141b22;
  --color-secondary-light: #1f2937;
  --color-secondary-muted: #374151;

  /* Accent & Technical Grays */
  --color-steel-dark: #242c35;
  --color-steel-base: #4b5563;
  --color-steel-light: #9ca3af;
  --color-border: #e5e7eb;
  --color-surface-subtle: #f8fafc;
  --color-surface-white: #ffffff;

  /* Status & Verification Badges */
  --color-success: #10b981; /* Inspected Under Power */
  --color-info: #0284c7;    /* In Stock Europe/Russia */
  --color-warning: #f59e0b; /* Available on High Seas */
  --color-danger: #ef4444;

  /* Industrial Accent Overlays */
  --overlay-dark: rgba(20, 27, 34, 0.88);
  --overlay-hero: linear-gradient(135deg, rgba(20, 27, 34, 0.94) 0%, rgba(31, 41, 55, 0.78) 100%);
  --overlay-card: linear-gradient(180deg, rgba(0, 0, 0, 0) 50%, rgba(20, 27, 34, 0.9) 100%);
}
```

### Color Usage Matrix

| Token | Hex Code | Visual Application |
|---|---|---|
| `--color-primary` | `#FFB400` | Header active state, CTA button fills, quote icons, metric counter highlights, machine badge tags. |
| `--color-secondary` | `#141B22` | Topbar background, header navigation bar, hero text headings, footer background, primary buttons on light surfaces. |
| `--color-steel-dark` | `#242C35` | Secondary card background, footer widget background, tab navigation background. |
| `--color-surface-subtle`| `#F8FAFC` | Main body background, alternating section backgrounds (services, inspection steps). |
| `--color-success` | `#10B981` | "Inspected Under Power" verified seal, availability status. |

---

## 🔤 2. Typography System

The typography pairs an **Industrial Extended Grotesque** font for headings (Barlow / Rajdhani) with a crisp, ultra-legible **Modern Sans-Serif** for technical specifications and body text (Inter).

### Google Font Embeds
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Barlow:ital,wght@0,500;0,600;0,700;0,800;0,900;1,700&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
```

### Type Scale

```css
:root {
  --font-heading: 'Barlow', sans-serif;
  --font-body: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;

  /* Scale */
  --text-xs:   0.75rem;   /* 12px - Specs captions, timestamps */
  --text-sm:   0.875rem;  /* 14px - Topbar, metadata, table data */
  --text-base: 1.00rem;   /* 16px - Standard body copy */
  --text-lg:   1.125rem;  /* 18px - Subheadings, card titles */
  --text-xl:   1.25rem;   /* 20px - Section highlights */
  --text-2xl:  1.50rem;   /* 24px - Subsection titles */
  --text-3xl:  1.875rem;  /* 30px - Section headings */
  --text-4xl:  2.25rem;   /* 36px - Page banner headers */
  --text-5xl:  3.25rem;   /* 52px - Hero slide main headline */
  --text-6xl:  4.25rem;   /* 68px - Hero big metric numbers (e.g., 6300T) */
}

/* Heading Styling Rules */
h1, h2, h3, h4, h5, h6 {
  font-family: var(--font-heading);
  color: var(--color-secondary);
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: -0.02em;
  line-height: 1.15;
}

.section-subtitle {
  font-family: var(--font-heading);
  font-size: var(--text-sm);
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.15em;
  color: var(--color-primary-dark);
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.section-subtitle::before {
  content: '';
  display: inline-block;
  width: 24px;
  height: 3px;
  background-color: var(--color-primary);
}
```

---

## 🔲 3. Spacing, Grid & Layout Containers

Built around the classic **12-column industrial grid** with standard 30px gutters and 1200px max-width container.

```css
:root {
  --container-max: 1200px;
  --container-wide: 1360px;
  --gutter: 1.875rem; /* 30px */

  --space-xs: 0.25rem; /* 4px */
  --space-sm: 0.5rem;  /* 8px */
  --space-md: 1rem;    /* 16px */
  --space-lg: 1.5rem;  /* 24px */
  --space-xl: 2.5rem;  /* 40px */
  --space-2xl: 4rem;   /* 64px */
  --space-3xl: 6rem;   /* 96px */
}

.container {
  width: 100%;
  max-width: var(--container-max);
  margin-left: auto;
  margin-right: auto;
  padding-left: 1rem;
  padding-right: 1rem;
}
```

---

## 🔘 4. Industrial Buttons & Micro-Interactions

Inspired by the ThemeForest Machinery template, buttons feature **bold industrial chamfers**, **high-contrast color blocks**, and smooth sliding hover transitions.

### Button Variants

```css
/* Base Button */
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  font-family: var(--font-heading);
  font-size: var(--text-sm);
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  padding: 0.875rem 2rem;
  border: 2px solid transparent;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  text-decoration: none;
  border-radius: 2px;
}

/* Primary Industrial Yellow Button */
.btn-primary {
  background-color: var(--color-primary);
  color: var(--color-secondary);
  border-color: var(--color-primary);
}

.btn-primary:hover {
  background-color: var(--color-secondary);
  color: var(--color-primary);
  border-color: var(--color-secondary);
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
}

/* Secondary Dark Button */
.btn-secondary {
  background-color: var(--color-secondary);
  color: #ffffff;
  border-color: var(--color-secondary);
}

.btn-secondary:hover {
  background-color: var(--color-primary);
  color: var(--color-secondary);
  border-color: var(--color-primary);
  transform: translateY(-2px);
}

/* Outline Technical Button */
.btn-outline-white {
  background-color: transparent;
  color: #ffffff;
  border-color: rgba(255, 255, 255, 0.5);
}

.btn-outline-white:hover {
  background-color: #ffffff;
  color: var(--color-secondary);
  border-color: #ffffff;
}
```

---

## 🏷 5. Industrial Badges & Machine Tags

Used on machine listings to instantly communicate verification status, capacity, and stock location.

```css
.badge {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  padding: 0.3rem 0.75rem;
  font-size: var(--text-xs);
  font-family: var(--font-heading);
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  border-radius: 2px;
}

/* Verified Under Power Badge */
.badge-under-power {
  background: rgba(16, 185, 129, 0.15);
  color: #065f46;
  border: 1px solid #10b981;
}

/* Tonnage Badge */
.badge-tonnage {
  background: var(--color-primary);
  color: var(--color-secondary);
  font-weight: 900;
}

/* Location Badge */
.badge-origin {
  background: var(--color-secondary);
  color: #ffffff;
}
```

---

## 🪟 6. Shadow & Elevation Tokens

```css
:root {
  --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.08), 0 2px 4px -1px rgba(0, 0, 0, 0.04);
  --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
  --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.15), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  --shadow-card-hover: 0 16px 32px rgba(20, 27, 34, 0.14);
}
```

---

## 📱 7. Responsive Breakpoints

| Breakpoint Name | Media Query | Layout Target |
|---|---|---|
| Mobile Small | `< 576px` | Single column, compressed headers, sticky call button |
| Mobile Large | `576px - 767px` | 2-column machine catalog grid, collapsible navigation |
| Tablet | `768px - 991px` | 2-column feature blocks, tablet drawer navigation |
| Desktop | `992px - 1199px` | 3-column machine cards, full mega menu enabled |
| Large Desktop | `>= 1200px` | 4-column feature highlights, 1200px centered canvas |
