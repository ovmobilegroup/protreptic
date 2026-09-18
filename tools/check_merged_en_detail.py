#!/usr/bin/env python3
import json

# Check merged scenarios_en.json
with open('/opt/data/kanban/boards/protreptic/attachments/t_barbosa_merge_1787640880_3/scenarios_en.json', 'r', encoding='utf-8') as f:
    en_merged = json.load(f)

print(f"Merged EN total: {len(en_merged)}")

dict_entries = {k: v for k, v in en_merged.items() if isinstance(v, dict) and 'modes' in v and isinstance(v['modes'], list)}
print(f"Merged EN dict entries: {len(dict_entries)}")

# Count by prefix
from collections import Counter
prefixes = Counter()
for k in dict_entries.keys():
    if '-' in k:
        prefix = k.split('-')[0]
        prefixes[prefix] += 1
    else:
        prefixes['other'] += 1

for p, c in sorted(prefixes.items(), key=lambda x: -x[1])[:30]:
    print(f"  {p}: {c}")

# Also check the 6 new entries
new_entries = ['IN-ASH-001', 'IN-KAU-001', 'IN-TAG-001', 'IN-GAN-001', 'IN-IGD-001', 'JP-TOK-001']
for code in new_entries:
    if code in en_merged:
        print(f"FOUND: {code}")
    else:
        print(f"MISSING: {code}")