#!/usr/bin/env python3
"""
Data Verifier for Protreptic Main Data Files
验证主数据文件的完整性和正确性

Usage: python verify_main_data.py
"""

import json
import sys
import os
from pathlib import Path
from collections import Counter


def verify_main_data(tools_dir: str) -> dict:
    """验证主数据文件的完整性"""
    tools = Path(tools_dir)
    
    results = {
        "duplicate_codes": [],
        "parse_errors": [],
        "format_errors": [],
        "integrity_issues": [],
        "missing_scenarios_tags": [],
        "cross_file_consistency": [],
        "summary": {}
    }
    
    # 主数据文件路径
    main_files = {
        "scenarios_zh": tools / "scenarios_zh.json",
        "scenarios_en": tools / "scenarios_en.json", 
        "code_maps": tools / "code_maps.json",
        "scenario_tags": tools / "scenario_tags.json",
        "modes_data": tools / "modes_data.json",
    }
    
    # 1. 加载并验证各文件
    scenarios_zh = {}
    scenarios_en = {}
    code_maps = {}
    scenario_tags = {}
    modes_data = {}
    
    for name, path in main_files.items():
        if not path.exists():
            results["format_errors"].append(f"主文件缺失: {name} ({path})")
            continue
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if name == "scenarios_zh":
                scenarios_zh = data
            elif name == "scenarios_en":
                scenarios_en = data
            elif name == "code_maps":
                code_maps = data
            elif name == "scenario_tags":
                scenario_tags = data
            elif name == "modes_data":
                modes_data = data
                
        except json.JSONDecodeError as e:
            results["parse_errors"].append(f"{name}: {str(e)}")
        except Exception as e:
            results["format_errors"].append(f"{name}: {str(e)}")
    
    # 2. 检查 scenarios_zh 和 scenarios_en 结构一致性
    if scenarios_zh and scenarios_en:
        zh_keys = set(scenarios_zh.keys())
        en_keys = set(scenarios_en.keys())
        
        if zh_keys != en_keys:
            missing_in_en = zh_keys - en_keys
            missing_in_zh = en_keys - zh_keys
            if missing_in_en:
                results["cross_file_consistency"].append(f"scenarios_en 缺失 {len(missing_in_en)} 个键: {list(missing_in_en)[:5]}")
            if missing_in_zh:
                results["cross_file_consistency"].append(f"scenarios_zh 缺失 {len(missing_in_zh)} 个键: {list(missing_in_zh)[:5]}")
        
        # 检查每个条目的字段完整性
        required_scenario_fields = ['name', 'description', 'modes', 'reason', 'steps', 'expected', 'case']
        for code, entry in scenarios_zh.items():
            for field in required_scenario_fields:
                if field not in entry:
                    results["integrity_issues"].append(f"scenarios_zh[{code}] 缺少字段: {field}")
            if not isinstance(entry.get('modes'), list) or len(entry['modes']) < 3:
                results["integrity_issues"].append(f"scenarios_zh[{code}] modes 无效或少于3个")
        
        for code, entry in scenarios_en.items():
            for field in required_scenario_fields:
                if field not in entry:
                    results["integrity_issues"].append(f"scenarios_en[{code}] 缺少字段: {field}")
            if not isinstance(entry.get('modes'), list) or len(entry['modes']) < 3:
                results["integrity_issues"].append(f"scenarios_en[{code}] modes 无效或少于3个")
    
    # 3. 检查 code_maps 完整性
    if code_maps:
        if 'CODE_MAP' not in code_maps or 'CODE_MAP_EN' not in code_maps:
            results["format_errors"].append("code_maps 缺少 CODE_MAP 或 CODE_MAP_EN")
        else:
            cm_codes = set(code_maps['CODE_MAP'].keys())
            cm_en_codes = set(code_maps['CODE_MAP_EN'].keys())
            
            if cm_codes != cm_en_codes:
                results["cross_file_consistency"].append("CODE_MAP 和 CODE_MAP_EN 键不一致")
            
            # 检查是否覆盖所有场景
            if scenarios_zh:
                missing_in_cm = set(scenarios_zh.keys()) - cm_codes
                if missing_in_cm:
                    results["cross_file_consistency"].append(f"code_maps 缺少 {len(missing_in_cm)} 个场景映射")
    
    # 4. 检查重复 code
    if scenarios_zh:
        all_codes = list(scenarios_zh.keys())
        code_counts = Counter(all_codes)
        for code, count in code_counts.items():
            if count > 1:
                results["duplicate_codes"].append(f"{code}: 出现 {count} 次")
    
    # 4. 检查 scenario_tags 完整性
    if scenario_tags and 'tags' in scenario_tags:
        tag_codes = set(scenario_tags['tags'].keys())
        if scenarios_zh:
            missing_tags = set(scenarios_zh.keys()) - tag_codes
            if missing_tags:
                results["missing_scenarios_tags"].append(f"scenario_tags 缺少 {len(missing_tags)} 个标签")
    
    # 5. 检查 modes_data
    if modes_data:
        if isinstance(modes_data, list):
            mode_codes = set()
            for m in modes_data:
                if 'code' in m:
                    mode_codes.add(m['code'])
                if 'name' in m:
                    mode_codes.add(m['name'])
            # 检查 modes 覆盖
            if scenarios_zh:
                all_modes_used = set()
                for entry in scenarios_zh.values():
                    for m in entry.get('modes', []):
                        all_modes_used.add(m)
                missing_modes = all_modes_used - mode_codes
                if missing_modes:
                    results["cross_file_consistency"].append(f"modes_data 缺少模式定义: {missing_modes}")
    
    # 6. 汇总
    results["summary"] = {
        "scenarios_zh_count": len(scenarios_zh) if scenarios_zh else 0,
        "scenarios_en_count": len(scenarios_en) if scenarios_en else 0,
        "code_maps_count": len(code_maps.get('CODE_MAP', {})) if code_maps else 0,
        "scenario_tags_count": len(scenario_tags.get('tags', {})) if scenario_tags else 0,
        "modes_data_count": len(modes_data) if isinstance(modes_data, list) else 0,
        "duplicate_codes_count": len(results["duplicate_codes"]),
        "parse_error_count": len(results["parse_errors"]),
        "format_error_count": len(results["format_errors"]),
        "integrity_issue_count": len(results["integrity_issues"]),
        "cross_consistency_count": len(results["cross_file_consistency"]),
        "missing_tags_count": len(results["missing_scenarios_tags"]),
        "all_passed": (
            len(results["duplicate_codes"]) == 0 and
            len(results["parse_errors"]) == 0 and
            len(results["format_errors"]) == 0 and
            len(results["integrity_issues"]) == 0 and
            len(results["cross_file_consistency"]) == 0 and
            len(results["missing_scenarios_tags"]) == 0
        )
    }
    
    return results


def main():
    tools_dir = "/opt/data/workspace/Protreptic/tools"
    print(f"Verifying main data files in: {tools_dir}")
    
    results = verify_main_data(tools_dir)
    
    # 打印结果
    print("\n=== Main Data Verification Results ===")
    print(f"scenarios_zh entries: {results['summary']['scenarios_zh_count']}")
    print(f"scenarios_en entries: {results['summary']['scenarios_en_count']}")
    print(f"code_maps entries: {results['summary']['code_maps_count']}")
    print(f"scenario_tags entries: {results['summary']['scenario_tags_count']}")
    print(f"modes_data entries: {results['summary']['modes_data_count']}")
    print(f"Duplicate codes: {results['summary']['duplicate_codes_count']}")
    print(f"Parse errors: {results['summary']['parse_error_count']}")
    print(f"Format errors: {results['summary']['format_error_count']}")
    print(f"Integrity issues: {results['summary']['integrity_issue_count']}")
    print(f"Cross-file consistency issues: {results['summary']['cross_consistency_count']}")
    print(f"Missing tags: {results['summary']['missing_tags_count']}")
    
    if results["duplicate_codes"]:
        print("\n❌ Duplicate codes:")
        for d in results["duplicate_codes"][:5]:
            print(f"  - {d}")
    
    if results["parse_errors"]:
        print("\n❌ Parse errors:")
        for e in results["parse_errors"]:
            print(f"  - {e}")
    
    if results["format_errors"]:
        print("\n❌ Format errors:")
        for e in results["format_errors"]:
            print(f"  - {e}")
    
    if results["integrity_issues"]:
        print("\n❌ Integrity issues (first 10):")
        for e in results["integrity_issues"][:10]:
            print(f"  - {e}")
    
    if results["cross_file_consistency"]:
        print("\n❌ Cross-file consistency issues:")
        for e in results["cross_file_consistency"]:
            print(f"  - {e}")
    
    if results["missing_scenarios_tags"]:
        print("\n⚠️ Missing scenario tags:")
        for e in results["missing_scenarios_tags"]:
            print(f"  - {e}")
    
    if results["summary"]["all_passed"]:
        print("\n✅ All verification checks PASSED!")
        return 0
    else:
        print("\n❌ Verification FAILED!")
        return 1


if __name__ == "__main__":
    sys.exit(main())