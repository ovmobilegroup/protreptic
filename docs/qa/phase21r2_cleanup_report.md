# Phase21-R2 编码归一清理报告（卡 t_72e34e75）

日出前 · 全链可复核 · 主库零写入

## 0. 结论摘要

| # | 卡面事项 | 处置 | 主库改动 | 公开侧可见 |
|---|---|---|---|---|
| 1 | 班固 H-BG-001 / BAN 两代人物 | **事实修正**（非同一人）+ 登记对齐 | 零 | 登记层（figure_names） |
| 2 | 商羯罗 H-SJL-001 旧码档 | 清档（字节原件归档 `_duplicates`） | 零 | docs 页面撤下 1 张 |
| 3 | 董宇明 / 杜威 H-DY-001 覆盖链 | 改码 `H-DYM-001` + 恢复杜威镜像 | 零 | docs 页面内容归位 + 新增 1 张 |
| 4 | verification 漂移 73 条 | 逐条复核 + **留痕**（不写回） | 零 | 零 |
| 5 | 董仲舒 DZS 口径 | 咨询性建议（零动作） | 零 | 零 |

- **主库 `data/modes_data.json` 全卡零写入**：开工/收工 sha256 均为 `83be45b5bf63…`（24,200,321 B），独立核验脚本第 D 组断言。
- 全部"撤下/改名"动作均以**字节原件**进入 `data/figures/_duplicates/`（sha256 逐件登记，见证据包），无一处删除 —— 符合卡面硬性纪律"纯保守清理、不删数据本体"。
- 门禁 7 条全绿（命令与退出码见 §7）；两仓 `check_repo_parity.py` exit 0。
- 三例归一结论明确、活跃数据层零悬空（§2/§3/§4 各有独立断言）。
- 待船长决策 5 项（§9 灰区），其中 1 项（verification 归位）附带可直接执行的命令与影响预估。

## 1. 卡面与执行口径

卡面五项（E1 班固/BAN、E2 商羯罗 SJL、E3 董宇明/杜威、E4 verification 漂移、E5 董仲舒 DZS），验收条款：
三例归一结论明确且活跃数据层零悬空；verification 漂移逐条有处置或留痕；parity 0；线上可见变化清单（如有）。

执行口径（依据卡面 + 仓库既有先例）：
1. **先取证后动手**：任何改动前先做活跃层引用扫描、sha256 快照与"消费方定位"（`tools/export_static_site.py` / `figure_library.py` / `build_unified_index.py`）；
2. **能力边界内保守**：主库（`data/modes_data.json`）与 canonical 档案（`H-SHA-001`、`H-BG-001`、`H-BAN-001`、杜威 M-DY-001~010）零改动；
3. **旧码三件套**（`data/individuals/*` + `data/figures/*_modes.json` + `docs/figures/*.md`）撤下时改为**归档保留**（先例见 `docs/research/phase20_chenghao_orphan_cleanup_report.md`，本卡较其更保守：不删字节）；
4. **登记层修正**用最小 diff（`data/figure_names.json` 7 键）。

## 2. 商羯罗 H-SJL-001 旧码清档（E2）

现状：`H-SJL-001` 为 Phase 21 基础版旧编码；canonical 为 `H-SHA-001` / `SHA` / `Shankara`（同一人物商羯罗，8 世纪吠檀多）。旧码侧残留 4 件活跃文件 + 登记 3 键：

| 路径 | 字节 | 处置 |
|---|---|---|
| `data/individuals/H-SJL-001.json` | 42,523 | → `_duplicates/H-SJL-001_individuals.json` |
| `data/individuals/H-SJL-001_modes.json` | 36,271 | → `_duplicates/H-SJL-001_individuals_modes.json` |
| `data/figures/H-SJL-001_modes.json` | 36,991 | → `_duplicates/H-SJL-001_figures_modes.json` |
| `docs/figures/H-SJL-001.md` | 24,370 | → `_duplicates/H-SJL-001_archive_page.md` |
| `data/figure_names.json` 3 键 | — | 删除（`H-SJL-001` / `_modes` / `_MODES`） |

（`data/figures/_duplicates/H-SJL-001.json` 为 Phase46-R 已归档件，本次未动。）

方案对照：
- (a) **清档 + 字节归档**（采纳）：与先例一致，活跃层零悬空；内容零丢失（`_duplicates` 不在任何 `figures/*.json` glob 内，属仓库既定"安全归档"位）。
- (b) 内容迁移合并进 canonical：旧档为 Phase 21 基础版（9 节先例形态），与 canonical 差异大（`docs/figures/H-SJL-001.md` vs `H-SHA-001.md` 差异 688 行），逐字段合并属"改数据本体"，超出本卡。
- (c) 不动：与"活跃数据层零悬空"验收冲突。

证据（独立核验脚本 A 组 12 项断言全 PASS）：
- 活跃层键引用 = 0：`figure_names` / `code_maps.json` / `modes_data.json` 均无 `H-SJL-001`；`data/figures`、`data/individuals` 目录无 `H-SJL-001*` 文件；
- 四件归档 sha256 与撤下前逐一一致（`f46eff6f…` / `1aee3b80…` / `e1e226e5…` / `59412971…`）；
- canonical 未动：`H-SHA-001` / `SHA` / `Shankara` / `SHANKARA` 四键仍指"商羯罗"；
- 与 canonical 字段差异（仅登记，不裁剪）：`_individuals.json` 比 canonical 多 8 个字段（`core_thoughts`/`courtesy_name`/`famous_quote`/`influence`/`protreptic_mapping`/`pseudonym`/`representative_works`/`style_name`），两份 `*_modes.json` 的模式级字段与 canonical 完全同集。
- 剩余文本提及（非引用）：`data/figures/H-IBR-001.md` 与 `data/individuals/H-IBR-001.md` 各 1 处沿革注记（"按 H-ISN-001/H-SJL-001 九节先例生成"），保留；QA/报告层历史记录保留；`tools/` `web/` `api/` 零提及。

## 3. 董宇明 / 杜威 H-DY-001 覆盖链（E3）

现状（两个人物共用一码）：
- 主库：`M-DY-001~010`（10 条，figure_name=约翰·杜威），另有 10 条"董宇明"档内容（ids `M11~M20`，未入库）；
- 档案/登记/文档镜像：`data/figures/H-DY-001.json`（1,599 B）、`docs/figures/H-DY-001.md`（13,894 B）与 `data/figure_names.json["H-DY-001"]` 被 09-21 boards 镜像落地批次写成"董宇明"，覆盖了 09-20 杜威研究卡（t_* 杜威）的归档。

方案对照：
- (a) **改码董宇明 → `H-DYM-001` + 恢复杜威 H-DY-001 三镜像**（采纳）：两人物各自有 canonical 码，零合并、零删除；
- (b) 合并为一人：不成立（董宇明档领域为军事/谋略类 M11~M20，杜威为教育哲学 M-DY-001~010；figure 档案内容亦不同源）；
- (c) 只改 figure_names：留悬空（档案/文档仍指错人）。

执行（4 项）：
1. `git mv` 三件董宇明档 → `H-DYM-001`（`data/figures/H-DYM-001.json`、`data/individuals/H-DYM-001_modes.json`、`docs/figures/H-DYM-001.md`），并改码内字段 `code`/`figure_code` → `H-DYM-001`（文档 md 内 2 处编号引用同步）；
2. 恢复杜威镜像：`data/figures/H-DY-001.json` 与 `docs/figures/H-DY-001.md` 从 `1c13431e` 取回字节原件；
3. `figure_names`：`H-DY-001` → 约翰·杜威；新增 `H-DYM-001` → 董宇明；
4. 主库零改动（`H-DY-001` 组 10 条 `M-DY-001~010` 一直在库、未被覆盖）。

证据（独立核验脚本 B 组 10 项断言全 PASS）：
- 恢复件 sha256 = `cb64cdfb…`（与杜威研究卡交接元数据声明值一致）、镜像 `9e7b5e15…`（同卡声明值一致）—— 交叉复核通过；
- 恢复后 `figure_name=约翰·杜威`、`mode_ids = M-DY-001~010`、内嵌 10 条，与主库 `figure_code=H-DY-001` 组一一对应；
- 董宇明三件 `code` 全部为 `H-DYM-001`，主库无 `figure_code=H-DYM-001`（不重号）；
- 残留（见 §9-G2）：主库 10 条杜威记录的 `figure_name` 字段仍为"董宇明"（卡面"杜威 10 条数据不得受影响、不得删改"→ 未触碰，列灰区）。

## 4. 班固 / 班昭 BG/BAN 两代人物（E1）

**事实认定：卡题 E1 的前提（"同一人物两个编码"）不成立 —— `H-BG-001`（班固，东汉史学家，《汉书》作者）与 `BAN`/`H-BAN-001`（班昭，班固之妹，《汉书》八表与《天文志》续作者）是两位不同人物。**

证据：
- 两套档案各自内在一致：`H-BG-001` 三件（figure_name=班固，`data/individuals/H-BG-001_modes.json` 持有 `M-BG-001~010` 正文，`docs/figures/H-BG-001.md` 9,416 B）；`H-BAN-001` 三件（figure_name=班昭）。
- 主库实况：`figure_code=BAN` 组 10 条（`M-BAN-001~010`），组内 `figure_name` 全部为"班固"（**错标**，应为班昭）；无 `figure_code=H-BAN-001` 组；无 `M-BG-*` 条目。
- git 溯源：`M-BG-001` 字符串曾随 `f66bb2fd`（2026-09-07"Phase 21: 班固(H-BG-001)增量合并入主库"）出现，并在 `91832eb6`（2026-09-09 主库重写类提交）中被移除（父提交 5 处命中 → 该提交 0 处）。

执行（登记层对齐，主库零改动）：
- `figure_names`：`BAN` 班固 → **班昭**；新增 `H-BAN-001` → 班昭；`H-BG-001` → 班固（保留，正确）。
- 主库 `M-BAN-*` 与两套档案全部未动。

灰区（§9-G1/G4）：主库 10 条 `M-BAN-*` 的内嵌 `figure_name=班固`（改字段=动主库，未授权）；班固 10 条 `M-BG-*` 未随"旧世代恢复"批次回库（属另卡评估类）。

## 5. 董仲舒 DZS 口径（E5，咨询性）

现状：主库 `figure_code=H-DZS-001` 组 10 条在库，但 `mode_code`/`id` 为 `M01~M10`（无人物前缀旧编号），故以 id 前缀判归属的扫描（F1 类）读成 1/10；档案侧 5 件齐备（`data/figures/H-DZS-001.json` 2,548 B stub + `_modes` + individuals 两件 + `docs/figures/H-DZS-001.md` 16,304 B）。

建议（另卡执行，本卡零动作）：将 10 条 ids 归一为 `M-DZS-001~010`，或在登记层显式记录"旧编号例外"，消除 id 口径歧义。

## 6. verification 漂移 73 条（E4）

机制口径（`tools/apply_verification_status.py`，单一实现，S1>S2>S3>S4）：
`suspect`（findings D4/D5）> `verified`（出处至少一条引文解析到可达链接）> `unverifiable`（引文全部登记为不可链接）> `pending`（其余）。

逐条复核：以该工具的 `classify()` 对库内 3,142 条重算，与库存状态比对。**73 条不一致**，全部为 `verification.method = "phase20"` 的落地登记（计 80 条，另 7 条与规则一致）：

| 漂移 | 条数 | 判读 |
|---|---|---|
| `verified → pending` | 72 | 引文未在 `source_links.json` 建链（`pending` 是规则口径的诚实状态） |
| `verified → suspect` | 1 | `M-WYM-003` 命中 D4/D5（`findings.json`） |

按人物分组（8 位，均为 2026-09-21/22 落地批次）：`H-CHE-001` 10、`H-CHI-001` 10、`H-ZDY-001` 10、`H-LJY-001` 10、`H-WFZ-001` 10、`H-DZ-001` 10、`H-ZXC-001` 10、`H-WYM-001` 3。

处置：**留痕**（完整 73 行清单见证据包 `docs/research/phase21r2_cleanup_evidence.json` → `item4_verification_drift.rows`，逐条含 `mode_code` / `figure_code` / 登记状态 / 规则判定 / 判定依据 / 登记时间）。不写回的三条理由：
1. 这 73 条是**并行卡在制的登记**（今日落地批次所写，非本卡引入；报告 §7.1 已确认"非修复卡引入"），卡面允许"属他卡在制的登记留痕"；
2. 归位动作只有一种 canonical 方式（`--write`），它会**重签全库 3,142 条的 verification 块**（含 `checked_at`），并改变公开侧计数：`verified 988→916`、`pending 1711→1783`、`suspect 33→34`（公开口径），触发站点重建与页面计数变化 —— 属"公开侧影响"，应由船长授权（硬性纪律：任何线上可见变化先列清单）；
3. 本卡"纯保守清理"口径 + 该文件为多卡共享热文件（并发卡在写），非授权写入易生跨卡覆盖。

（若船长授权，修法一行：`python3 tools/apply_verification_status.py --write`，随后 `export_static_site.py` → `gen_web_site_counts.py` → `apply_site_counts.py` → 站点重建；回滚方式：`git checkout` 主库 + 重建。）

## 7. 门禁与两仓一致性（命令证据）

| 门 | 命令 | 结果 |
|---|---|---|
| 可信度 | `python3 tools/credibility_gate.py --hard-fail --data-path data/modes_data.json` | exit 0（D5 命中 1 条存量 `M-NEW-007`，与基线同；硬失败 0） |
| findings | `python3 tools/verify_findings.py --hard-fail --data-path data/modes_data.json` | exit 0（新增 0；1 条非阻断存量警告 `M-ASM-001~010` 重复收录） |
| 引证链接 | `python3 tools/verify_source_links.py --hard-fail` | exit 0（新增坏链 0） |
| 站点导出 | `python3 tools/export_static_site.py` | exit 0（figures=1057 / modes=3132 / 发布=3072 / 隔离=60 / by-figure=304 / 产物 1371 文件；体积与计数断言全绿） |
| 每日索引 | `python3 tools/build_daily_index.py` | exit 0（3,072 条 / 304 人物） |
| 发布预检 | `python3 tools/pages_preflight.py --stage data` | exit 0（全部断言通过） |
| 独立核验 | `python3 verify_phase21r2_cleanup.py` | 31 PASS / 0 FAIL（A 12 + B 10 + C 5 + D 1 + E 1 + 汇总） |
| 两仓一致 | `python3 tools/check_repo_parity.py` | 本卡 11 条改动路径两仓逐字节一致（sha256 复核）；差异条目 0 条属本卡路径。当前全量口径下另有并发卡 `t_6c92966b`（曾子补做）未跟踪产物 `docs/research/phase20_zengzi_research_final.md` 单侧在制（其卡 QA 交接 §10 已声明"随该卡提交/镜像自然消解"，非本卡引入） |

（首轮 `pages_preflight` 缺 `data/daily/*` 而报 1 条失败，按 `pages.yml` 既有顺序补跑 `build_daily_index.py` 后全绿 —— 属复现 CI 步骤顺序，非数据缺陷。）

## 8. 线上可见变化清单（本次）

1. **文档站撤下 1 张页**：`/figures/H-SJL-001/`（旧码研究档案）→ 随清档 404；canonical `/figures/H-SHA-001/` 不变。
2. **文档站内容归位 1 张页**：`/figures/H-DY-001/` 由"董宇明旧档"（13,894 B 版本）变为"约翰·杜威研究档案"（7,623 B）。
3. **文档站新增 1 张页**：`/figures/H-DYM-001/`（董宇明研究档案，与上一条同源换码）。
4. **web 数据产物零变化**：`figures.index.json` / `modes/index-*.json` / `modes/by-figure/*.json` 的条数与 sha256 与上一版完全一致（`docs/architecture/static_data_manifest.json` 仅 `generated_at` 变化，`products` 与 `assertions` 段逐字节相同）；`verification` 四态计数不变。
5. **登记层**（`data/figure_names.json`，7 键）：公开侧解析路径无变化（库内 `figure_code` 未动），仅纠错备用登记。

## 9. 灰区清单（报船长决策，本卡未动）

| # | 事项 | 影响面 | 建议 |
|---|---|---|---|
| G1 | 主库 10 条 `M-BAN-*` 的 `figure_name=班固`（应"班昭"） | 主库 10 字段；by-figure 分片与人物页显示 | 授权后单字段改名（10 处，可回滚） |
| G2 | 主库 10 条 `M-DY-001~010` 的 `figure_name=董宇明`（应"约翰·杜威"） | 同上 | 卡面"杜威 10 条不得删改"未授权，待裁决 |
| G3 | verification 73 条归位（§6） | 全库 3,142 条 verification 重签 + 公开计数 3 项 | 授权后单命令执行 + 站点重建 |
| G4 | 班固 `M-BG-001~010` 未入库（旧世代未恢复类） | 档案正文齐备（`data/individuals/H-BG-001_modes.json`） | 并入旧世代恢复评估（参照 t_a060cd41 口径）或另卡 |
| G5 | 董仲舒 10 条 ids 旧编号 `M01~M10` | id 前缀类扫描误读（1/10） | 另卡归一 `M-DZS-001~010` |

## 10. 提交与推送状态

- 工作仓（master，无远端同名分支，按既有流程不推送）：数据/文档提交 `dae8ac5e`（11 路径：figure_names 登记 7 键 + 董宇明改码 3 件 + 杜威恢复 2 件 + 报告/证据/核验脚本/CHANGELOG/生成本账），修订提交 `<WS_COMMIT2>`（本报告第 10 节与核验脚本 E 组口径）。
- 发布仓（`/opt/data/release/Protreptic-publish`，main）：镜像提交 `7106867`（14 路径：10 数据/文档 + 报告/证据/CHANGELOG/生成本账），已 push 至 `origin/main`（回执 `2617587..7106867  main -> main`），修订提交 `<PB_COMMIT2>` 同步更新；推送后核验 `git rev-list --count origin/main..HEAD` = 0、`git status --short` 无本卡残留（仅余并发 QA 卡报告一份）。
- 最终提交哈希与推送回执以 kanban 卡 `t_72e34e75` 完成交接（summary / metadata）为准。

## 11. 产物与复现

- 本报告：`docs/qa/phase21r2_cleanup_report.md`
- 证据包：`docs/research/phase21r2_cleanup_evidence.json`（快照 / 三例事实与引用扫描 / 73 行漂移表 / 门禁记录 / 归档件 sha256）
- 独立核验：`verify_phase21r2_cleanup.py`（31 断言，可重复执行）
- 工作副本（未入库）：`scratch/phase21r2/{apply_cleanup.py, mirror_publish.py, build_evidence.py, cleanup_snapshot.json}`
- 复现顺序：`apply_cleanup.py` → `build_evidence.py` → `verify_phase21r2_cleanup.py` → 门禁 6 条 → 镜像 + `check_repo_parity.py`

（报告完）
