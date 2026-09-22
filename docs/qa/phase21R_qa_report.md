# Phase21-R 独立验收报告（QA 卡 t_7ccb530f）

- 复核对象：修复卡 t_3e74b456（barbosa）「Phase21-R 主库数据修复：恢复 20 位 / 194 条」
- 工作仓提交：`0309093a`（16 路径）+ 报告修订 `b1310553` / `97879127` / `aa2ac473`
- 发布仓提交：`bc8efec` / `5ebffe5` / `b2e5c0e` / `2617587`（HEAD）
- 验收方式：**独立复跑** —— 全部断言由本卡脚本 `verify_phase21r_qa_espinosa.py`（A~F 六段）现场重建，不引用修复报告结论；脚本位于仓库根，随本验收提交入库。
- 脚本证据：首轮（20:18:11）全部断言通过、`RESULT: PASS`（退出码 0）；终轮（20:26 实时复查）见 §10 —— 并发卡在制使 D1/E1 两段出现预期差异，其余 38 项断言仍全过。
- **结论：PASS —— 通过**。20 位 / 194 条全部可溯源、零捏造；两仓 parity（在验收对象提交时刻）零差异；站点计数链与主库 3142 口径一致；报告与审计自洽。问题清单 7 项均为记录性观察，无返工项。

环境：工作副本 /opt/data/workspace/Protreptic；发布仓 /opt/data/release/Protreptic-publish；验收时间 2026-09-22 20:00~20:25（CST），最终整理于 2026-09-22 20:24:43。

## 0. 清单对照

| 清单项 | 验收动作 | 结论 |
|---|---|---|
| 1 检索核验 | 20 位/194 条在两仓逐条命中；id/mode_code 全库唯一性 | PASS（§1） |
| 2 源对照 | 全量 20 位 200 条逐字段比对声明来源 + 反例检查 | PASS（§2） |
| 3 顾炎武专项 | 处置明确性 + 现库一致性 | PASS（§3） |
| 4 审计重跑 | F1/F2 原样重跑 vs phase21r_audit.json | PASS（§4） |
| 5 同步与门禁 | parity；发布仓 ahead=0；站点产物 vs 主库 3142 口径 | PASS（§5，含并发观察 O7） |
| 6 文件核查 | 报告/审计双仓存在 + 自洽 10 项交叉核对 | PASS（§6） |
| 7 输出 | 本报告 | 已交付 |

## 1. 检索核验（清单 1）PASS

命令：`python3 verify_phase21r_qa_espinosa.py`（B 段）→ 全部命中。

| figure_code | 人物 | 类别 | 本次恢复 n | id 区间 | 声明来源 |
|---|---|---|---|---|---|
| H-BLT-001 | 柏拉图 | A | 10 | M-BLT-001~M-BLT-010 | archive, commit:072bd72a |
| H-SQR-001 | 苏格拉底 | A | 10 | M-SQR-001~M-SQR-010 | archive, commit:f8514b54 |
| H-ZHX-001 | 朱熹 | A | 10 | M-ZHX-001~M-ZHX-010 | commit:8e4e5dd4 |
| H-YLS-001 | 亚里士多德 | A | 10 | M-YLS-001~M-YLS-010 | archive, commit:47bf8546 |
| H-SJM-001 | 释迦牟尼 | A | 10 | M-SJM-001~M-SJM-010 | archive, commit:a6c37c4d |
| H-DRK-001 | 德鲁克 | A | 10 | M-DRK-001~M-DRK-010 | archive, commit:5a4758fa |
| H-DA-001 | 道安 | A | 10 | M-DA-001~M-DA-010 | commit:0e78ffa5 |
| H-GX-001 | 郭象 | A | 10 | M-GX-001~M-GX-010 | archive, commit:e51bdae6 |
| H-JY-001 | 贾谊 | A | 10 | M-JY-001~M-JY-010 | commit:99a47440 |
| H-WB-001 | 王弼 | A | 10 | M-WB-001~M-WB-010 | commit:af79031a |
| H-SY-001 | 商君 | A | 10 | M-SY-001~M-SY-010 | archive |
| H-XFZ-001 | 谢富治 | A | 10 | M-XFZ-001~M-XFZ-010 | archive |
| H-GYW-001 | 顾炎武 | A | 10 | M311~M320 | archive, commit:959525d4 |
| H-JMLS-001 | 鸠摩罗什 | A | 10 | M-JMLS-001~M-JMLS-010 | commit:1b8c56ce |
| Homer | 荷马 | C | 10 | M-HOM-001~M-HOM-010 | archive, figure-embed |
| Coubertin | 顾拜旦 | C | 10 | M-COU-001~M-COU-010 | archive, figure-embed |
| Sophocles | 索福克勒斯 | C-closure | 10 | M-SOP-001~M-SOP-010 | boards-archive, boards-figure-embed |
| Thucydides | 修昔底德 | C-closure | 10 | M-THU-001~M-THU-010 | boards-archive, boards-figure-embed |
| H-NKR-001 | 恩克鲁玛 | D-NKR | 4 | M-NKR-006~M-NKR-009 | commit:c949e76d, figure-embed |
| H-QIN-001 | 李斯 | B-QIN | 10 | M-QIN-001~M-QIN-010 | archive |

- 两仓（工作仓 / 发布仓）逐条命中：20 位各 **10/10**；恩克鲁玛恢复 4 条后 10/10（M-NKR-006~009）；李斯 `M-QIN-001~010` 全在。
- 唯一性：全库 3142 条中 2742 个 distinct id、3132 个 distinct mode_code，**0 重复**；恢复的 194 条全部带 id。
- 观察 O1：无 id 条目口径（§7）。

## 2. 源对照（清单 2）PASS（全量 20 位，超出「抽核 ≥8 位」要求）

比对方法：对 20 位恢复条目逐字段（name_zh / name_en / definition_zh / definition_en / domain_zh / domain_en / key_concepts / key_quote_* / source_chapter / related_modes 等）与其声明来源逐一比较（JSON 规范化后逐字节一致判定）；来源取自 `git show <sha>:data/modes_data.json`（合并提交载荷）、`data/individuals/*` 档案、boards 副本与 figure 内嵌。

| 来源类型 | 覆盖 | 结果 |
|---|---|---|
| 合并提交载荷（13 位） | 柏拉图 072bd72a / 苏格拉底 f8514b54 / 朱熹 8e4e5dd4 / 亚里士多德 47bf8546 / 释迦牟尼 a6c37c4d / 德鲁克 5a4758fa / 道安 0e78ffa5 / 郭象 e51bdae6 / 贾谊 99a47440 / 王弼 af79031a / 鸠摩罗什 1b8c56ce / 顾炎武 959525d4（辅助键）/ 恩克鲁玛 c949e76d | 各 10/10（恩克鲁玛 4/4）逐字段一致 |
| individuals 档案 | 商君 / 谢富治 / 李斯 / 顾炎武（主字段） | 各 10/10 逐字段一致 |
| boards 副本 | 荷马 / 索福克勒斯 / 修昔底德（modes_data 副本）、顾拜旦（figure 内嵌） | 各 10/10 逐字段一致 |
| figure 内嵌 | 恩克鲁玛新增 4 条（category 归一后同步） | 0 内容差异 |

记录在案的转换（4 类，均为「内容保真」而非改写）：

1. 王弼：payload `related_modes`（自由文本陷阱）→ `failure_pitfalls_zh`，内容 10/10 逐字保真（C5）；
2. 恩克鲁玛：`category` 三元组 → 标准类目（政治治理/哲学形而上/伦理修养），4 条与 audit `normalizations.NKR_category.after` 完全一致（C6）；
3. 顾炎武：主字段来自档案；`contrast_modes` / `cross_domain_mapping` / `historical_context` 三键来自提交 959525d4 且逐字一致（C7）；
4. 李斯：`id` / `mode_code` / `related_modes` 重编号 M391~M400 → M-QIN-001~010（规避与库内既有 M391/M393/M400/M402 冲突），其余字段与档案 10/10 一致（C4）。

选源说明（非转换，反例复核）：顾拜旦恢复取 boards figure 内嵌版（完整文本），boards `modes_data` 副本为更短旧文本 —— 本卡独立复核确认两者确不同、恢复取源与报告 §2/§3.1 声明一致。

无捏造判定（C8，反占位检查）：对 200 条 × 全部字段做「来源并集」溯源（档案 ∪ 合并提交 ∪ boards 副本 ∪ figure 内嵌），未命中 **0**；不存在只在库内出现而无任何来源的内容。

## 3. 顾炎武（H-GYW-001）专项（清单 3）PASS

- 报告处置明确：§2 清单行「顾炎武 +10（M311~M320）」；§3.1 注明主字段取档案、三键取提交 959525d4；§4.2 F2 表 GYW 行注「按 figure_code 口径 10 条」—— 属**恢复入库**结论，非「待决策」。
- 现库与报告一致：`M311~M320` 存在、`figure_code=H-GYW-001`；三键与提交逐字一致；主字段与档案 10/10（C1/C7）。
- 卡面预设「该恢复而未入 → 记缺陷」：不适用（已恢复，0 条遗留）。

## 4. 审计重跑（清单 4）PASS

- F1（v6 型 claims 扫描，脚本原样重跑）：结果与 audit `audit_F.F1_v6_claims.after` **完全一致** = `{"H-BG-001.json": 10, "H-SJL-001_modes.json": 10}`（18 件收敛为 2 件）；`unresolved = 0`，两件均列明依据（BG→E1、SJL→E2）。✔
- F2（合并提交 × 现库交叉表，脚本原样重跑）：与 audit flagged 8 代号 **完全一致**（BG/CH/DZS/GYW/SJL/SQIN/SX/ZX；仅 DZS=1/10，其余 0/10）；`unresolved = 0`。✔
- GYW 注解成立：库内 `M-GYW-*` 码 0 条、`figure_code=H-GYW-001` 10 条（D5）。✔
- 判定：v6 型缺失 = 0 或全部为已列明例外 —— 满足。✔
- 附带复核：findings delta 独立复算与 audit 记录一致（156→165：D4_quote_without_source +10、D4_quote_mismatch +1、D6 −2）。✔
- 观察 O2：F2 输出中 commit 记号列对 CH 显示 `6830059b`（陆九渊入库提交）—— 脚本以「首个命中该代号正则的提交」为记号；audit 表 basis 注解正确，不影响结论（§7）。

## 5. 同步与门禁（清单 5）PASS

1) 两仓 parity（验收对象提交时刻）：
   - 独立运行 `tools/check_repo_parity.py --json`（20:07:52）与脚本 E1（20:18:11）均 exit 0、`status=OK`：`{workspace_in_boundary: 1538, publish_in_boundary: 1538, both_sides: 1538, identical: 1538, only_workspace: 0, only_publish: 0}` —— **零差异**。✔
2) 发布仓推送状态：
   - `HEAD = origin/main = 26175873`；`git rev-list --left-right --count origin/main...HEAD` = `0 0`；`git status --short` 空。与修复卡完成元数据（`publish_push: origin/main = 2617587, ahead=0, clean`）一致。✔
   - 说明：该项以本地 remote-tracking ref 核对；对外网远端做实时复核的尝试失败（`git ls-remote` → GnuTLS handshake failed，环境网络不可用），故联网核验不可行，以本地引用 + 修复卡推送回执为据。
3) 站点重建产物 vs 主库（3142 口径）：

| 指标 | 值 | 判定 |
|---|---|---|
| meta.modes_raw | 3142 = 现库条目数 | ✔ |
| meta.modes_deduped | 3132 | ✔ |
| meta.mode_summaries_published | 3072 = 3132 − 60 | ✔（published = dedup − 隔离） |
| meta.modes_quarantined | 60 | ✔ |
| by-figure 分片 | 304 | ✔ |
| figures | 1057 | ✔ |

   - 锚点：`tools/export_static_site.py` 与 `tools/pages_preflight.py` 同为 EXPECT_MODES=3132 / EXPECT_BY_FIGURE=304；`web/src/generated/siteCounts.ts` = 3072 × 304。✔
   - 独立复跑 `python3 tools/pages_preflight.py --stage data` → 全部断言通过（figures=1057 modes=3132 published=3072 隔离命中=0）。✔
   - 恢复 20 位在 by-figure 分片全部可见（含各片首尾 id）；无隔离泄漏（M-SX-* 0 命中）。✔
4) 观察 O3（非缺陷）：`api/protreptic.db` 两仓字节不同 —— parity 工具**显式排除**该文件（理由：CI Step 0 由 `build_figures_db.py` 清表重建，committed 内容不进构建结果；两仓 `.github/workflows/pages.yml` 均含该 Step）。独立核对：本卡对库文件的**逻辑内容零变更**（figures / thinking_modes 两表逐行比对差异 0，仅页面级字节重排）；库内 `thinking_modes` 表停留 2858 行为历史快照，CI 重建的库不含该表（`build_graph_data.py` 仅本地回退读取，链条以 `data/modes_data.json` 为准）→ 站点/CI 不受影响（§7）。
5) 观察 O7（并发实时状态）：终轮复查（20:22:30）parity 显示 1 条差异 —— `data/audit/phase20R_zengzi_residual_scan.json`（仅工作仓、untracked、mtime 20:19:33）：由**并发运行**的卡 `t_6c92966b`（Phase20R 曾子补做 · serrano · running）现场生成，晚于本验收对象的全部提交（≤20:18），与本验收对象无关。已按 hotspot 惯例记录（kanban 备注 + 完成元数据），待该卡镜像同步后自然归零。

## 6. 文件核查与自洽（清单 6）PASS

存在性与哈希（双仓一致）：

| 文件 | 工作仓 sha256 | 发布仓 sha256 |
|---|---|---|
| docs/qa/phase21R_restore_report.md | 5bf0e910bbbe6807c3dba6c7f1a6213af52cb679ae25da60372181f4bf471de5 | 5bf0e910bbbe6807c3dba6c7f1a6213af52cb679ae25da60372181f4bf471de5 |
| data/audit/phase21r_audit.json | dc84331f2b9b91f8d99405674f2d5797bce8c4035a42891869699b02dc31c2d9 | dc84331f2b9b91f8d99405674f2d5797bce8c4035a42891869699b02dc31c2d9 |

自洽性交叉核对（10 项，独立复算，非引用报告）：

| # | 检查项 | 结果 |
|---|---|---|
| 1 | audit 总量 194 = Σ{A140, C20, C-closure20, D-NKR4, B-QIN10} | ✔ |
| 2 | 前后计数 2948→3142、distinct 2938→3132（用 git 快照 `0309093a^` 独立复算） | ✔ |
| 3 | restore.ids_all_present=true 且 20 位 n/ids 与现库一致 | ✔ |
| 4 | findings delta 独立复算 = audit.findings_delta（156→165） | ✔ |
| 5 | site_counts before/after 与实况一致（锚点/meta/分片，§5.3） | ✔ |
| 6 | publish_sync 92 复制 / 4 删除：4 删除路径在发布仓确不存在；parity 复现 0 差异 | ✔ |
| 7 | 报告 §5.3「34 条 dict 内嵌内容字段零差异」独立复跑成立（YLS/SJM/DRK 各 10 + NKR 恢复 4；双仓共 68 次比对，0 差异） | ✔ |
| 8 | 报告观察复现：`apply_verification_status.py --check` 报 73 条漂移（72 pending + 1 suspect） | ✔ |
| 9 | 报告观察复现：H-DY-001 码冲突（figure 档/figure_names=董宇明 vs 库内 H-DY-001=杜威 M-DY-001~010） | ✔ |
| 10 | 报告修订 3 提交（b1310553/97879127/aa2ac473）均只改报告文件（零数据改动） | ✔ |

- 观察 O4：报告 §9「图档镜像 6 件」与提交 16 路径不严格对应（镜像面实为 7 件：data/figures 3 + docs/figures 2 + data/individuals 2）；建议改为精确枚举（§7）。
- 观察 O5：`data/figures/H-NKR-001.json` 既有 6 条（M-NKR-001~005/010）内嵌与库内存在三元组/文本差异 —— **先于本卡**（`0309093a^` 快照与现库差异集合逐条一致；本卡只同步恢复 4 条）；报告 §5.3 的 34 条零差异声明范围不含这 6 条（§7）。

## 7. 问题清单（本验收发现的全部问题/观察）

| # | 级别 | 位置 | 内容 | 建议 |
|---|---|---|---|---|
| O1 | 低（文档口径） | audit F3 / 报告 §4.3 | 「390 条无 id」与独立计数「无 id = 400」口径易混淆：2742 + 390 + 10 = 3142 仅在把 10 条空码组单列、390 定义为「无 id 但有 mode_code」时成立 | 文案改为「无 id 共 400：其中 390 有 mode_code、10 为空码组」 |
| O2 | 低（脚本可读性） | F2 输出 / audit F2 表 | commit 记号列对 CH 显示 6830059b（首个命中该代号正则的提交），易被误读为来源提交；basis 注解本身正确 | 在该列头标明「首次出现提交（参考）」 |
| O3 | 备注（非缺陷） | api/protreptic.db | 两仓字节不同（parity 明示排除、CI Step 0 重建）；库内逻辑内容本卡零变更；`thinking_modes` 表 2858 行历史快照 | 后续卡评估从 committed 库退役该表 |
| O4 | 低（文档） | 报告 §9 | 「图档镜像 6 件」与 16 路径不严格对应（实际 7 件） | 改为精确枚举 |
| O5 | 备注（先于本卡） | data/figures/H-NKR-001.json | 既有 6 条内嵌三元组/文本差异未归一 | 后续卡按 NKR_category 归一先例评估 |
| O6 | 备注（先于本卡） | figure 档 / figure_names | H-DY-001 码冲突（董宇明 vs 杜威）；报告已列为观察，本卡复核属实 | 已由 t_72e34e75 纳入处置 |
| O7 | 备注（并发） | data/audit/phase20R_zengzi_residual_*.json / data/figures/H-ZX-001*.json 等 | 并发卡 t_6c92966b 的在制产物（20:19~20:26）使实时 parity 出现 8 条仅工作仓 + 2 条 H-ZX-001 图档内容差异；与本验收对象无关 | 待该卡提交/镜像后自然归零（见 §10） |

级别定义：低 = 建议改进、不影响交付正确性；备注 = 事实记录（非缺陷）。
后续卡关联（观察已被跟进卡覆盖）：`t_72e34e75`（编码归一清理：BG↔BAN · SJL 旧码 · H-DY-001 · verification 漂移 73，running）、`t_a060cd41`（旧世代 20 件 v6 复刻评估，running）。

## 8. 复跑命令

```
python3 verify_phase21r_qa_espinosa.py             # A~F 六段断言；验收对象提交时刻 RESULT: PASS
python3 tools/check_repo_parity.py --json          # 期望 exit 0、diffs 空（并发卡在制时以其产物为准）
python3 tools/pages_preflight.py --stage data      # 期望全部断言通过
python3 tools/apply_verification_status.py --check # 期望 73 条漂移（他卡在制，先于本卡）
git -C /opt/data/release/Protreptic-publish rev-parse HEAD origin/main
```

## 9. 交付与镜像说明

- 本报告：`docs/qa/phase21R_qa_report.md`（工作仓，随本验收提交入库）；独立脚本：`verify_phase21r_qa_espinosa.py`（仓库根，A~F 六段断言，可离线复跑）。
- 工作仓提交：`690c0223`（QA 报告 + 独立脚本）；本 §10 并发补记与 §9 哈希注记随后续报告修订提交入库（报告层零数据改动）。
- 镜像：因 parity 口径覆盖 `docs/**`，本报告同内容放置于发布仓工作树 `docs/qa/phase21R_qa_report.md`（未提交，待下一次镜像提交入库；发布仓 HEAD 维持 `2617587`，ahead=0 不变；验收时外网推送不可用：`git ls-remote` GnuTLS handshake failed）。
- 本验收未改动任何数据文件；工作区中其他卡的未提交在制文件（verification_status.json、H-LJY-001.md、phase20_zhoudunyi_qa_evidence.txt 等）未被触碰。

## 10. 并发在制记录（本卡定稿后实时复查，2026-09-22 20:26）

本卡收尾期间，看板上有其他卡在同一工作副本并发作业；以下实时状态差异**均与本验收对象（`0309093a` 及其报告修订）无关**，属在制品：

- 卡 `t_6c92966b`（Phase20R 曾子补做 · 深度研究，serrano，running）：新增未跟踪文件 `data/audit/phase20R_zengzi_residual_scan.json`（20:19:33）、`data/audit/phase20R_zengzi_residual_inventory.json`、`data/backup_phase20R_H-ZX-001_20260922_2021/`（4 件）、`docs/research/phase20R_zengzi_residual_inventory.md`、`docs/research/phase20_zengzi_research_final.md`；并修改（未提交）`data/figures/H-ZX-001.json`（20:26:07）与 `data/figures/H-ZX-001_modes.json`（20:24:02）。
- 直接后果（终轮实时复查 20:26）：脚本 D1（F1 型扫描）实时结果多出 `H-ZX-001.json: 10`（曾子新载荷 `M-ZX-001~010` 尚未合并入库 —— 合并卡 `t_16ebe5c9` 仍为 todo，主库 `M-ZX-*` id 数 = 0、总条目仍 3142）；parity 实时状态 = 8 条仅工作仓 + 2 条 `H-ZX-001*.json` 图档内容差异。两者均随该卡提交/镜像后自然消解。
- 本验收对象在其提交时刻（≤20:18）的全部断言（含 D1 与 E1）为 PASS：见 §4/§5 与脚本首轮输出（工作副本 `verify_out.txt`，20:18:11）。
- 复跑提示：并发卡在制期间运行 `verify_phase21r_qa_espinosa.py`，D1/E1 两段为「实时状态检查」，会出现上述预期差异；其余 38 项断言仍应全过。
- 提交注记（自省）：本卡报告修订提交 `b5d27039` 因共享索引，同时携带了并行卡（`t_72e34e75` 编码归一清理）已 `git add` 的 7 个「0 内容变更」路径（`H-DY-001`→`H-DYM-001` 重命名 4 件、`H-SJL-001` 档案归入 `_duplicates` 3 件）；内容零改动，已在 kanban 备注与完成元数据中说明归属。本卡后续提交改用 pathspec 限定（`git commit -- <path>`）以避免夹带。

（报告完）
