#!/usr/bin/env python3
"""出处 → 链接 的**匹配规则唯一实现**（导出链 / 构建期注入 / QA 均复用它）。

背景
    `data/source_links.json` 是「按书名/事件名索引」的字典：
        {"《史记》": {"url": "...", "source_type": "ctext", "confidence": 0.9}, ...}
    模式的 `source_chapter` 是自由文本，里面可能写 `《史记·卫将军骠骑列传》`、
    `《焚书》《藏书》`、`朱熹《大学章句·格物补传》、《朱子语类》卷十` 等形态。
    本模块把「出处文本」解析成一串引文，并把每条引文匹配到索引 key。

匹配规则（与 docs/qa/link_coverage.md §1 逐字一致）
    R0 抽取：正则 `《([^》]{1,60})》` 抓取 source_chapter 中**全部**书名号跨度；
            每个跨度是一条「引文 citation」。没有书名号 → 0 条引文（不猜）。
    R1 候选：对引文内文 T 生成候选 key，**按优先级**命中即止：
            P1 精确      `《T》`                      （章级 key 覆盖书级 key）
            P2 去章名    T 按 '·' 逐级右截：A·B·C → 《A·B》→《A》
            P3 去缀语    去掉尾部括注/说明性后缀后重试 P1/P2
    R2 命中：第一个存在于索引的候选 key 即命中，取其 url（可为空 = 已登记不可链接）。
    R3 落空：全部候选都不在索引 → `unresolved`，**保持纯文本，不伪造链接**。

设计约束
    * key 一律**带书名号**，用字与 source_chapter 一致（简体）。
    * url 可指向繁体标题的源站页面（zh.wikisource 的 canonical title 是繁体）——
      键用简体、链指繁体，属于源站事实，不是错配。
    * 引文内文里出现的 '·' 既可能是「书·篇」也可能是人名（《埃隆·马斯克》）；
      P1 精确优先，只有精确不存在时才右截，因此人名书名不会被误拆。

用法
    from tools.source_link_index import load_index, resolve_source_chapter
    index = load_index()
    resolve_source_chapter("《史记·张仪列传》", index)
    # -> [{'citation': '史记·张仪列传', 'key': '《史记》', 'url': '...', 'status': 'linked'}]
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
LINKS_PATH = REPO_ROOT / "data" / "source_links.json"

CITATION_RE = re.compile(r"《([^》]{1,60})》")
SUFFIXES = ("及相关论著", "多篇综合", "及造纸工艺研究", "资料汇编", "考辨", "研究")
PAREN_RE = re.compile(r"[（(〔\[]([^）)〕\]]*)[）)〕\]]")


def _as_text(value) -> str:
    """source_chapter 少数条目是 list（实测 30 条）；统一成文本。"""
    if isinstance(value, list):
        return " ".join(str(x) for x in value)
    if value is None:
        return ""
    return str(value)


def extract_refs(source_chapter) -> list:
    """R0：抽出 source_chapter 中全部书名号内文（保序、去重）。"""
    text = _as_text(source_chapter)
    seen, out = set(), []
    for inner in CITATION_RE.findall(text):
        inner = inner.strip()
        if inner and inner not in seen:
            seen.add(inner)
            out.append(inner)
    return out


def extract_refs_raw(source_chapter) -> list:
    """R0-raw：抽出全部书名号内文（保序，不去重）。

    Phase21-W8 Stage2（卡 t_70a8cbce）候选口径修复用：原 R0（extract_refs）在同一
    source_chapter 内去重，导致书级被引被低估；此函数保留同一 mode 内的全部出现，
    供 build_source_links 的书级归并计数使用。匹配链（R1-R3）仍走 extract_refs 函数。
    """
    text = _as_text(source_chapter)
    out = []
    for inner in CITATION_RE.findall(text):
        inner = inner.strip()
        if inner:
            out.append(inner)
    return out


def candidate_keys(inner: str) -> list:
    """R1：一条引文的候选 key（带书名号），按优先级排序、去重。"""
    cands = []

    def add(name: str) -> None:
        name = name.strip()
        if not name:
            return
        key = "《" + name + "》"
        if key not in cands:
            cands.append(key)

    parts = inner.split("·")
    for i in range(len(parts), 0, -1):
        add("·".join(parts[:i]))

    stripped = PAREN_RE.sub("", inner).strip()
    for suf in SUFFIXES:
        if stripped.endswith(suf) and len(stripped) > len(suf):
            stripped = stripped[: -len(suf)].strip()
    if stripped != inner:
        sparts = stripped.split("·")
        for i in range(len(sparts), 0, -1):
            add("·".join(sparts[:i]))
    return cands


def load_index(path=LINKS_PATH) -> dict:
    """读索引；只接受 dict（裸列表 = 旧 schema，直接报错，避免静默降级）。"""
    path = Path(path)
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise ValueError(
            "%s: source_links.json 必须是『按书名索引』的 dict，实际是 %s"
            "（裸列表无法用于『出处→链接』匹配）" % (path, type(data).__name__)
        )
    for key, info in data.items():
        if not isinstance(info, dict) or "url" not in info:
            raise ValueError("%s: 条目 %r 不是 {url, source_type, confidence} 结构" % (path, key))
    return data


def resolve_citation(inner: str, index: dict) -> dict:
    """单条引文 → 命中信息。"""
    for key in candidate_keys(inner):
        if key in index:
            info = index[key]
            url = (info.get("url") or "").strip()
            status = "linked" if url else info.get("source_type", "unverifiable")
            return {
                "citation": inner,
                "key": key,
                "url": url,
                "source_type": info.get("source_type"),
                "confidence": info.get("confidence"),
                "status": status,
                "match_rule": "exact" if key == "《" + inner + "》" else "prefix",
            }
    return {
        "citation": inner,
        "key": None,
        "url": "",
        "source_type": None,
        "confidence": None,
        "status": "unresolved",
        "match_rule": None,
    }


def resolve_source_chapter(source_chapter, index: dict) -> list:
    """一条 source_chapter → 全部引文的匹配结果（保序）。"""
    return [resolve_citation(inner, index) for inner in extract_refs(source_chapter)]


def main() -> int:
    ap = argparse.ArgumentParser(description="出处→链接 匹配（R0-R3）自检/抽查")
    ap.add_argument("--links-path", default=str(LINKS_PATH))
    ap.add_argument("--sample", default=None, help="给一条 source_chapter 文本做匹配")
    ap.add_argument("--data-path", default=str(REPO_ROOT / "data" / "modes_data.json"))
    ap.add_argument("--coverage", action="store_true",
                    help="打印覆盖率对照（被引 >=3 书名 / 书级名 / 引文 / 模式 / 索引 provider 分布）")
    ap.add_argument("--min-citations", type=int, default=3)
    args = ap.parse_args()

    index = load_index(args.links_path)
    print("index keys: %d  (%s)" % (len(index), args.links_path))

    if args.sample:
        for r in resolve_source_chapter(args.sample, index):
            print(json.dumps(r, ensure_ascii=False))
        return 0

    with open(args.data_path, encoding="utf-8") as f:
        modes = json.load(f)["modes"]
    linked = unlinked = unresolved = 0
    for m in modes:
        for r in resolve_source_chapter(m.get("source_chapter"), index):
            if r["status"] == "linked":
                linked += 1
            elif r["status"] == "unresolved":
                unresolved += 1
            else:
                unlinked += 1
    total = linked + unlinked + unresolved
    print("citations: %d  linked=%d  registered-unlinkable=%d  unresolved=%d"
          % (total, linked, unlinked, unresolved))
    print("coverage = %d/%d = %.1f%%" % (linked, total, 100.0 * linked / total))
    if not args.coverage:
        return 0

    # ---- 覆盖率对照（被引 >=N 次的书名 / 书级名 / 模式）----------------
    counts: dict = {}
    for m in modes:
        for name in extract_refs(m.get("source_chapter")):
            counts[name] = counts.get(name, 0) + 1

    def linked_key_for(name: str):
        for key in candidate_keys(name):
            info = index.get(key)
            if info and (info.get("url") or "").strip():
                return key
        return None

    ge = [(n, c) for n, c in counts.items() if c >= args.min_citations]
    hit = sum(1 for n, _ in ge if linked_key_for(n))
    unv = sum(1 for n, _ in ge
              if not linked_key_for(n) and index.get("《%s》" % n, {}).get("source_type") == "unverifiable")
    base: dict = {}
    for n, c in counts.items():
        base[n.split("·")[0]] = base.get(n.split("·")[0], 0) + c
    bge = [(b, c) for b, c in base.items() if c >= args.min_citations]
    bhit = sum(1 for b, _ in bge if linked_key_for(b))
    modes_with_cit = sum(1 for m in modes if extract_refs(m.get("source_chapter")))
    modes_linked = sum(1 for m in modes
                       if any(x["status"] == "linked"
                              for x in resolve_source_chapter(m.get("source_chapter"), index)))

    print()
    print("distinct cited names: %d | >=%d: %d" % (len(counts), args.min_citations, len(ge)))
    print("names >=%d linked: %d/%d = %.1f%%  (registered-unverifiable %d)"
          % (args.min_citations, hit, len(ge), 100.0 * hit / max(1, len(ge)), unv))
    print("base names >=%d: %d | linked: %d = %.1f%%"
          % (args.min_citations, len(bge), bhit, 100.0 * bhit / max(1, len(bge))))
    print("modes with citations: %d | with >=1 linked citation: %d = %.1f%%"
          % (modes_with_cit, modes_linked, 100.0 * modes_linked / max(1, modes_with_cit)))
    print("index keys: %d | with url: %d | unverifiable: %d"
          % (len(index), sum(1 for v in index.values() if (v.get("url") or "").strip()),
             sum(1 for v in index.values() if not (v.get("url") or "").strip())))
    rep_path = REPO_ROOT / "data" / "audit" / "source_link_coverage.json"
    if rep_path.is_file():
        with rep_path.open(encoding="utf-8") as f:
            rep = json.load(f)
        print("provider distribution: %s" % json.dumps(rep.get("provider_distribution", {}),
                                                      ensure_ascii=False))
        print("unverifiable reasons: %s" % json.dumps(rep.get("unverifiable_reasons", {}),
                                                      ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
