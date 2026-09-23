# Phase21-R7 旁项：根目录 / 发布仓旧档残留调查与处置报告

- 卡号：t_151265db（elcano，工作仓 /opt/data/workspace/Protreptic）
- 日期：2026-09-23（操作窗口约 19:45–20:05 CST）
- 授权 / 来源：卡面（magallanes）「R5 卡留档未闭环旁项」；出处 = R5 报告（t_36c4079c）§8；先例 = R5 对根 modes_data.json 的 byte-exact 归档处置（data/backup_root_legacy_modes_data_20260923/）
- 纪律：先取证后动手；归档而非删除；主库 data/modes_data.json 零写入；发布仓同步仅限本卡涉及路径。

## 1. 调查（读序 / 引用 / 指纹 三线取证）

### 1.1 构建与脚本真实读取顺序（「活输入」圈定）

- `tools/build_figures_db.py` find() 实读（源行 53–55）：
  - `zh_path = find("tools/json/scenarios_zh.json", "tools/scenarios_zh.json")`
  - `en_path = find("tools/json/scenarios_en.json", "tools/scenarios_en.json")`
  - `tags_path = find("tools/scenario_tags.json", "tools/json/scenario_tags.json")`
- `tools/check_repo_parity.py` 现役集（源行 17–18、119–122）：`data/**`、`tools/json/scenarios_zh.json`、`tools/json/scenarios_en.json`、`tools/json/scenario_tags.json`、`tools/scenario_tags.json`、`tools/assets/fonts/**`；同文件 159 行明确将「根目录遗留副本（modes_data.json、scenarios_zh/en.json、code_maps.json、scenario_tags.json…）」列为边界外（不进构建图）。
- 结论——**活输入（原地保留，未处置）**：
  1. `tools/json/scenarios_zh.json`（sha256 c240aa300812af6d…）
  2. `tools/json/scenarios_en.json`（sha256 018aadd45918d72d…）
  3. `tools/json/scenario_tags.json`（sha256 c2617d455f2384a8…）
- 其余同名副本（根目录与 tools/json 中的 modes_data / main_data / code_maps 旧体）**均不在任何读取序列内**。

### 1.2 git tracked 与全仓引用（grep 普查）

- 13 件受处置项均 tracked（blob 见 §2 表）。
- 全仓 grep（对 modes_data.json.backup_homer / main_data.json / tools/json 旧体 / 根副本名逐一排查；排除 data、docs 归档域后）：**现行代码零 exec 引用**；命中仅出现在审计/报告类文档（如 phase20R_zengzi_residual_scan.json、R5 报告与证据）——均为「残留登记」记录性引用，非读者。
- 发布仓侧：`scripts/validate_bg.py` 等读 `data/**`（非根）；未发现任何根副本读者。`Dockerfile.api` 仅 COPY api/ 与 tools/。

### 1.3 内容指纹与现役 / 同名件字节对比（sha256）

- 关键同体对（逐字节相等，sha256 全等）：
  - 工作仓根 `modes_data.json.backup_homer_20260922_070524` ≡ 发布仓根 `modes_data.json`（675a7dc3…，492,499B）
  - 发布仓根 `code_maps.json` ≡ 工作仓根 `code_maps.json.backup_homer_20260922_070407`（fcb02802…，52,537B）
  - 发布仓根 `scenario_tags.json` ≡ 工作仓根 `scenario_tags.json`（b0e9032d…，31,079B）
  - 发布仓根 `scenarios_en.json` ≡ 工作仓根 `scenarios_en.json`（686dfaf1…，88,367B）
  - 发布仓根 `scenarios_zh.json` ≡ 工作仓根 `scenarios_zh.json`（9b3143b4…，87,475B）
- 判死三要件（组合）：① 不在构建/脚本读序（§1.1）；② 全仓零 exec 引用（§1.2）；③ 指纹与世系证其被现役数据代际取代（工具旧体 / 2026-09-17 期根副本 / H-DZS-M 旧号世系）。

## 2. 逐件判定与处置（13 件 = 全死；本轮无新增存疑）

### A. 工作仓根目录（3 件）

| 路径 | 尺寸(B) | sha256 | git blob | 归档去向 |
|---|---|---|---|---|
| modes_data.json.backup_homer_20260922_070524 | 492499 | 675a7dc3b2cf773635f2d45da6dba715d9aa0214618507d6bc837c63201c9ced | 3793899ba1e1 | data/backup_root_homer_modes_data_20260923/modes_data.json.backup_homer_20260922_070524 |
| main_data.json | 5181212 | f4d0285eac4c72df3a80ec4b43efcf8e7b024c05e2c41e2f95dd4737cb391a39 | 758d6845acc9 | data/backup_root_main_data_20260923/main_data.json |
| main_data.json.bak_hzx_merge_25696 | 0 | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 | e69de29bb2d1 | data/backup_root_main_data_20260923/main_data.json.bak_hzx_merge_25696 |

### B. tools/json 旧副本与垃圾件（5 件）

| 路径 | 尺寸(B) | sha256 | git blob | 归档去向 |
|---|---|---|---|---|
| tools/json/modes_data.json | 44008 | 5145a11aa93f01dce03e25b97d5d53fffa977b0ef4847950c527034af7c8c97b | 036c24c579d7 | data/backup_root_tools_json_legacy_20260923/modes_data.json |
| tools/json/main_data.json | 12655 | 7d080c5080e05837d8f17319d54eb1d9cd1d41010ff05df602027934a4b2254e | 19cd2e0cbe7a | data/backup_root_tools_json_legacy_20260923/main_data.json |
| tools/json/code_maps.json | 200401 | bf1d624d7e65e9f24a6570ed9b358436145d492111b828ca923b46f2d444e2a8 | 877a6d67af9d | data/backup_root_tools_json_legacy_20260923/code_maps.json |
| tools/json/, print( | 62 | d563e31b5c5681a1fd63381053899e4ff55794764d5d12078bf5ff6d9e2c05d7 | adee05308f79 | data/backup_root_tools_json_legacy_20260923/junk/stray_, print(.txt |
| tools/json/.json | 1660 | a70f3ec1a2a864352c3a1031ff1feff4ead29c0363f2a9945565e522169787bd | 7c6a01096d69 | data/backup_root_tools_json_legacy_20260923/junk/stub_.json |

### C. 发布仓根同名旧档（5 件，2026-09-17 期）

> 说明：卡面点名件 = `modes_data.json`（492,499B）；实测该批为 5 件同代系副本（与 R5 §8.2 登记一致），受处置全量 5 件；其中 4 件的同体孪生 = 工作仓根同名件（未在卡面清单 → **未动**，见 §5）。

| 路径 | 尺寸(B) | sha256 | git blob | 归档去向 |
|---|---|---|---|---|
| modes_data.json | 492499 | 675a7dc3b2cf773635f2d45da6dba715d9aa0214618507d6bc837c63201c9ced | 3793899ba1e1 | data/backup_root_homer_modes_data_20260923/（与工作仓件同体，单副本） |
| code_maps.json | 52537 | fcb02802470b41f9dd5040caa76f9d6d8178eb61909a209f04993e69bb488358 | 448685a0c722 | data/backup_root_publish_legacy_20260923/code_maps.json |
| scenario_tags.json | 31079 | b0e9032dfd1273d239178d209921702a9e2068e08d8d8689d5148408129b55c7 | 1dcce553f419 | data/backup_root_publish_legacy_20260923/scenario_tags.json |
| scenarios_en.json | 88367 | 686dfaf135497c1c26ea1a6bb8b5b76d890eea214734fd4d113f0689ba60a6ad | e80460dfdd91 | data/backup_root_publish_legacy_20260923/scenarios_en.json |
| scenarios_zh.json | 87475 | 9b3143b446f6dea4b1e8be52df099f64b776e8ec65d5b4f7638db7c3af9c58e7 | 7fb0721b82ae | data/backup_root_publish_legacy_20260923/scenarios_zh.json |

判定汇总：**死 13 / 存疑 0 / 活 0（本轮核查面无新增）**；活输入 3 件原地保留（§1.1）。全部处置均 byte-exact 归档 + README（指纹与 git 恢复法）。

## 3. 操作记录（归档 → 移除 → 提交 → 镜像 → 推送）

### 3.1 归档（byte-exact，指纹与 git 恢复法写入各 README）

| 归档目录 | 内容 | 归档件数 |
|---|---|---|
| `data/backup_root_homer_modes_data_20260923/` | modes_data.json.backup_homer_20260922_070524（+README，含发布仓同体件双来源说明） | 2 |
| `data/backup_root_main_data_20260923/` | main_data.json、main_data.json.bak_hzx_merge_25696（0B 空档）+README | 3 |
| `data/backup_root_tools_json_legacy_20260923/` | modes_data.json、main_data.json、code_maps.json + junk/（stray_, print(.txt、stub_.json）+README | 6 |
| `data/backup_root_publish_legacy_20260923/` | code_maps.json、scenario_tags.json、scenarios_en.json、scenarios_zh.json +README | 5 |

恢复法（示例，全量见各 README）：`git show <blob> > <原路径>`（工作仓/发布仓均可）；或直接从归档目录 cp 回原位。

### 3.2 提交与推送

- 工作仓提交 **2857a525**（2026-09-23 19:55:49）：17 条 = **8 例 R100（git 判定的字节等价重命名，零内容差）** + 9 项新增（4×README、发布仓 4 件副本、data/audit 证据）；pathspec 精确保交，未夹带并发卡文件。
- 发布仓镜像提交 **c72d007**（19:56:41）+ 推送回执：`dc8ca3b..c72d007  main -> main`；fetch 实测 `origin/main == c72d007`（`git rev-list --count origin/main..HEAD = 0`）。
- 跨仓一致性实测：5 路径（4 归档目录 + data/audit 证据）逐文件 `sha256sum | sort` diff —— **全部 IDENTICAL**。
- 推送口径（如实说明）：工作仓无 upstream/推送目标（`remote.origin` 仅 fetch，用于与发布侧线对比；远端唯一分支 `main` = 发布侧线）。依 R5/R6 先例：**推送 = 发布仓 → 远端 main；工作仓为本地提交**（提交号 2857a525 可独立复核）。双仓同步状态：发布仓=已推送；工作仓=已提交（本地，无推送目标，列明）。

## 4. 门禁（改动后复检）

| 门禁 | 结果 |
|---|---|
| `credibility_gate.py --hard-fail` | **exit 0**（无新增硬失败；存量 524 条冻结；D4/D5 警告 24 条非阻断） |
| `verify_findings.py --hard-fail` | **exit 0**（无新增；2 条既有警告：audit sha 过期、M-ASM 双采） |
| `apply_verification_status.py --check` | **exit 0**（四态自洽；公开 3211 + 隔离 60 = 3271 逐条一致） |
| `verify_source_links.py --hard-fail` | **exit 0**（无新增坏链；UNREACHABLE 清单为既有存量警告） |

- 构建输入面零变化：受处置 13 件无一在 build_figures_db find() 读序 / parity 现役集（§1.1）；站点链条五步未触发重跑（无输入变化），parity 构建图 1819 件逐字节一致作为替代强证。

## 5. 未处置清单（范围外 / 供编排）

1. **工作仓根同体孪生件（与发布仓处置件同体）**：`scenarios_zh.json`、`scenarios_en.json`、`scenario_tags.json`、`code_maps.json`、`code_maps.json.backup_homer_20260922_070407`、`code_maps_backup_nanming_20260909.json` 等 + `three_dimensional_comparison_matrix.xlsx`、`lighthouserc.json` 等根遗留——**卡面未点名 → 未动**；判据与本节一致（构建图外、零 exec 引用），建议合批另卡一次性裁定。
2. **tools/json 旧稿族**（同上目录，655+ 件）：figure 草稿 665、脚本 33、schema 文档 2、备份 1——本卡仅处置与现役同名的 3 件聚合旧副本 + 2 件垃圾件；旧稿族「非同名副本」且未逐一证死，**未动**；证据 `data/audit/phase21r7_leftovers_inventory.json` 已按件备好 class，可支撑后续「tools/json 旧稿清档」专项卡。
3. **在制物（勿动）**：`data/backup_merge_H-ZDY-001_*`（兄弟卡在制）、`docs/scratch/r7_probe_write_test.txt`（本卡写权限探针，收尾随卡清理）。


## 6. 证据与复核路径

- `data/audit/phase21r7_leftovers_inventory.json`（167,808B）：tools/json 全量 709 件逐件 class + sha256 + 判定；受处置 13 件全字段（size/sha256/blob/last_commit/archived_to）。
- `docs/research/phase21r7_leftovers_evidence.json`：本卡结构化证据（commits/gates/parity/archives/inputs_unchanged 等）。
- 归档 README ×4：每件指纹（size/sha256/blob/last_commit）+ git 恢复命令。
- 独立复核方法：① `sha256sum` 归档件与本节 §2 表逐件比对；② `git show <blob>` 从任一行历史复现原件；③ 删除有效性：两仓 `git ls-tree HEAD` 均不再含受处置原路径。

## 7. 两仓 parity（收尾实测）

- 工具：`tools/check_repo_parity.py`（边界自检通过后执行）。
- 本报告镜像前时点实测：**exit 1**；`[stats]` 两仓都有 **1819** 条、其中**逐字节一致 1819**；仅单侧 4 条（仅工作仓 4 · 仅发布仓 0）。
- 归属：**4 条全部为兄弟 R7 卡待镜像**（`docs/research/phase21r7_cgroup_identity_report.{md,json}`、`phase21r7_wangxiang_sourcing_report.{md,json}`，MISSING_IN_PUBLISH）——非本卡路径；**本卡路径零差异**（13 件移除两侧同步、4 归档目录 + audit 证据两侧同体）。
- 终态复检（本报告与证据镜像推送后）记录于完成交接（kanban metadata）与下方「收尾回执」。

## 8. 收尾回执（补记）

- 本报告/证据面镜像提交与推送回执、终态 parity 复检数值：见 kanban 完成交接（t_151265db metadata）与本卡评论；如后续补记，以本文件追加版本为准。

---
*生成：elcano / t_151265db；方法论：先取证后动手、归档而非删除、逐路径独立复核（sha 指纹链 + git blob 链）。*

## 9. 收尾回执（终态补记）

- 工作仓交付提交（报告 + 证据）：**ce9800d2**（v1 算例：报告 12,300B / sha256 c644fa0e…；证据 11,127B / sha256 52bceb97…；文件级 sha 以 git 链逐版复核为准）。
- 发布仓镜像提交：**2821874**；推送回执：`c72d007..2821874  main -> main`；fetch 实测 `origin/main == 2821874`（ahead=0）。
- 终态 parity 复检（工具实测，本补记前时点）：**exit 1**；两仓 **1821** 条逐字节一致 1821；仅单侧 4 条（仅工作仓 4）= 兄弟 R7 卡待镜像（§7 归属；非本卡路径，本卡全部路径两侧同体）。
- 处置汇总：**死 13 全处置**（byte-exact 归档 → 移除 → 双仓提交/推送）；存疑/活无新增；主库 data/modes_data.json 零写入；门禁四绿（§4）。
