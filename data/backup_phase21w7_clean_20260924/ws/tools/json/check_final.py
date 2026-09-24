import json

# Check root modes_data.json for M634-M645
with open('../../modes_data.json') as fp:
    d = json.load(fp)
print(f"modes_data.json (root): {type(d)}")
if isinstance(d, dict):
    for k, v in d.items():
        if isinstance(v, dict):
            print(f"  {k}: {len(v)} entries")
            # Find modes M634-M645
            for mode_key in v:
                if mode_key.startswith('M6') and int(mode_key[1:]) >= 634 and int(mode_key[1:]) <= 645:
                    print(f"    FOUND: {mode_key}: {v[mode_key].get('name', 'N/A')[:80]}")
            # Also show M506-M517
            for mode_key in v:
                if mode_key.startswith('M5') and int(mode_key[1:]) >= 506 and int(mode_key[1:]) <= 517:
                    print(f"    M506-M517: {mode_key}: {v[mode_key].get('name', 'N/A')[:80]}")

# Check root scenario_tags.json properly
with open('../../scenario_tags.json') as fp:
    d = json.load(fp)
print(f"\nscenario_tags.json (root): {type(d)}, keys={len(d)}")
if isinstance(d, dict):
    print(f"  keys (first 20): {list(d.keys())[:20]}")
    # Check for the 12 new codes
    new_codes = ['ES-FER-001', 'ES-CHA-001', 'ES-FRA-001', 'ES-ASU-001', 'ES-PID-001', 
                 'PT-HEN-001', 'PT-VAS-001', 'PT-SAL-001', 'PT-SPI-001',
                 'GR-PER-001', 'GR-JUS-001', 'GR-VEN-001']
    for code in new_codes:
        if code in d:
            print(f"  FOUND: {code}")
        else:
            print(f"  MISSING: {code}")

# Check tools scenario_tags.json (the authoritative one?)
with open('../scenario_tags.json') as fp:
    d = json.load(fp)
print(f"\nscenario_tags.json (tools): {type(d)}, keys={len(d)}")
if isinstance(d, dict):
    print(f"  keys: {list(d.keys())}")
    if 'tags' in d and isinstance(d['tags'], dict):
        print(f"  tags count: {len(d['tags'])}")
        new_codes = ['ES-FER-001', 'ES-CHA-001', 'ES-FRA-001', 'ES-ASU-001', 'ES-PID-001', 
                     'PT-HEN-001', 'PT-VAS-001', 'PT-SAL-001', 'PT-SPI-001',
                     'GR-PER-001', 'GR-JUS-001', 'GR-VEN-001']
        for code in new_codes:
            if code in d['tags']:
                print(f"  FOUND in tags: {code}")
            else:
                print(f"  MISSING in tags: {code}")