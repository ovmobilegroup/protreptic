# Phase21-R8 遗留清档 · H-AZJ-345「安子介（特区叙事）」清除 — 独立验收报告

- 验收卡：t_ff294775（验收员 espinosa）｜被验收卡：t_3669eb4a（执行 elcano）
- 被验收工作仓提交：8adbdabd981ba7c32f70c9e6d93854a5f0e7e4e3、1de660cfd5964f72313f3a4a3f38670c5e745240；自述镜像 1de660cf
- 验收时段：2026-09-24 02:00–03:00 CST；清前基线 bd039538；镜像末代 c32f669
- 验收方式：独立扫描器（不复用被验收方见证器）+ 隔离副本全链复跑 + 官方工具复跑
- 写入边界：**工作仓与发布仓零写入**（副本与日志在 /opt/data/profiles/espinosa/cache/scratch/azjqa/）

## 0. 总体结论：有条件驳回 · 建议补做发布面后复验

工作仓数据层清除与归档链已独立核实通过；**发布面未闭环**：发布仓未提交、live 面未镜像、未 push，发布面仍含 H-AZJ-345（远端 refs/heads/main 实测仍为 c32f669）。另有 3 项观察需船长裁定。

| # | 检查项 | 结论 |
|---|--------|------|
| 1 | 独立扫描（WS+PB 全量，含 gitignored 面） | WS PASS（live 残留 0）／PB **FAIL**（live 21 件） |
| 2 | 计数自洽 | PASS（关系全绿；前置差逐项归因，数据层零越界） |
| 3 | 测试与门禁 | 四门禁 + preflight + 站链五步 PASS；test_full_backup **FAIL（既有基线）**；apply_verification_status --check exit 1（在途 W5） |
| 4 | 归档/备份完整性 | PASS（12 片段 before/after + 8 字节存档 + 31 预像 + MANIFEST 全过） |
| 5 | 两仓 parity | **FAIL**（官方工具 exit 1，27 处；远端 main 仍 c32f669） |
| 6 | 反例检查 | PASS（仅删 AZJ；样本注册面齐全） |
| 7 | 自述复核 | 「16/16 PASS」系 --quick 口径；全量复跑 16/18 exit 1 |

> **【复验更新 · 2026-09-24 03:19 CST】船长裁定（03:15）后复验全绿：双仓 effective live=0、官方 parity CONTENT_DIFF 0、全量见证器 18/18、公开面正对照 200 且 H-AZJ-345 三径 404 生效 → 本验收结论由「有条件驳回」更新为「通过」。异议 1/2 已闭环；3 追认接受；4/5/7 登记不阻断；6 归子卡 t_fdc1589e；8 随补正同步复验确认。详见 §9（含 1 件受控归档显式豁免登记与首轮计数勘误）。**

## 1. 独立扫描（WS + PB 全量，含 gitignored）

方法：自写扫描器按 code `H-AZJ-345` 与名 `安子介` 双模全树扫描（0 漏），逐文件归档归属分类；site_docs 导航面逐条锚点核验。

- 工作仓：532 个命中文件，全落豁免类，**live 残留 0** —— 本卡存档/报告 41（备份 27、_duplicates 10、报告 3、见证器 1）；他卡/历史/发布快照/遗留 37；site_docs 454（302 纯导航，逐条锚点核验违例 0；152 报告页）。
- 发布仓：**FAIL** —— 412 命中 = live **21 件**（清单见附录 A）+ 陈旧 site_docs 335（2026-09-18 代次构建）+ 存档/他卡/历史 56（本卡备份 27、archive.json 1、disposition 2 等）。
- 附：PB 另有 4 个文件无 AZJ 字面量但与工作仓版本滞后（tools/ci_data_check.py、tools/pages_preflight.py、tools/export_static_site.py、web/src/api/static.ts），见 §5。

## 2. 计数自洽

当前值关系全绿：db=1056 ＝ meta.figures=1056 ＝ figures.index=1056 ＝ figure 分片=1056；by-figure=318 ＝ unified.figures=318；unified 1371 = 318+1053；routes 1387（bodies 328）；sitemap 1388 = 1387+1；scenarios_zh/en 各 1069；api/data/scenarios_en 520；模式四态 3281 去重（公开 3221）与 3291 顶格（公开 3231）双口径自洽。两处发布锚点 EXPECT_FIGURES=1056 与实际一致。

与清前基线的差：db −1、scenarios −1（=H-AZJ-345）；routes/sitemap +38（= +40 补页 −2 陈旧路由，成因见异议 3 / 附录 B）。**数据层无越界**（除 AZJ 外零改动，见 §6）。

## 3. 测试与门禁（全部本机复跑）

- test_full_backup.py：**FAIL**（断言期望 858 vs 实况 1056/1057）；自 bd039538 提取旧版复现同红 → 先存缺陷、非本卡引入（上游 metadata 未提）。
- test_thinking_mode_selector.py：PASS（ALL TESTS PASSED (11)）。
- 门禁四连：credibility_gate --hard-fail exit 0；verify_findings --hard-fail exit 0（非阻断警告 2 条：计数过期 E 164/166、M-ASM-* 重复收割）；verify_source_links --hard-fail exit 0（存量 UNREACHABLE 4 条）；ci_data_check PASS 24 断言 / 0 失败。
- pages_preflight --stage data：exit 0（figures=1056 modes=3281 published=3221 隔离命中 0；分片 1056/318）。
- apply_verification_status --check：exit 1，19 条 pending→verified（例 M-WC-001..005）——W5 pilot 待落地，属子卡 t_fdc1589e 范围（非本卡缺陷）。
- 站点链五步（隔离副本复跑）：build_figures_db（1056 行）→ export_static_site（figures=1056, by-figure=318）→ build_unified_index（total=1371）→ prerender_routes --body-persons all（1387 路由 / 328 正文）→ build_sitemap（1388 条）全部 exit 0；附加 site_counts/daily/search/graph 亦 exit 0；副本内 ci_data_check + pages_preflight 全绿。
- 产物字节对照（副本 vs 在库件）：1056/1056 分片、figures.index、unified、sitemap 逐字节全等；meta/manifest 仅 generated_at 类时间戳差（manifest 另含 db 文件 sha）；routes 1387 条逐条全等（唯一差异 total_html_bytes 为 dist 构建面状态量）；db 逻辑内容零差异（仅删 AZJ 行 + id 顺移；文件字节层为重建布局差异，db 属 CI 现场重建件、不在 parity 口径）。

## 4. 归档/备份完整性

- 12 片段：before=git bd039538 快照 sha、after=现库 sha，12/12 全对（含四镜像面）。
- 8 字节存档：sha 8/8 与 archive.json 一致；ledger 与清单一致。
- 31 预像文件 + MANIFEST.sha256：31/31；archive.json 的 preimage 清单与备份盘一致。
- 结论：**字节级归档链完整**，Stage I/J 要求达成。

## 5. 两仓 parity（官方与自测口径）

- 官方 tools/check_repo_parity.py：**exit 1 / DIFF**，27 处 = 11 CONTENT_DIFF（tools/json/scenarios_zh.json、tools/json/scenarios_en.json、api/data/scenarios_en.json、web/public/sitemap.xml、docs/architecture/web_p0_routes.json、docs/architecture/static_data_manifest.json、docs/historical_figures_thinking_modes_library.md、docs/research/batch_new_figures_research.md、docs/research/candidates_v4_research.legacy.md、tools/export_static_site.py、tools/pages_preflight.py、web/src/api/static.ts）+ 16 MISSING_IN_PUBLISH（9 个 _duplicates + clear_report.json + w4/w6 报告 6 件）。
- 远端实测：git ls-remote origin main = c32f66955a6fb996e546b531f1e26812c1feda07（W5 代次）→ **未推送**；发布仓本地 HEAD 亦 c32f669，工作区仅 2 个未跟踪项（备份目录、_archive/），无提交。
- 工作仓 master 无远端跟踪（branch -a --contains 仅 * master），工作仓提交本地留存符合惯例；未闭环的是镜像侧。
- 被验收方自测复核：verify_azj345_clear.py --quick = **16/16 PASS（该口径跳过发布扫描）**；全量复跑 = **16/18、exit 1**（scan.publish.live_zero live=21；parity.key_files mismatch 8）。

## 6. 反例检查

- scenarios_zh/en 与 api/data/scenarios_en：仅删 H-AZJ-345；公共键逐条深比全等、无新增键。
- db figures：仅删 H-AZJ-345 行（id 顺移 1 位，其余 19 列逐列全等）；行序保序（删行后序列 = 原序列减 AZJ）。
- 样本：H-HZX-002（王祥）、H-LUORQ-001（罗瑞卿）、H-ZX-001（曾子）在 data/figures、code_maps、figure_names、modes_data、docs/figures 各注册面齐全；场景样本 H-BYB-342/H-TJY-344/H-CY-346 完好。
- 结论：**无人为扩大清除面**。

## 7. 异议清单（8 条）

1. 【必须处置·发布面未闭环】发布仓未提交未推送：PB HEAD=c32f669 未动（01:59:54），远端 main 实测 c32f669；PB 仅 2 个未跟踪新增（备份目录 01:40、_archive/ 02:07-02:07），live 面 21 件仍含 AZJ；parity 工具 exit 1。上游 metadata commits.publish_mirror=1de660cf 实为**工作仓第 2 提交**（02:14:23），混淆。
2. 【必须处置·报告 md 缺失】metadata report_paths/artifacts 引用的 docs/research/phase21r8_azj345_clear_report.md 不存在（仅 .json 在盘且未提交未镜像）；push/parity 回执无载体。
3. 【需裁定·链重建刷新面超 AZJ】routes/sitemap +38 = +40 minds/* 补页（09-21~23 已入库人物；产物世代陈旧自 2026-09-20 12:22）−2 figures/*（H-AZJ-345 目标件 + H-CY-001：陈云档型由 scenario 转 figure，10 条模式档）。数据层零越界，但卡面要求「差异仅限 AZJ，否则停止并报告」，未见报告动作。
4. 【观察·既有红】test_full_backup.py 全红（bd039538 同红）；上游自述未提，四门禁口径未含此测试。
5. 【观察·名单外夹带】1de660cf（与 8adbdabd 同标题）夹带 27 件名单外文件：data/backup_merge_H-ZDY-001_*（21）与 docs/research/phase21r8_w4/phase21w4/phase21w6 报告（6）。
6. 【观察·在途】apply_verification_status --check exit 1（19 条 pending→verified）待子卡 t_fdc1589e 的 --write 落地。
7. 【观察·口径用词】metadata residual_exempt「site_docs_nav_only=454」实际为 302 纯导航 + 152 报告页（用词不准，结论不反）。
8. 【观察·镜像陈旧产物】PB site_docs 为 2026-09-18 代次构建：含 H-AZJ-345 之外的人名旧页（site_docs/figures/H-AN-001/「安子介 人物档案」，09-18）与 H-AZJ-345 13 处在 5 个陈旧文件内；属镜像未同步的从属现象。

## 8. 建议（给船长）

- A（推荐）：开补做卡（elcano）：① 发布仓全量同步（live 面 + 构建面 + 本卡存档/报告）；② 发布仓提交（含补交 clear_report.md 与本 QA 报告）；③ push origin main 并附回执 sha；④ QA 复跑（§1/§5 + 官方工具 + 全量见证器）。
- B：先裁定异议 3（接受刷新面）再补做。
- C（不建议）：直接判结——发布面未闭环前，「清除」对用户可见面未生效。

## 附录 A：发布仓 live 21 件清单

1. three_dimensional_comparison_matrix.xlsx
2. api/protreptic.db
3. api/data/scenarios_en.json
4. docs/historical_figures_thinking_modes_library.md
5. docs/architecture/web_p0_routes.json
6. docs/research/batch_new_figures_research.md
7. docs/research/candidates_v4_research.legacy.md
8. tools/batch2_candidates.json
9. tools/code_maps_en.json
10. tools/test_full_backup.py
11. tools/json/code_maps.json
12. tools/json/scenarios_en.json
13. tools/json/scenarios_zh.json
14. web/dist/sitemap.xml
15. web/dist/data/figures.index.json
16. web/dist/data/index.unified.json
17. web/dist/data/figures/H-AZJ-345.json
18. web/public/sitemap.xml
19. web/public/data/figures.index.json
20. web/public/data/index.unified.json
21. web/public/data/figures/H-AZJ-345.json

## 附录 B：链重建 +38 明细（异议 3 证据）

+40 minds/*：Coubertin、Homer、Sophocles、Thucydides、H-BG-001、H-BLT-001、H-CHB-001、H-CHE-001、H-CHI-001、H-CY-001、H-DA-001、H-DRK-001、H-DYC-001、H-DZ-001、H-FXT-001、H-GX-001、H-GYW-001、H-HZX-002、H-JMLS-001、H-JX-001、H-JY-001、H-KKQ-001、H-LJY-001、H-LUORQ-001、H-LWH-001、H-QIN-001、H-SJM-001、H-SQL-001、H-SQR-001、H-SY-001、H-WB-001、H-WFZ-001、H-WL-001、H-XFZ-001、H-YLS-001、H-YSK-001、H-ZDY-001、H-ZHX-001、H-ZX-001、H-ZXC-001。
−2 figures/*：figures/H-AZJ-345（目标件）；figures/H-CY-001（陈旧：陈云由场景档转人物档 minds/H-CY-001，5 条场景路由换代）。
证据：routes 1349→1387、sitemap 1350→1388；清前 routes/sitemap 末次生成 2026-09-20 12:22（Phase38-Y3），其后 09-21~23 的入库件未反映；本卡未改任何数据（除 AZJ 删除）。

## 附录 C：证据索引

- 副本仓：/opt/data/profiles/espinosa/cache/scratch/azjqa/chainrun/（五步复跑产物）
- 日志：同目录 logs/（g1b.log、g2b.log、g4b.log、ci2.log、pre2.log、chain*.log、verifier_parent.log、verifier_quick.log、parity_tool.json、test_full_backup.log、test_thinking_mode_selector.log）
- 扫描清单：ws_hits.json、pb_hits.json、class_WS.txt、class_PB.txt
- 复用命令：python3 verify_azj345_clear.py [--quick]；python3 tools/check_repo_parity.py --json；四门禁与 preflight 按 §3 名称直跑

## 9. 复验（船长裁定后 · 2026-09-24 03:14-03:19 CST）

依据船长 magallanes 2026-09-24 03:15 CST 裁定与复验指令（评论 #2957）执行；本卡复验全程只读（除本报告 pair 的追加、提交、镜像与 push 外零写入）。复验证据目录：`/opt/data/profiles/espinosa/cache/scratch/azjqa/reverify/`。

### 9.1 双仓全量扫描（复跑 §1）→ 双侧 effective live=0

命令（独立扫描器，与见证器不同实现；含 gitignored 面；跳过 .git/__pycache__/node_modules 等缓存目录，与首轮及见证器同口径）：

    python3 scan.py /opt/data/workspace/Protreptic ws_hits2.json
    python3 scan.py /opt/data/release/Protreptic-publish pb_hits2.json

- **工作仓**：29,046 文件扫描（03:14:43），命中 535，全落豁免类 —— 本卡存档 44（备份 27 / _duplicates 10 / 报告 6 / 见证器 1）；他卡·历史·发布快照·遗留 36；site_docs 454（302 纯导航 + 152 报告页）；受控归档登记 1（见 9.1a）。**live 0**。
- **发布仓**：10,744 文件扫描（03:14:47），命中 521，全落豁免类 —— 本卡存档 41（备份 27 / _duplicates 10 / 报告 4）；他卡·历史·遗留 25；site_docs 454（与工作仓对称）；受控归档登记 1。**live 0**。
- 首轮 PB 的 22 件 live（附录 A 21 件镜像清单 + 1 件受控归档）随补正卡 t_6acd458b 全量镜像清零；PB site_docs 由陈旧 335 件（09-18 代次）刷新为现行 454 件（302+152，两仓对称）。
- 含 H-AZJ-345 码字面量文件：WS 526 件 / PB 512 件 —— 逐件核对全部落在上述豁免类（全量分类清单：classfull_WS.txt / classfull_PB.txt）。
- 原 21 件 live 清单逐件复测：18 件两仓逐字节一致且 0 码 0 名；2 件 H-AZJ-345 分片两仓同删（ABSENT）；`tools/json/code_maps.json` 两仓同删（R7 链 R100 归档件，补正卡跨链镜像移除并登记于 clear_report §10）—— 合计 21/21 处置闭环。
- 证据：ws_hits2.json、pb_hits2.json、classfull_WS.txt、classfull_PB.txt、audit.log。

#### 9.1a 边界件裁定与登记（新增豁免登记 + 首轮勘误）

双仓各 1 件未豁免命中：`data/figures/_duplicates/H-AN-001_archive_page.md`（code=0 / name=29，17,379 B，两仓 byte-exact，sha256 326145b3…）。裁定为**他卡受控归档（豁免）**，依据：

1. 出处与登记：R6C 卡（t_4a9cf2cb，提交 7b767f39）字节归档件 —— 源 `docs/figures/H-AN-001.md`（安子介旧编号）R100 入 _duplicates；`docs/research/phase21r6C_archive_evidence.json` 登记 sha256 326145b3… = 实件；`data/audit/phase21r6_id_mapping_ledger.json` group C「已归档」。
2. 链条无关：清前基线 bd039538 与现 HEAD 同 blob（9acd3adb…），本链零改动；0 处 H-AZJ-345 码，仅档内原文含人名（R6C「未删字节·逐字留档」设计使然）。
3. 隔离：`data/figures/_duplicates/` 无任何构建/导出/上线读取链路（grep 全链 0 引用；上线 `…/data/figures/_duplicates/H-AN-001_archive_page.md` 实测 404）。
4. 上游口径：clear_report 残留豁免表已列（「字节归档（R6C/R8 口径）| 0 | 29」）。

**首轮勘误**：首轮报告 §1 将该件并入「他卡历史 37 / PB live 21」叙述，而 class_WS.txt/class_PB.txt 实际各含 1 条 LIVE 行（首轮未显式登记）；本轮更正为显式豁免登记（除该件外 WS 他卡类 36、首轮 PB LIVE 实为 22 行）。结论方向不变（非本链引入、非本链应处理、字节留存正确）。

### 9.2 官方 parity + 远端 + 全量见证器（复跑 §5）

- `python3 tools/check_repo_parity.py --json`（03:14:48）：**CONTENT_DIFF 0**（both_sides 2268 = identical 2268，逐字节一致）；only_workspace 8 条 = 本 QA pair 2 件（未跟踪在途；随本次镜像闭环，回执见本卡评论）+ W4/W6 他链报告 6 件（船长预期内）；only_publish 0。
- `git ls-remote origin main` = `de1b0eba05c49ea87a3f19e7370ea8e8e06c80fe` = 发布仓本地 HEAD（无并行写者）。
- `python3 verify_azj345_clear.py`（全量，非 --quick，03:16:55 完成）：**18/18 PASS，rc=0**（scan.workspace.live_zero、scan.publish.live_zero、counts.*、archive.*、registry.*、reverse.*、parity.key_files 全 PASS）。
- 证据：parity2.json、parity2.err、verifier_full2.log。

### 9.3 公开面复测（curl，含正对照）

- 正对照（探测面有效性）：`/figures/AE-FED-001/` 200、`/data/figures/AE-FED-001.json` 200、`/minds/H-HZX-002/` 200。
- 目标面：`/figures/H-AZJ-345/` **404**、`/minds/H-AZJ-345/` **404**、`/data/figures/H-AZJ-345.json` **404**；归档面 `/data/figures/_duplicates/H-AN-001_archive_page.md` 404（归档不上线）。
- live 数据面：`sitemap.xml` 1,388 条 loc / AZJ 码与名 0；`figures.index.json` 1,056 条 / 0；`index.unified.json` 1,371 条 / 0；`meta.json` 200（figures=1056、figure_shards=1056）。
- 证据：curl2.log、sitemap_live.xml、fi_live.json、uj_live.json、meta_live.json、livecheck 输出。

### 9.4 结论更新

船长裁定 8 条逐条闭环：异议 1/2 经补正卡 t_6acd458b 全链 push 闭环（复验实测 ls-remote=de1b0eb、parity CONTENT_DIFF 0、公开面 404 生效）；异议 3 追认接受（刷新面 +38 属站点产物自然刷新，数据层零越界）；异议 4/5/7 登记不阻断；异议 6 归子卡 t_fdc1589e；异议 8 随补正同步、复验确认。复验复跑全绿（§9.1-9.3），新增 1 件受控归档显式豁免与首轮计数勘误（§9.1a）。**验收结论：通过。**
