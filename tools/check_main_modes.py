import json
with open('/opt/data/kanban/boards/protreptic/attachments/t_1cafd4e3/main_data.json') as f:
    data = json.load(f)
print(json.dumps(data.get('modes', {}), indent=2, ensure_ascii=False)[:5000])