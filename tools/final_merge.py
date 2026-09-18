#!/usr/bin/env python3
"""
Final merger script - restore July baseline and merge only Middle East figures
This script:
1. Restores the 16 baseline entries from July 30 backup
2. Merges only the 11 Middle East scenarios (M612-M622)
3. Produces exactly 11 new entries total
"""

import json
import sys
from pathlib import Path

TOOLS_DIR = Path("/opt/data/workspace/Protreptic/tools")
JSON_DIR = TOOLS_DIR / "json"

# Load July 30 baseline (16 entries)
with open(TOOLS_DIR / "scenarios_zh.json.backup_2026-07-30_16-09-00", 'r', encoding='utf-8') as f:
    zh = json.load(f)
with open(TOOLS_DIR / "scenarios_en.json.backup_2026-07-30_16-09-00", 'r', encoding='utf-8') as f:
    en = json.load(f)
with open(TOOLS_DIR / "code_maps.json.backup_2026-07-30_16-09-00", 'r', encoding='utf-8') as f:
    cm = json.load(f)
with open(TOOLS_DIR / "scenario_tags.json.backup_2026-07-30_16-09-00", 'r', encoding='utf-8') as f:
    st = json.load(f)

print(f"Restored baseline: {len(zh)} scenarios")
print(f"Baseline CODE_MAP entries: {len(cm.get('CODE_MAP', {}))}")

# Load modes data (this should already contain M612-M622)
with open(TOOLS_DIR / "modes_data.json", 'r', encoding='utf-8') as f:
    md = json.load(f)

print(f"Modes data contains M612-M622: {all(str(i) in md.get('zh', {}) for i in range(612, 623))}")

# 11 Middle East scenarios to add
ME_CODES = [
    "AE-ZAY-001", "SA-OIL-001", "JO-HAS-001", "BH-ISL-001", "QA-ENE-001",
    "OM-QAB-001", "LB-CON-001", "SY-ALA-001", "IQ-CAL-001", "IR-KHA-001", "YE-HOU-001"
]

new_figures = 0

# Process each Middle East figure
for code in ME_CODES:
    # Read from project root
    json_path = Path("/opt/data/workspace/Protreptic") / f"{code}.json"
    if not json_path.exists():
        print(f"SKIP {code}: file not found at {json_path}")
        continue

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError:
        print(f"SKIP {code}: invalid JSON")
        continue

    # Extract modes
    modes = data.get('modes', [])
    if not modes:
        print(f"SKIP {code}: no modes found")
        continue

    # Add to main data files
    zh[code] = data

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
    en[code] = en_entry

    # Update code maps
    cm['CODE_MAP'][code] = data.get('name_zh', data.get('name', code))
    cm['CODE_MAP_EN'][code] = data.get('name_en', data.get('name', code))

    # Update scenario tags
    st['tags'][code] = {
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
    print(f"MERGED {code} with modes {modes}")

# Save the results
with open(TOOLS_DIR / "scenarios_zh.json", 'w', encoding='utf-8') as f:
    json.dump(zh, f, ensure_ascii=False, indent=2)
with open(TOOLS_DIR / "scenarios_en.json", 'w', encoding='utf-8') as f:
    json.dump(en, f, ensure_ascii=False, indent=2)
with open(TOOLS_DIR / "code_maps.json", 'w', encoding='utf-8') as f:
    json.dump(cm, f, ensure_ascii=False, indent=2)
with open(TOOLS_DIR / "scenario_tags.json", 'w', encoding='utf-8') as f:
    json.dump(st, f, ensure_ascii=False, indent=2)

print(f"\n=== Final Merge Summary ===")
print(f"Baseline entries: 16")
print(f"Middle East entries added: {new_figures}")
print(f"Total entries: {len(zh)}")
print(f"CODE_MAP entries: {len(cm.get('CODE_MAP', {}))}")
print(f"Expected: 27 total entries (16 baseline + 11 Middle East)")
print(f"Target delta: exactly 11 new entries")

# Exit with success code
sys.exit(0)