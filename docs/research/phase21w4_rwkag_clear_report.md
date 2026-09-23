# Phase21 W4 RW-KAG-1..27 模板废件全链清档·执行报告 (卡 t_ee203180)

- 卡号: t_ee203180 (单写者执行卡); 依据: docs/research/phase21w4_fix_manifest.md/.json 3.6 R10 + t_536073f4 报告 五/六
- 上游: t_536073f4 (done; R10 归属本卡, 其卡零触碰本批) ; 下游: t_8bad8d98 (独立 QA) -> t_616e4991 (文档)
- 证据 JSON: docs/research/phase21w4_rwkag_clear_evidence.json | 归档: docs/research/_archive/RW-KAG_1-27_archive.json | 见证器: verify_rwkag_clear.py
- 备份: data/backup_phase21w4_rwkag_clear_20260924/ (payload 89 件 + MANIFEST.sha256 + backup_manifest.json + README + 片段提取器; byte-exact)

## 一, 结论速览 (全部实测, 禁止照抄预测)

| 项 | 前 | 后 | 差 |
|---|---|---|---|
| scenarios_zh 键集 | 1067 | 1040 | -27 |
| scenarios_en 键集 | 1067 | 1040 | -27 |
| code_maps_en 键集 | 1019 | 992 | -27 |
| DB figures | 1054 | 1027 | -27 |
| figures.index | 1054 | 1027 | -27 |
| 详情分片 | 1054 | 1027 | -27 |
| 统一索引 total | 1369 (318+1051) | 1342 (318+1024) | -27 |
| 路由 | 1385 | 1358 | -27 |
| sitemap URL | 1386 | 1359 | -27 |
| 发布模式 / by-figure | 3221 / 318 | 3221 / 318 | 0 (边界外) |

- 27 码全链残留: **0** (源/DB/index/unified/routes/sitemap/dist + 发布仓; 豁免类清单见 六)
- RW-KAG-001 (卡加梅/Paul Kagame): 全链在位零触碰 (边界1), DB 逐字核对 PASS
- 门禁四连 + 双 preflight + npm build 全绿; ci_data_check 24/24; 见证器 16/16 (quick) + 全量见回执
- 备份 MANIFEST.sha256: sha256sum -c **89/89**; 归档片段字节级 27x6 逐项 PASS

## 二, 逐面处置表 (前像/后像/差异)

| 面 | 前像 | 后像 | 差 | 处置 |
|---|---|---|---|---|
| tools/json/scenarios_zh.json | 3015351 B / 1067 键 | 2981559 B / 1040 键 | -33792 B（= 27 条目字节和, 恒等式已验） | 27 条目键级删除（最小 diff） |
| tools/json/scenarios_en.json | 2275023 B / 1067 键 | 2250645 B / 1040 键 | -24378 B（= 27 条目字节和, 恒等式已验） | 27 条目键级删除（最小 diff） |
| tools/code_maps_en.json | 86330 B / 1019 键 | 84242 B / 992 键 | -2088 B（27 行, 零外溢字节） | 27 占位映射键整行删除（外科式） |
| api/protreptic.db | figures 1054（27 码行在） | figures 1027（27 码行 0） | -27 行 | 全量重建（build_figures_db） |
| tools/json/RW-KAG-1..27.json | 27 件 | 0 件（备份盘 byte-exact） | -27 件 | 草稿本体归档引用移出（git R100 -> 备份盘） |
| RW-KAG-1..27.json（根） | 27 件（与草稿逐字节相同） | 0 件（备份盘 byte-exact） | -27 件 | 同码双胞归档移出（git R100 -> 备份盘；超 R10 字面, 登记） |
| web/public/data/figures/RW-KAG-*.json | 27 分片在 | 0（分片数 1027） | -27 分片 | 全量重建（export_static_site prepare_out rmtree 重建口径） |
| web/public/data/figures.index.json | 1054 条 | 1027 条 | -27 | 重建 |
| web/public/data/index.unified.json | 1369（318+1051） | 1342（318+1024） | -27 | 重建 |
| docs/architecture/web_p0_routes.json | 1385 路由 | 1358 路由 | -27 | 重建（prerender_routes --body-persons all） |
| web/public/sitemap.xml | 1386 URL | 1359 URL（= 路由 1358 + 首页） | -27 | 重建（build_sitemap） |
| web/dist/** | 含 27 码页面/数据 | 27 码 0 残留 | 0（gitignore 产物） | 全量重建（npm run build + prerender 1358 页 + apply_site_counts + sw + sitemap） |
| 锚点 4 文件 | EXPECT_FIGURES 1054 x2 / MIN_SITEMAP_ENTRIES 1386 / 文案 1054 x4 | 1027 x2 / 1359 / 文案 1027 x4 | 同提交更新 | 取重建后实测 |

注: 三个文本源为**最小 diff** 编辑; 删除字节和恒等式 (前-后 = 被删片段字节和) 已在见证器 diff.minimal_identity 断言 PASS: zh -33792B / en -24378B / code_maps -2088B。
注: 差异行数口径 - 三个源中 scenarios 为紧凑单行 JSON (git numstat 计 1/1, 语义为 27 条目), code_maps_en 为 27 行整行删除; 机器可读 numstat 见 report.json surfaces[].numstat。

## 三, 重建链与锚点 (取重建后实测)

链 (全绿): build_figures_db(figures=1027) -> export_static_site(产物 1355 文件: index 1 + figures 1027 + modes 8 + by-figure 318 + meta 1; 隔离零泄漏) -> gen_web_site_counts(零 diff, 3221x318 口径不变) -> build_daily_index(318) -> preflight --stage data PASS -> build_search_index(16 分片) / build_graph_data -> build_unified_index(1342) -> 门禁四连 (credibility rc=0 / source_links rc=0 / findings rc=0 / ci_data_check 24/24) -> npm run build -> preflight --stage dist PASS -> prerender_routes(--body-persons all; routes=1358) -> apply_site_counts(dist 扫描 2739 文件零违规) / build_sw / build_sitemap(1359)。

锚点同提交更新 (实测, 见 二 末行与证据 JSON anchor_changes):
- tools/export_static_site.py: EXPECT_FIGURES 1054 -> **1027** (变更注释行不含码字面量, 防扫描噪音)
- tools/pages_preflight.py: EXPECT_FIGURES 1054 -> **1027**
- tools/ci_data_check.py: MIN_SITEMAP_ENTRIES 1386 -> **1359**
- web/src/api/static.ts L13/L15 文案 + web/src/views/ApiDocsView.vue L11 文案: 1054 -> **1027** (x4)

## 四, 验证 (全实测; 机器可读见证据 JSON)

1. **全仓扫描 (含 gitignored)**: 工作仓 27 码(1..27 口径) 命中文件 179 -> 124, live=0; 命中全落豁免类 (备份/审计/报告/归档/release/site_docs/validation_report)。
2. **构建面显式归零**: web/public/**、web/dist/** 27 码 0 (不依赖豁免断言)。
3. **计数自洽**: figures 1027 = DB = index = 分片 = meta; sitemap 1359 = 路由 1358 + 首页; unified 1342 = 318 + 1024; 发布模式 3221 / by-figure 318 不变。
4. **备份 byte-exact**: MANIFEST.sha256 sha256sum -c 89/89; backup_manifest.json 逐件 source/copy 双记; 根双胞 27/27 与草稿逐字节相等; intl 副本 27/27 与草稿逐字节相等 (归档引用)。
5. **归档字节级**: per_code_fragments 27 码 x 6 类片段 (zh/en 条目、code_maps 行、草稿、分片、根双胞) sha256 逐项重算 PASS; death_evidence 6 条依据链。
6. **反向核对**: RW-KAG-001 全链在位; H-LXN-001/SG-LEE-001/JP-SAS-001/UZ-ULU-001/H-MZ-001/H-HLG-001/H-CY-346 抽样在位。
7. **门禁/测试复跑**: 见 一/三; 见证器 verify_rwkag_clear.py 可复跑断言 (quick 16/16)。

## 五, 发布仓镜像

- 镜像面 (byte-exact): 源三件 + DB + routes + sitemap + static_data_manifest + 锚点四文件 + 备份盘 (含 README/提取器) + 归档 JSON + 报告对 + 证据 JSON + 草稿删除 (R100 对应删除)。
- 发布仓独有件处置: data/intl_figures/RW-KAG-1..27.json (27 件, 逐字节=草稿) 归档移除; 依据与登记见 六 E-f。
- 构建面同步: web/public/data (1355 文件) 与 web/dist 全树自工作仓同步 (发布仓 web/dist/index.html 为历史跟踪件, 随镜像提交)。
- parity 复现见 七。

## 六, 残留与登记 (不静默; 全部实测/有据)

- **E-a** tools/validation_report.json（2026-08-22 校验报告快照, 含 27 码记录性引用） -> 保留+登记（历史报告类, 非读者）
- **E-b** site_docs/** 6 件（routes 副本/报告页/搜索索引, 陈旧构建） -> 保留+登记（gitignore 构建产物；mkdocs 未安装未重建；与 t_536073f4 同口径；CI 重建）
- **E-c** release/v2.0.0/** 4 件（冻结发布归档镜像） -> 保留+登记（归档类）
- **E-d** data/audit/phase21r7_leftovers_inventory.json（R7 审计留痕） -> 保留+登记（审计类）
- **E-e** docs/research 报告类（W4/R8/本卡报告含码引用） -> 保留+登记（报告类）
- **E-f** 进程外处置登记: 根双胞 27 件 + 发布仓 intl 副本 27 件（manifest R10 字面未点名） -> 先备份后清除+本报告§六登记（依卡步7全仓口径 + W7 卡 deferral）
- **E-g** data/intl_figures/** 其余 610 件（发布仓留档, 非本 27 码） -> 零触碰（源库留档, parity 边界外）

分类计数 (工作仓 124 命中文件): BACKUP=107 (含本卡备份盘 93) / SITE_DOCS=6 / REPORT(research)=5 / RELEASE-ARCHIVE=4 / AUDIT=1 / TOOLS-other=1 (validation_report)。

## 七, 回执 (提交/镜像/push/parity/raw)

- 工作仓 commit: {{WS_COMMIT}} (主体; HEAD {{WS_HEAD}})
- 发布仓镜像 commit: {{PB_COMMIT}}; push: {{PUSH}}; remote main: {{REMOTE_MAIN}}
- parity: {{PARITY}}
- 远端 raw 校验: {{RAW}}
- 备份盘镜像: {{BAK_MIRROR}}; 报告 v2 补记: {{V2}}
- 见证器全量 (含发布面): {{VERIFIER_FULL}}

