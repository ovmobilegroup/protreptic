#!/usr/bin/env python3
"""apply_w8_stage2_batch1_landing.py — Phase21-W8 Stage2 批1 · 主库落地（卡 t_b85ae14a）。

本脚本只做「外部证据 → 主库」的两件搬运（幂等；已应用再跑即 ABORT）：

  ① 链接入库（data/source_links.json）：
     批1 素材包里**已抓取且逐字核验通道成立的中文书**（8 部，lang=lzh）写进链接索引。
     url / canonical_title / provider 取《书单》primary 段与批1 缓存索引的实测值，不新造、
     不猜 URL；confidence 同 W5《论衡》先例 0.9；checked_at 为本卡日期。
     跨语言书（en/grc/fr，9 部）**不建链接**——引文为中文译本、对非中文原文不适用逐字对读，
     口径待船长裁定（见落地报告 §待裁定），本脚本不带开关，防止误用。

  ② 缓存合并（data/audit/source_texts.json）：
     把批1 独立索引（data/audit/source_texts_w8_stage2_batch1.json）的 17 条条目并入
     D4 链唯一入口 source_texts.json。条目**原样搬**（含 zh_cn 元数据 / stale 标注 /
     coverage / file / sha256），不重写任何字段；已存在的 key 跳过（幂等）。

为什么只做这两件：findings / 四态由既有工具现算——
  tools/build_audit_findings.py --write（D4 现算）→ tools/apply_verification_status.py --write
本脚本不复写任何判定规则。

写盘格式与源文件逐字节同构（indent=2 / ensure_ascii=False / 保留尾换行与否），
自检「未变更部分的再序列化 sha256 与盘上一致」后才写；任何一条不满足即 exit 1。

用法
    python3 tools/apply_w8_stage2_batch1_landing.py                # 干跑（默认，只报告）
    python3 tools/apply_w8_stage2_batch1_landing.py --write        # 写盘
    python3 tools/apply_w8_stage2_batch1_landing.py --backup       # 先做备份目录（不入库）
退出码：0 成功 / 1 断言失败或重跑冲突 / 2 输入缺失。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
LINKS_PATH = REPO_ROOT / "data" / "source_links.json"
SOURCE_TEXTS_PATH = REPO_ROOT / "data" / "audit" / "source_texts.json"
BATCH1_INDEX_PATH = REPO_ROOT / "data" / "audit" / "source_texts_w8_stage2_batch1.json"
BOOKLIST_PATH = REPO_ROOT / "docs" / "research" / "phase21w8_stage2_batch1_booklist.json"
BACKUP_TARGETS = (
    "data/modes_data.json",
    "data/source_links.json",
    "data/audit/source_texts.json",
    "data/audit/findings.json",
    "data/audit/verification_status.json",
)
CHECKED_AT = "2026-09-24"
CONFIDENCE = 0.9


def sha16(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()[:16]


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def dump_like(original_bytes: bytes, doc) -> bytes:
    """与源文件同构序列化：indent=2 / ensure_ascii=False / 尾换行与否原样。"""
    out = json.dumps(doc, ensure_ascii=False, indent=2)
    if original_bytes.endswith(b"\n"):
        out += "\n"
    return out.encode("utf-8")


def build_new_links():
    """批1 中文书（lang=lzh）→ source_links 条目（值全部来自实测产物）。"""
    idx = load_json(BATCH1_INDEX_PATH)
    booklist = load_json(BOOKLIST_PATH)
    prim = {b["book"]: b.get("primary") or {} for b in booklist["batch1"]}
    new = {}
    for e in idx["entries"]:
        if e.get("lang") != "lzh":
            continue
        key = e["key"]
        book = e.get("label")
        primary = prim.get(book) or {}
        new[key] = {
            "url": e["url"],
            "source_type": e["source_type"],
            "confidence": CONFIDENCE,
            "canonical_title": primary.get("title") or book,
            "provider": primary.get("provider") or "",
            "checked_at": CHECKED_AT,
            "note": ("批1 入库（卡 t_b85ae14a）：抓取通道=%s；coverage=%s；"
                     "引文逐字/繁简对读结论与见证见落地报告 §逐条"
                     % (e.get("fetch_mode") or "?", e.get("coverage"))),
        }
    return new


def merge_cache_entries():
    """批1 索引 → source_texts 条目列表（未存在的 key）。"""
    idx = load_json(BATCH1_INDEX_PATH)
    return [dict(e) for e in idx["entries"]]


def do_backup() -> Path:
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out = REPO_ROOT / "data" / ("backup_merge_W8B1_%s" % ts)
    out.mkdir(parents=True, exist_ok=False)
    manifest = {"schema": "protreptic.backup/v1", "created_at": ts,
                "purpose": "Phase21-W8 Stage2 批1 主库落地（卡 t_b85ae14a）先备份后落地",
                "files": []}
    for rel in BACKUP_TARGETS:
        src = REPO_ROOT / rel
        if not src.is_file():
            manifest["files"].append({"path": rel, "present": False})
            continue
        data = src.read_bytes()
        dst = out / rel.replace("/", "__")
        dst.write_bytes(data)
        manifest["files"].append({"path": rel, "present": True, "bytes": len(data),
                                  "sha256": hashlib.sha256(data).hexdigest(),
                                  "backup_file": dst.name})
    (out / "MANIFEST.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
                                       encoding="utf-8")
    print("[backup] %s（%d 件 + MANIFEST）" % (out, len(BACKUP_TARGETS)))
    return out



def preserve_stamps(backup_dir: Path) -> int:
    """回填『状态未变、但 verification 块被刷新』的条目（保护他卡印记）。

    tools/apply_verification_status.py --write 会**重建全部** verification 块；
    实测其会覆盖 R9 两卡（M-AZJ/M-SHF 共 20 条，elcano 印记：method=phase21r9-*-landing
    + 素材包证据串）改成通用 auto-scan 块。本步骤把「状态未变而块内容变了」的条目
    从落地前备份原样回填——只回填块、不改状态，故 --check（只比 status）仍通过。
    回填名单逐条打印，报告与证据里留痕。
    """
    modes_path = REPO_ROOT / "data" / "modes_data.json"
    bpath = backup_dir / "data__modes_data.json"
    if not bpath.is_file():
        print("[FAIL] 备份缺 data__modes_data.json: %s" % bpath)
        return 1
    cur_bytes = modes_path.read_bytes()
    cur = json.loads(cur_bytes.decode("utf-8"))
    old = json.loads(bpath.read_text(encoding="utf-8"))
    if len(cur["modes"]) != len(old["modes"]):
        print("[FAIL] 模式条数不一致，拒绝回填")
        return 1
    restored = []
    for a, b in zip(old["modes"], cur["modes"]):
        va, vb = a.get("verification") or {}, b.get("verification") or {}
        if va.get("status") == vb.get("status") and va != vb:
            b["verification"] = va
            restored.append(str(b.get("mode_code") or b.get("id")))
    print("[stamps] 回填 %d 条状态未变但块被刷新的条目：%s" % (len(restored), "、".join(restored)))
    if not restored:
        print("[stamps] 无需回填")
        return 0
    out = dump_like(cur_bytes, cur)
    modes_path.write_bytes(out)
    back = json.loads(modes_path.read_text(encoding="utf-8"))
    assert [(m.get("verification") or {}).get("status") for m in back["modes"]] == \
           [(m.get("verification") or {}).get("status") for m in cur["modes"]], "回读状态不一致"
    print("[OK] 已回填并回读校验 %s" % modes_path)
    return 0



def refresh_status_report() -> int:
    """回填 verification_status.json 报告里的实测哈希（块回填后文件字节已变）。

    apply_verification_status.py --write 先写 modes_data.json、再按其写盘时刻的状态
    写报告；本卡随后回填 20 条他卡印记（preserve-stamps）会让 modes_data.json 字节再变，
    报告里的 sha256/bytes 因此落后于终态。本步骤只重算三个输入的 sha256/bytes/modes
    计数并回读校验，不改任何判定结论（状态与计数一律不动）。
    """
    rp = REPO_ROOT / "data" / "audit" / "verification_status.json"
    if not rp.is_file():
        print("[FAIL] 报告缺失: %s" % rp)
        return 1
    text = rp.read_text(encoding="utf-8")
    rep = json.loads(text)
    ins = rep.get("inputs") or {}
    updates = []
    md = REPO_ROOT / "data" / "modes_data.json"
    b = md.read_bytes()
    doc = json.loads(b.decode("utf-8"))
    old = ins.get("data/modes_data.json", {})
    new = dict(old)
    new["sha256"] = hashlib.sha256(b).hexdigest()
    new["bytes"] = len(b)
    new["modes"] = len([m for m in doc.get("modes", []) if isinstance(m, dict)])
    if old.get("sha256") != new["sha256"]:
        updates.append(("data/modes_data.json", old.get("sha256", "")[:16], new["sha256"][:16]))
    ins["data/modes_data.json"] = new
    for rel in ("data/source_links.json", "data/audit/findings.json"):
        fp = REPO_ROOT / rel
        fb = fp.read_bytes()
        o = ins.get(rel, {})
        n = dict(o)
        n["sha256"] = hashlib.sha256(fb).hexdigest()
        if rel.endswith("source_links.json"):
            n["keys"] = len(json.loads(fb.decode("utf-8")))
        if o.get("sha256") != n["sha256"]:
            updates.append((rel, o.get("sha256", "")[:16], n["sha256"][:16]))
        ins[rel] = n
    rep["inputs"] = ins
    out = json.dumps(rep, ensure_ascii=False, indent=2)
    if text.endswith("\n"):
        out += "\n"
    rp.write_text(out, encoding="utf-8")
    back = json.loads(rp.read_text(encoding="utf-8"))
    assert back["inputs"]["data/modes_data.json"]["sha256"] == new["sha256"], "回读不一致"
    print("[report] 回填实测哈希 %d 处：%s" % (len(updates), "；".join("%s %s->%s" % u for u in updates)))
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="W8 Stage2 批1 主库落地：链接入库 + 缓存合并")
    ap.add_argument("--write", action="store_true", help="写盘（默认只干跑）")
    ap.add_argument("--backup", action="store_true", help="先做备份目录")
    ap.add_argument("--preserve-stamps", metavar="BACKUP_DIR", default=None,
                    help="从备份目录回填『状态未变但块被刷新』的 verification 块（保护他卡印记）")
    ap.add_argument("--refresh-status-report", action="store_true",
                    help="按终态文件重算 verification_status.json 报告里的实测哈希")
    args = ap.parse_args()

    for p in (LINKS_PATH, SOURCE_TEXTS_PATH, BATCH1_INDEX_PATH, BOOKLIST_PATH):
        if not p.is_file():
            print("[FAIL] 输入缺失: %s" % p)
            return 2

    if args.backup:
        do_backup()

    if args.preserve_stamps:
        rc = preserve_stamps(Path(args.preserve_stamps))
        if rc != 0:
            return rc

    if args.refresh_status_report:
        rc = refresh_status_report()
        if rc != 0:
            return rc

    # ---- ① 链接入库 ----
    links_bytes = LINKS_PATH.read_bytes()
    links = json.loads(links_bytes.decode("utf-8"))
    new_links = build_new_links()
    to_add, same, conflict = {}, [], []
    for key, val in new_links.items():
        cur = links.get(key)
        if cur is None:
            to_add[key] = val
        elif cur.get("url") == val.get("url") and cur.get("source_type") == val.get("source_type"):
            same.append(key)
        else:
            conflict.append((key, cur.get("url"), val.get("url")))
    print("[links] 现有 %d key；本次新增 %d；已存在且一致 %d；冲突 %d"
          % (len(links), len(to_add), len(same), len(conflict)))
    for key, old, new in conflict:
        print("  [CONFLICT] %s: 盘上 %r vs 拟写 %r（人工裁定，不改）" % (key, old, new))
    if conflict:
        print("[ABORT] 链接索引存在冲突键，停止（不做任何写盘）")
        return 1
    links_out = dict(links)
    links_out.update(to_add)
    links_new_bytes = dump_like(links_bytes, links_out)
    # 同构自检：未变更时再序列化必须逐字节等于盘上
    if not to_add and links_new_bytes != links_bytes:
        print("[FAIL] source_links.json 序列化同构自检不过（无新增却字节不同）")
        return 1

    # ---- ② 缓存合并 ----
    st_bytes = SOURCE_TEXTS_PATH.read_bytes()
    st = json.loads(st_bytes.decode("utf-8"))
    have = {e.get("key") for e in st["entries"]}
    entries_add = [e for e in merge_cache_entries() if e.get("key") not in have]
    added_keys = [e["key"] for e in entries_add]
    print("[cache] 现有 %d 条目；本次并入 %d 条：%s"
          % (len(st["entries"]), len(entries_add), "、".join(added_keys)))
    st_out = dict(st)
    st_out["entries"] = list(st["entries"]) + entries_add
    st_out["counts"] = dict(st.get("counts") or {})
    st_out["counts"]["entries"] = len(st_out["entries"])
    st_out["counts"]["batch1_merged"] = len(entries_add)
    st_new_bytes = dump_like(st_bytes, st_out)
    if not entries_add and st_new_bytes != st_bytes:
        # 只差 counts 时说明此前已合并（幂等跳过，不算失败）
        if st.get("counts", {}).get("batch1_merged"):
            print("[cache] 此前已合并（counts.batch1_merged=%s），跳过写盘" % st["counts"]["batch1_merged"])
            st_new_bytes = st_bytes
        else:
            print("[FAIL] source_texts.json 序列化同构自检不过（无新增却字节不同）")
            return 1

    print("[receipt] source_links.json  %s -> %s（+%d key）"
          % (sha16(LINKS_PATH), hashlib.sha256(links_new_bytes).hexdigest()[:16], len(to_add)))
    print("[receipt] source_texts.json  %s -> %s（+%d 条）"
          % (sha16(SOURCE_TEXTS_PATH), hashlib.sha256(st_new_bytes).hexdigest()[:16], len(entries_add)))

    if not args.write:
        print("[dry-run] 未写盘（--write 才落盘）")
        return 0

    if links_new_bytes != links_bytes:
        LINKS_PATH.write_bytes(links_new_bytes)
        back = json.loads(LINKS_PATH.read_text(encoding="utf-8"))
        assert list(back) == list(links_out), "写盘回读键序不一致"
        print("[OK] 已写 %s" % LINKS_PATH)
    if st_new_bytes != st_bytes:
        SOURCE_TEXTS_PATH.write_bytes(st_new_bytes)
        back = json.loads(SOURCE_TEXTS_PATH.read_text(encoding="utf-8"))
        assert len(back["entries"]) == len(st_out["entries"]), "写盘回读条目数不一致"
        print("[OK] 已写 %s" % SOURCE_TEXTS_PATH)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
