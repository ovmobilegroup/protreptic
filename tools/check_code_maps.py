import json

with open('code_maps.json') as f:
    cm = json.load(f)

cm = cm.get('CODE_MAP', {})
cm_en = cm.get('CODE_MAP_EN', {})

missing_codes = ['AF-TRI-001', 'AO-NET-001', 'BD-LIB-001', 'BT-GNH-001', 'CF-BOG-001', 'CM-AHM-001', 'EE-MER-001', 'IL-HAVR-001-TEST', 'LK-CIV-001', 'MO-NAT-001', 'MV-ISL-001', 'NP-HIM-001', 'PK-ISL-001', 'PK-SUF-001', 'QA-ENE-001', 'ST-CAC-001', 'TD-HIS-001', 'TN-DEM-001']

for k in missing_codes:
    in_cm = k in cm
    in_cm_en = k in cm_en
    print(f"{k}: CODE_MAP={in_cm}, CODE_MAP_EN={in_cm_en}")