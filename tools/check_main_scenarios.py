import json
with open('/opt/data/kanban/boards/protreptic/attachments/t_1cafd4e3/main_data.json') as f:
    data = json.load(f)
scenarios_zh = data.get('scenarios_zh', {})
for k in ['JP-FUKU-001', 'JP-HIDE-001', 'JP-HONDA-001', 'JP-MATSU-001', 'KR-SEJO-001', 'KR-YI-001']:
    if k in scenarios_zh:
        print(f'{k}: FOUND in main_data.scenarios_zh, modes={scenarios_zh[k].get("modes")}')
    else:
        print(f'{k}: NOT FOUND in main_data.scenarios_zh')
print(f'scenarios_zh keys: {len(scenarios_zh)}')