#!/usr/bin/env python3
import json

with open('modes_data.json', 'r', encoding='utf-8') as f:
    md = json.load(f)

print('547 in zh:', '547' in md['zh'])
print('547 in en:', '547' in md['en'])