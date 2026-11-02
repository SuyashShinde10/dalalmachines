const fs = require('fs');

let code = fs.readFileSync('admin/inquiries.html', 'utf8');

// 1. Update setupPaginationEvents to include robust click event delegation
const oldSetupPagEvents = `    function setupPaginationEvents() {
      const sizeSelect = document.getElementById('pagination-size-select');
      if (sizeSelect) {
        sizeSelect.addEventListener('change', (e) => {
          pageSize = e.target.value === 'all' ? 'all' : parseInt(e.target.value, 10);
          currentPage = 1;
          renderInquiries();
        });
      }
    }`;

const newSetupPagEvents = `    function setupPaginationEvents() {
      const sizeSelect = document.getElementById('pagination-size-select');
      if (sizeSelect) {
        sizeSelect.addEventListener('change', (e) => {
          pageSize = e.target.value === 'all' ? 'all' : parseInt(e.target.value, 10);
          currentPage = 1;
          renderInquiries();
        });
      }

      // Robust delegated click handler on pagination container
      const controls = document.getElementById('pagination-controls');
      if (controls) {
        controls.addEventListener('click', (e) => {
          const btn = e.target.closest('.pagination-btn');
          if (!btn || btn.disabled) return;
          const pageVal = btn.getAttribute('data-page');
          if (pageVal) {
            e.preventDefault();
            goToPage(pageVal);
          }
        });
      }
    }`;

if (code.includes(oldSetupPagEvents)) {
  code = code.replace(oldSetupPagEvents, newSetupPagEvents);
  console.log('Updated setupPaginationEvents');
} else {
  console.log('setupPaginationEvents not matched directly, checking normalized');
  code = code.replace(
    /function setupPaginationEvents\(\)\s*\{[\s\S]*?renderInquiries\(\);\s*\}\);\s*\}\s*\}/,
    newSetupPagEvents
  );
  console.log('Replaced setupPaginationEvents via regex');
}

// 2. Update renderPaginationControls, generatePageNumbers, and goToPage
const oldPagControlsStart = 'function renderPaginationControls(totalItems, actualSize, totalPages, startIdx, endIdx) {';
const oldPagControlsEnd = 'async function updateInquiryStatus(id, newStatus) {';

const sIdx = code.indexOf(oldPagControlsStart);
const eIdx = code.indexOf(oldPagControlsEnd);

if (sIdx !== -1 && eIdx !== -1) {
  const newPagFunctions = `function renderPaginationControls(totalItems, actualSize, totalPages, startIdx, endIdx) {
      const infoText = document.getElementById('pagination-info-text');
      const controls = document.getElementById('pagination-controls');

      if (!infoText || !controls) return;

      if (totalItems === 0) {
        infoText.innerHTML = 'Showing <strong>0</strong> inquiries';
        controls.innerHTML = '';
        return;
      }

      infoText.innerHTML = \`Showing <strong>\${startIdx}</strong>-<strong>\${endIdx}</strong> of <strong>\${totalItems}</strong> inquiries\`;

      if (pageSize === 'all' || totalPages <= 1) {
        controls.innerHTML = \`
          <button type="button" class="pagination-btn active" data-page="1" disabled>1</button>
        \`;
        return;
      }

      let html = '';
      const curr = parseInt(currentPage, 10) || 1;

      // Prev Button
      const isFirst = curr <= 1;
      html += \`<button type="button" class="pagination-btn \${isFirst ? 'disabled' : ''}" data-page="\${curr - 1}" \${isFirst ? 'disabled' : ''} onclick="goToPage(\${curr - 1})" title="Previous Page">
        <i class="fa fa-chevron-left" style="font-size: 11px;"></i> Prev
      </button>\`;

      // Page numbers: 1, 2, 3, 4, 5...
      const pages = generatePageNumbers(curr, totalPages);
      pages.forEach(p => {
        if (p === '...') {
          html += \`<span class="pagination-ellipsis">&hellip;</span>\`;
        } else {
          const numP = parseInt(p, 10);
          const isActive = numP === curr;
          html += \`<button type="button" class="pagination-btn \${isActive ? 'active' : ''}" data-page="\${numP}" onclick="goToPage(\${numP})" \${isActive ? 'disabled' : ''}>\${numP}</button>\`;
        }
      });

      // Next Button
      const isLast = curr >= totalPages;
      html += \`<button type="button" class="pagination-btn \${isLast ? 'disabled' : ''}" data-page="\${curr + 1}" \${isLast ? 'disabled' : ''} onclick="goToPage(\${curr + 1})" title="Next Page">
        Next <i class="fa fa-chevron-right" style="font-size: 11px;"></i>
      </button>\`;

      controls.innerHTML = html;
    }

    function generatePageNumbers(current, total) {
      const c = parseInt(current, 10) || 1;
      const t = parseInt(total, 10) || 1;
      if (t <= 7) {
        return Array.from({ length: t }, (_, i) => i + 1);
      }
      if (c <= 4) {
        return [1, 2, 3, 4, 5, '...', t];
      }
      if (c >= t - 3) {
        return [1, '...', t - 4, t - 3, t - 2, t - 1, t];
      }
      return [1, '...', c - 1, c, c + 1, '...', t];
    }

    function goToPage(page) {
      const targetPage = parseInt(page, 10);
      if (isNaN(targetPage) || targetPage < 1) return;
      currentPage = targetPage;
      renderInquiries();
      const targetCard = document.querySelector('.table-responsive');
      if (targetCard) {
        targetCard.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    }
    window.goToPage = goToPage;

    `;

  code = code.substring(0, sIdx) + newPagFunctions + code.substring(eIdx);
  console.log('Replaced renderPaginationControls & goToPage');
} else {
  console.error('Hooks not found for pagination controls:', sIdx, eIdx);
}

// 3. Bump css/admin.css version
code = code.replace(/admin\.css\?v=[0-9.]+/g, 'admin.css?v=3.0');

fs.writeFileSync('admin/inquiries.html', code, 'utf8');
console.log('admin/inquiries.html updated successfully!');

