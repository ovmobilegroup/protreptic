#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# merge_iqb_hiqb001.py -- Phase 21 伊克巴尔 H-IQB-001 合并入主库（卡 t_30a3e702）
# 口径：纯追加零删改
#   modes_data.json  : modes +10（尾部，逐字等于落盘包 entries）；顶层块 H-IQB-001 新增（23 键，置于 'modes' 前）；total 随动 = len(modes)
#   code_maps.json   : figures +1（H-IQB-001 = {mode_ids, tags, cross_references 仅已注册目标}）
#   figure_names.json: 键级追加 H-IQB-001 -> 伊克巴尔
#   scenarios_zh/en  : 各 +10（C-IQB-001~010 / C-IQB-001E~010E，模板复算沿 C-WX/C-LUORQ/C-SHF 规则）
#   scenario_tags.json: +20（每模式 zh/en 两标签）
#   data/figures|individuals 四件：按落盘包逐字节落盘（上游落地卡未落盘）
# 幂等：主库已含完整本链足迹 -> [SKIP]（不写盘）；部分足迹 -> exit 2
# 并发护栏：读 → 构造 → 写前复读 sha 不变才写；检测到兄弟卡在途写入时自动重读重试
import hashlib
import io
import json
import os
import shutil
import sys
import time
from datetime import datetime

WS = "/opt/data/workspace/Protreptic"
CARD = "/opt/data/kanban/boards/protreptic/workspaces/t_30a3e702"
LAND = WS + "/docs/scratch/phase21_iqb_landing"
TS = os.environ.get("IQB_TS") or datetime.now().strftime("%Y%m%d_%H%M%S")
BACKUP = WS + "/data/backup_merge_H-IQB-001_" + TS
EVID = os.path.join(CARD, "evidence")
DRY = "--dry" in sys.argv
ATTEMPTS = 8

FIG = "H-IQB-001"
FNAME = "伊克巴尔"
CODES = ["M-IQB-%03d" % i for i in range(1, 11)]
SCODES = ["C-IQB-%03d" % i for i in range(1, 11)]
SCODES_E = ["C-IQB-%03dE" % i for i in range(1, 11)]
SIX = ["data/modes_data.json", "data/code_maps.json", "data/figure_names.json",
       "data/scenarios_zh.json", "data/scenarios_en.json", "data/scenario_tags.json"]
FOUR = ["data/figures/H-IQB-001.json", "data/figures/H-IQB-001_modes.json",
        "data/individuals/H-IQB-001.json", "data/individuals/H-IQB-001_modes.json"]
WATCH = SIX + FOUR
XREG = ("H-GAN-001", "H-ATK-001", "H-IKH-001")  # 已注册 xref 目标（H-GHZ-001 只名录未注册，按纪律不收录）


def rd(rel_or_abs):
    p = rel_or_abs if os.path.isabs(rel_or_abs) else os.path.join(WS, rel_or_abs)
    with io.open(p, encoding="utf-8") as f:
        return json.load(f)


def sha_file(p):
    with io.open(p, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def nl_of(p):
    if not os.path.exists(p):
        return "\n"
    return "\n" if open(p, "rb").read().endswith(b"\n") else ""


def dump_bytes(rel, obj):
    return (json.dumps(obj, ensure_ascii=False, indent=2) + nl_of(os.path.join(WS, rel))).encode("utf-8")


def count_of(rel, obj):
    if rel.endswith("modes_data.json"): return len(obj["modes"])
    if rel.endswith("code_maps.json"): return len(obj["figures"])
    if rel.endswith("scenarios_zh.json"): return len(obj["scenarios_zh"])
    if rel.endswith("scenarios_en.json"): return len(obj["scenarios_en"])
    if rel.endswith("scenario_tags.json"): return len(obj["scenario_tags"])
    return len(obj)


log = {"card": "t_30a3e702", "ts": TS, "dry": DRY, "steps": []}


def step(name, **kw):
    kw["step"] = name
    log["steps"].append(kw)
    print("[STEP]", name, json.dumps(kw, ensure_ascii=False)[:600])


def build_scen(entry, code):
    text_zh = entry["name_zh"] + "的当代应用场景：" + "；".join(entry.get("modern_applications_zh", [])) + "。"
    text_en = ("Contemporary applications of " + entry["name_en"] + ": "
               + "; ".join(entry.get("modern_applications_en", [])) + ".")
    return {"code": code, "mode_code": entry["mode_code"],
            "title_zh": entry["name_zh"], "title_en": entry["name_en"],
            "text_zh": text_zh, "text_en": text_en,
            "application_area_zh": list(entry.get("modern_applications_zh", [])),
            "application_area_en": list(entry.get("modern_applications_en", []))}


def main():
    # ---------- 0. 序列化自检（六件按现行 indent=2 + 尾换行态可逐字节复写） ----------
    for rel in SIX:
        p = os.path.join(WS, rel)
        raw = open(p, "rb").read()
        out = dump_bytes(rel, json.loads(raw.decode("utf-8")))
        assert raw == out, "serialization mismatch: " + rel
    step("serialization_selfcheck", files=len(SIX), ok=True)

    # ---------- 1. 载入落盘包（三面同体 + 与 landing manifest sha 校验） ----------
    lman = rd("data/audit/phase21_iqb_landing_manifest.json")
    for rel, meta in lman["files"].items():
        actual = sha_file(os.path.join(LAND, rel))
        assert actual == meta["sha256"], "landing sha mismatch: " + rel
    entries = rd(LAND + "/modes_library_entries.json")
    combined = rd(LAND + "/combined_library_entries.json")
    fm = rd(LAND + "/figures/H-IQB-001_modes.json")
    fg = rd(LAND + "/figures/H-IQB-001.json")
    im = rd(LAND + "/individuals/H-IQB-001_modes.json")
    assert len(entries) == 10 and [e["id"] for e in entries] == CODES
    assert entries == combined["modes"] == im["modes"] == fm["modes"] == fg["modes"], "三面不一致"
    assert all(e["figure_code"] == FIG and e["figure_name"] == FNAME for e in entries)
    assert all(e["mode_code"] == e["id"] for e in entries)
    assert all(e["verification"]["status"] == "pending" for e in entries)
    assert all(not e.get("legacy_mode_id") for e in entries)
    assert fg["mode_ids"] == CODES and fg["thinking_mode_count"] == 10
    assert [x["target_figure_code"] for x in fg["cross_references"]] == list(XREG)
    prop = rd(LAND + "/top_block_proposal.json")["proposal"]
    assert prop["code"] == FIG and prop["name_zh"].startswith(FNAME) and prop["core_modes"] == CODES
    step("load_landing", n=len(entries), block_keys=len(prop), three_face=True, xrefs=len(XREG))

    # ---------- 2..8. 读-构造-写 循环（并发护栏） ----------
    done = False
    for attempt in range(1, ATTEMPTS + 1):
        # 2. 前置断言（幂等护栏）
        md = rd(SIX[0]); cm = rd(SIX[1]); fn = rd(SIX[2])
        sz = rd(SIX[3]); se = rd(SIX[4]); st = rd(SIX[5])
        ids = set(m.get("id") for m in md["modes"])
        full_alr = set(CODES) <= ids
        if full_alr:
            assert FIG in cm["figures"] and FIG in fn and FIG in md, "partial merge state"
            scen_ok = all(c in sz["scenarios_zh"] for c in SCODES) and all(c in se["scenarios_en"] for c in SCODES_E)
            tag_ok = sum(1 for t in st["scenario_tags"] if isinstance(t, dict) and str(t.get("mode_code", "")).startswith("M-IQB")) == 20
            four_ok = all(os.path.exists(os.path.join(WS, r)) for r in FOUR)
            assert scen_ok and tag_ok and four_ok, "partial merge state (scen/tags/files)"
            print("[SKIP] already fully merged (attempt %d)" % attempt)
            step("skip_already_merged", modes=len(md["modes"]), total=md.get("total"))
            return 0
        alr = sorted(set(CODES) & ids)
        assert not alr, "ABORT: M-IQB already in library: %s" % alr
        assert "M-IQB" not in json.dumps([m.get("mode_code") for m in md["modes"]]), "ABORT: M-IQB mode_code present"
        assert FIG not in cm["figures"], "ABORT: %s already registered in code_maps" % FIG
        assert FIG not in fn, "ABORT: %s already in figure_names" % FIG
        assert FIG not in md, "ABORT: top-level block %s already present" % FIG
        for nm, obj in (("scenarios_zh", sz), ("scenarios_en", se), ("scenario_tags", st)):
            assert "IQB" not in json.dumps(obj, ensure_ascii=False), "ABORT: IQB residual in " + nm
        for r in FOUR:
            assert not os.path.exists(os.path.join(WS, r)), "ABORT: %s already exists" % r

        # 3. before 快照
        before_sha = {rel: sha_file(os.path.join(WS, rel)) for rel in SIX}
        before = {}
        objs = dict(zip(SIX, (md, cm, fn, sz, se, st)))
        for rel in SIX:
            before[rel] = {"count": count_of(rel, objs[rel]), "sha256": before_sha[rel],
                           "bytes": os.path.getsize(os.path.join(WS, rel)), "trailing_newline": bool(nl_of(os.path.join(WS, rel)))}
        for rel in FOUR:
            before[rel] = {"count": None, "sha256": None, "bytes": None, "absent": True}

        # 4. 构造
        cm_fig_before = {k: v for k, v in cm["figures"].items()}
        fn_before = dict(fn)
        new_modes = json.loads(json.dumps(entries, ensure_ascii=False))
        cm_entry = {"mode_ids": CODES, "tags": [e["name_zh"] for e in entries],
                    "cross_references": json.loads(json.dumps(fg["cross_references"], ensure_ascii=False))}
        nb = {}
        for k, v in md.items():
            if k == "modes":
                nb[FIG] = json.loads(json.dumps(prop, ensure_ascii=False))
            nb[k] = v
        nb["modes"] = list(nb["modes"]) + new_modes
        old_total = nb["total"]
        nb["total"] = len(nb["modes"])
        md2 = nb
        cm2 = json.loads(json.dumps(cm, ensure_ascii=False))
        cm2["figures"][FIG] = cm_entry
        fn2 = dict(fn); fn2[FIG] = FNAME
        sz2 = json.loads(json.dumps(sz, ensure_ascii=False))
        se2 = json.loads(json.dumps(se, ensure_ascii=False))
        st2 = json.loads(json.dumps(st, ensure_ascii=False))
        for i, e in enumerate(entries):
            sz2["scenarios_zh"][SCODES[i]] = build_scen(e, SCODES[i])
            se2["scenarios_en"][SCODES_E[i]] = build_scen(e, SCODES_E[i])
        for e in entries:
            st2["scenario_tags"].append({"mode_code": e["mode_code"], "tag": e["name_zh"] + "_zh",
                                         "figure_code": FIG, "language": "zh"})
            st2["scenario_tags"].append({"mode_code": e["mode_code"], "tag": e["name_en"] + "_en",
                                         "figure_code": FIG, "language": "en"})
        new_raw = {SIX[0]: dump_bytes(SIX[0], md2), SIX[1]: dump_bytes(SIX[1], cm2), SIX[2]: dump_bytes(SIX[2], fn2),
                   SIX[3]: dump_bytes(SIX[3], sz2), SIX[4]: dump_bytes(SIX[4], se2), SIX[5]: dump_bytes(SIX[5], st2)}
        four_raw = {r: open(os.path.join(LAND, r.replace("data/figures/", "figures/").replace("data/individuals/", "individuals/")), "rb").read() for r in FOUR}
        step("construct", attempt=attempt, new_modes=len(new_modes), top_block=FIG,
             total_from=old_total, total_to=nb["total"], cm_tags=len(cm_entry["tags"]), cm_xref=len(cm_entry["cross_references"]),
             scen_zh=len(SCODES), scen_en=len(SCODES_E), tags=20)

        # 5. 并发护栏：写前复读 sha 与读入时一致才写
        now_sha = {rel: sha_file(os.path.join(WS, rel)) for rel in SIX}
        moved = [rel for rel in SIX if now_sha[rel] != before_sha[rel]]
        if moved:
            print("[CONTEND] library moved under us (%d files) -- retry" % len(moved))
            time.sleep(1.5)
            continue
        if DRY:
            step("dry_run_ok", attempt=attempt)
            print("[DONE] dry-run only")
            return 0

        # 6. 备份 + 写盘
        if attempt == 1:
            os.makedirs(BACKUP, exist_ok=True)
            for rel in SIX:
                shutil.copy2(os.path.join(WS, rel), os.path.join(BACKUP, os.path.basename(rel)))
            ledger = {"card": "t_30a3e702", "ts": TS, "figure_code": FIG,
                      "files": {rel: before_sha[rel] for rel in SIX},
                      "note": "六件 before 全量备份（先备份后合并）；恢复法：cp 回 data/ 同名路径；四件数据件为新增（无 before）"}
            with io.open(os.path.join(BACKUP, "backup_ledger.json"), "w", encoding="utf-8") as f:
                f.write(json.dumps(ledger, ensure_ascii=False, indent=1) + "\n")
            step("backup", dir=BACKUP, files=len(SIX) + 1)
        for rel in SIX:
            tmp = os.path.join(WS, rel + ".merge_tmp")
            with io.open(tmp, "wb") as f:
                f.write(new_raw[rel])
            os.replace(tmp, os.path.join(WS, rel))
        for rel in FOUR:
            p = os.path.join(WS, rel)
            os.makedirs(os.path.dirname(p), exist_ok=True)
            tmp = p + ".merge_tmp"
            with io.open(tmp, "wb") as f:
                f.write(four_raw[rel])
            os.replace(tmp, p)
        step("written", files=SIX + FOUR)

        # 7. after 快照与不变量断言
        after = {}
        for rel in WATCH:
            p = os.path.join(WS, rel)
            after[rel] = {"count": count_of(rel, rd(p)), "sha256": sha_file(p), "bytes": os.path.getsize(p)}
        md_a = rd(SIX[0]); cm_a = rd(SIX[1]); fn_a = rd(SIX[2])
        sz_a = rd(SIX[3]); se_a = rd(SIX[4]); st_a = rd(SIX[5])
        assert after[SIX[0]]["count"] == before[SIX[0]]["count"] + 10
        assert after[SIX[1]]["count"] == before[SIX[1]]["count"] + 1
        assert after[SIX[2]]["count"] == before[SIX[2]]["count"] + 1
        assert after[SIX[3]]["count"] == before[SIX[3]]["count"] + 10
        assert after[SIX[4]]["count"] == before[SIX[4]]["count"] + 10
        assert after[SIX[5]]["count"] == before[SIX[5]]["count"] + 20
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
        # scenarios: 前缀相等（旧键零改动）+ 新增逐字
        zh_old = list(sz["scenarios_zh"].items())
        assert list(sz_a["scenarios_zh"].items())[:len(zh_old)] == zh_old, "scenarios_zh prefix mismatch"
        for i, e in enumerate(entries):
            assert sz_a["scenarios_zh"][SCODES[i]] == build_scen(e, SCODES[i])
            assert se_a["scenarios_en"][SCODES_E[i]] == build_scen(e, SCODES_E[i])
        assert len(st_a["scenario_tags"]) == len(st["scenario_tags"]) + 20
        assert st_a["scenario_tags"][:len(st["scenario_tags"])] == st["scenario_tags"], "tags prefix mismatch"
        step("after_state", modes=after[SIX[0]]["count"], cm=after[SIX[1]]["count"], fn=after[SIX[2]]["count"],
             total=md_a["total"], scen_zh=after[SIX[3]]["count"], scen_en=after[SIX[4]]["count"], tags=after[SIX[5]]["count"])
        done = True

        # 8. 审计 manifest 与合并日志
        manifest = {
            "schema": "protreptic.phase21_iqb_merge/v1",
            "card": "t_30a3e702", "date": "2026-09-24", "ts": TS, "dry": DRY,
            "figure_code": FIG, "figure_name": FNAME,
            "upstream": {"research_card": "t_16080f61", "landing_card": "t_6839d252",
                         "landing_pack": "docs/scratch/phase21_iqb_landing/",
                         "landing_manifest": "data/audit/phase21_iqb_landing_manifest.json",
                         "note": "上游落地卡仅导入遗留库 protreptic.db（ca7b2f31），未落盘量件；落盘包由本合并卡按研究产出生成"},
            "inputs_after_write": {rel: after[rel]["sha256"] for rel in SIX},
            "added": {"modes": CODES, "top_level_block": FIG, "code_maps": FIG, "figure_names": {FIG: FNAME},
                      "scenarios_zh": SCODES, "scenarios_en": SCODES_E, "scenario_tags": 20,
                      "data_files": FOUR},
            "rules": {
                "append_only": "纯追加零删改：旧对象逐对象全等（modes 前缀/其余 figures/figure_names/scenarios 前缀/tags 前缀）",
                "top_block": "顶层块新增（非替换）：位置=第一 H-* 块组末位、'modes' 键之前；23 键与库内块同构",
                "total_scalar": "随动对齐：total = len(modes)",
                "scenarios": "模板复算 10+10（沿 C-WX/C-LUORQ/C-SHF 生成规则；text = name + modern_applications）；C-IQB-001~010 / 001E~010E",
                "code_maps": "3 键 mode_ids/tags/cross_references；xref 仅已注册目标（H-GAN-001/H-ATK-001/H-IKH-001；H-GHZ-001 只名录未注册，caveat 登记不收录）",
                "figure_names": "键级追加 H-IQB-001 -> 伊克巴尔（文末）；其余键零改动",
                "serialization": "六件 indent=2 + 尾换行按现行态逐字节保持；四件数据件按落盘包逐字节落盘",
                "verification": "10/10 保持 pending，不回填",
                "concurrency": "写前复读六件 sha 护栏（兄弟卡在途写入自动重试）；attempt=%d" % attempt},
            "before": before, "after": after,
            "backup": {"dir": BACKUP, "ledger": "backup_ledger.json",
                       "files": sorted(os.path.basename(r) for r in SIX)}}
        os.makedirs(EVID, exist_ok=True)
        mp = os.path.join(WS, "data/audit/phase21_iqb_merge_manifest.json")
        with io.open(mp, "w", encoding="utf-8") as f:
            f.write(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
        with io.open(os.path.join(EVID, "merge_log_iqb.json"), "w", encoding="utf-8") as f:
            f.write(json.dumps(log, ensure_ascii=False, indent=1) + "\n")
        print("[DONE] manifest=", mp)
        return 0
    if not done:
        print("[FAIL] too many contentions, no write")
        return 2


if __name__ == "__main__":
    sys.exit(main())
