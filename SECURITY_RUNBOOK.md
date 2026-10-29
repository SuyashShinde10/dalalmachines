# Dalal Machine Tools - Security Runbook (SECURITY_RUNBOOK.md)
*Operational Security Monitoring, Incident Response & Emergency Procedures*

---

## 1. Where the Security Logs Live
- **In-Memory Audit Chain**: High-speed tamper-evident blockchain-style hash chain accessible in real time at:
  - `GET /api/dev/security/status` (Developer SecOps Console)
- **Persistent Database Audit Table**: `server/data/db.json` (`logs` array). Every security event is immutably signed with `hash = SHA256(previousHash + eventData)`.
- **System Service Logs**: In Docker / Linux deployments, view container logs with:
  ```bash
  docker logs -f --tail 200 dalal-machinery-platform
  ```

---

## 2. How to Search User & IP Activity
Run the following commands on the server to trace any suspect user or IP:

### Find all activities by a specific IP:
```bash
node -e "const db = require('./server/db'); const ip = '192.168.1.50'; console.log(db.getLogs().filter(l => l.ip === ip));"
```

### Trace failed login attempts in the last 1 hour:
```bash
node -e "const db = require('./server/db'); const oneHourAgo = Date.now() - 3600000; console.log(db.getLogs().filter(l => l.action.includes('LOGIN_FAILED') && new Date(l.timestamp).getTime() > oneHourAgo));"
```

### Verify Integrity of the Audit Trail (Check for Tampering):
```bash
node -e "const sec = require('./server/security/defenseInDepth'); console.log(sec.verifyAuditChain());"
```

---

## 3. Automated Alert Thresholds & Alarms

| Event / Pattern | Severity | Trigger Threshold | Automated Countermeasure |
|---|---|---|---|
| **Failed Logins** | HIGH | > 5 attempts in 15 min | Account locked for 15 minutes + Progressive delay |
| **Scanner Probes** | HIGH | Any hit on honeypots (`/wp-admin`, `/.env`, etc.) | IP immediately banned for 24 hours via `honeypot.js` |
| **Token Theft / Replay** | CRITICAL | Token replayed from different client fingerprint | Instant HTTP 401 Unauthorized + Security event logged |
| **RFQ Lead Flooding** | MEDIUM | > 30 inquiries per hr / IP | Rate limit HTTP 429 Too Many Requests |
| **AI Query Abuse** | MEDIUM | > 60 queries per 10 min | Rate limit HTTP 429 + Automatic fallback to local engine |

---

## 4. Emergency Card: 15-Minute Containment Action Plan
If you suspect an active intrusion, unauthorized account access, or leaked credentials:

### Step 1: Stop the Bleeding (First 5 Minutes)
1. Invalidate all active user sessions by restarting the server with a new `JWT_SECRET` and `SECURITY_DEVICE_SALT`:
   ```bash
   # In .env: change JWT_SECRET to a new random value
   # Restart container:
   docker-compose restart
   ```
2. Revoke the Secret Gateway Access Key:
   ```bash
   # In .env: change PORTAL_GATEWAY_KEY=dmta-ops-NEW-KEY-2026
   ```

### Step 2: Lock Down Sensitive Accounts (5-10 Minutes)
1. Verify Google AI Studio / Gemini API key usage:
   - Visit https://aistudio.google.com/app/apikey
   - If misuse is observed, delete the active key and generate a fresh key.
2. Verify Admin Passwords:
   - Reset staff admin passwords via the SuperAdmin portal or CLI script.

### Step 3: Verify Data Integrity (10-15 Minutes)
1. Run the audit integrity verification:
   ```bash
   node -e "const sec = require('./server/security/defenseInDepth'); console.log(sec.verifyAuditChain());"
   ```
2. Verify `server/data/db.json` has not been modified or corrupted. Restore from the most recent backup if necessary.
