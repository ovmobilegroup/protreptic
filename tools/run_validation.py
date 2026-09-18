import json

# Load all canonical files
with open('scenarios_zh.json', 'r', encoding='utf-8') as f:
    zh = json.load(f)
with open('scenarios_en.json', 'r', encoding='utf-8') as f:
    en = json.load(f)
with open('code_maps.json', 'r', encoding='utf-8') as f:
    cm = json.load(f)
with open('scenario_tags.json', 'r', encoding='utf-8') as f:
    st = json.load(f)
with open('modes_data.json', 'r', encoding='utf-8') as f:
    md = json.load(f)

print('=== BASIC COUNTS ===')
print(f'scenarios_zh.json: {len(zh)} entries')
print(f'scenarios_en.json: {len(en)} entries')
print(f'code_maps.json CODE_MAP: {len(cm.get("CODE_MAP", {}))} entries')
print(f'code_maps.json CODE_MAP_EN: {len(cm.get("CODE_MAP_EN", {}))} entries')
print(f'scenario_tags.json tags: {len(st.get("tags", {}))} entries')
print(f'modes_data.json zh: {len(md.get("zh", {}))} modes')
print(f'modes_data.json en: {len(md.get("en", {}))} modes')

# Check for duplicates in scenarios_zh
zh_keys = list(zh.keys())
zh_dupes = [k for k in zh_keys if zh_keys.count(k) > 1]
print(f'\nscenarios_zh duplicate keys: {len(set(zh_dupes))}')

# Check for duplicates in scenarios_en
en_codes = [k for k in en.keys()]
en_dupes = [c for c in en_codes if en_codes.count(c) > 1]
print(f'scenarios_en duplicate keys: {len(set(en_dupes))}')

# Cross-reference check
print('\n=== CROSS-REFERENCE CHECKS ===')
# All codes from scenarios_zh
zh_codes = set(zh.keys())
# All codes from scenarios_en
en_codes_set = set(en.keys())
# All codes from code_maps
cm_zh = set(cm.get('CODE_MAP', {}).keys())
cm_en = set(cm.get('CODE_MAP_EN', {}).keys())
# All codes from scenario_tags
st_codes = set(st.get('tags', {}).keys())

print(f'scenarios_zh codes: {len(zh_codes)}')
print(f'scenarios_en codes: {len(en_codes_set)}')
print(f'code_maps CODE_MAP: {len(cm_zh)}')
print(f'code_maps CODE_MAP_EN: {len(cm_en)}')
print(f'scenario_tags codes: {len(st_codes)}')

# Find mismatches
print(f'\nIn zh but not in en: {len(zh_codes - en_codes_set)}')
print(f'In en but not in zh: {len(en_codes_set - zh_codes)}')
print(f'In zh but not in cm_zh: {len(zh_codes - cm_zh)}')
print(f'In cm_zh but not in zh: {len(cm_zh - zh_codes)}')
print(f'In zh but not in st: {len(zh_codes - st_codes)}')
print(f'In st but not in zh: {len(st_codes - zh_codes)}')

# Schema compliance check for scenarios_zh
print('\n=== SCHEMA COMPLIANCE (scenarios_zh) ===')
required_fields_zh = ['name', 'description', 'modes', 'reason', 'steps', 'expected', 'case']
missing_counts_zh = {f: 0 for f in required_fields_zh}
for k, v in zh.items():
    if isinstance(v, dict):
        for f in required_fields_zh:
            if f not in v:
                missing_counts_zh[f] += 1
for f, count in missing_counts_zh.items():
    if count > 0:
        print(f'Missing {f}: {count} entries')

# Schema compliance check for scenarios_en
print('\n=== SCHEMA COMPLIANCE (scenarios_en) ===')
required_fields_en = ['name', 'description', 'modes', 'reason', 'steps', 'expected', 'case']
missing_counts_en = {f: 0 for f in required_fields_en}
for k, v in en.items():
    if isinstance(v, dict):
        for f in required_fields_en:
            if f not in v:
                missing_counts_en[f] += 1
for f, count in missing_counts_en.items():
    if count > 0:
        print(f'Missing {f}: {count} entries')

# Check modes are integers
print('\n=== MODE TYPE CHECK ===')
non_int_modes_zh = 0
for k, v in zh.items():
    if isinstance(v, dict) and 'modes' in v:
        for m in v['modes']:
            if not isinstance(m, int):
                non_int_modes_zh += 1
print(f'scenarios_zh non-int modes: {non_int_modes_zh}')

non_int_modes_en = 0
for k, v in en.items():
    if isinstance(v, dict) and 'modes' in v:
        for m in v['modes']:
            if not isinstance(m, int):
                non_int_modes_en += 1
print(f'scenarios_en non-int modes: {non_int_modes_en}')

# Check for the 22 new entries (PK-ISL-001 etc)
print('\n=== NEW ENTRY CHECK (22 South Asia figures) ===')
new_entries = ['PK-ISL-001', 'PK-SUF-001', 'BD-LIB-001', 'LK-CIV-001', 'NP-HIM-001', 
               'AF-TRI-001', 'MV-ISL-001', 'BT-GNH-001']
for code in new_entries:
    in_zh = code in zh
    in_en = code in en_codes_set
    in_cm_zh = code in cm_zh
    in_cm_en = code in cm_en
    in_st = code in st_codes
    print(f'{code}: zh={in_zh}, en={in_en}, cm_zh={in_cm_zh}, cm_en={in_cm_en}, st={in_st}')

# Check referential integrity: all modes in scenarios must exist in modes_data
print('\n=== MODE REFERENTIAL INTEGRITY ===')
zh_modes = set(md.get('zh', {}).keys())
en_modes = set(md.get('en', {}).keys())
all_scenario_modes = set()
for k, v in zh.items():
    if isinstance(v, dict) and 'modes' in v:
        for m in v['modes']:
            all_scenario_modes.add(str(m))
for k, v in en.items():
    if isinstance(v, dict) and 'modes' in v:
        for m in v['modes']:
            all_scenario_modes.add(str(m))

missing_in_zh = all_scenario_modes - zh_modes
missing_in_en = all_scenario_modes - en_modes
print(f'Modes used in scenarios but missing in modes_data zh: {sorted(missing_in_zh)[:20]}')
print(f'Modes used in scenarios but missing in modes_data en: {sorted(missing_in_en)[:20]}')

# Check scenario_tags entries for the new entries
print('\n=== SCENARIO_TAGS DETAILED CHECK FOR NEW ENTRIES ===')
for code in new_entries:
    if code in st_codes:
        tag = st['tags'][code]
        print(f'{code}: keys={list(tag.keys())}')
    else:
        print(f'{code}: NOT FOUND in scenario_tags')

# Check code_maps entries for the new entries
print('\n=== CODE_MAPS DETAILED CHECK FOR NEW ENTRIES ===')
for code in new_entries:
    if code in cm_zh:
        print(f'{code} in CODE_MAP: {cm["CODE_MAP"][code]}')
    else:
        print(f'{code}: NOT FOUND in CODE_MAP')
    if code in cm_en:
        print(f'{code} in CODE_MAP_EN: {cm["CODE_MAP_EN"][code]}')
    else:
        print(f'{code}: NOT FOUND in CODE_MAP_EN')

# Check for null/empty values
print('\n=== NULL/EMPTY VALUE CHECK ===')
null_count_zh = 0
empty_count_zh = 0
for k, v in zh.items():
    if isinstance(v, dict):
        for fk, fv in v.items():
            if fv is None:
                null_count_zh += 1
            elif isinstance(fv, str) and fv.strip() == '':
                empty_count_zh += 1
print(f'scenarios_zh null values: {null_count_zh}')
print(f'scenarios_zh empty strings: {empty_count_zh}')

null_count_en = 0
empty_count_en = 0
for k, v in en.items():
    if isinstance(v, dict):
        for fk, fv in v.items():
            if fv is None:
                null_count_en += 1
            elif isinstance(fv, str) and fv.strip() == '':
                empty_count_en += 1
print(f'scenarios_en null values: {null_count_en}')
print(f'scenarios_en empty strings: {empty_count_en}')

# Summary
print('\n=== VALIDATION SUMMARY ===')
all_passed = True
checks = [
    ('Zero duplicate entries in scenarios_zh', len(set(zh_dupes)) == 0),
    ('Zero duplicate entries in scenarios_en', len(set(en_dupes)) == 0),
    ('Zero ID conflicts (zh vs en)', len(zh_codes - en_codes_set) == 0),
    ('Zero ID conflicts (zh vs cm_zh)', len(zh_codes - cm_zh) == 0),
    ('Zero ID conflicts (cm_zh vs zh)', len(cm_zh - zh_codes) == 0),
    ('Zero ID conflicts (zh vs st)', len(zh_codes - st_codes) == 0),
    ('Schema compliance scenarios_zh', sum(missing_counts_zh.values()) == 0),
    ('Schema compliance scenarios_en', sum(missing_counts_en.values()) == 0),
    ('Modes are integers (zh)', non_int_modes_zh == 0),
    ('Modes are integers (en)', non_int_modes_en == 0),
    ('Mode referential integrity (zh)', len(missing_in_zh) == 0),
    ('Mode referential integrity (en)', len(missing_in_en) == 0),
    ('New entries queryable in all files', all(code in zh and code in en_codes_set and code in cm_zh and code in cm_en and code in st_codes for code in new_entries)),
    ('No null values in scenarios_zh', null_count_zh == 0),
    ('No null values in scenarios_en', null_count_en == 0),
]

for desc, result in checks:
    status = '✅ PASS' if result else '❌ FAIL'
    if not result:
        all_passed = False
    print(f'  {status} {desc}')

print(f'\nOverall: {"ALL CHECKS PASSED" if all_passed else "SOME CHECKS FAILED"}')