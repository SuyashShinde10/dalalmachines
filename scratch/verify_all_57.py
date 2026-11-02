import re

with open('DALAL_AND_OMPI_57_PAGES_AND_MODULES_MASTER_SPECIFICATION.html', 'r', encoding='utf-8') as f:
    text = f.read()

routes = re.findall(r'<span class="unit-id"[^>]*>(ROUTE \d+)</span>\s*<span class="unit-title">([^<]+)</span>', text)
modules = re.findall(r'<span class="unit-id"[^>]*>(MOD(?:ULE)? \d+)</span>\s*<span class="unit-title">([^<]+)</span>', text)

print(f"Total Routes: {len(routes)}")
for r_id, r_name in routes:
    print(f"  {r_id}: {r_name}")

print(f"\nTotal Modules: {len(modules)}")
for m_id, m_name in modules:
    print(f"  {m_id}: {m_name}")

