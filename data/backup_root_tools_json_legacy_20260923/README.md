# 归档说明：tools/json 旧副本（聚合件三件 + 垃圾件两件，Phase21-R7 旁项清理）

- 归档卡：t_151265db（Phase21-R7 旁项，2026-09-23）
- 归档缘由：R5 卡（t_36c4079c）留档「未闭环旁项」之「tools/json 旧副本」；本卡逐件取证：
  tools/json 内**现役活输入仅 scenarios_zh.json / scenarios_en.json（build_figures_db.py find() 第一候选，
  两仓 parity 边界文件）**，其余同名聚合件经读取面普查确证为死副本，纳入本归档。
- 归档件（本体三件，均为早期世系、被现役同名件取代；现役读取面为零）：
  1) modes_data.json — 早期 M 模式登记表（{code,name,core_mode,new_mode} 体例，44,008 B；
     sha256=5145a11aa93f01dce03e25b97d5d53fffa977b0ef4847950c527034af7c8c97b；blob=036c24c579d776dbc7b36c6b1c5a2bebfef6d8c9；
     最后改写 dbdc1c74 2026-09-04「Phase 20: 张载(ZC-ZC-001)数据合并完成」）；
  2) main_data.json — Phase 17.7 南部非洲批次元数据件（12,655 B；
     sha256=7d080c5080e05837d8f17319d54eb1d9cd1d41010ff05df602027934a4b2254e；blob=19cd2e0cbe7a6ce98edf2f6eb53244a14d18040f；
     最后改写 1c033b9b 2026-09-03「Phase 20: H-HZX-001 增量合并」）；
  3) code_maps.json — 早期 CODE_MAP 世系注册表（200,401 B；sha256=bf1d624d7e65e9f24a6570ed9b358436145d492111b828ca923b46f2d444e2a8；
     blob=877a6d67af9d342548ec826857ba31c669d40763；最后改写 c2a5c487 2026-09-18「fix(ci): build_graph_data.py ...」）。
     取代关系：现役注册表 = data/code_maps.json（v6 schema，本卡零写入）/ tools/code_maps.json（CODE_MAP 世系现役面）。
- 附：垃圾件两件（shell 误操作产物，非数据、零引用；沿用 0f54627f「清理 shell 误操作垃圾路径」先例顺带归档）：
  * junk/stray_, print(.txt ← 原名 "tools/json/, print("（62 B，内容为一行 stray 命令文本；sha256=d563e31b...）
  * junk/stub_.json ← 原名 "tools/json/.json"（1,660 B，code 为空的占位残稿；sha256=a70f3ec1...）
- git blob（垃圾件）：adee05308f7947c5474e943899c81024451f8942 / 7c6a01096d698eb8e5ce9dca4d6e1c756c5617a9
- 读取面核验（2026-09-23，本卡）：
  * 本体三件的引用方均为一次性历史脚本或已归档脚本（_tmp_modes.py / _look_mm3.py / verify_tools_json.py /
    tools/_tmp_lookup.py / data/figures/_duplicates/zengzi_legacy_scripts/verify_zengzi_root.py / tools/json/check_15.py[同目录]）；
  * 现役构建链（build_figures_db / export_static_site / 门禁三件 / parity 边界）只读 tools/json/scenarios_*.json 与
    tools/[json/]scenario_tags.json（后者的首个候选为 tools/scenario_tags.json，现役在位）；
  * 两仓该三件逐字节同体（本卡不再单侧保留）；removed from tools/json/ 后目录保留活输入与历史旧稿类（另册登记，见 R7 报告 §tools/json 分区）。
- 恢复方式（择一）：
  * 本目录副本：cp data/backup_root_tools_json_legacy_20260923/modes_data.json tools/json/modes_data.json（main_data.json / code_maps.json 同法）
  * git 历史：git show <blob> > tools/json/<原名>
- 注意：不得作为数据源回填；同名现役数据一律读 data/**（modes_data.json / code_maps.json）。
