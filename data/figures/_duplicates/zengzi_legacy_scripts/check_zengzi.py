import json

# Check modes_data.json for H-ZX-001
with open('/opt/data/workspace/Protreptic/data/modes_data.json', 'r') as f:
    modes_data = json.load(f)
    
hzx_modes = [entry for entry in modes_data if entry.get('code') == 'H-ZX-001']
print(f"modes_data.json H-ZX-001 entries: {len(hzx_modes)}")
for entry in hzx_modes:
    print(f"  {entry.get('code')}: {entry.get('figure_name_zh')}, modes={entry.get('thinking_mode_count', 'N/A')}")

# Check code_maps.json
with open('/opt/data/workspace/Protreptic/data/code_maps.json', 'r') as f:
    code_maps = json.load(f)
print(f"code_maps.json has H-ZX-001: {'H-ZX-001' in code_maps}")
if 'H-ZX-001' in code_maps:
    print(f"  {code_maps['H-ZX-001']}")

# Check scenarios_zh.json
with open('/opt/data/workspace/Protreptic/data/scenarios_zh.json', 'r') as f:
    scenarios_zh = json.load(f)
hzx_scenarios_zh = [s for s in scenarios_zh if s.get('code') == 'H-ZX-001']
print(f"scenarios_zh.json H-ZX-001 entries: {len(hzx_scenarios_zh)}")

# Check scenarios_en.json
with open('/opt/data/workspace/Protreptic/data/scenarios_en.json', 'r') as f:
    scenarios_en = json.load(f)
hzx_scenarios_en = [s for s in scenarios_en if s.get('code') == 'H-ZX-001']
print(f"scenarios_en.json H-ZX-001 entries: {len(hzx_scenarios_en)}")

# Check scenario_tags.json
with open('/opt/data/workspace/Protreptic/data/scenario_tags.json', 'r') as f:
    scenario_tags = json.load(f)
print(f"scenario_tags.json has H-ZX-001: {'H-ZX-001' in scenario_tags}")
if 'H-ZX-001' in scenario_tags:
    print(f"  {scenario_tags['H-ZX-001']}")

# Also check for H-ZZ-001 (Zhang Zai) which should exist
print("\n--- Checking existing H-ZZ-001 ---")
hzz_modes = [entry for entry in modes_data if entry.get('code') == 'H-ZZ-001']
print(f"modes_data.json H-ZZ-001 entries: {len(hzz_modes)}")
print(f"code_maps.json has H-ZZ-001: {'H-ZZ-001' in code_maps}")
hzz_scenarios_zh = [s for s in scenarios_zh if s.get('code') == 'H-ZZ-001']
hzz_scenarios_en = [s for s in scenarios_en if s.get('code') == 'H-ZZ-001']
print(f"scenarios_zh.json H-ZZ-001 entries: {len(hzz_scenarios_zh)}")
print(f"scenarios_en.json H-ZZ-001 entries: {len(hzz_scenarios_en)}")
print(f"scenario_tags.json has H-ZZ-001: {'H-ZZ-001' in scenario_tags}")