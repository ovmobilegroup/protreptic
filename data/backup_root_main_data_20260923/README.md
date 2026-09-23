# 归档说明：根目录 main_data.json（历史主档副本，Phase21-R7 旁项清理）

- 归档卡：t_151265db（Phase21-R7 旁项，2026-09-23）
- 归档缘由：R5 卡（t_36c4079c）留档「未闭环旁项」之一（原文：main_data.json（含 H-DZS-M 旧号））；
  本卡逐件取证后确证为死副本。
- 内容形态：对象（metadata.phase=Phase 18.12B 的大洋洲/太平洋批次合并主档体例；含 H-DZS-M01~M10 旧号 10 处）。
  它是早期「main_data.json 主档」世系的末代版本，后被 data/**（figures/individuals/modes_data.json/code_maps.json）
  分片体系取代并不再被任何现役步骤读取。
- 文件一：
  * 原始路径：./main_data.json（工作仓根）
  * 指纹：size=5181212 B；sha256=f4d0285eac4c72df3a80ec4b43efcf8e7b024c05e2c41e2f95dd4737cb391a39
  * git blob：758d6845acc9e4319dc8332ab315de7d771bf26a
  * 最后改写提交：c307178f（2026-09-04 06:58:41 Phase 20 Data Merge: H-HZX-001 rename modes->thinking_modes ...）
- 文件二（同批空档）：
  * 原始路径：./main_data.json.bak_hzx_merge_25696（工作仓根；0 字节空文件，H-HZX-001 合并脚本遗留占位）
  * 指纹：size=0；sha256=e3b0c442...b7852b855；git blob：e69de29bb2d1d6434b8b29ae775ad8c2e48c5391
- 读取面核验（2026-09-23，本卡）：
  * 现役构建/CI（pages.yml / quality-gate / ci-cd / check_repo_parity 边界）不读根 main_data.json；
  * 全仓 grep 读取方均为一次性历史脚本（根 check_*.py / _inspect_*.py / _verify_*.py、tools/update_templates_with_new_figures.py、
    tools/verify_main_data*.py 等，均不在任何管线内）；cli_tests 读的是 tools/json/main_data.json（另一件，见 tools_json 归档）。
  * parity 边界：根目录遗留副本不在边界内（check_repo_parity.py 文档口径）。
- 恢复方式（择一）：
  * 本目录副本：cp data/backup_root_main_data_20260923/main_data.json ./main_data.json
  * git 历史：git show 758d6845acc9e4319dc8332ab315de7d771bf26a > main_data.json
  * 空档：git show e69de29bb2d1d6434b8b29ae775ad8c2e48c5391 > main_data.json.bak_hzx_merge_25696
- 注意：不得回写为数据源；H-DZS-M* 旧号一律以 M-DZS-001~010 规范码为准。
