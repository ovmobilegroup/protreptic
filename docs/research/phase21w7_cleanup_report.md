# Phase21-W7 根/工具面清档报告 t_d24e11bc

- 日期: 2026-09-24 | 角色: 工作仓 elcano | 材料: `data/audit/phase21w7_classification.json|.md` (逐件 1351 条), `data/backup_phase21w7_clean_20260924/`
- 证据 JSON: `docs/research/phase21w7_cleanup_evidence.json` | 前像备份: `data/backup_phase21w7_clean_20260924/` MANIFEST.sha256

## 一 范围与口径

- 逐件三向证据: (1) 构建读序 build_figures_db find() / parity 现役集; (2) 引用扫描 - 文件名与 code 两向, 覆盖构建步骤/web/src/tools/docs/api/CI + scripts/tests 加严; (3) 字节孪生 - tools/json 对根 / 发布仓 intl_figures / 发布仓同路径.
- 裁定: 保留 = 真读者或活输入; 归档后删 = 零读者 + 零构建价值 + 字节孪生存在; 删 = 异常名杂物; 登记不动 = backup 目录与他卡在途件.

## 二 处置面 前像 / 裁定

| 面 | 件数 | 裁定 | 依据 |
|---|---|---|---|
| 根 *.json | 634 | 保留 2 件: .markdownlint.json / lighthouserc.json; 归档后删 632 | c 零读者零构建价值; 数据件 code 现役于 scenarios; 发布仓 intl_figures 字节孪生 608 件 + tools/json 孪生 |
| 根异常名杂物 | 5 目录 + `, ` | 删, 先备前像 | d shell 误操作残树, 内含 6 件破碎命令残留, 零引用 |
| tools/json | 673 递归 | 保留 3 件: scenarios_zh/en + scenario_tags 构建输入; 归档后删 670 | e R7 判死三要件; 发布仓同路径 673/673 byte-equal |
| backup 目录 | 33 | 30 已入库保持 + 3 未入库登记 - 他卡在途 W5FIX/W8B1/H-SHF-001 | f 按先例; 不夹带他卡产物 |
| R7 已处置件 | 5 | 只读复核, 原路径不存在 | g |

合计: 删除面 tracked 1309 = 根 632 + tools/json 670 + `, ` 1 + 异常目录内 6; 异常目录本体 5 个未跟踪目录树随删.

## 三 前像与可回滚

- 备份树: `data/backup_phase21w7_clean_20260924/{ws,pb}/` 保结构 + `MANIFEST.sha256`, 1979 行 = sha256 + rel + size; ws 1309 件 6,392,179 B; pb 670 件 2,884,879 B.
- 前像对账: ws 1309/1309, pb 670/670 逐件 sha256 与 git 历史 blob 一致, 工作仓 e5ddd13f^ / 发布仓 HEAD, 0 mismatch / 0 missing.
- 还原: `cp -a data/backup_phase21w7_clean_20260924/ws/. <repo>/`; 发布侧同理 `pb/.` 到发布仓根.

## 四 验证 全实测

1. 构建链隔离副本复跑, 8 步全绿 rc=0; 站点链五步 + 扩展: build_figures_db; export_static_site - figures=1027 / modes 3301 -> 发布 3241 / 隔离 60 / by-figure 320; gen_web_site_counts; build_daily_index - 3241; pages_preflight --stage data 全断言过; build_search_index; build_graph_data; build_unified_index - 1344 = figures 320 + scenarios 1024, with_modes=1308.
2. 门禁四连, 隔离副本: credibility_gate --hard-fail / verify_source_links --hard-fail / verify_findings --hard-fail / apply_verification_status --check 全部 rc=0.
3. 差异复跑对照 删前 vs 删后: iso = 删后状态, iso2 = 删前状态 由备份还原; 双跑同链: `Only in iso` = 0; `data/figures` 逐字节一致; 差异仅 13 件 = api/protreptic.db, row-hash 两侧相等 8cb98ba67531e983 行级零差异, + 12 件构建产物, generated_at 时间戳及其 sha 级联, 归一化后 9 件全等 / 3 件仅时间戳与级联 hash / 字节数全等. 结论: 删除面对构建输入与产物零影响.
4. 引用复扫 删后: 构建步骤/web/src/CI 0 命中, .github 与 web/src 全零; api/cli_tests/scripts 命中逐条核验 = 解析至 tools/ 或 data/, 非根; 其余提及限定在 archival 类: docs 297 件 / tools 一次性脚本 非构建图 / 根遗留 .py / data 登记与 audit/backup / CHANGELOG / release/. 结论: 0 悬空运行引用.
5. parity 实测: 见第五节, 镜像后复跑构建图逐字节.
6. 见证器: verify_azj345_clear.py 全量 = 10/18 PASS. 8 项 FAIL 逐项归因 = 见证器陈旧: 锚 1056/1388/1371 vs 现值 1027/1361/1344, W4 链重锚所致; scan.*.live_zero 前提被后继卡 r9 合法推翻 - 安子介已以 H-AZJ-001 重落地, data/modes_data.json 现役 57 处; scan.products.zero 命中含现役 H-AZJ-001 的陈旧产物. 本卡未修改见证器, 不夹带他卡产物; 建议: 重锚或退役, 移交船长裁定.
7. 计数自洽: e5ddd13f - W9 卡 14:18 提交 - 扫入本卡暂存的 1303 件删除, 已实测该提交全部删除 1303 件均属本卡删除面, 无越界; 本卡提交补异常目录内 6 件删除 + 备份/分类/报告. 删除面 tracked 1309 = e5ddd13f 1303 + 本卡 6, 逐件一致.

## 五 两仓角色与镜像

- 根面: 发布仓根无同名件, 仅 2 配置有根同名且保留; 发布仓 `data/intl_figures` 637 件为开发侧原始分片留档角色, 保留, 根面 608 件字节孪生即在其内. 根面删除仅工作仓, 无发布侧镜像.
- tools/json 面: 发布仓同路径 673/673 byte-equal 逐件已证. 按角色镜像: 发布侧同删 670 件, 前像入 `pb/`.
- 边界内新增 备份树/分类/报告: 两仓镜像保持一致, parity 全绿.

## 六 遗留与移交

- 3 个未入库 backup 目录 W5FIX/W8B1/H-SHF-001 = 他卡在途, 本卡登记未动.
- 根 643 件遗留 .py + 3 .sh, 本卡面外; 其引用已在第四节 4 项 archival 类登记. 建议另卡评估.
- verify_azj345_clear.py 重锚/退役建议, 见第四节 6 项.
