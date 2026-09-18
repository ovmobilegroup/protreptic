import json

with open('scenarios_zh.json', 'r') as f:
    data = json.load(f)

missing = []
for code in ['AO-NET-001', 'CF-BOG-001', 'CM-AHM-001', 'ST-CAC-001', 'TD-HIS-001']:
    if code not in data:
        missing.append(code)
    else:
        print(f"FOUND: {code}")

print(f"Missing: {missing}")