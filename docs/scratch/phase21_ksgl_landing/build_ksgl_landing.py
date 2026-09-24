#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build_ksgl_landing.py - Phase 21 麻赫穆德·喀什噶里 (H-KSGL-001) 落盘包生成器（卡 t_06017753）

背景（为什么由合并卡生成落盘包）
    上游落地卡 t_43e4872a 只写入 data/individuals 两件，且字段映射存在缺陷
    （读取 name_zh/mode_name_zh 等键名错位，正文全空壳，18 键 legacy 壳）。
    研究卡 t_1eb78b6b 的 attachments 两件为完整 v6 产出（27 键模式条目）。
    本生成器以研究产出为唯一内容源，构造：
      * modes_library_entries.json（10 条，逐字等于研究产出 modes）
      * combined_library_entries.json / id_mapping.tsv / category_mapping.tsv（台账）
      * top_block_proposal.json（23 键顶层块提案，供合并写入 modes_data.json）
      * scenario_notes.json（场景前缀与模板规则登记）
      * figures/H-KSGL-001.json、figures/H-KSGL-001_modes.json
      * individuals/H-KSGL-001.json、individuals/H-KSGL-001_modes.json
      * data/audit/phase21_ksgl_landing_manifest.json（sha256 台账）
    幂等：重跑结果字节一致（内容确定性，无时间戳字段）。

用法（仓库根）:
    python3 docs/scratch/phase21_ksgl_landing/build_ksgl_landing.py
"""
from __future__ import annotations

import hashlib
import io
import json
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
SRC_DIR = "/opt/data/kanban/boards/protreptic/attachments/t_1eb78b6b"
SRC_FIG = os.path.join(SRC_DIR, "H-KSGL-001.json")
SRC_MODES = os.path.join(SRC_DIR, "H-KSGL-001_modes.json")
LAND = os.path.join(REPO, "docs/scratch/phase21_ksgl_landing")
FIGURE = "H-KSGL-001"
FIGNAME = "麻赫穆德·喀什噶里"
CODES = ["M-KSGL-%03d" % i for i in range(1, 11)]
SCODES = ["C-KSGL-%03d" % i for i in range(1, 11)]
SCODES_E = ["C-KSGL-%03dE" % i for i in range(1, 11)]
KEYS27 = [
    "id", "mode_code", "figure_code", "figure_name", "name_zh", "name_en",
    "category", "category_raw", "domain_zh", "domain_en", "level", "priority",
    "definition_zh", "definition_en", "source_chapter", "key_concepts",
    "key_quote_zh", "key_quote_en", "process_zh", "process_en",
    "representative_cases_zh", "representative_cases_en",
    "modern_applications_zh", "modern_applications_en", "related_modes",
    "legacy_mode_id", "verification",
]
KEY23 = ["schema_version", "code", "name_zh", "name_en", "era", "historical_domains", "domains", "core_modes",
         "gender", "ethnicity", "nationality", "civilization_sphere", "time_period_standardized", "primary_language",
         "intellectual_tradition", "unique_thinking_zh", "unique_thinking_en", "mode_evidence", "key_texts",
         "key_concepts", "intellectual_lineage", "legacy_assessment", "scholarly_value"]
# 研究产出锚（attachments 与 workspace 两件 sha 实测一致；见 landing manifest sources）
SRC_FIG_SHA = "45b68ad1e1ca487a883082b3299f6465087119f83ccdf963e02efc2a2371429a"
SRC_MODES_SHA = "3c596ee8b3bb5f661cc9dbabe387d9f5ce1e7ba3ee143661ddc33468823740c1"


def sha_bytes(b):
    return hashlib.sha256(b).hexdigest()


def sha_file(p):
    with io.open(p, "rb") as f:
        return sha_bytes(f.read())


def load(p):
    with io.open(p, encoding="utf-8") as f:
        return json.load(f)


def dump(obj):
    return (json.dumps(obj, ensure_ascii=False, indent=1) + "\n").encode("utf-8")


def write(rel, data):
    p = os.path.join(REPO, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with io.open(p, "wb") as f:
        f.write(data)
    return p


def main():
    # ---------- 源校验 ----------
    assert sha_file(SRC_FIG) == SRC_FIG_SHA, "研究产出 figure sha 不符"
    assert sha_file(SRC_MODES) == SRC_MODES_SHA, "研究产出 modes sha 不符"
    srcfig = load(SRC_FIG)
    srcmodes = load(SRC_MODES)
    entries = srcmodes["modes"]
    assert len(entries) == 10 and [e["mode_code"] for e in entries] == CODES, "研究产出码序不符"
    for e in entries:
        ekeys = set(e.keys())
        if ekeys != set(KEYS27):
            print("[DBG] entry mode_code=%s keys_diff extra_in_entry=%s missing_from_KEY27=%s" % (
                e["mode_code"],
                sorted(ekeys - set(KEYS27)),
                sorted(set(KEYS27) - ekeys)))
        assert ekeys == set(KEYS27), "键集不符: %s" % e["mode_code"]
        assert e["id"] == e["mode_code"] and e["figure_code"] == FIGURE and e["figure_name"] == FIGNAME
        assert e.get("legacy_mode_id") == "", "legacy_mode_id 非空"
        assert (e.get("verification") or {}).get("status") == "pending", "verification 非 pending"

    # ---------- 1. 条目面 ----------
    entries_out = json.loads(json.dumps(entries, ensure_ascii=False))  # 逐字副本
    write("docs/scratch/phase21_ksgl_landing/modes_library_entries.json", dump(entries_out))
    combined = {"schema_version": "v6", "code": FIGURE, "figure_name_zh": FIGNAME,
                "figure_name_en": srcfig["figure_name_en"], "mode_count": 10, "modes": entries_out}
    write("docs/scratch/phase21_ksgl_landing/combined_library_entries.json", dump(combined))
    idmap = ["new_code\tlegacy_mode_id"] + ["%s\t" % e["mode_code"] for e in entries]
    write("docs/scratch/phase21_ksgl_landing/id_mapping.tsv", ("\n".join(idmap) + "\n").encode("utf-8"))
    catmap = ["mode_code\tcategory_raw\tcategory"] + ["%s\t%s\t%s" % (e["mode_code"], e["category_raw"], e["category"]) for e in entries]
    write("docs/scratch/phase21_ksgl_landing/category_mapping.tsv", ("\n".join(catmap) + "\n").encode("utf-8"))

    # ---------- 2. 顶层块提案（23 键） ----------
    top = {
        "schema_version": "v6",
        "code": FIGURE,
        "name_zh": "麻赫穆德·喀什噶里：突厥语大词典·田野采录·方言比较",
        "name_en": "Mahmud al-Kashgari: The Diwan · Field Collection · Comparative Dialectology",
        "era": "喀喇汗王朝/Kara-Khanid Khanate (1005-1102)",
        "historical_domains": ["突厥学与比较辞书学", "语言田野调查与方言学", "中亚历史地理与民族志", "口传文学保存", "制图与百科整合"],
        "domains": ["突厥学", "比较辞书学", "语言田野调查", "中亚民族志", "口传文学保存"],
        "core_modes": list(CODES),
        "gender": "Male",
        "ethnicity": "突厥（喀喇汗王朝王室支系） / Turkic (Kara-Khanid royal line)",
        "nationality": "喀喇汗王朝（今中国新疆—中亚） / Kara-Khanid Khanate (present-day Xinjiang, China - Central Asia)",
        "civilization_sphere": "伊斯兰—突厥世界/阿拔斯知识圈 / Islamo-Turkic World / Abbasid Learned Sphere",
        "time_period_standardized": "1005-1102 CE",
        "primary_language": "阿拉伯语（著作）/ 突厥诸方言（记录对象） / Arabic (composition) / Turkic dialects (recorded)",
        "intellectual_tradition": "伊斯兰语言学与阿拉伯辞书学（哈利勒·伊本·艾哈迈德传统）/突厥学奠基 / Islamic linguistics and Arabic lexicography / founding of Turkology",
        "unique_thinking_zh": (
            "麻赫穆德·喀什噶里（约1005—1102），喀喇汗王室支系，出身巴尔思汗（今伊塞克湖南岸）地方统治者家庭；"
            "约1057年因宫廷政变流亡，以十五至二十年游历突厥诸部，1072—1077年在巴格达以阿拉伯语编成《突厥语大词典》，"
            "献给阿拔斯哈里发穆克塔迪。其思路可提炼十法：田野实证采集（亲历亲录替代书斋转述）／方言比较标注"
            "（二十部族谱系＋逐词方言归属＋方言分级）／框架移植改造（以阿拉伯辞书学《阿因书》为蓝本而改其体例）／"
            "文明对等论证（「两匹赛马」并驾齐驱）／战略需求定位（以受众语言面向权力中心与读者）／百科整合编纂"
            "（词典兼收历史、地理、民俗）／口传活态保存（谚语、挽歌、史诗以写存口）／制图化认知表达"
            "（以巴拉沙衮为圆心的世界地图）／语言考古重构（词源、名物与口头记忆互证）／学习者导向教学编排"
            "（先语法后词典、由简入繁）。生卒、出生地与词条总数诸说并存，按 caveats 分层登记。"
        ),
        "unique_thinking_en": (
            "Mahmud al-Kashgari (c.1005-1102), of a collateral branch of the Kara-Khanid royal line, born to a local "
            "ruling family at Barsgan (south shore of Lake Issyk-Kul); after a palace coup c.1057 he wandered the "
            "Turkic lands for fifteen to twenty years, and in 1072-1077 compiled in Baghdad, in Arabic, the Diwan "
            "Lughat al-Turk, dedicated to the Abbasid caliph al-Muqtadi. Ten methods may be distilled: field "
            "empirical collection (first-hand record over second-hand compilation) / comparative dialect annotation "
            "(a twenty-tribe taxonomy, word-by-word attribution, graded dialects) / framework transplantation "
            "(modelled on Arabic lexicography's Kitab al-Ayn, its form remade) / civilizational parity argument "
            "(two horses in a race) / strategic positioning (speaking to the centre in its own language) / "
            "encyclopedic integration (the dictionary admits history, geography and folklore) / oral heritage "
            "preservation (proverbs, elegies and epics fixed in writing) / cartographic worldview (a world map "
            "centred on Balasagun) / linguistic archaeology (etymology, name-lore and oral memory cross-checked) / "
            "learner-oriented design (grammar before dictionary, simple to complex). Variants on his dates, "
            "birthplace and entry counts are registered in the caveats."
        ),
        "mode_evidence": [
            {"mode_id": "M-KSGL-001", "example_zh": "十五年以上的实地穿行与母语者采录（《词典》前言；Dankoff & Kelly 1982, vol.1）",
             "example_en": "Over fifteen years of travel and native-speaker collection (preface of the Diwan; Dankoff & Kelly 1982)"},
            {"mode_id": "M-KSGL-002", "example_zh": "二十部族自西向东谱系与逐词方言标注（DLT「突厥部落论」节）",
             "example_en": "The twenty-tribe west-to-east sequence and word-by-word annotation (DLT, On the Turkic Tribes)"},
            {"mode_id": "M-KSGL-003", "example_zh": "以哈利勒·伊本·艾哈迈德《阿因书》为蓝本而改其体例（DLT 前言）",
             "example_en": "Modelled on al-Khalil ibn Ahmad's Kitab al-Ayn, with a remade arrangement (preface)"},
            {"mode_id": "M-KSGL-004", "example_zh": "「两匹赛马」总纲性论证：以竞赛隐喻替代尊卑隐喻（Dankoff 1975/1982）",
             "example_en": "The master argument of two horses in a race (Dankoff 1975/1982)"},
            {"mode_id": "M-KSGL-005", "example_zh": "以流亡者的学术工程进入巴格达——靠近权力、读者与赞助（TDK 条目等）",
             "example_en": "Carrying the project to Baghdad as an exile - close to power, readers and patronage (TDK entries)"},
            {"mode_id": "M-KSGL-006", "example_zh": "词条即门户：谱系传说、二十部落方位与方言地理并收（DLT）",
             "example_en": "Entries as portals: genealogy, tribal geography and dialect geography together (DLT)"},
            {"mode_id": "M-KSGL-007", "example_zh": "挽歌《阿尔普·艾尔·通阿》——现存最古老突厥诗歌之一，数节完整传世（iie.kz/Wikiwand）",
             "example_en": "The elegy for Alp Er Tunga - one of the oldest surviving Turkic poems, preserved in full (iie.kz/Wikiwand)"},
            {"mode_id": "M-KSGL-008", "example_zh": "以巴拉沙衮为圆心、东方为上的圆形世界地图（附《词典》卷首）",
             "example_en": "The circular world map centred on Balasagun with the east at the top (prefixed to the Diwan)"},
            {"mode_id": "M-KSGL-009", "example_zh": "巴尔思汗词源两说并存——以地名保存记忆层次（DLT）",
             "example_en": "Two etymologies of Barsgan recorded side by side - toponymic memory kept in layers (DLT)"},
            {"mode_id": "M-KSGL-010", "example_zh": "先语法后词典、由简入繁的结构安排（DLT I.4 自述）",
             "example_en": "Grammar before dictionary, simple to complex (DLT I.4)"},
        ],
        "key_texts": [
            "《突厥语大词典》（Dīwān Lughāt al-Turk，1072—1077 编于巴格达）",
            "《突厥语语法精华》（Kitāb Jawāhir al-Naḥw fī Lughat al-Turk，已佚，见《词典》自述）",
            "《突厥语世界圆形地图》（附《词典》卷首，现存最早突厥世界地图）",
        ],
        "key_concepts": ["田野亲历亲录", "方言逐词标注", "部落谱系", "文明对等（两匹赛马）", "以突厥为中心的圆形地图", "口传活态保存"],
        "intellectual_lineage": ["阿拉伯辞书学（哈利勒·伊本·艾哈迈德《阿因书》体例）", "突厥部族口头文学与谚语传统", "阿拔斯知识圈的翻译与编纂语境"],
        "legacy_assessment": (
            "喀什噶里以一书写定突厥诸部语言与文化：语言学上，《词典》被称为突厥历史语言学最重要的单一文献（Dankoff），"
            "保存了鄂尔浑碑铭之外最古老的突厥文学实体；文化上，其为突厥诸族现代语言史与身份书写提供基石，"
            "UNESCO 定 2008 年为「麻赫穆德·喀什噶里年」，学界正筹备 2027 年成书 950 周年纪念；跨文明层面，"
            "它以阿拉伯语向中心呈现「边疆」价值，是文明对等论证的早期样本。待核事项（生卒、出生地、词条总数、"
            "圣训传述链等）按 caveats 分层使用。"
        ),
        "scholarly_value": ("突厥历史语言学与比较辞书学奠基文献；中亚历史、民族志与方言地理的一手材料；"
                            "口传文学（谚语、挽歌、史诗）早期标本；文明对话与知识组织方法的样本。"),
    }
    assert list(top.keys()) == KEY23, "顶层块键集不符"
    topdoc = {"schema_version": "v6", "card": "t_06017753", "figure_code": FIGURE,
              "proposal": top,
              "notes": ("本提案由合并卡 t_06017753 依研究产出（t_1eb78b6b）与库内 23 键块口径构造，供合并写入 "
                        "modes_data.json 顶层（置于 'modes' 键前）；core_modes=M-KSGL-001~010；键集与既有块同构。")}
    write("docs/scratch/phase21_ksgl_landing/top_block_proposal.json", dump(topdoc))

    # ---------- 3. 场景件登记 ----------
    scen = {"figure_code": FIGURE, "card": "t_06017753",
            "notes": {
                "new_prefix_suggestion": "C-KSGL-001~010 / C-KSGL-001E~010E（入库前全库 0 碰撞）",
                "template_rule": "text_zh/text_en 由 name_zh/name_en + modern_applications_zh/en 模板复算（沿 C-WX/C-LUORQ/C-SHF 生成规则）",
                "scenarios_zh_new": 0,
                "scenarios_en_new": 0,
                "old_code_dispositions": [],
                "template_generated_zh": 10,
                "template_generated_en": 10,
                "note": "Phase 21 首批合并：研究产出自带 modern_applications_*，场景按模板新生成（非旧码搬迁）；无旧载荷处置。",
            }}
    write("docs/scratch/phase21_ksgl_landing/scenario_notes.json", dump(scen))

    # ---------- 4. 图档 / 个体 / 模式四件 ----------
    meta = json.loads(json.dumps(srcfig.get("meta") or {}, ensure_ascii=False))
    meta.pop("source", None)
    archive = {}
    archive["schema_version"] = "v6"
    archive["id"] = FIGURE
    archive["code"] = FIGURE
    archive["figure_name"] = FIGNAME
    archive["figure_code"] = FIGURE
    archive["figure_pinyin"] = srcfig.get("figure_pinyin", "")
    archive["figure_name_en"] = srcfig["figure_name_en"]
    archive["birth_year"] = srcfig.get("birth_year")
    archive["death_year"] = srcfig.get("death_year")
    archive["era"] = srcfig["era"]
    archive["time_period_standardized"] = srcfig["time_period_standardized"]
    archive["nationality"] = srcfig["nationality"]
    archive["ethnicity"] = srcfig["ethnicity"]
    archive["school"] = srcfig["school"]
    archive["intellectual_tradition"] = srcfig["intellectual_tradition"]
    archive["courtesy_name"] = srcfig.get("courtesy_name", "")
    archive["style_name"] = srcfig.get("style_name", "")
    archive["pseudonym"] = srcfig.get("pseudonym", "")
    archive["representative_works"] = list(srcfig["representative_works"])
    archive["historical_significance"] = srcfig["historical_significance"]
    archive["core_thoughts"] = list(srcfig["core_thoughts"])
    archive["famous_quote"] = srcfig["famous_quote"]
    archive["famous_quote_source"] = srcfig["famous_quote_source"]
    archive["influence"] = srcfig["influence"]
    archive["tags"] = list(srcfig["tags"])
    # cross_references：只收录已注册目标（H-IKH-001 / H-MAI-001）；第 3 条 H-GHZ-001 未注册，
    # 按「新条目 0 悬空」纪律暂不收录，caveat 如实登记（原始提案见研究档）。
    xrefs = [x for x in srcfig["cross_references"] if x.get("target_figure_code") in ("H-IKH-001", "H-MAI-001")]
    assert len(xrefs) == 2, "已注册 xref 数不符"
    archive["cross_references"] = json.loads(json.dumps(xrefs, ensure_ascii=False))
    archive["meta"] = meta
    archive["meta"]["merge"] = "t_06017753 合并卡：按研究产出（t_1eb78b6b）重建 v6 归档并入库（六件+注册面）；上游 individuals 空壳件同卡修复（字段映射缺陷）。"
    archive["related_figures"] = [x["target_figure_code"] for x in archive["cross_references"]]
    archive["thinking_mode_count"] = 10
    archive["mode_ids"] = list(CODES)
    archive["mode_ids_note"] = ("Phase 21 入库：图码 H-KSGL-001 与模式码 M-KSGL-001~010 落盘前全库查重 0 占用；"
                                "核验状态 pending，入库后须走独立核验流程（沿 HLX 批次口径）。")
    caveats = list(srcfig["caveats"])
    caveats.append("cross_references 登记：研究稿第 3 条指向 H-GHZ-001（安萨里），该图码在 figure_names 有名录而无 "
                   "code_maps 条目（存量同类 57 例）；本卡按「新条目 0 悬空」纪律暂不收录该条，待其主档注册后补录"
                   "（原始提案见 t_1eb78b6b 研究档）。")
    caveats.append("上游落地卡 t_43e4872a 写入的 individuals 两件为字段映射缺陷的空壳件（18 键 legacy 壳，正文全空）；"
                   "本合并卡 t_06017753 已按研究产出重建为 v6 归档，图档/个体/模式四面同体。")
    archive["caveats"] = caveats

    figdoc = dict(archive)
    figdoc["modes"] = json.loads(json.dumps(entries, ensure_ascii=False))
    inddoc = dict(archive)

    wrapper = {"schema_version": "v6", "code": FIGURE, "figure_name_zh": FIGNAME,
               "figure_name_en": srcfig["figure_name_en"], "mode_count": 10,
               "modes": json.loads(json.dumps(entries, ensure_ascii=False))}

    write("docs/scratch/phase21_ksgl_landing/figures/H-KSGL-001.json", dump(figdoc))
    write("docs/scratch/phase21_ksgl_landing/figures/H-KSGL-001_modes.json", dump(wrapper))
    write("docs/scratch/phase21_ksgl_landing/individuals/H-KSGL-001.json", dump(inddoc))
    write("docs/scratch/phase21_ksgl_landing/individuals/H-KSGL-001_modes.json", dump(wrapper))

    # ---------- 5. landing manifest ----------
    rels = ["modes_library_entries.json", "combined_library_entries.json", "id_mapping.tsv", "category_mapping.tsv",
            "top_block_proposal.json", "scenario_notes.json",
            "figures/H-KSGL-001.json", "figures/H-KSGL-001_modes.json",
            "individuals/H-KSGL-001.json", "individuals/H-KSGL-001_modes.json"]
    man = {"schema_version": "v1", "card": "t_06017753", "chain": "Phase 21 麻赫穆德·喀什噶里（H-KSGL-001）合并链",
           "figure_code": FIGURE, "figure_name": FIGNAME,
           "landing_dir": "docs/scratch/phase21_ksgl_landing/",
           "sources": {"attachments/t_1eb78b6b/H-KSGL-001.json": SRC_FIG_SHA,
                       "attachments/t_1eb78b6b/H-KSGL-001_modes.json": SRC_MODES_SHA},
           "files": {r: {"sha256": sha_file(os.path.join(LAND, r)), "bytes": os.path.getsize(os.path.join(LAND, r))} for r in rels},
           "note": ("落盘包由合并卡生成（上游 t_43e4872a 仅落 individuals 空壳两件）；内容源=研究产出 attachments 两件，"
                    "条目 27 键逐字等于研究产出；图档 xref 只收录已注册目标（见 caveats 登记）。")}
    write("data/audit/phase21_ksgl_landing_manifest.json", dump(man))
    print("[OK] landing package built at docs/scratch/phase21_ksgl_landing/ (%d files)" % len(rels))
    for r in rels:
        print("   %-40s %s" % (r, sha_file(os.path.join(LAND, r))[:16]))


if __name__ == "__main__":
    main()
