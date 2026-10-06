// Dalal Machine Tools Agency Pvt. Ltd. - Chronological Shipment Gallery
const DALAL_SHIPMENTS = [
  // Page 1: 2026 Shipments
  {
    image: "images/dalal/hero_forging_press.jpg",
    date: "July 2026",
    title: "Loading National 1000T Hot Forging Press",
    desc: "Dismantled in Thailand and safely shipped for an automotive forging customer in Rajkot, Gujarat."
  },
  {
    image: "images/dalal/knuckle_coining_press.jpg",
    date: "June 2026",
    title: "1000T Knuckle Joint Press (K8340) in Russia",
    desc: "Procured directly in Russia for our customer in Jamshedpur for precision cold sizing operations."
  },
  {
    image: "images/dalal/logistics_heavy_transport.jpg",
    date: "May 2026",
    title: "Dismantling 2T Hydraulic Hammer",
    desc: "Mr. Yatin overseeing expert rigging and dismantling of a 2 Ton hydraulic hammer in Rajkot for Mumbai client."
  },
  {
    image: "images/dalal/cframe_press_pune.jpg",
    date: "April 2026",
    title: "Loading Eumuco 315T from Pune",
    desc: "Dispatched from Pune stockyard via specialized trailer to leading forging enterprise in Ludhiana, Punjab."
  },
  {
    image: "images/dalal/hero_forging_press.jpg",
    date: "March 2026",
    title: "Komatsu 1600T & 2000T Purchased in Poland",
    desc: "Mr. Vinit Dalal personal site inspection and acquisition of 2 heavy Komatsu forging lines for Bangalore customer."
  },
  {
    image: "images/dalal/port_crane_logistics.jpg",
    date: "2026 Feature",
    title: "Exhibiting at IMTEX Forming 2026",
    desc: "Exhibiting at Bangalore as official agents in India for DMT with ECAI forging lines and OMPI clutch systems."
  },

  // Page 2: 2025 Shipments
  {
    image: "images/dalal/hero_forging_press.jpg",
    date: "December 2025",
    title: "Voronezh 1600T (TMP) Hot Forging Press",
    desc: "Sourced and tested under live power in Ukraine, shipped to premier automotive forging plant in Faridabad."
  },
  {
    image: "images/dalal/cnc_boring_machine.jpg",
    date: "November 2025",
    title: "Kieserling MRP 100 Bar Peeling & Straightening Line",
    desc: "Imported from Germany directly under High Seas Sales for specialized bright steel bar manufacturing in Ahmedabad."
  },
  {
    image: "images/dalal/logistics_heavy_transport.jpg",
    date: "October 2025",
    title: "Dual 250T KB0034 Presses Customs Cleared",
    desc: "Seamless Nhava Sheva port handling with direct Bill of Entry clearance into Pune ready stock warehouse."
  },
  {
    image: "images/dalal/cnc_boring_machine.jpg",
    date: "September 2025",
    title: "TOS Varnsdorf 130mm CNC Horizontal Boring Mill",
    desc: "Procured from Czechia with full geometric alignment test logs, delivered to aerospace tier-1 in Bangalore."
  },
  {
    image: "images/dalal/knuckle_coining_press.jpg",
    date: "August 2025",
    title: "Enomoto 400T Friction Screw Press",
    desc: "Inspected at Osaka manufacturing facility and sea chartered to Mumbai for Rajkot precision hardware forge."
  },
  {
    image: "images/dalal/port_crane_logistics.jpg",
    date: "July 2025",
    title: "DMT Turnkey High-Speed Forging Line Installation",
    desc: "Complete factory mechanical assembly and turnkey alignment for heavy industrial customer in Chennai."
  },

  // Page 3: 2024 - 2025 Heavy Rigging & High Seas
  {
    image: "images/dalal/logistics_heavy_transport.jpg",
    date: "May 2025",
    title: "6,300 Ton Heavy Forging Press Sea Charter",
    desc: "Heavy-lift breakbulk vessel chartered from European port directly to Mumbai Port with full stevedoring."
  },
  {
    image: "images/dalal/logistics_heavy_transport.jpg",
    date: "April 2025",
    title: "Goldhofer Multi-Axle Hydraulic Trailer Convoy",
    desc: "Specialized oversized transport convoy carrying 120-ton press crown from Mumbai to Ludhiana manufacturing plant."
  },
  {
    image: "images/dalal/port_crane_logistics.jpg",
    date: "March 2025",
    title: "High Seas Sales Title Transfer at Nhava Sheva",
    desc: "Zero demurrage customs handover with 100% GST input tax credit realized directly under client IEC code."
  },
  {
    image: "images/dalal/ompi_clutch_brake_unit.jpg",
    date: "February 2025",
    title: "OMPI Pneumatic Clutch-Brake Retrofit Demo",
    desc: "Technical retrofitting demonstration replacing obsolete mechanical clutch with Italian pneumatic system."
  },
  {
    image: "images/dalal/knuckle_coining_press.jpg",
    date: "January 2025",
    title: "Kalinin K8440 1000T Knuckle Joint Power Test",
    desc: "Mr. Vinit Dalal on-site tolerance audit with dial indicator test under power prior to Russian containerization."
  },
  {
    image: "images/dalal/cframe_press_pune.jpg",
    date: "January 2025",
    title: "C-Frame Stamping Presses Dispatched from Pune",
    desc: "Ready stock delivery of 160T and 200T stamping presses to automotive tier-1 supplier in Sanand, Gujarat."
  }
];

let currentGalleryPage = 1;
const ITEMS_PER_PAGE = 6;

function renderGallery(page = 1) {
  const container = document.getElementById('gallery-items-container');
  if (!container || typeof DALAL_SHIPMENTS === 'undefined') return;

  const totalPages = Math.ceil(DALAL_SHIPMENTS.length / ITEMS_PER_PAGE);
  currentGalleryPage = Math.max(1, Math.min(page, totalPages));

  const startIdx = (currentGalleryPage - 1) * ITEMS_PER_PAGE;
  const pageItems = DALAL_SHIPMENTS.slice(startIdx, startIdx + ITEMS_PER_PAGE);

  container.innerHTML = pageItems.map(item => `
    <div class="col-lg-4 col-md-6 col-sm-12">
      <div class="gallery-item-card">
        <div class="gallery-thumb-box">
          <img src="${item.image}" alt="${item.title}" loading="lazy">
        </div>
        <div class="gallery-content">
          <span class="gallery-date-pill">${item.date}</span>
          <h4 class="gallery-title">${item.title}</h4>
          <p class="gallery-desc">${item.desc}</p>
        </div>
      </div>
    </div>
  `).join('');

  renderPagination(totalPages);
}

function renderPagination(totalPages) {
  const paginList = document.getElementById('gallery-pagination-list');
  if (!paginList) return;

  let html = '';

  // Prev Button
  if (currentGalleryPage > 1) {
    html += `<li><a href="javascript:void(0)" class="page-nav-btn prev-btn" onclick="changeGalleryPage(${currentGalleryPage - 1})">&larr; Prev</a></li>`;
  }

  // Page Numbers
  for (let i = 1; i <= totalPages; i++) {
    const activeClass = i === currentGalleryPage ? 'active' : '';
    html += `<li><a href="javascript:void(0)" class="page-num-btn ${activeClass}" onclick="changeGalleryPage(${i})">${i}</a></li>`;
  }

  // Next Button
  if (currentGalleryPage < totalPages) {
    html += `<li><a href="javascript:void(0)" class="page-nav-btn next-btn" onclick="changeGalleryPage(${currentGalleryPage + 1})">Next &rarr;</a></li>`;
  }

  paginList.innerHTML = html;
}

function changeGalleryPage(target) {
  const totalPages = Math.ceil(DALAL_SHIPMENTS.length / ITEMS_PER_PAGE);
  let newPage = currentGalleryPage;

  if (target === 'prev') {
    newPage = Math.max(1, currentGalleryPage - 1);
  } else if (target === 'next') {
    newPage = Math.min(totalPages, currentGalleryPage + 1);
  } else {
    newPage = parseInt(target, 10);
  }

  if (newPage !== currentGalleryPage) {
    renderGallery(newPage);
    const scrollTarget = document.getElementById('gallery-section-top');
    if (scrollTarget) {
      scrollTarget.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  }
}

document.addEventListener('DOMContentLoaded', () => {
  renderGallery(1);
});
