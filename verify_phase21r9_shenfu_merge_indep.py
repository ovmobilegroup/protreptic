#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""verify_phase21r9_shenfu_merge_indep.py - Phase21-R9 沈复合并卡（t_a7d233f0）独立核验

不信任合并卡自述：全部判据重回原始文件取证（备份前像 / 落盘包 / 主库现值 / 站点产物 / git 对象）。
分组：
  A 输入与备份完整性（前像/后像 sha、备份 6+1 件、ledger）
  B modes_data 纯追加与顶层块（逐字等于 A1 entries；其余条目零改动；total == len(modes)）
  C 场景 zh/en（10+10；模板复算；application_area 逐字等于 modern_applications_*）
  D scenario_tags（+20；字段/顺序/载体）
  E code_maps 与 figure_names（+1；mode_ids/tags/xref 口径；xref 0 悬空）
  F 并集护栏与残留（M-AZJ 保留；C-SHF/M-SHF 出现面白名单；归档三件字节未变）
  G 站点链复算（meta.json / siteCounts.ts / 锚点 / daily / manifest）
  H 门禁与四态（credibility/findings/verifstatus 复跑结论；四态求和自洽）
  I 上游回归（合并后口径复跑证据 74/0）

用法：python3 verify_phase21r9_shenfu_merge_indep.py [--json <out>]
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
import subprocess
import sys

REPO = os.path.dirname(os.path.abspath(__file__))
LANDING = os.path.join(REPO, "docs/scratch/legacy20_r9_shenfu_landing")
FIG = "H-SHF-001"
CODES = ["M-SHF-%03d" % i for i in range(1, 11)]
SCODES = ["C-SHF-%03d" % i for i in range(1, 11)]
SCODES_E = ["C-SHF-%03dE" % i for i in range(1, 11)]
KEY23 = ["schema_version", "code", "name_zh", "name_en", "era", "historical_domains", "domains", "core_modes",
         "gender", "ethnicity", "nationality", "civilization_sphere", "time_period_standardized", "primary_language",
         "intellectual_tradition", "unique_thinking_zh", "unique_thinking_en", "mode_evidence", "key_texts",
         "key_concepts", "intellectual_lineage", "legacy_assessment", "scholarly_value"]
RESULTS = []


def check(cid, grp, desc, ok, detail=""):
    RESULTS.append(dict(id=cid, group=grp, desc=desc, status="PASS" if ok else "FAIL", detail=str(detail)[:400]))
    print("%s  %-4s %s%s" % ("PASS" if ok else "FAIL", cid, desc, (" | " + str(detail)[:200]) if not ok else ""))


def jl(p):
    with io.open(p, encoding="utf-8") as f:
        return json.load(f)


def sha_file(p):
    with io.open(p, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", default=os.path.join(REPO, "docs/research/phase21r9_shenfu_merge_verify_indep.json"))
    args = ap.parse_args()

    man = jl(os.path.join(REPO, "data/audit/phase21r9_shenfu_merge_manifest.json"))
    entries = jl(os.path.join(LANDING, "modes_library_entries.json"))
    fig = jl(os.path.join(REPO, "data/figures/%s.json" % FIG))
    top = jl(os.path.join(LANDING, "top_block_proposal.json"))["proposal"]
    bdir = os.path.join(REPO, man["backup_dir"])

    # ---------- A 输入与备份完整性 ----------
    check("A01", "input", u"备份目录存在且 ledger 可解析", os.path.isdir(bdir) and
          jl(os.path.join(bdir, "backup_ledger.json"))["figure_code"] == FIG)
    led = jl(os.path.join(bdir, "backup_ledger.json"))
    six = ["modes_data.json", "code_maps.json", "figure_names.json",
           "scenarios_zh.json", "scenarios_en.json", "scenario_tags.json"]
    led_ok = all(os.path.isfile(os.path.join(bdir, s)) for s in six)
    check("A02", "input", u"备份六件齐备（六件 before 全量）", led_ok)
    pre = {}
    for rel, v in man["inputs"].items():
        p = os.path.join(bdir, os.path.basename(rel))
        pre[rel] = sha_file(p) if os.path.isfile(p) else ""
    check("A03", "input", u"备份件 sha256 == manifest.inputs", all(pre[rel] == v["sha256"] for rel, v in man["inputs"].items()),
          {k: (pre[k][:12], man["inputs"][k]["sha256"][:12]) for k in pre if pre[k] != man["inputs"][k]["sha256"]})
    for rel, v in man["after"].items():
        check("A04", "input", u"主库现值 sha256 == manifest.after [%s]" % os.path.basename(rel),
              sha_file(os.path.join(REPO, rel)) == v["sha256"], rel)
    check("A05", "input", u"落盘包 entries == 10 且码序 M-SHF-001~010",
          [e["mode_code"] for e in entries] == CODES)

    # ---------- B modes_data ----------
    md = jl(os.path.join(REPO, "data/modes_data.json"))
    md0 = jl(os.path.join(bdir, "modes_data.json"))
    check("B01", "modes", u"modes 数组 == 前像 + 10（纯追加，前列零改动）",
          md["modes"][:len(md0["modes"])] == md0["modes"] and len(md["modes"]) == len(md0["modes"]) + 10)
    check("B02", "modes", u"追加段逐字等于 A1 entries", md["modes"][-10:] == entries)
    check("B03", "modes", u"顶层块 H-SHF-001 == 提案逐字（23 键）",
          FIG in md and md[FIG] == top and list(md[FIG].keys()) == KEY23)
    # 顶层其余键：前像 + H-SHF-001，且 total 随动
    k_old = [k for k in md0 if k != "total"]
    k_new = [k for k in md if k != "total"]
    added = [k for k in k_new if k not in k_old]
    removed = [k for k in k_old if k not in k_new]
    check("B04", "modes", u"顶层键集合 == 前像 + H-SHF-001（零删）", added == [FIG] and not removed, {"added": added, "removed": removed})
    # 'modes' 与 'total' 由 B01/B06 另判；此处查其余顶层键（含各图块）逐字未动
    keys_cmp = [k for k in k_old if k in md and k != "modes"]
    others_ok = all(md[k] == md0[k] for k in keys_cmp)
    check("B05", "modes", u"除新增块/modes/total 外，其余顶层键逐字未动",
          others_ok, [k for k in keys_cmp if md[k] != md0[k]])
    check("B06", "modes", u"total == len(modes)（R5 裁定口径）", md["total"] == len(md["modes"]) == 3311,
          (md.get("total"), len(md["modes"])))
    codes = [m.get("mode_code") for m in md["modes"]]
    check("B07", "modes", u"全库 0 重复码（M-SHF 各 1 次）",
          all(codes.count(c) == 1 for c in CODES),
          {c: codes.count(c) for c in CODES})
    check("B08", "modes", u"追加条目 figure_code/figure_name/legacy_mode_id/verification 口径",
          all(m["figure_code"] == FIG and m["figure_name"] == u"沈复" and m["legacy_mode_id"] == ""
              and m["verification"]["status"] == "pending" for m in md["modes"][-10:]))
    check("B09", "modes", u"顶层块 core_modes == M-SHF-001~010（与数组追加一致）",
          md[FIG]["core_modes"] == CODES)

    # ---------- C 场景 ----------
    sz = jl(os.path.join(REPO, "data/scenarios_zh.json"))
    se = jl(os.path.join(REPO, "data/scenarios_en.json"))
    sz0 = jl(os.path.join(bdir, "scenarios_zh.json"))
    se0 = jl(os.path.join(bdir, "scenarios_en.json"))
    inn, ien = sz["scenarios_zh"], se["scenarios_en"]
    inn0, ien0 = sz0["scenarios_zh"], se0["scenarios_en"]
    check("C01", "scenario", u"zh 内层 == 前像 + 10（纯追加）",
          [k for k in inn if k not in inn0] == SCODES and all(inn[k] == inn0[k] for k in inn0))
    check("C02", "scenario", u"en 内层 == 前像 + 10（纯追加，E 后缀）",
          [k for k in ien if k not in ien0] == SCODES_E and all(ien[k] == ien0[k] for k in ien0))
    bad_tpl = []
    for i, e in enumerate(entries):
        z = inn[SCODES[i]]
        wants = dict(code=SCODES[i], mode_code=e["mode_code"], title_zh=e["name_zh"], title_en=e["name_en"],
                     text_zh=e["name_zh"] + u"的当代应用场景：" + u"；".join(e["modern_applications_zh"]) + u"。",
                     text_en=u"Contemporary applications of " + e["name_en"] + u": " + u"; ".join(e["modern_applications_en"]) + u".",
                     application_area_zh=e["modern_applications_zh"], application_area_en=e["modern_applications_en"])
        if z != wants:
            bad_tpl.append(SCODES[i])
    check("C03", "scenario", u"zh 10 条 8 键结构 + 模板复算逐字", not bad_tpl, bad_tpl)
    bad_en = []
    for i, e in enumerate(entries):
        w = inn[SCODES[i]].copy()
        w["code"] = SCODES_E[i]
        if ien[SCODES_E[i]] != w:
            bad_en.append(SCODES_E[i])
    check("C04", "scenario", u"en 10 条 == zh 同体（仅 code 换 E 后缀）", not bad_en, bad_en)
    check("C05", "scenario", u"场景引用模式码均为 M-SHF-*（0 外部码）",
          all(inn[k]["mode_code"] in CODES for k in SCODES))

    # ---------- D scenario_tags ----------
    st = jl(os.path.join(REPO, "data/scenario_tags.json"))
    st0 = jl(os.path.join(bdir, "scenario_tags.json"))
    tl, tl0 = st["scenario_tags"], st0["scenario_tags"]
    check("D01", "tags", u"scenario_tags == 前像 + 20（纯追加）",
          tl[:len(tl0)] == tl0 and len(tl) == len(tl0) + 20)
    new20 = tl[-20:]
    want20 = []
    for e in entries:
        want20.append({"mode_code": e["mode_code"], "tag": e["name_zh"] + u"_zh", "figure_code": FIG, "language": "zh"})
        want20.append({"mode_code": e["mode_code"], "tag": e["name_en"] + u"_en", "figure_code": FIG, "language": "en"})
    check("D02", "tags", u"追加 20 条逐字（先 zh 后 en；4 键）", new20 == want20)
    check("D03", "tags", u"载体键集/值类型 == 既有先例（mode_code/tag/figure_code/language）",
          all(set(t.keys()) == {"mode_code", "tag", "figure_code", "language"} for t in new20))
    check("D04", "tags", u"tags 载体不含 C-SHF 场景码（tag=模式名口径）",
          not any("C-SHF" in json.dumps(t, ensure_ascii=False) for t in new20))

    # ---------- E code_maps / figure_names ----------
    cm = jl(os.path.join(REPO, "data/code_maps.json"))
    cm0 = jl(os.path.join(bdir, "code_maps.json"))
    figs, figs0 = cm["figures"], cm0["figures"]
    check("E01", "codemaps", u"figures == 前像 + 1（其余逐字未动）",
          {k: v for k, v in figs.items() if k != FIG} == figs0 and FIG in figs)
    ent = figs[FIG]
    check("E02", "codemaps", u"mode_ids == M-SHF-001~010", ent["mode_ids"] == CODES)
    check("E03", "codemaps", u"tags == 10 条模式名（name_zh，先例口径）", ent["tags"] == [e["name_zh"] for e in entries])
    check("E04", "codemaps", u"cross_references == 图档逐字（3 条）", ent["cross_references"] == fig["cross_references"])
    tgt = [x["target_figure_code"] for x in ent["cross_references"]]
    check("E05", "codemaps", u"xref 目标全部已注册（0 悬空）", all(t in figs for t in tgt), tgt)
    check("E06", "codemaps", u"code_maps 顶层键集未变（schema_version/figures）", set(cm.keys()) == set(cm0.keys()))
    fn = jl(os.path.join(REPO, "data/figure_names.json"))
    fn0 = jl(os.path.join(bdir, "figure_names.json"))
    check("F01", "names", u"figure_names == 前像 + 1（H-SHF-001 -> 沈复）",
          {k: v for k, v in fn.items() if k != FIG} == fn0 and fn[FIG] == u"沈复")

    # ---------- F 并集护栏与残留 ----------
    azj = [m.get("mode_code") for m in md["modes"] if str(m.get("mode_code", "")).startswith("M-AZJ")]
    check("F02", "union", u"并集护栏：M-AZJ-001~010 在位（兄弟卡 t_ce457734 未受损）",
          azj == ["M-AZJ-%03d" % i for i in range(1, 11)], azj[:3])
    azj_fig = jl(os.path.join(REPO, "data/figures/H-AZJ-001.json"))
    check("F03", "union", u"并集护栏：H-AZJ-001 图档/图名在位", "H-AZJ-001" in figs and fn.get("H-AZJ-001") == u"安子介")
    arc = jl(os.path.join(REPO, "data/audit/phase21r9_shenfu_landing_manifest.json"))["archive_untouched"]
    mis_arc = [n for n, v in arc.items() if sha_file(os.path.join(REPO, "data/figures/_duplicates", n)) != v]
    check("F04", "union", u"归档三件（H-HAN-001 系列）字节未变", not mis_arc, mis_arc)
    # M-SHF/C-SHF/H-SHF 出现面：主库六件 + 本链产物（快速抽查：git tracked+untracked 小文件扫描）
    hits = []
    out = subprocess.check_output(["git", "-C", REPO, "ls-files"], text=True).split("\n")
    out += subprocess.check_output(["git", "-C", REPO, "ls-files", "--others", "--exclude-standard"], text=True).split("\n")
    allowed_exact = set([
        "data/modes_data.json", "data/code_maps.json", "data/figure_names.json", "data/scenarios_zh.json",
        "data/scenarios_en.json", "data/scenario_tags.json", "data/audit/phase21r9_shenfu_merge_manifest.json",
        "data/audit/phase21r9_shenfu_landing_manifest.json", "docs/research/phase21r9_shenfu_merge_report.md",
        "docs/research/phase21r9_shenfu_merge_evidence.json", "docs/research/phase21r9_shenfu_merge_evidence.txt",
        "docs/research/phase21r9_shenfu_verify_evidence_merged.json", "docs/research/phase21r9_shenfu_landing_evidence.json",
        "docs/research/phase21r9_shenfu_rebuild_report.md", "docs/research/phase21r9_shenfu_verify_evidence.json",
        "docs/research/phase21r9_shenfu_gate.txt", "verify_phase21r9_shenfu.py", "verify_phase21r9_shenfu_merge_indep.py",
        "tools/merge_phase21r9_shenfu.py", "tools/export_static_site.py", "tools/pages_preflight.py",
        "verify_phase21r9_azj.py", "verify_azj_merge_indep.py",  # 兄弟卡（t_ce457734）核验脚本含本卡足迹引用
        "data/figures/H-SHF-001.json", "data/individuals/H-SHF-001.json",
        "data/individuals/H-SHF-001_modes.json", "tools/build_phase21r9_shenfu.py",
    ])
    allowed_prefix = ("docs/scratch/legacy20_r9_shenfu_landing/", "docs/scratch/phase21r9_shenfu/",
                      "docs/research/phase21r9_shenfu_", "data/backup_merge_H-SHF-001_", "data/audit/phase21r9_shenfu_",
                      # 兄弟卡 t_ce457734（安子介 H-AZJ-001，在制）链产物：其并集说明/证据会引用本卡图码与模式码，
                      # 属链式正常占用（前 10 后 10 由 F02/F03 断言其未受损）
                      "docs/research/phase21r9_azj_", "docs/research/phase21r9_anzijie_",
                      "data/audit/phase21r9_azj_", "docs/scratch/legacy20_r9_azj_",
                      "docs/scratch/phase21r9_anzijie/", "docs/scratch/phase21r9_azj_", "verify_azj_")
    for rel in sorted(set(out)):
        if not rel or rel.startswith(".git") or "/node_modules/" in rel or rel.startswith("node_modules/"):
            continue
        fp = os.path.join(REPO, rel)
        if not os.path.isfile(fp) or os.path.getsize(fp) > 3000000:
            continue
        if rel in allowed_exact or rel.startswith(allowed_prefix):
            continue
        try:
            s = io.open(fp, encoding="utf-8", errors="ignore").read()
        except Exception:
            continue
        if "M-SHF" in s or "C-SHF" in s or "H-SHF-001" in s:
            hits.append(rel)
    check("F05", "union", u"残留面扫描：非白名单文件零 M-SHF/C-SHF/H-SHF 命中", not hits, hits[:6])

    # ---------- G 站点链 ----------
    meta = jl(os.path.join(REPO, "web/public/data/meta.json"))["counts"]
    check("G01", "site", u"meta.json：dedup 3301 / published 3241 / by-figure 320 / figures 1027 / 隔离 60",
          meta["modes_deduped"] == 3301 and meta["mode_summaries_published"] == 3241
          and meta["mode_by_figure_shards"] == 320 and meta["figures"] == 1027 and meta["modes_quarantined"] == 60,
          {k: meta.get(k) for k in ["modes_deduped", "mode_summaries_published", "mode_by_figure_shards", "figures"]})
    check("G02", "site", u"published = dedup - 隔离（3241 = 3301 - 60）",
          meta["mode_summaries_published"] == meta["modes_deduped"] - meta["modes_quarantined"])
    sc = io.open(os.path.join(REPO, "web/src/generated/siteCounts.ts"), encoding="utf-8").read()
    check("G03", "site", u"siteCounts.ts 3241x320 与 meta 同值",
          "modes: 3241" in sc and "figures: 320" in sc and "sourceTotal: 3301" in sc)
    for f, pat in [("tools/export_static_site.py", "EXPECT_MODES = 3301"),
                   ("tools/export_static_site.py", "EXPECT_BY_FIGURE = 320"),
                   ("tools/pages_preflight.py", "EXPECT_MODES = 3301"),
                   ("tools/pages_preflight.py", "EXPECT_BY_FIGURE = 320")]:
        check("G04", "site", u"锚点 %s: %s" % (f.split("/")[-1], pat),
              pat in io.open(os.path.join(REPO, f), encoding="utf-8").read())
    dj = jl(os.path.join(REPO, "web/public/data/daily/index.json"))
    check("G05", "site", u"daily index total == 3241（发布口径）", dj.get("total") == 3241, dj.get("total"))
    sd = jl(os.path.join(REPO, "docs/architecture/static_data_manifest.json"))["counts"]
    check("G06", "site", u"static_data_manifest：mode_summaries 3301 / published 3241 / by_figure 320",
          sd["mode_summaries"] == 3301 and sd["mode_summaries_published"] == 3241 and sd["mode_by_figure_shards"] == 320)
    # 场景/标签镜像面：web/public/data 内不含 C-SHF 泄漏到隔离面？(by-figure 分片应含 M-SHF)
    bf = os.path.join(REPO, "web/public/data/modes/by-figure/%s.json" % FIG)
    check("G07", "site", u"by-figure 分片 H-SHF-001.json 存在且含 10 条 M-SHF",
          os.path.isfile(bf) and sum(1 for m in jl(bf)["modes"] if str(m.get("mode_code", "")).startswith("M-SHF")) == 10)

    # ---------- H 门禁与四态 ----------
    fd = jl(os.path.join(REPO, "data/audit/findings.json"))
    am = fd["audit_meta"]
    check("H01", "gate", u"findings.audit_meta 随库刷新（sha/计数与现值一致）",
          am["modes_file_sha256"] == sha_file(os.path.join(REPO, "data/modes_data.json"))
          and am["top_level_modes_entries"] == 3311 and am["distinct_mode_codes"] == 3301,
          (am["modes_file_sha256"][:12], am["top_level_modes_entries"], am["distinct_mode_codes"]))
    v = meta["verification"]
    check("H02", "gate", u"四态求和自洽：公开 3241 + 隔离 60 == 全库 3301",
          v["published_total"] == 3241 and sum(v["published"][k] for k in v["published"]) == 3241
          and v["all_total"] == 3301 and sum(v["all"][k] for k in v["all"]) == 3301
          and v["published_total"] + v["quarantined_total"] == v["all_total"])
    check("H03", "gate", u"新增 10 条全 pending（未回填核验状态）",
          v["all"]["pending"] - 1939 == 10 if False else v["all"]["pending"] == 1949, v["all"]["pending"])

    # ---------- I 上游回归 ----------
    evp = os.path.join(REPO, "docs/research/phase21r9_shenfu_verify_evidence_merged.json")
    ev = jl(evp) if os.path.isfile(evp) else {}
    check("I01", "upstream", u"上游脚本合并后口径复跑 74 PASS / 0 FAIL",
          ev.get("counts", {}).get("fail") == 0 and ev.get("counts", {}).get("pass_") == 74,
          ev.get("counts"))

    npass = len([r for r in RESULTS if r["status"] == "PASS"])
    nfail = len([r for r in RESULTS if r["status"] == "FAIL"])
    print("TOTAL: %d PASS / %d FAIL" % (npass, nfail))
    with io.open(args.json, "w", encoding="utf-8") as f:
        json.dump(dict(card="t_a7d233f0", figure_code=FIG, generated_at=__import__("time").strftime("%Y-%m-%d %H:%M:%S"),
                       script="verify_phase21r9_shenfu_merge_indep.py", counts=dict(pass_=npass, fail=nfail),
                       results=RESULTS, verdict="ALL PASS" if nfail == 0 else "HAS FAILURES"), f,
                  ensure_ascii=False, indent=1)
        f.write(u"\n")
    return 0 if nfail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
