import json

with open('/opt/data/workspace/Protreptic/tools/scenarios_en.json', 'r') as f:
    data = json.load(f)

print('Total entries:', len(data))
print('Keys:', list(data.keys())[:5])
print('Type of first value:', type(list(data.values())[0]))

first_key = list(data.keys())[0]
first_val = data[first_key]
print('First key:', first_key)
print('First value keys:', list(first_val.keys()) if isinstance(first_val, dict) else 'not dict')
print('First value modes:', first_val.get('modes') if isinstance(first_val, dict) else 'N/A')

# Check for problematic entries
for k, v in data.items():
    if isinstance(v, dict):
        modes = v.get('modes')
        if modes:
            for m in modes:
                if not isinstance(m, int):
                    print(f'ERROR in {k}: mode {m} not integer')
    else:
        print(f'ERROR in {k}: not a dict, type={type(v)}')