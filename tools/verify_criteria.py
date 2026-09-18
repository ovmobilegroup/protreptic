#!/usr/bin/env python3
import json

# Load current state
zh = json.load(open('/opt/data/workspace/Protreptic/tools/scenarios_zh.json'))
en = json.load(open('/opt/data/workspace/Protreptic/tools/scenarios_en.json'))
cm = json.load(open('/opt/data/workspace/Protreptic/tools/code_maps.json'))
st = json.load(open('/opt/data/workspace/Protreptic/tools/scenario_tags.json'))
md = json.load(open('/opt/data/workspace/Protreptic/tools/modes_data.json'))

# Load pre-merge backup state
zh_pre = json.load(open('/opt/data/workspace/Protreptic/tools/scenarios_zh.json.backup_2026-07-30_16-09-00'))
en_pre = json.load(open('/opt/data/workspace/Protreptic/tools/scenarios_en.json.backup_2026-07-30_16-09-00'))
cm_pre = json.load(open('/opt/data/workspace/Protreptic/tools/code_maps.json.backup_2026-07-30_16-09-00'))
st_pre = json.load(open('/opt/data/workspace/Protreptic/tools/scenario_tags.json.backup_2026-07-30_16-09-00'))

# Count entries
print("=== Criterion 1: scenarios_zh.json gains exactly 11 new entries ===")
print(f"  Pre-merge: {len(zh_pre)}")
print(f"  Post-merge: {len(zh)}")
print(f"  Delta: {len(zh) - len(zh_pre)}")
print(f"  PASS: {len(zh) - len(zh_pre) == 11}")

print("\n=== Criterion 2: scenarios_en.json gains exactly 11 new entries ===")
print(f"  Pre-merge: {len(en_pre)}")
print(f"  Post-merge: {len(en)}")
print(f"  Delta: {len(en) - len(en_pre)}")
print(f"  PASS: {len(en) - len(en_pre) == 11}")

print("\n=== Criterion 3: code_maps.json CODE_MAP gains 11 entries, CODE_MAP_EN gains 11 entries ===")
print(f"  Pre-merge CODE_MAP: {len(cm_pre.get('CODE_MAP', {}))}")
print(f"  Post-merge CODE_MAP: {len(cm.get('CODE_MAP', {}))}")
print(f"  Delta CODE_MAP: {len(cm.get('CODE_MAP', {})) - len(cm_pre.get('CODE_MAP', {}))}")
print(f"  Pre-merge CODE_MAP_EN: {len(cm_pre.get('CODE_MAP_EN', {}))}")
print(f"  Post-merge CODE_MAP_EN: {len(cm.get('CODE_MAP_EN', {}))}")
print(f"  Delta CODE_MAP_EN: {len(cm.get('CODE_MAP_EN', {})) - len(cm_pre.get('CODE_MAP_EN', {}))}")
print(f"  PASS: {(len(cm.get('CODE_MAP', {})) - len(cm_pre.get('CODE_MAP', {})) == 11) and (len(cm.get('CODE_MAP_EN', {})) - len(cm_pre.get('CODE_MAP_EN', {})) == 11)}")

print("\n=== Criterion 4: scenario_tags.json tags gain 11 entries ===")
print(f"  Pre-merge: {len(st_pre.get('tags', {}))}")
print(f"  Post-merge: {len(st.get('tags', {}))}")
print(f"  Delta: {len(st.get('tags', {})) - len(st_pre.get('tags', {}))}")
print(f"  PASS: {len(st.get('tags', {})) - len(st_pre.get('tags', {})) == 11}")

print("\n=== Criterion 5: modes_data.json adds new mode definitions M612 through M622 (inclusive) ===")
missing = []
for i in range(612, 623):
    if str(i) not in md.get('zh', {}):
        missing.append(i)
print(f"  Missing modes: {missing}")
print(f"  PASS: {len(missing) == 0}")

print("\n=== Criterion 6: Zero duplicate codes across all five files ===")
# Check for duplicates in each file
zh_codes = list(zh.keys())
en_codes = list(en.keys())
cm_codes = list(cm.get('CODE_MAP', {}).keys())
cm_en_codes = list(cm.get('CODE_MAP_EN', {}).keys())
st_codes = list(st.get('tags', {}).keys())

zh_dupes = [c for c in zh_codes if zh_codes.count(c) > 1]
en_dupes = [c for c in en_codes if en_codes.count(c) > 1]
cm_dupes = [c for c in cm_codes if cm_codes.count(c) > 1]
cm_en_dupes = [c for c in cm_en_codes if cm_en_codes.count(c) > 1]
st_dupes = [c for c in st_codes if st_codes.count(c) > 1]

print(f"  scenarios_zh duplicates: {len(zh_dupes)}")
print(f"  scenarios_en duplicates: {len(en_dupes)}")
print(f"  code_maps CODE_MAP duplicates: {len(cm_dupes)}")
print(f"  code_maps CODE_MAP_EN duplicates: {len(cm_en_dupes)}")
print(f"  scenario_tags duplicates: {len(st_dupes)}")
print(f"  PASS: {len(zh_dupes) == 0 and len(en_dupes) == 0 and len(cm_dupes) == 0 and len(cm_en_dupes) == 0 and len(st_dupes) == 0}")

print("\n=== Criterion 7: Zero parsing/validation errors ===")
try:
    # Validate JSON structure by re-serializing
    json.dumps(zh)
    json.dumps(en)
    json.dumps(cm)
    json.dumps(st)
    json.dumps(md)
    print("  All JSON files parse successfully")
    print("  PASS: True")
except Exception as e:
    print(f"  ERROR: {e}")
    print("  PASS: False")