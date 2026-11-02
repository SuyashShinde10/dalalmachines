# Clean fix for FAQ Accordion:
# 1. Remove inline onclick="toggleDalalSplitFaq(this)" from all buttons in index.html and services.html
# 2. Implement robust single-execution event delegation with latch/lock (no double firing)
# 3. Handle smooth open/close

def fix_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Remove inline onclick handlers
    old_btn = 'class="faq-minimal-btn" onclick="toggleDalalSplitFaq(this)"'
    new_btn = 'class="faq-minimal-btn"'
    
    count = content.count(old_btn)
    if count > 0:
        content = content.replace(old_btn, new_btn)
        print(f"Removed {count} inline onclick attributes in {path}")
    else:
        print(f"No inline onclick attributes found in {path}")

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

fix_file('new/dalalmachine/index.html')
fix_file('new/dalalmachine/services.html')

