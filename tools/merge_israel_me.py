#!/usr/bin/env python3
"""
Merge the 3 missing Israel entries and ensure all 11 Middle East entries
are fully integrated into code_maps and scenario_tags.
"""

import json
import sys
from pathlib import Path

TOOLS_DIR = Path("/opt/data/workspace/Protreptic/tools")
IL_DIR = Path("/opt/data/workspace/Protreptic/IL")

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# Load authoritative files
scenarios_zh = load_json(TOOLS_DIR / "scenarios_zh.json")
scenarios_en = load_json(TOOLS_DIR / "scenarios_en.json")
code_maps = load_json(TOOLS_DIR / "code_maps.json")
scenario_tags = load_json(TOOLS_DIR / "scenario_tags.json")
modes_data = load_json(TOOLS_DIR / "modes_data.json")

# The 3 missing Israel entries to merge
il_missing = ['IL-DIAS-001', 'IL-LIT-001', 'IL-MIL-001']

# The 11 Middle East entries that need code_maps and scenario_tags
me_codes = ['AE-ZAY-001', 'SA-OIL-001', 'JO-HAS-001', 'BH-ISL-001', 'QA-ENE-001', 
            'OM-QAB-001', 'LB-CON-001', 'SY-ALA-001', 'IQ-CAL-001', 'IR-KHA-001', 'YE-HOU-001']

# All Israel entries (for code_maps and scenario_tags)
il_all = ['IL-DIAS-001', 'IL-LIT-001', 'IL-MIL-001', 'IL-HAVR-001', 'IL-SCI-001', 'IL-TECH-001', 'IL-ZION-001', 'IL-PSY-001']

print("=== Merging missing Israel entries ===")
for code in il_missing:
    json_path = IL_DIR / f"{code}.json"
    if not json_path.exists():
        print(f"  SKIP {code}: file not found")
        continue
    
    data = load_json(json_path)
    if data.get('code') != code:
        print(f"  SKIP {code}: code mismatch")
        continue
    
    # Merge to scenarios_zh
    scenarios_zh[code] = data
    
    # Create EN entry
    en_entry = {}
    for key, value in data.items():
        if key == 'code':
            en_entry[key] = value
        elif key.endswith('_zh'):
            en_key = key.replace('_zh', '_en')
            en_entry[en_key] = data.get(en_key, value)
        elif key.endswith('_en'):
            en_entry[key] = value
        elif key in ['name', 'description', 'reason', 'steps', 'expected', 'case']:
            en_key = key + '_en'
            zh_key = key + '_zh'
            if en_key in data:
                en_entry[key] = data[en_key]
            elif zh_key in data:
                en_entry[key] = data[zh_key]
            else:
                en_entry[key] = value
        else:
            en_entry[key] = value
    scenarios_en[code] = en_entry
    
    print(f"  MERGED {code} into scenarios_zh/en")

print("\n=== Updating code_maps for all 8 Israel entries ===")
for code in il_all:
    if code in scenarios_zh:
        data = scenarios_zh[code]
        code_maps['CODE_MAP'][code] = data.get('name_zh', data.get('name', code))
        code_maps['CODE_MAP_EN'][code] = data.get('name_en', data.get('name', code))
        print(f"  Added {code} to code_maps")

print("\n=== Updating code_maps for 11 Middle East entries ===")
for code in me_codes:
    if code in scenarios_zh:
        data = scenarios_zh[code]
        code_maps['CODE_MAP'][code] = data.get('name_zh', data.get('name', code))
        code_maps['CODE_MAP_EN'][code] = data.get('name_en', data.get('name', code))
        print(f"  Added {code} to code_maps")

print("\n=== Updating scenario_tags for all 8 Israel entries ===")
for code in il_all:
    if code in scenarios_zh:
        data = scenarios_zh[code]
        modes = data.get('modes', [])
        if not modes and 'core_mode' in data:
            import re
            modes = [int(m) for m in re.findall(r'M(\d+)', data['core_mode'])]
        
        scenario_tags['tags'][code] = {
            'code': code,
            'name_zh': data.get('name_zh', data.get('name', code)),
            'name_en': data.get('name_en', ''),
            'era': data.get('time_period_standardized', ''),
            'gender': data.get('gender', 'male'),
            'ethnicity': data.get('nationality', ''),
            'domains': data.get('domains', []),
            'core_modes': [str(m) for m in modes],
            'applications': [],
            'historical_domains': data.get('historical_domains', []),
            'mode_count': len(modes)
        }
        print(f"  Added {code} to scenario_tags")

print("\n=== Updating scenario_tags for 11 Middle East entries ===")
for code in me_codes:
    if code in scenarios_zh:
        data = scenarios_zh[code]
        modes = data.get('modes', [])
        if not modes and 'core_mode' in data:
            import re
            modes = [int(m) for m in re.findall(r'M(\d+)', data['core_mode'])]
        
        scenario_tags['tags'][code] = {
            'code': code,
            'name_zh': data.get('name_zh', data.get('name', code)),
            'name_en': data.get('name_en', ''),
            'era': data.get('time_period_standardized', ''),
            'gender': data.get('gender', 'male'),
            'ethnicity': data.get('nationality', ''),
            'domains': data.get('domains', []),
            'core_modes': [str(m) for m in modes],
            'applications': [],
            'historical_domains': data.get('historical_domains', []),
            'mode_count': len(modes)
        }
        print(f"  Added {code} to scenario_tags")

# Save all files
save_json(TOOLS_DIR / "scenarios_zh.json", scenarios_zh)
save_json(TOOLS_DIR / "scenarios_en.json", scenarios_en)
save_json(TOOLS_DIR / "code_maps.json", code_maps)
save_json(TOOLS_DIR / "scenario_tags.json", scenario_tags)

print(f"\n=== Merge Complete ===")
print(f"Total scenarios_zh: {len(scenarios_zh)}")
print(f"Total scenarios_en: {len(scenarios_en)}")
print(f"Total CODE_MAP: {len(code_maps.get('CODE_MAP', {}))}")
print(f"Total CODE_MAP_EN: {len(code_maps.get('CODE_MAP_EN', {}))}")
print(f"Total scenario_tags: {len(scenario_tags.get('tags', {}))}")