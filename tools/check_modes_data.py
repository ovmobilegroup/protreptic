import json
with open('../modes_data.json') as f:
    md = json.load(f)
print('Root modes_data.json:', type(md), len(md) if isinstance(md, (list, dict)) else 'N/A')
if isinstance(md, list):
    print('First item keys:', md[0].keys() if md else 'empty')
elif isinstance(md, dict):
    print('Keys:', md.keys())