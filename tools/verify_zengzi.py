#!/usr/bin/env python3
import json

with open('/opt/data/workspace/Protreptic/modes_data.json', 'r') as f:
    data = json.load(f)

# Find H-ZX-001 entry and verify
found_entry = None
if isinstance(data, dict):
    found_entry = data.get('H-ZX-001')
else:
    for item in data:
        if isinstance(item, dict) and item.get('code') == 'H-ZX-001':
            found_entry = item
            break

if found_entry:
    print("H-ZX-001 verification:")
    print(f"  figure_name_zh: {found_entry.get('figure_name_zh')}")
    print(f"  figure_name_en: {found_entry.get('figure_name_en')}")
    print(f"  era: {found_entry.get('era')}")
    print(f"  birth_year: {found_entry.get('birth_year')}")
    print(f"  death_year: {found_entry.get('death_year')}")
    modes = found_entry.get('thinking_modes', [])
    print(f"  Mode count: {len(modes)}")
    for m in modes:
        print(f"    {m['id']}: {m['name_zh']}")
    
    # Also verify the modes file standalone
    with open('/opt/data/workspace/Protreptic/H-ZX-001_modes.json', 'r') as f2:
        modes_json = json.load(f2)
    print(f"\nStandalone H-ZX-001_modes.json:")
    print(f"  code: {modes_json.get('code')}")
    core_modes = modes_json.get('core_modes', [])
    print(f"  Core mode IDs: {core_modes}")
    
    # Total entries count
    total = len(data) if isinstance(data, list) else len(data.keys())
    print(f"\nTotal entries in modes_data.json: {total}")
else:
    print("ERROR: H-ZX-001 not found!")