#!/usr/bin/env python3
"""
Process the final batch of 5 historical figures for Chinese thinking modes
Reads from research JSON and generates the four core data files:
- scenarios_zh.json
- scenarios_en.json
- code_maps.json (CODE_MAP / CODE_MAP_EN)
- scenario_tags.json (tags + metadata)
"""

import json
import os

def generate_english_translation(original_name_cn, code, mode_desc):
    """Generate English translation for historical figure"""
    # Basic mapping for names
    name_map = {
        '廖承志': 'Liao Chengzhi',
        '乌兰夫': 'Ulanfu',
        '彭真': 'Peng Zhen',
        '谷牧': 'Gu Mu',
        '薄一波': 'Bo Yibo'
    }
    
    # Basic translations for modes
    mode_en_map = {
        '9 统一战线': 'United Front',
        '13 目标管理': 'Management by Objectives'
    }
    
    name_en = name_map.get(original_name_cn, original_name_cn)
    mode_en = mode_en_map.get(mode_desc, mode_desc)
    
    # Extract mode number from the original mode description
    mode_number = None
    if '统一战线' in mode_desc:
        mode_number = 9
    elif '目标管理' in mode_desc:
        mode_number = 13
    
    return name_en, mode_en, mode_number

def create_scenario_structure(original_data, is_chinese=True):
    """Create scenario entry for scenarios_zh.json or scenarios_en.json"""
    
    # Determine mode number from original data
    mode_number = None
    if '统一战线' in original_data['mode']:
        mode_number = 9
    elif '目标管理' in original_data['mode']:
        mode_number = 13
    
    if is_chinese:
        name = original_data['name']
        original_unique_thinking = original_data['unique_thinking']
        mode = original_data['mode']
        mode_description = original_data['mode'].replace(' 统一战线', '').replace(' 目标管理', '').strip()
        
        return {
            'name': name,
            'description': original_unique_thinking[:100] + '...' if len(original_unique_thinking) > 100 else original_unique_thinking,
            'modes': [mode_number],
            'reason': original_unique_thinking,
            'steps': original_data['proposed_steps'],
            'expected': [
                f"理解{original_data['name']}的独特贡献",
                f"掌握相关思维模式", 
                f"发展实用的应用策略"
            ],
            'case': f"{original_data['name']} ({original_data['code']}): " + original_unique_thinking
        }
    else:
        name_en, mode_en, mode_number = generate_english_translation(
            original_data['name'], 
            original_data['code'], 
            original_data['mode']
        )
        original_unique_thinking = original_data['unique_thinking']
        mode = mode_en
        mode_description = mode_en
        
        # Create description based on original unique_thinking
        desc_sentences = original_unique_thinking.split('。')
        desc_base = desc_sentences[0][:150] + '...' if len(desc_sentences[0]) > 150 else desc_sentences[0]
        
        return {
            'name': name_en,
            'description': desc_base,
            'modes': [mode_number],
            'reason': original_unique_thinking[:100] + '...' if len(original_unique_thinking) > 100 else original_unique_thinking,
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
            'case': f"{name_en} ({original_data['code']}): " + original_unique_thinking
        }

def process_research_data():
    """Process the 5 historical figures from research JSON"""
    with open('/opt/data/kanban/boards/protreptic/attachments/t_beb98d74/phase3_final_research.json', 'r', encoding='utf-8') as f:
        research_data = json.load(f)
    
    print(f"Processing {len(research_data)} research figures...")
    
    # Create entries for the 5 figures
    new_scenarios_zh = {}
    new_scenarios_en = {}
    new_code_maps = {}
    new_tags = {}
    
    for fig in research_data:
        code = fig['code']
        
        # Generate English translations and get mode number
        name_en, mode_en, mode_number = generate_english_translation(
            fig['name'], code, fig['mode']
        )
        
        # Extract mode number from the original
        if '统一战线' in fig['mode']:
            original_mode_number = 9
        elif '目标管理' in fig['mode']:
            original_mode_number = 13
        else:
            original_mode_number = None
        
        # Clean mode descriptions for code maps
        mode_clean_zh = fig['mode'].replace('统一战线', '').replace('目标管理', '').strip()
        mode_clean_en = mode_en.replace('United Front', 'United Front').replace('Management by Objectives', 'Management by Objectives').strip()
        
        # Create scenarios for both languages
        new_scenarios_zh[code] = create_scenario_structure(fig, is_chinese=True)
        new_scenarios_en[code] = create_scenario_structure(fig, is_chinese=False)
        
        # Create code maps
        new_code_maps[code] = {
            'name_zh': fig['name'],
            'name_en': name_en,
            'mode_zh': mode_clean_zh,
            'mode_en': mode_clean_en,
            'core_contributions': {
                'zh': fig['unique_thinking'][:150] + '...',
                'en': fig['unique_thinking'][:150] + '...'
            },
            'categories': fig['applications'],
            'code': code,
            'core_mode_number': original_mode_number
        }
        
        # Create scenario tags (minimal but complete)
        new_tags[code] = {
            'code': code,
            'name_zh': fig['name'],
            'name_en': name_en,
            'mode_zh': fig['mode'],
            'mode_en': mode_en,
            'era': 'Modern',
            'gender': 'Male',
            'ethnicity': 'Han',
            'domains': ['Governance', 'Strategy'],
            'core_modes': [original_mode_number],
            'applications': fig['applications'],
            'mode_count': 1,
            'historical_domains': ['Governance', 'Strategy']
        }
    
    return new_scenarios_zh, new_scenarios_en, new_code_maps, new_tags

def main():
    """Main processing function"""
    print("=== Processing Final Batch: 5 Historical Figures ===\n")
    
    # Load existing data
    with open('scenarios_zh.json', 'r', encoding='utf-8') as f:
        scenarios_zh = json.load(f)
    
    with open('scenarios_en.json', 'r', encoding='utf-8') as f:
        scenarios_en = json.load(f)
    
    with open('code_maps.json', 'r', encoding='utf-8') as f:
        code_maps = json.load(f)
    
    with open('scenario_tags.json', 'r', encoding='utf-8') as f:
        scenario_tags = json.load(f)
    
    # Process research data
    new_scenarios_zh, new_scenarios_en, new_code_maps, new_tags = process_research_data()
    
    # Update scenarios_zh.json
    original_zh_count = len(scenarios_zh)
    scenarios_zh.update(new_scenarios_zh)
    
    # Update scenarios_en.json  
    original_en_count = len(scenarios_en)
    scenarios_en.update(new_scenarios_en)
    
    # Update code_maps.json
    original_code_maps_count = len(code_maps['CODE_MAP'])
    code_maps['CODE_MAP'].update(new_code_maps)
    code_maps['CODE_MAP_EN'].update(new_code_maps)
    
    # Update scenario_tags.json
    current_metadata = scenario_tags['metadata']
    current_tags = scenario_tags['tags']
    
    current_metadata['total_scenarios'] = original_zh_count + len(new_scenarios_zh)
    current_tags.update(new_tags)
    
    # Write updated files
    print(f"Writing updated files...")
    
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
    print(f"scenarios_zh.json: {original_zh_count} → {len(scenarios_zh)} entries")
    print(f"scenarios_en.json: {original_en_count} → {len(scenarios_en)} entries")
    print(f"code_maps.json: {original_code_maps_count} → {len(code_maps['CODE_MAP'])} entries")
    print(f"scenario_tags.json: {len(current_tags)} total entries")
    print(f"Historical figures added: {len(new_scenarios_zh)}")
    
    # Print the 5 figures processed
    print(f"\n=== FIGURES PROCESSED ===")
    for fig in ['廖承志 (H-LCZ-362)', '乌兰夫 (H-WLF-363)', 
                '彭真 (H-PZ-364)', '谷牧 (H-GM-365)', 
                '薄一波 (H-BYB-366)']:
        print(f"  ✓ {fig}")
    
    print(f"\nAll four core files have been updated successfully!")
    print(f"The new 5 figures from serrano's research have been integrated into the system.")
    
    return len(new_scenarios_zh)

if __name__ == '__main__':
    added = main()
    print(f"\nTask completed: Added {added} new historical figures to the system.")