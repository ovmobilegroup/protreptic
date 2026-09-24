#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# merge_azj_hazj001.py -- Phase21-R9 安子介 H-AZJ-001 合并入主库（卡 t_ce457734）
# 口径：纯追加零删改（modes +10 / code_maps +1 / figure_names +1 / 顶层块 H-AZJ-001 新增 / total 随动对齐）
# 幂等：主库已含本链足迹时前置断言 ABORT（不写盘）
# 序列化：各文件尾换行按现行态保持（modes_data.json 无尾换行，其余有）
import hashlib, json, os, shutil, sys
from datetime import datetime

WS = "/opt/data/workspace/Protreptic"
LAND = WS + "/docs/scratch/legacy20_r9_azj_landing"
CARD = "/opt/data/kanban/boards/protreptic/workspaces/t_ce457734"
TS = os.environ.get("AZJ_TS") or datetime.now().strftime("%Y%m%d_%H%M%S")
BACKUP = WS + "/data/backup_merge_H-AZJ-001_" + TS
EVID = os.path.join(CARD, "evidence")
DRY = "--dry" in sys.argv

FIG = "H-AZJ-001"
FNAME = "安子介"
CODES = ["M-AZJ-%03d" % i for i in range(1, 11)]
MAIN = {"modes": "data/modes_data.json", "cm": "data/code_maps.json", "fn": "data/figure_names.json"}
WATCH = ["data/modes_data.json", "data/code_maps.json", "data/scenarios_zh.json", "data/scenarios_en.json",
         "data/scenario_tags.json", "data/figure_names.json"]

def rd(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)

def nl_of(p):
    if not os.path.exists(p):
        return "\n"
    return "\n" if open(p, "rb").read().endswith(b"\n") else ""

def dump_of(obj, nl):
    return json.dumps(obj, ensure_ascii=False, indent=2) + nl

def wr(p, obj):
    with open(p, "w", encoding="utf-8") as f:
        f.write(dump_of(obj, nl_of(p)))

def sha_file(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()

def count_of(rel, obj):
    if rel.endswith("modes_data.json"): return len(obj["modes"])
    if rel.endswith("code_maps.json"): return len(obj["figures"])
    if rel.endswith("scenarios_zh.json"): return len(obj["scenarios_zh"])
    if rel.endswith("scenarios_en.json"): return len(obj["scenarios_en"])
    if rel.endswith("scenario_tags.json"): return len(obj["scenario_tags"])
    return len(obj)

log = {"card": "t_ce457734", "ts": TS, "dry": DRY, "steps": []}
def step(name, **kw):
    kw["step"] = name
    log["steps"].append(kw)
    print("[STEP]", name, json.dumps(kw, ensure_ascii=False)[:600])

# ---------- 0. 序列化自检（六件按现行 indent=2 + 尾换行态可逐字节复写）----------
for rel in WATCH:
    p = os.path.join(WS, rel)
    raw = open(p, "rb").read()
    out = dump_of(json.loads(raw.decode("utf-8")), nl_of(p)).encode("utf-8")
    assert raw == out, "serialization mismatch: " + rel
step("serialization_selfcheck", files=len(WATCH), ok=True)

# ---------- 1. 载入 AZJ-2 落盘产物（三面同体）----------
entries = rd(LAND + "/modes_library_entries.json")
combined = rd(LAND + "/combined_library_entries.json")
im = rd(WS + "/data/individuals/H-AZJ-001_modes.json")
fg = rd(WS + "/data/figures/H-AZJ-001.json")
fm = rd(WS + "/data/figures/H-AZJ-001_modes.json")
assert len(entries) == 10 and [e["id"] for e in entries] == CODES
assert entries == combined["modes"] == im["modes"] == fg["modes"], "三面不一致"
if "thinking_modes_v6_phase20" in fm:
    assert entries == fm["thinking_modes_v6_phase20"]
if "modes" in fm:
    assert entries == fm["modes"]
assert all(e["figure_code"] == FIG and e["figure_name"] == FNAME for e in entries)
assert all(e["mode_code"] == e["id"] for e in entries)
assert all(e["verification"]["status"] == "pending" for e in entries)
assert all(not e.get("legacy_mode_id") for e in entries)
assert fg["mode_ids"] == CODES and fg["thinking_mode_count"] == 10
assert fg.get("cross_references") == []
prop = rd(LAND + "/top_block_proposal.json")["proposal"]
assert prop["code"] == FIG and prop["name_zh"].startswith(FNAME) and prop["core_modes"] == CODES
step("load_landing", n=len(entries), block_keys=len(prop), three_face=True)

# ---------- 2. 前置断言（幂等护栏 + 在途写者护栏；命中即 ABORT）----------
md = rd(WS + "/data/modes_data.json")
cm = rd(WS + "/data/code_maps.json")
fn = rd(WS + "/data/figure_names.json")
sz = rd(WS + "/data/scenarios_zh.json")
se = rd(WS + "/data/scenarios_en.json")
st = rd(WS + "/data/scenario_tags.json")
cm_fig_before = {k: v for k, v in cm["figures"].items()}
fn_before = dict(fn)
ids = set(m.get("id") for m in md["modes"])
alr = sorted(set(CODES) & ids)
assert not alr, "ABORT: M-AZJ already in library: %s" % alr
assert "M-AZJ" not in json.dumps([m.get("mode_code") for m in md["modes"]]), "ABORT: M-AZJ mode_code present"
assert FIG not in cm["figures"], "ABORT: %s already registered in code_maps" % FIG
assert FIG not in fn, "ABORT: %s already in figure_names" % FIG
assert FIG not in md, "ABORT: top-level block %s already present" % FIG
for nm, obj in (("scenarios_zh", sz), ("scenarios_en", se), ("scenario_tags", st)):
    assert "AZJ" not in json.dumps(obj, ensure_ascii=False), "ABORT: AZJ residual in " + nm
ev = rd(WS + "/docs/research/phase21r9_azj_landing_evidence.json")
ref_before = ev["zero_library_write"]["before"]
for rel, h in ref_before.items():
    actual = sha_file(os.path.join(WS, rel))
    assert actual == h, "ABORT: library changed since landing: %s" % rel
step("preflight_abort_checks", m_azj_free=True, fig_free=True, azj_residual=0, landing_before_sha_match=True)

# ---------- 3. before 快照（六件）----------
objs = {"data/modes_data.json": md, "data/code_maps.json": cm, "data/scenarios_zh.json": sz,
        "data/scenarios_en.json": se, "data/scenario_tags.json": st, "data/figure_names.json": fn}
before = {}
for rel in WATCH:
    p = os.path.join(WS, rel)
    before[rel] = {"count": count_of(rel, objs[rel]), "sha256": sha_file(p), "bytes": os.path.getsize(p),
                   "trailing_newline": bool(nl_of(p))}
step("before_state", modes=before["data/modes_data.json"]["count"], cm=before["data/code_maps.json"]["count"],
     fn=before["data/figure_names.json"]["count"], total_scalar=md.get("total"))

# ---------- 4. 备份（data/backup_merge_H-AZJ-001_<TS>/，六件 before 全量 + ledger）----------
if not DRY:
    os.makedirs(BACKUP, exist_ok=True)
    for rel in WATCH:
        shutil.copy2(os.path.join(WS, rel), os.path.join(BACKUP, os.path.basename(rel)))
    ledger = {"card": "t_ce457734", "ts": TS, "figure_code": FIG,
              "files": {rel: before[rel]["sha256"] for rel in WATCH},
              "note": "六件 before 全量备份（先备份后合并）；恢复法：cp 回 data/ 同名路径"}
    with open(os.path.join(BACKUP, "backup_ledger.json"), "w", encoding="utf-8") as f:
        f.write(json.dumps(ledger, ensure_ascii=False, indent=1) + "\n")
    step("backup", dir=BACKUP, files=len(WATCH) + 1)
else:
    step("backup", skipped=True)

# ---------- 5. 构造新增内容 ----------
new_modes = list(entries)
cm_entry = {"mode_ids": CODES, "tags": [e["name_zh"] for e in entries],
            "cross_references": list(fg.get("cross_references") or [])}
nb = {}
for k, v in md.items():
    if k == "modes":
        nb[FIG] = prop
    nb[k] = v
nb["modes"] = list(nb["modes"]) + new_modes
old_total = nb["total"]
nb["total"] = len(nb["modes"])
md2 = nb
cm2 = cm
cm2["figures"][FIG] = cm_entry
fn2 = fn
fn2[FIG] = FNAME
step("construct", new_modes=len(new_modes), top_block=FIG, total_from=old_total, total_to=nb["total"],
     cm_tags=len(cm_entry["tags"]), cm_xref=len(cm_entry["cross_references"]))

# ---------- 6. 写盘 ----------
if not DRY:
    wr(os.path.join(WS, MAIN["modes"]), md2)
    wr(os.path.join(WS, MAIN["cm"]), cm2)
    wr(os.path.join(WS, MAIN["fn"]), fn2)
    step("written", files=list(MAIN.values()))
else:
    step("written", dry=True)

# ---------- 7. after 快照与不变量断言（先记 before 副本，避免别名污染）----------
after = {}
if not DRY:
    for rel in WATCH:
        p = os.path.join(WS, rel)
        after[rel] = {"count": count_of(rel, rd(p)), "sha256": sha_file(p), "bytes": os.path.getsize(p)}
    for rel in ("data/scenarios_zh.json", "data/scenarios_en.json", "data/scenario_tags.json"):
        assert after[rel]["sha256"] == before[rel]["sha256"], "unexpected write: " + rel
    assert after["data/modes_data.json"]["count"] == before["data/modes_data.json"]["count"] + 10
    assert after["data/code_maps.json"]["count"] == before["data/code_maps.json"]["count"] + 1
    assert after["data/figure_names.json"]["count"] == before["data/figure_names.json"]["count"] + 1
    md_a = rd(os.path.join(WS, MAIN["modes"]))
    cm_a = rd(os.path.join(WS, MAIN["cm"]))
    fn_a = rd(os.path.join(WS, MAIN["fn"]))
    assert set(md_a.keys()) == set(md.keys()) | {FIG}, "unexpected top-level keys"
    assert md_a["modes"][:len(md["modes"])] == md["modes"], "modes prefix mismatch"
    assert md_a["modes"][len(md["modes"]):] == new_modes, "appended modes mismatch"
    for k in md:
        if k in ("total", "modes"):
            continue
        assert md_a[k] == md[k], "top-level changed: " + k
    assert md_a[FIG] == prop, "top block mismatch"
    assert md_a["total"] == len(md_a["modes"]), "total not aligned"
    assert {k: v for k, v in cm_a["figures"].items() if k != FIG} == cm_fig_before, "code_maps others changed"
    assert cm_a["figures"][FIG] == cm_entry
    assert {k: v for k, v in fn_a.items() if k != FIG} == fn_before, "figure_names others changed"
    assert fn_a[FIG] == FNAME
    step("after_state", modes=after["data/modes_data.json"]["count"], cm=after["data/code_maps.json"]["count"],
         fn=after["data/figure_names.json"]["count"], total=md_a["total"], zero_write_scen=True)

# ---------- 8. 审计 manifest 与合并日志 ----------
manifest = {
    "schema": "protreptic.phase21r9_azj_merge/v1",
    "card": "t_ce457734", "date": "2026-09-24", "ts": TS, "dry": DRY,
    "figure_code": FIG, "figure_name": FNAME,
    "upstream": {"sourcing_card": "t_1aa06d0c", "rebuild_card": "t_58ebf9c2",
                 "rebuild_commits": ["602a5d47", "25176b26"],
                 "landing_dir": "docs/scratch/legacy20_r9_azj_landing/",
                 "entries_sha256": sha_file(LAND + "/modes_library_entries.json"),
                 "top_block_proposal_sha256": sha_file(LAND + "/top_block_proposal.json"),
                 "landing_before_sha_verified": True},
    "inputs_after_write": {rel: sha_file(os.path.join(WS, rel)) for rel in MAIN.values()},
    "added": {"modes": CODES, "top_level_block": FIG, "code_maps": FIG, "figure_names": {FIG: FNAME},
              "scenarios_zh": 0, "scenarios_en": 0, "scenario_tags": 0},
    "rules": {
        "append_only": "纯追加零删改：旧对象逐对象全等；scenarios_zh/en + scenario_tags 三件 sha 前后一致（零写入）",
        "top_block": "顶层块新增（非替换）：H-AZJ-345 旧块已判死清档；插入位置=第一个 H-* 块组末位、modes 键之前；23 键与库内块同构；提案包装字段不入库",
        "total_scalar": "随动对齐：total = len(modes)（先例：R5 2948->3162=len(modes)、R6 收尾 95139996 对齐 3271；09-24 QA 登记的口径漂移项本卡闭环；全库零现役消费方）",
        "scenarios": "0 新增：AZJ-2 landing scenario_notes 登记 0 新/0 旧处置；本卡不造场景与标签，三件零写入",
        "code_maps": "3 键 mode_ids/tags/cross_references；tags=10 中文模式名；cross_references=[]（图档为空并有 caveat 如实登记，不代拟）",
        "figure_names": "键级追加 H-AZJ-001 -> 安子介（文末）；其余键零改动",
        "serialization": "modes_data.json 无尾换行（现行态保持）；code_maps/figure_names 有尾换行保持；其余三件零写入",
        "db_and_mirrors": "api/protreptic.db 与 tools/json 镜像零改动（现役先例：R8 王祥/罗瑞卿合并未触；DB figures 表为情景主题建表；实测 H-WL-001/H-ZX-001/H-LUORQ-001 在该表 0 行）",
        "verification": "10/10 保持 pending，不回填（与 AZJ-2 落盘逐字一致）"},
    "before": before, "after": after,
    "backup": {"dir": BACKUP, "ledger": "backup_ledger.json",
               "files": sorted(os.path.basename(r) for r in WATCH)}}
if not DRY:
    os.makedirs(EVID, exist_ok=True)
    mp = os.path.join(WS, "data/audit/phase21r9_azj_merge_manifest.json")
    with open(mp, "w", encoding="utf-8") as f:
        f.write(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    with open(os.path.join(EVID, "merge_log_azj.json"), "w", encoding="utf-8") as f:
        f.write(json.dumps(log, ensure_ascii=False, indent=1) + "\n")
    print("[DONE] manifest=", mp)
else:
    print("[DONE] dry-run only")
