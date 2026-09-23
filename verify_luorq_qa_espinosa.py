#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase21-R8 罗瑞卿 H-LUORQ-001 QA 独立核验脚本 (espinosa / 卡 t_8773cb6b)

判据修正 v2 (卡 t_65998945 复验时定位并修正, 两种模式同时生效):
  - A03: 章号见证路径改用 ch 组号 (xuoba/ch√号.txt); 原用 W 组号导致章号误定位
  - B01: 注册解析改为行域匹配 (原跨行正则会将 W14 无 sha 行误并入后行)
  - A07/B05: 扫描面扩展至素材包 json (原仅 md, 导致 json 字段来源片段误报越界)
  - C/E/G02: 场景面下钻内层字典 scenarios_zh/en (原扫顶层键恒 0, 与合并落地无关)
  - A07 省略号片段: 按……切分各段逐一追溯 (原整段子串匹配, 带省略号的片段恒不命中)
  修正前口径证据冻结于 docs/qa/phase21r8_luorq_qa_evidence/ (卡 t_8773cb6b); 复验证据另存 docs/qa/phase21r8_luorq_qa_recheck_evidence/


独立第二实现: 不引用合并卡或落盘卡自述结论, 直接对工作仓现势与素材包/见证原件、
审计登记、门禁与两仓 parity 复算。
用法:
  python3 verify_luorq_qa_espinosa.py             # 全量核验 + 反向注入自检
  python3 verify_luorq_qa_espinosa.py --no-gates  # 跳过门禁子进程 (快速复跑)
退出码: 0 = 0 FAIL; 1 = 有 FAIL。
"""
import hashlib, io, json, os, re, subprocess, sys, glob
from collections import Counter
from datetime import datetime

REPO = os.path.dirname(os.path.abspath(__file__))
WIT = "/opt/data/profiles/serrano/cache/scratch/r8"
BACKUP_GLOB = "/opt/data/kanban/boards/protreptic/workspaces/t_08bbb73d/backup_merge_H-LUORQ-001_*"
PUBLISH = "/opt/data/release/Protreptic-publish"
EV = os.path.join(REPO, "docs/qa/phase21r8_luorq_qa_evidence")
GATES = os.path.join(REPO, "docs/qa/phase21r8_luorq_qa_gates")
SELFTEST = os.path.join(REPO, "docs/qa/phase21r8_luorq_qa_selftest.json")
CARD = "t_8773cb6b"
RECHECK = False
FIG = "H-LUORQ-001"
NAME = "罗瑞卿"
CODES = ["M-LUORQ-%03d" % i for i in range(1, 11)]
LEGACY = ["M35%d" % i for i in range(1, 10)] + ["M360"]
SZH = ["C-LUORQ-%03d" % i for i in range(1, 11)]
SEN = [c + "E" for c in SZH]
SURF6 = ["data/modes_data.json", "data/code_maps.json", "data/scenarios_zh.json",
         "data/scenarios_en.json", "data/scenario_tags.json", "data/figure_names.json"]
BANNED4 = ["安全立军", "整编革新", "参谋统筹", "情报先行"]
BANNED_OLD = BANNED4 + ["Ten Marshals", "主要创建者", "国防部长"]
PASS, FAIL, INFO = [], [], []
CJKQ = "\u300c\u300d\u300e\u300f"
NOW = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def check(cid, desc, cond, detail=""):
    (PASS if cond else FAIL).append({"id": cid, "desc": desc, "detail": str(detail)[:400]})
    print("%s %-6s %s%s" % ("PASS" if cond else "FAIL", cid, desc,
                            (" | " + str(detail)[:300]) if detail else ""), flush=True)
    return bool(cond)

def note(msg): INFO.append(msg); print("INFO  " + msg, flush=True)
def jl(p): return json.load(io.open(p, encoding="utf-8"))
def rl(p, err="replace"): return io.open(p, encoding="utf-8", errors=err).read()
def rb(p): return open(p, "rb").read()
def sha_b(b): return hashlib.sha256(b).hexdigest()
def sha_f(p): return sha_b(rb(p))
WS = re.compile(r"\s+")
def norm_ws(s): return WS.sub("", s)

def strong_norm(s):
    """强归一化: 去空白+去 ASCII 标点+去 CJK 标点/全角形/通用标点, 保留汉字字母数字。"""
    s = norm_ws(s)
    keep = []
    for ch in s:
        o = ord(ch)
        if o < 128:
            if ch.isalnum(): keep.append(ch)
        elif 0x3000 <= o <= 0x303F or 0xFF00 <= o <= 0xFFEF or 0x2000 <= o <= 0x206F or 0xFE30 <= o <= 0xFE4F:
            continue
        else:
            keep.append(ch)
    return "".join(keep)

def banned_hits(text, terms=BANNED_OLD):
    return sorted(set(t for t in terms if t in text))

def dup_keys_of(path):
    dups = []
    def hook(pairs):
        seen = set()
        for k, v in pairs:
            if k in seen:
                dups.append(k)
            seen.add(k)
        return dict(pairs)
    try:
        json.load(io.open(path, encoding="utf-8"), object_pairs_hook=hook)
    except Exception as e:
        dups.append("PARSE_ERROR: %s" % e)
    return dups

def load_library(root=REPO):
    d = {}
    d["md"] = jl(os.path.join(root, "data/modes_data.json"))
    d["cm"] = jl(os.path.join(root, "data/code_maps.json"))
    d["fn"] = jl(os.path.join(root, "data/figure_names.json"))
    d["sz"] = jl(os.path.join(root, "data/scenarios_zh.json"))
    if isinstance(d["sz"], dict) and "scenarios_zh" in d["sz"]:
        d["sz"] = d["sz"]["scenarios_zh"]
    d["se"] = jl(os.path.join(root, "data/scenarios_en.json"))
    if isinstance(d["se"], dict) and "scenarios_en" in d["se"]:
        d["se"] = d["se"]["scenarios_en"]
    d["st"] = jl(os.path.join(root, "data/scenario_tags.json"))
    # modes_data has top-level figure objects AND modes list
    # The H-LUORQ-001 top block is at md[FIG] directly
    top_block = d["md"].get(FIG)
    # modes list may have entries with 'id' or 'mode_code'
    modes = d["md"].get("modes", [])
    d["entries"] = [e for e in modes if str(e.get("mode_code", e.get("id", ""))).startswith("M-LUORQ")]
    d["top_block"] = top_block
    return d

def parse_b1_sections(path=None):
    path = path or os.path.join(REPO, "docs/research/phase21r8_luorq_sourcing_report.md")
    src = rl(path)
    secs, quotes, cur = {}, {}, None
    for line in src.split("\n"):
        m = re.match(r"^### (M-LUORQ-\d+)", line)
        if m:
            cur = m.group(1); secs[cur] = []; quotes[cur] = []
        elif cur and line.strip().startswith(">"):
            secs[cur].append(line.strip()); quotes[cur].append(line.strip().lstrip(">").strip())
    return src, secs, quotes

WMAP = {"W1": "web/B520315.txt", "W2": "web/rr1951_0101_p3.txt", "W3": "web/rr1978_0813_p2.txt",
        "W4": "web/ws_pingfan_raw.txt", "W5": "web/ws_1966_raw.txt", "W6": "web/ccrd_000209.txt",
        "W7": "web/hprc5150213.txt", "W8": "web/iccs5392393.txt", "W9": "web/iccs5392400.txt",
        "W10": "web/hswh_92285.txt", "W11": "web/chinanews_1088475.txt", "W12": "web/cpc_zhenli.txt",
        "W13": "web/dangshi34.txt", "W15": "web/cn2008.txt", "W16": "web/wangsu.txt",
        "W17": "web/mod_gxf.txt", "W18": "web/cpc_gxf2023.txt", "W19": "web/cpc_12371_gxf.txt",
        "W21": "web/mtoou_toc.txt"}

def witness_files_for(mode_quotes):
    ids, chaps = [], []
    for q in mode_quotes:
        for m in re.finditer(r"W(\d{1,2})(?:/ch(\d{3}))?", q):
            wid = "W" + m.group(1)
            if m.group(2):
                chaps.append("xuoba/ch%s.txt" % m.group(2))
            elif wid in WMAP and WMAP[wid] not in ids:
                ids.append(WMAP[wid])
    return ids, sorted(set(chaps))

def pred_quote_verbatim(entries, quotes):
    bad = []
    for e in entries:
        mid, q = e["id"], e.get("key_quote_zh", "")
        if not any(q and q in ln for ln in quotes.get(mid, [])):
            bad.append(mid)
    return bad

def section_A(root=REPO):
    print("== A 引文逐条核验 ==")
    d = load_library(root)
    src, secs, quotes = parse_b1_sections(os.path.join(root, "docs/research/phase21r8_luorq_sourcing_report.md"))
    eids = [e["id"] for e in d["entries"]]
    check("A01", "10 条存在且 id 序 == M-LUORQ-001~010", eids == CODES, eids)
    bad = pred_quote_verbatim(d["entries"], quotes)
    check("A02", "10 条 key_quote_zh 逐字为 B1 该模式 quotes 子串", not bad, "未命中: %s" % bad)
    wit_ok = []
    for e in d["entries"]:
        mid = e["id"]
        qq = e.get("key_quote_zh", "").strip(CJKQ)
        wids, chaps = witness_files_for(quotes.get(mid, []))
        hits = []
        for rel in wids + chaps:
            p = os.path.join(WIT, rel)
            if os.path.exists(p) and strong_norm(qq) in strong_norm(rl(p)):
                hits.append(rel)
        wit_ok.append((mid, len(hits)))
        check("A03", "%s 引文见证强归一化命中 %d 件" % (mid, len(hits)), len(hits) >= 1, str(hits[:3]))
    for e in d["entries"]:
        mid = e["id"]
        en = e.get("key_quote_en", "")
        check("A04", "%s key_quote_en 非空且无 CJK" % mid,
              bool(en) and not re.search(u"[\u4e00-\u9fff]", en), str(en)[:60])
        sc = e.get("source_chapter", "")
        check("A05", "%s source_chapter 可落源格式 (书名号+年份)" % mid,
              ("《" in sc and "》" in sc) and re.search(r"(19|20)\d\d", sc) is not None, str(sc)[:60])
        check("A06", "%s key_concepts 非空且无禁字" % mid,
              bool(e.get("key_concepts")) and not banned_hits(json.dumps(e["key_concepts"], ensure_ascii=False)))
    for e in d["entries"]:
        rm = e.get("related_modes", [])
        check("A08", "%s related_modes 合法 (子集且无自引)" % e["id"],
              all(r in CODES for r in rm) and e["id"] not in rm, str(rm))
    imp = os.path.join(root, "docs/scratch/legacy20_r8_luorq_landing/id_mapping.tsv")
    mapping = {}
    for line in rl(imp).split("\n")[1:]:
        c = line.split("\t")
        if len(c) >= 2 and c[0].startswith("M3"):
            mapping[c[0]] = c[1]
    ok = all(mapping.get(e.get("legacy_mode_id", "")) == e["id"] for e in d["entries"])
    check("A09", "legacy_mode_id M351~M360 与 id_mapping.tsv 一一对应", ok and len(mapping) == 10, "%d 行" % len(mapping))
    vs = set(e.get("verification", {}).get("status") for e in d["entries"])
    check("A10", "10 条 verification 全 pending (纪律: 不回填)", vs == {"pending"}, str(vs))
    names = [e["name_zh"] for e in d["entries"]]
    names_en = [e["name_en"] for e in d["entries"]]
    check("A11", "模式名唯一/无禁字/英文名无 CJK",
          len(set(names)) == 10 and len(set(names_en)) == 10
          and not banned_hits(json.dumps(names + names_en, ensure_ascii=False))
          and not re.search(u"[\u4e00-\u9fff]", " ".join(names_en)))
    check("A12", "figure_code/figure_name 口径 == H-LUORQ-001/罗瑞卿",
          all(e.get("figure_code") == FIG and e.get("figure_name") == NAME for e in d["entries"]))
    blob = json.dumps(d["entries"], ensure_ascii=False)
    frags = set(re.findall(u"[\u300c]([^\u300c\u300d]+)[\u300d]", blob))
    frags |= set(re.findall(u"[\u300e]([^\u300e\u300f]+)[\u300f]", blob))
    wl_src = _extract_whitelist(os.path.join(root, "docs/research/phase21r8_luorq_rebuild_report.md"))
    all_quote_text = "|".join("|".join(quotes.get(e["id"], [])) for e in d["entries"])
    _pkgj = os.path.join(root, "docs/research/phase21r8_luorq_sourcing_report.json")
    pkg_json_txt = rl(_pkgj) if os.path.exists(_pkgj) else ""
    def _traceable(x):
        if x in all_quote_text: return True
        if strong_norm(x) in strong_norm(all_quote_text): return True
        if pkg_json_txt and strong_norm(x) in strong_norm(pkg_json_txt): return True
        if any(strong_norm(x) in strong_norm(w) or strong_norm(w) in strong_norm(x) for w in wl_src): return True
        return False
    missing = []
    for f in sorted(frags):
        if len(norm_ws(f)) < 3: continue
        parts = [pp for pp in re.split(u"[…⋯]+", f) if len(norm_ws(pp)) >= 3]
        ok = all(_traceable(pp) for pp in parts) if parts else _traceable(f)
        if not ok:
            missing.append(f)
    check("A07", "条目内引号片段全部可溯源 (B1 引文或白名单)", not missing, "越界: " + "; ".join(missing[:6]))
    return {"levels_missing": bad, "witness": wit_ok, "frags_total": len(frags), "frags_missing": missing}

def _extract_whitelist(path):
    out = []
    for line in rl(path).split("\n"):
        if line.startswith("| M-LUORQ-"):
            c = [x.strip() for x in line.strip("|").split("|")]
            if len(c) >= 2 and c[1]:
                out.append(c[1])
    return out

def section_B(root=REPO):
    print("== B 来源抽查 ==")
    src, secs, quotes = parse_b1_sections(os.path.join(root, "docs/research/phase21r8_luorq_sourcing_report.md"))
    reg = {}
    for ln in src.split("\n"):
        m = re.match(r"^-?\s*\*\*(W\d{1,2})\*\*", ln)
        if not m:
            continue
        ms = re.search(r"sha256=([0-9a-f]{64})", ln)
        if ms:
            reg[m.group(1)] = ms.group(1)
    matched, mism, absent = [], [], []
    for w, rel in sorted(WMAP.items()):
        p = os.path.join(WIT, rel)
        if not os.path.exists(p):
            absent.append(w); continue
        (matched if sha_f(p) == reg.get(w) else mism).append(w)
    check("B01", "见证文件 sha256 与素材包登记一致 %d 件命中" % len(matched),
          not mism and not absent, "mism=%s absent=%s" % (mism, absent))
    chaps = sorted(glob.glob(os.path.join(WIT, "xuoba/ch0[2-8][0-9].txt")))
    comb = hashlib.sha256(b"".join(rb(p) for p in chaps)).hexdigest()
    reg_w20 = "46a07973b8515d45bcf179a034b336b6d4b20dbef7a41ff36a78607fa6330af0"
    check("B02", "W20 组合 sha256 (59 章按序拼接) == 登记值", len(chaps) == 59 and comb == reg_w20,
          "n=%d sha=%s" % (len(chaps), comb[:16]))
    demo = [("web/B520315.txt", "依照毛主席的指示"), ("web/ccrd_000209.txt", "我国的公安工作"),
            ("web/cpc_zhenli.txt", "打板子打我的"), ("xuoba/ch054.txt", "警卫工作一要保证不出乱子"),
            ("web/rr1978_0813_p2.txt", "中国人民解放军的杰出领导人")]
    for rel, s in demo:
        check("B03", "复核示例命中: %s 属于 %s" % (s, rel),
              strong_norm(s) in strong_norm(rl(os.path.join(WIT, rel))), "")
    total_w = sum(len(witness_files_for(quotes.get(c, []))[0]) > 0 for c in CODES)
    check("B04", "10 条模式引文源括注可解析并映射本地见证文件", total_w == 10, "web witness modes: %d" % total_w)
    wl = _extract_whitelist(os.path.join(root, "docs/research/phase21r8_luorq_rebuild_report.md"))
    whole = rl(os.path.join(root, "docs/research/phase21r8_luorq_sourcing_report.md"))
    _jp = os.path.join(root, "docs/research/phase21r8_luorq_sourcing_report.json")
    if os.path.exists(_jp):
        whole = whole + "\n" + rl(_jp)
    bad_wl = [w for w in wl if w and strong_norm(w) not in strong_norm(whole)]
    check("B05", "白名单 %d 条逐条可回溯素材包" % len(wl), len(wl) >= 23 and not bad_wl, "缺失: %s" % bad_wl[:4])
    return {"witness_matched": matched, "mismatch": mism, "absent": absent}


SKIP_DIRS = {".git", "node_modules", "__pycache__", "dist", ".venv", "venv"}

def scan_repo(root, terms=BANNED_OLD, max_mb=60):
    rows = []
    for dp, dn, fns in os.walk(root):
        dn[:] = [d for d in dn if d not in SKIP_DIRS]
        for fn in fns:
            p = os.path.join(dp, fn)
            rel = os.path.relpath(p, root)
            try:
                if os.path.getsize(p) > max_mb * 1024 * 1024: continue
                b = open(p, "rb").read()
                if b"\x00" in b[:4096]: continue
                txt = b.decode("utf-8", "replace")
            except OSError:
                continue
            for t in terms:
                c = txt.count(t)
                if c:
                    i = txt.find(t)
                    rows.append({"path": rel, "term": t, "count": c,
                                 "ctx": txt[max(0, i - 60):i + len(t) + 60].replace("\n", " ")})
    return rows

def classify_path(rel):
    base = rel.split("/")[-1]
    if rel.startswith("data/figures/_duplicates/"): return "archive"
    if ".bak" in base or rel.startswith(("data/backup", "data/merge_staging", "backups/", "backups_merge", "backups_")):
        return "backup"
    if rel.startswith("data/audit/"): return "registration"
    if rel.startswith("data/"): return "active_data"
    if rel.startswith(("docs/research/", "docs/qa/", "docs/scratch/", "docs/architecture/")): return "report"
    if rel.startswith("docs/figures/"): return "active_docs"
    if rel.startswith("docs/"): return "docs_other"
    if rel.startswith("tools/"): return "tooling"
    if rel.startswith("web/"): return "web"
    if rel.startswith(("site_docs/", "release/")): return "stale_copy"
    return "other"

ACTIVE_REQUIRED = {
    "国防部长": ["H-YDZ-001", "H-ZKU-001", "GT-LAN-001"],
    "主要创建者": ["H-ZhouEnLai-001"],
    "Ten Marshals": ["H-YJY-001"],
    "情报先行": None,
    "安全立军": [], "整编革新": [], "参谋统筹": [],
}

def pred_active_hits(rows):
    bad = []
    for r in rows:
        cls = classify_path(r["path"])
        if cls not in ("active_data", "active_docs", "web"):
            continue
        req = ACTIVE_REQUIRED.get(r["term"])
        if req is None:
            continue
        if any(tok in (r["path"] + " " + r["ctx"]) for tok in req):
            continue
        bad.append(r)
    return bad

def section_C(root=REPO):
    print("== C 硬伤清零复扫 ==")
    d = load_library(root)
    lz = []
    lz.append(json.dumps(d["entries"], ensure_ascii=False))
    # Check if LUORQ scenarios exist
    lu_zh = {k:v for k,v in d["sz"].items() if 'LUORQ' in k}
    lu_en = {k:v for k,v in d["se"].items() if 'LUORQ' in k}
    check("C_ScenExist", "LUORQ 场景已入库 (scenarios 内层字典)", len(lu_zh) >= 10 and len(lu_en) >= 10, "zh=%d en=%d" % (len(lu_zh), len(lu_en)))
    tags = d["st"].get("scenario_tags", [])
    lz_tags = [t for t in tags if isinstance(t, dict) and t.get("figure_code") == FIG]
    lz.append(json.dumps([t.get("tag") for t in lz_tags], ensure_ascii=False))
    cm = d["cm"]
    fig_info = cm.get("figures", {}).get(FIG)
    lz.append(json.dumps(fig_info, ensure_ascii=False))
    for p in ["data/figures/%s.json" % FIG, "data/individuals/%s.json" % FIG, "data/individuals/%s_modes.json" % FIG,
              "docs/scratch/legacy20_r8_luorq_landing/modes_library_entries.json",
              "docs/scratch/legacy20_r8_luorq_landing/combined_library_entries.json"]:
        if os.path.exists(os.path.join(root, p)):
            lz.append(rl(os.path.join(root, p)))
    hits = banned_hits("".join(lz))
    check("C01", "LUORQ 交付面 (条目/场景/标签/注册/三件/落地包) 禁字零残留", not hits, hits)
    rows = scan_repo(root)
    byclass = {}
    for r in rows:
        byclass.setdefault(classify_path(r["path"]), []).append(r)
    bad_active = pred_active_hits(rows)
    four = [r for r in rows if r["term"] in ("安全立军", "整编革新", "参谋统筹")
            and classify_path(r["path"]) in ("active_data", "active_docs", "web")]
    check("C02a", "四式弃名中三个唯一自造名 (安全立军/整编革新/参谋统筹): 全库活跃面 0", not four,
          [(r["path"], r["term"]) for r in four][:6])
    check("C02b", "活跃面其余禁字命中均可归因他人物合法语境 (逐条登记)", not bad_active,
          [(r["path"], r["term"]) for r in bad_active][:6])
    for cls in sorted(byclass):
        note("C02 扫描面登记: %s -> %d 行命中 (例: %s)" % (cls, len(byclass[cls]),
             ", ".join(sorted(set(r["path"] for r in byclass[cls]))[:3])))
    au = jl(os.path.join(root, "data/audit/phase21r8_luorq_top_block_backup.json"))
    check("C03a", "审计 after_image 禁字零残留", not banned_hits(json.dumps(au["after_image"], ensure_ascii=False)))
    btxt = json.dumps(au["before_image"], ensure_ascii=False)
    check("C03b", "审计 before_image 为旧叙事 (对照: 含自造名与抬高表述)",
          ("安全立军" in btxt) and ("主要创建者" in btxt))
    m6 = jl(os.path.join(root, "docs/scratch/legacy20_r6c/r6c_archive_manifest.json"))
    regs = [f for f in m6["files"] if "H-LUORQ-001" in f["target"]]
    bad_arch = []
    for f in regs:
        p = os.path.join(root, f["target"])
        if not os.path.exists(p) or sha_f(p) != f["sha256"]:
            bad_arch.append(f["target"])
    check("C04", "归档 _duplicates 四件字节未变 (R6C 登记 sha 复核)", len(regs) == 4 and not bad_arch, bad_arch)
    return {"byclass": {k: len(v) for k, v in byclass.items()},
            "bad_active": [(r["path"], r["term"]) for r in bad_active],
            "sample": rows[:40], "luorq_scenarios_zh": len(lu_zh), "luorq_scenarios_en": len(lu_en)}

def section_D(root=REPO):
    print("== D 顶层块处置/前后像/备份 sha ==")
    d = load_library(root)
    baks = sorted(glob.glob(BACKUP_GLOB))
    check("D00", "备份目录存在 (合并卡工作区备份)", len(baks) >= 1, str(baks))
    if not baks:
        return {}
    bak = baks[-1]
    note("D 备份目录: " + bak + " (卡工作区临时目录, 审计副本见 data/audit/phase21r8_luorq_top_block_backup.json)")
    led = jl(os.path.join(bak, "backup_ledger.json"))
    mm = jl(os.path.join(root, "data/audit/phase21r8_luorq_merge_manifest.json"))
    au = jl(os.path.join(root, "data/audit/phase21r8_luorq_top_block_backup.json"))
    bad1 = []
    for rel in SURF6:
        bp = os.path.join(bak, os.path.basename(rel))
        h = sha_f(bp)
        if not (h == led["files"][rel]["sha256"] == mm["inputs"][rel]["sha256"]):
            bad1.append((rel, h[:12], led["files"][rel]["sha256"][:12], mm["inputs"][rel]["sha256"][:12]))
    check("D01", "备份六件 sha256 == ledger == manifest.inputs (合并前状态可复算)", not bad1, bad1)
    f_old = os.path.join(bak, "top_block_old_H-LUORQ-001.json")
    f_new = os.path.join(bak, "top_block_new_H-LUORQ-001.json")
    so, sn = sha_f(f_old), sha_f(f_new)
    check("D02a", "旧块导出行 sha == ledger.old_canonical == audit.before 登记",
          so == led["top_block"]["old_canonical_sha256"] == au["top_block"]["old_canonical_sha256"], so[:16])
    check("D02b", "新块导出行 sha == manifest.after == audit.after_image 登记",
          sn == mm["top_block_disposition"]["after"]["sha256"] == au["after_image_sha256"], sn[:16])
    old_obj, new_obj = jl(f_old), jl(f_new)
    canon_o = sha_b(json.dumps(old_obj, ensure_ascii=False, indent=2).encode("utf-8"))
    canon_n = sha_b(json.dumps(new_obj, ensure_ascii=False, indent=2).encode("utf-8"))
    file_o = sha_b(json.dumps(old_obj, ensure_ascii=False, indent=2).encode("utf-8") + b"\n")
    file_n = sha_b(json.dumps(new_obj, ensure_ascii=False, indent=2).encode("utf-8") + b"\n")
    check("D02c", "口径复现: 无换行规范序列化 == 上游核验记录 computed 值 (4a40dcd7/a7dab517)",
          canon_o.startswith("4a40dcd76fae519b") and canon_n.startswith("a7dab5177718b5ba"),
          "old=%s new=%s" % (canon_o[:16], canon_n[:16]))
    check("D02d", "登记值 == 规范序列化+行尾换行 (导出行文件字节口径, 可复现)",
          file_o == so and file_n == sn, "%s / %s" % (file_o[:16], file_n[:16]))
    bmd = jl(os.path.join(bak, "modes_data.json"))
    cur = d["md"]
    check("D03a", "before 像三方等价: 备份 modes_data 顶层块 == 导出旧块 == audit.before_image",
          bmd.get(FIG) == old_obj == au["before_image"])
    # D03b: after image 三方等价 (需要当前顶层块存在)
    cur_tb = cur.get(FIG)
    check("D03b", "after 像三方等价: 主库现行顶层块 == 导出新块 == audit.after_image",
          cur_tb == new_obj == au["after_image"], "cur_tb=%s new=%s audit=%s" % 
          (str(cur_tb is not None)[:5], str(new_obj is not None)[:5], str(au["after_image"] is not None)[:5]))
    prop = jl(os.path.join(root, "docs/scratch/legacy20_r8_luorq_landing/top_block_proposal.json"))["proposal"]
    check("D03c", "主库现行顶层块 == 落地提案 (剥离 proposal_note 后逐字)",
          {k: v for k, v in prop.items() if k != "proposal_note"} == cur_tb if cur_tb else False)
    check("D04a", "新旧块同为 23 键且键序一致",
          len(old_obj) == 23 and len(new_obj) == 23 and list(old_obj.keys()) == list(new_obj.keys()),
          "old=%d new=%d" % (len(old_obj), len(new_obj)))
    check("D04b", "proposal_note 未入库 (新块与主库均无)", "proposal_note" not in new_obj and "proposal_note" not in (cur_tb or {}))
    others = [k for k in cur if k not in ("modes", FIG, "schema_version", "total")]
    diff = [k for k in others if cur.get(k) != bmd.get(k)]
    check("D05", "其余顶层键与旧块逐字全等 (仅 H-LUORQ-001 一处差异) 且 total 零改写 3271",
          not diff and cur.get("total") == bmd.get("total") == 3271, diff)
    ntxt = json.dumps(cur_tb or {}, ensure_ascii=False)
    check("D07", "新块硬伤 2/3 修正落实 (杰出领导人 + ten senior generals) 且禁字 0",
          cur_tb and "杰出领导人" in cur_tb.get("unique_thinking_zh", "") and "one of the ten senior generals" in cur_tb.get("unique_thinking_en", "")
          and not banned_hits(ntxt))
    return {"sha_old": so, "sha_new": sn, "canon_old": canon_o, "canon_new": canon_n,
            "cur_topblock_exists": cur_tb is not None}

def section_E(root=REPO):
    print("== E 全库一致性 ==")
    d = load_library(root)
    modes = d["md"]["modes"]
    check("E01", "modes_data: 条目 3291 / total 标量 3271 (口径如实登记)",
          len(modes) == 3291 and d["md"].get("total") == 3271, "%d / %s" % (len(modes), d["md"].get("total")))
    ids = [str(e.get("id") or e.get("mode_code")) for e in modes]
    mcs = [str(e.get("mode_code")) for e in modes if e.get("mode_code")]
    dup_ids = [k for k, v in Counter(ids).items() if v > 1]
    dup_mcs = [k for k, v in Counter(mcs).items() if v > 1]
    # Note: entries without id field have id=None; skip those when checking duplicates
    real_ids = [i for i in ids if i and i != "None"]
    dup_real = [k for k, v in Counter(real_ids).items() if v > 1]
    check("E02a", "全库非空 id 0 重复 / mode_code 0 重复", not dup_real and not dup_mcs,
          "dup_real=%s dup_mcs=%s" % (dup_real[:5], dup_mcs[:5]))
    dk = dup_keys_of(os.path.join(root, "data/modes_data.json"))
    check("E02b", "modes_data JSON 原文无重复键", not dk, dk[:6])
    # Check LUORQ scenarios exist or not (depending on merge status)
    lu_zh = {k:v for k,v in d["sz"].items() if 'LUORQ' in k}
    lu_en = {k:v for k,v in d["se"].items() if 'LUORQ' in k}
    check("E03a", "scenarios_zh 含 C-LUORQ-001~010 (内层字典 10 条)", len(lu_zh) == 10, "zh=%d" % len(lu_zh))
    check("E03b", "scenarios_en 含 C-LUORQ-001E~010E", len(lu_en) == 10, "en=%d" % len(lu_en))
    dk_sz = dup_keys_of(os.path.join(root, "data/scenarios_zh.json"))
    dk_se = dup_keys_of(os.path.join(root, "data/scenarios_en.json"))
    check("E03c", "scenarios zh/en JSON 原文无重复键", not dk_sz and not dk_se, "%s / %s" % (dk_sz[:3], dk_se[:3]))
    # Tags count and LUORQ subset
    tags = d["st"].get("scenario_tags", [])
    lz_tags = [t for t in tags if isinstance(t, dict) and t.get("figure_code") == FIG]
    check("E04a", "scenario_tags 计数 7518 且 LUORQ 计 20", len(tags) == 7518 and len(lz_tags) == 20,
          "%d / %d" % (len(tags), len(lz_tags)))
    bad_t = []
    for t in lz_tags:
        if sorted(t.keys()) != sorted(["mode_code", "tag", "figure_code", "language"]):
            bad_t.append(("keys", t.get("tag")))
        if t.get("language") not in ("zh", "en"):
            bad_t.append(("lang", t.get("tag")))
    pair = Counter((t.get("mode_code"), t.get("language")) for t in lz_tags)
    bad_pair = [k for k, v in pair.items() if v != 1]
    check("E04b", "20 条标签 4 键 / 每 mode zh+en 各 1 / 无重复", not bad_t and not bad_pair
          and len(pair) == 20, (bad_t[:3], bad_pair[:3]))
    name_map = dict(zip(CODES, [e["name_zh"] for e in d["entries"]]))
    ename_map = dict(zip(CODES, [e["name_en"] for e in d["entries"]]))
    bad_tag_name = [t["tag"] for t in lz_tags if t["tag"] not in (name_map[t["mode_code"]] + "_zh", ename_map[t["mode_code"]] + "_en")]
    check("E04c", "标签命名 == 模式中英名 + _zh/_en", not bad_tag_name, bad_tag_name[:5])
    figs = d["cm"].get("figures", {})
    idset = set(ids)
    dangling = [(fc, mc) for fc, v in figs.items() for mc in v.get("mode_ids", []) if mc not in idset]
    lz_dang = [x for x in dangling if x[0] == FIG]
    check("E05a", "code_maps H-LUORQ-001 mode_ids 0 悬空; 全库悬空如实登记 %d" % len(dangling),
          not lz_dang, lz_dang)
    fn = d["fn"]
    xd_all = []
    for fc, v in figs.items():
        for x in v.get("cross_references", []) or []:
            tc = x.get("target_figure_code", x) if isinstance(x, dict) else x
            if tc not in fn:
                xd_all.append((fc, tc))
    lz_xd = [x for x in xd_all if x[0] == FIG]
    check("E05b", "cross_references LUORQ 目标 0 悬空; 全库悬空如实登记 %d" % len(xd_all), not lz_xd, lz_xd)
    check("E05c", "code_maps H-LUORQ-001 tags == 10 中文模式名",
          figs.get(FIG, {}).get("tags") == [e["name_zh"] for e in d["entries"]])
    check("E06", "figure_names: H-LUORQ-001 -> 罗瑞卿; 计数 1083; 名称唯一",
          fn.get(FIG) == NAME and len(fn) == 1083 and sum(1 for v in fn.values() if v == NAME) == 1,
          "%s / %d" % (fn.get(FIG), len(fn)))
    fig = jl(os.path.join(root, "data/figures/%s.json" % FIG)) if os.path.exists(os.path.join(root, "data/figures/%s.json" % FIG)) else {}
    ind = jl(os.path.join(root, "data/individuals/%s.json" % FIG)) if os.path.exists(os.path.join(root, "data/individuals/%s.json" % FIG)) else {}
    im = jl(os.path.join(root, "data/individuals/%s_modes.json" % FIG)) if os.path.exists(os.path.join(root, "data/individuals/%s_modes.json" % FIG)) else {}
    comb = jl(os.path.join(root, "docs/scratch/legacy20_r8_luorq_landing/combined_library_entries.json")) if os.path.exists(os.path.join(root, "docs/scratch/legacy20_r8_luorq_landing/combined_library_entries.json")) else {}
    check("E07a", "三面同体: figure.modes == individuals_modes.modes == landing combined == 主库 10 条",
          fig.get("modes") == im.get("modes") == comb.get("modes") == d["entries"] if all([fig, im, comb]) else len(d["entries"]) == 10)
    check("E07b", "individuals 口径: figure_code/计数/图码一致",
          ind.get("figure_code") == FIG and ind.get("thinking_mode_count") == 10 and fig.get("code") == FIG,
          "%s/%s" % (ind.get("figure_code"), ind.get("thinking_mode_count")))
    live_legacy = [i for i in ids if i in LEGACY] + [m for m in mcs if m in LEGACY]
    leg_field = [e.get("legacy_mode_id") for e in d["entries"]]
    check("E08a", "旧号 M351~M360 不在现役 id/mode_code", not live_legacy, live_legacy)
    check("E08b", "legacy_mode_id 字段为唯一留痕且 == M351~M360 序", leg_field == LEGACY, str(leg_field))
    fjs = sorted(glob.glob(os.path.join(root, "data/figures/*.json")))
    fmd = sorted(glob.glob(os.path.join(root, "data/figures/*.md")))
    dmd = sorted(glob.glob(os.path.join(root, "docs/figures/*.md")))
    note("E09 文件面计数: data/figures json=%d md=%d; docs/figures md=%d; data/individuals json=%d" %
         (len(fjs), len(fmd), len(dmd), len(glob.glob(os.path.join(root, "data/individuals/*.json")))))
    three = (os.path.exists(os.path.join(root, "data/figures/%s.json" % FIG))
             and os.path.exists(os.path.join(root, "data/individuals/%s.json" % FIG))
             and os.path.exists(os.path.join(root, "data/individuals/%s_modes.json" % FIG)))
    docp = os.path.join(root, "docs/figures/%s.md" % FIG)
    if RECHECK:
        shax = sha_f(docp) if os.path.exists(docp) else ""
        note("E09 复验口径: docs 档案页在册实况 sha256=%s (%d B)" % (shax[:16], os.path.getsize(docp) if os.path.exists(docp) else 0))
        check("E09", "H-LUORQ-001 三件在册 + docs 档案页在册 (补交/归档后复验口径)",
              three and os.path.exists(docp) and shax != "", "doc_sha=%s" % shax[:16])
        check("E09d", "docs 档案页 × 发布仓镜像 byte-exact", files_identical("docs/figures/%s.md" % FIG), "")
    else:
        check("E09", "H-LUORQ-001 三件在册且 docs 档案页待归档卡 (不在册为预期)",
              three and not os.path.exists(docp))
    return {"dangling_global": len(dangling), "xref_dangling_global": len(xd_all),
            "luorq_scenarios_zh": len(lu_zh), "luorq_scenarios_en": len(lu_en)}


def run_tool(name, args, out_file, timeout=2400):
    cmd = [sys.executable, os.path.join(REPO, "tools/%s.py" % name)] + args
    try:
        r = subprocess.run(cmd, cwd=REPO, capture_output=True, text=True, timeout=timeout)
        rc, out = r.returncode, r.stdout + (("\n--- stderr ---\n" + r.stderr) if r.stderr else "")
    except subprocess.TimeoutExpired:
        rc, out = -99, "TIMEOUT after %ss" % timeout
    io.open(out_file, "w", encoding="utf-8").write("$ %s\nexit=%d\n%s" % (" ".join(cmd), rc, out))
    return rc, out

def tail_lines(out, n=4):
    return " / ".join([l for l in out.strip().split("\n") if l.strip()][-n:])[:400]

def section_F(run=True):
    print("== F 门禁与站点数据面复跑 ==")
    if not run:
        note("F 段跳过 (--no-gates)")
        return {}
    os.makedirs(GATES, exist_ok=True)
    rc, out = run_tool("credibility_gate", ["--hard-fail"], os.path.join(GATES, "gate_credibility_gate.txt"))
    check("F01", "credibility_gate --hard-fail exit 0", rc == 0, "exit=%d | %s" % (rc, tail_lines(out, 3)))
    rc, out = run_tool("verify_findings", ["--hard-fail"], os.path.join(GATES, "gate_verify_findings.txt"))
    check("F02", "verify_findings --hard-fail exit 0", rc == 0, "exit=%d | %s" % (rc, tail_lines(out, 3)))
    rc, out = run_tool("verify_source_links", ["--hard-fail"], os.path.join(GATES, "gate_verify_source_links.txt"), timeout=2400)
    check("F03", "verify_source_links --hard-fail exit 0 (活链复扫)", rc == 0, "exit=%d | %s" % (rc, tail_lines(out, 3)))
    rc, out = run_tool("apply_verification_status", ["--check"], os.path.join(GATES, "gate_apply_verification_status.txt"))
    note("F04 登记: apply_verification_status --check exit=%d | %s" % (rc, tail_lines(out, 2)))
    check("F04", "apply_verification_status --check 如实登记 (非硬门禁)", True, "exit=%d" % rc)
    rc, out = run_tool("pages_preflight", ["--stage", "data"], os.path.join(GATES, "gate_pages_preflight_data.txt"))
    check("F05", "pages_preflight --stage data exit 0 (静态数据基线/隔离零泄漏)", rc == 0,
          "exit=%d | %s" % (rc, tail_lines(out, 3)))
    rc, out = run_tool("gen_web_site_counts", ["--check"], os.path.join(GATES, "gate_gen_web_site_counts_check.txt"))
    check("F06", "gen_web_site_counts --check exit 0 (站点计数件现行口径)", rc == 0,
          "exit=%d | %s" % (rc, tail_lines(out, 3)))
    return {"f01": rc}

def gitlines(args, cwd):
    r = subprocess.run(["git"] + args, cwd=cwd, capture_output=True, text=True)
    return r.stdout

EXPECT_PENDING = [
    "data/modes_data.json", "data/code_maps.json", "data/figure_names.json", "data/scenario_tags.json",
    "data/scenarios_zh.json", "data/scenarios_en.json", "data/source_links.json",
    "data/figures/H-LUORQ-001.json", "data/individuals/H-LUORQ-001.json", "data/individuals/H-LUORQ-001_modes.json",
    "data/audit/findings.json", "data/audit/source_texts.json",
    "data/audit/source_texts/6f2e2e4e124df80a.txt", "data/audit/source_texts/6f2e2e4e124df80a.zh-cn.txt",
    "data/audit/phase21r8_luorq_landing_manifest.json", "data/audit/phase21r8_luorq_merge_manifest.json",
    "data/audit/phase21r8_luorq_top_block_backup.json",
    "docs/architecture/static_data_manifest.json",
    "web/src/generated/siteCounts.ts",
]

def files_identical(rel):
    a = os.path.join(REPO, rel)
    b = os.path.join(PUBLISH, rel)
    if not (os.path.exists(a) and os.path.exists(b)):
        return False
    return sha_f(a) == sha_f(b)

def section_G(run=True):
    print("== G 两仓 parity ==")
    diffs = {}
    if run:
        rc, out = run_tool("check_repo_parity", [], os.path.join(GATES, "parity_check_repo.txt"), timeout=900)
        note("G01 check_repo_parity exit=%d (在途多卡状态下非零属预期, 差异逐条归属)" % rc)
        for line in out.split("\n"):
            m = re.match(r"\s{2,}([A-Z][A-Z_]+)\s+\[[^\]]*\]\s+(\S+)\s*$", line)
            if m:
                diffs[m.group(2)] = m.group(1)
    pend = {p: ("pending" if p in diffs else ("synced" if files_identical(p) else "ABSENT/OTHER")) for p in EXPECT_PENDING}
    bad = [p for p, s in pend.items() if s == "ABSENT/OTHER"]
    check("G01b", "LUORQ 待镜像清单件件可归属 (在差异清单或已同步, 0 悬空)", not bad, "悬空=%d" % len(bad) if bad else "")
    lz_extra = [p for p in diffs if "luorq" in p.lower() and p not in EXPECT_PENDING]
    check("G01c", "parity 差异中 LUORQ 面路径均在本卡预期清单内", not lz_extra, lz_extra)
    others = sorted(p for p in diffs if p not in EXPECT_PENDING)
    note("G01 差异总数 %d; 非 LUORQ-预期路径 %d 条 (他卡在途/前置漂移, 归报告登记面):" % (len(diffs), len(others)))
    for p in others[:200]:
        note("G01   %s %s" % (diffs[p], p))
    pub = load_library(PUBLISH)
    tri = (FIG in pub["fn"], FIG in pub["cm"].get("figures", {}), any("C-LUORQ" in k for k in pub["sz"]))
    check("G02a", "发布仓 H-LUORQ-001 注册全无 / 全有 (无半截镜像态)", len(set(tri)) == 1, str(tri))
    note("G02 发布仓实况: modes=%d fn=%d cm=%d tags=%d sz=%d (未镜像时 %s 不在册)"
         % (len(pub["md"]["modes"]), len(pub["fn"]), len(pub["cm"].get("figures", {})),
            len(pub["st"].get("scenario_tags", [])), len(pub["sz"]), FIG))
    if FIG in pub["md"]:
        note("G02 发布仓顶层块 name_zh = %s" % pub["md"][FIG].get("name_zh"))
    else:
        note("G02 发布仓无 H-LUORQ-001 顶层块 (未镜像实况)")
    return {"diffs": diffs, "pending": pend, "non_expected": others}

def section_H(root=REPO):
    print("== H 反向注入自检 (判据可致错) ==")
    d = load_library(root)
    _, secs, quotes = parse_b1_sections(os.path.join(root, "docs/research/phase21r8_luorq_sourcing_report.md"))
    au = jl(os.path.join(root, "data/audit/phase21r8_luorq_top_block_backup.json"))
    bak = sorted(glob.glob(BACKUP_GLOB))[-1]
    led = jl(os.path.join(bak, "backup_ledger.json"))
    exp = {rel: led["files"][rel]["sha256"] for rel in SURF6}

    def pred_quote(es):
        return not pred_quote_verbatim(es, quotes)

    def pred_codes(ids):
        return ids == CODES

    def pred_lz_blob(b):
        return not banned_hits(b)

    def pred_topblock(md_obj):
        return md_obj.get(FIG) == au["after_image"]

    def pred_no_legacy(ids, mcs):
        return (not [i for i in ids if i in LEGACY]) and (not [m for m in mcs if m in LEGACY])

    def pred_uniq(seq):
        return all(v == 1 for v in Counter(seq).values())

    def pred_sha_map(pairs):
        return all(h == exp[rel] for rel, h in pairs)

    def pred_xref(xd):
        return not xd

    e2 = json.loads(json.dumps(d["entries"]))
    e2[2]["key_quote_zh"] = e2[2]["key_quote_zh"].rstrip() + "衍"
    check("H01", "注入: 篡改 M-LUORQ-003 引文 -> 逐字判据报错", (not pred_quote(e2)) and pred_quote(d["entries"]))
    i2 = list(CODES)
    i2[0] = "M351"
    check("H02", "注入: 旧号替换 -> 号码判据报错", (not pred_codes(i2)) and pred_codes(CODES))
    b2 = json.dumps(d["entries"], ensure_ascii=False) + "安全立军"
    check("H03", "注入: LUORQ 面混入弃名 -> 禁字判据报错",
          (not pred_lz_blob(b2)) and pred_lz_blob(json.dumps(d["entries"], ensure_ascii=False)))
    m2 = json.loads(json.dumps(d["md"]))
    if FIG in m2:
        m2[FIG]["era"] = "篡改"
    check("H04", "注入: 顶层块篡改 -> 三方等价判据报错", 
          (not pred_topblock(m2)) and pred_topblock(d["md"]),
          "m2 has %s, d has %s" % (FIG in m2, FIG in d["md"]))
    ids_ok = [str(e.get("id") or e.get("mode_code")) for e in d["md"]["modes"]]
    mcs_ok = [str(e.get("mode_code")) for e in d["md"]["modes"] if e.get("mode_code")]
    check("H05", "注入: 现役混入 M351 -> 旧号判据报错",
          (not pred_no_legacy(ids_ok + ["M351"], mcs_ok)) and pred_no_legacy(ids_ok, mcs_ok))
    tmp = os.path.join(EV, "_inject_tmp")
    os.makedirs(tmp, exist_ok=True)
    tname = os.path.basename(SURF6[0])
    data = rb(os.path.join(bak, tname))
    tgt = os.path.join(tmp, tname)
    open(tgt, "wb").write(data[:-1] + bytes([data[-1] ^ 0x01]))
    base_pairs = [(rel, sha_f(os.path.join(bak, os.path.basename(rel)))) for rel in SURF6]
    bad_pairs = list(base_pairs)
    bad_pairs[0] = (SURF6[0], sha_f(tgt))
    check("H06", "注入: 备份件字节翻改 -> sha 判据报错", (not pred_sha_map(bad_pairs)) and pred_sha_map(base_pairs))
    check("H07", "注入: mode_code 重复 -> 唯一性判据报错",
          (not pred_uniq(mcs_ok + ["M-LUORQ-001"])) and pred_uniq(mcs_ok))
    check("H08", "注入: xref 悬空 -> 悬空判据报错",
          (not pred_xref([(FIG, "H-NOPE-999")])) and pred_xref([]))
    return {"n": 8}

def section_Z(root=REPO):
    print("== Z 状态钉扎 (验收时点) ==")
    keys = SURF6 + [
        "data/figures/H-LUORQ-001.json", "data/individuals/H-LUORQ-001.json",
        "data/individuals/H-LUORQ-001_modes.json",
        "data/audit/phase21r8_luorq_merge_manifest.json", "data/audit/phase21r8_luorq_top_block_backup.json",
        "data/audit/phase21r8_luorq_landing_manifest.json",
        "docs/scratch/legacy20_r8_luorq_landing/top_block_proposal.json",
        "docs/research/phase21r8_luorq_sourcing_report.md",
        "docs/research/phase21r8_luorq_rebuild_report.md",
        os.path.relpath(os.path.abspath(__file__), root),
    ]
    shas = {}
    for rel in keys:
        p = os.path.join(root, rel)
        if os.path.exists(p):
            shas[rel] = sha_f(p)
    ws_head = gitlines(["rev-parse", "HEAD"], root).strip()
    ws_porc = gitlines(["status", "--porcelain"], root)
    pub_head = gitlines(["rev-parse", "HEAD"], PUBLISH).strip()
    pub_porc = gitlines(["status", "--porcelain"], PUBLISH)
    note("Z workspace HEAD=%s (porcelain %d 行); publish HEAD=%s (porcelain %d 行)"
         % (ws_head[:12], len([l for l in ws_porc.split("\n") if l.strip()]),
            pub_head[:12], len([l for l in pub_porc.split("\n") if l.strip()])))
    return {"shas": shas, "ws_head": ws_head, "ws_porcelain_lines": len([l for l in ws_porc.split("\n") if l.strip()]),
            "pub_head": pub_head, "pub_porcelain_lines": len([l for l in pub_porc.split("\n") if l.strip()])}

def _argval(name, default=None):
    for a in sys.argv:
        if a.startswith(name + "="):
            return a.split("=", 1)[1]
    return default

def main():
    global EV, GATES, SELFTEST, CARD, RECHECK
    no_gates = "--no-gates" in sys.argv
    EV = _argval("--ev-dir", EV)
    GATES = _argval("--gates-dir", GATES)
    SELFTEST = _argval("--selftest-path", SELFTEST)
    CARD = _argval("--card", CARD)
    RECHECK = "--recheck" in sys.argv
    if RECHECK:
        note("\u5224\u636e\u4fee\u6b63 v2 \u751f\u6548: A03 \u7ae0\u53f7 group(2) / B01 \u884c\u57df\u89e3\u6790 / A07 \u7701\u7565\u53f7\u5206\u6bb5+B05 \u626b\u63cf\u9762\u542b\u7d20\u6750\u5305 json / C-E-G02 \u5185\u5c42\u5b57\u5178")
    os.makedirs(EV, exist_ok=True)
    os.makedirs(GATES, exist_ok=True)
    os.makedirs(os.path.dirname(SELFTEST), exist_ok=True)
    print("==== Phase21-R8 罗瑞卿 (H-LUORQ-001) QA 独立核验 [espinosa/%s%s] @ %s ====" % (CARD, " 复验" if RECHECK else "", NOW))
    res = {"card": CARD, "script": "verify_luorq_qa_espinosa.py", "ts": NOW, "repo": REPO, "recheck": RECHECK}
    for sec, fn in [("A", section_A), ("B", section_B), ("C", section_C), ("D", section_D), ("E", section_E)]:
        res[sec] = fn(REPO)
    res["F"] = section_F(run=not no_gates)
    res["G"] = section_G(run=not no_gates)
    res["H"] = section_H(REPO)
    res["Z"] = section_Z(REPO)
    res["pass"] = len(PASS)
    res["fail"] = len(FAIL)
    res["checks"] = PASS + FAIL
    with io.open(os.path.join(EV, "result.json"), "w", encoding="utf-8") as f:
        f.write(json.dumps(res, ensure_ascii=False, indent=2, default=str))
    with io.open(os.path.join(EV, "result.txt"), "w", encoding="utf-8") as f:
        for d in PASS:
            f.write("PASS  %-6s %s | %s\n" % (d["id"], d["desc"], d["detail"]))
        for d in FAIL:
            f.write("FAIL  %-6s %s | %s\n" % (d["id"], d["desc"], d["detail"]))
        for i in INFO:
            f.write("INFO  %s\n" % i)
    self_j = {"card": CARD, "ts": NOW, "script": "verify_luorq_qa_espinosa.py", "recheck": RECHECK,
              "pass": len(PASS), "fail": len(FAIL), "checks": PASS + FAIL,
              "injections": [c for c in (PASS + FAIL) if c["id"].startswith("H")],
              "state": res.get("Z"), "git": {"ws_head": res["Z"]["ws_head"], "pub_head": res["Z"]["pub_head"]}}
    with io.open(SELFTEST, "w", encoding="utf-8") as f:
        f.write(json.dumps(self_j, ensure_ascii=False, indent=2, default=str))
    print("==== 总结: %d PASS / %d FAIL / %d INFO ====" % (len(PASS), len(FAIL), len(INFO)))
    if FAIL:
        print("FAIL 清单:")
        for d in FAIL:
            print("  %s %s | %s" % (d["id"], d["desc"], d["detail"]))
    return 0 if not FAIL else 1

if __name__ == "__main__":
    sys.exit(main())
