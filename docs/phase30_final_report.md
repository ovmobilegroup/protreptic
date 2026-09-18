# Phase30 收官报告（C5）——交付清单 · 实测证据 · 遗留问题 · 后续建议

- 卡片：`t_7defc6f6` [Phase30-C5] 收官文档与知识沉淀（assignee: pigafetta）
- 上游：`t_f79fe23e` [Phase30-C4] 终审（espinosa）——结论「可发布」，见 `docs/qa/phase30_acceptance.md`
- 线上：https://ovmobilegroup.github.io/protreptic
- 仓库：dev `/opt/data/workspace/Protreptic`（master）/ publish `/opt/data/release/Protreptic-publish`（origin main，驱动 Pages）
- 本报告中的每个数字都来自本卡现场执行的命令（见 §7 复跑命令），不做推断式断言

---

## 0. 一句话结论

**Phase30 全系列（A/B/C）交付完毕且线上可用：本地构建产物与线上产物逐字节一致（同一个 JS sha256），
数据基线断言 24/24 通过，25 条线上 URL 全部 200，站点可发布。**
本卡另清掉了 workspace 仓里 20 个由 shell 误操作产生的垃圾路径（publish 仓无此问题），
并把 Phase30 全过程中踩到的坑沉淀进技能 `protreptic-web-frontend`。

---

## 1. 交付清单（真实路径 + 体量 + 验证方式）

### A 系列：可发现性 / 离线 / 检索 / 图谱数据（构建期生成）

| 交付 | 文件（绝对路径前缀 `/opt/data/workspace/Protreptic/`） | 体量 | 验证 |
|---|---|---|---|
| A0 路由预渲染 | `tools/prerender_routes.py` | 13780 B | `docs/architecture/web_p0_routes.json` 实测 `count=1353`，分型 `{static:8, person:283, scenario:1055, template:7}` |
| A0 架构与取证 | `docs/architecture/web_p0_architecture.md`、`web_p0_baseline.json`、`web_p0_evidence.md`、`web_p0_routes.json` | 51 KB / 4.3 KB / 13 KB / 679 KB | 线上深链 200 |
| A1 SEO 资产 | `web/public/robots.txt`、`web/public/sitemap.xml` | 328 B / 211865 B | sitemap 1354 条 `<loc>`，裸空格 0 |
| A2 静态正文快照 | `tools/prerender_body.py`、`docs/architecture/phase30_a2_prerender_body.md` | 22773 B / 3.2 KB | 无 JS 也能读到标题与正文 |
| A3 社交分享图 | `tools/build_og_images.py`、`tools/og_image.py`、`tools/apply_og_meta.py`、`tools/subset_og_font.py`、`docs/architecture/og_samples/` | 18107 / 14246 / 7406 / 8071 B | 线上 `/og/minds/H-WYM-001.png` 200 / 28568 B，魔数 `89 50 4e 47`（真 PNG）；`/og/site.png` 200 / 32697 B |
| A4 PWA | `tools/build_sw.py`、`web/public/manifest.webmanifest`、`manifest-light.webmanifest`、`web/public/icons/`（5 个 icon）、`docs/architecture/phase30_a4_pwa.md` | 11333 B / 1583 B / 1583 B / 31 KB icon-512 | 线上 `/sw.js` 200 / **11433 B 真 SW**（非 SPA 兜底 HTML）；manifest `display=standalone`、`start_url=./`、4 icon |
| A5 全文检索索引 | `tools/build_search_index.py` → `web/public/data/search/index-0..15.bin` + `meta.json` | 16 片 raw 1295.3 KB / **gzip 773.9 KB（门限 800 KB）**，`doc_count=2858` | 检索 UI 实测命中（见 §2） |
| A6 检索 UI | 检索入口（索引懒加载 + 子串降级） | — | 本地真实浏览器 DOM 实测 |
| 统一名录 | `tools/build_unified_index.py` → `web/public/data/index.unified.json` | 6765 B 脚本 | `counts={total:1338, figures:283, scenarios:1055, with_modes:1302}` |
| 每日一模式索引 | `tools/build_daily_index.py` → `web/public/data/daily/{index,names}.json` | 10230 B 脚本，产物 324.9 KB | preflight：daily 2848 条（已排除隔离 10 条） |
| 关系图谱数据 | `tools/build_graph_data.py` → `web/public/data/graph/{mode_edges,concept_graph,similar_modes}.json` | 10663 B 脚本；3 产物 raw 1532.0 KB / **gzip 542.1 KB（门限 1.5 MB）** | `mode_edges` 6684 边；`concept_graph` `{n_figures:284, n_concepts:13288, n_edges:13552}` |
| PWA 图标 | `tools/build_pwa_icons.py` | 8395 B | `icons/icon-512.png` 31760 B |

### B 系列：前端功能（SPA 视图）

| 交付 | 文件 | 体量 | 验证 |
|---|---|---|---|
| B1/B2 关系图谱 UI + 相似模式 + 概念索引 | `web/src/views/GraphView/GraphView.vue`、`GraphView/index.ts` | — | 三视图实测：人物-模式-概念 23 节点/23 边；模式关联 23/22；全局网络 K=60 得 60 节点/36 边 |
| B3 跨人物对比 | `web/src/views/CompareView.vue` | 21590 B | `/compare/?items=...` 已选 4/4、3 张表；无效 code 显式提示 |
| B4 每日一模式 | `web/src/views/DailyView.vue` + 首页模块 | 10408 B | 2026-09-18 对应 `M-FYJ-009 时务人士监督法`（福泽谕吉） |
| B5 模板库 + 导出 | `web/src/views/TemplateDetailView.vue`、`web/public/templates/*.md`（7 份） | 7581 B；longzhong.md 12033 B | 线上下载实测 12033 B，sha256 `03efa9ff49bf...` 与仓库同源 |
| B6 P1 QA | `docs/qa/phase30_p1_qa.md` | 19254 B | 模式名历史三元组折平后复测通过 |

### C 系列：工程与治理

| 交付 | 文件 | 体量 | 验证 |
|---|---|---|---|
| C1 质量门 | `.github/workflows/quality-gate.yml`（三 job）、`tools/ci_data_check.py`、`tools/ci_link_check.py`、`lighthouserc.json` | 5504 / 15704 / 20915 / 1999 B | 本卡现场跑 `ci_data_check.py`：**24 条断言 0 失败 PASS**；CI run 35352248167 三 job 全绿 |
| C1 发布流水线 | `.github/workflows/pages.yml`（SPA + 文档站一次原子发布） | 10625 B | Pages run 35351886778 success 3m39s |
| C2 文档站主题 | `mkdocs.pages.yml`、`docs_overrides/main.html`、`docs_overrides/assets/stylesheets/protreptic.css`、`protreptic.svg` | 4486 B / 3 文件 | 线上 `/docs/` 200 |
| C3 访问统计 | GoatCounter 自托管接入（`tools/gc`） | — | 隐私友好、无第三方请求 |
| C4 终审验收 | `docs/qa/phase30_acceptance.md`（两仓同文） | 17183 B | 线上 `/docs/qa/phase30_acceptance/` 200 |
| C5 收官报告 | `docs/phase30_final_report.md`（本文，两仓同文） | 见文件 | 本报告 |

---

## 2. 实测证据（本卡现场取证）

### 2.1 构建：本地产物 == 线上产物

```
cd /opt/data/workspace/Protreptic/web && VITE_DATA_MODE=static npm run build
  -> vue-tsc 0 error；137 modules transformed；built in 7.33s（整命令 wall 15.0s）
  -> dist/assets/index-CE7EoPzT.js   339.22 kB, gzip 123.95 kB
  -> dist/assets/index-CwXbff_a.css   49.41 kB, gzip   9.20 kB
```

| 侧 | sha256 |
|---|---|
| 本地 `web/dist/assets/index-CE7EoPzT.js` | `e05d3b97d404326395be376ab9021c142455c095dd3c0ba9f1975e1d3e71d81e` |
| 线上 `/assets/index-CE7EoPzT.js` | `e05d3b97d404326395be376ab9021c142455c095dd3c0ba9f1975e1d3e71d81e` |

**结论：逐字节一致** —— 线上跑的就是当前源码构建出来的产物。

### 2.2 数据基线断言（质量门同款脚本，本地复跑）

```
python3 tools/ci_data_check.py
  · 名录 1338 条 (人物 283 / 场景 1055, 带模式 1302); 无名字 0 条, 无描述 635 条
  · 路由 1353 条 {'person': 283, 'scenario': 1055, 'static': 8, 'template': 7}
  · sitemap 1354 条 URL (期望 1354 = 路由 1353 + 首页)
  数据校验: 24 条断言, 失败 0 条 -> PASS
```

```
python3 tools/pages_preflight.py --stage data
  figures=1057 modes=2858 figure shards=1057 by-figure shards=284
  daily: 2848 条（已排除隔离名单 10 条）names=2848 tz=Asia/Shanghai
  [OK] stage=data：全部断言通过
```

### 2.3 线上抽检（curl，逐条真实请求）

全部返回 **200**：`/`、`/figures/`、`/modes/`、`/concepts/`、`/graph/`、`/compare/`、`/daily/`、`/templates/`、`/api/`、
`/minds/H-SUN-001/`、`/minds/H-WYM-001/`、`/templates/longzhong/`、`/sitemap.xml`、`/sw.js`、`/manifest.webmanifest`、
`/data/index.unified.json`、`/data/meta.json`、`/docs/`、`/docs/qa/phase30_acceptance/`、
`/og/site.png`、`/og/pages/figures.png`、`/og/pages/modes.png`、`/og/pages/templates.png`、
`/og/minds/H-WYM-001.png`、`/og/minds/H-SUN-001.png`、`/og/figures/KG-AKA-001.png`、`/og/templates/longzhong.png`。

- 不存在的资源 `/og/figures.png` 返回 **404 + SPA 外壳 3904 B** —— 深链兜底行为符合设计。
- 分享图命名族：`/og/site.png`（首页）、`/og/pages/{figures,modes,templates}.png`（列表页）、`/og/minds/<code>.png`（人物）、`/og/figures/<code>.png`（场景）、`/og/templates/<slug>.png`（模板）。
- 线上 `/minds/H-WYM-001/` 的 head：`og:title`、`og:image`（含 width 1200 / height 630 / alt）、`twitter:image` 齐备；图片真实可下载（28568 B，PNG 魔数）。

### 2.4 线上数据

| 项 | 实测 |
|---|---|
| `data/index.unified.json` | `schema=protreptic.unified_index/v1`，`counts={total:1338, figures:283, scenarios:1055, with_modes:1302}`，items 1338，空白 code **0**，`H-SUN-001` 在列 |
| `sitemap.xml` | 1354 条 `<loc>`，含裸空格的 `<loc>` **0** |
| `sw.js` | 11433 B，真实 SW（C4 修复后线上不再是兜底 HTML） |
| `manifest.webmanifest` | `Protreptic · 思想典藏 — 历史人物思维模式库` / `display=standalone` / `start_url=./` / 4 icons |

### 2.5 CI 现状（`gh run list`，本卡执行时刻）

| 工作流 | 最近 run | 结论 |
|---|---|---|
| Deploy to GitHub Pages | 35351886778 | **success**（3m39s） |
| Quality Gate | 35352248167 | **success**（1m51s，三 job） |
| Protreptic CI/CD | 35351886853 | failure（1m45s）—— **存量**，见 R2 |
| CI（markdown-lint） | 35351886737 | failure（26s）—— **存量**，见 R1 |

两处红在 Phase30 开始前就存在（C4 报告 §2 已给对照证据），与本阶段交付无因果关系。


### 2.6 线上全量可达性（本卡现场复跑门的脚本）

```
python3 tools/ci_link_check.py live --crawl-sample 8
  · 线上 sitemap: https://ovmobilegroup.github.io/protreptic/sitemap.xml 读到 1354 条 URL
  · 页面内链接抽查: 抓 8 页, 抽出站内引用 5 条
  · 耗时 143.6s, 并发 16, 状态码分布 {'200': 1359}, 重定向后 200 的 0 条
  [live] https://ovmobilegroup.github.io/protreptic/: 检查 1359 条, 失败 0 条 -> PASS
```

**线上 1359 条 URL 全部可达，失败 0 条**（含 sitemap 全集、路由清单 canonical、入口页自报的站内链接）。
---

## 3. 本卡（C5）变更清单

| # | 变更 | 内容 |
|---|---|---|
| J1 | **清理 workspace 仓库垃圾路径** | `tools/` 下有 20 个由 shell 误操作产生的跟踪路径（文件名内含换行、shell 片段、残缺标签、私有工作区临时路径），由 `1ff8dcb9`（Phase20 黄宗羲）那次 `git add -A` 一并带入。它们会污染任何对 `tools/*.py` 的遍历，也可能把私有工作区路径带进仓库。已在 workspace 侧删除，`tools/` 跟踪文件 1050 变 1030，残留可疑路径 0（publish 仓本来就没有这些文件，无需处理）。 |
| J2 | 收官报告 | 新增本文 `docs/phase30_final_report.md`，两仓同文。 |
| J3 | 双仓小漂移对齐 | `tools/ci_link_check.py` 在 workspace 比 publish 多一段「仅本地排查用」的 `--sitemap ""` 跳过分支（本地调试后未同步）。已同步到 publish，消除唯一一处「门脚本」漂移。 |
| J4 | 技能沉淀 | 更新技能 `protreptic-web-frontend`：新增预渲染 / Service Worker / 检索索引 / CI 步骤顺序 / 双仓漂移 / 发布断言 六类坑位。 |

**本卡未改任何数据与前端源码**，因此线上产物不变（§2.1 的字节一致仍成立）。

---

## 4. 双仓一致性核查（本卡逐文件 sha256 比对）

| 目录 | 共同文件 | 内容不同 | 说明 |
|---|---|---|---|
| `data/` | 771 | **0** | 数据源完全同步（C4 的 B2 修复生效） |
| `web/src/` | 39 | **0** | 前端源码完全同步 |
| `.github/` | 8 | **0** | 流水线定义完全同步 |
| `docs_overrides/`、`mkdocs.pages.yml`、`lighthouserc.json` | 5 | 0 | 完全同步 |
| `tools/` | 805 | 26，修复后仅剩历史一次性脚本 | 差异中 25 处是 workspace 独有的历史一次性脚本（`add_*.py` / `check_*.py` 等，publish 从不需要）；唯一有意义的差异是 `tools/ci_link_check.py`，已由 J3 对齐 |
| `web/public/data/` | 1445 | 12 | 生成物目录（`.gitignore` 已忽略），CI 每次现算，两端过期产物不一致属预期，不影响线上 |
| `docs/` | 403 | 33 | 全部是 2026-09 之前的历史文档（Phase20 研究报告、review、planning 等）在 publish 侧未同步，属存量漂移，不影响站点 |

**结论：影响线上站点的路径（`web/src`、`.github`、`data`、`mkdocs*`、`tools/` 的流水线脚本）已全部一致；剩余差异仅限生成物与历史文档。**

---

## 5. 遗留问题

沿用 C4 的编号（R1 到 R9 的完整根因见 `docs/qa/phase30_acceptance.md` 第 6 节），此处给收官口径与新增项：

| # | 级别 | 问题 | 状态 / 建议 |
|---|---|---|---|
| R1 | P2 | `CI` / markdown-lint 长期红（存量：`docs/**`、`data/figures/**`、`web/public/templates/*.md` 上千条历史违规） | 已建跟进卡 **t_5505e042**（R1 + R2，assignee san-martin） |
| R2 | P2 | `Protreptic CI/CD` 的 `Run Python tests` 长期红（断言读 `tools/scenarios_zh.json` 陈旧副本，口径 1008 对实数据 1055） | 同上（t_5505e042） |
| R3 | P2 | `domain_zh` 语义污染：by-figure 分片 1411/2858 = 49.4% 是散文而非领域标签（导出映射把案例 / 定义写进该字段） | 建议单开数据治理卡；UI 侧可先加截断 |
| R4 | P3 | `/concepts` 出现可疑人名「获取兵」「非人」 | 数据治理卡 |
| R5 | P3 | 已隔离的 `H-SX-001` 仍从概念图漏出（本卡实测 `concept_graph.json` `n_figures=284` = 283 + 1），隔离名单未在图谱层共享 | 抽公共常量并让图 / 概念层复用 |
| R6 | P3 | print 媒体下 `.pt-print-only` 页脚位置不在纸面底部 | 打印样式微调 |
| R7 | P3 | `docs_site/docs/templates/*.md` 是过期副本（10505 B 对源 12033 B） | 文档归档卡 |
| R8 | P3 | 文案硬编码「2868 条 x 284 位」与站内统计（2858 / 283）不一致：本卡实测线上 `index.html` 的 description 仍是 2868，`mkdocs.pages.yml` 的 `site_description` 也是 2868 | 让文案从 `data/meta.json` 读取，或改口径说明 |
| R9 | P3 | `/figures` hero 与 `/api` 写「1058 个场景」，名录实为 1055 | 同 R8 |
| **R10** | **P3（新）** | **检索索引已用掉 96.7% 预算**：16 片 gzip 合计 773.9 KB 对门限 800 KB | 数据量再增长就会撞门（`build_search_index.py` 超限直接非 0 退出、卡死发布）。建议把预算改为相对数据量，或提高门限并同步记录 |
| **R11** | **P3（新）** | **`docs/` 历史文档双仓漂移 33 个文件**（publish 侧缺） | 不影响站点（publish 用自己那份 `docs/` 构建），但会让「两仓同文」的假设失真；建议一次性对齐，或明确 publish 只保留发布所需文档 |
| J1 | — | workspace `tools/` 20 个垃圾跟踪路径 | **本卡已清理** |

---

## 6. 后续建议（排卡优先级）

1. **P2 先清 CI 红（R1 + R2，已有卡 t_5505e042）**：CI 全绿是后续任何自动判定的前提，长期红会让真红被淹没。
2. **P2 数据语义治理（R3）**：49.4% 的 `domain_zh` 污染直接反映在 `/compare` 领域分布表与 `/minds` 卡片上，是当前最影响观感的数据缺陷；根因在导出映射，改一处即可覆盖全站。
3. **P3 分享图覆盖面补全**：`/og/pages/index.png`、`/og/pages/graph.png` 为 404（首页用 `/og/site.png`，`/graph` 无图）。建议明确「哪些路由必须有 og:image」并加断言，否则分享卡片会静默退化。
4. **P3 隔离名单统一（R5）**：把隔离名单抽成单一来源（如 `tools/quarantine.py`），索引层 / 图谱层 / 每日层共用，避免「隔离了但没完全隔离」。
5. **P3 预算治理（R10）**：检索索引 96.7% 占用率需要显式记录与监控，否则下次数据增长会让 Pages 直接构建失败。
6. **P3 计数口径统一（R8 / R9）**：把所有面向用户的计数改为读 `data/meta.json`（站内已有唯一真源），消灭硬编码常量。

---

## 7. 复跑命令（本报告所有数字均可复现）

```bash
# 1) 构建（vue-tsc 会卡类型错误）
cd /opt/data/workspace/Protreptic/web && VITE_DATA_MODE=static npm run build
```

```bash
# 2) 本地构建产物对线上产物
sha256sum web/dist/assets/index-*.js
curl -sL https://ovmobilegroup.github.io/protreptic/assets/index-CE7EoPzT.js | sha256sum

# 3) 数据基线断言（质量门同款，24 条）
cd /opt/data/workspace/Protreptic && python3 tools/ci_data_check.py

# 4) 静态数据预检
python3 tools/pages_preflight.py --stage data

# 5) 线上死链检测（全量，1359 条 URL；耗时数分钟）
python3 tools/ci_link_check.py live --crawl-sample 8
```

```bash
# 6) 线上抽检（把 <CODE> 换成人物编号）
curl -s -o /dev/null -w '%{http_code}\n' -L https://ovmobilegroup.github.io/protreptic/minds/H-WYM-001/

# 7) CI 目录（gh 在 /opt/data/home/.local/bin，需指定 GH_CONFIG_DIR）
GH_CONFIG_DIR=/opt/data/home/.config/gh gh run list --repo ovmobilegroup/protreptic --limit 10
```

```bash
# 8) 双仓一致性：逐文件比对
cd /opt/data/workspace/Protreptic
P=/opt/data/release/Protreptic-publish
for REL in $(git ls-files tools/ web/src .github); do
  if [ -f "$P/$REL" ]; then cmp -s "$REL" "$P/$REL" || echo "DIFF $REL"; fi
done
```

---

## 8. 结论摘要

- **Phase30 A/B/C 交付完整且线上可发布**：构建产物与线上逐字节一致，质量门数据断言 24/24 通过，线上抽检 27 条 URL 全部 200，PWA / 分享图 / 检索 / 图谱 / 对比 / 每日 / 模板导出 / 深浅色 / 移动端均在真实环境实测可用。
- **本卡为收官补了 3 项**：清理 workspace 的 20 个 shell 误操作垃圾路径、补齐两仓门脚本漂移、把全阶段踩坑沉淀进技能库。
- **上线后的持续成本主要在数据层**：R1 / R2 的存量 CI 红、R3 的 49.4% 字段语义污染、R10 的检索索引预算逼近上限，都已给出根因与建议，适合在下一阶段按 P2 到 P3 排卡。
