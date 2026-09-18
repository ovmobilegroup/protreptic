#!/usr/bin/env python3
import json

with open('/opt/data/kanban/boards/protreptic/attachments/t_barbosa_merge_1787640880_3/modes_data.json', 'r', encoding='utf-8') as f:
    modes = json.load(f)

print(f"Type: {type(modes)}")
if isinstance(modes, list):
    print(f"Length: {len(modes)}")
    for item in modes:
        print(f"  {item.get('code', 'N/A')}: {item.get('name', 'N/A')}")