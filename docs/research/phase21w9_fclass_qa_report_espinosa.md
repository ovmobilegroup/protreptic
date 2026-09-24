# Phase21 W9 F 类回填独立 QA 报告（espinosa / 卡 t_9ed2866a）

**结论：FAIL**（W9 执行卡自述「537 条回填成功、1027→1017 有名字」与落盘终态不符：实际回填 **0/504**、DB 空名 **514**；另有 10 条处置未落地、完成合同缺件（报告缺、发布镜像缺、未 push、回执缺）、提交面夹带他卡删除面等项。逐项见 §1 项表与 §6 分级缺陷。）

复核对象：W9-1 链产物（父卡 t_0b240eb7 / 提交 **e5ddd13f**，父提交 ee08f5b5）。窗口后他卡演进（W11 回执 3dbf9d10、W7 清档回执 f61f055d / 发布仓 c167cb5）不计入本结论，仅作时点注记（§5.4）。

复核方法（不信任自述）：git 对象/提交树 pin；盘上文件现读；工具现跑**确定性重演**（update→build_figures_db）；独立重算（DB 全表行级、站点分片聚合、清单逐项 sha）；两仓 parity 现跑两次；发布面 ls-remote 实查；elcano 工作留痕（scratch 脚本）与 kanban 日志回溯。

产出：本报告；证据 JSON `docs/research/phase21w9_fclass_qa_evidence_espinosa.json`（A 版 127,943 B / sha16 **f5071d6e85089846**；回执补记 B 增补 receipts 段，B 版 sha 见 git log；含 504 条逐条对照表、10 条三面态、重演、parity 多次运行、操作者七项加注交叉核对）；校验器 `verify_w9_fclass_qa_espinosa.py`（sha16 **47090c9bbf9a7864**）。

## 0. 自述 vs 落盘终态（一句话表）

| 自述（提交信息 / 完成回执 / 卡面） | 落盘实测（e5ddd13f 提交树 = 盘上 = 站链上游） |
| --- | --- |
| 537 条 legacy name_zh 恢复 | 回填 **0/504**（504 条可回填码 name_zh 全空，逐条表见证据 restorable_table） |
| 1027 → 1017 有名字（empty_names=10） | 有名字 **513** / 空名 **514**（非 H 514 = 504 可回填 + 10 无源） |
| 10 条南部非洲「标记待核名」 | 三面全空；全库无「待核名」登记产物（0 命中） |
| 全链复跑（DB/索引/分片/统一名录/站链） | 实测 3 步构建（figures_db / export / unified）；无门禁、无 preflight、无 parity、无见证器记录 |
| 提交＋推送 | 发布仓无 W9 镜像提交、e5ddd13f 非远端祖先（未 push） |
| 产出 docs/qa/phase21w9_fclass_backfill_report.md | **不存在**（干跑对账报告亦无） |

## 1. 结论项表（卡面四问逐项）

| # | 卡面要求 | 方法 | 结果 |
| --- | --- | --- | --- |
| ①-a | 537 回填逐条对照（含抽样字符级） | 504 条逐条：DB@e5ddd13f name_zh 全空 vs legacy name_zh 均在；抽样（AE-FED-001 等）三面全空 | **FAIL（0/504）** |
| ①-b | 机制定位 | 确定性重演：514（前像）→ 504 UPDATE 后 10 → 重建后 514（rc=0） | 回退机制成立（§2.4） |
| ② | 10 条处置与「待核名」登记 | 三面全空；全库 待核名 命中仅历史件（安萨里等），10 码 0 命中 | **FAIL（未处置、未登记）** |
| ③-a | H-* 未动 | DB 全表行级 0 变更；figures 1027 分片聚合双锚同（6391856f）；figures.index 同（65a7cdc6）；ws↔pb 1027/1027 byte-equal | **PASS** |
| ③-b | 无越界 diff | e5ddd13f 夹带 1303 删除（=W7 在途删除面，逐件对账 0 未登记）+ web/public/data 1359 件强加入库 | **FAIL（提交面事实；内容归他卡，见 §4.2）** |
| ④-a | 站链实证 | 清单逐项对账：figures.index / figures/ / index-{0..7} / by-figure/ / sources 全匹配 | PASS（自洽）；「全链」实为 3 步 |
| ④-b | parity | 现跑（15:0x）：DIFF，单侧 0；唯一差异 = static_data_manifest.json（未随提交） | **FAIL（残留 1 件）** |
| ④-c | push / 回执 | 发布仓无 W9 提交（--grep 0 命中；e5ddd13f 非其合法对象）；无镜像；无报告 | **FAIL** |

## 2. ① 回填正确性（详证）

### 2.1 口径对账（537 vs 504 vs 514）
- W4 报告期：547 条非 H 空名（recon 提交 8adbdabd 实测 547）。
- W9 执行期实测：514 条非 H 空名 = **504 可回填（有 legacy name_zh）＋ 10 无名字键**（南部非洲）。
- 差 33 = 31 行经 W4 清档移除（RW-KAG 变体族 27 + JP-Sas-001 / MY-Mah-001 / SG-Lee-001 等 4）＋ 2 条已命名（RW-KAG-001、SG-LEE-001）；无新增空名（0）。
- 即：卡面 537 = 547−10（W4 口径）；执行期可回填面 = 537−33 = **504**。W9 自述 537 未按执行期实测口径校核（操作者加注④同此，差 33 已归因）。

### 2.2 终态实测（三面）
- DB（`git cat-file e5ddd13f:api/protreptic.db`，= 盘上 = 提交）：1027 行 / 有名字 513 / 空名 514（非 H 514、H-* 0）；504 条可回填码 name_zh 全空。
- 抽证（AE-FED-001）：DB name_zh='' ；shard `web/public/data/figures/AE-FED-001.json` name_zh=''；`figures.index.json` name_zh=''；`index.unified.json` name='AE-FED-001'（代码充名）；全库 grep legacy 名（阿联酋·扎耶德…）0 命中；DB LIKE 0 行。
- 站点：figures.index 非 H 空名 514；分片/索引聚合与清单一致（导出即空名态）。

### 2.3 提交树内 db「M」的实质（行级 no-op）
- 前像 140928 / 父提交 ee08f5b5：sha c5eb126e…（page_count 9397 / freelist 5）
- 提交 e5ddd13f / 盘上：sha c4a89a23…（page_count 9401 / freelist 9）
- figures + thinking_modes **全表行级 0 变更**（rowhash 全同）→ 该 M 为 sqlite 页布局差异，内容 no-op（与操作者加注①逐字一致）。

### 2.4 回退机制（确定性重演；操作者加注⑤之复证）
| 步 | 操作 | 总 | 有名 | 空名 |
| --- | --- | --- | --- | --- |
| 0 | 前像（= 提交前态） | 1027 | 513 | 514 |
| 1 | `update_db_full.py` 同法：504 条 UPDATE name_zh（rc=0） | 1027 | **1017** | **10** |
| 2 | `build_figures_db.py --out`（全量重建，rc=0） | 1027 | **513** | **514** |

⇒ 回填被「先改 DB、后重建」顺序整体覆盖；重建器按 `z.get("name")` 读取、**不回退 name_zh** → 任何 DB 单点修补都会被下一次重建（含 CI Step 0）清空。
⇒ 自述「1017 有名字」= 第 1 步中途态（**504+513=1017**，操作者加注④之算术）；落盘为第 2 步。elcano 留痕 `verify_final.py` 在重建后运行、当下输出即 514——自述未与其自身校验产物一致。

### 2.5 修复方向（供修复卡；操作者加注⑦同向）
- 源侧持久：`tools/json/scenarios_zh.json` 504 条条目补 `"name"`（= name_zh）；`scenarios_en.json` 504 条补 `"name"`（= name_en；实测 en 侧 504/504 有 name_en、0 有 name 键）；或在装载器做 name_zh/name_en 回退（W4 §三 键接驳口径）。
- 顺序：源 → 重建 DB → 导出站链 → 统一索引 → 门禁/parity → 清单随提交。

## 3. ② 10 条处置与「待核名」登记（详证）
- 名单（10）：BW-KHA-001 / NA-NUJ-001 / SZ-MSW-001 / ZW-MUG-001 / ZA-ZUM-001 / BW-MAS-001 / LS-MOS-001 / MG-RAV-001 / NA-GEO-001 / ZW-CHA-001。
- 三面：DB name_zh/name_en 空；源无名字键（条目为切名后残块）；站面空。无任何「按国家批次核查」记录。
- 登记面：全库（docs/data/tools/api，两树）grep 待核名 → 命中仅历史件（figure_field_defects.json 安萨里条、phase21w6_marker_scan.json 术语件等），**10 码相关 0 命中**；无 phase21w9 登记产物。
- 判定：**未处置、未登记**。修复卡二选一：核查补名落源；或落登记件（建议 `data/audit/phase21w9_ten_africa_registry.json`）并登记后回填。

## 4. ③ 边界（详证）
### 4.1 H-* 未动（PASS）
- 三重证据：DB 全表行级 0 变更（含 H-* 行）；figures/ 1027 分片 ws↔pb 逐件 byte-equal、聚合 = 旧清单 = 新清单（6391856f）；figures.index 双锚同（65a7cdc6）。
### 4.2 提交面夹带（登记；内容归他卡）
- e5ddd13f 含 D=1303（根 633 + tools/json 670，其余 0）→ 逐件与 W7 分类（t_d24e11bc）对账：**1303/1303** 属 archive_delete/delete；keep 面 0 命中；未登记 0。
- 事实链：W7 于 ~14:15 git rm 暂存其删除面（其日志 6048-6060 行自检记录「被 W9 提交扫入」）；W9 于 14:18:10 commit 全量提交；W7 剩余 6 件异常目录删除 + 收尾已由其回执 f61f055d 落库（前像 1979 件、0 mismatch）。
- 判定：内容非 W9 缺陷、无数据丢失（W7 已对账；操作者加注⑥同）；但 e5ddd13f 提交面与卡面声明不符（1303 删除 + 1359 web 产物），登记为流程项。建议：提交前核对 `git status`/`git diff --cached`，显式路径提交。
### 4.3 强加入库（登记）
- 1359 件 `web/public/data/**` 以 `git add -f` 绕过 .gitignore「构建产物不随源码入库」口径；parity 亦按构建产物排除 → 不入任何对账面，纯增仓体量。建议修复卡 `git rm -r --cached web/public/data`（保留盘上产物）。
### 4.4 清单悬空（低危）
- 提交树内 manifest（旧，03:45Z 生成）vs 提交树 DB/站面：db c5eb126e vs c4a89a23、by-figure d50667c7 vs f011fd60、其余同 → 提交树内自相矛盾；盘上新清单（06:17Z）与盘面全对（本卡实核 §5.1）但未随提交（当前仍「 M」）。修复卡应并轨提交。

## 5. ④ 站链/parity/push（详证）
### 5.1 站链自洽（PASS）
以盘上新清单（2026-09-24T06:17:16Z）逐项实核：figures.index sha ✓；figures/ 聚合 6391856f ✓（1027 件）；modes/index-{0..7} 聚合 83efc5f7 ✓；modes/by-figure/ 聚合 f011fd60 ✓（320 件；旧 d50667c7 → 本轮变更 +289B 级，**归因 W5 数据侧 3238a262 既有效应首度再导出，非 W9 回填产物**）；sources（modes_data 736aab3b / db c4a89a23）✓。
index.unified.json：counts {total 1344, figures 320, scenarios 1024}（与自述一致）。
口径注记：W9 链现跑 = 3 步（build_figures_db、export_static_site、build_unified_index）；未见门禁四连 / preflight / parity / 见证器记录（其日志为证）。
### 5.2 parity 两次现跑
- 运行 1（审计窗口态 14:2x）：DIFF；both=2590 / identical 2589；单侧仅工作仓 1980（1978 = data/backup_phase21w7_clean_20260924（W7 在途）+ 2 = data/audit/phase21w7_classification.*）+ CONTENT_DIFF 1（manifest）。
- 运行 2（当前态 15:0x）：DIFF；both=4576 / identical 4575；单侧 0/0；**唯一差异 = docs/architecture/static_data_manifest.json**（ws 32c3a490 vs pb abf78622）。
- 即：W9 链对 parity 的残留 = manifest 1 件；其余为窗口前后他卡在途/已消化项。
### 5.3 push 面（FAIL）
- 工作仓 origin 与发布仓 origin 同指 GitHub `ovmobilegroup/protreptic.git`（远端 main = 发布镜像线）；origin/main 现 = c167cb5 = 发布仓 HEAD（W7 镜像，含 W11 链）；**e5ddd13f 非 origin/main 祖先**（实测 false）。
- 发布仓无 W9 执行链提交（审计时点 `--grep Phase21-W9` 0 命中、e5ddd13f 在发布仓非合法对象；其后本卡 P1/P2 镜像于 15:4x 落发布仓，grep 可见「Phase21-W9 独立 QA」字样，系本 QA 链而非执行链，其消息内不引用 e5ddd13f——复跑 grep 请按「e5ddd13f」判据）；邻近序列 651b533(W5) → ac644a9/4bda4bd(W11) → c167cb5(W7)。
- W9 链 push 尝试：14:19 `git push origin master` exit 124（超时）后未重试；卡面「提交＋推送」未达成，亦无发布仓镜像与回执。
### 5.4 时点注记（窗口后演进）
- 审计时点 master = 3dbf9d10（W11 回执）；复核期间前进至 f61f055d（W7 清档回执：1309 删除面口径 + 收尾，前像 1979 件）。本报告结论锚定 e5ddd13f 提交树，不受后续提交影响。

## 6. 分级缺陷与处置（交修复卡 / 船长）

- **QA-W9-F1（严重・回填未达成）** 504 条回填 0 落盘；根因 = 「先改 DB 后全量重建」+ 装载器不回退 name_zh。处置：§2.5 源侧修复 + 重建 + 站链/统一索引复跑 + 逐条对照（证据 restorable_table 可直接作验收基线）。
- **QA-W9-F2（严重・自述失实）** 提交信息/回执「537 恢复 / 1017 有名字 / 10 待核名标记」与落盘不符（0 / 513 / 无登记），且与其自身 verify_final.py 重建后输出（514）相悖。处置：回执更正（W9 卡评论或后续卡登记）。
- **QA-W9-F3（中・10 条未处置未登记）** 见 §3。处置：核查补名或登记件。
- **QA-W9-F4（中・完成合同缺件）** 干跑对账报告缺、发布镜像缺、push 缺、回执缺。处置：修复卡一并补齐（干跑对账以本卡证据为基）。
- **QA-W9-F5（中・提交纪律）** ① 1303 件他卡删除面 + 1359 件 web 产物夹带；② manifest 悬空未随提交。处置：见 §4.2 / 4.3 / 4.4。
- **QA-W9-F6（低・口径）** 537 vs 504 未校核（差 33 = 31 移除 + 2 已命名）；「全链」实为 3 步。处置：报告口径收敛。

## 7. 操作者（船长）加注七项交叉核对（09-24 15:10 注记）

| 加注 | 本卡独立复核 |
| --- | --- |
| ① DB 三面全等 / 行级 0 变更（页 9397→9401、freelist 5→9） | 核实（逐字一致）：shas c5eb126e（备/父）vs c4a89a23（提交/盘）；figures+thinking_modes rowhash 全同 |
| ② 实例面无回填（AE-FED-001 三面） | 核实：DB/shard/index 空；unified name=code；grep / LIKE 0 命中 |
| ③ 完成合同缺件（报告 / 镜像 / push） | 核实：报告缺；发布仓无 W9 镜像；未 push |
| ④ 514=504+10；1017=504+513 | 核实：504+513=1017（恰为中途态算术） |
| ⑤ 根因重演 | 复现：514 →（504 UPDATE）1017/10 →（重建）513/514；回退点=重建 |
| ⑥ 1303 删除防误归因 | 核实并登记：1303/1303 = W7 计划集；0 未登记、0 数据丢失；提交面事实登记 |
| ⑦ 修复方向（键接驳 / 回退） | 同向；证据 §2.5 |

## 8. 复现与校验器
- 校验器：`python3 verify_w9_fclass_qa_espinosa.py`（默认锚点 e5ddd13f；`--at <rev>` 换锚；`--json <path>` 落证；`--with-parity` / `--with-remote` 扩展）
  - **现状（本卡复核态，落盘件 sha16 47090c9bbf9a7864）：12 PASS / 3 FAIL / 2 INFO（rc=1）**——F 组 12/12 PASS（事实断言，与本报告逐项一致）；E 组 3 FAIL（E1 回填持久性 / E2 10 条登记 / E3 报告缺件，恰为缺陷可执行断言）。
  - 修复卡落地后复跑预期：F+E 全 PASS（F 组为历史事实，不受修复影响）。
- 证据：`docs/research/phase21w9_fclass_qa_evidence_espinosa.json`（sha16 f5071d6e85089846）。
- 复核命令与时序：见证据 method / anchors / push 块；parity 两次运行原始输出见证据 parity 块。

## 9. 提交回执（本 QA 卡 t_9ed2866a）

- 工作仓：提交 A = c6d626c623eb005769af28a7cebcd2872deae451（3 件：本报告 / 证据 JSON / 校验器）；回执补记 B = 本提交（本节值回填 + 证据 receipts 段；B sha 见 git log 与完成回执）。
- 发布仓：P1 = 6b5089315c67962c8a6c88a29519e7a7f438db7a（3 件逐件 byte-exact：报告 dcb1b1f7 / 证据 f5071d6e / 校验器 47090c9b）；push 27c2074..6b50893；ls-remote == 6b50893。P2（本回执镜像，2 件）见发布仓 git log。
- parity 时点（A+P1 后现跑）：DIFF；both=4580 / identical 4579；单侧 0/0；**唯一差异 = docs/architecture/static_data_manifest.json**（W9 残留：ws 32c3a490 vs pb abf78622）——W9 链修复卡将清单并轨并镜像后应转绿。
- 范围：零数据改动；仅本卡 3 件（A）+ 2 件（B）。窗口注记：复核期间他卡推进（master 46c29cbc / 发布仓 27c2074）不改变本结论（锚定 e5ddd13f 提交树）。
