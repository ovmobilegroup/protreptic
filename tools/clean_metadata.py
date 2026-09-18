#!/usr/bin/env python3
"""Clean up metadata/template entries from scenarios files"""
import json

# Keys that are metadata/template entries (not actual scenarios)
METADATA_KEYS = {
    'case', 'civilization_sphere', 'code', 'cross_cultural_impact', 'description',
    'domains', 'era', 'ethnicity', 'expected', 'gender', 'historical_domains',
    'intellectual_tradition', 'modes', 'name', 'nationality', 'primary_language',
    'quality_checklist_v2', 'reason', 'steps', 'test_thinking_mode_selector',
    'time_period_standardized', 'wiki_id'
}

def clean_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    original_count = len(data)
    # Remove metadata/template entries
    cleaned = {k: v for k, v in data.items() if k not in METADATA_KEYS}
    removed = original_count - len(cleaned)
    print(f"  {filepath}: removed {removed} metadata entries, {len(cleaned)} remaining")
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(cleaned, f, ensure_ascii=False, indent=2)
    
    return removed

removed_zh = clean_file('/opt/data/workspace/Protreptic/scenarios_zh.json')
removed_en = clean_file('/opt/data/workspace/Protreptic/scenarios_en.json')
print(f"Total removed: {removed_zh + removed_en}")