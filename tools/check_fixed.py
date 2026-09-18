import json
with open('../scenarios_zh.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
for code in ['H-ZDY-212', 'H-CC-213', 'A-1-X-P']:
    entry = data.get(code)
    if entry:
        expected = entry.get('expected')
        print(f'{code}: expected type {type(expected)}, value: {expected}')
    else:
        print(f'{code}: not found')
