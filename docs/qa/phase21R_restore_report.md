# Phase21-R 主库数据修复报告：恢复 16 位人物缺失模式块 + 恩克鲁玛补缺 + 全量审计

- 卡：t_3e74b456（board: protreptic）
- 日期：2026-09-22
- 仓库：workspace master（/opt/data/workspace/Protreptic）→ publish main（/opt/data/release/Protreptic-publish）
- 计划与逐条溯源：scratch phase21r/plan2.json（每条恢复记录带 src/provenance/conflicts 字段）
- 机器可读审计：data/audit/phase21r_audit.json

## 0. 摘要

| 项目 | 修复前 | 修复后 |
|---|---|---|
| 主库条目（raw modes 列表） | 2948 | 3142 |
| distinct mode_code | 2938 | 3132 |
| 空 mode_code 条目（历史，未动） | 10 | 10 |
| 重复 mode_code | 0（空码组除外） | 0（空码组除外） |
| 站点 modes(源) | 2858 | 3132 |
| 站点 modes(发布) | 2798 | 3072 |
| by-figure 分片 | 278 | 304 |
| figures | 1057 | 1057 |

恢复总量 194 条 / 20 位人物：A 组 14 位×10=140、C 组 2 位×10=20、引用闭包 2 位×10=20、
恩克鲁玛 +4（补齐 10/10）、李斯 10（B 组核验后恢复）。

门禁（两仓各自跑）：credibility_gate --hard-fail、verify_findings --hard-fail、
verify_source_links --hard-fail 全部 exit 0（新增 0）；export_static_site 产物断言全绿（1371 文件）；
pages_preflight --stage data 全部断言通过；两仓 parity 0 差异。

## 1. 背景与根因

卡面结论（可复核）：主库 data/modes_data.json 在 9/9 大重写提交 91832eb6（"Fix M381-M390 mode ID conflict"）
之后，一批已在 9/7-9/9 完成「Phase 21 增量合并入主库」的人物模式块持续缺失；
9/10-9/17 的 boards→workspace「全量镜像」未将其带回（boards 副本同缺，publish 仓同缺）。

本次实测（修复前快照 backup_modes_data_20260922_172740.json）：
- 主库 2948 条，A 组 14 人 + C 组 2 人在库条目数均为 0；
- 恩克鲁玛仅 6 条（M-NKR-001~005、010）；
- 李斯 M-QIN-* 0 条；
- 另发现引用闭包缺口：库内 related_modes/图档引用了 M-SOP-*/M-THU-*，而两个块在库内缺失
  （证据见第 6 节 gate 输出：M-HOM-002 等 6 条 NEW D6 悬空引用）。

## 2. 恢复清单（逐人物，修复前→修复后）

| # | 组 | figure_code | 人物 | 来源 | 条数 | id 范围 |
|---|----|-------------|------|------|------|---------|
| 1 | A | H-BLT-001 | 柏拉图 | archive, commit:072bd72a | 10 | M-BLT-001~M-BLT-010 |
| 2 | A | H-DA-001 | 道安 | commit:0e78ffa5 | 10 | M-DA-001~M-DA-010 |
| 3 | A | H-DRK-001 | 德鲁克 | archive, commit:5a4758fa | 10 | M-DRK-001~M-DRK-010 |
| 4 | A | H-GX-001 | 郭象 | archive, commit:e51bdae6 | 10 | M-GX-001~M-GX-010 |
| 5 | A | H-GYW-001 | 顾炎武 | archive, commit:959525d4 | 10 | M311~M320 |
| 6 | A | H-JMLS-001 | 鸠摩罗什 | commit:1b8c56ce | 10 | M-JMLS-001~M-JMLS-010 |
| 7 | A | H-JY-001 | 贾谊 | commit:99a47440 | 10 | M-JY-001~M-JY-010 |
| 8 | A | H-SJM-001 | 释迦牟尼 | archive, commit:a6c37c4d | 10 | M-SJM-001~M-SJM-010 |
| 9 | A | H-SQR-001 | 苏格拉底 | archive, commit:f8514b54 | 10 | M-SQR-001~M-SQR-010 |
| 10 | A | H-SY-001 | 商君 | archive | 10 | M-SY-001~M-SY-010 |
| 11 | A | H-WB-001 | 王弼 | commit:af79031a | 10 | M-WB-001~M-WB-010 |
| 12 | A | H-XFZ-001 | 谢富治 | archive | 10 | M-XFZ-001~M-XFZ-010 |
| 13 | A | H-YLS-001 | 亚里士多德 | archive, commit:47bf8546 | 10 | M-YLS-001~M-YLS-010 |
| 14 | A | H-ZHX-001 | 朱熹 | commit:8e4e5dd4 | 10 | M-ZHX-001~M-ZHX-010 |
| 15 | B-QIN | H-QIN-001 | 李斯 | archive | 10 | M-QIN-001~M-QIN-010 |
| 16 | C | Coubertin | 顾拜旦 | archive, figure-embed | 10 | M-COU-001~M-COU-010 |
| 17 | C | Homer | 荷马 | archive, figure-embed | 10 | M-HOM-001~M-HOM-010 |
| 18 | C-closure | Sophocles | 索福克勒斯 | boards-archive, boards-figure-embed | 10 | M-SOP-001~M-SOP-010 |
| 19 | C-closure | Thucydides | 修昔底德 | boards-archive, boards-figure-embed | 10 | M-THU-001~M-THU-010 |
| 20 | D-NKR | H-NKR-001 | 恩克鲁玛 | commit:c949e76d, figure-embed | 4 | M-NKR-006~M-NKR-009 |

## 3. 来源、交叉校验与字段处置

### 3.1 来源优先级与逐条溯源
- 来源 1：合并 commit chunk —— `git show <合并commit>:data/modes_data.json` 提取该人物块（首选，字段最全）；
- 来源 2：档案侧 —— data/individuals/<code>_modes.json（v6 映射）或 data/figures/<code>.json 内嵌 modes；
- 来源 3：boards 副本 —— /opt/data/kanban/boards/protreptic/data/**（C 组与引用闭包来源）。
- 每条恢复记录的 src/provenance/conflicts 均落盘于 plan2.json（逐字段记录取自哪个来源）；
  两源都有时按「字段以更全者为准」逐字段取用，未出现无法裁决的冲突（plan2.json conflicts = []）。
- A 组中 4 人（道安 0e78ffa5 / 朱熹 8e4e5dd4 / 贾谊 99a47440 / 王弼 af79031a）只有 commit 单源可用：
  其 individuals 档案为旧世代 thinking_modes 结构（例：data/individuals/H-ZHX-001_modes.json 只有
  mode_id / mode_name_zh / definition_zh 等字段，未含 v6 的 source_chapter / key_quote 等），不能作为 v6 字段来源。

### 3.2 字段归一之一：王弼 related_modes -> failure_pitfalls_zh
- 现象：af79031a payload 中 H-WB-001 的 related_modes 字段内容为自由文本失败陷阱
  （如「章句训诂式的字句穿凿…」，与 docs/figures/H-WB-001.md 一致），并非模式编号；
- 处置：迁移为 failure_pitfalls_zh（内容保真、原键不再占用）；不新增、不改写任何文本；
- 记录：plan2.json transforms（10 条），audit json normalizations.WB_field_rename。

### 3.3 字段归一之二：恩克鲁玛 category 三元组 -> 标准类目（库内 + 图档同步）
- 现象：c949e76d payload 与 data/figures/H-NKR-001.json 内嵌中，M-NKR-006~009 的
  name_zh / name_en / category 三个字段被写成同一个三元组 [短名, 英文名, 领域标签]（上游载荷生成缺陷）；
- 影响：category 为三元组时，tools/export_static_site.py 的 domain 清洗回退失效，
  站点构建断言会报 4 条 domain_zh 超 30 字符（修复前 dry-run 复现该报错）；
- 处置：按同人物既有 6 条的既定归一规则（三元组第 3 项首段 -> 库内标准类目：
  政治* -> 政治治理, 哲学* -> 哲学形而上, 个人品格 -> 伦理修养）把 category 归一为字符串：
  M-NKR-006 政治治理 / M-NKR-007 哲学形而上 / M-NKR-008 哲学形而上 / M-NKR-009 政治治理；
  同时同步 data/figures/H-NKR-001.json 内嵌同名 4 处（保证库与图档 0 mismatch）；
- 原始值可从 git（c949e76d 与 HEAD^）及 boards/workspaces/t_d6a190f8 完整回滚，不丢信息；
- 只动这 4 条新建条目，既有 6 条一笔未动。

### 3.4 验证状态
- 194 条恢复条目均携带合法 verification 四态（恢复过程把状态块并入条目，不另写名单副本）；
  全库口径自洽：公开 3082 + 隔离 60 = 全库 3142（apply_verification_status.py 断言通过）。

## 4. 全量审计结果（F 脚本重跑 + E 组条目 + B 组结论）

### 4.1 F1 v6 型 claims 扫描（船长版脚本原样重跑）
- 重跑结果：18 件清单已收敛为 2 件，且两条均为已知例外、依据明确；未决 0 条。
- data/figures/H-BG-001.json 缺 10 条：E1 码系（该档持 H-BG-001 / M-BG-*，库内 canonical 为 M-BAN-*，10 条在库）；
- data/individuals/H-SJL-001_modes.json 缺 10 条：E2 旧码（canonical H-SHA-001 / M-SHA-* 在库）。

### 4.2 F2 合并提交x现库交叉表（对每个代号判 0 与不足 10）
- 从 124 个 merge-ish 提交代号中筛出不足 10 的 8 个，逐条注依据（未决 0 条）：
  - BG 0/10：E1 码系（库内 M-BAN-* 10 条，figure_code=BAN）；
  - CH 0/10：H-CH-001 已清档旧码（工作仓档案已删，本次同步删除发布仓同名 4 件）；
  - DZS 1/10：董仲舒 10 条在库（figure_code=H-DZS-001），id 为 M01~M10 旧编号，非 M-DZS-* 口径；卡外遗留；
  - GYW 0/10：本次恢复；上游 id 为 M311~M320（959525d4 payload），按 figure_code=H-GYW-001 计 10/10；
  - SJL 0/10：E2 旧码副本，canonical M-SHA-* 在库；
  - SQIN 0/10：已核清，入库码为 M-SQ-*（10 条在库）；
  - SX 0/10：H-SX-001 已知隔离（QUARANTINE，M393-M402），不得恢复；
  - ZX 0/10：B 组曾子，见 4.6，列待决策。

### 4.3 F3 观察项：仅 mode_code、无 id 字段的条目（诚实上报）
- 现状：全库 3142 条中，2742 条有 id、390 条无 id（约 400 条量级，与卡面估计一致）、10 条无 mode_code（历史空码组）；
- 本地恢复的 194 条全部带 id（0 条落在此观察项内）；
- 影响评估：以 mode_code 为键的工具链（export_static_site / credibility_gate / verify_findings /
  build_figures_db / 前端索引）不受影响 —— 实测产物断言与门禁全绿（第 5 节）；
  受影响的只有以 id 集合判归属的扫描（如 F1 脚本的 ids 集），故 F1/F2 判读须以 mode_code / figure_code 口径为准；
- 无 id 条目的分布：Bismarck、CatherineII、Leibniz、Tesla、Edison、WrightBrothers、Jenner、ZhangQian 等
  旧批人物各 10 条（多为 2026-09 前期批次），是否补 id 属结构归一议题，本卡不改（卡面列为观察项）。

### 4.4 findings.json 变化（data/audit/findings.json，已随本次刷新）
| defect | 恢复前 | 恢复后 | 增量 |
|---|---|---|---|
| D1_pseudo_figure | 60 | 60 | +0 |
| D2_fabricated_source | 10 | 10 | +0 |
| D3_source_contamination | 6 | 6 | +0 |
| D4_quote_mismatch | 22 | 23 | +1 |
| D4_quote_without_source | 17 | 27 | +10 |
| D5_timeline_conflict | 1 | 1 | +0 |
| D6_orphan_reference | 40 | 38 | -2 |
| **合计** | **156** | **165** | **+9** |

- 新增标记条目：M-ZHX-001~010（D4_quote_without_source，朱熹批忠实恢复所致：上游 8e4e5dd4 payload
  未含 source_chapter 字段，档案侧为旧世代 thinking_modes 亦无来源字段，未补造）与 M-WYM-003（并行卡）；
- 移除标记条目：M-NKR-010（D4 口径变化，非删改数据）；
- D6 悬空引用净减 2（引用闭包补齐收益）；D5/D3/D2/D1 不变。

### 4.5 E 组：编码归一与旧档分类（核验输出，本卡未改）
- E1 班固：同一人物两套码并存 —— figure 档持 H-BG-001 / M-BG-*，库内 canonical 为 M-BAN-*（figure_code=BAN，10 条在库）。
  建议参照 ZX -> ZHX 先例统一为单码（推荐保留库内 M-BAN-*，figure/档案侧改名），或至少在工具白名单显式记录该别名。
- E2 商羯罗：SJL 为旧码副本（332c0ad3 曾合并），canonical H-SHA-001 已在库。
  建议按 H-CH-001 清档先例归档/清档 SJL 侧档案；canonical 保留 H-SHA-001。
- E3 旧世代编号文件 20 件（claims 为 M### 老编号、主库无对应条目；本卡不动，逐件清单如下）：

| 编号 | 姓名 | figure 档 | 载荷 | 库内 | git 记录 | 建议 |
|---|---|---|---|---|---|---|
| AN | 安子 | H-AN-001 | H-AN-001.json(10,legacy-M###); H-AN-001_modes.json(10,legacy-M###) | 0 | 0 | 待决策: 载荷在档 (10 条, legacy-M###) 但库内 0 条 -> 旧世代未入库; 单独评估 v6 复刻 or 归档 |
| CHB | 陈伯达 | H-CHB-001 | H-CHB-001_modes.json(10,legacy-M###); H-CHB-001.json(10,v6) | 0 | 1 | 待决策: 载荷在档 (10 条, legacy-M###) 但库内 0 条 -> 旧世代未入库; 单独评估 v6 复刻 or 归档 |
| CY | 陈云 | H-CY-001 | H-CY-001.json(10,legacy-M###); H-CYP-001.json(10,v6) | 0 | 2 | 待决策: 载荷在档 (10 条, legacy-M###) 但库内 0 条 -> 旧世代未入库; 单独评估 v6 复刻 or 归档 |
| DY | 董宇明 | H-DY-001 | H-DY-001_modes.json(10,legacy-M###); H-ZDY-001.json(10,v6) | 10 | 0 | 已在库: 10 条 (H-...-001 同名) -> 档案归档, 无需恢复 |
| DYC | 邓颖超 | H-DYC-001 | H-DYC-001_modes.json(10,legacy-M###); H-DYC-001.json(10,legacy-M###) | 0 | 1 | 待决策: 载荷在档 (10 条, legacy-M###) 但库内 0 条 -> 旧世代未入库; 单独评估 v6 复刻 or 归档 |
| FXT | 费孝通 | H-FXT-001 | H-FXT-001_modes.json(10,legacy-M###); H-FXT-001.json(10,v6) | 0 | 0 | 待决策: 载荷在档 (10 条, legacy-M###) 但库内 0 条 -> 旧世代未入库; 单独评估 v6 复刻 or 归档 |
| HAN | 沈幅 | H-HAN-001 | H-HAN-001_modes.json(8,legacy-M###); H-HAN-001.json(8,v6) | 0 | 1 | 待决策: 仅部分载荷 (H-HAN-001_modes.json(8),H-HAN-001.json(8)) -> 单独评估 |
| HZX-002 | 王祥 | H-HZX-002 | H-HZX-002.json(10,v6) | 0 | 0 | 待决策: 载荷在档 (10 条, v6) 但库内 0 条 -> 旧世代未入库; 单独评估 v6 复刻 or 归档 |
| JX | 纪弦 | H-JX-001 | H-JX-001.json(10,v6) | 0 | 0 | 待决策: 载荷在档 (10 条, v6) 但库内 0 条 -> 旧世代未入库; 单独评估 v6 复刻 or 归档 |
| KKQ | 康克清 | H-KKQ-001 | H-KKQ-001.json(10,v6) | 0 | 1 | 待决策: 载荷在档 (10 条, v6) 但库内 0 条 -> 旧世代未入库; 单独评估 v6 复刻 or 归档 |
| LC | 陆沉 | H-LC-001 | H-YLC-001.json(10,v6) | 0 | 0 | 待决策: 载荷在档 (10 条, v6) 但库内 0 条 -> 旧世代未入库; 单独评估 v6 复刻 or 归档 |
| LUORQ | 罗瑞卿 | H-LUORQ-001 | H-LUORQ-001_modes.json(10,legacy-M###) | 0 | 0 | 待决策: 载荷在档 (10 条, legacy-M###) 但库内 0 条 -> 旧世代未入库; 单独评估 v6 复刻 or 归档 |
| LWH | 李维汉 | H-LWH-001 | H-LWH-001_modes.json(10,legacy-M###); H-LWH-001.json(10,v6) | 0 | 1 | 待决策: 载荷在档 (10 条, legacy-M###) 但库内 0 条 -> 旧世代未入库; 单独评估 v6 复刻 or 归档 |
| MODERN-002 | 大云 | H-MODERN-002 | 无 | 0 | 0 | 待决策: 无模式载荷, 仅元数据 -> 归档或立项补做 |
| SQL | 宋庆龄 | H-SQL-001 | H-SQL-001.json(10,v6); H-SQL-001.json(10,v6) | 0 | 1 | 待决策: 载荷在档 (10 条, v6) 但库内 0 条 -> 旧世代未入库; 单独评估 v6 复刻 or 归档 |
| WL | 万里 | H-WL-001 | 无 | 0 | 0 | 待决策: 无模式载荷, 仅元数据 -> 归档或立项补做 |
| WZ | 王震 | H-WZ-001 | H-WZ-001.json(2,v6); H-WZ-001_modes.json(2,legacy-M###) | 2 | 2 | 已在库: 2 条 (H-...-001 同名) -> 档案归档, 无需恢复 |
| YE | 叶筱 | H-YE-001 | H-YE-001_modes.json(10,legacy-M###); H-YE-001.json(10,v6) | 0 | 0 | 待决策: 载荷在档 (10 条, legacy-M###) 但库内 0 条 -> 旧世代未入库; 单独评估 v6 复刻 or 归档 |
| YSK | 杨尚昆 | H-YSK-001 | H-YSK-001_modes.json(10,legacy-M###); H-YSK-001.json(10,v6) | 0 | 0 | 待决策: 载荷在档 (10 条, legacy-M###) 但库内 0 条 -> 旧世代未入库; 单独评估 v6 复刻 or 归档 |
| ZOU | 邹文献 | H-ZOU-001 | H-ZOU-001_modes.json(10,v6) | 0 | 0 | 待决策: 载荷在档 (10 条, v6) 但库内 0 条 -> 旧世代未入库; 单独评估 v6 复刻 or 归档 |


### 4.6 B 组结论（核验后处置）
- 李斯 H-QIN-001：核验确认丢失后按 A 组口径恢复 —— 修复前主库 0 条含李斯的条目、亦无 M-QIN-*；
  别名检索仅命中李商隐（M-LIS-*，20 条，属另一人物）与苏秦（M-SQ-* 在库）两处已核先例，均非李斯别名；
  恢复 10 条（源 a3467e1d + individuals 档案交叉校验），恢复后 figure_code=H-QIN-001 计 10/10。
- 曾子 H-ZX-001：列待决策（不恢复），证据如下：
  - figure 档 data/figures/H-ZX-001.json 存在（figure_name=曾子，16899 B）但仅元数据，无 modes / mode_ids；
  - individuals 档 data/individuals/H-ZX-001_modes.json 缺失（工作仓与 boards 副本均无）；
  - 主库 0 条（无 M-ZX-*、无曾子条目）；
  - git 全历史无独立合并提交；--grep 曾子 仅见 9c074ddd / 5956dd8b 等提交中的
    「H-ZX-001 -> H-ZHX-001 曾子误码」交叉引用修复记录（即该码被曾子占用，朱熹上游码因此改 ZHX）；
  - 结论：属从未入库（而非丢失），无载荷可恢复 —— 本卡不编造内容；是否立项补做请船长定。

## 5. 门禁、站点重建与计数锚点

### 5.1 门禁（工作仓实际命令与结果）
| 步骤 | 命令 | 结果 |
|---|---|---|
| 可信度门 | `python3 tools/credibility_gate.py --hard-fail --data-path data/modes_data.json` | exit 0，存量 525 条冻结（D1=60 D2=9 D3=0 D6=456），新增 0 |
| findings 门 | `python3 tools/verify_findings.py --hard-fail --data-path data/modes_data.json` | exit 0，存量 0 条，新增 0 |
| 引证链接 | `python3 tools/verify_source_links.py --hard-fail` | exit 0，无新增坏链（存量 0 冻结） |
| 站点导出 | `python3 tools/export_static_site.py` | exit 0，产物 1371 文件；figures=1057 modes(源)=3132 modes(发布)=3072 隔离=60 by-figure=304；体积断言通过 |
| 数据门 | `python3 tools/pages_preflight.py --stage data` | [OK] stage=data 全部断言通过（隔离命中=0） |
| 两仓 parity | `python3 tools/check_repo_parity.py` | exit 0，0 差异 |

沙箱前置（先立后破）：恢复前先在沙箱副本上跑门禁，找出「哪些内容必须一并恢复才不新增硬失败」。
证据：只放 A/C/D 计划（无引用闭包）时门禁报 NEW D6 悬空引用（例：M-HOM-002 -> M-SOP-004、
M-HOM-006 -> M-THU-005 等 6 条）；把 boards 侧的索福克勒斯 / 修昔底德两块（引用闭包）并入后降为 0 新增。
这就是本卡在 A / C 组之外恢复 SOP / THU 两块（共 20 条）的依据来源。
幂等与回滚：apply_plan.py 复跑在写盘前 ABORT（幂等自检）；恢复前备份
phase21r/backup_modes_data_20260922_172740.json（2948 条），可整库回滚。

### 5.2 站点数据重建与计数锚点新旧值
- 工作仓链条：build_figures_db -> export_static_site -> gen_web_site_counts -> build_daily_index ->
  pages_preflight --stage data -> build_search_index -> build_graph_data -> build_unified_index（全部 exit 0）；
- 发布仓链条：同链条在发布仓重跑（全部 exit 0），preflight 打印
  figures=1057 modes=3132 published=3072 隔离命中=0 by-figure=304。

| 计数锚点 | 修复前 | 修复后 | 位置 |
|---|---|---|---|
| EXPECT_MODES | 2858 | 3132 | tools/export_static_site.py 与 tools/pages_preflight.py（单一构建源同步改） |
| EXPECT_BY_FIGURE | 278 | 304 | 同上 |
| EXPECT_FIGURES | 1057 | 1057 | 同上（不变） |
| EXPECT_MODE_INDEX_SHARDS | 8 | 8 | 同上（不变） |
| meta.mode_summaries | 2858 | 3132 | web/public/data/meta.json（现场生成产物） |
| meta.mode_summaries_published | 2798 | 3072 | 同上 |
| by-figure 分片数 | 278 | 304 | 同上 |

- 增量分解：3132 = 2858 + 80（并行 Phase20 批尚未同步进站点的增量）+ 194（本卡恢复）；
  304 = 278 + 26（本卡新增分片 + 并行批分片）；
- 跟踪型产物：docs/architecture/static_data_manifest.json、web/src/generated/siteCounts.ts
  （3072 条模式 x 304 位人物）；web/public/data/** 为 .gitignore 产物，由 CI 现场重建。

### 5.3 恢复条目与 figure 内嵌的一致性核验

- 方法：对 194 条恢复条目，逐一在对应 data/figures/<figure_code>.json 的内嵌 modes 中按 id 找同一条目，逐字段比对；
- 有 dict 条目的内嵌共 34 条覆盖恢复 id：H-YLS-001 10、H-SJM-001 10、H-DRK-001 10、H-NKR-001 4；
  这 34 条的内容字段（name_zh / name_en / definition_zh / definition_en / domain_* / key_quote_* / source_chapter 等）
  与内嵌逐字一致 —— 差异只出现在 3 个「库内专属」字段：verification（34 条，内嵌本不含验证块）、
  figure_name（34 条，内嵌为 null）、figure_code（30 条，内嵌为 null），即内嵌侧本无这些键，非内容冲突，内容 mismatch = 0；
- 其余 160 条：对应图档的内嵌形态是 mode_ids 清单或仅图档元数据（无条目体），无条目体可比对；
  其 id 与库内一一对应（F1 claims 扫描 0 缺失佐证）；
- 恩克鲁玛 4 条的 category 归一已同步进图档内嵌（第 3.3 节），故这 4 条同为 0 内容差异。

## 6. 两仓同步与 parity

- 工具口径：tools/check_repo_parity.py（构建图文件逐字节 sha256；含未跟踪但不被 .gitignore 的文件；排除产物/备份/不参与构建者，排除项带理由）；
- 同步前：96 差异（CONTENT_DIFF 38、仅工作仓 54、仅发布仓 4）；
- 同步动作：92 文件工作仓 -> 发布仓（含 data/modes_data.json、figures/individuals/docs 镜像、audit 产物、
  tools 计数锚点、siteCounts.ts），4 文件在发布仓删除（H-CH-001 清档 4 件：figure/individuals x2/docs md）；
- 同步后：parity exit 0、0 差异；
- 发布仓门禁：credibility_gate --hard-fail exit 0（存量 525 / 新增 0）、verify_findings --hard-fail exit 0（0/0）、
  数据链条与 preflight 全绿；
- 说明：本次发布仓同步为「镜像工作仓现状」，其中含并行卡在制但未同步的 Phase20 批次内容（80 条模式及配套文档），
  这些内容已在工作仓提交入库，站点重建的 EXPECT 增量因此一并覆盖它们；发布仓提交信息中已列明。

## 7. 遗留与观察（诚实上报，本卡未擅自处理）

1. verification 状态漂移 73 条：`python3 tools/apply_verification_status.py --check` exit 1
   （72 条 verified -> pending、1 条 verified -> suspect；样例 M-CHE-001~005，多为并行卡 H-CHE-001 批，
   checked_at=20260922_122743 为该卡合并脚本所写）。恢复前快照上复现同样 73 条 -> 非本卡引入；
   CI 不跑 --check，本次未越权改他卡状态。
2. H-DY-001 码冲突：data/figures/H-DY-001.json 与 data/figure_names.json 现持「董宇明」（legacy 载荷），
   而主库 figure_code=H-DY-001 的 10 条为杜威（M-DY-001~010，2026-09-10 1c13431e 入库）—— 归一/换码建议报船长，本卡不动。
3. 旧世代编号文件 20 件（第 4.5 节清单）：均未入库、载荷在档（多为 legacy M### 编号），本卡不动。
4. findings 软性观察：本次恢复使 findings.json 增 10 条 D4_quote_without_source（朱熹批上游载荷无 source_chapter），
   属软性报告项（不触发 hard-fail），已在 4.4 说明。
5. 隔离名单未触碰：H-SX-001、H-P23F-001、P24F、P25F、P26F、Phase27Final 均未恢复、未进入公开产出（export 隔离命中=0）。
6. 并发写注意：data/modes_data.json 为多卡共享工作副本，本次提交前的最后一次整库写由本卡完成；
   提交内容含并行卡已落盘但未提交的少量字段热修（如 H-ZXC-001 批引文修复），按仓库先例随本提交入库。
7. data/audit/verification_status.json 为并行卡 2026-09-22 的 apply_verification_status --write 登记产物：
   其 inputs.sha256 记录的是生成时刻的盘上库 sha（d649f973…），与本次提交后的库 sha（83be45b5…）不同，
   属登记时点差（该文件自述如此），非数据不一致；全库四态口径仍自洽（公开 3082 + 隔离 60 = 全库 3142）。

## 8. 附录：复现命令清单

- 恢复前后逐人物计数：`python3 scratch/phase21r/per_figure.py`（工作副本；等价数据见 data/audit/phase21r_audit.json restore 段）；
- 恢复计划（逐条溯源）：`scratch/phase21r/plan2.json`（entry 级 src / provenance / conflicts）；
- 应用恢复（含幂等自检）：`python3 scratch/phase21r/apply_plan.py --plan plan2.json --apply`；
- F1 / F2 审计脚本：卡面 F.1 / F.2 原文（本次重跑输出见 data/audit/phase21r_audit.json audit_F 段）；
- 门禁：见 5.1 表内命令；
- 两仓 parity：`python3 tools/check_repo_parity.py --json`（期望 exit 0、diffs 空）；
- 计数锚点自检：`python3 tools/pages_preflight.py --stage data`（期望打印 modes=3132 published=3072 by-figure=304）。

## 9. 提交与推送状态

- 工作仓（master）：数据/文档提交 `0309093a`（16 路径：主库 modes_data.json + 图档镜像 6 件 +
  data/audit 产物与报告 + 计数锚点 2 件 + siteCounts.ts + static_data_manifest.json + api/protreptic.db），
  随后报告修订提交 `b1310553`；data/modes_data.json 为多卡共享文件，随提交一并入库的还有并行卡已落盘未提交的
  少量字段热修（第 7 节第 6 条）。
- 工作仓 master 的远端：origin 上只有 main 一条分支（发布支线），master 无远端同名分支，
  故本次不推送 master（与仓库既有流程一致：工作仓内容以镜像方式进入发布仓）；
  工作仓仍留有并行卡在制未提交文件：data/audit/verification_status.json、docs/figures/H-LJY-001.md、
  docs/research/phase20_zhoudunyi_qa_evidence.txt（其内容已在发布仓镜像提交）。
- 发布仓（main）：镜像提交 `bc8efec` + 报告修订提交 `5ebffe5`，均已 push 到 origin/main；
  推送后核验：`git status --short` 无剩余改动、`git rev-list --count origin/main..HEAD` = 0（干净且齐平）。
- 本报告自身的后续修订提交会使 HEAD 再前移一位，最终提交哈希与推送回执以 kanban 卡 t_3e74b456 的
  完成交接（summary / metadata）为准。

（报告完）
