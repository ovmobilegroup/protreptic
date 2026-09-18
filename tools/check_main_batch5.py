import json
with open('/opt/data/kanban/boards/protreptic/attachments/t_1cafd4e3/main_data.json') as f:
    data = json.load(f)
for k in ['JP-FUKU-001', 'JP-HIDE-001', 'JP-HONDA-001', 'JP-MATSU-001', 'KR-SEJO-001', 'KR-YI-001']:
    if k in data:
        print(f'{k}: FOUND in main_data, modes={data[k].get("modes")}')
    else:
        print(f'{k}: NOT FOUND in main_data')
print(f'Main data keys: {len(data)}')