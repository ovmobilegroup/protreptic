import json

with open('scenarios_en.json') as f:
    en = json.load(f)

# Check for some of the missing codes in EN
missing_codes = ['AF-TRI-001', 'AO-NET-001', 'BD-LIB-001', 'BT-GNH-001', 'CF-BOG-001', 'CM-AHM-001', 'EE-MER-001', 'IL-HAVR-001-TEST', 'LK-CIV-001', 'MO-NAT-001', 'MV-ISL-001', 'NP-HIM-001', 'PK-ISL-001', 'PK-SUF-001', 'QA-ENE-001', 'ST-CAC-001', 'TD-HIS-001', 'TN-DEM-001']

for k in missing_codes:
    v = en.get(k)
    print(f"\n=== {k} ===")
    if v is None:
        print("NOT FOUND IN EN")
    else:
        print(f"Type: {type(v)}")
        if isinstance(v, dict):
            print(f"Keys: {list(v.keys())}")
            if 'modes' in v:
                print(f"Modes: {v['modes']}")