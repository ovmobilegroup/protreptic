import json

with open('<repo>/data/scenarios_en.json', 'r') as f:
    en = json.load(f)
with open('<repo>/data/scenarios_zh.json', 'r') as f:
    zh = json.load(f)

none_count_en = sum(1 for s in en if 'None framework' in s.get('description', ''))
none_count_zh = sum(1 for s in zh if 'None framework' in s.get('description', ''))

print(f'EN scenarios with "None framework": {none_count_en}')
print(f'ZH scenarios with "None framework": {none_count_zh}')
print(f'Total EN scenarios: {len(en)}')
print(f'Total ZH scenarios: {len(zh)}')