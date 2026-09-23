# 归档说明：发布仓根 2026-09-17 期旧副本（Phase21-R7 旁项清理）

- 归档卡：t_151265db（Phase21-R7 旁项，2026-09-23）
- 归档缘由：R5 卡（t_36c4079c）§8.2 留档「发布仓根目录遗留副本（2026-09-17 期）
  ：modes_data.json 492499B、code_maps.json、scenario_tags.json、scenarios_zh/en.json」。
  其中 modes_data.json（492499B）与工作仓同名旧档逐字节同体，随
  data/backup_root_homer_modes_data_20260923/ 归档；其余四件（本目录）本卡一并取证处置。
- 逐件指纹（发布仓根原件；全部来自提交 782a1ad，2026-09-17 20:48:30 初始入库，此后未再更新）：
  1) code_maps.json       size=52537 B  sha256=fcb02802470b41f9dd5040caa76f9d6d8178eb61909a209f04993e69bb488358
     —— 与工作仓根 code_maps.json.backup_homer_20260922_070407 逐字节同体（预 homer 版快照）
  2) scenario_tags.json   size=31079 B  sha256=b0e9032dfd1273d239178d209921702a9e2068e08d8d8689d5148408129b55c7
     —— 与工作仓根 scenario_tags.json 逐字节同体
  3) scenarios_en.json    size=88367 B  sha256=686dfaf135497c1c26ea1a6bb8b5b76d890eea214734fd4d113f0689ba60a6ad
     —— 与工作仓根 scenarios_en.json 逐字节同体
  4) scenarios_zh.json    size=87475 B  sha256=9b3143b446f6dea4b1e8be52df099f64b776e8ec65d5b4f7638db7c3af9c58e7
     —— 与工作仓根 scenarios_zh.json 逐字节同体
- 读取面核验（2026-09-23，本卡）：
  * 发布仓现役构建链（pages.yml 全步骤、quality-gate）读 data/** 与 tools/**，根副本不进构建图；
  * check_repo_parity.py 明确将根目录遗留副本（modes_data.json、scenarios_zh/en.json、code_maps.json、
    scenario_tags.json 等）列为边界外角色（不参与 parity 差异判定）；
  * 全仓 grep（两仓）无现役读取方；唯一形式上的根相对读取例（scripts/validate_bg.py）实际 base='data'，读 data/**。
- 恢复方式（择一）：
  * 本目录副本：cp data/backup_root_publish_legacy_20260923/code_maps.json /opt/data/release/Protreptic-publish/code_maps.json（其余同法）
  * git 历史：git -C /opt/data/release/Protreptic-publish show <blob> > <原名>
    （blob：code_maps=448685a0c722e4687691601a112d525fe314b0f5 / scenario_tags=1dcce553f4194050e7617757e426591e7011223d /
     scenarios_en=e80460dfdd91ea0da4f458344f35d5db36879863 / scenarios_zh=7fb0721b82ae420b11fa6e9cdbe0e2b93b741f46）
- 注意：工作仓根同名件（scenarios_zh/en.json、scenario_tags.json、code_maps.json[+备份件]）不在本卡清单内、
  维持原地（详见 R7 报告 §范围外登记与建议）；不得以任一旧副本回写现役数据。
