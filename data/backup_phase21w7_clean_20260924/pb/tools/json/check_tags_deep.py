import json

# Check scenario_tags in tools
with open('../scenario_tags.json') as fp:
    d = json.load(fp)
print(f"scenario_tags.json (tools): {type(d)}, keys={len(d)}")
if isinstance(d, dict):
    print(f"  keys: {list(d.keys())}")
    for k, v in d.items():
        if isinstance(v, (list, dict)):
            print(f"    {k}: {len(v)}")
            if k == 'tags' and isinstance(v, dict):
                new_codes = ['ES-FER-001', 'ES-CHA-001', 'ES-FRA-001', 'ES-ASU-001', 'ES-PID-001', 
                             'PT-HEN-001', 'PT-VAS-001', 'PT-SAL-001', 'PT-SPI-001',
                             'GR-PER-001', 'GR-JUS-001', 'GR-VEN-001']
                for code in new_codes:
                    if code in v:
                        print(f"      FOUND: {code} = {v[code]}")
                    else:
                        print(f"      MISSING: {code}")

# Check scenario_tags in root - maybe it's a different structure
with open('../../scenario_tags.json') as fp:
    d = json.load(fp)
print(f"\nscenario_tags.json (root): {type(d)}, keys={len(d)}")
if isinstance(d, dict):
    new_codes = ['ES-FER-001', 'ES-CHA-001', 'ES-FRA-001', 'ES-ASU-001', 'ES-PID-001', 
                 'PT-HEN-001', 'PT-VAS-001', 'PT-SAL-001', 'PT-SPI-001',
                 'GR-PER-001', 'GR-JUS-001', 'GR-VEN-001']
    for code in new_codes:
        if code in d:
            print(f"  FOUND: {code} = {d[code]}")
        else:
            print(f"  MISSING: {code}")