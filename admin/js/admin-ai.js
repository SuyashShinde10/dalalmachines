/**
 * Dalal Admin & Superadmin - AI Copilot & Productivity Tools Engine
 * Author: Suyash Shinde | Version: 2.0
 */

(function () {
  'use strict';

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initAdminAI);
  } else {
    initAdminAI();
  }

  function initAdminAI() {
    if (document.getElementById('aic-copilot-container')) return;

    // Remove legacy or duplicate inquiry modal if any exists in DOM
    const legacyModal = document.getElementById('aic-inquiry-modal');
    if (legacyModal) legacyModal.remove();

    // 1. Build and Inject Drawer UI
    const container = document.createElement('div');
    container.id = 'aic-copilot-container';
    container.innerHTML = `
      <!-- Floating Copilot Button -->
      <div class="aic-float-trigger" id="aic-float-trigger" title="Open Dalal AI Operations Copilot">
        <div class="aic-float-trigger-icon">
          <i class="fa fa-magic"></i>
        </div>
        <div class="aic-float-trigger-text">AI Copilot</div>
      </div>

      <!-- Backdrop -->
      <div class="aic-drawer-backdrop" id="aic-drawer-backdrop"></div>

      <!-- Slide-in Drawer -->
      <aside class="aic-drawer" id="aic-drawer" aria-label="Dalal AI Operations Copilot">
        <div class="aic-drawer-header">
          <div class="aic-brand-title">
            <div class="aic-brand-icon">
              <i class="fa fa-bolt"></i>
            </div>
            <div class="aic-brand-text">
              <h3>Dalal AI Copilot</h3>
              <span id="aic-engine-status-text">Operations Intelligence</span>
            </div>
          </div>
          <button class="aic-close-btn" id="aic-drawer-close" title="Close Drawer">
            <i class="fa fa-times"></i>
          </button>
        </div>

        <div class="aic-drawer-body" id="aic-drawer-body">
          <div class="aic-msg bot">
            <div class="aic-msg-content">
              <h3>Dalal Operations Copilot Active</h3>
              Hello! Main aapka ERP Operations AI Copilot hoon. Aap mujhse live inventory stats, yard distribution, customer inquiries, ya proposal drafting ke baare me pooch sakte hain.
            </div>
          </div>
        </div>

        <div class="aic-prompts-bar" id="aic-prompts-bar">
          <button class="aic-prompt-chip" data-q="Show operations summary">📊 Operations Summary</button>
          <button class="aic-prompt-chip" data-q="How many machines in Pune yard?">📍 Pune Yard Stock</button>
          <button class="aic-prompt-chip" data-q="Summarize new customer inquiries">📬 Customer Leads</button>
          <button class="aic-prompt-chip" data-q="List European sourcing stock">🚢 European Import Stock</button>
        </div>

        <div class="aic-drawer-footer">
          <input type="text" id="aic-input" class="aic-input" placeholder="Ask operations questions or draft proposals..." autocomplete="off">
          <button id="aic-send-btn" class="aic-send-btn" title="Send to AI">
            <i class="fa fa-paper-plane"></i>
          </button>
        </div>
      </aside>

      <!-- AI Auto-Fill Modal (for Product Form) -->
      <div class="aic-modal-backdrop" id="aic-autofill-modal">
        <div class="aic-modal">
          <div class="aic-modal-header">
            <h3><i class="fa fa-magic" style="color: var(--aic-gold);"></i> 1-Click AI Machine Auto-Fill</h3>
            <button class="aic-close-btn" id="aic-autofill-close"><i class="fa fa-times"></i></button>
          </div>
          <div class="aic-modal-body">
            <p style="font-size: 13px; color: var(--aic-text-muted); margin-bottom: 12px;">
              Supplier ka raw WhatsApp forward, email spec sheet ya machine details niche paste karein. AI automatically fields aur specifications table fill kar dega:
            </p>
            <textarea id="aic-autofill-input" class="form-control" style="width: 100%; height: 160px; background: #090e17; color: #fff; border: 1px solid var(--aic-border); border-radius: 8px; padding: 12px; font-family: monospace; font-size: 12.5px; resize: vertical;" placeholder="Example:&#10;Russian 1600 Ton Hot Forging Press Model K8542 Year 1991&#10;Slide Stroke: 350 mm&#10;Bed Area: 1250 x 1250 mm&#10;Location: In Stock Pune yard&#10;Condition: Excellent live power inspected abroad"></textarea>
          </div>
          <div class="aic-modal-footer">
            <button type="button" class="btn-secondary" id="aic-autofill-cancel">Cancel</button>
            <button type="button" class="btn-primary" id="aic-autofill-submit" style="background: var(--aic-gold); color: #0f172a; font-weight: 700; border: none; padding: 8px 18px; border-radius: 6px; cursor: pointer;">
              <i class="fa fa-magic"></i> Extract & Auto-Fill Form
            </button>
          </div>
        </div>
      </div>

      <!-- AI Lead Scoring Modal (for Inquiries) -->
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
      </div>
    `;
    document.body.appendChild(container);

    // 2. Add Topbar Copilot Button if topbar exists
    const topbarRight = document.querySelector('.topbar-right, .sa-topbar-right');
    if (topbarRight) {
      const topbarBtn = document.createElement('button');
      topbarBtn.type = 'button';
      topbarBtn.className = 'btn-topbar-copilot';
      topbarBtn.innerHTML = `<i class="fa fa-magic"></i> <span>AI Copilot</span>`;
      topbarBtn.addEventListener('click', toggleDrawer);
      topbarRight.insertBefore(topbarBtn, topbarRight.firstChild);
    }

    // 3. Drawer Toggle Logic
    const trigger = document.getElementById('aic-float-trigger');
    const drawer = document.getElementById('aic-drawer');
    const backdrop = document.getElementById('aic-drawer-backdrop');
    const closeBtn = document.getElementById('aic-drawer-close');
    const inputEl = document.getElementById('aic-input');
    const sendBtn = document.getElementById('aic-send-btn');
    const bodyEl = document.getElementById('aic-drawer-body');

    function toggleDrawer() {
      drawer.classList.toggle('active');
      backdrop.classList.toggle('active');
      if (drawer.classList.contains('active')) {
        setTimeout(() => inputEl.focus(), 200);
      }
    }

    trigger.addEventListener('click', toggleDrawer);
    backdrop.addEventListener('click', toggleDrawer);
    closeBtn.addEventListener('click', toggleDrawer);

    // Prompt Chips
    document.querySelectorAll('.aic-prompt-chip').forEach(chip => {
      chip.addEventListener('click', () => {
        const q = chip.getAttribute('data-q');
        if (q) {
          inputEl.value = q;
          handleAdminSend();
        }
      });
    });

    sendBtn.addEventListener('click', handleAdminSend);
    inputEl.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') {
        e.preventDefault();
        handleAdminSend();
      }
    });

    async function handleAdminSend() {
      const text = inputEl.value.trim();
      if (!text) return;
      inputEl.value = '';

      // User Bubble
      const userMsg = document.createElement('div');
      userMsg.className = 'aic-msg user';
      userMsg.innerHTML = `<div class="aic-msg-content">${escapeHTML(text)}</div>`;
      bodyEl.appendChild(userMsg);
      bodyEl.scrollTop = bodyEl.scrollHeight;

      // Loading Bot Bubble
      const botMsg = document.createElement('div');
      botMsg.className = 'aic-msg bot';
      botMsg.innerHTML = `<div class="aic-msg-content"><i class="fa fa-spinner fa-spin"></i> Processing telemetry & analytics...</div>`;
      bodyEl.appendChild(botMsg);
      bodyEl.scrollTop = bodyEl.scrollHeight;

      try {
        const token = localStorage.getItem('admin_token') || localStorage.getItem('superadmin_token');
        const res = await fetch('/api/ai/admin/copilot', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': token ? `Bearer ${token}` : ''
          },
          body: JSON.stringify({ message: text })
        });
        const data = await res.json();
        if (data.success) {
          botMsg.querySelector('.aic-msg-content').innerHTML = formatMarkdown(data.reply);
        } else {
          botMsg.querySelector('.aic-msg-content').innerHTML = `<span style="color:#ef4444;">${data.message || 'Error occurred.'}</span>`;
        }
      } catch (err) {
        botMsg.querySelector('.aic-msg-content').innerHTML = `<span style="color:#ef4444;">Network error: ${err.message}</span>`;
      }
      bodyEl.scrollTop = bodyEl.scrollHeight;
    }

    // 4. Attach Product Form AI Auto-Fill Button if on product-form.html
    initProductFormAutoFill();

    // 5. Attach Inquiry Scoring Modal Hook
    initInquiryLeadScoring();
  }

  // -------------------------------------------------------------
  // Feature: 1-Click Product Form Auto-Fill
  // -------------------------------------------------------------
  function initProductFormAutoFill() {
    const pageHeader = document.querySelector('.page-header');
    const machineForm = document.getElementById('machine-form');
    if (!pageHeader || !machineForm) return;

    // Add "✨ AI Auto-Fill" button to header
    const btnAutoFill = document.createElement('button');
    btnAutoFill.type = 'button';
    btnAutoFill.className = 'btn-primary';
    btnAutoFill.style.background = 'linear-gradient(135deg, #f89d13 0%, #b45309 100%)';
    btnAutoFill.style.color = '#0f172a';
    btnAutoFill.style.fontWeight = '700';
    btnAutoFill.style.border = 'none';
    btnAutoFill.innerHTML = `<i class="fa fa-magic"></i> <span>✨ AI Auto-Fill with Spec Sheet</span>`;
    btnAutoFill.title = 'Paste raw machinery text or specs to automatically populate the entire form';

    const actionsWrap = pageHeader.querySelector('.page-actions') || pageHeader;
    actionsWrap.appendChild(btnAutoFill);

    const modal = document.getElementById('aic-autofill-modal');
    const closeBtn = document.getElementById('aic-autofill-close');
    const cancelBtn = document.getElementById('aic-autofill-cancel');
    const submitBtn = document.getElementById('aic-autofill-submit');
    const textArea = document.getElementById('aic-autofill-input');

    function toggleModal() {
      modal.classList.toggle('active');
      if (modal.classList.contains('active')) {
        setTimeout(() => textArea.focus(), 200);
      }
    }

    btnAutoFill.addEventListener('click', toggleModal);
    closeBtn.addEventListener('click', toggleModal);
    cancelBtn.addEventListener('click', toggleModal);

    submitBtn.addEventListener('click', async () => {
      const rawText = textArea.value.trim();
      if (!rawText) {
        alert('Please paste some machine specs or text first.');
        return;
      }

      submitBtn.disabled = true;
      submitBtn.innerHTML = `<i class="fa fa-spinner fa-spin"></i> Extracting Specifications...`;

      try {
        const token = localStorage.getItem('admin_token') || localStorage.getItem('superadmin_token');
        const res = await fetch('/api/ai/parse-product', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': token ? `Bearer ${token}` : ''
          },
          body: JSON.stringify({ rawText })
        });

        const data = await res.json();
        if (data.success && data.data) {
          populateFormWithAI(data.data);
          toggleModal();
          textArea.value = '';
          if (window.AdminCore && AdminCore.toast) {
            AdminCore.toast('✨ AI parsed specifications and filled form successfully!');
          } else {
            alert('Machine Form Auto-Filled Successfully!');
          }
        } else {
          alert(data.message || 'Failed to parse text.');
        }
      } catch (err) {
        alert('AI Parse Error: ' + err.message);
      } finally {
        submitBtn.disabled = false;
        submitBtn.innerHTML = `<i class="fa fa-magic"></i> Extract & Auto-Fill Form`;
      }
    });

    function populateFormWithAI(d) {
      if (d.name) document.getElementById('input-name').value = d.name;
      if (d.make) document.getElementById('input-make').value = d.make;
      if (d.model) document.getElementById('input-model').value = d.model;
      if (d.year) document.getElementById('input-year').value = d.year;
      if (d.tonnage) document.getElementById('input-tonnage').value = d.tonnage;
      if (d.condition) document.getElementById('input-condition').value = d.condition;
      if (d.priceText && document.getElementById('input-price-text')) {
        document.getElementById('input-price-text').value = d.priceText;
      }

      // Location
      if (d.location) {
        const locSelect = document.getElementById('input-location');
        if (locSelect) {
          for (let opt of locSelect.options) {
            if (opt.value.toLowerCase().includes(d.location.toLowerCase()) || d.location.toLowerCase().includes(opt.value.toLowerCase())) {
              locSelect.value = opt.value;
              break;
            }
          }
        }
      }

      // Section & Category
      if (d.section) {
        const secSelect = document.getElementById('input-section');
        if (secSelect) {
          secSelect.value = d.section;
          secSelect.dispatchEvent(new Event('change'));
        }
      }

      if (d.category) {
        const catSelect = document.getElementById('input-category');
        if (catSelect) {
          catSelect.value = d.category;
        }
      }

      // Specs Rows
      if (d.specs && Array.isArray(d.specs) && d.specs.length > 0) {
        const container = document.getElementById('dynamic-specs-container');
        if (container) {
          container.innerHTML = '';
          d.specs.forEach(s => {
            const row = document.createElement('div');
            row.className = 'spec-row';
            row.style.display = 'grid';
            row.style.gridTemplateColumns = '1fr 1fr 40px';
            row.style.gap = '10px';
            row.style.marginBottom = '10px';
            row.innerHTML = `
              <input type="text" class="form-control spec-key" value="${escapeHTML(s.label)}" required>
              <input type="text" class="form-control spec-val" value="${escapeHTML(s.val)}" required>
              <button type="button" class="btn-danger btn-sm" onclick="this.closest('.spec-row').remove();" title="Delete Row" style="display:flex;align-items:center;justify-content:center;">
                <i class="fa fa-trash"></i>
              </button>
            `;
            container.appendChild(row);
          });
        }
      }
    }
  }

  // -------------------------------------------------------------
  // Feature: Inquiry Lead Scoring & Smart WhatsApp Reply
  // -------------------------------------------------------------
  function initInquiryLeadScoring() {
    // Expose robust global helpers for inquiries page table
    async function executeInquiryScore(inquiryData) {
      const modal = document.getElementById('aic-inquiry-modal');
      const body = document.getElementById('aic-inquiry-body');
      const waBtn = document.getElementById('aic-inquiry-copy-wa');
      const closeBtn = document.getElementById('aic-inquiry-close') || (modal ? modal.querySelector('.aic-close-btn') : null);
      const doneBtn = document.getElementById('aic-inquiry-done') || (modal ? modal.querySelector('.btn-secondary') : null);

      if (!modal || !body) return;

      // Handle ID string or object payload seamlessly
      let inq = inquiryData;
      if (typeof inq === 'string') {
        let found = (window.allInquiries || []).find(x => String(x.id) === String(inq));
        if (!found) {
          try {
            const resInq = await fetch('/api/inquiries');
            const inqData = await resInq.json();
            if (inqData.success && Array.isArray(inqData.inquiries)) {
              window.allInquiries = inqData.inquiries;
              found = inqData.inquiries.find(x => String(x.id) === String(inq));
            }
          } catch (_) {}
        }
        inq = found || { id: inquiryData, name: 'Customer Inquiry' };
      }

      modal.style.display = 'flex';
      modal.classList.add('active');
      body.innerHTML = `
        <div style="text-align: center; padding: 40px 20px;">
          <i class="fa fa-spinner fa-spin" style="font-size: 28px; color: var(--aic-gold);"></i>
          <div style="margin-top: 14px; font-weight: 700; color: #fff; font-size: 14px;">Analyzing inquiry with Dalal AI Lead Engine...</div>
          <div style="margin-top: 6px; font-size: 12px; color: var(--aic-text-muted);">Scoring buyer intent &amp; generating smart WhatsApp draft</div>
        </div>
      `;

      const closeModal = () => {
        modal.classList.remove('active');
        modal.style.display = 'none';
      };

      if (closeBtn) closeBtn.onclick = closeModal;
      if (doneBtn) doneBtn.onclick = closeModal;
      modal.onclick = (e) => {
        if (e.target === modal) closeModal();
      };

      try {
        const token = (window.AdminCore && window.AdminCore.getToken && window.AdminCore.getToken()) ||
                      localStorage.getItem('admin_token') ||
                      localStorage.getItem('superadmin_token') || '';

        const res = await fetch('/api/ai/score-inquiry', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': token ? `Bearer ${token}` : ''
          },
          body: JSON.stringify({ inquiry: inq })
        });
        const data = await res.json();
        if (data.success && data.analysis) {
          const a = data.analysis;
          const scoreClass = a.leadScore === 'HOT' ? 'aic-score-hot' : a.leadScore === 'WARM' ? 'aic-score-warm' : 'aic-score-general';
          const scoreIcon = a.leadScore === 'HOT' ? '🔥' : a.leadScore === 'WARM' ? '⚡' : '📋';

          let matchedHtml = '';
          if (a.matchedMachines && a.matchedMachines.length > 0) {
            matchedHtml = `
              <div style="margin-top: 14px;">
                <div style="font-size: 11px; font-weight: 800; color: var(--aic-gold); margin-bottom: 8px; text-transform: uppercase; letter-spacing: 0.5px;">RECOMMENDED CATALOG MATCHES:</div>
                ${a.matchedMachines.map(m => `
                  <div style="background: rgba(30, 41, 59, 0.75); border: 1px solid var(--aic-border); border-radius: 8px; padding: 10px 14px; margin-bottom: 8px; font-size: 13px; display: flex; justify-content: space-between; align-items: center; gap: 14px;">
                    <div style="flex: 1; min-width: 0;">
                      <div style="color: #ffffff; font-weight: 700; font-size: 13px; line-height: 1.4; word-break: break-word;">${escapeHTML(m.name)}</div>
                      <div style="color: #94a3b8; font-size: 11.5px; margin-top: 3px;">
                        <i class="fa fa-map-marker" style="color: var(--aic-gold); margin-right: 4px;"></i>${escapeHTML(m.location || 'Pune Yard')}
                        ${m.tonnage ? ` &bull; <span style="color:#e2e8f0; font-weight:600;">${m.tonnage} Ton</span>` : ''}
                      </div>
                    </div>
                    <a href="/new/dalalmachine/product.html?id=${m.id}" target="_blank" style="background: rgba(248, 157, 19, 0.15); color: var(--aic-gold); border: 1px solid rgba(248, 157, 19, 0.35); padding: 6px 14px; border-radius: 6px; font-size: 11.5px; text-decoration: none; font-weight: 700; white-space: nowrap; flex-shrink: 0; display: inline-flex; align-items: center; gap: 4px;">View Specs &rarr;</a>
                  </div>
                `).join('')}
              </div>
            `;
          }

          body.innerHTML = `
            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 14px; border-bottom: 1px solid var(--aic-border); padding-bottom: 12px; gap: 12px; flex-wrap: wrap;">
              <div>
                <div style="font-size: 16px; font-weight: 700; color: #fff;">${escapeHTML(inq.name || 'Inquiry')}</div>
                <div style="font-size: 12px; color: var(--aic-text-muted); margin-top: 2px;">
                  ${escapeHTML(inq.company || 'Private Buyer')} &bull; 
                  <span style="color: #cbd5e1; font-weight: 600;">${escapeHTML(inq.phone || inq.email || 'No Direct Phone')}</span>
                </div>
              </div>
              <div class="aic-score-badge ${scoreClass}" style="font-size: 12px; font-weight: 800; padding: 6px 14px; border-radius: 9999px;">
                ${scoreIcon} ${a.leadScore} LEAD
              </div>
            </div>

            <div style="background: rgba(248, 157, 19, 0.08); border: 1px solid rgba(248, 157, 19, 0.25); border-radius: 8px; padding: 12px 14px; margin-bottom: 14px; font-size: 12.5px; line-height: 1.5; color: #f1f5f9;">
              <strong style="color: var(--aic-gold); display: block; margin-bottom: 4px; font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px;">AI Lead Procurement Analysis:</strong>
              ${escapeHTML(a.scoreReason)}
            </div>

            ${matchedHtml}

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
          `;

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

          const phoneNum = (inq.phone || '').replace(/[^0-9]/g, '');
          if (waBtn) {
            waBtn.onclick = () => {
              const textEl = document.getElementById('aic-wa-reply-text');
              const text = encodeURIComponent(textEl ? textEl.value : a.suggestedWhatsAppReply);
              const url = phoneNum ? `https://wa.me/${phoneNum}?text=${text}` : `https://wa.me/?text=${text}`;
              window.open(url, '_blank');
            };
          }
        } else {
          body.innerHTML = `<div style="color:#ef4444; padding:20px;">Analysis failed: ${data.message || 'Unknown error'}</div>`;
        }
      } catch (err) {
        body.innerHTML = `<div style="color:#ef4444; padding:20px;">Error: ${err.message}</div>`;
      }
    }

    // Expose under all common alias names for fail-safe compatibility
    window.openAIInquiryAnalysis = executeInquiryScore;
    window.openAILeadScore = executeInquiryScore;
    window.handleAIInquiryClick = executeInquiryScore;
  }

  function escapeHTML(str) {
    if (!str) return '';
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  function formatMarkdown(text) {
    if (!text) return '';
    let escaped = escapeHTML(text);
    escaped = escaped.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    escaped = escaped.replace(/•\s+(.*?)(?=\n|$)/g, '<li>$1</li>');
    escaped = escaped.replace(/(<li>.*?<\/li>)/gs, '<ul>$1</ul>');
    escaped = escaped.replace(/###\s+(.*?)(?=\n|$)/g, '<h3 style="color:#f89d13; margin:8px 0 4px;">$1</h3>');
    escaped = escaped.replace(/\n\n/g, '<br><br>');
    escaped = escaped.replace(/\n/g, '<br>');
    return escaped;
  }
})();
