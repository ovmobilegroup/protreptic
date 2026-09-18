"""
Complete H-HLG-001 integration script (v4 - handles all 4 file formats, code_maps restored from git).
Applies Hua Luogeng (华罗庚) full v6 schema entry to all 4 data files.
"""
import json

PROJ = '/opt/data/workspace/Protreptic'

# ── 1. Update modes_data.json (list of dicts, append) ───────────────
with open(f'{PROJ}/modes_data.json', 'r') as f:
    modes_list = json.load(f)

hhlg_modes_entry = {
    "code": "H-HLG-001",
    "name": "华罗庚",
    "core_mode": "M9 独立自主法/多元思维模型/摸石头过河/战略预判法",
    "new_mode": "",  # No new mode (same as core) - standard for H-HLG-001
    "wiki_id": "",  # Placeholder for wiki entry (created separately)
    "nationality_standardized": "Chinese",
    "civilization_sphere": "Confucian Cultural Sphere/Modern Science",
    "time_period_standardized": "1910-1985 (Modern)",
    "primary_language": "Chinese",
    "gender_zh": "Male",
    "role_zh": "Mathematician / Applied Mathematician / Science Organizer"
}

if not any(e.get('code') == 'H-HLG-001' for e in modes_list):
    modes_list.append(hhlg_modes_entry)

with open(f'{PROJ}/modes_data.json', 'w') as f:
    json.dump(modes_list, f, ensure_ascii=False, indent=2)

print(f'modes_data.json: {len(modes_list)} entries (H-HLG-001 added)')

# ── 2. Update scenarios_zh.json (LIST of dicts, append) ─────────────
with open(f'{PROJ}/scenarios_zh.json', 'r') as f:
    zh_list = json.load(f)

hhlg_zh_entry = {
    "code": "H-HLG-001",
    "name": "华罗庚",
    "core_mode": "M9 独立自主法/多元思维模型/摸石头过河/战略预判法",
    "new_mode": "",
    "category": "中国/现代数学",
    "region": "中国大陆",
    "country": "中国",
    "time_period_standardized": "1910-1985（现代）",
    "nationality_standardized": "中国",
    "civilization_sphere": "儒家文化圈/现代科学",
    "primary_language": "中文",
    "gender_zh": "男",
    "role_zh": "数学家/应用数学家/科学组织家",
    "description_zh": "华罗庚：自学成才的数学天才，从杂货店学徒到世界顶级数学家。创立'优选法'和'统筹法'，推动数学方法的群众化应用。在代数、数论、多复变函数论等领域做出原创性贡献，培养了陈景润等大批数学人才。",
    "description_en": "Hua Luogeng: A self-taught mathematical genius who went from a shop apprentice to one of the world's top mathematicians. Created 'optimization methods' and 'scheduling methods', promoting popular application of mathematical techniques. Made original contributions to algebra, number theory, and several complex variable theory, mentoring many mathematicians including Chen Jingrun.",
    "reason_zh": "核心思维：M9（独立自主法/自学精神）、多元思维模型、摸石头过河（应用数学工程化）、战略预判。华罗庚从学徒到数学家，体现了自学成才的独立自主精神；他创立优选法和统筹法是将数学理论工程化的典范；战略预判体现在其对学科发展的长远布局。",
    "reason_en": "Core thinking modes: M9 (Independent Self-Study Method/Self-Learning Spirit), Multi-Model Thinking, 'Crossing the River by Feeling Stones' (Applied Mathematics Engineering), Strategic Forecasting. Hua Luogeng's journey from apprentice to mathematician embodies independent self-study spirit; his creation of optimization and scheduling methods is a paradigm of mathematical theory engineering; strategic forecasting reflected in long-term discipline development planning.",
    "wiki_id": "",
    "modes": [9],
    "steps_zh": [
        "Step 1: 自学奠基——华罗庚用'独立自主法'(M9)从初中数学教材起步，通过自学攻克高中、大学微积分",
        "Step 2: 多元建模——将纯数学理论转化为'优选法'(0.618法)和'统筹法'，实现从理论到应用的工程化",
        "Step 3: 战略预判——预见中国数学学科发展方向，布局多复变函数论、代数等多领域",
        "Step 4: 人才培养——培养陈景润等大批数学人才，建立中国数学学派"
    ],
    "steps_en": [
        "Step 1: Self-Study Foundation -- Hua Luogeng used 'Independent Self-Study Method' (M9) starting from middle school math textbooks, self-studying through high school and university calculus",
        "Step 2: Multi-Model Engineering -- Translated pure math theory into 'Optimization Methods' (0.618 method) and 'Scheduling Methods', achieving theory-to-application engineering",
        "Step 3: Strategic Forecasting -- Anticipated China's mathematics discipline development direction, laying out multiple complex variable theory, algebra and other fields",
        "Step 4: Talent Cultivation -- Mentored many mathematicians including Chen Jingrun, establishing the Chinese mathematics school"
    ]
}

if not any(e.get('code') == 'H-HLG-001' for e in zh_list):
    zh_list.append(hhlg_zh_entry)

with open(f'{PROJ}/scenarios_zh.json', 'w') as f:
    json.dump(zh_list, f, ensure_ascii=False, indent=2)

print(f'scenarios_zh.json: {len(zh_list)} entries (H-HLG-001 added)')

# ── 3. Update scenarios_en.json (LIST of dicts, append) ─────────────
with open(f'{PROJ}/scenarios_en.json', 'r') as f:
    en_list = json.load(f)

hhlg_en_entry = {
    "code": "H-HLG-001",
    "name": "Hua Luogeng",
    "core_mode": "M9 独立自主法/多元思维模型/摸石头过河/战略预判法",
    "new_mode": "",
    "category": "Chinese/Modern Mathematics",
    "region": "Mainland China",
    "country": "China",
    "time_period_standardized": "1910-1985 (Modern)",
    "nationality_standardized": "Chinese",
    "civilization_sphere": "Confucian Cultural Sphere/Modern Science",
    "primary_language": "Chinese",
    "gender_zh": "Male",
    "role_zh": "Mathematician / Applied Mathematician / Science Organizer",
    "description_zh": "华罗庚：自学成才的数学天才，从杂货店学徒到世界顶级数学家。创立'优选法'和'统筹法'，推动数学方法的群众化应用。在代数、数论、多复变函数论等领域做出原创性贡献，培养了陈景润等大批数学人才。",
    "description_en": "Hua Luogeng: A self-taught mathematical genius who went from a shop apprentice to one of the world's top mathematicians. Created 'optimization methods' and 'scheduling methods', promoting popular application of mathematical techniques. Made original contributions to algebra, number theory, and several complex variable theory, mentoring many mathematicians including Chen Jingrun.",
    "reason_zh": "核心思维：M9（独立自主法/自学精神）、多元思维模型、摸石头过河（应用数学工程化）、战略预判。华罗庚从学徒到数学家，体现了自学成才的独立自主精神；他创立优选法和统筹法是将数学理论工程化的典范；战略预判体现在其对学科发展的长远布局。",
    "reason_en": "Core thinking modes: M9 (Independent Self-Study Method/Self-Learning Spirit), Multi-Model Thinking, 'Crossing the River by Feeling Stones' (Applied Mathematics Engineering), Strategic Forecasting. Hua Luogeng's journey from apprentice to mathematician embodies independent self-study spirit; his creation of optimization and scheduling methods is a paradigm of mathematical theory engineering; strategic forecasting reflected in long-term discipline development planning.",
    "wiki_id": "",
    "modes": [9],
    "steps_zh": [
        "Step 1: 自学奠基——华罗庚用'独立自主法'(M9)从初中数学教材起步，通过自学攻克高中、大学微积分",
        "Step 2: 多元建模——将纯数学理论转化为'优选法'(0.618法)和'统筹法'，实现从理论到应用的工程化",
        "Step 3: 战略预判——预见中国数学学科发展方向，布局多复变函数论、代数等多领域",
        "Step 4: 人才培养——培养陈景润等大批数学人才，建立中国数学学派"
    ],
    "steps_en": [
        "Step 1: Self-Study Foundation -- Hua Luogeng used 'Independent Self-Study Method' (M9) starting from middle school math textbooks, self-studying through high school and university calculus",
        "Step 2: Multi-Model Engineering -- Translated pure math theory into 'Optimization Methods' (0.618 method) and 'Scheduling Methods', achieving theory-to-application engineering",
        "Step 3: Strategic Forecasting -- Anticipated China's mathematics discipline development direction, laying out multiple complex variable theory, algebra and other fields",
        "Step 4: Talent Cultivation -- Mentored many mathematicians including Chen Jingrun, establishing the Chinese mathematics school"
    ]
}

if not any(e.get('code') == 'H-HLG-001' for e in en_list):
    en_list.append(hhlg_en_entry)

with open(f'{PROJ}/scenarios_en.json', 'w') as f:
    json.dump(en_list, f, ensure_ascii=False, indent=2)

print(f'scenarios_en.json: {len(en_list)} entries (H-HLG-001 added)')

# ── 4. Update code_maps.json (flat dict keyed by code, append) ──────
with open(f'{PROJ}/code_maps.json', 'r') as f:
    cm = json.load(f)

# Add H-HLG-001 and H-HLG-002 (flat dict format - key is code, value is description)
if 'H-HLG-001' not in cm:
    cm['H-HLG-001'] = '华罗庚：数学自学成才与应用数学工程化全链路自主范式'
    cm['H-HLG-002'] = '华罗庚：优选法/多元思维模型/战略预判/摸石头过河'

with open(f'{PROJ}/code_maps.json', 'w') as f:
    json.dump(cm, f, ensure_ascii=False, indent=2)

# ── 5. Final Verification ───────────────────────────────────────────
with open(f'{PROJ}/modes_data.json', 'r') as f:
    ml = json.load(f)
with open(f'{PROJ}/scenarios_zh.json', 'r') as f:
    sz = json.load(f)
with open(f'{PROJ}/scenarios_en.json', 'r') as f:
    se = json.load(f)
with open(f'{PROJ}/code_maps.json', 'r') as f:
    cmm = json.load(f)

all_ok = (
    any(e.get('code') == 'H-HLG-001' for e in ml) and
    any(e.get('code') == 'H-HLG-001' for e in sz) and
    any(e.get('code') == 'H-HLG-001' for e in se) and
    'H-HLG-001' in cmm
)

print(f'\n=== FINAL VERIFICATION ===')
if all_ok:
    print('H-HLG-001 integration: COMPLETE (all 4 files)')
else:
    print('H-HLG-001 integration: FAILED - check individual files')

for k, v in [
    ('modes_data', any(e.get('code') == 'H-HLG-001' for e in ml)),
    ('scenarios_zh', any(e.get('code') == 'H-HLG-001' for e in sz)),
    ('scenarios_en', any(e.get('code') == 'H-HLG-001' for e in se)),
    ('code_maps', 'H-HLG-001' in cmm)
]:
    print(f'  {k}: {"OK" if v else "MISSING"}')

# Print details
for e in ml:
    if e.get('code') == 'H-HLG-001':
        print(f'\nmodes_data H-HLG-001:')
        print(f'  name={e.get("name")}, core_mode={e.get("core_mode")}')
        break

for e in sz:
    if e.get('code') == 'H-HLG-001':
        print(f'\nscenarios_zh H-HLG-001:')
        print(f'  name={e.get("name")}, core_mode={e.get("core_mode")}')
        print(f'  category={e.get("category")}, region={e.get("region")}')
        print(f'  modes={e.get("modes")}, steps_zh count={len(e.get("steps_zh", []))}')
        break

print(f'\ncode_maps H-HLG-001: {cmm.get("H-HLG-001")}')
print(f'code_maps H-HLG-002: {cmm.get("H-HLG-002")}')

print('\n=== Integration complete ===')