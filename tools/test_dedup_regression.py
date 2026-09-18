#!/usr/bin/env python3
"""
回归测试：验证去重后的模式库完整性
"""
import json
import sys

def test_no_duplicate_names():
    """测试无重复模式名称"""
    with open('modes_data.json') as f:
        data = json.load(f)
    
    names_zh = []
    names_en = []
    for k, v in data['zh'].items():
        if k.isdigit() and isinstance(v, list) and v:
            names_zh.append(v[0])
    for k, v in data['en'].items():
        if k.isdigit() and isinstance(v, list) and v:
            names_en.append(v[0])
    
    dup_zh = [n for n in set(names_zh) if names_zh.count(n) > 1]
    dup_en = [n for n in set(names_en) if names_en.count(n) > 1]
    
    if dup_zh:
        print(f"❌ FAIL: 中文重复名称: {dup_zh}")
        return False
    if dup_en:
        print(f"❌ FAIL: 英文重复名称: {dup_en}")
        return False
    print(f"✅ PASS: 无重复名称 (中文 {len(names_zh)} 个, 英文 {len(names_en)} 个)")
    return True

def test_core_78_preserved():
    """测试核心 1-78 模式完整保留"""
    with open('modes_data.json') as f:
        data = json.load(f)
    
    missing_zh = []
    missing_en = []
    for i in range(1, 79):
        if str(i) not in data['zh']:
            missing_zh.append(i)
        if str(i) not in data['en']:
            missing_en.append(i)
    
    if missing_zh:
        print(f"❌ FAIL: 中文核心模式缺失: {missing_zh}")
        return False
    if missing_en:
        print(f"❌ FAIL: 英文核心模式缺失: {missing_en}")
        return False
    print("✅ PASS: 核心 1-78 模式完整保留")
    return True

def test_scenario_mapping_valid():
    """测试场景引用的模式 ID 均有效"""
    with open('modes_data.json') as f:
        modes = json.load(f)
    with open('scenarios_zh.json') as f:
        scenarios = json.load(f)
    
    valid_ids = set(int(k) for k in modes['zh'].keys() if k.isdigit())
    
    orphan_count = 0
    for code, sc in scenarios.items():
        if isinstance(sc, dict) and 'modes' in sc:
            for m in sc['modes']:
                if m not in valid_ids:
                    print(f"  孤儿映射: 场景 {code} -> 模式 {m}")
                    orphan_count += 1
    
    if orphan_count > 0:
        print(f"❌ FAIL: 发现 {orphan_count} 个孤儿映射")
        return False
    print("✅ PASS: 所有场景引用有效模式 ID")
    return True

def test_selector_runs():
    """测试思维模式选择器基本功能"""
    import subprocess
    result = subprocess.run([
        sys.executable, 'thinking_mode_selector.py', '-c', 'A-1-X-P'
    ], capture_output=True, text=True, cwd='.')
    
    if result.returncode != 0:
        print(f"❌ FAIL: 选择器报错: {result.stderr[:200]}")
        return False
    print("✅ PASS: 选择器查询正常")
    return True

def test_mode_count_reasonable():
    """测试模式总数在合理范围"""
    with open('modes_data.json') as f:
        data = json.load(f)
    
    zh_count = sum(1 for k in data['zh'].keys() if k.isdigit())
    en_count = sum(1 for k in data['en'].keys() if k.isdigit())
    
    print(f"模式统计: 中文 {zh_count}, 英文 {en_count}")
    
    if zh_count < 500 or zh_count > 600:
        print(f"❌ FAIL: 中文模式数异常: {zh_count}")
        return False
    if en_count < 500 or en_count > 600:
        print(f"❌ FAIL: 英文模式数异常: {en_count}")
        return False
    if zh_count != en_count:
        print(f"❌ FAIL: 中英文模式数不一致")
        return False
    print("✅ PASS: 模式总数合理")
    return True

def test_no_placeholder_modes():
    """测试无占位符模式"""
    with open('modes_data.json') as f:
        data = json.load(f)
    
    placeholders = []
    for k, v in data['zh'].items():
        if k.isdigit() and isinstance(v, list) and v and v[0].startswith('模式_'):
            placeholders.append((k, v[0]))
    
    if placeholders:
        print(f"❌ FAIL: 发现占位符模式: {placeholders}")
        return False
    print("✅ PASS: 无占位符模式")
    return True

def test_no_m_prefixed_garbled():
    """测试无 M 前缀乱码模式"""
    with open('modes_data.json') as f:
        data = json.load(f)
    
    garbled = []
    for k, v in data['zh'].items():
        if k.startswith('M') and isinstance(v, list) and v:
            # 检查是否包含乱码字符
            name = v[0]
            if any(ord(c) > 0xFFFF for c in name) or '�' in name:
                garbled.append((k, name[:50]))
    
    if garbled:
        print(f"❌ FAIL: 发现 M 前缀乱码模式: {garbled}")
        return False
    print("✅ PASS: 无 M 前缀乱码模式")
    return True

def run_all_tests():
    """运行所有测试"""
    tests = [
        test_no_duplicate_names,
        test_core_78_preserved,
        test_scenario_mapping_valid,
        test_mode_count_reasonable,
        test_no_placeholder_modes,
        test_no_m_prefixed_garbled,
        test_selector_runs,
    ]
    
    results = []
    for test in tests:
        try:
            results.append(test())
        except Exception as e:
            print(f"❌ ERROR in {test.__name__}: {e}")
            results.append(False)
    
    passed = sum(results)
    total = len(results)
    print(f"\n=== 总计: {passed}/{total} 通过 ===")
    
    if passed == total:
        print("🎉 所有回归测试通过！")
        return 0
    else:
        print("💥 部分测试失败，请检查上述输出")
        return 1

if __name__ == '__main__':
    sys.exit(run_all_tests())