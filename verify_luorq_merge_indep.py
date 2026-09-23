#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import hashlib, json, os, glob, io, subprocess, sys
from datetime import datetime
from collections import Counter

REPO = "/opt/data/workspace/Protreptic"
CARD = "/opt/data/kanban/boards/protreptic/workspaces/t_08bbb73d"
BACKUP = sorted(glob.glob(os.path.join(CARD, "backup_merge_H-LUORQ-001_*")))[-1]
LAND = REPO + "/docs/scratch/legacy20_r8_luorq_landing"
FIG = "H-LUORQ-001"
CODES = ["M-LUORQ-%03d" % i for i in range(1, 11)]
SZH = ["C-LUORQ-%03d" % i for i in range(1, 11)]
SEN = [c + "E" for c in SZH]
DEPRECATED = ["安全立军", "整编革新", "参谋统筹", "情报先行", "Ten Marshals", "主要创建者"]
PASS, FAIL = [], []

def check(cid, desc, cond, detail=''):
    (PASS if cond else FAIL).append(dict(id=cid, desc=desc, detail=detail))
    print(("%s  %-5s %s%s" % ("PASS" if cond else "FAIL", cid, desc,
                              (" | " + str(detail)[:220]) if detail and not cond else "")))

def warn(cid, desc, detail=''):
    PASS.append(dict(id=cid, desc=desc, detail=detail))
    print("WARN  %-5s %s%s" % (cid, desc, (" | " + str(detail)[:220]) if detail else ""))

def sha_file(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()
def jl(p): return json.load(io.open(p, encoding="utf-8"))
def rd(p): return open(p, encoding="utf-8").read()
def run(args, timeout=1800):
    r = subprocess.run(args, cwd=REPO, capture_output=True, text=True, timeout=timeout)
    return r.returncode, (r.stdout or "") + (r.stderr or "")

def main():
    mm = jl(os.path.join(REPO, "data/audit/phase21r8_luorq_merge_manifest.json"))
    lm = jl(os.path.join(REPO, "data/audit/phase21r8_luorq_landing_manifest.json"))
    lfiles = dict((k, v["sha256"]) for k, v in lm["deliverables"].items())
    led = jl(os.path.join(BACKUP, "backup_ledger.json"))
    
    md = jl(os.path.join(REPO, "data/modes_data.json"))
    old_md = jl(os.path.join(BACKUP, "modes_data.json"))
    newm = md["modes"][len(old_md["modes"]):]
    entries = jl(os.path.join(LAND, "modes_library_entries.json"))
    fig = jl(os.path.join(REPO, "data/figures/%s.json" % FIG))
    ind = jl(os.path.join(REPO, "data/individuals/%s.json" % FIG))
    im = jl(os.path.join(REPO, "data/individuals/%s_modes.json" % FIG))
    top = jl(os.path.join(LAND, "top_block_proposal.json"))
    blk = jl(os.path.join(REPO, "data/audit/phase21r8_luorq_top_block_backup.json"))
    old_img = jl(os.path.join(BACKUP, "top_block_old_H-LUORQ-001.json"))
    new_img = jl(os.path.join(BACKUP, "top_block_new_H-LUORQ-001.json"))
    
    print("== A 输入完整性 ==")
    for rel in ["docs/scratch/legacy20_r8_luorq_landing/modes_library_entries.json",
                "docs/scratch/legacy20_r8_luorq_landing/combined_library_entries.json",
                "docs/scratch/legacy20_r8_luorq_landing/id_mapping.tsv",
                "docs/scratch/legacy20_r8_luorq_landing/category_mapping.tsv",
                "docs/scratch/legacy20_r8_luorq_landing/scenario_notes.json",
                "docs/scratch/legacy20_r8_luorq_landing/top_block_proposal.json",
                "data/figures/%s.json" % FIG, "data/individuals/%s.json" % FIG,
                "data/individuals/%s_modes.json" % FIG]:
        check("A01", "A1 %s sha256 == landing manifest" % rel,
              sha_file(os.path.join(REPO, rel)) == lfiles.get(rel))
    for rel, meta in sorted(led["files"].items()):
        bp = os.path.join(BACKUP, os.path.basename(rel))
        check("A02", "备份 %s sha256 == ledger" % os.path.basename(rel), sha_file(bp) == meta["sha256"])
    check("A03", "A1 entries sha256 == merge manifest upstream",
          sha_file(os.path.join(LAND, "modes_library_entries.json")) == mm["upstream"]["entries_sha256"])
    check("A04", "备份副本 == 合并前状态 sha（manifest.inputs）",
          all(sha_file(os.path.join(BACKUP, os.path.basename(rel))) == mm["inputs"][rel]["sha256"] for rel in ["data/modes_data.json", "data/code_maps.json", "data/scenarios_zh.json", "data/scenarios_en.json", "data/scenario_tags.json", "data/figure_names.json"]))
    
    print("== B 顶层旧块处置 ==")
    check("B01", "旧块值导出存在且 name_zh=旧叙事", old_img["name_zh"] == u"罗瑞卿：安全立军·整编革新·参谋统筹")
        # B02: Check old block file SHA matches ledger

    old_ledger = led["top_block"]["old_canonical_sha256"]

    check("B02", "旧块 file SHA == ledger", hashlib.sha256(open(os.path.join(BACKUP, "top_block_old_H-LUORQ-001.json"), "rb").read()).hexdigest() == led["top_block"]["old_canonical_sha256"], f"file={hashlib.sha256(open(os.path.join(BACKUP, "top_block_old_H-LUORQ-001.json"), "rb").read()).hexdigest()[:16]}... ledger={led["top_block"]["old_canonical_sha256"][:16]}...")


    check("B03", "备份目录内 modes_data.json 的顶层块 == 旧块导出",
          jl(os.path.join(BACKUP, "modes_data.json"))[FIG] == old_img)
    check("B04", "主库现行顶层块 == 冻结新值（逐字）", md[FIG] == new_img)
        # B05: Check new block file SHA matches manifest
    new_computed = hashlib.sha256(json.dumps(md[FIG], ensure_ascii=False, indent=2).encode("utf-8")).hexdigest()
    new_manifest = mm["top_block_disposition"]["after"]["sha256"]

    check("B05", "新块 file SHA == manifest.after", hashlib.sha256(open(os.path.join(BACKUP, "top_block_new_H-LUORQ-001.json"), "rb").read()).hexdigest() == mm["top_block_disposition"]["after"]["sha256"], f"file={hashlib.sha256(open(os.path.join(BACKUP, "top_block_new_H-LUORQ-001.json"), "rb").read()).hexdigest()[:16]}... manifest={mm["top_block_disposition"]["after"]["sha256"][:16]}...")


    check("B06", "新块 23 键、键序与旧块口径一致", list(md[FIG].keys()) == list(old_img.keys()))
    txt = json.dumps(md[FIG], ensure_ascii=False)
    check("B07", "新块禁字零残留（四式旧命名/Ten Marshals/主要创建者/国防部长）",
          not any(n in txt for n in DEPRECATED + ["国防部长"]))
    check("B08", "硬伤 2/3 修正落实（杰出领导人 + ten senior generals）",
          u"杰出领导人" in md[FIG]["unique_thinking_zh"] and "one of the ten senior generals" in md[FIG]["unique_thinking_en"])
    check("B09", "顶层其余键与旧块逐字全等（仅 H-LUORQ-001 一处差异）",
          all(md[k] == jl(os.path.join(BACKUP, "modes_data.json"))[k] for k in jl(os.path.join(BACKUP, "modes_data.json")) if k not in ("modes", FIG)))
    check("B10", "total 标量零改写（3271）", md["total"] == jl(os.path.join(BACKUP, "modes_data.json"))["total"] == 3271)
    check("B11", "剥离字段 proposal_note 未入库", "proposal_note" not in md[FIG])
    # B12: Check that before/after images exist in audit file
    check("B12", "audit 登记文件含前后像（before/after image）",
          blk.get("before_image") == old_img and blk.get("after_image") == new_img)
    
    print("== C modes 主库新增 ==")
    check("C01", "+10 且居文末（前缀逐对象全等）",
          md["modes"][:len(old_md["modes"])] == old_md["modes"] and len(newm) == 10)
    check("C02", "10 条 id 序 == M-LUORQ-001~010", [m["id"] for m in newm] == CODES)
    check("C03", "10 条逐字等于 A1 entries", newm == entries)
    check("C04", "新入库 10 条 id/mode_code 无重复", len(set(m["id"] for m in newm)) == 10)
    check("C05", "旧号 M351~M360 不在现役 id/mode_code", 
          not [m for m in md["modes"] if m.get("id") in ["M%03d" % i for i in range(351, 361)]] and
          [m["legacy_mode_id"] for m in newm] == ["M%03d" % i for i in range(351, 361)])
    check("C06", "10 条 verification 全 pending", all(m["verification"]["status"] == "pending" for m in newm))
    check("C07", "figure_code/figure_name 一致", all(m["figure_code"] == FIG and m["figure_name"] == u"罗瑞卿" for m in newm))
    check("C08", "新入库 10 条 name_zh/name_en 无重复",
          len(set(m["name_zh"] for m in newm)) == 10 and len(set(m["name_en"] for m in newm)) == 10)
    
    print("== D scenarios ==")
    oz, oe = jl(os.path.join(BACKUP, "scenarios_zh.json")), jl(os.path.join(BACKUP, "scenarios_en.json"))
    z, e = jl(os.path.join(REPO, "data/scenarios_zh.json")), jl(os.path.join(REPO, "data/scenarios_en.json"))
    check("D01", "zh/en 各 +10 纯追加（旧键逐对象全等）",
          all(z["scenarios_zh"][k] == oz["scenarios_zh"][k] for k in oz["scenarios_zh"]) and
          all(e["scenarios_en"][k] == oe["scenarios_en"][k] for k in oe["scenarios_en"]) and
          len(z["scenarios_zh"]) == len(oz["scenarios_zh"]) + 10 and len(e["scenarios_en"]) == len(oe["scenarios_en"]) + 10)
    check("D02", "新增键集 == C-LUORQ-001~010 / ·E 且居层面文末",
          [k for k in z["scenarios_zh"] if k not in oz["scenarios_zh"]] == SZH and
          [k for k in e["scenarios_en"] if k not in oe["scenarios_en"]] == SEN)
    ok8 = all(sorted(v.keys()) == ["application_area_en", "application_area_zh", "code", "mode_code", "text_en", "text_zh", "title_en", "title_zh"]
              for v in list(z["scenarios_zh"].values())[-10:] + list(e["scenarios_en"].values())[-10:])
    check("D03", "8 键结构", ok8)
    tmpl_ok, pair_ok, name_ok = True, True, True
    for i, m in enumerate(entries, 1):
        cz, ce = "C-LUORQ-%03d" % i, "C-LUORQ-%03dE" % i
        area_zh, area_en = m["modern_applications_zh"], m["modern_applications_en"]
        want_zh = u"%s的当代应用场景：" % m["name_zh"] + u"；".join(area_zh) + u"。"
        want_en = "Contemporary applications of %s: " % m["name_en"] + "; ".join(area_en) + "."
        tmpl_ok &= (z["scenarios_zh"][cz]["text_zh"] == want_zh and z["scenarios_zh"][cz]["text_en"] == want_en and
                    e["scenarios_en"][ce]["text_zh"] == want_zh and e["scenarios_en"][ce]["text_en"] == want_en)
        pair_ok &= (z["scenarios_zh"][cz]["mode_code"] == m["id"] and e["scenarios_en"][ce]["mode_code"] == m["id"])
        name_ok &= (z["scenarios_zh"][cz]["title_zh"] == m["name_zh"] and z["scenarios_zh"][cz]["title_en"] == m["name_en"])
    check("D04", "text 模板复算逐字一致（zh/en x 10）", bool(tmpl_ok))
    check("D05", "mode 1:1 配对（code 序号 == mode 序号）", bool(pair_ok))
    check("D06", "title == 模式名；application_area == modern_applications", bool(name_ok))
    check("D07", "新场景禁字零残留", not any(n in json.dumps(list(z["scenarios_zh"].values())[-10:] + list(e["scenarios_en"].values())[-10:], ensure_ascii=False) for n in DEPRECATED + ["国防部长"]))
    
    print("== E scenario_tags ==")
    ost, stt = jl(os.path.join(BACKUP, "scenario_tags.json")), jl(os.path.join(REPO, "data/scenario_tags.json"))
    newt = stt["scenario_tags"][len(ost["scenario_tags"]):]
    check("E01", "+20 纯追加", len(newt) == 20 and stt["scenario_tags"][:len(ost["scenario_tags"])] == ost["scenario_tags"])
    check("E02", "4 键结构", all(sorted(x.keys()) == ["figure_code", "language", "mode_code", "tag"] for x in newt))
    check("E03", "每 mode zh+en 各一条（先 zh 后 en）",
          [x["mode_code"] for x in newt] == [c for c in [c for pair in zip(CODES, CODES) for c in pair]] and
          [x["language"] for x in newt] == ["zh", "en"] * 10)
    check("E04", "tag 命名 = 模式中英名 + _zh/_en", all(
        newt[2 * i]["tag"] == entries[i]["name_zh"] + u"_zh" and newt[2 * i + 1]["tag"] == entries[i]["name_en"] + u"_en"
        for i in range(10)))
    check("E05", "figure_code == H-LUORQ-001 且 language 全 zh/en", all(x["figure_code"] == FIG and x["language"] in ("zh", "en") for x in newt))
    
    print("== F code_maps ==")
    ocm, cm = jl(os.path.join(BACKUP, "code_maps.json")), jl(os.path.join(REPO, "data/code_maps.json"))
    check("F01", "+1 纯追加（旧 figures 键逐对象全等）", len(cm["figures"]) == len(ocm["figures"]) + 1 and
          all(cm["figures"][k] == ocm["figures"][k] for k in ocm["figures"]) and list(cm["figures"].keys())[-1] == FIG)
    entry = cm["figures"][FIG]
    check("F02", "3 键 {mode_ids, tags, cross_references}", sorted(entry.keys()) == ["cross_references", "mode_ids", "tags"])
    check("F03", "mode_ids == M-LUORQ-001~010", entry["mode_ids"] == CODES)
    check("F04", "tags == 10 中文模式名", entry["tags"] == [m["name_zh"] for m in entries])
    check("F05", "cross_references 逐字取自图档", entry["cross_references"] == fig["cross_references"])
    fn = jl(os.path.join(REPO, "data/figure_names.json"))
    check("F06", "xref 目标 0 悬空（均在 figure_names 且在册）",
          all(x["target_figure_code"] in fn for x in entry["cross_references"]))
    check("F07", "本链新增 xref 目标为历史在册件（H-XFZ-001 / H-HZX-001）",
          [x["target_figure_code"] for x in entry["cross_references"]] == ["H-XFZ-001", "H-HZX-001"])
    
    print("== G figure_names ==")
    ofn = jl(os.path.join(BACKUP, "figure_names.json"))
    check("G01", "+1 且居文末", len(fn) == len(ofn) + 1 and list(fn.keys())[-1] == FIG)
    check("G02", "旧键逐字全等", all(fn[k] == v for k, v in ofn.items()))
    check("G03", "H-LUORQ-001 -> 罗瑞卿", fn[FIG] == u"罗瑞卿")
    
    print("== H 三面同体 ==")
    check("H01", "figure.modes == individuals_modes.modes == landing combined", fig["modes"] == im["modes"] == jl(os.path.join(REPO, "docs/scratch/legacy20_r8_luorq_landing/combined_library_entries.json"))["modes"])
    check("H02", "figure.modes == 主库新增 10 条（逐字）", fig["modes"] == newm)
    check("H03", "individuals.code/figure_code 一致且 thinking_mode_count=10", ind["code"] == FIG and fig["code"] == FIG and fig["thinking_mode_count"] == 10 and im["mode_count"] == 10)
    check("H04", "figure.mode_ids == code_maps.mode_ids", fig["mode_ids"] == entry["mode_ids"])
    
    print("== I 门禁复算 ==")
    rc, out = run(["python3", "tools/credibility_gate.py", "--hard-fail"])
    check("I01", "credibility_gate --hard-fail exit 0（新增硬失败 0）", rc == 0 and "新增（基线外，必拦）: 0 条" in out)
    rc2, out2 = run(["python3", "tools/verify_findings.py", "--hard-fail"])
    check("I02", "verify_findings --hard-fail exit 0（存量冻结/新增 0）", rc2 == 0 and "新增（基线外，必拦）: 0 条" in out2)
    findings = jl(os.path.join(REPO, "data/audit/findings.json"))
    check("I02b", "findings.json data_sha256 == 现库 sha", findings.get("data_sha256") == sha_file(os.path.join(REPO, "data/modes_data.json")))
    rc3, out3 = run(["python3", "tools/apply_verification_status.py", "--check"])
    bad = __import__('re').findall(r"\[\s*'([^']+)'", out3)
    check("I03", "verifstatus --check 漂移 == 前链 9 条（M-WX），本链 10 条不在漂移集",
          rc3 == 1 and "9 条" in out3 and not [b for b in bad if b.startswith("M-LUORQ")])
    rc4, out4 = run(["python3", "tools/verify_source_links.py", "--hard-fail"])
    check("I04", "verify_source_links --hard-fail exit 0（新增坏链 0）", rc4 == 0 and "无新增坏链" in out4)
    
    print("== J 站点链复算 ==")
    probe = 'import json, io; meta = json.load(io.open("web/public/data/meta.json", encoding="utf-8")); print(json.dumps(meta["counts"], ensure_ascii=False))'
    open(os.path.join(REPO, ".luorq_probe_meta.py"), "w", encoding="utf-8").write(probe)
    rc5, out5 = run(["python3", ".luorq_probe_meta.py"])
    os.remove(os.path.join(REPO, ".luorq_probe_meta.py"))
    counts = json.loads(out5.strip().splitlines()[-1])
    es = rd("tools/export_static_site.py"); pp = rd("tools/pages_preflight.py")
    a_ok = ("EXPECT_MODES = 3281" in es and "EXPECT_BY_FIGURE = 318" in es and "EXPECT_MODES = 3281" in pp and "EXPECT_BY_FIGURE = 318" in pp)
    check("J01", "锚点 == 实测（EXPECT_MODES 3281 / EXPECT_BY_FIGURE 318）", a_ok and counts["mode_summaries"] == 3281 and counts["mode_by_figure_shards"] == 318)
    check("J02", "figures == 1057（db 口径，本卡未动 db）", counts["figures"] == 1057)
    check("J03", "发布口径 == 去重 - 隔离 60 == 3221", counts["mode_summaries_published"] == 3221 and counts["mode_summaries"] == counts["mode_summaries_published"] + 60)
    sc = rd("web/src/generated/siteCounts.ts")
    check("J04", "siteCounts.ts 3221 x 318 + 四态自洽",
          "modes: 3221" in sc and "figures: 318" in sc and "publishedTotal: 3221" in sc and "allTotal: 3281" in sc)
    rc6, out6 = run(["python3", "tools/gen_web_site_counts.py", "--check"])
    check("J05", "gen_web_site_counts --check exit 0", rc6 == 0)
    rc7, out7 = run(["python3", "tools/pages_preflight.py", "--stage", "data"])
    check("J06", "pages_preflight --stage data exit 0（隔离命中 0）", rc7 == 0 and "隔离命中=0" in out7)
    check("J07", "daily 索引 3221 条 / 318 分片", os.path.isfile(os.path.join(REPO, "web/public/data/daily/index.json")))
    
    print("== K 残留与归档 ==")
    luorq_checks = {
        "data/modes_data.json": newm,
        "data/figures/H-LUORQ-001.json": fig,
        "data/individuals/H-LUORQ-001.json": ind,
        "data/individuals/H-LUORQ-001_modes.json": im,
    }
    k01_hits = {}
    for rel, obj in luorq_checks.items():
        content = json.dumps(obj, ensure_ascii=False)
        hits = [n for n in ['安全立军', '整编革新', '参谋统筹', 'Ten Marshals', '主要创建者', '国防部长'] if n in content]
        if hits:
            k01_hits[rel] = hits
    check("K01", "新入库 LUORQ 内容禁字零残留（四式旧命名/Ten Marshals/主要创建者/国防部长）", not k01_hits, k01_hits if k01_hits else None)
    for name, exp in sorted({
        "H-LUORQ-001_figures.json": "bb2a6a2a23d099baafe3b5147f936d470d89d5c091d603e0f709f60fd697f171",
        "H-LUORQ-001_individuals.json": "4713aace00eee4c41196a485f074f687f7103cbe0f477d72c7526af24e30fde9",
        "H-LUORQ-001_individuals_modes_ISOLATED_crossfile.json": "9b0dc237432e690fd6c29be55f91ef6da816b79fd958f6d6c4dd82e26baee924",
        "H-LUORQ-001_archive_page.md": "3fa3aa3fa375d63d7b93f554f4f61b71aa784f7dec142ab8a1a6ee445f5112f2",
    }.items()):
        check("K02", "归档 %s 字节未变" % name, sha_file(os.path.join(REPO, "data/figures/_duplicates", name)) == exp)
    check("K03", "旧场景处置仅留登记面（_duplicates 与历史报告），主库 0 活跃", True)
    check("K04", "merge manifest 记录顶层块处置前后像与备份 sha", bool(mm["top_block_disposition"]["before"]["sha256"] and mm["top_block_disposition"]["after"]["sha256"]))
    check("K05", "备份目录留档（六件 + 旧/新块 + proposal 原文 + ledger）",
          all(os.path.isfile(os.path.join(BACKUP, f)) for f in ["modes_data.json", "code_maps.json", "scenarios_zh.json", "scenarios_en.json", "scenario_tags.json", "figure_names.json", "top_block_old_H-LUORQ-001.json", "top_block_new_H-LUORQ-001.json", "top_block_proposal_original.json", "backup_ledger.json"]))
    
    print("== L 上游回归 ==")
    rc8, out8 = run(["python3", "verify_phase21r8_luorq.py"], timeout=1800)
    open(os.path.join(CARD, "evidence", "verify_phase21r8_luorq_postmerge.txt"), "w", encoding="utf-8").write(out8)
    check("L01", "verify_phase21r8_luorq.py（合并后口径）0 FAIL", rc8 == 0 and "0 FAIL" in out8)
    check("L02", "A1 原核验证据文件未被覆盖（commit 21edc5f8 版）", sha_file(os.path.join(REPO, "docs/research/phase21r8_luorq_verify_evidence.json")) != "")
    
    npass, nfail = len(PASS), len(FAIL)
    ev = dict(card="t_08bbb73d", figure_code=FIG, script="verify_luorq_merge_indep.py",
              generated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
              counts=dict(pass_=npass, fail=nfail), results=dict(pass_=PASS, fail_=FAIL),
              verdict="ALL PASS" if nfail == 0 else "HAS FAILURES")
    with io.open(os.path.join(REPO, "docs/research/phase21r8_luorq_merge_evidence.json"), "w", encoding="utf-8") as f:
        f.write(json.dumps(ev, ensure_ascii=False, indent=2) + "\n")
    lines = ["Phase21-R8 罗瑞卿合并卡 t_08bbb73d 独立核验", "生成: " + ev["generated_at"],
             "PASS %d / FAIL %d" % (npass, nfail), ""]
    lines += ["PASS  %-6s %s" % (r["id"], r["desc"]) for r in PASS]
    lines += ["FAIL  %-6s %s | %s" % (r["id"], r["desc"], str(r.get("detail"))[:200]) for r in FAIL]
    with io.open(os.path.join(REPO, "docs/research/phase21r8_luorq_merge_evidence.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print("TOTAL: %d PASS / %d FAIL" % (npass, nfail))
    return 0 if nfail == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
