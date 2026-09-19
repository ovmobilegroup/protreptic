#!/usr/bin/env python3
"""Verify source_links.json URLs (real HTTP check) —— 存量冻结/新增即拦两档（Phase37-X3）。

为什么改
    原版对**任何**非 200 一律 exit 1。实测源库 50 条链接里 2 条存量坏链
    （《天学初函》 archive.org 404；《德川幕府制度研究》 openlibrary 连接失败），
    照抄接进 CI 会让 Pages 永久红 —— 与 credibility_gate 同一个坑。

口径（与 tools/credibility_gate.py 的两档模式同构）
    * 默认（无档位参数）         : 严格口径（历史行为，任何非 200 都 exit 1）；
    * `--legacy-report`         : 存量与新增都列出，**一律 exit 0**；
    * `--hard-fail`             : 基线内（data/audit/source_links_baseline.json）只报告，
                                  **基线外的坏链 exit 1**。
    分类细则（--hard-fail / --legacy-report 共用）：
      ok          HTTP 200                     -> 通过
      dead        HTTP 4xx/5xx（确定性坏链）    -> 违规，进基线/新增判定
      unreachable 连接层失败（000/超时/代理）    -> **警告**，不计违规
                  （CI 里网络抖动不该把发布链打红；要严格用默认档位）
      指纹 = "source|url"：换 URL 必须重新核验（指纹不同 = 新增）。

用法
    python3 tools/verify_source_links.py --legacy-report              # 只报告
    python3 tools/verify_source_links.py --hard-fail                  # CI 口径
    python3 tools/verify_source_links.py --write-baseline             # 重新冻结坏链基线
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
LINKS_PATH = REPO_ROOT / "data" / "source_links.json"
DEFAULT_BASELINE_PATH = REPO_ROOT / "data" / "audit" / "source_links_baseline.json"
SCHEMA = "protreptic.source_links_baseline/v1"
POLICY = ("存量冻结、新增即拦：本文件登记的坏链只报告不阻断（exit 0）；"
          "任何未登记的确定性坏链在 --hard-fail 下 exit 1；连接层失败只算警告")


def check_url(url: str, max_time: int = 10) -> tuple[str, int]:
    """返回 (kind, status)。kind ∈ {ok, dead, unreachable}。"""
    if not url:
        return "unreachable", 0
    try:
        result = subprocess.run(
            ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", "--max-time", str(max_time), url],
            capture_output=True, text=True, timeout=max_time + 5,
        )
        raw = (result.stdout or "").strip()
        status = int(raw) if raw.isdigit() else 0
    except Exception:
        status = 0
    if status == 200:
        return "ok", 200
    if status == 0:
        return "unreachable", 0
    return "dead", status


def fingerprint(source: str, url: str) -> str:
    return f"{source}|{url}"


def load_baseline(path: Path):
    if not path.is_file():
        return None
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def build_baseline(violations) -> dict:
    entries = {}
    for src, url, status in violations:
        fid = fingerprint(src, url)
        entries[fid] = {"id": fid, "source": src, "url": url, "status": status}
    return {
        "schema": SCHEMA,
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "generated_by": "tools/verify_source_links.py --write-baseline",
        "policy": POLICY,
        "counts": {"violations": len(violations), "distinct": len(entries)},
        "entries": [entries[k] for k in sorted(entries)],
    }


def save_baseline(baseline: dict, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(baseline, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def probe(links: dict, max_time: int, jobs: int) -> list[dict]:
    items = []
    for source, info in links.items():
        items.append({
            "source": source,
            "url": info.get("url", ""),
            "type": info.get("source_type", "unknown"),
        })
    with ThreadPoolExecutor(max_workers=max(1, jobs)) as ex:
        kinds = list(ex.map(lambda it: check_url(it["url"], max_time), items))
    for it, (kind, status) in zip(items, kinds):
        it["kind"], it["status"] = kind, status
    return items


def main() -> int:
    ap = argparse.ArgumentParser(description="Verify source_links.json URLs")
    ap.add_argument("--links-path", type=str, default=str(LINKS_PATH))
    ap.add_argument("--baseline", type=str, default=None,
                    help=f"坏链基线路径（缺省 {DEFAULT_BASELINE_PATH}）")
    ap.add_argument("--legacy-report", action="store_true", help="只报告，一律 exit 0")
    ap.add_argument("--hard-fail", action="store_true", help="基线外的坏链 exit 1")
    ap.add_argument("--write-baseline", action="store_true", help="用当前坏链重新冻结基线")
    ap.add_argument("--max-time", type=int, default=10, help="单条 curl 超时秒数（默认 10）")
    ap.add_argument("--jobs", type=int, default=8, help="并发核验线程数（默认 8）")
    args = ap.parse_args()

    links_path = Path(args.links_path)
    baseline_path = Path(args.baseline) if args.baseline else DEFAULT_BASELINE_PATH
    with links_path.open("r", encoding="utf-8") as f:
        links = json.load(f)

    print(f"Checking {len(links)} source links... (jobs={args.jobs}, max-time={args.max_time}s)")
    items = probe(links, args.max_time, args.jobs)

    ok = [i for i in items if i["kind"] == "ok"]
    unverifiable = [i for i in items if i["type"] == "unverifiable" and i["kind"] != "ok"]
    dead = [i for i in items if i["kind"] == "dead"]
    unreachable = [i for i in items if i["kind"] == "unreachable" and i["type"] != "unverifiable"]

    for it in items:
        if it["kind"] == "ok":
            print(f"  [OK 200] {it['source']} -> {it['url']}")
        elif it["kind"] == "dead":
            print(f"  [DEAD {it['status']}] {it['source']} -> {it['url']}")
        elif it["type"] == "unverifiable":
            print(f"  [UNVERIFIABLE] {it['source']} (type=unverifiable)")
        else:
            print(f"  [UNREACHABLE] {it['source']} -> {it['url']}")

    print()
    print(f"Summary: {len(ok)} OK, {len(dead)} dead, {len(unreachable)} unreachable, "
          f"{len(unverifiable)} unverifiable")

    violations = [(i["source"], i["url"], i["status"]) for i in dead]

    if args.write_baseline:
        bl = build_baseline(violations)
        save_baseline(bl, baseline_path)
        print(f"[OK] 坏链基线已写入 {baseline_path} counts={json.dumps(bl['counts'])}")
        return 0

    if not (args.legacy_report or args.hard_fail):
        failed = len(dead) + len(unreachable)
        print(f"strict mode: {failed} failed (dead={len(dead)}, unreachable={len(unreachable)})")
        return 0 if failed == 0 else 1

    baseline = load_baseline(baseline_path)
    print(f"resolved links path:    {links_path}")
    print(f"resolved baseline path: {baseline_path} (exists={baseline_path.is_file()})")
    if baseline is None:
        print(f"[FAIL] baseline file missing: {baseline_path}")
        print("       先冻结基线: python3 tools/verify_source_links.py --write-baseline")
        return 2
    known = {e["id"]: e for e in baseline.get("entries", [])}
    cur_ids = {fingerprint(s, u) for s, u, _ in violations}
    legacy = [v for v in violations if fingerprint(v[0], v[1]) in known]
    new = [v for v in violations if fingerprint(v[0], v[1]) not in known]
    stale = [known[i] for i in known if i not in cur_ids]

    print(f"baseline frozen at {baseline.get('generated_at')} "
          f"counts={json.dumps(baseline.get('counts', {}), ensure_ascii=False)}")
    print()
    print(f"--- 存量坏链（基线内，冻结）: {len(legacy)} 条 ---")
    for s, u, st in legacy:
        print(f"  ::notice::LEGACY [DEAD {st}] {s} -> {u}")
    print()
    print(f"--- 新增坏链（基线外，必拦）: {len(new)} 条 ---")
    for s, u, st in new:
        print(f"  ::error::NEW [DEAD {st}] {s} -> {u}")
    if unreachable:
        print()
        print(f"--- 连接层失败（警告，不计违规）: {len(unreachable)} 条 ---")
        for i in unreachable:
            print(f"  ::warning::UNREACHABLE {i['source']} -> {i['url']}")
    if stale:
        print()
        print(f"--- 基线内已不再成立（可重新冻结）: {len(stale)} 条 ---")
        for e in stale:
            print(f"  ::warning::STALE {e['id']}")
    print()
    if args.legacy_report:
        print(f"[OK] legacy-report: 存量 {len(legacy)} / 新增 {len(new)} —— 只报告，不阻断 (exit 0)")
        return 0
    if new:
        print(f"[FAIL] hard-fail: {len(new)} 条新增坏链（基线外）-> exit 1（存量 {len(legacy)} 条已冻结）")
        return 1
    print(f"[OK] hard-fail: 无新增坏链（存量 {len(legacy)} 条已冻结）-> exit 0")
    return 0


if __name__ == "__main__":
    sys.exit(main())
