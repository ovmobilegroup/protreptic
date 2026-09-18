#!/usr/bin/env python3
import json

with open('scenarios_zh.json', 'r', encoding='utf-8') as f:
    zh = json.load(f)
with open('scenarios_en.json', 'r', encoding='utf-8') as f:
    en = json.load(f)
with open('code_maps.json', 'r', encoding='utf-8') as f:
    cm = json.load(f)
with open('scenario_tags.json', 'r', encoding='utf-8') as f:
    st = json.load(f)

il_codes = ['IL-DIAS-001', 'IL-LIT-001', 'IL-MIL-001', 'IL-HAVR-001', 'IL-SCI-001', 'IL-TECH-001', 'IL-ZION-001', 'IL-PSY-001']

print('=== Israel codes in scenarios_zh ===')
for code in il_codes:
    if code in zh:
        print(f'  {code}: FOUND (modes: {zh[code].get("modes", [])})')
    else:
        print(f'  {code}: MISSING')

print()
print('=== Israel codes in scenarios_en ===')
for code in il_codes:
    if code in en:
        print(f'  {code}: FOUND')
    else:
        print(f'  {code}: MISSING')

print()
print('=== Israel codes in code_maps ===')
for code in il_codes:
    if code in cm.get('CODE_MAP', {}):
        print(f'  {code}: FOUND ({cm["CODE_MAP"][code]})')
    else:
        print(f'  {code}: MISSING')

print()
print('=== Israel codes in scenario_tags ===')
for code in il_codes:
    if code in st.get('tags', {}):
        print(f'  {code}: FOUND')
    else:
        print(f'  {code}: MISSING')