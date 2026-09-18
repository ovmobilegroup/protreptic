#!/usr/bin/env python3
import json

# Check tools/scenarios_en.json
with open('/opt/data/workspace/Protreptic/tools/scenarios_en.json', 'r', encoding='utf-8') as f:
    en_tools = json.load(f)

print(f"Tools EN total: {len(en_tools)}")

dict_entries = {k: v for k, v in en_tools.items() if isinstance(v, dict) and 'modes' in v and isinstance(v['modes'], list)}
print(f"Tools EN dict entries: {len(dict_entries)}")

# Check for the 6 new entries
new_entries = ['IN-ASH-001', 'IN-KAU-001', 'IN-TAG-001', 'IN-GAN-001', 'IN-IGD-001', 'JP-TOK-001']
for code in new_entries:
    if code in en_tools:
        print(f"FOUND: {code}")
    else:
        print(f"MISSING: {code}")