const fs = require('fs');

// 1. Patch new/dalalmachine/js/script.js
let scriptJs = fs.readFileSync('new/dalalmachine/js/script.js', 'utf8');
const scriptTarget = `        // Toggle selected item
        if (!isOpen) {
            item.classList.add('is-open');
            btn.setAttribute('aria-expanded', 'true');
        }
    };`;

const scriptReplacement = `        // Toggle selected item
        if (!isOpen) {
            item.classList.add('is-open');
            btn.setAttribute('aria-expanded', 'true');
        }
    };

    // CSP-compliant delegated click listener for FAQ toggles
    document.addEventListener('click', function(e) {
        var btn = e.target.closest('.faq-minimal-btn');
        if (!btn) return;
        e.preventDefault();
        window.toggleDalalSplitFaq(btn);
    });`;

if (scriptJs.includes('toggleDalalSplitFaq')) {
  scriptJs = scriptJs.replace(scriptTarget, scriptReplacement);
  fs.writeFileSync('new/dalalmachine/js/script.js', scriptJs, 'utf8');
  console.log('Successfully patched script.js!');
} else {
  console.error('Target not found in script.js');
}

// 2. Patch new/dalalmachine/index.html (Inline script controller and cache buster)
let indexHtml = fs.readFileSync('new/dalalmachine/index.html', 'utf8');
const indexTarget = `    <!-- FAQ Interactive JavaScript Controller -->
    <script>
    function toggleDalalSplitFaq(btn) {
        var item = btn.closest('.faq-minimal-item');
        if (!item) return;
        var isOpen = item.classList.contains('is-open');

        // Close other items for accordion behavior
        var allItems = document.querySelectorAll('.faq-minimal-item');
        allItems.forEach(function(el) {
            el.classList.remove('is-open');
            var button = el.querySelector('.faq-minimal-btn');
            if (button) button.setAttribute('aria-expanded', 'false');
        });

        // Toggle selected item
        if (!isOpen) {
            item.classList.add('is-open');
            btn.setAttribute('aria-expanded', 'true');
        }
    }
    </script>`;

const indexReplacement = `    <!-- FAQ Interactive JavaScript Controller -->
    <script>
    (function() {
        function toggleDalalSplitFaq(btn) {
            var item = btn.closest('.faq-minimal-item');
            if (!item) return;
            var list = item.closest('.faq-minimal-list');
            var isOpen = item.classList.contains('is-open');

            var allItems = (list || document).querySelectorAll('.faq-minimal-item');
            allItems.forEach(function(el) {
                el.classList.remove('is-open');
                var button = el.querySelector('.faq-minimal-btn');
                if (button) button.setAttribute('aria-expanded', 'false');
            });

            if (!isOpen) {
                item.classList.add('is-open');
                btn.setAttribute('aria-expanded', 'true');
            }
        }
        window.toggleDalalSplitFaq = toggleDalalSplitFaq;

        // CSP-compliant delegated click listener
        document.addEventListener('click', function(e) {
            var btn = e.target.closest('.faq-minimal-btn');
            if (!btn) return;
            e.preventDefault();
            toggleDalalSplitFaq(btn);
        });
    })();
    </script>`;

indexHtml = indexHtml.replace(indexTarget, indexReplacement);

// Cache-bust script.js
indexHtml = indexHtml.replace('<script src="js/script.js"></script>', '<script src="js/script.js?v=3.5"></script>');

fs.writeFileSync('new/dalalmachine/index.html', indexHtml, 'utf8');
console.log('Successfully patched index.html!');

// 3. Patch new/dalalmachine/services.html (Cache buster)
let servicesHtml = fs.readFileSync('new/dalalmachine/services.html', 'utf8');
servicesHtml = servicesHtml.replace('<script src="js/script.js"></script>', '<script src="js/script.js?v=3.5"></script>');
fs.writeFileSync('new/dalalmachine/services.html', servicesHtml, 'utf8');
console.log('Successfully patched services.html!');

