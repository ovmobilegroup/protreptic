# [Phase20R 曾子补做] 残留清单（H-ZS* / H-ZX* / M-ZS* / M-ZX* 全量定性）

- 研究卡：**t_6c92966b**（serrano）· 落地卡：**t_4a9c2c2e**（elcano）· 生成日期：2026-09-22
- 人物：曾子（**H-ZX-001**）· 定稿模式号：**M-ZX-001 ~ M-ZX-010**（旧号 M230-M239 作废）
- 机读版：`data/audit/phase20R_zengzi_residual_inventory.json`（31 项）；原始 grep 扫描：`data/audit/phase20R_zengzi_residual_scan.json`（全仓 476 命中文件原始记录）
- 扫描口径：全仓 `grep -rIlE 'H-ZS-001|H-ZX-001|H-ZX-00[0-9]|H-ZS-00[0-9]|H-ZZ-166|H-ZZ-222|M-ZS-|M-ZX-'`，再逐件定性（站点构建产物与备份/快照按类归并）

## 0. 命名空间结论

| 检查项 | 结果 |
|--------|------|
| `M-ZX-*` | 全库 **0 命中**（仅 phase21r 审计留有历史结论『无 M-ZX-*、无曾子条目』）→ 本卡定稿启用 M-ZX-001~010，**零冲突** |
| `M-ZS-*` | 全库 **0 命中** |
| `M230-M239`（旧号） | 仅曾子侧文件（模式档/研究旧稿/文档 md/伴随包）与历史备份引用；**无他人与主库条目占用** → 可安全作废/重命名 |
| `H-ZS-00x` | 曾子旧号（H-ZS-001）与**朱升研究（H-ZS-001~004，release/zhusheng-jiuzi-sance）编号冲突** → 曾子侧一律不得再用 |
| `H-ZZ-166 / H-ZZ-222` | 曾子旧数字码（与张载 H-ZZ-001 同前缀不同键号），仍存于 code_maps 中英两表与 web 数据层 |
| `H-ZX-001`（曾被误用为**朱熹**代号） | 历史误码链已定位：Phase21 已改 H-ZHX-001；**吕祖谦档与彼得大帝档仍有可疑残留**（见 §3） |

## 1. 逐件清单（31 项）

| # | 路径 | 类别 | 定性 | 处置建议 | 负责 |
|---|------|------|------|----------|------|
| 1 | `data/figures/H-ZX-001.json` | canonical-figure | 曾子 v6 人物档正本 | 本卡已更新：M-ZX-001~010 定稿 + 引文修正 + 归属标注 + phase20R 溯源块 | serrano（本卡完成） |
| 2 | `data/figures/H-ZX-001_modes.json` | companion-modes-package | 曾子伴随模式包（core_modes 旧为 [230..239]） | 本卡已更新 ID（core_modes/mode_evidence/mode_id_mapping）；v6 schema 对齐交落地卡 | serrano（ID）+elcano（对齐） |
| 3 | `docs/figures/H-ZX-001.md` | legacy-mode-doc | 第3代变体：10 条中 M232×2 / M236×2 重复；含『与孔子、孟子并称曾孟』等不可溯源表述；『10个专属思维模式（M234-M239）』计数错误；与 v6 定稿不一致 | 待重写为定稿或归档（不得作为数据源） | elcano / 另卡 |
| 4 | `docs/figures/H-ZX-001.md.bak_zengzi_fix` | backup | 旧 md 内容快照备份 | 建议清理（如需留证可保留） | elcano |
| 5 | `docs/research/phase20_zengzi_research.md` | legacy-research-draft | 旧研究稿 v1.0（2026-09-02）：含旧号 M230-M239、伪造引文（M238）与误引（M239） | 已由 docs/research/phase20_zengzi_research_final.md 取代（旧稿保留只读备查） | serrano（本卡） |
| 6 | `H-ZX-001.json` | stale-root-copy | 工作仓根目录旧版副本：figure_code=『春秋』（非规范）、无 figure_name | 归档/删除（取值键已由 data/figures 版覆盖） | elcano |
| 7 | `H-ZX-001_modes.json` | stale-root-copy | 根目录旧版伴随包副本 | 归档/删除 | elcano |
| 8 | `data/individuals/H-ZS-001.json` | gen-f-residual | Gen F 残留：8 模式 M311-M318；系统性错字（儒→浙、孝→效、恕→念）；生卒年损坏『前505-57617935年』；figure_code 缺失 | 废弃/归档（H-ZS-00x 与朱升研究 H-ZS-001~004 编号冲突，禁止回收编号） | elcano |
| 9 | `data/individuals/H-ZS-001_modes.json` | gen-f-residual | Gen F 模式清单（M311-M318）；M311-M318 已为顾炎武 H-GYW-001 占用（phase21R restore） | 废弃（不得复用 M311-M318 于曾子） | elcano |
| 10 | `data/figures/_duplicates/H-ZS-001.json` | quarantined-duplicate | Phase46 已隔离副本（sha256 697922d0…，全部取值键由 H-ZX-001/春秋 覆盖） | 保留为隔离证据；不得回迁主目录 | elcano |
| 11 | `docs/figures/H-ZS-001.md` | gen-f-residual | Gen F 文档（M311-M318，含『曾子传子思』等旧表述） | 归档/删除 | elcano |
| 12 | `data/figure_names.json` | key-registry | 键面：H-ZX-001/H-ZX-001_modes/H-ZX-001_MODES 为现役键（后两者＝伴随包键＋大小写变体，与 H-MZ-001/H-WC-001/H-DYC-001 等既有成对约定一致）；H-ZS-001:『曾子』为废弃旧键 | 保留 H-ZX-001* 三键；H-ZS-001 键删除或改注（避免工具继续解析为曾子主键，并避让朱升 H-ZS-001~004） | elcano |
| 13 | `web/public/data/figures/H-ZZ-166.json ; web/public/data/figures/H-ZZ-222.json ; web/dist 同件` | legacy-web-data | 旧数字码 H-ZZ-166/H-ZZ-222 的 web 数据（含『待完善』占位与工程化改写文本，modes 字段为数字序号[9,36,37,28,35]） | 建议下架或重写映射到 H-ZX-001（另卡：web 层映射与数字码清理） | 另卡（web） |
| 14 | `tools/json/code_maps.json` | code-registry | H-ZX-001 已注册（10 模式中文名清单，与定稿模式名逐一对应 ✓）；另有遗留别名 H-ZZ-166/H-ZZ-222→曾子（数字序列遗留，与 H-ZZ-001 张载不同键号，不冲突） | 保留（模式名未变，零改动）；H-ZZ-166/222 标注 deprecated | elcano/记录 |
| 15 | `tools/code_maps_en.json` | code-registry | H-ZZ-166/222 遗留别名同 #14 | 同上（记录） | 记录 |
| 16 | `modes_data.json` | main-library | 含 H-ZX-001 人物块（内嵌 10 模式，旧号 M230-M239，行 ~5502-5900） | 由落地卡 t_4a9c2c2e 按定稿 rebase 到 M-ZX-001~010（本卡不改主库） | elcano |
| 17 | `scenario_tags.json ; tools/json/scenario_tags.json` | scenario-tags | H-ZX-001 键存在，内容为模式名清单（无 M 编号） | 保留（模式名未变，零改动）；如需补 mode_ids 交落地卡 | elcano |
| 18 | `scenarios_zh_add.json ; scenarios_zh_new.json ; scenarios_en_add.json` | staging-residual | HS-ZS-001/ES-ZS-001 待入库条目（figure_code=H-ZS-001，modes=M311-M318）；scenarios_zh.json/en.json 中无 HS-ZS-001（未入库） | 废弃或改码为 H-ZX-001 + M-ZX-001~010 后重提（elcano/另卡） | elcano |
| 19 | `data/individuals/H-LJY-001_modes.json:478` | external-crossref-defect | 吕祖谦档 cross_references 残留『H-ZX-001 (朱熹·同时代对峙)』——H-ZX-001 曾被误用作朱熹代号，canonical 应为 H-ZHX-001 | 另立卡修复（吕祖谦档交叉引用；人工核读后改码） | 另卡 |
| 20 | `data/figures/H-PGR-001.json (cross_references)` | external-crossref-unclear | cross_references 含『H-ZX-001』，指向曾子还是误码朱熹待核 | 下游核对后改码或保留 | 另卡 |
| 21 | `docs/figures/H-ZHX-001.md ; docs/figures/H-LJY-001.md ; docs/figures/H-WYM-001.md` | qa-archive | 记录 H-ZX-001 曾为朱熹误码→改 H-ZHX-001 的修复历史（Phase21 入库 QA） | 只读保留 | — |
| 22 | `tools/update_zengzi_db.py ; tools/verify_zengzi.py ; verify_zengzi.py ; verify_zengzi_data.py ; check_zengzi.py` | one-shot-scripts | Phase20 旧号时代一次性脚本（引用根目录 H-ZX-001_modes.json 与旧号） | 归档（不要重跑：会把旧号写回） | elcano |
| 23 | `release/zhusheng-jiuzi-sance/**` | id-collision-avoid | 朱升九字三策研究占用 H-ZS-001~004（非曾子） | 禁止改动/回收编号；曾子侧一律不得再用 H-ZS-* | （避让项） |
| 24 | `data/figures/H-ZSS-001.json ; docs/figures/H-ZSS-001.json` | unrelated | 朱舜水（H-ZSS-001），前缀相似 | 勿动 | — |
| 25 | `data/figures/H-ZXC-001* ; web/public/data/figures/H-ZXC-*.json ; web H-ZX-<num>.json` | unrelated | 章学诚（H-ZXC）与 web 数字键命名空间（H-ZX-62/172/252…） | 勿动 | — |
| 26 | `data/audit/**（figure_field_defects.json 等 + 本卡新增 phase20R_zengzi_residual_scan.json / inventory.json）` | audit-archive | 字段审计/修复清单档案（提及 H-ZS-001/H-ZX-001 的历史记录） | 只读保留；本卡新增两份扫描/清单文件 | serrano（新增） |
| 27 | `backups_merge_*/** ; code_maps.json.backup_qa_zhx_20260908 ; data/*.bak.fix-* ; modes_data.json.backup_homer_* ; backups/**` | historical-backup | 历史备份/快照（含旧号 M230-M239 与 H-ZX-001 块） | 只读保留（勿作为数据源回写） | — |
| 28 | `docs/qa/phase46_figure_fields.md ; docs/qa/phase21R_restore_report.md ; docs/research/phase20_chenghao_orphan_cleanup_evidence.json` | qa-archive | QA 结论档案（H-ZS-001 归档决策、『无 M-ZX-*、无曾子条目』历史结论等） | 只读保留 | — |
| 29 | `api/data/scenarios_en.json ; main_data.json ; tools/json/scenarios_zh.json/en.json ; docs_site/** ; release/v2.0.0/**` | snapshot-publish | 发布/快照件，含 H-ZZ-166/H-ZZ-222 旧码 | 不手改（发布快照）；如需统一另起发布卡 | — |
| 30 | `site_docs/**（含 figures/H-ZS-001/index.html、figures/H-ZX-001/index.html、search_index.json、sitemap.xml）` | site-build-output | mkdocs 构建产物，含 H-ZS-001/H-ZX-001 旧内容快照 | 不手改（重新构建再生） | — |
| 31 | `M-ZS-* / M-ZX-*（全库扫描）` | namespace-scan | M-ZS-* 0 命中；M-ZX-* 0 命中（仅 phase21r 审计记录历史结论『无 M-ZX-*、无曾子条目（0 条）』） | 无需处理；本卡定稿启用 M-ZX-001~010（renumber 后与全库零冲突） | serrano（本卡） |

## 2. 高优先处置项（交落地卡 elcano）

1. **Gen F 三件**（`data/individuals/H-ZS-001.json`、`data/individuals/H-ZS-001_modes.json`、`docs/figures/H-ZS-001.md`）：系统性错字（儒→浙、孝→效、恕→念）、生卒年损坏（『前505-57617935年』）、M311-M318 与顾炎武冲突 → **废弃/归档**。
2. **旧文档** `docs/figures/H-ZX-001.md`：10 条中 **M232×2、M236×2 重复**，含『与孔子、孟子并称曾孟』『10个专属思维模式（M234-M239）』等不可溯源表述 → **重写为定稿或归档**；`docs/figures/H-ZX-001.md.bak_zengzi_fix` 建议清理。
3. **根目录旧副本** `./H-ZX-001.json`（figure_code=『春秋』非规范）、`./H-ZX-001_modes.json` → 归档/删除。
4. **键面** `data/figure_names.json`：`H-ZS-001:『曾子』` → 删除或改注；`H-ZX-001_modes` / `H-ZX-001_MODES` 定性＝伴随包键＋大小写变体（与 H-MZ-001 / H-WC-001 / H-DYC-001 等既有成对约定一致）→ **保留**。
5. **web 旧码** `web/public/data/figures/H-ZZ-166.json`、`H-ZZ-222.json`（+`web/dist` 同件）：旧数字码数据（含『待完善』占位与工程化改写文本、modes 为数字序号）→ 下架或重映射到 H-ZX-001（另卡）。
6. **场景 staging** `scenarios_zh_add.json` / `scenarios_zh_new.json` / `scenarios_en_add.json`：HS-ZS-001/ES-ZS-001（H-ZS-001 + M311-M318）**未入库**（`scenarios_zh.json` 无此条）→ 废弃或改码后重提。
7. **一次性脚本** `tools/update_zengzi_db.py`、`tools/verify_zengzi.py`、`verify_zengzi.py`、`verify_zengzi_data.py`、`check_zengzi.py`：引用根目录旧文件与旧号 → 归档（勿重跑，会把旧号写回）。

## 3. 外部文件误码残留（另卡修复，本卡只定性）

- `data/individuals/H-LJY-001_modes.json:478`：吕祖谦档写『H-ZX-001 (朱熹·同时代对峙)』——H-ZX-001 曾被误用作朱熹代号，canonical 应为 **H-ZHX-001**。
- `data/figures/H-PGR-001.json`（cross_references 列表）含 `H-ZX-001`：指向曾子或误码朱熹**待核**。

## 4. 避让项（严禁改动、严禁回收编号）

- `release/zhusheng-jiuzi-sance/**`：朱升九字三策研究占用 **H-ZS-001~004**（与曾子无关）。
- `data/figures/H-ZSS-001.json`、`docs/figures/H-ZSS-001.json`：**朱舜水**（H-ZSS-001）——前缀相似，易误伤，勿动。
- `data/figures/H-ZXC-001*`（章学诚 H-ZXC）与 `web/**/H-ZXC-*.json`、`web/**/H-ZX-<数字>.json`（web 数字键命名空间）——与曾子无关，勿动。

## 5. 只读保留类

- QA / 审计档案：`docs/qa/phase46_figure_fields.md`、`docs/qa/phase21R_restore_report.md`、`docs/research/phase20_chenghao_orphan_cleanup_evidence.json`、`data/audit/figure_field_defects*.json`、`data/audit/figure_field_fix_manifest.json`、`data/audit/lifespan_backfill.json`、`data/audit/phase21r_audit.json`。
- 历史备份 / 快照：`backups_merge_H-DZ-001_*/`、`backups_merge_H-SJM-001_*/`、`code_maps.json.backup_qa_zhx_20260908`、`data/code_maps.json.bak.fix-20260906_225525`、`data/modes_data.json.bak.fix-20260906_225525`、`modes_data.json.backup_homer_*`。
- 发布 / 站点产物：`api/data/scenarios_en.json`、`main_data.json`、`tools/json/scenarios_*.json`、`docs_site/**`、`release/v2.0.0/**`、`site_docs/**`（含 `site_docs/figures/H-ZS-001/index.html`、`site_docs/figures/H-ZX-001/index.html`、`site_docs/search/search_index.json`）——**不手改**，随重建/再发布自然更新。
- 误码修复历史记录：`docs/figures/H-ZHX-001.md:157`、`docs/figures/H-LJY-001.md`、`docs/figures/H-WYM-001.md`。

## 6. 本卡已处置（无需下游重复）

- `data/figures/H-ZX-001.json`：M-ZX-001~010 定稿 + 引文修正（M238/M239）+ 出处补全（M236）+ wiki_id 修正（Q562→Q1207671）+ 6 条归属标注 + phase20R 溯源块。
- `data/figures/H-ZX-001_modes.json`：core_modes / mode_evidence / mode_id_mapping 全面换新号。
- 备份：`data/backup_phase20R_H-ZX-001_20260922_2021/`（4 件改前快照，含 sha 可考）。

---
*Phase20R 补做·研究卡 t_6c92966b（serrano）· 2026-09-22 · 与机读清单一同交付*
