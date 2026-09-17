#!/usr/bin/env python3
"""figure_library.py — 历史人物思维模式库查询工具

把 Protreptic 的核心资产（data/modes_data.json，285 位历史人物 × 每人 10 条
专属思维模式 = 2868 条）接入可查询的产品层。

用法:
    python figure_library.py -L                      # 列出全部历史人物
    python figure_library.py -f H-INM-001            # 查看某人的 10 条思维模式
    python figure_library.py -m M-DKR-009            # 查看单条模式详情
    python figure_library.py -s 矛盾                  # 按关键词搜索模式
    python figure_library.py -c 军事战略              # 按类目列出模式
    python figure_library.py -f H-INM-001 -e json    # 导出为 JSON
    python figure_library.py --lang en -f H-INM-001  # 英文输出
    python figure_library.py --stats                 # 库统计

可作为模块导入:
    from figure_library import FigureLibrary
    lib = FigureLibrary()
    lib.figure('H-INM-001')      # 返回 dict
    lib.search('矛盾')           # 返回 list[dict]
"""

import sys
import json
import re
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Any

# ── 数据路径解析：优先仓库根 data/modes_data.json ──────────────────────────
def _find_data_file() -> Path:
    here = Path(__file__).resolve().parent
    candidates = [
        here.parent / "data" / "modes_data.json",   # <repo>/tools/ -> <repo>/data/
        here / "json" / "modes_data_full.json",
        here / "modes_data.json",
        Path.cwd() / "data" / "modes_data.json",
    ]
    for c in candidates:
        if c.exists() and c.stat().st_size > 100_000:
            return c
    raise FileNotFoundError(
        "找不到 data/modes_data.json（核心资产文件）。"
        f"已尝试: {[str(c) for c in candidates]}"
    )


class FigureLibrary:
    """历史人物思维模式库查询接口。"""

    def __init__(self, data_file: Optional[str] = None, lang: str = "zh"):
        self.lang = lang.lower()
        path = Path(data_file) if data_file else _find_data_file()
        self.data_path = path
        raw = json.loads(path.read_text(encoding="utf-8"))
        self.modes: List[dict] = raw.get("modes", [])
        self._by_mode_code = {}
        self._by_figure = {}
        self._figure_names = {}
        self._load_figure_names()
        self._build_index()

    def _load_figure_names(self):
        """建立 figure_code -> 人物名 映射（多源）。"""
        # 源0: 预生成的映射表 data/figure_names.json
        fn = self.data_path.parent / "figure_names.json"
        if fn.exists():
            try:
                self._figure_names.update(json.loads(fn.read_text(encoding="utf-8")))
            except Exception:
                pass
        # 源1: data/figures/*.json
        figs_dir = self.data_path.parent / "figures"
        if figs_dir.is_dir():
            for f in figs_dir.glob("*.json"):
                try:
                    d = json.loads(f.read_text(encoding="utf-8"))
                except Exception:
                    continue
                name = d.get("figure_name") or d.get("figure_name_zh") or d.get("name_zh") or d.get("name")
                if not name:
                    continue
                for code in (f.stem, str(d.get("figure_code") or ""), str(d.get("code") or "")):
                    if code:
                        self._figure_names.setdefault(code, str(name))
                        self._figure_names.setdefault(code.upper(), str(name))

    def _figure_name(self, fc: str, sample_mode: dict) -> str:
        """解析人物显示名：映射表 → figures 目录 → 模式内嵌字段 → 短码别名。"""
        if fc in self._figure_names:
            return self._figure_names[fc]
        up = fc.upper()
        if up in self._figure_names:
            return self._figure_names[up]
        # H-XXX-001 -> XXX 短码
        m = re.match(r"^[A-Z]{2}-([A-Z0-9]+)-\d+$", up)
        if m and m.group(1) in self._figure_names:
            return self._figure_names[m.group(1)]
        for cand in (f"{fc}-001", f"{up}-001"):
            if cand in self._figure_names:
                return self._figure_names[cand]
        for k in ("figure_name_zh", "figure_name"):
            v = sample_mode.get(k)
            if isinstance(v, str) and v:
                return v
        return ""

    @staticmethod
    def _pick_name(v: Any) -> str:
        """name_zh 可能是 str 或 list，统一取字符串。"""
        if isinstance(v, list):
            return str(v[0]) if v else ""
        return str(v) if v else ""

    def _build_index(self):
        for m in self.modes:
            mc = str(m.get("mode_code") or "")
            fc = str(m.get("figure_code") or "")
            if mc:
                self._by_mode_code[mc] = m
            if fc:
                self._by_figure.setdefault(fc, []).append(m)
        # 人物内模式按 mode_code 排序
        for fc in self._by_figure:
            self._by_figure[fc].sort(key=lambda x: str(x.get("mode_code", "")))

    # ── 查询 API ──────────────────────────────────────────────────────────
    def figures(self) -> List[str]:
        """全部人物 code。"""
        return sorted(self._by_figure.keys())

    def figure(self, code: str) -> Optional[dict]:
        """取某位人物的全部模式。返回 {'code', 'name', 'count', 'modes':[...]}。"""
        code = code.upper().strip()
        ms = self._by_figure.get(code)
        if not ms:
            # 容错：允许模糊匹配（如 INM 匹配 H-INM-001）
            hits = [c for c in self._by_figure if code in c.upper()]
            if len(hits) == 1:
                code, ms = hits[0], self._by_figure[hits[0]]
            else:
                return None
        name = self._figure_name(code, ms[0])
        return {
            "code": code,
            "name": name,
            "count": len(ms),
            "modes": ms,
        }

    def mode(self, code: str) -> Optional[dict]:
        """按 mode_code 取单条模式。"""
        return self._by_mode_code.get(code.upper().strip())

    def search(self, keyword: str) -> List[dict]:
        """按关键词搜索（名称/定义/概念/类目）。"""
        kw = keyword.lower()
        out = []
        for m in self.modes:
            blob = " ".join(str(m.get(f, "")) for f in (
                "name_zh", "name_en", "definition_zh", "definition_en",
                "category", "category_raw", "domain_zh", "key_concepts",
            ))
            if kw in blob.lower():
                out.append(m)
        return out

    def by_category(self, cat: str) -> List[dict]:
        cat = cat.strip()
        return [m for m in self.modes if str(m.get("category", "")) == cat
                or cat in str(m.get("category_raw", ""))]

    def stats(self) -> dict:
        from collections import Counter
        figs = Counter()
        cats = Counter()
        for m in self.modes:
            if m.get("figure_code"):
                figs[m["figure_code"]] += 1
            cats[str(m.get("category", "?"))] += 1
        return {
            "total_modes": len(self.modes),
            "total_figures": len(figs),
            "categories": dict(cats.most_common()),
        }

    # ── 展示层 ────────────────────────────────────────────────────────────
    def _f(self, m: dict, base: str) -> Any:
        """取字段，按语言回退。"""
        if self.lang == "en":
            v = m.get(base + "_en")
            return v if v else m.get(base + "_zh", "")
        v = m.get(base + "_zh")
        return v if v else m.get(base + "_en", "")

    def render_mode(self, m: dict, index: Optional[int] = None) -> str:
        """渲染单条模式为文本块。"""
        zh = self.lang == "zh"
        name = self._pick_name(m.get("name_zh")) if zh else (self._pick_name(m.get("name_en")) or self._pick_name(m.get("name_zh")))
        lines = []
        prefix = f"{index}. " if index else ""
        lines.append(f"{prefix}【{name}】 ({m.get('mode_code','')})")
        cat = m.get("category", "")
        dom = self._f(m, "domain")
        if cat:
            lines.append(f"   类目: {cat}" + (f" · 领域: {dom}" if dom else ""))
        d = self._f(m, "definition")
        if d:
            lines.append(f"   定义: {d}")
        proc = self._f(m, "process")
        if isinstance(proc, list) and proc:
            lines.append("   步骤:")
            for s in proc:
                lines.append(f"     - {s}")
        elif isinstance(proc, str) and proc:
            lines.append(f"   步骤: {proc}")
        kc = m.get("key_concepts")
        if isinstance(kc, list) and kc:
            lines.append(f"   关键概念: {' / '.join(map(str, kc))}")
        src = m.get("source_chapter")
        if src:
            lines.append(f"   出处: {src}")
        q = self._f(m, "key_quote")
        if q:
            lines.append(f"   原话: {q}")
        cases = self._f(m, "representative_cases")
        if isinstance(cases, list) and cases:
            lines.append(f"   史实案例: {'；'.join(map(str, cases))}")
        elif isinstance(cases, str) and cases:
            lines.append(f"   史实案例: {cases}")
        app = self._f(m, "modern_applications")
        if isinstance(app, list) and app:
            lines.append(f"   现代应用: {'；'.join(map(str, app))}")
        elif isinstance(app, str) and app:
            lines.append(f"   现代应用: {app}")
        return "\n".join(lines)

    def show_figure(self, code: str) -> str:
        fig = self.figure(code)
        if not fig:
            return f"⚠️  未找到人物代码: {code}\n提示: 用 -L 列出全部人物"
        zh = self.lang == "zh"
        lines = [""]
        lines.append("=" * 64)
        head = f"🏛️  {fig['name'] or fig['code']}  ({fig['code']})  —  {fig['count']} 条思维模式"
        lines.append(head)
        lines.append("=" * 64)
        for i, m in enumerate(fig["modes"], 1):
            lines.append("")
            lines.append(self.render_mode(m, index=i))
        lines.append("")
        lines.append("=" * 64)
        return "\n".join(lines)

    def show_mode(self, code: str) -> str:
        m = self.mode(code)
        if not m:
            return f"⚠️  未找到模式代码: {code}"
        return "\n" + self.render_mode(m) + "\n"

    def list_figures(self) -> str:
        zh = self.lang == "zh"
        figs = self.figures()
        lines = ["", f"📚 历史人物库 — 共 {len(figs)} 位", "=" * 64]
        for fc in figs:
            ms = self._by_figure[fc]
            name = self._figure_name(fc, ms[0])
            sample = self._pick_name(ms[0].get("name_zh"))
            lines.append(f"  {fc:<16} {(name or '(人物)'):<10} {len(ms):>2}条  例: {sample}")
        lines.append("")
        return "\n".join(lines)


# ── CLI ───────────────────────────────────────────────────────────────────
def main(argv=None):
    p = argparse.ArgumentParser(
        description="Protreptic 历史人物思维模式库查询工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("-L", "--list", action="store_true", help="列出全部历史人物")
    p.add_argument("-f", "--figure", metavar="CODE", help="查看某人物的全部思维模式")
    p.add_argument("-m", "--mode", metavar="CODE", help="查看单条模式详情")
    p.add_argument("-s", "--search", metavar="KW", help="按关键词搜索模式")
    p.add_argument("-c", "--category", metavar="CAT", help="按类目列出模式")
    p.add_argument("-e", "--export", choices=["json"], help="导出为 JSON")
    p.add_argument("--lang", default="zh", choices=["zh", "en"], help="输出语言")
    p.add_argument("--stats", action="store_true", help="显示库统计")
    p.add_argument("--data", metavar="PATH", help="指定数据文件路径")
    args = p.parse_args(argv)

    lib = FigureLibrary(data_file=args.data, lang=args.lang)

    if args.stats:
        s = lib.stats()
        print(f"\n📊 Protreptic 思维模式库统计")
        print(f"   模式总数: {s['total_modes']}")
        print(f"   人物总数: {s['total_figures']}")
        print(f"   类目分布:")
        for k, v in s["categories"].items():
            print(f"     {k}: {v}")
        print()
        return 0

    if args.list:
        print(lib.list_figures())
        return 0

    if args.figure:
        code = args.figure.upper()
        if args.export == "json":
            fig = lib.figure(code)
            if not fig:
                print(json.dumps({"error": f"未找到 {code}"}, ensure_ascii=False))
                return 1
            print(json.dumps(fig, ensure_ascii=False, indent=2))
        else:
            print(lib.show_figure(code))
        return 0

    if args.mode:
        code = args.mode.upper()
        m = lib.mode(code)
        if not m:
            print(f"⚠️  未找到模式: {code}")
            return 1
        if args.export == "json":
            print(json.dumps(m, ensure_ascii=False, indent=2))
        else:
            print(lib.show_mode(code))
        return 0

    if args.search:
        hits = lib.search(args.search)
        print(f"\n🔍 搜索 '{args.search}' — {len(hits)} 条\n")
        for m in hits[:30]:
            fc = m.get("figure_code", "")
            fname = lib._figure_name(str(fc), m)
            print(f"  {m.get('mode_code',''):<18} {lib._pick_name(m.get('name_zh'))}  [{fc} {fname}]")
        if len(hits) > 30:
            print(f"  ... 还有 {len(hits)-30} 条")
        print()
        return 0

    if args.category:
        hits = lib.by_category(args.category)
        print(f"\n📂 类目 '{args.category}' — {len(hits)} 条\n")
        for m in hits[:40]:
            print(f"  {m.get('mode_code',''):<18} {lib._pick_name(m.get('name_zh'))}")
        if len(hits) > 40:
            print(f"  ... 还有 {len(hits)-40} 条")
        print()
        return 0

    p.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
