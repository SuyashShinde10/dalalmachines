const fs = require('fs');

let code = fs.readFileSync('admin/js/admin-ai.js', 'utf8');

// 1. Modal template replacement
const oldModalTpl = `      <!-- AI Lead Scoring Modal (for Inquiries) -->
      <div class="aic-modal-backdrop" id="aic-inquiry-modal">
        <div class="aic-modal" style="width: 620px;">
          <div class="aic-modal-header">
            <h3><i class="fa fa-shield" style="color: var(--aic-gold);"></i> AI Lead Analysis & Smart Reply</h3>
            <button class="aic-close-btn" id="aic-inquiry-close"><i class="fa fa-times"></i></button>
          </div>
          <div class="aic-modal-body" id="aic-inquiry-body">
            <div style="text-align: center; padding: 30px;">Analyzing lead with AI...</div>
          </div>
          <div class="aic-modal-footer">
            <button type="button" class="btn-secondary" id="aic-inquiry-done">Close</button>
            <button type="button" class="btn-primary" id="aic-inquiry-copy-wa" style="background: #10b981; color: #fff; font-weight: 700; border: none; padding: 8px 18px; border-radius: 6px; cursor: pointer;">
              <i class="fa fa-whatsapp"></i> Open in WhatsApp
            </button>
          </div>
        </div>
      </div>`;

const newModalTpl = `      <!-- AI Lead Scoring Modal (for Inquiries) -->
      <div class="aic-modal-backdrop" id="aic-inquiry-modal">
        <div class="aic-modal" style="width: 720px; max-width: 95vw; max-height: 92vh; display: flex; flex-direction: column; overflow: hidden; border-radius: 14px; box-shadow: 0 25px 60px rgba(0,0,0,0.85);">
          <div class="aic-modal-header" style="padding: 16px 22px; background: #090e17; border-bottom: 1px solid var(--aic-border); display: flex; align-items: center; justify-content: space-between;">
            <h3 style="margin: 0; font-size: 16px; font-weight: 700; color: #fff; display: flex; align-items: center; gap: 8px;">
              <i class="fa fa-shield" style="color: var(--aic-gold);"></i> AI Lead Analysis &amp; WhatsApp Reply
            </h3>
            <button class="aic-close-btn" id="aic-inquiry-close" style="background:none; border:none; color:#94a3b8; font-size:20px; cursor:pointer;"><i class="fa fa-times"></i></button>
          </div>
          <div class="aic-modal-body" id="aic-inquiry-body" style="overflow-y: auto; max-height: calc(92vh - 140px); padding: 20px 24px;">
            <div style="text-align: center; padding: 40px 20px;">
              <i class="fa fa-spinner fa-spin" style="font-size: 28px; color: var(--aic-gold);"></i>
              <div style="margin-top: 14px; font-weight: 700; color: #fff; font-size: 14px;">Analyzing inquiry with Dalal AI Lead Engine...</div>
            </div>
          </div>
          <div class="aic-modal-footer" style="padding: 14px 24px; background: #090e17; border-top: 1px solid var(--aic-border); display: flex; justify-content: space-between; align-items: center;">
            <button type="button" class="btn-secondary" id="aic-inquiry-done" style="background: rgba(255,255,255,0.08); color: #fff; border: 1px solid rgba(255,255,255,0.15); padding: 8px 18px; border-radius: 6px; cursor: pointer; font-weight: 600;">Close</button>
            <button type="button" class="btn-primary" id="aic-inquiry-copy-wa" style="background: #10b981; color: #fff; font-weight: 700; border: none; padding: 9px 20px; border-radius: 6px; cursor: pointer; display: inline-flex; align-items: center; gap: 8px; box-shadow: 0 4px 14px rgba(16,185,129,0.35);">
              <i class="fa fa-whatsapp" style="font-size: 16px;"></i> <span>Open in WhatsApp</span>
            </button>
          </div>
        </div>
      </div>`;

// Normalize CRLF to LF for safe comparison
const normCode = code.replace(/\r\n/g, '\n');
const normOldModal = oldModalTpl.replace(/\r\n/g, '\n');

if (normCode.includes(normOldModal)) {
  code = normCode.replace(normOldModal, newModalTpl.replace(/\r\n/g, '\n'));
  console.log('Replaced modal container template');
} else {
  console.log('Old modal template not matched directly');
}

// 2. Body rendering replacement
const startHook = 'let matchedHtml = \'\';';
const endHook = 'const phoneNum = (inq.phone || \'\').replace(/[^0-9]/g, \'\');';

const sPos = code.indexOf(startHook);
const ePos = code.indexOf(endHook);

if (sPos !== -1 && ePos !== -1) {
  const replacementBody = `let matchedHtml = '';
          if (a.matchedMachines && a.matchedMachines.length > 0) {
            matchedHtml = \`
              <div style="margin-top: 14px;">
                <div style="font-size: 11px; font-weight: 800; color: var(--aic-gold); margin-bottom: 8px; text-transform: uppercase; letter-spacing: 0.5px;">RECOMMENDED CATALOG MATCHES:</div>
                \${a.matchedMachines.map(m => \`
                  <div style="background: rgba(30, 41, 59, 0.75); border: 1px solid var(--aic-border); border-radius: 8px; padding: 10px 14px; margin-bottom: 8px; font-size: 13px; display: flex; justify-content: space-between; align-items: center; gap: 14px;">
                    <div style="flex: 1; min-width: 0;">
                      <div style="color: #ffffff; font-weight: 700; font-size: 13px; line-height: 1.4; word-break: break-word;">\${escapeHTML(m.name)}</div>
                      <div style="color: #94a3b8; font-size: 11.5px; margin-top: 3px;">
                        <i class="fa fa-map-marker" style="color: var(--aic-gold); margin-right: 4px;"></i>\${escapeHTML(m.location || 'Pune Yard')}
                        \${m.tonnage ? \` &bull; <span style="color:#e2e8f0; font-weight:600;">\${m.tonnage} Ton</span>\` : ''}
                      </div>
                    </div>
                    <a href="/new/dalalmachine/product.html?id=\${m.id}" target="_blank" style="background: rgba(248, 157, 19, 0.15); color: var(--aic-gold); border: 1px solid rgba(248, 157, 19, 0.35); padding: 6px 14px; border-radius: 6px; font-size: 11.5px; text-decoration: none; font-weight: 700; white-space: nowrap; flex-shrink: 0; display: inline-flex; align-items: center; gap: 4px;">View Specs &rarr;</a>
                  </div>
                \`).join('')}
              </div>
            \`;
          }

          body.innerHTML = \`
            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 14px; border-bottom: 1px solid var(--aic-border); padding-bottom: 12px; gap: 12px; flex-wrap: wrap;">
              <div>
                <div style="font-size: 16px; font-weight: 700; color: #fff;">\${escapeHTML(inq.name || 'Inquiry')}</div>
                <div style="font-size: 12px; color: var(--aic-text-muted); margin-top: 2px;">
                  \${escapeHTML(inq.company || 'Private Buyer')} &bull; 
                  <span style="color: #cbd5e1; font-weight: 600;">\${escapeHTML(inq.phone || inq.email || 'No Direct Phone')}</span>
                </div>
              </div>
              <div class="aic-score-badge \${scoreClass}" style="font-size: 12px; font-weight: 800; padding: 6px 14px; border-radius: 9999px;">
                \${scoreIcon} \${a.leadScore} LEAD
              </div>
            </div>

            <div style="background: rgba(248, 157, 19, 0.08); border: 1px solid rgba(248, 157, 19, 0.25); border-radius: 8px; padding: 12px 14px; margin-bottom: 14px; font-size: 12.5px; line-height: 1.5; color: #f1f5f9;">
              <strong style="color: var(--aic-gold); display: block; margin-bottom: 4px; font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px;">AI Lead Procurement Analysis:</strong>
              \${escapeHTML(a.scoreReason)}
            </div>

            \${matchedHtml}

            <div style="margin-top: 16px;">
              <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                <div style="font-size: 11px; font-weight: 800; color: #cbd5e1; letter-spacing: 0.5px; text-transform: uppercase; display: flex; align-items: center; gap: 6px;">
                  <i class="fa fa-whatsapp" style="color: #10b981; font-size: 14px;"></i>
                  <span>Ready-to-Send WhatsApp / Email Reply:</span>
                </div>
                <button type="button" id="aic-btn-copy-draft" style="background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.18); color: #cbd5e1; font-size: 11.5px; font-weight: 700; padding: 5px 12px; border-radius: 6px; cursor: pointer; display: inline-flex; align-items: center; gap: 6px; transition: all 0.2s ease;">
                  <i class="fa fa-clone"></i> <span>Copy Text</span>
                </button>
              </div>
              <textarea id="aic-wa-reply-text" rows="9" style="width: 100%; min-height: 220px; height: auto; background: #070c14; color: #f8fafc; border: 1px solid rgba(255,255,255,0.14); border-radius: 8px; padding: 14px; font-size: 13px; line-height: 1.6; outline: none; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; resize: vertical; box-sizing: border-box; display: block;"></textarea>
            </div>
          \`;

          const textEl = document.getElementById('aic-wa-reply-text');
          if (textEl) {
            textEl.value = a.suggestedWhatsAppReply || '';
            // Auto-expand textarea to fit entire text with NO SCROLLBAR & ZERO OVERFLOW
            textEl.style.height = 'auto';
            textEl.style.height = Math.max(220, textEl.scrollHeight + 14) + 'px';
          }

          const copyBtn = document.getElementById('aic-btn-copy-draft');
          if (copyBtn && textEl) {
            copyBtn.onclick = () => {
              const val = textEl.value;
              if (navigator.clipboard && navigator.clipboard.writeText) {
                navigator.clipboard.writeText(val).then(() => {
                  copyBtn.innerHTML = '<i class="fa fa-check" style="color:#10b981;"></i> <span style="color:#10b981;">Copied!</span>';
                  setTimeout(() => {
                    copyBtn.innerHTML = '<i class="fa fa-clone"></i> <span>Copy Text</span>';
                  }, 2500);
                }).catch(() => {
                  textEl.select();
                  document.execCommand('copy');
                });
              } else {
                textEl.select();
                document.execCommand('copy');
                copyBtn.innerHTML = '<i class="fa fa-check" style="color:#10b981;"></i> <span style="color:#10b981;">Copied!</span>';
                setTimeout(() => {
                  copyBtn.innerHTML = '<i class="fa fa-clone"></i> <span>Copy Text</span>';
                }, 2500);
              }
            };
          }

          `;

  code = code.substring(0, sPos) + replacementBody + code.substring(ePos);
  console.log('Replaced body rendering');
} else {
  console.error('Hooks not found:', sPos, ePos);
}

fs.writeFileSync('admin/js/admin-ai.js', code, 'utf8');
console.log('admin-ai.js patched successfully!');

