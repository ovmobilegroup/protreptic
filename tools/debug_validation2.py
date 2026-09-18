import json

with open('scenarios_zh.json', 'r', encoding='utf-8') as f:
    zh = json.load(f)
with open('scenarios_en.json', 'r', encoding='utf-8') as f:
    en = json.load(f)

# Count valid dict entries
zh_valid = {k: v for k, v in zh.items() if isinstance(v, dict)}
en_valid = {k: v for k, v in en.items() if isinstance(v, dict)}

print(f"Total keys in zh: {len(zh)}")
print(f"Valid dict entries in zh: {len(zh_valid)}")
print(f"Invalid (string) entries in zh: {len(zh) - len(zh_valid)}")

print(f"\nTotal keys in en: {len(en)}")
print(f"Valid dict entries in en: {len(en_valid)}")
print(f"Invalid (string) entries in en: {len(en) - len(en_valid)}")

# List the invalid keys
invalid_zh = [k for k, v in zh.items() if not isinstance(v, dict)]
invalid_en = [k for k, v in en.items() if not isinstance(v, dict)]
print(f"\nInvalid keys in zh: {invalid_zh}")
print(f"Invalid keys in en: {invalid_en}")

# Check the 22 new entries
new_entries = ['PK-ISL-001', 'PK-SUF-001', 'BD-LIB-001', 'LK-CIV-001', 'NP-HIM-001', 
               'AF-TRI-001', 'MV-ISL-001', 'BT-GNH-001']

print("\n=== NEW ENTRIES STRUCTURE ===")
for code in new_entries:
    if code in zh_valid:
        v = zh_valid[code]
        print(f"\n{code}:")
        print(f"  Keys: {list(v.keys())}")
        for fk, fv in v.items():
            if isinstance(fv, str):
                print(f"  {fk}: {fv[:100]}...")
            else:
                print(f"  {fk}: {fv}")