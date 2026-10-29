# Dalal Machine Tools Agency Pvt. Ltd. - Security Map (SECURITY_MAP.md)
*Generated according to Pre-Launch Security Toolkit (Check 00)*

---

## 1. Stack & Architecture
- **Language & Runtime**: Node.js v20+ / Express 5.2.1
- **Architectural Style**: Clean Modular Monolith with Sub-10ms In-Memory Micro-Cache, Zero-Trust Cryptographic Layer, Bank-Grade Helmet (CSP Level 3), Real-Time WebSockets (Socket.IO v4.8.4), and Progressive Web App (PWA) Offline Engine.
- **Package Manager**: npm (Strict clean dependencies, `npm audit` 0 vulnerabilities).
- **Hosting / Deployment Target**: Multi-stage Docker container (`node:20-alpine`, non-root user `dalal:nodejs`), deployable to VPS, Render, AWS ECS, or Fly.io with automated `docker-compose.yml`.

---

## 2. Data Stores & Storage Topology
- **Primary Database**: Lightweight Atomic Embedded Relational Database in `server/data/db.json` managed via `server/db.js`.
  - Accessed: **Server-only**. No direct client SDK access (eliminates client-side Supabase/Firebase RLS exposure risks).
  - Collections: `products` (49 active machines), `users` (RBAC admin/developer), `inquiries` (quotation leads), `logs` (tamper-evident audit trail), `settings` (site config).
  - Data Sensitivity:
    - `users`: High (bcrypt password hashes, role assignments).
    - `inquiries`: Medium-High (client phone numbers, emails, industrial inquiries).
    - `products`: Public-Commercial.
    - `logs`: High (cryptographically chained audit records).
- **File Storage**: Local persistent disk `/uploads` for machinery photography and PDF brochures.
  - Restricted via strict Multer MIME filtering and path traversal barriers.

---

## 3. Identity, Authentication & Session Life-Cycle
- **Auth Engine**: Cryptographic JWT (HMAC-SHA256) combined with **Hardware/Device Fingerprinting**:
  - `Fingerprint = SHA256(Subnet-IP + UserAgent + SecretSalt)` embedded into every signed token.
  - Stored: `HttpOnly`, `SameSite: Lax`, `Secure` cookie and/or `Authorization: Bearer <token>`.
  - Anti-Replay / Anti-Theft: If a token is stolen and replayed from a different IP or User-Agent, it is immediately dropped with HTTP 401.
  - Brute Force Lockout: Progressive delay + account lockout after 5 consecutive failed attempts.
- **Authorization Levels (RBAC)**:
  - `public`: Browsing machinery catalog, dynamic sitemaps, robots.txt, submitting RFQ inquiries, AI chatbot and technical matchmaker.
  - `admin`: Product management, inquiry lead tracking, PDF quotation generation.
  - `superadmin`: Developer console, system settings, AI engine configuration, user account management.
- **Portals Concealment Gate**:
  - Direct access to `/admin`, `/superadmin`, and `/dev` is cloaked as **HTTP 404 Not Found**.
  - Requires visiting the secret gateway `/portal-gate?key=dmta-ops-2026&to=admin` to receive an HMAC-signed access pass.

---

## 4. Entry Points Inventory

| Entry Point | Method | Purpose | Auth Required | Role Allowed | Inputs Accepted |
|---|---|---|---|---|---|
| `/` | GET | Public Industrial Homepage | No | Public | None |
| `/new/dalalmachine/` | GET | Machinery Portal App Shell | No | Public | Query filters |
| `/new/dalalmachine/category.html` | GET | 26-Category Machine Catalog | No | Public | `category`, `section`, `location`, `query` |
| `/new/dalalmachine/product.html` | GET | Product Specification Detail | No | Public | `id` |
| `/manifest.json` | GET | PWA Web App Manifest | No | Public | None |
| `/sw.js` | GET | Offline Service Worker | No | Public | None |
| `/sitemap.xml` | GET | Dynamic XML Sitemap (83 URLs) | No | Public / Search Engines | None |
| `/robots.txt` | GET | AI & Crawler Policy Rules | No | Public / Crawlers | None |
| `/api/health` | GET | Production Health Check | No | Public / Load Balancers | None |
| `/portal-gate` | GET/POST | Secret URL Cloaking Gateway | Secret Key | Authorized Staff | `key`, `to` |
| `/portal-exit` | GET | Revoke Gateway Passkey | Yes | Any with Gate Pass | None |
| `/api/auth/login` | POST | Secure Staff Login | No (Rate Limited) | Public Staff | `username`, `password` |
| `/api/auth/me` | GET | Verify Current Session | Yes | User | JWT Cookie / Bearer |
| `/api/auth/logout` | POST | Terminate Session | Yes | User | None |
| `/api/products` | GET | Fast In-Memory Catalog Feed | No (Cached) | Public | `category`, `section`, `location`, `query` |
| `/api/products/:id` | GET | Single Machine Specs | No (Cached) | Public | `id` (Param) |
| `/api/products/:id/spec-sheet` | GET | Vector A4 PDF Spec Sheet | No (Rate Limited) | Public / Admin | `id`, `buyer`, `price`, `quoteNo` |
| `/api/products` | POST | Add New Machine | Yes | Admin | Machine schema, multipart image |
| `/api/products/:id` | PUT | Edit Machine Specs | Yes | Admin | Partial machine schema |
| `/api/products/:id` | DELETE | Delete Machine | Yes | Admin | `id` (Param) |
| `/api/inquiries` | POST | Submit Quotation RFQ | No (Rate Limited) | Public | `name`, `email`, `phone`, `company`, `message` |
| `/api/inquiries` | GET | List All Buyer Inquiries | Yes | Admin | None |
| `/api/ai/matchmaker` | POST | AI Technical Machine Matcher | No (Rate Limited) | Public | `query` (Natural Language), `options` |
| `/api/ai/chat` | POST | Multilingual AI Chat Advisor | No (Rate Limited) | Public | `message`, `history`, `language` |
| `/api/ai/admin/copilot` | POST | Staff Operations Assistant | Yes | Admin | `message` |
| `/api/ai/parse-product` | POST | Spec Sheet Form Auto-Fill | Yes | Admin | `rawText` |
| `/api/ai/score-inquiry` | POST | Smart Lead Scoring Engine | Yes | Admin | `inquiry` |
| `/api/users` | GET/POST | Manage Staff Accounts | Yes | SuperAdmin | User fields, credentials |
| `/api/system/settings` | GET/PUT | Global Site Configuration | Yes | SuperAdmin | Settings payload |
| `/api/dev/security/status` | GET | Real-Time SecOps Telemetry | Yes (Dev IP) | Developer / Admin | None |

---

## 5. Third-Party Integrations
- **Google Gemini API**: Optional AI Intelligence Engine for deep technical spec analysis. Uses server-only `GEMINI_API_KEY`. If unconfigured, automatically falls back to Built-In Machinery Intelligence.
- **WhatsApp Web API**: Direct lead dispatch link generation targeting MD Mr. Vinit Dalal (`+91 9821232131`). Zero client-side credentials exposed.
- **OMPI India Technical Partnership**: Embedded clutch-brake data and verification references.

---

## 6. Environment Variables (Secret vs Public)

| Variable Name | Exposure | Purpose |
|---|---|---|
| `PORT` | Server-Only | Listening port (Default 5000) |
| `NODE_ENV` | Server-Only | Production runtime environment flag |
| `SITE_URL` | Server-Only | Canonical URL (`https://dalalmachines.com`) |
| `JWT_SECRET` | **SECRET** | 64-character HMAC token signing key |
| `JWT_EXPIRY` | Server-Only | Session duration (Default `7d` / `8h`) |
| `SECURITY_DEVICE_SALT` | **SECRET** | Zero-trust device fingerprinting salt |
| `GATEWAY_COOKIE_SECRET`| **SECRET** | HMAC signing key for `dmta_gate_pass` cookie |
| `PORTAL_GATEWAY_KEY` | **SECRET** | Secret key required to reveal `/admin` and `/dev` |
| `GEMINI_API_KEY` | **SECRET** | Optional Google AI Studio Key (Server-side only) |
| `WHATSAPP_DISPATCH_PHONE` | Server-Only | Target phone for lead notifications |
| `ALLOWED_DEV_IPS` | Server-Only | Developer portal IP whitelist |
| `HONEYPOT_ENABLED` | Server-Only | Automated scanner auto-ban toggle (`true`) |

---

## 7. High-Risk Features & Defensive Countermeasures
1. **File Uploads (`/uploads`)**:
   - Risk: Malicious executable/webshell disguised as image.
   - Defense: Extension allowlist (`.jpg`, `.jpeg`, `.png`, `.webp`), 5MB size limit, stored outside executable directories, served with `nosniff`.
2. **AI Machinery Matchmaker & Public Chat**:
   - Risk: Cost abuse, prompt injection, DoS.
   - Defense: `chatLimiter` (60 requests per 10 mins per IP), input length limits, strict output sanitization, zero secrets in prompt context.
3. **Admin & Developer Portals**:
   - Risk: Targeted credential stuffing, scanning bots.
   - Defense: Portals completely cloaked with HTTP 404 Decoy via `routeShield.js`. Account lockout after 5 failed attempts. Honeypots (`/wp-admin`, `/.env`, etc.) ban attacking IPs.
4. **Lead Inquiries**:
   - Risk: Spam flooding, database bloat.
   - Defense: `inquiryLimiter` (30 requests per hour per IP), deep prototype pollution sanitization, chained cryptographic audit logging.
