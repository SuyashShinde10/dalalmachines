import subprocess, os

# Create test script to update and verify contact.html
contact_path = 'new/dalalmachine/contact.html'
with open(contact_path, 'r', encoding='utf-8') as f:
    c = f.read()

# Let's inspect line 288-348
import re
old_card_pattern = r'<div class="contact-form-card"[^>]*>.*?</div>\s*</div>\s*</div>\s*<!-- Dual Interactive'
# Let's see what is inside
match = re.search(r'(<div class="contact-form-card"[^>]*>)(.*?)(</div>\s*</div>\s*</div>\s*<!-- Dual Interactive)', c, re.DOTALL)
if match:
    print("Found contact-form-card block! Length:", len(match.group(2)))
else:
    print("Not found with regex")

