# Phase21-R8 罗瑞卿 H-LUORQ-001 重建落盘报告

- 卡：t_bf2d9b82（Phase21-R8 罗瑞卿重做；单链作战）
- 落盘日期：2026-09-23
- 素材：B1 素材包 docs/research/phase21r8_luorq_sourcing_report.md / .json（见证 W1–W21）
- 落盘脚本：tools/build_phase21r8_luorq.py；独立核验：verify_phase21r8_luorq.py
- 结论：10 模式 M-LUORQ-001~010 全部落盘（主库零写入）；独立核验 69 PASS / 0 FAIL；credibility gate --hard-fail exit 0

## 0. 核验摘要

| 项 | 结果 |
| --- | --- |
| 条目 | 10 条：M-LUORQ-001~010（legacy_mode_id M351~M360，旧号不复用） |
| 引文 | 10/10 逐条为素材包 §三 quotes 子串；10/10 见证文本强归一化命中 |
| 见证索引 | 18 件见证文件 sha256 与本包 md 登记逐一一致 |
| 查重 | M-LUORQ-001~010 外部 0 碰撞；主库六件 0 命中（modes_data 顶层块保留、待合并卡） |
| 归档 | 4 件 sha256 未变（字节冻结、未动） |
| 片段白名单 | 23 条（登记于产出证据；均可回溯素材包 md/json） |
| 硬伤修正 | 5 项裁定全部落实（见 §3.1） |
| 旧场景 | C-LUORQ-001~010 逐条处置（见 §3.2） |
| 独立核验 | 69 PASS / 0 FAIL（明细 docs/research/phase21r8_luorq_verify_evidence.json） |
| 门禁 | credibility gate --hard-fail：0 硬失败、exit 0；D4 10 unchecked、D5 clean 10 / 命中 0 |

## 1. 落盘产物清单（含 sha256）

| 路径 | 字节 | sha256 |
| --- | --- | --- |
| data/figures/H-LUORQ-001.json | 68296 | d609b968a8d324eacb2a52ae6f9b03cba512d644ef6c4ae4ab167961b5056640 |
| data/individuals/H-LUORQ-001.json | 7704 | 91efb1b79a672bef9196d04e926c8ee3c2f9154b895e84f74534165f85d9c73f |
| data/individuals/H-LUORQ-001_modes.json | 60729 | a75decd03f71d7447c9a220d06b6a71fa379942200615b176cb01e17b68f3e8f |
| docs/scratch/legacy20_r8_luorq_landing/category_mapping.tsv | 892 | 582085e67f3794988e56eb7689df5f00b2e6fcfe90e8890227034c4fd5e337d2 |
| docs/scratch/legacy20_r8_luorq_landing/combined_library_entries.json | 60620 | 4b3498e3a6362e03a12e64a93516032bdeaf2d5866d585535d6a0bb56d3ad4c8 |
| docs/scratch/legacy20_r8_luorq_landing/figures/H-LUORQ-001.json | 68296 | d609b968a8d324eacb2a52ae6f9b03cba512d644ef6c4ae4ab167961b5056640 |
| docs/scratch/legacy20_r8_luorq_landing/id_mapping.tsv | 1493 | 81e145a2683517a96202cdc4ce28f66d7817d4eb7f15896f2f8954584aa806cc |
| docs/scratch/legacy20_r8_luorq_landing/individuals/H-LUORQ-001.json | 7704 | 91efb1b79a672bef9196d04e926c8ee3c2f9154b895e84f74534165f85d9c73f |
| docs/scratch/legacy20_r8_luorq_landing/individuals/H-LUORQ-001_modes.json | 60729 | a75decd03f71d7447c9a220d06b6a71fa379942200615b176cb01e17b68f3e8f |
| docs/scratch/legacy20_r8_luorq_landing/modes_library_entries.json | 59856 | c960b0716397cfa9eb23c55affc76ee3f42578262f6f82a4b006a3321acf337f |
| docs/scratch/legacy20_r8_luorq_landing/scenario_notes.json | 3740 | 370abdb329f2b9e453778d8640144049729487a7c662a1b05dfd094a3081c92b |
| docs/scratch/legacy20_r8_luorq_landing/top_block_proposal.json | 8107 | dd43241369ddc7a431e160aa644a11a1ea970fc4ece433fa23e29ee7f84ac2f9 |

（报告自身与核验证据不在清单内：docs/research/phase21r8_luorq_rebuild_report.md、docs/research/phase21r8_luorq_verify_evidence.json、verify_phase21r8_luorq.py。）

## 2. 逐条结果（10 条）

| # | 模式码 | 命名（中文） | 类目 | 引文 | 见证 | 引文字数 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | M-LUORQ-001 | 镇压与宽大相结合 | 政治治理 | q#1 | W1 | 45 |
| 2 | M-LUORQ-002 | 军警分途 | 组织领导 | q#2 | W7/W9 | 21 |
| 3 | M-LUORQ-003 | 党委领导＋群众路线 | 政治治理 | q#1 | W6 | 68 |
| 4 | M-LUORQ-004 | 郭兴福教学法与群众练兵 | 教育传承 | q#4 | W20/ch064 | 33 |
| 5 | M-LUORQ-005 | 警卫思想 | 战略决策 | q#1 | W20/ch054 | 21 |
| 6 | M-LUORQ-006 | 人民警察作风与警民关系 | 伦理修养 | q#1 | W10 | 41 |
| 7 | M-LUORQ-007 | 悼词与平反 | 史学文献 | q#1 | W3 | 49 |
| 8 | M-LUORQ-008 | 政治与军事的辩证统一 | 军事战略 | q#3 | W15 | 47 |
| 9 | M-LUORQ-009 | 反孤立主义、反神秘主义 | 方法论通用 | q#1 | W6 | 44 |
| 10 | M-LUORQ-010 | 支持真理标准讨论 | 认识论逻辑 | q#1 | W12 | 49 |

### 2.1 引文全文（逐字取自 B1 素材包 §三，q 序号为包内 quotes 顺序）

1. **M-LUORQ-001 镇压与宽大相结合**（q#1，见证 W1）：我们的政策从来就是镇压与宽大相结合的，现在也还是镇压与宽大相结合的，这乃是我们的基本政策。

2. **M-LUORQ-002 军警分途**（q#2，见证 W7/W9；《罗瑞卿军事文选》2006 第 566 页）：公安部队的指挥关系属军委，工作关系属公安部

3. **M-LUORQ-003 党委领导＋群众路线**（q#1，见证 W6）：把公安工作置于党中央和各级党委的绝对领导之下，并在工作中实行放手发动群众，大胆依靠群众的路线，这是我们党在长期革命实践中一个独特的创造。

4. **M-LUORQ-004 郭兴福教学法与群众练兵**（q#4，见证 W20/ch064）：训练要做到红、硬、活，又红又专；红第一，专第二，但一定要红专结合。

5. **M-LUORQ-005 警卫思想**（q#1，见证 W20/ch054）：警卫工作一要保证不出乱子，二要不脱离群众。

6. **M-LUORQ-006 人民警察作风与警民关系**（q#1，见证 W10）：我们必须反对侵犯人民利益、脱离群众的国民党作风。不准坐霸王车、吃霸王饭、看霸王戏!

7. **M-LUORQ-007 悼词与平反**（q#1，见证 W3）：罗瑞卿同志是无产阶级久经考验的忠诚的革命战士，中国人民解放军的杰出领导人，伟大导师毛主席的好学生。

8. **M-LUORQ-008 政治与军事的辩证统一**（q#3，见证 W15）：如果单纯把政治搞好，别的都不好，垮下来，这种政治恐怕不能算好政治，是空头政治，哪里有这种政治！

9. **M-LUORQ-009 反孤立主义、反神秘主义**（q#1，见证 W6）：主要表现为只相信自己，不相信群众；只相信上面，不相信下面；迷信某些技术，看不到人的作用。

10. **M-LUORQ-010 支持真理标准讨论**（q#1，见证 W12）：什么是检验真理的标准？马列主义、毛泽东思想是真理，但不能用来检验自己，只有实践才是检验真理的标准。


## 3. 裁定执行记录

### 3.1 硬伤修正 5 项（全部落实）

| # | 问题 | 处置 | 落点 |
| --- | --- | --- | --- |
| 1 | 「国防部长」误 | 纠偏：一律改写为「国防部副部长（1959 起，兼总参谋长）」；本档全字段零出现「国防部长」 | 旧图档正文与旧场景 C-LUORQ-004 |
| 2 | 「主要创建者之一」（失度） | 降格：改用悼词口径「中国人民解放军的杰出领导人」；本档全字段零出现「主要创建者」 | 旧图档正文 |
| 3 | 「Ten Marshals」误译 | 替换：one of the ten senior generals（开国十大大将之一）；替换文本见 top_block_proposal.json（落库由合并卡执行） | modes_data 顶层块 unique_thinking_en |
| 4 | 无源自拟命名（安全立军 / 整编革新 / 参谋统筹 / 情报先行） | 弃用：四式永久废名、不得任何形式回填；十条命名全部改用素材包 §三 可落源描述式命名 | 旧图档命名与旧顶层块 |
| 5 | C-LUORQ-007/008/009 泛化场景 | 逐条处置：C-007 改写锚 1958-08 八大纪律十项注意（或 1956-12-28 条例草案说明）；C-008 以宋德贵案/合肥事件重写；C-009 删除或改锚；全表见 scenario_notes.json | 归档件旧场景 |

### 3.2 旧场景处置表（C-LUORQ-001~010）

| 旧码 | 旧题 | 处置 |
| --- | --- | --- |
| C-LUORQ-001 | 安全保卫优先——建国初期国家安全体系建设案例 | 弃用（旧题旨属弃用四式「安全立军」） |
| C-LUORQ-002 | 专门工作与群众路线相结合——镇反运动中的工作方法案例 | 改写重锚（题旨可用，描述需落到素材包引文） |
| C-LUORQ-003 | 预防为主——公安预警机制建设案例 | 删除（「预防为主、防患未然」无源，泛化） |
| C-LUORQ-004 | 军队正规化建设——解放军现代化建设推进案例 | 删除并纠偏（含「国防部长」硬伤；题旨非新素材面） |
| C-LUORQ-005 | 情报主导决策——国家安全战略制定案例 | 弃用（旧题旨属弃用四式「情报先行」） |
| C-LUORQ-006 | 政治可靠优先——公安队伍政治审查案例 | 删除（泛化，无逐条落源） |
| C-LUORQ-007 | 法制化公安建设——新中国第一部公安机关组织法案例 | 改写（原件未获；按素材包口径重锚可核篇目） |
| C-LUORQ-008 | 军队纪律建设——高级干部违纪处理案例 | 重写（以已落源真案例替换泛化叙述） |
| C-LUORQ-009 | 国家安全战略——抗美援朝时期的安全决策案例 | 建议删除（无反证亦无正证；2007 文汇报转述属疑似，W11） |
| C-LUORQ-010 | 历史经验——新中国安全保卫工作体系总结案例 | 弃用（泛化＋旧题旨） |

### 3.3 归属性与引文口径订正（落实）

- 郭兴福教学法两则表述（「郭兴福的教学法是我军传统的练兵方法的继承和发扬……不仅适合于部队，而且适合于学校」）权属订正为叶剑英 1963-12-27 电报，不作为罗瑞卿直接引语（W20/ch063）。
- 「按照毛主席的指示」订正为「依照」（W1）；「我们的公安工作」订正为「我国的公安工作」、「认真正确地解决」订正为「认真地正确地解决」（W6）——引文按订正后文本落盘。
- 1966 年《关于罗瑞卿错误问题的报告》定性文件：不作史实来源、不引原句，仅作语境/反证，引用必须并置 1978 悼词与 1980-05-20 平反通知结论。
- M-001 自设边界两则（「决不会根据一两封告密信去捉人，去杀人……」「决不牵连一个好人，也决不放走一个反革命分子」）为素材包 md §三 边界文本（W1），以边界口径登记（见 §4），不作直接引语单独使用。

### 3.4 无源四式命名弃用（落实）

旧自拟命名「安全立军 / 整编革新 / 参谋统筹 / 情报先行」永久弃用、本档全字段零出现；十条命名全部改为 B1 素材包 §三 可落源描述式命名（对照见 id_mapping.tsv）。

## 4. 片段白名单登记（材料性片段 23 条）

| 模式 | 片段 | 回溯依据 |
| --- | --- | --- |
| M-LUORQ-001 | 按照 |  |
| M-LUORQ-001 | 决不会根据一两封告密信去捉人，去杀人，我们主要是依靠调查研究，依靠证据来办事的 |  |
| M-LUORQ-001 | 决不牵连一个好人，也决不放走一个反革命分子 |  |
| M-LUORQ-001 | 片面宽大 |  |
| M-LUORQ-001 | 纠偏—定策—试点—复盘 |  |
| M-LUORQ-001 | 政府为人民除暴，大快人心 |  |
| M-LUORQ-002 | 建设与使用的矛盾 |  |
| M-LUORQ-002 | 条条与块块关系 |  |
| M-LUORQ-002 | 性质—规模—质量—指挥关系 |  |
| M-LUORQ-003 | 党委绝对领导＋群众路线 |  |
| M-LUORQ-003 | 放手动员群众 |  |
| M-LUORQ-004 | 兵怎么练 |  |
| M-LUORQ-004 | 典型示范—以点带面—评比检验 |  |
| M-LUORQ-005 | 安全—亲民 |  |
| M-LUORQ-006 | 个案严处→制度立规→基层检查→群众监督 |  |
| M-LUORQ-006 | 我们内部如果有很多像宋德贵等这样的共产党员，还得了吗？如果这样，我们就有亡党的危险。 |  |
| M-LUORQ-008 | 冲击一切 |  |
| M-LUORQ-008 | 政治可以冲击其他 |  |
| M-LUORQ-008 | 局部／全局 |  |
| M-LUORQ-008 | 公开表态—私下保留—文本修订 |  |
| M-LUORQ-009 | 还有孤立主义和神秘主义的残余 |  |
| M-LUORQ-009 | 专群结合 |  |
| M-LUORQ-010 | 有限能动 |  |

说明：条目内所有「」/『』片段须为素材包 quotes 子串或白名单登记项；白名单仅收录素材包 md/json 中确有的材料性片段（纠错语境、边界文本、未入 json quotes 的全段文），并逐条给出回溯依据，独立核验脚本复核白名单与片段一致。

## 5. 核验与门禁结果

### 5.1 独立核验 verify_phase21r8_luorq.py

| 组 | 内容 | 结果 |
| --- | --- | --- |
| A | 文件与解析、冻结副本逐字节一致、结构与同链布局一致（figures 含 modes、individuals 去 modes） | PASS 12 |
| B | 条目不变量（id/legacy/figure/类目/级别/priority/verification/英文面/key_concepts/related_modes） | PASS 9 |
| C | 引文 vs 素材包 §三 quotes 子串 | PASS 10 |
| D | 引文 vs 见证文本强归一化命中 | PASS 10 |
| E | 见证文件 sha256 逐一复核（18 件）+ xuoba 分章 59 件 | PASS 2 |
| F | 片段白名单、禁字扫描（10 项） | PASS 5 |
| G | 查重与残留（M 码 0 碰撞；主库六件 0 命中） | PASS 4 |
| H | 归档 4 件 sha 未变；modes_data 顶层旧块保留（合并卡面） | PASS 7 |
| I | 场景处置表 10 条 | PASS 3 |
| J | figure 层（mode_ids/core_thoughts/tags/caveats/篇目/互引） | PASS 6 |
| K | 报告存在 | PASS 1 |
| 合计 | 69 PASS / 0 FAIL / 0 WARN | exit 0 |

### 5.2 credibility gate（--hard-fail，数据面 = 落盘包）

- 硬失败 0 条、exit 0；基线 527 条冻结、D3 豁免 on。
- D4（引文不符）：10 条 unchecked——理由分布 no-fulltext-link 7、no-citation 3；按「不假装核过」口径登记（缓存无原文链接者不可核）。
- D5（时间线矛盾）：10 条 clean、命中 0；年份 token 128 个，过滤理由分布 name-not-in-context 12、source-marker 2、field-not-claim 2。
- 全文：docs/research/phase21r8_luorq_gate.txt。

## 6. 边界与遗留（不属本卡）

### 6.1 合并卡面（等合并卡执行）

- modes_data.json 顶层「H-LUORQ-001」块替换：先备份后替换，替换文见 docs/scratch/legacy20_r8_luorq_landing/top_block_proposal.json（含「国防部副部长（1959 起，兼总参谋长）」纠偏与 one of the ten senior generals 替换）。
- 主库新增注册：M-LUORQ-001~010 进 modes_data / code_maps / scenario_tags / figure_names。
- 旧场景落库与清理：C-LUORQ-001~010 处置执行（表见 §3.2 与 scenario_notes.json）；全库旧叙事清理（含审计/登记面之外的活跃面）。

### 6.2 已知残留登记面（活跃、非叙事面，供合并卡终扫；本卡不擅动）

- data/audit/：phase21r6_id_mapping_ledger.json/.tsv、phase21r_audit.json、phase20R_zengzi_residual_scan.json
- docs/research/：phase21r6C_archive_evidence.json、phase21r6C_archive_report.md、phase21r6C_luorq_isolation_note.md、phase21r7_cgroup_identity_report.md/.json、phase21r8_luorq_sourcing_report.md/.json、legacy20_rev6_assessment.md、phase20_chenghao_orphan_cleanup_evidence.json
- docs/qa/phase21R_restore_report.md；docs/scratch/legacy20_r6c/（归档脚本与登记）；verify_phase21r6C_archive.py
- 未分类命中：无（预检/后检均为 0）。

### 6.3 误删披露（如实登记）

本卡清理动作误删工作仓 untracked 开发目录 scratch/（该目录含其他链的临时开发件，例如 hzx_author.py、build_hzx_landing.py、quarantine_hzx.py、phase21r2/* 等；非 git 追踪文件、非交付物、未影响任何已提交成果与落盘产物的字节）。处置：如实登记于本报告与产出证据；若后续卡需要其内容可由对应流程重生成。教训：清理须仅针对本卡明确产出物。

### 6.4 商榷项（等裁定，不影响本卡完成度）

- 素材包开放项 1：模式 5「警卫思想」替换入选（本卡按素材包选择执行；备选口径为保留毛语转引为第 5 条、警卫为第 11 条）。
- 素材包开放项 2：W4 见证原件未获（维基文库 raw 含 wiki 链接标记，比对按渲染文本），页级引用降为章节级。
- 素材包开放项 3：异文双注（发动/动员；1958-06-11 vs 1958-04-22；八大纪律十项注意时序）——按双注登记，未单方面裁定。
- 素材包开放项 6：顶层块处置随重做裁定（本卡仅备替换文本）。
- 素材包开放项 9：备选未纳入素材（禁毒/反刑讯/宋德贵案/登记政策/军报文风/雷锋宣传）——宋德贵案仅用于 C-LUORQ-008 重写素材。

### 6.5 未动面（核验覆盖）

- data/figures/_duplicates/ 四件归档：字节未变。
- 主库六件：data/modes_data.json（仅顶层旧块保留）、code_maps.json、scenarios_zh.json、scenarios_en.json、scenario_tags.json、figure_names.json——M-LUORQ / C-LUORQ 均 0 命中；「罗瑞卿」字样仅出现于 H-XFZ-001（谢富治）场景文本内，非本链面、未动。
- 备份面（data/backup*、backups*/）与 data/*.bak*：未动。

## 7. 证据与产物路径

- 落盘脚本：tools/build_phase21r8_luorq.py
- 独立核验脚本：verify_phase21r8_luorq.py
- 落盘清单与预检/后检：data/audit/phase21r8_luorq_landing_manifest.json
- 产出证据（含硬伤/场景/白名单登记）：docs/research/phase21r8_luorq_landing_evidence.json
- 核验证据（68 项逐条）：docs/research/phase21r8_luorq_verify_evidence.json
- 门禁全文：docs/research/phase21r8_luorq_gate.txt
- 数据三件：data/figures/H-LUORQ-001.json、data/individuals/H-LUORQ-001.json、data/individuals/H-LUORQ-001_modes.json
- 落地包：docs/scratch/legacy20_r8_luorq_landing/（12 件）
- 素材包（B1）：docs/research/phase21r8_luorq_sourcing_report.md / .json

## 8. 提交回执（落盘后）

- 工作仓提交：21edc5f8（21 件、+9803 行；含数据三件、落地包 12 件、脚本两件、报告/证据/门禁文件）。
- 未提交/未动：主库六件（0 命中、未改）、归档 _duplicates 4 件、备份面；发布仓镜像与 push 属本链后续卡（合并卡 t_08bbb73d）范围，本卡不镜像。
- 交付对象（合并卡 t_08bbb73d 消费清单）：docs/scratch/legacy20_r8_luorq_landing/ 下 modes_library_entries.json、combined_library_entries.json、id_mapping.tsv、category_mapping.tsv、figures/H-LUORQ-001.json、individuals/H-LUORQ-001(.modes).json、scenario_notes.json、top_block_proposal.json；data 三件；data/audit/phase21r8_luorq_landing_manifest.json；docs/research/phase21r8_luorq_landing_evidence.json。
- 预检/后检：全库扫描（跳过备份面）M-LUORQ-001~010 外部碰撞 0；H-LUORQ-001 / C-LUORQ-* 活跃残留登记面清单见 §6.2（供合并卡终扫）。
- 核验复跑口径：verify_phase21r8_luorq.py 69 PASS / 0 FAIL / 0 WARN（exit 0）；credibility gate --hard-fail exit 0。
