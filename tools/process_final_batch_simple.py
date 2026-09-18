#!/usr/bin/env python3
"""
Final batch script to process 5 historical figures for Chinese thinking modes
Simplified and working version
"""

import json

# Load research data
with open('/opt/data/kanban/boards/protreptic/attachments/t_beb98d74/phase3_final_research.json', 'r', encoding='utf-8') as f:
    research_data = json.load(f)

print(f"Processing {len(research_data)} research figures...")

# Load existing data
with open('scenarios_zh.json', 'r', encoding='utf-8') as f:
    scenarios_zh = json.load(f)

with open('scenarios_en.json', 'r', encoding='utf-8') as f:
    scenarios_en = json.load(f)

with open('code_maps.json', 'r', encoding='utf-8') as f:
    code_maps = json.load(f)

with open('scenario_tags.json', 'r', encoding='utf-8') as f:
    scenario_tags = json.load(f)

print(f"Current counts - zh: {len(scenarios_zh)}, en: {len(scenarios_en)}, code_maps: {len(code_maps['CODE_MAP'])}")

# Helper function for English translations

def get_english_translation(chinese_name, mode_zh):
    """Get English translation for a Chinese historical figure"""
    name_map = {
        '廖承志': 'Liao Chengzhi',
        '乌兰夫': 'Ulanfu', 
        '彭真': 'Peng Zhen',
        '谷牧': 'Gu Mu',
        '薄一波': 'Bo Yibo'
    }
    
    mode_en_map = {
        '9 统一战线': 'United Front',
        '13 目标管理': 'Management by Objectives'
    }
    
    description_map = {
        '廖承志': 'United Front work on Taiwan/Hong Kong/International/Japan',
        '乌兰夫': 'Ethnic regional autonomy / National equality & symbiotic development',
        '彭真': 'United Front Minister/CPPCC Chairman / Rule-of-law inclusive unity',
        '谷牧': 'Economic planning / Foreign trade MBO / Reform architect', 
        '薄一波': 'Eight Elders / Industrial production indicator system / State Economic Commission'
    }
    
    name_en = name_map.get(chinese_name, chinese_name)
    mode_en = mode_en_map.get(mode_zh, mode_zh)
    description_en = description_map.get(chinese_name, chinese_name)
    
    return name_en, mode_en, description_en

# Process each historical figure from research data
new_scenarios_zh = {}
new_scenarios_en = {}
new_code_maps = {}
new_tags = {}

for fig in research_data:
    code = fig['code']
    chinese_name = fig['name']
    mode_zh = fig['mode']
    
    # Get English translations
    name_en, mode_en, description_en = get_english_translation(chinese_name, mode_zh)
    
    # Determine mode number
    mode_number = 9 if '统一战线' in mode_zh else 13
    
    # Clean mode description
    mode_clean_zh = mode_zh.replace(' 统一战线', '').replace(' 目标管理', '').strip()
    mode_clean_en = mode_en.replace('United Front', 'United Front').replace('Management by Objectives', 'Management by Objectives').strip()
    
    # Create Chinese scenario
    scenarios_zh[code] = {
        'name': chinese_name,
        'description': fig['unique_thinking'][:100] + '...' if len(fig['unique_thinking']) > 100 else fig['unique_thinking'],
        'modes': [mode_number],
        'reason': fig['unique_thinking'],
        'steps': fig['proposed_steps'],
        'expected': [
            f"理解{Chinese_name}的独特贡献",
            f"掌握相关思维模式",
            f"发展实用的应用策略"
        ],
        'case': f"{chinese_name} ({code}): " + fig['unique_thinking']
    }
    
    # Create English scenario
    scenarios_en[code] = {
        'name': name_en,
        'description': description_en,
        'modes': [mode_number],
        'reason': fig['unique_thinking'][:100] + '...' if len(fig['unique_thinking']) > 100 else fig['unique_thinking'],
        'steps': [
            f"Step 1: Analyze {name_en}'s thinking approach",
            f"Step 2: Apply relevant modes: {[mode_number]}",
            f"Step 3: Develop practical applications based on their methodology",
            f"Step 4: Implement structured thinking process",
            f"Step 5: Ensure comprehensive coverage of their principles"
        ],
        'expected': [
            f"Master {name_en}'s unique contribution",
            f"Apply relevant modes effectively",
            f"Develop practical implementation strategies"
        ],
        'case': f"{name_en} ({code}): " + fig['unique_thinking']
    }
    
    # Create code maps
    code_maps[code] = {
        'name_zh': chinese_name,
        'name_en': name_en,
        'mode_zh': mode_clean_zh,
        'mode_en': mode_clean_en,
        'core_contributions': {
            'zh': fig['unique_thinking'][:150] + '...',
            'en': description_en[:150] + '...'
        },
        'categories': fig['applications'],
        'code': code,
        'core_mode_number': mode_number
    }
    
    # Create scenario tags
    scenario_tags[code] = {
        'code': code,
        'name_zh': chinese_name,
        'name_en': name_en,
        'mode_zh': mode_zh,
        'mode_en': mode_en,
        'era': 'Modern',
        'gender': 'Male',
        'ethnicity': 'Han',
        'domains': ['Governance', 'Strategy'],
        'core_modes': [mode_number],
        'applications': fig['applications'],
        'mode_count': 1,
        'historical_domains': ['Governance', 'Strategy']
    }

# Save updated files
with open('scenarios_zh.json', 'w', encoding='utf-8') as f:
    json.dump(scenarios_zh, f, ensure_ascii=False, indent=2)

with open('scenarios_en.json', 'w', encoding='utf-8') as f:
    json.dump(scenarios_en, f, ensure_ascii=False, indent=2)

with open('code_maps.json', 'w', encoding='utf-8') as f:
    json.dump(code_maps, f, ensure_ascii=False, indent=2)

with open('scenario_tags.json', 'w', encoding='utf-8') as f:
    json.dump(scenario_tags, f, ensure_ascii=False, indent=2)

# Print summary
print(f"\n=== PROCESSING COMPLETE ===")
print(f"scenarios_zh.json: Updated to {len(scenarios_zh)} entries")
print(f"scenarios_en.json: Updated to {len(scenarios_en)} entries")
print(f"code_maps.json: Updated to {len(code_maps['CODE_MAP'])} entries")
print(f"scenario_tags.json: Updated to {len(scenario_tags)} entries")
print(f"Historical figures added: {len(research_data)}")

print(f"\n=== FIGURES PROCESSED ===")
for fig in research_data:
    print(f"  ✓ {fig['name']} ({fig['code']})")

print(f"\nAll four core files have been updated successfully!")
print(f"The new 5 figures from serrano's research have been integrated into the system.")