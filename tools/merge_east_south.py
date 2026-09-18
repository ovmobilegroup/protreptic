import json

# Load the fixed scenarios_zh.json (1015 entries)
with open('/opt/data/workspace/Protreptic/tools/scenarios_zh.json.fixed', 'r') as f:
    fixed = json.load(f)

# Load the East Africa entries from the authoritative file
with open('/opt/data/kanban/boards/protreptic/workspaces/t_922bef56/scenarios_zh.json', 'r') as f:
    auth = json.load(f)

# Get the East Africa entries (AO-NET through TD-HIS)
east_codes = ['AO-NET-001', 'CF-BOG-001', 'CG-SAS-001', 'CM-AHM-001', 'GA-BON-001', 'GQ-OBI-001', 'ST-CAC-001', 'TD-HIS-001']

for code in east_codes:
    if code in auth:
        fixed[code] = auth[code]
        print(f"Added {code} from authoritative")
    else:
        print(f"NOT FOUND IN AUTH: {code}")

# Also add Southern Africa if missing
south_codes = ['BI-NKU-001', 'MW-BAN-001', 'ZM-KAU-001', 'ZA-MBK-001', 'ZA-ZUM-001', 'ZW-MUG-001', 'BW-KHA-001', 'NA-NUJ-001']
for code in south_codes:
    if code in auth:
        fixed[code] = auth[code]
        print(f"Added/Updated {code} from authoritative")
    else:
        print(f"NOT FOUND IN AUTH: {code}")

print(f"\nTotal entries after merge: {len(fixed)}")

# Save back
with open('/opt/data/workspace/Protreptic/tools/scenarios_zh.json', 'w', encoding='utf-8') as f:
    json.dump(fixed, f, ensure_ascii=False, indent=2)

print("Saved merged scenarios_zh.json")