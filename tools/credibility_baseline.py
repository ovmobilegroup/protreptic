#!/usr/bin/env python3
"""可信度门「存量冻结 / 新增即拦」基线内核（Phase37-X3）。

为什么要有这个文件
    `tools/credibility_gate.py` 对**所有**硬失败（D1/D2/D3/D6）一律 FAIL。源库当前
    仍有 527 条存量硬失败（D1 60 / D2 9 / D6 458），照抄接进 CI 的后果是把线上发布链
    （Pages）永久打红 —— 部署永远 skip（QA6 §4.2）。

    本模块把判定内核独立出来，给 gate 提供「两档模式」所需的分类能力：

      * `--legacy-report`  存量（基线内）与新增都列出来，**一律 exit 0**；
      * `--hard-fail`      存量只报告（::notice），**基线外的任何一条硬失败 = exit 1**。

    口径：**存量用基线文件（baseline）冻结，新增即拦**。
    基线文件 = `data/audit/credibility_baseline.json`（入库、两仓字节一致），
    由 `python3 tools/credibility_gate.py --write-baseline` 重新冻结。

指纹（fingerprint）口径 —— 为什么不是「整条消息取哈希」
    对整条消息取哈希，会把「给存量模式改一句 source_chapter 说明文字」也算成新增，
    于是存量债务会把无关的编辑拦下来。指纹改为
    **(mode_code, 规则, 规则内稳定键)**，稳定键取「这条违规到底是什么」：

      D1 伪人物      key = figure_code
      D2 伪造出处    key = 命中的伪造书名
      D3 出处污染    key = 命中的污染正则
      D6 悬空引用    key = 字段(related_modes/cross_references) + 被引用的 code 主体

    于是：新模式 / 新 figure_code / 新伪造书名 / 新污染模式 / 新悬空引用
    必然产生基线里没有的指纹 -> `--hard-fail` 拦下；而存量条目的文字编辑不误报。
    无法按已知格式解析的失败退化为「整条消息」作指纹（保守：不进基线就会被拦）。
"""

from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

SCHEMA = "protreptic.credibility_baseline/v1"
POLICY = ("存量冻结、新增即拦：本文件登记的硬失败只报告不阻断（exit 0）；"
          "任何未登记的硬失败在 --hard-fail 下 exit 1")

# 消息格式由 tools/credibility_gate.py 的 check_d1/d2/d3/d6_* 生成
RE_MODE_CODE = re.compile(r"^\[([^\]]+)\]\s*(.*)$", re.DOTALL)
RE_D1 = re.compile(r"^D1 伪人物:\s*figure_code=(\S+)\s")
RE_D2 = re.compile(r"^D2 伪造出处:.*?'(.*?)'")
RE_D3 = re.compile(r"^D3 出处污染:.*?'(.*?)'")
RE_D6 = re.compile(r"^D6 悬空引用:\s*(\S+)\s*指向不存在的 mode_code=(.+)$", re.DOTALL)
RE_REF_CODE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.\-]*")


def rule_of(rest: str) -> str:
    m = re.match(r"^(D\d)\b", rest or "")
    return m.group(1) if m else "??"


def stable_key(rule: str, rest: str) -> str:
    """规则内稳定键；取不到就退回整条消息（保守）。"""
    if rule == "D1":
        m = RE_D1.match(rest)
        if m:
            return m.group(1)
    elif rule == "D2":
        m = RE_D2.match(rest)
        if m:
            return m.group(1)
    elif rule == "D3":
        m = RE_D3.match(rest)
        if m:
            return m.group(1)
    elif rule == "D6":
        m = RE_D6.match(rest)
        if m:
            field, ref = m.group(1), m.group(2).strip()
            code = RE_REF_CODE.match(ref)
            # related_modes 里混进了「M-XXX-001（说明文字）」这种带说明的引用，
            # 只取 code 主体，让「改说明」不产生新指纹。
            return "%s=%s" % (field, code.group(0) if code else ref)
    return rest


def fingerprint(finding: str) -> str:
    """一条硬失败 -> 稳定指纹 'mode_code|规则|稳定键'。"""
    m = RE_MODE_CODE.match(finding or "")
    if not m:
        return "UNPARSED|??|%s" % finding
    mode_code, rest = m.group(1), m.group(2)
    rule = rule_of(rest)
    return "%s|%s|%s" % (mode_code, rule, stable_key(rule, rest))


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load_baseline(path: Path):
    if not path.is_file():
        return None
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def build_baseline(failures, data_path=None) -> dict:
    """把当前全部硬失败冻结成基线（按指纹排序，确定性输出）。"""
    entries = {}
    for f in failures:
        fid = fingerprint(f)
        if fid in entries:
            continue
        m = RE_MODE_CODE.match(f)
        rest = m.group(2) if m else f
        r = rule_of(rest)
        entries[fid] = {
            "id": fid,
            "mode_code": (m.group(1) if m else "UNKNOWN"),
            "rule": r,
            "key": stable_key(r, rest),
            "sample": f[:200],
        }
    counts = {"total": len(failures), "D1": 0, "D2": 0, "D3": 0, "D6": 0}
    modes = set()
    for e in entries.values():
        counts[e["rule"]] = counts.get(e["rule"], 0) + 1
        modes.add(e["mode_code"])
    counts["distinct_fingerprints"] = len(entries)
    counts["modes_with_findings"] = len(modes)
    return {
        "schema": SCHEMA,
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "generated_by": "tools/credibility_gate.py --write-baseline",
        "policy": POLICY,
        "data_path": str(data_path) if data_path else None,
        "data_sha256": sha256_file(data_path) if data_path and data_path.is_file() else None,
        "counts": counts,
        "entries": [entries[k] for k in sorted(entries)],
    }


def save_baseline(baseline: dict, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(baseline, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def classify(failures, baseline: dict) -> dict:
    """当前硬失败 vs 基线 -> (legacy, new, stale)。"""
    known = {e["id"]: e for e in baseline.get("entries", [])}
    legacy, new = [], []
    seen = set()
    for f in failures:
        fid = fingerprint(f)
        seen.add(fid)
        (legacy if fid in known else new).append((fid, f))
    stale = [known[i] for i in known if i not in seen]
    by_rule = {"D1": 0, "D2": 0, "D3": 0, "D6": 0}
    for fid, _ in legacy:
        r = fid.split("|")[1]
        by_rule[r] = by_rule.get(r, 0) + 1
    return {"legacy": legacy, "new": new, "stale": stale, "legacy_by_rule": by_rule}


def run_mode(mode, failures, warnings, exempted, baseline_path, data_path, limit=1000) -> int:
    """`--legacy-report` / `--hard-fail` 的打印与退出码。

    legacy-report -> 一律 exit 0（只报告不阻断）
    hard-fail     -> 基线外任何一条硬失败 exit 1；正常 exit 0
    基线缺失       -> exit 2（fail-closed：没有基线就谈不上存量冻结，宁可红）
    """
    baseline = load_baseline(baseline_path)
    print("=== CREDIBILITY GATE · 存量/新增两档 ===")
    print("mode: %s" % mode)
    print("resolved data path:     %s (exists=%s)" % (data_path, data_path.is_file()))
    print("resolved baseline path: %s (exists=%s)" % (baseline_path, baseline_path.is_file()))
    print("hard failures on this dataset: %d" % len(failures))
    if baseline is None:
        print("[FAIL] baseline file missing: %s" % baseline_path)
        print("       先冻结基线: python3 tools/credibility_gate.py --write-baseline "
              "--data-path data/modes_data.json")
        return 2

    b = baseline.get("counts", {})
    print("baseline frozen at %s (total=%s, fingerprints=%s, D1=%s D2=%s D3=%s D6=%s)" % (
        baseline.get("generated_at"), b.get("total"), b.get("distinct_fingerprints"),
        b.get("D1"), b.get("D2"), b.get("D3"), b.get("D6")))
    print("baseline data_sha256: %s" % baseline.get("data_sha256"))
    print("current  data_sha256: %s" % (sha256_file(data_path) if data_path.is_file() else "N/A"))
    print("D3 exemption: on, exempted modes: %d" % len(exempted))

    res = classify(failures, baseline)
    legacy, new, stale = res["legacy"], res["new"], res["stale"]
    lr = res["legacy_by_rule"]

    print("")
    print("--- 存量（基线内，冻结）: %d 条 [D1=%d D2=%d D3=%d D6=%d] ---" % (
        len(legacy), lr.get("D1", 0), lr.get("D2", 0), lr.get("D3", 0), lr.get("D6", 0)))
    for fid, f in legacy[:limit]:
        print("  ::notice::LEGACY %s | %s" % (fid, f))
    if len(legacy) > limit:
        print("  ... and %d more legacy findings" % (len(legacy) - limit))

    print("")
    print("--- 新增（基线外，必拦）: %d 条 ---" % len(new))
    if not new:
        print("  (none)")
    for fid, f in new[:limit]:
        print("  ::error::NEW %s | %s" % (fid, f))
    if len(new) > limit:
        print("  ... and %d more new findings" % (len(new) - limit))

    if stale:
        print("")
        print("--- 基线里已不再成立（可重新冻结）: %d 条 ---" % len(stale))
        for e in stale[:50]:
            print("  ::warning::STALE %s" % e["id"])
        if len(stale) > 50:
            print("  ... and %d more stale entries" % (len(stale) - 50))

    if warnings:
        print("")
        print("warnings (D4/D5, 非阻断): %d" % len(warnings))

    print("")
    if mode == "legacy-report":
        print("[OK] legacy-report: 存量 %d 条 / 新增 %d 条 —— 只报告，不阻断 (exit 0)"
              % (len(legacy), len(new)))
        return 0
    if new:
        print("[FAIL] hard-fail: %d 条新增硬失败（基线外）-> exit 1（存量 %d 条已冻结）"
              % (len(new), len(legacy)))
        return 1
    print("[OK] hard-fail: 无新增硬失败（存量 %d 条已冻结）-> exit 0" % len(legacy))
    return 0
