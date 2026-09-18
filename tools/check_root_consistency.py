#!/usr/bin/env python3
import json

with open('scenarios_zh.json', 'r', encoding='utf-8') as f:
    zh = json.load(f)
with open('scenarios_en.json', 'r', encoding='utf-8') as f:
    en = json.load(f)

print('Root dir - ZH count:', len(zh), 'EN count:', len(en))

new_entries = ['PK-ISL-001', 'PK-SUF-001', 'BD-LIB-001', 'LK-CIV-001', 'NP-HIM-001', 'AF-TRI-001', 'MV-ISL-001', 'BT-GNH-001']
for code in new_entries:
    print(f'{code}: zh={code in zh}, en={code in en}')