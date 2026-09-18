#!/usr/bin/env python3
import json

with open('scenarios_zh.json', 'r', encoding='utf-8') as f:
    zh = json.load(f)
with open('scenarios_en.json', 'r', encoding='utf-8') as f:
    en = json.load(f)

all_modes = set()
for code, figure in zh.items():
    if isinstance(figure, dict) and 'modes' in figure:
        for m in figure['modes']:
            all_modes.add(str(m))

for code, figure in en.items():
    if isinstance(figure, dict) and 'modes' in figure:
        for m in figure['modes']:
            all_modes.add(str(m))

print('All modes used in scenarios:', sorted(all_modes))

with open('modes_data.json', 'r', encoding='utf-8') as f:
    md = json.load(f)

zh_modes = set(md['zh'].keys())
en_modes = set(md['en'].keys())

print('Modes in modes_data zh:', len(zh_modes))
print('Modes in modes_data en:', len(en_modes))
print('Missing modes:', sorted(all_modes - zh_modes))