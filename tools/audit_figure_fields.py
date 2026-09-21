#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""audit_figure_fields.py - figure 文件字段缺陷全量审计 (Phase46-R / 卡 t_e3f8cf8f)

产出: data/audit/figure_field_defects.json (逐文件记录 + 修复建议 + 待人工核名清单)

四类缺陷 (卡面口径)
    empty_name      : figure_name 字段缺失/为空 -- 该人物从人名表里消失
    bad_figure_code : figure_code 不等于规范值. 规范 = 文件名主干 H-<CODE>-001
                      (与 id / 根 modes_data.json 的 figure code 同形).
                      实测脏值三类: 朝代或时代 (战国 / 春秋 / 明 / 东汉 / Modern / Han /
                      WarringStates), 人物名锚点 (Bach / DaVinci / Amundsen ...),
                      H-XXX 缺序号 (H-DZS), 整字段缺失 (None).
    name_mismatch   : figure_name 与文件内证据冲突 (正文首名 / 拼音 / 英文名 / id 锚点).
                      只有拿到文件内证据才改; 拿不到证据的一律进待人工核名, 禁止臆造.
    duplicate       : 同一个人物两份文件 (判据: 归一化人名相同 + 生卒年相同或内容逐字节相同).

另记非四类的观察项 (不改数据, 只登记):
    companion_*     : data/figures/ 下的 *_modes.json 伴随模式包. 仓库既有约定
                      (tools/credibility_gate.py 的 figure_key_candidates 明确支持
                      <stem>_modes.json 伴随文件), 不是文件名异常, 故不改名
                      (卡面第 5 条前提与仓库约定不符, 详见报告).
    data_quality    : 正文内年份/生卒年明显损坏 (如 H-ZS-001 正文 前505-57617935年)
                      -- 改生卒年会动 D5 判定, 属另一条线, 本卡只登记.

用法:
    python3 tools/audit_figure_fields.py            # 写 data/audit/figure_field_defects.json
    python3 tools/audit_figure_fields.py --print    # 只打印摘要, 不写文件
"""
from __future__ import annotations

import argparse
import collections
import datetime
import glob
import hashlib
import json
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIG_DIR = os.path.join(REPO, "data", "figures")
OUT = os.path.join(REPO, "data", "audit", "figure_field_defects.json")
MODES = os.path.join(REPO, "data", "modes_data.json")

STEM_RE = re.compile(r"^H-[A-Za-z0-9]+-\d{3}$")
CJK = re.compile(r"^[\u4e00-\u9fff\u00b7]+$")
LATIN_WORD = re.compile(r"^[A-Za-z][A-Za-z'\-]*$")
SHORT_CODE = re.compile(r"^H-[A-Za-z0-9]+$")
SEP = re.compile(r"[\s\u00b7\uff0e.\u3000]")

# 已人工裁定的 name_mismatch: 每条都给文件内证据
CONFIRMED_NAME_MISMATCH = {
    "H-Mendel-001.json": (
        "\u5b5f\u5fb7\u5c14",
        "historical_significance 首句 [孟德尔(1822-1884), 奥地利奥古斯丁会修士, 遗传学之父]; "
        "id=H-MENDEL-001 / code=Mendel; figure_pinyin='Shi Nai Geng' 与 name='施耐庚' 同为整体误写",
    ),
    "H-AlGhazali-001.json": (
        "\u963f\u658b\u900a",
        "historical_significance 首句 [阿斋逊(1058-1111), 伊斯兰黄金时代思想家...]; "
        "原 name='加括友' 与 pinyin='Jia Ku You' 为杜撰读音. 同人文件 H-GHZ-163.json 用正式名"
        "[安萨里](Al-Ghazali), 是否统一为安萨里留待船长裁定 -> 同时进待核名清单",
    ),
    "H-Heisenberg-001.json": (
        "\u6d77\u68ee\u5821",
        "historical_significance 全文为 Werner Karl Heisenberg (1901-1976), uncertainty principle, "
        "1932 诺贝尔物理学奖; figure_pinyin='He Sen Bei' 即海森堡; id/code/figure_code 均为 Heisenberg. "
        "原 name='海瑞'(明代官员 1514-1587) 与生卒年 1901-1976 及正文均冲突",
    ),
    "H-Heisenberg-001.json": (
        "\u6d77\u68ee\u5821",
        "与 H-Heisenberg-001.json 逐字节相同的重复文件, 同证据",
    ),
}

# 待人工核名的存疑项 (有名字但对不上任何外部锚点, 禁止臆造, 故不改)
SUSPECT_NAMES = {
    "H-HAN-001.json": "name='沈幅'/en='Shen Fu'/生卒年=-100~180, 三者互不吻合; 疑似沈复(清,1763-1830) "
                      "但文件内无证据, 且生卒年本身不可信 -> 不改, 待人工核名",
    "H-YE-001.json": "name='叶筱', 正文只有泛泛描述 (birth/death=1900/1975 无出处) -> 不改, 待人工核名",
    "H-AlGhazali-001.json": "改后名阿斋逊出自本文件正文, 但与同人文件 H-GHZ-163.json 的正式名安萨里不一致 "
                            "-> 是否统一待裁定",
}

DATA_QUALITY_NOTES = {
    "H-ZS-001.json": ("body-year-corrupted",
                      "historical_significance 内 [曾子(前505-57617935年)], 年份字段本身为 -505/-435 (正常) "
                      "-- 正文年份损坏, 修它属引证/文本治理线"),
    "H-HAN-001.json": ("suspect-name",
                      "name='沈幅'/en='Shen Fu' 与生卒年 -100~180 三者互不吻合; 疑似沈复(清,1763-1830) 但文件内无证据 "
                      "-> 不改名, 进待人工核名清单"),
    "H-MZ-001_modes.json": ("lifespan-key-collision",
                            "fc='战国' 且 birth/death=-372/-289, 与主文件 H-MZ-001.json(1890/1990) 在键 'H-MZ-001' 上冲突 "
                            "(credibility_gate 整体丢弃该键) -- 伴随包不属 figure 文件, 本卡不动"),
}


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def declared_name(doc):
    return str(doc.get("figure_name") or "").strip()


def in_file_name(doc):
    for k in ("figure_name_zh", "name_zh", "figure_name", "name"):
        v = doc.get(k)
        if isinstance(v, str) and v.strip():
            return v.strip(), k
    return "", ""


def body_lead_name(doc):
    sig = str(doc.get("historical_significance") or doc.get("summary_zh") or "")
    m = re.match(r"^([\u4e00-\u9fff\u00b7]{2,9})[\uff08(\uff0c,\s]", sig)
    return m.group(1) if m else ""


def normalize_name(s):
    return SEP.sub("", str(s or "").strip())


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def year_key(*vals):
    """生卒年归一化: 数字/字符串/约/公元前 统一成可比字符串; 解析不出返回原样。"""
    out = []
    for v in vals:
        if v in (None, ""):
            out.append("?")
            continue
        digits = re.sub(r"[^0-9]", "", str(v))
        out.append(digits.lstrip("0") or "0" if digits else str(v))
    return "|".join(out)


def code_alias_set(doc, stem):
    keys = []
    for cand in [doc.get(f) for f in ("code", "id", "figure_code")] + [stem]:
        if isinstance(cand, str) and cand.strip() and cand.strip() not in keys:
            keys.append(cand.strip())
    return keys


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--print", dest="dry", action="store_true")
    ap.add_argument("--out", default=OUT, help="输出路径(默认 data/audit/figure_field_defects.json)")
    ap.add_argument("--fig-dir", default=FIG_DIR,
                    help="figure 目录(默认 data/figures); 传 HEAD 版本副本即可复现修复前审计")
    args = ap.parse_args()

    fig_dir = args.fig_dir
    files = sorted(os.path.basename(p) for p in glob.glob(os.path.join(fig_dir, "*.json")))
    figure_files = [f for f in files if not f.endswith("_modes.json")]
    companion_files = [f for f in files if f.endswith("_modes.json")]

    modes = load_json(MODES)["modes"]
    mode_fc = collections.Counter(str(m.get("figure_code") or "") for m in modes)
    mode_name_of = {}
    for m in modes:
        fc = str(m.get("figure_code") or "")
        nm = str(m.get("figure_name") or "").strip()
        if fc and nm and fc not in mode_name_of:
            mode_name_of[fc] = nm

    docs = {}
    for fn in files:
        try:
            docs[fn] = load_json(os.path.join(fig_dir, fn))
        except Exception as e:
            print("[warn] unreadable: %s (%s)" % (fn, e), file=sys.stderr)

    defects = []

    def add(**kw):
        defects.append(kw)

    # ---------- 1. empty_name ----------
    for fn in files:
        doc = docs[fn]
        if declared_name(doc):
            continue
        stem = fn[:-5]
        nm, src_field = in_file_name(doc)
        proposed, evidence = None, ""
        if fn.endswith("_modes.json"):
            evidence = "伴随模式包(非 figure 文件), 不进 figure_name 回填范围"
        elif nm:
            proposed = nm
            evidence = "%s=%r" % (src_field, nm)
        else:
            lead = body_lead_name(doc)
            if lead:
                proposed = lead
                evidence = "historical_significance 首名=%r" % lead
        add(file=fn, figure_name=doc.get("figure_name"), figure_code=doc.get("figure_code"),
            code=doc.get("code"), defect_class="empty_name",
            detail="figure_name 缺失或为空",
            in_file_name=nm, in_file_field=src_field,
            body_lead=body_lead_name(doc),
            mode_side_name=(mode_name_of.get(str(doc.get("figure_code") or ""))
                            or mode_name_of.get(str(doc.get("code") or ""))
                            or mode_name_of.get(stem)),
            evidence=evidence,
            proposed_fix=({"field": "figure_name", "value": proposed} if proposed else None),
            status="fixable" if proposed else "needs_human")

    # ---------- 2. bad_figure_code ----------
    for fn in figure_files:
        doc = docs[fn]
        stem = fn[:-5]
        fc = doc.get("figure_code")
        fcs = "" if fc is None else str(fc).strip()
        if fcs == stem:
            continue
        if fcs == "":
            sub = "missing"
        elif fcs in ("\u6218\u56fd", "\u6625\u79cb", "\u660e", "\u4e1c\u6c49", "\u897f\u6c49", "\u79e6",
                     "\u6c49", "\u5510", "\u5b8b", "\u5143", "\u6e05", "\u4e09\u56fd"):
            sub = "dynasty"
        elif fcs in ("Modern", "MODERN", "Han", "WarringStates", "Ancient", "Medieval", "MODERN-EARLY"):
            sub = "era_name"
        elif CJK.match(fcs):
            sub = "place_or_era"
        elif LATIN_WORD.match(fcs):
            sub = "person_name_anchor"
        elif SHORT_CODE.match(fcs):
            sub = "short_code_no_seq"
        else:
            sub = "other"
        others = [a for a in code_alias_set(doc, stem) if a != fcs]
        keep_alias = bool(fcs) and mode_fc.get(fcs, 0) > 0 and fcs not in others
        fix = {"field": "figure_code", "value": stem}
        if keep_alias:
            fix["alias_field"] = "code"
            fix["alias_value"] = fcs
        add(file=fn, figure_name=doc.get("figure_name") or doc.get("figure_name_zh"),
            figure_code=fc, code=doc.get("code"), defect_class="bad_figure_code",
            detail="figure_code=%r 非规范(应为 %r); 子类=%s" % (fcs or None, stem, sub),
            subtype=sub,
            mode_refs=int(mode_fc.get(fcs, 0)),
            preserve_alias=(fcs if keep_alias else None),
            evidence="文件名主干=%r; id=%r; code=%r" % (stem, doc.get("id"), doc.get("code")),
            proposed_fix=fix,
            status="fixable")

    # ---------- 3. name_mismatch ----------
    for fn in figure_files:
        doc = docs[fn]
        name = declared_name(doc) or str(doc.get("figure_name_zh") or "").strip()
        if not name:
            continue
        lead = body_lead_name(doc)
        hit_a = bool(lead) and lead not in normalize_name(name) and normalize_name(name) not in lead
        if fn in CONFIRMED_NAME_MISMATCH and name != CONFIRMED_NAME_MISMATCH[fn][0]:
            new_name, ev = CONFIRMED_NAME_MISMATCH[fn]
            add(file=fn, figure_name=doc.get("figure_name"), figure_code=doc.get("figure_code"),
                code=doc.get("code"), defect_class="name_mismatch",
                detail="figure_name=%r 与文件内证据冲突 -> 应为 %r" % (name, new_name),
                evidence=ev,
                proposed_fix={"field": "figure_name", "value": new_name},
                status="fixable")
        elif hit_a:
            add(file=fn, figure_name=doc.get("figure_name"), figure_code=doc.get("figure_code"),
                code=doc.get("code"), defect_class="name_mismatch",
                detail="正文首名 %r 与声明名 %r 不一致" % (lead, name),
                evidence="historical_significance 首名=%r" % lead,
                proposed_fix=None,
                status="needs_human" if fn in SUSPECT_NAMES else "false_positive",
                verdict=SUSPECT_NAMES.get(fn, "非缺陷: 正文首句为身份描述语(如 两度获诺贝尔奖 / 精神分析学的创始人 "
                                               "等), 不是人名; 或为同一人的写法变体(如 居鲁士大帝 / 居鲁士二世)"))

    # ---------- 4. duplicate ----------
    groups = collections.defaultdict(list)
    for fn in figure_files:
        doc = docs[fn]
        nm = normalize_name(declared_name(doc) or doc.get("figure_name_zh") or doc.get("name_zh"))
        en = normalize_name(doc.get("figure_name_en") or doc.get("name_en"))
        for k in ((("zh", nm) if nm else None), (("en", en.lower()) if en else None)):
            if k:
                groups[k].append(fn)
    merged = {}
    for k, v in groups.items():
        if len(v) < 2:
            continue
        merged.setdefault(tuple(sorted(v)), []).append(k)
    # 补充判据: 人物名锚点相同(卡面给的 巴哈/巴赫 就靠这条才查得出来 —— 两份文件的中文名差一个字,
    # 归一化人名并不相等, 但 figure_code/code 锚点都是 'Bach'、生卒年都是 1685-1750)
    era_words = {"Modern", "MODERN", "Han", "WarringStates", "Ancient", "Medieval", "MODERN-EARLY"}
    anchors = collections.defaultdict(list)
    for fn in figure_files:
        doc = docs[fn]
        for a_ in (doc.get("figure_code"), doc.get("code")):
            a_s = a_.strip() if isinstance(a_, str) else ""
            if a_s and a_s not in era_words and LATIN_WORD.match(a_s) and fn not in anchors[a_s.lower()]:
                anchors[a_s.lower()].append(fn)
    for a_s, v in anchors.items():
        if len(v) > 1:
            merged.setdefault(tuple(sorted(v)), []).append(["anchor", a_s])
    duplicates = []
    for members, keys in sorted(merged.items()):
        info = []
        for fn in members:
            doc = docs[fn]
            info.append({
                "file": fn,
                "size": os.path.getsize(os.path.join(fig_dir, fn)),
                "keys": len(doc),
                "sha256": sha256(os.path.join(fig_dir, fn)),
                "years": [doc.get("birth_year"), doc.get("death_year")],
                "years_key": year_key(doc.get("birth_year"), doc.get("death_year")),
                "has_modes": bool(doc.get("modes") or doc.get("mode_ids") or doc.get("thinking_modes")),
                "aliases": code_alias_set(doc, fn[:-5]),
                "figure_name": declared_name(doc) or doc.get("figure_name_zh") or doc.get("name_zh"),
                "figure_code": doc.get("figure_code"),
                "code": doc.get("code"),
            })
        yrs = {year_key(*i["years"]) for i in info}
        shas = {i["sha256"] for i in info}
        identical, same_years = len(shas) == 1, len(yrs) == 1
        verdict = "confirmed" if (identical or same_years) else "name-match-years-differ"
        ranked = sorted(info, key=lambda i: (-i["size"], -i["keys"], 0 if i["has_modes"] else 1, i["file"]))
        survivor, redundants = ranked[0], ranked[1:]
        plan = []
        for r in redundants:
            unique = [a for a in r["aliases"] if a not in survivor["aliases"]]
            live = [a for a in unique if mode_fc.get(a, 0) > 0]
            plan.append({
                "file": r["file"],
                "unique_aliases": unique,
                "mode_referenced_aliases": live,
                "action": "defer" if live else "archive",
                "reason": ("其取值键 %s 仍被 %d 条模式引用 -- 移走会让这些模式找不到主体(figures/生卒年), "
                           "须与 code 改名 + 模式侧同步同批处理" % (live, sum(mode_fc[a] for a in live)))
                          if live else
                          ("全部取值键都被保留者覆盖(%s), 可安全归档" % (", ".join(survivor["aliases"]))),
            })
        duplicates.append({
            "group_keys": [list(k) for k in keys],
            "verdict": verdict,
            "identical_files": identical,
            "same_years": same_years,
            "members": info,
            "survivor": survivor["file"],
            "redundants": plan,
        })
        for p in plan:
            add(file=p["file"], figure_name=None, figure_code=None, code=None,
                defect_class="duplicate",
                detail="与 %s 为同一人物(%s); 处置=%s" % (survivor["file"], verdict, p["action"]),
                evidence=p["reason"],
                proposed_fix=({"action": "archive",
                               "to": "data/figures/_duplicates/%s" % p["file"]}
                              if p["action"] == "archive" else None),
                status="fixable" if p["action"] == "archive" else "needs_human")

    # ---------- 5. 观察项(非四类) ----------
    companions = []
    for fn in companion_files:
        doc = docs[fn]
        companions.append({
            "file": fn,
            "figure_code": doc.get("figure_code"),
            "code": doc.get("code"),
            "main_file_exists": os.path.exists(os.path.join(fig_dir, fn[:-len("_modes.json")] + ".json")),
            "note": "仓库既有约定: tools/credibility_gate.py 的 figure_key_candidates / load_figure_lifespans "
                    "显式支持 <stem>_modes.json 伴随文件(主文件先, 伴随包后) -> 不算文件名异常, 本卡不改名",
        })
    observations = [{"file": k, "kind": v[0], "note": v[1]} for k, v in sorted(DATA_QUALITY_NOTES.items())]

    # ---------- 6. mode -> figure 一致性(引用面) ----------
    all_aliases = set()
    for fn in figure_files:
        for a in code_alias_set(docs[fn], fn[:-5]):
            all_aliases.add(a)
            all_aliases.add(a.upper())
    unresolved = []
    for fc, n in sorted(mode_fc.items()):
        if not fc:
            continue
        if fc not in all_aliases and fc.upper() not in all_aliases:
            unresolved.append({"figure_code": fc, "modes": n, "mode_side_name": mode_name_of.get(fc)})

    payload = {
        "schema": "protreptic.figure_field_defects/v1",
        "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
        "generator": "tools/audit_figure_fields.py",
        "card": "t_e3f8cf8f",
        "scope": {
            "figures_dir": "data/figures",
            "json_total": len(files),
            "figure_files": len(figure_files),
            "companion_modes_files": len(companion_files),
            "mode_records": len(modes),
            "mode_distinct_figure_code": len([c for c in mode_fc if c]),
        },
        "canonical_rule": {
            "figure_code": "等于文件名主干 H-<CODE>-001(与 id 及根 modes_data.json 的 figure code 同形)",
            "figure_name": "非空中文人名, 且必须与文件内正文/拼音/英文名/id 锚点一致",
            "note": "改动 figure_code 时, 若旧值仍被模式引用, 必须把旧值保留在 code 字段(取值键不丢)",
        },
        "class_counts": dict(collections.Counter(d["defect_class"] for d in defects)),
        "defects": defects,
        "duplicates": duplicates,
        "companion_modes_files": companions,
        "observations": observations,
        "mode_to_figure_unresolved": unresolved,
        "needs_human": [d for d in defects if d.get("status") == "needs_human"],
    }

    cc = payload["class_counts"]
    print("figure 文件 %d(另伴随模式包 %d); 模式记录 %d 条 / 不同 figure_code %d 个"
          % (len(figure_files), len(companion_files), len(modes), payload["scope"]["mode_distinct_figure_code"]))
    for k in ("empty_name", "bad_figure_code", "name_mismatch", "duplicate"):
        print("  %-16s %d" % (k, cc.get(k, 0)))
    print("  重复组 %d(确认 %d / 同名不同人 %d)"
          % (len(duplicates), sum(1 for d in duplicates if d["verdict"] == "confirmed"),
             sum(1 for d in duplicates if d["verdict"] != "confirmed")))
    print("  待人工核名 %d; 模式->figure 无法定位的 figure_code %d 个(%d 条模式)"
          % (len(payload["needs_human"]), len(unresolved), sum(u["modes"] for u in unresolved)))
    if args.dry:
        return 0
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print("OK 写入 %s (%d bytes)" % (args.out, os.path.getsize(args.out)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
