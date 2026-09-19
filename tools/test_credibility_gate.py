#!/usr/bin/env python3
"""credibility_gate 自测（D3 豁免口径的两个方向 + 负对照 + 严格模式）。

为什么有这个文件
    Phase36-QA6 §2.2 的结论是「豁免条款只写在 docs/planning/credibility_framework.md
    里，tools/credibility_gate.py 中不存在」——文档自述当时无任何机检证据。
    本脚本把 QA 当时用 /tmp 手搭的两套夹具固化成可复跑的自测，防回流。

两个方向都要验（缺一不可）：
    A. 已隔离(D1) figure 的污染出处  -> 必须「不报」D3（豁免生效）
    B. 公开 figure 的同样污染出处    -> 必须「报」D3（豁免不越界）
    C. 严格模式 --no-d3-exemption    -> 已隔离记录也必须报 D3（豁免可关）
    D. --negative-test 语义          -> 注入坏样本必须 exit 1
    E. 干净公开记录                  -> 必须 exit 0（不误报）
    F. 真实源库 data/modes_data.json -> gate 的 D3 计数必须为 0（豁免后）

用法：python3 tools/test_credibility_gate.py     （全过 exit 0，任一失败 exit 1）
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
GATE_SRC = REPO_ROOT / "tools" / "credibility_gate.py"
QUARANTINE_SRC = REPO_ROOT / "tools" / "_quarantine.py"
DATA_PATH = REPO_ROOT / "data" / "modes_data.json"

# 与 gate 的 D3 正则必然命中的工程痕迹样本（sha256 + 提交哈希）
POLLUTED_SOURCE = "Phase 21 入库与修复提交链（双镜像 sha256 记录：茅以升 96bdd4c4）"
CLEAN_SOURCE = "《论语·述而》"


class Failure(Exception):
    pass


def build_fixture(tmp: Path, modes: list[dict]) -> None:
    """把 gate + 隔离名单 + 自造数据放进临时夹具目录（不动真实仓）。
    """
    (tmp / "tools").mkdir(parents=True, exist_ok=True)
    (tmp / "data").mkdir(parents=True, exist_ok=True)
    shutil.copy(GATE_SRC, tmp / "tools" / "credibility_gate.py")
    shutil.copy(QUARANTINE_SRC, tmp / "tools" / "_quarantine.py")
    (tmp / "data" / "modes_data.json").write_text(
        json.dumps({"modes": modes}, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def run_gate(cwd: Path, *extra: str) -> tuple[int, str]:
    proc = subprocess.run(
        [sys.executable, "tools/credibility_gate.py", *extra],
        cwd=str(cwd), capture_output=True, text=True,
    )
    return proc.returncode, proc.stdout + proc.stderr


def d3_error_lines(out: str) -> list[str]:
    """只认「硬失败明细行」里的 D3，避免把汇总行 of which D3 ... 当成命中。
    """
    return [ln for ln in out.splitlines() if "::error::" in ln and "D3 出处污染" in ln]


def case_a_exempt_figure_not_reported(tmp: Path) -> None:
    """A. 豁免方向：已隔离 figure 的污染出处不得被报 D3。
    """
    build_fixture(tmp, [{
        "mode_code": "M-EXEMPT-TEST-001",
        "figure_code": "H-P23F-001",
        "source_chapter": POLLUTED_SOURCE,
        "key_quote_zh": "夹具引文",
    }])
    code, out = run_gate(tmp)
    if d3_error_lines(out):
        raise Failure("已隔离 figure 仍被报 D3（豁免未生效）:\n" + out)
    if "D1 伪人物" not in out:
        raise Failure("夹具自身不对：H-P23F-001 应触发 D1 硬 FAIL，实际未触发")
    if "M-EXEMPT-TEST-001" not in out:
        raise Failure("豁免面未如实公布：输出里找不到被豁免的 mode_code")
    if code != 1:
        raise Failure(f"D1 硬 FAIL 时退出码应为 1，实际 {code}")


def case_b_public_figure_reported(tmp: Path) -> None:
    """B. 非豁免方向：公开 figure 的同样污染必须报 D3。
    """
    build_fixture(tmp, [{
        "mode_code": "M-NONEXEMPT-TEST-001",
        "figure_code": "H-CLEAN-TEST-001",
        "source_chapter": POLLUTED_SOURCE,
        "key_quote_zh": "夹具引文",
    }])
    code, out = run_gate(tmp)
    if not d3_error_lines(out):
        raise Failure("公开 figure 的污染出处未被报 D3（豁免越界）:\n" + out)
    if code != 1:
        raise Failure(f"D3 硬 FAIL 时退出码应为 1，实际 {code}")


def case_c_strict_flag(tmp: Path) -> None:
    """C. --no-d3-exemption：豁免可关，已隔离记录的污染也必须报 D3。
    """
    build_fixture(tmp, [{
        "mode_code": "M-EXEMPT-TEST-001",
        "figure_code": "H-P23F-001",
        "source_chapter": POLLUTED_SOURCE,
    }])
    code, out = run_gate(tmp, "--no-d3-exemption")
    if not d3_error_lines(out):
        raise Failure("--no-d3-exemption 下仍未报 D3（严格模式失效）:\n" + out)
    if "D3 exemption: off" not in out:
        raise Failure("严格模式未在报告里标明 exemption off")
    if code != 1:
        raise Failure(f"严格模式应 exit 1，实际 {code}")


def case_d_negative_test(tmp: Path) -> None:
    """D. 负对照：注入 D3 坏样本必须 exit 1。
    """
    build_fixture(tmp, [{
        "mode_code": "M-CLEAN-TEST-001",
        "figure_code": "H-CLEAN-TEST-001",
        "source_chapter": CLEAN_SOURCE,
        "key_quote_zh": "夹具引文",
    }])
    code, out = run_gate(tmp, "--negative-test")
    if "[OK] Negative test PASSED" not in out:
        raise Failure("负对照未通过（注入的 D3 坏样本没被抓到）:\n" + out)
    if code != 1:
        raise Failure(f"负对照成功语义应为 exit 1，实际 {code}")


def case_e_clean_public_passes(tmp: Path) -> None:
    """E. 干净公开记录不得误报 -> exit 0。
    """
    build_fixture(tmp, [{
        "mode_code": "M-CLEAN-TEST-002",
        "figure_code": "H-CLEAN-TEST-002",
        "source_chapter": CLEAN_SOURCE,
        "key_quote_zh": "夹具引文",
    }])
    code, out = run_gate(tmp)
    if code != 0 or d3_error_lines(out):
        raise Failure(f"干净记录被误报（应 exit 0 / 无 D3）exit={code}:\n" + out)


def case_f_real_repo_data(tmp: Path) -> None:
    """F. 真实源库：豁免生效后 gate 的 D3 硬失败数必须为 0。

    注意：D1/D2/D6 的存量债务（隔离人物 / 伪造出处 / 悬空引用）由 CI 卡单独处置，
    本自测只断言 D3 一项，不把存量债务算成这里的失败。
    """
    if not DATA_PATH.exists():
        raise Failure(f"找不到源库数据 {DATA_PATH}")
    code, out = run_gate(REPO_ROOT, "--data-path", str(DATA_PATH))
    if "of which D3 出处污染: 0" not in out:
        raise Failure("真实源库 D3 计数不为 0:\n" + out)
    if "D3-exempted modes" not in out:
        raise Failure("真实源库跑 gate 时未报告豁免面（豁免可能被静默跳过）:\n" + out)


CASES = [
    ("A 已隔离 figure 的污染出处不报 D3", case_a_exempt_figure_not_reported),
    ("B 公开 figure 的污染出处必报 D3", case_b_public_figure_reported),
    ("C --no-d3-exemption 严格模式必报 D3", case_c_strict_flag),
    ("D --negative-test 注入坏样本必 exit 1", case_d_negative_test),
    ("E 干净公开记录必须 exit 0", case_e_clean_public_passes),
    ("F 真实源库 D3 计数为 0", case_f_real_repo_data),
]


def main() -> int:
    failed = 0
    with tempfile.TemporaryDirectory(prefix="cgate-selftest-") as tmpdir:
        base = Path(tmpdir)
        for idx, (name, fn) in enumerate(CASES):
            case_dir = base / f"case{idx}"
            case_dir.mkdir(parents=True)
            try:
                fn(case_dir)
                print(f"[PASS] {name}")
            except Failure as exc:
                failed += 1
                print(f"[FAIL] {name}\n       {exc}")
            except Exception as exc:  # noqa: BLE001
                failed += 1
                print(f"[ERROR] {name}: {type(exc).__name__}: {exc}")
    total = len(CASES)
    print(f"\n{total - failed}/{total} passed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
