# Phase21-R6B B 组收口执行报告（卡 t_f3aabe2c）

- 卡：t_f3aabe2c（[Phase21-R6B] B 组收口：王祥入库/归档 · 王震对齐 · 董宇明登记）
- 日期：2026-09-23；工作区基线 commit 98f34377（Phase21-R5 收尾）；前置卡 t_434af550 提交 37045418
- 口径依据：docs/research/legacy20_rev6_assessment.md（§2 子串修正 / §4.1 A 组 / §5 样例 / §7 风险）+ 前置件 payload（docs/scratch/legacy20_r6b/）+ albo 通报的 R6C 统一口径（归档件 figure_names 机制键清档 + 垃圾键删除 + 登记删除记录）。
- 结论：三项逐一落实并入库提交；门禁四连 exit 0；站点链条五步 exit 0（计数锚点 3252 -> 3261）；独立核验 94 PASS / 0 FAIL / 1 INFO；parity 与镜像推送回执见 §8 / §9。

## 1. 王震 H-WZ-001 并轨（主库动作唯一写入者）

### 1.1 动作

1. 10 条迁入：M-WZ-001~010 逐条 json 等于前置件 payload（docs/scratch/legacy20_r6b/H-WZ-001/modes_library_entries.json），编号循前置卡统一重编号，legacy_mode_id 留证。
2. 旧码 2 条处置：M392 字段整体重编号为 M-WZ-011（兵团模式法；related_modes 重指至 M-WZ-001；legacy_mode_id 保留 M392）；M391 与 M371 同题重复 -> 归档去重（不并入），快照与差异表入隔离位：
   - data/figures/_duplicates/H-WZ-001_M391_archive_snapshot.json
   - data/figures/_duplicates/H-WZ-001_M391_relation_analysis.json
3. 释放码引用面重指：M-EUC-006（欧几里得）related_modes M391/M392 重指至 M-WZ-001/M-WZ-011；data/figures/H-EUC-001.json 内嵌同体条目同步重指（缘由见 §5 门禁首轮回执）。

### 1.2 落盘与哈希（前 -> 后）

| 文件 | 计数变化 | sha256 前 -> 后 |
| --- | --- | --- |
| data/modes_data.json | 数组 3262 -> 3271；去重口径 3252 -> 3261 | 4ca4eda2... -> bdf672a2... |
| data/figures/H-WZ-001.json | modes 10 -> 11；thinking_mode_count 10 -> 11；字节 8183 -> 15674 | f0e78a96... -> cb1a7483... |
| data/individuals/H-WZ-001.json | modes 2 -> 11；计数 2 -> 11 | 9bf4d63a... -> 37e48795... |
| data/individuals/H-WZ-001_modes.json | modes 2 -> 11；计数 2 -> 11；字节 5527 -> 13882 | 1f924bdb... -> 5589b7a7... |
| data/code_maps.json（H-WZ-001.mode_ids） | 2 -> 11（figures 计数 215 不变） | 82fc77d5... -> df62a33f... |
| data/scenario_tags.json（H-WZ-001 平铺引用） | 2 条重指为 M-WZ-001 / M-WZ-011（总数 7478 不变） | d467bd6d... -> 40bdb194... |
| data/figures/H-EUC-001.json（M-EUC-006 内嵌） | 2 处引用重指 | a6eb2a42... -> dc2ae134... |

- 日志：evidence/wz_merge_log.json（含 counts 与前后 sha）、evidence/euc_repoint_log.json。
- 备份：backup/merge_r6b_20260923/（卡工作区）+ data/backup_r6_H-WZ-001_20260923/（仓内，循 R6 先例）。

## 2. 王祥 H-HZX-002 归档（活跃层清档 + 待重做清单）

### 2.1 三件入隔离位（sha256 与前置件登记逐一相同）

| 源（活跃层） | 归档位（data/figures/_duplicates/） | sha256（前 16） |
| --- | --- | --- |
| data/figures/H-HZX-002.json | H-HZX-002_figures.json | 8c40067cb04565a6 |
| data/figures/H-HZX-002_modes.json | H-HZX-002_figures_modes.json | 1e3e97d41f4135cb |
| docs/figures/phase20_wangxiang_research.md | H-HZX-002_research_phase20.md | 8b63cda2991a5b96 |

### 2.2 登记面与清单

- figure_names 清档 5 键（机制键 H-HZX-002 / H-HZX-002_modes / H-HZX-002_MODES + 垃圾键 H / 东岳），撤下原文逐字留档 docs/scratch/legacy20_r6b/removed_registrations_r6b.json（键级可回填）。
- 待重做清单：docs/research/phase21r6B_wangxiang_redo_list.md（10 条模式 + 6 项全局动作 + 12 条落源锚点；机器可读 docs/scratch/legacy20_r6b/H-HZX-002/redo_checklist.json）。
- 活跃层复扫：code_maps / scenarios_zh / scenarios_en / scenario_tags 对 H-HZX-002 与 M301~M310 零引用（独立核验 B15）。

### 2.3 口径偏差登记（如实）

- 前置件建议「机制键保留（待重做卡使用）、垃圾键删除」；本卡按 albo 通报的 R6C 统一口径（归档件机制键清档 + 垃圾键删除 + 登记删除记录）全量清档，并逐字留档以便键级回填；如船长另有裁定以裁定为准。
- 码位提示更正：评估稿所称「H-WX-001 未占用」系误判（该码已被王选占用）-> 重做不以换码为前提；建议 M-WX-001~010 或船长另定（redo_checklist.global_actions 已载）。

## 3. 董宇明 H-DYM-001 归档登记执行

### 3.1 三件入隔离位（sha256 与 R2 post 快照逐一相同）

| 源（活跃层） | 归档位（data/figures/_duplicates/） | sha256（前 16） |
| --- | --- | --- |
| data/figures/H-DYM-001.json | H-DYM-001_figures.json | 3b2e71fb984f... |
| data/individuals/H-DYM-001_modes.json | H-DYM-001_individuals_modes.json | c9ac05dc13c3... |
| docs/figures/H-DYM-001.md | H-DYM-001_archive_page.md | 1f47d4c1463b... |

### 3.2 登记面与复核

- figure_names 清档 1 键（H-DYM-001 = 董宇明），撤下原文与王祥同档留档（removed_registrations_r6b.json）。
- 活跃层零引用复扫：data/code_maps.json / data/scenario_tags.json / data/scenarios_zh.json / data/scenarios_en.json / data/modes_data.json 均无 H-DYM-001（独立核验 C1~C8）；主库 0 条。
- 口径偏差登记：前置件建议「figure_names 保留键（待收官统一口径）」-> 本卡按 R6C 统一口径清档 + 留档（同 §2.3）。

## 4. 台账刷新（data/audit/phase21r6_id_mapping_ledger.json / .tsv）

- B 组 32 行状态刷新（王震 12 / 王祥 10 / 董宇明 10），disposition 与 notes 补执行事实与口径依据。
- A/C 组 178 行逐字段与基线前像（98f34377）一致（独立核验 D4）。
- dedupe.in_modes_data / in_code_maps：100 -> 111（B 组 11 个新号入主库与码图；独立核验 D6/D7 可复算；保持 R6C 核验脚本 C7 复算为真）。
- tsv 由 json 逐字节复算一致（独立核验 D8）；日志 evidence/ledger_refresh_log.json；json 字节 103412 -> 107602，tsv 51935 -> 55583。

## 5. 门禁四连（回执）

- tools/credibility_gate.py --hard-fail --data-path data/modes_data.json：首轮 exit 1（新增硬失败 2 条：M-EUC-006 的 related_modes 指向已释放 M391/M392）-> 依 §1.1 第 3 条重指后复跑 exit 0（新增 0；存量 524 冻结）。证据 evidence/gate_credibility.txt。
- tools/verify_findings.py --hard-fail --data-path data/modes_data.json：exit 0（先 tools/build_audit_findings.py --write 刷新 audit_meta.modes_file_sha256；写盘回执 total: 164）。证据 evidence/gate_findings.txt。
- tools/verify_source_links.py --hard-fail：exit 0（新增坏链 0）。证据 evidence/gate_source_links.txt。
- tools/apply_verification_status.py --check：exit 0（库中状态与规则逐条一致；公开 3211 + 隔离 60 = 全库 3271 自洽）。证据 evidence/verify_status_check.txt。

## 6. 站点链条五步（计数锚点 3252 -> 3261）

1. tools/export_static_site.py：modes_deduped 3261 / 发布摘要 3201 / figures 1057 / by-figure 316 / 隔离名单 60 零泄漏 / 体积上限通过。
2. tools/gen_web_site_counts.py：web/src/generated/siteCounts.ts 更新为 3201 条 x 316 位；四态 931 / 1896 / 34 / 340。
3. tools/apply_site_counts.py：manifest（public 与 dist）与文档门面零违规。
4. tools/build_daily_index.py：3201 条 / 316 位 / 316 分片。
5. tools/pages_preflight.py --stage data：全部断言通过。
- 锚点更新：tools/export_static_site.py 与 tools/pages_preflight.py 的 EXPECT_MODES 3252 -> 3261（注释同风格记录；EXPECT_BY_FIGURE 316 / EXPECT_FIGURES 1057 不变）。
- 回归登记：findings.json 于门禁第 2 步刷新（+12/-12 行），static_data_manifest.json 随站点重建更新（sources.modes_data.json sha 与库存一致）。

## 7. 独立核验（verify_r6b_exec_indep.py，仓根第二实现）

- 口径：现盘 + 前置件 payload + 基线 commit 98f34377 前像（git show 读 commit object）；不联网、不复用本卡脚本。
- 覆盖：A 王震 22 项 / B 王祥与隔离位 19 项 / C 董宇明 8 项 / D 台账 8 项 / E 门禁回执 5 项 / F 站点链条 5 项。
- 结果：94 PASS / 0 FAIL / 1 INFO（exit 0）；INFO = 基线冻结悬空引用存量 452 条（历史，非本批新增；本批新增悬空 0 由 A20 断言）。
- 输出：evidence/verify_r6b_exec_indep.out.txt。

## 8. parity（两仓一致性机检）

- 镜像前：tools/check_repo_parity.py --json -> status DIFF；boundary 内 workspace 1790 / publish 1762；diffs 97 = CONTENT_DIFF 13（本批构建图路径）+ MISSING_IN_PUBLISH 56（含 R6C/R2 隔离位、R6C 报告层与前置卡遗留，合并卡统一收敛）+ MISSING_IN_WORKSPACE 28（R6C/R2/R6B 已清档原件，须发布仓删除）。
- 证据：evidence/parity_pre_json.json。
- 镜像后回执见 §9 与 evidence/parity_post_json.json。

## 9. 镜像与推送回执

- 发布仓镜像：本轮由合并卡统一收敛（曾子先例）——复制工作仓构建图路径（含 R6C/R2 遗留隔离位与本批 13 路径）/ 发布仓删除 28 条已清档原件 / 跳过他卡未跟踪在制文件（docs/qa/phase21r6_qa_* 等）。
- 推送回执：待本轮执行后补齐（见本文件 v2 补丁与 evidence/mirror_log_r6b*.json）。

## 10. 复现步骤

```
cd /opt/data/workspace/Protreptic
WS=/opt/data/kanban/boards/protreptic/workspaces/t_f3aabe2c
python3 $WS/scripts/01_baseline.py        # 基线快照（只读，含 17 件 sha256 与前像 commit）
python3 $WS/scripts/02_merge_wz.py        # 王震并轨（写前 sha 校验，FAIL 即中止；幂等可复跑）
python3 $WS/scripts/03_archive_b.py       # 王祥/董宇明归档 + figure_names 清档 + 留档
python3 $WS/scripts/04_redo_list.py       # 待重做清单导出
python3 $WS/scripts/06_fix_euc_refs.py    # M-EUC-006 引用重指
python3 $WS/scripts/05_ledger.py          # 台账 B 行刷新 + dedupe 复算
python3 $WS/scripts/07_anchor_update.py   # 站点锚点 3252 -> 3261
python3 tools/credibility_gate.py --hard-fail --data-path data/modes_data.json
python3 tools/verify_findings.py --hard-fail --data-path data/modes_data.json
python3 tools/verify_source_links.py --hard-fail
python3 tools/apply_verification_status.py --check
python3 verify_r6b_exec_indep.py          # 独立核验（94 PASS / 0 FAIL / 1 INFO）
```

- 回滚：数据文件从 backup/merge_r6b_20260923/ 与 data/backup_r6_H-WZ-001_20260923/ 拷回；归档件由 data/figures/_duplicates/ 回拷至原位；figure_names 键值按 removed_registrations_r6b.json 键级回填。

## 11. 遗留与登记（不夹带他卡产物）

- site_docs 本地镜像目录（两仓均 0 跟踪文件、不在构建图）仍有 phase20_wangxiang_research 页与搜索索引提及 -> 循 R6C 口径登记为后续站点重建项，本卡不动作。
- 历史报告层引用保留：docs/qa/phase36_acceptance.md、docs/qa/phase37_x4_repo_parity.md、docs/research 前置件与 docs/scratch/legacy20_r6b payload 原件 —— 按前置件 post_archive_checks 口径。
- M391 富字段吸收（并入 M371 的精修）为后续候选，本批未扩写（诚实纪律：不新增事实性内容）。
- 未跟踪在制（他卡，本卡提交不夹带）：docs/qa/phase21r6_qa_*（QA 卡）、web/dist（构建产物）、scratch/、data/backup_merge_H-ZDY-001_2026*（他卡备份）。
- 镜像快照之后他卡新提交由各卡自身镜像步骤消解（post parity 登记）。

## 12. 证据索引

| 路径 | 内容 |
| --- | --- |
| docs/qa/phase21r6B_execution_report.md | 本报告 |
| docs/qa/phase21r6B_execution_evidence.json | 机器可读证据（计数/哈希/回执） |
| verify_r6b_exec_indep.py | 独立核验脚本（第二实现） |
| data/audit/phase21r6_id_mapping_ledger.json / .tsv | 台账（B 行刷新） |
| docs/scratch/legacy20_r6b/removed_registrations_r6b.json | figure_names 撤下原文留档（6 键） |
| docs/research/phase21r6B_wangxiang_redo_list.md | 王祥待重做清单（单列） |
| 卡工作区 evidence/ | baseline / wz_merge_log / archive_log_r6b / ledger_refresh_log / euc_repoint_log / 门禁与链条回执 txt / parity_pre_json / mirror_log_r6b |
| 卡工作区 scripts/ | 01~07 执行脚本（可复跑） |
