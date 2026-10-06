// Dalal Machine Tools Agency Pvt. Ltd. - Interactive Application Logic

document.addEventListener('DOMContentLoaded', () => {
  // Initialize Catalog if on category.html or index.html
  const gridContainer = document.getElementById('catalog-grid-container');
  const paginationWrap = document.getElementById('catalog-pagination');
  const searchInput = document.getElementById('machine-search-input');
  const locationFilters = document.querySelectorAll('.loc-filter-btn');
  const categoryFilters = document.querySelectorAll('.cat-filter-link');
  const countIndicator = document.getElementById('catalog-results-count');

  const PAGE_SIZE = 9; // cards per page
  let currentPage = 1;

  let currentFilter = {
    section: '',
    category: '',
    location: '',
    query: ''
  };

  // Parse URL query parameters if present
  const urlParams = new URLSearchParams(window.location.search);
  if (urlParams.has('category')) {
    const targetCat = urlParams.get('category');
    currentFilter.category = targetCat;
    categoryFilters.forEach(l => {
      if (l.getAttribute('data-cat') === targetCat) {
        categoryFilters.forEach(other => other.classList.remove('active'));
        l.classList.add('active');
      }
    });
  }
  if (urlParams.has('section')) {
    currentFilter.section = urlParams.get('section');
  }
  if (urlParams.has('location')) {
    const targetLoc = urlParams.get('location');
    currentFilter.location = targetLoc;
    locationFilters.forEach(b => {
      if (b.getAttribute('data-loc') === targetLoc) {
        locationFilters.forEach(other => other.classList.remove('active'));
        b.classList.add('active');
      }
    });
  }

  function syncSidebarCounts() {
    if (typeof DALAL_MACHINES === 'undefined' || categoryFilters.length === 0) return;
    const catCounts = {};
    let formingCount = 0;
    let cuttingCount = 0;
    DALAL_MACHINES.forEach(m => {
      catCounts[m.category] = (catCounts[m.category] || 0) + 1;
      if (m.section === 'forming') formingCount++;
      if (m.section === 'cutting') cuttingCount++;
    });

    categoryFilters.forEach(link => {
      const cat = link.getAttribute('data-cat');
      const countSpan = link.querySelector('.count');
      if (countSpan) {
        if (!cat) {
          const text = link.textContent.toLowerCase();
          if (text.includes('forming')) countSpan.textContent = formingCount;
          else if (text.includes('cutting')) countSpan.textContent = cuttingCount;
          else countSpan.textContent = DALAL_MACHINES.length;
        } else if (catCounts[cat] !== undefined) {
          countSpan.textContent = catCounts[cat];
        }
      }
    });
  }

  syncSidebarCounts();

  function buildCardHTML(m) {
    return `
      <div class="col-lg-4 col-md-6 col-sm-12" style="margin-bottom: 30px;">
        <div class="machine-item-card">
          <div class="machine-thumb-box">
            <img src="${m.image}" alt="${m.name}" loading="lazy">
            <span class="machine-location-pill"><i class="fa fa-map-marker"></i> ${m.location}</span>
            <span class="machine-stock-badge">ID: ${m.id}</span>
          </div>
          <div class="machine-info-content">
            <div class="machine-cat-label">${m.categoryName} &bull; ${m.make}</div>
            <h4 class="machine-title">${m.name}</h4>
            <div class="machine-specs-grid">
              <div class="spec-item">
                <span class="label">Capacity / Tonnage</span>
                <span class="val">${m.tonnage > 0 ? m.tonnage + ' Tons' : 'Precision CNC'}</span>
              </div>
              <div class="spec-item">
                <span class="label">Mfg. Year</span>
                <span class="val">${m.year || 'Standard'}</span>
              </div>
              <div class="spec-item">
                <span class="label">Model Code</span>
                <span class="val">${m.model}</span>
              </div>
              <div class="spec-item">
                <span class="label">Ready Status</span>
                <span class="val" style="color: #16a34a;">Inspected / Verified</span>
              </div>
            </div>
            <div class="machine-card-footer">
              <a href="product.html?id=${m.id}" class="btn-view-details">Full Specifications &rarr;</a>
              <a href="https://wa.me/919821232131?text=Hello%20Mr.%20Vinit%20Dalal,%20I%20am%20interested%20in%20${encodeURIComponent(m.name)}%20(Machine%20ID:%20${m.id})"
                 target="_blank" class="btn-rfq-whatsapp" title="Instant WhatsApp RFQ">
                <i class="fa fa-whatsapp"></i>
              </a>
            </div>
          </div>
        </div>
      </div>`;
  }

  function renderPagination(totalItems, pageSize, current) {
    if (!paginationWrap) return;
    const totalPages = Math.ceil(totalItems / pageSize);
    if (totalPages <= 1) { paginationWrap.style.display = 'none'; return; }

    paginationWrap.style.display = 'flex';

    // Build visible page numbers (smart windowed set)
    const pages = [];
    if (totalPages <= 7) {
      for (let i = 1; i <= totalPages; i++) pages.push(i);
    } else {
      pages.push(1);
      if (current > 3) pages.push('…');
      const start = Math.max(2, current - 1);
      const end   = Math.min(totalPages - 1, current + 1);
      for (let i = start; i <= end; i++) pages.push(i);
      if (current < totalPages - 2) pages.push('…');
      pages.push(totalPages);
    }

    const btnHTML = pages.map(p => {
      if (p === '…') return `<span class="page-dots">…</span>`;
      return `<button class="page-btn${p === current ? ' active' : ''}" data-page="${p}">${p}</button>`;
    }).join('');

    paginationWrap.innerHTML =
      `<button class="page-btn page-nav-btn${current === 1 ? ' disabled' : ''}" data-page="${current - 1}">
         <i class="fa fa-angle-left"></i> Prev
       </button>
       ${btnHTML}
       <button class="page-btn page-nav-btn${current === totalPages ? ' disabled' : ''}" data-page="${current + 1}">
         Next <i class="fa fa-angle-right"></i>
       </button>`;

    // Bind clicks
    paginationWrap.querySelectorAll('.page-btn:not(.disabled):not(.active)').forEach(btn => {
      btn.addEventListener('click', () => {
        currentPage = parseInt(btn.getAttribute('data-page'));
        renderGrid();
        // Scroll up to top of grid smoothly
        if (gridContainer) {
          const y = gridContainer.getBoundingClientRect().top + window.pageYOffset - 100;
          window.scrollTo({ top: Math.max(0, y), behavior: 'smooth' });
        }
      });
    });
  }

  function renderGrid() {
    if (!gridContainer || typeof DALAL_MACHINES === 'undefined') return;

    const filtered = getMachines(currentFilter);
    const isHomePage = window.location.pathname.endsWith('index.html') || window.location.pathname === '/' || window.location.pathname.endsWith('/Machinery/');

    // Homepage: always show 6 cards, no pagination
    if (isHomePage && !currentFilter.query && !currentFilter.location && !currentFilter.category && !currentFilter.section) {
      const displayList = filtered.slice(0, 6);
      if (countIndicator) countIndicator.textContent = `Showing ${displayList.length} machine${displayList.length === 1 ? '' : 's'}`;
      if (paginationWrap) paginationWrap.style.display = 'none';

      if (displayList.length === 0) {
        gridContainer.innerHTML = buildEmptyState();
        return;
      }
      gridContainer.innerHTML = displayList.map(buildCardHTML).join('');
      return;
    }

    // Catalog page: paginated
    const totalItems = filtered.length;
    const totalPages = Math.ceil(totalItems / PAGE_SIZE);
    if (currentPage > totalPages) currentPage = Math.max(1, totalPages);
    const start = (currentPage - 1) * PAGE_SIZE;
    const pageItems = filtered.slice(start, start + PAGE_SIZE);

    if (countIndicator) {
      const end = Math.min(start + PAGE_SIZE, totalItems);
      countIndicator.textContent = totalItems === 0
        ? 'No machines found'
        : `Showing ${start + 1}–${end} of ${totalItems} machine${totalItems === 1 ? '' : 's'}`;
    }

    if (totalItems === 0) {
      gridContainer.innerHTML = buildEmptyState();
      if (paginationWrap) paginationWrap.style.display = 'none';
      return;
    }

    gridContainer.innerHTML = pageItems.map(buildCardHTML).join('');
    renderPagination(totalItems, PAGE_SIZE, currentPage);
  }

  function buildEmptyState() {
    return `
      <div class="col-xs-12 col-sm-12 col-md-12 col-lg-12 col-12 catalog-empty-state" style="width:100%!important;flex:0 0 100%!important;max-width:100%!important;display:flex!important;flex-direction:column!important;align-items:center!important;justify-content:center!important;text-align:center!important;margin:0 auto!important;padding:60px 20px!important;">
        <div class="empty-icon" style="font-size:52px;color:#94a3b8;margin-bottom:18px;line-height:1;"><i class="fa fa-search"></i></div>
        <h3 style="font-family:'Barlow',sans-serif;font-weight:700;font-size:26px;color:#1e293b;margin:0 0 12px;text-align:center;">No Machines Matching Your Criteria</h3>
        <p style="color:#64748b;font-size:15.5px;line-height:1.6;max-width:520px;margin:0 auto 24px;text-align:center;">We regularly source heavy machinery directly through our European &amp; Asian dealer network. Contact Mr. Vinit Dalal for custom sourcing.</p>
        <a href="https://wa.me/919821232131?text=Hello%20Dalal%20Machines,%20I%20am%20looking%20for%20a%20specific%20machine%20not%20in%20current%20listing."
           target="_blank" class="theme-btn btn-style-one" style="padding:13px 30px;background:#25D366;border-color:#25D366;color:#fff;font-weight:600;border-radius:6px;display:inline-flex;align-items:center;gap:8px;justify-content:center;margin:0 auto;text-decoration:none;">
          <i class="fa fa-whatsapp" style="font-size:18px;"></i> Inquire on WhatsApp (+91 9821232131)
        </a>
      </div>`;
  }


  // Bind search box
  if (searchInput) {
    searchInput.addEventListener('input', (e) => {
      currentFilter.query = e.target.value.trim();
      currentPage = 1;
      renderGrid();
    });
  }

  // Bind location buttons
  locationFilters.forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      locationFilters.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      currentFilter.location = btn.getAttribute('data-loc') || '';
      currentPage = 1;
      renderGrid();
    });
  });

  // Bind category sidebar links
  categoryFilters.forEach(link => {
    link.addEventListener('click', (e) => {
      e.preventDefault();
      categoryFilters.forEach(l => l.classList.remove('active'));
      link.classList.add('active');
      const cat = link.getAttribute('data-cat') || '';
      currentFilter.category = cat;
      
      // Reset section filter when category is selected
      if (!cat) {
        const text = link.textContent.toLowerCase();
        if (text.includes('forming')) {
          currentFilter.section = 'forming';
        } else if (text.includes('cutting')) {
          currentFilter.section = 'cutting';
        } else {
          currentFilter.section = '';
        }
      } else {
        currentFilter.section = '';
      }
      currentPage = 1;
      renderGrid();

      // Smooth scroll to catalog results header if out of view
      const resultsBar = document.getElementById('catalog-results-count') || gridContainer;
      if (resultsBar) {
        const rect = resultsBar.getBoundingClientRect();
        if (rect.top < 60 || rect.top > 300) {
          const y = rect.top + window.pageYOffset - 90;
          window.scrollTo({ top: Math.max(0, y), behavior: 'smooth' });
        }
      }
    });
  });

  // Initial render
  renderGrid();

  // Dynamic Live API Synchronization (falls back smoothly to static catalog-data.js)
  if (typeof fetch !== 'undefined') {
    fetch('/api/products')
      .then(r => r.json())
      .then(data => {
        if (data && data.success && Array.isArray(data.products) && data.products.length > 0) {
          window.DALAL_MACHINES = data.products;
          syncSidebarCounts();
          renderGrid();
        }
      })
      .catch(() => {
        // Silent fallback for static/offline operation
      });
  }

  // High Seas Calculator Setup
  const calcBtn = document.getElementById('calc-calculate-btn');
  if (calcBtn) {
    calcBtn.addEventListener('click', () => {
      const valInput = parseFloat(document.getElementById('calc-machine-val').value) || 0;
      const currency = document.getElementById('calc-currency').value;
      const rate = currency === 'EUR' ? 90.0 : 84.0;
      
      const inrValue = valInput * rate;
      // High Seas benefit: no foreign supplier currency hedge fee (~3%), direct customs bill of entry
      const savingsEstimated = inrValue * 0.045; // ~4.5% logistics/currency savings
      const gstInputCredit = inrValue * 0.18; // 18% GST credit allowed to buyer

      document.getElementById('calc-val-inr').textContent = '₹ ' + (inrValue / 100000).toFixed(2) + ' Lakhs';
      document.getElementById('calc-savings-inr').textContent = '₹ ' + (savingsEstimated / 100000).toFixed(2) + ' Lakhs';
      document.getElementById('calc-gst-credit').textContent = '₹ ' + (gstInputCredit / 100000).toFixed(2) + ' Lakhs (100% ITC)';
    });
  }
});
