#!/usr/bin/env python3
"""
Data Merger — 自动化合并 worker 产出到主数据文件
用法: python data_merger.py <workspace_path>
"""
import json
import os
import sys
from pathlib import Path

TOOLS_DIR = Path("/opt/data/workspace/Protreptic/tools")
JSON_DIR = TOOLS_DIR / "json"

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def extract_new_modes(figure_data):
    """从人物数据提取新模式定义"""
    new_modes = {}
    modes = figure_data.get('modes', [])
    for mode_id in modes:
        mode_id = str(mode_id)
        if mode_id not in new_modes:
            # 这里只记录模式ID，实际定义需从 modes_expansion_proposal 或单独文件获取
            new_modes[mode_id] = True
    return new_modes

def merge_workspace(workspace_path):
    """合并单个 workspace 的所有 JSON 到主数据"""
    ws = Path(workspace_path)
    if not ws.exists():
        print(f"Workspace not found: {workspace_path}")
        return False
    
    # 收集所有有效 JSON
    json_files = list(ws.rglob("*.json"))
    print(f"Found {len(json_files)} JSON files in {ws.name}")
    
    # 加载主数据
    scenarios_zh = load_json(TOOLS_DIR / "scenarios_zh.json")
    scenarios_en = load_json(TOOLS_DIR / "scenarios_en.json")
    code_maps = load_json(TOOLS_DIR / "code_maps.json")
    scenario_tags = load_json(TOOLS_DIR / "scenario_tags.json")
    modes_data = load_json(TOOLS_DIR / "modes_data.json")
    
    # 验证必需字段 - 支持多种字段格式
    new_figures = 0
    new_modes_collected = set()
    for jf in json_files:
        data = load_json(jf)
        required_fields = []
        required_fields = []
        if 'code' in data:
            required_fields.append(('code', data['code']))
        elif 'id' in data:
            required_fields.append(('code', data['id']))
        else:
            print(f"  SKIP {jf.name}: missing code/id field")
            continue
            
        if 'description_zh' in data:
            required_fields.append(('description_zh', data['description_zh']))
        elif 'description' in data:
            required_fields.append(('description_zh', data['description']))
            
        if 'description_en' in data:
            required_fields.append(('description_en', data['description_en']))
        elif 'description_en' in data:
            required_fields.append(('description_en', data['description_en']))
        elif 'description' in data:
            required_fields.append(('description_en', data['description']))
            
        if 'modes' in data:
            required_fields.append(('modes', data['modes']))
        elif 'new_thinking_mode' in data:
            # 尝试从 new_thinking_mode 提取模式ID
            modes = []
            if data['new_thinking_mode']:
                # 从 "M416 Truth and Reconciliation/Rainbow Country/Moral Authority" 中提取 M416
                import re
                mode_matches = re.findall(r'M(\d+)', data['new_thinking_mode'])
                modes.extend(mode_matches)
            required_fields.append(('modes', modes))
        
        if len(required_fields) < 2:  # 需要至少 code 和 modes
            print(f"  SKIP {jf.name}: missing required fields (need code and modes)")
            continue
            
        # 提取 code
        code = None
        for field_name, field_value in required_fields:
            if field_name == 'code':
                code = field_value
                break
                
        if not code:
            print(f"  SKIP {jf.name}: cannot extract code")
            continue
            
        # 提取 modes
        modes = []
        for field_name, field_value in required_fields:
            if field_name == 'modes':
                modes = field_value
                break
                
        # 继续处理...
        scenarios_zh[code] = data
        
        # 创建 EN 条目
        en_entry = {}
        for key, value in data.items():
            if key == 'code':
                en_entry[key] = value
            elif key.endswith('_zh'):
                en_key = key.replace('_zh', '_en')
                en_entry[en_key] = data.get(en_key, value)
            elif key.endswith('_en'):
                en_entry[key] = value
            elif key in ['name', 'description', 'reason', 'steps', 'expected', 'case']:
                en_key = key + '_en'
                zh_key = key + '_zh'
                if en_key in data:
                    en_entry[key] = data[en_key]
                elif zh_key in data:
                    en_entry[key] = data[zh_key]
                else:
                    en_entry[key] = value
            else:
                en_entry[key] = value
        scenarios_en[code] = en_entry
        
        # 更新 code_maps
        code_maps['CODE_MAP'][code] = data.get('name', data.get('name_zh', code))
        code_maps['CODE_MAP_EN'][code] = data.get('name_en', data.get('name', code))
        
        # 更新 scenario_tags
        scenario_tags['tags'][code] = {
            'code': code,
            'name_zh': data.get('name', data.get('name_zh', code)),
            'name_en': data.get('name_en', ''),
            'era': data.get('time_period_standardized', ''),
            'gender': data.get('gender', 'male'),
            'ethnicity': data.get('nationality', ''),
            'domains': [],
            'core_modes': [str(m) for m in modes],
            'applications': [],
            'historical_domains': [],
            'mode_count': len(modes)
        }
        
        # 收集新模式
        for m in modes:
            new_modes_collected.add(str(m))
        
        # 复制到 tools/json/ 归档
        save_json(JSON_DIR / f"{code}.json", data)
        
        new_figures += 1
        print(f"  MERGED {code}")
    
    # 保存主数据
    save_json(TOOLS_DIR / "scenarios_zh.json", scenarios_zh)
    save_json(TOOLS_DIR / "scenarios_en.json", scenarios_en)
    save_json(TOOLS_DIR / "code_maps.json", code_maps)
    save_json(TOOLS_DIR / "scenario_tags.json", scenario_tags)
    
    print(f"\n=== Merge Summary ===")
    print(f"New figures merged: {new_figures}")
    print(f"New modes referenced: {sorted(new_modes_collected)}")
    print(f"Total scenarios: {len(scenarios_zh)}")
    
    return new_figures > 0

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python data_merger.py <workspace_path>")
        sys.exit(1)
    
    success = merge_workspace(sys.argv[1])
    sys.exit(0 if success else 1)