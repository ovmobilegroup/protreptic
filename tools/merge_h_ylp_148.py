#!/usr/bin/env python3
"""
Merge Report Generator for H-YLP-001 (袁隆平)
"""
import json
from datetime import datetime
from pathlib import Path

WORKSPACE = Path('/opt/data/workspace/Protreptic')
TOOLS_DIR = WORKSPACE / 'tools'

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# Load current state
scenarios_zh = load_json(TOOLS_DIR / 'scenarios_zh.json')
scenarios_en = load_json(TOOLS_DIR / 'scenarios_en.json')
code_maps = load_json(TOOLS_DIR / 'code_maps.json')
scenario_tags = load_json(TOOLS_DIR / 'scenario_tags.json')

# Generate merge report
report = {
    "merge_timestamp": datetime.now().isoformat(),
    "figure_code": "H-YLP-148",
    "figure_name": "袁隆平 / Yuan Longping",
    "new_entry_added": True,
    "modes_merged": [1, 36, 23, 24, 41],
    "verification": {
        "scenarios_zh_has_entry": "H-YLP-148" in scenarios_zh,
        "scenarios_en_has_entry": "H-YLP-148" in scenarios_en,
        "code_maps_code_map_has_entry": "H-YLP-148" in code_maps.get('CODE_MAP', {}),
        "code_maps_code_map_en_has_entry": "EN-H-YLP-148" in code_maps.get('CODE_MAP_EN', {}),
        "scenario_tags_has_entry": "H-YLP-148" in scenario_tags.get('tags', {}),
    },
    "stats": {
        "total_scenarios_zh": len(scenarios_zh),
        "total_scenarios_en": len(scenarios_en),
        "total_code_map_entries": len(code_maps.get('CODE_MAP', {})),
        "total_code_map_en_entries": len(code_maps.get('CODE_MAP_EN', {})),
    },
    "issues": [
        "H-YLP-148 missing from scenario_tags.json - manual entry needed",
    ]
}

# Save report
report_path = WORKSPACE / 'merge_report_h_ylp_148.json'
save_json(report_path, report)
print(f"Report saved to: {report_path}")

# Create backup of main files
backup_dir = WORKSPACE / 'backup_pre_merge_20260901_085200'
backup_dir.mkdir(exist_ok=True)
save_json(backup_dir / 'scenarios_zh.json', scenarios_zh)
save_json(backup_dir / 'scenarios_en.json', scenarios_en)
save_json(backup_dir / 'code_maps.json', code_maps)
save_json(backup_dir / 'scenario_tags.json', scenario_tags)
print(f"Backup created at: {backup_dir}")

# Check scenario_tags for H-YLP-148
if "H-YLP-148" not in scenario_tags.get('tags', {}):
    print("ISSUE: H-YLP-148 NOT in scenario_tags.json - needs manual fix")
else:
    print("OK: H-YLP-148 is in scenario_tags.json")
