with open('DALAL_WEBSITE_ADMIN_AND_USER_FLOW_GUIDE.html', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

import re
pattern = r'<div class="route-title">([^<]+)</div>\s*<div class="route-path">([^<]+)</div>\s*<div class="route-purpose"><strong>Business Purpose:</strong>\s*([^<]+)</div>\s*<div class="route-features"><strong>Key Operational Features:</strong>\s*([^<]+)</div>'
matches = re.findall(pattern, text)
for i, (title, path, purpose, feats) in enumerate(matches, 1):
    print(f"{i}. {title.strip()} ({path.strip()})")
    print(f"   Why: {purpose.strip()[:100]}...")
    print(f"   What: {feats.strip()[:100]}...")
print(f"Total routes parsed: {len(matches)}")

