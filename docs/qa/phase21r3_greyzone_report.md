# Phase21-R4 灰区收尾报告（卡 t_ea3a32e5）

- 卡：`t_ea3a32e5`（assignee: barbosa，Phase21-R4「灰区收尾 G1~G5 · 重建推送」）
- 日期：2026-09-22
- 授权：船长已批准 G1~G5 全部执行（用户 2026-09-22「都做」拍板，含公开侧变化）——见卡面 `【授权】` 段
- 事实来源：`docs/qa/phase21r2_cleanup_report.md` §4/§5/§6/§9 + 证据包 `docs/research/phase21r2_cleanup_evidence.json`
- 交付物：本报告 + `docs/research/phase21r3_greyzone_evidence.json` + 可复跑核验脚本 `verify_greyzone_phase21r4.py`
- 结论：**G1/G2/G4/G5 数据落地、G3 verification 四态归位、引用面随迁、曾子四面同体回归修复、站点链条重建、两仓镜像并推送——全部完成；本地核验 `verify_greyzone_phase21r4.py` 38 PASS / 0 FAIL / 6 INFO；门禁 3 条 --hard-fail 全 exit 0；两仓已跟踪面 0 差异（余 15 条为并行卡未跟踪在制产物，见 §9）**
- 工作仓提交：`19b220ab`；发布仓镜像提交：`6fea2e7`（已 push：`3f68f62..6fea2e7 main -> main`）

---

## 1. 基线（改动前）

| 项 | 值 |
|---|---|
| 主库 `data/modes_data.json` sha256 | `9d9c98c5547a7edd4414858dc6c8e498bd659935289f6e4007d495a44eb70d3f`（24,262,313 B） |
| 条目数 | 3152（含 10 条空模式码壳） |
| 站点去重口径 `modes_deduped` | 3132；by-figure 分片 304；figures 1057 |
| 公开 verification | verified 988 / pending 1721+10 非四态 / suspect 33 / unverifiable 340 |
| 锚点（两工具）| `EXPECT_MODES = 3132`、`EXPECT_BY_FIGURE = 304` |
| 两仓 parity | 69 差异（CONTENT_DIFF 16 / 仅工作仓 50 / 仅发布仓 3） |
| 门禁 | G5 前：绿；G5 改名后：credibility_gate --hard-fail **exit 1**（9 条 D6 新增悬空，见 §4） |

事实认定（§4 依据）：`H-BAN-001`/`BAN` = **班昭**；`H-DY-001` = **约翰·杜威**（旧显示名「董宇明」）；`H-BG-001` = **班固**（`91832eb6` 丢失同仇，需回库）；董仲舒旧号 `M01~M10` 与全库唯一裸码冲突，须归一。

## 2. G1/G2/G4/G5 逐项

统一落地脚本：`/opt/data/kanban/boards/protreptic/workspaces/t_ea3a32e5/scripts/greyzone_apply.py`（幂等，含回读自检；日志 `evidence/apply_changes.json`）。前置断言：条目数 ∈ {3152, 3162}、目标 id 在位、跨库交叉校验、备份落盘。

### G1 班昭显示名纠正（10 条）
- 改动：`data/modes_data.json` 中 `M-BAN-001~010` 的 `figure_name` + `figure_name_zh`：`班固` → `班昭`。
- 依据：`H-BAN-001`/`BAN` = 班昭（§4 事实认定）。
- 计数：10 处；其余字段零改写。
- 核验：`verify_greyzone_phase21r4.py` G1.1/G1.1b/G1.2/G1.3/G1.4（含「全库『班固』只属 H-BG-001」）。

### G2 约翰·杜威显示名纠正（10 条）
- 改动：`M-DY-001~010` 的 `figure_name` + `figure_name_zh`：`董宇明` → `约翰·杜威`（仅显示名字段）。
- 计数：10 处；`verify_greyzone_phase21r4.py` G2.1~G2.3（含全库无「董宇明」残留）。

### G4 班固 `M-BG-001~010` 回库（纯增量 +10 + 1 处英文残留清理）
- 来源：`f66bb2fd:data/modes_data.json` 的 figure 级 `H-BG-001.thinking_modes`（前版快照，`id == mode_code == M-BG-001~010`），交叉校验 `data/individuals/H-BG-001_modes.json` 正本。
- 溯源规则：源档字段逐条照抄（零捏造、零改写）；库内按 v6 规范补 `figure_code=H-BG-001`、`figure_name=班固`、`representative_figures` 等面字段。
- 交叉校验：正本 legacy 字段名 → 库内 v6 规范名映射 **9 组 × 10 条逐字一致**（`name_zh/name_en/definition_zh/definition_en/key_concepts/source_chapter/process→process_zh/modern_applications→modern_applications_zh/representative_figures`）。
- 同源清理：`data/individuals/H-BG-001_modes.json` 的 `definition_en` 1 处中英混排 `and求真 spirit` → `and truth-seeking spirit`（以 f66bb2fd 干净英文为准）。
- 计数：+10 条目（含 +10 组 mode 级标签面入站点分片）；`figure_code=H-BG-001` 分片 +1。
- 核验：G4.1~G4.6。

### G5 董仲舒归一：`M01~M10` → `M-DZS-001~010`
- 改动（`evidence/apply_changes.json`：G5 计 16 项）：
  1. `data/modes_data.json`：10 条 `id`+`mode_code` 改名；`research_mode_id` **保留旧号 M01~M10 作为溯源登记**（零悬空、零语义丢失）。
  2. `data/code_maps.json`：`H-DZS-001.mode_ids`、`protreptic_mapping`、`scenarios_zh/en[].mode_id` 随迁。
  3. `data/scenarios_zh.json` / `data/scenarios_en.json`：`C-DZS-001~010` / `…E` 的 `mode_id` 随迁。
- 查重依据：改名后全库 `mode_code` 唯一；裸码 `M01~M10` 不再作为任何 `id`/`mode_code` 存在。
- 引用面随迁（`scripts/greyzone_fix_referrers.py`，日志 `evidence/referrer_fix.json`）：9 条其他人物的 `related_modes` **裸码**引用（`M01`×7、`M03`×1、`M10`×1，见 §4）→ `M-DZS-001/003/010`——保持改名前的解析目标不变，避免新增 D6 悬空。
- 注记形态保留 3 条（如 `M01（董仲舒·天人感应法——…）`）：库内 P24F/P25F 判例已按「合法注记层」处置，审计断言为「bare 悬空 0」，本卡不动。
- 卡面注「库内 WGW/NOB 两处描述曾引用『不存在的 M-DZS-001』，归一后自然对齐」：草证 `data/audit/findings.json` 刷新后 D6 悬空 38 → 37，其中 `M-SALADIN-006` 的 `M-DZS-001` 锚点由「悬空」转「可达」，与该注一致。
- 核验：G5.1~G5.10。

## 3. G3 verification 归位（全库四态）

- 命令：`python3 tools/apply_verification_status.py --write`（唯一实现；G3 在 G1/G2/G4/G5 之后执行）。
- 结果：全库 `verification.status` 收敛为四态 `verified/pending/suspect/unverifiable`（非四态值会令 `tools/export_static_site.py` 的 `verification_counts` 直接 SystemExit——即站点链与「定稿留证口径」的强约束冲突，故必须归位）。
- 公开口径计数（站点 `meta.json`）：**verified 988 → 932、pending 1731 → 1796、suspect 33 → 34、unverifiable 340（不变）**，发布口径合计 3092。
  - 明细：Phase20 漂移 −72（verified→pending）、−1（verified→suspect）、曾子 10 条定稿留证口径归位（+7 verified / +3 pending）、班固 +10 verified。
  - 与卡面预期（988→916 / 1711→1783 / 33→34）差异的原因：卡面锚点在曾子批次与班固回库之前；实测差值已逐项对齐（卡面已声明「以实测为准、如实记录」）。
- 零漂移复检：`python3 tools/apply_verification_status.py --check` → **exit 0**。
- 审计件：`data/audit/verification_status.json` 随写（G3.2 逐条一致）；`data/audit/findings.json` 同步刷新（164 条；D6 37）。
- 说明（口径留证）：工具对纳入判定的条目会同时重刷 `checked_at` 为本次归位日（2026-09-22），属工具口径而非状态变更；`git diff` 中该类行 ~2.9k 行（占本次 modes_data diff 的主体）。

## 4. 引用面随迁与门禁往返（G5 改名的连带修复）

改号为 `M-DZS-*` 后，`M01/M03/M10` 这三个**裸码**不再存在，原先「恰好解析到」董仲舒条目的 9 条跨人物引用随即成为新增 D6 悬空：

| 引用方 | 字段 | 旧值 | 新值 | 解析目标（改名前后一致） |
|---|---|---|---|---|
| M-CC-023 / M-CC-026 | related_modes[3] | M01 | M-DZS-001 | 天人感应法 |
| M-MIY-006 | related_modes[3] | M01 | M-DZS-001 | 天人感应法 |
| M-GUE-007 / M-GUE-009 | related_modes[3] | M01 | M-DZS-001 | 天人感应法 |
| M-WDZ-008 | related_modes[3] | M01 | M-DZS-001 | 天人感应法 |
| M-LZH-004 | related_modes[-1] | M01 | M-DZS-001 | 天人感应法（库内 P25F 判例明载「李泽厚 related_modes 引用董仲舒旧式编号 M01」） |
| M-LIB-006 | related_modes[3] | M03 | M-DZS-003 | 三纲五常法 |
| M-WDZ-010 | related_modes[3] | M10 | M-DZS-010 | 原心定罪法 |

- 处置脚本：`scripts/greyzone_fix_referrers.py`（幂等，备份 + 回读自检；日志 `evidence/referrer_fix.json`）。
- 判据：改名前的解析目标必须保持（引用边零信息损失）；「自指」解释与档案第四槽跨人物惯例、以及列表内已有本人物条目重复矛盾，故不采用。
- 门禁往返：修复前 `credibility_gate --hard-fail` = exit 1（9 条新增 D6 + 3 条过期基线）；修复+findings 刷新后 = **exit 0**（存量 524 条全为冻结基线，新增 0）。
- 回读：全库 `related_modes` 裸码悬空 **0**。

## 5. 曾子（H-ZX-001）四面同体回归修复（响应 QA 卡 t_8ceed107 hotspot）

**报知**（QA 卡 comment 2926）：本卡 G3 将库内 `M-ZX-001~010` 的 `verification` 整体改写为四态口径，导致镜像/正本/伴随包未同步、`verify_hzx_merge_phase20R.py` 由 66/66 降至 59/7。

**裁定：方案 (b)**（全域标准化 + 同步改写正本/三镜像/伴随包 + manifest 留证）。
- 不采 (a)（把 M-ZX-* 排除出自动归位）：非四态 status 会令站点导出 `verification_counts` SystemExit，与「重建推送」硬冲突；且 (a) 需在白名单口径上开口子，违背「规则只写在这里」。
- 执行（`scripts/greyzone_sync_zx_mirrors.py`，日志 `evidence/zx_mirror_sync.json`）：30 处 `verification` 随库同步（图档 `thinking_modes` / 正本 `individuals/…_modes.json` / 伴随包 `figures/…_modes.json` 各 10 条），三镜像字节复制保持同体；仅 `verification` 字段改动，其余字段不同体即 ABORT（实际 0 处）。
- 留证：`data/audit/phase20R_zengzi_landing_manifest.json#verification_restamp`（旧留证 status/note 全文存档 + 新旧镜像 sha）与 `data/audit/phase20R_zengzi_merge_manifest.json#verification_restamp`；QA 证据包 `docs/qa/phase20R_zengzi_qa_evidence.txt` §5 为原始逐条 diff。
- 回归复跑：
  - `verify_hzx_phase20R.py` **31 PASS / 0 FAIL**；`verify_hzx_landing.py` **26 PASS / 0 FAIL**（含 manifest 镜像 sha 一致性 F5/G2 侧）。
  - `verify_hzx_merge_phase20R.py` **61 PASS / 5 FAIL**（A10/A11 三面同体已修复；余 A17/A17b、E1/E3/E4）。
  - `verify_zengzi_qa_espinosa.py` **78 PASS / 3 FAIL**（B1 四面同体已修复；余 0.4、G2、H1）。
- 余 8 条断言属**口径过时项**（不可与新口径兼得，逐条见 evidence `zx_regression_fix.obsolete_assertions`）：A17/A17b（Phase20R 定稿枚举）、E1/E3/E4（3152 纯追加台账，被班固批次 +10 与改名合法改变）、0.4（合并快照足迹含 verification）、G2（硬编码落地态镜像 sha 前缀）、H1（依赖上述 merge 脚本全绿）。建议编排按四态口径改版上述脚本（本卡不擅自改他卡验收脚本的断言本体）。

## 6. 站点链条重建与计数锚点

命令序列（全 `exit 0`，输出存档 `evidence/chain_*.txt`）：

| 步骤 | 命令 | 结果 |
|---|---|---|
| 1 | `python3 tools/export_static_site.py` | 完成 OK；`modes_deduped=3152`、`mode_by_figure_shards=306`、`modes_raw=3162`、figures=1057（断言通过） |
| 2 | `python3 tools/gen_web_site_counts.py` | `web/src/generated/siteCounts.ts`：3092 条模式 × 306 位人物；四态 932/1786/34/340 |
| 3 | `python3 tools/apply_site_counts.py` | dist（本地陈旧构建物，CI 重建）与 docs 门面 6 页零违规 |
| 4 | `python3 tools/build_daily_index.py` | 3092 条 / 306 位 / 306 分片 |
| 5 | `python3 tools/pages_preflight.py --stage data` | 全部断言通过（figures=1057 modes=3152 published=3092 隔离命中=0） |

计数锚点更新（两工具同步，`scripts/../evidence/anchor_update.json`）：

| 锚点 | 旧 | 新 | 依据 |
|---|---|---|---|
| `EXPECT_MODES` | 3132 | **3152** | 班固 +10 入库；董仲舒 M01~M10 归一后不再落入「空模式码丢弃面」（该面 20 → 10 条壳），去重口径净 +20 |
| `EXPECT_BY_FIGURE` | 304 | **306** | 曾子 +1、班固 +1 分片 |
| `EXPECT_FIGURES` | 1057 | 1057（不变） | |

公开可见变化：班昭/约翰·杜威显示名纠正、班固 10 条模式上线（含其分片）、董仲舒 10 条模式由「空码丢弃」恢复为可发布（页面模式号变为 `M-DZS-001~010`）、曾子 10 条模式 verification 标注由定稿留证改为四态口径（`verified/pending`）——站点可信度四态计数随之变化（见 §3）。

## 7. 两仓同步与 parity

- 工具/口径：`tools/check_repo_parity.py`（构建图文件逐字节 sha256；含未跟踪但不被 .gitignore 的文件；排除产物/备份/非构建图项，排除带理由）。
- 同步前：**69 差异**（CONTENT_DIFF 16 / 仅工作仓 50 / 仅发布仓 3）。
- 镜像动作（`scripts/mirror_to_publish.py`，日志 `evidence/mirror_log.json`）：
  - 复制 **51** 路径（工作仓 tracked 侧）：本卡 18 件 + 曾子批次已提交产物（`data/audit/phase20R_zengzi_*`、`data/figures|individuals` H-ZX-001 三镜像与伴随包、`data/backup_phase20R_*`、`data/figures/_duplicates/*`、`docs/qa|research` 曾子报告与证据、`tools/*` 锚点、`web/src/generated/siteCounts.ts`）；
  - 删除 **3** 路径（发布仓侧旧码清档，git 识别为 rename 至隔离区）：`docs/figures/H-ZS-001.md`、`data/individuals/H-ZS-001.json`、`data/individuals/H-ZS-001_modes.json`；
  - 跳过 **15** 路径：并行卡未跟踪在制产物（见 §9）。
- 同步后：**15 差异**，全部为「仅工作仓 · 未跟踪（未 git add）」同一类，且不为本卡路径；**已跟踪面 0 差异（CONTENT_DIFF 0 / MISSING_IN_WORKSPACE 0）**。
- 发布仓提交：`6fea2e7`（52 路径）；推送回执：`3f68f62..6fea2e7  main -> main`，`git rev-list --count origin/main..HEAD = 0`。
- 镜像提交内含并行卡「已跟踪但在制」最新内容（`docs/figures/H-ZX-001.md` 归档卡编辑、`verify_hzx_*.py` 白名单落位），已在提交信息中列明；其归属卡提交后若内容再生变化，由下一次镜像收敛。

## 8. 门禁与核验（命令 + 退出码）

| 检查 | 命令 | 结果 |
|---|---|---|
| 可信度门禁 | `python3 tools/credibility_gate.py --hard-fail --data-path data/modes_data.json` | **exit 0**（存量 524 条冻结基线；新增硬失败 0；D5 存量 1 条 M-NEW-007 与基线同） |
| findings 门禁 | `python3 tools/verify_findings.py --hard-fail --data-path data/modes_data.json` | **exit 0**（无新增硬失败；1 条非阻断警告：M-ASM-* 双重收割，存量） |
| 出处链接门禁 | `python3 tools/verify_source_links.py --hard-fail` | **exit 0**（无新增坏链） |
| verification 零漂移 | `python3 tools/apply_verification_status.py --check` | **exit 0** |
| 本卡独立核验 | `python3 verify_greyzone_phase21r4.py` | **38 PASS / 0 FAIL / 6 INFO**（exit 0） |
| 两仓 parity | `python3 tools/check_repo_parity.py` | 已跟踪面 0 差异（另 15 条为他卡未跟踪在制产物，见 §9） |
| 站点链条 | §6 五步 | 全 exit 0 |

## 9. 残留清单（逐条：内容 / 归属 / 建议）

1. **parity 余 15 条未跟踪在制产物**（非本卡引入，本卡不镜像、不提交）：
   - `docs/scratch/legacy20_rev6_samples/**`（13 件） + `docs/research/legacy20_rev6_assessment.md`：归属 **t_a060cd41（albo，已完成）**；其卡面声明「评估产物只新增 docs/scratch」「样例仅存 scratch，不入库」，故不镜像；建议编排裁定：由该卡补提交，或按「scratch 不入库」口径把 `docs/scratch/` 纳入 .gitignore（否则将持续计入 parity 单侧在制）。
   - `docs/research/phase20R_zengzi_archive_report.md`：归属 **t_6c7e070a（pigafetta，在途）**；随其提交/镜像自然消解。
2. **`modes_data.json` 的 `total` 字段** = 2948，与 `len(modes)=3162` 漂移 −214（Phase21-R 的 −194 + 本批 −20）；本卡按「纯追加零改写」零写入，建议编排一次性裁定（改口径 or 保留并冻结说明）。
3. **董仲舒 legacy 档案层旧号**：`data/figures/H-DZS-001_modes.json`、`data/individuals/H-DZS-001_modes.json`（`id`/`code` = `M01~M10`、`H-DZS-M01~`）与 `docs/figures/H-DZS-001.md` 的「M01-M10」叙述；属 **legacy 档案层编号**（14 个旧号段中 9 个跨人物重码），归 `t_a060cd41` 的 legacy20 复刻评估范围；本卡只归一主库与主库引用面（code_maps/scenarios），档案层未动以保持层间口径一致。
4. **班固恢复条目 `_en` 字段含中文 3 处**（`M-BG-003.process_en`「文献」、`M-BG-010.process_en`「文献」、`M-BG-010.modern_applications_en`「论证」）：源档逐字继承，为保「零捏造」未改写；如按「现役字段零混排」口径处理，建议连同源档（individuals 正本）与三分面同步的一次小型编码归一。
5. **曾子批次三脚本 8 条断言的过时口径**（§5）：A17/A17b、E1/E3/E4、0.4、G2、H1；建议编排按四态口径改版或明确废止，避免后续复核误判。

## 10. 复现顺序（可复跑）

```
cd /opt/data/workspace/Protreptic
python3 verify_greyzone_phase21r4.py                     # 本卡独立核验（38/0/6）
python3 tools/apply_verification_status.py --check      # G3 零漂移
python3 tools/credibility_gate.py --hard-fail --data-path data/modes_data.json
python3 tools/verify_findings.py --hard-fail --data-path data/modes_data.json
python3 tools/verify_source_links.py --hard-fail
python3 tools/export_static_site.py && python3 tools/gen_web_site_counts.py && \
python3 tools/apply_site_counts.py && python3 tools/build_daily_index.py && \
python3 tools/pages_preflight.py --stage data
python3 tools/check_repo_parity.py                      # 已跟踪面 0 差异
# 数据落地/引用面/镜像/锚点脚本与日志：
#   /opt/data/kanban/boards/protreptic/workspaces/t_ea3a32e5/{scripts,evidence,backup}/
# 上游回归：
python3 verify_hzx_phase20R.py && python3 verify_hzx_landing.py
python3 verify_hzx_merge_phase20R.py ; python3 verify_zengzi_qa_espinosa.py   # 余项见 §5/§9
```
