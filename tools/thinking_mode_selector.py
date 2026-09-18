#!/usr/bin/env python3
"""
思维模式选择器 - 可执行工具
基于 Protreptic 知识体系（78种思维模式 + 10种写作技法）

用法:
    python thinking_mode_selector.py           # 交互式诊断模式
    python thinking_mode_selector.py -c CODE   # 直接查询处境代码
    python thinking_mode_selector.py -l        # 列出所有场景
    python thinking_mode_selector.py -s        # 搜索场景
    python thinking_mode_selector.py -e json   # 导出所有场景为 JSON
    python thinking_mode_selector.py -e md     # 导出所有场景为 Markdown
    python thinking_mode_selector.py -c A-1-X-P -e json  # 导出单个场景
    python thinking_mode_selector.py --lang en  # 英文输出
    python thinking_mode_selector.py -t 领域=军事  # 按标签筛选
"""

import sys
import json
import sqlite3
import argparse
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from pathlib import Path


@dataclass
class ThinkingMode:
    id: int
    name: str
    description: str
    formula: str
    scenario: str


@dataclass
class ModeCombination:
    modes: List[ThinkingMode]
    reason: str
    steps: List[str]
    expected: List[str]
    case: str


def load_json(filename: str) -> Any:
    path = Path(__file__).parent / filename
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


# ── 数据源：只认 api/protreptic.db ────────────────────────────────────────────
# 场景（SCENARIOS_ZH/EN）、code→名称（CODE_MAP*）、标签（SCENARIO_TAGS）全部从
# api/protreptic.db 的 figures 表派生 —— 这是全站（web/public/data/**、
# index.unified.json、质量门 tools/ci_data_check.py）共用的唯一真相源。
#
# 历史坑：本文件曾经读 tools/scenarios_zh.json / tools/scenarios_en.json，
# 那是 39 键的陈年副本（真数据早已是 db 里的 1000+ 场景），
# 断言与导出因此长期对着旧数据自说自话。这类副本已删除，不再作为输入。
# 模式目录仍读 tools/modes_data.json（数字/M 前缀模式的名称与定义，不是场景副本）。
REPO_ROOT = Path(__file__).resolve().parent.parent


def _find_db() -> Path:
    """定位 api/protreptic.db（解析顺序与 figure_library._find_data_file 同构）。"""
    candidates = [
        REPO_ROOT / 'api' / 'protreptic.db',                 # <repo>/tools/ -> <repo>/api/
        Path(__file__).resolve().parent / 'api' / 'protreptic.db',
        Path.cwd() / 'api' / 'protreptic.db',
    ]
    for c in candidates:
        if c.exists() and c.stat().st_size > 10_000:
            return c
    raise FileNotFoundError(
        '找不到 api/protreptic.db（场景唯一数据源）。已尝试: '
        + ', '.join(str(c) for c in candidates)
    )


def _as_list(v: Any) -> List[Any]:
    """db 里的 steps/expected/modes 等列是 JSON 文本；缺失/坏值一律退化为 []。"""
    if v is None or v == '':
        return []
    try:
        val = json.loads(v)
    except Exception:
        return [v] if isinstance(v, str) and v.strip() else []
    if isinstance(val, list):
        return val
    if val is None or val == '':
        return []
    return [val]


def load_scenarios(lang: str) -> Dict[str, dict]:
    """从 api/protreptic.db 读全部场景（按 code 索引，英/中各自取本语言字段）。"""
    db = _find_db()
    con = sqlite3.connect('file:%s?mode=ro' % db, uri=True)
    try:
        rows = con.execute(
            'SELECT code, name_zh, name_en, description_zh, description_en, '
            'reason_zh, reason_en, steps_zh, steps_en, expected_zh, expected_en, '
            'case_zh, case_en, modes, era, historical_domains, domains FROM figures'
        ).fetchall()
    finally:
        con.close()

    zh_first = (lang == 'zh')
    out: Dict[str, dict] = {}
    for (code, nz, ne, dz, de, rz, re_, sz, se, ez, ee, cz, ce,
         modes, era, hd, dm) in rows:
        code = str(code or '').strip()
        if not code:
            continue
        name = ((nz or ne) if zh_first else (ne or nz)) or code
        out[code] = {
            'code': code,
            # 标准字段（本语言优先，缺则退到另一语言，再缺退到 code）
            'name': str(name).strip() or code,
            'description': str(((dz or de) if zh_first else (de or dz)) or '').strip(),
            'reason': str(((rz or re_) if zh_first else (re_ or rz)) or '').strip(),
            'steps': _as_list(sz if zh_first else se),
            'expected': _as_list(ez if zh_first else ee),
            'case': str(((cz or ce) if zh_first else (ce or cz)) or '').strip(),
            # 双语原值（测试/对比用，不写死数量）
            'name_zh': str(nz or '').strip(),
            'name_en': str(ne or '').strip(),
            # 语义字段
            'modes': _as_list(modes),
            'era': str(era or '').strip(),
            'historical_domains': _as_list(hd),
            'domains': _as_list(dm),
        }
    return out


MODES_DATA = load_json('modes_data.json')
# Filter out M-prefixed keys (legacy format) - only numeric keys can be converted to int
zh_modes_numeric = {k: v for k, v in MODES_DATA['zh'].items() if not k.startswith('M')}
en_modes_numeric = {k: v for k, v in MODES_DATA['en'].items() if not k.startswith('M')}
THINKING_MODES_ZH = {int(k): ThinkingMode(int(k), *v) for k, v in zh_modes_numeric.items()}
THINKING_MODES_EN = {int(k): ThinkingMode(int(k), *v) for k, v in en_modes_numeric.items()}

SCENARIOS_ZH = load_scenarios('zh')
SCENARIOS_EN = load_scenarios('en')

# code → 名称：由唯一数据源派生（不再读 tools/code_maps.json 这份派生副本）
CODE_MAP = {c: (s['name_zh'] or s['name']) for c, s in SCENARIOS_ZH.items()}
CODE_MAP_EN = {c: (s['name_en'] or s['name']) for c, s in SCENARIOS_EN.items()}

# 标签：同样由数据源派生（era / historical_domains / domains），不读陈旧副本
SCENARIO_TAGS = {
    c: {
        'era': s['era'],
        'historical_domains': s['historical_domains'],
        'domains': s['domains'],
    }
    for c, s in SCENARIOS_ZH.items()
}


class ThinkingModeSelector:
    def __init__(self, lang: str = "zh"):
        self.lang = lang.lower()
        self.scenarios = SCENARIOS_ZH if self.lang == "zh" else SCENARIOS_EN
        self.code_map = CODE_MAP if self.lang == "zh" else CODE_MAP_EN
        self.modes = THINKING_MODES_ZH if self.lang == "zh" else THINKING_MODES_EN

    def _mode_name(self, m: Any) -> str:
        """模式引用 → 名称。db 里的引用可能是 int、'M218' 或目录中不存在的旧 id，
        解析不到就退回引用本身的字符串（不让 CLI 因 KeyError 崩）。"""
        mm = self.modes.get(m)
        if mm is None and isinstance(m, str) and m.isdigit():
            mm = self.modes.get(int(m))
        return mm.name if mm else str(m)

    def _get_field(self, scenario: dict, field: str) -> Any:
        """Get field value handling both standard and i18n formats."""
        lang = self.lang
        # Try standard field first
        if field in scenario:
            return scenario[field]
        # Try i18n field
        i18n_field = f"{field}_{lang}"
        if i18n_field in scenario:
            return scenario[i18n_field]
        # Try alternative i18n field names
        alt_fields = {
            'name': ['name_zh', 'name_en', 'core_mode'],
            'description': ['description_zh', 'description_en', 'core_mode'],
            'reason': ['reason_zh', 'reason_en', 'mode'],
            'steps': ['steps_zh', 'steps_en'],
            'expected': ['expected_zh', 'expected_en'],
            'case': ['case_zh', 'case_en'],
        }
        for alt in alt_fields.get(field, []):
            if alt in scenario:
                return scenario[alt]
        return ""

    def list_scenarios(self):
        if self.lang == "zh":
            print("\n📋 思维模式选择器 - 全部处境场景\n")
            print("=" * 60)
            categories = {
                        "A": "🎯 方向性问题（何去何从）",
                        "B": "💡 突破性问题（如何突围）",
                        "C": "👥 人相关问题（如何共事）",
                        "D": "⏳ 长期性问题（如何持久）",
                        "H": "🏛️ 历史人物思维模式（古今通鉴）",
                        "M": "🏛️ 毛泽东分阶段思维模式（体系化纲领工程化）"
                    }
        else:
            print("\n📋 Thinking Mode Selector - All Scenarios\n")
            print("=" * 60)
            categories = {
                "A": "🎯 Directional (Where to Go)",
                "B": "💡 Breakthrough (How to Break Out)",
                "C": "👥 People (How to Work Together)",
                "D": "⏳ Long-Term (How to Last)",
                "H": "🏛️ Historical Figures (Ancient Wisdom for Modern Times)",
                "M": "🏛️ Mao Zedong Phased Thinking (Systematic Program Engineering)"
            }

        for cat_code, cat_name in categories.items():
            print(f"\n{cat_name}")
            print("-" * 40)
            for code in sorted(self.scenarios.keys()):
                if code.startswith(cat_code + "-"):
                    name = self._get_field(self.scenarios[code], "name")
                    modes = ", ".join([self._mode_name(m) for m in self.scenarios[code]["modes"][:3]])
                    more = "..." if len(self.scenarios[code]["modes"]) > 3 else ""
                    print(f"  {code:<12} {name} [{modes}{more}]")
        print()

    def search_scenarios(self, keyword: str):
        keyword_lower = keyword.lower()
        results = []
        for code, scenario in self.scenarios.items():
            # Skip non-dict entries (metadata fields)
            if not isinstance(scenario, dict):
                continue
            name = self._get_field(scenario, "name").lower()
            reason = self._get_field(scenario, "reason").lower()
            # Handle modes that may not be in self.modes (e.g., M-prefixed legacy modes)
            modes_str_parts = [self._mode_name(m).lower() for m in scenario["modes"]]
            modes_str = " ".join(modes_str_parts)
            if (keyword_lower in name or
                keyword_lower in reason or
                keyword_lower in modes_str or
                keyword_lower in code.lower()):
                results.append((code, self._get_field(scenario, "name")))

        if self.lang == "zh":
            print(f"\n🔍 搜索 '{keyword}' 的结果：\n")
        else:
            print(f"\n🔍 Search results for '{keyword}':\n")

        if results:
            for code, name in results:
                print(f"  {code} - {name}")
        else:
            if self.lang == "zh":
                print("  未找到匹配场景")
            else:
                print("  No matching scenarios found")
        print()

    def filter_by_tag(self, tag_filter: str):
        """Filter scenarios by tag. Format: key=value or just key"""
        if not SCENARIO_TAGS:
            if self.lang == "zh":
                print("⚠️ 标签数据未加载，请先运行 generate_tags.py")
            else:
                print("⚠️ Tags data not loaded, please run generate_tags.py first")
            return

        # Parse filter
        if '=' in tag_filter:
            key, value = tag_filter.split('=', 1)
            key = key.strip()
            value = value.strip()
        else:
            key = tag_filter.strip()
            value = None

        results = []
        for code, tags in SCENARIO_TAGS.items():
            if code in self.scenarios:
                if key in tags:
                    tag_value = tags[key]
                    # Handle both list and scalar values
                    if value is None:
                        results.append((code, self._get_field(self.scenarios[code], "name")))
                    elif isinstance(tag_value, list):
                        if value in tag_value:
                            results.append((code, self._get_field(self.scenarios[code], "name")))
                    elif tag_value == value:
                        results.append((code, self._get_field(self.scenarios[code], "name")))

        if self.lang == "zh":
            print(f"\n🏷️ 按标签筛选 '{tag_filter}' 的结果：\n")
        else:
            print(f"\n🏷️ Filter by tag '{tag_filter}' results:\n")

        if results:
            for code, name in results:
                print(f"  {code} - {name}")
        else:
            if self.lang == "zh":
                print("  未找到匹配场景")
            else:
                print("  No matching scenarios found")
        print()

    def _query_figure_fallback(self, code: str) -> bool:
        """从 figure_library（人物专属模式库）查询。找到则打印并返回 True。"""
        try:
            from figure_library import FigureLibrary
        except Exception:
            return False
        try:
            lib = FigureLibrary(lang=self.lang)
        except Exception:
            return False
        # 先按人物代码查
        fig = lib.figure(code)
        if fig:
            print(lib.show_figure(code))
            return True
        # 再按模式代码查
        m = lib.mode(code)
        if m:
            print(lib.show_mode(code))
            return True
        return False

    def query_code(self, code: str):
        code = code.upper().strip()
        if code not in self.scenarios:
            # 回退：尝试从 figure_library（2858 条人物专属模式）查询
            if self._query_figure_fallback(code):
                return
            if self.lang == "zh":
                print(f"⚠️ 未找到代码: {code}")
                print("可用代码: " + ", ".join(sorted(self.scenarios.keys())))
            else:
                print(f"⚠️ Code not found: {code}")
                print("Available codes: " + ", ".join(sorted(self.scenarios.keys())))
            return

        scenario = self.scenarios[code]
        name = self._get_field(scenario, "name")
        mode_names = [self._mode_name(m) for m in scenario["modes"]]
        reason = self._get_field(scenario, "reason")
        steps = self._get_field(scenario, "steps")
        expected = self._get_field(scenario, "expected")
        case = self._get_field(scenario, "case")

        if self.lang == "zh":
            print(f"\n{'='*60}")
            print(f"📍 处境代码: {code} - {name}")
            print(f"{'='*60}")
            print(f"\n🧠 推荐思维模式组合 ({len(mode_names)} 种):")
            for i, mode in enumerate(mode_names, 1):
                print(f"  {i}. {mode}")
            print(f"\n💡 推荐理由:")
            print(f"  {reason}")
            print(f"\n📋 分步操作指南:")
            for step in steps:
                print(f"  {step}")
            print(f"\n✅ 预期效果:")
            for exp in expected:
                print(f"  {exp}")
            print(f"\n📖 实战案例:")
            print(f"  {case}")
            print(f"{'='*60}\n")
        else:
            print(f"\n{'='*60}")
            print(f"📍 Situation Code: {code} - {name}")
            print(f"{'='*60}")
            print(f"\n🧠 Recommended Thinking Modes ({len(mode_names)}):")
            for i, mode in enumerate(mode_names, 1):
                print(f"  {i}. {mode}")
            print(f"\n💡 Rationale:")
            print(f"  {reason}")
            print(f"\n📋 Step-by-Step Guide:")
            for step in steps:
                print(f"  {step}")
            print(f"\n✅ Expected Outcomes:")
            for exp in expected:
                print(f"  {exp}")
            print(f"\n📖 Case Example:")
            print(f"  {case}")
            print(f"{'='*60}\n")

    def export_result(self, code: str, format: str = "json") -> str:
        scenario_name = self.code_map.get(code, "Unknown Scenario" if self.lang == "en" else "未知场景")
        scenario = self.scenarios.get(code)
        if not scenario:
            return f"⚠️ No preset for ({code})" if self.lang == "en" else f"⚠️ 该组合 ({code}) 暂无预设方案"

        mode_names = [self._mode_name(m) for m in scenario["modes"]]

        if format == "json":
            import json
            export_data = {
                "code": code,
                "name": self._get_field(scenario, "name"),
                "modes": mode_names,
                "reason": self._get_field(scenario, "reason"),
                "steps": self._get_field(scenario, "steps"),
                "expected": self._get_field(scenario, "expected"),
                "case": self._get_field(scenario, "case")
            }
            return json.dumps(export_data, ensure_ascii=False, indent=2)
        elif format == "md":
            lines = [
                f"# {scenario_name} ({code})",
                "",
                f"## 🧠 Recommended Thinking Modes ({len(mode_names)})" if self.lang == "en" else f"## 🧠 推荐思维模式组合 ({len(mode_names)})",
            ]
            for i, mode in enumerate(mode_names, 1):
                lines.append(f"{i}. {mode}")
            lines.append("")
            lines.append("## 💡 Rationale" if self.lang == "en" else "## 💡 推荐理由")
            lines.append(scenario["reason"])
            lines.append("")
            lines.append("## 📋 Steps" if self.lang == "en" else "## 📋 分步操作指南")
            for step in scenario["steps"]:
                lines.append(f"- {step}")
            lines.append("")
            lines.append("## ✅ Expected Outcome" if self.lang == "en" else "## ✅ 预期效果")
            for exp in scenario["expected"]:
                lines.append(f"- {exp}")
            lines.append("")
            lines.append("## 📖 Case Example" if self.lang == "en" else "## 📖 实战案例")
            lines.append(scenario["case"])
            return "\n".join(lines)
        return ""

    def export_all(self, format: str = "json") -> str:
        if format == "json":
            import json
            all_data = {}
            for code, scenario in self.scenarios.items():
                # Skip non-dict entries (metadata fields)
                if not isinstance(scenario, dict):
                    continue
                mode_names = [self._mode_name(m) for m in scenario["modes"]]
                all_data[code] = {
                    "name": self._get_field(scenario, "name"),
                    "modes": mode_names,
                    "reason": self._get_field(scenario, "reason"),
                    "steps": self._get_field(scenario, "steps"),
                    "expected": self._get_field(scenario, "expected"),
                    "case": self._get_field(scenario, "case")
                }
            return json.dumps(all_data, ensure_ascii=False, indent=2)
        elif format == "md":
            lines = ["# All Scenarios" if self.lang == "en" else "# 所有场景", ""]
            categories = {
                "A": "Directional (Where to Go)" if self.lang == "en" else "方向性问题（何去何从）",
                "B": "Breakthrough (How to Break Out)" if self.lang == "en" else "突破性问题（如何突围）",
                "C": "People (How to Work Together)" if self.lang == "en" else "人相关问题（如何共事）",
                "D": "Long-Term (How to Last)" if self.lang == "en" else "长期性问题（如何持久）",
                "H": "Historical Figures (Ancient Wisdom)" if self.lang == "en" else "历史人物思维模式（古今通鉴）"
            }
            for cat_code, cat_name in categories.items():
                lines.append(f"## {cat_name}")
                lines.append("")
                for code in sorted(self.scenarios.keys()):
                    if code.startswith(cat_code + "-"):
                        scenario = self.scenarios[code]
                        # Skip non-dict entries (metadata fields)
                        if not isinstance(scenario, dict):
                            continue
                        mode_names = [self._mode_name(m) for m in scenario["modes"]]
                        lines.append(f"### {self._get_field(scenario, 'name')} ({code})")
                        lines.append("")
                        lines.append(f"**Modes:** {', '.join(mode_names)}")
                        lines.append("")
                        lines.append(f"**Rationale:** {self._get_field(scenario, 'reason')}" if self.lang == "en" else f"**推荐理由:** {self._get_field(scenario, 'reason')}")
                        lines.append("")
                        lines.append("**Steps:**" if self.lang == "en" else "**步骤:**")
                        for step in self._get_field(scenario, "steps"):
                            lines.append(f"- {step}")
                        lines.append("")
                        lines.append(f"**Expected:** {self._get_field(scenario, 'expected')}" if self.lang == "en" else f"**预期:** {self._get_field(scenario, 'expected')}")
                        lines.append("")
                        lines.append(f"**Case:** {self._get_field(scenario, 'case')}" if self.lang == "en" else f"**案例:** {self._get_field(scenario, 'case')}")
                        lines.append("")
            return "\n".join(lines)
        return ""

    def interactive_diagnosis(self):
        if self.lang == "zh":
            print("\n🧭 思维模式选择器 - 交互式诊断")
            print("回答 4 个问题，获得推荐思维模式组合\n")
            print("问题 1: 问题属于哪一类？")
            print("  A) 方向性 - 何去何从（战略、投资、谈判）")
            print("  B) 突破性 - 如何突围（创新、攻坚、迭代）")
            print("  C) 人相关 - 如何共事（团队、领导、冲突、关系）")
            print("  D) 长期性 - 如何持久（成长、组织、危机、生死）\n")
            cat = input("请选择 [A/B/C/D]: ").strip().upper()
            while cat not in ["A", "B", "C", "D"]:
                cat = input("请输入 A/B/C/D: ").strip().upper()

            print("\n问题 2: 不确定性程度？")
            print("  1) 高 - 变量多、信息少、难预测")
            print("  2) 中 - 部分已知、有历史参考")
            print("  3) 低 - 规则明确、环境稳定\n")
            unc = input("请选择 [1/2/3]: ").strip()
            while unc not in ["1", "2", "3"]:
                unc = input("请输入 1/2/3: ").strip()

            print("\n问题 3: 目标特征？")
            print("  X) 单一明确目标")
            print("  Y) 多目标需平衡")
            print("  Z) 生死存亡/底线目标\n")
            obj = input("请选择 [X/Y/Z]: ").strip().upper()
            while obj not in ["X", "Y", "Z"]:
                obj = input("请输入 X/Y/Z: ").strip().upper()

            print("\n问题 4: 你的态势？")
            print("  P) 进攻 - 主动出击、争取主动")
            print("  R) 防守 - 守住底线、求稳防险")
            print("  S) 探索 - 试错学习、寻找路径")
            print("  Q) 治理 - 设计规则、长期机制\n")
            stance = input("请选择 [P/R/S/Q]: ").strip().upper()
            while stance not in ["P", "R", "S", "Q"]:
                stance = input("请输入 P/R/S/Q: ").strip().upper()

            code = f"{cat}-{unc}-{obj}-{stance}"
            print()
            self.query_code(code)
        else:
            print("\n🧭 Thinking Mode Selector - Interactive Diagnosis")
            print("Answer 4 questions to get recommended thinking mode combination\n")
            print("Question 1: What category is the problem?")
            print("  A) Directional - Where to go (Strategy, Investment, Negotiation)")
            print("  B) Breakthrough - How to break out (Innovation, Breakthrough, Iteration)")
            print("  C) People - How to work together (Team, Leadership, Conflict, Relations)")
            print("  D) Long-Term - How to last (Growth, Organization, Crisis, Life/Death)\n")
            cat = input("Select [A/B/C/D]: ").strip().upper()
            while cat not in ["A", "B", "C", "D"]:
                cat = input("Enter A/B/C/D: ").strip().upper()

            print("\nQuestion 2: Uncertainty level?")
            print("  1) High - Many variables, little info, hard to predict")
            print("  2) Medium - Partially known, some historical reference")
            print("  3) Low - Clear rules, stable environment\n")
            unc = input("Select [1/2/3]: ").strip()
            while unc not in ["1", "2", "3"]:
                unc = input("Enter 1/2/3: ").strip()

            print("\nQuestion 3: Objective characteristic?")
            print("  X) Single clear objective")
            print("  Y) Multiple objectives to balance")
            print("  Z) Life-or-death / bottom-line objective\n")
            obj = input("Select [X/Y/Z]: ").strip().upper()
            while obj not in ["X", "Y", "Z"]:
                obj = input("Enter X/Y/Z: ").strip().upper()

            print("\nQuestion 4: Your stance?")
            print("  P) Offensive - Proactive, seize initiative")
            print("  R) Defensive - Hold bottom line, seek stability")
            print("  S) Exploratory - Trial and error, find path")
            print("  Q) Governance - Design rules, long-term mechanism\n")
            stance = input("Select [P/R/S/Q]: ").strip().upper()
            while stance not in ["P", "R", "S", "Q"]:
                stance = input("Enter P/R/S/Q: ").strip().upper()

            code = f"{cat}-{unc}-{obj}-{stance}"
            print()
            self.query_code(code)


import argparse


def main():
    parser = argparse.ArgumentParser(
        description="思维模式选择器 / Thinking Mode Selector",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("-c", "--code", help="直接查询处境代码 / Query situation code directly")
    parser.add_argument("-l", "--list", action="store_true", help="列出所有场景 / List all scenarios")
    parser.add_argument("-s", "--search", help="搜索场景关键词 / Search scenario keyword")
    parser.add_argument("-t", "--tag", help="按标签筛选 / Filter by tag (key=value or key)")
    parser.add_argument("-e", "--export", choices=["json", "md"], help="导出格式 / Export format")
    parser.add_argument("-o", "--output", help="输出文件路径 / Output file path")
    parser.add_argument("--lang", choices=["zh", "en"], default="zh", help="输出语言 / Output language (default: zh)")
    args = parser.parse_args()

    selector = ThinkingModeSelector(lang=args.lang)

    if args.code:
        if args.export:
            result = selector.export_result(args.code, args.export)
            if args.output:
                with open(args.output, "w", encoding="utf-8") as f:
                    f.write(result)
                msg = f"已导出到 {args.output}" if args.lang == "zh" else f"Exported to {args.output}"
                print(msg)
            else:
                print(result)
        else:
            selector.query_code(args.code)
    elif args.list:
        selector.list_scenarios()
    elif args.search:
        selector.search_scenarios(args.search)
    elif args.tag:
        selector.filter_by_tag(args.tag)
    elif args.export:
        result = selector.export_all(args.export)
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(result)
            msg = f"已导出到 {args.output}" if args.lang == "zh" else f"Exported to {args.output}"
            print(msg)
        else:
            print(result)
    else:
        selector.interactive_diagnosis()


if __name__ == "__main__":
    main()