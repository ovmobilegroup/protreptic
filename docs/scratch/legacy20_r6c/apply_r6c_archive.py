#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase21-R6C 归档执行脚本（卡 t_4a9cf2cb）——一次性操作，逐件守卫。

动作
  0 快照与守卫：22 源件存在 / 22 归档目标不存在 / modes_data.json 冻结值记录
  1 字节归档：22 件 -> data/figures/_duplicates/（先复制、sha256 逐件复核；不删字节）
  2 活跃层清档：tracked 源件 git rm；untracked 用 os.remove（不引入第三方目录）
  3 自件登记撤下：figure_names 9 键 / code_maps 3 条目 / scenarios_zh+en 自件条目（按 figure_id 扫描）
  4 产出：manifest + removed_registrations（撤下内容逐字保留）
卫生：主库 data/modes_data.json 零写入（前后 sha 断言）；共享文件保留原格式（indent=2 + 末尾换行，
      已实测 load/dump 往返与原件字节一致，diff 仅撤下条目）。
重跑说明：一次性脚本——源件已清档后重跑会 ABORT（需先从 _duplicates 复原）。
"""
import hashlib
import json
import os
import subprocess
import sys

ROOT = "/opt/data/workspace/Protreptic"
DUP = "data/figures/_duplicates"
SK = "docs/scratch/legacy20_r6c"
DATE = "20260923"
CODES = ["H-AN-001", "H-LC-001", "H-YE-001", "H-ZOU-001", "H-HAN-001", "H-MODERN-002", "H-LUORQ-001"]

FILES = [
    ("data/figures/H-AN-001.json", "H-AN-001_figures.json"),
    ("data/individuals/H-AN-001.json", "H-AN-001_individuals.json"),
    ("data/individuals/H-AN-001_modes.json", "H-AN-001_individuals_modes.json"),
    ("docs/figures/H-AN-001.md", "H-AN-001_archive_page.md"),
    ("data/figures/H-LC-001.json", "H-LC-001_figures.json"),
    ("data/individuals/H-LC-001.json", "H-LC-001_individuals.json"),
    ("data/individuals/H-LC-001_modes.json", "H-LC-001_individuals_modes.json"),
    ("data/figures/H-YE-001.json", "H-YE-001_figures.json"),
    ("data/individuals/H-YE-001_modes.json", "H-YE-001_individuals_modes.json"),
    ("data/figures/H-ZOU-001.json", "H-ZOU-001_figures.json"),
    ("data/individuals/H-ZOU-001_modes.json", "H-ZOU-001_individuals_modes.json"),
    ("docs/figures/H-ZOU-001.md", "H-ZOU-001_archive_page.md"),
    ("data/figures/H-HAN-001.json", "H-HAN-001_figures.json"),
    ("data/individuals/H-HAN-001.json", "H-HAN-001_individuals.json"),
    ("data/individuals/H-HAN-001_modes.json", "H-HAN-001_individuals_modes.json"),
    ("data/figures/H-MODERN-002.json", "H-MODERN-002_figures.json"),
    ("data/individuals/H-MODERN-002.json", "H-MODERN-002_individuals.json"),
    ("data/individuals/H-MODERN-002_modes.json", "H-MODERN-002_individuals_modes.json"),
    ("data/figures/H-LUORQ-001.json", "H-LUORQ-001_figures.json"),
    ("data/individuals/H-LUORQ-001.json", "H-LUORQ-001_individuals.json"),
    ("data/individuals/H-LUORQ-001_modes.json", "H-LUORQ-001_individuals_modes_ISOLATED_crossfile.json"),
    ("docs/figures/H-LUORQ-001.md", "H-LUORQ-001_archive_page.md"),
]

FN_KEYS = ["H-AN-001", "H-LC-001", "H-YE-001", "H-ZOU-001", "H-HAN-001", "Han", "HAN", "H-MODERN-002", "H-LUORQ-001"]
CM_KEYS = ["H-ZOU-001", "H-MODERN-002", "H-LUORQ-001"]
SC_FILES = ["data/scenarios_zh.json", "data/scenarios_en.json"]
SC_EXPECT = 30  # 每文件：ZOU 10 + MODERN-002 10 + LUORQ 10（zh 与 en 各自命名）


def sha256b(b):
    return hashlib.sha256(b).hexdigest()


def readb(rel):
    return open(os.path.join(ROOT, rel), "rb").read()


def git(*args):
    r = subprocess.run(["git"] + list(args), cwd=ROOT, capture_output=True, text=True)
    return r.returncode, (r.stdout or "").strip(), (r.stderr or "").strip()


def is_tracked(rel):
    rc, _, _ = git("ls-files", "--error-unmatch", "--", rel)
    return rc == 0


def dump_json(rel, obj):
    b = (json.dumps(obj, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    open(os.path.join(ROOT, rel), "wb").write(b)
    return sha256b(b)


manifest = {"schema": "protreptic.r6c_archive_manifest/v1", "card": "t_4a9cf2cb", "date": DATE,
            "files": [], "shared": {}, "modes_data_freeze": {}, "notes": []}
removed = {"schema": "protreptic.r6c_removed_registrations/v1", "card": "t_4a9cf2cb", "date": DATE,
           "figure_names": {}, "code_maps": {}, "scenarios": {}}

# ---------- 0 快照与守卫 ----------
for src, _ in FILES:
    if not os.path.exists(os.path.join(ROOT, src)):
        sys.exit("ABORT 源缺失: " + src)
for _, tgt in FILES:
    if os.path.exists(os.path.join(ROOT, DUP, tgt)):
        sys.exit("ABORT 归档目标已存在: " + tgt)
MODES_PRE = sha256b(readb("data/modes_data.json"))
XSHA = {}
for rel in ["data/figure_names.json", "data/code_maps.json"] + SC_FILES:
    XSHA[rel] = sha256b(readb(rel))
print("[0] 守卫通过：22 源件在场、22 目标无占用、modes_data=%s" % MODES_PRE[:12])

# ---------- 1 字节归档 ----------
for src, tgt in FILES:
    b = readb(src)
    tpath = os.path.join(ROOT, DUP, tgt)
    with open(tpath, "wb") as f:
        f.write(b)
    got = sha256b(open(tpath, "rb").read())
    if got != sha256b(b):
        sys.exit("ABORT 归档字节复核失败: " + src)
    manifest["files"].append({"source": src, "target": DUP + "/" + tgt, "bytes": len(b),
                              "sha256": got, "source_tracked": is_tracked(src)})
    print("[1] 归档 %-42s -> %s (%d B)" % (src, tgt, len(b)))

# ---------- 2 活跃层清档 ----------
for src, _ in FILES:
    if is_tracked(src):
        rc, out, err = git("rm", "-q", "--", src)
        if rc != 0:
            sys.exit("ABORT git rm 失败: %s %s" % (src, err))
    else:
        os.remove(os.path.join(ROOT, src))
print("[2] 清档完成：22 源件移出活跃层")

# ---------- 3 自件登记撤下 ----------
fn_rel = "data/figure_names.json"
fn = json.loads(readb(fn_rel).decode("utf-8"))
for k in FN_KEYS:
    if k not in fn:
        sys.exit("ABORT figure_names 缺键: " + k)
    removed["figure_names"][k] = fn.pop(k)
manifest["shared"][fn_rel] = {"pre_sha256": XSHA[fn_rel], "post_sha256": dump_json(fn_rel, fn),
                              "removed_keys": len(FN_KEYS)}
print("[3] figure_names 撤下 %d 键" % len(FN_KEYS))

cm_rel = "data/code_maps.json"
cm = json.loads(readb(cm_rel).decode("utf-8"))
for k in CM_KEYS:
    e = cm["figures"].pop(k, None)
    if e is None:
        sys.exit("ABORT code_maps 缺条目: " + k)
    removed["code_maps"][k] = e
manifest["shared"][cm_rel] = {"pre_sha256": XSHA[cm_rel], "post_sha256": dump_json(cm_rel, cm),
                              "removed_entries": len(CM_KEYS)}
print("[3] code_maps 撤下 %d 条目" % len(CM_KEYS))


def sweep(node, bucket):
    n = 0
    for k in list(node.keys()):
        v = node[k]
        if isinstance(v, dict) and v.get("figure_id") in CODES:
            bucket[k] = v
            del node[k]
            n += 1
    return n


for sc_rel in SC_FILES:
    sc = json.loads(readb(sc_rel).decode("utf-8"))
    bucket = {}
    n = sweep(sc, bucket)
    for k, v in list(sc.items()):
        if isinstance(v, dict):
            n += sweep(v, bucket)
    removed["scenarios"][sc_rel] = bucket
    if n != SC_EXPECT:
        sys.exit("ABORT scenarios 撤下条数异常: %s 实得 %d 期望 %d" % (sc_rel, n, SC_EXPECT))
    manifest["shared"][sc_rel] = {"pre_sha256": XSHA[sc_rel], "post_sha256": dump_json(sc_rel, sc),
                                  "removed_entries": n}
    print("[3] %s 撤下 %d 条" % (sc_rel, n))

# ---------- 4 冻结断言与产出 ----------
MODES_POST = sha256b(readb("data/modes_data.json"))
if MODES_POST != MODES_PRE:
    sys.exit("ABORT modes_data.json 被写入（冻结违例）")
manifest["modes_data_freeze"] = {"pre_sha256": MODES_PRE, "post_sha256": MODES_POST, "changed": False}
manifest["notes"].append("共享文件保留原格式 dump（indent=2 + 末尾换行），diff 仅撤下条目；撤下原文逐字见 removed_registrations.json")
with open(os.path.join(ROOT, SK, "r6c_archive_manifest.json"), "w", encoding="utf-8") as f:
    json.dump(manifest, f, ensure_ascii=False, indent=1)
    f.write("\n")
with open(os.path.join(ROOT, SK, "removed_registrations.json"), "w", encoding="utf-8") as f:
    json.dump(removed, f, ensure_ascii=False, indent=1)
    f.write("\n")
print("[4] manifest / removed_registrations 已产出")
print("DONE")
