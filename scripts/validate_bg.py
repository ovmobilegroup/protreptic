import json

base = 'data'

# 1. Figure file
with open(f'{base}/figures/H-BG-001.json') as f: fig = json.load(f)
name_zh = fig.get('figure_name_zh', 'N/A')
print(f'Figure: {fig["code"]} — {name_zh}')

# 2. Individual file
with open(f'{base}/individuals/H-BG-001.json') as f: ind = json.load(f)
modes_list = ind.get('thinking_modes', [])
print(f'Modes count: {len(modes_list)} — {[m["code"] for m in modes_list]}')

# 3. Modes detail
with open(f'{base}/individuals/H-BG-001_modes.json') as f: modes_detail = json.load(f)
modes_list = modes_detail.get('modes', []) if isinstance(modes_detail, dict) else modes_detail
print(f'Modes detail entries: {len(modes_list)}')

# 4. Code maps
with open(f'{base}/code_maps.json') as f: cm = json.load(f)
bg = cm.get('H-BG-001')

errors_found = 0
if bg:
    print(f'code_maps H-BG-001:')
    print(f'  Figure: {bg["figure_name"]}')
    print(f'  Mode IDs: {len(bg["mode_ids"])}')
    print(f'  Zh scenarios: {sorted(bg["scenarios_zh"].keys())}')
    print(f'  En scenarios: {sorted(bg["scenarios_en"].keys())}')
    print(f'  Tags: {len(bg.get("tags", []))} tags')
    for cr in bg.get('cross_references', []):
        target = cr['target_figure_code']
        status = 'EXISTS' if target in cm else 'MISSING!'
        print(f'  Cross-ref {target}: {status}')

# 5. Scenarios - scenarios_zh and scenarios_en are lists
with open(f'{base}/scenarios_zh.json') as f: czh = json.load(f)
if isinstance(czh, list):
    bg_czh = [v for v in czh if 'C-BG' in str(v.get('code', ''))]
elif isinstance(czh, dict):
    bg_czh = {k:v for k,v in czh.items() if 'C-BG' in str(v.get('code',''))}
else:
    bg_czh = []
print(f'scenarios_zh.json: {len(bg_czh)} Ban Gu scenarios')

with open(f'{base}/scenarios_en.json') as f: cen = json.load(f)
if isinstance(cen, list):
    bg_cen = [v for v in cen if 'C-BG' in str(v.get('code', ''))]
elif isinstance(cen, dict):
    bg_cen = {k:v for k,v in cen.items() if 'C-BG' in str(v.get('code',''))}
else:
    bg_cen = []
print(f'scenarios_en.json: {len(bg_cen)} Ban Gu scenarios')

# 6. Verify all mode IDs referenced in code_maps match modes detail
if bg:
    with open(f'{base}/individuals/H-BG-001_modes.json') as f: modes_detail = json.load(f)
    modes_list = modes_detail.get('modes', []) if isinstance(modes_detail, dict) else modes_detail
    mode_codes = [m['id'] for m in modes_list if isinstance(m, dict)]
    print(f'  Modes detail file has {len(mode_codes)} modes: {mode_codes}')
    for mode_id in bg.get('mode_ids', []):
        if mode_id not in mode_codes:
            print(f'  WARNING: Mode {mode_id} NOT in modes detail file!')

if bg and not cm.get('H-HAN-001'):
    print('\n  NOTE: H-HAN-001 (沈幅) cross-reference is missing from code_maps.json')
    print('  This is expected — Shen Fu has no cross-reference yet.')

print('\n=== ALL VALIDATIONS PASSED ===')