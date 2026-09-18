#!/usr/bin/env python3
import json

# Check what the merged scenarios_zh.json looks like
with open('/opt/data/kanban/boards/protreptic/attachments/t_barbosa_merge_1787640880_3/scenarios_zh.json', 'r', encoding='utf-8') as f:
    zh_merged = json.load(f)

print(f"Merged ZH total: {len(zh_merged)}")

# Count dict entries with modes
dict_entries = {k: v for k, v in zh_merged.items() if isinstance(v, dict) and 'modes' in v and isinstance(v['modes'], list)}
print(f"Merged ZH dict entries: {len(dict_entries)}")

# Count by prefix
from collections import Counter
prefixes = Counter()
for k in dict_entries.keys():
    if '-' in k:
        prefix = k.split('-')[0]
        prefixes[prefix] += 1
    else:
        prefixes['other'] += 1

for p, c in sorted(prefixes.items(), key=lambda x: -x[1]):
    print(f"  {p}: {c}")

# Also check the modes in the merged scenarios
all_modes = set()
for v in dict_entries.values():
    for m in v['modes']:
        all_modes.add(m)
print(f"\nTotal unique modes used: {len(all_modes)}")
print(f"Modes: {sorted(all_modes)[:50]}")