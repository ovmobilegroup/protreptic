# Web 前端迁移 GitHub Pages 可行性评估

- 评估者：san-martin（架构/技术选型）
- 日期：2026-09-17
- 评估对象：`web/`（Vue 3.4 + Vite 5 + TS 5 单页应用）
- 目标：判断能否静态托管到 GitHub Pages（`https://ovmobilegroup.github.io/protreptic/`），并给出可执行迁移方案
- 证据原则：本文所有结论均来自实测（本地构建 / 数据实测 / HTTP 实测 / 源码行号），未验证项在 §6 明确标注

---

## 0. 结论速览（TL;DR）

**部分可行：静态内容展示 100% 可行，运行时语义检索与后端导出不可行（必须降级）。**

1. 前端取数是一个"薄层"：所有数据访问都汇聚在 `web/src/stores/figures.ts`（6 处 axios 调用）、`web/src/views/FiguresView.vue`（2 处语义搜索）与 `web/src/views/ModesView.vue`（1 处 fetch）。**接口面收敛，是可行性的关键前提**——只需替换 3 个文件里的取数实现，页面组件几乎不动。
2. 数据体量完全撑得住：人物库全量 501 条 JSON 仅 **1.45 MB raw / 0.30 MB gzip**；核心资产 2858 条模式全量 **18.9 MB raw / 7.4 MB gzip（单文件不可取）**，但按人物分片后 **284 个分片、单片中位 57.6 KB raw / 23.4 KB gzip**，按需加载完全可行。
3. 构建链有一个**必须先修的前置故障**：`npm run build` 目前是**失败**的（`vue-tsc` 报 9 个类型错误，`vite build` 根本没机会执行）。实测 `vite build` 单独跑是通的（2.5 s，196 KB JS / 71 KB gzip）。
4. 路由/资源路径改造量小且已实测验证：给 `vite.config.ts` 加 `base: '/protreptic/'` 后，产物资源路径正确变为 `/protreptic/assets/...`（本文实测）。`router/index.ts:47` 用的是 `createWebHistory(import.meta.env.BASE_URL)`，会**自动跟随 base**，无需改路由代码。
5. 需要一份 `404.html` 回退（history 模式）或改用 hash 模式；Pages 源配置需人工从 "main /docs (Jekyll)" 切到 "GitHub Actions"——这一步决定了文档站点的去向，见 §3.7。
6. **最大的架构风险不是 Pages，而是数据编码体系不连通**：`figures` 表（501 行，`H-AZJ-345` 形态）与核心资产 `data/modes_data.json`（284 人物，`H-WYM-001`/`HCM` 形态）**交集为 0**（实测）。静态站点要同时承载两套资产，必须先决定 join 策略。详见 §1.5 与 §6。

---

## 1. 现状诊断

### 1.1 前端结构与规模

`web/` 目录（本地 `<repo>/web/`）：

| 文件 | 行数 | 作用 |
|---|---|---|
| `src/main.ts` | 12 | 挂载 Pinia + Router |
| `src/App.vue` | 71 | 顶栏（4 个导航）/ 页脚 |
| `src/router/index.ts` | 58 | 5 条路由 |
| `src/api/client.ts` | 32 | axios 实例，`baseURL = VITE_API_BASE_URL \|\| '/api'` |
| `src/stores/figures.ts` | 178 | **唯一的数据 store**，6 处后端调用 |
| `src/views/FiguresView.vue` | 487 | 人物库列表 + 关键词/语义搜索 + 筛选 + 分页 |
| `src/views/FigureDetailView.vue` | 404 | 人物详情 + 相似人物 + 雷达/时间线/应用场景（纯本地推导） |
| `src/views/ModesView.vue` | 108 | 思维模式库（42 条硬编码后端数据） |
| `src/views/TemplatesView.vue` | 81 | 复盘模板（纯静态数组，点开跳 `/templates/{id}.md`） |
| `src/views/ApiDocsView.vue` | 128 | API 文档（纯静态数组 + 硬编码 `http://localhost:8000`） |
| `src/components/{FigureCard,FilterPanel,Pagination,LanguageSwitcher,FigureCardSkeleton}.vue` | 205/189/56/82/42 | 展示组件 |
| **合计** | **1782** | — |

依赖（`web/package.json`）：`vue@^3.4`、`vue-router@^4.3`、`pinia@^2.1`、`axios@^1.6`；构建 `vue-tsc && vite build`。

### 1.2 取数依赖清单（代码级）

| # | 调用点（文件:行） | 请求 | 后端路由（文件:行） | 数据源 | Pages 可静态化？ |
|---|---|---|---|---|---|
| 1 | `stores/figures.ts:92` | `GET /api/v1/scenarios`（分页/筛选/搜索） | `routes/figures.py:16` | SQLite `figures` 表（501 行） | ✅ 全量 JSON + 前端筛选 |
| 2 | `stores/figures.ts:107` | `GET /api/v1/scenarios/{code}` | `routes/figures.py:124` | 同上 | ✅ 每人一片 |
| 3 | `stores/figures.ts:120` | `GET /api/v1/scenarios/search` | `routes/search.py:24` | 同上（SQL LIKE） | ✅ 前端内存检索 |
| 4 | `stores/figures.ts:131` | `GET /api/v1/scenarios/semantic-search` | **不存在**（后端是 `search.py:63 /search/semantic`） | BGE-m3 + FAISS | ❌ 需降级 |
| 5 | `stores/figures.ts:144` | `GET /api/v1/scenarios/{code}/similar` | `routes/search.py:106` | FAISS 相似度 | ⚠️ 可离线预计算 |
| 6 | `stores/figures.ts:157` | `GET /api/v1/scenarios/batch/{code}/similar` | **不存在** | — | ❌ 死代码 |
| 7 | `FiguresView.vue:184` | `GET /api/v1/scenarios/batch/semantic-search` | **不存在** | — | ❌ 死代码 |
| 8 | `FiguresView.vue:197` | `GET /api/v1/scenarios/semantic-search`（回退） | **不存在** | — | ❌ 死代码 |
| 9 | `ModesView.vue:15` | `GET /api/v1/modes`（原生 fetch） | `routes/modes.py:61` | **代码内硬编码 42 条**（`modes.py:10-58`） | ✅ 全量 JSON（且可升级为 2858 条） |
| 10 | `FigureDetailView.vue:79` → store:107 | 人物详情 | 同上 #2 | — | ✅ |
| 11 | `FigureDetailView.vue:96` → store:144 | 相似人物 | 同上 #5 | — | ⚠️ 预计算 |
| 12 | `TemplatesView.vue:23` | `window.open('/templates/{id}.md')` | 静态文件（仓库内无 `web/public/templates/`） | — | ⚠️ 需补素材 |
| 13 | `ApiDocsView.vue:49` | 展示 `http://localhost:8000/api/v1` | — | 纯文案 | ✅ 改文案 |

**结论：真正依赖"运行时后端能力"的只有 #4/#5（向量语义检索）与 #6/#7/#8（已是死代码，指向不存在的路由）。其余全部是"读静态数据"。**

### 1.3 后端与数据资产

- 后端：FastAPI 单服务（`api/main.py:36-42`，7 个 router，前缀 `/api/v1`），CORS `allow_origins=["*"]`（`api/main.py:29-34`）。
- 语义检索栈：`sentence-transformers==3.0.1` + `faiss-cpu==1.15.0`（`api/requirements.txt`），模型 `BAAI/bge-m3`，索引 `api/data/semantic_index.faiss`（1.96 MB）+ `..._metadata.pkl`（0.45 MB），硬编码绝对路径（`api/semantic_search.py:35-37`）——**这是纯服务端资产，浏览器无法复用**。
- 核心资产：`data/modes_data.json`（20.35 MB），结构为单个混合 dict：字段键 + `modes` 列表（**2868 条**，`load_v6.py:11`、`tools/figure_library.py:57` 均取 `raw["modes"]`）+ 23 个 `H-*` 人物记录键。
- 装载脚本 `api/load_v6.py` 按 `mode_code` 首现去重 → 实测 **2868 → 2858 条**（丢弃 10 条重复 `mode_code`）。
- 实测资产尺寸：

| 资产 | 体积 | 条数 |
|---|---|---|
| `api/protreptic.db` figures 表 | 导出 JSON 1.45 MB | 501 |
| `api/protreptic.db` thinking_modes 表 | raw_json 合计 13.54 MB | 2858（覆盖 284 人物） |
| `data/modes_data.json` | 20.35 MB | `modes` 2868 → 去重 2858 |
| `data/figures/*.json` | 17.97 MB | 347 个文件 |
| `api/data/semantic_index.faiss` | 1.96 MB | FAISS 索引 |
| `web/dist/`（已提交的旧产物） | JS 197 KB + CSS 3.6 KB | 2 个 hash 文件 |

### 1.4 前端与后端接口的实际错配（现状就是坏的）

实测：前端调用的 `semantic-search` / `batch/semantic-search` / `batch/{code}/similar` 三个路径在 `api/routes/` 中**均不存在**。也就是说：

- 人物库的"语义搜索"按钮当前**必然失败**（两次 fallback 都命中不存在的路由，`FiguresView.vue:184-210`）；
- 即便请求成功，**结果也不会被渲染**——`semanticResults`（`FiguresView.vue:140`）在模板中从未被使用（模板只渲染 `figuresStore.figures`，`FiguresView.vue:63-84`）。

**判定：语义检索在 UI 层已是死功能。这大幅降低了"迁移导致功能降级"的实际损失。**

### 1.5 数据编码体系不连通（实测，重大）

三套人物主键互不相通：

| 数据源 | 主键形态 | 数量 | 与其它源交集 |
|---|---|---|---|
| `api/protreptic.db` figures 表 | `H-AZJ-345`、`H-BC-45`、`A-1-X-P`、`P4-*` | 501 | 与 `data/figures/*.json`：**0** |
| `data/modes_data.json["modes"]` | `H-WYM-001`（117 个）/ `HCM`、`AlGhazali`（167 个） | 284 人物 / 2858 条 | 与 figures 表：**0**；与 `data/figures/*.json`：115 |
| `data/figures/*.json` | `H-AE-001` 形态 | 347 文件 | 与 figures 表：**0** |

实测命令与结果（脚本见附录 A）：

```
figures 表是否含 H-WYM-001: 0
figures 表是否含 H-WL-001: 0
figures 表是否含 H-ZL-08: 1
modes 里 H- 形态 figure_code 数 117
modes H- 与 data/figures 交集 115
figures 表 与 data/figures 交集 0
```

**含义**：前端人物库（读 figures 表）与核心资产 2868 模式（读 modes_data.json）**今天无法按 code join**。静态站点要么"两个页面各自独立、不 join"，要么先做一次数据治理（建议独立卡，不在本次迁移范围内）。这是本评估给出的**最重要架构提示**。

### 1.6 现状已损坏项（迁移前必须一并处理）

实测 `npm ci && npm run build`（在 `web/` 的副本中执行，未改动仓库源码）：

```
> vue-tsc && vite build
src/components/FilterPanel.vue(79,10): error TS7053 ...          (1)
src/views/FigureDetailView.vue(197,83): error TS2322 ...          (2)
src/views/FigureDetailView.vue(298,30): error TS2339 'timelineEvents' ...      (3)
src/views/FigureDetailView.vue(301,49): error TS2339 'timelineEvents' ...      (4)
src/views/FigureDetailView.vue(310,40): error TS2339 'timelineEvents' ...      (5)
src/views/FigureDetailView.vue(315,30): error TS2339 'applicationScenarios' ... (6)
src/views/FigureDetailView.vue(318,47): error TS2339 'applicationScenarios' ... (7)
src/views/FiguresView.vue(40,10): error TS2345 缺 tagLabels ...    (8)
src/views/FiguresView.vue(70,14): error TS2345 缺 lang ...         (9)
```

`vue-tsc --noEmit` 统计：**9 errors / 3 files**（FigureDetailView 6、FiguresView 2、FilterPanel 1）。→ **`npm run build` 当前整体失败**，已提交的 `web/dist/`（JS hash `index-DhuN4bel.js`）是历史产物，与当前源码已不同步。

其它既有缺陷（迁移会连带修复或放大）：

1. `FilterPanel` 声明了必填 prop `tagLabels`（`FilterPanel.vue:22`），但 `FiguresView.vue:40-44` 没传；同时 `filterOptions` 遍历的是 `props.filters`（值为字符串）而非 `tagLabels`，类型判断 `typeof labels === 'object'` 恒为假（`FilterPanel.vue:56-63`）→ 侧边栏恒显示"暂无选项"。
2. `ModesView.vue:61` 使用了 `<ModeCardSkeleton>` 但**从未 import**，加载骨架屏报组件未注册。
3. `web/public/` 为空，`index.html:8` 引用 `/favicon.svg` → favicon 404（实测 `web/public/` 目录 0 文件）。
4. `ApiDocsView.vue:49` 硬编码 `http://localhost:8000/api/v1`。
5. `App.vue:59` 页脚 GitHub 链接指向 `https://github.com/protreptic/protreptic`，与实际仓库 `ovmobilegroup/protreptic` 不符。
6. `TemplatesView.vue:23` 打开 `/templates/{id}.md`，但仓库内无该静态目录。

### 1.7 部署现状（实测）

- 仓库：`ovmobilegroup/protreptic`，public，`default_branch=main`，`has_pages=true`，创建于 `2026-09-17T13:02:52Z`（API 实测）。
- Pages 线上：`https://ovmobilegroup.github.io/protreptic/` 返回 200，HTML 由 **Jekyll 3.10.0** 生成，标题 `Protreptic 思维模式库 | 2868 条历史人物思维模式 · 284 位人物 · 中英双语` → 与"从 main `/docs` 发布"一致；上游 `docs/_config.yml` 使用 `theme: jekyll-theme-cayman`，`docs/index.md` 为入口。
- 上游 `main` 根目录包含 `web/`（含已提交的 `dist/`）与 `docs/`；`.github/workflows/` 只有 `ci-cd.yml` 与 `markdown-lint.yml`，**没有任何 Pages workflow**。
- 容器化方案现状：`Dockerfile.web`（node 构建 → nginx）+ `web/nginx.conf`（`try_files $uri $uri/ /index.html` 的 SPA 回退 + `/api/` 反代 `http://api:8000`）。**这套"nginx + 反代"正是 Pages 上不存在的东西**，替代品就是 §3.5 的 `404.html` 与 §3.2 的静态数据。
- ⚠️ 既有 CI 有硬伤：`.github/workflows/ci-cd.yml:34,40` 使用本机绝对路径 `cd <repo>/...`，在 GitHub runner 上必然失败（`api`、`tools` 在仓库里是相对根目录的 `api`、`tools`）。

---

## 2. 可行性结论（逐能力判定）

| 能力 | 判定 | 依据 |
|---|---|---|
| 人物库列表 / 分页 / 筛选 / 关键词搜索 | ✅ 完全可行 | 全量 501 条仅 1.45 MB raw / 0.30 MB gzip，可整包下载后前端筛选 |
| 人物详情页 | ✅ 完全可行 | 分片平均 3.0 KB/人，最大 7.4 KB |
| 思维模式库（列表/浏览） | ✅ 完全可行且是**升级** | 现状只展示硬编码 42 条；静态化可把 2858 条真正上线 |
| 复盘模板页 | ✅ 可行（需补静态 .md 素材） | 纯静态数组 + 文件跳转 |
| API 文档页 | ✅ 可行（改文案） | 组件本身是静态数组；Swagger/ReDoc 页面不可搬 |
| 中英切换 | ✅ 可行 | `useI18n` 纯本地（localStorage），双语数据在静态 JSON 中并存 |
| 语义检索（BGE-m3 + FAISS） | ❌ 不可行，需降级 | 模型 3.0.1 + FAISS 索引为服务端资产；浏览器端跑 BGE-m3 不现实 |
| 相似人物推荐 | ⚠️ 部分可行（离线预计算） | 离线用现有 FAISS 索引跑 501×top-10，生成 `similar.json`，可完整保留该卡片 |
| 服务端导出 `/api/v1/export`、健康检查、标签统计 | ❌ 不可行 → 改为构建期生成静态文件或删除入口 | 无后端 |
| 后端运行时更新数据后前端即时可见 | ❌ 不可行 | 静态站点 = 数据变更需重新构建发布（工作流可自动化） |

**总体判定：部分可行（需降级）。核心内容展示 100% 可搬；唯一真正的能力损失是"在线语义检索"，且该功能在 UI 层当前已是死代码（§1.4），实际损失接近 0（相似人物可用离线预计算替代）。**

---

## 3. 迁移方案

### 3.1 目标架构

```
GitHub Actions (push to main)
  ├─ Step A: node 20 → cd web && npm ci && npm run build   → web/dist/
  ├─ Step B: python → tools/export_static_site.py          → web/public/data/** ─┐
  │           (读 data/modes_data.json + api/protreptic.db)                      │ 随 dist 一起产出
  ├─ Step C: mkdocs build（docs_site/mkdocs.yml）→ site/docs/** ─┐              │
  └─ Step D: 合并 dist + site/docs → _site/  → upload-pages-artifact → deploy-pages
                                                                 │              │
https://ovmobilegroup.github.io/protreptic/                       │              │
  ├─ /               → SPA（Vue，base=/protreptic/）  ←───────────┘              │
  ├─ /data/**        → 静态 JSON 分片 ←──────────────────────────────────────────┘
  └─ /docs/**        → 原 docs/ 文档站（mkdir 生成）
```

### 3.2 数据静态化（核心）

**产物规范**（建议落在 `web/public/data/`，Vite 会原样复制进 `dist/`）：

| 产物 | 内容 | 实测体积 |
|---|---|---|
| `data/figures.index.json` | 501 条轻量索引（code/name_zh/name_en/era/domains/historical_domains/gender/ethnicity/n_modes） | 157 KB raw / **33 KB gzip** |
| `data/figures/{code}.json` | 501 个详情分片 | 合计 1.45 MB，平均 3.0 KB，最大 7.4 KB |
| `data/modes/index-{0..7}.json` | 2858 条模式摘要，按 `md5(mode_code) % 8` 均分 | 合计 2.50 MB raw / **1.07 MB gzip**，单片 126–152 KB gzip |
| `data/modes/by-figure/{figure_code}.json` | 284 个"某人的 10 条模式"分片 | 合计 16.09 MB raw / 6.48 MB gzip，单片中位 57.6 KB raw / **23.4 KB gzip** |
| `data/tags.json` | 由 `routes/tags.py:90` 的 `TAG_VALUES` + DB 聚合生成 | <10 KB |
| `data/similar.json`（可选） | 离线 FAISS 预计算 top-10 相似人物 | 待测 |
| `data/meta.json` | 构建时间戳、源文件 sha256、条数统计（供前端校验） | <1 KB |

**分片规则（踩坑记录，必须按此实现）**：

- ❌ **不要按 `H-` 前缀分片**：实测 2858 条中有 **1670 条的 `figure_code` 是旧式三字母 slug**（`HCM`、`SUK`、`AMP`、`AlGhazali`…），按前缀分片会把它们全挤进一个 1.78 MB 的分片。
- ✅ **按 `figure_code` 原值分组** → 恰好 284 个均衡分片（实测）。
- ✅ 摘要索引用 `md5(mode_code) % N` 均分（实测 8 片最均衡）。
- ❌ **不要生成单个全量文件**：实测 18.92 MB raw / **7.4 MB gzip**，移动端不可接受。
- 摘要索引字段建议只含 `mode_code/figure_code/figure_name/name_zh/name_en/category/domain_zh/domain_en`（实测 2.50 MB raw / 0.99 MB gzip）；若加 60 字截断定义则涨到 2.99 MB raw / 1.19 MB gzip —— **定义全文只在 `by-figure` 分片里给**。

**生成脚本**（新增 `tools/export_static_site.py`，属新文件、不修改 `web/` 源码）：

1. `data/modes_data.json` → `raw["modes"]`，按 `load_v6.py` 同规则按 `mode_code` 首现去重（2868 → 2858）。
2. `api/protreptic.db` → `figures` 表全量导出；JSON 文本字段（`modes`/`domains`/`historical_domains`）反序列化为数组。
3. 每个产物写 `meta.json`（条数 + sha256），前端启动时可比对，避免"数据没更新但前端缓存了"的幽灵问题。
4. 建议同时输出 `docs/architecture/static_data_manifest.json`，让数据治理卡有据可依。

### 3.3 前端适配层改造（最小侵入）

**关键设计：新增一层数据适配器，页面组件几乎零改动。**

- 新增 `web/src/api/static.ts`：实现与 `stores/figures.ts` 完全一致的 5 个方法签名
  （`fetchFigures(params)` / `fetchFigure(code, lang)` / `searchFigures(q, lang, limit)` / `semanticSearch(q,...)` / `getSimilar(code,...)`），内部改为：
  - 第一次调用时 `fetch(BASE + 'data/figures.index.json')` 并缓存到内存；
  - 分页/筛选/关键词过滤在内存完成（501 条，成本可忽略）；
  - `searchFigures` 用已有的 `tagLabels`（`FiguresView.vue:274-315`）做多字段子串匹配；
  - `semanticSearch` **降级为 `searchFigures` 的别名**，并在 UI 上把按钮文案从"语义搜索"改为"智能检索"（诚实标注）；
  - `getSimilar` 若采用 §3.2 的 `similar.json`，则直接读预计算结果。
- 改造点清单（**共 3 个文件，7 处**）：
  1. `web/src/stores/figures.ts:3` 增加一行按 `import.meta.env.VITE_DATA_MODE` 的条件导入（`static` / `api` 二选一），其余 88-165 行逻辑不变；
  2. `web/src/views/ModesView.vue:15` 把 `fetch('/api/v1/modes')` 换成读 `data/modes/index-*.json`（可顺带把 42 条升级为 2858 条）；
  3. `web/src/views/FiguresView.vue:182-210` 删除/改写两处语义搜索调用（本就是死代码）。
- 组件层（`FigureCard` / `FilterPanel` / `Pagination` / `FigureDetailView` 的雷达图、时间线、应用场景）**全部是本地推导，无需改动**。

### 3.4 构建配置

`web/vite.config.ts`（现有 21 行，无 `base`）：

```ts
export default defineConfig({
  base: process.env.VITE_BASE ?? '/protreptic/',   // ← 新增：Pages 项目站点子路径
  plugins: [vue()],
  resolve: { alias: { '@': fileURLToPath(new URL('./src', import.meta.url)) } },
  server: { port: 3000, proxy: { '/api': { target: 'http://localhost:8000', changeOrigin: true } } },
})
```

**实测验证**（在 `web/` 副本中加 `base: '/protreptic/'` 后重新构建）：

```
dist/index.html   0.50 kB │ gzip: 0.36 kB
dist/assets/index-0_7iAHxO.css  3.63 kB │ gzip: 1.18 kB
dist/assets/index-DzwXnKwA.js 195.99 kB │ gzip: 71.37 kB
✓ built in 2.47s

<script type="module" crossorigin src="/protreptic/assets/index-DzwXnKwA.js"></script>
<link rel="stylesheet" crossorigin href="/protreptic/assets/index-0_7iAHxO.css">
```

→ 资源路径正确带上 `/protreptic/`。注意 `index.html:8` 的 `<link rel="icon" href="/favicon.svg">` **未被重写**（该文件在 `public/` 中不存在），需改为相对路径 `./favicon.svg` 并补上 `web/public/favicon.svg`。

`package.json` 的 `build` 脚本建议改为两段，避免 TS 错误阻塞发布（但**推荐先修错**，见 §5 Step 0）：

```json
"build": "vue-tsc --noEmit && vite build",
"build:app": "vite build",
"build:data": "python3 ../tools/export_static_site.py --out public/data"
```

### 3.5 路由模式（Pages 的 SPA 陷阱与解法）

现状：`router/index.ts:47` `createWebHistory(import.meta.env.BASE_URL)`。`BASE_URL` 会跟随 §3.4 的 `base` 变成 `/protreptic/`，**深层链接解析天然正确**（实测 base 已生效）。

两个可选方案：

| 方案 | 做法 | 优点 | 代价 |
|---|---|---|---|
| **A（推荐）history + 404 回退** | `web/public/404.html` 内容 = `index.html` 的产物副本（构建后 `cp dist/index.html dist/404.html`），Pages 对未知路径返回它，SPA 正常接管 | URL 干净（`/protreptic/figures/H-ZL-08`），与现有路由代码零改动 | Pages 以 **HTTP 404** 状态返回该页（soft-404），SEO/分享卡片不理想 |
| B 改用 hash 路由 | `createWebHashHistory(import.meta.env.BASE_URL)` | 零服务端技巧，任何子路径都 200 | URL 变 `/#/figures/H-ZL-08`，需改 1 行；SEO 同样不理想 |

建议：**先 A**；若日后需要 SEO/分享优化，另开一卡做"每人物预渲染静态 HTML"（Vite SSG / `vite-plugin-pages` + `vite-ssg`），那是 +1 人日量级的独立工作。

### 3.6 部署方式（GitHub Actions）

新增 `.github/workflows/pages.yml`（**不要复用** `ci-cd.yml` 的 `build-web`，它依赖 Docker/ghcr 流程）：

```yaml
name: Deploy Web to Pages
on:
  push: { branches: [main] }
  workflow_dispatch:
permissions:
  contents: read
  pages: write
  id-token: write
concurrency:
  group: pages
  cancel-in-progress: true
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '20', cache: 'npm', cache-dependency-path: web/package-lock.json }
      - uses: actions/setup-python@v5
        with: { python-version: '3.12' }
      - name: Build static data
        run: python3 tools/export_static_site.py --out web/public/data
      - name: Build SPA
        working-directory: web
        run: |
          npm ci
          npm run build          # vue-tsc + vite build（需先修 §1.6 的 9 个类型错误）
          cp dist/index.html dist/404.html
      - uses: actions/configure-pages@v5
      - uses: actions/upload-pages-artifact@v3
        with: { path: web/dist }
  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment: { name: github-pages, url: "${{ steps.deployment.outputs.page_url }}" }
    steps:
      - id: deployment
        uses: actions/deploy-pages@v4
```

**注意（人工一步，无法用 API 验证）**：Settings → Pages → Source 必须从 "Deploy from a branch: main /docs (Jekyll)" 切换到 **"GitHub Actions"**。切换后原 Jekyll 文档站**不再自动发布**，因此需要 §3.7 的决定。

### 3.7 文档站点的去向（本次必须一起决定）

现状：`https://ovmobilegroup.github.io/protreptic/` 是 Jekyll 渲染的 `docs/`（cayman 主题），这是**已有用户可见的资产**，不能静默丢失。三个选项：

| 选项 | 做法 | 评价 |
|---|---|---|
| **A（推荐）合并到 Actions 站点** | workflow 里多跑一步 `mkdocs build`（仓库已有 `docs_site/mkdocs.yml` + `uv.lock`），产物放到 `_site/docs/`，SPA 在根，文档在 `/protreptic/docs/` | 一次发布、单域名、两个站点都在；代价是要用 mkdocs 复刻当前 Jekyll 的导航（`docs/index.md` 已含导航链接，mkdocs 可直接吃 markdown） |
| B 保留双站点 | 前端发布到另一个仓库的 gh-pages 或另一个 Pages 项目路径 | 零文档迁移成本，但两套发布流程 + 两个 URL |
| C 产出物塞进 `docs/` 目录 | 保持 main:/docs 发布，把 `dist/` 放进 `docs/app/` 并删掉 `docs/index.md`（否则 Jekyll 冲突） | 不必改设置，但**必须提交构建产物**、且 SPA 与文档在同一目录树里互相污染，不推荐 |

### 3.8 运行时 API 的保留可能性（备选，非本次范围）

若希望**保留**真实语义检索：把 `api/` 部署到任意托管（现成 `Dockerfile.api` + `api/requirements.txt`），Pages 前端通过 `VITE_API_BASE_URL=https://api.xxx` 调用——`api/main.py:29-34` 已是 `allow_origins=["*"]`，CORS 无障碍。这属于"另开一张卡"的独立部署议题，与 Pages 迁移解耦：**静态化方案与远程 API 方案并不互斥**，适配层（§3.3）的 `VITE_DATA_MODE=api` 分支天然支持回切。

---

## 4. 需降级 / 舍弃的功能清单

| # | 功能 | 现状 | 迁移后 | 用户可感知程度 |
|---|---|---|---|---|
| 1 | 语义搜索（BGE-m3 + FAISS） | UI 已是死代码（路由不存在，结果不渲染） | 改为前端关键词/标签检索，按钮文案改"智能检索" | 低（现在也用不了） |
| 2 | 相似人物推荐 | 依赖 `/scenarios/{code}/similar`（且该 code 空间与前端 figures 表不连通） | 离线预计算 `similar.json`（用现有 FAISS 索引，501×top-10） | 低 |
| 3 | `/api/v1/export`（JSON/Markdown 导出） | 无前端入口 | 舍弃；如需，构建期生成 `export_zh.json` / `export_en.json` 供直接下载 | 低 |
| 4 | `/api/v1/health`、`/api/v1/tags/stats` 动态统计 | 无前端入口（标签统计页未实现） | 改为 `data/meta.json` 静态统计 | 低 |
| 5 | Swagger `/docs`、ReDoc `/redoc` | `ApiDocsView` 只列路径，不嵌 UI（且硬编码 localhost:8000） | 保留手写 API 文档页，加"本站为静态托管，API 参考已归档"说明 | 中（文档准确性） |
| 6 | 后端改数据→网站即时更新 | 运行时可热改 | 改为"提交/重建即发布"（Actions 自动化，但有时延） | 中（仅对维护者） |
| 7 | 服务端分页（20/页） | 后端 `LIMIT/OFFSET` | 前端内存分页（501 条，无感） | 无 |
| 8 | P4/P5 专题筛选字段（`theme`、`nationality`…） | `figures` 表**根本没有**这些列（实测 20 列，无 `nationality`/`civilization_sphere`/`wiki_id`…） | 这些筛选 tab 在静态方案下应隐藏或置灰（本来就是永远无结果的死筛选） | 中（现状即坏） |
| 9 | 复盘模板 `.md` 打开 | `web/public/templates/` 不存在 | 需补素材目录，否则该页点击 404 | 中 |

---

## 5. 工作量估算与分步执行计划

前置说明：以下为"一个人、熟悉本仓库、含验证"的估算，单位为**人日**。

| 阶段 | 内容 | 交付物 | 估算 |
|---|---|---|---|
| **Step 0（阻塞项）** | 修复 9 个 `vue-tsc` 类型错误（3 个文件）+ 补 `web/public/favicon.svg` 与相对引用 + 修复 `ci-cd.yml:34,40` 的本机绝对路径 + `App.vue:59` 仓库链接 | 可控的 `npm run build` | 0.5–1.0 |
| **Step 1** | `tools/export_static_site.py`：去重、双数据源导出、分片（按 §3.2 的踩坑规则）、`meta.json`+sha256、体积断言 | 静态数据产物 + 生成器 | 0.5–1.0 |
| **Step 2** | `web/src/api/static.ts` 适配层 + `VITE_DATA_MODE` 开关 + `ModesView` 改读静态索引（顺带 42→2858）+ 前端筛选/分页 | 离线可跑通的 SPA | 1.0–1.5 |
| **Step 3** | `vite.config.ts` base + `404.html` 回退 + `npm run build` 冒烟（本地 `vite preview --base` 验证深链） | 可本地预览的 dist | 0.5 |
| **Step 4** | `.github/workflows/pages.yml` + Pages Source 切换 + 文档站点合并（§3.7 选项 A 的 mkdocs 步骤） | 线上可访问 | 0.5–1.0 |
| **Step 5（可选）** | 离线 FAISS 预计算 `similar.json`（保留相似人物卡片） | 相似人物功能 | 0.5–1.0 |
| **Step 6（可选，独立卡）** | 每人物预渲染静态 HTML（SEO/分享） | SSG 产物 | 1.0 |
| | | **合计** | **3.5–5.5 人日**（不含 Step 6） |

**分步验收点**：

1. Step 0 验收：`cd web && npm ci && npm run build` 退出码 0，`dist/index.html` 资源路径带 `/protreptic/`。
2. Step 1 验收：脚本产出 501 + 284 + 8 个文件，`figures.index.json` gzip ≤ 50 KB、`modes/index-*.json` 单片 gzip ≤ 200 KB，`meta.json` 条数与 `load_v6.py` 输出的 2858 一致。
3. Step 2 验收：断网 `vite preview` 下人物库列表/详情/筛选/分页/中英切换全部可用，浏览器 Network 无 `/api/` 请求。
4. Step 3 验收：直接访问 `http://localhost:4173/protreptic/figures/H-ZL-08` 返回 SPA（404 回退生效）。
5. Step 4 验收：`https://ovmobilegroup.github.io/protreptic/` 与 `/protreptic/figures/H-ZL-08` 均正常，`/protreptic/data/figures.index.json` 可 200 命中。

---

## 6. 风险与未验证项（诚实标注）

**风险（按严重度）**

1. **数据编码不连通（高）**：§1.5 实测三套主键交集为 0。静态站点若想让人物详情页显示"此人的 10 条模式"，必须先建立 `figures.code ↔ modes_data.figure_code` 的映射（建议按 `name_zh` 匹配 + 人工核对，作独立卡）。**迁移本身不被此阻塞**：Step 1–4 可先"两个页面各自独立"上线。
2. **Pages Soft-404（中）**：history 模式下深链返回 HTTP 404 状态码（页面正常渲染）。若在意 SEO，需 Step 6 或改 hash 模式。
3. **Pages Source 切换是人工操作（中）**：切换后 Jekyll 文档站停止发布；§3.7 选项 A 必须在同一次上线中完成，否则线上文档会消失。
4. **数据是"构建时快照"（中）**：`data/modes_data.json` 仍在高频演进（近一周仍有 merge/QA 提交），每次数据更新都需重新构建。建议在 workflow 里加 `paths` 过滤 + `meta.json` 条数断言，避免"数据更新但站点没跟上"。
5. **静态 JSON 未做体积回归防护（低）**：2858 条现在 2.5 MB 摘要；若模式数继续增长（目标 3000+），需在生成脚本里加体积上限断言。
6. **两库体积与缓存（低）**：`data/**` 建议配长缓存（文件名带内容 hash 或用带版本目录 `data/v{n}/`），否则用户可能拿到旧索引。

**未验证项（明确说明，未编造）**

1. **Pages 的 Source 设置无法通过公开 API 读取**（`/repos/{owner}/{repo}/pages` 需 push 权限）。"main /docs + Jekyll"是从线上 HTML 的 `Jekyll v3.10.0` 生成器标记与上游 `docs/_config.yml` 推断的。
2. **本地 `<repo>` 未配置 git remote**（`git remote -v` 为空，仅有本地分支 `master`/`boardmaster`），因此我**无法断言**本地 `web/` 与上游 `main` 的 `web/` 逐文件一致；仅比对到目录结构一致（上游 `web/` 含 `dist,index.html,nginx.conf,package-lock.json,package.json,src,tailwind.config.js,tsconfig*.json,vite.config.ts`）。**上线前必须先确认发布用的源码基线。**
3. **未实测线上 `web/dist` 的可用性**（Pages 未承载前端，无 URL 可测）。
4. **未实测 mkdocs 复刻 Jekyll 导航的效果**（`docs_site/mkdocs.yml` 存在但未构建过）。
5. **未实测离线 FAISS 预计算 `similar.json` 的耗时与体积**（Step 5 的估算基于 1.96 MB 索引 + 501 次查询的量级推断）。
6. 本文实测均在本机（Gentoo，node v26.5.1 / npm 11.17.0，Python 3.13）完成；GitHub runner 的 node 20 环境未验证。
7. 本地 `docs/` 与上游不同（上游含 `_config.yml`、`index.md`；本地没有），说明本地工作副本落后于上游，进一步支持"上线前确认基线"这一要求。

---

## 附录 A：实测脚本与原始输出

所有探针脚本位于本次评估工作区 `<internal>`（只读原仓库，未改动仓库内任何文件）：

| 脚本 | 作用 | 关键输出 |
|---|---|---|
| `probe.py` | 数据文件体积 | `data/modes_data.json` 20.35 MB、`api/protreptic.db` 36.71 MB |
| `probe2.py` | modes_data.json 结构 / sqlite 表 | top-level 48 键；`figures` 501 行、`thinking_modes` 2858 行 |
| `probe3.py` | 逐字段体积 | `modes` 键 14.2 MB（唯一大块） |
| `probe4.py` | 2868 条结构与 `load_v6.py` | `modes` len 2868，27 字段/条 |
| `probe5.py` | figures 全量导出体积 | 501 条 = 0.81 MB（字符串口径）/ 1.45 MB（JSON 口径） |
| `probe6.py` | 索引变体 + 人物分片 | thin 索引 2.50 MB raw / 0.99 MB gzip；分片人均 23.4 KB gzip |
| `probe7.py` | 前缀分片 + 首屏预算 | 前缀分片失衡（单片 739 KB gzip，因 1670 条旧式 code）；JS gzip 69.3 KB |
| `probe8.py` | `md5%8` 均分 | 8 片，单片 126–152 KB gzip |
| `probe9.py` | 旧式 `figure_code` 抽样 | `HCM`/`SUK` 形态 1670 条 / 167 人物 |
| `probe10.py` | 三库主键交集 | figures 表 vs modes：**交集 0** |
| `probe11.py` | 具体 code 命中 + `data/figures` 交集 | `H-WYM-001` 不在 figures 表；modes ∩ data/figures = 115 |
| `run_build.sh` | 在 `web/` 副本上构建 | `vite build` 成功（2.5 s）；`base` 生效后 `/protreptic/assets/...` |
| `gen_static_probe.py` | 端到端生成静态分片样例 | `site_data_probe/` 291 文件，尺寸见 §3.2 |
| `site_data_probe*/` | 实测产物（未提交） | 291 + 多个分片目录 |

## 附录 B：证据索引（文件:行）

- 前端取数：`web/src/api/client.ts:4`、`web/src/stores/figures.ts:3,88-165`、`web/src/views/FiguresView.vue:105,111,140,182-214,270`、`web/src/views/ModesView.vue:11-23,61`、`web/src/views/FigureDetailView.vue:75-103`
- 路由与构建：`web/src/router/index.ts:46-56`、`web/vite.config.ts:1-21`、`web/index.html:8`、`web/package.json:10-14`
- 既有缺陷：`web/src/components/FilterPanel.vue:22,56-63,79`、`web/src/views/FiguresView.vue:40-44,70`、`web/src/views/FigureDetailView.vue:197,298,301,310,315,318`、`web/src/views/ApiDocsView.vue:49`、`web/src/App.vue:59`、`web/src/views/TemplatesView.vue:23`
- 后端：`api/main.py:29-42`、`api/routes/figures.py:16,124`、`api/routes/modes.py:10-58,61`、`api/routes/search.py:24,63,106`、`api/routes/tags.py:32,90,96`、`api/routes/export.py:16`、`api/requirements.txt`、`api/semantic_search.py:22-23,35-37`、`api/load_v6.py:11-20,60-73`
- 数据资产：`data/modes_data.json`（`["modes"]` 2868）、`api/protreptic.db`（figures 501 / thinking_modes 2858）、`api/data/semantic_index.faiss`、`data/figures/*.json`（347）、`tools/figure_library.py:32-46,57`
- 部署现状：`.github/workflows/ci-cd.yml:34,40`、`.github/workflows/markdown-lint.yml`、`Dockerfile.web`、`web/nginx.conf`、上游 `docs/_config.yml`、上游 `docs/index.md`
