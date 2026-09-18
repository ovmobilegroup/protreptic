#!/usr/bin/env python3
"""
写入Batch 3历史人物数据 (H-352到H-361)
根据batch3_candidates.json生成4个JSON文件
"""
import json
from pathlib import Path

def load_json(filename):
    path = Path(__file__).parent / filename
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(filename, data):
    path = Path(__file__).parent / filename
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_historical_prefix(code):
    """获取历史人物代码的前缀"""
    if code.startswith('H-'):
        return code[:3]
    return code[:2]

def convert_to_english_imperative(text):
    """简易英文imperative转换（基于已有文本的简单翻译）"""
    if not text:
        return ""
    
    # 一些常见的转换规则
    translations = {
        "的": ": ",
        "-": "-",
        "。": ".",
        "，": ", ",
        "建立": "establish",
        "制定": "formulate",
        "进行": "conduct",
        "加强": "strengthen",
        "推动": "promote",
        "实现": "realize",
        "完成": "complete",
        "完善": "improve",
        "构建": "build",
        "形成": "form",
        "建立": "establish",
        "发展": "develop",
        "成长": "grow",
        "提升": "enhance",
        "增加": "increase",
        "减少": "reduce",
        "控制": "control",
        "管理": "manage",
        "协调": "coordinate",
        "合作": "cooperate",
        "统一": "unify",
        "设计": "design",
        "规划": "plan",
        "组织": "organize",
        "领导": "lead",
        "决策": "decide",
        "战略": "strategic",
        " tactics ": " tactics ",
        "、": ", ",
    }
    
    result = text
    for cn, en in translations.items():
        result = result.replace(cn, en)
    
    # 确保英文首字母大写
    if result:
        result = result.strip()
        if result:
            result = result[0].upper() + result[1:]
    
    return result

def main():
    # 加载现有数据
    scenarios_zh = load_json('scenarios_zh.json')
    scenarios_en = load_json('scenarios_en.json')
    code_maps = load_json('code_maps.json')
    scenario_tags = load_json('scenario_tags.json')
    
    # 加载Batch 3候选数据
    batch3_data = load_json('batch3_candidates.json')
    
    print(f"开始写入Batch 3历史人物数据 (共{len(batch3_data)}位)...")
    
    # 处理每一位历史人物
    for figure in batch3_data:
        code = figure['code']
        name_zh = figure['name_zh']
        name_en = figure['name_en']
        era = figure['era']
        domains = figure['domains']
        core_modes = figure['core_modes']
        
        print(f"  处理 {code}: {name_zh}")
        
        # 1. 写入 scenarios_zh.json
        scenario_zh = {
            "name": f"{name_zh}: {figure['unique_thinking']}",
            "description": figure.get('unique_thinking', f"{name_zh}的相关思维模式应用。"),
            "modes": core_modes,
            "reason": f"{name_zh}的关键思维模式：{', '.join([str(m) for m in core_modes])}。这代表着{get_historical_prefix(code)}-{code[-3:]}{figure.get('era_type', '现代')}的历史人物思维特色。",
            "steps": figure.get('proposed_steps', [
                f"第1步：应用核心思维模式{core_modes[0]}进行分析",
                f"第2步：结合历史人物经验{code}进行实践", 
                f"第3步：制度化{code}的经验成果"
            ]),
            "expected": figure.get('applications', [
                f"提升{name_zh}的思维水平",
                f"完善{code}的相关理论体系",
                f"推广{code}的成功经验"
            ]),
            "case": figure.get('historical_example', f"以{name_zh}为代表的{get_historical_prefix(code)}-{code[-3:]}历史人物在{era}时期的思维特点和实践经验。"),
            "era": era,
            "historical_domains": figure['historical_domains'],
            "domains": domains,
            "code": code,
            "name_zh": name_zh,
            "name_en": name_en
        }
        scenarios_zh[code] = scenario_zh
        
        # 2. 写入 scenarios_en.json - 英文imperative
        scenario_en = {
            "name": f"{name_en}: {figure['unique_thinking']}",
            "description": convert_to_english_imperative(figure.get('unique_thinking', f"{name_zh}思维模式应用。")),
            "modes": core_modes,
            "reason": convert_to_english_imperative(f"{name_zh}的关键思维模式：{', '.join([str(m) for m in core_modes])}。这代表着{get_historical_prefix(code)}-{code[-3:]}{figure.get('era_type', 'Modern')} historical figure thinking features。"),
            "steps": [convert_to_english_imperative(step) for step in figure.get('proposed_steps', [
                f"Step 1: Apply core thinking mode {core_modes[0]} for analysis",
                f"Step 2: Combine with historical figure experience of {code}",
                f"Step 3: Systematize the experience of {code}"
            ])],
            "expected": [convert_to_english_imperative(exp) for exp in figure.get('applications', [
                f"Enhance {name_zh}'s thinking level",
                f"Improve {code}'s theoretical system", 
                f"Promote {code}'s successful experience"
            ])],
            "case": convert_to_english_imperative(figure.get('historical_example', f"The thinking characteristics and practical experience of {name_zh} representative of {get_historical_prefix(code)}-{code[-3:]} historical figure in {era} period.")),
            "era": era,
            "historical_domains": figure['historical_domains'],
            "domains": domains,
            "code": code,
            "name_zh": name_zh,
            "name_en": name_en
        }
        scenarios_en[code] = scenario_en
        
        # 3. 写入 code_maps.json
        code_map_zh = f"{code}: {figure['name_zh']}"
        code_map_en = f"{code}: {figure['name_en']}"
        
        if 'CODE_MAP' not in code_maps:
            code_maps['CODE_MAP'] = {}
        if 'CODE_MAP_EN' not in code_maps:
            code_maps['CODE_MAP_EN'] = {}
            
        code_maps['CODE_MAP'][code] = code_map_zh
        code_maps['CODE_MAP_EN'][code] = code_map_en
        
        # 4. 写入 scenario_tags.json
        if code not in scenario_tags:
            scenario_tags[code] = {
                "code": code,
                "name_zh": name_zh,
                "name_en": name_en,
                "era": era,
                "domains": domains,
                "core_modes": core_modes,
                "applications": figure.get('applications', []),
                "mode_count": len(core_modes)
            }
        
        scenario_tags[code]["name_zh"] = name_zh
        scenario_tags[code]["name_en"] = name_en
        scenario_tags[code]["era"] = era
        scenario_tags[code]["domains"] = domains
        scenario_tags[code]["core_modes"] = core_modes
        
        print(f"    ✓ 已写入 {code}")
    
    # 保存所有文件
    save_json('scenarios_zh.json', scenarios_zh)
    save_json('scenarios_en.json', scenarios_en)
    save_json('code_maps.json', code_maps)
    save_json('scenario_tags.json', scenario_tags)
    
    print(f"\n✓ Batch 3数据写入完成！")
    print(f"  scenarios_zh.json: {len(scenarios_zh)} 条记录")
    print(f"  scenarios_en.json: {len(scenarios_en)} 条记录")
    print(f"  code_maps.json: {len(code_maps.get('CODE_MAP', {}))} 条映射")
    print(f"  scenario_tags.json: {len(scenario_tags)} 条标签")
    
    # 验证数据
    print("\n验证数据一致性...")
    
    # 检查中英文对应
    for code in scenarios_zh:
        if code in scenarios_en:
            zh_entry = scenarios_zh[code]
            en_entry = scenarios_en[code]
            if zh_entry['modes'] == en_entry['modes']:
                print(f"  ✓ {code} - 中英文模式一致")
            else:
                print(f"  ✗ {code} - 中英文模式不一致")
        else:
            print(f"  ✗ {code} - 缺少英文版本")
    
    print("\nBatch 3写入完成！")

if __name__ == '__main__':
    main()