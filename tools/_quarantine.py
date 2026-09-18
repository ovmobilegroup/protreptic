#!/usr/bin/env python3
"""共享隔离名单 —— 所有「公开产出层」的唯一事实来源 (Phase31-R4R5)。

为什么要有这个文件
    Phase30 的教训: QUARANTINE 只写在 tools/build_unified_index.py 里, 于是
    「统一索引 / 每日一模式」层过滤了虚构人物, 而「关系图谱」层
    (tools/build_graph_data.py 的 concept / mode / similar 三层) 没有过滤 ——
    H-SX-001「苏咸」从 /concepts 概念图漏出, concept_graph.json 的人物数变成
    284 = 283(公开名录口径) + 1(隔离项), 前端因为名录里查不到它, 只能把裸编号
    当人名显示。

    现在名单在此处定义一处, 下列脚本全部从这里导入, 不复制副本:
      * tools/build_unified_index.py   (名录层: figures/scenarios)
      * tools/build_graph_data.py      (图谱层: concept / mode / similar 三层)
      * tools/build_daily_index.py     (每日一模式层)
      * tools/ci_data_check.py         (校验门: 隔离项不得出现在公开名录)
    改名单 = 只改这里。

QUARANTINE —— 进入者不进入任何公开产出(名录 / 每日 / 图谱 / 概念层)
    H-SX-001「苏咸」: 10 条模式 (M393-M402) 全部引《苏咸子·权变篇/纵横篇/…》——
    该人物与该书均不存在 (检索仅得「苏秦」; 《汉书·艺文志》纵横家著录《苏子》
    31 篇, 无《苏咸子》)。判为虚构, 隔离。
    源数据仍保留在 data/modes_data.json / data/figures/ / data/figure_names.json,
    以便复核与回滚; 隔离只作用于公开产出层。

ADJUDICATED —— 2026-09 Phase31-R4R5 复核过、决定「保留不隔离」的记录
    H-FEI-001「非人」: 曾与 H-SX-001 并列被 QA 记为可疑人名 (R4), 复核结论为保留。

    它不是「伪造的历史人物」, 而是名录里唯一一条「概念主题簇」:
      1) 记录自述就是概念而非个人: data/figures/H-FEI-001.json 的
         historical_significance 原文「战国时期'非人'概念的哲学与制度探讨, 涉及
         道家虚无论、法家机器化思想、儒家礼义重构等多维度的思想流派」; 无生卒年
         (birth_year / death_year = null), school = 「百家」, gender =
         「Non-binary」—— 没有任何伪装成历史人物的身份主张。
      2) 10 条模式的内容与概念 (非有 / 无用之用 / 徙木立信 / 什伍连坐 / 礼论 /
         非人格化治理) 都能落到真实典籍:《道德经》《庄子·天运》《商君书·垦令》
         《荀子·礼论》。
      3) 缺陷确实存在, 但属「引证标签错误」而非「虚构人物」: M-FEI-001 /
         M-FEI-010 的 source_chapter 写作《道德经·极经》(道德经无此篇),
         M-FEI-003 写作《商君书·上》(无此篇), M-FEI-005/007/008/009 引
         《卓特思维模式考辨》(无此书目)。这些应在「引证治理」卡里单独处理,
         不该用「删掉整条记录」来掩盖。
      4) 计数口径: 隔离它会让 concept_graph 人物数变成 282, 与 Phase31-R4R5
         验收线 283 (公开名录口径: 284 个 figure_code - H-SX-001) 冲突。
    结论: 保留。若产品上要把「人物」与「概念主题」分开, 正确做法是在名录 schema
    里增加第三种 type, 而不是把有真实典籍支撑的概念簇当虚构数据删除。
"""

from __future__ import annotations

SCHEMA = "protreptic.quarantine/v1"

# code -> 隔离理由 (手工维护; 只加「已确证虚构」的记录)
QUARANTINE = {
    "H-SX-001": "引证伪造典籍《苏咸子》, 人物与书皆不存在 (10 条模式 M393-M402 全部引该书)",
}

# code -> 复核结论 (保留, 附证据; 见模块 docstring)
ADJUDICATED = {
    "H-FEI-001": "概念主题簇(非历史人物), 有真实典籍支撑; 引证标签错误另计, 保留不隔离",
}


def is_quarantined(code) -> bool:
    """figure_code / 名录 code 是否被隔离。空值一律不隔离。"""
    return str(code or "").strip() in QUARANTINE


def quarantined_mode_codes(modes) -> set:
    """从模式列表里算出「属于隔离人物」的 mode_code 集合。

    图谱层必须连这些模式一起剔除 —— 否则 M393-M402 仍会以模式节点 / 概念边 /
    相似模式邻居的形式把虚构人物带回公开产物。
    """
    out = set()
    for m in modes or ():
        mc = m.get("mode_code")
        if mc and is_quarantined(m.get("figure_code")):
            out.add(str(mc))
    return out


def drop_quarantined_modes(modes):
    """返回 (保留的模式列表, 被剔除的 mode_code 集合)。

    同时把保留模式 related_modes 里指向被剔除模式的引用删掉 (不能留悬挂边)。
    """
    modes = list(modes or ())
    dropped = quarantined_mode_codes(modes)
    kept = []
    for m in modes:
        mc = str(m.get("mode_code"))
        if mc in dropped:
            continue
        rel = m.get("related_modes")
        if isinstance(rel, list):
            pruned = [t for t in rel if str(t) not in dropped]
            if len(pruned) != len(rel):
                m = dict(m)
                m["related_modes"] = pruned
        kept.append(m)
    return kept, dropped
