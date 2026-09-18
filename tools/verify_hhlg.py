import json
import sys

# Verify scenarios_zh.json is valid JSON and contains H-HLG-001
try:
    with open('/opt/data/workspace/Protreptic/scenarios_zh.json', 'r') as f:
        zh = json.load(f)
    print('scenarios_zh.json: OK')
    print('H-HLG-001 in scenarios_zh:', 'H-HLG-001' in zh)
    if 'H-HLG-001' in zh:
        entry = zh['H-HLG-001']
        print(f'  name: {entry.get("name")}')
        print(f'  core_mode: {entry.get("core_mode")}')
        print(f'  category: {entry.get("category")}')
        print(f'  region: {entry.get("region")}')
except Exception as e:
    print(f'scenarios_zh.json ERROR: {e}')

# Verify scenarios_en.json
try:
    with open('/opt/data/workspace/Protreptic/scenarios_en.json', 'r') as f:
        en = json.load(f)
    print('scenarios_en.json: OK')
    print('H-HLG-001 in scenarios_en:', 'H-HLG-001' in en)
    if 'H-HLG-001' in en:
        entry = en['H-HLG-001']
        print(f'  name: {entry.get("name")}')
        print(f'  core_mode: {entry.get("core_mode")}')
except Exception as e:
    print(f'scenarios_en.json ERROR: {e}')

# Verify code_maps.json
try:
    with open('/opt/data/workspace/Protreptic/code_maps.json', 'r') as f:
        cm = json.load(f)
    print('code_maps.json: OK')
    print('H-HLG-001 in CODE_MAP:', 'H-HLG-001' in cm.get('CODE_MAP', {}))
    print('H-HLG-001 in CODE_MAP_EN:', 'H-HLG-001' in cm.get('CODE_MAP_EN', {}))
except Exception as e:
    print(f'code_maps.json ERROR: {e}')

# Verify modes_data.json has H-HLG-001
try:
    with open('/opt/data/workspace/Protreptic/modes_data.json', 'r') as f:
        md = json.load(f)
    print('modes_data.json: OK')
    print('H-HLG-001 in modes_data:', 'H-HLG-001' in md)
    if 'H-HLG-001' in md:
        entry = md['H-HLG-001']
        print(f'  name: {entry.get("name")}')
        print(f'  core_mode: {entry.get("core_mode")}')
except Exception as e:
    print(f'modes_data.json ERROR: {e}')