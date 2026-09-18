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
with open('modes_data.json', 'r', encoding='utf-8') as f:
    md = json.load(f)

me_codes = ['AE-ZAY-001', 'SA-OIL-001', 'JO-HAS-001', 'BH-ISL-001', 'QA-ENE-001', 'OM-QAB-001', 'LB-CON-001', 'SY-ALA-001', 'IQ-CAL-001', 'IR-KHA-001', 'YE-HOU-001']

print('=== Middle East codes in scenarios_zh ===')
for code in me_codes:
    if code in zh:
        print(f'  {code}: FOUND (modes: {zh[code].get("modes", [])})')
    else:
        print(f'  {code}: MISSING')

print()
print('=== Middle East codes in scenarios_en ===')
for code in me_codes:
    if code in en:
        print(f'  {code}: FOUND')
    else:
        print(f'  {code}: MISSING')

print()
print('=== Middle East codes in code_maps ===')
for code in me_codes:
    if code in cm.get('CODE_MAP', {}):
        print(f'  {code}: FOUND ({cm["CODE_MAP"][code]})')
    else:
        print(f'  {code}: MISSING')

print()
print('=== Middle East codes in scenario_tags ===')
for code in me_codes:
    if code in st.get('tags', {}):
        print(f'  {code}: FOUND')
    else:
        print(f'  {code}: MISSING')