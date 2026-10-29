# Cloudflare Zero Trust (Access) Hardening Guide
## Dalal Machine Tools Agency Pvt. Ltd.

This guide outlines the industry-standard architecture for completely isolating and protecting Administrative, Superadmin, and Developer panels from public internet discovery.

---

### 1. The Core Philosophy: "Dark Portals"

In traditional hosting, anyone can navigate to `yourdomain.com/admin` or `yourdomain.com/dev` and see a login screen. Even if password-protected, the URL is public and vulnerable to:
* Zero-day exploits in authentication libraries
* Brute-force / credential stuffing attacks
* Port scanning and reconnaissance tools (Gobuster, Dirbuster, Shodan)

**Zero-Trust Solution:**
All administrative panels are kept completely "dark" from the public internet. Before any request can even reach the Node.js server, Cloudflare challenges the user for enterprise identity (Corporate Google Workspace, Microsoft Entra ID, or Email One-Time PIN).

---

### 2. Architecture Diagram

```
[Public Client] ────────▶ https://dalalmachines.com ──────▶ Node.js Server (Port 5000)
                                                                 │
                                                       (Accesses public machinery catalog)

[Staff / Developer] ─────▶ https://dalalmachines.com/portal-gate?key=...
                                  │
                                  ▼
                     ┌───────────────────────────┐
                     │ Cloudflare Zero Trust     │
                     │ (Email OTP / Okta / SAML) │
                     └─────────────┬─────────────┘
                                   │ Verified Corporate Staff
                                   ▼
                     ┌───────────────────────────┐
                     │ Node.js Route Shield      │
                     │ (Verifies HMAC Gate Pass) │
                     └─────────────┬─────────────┘
                                   │ Valid Passkey
                                   ▼
                     ┌───────────────────────────┐
                     │ Admin / Superadmin / Dev  │
                     │ Portals & Real-Time Sync  │
                     └───────────────────────────┘
```

---

### 3. Step-by-Step Cloudflare Zero Trust Setup

#### Step 1: Open Cloudflare Zero Trust Dashboard
1. Go to [one.dash.cloudflare.com](https://one.dash.cloudflare.com/).
2. Under **Access** > **Applications**, click **Add an Application**.
3. Choose **Self-Hosted**.

#### Step 2: Configure Application Rules
1. **Application Name:** `Dalal Internal Operations & Developer Console`
2. **Session Duration:** `12 hours`
3. **Application Domain:**
   * Path: `/portal-gate*`
   * Path: `/admin*`
   * Path: `/superadmin*`
   * Path: `/dev*`

#### Step 3: Define Access Policies
1. **Policy Name:** `Authorized Operations Staff Only`
2. **Action:** `Allow`
3. **Rule Configuration:**
   * **Include:** Emails ending in `@dalalmachines.com` OR designated developer email (e.g., `developer@dalalmachines.com`).
   * **Optional (Enhanced SecOps):** Add **Country/IP Requirement** (e.g., Only allow connections originating from India / designated office static IP).

#### Step 4: Enable Honeypot Bypass
Ensure that the honeypot paths (`/wp-admin`, `/.env`, `/phpmyadmin`) are **NOT** protected by Cloudflare Access rules. Allow them to pass through directly to the Node.js server so our built-in `server/security/honeypot.js` can auto-detect, trap, and blacklist malicious bot scanners automatically.

---

### 4. Local & Production Verification Checklist

* [x] Direct unauthenticated access to `/admin` returns **HTTP 404 (Not Found)** with the authentic Dalal 404 page.
* [x] Direct unauthenticated access to `/dev` returns **HTTP 404 (Not Found)**.
* [x] Probe to `/wp-admin` or `/.env` triggers the SecOps Honeypot and emits a real-time WebSocket alert.
* [x] Accessing `/portal-gate?key=dmta-ops-2026` grants the 12-hour signed gateway pass and unlocks staff login.
* [x] Developer console can view intruder logs and unban/ban IPs with 1 click.

