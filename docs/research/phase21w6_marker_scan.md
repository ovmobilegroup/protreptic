# Phase21 W6 全仓标记扫描报告（候选归并）

- 卡 t_51db608d ［Phase21 W6］全仓「待办/待核/待重做/旁项/未闭环」标记扫描 → 候选归并（只读·零提交·零库写）
- 生成 2026-09-24 02:10:44 +0800，由脚本 phase21w6_marker_scan.py 自动生成
- 仓库 /opt/data/workspace/Protreptic，分支 master，HEAD bd039538
- 本报告 pair 保持未提交（与 W4 清单先例一致，随下个收口卡提交；backlog 台账已预登记 [待生成] 条目）

## 1. 扫描口径

- 范围（卡面）： docs/**/*.md、tools/**/*.py、api/**/*.py、scripts/**/*.py、web/src/**/*.{ts,vue,js}、根目录 *.md、tools/*.json（不超过 200KB 者）
- 排除（卡面）： data/**、docs/archive/**、web/node_modules、web/dist、.git、__pycache__、*.xlsx、*.bak*、data/backup_*、data/merge_staging_*、tools/json/scenarios_*.json、*.min.*、docs/scratch/**
- 最终 regex（原样未删改，脚本内为 REGEX_STR）： `待办|待核|待重做|待复验|待补|旁项|未闭环|暂缓|待议|TODO|FIXME|TBD`
- 计数口径： 1 条记录 = 文件 × 行号 × 去重标记；同一行含多个不同标记时分别计条
- 术语标注（微调披露）： 标记「待核」若全数落在「待核验 / 待核名」词形内、且同行含下条状态词之一或紧随计数数字，标注为术语命中；保留计数与记录，仅不进入 A 类净候选表
- 状态词表（术语判定用）： 已核验 / 存疑 / 一手材料 / 四态 / 缺省态 / schema / 徽章 / badge / pending / chip / 核验状态 / 尚未核验
- 自排除（披露）： 本报告 pair 在扫描前剔除（防自引用、保复跑一致）；为卡面排除表的一处增补
- JSON 扩展字段（披露）： 记录含 term 布尔字段；基础字段为 file / line / marker / bucket / snippet / ann（ann 即初判注解）
- 边界： docs_site/** 不在卡面范围（未计入）；docs/research/_archive/ 仅含 .json（按范围自然跳过）；tools/json/**/*.json 共 647 件，实测含标记 111 件 / 874 行（多为「待补充」占位），不在 tools/*.json 字面范围，一并披露供船长定夺是否扩面

## 2. 计数表（marker × bucket）

| 标记 | A 活跃面 | B 历史面 | C 已知/在途 | 合计 | 其中术语命中 |
|---|---|---|---|---|---|
| 待办 | 3 | 0 | 3 | 6 | 0 |
| 待核 | 40 | 30 | 15 | 85 | 41 |
| 待重做 | 0 | 0 | 15 | 15 | 0 |
| 待复验 | 0 | 0 | 0 | 0 | 0 |
| 待补 | 10 | 6 | 8 | 24 | 0 |
| 旁项 | 0 | 0 | 6 | 6 | 0 |
| 未闭环 | 1 | 6 | 1 | 8 | 0 |
| 暂缓 | 9 | 1 | 0 | 10 | 0 |
| 待议 | 0 | 0 | 0 | 0 | 0 |
| TODO | 1 | 9 | 0 | 10 | 0 |
| FIXME | 0 | 0 | 0 | 0 | 0 |
| TBD | 1 | 1 | 0 | 2 | 0 |
| 合计 | 65 | 53 | 48 | 166 | 41 |

- 命中文件 82 个；命中行 165 行；记录 166 条（多标记行按标记分别计条）
- 扫描文件 872 个（范围与排除应用后）

## 3. A 类 top40 候选表（净候选；已剔除术语命中）

| 序 | file:line | 标记 | 一句话摘录 |
|---|---|---|---|
| 1 | api/typing_extensions.py:3457 | TODO | # TODO: Use inspect.VALUE here, and make the annotations lazily evaluated |
| 2 | tools/audit_figure_fields.py:64 | 待核 | "[安萨里](Al-Ghazali), 是否统一为安萨里留待船长裁定 -> 同时进待核名清单", |
| 3 | tools/fix_qa_batch4.py:159 | 待补 | f"描述待补充", |
| 4 | tools/fix_qa_batch4.py:160 | 待补 | f"步骤待补充", |
| 5 | tools/fix_qa_batch4.py:161 | 待补 | f"适用场景待补充" |
| 6 | tools/fix_qa_batch4.py:184 | 待补 | f"描述待补充", |
| 7 | tools/fix_qa_batch4.py:185 | 待补 | f"步骤待补充", |
| 8 | tools/fix_qa_batch4.py:186 | 待补 | f"适用场景待补充" |
| 9 | tools/json/merge_lizhi_scenarios.py:149 | TBD | pattern_en = r'("H-LZ-169":\s*\{[^}]*"description_en":\s*"\[TBD\] H-LZ-169 description"\s*\})' |
| 10 | tools/og_image.py:278 | 待核 | chips = [("时代 · %s" % era) if era else "时代待核", |
| 11 | tools/test_thinking_mode_selector.py:39 | 待补 | # db 里引用了模式目录中尚不存在的 id —— 属数据层待补项。 |
| 12 | tools/test_thinking_mode_selector.py:46 | 待补 | # 允许"暂无思维模式"的场景比例上限（当前约 3.4% 属数据层待补；大幅劣化即失败） |
| 13 | tools/test_thinking_mode_selector.py:111 | 待补 | print('✓ 名称: %d/%d 个场景有真实名称（其余退化为 code，属数据层待补）' |
| 14 | tools/update_templates_with_new_figures.py:73 | 待补 | appendix += f"／ **{code}** ／ {name} ／ 待补充 ／ 待补充 ／ {modes} ／\n" |
| 15 | docs/figures/H-ATK-001.md:70 | 暂缓 | - 四步过程: 重定义单位：把政治忠诚从王朝与宗教共同体改写为语言与居所界定的民族，明确新契约的基本盘 → 三变量测量：以人口多数、语言分布、可防守地理三角定位核心区，区分『必须争』与『必须弃』... |
| 16 | docs/figures/H-CY-001.md:23 | 待核 | - 类目归一：10 条按映射表归一（category_raw 保留原值），0 条不在表内按原值保留并标记待核 |
| 17 | docs/figures/H-DAV-001.md:115 | 待办 | - 定义: 达·芬奇手稿中最动人的部分不是答案而是问题：他记录『啄木鸟用什么舌头』『鳄的下颚如何工作』『为何鱼在水中比海中物体的影子快』——有的问题三十年间被反复重访。他展示了好奇心的工程化：好... |
| 18 | docs/figures/H-DRK-001.md:116 | 待办 | - **操作过程**：["双清单分流：把待办分为'恢复昨日的问题'与'创造明天的机会'两类，禁止混排", "机会注入：检查优秀人才与增量预算的去向——若70%以上在救问题，即为平庸信号", "系... |
| 19 | docs/figures/H-HFZ-001.md:94 | 待核 | - **M-FEI-001** (needs_verification): 待核：库中 H-FEI-001（'非人'）条目对法家机器化治理的论述与韩非体系高度相关，但人物本体不同，待下游核查后再... |
| 20 | docs/figures/H-JX-001.md:21 | 待核 | - 类目归一：10 条按映射表归一（category_raw 保留原值），0 条不在表内按原值保留并标记待核 |
| 21 | docs/figures/H-LNC-001.md:525 | 暂缓 | **定义**: 1862 年 7 月，林肯已向内阁宣读初步解放宣言草稿，西华德劝阻：此时发布等于败仗之后的哀鸣。林肯把草稿收回抽屉，公开承认判断已定、发布待时——他在等待一个不可逆的军事支点。9... |
| 22 | docs/figures/H-MAI-001.md:231 | 暂缓 | - 预防滑坡：明示'双重归档'与'两真并存'的区别——归档是暂缓裁决并保留唯一实践标准，不是承认两套互斥真理都真 |
| 23 | docs/figures/H-SQL-001.md:20 | 待核 | - 类目归一：5 条按映射表归一（category_raw 保留原值），5 条不在表内按原值保留并标记待核 |
| 24 | docs/figures/H-SU-001.md:522 | 暂缓 | **领域**: 对权威结论保持系统性的暂缓相信，并以多源独立证据互证后才收纳为认知：『事不目见耳闻而臆断其有无，可乎』——把『存疑』制度化为求知的第一道工序 |
| 25 | docs/figures/H-WL-001.md:21 | 待核 | - 类目归一：10 条按映射表归一（category_raw 保留原值），0 条不在表内按原值保留并标记待核 |
| 26 | docs/figures/H-WL-001.md:22 | 待核 | - 引文归属勘误：M-WL-001（旧 M274）key_quote 白猫黑猫语通行归属邓小平，旧载荷置于万里名下；本卡按现状保真保留原文并标注 attribution_note，待核验卡处置 |
| 27 | docs/figures/H-WL-001.md:63 | 待核 | - 归属标注: 引文归属勘误（Phase21-R6 批1）：『不管白猫黑猫，抓住老鼠就是好猫』通行归属为邓小平语，旧载荷置于万里名下；本卡按现状保真保留原文，仅作此标注，待核验卡处置。 |
| 28 | docs/figures/H-YSK-001.md:18 | 待核 | - 类目归一：7 条按映射表归一（category_raw 保留原值），3 条不在表内按原值保留并标记待核 |
| 29 | docs/figures/H-ZX-001.md:375 | 未闭环 | - QA 遗留观察（QA 报告 §6，非本卡引入）: ① `legacy_field_aliases` 为说明性留证字段（10 条独有）；② 图档 `source_files` 含非路径描述项；... |
| 30 | docs/04-training/daily_thinking_training.md:49 | 暂缓 | → 功能延期暂缓（市场窗口还有一个月）。 |
| 31 | docs/06-ai-collaboration/thinking_mode_ai_templates.md:182 | 待办 | 【待办事项】 |
| 32 | docs/06-ai-collaboration/thinking_mode_ai_templates.md:217 | 暂缓 | - **可暂缓**：[⚪事项] |
| 33 | docs/07-coaching/thinking_mode_journal.md:56 | 暂缓 | 3. 集中全部运维资源修复服务器，功能延期暂缓 |
| 34 | docs/07-coaching/thinking_mode_journal.md:61 | 暂缓 | - ❌ 做错了什么：没有提前和员工沟通暂缓计划，导致部分人心浮动 |
| 35 | docs/07-coaching/thinking_mode_meeting_templates.md:754 | 待核 | ### 待核实的信息 |
| 36 | docs/09-evolution/knowledge_system_evolution.md:144 | 暂缓 | "bad": "没有提前和员工沟通暂缓计划", |
| 37 | docs/research/phase21r6_landing_batch1_report.md:45 | 待核 | ／ 件 ／ 人物 ／ 载荷来源 ／ 旧号到新号 ／ 互引条数 ／ 类目归一（应用/待核） ／ 场景附随件 ／ 备份登记 ／ |
| 38 | docs/research/phase21r6_landing_batch1_report.md:57 | 待核 | ## 3. 类目归一（船长裁定口径：照样例映射表批量应用；表外者按原值保留 + 标记待核） |
| 39 | docs/research/phase21r6_landing_batch1_report.md:78 | 待核 | ### 3.2 待核（8 条，按原值保留，未应用） |
| 40 | docs/research/phase21r6_landing_batch1_report.md:94 | 待核 | - **WL 引文勘误**（报告 §7-2 与卡面要求）：M-WL-001（旧 M274）的 key_quote「不管白猫黑猫，抓住老鼠就是好猫」通行归属为邓小平，旧载荷置于万里名下；处置为引文... |

- A 类合计 65 条；其中术语命中 21 条；净候选 44 条；本表排序 = 代码面优先，其后 README 与档案页、方法论文档、研究文档，组内按 file 与 line 确定性排序取前 40
- 提示：暂缓与待办等词在训练示例、模板与模式正文中存在自然语义用法，本表按字面命中列出，需人工判是否为待办标记；完整净候选见 JSON records 中 bucket=A 且 term=false 者
- A 面术语命中分布（按文件）： README.md × 2；docs/community/zhihu_launch_post.md × 4；tools/gen_web_site_counts.py × 1；tools/prerender_body.py × 1；tools/site_counts.py × 3；web/src/App.vue × 1；web/src/components/CredibilityBadge.vue × 3；web/src/components/EntryCard.vue × 1；web/src/router/index.ts × 2；web/src/views/ConceptsView.vue × 1；web/src/views/CredibilityView.vue × 2

## 4. 附录 B：历史过程面命中分布（按文件聚合，供人工判过期）

| file | 条数 | 样例摘录 |
|---|---|---|
| docs/qa/phase38_y3_report.md | 10 | ／ `pending` ／ `○ 待核验` ／ 灰 ／ 可信度：待核验 —— 尚未核验（schema 缺省态） ／ |
| tools/build_legacy20_r6_batch1.py | 5 | 2) 类目归一（样例映射表为准 + 本卡扩展候选；不在表内者按原值保留并标记待核） |
| docs/planning/credibility_framework.md | 3 | ／ `pending` ／ 未核验（缺省） ／ ○ 待核验 ／ |
| docs/qa/phase45_acceptance.md | 3 | - 未暗示「全部已考证」：草稿第 84–102 行专门开「可信度：我不打算假装每条都可信」，并**如实公布四态**「已核验 888 /... |
| docs/architecture/phase30_a3_og_image.md | 2 | 468 字, 先砍括号/破折号注解再截断), N 条思维模式, 领域; 没有时代数据的显示「时代待核」. |
| docs/qa/phase30_c4_followup_r1r2.md | 2 | ／ MD056 表格列数 ／ `comparison_matrix` 表头多一列（5→4）；`phase2_candidates` 3... |
| docs/qa/phase38_acceptance.md | 2 | - `○ 待核验` (1547) — 白色半透明 |
| docs/research/legacy20_rev6_assessment.md | 2 | ／ DY ／ 董宇明 ／ H-DY-001 ／ figures/H-DY-001.json=10（M-DY-001-010，内容实为杜... |
| docs/research/phase20R_zengzi_archive_report.md | 2 | - 归档后档案结构：九章齐备（1 Overview / 2 Ten Thinking Modes / 3 Attribution No... |
| docs/research/phase20R_zengzi_residual_inventory.md | 2 | ／ 20 ／ `data/figures/H-PGR-001.json (cross_references)` ／ external-... |
| docs/research/phase2_detailed_research.md | 2 | ## 5. 研究空白与待补齐项 |
| docs/architecture/san-martin_schema_evolution.md | 1 | - D3：自由文本字段（region/topic/source_refs）是否进枚举？→ 建议暂缓，先字符串后治理。 |
| docs/islam_phase2_review_report.md | 1 | - 检测模板指示词：`example`, `sample`, `template`, `placeholder`, `待定`, `待填... |
| docs/qa/phase20R_zengzi_qa_report.md | 1 | 5. 根目录旧档 `modes_data.json`（101 图块汇编，含曾子旧号块）仍在，为残留清单 #16 未闭环项——建议编排另... |
| docs/qa/phase36_acceptance.md | 1 | 3. **W4 · 两仓字节级一致未达**：全量比对 44/2363 共同 tracked 文件 hash 不同（含 `.github... |
| docs/qa/phase38_y2_link_injection.md | 1 | （渲染成纯文本 + 「待核验」徽章，符合预期） |
| docs/qa/phase44_acceptance.md | 1 | 已核验 888 · 待核验 1547 · 存疑 23 · 一手材料 340 |
| docs/research/candidates_v2_research.md | 1 | ／ 李时珍/孙思邈/张…（源文件此行被截断，待补） ／ 中医药学群体 ／ 待补：该行在初始提交 782a1ad 即截断；其中李时珍已收... |
| docs/research/phase20R_zengzi_merge_report.md | 1 | - 残留清单 #16 未闭环（交接项）：根目录旧档 modes_data.json（610KB 级、101 图块汇编、内嵌曾子旧号块 ... |
| docs/research/phase20_daizhen_archive_report.md | 1 | - 归档后档案结构：七章齐备（一历史定位 / 二核心思想 / 三十大思维模式 / 四双语场景索引 / 五跨引用 / 六现代价值 / 七... |
| docs/research/phase20_daizhen_merge_report.md | 1 | 9. 档案 md > 20KB、10 模式定义中英逐字等于库内、含 20 条双语场景索引、无 TODO/替换字符； |
| docs/research/phase20_lujiuyuan_archive_report.md | 1 | - **回归拦截记录（诚实披露）**：初稿把三镜像哈希记作缩写 `8a61a691…ede8`，触发上游第 43 项与 QA 6.3「... |
| docs/research/phase20_lujiuyuan_qa_report.md | 1 | 6. `docs/figures/H-LJY-001.md` 33831 B，10 模式全字段（定义/流程/案例/现代应用）与库内**... |
| docs/research/phase20_wangfuzhi_merge_report.md | 1 | 9. 档案 md > 20KB、10 模式定义中英逐字等于库内、含 20 条双语场景索引、无 TODO/替换字符 |
| docs/research/phase20_wangfuzhi_qa_report.md | 1 | 8. `docs/figures/H-WFZ-001.md` 53,330 B：10 模式**全字段**（名称/定义/流程/案例/应用... |
| docs/research/phase20_wangyangming_qa_report.md | 1 | 5. `docs/figures/H-WYM-001.md` 46173 B，10 模式核心字段与库内**逐字一致**，含双语场景索引... |
| docs/research/phase20_zengzi_research_final.md | 1 | - `data/figures/H-PGR-001.json` `cross_references` 含 `H-ZX-001`——指向... |
| docs/research/phase20_zhangxuecheng_archive_report.md | 1 | - 归档后档案结构：七章齐备（一历史定位 / 二核心思想 / 三十大思维模式 / 四双语场景索引 / 五跨引用 / 六现代价值 / 七... |
| docs/review/consistency_review_v2.md | 1 | - 空键条目 (1 个): 含 `modes: [146,147,148]` 但所有文本字段为"待补充"，属模板脏数据 |

- B 类合计 53 条；其中术语命中 18 条

## 5. C 类对照说明（已知或在途；不重复登记，仅列对照计数）

对照词表（逐条抄录自 backlog 台账或队列点名；匹配规则 = 文件路径含词，大小写不敏感）：

| 词 | backlog 依据 |
|---|---|
| luorq | 台账 luorq QA 产物 39 件 untracked，t_65998945 在途；队列 R8-B 罗瑞卿链收尾 |
| h-luorq-001 | 台账 H-LUORQ-001.md 两仓 byte-same 复验 |
| wangxiang | 队列 R8-A 王祥链收尾；台账 王祥遗留已清 t_a8f544f5 |
| azj | 队列 R8 遗留清档链 AZJ 全链清除进行中 t_3669eb4a |
| phase21w4 | 台账 W4 recon/manifest 未提交；W4 台账 4 |
| phase21r8_w4 | 台账 phase21r8_w4_names_recon 未提交 |
| phase21w5 | 台账 W5 遗留数据层已清 t_9f3ccb2c，等卡回执 |
| phase21r6b | 队列 R8-A 王祥链追溯：R6B 前置轮与台账 王祥遗留已清 |
| phase21r7 | 队列 R8-B 罗瑞卿链与 R8 遗留清档链追溯：R7 轮核名与旁项已收口 |

C 类明细（按文件）：

| file | 条数 | 对照来源 |
|---|---|---|
| docs/qa/phase21r6B_execution_report.md | 5 | 台账点名 phase21r6b |
| docs/qa/phase21r7_leftovers_report.md | 3 | 台账点名 phase21r7 |
| docs/research/phase21r6B_prep_report.md | 6 | 台账点名 phase21r6b |
| docs/research/phase21r6B_wangxiang_redo_list.md | 3 | 台账点名 wangxiang phase21r6b |
| docs/research/phase21r7_cgroup_identity_report.md | 4 | 台账点名 phase21r7 |
| docs/research/phase21r7_wangxiang_sourcing_report.md | 4 | 台账点名 wangxiang phase21r7 |
| docs/research/phase21r8_azj345_disposition.md | 4 | 台账点名 azj |
| docs/research/phase21r8_luorq_merge_report.md | 1 | 台账点名 luorq |
| docs/research/phase21r8_luorq_sourcing_report.md | 6 | 台账点名 luorq |
| docs/research/phase21r8_w4_names_recon.md | 3 | git 在途；台账点名 phase21r8_w4 |
| docs/research/phase21r8_wangxiang_merge_report.md | 2 | 台账点名 wangxiang |
| docs/research/phase21r8_wangxiang_rebuild_report.md | 1 | 台账点名 wangxiang |
| docs/research/phase21w4_fix_manifest.md | 2 | git 在途；台账点名 phase21w4 |
| docs/research/phase21w5_wangchong_sourcing_report.md | 2 | 台账点名 phase21w5 |
| tools/build_phase21r8_wangxiang.py | 2 | 台账点名 wangxiang |

- C 类合计 48 条；其中术语命中 2 条
- 实时 git 在途集合件数 36（git status --porcelain，另含未跟踪目录前缀： data/backup_merge_H-ZDY-001_20260922_131851/, data/backup_merge_H-ZDY-001_20260922_132324/, data/backup_merge_H-ZDY-001_20260922_132519/, data/backup_phase21r8_azj345_clear_20260923/, docs/research/_archive/）

抽查 5 条（C 类与 backlog 对照正确性）：

| file:line | 对照来源 | backlog 原文摘录要点 | 结论 |
|---|---|---|---|
| docs/research/phase21r8_luorq_sourcing_report.md:46 | 台账点名 luorq | 台账 luorq QA 产物 39 件 untracked，t_65998945 在途 | 一致 |
| docs/research/phase21r8_wangxiang_merge_report.md:46 | 台账点名 wangxiang | 台账 王祥遗留 → 已清，t_a8f544f5 交付，两仓 byte-same 复核 | 一致 |
| docs/research/phase21r8_azj345_disposition.md:5 | 台账点名 azj | 队列 AZJ 全链清除进行中，备份目录 30 件 与 _duplicates 8 件已生成 | 一致 |
| docs/research/phase21r8_w4_names_recon.md:189 | git 在途；台账点名 phase21r8_w4 | 台账 W4 recon/manifest 未提交：phase21r8_w4_names_recon.* 与 phase21w4_fix_manifest.* | 一致 |
| docs/research/phase21w5_wangchong_sourcing_report.md:263 | 台账点名 phase21w5 | 台账 W5 遗留 tools×4 source_texts source_links 报告 见证 → 数据层已清 t_9f3ccb2c | 一致 |

## 6. 复跑命令

    cd /opt/data/workspace/Protreptic
    python3 /opt/data/cache/scratch/phase21w6_marker_scan.py

- 预期终端摘要行 RECORDS=... LINES=... FILES=... SCANNED=... A=... B=... C=... TERM=...
- 计数一致：本报告第 2 节与 phase21w6_marker_scan.json 的 counts 字段由同一次运行的内存数据生成，复跑后可用摘要行比对
- 只读保证：脚本仅写 4 个产物路径（本报告 pair 加 scratch 副本），其余零写；零 git 提交

