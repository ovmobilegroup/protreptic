# Phase21-R9 安子介 H-AZJ-001 重建落盘报告

- 卡：t_58ebf9c2（Phase21-R9 安子介重做 · 重建落盘；上游 t_1aa06d0c 素材包）
- 落盘日期：2026-09-24（CST）
- 素材：AZJ-1 素材包 docs/research/phase21r9_anzijie_sourcing_report.md/.json（见证 W01—W11）
- 落盘脚本：tools/build_phase21r9_azj.py；独立核验：verify_phase21r9_azj.py
- 结论：10 模式 M-AZJ-001~010 与 figure 档案 H-AZJ-001 全部落盘（主库零写入）；独立核验 81 PASS / 0 FAIL；credibility gate --hard-fail exit 0

## 0. 核验摘要

| 项 | 结果 |
| --- | --- |
| 条目 | 10 条：M-AZJ-001~010（重做链新码；H-AZJ-345 判死清档件号段不复用，legacy 面空缺） |
| 引文 | 10/10 逐条为素材包 quotes 子串（key_quote 全段落源，qsrc 索引见 manifest.quote_table） |
| 见证 | 11 件存证 sha256 与素材包逐一一致（E01—E11）；10/10 key quote 见证文本强归一化命中 |
| 片段 | 91 段「」片段全部可回溯素材包（引文段/字段/md），零无源片段 |
| 查重（码/名） | M-AZJ 全库外部 0 碰撞；live 主库六件 AZJ/安子介 0 命中；H-AZJ-001 命名空间 0 占用（除本卡产出与 AZJ-1 素材包） |
| 禁用复用 | 旧载荷标记 19 项（特区建设/摸着石头过河/伪造出处/旧号段等）零出现（verify F02） |
| 主库 | 六件 sha 前后一致（零写入，manifest.zero_library_write）；归档 10 件字节未动 |
| 门禁 | credibility gate --hard-fail：0 硬失败、exit 0；D4 10 unchecked、D5 命中 0 |
| 独立核验 | 81 PASS / 0 FAIL（docs/research/phase21r9_azj_verify_evidence.json） |

## 1. 落盘产物清单（含 sha256）

| 路径 | 字节 | sha256 |
| --- | --- | --- |
| data/figures/H-AZJ-001.json | 74464 | 404bec49e7bfcdf8cfdc666b77270aa531bbb02d053c672f38af93bafe8cf7b9 |
| data/figures/H-AZJ-001_modes.json | 68260 | 5579911724b2844fa6b6eafdcad722a71b4250bc917be5043813e992025f048a |
| data/individuals/H-AZJ-001.json | 6339 | a14a93ef50ee0d8fa680f7b4d454df8df0e75ca2eeb000a083f12121f0c88404 |
| data/individuals/H-AZJ-001_modes.json | 68260 | 5579911724b2844fa6b6eafdcad722a71b4250bc917be5043813e992025f048a |
| docs/scratch/legacy20_r9_azj_landing/category_mapping.tsv | 1010 | f8f552123dde2e4b02b5b1d565af4a979facf1a2cbedc85abce44c5810c88052 |
| docs/scratch/legacy20_r9_azj_landing/combined_library_entries.json | 68153 | deb0a98fa59e0d0fffd5999b330222d78370388d84d9e8444d3ba49b2e010e6b |
| docs/scratch/legacy20_r9_azj_landing/figures/H-AZJ-001.json | 74464 | 404bec49e7bfcdf8cfdc666b77270aa531bbb02d053c672f38af93bafe8cf7b9 |
| docs/scratch/legacy20_r9_azj_landing/figures/H-AZJ-001_modes.json | 68260 | 5579911724b2844fa6b6eafdcad722a71b4250bc917be5043813e992025f048a |
| docs/scratch/legacy20_r9_azj_landing/id_mapping.tsv | 2259 | 8284cd7c89db522013a88ebdf4b6934a1c458ffa92221c162290c01fbf33412c |
| docs/scratch/legacy20_r9_azj_landing/individuals/H-AZJ-001.json | 6339 | a14a93ef50ee0d8fa680f7b4d454df8df0e75ca2eeb000a083f12121f0c88404 |
| docs/scratch/legacy20_r9_azj_landing/individuals/H-AZJ-001_modes.json | 68260 | 5579911724b2844fa6b6eafdcad722a71b4250bc917be5043813e992025f048a |
| docs/scratch/legacy20_r9_azj_landing/modes_library_entries.json | 67433 | 4853d3ee9154cbcd5812a20c64a640afc0838c1ef79952d7ef93a8529edf6463 |
| docs/scratch/legacy20_r9_azj_landing/scenario_notes.json | 521 | 6a25943136581ea6775423e8138f726db89a993faf1c11fa495ce9930b1a3623 |
| docs/scratch/legacy20_r9_azj_landing/top_block_proposal.json | 8054 | 82a14e9cdc2069c04bb6db234cbaeeca466eee8455fa7d80b52f9a056c05ec44 |

（报告、核验证据、门禁全文不在清单内：docs/research/phase21r9_azj_rebuild_report.md、docs/research/phase21r9_azj_verify_evidence.json、docs/research/phase21r9_azj_gate.txt、docs/research/phase21r9_azj_landing_evidence.json。）

## 2. 逐条结果（10 条）

| # | 模式码 | 命名（中文） | 类目 | 主题域（素材包） | key quote 见证 | 字数 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | M-AZJ-001 | 汉字本位主义 | 教育传承 | 语言文字学/汉字现代化/文化观 | W01 | 102 |
| 2 | M-AZJ-002 | 实业救国路径 | 经济商业 | 实业经济/产业升级/知识迁移 | W07 | 64 |
| 3 | M-AZJ-003 | 多语种国际游说 | 战略决策 | 国际商务/语言战略 | W07 | 33 |
| 4 | M-AZJ-004 | 体制内建言 | 政治治理 | 政治参与/制度设计 | W01 | 64 |
| 5 | M-AZJ-005 | 「一国两制」早期理论贡献 | 政治治理 | 「一国两制」理论/政治战略 | W01 | 80 |
| 6 | M-AZJ-006 | 汉字解析教学法 | 教育传承 | 语言文字学/教育方法/文化传播 | W01 | 90 |
| 7 | M-AZJ-007 | 写字机与六位数编码 | 工程技术 | 发明创造/知识产权/汉字现代化 | W04 | 125 |
| 8 | M-AZJ-008 | 儒商传统 | 伦理修养 | 企业家精神/社会贡献/文化人格 | W01 | 49 |
| 9 | M-AZJ-009 | 教育公益与学术激励 | 教育传承 | 教育资助/学术激励/学界与业界互动 | W01 | 48 |
| 10 | M-AZJ-010 | 晚年使命 | 政治治理 | 「一国两制」实践/政治担当/生命史 | W07 | 73 |

### 2.1 引文全文（逐字取自 AZJ-1 素材包 §二 quotes；qsrc 索引见 manifest.quote_table）

1. **M-AZJ-001 汉字本位主义**（第 1 段；见证 W01）：他从小接受古典文化熏陶，对汉字和中国传统文化怀有深厚感情，认为汉字是中国第五大发明和中华文化之根，几十年如一日地致力于汉字学研究。他在繁忙的政务和商务间隙撰写了21本汉字学专著，不遗余力地向世界推广汉字。

2. **M-AZJ-002 实业救国路径**（第 3 段；见证 W07）：他通過翻譯日本商業書籍《間接成本之研究》，驚覺中國的工業生產力遠遠落後於世界列強，遂引發他借外國經濟理論振興中國民族工業的念頭。

3. **M-AZJ-003 多语种国际游说**（第 4 段；见证 W07）：他在不同的國家，能以不同的語言發表演說，很容易便打動了當地人的心。

4. **M-AZJ-004 体制内建言**（第 4 段；见证 W01）：1985年7月，安子介先生出任香港特别行政区基本法起草委员会副主任委员，同年12月被香港各界一致推举为基本法咨询委员会主任委员。

5. **M-AZJ-005 「一国两制」早期理论贡献**（第 2 段；见证 W01）：1984年，他在全国政协六届二次会议上提出“香港保持繁荣稳定16条”重要建议，并在香港报刊发表《保持香港繁荣之我见》等一系列文章，对稳定香港人心起到了积极作用。

6. **M-AZJ-006 汉字解析教学法**（第 1 段；见证 W01）：1982年，他用英文撰写的《解开汉字之谜》在香港出版，受到海内外人士和专家广泛关注，新加坡资政李光耀曾风趣地说：“如果此书出版于我开始学习中文之前，我学习中文就会感到比较容易了。”

7. **M-AZJ-007 写字机与六位数编码**（第 1 段；见证 W04）：本发明的编码方法的特征是，每个汉字取一个且只取一个部首赋予相应的数码，将此部首“切除”后余下的部分赋予另一数码，这两部分数码合起来构成了此汉字的本发明的编码，本发明的键盘的特点是，输入的键盘只由0至9的单个数字键及少量的统领其它一切机能的功能键构成。

8. **M-AZJ-008 儒商传统**（第 1 段；见证 W01）：安子介先生一生热心公益，担任过多项社会公职，以自己的模范行为践行了“我始终为香港人民服务”的诺言。

9. **M-AZJ-009 教育公益与学术激励**（第 1 段；见证 W01）：1991年，他在北京设立“安子介国际贸易研究奖”，为促进中国国际贸易理论教学研究发挥了积极作用。

10. **M-AZJ-010 晚年使命**（第 1 段；见证 W07）：已到「從心所欲」之年的安子介，原本打算從政商界退下來，全力研究漢字。但是他最終未能從心所欲，因為八十年代，啟動了香港回歸祖國進程，他毅然「出山」。

## 3. 裁定执行记录（本卡对落库字段的裁定）

### 3.1 命名与字段裁定

- name_zh 取素材包名称主干（全名保留于 id_mapping.tsv pack_name 列）；name_en 为重建卡译写（素材包未给英译名，其余英文面同为中文内容之译写，如实注明为重建卡译写，非来源文本）。
- legacy_mode_id 一律为空：H-AZJ-345 判死清档件号段与叙事不复用（与 R8 罗瑞卿「旧号不复用」口径同构）。
- category 归入库内标准 18 类；category_raw 保留素材包主题域原文（对照表见 category_mapping.tsv）。
- level=核心、priority=1..10：重做链内置排序（非素材包判定，落库以合并卡为准）。
- key_quote_zh 逐字取素材包 quotes 段（不改写、不拼接）；key_quote_en 为译写。
- verification.status=pending（10/10）：疑似与概述级内容不得因本卡核验而升级；入库前须走独立核验流程。
- source_chapter 全部含「AZJ-1 素材包 §二 M-AZJ-0xx」并附见证编号；key quote 出处逐条可回溯。

### 3.2 疑似与两说口径落实（素材包 §五 保留 pending）

- M-AZJ-001：「第五大发明」保持「讲话转述」口径；「二十一世纪是汉字发挥威力」保留疑似（W09 转述链）。
- M-AZJ-004：接见次数两说（W01 七次 / W10 六次）并注，不单取。
- M-AZJ-005：「16 条」条目内容未获，不得代拟。
- M-AZJ-006：「部首切除法」与 170 部首样本保留疑似（词条转述）。
- M-AZJ-009：「最高学术奖」保留转述评价语口径。
- M-AZJ-010：享年 87/88、「国葬」口径并注（官方通稿未用该词）。

### 3.3 禁用复用落实

- verify F02 扫描 19 项旧载荷/伪造出处标记（含「特区建设」「摸着石头过河」「《安子介回忆录》」「《深圳特区建设档案》」「An Zijie」「SEZ」「M001—M010」等）在本卡数据面零出现。
- H-AZJ-345 仅出现在判死清档的登记性说明（mode_ids_note/caveats/id_mapping note），无任何字段/叙事复用。

## 4. 片段来源登记（91 段）

条目内所有「」/『』片段均须可回溯素材包；本卡 91 段片段全部命中引文段与/或素材包字段（summary/boundary/modern/theme/tier/name）或素材包 md 全文。分源计数（片段·来源组合）：

| 来源 | 片段数 |
| --- | --- |
| quotes#1(W01)|pack_md | 9 |
| quotes#2(W01)|pack_md | 6 |
| quotes#2(W02)|pack_md | 5 |
| pack.modern|pack_md | 5 |
| quotes#3(W07)|pack_md | 4 |
| quotes#3(W09)|pack_md | 3 |
| pack_md | 3 |
| quotes#4(W02)|pack.summary|pack.name|pack_md | 3 |
| quotes#1(W02)|pack_md | 3 |
| pack.boundary|pack_md | 3 |
| quotes#4(W01)|pack.summary|pack_md | 3 |
| pack.summary|pack.boundary|pack_md | 3 |
| quotes#1(W07)|pack_md | 3 |
| quotes#4(W02)|pack_md | 2 |
| quotes#4(W01)|pack_md | 2 |
| quotes#1(W01)|pack.summary|pack_md | 2 |
| pack.summary|pack.boundary|pack.name|pack_md | 2 |
| quotes#3(W09)|pack.summary|pack.name|pack_md | 2 |
| pack.summary|pack_md | 2 |
| quotes#1(W01)|quotes#2(W02)|pack.summary|pack.name|pack_md | 2 |
| quotes#1(W07)|pack.summary|pack_md | 2 |
| quotes#4(W03)|pack.boundary|pack_md | 2 |
| quotes#1(W01)|pack.summary|pack.name|pack_md | 1 |
| quotes#1(W01)|pack.summary|pack.boundary|pack.name|pack_md | 1 |
| quotes#2(W08)|pack_md | 1 |
| quotes#5(W02)|pack_md | 1 |
| quotes#4(W07)|pack_md | 1 |
| quotes#3(W02)|pack_md | 1 |
| quotes#5(W01)|pack_md | 1 |
| quotes#6(W10)|pack_md | 1 |
| pack.summary|pack.modern|pack.name|pack_md | 1 |
| quotes#4(W08)|pack.summary|pack_md | 1 |
| quotes#4(W08)|pack_md | 1 |
| quotes#1(W04)|pack.summary|pack_md | 1 |
| quotes#1(W04)|pack_md | 1 |
| quotes#3(W04)|pack_md | 1 |
| quotes#5(W05)|pack_md | 1 |
| quotes#6(W03)|pack_md | 1 |
| quotes#4(W10)|pack_md | 1 |
| quotes#3(W03)|pack_md | 1 |
| quotes#3(W01)|pack_md | 1 |
| quotes#5(W07)|pack_md | 1 |

## 5. 核验与门禁结果

### 5.1 独立核验 verify_phase21r9_azj.py

| 组 | 内容 | 结果 |
| --- | --- | --- |
| files | 文件与结构（解析/冻结副本逐字节/TSV/manifest sha 复算/同链布局） | PASS 13 / FAIL 0 |
| entries | 条目不变量（id/legacy 空/figure/类目/level/priority/verification pending/英文面/来源指向） | PASS 12 / FAIL 0 |
| quote-pack | 引文 vs 素材包 quotes 子串（10 条） | PASS 10 / FAIL 0 |
| quote-witness | 引文 vs 见证文本强归一化（10 条） | PASS 10 / FAIL 0 |
| witness | 见证 11 件 sha256 逐一复核 | PASS 12 / FAIL 0 |
| fragments | 片段可回溯 + 旧载荷标记零出现 + 疑似/两说保留 | PASS 5 / FAIL 0 |
| dedup | 查重与残留（M 码 0 碰撞 / live 0 命中） | PASS 3 / FAIL 0 |
| frozen | 主库零写入 + 归档字节未动 | PASS 3 / FAIL 0 |
| figure | figure 层（mode_ids/core_thoughts/caveats/tags/meta/引语/互引） | PASS 8 / FAIL 0 |
| landing | 顶层块提案与场景登记 | PASS 4 / FAIL 0 |
| report | 报告与产出证据存在 | PASS 1 / FAIL 0 |
| 合计 | — | 81 PASS / 0 FAIL |

### 5.2 credibility gate（--hard-fail，数据面 = 落盘包）

- 硬失败 0 条、exit 0；新增（基线外）0 条；D3 豁免 on、豁免 0 条。
- D4（引文不符）：10 条 unchecked——理由分布 no-fulltext-link 8、no-citation 2；按「不假装核过」口径登记。
- D5（时间线矛盾）：0 条命中（全库扫描无通过全部过滤的矛盾）。
- 全文：docs/research/phase21r9_azj_gate.txt。

## 6. 边界与遗留（不属本卡）

### 6.1 合并卡面（t_ce457734，等合并卡执行）

- M-AZJ-001~010 入 data/modes_data.json（modes 列表 + 顶层块「H-AZJ-001」新增，随动 total）
- figure 注册：data/code_maps.json / data/figure_names.json / tools/json 镜像与 DB（api/protreptic.db）
- 站链复跑（既定 5 步）与 parity 复测；发布仓镜像 + push + ls-remote 回执
- 顶层块新增提案（非替换；H-AZJ-345 旧块已清档）：docs/scratch/legacy20_r9_azj_landing/top_block_proposal.json（23 键与库内块同构）。

### 6.2 已登记残留分层（非本卡产出，登记不触）

- 语义索引副本：data/semantic_index_metadata.pkl、api/data/semantic_index_metadata.pkl（R8 S29/S30 口径，另卡裁定）。
- 离线旧库：根 protreptic.db（R8 S31：「历史件，构建链忽略，保留可视为离线快照」）。
- 冻结发布快照：release/v2.0.0/**（R7 已列「建议另卡核定」）。
- 构建面：site_docs/** 全站导航（gitignored，重建站点即更新）。
- 记录/证据类：R6C/R7/R8/R9 研究、QA、评审文档与 data/figures/_duplicates、data/backup*（历史证据件）。

### 6.3 商榷项（等裁定，不影响本卡完成度）

- AZJ-1 素材包 §五 开放项（10 项 / 13 条登记）：全部保留 pending 或两说口径，本卡未升级、未代拟。
- 本卡新增商榷项：无。

### 6.4 未动面（核验覆盖）

- 主库六件（modes_data/code_maps/scenarios_zh/scenarios_en/scenario_tags/figure_names）：sha 前后一致，0 命中、零写入。
- data/figures/_duplicates/H-AZJ-345_* 十件：字节未变（manifest.archive_untouched）。
- data/backup*、backups*/、发布仓：未触。

## 7. 证据与产物路径

- 落盘脚本：tools/build_phase21r9_azj.py
- 独立核验脚本：verify_phase21r9_azj.py
- 落盘清单与预检/后检：data/audit/phase21r9_azj_landing_manifest.json
- 产出证据（层级表/身份锚点/片段登记/合并卡面）：docs/research/phase21r9_azj_landing_evidence.json
- 核验证据（逐条）：docs/research/phase21r9_azj_verify_evidence.json
- 门禁全文：docs/research/phase21r9_azj_gate.txt
- 数据四件：data/figures/H-AZJ-001.json、data/figures/H-AZJ-001_modes.json、data/individuals/H-AZJ-001.json、data/individuals/H-AZJ-001_modes.json
- 落地包（10 件）：docs/scratch/legacy20_r9_azj_landing/**
- 素材包（AZJ-1）：docs/research/phase21r9_anzijie_sourcing_report.md / .json；见证存证：docs/scratch/phase21r9_anzijie/witness/（11 件）

---
*本报告由 t_58ebf9c2（elcano）生成于 2026-09-24（CST）；数据面 = 落盘包（14 件）+ 报告/证据件；主库零写入。*

*v1.1 回执补记（2026-09-24）：全部产出已提交（commit 602a5d47；23 件、9,962 插入，含数据四件/落地包 10 件/报告与证据 4 件/脚本 3 件）；提交后复跑 verify_phase21r9_azj.py：81 PASS / 0 FAIL（exit 0）；credibility gate --hard-fail exit 0；主库六件 sha 复核未变（零写入口径）；归档 10 件字节未动。*
