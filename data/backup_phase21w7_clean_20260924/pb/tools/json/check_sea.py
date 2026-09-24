import json

# Check root scenarios_zh.json for SEA country codes
with open('../../scenarios_zh.json') as fp:
    d = json.load(fp)

# Look for SEA country codes
sea_codes = [k for k in d.keys() if k.startswith(('ID-', 'MY-', 'TH-', 'VN-', 'PH-', 'SG-', 'MM-', 'LA-', 'KH-', 'BN-', 'TL-'))]
print(f"SEA codes in root scenarios_zh.json: {len(sea_codes)}")
for c in sorted(sea_codes):
    print(f"  {c}")

# Also check for the 12 Iberia/Greece codes
iberia_codes = [k for k in d.keys() if k.startswith(('ES-', 'PT-', 'GR-'))]
print(f"\nIberia/Greece codes in root scenarios_zh.json: {len(iberia_codes)}")
for c in sorted(iberia_codes):
    print(f"  {c}")

# Total count
print(f"\nTotal scenarios in root scenarios_zh.json: {len(d)}")

# Check tools scenarios_zh.json
with open('../scenarios_zh.json') as fp:
    d = json.load(fp)
print(f"\nTotal scenarios in tools scenarios_zh.json: {len(d)}")
sea_codes = [k for k in d.keys() if k.startswith(('ID-', 'MY-', 'TH-', 'VN-', 'PH-', 'SG-', 'MM-', 'LA-', 'KH-', 'BN-', 'TL-'))]
print(f"SEA codes in tools scenarios_zh.json: {len(sea_codes)}")
for c in sorted(sea_codes):
    print(f"  {c}")