#!/usr/bin/env python3
"""verify_batch1_qa_espinosa.py — Phase21-W8 Stage2 批1 QA 复核的独立校验器（卡 t_e727be57）。

双锚点核验：
  * QA 锚点（--at，默认 = 最后一次改动本文件的提交）：账本修正 / qa_addendum / 跨引 / 书级列；
  * W8 数据锚点（--w8-at，默认 eda40f5b）：四态重算 / 翻面 / 引文零改写 / findings / 缓存 / 链接 / 站面计数。
  （W8 之后他卡链继续演进，W8 数据面必须钉在 W8 窗口提交上复核，见 QA 报告口径节。）

    python3 tools/verify_batch1_qa_espinosa.py                 # QA 锚点默认 + W8 锚点默认
    python3 tools/verify_batch1_qa_espinosa.py --at eda40f5b   # 复核前态: 应命中 6 项缺陷断言（退出码 1）
    python3 tools/verify_batch1_qa_espinosa.py --with-gates    # 外加 3 门禁复跑（临时 worktree, 无网络）
    python3 tools/verify_batch1_qa_espinosa.py --with-links    # 外加链接门禁复跑（走网络）
    python3 tools/verify_batch1_qa_espinosa.py --with-remote   # 外加发布仓 push 面（ls-remote）
退出码：0 全 PASS / 1 任一 FAIL / 2 基础设施错误。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from collections import Counter
from pathlib import Path

SELF = Path(__file__).resolve()
REPO_ROOT = SELF.parent.parent
PUBLISH = Path("/opt/data/release/Protreptic-publish")
BACKUP = REPO_ROOT / "data/backup_merge_W8B1_20260924_113742"

W8_COMMIT = "eda40f5b"     # W8 landing 终态（数据面与 004332b4 同）
WS_W8 = "004332b4"         # W8 主提交（工作仓）
MIRROR_W8 = "023a794"      # W8 主镜像提交（发布仓，对齐 004332b4）
MIRROR_W8FIX = "c522897"   # W8 回执补记镜像提交（对齐 eda40f5b）
WS_W8FIX = "eda40f5b"

L_LEDGER = "data/audit/phase21w8_stage2_batch1_landing_ledger.json"
P_REPORT = "docs/research/phase21w8_stage2_batch1_landing_report.md"
P_EVID = "docs/research/phase21w8_stage2_batch1_landing_evidence.json"
QA_REPORT = "docs/research/phase21w8_stage2_batch1_qa_report_espinosa.md"
QA_EVID = "docs/research/phase21w8_stage2_batch1_qa_evidence_espinosa.json"
T_VERIF = "tools/verify_batch1_qa_espinosa.py"
T_LEDGER_TOOL = "tools/build_batch1_landing_ledger.py"
QA_FILES = [L_LEDGER, P_REPORT, P_EVID, QA_REPORT, QA_EVID, T_VERIF, T_LEDGER_TOOL]

RESULTS = []


def check(name, cond, detail=""):
    RESULTS.append((name, bool(cond), detail))
    print("[%s] %s%s" % ("PASS" if cond else "FAIL", name, (" — " + detail) if detail else ""), flush=True)


def git(*args, cwd=REPO_ROOT, text=False):
    r = subprocess.run(["git", "-C", str(cwd), *args], capture_output=True)
    if text:
        return r.stdout.decode("utf-8", errors="replace"), r.returncode
    return r.stdout, r.returncode


def gfile(commit, path, cwd=REPO_ROOT):
    out, rc = git("show", "%s:%s" % (commit, path), cwd=cwd)
    return out if rc == 0 else None


def sha16b(b):
    return hashlib.sha256(b).hexdigest()[:16]


def sha16f(p):
    return sha16b(Path(p).read_bytes())


def jload(b):
    return json.loads(b.decode("utf-8"))


def entries_map(doc):
    e = doc.get("entries")
    if isinstance(e, dict):
        return e
    out = {}
    for x in (e or []):
        out[x.get("key") or x.get("label")] = x
    return out


def load_quarantine():
    import importlib.util
    cand = REPO_ROOT / "tools" / "_quarantine.py"
    spec = importlib.util.spec_from_file_location("_q_qa", cand)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return set((getattr(mod, "QUARANTINE", {}) or {}).keys())


def resolve_commit(explicit):
    if explicit:
        return explicit
    rel = str(SELF.relative_to(REPO_ROOT))
    out, rc = git("log", "-1", "--format=%H", "--", rel, text=True)
    if rc == 0 and out.strip():
        return out.strip()
    out, rc = git("rev-parse", "HEAD", text=True)
    return out.strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--at", default=None)
    ap.add_argument("--w8-at", default=None)
    ap.add_argument("--with-gates", action="store_true")
    ap.add_argument("--with-links", action="store_true")
    ap.add_argument("--with-remote", action="store_true")
    args = ap.parse_args()

    commit = resolve_commit(args.at)
    w8 = args.w8_at or W8_COMMIT
    csha, rc = git("rev-parse", commit, text=True)
    if rc != 0:
        print("[ERR] QA 提交不可解析: %s" % commit)
        return 2
    wsha, rc = git("rev-parse", w8, text=True)
    if rc != 0:
        print("[ERR] W8 锚点不可解析: %s" % w8)
        return 2
    print("== verify_batch1_qa_espinosa @ QA %s / W8 %s ==" % (csha.strip()[:12], wsha.strip()[:12]))

    bmd = jload((BACKUP / "data__modes_data.json").read_bytes())
    bfind = jload((BACKUP / "data__audit__findings.json").read_bytes())
    bstxt = entries_map(jload((BACKUP / "data__audit__source_texts.json").read_bytes()))
    blinks = jload((BACKUP / "data__source_links.json").read_bytes())

    led_b = gfile(commit, L_LEDGER)
    rep_b = gfile(commit, P_REPORT)
    ev_b = gfile(commit, P_EVID)
    if led_b is None or rep_b is None or ev_b is None:
        print("[ERR] 基本文件在 QA 锚点缺失")
        return 2
    led = jload(led_b)
    ev = jload(ev_b)
    Lsha = sha16b(led_b)
    Rsha = sha16b(rep_b)

    md_b = gfile(w8, "data/modes_data.json")
    md = jload(md_b)
    modes = [m for m in md["modes"] if isinstance(m, dict)]

    # ---------- F1/F2/F3: 账本修正断言（QA 锚点） ----------
    fs = led.get("four_state") or {}
    fb = (fs.get("before") or {}).get("counts") or {}
    fa = (fs.get("after") or {}).get("counts") or {}
    fbi = (fs.get("before") or {}).get("inputs") or {}
    fai = (fs.get("after") or {}).get("inputs") or {}
    check("F1 账本 four_state.before 真值（949/1959/52/351, 3311）",
          fb.get("all", {}).get("verified") == 949 and fb.get("all", {}).get("pending") == 1959
          and fb.get("all", {}).get("suspect") == 52 and fb.get("all", {}).get("unverifiable") == 351
          and fb.get("all_total") == 3311)
    check("F1b 账本 before 发布口径 949/1927/35/340（3251）",
          fb.get("published", {}).get("verified") == 949 and fb.get("published", {}).get("pending") == 1927
          and fb.get("published", {}).get("suspect") == 35 and fb.get("published", {}).get("unverifiable") == 340
          and fb.get("published_total") == 3251 and fb.get("quarantined_total") == 60)
    check("F1c 账本 before inputs sha16 == 备份态实测",
          fbi.get("data/modes_data.json") == "6f3f4580397614f5"
          and fbi.get("data/source_links.json") == "9df3d1fd210b2926"
          and fbi.get("data/audit/findings.json") == "b73e32806f7c910b")
    fai_ok = (fai.get("data/modes_data.json") == sha16b(md_b)
              and fai.get("data/source_links.json") == sha16b(gfile(w8, "data/source_links.json") or b"")
              and fai.get("data/audit/findings.json") == sha16b(gfile(w8, "data/audit/findings.json") or b""))
    check("F3 账本 after inputs sha16 == W8 锚点文件", fai_ok)
    add = led.get("qa_addendum") or {}
    cids = {c.get("id") for c in (add.get("corrections") or [])}
    fids = {f.get("id") for f in (add.get("findings") or [])}
    check("F2 qa_addendum 修正与发现登记齐备（C0/C1/C2 + F1..F6）",
          {"QA-C0", "QA-C1", "QA-C2"} <= cids and {"QA-F1", "QA-F2", "QA-F3", "QA-F4", "QA-F5", "QA-F6"} <= fids)

    # ---------- F4: 跨引一致性（QA 锚点） ----------
    rep_txt = rep_b.decode("utf-8")
    ref_line = "| data/audit/phase21w8_stage2_batch1_landing_ledger.json | — | %s |" % Lsha
    check("F4a 报告附录 B 账本 sha16 == QA 锚点实测", ref_line in rep_txt)
    outputs = {o.get("path"): o for o in (ev.get("outputs") or [])}
    check("F4b 证据 outputs 账本/报告 sha16 == QA 锚点实测",
          (outputs.get(L_LEDGER) or {}).get("sha16") == Lsha and (outputs.get(P_REPORT) or {}).get("sha16") == Rsha)
    tool_b = gfile(commit, T_LEDGER_TOOL) or b""
    check("F4c 证据 outputs 账本工具 sha16 == QA 锚点实测",
          (outputs.get(T_LEDGER_TOOL) or {}).get("sha16") == sha16b(tool_b))

    # ---------- C0: 书级列 + links_added（QA 锚点账本 vs W8 数据） ----------
    books = led.get("books") or []
    linked = [b for b in books if b.get("link_in_source_links")]
    merged = [b for b in books if b.get("cache_merged_into_source_texts")]
    linked_ok = len(linked) == 8 and all(b.get("link_url") for b in linked)
    check("C0a 账本书级列 8 链接 / 17 缓存合并 / sha 全等",
          linked_ok and len(merged) == 17
          and all(b.get("cache_sha256_matches") is True for b in merged))
    sl_b = gfile(w8, "data/source_links.json") or b""
    sl = jload(sl_b)
    la = led["cross_checks"].get("links_added") or {}
    check("C0b cross_checks.links_added == 新增 8 键 == source_links 实测",
          len(la) == 8 and set(la) == set(k for k in sl if k not in blinks))

    # ---------- C1: 四态重算（W8 锚点） ----------
    cnt = Counter((m.get("verification") or {}).get("status") for m in modes)
    check("C1a 全库四态重算 1018/1887/55/351（3311）",
          cnt.get("verified") == 1018 and cnt.get("pending") == 1887
          and cnt.get("suspect") == 55 and cnt.get("unverifiable") == 351 and sum(cnt.values()) == 3311)
    qset = load_quarantine()
    pub = Counter((m.get("verification") or {}).get("status") for m in modes
                  if str(m.get("figure_code")) not in qset)
    check("C1b 发布口径重算 1018/1855/38/340（3251）",
          pub.get("verified") == 1018 and pub.get("pending") == 1855
          and pub.get("suspect") == 38 and pub.get("unverifiable") == 340 and sum(pub.values()) == 3251)
    check("C1c 账本 after 与重算一致",
          fa.get("all", {}).get("verified") == 1018 and fa.get("all", {}).get("pending") == 1887
          and fa.get("all", {}).get("suspect") == 55 and fa.get("all_total") == 3311
          and fa.get("published", {}).get("pending") == 1855)

    # ---------- C2: 翻面（W8 锚点 vs 备份） ----------
    bstat = Counter((m.get("mode_code"), (m.get("verification") or {}).get("status")) for m in bmd["modes"])
    astat = Counter((m.get("mode_code"), (m.get("verification") or {}).get("status")) for m in modes)
    bset = {c for c, _ in bstat}
    aset = {c for c, _ in astat}
    check("C2a 模式集合与总量不变（3311 条 / 3302 码，含 10 条空码）",
          bset == aset and sum(bstat.values()) == 3311 and sum(astat.values()) == 3311)
    rem = bstat - astat
    addp = astat - bstat
    old_by, new_by = {}, {}
    for (c, s), n in rem.items():
        old_by.setdefault(c, []).append((s, n))
    for (c, s), n in addp.items():
        new_by.setdefault(c, []).append((s, n))
    trans = Counter()
    for c in set(old_by) | set(new_by):
        for s1, n1 in old_by.get(c, []):
            for s2, n2 in new_by.get(c, []):
                trans[(s1, s2)] += min(n1, n2)
    check("C2b 翻面重算 == 69 verified / 3 suspect（多重集差）",
          trans.get(("pending", "verified")) == 69 and trans.get(("pending", "suspect")) == 3
          and sum(trans.values()) == 72)
    item_codes = {str(i.get("mode_code")) for i in (led.get("items") or [])}
    flipped = set(old_by) | set(new_by)
    check("C2c 翻面全在包内、包外零翻面",
          flipped <= item_codes and (led["cross_checks"].get("side_effect_flips_outside_pack") == []))

    # ---------- C3: 引文零改写（QA 锚点账本 vs W8 数据） ----------
    midx = {}
    for m in modes:
        midx.setdefault(str(m.get("mode_code")), m)
    bad, compared = [], 0
    for it in led.get("items") or []:
        q = it.get("quote")
        m = midx.get(str(it.get("mode_code")))
        if q is None or m is None:
            continue
        dq = m.get("key_quote_zh") or m.get("key_quote")
        if dq == q:
            compared += 1
        else:
            bad.append(it.get("mode_code"))
    check("C3 154/154 引文与库内逐字一致（零改写）", compared == 154 and not bad, "bad=%s" % bad[:5])

    # ---------- C4: findings（W8 锚点 vs 备份） ----------
    fnd = jload(gfile(w8, "data/audit/findings.json") or b"{}")

    def fkey(f):
        return json.dumps(f, sort_keys=True, ensure_ascii=False)

    co, cn = Counter(fkey(f) for f in bfind["findings"]), Counter(fkey(f) for f in fnd["findings"])
    added = [json.loads(k) for k in cn if cn[k] > co.get(k, 0)]
    removed = [k for k in co if co[k] > cn.get(k, 0)]
    check("C4 findings 165→168 且仅 +3（M-WB-003/004/008 D4）",
          len(fnd["findings"]) == 168 and not removed and len(added) == 3
          and all(a.get("defect") == "D4_quote_mismatch" and a.get("mode_code") in ("M-WB-003", "M-WB-004", "M-WB-008") for a in added)
          and (fnd.get("summary") or {}).get("D4_quote_mismatch") == 27 and (fnd.get("summary") or {}).get("total") == 168)

    # ---------- C5: source_texts（W8 锚点 vs 备份 + W8 索引） ----------
    stxt = entries_map(jload(gfile(w8, "data/audit/source_texts.json") or b"{}"))
    idx = jload(gfile(w8, "data/audit/source_texts_w8_stage2_batch1.json") or b"{}")
    ix = {e.get("label"): e for e in idx.get("entries", [])}
    newk = [k for k in stxt if k not in bstxt]
    oldsame = all(json.dumps(stxt[k], sort_keys=True, ensure_ascii=False) == json.dumps(bstxt[k], sort_keys=True, ensure_ascii=False) for k in bstxt)
    newok = True
    for k in newk:
        ent = stxt[k]
        lab = k.strip("《》")
        e = ix.get(lab) or ix.get(k)
        if not e or ent.get("file") != e.get("file") or ent.get("sha256") != e.get("sha256"):
            newok = False
    check("C5 source_texts 97→114（+17 与 W8 索引逐条同源，旧 97 未动）",
          len(stxt) == 114 and len(newk) == 17 and oldsame and newok)

    # ---------- C6: source_links（W8 锚点 vs 备份） ----------
    newlinks = [k for k in sl if k not in blinks]
    oldlink_ok = all(json.dumps(sl[k], sort_keys=True, ensure_ascii=False) == json.dumps(blinks[k], sort_keys=True, ensure_ascii=False) for k in blinks)
    cl = ["理想国", "俄狄浦斯王", "伊利亚特", "奥德赛", "战争史", "形而上学", "奥林匹克回忆录", "诗学", "安提戈涅"]
    check("C6 source_links 383→391（+8 本书键；旧键未动；跨语言零链接）",
          len(sl) == 391 and len(newlinks) == 8 and oldlink_ok
          and not [k for k in newlinks if any(c in k for c in cl)]
          and (led["cross_checks"].get("cross_lang_linked") == []))

    # ---------- C7: siteCounts（W8 锚点） ----------
    sc_b = gfile(w8, "web/src/generated/siteCounts.ts") or b""
    sc = sc_b.decode("utf-8")
    sc_need = ["published: { verified: 1018, pending: 1845, suspect: 38, unverifiable: 340 }",
               "all: { verified: 1018, pending: 1877, suspect: 55, unverifiable: 351 }",
               "modes: 3241", "figures: 320", "modesWithLink: 1046",
               "citationsLinked: 1304", "citationsUnresolved: 2262"]
    check("C7 siteCounts 计数与 sha16 一致", all(s in sc for s in sc_need) and sha16b(sc_b) == "a698abe698bb3db3")

    # ---------- C8a: QA 文件镜面（发布仓现行） ----------
    if not PUBLISH.is_dir():
        check("C8a 发布仓可达", False, "缺 %s" % PUBLISH)
    else:
        okn = missn = 0
        badf = []
        for rel in QA_FILES:
            latest, lrc = git("log", "-1", "--format=%H", "--", rel, text=True)
            cb = gfile(latest.strip(), rel) if (lrc == 0 and latest.strip()) else gfile(commit, rel)
            pb = PUBLISH / rel
            if cb is None and not pb.exists():
                missn += 1
                continue
            if cb is None or not pb.exists():
                badf.append(rel)
                continue
            if sha16b(cb) == sha16f(pb):
                okn += 1
            else:
                badf.append(rel)
        check("C8a QA 文件镜面 byte-exact（%d 件；%d 件无历史版本）" % (okn, missn),
              not badf, "bad=%s" % badf)
        # ---------- C8b: W8 镜像回执（历史提交对） ----------
        names, _ = git("show", "--name-only", "--format=", MIRROR_W8, cwd=PUBLISH, text=True)
        f50 = [l.strip() for l in names.splitlines() if l.strip()]
        names2, _ = git("show", "--name-only", "--format=", MIRROR_W8FIX, cwd=PUBLISH, text=True)
        f2 = [l.strip() for l in names2.splitlines() if l.strip()]
        bad2 = []
        for rel in f50:
            a = gfile(MIRROR_W8, rel, cwd=PUBLISH)
            b = gfile(WS_W8, rel)
            if a is None or b is None or sha16b(a) != sha16b(b):
                bad2.append(rel)
        for rel in f2:
            a = gfile(MIRROR_W8FIX, rel, cwd=PUBLISH)
            b = gfile(WS_W8FIX, rel)
            if a is None or b is None or sha16b(a) != sha16b(b):
                bad2.append(rel)
        check("C8b W8 镜像回执 byte-exact（%d + %d 件）" % (len(f50), len(f2)),
              len(f50) >= 50 and len(f2) == 2 and not bad2, "bad=%s" % bad2[:4])
        if args.with_remote:
            h1, _ = git("rev-parse", "HEAD", cwd=PUBLISH, text=True)
            h2, _ = git("ls-remote", "origin", "refs/heads/main", cwd=PUBLISH, text=True)
            rsha = (h2.strip().split()[0] if h2.strip() else "")
            check("C9 push 面：发布仓 HEAD == ls-remote main", h1.strip() == rsha, "%s vs %s" % (h1.strip()[:12], rsha[:12]))

    # ---------- G: 门禁复跑（W8 锚点临时 worktree） ----------
    if args.with_gates or args.with_links:
        tmp = tempfile.mkdtemp(prefix="qa_w8_verify_")
        wt = Path(tmp) / "wt"
        _, rc = git("worktree", "add", "--detach", str(wt), wsha.strip(), text=True)
        if rc != 0:
            check("G worktree 建立", False, str(wt))
        else:
            try:
                runs = [("G1 credibility_gate --hard-fail", ["python3", "tools/credibility_gate.py", "--hard-fail"]),
                        ("G2 verify_findings --hard-fail", ["python3", "tools/verify_findings.py", "--hard-fail"]),
                        ("G3 apply_verification_status --check", ["python3", "tools/apply_verification_status.py", "--check"])]
                if args.with_links:
                    runs.append(("G4 verify_source_links --hard-fail", ["python3", "tools/verify_source_links.py", "--hard-fail"]))
                for name, cmd in runs:
                    r = subprocess.run(cmd, cwd=str(wt), capture_output=True)
                    check("%s rc=0" % name, r.returncode == 0, "rc=%d" % r.returncode)
            finally:
                git("worktree", "remove", "--force", str(wt), text=True)
                shutil.rmtree(tmp, ignore_errors=True)

    npass = sum(1 for _, ok, _ in RESULTS if ok)
    nfail = len(RESULTS) - npass
    print("== 汇总: %d PASS / %d FAIL ==" % (npass, nfail))
    return 1 if nfail else 0


if __name__ == "__main__":
    sys.exit(main())
