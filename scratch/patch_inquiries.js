const fs = require('fs');

let code = fs.readFileSync('admin/inquiries.html', 'utf8');

// 1. CSS version bump to v4.0
code = code.replace(/admin-ai\.css\?v=[0-9.]+/g, 'admin-ai.css?v=4.0');

// 2. allInquiries window exposure
code = code.replace('let allInquiries = [];', 'let allInquiries = [];\n    window.allInquiries = allInquiries;');
code = code.replace('allInquiries = res.inquiries;', 'allInquiries = res.inquiries;\n        window.allInquiries = allInquiries;');

// 3. Button inside renderInquiries()
code = code.replace(
  /onclick=['"]handleAIInquiryClick\([^)]*\)['"]/,
  'class="btn-sm btn-ai-score" data-inquiry-id="${esc(i.id)}" onclick=\'openAILeadScore("${esc(i.id)}")\''
);

// 4. Remove duplicate closeAIModal, handleAIInquiryClick, and inline modal
const cutIndex = code.indexOf('function closeAIModal()');
if (cutIndex !== -1) {
  const replacement = `function openAILeadScore(id) {
      if (typeof window.openAIInquiryAnalysis === 'function') {
        window.openAIInquiryAnalysis(id);
      } else if (typeof window.handleAIInquiryClick === 'function') {
        window.handleAIInquiryClick(id);
      } else {
        console.warn('AI copilot script initializing...');
      }
    }
    window.openAILeadScore = openAILeadScore;
    window.handleAIInquiryClick = openAILeadScore;

    // Delegated click listener for dynamic rows
    document.addEventListener('DOMContentLoaded', () => {
      const tbody = document.getElementById('inquiries-tbody');
      if (tbody) {
        tbody.addEventListener('click', (e) => {
          const btn = e.target.closest('.btn-ai-score');
          if (btn) {
            e.preventDefault();
            const id = btn.getAttribute('data-inquiry-id');
            if (id) openAILeadScore(id);
          }
        });
      }
    });
  </script>

  <script src="js/admin-ai.js?v=4.0"></script>
</body>
</html>
`;
  code = code.substring(0, cutIndex) + replacement;
}

fs.writeFileSync('admin/inquiries.html', code, 'utf8');
console.log('Successfully updated admin/inquiries.html');

