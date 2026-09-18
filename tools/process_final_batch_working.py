#!/usr/bin/env python3
"""
Process final batch: 5 historical figures from serrano research
Clean, working version that ensures mode consistency between ZH and EN
"""

import json

def get_english_translation(chinese_name, mode_desc):
    """Generate English translation for historical figure"""
    # Basic name mapping
    name_map = {
        '廖承志': 'Liao Chengzhi',
        '乌兰夫': 'Ulanfu',
        '彭真': 'Peng Zhen',
        '谷牧': 'Gu Mu',
        '薄一波': 'Bo Yibo'
    }
    
    # English mode descriptions
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
    mode_en = mode_en_map.get(mode_desc, mode_desc)
    description_en = description_map.get(chinese_name, chinese_name)
    
    return name_en, mode_en, description_en

def main():
    print("=== Processing Final Batch: 5 Historical Figures ===\n")
    
    # Load research data
    with open('/opt/data/kanban/boards/protreptic/attachments/t_beb98d74/phase3_final_research.json', 'r', encoding='utf-8') as f:
        research_data = json.load(f)
    
    print(f"Loaded {len(research_data)} research figures")
    
    # Load existing data files
    with open('scenarios_zh.json', 'r', encoding='utf-8') as f:
        scenarios_zh = json.load(f)
    
    with open('scenarios_en.json', 'r', encoding='utf-8') as f:
        scenarios_en = json.load(f)
    
    with open('code_maps.json', 'r', encoding='utf-8') as f:
        code_maps = json.load(f)
    
    with open('scenario_tags.json', 'r', encoding='utf-8') as f:
        scenario_tags = json.load(f)
    
    print(f"Current counts - ZH: {len(scenarios_zh)}, EN: {len(scenarios_en)}, Code Maps: {len(code_maps['CODE_MAP'])}")
    
    # Process each historical figure
    added_count = 0
    for fig in research_data:
        code = fig['code']
        chinese_name = fig['name']
        mode_zh = fig['mode']
        
        # Get English translations
        english_name, english_mode, english_description = get_english_translation(chinese_name, mode_zh)
        
        # Determine mode number (9 or 13) for consistency
        mode_number = 9 if '统一战线' in mode_zh else 13
        
        # Clean mode descriptions
        mode_clean_zh = mode_zh.replace(' 统一战线', '').replace(' 目标管理', '').strip()
        mode_clean_en = english_mode.replace('United Front', 'United Front').replace('Management by Objectives', 'Management by Objectives').strip()
        
        # Add to scenarios_zh.json
        scenarios_zh[code] = {
            'name': chinese_name,
            'description': fig['unique_thinking'][:100] + '...',
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
        
        # Add to scenarios_en.json  
        scenarios_en[code] = {
            'name': english_name,
            'description': english_description,
            'modes': [mode_number],  # Same mode number for consistency!
            'reason': fig['unique_thinking'][:100] + '...',
            'steps': [
                f"Step 1: Analyze {english_name}'s thinking approach",
                f"Step 2: Apply relevant modes: {[mode_number]}",
                f"Step 3: Develop practical applications based on their methodology",
                f"Step 4: Implement structured thinking process",
                f"Step 5: Ensure comprehensive coverage of their principles"
            ],
            'expected': [
                f"Master {english_name}'s unique contribution",
                f"Apply relevant modes effectively",
                f"Develop practical implementation strategies"
            ],
            'case': f"{english_name} ({code}): " + fig['unique_thinking']
        }
        
        # Add to code_maps.json
        code_maps[code] = {
            'name_zh': chinese_name,
            'name_en': english_name,
            'mode_zh': mode_clean_zh,
            'mode_en': mode_clean_en,
            'core_contributions': {
                'zh': fig['unique_thinking'][:150] + '...',
                'en': english_description[:150] + '...'
            },
            'categories': fig['applications'],
            'code': code,
            'core_mode_number': mode_number
        }
        
        # Add to scenario_tags.json
        scenario_tags[code] = {
            'code': code,
            'name_zh': chinese_name,
            'name_en': english_name,
            'mode_zh': mode_zh,
            'mode_en': english_mode,
            'era': 'Modern',
            'gender': 'Male',
            'ethnicity': 'Han',
            'domains': ['Governance', 'Strategy'],
            'core_modes': [mode_number],
            'applications': fig['applications'],
            'mode_count': 1,
            'historical_domains': ['Governance', 'Strategy']
        }
        
        added_count += 1
        print(f"✓ Added: {chinese_name} ({code})")
    
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
    print(f"✓ Added {added_count} historical figures to the system")
    print(f"✓ scenarios_zh.json: {len(scenarios_zh)} entries")
    print(f"✓ scenarios_en.json: {len(scenarios_en)} entries")
    print(f"✓ code_maps.json: {len(code_maps['CODE_MAP'])} entries")
    print(f"✓ scenario_tags.json: {len(scenario_tags)} entries")
    
    print(f"\n=== FIGURES PROCESSED ===")
    for fig in research_data:
        print(f"  ✓ {fig['name']} ({fig['code']})")
    
    print(f"\n🎉 All four core files updated successfully!")
    print(f"The 5 research figures from serrano have been integrated into Protreptic.")
    
    return added_count

if __name__ == '__main__':
    added = main()
    print(f"\n✅ Task completed: Added {added} new historical figures!")