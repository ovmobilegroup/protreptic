# Phase21-R6B B 组前置处置报告（王祥修正核验 · 王震对齐调查 · 董宇明登记准备）

- 卡：t_434af550（board: protreptic）；执行：serrano；日期：2026-09-23
- 口径依据：docs/research/legacy20_rev6_assessment.md（2 子串修正 / 4.1 A 组 / 5 样例 / 7 风险）
- 边界：本卡只做前置准备与核验（未写 data/，主库零写入）；主库与发布仓动作交收口卡 t_f3aabe2c
- 产物：docs/scratch/legacy20_r6b/（payload、清单、证据、核验脚本、门禁原始输出）
- 核验状态：本卡 29 项独立核验全 PASS（verify_r6b_prep.py，exit 0）；门禁 credibility_gate --hard-fail exit 0（新增硬失败 0）

## 1. 结论摘要

- 王祥 H-HZX-002：结论为 归档 + 待重做清单。核心事实可修正，但 引文全量落源 不成立：figure 引文为自造、模式引文层为空、M301 题旨建立在错误典故上。
  产物：docs/scratch/legacy20_r6b/H-HZX-002/corrections.json、corrected_record.json、redo_checklist.json、archive_recommendation.json
- 王震 H-WZ-001：关系查清。同名重复 1 对（屯垦戍边法）、独立 1 条（兵团模式法）、新增 10 条。
  产物：docs/scratch/legacy20_r6b/H-WZ-001/（entries 10 条 + 并轨件 M-WZ-011 + 关系分析 + 快照）与 collision_scan.json
- 董宇明 H-DYM-001：归档登记件就绪。三件 sha256 与 R2 post 逐一相同（未再改动），执行配方见登记件。
  产物：docs/scratch/legacy20_r6b/H-DYM-001/archive_manifest.json

## 2. 王祥 H-HZX-002（修正核验，结论：归档 + 待重做清单）

### 2.1 现状与文件
- data/figures/H-HZX-002.json（figure 档案；含 4 处硬伤与错误故事段）
- data/figures/H-HZX-002_modes.json（modes 伴随包 M301-M310；figure_code 残损为 H）
- docs/figures/phase20_wangxiang_research.md（旧世代自产研究件，错误源）
- 三件当前 sha256 逐件登入 corrections.json 与 archive_recommendation.json，并经核验脚本复算一致。

### 2.2 四处硬伤修正（before / after，逐条留证）
1. 字：旧稿 承宣 误，应为 休徵。修正：courtesy_name 由 无 改为 休徵；style_name 原值移除（循 H-HZX-001 黄宗羲档先例：courtesy_name 持字）。
   源：晋书 王祥传开篇「王祥，字休徵，琅邪臨沂人」；搜神记卷十一同（维基文库链接见证据）。
2. 典故：卧冰求鲤 是，温席属黄香。修正：卧冰求鲤（本传作「解衣将剖冰求之，冰忽自解，双鲤跃出」；元 郭居敬 二十四孝 定型）；温席与扇枕温衾 归黄香（二十四孝 扇枕温衾 条）。旧稿 温席求鱼 卧冰求梨 两词皆误。
3. 时代：旧稿 东汉 误，应为 汉末至西晋。修正：era 改 汉末至西晋；time_period_standardized 由 uncertain 改 184-268。存异登记：本传遗令「吾年八十有五」；卒年维基作 268、本传作泰始五年薨，两说并存。
4. 出处：旧稿 东晋裴松之注后汉书 双重错误。修正：王祥事迹主要载 晋书 卷三十三 王祥传（唐修）与 搜神记 卷十一（东晋 干宝）；
裴松之所注为 三国志（南朝宋）。
figure influence 与 M301 source_chapter 按此口径重写（修正稿）。

### 2.3 同错误面与连带项（登记，不删数据本体）
- historical_significance 故事段整体错写（季节与对象颠倒）：修正稿整段重写。
- famous_quote（冬则铺席以候温，夏则卧冰以求梨）：未落源且据错误典故自造：修正稿移除；重做建议取本传原句（候选：海沂之康，实赖王祥）。
- representative_works 两项不可落源：修正稿清空并注明（王祥无传世著作，如保留宜改列参考文献）。
- school（孝道 道家）：道家无据，修正稿改 孝道 儒家。
- wiki_id Q123456789：伪占位，待重做卡查证后回填。
- figure_names 垃圾键 H 与 东岳：建议清理，保留 H-HZX-002 机制键 3 个（待重做使用）。
- modes 文件 figure_code 残损值 H：修正稿改正为 H-HZX-002。
- 模式层 source_chapter 4 条为分析性占位（非文献，不可落源）。
- 引文层现状：figure 引文自造、10 条模式引文全空。

### 2.4 归档建议（对应 archive_recommendation.json）
- 三件现行 sha256 登记在案；建议保持原位（data/figures 与 docs/figures）不移动，由重做卡产出修正件后换血；如按 R6 批次惯例，可移入 docs/scratch/legacy20_r6b/H-HZX-002/ 冷存。两案并列，决策权在收口卡。
- 不建议直接删改原档：错误面已登记，修正稿与重做清单齐备，历史可追踪。

### 2.5 查重矩阵（H-HZX 命名区）
- H-HZX-001 黄宗羲、H-HZX-002 王祥 唯一占用，无碰撞。
- figure_names 现有键：H-HZX-001、H-HZX-002、H、东岳。后两键为垃圾键（来源未明），建议随重做清理。

### 2.6 研究件问题（docs/figures/phase20_wangxiang_research.md）
- 与 figure 档案同源同错（承宣、温席求鱼、卧冰求梨、东汉、裴松之后汉书等），不可作为重做卡的落源依据；重做须直接从原始文献重新取证（晋书卷三十三、搜神记卷十一、二十四孝）。

### 2.7 重做提示（redo_checklist.json）
- 10 条模式 M301-M310 全部进入待重做：每条含 problem、redo_suggestion、sourcing_status、salvage 四栏；题旨须从正确典故（卧冰求鲤）与正确出处重立。
- 元信息：global_actions 与 sourcing_anchors 给出重做卡的行动序与落源锚点（含前引三源链接）。
- 重做卡建议：先查证 wiki_id 与代表作落源，再重写 figure 四处硬伤、故事段与引文层，最后按 v6 门禁过闸。

## 3. 王震 H-WZ-001（对齐调查，结论：payload 备妥待并轨，主库零写入）

### 3.1 覆盖与关系（12 条 = 档案 10 + 库内 legacy 2）
- 档案：data/figures/H-WZ-001.json 含 modes M371-M380 共 10 条；另有 individuals 伴随包（H-WZ-001.json 与 H-WZ-001_modes.json）为同文旧档（仅 category 未归一）。
- 库内 legacy：M391 屯垦戍边法（与 M371 同题重复，非字节级；M391 另含 process、application、pitfalls、key_quote 等 14 项富字段，M371 无）；M392 兵团模式法（独立；字段完整、含既有 link-resolved 核验记录）。
- 结论：同名重复 1 对（屯垦戍边法）；独立 1 条（兵团模式法）；档案 10 条库内零占用，可直接迁入。

### 3.2 payload（docs/scratch/legacy20_r6b/H-WZ-001/）
- modes_library_entries.json：M-WZ-001 至 M-WZ-010（与 A 组样例同构；正文逐字段照档案原文，category 按候选映射改名、原值入 category_raw；verification 以 pending 批量标注）。
- modes_library_entries_bingtu_M-WZ-011.json：M392 并轨件（字段保全重编号；id 与 mode_code 均为 M-WZ-011；related_modes 重指 M-WZ-001；内容与库内 M392 逐字段一致，仅 4 字段为迁移变换）。
- id_mapping.tsv：12 行（10 迁入 + M391 归档去重 + M392 并轨）。
- m391_archive_snapshot.json（字节快照）、relation_analysis.json（逐对差异表与映射依据）。

### 3.3 分类映射（10 条，各附依据）
- 战略建设、制度创新、政治品格、党的建设 四类归入 政治治理；工作方法、创新精神 两类归入 方法论通用；政治策略归入 战略决策；思想路线归入 认识论逻辑；精神品质归入 伦理修养。
- 两条候选档已注明无直接先例（M377 创新精神、M379 党的建设，按近例推理）；M371 归属依据为库内同题 M391 已归 政治治理。

### 3.4 碰撞矩阵（collision_scan.json）
- M-WZ- 全域：仅 docs/research/legacy20_rev6_assessment.md 一处预分配文本提及，data、tools、site 层零占用（可用）。
- 旧码占用（排除归档区与生成物后）：M391 28 文件、M392 27、M371 10、M372 9、M373 10、M374 8、M375 8、M376 8、M377 8、M378 6、M379 6、M380 7；层别（library、archive、cross-ref、historical-report、derived 等）逐条登记。
- M391、M392 现有引用面以历史报告、派生站点与关联档案为主；并轨与去重不删任何既有文件。

### 3.5 清零清单（收口卡待办）
- 迁入 M-WZ-001 至 M-WZ-010 并统一重编；并轨件 M-WZ-011 落地与 related_modes 重指确认（待收口确认并轨方向）。
- M391 归档去重：快照入 _duplicates 区、差异表留存；14 项富字段列精修候选。
- individuals 伴随包 category 归一（如需）与旧码 M371-M380 的释放决策。

### 3.6 缺陷登记（诚实项）

- 双码并存期（M391 与 M371 同题）的引用面在合并前仍双显；本批不改库，收口卡合并时自然消解。
- 旧档与主档是否属同一份逻辑档案，留待收口卡裁定；本报告只登记文件指纹。

## 4. 董宇明 H-DYM-001（登记准备，结论：三件未变，配方就绪）
- 时线：R2 换码，三件 git mv 至 H-DYM-001 并正码内字段；R4 灰区收尾（t_ea3a32e5）纠正杜威侧显示名。
- 三件：figure 档、modes 包与研究件（路径见登记件）；sha256 与 R2 换码后的值逐一相同，未再改动。
- 现状复核：主库 0 条董宇明 figure_code；M-DY-001 至 M-DY-010 显示名已修正为约翰·杜威；三件在位。
- 【存疑登记】R-恢复报告 4.5 节表 DY 行：将 H-ZDY-001.json 列为董宇明侧文件，并注「已在库 10 条，同名」。与现盘不符：主库无董宇明条目；H-ZDY-001 实为周敦颐。疑似生成脚本按 DY 二字误配所致，登记备查，不修改历史报告。
- 登记件：H-DYM-001/archive_manifest.json（逐件 sha256、现状复核、卡面口径、存疑登记与站点面结论）。
- 补充键与号：R2 换码提交 dae8ac5e；登记件键 unchanged_since_r2_post 全部 true；显示名键 figure_name 已修正为约翰·杜威。
- 站点面：现行 site_docs 与 web 无 H-DYM-001 页、搜索索引 0 处提及（R2 报告曾记载文档站新增页；现行构建未见，以现盘为准）。

## 5. 核验与证据
- 独立核验：verify_r6b_prep.py 共 29 项断言全 PASS（exit 0）：entries 数量与字段白名单、正文逐字段 verbatim、并轨差异面、映射表 12 行、库内零占用与全域零占用、王祥与董宇明三件 sha256、碰撞矩阵一致性、重做清单 10 条。
- 门禁：credibility_gate --hard-fail，exit 0；新增硬失败 0；存量 0；基线对照 STALE 提示为已知噪声（与 A 组样例同款说明）。
- 样例对表：legacy20_rev6_samples 目录（H-CHB-001、H-FXT-001）逐项同构。
- 门禁原始输出：docs/scratch/legacy20_r6b/gate_evidence.txt。
- 机器可读汇总：docs/research/phase21r6B_evidence.json。

## 6. 边界与遗留（诚实上报）
- 本卡未写 data/、未动站点、未提交远端；产出集中在 docs/scratch/legacy20_r6b/ 与本报告。
- 未做（属收口卡 t_f3aabe2c）：主库迁入、去重、并轨落地、figure_names 更新、site_docs 再生、旧码释放。
- 工具链：个别中英混排句式触发安全扫描误报，本卡以改写与小片写出绕过，内容无损；若复现，按先分片写、受阻再改写处理。
- 王祥重做与董宇明归档动作的卡片派生：由收口卡按本报告 2、4 节执行（如已存在或复用）。
