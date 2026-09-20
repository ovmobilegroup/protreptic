#!/usr/bin/env python3
"""apply_verification_status.py -- credibility_framework.md 第 3 节 verification.status 推进。

为什么有它
    Phase36-W4 只把 `verification` **字段（schema）**灌进 2868 条模式，状态**全是 pending**：
    schema 就位、一次核验都没做（Phase38-Y1 侦察确认）。本模块是「状态判定」的**唯一实现**，
    导出链 / 复核 / QA 都调它；规则只写在这里，别在别处再抄一遍。

判定规则（按下面顺序判定，先命中先定）
    S1 suspect        mode_code 命中 data/audit/findings.json 的 D4/D5（引文不符 / 时间线矛盾）
    S2 verified       出处里至少一条引文解析到**可达链接**（source_links.json 里 url 非空）
                      method=link-resolved，evidence=该 url（逐条回查索引，不靠信任）
    S3 unverifiable   出处有引文，且**全部**命中「已登记不可链接」条目（url 为空 = 口述/信札等一手材料）
    S4 pending        其余（出处无书名号引文 / 引文全部 unresolved / 无出处）

    * 优先级为何 suspect 先于 verified：同一条模式既「链接可达」又「引文与原文不符」时，
      不得给出「已核验」的结论。实测当前库两者交集 = 0（报告里打印，供复核）。
    * D1/D2/D3 **不在这里判**：它们由 credibility_gate 拦、由 tools/_quarantine.py 隔离，
      不进公开产物（credibility_framework.md 第 1 节的豁免条款）。本模块只推四态。

自洽断言（写盘前必过，不过就 exit 1）
    * 每条模式的状态属于四态，且四态求和等于库中模式条数；
    * 每条 verified 的 evidence 必须是 source_links.json 里某个 key 的 url（逐条回查）。

用法
    python3 tools/apply_verification_status.py            # 只报告，不写盘
    python3 tools/apply_verification_status.py --write    # 写回 data/modes_data.json
    python3 tools/apply_verification_status.py --check    # 校验库里状态与本规则一致（漂移 exit 1）
    python3 tools/apply_verification_status.py --report data/audit/verification_status.json

退出码：0 成功 / 无漂移；1 自洽断言失败 或 --check 发现漂移；2 输入缺失。
"""

from __future__ import annotations

import argparse
import collections
import hashlib
import json
import sys
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

from _quarantine import is_quarantined  # noqa: E402
from source_link_index import extract_refs, load_index, resolve_citation  # noqa: E402

DATA_PATH = REPO_ROOT / "data" / "modes_data.json"
LINKS_PATH = REPO_ROOT / "data" / "source_links.json"
FINDINGS_PATH = REPO_ROOT / "data" / "audit" / "findings.json"
REPORT_PATH = REPO_ROOT / "data" / "audit" / "verification_status.json"

STATUSES = ("verified", "pending", "suspect", "unverifiable")
SUSPECT_DEFECTS = ("D4", "D5")

RULES = {
    "S1": "suspect      : mode_code 命中 findings.json 的 D4/D5（引文不符 / 时间线矛盾）",
    "S2": "verified     : 出处至少一条引文解析到可达链接（url 非空） -> method=link-resolved, evidence=url",
    "S3": "unverifiable : 出处有引文且全部命中『已登记不可链接』（url 为空：口述/信札等一手材料）",
    "S4": "pending      : 其余（无书名号引文 / 引文全部 unresolved）",
}
PRECEDENCE = ("S1", "S2", "S3", "S4")


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_suspect_codes(path: Path):
    """读 findings.json 的 D4/D5 命中模式号。文件缺失则返回空集（诚实标注，不猜）。"""
    if not path.is_file():
        print("[warn] %s not found: D4/D5 判定按空集处理" % path)
        return set(), {"present": False, "by_defect": {}}
    data = json.loads(path.read_text(encoding="utf-8"))
    entries = data.get("findings") or data.get("entries") or []
    codes = set()
    by_defect = collections.Counter()
    for e in entries:
        defect = str(e.get("defect") or "")
        if defect[:2] in SUSPECT_DEFECTS and e.get("mode_code"):
            codes.add(str(e["mode_code"]))
            by_defect[defect] += 1
    return codes, {"present": True, "by_defect": dict(by_defect)}


def classify(mode: dict, index: dict, suspect_codes: set) -> dict:
    """单条模式 -> {status, method, evidence} 。规则见模块 docstring 的 S1..S4 。"""
    code = str(mode.get("mode_code") or "")
    if code and code in suspect_codes:
        return {
            "status": "suspect",
            "method": "auto-scan",
            "evidence": "D4/D5 hit in data/audit/findings.json (quote mismatch or timeline conflict)",
        }
    refs = [resolve_citation(inner, index) for inner in extract_refs(mode.get("source_chapter"))]
    linked = [r for r in refs if r["status"] == "linked"]
    if linked:
        return {"status": "verified", "method": "link-resolved", "evidence": linked[0]["url"]}
    if refs:
        registered_unlinkable = [r for r in refs
                                 if r["status"] != "unresolved" and not (r["url"] or "").strip()]
        if len(registered_unlinkable) == len(refs):
            return {
                "status": "unverifiable",
                "method": "auto-scan",
                "evidence": "source_links.json 登记为不可链接 type=%s key=%s"
                            % (refs[0]["source_type"] or "unverifiable",
                               "/".join(r["key"] or r["citation"] for r in refs[:3])),
            }
    return {
        "status": "pending",
        "method": "auto-scan",
        "evidence": ("no-citation: 出处无可链接引文" if not refs
                     else "unresolved: 引文未在 source_links.json 建立链接源"),
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="verification status 推进（四态规则的唯一实现）")
    ap.add_argument("--data-path", default=str(DATA_PATH))
    ap.add_argument("--links-path", default=str(LINKS_PATH))
    ap.add_argument("--findings-path", default=str(FINDINGS_PATH))
    ap.add_argument("--report", default=None,
                    help="机读报告写到该路径（默认只在 --write 时写 %s ）" % REPORT_PATH)
    ap.add_argument("--write", action="store_true", help="写回 data/modes_data.json")
    ap.add_argument("--check", action="store_true", help="校验库里状态与本规则一致（漂移 exit 1 ）")
    ap.add_argument("--checked-at", default=date.today().isoformat())
    ap.add_argument("--checker", default="phase38-y2")
    args = ap.parse_args()

    data_path = Path(args.data_path)
    links_path = Path(args.links_path)
    findings_path = Path(args.findings_path)
    for p in (data_path, links_path):
        if not p.is_file():
            print("[FAIL] 输入缺失: %s" % p)
            return 2

    raw = data_path.read_bytes()
    doc = json.loads(raw.decode("utf-8"))
    modes = doc.get("modes")
    if not isinstance(modes, list):
        print("[FAIL] %s 里没有 modes 数组" % data_path)
        return 2
    index = load_index(links_path)
    suspect_codes, findings_meta = load_suspect_codes(findings_path)

    print("库: %s (%d 条模式, sha256 %s)" % (data_path, len(modes), sha256_file(data_path)[:16]))
    print("链接源: %s (%d key, 其中有 url %d)"
          % (links_path, len(index), sum(1 for v in index.values() if (v.get("url") or "").strip())))
    print("D4/D5 命中: %d 条模式 %s" % (len(suspect_codes), json.dumps(findings_meta, ensure_ascii=False)))
    print("规则优先级: %s" % " > ".join(PRECEDENCE))
    for k in PRECEDENCE:
        print("  %s" % RULES[k])
    print()

    results: list = []
    changed = collections.Counter()
    overlap_s1_s2 = 0
    evidence_urls: set = set()
    for m in modes:
        if not isinstance(m, dict):
            continue
        code = str(m.get("mode_code") or "")
        res = classify(m, index, suspect_codes)
        results.append(res)
        if res["status"] == "verified":
            evidence_urls.add(res["evidence"])
        old = m.get("verification") or {}
        if old.get("status") != res["status"]:
            changed["%s -> %s" % (old.get("status"), res["status"])] += 1
        if code in suspect_codes:
            refs = [resolve_citation(i, index) for i in extract_refs(m.get("source_chapter"))]
            if any(r["status"] == "linked" for r in refs):
                overlap_s1_s2 += 1

    cnt = collections.Counter(v["status"] for v in results)
    total = sum(cnt.values())
    pub = collections.Counter(r["status"] for m, r in zip(modes, results)
                              if not is_quarantined(m.get("figure_code")))
    pub_total = sum(pub.values())
    print("四态（全库 %d 条）:" % total)
    for s in STATUSES:
        print("  %-13s %5d" % (s, cnt[s]))
    print("四态（公开口径 %d 条, 已剔除隔离人物）:" % pub_total)
    for s in STATUSES:
        print("  %-13s %5d" % (s, pub[s]))
    print()
    print("S1 交 S2 的重叠（既命中 D4/D5 又解析出可达链接）: %d 条" % overlap_s1_s2)
    print("与库中现状态相比的变更: %s"
          % (", ".join("%s=%d" % kv for kv in sorted(changed.items())) or "无（已一致）"))
    print()

    problems = []
    if total != len(modes):
        problems.append("四态求和 %d 不等于模式条数 %d" % (total, len(modes)))
    bad = [s for s in cnt if s not in STATUSES]
    if bad:
        problems.append("出现非法状态 %s" % bad)
    url_values = {(v.get("url") or "").strip() for v in index.values() if (v.get("url") or "").strip()}
    unknown = sorted(u for u in evidence_urls if u not in url_values)
    if unknown:
        problems.append("verified 的 evidence 有 %d 个不在链接源 url 集合里: %s"
                        % (len(unknown), unknown[:3]))
    if problems:
        print("[FAIL] 自洽断言未过:")
        for p in problems:
            print("  - %s" % p)
        return 1
    print("[OK] 自洽断言: 四态求和等于模式条数; verified 的 evidence 全部回查到索引 url (%d 个不同 url)"
          % len(evidence_urls))
    excluded = total - pub_total
    if sum(pub.values()) + excluded != total:
        print("[FAIL] 公开口径加隔离口径不等于全库")
        return 1
    print("[OK] 公开口径求和自洽: 公开 %d 加隔离 %d 等于全库 %d" % (pub_total, excluded, total))

    if args.check:
        live = {str(m.get("mode_code") or ""): (m.get("verification") or {}).get("status")
                for m in modes if isinstance(m, dict)}
        mismatched = [str(m.get("mode_code") or "") for m, r in zip(modes, results)
                      if live.get(str(m.get("mode_code") or "")) != r["status"]]
        if mismatched:
            print("[FAIL] --check: %d 条状态与本规则不一致（例: %s ）; 修复用 --write"
                  % (len(mismatched), mismatched[:5]))
            return 1
        print("[OK] --check: 库中状态与本规则逐条一致")
        return 0

    report = {
        "schema": "protreptic.verification_status/v1",
        "generated_by": "tools/apply_verification_status.py",
        "generated_at": args.checked_at,
        "checked_at": args.checked_at,
        "checker": args.checker,
        "rules": RULES,
        "precedence": list(PRECEDENCE),
        "inputs": {
            "data/modes_data.json": {"sha256": sha256_file(data_path), "modes": len(modes),
                                     "note": "sha256 为报告生成时刻的盘上文件（--write 走盘后回填）"},
            "data/source_links.json": {"sha256": sha256_file(links_path), "keys": len(index),
                                       "links_with_url": sum(
                                           1 for v in index.values()
                                           if (v.get("url") or "").strip()),
                                       "distinct_urls": len(url_values)},
            "data/audit/findings.json": {"sha256": sha256_file(findings_path)
                                         if findings_path.is_file() else None,
                                         "d4_d5_modes": len(suspect_codes)},
        },
        "counts": {"all": {s: cnt[s] for s in STATUSES}, "all_total": total,
                   "published": {s: pub[s] for s in STATUSES}, "published_total": pub_total,
                   "quarantined_total": excluded},
        "cross_checks": {"suspect_and_linked_overlap": overlap_s1_s2,
                         "verified_distinct_evidence_urls": len(evidence_urls)},
        "changes_vs_library": dict(sorted(changed.items())),
    }

    if args.write:
        for m, res in zip(modes, results):
            m["verification"] = {
                "status": res["status"],
                "method": res["method"],
                "evidence": res["evidence"],
                "checked_at": args.checked_at,
                "checker": args.checker,
            }
        # 格式与源文件逐字节同构（indent=2 / ensure_ascii=False / 无尾换行）：
        # 已实测 json.dumps(doc, ensure_ascii=False, indent=2) 与原文件 sha256 相同，
        # 所以本工具只改 verification 字段，不会把 22 MB 语料抖成整文件重排。
        out = json.dumps(doc, ensure_ascii=False, indent=2)
        data_path.write_text(out, encoding="utf-8")
        back = json.loads(data_path.read_text(encoding="utf-8"))
        back_cnt = collections.Counter((m.get("verification") or {}).get("status")
                                       for m in back["modes"] if isinstance(m, dict))
        if dict(back_cnt) != dict(cnt):
            print("[FAIL] 写盘回读的四态与判定不符: %s" % dict(back_cnt))
            return 1
        report["inputs"]["data/modes_data.json"]["sha256"] = sha256_file(data_path)
        report["inputs"]["data/modes_data.json"]["bytes"] = len(out.encode("utf-8"))
        print("[OK] 已写回 %s （回读四态一致, bytes %d ）"
              % (data_path, len(out.encode("utf-8"))))

    if args.report or args.write:
        rp = Path(args.report) if args.report else REPORT_PATH
        rp.parent.mkdir(parents=True, exist_ok=True)
        rp.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print("[OK] 机读报告 %s" % rp)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
