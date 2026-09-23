#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase21-R8 罗瑞卿链 提交/镜像/push 产物独立复核 (espinosa / 卡 t_65998945)

独立复核 (不以被验收方自述为结论, 一律以 git 对象 / 远端 ref / 文件实算为准):
  K1 工作仓提交文件集 == 回执报告声明白名单 (逐件集合比对, 名单外 0 / 缺失 0)
  K2 工作仓提交 × 发布仓镜像 逐件字节相等 (git blob 内容 sha256 实算)
  K3 镜像侧新增件 (镜像提交 - 工作仓提交 差集) 与工作仓对应件 byte-exact 复核
  K4 回执报告表列 sha256 与 git 对象实算值逐件对照 (回执自洽性核对, 非结论来源)
  K5 push 回执: git ls-remote 远端 ref 包含各镜像提交 (ancestry 实测)
  K6 零数据改动: 六件数据 sha256 == merge manifest.after; 0cbf6ab6..HEAD 数据路径 0 提交; 工作树 == HEAD
  K7 文档归档页 byte-exact (工作仓 × 发布仓) + 尺寸/行数登记
  K8 两仓 parity 复测: 本卡 QA 产物面 / LUORQ 命名路径 0 残留; 他卡在途差异逐条登记
用法: python3 verify_luorq_chain_recheck_espinosa.py
输出: docs/qa/phase21r8_luorq_qa_recheck_evidence/chain_commits_verify.json / .txt
退出码: 0 = 0 FAIL; 1 = 有 FAIL。
"""
import hashlib, io, json, os, re, subprocess, sys
from datetime import datetime

REPO = os.path.dirname(os.path.abspath(__file__))
PUB = "/opt/data/release/Protreptic-publish"
OUT = os.path.join(REPO, "docs/qa/phase21r8_luorq_qa_recheck_evidence")
RECEIPT = os.path.join(REPO, "docs/qa/phase21r8_luorq_receipt_report.md")
SURF6 = ["data/modes_data.json", "data/code_maps.json", "data/scenarios_zh.json",
         "data/scenarios_en.json", "data/scenario_tags.json", "data/figure_names.json"]
PAIRS = [
    {"label": "合并提交 t_2d15bd2e#1 (卡 t_08bbb73d 结果选择性入库)", "ws": "0cbf6ab6", "pub": "ec0a06b"},
    {"label": "回执提交 t_2d15bd2e#2 (报告/证据补记)", "ws": "a119ad9c", "pub": "fee63a3"},
    {"label": "文档归档提交 t_d9cb98bb (九节档案首次装配)", "ws": "63a0e463", "pub": "2b3681d"},
]
PAGE = "docs/figures/H-LUORQ-001.md"
NOW = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

PASS, FAIL, INFO = [], [], []

def check(cid, desc, cond, detail=""):
    (PASS if cond else FAIL).append({"id": cid, "desc": desc, "detail": str(detail)[:400]})
    print("%s %-4s %s%s" % ("PASS" if cond else "FAIL", cid, desc,
                            (" | " + str(detail)[:300]) if detail else ""), flush=True)
    return bool(cond)

def note(msg):
    INFO.append(msg); print("INFO  " + msg, flush=True)

def sh(cmd, cwd=None):
    r = subprocess.run(cmd, cwd=cwd, capture_output=True)
    return r.returncode, r.stdout, r.stderr

def blob_bytes(repo, spec):
    rc, out, _ = sh(["git", "cat-file", "blob", spec], cwd=repo)
    return out if rc == 0 else None

def blob_sha256(repo, spec):
    b = blob_bytes(repo, spec)
    return None if b is None else hashlib.sha256(b).hexdigest()

def name_status(repo, commit):
    rc, out, err = sh(["git", "show", "--name-status", "--format=", commit], cwd=repo)
    rows = []
    for ln in out.decode("utf-8", "replace").split("\n"):
        ln = ln.rstrip()
        if not ln.strip():
            continue
        parts = ln.split("\t")
        if len(parts) >= 2:
            rows.append((parts[0].strip(), parts[-1].strip()))
    return rows

def rev(repo, prefix):
    rc, out, _ = sh(["git", "rev-parse", prefix], cwd=repo)
    return out.decode().strip() if rc == 0 else None

def file_sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest() if os.path.exists(path) else None

def parse_receipt_tables(path):
    src = io.open(path, encoding="utf-8").read()
    t1, t2 = {}, {}
    cur = None
    for ln in src.split("\n"):
        if ln.startswith("## 1"):
            cur = t1; continue
        if ln.startswith("## 2"):
            cur = t2; continue
        if ln.startswith("## 3"):
            cur = None; continue
        m = re.match(r"^\|\s*`([^`]+)`\s*\|\s*`([0-9a-f]{64})`\s*\|", ln)
        if m and cur is not None:
            cur[m.group(1)] = m.group(2)
    return t1, t2

def main():
    os.makedirs(OUT, exist_ok=True)
    res = {"card": "t_65998945", "script": "verify_luorq_chain_recheck_espinosa.py", "ts": NOW}
    print("==== Phase21-R8 罗瑞卿链 提交产物独立复核 [espinosa/t_65998945] @ %s ====" % NOW, flush=True)

    ws_head = rev(REPO, "HEAD"); pub_head = rev(PUB, "HEAD")
    ws_porc = sh(["git", "status", "--porcelain"], cwd=REPO)[1].decode("utf-8", "replace")
    pub_porc = sh(["git", "status", "--porcelain"], cwd=PUB)[1].decode("utf-8", "replace")
    ws_lines = [l for l in ws_porc.split("\n") if l.strip()]
    pub_lines = [l for l in pub_porc.split("\n") if l.strip()]
    note("状态钉扎: workspace HEAD=%s (porcelain %d 行); publish HEAD=%s (porcelain %d 行)"
         % (ws_head[:12], len(ws_lines), pub_head[:12], len(pub_lines)))
    res["state"] = {"workspace_head": ws_head, "publish_head": pub_head,
                    "ws_porcelain": len(ws_lines), "pub_porcelain": len(pub_lines)}

    wl_commit, wl_mirror = parse_receipt_tables(RECEIPT)
    note("回执表解析: 工作仓白名单 %d 件; 镜像清单 %d 件 (仅作比对靶, 结论取 git 实算)" % (len(wl_commit), len(wl_mirror)))

    res["pairs"] = {}
    for p in PAIRS:
        wsc = rev(REPO, p["ws"]); pubc = rev(PUB, p["pub"])
        wsf = name_status(REPO, wsc) if wsc else []
        pubf = name_status(PUB, pubc) if pubc else []
        wset = set(x[1] for x in wsf); pset = set(x[1] for x in pubf)
        tag = p["label"]
        check("K0", "%s: 双仓提交均可解析 (%s / %s)" % (tag, (wsc or "?")[:12], (pubc or "?")[:12]), bool(wsc and pubc))
        common = sorted(wset & pset)
        mism, miss_pub = [], []
        for rel in common:
            a = blob_sha256(REPO, "%s:%s" % (wsc, rel))
            b = blob_sha256(PUB, "%s:%s" % (pubc, rel))
            if a != b:
                mism.append(rel)
        ws_only = sorted(wset - pset)
        pub_only = sorted(pset - wset)
        check("K2", "%s: 提交×镜像 逐件字节相等 (%d/%d)" % (tag, len(common) - len(mism), len(common)),
              not mism, "不一致: %s" % mism[:5])
        if ws_only:
            note("K2 %s: 镜像缺件 %d 件: %s" % (tag, len(ws_only), ws_only[:8]))
        res["pairs"][p["ws"]] = {"ws_commit": wsc, "pub_commit": pubc, "common": len(common),
                                 "mismatch": mism, "ws_only": ws_only, "pub_only": pub_only}
        # K3 镜像侧新增件与工作仓对应件复核
        if pub_only:
            bad3, ok3, absent3 = [], [], []
            for rel in pub_only:
                bp = blob_sha256(PUB, "%s:%s" % (pubc, rel))
                ws_equiv = rev(REPO, "HEAD:%s" % rel)
                if ws_equiv:
                    a = blob_sha256(REPO, "HEAD:%s" % rel)
                elif os.path.exists(os.path.join(REPO, rel)):
                    a = file_sha(os.path.join(REPO, rel))
                else:
                    absent3.append(rel); continue
                (ok3 if a == bp else bad3).append(rel)
            check("K3", "%s: 镜像侧新增 %d 件与工作仓对应件 byte-exact (%d 件)" % (tag, len(pub_only), len(ok3)),
                  not bad3 and not absent3, "不一致: %s 缺工作仓对应: %s" % (bad3[:3], absent3[:3]))

    # K1 白名单集合核对 (针对 0cbf6ab6)
    wsc = rev(REPO, "0cbf6ab6")
    commit_set = set(x[1] for x in name_status(REPO, wsc))
    check("K1", "0cbf6ab6 提交文件集 == 回执声明白名单 21 件 (名单外 0 / 缺失 0)",
          set(wl_commit) == commit_set and len(commit_set) == 21,
          "commit=%d, 声明=%d, 名单外=%s, 缺失=%s" % (len(commit_set), len(wl_commit),
                                                     sorted(commit_set - set(wl_commit))[:5],
                                                     sorted(set(wl_commit) - commit_set)[:5]))
    # K4 回执表 sha 与 git 实算
    bad4 = []
    for rel in sorted(set(wl_commit) & commit_set):
        a = blob_sha256(REPO, "%s:%s" % (wsc, rel))
        if a != wl_commit[rel]:
            bad4.append(rel)
    check("K4", "回执表 sha256 与 0cbf6ab6 git 对象实算逐件一致 (%d 件)" % len(set(wl_commit) & commit_set),
          not bad4, bad4[:5])
    pubc = rev(PUB, "ec0a06b")
    bad4b = []
    for rel in sorted(set(wl_mirror) & set(x[1] for x in name_status(PUB, pubc))):
        b = blob_sha256(PUB, "%s:%s" % (pubc, rel))
        if b != wl_mirror[rel]:
            bad4b.append(rel)
    check("K4b", "回执镜像表 sha256 与 ec0a06b git 对象实算逐件一致 (%d 件)" % len(set(wl_mirror)),
          not bad4b, bad4b[:5])

    # K5 push 回执: 远端 ref
    rc, out, err = sh(["git", "ls-remote", "origin"], cwd=PUB)
    remote_main = None
    remote_all = []
    for ln in out.decode().split("\n"):
        if not ln.strip():
            continue
        sha, refname = ln.split("\t")
        remote_all.append(ln.strip())
        if refname == "refs/heads/main":
            remote_main = sha
    note("K5 远端 refs: %s" % (remote_all if remote_all else "空/不可达"))
    res["push"] = {"remote_main": remote_main, "remote_refs": remote_all}
    if remote_main:
        for p in PAIRS:
            pubc = rev(PUB, p["pub"])
            ok = subprocess.run(["git", "merge-base", "--is-ancestor", pubc, remote_main], cwd=PUB).returncode == 0 if pubc else False
            check("K5", "push 回执 %s (%s): 远端 main 含该镜像提交" % (p["pub"], p["label"][:24]), ok, "远端 main=%s" % remote_main[:12])
        check("K5b", "工作仓 master push 目标不存在 (远端无 refs/heads/master, 仅 refs/heads/main; 环境事实)",
              not any(r.endswith("refs/heads/master") for r in remote_all), str(remote_all))
    else:
        check("K5", "远端 ref 可达", False, "ls-remote 不可达: %s" % err.decode()[:120])

    # K6 零数据改动
    mm = json.load(io.open(os.path.join(REPO, "data/audit/phase21r8_luorq_merge_manifest.json"), encoding="utf-8"))
    aft = {k: v["sha256"] for k, v in mm["after"].items() if k in SURF6}
    bad6a, bad6b = [], []
    for rel in SURF6:
        wt = file_sha(os.path.join(REPO, rel))
        reg = aft.get(rel)
        if wt != reg:
            bad6a.append((rel, (wt or "?")[:12], (reg or "?")[:12]))
        hd = blob_sha256(REPO, "HEAD:%s" % rel)
        if hd != wt:
            bad6b.append(rel)
    check("K6a", "工作树六件数据 sha256 == merge manifest.after 逐件", not bad6a, bad6a[:4])
    check("K6b", "工作树六件 == HEAD 对象 (无未提交数据改动)", not bad6b, bad6b[:4])
    rc, out, _ = sh(["git", "log", "--format=%h %s", "0cbf6ab6..HEAD", "--"] + SURF6, cwd=REPO)
    after_commits = [l for l in out.decode().split("\n") if l.strip()]
    check("K6c", "0cbf6ab6..HEAD 六件数据路径 0 提交 (补交后无数据改动)", not after_commits, after_commits[:3])
    bad6d = []
    for rel in SURF6:
        a = blob_sha256(REPO, "%s:%s" % (wsc, rel))
        if a != aft.get(rel):
            bad6d.append(rel)
    check("K6d", "0cbf6ab6 提交内六件数据 == merge manifest.after 逐件", not bad6d, bad6d[:4])
    res["zero_data_change"] = {"worktree_vs_manifest": bad6a, "worktree_vs_head": bad6b,
                               "commits_after": after_commits, "commit_vs_manifest": bad6d}

    # K7 文档归档页
    wpage = os.path.join(REPO, PAGE); ppage = os.path.join(PUB, PAGE)
    wsh = file_sha(wpage); psh = file_sha(ppage)
    lines = len(io.open(wpage, encoding="utf-8").read().split("\n")) if os.path.exists(wpage) else 0
    check("K7", "文档归档页 byte-exact (工作仓 × 发布仓) 且非空",
          bool(wsh) and wsh == psh and lines > 100,
          "ws=%s pub=%s bytes=%d lines=%d" % ((wsh or "?")[:16], (psh or "?")[:16],
                                              os.path.getsize(wpage) if os.path.exists(wpage) else 0, lines))
    res["page"] = {"sha256": wsh, "publish_sha256": psh,
                   "bytes": os.path.getsize(wpage) if os.path.exists(wpage) else 0, "lines": lines}

    # K8 两仓 parity 复测 (本卡覆盖面 0 残留; 他卡在途逐条登记)
    MY_PATHS = ["docs/qa/phase21r8_luorq_qa_evidence", "docs/qa/phase21r8_luorq_qa_gates",
                "docs/qa/phase21r8_luorq_qa_selftest.json", "docs/qa/phase21r8_luorq_qa_recheck_evidence",
                "docs/qa/phase21r8_luorq_qa_recheck_gates", "docs/qa/phase21r8_luorq_qa_recheck_selftest.json",
                "docs/qa/phase21r8_luorq_qa_recheck_report.md",
                "verify_luorq_qa_espinosa.py", "verify_luorq_chain_recheck_espinosa.py"]
    rc8, out8, err8 = sh(["python3", "tools/check_repo_parity.py", "--json"], cwd=REPO)
    pdiffs = []
    try:
        pj = json.loads(out8.decode("utf-8"))
        pdiffs = pj.get("diffs", [])
    except Exception as e:
        note("K8 parity json 解析失败: %s" % e)
    _mine_all = [d for d in pdiffs if any(d["path"].startswith(pp) or d["path"] == pp for pp in MY_PATHS)]
    mine = [d for d in _mine_all if "/parity_postmirror/" not in d["path"]]
    mine_inflight = [d for d in _mine_all if "/parity_postmirror/" in d["path"]]
    lz = [d for d in pdiffs if "luorq" in d["path"].lower() and "/parity_postmirror/" not in d["path"]]
    others = [d for d in pdiffs if d not in _mine_all]
    check("K8a", "两仓 parity: 本卡 QA 产物面 0 残留 (差异总 %d)" % len(pdiffs), not mine,
          [d["path"] for d in mine][:6])
    check("K8b", "两仓 parity: LUORQ 命名路径 0 残留", not lz, [d["path"] for d in lz][:6])
    note("K8 回执采集件在制: %d 件 (parity_postmirror, 随后提交)" % len(mine_inflight))
    note("K8 parity exit=%d; 差异 %d 条 (他卡在途/前置漂移, 逐条登记前 60)" % (rc8, len(pdiffs)))
    for d in others[:60]:
        note("K8   %s %s [%s]" % (d.get("kind"), d["path"], d.get("reason", "")))
    res["parity"] = {"exit": rc8, "diffs": len(pdiffs), "mine": [d["path"] for d in mine],
                     "luorq_named": [d["path"] for d in lz],
                     "others": [{"path": d["path"], "kind": d.get("kind"), "reason": d.get("reason")} for d in others]}

    res["pass"] = len(PASS); res["fail"] = len(FAIL); res["checks"] = PASS + FAIL
    with io.open(os.path.join(OUT, "chain_commits_verify.json"), "w", encoding="utf-8") as f:
        f.write(json.dumps(res, ensure_ascii=False, indent=2, default=str))
    with io.open(os.path.join(OUT, "chain_commits_verify.txt"), "w", encoding="utf-8") as f:
        f.write("==== 罗瑞卿链 提交产物独立复核 [espinosa/t_65998945] @ %s ====\n" % NOW)
        for d in PASS:
            f.write("PASS  %-4s %s | %s\n" % (d["id"], d["desc"], d["detail"]))
        for d in FAIL:
            f.write("FAIL  %-4s %s | %s\n" % (d["id"], d["desc"], d["detail"]))
        for i in INFO:
            f.write("INFO  %s\n" % i)
    print("==== 总结: %d PASS / %d FAIL / %d INFO ====" % (len(PASS), len(FAIL), len(INFO)), flush=True)
    if FAIL:
        for d in FAIL:
            print("  %s %s | %s" % (d["id"], d["desc"], d["detail"]))
    return 0 if not FAIL else 1

if __name__ == "__main__":
    sys.exit(main())
