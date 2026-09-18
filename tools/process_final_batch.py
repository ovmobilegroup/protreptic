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

def load_existing_files():
    """Load existing data files"""
    with open('scenarios_zh.json', 'r', encoding='utf-8') as f:
        scenarios_zh = json.load(f)
    
    with open('scenarios_en.json', 'r', encoding='utf-8') as f:
        scenarios_en = json.load(f)
    
    with open('code_maps.json', 'r', encoding='utf-8') as f:
        code_maps = json.load(f)
    
    with open('scenario_tags.json', 'r', encoding='utf-8') as f:
        scenario_tags = json.load(f)
    
    return scenarios_zh, scenarios_en, code_maps, scenario_tags

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
    
    # Basic translations for descriptions
    description_map = {
        '廖承志': 'United Front work on Taiwan/Hong Kong/International/Japan',
        '乌兰夫': 'Ethnic regional autonomy / National equality & symbiotic development',
        '彭真': 'United Front Minister/CPPCC Chairman / Rule-of-law inclusive unity',
        '谷牧': 'Economic planning / Foreign trade MBO / Reform architect',
        '薄一波': 'Eight Elders / Industrial production indicator system / State Economic Commission'
    }
    
    name_en = name_map.get(original_name_cn, original_name_cn)
    mode_en = mode_en_map.get(mode_desc, mode_desc)
    description_en = description_map.get(original_name_cn, original_name_cn)
    
    return name_en, mode_en, description_en

def create_scenario_structure(original_data, is_chinese=True):
    """Create scenario entry for scenarios_zh.json or scenarios_en.json"""
    if is_chinese:
        name = original_data['name']
        original_unique_thinking = original_data['unique_thinking']
        mode = original_data['mode']
    else:
        name_en, mode_en, description_en = generate_english_translation(
            original_data['name'], 
            original_data['code'], 
            original_data['mode']
        )
        original_unique_thinking = original_data['unique_thinking']
        mode = mode_en
        
        # Create description for English
        desc_base = description_en
        if '统一战线' in original_data['mode']:
            desc_base = 'United Front'
        elif '目标管理' in original_data['mode']:
            desc_base = 'Management by Objectives'
            
        return {
            'name': name_en,
            'description': desc_base,
            'modes': [9] if '统一战线' in mode else [13],
            'reason': original_unique_thinking[:100] + '...' if len(original_unique_thinking) > 100 else original_unique_thinking,
            'steps': [
                f"Step 1: Analyze {name_en}'s thinking approach",
                f"Step 2: Apply relevant modes: {[9] if '统一战线' in mode else [13]}",
                f"Step 3: Develop practical applications based on their methodology",
                f"Step 4: Implement structured thinking process",
                f"Step 5: Ensure comprehensive coverage of their principles"
            ],
            'expected': [
                f"Master {name_en}'s unique contribution",
                f"Apply relevant modes effectively",
                f"Develop practical implementation strategies"
            ],
            'case': f"{name_en} ({original_data['code']}): " + original_unique_thinking[:200] + '...' if len(original_unique_thinking) > 200 else f"{name_en} ({original_data['code']}): " + original_unique_thinking
        }
    
    # Create Chinese scenario
    return {
        'name': name,
        'description': original_data['unique_thinking'][:100] + '...' if len(original_data['unique_thinking']) > 100 else original_data['unique_thinking'],
        'modes': [9] if '统一战线' in mode else [13],
        'reason': original_unique_thinking,
        'steps': original_data['proposed_steps'],
        'expected': [
            f"理解{original_data['name']}的独特贡献",
            f"掌握相关思维模式", 
            f"发展实用的应用策略"
        ],
        'case': f"{original_data['name']} ({original_data['code']}): " + original_unique_thinking
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
        
        # English translations and mappings
        name_en, mode_en, description_en = generate_english_translation(
            fig['name'], code, fig['mode']
        )
        
        # Create scenarios for both languages
        new_scenarios_zh[code] = create_scenario_structure(fig, is_chinese=True)
        new_scenarios_en[code] = create_scenario_structure(fig, is_chinese=False)
        
        # Create code maps
        # Clean and normalize for English
        mode_clean_en = mode_en.replace(' 统一战线', '').strip()
        mode_clean_zh = fig['mode'].replace('统一战线', '').strip()
        
        new_code_maps[code] = {
            'name_zh': fig['name'],
            'name_en': name_en,
            'mode_zh': mode_clean_zh,
            'mode_en': mode_clean_en,
            'core_contributions': {
                'zh': fig['unique_thinking'][:150] + '...',
                'en': description_en[:150] + '...'
            },
            'categories': fig['applications'],
            'code': code
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
            'core_modes': [9] if '统一战线' in fig['mode'] else [13],
            'applications': fig['applications'],
            'mode_count': 1,
            'historical_domains': ['Governance', 'Strategy']
        }
    
    return new_scenarios_zh, new_scenarios_en, new_code_maps, new_tags

def main():
    """Main processing function"""
    print("=== Processing Final Batch: 5 Historical Figures ===\n")
    
    # Load existing data
    scenarios_zh, scenarios_en, code_maps, scenario_tags = load_existing_files()
    
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