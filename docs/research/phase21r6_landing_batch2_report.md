# Phase21-R6 A组批2 复刻·转换落盘报告

卡：t_2d5112c6 ｜ 日期：2026-09-23 ｜ 执行：san-martin
依据：docs/research/legacy20_rev6_assessment.md（§2 子串修正 / §4.1 A组 / §5 样例 / §7 风险）；模板：docs/scratch/legacy20_rev6_samples/

## 0. 结论

5 件（H-CHB-001 陈伯达 / H-FXT-001 费孝通 / H-DYC-001 邓颖超 / H-KKQ-001 康克清 / H-LWH-001 李维汉）升级载荷已复刻落盘并提交：50 条 v6 条目（M-<COD>-001~010，5 件），三面一致、互引 98 条 0 悬空、编号全库 0 碰撞；落盘前 17 个原档字节备份（sha256 登记且与 git HEAD 逐件一致）；独立核验脚本 18/18 PASS；credibility gate（--hard-fail）0 失败；主库 modes_data.json 零写入。

## 1. 诚实纪律执行记录（只做转换、不做扩写）

- 仅执行：字段搬迁 + 编号重编 + 类目归一 + 互引重指 + v6 形态升级。未新增事实性内容。
- 50/50 条 verification.status = pending，evidence 均明写「引文与出处未独立核验」。
- 缺项按现状保真并如实登记（见 §5），不补写、不扩写。
- 未删除任何数据本体：原档字节备份 + FXT 富模板存档 + DYC 游离副本归档（见 §7）。

## 2. 逐件清单

| code | 人物 | 读取源档（落盘前） | 落盘文件 | 备份目录 |
|---|---|---|---|---|
| H-CHB-001 | 陈伯达 | figures/H-CHB-001.json、individuals/H-CHB-001.json、individuals/H-CHB-001_modes.json | data/figures/H-CHB-001.json + data/individuals/H-CHB-001.json + data/individuals/H-CHB-001_modes.json | data/backup_r6_H-CHB-001_20260923/ |
| H-FXT-001 | 费孝通 | figures/H-FXT-001.json、figures/H-FXT-001_modes.json（富模板）、individuals/H-FXT-001_modes.json | 同上三面 + data/figures/H-FXT-001_modes.json（另新建 data/individuals/H-FXT-001.json） | data/backup_r6_H-FXT-001_20260923/ |
| H-DYC-001 | 邓颖超 | figures/H-DYC-001.json、figures/H-DYC-001_modes.json、individuals/H-DYC-001.json、individuals/H-DYC-001_modes.json、data/H-DYC-001_modes.json（游离副本） | 同上三面 + data/figures/H-DYC-001_modes.json；游离副本移 _duplicates | data/backup_r6_H-DYC-001_20260923/（5 件） |
| H-KKQ-001 | 康克清 | figures/H-KKQ-001.json、individuals/H-KKQ-001.json、individuals/H-KKQ-001_modes.json | 三面 | data/backup_r6_H-KKQ-001_20260923/ |
| H-LWH-001 | 李维汉 | figures/H-LWH-001.json、individuals/H-LWH-001.json、individuals/H-LWH-001_modes.json | 三面 | data/backup_r6_H-LWH-001_20260923/ |

产物包（可直接并入主库）：docs/scratch/legacy20_rev6_landing/batch2/H-<COD>-001/（modes_library_entries.json、id_mapping.tsv、category_mapping.tsv、merge_manifest.json、scenario_notes.json、figures/、individuals/）。汇总：batch2/combined_library_entries.json。

## 3. 复刻动作 (1)~(7) 核对

(1) 编号重编 M-<COD>-001~010：完成。本批涉及的跨人物重码段 M321~M330（DYC 与 KKQ）、M341~M350（FXT 与 LWH）全部以 M-<COD>- 前缀消歧；重编后全库 0 碰撞（verify V2）。
(2) 类目归一：见 §4。
(3) 互引重指：related_modes 共 98 条引用全部块内可解析，0 悬空；另有旧号文本引用重指：CHB 10 处（protreptic_mapping 值）、FXT 20 处（scenarios_zh/en 的 mode_id）、KKQ 10 处（protreptic_mapping 值）、DYC 6 处（M-DYC-010 定义内联引用 M321~M330 段）。mode_ids_note 内的旧号按设计保留（映射说明用途，不参与重指）。
(4) 原地升级 v6 + 字节备份先行：完成（17 件，见 §7）。
(5) entries（50 条） + id_mapping.tsv（旧号到新号）：完成，与批1 同构（目录名 batch2/ 区分）。
(6) 核验状态统一 pending + evidence 短语：完成（verify V5：50/50）。
(7) 逐件独立核验脚本 + 证据：verify_legacy20_r6_batch2.py（18/18 PASS）+ docs/research/phase21r6_landing_batch2_evidence.json。

## 4. 类目归一结果（20 映射 / 30 原值保留）

- 样例表内命中并已应用：20 条（CHB 8、FXT 10、DYC 1、KKQ 1、LWH 0）。
- 原值保留（标记待核）：30 条 =
  - CHB 2 条 identity（文化批判思维、哲学思维）：样例即按原值保留，且为库内既有类目（非表外问题）；
  - 真表外 28 条（DYC 9、KKQ 9、LWH 10）。
- 28 条真表外的候选提案（未应用）已写入各件 batch2/H-<COD>-001/category_mapping.tsv 的 candidate_target 列（含置信度标注），供裁定后一键套用；状态列 kept_as_is_待核。
- 口径差异告警（需船长/归并卡裁定）：批1（前置卡产物）对表外类目采用 extended_candidate 直接映射（例：CY 方法论到方法论通用、认识论到认识论逻辑），未按「原值保留+标记待核」字面执行。本卡按卡面裁定的字面口径执行；若最终采批1口径，本卡 28 条按 candidate_target 批量应用即可对齐。

## 5. 缺项登记（按现状保真，不补写）

- FXT：10 条 modern_applications_zh/en 空（源档即空），记入 legacy_missing_fields。
- LWH：10 条 key_quote_zh/en、representative_cases_zh/en、modern_applications_zh/en 空（源档即空）。
- DYC/KKQ：header tags 为 null（源档无标签，本批不补）。
- 以上逐条登记于各件 merge_manifest.json 的 missing_fields_per_mode 与条目 legacy_missing_fields。

## 6. 场景（batch2）

- FXT：载荷内嵌 C-FXT-001-001~010（zh/en）已搬迁 + 归一为 C-FXT-001~010 / C-FXT-001E~010E，mode_code 指向新号；条目仅含标题（源即如此，未补描述）。见 batch2/H-FXT-001/scenarios_zh.json、scenarios_en.json、scenario_remap_needed.json。
- CHB/DYC/KKQ/LWH：载荷与库内均无场景条目，C-<COD>-001~010（E）双语缺口登记（batch2/scenario_notes.json），补写另立卡。
- 汇总文件：batch2/scenario_notes.json、batch2/scenario_remap_needed.json。

## 7. 数据保全

- 落盘前字节备份 17 件 / 266,663 B：data/backup_r6_H-<COD>-001_20260923/（每目录含 manifest.json；聚合 data/audit/phase21r6_batch2_backup_manifest.json）。verify V4 复核：sha256 与登记一致，且与 git HEAD 原档逐件一致（即备份确为落盘前原档）。
- FXT 富模板版（字段名非 v6）原样存档：batch2/H-FXT-001/legacy_rich_template_modes.json（样例未携带该版扩展字段，防丢；其旧号 M341~M350 对应见 id_mapping.tsv）。
- DYC 游离副本：data/H-DYC-001_modes.json 移入 data/figures/_duplicates/H-DYC-001_root_modes.json（字节归档、未删；与 figures/_modes 仅 2 处 definition_en 措辞差异，见 batch2/dyc_root_copy_disposal.json）。
- CHB/FXT 样例核对：记录级除 verification（FXT 另加 legacy_missing_fields）外与样例逐字段一致；header 层差异仅 tags（CHB 由 null 回填 15 项）、caveats（更新为落盘口径）、mode_ids_note（旧号到新号写法）、新增 verification 块与源档独有字段回填。

## 8. 独立核验与证据

- verify_legacy20_r6_batch2.py：18/18 PASS —— V1 三面一致 / V2 编号 + 全库 0 碰撞 / V3 互引 0 悬空 / V4 备份哈希 + HEAD 一致 / V5 pending + 短语 / V6 产物齐备 / V7 主库零写入判据。
- credibility gate：python3 tools/credibility_gate.py --data-path docs/scratch/legacy20_rev6_landing/batch2/combined_library_entries.json --hard-fail 退出码 0，新增硬失败 0（batch2/gate_evidence.txt）。
- 证据 json：docs/research/phase21r6_landing_batch2_evidence.json（各件 sha256、备份 sha256、gate 命令与退出码、pending 统计）。

## 9. header 回填与源档独有字段（不删数据本体）

- CHB 回填 10 个源档独有字段（civilization_sphere、cross_references、ethnicity、figure_name_en、intellectual_tradition、nationality、primary_language、protreptic_mapping、time_period_standardized、tags）；FXT 9 个（cross_references、figure_description 及 _en、figure_name_en、meta、related_figures、scenarios_zh/en）。
- 同名字段多版本取值不同：一律保留基版（图档侧较富者），异文全文存档于 merge_manifest.json 的 header_decisions（含 DYC 三版本 influence/historical_significance 等异文）。
- 字段命名备注：core_thoughts 到 unique_thinking 依样例模板归一（批1 保留了 core_thoughts 原名，属两批字段命名口径差异，供归并卡统一）。

## 10. 边界与并发

- 主库 modes_data.json 零写入（verify V7：50 个新号不在其中）；发布仓镜像未动（合并卡统一收敛）。
- 本卡提交路径仅限：data/{figures,individuals,audit,backup_r6_*}、data/figures/_duplicates/H-DYC-001_root_modes.json、docs/scratch/legacy20_rev6_landing/batch2/、docs/research/phase21r6_landing_batch2_*、verify_legacy20_r6_batch2.py。
- 并发在制（未触碰）：批1（elcano：CY/JX/SQL/WL/YSK）、他卡（H-DZS-001、曾子文件、data/modes_data.json 等）。报告内所有统计仅针对本卡 5 件。
- 全部「全库」结论以 verify 脚本实跑为准，且已排除本卡自身产物（避免自证碰撞的假阳性）。

## 11. 后续建议（另立卡）

(1) 类目口径裁定：本卡 28 条候选提案 + 与批1 口径统一（见 §4）。
(2) 场景双语补写：FXT/DYC/KKQ/LWH 共 4 件，10 条双语缺口（batch2/scenario_notes.json）。
(3) 引文落源核验：50 条全部 pending；含 DYC「妇女能顶半边天」归属勘误（评估报告 §7 风险 2）。
(4) 精修补齐：FXT modern_applications、LWH quotes/cases、DYC/KKQ tags（评估报告 §7 风险）。
(5) CHB 敏感人物表述按风险 8 口径复核（本卡已保留 caveat 与史料句式）。

## 12. 提交

- 首次提交：eb53a42f（95 路径入库：5 件载荷 + entries/映射/备份/证据/脚本）。
- 本小提交补记：V4 备份判据改为参照 manifest.pre_landing_commit（落盘前提交 d879eb9c，即 eb53a42f 的父提交），证据 json 同步补 pre_landing_commit 与 landing_commit_initial；核验脚本重跑 18/18 PASS。
