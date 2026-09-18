#!/usr/bin/env python3
"""
Data Verifier for Protreptic Project
验证合并后的数据完整性和正确性

Usage: python data_verifier.py <workspace_path>
"""

import json
import sys
import os
from pathlib import Path
from collections import Counter


def verify_workspace(workspace_path: str) -> dict:
    """验证工作区中的所有 JSON 文件和主数据文件"""
    workspace = Path(workspace_path)
    
    results = {
        "duplicate_codes": [],
        "parse_errors": [],
        "format_errors": [],
        "integrity_issues": [],
        "missing_scenarios_tags": [],
        "summary": {}
    }
    
    # 1. 检查工作区 JSON 文件
    json_files = list(workspace.glob("*.json"))
    all_codes = []
    
    for json_file in json_files:
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 检查必要字段
            required_fields = ['code', 'name_zh', 'name_en', 'modes']
            for field in required_fields:
                if field not in data:
                    results["format_errors"].append(f"{json_file.name}: 缺少字段 {field}")
            
            # 收集 code
            if 'code' in data:
                all_codes.append(data['code'])
                
        except json.JSONDecodeError as e:
            results["parse_errors"].append(f"{json_file.name}: {str(e)}")
        except Exception as e:
            results["format_errors"].append(f"{json_file.name}: {str(e)}")
    
    # 2. 检查重复 code
    code_counts = Counter(all_codes)
    for code, count in code_counts.items():
        if count > 1:
            results["duplicate_codes"].append(f"{code}: 出现 {count} 次")
    
    # 3. 验证主数据文件 (如果存在)
    main_files = {
        "scenarios_zh.json": workspace / "scenarios_zh.json",
        "scenarios_en.json": workspace / "scenarios_en.json", 
        "code_maps.json": workspace / "code_maps.json",
        "scenario_tags.json": workspace / "scenario_tags.json",
        "modes_data.json": workspace / "modes_data.json"
    }
    
    for name, path in main_files.items():
        if path.exists():
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # 检查是否有空值或异常
                if isinstance(data, dict):
                    for k, v in data.items():
                        if v is None:
                            results["integrity_issues"].append(f"{name}: {k} 值为 null")
                        if isinstance(v, dict):
                            for field in ['code', 'name_zh', 'name_en', 'modes']:
                                if field not in v and k.startswith(('H-', 'A-', 'B-', 'C-', 'D-', 'M-', 'IN-', 'IR-', 'IL-', 'SE-', 'CM-', 'CF-', 'TD-', 'CG-', 'GA-', 'GQ-', 'ST-', 'AO-', 'PK-', 'BD-', 'LK-', 'NP-', 'AF-', 'MV-', 'BT-', 'TR-', 'EG-', 'MA-', 'DZ-', 'TN-', 'LY-', 'SD-', 'YE-', 'OM-', 'AE-', 'QA-', 'KW-', 'BH-', 'SA-', 'JO-', 'PS-', 'GE-', 'AM-', 'AZ-')):
                                    results["integrity_issues"].append(f"{name}: {k} 缺少字段 {field}")
                            # 检查场景字段
                            if k.startswith(('H-', 'A-', 'B-', 'C-', 'D-')):
                                for field in ['name_zh', 'name_en', 'description_zh', 'description_en', 'reason_zh', 'reason_en', 'steps_zh', 'steps_en', 'expected_zh', 'expected_en', 'case_zh', 'case_en', 'era', 'gender', 'ethnicity', 'historical_domains', 'domains', 'core_modes', 'applications', 'mode_count']:
                                    if field not in v:
                                        results["missing_scenarios_tags"].append(f"{name}: {k} 缺少场景字段 {field}")
                        
            except json.JSONDecodeError as e:
                results["parse_errors"].append(f"{name}: {str(e)}")
            except Exception as e:
                results["integrity_issues"].append(f"{name}: {str(e)}")
    
    # 4. 汇总
    results["summary"] = {
        "json_files_checked": len(json_files),
        "total_codes": len(all_codes),
        "unique_codes": len(set(all_codes)),
        "duplicate_count": len(results["duplicate_codes"]),
        "parse_error_count": len(results["parse_errors"]),
        "format_error_count": len(results["format_errors"]),
        "integrity_issue_count": len(results["integrity_issues"]),
        "missing_scenarios_tags_count": len(results["missing_scenarios_tags"]),
        "all_passed": (
            len(results["duplicate_codes"]) == 0 and
            len(results["parse_errors"]) == 0 and
            len(results["format_errors"]) == 0 and
            len(results["integrity_issues"]) == 0 and
            len(results["missing_scenarios_tags"]) == 0
        )
    }
    
    return results


def main():
    if len(sys.argv) < 2:
        print("Usage: python data_verifier.py <workspace_path>")
        sys.exit(1)
    
    workspace_path = sys.argv[1]
    print(f"Verifying workspace: {workspace_path}")
    
    results = verify_workspace(workspace_path)
    
    # 打印结果
    print("\n=== Verification Results ===")
    print(f"JSON files checked: {results['summary']['json_files_checked']}")
    print(f"Total codes: {results['summary']['total_codes']}")
    print(f"Unique codes: {results['summary']['unique_codes']}")
    print(f"Duplicate codes: {results['summary']['duplicate_count']}")
    print(f"Parse errors: {results['summary']['parse_error_count']}")
    print(f"Format errors: {results['summary']['format_error_count']}")
    print(f"Integrity issues: {results['summary']['integrity_issue_count']}")
    print(f"Missing scenario/tags: {results['summary']['missing_scenarios_tags_count']}")
    
    if results["duplicate_codes"]:
        print("\n❌ Duplicate codes:")
        for d in results["duplicate_codes"]:
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
        print("\n❌ Integrity issues:")
        for e in results["integrity_issues"]:
            print(f"  - {e}")
    
    if results["missing_scenarios_tags"]:
        print("\n⚠️ Missing scenario/tags (first 10):")
        for e in results["missing_scenarios_tags"][:10]:
            print(f"  - {e}")
    
    if results["summary"]["all_passed"]:
        print("\n✅ All verification checks PASSED!")
        return 0
    else:
        print("\n❌ Verification FAILED!")
        return 1


if __name__ == "__main__":
    sys.exit(main())