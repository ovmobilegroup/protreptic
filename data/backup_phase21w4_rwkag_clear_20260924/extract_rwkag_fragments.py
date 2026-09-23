#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""extract_rwkag_fragments.py - RW-KAG-1..27 清档前像片段提取/校验器 (卡 t_ee203180).

默认(校验): 从本备份盘前像逐字节重算 27 码片段 sha256, 与归档 JSON
docs/research/_archive/RW-KAG_1-27_archive.json 的 per_code_fragments 逐项比对.
提取模式: --extract RW-KAG-N --out DIR 将 6 类片段字节级落盘.

用法:
  python3 extract_rwkag_fragments.py
  python3 extract_rwkag_fragments.py --extract RW-KAG-1 --out /tmp/rwkag1
"""
import argparse, hashlib, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ARCHIVE = os.path.join(HERE, "../../docs/research/_archive/RW-KAG_1-27_archive.json")
CODES = ["RW-KAG-%d" % n for n in range(1, 28)]

def sha_b(b):
    return hashlib.sha256(b).hexdigest()

def entry_span(d, code):
    return ('"%s":%s,' % (code, json.dumps(d[code], ensure_ascii=False, separators=(',', ':')))).encode()

def load_fragments(code):
    old_zh = json.loads(open(os.path.join(HERE, "tools/json/scenarios_zh.json"), "rb").read())
    old_en = json.loads(open(os.path.join(HERE, "tools/json/scenarios_en.json"), "rb").read())
    old_cm = open(os.path.join(HERE, "tools/code_maps_en.json"), encoding="utf-8").read().splitlines(keepends=True)
    line = [l for l in old_cm if l.startswith('  "%s": "Andean/' % code)]
    assert len(line) == 1, code
    return {
        "scenarios_zh_entry": entry_span(old_zh, code),
        "scenarios_en_entry": entry_span(old_en, code),
        "code_maps_en_line": line[0].encode(),
        "draft": open(os.path.join(HERE, "tools/json/%s.json" % code), "rb").read(),
        "shard": open(os.path.join(HERE, "web/public/data/figures/%s.json" % code), "rb").read(),
        "root_twin": open(os.path.join(HERE, "%s.json" % code), "rb").read(),
    }

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--archive", default=ARCHIVE)
    ap.add_argument("--extract")
    ap.add_argument("--out")
    a = ap.parse_args()
    if a.extract:
        assert a.out, "--out required with --extract"
        os.makedirs(a.out, exist_ok=True)
        fr = load_fragments(a.extract)
        for k, b in fr.items():
            open(os.path.join(a.out, a.extract + "_" + k + (".txt" if k.endswith("line") else ".json")), "wb").write(b)
        print("extracted", a.extract, "->", a.out, {k: len(v) for k, v in fr.items()})
        return 0
    arch = json.load(open(a.archive, encoding="utf-8"))
    bad = []
    for c in CODES:
        row = arch["per_code_fragments"].get(c, {})
        fr = load_fragments(c)
        for k, b in fr.items():
            if row.get(k, {}).get("sha256") != sha_b(b):
                bad.append("%s:%s" % (c, k))
    print("fragments checked:", len(CODES), "x 6; mismatches:", len(bad), bad[:5])
    print("PASS" if not bad else "FAIL")
    return 0 if not bad else 1

if __name__ == "__main__":
    sys.exit(main())
