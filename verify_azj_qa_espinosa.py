#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""verify_azj_qa_espinosa.py — Phase21-R9 安子介(H-AZJ-001) 全链 独立 QA（卡 t_02007da8 · espinosa）

验收对象：AZJ-1 素材包(t_1aa06d0c) → AZJ-2 重建落盘(t_58ebf9c2) → AZJ-3 合并入主库(t_ce457734) 全链产物。
方法（不采信任何卡面自述）：直读 git 对象 / 磁盘字节 / 远端 ref / raw 实测；AZJ 合并中间态以
「before 备份 + entries 字节级复现 == 卡面 after sha」反证；figure 层逐条核对内容/来源/编号。
产出：docs/research/phase21r9_azj_qa_evidence.json/.txt；FAIL 时 exit 1。
"""
import hashlib, io, json, os, re, subprocess, sys

REPO = "/opt/data/workspace/Protreptic"
PB = "/opt/data/release/Protreptic-publish"
SC = "/opt/data/profiles/espinosa/cache/scratch/azj_qa"
REBUILD = os.environ.get("AZJQA_REBUILD", SC + "/site_rebuild_r1")
RAWLOG = SC + "/raw_probe_log.txt"
R8WS = "/opt/data/profiles/espinosa/cache/scratch/azjqa/ws_hits.json"

FIG = "H-AZJ-001"
FNAME = "安子介"
CODES = ["M-AZJ-%03d" % i for i in range(1, 11)]
PACKJ = REPO + "/docs/research/phase21r9_anzijie_sourcing_report.json"
PACKM = REPO + "/docs/research/phase21r9_anzijie_sourcing_report.md"
LAND = REPO + "/docs/scratch/legacy20_r9_azj_landing"
LMAN = REPO + "/data/audit/phase21r9_azj_landing_manifest.json"
MMAN = REPO + "/data/audit/phase21r9_azj_merge_manifest.json"
SMAN = REPO + "/data/audit/phase21r9_shenfu_merge_manifest.json"
BACK = REPO + "/data/backup_merge_H-AZJ-001_20260924_092502"
LIB6 = ["data/modes_data.json", "data/code_maps.json", "data/figure_names.json",
        "data/scenarios_zh.json", "data/scenarios_en.json", "data/scenario_tags.json"]
LIB3W = LIB6[:3]
LIB3Z = LIB6[3:]
FORBIDDEN_OLD = [u'特区建设', u'摸着石头过河', u'安子介回忆录', u'深圳特区建设档案', u'对外开放政策',
                 u'经济特区', 'An Zijie', 'SEZ', 'Opening Up',
                 'M001', 'M002', 'M003', 'M004', 'M005', 'M006', 'M007', 'M008', 'M009', 'M010']
STD_CATEGORIES = [u'伦理修养', u'军事战略', u'医学养生', u'史学文献', u'哲学形而上', u'宗教修行', u'工程技术',
                  u'心理洞察', u'战略决策', u'探险发现', u'政治治理', u'教育传承', u'文艺审美', u'方法论通用',
                  u'科学方法', u'组织领导', u'经济商业', u'认识论逻辑']
PASS, FAIL, INFO = [], [], []

def check(tag, cond, msg, extra=None):
    rec = {"tag": tag, "status": "PASS" if cond else "FAIL", "msg": msg}
    if extra is not None:
        rec["extra"] = extra
    (PASS if cond else FAIL).append(rec)
    print(("  [PASS] " if cond else "  [FAIL] ") + tag + " " + msg + ("" if extra is None else " | " + json.dumps(extra, ensure_ascii=False)[:220]))
    return cond

def note(tag, msg, extra=None):
    rec = {"tag": tag, "status": "INFO", "msg": msg}
    if extra is not None:
        rec["extra"] = extra
    INFO.append(rec)
    print("  [INFO] " + tag + " " + msg + ("" if extra is None else " | " + json.dumps(extra, ensure_ascii=False)[:220]))

def rb(p):
    with open(p, "rb") as f:
        return f.read()

def sha(p):
    return hashlib.sha256(rb(p)).hexdigest()

def rj(p):
    with io.open(p, encoding="utf-8") as f:
        return json.load(f)

def rt(p):
    with io.open(p, encoding="utf-8") as f:
        return f.read()

def canon(o):
    return json.dumps(o, ensure_ascii=False, indent=2)

def git(args, cwd=REPO, binary=True):
    r = subprocess.run(["git"] + args, cwd=cwd, capture_output=True)
    if r.returncode != 0:
        raise RuntimeError("git %s rc=%d %s" % (" ".join(args), r.returncode, r.stderr.decode("utf-8", "replace")[:200]))
    return r.stdout if binary else r.stdout.decode("utf-8", "replace")

def git_blob(rev_path, cwd=REPO):
    return git(["show", rev_path], cwd=cwd)

def norm_ws(s):
    return re.sub(r"[\s\u3000\u200b\ufeff]+", "", s)

def norm_alnum(s):
    return re.sub(r"[^0-9A-Za-z\u4e00-\u9fff]+", "", s)

def f_code(e, idx):
    return (e.get("id") == CODES[idx] and e.get("mode_code") == CODES[idx]
            and e.get("priority") == idx + 1 and not e.get("legacy_mode_id")
            and e.get("figure_code") == FIG and e.get("figure_name") == FNAME and e.get("level") == u"核心")

def f_quote(e, pack_mode):
    return any(q.get("text") == e.get("key_quote_zh") for q in pack_mode.get("quotes", []))

def f_prefix(modes, backup_modes):
    return len(modes) >= len(backup_modes) and all(canon(a) == canon(b) for a, b in zip(modes[:len(backup_modes)], backup_modes))

def f_slice(modes, start, entries):
    return all(canon(a) == canon(b) for a, b in zip(modes[start:start + len(entries)], entries))

def f_block_pos(keys, backup_keys):
    cur = [k for k in keys if k not in ("H-AZJ-001", "H-SHF-001")]
    return (cur == list(backup_keys) and "H-AZJ-001" in keys and "H-SHF-001" in keys
            and keys.index("H-AZJ-001") == keys.index("H-SHF-001") - 1
            and keys.index("H-SHF-001") == keys.index("modes") - 1)

def f_figmodes(fig, codes):
    return fig.get("mode_ids") == codes and fig.get("thinking_mode_count") == len(codes)

def f_meta_counts(counts, recomputed):
    keys = ["figures", "mode_summaries", "mode_summaries_published", "modes_quarantined",
            "mode_by_figure_shards", "modes_raw", "modes_deduped", "modes_empty_mode_code_dropped"]
    return all(counts.get(k) == recomputed.get(k) for k in keys)

def f_verif_states(v, expected):
    return v.get("published") == expected["published"] and v.get("all") == expected["all"]


def main():
    print("=" * 78)
    print("Phase21-R9 安子介 H-AZJ-001 独立 QA（espinosa / t_02007da8）")
    print("=" * 78)
    pack = rj(PACKJ)
    pack_md = rt(PACKM)
    pm = dict((m["id"], m) for m in pack["modes"])
    wmap = dict((w["w"], w) for w in pack["witnesses"])
    wtxt = {}
    for w, d in wmap.items():
        wtxt[w] = rt(os.path.join(REPO, d["file"]))
    entries = rj(LAND + "/modes_library_entries.json")
    combined = rj(LAND + "/combined_library_entries.json")
    md = rj(REPO + "/data/modes_data.json")
    modes = md["modes"]
    cm = rj(REPO + "/data/code_maps.json")
    fn = rj(REPO + "/data/figure_names.json")
    fg = rj(REPO + "/data/figures/H-AZJ-001.json")
    fgm = rj(REPO + "/data/figures/H-AZJ-001_modes.json")
    ind = rj(REPO + "/data/individuals/H-AZJ-001.json")
    indm = rj(REPO + "/data/individuals/H-AZJ-001_modes.json")
    mm = rj(MMAN)
    lm = rj(LMAN)
    sm = rj(SMAN)
    bmd = rj(BACK + "/modes_data.json")
    bcm = rj(BACK + "/code_maps.json")
    bfn = rj(BACK + "/figure_names.json")
    bmodes = bmd["modes"]

    # ================= A 输入链（素材包/见证/落盘/数据件 · git 级） =================
    print("== A 输入链（素材包/见证/落盘包/数据件 == git 提交版本） ==")
    for rel in ["docs/research/phase21r9_anzijie_sourcing_report.json",
                "docs/research/phase21r9_anzijie_sourcing_report.md"]:
        last = git(["log", "-1", "--format=%H", "--", rel], binary=False).strip()
        check("A01", sha(REPO + "/" + rel) == hashlib.sha256(git_blob(last + ":" + rel)).hexdigest(),
              "素材包 %s == git(%s) blob（工作区=提交版本）" % (rel.split("/")[-1], last[:8]))
    check("A02", len(pack["witnesses"]) == 11, "见证登记 11 件")
    w_ok = 0
    for w, d in sorted(wmap.items()):
        p = os.path.join(REPO, d["file"])
        ok = os.path.isfile(p) and sha(p) == d["sha256"]
        last = git(["log", "-1", "--format=%H", "--", d["file"]], binary=False).strip()
        ok = ok and sha(p) == hashlib.sha256(git_blob(last + ":" + d["file"])).hexdigest()
        w_ok += 1 if ok else 0
    check("A03", w_ok == 11, "见证 11 件 sha256 == 素材包登记 且 == git blob（%d/11）" % w_ok)
    n_land = 0
    for rel, want in sorted(lm["deliverables"].items()):
        want_sha = want["sha256"] if isinstance(want, dict) else want
        last = git(["log", "-1", "--format=%H", "--", rel], binary=False).strip()
        ok = sha(REPO + "/" + rel) == want_sha and sha(REPO + "/" + rel) == hashlib.sha256(git_blob(last + ":" + rel)).hexdigest()
        n_land += 1 if ok else 0
    check("A04", n_land == len(lm["deliverables"]),
          "落盘包 %d 件 sha == landing manifest 且 == git blob（%d/%d）" % (len(lm["deliverables"]), n_land, len(lm["deliverables"])))
    check("A05", sha(REPO + "/data/figures/H-AZJ-001.json") == sha(LAND + "/figures/H-AZJ-001.json")
          and sha(REPO + "/data/individuals/H-AZJ-001_modes.json") == sha(LAND + "/individuals/H-AZJ-001_modes.json"),
          "数据件 == 落盘包副本（figure/individuals 面逐字节）")

    # ================= B 10 条逐条核对（内容/来源/编号） =================
    print("== B +10 条逐条核对（内容/来源/编号 vs figure/三面/素材包/见证） ==")
    idx0 = len(bmodes)
    b_ok = dict(list1=0, quote=0, wit=0, src=0, code=0, cat=0, name=0, keys=0, fbid=0, nonempty=0)
    catj_mism = []
    for i, e in enumerate(entries):
        b_ok["code"] += 1 if f_code(e, i) else 0
        same = (canon(e) == canon(fg["modes"][i]) == canon(fgm["modes"][i]) == canon(indm["modes"][i])
                == canon(combined["modes"][i]) and canon(modes[idx0 + i]) == canon(e))
        b_ok["list1"] += 1 if same else 0
        pn = pm[e["id"]]["name"]
        b_ok["name"] += 1 if (pn.split(u"：")[0] == e["name_zh"]) else 0
        mdm = re.search(u"### %s [^\n]*\n- 主题域：([^\n]+)" % re.escape(e["id"]), pack_md)
        md_ok = bool(mdm) and norm_ws(e["category_raw"]) == norm_ws(mdm.group(1))
        if e["category_raw"] != pm[e["id"]]["theme"]:
            catj_mism.append(e["id"])
        b_ok["cat"] += 1 if (e["category"] in STD_CATEGORIES and md_ok) else 0
        w = None
        if f_quote(e, pm[e["id"]]):
            b_ok["quote"] += 1
            qi = [q for q in pm[e["id"]]["quotes"] if q["text"] == e["key_quote_zh"]][0]
            w = qi["w"]
            hit = norm_ws(e["key_quote_zh"]) in norm_ws(wtxt[w]) or norm_alnum(e["key_quote_zh"]) in norm_alnum(wtxt[w])
            b_ok["wit"] += 1 if (w in wtxt and hit) else 0
        sc = e["source_chapter"]
        cited = set(re.findall(r"W\d\d", sc))
        ok_src = ("AZJ-1 素材包" in sc and e["mode_code"] in sc and bool(cited) and cited <= set(wmap)
                  and (w is None or w in cited))
        b_ok["src"] += 1 if ok_src else 0
        b_ok["keys"] += 1 if (set(e.keys()) == set(fg["modes"][0].keys()) and e["verification"].get("status") == "pending"
                              and not e.get("legacy_mode_id")) else 0
        b_ok["nonempty"] += 1 if (e["name_en"] and e["key_quote_en"] and e["definition_zh"] and e["definition_en"]
                                  and e["process_zh"] and e["representative_cases_zh"] and e["modern_applications_zh"]) else 0
        fb = [t for t in FORBIDDEN_OLD if t in canon(e)]
        b_ok["fbid"] += 1 if not fb else 0
    check("B01", b_ok["code"] == 10, "编号/顺序/归属：M-AZJ-001~010 顺序、priority 1..10、legacy 空、figure_code/名/level（%d/10）" % b_ok["code"])
    check("B02", b_ok["list1"] == 10, "内容同体：主库条目 == figure == fig_modes == individuals_modes == landing 两面（逐条有序，%d/10）" % b_ok["list1"])
    check("B03", b_ok["quote"] == 10 and b_ok["wit"] == 10, "来源-引文：key_quote_zh == 素材包 quotes 逐字（%d/10）且见证文本命中（%d/10）" % (b_ok["quote"], b_ok["wit"]))
    check("B04", b_ok["src"] == 10, "来源-指向：source_chapter 含「AZJ-1 素材包」+ 本条码 + 引文见证在内、所引编号均在册（%d/10）" % b_ok["src"])
    check("B05", b_ok["keys"] == 10, "条键面：键集与图档一致、verification pending、legacy 空（%d/10）" % b_ok["keys"])
    check("B06", b_ok["cat"] == 10, "类目：category ∈ 标准 18 类 且 category_raw == 素材包 §二 主题域行（md 为准、去空格）（%d/10）" % b_ok["cat"], {"json_theme_mismatch": catj_mism})
    note("B06n", "口径差：category_raw 与素材包 JSON theme 字段不一致 %d 项（素材包 md/json 内部差异；落库取 md 口径、与 category_mapping.tsv 一致）" % len(catj_mism), {"items": catj_mism})
    check("B07", b_ok["name"] == 10, "命名：name_zh == 素材包名主干（全名在 id_mapping.tsv）（%d/10）" % b_ok["name"])
    check("B08", b_ok["nonempty"] == 10, "内容非空：中英定义/流程/案例/现代应用 齐（%d/10）" % b_ok["nonempty"])
    check("B09", b_ok["fbid"] == 10, "禁用标记（19 项旧载荷）在本 10 条零出现（%d/10）" % b_ok["fbid"])
    blob = norm_alnum(pack_md + json.dumps(pack, ensure_ascii=False) + "".join(wtxt.values()))
    segs = []
    for e in entries:
        segs += re.findall(u"[「『]([^」』]+)[」』]", canon(e))
    miss = [s for s in set(segs) if norm_alnum(s) not in blob]
    check("B10", not miss, "「」/『』片段 %d 处（唯一 %d）全部可回溯素材包/见证" % (len(segs), len(set(segs))), {"miss": miss[:10]})
    allcodes = set(m.get("mode_code") for m in modes if m.get("mode_code"))
    azj_codes = sorted(m.get("mode_code") for m in modes if "AZJ" in str(m.get("mode_code", "")))
    rel_ok = all(all(str(t) in allcodes for t in (e.get("related_modes") or [])) for e in entries)
    check("B11", azj_codes == CODES and rel_ok, "全库 M-AZJ 恰 10 条且条目 related_modes 引用可解析", {"n": len(azj_codes), "rel_ok": rel_ok})

    # ================= C 图档/顶层块/注册面 =================
    print("== C 图档 figure / 顶层块 / 注册面 ==")
    check("C01", f_figmodes(fg, CODES) and fg.get("cross_references") == [] and len(fg.get("core_thoughts") or []) == 10
          and len(fg.get("tags") or []) >= 10 and FNAME in (fg.get("tags") or []),
          "figure：mode_ids/计数=10、core_thoughts 10、tags 非空且含本名、xref=[]")
    shared = ["figure_name", "figure_code", "birth_year", "death_year", "era", "nationality", "ethnicity", "school",
              "intellectual_tradition", "representative_works", "historical_significance", "core_thoughts",
              "famous_quote", "famous_quote_source", "influence", "tags", "cross_references", "meta",
              "related_figures", "mode_ids", "mode_ids_note", "caveats"]
    diff = [k for k in shared if fg.get(k) != ind.get(k)]
    check("C02", not diff, "figure 与 individuals 档案面同体（%d 共享键）" % len(shared), {"diff": diff[:8]})
    prop_wrap = rj(LAND + "/top_block_proposal.json")
    prop = prop_wrap["proposal"]
    check("C03", md.get(FIG) == prop and len(prop) == 23 and prop.get("core_modes") == CODES,
          "顶层块 H-AZJ-001 == top_block_proposal.proposal（23 键，core_modes 10）")
    check("C04", f_block_pos(list(md.keys()), list(bmd.keys())),
          "顶层块位次：backup 键序守恒、H-AZJ-001 于 H-SHF-001 前、modes 前（插入=块组末位）")
    check("C05", md.get("total") == len(modes) == 3311, "total 对齐 len(modes)=3311")
    cme = cm["figures"].get(FIG, {})
    check("C06", set(cme.keys()) == {"mode_ids", "tags", "cross_references"} and cme["mode_ids"] == CODES
          and cme["tags"] == [e["name_zh"] for e in entries] and cme["cross_references"] == [],
          "code_maps 条目：3 键 / mode_ids / tags=10 名 / xref=[]")
    same_others = [k for k in bcm["figures"] if cm["figures"].get(k) != bcm["figures"][k]]
    check("C07", not same_others and all(cm[k] == bcm[k] for k in bcm if k != "figures"),
          "code_maps 其余条目/顶层键零改动", {"changed": same_others[:5]})
    check("C08", fn.get(FIG) == FNAME and list(fn.keys()).index(FIG) == len(bfn)
          and all(fn.get(k) == bfn[k] for k in bfn),
          "figure_names：H-AZJ-001->安子介于追加位、其余零改动")
    n345 = canon(fg).count("H-AZJ-345")
    check("C09", n345 == 2 and "H-AZJ-345" not in canon(fg.get("modes", [])) and canon(md[FIG]).count("H-AZJ-345") == 0,
          "H-AZJ-345 于 figure 仅 2 处（meta/mode_ids_note 登记），条目/顶层块 0 复用", {"n": n345})

    # ================= D 合并链算术（before+entries → after 字节级复现） =================
    print("== D 合并链算术与纯追加（备份/复现/链式口径） ==")
    d_ok = 0
    for rel in LIB6:
        rel_b = os.path.basename(rel)
        ok = (sha(BACK + "/" + rel_b) == mm["before"][rel]["sha256"]
              and sha(BACK + "/" + rel_b) == hashlib.sha256(git_blob("5a657b81^:" + rel)).hexdigest())
        d_ok += 1 if ok else 0
    check("D01", d_ok == 6, "六件：backup == AZJ before == git 5a657b81^（%d/6）" % d_ok)
    d_cur = 0
    for rel in LIB6:
        d_cur += 1 if sha(REPO + "/" + rel) == hashlib.sha256(git_blob("HEAD:" + rel)).hexdigest() else 0
    check("D02", d_cur == 6, "六件：现行工作区 == git HEAD 提交版本（%d/6）" % d_cur)
    ok_after = 0
    for rel in LIB3W:
        ok_after += 1 if (sha(BACK + "/" + os.path.basename(rel)) == mm["before"][rel]["sha256"]
                          and sha(REPO + "/" + rel) == (sm["after"][rel]["sha256"] if isinstance(sm["after"][rel], dict) else sm["after"][rel])
                          and mm["before"][rel]["sha256"] != mm["after"][rel]["sha256"]) else 0
    for rel in LIB3Z:
        ok_after += 1 if (mm["before"][rel]["sha256"] == mm["after"][rel]["sha256"] == sha(BACK + "/" + os.path.basename(rel))) else 0
    check("D03", ok_after == 6, "写/零写面自洽：三写件 备份==before 且 现行==末写者 且确有增量；三场景 before==after==备份（%d/6）" % ok_after)
    before_md = rb(BACK + "/modes_data.json")
    d = json.loads(before_md.decode("utf-8"))
    newd = {}
    for k, v in d.items():
        if k == "modes":
            newd[FIG] = prop
            newd[k] = v + entries
        elif k == "total":
            newd[k] = len(d["modes"]) + 10
        else:
            newd[k] = v
    recon_md = json.dumps(newd, ensure_ascii=False, indent=2).encode("utf-8")
    d2 = json.loads(rb(BACK + "/code_maps.json").decode("utf-8"))
    d2["figures"] = dict(d2["figures"]); d2["figures"][FIG] = cme
    recon_cm = json.dumps(d2, ensure_ascii=False, indent=2).encode("utf-8")
    d3 = json.loads(rb(BACK + "/figure_names.json").decode("utf-8"))
    d3[FIG] = FNAME
    recon_fn = json.dumps(d3, ensure_ascii=False, indent=2).encode("utf-8")
    ok_md = hashlib.sha256(recon_md).hexdigest() == mm["after"]["data/modes_data.json"]["sha256"] and len(recon_md) == mm["after"]["data/modes_data.json"]["bytes"]
    ok_cm = hashlib.sha256(recon_cm).hexdigest() == mm["after"]["data/code_maps.json"]["sha256"] and len(recon_cm) == mm["after"]["data/code_maps.json"]["bytes"]
    ok_fn = hashlib.sha256(recon_fn).hexdigest() == mm["after"]["data/figure_names.json"]["sha256"] and len(recon_fn) == mm["after"]["data/figure_names.json"]["bytes"]
    check("D04", ok_md and ok_cm and ok_fn, "AZJ after 字节级复现（before + entries）：三写件 sha+bytes 与卡面 after 一致",
          {"modes_data": ok_md, "code_maps": ok_cm, "figure_names": ok_fn})
    chain_ok = all(sm["inputs"][rel]["sha256"] == mm["after"][rel]["sha256"] for rel in LIB6) and \
               all(sha(REPO + "/" + rel) == (sm["after"][rel]["sha256"] if isinstance(sm["after"][rel], dict) else sm["after"][rel]) for rel in LIB6)
    check("D05", chain_ok, "链式：AZJ after == 沈复 before（六件）；现行 == 沈复 after（末次写者）")
    check("D06", f_prefix(modes, bmodes), "纯追加：现行前 %d 条 == backup 逐对象全等" % len(bmodes))
    check("D07", f_slice(modes, idx0, entries) and [m["id"] for m in modes[idx0:idx0 + 10]] == CODES,
          "AZJ 10 条位于 [%d:%d]（兄弟增量之前）且逐字 == entries" % (idx0, idx0 + 10))
    shf = [m for m in modes if str(m.get("mode_code", "")).startswith("M-SHF-")]
    tail_ok = len(shf) == 10 and canon(modes[-10:]) == canon(shf) and [m["id"] for m in shf] == ["M-SHF-%03d" % i for i in range(1, 11)]
    check("D08", tail_ok, "尾部 10 条 = 兄弟卡 M-SHF-001~010（链式可解释）", {"n_shf": len(shf)})
    check("D09", sm.get("union_guard", {}).get("M_AZJ_before") == 10 and sm.get("union_guard", {}).get("M_AZJ_after") == 10,
          "兄弟卡 union_guard：M-AZJ 10 -> 10 守恒（未伤本链面）")
    z_ok = 0
    for rel in LIB3Z:
        rel_b = os.path.basename(rel)
        ok = (mm["before"][rel]["sha256"] == mm["after"][rel]["sha256"] == sha(BACK + "/" + rel_b) == sm["inputs"][rel]["sha256"])
        z_ok += 1 if ok else 0
    check("D10", z_ok == 3, "场景三件 AZJ 零写入（before==after==兄弟 before；%d/3）" % z_ok)
    nl_now = dict((r, rb(REPO + "/" + r)[-1:] == b"}") for r in LIB3W)
    nl_before = dict((r, rb(BACK + "/" + os.path.basename(r))[-1:] == b"}") for r in LIB3W)
    check("D11", nl_now["data/modes_data.json"] and nl_before["data/modes_data.json"]
          and nl_now["data/code_maps.json"] and nl_now["data/figure_names.json"],
          "序列化：现行三件无尾换行；modes_data before==after（保持）；cm/fn before 有尾换行、after 无（口径注记）",
          {"nl_before": nl_before, "nl_after": nl_now})


    # ================= E 站链与 parity 复核 =================
    print("== E 站链（重算/产物/复跑）与 parity ==")
    meta = rj(REPO + "/web/public/data/meta.json")
    counts = meta["counts"]
    seen = set(); dedup = []
    for m in modes:
        mc = m.get("mode_code")
        if not mc or mc in seen:
            continue
        seen.add(mc); dedup.append(m)
    import importlib.util
    spec = importlib.util.spec_from_file_location("quar", REPO + "/tools/_quarantine.py")
    quar = importlib.util.module_from_spec(spec); spec.loader.exec_module(quar)
    qset = set(quar.QUARANTINE.keys())
    qmodes = [m for m in dedup if m.get("figure_code") in qset]
    pub = [m for m in dedup if m.get("figure_code") not in qset]
    from collections import Counter
    st_pub = dict(Counter(m["verification"]["status"] for m in pub))
    st_all = dict(Counter(m["verification"]["status"] for m in dedup))
    recomputed = {
        "figures": counts.get("figures"), "mode_summaries": len(dedup), "mode_summaries_published": len(pub),
        "modes_quarantined": len(qmodes), "mode_by_figure_shards": len(set(m.get("figure_code") for m in pub)),
        "modes_raw": len(modes), "modes_deduped": len(dedup), "modes_empty_mode_code_dropped": sum(1 for m in modes if not m.get("mode_code")),
    }
    check("E01", f_meta_counts(counts, recomputed), "meta.counts == 数据重算（published %d、by-figure %d、隔离 %d、去重 %d）" % (recomputed["mode_summaries_published"], recomputed["mode_by_figure_shards"], recomputed["modes_quarantined"], recomputed["modes_deduped"]), recomputed)
    vexp = {"published": st_pub, "all": st_all}
    check("E02", f_verif_states(counts.get("verification", {}), vexp), "四态计数 == 数据重算", {"pub": st_pub, "all": st_all})
    sc_txt = rt(REPO + "/web/src/generated/siteCounts.ts")
    mf = rt(REPO + "/web/public/manifest.webmanifest"); mfl = rt(REPO + "/web/public/manifest-light.webmanifest")
    day = rj(REPO + "/web/public/data/daily/index.json")
    ok_face = ("modes: %d" % len(pub)) in sc_txt and ("figures: %d" % recomputed["mode_by_figure_shards"]) in sc_txt
    ok_face = ok_face and (u"%d 条思维模式" % len(pub)) in rt(REPO + "/docs/index.md")
    ok_face = ok_face and (u"%d 条思维模式" % len(pub)) in rt(REPO + "/docs/02-tools/figure_library.md")
    ok_face = ok_face and (u"%d 条思维模式" % len(pub)) in mf and (u"%d 位历史人物" % recomputed["mode_by_figure_shards"]) in mf
    ok_face = ok_face and (u"%d 条思维模式" % len(pub)) in mfl
    ok_face = ok_face and day.get("total") == len(pub) and day.get("shard_count") == recomputed["mode_by_figure_shards"]
    check("E03", ok_face, "门面口径一致：siteCounts.ts / docs / PWA manifest ×2 / daily index（%d x %d）" % (len(pub), recomputed["mode_by_figure_shards"]))
    shard = rj(REPO + "/web/public/data/modes/by-figure/H-AZJ-001.json")
    sm_ok = shard.get("count") == 10 and [m.get("mode_code") for m in shard["modes"]] == CODES
    pick = ["mode_code", "figure_code", "figure_name", "name_zh", "name_en", "category"]
    sm_ok = sm_ok and all(all(sm_m.get(k) == e.get(k) for k in pick) for sm_m, e in zip(shard["modes"], modes[idx0:idx0 + 10]))
    sm_ok = sm_ok and all((sm_m.get("legacy_mode_id") or "") == (e.get("legacy_mode_id") or "")
                          and sm_m.get("key_quote_zh") == e.get("key_quote_zh") for sm_m, e in zip(shard["modes"], modes[idx0:idx0 + 10]))
    CATEGORY_EN = {u"伦理修养": "Ethics & Self-Cultivation", u"军事战略": "Military Strategy", u"医学养生": "Medicine & Wellness",
                   u"史学文献": "History & Texts", u"哲学形而上": "Philosophy & Metaphysics", u"宗教修行": "Religious Practice",
                   u"工程技术": "Engineering & Technology", u"心理洞察": "Psychological Insight", u"战略决策": "Strategic Decision",
                   u"探险发现": "Exploration & Discovery", u"政治治理": "Politics & Governance", u"教育传承": "Education & Transmission",
                   u"文艺审美": "Arts & Aesthetics", u"方法论通用": "General Methodology", u"科学方法": "Scientific Method",
                   u"组织领导": "Organizational Leadership", u"经济商业": "Economics & Business", u"认识论逻辑": "Epistemology & Logic"}
    def _pick_domain(value, fallback, punct):
        s = "" if value is None else str(value).strip()
        if not s:
            return fallback
        head = s.split("/", 1)[0].strip()
        if head and not (len(head) > 30 or punct.search(head)):
            return head
        return fallback
    DOM_ZH = re.compile(u"[。，、；：！？…\n]")
    DOM_EN = re.compile(r"[.,;:!?\n]")
    domain_ok = True
    for sm_m, e in zip(shard["modes"], modes[idx0:idx0 + 10]):
        cat = e.get("category") or ""
        zh = _pick_domain(e.get("domain_zh"), cat, DOM_ZH)
        en = _pick_domain(e.get("domain_en"), CATEGORY_EN.get(cat, cat), DOM_EN)
        if sm_m.get("domain_zh") != zh or sm_m.get("domain_en") != en:
            domain_ok = False
    check("E04", sm_ok and domain_ok, "by-figure 分片 H-AZJ-001：10 条、摘要面 == 主库、domain 压缩 == export 清洗规则")
    if os.path.isdir(REBUILD):
        mism = []; nf = 0
        for dp, dn, fnames in os.walk(REBUILD):
            for fname in fnames:
                rel = os.path.relpath(os.path.join(dp, fname), REBUILD)
                nf += 1
                if rel == "meta.json":
                    rm = rj(os.path.join(dp, fname))
                    if not f_meta_counts(rm.get("counts", {}), recomputed):
                        mism.append(rel + " (counts)")
                    continue
                a = os.path.join(REBUILD, rel); b = REPO + "/web/public/data/" + rel
                if not os.path.isfile(b) or sha(a) != sha(b):
                    mism.append(rel)
        check("E05", not mism, "站链复跑（export_static_site --out 隔离目录）：%d 产物逐字节复现 == web/public/data" % nf, {"mismatch": mism[:8], "files": nf})
    else:
        check("E05", False, "站链复跑目录缺失（%s）：需先跑 tools/export_static_site.py --out" % REBUILD)
    pf = subprocess.run(["python3", "tools/pages_preflight.py", "--stage", "data"], cwd=REPO, capture_output=True, text=True, timeout=1800)
    check("E06", pf.returncode == 0, "pages_preflight --stage data 复跑 exit 0", {"tail": (pf.stdout or pf.stderr)[-200:]})
    par = subprocess.run(["python3", "tools/check_repo_parity.py", "--json"], cwd=REPO, capture_output=True, text=True, timeout=2400)
    pj = json.loads(par.stdout)
    OWN_PENDING = ("docs/research/phase21r9_azj_qa_evidence.json", "docs/research/phase21r9_azj_qa_evidence.txt",
                   "docs/research/phase21r9_azj_qa_report.md", "verify_azj_qa_espinosa.py")
    azj_all = [x for x in pj["diffs"] if ("azj" in x["path"].lower() or u"安子介" in x["path"])]
    own_pending = [x for x in azj_all if x["path"] in OWN_PENDING and x["kind"] == "MISSING_IN_PUBLISH" and u"未跟踪" in (x.get("reason") or "")]
    azj_diffs = [x for x in azj_all if x not in own_pending]
    if own_pending:
        note("E07n", "本卡自证物闭合前登记：未入库的 QA 证据/脚本 %d 件（闭合提交+镜像后复跑须清零）" % len(own_pending),
             {"paths": [x["path"] for x in own_pending]})
    kinds = {}
    for x in pj["diffs"]:
        kinds[x["kind"]] = kinds.get(x["kind"], 0) + 1
    check("E07", not azj_diffs, "parity：本链残留 0（现行 %d 条差异全部为他链在制）" % len(pj["diffs"]), {"kinds": kinds})
    probe = ["data/modes_data.json", "data/code_maps.json", "data/figure_names.json", "data/scenarios_zh.json",
             "data/scenarios_en.json", "data/scenario_tags.json", "data/figures/H-AZJ-001.json",
             "data/figures/H-AZJ-001_modes.json", "data/individuals/H-AZJ-001.json",
             "docs/research/phase21r9_azj_verify_evidence_merged.json", "web/src/generated/siteCounts.ts",
             "docs/research/phase21r9_azj_merge_report.md", "verify_azj_merge_indep.py"]
    info_probe = [rel for rel in probe if not os.path.isfile(PB + "/" + rel) or sha(REPO + "/" + rel) != sha(PB + "/" + rel)]
    check("E08", not info_probe, "两仓点试 %d 件逐字节一致（parity 边界内 AZJ 链面）" % len(probe), {"diff": info_probe})
    pbf = PB + "/web/public/data/modes/by-figure"
    n_pbf_pb = len(os.listdir(pbf)) if os.path.isdir(pbf) else -1
    n_pbf_ws = len(os.listdir(REPO + "/web/public/data/modes/by-figure"))
    note("E08n", "PB web/public/data/** 属 parity 排除类（构建产物，部署侧再生成）；PB by-figure 为旧代次快照（%d 件 vs 工作仓 %d 件；AZJ 分片不在 PB）——建设期登记项，非本链镜像承诺面" % (n_pbf_pb, n_pbf_ws), {"pb_has_azj": os.path.isfile(pbf + "/H-AZJ-001.json")})
    d1 = REPO + "/web/dist/data/modes/by-figure/H-AZJ-001.json"; d2 = REPO + "/web/public/data/modes/by-figure/H-AZJ-001.json"
    if os.path.isfile(d1):
        note("E09", ("dist by-figure H-AZJ-001 == public 副本" if sha(d1) == sha(d2) else "dist by-figure H-AZJ-001 与 public 不同（构建产物，非链产物）"), {"same": sha(d1) == sha(d2)})
    else:
        note("E09", "dist 无 by-figure H-AZJ-001（构建产物缺失）")
    import sqlite3
    con = sqlite3.connect(REPO + "/api/protreptic.db")
    try:
        nfig = con.execute("SELECT COUNT(*) FROM figures").fetchone()[0]
        azj_rows = con.execute("SELECT COUNT(*) FROM figures WHERE code=?", (FIG,)).fetchone()[0]
    finally:
        con.close()
    check("E10", nfig == counts.get("figures") and azj_rows == 0,
          "api/protreptic.db：figures 行数 %d == meta；H-AZJ-001 0 行（DB 非合并卡链条面，先例一致）" % nfig, {"azj_rows": azj_rows})


    # ================= F 推送与镜像实证 =================
    print("== F 推送与镜像实证（ls-remote / PB tree / raw） ==")
    lsr = git(["ls-remote", "origin", "main"], binary=False).strip()
    pb_head = git(["rev-parse", "HEAD"], cwd=PB, binary=False).strip()
    ls_sha = lsr.split()[0] if lsr else ""
    e6 = "e6d133c43c4851ebcd77ab93acd17e5b861d345b"
    subprocess.run(["git", "-C", PB, "fetch", "-q", "origin", "main"], capture_output=True)
    om = git(["rev-parse", "origin/main"], cwd=PB, binary=False).strip()
    e6_anc = subprocess.run(["git", "-C", PB, "merge-base", "--is-ancestor", e6, pb_head]).returncode == 0
    ls_anc = bool(om) and subprocess.run(["git", "-C", PB, "merge-base", "--is-ancestor", e6, om]).returncode == 0
    check("F01", e6_anc and ls_anc,
          "推送实证：e6d133c ∈ 发布仓谱系 ∧ ∈ origin/main 谱系（远端现值 %s；收口时点 e6d133c 见链回执与本卡前轮实测）" % (ls_sha[:8] or om[:8]),
          {"ls": ls_sha[:12], "origin_main": om[:12], "pb_head": pb_head[:12]})
    if ls_sha != e6 or pb_head != e6:
        note("F01n", "远端/发布仓已前移 e6d133c → %s（含他卡/本卡 QA 镜像推送；本链收口 sha e6d133c 在谱系内）" % ((ls_sha or om)[:8]),
             {"pb_head": pb_head[:8]})
    anc = [git(["rev-parse", "%s^" % c], cwd=PB, binary=False).strip()[:7] for c in ["e6d133c", "78246d4", "fe250fd"]]
    msgs_ok = all(("AZJ" in (git(["log", "--format=%s", "-1", c], cwd=PB, binary=False)) or u"安子介" in (git(["log", "--format=%s", "-1", c], cwd=PB, binary=False))) for c in ["fe250fd", "78246d4", "e6d133c"])
    check("F02", anc == ["78246d4", "fe250fd", "3b6874f"] and msgs_ok,
          "发布仓 AZJ 链提交链：e6d133c^=78246d4、78246d4^=fe250fd、fe250fd^=3b6874f 且三提交题为 AZJ 镜像", {"anc": anc, "msgs_ok": msgs_ok})
    spot = ["docs/research/phase21r9_azj_merge_report.md", "docs/research/phase21r9_azj_rebuild_report.md",
            "data/figures/H-AZJ-001.json", "verify_azj_merge_indep.py",
            "docs/scratch/phase21r9_anzijie/witness/W04_patent_CN85101817A.txt",
            "docs/scratch/legacy20_r9_azj_landing/modes_library_entries.json",
            "data/audit/phase21r9_azj_merge_manifest.json", "docs/research/phase21r9_anzijie_sourcing_report.json"]
    bad = [rel for rel in spot if hashlib.sha256(git_blob("e6d133c:" + rel, cwd=PB)).hexdigest() != sha(REPO + "/" + rel)]
    check("F03", not bad, "发布仓 e6d133c 树 blob == 工作仓（%d 件抽验）" % len(spot), {"bad": bad})
    tree = git(["ls-tree", "-r", "--name-only", "e6d133c"], cwd=PB, binary=False).splitlines()
    azj_files = [p for p in tree if ("azj" in p.lower() or "anzijie" in p.lower())]
    miss = []
    for p in azj_files:
        wp = REPO + "/" + p
        if not os.path.isfile(wp):
            miss.append(p + " (worktree-missing)"); continue
        if hashlib.sha256(git_blob("e6d133c:" + p, cwd=PB)).hexdigest() != sha(wp):
            miss.append(p)
    check("F04", not miss, "R9 AZJ 链镜像：PB 树 %d 件 azj/anzijie 命名文件全部 == 工作仓（逐字节）" % len(azj_files), {"miss": miss[:8], "n": len(azj_files)})
    if os.path.isfile(RAWLOG):
        lines = [l for l in rt(RAWLOG).splitlines() if l.strip() and l.strip() != "DONE"]
        ok_raw = len(lines) >= 5 and all((" http=200 " in l and " SAME " in l) for l in lines)
        check("F05", ok_raw, "raw.githubusercontent.com 抽验 %d 件：http=200 且逐字节 SAME（远端发布面）" % len(lines), {"lines": [l.split()[0] for l in lines]})
    else:
        check("F05", False, "raw 抽验日志缺失：需先跑 rawprobe.py")
    for c, tag in [("602a5d47", "AZJ-2 重建"), ("a96302f1", "AZJ-3 合并"), ("5ce7f6ad", "回执补记"), ("8c486442", "回执补记 v2")]:
        files = [p for p in git(["show", "--name-only", "--format=", c], binary=False).splitlines() if p.strip()]
        check("F06." + c[:4], len(files) > 0, "回执提交 %s（%s）在库，%d 件" % (c[:8], tag, len(files)))
    OWN_CLOSURE = ("verify_azj_qa_espinosa.py", "docs/research/phase21r9_azj_qa_report.md",
                   "docs/research/phase21r9_azj_qa_evidence.json", "docs/research/phase21r9_azj_qa_evidence.txt")
    pb_delta = [p for p in git(["log", "--name-only", "--format=", "%s..%s" % (e6, pb_head)], cwd=PB, binary=False).splitlines() if p.strip()]
    own_in_delta = [p for p in pb_delta if p in OWN_CLOSURE]
    other_delta = [p for p in pb_delta if p not in OWN_CLOSURE]
    azj_delta = [p for p in other_delta if ("azj" in p.lower() or "anzijie" in p.lower())]
    check("F07", not azj_delta, "发布仓在制增量（e6d133c..HEAD %d 件，含本卡 QA 镜像 %d 件）零他卡 AZJ 链文件" % (len(pb_delta), len(own_in_delta)), {"delta": other_delta[:6]})

    # ================= G 边界抽查 =================
    print("== G 边界抽查（旧假件零残留 / 未动他人物 / 禁用面） ==")
    scan = json.load(open(SC + "/scan345.json"))
    ws_hits = scan["ws"]
    live_prefixes = ["data/modes_data.json", "data/code_maps.json", "data/figure_names.json",
                     "data/scenarios_zh.json", "data/scenarios_en.json", "data/scenario_tags.json",
                     "web/public/", "web/src/", "web/dist/", "api/protreptic.db", "api/data/scenarios",
                     "tools/json/", "docs/figures/"]
    live_ws = [h for h in ws_hits if any(h == p or h.startswith(p) for p in live_prefixes)]
    check("G01", not live_ws, "H-AZJ-345 工作仓：live 面（主库六件/站点数据/dist/DB/tools json/docs figures）0 命中", {"live_hits": live_ws[:8], "total": len(ws_hits)})
    cls = Counter()
    for h in ws_hits:
        if h.startswith("site_docs/"): cls[u"site_docs(陈旧导航/页)"] += 1
        elif h.startswith("data/backup"): cls["data/backup*"] += 1
        elif h.startswith("data/figures/_duplicates/"): cls["_duplicates"] += 1
        elif h.startswith("docs/research/") or h.startswith("docs/qa/") or h.startswith("docs/scratch/") or h.startswith("data/audit/"): cls[u"记录/证据"] += 1
        elif h.startswith("release/"): cls[u"冻结快照"] += 1
        elif "semantic_index" in h: cls[u"登记残留(语义索引)"] += 1
        elif h in ("protreptic.db",): cls[u"离线根库"] += 1
        elif h.startswith("tools/") or h.startswith("verify_"): cls[u"脚本面(链)"] += 1
        elif h.startswith("data/figures/H-AZJ-001") or h.startswith("data/individuals/H-AZJ-001"): cls[u"AZJ-001 数据件(登记)"] += 1
        elif h.startswith("docs/architecture/"): cls["docs/architecture"] += 1
        else: cls[u"未分类"] += 1
    note("G02", "工作仓 H-AZJ-345 命中分类（%d 件）" % len(ws_hits), dict(cls))
    r8 = json.load(open(R8WS))
    r8code = set(h[0] for h in r8["hits"] if h[1] > 0)
    cur = set(ws_hits)
    new = sorted(cur - r8code); gone = sorted(r8code - cur)
    ok_new = all(
        (p.startswith("docs/research/phase21r9") or p.startswith("data/audit/phase21r9") or p.startswith("data/figures/H-AZJ-001")
         or p.startswith("data/individuals/H-AZJ-001") or p.startswith("docs/scratch/legacy20_r9_azj_landing") or p.startswith("docs/scratch/phase21r9_azj")
         or p.startswith("tools/build_phase21r9_azj") or p.startswith("tools/merge_azj_hazj001") or p.startswith("verify_phase21r9_azj")
         or p.startswith("docs/research/phase21r8_azj345") or p.startswith("verify_azj_qa_espinosa"))
        for p in new)
    live_new = [p for p in new if p.startswith("web/") or p.startswith("data/scenarios") or p.startswith("api/")]
    check("G03", ok_new and not live_new, "R8 清档基线对比：新增 %d 件全部为受控登记件、零移除、无 live 面新增" % len(new), {"new": new, "gone": gone})
    fb = [t for t in FORBIDDEN_OLD if t in (canon(fg) + canon(entries) + canon(md[FIG]) + canon(cme))]
    check("G04", not fb, "禁用标记 19 项：figure+条目+顶层块+code_maps 面零出现", {"hits": fb})
    chain_commit_ok = True
    for c in ["602a5d47", "a96302f1"]:
        for p in git(["show", "--name-only", "--format=", c], binary=False).splitlines():
            p = p.strip()
            if not p:
                continue
            if not (p.startswith("docs/scratch/legacy20_r9_azj") or p.startswith("docs/scratch/phase21r9_azj")
                    or p.startswith("docs/scratch/phase21r9_anzijie") or p.startswith("docs/research/phase21r9_azj")
                    or p.startswith("docs/research/phase21r9_anzijie") or p.startswith("data/figures/H-AZJ-001")
                    or p.startswith("data/individuals/H-AZJ-001") or p.startswith("data/audit/phase21r9_azj")
                    or p.startswith("data/backup_merge_H-AZJ-001")
                    or p in ("tools/build_phase21r9_azj.py", "tools/merge_azj_hazj001.py", "verify_phase21r9_azj.py", "verify_azj_merge_indep.py")):
                chain_commit_ok = False
    check("G05", chain_commit_ok, "链提交面：602a5d47/a96302f1 文件清单全部为 AZJ 链文件（零夹带他人物/他链）")

    # ================= H 反向注入自检（检查器灵敏度） =================
    print("== H 反向注入自检（检查器灵敏度） ==")
    inj = []
    e0 = json.loads(canon(entries[0])); e0["mode_code"] = "M-AZJ-099"; inj.append(("编号篡改", not f_code(e0, 0)))
    q0 = json.loads(canon(entries[0])); q0["key_quote_zh"] = q0["key_quote_zh"][:-2]; inj.append(("引文篡改", not f_quote(q0, pm[CODES[0]])))
    m0 = json.loads(canon(modes)); m0[5] = dict(m0[5]); m0[5]["name_zh"] = "X"; inj.append(("前缀篡改", not f_prefix(m0, bmodes)))
    m1 = json.loads(canon(modes)); m1.pop(idx0 + 3); inj.append(("位置缺失", not f_slice(m1, idx0, entries)))
    keys = list(md.keys()); k2 = [k for k in keys if k != FIG]; k2.insert(keys.index("modes"), FIG)
    inj.append(("块位移", not f_block_pos(k2, list(bmd.keys()))))
    f2 = json.loads(canon(fg)); f2["mode_ids"] = f2["mode_ids"][:-1]; inj.append(("图档码缺失", not f_figmodes(f2, CODES)))
    c2 = dict(recomputed); c2["mode_summaries_published"] = 1; inj.append(("计数篡改", not f_meta_counts(dict(counts), c2)))
    check("H01", all(x[1] for x in inj), "反向注入 %d/%d 全部被检查器捕获" % (sum(1 for x in inj if x[1]), len(inj)), {"inj": inj})

    # ================= 汇总 =================
    npass, nfail = len(PASS), len(FAIL)
    print("-" * 78)
    print("TOTAL %d PASS / %d FAIL / %d INFO" % (npass, nfail, len(INFO)))
    out = {"schema": "protreptic.phase21r9_azj_qa/v1", "card": "t_02007da8", "tool": "verify_azj_qa_espinosa.py",
           "date": "2026-09-24", "figure_code": FIG, "total": npass + nfail, "passed": npass, "failed": nfail,
           "info": len(INFO), "results": PASS + FAIL + INFO}
    with io.open(REPO + "/docs/research/phase21r9_azj_qa_evidence.json", "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write(u"\n")
    with io.open(REPO + "/docs/research/phase21r9_azj_qa_evidence.txt", "w", encoding="utf-8") as f:
        for r in PASS:
            f.write("PASS " + r["tag"] + " " + r["msg"] + "\n")
        for r in FAIL:
            f.write("FAIL " + r["tag"] + " " + r["msg"] + "\n")
        for r in INFO:
            f.write("INFO " + r["tag"] + " " + r["msg"] + "\n")
        f.write("\nTOTAL %d PASS / %d FAIL / %d INFO\n" % (npass, nfail, len(INFO)))
    print("evidence -> docs/research/phase21r9_azj_qa_evidence.json/.txt")
    sys.exit(1 if nfail else 0)


if __name__ == "__main__":
    main()
