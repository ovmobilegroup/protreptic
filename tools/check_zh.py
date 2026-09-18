#!/usr/bin/env python3
import json

with open('/opt/data/workspace/Protreptic/scenarios_zh.json', 'r', encoding='utf-8') as f:
    zh = json.load(f)

print(f'Total keys: {len(zh)}')
dict_entries = {k: v for k, v in zh.items() if isinstance(v, dict) and 'modes' in v and isinstance(v['modes'], list)}
print(f'Dict entries with modes: {len(dict_entries)}')

# Check what are the non-dict entries
non_dict = {k: v for k, v in zh.items() if not (isinstance(v, dict) and 'modes' in v and isinstance(v['modes'], list))}
print(f'Non-dict entries: {len(non_dict)}')
for k, v in list(non_dict.items())[:30]:
    print(f'  {k}: {type(v).__name__} - {str(v)[:100]}')