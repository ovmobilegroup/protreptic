#!/usr/bin/env python3
"""Fix duplicate 'code field' entries in scenarios_zh.json"""
import json

with open('/opt/data/workspace/Protreptic/scenarios_zh.json', 'r', encoding='utf-8') as f:
    zh = json.load(f)

# Find all "code field" keys
code_field_keys = [k for k in zh.keys() if k == "code field"]
print(f"Found {len(code_field_keys)} 'code field' entries")

# Remove all "code field" entries
for k in code_field_keys:
    del zh[k]

print(f"After removal: {len(zh)} keys")

# Save fixed file
with open('/opt/data/workspace/Protreptic/scenarios_zh.json', 'w', encoding='utf-8') as f:
    json.dump(zh, f, ensure_ascii=False, indent=2)

print("Fixed scenarios_zh.json")