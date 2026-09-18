#!/usr/bin/env python3
import json

with open('/opt/data/kanban/boards/protreptic/attachments/t_barbosa_merge_1787640880_3/scenarios_en.json', 'r', encoding='utf-8') as f:
    en = json.load(f)

# Check for the 6 new entries from batch 4
new_entries = ['IN-ASH-001', 'IN-KAU-001', 'IN-TAG-001', 'IN-GAN-001', 'IN-IGD-001', 'JP-TOK-001']

for code in new_entries:
    if code in en:
        print(f"FOUND: {code}")
        print(f"  Keys: {list(en[code].keys()) if isinstance(en[code], dict) else 'NOT DICT'}")
    else:
        print(f"MISSING: {code}")

print(f"\nTotal keys in merged EN: {len(en)}")