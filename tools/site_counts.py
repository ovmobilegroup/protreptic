#!/usr/bin/env python3
"""site_counts.py — 站点门面计数（「N 条思维模式 × M 位历史人物」）的唯一取数入口。

为什么有它（真实事故，别重犯）
    同一句话要被多个表面复用：站点 HTML meta（含预渲染 head）、og:image:alt、
    两份 PWA manifest、docs 站产品页、SPA 运行时（useSeo.ts）…… 每个表面各自硬编码、
    各自读 meta.json，于是每加一个表面就漏一次：
      * Phase31-R8R9 清了 web/src 的硬编码，漏了 web/index.html（首页 head 一直在说谎）；
      * Phase33-L1 清了 HTML 与分享图，漏了 web/public/manifest*.webmanifest
        （Vite 原样拷进 dist，线上可直取）与 docs/02-tools/figure_library.md（docs 站产品页）。
    QA3 终审因此判 L1 FAIL：部署产物里仍有两份 manifest 写着旧口径。

做法
    唯一来源 = 部署产物里的 data/meta.json（tools/export_static_site.py 产出）：
        modes   = counts.mode_summaries_published  真正发布出去、站上打得开的模式摘要条数
                  （不是 modes_raw 的源记录数，也不是含 10 条被隔离伪造模式 M393-M402 的
                   mode_summaries —— 那两个数只是内部计数键，不做门面文案）
        figures = counts.mode_by_figure_shards     人物数（by-figure 分片数）
    **只有本模块**把这两个数字变成文案。其它工具一律 import 它（或调它的 CLI）：
    不许自己 json.load(meta.json) 拼串，更不许在源码里写死数字。

调用点（改口径只改这一个文件，下面这些地方自动跟着走）
    tools/apply_site_counts.py     首页 head 覆写 + manifest 收口 + 全量门面扫描（CI 步骤）
    （可选）任何新增表面：import site_counts 后用 description_text / og_description_text /
    manifest_description_text 取文案，用 scan_display_surfaces 做自检

CLI
    python3 tools/site_counts.py --show     # 打印当前口径与三句文案
    python3 tools/site_counts.py --sync     # 收口 web/public 与 web/dist 的两份 manifest
    python3 tools/site_counts.py --scan     # 扫 web/dist 全量门面数字（发布产物自查）
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DEFAULT_DIST = REPO / "web" / "dist"
DEFAULT_PUBLIC = REPO / "web" / "public"
MANIFEST_FILES = ("manifest.webmanifest", "manifest-light.webmanifest")

# 三句门面文案（口径唯一；与 web/src/composables/useSeo.ts 的 SEO_DEFAULT_DESCRIPTION、
# tools/og_image.py 的图内文案必须同值 —— apply_site_counts 会做交叉校验）
DESCRIPTION_FMT = "%d 条思维模式 × %d 位历史人物：每条都有出处、操作步骤与现代应用。以人为鉴，明得失。"
OG_DESCRIPTION_FMT = "%d 条思维模式 × %d 位历史人物 · 中英双语"
MANIFEST_DESCRIPTION_FMT = "%d 条思维模式 × %d 位历史人物：每条都有出处、操作步骤与现代应用，中英双语，可离线查阅。"

# 门面短语（全库硬门）：= QA3 的判定式，出现即必须等于本站口径。
#   只认标准措辞「N 条思维模式」「N 位历史人物」：更宽松的「N 条模式」「N 位人物」会命中文
#   正文里的**别的规模**（例：某人物档案写「知识库里躺着 1122 条模式」、入库记录写
#   「1542 条模式」），那是内容而不是站点门面数字，误判会逼着人去改史料文本。
#   门面文件（html/manifest/txt/xml/svg）另加一条裸数字硬门：不许出现 2868 / 2858。
MODES_PHRASE_RE = re.compile(r"(\d{3,5})\s*条思维模式")
PERSONS_PHRASE_RE = re.compile(r"(\d{2,4})\s*位历史人物")

# 旧口径裸数字：只在门面文件（HTML/manifest/txt/xml/svg）里算违规
STALE_RAW = ("2868", "2858")
RAW_CHECK_SUFFIXES = (".html", ".htm", ".webmanifest", ".txt", ".xml", ".svg")

# 二进制/字体/图不动
SKIP_SUFFIXES = (
    ".png", ".jpg", ".jpeg", ".webp", ".gif", ".ico", ".svgz",
    ".woff", ".woff2", ".otf", ".ttf", ".gz", ".bin", ".mp4", ".map",
    ".chroma", ".arrow", ".xlsx", ".db", ".pdf",
)

# manifest 里被收口的那一行（只改 description，其余字节不动）
MANIFEST_DESC_RE = re.compile(r'^(\s*)"description":\s*"(?:[^"\\]|\\.)*",[ \t]*$', re.MULTILINE)


def fail(msg: str) -> None:
    print("[counts] %s" % msg)
    raise SystemExit(1)


# ---------------------------------------------------------------- 取数

def load_counts(data_dir: Path) -> tuple:
    """从 data/ 目录（部署产物里就是 dist/data）读门面口径，返回 (modes, figures)。"""
    meta = Path(data_dir) / "meta.json"
    if not meta.is_file():
        fail("缺少 %s：先跑 python3 tools/export_static_site.py" % meta)
    try:
        counts = json.loads(meta.read_text(encoding="utf-8")).get("counts") or {}
    except json.JSONDecodeError as exc:
        fail("%s 不是合法 JSON：%s" % (meta, exc))
    for key in ("mode_summaries_published", "mode_by_figure_shards"):
        if not isinstance(counts.get(key), int):
            fail("%s 的 counts.%s 不是整数: %r" % (meta, key, counts.get(key)))
    return counts["mode_summaries_published"], counts["mode_by_figure_shards"]


def description_text(modes: int, figures: int) -> str:
    return DESCRIPTION_FMT % (modes, figures)


def og_description_text(modes: int, figures: int) -> str:
    return OG_DESCRIPTION_FMT % (modes, figures)


def manifest_description_text(modes: int, figures: int) -> str:
    return MANIFEST_DESCRIPTION_FMT % (modes, figures)


# ---------------------------------------------------------------- manifest 收口

def sync_manifest(path, modes: int, figures: int, dry_run: bool = False) -> tuple:
    """把一份 manifest 的 description 收口到当日口径。返回 (path, changed, old, new)。"""
    p = Path(path)
    if not p.is_file():
        fail("缺少 %s：manifest 必须存在（源在 web/public/，产物在 dist/）" % p)
    text = p.read_text(encoding="utf-8")
    if len(MANIFEST_DESC_RE.findall(text)) != 1:
        fail("%s 里 description 行有 %d 处（应为 1）" % (p, len(MANIFEST_DESC_RE.findall(text))))
    try:
        old = json.loads(text)["description"]
    except (json.JSONDecodeError, KeyError) as exc:
        fail("%s 不是合法 manifest（%s）" % (p, exc))
    want = manifest_description_text(modes, figures)
    if old == want:
        return p, False, old, want
    new = MANIFEST_DESC_RE.sub(lambda m: '%s"description": "%s",' % (m.group(1), want), text, count=1)
    if not dry_run:
        p.write_text(new, encoding="utf-8")
        back = json.loads(p.read_text(encoding="utf-8"))
        if back.get("description") != want:
            fail("回读失败 %s: %r" % (p, back.get("description")))
        # 除 description 外的键必须一个都不动（逐键比较，注意旧的 description 本来就不同）
        before, after = json.loads(text), dict(back)
        before.pop("description", None)
        after.pop("description", None)
        if before != after:
            fail("%s 收口时改动了 description 以外的内容" % p)
    return p, True, old, want


def sync_manifests(dist=DEFAULT_DIST, public=DEFAULT_PUBLIC, modes=None, figures=None,
                   dry_run: bool = False) -> list:
    """源（web/public，Vite 会原样拷进 dist）+ 产物（dist）两份 manifest 一起收口。"""
    if modes is None or figures is None:
        modes, figures = load_counts(Path(dist) / "data")
    out = []
    targets = []
    if public is not None:
        for name in MANIFEST_FILES:
            targets.append(Path(public) / name)
    for name in MANIFEST_FILES:
        p = Path(dist) / name
        if p not in targets:
            targets.append(p)
    for p in targets:
        if p.is_file() or p.parent == Path(dist):
            out.append(sync_manifest(p, modes, figures, dry_run=dry_run))
    return out


# ---------------------------------------------------------------- 扫描

def scan_display_surfaces(root, modes: int, figures: int) -> tuple:
    """扫一棵产物树（web/dist/**）里的全部门面数字。

    规则：
      * 任何「N 条思维模式」必须 == modes，任何「N 位历史人物」必须 == figures（QA3 判定式）；
      * 门面文件（html/webmanifest/txt/xml/svg）里不允许出现旧口径裸数字（2868 / 2858）——
        data/*.json 的 counts 是**数据契约**（modes_raw / mode_summaries 为内部键），不算门面。
    返回 (扫描文件数, 违规列表[(rel, 类别, 命中)])。
    """
    root = Path(root)
    if not root.is_dir():
        fail("扫描目录不存在: %s" % root)
    violations = []
    checked = 0
    want_modes, want_figures = str(modes), str(figures)
    for p in sorted(root.rglob("*")):
        if not p.is_file() or ".git" in p.parts:
            continue
        suffix = p.suffix.lower()
        if suffix in SKIP_SUFFIXES:
            continue
        try:
            text = p.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        checked += 1
        rel = p.relative_to(root).as_posix()
        for m in MODES_PHRASE_RE.finditer(text):
            if m.group(1) != want_modes:
                violations.append((rel, "条数", m.group(0)))
        for m in PERSONS_PHRASE_RE.finditer(text):
            if m.group(1) != want_figures:
                violations.append((rel, "人物数", m.group(0)))
        if suffix in RAW_CHECK_SUFFIXES:
            for token in STALE_RAW:
                if token in text and token not in (want_modes, want_figures):
                    violations.append((rel, "旧口径裸数字", token))
    return checked, violations


# docs 站的**产品门面页**（其余 docs 是历时报告/研究记录，允许保留当时的实测数字）
PRODUCT_DOCS = ("index.md", "02-tools")

# 允许在 docs 产品页里出现的「源库原始数」——但必须逐行标注口径来源，
# 否则就是门面数字打架（Phase33-L1 线上翻车的正是这种未标注的旧口径）。
DOC_SOURCE_LABELS = ("源库", "源数据", "原始记录", "口径")


def scan_product_docs(docs_dir, modes: int, figures: int) -> tuple:
    """扫 docs 站的产品门面页：只有这些页面代表「现在的产品规模」。

    规则：任何门面数字必须等于本站口径；**逐行**标注了「源库 / 源数据 / 原始记录 / 口径」
    的行除外 —— 那种行是在如实交代源库与站上发布数的差别，不算打架。
    """
    docs_dir = Path(docs_dir)
    if not docs_dir.is_dir():
        return 0, []
    files = _product_doc_files(docs_dir)
    violations = []
    want_modes, want_figures = str(modes), str(figures)
    for p in files:
        rel = p.relative_to(docs_dir).as_posix()
        for lineno, line in enumerate(p.read_text(encoding="utf-8", errors="ignore").splitlines(), 1):
            if any(label in line for label in DOC_SOURCE_LABELS):
                continue
            for m in MODES_PHRASE_RE.finditer(line):
                if m.group(1) != want_modes:
                    violations.append(("%s:%d" % (rel, lineno), "条数", m.group(0)))
            for m in PERSONS_PHRASE_RE.finditer(line):
                if m.group(1) != want_figures:
                    violations.append(("%s:%d" % (rel, lineno), "人物数", m.group(0)))
            for token in STALE_RAW:
                if token in line and token not in (want_modes, want_figures):
                    violations.append(("%s:%d" % (rel, lineno), "旧口径裸数字", token))
    return len(files), violations


def _product_doc_files(docs_dir):
    """docs 站**产品门面页**清单（index.md + 02-tools/** 的 md）."""
    docs_dir = Path(docs_dir)
    files = []
    if not docs_dir.is_dir():
        return files
    for entry in PRODUCT_DOCS:
        p = docs_dir / entry
        if p.is_file():
            files.append(p)
        elif p.is_dir():
            files.extend(sorted(p.rglob("*.md")))
    return files


def _align_line(line: str, want_modes: str, want_figures: str) -> str:
    """把一行里的门面短语改写成当前口径（只动数字，措辞与其余字节不动）."""
    out = MODES_PHRASE_RE.sub(lambda m: want_modes + m.group(0)[len(m.group(1)):], line)
    out = PERSONS_PHRASE_RE.sub(lambda m: want_figures + m.group(0)[len(m.group(1)):], out)
    return out


def align_product_docs(docs_dir, modes: int, figures: int) -> list:
    """把 docs 产品门面页的门面数字对齐到当前口径，返回 [(rel, lineno, old, new)].

    判定规则与 scan_product_docs 完全一致（逐行、逐短语；标了「源库 / 源数据 / 原始记录 /
    口径」的行是如实交代源库与原站发布数的差别，不碰）。两者同规则是刻意的：能过扫描的
    行就是这里不会改的行，避免出现「体检说违规、对齐又不动」的死角。
    """
    want_modes, want_figures = str(modes), str(figures)
    changes = []
    for p in _product_doc_files(docs_dir):
        rel = p.relative_to(Path(docs_dir)).as_posix()
        lines = p.read_text(encoding="utf-8", errors="ignore").splitlines(keepends=True)
        out = []
        for lineno, line in enumerate(lines, 1):
            if any(label in line for label in DOC_SOURCE_LABELS):
                out.append(line)
                continue
            new = _align_line(line, want_modes, want_figures)
            if new != line:
                changes.append((rel, lineno, line.strip()[:100], new.strip()[:100]))
            out.append(new)
        body = "".join(out)
        if body != p.read_text(encoding="utf-8", errors="ignore"):
            p.write_text(body, encoding="utf-8")
    return changes


# ---------------------------------------------------------------- CLI

def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="站点门面计数的唯一取数入口")
    ap.add_argument("--dist", default=str(DEFAULT_DIST))
    ap.add_argument("--public", default=str(DEFAULT_PUBLIC))
    ap.add_argument("--data-dir", default=None, help="默认 <dist>/data")
    ap.add_argument("--show", action="store_true", help="打印当前口径与三句文案")
    ap.add_argument("--sync", action="store_true", help="收口两份 manifest（源 + 产物）")
    ap.add_argument("--scan", action="store_true", help="扫 <dist> 全量门面数字")
    ap.add_argument("--docs", default=str(REPO / "docs"), help="docs 站目录（产品门面页体检）")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)

    data_dir = Path(args.data_dir) if args.data_dir else Path(args.dist) / "data"
    modes, figures = load_counts(data_dir)

    if args.show or not (args.sync or args.scan):
        print("[counts] 口径来源: %s/meta.json 的 counts.mode_summaries_published / counts.mode_by_figure_shards" % data_dir)
        print("[counts] description          : %s" % description_text(modes, figures))
        print("[counts] og:description       : %s" % og_description_text(modes, figures))
        print("[counts] manifest description : %s" % manifest_description_text(modes, figures))

    if args.sync:
        for p, changed, old, new in sync_manifests(args.dist, args.public, modes, figures, args.dry_run):
            print("[counts] manifest %s %s -> %s" % ("更新" if changed else "已一致", p, new))

    rc = 0
    if args.scan:
        checked, violations = scan_display_surfaces(args.dist, modes, figures)
        print("[counts] 扫描 %s 共 %d 个文件；口径 %d 条 × %d 位" % (args.dist, checked, modes, figures))
        for rel, kind, hit in violations:
            print("    [%s] %s -> %s" % (kind, rel, hit))
        print("[counts] 违规 %d 条" % len(violations))
        n_docs, doc_violations = scan_product_docs(args.docs, modes, figures)
        print("[counts] docs 产品门面页 %d 个；违规 %d 条" % (n_docs, len(doc_violations)))
        for rel, kind, hit in doc_violations:
            print("    [docs:%s] %s -> %s" % (kind, rel, hit))
        if violations or doc_violations:
            rc = 1
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
