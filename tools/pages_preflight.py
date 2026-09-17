#!/usr/bin/env python3
"""pages_preflight.py - GitHub Pages 发布前断言（Phase 29-5）。

把 .github/workflows/pages.yml 里三道关卡抽成可本地复跑的脚本，CI 与本地用同一条命令：

    --stage data     web/public/data 静态数据基线（meta.json 条数 / 分片数）
    --stage dist     web/dist SPA 产物（404.html 回退、/protreptic/ 前缀、data 随构建进包）
    --stage merged   _site/ 合并产物（SPA 在根 + 文档站在 /docs/ + 404.html 只出现一次）

基线常量 EXPECT_* 必须与 tools/export_static_site.py 保持一致；数据源变了两处一起改，
否则这里会红着脸拦住发布（这正是加这道断言的目的：数据动了、站点没跟上）。

退出码：0 全部通过；1 有断言失败（逐条打印 ::error:: 供 Actions 标注）。
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

EXPECT_FIGURES = 501
EXPECT_MODES = 2858
EXPECT_BY_FIGURE = 284
EXPECT_MODE_INDEX_SHARDS = 8
SPA_BASE = "/protreptic/"

DATA_DIR = REPO_ROOT / "web" / "public" / "data"
DIST_DIR = REPO_ROOT / "web" / "dist"
SITE_DIR = REPO_ROOT / "_site"


class Checker:
    def __init__(self, stage: str) -> None:
        self.stage = stage
        self.failures: list[str] = []
        self.notes: list[str] = []

    def fail(self, msg: str) -> None:
        self.failures.append(msg)

    def note(self, msg: str) -> None:
        self.notes.append(msg)

    def expect(self, got, want, label: str) -> None:
        if got != want:
            self.fail(f"{label} = {got}，期望 {want}")

    def read_json(self, path: Path):
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except FileNotFoundError:
            self.fail(f"缺少文件 {path.relative_to(REPO_ROOT)}")
        except json.JSONDecodeError as exc:
            self.fail(f"{path.relative_to(REPO_ROOT)} 不是合法 JSON：{exc}")
        except UnicodeDecodeError as exc:
            self.fail(f"{path.relative_to(REPO_ROOT)} 不是 UTF-8：{exc}")
        return None

    def report(self) -> int:
        for line in self.notes:
            print(f"      {line}")
        if self.failures:
            for line in self.failures:
                print(f"::error::{line}")
            print(f"[FAIL] stage={self.stage}：{len(self.failures)} 条断言未通过")
            return 1
        print(f"[OK] stage={self.stage}：全部断言通过")
        return 0


def check_data(c: Checker) -> None:
    meta = c.read_json(DATA_DIR / "meta.json")
    if meta is None:
        return
    counts = meta.get("counts") or {}
    c.expect(counts.get("figures"), EXPECT_FIGURES, "meta.json counts.figures")
    c.expect(counts.get("mode_summaries"), EXPECT_MODES, "meta.json counts.mode_summaries")
    c.expect(
        counts.get("mode_by_figure_shards"),
        EXPECT_BY_FIGURE,
        "meta.json counts.mode_by_figure_shards",
    )
    c.expect(
        counts.get("mode_index_shards"),
        EXPECT_MODE_INDEX_SHARDS,
        "meta.json counts.mode_index_shards",
    )

    index = c.read_json(DATA_DIR / "figures.index.json")
    if isinstance(index, list):
        c.expect(len(index), EXPECT_FIGURES, "figures.index.json 条数")
    elif index is not None:
        c.fail("figures.index.json 顶层不是数组")

    figure_shards = sorted((DATA_DIR / "figures").glob("*.json"))
    c.expect(len(figure_shards), EXPECT_FIGURES, "data/figures/*.json 分片数")

    mode_shards = sorted((DATA_DIR / "modes").glob("index-*.json"))
    c.expect(len(mode_shards), EXPECT_MODE_INDEX_SHARDS, "data/modes/index-*.json 分片数")

    by_figure = sorted((DATA_DIR / "modes" / "by-figure").glob("*.json"))
    c.expect(len(by_figure), EXPECT_BY_FIGURE, "data/modes/by-figure/*.json 分片数")

    c.note(
        f"figures={counts.get('figures')} modes={counts.get('mode_summaries')} "
        f"figure shards={len(figure_shards)} by-figure shards={len(by_figure)}"
    )


def check_dist(c: Checker) -> None:
    for rel in ("index.html", "404.html", "favicon.svg", "data/meta.json", "assets"):
        if not (DIST_DIR / rel).exists():
            c.fail(f"web/dist/{rel} 缺失")

    index_html = None
    if (DIST_DIR / "index.html").is_file():
        index_html = (DIST_DIR / "index.html").read_text(encoding="utf-8")
        if f"{SPA_BASE}assets/" not in index_html:
            c.fail(f"web/dist/index.html 里没有 {SPA_BASE}assets/ 前缀（VITE_BASE 被覆盖了？）")

    if index_html is not None and (DIST_DIR / "404.html").is_file():
        if (DIST_DIR / "404.html").read_text(encoding="utf-8") != index_html:
            c.fail("web/dist/404.html 与 index.html 不一致：SPA 深链回退失效")

    built_meta = c.read_json(DIST_DIR / "data" / "meta.json")
    public_meta = c.read_json(DATA_DIR / "meta.json")
    if built_meta is not None and public_meta is not None:
        if built_meta.get("counts") != public_meta.get("counts"):
            c.fail(
                "web/dist/data/meta.json 与 web/public/data/meta.json 不一致："
                "SPA 在静态数据导出之前（或没带上数据）就构建了"
            )

    built_index = c.read_json(DIST_DIR / "data" / "figures.index.json")
    if isinstance(built_index, list):
        c.expect(len(built_index), EXPECT_FIGURES, "dist/data/figures.index.json 条数")

    c.note("dist: index.html + 404.html（逐字节相同）+ data/ + /protreptic/ 前缀")


def check_merged(c: Checker) -> None:
    for rel in ("index.html", "404.html", "favicon.svg", "data/meta.json", ".nojekyll"):
        if not (SITE_DIR / rel).exists():
            c.fail(f"_site/{rel} 缺失")

    root_404 = list(SITE_DIR.glob("404.html"))
    c.expect(len(root_404), 1, "_site 根目录 404.html 数量")

    docs_pages = sorted((SITE_DIR / "docs").rglob("*.html"))
    if not docs_pages:
        c.fail("_site/docs/ 下没有任何 html：文档站没有合并进来")
    if (REPO_ROOT / "docs" / "index.md").is_file() and not (SITE_DIR / "docs" / "index.html").is_file():
        c.fail("docs/index.md 存在但 _site/docs/index.html 缺失：文档站首页没构建出来")
    if not (REPO_ROOT / "docs" / "index.md").is_file():
        c.note("docs/index.md 不存在：/docs/ 暂时没有落地页（把 Jekyll 时代的首页一起带上即可）")

    raw_docs = [p for p in (SITE_DIR / "docs").rglob("*.md")]
    if raw_docs:
        c.fail(f"_site/docs/ 里残留了 {len(raw_docs)} 个未渲染的 .md 文件")

    c.note(f"merged: SPA 在根 + 文档站 {len(docs_pages)} 个页面在 /docs/")


STAGES = {"data": check_data, "dist": check_dist, "merged": check_merged}


def main() -> int:
    parser = argparse.ArgumentParser(description="GitHub Pages 发布前断言")
    parser.add_argument("--stage", choices=sorted(STAGES), required=True)
    args = parser.parse_args()

    checker = Checker(args.stage)
    STAGES[args.stage](checker)
    return checker.report()


if __name__ == "__main__":
    sys.exit(main())
