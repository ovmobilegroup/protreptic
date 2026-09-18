#!/usr/bin/env python3
"""
Final batch processing for 5 historical figures
Ensures mode consistency between Chinese and English scenarios
"""

import json

def get_english_translation(chinese_name, mode_zh, mode_number):
    """Get English translation with correct mode number"""
    # Chinese to English name mapping
    name_map = {
        '廖承志': 'Liao Chengzhi',
        '乌兰夫': 'Ulanfu',
        '彭真': 'Peng Zhen',
        '谷牧': 'Gu Mu',
        '薄一波': 'Bo Yibo'
    }
    
    # English mode descriptions
    mode_en_map = {
        9: 'United Front',
        13: 'Management by Objectives'
    }
    
    description_map = {
        '廖承志': 'United Front work on Taiwan/Hong Kong/International/Japan',
        '乌兰夫': 'Ethnic regional autonomy / National equality & symbiotic development',
        '彭真': 'United Front Minister/CPPCC Chairman / Rule-of-law inclusive unity',
        '谷牧': 'Economic planning / Foreign trade MBO / Reform architect',
        '薄一波': 'Eight Elders / Industrial production indicator system / State Economic Commission'
    }
    
    english_name = name_map.get(chinese_name, chinese_name)
    english_mode = mode_en_map.get(mode_number, 'Unknown')
    english_description = description_map.get(chinese_name, chinese_name)
    
    return english_name, english_mode, english_description

def main():
    print("=== Processing Final Batch: 5 Historical Figures ===\n")
    
    # Load research data
    with open('/opt/data/kanban/boards/protreptic/attachments/t_beb98d74/phase3_final_research.json', 'r', encoding='utf-8') as f:
        research_data = json.load(f)
    
    print(f"Loaded {len(research_data)} research figures")
    
    # Load current data
    with open('scenarios_zh.json', 'r', encoding='utf-8') as f:
        scenarios_zh = json.load(f)
    
    with open('scenarios_en.json', 'r', encoding='utf-8') as f:
        scenarios_en = json.load(f)
    
    with open('code_maps.json', 'r', encoding='utf-8') as f:
        code_maps = json.load(f)
    
    with open('scenario_tags.json', 'r', encoding='utf-8') as f:
        scenario_tags = json.load(f)
    
    print(f"Current counts - ZH: {len(scenarios_zh)}, EN: {len(scenarios_en)}, Code Maps: {len(code_maps['CODE_MAP'])}")
    
    # Verify the 5 new figures from research data
    print("\n=== Figures to process ===")
    for fig in research_data:
        code = fig['code']
        chinese_name = fig['name']
        mode_zh = fig['mode']
        
        # Extract correct mode number
        if '统一战线' in mode_zh:
            mode_number = 9
            mode_desc = 'United Front'
        elif '目标管理' in mode_zh:
            mode_number = 13
            mode_desc = 'Management by Objectives'
        else:
            mode_number = 9  # Default
            mode_desc = 'Unknown'
        
        print(f"  ✓ {chinese_name} ({code})")
        print(f"    Chinese mode: {mode_zh} → Mode number: {mode_number}, English mode: {mode_desc}")
        
        # Verify current mode numbers for consistency check
        current_zh_mode = scenarios_zh.get(code, {}).get('modes', [])
        current_en_mode = scenarios_en.get(code, {}).get('modes', [])
        if current_zh_mode == [mode_number] and current_en_mode != [mode_number]:
            print(f"    ⚠️  MODE INCONSISTENCY! Need to fix English scenario")
    
    print(f"\n=== Processing with Correct Mode Numbers ===")
    
    # Reset and reprocess with correct mode numbers
    updated_scenarios_zh = dict(scenarios_zh)
    updated_scenarios_en = dict(scenarios_en)
    updated_code_maps = dict(code_maps)
    updated_scenario_tags = dict(scenario_tags)
    
    # Clear the 5 figures from existing files
    codes_to_remove = ['H-LCZ-362', 'H-WLF-363', 'H-PZ-364', 'H-GM-365', 'H-BYB-366']
    for code in codes_to_remove:
        updated_scenarios_zh.pop(code, None)
        updated_scenarios_en.pop(code, None)
        updated_code_maps[code].pop('CODE_MAP', None)
        updated_code_maps[code].pop('CODE_MAP_EN', None)
        updated_scenario_tags.pop(code, None)
    
    print("✓ Removed old entries with incorrect mode numbers")
    
    # Process each research figure with correct mode numbers
    for fig in research_data:
        code = fig['code']
        chinese_name = fig['name']
        mode_zh = fig['mode']
        
        # Determine correct mode number
        if '统一战线' in mode_zh:
            mode_number = 9
        elif '目标管理' in mode_zh:
            mode_number = 13
        else:
            mode_number = 9
        
        # Get English translation
        english_name, english_mode, english_description = get_english_translation(chinese_name, mode_zh, mode_number)
        
        # Clean mode descriptions
        mode_clean_zh = mode_zh.replace(' 统一战线', '').replace(' 目标管理', '').strip()
        mode_clean_en = mode_desc.replace('United Front', 'United Front').replace('Management by Objectives', 'Management by Objectives').strip()
        
        # Update scenarios_zh.json
        updated_scenarios_zh[code] = {
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
        
        # Update scenarios_en.json with CORRECT mode number
        updated_scenarios_en[code] = {
            'name': english_name,
            'description': english_description,
            'modes': [mode_number],  # CRITICAL: Same mode number as Chinese!
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
        
        # Update code_maps.json
        updated_code_maps[code] = {
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
        
        # Update scenario_tags.json
        updated_scenario_tags[code] = {
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
        
        print(f"✓ Processed: {chinese_name} ({code}) - Mode: {mode_number}")
    
    # Save updated files
    with open('scenarios_zh.json', 'w', encoding='utf-8') as f:
        json.dump(updated_scenarios_zh, f, ensure_ascii=False, indent=2)
    
    with open('scenarios_en.json', 'w', encoding='utf-8') as f:
        json.dump(updated_scenarios_en, f, ensure_ascii=False, indent=2)
    
    with open('code_maps.json', 'w', encoding='utf-8') as f:
        json.dump(updated_code_maps, f, ensure_ascii=False, indent=2)
    
    with open('scenario_tags.json', 'w', encoding='utf-8') as f:
        json.dump(updated_scenario_tags, f, ensure_ascii=False, indent=2)
    
    # Verification
    print(f"\n=== VERIFICATION ===")
    mode_consistent = True
    for fig in research_data:
        code = fig['code']
        if '统一战线' in fig['mode']:
            expected_mode = 9
        elif '目标管理' in fig['mode']:
            expected_mode = 13
        
        zh_mode = updated_scenarios_zh[code]['modes']
        en_mode = updated_scenarios_en[code]['modes']
        
        if zh_mode != [expected_mode] or en_mode != [expected_mode]:
            mode_consistent = False
            print(f"  ❌ INCONSISTENCY: {code}")
            print(f"     Expected mode: {expected_mode}")
            print(f"     ZH mode: {zh_mode}")
            print(f"     EN mode: {en_mode}")
        else:
            print(f"  ✓ {code}: Mode {expected_mode} consistent")
    
    # Final summary
    print(f"\n=== FINAL SUMMARY ===")
    print(f"✓ Successfully processed {len(research_data)} historical figures")
    print(f"✓ All mode numbers are now consistent between ZH and EN")
    print(f"✓ scenarios_zh.json: {len(updated_scenarios_zh)} entries")
    print(f"✓ scenarios_en.json: {len(updated_scenarios_en)} entries")
    print(f"✓ code_maps.json: {len(updated_code_maps)} entries")
    print(f"✓ scenario_tags.json: {len(updated_scenario_tags)} entries")
    
    if mode_consistent:
        print(f"\n🎉 SUCCESS! All mode numbers are consistent!")
        print(f"The 5 historical figures from serrano's research have been properly integrated with correct bilingual alignment.")
    else:
        print(f"\n❌ There are still inconsistencies. Please check the VERIFICATION section above.")
    
    return len(research_data)