#!/usr/bin/env python3
import json

# Check scenario_tags.json
with open('/opt/data/kanban/boards/protreptic/attachments/t_barbosa_merge_1787640880_3/scenario_tags.json', 'r', encoding='utf-8') as f:
    st_merged = json.load(f)

with open('/opt/data/workspace/Protreptic/scenario_tags.json', 'r', encoding='utf-8') as f:
    st_root = json.load(f)

with open('/opt/data/workspace/Protreptic/tools/scenario_tags.json', 'r', encoding='utf-8') as f:
    st_tools = json.load(f)

print(f"Merged scenario_tags: {len(st_merged)}")
print(f"Root scenario_tags: {len(st_root)}")
print(f"Tools scenario_tags: {len(st_tools)}")

# Check for the 6 new entries
new_entries = ['IN-ASH-001', 'IN-KAU-001', 'IN-TAG-001', 'IN-GAN-001', 'IN-IGD-001', 'JP-TOK-001']
for code in new_entries:
    in_st = code in st_merged
    in_str = code in st_root
    in_stt = code in st_tools
    print(f"  {code}: merged={in_st} root={in_str} tools={in_stt}")