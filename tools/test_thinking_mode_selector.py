#!/usr/bin/env python3
"""thinking_mode_selector.py 的测试（CI: `.github/workflows/ci-cd.yml` → Run Python tests）。

口径（Phase30-C4-followup / R2）：
  * 场景只认 **api/protreptic.db** 这一个数据源；tools/scenarios_*.json 这类陈年副本已删除，
    本文件断言它们不再出现（防止有人再把旧副本塞回来喂给 selector）。
  * 断言一律**派生**：与数据源、与 web/public/data/index.unified.json 的计数互相印证，
    不再写死 1008 / 370 / 44 / 25 / 455 / 390 这类历史口径 ——
    写死数字的断言一旦数据演进就变成噪声，反而把真实回归埋掉。
  * 保留有意义的语义断言：code 卫生（无空格/占位符）、必有可显示名称、
    modes 结构合法且引用可解析、中英键集一致、CLI 端到端可用。

跑法：cd tools && python3 test_thinking_mode_selector.py
"""
import json
import os
import re
import sqlite3
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from thinking_mode_selector import (  # noqa: E402
    SCENARIOS_ZH,
    SCENARIOS_EN,
    MODES_DATA,
    CODE_MAP,
    CODE_MAP_EN,
    THINKING_MODES_ZH,
)

TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(TOOLS_DIR)
DB_PATH = os.path.join(REPO_ROOT, 'api', 'protreptic.db')
INDEX_PATH = os.path.join(REPO_ROOT, 'web', 'public', 'data', 'index.unified.json')

# 已知的数据层边界（不是"忽略"，而是把越界摊在明面上）：
# db 里引用了模式目录中尚不存在的 id —— 属数据层待补项。
# 断言写成"新越界必须失败、旧越界允许存在"，修好一个不会被测试拦住，
# 新引入一个立刻红。
KNOWN_UNRESOLVED_MODE_REFS = {
    '562', '563', '564', '565', '566', '567', '569',
    'M218', 'M219', 'M220', 'M221', 'M222', 'M223', 'M224', 'M225', 'M226', 'M227', 'M571',
}
# 允许"暂无思维模式"的场景比例上限（当前约 3.4% 属数据层待补；大幅劣化即失败）
MAX_NO_MODE_RATIO = 0.05

CODE_RE = re.compile(r'^[A-Za-z0-9][A-Za-z0-9._-]*$')
PLACEHOLDERS = {'code field', 'code', 'code_field', 'todo', '...'}


def _db_codes():
    con = sqlite3.connect('file:%s?mode=ro' % DB_PATH, uri=True)
    try:
        return {str(c or '').strip() for c, in con.execute('SELECT code FROM figures')
                if str(c or '').strip()}
    finally:
        con.close()


def test_single_data_source():
    """场景来自唯一数据源 api/protreptic.db；陈旧副本不得复活。"""
    assert os.path.exists(DB_PATH), '找不到唯一数据源 %s' % DB_PATH
    db_codes = _db_codes()
    assert len(SCENARIOS_ZH) == len(db_codes), \
        '场景数应与 api/protreptic.db 的 figures 行数一致：loader=%d db=%d' % (
            len(SCENARIOS_ZH), len(db_codes))
    assert set(SCENARIOS_ZH) == db_codes, 'loader 的 code 集合必须等于 db 的 code 集合'
    for stale in ('scenarios_zh.json', 'scenarios_en.json'):
        p = os.path.join(TOOLS_DIR, stale)
        assert not os.path.exists(p), \
            '%s 是陈年副本（真数据在 api/protreptic.db），不得再作为输入' % p
    print('✓ 单一数据源: %d 个场景全部来自 api/protreptic.db（无 scenarios_*.json 副本）'
          % len(SCENARIOS_ZH))


def test_counts_against_unified_index():
    """派生口径断言：selector 的场景集合必须覆盖统一索引里发布的场景。"""
    if not os.path.exists(INDEX_PATH):
        print('⚠ 跳过统一索引交叉校验（%s 未生成；CI 会先跑 tools/build_unified_index.py）'
              % os.path.relpath(INDEX_PATH, REPO_ROOT))
        return
    with open(INDEX_PATH, encoding='utf-8') as fh:
        idx = json.load(fh)
    items = idx['items']
    scen = [it for it in items if it.get('type') == 'scenario']
    assert idx['counts']['total'] == len(items), 'index.counts.total 与 items 长度不一致'
    assert idx['counts']['scenarios'] == len(scen), \
        'index.counts.scenarios 与 scenario 条目数不一致'
    missing = sorted(it['code'] for it in scen if it['code'] not in SCENARIOS_ZH)
    assert not missing, '统一索引发布了场景库里没有的 code: %s' % missing[:10]
    print('✓ 口径一致: index.unified.json scenarios=%d ⊆ 场景库 %d（同一数据源 api/protreptic.db）'
          % (len(scen), len(SCENARIOS_ZH)))


def test_codes_are_clean():
    """code 卫生：无空白、无占位符、无非法字符（回归 Phase30-C1 的脏 code 缺陷）。"""
    bad = [c for c in SCENARIOS_ZH if not CODE_RE.match(c) or c.lower() in PLACEHOLDERS]
    assert not bad, '异常 code（空白/占位符/非法字符）: %s' % bad[:10]
    ws = [c for c in SCENARIOS_ZH if c != c.strip()]
    assert not ws, 'code 含首尾空白: %s' % ws[:10]
    print('✓ code 卫生: %d 个 code 全部合法（无空白/占位符）' % len(SCENARIOS_ZH))


def test_names_present():
    """每个场景都要有可显示名称（缺名退化为 code，而不是空串）。"""
    empty = [c for c, s in SCENARIOS_ZH.items() if not s['name'].strip()]
    assert not empty, '缺少可显示名称的场景: %s' % empty[:10]
    named = sum(1 for c, s in SCENARIOS_ZH.items() if s['name'] != c)
    print('✓ 名称: %d/%d 个场景有真实名称（其余退化为 code，属数据层待补）'
          % (named, len(SCENARIOS_ZH)))


def test_bilingual_consistency():
    """中英键集一致、modes 一致；CODE_MAP 由数据源派生。"""
    assert set(SCENARIOS_ZH) == set(SCENARIOS_EN), '中英场景 code 集合不一致'
    mismatched = [c for c in SCENARIOS_ZH
                  if SCENARIOS_ZH[c]['modes'] != SCENARIOS_EN[c]['modes']]
    assert not mismatched, '中英 modes 不一致: %s' % mismatched[:10]
    assert len(CODE_MAP) == len(SCENARIOS_ZH)
    assert len(CODE_MAP_EN) == len(SCENARIOS_EN)
    for c in SCENARIOS_ZH:
        assert CODE_MAP[c] and CODE_MAP_EN[c], 'CODE_MAP 缺 %s' % c
    print('✓ 双语: %d 个场景中英齐全，modes 一致，CODE_MAP 与数据源同步' % len(SCENARIOS_ZH))


def test_modes_schema_and_coverage():
    """modes 结构合法；覆盖率达标；模式引用可解析（越界只在已知清单内）。"""
    no_modes, refs = [], set()
    for c, s in SCENARIOS_ZH.items():
        m = s['modes']
        assert isinstance(m, list) and all(isinstance(x, (int, str)) for x in m), \
            '%s 的 modes 结构非法: %r' % (c, m)
        if not m:
            no_modes.append(c)
        refs.update(m)
    ratio = 1 - len(no_modes) / max(1, len(SCENARIOS_ZH))
    assert ratio >= 1 - MAX_NO_MODE_RATIO, \
        '无模式场景比例 %.1f%% 超出上限 %.1f%%' % (100 * (1 - ratio), 100 * MAX_NO_MODE_RATIO)

    def resolvable(x):
        s = str(x)
        return s in MODES_DATA['zh'] or (s.isdigit() and int(s) in THINKING_MODES_ZH)

    unresolved = {str(x) for x in refs if not resolvable(x)}
    new = sorted(unresolved - KNOWN_UNRESOLVED_MODE_REFS)
    assert not new, '出现新的悬空模式引用（数据层回归）: %s' % new
    print('✓ modes: %d/%d 场景有模式（覆盖 %.1f%%），%d 个模式引用，悬空 %d 个（均在已知清单内）'
          % (len(SCENARIOS_ZH) - len(no_modes), len(SCENARIOS_ZH), 100 * ratio,
             len(refs), len(unresolved)))


def test_modes_catalog_parity():
    """模式目录本身的中英键集一致（派生断言，不写死 618）。"""
    zh_keys = set(MODES_DATA['zh'])
    en_keys = set(MODES_DATA['en'])
    assert zh_keys == en_keys, '模式目录中英键集不一致: %s' % sorted(zh_keys ^ en_keys)[:10]
    numeric = {k for k in zh_keys if k.isdigit()}
    assert len(THINKING_MODES_ZH) == len(numeric)
    assert numeric, '模式目录里没有任何数字模式，数据源可疑'
    print('✓ 模式目录: %d 个模式键（中英一致），可解析数字模式 %d 个'
          % (len(zh_keys), len(THINKING_MODES_ZH)))


def _run(args):
    return subprocess.run([sys.executable, 'thinking_mode_selector.py'] + args,
                          capture_output=True, text=True, cwd=TOOLS_DIR)


def _pick_rich_scenario():
    cands = sorted(c for c, s in SCENARIOS_ZH.items() if s['name'] != c and s['modes'])
    assert cands, '数据源里没有"有名称且有模式"的场景'
    return cands[0]


def test_cli_query():
    code = _pick_rich_scenario()
    for lang in ('zh', 'en'):
        r = _run(['-c', code, '--lang', lang])
        assert r.returncode == 0, 'CLI query %s %s failed: %s' % (code, lang, r.stderr)
        assert code in r.stdout
    print('✓ CLI -c: %s 中英查询正常' % code)


def test_cli_search():
    code = _pick_rich_scenario()
    kw = SCENARIOS_ZH[code]['name'][:2]
    r = _run(['-s', kw])
    assert r.returncode == 0, 'CLI search failed: %s' % r.stderr
    assert code in r.stdout, '搜索 %s 应命中 %s' % (kw, code)
    print('✓ CLI -s: 关键词 %s 命中 %s' % (kw, code))


def test_cli_list_and_export():
    r = _run(['-l'])
    assert r.returncode == 0, 'CLI -l failed: %s' % r.stderr
    listed = [ln for ln in r.stdout.split('\n')
              if ln.strip().startswith(('A-', 'B-', 'C-', 'D-', 'H-', 'M-'))]
    expected = [c for c in SCENARIOS_ZH if c.split('-')[0] in ('A', 'B', 'C', 'D', 'H', 'M')]
    assert len(listed) == len(expected), \
        'CLI -l 列出 %d 行，数据源里 A/B/C/D/H/M 分类场景 %d 个' % (len(listed), len(expected))

    r = _run(['-e', 'json'])
    assert r.returncode == 0, 'CLI -e json failed: %s' % r.stderr
    data = json.loads(r.stdout)
    assert len(data) == len(SCENARIOS_ZH), \
        '导出 JSON 条数 %d != 数据源场景数 %d' % (len(data), len(SCENARIOS_ZH))
    r = _run(['-e', 'md'])
    assert r.returncode == 0, 'CLI -e md failed: %s' % r.stderr
    print('✓ CLI -l/-e: 列表 %d 行，导出 JSON %d 条 / Markdown 正常' % (len(listed), len(data)))


def test_cli_tag_filter():
    """标签由数据源派生：用数据里真实存在的标签值做端到端筛选。"""
    key = value = code = None
    for c, s in sorted(SCENARIOS_ZH.items()):
        for k in ('historical_domains', 'domains'):
            if s[k]:
                key, value, code = k, s[k][0], c
                break
        if key:
            break
    if not key:
        print('⚠ 跳过 CLI -t（数据源里暂无标签值）')
        return
    r = _run(['-t', '%s=%s' % (key, value)])
    assert r.returncode == 0, 'CLI -t failed: %s' % r.stderr
    assert code in r.stdout, '按 %s=%s 筛选应命中 %s' % (key, value, code)
    print('✓ CLI -t: %s=%s 命中 %s' % (key, value, code))


def run_all_tests():
    tests = [
        test_single_data_source,
        test_counts_against_unified_index,
        test_codes_are_clean,
        test_names_present,
        test_bilingual_consistency,
        test_modes_schema_and_coverage,
        test_modes_catalog_parity,
        test_cli_query,
        test_cli_search,
        test_cli_list_and_export,
        test_cli_tag_filter,
    ]
    for t in tests:
        t()
    print('\n=== ALL TESTS PASSED (%d) ===' % len(tests))


if __name__ == '__main__':
    run_all_tests()
