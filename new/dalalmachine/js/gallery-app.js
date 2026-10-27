// Dalal Machine Tools Agency Pvt. Ltd. - Chronological Shipment Gallery v5.0
// Features: Robust Category Filtering, Lightbox Zoom Modal, Delivery Verification Badges, Pagination

window.DALAL_SHIPMENTS = [
  // Page 1: 2026 Shipments
  {
    image: "images/dalal/hero_forging_press.jpg",
    date: "July 2026",
    category: "forging",
    title: "Loading National 1000T Hot Forging Press",
    desc: "Dismantled in Thailand and safely shipped for an automotive forging customer in Rajkot, Gujarat."
  },
  {
    image: "images/dalal/knuckle_coining_press.jpg",
    date: "June 2026",
    category: "coining",
    title: "1000T Knuckle Joint Press (K8340) in Russia",
    desc: "Procured directly in Russia for our customer in Jamshedpur for precision cold sizing operations."
  },
  {
    image: "images/dalal/logistics_heavy_transport.jpg",
    date: "May 2026",
    category: "forging",
    title: "Dismantling 2T Hydraulic Hammer",
    desc: "Mr. Yatin overseeing expert rigging and dismantling of a 2 Ton hydraulic hammer in Rajkot for Mumbai client."
  },
  {
    image: "images/dalal/cframe_press_pune.jpg",
    date: "April 2026",
    category: "forging",
    title: "Loading Eumuco 315T from Pune",
    desc: "Dispatched from Pune stockyard via specialized trailer to leading forging enterprise in Ludhiana, Punjab."
  },
  {
    image: "images/dalal/hero_forging_press.jpg",
    date: "March 2026",
    category: "forging",
    title: "Komatsu 1600T & 2000T Purchased in Poland",
    desc: "Mr. Vinit Dalal personal site inspection and acquisition of 2 heavy Komatsu forging lines for Bangalore customer."
  },
  {
    image: "images/dalal/port_crane_logistics.jpg",
    date: "2026 Feature",
    category: "imtex",
    title: "Exhibiting at IMTEX Forming 2026",
    desc: "Exhibiting at Bangalore as official agents in India for DMT with ECAI forging lines and OMPI clutch systems."
  },

  // Page 2: 2025 Shipments
  {
    image: "images/dalal/hero_forging_press.jpg",
    date: "December 2025",
    category: "forging",
    title: "Voronezh 1600T (TMP) Hot Forging Press",
    desc: "Sourced and tested under live power in Ukraine, shipped to premier automotive forging plant in Faridabad."
  },
  {
    image: "images/dalal/cnc_boring_machine.jpg",
    date: "November 2025",
    category: "transport",
    title: "Kieserling MRP 100 Bar Peeling & Straightening Line",
    desc: "Imported from Germany directly under High Seas Sales for specialized bright steel bar manufacturing in Ahmedabad."
  },
  {
    image: "images/dalal/logistics_heavy_transport.jpg",
    date: "October 2025",
    category: "coining",
    title: "Dual 250T KB0034 Presses Customs Cleared",
    desc: "Seamless Nhava Sheva port handling with direct Bill of Entry clearance into Pune ready stock warehouse."
  },
  {
    image: "images/dalal/cnc_boring_machine.jpg",
    date: "September 2025",
    category: "transport",
    title: "TOS Varnsdorf 130mm CNC Horizontal Boring Mill",
    desc: "Procured from Czechia with full geometric alignment test logs, delivered to aerospace tier-1 in Bangalore."
  },
  {
    image: "images/dalal/knuckle_coining_press.jpg",
    date: "August 2025",
    category: "forging",
    title: "Enomoto 400T Friction Screw Press",
    desc: "Inspected at Osaka manufacturing facility and sea chartered to Mumbai for Rajkot precision hardware forge."
  },
  {
    image: "images/dalal/port_crane_logistics.jpg",
    date: "July 2025",
    category: "imtex",
    title: "DMT Turnkey High-Speed Forging Line Installation",
    desc: "Complete factory mechanical assembly and turnkey alignment for heavy industrial customer in Chennai."
  },

  // Page 3: 2024 - 2025 Heavy Rigging & High Seas
  {
    image: "images/dalal/logistics_heavy_transport.jpg",
    date: "May 2025",
    category: "transport",
    title: "6,300 Ton Heavy Forging Press Sea Charter",
    desc: "Heavy-lift breakbulk vessel chartered from European port directly to Mumbai Port with full stevedoring."
  },
  {
    image: "images/dalal/logistics_heavy_transport.jpg",
    date: "April 2025",
    category: "transport",
    title: "Goldhofer Multi-Axle Hydraulic Trailer Convoy",
    desc: "Specialized oversized transport convoy carrying 120-ton press crown from Mumbai to Ludhiana manufacturing plant."
  },
  {
    image: "images/dalal/port_crane_logistics.jpg",
    date: "March 2025",
    category: "transport",
    title: "High Seas Sales Title Transfer at Nhava Sheva",
    desc: "Zero demurrage customs handover with 100% GST input tax credit realized directly under client IEC code."
  },
  {
    image: "images/dalal/ompi_clutch_brake_unit.jpg",
    date: "February 2025",
    category: "imtex",
    title: "OMPI Pneumatic Clutch-Brake Retrofit Demo",
    desc: "Technical retrofitting demonstration replacing obsolete mechanical clutch with Italian pneumatic system."
  },
  {
    image: "images/dalal/knuckle_coining_press.jpg",
    date: "January 2025",
    category: "coining",
    title: "Kalinin K8440 1000T Knuckle Joint Power Test",
    desc: "Mr. Vinit Dalal on-site tolerance audit with dial indicator test under power prior to Russian containerization."
  },
  {
    image: "images/dalal/cframe_press_pune.jpg",
    date: "January 2025",
    category: "forging",
    title: "C-Frame Stamping Presses Dispatched from Pune",
    desc: "Ready stock delivery of 160T and 200T stamping presses to automotive tier-1 supplier in Sanand, Gujarat."
  }
];

window.currentGalleryPage = 1;
window.currentGalleryCategory = 'all';
window.GALLERY_ITEMS_PER_PAGE = 6;

window.getFilteredShipments = function() {
  var list = window.DALAL_SHIPMENTS || [];
  if (window.currentGalleryCategory === 'all') return list;
  return list.filter(function(s) { return s.category === window.currentGalleryCategory; });
};

window.renderGallery = function(page) {
  var container = document.getElementById('gallery-items-container');
  if (!container || !window.DALAL_SHIPMENTS) return;

  var filtered = window.getFilteredShipments();
  var totalPages = Math.ceil(filtered.length / window.GALLERY_ITEMS_PER_PAGE) || 1;
  window.currentGalleryPage = Math.max(1, Math.min(page || 1, totalPages));

  var startIdx = (window.currentGalleryPage - 1) * window.GALLERY_ITEMS_PER_PAGE;
  var pageItems = filtered.slice(startIdx, startIdx + window.GALLERY_ITEMS_PER_PAGE);

  if (pageItems.length === 0) {
    container.innerHTML = 
      '<div class="col-12 text-center" style="padding: 60px 20px;">' +
      '  <i class="fa fa-ship" style="font-size:42px; color:#cbd5e1; margin-bottom:15px; display:block;"></i>' +
      '  <h4 style="font-family:\'Barlow\', sans-serif; font-weight:700; color:#1e293b; font-size:22px;">No Shipments Found in this Category</h4>' +
      '  <p style="color:#64748b; font-size:14px; margin-top:8px;">Select "All Deliveries" to view the complete historical log.</p>' +
      '  <button type="button" class="theme-btn btn-style-one" onclick="window.filterGalleryByCategory(\'all\')" style="margin-top:16px; padding:8px 22px; font-size:13px; background:#f89d13; color:#111; font-weight:700;">Show All Deliveries</button>' +
      '</div>';
    window.renderPagination(0);
    return;
  }

  var html = pageItems.map(function(item) {
    var rawImg = item.image || 'images/dalal/hero_forging_press.jpg';
    var thumbWebp = rawImg.replace(/\.(jpe?g|png)$/i, '_thumb.webp');
    var thumbJpg = rawImg.replace(/\.(jpe?g|png)$/i, '_thumb.jpg');
    var safeTitle = (item.title || '').replace(/'/g, "\\'");
    var safeDesc = (item.desc || '').replace(/'/g, "\\'");

    return (
      '<div class="col-lg-4 col-md-6 col-sm-12" style="margin-bottom:30px;">' +
      '  <div class="gallery-item-card" onclick="window.openGalleryLightbox(\'' + rawImg + '\', \'' + safeTitle + '\', \'' + safeDesc + '\')" style="cursor:pointer; height:100%; transition:all 0.3s ease;">' +
      '    <div class="gallery-thumb-box" style="position:relative; overflow:hidden;">' +
      '      <picture>' +
      '        <source srcset="' + thumbWebp + '" type="image/webp">' +
      '        <img src="' + thumbJpg + '" onerror="this.onerror=null; this.src=\'' + rawImg + '\';" alt="' + item.title + '" loading="lazy" decoding="async" width="370" height="240" style="width:100%; height:100%; object-fit:cover; display:block;">' +
      '      </picture>' +
      '      <div style="position:absolute; top:12px; right:12px; background:rgba(0,0,0,0.6); color:#fff; width:32px; height:32px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:13px;" title="Click to Zoom Image">' +
      '        <i class="fa fa-search-plus"></i>' +
      '      </div>' +
      '    </div>' +
      '    <div class="gallery-content">' +
      '      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">' +
      '        <span class="gallery-date-pill">' + item.date + '</span>' +
      '        <span style="display:inline-flex; align-items:center; gap:4px; font-size:11px; font-weight:700; color:#059669; background:#ecfdf5; border:1px solid #a7f3d0; padding:2px 8px; border-radius:4px;">' +
      '          <i class="fa fa-check-circle"></i> Delivered' +
      '        </span>' +
      '      </div>' +
      '      <h4 class="gallery-title" style="margin-bottom:8px;">' + item.title + '</h4>' +
      '      <p class="gallery-desc">' + item.desc + '</p>' +
      '    </div>' +
      '  </div>' +
      '</div>'
    );
  }).join('');

  container.innerHTML = html;
  window.renderPagination(totalPages);
};

window.renderPagination = function(totalPages) {
  var paginList = document.getElementById('gallery-pagination-list');
  if (!paginList) return;

  if (totalPages <= 1) {
    paginList.innerHTML = '';
    return;
  }

  var html = '';
  if (window.currentGalleryPage > 1) {
    html += '<li><a href="javascript:void(0)" class="page-nav-btn prev-btn" onclick="window.changeGalleryPage(' + (window.currentGalleryPage - 1) + ')">&larr; Prev</a></li>';
  }

  for (var i = 1; i <= totalPages; i++) {
    var activeClass = (i === window.currentGalleryPage) ? 'active' : '';
    html += '<li><a href="javascript:void(0)" class="page-num-btn ' + activeClass + '" onclick="window.changeGalleryPage(' + i + ')">' + i + '</a></li>';
  }

  if (window.currentGalleryPage < totalPages) {
    html += '<li><a href="javascript:void(0)" class="page-nav-btn next-btn" onclick="window.changeGalleryPage(' + (window.currentGalleryPage + 1) + ')">Next &rarr;</a></li>';
  }

  paginList.innerHTML = html;
};

window.changeGalleryPage = function(target) {
  var filtered = window.getFilteredShipments();
  var totalPages = Math.ceil(filtered.length / window.GALLERY_ITEMS_PER_PAGE) || 1;
  var newPage = window.currentGalleryPage;

  if (target === 'prev') {
    newPage = Math.max(1, window.currentGalleryPage - 1);
  } else if (target === 'next') {
    newPage = Math.min(totalPages, window.currentGalleryPage + 1);
  } else {
    newPage = parseInt(target, 10) || 1;
  }

  if (newPage !== window.currentGalleryPage) {
    window.renderGallery(newPage);
    var scrollTarget = document.getElementById('gallery-section-top');
    if (scrollTarget) {
      scrollTarget.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  }
};

// Category Filter Handler
window.filterGalleryByCategory = function(category, btn) {
  window.currentGalleryCategory = category || 'all';

  // Update active state on buttons
  var allButtons = document.querySelectorAll('.gallery-filter-btn, [data-type]');
  allButtons.forEach(function(b) {
    if (b.classList.contains('gallery-filter-btn') || b.getAttribute('data-type')) {
      b.classList.remove('active');
    }
  });

  if (btn && btn.classList) {
    btn.classList.add('active');
  } else {
    // If called without element reference, find by category
    var matching = document.querySelector('.gallery-filter-btn[data-type="' + category + '"]');
    if (matching) matching.classList.add('active');
  }

  window.renderGallery(1);

  // Synchronize Polaroid Line Carousel
  if (window.polaroidCarouselInstance && typeof window.polaroidCarouselInstance.setSlides === 'function') {
    var filtered = window.getFilteredShipments();
    var newSlides = filtered.map(function(s, idx) {
      return {
        image: s.image,
        title: s.title,
        caption: s.desc,
        alt: s.title,
        date: s.date,
        category: s.category,
        seed: idx + 1
      };
    });
    window.polaroidCarouselInstance = window.polaroidCarouselInstance.setSlides(newSlides);
  }
};

// Lightbox Handlers
window.openGalleryLightbox = function(imgSrc, title, desc) {
  var modal = document.getElementById('dalal-lightbox-modal');
  var img = document.getElementById('dalal-lightbox-img');
  var titleEl = document.getElementById('dalal-lightbox-title');
  var descEl = document.getElementById('dalal-lightbox-desc');

  if (modal && img) {
    img.src = imgSrc;
    if (titleEl) titleEl.textContent = title || 'Machinery Shipment';
    if (descEl) descEl.textContent = desc || '';
    modal.classList.add('is-open');
    document.body.style.overflow = 'hidden';
  }
};

window.closeDalalLightbox = function(event) {
  if (event && event.target && event.target.closest('.dalal-lightbox-content') && !event.target.classList.contains('dalal-lightbox-close')) {
    return; // Don't close if clicked inside content unless it's close button
  }
  var modal = document.getElementById('dalal-lightbox-modal');
  if (modal) {
    modal.classList.remove('is-open');
    document.body.style.overflow = '';
  }
};

// Global Delegated Click Listener for Filter Buttons
document.addEventListener('click', function(e) {
  var filterBtn = e.target.closest('.gallery-filter-btn');
  if (filterBtn) {
    e.preventDefault();
    var cat = filterBtn.getAttribute('data-type');
    window.filterGalleryByCategory(cat, filterBtn);
  }
});

// ESC key to close lightbox
document.addEventListener('keydown', function(e) {
  if (e.key === 'Escape') {
    window.closeDalalLightbox();
  }
});

// Auto-run on load
function autoInitGallery() {
  window.renderGallery(1);
  if (typeof window.initPolaroidLine === 'function' && !window.polaroidCarouselInstance) {
    window.initPolaroidLine();
  }
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', autoInitGallery);
} else {
  autoInitGallery();
}
