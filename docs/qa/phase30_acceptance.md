# Phase30 终审报告（C4）——全站端到端回归 + 发布验收

- 卡片：`t_f79fe23e` [Phase30-C4] 终审：全站回归 + 发布验收（assignee: espinosa）
- 线上站点：https://ovmobilegroup.github.io/protreptic
- 仓库：dev `/opt/data/workspace/Protreptic`（master，本地） / publish `/opt/data/release/Protreptic-publish`（origin main，驱动 Pages）
- 验收基线：workspace `b089136f` / publish `e5103dc`
- 线上产物指纹：`assets/index-CE7EoPzT.js`（sha256 `e05d3b97d404...`，与本地 `web/dist/assets/index-CE7EoPzT.js` 逐字节相同）；`sw.js` BUILD_ID `d131673f513e`
- 本轮 Pages 部署：run **35349687457 success**（4m17s，数据基线修复后）+ 报告提交后一次 success；Quality Gate：run **35351209916 success**（3 个 job 全绿）

---

## 0. 结论（是否可发布）

**结论：可以发布（PASS，带 2 项存量 CI 红与若干遗留数据质量问题，均不阻塞站点发布）。**

判定要点：

1. 站点在真实浏览器 + 线上 live 环境逐路由实测通过：线上 1359 条 URL 可达性 **1359/1359 PASS**（0 死链），sitemap 与路由清单一致，浅深色/移动端/搜索/图谱/对比/每日/模板导出/PWA 全部实测可用。
2. 本卡在验收过程中发现并**修复了 4 个真实阻塞项**，它们直接决定「线上到底是不是可交付状态」：
   - **B1** `quality-gate.yml` 含重复 job 键，GitHub 判定工作流非法，C1 的质量门自 `d72e25b` 起**从未真正运行**（每个 push 只有一个 0 job 幻影失败）。
   - **B2** t_dd99310c 的数据修复只落在 workspace，发布仓仍是脏数据，每次 CI 重新生成线上产物时把缺陷带回来：线上 `/minds/H-SUN-001/` 是 404 空壳页，sitemap 有 2 条 `<loc>` 带裸空格。
   - **B3** 清理脏记录后 figures 口径 1058 变 1057，但 `EXPECT_FIGURES` 常量未同步，**Pages 部署被断言卡死失败**，线上停留在旧版本。
   - **B4** 质量门恢复运行后 `data-check` job 仍失败：该 job 从不构建 SPA，`prerender_routes.py` 找不到 `web/dist`。
3. 修复后复核：B2 的线上症状全部消失（`/minds/H-SUN-001/` -> 200 且渲染 10 条模式；`/minds/Sun%20Quan/`、`/figures/code%20field/` -> 404 退出；sitemap 裸空格 0），B3 后 Pages 部署成功，B1 后质量门恢复真实执行，B4 修复后首次**三 job 全绿**（run 35351209916：data-check 24/24、live-links 1359/1359、Lighthouse success）。
4. 未达标但**不影响站点发布**的存量项：`markdown-lint`（CI）与 `ci-cd` 的 Python 测试长期红（根因已定位，见 R1/R2），以及数据语义层问题（R3 到 R9）。这些不是 Phase30 A/B/C 交付本身的功能缺陷，建议单独排卡。

---

## 1. 交付面（A/B/C）覆盖核对

| 交付 | 代表产物（真实路径） | 本次验收方式 | 结论 |
|---|---|---|---|
| A 系列：SEO/预渲染/PWA/搜索/图谱数据 | `tools/prerender_routes.py`、`tools/build_sw.py`、`tools/build_search_index.py`、`tools/build_graph_data.py`、`web/public/manifest.webmanifest` | 线上 HTTP + 浏览器 DOM + 线上 `sw.js`/`manifest` 内容 | PASS |
| B 系列：图谱 UI/对比/每日/模板导出 | `web/src/views/GraphView/`、`CompareView.vue`、`DailyView.vue`、`TemplateDetailView.vue` | 本地 `vite preview` 真实 DOM + 点击行为 + 线上复测 | PASS |
| C 系列：质量门/文档站主题/统计 | `.github/workflows/quality-gate.yml`、`tools/ci_data_check.py`、`tools/ci_link_check.py`、`docs_overrides/` | GitHub Actions 真实运行结果 + 脚本本地复跑 | PASS（修复后） |

---

## 2. 构建与 CI

| 项 | 结果 | 证据 |
|---|---|---|
| `cd web && VITE_DATA_MODE=static npm run build` | **PASS** | vue-tsc 0 error，137 modules，`dist/assets/index-CE7EoPzT.js` 339.22 kB（gzip 123.95 kB） |
| 本地构建产物 == 线上产物 | **PASS** | 两侧 `index-CE7EoPzT.js` sha256 `e05d3b97d404326395be376ab9021c142455c095dd3c0ba9f1975e1d3e71d81e` |
| Pages 部署（`pages.yml`） | **PASS** | run 35349687457 `success` 4m17s（修复 B3 前为 failure 18s，断言 `figures 条数 1057 != 1058`） |
| Quality Gate（`quality-gate.yml`） | **PASS** | run **35351209916 success**：`data-check` **success**（24 条断言 0 失败：名录 1338 = 人物 283 / 场景 1055、路由 1353、sitemap 1354 = 路由 + 首页）、`live-links` **success**、`Lighthouse` **success**。该门自 `d72e25b` 起从未真正运行（见 B1），本次是恢复后第一次跑完且全绿 |
| `CI`（markdown-lint） | **FAIL（存量，非本阶段引入）** | run 35349687441 failure，违规集中在 `docs/**`、`data/figures/**` 与 B5 新增的 `web/public/templates/*.md`，见 R1 |
| `Protreptic CI/CD` | **FAIL（存量，非本阶段引入）** | run 35349687510 failure，步骤 `Run Python tests`：`assert len(SCENARIOS_ZH) == 1008` 实测 39，见 R2 |

CI 红对照（证明不是本卡引入）：`markdown-lint` 与 `ci-cd` 的失败在 2026-09-17 23:46 的 run（`41c73ba0`）就已存在；本次唯一新增的红是 B1/B3 造成的**门失效**与**部署卡死**，两者均已修复。

---

## 3. 逐路由回归（本地 `vite preview --base=/protreptic/ --port 4210` + 线上）

本地逐路由渲染（真实 DOM，非截图）：

| 路由 | HTTP | 正文字符数 | article 卡数 | 标题 |
|---|---|---|---|---|
| `/` 转 `/figures` | 200 | 4753 | 25 | 以人为鉴，明得失 |
| `/modes` | 200 | 16156 | 120 | 思维模式库 |
| `/concepts` | 200 | 2007 | 60 | 概念索引 |
| `/graph` | 200 | 2853 | - | 关系图谱 |
| `/compare`（空态） | 200 | 356 | - | 跨人物对比 |
| `/templates` | 200 | 598 | 7 | 复盘模板库 |
| `/daily` | 200 | 2761 | 1 | 每日一模式 |
| `/api` | 200 | 1114 | - | 数据与 API |
| `/minds/H-WYM-001` | 200 | 3115 | 10 | 王阳明 |
| `/templates/longzhong` | 200 | 5131 | 1 | 隆中对复盘模板 |
| `/no-such-page-xyz` | 200（SPA 404 页） | 281 | - | 这一页不在典藏里 |

线上 HTTP（`curl -L`，20 条关键 URL）：`/`、`/figures/`、`/modes/`、`/concepts/`、`/graph/`、`/compare/`、`/daily/`、`/templates/`、`/templates/longzhong/`、`/api/`、`/minds/H-WYM-001/`、`/minds/QIU/`、`/robots.txt`、`/sitemap.xml`、`/manifest.webmanifest`、`/sw.js`、`/404.html`、`/data/index.unified.json`、`/templates/longzhong.md`、`/assets/index-CE7EoPzT.js` **全部 200**；未知深链 `/minds/NOPE-999/` -> **404 + SPA 外壳**（3904 B，深链兜底符合设计）。

线上深链数据（修复 B2 后）：`/minds/H-SUN-001/` -> **200 / 27771 B**，浏览器实测 `title=孙权 - 思维模式档案 10 条`、`h1=孙权`、10 个 article；`/data/modes/by-figure/H-SUN-001.json` -> 200 / 20767 B。

---

## 4. 功能项实测（本地真实浏览器 DOM + 交互）

| 项 | 结果 | 证据 |
|---|---|---|
| 搜索 | **PASS** | `/figures` 输入框 `input.pt-input`；`致良知` -> 9 卡、`M381` -> 1 卡、`王阳明` -> 8 卡、乱码 `不存在的字符串zzz` -> 回退全量 25 卡（无空白页） |
| 图谱三视图 | **PASS** | `人物-模式-概念` 23 节点/23 边；`模式关联` 23 节点/22 边（正文 63260 字符）；`全局模式网络` K=60 -> 60 节点/36 边；`节点数（按度数取前 K）` 下拉 20/40/60/80 生效 |
| 对比（4 项） | **PASS（含已记录的边界行为）** | `/compare/?items=H-WYM-001,H-KONG-001,M-MF-004,M-QIU-001` -> `已选 4 / 4 项`、3 张表（总览 10 行、领域分布 11 行、并排对照）、共同概念区块齐全；无效 code 显式提示 `无法解析（编号不存在或为场景条目）：H-KONG-001`，不渲染空列 |
| 每日一模式 | **PASS** | 首页模块 + `/daily`：2026-09-18（周五）-> `M-FYJ-009 时务人士监督法`（福泽谕吉），与 B6 P1 QA 记录一致 |
| 模板库/导出 | **PASS** | `/templates` 7 张卡；`/templates/longzhong` markdown 渲染进 `.pt-prose`（4846 字符）；点击「下载 Markdown 11.8 KB」**真实下载成功**（`/tmp/c4/dl/longzhong.md` 12033 B，sha256 `03efa9ff49bf...` 等于仓库 `web/public/templates/longzhong.md`）；「打印 / 导出 PDF」点击触发 `window.print()`（计数 1）；`Emulation.setEmulatedMedia('print')` 下 `.pt-print-only` 显式显示 |
| PWA | **PASS** | `manifest.webmanifest` 200（name/short_name/`start_url=./`/`display=standalone`/theme `#04060c`/4 个 icon）；线上 `sw.js` 200 / **11433 B 真实 SW**（注释头 `Protreptic service worker (Phase30-A4)`），非 SPA 兜底 HTML；`404.html` 为 SPA 外壳副本 |
| 浅色/深色 | **PASS** | 点击主题按钮：`data-theme=light`，body 背景 `rgb(4,6,12)` 变 `rgb(248,245,240)`，正文色 `rgb(243,236,224)` 变 `rgb(32,28,22)`，卡片 `bg-white/...` 随 `--pt-overlay` 反向；`localStorage['protreptic-theme']='light'` 跨页持久（`/modes` 重载后仍为 light），切回深色正常 |
| 移动端 390x844 | **PASS** | `/figures`：`scrollWidth=390`、无横向溢出，25 卡 + 导航正常；`/compare/?items=H-WYM-001,QIU`：`scrollWidth=390`、3 张表可读（正文 11599 字符） |
| 站内可达性（独立复跑门的脚本） | **PASS** | `python3 tools/ci_link_check.py live --crawl-sample 8`：检查 **1359 条，失败 0 条**（修复前为 1361 条检查 / 2 条失败：`/minds/H-SUN-001/` 404、`/figures/KG-AKA-001/` 一次 SSL 抖动） |
| 数据一致性 | **PASS** | 线上 `index.unified.json`：`total 1338 / figures 283 / scenarios 1055 / with_modes 1302`，**空白 code 0 条**，`H-SUN-001` 在列、`Sun Quan` 已下线；线上 `sitemap.xml` 1354 条 `<loc>`，**裸空格 0 条**；线上 283 个 figure 分片逐个 GET **全部 200** |

---

## 5. 本卡修复清单（均已提交两仓）

| # | 问题 | 根因 | 修复 | 提交 |
|---|---|---|---|---|
| B1 | Quality Gate 自 `d72e25b` 起**从未运行**（每个 push 只有 0 job 幻影失败，workflow 名退化成文件路径） | `quality-gate.yml` 被重复追加了 `lighthouse` 与 `data-check-and-links` 两个 job（同一 YAML 映射键出现两次），GitHub 判定文件非法 | 删除重复块，保留 canonical 三 job（`data-check` / `live-links` / `lighthouse`），本地 YAML 校验 job 键唯一 | workspace `a1674724` / publish `38e3d1f` |
| B2 | 线上 `/minds/H-SUN-001/` 404 空壳页；`/minds/Sun%20Quan/`、`/figures/code%20field/` 才是「真页面」；sitemap 2 条 `<loc>` 带裸空格 | t_dd99310c 的清洗只落在 **workspace**，发布仓 `data/modes_data.json`（10 条 M-SUN 的 `figure_code='Sun Quan'`）、`data/figure_names.json`、`data/figures/H-SUN-001.json`、`tools/json/scenarios_{zh,en}.json`、`code_maps*.json` 仍是脏版本；Pages 从发布仓重新生成，缺陷被持续带回线上 | 把 8 个源文件按内容级 diff 与 workspace 对齐（`data/modes_data.json`、`data/figure_names.json`、`data/figures/H-SUN-001.json`、`tools/json/scenarios_zh.json`、`tools/json/scenarios_en.json`、`api/data/scenarios_en.json`、`tools/json/code_maps.json`、`tools/code_maps_en.json`）；复核 publish 侧 `figure_code` 无空白值，「Sun Quan」仅存在于英文散文 | publish `5203888` |
| B3 | Pages 部署断言失败被卡死（`figures 条数 1057 != 1058`），线上停在旧版本 | 清洗后 figures 表由 1058 降为 1057，但 `tools/export_static_site.py:EXPECT_FIGURES` 与 `tools/pages_preflight.py:EXPECT_FIGURES` 仍是 1058；本地 `api/protreptic.db` 也未重建（仍 1058 行） | 常量 1058 改 1057（两仓各 2 处）；两仓 `python3 tools/build_figures_db.py` 从清洗后 JSON 重建 figures 表（1057 行、0 条空白 code）；重跑 `export_static_site -> build_daily_index -> build_search_index -> build_graph_data -> build_unified_index`，`pages_preflight --stage data` 两仓全绿 | workspace `b089136f` / publish `e5103dc` |
| B4 | 质量门恢复运行后 `data-check` job 仍失败：`[prerender] missing .../web/dist/data/index.unified.json` | 该 job 重建数据后直接调用 `prerender_routes.py`，但从不构建 SPA，`web/dist` 不存在（pages.yml 是在 `npm run build` 之后才 prerender） | job 内补 `Set up Node 20` + `cd web && npm ci && VITE_DATA_MODE=static npm run build`，并把 `timeout-minutes` 10 改 15。复核：run **35351209916** 的 `data-check` **success**（24/24） | workspace/publish `quality-gate.yml`（本报告同批提交） |

---

## 6. 遗留问题（不阻塞本次发布，建议单独排卡）

| # | 级别 | 问题 | 根因（已定位） | 建议 |
|---|---|---|---|---|
| R1 | P2 | `CI`/markdown-lint 长期红 | 门口径是 `**/*.md`，而仓库有上千条历史违规（`docs/historical_figures_thinking_modes_library.md` 单文件 824 处 MD032、`data/figures/*.md` 等）；B5 又把 7 份模板副本放进 `web/public/templates/*.md`（MD022/MD032/MD009/MD047）。`.markdownlint.json` 已关掉 MD007/009(br_spaces)/013/024 等，但没解决存量与生成副本 | 二选一：把生成副本目录（`web/public/templates/`）与历史文档目录加入 ignore，或分批格式化存量文档并收紧门 |
| R2 | P2 | `Protreptic CI/CD` 的 `Run Python tests` 长期红 | `tools/test_thinking_mode_selector.py` 断言 `len(SCENARIOS_ZH)==1008`，但 `thinking_mode_selector.py` 相对路径读到的是 `tools/scenarios_zh.json`（**39 键的陈旧副本**，仓库根同名文件也只有 93 键），而真实数据集已是 1055 场景；断言口径（1008/370/44/25/455）与现数据完全脱节 | 让 selector 读唯一数据源（`api/protreptic.db` 或 `web/public/data`），并把断言口径更新到现基线（或改成「与数据源计数一致」的派生断言） |
| R3 | P2 | `domain_zh` 语义污染：by-figure 分片 **1411/2858（49.4%）** 的 `domain_zh` 是散文叙述而非领域标签（如 `M-QIU-001` 190 字符；`M-AMP-001` 366 字符），其中 448 条以 `definition_zh` 开头 | 导出层把「案例/定义」写进了 `domain_zh` 字段（摘要索引 `modes/index-*.json` 的同名字段是干净的短标签，形成双口径） | 修导出映射（by-figure 用摘要索引同源字段），或至少在 UI（`/compare` 领域分布表头、`/minds` 卡片）加截断 |
| R4 | P3 | `/concepts` 出现可疑人物名「获取兵」「非人」 | 人物名录脏值（`figure_names.json` 缺名时回落到读音/代号），`H-FEI-001` 本身可疑 | 数据治理卡：清理 + 补 `figure_names.json` |
| R5 | P3 | 已隔离的虚构人物 `H-SX-001` 仍从概念图漏出（`concept_graph.json` 284 人物 = 283 + 1），`/concepts` 直接显示裸编号 | `QUARANTINE` 只作用于索引/每日层，图谱构建未共享该名单 | 把隔离名单抽成共享常量，图/概念层同样过滤 |
| R6 | P3 | 打印模式下 `.pt-print-only` 页脚渲染在 `y=188`（panel 内首屏）而非纸面页脚 | CSS position 未在 print 媒体下改为固定页脚 | 打印样式微调 |
| R7 | P3 | `docs_site/docs/templates/*.md` 是过期副本（`longzhong` 10505 B vs 源 12033 B） | 归档目录未随源模板更新 | 文档归档卡 |
| R8 | P3 | 文案自述数字与站内统计不一致：页脚/`meta description` 写「2868 条思维模式 x 284 位历史人物」，而站内统计为 `2858` 条 / `283` 位（`2868` 是含 10 条被丢弃项前的原始计数，`284` 是含隔离项的分片数） | 硬编码常量未与导出产物口径对齐 | 让文案从 `data/meta.json` 读取计数，或改口径说明 |
| R9 | P3 | `/figures` hero 与 `/api` 文档页写「1058 个现代处境场景 / 1058 条」，名录统计为 `1055` 场景 | 同 R8（硬编码） | 同 R8 |

---

## 7. 复跑命令（本报告所有数字均可复现）

```bash
# 构建（vue-tsc 会卡类型错误）
cd /opt/data/workspace/Protreptic/web && VITE_DATA_MODE=static npm run build

# 本地回归（真实浏览器）
cd /opt/data/workspace/Protreptic/web && npx vite preview --base=/protreptic/ --port 4210

# 线上可达性（质量门同款脚本）
cd /opt/data/workspace/Protreptic && python3 tools/ci_link_check.py live --base-url https://ovmobilegroup.github.io/protreptic --crawl-sample 8

# 数据基线（两仓同跑）
python3 tools/build_figures_db.py && python3 tools/export_static_site.py && python3 tools/build_daily_index.py \
  && python3 tools/build_search_index.py && python3 tools/build_graph_data.py && python3 tools/build_unified_index.py \
  && python3 tools/pages_preflight.py --stage data

# CI 目录
gh run list --repo ovmobilegroup/protreptic --limit 5
```

---

## 8. 结论摘要

- **站点可发布**：线上产物与本地构建逐字节一致，1359/1359 URL 可达，核心功能（搜索/图谱/对比/每日/模板导出/PWA/主题/移动端）在真实浏览器实测可用。
- **本卡修掉了 4 个真实阻塞项**（质量门失效、脏数据未同步、部署断言卡死、门内缺 SPA 构建），其中前三个直接决定「线上是否可交付」。
- **仍需跟进**：R1/R2 两项存量 CI 红（根因已定位），R3 数据字段语义污染（49.4% 模式），R4 到 R9 低级别数据/文案问题。这些不影响站点功能，但应在下一阶段排卡清理。
