const fs = require('fs');

let code = fs.readFileSync('admin/js/admin-ai.js', 'utf8');

// 1. Update modal markup width and flex properties
code = code.replace(
  '<div class="aic-modal" style="width: 620px;">',
  '<div class="aic-modal" style="width: 720px; max-width: 95vw; max-height: 92vh; display: flex; flex-direction: column; overflow: hidden; border-radius: 14px; box-shadow: 0 25px 60px rgba(0,0,0,0.8);">'
);

// 2. Update body rendering in executeInquiryScore
const oldRenderStart = 'body.innerHTML = `';
const oldRenderEnd = 'const phoneNum = (inq.phone || \'\').replace(/[^0-9]/g, \'\');';

const targetIdx = code.indexOf(oldRenderStart, code.indexOf('executeInquiryScore'));
const endIdx = code.indexOf(oldRenderEnd, targetIdx);

if (targetIdx !== -1 && endIdx !== -1) {
  const replacement = `body.innerHTML = \`
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
              <strong style="color: var(--aic-gold); display: block; margin-bottom: 4px; font-size: 11.5px; text-transform: uppercase; letter-spacing: 0.5px;">AI Lead Procurement Analysis:</strong>
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
              <textarea id="aic-wa-reply-text" rows="8" style="width: 100%; min-height: 200px; height: auto; background: #070c14; color: #f8fafc; border: 1px solid rgba(255,255,255,0.14); border-radius: 8px; padding: 14px; font-size: 13px; line-height: 1.6; outline: none; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; resize: vertical; box-sizing: border-box; display: block;"></textarea>
            </div>
          \`;

          const textEl = document.getElementById('aic-wa-reply-text');
          if (textEl) {
            textEl.value = a.suggestedWhatsAppReply || '';
            // Auto-expand textarea to fit entire text with NO SCROLLBAR & ZERO OVERFLOW
            textEl.style.height = 'auto';
            textEl.style.height = Math.max(200, textEl.scrollHeight + 14) + 'px';
          }

          const copyBtn = document.getElementById('aic-btn-copy-draft');
          if (copyBtn && textEl) {
            copyBtn.onclick = () => {
              if (navigator.clipboard && navigator.clipboard.writeText) {
                navigator.clipboard.writeText(textEl.value).then(() => {
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

  code = code.substring(0, targetIdx) + replacement + code.substring(endIdx);
  console.log('Successfully replaced body rendering in admin-ai.js');
} else {
  console.error('Target indices not found:', targetIdx, endIdx);
}

// 3. Fix matched machines link wrapping
const oldMatchCard = `<div style="background: #1e293b; border: 1px solid var(--aic-border); border-radius: 6px; padding: 8px 12px; margin-bottom: 6px; font-size: 13px; display: flex; justify-content: space-between; align-items: center;">
                    <span><strong>\${escapeHTML(m.name)}</strong> (\${escapeHTML(m.location || 'Pune Yard')})</span>
                    <a href="/new/dalalmachine/product.html?id=\${m.id}" target="_blank" style="color: var(--aic-gold); font-size: 11.5px; text-decoration: none;">View Specs &rarr;</a>
                  </div>`;

const newMatchCard = `<div style="background: rgba(30, 41, 59, 0.75); border: 1px solid var(--aic-border); border-radius: 8px; padding: 10px 14px; margin-bottom: 8px; font-size: 13px; display: flex; justify-content: space-between; align-items: center; gap: 14px;">
                    <div style="flex: 1; min-width: 0;">
                      <div style="color: #ffffff; font-weight: 700; font-size: 13px; line-height: 1.4; word-break: break-word;">\${escapeHTML(m.name)}</div>
                      <div style="color: #94a3b8; font-size: 11.5px; margin-top: 3px;">
                        <i class="fa fa-map-marker" style="color: var(--aic-gold); margin-right: 4px;"></i>\${escapeHTML(m.location || 'Pune Yard')}
                        \${m.tonnage ? \` &bull; <span style="color:#e2e8f0; font-weight:600;">\${m.tonnage} Ton</span>\` : ''}
                      </div>
                    </div>
                    <a href="/new/dalalmachine/product.html?id=\${m.id}" target="_blank" style="background: rgba(248, 157, 19, 0.15); color: var(--aic-gold); border: 1px solid rgba(248, 157, 19, 0.35); padding: 6px 14px; border-radius: 6px; font-size: 11.5px; text-decoration: none; font-weight: 700; white-space: nowrap; flex-shrink: 0; display: inline-flex; align-items: center; gap: 4px;">View Specs &rarr;</a>
                  </div>`;

if (code.includes(oldMatchCard)) {
  code = code.replace(oldMatchCard, newMatchCard);
  console.log('Replaced machine match card markup');
} else {
  console.log('Old match card not found exactly, trying relaxed replace');
  code = code.replace(
    /\$\{escapeHTML\(m\.name\)\}<\/strong>[\s\S]*?View Specs &rarr;<\/a>\s*<\/div>/,
    `\${escapeHTML(m.name)}</div>
                      <div style="color: #94a3b8; font-size: 11.5px; margin-top: 3px;">
                        <i class="fa fa-map-marker" style="color: var(--aic-gold); margin-right: 4px;"></i>\${escapeHTML(m.location || 'Pune Yard')}
                        \${m.tonnage ? \` &bull; <span style="color:#e2e8f0; font-weight:600;">\${m.tonnage} Ton</span>\` : ''}
                      </div>
                    </div>
                    <a href="/new/dalalmachine/product.html?id=\${m.id}" target="_blank" style="background: rgba(248, 157, 19, 0.15); color: var(--aic-gold); border: 1px solid rgba(248, 157, 19, 0.35); padding: 6px 14px; border-radius: 6px; font-size: 11.5px; text-decoration: none; font-weight: 700; white-space: nowrap; flex-shrink: 0; display: inline-flex; align-items: center; gap: 4px;">View Specs &rarr;</a>
                  </div>`
  );
}

fs.writeFileSync('admin/js/admin-ai.js', code, 'utf8');
console.log('admin/js/admin-ai.js successfully updated!');

