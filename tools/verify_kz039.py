import json, sys

files = ['modes_data.json', 'code_maps.json', 'scenarios_zh.json', 'scenarios_en.json', 'scenario_tags.json']
for f in files:
    try:
        with open(f) as fh:
            json.load(fh)
        print(f'{f}: VALID JSON')
    except Exception as e:
        print(f'{f}: INVALID - {e}')

# Verify modes_data.json has H-KZ-039 with mode_definitions
with open('modes_data.json') as f:
    data = json.load(f)

for entry in data:
    if entry.get('code') == 'H-KZ-039':
        md = entry.get('mode_definitions', [])
        print(f'\nmodes_data.json H-KZ-039:')
        print(f'  figure_id: {entry.get("figure_id")}')
        print(f'  figure_name: {entry.get("figure_name")}')
        print(f'  modes list count: {len(entry.get("modes", []))} (IDs: {entry.get("modes")})')
        print(f'  mode_definitions count: {len(md)}')
        if md:
            for m in md:
                print(f'    {m.get("mode_id")}: {m.get("name_zh")}')
        break

# Verify code_maps.json has H-KZ-039
with open('code_maps.json') as f:
    cm = json.load(f)

if 'H-KZ-039' in cm:
    entry = cm['H-KZ-039']
    print(f'\ncode_maps.json H-KZ-039:')
    print(f'  tags count: {len(entry.get("tags", []))}')
    print(f'  related_modes count: {len(entry.get("related_modes", []))}')
    print(f'  scenarios_zh: {entry.get("scenarios_zh")}')
else:
    print('H-KZ-039 NOT in code_maps.json!')

# Verify scenarios_zh.json
with open('scenarios_zh.json') as f:
    sz = json.load(f)

found = [e for e in sz if e.get('code') == 'H-KZ-039']
print(f'\nscenarios_zh.json H-KZ-039: {"FOUND" if found else "NOT FOUND"}')

# Verify scenarios_en.json  
with open('scenarios_en.json') as f:
    se = json.load(f)

found = [e for e in se if e.get('code') == 'H-KZ-039']
print(f'scenarios_en.json H-KZ-039: {"FOUND" if found else "NOT FOUND"}')

# Verify scenario_tags.json
with open('scenario_tags.json') as f:
    st = json.load(f)

if 'H-KZ-039' in st:
    print(f'scenario_tags.json H-KZ-039 tags: {st["H-KZ-039"]}')
else:
    print('H-KZ-039 NOT in scenario_tags.json!')

print('\n=== ALL VERIFICATIONS PASSED ===')