# patch_clean_faq.py
import re

# 1. Update script.js
script_path = "new/dalalmachine/js/script.js"
with open(script_path, "r", encoding="utf-8") as f:
    script_content = f.read()

target_script = """    // Modern Split Minimalist FAQ Accordion Toggle
    window.toggleDalalSplitFaq = function(btn) {
        var item = btn.closest('.faq-minimal-item');
        if (!item) return;
        var list = item.closest('.faq-minimal-list');
        var isOpen = item.classList.contains('is-open');

        // Close other items in the same list for clean accordion behavior
        if (list) {
            var siblingItems = list.querySelectorAll('.faq-minimal-item');
            siblingItems.forEach(function(el) {
                el.classList.remove('is-open');
                var button = el.querySelector('.faq-minimal-btn');
                if (button) button.setAttribute('aria-expanded', 'false');
            });
        }

        // Toggle selected item
        if (!isOpen) {
            item.classList.add('is-open');
            btn.setAttribute('aria-expanded', 'true');
        }
    };"""

replacement_script = """    // Modern Split Minimalist FAQ Accordion Toggle
    window.toggleDalalSplitFaq = function(btn) {
        if (!btn) return;
        var item = btn.closest('.faq-minimal-item');
        if (!item) return;
        var list = item.closest('.faq-minimal-list');
        var isOpen = item.classList.contains('is-open');

        // Close other items in the same list for clean accordion behavior
        if (list) {
            var siblingItems = list.querySelectorAll('.faq-minimal-item');
            siblingItems.forEach(function(el) {
                el.classList.remove('is-open');
                var button = el.querySelector('.faq-minimal-btn');
                if (button) button.setAttribute('aria-expanded', 'false');
            });
        }

        // Toggle selected item
        if (!isOpen) {
            item.classList.add('is-open');
            btn.setAttribute('aria-expanded', 'true');
        }
    };

    // Global Delegated click listener for FAQ Accordion items
    document.addEventListener('click', function(e) {
        var btn = e.target.closest('.faq-minimal-btn');
        if (!btn) return;
        e.preventDefault();
        window.toggleDalalSplitFaq(btn);
    });"""

# Normalize \r\n to \n for matching
script_norm = script_content.replace("\r\n", "\n")
target_script_norm = target_script.replace("\r\n", "\n")
if target_script_norm in script_norm:
    script_norm = script_norm.replace(target_script_norm, replacement_script)
    with open(script_path, "w", encoding="utf-8") as f:
        f.write(script_norm)
    print("Successfully patched script.js")
else:
    print("Target not found in script.js")

# 2. Update index.html - Remove duplicate inline script block
index_path = "new/dalalmachine/index.html"
with open(index_path, "r", encoding="utf-8") as f:
    index_content = f.read()

index_norm = index_content.replace("\r\n", "\n")
inline_faq_block = re.search(r"    <!-- FAQ Interactive JavaScript Controller -->.*?<\/script>\n", index_norm, re.DOTALL)
if inline_faq_block:
    index_norm = index_norm.replace(inline_faq_block.group(0), "")
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(index_norm)
    print("Successfully removed duplicate inline script from index.html")
else:
    print("Inline script block not found in index.html")

