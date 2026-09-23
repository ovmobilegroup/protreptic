# Phase21-R5 记录性残留微清理 报告（卡 t_36c4079c）

- 卡号: t_36c4079c（elcano，工作仓 /opt/data/workspace/Protreptic）
- 日期: 2026-09-23
- 来源: docs/qa/phase21r3_greyzone_report.md §9 第 2/3/4/5 项 + docs/research/phase20R_zengzi_merge_report.md 残留 #16
- 纪律: 先取证后动手；归档而非删除；主库写操作本卡排他（观测期内主库零并发写，R6 批次卡仅在各卡自身的 figures/individuals 路径在制）
- 工作仓提交: 45c5f43a（数据+脚本）；发布仓镜像提交见 §6

## 0. 摘要

四项全部闭环、逐项留命令证据、可独立复算：

| # | 项 | 处置 | 前后哈希 |
|---|---|---|---|
| 1 | 班固恢复件 _en 中文残留 3 处 | 主库逐字归一（documents x2 / argumentation），现役面零残留 | 0c627b73 -> 2aef1275 |
| 2 | H-DZS 档案层旧号 | 双件 id/code 归一 M-DZS-001~010 + 映射表/留痕；档案页叙述同步 | f1f9e845 -> 717efd3b（双件同体）|
| 3 | 曾子批次 8 条过时断言 | 四态口径改版（A17/A17b/E1/E2/E3/E4/0.4/G2 + G1/R5 + H1 复跑） | 见 §3 |
| 4 | total 字段 + 根目录旧档 | total 2948 -> 3162 随计数对齐；根档归档 data/backup_root_legacy_modes_data_20260923/ 并 git rm | 610302B / 34b734d2 |

收尾：门禁三连 exit 0；verification --check 零漂移；站点链条五步 exit 0；两仓 parity 见 §7；发布仓镜像+push 见 §6。
独立核验脚本 verify_phase21r5_micro_cleanup.py 全绿（结果见 §10）。

## 1. ① 班固恢复件 _en 中文残留 3 处（主库逐字归一）

**现状（取证）**：3 处残留位于主库 data/modes_data.json 的 M-BG-003.process_en[0]、M-BG-010.process_en[0]、M-BG-010.modern_applications_en[1]，逐字继承自 f66bb2fd 快照；R4 报告 §9.4 定性为「源档逐字继承」的历史性混排。

**消费方核验**：
- docs/figures/H-BG-001.md 为中文档案页，无对应 EN 段，无需镜像改写；
- data/figures/H-BG-001.json / data/individuals/H-BG-001.json / data/individuals/H-BG-001_modes.json — BC 族档案为 legacy 体例（无 process_en/modern_applications_en 字段，扫描零命中），无镜像面；
- web/public/data/modes/by-figure/H-BG-001.json 为 gitignored 现场产物（export_static_site 生成），本轮站点链条重建后新串在位、旧串零（见 §5）。

**处置（逐字改写，最小对位）**：
| 字段 | 旧（残句） | 新 |
|---|---|---|
| M-BG-003.process_en[0] | ...accounts and Wenxian for same events | ...accounts and documents for same events |
| M-BG-010.process_en[0] | ...genealogical Wenxian and historical records | ...genealogical documents and historical records |
| M-BG-010.modern_applications_en[1] | Brand origin Lunzheng | Brand origin argumentation |

（表中旧串以拼音代记，原字见证据 json；术语沿用库内既有先例 documents / argumentation；docs/terminology/phase3_terminology.md 无此三项条目，不入表。）

**哈希**：data/modes_data.json 0c627b73... -> 2aef1275...（本项与 §4a 合计 4 行 diff，已核对无其它行；文件字节数 24297363 -> 24297379）。
**全库残留面**：旧串仅存两个历史备份（backups_merge_H-DZ-001_20260909_005314 / backups_merge_H-SJM-001_20260909_071433，均属历史留档）；现役面（data/ docs/ web/ src 侧）零命中。

## 2. ② H-DZS 档案层旧号归一（对齐主库口径）

**现状（取证）**：data/figures/H-DZS-001_modes.json 与 data/individuals/H-DZS-001_modes.json（当时 byte-exact 同体，f1f9e845）内 10 条模式 id = M01~M10、code = H-DZS-M01~H-DZS-M10；docs/figures/H-DZS-001.md 两处叙述「思维模式 M01-M10 全部映射」。主库与主库引用面（code_maps/scenarios）已由 R4（t_ea3a32e5 G5）归一为 M-DZS-001~010，本卡补档案层，保层间一致。

**处置**：
- 双件 id/code 全量归一 M-DZS-001~M-DZS-010（20 行/件）；
- 双件追加 mode_id_mapping（10 项旧号映射 M01~M10 -> M-DZS-001~010）与 mode_ids_note（定稿/作废/卡号留痕，作废旧号仅存该注记语境）；
- docs/figures/H-DZS-001.md 两处「思维模式 M01-M10 全部映射」-> 「思维模式 M-DZS-001~010 全部映射」；
- 主库 10 条 M-DZS-* 的 research_mode_id 保留 M01~M10 溯源位（未动）。

**层间一致性抽验**：主库 research_mode_id 序列 = M01..M10 与双件映射表逐项对应；档案层 id/code 与 code_maps/scenarios 引用的 M-DZS-* 完全对齐。
**哈希**：双件 f1f9e845... -> 717efd3b...（仍双件同体）；docs 页 236afc1b... -> b942fefb...；diff 仅 20 行 id/code + 尾部映射块 + 档案页 2 行。
**旧号残余（设计使然/范围外）**：注记内作废语境；main_data.json、tools/json/* 旧副本、根目录遗留备份等历史面不在本卡范围（见 §8）。

## 3. ③ 曾子批次 8 条过时断言四态改版

**点位说明**：卡面列「脚本: verify_hzx_phase20R.py / verify_hzx_merge_phase20R.py / verify_hzx_landing.py」，实测 8 条点位（R4 报告 §5: A17/A17b、E1/E3/E4、0.4、G2、H1）分布于 **verify_hzx_merge_phase20R.py** 与 **verify_zengzi_qa_espinosa.py** 两个脚本；phase20R / landing 为 H1 聚合对象（其中 phase20R 的引用面白名单随 R5 产物同步更新，landing 无改动点）。四处均已处置。

**逐条改版（口径 = 四态 verified/pending/suspect/unverifiable + 留证；原落地裁定枚举 SANC 废止，原文留证于 manifest#verification_restamp.old_statuses）**：

| 点位 | 脚本 | 改版前 | 改版后 |
|---|---|---|---|
| A17 | merge | status in SANC 四值（quote-verified 等） | status in FOUR 且 manifest#verification_restamp.old_statuses 覆盖 10 条 |
| A17b | merge | 非 quote-verified 带 correction_zh（0 条成立） | 判据改为留证旧态（source-verified-corrected / corrected-*）-> 3 条 M-ZX-007/009/010 带 correction_zh |
| E1 | merge | 库模式数 == 3152 | == 3162（台账随批次更新；+10 班固 R4-G4） |
| E2 | merge | total == 2948（冻结说明） | total == len(modes)（R5 裁定现口径，见 §4a） |
| E3 | merge | 备份比对 3142 -> 3152 | 3142 -> 3162（+10 曾子 +10 班固） |
| E4 | merge | 前缀逐字全等（R4 改名后失真） | 授权面台账：verification 归位 2909 / 班昭·杜威显示名 20 / 董仲舒改名 10 / 引用面随迁 9；越界面报点 |
| 0.4 | qa_espinosa | 模式面零差异（R4 四态归位后失真） | 模式面差异仅限 verification 且属四态、留证在位；其余四面零差异保留 |
| G2 | qa_espinosa | 镜像 sha 前缀 == ba2ad769（旧落地态） | 与 restamp.new_mirror_sha256 同体同步 + old_mirror_sha256 留档核验 |
| H1 | qa_espinosa | 66/31/26 全绿（上游改版后依赖同批改版） | 不变更，随上述改版复跑全绿（无误判） |

**引面白名单同步（R5 落位）**：merge 与 phase20R 的 M-ZX-001 引用面白名单并入 R4/R5 产物（phase21r3_greyzone_report 为 R4 产物、R5 三产物），并把 web 构建产物（web/public、web/dist，均 gitignored/现场生成）排除出源码引用面扫描。

**结果（2026-09-23 复跑）**：verify_hzx_merge_phase20R 66 PASS / 0 FAIL；verify_hzx_phase20R 31 PASS / 0 FAIL；verify_hzx_landing 26 PASS / 0 FAIL；verify_zengzi_qa_espinosa 81 PASS / 0 FAIL / 7 INFO（观察 3/4/5 已更新为闭环记录，观察 1/2 保留）。

**脚本哈希**：merge 4f7ed16e -> 7b8b5340；phase20R 5229a9d4 -> 8b8f17d6；qa_espinosa a92c196d -> 108f1411 -> fdb73ef7（观察行收尾）。

## 4. ④ total 字段与根目录旧档

### 4a. 主库 total 字段（2948 -> 3162）

**消费方核验（先取证）**：grep tools/ web/src/ api/ 及全部提交面脚本，total 字段零现役消费方（tools/build_audit_findings.py 与 api/load_v6.py 等仅按 modes 数组计数；站点计数走独立来源）。
**裁定**：按仓库先例（docs/research/phase20_zhoudunyi_merge_report.md 记「total 与 len(modes) 一致」）随计数对齐 -> 3162 = len(modes)。历史 2948 漂移（差 214）终结，行内注释与 E2 断言同步。
**哈希**：见 §1（同文件，4 行 diff 中的 total 行）。

### 4b. 根目录旧档 modes_data.json（610302B，tracked）

**取证**：101 图块汇编（list 体例，含 H-DZS-001 与 H-ZX-001 旧号块）；最后改写于 2371a585（phase46 mining）；HEAD blob 44b9675dc8ee...；引用它的仅历史一次性脚本（merge_script.py / merge_workspace_json.py / fix_gulf_*.py / fix_qa_batch4.py，最后改动 2026-08-15，不在任何管线；现役工具链一律读 data/modes_data.json）。
**处置**：byte-exact 归档至 data/backup_root_legacy_modes_data_20260923/（modes_data.json + README.md 含指纹/恢复法/注意），git rm 根副本（git 识别 R100 rename）；无消费方，按卡面口径「归档而非删除」落地。
**核验**：归档副本 sha256 == 34b734d2ce998684e2a8b89f97997ee28839aadb623c914a27b2a4e6584453fb（与移除前一致）；恢复法：cp 归档副本回根，或 git show 44b9675d > modes_data.json（引用面脚本如需复跑）。

## 5. 门禁与站点链条（收尾复跑）

| 项目 | 命令 | 结果 |
|---|---|---|
| 可信度门禁 | tools/credibility_gate.py --hard-fail --data-path data/modes_data.json | exit 0（无硬失败） |
| findings 门禁 | tools/verify_findings.py --hard-fail --data-path data/modes_data.json | exit 0（存量警告 2 条：M-ASM-001~010 双重收割 + audit_meta.modes_file_sha256 待刷；无新增硬失败） |
| 出处链接门禁 | tools/verify_source_links.py --hard-fail | exit 0（无新增坏链、存量冻结判据 0/0；UNREACHABLE 软告警随网络波动，复跑 1~20 条） |
| verification 零漂移 | tools/apply_verification_status.py --check | exit 0（四态求和 == 模式条数；公开 3102 加隔离 60 等于全库 3162；库中状态逐条一致） |
| 站点链条五步 | export_static_site -> gen_web_site_counts -> apply_site_counts -> build_daily_index -> pages_preflight --stage data | 五步全 exit 0；preflight：figures=1057 / modes=3152 / published=3092 / 隔离命中=0 / by-figure 306；daily 3092 条「全部断言通过」 |

站点随动核对：docs/architecture/static_data_manifest.json 的 sources.data/modes_data.json.sha256 = 2aef1275b05fe15b4bfa...（与现库一致）；web/src/generated/siteCounts.ts 四态 932/1786/34/340、3092 条 × 306 人（R4 计数基线不变，本批不动计数）；by-figure 分片产物已随源重导（H-BG-001 分片 +16B，计数不变）。

## 6. 发布仓镜像与推送（公开侧）

- 数据面镜像提交（发布仓 main）：`65eb1c8` —— 7 路径：
  `data/backup_root_legacy_modes_data_20260923/{modes_data.json,README.md}`（新增）、`data/figures/H-DZS-001_modes.json`、`data/individuals/H-DZS-001_modes.json`、`data/modes_data.json`、`docs/figures/H-DZS-001.md`、`docs/architecture/static_data_manifest.json`。
- 推送回执：`a4906e7..65eb1c8  main -> main`；fetch 后实测 `origin/main == 65eb1c8`、`git rev-list --count origin/main..HEAD = 0`。
- 内容核对（发布仓 == 工作仓 HEAD，逐字节 sha256）：`data/modes_data.json` 2aef1275b05fe15b...；H-DZS 双件 717efd3bd4b15b80...（同体）；`docs/figures/H-DZS-001.md` b942fefb0c3195af...；`docs/architecture/static_data_manifest.json` 824d2573c116658e...；归档 README f00a6a9e31998153...。
- 报告与证据面镜像提交：收尾第二段推送（`docs/qa/phase21r5_micro_cleanup_report.md` + `docs/research/phase21r5_micro_cleanup_evidence.json`）；提交号与推送回执记录于本卡完成交接（kanban metadata / 评论）。
- 公开侧变化清单（上线可见）：(1) M-BG-003/M-BG-010 英文内容三处归一（上线文案字段）；(2) H-DZS 档案页模式号显示 M01-M10 -> M-DZS-001~010；(3) 站点 static_data_manifest 源 sha 随动（2aef1275...）；(4) 归档件 `data/backup_root_legacy_modes_data_20260923/`（含 README 指纹与恢复法）入发布仓。

## 7. 两仓 parity（收尾实测）

- 工具：`tools/check_repo_parity.py`（边界自检通过：pages.yml 构建步骤 16 / 触发器 30 全覆盖；纳入边界 ws 1763 / pub 1594）。
- 实测（报告/证据镜像 P2 前时点）：**211 处差异** = MISSING_IN_PUBLISH 170 / CONTENT_DIFF 40 / MISSING_IN_WORKSPACE 1。
- 归属：**210 处为 R6 在制卡**（t_10089b19 主库 +100 合并与站点在制、t_434af550 B 组产物、t_4a9cf2cb C 组在制、批1/批2 产物与 docs/scratch 归档）——非本卡路径；**1 处为本卡报告**（未跟踪，随 P2 镜像收敛）。
- 本卡数据面（P1 已镜像 7 路径）**逐字节零差异**（sha 表见 §6）；P2 后本卡全部路径收敛（终态实测记录于完成交接）。

## 8. 残留清单（范围外 / 供编排）

1. 根目录 tracked 遗留（本卡范围外）：`modes_data.json.backup_homer_20260922_070524`、`main_data.json`（含 H-DZS-M 旧号）、`tools/json/*` 旧副本。
2. 发布仓根目录遗留副本（2026-09-17 期）：`modes_data.json` 492499B、`code_maps.json`、`scenario_tags.json`、`scenarios_zh/en.json` —— 构建读 `data/**` 与 `tools/**`，根副本不进构建图，parity 边界不含根文件，本卡范围外。
3. 台账类断言随批次更新点：`verify_hzx_merge_phase20R.py` E1（3162）/E2 与本卡核验 4a 的 3162 锚点，在 R6 合并（+100）入库后需随批次刷新（R6 卡既有流程；不改口径以避免伪造台账）。
4. R6 在制（t_10089b19 主库 +100、t_434af550 后续、t_4a9cf2cb C 组）的 parity 差异与站点锚点 bump（EXPECT_MODES 3252 / siteCounts 3192 人 316）由各卡自行收敛。
5. `verify_zengzi_qa_espinosa.py` 内嵌 live BASE（/opt/data/workspace/Protreptic）：并发在制期的快照复算需用 BASE 重定向副本（本卡做法见 §10），供编排知悉该脚本属性。
## 9. 复现顺序（可复跑）

```
cd /opt/data/workspace/Protreptic
python3 verify_phase21r5_micro_cleanup.py            # 本卡独立核验（快照复算 27/0/5；环境说明见 §10）
python3 tools/apply_verification_status.py --check   # verification 零漂移
python3 tools/credibility_gate.py --hard-fail --data-path data/modes_data.json
python3 tools/verify_findings.py --hard-fail --data-path data/modes_data.json
python3 tools/verify_source_links.py --hard-fail
python3 tools/check_repo_parity.py                   # 两仓 parity
# 快照复算环境（并发在制期推荐）：git worktree add --detach <snap> 45c5f43a && cd <snap>
#   espinosa 内嵌 live BASE：把其 BASE 常量一行替换为快照路径后运行（本卡实做，仅 1 行路径、逻辑零改动）
#   python3 verify_phase21r5_micro_cleanup.py
# 发布仓核对：cd /opt/data/release/Protreptic-publish && git log --oneline -3 && git rev-list --count origin/main..HEAD
```

## 10. 独立核验结果（verify_phase21r5_micro_cleanup.py）

- 脚本 sha256：b57b5a322108a643...（全量见证据 json verification.script_sha256）；断言面：1a~1c / 2a~2g / 3a~3g / 4a~4g 共 27 条。
- **快照复算（推荐口径）**：worktree = 45c5f43a 数据面 + R6 批1/批2/B 组前置提交（HEAD 37045418），espinosa BASE 重定向副本 —— **27 PASS / 0 FAIL / 5 INFO（exit 0）**；其中 H1 四脚本重放：merge 66/0、phase20R 31/0、landing 26/0、qa_espinosa 81/0/7。
- live 树复核（收尾时点）：R6 卡在制主库合并（+100，3262）使 espinosa 内部重放按在制数据撞 3162 台账断言 —— live 结果 80 PASS / 1 FAIL / 7 INFO，属预期漂移、非本卡四项缺陷；本卡四项在 live 与快照两面单点复算均一致（字段/SHA 逐项命中）。
- 并发观测：本卡提交 45c5f43a 先于 R6 批次归档；复核时点主库在制写为 t_10089b19（+100 合并）—— 本卡零写入窗口已结束，与主库写操作本卡排他口径不冲突。
- 证据包：`docs/research/phase21r5_micro_cleanup_evidence.json`（逐项：现状、消费方证据、处置、前后 sha256 指纹）。
