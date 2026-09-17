#!/usr/bin/env python3
"""Verify Li Zhi data merge status and report issues."""

import json
from pathlib import Path

BASE = Path("<repo>/tools/json")

print("=" * 60)
print("李贽(H-LZ-001) 数据质量验收报告")
print("=" * 60)

# 1. 检查modes_data.json
print("\n【1】modes_data.json 验证")
with open(BASE / "modes_data.json", 'r', encoding='utf-8') as f:
    modes_data = json.load(f)

print(f"  总条目数: {len(modes_data)}")
lz_modes = [e for e in modes_data if 'LZ-' in e.get('code', '') or 'H-LZ' in e.get('code', '')]
print(f"  李贽相关条目: {len(lz_modes)}")
for e in lz_modes[:3]:
    print(f"    - {e.get('code', 'N/A')}: {e.get('name', '')[:50]}...")

# 检查孔子格式作为参考
kz_modes = [e for e in modes_data if 'H-KZ' in e.get('code', '')]
if kz_modes:
    print(f"\n  参考：孔子(H-KZ-001) 条目结构:")
    print(f"    keys: {list(kz_modes[0].keys())}")

# 2. 检查code_maps.json
print("\n【2】code_maps.json 验证")
with open(BASE / "code_maps.json", 'r', encoding='utf-8') as f:
    code_maps = json.load(f)

# 检查结构
if isinstance(code_maps, dict) and 'CODE_MAP' in code_maps:
    cm_data = code_maps['CODE_MAP']
    print(f"  结构: CODE_MAP 字典")
else:
    cm_data = code_maps
    print(f"  结构: 顶层字典")

h_entries = [k for k in cm_data.keys() if k.startswith('H-')]
print(f"  H-开头条目总数: {len(h_entries)}")

lz_001 = cm_data.get('H-LZ-001', None)
lz_169 = cm_data.get('H-LZ-169', None)
print(f"  H-LZ-001 存在: {'H-LZ-001' in cm_data}")
print(f"  H-LZ-169 存在: {'H-LZ-169' in cm_data}")

if lz_001:
    print(f"    H-LZ-001 数据: {str(lz_001)[:100]}...")
if lz_169:
    print(f"    H-LZ-169 数据: {str(lz_169)[:100]}...")

# 3. 检查scenario_tags.json
print("\n【3】scenario_tags.json 验证")
with open(BASE / "scenario_tags.json", 'r', encoding='utf-8') as f:
    tags = json.load(f)

lz_tags_001 = tags.get('H-LZ-001', None)
lz_tags_169 = tags.get('H-LZ-169', None)
print(f"  H-LZ-001 存在: {'H-LZ-001' in tags}")
print(f"  H-LZ-169 存在: {'H-LZ-169' in tags}")

if lz_tags_001:
    print(f"    tags: {len(lz_tags_001.get('tags', []))}, categories: {len(lz_tags_001.get('categories', []))}")
if lz_tags_169:
    print(f"    tags: {len(lz_tags_169.get('tags', []))}, categories: {len(lz_tags_169.get('categories', []))}")

# 4. 检查scenarios_zh.json
print("\n【4】scenarios_zh.json 验证")
with open(BASE / "scenarios_zh.json", 'r', encoding='utf-8') as f:
    zh = json.load(f)

lz_zh_001 = zh.get('H-LZ-001', None)
lz_zh_169 = zh.get('H-LZ-169', None)
print(f"  H-LZ-001 存在: {'H-LZ-001' in zh}")
print(f"  H-LZ-169 存在: {'H-LZ-169' in zh}")

if lz_zh_001:
    print(f"    name: {lz_zh_001.get('name', 'N/A')[:50]}...")
    print(f"    steps: {len(lz_zh_001.get('steps', []))}")
if lz_zh_169:
    print(f"    name: {lz_zh_169.get('name', 'N/A')[:50]}...")
    print(f"    steps: {len(lz_zh_169.get('steps', []))}")

# 5. 检查scenarios_en.json
print("\n【5】scenarios_en.json 验证")
with open(BASE / "scenarios_en.json", 'r', encoding='utf-8') as f:
    en = json.load(f)

lz_en_001 = en.get('H-LZ-001', None)
lz_en_169 = en.get('H-LZ-169', None)
print(f"  H-LZ-001 存在: {'H-LZ-001' in en}")
print(f"  H-LZ-169 存在: {'H-LZ-169' in en}")

if lz_en_001:
    print(f"    name: {lz_en_001.get('name', 'N/A')[:50]}...")
    print(f"    steps: {len(lz_en_001.get('steps', []))}")
if lz_en_169:
    print(f"    name: {lz_en_169.get('name', 'N/A')[:50]}...")
    print(f"    steps: {len(lz_en_169.get('steps', []))}")

# 6. 源文件检查
print("\n【6】源文件检查")
h_lz_001 = BASE / "H-LZ-001.json"
lz_modes = BASE / "LZ-MODES-001.json"
print(f"  H-LZ-001.json 存在: {h_lz_001.exists()}")
print(f"  LZ-MODES-001.json 存在: {lz_modes.exists()}")

if h_lz_001.exists():
    with open(h_lz_001, 'r', encoding='utf-8') as f:
        src = json.load(f)
    print(f"    mode_count: {src.get('mode_count', 'N/A')}")
    print(f"    schema_version: {src.get('schema_version', 'N/A')}")
    print(f"    codes: {[m['id'] for m in src.get('modes', [])]}")

if lz_modes.exists():
    with open(lz_modes, 'r', encoding='utf-8') as f:
        src = json.load(f)
    print(f"    mode_count: {len(src.get('modes', []))}")
    print(f"    schema_version: {src.get('schema_version', 'N/A')}")

# 7. 问题汇总
print("\n" + "=" * 60)
print("【问题汇总】")
print("=" * 60)

issues = []
if not lz_001:
    issues.append("P0: modes_data.json 缺少 H-LZ-001 条目")
if not lz_tags_001:
    issues.append("P0: scenario_tags.json 缺少 H-LZ-001 条目")
if not lz_zh_001:
    issues.append("P0: scenarios_zh.json 缺少 H-LZ-001 条目")
if not lz_en_001:
    issues.append("P0: scenarios_en.json 缺少 H-LZ-001 条目")
if lz_169:
    issues.append("P1: code_maps.json 使用了错误代码 H-LZ-169 (应为 H-LZ-001)")
if lz_tags_169:
    issues.append("P1: scenario_tags.json 使用了错误代码 H-LZ-169")
if lz_zh_169:
    issues.append("P1: scenarios_zh.json 使用了错误代码 H-LZ-169")
if lz_en_169:
    issues.append("P1: scenarios_en.json 使用了错误代码 H-LZ-169")

if issues:
    for i in issues:
        print(f"  {i}")
else:
    print("  无问题")

print("\n验收结论: 数据合并失败，需重新执行合并")
