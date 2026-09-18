#!/usr/bin/env python3
import json

# Check code_maps.json
with open('/opt/data/kanban/boards/protreptic/attachments/t_barbosa_merge_1787640880_3/code_maps.json', 'r', encoding='utf-8') as f:
    cm_merged = json.load(f)

with open('/opt/data/workspace/Protreptic/code_maps.json', 'r', encoding='utf-8') as f:
    cm_root = json.load(f)

with open('/opt/data/workspace/Protreptic/tools/code_maps.json', 'r', encoding='utf-8') as f:
    cm_tools = json.load(f)

print(f"Merged CODE_MAP: {len(cm_merged.get('CODE_MAP', {}))}, CODE_MAP_EN: {len(cm_merged.get('CODE_MAP_EN', {}))}")
print(f"Root CODE_MAP: {len(cm_root.get('CODE_MAP', {}))}, CODE_MAP_EN: {len(cm_root.get('CODE_MAP_EN', {}))}")
print(f"Tools CODE_MAP: {len(cm_tools.get('CODE_MAP', {}))}, CODE_MAP_EN: {len(cm_tools.get('CODE_MAP_EN', {}))}")

# Check for the 6 new entries
new_entries = ['IN-ASH-001', 'IN-KAU-001', 'IN-TAG-001', 'IN-GAN-001', 'IN-IGD-001', 'JP-TOK-001']
for code in new_entries:
    in_cm = code in cm_merged.get('CODE_MAP', {})
    in_cm_en = code in cm_merged.get('CODE_MAP_EN', {})
    in_cmr = code in cm_root.get('CODE_MAP', {})
    in_cmre = code in cm_root.get('CODE_MAP_EN', {})
    in_cmt = code in cm_tools.get('CODE_MAP', {})
    in_cmte = code in cm_tools.get('CODE_MAP_EN', {})
    print(f"  {code}: merged=({in_cm},{in_cm_en}) root=({in_cmr},{in_cmre}) tools=({in_cmt},{in_cmte})")