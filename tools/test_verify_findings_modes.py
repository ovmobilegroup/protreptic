#!/usr/bin/env python3
"""verify_findings 两档模式自测（Phase37-X5）：存量冻结 / 新增即拦 + 计数过期归属。

为什么有这个文件
    `tools/verify_findings.py` 接进 CI 前必须先定两件事：
      1) 两档口径与 `tools/credibility_gate.py` 同构（存量冻结、新增即拦）；
      2) E 类「计数过期」的归属 —— 本卡决策为**警告（不红）**，否则每次数据更新都要额外
         刷新 findings.json 才能绿。
    这两件事必须有机检证据，不能只写在文档里，且负对照（成功语义 = exit 1）不能当 CI 步骤。

八项断言：
    1. 干净态 `--hard-fail`            -> exit 0（当前无存量硬失败）
    2. 干净态 `--legacy-report`        -> exit 0，且「存量 / 新增」两档分节都在
    3. 注入 1 条不存在的 mode_code     -> `--hard-fail` exit 1，且打印 ::error::NEW
    4. 移除注入（用原始 findings）      -> `--hard-fail` 复绿 exit 0
    5. 基线文件缺失                    -> exit 2（fail-closed，不静默放行）
    6. 冻结注入态后再跑                -> exit 0（基线内的存量只报告，不阻断）
    7. 冻结态下再注入第二条不同坏 code  -> exit 1（基线不是「一冻永绿」）
    8. 换一份现算计数不同的库          -> `--hard-fail` exit 0 且打印「计数过期」（E 只警告）

用法：python3 tools/test_verify_findings_modes.py   （全过 exit 0，任一失败 exit 1）
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
VERIFY = REPO_ROOT / "tools" / "verify_findings.py"
FINDINGS = REPO_ROOT / "data" / "audit" / "findings.json"
DATA = REPO_ROOT / "data" / "modes_data.json"
BASELINE = REPO_ROOT / "data" / "audit" / "findings_baseline.json"

BAD_CODE_1 = "M-QA37-X5-SELFTEST-BAD"
BAD_CODE_2 = "M-QA37-X5-SELFTEST-BAD2"

CHECKS = []


def run(findings: Path, data: Path, *args) -> tuple[int, str]:
    r = subprocess.run(
        [sys.executable, str(VERIFY), "--findings", str(findings), "--data-path", str(data), *args],
        cwd=str(REPO_ROOT), capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr


def write_findings_variant(tmp: Path, name: str, mutate) -> Path:
    payload = json.loads(FINDINGS.read_text(encoding="utf-8"))
    mutate(payload)
    out = tmp / name
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return out


def set_code(index: int, code: str):
    def mutate(payload):
        payload["findings"][index]["mode_code"] = code
    return mutate


def add_one_dangling_mode(payload):
    """库副本：新增 1 条**悬空引用**（引用必须是 M-<大写/数字>-<数字> 这种裸 code，
    才会被 build_audit_findings 计入 D6）-> 现算计数与 findings.json 的 summary 不再相同。"""
    template = dict(payload["modes"][0])
    template["mode_code"] = "M-QA37X5STALE-999"
    template["figure_code"] = "H-QA37X5STALE"
    template["related_modes"] = ["M-QA37X5NOPE-999"]
    payload["modes"].insert(0, template)


def check(name, cond, detail=""):
    CHECKS.append((name, bool(cond), detail))
    print("[%s] %s%s" % ("PASS" if cond else "FAIL", name,
                         ("  " + detail) if detail and not cond else ""))


def main() -> int:
    assert FINDINGS.is_file(), "findings.json 缺失: %s" % FINDINGS
    assert BASELINE.is_file(), "基线文件缺失: %s" % BASELINE

    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)

        code, out = run(FINDINGS, DATA, "--hard-fail")
        check("1 干净态 --hard-fail exit 0", code == 0, "exit=%d" % code)

        code, out = run(FINDINGS, DATA, "--legacy-report")
        check("2 干净态 --legacy-report exit 0 且两档分节都在",
              code == 0 and "存量（基线内，冻结）" in out and "新增（基线外，必拦）" in out,
              "exit=%d" % code)

        bad = write_findings_variant(tmp, "findings_bad.json", set_code(0, BAD_CODE_1))
        code, out = run(bad, DATA, "--hard-fail")
        check("3 注入不存在的 mode_code -> exit 1 且 ::error::NEW",
              code == 1 and ("::error::NEW " in out) and (BAD_CODE_1 in out), "exit=%d" % code)

        code, out = run(FINDINGS, DATA, "--hard-fail")
        check("4 移除注入（原始 findings）-> 复绿 exit 0", code == 0, "exit=%d" % code)

        code, out = run(FINDINGS, DATA, "--hard-fail", "--baseline", str(tmp / "nope.json"))
        check("5 基线缺失 -> exit 2（fail-closed）", code == 2, "exit=%d" % code)

        frozen = tmp / "frozen_baseline.json"
        code, _ = run(bad, DATA, "--write-baseline", "--baseline", str(frozen))
        wrote = code == 0 and frozen.is_file()
        code, out = run(bad, DATA, "--hard-fail", "--baseline", str(frozen))
        check("6 冻结注入态后 -> 存量不阻断 exit 0",
              wrote and code == 0, "write=%s exit=%d" % (wrote, code))

        bad2 = write_findings_variant(tmp, "findings_bad2.json", set_code(1, BAD_CODE_2))
        payload = json.loads(bad2.read_text(encoding="utf-8"))
        payload["findings"][0]["mode_code"] = BAD_CODE_1
        bad2.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        code, out = run(bad2, DATA, "--hard-fail", "--baseline", str(frozen))
        check("7 冻结态下再注入第二条坏 code -> exit 1",
              code == 1 and BAD_CODE_2 in out, "exit=%d" % code)

        stale_data = tmp / "modes_data_stale.json"
        lib = json.loads(DATA.read_text(encoding="utf-8"))
        add_one_dangling_mode(lib)
        stale_data.write_text(json.dumps(lib, ensure_ascii=False), encoding="utf-8")
        code, out = run(FINDINGS, stale_data, "--hard-fail")
        check("8 计数过期只警告不红（E 归属：警告）",
              code == 0 and "计数过期（警告，不阻断）" in out and "::warning::计数过期(E)" in out,
              "exit=%d" % code)

    failed = [c for c in CHECKS if not c[1]]
    print()
    print("%d/%d passed" % (len(CHECKS) - len(failed), len(CHECKS)))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
