import json

with open('scenarios_zh.json') as f:
    zh = json.load(f)
with open('scenarios_en.json') as f:
    en = json.load(f)
with open('code_maps.json') as f:
    cm = json.load(f)
with open('scenario_tags.json') as f:
    st = json.load(f)

h_codes_zh = [k for k in zh.keys() if k.startswith('H-')]
h_codes_en = [k for k in en.keys() if k.startswith('H-')]
h_codes_cm = [k for k in cm.keys() if k.startswith('H-')]

print(f'SCENARIOS_ZH total keys: {len(zh)}')
print(f'SCENARIOS_ZH dict entries: {sum(1 for v in zh.values() if isinstance(v, dict))}')
print(f'H-codes in ZH: {len(h_codes_zh)}')
print(f'SCENARIOS_EN total keys: {len(en)}')
print(f'SCENARIOS_EN dict entries: {sum(1 for v in en.values() if isinstance(v, dict))}')
print(f'H-codes in EN: {len(h_codes_en)}')
print(f'code_maps total: {len(cm)}')
print(f'H-codes in code_maps: {len(h_codes_cm)}')
print(f'scenario_tags total: {len(st)}')
print(f'H-codes in tags: {len([k for k in st.keys() if k.startswith("H-")])}')