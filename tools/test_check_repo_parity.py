#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_repo_parity 双向单侧自测（Phase39-Z1）：修盲区 + 负对照。

为什么有这个文件
    船长独立核验发现：旧口径只枚举 `git ls-files`（**索引里的已跟踪文件**），
    在构建图内造一个「只在工作仓」的未跟踪文件（docs/qa/__parity_probe__.md），
    脚本仍输出 `[OK] 零差异：1325 ...` 并 exit 0 —— 盲区。真实事故同型：
    `docs/qa/phase38_acceptance.md` 曾只在工作仓、发布仓缺失。
    本项目铁律「任何机检规则都要有负对照测试」：本自测用两个临时 git 仓现场复现
    四个方向（只在工作仓 / 只在发布仓 / 内容不同 / 排除口径不回退），
    外加边界自检（pages.yml 多一个构建步骤 → exit 2）与排除规则硬自检。

十九项断言
     1. 干净态                                  -> exit 0，打印零差异
     2. 合法边界（pages.yml 一个构建步骤）        -> exit 0（边界自检不误报）
     3. 工作仓**未跟踪**新增构建图文件           -> exit 1 + MISSING_IN_PUBLISH + 理由「未跟踪」
     4. 删掉该文件                              -> exit 0（回归）
     5. 同一文件**已 git add**（已跟踪）         -> exit 1 + MISSING_IN_PUBLISH + 理由「已跟踪」
     6. 发布仓**未跟踪**新增构建图文件           -> exit 1 + MISSING_IN_WORKSPACE（反向同样有牙）
     7. 两仓同路径内容不同                      -> exit 1 + CONTENT_DIFF
     8. 排除口径不回退（docs/archive/*、*.bak*） -> exit 0，且报告按「规则 × 侧别」列出
     9. `--tracked-only`（旧口径）对本项 3       -> exit 0（证明盲区确实出在「只看索引」）
    10. pages.yml 多一个构建步骤                -> exit 2（边界过期，回归）
    11. exclusion_guard 合成输入                -> 撞构建图/触发器必须报，干净输入必须空
    12. workspace == publish 自比                        -> exit 2（假 OK 路径同样堵上）
    13. 机检脚本与其负对照自测同在纳入清单              -> TOOL_FILES 自洽（不得单侧漂移）

用法：python3 tools/test_check_repo_parity.py   （全过 exit 0，任一失败 exit 1）
"""

from __future__ import annotations

import importlib.util
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PARITY = REPO_ROOT / "tools" / "check_repo_parity.py"

PAGES_YML = """name: probe
on:
  push:
    paths:
      - 'docs/**'
      - 'tools/export_static_site.py'
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - run: python3 tools/export_static_site.py
"""

BASE_FILES = {
    "mkdocs.pages.yml": "site_name: probe\n",
    "docs/index.md": "# probe\n",
    "tools/export_static_site.py": "#!/usr/bin/env python3\nprint('export')\n",
    ".github/workflows/pages.yml": PAGES_YML,
}

CHECKS = []


def check(name, ok, detail=""):
    CHECKS.append((name, bool(ok), detail))
    print("%s %s%s" % ("[PASS]" if ok else "[FAIL]", name, ("  —— " + detail) if detail else ""))


def git(repo, *args):
    subprocess.run(["git", "-C", str(repo)] + list(args), check=True,
                   capture_output=True, text=True)


def scaffold(root, name):
    """造一个最小两仓（各自 git init + 构建图文件入索引），返回 (ws, pub)。"""
    ws = Path(root) / (name + "-workspace")
    pub = Path(root) / (name + "-publish")
    for repo in (ws, pub):
        repo.mkdir(parents=True)
        git(repo, "init", "-q")
        for rel, body in BASE_FILES.items():
            f = repo / rel
            f.parent.mkdir(parents=True, exist_ok=True)
            f.write_text(body, encoding="utf-8")
        git(repo, "add", "-A")
    return ws, pub


def run_parity(ws, pub, *extra):
    r = subprocess.run([sys.executable, str(PARITY), "--workspace", str(ws),
                        "--publish", str(pub), *extra],
                       cwd=str(REPO_ROOT), capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr


def load_parity_module():
    spec = importlib.util.spec_from_file_location("crp_under_test", str(PARITY))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    # ---- 1 / 2：干净态与边界自检不误报 ----
    with tempfile.TemporaryDirectory() as tmp:
        ws, pub = scaffold(tmp, "clean")
        code, out = run_parity(ws, pub)
        check("1 干净态 exit 0 + 零差异", code == 0 and "[OK] 零差异" in out,
              "exit=%d" % code)
        check("2 合法边界不误报（16 步清单里有的构建步骤）",
              "边界自检通过" in out and "边界过期" not in out, out.splitlines()[2][:60])

    # ---- 3 / 4 / 5 / 9：只在工作仓（未跟踪 / 已跟踪）与旧口径对照 ----
    with tempfile.TemporaryDirectory() as tmp:
        ws, pub = scaffold(tmp, "onlyws")
        probe = ws / "docs" / "probe.md"
        probe.write_text("# 只在工作仓（未跟踪）\n", encoding="utf-8")
        code, out = run_parity(ws, pub)
        check("3 工作仓未跟踪新增 -> exit 1 + MISSING_IN_PUBLISH + 理由未跟踪",
              code == 1 and "MISSING_IN_PUBLISH" in out and "未跟踪" in out
              and "[OK] 零差异" not in out, "exit=%d" % code)
        code, out = run_parity(ws, pub, "--tracked-only")
        check("9 --tracked-only（旧口径）对同一文件 exit 0 = 复现盲区",
              code == 0 and "[OK] 零差异" in out, "exit=%d" % code)
        probe.unlink()
        code, out = run_parity(ws, pub)
        check("4 删掉该文件 -> exit 0（回归）", code == 0 and "[OK] 零差异" in out,
              "exit=%d" % code)
        probe.write_text("# 只在工作仓（已跟踪）\n", encoding="utf-8")
        git(ws, "add", "docs/probe.md")
        code, out = run_parity(ws, pub)
        check("5 工作仓已跟踪新增 -> exit 1 + MISSING_IN_PUBLISH + 理由已跟踪",
              code == 1 and "MISSING_IN_PUBLISH" in out and "已跟踪" in out,
              "exit=%d" % code)
        check("5b 差异行同时给出侧别（仅工作仓）",
              "仅工作仓" in out and "docs/probe.md" in out, "")

    # ---- 6：反向（只在发布仓） ----
    with tempfile.TemporaryDirectory() as tmp:
        ws, pub = scaffold(tmp, "onlypub")
        (pub / "docs" / "pub_probe.md").write_text("# 只在发布仓\n", encoding="utf-8")
        code, out = run_parity(ws, pub)
        check("6 发布仓单侧新增 -> exit 1 + MISSING_IN_WORKSPACE + 侧别仅发布仓",
              code == 1 and "MISSING_IN_WORKSPACE" in out and "仅发布仓" in out,
              "exit=%d" % code)

    # ---- 7：内容不同 ----
    with tempfile.TemporaryDirectory() as tmp:
        ws, pub = scaffold(tmp, "diff")
        (ws / "docs" / "index.md").write_text("# probe changed\n", encoding="utf-8")
        code, out = run_parity(ws, pub)
        check("7 两仓都有但内容不同 -> exit 1 + CONTENT_DIFF",
              code == 1 and "CONTENT_DIFF" in out and "内容不同" in out, "exit=%d" % code)

    # ---- 8：排除口径不回退 ----
    with tempfile.TemporaryDirectory() as tmp:
        ws, pub = scaffold(tmp, "excluded")
        (ws / "docs" / "archive").mkdir(parents=True)
        (ws / "docs" / "archive" / "old.md").write_text("# 归档\n", encoding="utf-8")
        (ws / "docs" / "index.md.bak").write_text("# 备份\n", encoding="utf-8")
        (pub / "docs" / "archive").mkdir(parents=True)
        (pub / "docs" / "archive" / "old.md").write_text("# 归档\n", encoding="utf-8")
        code, out = run_parity(ws, pub)
        check("8 排除项不参与差异判定 -> exit 0", code == 0 and "[OK] 零差异" in out,
              "exit=%d" % code)
        check("8b 报告列出排除规则 × 侧别（含 docs/archive/* 与 *.bak*）",
              "docs/archive/*" in out and "*.bak*" in out and "排除规则 × 侧别" in out, "")
        check("8c 排除合计里有「仅单侧」计数（不静默吞掉）", "其中仅单侧" in out, "")

    # ---- 10：边界过期（pages.yml 多一个构建步骤）→ exit 2 ----
    with tempfile.TemporaryDirectory() as tmp:
        ws, pub = scaffold(tmp, "stale")
        wf = pub / ".github" / "workflows" / "pages.yml"
        wf.write_text(PAGES_YML.replace(
            "      - run: python3 tools/export_static_site.py\n",
            "      - run: python3 tools/export_static_site.py\n"
            "      - run: python3 tools/fake_new_step.py\n"), encoding="utf-8")
        code, out = run_parity(ws, pub)
        check("10 pages.yml 多一个构建步骤 -> exit 2 且点名",
              code == 2 and "边界过期" in out and "tools/fake_new_step.py" in out,
              "exit=%d" % code)

    # ---- 11：排除规则硬自检（合成输入） ----
    mod = load_parity_module()
    swallowed = mod.exclusion_guard(
        {"tools/credibility_gate.py": ("x", "tracked")}, {}, [])
    check("11a 排除撞上纳入清单 -> 必须报",
          len(swallowed) == 1 and "纳入清单" in swallowed[0][1], repr(swallowed))
    swallowed = mod.exclusion_guard(
        {}, {"data/modes_data.json": ("x", "tracked")}, ["data/modes_data.json"])
    check("11b 排除撞上未豁免触发器 -> 必须报",
          len(swallowed) == 1 and "触发器" in swallowed[0][1], repr(swallowed))
    swallowed = mod.exclusion_guard(
        {}, {"api/protreptic.db": ("x", "tracked")}, ["api/protreptic.db"])
    check("11c EXCLUDED_TRIGGERS 里已豁免的路径 -> 不报",
          swallowed == [], repr(swallowed))


    # ---- 12：自比防护（workspace == publish）-> exit 2 ----
    with tempfile.TemporaryDirectory() as tmp:
        ws, pub = scaffold(tmp, "selfcmp")
        code, out = run_parity(ws, ws)
        check("12 workspace 与 publish 同仓 -> exit 2（自比会让单侧检测恒为 0、假 OK）",
              code == 2 and "同一个仓" in out, "exit=%d" % code)
        code, out = run_parity(ws, pub)
        check("12b 换回正常两仓 -> exit 0（守卫不误伤）", code == 0, "exit=%d" % code)

    # ---- 13：机检脚本与它的负对照自测都在纳入清单（不得单侧漂移） ----
    mod = load_parity_module()
    check("13 check_repo_parity.py 与 test_check_repo_parity.py 均在 TOOL_FILES",
          "tools/check_repo_parity.py" in mod.TOOL_FILES
          and "tools/test_check_repo_parity.py" in mod.TOOL_FILES, "")
    failed = [c for c in CHECKS if not c[1]]
    print()
    print("%d/%d passed" % (len(CHECKS) - len(failed), len(CHECKS)))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
