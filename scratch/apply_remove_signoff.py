# -*- coding: utf-8 -*-
with open('scratch/build_large_font_manual.py', 'r', encoding='utf-8') as f:
    text = f.read()

# Define old block to replace
old_signoff_marker = '<!-- Formal Acceptance & Sign-off Block -->'
old_p32_header_marker = '{get_page_header("GOVERNANCE, RELIABILITY &amp; FORMAL SIGN-OFF")}'

new_p32 = """# PAGE 32: INFRASTRUCTURE, ZERO-TRUST SECURITY & REGULATORY COMPLIANCE
# ==============================================================================
p32_content = f\"\"\"
  <div class="page">
    <div class="page-content">
      {get_page_header("SYSTEM SECURITY, INFRASTRUCTURE &amp; COMPLIANCE ARCHITECTURE")}
      
      <div class="section-header" style="background:#0f172a;">
        <span class="section-title">Enterprise Infrastructure, Zero-Trust Security &amp; Regulatory Compliance</span>
        <span class="section-tag">Continuous Reliability Standards</span>
      </div>

      <!-- 4-Quadrant Governance Grid -->
      <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px; margin-bottom:10px;">
        <div style="background:#ffffff; border:1.5px solid #cbd5e1; border-radius:6px; padding:9px 11px;">
          <div style="font-size:8.8pt; font-weight:800; color:#0f172a; text-transform:uppercase; border-bottom:1px solid #e2e8f0; padding-bottom:3px; margin-bottom:4px;">
            1. LAN-First Resilience &amp; Deployment Topology
          </div>
          <p style="font-size:8.6pt; line-height:1.38; color:#334155;">
            The dual-system architecture utilizes a hybrid edge deployment. The public commercial portal is distributed via global CDN edge nodes with aggressive client-side caching. The OMPI industrial ERP executes primarily on a dedicated local area network (LAN) edge server situated inside the Pune stockyard and workshop, guaranteeing sub-5ms internal transaction response times and 100% operational autonomy during external internet disruptions.
          </p>
        </div>
        <div style="background:#ffffff; border:1.5px solid #cbd5e1; border-radius:6px; padding:9px 11px;">
          <div style="font-size:8.8pt; font-weight:800; color:#0f172a; text-transform:uppercase; border-bottom:1px solid #e2e8f0; padding-bottom:3px; margin-bottom:4px;">
            2. Cryptographic Security &amp; Immutable Audit Trail
          </div>
          <p style="font-size:8.6pt; line-height:1.38; color:#334155;">
            Zero-Trust Role-Based Access Control (RBAC) enforces strict least-privilege boundaries across 5 operational tiers: Sales, Technical Engineering, Warehouse Operations, Statutory Finance, and Executive Leadership. Every pricing modification, quotation discount override, credit limit change, and invoice status update generates an append-only transaction record sealed with SHA-256 cryptographic hashes for forensic auditability.
          </p>
        </div>
        <div style="background:#ffffff; border:1.5px solid #cbd5e1; border-radius:6px; padding:9px 11px;">
          <div style="font-size:8.8pt; font-weight:800; color:#0f172a; text-transform:uppercase; border-bottom:1px solid #e2e8f0; padding-bottom:3px; margin-bottom:4px;">
            3. Statutory Tax &amp; Customs Compliance
          </div>
          <p style="font-size:8.6pt; line-height:1.38; color:#334155;">
            Deep harmonization with Indian Customs (CBIC) and GST statutory frameworks. System enforces automated 8-digit HSN mapping (8483 for mechanical clutch-brakes and transmission components, 6813 for friction materials, 8462 for machine tool presses). Generates compliant B2B tax invoices with CGST/SGST/IGST breakdowns, Rule 55 delivery challans, and one-click JSON exports for direct GSTR-1 portal filing.
          </p>
        </div>
        <div style="background:#ffffff; border:1.5px solid #cbd5e1; border-radius:6px; padding:9px 11px;">
          <div style="font-size:8.8pt; font-weight:800; color:#0f172a; text-transform:uppercase; border-bottom:1px solid #e2e8f0; padding-bottom:3px; margin-bottom:4px;">
            4. Disaster Recovery &amp; Redundant Snapshots
          </div>
          <p style="font-size:8.6pt; line-height:1.38; color:#334155;">
            Automated zero-downtime database snapshots execute every 24 hours to an isolated Network Attached Storage (NAS) array. Nightly encrypted archives are transmitted to a secondary off-site location. Disaster recovery protocols are tested quarterly, providing a Recovery Point Objective (RPO) of &lt;24 hours and a Recovery Time Objective (RTO) of &lt;15 minutes.
          </p>
        </div>
      </div>

      <!-- Infrastructure Benchmarks Table (Replaces Sign-Off Block) -->
      <div style="border:1.5px solid #cbd5e1; border-radius:6px; padding:8px 12px; background:#f8fafc; margin-top:6px;">
        <div style="font-size:8.8pt; font-weight:800; color:#0f172a; text-transform:uppercase; letter-spacing:0.5px; margin-bottom:4px;">
          Enterprise Infrastructure Performance &amp; Reliability Benchmarks
        </div>
        <table class="matrix-table" style="font-size:8.2pt; background:#ffffff;">
          <thead>
            <tr>
              <th style="width:20%; padding:5px 8px;">Architecture Dimension</th>
              <th style="width:28%; padding:5px 8px;">System 1: Dalal Web Platform</th>
              <th style="width:28%; padding:5px 8px;">System 2: OMPI Industrial ERP</th>
              <th style="width:24%; padding:5px 8px;">Disaster Recovery Standard</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td style="font-weight:700; color:#0f172a; padding:5px 8px;">Primary Hosting</td>
              <td style="padding:5px 8px;">Cloud Edge CDN (Multi-AZ Resilient)</td>
              <td style="padding:5px 8px;">On-Premise LAN Server (Pune Hub)</td>
              <td style="padding:5px 8px; color:#047857; font-weight:600;">Secondary Encrypted NAS Array</td>
            </tr>
            <tr>
              <td style="font-weight:700; color:#0f172a; padding:5px 8px;">Latency Benchmark</td>
              <td style="padding:5px 8px;">&lt; 120ms Global Response Time</td>
              <td style="padding:5px 8px;">&lt; 5ms Internal LAN Transaction Time</td>
              <td style="padding:5px 8px; color:#047857; font-weight:600;">&lt; 15-Minute Recovery Time (RTO)</td>
            </tr>
            <tr>
              <td style="font-weight:700; color:#0f172a; padding:5px 8px;">Offline Capability</td>
              <td style="padding:5px 8px;">Client-side cached parametric catalog</td>
              <td style="padding:5px 8px;">Full autonomy during internet dropouts</td>
              <td style="padding:5px 8px; color:#047857; font-weight:600;">Automated point-in-time restore</td>
            </tr>
            <tr>
              <td style="font-weight:700; color:#0f172a; padding:5px 8px;">Data &amp; Security Standards</td>
              <td style="padding:5px 8px;">HTTPS TLS 1.3, CSP &amp; OWASP Top 10</td>
              <td style="padding:5px 8px;">SHA-256 Ledger, 5-Tier Granular RBAC</td>
              <td style="padding:5px 8px; color:#047857; font-weight:600;">AES-256 Nightly Encrypted Snapshots</td>
            </tr>
          </tbody>
        </table>
      </div>

    </div>
    {get_page_footer(32)}
  </div>
\"\"\"
"""

# Let's find start of PAGE 32 and replace to end of p32_content definition
idx_p32 = text.find("# PAGE 32:")
idx_append = text.find("pages_html.append(p32_content)")

if idx_p32 != -1 and idx_append != -1:
    updated_text = text[:idx_p32] + new_p32 + "\n" + text[idx_append:]
    with open('scratch/build_large_font_manual.py', 'w', encoding='utf-8') as f:
        f.write(updated_text)
    print("Successfully replaced Page 32 in scratch/build_large_font_manual.py!")
else:
    print(f"Error: indices not found. idx_p32={idx_p32}, idx_append={idx_append}")

