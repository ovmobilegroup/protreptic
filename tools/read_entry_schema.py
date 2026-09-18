#!/usr/bin/env python3
import json

with open('/opt/data/workspace/Protreptic/modes_data.json', 'r') as f:
    data = json.load(f)

if isinstance(data, dict):
    for code, entry in data.items():
        if 'H-KZ-001' in str(code):
            print(f"=== {code} ===")
            print(json.dumps(entry, ensure_ascii=False, indent=2))
            break
else:
    for item in data:
        if isinstance(item, dict) and item.get('code') == 'H-KZ-001':
            print(json.dumps(item, ensure_ascii=False, indent=2))
            break