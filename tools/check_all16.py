import json
d = json.load(open('scenarios_zh.json'))
print(len(d))
for code in ['AO-NET-001', 'CF-BOG-001', 'CG-SAS-001', 'CM-AHM-001', 'GA-BON-001', 'GQ-OBI-001', 'ST-CAC-001', 'TD-HIS-001',
             'BI-NKU-001', 'MW-BAN-001', 'ZM-KAU-001', 'ZA-MBK-001', 'ZA-ZUM-001', 'ZW-MUG-001', 'BW-KHA-001', 'NA-NUJ-001']:
    if code in d:
        print(f"FOUND: {code} - modes={d[code].get('modes')}")
    else:
        print(f"MISSING: {code}")