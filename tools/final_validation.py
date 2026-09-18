#!/usr/bin/env python3
"""
Comprehensive validation for the Israel/Middle East merge:
1. Check zero duplicate keys
2. Check zero conflicts between zh/en
3. Compute current checksums (new reference for merged state)
4. Run CLI tests
"""

import json
import hashlib

TOOLS_DIR = "/opt/data/workspace/Protreptic/tools"

def compute_sha256(path):
    with open(path, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

print("=== Loading authoritative files ===")
scenarios_zh = load_json(f"{TOOLS_DIR}/scenarios_zh.json")
scenarios_en = load_json(f"{TOOLS_DIR}/scenarios_en.json")
code_maps = load_json(f"{TOOLS_DIR}/code_maps.json")
scenario_tags = load_json(f"{TOOLS_DIR}/scenario_tags.json")
modes_data = load_json(f"{TOOLS_DIR}/modes_data.json")

print(f"scenarios_zh: {len(scenarios_zh)} entries")
print(f"scenarios_en: {len(scenarios_en)} entries")
print(f"code_maps CODE_MAP: {len(code_maps.get('CODE_MAP', {}))} entries")
print(f"code_maps CODE_MAP_EN: {len(code_maps.get('CODE_MAP_EN', {}))} entries")
print(f"scenario_tags: {len(scenario_tags.get('tags', {}))} entries")

# 1. Check duplicate keys
print("\n=== 1. Duplicate Key Check ===")
zh_keys = list(scenarios_zh.keys())
en_keys = list(scenarios_en.keys())
cm_keys = list(code_maps.get('CODE_MAP', {}).keys())
st_keys = list(scenario_tags.get('tags', {}).keys())

zh_dupes = [k for k, v in {k: zh_keys.count(k) for k in zh_keys}.items() if v > 1]
en_dupes = [k for k, v in {k: en_keys.count(k) for k in en_keys}.items() if v > 1]
cm_dupes = [k for k, v in {k: cm_keys.count(k) for k in cm_keys}.items() if v > 1]
st_dupes = [k for k, v in {k: st_keys.count(k) for k in st_keys}.items() if v > 1]

print(f"scenarios_zh duplicates: {len(zh_dupes)}")
print(f"scenarios_en duplicates: {len(en_dupes)}")
print(f"code_maps duplicates: {len(cm_dupes)}")
print(f"scenario_tags duplicates: {len(st_dupes)}")

if zh_dupes: print(f"  ZH dupes: {zh_dupes}")
if en_dupes: print(f"  EN dupes: {en_dupes}")
if cm_dupes: print(f"  CM dupes: {cm_dupes}")
if st_dupes: print(f"  ST dupes: {st_dupes}")

# 2. Check conflicts between zh/en for the merged entries
print("\n=== 2. Conflict Check (zh vs en for merged entries) ===")
merged_codes = ['IL-DIAS-001', 'IL-LIT-001', 'IL-MIL-001', 
                'AE-ZAY-001', 'SA-OIL-001', 'JO-HAS-001', 'BH-ISL-001', 
                'QA-ENE-001', 'OM-QAB-001', 'LB-CON-001', 'SY-ALA-001', 
                'IQ-CAL-001', 'IR-KHA-001', 'YE-HOU-001']

conflicts = []
for code in merged_codes:
    if code in scenarios_zh and code in scenarios_en:
        zh_entry = scenarios_zh[code]
        en_entry = scenarios_en[code]
        
        # Check critical fields match
        if zh_entry.get('code') != en_entry.get('code'):
            conflicts.append(f"{code}: code mismatch")
        if zh_entry.get('modes') != en_entry.get('modes'):
            conflicts.append(f"{code}: modes mismatch - zh={zh_entry.get('modes')} en={en_entry.get('modes')}")
        if zh_entry.get('wiki_id') != en_entry.get('wiki_id'):
            conflicts.append(f"{code}: wiki_id mismatch")
        if zh_entry.get('name_zh') != en_entry.get('name_en'):
            # Name can differ (translation), but code should match
            pass

print(f"Conflicts found: {len(conflicts)}")
for c in conflicts:
    print(f"  - {c}")

# 3. Check cross-file consistency
print("\n=== 3. Cross-File Consistency ===")
all_codes = set(scenarios_zh.keys()) | set(scenarios_en.keys())
print(f"Total unique codes in scenarios: {len(all_codes)}")

missing_in_en = set(scenarios_zh.keys()) - set(scenarios_en.keys())
missing_in_zh = set(scenarios_en.keys()) - set(scenarios_zh.keys())
print(f"Missing in en: {len(missing_in_en)}")
print(f"Missing in zh: {len(missing_in_zh)}")

missing_in_cm = all_codes - set(code_maps.get('CODE_MAP', {}).keys())
print(f"Missing in code_maps: {len(missing_in_cm)}")

missing_in_st = all_codes - set(scenario_tags.get('tags', {}).keys())
print(f"Missing in scenario_tags: {len(missing_in_st)}")

# 4. Current checksums (new reference for merged state)
print("\n=== 4. Current Checksums (Post-Merge Reference) ===")
checksums = {}
for fname in ["scenarios_zh.json", "scenarios_en.json", "code_maps.json", "modes_data.json", "scenario_tags.json"]:
    checksums[fname] = compute_sha256(f"{TOOLS_DIR}/{fname}")
    print(f"{fname}: {checksums[fname]}")

# Save checksums for reference
with open(f"{TOOLS_DIR}/post_merge_checksums.json", 'w') as f:
    json.dump(checksums, f, indent=2)
print("\nSaved post-merge checksums to post_merge_checksums.json")

# 5. Run CLI tests
print("\n=== 5. CLI Tests ===")
import subprocess
result = subprocess.run(["python", "run_cli_tests.py"], capture_output=True, text=True, cwd=TOOLS_DIR)
print(result.stdout)
if result.stderr:
    print("STDERR:", result.stderr)
print(f"Exit code: {result.returncode}")

# Summary
print("\n=== SUMMARY ===")
print(f"Duplicate keys: {len(zh_dupes) + len(en_dupes) + len(cm_dupes) + len(st_dupes)}")
print(f"Conflicts: {len(conflicts)}")
print(f"CLI tests: {'PASS' if result.returncode == 0 else 'FAIL'}")
print(f"Cross-file gaps - code_maps: {len(missing_in_cm)}, scenario_tags: {len(missing_in_st)}")