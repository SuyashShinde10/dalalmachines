// Dalal Machine Tools Agency Pvt. Ltd. - Interactive Application Logic v4.0
// Features: Multi-attribute filtering, Skeleton Loading, Grid/Table view, Machine Comparison

document.addEventListener('DOMContentLoaded', () => {
  // Initialize Catalog if on category.html or index.html
  const gridContainer = document.getElementById('catalog-grid-container');
  const paginationWrap = document.getElementById('catalog-pagination');
  const searchInput = document.getElementById('machine-search-input');
  const locationFilters = document.querySelectorAll('.loc-filter-btn');
  const categoryFilters = document.querySelectorAll('.cat-filter-link');
  const countIndicator = document.getElementById('catalog-results-count');
  const makeFilterSelect = document.getElementById('make-filter-select');
  const tonnageFilterSelect = document.getElementById('tonnage-filter-select');
  const viewModeBtns = document.querySelectorAll('.view-mode-btn');

  const PAGE_SIZE = 9; // cards per page
  let currentPage = 1;
  let currentViewMode = 'grid'; // 'grid' | 'table'
  window.dalalCompareList = window.dalalCompareList || [];

  let currentFilter = {
    section: '',
    category: '',
    location: '',
    query: '',
    make: '',
    minTonnage: 0,
    maxTonnage: 0
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
  if (urlParams.has('query')) {
    currentFilter.query = urlParams.get('query');
    if (searchInput) searchInput.value = currentFilter.query;
  }
  if (urlParams.has('make')) {
    currentFilter.make = urlParams.get('make');
    if (makeFilterSelect) makeFilterSelect.value = currentFilter.make;
  }
  if (urlParams.has('tonnage')) {
    const tonVal = urlParams.get('tonnage');
    if (tonVal === '50-250') { currentFilter.minTonnage = 50; currentFilter.maxTonnage = 250; }
    else if (tonVal === '250-1000' || tonVal === '300-800') { currentFilter.minTonnage = 250; currentFilter.maxTonnage = 1000; }
    else if (tonVal === '1000-2500') { currentFilter.minTonnage = 1000; currentFilter.maxTonnage = 2500; }
    else if (tonVal === '2500+' || tonVal === '3000-6300') { currentFilter.minTonnage = 2500; currentFilter.maxTonnage = 10000; }
    if (tonnageFilterSelect) tonnageFilterSelect.value = tonVal;
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

  function buildCardHTML(m, index) {
    const isHomePage = window.location.pathname.endsWith('index.html') || window.location.pathname === '/' || window.location.pathname.endsWith('/Machinery/');
    const colClass = isHomePage
      ? 'col-lg-4 col-md-6 col-sm-12 col-xs-12'
      : 'col-lg-4 col-md-6 col-sm-12 col-xs-12';
    const rawImg = m.image || 'images/dalal/cframe_press_pune.jpg';
    const thumbWebp = rawImg.replace(/\.(jpe?g|png)$/i, '_thumb.webp');
    const thumbJpg = rawImg.replace(/\.(jpe?g|png)$/i, '_thumb.jpg');
    const isPune = (m.location || '').toLowerCase().includes('pune');
    const locIcon = isPune ? '<span class="live-radar-dot"></span>' : '<i class="fa fa-map-marker"></i>';
    const isCompared = window.dalalCompareList.includes(m.id);

    return `
      <div class="${colClass}" style="margin-bottom: 30px;">
        <div class="machine-item-card animate-fade-in" style="animation-delay: ${(index % 9) * 0.04}s;">
          <div class="machine-thumb-box">
            <picture>
              <source srcset="${thumbWebp}" type="image/webp">
              <img src="${thumbJpg}" 
                   onerror="this.onerror=null; this.src='${rawImg}';" 
                   alt="${m.name}" 
                   loading="lazy" 
                   decoding="async" 
                   width="370" 
                   height="240"
                   style="width:100%; height:100%; object-fit:cover; display:block;">
            </picture>
            <span class="machine-location-pill">${locIcon} ${m.location}</span>
            <span class="machine-stock-badge">ID: ${m.id}</span>
          </div>
          <div class="machine-info-content">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;">
              <div class="machine-cat-label" style="margin-bottom:0;">${m.categoryName} &bull; ${m.make}</div>
              <label style="font-size:11.5px; font-weight:600; color:#64748b; cursor:pointer; margin:0; display:inline-flex; align-items:center; gap:4px;">
                <input type="checkbox" onchange="toggleCompareMachine('${m.id}')" ${isCompared ? 'checked' : ''} style="cursor:pointer; accent-color:#f89d13;"> Compare
              </label>
            </div>
            <h4 class="machine-title" title="${m.name}">${m.name}</h4>
            <div class="machine-specs-grid">
              <div class="spec-item" title="${m.tonnage > 0 ? m.tonnage + ' Tons' : 'Precision CNC'}">
                <span class="label">Capacity / Tonnage</span>
                <span class="val">${m.tonnage > 0 ? m.tonnage + ' Tons' : 'Precision CNC'}</span>
              </div>
              <div class="spec-item" title="${m.year || 'Standard'}">
                <span class="label">Mfg. Year</span>
                <span class="val">${m.year || 'Standard'}</span>
              </div>
              <div class="spec-item" title="${m.model || '-'}">
                <span class="label">Model Code</span>
                <span class="val">${m.model || '-'}</span>
              </div>
              <div class="spec-item" title="Inspected & Ready for Live Trial">
                <span class="label">Ready Status</span>
                <span class="val" style="color: #16a34a;"><i class="fa fa-check-circle" style="font-size:11px; margin-right:2px;"></i> Inspected</span>
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

  function buildTableHTML(items) {
    return `
      <div class="col-xs-12 col-sm-12 col-md-12 col-lg-12" style="width:100%!important; flex:0 0 100%!important; max-width:100%!important; margin-bottom:30px;">
        <div style="background:#fff; border:1px solid #e2e8f0; border-radius:8px; overflow-x:auto;">
          <table class="table table-hover" style="margin:0; font-size:13.5px;">
            <thead style="background:#f8fafc; font-weight:700; color:#1e293b;">
              <tr>
                <th style="padding:14px 16px; vertical-align:middle;">Photo</th>
                <th style="padding:14px 16px; vertical-align:middle;">Machine Name / ID</th>
                <th style="padding:14px 16px; vertical-align:middle;">Make & Model</th>
                <th style="padding:14px 16px; vertical-align:middle;">Capacity / Tonnage</th>
                <th style="padding:14px 16px; vertical-align:middle;">Location</th>
                <th style="padding:14px 16px; vertical-align:middle;">Status</th>
                <th style="padding:14px 16px; text-align:right; vertical-align:middle; width:160px; min-width:160px;">Actions</th>
              </tr>
            </thead>
            <tbody>
              ${items.map(m => {
                const isPune = (m.location || '').toLowerCase().includes('pune');
                const locIcon = isPune ? '<span class="live-radar-dot"></span>' : '<i class="fa fa-map-marker"></i>';
                return `
                <tr>
                  <td style="padding:10px 16px; width:70px; vertical-align:middle;">
                    <img src="${m.image || 'images/dalal/cframe_press_pune.jpg'}" alt="${m.name}" style="width:60px; height:42px; object-fit:cover; border-radius:4px; display:block;">
                  </td>
                  <td style="padding:14px 16px; font-weight:700; color:#1e293b; vertical-align:middle;">
                    <a href="product.html?id=${m.id}" style="color:#1b212f; text-decoration:none;">${m.name}</a>
                    <div style="font-size:11.5px; color:#64748b; font-weight:normal;">ID: ${m.id}</div>
                  </td>
                  <td style="padding:14px 16px; vertical-align:middle;">${m.make} &bull; ${m.model || '-'}</td>
                  <td style="padding:14px 16px; font-weight:700; color:#f89d13; vertical-align:middle;">${m.tonnage > 0 ? m.tonnage + ' Tons' : 'CNC Machining'}</td>
                  <td style="padding:14px 16px; vertical-align:middle;">${locIcon} ${m.location}</td>
                  <td style="padding:14px 16px; color:#16a34a; font-weight:600; vertical-align:middle;"><i class="fa fa-check-circle"></i> Operational</td>
                  <td class="tbl-actions-cell">
                    <div class="tbl-actions-wrap">
                      <a href="product.html?id=${m.id}" class="tbl-btn-view" title="View Full Specifications">
                        <span>View</span>
                        <i class="fa fa-arrow-right"></i>
                      </a>
                      <a href="https://wa.me/919821232131?text=Inquiry%20for%20${encodeURIComponent(m.name)}%20(${m.id})" target="_blank" class="tbl-btn-wa" title="Instant WhatsApp Inquiry">
                        <i class="fa fa-whatsapp"></i>
                      </a>
                    </div>
                  </td>
                </tr>`;
              }).join('')}
            </tbody>
          </table>
        </div>
      </div>`;
  }

  function renderSkeletons() {
    if (!gridContainer) return;
    const skeletonHTML = Array(6).fill(0).map(() => `
      <div class="col-lg-4 col-md-6 col-sm-12 col-xs-12">
        <div class="card-skeleton">
          <div class="skeleton-thumb skeleton-shimmer"></div>
          <div class="skeleton-body">
            <div class="skeleton-line short skeleton-shimmer"></div>
            <div class="skeleton-line full skeleton-shimmer"></div>
            <div class="skeleton-line medium skeleton-shimmer"></div>
            <div class="skeleton-line full skeleton-shimmer" style="margin-top:20px;"></div>
          </div>
        </div>
      </div>
    `).join('');
    gridContainer.innerHTML = skeletonHTML;
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

  function renderGrid(showSkeleton = false) {
    if (!gridContainer || typeof DALAL_MACHINES === 'undefined') return;

    if (showSkeleton) {
      renderSkeletons();
      setTimeout(executeRender, 140);
    } else {
      executeRender();
    }
  }

  function executeRender() {
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

    if (currentViewMode === 'table') {
      gridContainer.innerHTML = buildTableHTML(pageItems);
    } else {
      gridContainer.innerHTML = pageItems.map(buildCardHTML).join('');
    }
    renderPagination(totalItems, PAGE_SIZE, currentPage);
  }

  function buildEmptyState() {
    return `
      <div class="col-xs-12 col-sm-12 col-md-12 col-lg-12 col-12 catalog-empty-state" style="width:100%!important;flex:0 0 100%!important;max-width:100%!important;display:flex!important;flex-direction:column!important;align-items:center!important;justify-content:center!important;text-align:center!important;margin:0 auto!important;padding:60px 20px!important;">
        <div class="empty-icon" style="font-size:52px;color:#94a3b8;margin-bottom:18px;line-height:1;"><i class="fa fa-search"></i></div>
        <h3 style="font-family:'Barlow',sans-serif;font-weight:700;font-size:26px;color:#1e293b;margin:0 0 12px;text-align:center;">No Machines Matching Your Criteria</h3>
        <p style="color:#64748b;font-size:15.5px;line-height:1.6;max-width:520px;margin:0 auto 24px;text-align:center;">We regularly source heavy machinery directly through our European &amp; Asian dealer network. Contact Mr. Vinit Dalal for custom sourcing.</p>
        <div style="display:flex; gap:12px; justify-content:center; flex-wrap:wrap;">
          <button type="button" onclick="resetCatalogFilters()" class="theme-btn btn-style-two" style="padding:10px 22px;">Reset Filters</button>
          <a href="https://wa.me/919821232131?text=Hello%20Dalal%20Machines,%20I%20am%20looking%20for%20a%20specific%20machine%20not%20in%20current%20listing." 
             target="_blank" class="theme-btn btn-style-one" style="padding:10px 24px; background:#25D366; border-color:#25D366; color:#fff; font-weight:600;">
            <i class="fa fa-whatsapp"></i> Inquire on WhatsApp (+91 9821232131)
          </a>
        </div>
      </div>`;
  }

  window.resetCatalogFilters = function() {
    currentFilter = { section: '', category: '', location: '', query: '', make: '', minTonnage: 0, maxTonnage: 0 };
    if (searchInput) searchInput.value = '';
    if (makeFilterSelect) makeFilterSelect.value = '';
    if (tonnageFilterSelect) tonnageFilterSelect.value = '';
    locationFilters.forEach(b => b.classList.remove('active'));
    if (locationFilters[0]) locationFilters[0].classList.add('active');
    categoryFilters.forEach(l => l.classList.remove('active'));
    if (categoryFilters[0]) categoryFilters[0].classList.add('active');
    currentPage = 1;
    renderGrid(true);
  };

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
      renderGrid(true);
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
      renderGrid(true);

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

  // Bind Make selector if present
  if (makeFilterSelect) {
    makeFilterSelect.addEventListener('change', (e) => {
      currentFilter.make = e.target.value;
      currentPage = 1;
      renderGrid(true);
    });
  }

  // Bind Tonnage selector if present
  if (tonnageFilterSelect) {
    tonnageFilterSelect.addEventListener('change', (e) => {
      const val = e.target.value;
      if (val === '50-250') { currentFilter.minTonnage = 50; currentFilter.maxTonnage = 250; }
      else if (val === '250-1000') { currentFilter.minTonnage = 250; currentFilter.maxTonnage = 1000; }
      else if (val === '1000-2500') { currentFilter.minTonnage = 1000; currentFilter.maxTonnage = 2500; }
      else if (val === '2500+') { currentFilter.minTonnage = 2500; currentFilter.maxTonnage = 10000; }
      else { currentFilter.minTonnage = 0; currentFilter.maxTonnage = 0; }
      currentPage = 1;
      renderGrid(true);
    });
  }

  // Robust View Mode Switcher (Grid vs Table)
  window.setCatalogViewMode = function(mode) {
    currentViewMode = mode === 'table' ? 'table' : 'grid';

    const gridBtn = document.getElementById('view-mode-grid');
    const tableBtn = document.getElementById('view-mode-table');

    if (gridBtn && tableBtn) {
      if (currentViewMode === 'table') {
        gridBtn.classList.remove('active');
        tableBtn.classList.add('active');
        gridBtn.style.setProperty('background', '#ffffff', 'important');
        gridBtn.style.setProperty('color', '#475569', 'important');
        tableBtn.style.setProperty('background', '#0f172a', 'important');
        tableBtn.style.setProperty('color', '#ffffff', 'important');
      } else {
        tableBtn.classList.remove('active');
        gridBtn.classList.add('active');
        tableBtn.style.setProperty('background', '#ffffff', 'important');
        tableBtn.style.setProperty('color', '#475569', 'important');
        gridBtn.style.setProperty('background', '#0f172a', 'important');
        gridBtn.style.setProperty('color', '#ffffff', 'important');
      }
    }

    renderGrid(false);
  };

  viewModeBtns.forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      const mode = btn.getAttribute('data-mode') || 'grid';
      window.setCatalogViewMode(mode);
    });
  });

  // Comparison Tool Functions
  window.toggleCompareMachine = function(id) {
    const idx = window.dalalCompareList.indexOf(id);
    if (idx !== -1) {
      window.dalalCompareList.splice(idx, 1);
    } else {
      if (window.dalalCompareList.length >= 3) {
        alert('You can compare a maximum of 3 machines simultaneously.');
        return;
      }
      window.dalalCompareList.push(id);
    }
    updateCompareDrawer();
  };

  function updateCompareDrawer() {
    let drawer = document.getElementById('dalal-compare-drawer');
    if (!drawer) {
      drawer = document.createElement('div');
      drawer.id = 'dalal-compare-drawer';
      drawer.style.cssText = 'position:fixed; bottom:20px; left:50%; transform:translateX(-50%); background:#1b212f; color:#fff; padding:12px 24px; border-radius:50px; z-index:9999; box-shadow:0 10px 30px rgba(0,0,0,0.3); display:none; align-items:center; gap:16px; font-size:14px; border:1px solid rgba(248,157,19,0.4);';
      document.body.appendChild(drawer);
    }

    if (window.dalalCompareList.length === 0) {
      drawer.style.display = 'none';
      return;
    }

    drawer.style.display = 'flex';
    drawer.innerHTML = `
      <span><strong>${window.dalalCompareList.length}</strong> Machine${window.dalalCompareList.length > 1 ? 's' : ''} Selected</span>
      <button type="button" onclick="openCompareModal()" class="theme-btn btn-style-one" style="padding:6px 16px; font-size:12.5px; background:#f89d13; color:#111; font-weight:700; border:none; border-radius:30px;">
        Compare Now &rarr;
      </button>
      <button type="button" onclick="clearCompare()" style="background:none; border:none; color:#94a3b8; cursor:pointer; font-size:16px;" title="Clear">&times;</button>
    `;
  }

  window.clearCompare = function() {
    window.dalalCompareList = [];
    updateCompareDrawer();
    renderGrid(false);
  };

  window.openCompareModal = function() {
    if (!window.dalalCompareList.length) return;
    const machines = DALAL_MACHINES.filter(m => window.dalalCompareList.includes(m.id));
    let modal = document.getElementById('dalal-compare-modal');
    if (!modal) {
      modal = document.createElement('div');
      modal.id = 'dalal-compare-modal';
      modal.className = 'dalal-lightbox-backdrop';
      document.body.appendChild(modal);
    }

    modal.innerHTML = `
      <div class="dalal-lightbox-content" style="max-width:960px; padding:24px; background:#fff; color:#1e293b; max-height:90vh; overflow-y:auto;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:18px; border-bottom:1px solid #e2e8f0; padding-bottom:12px;">
          <h3 style="margin:0; font-family:'Barlow'; font-size:24px; font-weight:800; color:#1b212f;">Side-by-Side Machinery Comparison</h3>
          <button type="button" onclick="document.getElementById('dalal-compare-modal').classList.remove('is-open')" style="background:none; border:none; font-size:24px; cursor:pointer; color:#64748b;">&times;</button>
        </div>
        <div class="table-responsive">
          <table class="table table-bordered" style="font-size:13.5px;">
            <thead style="background:#f8fafc;">
              <tr>
                <th style="width:25%;">Parameter</th>
                ${machines.map(m => `<th style="text-align:center;"><strong>${m.name}</strong><br><span style="font-size:11px; color:#64748b;">(${m.id})</span></th>`).join('')}
              </tr>
            </thead>
            <tbody>
              <tr>
                <th>Photo</th>
                ${machines.map(m => `<td style="text-align:center;"><img src="${m.image || 'images/dalal/cframe_press_pune.jpg'}" style="width:120px; height:80px; object-fit:cover; border-radius:4px;"></td>`).join('')}
              </tr>
              <tr>
                <th>Manufacturer / Make</th>
                ${machines.map(m => `<td style="text-align:center; font-weight:600;">${m.make}</td>`).join('')}
              </tr>
              <tr>
                <th>Model Code</th>
                ${machines.map(m => `<td style="text-align:center;">${m.model || '-'}</td>`).join('')}
              </tr>
              <tr>
                <th>Capacity / Tonnage</th>
                ${machines.map(m => `<td style="text-align:center; font-weight:800; color:#f89d13;">${m.tonnage > 0 ? m.tonnage + ' Tons' : 'CNC Machining'}</td>`).join('')}
              </tr>
              <tr>
                <th>Mfg. Year</th>
                ${machines.map(m => `<td style="text-align:center;">${m.year || 'Standard'}</td>`).join('')}
              </tr>
              <tr>
                <th>Current Location</th>
                ${machines.map(m => `<td style="text-align:center;">${m.location}</td>`).join('')}
              </tr>
              <tr>
                <th>Inquiry Action</th>
                ${machines.map(m => `
                  <td style="text-align:center;">
                    <a href="https://wa.me/919821232131?text=Inquiry%20for%20${encodeURIComponent(m.name)}%20(${m.id})" target="_blank" class="theme-btn btn-style-one" style="padding:6px 14px; font-size:12px; background:#25D366; color:#fff; border-color:#25D366;">
                      <i class="fa fa-whatsapp"></i> Inquire
                    </a>
                  </td>`).join('')}
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    `;
    modal.classList.add('is-open');
  };

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
      const savingsEstimated = inrValue * 0.045; // ~4.5% logistics/currency savings
      const gstInputCredit = inrValue * 0.18; // 18% GST credit allowed to buyer

      const valInrEl = document.getElementById('calc-val-inr');
      const savInrEl = document.getElementById('calc-savings-inr');
      const gstCreditEl = document.getElementById('calc-gst-credit');

      if (valInrEl) {
        valInrEl.textContent = '₹ ' + (inrValue / 100000).toFixed(2) + ' Lakhs';
        valInrEl.classList.add('flash-updated');
        setTimeout(() => valInrEl.classList.remove('flash-updated'), 500);
      }
      if (savInrEl) {
        savInrEl.textContent = '₹ ' + (savingsEstimated / 100000).toFixed(2) + ' Lakhs';
        savInrEl.classList.add('flash-updated');
        setTimeout(() => savInrEl.classList.remove('flash-updated'), 500);
      }
      if (gstCreditEl) {
        gstCreditEl.textContent = '₹ ' + (gstInputCredit / 100000).toFixed(2) + ' Lakhs (100% ITC)';
        gstCreditEl.classList.add('flash-updated');
        setTimeout(() => gstCreditEl.classList.remove('flash-updated'), 500);
      }
    });
  }
});
