#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""fix_figure_fields.py - 按审计结论修 figure 文件字段 (Phase46-R / 卡 t_e3f8cf8f)

输入: data/audit/figure_field_defects.json (由 tools/audit_figure_fields.py 产出)
产出: data/audit/figure_field_fix_manifest.json (逐文件 old->new + 前后 sha256, 可回溯)

原则
  1. 只改字段值, 不新增/删除人物内容; 文本级定点替换 -> 除目标字段外的字节原样保留
     (不整文件 json 重排, 避免把 indent=1/2、末尾换行等既有风格改掉产生无谓 diff)
  2. 只应用 status=fixable 且给出 proposed_fix 的条目; needs_human 一律不动
  3. figure_code 规范化的引用保护: 若旧值仍被模式引用, 审计要求把它写进 code 字段
     (tools/credibility_gate.py 的 figure_key_candidates 会把 code 登记为取值键) -> 引用不丢
  4. duplicate: 仅归档 action=archive 者(其全部取值键都被保留者覆盖, 且无模式引用),
     移到 data/figures/_duplicates/ (该目录不在任何 figures/*.json glob 内) -> 用 git mv, 内容零丢失

用法
    python3 tools/fix_figure_fields.py --dry-run     # 只打印将要做的改动(默认)
    python3 tools/fix_figure_fields.py --apply       # 真正落盘
"""
from __future__ import annotations

import argparse
import datetime
import json
import os
import re
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIG_DIR = os.path.join(REPO, "data", "figures")
AUDIT = os.path.join(REPO, "data", "audit", "figure_field_defects.json")
MANIFEST = os.path.join(REPO, "data", "audit", "figure_field_fix_manifest.json")
ARCHIVE_DIR = os.path.join(FIG_DIR, "_duplicates")


def detect_indent(raw):
    m = re.match(r"\{\n( +)\"", raw)
    return m.group(1) if m else "  "


def json_value(v):
    return json.dumps(v, ensure_ascii=False)


def replace_field(raw, field, value, indent):
    """定点替换 顶层 field 的值; 返回 (新文本, 旧值, 是否命中)。

    两种口径: (1) 行首 + 精确缩进(多行 JSON, 只看顶层字段, 不会误伤嵌套同名键);
    (2) 单行 JSON 兜底: 剥掉行首锚点, 但要求该键在文本里只出现一次(防误伤嵌套)。
    """
    pat = re.compile(r'(?m)^(' + re.escape(indent) + r'"' + re.escape(field) +
                     r'")(\s*:\s*)(null|"(?:[^"\\]|\\.)*")')
    m = pat.search(raw)
    if not m:
        loose = re.compile(r'("' + re.escape(field) + r'")(\s*:\s*)(null|"(?:[^"\\]|\\.)*")')
        if raw.count('"' + field + '"') != 1:
            return raw, None, False
        m = loose.search(raw)
        if not m:
            return raw, None, False
        pat = loose
    old_txt = m.group(3)
    if old_txt == "null":
        old = None
    else:
        try:
            old = json.loads(old_txt)
        except Exception:
            old = old_txt
    new = pat.sub(lambda mm: mm.group(1) + mm.group(2) + json_value(value), raw, count=1)
    return new, old, True


def insert_field(raw, field, value, indent, after=("figure_name_zh", "name_zh", "code", "id", "schema_version")):
    """在 after 列表里第一个存在的顶层字段之后插入新字段(保持既有缩进)。"""
    for anchor in after:
        pat = re.compile(r'(?m)^(' + re.escape(indent) + r'"' + re.escape(anchor) +
                         r'"\s*:\s*(?:null|"(?:[^"\\]|\\.)*"|[^,\n]+)),?$')
        m = pat.search(raw)
        if not m:
            continue
        line = m.group(0)
        ins = indent + '"' + field + '": ' + json_value(value)
        body = line.rstrip()
        if body.endswith(","):
            repl = body + "\n" + ins + ","
        else:
            repl = body + ",\n" + ins
        return raw.replace(line, repl, 1), True
    # 兜底 1: 单行 JSON -> 紧跟开头的 { 插入(紧凑风格)
    if "\n" not in raw and raw.lstrip().startswith("{") and raw.rstrip().endswith("}"):
        pos = raw.index("{") + 1
        tail = raw[pos:].lstrip()
        if tail.startswith("}"):
            return raw[:pos] + '"' + field + '": ' + json_value(value) + raw[pos:], True
        return raw[:pos] + '"' + field + '": ' + json_value(value) + ", " + tail, True
    # 兜底 2: 闭合大括号独占一行 -> 在其前追加(作为最后一个字段)
    m = re.search(r"(?m)^([ \t]*)\}\s*$", raw)
    if m:
        close = m.group(0)
        before = raw[:m.start()]
        ins = indent + '"' + field + '": ' + json_value(value) + "\n"
        if before.rstrip().endswith("{"):
            return before + ins + close, True
        return before.rstrip() + ",\n" + ins + close, True
    return raw, False


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def write(path, text):
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text)


def sha256_text(t):
    import hashlib
    return hashlib.sha256(t.encode("utf-8")).hexdigest()


def reference_safe_alias(doc, new_fc, mode_fc, fn, skipped):
    """figure_code 规范化的引用保护.

    改 fc 之前先算出该文件当前的取值键集合(tools/credibility_gate.py 口径:
    code / id / figure_code / 文件名主干), 其中被模式引用的那些键在改完之后必须仍有人提供,
    否则那些模式会失去生卒年与 figure 主体. code 字段是唯一可安全承载旧值的位置
    (credibility_gate 会把它登记为取值键).

    返回 (ok, alias): alias 为要写进 code 的值(None = 不需要动 code); ok=False 表示放弃本文件.
    """
    fc_old = str(doc.get("figure_code") or "").strip()
    code_old = str(doc.get("code") or "").strip()
    idv = str(doc.get("id") or "").strip()
    stem = new_fc
    live = {k for k in (fc_old, code_old, idv, stem) if k and mode_fc.get(k)}
    base = {idv, stem} - {""}
    if not live:
        return True, None
    if live <= base:
        return True, None
    if live <= (base | {fc_old}):
        return True, fc_old
    if live <= (base | {code_old}):
        return True, code_old
    skipped.append({"file": fn, "field": "figure_code", "reason":
                    "取值键 %s 同时被模式引用, code 字段只装得下一处 -> 跳过本文件(改 fc 必丢引用), 待人工"
                    % sorted(live)})
    return False, None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="真正落盘(缺省为 dry-run)")
    ap.add_argument("--dry-run", action="store_true", help="显式 dry-run(与缺省相同)")
    ap.add_argument("--audit", default=AUDIT)
    args = ap.parse_args()

    audit = json.load(open(args.audit, encoding="utf-8"))
    modes = json.load(open(os.path.join(REPO, "data", "modes_data.json"), encoding="utf-8"))["modes"]
    mode_fc = {}
    for m in modes:
        fc = str(m.get("figure_code") or "")
        if fc:
            mode_fc[fc] = mode_fc.get(fc, 0) + 1

    planned = {}   # file -> {"changes": [(field, value, evidence)], "sha_before": ...}
    archived = []
    deferred = []
    skipped = []

    for d in audit["defects"]:
        fn = d["file"]
        st = d.get("status")
        cls = d["defect_class"]
        if cls == "duplicate":
            if st == "fixable" and d.get("proposed_fix", {}).get("action") == "archive":
                archived.append({"file": fn, "to": d["proposed_fix"]["to"], "reason": d.get("evidence", "")})
            else:
                deferred.append({"file": fn, "class": cls, "reason": d.get("evidence", "")})
            continue
        if st != "fixable" or not d.get("proposed_fix"):
            if st == "needs_human":
                deferred.append({"file": fn, "class": cls, "reason": d.get("detail", "")})
            continue
        pf = d["proposed_fix"]
        field, value = pf["field"], pf["value"]
        entry = planned.setdefault(fn, {"changes": []})
        pairs = [(field, value)]
        if cls == "bad_figure_code":
            docx = json.load(open(os.path.join(FIG_DIR, fn), encoding="utf-8"))
            ok, alias = reference_safe_alias(docx, value, mode_fc, fn, skipped)
            if not ok:
                planned.pop(fn, None)
                continue
            if alias:
                pairs.append(("code", alias))
        for (f, v) in pairs:
            if any(x[0] == f for x in entry["changes"]):
                if [x for x in entry["changes"] if x[0] == f][0][1] != v:
                    skipped.append({"file": fn, "field": f, "reason": "同一字段被两条审计条目给出不同目标值"})
                continue
            entry["changes"].append((f, v, d.get("evidence") or d.get("detail") or ""))

    archived_files = {a["file"] for a in archived}
    planned = {k: v for k, v in planned.items()
               if v["changes"] and k not in archived_files and not any(s["file"] == k for s in skipped)}

    print("计划改动文件 %d 个 / 归档 %d 个 / 待人工 %d 条 / 跳过 %d 条"
          % (len(planned), len(archived), len(deferred), len(skipped)))
    for s in skipped:
        print("  [skip] %s %s: %s" % (s["file"], s["field"], s["reason"]))

    manifest = {
        "schema": "protreptic.figure_field_fix_manifest/v1",
        "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
        "generator": "tools/fix_figure_fields.py",
        "card": "t_e3f8cf8f",
        "applied": bool(args.apply),
        "audit_input": os.path.relpath(args.audit, REPO),
        "files_changed": [],
        "archived": [],
        "deferred": deferred,
        "skipped": skipped,
    }

    for fn in sorted(planned):
        path = os.path.join(FIG_DIR, fn)
        raw = read(path)
        indent = detect_indent(raw)
        rec = {"file": fn, "sha256_before": sha256_text(raw), "changes": []}
        new = raw
        failed = None
        pending = []
        for f, v, ev in planned[fn]["changes"]:
            new2, old, hit = replace_field(new, f, v, indent)
            if not hit:
                new2, ins = insert_field(new, f, v, indent)
                if not ins:
                    failed = f
                    break
                old = None
            new = new2
            pending.append({"field": f, "old": old, "new": v, "evidence": ev})
        if failed:
            # 原子性: 任一字段写不进去 -> 整文件放弃(避免半套改动把引用改坏)
            skipped.append({"file": fn, "field": failed,
                            "reason": "字段不存在且插入失败 -> 整文件放弃(不做半套改动)"})
            continue
        rec["changes"] = pending
        if new == raw:
            skipped.append({"file": fn, "field": "-", "reason": "定点替换后文本无变化 -> 未写盘"})
            continue
        rec["sha256_after"] = sha256_text(new)
        manifest["files_changed"].append(rec)
        if args.apply:
            write(path, new)

    os.makedirs(ARCHIVE_DIR, exist_ok=True)
    for a in archived:
        src = os.path.join(FIG_DIR, a["file"])
        dst = os.path.join(ARCHIVE_DIR, a["file"])
        rec = {"file": a["file"], "to": os.path.relpath(dst, REPO), "reason": a["reason"],
               "sha256": sha256_text(read(src))}
        manifest["archived"].append(rec)
        if args.apply:
            subprocess.run(["git", "-C", REPO, "mv", src, dst], check=True,
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    m = manifest
    if args.apply:
        with open(MANIFEST, "w", encoding="utf-8") as f:
            json.dump(m, f, ensure_ascii=False, indent=2)
            f.write("\n")
        print("OK 写入 %s" % MANIFEST)
    print("  字段改动文件 %d; 归档 %d" % (len(m["files_changed"]), len(m["archived"])))
    return 0


if __name__ == "__main__":
    sys.exit(main())
