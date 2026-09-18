#!/usr/bin/env python3
import json

# Check tools/modes_data.json
with open('/opt/data/workspace/Protreptic/tools/modes_data.json', 'r', encoding='utf-8') as f:
    modes_tools = json.load(f)

print(f"Tools modes_data: {type(modes_tools)}")
if isinstance(modes_tools, dict):
    print(f"  Keys: {list(modes_tools.keys())[:10]}")
    print(f"  zh modes: {len(modes_tools.get('zh', {}))}")
    print(f"  en modes: {len(modes_tools.get('en', {}))}")
elif isinstance(modes_tools, list):
    print(f"  List length: {len(modes_tools)}")

# Check tools/code_maps.json
with open('/opt/data/workspace/Protreptic/tools/code_maps.json', 'r', encoding='utf-8') as f:
    cm_tools = json.load(f)

print(f"\nTools CODE_MAP: {len(cm_tools.get('CODE_MAP', {}))}")
print(f"Tools CODE_MAP_EN: {len(cm_tools.get('CODE_MAP_EN', {}))}")