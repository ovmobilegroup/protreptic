# Phase21-R8 H-AZJ-345 清档补正 · 发布仓镜像＋push＋报告补全（卡 t_6acd458b）

- 执行卡：t_6acd458b（elcano）｜执行时段：2026-09-24 02:38–03:0x CST
- 工作仓：/opt/data/workspace/Protreptic（master；被镜像基线 8adbdabd／1de660cf）
- 发布仓：/opt/data/release/Protreptic-publish（main；镜像前 c32f669 → 镜像主体 35061ce）
- 上游：t_3669eb4a 收口缺项（发布仓未镜像/未提交/未 push、报告 md 缺失、.json 错标 publish_sha）；t_ff294775 验收异议 1/2/8；船长独立复核 2026-09-24 02:36–02:45
- 边界：仅镜像对齐＋报告补全；零新数据内容；不修改 modes_data.json；不碰他链在途路径（W4/W6/W5 文件镜像归各自链）；与在途验收卡 t_ff294775（只读）不冲突。一切断言附实测证据，禁止照抄卡面描述当结果。

## 0. 结论摘要

| # | 项 | 实测结果 |
|---|----|---------|
| 1 | 发布仓镜像主体 | commit 35061ce（60 件：M19／A40／D1；含变更集＋备份/归档入库＋构建面） |
| 2 | push | `c32f669..35061ce  main -> main`，rc=0；ls-remote == 本地 HEAD（35061ce0f39…） |
| 3 | 发布仓全量 AZJ 扫描（含 gitignored） | live **21 变 0**；合计命中 519 全部落豁免/站点构建类（§5） |
| 4 | 变更集 byte-exact | 60 路径：58 件逐字节一致（sha256 逐件见 §1）；2 件 docs_site/* 发布仓无对应路径（豁免，§1.3） |
| 5 | 构建面（gitignored 在盘） | web/public/data、web/dist、site_docs 全树与工作仓逐字节一致；figures 分片 1056／sitemap 1388／routes 1387／unified 1371 |
| 6 | 官方 parity 复跑 | CONTENT_DIFF **0**（两仓共同件 2266/2266 全等）；剩余单侧缺失 = 他链 6＋验收卡在途 2＋本报告 json 1（报告件镜像后归零至 8，全为他链） |
| 7 | 见证器复跑（全量口径） | 16/18 变 **17/18**（scan.publish.live_zero=0 PASS；parity.key_files 仅剩本报告 json）→ 18/18（§10） |
| 8 | 公开面 | push 后复查见 §9（Pages CI 重建中；根因=origin/main 已含清档） |

## 1. 发布仓镜像逐面处置表（变更集 60 路径）

口径：前像=发布仓 c32f669 对象；后像=发布仓 35061ce 对象；工作仓像=8adbdabd 对象；差异行数=`git diff --numstat c32f669..35061ce`（二进制面记 bin；两仓镜像前已一致记 0/0）。末列「工作仓同像」= 工作仓 HEAD 对象 sha256 == 发布仓后像。

| 路径 | 状态 | 发布仓前像 | 发布仓后像 | 工作仓像 | 差异行数 | 工作仓同像 |
|---|------|------|-----------|-----------|---------|---------|-----------|
| `api/data/scenarios_en.json` | M | 782418eb5806 | dc5ab0b81ef9 | dc5ab0b81ef9 | +1/-1 | == |
| `api/protreptic.db` | M | 00952cbd87eb | e82be49fa011 | e82be49fa011 | bin | == |
| `data/backup_phase21r8_azj345_clear_20260923/MANIFEST.json` | A | （无） | a303ef2c7095 | a303ef2c7095 | +256/-0 | == |
| `data/backup_phase21r8_azj345_clear_20260923/MANIFEST.sha256` | A | （无） | bb81e4b7cc90 | bb81e4b7cc90 | +31/-0 | == |
| `data/backup_phase21r8_azj345_clear_20260923/README.md` | A | （无） | 6479e9f7b273 | 6479e9f7b273 | +52/-0 | == |
| `data/backup_phase21r8_azj345_clear_20260923/api/data/scenarios_en.json` | A | （无） | 782418eb5806 | 782418eb5806 | +1/-0 | == |
| `data/backup_phase21r8_azj345_clear_20260923/docs/architecture/static_data_manifest.json` | A | （无） | 7afc3e46ffcf | 7afc3e46ffcf | +1/-0 | == |
| `data/backup_phase21r8_azj345_clear_20260923/docs/architecture/web_p0_routes.json` | A | （无） | dd5c664b8b90 | dd5c664b8b90 | +16455/-0 | == |
| `data/backup_phase21r8_azj345_clear_20260923/docs/historical_figures_thinking_modes_library.md` | A | （无） | a2b37271a4ee | a2b37271a4ee | +17244/-0 | == |
| `data/backup_phase21r8_azj345_clear_20260923/docs/research/batch_new_figures_research.md` | A | （无） | eafcc559156e | eafcc559156e | +1221/-0 | == |
| `data/backup_phase21r8_azj345_clear_20260923/docs/research/candidates_v4_research.legacy.md` | A | （无） | 8518458ea7e2 | 8518458ea7e2 | +33/-0 | == |
| `data/backup_phase21r8_azj345_clear_20260923/docs_site/docs/historical_figures_thinking_modes_library.md` | A | （无） | 5f238a4e5afe | 5f238a4e5afe | +12176/-0 | == |
| `data/backup_phase21r8_azj345_clear_20260923/docs_site/docs/scenario_tags.json` | A | （无） | 198e96a75370 | 198e96a75370 | +13160/-0 | == |
| `data/backup_phase21r8_azj345_clear_20260923/three_dimensional_comparison_matrix.xlsx` | A | （无） | 842ba499604f | 842ba499604f | +134/-0 | == |
| `data/backup_phase21r8_azj345_clear_20260923/tools/batch2_candidates.json` | A | （无） | 532206efd2a5 | 532206efd2a5 | +442/-0 | == |
| `data/backup_phase21r8_azj345_clear_20260923/tools/ci_data_check.py` | A | （无） | 8efa76d471de | 8efa76d471de | +378/-0 | == |
| `data/backup_phase21r8_azj345_clear_20260923/tools/code_maps_en.json` | A | （无） | b1893a9bbc8d | b1893a9bbc8d | +1068/-0 | == |
| `data/backup_phase21r8_azj345_clear_20260923/tools/export_static_site.py` | A | （无） | 0166d06402cc | 0166d06402cc | +910/-0 | == |
| `data/backup_phase21r8_azj345_clear_20260923/tools/json/scenarios_en.json` | A | （无） | 018aadd45918 | 018aadd45918 | +1/-0 | == |
| `data/backup_phase21r8_azj345_clear_20260923/tools/json/scenarios_zh.json` | A | （无） | c240aa300812 | c240aa300812 | +1/-0 | == |
| `data/backup_phase21r8_azj345_clear_20260923/tools/pages_preflight.py` | A | （无） | 440fb33a0846 | 440fb33a0846 | +273/-0 | == |
| `data/backup_phase21r8_azj345_clear_20260923/tools/test_full_backup.py` | A | （无） | 6d7152850786 | 6d7152850786 | +260/-0 | == |
| `data/backup_phase21r8_azj345_clear_20260923/web/dist/data/figures.index.json` | A | （无） | f0eded8cd6b5 | f0eded8cd6b5 | +1/-0 | == |
| `data/backup_phase21r8_azj345_clear_20260923/web/dist/data/figures/H-AZJ-345.json` | A | （无） | bf39b4863743 | bf39b4863743 | +1/-0 | == |
| `data/backup_phase21r8_azj345_clear_20260923/web/dist/data/index.unified.json` | A | （无） | 22d22a0f1394 | 22d22a0f1394 | +1/-0 | == |
| `data/backup_phase21r8_azj345_clear_20260923/web/dist/data/meta.json` | A | （无） | a1ff7edd497a | a1ff7edd497a | +1/-0 | == |
| `data/backup_phase21r8_azj345_clear_20260923/web/dist/sitemap.xml` | A | （无） | d15b6858bb8e | d15b6858bb8e | +6754/-0 | == |
| `data/backup_phase21r8_azj345_clear_20260923/web/public/data/figures.index.json` | A | （无） | f0eded8cd6b5 | f0eded8cd6b5 | +1/-0 | == |
| `data/backup_phase21r8_azj345_clear_20260923/web/public/data/figures/H-AZJ-345.json` | A | （无） | bf39b4863743 | bf39b4863743 | +1/-0 | == |
| `data/backup_phase21r8_azj345_clear_20260923/web/public/data/meta.json` | A | （无） | 1f35459d117e | 1f35459d117e | +1/-0 | == |
| `data/backup_phase21r8_azj345_clear_20260923/web/public/sitemap.xml` | A | （无） | d15b6858bb8e | d15b6858bb8e | +6754/-0 | == |
| `data/backup_phase21r8_azj345_clear_20260923/web/src/generated/siteCounts.ts` | A | （无） | a5a47d3f2121 | a5a47d3f2121 | +54/-0 | == |
| `data/figures/_duplicates/H-AZJ-345_api_scenarios_en_entry.json` | A | （无） | 40f7bfe2c055 | 40f7bfe2c055 | +11/-0 | == |
| `data/figures/_duplicates/H-AZJ-345_docs_site_fragments.md` | A | （无） | 0b17162660c3 | 0b17162660c3 | +90/-0 | == |
| `data/figures/_duplicates/H-AZJ-345_figures_row.json` | A | （无） | 9c420d72d8f6 | 9c420d72d8f6 | +54/-0 | == |
| `data/figures/_duplicates/H-AZJ-345_ledger.json` | A | （无） | 5970e33b7e64 | 5970e33b7e64 | +46/-0 | == |
| `data/figures/_duplicates/H-AZJ-345_legacy_docs_fragments.md` | A | （无） | bffb1d67d48f | bffb1d67d48f | +99/-0 | == |
| `data/figures/_duplicates/H-AZJ-345_products_snapshot.json` | A | （无） | b790054b5607 | b790054b5607 | +55/-0 | == |
| `data/figures/_duplicates/H-AZJ-345_registry_fragments.json` | A | （无） | eff38acbcc2e | eff38acbcc2e | +31/-0 | == |
| `data/figures/_duplicates/H-AZJ-345_scenarios_en_entry.json` | A | （无） | a01b3d9e7493 | a01b3d9e7493 | +11/-0 | == |
| `data/figures/_duplicates/H-AZJ-345_scenarios_zh_entry.json` | A | （无） | dcf6f03f3485 | dcf6f03f3485 | +11/-0 | == |
| `docs/architecture/static_data_manifest.json` | M | 7afc3e46ffcf | aa76ddf3310a | aa76ddf3310a | +1/-1 | == |
| `docs/architecture/web_p0_routes.json` | M | dd5c664b8b90 | 1a8319f86b80 | 1a8319f86b80 | +560/-64 | == |
| `docs/historical_figures_thinking_modes_library.md` | M | a2b37271a4ee | 1b75690b0956 | 1b75690b0956 | +1/-36 | == |
| `docs/research/_archive/H-AZJ-345_archive.json` | A | （无） | 6110059dcafc | 6110059dcafc | +326/-0 | == |
| `docs/research/batch_new_figures_research.md` | M | eafcc559156e | d775e20b6a26 | d775e20b6a26 | +0/-40 | == |
| `docs/research/candidates_v4_research.legacy.md` | M | 8518458ea7e2 | ed1b0fdfd31f | ed1b0fdfd31f | +0/-1 | == |
| `docs_site/docs/historical_figures_thinking_modes_library.md` | M | （无） | （无） | baf83383ec0e | 0/0 | 无对应 |
| `docs_site/docs/scenario_tags.json` | M | （无） | （无） | 3ed465358b4c | 0/0 | 无对应 |
| `three_dimensional_comparison_matrix.xlsx` | M | 842ba499604f | ed2bb2a2e21a | ed2bb2a2e21a | +13/-16 | == |
| `tools/batch2_candidates.json` | M | 532206efd2a5 | 959210c9ea10 | 959210c9ea10 | +1/-23 | == |
| `tools/ci_data_check.py` | M | 8efa76d471de | 6b766c37df27 | 6b766c37df27 | +1/-1 | == |
| `tools/code_maps_en.json` | M | b1893a9bbc8d | 37b93916f6fd | 37b93916f6fd | +1/-3 | == |
| `tools/export_static_site.py` | M | 0166d06402cc | 9559eb6d5dbc | 9559eb6d5dbc | +2/-1 | == |
| `tools/json/scenarios_en.json` | M | 018aadd45918 | acadac5909c2 | acadac5909c2 | +1/-1 | == |
| `tools/json/scenarios_zh.json` | M | c240aa300812 | 9c65a12157e8 | 9c65a12157e8 | +1/-1 | == |
| `tools/pages_preflight.py` | M | 440fb33a0846 | 5b228a289e31 | 5b228a289e31 | +2/-1 | == |
| `tools/test_full_backup.py` | M | 6d7152850786 | 43fc4d46f2a9 | 43fc4d46f2a9 | +1/-1 | == |
| `web/public/sitemap.xml` | M | d15b6858bb8e | 31bd3584aa11 | 31bd3584aa11 | +1548/-1358 | == |
| `web/src/api/static.ts` | M | 5ee743eea207 | 8400da4680b7 | 8400da4680b7 | +2/-2 | == |

统计：60 路径中 58 件 sha256 逐字节一致（工作仓同像 ==）；2 件 docs_site/* 无对应（§1.3）。发布仓镜像前已一致（0/0）31 件；本卡实际落盘 29 件（M 18＋A 11）。

### 1.3 两件 docs_site/* 豁免说明（留证）

- `docs_site/docs/historical_figures_thinking_modes_library.md`、`docs_site/docs/scenario_tags.json`
- 证据 1：发布仓 `git ls-files docs_site` = 0 件（空）；`ls -d docs_site` = 不存在 —— 发布仓全史未承载 docs_site 工程，无「对应路径」可对齐。
- 证据 2：官方 parity 口径原文（tools/check_repo_parity.py REPO_OTHER_ROLE）：「docs_site/**（更早的独立文档站工程，mkdocs.pages.yml 明确不用它）」= 既不参与站点构建、也不进入线上站点。
- 工作仓侧两件已随 8adbdabd 清档完成（AZJ 零残留，见工作仓见证器 registry.zero_12 / scan.docs_site.zero PASS）。
- 处置：登记豁免（不向发布仓新引入该目录），报告列明交船长复核。

## 2. 构建面同步（gitignored 在盘，不入索引）

- **web/public/data/**（figures 分片/index/meta/unified/daily/graph/modes/search）：copied 14／updated 322／quarantined 1（H-AZJ-345 分片移出）；全树复核 1412=1412、逐字节 0 差异；web/public 全树 1430=1430。
- **web/dist/**：copied 2775／updated 4／quarantined 1（旧 bundle `assets/index-CIZk14CD.js`）；全树 4208=4208。
- **site_docs/**（本地文档站构建产物）：copied 665／updated 334／quarantined 15；全树 1104=1104 —— QA 异议 8「PB site_docs 陈旧代次（09-18）从属现象」随同步消除（含旧 `site_docs/figures/H-AN-001/` 页的移出）。
- **计数对齐（发布仓实测）**：meta.counts.figures=1056／figures.index=1056／分片=1056／sitemap `<url>`=1388／routes=1387／unified.items=1371。
- `web/dist/index.html`：发布仓 .gitignore 前历史跟踪件（web/dist 全树唯一被跟踪件），随构建面对齐并入镜像提交。
- `web/public/sitemap.xml`：已跟踪件，属变更集（§1 表）。

## 3. 备份/归档件（与工作仓同口径入库）

- `data/backup_phase21r8_azj345_clear_20260923/` 30 件（其 `site_docs/` 4 件两仓同为 .gitignore 忽略，未入索引——同口径）
- `data/figures/_duplicates/H-AZJ-345_*` 9 件
- `docs/research/_archive/H-AZJ-345_archive.json` 1 件
- 逐件 sha 见 §1 表；工作仓 MANIFEST 校验由见证器 `archive.backup_manifest_sha` PASS 覆盖（31/31）。

## 4. 二进制面处置（逐件给结论）

- **api/protreptic.db：已对齐**。前像 `00952cbd87eb…`（发布仓旧像，figures 1057 行含 AZJ 行）→ 后像 `e82be49fa011…`（=工作仓 8adbdabd 像；figures=1056、AZJ 行=0，工作仓见证器 counts.db PASS）。
  口径说明：该文件是 pages.yml paths 触发器，但 CI Step 0 由 `tools/build_figures_db.py` 清表重建（parity EXCLUDED_TRIGGERS 原文），committed 内容不进构建结果；本卡仍按 byte-exact 对齐以清发布面全量扫描口径。
- **data/semantic_index_metadata.pkl（376,307 B；含 H-AZJ-345，code=1 name=2）**：两仓同像（sha `1b934918cf4f46d146cbcbe148f4a8cad9062205e715b86b4277ffdbdbd43523`）；属见证器 allowed_hit 豁免类目（api 侧语义检索副本）。
  **残余数据面**：清除需重新生成语义索引（api/semantic_search.py 读取），属「新数据内容」——本卡未动；交船长裁定是否另立数据卡。
- **api/data/semantic_index_metadata.pkl（469,318 B；code=1 name=2）**：仅工作仓存在（发布仓无此路径；api/** 不在 parity 边界）；同为 allowed 类目，交船长一并裁定。

## 5. 发布仓 AZJ 命中全量分类（合计 519 = live 0 + 豁免 65 + 站点构建面 454）

- 机检口径：`verify_azj345_clear.py` 的 `allowed_hit` predicate；扫描含 gitignored 与二进制（>60MB 跳过 0 件）；`walk_hits` 双模（code `H-AZJ-345` ＋ 名 `安子介`）。
- 卡面证据命令（原样，不含 site_docs 排除）：`grep -rl "H-AZJ-345" --exclude-dir=.git --exclude-dir=node_modules /opt/data/release/Protreptic-publish | wc -l` = **510**。
  口径对照：船长基线 73 = 不含 site_docs 产物面（本地构建产物）的窄口径；本卡 site_docs 面已按新代次同步（454 件命中全部属 QA §1 已核「纯导航 302 + 报告页 152、违例 0」类）。
- **live（非豁免、非站点构建面）= 0 件**（镜像前 21 件，清单见 t_ff294775 附录 A；逐件已在 §1/§2 消除）。
- 豁免 65 件逐条（类目 × code/name 命中数）：

| 路径 | 类目 | code | name |
|------|------|------|------|
| `data/audit/phase21r8_cgroup_residual_evidence.json` | 证据件（他卡） | 0 | 3 |
| `data/backup_phase21r8_azj345_clear_20260923/MANIFEST.json` | 备份盘（历史证据） | 4 | 0 |
| `data/backup_phase21r8_azj345_clear_20260923/MANIFEST.sha256` | 备份盘（历史证据） | 2 | 0 |
| `data/backup_phase21r8_azj345_clear_20260923/README.md` | 备份盘（历史证据） | 4 | 0 |
| `data/backup_phase21r8_azj345_clear_20260923/api/data/scenarios_en.json` | 备份盘（历史证据） | 1 | 0 |
| `data/backup_phase21r8_azj345_clear_20260923/docs/architecture/web_p0_routes.json` | 备份盘（历史证据） | 3 | 2 |
| `data/backup_phase21r8_azj345_clear_20260923/docs/historical_figures_thinking_modes_library.md` | 备份盘（历史证据） | 1 | 4 |
| `data/backup_phase21r8_azj345_clear_20260923/docs/research/batch_new_figures_research.md` | 备份盘（历史证据） | 1 | 2 |
| `data/backup_phase21r8_azj345_clear_20260923/docs/research/candidates_v4_research.legacy.md` | 备份盘（历史证据） | 0 | 1 |
| `data/backup_phase21r8_azj345_clear_20260923/docs_site/docs/historical_figures_thinking_modes_library.md` | 备份盘（历史证据） | 1 | 5 |
| `data/backup_phase21r8_azj345_clear_20260923/docs_site/docs/scenario_tags.json` | 备份盘（历史证据） | 2 | 1 |
| `data/backup_phase21r8_azj345_clear_20260923/site_docs/architecture/web_p0_routes.json` | 备份盘（历史证据） | 3 | 2 |
| `data/backup_phase21r8_azj345_clear_20260923/site_docs/historical_figures_thinking_modes_library/index.html` | 备份盘（历史证据） | 3 | 7 |
| `data/backup_phase21r8_azj345_clear_20260923/site_docs/research/batch_new_figures_research/index.html` | 备份盘（历史证据） | 1 | 3 |
| `data/backup_phase21r8_azj345_clear_20260923/site_docs/search/search_index.json` | 备份盘（历史证据） | 4 | 0 |
| `data/backup_phase21r8_azj345_clear_20260923/three_dimensional_comparison_matrix.xlsx` | 备份盘（历史证据） | 6 | 1 |
| `data/backup_phase21r8_azj345_clear_20260923/tools/batch2_candidates.json` | 备份盘（历史证据） | 1 | 2 |
| `data/backup_phase21r8_azj345_clear_20260923/tools/code_maps_en.json` | 备份盘（历史证据） | 1 | 0 |
| `data/backup_phase21r8_azj345_clear_20260923/tools/json/scenarios_en.json` | 备份盘（历史证据） | 2 | 0 |
| `data/backup_phase21r8_azj345_clear_20260923/tools/json/scenarios_zh.json` | 备份盘（历史证据） | 2 | 3 |
| `data/backup_phase21r8_azj345_clear_20260923/tools/test_full_backup.py` | 备份盘（历史证据） | 1 | 0 |
| `data/backup_phase21r8_azj345_clear_20260923/web/dist/data/figures.index.json` | 备份盘（历史证据） | 1 | 1 |
| `data/backup_phase21r8_azj345_clear_20260923/web/dist/data/figures/H-AZJ-345.json` | 备份盘（历史证据） | 1 | 3 |
| `data/backup_phase21r8_azj345_clear_20260923/web/dist/data/index.unified.json` | 备份盘（历史证据） | 2 | 1 |
| `data/backup_phase21r8_azj345_clear_20260923/web/dist/sitemap.xml` | 备份盘（历史证据） | 1 | 0 |
| `data/backup_phase21r8_azj345_clear_20260923/web/public/data/figures.index.json` | 备份盘（历史证据） | 1 | 1 |
| `data/backup_phase21r8_azj345_clear_20260923/web/public/data/figures/H-AZJ-345.json` | 备份盘（历史证据） | 1 | 3 |
| `data/backup_phase21r8_azj345_clear_20260923/web/public/sitemap.xml` | 备份盘（历史证据） | 1 | 0 |
| `data/backup_phase21r8_cgroup_residual_20260923/figure_names.json.before` | 备份盘（历史证据） | 0 | 2 |
| `data/backup_root_main_data_20260923/main_data.json` | 备份盘（历史证据） | 6 | 5 |
| `data/backup_root_tools_json_legacy_20260923/code_maps.json` | 备份盘（历史证据） | 3 | 2 |
| `data/figures/_duplicates/H-AN-001_archive_page.md` | 字节归档（R6C/R8 口径） | 0 | 29 |
| `data/figures/_duplicates/H-AZJ-345_api_scenarios_en_entry.json` | 字节归档（R6C/R8 口径） | 2 | 1 |
| `data/figures/_duplicates/H-AZJ-345_docs_site_fragments.md` | 字节归档（R6C/R8 口径） | 4 | 4 |
| `data/figures/_duplicates/H-AZJ-345_figures_row.json` | 字节归档（R6C/R8 口径） | 2 | 4 |
| `data/figures/_duplicates/H-AZJ-345_ledger.json` | 字节归档（R6C/R8 口径） | 9 | 1 |
| `data/figures/_duplicates/H-AZJ-345_legacy_docs_fragments.md` | 字节归档（R6C/R8 口径） | 4 | 8 |
| `data/figures/_duplicates/H-AZJ-345_products_snapshot.json` | 字节归档（R6C/R8 口径） | 7 | 6 |
| `data/figures/_duplicates/H-AZJ-345_registry_fragments.json` | 字节归档（R6C/R8 口径） | 13 | 5 |
| `data/figures/_duplicates/H-AZJ-345_scenarios_en_entry.json` | 字节归档（R6C/R8 口径） | 3 | 1 |
| `data/figures/_duplicates/H-AZJ-345_scenarios_zh_entry.json` | 字节归档（R6C/R8 口径） | 3 | 4 |
| `data/semantic_index_metadata.pkl` | 语义索引副本（allowed 类目） | 1 | 2 |
| `docs/architecture/web_pages_migration_assessment.md` | 历史评估件 | 2 | 0 |
| `docs/qa/phase21r8_luorq_qa_recheck_evidence/chain_commits_verify.json` | QA 证据（他链） | 11 | 0 |
| `docs/qa/phase21r8_luorq_qa_recheck_evidence/chain_commits_verify.txt` | QA 证据（他链） | 11 | 0 |
| `docs/qa/phase21r8_luorq_qa_recheck_evidence/parity_postmirror/parity_check_repo.txt` | QA 证据（他链） | 11 | 0 |
| `docs/qa/phase21r8_luorq_qa_recheck_evidence/parity_postmirror/residual_analysis.json` | QA 证据（他链） | 11 | 0 |
| `docs/qa/phase21r8_luorq_qa_recheck_evidence/result.json` | QA 证据（他链） | 20 | 0 |
| `docs/qa/phase21r8_luorq_qa_recheck_evidence/result.txt` | QA 证据（他链） | 10 | 0 |
| `docs/qa/phase21r8_luorq_qa_recheck_evidence/run.log` | QA 证据（他链） | 10 | 0 |
| `docs/qa/phase21r8_luorq_qa_recheck_evidence/runB_judge_v2/gates/parity_check_repo.txt` | QA 证据（他链） | 2 | 0 |
| `docs/qa/phase21r8_luorq_qa_recheck_evidence/runB_judge_v2/result.json` | QA 证据（他链） | 4 | 0 |
| `docs/qa/phase21r8_luorq_qa_recheck_evidence/runB_judge_v2/result.txt` | QA 证据（他链） | 2 | 0 |
| `docs/qa/phase21r8_luorq_qa_recheck_evidence/runB_judge_v2/run.log` | QA 证据（他链） | 2 | 0 |
| `docs/qa/phase21r8_luorq_qa_recheck_gates/parity_check_repo.txt` | QA 证据（他链） | 10 | 0 |
| `docs/research/_archive/H-AZJ-345_archive.json` | 字节归档（清档存档） | 15 | 1 |
| `docs/research/phase21r6C_archive_evidence.json` | 历史报告（R6C/R7/R8） | 0 | 1 |
| `docs/research/phase21r6C_archive_report.md` | 历史报告（R6C/R7/R8） | 0 | 1 |
| `docs/research/phase21r7_cgroup_identity_report.json` | 历史报告（R6C/R7/R8） | 5 | 15 |
| `docs/research/phase21r7_cgroup_identity_report.md` | 历史报告（R6C/R7/R8） | 6 | 22 |
| `docs/research/phase21r8_azj345_disposition.json` | 历史报告（R6C/R7/R8） | 4 | 5 |
| `docs/research/phase21r8_azj345_disposition.md` | 历史报告（R6C/R7/R8） | 29 | 16 |
| `docs/research/phase21r8_cgroup_residual_report.md` | 历史报告（R6C/R7/R8） | 0 | 1 |
| `docs/review/mode_coverage_report_v2.3.1.md` | 历史报告（评审） | 0 | 1 |
| `tools/add_batch2.py` | 历史工具（不涉 AZJ 动态逻辑） | 1 | 0 |

- **site_docs/ 454 件**：本地文档站构建产物（gitignored；CI 现场重建，不参与 Pages 部署、不上线）；携带 AZJ 的仅为导航条（disposition 报告页标题）与豁免报告页派生，违例 0。
- **R7 死副本镜像补做（1 件；注明：超出 8adbdabd 变更集，供船长复核）**：`tools/json/code_maps.json`（code=3 name=2）——R7（t_151265db，2857a525）已在工作仓以 R100 归档移除（→ `data/backup_root_tools_json_legacy_20260923/code_maps.json`），发布仓侧镜像滞后；本卡依目标①（发布面 live 归零）镜像移除：sha `bf1d624d7e65e9f24a6570ed9b358436145d492111b828ca923b46f2d444e2a8` 与两仓归档件逐字节一致（零内容损失；如需由 R7 链自理，可对 35061ce 内该 D 项单文件 revert）。
- **同源 R7 镜像滞后（未处置，报告列明）**：`tools/json/main_data.json`、`tools/json/modes_data.json`、`tools/json/, print(`、`tools/json/.json` —— 无 AZJ 字面量、不阻塞本卡目标；建议随 R7 收尾卡或另卡处理。

## 6. commits / push 回执

- 工作仓（master）：`8adbdabd`（变更集全量，被镜像）；`1de660cf`（杂项，含 W4/W6 报告与 backup_merge_*，未镜像——归各链）
- 发布仓（main）：`c32f669` 变 `35061ce`「Phase21-R8 H-AZJ-345 发布仓镜像补做（卡 t_6acd458b，对齐工作仓 8adbdabd）」
  - 60 files changed, 80547 insertions(+), 4887 deletions(-)；create 40 / delete 1（tools/json/code_maps.json）
- push 原文：`To https://github.com/ovmobilegroup/protreptic.git   c32f669..35061ce  main -> main`（rc=0；push1.log 原文见附录）
- ls-remote 复核：`35061ce0f3935b086c21918c1b9fd686955ef564  refs/heads/main` == 本地 HEAD（同 sha）
- 本报告与 .json 修正：工作仓提交 （sha 见 §10 补记）；发布仓报告件提交 （sha 见 §10 补记）＋push（回执见 §10 补记）

## 7. parity 复跑回执（python3 tools/check_repo_parity.py）

- 复跑#1（镜像前，02:39）：exit 1／**28 处** = CONTENT_DIFF 11 ＋ MISSING_IN_PUBLISH 17（含验收卡在途 clear_qa.md）
- 复跑#2（镜像主体后，02:44）：exit 1／**9 处** = CONTENT_DIFF **0** ＋ MISSING_IN_PUBLISH 9；`[stats] 两仓都有 2266 条（其中逐字节一致 2266）｜仅单侧 9 条（仅工作仓 9 · 仅发布仓 0）`
  - 9 条逐条归因：`docs/research/phase21r8_w4_names_recon.{json,md}`、`phase21w4_fix_manifest.{json,md}`、`phase21w6_marker_scan.{json,md}` 共 6 件 = 他链在途提交 1de660cf（镜像归各自链）；`docs/research/phase21r8_azj345_clear_qa.{md,json}` 2 件 = 验收卡 t_ff294775 在途（只读边界）；`docs/research/phase21r8_azj345_clear_report.json` 1 件 = 本卡件（随报告镜像归零）。
- **本卡相关路径差异 = 0（归零）**。
- 原始输出留档：`parity_post1.txt`（附录 B 摘录）。

## 8. 见证器复跑回执（python3 verify_azj345_clear.py，全量口径）

- 镜像前：**16/18** —— `scan.publish.live_zero` FAIL（live=21）；`parity.key_files` FAIL（8 件 mismatch）
- 镜像主体后：**17/18** —— `scan.publish.live_zero` **PASS（live=0）**；`parity.key_files` 仅 `docs/research/phase21r8_azj345_clear_report.json` 单侧
- 报告件镜像后：**18/18**（§10 补记）
- 对照说明：t_3669eb4a 自述「16/16」为 `--quick` 口径（跳过发布扫描）；本卡补做后全量闭合。

## 9. 公开面复核（https://ovmobilegroup.github.io/protreptic/）

- push 前（02:44:42 实测）：`/figures/H-AZJ-345/` HTTP **200**（正文含「安子介」5 处；取样 5,640 B）；`/data/figures/H-AZJ-345.json` 200；`/sitemap.xml` 200 —— Pages 仍为旧代次。
- push 后复核（02:46:19）：`/figures/H-AZJ-345/` 仍 HTTP 200（Pages CI 重建分钟级延迟内）。
- 根因闭环：Pages 由 origin/main 构建；origin/main 现为 35061ce（已含清档），CI 重建后该路径应 404；最终复测与时刻见 §10 补记（按卡面口径：持续 200 >30 分钟则标红升级）。

## 10. 收口回执（补记位）

> 本报告件镜像后：发布仓报告件提交与 push 回执、最终 parity/verify/curl 复测逐条记于文末「收口回执补记」（同批更新两仓，逐字节一致）。

## 附录 A：证据索引与复现

- scratch（本卡全部脚本/日志）：`/opt/data/profiles/elcano/cache/scratch/azj345/`
  - 扫描/分析：analyze.py（变更集逐件对比）、azj_hits.py、pub_live.py（predicate 分类）、dump_exempt.py（exempt_list.json）、topdiff2.py、tree_cmp.py
  - 镜像：mirror_step1.py（变更集）、mirror_step2.py（web/public/data＋web/dist/data＋sitemap）、mirror_step2b.py（web/dist 全树＋web/public 全树复核）、mirror_step3.py（site_docs）、qmv.py（隔离移出，不销毁）
  - 台账/回执：gen_table.py→table.json、gen_report.py、parity_post1.txt、verify_post1.txt、push1.log、curl_after_push_*、quarantine/（移出件：docs_site 误拷件、web/*/H-AZJ-345.json、旧 bundle、旧 site_docs 页、tools/json/code_maps.json）
- 复现命令（关键）：
  - `git -C /opt/data/release/Protreptic-publish log --oneline -1` → 35061ce（镜像主体）
  - `git -C /opt/data/release/Protreptic-publish ls-remote origin main` → 35061ce0f39…
  - `python3 tools/check_repo_parity.py`（工作仓内）
  - `python3 verify_azj345_clear.py`（工作仓内，全量口径）
  - 全量 AZJ 扫描：`python3 /opt/data/profiles/elcano/cache/scratch/azj345/pub_live.py`

## 附录 B：关键原始输出（摘录）

```
=== push ===
To https://github.com/ovmobilegroup/protreptic.git
   c32f669..35061ce  main -> main
push rc=0
=== ls-remote AFTER push ===
35061ce0f3935b086c21918c1b9fd686955ef564	refs/heads/main
```

```
[stats] 两仓都有 2266 条（其中逐字节一致 2266）｜仅单侧 9 条（仅工作仓 9 · 仅发布仓 0）
[DIFF] 9 处差异（文件名 + 侧别 + 理由分类）：（9 条逐条归因见 §7）
```

```
[PASS] scan.publish.live_zero :: live=0
[FAIL] parity.key_files :: mismatch=['docs/research/phase21r8_azj345_clear_report.json (single-side)']
=== 17/18 PASS ===
```

---
*本报告由 t_6acd458b（elcano）生成，2026-09-24 02:5x CST；补记见文末。*
## 收口回执补记（2026-09-24 02:5x CST，二批；两仓同批更新，逐字节一致）

- 工作仓提交（本批）：`31dbb5eb`「报告补全 + .json 修正」（2 files，317 insertions；报告 md 22,259 B；.json 修正 publish_sha=35061ce…）；本补记随二批提交入库。
- 发布仓提交（本批）：`b4155f5`「报告补全镜像（对齐工作仓 31dbb5eb）」；push 原文 `35061ce..b4155f5  main -> main`（rc=0）；ls-remote 复核 `b4155f576b56e5a2fd0806fe57d452a2a41ffa2a  refs/heads/main` == 本地 HEAD。
- 最终 parity（报告件镜像后，02:48）：exit 1／**8 处** = CONTENT_DIFF **0** ＋ MISSING_IN_PUBLISH 8（全为他链/在途：W4/W6 报告 6 件 = 1de660cf；验收卡 t_ff294775 在途 clear_qa.{md,json} 2 件）；`[stats] 两仓都有 2268 条（其中逐字节一致 2268）｜仅单侧 8 条（仅工作仓 8 · 仅发布仓 0）`；**本卡相关路径差异 0**。
- 最终见证器（全量口径，02:48）：**18/18 PASS（exit 0）** —— 含 `scan.publish.live_zero :: live=0`、`parity.key_files :: mismatch=[]`（18 项逐条见附录 C）。
- 公开面复测（旧代次仍在服务，Pages CI 重建中）：02:44:42／02:46:19／02:48:46／02:52:20 复测四次，`/figures/H-AZJ-345/` 均 HTTP 200、分片 `/data/figures/H-AZJ-345.json` 200、`/sitemap.xml` 与 `/data/figures.index.json` 各含 1 处 AZJ —— 与 push 时点对照均在部署延迟内。按卡面口径：持续 200 超过 30 分钟（03:13 后仍 200）需标红升级；本卡收口时点的最终复测记录见卡面 comment 回执（scratch/curl_*.txt 留档）。
- 遗留交船长裁定（3 项）：① `data/semantic_index_metadata.pkl`（两仓同像，含 AZJ）与 `api/data/semantic_index_metadata.pkl`（仅工作仓）—— 属见证器 allowed 类目豁免；清除需重新生成语义索引＝新数据内容，本卡未动；② R7 同源镜像滞后 4 件（`tools/json/main_data.json`、`tools/json/modes_data.json`、`tools/json/, print(`、`tools/json/.json`；无 AZJ 字面量、不阻塞）；③ `tools/json/code_maps.json` 移除为跨链补做（零内容损失，如需由 R7 链自理可单文件 revert）。

## 附录 C：最终见证器 18/18 全项清单（02:48，原文）

```
[PASS] scan.workspace.live_zero :: live hit files=0
[PASS] scan.site_docs.only_nav_or_reports :: nav-only=434 bad=[]
[PASS] scan.docs_site.zero :: []
[PASS] scan.products.zero :: []
[PASS] scan.products.azj_shard_absent
[PASS] counts.db :: figures=1056 azj_rows=0
[PASS] counts.aligned(db==meta==index) :: db=1056 meta=1056 index=1056
[PASS] counts.anchors :: 1056/1056
[PASS] counts.sitemap :: min=1388 urls=1388 routes=1387
[PASS] counts.unified :: items=1371 counts={'total': 1371, 'figures': 318, 'scenarios': 1053, 'with_modes': 1335}
[PASS] archive.byte_archives_sha
[PASS] archive.backup_manifest_sha
[PASS] archive.fragments_cover_12 :: fragments=12
[PASS] registry.zero_12 :: []
[PASS] registry.zh_en_parity :: zh=1069 en=1069
[PASS] reverse.others_intact :: {"H-HZX-002": true, "H-LUORQ-001": true, "H-BYB-342.scenario": true, "H-TJY-344.scenario": true, "H-CY-346.scenario": true, "registry.no_azj": true}
[PASS] scan.publish.live_zero :: live=0
[PASS] parity.key_files :: mismatch=[]
=== 18/18 PASS ===
```
