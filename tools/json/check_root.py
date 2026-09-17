import json

# Check the root modes_data.json - count M506-M517
with open('../modes_data.json') as fp:
    d = json.load(fp)
print(f"modes_data.json (root): {type(d)}")
if isinstance(d, dict):
    print(f"  keys: {list(d.keys())}")
    for k, v in d.items():
        if isinstance(v, dict):
            print(f"    {k}: {len(v)} entries")
            # Find modes M506-M517
            for mode_key in v:
                if mode_key.startswith('M5') and int(mode_key[1:]) >= 506 and int(mode_key[1:]) <= 517:
                    print(f"      {mode_key}: {v[mode_key].get('name', 'N/A')[:50]}")

# Check the root scenarios_zh.json for the 12 new entries (ES-*, PT-*, GR-*)
with open('../scenarios_zh.json') as fp:
    d = json.load(fp)
print(f"\nscenarios_zh.json (root): {len(d)} entries")
new_codes = ['ES-FER-001', 'ES-CHA-001', 'ES-FRA-001', 'ES-ASU-001', 'ES-PID-001', 
             'PT-HEN-001', 'PT-VAS-001', 'PT-SAL-001', 'PT-SPI-001',
             'GR-PER-001', 'GR-JUS-001', 'GR-VEN-001']
for code in new_codes:
    if code in d:
        print(f"  FOUND: {code}")
    else:
        print(f"  MISSING: {code}")

# Check root scenarios_en.json
with open('../scenarios_en.json') as fp:
    d = json.load(fp)
print(f"\nscenarios_en.json (root): {type(d)}, {len(d)} entries")
if isinstance(d, dict):
    for code in new_codes:
        if code in d:
            print(f"  FOUND: {code}")
        else:
            print(f"  MISSING: {code}")
elif isinstance(d, list):
    for code in new_codes:
        found = any(item.get('code') == code for item in d)
        if found:
            print(f"  FOUND: {code}")
        else:
            print(f"  MISSING: {code}")

# Check root code_maps.json
with open('../code_maps.json') as fp:
    d = json.load(fp)
print(f"\ncode_maps.json (root): CODE_MAP={len(d.get('CODE_MAP', {}))}, CODE_MAP_EN={len(d.get('CODE_MAP_EN', {}))}")
for code in new_codes:
    in_map = code in d.get('CODE_MAP', {})
    in_map_en = code in d.get('CODE_MAP_EN', {})
    print(f"  {code}: CODE_MAP={'Y' if in_map else 'N'}, CODE_MAP_EN={'Y' if in_map_en else 'N'}")

# Check root scenario_tags.json
with open('../scenario_tags.json') as fp:
    d = json.load(fp)
print(f"\nscenario_tags.json (root): {len(d)} keys")
for code in new_codes:
    if code in d:
        print(f"  FOUND: {code} = {d[code]}")
    else:
        print(f"  MISSING: {code}")