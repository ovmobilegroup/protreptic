import json

# Check root modes_data.json for all mode keys
with open('../../modes_data.json') as fp:
    d = json.load(fp)
print(f"modes_data.json (root) zh keys (last 30):")
zh_keys = sorted([k for k in d['zh'].keys()])
for k in zh_keys[-30:]:
    print(f"  {k}")

print(f"\nmodes_data.json (root) en keys (last 30):")
en_keys = sorted([k for k in d['en'].keys()])
for k in en_keys[-30:]:
    print(f"  {k}")

# Check tools modes_data.json
with open('../modes_data.json') as fp:
    d = json.load(fp)
print(f"\nmodes_data.json (tools) zh keys (last 30):")
zh_keys = sorted([k for k in d['zh'].keys()])
for k in zh_keys[-30:]:
    print(f"  {k}")

print(f"\nmodes_data.json (tools) en keys (last 30):")
en_keys = sorted([k for k in d['en'].keys()])
for k in en_keys[-30:]:
    print(f"  {k}")

# Find M634-M645 in either
print("\nSearching for M634-M645:")
for k in zh_keys:
    if k.startswith('M6') and int(k[1:]) >= 634 and int(k[1:]) <= 645:
        print(f"  ROOT zh: {k}")
for k in en_keys:
    if k.startswith('M6') and int(k[1:]) >= 634 and int(k[1:]) <= 645:
        print(f"  ROOT en: {k}")