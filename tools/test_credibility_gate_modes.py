#!/usr/bin/env python3
"""credibility_gate 两档模式自测（Phase37-X3）：存量冻结 / 新增即拦。

为什么有这个文件
    Phase36-QA6 §4.2 实测「照抄接入会让 Pages 永久变红（exit 1 / 533）」，本卡要的口径是
    **存量用基线冻结，新增即拦**。这个口径必须有机检证据，不能只写在文档里。

七项断言：
    1. 存量态 `--hard-fail`            -> exit 0（存量 527 条不阻断）
    2. 存量态 `--legacy-report`        -> exit 0，且列出存量条数
    3. 注入 1 条新 D3 坏样本           -> `--hard-fail` exit 1，且打印 ::error::NEW
    4. 改写存量坏引用的说明文字        -> `--hard-fail` 仍 exit 0（指纹不含说明文字）
    5. 基线文件缺失                    -> exit 2（fail-closed，不静默放行）
    6. `--data-path` 两份数据          -> 结论必须不同（证明参数真的生效）
    7. `--write-baseline` 重新冻结后可继续跑 -> exit 0

用法：python3 tools/test_credibility_gate_modes.py   （全过 exit 0，任一失败 exit 1）
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
GATE = REPO_ROOT / "tools" / "credibility_gate.py"
DATA = REPO_ROOT / "data" / "modes_data.json"
BASELINE = REPO_ROOT / "data" / "audit" / "credibility_baseline.json"
INJECTED_CODE = "M-QA37-X3-SELFTEST-BAD"


def run(*args):
    r = subprocess.run([sys.executable, str(GATE), *args], cwd=str(REPO_ROOT),
                       capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr


def write_variant(tmp: Path, mutate, name: str) -> Path:
    data = json.loads(DATA.read_text(encoding="utf-8"))
    mutate(data)
    out = tmp / name
    out.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    return out


def inject_new_d3(data):
    bad = dict(data["modes"][0])
    bad["mode_code"] = INJECTED_CODE
    bad["figure_code"] = "H-WYM-001"
    bad["source_chapter"] = "Phase 21 入库与修复提交链（双镜像 sha256 记录：茅以升 96bdd4c4）"
    data["modes"].insert(0, bad)


def rewrite_legacy_ref_text(data):
    """改写一条存量 D6 坏引用的括号说明文字（code 不变）——不该被判为新增。"""
    for m in data["modes"]:
        refs = []
        for x in (m.get("related_modes") or []):
            s = str(x)
            if s.startswith("M-HER-005（"):
                s = "M-HER-005（说明文字已改写：code 未变）"
            refs.append(s)
        m["related_modes"] = refs


CHECKS = []


def check(name, cond, detail=""):
    CHECKS.append((name, bool(cond), detail))
    print("[%s] %s%s" % ("PASS" if cond else "FAIL", name, ("  " + detail) if detail and not cond else ""))


def main() -> int:
    assert BASELINE.is_file(), "基线文件缺失: %s" % BASELINE
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)

        code, out = run("--hard-fail", "--data-path", str(DATA))
        check("1 存量态 --hard-fail exit 0", code == 0, "exit=%d" % code)

        code, out = run("--legacy-report", "--data-path", str(DATA))
        check("2 存量态 --legacy-report exit 0 且列出存量",
              code == 0 and "存量（基线内，冻结）" in out, "exit=%d" % code)

        bad = write_variant(tmp, inject_new_d3, "injected.json")
        code, out = run("--hard-fail", "--data-path", str(bad))
        check("3 新增 D3 坏样本 -> exit 1 且 ::error::NEW",
              code == 1 and ("::error::NEW " + INJECTED_CODE) in out, "exit=%d" % code)

        edited = write_variant(tmp, rewrite_legacy_ref_text, "legacy_edit.json")
        code, out = run("--hard-fail", "--data-path", str(edited))
        check("4 改写存量引用说明文字 -> 仍 exit 0", code == 0, "exit=%d" % code)

        code, out = run("--hard-fail", "--data-path", str(DATA),
                        "--baseline", str(tmp / "nope.json"))
        check("5 基线缺失 -> exit 2（fail-closed）", code == 2, "exit=%d" % code)

        c_bad, _ = run("--hard-fail", "--data-path", str(bad))
        c_clean, _ = run("--hard-fail", "--data-path", str(DATA))
        check("6 --data-path 两份数据结论不同", c_bad != c_clean,
              "bad=%d clean=%d" % (c_bad, c_clean))

        fresh = tmp / "fresh_baseline.json"
        code, out = run("--write-baseline", "--data-path", str(DATA), "--baseline", str(fresh))
        ok_written = code == 0 and fresh.is_file()
        code, out = run("--hard-fail", "--data-path", str(DATA), "--baseline", str(fresh))
        check("7 --write-baseline 重新冻结后可继续跑 exit 0",
              ok_written and code == 0, "write=%s exit=%d" % (ok_written, code))

    failed = [c for c in CHECKS if not c[1]]
    print()
    print("%d/%d passed" % (len(CHECKS) - len(failed), len(CHECKS)))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
