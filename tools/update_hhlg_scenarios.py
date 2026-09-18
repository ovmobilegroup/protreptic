import json
import re

# Read the Serrano deliverable for H-HLG-001 source data
with open('/opt/data/workspace/Protrectic/H-HLG-001-deliverable.md', 'r') as f:
    deliverable = f.read()

# Extract key info from deliverable (华罗庚's story)
# H-HLG-001 is about Hua Luogeng: mathematical self-taught talent
# core_mode: M9 独立自主法/多元思维模型/摸石头过河/战略预判法
# new_mode: M9 (same as core - no NEW mode created)

# First, fix scenarios_zh.json with complete H-HLG-001
with open('/opt/data/workspace/Protreptic/scenarios_zh.json', 'r') as f:
    zh = json.load(f)

# Build complete H-HLG-001 entry (matching the full v6 schema from deliverable)
hhlg_zh = {
    "code": "H-HLG-001",
    "name": "华罗庚",
    "core_mode": "M9 独立自主法/多元思维模型/摸石头过河/战略预判法",
    "new_mode": "",  # No new mode created (same as core)
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
    "description_en": "Hua Luogeng: A self-taught mathematical genius who went from a杂货店 apprentice to one of the world's top mathematicians. Created 'optimization methods' and 'scheduling methods', promoting popular application of mathematical techniques. Made original contributions to algebra, number theory, and several complex variable theory, mentoring many mathematicians including Chen Jingrun.",
    "reason_zh": "核心思维：M9（独立自主法/自学精神）、多元思维模型、摸石头过河（应用数学工程化）、战略预判。华罗庚从学徒到数学家，体现了自学成才的独立自主精神；他创立优选法和统筹法是将数学理论工程化的典范；战略预判体现在其对学科发展的长远布局。",
    "reason_en": "Core thinking modes: M9 (Independent Self-Study Method/Self-Learning Spirit), Multi-Model Thinking, 'Crossing the River by Feeling Stones' (Applied Mathematics Engineering), Strategic Forecasting. Hua Luogeng's journey from apprentice to mathematician embodies independent self-study spirit; his creation of optimization and scheduling methods is a paradigm of mathematical theory engineering; strategic forecasting reflected in long-term discipline development planning.",
    "wiki_id": "",
    "modes": [9],
    "steps_zh": ["Step 1: 自学奠基——华罗庚用'独立自主法'(M9)从初中数学教材起步，通过自学攻克高中、大学微积分", "Step 2: 多元建模——将纯数学理论转化为'优选法'(0.618法)和'统筹法'，实现从理论到应用的工程化", "Step 3: 战略预判——预见中国数学学科发展方向，布局多复变函数论、代数等多领域", "Step 4: 人才培养——培养陈景润等大批数学人才，建立中国数学学派"],
    "steps_en": ["Step 1: Self-Study Foundation -- Hua Luogeng used 'Independent Self-Study Method' (M9) starting from middle school math textbooks, self-studying through high school and university calculus", "Step 2: Multi-Model Engineering -- Translated pure math theory into 'Optimization Methods' (0.618 method) and 'Scheduling Methods', achieving theory-to-application engineering", "Step 3: Strategic Forecasting -- Anticipated China's mathematics discipline development direction, laying out multiple complex variable theory, algebra and other fields", "Step 4: Talent Cultivation -- Mentored many mathematicians including Chen Jingrun, establishing the Chinese mathematics school"]
}

zh['H-HLG-001'] = hhlg_zh

with open('/opt/data/workspace/Protreptic/scenarios_zh.json', 'w') as f:
    json.dump(zh, f, ensure_ascii=False, indent=2)

print('scenarios_zh.json updated with H-HLG-001')
print(f'Total entries: {len(zh)}')

# Now fix scenarios_en.json with complete H-HLG-001
with open('/opt/data/workspace/Protreptic/scenarios_en.json', 'r') as f:
    en = json.load(f)

hhlg_en = {
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
    "steps_zh": ["Step 1: 自学奠基——华罗庚用'独立自主法'(M9)从初中数学教材起步，通过自学攻克高中、大学微积分", "Step 2: 多元建模——将纯数学理论转化为'优选法'(0.618法)和'统筹法'，实现从理论到应用的工程化", "Step 3: 战略预判——预见中国数学学科发展方向，布局多复变函数论、代数等多领域", "Step 4: 人才培养——培养陈景润等大批数学人才，建立中国数学学派"],
    "steps_en": ["Step 1: Self-Study Foundation -- Hua Luogeng used 'Independent Self-Study Method' (M9) starting from middle school math textbooks, self-studying through high school and university calculus", "Step 2: Multi-Model Engineering -- Translated pure math theory into 'Optimization Methods' (0.618 method) and 'Scheduling Methods', achieving theory-to-application engineering", "Step 3: Strategic Forecasting -- Anticipated China's mathematics discipline development direction, laying out multiple complex variable theory, algebra and other fields", "Step 4: Talent Cultivation -- Mentored many mathematicians including Chen Jingrun, establishing the Chinese mathematics school"]
}

en['H-HLG-001'] = hhlg_en

with open('/opt/data/workspace/Protreptic/scenarios_en.json', 'w') as f:
    json.dump(en, f, ensure_ascii=False, indent=2)

print('scenarios_en.json updated with H-HLG-001')
print(f'Total entries: {len(en)}')

# Now update modes_data.json with complete H-HLG-001 entry
with open('/opt/data/workspace/Protreptic/modes_data.json', 'r') as f:
    modes_list = json.load(f)

# Find H-HLG-001 and update with full data
for i, entry in enumerate(modes_list):
    if entry.get('code') == 'H-HLG-001':
        modes_list[i] = {
            "code": "H-HLG-001",
            "name": "华罗庚",
            "core_mode": "M9 独立自主法/多元思维模型/摸石头过河/战略预判法",
            "new_mode": "",  # No new mode created (same as core) - this is standard for H-HLG-001
            "wiki_id": "",  # Placeholder - will be filled when wiki is created
            "nationality_standardized": "Chinese",
            "civilization_sphere": "Confucian Cultural Sphere/Modern Science",
            "time_period_standardized": "1910-1985 (Modern)",
            "primary_language": "Chinese",
            "gender_zh": "Male",
            "role_zh": "Mathematician / Applied Mathematician / Science Organizer"
        }

with open('/opt/data/workspace/Protreptic/modes_data.json', 'w') as f:
    json.dump(modes_list, f, ensure_ascii=False, indent=2)

print('modes_data.json updated with H-HLG-001')
print(f'Total modes: {len(modes_list)}')

# Verify all files
with open('/opt/data/workspace/Protreptic/scenarios_zh.json', 'r') as f:
    zh = json.load(f)
with open('/opt/data/workspace/Protreptic/scenarios_en.json', 'r') as f:
    en = json.load(f)
with open('/opt/data/workspace/Protreptic/modes_data.json', 'r') as f:
    modes_list = json.load(f)

print('\n=== VERIFICATION ===')
print(f'scenarios_zh H-HLG-001: name={zh.get("H-HLG-001", {}).get("name")}, core_mode={zh.get("H-HLG-001", {}).get("core_mode")}')
print(f'scenarios_en H-HLG-001: name={en.get("H-HLG-001", {}).get("name")}, core_mode={en.get("H-HLG-001", {}).get("core_mode")}')
print(f'modes_data H-HLG-001: found={any(e.get("code") == "H-HLG-001" for e in modes_list)}')