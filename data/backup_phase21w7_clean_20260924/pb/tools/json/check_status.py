#!/usr/bin/env python3
import json

with open('modes_data.json', 'r') as f:
    md = json.load(f)

lz = [e for e in md if e.get('code', '').startswith('LZ-M')]
print(f'LZ-M entries in modes_data.json: {len(lz)}')
for e in lz:
    print(f'  {e["code"]}: {e["name"][:80]}')

print(f'\nTotal modes_data entries: {len(md)}')

with open('code_maps.json', 'r') as f:
    cm = json.load(f)

print(f'\nH-LZ-001 in code_maps: {"H-LZ-001" in cm}')
print(f'H-LZ-169 in code_maps: {"H-LZ-169" in cm}')
if 'H-LZ-001' in cm:
    e = cm['H-LZ-001']
    print(f'  H-LZ-001 figure: {e.get("figure")}')
    print(f'  H-LZ-001 modes: {e.get("core_thinking_modes", [])}')
if 'H-LZ-169' in cm:
    e = cm['H-LZ-169']
    print(f'  H-LZ-169 figure: {e.get("figure")}')
    print(f'  H-LZ-169 modes: {e.get("core_thinking_modes", [])}')