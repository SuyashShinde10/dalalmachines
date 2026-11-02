import json, re

with open('new/dalalmachine/js/catalog-data.js', 'r', encoding='utf-8') as f:
    text = f.read()

# Match machines in DALAL_MACHINES
models = re.findall(r'"model":\s*"([^"]+)"', text)
makes = re.findall(r'"make":\s*"([^"]+)"', text)
cats = re.findall(r'"categoryName":\s*"([^"]+)"', text)
names = re.findall(r'"name":\s*"([^"]+)"', text)

print("Unique Models (longest first):")
for m in sorted(set(models), key=len, reverse=True)[:15]:
    print(f"  [{len(m)}] {m}")

print("\nLongest Category + Make combinations:")
combos = set()
for c, mk in zip(cats, makes):
    combos.add(f"{c} • {mk}")
for combo in sorted(combos, key=len, reverse=True)[:10]:
    print(f"  [{len(combo)}] {combo}")

