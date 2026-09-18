import json

# Check which mode numbers are missing
with open('/opt/data/workspace/Protreptic/tools/modes_data.json', 'r', encoding='utf-8') as f:
    tools_modes = json.load(f)

zh_modes = tools_modes['zh']
numeric_keys = set(int(k) for k in zh_modes.keys() if not k.startswith('M') and k.isdigit())

print(f"Total modes: {len(numeric_keys)}")
print(f"Min: {min(numeric_keys)}, Max: {max(numeric_keys)}")

all_numbers = set(range(1, max(numeric_keys) + 1))
missing = all_numbers - numeric_keys
print(f"Missing numbers: {sorted(missing)}")
print(f"Count missing: {len(missing)}")

# Check en modes
en_modes = tools_modes['en']
en_numeric = set(int(k) for k in en_modes.keys() if not k.startswith('M') and k.isdigit())
print(f"\nEN modes: {len(en_numeric)}")
en_missing = all_numbers - en_numeric
print(f"EN missing: {sorted(en_missing)}")

# Check root modes_data.json
with open('/opt/data/workspace/Protreptic/modes_data.json', 'r', encoding='utf-8') as f:
    root_modes = json.load(f)

if isinstance(root_modes, dict):
    for lang in ['zh', 'en']:
        if lang in root_modes:
            modes = root_modes[lang]
            numeric = set(int(k) for k in modes.keys() if not k.startswith('M') and k.isdigit())
            print(f"\nRoot {lang}: {len(numeric)} modes")
            root_missing = all_numbers - numeric
            print(f"Root {lang} missing: {sorted(root_missing)}")