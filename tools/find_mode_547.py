#!/usr/bin/env python3
import json

with open('scenarios_zh.json', 'r', encoding='utf-8') as f:
    zh = json.load(f)

for code, data in zh.items():
    if isinstance(data, dict) and 'modes' in data:
        if 547 in data['modes'] or '547' in [str(m) for m in data['modes']]:
            print(f'Found mode 547 in: {code}')
            print(f'  modes: {data["modes"]}')