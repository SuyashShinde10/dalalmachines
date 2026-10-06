/**
 * Dalal Machines - Modern Industrial UI Script
 * Controls Hero Slider, Catalog Tabs Filtering, KPI Counters, RFQ Modals,
 * Scroll Reveal Animations, Product Gallery Zoom, and High Seas Calculator.
 */

document.addEventListener('DOMContentLoaded', () => {
  initHeroSlider();
  initCatalogTabs();
  initKpiCounters();
  initModal();
  initRfqForm();
  initScrollReveal();
  initProductGallery();
  initHighSeasCalculator();
});

/* ==========================================================================
   1. HERO SLIDER WITH KINETIC TEXT REVEAL
   ========================================================================== */
function initHeroSlider() {
  const slides = document.querySelectorAll('.hero-slide');
  const prevBtn = document.querySelector('.slider-prev');
  const nextBtn = document.querySelector('.slider-next');
  let currentSlide = 0;
  let slideInterval;

  if (!slides.length) return;

  function showSlide(index) {
    slides.forEach((slide, i) => {
      const isCurrent = (i === index);
      slide.classList.toggle('active', isCurrent);
      if (isCurrent) {
        const pill = slide.querySelector('.hero-pill');
        const title = slide.querySelector('.hero-title');
        const text = slide.querySelector('.hero-text');
        const actions = slide.querySelector('.hero-actions');
        
        [pill, title, text, actions].forEach(el => {
          if (el) {
            el.style.animation = 'none';
            el.offsetHeight; /* trigger reflow */
          }
        });

        if (pill) pill.style.animation = 'kineticSlideUp 0.7s cubic-bezier(0.16, 1, 0.3, 1) forwards';
        if (title) title.style.animation = 'kineticSlideUp 0.85s 0.1s cubic-bezier(0.16, 1, 0.3, 1) both';
        if (text) text.style.animation = 'kineticSlideUp 0.85s 0.25s cubic-bezier(0.16, 1, 0.3, 1) both';
        if (actions) actions.style.animation = 'kineticSlideUp 0.85s 0.4s cubic-bezier(0.16, 1, 0.3, 1) both';
      }
    });
  }

  function nextSlide() {
    currentSlide = (currentSlide + 1) % slides.length;
    showSlide(currentSlide);
  }

  function prevSlide() {
    currentSlide = (currentSlide - 1 + slides.length) % slides.length;
    showSlide(currentSlide);
  }

  if (nextBtn && prevBtn) {
    nextBtn.addEventListener('click', () => {
      nextSlide();
      resetInterval();
    });

    prevBtn.addEventListener('click', () => {
      prevSlide();
      resetInterval();
    });
  }

  function startInterval() {
    slideInterval = setInterval(nextSlide, 7000);
  }

  function resetInterval() {
    clearInterval(slideInterval);
    startInterval();
  }

  startInterval();

  // Pause ticker on mouse hover
  const tickerTrack = document.querySelector('.ticker-track');
  const tickerContent = document.querySelector('.ticker-content');
  if (tickerTrack && tickerContent) {
    tickerTrack.addEventListener('mouseenter', () => {
      tickerContent.style.animationPlayState = 'paused';
    });
    tickerTrack.addEventListener('mouseleave', () => {
      tickerContent.style.animationPlayState = 'running';
    });
  }
}

/* ==========================================================================
   2. CATALOG TABS FILTERING
   ========================================================================== */
function initCatalogTabs() {
  const tabButtons = document.querySelectorAll('.tab-btn');
  const machineCards = document.querySelectorAll('.machine-card');

  if (!tabButtons.length || !machineCards.length) return;

  tabButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      tabButtons.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');

      const filter = btn.getAttribute('data-filter');

      machineCards.forEach(card => {
        const category = card.getAttribute('data-category');
        if (filter === 'all' || category === filter) {
          card.style.display = 'flex';
          card.style.animation = 'fadeUpIn 0.5s ease forwards';
        } else {
          card.style.display = 'none';
        }
      });
    });
  });
}

/* ==========================================================================
   3. ANIMATED KPI COUNTERS
   ========================================================================== */
function initKpiCounters() {
  const counters = document.querySelectorAll('.kpi-num');
  let animated = false;

  if (!counters.length) return;

  function runCounters() {
    counters.forEach(counter => {
      const target = parseInt(counter.getAttribute('data-target'), 10);
      const suffix = counter.getAttribute('data-suffix') || '';
      let count = 0;
      const step = Math.max(1, Math.ceil(target / 45));

      const timer = setInterval(() => {
        count += step;
        if (count >= target) {
          count = target;
          clearInterval(timer);
        }
        counter.textContent = count.toLocaleString() + suffix;
      }, 30);
    });
  }

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting && !animated) {
        animated = true;
        runCounters();
      }
    });
  }, { threshold: 0.25 });

  const kpiSection = document.querySelector('.kpi-grid');
  if (kpiSection) {
    observer.observe(kpiSection);
  }
}

/* ==========================================================================
   4. MODAL MANAGEMENT
   ========================================================================== */
function initModal() {
  const modal = document.getElementById('quote-modal');
  const closeBtn = document.querySelector('.modal-close');
  const triggers = document.querySelectorAll('[data-modal="quote-modal"]');

  if (!modal) return;

  function openModal(machineName = '') {
    modal.classList.add('active');
    document.body.style.overflow = 'hidden';
    if (machineName) {
      const select = document.getElementById('modal-machine-select');
      if (select) {
        select.value = machineName;
      }
    }
  }

  function closeModal() {
    modal.classList.remove('active');
    document.body.style.overflow = '';
  }

  triggers.forEach(trigger => {
    trigger.addEventListener('click', (e) => {
      e.preventDefault();
      const machine = trigger.getAttribute('data-machine') || '';
      openModal(machine);
    });
  });

  if (closeBtn) {
    closeBtn.addEventListener('click', closeModal);
  }

  modal.addEventListener('click', (e) => {
    if (e.target === modal) {
      closeModal();
    }
  });

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && modal.classList.contains('active')) {
      closeModal();
    }
  });

  window.openInquiryModal = openModal;
}

/* ==========================================================================
   5. RFQ FORM & WHATSAPP INTEGRATION
   ========================================================================== */
function initRfqForm() {
  const forms = document.querySelectorAll('.rfq-form');

  forms.forEach(form => {
    form.addEventListener('submit', (e) => {
      e.preventDefault();

      const name = form.querySelector('[name="name"]')?.value || 'Valued Client';
      const company = form.querySelector('[name="company"]')?.value || 'Manufacturing Firm';
      const phone = form.querySelector('[name="phone"]')?.value || '';
      const email = form.querySelector('[name="email"]')?.value || '';
      const machine = form.querySelector('[name="machine"]')?.value || 'Industrial Machinery';
      const tonnage = form.querySelector('[name="tonnage"]')?.value || 'Standard';
      const message = form.querySelector('[name="message"]')?.value || '';

      const text = encodeURIComponent(
        `*MACHINERY INQUIRY - DALAL MACHINES*\n` +
        `===================================\n` +
        `👤 *Contact Person:* ${name}\n` +
        `🏢 *Company:* ${company}\n` +
        `📞 *Phone/WhatsApp:* ${phone}\n` +
        `✉️ *Email:* ${email || 'Not provided'}\n` +
        `⚙️ *Machine Requested:* ${machine}\n` +
        `⚖️ *Tonnage / Capacity:* ${tonnage}\n` +
        `💬 *Technical Note:* ${message || 'Please provide quotation, foundation drawings, and power inspection schedule.'}\n` +
        `===================================\n` +
        `_Source: dalalmachines.com Web Portal_`
      );

      const whatsappUrl = `https://wa.me/919821232131?text=${text}`;
      window.open(whatsappUrl, '_blank');

      alert(`Thank you, ${name}! Your inquiry for ${machine} has been routed directly to Mr. Vinit Dalal and the technical sales team via WhatsApp.`);

      const modal = document.getElementById('quote-modal');
      if (modal && modal.classList.contains('active')) {
        modal.classList.remove('active');
        document.body.style.overflow = '';
      }
      form.reset();
    });
  });
}

/* ==========================================================================
   6. SCROLL REVEAL ANIMATIONS
   ========================================================================== */
function initScrollReveal() {
  const revealElements = document.querySelectorAll('.feature-card, .service-card, .machine-card, .gallery-card, .about-grid');

  if (!revealElements.length || !('IntersectionObserver' in window)) return;

  revealElements.forEach(el => {
    el.classList.add('reveal-on-scroll');
  });

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-revealed');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.15 });

  revealElements.forEach(el => observer.observe(el));
}

/* ==========================================================================
   7. PRODUCT DETAIL GALLERY THUMBNAIL SWITCHER
   ========================================================================== */
function initProductGallery() {
  const mainImageContainer = document.querySelector('.pdp-main-image');
  const thumbs = document.querySelectorAll('.pdp-thumb-item');

  if (!mainImageContainer || !thumbs.length) return;

  const imageMap = {
    0: 'assets/images/cframe_press_pune.jpg',
    1: 'assets/images/hero_forging_press.jpg',
    2: 'assets/images/ompi_clutch_brake_unit.jpg',
    3: 'assets/images/knuckle_coining_press.jpg'
  };

  thumbs.forEach((thumb, idx) => {
    thumb.addEventListener('click', () => {
      thumbs.forEach(t => t.classList.remove('active'));
      thumb.classList.add('active');

      const targetImgSrc = imageMap[idx] || imageMap[0];
      const existingImg = mainImageContainer.querySelector('img');

      if (existingImg) {
        existingImg.style.opacity = '0';
        setTimeout(() => {
          existingImg.src = targetImgSrc;
          existingImg.style.opacity = '1';
        }, 150);
      } else {
        mainImageContainer.innerHTML = `
          <img src="${targetImgSrc}" alt="Machine View" style="width:100%; height:100%; object-fit:cover; transition:opacity 0.3s ease;">
          <span class="badge badge-under-power" style="position:absolute; top:16px; left:16px;">SEEN UNDER POWER</span>
          <span class="badge badge-tonnage" style="position:absolute; bottom:16px; right:16px; font-size:15px; padding:6px 14px;">200 TON CAPACITY</span>
        `;
      }
    });
  });
}

/* ==========================================================================
   8. INTERACTIVE HIGH SEAS SAVINGS CALCULATOR
   ========================================================================== */
function initHighSeasCalculator() {
  const calcBtn = document.getElementById('btn-calc-high-seas');
  const euroInput = document.getElementById('calc-euro-input');
  const inrOutput = document.getElementById('calc-inr-output');
  const gstOutput = document.getElementById('calc-gst-output');
  const savingsOutput = document.getElementById('calc-savings-output');

  if (!calcBtn || !euroInput) return;

  const EUR_INR_RATE = 91.50; // Approximate baseline benchmark

  calcBtn.addEventListener('click', () => {
    const euroVal = parseFloat(euroInput.value) || 0;
    if (euroVal <= 0) {
      alert('Please enter a valid estimated machine value in Euros (EUR).');
      return;
    }

    const inrVal = euroVal * EUR_INR_RATE;
    const gstVal = inrVal * 0.18; // 18% GST Input Credit
    const forexRiskSaved = inrVal * 0.06; // Estimated 6% forex hedging & bank spread saved

    if (inrOutput) inrOutput.textContent = '₹ ' + inrVal.toLocaleString('en-IN', { maximumFractionDigits: 0 });
    if (gstOutput) gstOutput.textContent = '₹ ' + gstVal.toLocaleString('en-IN', { maximumFractionDigits: 0 }) + ' (100% Claimable)';
    if (savingsOutput) savingsOutput.textContent = '₹ ' + forexRiskSaved.toLocaleString('en-IN', { maximumFractionDigits: 0 }) + ' (Direct Savings)';
  });
}
