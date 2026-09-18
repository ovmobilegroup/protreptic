#!/usr/bin/env python3
import json

with open('scenarios_zh.json', 'r', encoding='utf-8') as f:
    zh = json.load(f)
with open('scenarios_en.json', 'r', encoding='utf-8') as f:
    en = json.load(f)

zh_codes = set(zh.keys())
en_codes = set(en.keys())

print('Tools dir - ZH count:', len(zh_codes), 'EN count:', len(en_codes))
print('In ZH but not EN:', zh_codes - en_codes)
print('In EN but not ZH:', en_codes - zh_codes)