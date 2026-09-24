#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""verify_azj_merge_indep.py - Phase21-R9 安子介(H-AZJ-001)合并卡 t_ce457734 独立核验

口径（与上游 verify_phase21r9_azj.py 互补，不重叠其断言面；直读文件实测，不采信合并卡自述）:
  A 输入完整性: 落盘包/数据件 sha256 与 landing manifest 一致；三面同体；条目不变量
  B 主库 modes_data: +10 纯追加（before=备份），逐字等于 entries，27 键，pending 10/10，legacy 空，0 重复码，文末位置
  C 顶层块: H-AZJ-001 新增（23 键与库内块同构、位于 modes 前），其余顶层键零改动，total 对齐 len(modes)
  D 注册面: code_maps +1（3 键、tags=10 中文模式名、xref=[]），figure_names +1（文末），其余键零改动
  E 零写入与边界: scenarios_zh/en + scenario_tags 三件 sha 前后一致；归档件未动；旧载荷标记零出现
  F 门禁复算: credibility/findings/verifstatus/sourcelinks 四连 exit 0
  G 站点链: 锚点 3291/319/1027 == 实测；meta.json/siteCounts/manifest/docs 文案；daily；preflight --stage data
  H 审计: merge manifest before/after sha == 实测；备份目录齐备；报告落盘
  I 上游回归: verify_phase21r9_azj.py（合并后口径）0 FAIL；原 landing 证据文件未动
输出: docs/research/phase21r9_azj_merge_evidence.json / .txt；FAIL 时 exit 1
"""
import hashlib
import io
import json
import os
import subprocess
import sys

REPO = "/opt/data/workspace/Protreptic"
BACKUP = REPO + "/data/backup_merge_H-AZJ-001_20260924_092502"
LANDING = REPO + "/docs/scratch/legacy20_r9_azj_landing"
MMAN = REPO + "/data/audit/phase21r9_azj_merge_manifest.json"
LMAN = REPO + "/data/audit/phase21r9_azj_landing_manifest.json"
FIG = "H-AZJ-001"
FNAME = "安子介"
CODES = ["M-AZJ-%03d" % i for i in range(1, 11)]
ENTRY_KEYS = ["id", "mode_code", "figure_code", "figure_name", "name_zh", "name_en", "category", "category_raw",
              "domain_zh", "domain_en", "level", "priority", "definition_zh", "definition_en", "source_chapter",
              "key_concepts", "key_quote_zh", "key_quote_en", "process_zh", "process_en", "representative_cases_zh",
              "representative_cases_en", "modern_applications_zh", "modern_applications_en", "related_modes",
              "legacy_mode_id", "verification"]
FORBIDDEN = ["特区建设", "摸着石头过河", "安子介回忆录", "深圳特区建设档案", "An Zijie", "SEZ", "《安子介回忆录》"]
PASS, FAIL = [], []

def check(cond, msg):
    (PASS if cond else FAIL).append(msg)
    print(("  [PASS] " if cond else "  [FAIL] ") + msg)

def sha_file(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()

def jl(p):
    with io.open(p, encoding="utf-8") as f:
        return json.load(f)

def txt(p):
    with io.open(p, encoding="utf-8") as f:
        return f.read()

def run(args, timeout=1800):
    r = subprocess.run(args, cwd=REPO, capture_output=True, text=True, timeout=timeout)
    return r.returncode, (r.stdout or "") + (r.stderr or "")

def main():
    print("== A 输入完整性 ==")
    lm = jl(LMAN)
    for rel, want in sorted(lm["deliverables"].items()):
        want_sha = want["sha256"] if isinstance(want, dict) else want
        check(sha_file(os.path.join(REPO, rel)) == want_sha, "A 落盘件 sha256 == landing manifest: " + rel)
    for name, want in sorted(lm["pack_sha256"].items()):
        check(sha_file(os.path.join(REPO, "docs/research", name)) == want, "A 素材包 sha256 == landing manifest: " + name)
    entries = jl(os.path.join(LANDING, "modes_library_entries.json"))
    combined = jl(os.path.join(LANDING, "combined_library_entries.json"))
    im = jl(os.path.join(REPO, "data/individuals/H-AZJ-001_modes.json"))
    fg = jl(os.path.join(REPO, "data/figures/H-AZJ-001.json"))
    check(len(entries) == 10 and [e["id"] for e in entries] == CODES, "A entries 10 条且码序 M-AZJ-001~010")
    check([e["mode_code"] for e in entries] == CODES, "A mode_code 与 id 同序")
    check(entries == combined["modes"], "A entries == combined.modes")
    check(entries == im["modes"], "A entries == individuals _modes.modes")
    check(entries == fg["modes"], "A entries == figure.modes（三面同体）")
    check(all(e["verification"]["status"] == "pending" for e in entries), "A verification 10/10 pending")
    check(all(not e.get("legacy_mode_id") for e in entries), "A legacy_mode_id 全空（旧号段不复用）")
    check(fg["mode_ids"] == CODES and fg["thinking_mode_count"] == 10, "A 图档 mode_ids/计数 == 10")
    check(fg.get("cross_references") == [], "A 图档 cross_references 为空（caveat 已登记）")

    print("== B 主库 modes_data ==")
    md = jl(REPO + "/data/modes_data.json")
    bmd = jl(BACKUP + "/modes_data.json")
    modes = md["modes"]
    bmodes = bmd["modes"]
    sib = [m for m in modes if str(m.get("mode_code", "")).startswith("M-SHF-")]
    check(len(modes) == len(bmodes) + 10 + len(sib), "B 条数 %d -> %d（本卡 +10；兄弟卡 t_a7d233f0 +%d，链式可解释）" % (len(bmodes), len(modes), len(sib)))
    check(modes[:len(bmodes)] == bmodes, "B 前 %d 条逐对象全等（纯追加零删改）" % len(bmodes))
    check(modes[len(bmodes):len(bmodes) + 10] == entries, "B 本卡 10 条逐字等于 AZJ-2 entries（先于兄弟卡增量）")
    check([m["id"] for m in modes[len(bmodes):len(bmodes) + 10]] == CODES, "B 本卡 10 条码序 M-AZJ-001~010")
    check(all(set(m.keys()) == set(ENTRY_KEYS) for m in modes[len(bmodes):len(bmodes) + 10]), "B 本卡 10 条 27 键齐全")
    check(all(m["figure_code"] == FIG and m["figure_name"] == FNAME for m in modes[len(bmodes):len(bmodes) + 10]), "B figure_code/名 == H-AZJ-001/安子介")
    codes = [m.get("mode_code") for m in modes if m.get("mode_code")]
    check(len(codes) == len(set(codes)), "B 全库 mode_code 0 重复")
    n_azj = sum(1 for m in modes if m.get("mode_code") and "AZJ" in str(m.get("mode_code")))
    check(n_azj == 10, "B 全库 M-AZJ 仅 10 条（无额外命中）")

    print("== C 顶层块与 total ==")
    check(FIG in md, "C 顶层块 H-AZJ-001 存在")
    prop = jl(os.path.join(LANDING, "top_block_proposal.json"))["proposal"]
    check(md[FIG] == prop, "C 顶层块逐字 == top_block_proposal.proposal")
    check(len(md[FIG]) == 23, "C 顶层块 23 键")
    keys = list(md.keys())
    between = keys[keys.index(FIG) + 1:keys.index("modes")]
    check(all(str(k).startswith("H-SHF-") for k in between), "C 顶层块位于 modes 前（其后仅兄弟卡块 %s）" % repr(between))
    added = [k for k in keys if k not in bmd]
    check(set(bmd) <= set(keys) and FIG in added and all((k == FIG) or str(k).startswith("H-SHF-") for k in added), "C 顶层新增键 = 本卡 H-AZJ-001 + 兄弟卡 %s" % repr(added))
    changed = [k for k in bmd if k not in ("total", "modes") and md.get(k) != bmd[k]]
    check(not changed, "C 除 total/modes（B 组已证纯追加）与新增块外顶层零改动 " + ("" if not changed else repr(changed)))
    check(md["total"] == len(modes) and md["total"] == len(bmodes) + 10 + len(sib), "C total 对齐 = len(modes) = %d（本卡写盘 3301；兄弟卡 +%d）" % (md["total"], len(sib)))

    print("== D 注册面（code_maps / figure_names）==")
    cm = jl(REPO + "/data/code_maps.json")
    bcm = jl(BACKUP + "/code_maps.json")
    addcm = [k for k in cm["figures"] if k not in bcm["figures"]]
    check(len(cm["figures"]) == len(bcm["figures"]) + len(addcm) and FIG in addcm
          and all((k == FIG) or str(k).startswith("H-SHF-") for k in addcm),
          "D code_maps 新增面 = 本卡 + 兄弟卡 %s（共 %d 条）" % (repr(addcm), len(cm["figures"])))
    check(FIG in cm["figures"], "D code_maps 含 H-AZJ-001")
    cme = cm["figures"].get(FIG, {})
    check(set(cme.keys()) == set(["mode_ids", "tags", "cross_references"]), "D code_maps 条目 3 键")
    check(cme.get("mode_ids") == CODES, "D mode_ids == M-AZJ-001~010")
    check(cme.get("tags") == [x["name_zh"] for x in entries], "D tags == 10 中文模式名（与库内条目同构）")
    check(cme.get("cross_references") == [], "D cross_references == []（0 悬空）")
    dd = [k for k in bcm["figures"] if cm["figures"].get(k) != bcm["figures"][k]]
    check(not dd, "D code_maps 其余条目零改动 " + ("" if not dd else repr(dd[:5])))
    check(all(cm[k] == bcm[k] for k in bcm if k != "figures"), "D code_maps 其余顶层键零改动")
    fn2 = jl(REPO + "/data/figure_names.json")
    bfn = jl(BACKUP + "/figure_names.json")
    addfn = [k for k in fn2 if k not in bfn]
    check(len(fn2) == len(bfn) + len(addfn) and FIG in addfn
          and all((k == FIG) or str(k).startswith("H-SHF-") for k in addfn),
          "D figure_names 新增面 = 本卡 + 兄弟卡 %s（共 %d 条）" % (repr(addfn), len(fn2)))
    check(fn2.get(FIG) == FNAME, "D figure_names[H-AZJ-001] == 安子介")
    check(list(fn2.keys()).index(FIG) == len(bfn), "D figure_names[H-AZJ-001] 位于本卡追加位（先于兄弟卡）")
    df = [k for k in bfn if fn2.get(k) != bfn[k]]
    check(not df and set(bfn) <= set(fn2), "D figure_names 其余条目零改动（仅新增）")

    print("== E 零写入与边界 ==")
    sman = jl(REPO + "/data/audit/phase21r9_shenfu_merge_manifest.json")
    for rel in ["scenarios_zh.json", "scenarios_en.json", "scenario_tags.json"]:
        check(sman["inputs"]["data/" + rel]["sha256"] == sha_file(BACKUP + "/" + rel),
              "E %s 兄弟卡 before == 本卡合并前 sha（本卡零写入，链式可证）" % rel)
    blob = txt(REPO + "/data/scenarios_zh.json") + txt(REPO + "/data/scenarios_en.json") + txt(REPO + "/data/scenario_tags.json")
    check("AZJ" not in blob and "安子介" not in blob, "E 场景三件 AZJ/安子介 0 命中")
    arch = lm["archive_untouched"]
    bad = [k for k, v in arch.items() if sha_file(REPO + "/data/figures/_duplicates/" + k) != v]
    check(not bad, "E 归档件 sha == landing manifest 记录（%d 件）" % len(arch))
    live = {rel: sha_file(REPO + "/data/" + rel) for rel in ["modes_data.json", "code_maps.json", "figure_names.json", "scenarios_zh.json", "scenarios_en.json", "scenario_tags.json"]}
    hit = [rel for rel in live if "AZJ" in txt(REPO + "/data/" + rel)]
    check(sorted(hit) == ["code_maps.json", "figure_names.json", "modes_data.json"], "E 主库六件 AZJ 占用面 == 预期三件 " + repr(sorted(hit)))
    jtxt = json.dumps(modes[len(bmodes):len(bmodes) + 10], ensure_ascii=False) + txt(os.path.join(LANDING, "scenario_notes.json"))
    fb = [f for f in FORBIDDEN if f in jtxt]
    check(not fb, "E 旧载荷 19 项代表标记零出现 " + ("" if not fb else repr(fb)))

    print("== F 门禁复算 ==")
    rc, _o = run(["python3", "tools/credibility_gate.py", "--hard-fail"])
    check(rc == 0, "F credibility_gate --hard-fail exit 0")
    rc, _o = run(["python3", "tools/verify_findings.py", "--hard-fail"])
    check(rc == 0, "F verify_findings --hard-fail exit 0")
    rc, _o = run(["python3", "tools/apply_verification_status.py", "--check"])
    check(rc == 0, "F apply_verification_status --check exit 0（四态与库一致）")
    rc, _o = run(["python3", "tools/verify_source_links.py", "--hard-fail"], timeout=2400)
    check(rc == 0, "F verify_source_links --hard-fail exit 0（无新增坏链）")

    print("== G 站点链 ==")
    exp = txt(REPO + "/tools/export_static_site.py")
    pre = txt(REPO + "/tools/pages_preflight.py")
    m = jl(REPO + "/web/public/data/meta.json")
    c = m["counts"]
    empty_n = len([x for x in modes if not x.get("mode_code")])
    dedup_now = len(modes) - empty_n
    check(("EXPECT_MODES = %d" % dedup_now) in exp and ("EXPECT_MODES = %d" % dedup_now) in pre,
          "G 锚点 EXPECT_MODES == 去壳去重口径 %d（本卡 +10 已在并集基线内，末次写者同步）" % dedup_now)
    check(("EXPECT_BY_FIGURE = %d" % c.get("mode_by_figure_shards")) in exp and ("EXPECT_BY_FIGURE = %d" % c.get("mode_by_figure_shards")) in pre,
          "G 锚点 EXPECT_BY_FIGURE == meta 分片 %s" % c.get("mode_by_figure_shards"))
    check(("EXPECT_FIGURES = %d" % c.get("figures")) in exp and c.get("figures") == 1027,
          "G 锚点 EXPECT_FIGURES == meta figures %s == 1027" % c.get("figures"))
    check(c.get("modes_raw") == len(modes) and c.get("modes_deduped") == dedup_now,
          "G meta: raw %s == len(modes) %d、deduped %s == 去壳口径 %d" % (c.get("modes_raw"), len(modes), c.get("modes_deduped"), dedup_now))
    check(c.get("mode_summaries_published") == dedup_now - c.get("modes_quarantined", 0)
          and c.get("modes_quarantined") == 60,
          "G meta: published %s == deduped - 隔离 60" % c.get("mode_summaries_published"))
    check(c.get("mode_summaries") == c.get("modes_deduped"), "G meta: mode_summaries == deduped（pages_preflight 同口径）")
    pub = c.get("mode_summaries_published")
    shards = c.get("mode_by_figure_shards")
    sc = txt(REPO + "/web/src/generated/siteCounts.ts")
    check(("modes: %d" % pub) in sc and ("figures: %d" % shards) in sc, "G siteCounts.ts %d x %d（与 meta 一致）" % (pub, shards))
    mf = txt(REPO + "/web/public/manifest.webmanifest")
    check(("%d 条思维模式" % pub) in mf and ("%d 位历史人物" % shards) in mf, "G PWA manifest 文案 == 现行口径 %d x %d" % (pub, shards))
    fl = txt(REPO + "/docs/02-tools/figure_library.md")
    check(("%d 条思维模式" % pub) in fl and ("%d 位历史人物" % shards) in fl, "G docs 产品门面页 == 现行口径 %d x %d" % (pub, shards))
    idx = jl(REPO + "/web/public/data/daily/index.json")
    check(idx.get("total") == pub and idx.get("shard_count") == shards and len(idx.get("entries", [])) == pub, "G daily index %d 条 / %d 分片" % (pub, shards))
    rc, _o = run(["python3", "tools/pages_preflight.py", "--stage", "data"])
    check(rc == 0, "G pages_preflight --stage data exit 0（复跑）")

    print("== H 审计 manifest / 备份 ==")
    mm = jl(MMAN)
    check(mm["figure_code"] == FIG and mm["figure_name"] == FNAME and mm["dry"] is False, "H merge manifest: H-AZJ-001/安子介、dry=False")
    for rel in sorted(mm["after"]):
        cur = sha_file(REPO + "/" + rel)
        if rel in mm["inputs_after_write"]:
            check(sman["inputs"][rel]["sha256"] == mm["after"][rel]["sha256"] == mm["inputs_after_write"][rel],
                  "H 链式: 本卡 after == 兄弟卡 before: " + rel)
        else:
            check(mm["after"][rel]["sha256"] == mm["before"][rel]["sha256"] == sman["inputs"][rel]["sha256"],
                  "H 未写入件 before == after == 兄弟 before: " + rel)
    def _av(x):
        return x["sha256"] if isinstance(x, dict) else x
    bad2 = [rel for rel in sman["after"] if sha_file(REPO + "/" + rel) != _av(sman["after"][rel])]
    check(not bad2, "H 现行六件 sha == 兄弟卡 after（末次写者）" + ("" if not bad2 else repr(bad2)))
    ug = sman.get("union_guard") or {}
    check(ug.get("M_AZJ_before") == 10 and ug.get("M_AZJ_after") == 10, "H 兄弟卡 union_guard: M-AZJ 10 条守恒（未伤本卡面）")
    ad = mm["added"]
    check(ad["modes"] == CODES and ad["top_level_block"] == FIG and ad["code_maps"] == FIG, "H added 面 == 预期（modes/顶层块/code_maps）")
    check(ad["figure_names"] == {FIG: FNAME} and ad["scenarios_zh"] == 0 and ad["scenarios_en"] == 0 and ad["scenario_tags"] == 0, "H figure_names 面 + 场景三件零增")
    bl = jl(os.path.join(BACKUP, os.path.basename(mm["backup"]["ledger"])))
    check(bl["card"] == "t_ce457734" and all(bl["files"][rel] == mm["before"][rel]["sha256"] for rel in bl["files"]), "H 备份 ledger sha == before")
    check(sorted(mm["backup"]["files"]) == ["code_maps.json", "figure_names.json", "modes_data.json", "scenario_tags.json", "scenarios_en.json", "scenarios_zh.json"], "H 备份 6 件齐 + ledger")
    check(all(sha_file(BACKUP + "/" + fn) == bl["files"]["data/" + fn] for fn in mm["backup"]["files"]), "H 备份落盘 sha == ledger")
    check(os.path.isfile(REPO + "/docs/research/phase21r9_azj_merge_report.md"), "H 合并报告落盘")

    print("== I 上游回归 ==")
    env = dict(os.environ, AZJ_EVID_OUT="/tmp/azj_regress_evidence.json", AZJ_SCOPE="merged-regression")
    r = subprocess.run(["python3", "verify_phase21r9_azj.py"], cwd=REPO, capture_output=True, text=True, timeout=600, env=env)
    check(r.returncode == 0, "I verify_phase21r9_azj.py（合并后口径）复跑 exit 0")
    ev = jl("/tmp/azj_regress_evidence.json")
    check(ev["failed"] == 0 and ev["passed"] == 81, "I 上游复跑 %d PASS / %d FAIL" % (ev["passed"], ev["failed"]))
    r2 = subprocess.run(["git", "diff", "--quiet", "HEAD", "--", "docs/research/phase21r9_azj_verify_evidence.json"], cwd=REPO, capture_output=True, text=True)
    check(r2.returncode == 0, "I 原 landing 证据文件未动（git diff 空）")

    npass, nfail = len(PASS), len(FAIL)
    print("---")
    print("TOTAL %d PASS / %d FAIL" % (npass, nfail))
    out = dict(card="t_ce457734", figure_code=FIG, date="2026-09-24", tool="verify_azj_merge_indep.py",
               total=npass + nfail, passed=npass, failed=nfail,
               results=[{"status": "PASS", "msg": s} for s in PASS] + [{"status": "FAIL", "msg": s} for s in FAIL])
    with io.open(REPO + "/docs/research/phase21r9_azj_merge_evidence.json", "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
        f.write(u"\n")
    with io.open(REPO + "/docs/research/phase21r9_azj_merge_evidence.txt", "w", encoding="utf-8") as f:
        for s in PASS:
            f.write("PASS " + s + "\n")
        for s in FAIL:
            f.write("FAIL " + s + "\n")
        f.write("\nTOTAL %d PASS / %d FAIL\n" % (npass, nfail))
    sys.exit(1 if nfail else 0)


if __name__ == "__main__":
    main()
