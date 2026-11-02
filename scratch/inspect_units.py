# scratch/inspect_units.py
with open('scratch/build_enterprise_specification_v2.py', 'r', encoding='utf-8') as f:
    text = f.read()

import json

# Find UNIT-10, 15, 16, 24
for uid in ["UNIT-10", "UNIT-15", "UNIT-16", "UNIT-24"]:
    pos = text.find(f'"id": "{uid}"')
    if pos != -1:
        start = text.rfind('{', 0, pos)
        end = text.find('}', pos) + 1
        print(f"=== {uid} ===")
        print(text[start:end])

# Find ERP-MOD-04, 07, 18
for mid in ["ERP-MOD-04", "ERP-MOD-07", "ERP-MOD-18"]:
    pos = text.find(f'"id": "{mid}"')
    if pos != -1:
        start = text.rfind('{', 0, pos)
        end = text.find('}', pos) + 1
        print(f"=== {mid} ===")
        print(text[start:end])

