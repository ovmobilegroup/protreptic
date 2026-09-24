import json

# Check root scenario_tags.json in detail
with open('/opt/data/workspace/Protreptic/scenario_tags.json') as fp:
    d = json.load(fp)
print(f"scenario_tags.json (root): {type(d)}")
print(f"  keys: {list(d.keys())}")
for k, v in d.items():
    if isinstance(v, (list, dict)):
        print(f"    {k}: {len(v)}")
    else:
        print(f"    {k}: {type(v)} = {v}")

# Check if tags is a dict with scenario codes as keys
if 'tags' in d and isinstance(d['tags'], dict):
    print(f"\n  tags dict has {len(d['tags'])} entries")
    sea_codes = [k for k in d['tags'].keys() if k.startswith(('ID-', 'MY-', 'TH-', 'VN-', 'PH-', 'SG-', 'MM-', 'LA-', 'KH-', 'BN-', 'TL-'))]
    print(f"  SEA codes in tags: {len(sea_codes)}")
    for c in sorted(sea_codes):
        print(f"    {c}")

# Check tools scenario_tags.json
with open('/opt/data/workspace/Protreptic/tools/scenario_tags.json') as fp:
    d = json.load(fp)
print(f"\nscenario_tags.json (tools): {type(d)}")
print(f"  keys: {list(d.keys())}")
for k, v in d.items():
    if isinstance(v, (list, dict)):
        print(f"    {k}: {len(v)}")
    else:
        print(f"    {k}: {type(v)} = {v}")

if 'tags' in d and isinstance(d['tags'], dict):
    print(f"\n  tags dict has {len(d['tags'])} entries")
    sea_codes = [k for k in d['tags'].keys() if k.startswith(('ID-', 'MY-', 'TH-', 'VN-', 'PH-', 'SG-', 'MM-', 'LA-', 'KH-', 'BN-', 'TL-'))]
    print(f"  SEA codes in tags: {len(sea_codes)}")
    for c in sorted(sea_codes):
        print(f"    {c}")