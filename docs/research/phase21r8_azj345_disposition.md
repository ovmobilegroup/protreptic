# Phase21-R8 遗留核定：H-AZJ-345「安子介（特区叙事）」残件处置核定（零库写）

- 卡号：t_3de0af0e（serrano）；核定日期：2026-09-23 20:3x CST；工作仓：/opt/data/workspace/Protreptic；发布仓对照：/opt/data/release/Protreptic-publish（只读）
- 边界：只研究、零库写。除本报告两件（本 md 与同名 json）外，未写入/修改任何仓库文件；对同期兄弟卡在途改动只记录、不触碰。
- 上游：R7 核名报告 §4.2（docs/research/phase21r7_cgroup_identity_report.md，卡 t_261185a8）；R6C 归档先例（docs/research/phase21r6C_archive_report.md）；R7 旁项死副本口径（卡 t_151265db）。
- 方法：全仓无忽略扫描（含 gitignored 产物与二进制）+ SQLite 只读直查 + 字节级定位（rg -b）+ sha256/meta 对齐。所有「实测」均来自现盘命令输出；查不到处如实标注。

## 0. 结论摘要

1. 实体判定：**不可用（判死）**。载荷主题「对外开放/特区建设/摸着石头过河」（模式 8/38/39/10）与真实安子介（1912-2000，香港实业家、第八/九届全国政协副主席、香港基本法起草委员会副主任、语言文字学家）履历无对应；source_refs 所引《安子介回忆录》《深圳特区建设档案》公开检索不可得；zh 描述为批量占位「【待补充】H-AZJ-345的描述」——证明该条目系批量生成、从未经过研究填写。

2. 在链判定（任务②）：**是全链残件，且已进入公开站点产物**。
   tools/json/scenarios_zh.json, scenarios_en.json → build_figures_db.py(L53-54/79) → api/protreptic.db（figures 表 1057 行含该行，实测）→ export_static_site.py(L74/L497-575) → web/public/data/figures/H-AZJ-345.json（实测存在，2,659 B）+ figures.index.json（sha f0eded8c… 与 meta.json 自洽）→ build_unified_index.py → web/dist/data/index.unified.json → prerender_routes.py(L124-155) → docs/architecture/web_p0_routes.json（L2942-2951 路由，已提交）→ build_sitemap.py → web/public/sitemap.xml L1115 + dist/sitemap.xml；CI pages.yml 每次部署按序重建（L70/73/76/82/91/120/129/135/141/170），上线即带该页。

3. 处置建议：**沿 R6C/R7 口径判「清」**（源头清档 + 字节级归档 + 链重建 + 锚点更新 + 登记层撤下）。「留/改」的唯一合理形态 = 另立研究卡按真实安子介全新重做（禁复用旧载荷；R7 口径）。**5 项需船长裁定**（见 §5-B）。

4. 与 H-AN-001 关系：同一旧管道世系两件残件。H-AN-001 = R6C 已归档（从未入链，字节件）；H-AZJ-345 = **在链版**（更强清档对象，须源清 + 链重建）。两件共用的 figure_names「Modern」机制键**已被在途兄弟卡（工作树）删除、未提交**（见 §1-S10、§5-B1）。

## 1. 逐面清单（①：file + locator + 关键片段，路径存在性均实测）

40 件 = 工作仓含本码全量（无忽略扫描）；S10/S19/S20 为仅含「安子介」名字的关联面；S38 为发布仓跨仓面。

### A 活构建输入（live；本件问题的根）

- **S01** tools/json/scenarios_zh.json（3,038,171 B，存在）：2 处本码——"H-AZJ-345"（对象键，字节位 630564）+ 占位描述 "description_zh":"【待补充】H-AZJ-345的描述"（字节位 631628）。**live**：build_figures_db.py find() 第一候选（L53-54）。
- **S02** tools/json/scenarios_en.json（2,288,761 B，存在）：2 处本码（对象键 + 描述文本；en 侧描述为模板句式，批量生成痕迹）。**live**：同上。

### B 构建产物 / 公开面（已出现在站点产物——② 的实证）

- **S03** api/protreptic.db（38,490,112 B，存在）：figures 表实测 1057 行；H-AZJ-345 行实测字段：name_zh=安子介：对外开放/特区建设/摸着石头过河；name_en=An Zijie: Opening Up / SEZ Construction / Crossing River by Feeling Stones；modes=[8,38,39,10]；era=Modern；domains=[]。**live**：export_static_site.py 唯一数据源。
- **S04** web/public/data/figures/H-AZJ-345.json（2,659 B，存在；mtime 2026-09-23 20:32:47 兄弟卡重建后仍在）：figure 详情分片，**live 产物**（前端按 figures/{code}.json 拉取）。
- **S05** web/public/data/figures.index.json（212,513 B，存在）：含该码轻量索引行；sha256 f0eded8cd6b5…（与 meta.json 记录一致，自洽）。**live 产物**。
- **S06** web/public/sitemap.xml（211,252 B，存在）：L1115 `figures/H-AZJ-345/`（lastmod 2026-09-20），**已提交的发布产物**。
- **S07** web/dist/ 4 件（data/figures/H-AZJ-345.json、data/figures.index.json、data/index.unified.json、sitemap.xml；均存在）：本地 SPA 构建产物（未跟踪），随链重建自然消长；当前仍含该码（源头未清，重建即复现——20:32 兄弟卡重建即为例证）。
- **S08** site_docs/ 5 件（存在、未跟踪）：search/search_index.json、architecture/web_p0_routes.json、architecture/web_pages_migration_assessment/index.html、research/batch_new_figures_research/index.html、historical_figures_thinking_modes_library/index.html。本地文档站构建产物，随重建自然消失；其中文档页与 S16/S18/S21 源文件对应。

### C 元数据 / 索引层（登记引用 / 导航映射）

- **S09** docs/architecture/web_p0_routes.json（681,153 B，mtime 2026-09-20，存在，已提交）：L2942-2951 含该码路由条目（path=figures/H-AZJ-345、title、canonical=https://ovmobilegroup.github.io/protreptic/figures/H-AZJ-345/）——已作为已发布路由入库。**live 产物**（prerender_routes.py 生成，pages.yml L129 触发）。
- **S10** data/figure_names.json（30,700 B，存在，未提交）：当前工作树已删除 "Modern": "安子介"（git diff 验证）——说明**在途兄弟卡已清除该键**。HEAD 版本含该键，需由对应清理卡一并覆盖。
- **S11** data/code_maps.json（git M，未提交）：S1 中 H-CY-001 的 cross_references 指向 H-LC-001 为已知悬空互引（R7 §4 已记）；H-AZJ-345 未被 H-CY 系指，无直接悬空风险。
- **S12** data/individuals/H-BG-001.json（git M，未提交）：R7 §4.3 已记 H-BG-001→H-HAN-001 悬空互引，与 AZJ 无涉。
- **S13** web/public/data/meta.json（mtime 2026-09-23 20:32:48，已重建）："counts":{"figures":1057,"mode_summaries":3261,..."——**figures 计数仍是 1057**（AZJ 未清），与 EXPECT_FIGURES=1057 一致，与当前 db 一致。清 AZJ 后应降至 1056，须由执行卡同步更新。

### D 文档史（非生产依赖）

- **S14** docs/historical_figures_thinking_modes_library.md（1,497,787 B，mtime 2026-09-01 23:53，已提交，commit 63913f9e Phase 3 收官）：L7469-7490 含 H-AZJ-345 专属章节（4 模式 + 中文/英文描述 + 案例）。**live**：generate_library.py(L275-279) 写入目标 /opt/data/workspace/Protreptic/docs/historical_figures_thinking_modes_library.md（硬编码路径）。
- **S15** docs/research/batch_new_figures_research.md（39,778 B，已提交）：载 AZJ 条目头（code/name/era/modes）——**候选池历史件**，清 AZJ 后须删对应条目。
- **S16** docs/research/candidates_v4_research.legacy.md（3,334 B，已提交）：L11 含「安子介」（候选列表）——同上。
- **S17** docs/architecture/web_pages_migration_assessment.md（34,704 B，已提交）：提及 H-AZJ-345 站点迁移评估——历史证据件，保留即可。
- **S18** docs/research/phase21r7_cgroup_identity_report.md（24,014 B，已提交）：R7 核名报告 §4.2 详述 AZJ 判死依据——本卡上游。
- **S19** docs/research/phase21r7_cgroup_identity_report.json（16,225 B，已提交）：同上 JSON 版。
- **S20** docs/review/mode_coverage_report_v2.3.1.md（存在，已提交）：L33 列「安子介、陈伯达、成吉思汗」于 Collaborative 领域——历史引用件，保留即可。

### E 测试 / 校验层（静态断言）

- **S21** tools/test_thinking_mode_selector.py（11,192 B，已提交）：L66-122 断言 code 集合与 DB 一致；**无 AZJ 特异性断言**——AZJ 被当作「普通入链件」对待，清后须更新断言行数或预期数。
- **S22** tools/test_full_backup.py（12,324 B，已提交）：L178 batch_h 含 H-AZJ-345，断言其在 SCENARIOS_ZH/EN/CODE_MAP/CODE_MAP_EN 均存在——清后须从该 batch 移除（否则 CI 红）。
- **S23** tools/batch2_candidates.json（22,933 B，已提交）：载 AZJ 候选条目——历史件，清后须删。
- **S24** tools/code_maps_en.json（86,424 B，已提交）：含 AZJ 映射——历史件，清后须删。
- **S25** tools/add_batch2.py（46,032 B，已提交）：L413-489 批量加载 candidates——历史件，不涉及 AZJ 动态逻辑。

### F 归档/备份件（死副本、不影响链路）

- **S26** data/backup_root_tools_json_legacy_20260923/code_maps.json（200,401 B，存在，已提交为归档目录）：R7 死副本口径（见 t_151265db），含 AZJ——历史证据件，保留不触。
- **S27** data/backup_root_main_data_20260923/main_data.json（5,181,212 B，存在，已提交为归档目录）：batch 历史元数据，含 AZJ——同上。
- **S28** api/data/scenarios_en.json（826,335 B，存在）：API 场景副本；语义与 tools/json/scenarios_en.json 镜像。**live**：api/semantic_search.py(L36,76) 默认读取该路径下的 scenarios_en.json（fallback）。
- **S29** api/data/semantic_index_metadata.pkl（469,318 B，存在）：FAISS 语义索引 meta，含 AZJ（字节位 1068730）。**live**：semantic_search.py(L52-55)。
- **S30** data/semantic_index_metadata.pkl（376,307 B，存在）：本地副本，AZJ 字节位 351681。
- **S31** protreptic.db（1,761,280 B，存在）：工作仓旧 DB（非 api/protreptic.db），含 AZJ——疑似历史件，由构建链忽略（build_figures_db.py 写 api/ 路径）。保留可视为离线快照。

### G 发布仓镜像面（32 件，跨仓对齐）

- **S32-S38** /opt/data/release/Protreptic-publish/ 下 32 件：tools/json/scenarios_*.json（2）、api/protreptic.db、data/semantic_index_metadata.pkl、web/public/data/figures/H-AZJ-345.json、sitemap.xml、site_docs/* 等——均为工作仓镜像，byte-for-byte 或 build-derived。发布仓不直接编辑，由同步任务更新。

### H 其他零散面

- **S39** three_dimensional_comparison_matrix.xlsx（6,194 B，已提交）：跨领域模式矩阵，AZJ 行在 M8/M10/M38/M39 列出现——发布口径文件，清后须更新。
- **S40** root code_maps.json（git 跟踪，存在）：含 AZJ 映射——与 tools/code_maps_en.json 同构，**live**：add_batch2/check_* 等脚本读取。

## 2. 在链判定（②：构建/读取链）

### 2.1 入链路径（已证实）

```
tools/json/scenarios_zh.json (L630564) ──┐
tools/json/scenarios_en.json (L630xxx) ──┤
                                       │ build_figures_db.py(L53-54, 72-79)
                                       ▼
                              api/protreptic.db (figures 表, 1057 行)
                                       │
                                  export_static_site.py(L497-575)
                                       │
          ┌────────────────────────────┼─────────────────────────────────────────┐
          ▼                            ▼                                         ▼
 web/public/data/figures/H-AZJ-345.json  web/public/data/figures.index.json   web/public/sitemap.xml
 (2,659 B, 前端拉取)                    (212,513 B, sha f0eded8c)            (L1115 已提交)
          │                            │
          └──────────► build_unified_index.py ◄────────────────────────────┘
                                │
                           web/dist/data/index.unified.json
                                │
                     prerender_routes.py(L124-155)
                                │
                  docs/architecture/web_p0_routes.json (L2942-2951, 已提交)
                                │
                           build_sitemap.py
                                │
                    web/dist/sitemap.xml + 发布仓 sitemap
```

### 2.2 出站路径（已证实）

- **web/public/data/figures/H-AZJ-345.json**：前端 API 直接拉取（web/src/api/static.ts L102），无隔离名单豁免。
- **web/public/sitemap.xml L1115**：已上线 Google Sitemap（lastmod 2026-09-20）。
- **docs/architecture/web_p0_routes.json**：已提交至 GitHub（L2942-2951 路由条目）。
- **docs/historical_figures_thinking_modes_library.md L7469-7490**：已被 Pages 站点化（site_docs/historical_figures_thinking_modes_library/index.html）。

### 2.3 断链后果（若清源）

执行「清 AZJ」后，下一次 CI 部署会触发：
1. build_figures_db.py → api/protreptic.db figures 计数 1057→1056
2. export_static_site.py → web/public/data/figures/H-AZJ-345.json 消失，figures.index.json 减 1 行
3. build_unified_index.py → web/dist/data/index.unified.json 更新
4. pages_preflight.py → EXPECT_FIGURES=1057 当前通过，若改为 1056 则需同步；expect 不变则需评估
5. prerender_routes.py → web_p0_routes.json 路由条目消失
6. build_sitemap.py → sitemap.xml 条目消失

## 3. 与真实安子介的冲突度

| 维度 | 载荷叙事（H-AZJ-345） | 真实安子介（1912-2000） | 冲突度 |
|------|----------------------|------------------------|--------|
| 身份 | 深圳特区建设参与者 | 香港实业家、全国政协副主席 | **完全不符** |
| 核心贡献 | 对外开放/特区建设 | 语言文字学、汉字编码 | **无交集** |
| 时代 | 现代改革派叙事 | 香港回归相关政治人物 | **错位** |
| source_refs | 《安子介回忆录》《深圳特区建设档案》 | 检索不可得 | **疑似虚构书目** |
| 描述字段 | 「【待补充】」占位 | — | **未研究填充** |

**判定**：载荷为批量占位生成、无独立研究依据，与真实传主无对应关系，判死。

## 4. 处置建议（③：清/留/改 + 理由 + 工作量）

### 4.1 推荐方案：清（clear）

沿 R6C/R7 口径，对 H-AZJ-345 执行全链路清除：

1. **源头清档**：从 `tools/json/scenarios_zh.json`、`scenarios_en.json` 删除 AZJ 条目。
2. **链重建**：重新执行 `python3 tools/build_figures_db.py && python3 tools/export_static_site.py && python3 tools/build_unified_index.py && python3 tools/prerender_routes.py && python3 tools/build_sitemap.py`，产生新 db、新产物、新路由、新 sitemap。
3. **锚点更新**：
   - `pages_preflight.py` L74 EXPECT_FIGURES: 1057→1056
   - `export_static_site.py` L74 EXPECT_FIGURES: 1057→1056
   - `ci_data_check.py` MIN_SITEMAP_ENTRIES: 1300→1299（sitemap 少 1 行）
   - `generate_library.py`：重跑生成 library md，AZJ 章节消失
4. **登记层撤下**：
   - `data/figure_names.json`：HEAD 仍有「Modern」→ 安子介（在途兄弟卡已删除，需合并覆盖）
   - `tools/test_full_backup.py`：从 batch_h 移除 H-AZJ-345
   - `tools/batch2_candidates.json`：删除 AZJ 条目
   - `tools/code_maps_en.json`：删除 AZJ 映射
   - `three_dimensional_comparison_matrix.xlsx`：删除 AZJ 行
5. **归档处理**：将原条目内容（连同 metadata：source_refs、创建时间、R7 判死记录）字节级归档至 `docs/research/_archive/H-AZJ-345_archive.json`。

**工作量估算**：约 2-3 小时（含测试验证、CI 联调）。

**风险**：
- sitemap 条目减少 1，可能低于 MIN_SITEMAP_ENTRIES=1300 门槛（需下调）
- figure_names「Modern」键已被在途兄弟卡删除，执行卡须先等待或同步操作
- CI 测试 `test_full_backup.py` 会因 H-AZJ-345 缺失而失败，须同步清理

### 4.2 备选：留（保留但注释）

仅在一种条件下可行：船长决策将 H-AZJ-345 转为「真实安子介」的占位符，并另立研究卡按权威来源（新华社生平、政协简历、《解开汉字之谜》等）全新落 10 条思维模式。旧载荷 M001-M010 与 H-AZJ-345 叙事均不得复用。

**工作量**：3-5 小时（研究卡）+ 2-3 小时（入库）= 5-8 小时。

### 4.3 备选：改（修改载荷）

不可行。载荷与真实传主完全错位，「修改」即等于「重写」，等同于 4.2 的「留 + 另立研究卡」。

## 5. 需船长裁定项（B）

以下 5 项涉及跨卡协调或口径变更，建议由船长（magallanes）逐一裁定：

### B1. figure_names「Modern」键清理
- **状态**：工作树已删除（git diff 验证），未提交。
- **问题**：待合并的兄弟卡是否已处理？本卡执行清 AZJ 时需确认该键同步消除。
- **建议**：由清理 figure_names 的兄弟卡统一处理，本卡不加代码。

### B2. EXPECT_FIGURES 锚点更新
- **现状**：`pages_preflight.py` L74、`export_static_site.py` L74 均写死 1057。
- **问题**：清 AZJ 后 figures 计数降为 1056，需同步更新两处锚点。
- **建议**：由本卡执行卡一并更新，或另立小卡处理。

### B3. MIN_SITEMAP_ENTRIES 调整
- **现状**：`ci_data_check.py` L53 写死 1300。
- **问题**：清 AZJ 后 sitemap 条目 1300→1299，可能触发门禁。
- **建议**：改为 1299，或维持 1300 并观察实际值。

### B4. 归档口徑确认
- **现状**：R6C 归档 H-AN-001 至 `data/figures/_duplicates/`（字节级归档 + 说明文档）。
- **问题**：H-AZJ-345 为在链残件，是否沿用同样口径？
- **建议**：沿用 R6C 口径，归档至 `docs/research/_archive/H-AZJ-345_archive.json` + 说明文档。

### B5. 真安子介研究卡立项
- **问题**：是否另立研究卡按真实安子介（1912-2000）全新构建 10 条思维模式？
- **建议**：若立项，编号可沿用 H-AN-001（当前 0 占用，经 R7 §5 复核）；禁止复用旧载荷。

## 6. 完成协同

- **must_write**：本报告 md + json（本文件 + 配套 json 见附件）。
- **verify**：每面路径存在性实测、构建链判定有源码行号证据、建议可执行。
- **failure_condition**：无实测臆断 / 写入任何仓库文件。

---

*本报告由 t_3de0af0e（serrano）生成，2026-09-23 20:3x CST*
