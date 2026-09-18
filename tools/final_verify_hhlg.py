import json

# Final verification of all 4 data files for H-HLG-001
files = {
    'modes_data.json': '/opt/data/workspace/Protreptic/modes_data.json',
    'scenarios_zh.json': '/opt/data/workspace/Protreptic/scenarios_zh.json',
    'scenarios_en.json': '/opt/data/workspace/Protreptic/scenarios_en.json',
    'code_maps.json': '/opt/data/workspace/Protretic/code_maps.json'
}

results = {}

# modes_data.json (list of dicts)
with open('/opt/data/workspace/Protreptic/modes_data.json', 'r') as f:
    modes_list = json.load(f)
found = any(e.get('code') == 'H-HLG-001' for e in modes_list)
results['modes_data'] = found

# scenarios_zh.json (dict keyed by code)
with open('/opt/data/workspace/Protreptic/scenarios_zh.json', 'r') as f:
    zh = json.load(f)
found_zh = 'H-HLG-001' in zh
results['scenarios_zh'] = found_zh

# scenarios_en.json (dict keyed by code)
with open('/opt/data/workspace/Protreptic/scenarios_en.json', 'r') as f:
    en = json.load(f)
found_en = 'H-HLG-001' in en
results['scenarios_en'] = found_en

# code_maps.json (dict with CODE_MAP and CODE_MAP_EN)
with open('/opt/data/workspace/Protreptic/code_maps.json', 'r') as f:
    cm = json.load(f)
found_cm_zh = 'H-HLG-001' in cm.get('CODE_MAP', {})
found_cm_en = 'H-HLG-001' in cm.get('CODE_MAP_EN', {})
results['code_maps_zh'] = found_cm_zh
results['code_maps_en'] = found_cm_en

# Print summary
all_ok = all(results.values())
print(f'H-HLG-001 integration: {"COMPLETE" if all_ok else "INCOMPLETE"}')
for k, v in results.items():
    print(f'  {k}: {"OK" if v else "MISSING"}')

if all_ok:
    print('\nAll 4 data files contain H-HLG-001 entries.')
else:
    print('\nWARNING: Some files missing H-HLG-001!')