import json

with open('scenarios_zh.json') as f:
    zh = json.load(f)

# Check the 19 ZH-only keys
zh_only = ['AF-TRI-001', 'AO-NET-001', 'BD-LIB-001', 'BT-GNH-001', 'CF-BOG-001', 'CM-AHM-001', 'EE-MER-001', 'IL-HAVR-001-TEST', 'LK-CIV-001', 'MO-NAT-001', 'MV-ISL-001', 'NP-HIM-001', 'PK-ISL-001', 'PK-SUF-001', 'QA-ENE-001', 'ST-CAC-001', 'TD-HIS-001', 'TN-DEM-001', 'code field']

for k in zh_only:
    v = zh.get(k)
    print(f"\n=== {k} ===")
    print(f"Type: {type(v)}")
    if isinstance(v, dict):
        print(f"Keys: {list(v.keys())}")
        if 'modes' in v:
            print(f"Modes: {v['modes']}")
        if 'code' in v:
            print(f"Code: {v['code']}")
    else:
        print(f"Value: {v}")