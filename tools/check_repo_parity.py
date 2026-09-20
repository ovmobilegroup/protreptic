#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_repo_parity.py — 「两仓一致性」机检（Phase37-X4 定义，Phase39-Z1 双向加固）

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

Phase39-Z1 加固：单侧缺失的**双向**检测（修盲区）
  旧口径只枚举 `git ls-files`（索引里的已跟踪文件）→ 四处盲区（前三处见下，(d) 是同族假 OK）：
    (a) **未跟踪**（未 git add）的构建图文件完全不可见：
        Phase38-QA8 的 docs/qa/phase38_acceptance.md 只在开发仓、发布仓缺失，
        以及船长复现用的 docs/qa/__parity_probe__.md，都是「未跟踪」→ 机检静默通过；
    (b) 索引里有、工作树里已被删除（或从未检出）的文件被当成「两边都没」跳过；
    (c) 符号链接一律记 sha=None，两侧 None==None 也被跳过。
    (d) 自比：本脚本随两仓同步，若在发布仓里直接跑（不传 --workspace），workspace 默认 = 脚本所在仓
        = publish，两侧同一目录 → 单侧检测恒为 0、输出假 OK（现已加硬守卫，直接 exit 2）。
  现口径：文件集 = **索引（已跟踪）∪ 未跟踪且未被 .gitignore**；
  逐条 sha256（符号链接按「链接→目标」取值；工作树缺失记 absent）。
  单侧缺失 → MISSING_IN_WORKSPACE / MISSING_IN_PUBLISH，**报出并 exit 1**；
  每条差异都带「侧别 + 理由分类」（未跟踪 vs 已跟踪 vs 内容不同），
  让「并行卡未提交的在制工作」与「真漂移」一眼可分。
  `--tracked-only` 可回到旧的「只看索引」口径（诊断用，不是默认）。

排除（角色性差异 / 构建产物 / 备份 / 未进构建图，逐条给理由，见 EXCLUDE_RULES）
    例：api/protreptic.db（CI Step 0 现场重建）、.github/workflows/*（两仓编排职责不同）、
        web/dist/**、web/public/data/**（构建产物）、docs/archive/**（mkdocs 不构建）、
        data/intl_figures/**（grep 证实无任何构建步骤/前端读取）。
    排除项**不静默吞掉**：报告里按「规则 × 侧别」列出条数与理由（含只在单侧的条数），
    并有硬自检 —— 任何排除路径若撞上清单内明确纳入的构建图文件或 pages.yml 触发器
    → exit 2（排除规则过期）。

用法
    python3 tools/check_repo_parity.py [--workspace DIR] [--publish DIR]
    python3 tools/check_repo_parity.py --json             # 机读
    python3 tools/check_repo_parity.py --list             # 打印纳入/排除清单（含理由）
    python3 tools/check_repo_parity.py --tracked-only     # 旧口径（只看索引）
退出码
    0 = 零差异；1 = 有差异（缺一侧 / 内容不同）；2 = 边界过期或环境不满足。
"""

import argparse
import collections
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
    # Phase40-Z2 D4/D5 工具链（gate 的 import 闭包 + 缓存生成器 + 其负对照自测）
    "tools/source_text_cache.py",
    "tools/fetch_source_texts.py",
    "tools/test_credibility_d45.py",
    "tools/build_audit_findings.py",
    # 本机检脚本与它的负对照自测（随两仓同步；纳入以示自洽，不得单侧漂移）
    "tools/check_repo_parity.py",
    "tools/test_check_repo_parity.py",
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

# 一条工作树记录：fingerprint（sha256 / symlink 目标 / absent）+ 来源（tracked / untracked）
Entry = collections.namedtuple("Entry", "fingerprint state")


def _sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _fingerprint(path):
    """内容指纹：普通文件 = sha256；符号链接 = 链接目标（内容差异同样可见）；
    索引里有但工作树没有（已删除 / 未检出）= absent。"""
    if os.path.islink(path):
        return "symlink:" + os.readlink(path)
    if os.path.isfile(path):
        return "sha256:" + _sha256(path)
    return "absent"


def _ls_files(repo, *args):
    out = subprocess.run(["git", "-C", repo, "ls-files", "-z"] + list(args),
                         capture_output=True, check=True).stdout
    return [p.decode("utf-8") for p in out.split(b"\0") if p]


def working_files(repo, include_untracked=True):
    """工作树里的构建图候选文件集 {path: state}。

    state = 'tracked'（在索引里，会被 commit / CI 看到）
          | 'untracked'（未 git add，但没被 .gitignore —— 一旦 add 就进构建图；
             旧口径在这里是盲区：Phase38-QA8 的报告与船长的探针都栽在这一格）
    """
    states = {}
    for p in _ls_files(repo, "--cached"):
        states[p] = "tracked"
    if include_untracked:
        for p in _ls_files(repo, "--others", "--exclude-standard"):
            states.setdefault(p, "untracked")
    return states


def matched_rule(path):
    """返回命中的 (pattern, reason)；None = 未命中任何排除规则。"""
    for pattern, reason in EXCLUDE_RULES:
        if fnmatch.fnmatch(path, pattern):
            return pattern, reason
        # '*/node_modules/*' 这类需要匹配任意层级
        if pattern.startswith("*/") and fnmatch.fnmatch(path, pattern[1:].lstrip("/")):
            return pattern, reason
    for pattern, reason in EXCLUDE_RULES:
        if pattern.endswith("/*") and path.startswith(pattern[:-1]) and fnmatch.fnmatch(
                os.path.basename(path), "*"):
            base = pattern[:-1]
            if path.startswith(base) or ("/" + base) in path:
                return pattern, reason
    return None, None


def exclude_reason(path):
    """返回排除理由（None = 纳入边界）。"""
    return matched_rule(path)[1]


def in_boundary(path):
    if path in BOUNDARY_FILES or path in TOOL_FILES or path in TOOL_DATA_FILES:
        return True
    if path.startswith(SUBTREES) or path.startswith(TOOL_SUBTREES):
        return True
    return False


def collect(repo, include_untracked=True):
    """返回 (纳入集合 {path: Entry}, 排除集合 {path: (reason, state)})。"""
    included, excluded = {}, {}
    for path, state in working_files(repo, include_untracked).items():
        if not in_boundary(path):
            continue
        reason = exclude_reason(path)
        if reason:
            excluded[path] = (reason, state)
        else:
            included[path] = Entry(_fingerprint(os.path.join(repo, path)), state)
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


def exclusion_guard(exc_ws, exc_pub, triggers):
    """硬自检：排除规则不得吞掉构建图文件（撞上明确纳入清单或未豁免触发器 → exit 2）。"""
    explicit = set(TOOL_FILES) | set(TOOL_DATA_FILES) | set(BOUNDARY_FILES)
    problems = []
    for path in sorted(set(exc_ws) | set(exc_pub)):
        if path in explicit:
            problems.append((path, "该路径在纳入清单内（TOOL_FILES / BOUNDARY_FILES），却命中了排除规则"))
        elif path in triggers and path not in EXCLUDED_TRIGGERS:
            problems.append((path, "该路径是 pages.yml 的 paths 触发器（可能改变线上），却命中了排除规则"))
    return problems


def diff_label(side, reason):
    return "[%s · %s]" % (side, reason)


def main():
    ap = argparse.ArgumentParser(description="两仓一致性机检（构建图口径 Phase37-X4；Phase39-Z1 双向加固）")
    ap.add_argument("--workspace", default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    help="开发仓根（默认：本脚本所在仓库）")
    ap.add_argument("--publish", default=DEFAULT_PUBLISH, help="发布仓根")
    ap.add_argument("--json", action="store_true", help="输出 JSON")
    ap.add_argument("--list", action="store_true", help="打印纳入/排除清单（含理由）")
    ap.add_argument("--tracked-only", action="store_true",
                    help="旧口径：只看索引里的已跟踪文件（不看未跟踪的新增文件；诊断用）")
    args = ap.parse_args()

    include_untracked = not args.tracked_only
    ws, pub = os.path.abspath(args.workspace), os.path.abspath(args.publish)
    for label, repo in (("workspace", ws), ("publish", pub)):
        if not os.path.isdir(os.path.join(repo, ".git")):
            print("[FAIL] %s 不是 git 仓库：%s" % (label, repo), file=sys.stderr)
            return 2

    # ---- self-compare guard (Phase39-Z1 blind spot d) ----
    if os.path.realpath(ws) == os.path.realpath(pub):
        print("[FAIL] workspace 与 publish 指向同一个仓: %s; 自比会让单侧检测恒为 0、输出假 OK,"
              "请显式指定另一侧的仓根" % ws, file=sys.stderr)
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

    inc_ws, exc_ws = collect(ws, include_untracked)
    inc_pub, exc_pub = collect(pub, include_untracked)

    # ---- 排除规则自检：排除不得吞掉构建图文件（Phase39-Z1）----
    swallowed = exclusion_guard(exc_ws, exc_pub, triggers)
    if swallowed:
        print("[FAIL] 排除规则过期：有路径既被排除、又属于构建图（排除不得静默吞掉构建图文件）",
              file=sys.stderr)
        for path, why in swallowed:
            print("        %s —— %s" % (path, why), file=sys.stderr)
        return 2

    # ---- 双向比对：只看单侧 / 内容不同都算差异（Phase39-Z1）----
    diffs = []
    both_sides = identical = only_ws = only_pub = 0
    for path in sorted(set(inc_ws) | set(inc_pub)):
        w, p = inc_ws.get(path), inc_pub.get(path)
        w_have = w is not None and w.fingerprint != "absent"
        p_have = p is not None and p.fingerprint != "absent"
        if not w_have and not p_have:
            continue
        if not w_have or not p_have:
            present = p if not w_have else w
            absent_side = w if not w_have else p
            if absent_side is not None and absent_side.fingerprint == "absent":
                reason = "工作树缺失（索引里有、文件不在工作树：已删除或未检出）"
            elif present.state == "untracked":
                reason = "未跟踪（未 git add，尚未进入索引）"
            else:
                reason = "已跟踪（索引里有，另一侧没有）"
            if not w_have:
                kind, side = "MISSING_IN_WORKSPACE", "仅发布仓"
                only_pub += 1
            else:
                kind, side = "MISSING_IN_PUBLISH", "仅工作仓"
                only_ws += 1
            diffs.append({"path": path, "kind": kind, "side": side, "reason": reason,
                          "workspace": w.fingerprint if w else None,
                          "publish": p.fingerprint if p else None,
                          "workspace_state": w.state if w else None,
                          "publish_state": p.state if p else None,
                          "workspace_has_file": w_have, "publish_has_file": p_have})
            continue
        both_sides += 1
        if w.fingerprint != p.fingerprint:
            state_hint = ""
            if w.state == "untracked" or p.state == "untracked":
                state_hint = "（含未跟踪侧）"
            diffs.append({"path": path, "kind": "CONTENT_DIFF", "side": "两仓都有",
                          "reason": "内容不同" + state_hint,
                          "workspace": w.fingerprint, "publish": p.fingerprint,
                          "workspace_state": w.state, "publish_state": p.state,
                          "workspace_has_file": True, "publish_has_file": True})
        else:
            identical += 1

    ok = not diffs

    # ---- 排除项按「规则 × 侧别」列出（含单侧差异与理由）----
    rule_rows = []
    for pattern, reason in EXCLUDE_RULES:
        in_ws = sorted(p for p in exc_ws if matched_rule(p)[0] == pattern)
        in_pub = sorted(p for p in exc_pub if matched_rule(p)[0] == pattern)
        rule_rows.append({
            "pattern": pattern, "reason": reason,
            "workspace": len(in_ws), "publish": len(in_pub),
            "only_workspace": len([p for p in in_ws if p not in exc_pub]),
            "only_publish": len([p for p in in_pub if p not in exc_ws]),
        })
    excluded_side = {
        "workspace": len(exc_ws), "publish": len(exc_pub),
        "only_workspace": len([p for p in exc_ws if p not in exc_pub]),
        "only_publish": len([p for p in exc_pub if p not in exc_ws]),
    }
    untracked_counts = {
        "workspace": len([1 for p in inc_ws if inc_ws[p].state == "untracked"]),
        "publish": len([1 for p in inc_pub if inc_pub[p].state == "untracked"]),
    }
    reason_counts = {}
    for exc in (exc_pub, exc_ws):
        for path, (reason, _state) in exc.items():
            reason_counts[reason] = reason_counts.get(reason, 0) + 1

    result = {
        "status": "OK" if ok else "DIFF",
        "workspace": ws, "publish": pub,
        "include_untracked": include_untracked,
        "counts": {"workspace_in_boundary": len(inc_ws), "publish_in_boundary": len(inc_pub),
                   "both_sides": both_sides, "identical": identical,
                   "only_workspace": only_ws, "only_publish": only_pub,
                   "excluded_publish": len(exc_pub), "excluded_workspace": len(exc_ws)},
        "untracked_in_boundary": untracked_counts,
        "workflow_steps": steps, "workflow_triggers": triggers,
        "diffs": diffs,
        "excluded_sides": excluded_side,
        "excluded_by_rule": rule_rows,
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
        print("[boundary] 文件集口径：%s"
              % ("索引（已跟踪）∪ 未跟踪且未被 .gitignore —— 双向单侧检测（Phase39-Z1）"
                 if include_untracked else "--tracked-only：只看索引里的已跟踪文件（旧口径）"))
        print("[boundary] 未跟踪未提交（但已纳入机检）：workspace %d / publish %d"
              % (untracked_counts["workspace"], untracked_counts["publish"]))
        if args.list:
            print("\n-- 纳入清单（publish 侧） --")
            for p in sorted(inc_pub):
                print("   + %s" % p)
            print("\n-- 排除清单（两仓并集，含理由） --")
            seen = set()
            for g in sorted(list(exc_pub) + list(exc_ws)):
                if g in seen:
                    continue
                seen.add(g)
                reason, _state = (exc_pub.get(g) or exc_ws[g])
                print("   - %s\n       └ %s" % (g, reason))
        else:
            print("\n-- 排除统计（publish 侧） --")
            for reason, n in sorted(reason_counts.items(), key=lambda kv: -kv[1]):
                print("   %4d  %s" % (n, reason[:70]))
            print("\n-- 排除规则 × 侧别（排除项不参与差异判定；单侧差异一并列出理由，不静默吞掉） --")
            print("   %-30s %6s %6s %8s %8s" % ("pattern", "ws", "pub", "仅ws", "仅pub"))
            for row in rule_rows:
                print("   %-30s %6d %6d %8d %8d" % (row["pattern"], row["workspace"], row["publish"],
                                                     row["only_workspace"], row["only_publish"]))
                print("      └ %s" % row["reason"])
            print("   合计：排除 ws=%d / pub=%d；其中仅单侧 %d 条（仅工作仓 %d · 仅发布仓 %d）"
                  % (excluded_side["workspace"], excluded_side["publish"],
                     excluded_side["only_workspace"] + excluded_side["only_publish"],
                     excluded_side["only_workspace"], excluded_side["only_publish"]))
            print("\n" + REPO_OTHER_ROLE)

        print("\n[stats] 两仓都有 %d 条（其中逐字节一致 %d）｜仅单侧 %d 条（仅工作仓 %d · 仅发布仓 %d）"
              % (both_sides, identical, only_ws + only_pub, only_ws, only_pub))
        if ok:
            print("[OK] 零差异：%d 个构建图文件两仓逐字节一致（sha256）" % identical)
        else:
            print("\n[DIFF] %d 处差异（文件名 + 侧别 + 理由分类）：" % len(diffs))
            for d in diffs:
                print("   %-22s %-52s %s" % (d["kind"], diff_label(d["side"], d["reason"]), d["path"]))
            print("\n修法：内容差异按发布仓为准同步（cp <publish>/<path> <workspace>/<path> 反之视角色而定）；"
                  "单侧缺失按角色补齐（构建图文件两边都必须有）。同步后重跑本脚本；退出码 1。")

    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
