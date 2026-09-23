# batch2 落盘产物索引（A组批2：CHB/FXT/DYC/KKQ/LWH）

卡 t_2d5112c6。产物结构与同族卡产物（batch1）对齐；本目录即「可直接并入主库」的产物包。

## 顶层

- combined_library_entries.json —— 50 条 v6 条目（schema_version + modes，与样例/批1 同构）汇总
- scenario_notes.json —— 5 件场景落盘汇总（FXT 归一 10+10；其余 4 件缺口登记）
- scenario_remap_needed.json —— FXT 旧场景码 C-FXT-001-001~010 到 C-FXT-001~010 / 001E~010E 归一登记
- gate_evidence.txt —— credibility gate（--hard-fail）实跑证据（退出码 0）

## 各件（H-<COD>-001/）

- modes_library_entries.json —— 10 条可直接并库条目（含 verification=pending、legacy_mode_id）
- id_mapping.tsv —— 旧号到新号（M<NNN> 到 M-<COD>-NNN）
- category_mapping.tsv —— 类目归一登记（status: mapped_by_sample_table / kept_as_is_待核；candidate_target 为未应用候选提案）
- merge_manifest.json —— 合并/回填/缺项逐字段决策记录（header_decisions、record_merge_log、missing_fields_per_mode）
- scenario_notes.json —— 本件场景统计与缺口
- figures/、individuals/ —— 本件落盘载荷副本（与 data/ 下同文件字节一致）
- scenarios_zh.json、scenarios_en.json —— 仅 FXT（搬迁 + 归一）
- legacy_rich_template_modes.json —— 仅 FXT（旧富模板版原样存档）
- dyc_root_copy_disposal.json —— 仅 DYC（游离副本归档登记）

## 相关

- 报告：docs/research/phase21r6_landing_batch2_report.md
- 证据：docs/research/phase21r6_landing_batch2_evidence.json
- 核验脚本：verify_legacy20_r6_batch2.py（仓库根，18/18 PASS）
- 备份：data/backup_r6_H-<COD>-001_20260923/；聚合登记 data/audit/phase21r6_batch2_backup_manifest.json
