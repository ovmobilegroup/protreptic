#!/usr/bin/env python3
"""
Update Xue Muqiao (薛暮桥) data in all 4 JSON files based on Serrano research output.
The H-XMQ-001.json provides the structured data with 5 thinking modes (26,19,38,39,41)
and a 5-step process. We update H-XMQ-299 (the test-expected entry) with this data,
while keeping H-XMQ-151 (existing upgraded version) intact.
"""

import json
import sys
import os

PROJE_ROOT = '/opt/data/workspace/Protreptic'
TOOLS_DIR = os.path.join(PROJE_ROOT, 'tools')

# Load Serrano source data
with open(os.path.join(PROJE_ROOT, 'H-XMQ-001.json'), 'r', encoding='utf-8') as f:
    xue = json.load(f)

# Build the updated entry for H-XMQ-299 (replacing stub with full data)
# Map Serrano fields to the existing file format:
#   code -> H-XMQ-299 (test expectation)
#   name_zh/name_en -> name
#   description_zh/description_en -> description  
#   modes -> modes (already list of ints [26,19,38,39,41])
#   reason_zh/reason_en -> reason (use zh)
#   steps_zh/steps_en -> steps (use zh)
#   expected_zh/expected_en -> expected (use zh, join list with \n)
#   case_zh/case_en -> case (use zh)

xue_name_zh = xue.get('name_zh', '薛暮桥')
xue_code = xue.get('code', 'H-XMQ-151')

# Build zh entry (matching existing file format)
zh_entry = {
    'name': f'薛暮桥：价格改革理论奠基与改革风险决策框架',
    'description': xue.get('description_zh', ''),
    'modes': xue.get('modes', [26, 19, 38, 39, 41]),
    'reason': xue.get('reason_zh', ''),
    'steps': xue.get('steps_zh', []),
    'expected': '\n'.join(xue.get('expected_zh', [])),
    'case': xue.get('case_zh', '')
}

# Build en entry (matching existing file format)
en_entry = {
    'name': f'Xue Muqiao: Price Reform Theory Foundation and Reform Risk Decision Framework',
    'description': xue.get('description_en', ''),
    'modes': xue.get('modes', [26, 19, 38, 39, 41]),
    'reason': xue.get('reason_en', ''),
    'steps': [s.replace('第X步：', 'Step X: ') for s in xue.get('steps_en', [])],
    'expected': '\n'.join(xue.get('expected_en', [])),
    'case': xue.get('case_en', '').rstrip(';')  # strip trailing semicolons
}

def load_json(filename):
    path = os.path.join(TOOLS_DIR, filename)
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f), path

def save_json(data, path):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# 1. Update scenarios_zh.json - fix H-XMQ-299 (replace stub with full data)
print("=== Updating scenarios_zh.json ===")
sz, sz_path = load_json('scenarios_zh.json')

if 'H-XMQ-299' in sz:
    old = sz['H-XMQ-299']
    print(f"  Old H-XMQ-299: name={old.get('name','')}, modes={old.get('modes',[])}")
    sz['H-XMQ-299'] = zh_entry
    print(f"  New H-XMQ-299: name={zh_entry['name']}, modes={zh_entry['modes']}")

save_json(sz, sz_path)
print("  Done.")

# 2. Update scenarios_en.json - fix H-XMQ-299 (replace stub with full data)
print("=== Updating scenarios_en.json ===")
se, se_path = load_json('scenarios_en.json')

if 'H-XMQ-299' in se:
    old = se['H-XMQ-299']
    print(f"  Old H-XMQ-299: name={old.get('name','')}, modes={old.get('modes',[])}")
    se['H-XMQ-299'] = en_entry
    print(f"  New H-XMQ-299: name={en_entry['name']}, modes={en_entry['modes']}")

save_json(se, se_path)
print("  Done.")

# 3. Update code_maps.json - update H-XMQ-299 description
print("=== Updating code_maps.json ===")
cm, cm_path = load_json('code_maps.json')

if 'H-XMQ-299' in cm:
    old_desc = cm['H-XMQ-299']
    print(f"  Old H-XMQ-299 desc: {old_desc[:80]}...")
    cm['H-XMQ-299'] = '薛暮桥：价格改革理论奠基与改革风险决策框架'
    print(f"  New H-XMQ-299 desc: {cm['H-XMQ-299']}")

save_json(cm, cm_path)
print("  Done.")

# 4. Update code_maps_en.json - update H-XMQ-299 description
print("=== Updating code_maps_en.json ===")
cme, cme_path = load_json('code_maps_en.json')

if 'H-XMQ-299' in cme:
    old_desc = cme['H-XMQ-299']
    print(f"  Old H-XMQ-299 desc: {old_desc[:80]}...")
    cme['H-XMQ-299'] = 'Xue Muqiao: Price Reform Theory Foundation and Reform Risk Decision Framework'
    print(f"  New H-XMQ-299 desc: {cme['H-XMQ-299']}")

save_json(cme, cme_path)
print("  Done.")

# Summary
print("\n=== Update Summary ===")
print(f"  H-XMQ-299 updated in scenarios_zh.json: modes={zh_entry['modes']}")
print(f"  H-XMQ-299 updated in scenarios_en.json: modes={en_entry['modes']}")
print(f"  H-XMQ-299 updated in code_maps.json: OK")
print(f"  H-XMQ-299 updated in code_maps_en.json: OK")
print(f"  H-XMQ-151 (existing) kept intact with modes {sz.get('H-XMQ-151', {}).get('modes')}")