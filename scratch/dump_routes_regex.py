with open('DALAL_WEBSITE_ADMIN_AND_USER_FLOW_GUIDE.html', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

import re
matches = re.findall(r'Route\s+(\d+)[:\s]+([^<\(\n]+)(?:<span class="code-pill">|\()([^\)<\n]+)', text)
for num, name, path in matches:
    print(f"Route {num}: {name.strip()} ({path.strip()})")
print(f"Total routes matched: {len(matches)}")

