#!/usr/bin/env python3
"""
QA Gate — 自动化验收检查
用法: python qa_gate.py
"""
import json
import sys
import subprocess
from pathlib import Path

TOOLS_DIR = Path("/opt/data/workspace/Protreptic/tools")

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def check_scenarios_integrity():
    """检查 scenarios 完整性"""
    zh = load_json(TOOLS_DIR / "scenarios_zh.json")
    en = load_json(TOOLS_DIR / "scenarios_en.json")
    code_maps = load_json(TOOLS_DIR / "code_maps.json")
    scenario_tags = load_json(TOOLS_DIR / "scenario_tags.json")
    modes_data = load_json(TOOLS_DIR / "modes_data.json")
    
    errors = []
    warnings = []
    
    # 1. 中英文数量一致
    if len(zh) != len(en):
        errors.append(f"ZH/EN count mismatch: {len(zh)} vs {len(en)}")
    
    # 2. 每个 code 都有 EN 对应
    for code in zh:
        if code not in en:
            errors.append(f"Missing EN for {code}")
    
    # 3. code_maps 覆盖 - 仅检查实际场景 code
    scenario_codes = [k for k in zh if isinstance(zh[k], dict) and 'modes' in zh[k]]
    for code in scenario_codes:
        if code not in code_maps.get('CODE_MAP', {}):
            errors.append(f"Missing CODE_MAP for {code}")
        if code not in code_maps.get('CODE_MAP_EN', {}):
            errors.append(f"Missing CODE_MAP_EN for {code}")
    
    # 4. 字段完整性 (国际化格式) - 仅检查新版国际化格式条目
    required_fields = ['code', 'description_zh', 'description_en', 'modes']
    for code, data in zh.items():
        if not isinstance(data, dict):
            continue
        # 跳过旧版格式条目 (A/B/C/D/H/M/P4/P5 前缀，且没有 description_zh 字段)
        legacy_prefixes = ('A-', 'B-', 'C-', 'D-', 'H-', 'M-', 'P4-', 'P5-')
        if code.startswith(legacy_prefixes) and 'description_zh' not in data:
            continue
        for field in required_fields:
            if field not in data:
                errors.append(f"{code}: missing required field '{field}'")
    
    # 5. 模式覆盖
    zh_modes = modes_data.get('zh', {})
    en_modes = modes_data.get('en', {})
    used_modes = set()
    for data in zh.values():
        if isinstance(data, dict):
            used_modes.update(str(m) for m in data.get('modes', []))
    
    missing_modes = [m for m in used_modes if m not in zh_modes]
    if missing_modes:
        errors.append(f"Modes used but not defined: {sorted(missing_modes)}")
    
    # 6. 双语模式一致
    for mode_id in zh_modes:
        if mode_id not in en_modes:
            errors.append(f"Missing EN mode: {mode_id}")
    
    # 7. 统计
    h_count = sum(1 for k in zh if k.startswith('H-') or k.startswith('M-'))
    p4_count = sum(1 for k in zh if k.startswith('P4-'))
    p5_count = sum(1 for k in zh if k.startswith('P5-'))
    
    intl_prefixes = ('EU-', 'UK-', 'US-', 'RU-', 'JP-', 'KR-', 'BR-', 'FR-', 'IT-', 'IN-', 'IR-', 'AT-', 'CH-', 'PL-', 'CZ-',
        'MX-', 'AR-', 'CL-', 'CO-', 'IL-', 'SE-', 'NO-', 'DK-', 'FI-', 'ZA-', 'NG-', 'KE-', 'EG-', 'SG-', 'TH-',
        'VN-', 'ID-', 'PH-', 'AU-', 'NZ-', 'TR-', 'UZ-', 'KZ-', 'MN-', 'TW-', 'SA-', 'IQ-', 'SY-', 'LB-', 'JO-',
        'PS-', 'CA-', 'GL-', 'INU-', 'CA-SMI-', 'UA-', 'BY-', 'RS-', 'HR-', 'SI-', 'HU-', 'RO-', 'BG-', 'ET-',
        'GH-', 'TZ-', 'CD-', 'SN-', 'CI-', 'MZ-', 'AO-', 'PE-', 'VE-', 'CU-', 'BO-', 'EC-', 'UY-', 'PY-', 'KG-',
        'TJ-', 'TM-', 'MM-', 'KH-', 'LA-', 'BN-', 'ID-', 'PH-', 'TL-', 'PG-', 'FJ-', 'WS-', 'TO-', 'VU-', 'JM-',
        'HT-', 'DO-', 'TT-', 'BB-', 'AR-', 'CL-', 'PK-', 'BD-', 'LK-', 'NP-', 'AF-', 'MV-', 'BT-', 'AE-', 'QA-',
        'KW-', 'BH-', 'SA-', 'JO-', 'PS-', 'ML-', 'BF-', 'NE-', 'MR-', 'SN-', 'GM-', 'GW-', 'CI-', 'LR-', 'SL-',
        'ZA-', 'ZW-', 'BW-', 'NA-', 'SZ-', 'CO-', 'EC-', 'PE-', 'BO-', 'PY-', 'UY-', 'AR-', 'ES-', 'PT-', 'GR-',
        'AL-', 'MK-', 'BA-', 'SI-', 'MT-', 'NO-', 'SE-', 'DK-', 'FI-', 'EE-', 'LV-', 'LT-', 'PL-', 'GE-', 'AM-',
        'AZ-', 'MD-', 'RO-', 'KZ-', 'UZ-', 'KG-', 'TJ-', 'TM-', 'VN-', 'LA-', 'KH-', 'TH-', 'MM-', 'MY-', 'ID-',
        'PH-', 'SG-', 'BN-', 'TL-', 'NP-', 'BT-', 'LK-', 'MV-', 'YE-', 'OM-', 'KW-', 'BH-', 'QA-', 'AE-', 'JO-',
        'LB-', 'SY-', 'IQ-', 'NG-', 'KE-', 'TZ-', 'ZW-', 'ZA-', 'ET-', 'GH-', 'SN-', 'CI-', 'CO-', 'EC-', 'BO-',
        'PY-', 'UY-', 'AR-', 'CL-', 'MX-', 'GT-', 'SV-', 'NI-', 'CU-', 'HT-', 'DO-', 'JM-', 'CA-', 'US-', 'GL-')
    
    intl_count = sum(1 for k in zh if k.startswith(intl_prefixes))
    
    print(f"=== QA Report ===")
    print(f"Total scenarios: {len(zh)}")
    print(f"Historical (H/M): {h_count}")
    print(f"P4: {p4_count}")
    print(f"P5: {p5_count}")
    print(f"International: {intl_count}")
    print(f"Base (A/B/C/D): {len(zh) - h_count - p4_count - p5_count - intl_count}")
    print(f"Modes defined: {len(zh_modes)} zh + {len(en_modes)} en")
    print(f"Modes used: {len(used_modes)}")
    
    if errors:
        print(f"\n❌ ERRORS ({len(errors)}):")
        for e in errors:
            print(f"  - {e}")
        return False
    
    if warnings:
        print(f"\n⚠️  WARNINGS ({len(warnings)}):")
        for w in warnings:
            print(f"  - {w}")
    
    print("\n✅ ALL CHECKS PASSED")
    return True

def run_cli_tests():
    """运行 CLI 测试"""
    result = subprocess.run(
        [sys.executable, 'test_thinking_mode_selector.py'],
        cwd=TOOLS_DIR, capture_output=True, text=True, timeout=120
    )
    print(result.stdout)
    if result.stderr:
        print(result.stderr)
    return result.returncode == 0

if __name__ == '__main__':
    ok = True
    ok &= check_scenarios_integrity()
    print("\n=== Running CLI Tests ===")
    ok &= run_cli_tests()
    
    if ok:
        print("\n🎉 QA GATE PASSED")
        sys.exit(0)
    else:
        print("\n💥 QA GATE FAILED")
        sys.exit(1)