#!/usr/bin/env python3
"""Update modes_data.json with Zengzi (H-ZX-001) entry."""
import json

# Read existing data
with open('/opt/data/workspace/Protreptic/modes_data.json', 'r') as f:
    data = json.load(f)

# Read new Zengzi main entry
with open('/opt/data/workspace/Protreptic/H-ZX-001.json', 'r') as f:
    zengzi_main = json.load(f)

# Read Zengzi modes entry
with open('/opt/data/workspace/Protreptic/H-ZX-001_modes.json', 'r') as f:
    zengzi_modes = json.load(f)

# Merge into modes_data.json (dict-keyed format with 'code' key inside each entry)
# Find and replace existing H-ZX-001 if it exists, or add new entry

if isinstance(data, dict):
    # Dict-keyed format: {code: entry_dict}
    data['H-ZX-001'] = zengzi_main
elif isinstance(data, list):
    # List format: [entry_dict1, entry_dict2, ...]
    # Check if H-ZX-001 already exists and replace it
    found = False
    for i, item in enumerate(data):
        if isinstance(item, dict) and item.get('code') == 'H-ZX-001':
            data[i] = zengzi_main
            found = True
            break
    if not found:
        data.append(zengzi_main)

# Write back with proper formatting (preserve existing format type)
if isinstance(data, dict):
    # For dict-keyed: maintain sorted order by code for consistency
    sorted_keys = sorted(data.keys())
    ordered_data = {k: data[k] for k in sorted_keys}
else:
    # For list: keep as-is (order matters in lists)
    pass

with open('/opt/data/workspace/Protreptic/modes_data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# Print summary
if isinstance(data, dict):
    print(f"Dict format: {len(data)} total entries")
else:
    print(f"List format: {len(data)} total entries")

# Verify the new entry
if isinstance(data, dict):
    entry = data.get('H-ZX-001')
else:
    entry = None
    for item in data:
        if isinstance(item, dict) and item.get('code') == 'H-ZX-001':
            entry = item
            break

if entry:
    print(f"\nNew Zengzi entry added successfully:")
    print(f"  Code: {entry.get('code')}")
    print(f"  Name (ZH): {entry.get('figure_name_zh')}")
    if 'thinking_modes' in entry:
        mode_count = len(entry['thinking_modes'])
        print(f"  Mode count: {mode_count}")
        mode_ids = [m['id'] for m in entry['thinking_modes']]
        print(f"  Mode IDs: {mode_ids}")
else:
    print("ERROR: Could not verify new entry!")

# Save backup
import shutil, os, time
backup_path = '/opt/data/workspace/Protreptic/modes_data.json.bak_zx_{}'.format(int(time.time()))
shutil.copy2('/opt/data/workspace/Protreptic/modes_data.json', backup_path)
print(f"\nBackup saved: {backup_path}")

# Also update the release version if it exists
release_path = '/opt/data/workspace/Protreptic/release/v2.0.0/modes_data.json'
if os.path.exists(release_path):
    shutil.copy2('/opt/data/workspace/Protreptic/modes_data.json', release_path)
    print("Release version updated")

# Update data/ directory if it exists
data_path = '/opt/data/workspace/Protreptic/data/modes_data.json'
if os.path.exists(data_path):
    shutil.copy2('/opt/data/workspace/Protreptic/modes_data.json', data_path)
    print("Data directory version updated")