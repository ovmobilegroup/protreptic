import json

# Load from the merged attachments
zh = json.load(open('/opt/data/kanban/boards/protreptic/attachments/t_barbosa_merge_1787640880_3/scenarios_zh.json'))
en = json.load(open('/opt/data/kanban/boards/protreptic/attachments/t_barbosa_merge_1787640880_3/scenarios_en.json'))

print(f"ZH keys: {len(zh)}")
print(f"EN keys: {len(en)}")

# Find missing EN keys
missing_en = [k for k in zh if k not in en]
print(f"\nMissing EN ({len(missing_en)}):")
for k in missing_en:
    print(f"  {k}")

# Find missing ZH keys
missing_zh = [k for k in en if k not in zh]
print(f"\nMissing ZH ({len(missing_zh)}):")
for k in missing_zh:
    print(f"  {k}")

# Check for 'code field' entry
if 'code field' in zh:
    print("\n'code field' in ZH:", zh['code field'])
if 'code field' in en:
    print("'code field' in EN:", en['code field'])