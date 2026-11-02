# scratch/find_currency_shipping.py
with open('scratch/build_enterprise_specification_v2.py', 'r', encoding='utf-8') as f:
    text = f.read()

for term in ["Euro", "Landed", "Container", "Shipment", "Freight", "Customs"]:
    print(f"=== Matches for {term} ===")
    lines = text.split('\n')
    for i, l in enumerate(lines):
        if term.lower() in l.lower() and ('"id"' in l or '"title"' in l):
            print(f"Line {i}: {l.strip()}")

