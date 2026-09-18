#!/usr/bin/env python3
"""
Merge the 10 missing CEE entries from tools/json/ into authoritative data files
"""

import json
from pathlib import Path

TOOLS_DIR = Path("/opt/data/workspace/Protreptic/tools")
JSON_DIR = TOOLS_DIR / "json"

# The 10 missing CEE entries
MISSING_CODES = [
    "CZ-TECH-001",
    "EE-MER-001",
    "RU-AERO-001",
    "RU-CHEM-001",
    "RU-GEOP-001",
    "RU-INDU-001",
    "RU-LITE-001",
    "RU-NUCL-001",
    "RU-REFR-001",
    "RU-REVO-001"
]

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def main():
    # Load authoritative data files
    scenarios_zh = load_json(TOOLS_DIR / "scenarios_zh.json")
    scenarios_en = load_json(TOOLS_DIR / "scenarios_en.json")
    code_maps = load_json(TOOLS_DIR / "code_maps.json")
    scenario_tags = load_json(TOOLS_DIR / "scenario_tags.json")
    modes_data = load_json(TOOLS_DIR / "modes_data.json")

    print(f"Before merge:")
    print(f"  scenarios_zh: {len(scenarios_zh)}")
    print(f"  scenarios_en: {len(scenarios_en)}")
    print(f"  CODE_MAP: {len(code_maps.get('CODE_MAP', {}))}")
    print(f"  CODE_MAP_EN: {len(code_maps.get('CODE_MAP_EN', {}))}")
    print(f"  scenario_tags: {len(scenario_tags.get('tags', {}))}")

    new_figures = 0

    for code in MISSING_CODES:
        json_path = JSON_DIR / f"{code}.json"
        if not json_path.exists():
            print(f"  SKIP {code}: file not found at {json_path}")
            continue

        try:
            data = load_json(json_path)
        except json.JSONDecodeError:
            print(f"  SKIP {code}: invalid JSON")
            continue

        if not isinstance(data, dict):
            print(f"  SKIP {code}: not a JSON object")
            continue

        if 'code' not in data or data['code'] != code:
            print(f"  SKIP {code}: code mismatch")
            continue

        modes = data.get('modes', [])
        if not modes:
            print(f"  SKIP {code}: no modes found")
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

        # Update code_maps
        code_maps['CODE_MAP'][code] = data.get('name_zh', data.get('name', code))
        code_maps['CODE_MAP_EN'][code] = data.get('name_en', data.get('name', code))

        # Update scenario_tags
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

        new_figures += 1
        print(f"  MERGED {code} with modes {modes}")

    # Save the results
    save_json(TOOLS_DIR / "scenarios_zh.json", scenarios_zh)
    save_json(TOOLS_DIR / "scenarios_en.json", scenarios_en)
    save_json(TOOLS_DIR / "code_maps.json", code_maps)
    save_json(TOOLS_DIR / "scenario_tags.json", scenario_tags)

    print(f"\n=== Merge Summary ===")
    print(f"New figures merged: {new_figures}")
    print(f"Total scenarios_zh: {len(scenarios_zh)}")
    print(f"Total scenarios_en: {len(scenarios_en)}")
    print(f"Total CODE_MAP: {len(code_maps.get('CODE_MAP', {}))}")
    print(f"Total CODE_MAP_EN: {len(code_maps.get('CODE_MAP_EN', {}))}")
    print(f"Total scenario_tags: {len(scenario_tags.get('tags', {}))}")

if __name__ == '__main__':
    main()