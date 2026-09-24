#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""R9 安子介素材包复核脚本：见证 sha256 + 引文逐条复跑（无需联网）。

用法：python3 docs/scratch/phase21r9_anzijie/verify_quotes.py
返回：0 = 全绿；1 = 存在失败项（逐项打印）。
"""
import hashlib
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPORT = os.path.normpath(os.path.join(HERE, "..", "..", "research", "phase21r9_anzijie_sourcing_report.json"))
WIT = os.path.join(HERE, "witness")


def norm(s):
    return re.sub(r"\s+", "", s)


fails = []
d = json.load(open(REPORT, encoding="utf-8"))

for w in d["witnesses"]:
    fp = os.path.join(WIT, os.path.basename(w["file"]))
    if not os.path.exists(fp):
        fails.append("MISSING " + w["w"])
        continue
    h = hashlib.sha256(open(fp, "rb").read()).hexdigest()
    if h != w["sha256"]:
        fails.append("SHA256 " + w["w"])

skip = {"专利页字段", "疑似级引文（词条转述）"}
n = 0
for m in d["modes"]:
    for qq in m["quotes"]:
        if qq.get("note") in skip:
            continue
        n += 1
        fn = [w for w in d["witnesses"] if w["w"] == qq["w"]][0]["file"]
        fp = os.path.join(WIT, os.path.basename(fn))
        if norm(qq["text"]) not in norm(open(fp, encoding="utf-8").read()):
            fails.append("QUOTE " + m["id"] + " " + qq["w"])

print("witnesses:", len(d["witnesses"]), "| quotes checked:", n)
if fails:
    print("FAIL:", len(fails))
    for f in fails:
        print("  -", f)
    sys.exit(1)
print("ALL GREEN (sha256 11/11 + quotes %d/%d)" % (n, n))
