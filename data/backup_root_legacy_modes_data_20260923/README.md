# 归档说明：根目录历史遗留 modes_data.json（Phase21-R5 微清理）

- **归档卡**：t_36c4079c（Phase21-R5 微清理，2026-09-23）
- **归档缘由**：phase21r3 灰区报告 §9 第 ④ 项 + phase20R 合并收尾残留清单 #16——
  根目录 modes_data.json 为早期阶段遗留副本（101 图块汇编，含 H-DZS-001 与 H-ZX-001 旧号块 M230~M239），
  无任何现役工具/CI 读取，属「残留」，从根移除并保留可恢复。
- **原始路径**：./modes_data.json（仓库根）
- **形态**：JSON 数组，101 个图块对象（code / figure_name_zh|en / era / thinking_modes ...）
- **文件指纹**：size=610302 B；sha256=34b734d2ce998684e2a8b89f97997ee28839aadb623c914a27b2a4e6584453fb
- **入库历史**：最后改写于提交 2371a585（2026-09-22，"mining(phase46): 同步 33 位缺档案人物到两仓 + 创建晏阳初 + parity 零差异"）；
  移除前 HEAD blob = 44b9675dc8eee7ee1b20499a9729016062efdebe
- **读取面核验（2026-09-23，R5 卡）**：
  * 现役工具链（tools/build_*、export_static_site、credibility_gate、apply_verification_status、build_audit_findings 及 pages / quality-gate 全部 CI 步骤）一律读取 data/modes_data.json，不读根副本；
  * pages.yml 触发路径为 data/modes_data.json，不含根副本路径；
  * 相对根路径引用该文件的仅为历史一次性脚本（merge_script.py / merge_workspace_json.py / fix_gulf_*.py / fix_qa_batch4.py 等，最后改动 2026-08-15，不在任何管线内）。
- **恢复方式（择一）**：
  * 本目录副本：cp data/backup_root_legacy_modes_data_20260923/modes_data.json ./modes_data.json
  * git 历史：git show 44b9675dc8eee7ee1b20499a9729016062efdebe > modes_data.json
- **注意**：历史脚本 fix_qa_batch4.py 等若再次运行会在根目录重建同名文件（属历史行为，勿运行）。
