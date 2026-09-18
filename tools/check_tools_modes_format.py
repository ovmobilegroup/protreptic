#!/usr/bin/env python3
import json

# Check the original tools/modes_data.json before copy
with open('/opt/data/workspace/Protreptic/tools/modes_data.json', 'r', encoding='utf-8') as f:
    modes = json.load(f)

print(f"Type: {type(modes)}")
if isinstance(modes, dict):
    print(f"Keys: {list(modes.keys())}")
    for k, v in list(modes.items())[:5]:
        print(f"  {k}: {type(v)} - {str(v)[:100]}")