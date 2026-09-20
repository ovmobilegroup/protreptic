#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_repo_parity.py — 「两仓一致性」机检（Phase37-X4）

标准（本阶段起，取代 Phase36-W4「全 tracked 文件字节一致」的过宽口径）
    凡**进入站点构建图或线上站点**的文件，开发仓（workspace）与发布仓（publish）
    必须逐字节一致（sha256）。
    两仓是同一个 GitHub 仓库的两条分支，职责不同：
      workspace = /opt/data/workspace/Protreptic        （master，干活/编辑语料的地方）
      publish   = /opt/data/release/Protreptic-publish  （origin main，驱动 GitHub Pages）

构建图怎么推出来（可复核，不靠猜）
  1. publish 仓 .github/workflows/pages.yml 的 build job 里 `python3 tools/<x>.py`
     → 这些脚本即构建图入口；本脚本每次运行都会现场解析 pages.yml 做边界自检，
       新增/删除构建步骤而没更新本清单 → 退出码 2（边界过期，不许静默漂移）；
  2. 这些脚本的本地 import 闭包（tools/*.py，见 TOOL_FILES 分组注释）；
  3. 这些脚本读的数据/资源：data/**、tools/json/scenarios_*.json、
     tools/json/scenario_tags.json、tools/scenario_tags.json、tools/assets/fonts/**；
  4. `mkdocs build -f mkdocs.pages.yml` 的输入：docs/**（exclude_docs: archive/ 除外）、
     docs_overrides/**（theme.custom_dir）、mkdocs.pages.yml 本身；
  5. web/**：Vite 输入（npm run build 出 dist/ → _site 产物根）；
  6. pages.yml 的 `on.push.paths` 触发器里声明的 tools/*（「可能改变线上站点」）。

排除（角色性差异 / 构建产物 / 备份 / 未进构建图，逐条给理由，见 EXCLUDE_RULES）
    例：api/protreptic.db（CI Step 0 现场重建）、.github/workflows/*（两仓编排职责不同）、
        web/dist/**、web/public/data/**（构建产物）、docs/archive/**（mkdocs 不构建）、
        data/intl_figures/**（grep 证实无任何构建步骤/前端读取）。

用法
    python3 tools/check_repo_parity.py [--workspace DIR] [--publish DIR]
    python3 tools/check_repo_parity.py --json     # 机读
    python3 tools/check_repo_parity.py --list     # 打印纳入/排除清单（含理由）
退出码
    0 = 零差异；1 = 有差异（缺一侧 / 内容不同）；2 = 边界过期或环境不满足。
"""

import argparse
import fnmatch
import hashlib
import json
import os
import re
import subprocess
import sys

DEFAULT_PUBLISH = "/opt/data/release/Protreptic-publish"

# ---- 边界：整棵子树 ------------------------------------------------
SUBTREES = ("data/", "web/", "docs/", "docs_overrides/")
# ---- 边界：单文件 --------------------------------------------------
BOUNDARY_FILES = ("mkdocs.pages.yml",)

# ---- 边界：tools/ 只纳入构建图脚本（不是整个 tools/：仓里有 ~950 个一次性历史脚本）----
TOOL_FILES = (
    # pages.yml build job 直接调用
    "tools/credibility_gate.py",
    "tools/verify_source_links.py",
    "tools/build_figures_db.py",
    "tools/export_static_site.py",
    "tools/gen_web_site_counts.py",
    "tools/build_daily_index.py",
    "tools/pages_preflight.py",
    "tools/build_search_index.py",
    "tools/build_graph_data.py",
    "tools/build_unified_index.py",
    "tools/build_og_images.py",
    "tools/prerender_routes.py",
    "tools/apply_og_meta.py",
    "tools/apply_site_counts.py",
    "tools/build_sw.py",
    "tools/build_sitemap.py",
    # pages.yml on.push.paths 声明（改了就触发发布 = 可能改变线上）
    "tools/prerender_body.py",
    "tools/og_image.py",
    "tools/build_pwa_icons.py",
    "tools/subset_og_font.py",
    # CI 门脚本（ci-cd.yml test job 调用；X5 已两仓同步，纳入以防漂移）
    "tools/verify_findings.py",
    # 上面脚本的本地 import 闭包
    "tools/site_counts.py",
    "tools/_quarantine.py",
    "tools/credibility_baseline.py",
    # Phase38-Y1 链接源工具链（source_link_index 将被 export 链 import；
    # build_source_links 是 data/source_links.json 的唯一生成器）
    "tools/source_link_index.py",
    "tools/build_source_links.py",
    # 本机检脚本自身（随两仓同步；纳入以示自洽）
    "tools/check_repo_parity.py",
)

# ---- 边界：tools/ 下被构建步骤读取的数据文件 ----------------------
TOOL_DATA_FILES = (
    "tools/json/scenarios_zh.json",
    "tools/json/scenarios_en.json",
    "tools/json/scenario_tags.json",
    "tools/scenario_tags.json",
)
# tools/assets/fonts/** 由 build_og_images / subset_og_font / build_pwa_icons 读取
TOOL_SUBTREES = ("tools/assets/fonts/",)

# ---- 排除规则（顺序即优先级；理由必须能指向证据） -----------------
EXCLUDE_RULES = (
    ("data/intl_figures/*",
     "开发侧原始分片留档（637 个，仅发布仓有）：grep tools/ + .github/ + web/src/ 无任何读取；"
     "不参与构建、不上线，故不纳入（如要按「源库留档」更严口径纳入，删掉本规则并执行 "
     "publish→workspace 同步）"),
    ("data/backup_merge_*/*", "入库前备份目录（开发仓独有，非构建图）"),
    ("data/merge_staging_*/*", "merge 暂存目录（开发仓独有，非构建图）"),
    ("*/node_modules/*", "依赖目录（.gitignore）"),
    ("*.bak*", "备份文件（.bak / .bak_<tag>）"),
    ("data/all_sources.json", "开发侧汇总实验产物，无构建步骤读取"),
    ("data/semantic_index.faiss", "开发侧 FAISS 索引二进制（无构建步骤读取；语义检索为 api/ 侧）"),
    ("docs/archive/*", "mkdocs.pages.yml `exclude_docs: archive/` → 不构建、不上线"),
    ("web/dist/*", "前端构建产物（CI 现场 npm run build 生成；发布仓为加 .gitignore 之前的历史跟踪）"),
    ("web/public/data/*", "静态数据产物（tools/export_static_site.py 现场生成；.gitignore 已声明）"),
    ("tools/assets/fonts/.cache/*", "字体源缓存（.gitignore；只在本机重新子集化时用）"),
    ("tools/gc/gc", "开发侧工具二进制，未被任何构建步骤调用"),
)

# ---- pages.yml 触发器里「不属于构建图」的路径（必须逐条给出理由）----
EXCLUDED_TRIGGERS = {
    "api/protreptic.db": "CI Step 0 由 tools/build_figures_db.py 清表重建，committed 内容不进构建结果",
    ".github/workflows/pages.yml": "编排本身（两仓 workflow 职责不同：发布仓才有 Pages 触发）",
}

REPO_OTHER_ROLE = (
    "不在边界内（既不参与站点构建、也不进入线上站点）的其余路径："
    "Dockerfile.api/Dockerfile.web、docker-compose.yml、api/**（后端 FastAPI 容器）、"
    ".github/**（CI 编排，两仓职责不同）、tests/、cli_tests/、scripts/、docs_site/**"
    "（更早的独立文档站工程，mkdocs.pages.yml 明确不用它）、kanban/、release/、backups_merge_*/、"
    "IL/、Vietnam/、assets/、templates/、scenarios/、individuals/、构建/ 等开发侧目录，"
    "以及根目录遗留副本（modes_data.json、scenarios_zh/en.json、code_maps.json、"
    "scenario_tags.json、three_dimensional_comparison_matrix.xlsx、lighthouserc.json 等）"
    "——构建步骤读的是 data/** 与 tools/** 下的同名文件（见 build_figures_db.py 的 find() 顺序）。"
)


def _sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def tracked_files(repo):
    """git ls-files（跟踪文件）——未跟踪/被 .gitignore 的构建产物天然不进集合。"""
    out = subprocess.run(["git", "-C", repo, "ls-files", "-z"],
                         capture_output=True, check=True).stdout
    return [p.decode("utf-8") for p in out.split(b"\0") if p]


def exclude_reason(path):
    """返回排除理由（None = 纳入边界）。"""
    for pattern, reason in EXCLUDE_RULES:
        if fnmatch.fnmatch(path, pattern):
            return reason
        # '*/node_modules/*' 这类需要匹配任意层级
        if pattern.startswith("*/") and fnmatch.fnmatch(path, pattern[1:].lstrip("/")):
            return reason
    for pattern, reason in EXCLUDE_RULES:
        if pattern.endswith("/*") and path.startswith(pattern[:-1]) and fnmatch.fnmatch(
                os.path.basename(path), "*"):
            base = pattern[:-1]
            if path.startswith(base) or ("/" + base) in path:
                return reason
    return None


def in_boundary(path):
    if path in BOUNDARY_FILES or path in TOOL_FILES or path in TOOL_DATA_FILES:
        return True
    if path.startswith(SUBTREES) or path.startswith(TOOL_SUBTREES):
        return True
    return False


def collect(repo):
    """返回 (纳入集合, 排除集合{path: reason})。"""
    included, excluded = {}, {}
    for path in tracked_files(repo):
        if not in_boundary(path):
            continue
        reason = exclude_reason(path)
        if reason:
            excluded[path] = reason
        else:
            full = os.path.join(repo, path)
            if os.path.isfile(full):
                included[path] = _sha256(full)
            else:
                included[path] = None  # 跟踪但不是普通文件（目录/子模块）
    return included, excluded


def workflow_boundary(publish):
    """从 pages.yml 现场解析构建步骤与 paths 触发器（边界自检用）。"""
    wf = os.path.join(publish, ".github", "workflows", "pages.yml")
    text = open(wf, encoding="utf-8").read()
    steps = sorted(set(re.findall(r"python3\s+(tools/[A-Za-z0-9_./\-]+\.py)", text)))
    m = re.search(r"^ {4}paths:\n((?: {6}- '[^']+'\n)+)", text, re.M)
    triggers = re.findall(r"- '([^']+)'", m.group(1)) if m else []
    return steps, triggers


def covered_by_boundary(path):
    if path in BOUNDARY_FILES or path in TOOL_FILES or path in TOOL_DATA_FILES:
        return True
    if path in EXCLUDED_TRIGGERS:
        return True
    p = path[:-2] if path.endswith("/**") else path
    return p.startswith(SUBTREES) or p.startswith(TOOL_SUBTREES)


def main():
    ap = argparse.ArgumentParser(description="两仓一致性机检（构建图口径，Phase37-X4）")
    ap.add_argument("--workspace", default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    help="开发仓根（默认：本脚本所在仓库）")
    ap.add_argument("--publish", default=DEFAULT_PUBLISH, help="发布仓根")
    ap.add_argument("--json", action="store_true", help="输出 JSON")
    ap.add_argument("--list", action="store_true", help="打印纳入/排除清单（含理由）")
    args = ap.parse_args()

    ws, pub = os.path.abspath(args.workspace), os.path.abspath(args.publish)
    for label, repo in (("workspace", ws), ("publish", pub)):
        if not os.path.isdir(os.path.join(repo, ".git")):
            print("[FAIL] %s 不是 git 仓库：%s" % (label, repo), file=sys.stderr)
            return 2

    # ---- 边界自检：pages.yml 的构建步骤 / 触发器必须已被本清单覆盖 ----
    steps, triggers = workflow_boundary(pub)
    stale = [s for s in steps if s not in TOOL_FILES]
    if stale:
        print("[FAIL] 边界过期：pages.yml 有构建步骤不在本清单 → 请更新 tools/check_repo_parity.py",
              file=sys.stderr)
        for s in stale:
            print("        未纳入: %s" % s, file=sys.stderr)
        return 2
    unstaged = [t for t in triggers if not covered_by_boundary(t)]
    if unstaged:
        print("[FAIL] 边界过期：pages.yml 的 paths 触发器未被本清单覆盖 → 请更新",
              file=sys.stderr)
        for t in unstaged:
            print("        未覆盖: %s" % t, file=sys.stderr)
        return 2

    inc_ws, exc_ws = collect(ws)
    inc_pub, exc_pub = collect(pub)

    diffs = []
    for path in sorted(set(inc_pub) | set(inc_ws)):
        a, b = inc_ws.get(path), inc_pub.get(path)
        if a is None and b is None:
            continue
        if a is None:
            diffs.append({"path": path, "kind": "MISSING_IN_WORKSPACE", "workspace": None, "publish": b})
        elif b is None:
            diffs.append({"path": path, "kind": "MISSING_IN_PUBLISH", "workspace": a, "publish": None})
        elif a != b:
            diffs.append({"path": path, "kind": "CONTENT_DIFF", "workspace": a, "publish": b})

    groups = []
    for exc in (exc_pub, exc_ws):
        for path, reason in exc.items():
            groups.append({"path": path, "reason": reason})
    reason_counts = {}
    for g in groups:
        reason_counts[g["reason"]] = reason_counts.get(g["reason"], 0) + 1

    ok = not diffs
    result = {
        "status": "OK" if ok else "DIFF",
        "workspace": ws, "publish": pub,
        "counts": {"workspace_in_boundary": len(inc_ws), "publish_in_boundary": len(inc_pub),
                   "identical": len([1 for p in set(inc_pub) & set(inc_ws)
                                     if inc_ws[p] is not None and inc_ws[p] == inc_pub[p]]),
                   "excluded_publish": len(exc_pub), "excluded_workspace": len(exc_ws)},
        "workflow_steps": steps, "workflow_triggers": triggers,
        "diffs": diffs,
        "excluded_reasons": reason_counts,
    }

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("[boundary] workspace = %s" % ws)
        print("[boundary] publish   = %s" % pub)
        print("[boundary] pages.yml 构建步骤 %d 个 / paths 触发器 %d 条 —— 均已被清单覆盖（边界自检通过）"
              % (len(steps), len(triggers)))
        print("[boundary] 纳入边界：workspace %d / publish %d；排除：workspace %d / publish %d"
              % (len(inc_ws), len(inc_pub), len(exc_ws), len(exc_pub)))
        if args.list:
            print("\n-- 纳入清单（publish 侧） --")
            for p in sorted(inc_pub):
                print("   + %s" % p)
            print("\n-- 排除清单（两仓并集，含理由） --")
            seen = set()
            for g in sorted(groups, key=lambda x: (x["path"])):
                if g["path"] in seen:
                    continue
                seen.add(g["path"])
                print("   - %s\n       └ %s" % (g["path"], g["reason"]))
        else:
            print("\n-- 排除统计（publish 侧） --")
            for reason, n in sorted(reason_counts.items(), key=lambda kv: -kv[1]):
                print("   %4d  %s" % (n, reason[:70]))
            print("\n" + REPO_OTHER_ROLE)
        if ok:
            print("\n[OK] 零差异：%d 个构建图文件两仓逐字节一致（sha256）" % result["counts"]["identical"])
        else:
            print("\n[DIFF] %d 处差异：" % len(diffs))
            for d in diffs:
                print("   %-22s %s" % (d["kind"], d["path"]))
            print("\n修法：内容差异按发布仓为准同步（cp <publish>/<path> <workspace>/<path> 反之视角色而定），"
                  "同步后重跑本脚本；退出码 1。")

    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
