#!/usr/bin/env python3
"""test_credibility_d45.py -- D4/D5 真实现的自测（Phase40-Z2，铁律：机检规则必须有负对照）。

为什么有这个文件
    船长 2026-09-20 独立核验发现：tools/credibility_gate.py 的 D4/D5 是**空壳**
    （D4 只判「有引文但出处为空」；D5 直接 return []），而方案文档把它们列成「已实现检查」。
    Phase40-Z2 把两者改成真检查，本自测钉住它们的「有牙」语义与「不误报」边界：

    A  D5 矛盾样本（年份晚于卒年 + 与人物名同现 + 本人叙述字段）-> 必须判 conflict
    B  D5 干净样本（年份落在生卒年之间）-> 必须 clean，且不产生矛盾
    C  D5 误报控制①：年份落在生卒年外但**不与人物名同现**（背景/他人事件）-> 不得判 conflict
    D  D5 误报控制②：年份落在生卒年外但上下文含「后世/卒后」类余波标记 -> 不得判 conflict
    E  D5 误报控制③：年份落在生卒年外但离生卒年过远（对照/现代年份）-> 不得判 conflict
    F  D5 不可判定：人物无生卒年 -> status=undetermined 且 reason 明确（不静默放过）
    G  D5 生卒年解析：int / "1805" / "约前287" / "-356" 四种形态都要能解析（解析不了返回 None）
    H  D4 不符样本：引文片段不在缓存原文里（coverage=single-page）-> 必须判 mismatch
    I  D4 干净样本：引文片段在缓存原文里 -> 必须判 matched，不得报不符
    J  D4 误报控制：缓存 coverage=partial（只抓到部分篇章）-> 必须 unchecked，**不得判 mismatch**
    K  D4 不可核：出处引文没有缓存条目 -> unchecked 且 reason 明确
    L  端到端：负对照夹具跑 gate（--data-path 指向夹具）-> D4 mismatch / D5 conflict 必须出现在
       报告的 warnings 明细里，干净夹具不出现

用法：python3 tools/test_credibility_d45.py    （全过 exit 0，任一失败 exit 1）
"""

from __future__ import annotations

import importlib.util
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
GATE_SRC = REPO_ROOT / "tools" / "credibility_gate.py"
CACHE_SRC = REPO_ROOT / "tools" / "source_text_cache.py"
LINKIDX_SRC = REPO_ROOT / "tools" / "source_link_index.py"
QUARANTINE_SRC = REPO_ROOT / "tools" / "_quarantine.py"


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


GATE = load_module("gate_under_test", GATE_SRC)
CACHE = load_module("cache_under_test", CACHE_SRC)

RESULTS = []


def check(name, cond, detail=""):
    RESULTS.append((name, bool(cond)))
    print("[%s] %s%s" % ("PASS" if cond else "FAIL", name,
                         ("  " + str(detail)) if (detail and not cond) else ""))


def lifespan(root, code="H-D45T-001", name="测试人物", birth=1610, death=1695):
    """在夹具仓里写一个 figure 文件。"""
    d = Path(root) / "data" / "figures"
    d.mkdir(parents=True, exist_ok=True)
    (d / (code + ".json")).write_text(json.dumps(
        {"figure_code": code, "figure_name": name, "birth_year": birth, "death_year": death,
         "era": "明末清初"}, ensure_ascii=False), encoding="utf-8")


def mode(**kw):
    base = {"mode_code": "M-D45T-001", "figure_code": "H-D45T-001", "figure_name": "测试人物",
            "definition_zh": "", "process_zh": "", "representative_cases_zh": "",
            "source_chapter": "", "key_quote_zh": ""}
    base.update(kw)
    return base


def write_cache_fixture(root, coverage="single-page", text="子曰学而时习之不亦说乎有朋自远方来不亦乐乎",
                        status="ok"):
    (Path(root) / "tools").mkdir(parents=True, exist_ok=True)
    (Path(root) / "tools" / "source_text_cache.py").write_text(CACHE_SRC.read_text(encoding="utf-8"),
                                                               encoding="utf-8")
    (Path(root) / "tools" / "source_link_index.py").write_text(LINKIDX_SRC.read_text(encoding="utf-8"),
                                                               encoding="utf-8")
    (Path(root) / "data" / "audit" / "source_texts").mkdir(parents=True, exist_ok=True)
    (Path(root) / "data" / "audit" / "source_texts" / "f.txt").write_text(text, encoding="utf-8")
    (Path(root) / "data" / "source_links.json").write_text(json.dumps(
        {"《论语》": {"url": "https://zh.wikisource.org/wiki/論語", "source_type": "wikisource",
                     "confidence": 0.9}}, ensure_ascii=False), encoding="utf-8")
    (Path(root) / "data" / "audit" / "source_texts.json").write_text(json.dumps({
        "schema": "protreptic.source_texts/v1",
        "entries": [{"key": "《论语》", "url": "https://zh.wikisource.org/wiki/論語",
                     "status": status, "coverage": coverage, "chars": len(text),
                     "file": "data/audit/source_texts/f.txt", "source_type": "wikisource"}],
    }, ensure_ascii=False), encoding="utf-8")


def main():
    tmp_root = Path(tempfile.mkdtemp(prefix="d45-fixture-"))
    tmp2 = Path(tempfile.mkdtemp(prefix="d45-cache-"))
    tmp3 = Path(tempfile.mkdtemp(prefix="d45-gate-"))
    try:
        # ---- A-F: D5 ----
        lifespan(tmp_root)
        life = GATE.load_figure_lifespans(tmp_root)
        check("G 生卒年解析（int/字符串/约前/负号）",
              GATE.parse_year_value(1610) == 1610
              and GATE.parse_year_value("1805") == 1805
              and GATE.parse_year_value("约前287") == -287
              and GATE.parse_year_value("-356") == -356
              and GATE.parse_year_value("不是年份") is None,
              "parse_year_value 结果不符")
        check("G2 夹具人物生卒年装载", "H-D45T-001" in life and life["H-D45T-001"]["death_year"] == 1695,
              life.get("H-D45T-001"))

        a = GATE.d5_scan(mode(representative_cases_zh="1699年测试人物主持重修书院，立规三条"),
                         life)
        check("A D5 矛盾样本必被检出", a["status"] == "conflict" and len(a["conflicts"]) == 1, a)
        check("A2 check_d5_timeline_conflict 返回警告文案",
              len(GATE.check_d5_timeline_conflict(
                  mode(representative_cases_zh="1699年测试人物主持重修书院，立规三条"), life)) == 1,
              "未产生警告")

        b = GATE.d5_scan(mode(representative_cases_zh="1644年测试人物主持重修书院"),
                         life)
        check("B D5 干净样本必须 clean（不误报）", b["status"] == "clean" and not b["conflicts"], b)

        c = GATE.d5_scan(mode(representative_cases_zh="1699年另一位学者主持重修书院"), life)
        check("C 误报控制①：年份不与人物名同现 -> 不判矛盾",
              c["status"] == "clean" and any("name-not-in-context" in x["reason"] for x in c["undetermined"]),
              c)

        d = GATE.d5_scan(mode(representative_cases_zh="测试人物身后的1699年，后人重修其书院"), life)
        check("D 误报控制②：余波标记 -> 不判矛盾",
              d["status"] == "clean" and any("afterlife-marker" in x["reason"] for x in d["undetermined"]),
              d)

        e = GATE.d5_scan(mode(representative_cases_zh="测试人物的方法在1950年的现代管理学界被重新发现"),
                         life)
        check("E 误报控制③：离生卒年过远 -> 不判矛盾",
              e["status"] == "clean" and any("out-of-window" in x["reason"] for x in e["undetermined"]),
              e)

        f = GATE.d5_scan(mode(figure_code="H-NO-LIFE", figure_name="无生卒年人物",
                              representative_cases_zh="1699年无生卒年人物主持重修书院"), life)
        check("F 无生卒年 -> undetermined 且理由明确",
              f["status"] == "undetermined" and f["reason"] == "no-lifespan-for-figure", f)

        # ---- H-K: D4 ----
        write_cache_fixture(tmp2, coverage="single-page")
        cache = GATE.make_cache(tmp2)
        li = GATE.load_link_index()
        h = GATE.d4_scan(mode(source_chapter="《论语·学而》", key_quote_zh="君子坦荡荡小人长戚戚"), cache, li)
        check("H D4 不符样本必被检出（mismatch）",
              h["status"] == "mismatch" and h["key"] == "《论语》", h)
        i = GATE.d4_scan(mode(source_chapter="《论语·学而》", key_quote_zh="有朋自远方来不亦乐乎"), cache, li)
        check("I D4 干净样本必须 matched（不误报）", i["status"] == "matched", i)

        tmp_partial = Path(tempfile.mkdtemp(prefix="d45-partial-"))
        write_cache_fixture(tmp_partial, coverage="partial")
        cache_p = GATE.make_cache(tmp_partial)
        j = GATE.d4_scan(mode(source_chapter="《论语·学而》", key_quote_zh="君子坦荡荡小人长戚戚"), cache_p, li)
        check("J 误报控制：coverage=partial -> 不可核（不得判 mismatch）",
              j["status"] == "unchecked" and "partial-coverage" in j["reason"], j)

        tmp_empty = Path(tempfile.mkdtemp(prefix="d45-empty-"))
        (tmp_empty / "data").mkdir(parents=True, exist_ok=True)
        (tmp_empty / "data" / "source_links.json").write_text(json.dumps(
            {"《论语》": {"url": "https://zh.wikisource.org/wiki/論語", "source_type": "wikisource"}},
            ensure_ascii=False), encoding="utf-8")
        (tmp_empty / "data" / "audit").mkdir(parents=True, exist_ok=True)
        (tmp_empty / "data" / "audit" / "source_texts.json").write_text(
            json.dumps({"entries": []}), encoding="utf-8")
        cache_e = GATE.make_cache(tmp_empty)
        k = GATE.d4_scan(mode(source_chapter="《论语·学而》", key_quote_zh="君子坦荡荡小人长戚戚"), cache_e, li)
        check("K 无缓存条目 -> unchecked 且理由明确",
              k["status"] == "unchecked" and k["reason"].startswith("cache-not-ok"), k)

        # ---- L: 端到端（夹具跑 gate，--data-path 指向夹具） ----
        (tmp3 / "tools").mkdir(parents=True, exist_ok=True)
        shutil.copy(GATE_SRC, tmp3 / "tools" / "credibility_gate.py")
        shutil.copy(CACHE_SRC, tmp3 / "tools" / "source_text_cache.py")
        shutil.copy(LINKIDX_SRC, tmp3 / "tools" / "source_link_index.py")
        shutil.copy(QUARANTINE_SRC, tmp3 / "tools" / "_quarantine.py")
        lifespan(tmp3, code="H-D45T-001", name="测试人物", birth=1610, death=1695)
        write_cache_fixture(tmp3, coverage="single-page")
        bad = {"modes": [mode(mode_code="M-D45T-BAD", source_chapter="《论语·学而》",
                              key_quote_zh="君子坦荡荡小人长戚戚",
                              representative_cases_zh="1699年测试人物主持重修书院")]}
        (tmp3 / "data" / "modes_data.json").write_text(json.dumps(bad, ensure_ascii=False), encoding="utf-8")
        proc = subprocess.run([sys.executable, "tools/credibility_gate.py",
                               "--data-path", str(tmp3 / "data" / "modes_data.json")],
                              cwd=str(tmp3), capture_output=True, text=True)
        out = proc.stdout + proc.stderr
        check("L 端到端：坏样本必须在 gate 报告里报出 D4 + D5",
              "D4 引文不符(警告)" in out and "D5 时间线矛盾(警告)" in out
              and "M-D45T-BAD" in out, out[-400:])
        good = {"modes": [mode(mode_code="M-D45T-GOOD", source_chapter="《论语·学而》",
                               key_quote_zh="有朋自远方来不亦乐乎",
                               representative_cases_zh="1644年测试人物主持重修书院")]}
        (tmp3 / "data" / "modes_data.json").write_text(json.dumps(good, ensure_ascii=False), encoding="utf-8")
        proc2 = subprocess.run([sys.executable, "tools/credibility_gate.py",
                                "--data-path", str(tmp3 / "data" / "modes_data.json")],
                               cwd=str(tmp3), capture_output=True, text=True)
        out2 = proc2.stdout + proc2.stderr
        check("L2 端到端：干净样本不得报 D4/D5",
              "D4 引文不符(警告)" not in out2 and "D5 时间线矛盾(警告)" not in out2
              and "matched" in out2, out2[-400:])
    finally:
        for d in (tmp_root, tmp2, tmp3, locals().get("tmp_partial"), locals().get("tmp_empty")):
            if d and Path(d).exists():
                shutil.rmtree(d, ignore_errors=True)

    failed = [r for r in RESULTS if not r[1]]
    print()
    print("%d/%d passed" % (len(RESULTS) - len(failed), len(RESULTS)))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
