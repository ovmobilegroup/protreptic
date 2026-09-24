#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""merge_phase21r9_shenfu.py - Phase21-R9 沈复 H-SHF-001 合并入主库（卡 t_a7d233f0）

链条：素材包 t_d78053e7 -> 重建落盘 t_b6d4c0ee -> 本卡（合并）-> QA t_83e0d68d -> 归档 t_7e5afcbb
口径（沿 C-WX / C-LUORQ 先例）：
  * modes_data.json：10 条 M-SHF-001~010 逐字追加于 'modes' 数组文末；顶层块 H-SHF-001 新增
    （23 键，位于 'modes' 键之前）；total 字段随动对齐 = len(modes)（R5 裁定口径 total == len(modes)）。
  * code_maps.json：figures[H-SHF-001] = mode_ids(10, 取自图档) + tags(10, = 各模式 name_zh)
    + cross_references(取自图档, 目标已注册)，追加于 figures 文末。
  * figure_names.json：键级追加 H-SHF-001 -> 沈复（文末）。
  * scenarios_zh.json / scenarios_en.json：内层 scenarios_zh/scenarios_en 各 +10（C-SHF-001~010 /
    C-SHF-001E~010E，1:1 配对；text 由模板规则自 modern_applications_* 复算）。
  * scenario_tags.json：内层 scenario_tags 列表 +20（每模式 zh+en 各一条，先 zh 后 en）。

纪律：
  * 先备份后合并（六件 before 全量 + ledger 到 data/backup_merge_H-SHF-001_<ts>/）。
  * 幂等：已合并（M-SHF 已在库）则拒绝重跑（非破坏性 exit 3）。
  * 在途写者护栏：读-改-写以 (size, mtime_ns) 双检做乐观锁；读后文件被改动则中止（exit 4）。
  * 序列化：json.dump(indent=2, ensure_ascii=False) + 保留原文件尾换行状态（字节可复算）。
  * 不触碰：tools/ 副本面、_duplicates 归档、api/protreptic.db、其它卡在制文件。

用法：
  python3 tools/merge_phase21r9_shenfu.py            # dry-run（只打印计划与前后像）
  python3 tools/merge_phase21r9_shenfu.py --write    # 执行（备份 + 写入 + manifest）
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
import sys
import time

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LANDING = os.path.join(REPO, "docs/scratch/legacy20_r9_shenfu_landing")
FIG = os.path.join(REPO, "data/figures/H-SHF-001.json")
ENTRIES = os.path.join(LANDING, "modes_library_entries.json")
TOPBLOCK = os.path.join(LANDING, "top_block_proposal.json")
SCEN_NOTES = os.path.join(LANDING, "scenario_notes.json")

MAIN_LIB6 = [
    "data/modes_data.json",
    "data/code_maps.json",
    "data/figure_names.json",
    "data/scenarios_zh.json",
    "data/scenarios_en.json",
    "data/scenario_tags.json",
]
KEY23 = ["schema_version", "code", "name_zh", "name_en", "era", "historical_domains", "domains", "core_modes",
         "gender", "ethnicity", "nationality", "civilization_sphere", "time_period_standardized", "primary_language",
         "intellectual_tradition", "unique_thinking_zh", "unique_thinking_en", "mode_evidence", "key_texts",
         "key_concepts", "intellectual_lineage", "legacy_assessment", "scholarly_value"]
CODES = ["M-SHF-%03d" % i for i in range(1, 11)]
SCODES = ["C-SHF-%03d" % i for i in range(1, 11)]
SCODES_E = ["C-SHF-%03dE" % i for i in range(1, 11)]
FIGURE = "H-SHF-001"


def sha_bytes(b):
    return hashlib.sha256(b).hexdigest()


def sha_file(p):
    with io.open(p, "rb") as f:
        return sha_bytes(f.read())


def load(p):
    with io.open(p, encoding="utf-8") as f:
        return json.load(f)


def dump_preserve(obj, raw):
    """json.dump(indent=2, ensure_ascii=False) + 保留原尾换行状态（与既有产物字节可复算）。"""
    out = json.dumps(obj, ensure_ascii=False, indent=2).encode("utf-8")
    if raw.endswith(b"\n"):
        out += b"\n"
    return out


def deep(obj):
    return json.loads(json.dumps(obj, ensure_ascii=False))


def counts_of(md):
    modes = md["modes"]
    codes = [m.get("mode_code") for m in modes]
    nonempty = [c for c in codes if c]
    return dict(top_level_modes_entries=len(modes), distinct_mode_codes=len(set(nonempty)),
                empty_mode_code=len(codes) - len(nonempty))


def build_scen(entry, idx, lang):
    code = SCODES[idx] if lang == "zh" else SCODES_E[idx]
    text_zh = entry["name_zh"] + u"的当代应用场景：" + u"；".join(entry["modern_applications_zh"]) + u"。"
    text_en = (u"Contemporary applications of " + entry["name_en"] + u": "
               + u"; ".join(entry["modern_applications_en"]) + u".")
    return {
        "code": code,
        "mode_code": entry["mode_code"],
        "title_zh": entry["name_zh"],
        "title_en": entry["name_en"],
        "text_zh": text_zh,
        "text_en": text_en,
        "application_area_zh": list(entry["modern_applications_zh"]),
        "application_area_en": list(entry["modern_applications_en"]),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true", help="执行写入（缺省 dry-run）")
    ap.add_argument("--ts", default=None, help="备份时间戳（默认当前）")
    args = ap.parse_args()

    entries = load(ENTRIES)
    fig = load(FIG)
    top = load(TOPBLOCK)
    notes = load(SCEN_NOTES)

    # ---------- 预检（对输入） ----------
    assert isinstance(entries, list) and len(entries) == 10, "entries != 10"
    assert [e["mode_code"] for e in entries] == CODES, "mode_code 序列不符"
    assert all(e["id"] == e["mode_code"] for e in entries), "id != mode_code"
    assert all(e["figure_code"] == FIGURE and e["figure_name"] == u"沈复" for e in entries), "figure_code/name 不符"
    assert all(e.get("legacy_mode_id") == "" for e in entries), "legacy_mode_id 非空"
    assert all((e.get("verification") or {}).get("status") == "pending" for e in entries), "verification 非 pending"
    assert all(set(e.keys()) == set(entries[0].keys()) for e in entries), "键集不一致"
    assert fig["mode_ids"] == CODES and fig["figure_name"] == u"沈复" and fig["code"] == FIGURE
    assert list(top["proposal"].keys()) == KEY23, "顶层块键集 != 23 键"
    assert top["proposal"]["core_modes"] == CODES
    assert notes["figure_code"] == FIGURE and "C-SHF-001~010" in notes["notes"]["new_prefix_suggestion"]

    # ---------- 读六件（乐观锁快照） ----------
    raw = {}
    stat0 = {}
    for rel in MAIN_LIB6:
        p = os.path.join(REPO, rel)
        with io.open(p, "rb") as f:
            raw[rel] = f.read()
        st = os.stat(p)
        stat0[rel] = (st.st_size, st.st_mtime_ns)
    before_sha = {rel: sha_bytes(raw[rel]) for rel in MAIN_LIB6}

    md = json.loads(raw["data/modes_data.json"].decode("utf-8"))
    cm = json.loads(raw["data/code_maps.json"].decode("utf-8"))
    fn = json.loads(raw["data/figure_names.json"].decode("utf-8"))
    sz = json.loads(raw["data/scenarios_zh.json"].decode("utf-8"))
    se = json.loads(raw["data/scenarios_en.json"].decode("utf-8"))
    st = json.loads(raw["data/scenario_tags.json"].decode("utf-8"))

    # ---------- 幂等预检（对主库） ----------
    present = [m.get("mode_code") for m in md["modes"] if str(m.get("mode_code", "")).startswith("M-SHF")]
    if present or FIGURE in cm["figures"] or FIGURE in fn:
        print("[ABORT] 已合并（M-SHF=%s, code_maps=%s, figure_names=%s）——幂等守卫拒绝重跑"
              % (present[:3], FIGURE in cm["figures"], FIGURE in fn))
        sys.exit(3)
    assert not any(k.startswith("C-SHF") for k in sz["scenarios_zh"]), "C-SHF 已存在（zh 内层）"
    assert not any(k.startswith("C-SHF") for k in se["scenarios_en"]), "C-SHF 已存在（en 内层）"
    assert not any(str(t.get("mode_code", "")).startswith("M-SHF") for t in st["scenario_tags"]), "M-SHF 标签已存在"
    assert FIGURE not in md, "顶层块 H-SHF-001 已存在"
    assert "modes" in md and "total" in md

    # ---------- 计算 after（深拷贝，避免污染 before 像） ----------
    src_md = deep(md)
    new_md = {}
    for k, v in src_md.items():
        if k == "modes":
            new_md[FIGURE] = deep(top["proposal"])
            new_md[k] = v
        else:
            new_md[k] = v
    modes = new_md["modes"]
    for e in entries:
        modes.append(deep(e))
    new_md.pop("total", None)
    new_md["total"] = len(modes)
    # 逐字核：追加段 == A1 entries
    assert new_md["modes"][-10:] == [deep(e) for e in entries], "追加段与 A1 entries 不符"

    cm2 = deep(cm)
    cm2["figures"][FIGURE] = {
        "mode_ids": list(fig["mode_ids"]),
        "tags": [e["name_zh"] for e in entries],
        "cross_references": deep(fig.get("cross_references") or []),
    }
    tgt_bad = [x.get("target_figure_code") for x in cm2["figures"][FIGURE]["cross_references"]
               if x.get("target_figure_code") not in cm2["figures"]]
    assert not tgt_bad, "xref 悬空: %s" % tgt_bad

    fn2 = deep(fn)
    fn2[FIGURE] = fig["figure_name"]

    sz2 = deep(sz)
    se2 = deep(se)
    for i, e in enumerate(entries):
        sz2["scenarios_zh"][SCODES[i]] = build_scen(e, i, "zh")
        se2["scenarios_en"][SCODES_E[i]] = build_scen(e, i, "en")

    st2 = deep(st)
    tag_list = st2["scenario_tags"]
    for e in entries:
        tag_list.append({"mode_code": e["mode_code"], "tag": e["name_zh"] + u"_zh",
                         "figure_code": FIGURE, "language": "zh"})
        tag_list.append({"mode_code": e["mode_code"], "tag": e["name_en"] + u"_en",
                         "figure_code": FIGURE, "language": "en"})

    new_raw = {
        "data/modes_data.json": dump_preserve(new_md, raw["data/modes_data.json"]),
        "data/code_maps.json": dump_preserve(cm2, raw["data/code_maps.json"]),
        "data/figure_names.json": dump_preserve(fn2, raw["data/figure_names.json"]),
        "data/scenarios_zh.json": dump_preserve(sz2, raw["data/scenarios_zh.json"]),
        "data/scenarios_en.json": dump_preserve(se2, raw["data/scenarios_en.json"]),
        "data/scenario_tags.json": dump_preserve(st2, raw["data/scenario_tags.json"]),
    }
    # round-trip 稳定性（字节可复算：loads -> dump_preserve 恒等）
    for rel in MAIN_LIB6:
        obj_rt = json.loads(new_raw[rel].decode("utf-8"))
        assert dump_preserve(obj_rt, new_raw[rel]) == new_raw[rel], "round-trip 不稳: " + rel
    after_sha = {rel: sha_bytes(new_raw[rel]) for rel in MAIN_LIB6}
    assert len(md["modes"]) + 10 == len(new_md["modes"]), "before/after 计数护栏失败"
    before_counts = {
        "modes_data": counts_of(md),
        "code_maps_figures": len(cm["figures"]),
        "figure_names": len(fn),
        "scenarios_zh_inner": len(sz["scenarios_zh"]),
        "scenarios_en_inner": len(se["scenarios_en"]),
        "scenario_tags_inner": len(st["scenario_tags"]),
    }
    after_counts = {
        "modes_data": counts_of(new_md),
        "code_maps_figures": len(cm2["figures"]),
        "figure_names": len(fn2),
        "scenarios_zh_inner": len(sz2["scenarios_zh"]),
        "scenarios_en_inner": len(se2["scenarios_en"]),
        "scenario_tags_inner": len(st2["scenario_tags"]),
    }
    azj_before = [m.get("mode_code") for m in md["modes"] if str(m.get("mode_code", "")).startswith("M-AZJ")]
    azj_after = [m.get("mode_code") for m in new_md["modes"] if str(m.get("mode_code", "")).startswith("M-AZJ")]
    if azj_before:
        assert azj_after == azj_before, "并集护栏：M-AZJ 条目丢失"

    print("== 合并计划（卡 t_a7d233f0, %s）==" % ("WRITE" if args.write else "DRY-RUN"))
    for rel in MAIN_LIB6:
        print("  %-30s %s -> %s" % (rel, before_sha[rel][:12], after_sha[rel][:12]))
    print("  before:", json.dumps(before_counts, ensure_ascii=False))
    print("  after: ", json.dumps(after_counts, ensure_ascii=False))
    print("  modes_data.total: %s -> %s" % (md.get("total"), new_md["total"]))
    print("  union guard M-AZJ: before=%d after=%d" % (len(azj_before), len(azj_after)))

    if not args.write:
        print("  [dry-run] 未写入；--write 执行")
        return

    # ---------- 备份 ----------
    ts = args.ts or time.strftime("%Y%m%d_%H%M%S")
    bdir = os.path.join(REPO, "data", "backup_merge_%s_%s" % (FIGURE, ts))
    os.makedirs(bdir, exist_ok=False)
    for rel in MAIN_LIB6:
        dst = os.path.join(bdir, os.path.basename(rel))
        with io.open(dst, "wb") as f:
            f.write(raw[rel])
    ledger = {"card": "t_a7d233f0", "figure_code": FIGURE, "created": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
              "files": {rel: {"sha256": before_sha[rel], "bytes": len(raw[rel])} for rel in MAIN_LIB6},
              "note": u"Phase21-R9 沈复合并卡 t_a7d233f0 合并前全量备份（先备份后合并）"}
    with io.open(os.path.join(bdir, "backup_ledger.json"), "w", encoding="utf-8") as f:
        json.dump(ledger, f, ensure_ascii=False, indent=2)
        f.write(u"\n")

    # ---------- 乐观锁复核 + 原子写 ----------
    for rel in MAIN_LIB6:
        p = os.path.join(REPO, rel)
        st_now = os.stat(p)
        if (st_now.st_size, st_now.st_mtime_ns) != stat0[rel]:
            print("[ABORT] 在途写者护栏触发：%s 于读后被改动（%s/%s vs %s/%s）" %
                  (rel, st_now.st_size, st_now.st_mtime_ns, stat0[rel][0], stat0[rel][1]))
            sys.exit(4)
    written = []
    for rel in MAIN_LIB6:
        p = os.path.join(REPO, rel)
        tmp = p + ".merge_tmp"
        with io.open(tmp, "wb") as f:
            f.write(new_raw[rel])
        os.replace(tmp, p)
        written.append(rel)
        got = sha_file(p)
        assert got == after_sha[rel], "写入后 sha 不符: %s" % rel

    # ---------- manifest ----------
    manifest = {
        "schema_version": "v1",
        "card": "t_a7d233f0",
        "chain": u"Phase21-R9 沈复重做链（2/4 合并卡）",
        "date": time.strftime("%Y-%m-%d"),
        "figure_code": FIGURE,
        "landing_package": "docs/scratch/legacy20_r9_shenfu_landing/",
        "backup_dir": os.path.relpath(bdir, REPO),
        "rules": {
            "modes_append": u"10 条 M-SHF-001~010 逐字等于 A1 entries，追加于 'modes' 文末",
            "top_block": u"顶层块 H-SHF-001 新增（23 键，置于 'modes' 之前）；原块缺失，无旧块置换",
            "total": u"total 随动对齐 = len(modes)（R5 裁定口径；合并卡只写这一个标量）",
            "code_maps": u"figures[H-SHF-001] = mode_ids(图档) + tags(10 = 各模式 name_zh) + cross_references(图档逐字, 目标已注册)",
            "scenario_prefix": u"C-SHF-001~010 / C-SHF-001E~010E（1:1 配对 mode 序号；全库 0 碰撞）",
            "scenario_template": u"text 由 name_zh/name_en + modern_applications_* 模板复算（沿 C-WX/C-LUORQ 生成规则）",
            "tags": u"scenario_tags +20：每模式 zh+en 各一条（tag = name_zh_zh / name_en_en），先 zh 后 en",
            "serialization": u"json.dump(indent=2, ensure_ascii=False) + 保留原尾换行状态（字节可复算）",
        },
        "inputs": {rel: {"sha256": before_sha[rel], "bytes": len(raw[rel])} for rel in MAIN_LIB6},
        "after": {rel: {"sha256": after_sha[rel], "bytes": len(new_raw[rel])} for rel in MAIN_LIB6},
        "counts": {"before": before_counts, "after": after_counts,
                   "total_field": {"before": md.get("total"), "after": new_md["total"]}},
        "union_guard": {"M_AZJ_before": len(azj_before), "M_AZJ_after": len(azj_after)},
        "written": written,
    }
    mpath = os.path.join(REPO, "data/audit/phase21r9_shenfu_merge_manifest.json")
    with io.open(mpath, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
        f.write(u"\n")
    print("  [OK] 六件写入完成；manifest -> %s" % os.path.relpath(mpath, REPO))
    print("  [OK] 备份目录 -> %s" % os.path.relpath(bdir, REPO))


if __name__ == "__main__":
    main()
