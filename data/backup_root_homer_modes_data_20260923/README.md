# 归档说明：根目录 modes_data.json 历史备份（Phase21-R7 旁项清理）

- 归档卡：t_151265db（Phase21-R7 旁项：根目录/发布仓旧档残留调查与处置，2026-09-23）
- 归档缘由：R5 卡（t_36c4079c）留档「未闭环旁项」之一；本卡逐件取证后确证为死副本
  （读取面普查 + 指纹比对 + parity 边界核对，详见 docs/qa/phase21r7_leftovers_report.md）。
- 内容形态：JSON 数组（早期图块汇编体例，含 H-DZS-001 块与旧号 H-DZS-M01~M10），
  为 R5 已归档的 legacy 根档（data/backup_root_legacy_modes_data_20260923/，610302B）之前一版本。
- 原件一（工作仓根）：
  * 原始路径：./modes_data.json.backup_homer_20260922_070524
  * 指纹：size=492499 B；sha256=675a7dc3b2cf773635f2d45da6dba715d9aa0214618507d6bc837c63201c9ced
  * git blob：3793899ba1e1356d64d49d148cdea7b75524107d
  * 最后改写提交：2371a585（2026-09-22 09:53:57 mining(phase46) 同步 33 位缺档案人物到两仓）
- 原件二（发布仓根，与原件一逐字节同体，本卡随此归档一并移除）：
  * 原始路径：modes_data.json（发布仓 /opt/data/release/Protreptic-publish 根）
  * git blob：同上（3793899b...）；入库提交：782a1ad（2026-09-17 20:48:30 发布仓初始入库）
- 读取面核验（2026-09-23，本卡）：现役构建/工具链一律读 data/modes_data.json（本卡零写入），
  不读两份根副本；build_figures_db.py find() 顺序、pages.yml 触发器、parity 边界
  （check_repo_parity.py：根目录遗留副本明确不在边界内）均不含根副本。全仓 grep 无现役读取方，
  引用仅见审计/报告记录（phase20R_zengzi_residual_scan.json / R5 报告与证据 / R7 报告）。
- 恢复方式（择一）：
  * 本目录副本：cp data/backup_root_homer_modes_data_20260923/modes_data.json.backup_homer_20260922_070524 ./modes_data.json.backup_homer_20260922_070524
  * 工作仓 git 历史：git show 3793899ba1e1356d64d49d148cdea7b75524107d > modes_data.json.backup_homer_20260922_070524
  * 发布仓 git 历史：git -C /opt/data/release/Protreptic-publish show 3793899ba1e1356d64d49d148cdea7b75524107d > modes_data.json
- 注意：作废旧号（H-DZS-M01~M10 等）仅存于本归档与既有审计语境，不得作为数据源回写；
  规范码 = M-DZS-001~010（R5 归一）。
