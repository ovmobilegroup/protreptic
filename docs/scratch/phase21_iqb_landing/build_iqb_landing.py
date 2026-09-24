#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build_iqb_landing.py - Phase 21 伊克巴尔 (H-IQB-001) 落盘包生成器（卡 t_30a3e702）

背景（为什么由合并卡生成落盘包）
    上游落地卡 t_6839d252 只把研究产出导入仓库遗留库 protreptic.db（1 处提交 ca7b2f31），
    未落盘六件/图档/个体件，也无 landing 包与审计 manifest。
    研究卡 t_16080f61 的 attachments 两件为完整 v6 产出（27 键模式条目）。
    本生成器以研究产出为唯一内容源，构造：
      * modes_library_entries.json（10 条，逐字等于研究产出 modes）
      * combined_library_entries.json / id_mapping.tsv / category_mapping.tsv（台账）
      * top_block_proposal.json（23 键顶层块提案，供合并写入 modes_data.json）
      * scenario_notes.json（场景前缀与模板规则登记）
      * figures/H-IQB-001.json、figures/H-IQB-001_modes.json
      * individuals/H-IQB-001.json、individuals/H-IQB-001_modes.json
      * data/audit/phase21_iqb_landing_manifest.json（sha256 台账）
    幂等：重跑结果字节一致（内容确定性，无时间戳字段）。

用法（仓库根）:
    python3 docs/scratch/phase21_iqb_landing/build_iqb_landing.py
"""
from __future__ import annotations

import hashlib
import io
import json
import os

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
SRC_DIR = "/opt/data/kanban/boards/protreptic/attachments/t_16080f61"
SRC_FIG = os.path.join(SRC_DIR, "H-IQB-001.json")
SRC_MODES = os.path.join(SRC_DIR, "H-IQB-001_modes.json")
LAND = os.path.join(REPO, "docs/scratch/phase21_iqb_landing")
FIGURE = "H-IQB-001"
FIGNAME = "伊克巴尔"
CODES = ["M-IQB-%03d" % i for i in range(1, 11)]
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
SRC_FIG_SHA = "f2138dcc714051ae17c54fee4f0c86cee1f98b92c63b763e5f70bd3de13220dd"
SRC_MODES_SHA = "4eba6c5465e98690975dce434ea5d4d5b203077fde7b289dd9ee14408f4b3163"


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
                e["mode_code"], sorted(ekeys - set(KEYS27)), sorted(set(KEYS27) - ekeys)))
        assert ekeys == set(KEYS27), "键集不符: %s" % e["mode_code"]
        assert e["id"] == e["mode_code"] and e["figure_code"] == FIGURE and e["figure_name"] == FIGNAME
        assert e.get("legacy_mode_id") == "", "legacy_mode_id 非空"
        assert (e.get("verification") or {}).get("status") == "pending", "verification 非 pending"

    # ---------- 1. 条目面 ----------
    entries_out = json.loads(json.dumps(entries, ensure_ascii=False))  # 逐字副本
    write("docs/scratch/phase21_iqb_landing/modes_library_entries.json", dump(entries_out))
    combined = {"schema_version": "v6", "code": FIGURE, "figure_name_zh": FIGNAME,
                "figure_name_en": srcfig["figure_name_en"], "mode_count": 10, "modes": entries_out}
    write("docs/scratch/phase21_iqb_landing/combined_library_entries.json", dump(combined))
    idmap = ["new_code\tlegacy_mode_id"] + ["%s\t" % e["mode_code"] for e in entries]
    write("docs/scratch/phase21_iqb_landing/id_mapping.tsv", ("\n".join(idmap) + "\n").encode("utf-8"))
    catmap = ["mode_code\tcategory_raw\tcategory"] + ["%s\t%s\t%s" % (e["mode_code"], e["category_raw"], e["category"]) for e in entries]
    write("docs/scratch/phase21_iqb_landing/category_mapping.tsv", ("\n".join(catmap) + "\n").encode("utf-8"))

    # ---------- 2. 顶层块提案（23 键） ----------
    top = {
        "schema_version": "v6",
        "code": FIGURE,
        "name_zh": "伊克巴尔：自我锻造·宗教思想重建·东西互文",
        "name_en": "Muhammad Iqbal: Self-Forging (Khudi) · Reconstruction of Religious Thought · East-West Dialogue",
        "era": "英属印度殖民晚期/British India, Colonial Era (1877-1938)",
        "historical_domains": ["伊斯兰现代主义与宗教思想重建", "诗性哲学与意象锻造（波斯语/乌尔都语）", "政治构想与宪政设计", "东西文明对话", "自我哲学与人格教育"],
        "domains": ["伊斯兰现代主义", "诗性哲学", "宪政设计", "文明对话", "自我锻造"],
        "core_modes": list(CODES),
        "gender": "Male",
        "ethnicity": "克什米尔裔旁遮普穆斯林 / Kashmiri-descended Punjabi Muslim",
        "nationality": "英属印度（今巴基斯坦旁遮普省） / British India (present-day Punjab, Pakistan)",
        "civilization_sphere": "伊斯兰—南亚/英属印度殖民现代 / Islamo-South Asia / Colonial British India",
        "time_period_standardized": "1877-1938 CE",
        "primary_language": "波斯语/乌尔都语/英语（分层语域） / Persian / Urdu / English (layered registers)",
        "intellectual_tradition": "伊斯兰哲学、苏非传统与比较哲学及诗学（兼受尼采、柏格森与过程哲学等西方思潮影响）/ Islamic philosophy, Sufi tradition, comparative philosophy and poetics (with Nietzsche, Bergson and process philosophy)",
        "unique_thinking_zh": (
            "伊克巴尔（1877—1938），英属印度旁遮普锡亚尔科特（Sialkot）人，诗人、哲学家与政治思想家，"
            "被誉为「东方诗人」（Shair-e-Mashriq）与「乌玛的智者」（Hakeem-ul-Ummat）；受教于拉合尔政府学院、"
            "剑桥三一学院与慕尼黑大学（1907 年博士论文《波斯形而上学的发展》），并以波斯语、乌尔都语、英语三线写作。"
            "其思路可提炼十法：自我锻造（以自我肯定替代自我消解，三阶段——服从、自控、代治）／宗教思想重构"
            "（以伊智提哈德为运动原则，重启对经典的创造性诠释）／经验与科学对话（宗教经验作为知识，与科学双向对话）／"
            "东西互文对话（以《东方之信》回应歌德，平等交换文明礼物）／共同体融入（个体在共同体 millat 中完成"
            "第二次自我实现）／政治构想设计（把哲学愿景转译为可谈判的宪政架构，阿拉哈巴德方案）／意象铸造"
            "（以「隼鹰」「信士之人」把哲学下沉为大众符号）／历史精神重读（以「行先于思」的经验精神重读文明兴衰）／"
            "分层语域书写（波斯语、乌尔都语、英语三层受众分写）／未来世代召唤（以「明日之诗」与青年教育向未来说话）。"
            "生年（1877 主说，1876/1873/1875 旧说并存）、封爵年份（1922/1923 两说）、《无我之秘》出版年、"
            "《怨诉》《答复》首诵年份与语种占比诸说并存，按 caveats 分层登记。"
        ),
        "unique_thinking_en": (
            "Muhammad Iqbal (1877-1938), of Sialkot in the Punjab, British India, was a poet, philosopher and "
            "political thinker, honoured as the Poet of the East (Shair-e-Mashriq) and the Sage of the Ummah "
            "(Hakeem-ul-Ummat); educated at Government College Lahore, Trinity College Cambridge and the University "
            "of Munich (doctorate 1907, The Development of Metaphysics in Persia), he wrote across Persian, Urdu and "
            "English. Ten methods may be distilled: self-forging (self-affirmation over self-annihilation, in three "
            "stages - obedience, self-control, vicegerency) / reconstruction of religious thought (ijtihad as the "
            "principle of movement, reopening creative interpretation) / religious experience and science in dialogue "
            "(experience as knowledge, a two-way exchange with science) / East-West intertextual dialogue (answering "
            "Goethe in Payam-i-Mashriq, an equal exchange of gifts) / community integration (the self fulfilled a "
            "second time within the millat) / political blueprint design (translating vision into a negotiable "
            "constitutional scheme - the Allahabad Address) / symbol-image forging (the falcon and the man of faith "
            "sinking philosophy into popular symbols) / historical-spirit re-reading (reading civilizational rise "
            "and fall through the empirical spirit of 'deed rather than idea') / layered register writing (separate "
            "audiences in Persian, Urdu and English) / summoning the future generation (the poet of to-morrow "
            "speaking through youth and education). Variants on his birth year (1877 primary; 1876/1873/1875 older "
            "claims), knighthood year (1922/1923), the publication year of Rumuz-i Bekhudi, the recitation years of "
            "Shikwa and Jawab-e-Shikwa, and the language ratio are registered in the caveats."
        ),
        "mode_evidence": [
            {"mode_id": "M-IQB-001", "example_zh": "《自我的秘密》（1915）「存在之形是自我的效果，你所见皆为自我的秘密」；致尼科尔森哲学说明给出服从—自控—代治三阶段（1920）",
             "example_en": "Asrar-i Khudi (1915): 'the form of existence is an effect of the self'; the note to Nicholson sets out the three stages - obedience, self-control, vicegerency (1920)"},
            {"mode_id": "M-IQB-002", "example_zh": "《宗教思想重建》第 6 讲：「伊斯兰本质中的运动原则……这就是伊智提哈德」，并以土耳其改革为参照",
             "example_en": "Reconstruction, Lecture VI: 'the principle of movement in the structure of Islam... is ijtihad', citing Turkey's revival"},
            {"mode_id": "M-IQB-003", "example_zh": "《重建》前言：以「经典物理学自我批判—唯物论退潮」预告宗教与科学的「未见和谐」；第 7 讲「宗教是可能的吗？」",
             "example_en": "Preface to the Reconstruction: classical physics' self-criticism and the retreat of materialism foretell 'unsuspected mutual harmonies' of religion and science; Lecture VII asks 'Is Religion Possible?'"},
            {"mode_id": "M-IQB-004", "example_zh": "《东方之信》（1923）献诗：「为答复他，我写下了《东方之信》；我为东方的黄昏洒下了月光」",
             "example_en": "Payam-i-Mashriq (1923), dedicatory poem: 'In reply to him I have composed the Payam-i-Mashriq: I have shed moonbeams o'er the evening of the East'"},
            {"mode_id": "M-IQB-005", "example_zh": "《无我之秘》（1918）与《自我的秘密》对偶；《怨诉》与《答复》以「向神抱怨—神作答」迫使共同体自省（1913）",
             "example_en": "Rumuz-i Bekhudi (1918) as the counterpart to Asrar-i Khudi; Shikwa and Jawab-e-Shikwa stage the community's self-examination (1913)"},
            {"mode_id": "M-IQB-006", "example_zh": "阿拉哈巴德演讲（1930）：主张旁遮普、西北边省、信德与俾路支合并为「单一自治邦」，表述为印度的「内部均势」",
             "example_en": "Allahabad Address (1930): the amalgamation of Punjab, NWFP, Sind and Baluchistan into a single self-governing state, framed as an 'internal balance of power'"},
            {"mode_id": "M-IQB-007", "example_zh": "「隼鹰」意象群（《加百列的翅膀》1935）：「你是隼鹰，翱翔是你的天职」；认主词压缩句「胡迪之秘是万物非主」",
             "example_en": "The falcon image (Bal-i-Jibril, 1935): 'You are a falcon; flight is your vocation'; the kalima compressed: 'the hidden secret of the self is: there is no god but God'"},
            {"mode_id": "M-IQB-008", "example_zh": "《重建》前言「古兰经是一部强调『行』而非『思』的书」；把「堕落」重释为走向自由自我的过渡（1930: 85）",
             "example_en": "Preface: 'The Qur'an is a book which emphasizes deed rather than idea'; the Fall re-read as the passage to a free self (1930: 85)"},
            {"mode_id": "M-IQB-009", "example_zh": "尼科尔森导言：「他的信息不只是给印度的穆斯林，而是给所有地方的穆斯林；因此他用波斯语而非印度斯坦语写作」（1920, p. ix）",
             "example_en": "Nicholson's Introduction: 'His message is not for the Mohammedans of India alone, but for Moslems everywhere: accordingly he writes in Persian instead of Hindustani' (1920, p. ix)"},
            {"mode_id": "M-IQB-010", "example_zh": "《自我的秘密》自白：「我不需要今日之耳；我是明日诗人的声音」；《加百列游记》（1932）以儿子之名命名并向新世代讲话",
             "example_en": "'I have no need of the ear of To-day, I am the voice of the poet of To-morrow'; Javid Nama (1932), named for his son, addresses the new generation"},
        ],
        "key_texts": [
            "《自我的秘密》（Asrār-i Khudī，波斯文，1915；Nicholson 英译 1920）",
            "《无我之秘》（Rumūz-i Bekhudī，波斯文，1918）",
            "《东方之信》（Payām-i Mašriq，波斯文，1923；回应歌德《西东合集》）",
            "《钟声集》（Bang-i Dārā，乌尔都文，1924；收《怨诉》《答复》《印度之歌》）",
            "《宗教思想重建》（The Reconstruction of Religious Thought in Islam，英语，1930 拉合尔六讲本 / 1934 牛津增订本）",
            "《加百列游记》（Jāvīd Nāma，波斯文，1932）",
            "《加百列的翅膀》（Bal-i Jibrīl，乌尔都文，1935）",
            "《摩西的杖》（Zarb-i Kalīm，乌尔都文，1936）；《汉志的礼物》（Armaghān-i Hijāz，1938 遗作）",
        ],
        "key_concepts": ["胡迪（khudi，自我锻造）", "伊智提哈德（ijtihad，创制）", "无我（bekhudi）与共同体（millat）", "隼鹰（shaheen）", "信士之人（mard-e-momin）", "阿拉哈巴德方案与「内部均势」", "明日之诗（代际契约）"],
        "intellectual_lineage": ["伊斯兰哲学与苏非传统（鲁米、安萨里、莫拉·萨德拉等波斯思想）", "西方现代哲学（尼采、柏格森与过程哲学）", "歌德《西东合集》与东西互文对话传统"],
        "legacy_assessment": (
            "伊克巴尔身后影响持续放大：《自我的秘密》经尼科尔森（1920）译入英语后进入世界学术视野，《宗教思想重建》"
            "成为现代伊斯兰思想的关键文本；其波斯语诗歌使他获「拉合尔的伊克巴尔」（Iqbal Lahori）之名并影响阿里·沙里亚蒂"
            "等后来的伊斯兰复兴思想家；阿伯里、席梅尔、鲍萨尼等译本把《加百列游记》推向德语、意大利语与土耳其语读者。"
            "巴基斯坦独立后，他被尊为「巴基斯坦的思想奠基者」（Muffakir-e-Pakistan），拉合尔建有陵墓（Mazar-e-Iqbal），"
            "设有伊克巴尔学院（1951）与阿拉马·伊克巴尔开放大学（1974），11 月 9 日为「伊克巴尔日」。"
            "对其思想「民族主义—泛伊斯兰—穆斯林独立」的三阶段切割式解读与「巴基斯坦之父」标签存在过度叠加风险，"
            "本档按「精神之父/思想奠基者」表述并保留 1930 年演讲原始语境；生卒、封爵年份、首诵年份与语种占比诸说按 caveats 分层使用。"
        ),
        "scholarly_value": ("伊斯兰现代主义的枢纽文本与诗性哲学典范；南亚穆斯林现代政治思想（阿拉哈巴德方案）的一手来源；"
                            "东西文明对话与宗教—科学关系的早期样本；多语种分层写作与意象铸造的传播学标本。"),
    }
    assert list(top.keys()) == KEY23, "顶层块键集不符"
    topdoc = {"schema_version": "v6", "card": "t_30a3e702", "figure_code": FIGURE,
              "proposal": top,
              "notes": ("本提案由合并卡 t_30a3e702 依研究产出（t_16080f61）与库内 23 键块口径构造，供合并写入 "
                        "modes_data.json 顶层（置于 'modes' 键前）；core_modes=M-IQB-001~010；键集与既有块同构。")}
    write("docs/scratch/phase21_iqb_landing/top_block_proposal.json", dump(topdoc))

    # ---------- 3. 场景件登记 ----------
    scen = {"figure_code": FIGURE, "card": "t_30a3e702",
            "notes": {
                "new_prefix_suggestion": "C-IQB-001~010 / C-IQB-001E~010E（入库前全库 0 碰撞）",
                "template_rule": "text_zh/text_en 由 name_zh/name_en + modern_applications_zh/en 模板复算（沿 C-WX/C-LUORQ/C-SHF 生成规则）",
                "scenarios_zh_new": 0,
                "scenarios_en_new": 0,
                "old_code_dispositions": [],
                "template_generated_zh": 10,
                "template_generated_en": 10,
                "note": "Phase 21 首批合并：研究产出自带 modern_applications_*，场景按模板新生成（非旧码搬迁）；无旧载荷处置。",
            }}
    write("docs/scratch/phase21_iqb_landing/scenario_notes.json", dump(scen))

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
    # cross_references：只收录已注册目标（H-GAN-001 / H-ATK-001 / H-IKH-001）；
    # 第 3 条 H-GHZ-001（安萨里）有名录无 code_maps 条目，按「新条目 0 悬空」纪律暂不收录，
    # caveat 如实登记（原始提案见研究档）。
    xrefs = [x for x in srcfig["cross_references"] if x.get("target_figure_code") in ("H-GAN-001", "H-ATK-001", "H-IKH-001")]
    assert len(xrefs) == 3, "已注册 xref 数不符"
    archive["cross_references"] = json.loads(json.dumps(xrefs, ensure_ascii=False))
    archive["meta"] = meta
    archive["meta"]["merge"] = "t_30a3e702 合并卡：按研究产出（t_16080f61）重建 v6 归档并入库（六件+注册面）；上游落地卡 t_6839d252 未落盘量件，本卡补全。"
    archive["related_figures"] = [x["target_figure_code"] for x in archive["cross_references"]]
    archive["thinking_mode_count"] = 10
    archive["mode_ids"] = list(CODES)
    archive["mode_ids_note"] = ("Phase 21 入库：图码 H-IQB-001 与模式码 M-IQB-001~010 落盘前全库查重 0 占用；"
                                "核验状态 pending，入库后须走独立核验流程（沿 HLX/KSGL 批次口径）。")
    caveats = list(srcfig["caveats"])
    caveats.append("cross_references 登记：研究稿第 3 条指向 H-GHZ-001（安萨里），该图码在 figure_names 有名录而无 "
                   "code_maps 条目（存量同类 57 例）；本卡按「新条目 0 悬空」纪律暂不收录该条，待其主档注册后补录"
                   "（原始提案见 t_16080f61 研究档）。")
    caveats.append("上游落地卡 t_6839d252 只把研究产出导入仓库遗留库 protreptic.db（提交 ca7b2f31），未落盘图档/个体/模式件；"
                   "本合并卡 t_30a3e702 已按研究产出重建 v6 归档，图档/个体/模式四面同体。")
    archive["caveats"] = caveats

    figdoc = dict(archive)
    figdoc["modes"] = json.loads(json.dumps(entries, ensure_ascii=False))
    inddoc = dict(archive)

    wrapper = {"schema_version": "v6", "code": FIGURE, "figure_name_zh": FIGNAME,
               "figure_name_en": srcfig["figure_name_en"], "mode_count": 10,
               "modes": json.loads(json.dumps(entries, ensure_ascii=False))}

    write("docs/scratch/phase21_iqb_landing/figures/H-IQB-001.json", dump(figdoc))
    write("docs/scratch/phase21_iqb_landing/figures/H-IQB-001_modes.json", dump(wrapper))
    write("docs/scratch/phase21_iqb_landing/individuals/H-IQB-001.json", dump(inddoc))
    write("docs/scratch/phase21_iqb_landing/individuals/H-IQB-001_modes.json", dump(wrapper))

    # ---------- 5. landing manifest ----------
    rels = ["modes_library_entries.json", "combined_library_entries.json", "id_mapping.tsv", "category_mapping.tsv",
            "top_block_proposal.json", "scenario_notes.json",
            "figures/H-IQB-001.json", "figures/H-IQB-001_modes.json",
            "individuals/H-IQB-001.json", "individuals/H-IQB-001_modes.json"]
    man = {"schema_version": "v1", "card": "t_30a3e702", "chain": "Phase 21 伊克巴尔（H-IQB-001）合并链",
           "figure_code": FIGURE, "figure_name": FIGNAME,
           "landing_dir": "docs/scratch/phase21_iqb_landing/",
           "sources": {"attachments/t_16080f61/H-IQB-001.json": SRC_FIG_SHA,
                       "attachments/t_16080f61/H-IQB-001_modes.json": SRC_MODES_SHA},
           "files": {r: {"sha256": sha_file(os.path.join(LAND, r)), "bytes": os.path.getsize(os.path.join(LAND, r))} for r in rels},
           "note": ("落盘包由合并卡生成（上游落地卡 t_6839d252 仅导入遗留库，未落盘量件）；内容源=研究产出 attachments 两件，"
                    "条目 27 键逐字等于研究产出；图档 xref 只收录已注册目标（见 caveats 登记）。")}
    write("data/audit/phase21_iqb_landing_manifest.json", dump(man))
    print("[OK] landing package built at docs/scratch/phase21_iqb_landing/ (%d files)" % len(rels))
    for r in rels:
        print("   %-40s %s" % (r, sha_file(os.path.join(LAND, r))[:16]))


if __name__ == "__main__":
    main()
