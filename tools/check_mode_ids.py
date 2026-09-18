#!/usr/bin/env python3
import json

with open('/opt/data/workspace/Protreptic/modes_data.json', 'r') as f:
    data = json.load(f)

# Collect all mode IDs used across entries
all_mode_ids = set()
if isinstance(data, list):
    for item in data:
        if isinstance(item, dict) and 'thinking_modes' in item:
            for mode in item['thinking_modes']:
                all_mode_ids.add(mode.get('id', ''))

print(f"Total mode IDs in use: {len(all_mode_ids)}")
for m in sorted(all_mode_ids):
    print(f"  {m}")

# Also check H-MZ-001 modes (from the parent task's output)
with open('/opt/data/kanban/boards/protreptic/workspaces/t_64303484/H-MZ-001.json', 'r') as f:
    mz_data = json.load(f)

print(f"\nM-Zengzi (actually Mengzi) mode IDs: {[m['id'] for m in mz_data.get('thinking_modes', [])]}")