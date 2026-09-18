#!/usr/bin/env python3
import json, sys

with open('/opt/data/workspace/Protreptic/modes_data.json', 'r') as f:
    data = json.load(f)

# Check structure
if isinstance(data, dict):
    all_codes = list(data.keys())
else:
    all_codes = [item.get('code', '?') for item in data]

zeng = [c for c in all_codes if 'Zeng' in str(c) or 'ZX' in str(c)]
print(f'Total codes: {len(all_codes)}')
print(f'Zengzi-related: {zeng}')

# Show first entry structure for schema reference
if isinstance(data, dict):
    sample = list(data.values())[0] if data else {}
else:
    sample = data[0] if data else {}

print(f'\nSample type: {type(sample).__name__}')
if isinstance(sample, dict):
    print(f'Sample keys: {list(sample.keys())[:15]}')

# Print all codes for reference
print('\nAll codes:')
for c in sorted(all_codes):
    print(f'  {c}')