#!/usr/bin/env python3
import json

# Check root directory files
with open('/opt/data/workspace/Protreptic/scenarios_zh.json', 'r', encoding='utf-8') as f:
    zh_root = json.load(f)

with open('/opt/data/workspace/Protreptic/scenarios_en.json', 'r', encoding='utf-8') as f:
    en_root = json.load(f)

print(f"Root ZH: {len(zh_root)}")
print(f"Root EN: {len(en_root)}")

# Check for the 6 new entries from batch 4
new_entries = ['IN-ASH-001', 'IN-KAU-001', 'IN-TAG-001', 'IN-GAN-001', 'IN-IGD-001', 'JP-TOK-001']

for code in new_entries:
    in_zh = code in zh_root
    in_en = code in en_root
    print(f"  {code}: ZH={in_zh}, EN={in_en}")

# Check tools directory
with open('/opt/data/workspace/Protreptic/tools/scenarios_zh.json', 'r', encoding='utf-8') as f:
    zh_tools = json.load(f)

with open('/opt/data/workspace/Protreptic/tools/scenarios_en.json', 'r', encoding='utf-8') as f:
    en_tools = json.load(f)

print(f"\nTools ZH: {len(zh_tools)}")
print(f"Tools EN: {len(en_tools)}")

for code in new_entries:
    in_zh = code in zh_tools
    in_en = code in en_tools
    print(f"  {code}: ZH={in_zh}, EN={in_en}")