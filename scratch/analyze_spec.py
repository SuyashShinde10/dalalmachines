# scratch/analyze_spec.py
import re

with open("DALAL_AND_OMPI_57_PAGES_AND_MODULES_MASTER_SPECIFICATION.html", "r", encoding="utf-8") as f:
    html = f.read()

route_headers = re.findall(r'<div class="route-card-header">([\s\S]*?)</div>', html)
print(f"Total route-card-header: {len(route_headers)}")
for idx, rh in enumerate(route_headers):
    # clean tags
    clean = re.sub(r'<[^>]+>', ' ', rh)
    clean = ' '.join(clean.split())
    print(f"R{idx+1}: {clean}")

module_headers = re.findall(r'<div class="module-card-header">([\s\S]*?)</div>', html)
print(f"\nTotal module-card-header: {len(module_headers)}")
for idx, mh in enumerate(module_headers):
    clean = re.sub(r'<[^>]+>', ' ', mh)
    clean = ' '.join(clean.split())
    print(f"M{idx+1}: {clean}")
