/**
 * Dalal Machine Tools - Enterprise AI Machinery Sales & Technical Advisor
 * Frontend Controller with Multi-Language Support (English Default)
 * Author: Suyash Shinde | Version: 3.0
 */

(function () {
  'use strict';

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initDalalAI);
  } else {
    initDalalAI();
  }

  function initDalalAI() {
    const el = document.getElementById('dai-widget-container');
    if (el) el.remove();

    // Supported Languages Config
    const LANGUAGES = {
      en: {
        code: 'en',
        name: 'English',
        flag: '🇬🇧',
        welcome: `Welcome to **Dalal Machine Tools Agency Pvt. Ltd.**! I am your AI Machinery Sales & Technical Advisor.\n\nI can assist you in finding heavy metal forming machinery (Hot Forging Presses, Knuckle Joint Coining, C-Frame, Hydraulic Deep Draw) and heavy metal cutting machine tools (Heavy Duty Lathes, Horizontal Boring, Gear Hobbing), calculate High Seas import duty savings, or schedule an inspection at our Pune yard.\n\nWhat machinery capacity, make, or application are you looking for?`,
        placeholder: 'Type machinery requirement (e.g. 2000T press in Pune)...',
        chips: [
          'Search 1000T - 2500T Forging Press',
          'High Seas Duty & Tax Savings',
          'Live Stock at Pune Yard',
          'OMPI Clutch & Brake Retrofit'
        ],
        viewSpecs: 'View Specs',
        getQuote: 'Get Quote',
        langSwitched: 'Language switched to **English**.'
      },
      hinglish: {
        code: 'hinglish',
        name: 'Hinglish',
        flag: '🇮🇳',
        welcome: `Namaste! Main **Dalal Machine Tools** ka AI Machinery Advisor hoon.\n\nMain aapki factory requirement ke mutabiq best metal forming (Hot Forging, Coining, C-Frame, Hydraulic) aur cutting machines (Lathes, Horizontal Boring, Gear Hobbing) suggest kar sakta hoon.\n\nAapko kis tonnage, make ya machine type ki talash hai?`,
        placeholder: 'Requirement likhein (e.g. 2000T press in Pune)...',
        chips: [
          'Find 1000T - 2500T Forging Press',
          'High Seas Duty & Tax Savings',
          'Pune Stock Live Trials',
          'OMPI Clutch & Brake Retrofit'
        ],
        viewSpecs: 'Specs Dekhein',
        getQuote: 'Quote Paayein',
        langSwitched: 'Language switched to **Hinglish**.'
      },
      hi: {
        code: 'hi',
        name: 'हिन्दी (Hindi)',
        flag: '🇮🇳',
        welcome: `नमस्ते! मैं **दलाल मशीन टूल्स** का AI मशीनरी एडवाइजर हूँ।\n\nमैं आपकी औद्योगिक आवश्यकता के अनुसार मेटल फॉर्मिंग (हॉट फोर्जिंग प्रेस, सी-फ्रेम, कॉइनिंग, हाइड्रोलिक) और मेटल कटिंग मशीनरी (लेथ, बोरिंग, गियर हॉबिंग) खोजने में मदद कर सकता हूँ।\n\nआपको किस प्रकार की मशीन या क्षमता की आवश्यकता है?`,
        placeholder: 'अपनी आवश्यकता यहाँ लिखें (उदा. 2000T प्रेस)...',
        chips: [
          '1000T - 2500T फोर्जिंग प्रेस',
          'हाई सीज कस्टम ड्यूटी बचत',
          'पुणे यार्ड उपलब्ध स्टॉक',
          'व्हाट्सएप कोटेशन'
        ],
        viewSpecs: 'स्पेक्स देखें',
        getQuote: 'कोटेशन पाएँ',
        langSwitched: 'भाषा बदलकर **हिन्दी** कर दी गई है।'
      },
      gu: {
        code: 'gu',
        name: 'ગુજરાતી (Gujarati)',
        flag: '🇮🇳',
        welcome: `નમસ્તે! હું **દલાલ મશીન ટુલ્સ**નો AI મશીનરી એડવાઇઝર છું.\n\nહું આપની ફેક્ટરી જરૂરિયાત મુજબ યોગ્ય મેટલ ફોર્મિંગ અને કટિંગ મશીનો (ફોર્જિંગ પ્રેસ, સી-ફ્રેમ, લેથ, હોરિઝોન્ટલ બોરિંગ) શોધવામાં મદદ કરી શકું છું.\n\nઆપને કઈ ક્ષમતા (ટનેજ) અથવા મશીનની જરૂર છે?`,
        placeholder: 'જરૂરિયાત અહીં લખો (દા.ત. 2000T પ્રેસ)...',
        chips: [
          '1000T - 2500T ફોર્જિંગ પ્રેસ',
          'હાઇ સીઝ કસ્ટમ ડ્યુટી બચત',
          'પુણે યાર્ડ લાઇવ સ્ટોક',
          'વોટ્સએપ કોટેશન'
        ],
        viewSpecs: 'સ્પેક્સ જુઓ',
        getQuote: 'કોટેશન મેળવો',
        langSwitched: 'ભાષા બદલીને **ગુજરાતી** કરવામાં આવી છે.'
      },
      mr: {
        code: 'mr',
        name: 'मराठी (Marathi)',
        flag: '🇮🇳',
        welcome: `नमस्कार! मी **दलाल मशीन टूल्स** चा AI मशीनरी सल्लागार आहे.\n\nमी आपल्या कारखान्याच्या गरजेनुसार मेटल फॉर्मिंग आणि मेटल कटिंग मशीन्स शोधण्यात मदत करू शकतो.\n\nआपल्याला कोणत्या प्रकारच्या मशीनची किंवा क्षमतेची आवश्यकता आहे?`,
        placeholder: 'आपली गरज येथे टाईप करा (उदा. 2000T प्रेस)...',
        chips: [
          '1000T - 2500T फोर्जिंग प्रेस',
          'हाय सीज कस्टम्स बचत',
          'पुणे यार्ड उपलब्ध स्टॉक',
          'व्हॉट्सॲप कोटेशन'
        ],
        viewSpecs: 'माहिती पहा',
        getQuote: 'कोटेशन मिळवा',
        langSwitched: 'भाषा बदलून **मराठी** करण्यात आली आहे.'
      }
    };

    const config = {
      apiEndpoint: '/api/ai/chat',
      whatsappNumber: '919821232131',
      sessionKey: 'dalal_ai_chat_history_v3',
      langKey: 'dalal_ai_selected_lang'
    };

    let currentLang = localStorage.getItem(config.langKey) || 'en';
    let chatHistory = [];
    let isWaiting = false;

    // 1. Build and Inject DOM Elements
    const root = document.createElement('div');
    root.id = 'dai-widget-container';
    root.innerHTML = `
      <!-- Floating Trigger Button (Positioned at bottom: 84px to prevent overlapping WhatsApp at bottom: 25px) -->
      <div class="dai-launcher" id="dai-launcher" title="Chat with Dalal Machinery AI Advisor">
        <div class="dai-launcher-icon-wrap">
          <div class="dai-pulse-ring"></div>
          <i class="fa fa-magic"></i>
        </div>
        <div class="dai-launcher-text">
          <span class="dai-launcher-title">Machinery AI Advisor</span>
          <span class="dai-launcher-sub"><span class="dai-sub-dot"></span> Online 24/7 RFQ</span>
        </div>
      </div>

      <!-- Floating Chat Widget -->
      <div class="dai-widget" id="dai-widget" role="dialog" aria-label="Dalal AI Machinery Sales Advisor">
        <!-- Header -->
        <div class="dai-header">
          <div class="dai-header-brand">
            <div class="dai-avatar">
              <i class="fa fa-robot"></i>
            </div>
            <div class="dai-header-meta">
              <h4>Dalal AI Advisor <i class="fa fa-check-circle dai-verified-icon" title="Verified Advisor"></i></h4>
              <div class="dai-status-badge">
                <span class="dai-status-dot"></span>
                <span>Live Sourcing Specialist</span>
              </div>
            </div>
          </div>
          <div class="dai-header-actions">
            <!-- Language Switcher Button -->
            <button class="dai-lang-picker-btn" id="dai-lang-picker-btn" title="Choose Language / भाषा बदलें">
              <span id="dai-lang-flag">🇬🇧</span> <span id="dai-lang-name">EN</span> <i class="fa fa-angle-down"></i>
            </button>
            <button class="dai-icon-btn" id="dai-btn-clear" title="Restart / Clear Chat">
              <i class="fa fa-trash"></i>
            </button>
            <button class="dai-icon-btn" id="dai-btn-close" title="Minimize Chat">
              <i class="fa fa-times"></i>
            </button>
          </div>

          <!-- Language Dropdown Menu -->
          <div class="dai-lang-dropdown" id="dai-lang-dropdown">
            <button class="dai-lang-opt" data-lang="en">🇬🇧 English</button>
            <button class="dai-lang-opt" data-lang="hinglish">🇮🇳 Hinglish</button>
            <button class="dai-lang-opt" data-lang="hi">🇮🇳 हिन्दी (Hindi)</button>
            <button class="dai-lang-opt" data-lang="gu">🇮🇳 ગુજરાતી (Gujarati)</button>
            <button class="dai-lang-opt" data-lang="mr">🇮🇳 मराठी (Marathi)</button>
          </div>
        </div>

        <!-- Chat Messages -->
        <div class="dai-messages" id="dai-messages"></div>

        <!-- Quick Chips Bar -->
        <div class="dai-chips-wrap" id="dai-chips-wrap"></div>

        <!-- Input Bar -->
        <div class="dai-input-bar">
          <input type="text" id="dai-input" class="dai-input" placeholder="${LANGUAGES[currentLang].placeholder}" autocomplete="off">
          <button id="dai-btn-send" class="dai-btn-send" title="Send Inquiry">
            <i class="fa fa-paper-plane"></i>
          </button>
        </div>
      </div>
    `;
    document.body.appendChild(root);

    // 2. Select Elements
    const launcher = document.getElementById('dai-launcher');
    const widget = document.getElementById('dai-widget');
    const closeBtn = document.getElementById('dai-btn-close');
    const clearBtn = document.getElementById('dai-btn-clear');
    const messagesEl = document.getElementById('dai-messages');
    const chipsWrap = document.getElementById('dai-chips-wrap');
    const inputEl = document.getElementById('dai-input');
    const sendBtn = document.getElementById('dai-btn-send');
    const langPickerBtn = document.getElementById('dai-lang-picker-btn');
    const langDropdown = document.getElementById('dai-lang-dropdown');
    const langFlagEl = document.getElementById('dai-lang-flag');
    const langNameEl = document.getElementById('dai-lang-name');

    updateHeaderLang();

    // 3. Restore History or Show Welcome Greeting with Language Selector
    try {
      const stored = sessionStorage.getItem(config.sessionKey);
      if (stored) {
        chatHistory = JSON.parse(stored);
      }
    } catch (e) {
      chatHistory = [];
    }

    if (chatHistory.length > 0) {
      renderAllMessages();
    } else {
      showInitialGreetingWithLanguageSelector();
    }

    renderChips(LANGUAGES[currentLang].chips);

    // 4. Event Listeners
    launcher.addEventListener('click', () => {
      widget.classList.toggle('dai-open');
      if (widget.classList.contains('dai-open')) {
        setTimeout(() => inputEl.focus(), 250);
        scrollToBottom();
      }
    });

    closeBtn.addEventListener('click', () => {
      widget.classList.remove('dai-open');
    });

    // Language Dropdown Toggle
    langPickerBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      langDropdown.classList.toggle('show');
    });

    document.addEventListener('click', (e) => {
      if (!langPickerBtn.contains(e.target) && !langDropdown.contains(e.target)) {
        langDropdown.classList.remove('show');
      }
    });

    // Language Options Click inside dropdown
    document.querySelectorAll('.dai-lang-opt').forEach(opt => {
      opt.addEventListener('click', () => {
        const selectedCode = opt.getAttribute('data-lang');
        switchLanguage(selectedCode);
        langDropdown.classList.remove('show');
      });
    });

    clearBtn.addEventListener('click', () => {
      if (confirm('Do you want to restart this conversation? / क्या आप चैट रीस्टार्ट करना चाहते हैं?')) {
        chatHistory = [];
        sessionStorage.removeItem(config.sessionKey);
        messagesEl.innerHTML = '';
        showInitialGreetingWithLanguageSelector();
      }
    });

    sendBtn.addEventListener('click', handleUserSend);

    inputEl.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        handleUserSend();
      }
    });

    // 5. Initial Greeting with Prominent Language Selector Card
    function showInitialGreetingWithLanguageSelector() {
      // First card: Language Choice Buttons
      const langCard = document.createElement('div');
      langCard.className = 'dai-lang-card';
      langCard.innerHTML = `
        <div class="dai-lang-card-header">
          <i class="fa fa-globe"></i> Select Language / भाषा चुनें:
        </div>
        <div class="dai-lang-grid">
          <button type="button" class="dai-lang-btn ${currentLang === 'en' ? 'active' : ''}" data-lang="en">🇬🇧 English</button>
          <button type="button" class="dai-lang-btn ${currentLang === 'hinglish' ? 'active' : ''}" data-lang="hinglish">🇮🇳 Hinglish</button>
          <button type="button" class="dai-lang-btn ${currentLang === 'hi' ? 'active' : ''}" data-lang="hi">🇮🇳 हिन्दी</button>
          <button type="button" class="dai-lang-btn ${currentLang === 'gu' ? 'active' : ''}" data-lang="gu">🇮🇳 ગુજરાતી</button>
          <button type="button" class="dai-lang-btn ${currentLang === 'mr' ? 'active' : ''}" data-lang="mr">🇮🇳 मराठी</button>
        </div>
      `;

      // Attach clicks to language card buttons
      langCard.querySelectorAll('.dai-lang-btn').forEach(btn => {
        btn.addEventListener('click', () => {
          const langCode = btn.getAttribute('data-lang');
          switchLanguage(langCode);
        });
      });

      messagesEl.appendChild(langCard);

      // Followed by Welcome greeting in current language (English default)
      appendBotMessage(
        LANGUAGES[currentLang].welcome,
        [],
        LANGUAGES[currentLang].chips
      );
    }

    // 6. Language Switcher Handler
    function switchLanguage(langCode) {
      if (!LANGUAGES[langCode]) return;
      currentLang = langCode;
      localStorage.setItem(config.langKey, currentLang);
      updateHeaderLang();

      inputEl.placeholder = LANGUAGES[currentLang].placeholder;
      renderChips(LANGUAGES[currentLang].chips);

      // Update active state in any existing language cards
      document.querySelectorAll('.dai-lang-btn').forEach(btn => {
        btn.classList.toggle('active', btn.getAttribute('data-lang') === currentLang);
      });

      // Post notification bubble
      appendBotMessage(
        LANGUAGES[currentLang].langSwitched + '\n\n' + LANGUAGES[currentLang].welcome,
        [],
        LANGUAGES[currentLang].chips
      );
    }

    function updateHeaderLang() {
      const cfg = LANGUAGES[currentLang] || LANGUAGES['en'];
      if (langFlagEl) langFlagEl.textContent = cfg.flag;
      if (langNameEl) langNameEl.textContent = currentLang.toUpperCase().slice(0, 3);
    }

    // 7. User Send Logic
    async function handleUserSend() {
      const text = inputEl.value.trim();
      if (!text || isWaiting) return;

      inputEl.value = '';
      appendUserMessage(text);
      isWaiting = true;
      sendBtn.disabled = true;

      showTypingIndicator();

      try {
        const response = await fetch(config.apiEndpoint, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            message: text,
            history: chatHistory.slice(-6),
            language: currentLang
          })
        });

        removeTypingIndicator();

        if (response.ok) {
          const data = await response.json();
          if (data.success) {
            appendBotMessage(data.reply, data.matchedMachines, data.chips);
          } else {
            appendBotMessage(data.message || 'Apologies, could not fetch response. Please try again.');
          }
        } else {
          fallbackLocalMatching(text);
        }
      } catch (err) {
        removeTypingIndicator();
        console.warn('[Dalal AI] API unreachable, executing local fallback engine:', err);
        fallbackLocalMatching(text);
      } finally {
        isWaiting = false;
        sendBtn.disabled = false;
        setTimeout(() => inputEl.focus(), 150);
      }
    }

    // 8. Local Fallback Engine if Offline
    function fallbackLocalMatching(query) {
      let matched = [];
      if (window.DALAL_MACHINES && Array.isArray(window.DALAL_MACHINES)) {
        const q = query.toLowerCase();
        matched = window.DALAL_MACHINES.filter(m => {
          return (m.name && m.name.toLowerCase().includes(q)) ||
                 (m.category && m.category.toLowerCase().includes(q)) ||
                 (m.make && m.make.toLowerCase().includes(q));
        }).slice(0, 3);
      }

      let reply = `Regarding your inquiry for **"${query}"**, our sales specialists at Dalal Machine Tools can prepare an official CIF Nhava Sheva or Ex-Pune Yard proposal with live inspection video records.\n\nPlease connect directly on WhatsApp (+91 9821232131) for immediate pricing.`;
      
      if (matched.length > 0) {
        reply = `Here are the top machines verified in our current inventory matching your requirement:`;
      }

      appendBotMessage(reply, matched, LANGUAGES[currentLang].chips);
    }

    // 9. Message Appending & Rendering
    function appendUserMessage(text) {
      const msg = {
        role: 'user',
        text: text,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      };
      chatHistory.push(msg);
      saveHistory();

      const row = document.createElement('div');
      row.className = 'dai-msg-row dai-user-row';
      row.innerHTML = `
        <div class="dai-msg-bubble">
          ${escapeHTML(text)}
          <div class="dai-msg-time">${msg.timestamp}</div>
        </div>
      `;
      messagesEl.appendChild(row);
      scrollToBottom();
    }

    function appendBotMessage(text, matchedMachines = [], chips = []) {
      const msg = {
        role: 'bot',
        text: text,
        matchedMachines: matchedMachines || [],
        chips: chips || [],
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      };
      chatHistory.push(msg);
      saveHistory();

      const row = document.createElement('div');
      row.className = 'dai-msg-row dai-bot-row';

      let cardsHtml = '';
      if (matchedMachines && matchedMachines.length > 0) {
        cardsHtml = matchedMachines.map(m => renderProductCard(m)).join('');
      }

      row.innerHTML = `
        <div class="dai-msg-avatar">
          <i class="fa fa-cube"></i>
        </div>
        <div class="dai-msg-bubble">
          <div>${formatMarkdown(text)}</div>
          ${cardsHtml}
          <div class="dai-msg-time">${msg.timestamp}</div>
        </div>
      `;
      messagesEl.appendChild(row);

      if (chips && chips.length > 0) {
        renderChips(chips);
      }
      scrollToBottom();
    }

    function renderProductCard(m) {
      const id = m.id || 'MCH';
      const name = m.name || 'Industrial Machine';
      const tonnage = m.tonnage ? `${m.tonnage} Tons` : 'Heavy Duty';
      const location = m.location || 'Pune Yard';
      const img = m.image || 'images/dalal/hero_forging_press.jpg';
      const pdpUrl = `product.html?id=${id}`;
      const waText = encodeURIComponent(`Hello Dalal Machines, I am interested in [${id}] ${name} (${location}). Please share technical quote and video inspection.`);
      const waUrl = `https://wa.me/${config.whatsappNumber}?text=${waText}`;

      const cfg = LANGUAGES[currentLang] || LANGUAGES['en'];

      return `
        <div class="dai-product-card">
          <img src="${img}" alt="${escapeHTML(name)}" class="dai-product-thumb" onerror="this.src='images/dalal/hero_forging_press.jpg';">
          <div class="dai-product-title">${escapeHTML(name)}</div>
          <div class="dai-product-badges">
            <span class="dai-badge dai-badge-gold"><i class="fa fa-tachometer"></i> ${tonnage}</span>
            <span class="dai-badge dai-badge-loc"><i class="fa fa-map-marker"></i> ${location}</span>
          </div>
          <div class="dai-product-actions">
            <a href="${pdpUrl}" class="dai-btn-card-pdp" target="_blank">
              <i class="fa fa-external-link"></i> ${cfg.viewSpecs}
            </a>
            <a href="/api/products/${id}/spec-sheet" class="dai-btn-card-pdp" style="background:#0f172a; border-color:#f89d13; color:#f89d13;" target="_blank" title="Official 1-Click PDF Spec Sheet">
              <i class="fa fa-file-pdf-o"></i> PDF
            </a>
            <a href="${waUrl}" class="dai-btn-card-wa" target="_blank">
              <i class="fa fa-whatsapp"></i> ${cfg.getQuote}
            </a>
          </div>
        </div>
      `;
    }

    function renderChips(chips) {
      chipsWrap.innerHTML = '';
      if (!chips || !chips.length) return;
      chips.forEach(chipText => {
        const chip = document.createElement('button');
        chip.type = 'button';
        chip.className = 'dai-chip';
        chip.textContent = chipText;
        chip.addEventListener('click', () => {
          inputEl.value = chipText;
          handleUserSend();
        });
        chipsWrap.appendChild(chip);
      });
    }

    function renderAllMessages() {
      messagesEl.innerHTML = '';
      chatHistory.forEach(msg => {
        if (msg.role === 'user') {
          const row = document.createElement('div');
          row.className = 'dai-msg-row dai-user-row';
          row.innerHTML = `
            <div class="dai-msg-bubble">
              ${escapeHTML(msg.text)}
              <div class="dai-msg-time">${msg.timestamp || ''}</div>
            </div>
          `;
          messagesEl.appendChild(row);
        } else {
          const row = document.createElement('div');
          row.className = 'dai-msg-row dai-bot-row';
          let cardsHtml = '';
          if (msg.matchedMachines && msg.matchedMachines.length > 0) {
            cardsHtml = msg.matchedMachines.map(m => renderProductCard(m)).join('');
          }
          row.innerHTML = `
            <div class="dai-msg-avatar">
              <i class="fa fa-cube"></i>
            </div>
            <div class="dai-msg-bubble">
              <div>${formatMarkdown(msg.text)}</div>
              ${cardsHtml}
              <div class="dai-msg-time">${msg.timestamp || ''}</div>
            </div>
          `;
          messagesEl.appendChild(row);
        }
      });
      scrollToBottom();
    }

    function showTypingIndicator() {
      const ind = document.createElement('div');
      ind.id = 'dai-typing-indicator-row';
      ind.className = 'dai-msg-row dai-bot-row';
      ind.innerHTML = `
        <div class="dai-msg-avatar"><i class="fa fa-cube"></i></div>
        <div class="dai-typing-indicator">
          <div class="dai-dot"></div>
          <div class="dai-dot"></div>
          <div class="dai-dot"></div>
        </div>
      `;
      messagesEl.appendChild(ind);
      scrollToBottom();
    }

    function removeTypingIndicator() {
      const ind = document.getElementById('dai-typing-indicator-row');
      if (ind) ind.remove();
    }

    function scrollToBottom() {
      setTimeout(() => {
        messagesEl.scrollTop = messagesEl.scrollHeight;
      }, 50);
    }

    function saveHistory() {
      try {
        sessionStorage.setItem(config.sessionKey, JSON.stringify(chatHistory.slice(-15)));
      } catch (e) {}
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
      escaped = escaped.replace(/###\s+(.*?)(?=\n|$)/g, '<div style="font-weight:700; color:#f89d13; margin:6px 0;">$1</div>');
      escaped = escaped.replace(/\n\n/g, '<br><br>');
      escaped = escaped.replace(/\n/g, '<br>');
      return escaped;
    }
  }
})();
