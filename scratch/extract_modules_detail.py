# scratch/extract_modules_detail.py
import re, json

with open("DALAL_AND_OMPI_57_PAGES_AND_MODULES_MASTER_SPECIFICATION.html", "r", encoding="utf-8") as f:
    html = f.read()

# find module cards
module_cards = re.findall(r'<div class="module-card">([\s\S]*?)</div>\s*</div>\s*(?:<!--|</div>|<div class="page")', html)
print(f"Extracted {len(module_cards)} raw module blocks")

modules_data = []
for idx, card in enumerate(module_cards):
    header_m = re.search(r'<div class="module-card-header">([\s\S]*?)</div>', card)
    header = re.sub(r'<[^>]+>', ' ', header_m.group(1)).strip() if header_m else f"Module {idx+1}"
    header = ' '.join(header.split())
    
    # Extract sections: Objective, Workflow, Technical Specs, Database Schema
    obj_m = re.search(r'<strong>Business Objective[^:<]*:?</strong>\s*([^<]+)', card, re.I)
    workflow_m = re.search(r'<strong>Operational Workflow[^:<]*:?</strong>\s*([^<]+)', card, re.I)
    
    modules_data.append({
        "index": idx + 1,
        "title": header,
        "raw": card[:400]
    })

print(f"Parsed {len(modules_data)} modules:")
for m in modules_data:
    print(f"{m['index']}. {m['title']}")

