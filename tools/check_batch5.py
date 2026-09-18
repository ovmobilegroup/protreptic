import json
with open('scenarios_zh.json') as f:
    zh = json.load(f)
for k in ['JP-FUKU-001', 'JP-HIDE-001', 'JP-HONDA-001', 'JP-MATSU-001', 'KR-SEJO-001', 'KR-YI-001']:
    v = zh.get(k)
    if v:
        print(f'{k}: modes={v.get("modes")}')
    else:
        print(f'{k}: NOT FOUND')