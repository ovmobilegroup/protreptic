#!/usr/bin/env python3
"""
Unit tests for thinking_mode_selector.py
"""
import sys
import os
import json
import subprocess
sys.path.insert(0, os.path.dirname(__file__))

from thinking_mode_selector import (
    SCENARIOS_ZH,
    SCENARIOS_EN,
    MODES_DATA,
    CODE_MAP,
    CODE_MAP_EN,
)

# All international prefixes for counting
INTL_PREFIXES = (
    'EU-', 'UK-', 'US-', 'RU-', 'JP-', 'KR-', 'BR-', 'FR-', 'IT-', 'IN-', 'IR-', 'AT-', 'CH-', 'PL-', 'CZ-',
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
    'PY-', 'UY-', 'AR-', 'CL-', 'MX-', 'GT-', 'SV-', 'NI-', 'CU-', 'HT-', 'DO-', 'JM-', 'CA-', 'US-', 'GL-'
)


def test_scenarios_zh():
    """测试中文场景加载"""
    assert len(SCENARIOS_ZH) == 1008, f"Expected 1008, got {len(SCENARIOS_ZH)}"
    h_count = sum(1 for k in SCENARIOS_ZH if k.startswith('H-') or k.startswith('M-'))
    assert h_count == 370, f"Expected 370 historical figures, got {h_count}"
    p4_count = sum(1 for k in SCENARIOS_ZH if k.startswith('P4-'))
    assert p4_count == 44, f"Expected 44 P4 figures, got {p4_count}"
    p5_count = sum(1 for k in SCENARIOS_ZH if k.startswith('P5-'))
    assert p5_count == 25, f"Expected 25 P5 figures, got {p5_count}"
    intl_count = sum(1 for k in SCENARIOS_ZH if k.startswith(INTL_PREFIXES))
    assert intl_count == 455, f"Expected 455 international figures, got {intl_count}"
    print(f"��� SCENARIOS_ZH: {len(SCENARIOS_ZH)} total, {h_count} historical, {p4_count} P4, {p5_count} P5, {intl_count} international")


def test_scenarios_en():
    """测试英文场景加载"""
    assert len(SCENARIOS_EN) == 1008, f"Expected 1008, got {len(SCENARIOS_EN)}"
    h_count = sum(1 for k in SCENARIOS_EN if k.startswith('H-') or k.startswith('M-'))
    assert h_count == 370, f"Expected 370 historical figures, got {h_count}"
    p4_count = sum(1 for k in SCENARIOS_EN if k.startswith('P4-'))
    assert p4_count == 44, f"Expected 44 P4 figures, got {p4_count}"
    p5_count = sum(1 for k in SCENARIOS_EN if k.startswith('P5-'))
    assert p5_count == 25, f"Expected 25 P5 figures, got {p5_count}"
    intl_count = sum(1 for k in SCENARIOS_EN if k.startswith(INTL_PREFIXES))
    assert intl_count == 455, f"Expected 455 international figures, got {intl_count}"
    print(f"��� SCENARIOS_EN: {len(SCENARIOS_EN)} total, {h_count} historical, {p4_count} P4, {p5_count} P5, {intl_count} international")


def test_modes_data():
    """��试思维模式数据加载"""
    assert 'zh' in MODES_DATA and 'en' in MODES_DATA
    zh_modes = MODES_DATA['zh']
    en_modes = MODES_DATA['en']
    # ��持��展模式：原 42 个 + Phase 4 新增 + Phase 9.1 新增 (M215, M216, M217) + Phase 18.6 Central/Eastern Europe (M520-M533) + Middle East/Central Asia (M612-M633) + Africa legacy (M577, M578, M579, M581, M582, M584) + Phase 19 H-001
    assert len(zh_modes) == 618, f"Expected 618 zh modes, got {len(zh_modes)}"
    assert len(en_modes) == 618, f"Expected 618 en modes, got {len(en_modes)}"
    # Check modes that exist in both - all numeric + M-prefixed modes are now bilingual
    for mode_id in en_modes:
        assert mode_id in zh_modes, f"Missing ZH mode: {mode_id}"
        zh_mode = zh_modes[mode_id]
        en_mode = en_modes[mode_id]
        assert isinstance(zh_mode, list) and len(zh_mode) >= 2
        assert isinstance(en_mode, list) and len(en_mode) >= 2
    print(f"��� MODES_DATA: {len(zh_modes)} zh modes + {len(en_modes)} en modes (all bilingual including 6 M-prefixed legacy modes)")


def test_code_maps():
    """��试代码映射加载"""
    # CODE_MAP should have one entry per scenario dict entry (984)
    dict_count = sum(1 for k in SCENARIOS_ZH if isinstance(SCENARIOS_ZH[k], dict))
    assert len(CODE_MAP) == dict_count, f"Expected {dict_count} CODE_MAP, got {len(CODE_MAP)}"
    assert len(CODE_MAP_EN) == dict_count, f"Expected {dict_count} CODE_MAP_EN, got {len(CODE_MAP_EN)}"
    for code in CODE_MAP:
        assert code in CODE_MAP_EN, f"Missing EN mapping for {code}"
    print(f"��� CODE_MAP: {len(CODE_MAP)}, CODE_MAP_EN: {len(CODE_MAP_EN)}")


def test_bilingual_consistency():
    """测试中英文一致性 - 支持多种字段格式（标准格式 + 国际化格式）"""
    # 标准字段名（基础条目）
    standard_keys = {'name', 'description', 'modes', 'reason', 'steps', 'expected', 'case'}
    # 国际化字段名（新增条目）
    zh_i18n_keys = {'name_zh', 'description_zh', 'reason_zh', 'steps_zh', 'expected_zh', 'case_zh'}
    en_i18n_keys = {'name_en', 'description_en', 'reason_en', 'steps_en', 'expected_en', 'case_en'}

    for code in SCENARIOS_ZH:
        assert code in SCENARIOS_EN, f"Missing EN for {code}"
        zh_entry = SCENARIOS_ZH[code]
        en_entry = SCENARIOS_EN[code]

        # Skip non-dict entries (metadata fields)
        if not isinstance(zh_entry, dict) or not isinstance(en_entry, dict):
            continue

        zh_keys = set(zh_entry.keys())
        en_keys = set(en_entry.keys())

        # 检查基础字段：至少要有 name/description/modes 的某种形式
        # 标准格式或国际化格式
        has_name = ('name' in zh_keys and 'name' in en_keys) or \
                   ('name_zh' in zh_keys and 'name_en' in en_keys)
        has_desc = ('description' in zh_keys and 'description' in en_keys) or \
                   ('description_zh' in zh_keys and 'description_en' in en_keys)
        has_modes = 'modes' in zh_keys and 'modes' in en_keys

        assert has_name, f"Missing name field for {code}"
        assert has_desc, f"Missing description field for {code}"
        assert has_modes, f"Missing modes field for {code}"

        # Check modes match
        assert zh_entry['modes'] == en_entry['modes'], f"Modes mismatch for {code}"
    print("✓ Bilingual consistency: all required keys and modes match")


def test_modes_coverage():
    """测试模式覆盖度"""
    used_modes = set()
    for entry in SCENARIOS_ZH.values():
        if not isinstance(entry, dict):
            continue
        used_modes.update(entry['modes'])
    zh_modes = MODES_DATA['zh']
    for mode_id in used_modes:
        assert str(mode_id) in zh_modes, f"Mode {mode_id} used but not defined"
    print(f"✓ Mode coverage: {len(used_modes)}/550 modes used")


def test_new_batch_figures():
    """测试新增批次人物"""
    # Batch 1: 10 modern entrepreneurs
    batch_a = ['H-RZF-270', 'H-MY-271', 'H-MHT-272', 'H-LJ-273', 'H-WX-274',
               'H-ZYM-275', 'H-HZ-276', 'H-LYH-277', 'H-DL-278', 'H-CW-279']
    # Batch 2: 6 Mao phases
    batch_b = ['M-JGS-280', 'M-CZ-281', 'M-YA-282', 'M-JG-283', 'M-TS-284', 'M-WN-285']
    # Batch 3: 12 literature
    batch_c = ['H-SC-286', 'H-HT-287', 'H-MF-288', 'H-ZMF-289', 'H-WZM-290',
               'H-DQC-291', 'H-WXZ-292', 'H-YZQ-293', 'H-OYX-294', 'H-LGQ-295',
               'H-GHQ-296', 'H-TXZ-297']
    # Batch 4: 8 economics
    batch_d = ['H-CY-298', 'H-XMQ-299', 'H-WJL-300', 'H-LYN-301',
               'H-ZRJ-302', 'H-ZXC-303', 'H-YG-304', 'H-PGS-305']
    # Batch 5: 8 diplomacy
    batch_e = ['H-ZEL-306', 'H-QGH-307', 'H-HH-308', 'H-QQK-309',
               'H-TJX-310', 'H-LZX-311', 'H-YJC-312', 'H-WY-313']
    # Batch 6: 8 education
    batch_f = ['H-CYP-314', 'H-THZ-315', 'H-MYQ-316', 'H-ZKZ-317',
               'H-QWC-318', 'H-ZGY-319', 'H-GYH-320', 'H-LZD-321']
    # Batch 7: 10 new (Phase 3 Batch 1)
    batch_g = ['H-SY-322', 'H-ZHL-323', 'H-HY-324', 'H-ZEL-325', 'H-QXS-326',
               'H-WL-327', 'H-CY-328', 'H-SQL-329', 'H-DJX-330', 'H-FXT-331']
    # Batch 8: 20 new (Phase 3 Batch 2)
    batch_h = ['H-ZEL-332', 'H-LSQ-333', 'H-PDH-334', 'H-LRH-335', 'H-YDZ-336',
               'H-QXS-337', 'H-DJX-338', 'H-HLG-339', 'H-ZKZ-340', 'H-YYY-341',
               'H-BYB-342', 'H-WL-343', 'H-TJY-344', 'H-AZJ-345',
               'H-CY-346', 'H-LXN-347', 'H-QGH-348',
               'H-SQL-349', 'H-DYC-350', 'H-FXT-351']
    # Batch 9: 5 final batch (newly added)
    batch_i = ['H-LCZ-362', 'H-WLF-363', 'H-PZ-364', 'H-GM-365', 'H-BYB-366']
    # Batch 10: M-ZD-001 (Mao Zedong — Revolutionary Program Engineering)
    batch_j = ['M-ZD-001']

    all_new = batch_a + batch_b + batch_c + batch_d + batch_e + batch_f + batch_g + batch_h + batch_i + batch_j
    for code in all_new:
        assert code in SCENARIOS_ZH, f"Missing ZH: {code}"
        assert code in SCENARIOS_EN, f"Missing EN: {code}"
        assert code in CODE_MAP, f"Missing CODE_MAP: {code}"
        assert code in CODE_MAP_EN, f"Missing CODE_MAP_EN: {code}"
    print(f"✓ New batch figures: all {len(all_new)} present")


def test_cli_list():
    """测试 CLI 列表功能 - 验证输出包含预期的场景数量"""
    result = subprocess.run(
        [sys.executable, 'thinking_mode_selector.py', '-l'],
        capture_output=True, text=True, cwd=os.path.dirname(__file__)
    )
    assert result.returncode == 0, f"CLI -l failed: {result.stderr}"
    lines = [line for line in result.stdout.split('\n') if line.strip().startswith(('A-', 'B-', 'C-', 'D-', 'H-', 'M-'))]
    # CLI 只显示 A/B/C/D/H/M 分类，不包含 P4 专题场景和国际场景
    assert len(lines) == 390, f"Expected 390 scenario lines (A/B/C/D/H/M categories), got {len(lines)}"
    print(f"✓ CLI -l: works, listed {len(lines)} scenarios")


def test_cli_query():
    """测试 CLI 单个查询"""
    for code in ['H-RZF-270', 'M-JGS-280', 'H-SC-286', 'H-CY-298']:
        for lang in ['zh', 'en']:
            result = subprocess.run(
                [sys.executable, 'thinking_mode_selector.py', '-c', code, '--lang', lang],
                capture_output=True, text=True, cwd=os.path.dirname(__file__)
            )
            assert result.returncode == 0, f"CLI query {code} {lang} failed: {result.stderr}"
            assert code in result.stdout
    print("✓ CLI query: works for new batch figures")


def test_cli_search():
    """测试 CLI 搜索功能"""
    for keyword in ['任正非', '毛泽东', '苏轼', '陈云', '周恩来', '蔡元培']:
        result = subprocess.run(
            [sys.executable, 'thinking_mode_selector.py', '-s', keyword],
            capture_output=True, text=True, cwd=os.path.dirname(__file__)
        )
        assert result.returncode == 0, f"CLI search {keyword} failed: {result.stderr}"
        assert '搜索' in result.stdout or '结果' in result.stdout or 'H-' in result.stdout or 'M-' in result.stdout
    print("✓ CLI search: works")


def test_cli_export():
    """测试 CLI 导出功能"""
    for fmt in ['json', 'md']:
        result = subprocess.run(
            [sys.executable, 'thinking_mode_selector.py', '-e', fmt],
            capture_output=True, text=True, cwd=os.path.dirname(__file__)
        )
        assert result.returncode == 0, f"CLI export {fmt} failed: {result.stderr}"
    print("✓ CLI export: works")


def test_cli_tag_filter():
    """测试 CLI 标签筛选"""
    result = subprocess.run(
        [sys.executable, 'thinking_mode_selector.py', '-t', 'historical_domains=Military'],
        capture_output=True, text=True, cwd=os.path.dirname(__file__)
    )
    assert result.returncode == 0, f"CLI tag filter failed: {result.stderr}"
    assert 'H-' in result.stdout or 'M-' in result.stdout
    print("✓ CLI tag filter: works")


def test_new_south_asia_figures():
    """测试新增南亚次大陆人物"""
    # Phase 9.1 新增的8个南亚次大陆人物
    south_asia_codes = ['PK-ISL-001', 'PK-SUF-001', 'BD-LIB-001', 'LK-CIV-001', 
                       'NP-HIM-001', 'AF-TRI-001', 'MV-ISL-001', 'BT-GNH-001']
    for code in south_asia_codes:
        assert code in SCENARIOS_ZH, f"Missing ZH: {code}"
        assert code in SCENARIOS_EN, f"Missing EN: {code}"
        assert code in CODE_MAP, f"Missing CODE_MAP: {code}"
        assert code in CODE_MAP_EN, f"Missing CODE_MAP_EN: {code}"
        # 验证新人物使用了新的思维模式
        if code == 'PK-ISL-001':
            assert 215 in SCENARIOS_ZH[code]['modes'], f"PK-ISL-001 should use mode 215"
        elif code == 'LK-CIV-001':
            assert 216 in SCENARIOS_ZH[code]['modes'], f"LK-CIV-001 should use mode 216"
        elif code == 'BT-GNH-001':
            assert 217 in SCENARIOS_ZH[code]['modes'], f"BT-GNH-001 should use mode 217"
    print(f"✓ South Asia figures: all {len(south_asia_codes)} present with correct modes")


def run_all_tests():
    test_scenarios_zh()
    test_scenarios_en()
    test_modes_data()
    test_code_maps()
    test_bilingual_consistency()
    test_modes_coverage()
    test_new_batch_figures()
    test_new_south_asia_figures()
    test_cli_list()
    test_cli_query()
    test_cli_search()
    test_cli_export()
    test_cli_tag_filter()
    print("\n=== ALL TESTS PASSED ===")


if __name__ == '__main__':
    run_all_tests()