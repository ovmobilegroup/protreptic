import json
with open('/opt/data/kanban/boards/protreptic/attachments/t_1cafd4e3/main_data.json') as f:
    data = json.load(f)
for k in data.keys():
    print(k)