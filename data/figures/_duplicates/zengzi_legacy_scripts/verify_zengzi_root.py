#!/usr/bin/env python3
"""验证曾子（H-ZX-001）数据集成状态"""

import json
import os

BASE = "/opt/data/workspace/Protreptic"

def check_file(path, name):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"✅ {name}: 读取成功")
        return data
    except Exception as e:
        print(f"❌ {name}: {e}")
        return None

# 1. 检查 modes_data.json 中的 H-ZX-001
print("\n=== 1. modes_data.json 检查 ===")
modes_data = check_file(f"{BASE}/modes_data.json", "modes_data.json")
if modes_data:
    zx_entry = None
    for entry in modes_data:
        if entry.get('code') == 'H-ZX-001':
            zx_entry = entry
            break
    if zx_entry:
        print(f"✅ H-ZX-001 存在于 modes_data.json")
        modes = zx_entry.get('thinking_modes', [])
        print(f"   思维模式数量: {len(modes)}")
        mode_ids = [m.get('id') for m in modes]
        print(f"   模式ID列表: {mode_ids}")
    else:
        print("❌ H-ZX-001 不存在于 modes_data.json")

# 2. 检查 code_maps.json
print("\n=== 2. code_maps.json 检查 ===")
code_maps = check_file(f"{BASE}/tools/json/code_maps.json", "code_maps.json")
if code_maps:
    if 'H-ZX-001' in code_maps.get('CODE_MAP', {}):
        print(f"✅ H-ZX-001 存在于 code_maps.json")
        print(f"   描述: {code_maps['CODE_MAP']['H-ZX-001'][:80]}...")
    else:
        print("❌ H-ZX-001 不存在于 code_maps.json")

# 3. 检查 scenario_tags.json
print("\n=== 3. scenario_tags.json 检查 ===")
scenario_tags = check_file(f"{BASE}/tools/json/scenario_tags.json", "scenario_tags.json")
if scenario_tags:
    if 'H-ZX-001' in scenario_tags:
        print(f"✅ H-ZX-001 存在于 scenario_tags.json")
        tags = scenario_tags['H-ZX-001'].get('tags', [])
        print(f"   标签数量: {len(tags)}")
        print(f"   类别数量: {len(scenario_tags['H-ZX-001'].get('categories', []))}")
    else:
        print("❌ H-ZX-001 不存在于 scenario_tags.json")

# 4. 检查 H-ZX-001.json
print("\n=== 4. H-ZX-001.json 检查 ===")
hx_json = check_file(f"{BASE}/H-ZX-001.json", "H-ZX-001.json")
if hx_json:
    print(f"✅ H-ZX-001.json 存在")
    print(f"   Schema版本: {hx_json.get('schema_version')}")
    print(f"   姓名: {hx_json.get('figure_name_zh')}")

# 5. 检查 H-ZX-001_modes.json
print("\n=== 5. H-ZX-001_modes.json 检查 ===")
hx_modes = check_file(f"{BASE}/H-ZX-001_modes.json", "H-ZX-001_modes.json")
if hx_modes:
    print(f"✅ H-ZX-001_modes.json 存在")
    core_modes = hx_modes.get('core_modes', [])
    print(f"   核心模式数量: {len(core_modes)}")

# 6. 检查研究报告
print("\n=== 6. 研究报告检查 ===")
research_path = f"{BASE}/docs/research/phase20_zengzi_research.md"
if os.path.exists(research_path):
    with open(research_path, 'r', encoding='utf-8') as f:
        content = f.read()
    print(f"✅ phase20_zengzi_research.md 存在")
    print(f"   文件大小: {len(content)} 字符")
else:
    print("❌ phase20_zengzi_research.md 不存在")

print("\n=== 验证完成 ===")
