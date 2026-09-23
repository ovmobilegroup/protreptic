# Phase21-R6 A 组 10 件合并入主库报告（卡 t_10089b19）

- 日期：2026-09-23
- 卡：t_10089b19（barbosa · 数据归并与资产入库）
- 前置提交：60a14a38（合并前 HEAD，全部备份与基线核验均对该 commit object）
- 输入落盘：docs/scratch/legacy20_rev6_landing/batch1（陈云 / 宋庆龄 / 杨尚昆 / 万里 / 纪弦）与 batch2（陈华必 / 傅玄同 / 邓友昌 / 孔克勤 / 蓝蔚华）
- 输出：data/modes_data.json、data/code_maps.json、data/scenarios_zh.json、data/scenarios_en.json、data/scenario_tags.json
- 独立核验脚本：verify_r6_merge_indep.py（仓根，第二实现）
- 审计 manifest：data/audit/phase21r6_merge_manifest.json

## 1. 合并结果（实测计数）

| 文件 | before | after | 增量 | 说明 |
|---|---|---|---|---|
| data/modes_data.json（modes 数组） | 3162 | 3262 | +100 | 纯追加（旧 3162 条逐对象全等） |
| data/code_maps.json（figures） | 212 | 215 | +3 | 7 件既有条目引用面重指 + 3 件新增注册 |
| data/scenarios_zh.json | 2183 | 2213 | +30 | 陈云/纪弦/傅玄同 各 10 条 |
| data/scenarios_en.json | 2183 | 2213 | +30 | 同上（键=zh 键+E） |
| data/scenario_tags.json（平铺） | 7278 | 7478 | +200 | 100 模式 zh/en 双语标签 |
| data/figure_names.json | 1098 | 1098 | 0 | 本卡零写入（10 件登记齐全，仅复核） |

工作区 diff 行数（git diff --numstat，仅上表五文件）：modes_data +7097/-0；code_maps +352/-218；scenario_tags +1250/-50；scenarios_zh +260/-30；scenarios_en +260/-30。
（code_maps 与场景/标签的删除行全部为编号重指的同一行替换，非内容删除。）

## 2. 十件清单（mode 新号 / 场景 id / 注册）

| 件 | 人物 | 批 | 旧号段 | 新号 | 场景 zh / en | code_maps |
|---|---|---|---|---|---|---|
| H-CY-001 | 陈云 | 1 | M101-M110 | M-CY-001..010 | C-CY-001..010 / -010E | 既有（10 叶重指） |
| H-SQL-001 | 宋庆龄 | 1 | M361-M370 | M-SQL-001..010 | C-SQL-001..010 / -010E | 既有（38 叶重指） |
| H-YSK-001 | 杨尚昆 | 1 | M431-M440 | M-YSK-001..010 | 无附随件 | 新增注册（15 tags / 1 xref） |
| H-WL-001 | 万里 | 1 | M274-M283 | M-WL-001..010 | C-WL-001..010 / -010E | 既有（30 叶重指） |
| H-JX-001 | 纪弦 | 1 | M001-M010 | M-JX-001..010 | C-JX-001..010 / -010E | 新增注册（15 tags / 3 xrefs） |
| H-CHB-001 | 陈华必 | 2 | M211-M220 | M-CHB-001..010 | C-CHB-001..010 / -010E | 既有（40 叶重指） |
| H-FXT-001 | 傅玄同 | 2 | M341-M350 | M-FXT-001..010 | C-FXT-001..010 / -010E | 既有（30 叶重指） |
| H-DYC-001 | 邓友昌 | 2 | M321-M330 | M-DYC-001..010 | 无附随件 | 既有（30 叶重指） |
| H-KKQ-001 | 孔克勤 | 2 | M321-M330 | M-KKQ-001..010 | 无附随件 | 既有（40 叶重指） |
| H-LWH-001 | 蓝蔚华 | 2 | M341-M350 | M-LWH-001..010 | 无附随件 | 新增注册（10 tags / 3 xrefs） |

注意：邓友昌与孔克勤各自持 M321-M330 段（名称不同，非同一模式），傅玄同与蓝蔚华各自持 M341-M350 段。重指一律按「本件自己的 id_mapping.tsv」作用域执行，绝不跨件套用。

## 3. 只做四件事（边界）

1. modes 纯追加 100 条（逐字复制落盘条目，含 legacy_mode_id / legacy_fields / verification 留证字段，零改写）。
2. code_maps 引用面重指（旧号到新号，仅本批十件自身条目）。
3. code_maps 新增 3 件注册（H-YSK-001 / H-JX-001 / H-LWH-001：mode_ids + tags + cross_references）。
4. 场景与标签的引用面重指 + 新增（zh/en 各 30 条场景、200 条标签），以及 EN 场景码风格裁定（见第 4 节）。

未做（如实登记）：figure_names 零写入；modes_data 标量字段 total 保持 3162（合并只追加数组，未改标量；manifest 已登记该漂移）；documents/figures 档案层、tools/json 副本、dist 构建物均未触碰。

## 4. EN 场景码风格裁定（落盘批1报告移交第 7.3 项）

- 裁定：统一为库约定「en 键 = zh 键 + E」。落盘载荷中纪弦件 en 键为 C-JXE-001（中缀式），已改回 C-JX-001E；陈云件 C-CY-001 亦归一为 C-CY-001E（该件内嵌 code 字段同步）。
- 账：scenarios_en.json 内 10 个键改名（C-JXE-001E..010E 到 C-JX-001E..010E），改名前与改名后 sha256 一并记入 evidence/rework_en_keys.json。
- 旁证：库内既有 C-SQL-001E / C-WL-001E / C-CHB-001E 同批先例同风格；基线无任何 EE 结尾键。

## 5. 引用面重指明细（引用面随迁，零跨件误伤）

- code_maps 叶改动 218 处（既有 7 件）：宋庆龄 38、孔克勤 40、陈华必 40、傅玄同 30、万里 30、邓友昌 30、陈云 10 —— 独立核验逐叶断言「新值等于本件 id_mapping 的映射值」，218/218 全部命中，无越界改写。
- scenarios 重指 60 处（zh 30 + en 30）：C-SQL / C-WL / C-CHB 三组的 mode_id 由旧号改为新号，条目其余字段逐对象全等。
- scenario_tags 重指 50 处：平铺 10（傅玄同件 M341..M350）+ dict 级 40（傅玄同件 20 + 宋庆龄件 20，键名不改）。
- 十件自身条目旧号零残留（新号命名 M-<COD>-NNN；旧号仅存于 legacy_mode_id / legacy_fields 留证字段，独立核验按字段白名单放行）。

## 6. 站点链条与锚点（五步全部 exit 0）

- tools/export_static_site.py（去重 3252 / 发布 3192 / by-figure 分片 316 / figures 1057）
- tools/gen_web_site_counts.py（siteCounts.ts：3192 x 316；四态 932/1886/34/340）
- tools/apply_site_counts.py（dist 扫描零违规；docs 门面 6 页零违规）
- tools/build_daily_index.py（3192 条 / 316 位 / 分片 316）
- tools/pages_preflight.py --stage data（figures=1057 modes=3252 published=3192 隔离命中=0 by-figure shards=316；daily 3192；全部断言通过）
- 锚点更新：tools/export_static_site.py 与 tools/pages_preflight.py 的 EXPECT_MODES 3152 到 3252、EXPECT_BY_FIGURE 306 到 316（EXPECT_FIGURES 1057 不变）。

## 7. 门禁（复跑，原始输出见卡工作区 evidence/）

- tools/credibility_gate.py --hard-fail --data-path data/modes_data.json：exit 0（新增硬失败 0，存量 524 冻结）
- tools/verify_findings.py --hard-fail --data-path data/modes_data.json：exit 0（新增 0；build_audit_findings.py --write 已刷新 sha）
- tools/verify_source_links.py --hard-fail：exit 0（新增坏链 0）
- tools/apply_verification_status.py --check：exit 0（无漂移）

## 8. 独立核验（verify_r6_merge_indep.py，第二实现）

- 口径：基线一律经 git show 60a14a38:<path> 读 commit object；全部期望值从落盘载荷与 id_mapping.tsv 独立推导。
- 覆盖：A 组 15 项（纯追加/唯一性/悬空/留证字段）、B 组 16 项（重指映射/注册/悬空/残留）、C 组 11 项、D 组 8 项、E 组 3 项、F 组 4 项门禁、G 组 4 项站点链条、H 组 4 项交付物。
- 自我修正（如实上报）：核验脚本初版有两处判据缺陷（EN 码归一推导过于宽松、ADDED 判据按值比对），已修正后复跑；两处缺陷均在核验脚本自身，不涉及数据缺陷。

### 核验结果

- 最终复跑：83 PASS / 0 FAIL / 3 INFO，exit 0（机器可读 docs/research/phase21r6_merge_evidence.json；控制台誊本 卡工作区 evidence/verify_final_console.txt）。
- 口径（本卡提交后他卡落盘的口径修订，如实登记）：合并态经 git show d0f1bb65:<path> 读（MY 口径），基线经 git show 60a14a38:<path> 读（PRE 口径），另加 I 组 6 项「当前工作区存活复核」（他卡可增删自身项，仅断言本批 100 号 / 十件注册 / 30+30 场景 / 200 标签仍存活）。
- 三处 INFO：新增号足迹（M-CY-001 起 / M-LWH-010 止）、十件历史悬空存量（H-SQL-001 指向 H-MZD-001 / H-ZET-001，非本批引入）、当前口径计数快照。
- 修订缘由：R6C 卡（t_4a9cf2cb）于本卡提交后落盘 7b767f39，撤下其自件登记（figure_names 9 键 / code_maps 3 条目 / scenarios zh·en 各 30 条；modes_data 零写入），绝对计数随之变化；核验脚本改为「MY 合并态 + 当前存活」双口径后复跑全过（执行于 d0f1bb65 之后的运行时事实，非数据改动）。

## 9. 备份与回滚

- 备份目录：/opt/data/kanban/boards/protreptic/workspaces/t_10089b19/backup/merge_r6_20260923/（六文件字节副本，sha256 与 60a14a38 逐一致，独立核验已断言）
- 回滚：从该目录拷回 data/ 对应五文件（figure_names 未写入，无需回滚）即可回到前置状态。

## 10. 已知漂移与遗留（非本卡引入）

- data/modes_data.json 顶层 total 字段为 3162（数组已 3262）——合并只追加数组未改标量，manifest 已登记为漂移。
- code_maps 悬空存量：H-SQL-001 的 cross_references 指向 H-MZD-001 / H-ZET-001，二者在 figures/code_maps/figure_names 三层均不可解析（合并前后集合完全一致，非本次引入）；独立核验以「本批零新增悬空」为断言口径。
- scenario_tags 键名未改（C-SQL-0010、env_un_strategy_actions_zh 等历史命名保留原样），不在本卡口径内。
- 跨卡观察（仅登记，本卡不动作）：R6C 撤下 H-LC-001 注册后，本批 H-CY-001 的 cross_references 目标 H-LC-001 在现状中不可解析；该件列入 R6C「待身份清单 6 件」，随其后续处理消解。

## 11. 移交

1. QA 独立审计卡（如已建）：按本报告第 1/5/8 节逐项复核；机器可读记录见 docs/research/phase21r6_merge_evidence.json 与 data/audit/phase21r6_merge_manifest.json。
2. 站点链条：本地五步已通过；发布仓镜像与推送回执见第 12 节。
3. 后续批次：按船长批次表继续（他卡在制）。

## 12. 提交与推送

- 工作仓提交：d0f1bb65（master，14 路径：五数据文件 + audit/findings + 合并 manifest + static_data_manifest + 报告/证据 + 两工具锚点 + siteCounts + 核验脚本）。工作仓远端仅 main 分支（本仓不作为发布通道），未推送。
- 发布仓提交：48afa7b（main），内容与工作仓构建图文件一一对应（本卡 13 条构建图路径逐文件 sha256 一致，见 evidence/mirror_completeness.json）。
- 镜像：复制 207 路径 / 归档移除 1 路径（data/H-DYC-001_modes.json 归入 data/backup_r6_H-DYC-001_20260923/）/ 跳过 5 路径（他卡未跟踪在制）。日志 evidence/mirror_log_r6a.json、镜像前 parity evidence/parity_pre_json.json。
- 推送回执：git push origin main -> 65eb1c8..48afa7b（main）；复核 git ls-remote --heads origin 得远端 main = 48afa7bbf235ca474fde0cfeac7ecda17b4a979e。
- 快照后差异（如实登记）：post parity（evidence/parity_post_json.json）新增 58 项他卡后续提交，其中 R6C 卡已落盘 7b767f39（C 组 7 件清档：_duplicates 落位、自件登记撤下 9/3/30/30、LUORQ 载荷隔离说明），另有 phase21r6_id_mapping_ledger、data/figure_names.json 随动、R5 收尾 efe7a806 等；均属镜像快照之后的新提交，由各卡自身镜像步骤消解，本卡不代镜像。
- 收尾提交（本卡）：报告/manifest/证据与核验脚本口径修订随最终提交落盘（见 §12 之后的提交记录）。

## 13. 证据索引

- data/audit/phase21r6_merge_manifest.json（计数、哈希、重指账、门禁与链条记录）
- docs/research/phase21r6_merge_evidence.json（独立核验机器可读结果）
- verify_r6_merge_indep.py（仓根，可复跑）
- 卡工作区 /opt/data/kanban/boards/protreptic/workspaces/t_10089b19/：evidence/（门禁与链条原始输出、锚点更新记录、EN 码改名账、核验草稿）、scripts/（合并脚本与修复脚本）、backup/merge_r6_20260923/
