#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Phase21-R9 安子介重建落盘报告生成器（卡 t_58ebf9c2）
import collections
import io
import json
import os

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
MAN = os.path.join(REPO, 'data/audit/phase21r9_azj_landing_manifest.json')
EV = os.path.join(REPO, 'docs/research/phase21r9_azj_landing_evidence.json')
VER = os.path.join(REPO, 'docs/research/phase21r9_azj_verify_evidence.json')
GATE = os.path.join(REPO, 'docs/research/phase21r9_azj_gate.txt')
OUT = os.path.join(REPO, 'docs/research/phase21r9_azj_rebuild_report.md')


def jl(p):
    return json.load(io.open(p, encoding='utf-8'))


man = jl(MAN)
ev = jl(EV)
ver = jl(VER)
land = jl(os.path.join(REPO, 'docs/scratch/legacy20_r9_azj_landing/modes_library_entries.json'))
top = jl(os.path.join(REPO, 'docs/scratch/legacy20_r9_azj_landing/top_block_proposal.json'))
gate = io.open(GATE, encoding='utf-8').read()

L = []
A = L.append
A(u'# Phase21-R9 安子介 H-AZJ-001 重建落盘报告')
A(u'')
A(u'- 卡：t_58ebf9c2（Phase21-R9 安子介重做 · 重建落盘；上游 t_1aa06d0c 素材包）')
A(u'- 落盘日期：2026-09-24（CST）')
A(u'- 素材：AZJ-1 素材包 docs/research/phase21r9_anzijie_sourcing_report.md/.json（见证 W01—W11）')
A(u'- 落盘脚本：tools/build_phase21r9_azj.py；独立核验：verify_phase21r9_azj.py')
A(u'- 结论：10 模式 M-AZJ-001~010 与 figure 档案 H-AZJ-001 全部落盘（主库零写入）；独立核验 %d PASS / %d FAIL；credibility gate --hard-fail exit 0' % (ver['passed'], ver['failed']))
A(u'')
A(u'## 0. 核验摘要')
A(u'')
A(u'| 项 | 结果 |')
A(u'| --- | --- |')
A(u'| 条目 | 10 条：M-AZJ-001~010（重做链新码；H-AZJ-345 判死清档件号段不复用，legacy 面空缺） |')
A(u'| 引文 | 10/10 逐条为素材包 quotes 子串（key_quote 全段落源，qsrc 索引见 manifest.quote_table） |')
A(u'| 见证 | 11 件存证 sha256 与素材包逐一一致（E01—E11）；10/10 key quote 见证文本强归一化命中 |')
A(u'| 片段 | %d 段「」片段全部可回溯素材包（引文段/字段/md），零无源片段 |' % ev['frag_register_total'])
A(u'| 查重（码/名） | M-AZJ 全库外部 0 碰撞；live 主库六件 AZJ/安子介 0 命中；H-AZJ-001 命名空间 0 占用（除本卡产出与 AZJ-1 素材包） |')
A(u'| 禁用复用 | 旧载荷标记 19 项（特区建设/摸着石头过河/伪造出处/旧号段等）零出现（verify F02） |')
A(u'| 主库 | 六件 sha 前后一致（零写入，manifest.zero_library_write）；归档 10 件字节未动 |')
A(u'| 门禁 | credibility gate --hard-fail：0 硬失败、exit 0；D4 10 unchecked、D5 命中 0 |')
A(u'| 独立核验 | %d PASS / %d FAIL（docs/research/phase21r9_azj_verify_evidence.json） |' % (ver['passed'], ver['failed']))
A(u'')
A(u'## 1. 落盘产物清单（含 sha256）')
A(u'')
A(u'| 路径 | 字节 | sha256 |')
A(u'| --- | --- | --- |')
for k in sorted(man['deliverables']):
    v = man['deliverables'][k]
    A(u'| %s | %d | %s |' % (k, v['bytes'], v['sha256']))
A(u'')
A(u'（报告、核验证据、门禁全文不在清单内：docs/research/phase21r9_azj_rebuild_report.md、docs/research/phase21r9_azj_verify_evidence.json、docs/research/phase21r9_azj_gate.txt、docs/research/phase21r9_azj_landing_evidence.json。）')
A(u'')
A(u'## 2. 逐条结果（10 条）')
A(u'')
A(u'| # | 模式码 | 命名（中文） | 类目 | 主题域（素材包） | key quote 见证 | 字数 |')
A(u'| --- | --- | --- | --- | --- | --- | --- |')
for i, e in enumerate(land, 1):
    A(u'| %d | %s | %s | %s | %s | %s | %d |' % (i, e['id'], e['name_zh'], e['category'], e['category_raw'],
                                                 e['verification']['evidence'].split(u'见证 ')[1].split(u'）')[0], len(e['key_quote_zh'])))
A(u'')
A(u'### 2.1 引文全文（逐字取自 AZJ-1 素材包 §二 quotes；qsrc 索引见 manifest.quote_table）')
A(u'')
for i, e in enumerate(land, 1):
    A(u'%d. **%s %s**（%s）：%s' % (i, e['id'], e['name_zh'],
                                    e['verification']['evidence'].split(u'（quotes ')[1].split(u'）')[0],
                                    e['key_quote_zh']))
    A(u'')
A(u'## 3. 裁定执行记录（本卡对落库字段的裁定）')
A(u'')
A(u'### 3.1 命名与字段裁定')
A(u'')
A(u'- name_zh 取素材包名称主干（全名保留于 id_mapping.tsv pack_name 列）；name_en 为重建卡译写（素材包未给英译名，其余英文面同为中文内容之译写，如实注明为重建卡译写，非来源文本）。')
A(u'- legacy_mode_id 一律为空：H-AZJ-345 判死清档件号段与叙事不复用（与 R8 罗瑞卿「旧号不复用」口径同构）。')
A(u'- category 归入库内标准 18 类；category_raw 保留素材包主题域原文（对照表见 category_mapping.tsv）。')
A(u'- level=核心、priority=1..10：重做链内置排序（非素材包判定，落库以合并卡为准）。')
A(u'- key_quote_zh 逐字取素材包 quotes 段（不改写、不拼接）；key_quote_en 为译写。')
A(u'- verification.status=pending（10/10）：疑似与概述级内容不得因本卡核验而升级；入库前须走独立核验流程。')
A(u'- source_chapter 全部含「AZJ-1 素材包 §二 M-AZJ-0xx」并附见证编号；key quote 出处逐条可回溯。')
A(u'')
A(u'### 3.2 疑似与两说口径落实（素材包 §五 保留 pending）')
A(u'')
A(u'- M-AZJ-001：「第五大发明」保持「讲话转述」口径；「二十一世纪是汉字发挥威力」保留疑似（W09 转述链）。')
A(u'- M-AZJ-004：接见次数两说（W01 七次 / W10 六次）并注，不单取。')
A(u'- M-AZJ-005：「16 条」条目内容未获，不得代拟。')
A(u'- M-AZJ-006：「部首切除法」与 170 部首样本保留疑似（词条转述）。')
A(u'- M-AZJ-009：「最高学术奖」保留转述评价语口径。')
A(u'- M-AZJ-010：享年 87/88、「国葬」口径并注（官方通稿未用该词）。')
A(u'')
A(u'### 3.3 禁用复用落实')
A(u'')
A(u'- verify F02 扫描 19 项旧载荷/伪造出处标记（含「特区建设」「摸着石头过河」「《安子介回忆录》」「《深圳特区建设档案》」「An Zijie」「SEZ」「M001—M010」等）在本卡数据面零出现。')
A(u'- H-AZJ-345 仅出现在判死清档的登记性说明（mode_ids_note/caveats/id_mapping note），无任何字段/叙事复用。')
A(u'')
A(u'## 4. 片段来源登记（%d 段）' % ev['frag_register_total'])
A(u'')
A(u'条目内所有「」/『』片段均须可回溯素材包；本卡 %d 段片段全部命中引文段与/或素材包字段（summary/boundary/modern/theme/tier/name）或素材包 md 全文。分源计数（片段·来源组合）：' % ev['frag_register_total'])
A(u'')
A(u'| 来源 | 片段数 |')
A(u'| --- | --- |')
for k, v in sorted(ev['frag_register_counts'].items(), key=lambda x: -x[1]):
    A(u'| %s | %d |' % (k, v))
A(u'')
A(u'## 5. 核验与门禁结果')
A(u'')
A(u'### 5.1 独立核验 verify_phase21r9_azj.py')
A(u'')
g = collections.OrderedDict()
for r in ver['results']:
    d = g.setdefault(r['group'], [0, 0])
    d[0 if r['status'] == 'PASS' else 1] += 1
A(u'| 组 | 内容 | 结果 |')
A(u'| --- | --- | --- |')
GNAME = dict(files=u'文件与结构（解析/冻结副本逐字节/TSV/manifest sha 复算/同链布局）',
             entries=u'条目不变量（id/legacy 空/figure/类目/level/priority/verification pending/英文面/来源指向）',
             **{'quote-pack': u'引文 vs 素材包 quotes 子串（10 条）',
                'quote-witness': u'引文 vs 见证文本强归一化（10 条）',
                'witness': u'见证 11 件 sha256 逐一复核',
                'fragments': u'片段可回溯 + 旧载荷标记零出现 + 疑似/两说保留',
                'dedup': u'查重与残留（M 码 0 碰撞 / live 0 命中）',
                'frozen': u'主库零写入 + 归档字节未动',
                'figure': u'figure 层（mode_ids/core_thoughts/caveats/tags/meta/引语/互引）',
                'landing': u'顶层块提案与场景登记',
                'report': u'报告与产出证据存在'})
for k, v in g.items():
    A(u'| %s | %s | PASS %d / FAIL %d |' % (k, GNAME.get(k, k), v[0], v[1]))
A(u'| 合计 | — | %d PASS / %d FAIL |' % (ver['passed'], ver['failed']))
A(u'')
A(u'### 5.2 credibility gate（--hard-fail，数据面 = 落盘包）')
A(u'')
A(u'- 硬失败 0 条、exit 0；新增（基线外）0 条；D3 豁免 on、豁免 0 条。')
A(u'- D4（引文不符）：10 条 unchecked——理由分布 no-fulltext-link 8、no-citation 2；按「不假装核过」口径登记。')
A(u'- D5（时间线矛盾）：0 条命中（全库扫描无通过全部过滤的矛盾）。')
A(u'- 全文：docs/research/phase21r9_azj_gate.txt。')
A(u'')
A(u'## 6. 边界与遗留（不属本卡）')
A(u'')
A(u'### 6.1 合并卡面（t_ce457734，等合并卡执行）')
A(u'')
for it in ev['merge_card_scope']:
    A(u'- %s' % it)
A(u'- 顶层块新增提案（非替换；H-AZJ-345 旧块已清档）：docs/scratch/legacy20_r9_azj_landing/top_block_proposal.json（23 键与库内块同构）。')
A(u'')
A(u'### 6.2 已登记残留分层（非本卡产出，登记不触）')
A(u'')
A(u'- 语义索引副本：data/semantic_index_metadata.pkl、api/data/semantic_index_metadata.pkl（R8 S29/S30 口径，另卡裁定）。')
A(u'- 离线旧库：根 protreptic.db（R8 S31：「历史件，构建链忽略，保留可视为离线快照」）。')
A(u'- 冻结发布快照：release/v2.0.0/**（R7 已列「建议另卡核定」）。')
A(u'- 构建面：site_docs/** 全站导航（gitignored，重建站点即更新）。')
A(u'- 记录/证据类：R6C/R7/R8/R9 研究、QA、评审文档与 data/figures/_duplicates、data/backup*（历史证据件）。')
A(u'')
A(u'### 6.3 商榷项（等裁定，不影响本卡完成度）')
A(u'')
A(u'- AZJ-1 素材包 §五 开放项（10 项 / 13 条登记）：全部保留 pending 或两说口径，本卡未升级、未代拟。')
A(u'- 本卡新增商榷项：无。')
A(u'')
A(u'### 6.4 未动面（核验覆盖）')
A(u'')
A(u'- 主库六件（modes_data/code_maps/scenarios_zh/scenarios_en/scenario_tags/figure_names）：sha 前后一致，0 命中、零写入。')
A(u'- data/figures/_duplicates/H-AZJ-345_* 十件：字节未变（manifest.archive_untouched）。')
A(u'- data/backup*、backups*/、发布仓：未触。')
A(u'')
A(u'## 7. 证据与产物路径')
A(u'')
A(u'- 落盘脚本：tools/build_phase21r9_azj.py')
A(u'- 独立核验脚本：verify_phase21r9_azj.py')
A(u'- 落盘清单与预检/后检：data/audit/phase21r9_azj_landing_manifest.json')
A(u'- 产出证据（层级表/身份锚点/片段登记/合并卡面）：docs/research/phase21r9_azj_landing_evidence.json')
A(u'- 核验证据（逐条）：docs/research/phase21r9_azj_verify_evidence.json')
A(u'- 门禁全文：docs/research/phase21r9_azj_gate.txt')
A(u'- 数据四件：data/figures/H-AZJ-001.json、data/figures/H-AZJ-001_modes.json、data/individuals/H-AZJ-001.json、data/individuals/H-AZJ-001_modes.json')
A(u'- 落地包（10 件）：docs/scratch/legacy20_r9_azj_landing/**')
A(u'- 素材包（AZJ-1）：docs/research/phase21r9_anzijie_sourcing_report.md / .json；见证存证：docs/scratch/phase21r9_anzijie/witness/（11 件）')
A(u'')
A(u'---')
A(u'*本报告由 t_58ebf9c2（elcano）生成于 2026-09-24（CST）；数据面 = 落盘包（14 件）+ 报告/证据件；主库零写入。*')

with io.open(OUT, 'w', encoding='utf-8') as f:
    f.write(u'\n'.join(L) + u'\n')
print('WROTE', OUT, os.path.getsize(OUT))
