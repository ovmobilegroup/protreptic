#!/usr/bin/env python3
import json

# Load the actual database files
with open('modes_data.json', 'r') as f:
    modes_data = json.load(f)
with open('code_maps.json', 'r') as f:
    code_maps = json.load(f)
with open('scenarios_zh.json', 'r') as f:
    scenarios_zh = json.load(f)
with open('scenarios_en.json', 'r') as f:
    scenarios_en = json.load(f)
with open('scenario_tags.json', 'r') as f:
    scenario_tags = json.load(f)

print('=== 实际数据库文件内容验证 ===')
print()

# Check for any H-ZX-001 or 曾子 entries
print('1. modes_data.json 中搜索 H-ZX-001:')
found_modes = [entry for entry in modes_data if entry.get('code') == 'H-ZX-001']
print(f'   找到 {len(found_modes)} 个条目')
for entry in found_modes:
    print(f'   {entry}')

print('\n2. modes_data.json 中搜索 曾子:')
found_zengzi = [entry for entry in modes_data if '曾子' in str(entry).lower()]
print(f'   找到 {len(found_zengzi)} 个条目')
for entry in found_zengzi:
    print(f'   {entry}')

print('\n3. code_maps.json 中搜索 H-ZX-001:')
found_codemap = code_maps.get('H-ZX-001', None)
print(f'   找到 {1 if found_codemap else 0} 个条目')
if found_codemap:
    print(f'   {found_codemap}')

print('\n4. scenarios_zh.json 中搜索 H-ZX-001:')
found_scenarios_zh = [s for s in scenarios_zh if s.get('code') == 'H-ZX-001']
print(f'   找到 {len(found_scenarios_zh)} 个条目')

print('\n5. scenarios_en.json 中搜索 H-ZX-001:')
found_scenarios_en = [s for s in scenarios_en if s.get('code') == 'H-ZX-001']
print(f'   找到 {len(found_scenarios_en)} 个条目')

print('\n6. scenario_tags.json 中搜索 H-ZX-001:')
found_tags = scenario_tags.get('H-ZX-001', None)
print(f'   找到 {1 if found_tags else 0} 个条目')
if found_tags:
    print(f'   {found_tags}')

print('\n=== 结论 ===')
if len(found_modes) == 0 and len(found_codemap) == 0 and len(found_scenarios_zh) == 0 and len(found_scenarios_en) == 0 and len(found_tags) == 0:
    print('❌ 严重问题：曾子(H-ZX-001)数据在5个核心数据库文件中完全缺失！')
    print('   父任务t_dda03623声称已完成数据合并，但实际无数据存在。')
    print('   这属于P0级数据质量问题，需要立即修复。')
else:
    print('✅ 曾子数据存在，需要进一步验证完整性。')