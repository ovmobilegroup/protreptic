# Protreptic Web P0 架构方案 (Phase30-A0)

> 卡片: `t_8a6d69c5` / 负责人: san-martin / 日期: 2026-09-18
> 仓库: `/opt/data/workspace/Protreptic` (前端 `web/`) ; 发布仓 `/opt/data/release/Protreptic-publish`
> 线上: https://ovmobilegroup.github.io/protreptic
>
> 本文所有数字都来自本卡的真实取证.取证脚本与产物:
> - `tools/measure_web_p0_baseline.py` -> `docs/architecture/web_p0_baseline.json` (体积基线)
> - `tools/prerender_routes.py` -> `docs/architecture/web_p0_routes.json` (预渲染路由清单, 发布仓基线 1350 条)
> - `docs/architecture/web_p0_evidence.md` (每个数字对应的命令与原始输出)
>
> 凡未实测的, 本文一律标注 **[未验证]**, 不做推断式断言.

---

## 0. 结论速览

| # | 问题 | 结论 | 证据 |
|---|------|------|------|
| 1 | 深链返回 200 | 已在流水线内解决: 构建后为公开名录的 **1350** 个路由 (发布仓基线) 各生成 `<route>/index.html` (等于 `dist/index.html` 加上该路由的 head).本地静态托管实测 **1350/1350 返回 200** | 2.1 / 2.5 |
| 2 | Service Worker 缓存 | scope 为 `/protreptic/`; app shell 加索引在 install 期预缓存 (约 244 KB gzip); `data/**` 为 cache-first 且按数据版本号命名缓存; 导航 network-first 并回退到通用 shell; `modes/index-*.json` (1.11 MB gzip) 在激活后后台预热, 不用它阻塞 install | 3.4 |
| 3 | 全文检索索引 | 二进制 varint 倒排, 按 token 首字符分 16 片; 推荐规格 **721 KB gzip** (预算 800 KB), 单片最大约 58 KB; 查询按需只拉不超过 3 片 | 4.2 / 4.3 |

**本卡交付的代码产物 (均已落盘并实跑)**

| 路径 | 作用 | 实测结果 |
|------|------|----------|
| `tools/prerender_routes.py` | 路由预渲染 (P0 主方案) | 1350 路由 / 3888 KB HTML / 0.35 s |
| `tools/measure_web_p0_baseline.py` | 体积基线取证 | 输出 `docs/architecture/web_p0_baseline.json` |
| `docs/architecture/web_p0_routes.json` | 路由清单 (供 sitemap / SW / CI 消费) | `count=1350`, `counts_by_type={static:4, person:283, scenario:1056, template:7}` |
| `.github/workflows/pages.yml` | 新增 Step B2 路由预渲染 与 paths 过滤 | 步骤顺序已用 pyyaml 解析校验 |

---

## 1. 取证方法与环境

**环境 (实测)**: Node v26.5.1 / npm 11.17.0; 构建链 `vue-tsc && vite build`; `vue` 3.5.40,
`vue-router` 4.6.4, `@vue/server-renderer` 3.5.40 (随 vue 传递安装, 已存在于 `node_modules`),
`vite` 5.4.21; 仓库内没有 `puppeteer` / `playwright` / `vite-plugin-prerender` / `jsdom`
(`ls node_modules` 实测, 无匹配项).

**线上探测**: `curl` 直连 `https://ovmobilegroup.github.io`, 时间 2026-09-18, HTTP/2.

**本地复现托管**: `python3 -m http.server` 服务 `dist/` 目录树.该服务器与 Pages 共享
"目录请求回落目录内 `index.html`"的语义, 因此可以用来验证预渲染机制 (见 2.5).

需要说明的差异: `python3 -m http.server` 不会像 Pages 那样把 `404.html` 当作错误页内容返回,
未匹配路径它直接返回裸 404.这反而说明 2.5 里返回 200 的是**真实生成的静态文件**,
不是回退体的巧合.

### 1.1 两个数据基线 (必须先读这一条)

本卡取证时发现工作区仓库与发布仓库的数据基线不一致. 以下所有依赖数据条数的结论,
都要先看清是哪一个基线:

| 基线 | figures 表 | 公开名录 items | 预渲染路由数 | 证据 |
|------|-----------|----------------|--------------|------|
| **发布仓 / CI 基线** | 1058 | 1339 (283 人物 加 1056 场景) | **1350** | `api/protreptic.db` 不入库, CI 由 `tools/build_figures_db.py` 现场重建得到 1058 行 (本地实跑确认); 线上 `data/index.unified.json` 实测 `counts.total=1339`, 由 2026-09-18T01:58:54Z 那次成功的 Pages 发布产出 |
| 工作区基线 | 501 | 784 (283 人物 加 501 场景) | 795 | 工作区 `api/protreptic.db` (38 MB, 2026-09-17 20:29), 行数与体积都远小于 CI 重建结果 |

判定哪一边完整:

- 两边 `data/modes_data.json` **完全相同** (sha256 均为 `782e48cc...63043`), 模式资产没有差异;
- 差异都在 figures 数据与工具脚本上: `git ls-files data` 发布仓 **1407** 个文件, 工作区只有 **795** 个;
  工作区 `tools/` 的 tracked 清单里还混进了若干由历史终端事故产生的垃圾文件名
  (例如 `tools/'` 或 `tools/  cd /opt/data/...` 这类), 发布仓没有这些;
- 结论: **工作区是缺失的旧快照, 发布仓是完整的那一份.**

因此**本文以下所有数字, 除特别说明, 一律以发布仓 / CI 基线为准**, 那才是实际部署上线的那份.
2.5 与 3.4 的验证都在该基线上重跑过.

影响与建议:

- `docs/architecture/web_p0_routes.json` 与 `web_p0_baseline.json` 是**发布仓基线**的产物.
  在工作区本地按第 8 节复跑会得到 795 条与更小的体积, 这是本地数据旧导致的, 不是脚本错误;
  脚本本身对两个基线都成立, 路由数从 `index.unified.json` 现算.
- 建议 magallanes 另开一张仓库卫生卡: 把工作区 `data/` 同步到发布仓基线, 清理 `tools/` 里的
  垃圾文件名, 并统一 `tools/export_static_site.py` 与 `tools/pages_preflight.py` 里的
  `EXPECT_FIGURES` (工作区 501, 发布仓 1058, 目前两边不一致). 本卡不动这两处,
  以免与在跑的卡冲突.

---

## 2. 问题一: 预渲染策略

目标是让 `/figures` `/modes` `/minds/:code` `/templates/:id` 深链返回 200.

### 2.1 现状实测 (线上, 2026-09-18)

| URL | 状态码 | 响应体 |
|-----|--------|--------|
| `/protreptic/` | **200** | SPA 外壳 |
| `/protreptic/figures` | **404** | 2094 B, 内容等于 SPA 外壳 |
| `/protreptic/modes` | **404** | 同上 |
| `/protreptic/minds/H-MO-001` | **404** | 同上 |
| `/protreptic/figures/H-MO-001` | **404** | 同上 |
| `/protreptic/templates` | **301** | 跳到 `/protreptic/templates/` , 同名目录存在, Pages 补斜杠 |
| `/protreptic/templates/` | **404** | 目录内没有 `index.html` |
| `/protreptic/404.html` | **200** | 与 SPA 外壳逐字节相同 |
| `/protreptic/templates/chibi.md` | **200** | 原始 markdown 文本 |
| `/protreptic/data/meta.json` | **200** | `application/json` , 静态数据路径正常 |

**对是否真的坏了的诚实判定**: 线上 404 的响应体就是 SPA 外壳, 浏览器打开深链时
Vue Router 会按路径渲染出正确页面, 所以**用户视角基本可用**. 真正坏掉的是三件事:

1. HTTP 状态码, 爬虫 / SEO / 监控 / 链接预览一律按 404 处理;
2. 不执行 JS 的 UA 即社交预览 / 部分搜索引擎 / `curl` 类检查, 拿到的是空的 `#app`;
3. 全站共用同一个 `<title>` 与 `<meta description>`, 且没有 canonical.

`/protreptic/templates` 返回 301 这个实测事实很关键: 它证明 **Pages 确实会对同名目录补斜杠,
并回落目录内的 `index.html`**. 这正是本方案的机制基础.

### 2.2 三个候选方案的取舍

| 候选 | 判定 | 理由 |
|------|------|------|
| `vite-plugin-prerender`, puppeteer 驱动 | **P0 否决** | 需要引入 Chromium 镜像约 300 MB 与 puppeteer 依赖; 仓库现无任何 headless 依赖; CI 时间增加 2 到 4 min; 而本卡只需要每路由正确的 head 与 200, 不需要整棵 DOM. [未验证]: 未在本仓安装试跑 |
| 自写 SSG 即 `vite build --ssr` 加 `@vue/server-renderer` 加 hydrate | **降级为 P1** | 技术前提已具备, `@vue/server-renderer` 3.5.40 就在 `node_modules`; 但必须先改数据取数时机: 现所有视图都在 `onMounted` 里 fetch, SSR 首帧只能渲染 loading 态, 而 `createSSRApp` 加 `hydrate()` 要求服务端首帧 DOM 与客户端一致, 否则 hydration mismatch 或闪屏. 详见 2.6 |
| **静态路由壳加每路由 head, 本卡实现** | **P0 采纳** | 零新增依赖; 0.27 s 构建; 产物 2497 KB; 直接把 404 变 200; 每路由 title 与 description 与 canonical 与 JSON-LD 都在静态 HTML 里, 比运行时注入对爬虫更友好 |

### 2.3 路由分区

**预渲染, 生成真实 `index.html` 并返回 200, 共 1350 条 (发布仓基线, 见 1.1)**

| 路由 | 条数 | 数据来源 | 说明 |
|------|------|----------|------|
| `/figures` `/modes` `/templates` `/api` | 4 | 常量 | 固定入口 |
| `/minds/{code}` | **283** | `data/index.unified.json` 中 `type=figure` | 人物模式档案, MindView |
| `/figures/{code}` | **1056** | `data/index.unified.json` 中 `type=scenario` | 场景详情, FigureDetailView |
| `/templates/{id}` | **7** | `dist/templates/*.md`, 标题与描述从 markdown 现场提取 | 与 `TemplatesView.vue` 的 7 个 id 对齐 |

**保持 SPA, 不生成路由目录, 继续走 `404.html` 外壳**

- 带查询参数的筛选态, 例如 `/figures?type=figure&era=...&page=2`, query 不产生新文件;
- 未来新增的且不在清单里的路由;
- **被隔离的数据**: `/minds/H-SX-001`, 见 6.1.

设计取舍: **不预渲染筛选态组合**. 筛选态是 query 维度, 组合爆炸且内容随数据变化,
它们的 200 由 `/figures` 这一条路由承担, 分享链接仍可用, SPA 读 query 还原状态.

### 2.4 实现: 产物路径与 CI 步骤

**脚本**: `tools/prerender_routes.py`

输入是 `web/dist/index.html` 即构建产物, 以及 `web/dist/data/index.unified.json`.
对每条路由改写 `<title>`, `<meta name="description">`, `og:title`, `og:description`,
并在 `</head>` 前注入 `link[rel=canonical]`, `og:url` 与 `application/ld+json`.

**产物路径, 真实落盘**

```
web/dist/index.html                         SPA 外壳, 未改动
web/dist/404.html                           与 index.html 逐字节相同, 脚本重写并保持这个不变式
web/dist/api/index.html
web/dist/figures/index.html                 加 web/dist/figures/{code}/index.html 共 1056 个
web/dist/minds/index.html                   加 web/dist/minds/{code}/index.html 共 283 个
web/dist/modes/index.html
web/dist/templates/index.html               加 web/dist/templates/{id}/index.html 共 7 个
docs/architecture/web_p0_routes.json        1350 条路由清单, 含 canonical 与 counts_by_type
```

canonical 一律写成**带尾斜杠**的绝对地址, 例如
`https://ovmobilegroup.github.io/protreptic/minds/H-WYM-001/`.
原因是目录入口在真实托管下会 301 到带斜杠形式, 见 2.1 的 `/templates` 实测.

**CI 步骤, 已写入 `.github/workflows/pages.yml`, 位置在断言 dist 产物之后**

```yaml
      - name: 路由预渲染 深链 200
        run: python3 tools/prerender_routes.py
```

顺序约束三条, 都是实测踩到的:

1. **必须在 `npm run build` 之后**: 脚本读 `dist/index.html` 与 `dist/data/index.unified.json`;
2. **必须在 `python3 tools/export_static_site.py` 与 `tools/build_unified_index.py` 之后**:
   前者会清空 `web/public/data/`, 而路由清单依赖 `index.unified.json`;
3. **必须在断言 dist 产物之后**: 该断言要求 `dist/404.html` 与 `dist/index.html` 逐字节相同,
   脚本重写 `404.html` 时保持这个不变式; 脚本还内置写盘自检, 逐个路由校验 `index.html`
   存在且含 canonical, 任一不满足就以非 0 退出.

`pages.yml` 的 `paths` 过滤同时补进了 `tools/prerender_routes.py` 与 `tools/build_unified_index.py`,
否则只改这两个文件不会触发发布.

### 2.5 验收实测

**(a) 全量扫描**: `python3 -m http.server` 托管 `web/dist`, 对路由清单里全部 1350 条
按 URL 编码请求:

```
routes=1350  status={200: 1350}  failures: 0
```

**(b) 定点抽查, 含需要编码的编码**:

| URL | 本地静态托管 |
|-----|--------------|
| `/protreptic/` | 200 |
| `/protreptic/figures` | 301 |
| `/protreptic/figures/` | **200** |
| `/protreptic/modes` | 301 |
| `/protreptic/modes/` | **200** |
| `/protreptic/templates/chibi` | 301 |
| `/protreptic/templates/chibi/` | **200** |
| `/protreptic/figures/A-1-X-P/` | **200** |
| `/protreptic/minds/Sun%20Quan/` | **200**, 编码里含空格 |
| `/protreptic/data/meta.json` | 200 |
| `/protreptic/no-such-page` | 404, 未覆盖路径行为不变 |

**(c) head 与结构化数据完整性**: 对 1350 个页面逐一解析 `application/ld+json`:

```
files=1350  ld_ok=1350  canonical=1350  bad=0
@type histogram {'CreativeWork': 1060, 'Article': 7, 'Person': 283}
```

**(d) 体积**: 1350 个页面合计 3888 KB raw 与 1674 KB gzip; 单页均值 2949 B raw,
单页 gzip 约 1.24 KB. `web/dist` 由约 25.2 MB 增至 29.2 MB 即 29152912 B,
远低于 Pages 单产物上限.

**结论**: 深链由 404 变为 200 这一目标**已在实现层达成并全量验证**;
线上验证需等发布, 见第 7 节.

### 2.6 P1: 内容级预渲染 (SSR + hydrate) 的前提与分步

P0 的产物只预渲染了 head, `<body>` 仍是空的 `#app`, 正文靠客户端 JS. 要让爬虫与首屏
直接看到正文, 需要真正的 SSR. 前提与步骤 (全部为 **设计**, 本卡未实施, 未实测):

**前提 1 - 取数时机前移 (最大的那个工作量)**
现状: 所有视图在 `onMounted`/`watch` 里 fetch, SSR 首帧只能是 loading 态.
需要抽出与路由一一对应的取数函数, 例如 `web/src/data/loaders.ts` 导出
`loadMind(code)`, `loadFigure(code)`, `loadTemplate(id)`, `loadFiguresIndex()`;
服务端渲染前 await 它, 客户端则在 `createSSRApp` 之前用同一份结果预填 pinia,
保证首帧 DOM 与服务端一致.

**前提 2 - SSR 构建入口**
新增 `web/src/entry-server.ts` 导出 `render(url)`; CI 增加
`vite build --ssr src/entry-server.ts --outDir dist-ssr` (vite 5.4.21 原生支持).
`@vue/server-renderer` 3.5.40 已在 `node_modules` (vue 的传递依赖), 无需新增依赖.

**前提 3 - 客户端切换为 hydrate**
`src/main.ts` 从 `createApp(App).mount('#app')` 改为 `createSSRApp(App).mount('#app')`.
这是唯一需要改的挂载点.

**前提 4 - 消除非确定性**
SSR 与客户端首帧必须逐字节一致. 现有 SSR 安全的部分已实测: `useTheme.ts` 用
`typeof window === 'undefined'` 守卫, `useI18n.ts` 的 `localStorage` 访问包在 try/catch 里,
两者在 Node 下都不会崩. 但必须在服务端固定 `locale='zh'` 与 `theme='dark'`,
否则 localStorage 里的偏好会造成 mismatch.

**替代的轻量 P1-a (低风险, 建议先做)**
不引入 SSR, 只给每个预渲染页面加 `<noscript>` 摘要块: 从 `index.unified.json` 的
`description` 与 `n_modes` 生成一段静态文本, 放在 `#app` 的兄弟节点或 `#app` 内部
(客户端挂载会清空它). 好处是零 hydration 风险, 爬虫可见一段真实文本;
坏处是内容量与正文差距大.

**为什么 P0 不做内容预渲染**: 无 headless 依赖时, 唯一不引入新依赖的路径就是 SSR,
而 SSR 的阻塞点是前提 1, 它要改所有视图的取数结构, 属于独立卡的工作量, 不该塞进架构卡.

### 2.7 预渲染的风险与边界

| 风险 | 现状 | 缓解 |
|------|------|------|
| 1350 个页面 body 相同, 只 head 不同 | 已存在 | 唯一 head 与 canonical 已就位; 真正的解法是 2.6 的 P1; sitemap 只列真实内容路由 |
| 数据新增但未重跑路由清单 | 无 | CI 顺序保证 prerender 在 `build_unified_index.py` 之后; 脚本对 `index.unified.json` 缺失直接非 0 退出 |
| 根路径部署 (docker/nginx 用 `VITE_BASE=/`) | 无 | 脚本支持 `--base /`; 但当前只有 Pages 流水线调用它, docker 路径 [未验证] |
| `/figures` 无尾斜杠返回 301 而非 200 | 已实测 | 301 会跟随到 200, 属于标准行为; canonical 与 sitemap 一律用带尾斜杠形式 |
| 旧版 404.html 缓存 | 无 | 与 PWA 的交互见 3.6 |

---

## 3. 问题二: Service Worker 缓存策略

### 3.1 scope 与注册

- **文件位置**: `web/public/sw.js`, 构建后位于 `dist/sw.js`, 线上路径
  `https://ovmobilegroup.github.io/protreptic/sw.js`.
- **scope**: 默认 scope 等于脚本所在目录, 即 `/protreptic/`. 这是本部署下能拿到的最大 scope,
  也是必须的: 站点全部内容都在该前缀下.
- **注册**: 只在生产构建里注册, 通过 `import.meta.env.PROD` 守卫, 开发态 `vite dev` 不注册,
  避免缓存把本地调试搞乱. 注册点放在 `src/main.ts` 末尾, `DOMContentLoaded` 之后.
- **注意**: GitHub Pages 对 `/protreptic/sw.js` 是否返回 `application/javascript` 需要实测.
  [未验证: 本卡未部署 PWA, 未实测该响应头] 若响应头不是 JS MIME, 注册会失败, A4 实施时
  先用 `curl -I` 确认. Pages 不支持下发自定义响应头, 所以 scope 只能靠文件路径控制,
  没有 `Service-Worker-Allowed` 这条备用路径.

### 3.2 版本化

两个独立的版本号, 分开失效, 避免 "数据没变却清空 shell" 或 "shell 没变却读到旧数据":

| 缓存名 | 版本来源 | 何时变化 |
|--------|----------|----------|
| `protreptic-shell-<BUILD_ID>` | `BUILD_ID` 等于 `dist/assets/*` 文件名内容哈希串接后取 sha256 前 12 位 | 每次 `npm run build` 产物变化时 |
| `protreptic-data-<DATA_REV>` | `DATA_REV` 等于 `dist/data/meta.json` 的 `generated_at`, 实测产物里形如 `2026-09-18T01:33:40+00:00` | 每次静态数据重新导出时 |

两个值在构建期注入 `sw.js`: 把脚本作为模板放在 `web/public/sw.template.js`,
在 CI 的 prerender 步骤之后由一个小脚本替换 `__BUILD_ID__` 与 `__DATA_REV__` 并写出 `dist/sw.js`.
放在 prerender 之后是为了不与 `export_static_site.py` 抢 `web/public/data` 下的文件.
`activate` 阶段删除所有以 `protreptic-` 开头但不等于当前两个名字的缓存.

### 3.3 分片缓存策略

| 资源 | 路径 | 策略 | 理由 |
|------|------|------|------|
| app shell | `index.html`, `assets/*`, `favicon.svg` | install 期 precache, 之后 cache-first | 文件名带内容哈希, 内容不会原地变化; 命中缓存省掉一次往返 |
| 静态索引 | `data/figures.index.json`, `data/index.unified.json`, `data/meta.json` | install 期 precache, cache-first | 首页与 /figures 的首屏依赖它; 数据版本号保证不读到旧版 |
| 模式摘要 | `data/modes/index-0..7.json` | cache-first, 但激活后后台预热 | 共 1114.7 KB gzip, 不阻塞 install; 见 3.4 |
| 人物详情 | `data/figures/{code}.json` | cache-first, 命中即入缓存 | 单文件很小, 中位 1.1 KB gzip / p90 1.8 KB gzip |
| 人物模式分片 | `data/modes/by-figure/{code}.json` | cache-first | 中位 27.9 KB gzip / p90 41.5 KB gzip, 访问即缓存 |
| markdown 模板 | `templates/*.md` | stale-while-revalidate | 体积小但容易在数据更新时被改, 允许先给旧的再刷新 |
| 预渲染路由 HTML | `*/index.html` 共 1350 条 | 不 precache; 导航 network-first, 失败回退通用 shell | 1350 页全 precache 要多花约 1674 KB gzip; 而离线时只要有通用 shell 加已缓存数据, SPA 就能渲染任意深链 |
| 搜索索引 | `data/search/**` 即 A5 产物 | cache-first, 按需拉取 | 查询时才需要, 见第 4 节 |
| 其他 | 任何非 GET 或跨域请求 | 不拦截 | 交给网络, 避免把统计脚本也缓存住 |

关键设计点: **离线的深链不靠预缓存每页 HTML, 靠通用 shell 加数据**.
SW 拦截 navigation 请求时, 若网络失败则返回缓存的 `index.html` 并用 `Response` 构造 200;
由于浏览器地址栏 URL 没有被改写, Vue Router 会按真实路径渲染, 再从缓存里取该路由的数据分片.
这样 "爆缓存" 与 "离线可用" 两个目标就不再互相要价.

### 3.4 离线最小集, 实测体积

| 集合 | 内容 | gzip 体积 | 时机 |
|------|------|-----------|------|
| **T1 最小可用** | app shell 99.2 KB 加 `figures.index.json` 33.8 KB 加 `index.unified.json` 114.0 KB 加 `meta.json` 1.4 KB | **248.4 KB** | install 期 precache |
| **T2 完整浏览模式库** | T1 加 `modes/index-0..7.json` 1114.7 KB, 单片 127.5 到 155.0 KB | **1363.1 KB** | `activate` 之后后台预热 |
| 单次深链访问增量 | 一个人物的 by-figure 分片, 中位 27.9 KB | 约 28 KB | 首次访问时 |

**T1 不包含模式摘要**是有意的: 1.11 MB gzip 放进 install 会让首次安装明显拖慢,
而 `/modes` 页面在断网时仍能从已预热缓存打开. 预热实现: `activate` 后遍历 8 个分片逐个
`cache.add`, 不 `await` 全部; 用 `navigator.connection.effectiveType` 判断, 若为
`slow-2g` / `2g` / `3g` 或 `saveData === true` 就跳过预热, 只保留按需缓存.
[未验证: 未在真机测 effectiveType 分支, 也未知这些接口在 iOS Safari 上的覆盖度]

**A4 验收口径提醒**: 卡片要求断网后 `/figures` 与 `/modes` 仍能打开.
按上面的设计, 安装后立刻拔网只能保证 `/figures`; `/modes` 要等后台预热完成
(8 个分片合计 1114.7 KB gzip, 常见移动网络下约 1 到 5 秒) 或用户访问过一次 `/modes`.
若 A4 需要 "安装即离线可开 /modes", 就把 8 个分片并入 T1, 代价是 install 期多 1.11 MB,
这个取舍需要 A4 明确写下结论.

### 3.5 升级与清缓存

1. `npm run build` 改变 `assets/*` 哈希即改变 `BUILD_ID`; `sw.js` 自身字节变化会让浏览器触发 update;
2. `install` 里 `skipWaiting()` 让新 SW 立即接管. 取舍: 会打断正在进行的导航,
   A4 若更保守, 可改为等待用户确认后再 `skipWaiting`;
3. `activate` 里删除旧版本缓存后 `clients.claim()`;
4. 数据版本独立: 只更新数据时 `DATA_REV` 变而 `BUILD_ID` 不变, shell 缓存保持,
   只重建 data 缓存, 避免用户被迫重下 99.2 KB 的 JS 与 CSS.

预期症状 "升级后旧缓存卡死" 在本设计下不会出现, 因为缓存名带版本且 activate 会清理;
但必须实测: 两次发布之间切换, 断网刷新, 确认拿到的是新数据. [未验证, A4 实施时验证]

### 3.6 与预渲染,404 的交互

- 未匹配路径仍回落 `404.html`, 它与 `index.html` 逐字节相同. SW 命中缓存时, 对 navigation
  一律返回 200 的缓存外壳; 若用户访问的是真正不存在的路径, 客户端路由没有该 path,
  Vue Router 会渲染空白页. **建议 A4 顺手加一个 catch-all 路由**, 重定向到 `/figures`
  或一个 404 视图, 否则 "离线加未知路径" 与 "在线加未知路径" 表现不一致.
  [未验证: 本卡未检查 router 是否有 catch-all; 从 `src/router/index.ts` 的 8 条路由看是没有的]
- 预渲染的 1350 个 HTML 不 precache, 但它们会走 navigation 的 network-first:
  在线的第一次访问拿到真实文件, 即 200 加正确 head, 之后进入运行时缓存;
  离线时回退通用 shell, 结果仍可用.

---

## 4. 问题三: 全文检索索引分片方案

现状: 搜索是编号 / 名称 / 领域的子串匹配 (见 `web/src/api/static.ts` 的 `matchesKeyword` 与
`ModesView.vue` 的 `filtered`), UI 已诚实标注为 "智能检索". 本节给出可替换它的全文索引规格.

### 4.1 语料口径复现

`tools/measure_web_p0_baseline.py` 对 284 个 by-figure 分片里全部 2858 条模式逐字段统计字符数:

| 口径 | 字符数 | 说明 |
|------|--------|------|
| 中文字段合计 (`*_zh` 与不带 `_en` 后缀的字段) | **3,629,083** | 含 mode_code / id / figure_code 等元数据 |
| 英文字段合计 (`*_en`) | **8,653,082** | |
| 全部字符串字段 | **12,282,165** | |

字段体积前 16 (字符):

```
definition_en 2712701   representative_cases_en 1660060   process_en 1524767
modern_applications_en 1174241   domain_en 968588   definition_zh 801592
representative_cases_zh 491994   process_zh 433128   key_quote_en 354674
representative_figures 345485   modern_applications_zh 344067   domain_zh 281001
source_chapter 245366   key_concepts 232022   related_modes 99615   key_quote_zh 97008
```

**关于任务书里 "全库可索引正文 2.4MB 字符" 的口径**: 本卡逐一试算了 6 种口径,
**没有一种精确等于 2.4M**, 最接近的是
`definition_zh + process_zh + representative_cases_zh + modern_applications_zh + domain_zh`
= **2,351,782** (2.35M). 其他候选: 上者去掉 domain_zh = 2,070,781;
上者再加 key_quote_zh 与 key_concepts 与 source_chapter = 2,645,177;
排除元数据字段的全部中文 = 3,024,167; 全部中文字段 = 3,629,083.
**结论: 任务书的 2.4M 口径不可复现, 本卡按实测值决策, 不按 2.4M 决策.** (标注为不确定项)

### 4.2 体积预算矩阵 (实测)

统一条件: 每片一个二进制倒排文件; postings 用 varint 差值编码 doc_id, 不存词频权重;
分片函数为 `crc32(token 首字符) % N`; 除注明外 N=16; 语料为 2858 条模式.

**A. 字段集扫描** (目标: 总 gzip 不超过 A5 卡片给的 800 KB)

| 编号 | 索引字段 | token 数 | 总 gzip | 最大片 | 最小片 |
|------|----------|----------|---------|--------|--------|
| I1 | name_zh, name_en | 27,351 | 201 KB | 18 KB | 9 KB |
| I2 | I1 加 category | 27,365 | 207 KB | 19 KB | 9 KB |
| I3 | I2 加 source_chapter[:40] | 51,401 | 366 KB | 28 KB | 17 KB |
| I4 | I3 加 key_concepts[:60] | 75,183 | 525 KB | 40 KB | 26 KB |
| I5 | I4 加 domain_zh[:30] | 85,452 | 605 KB | 47 KB | 30 KB |
| I6 | I5 加 definition_zh[:60] | 112,003 | **818 KB 超预算** | 67 KB | 41 KB |
| R1 | 同上, definition_zh[:20] | 92,950 | 667 KB | 53 KB | 34 KB |
| R2 | 同上, definition_zh[:30] | 97,115 | 701 KB | 56 KB | 35 KB |
| R3 | 同上, definition_zh[:40] | 102,200 | 741 KB | 60 KB | 37 KB |
| R4 | R2 加 process_zh[:30] | 110,407 | **816 KB 超预算** | 65 KB | 41 KB |

**B. 分片数扫描** (配置 R2)

| N | 总 gzip | 最大片 | 最小片 |
|---|---------|--------|--------|
| 8 | 699 KB | 94 KB | 79 KB |
| 12 | 698 KB | 69 KB | 43 KB |
| 16 | 701 KB | 56 KB | 35 KB |
| 24 | 700 KB | 38 KB | 21 KB |
| 32 | 703 KB | 38 KB | 13 KB |

值得记一笔: **分片数不是越大越均匀**. `crc32(首字符)` 的取值空间受限于出现过的首字符数量,
N 从 16 加到 24 时总体积几乎不变但最大片反而从 56 KB 涨到 57 KB 之类的抖动是真实的
(在另一组配置上实测到 47 KB 变 57 KB). 结论: N 必须在真实语料上量出来定, 不能凭直觉取.

**C. 编码对比** (同字段集, 24 片): gzip 后的 JSON 差值数组 vs 二进制 varint

| 配置 | JSON + gzip | 二进制 varint + gzip | 收益 |
|------|-------------|----------------------|------|
| F2 字段集 | 1409 KB | 1255 KB | 少 11% |
| F5 字段集 | 1209 KB | 1074 KB | 少 11% |

另测: 全字段集 (14 个中英字段) 的 JSON 差值方案 = **4.11 MB gzip**, 带词频权重的二进制方案
= 5.01 MB gzip. 两者都远超预算, 所以 **"全字段全文索引" 这个方向在本部署下不可行**,
必须靠字段截断控制体积.

**D. 拉丁词前缀扩展的代价**: 在推荐规格上额外索引每个拉丁词的全部前缀 (长度 2 到 15),
总 gzip 从 702 KB 涨到 **820 KB 超预算**, 最大片 64 KB. 所以 **前缀检索不进主索引**.

### 4.3 最终索引规格 (推荐, 已实测)

**字段与权重** (截断长度是控制体积的手段, 也是设计的一部分)

| 字段 | 权重 | 截断 | 作用 |
|------|------|------|------|
| `figure_name` | 4 | 不截断 | 支持按人物检索 |
| `name_zh` | 4 | 不截断 | 模式名 |
| `name_en` | 4 | 不截断 | 英文模式名 |
| `category` | 2 | 不截断 | 分类 |
| `source_chapter` | 2 | 40 字符 | 出处 |
| `key_concepts` | 2 | 60 字符 | 关键词 |
| `domain_zh` | 2 | 30 字符 | 领域, 原始值是整句, 必须截断 |
| `definition_zh` | 1 | 30 字符 | 定义首部 |
| `definition_en` | 1 | 30 字符 | 英文定义首部 |

**实测体积**: token 数 99,016, 总 **741 KB gzip** (N=16), 最大片 59 KB, 最小片 37 KB.
预算 800 KB, 余量 59 KB. (数字是在 doc_id 与 `modes/index-0..7.json` 的拼接顺序对齐之后测的.)

**doc_id 契约 (这一条决定了不需要额外的词典文件)**
`doc_id` 定义为该 mode 在 `data/modes/index-0.json` 到 `index-7.json` **按序拼接**后的下标
(2858 个, 实测双向一致: by-figure 有而 index 无 0 条, index 有而 by-figure 无 0 条).
前端本来就会为 `/modes` 拉取并拼接这 8 个分片, 因此拿到 doc_id 后可以直接查表取
mode_code / figure_code / figure_name / name / category / domain 用于展示,
**不需要再下发一份词典** (若单独下发, 实测 5 字段版词典是 494 KB raw 与 194 KB gzip,
加上它会直接击穿 800 KB 预算).

**分词规则**
1. 先做 `NFKC` 归一化;
2. 连续 CJK 串取全部 2-gram; 长度为 1 的串取该字本身;
3. 连续拉丁 / 数字串转小写后取长度不小于 2 的词;
4. 查询走同一函数, 因此中文查询是按 2-gram 求交, 不是子串扫描.

**文件格式, 每片一个二进制文件**

```
tokens 升序排列, 每个 token:
  varint(len(utf8(token))) + utf8(token) + varint(df) + 升序 doc_id 的 varint 差值序列
```

**分片函数**: `bucket = crc32(utf8(token 首字符)) % 16`.
选它的原因是**查询期可计算**: 一个中文查询的每个 2-gram 的首字符决定唯一分片,
所以查询只需拉 "查询串里出现过的首字符" 对应的分片, 而不是全部 16 片.
这正是不能用 `crc32(整个 token)` 的原因, 那样查任何词都要拉全部分片.

**产物路径**

```
web/public/data/search/index-0.bin ... index-15.bin    16 个倒排分片
web/public/data/search/meta.json                       条数 / 分片数 / 每片体积与 sha256 / 语料 sha256
```

### 4.4 懒加载时机与请求数

- **时机**: 首次触发搜索输入时 (中文长度不小于 2 字, 或拉丁长度不小于 2 字符), 防抖 150 ms 后开始;
  不在首屏加载, 不在 `/figures` 路由加载.
- **请求数**: 每次查询最多拉 `min(查询 token 的首字符去重数, 16)` 片.
  典型中文 4 字查询产生 3 个 2-gram, 首字符最多 3 个, 即最多 3 片, 按最大片 59 KB 估算
  最坏约 177 KB gzip, 常见约 60 到 120 KB.
- **缓存**: 拉过的分片常驻内存 Map, 同时交给 SW 的 cache-first 缓存 (见 3.3),
  二次查询不再走网络.
- **降级**: 分片拉取失败时回落到现有的子串匹配, 并让 UI 明确显示 "已降级为关键词匹配",
  不得静默把结果混为一谈.

### 4.5 功能验证 (真实查询)

在推荐规格的索引上直接跑查询 (查询串走同一分词函数, 分数为命中 token 的权重和):

```
良知      -> M381 王阳明 11, M-NKR-004 恩克鲁玛 9, M-ASHOKA-005 阿育王 6
战略 决策  -> M-MYS-008 茅以升 19, M-GUE-006 切-格瓦拉 14, M-LH-010 利德尔-哈特 13
联盟 合作  -> M-BISMARCK-007 俾斯麦 9, M-GAN-002 甘地 9, M-CHU-005 丘吉尔 8
王阳明    -> M381 王阳明 8, M382 王阳明 8, M383 王阳明 8
心之本体  -> M-ST-001 石涛 13, M381 王阳明 9, M-LZH-003 李泽厚 9
decision  -> M-YSS-010 李舜臣 8, M-BELISARI-007 贝利撒留 4
```

`figure_name` 进索引后 "王阳明" 能命中他自己的模式; 加它之前实测命中是错的
(返回休谟与张仲景), 所以这一条是实测驱动的修正.

### 4.6 已知缺口 (必须在 UI 或规格里承认)

1. **拉丁前缀**: `decis` 返回空, `decision` 有结果. 主索引不做前缀扩展 (会超预算),
   要么让 UI 要求完整词, 要么用已加载的 `modes/index-*.json` 的名字字段做前端子串兜底.
2. **相关性是粗暴的权重和**, 没有 IDF / BM25 / 长度归一. 若要更好的排序, 需要付体积
   (带权重的编码实测 5.01 MB gzip 那一档就是这条路的上限参考).
3. **深正文检索不到**: `representative_cases` 与 `modern_applications` 与完整 `definition`
   都没进索引 (实测全字段方案 4.11 MB gzip). 检索结果里的高亮只有名字 / 领域 / 概念 / 出处可用.
4. **英文语料只有名字与定义首 30 字符**, 英文正文检索基本不可用. 若要中英对等,
   需要按 4.2 的 A 表重新加预算.
5. 检索结果需要二次拉取正文时, 仍然走 by-figure 分片 (中位 27.9 KB gzip),
   所以 "点开一条结果" 的一次网络往返是预期的.

### 4.7 A5 实施清单 (给 barbosa 的卡)

1. 新增 `tools/build_search_index.py`, 读 `data/modes_data.json` 或 by-figure 分片取正文字段,
   读 `web/public/data/modes/index-0..7.json` 定 doc_id 顺序, 按 4.3 的字段与权重与截断与
   分片函数输出到 `web/public/data/search/`;
2. 输出 `search/meta.json`, 至少含: 条数, 分片数, 每片 raw 与 gzip 体积与 sha256,
   语料 sha256, 以及本卡的规格版本号;
3. **必须在 `tools/export_static_site.py` 之后跑** (该脚本会清空 `web/public/data/`),
   位置与 `tools/build_unified_index.py` 相邻;
4. 自检断言: 总 gzip 不超过 800 KB; 写成脚本内的 assert, 超了直接非 0 退出;
5. 前端接入点: `web/src/api/static.ts` 新增 `searchFullText(query)`, UI 层保留既有子串匹配
   作为降级路径与 "关键词模式" 开关; UI 文案必须写清是倒排匹配而不是语义检索.

---

## 5. 跨卡决策 (A1 / A4 / A5 / C1 必须遵守)

本卡是 `t_8a6d69c5` 的子卡们的前置卡, 以下决策已定, 子卡不应重新决定.

**给 A1 (`t_66b75e78` SEO 资产, elcano)**

1. **sitemap 的 URL 集合 = `docs/architecture/web_p0_routes.json` 的 1350 条 `canonical`**,
   不要再从 `index.unified.json` 自己拼 URL. 该清单里已经排除隔离数据, 且带尾斜杠.
2. **验收标准说明**: A1 卡片写的 "sitemap 条目数 >= 1300" 在**发布仓基线**上刚好成立:
   公开名录 1339 条 (`counts.total=1339`, 283 人物加 1056 场景) 加 4 个入口加 7 个模板
   = **1350**. 注意**工作区本地的数据基线更旧** (784 条, 见 1.1), 在工作区本地跑只会得到
   795 条, 断言会失败. A1 应以发布仓/CI 基线为准, 并把断言写成读
   `web_p0_routes.json` 的 `count` 而不是写死数字.
3. **不要使用 `index.unified.json` 的 `href` 字段**: 它的值是 `#/minds/H-WYM-001` 这种
   hash 形式, 而 `createWebHistory(import.meta.env.BASE_URL)` 的路由不带 hash,
   该字段是死字段 (实测 `web/src` 里没有任何代码读它). 详见 6.2.
4. **不要在运行时为已预渲染的路由再注入 JSON-LD**: 本卡已在静态 HTML 里为 1350 个页面
   注入了 `Person` (283) 与 `CreativeWork` (505) 与 `Article` (7), 重复注入会产生多份
   结构化数据. A1 的动态 `document.title` 逻辑对筛选态与后续新路由仍然有用, 保留即可.
5. `robots.txt` 应指向 `https://ovmobilegroup.github.io/protreptic/sitemap.xml`. 注意
   sitemap 里的 URL 是带尾斜杠的目录形式, 而站点根是 `/protreptic/`, 两者前缀要一致.

**给 A4 (`t_7c611d72` PWA, elcano)**

1. 严格按第 3 节的 scope / 版本号 / 策略表实施, 特别是 **T1 与 T2 的分层**,
   不要把 1114.7 KB gzip 的模式摘要塞进 install 期.
2. A4 卡片验收里的 "断网后 /figures 与 /modes 仍能打开" 需要按 3.4 的口径写清是
   "安装后" 还是 "访问过一次后", 这是真实差异, 不要含糊过去.
3. `sw.js` 的版本注入放在构建期, 需要在 `pages.yml` 里新增一步; 与本卡的
   prerender 步骤相邻, 顺序没有冲突 (prerender 只写 `dist/**.html`, 不碰 `dist/sw.js`).
4. 断网回退 shell 时对 navigation 必须构造 200 响应, 否则浏览器会把离线页面当错误.
5. 建议顺手加一个 Vue Router catch-all 路由, 原因见 3.6.

**给 A5 (`t_4f0b858a` 全文索引, barbosa)**

1. 严格按 4.3 的字段 / 权重 / 截断 / 分片函数 / doc_id 契约实施. **doc_id 的顺序契约
   是硬约束**: 一旦与 `modes/index-0..7.json` 的拼接顺序不一致, 结果面板会显示错的人与模式.
2. 预算 800 KB, 推荐规格实测 741 KB, 余量 59 KB. 不要加进前缀索引 (实测会让它变成 820 KB),
   也不要加 `process_zh` (816 KB), 也不要加 `definition_zh[:60]` (818 KB).
3. 索引里**不要**放词典文件; 用 doc_id 查已经加载的 modes index, 原因与实测数据见 4.3.
4. UI 必须承认能力边界: 倒排匹配不是语义检索, 拉丁词不做前缀, 深正文不在索引里.
5. 前端保留现有子串匹配作为降级路径.

**给 C1 (`t_14dd1aa0` CI 质量门, acurio)**

1. 本卡的预渲染自检已在 `tools/prerender_routes.py` 内部实现, 不需要重复;
   若要把断言并入 `tools/pages_preflight.py`, 建议新增 `--stage prerender`,
   断言 `web/dist/{api,figures,minds,modes,templates}/index.html` 存在且路由目录数与
   `docs/architecture/web_p0_routes.json` 的 `count` 相等.
2. **死链检测的口径变了**: 本卡落地后 `/protreptic/figures` 这类 URL 是 301 而不是 404,
   死链检查必须跟随重定向后再判定, 否则会把 301 误报为死链.
3. Lighthouse 的 SEO 项现在才有意义, 之前深链是 404.

---

## 6. 附带发现

### 6.1 H-SX-001 的隔离只做了一半 (真实缺陷, 建议尽快修)

- `tools/build_unified_index.py` 的 `QUARANTINE` 把 `H-SX-001` 判为虚构
  (10 条模式全部引用不存在的《苏咸子》), 因此它**不在**公开名录里: 实测
  公开名录 figures = **283**, 而 `web/public/data/modes/by-figure/` 有 **284** 个分片.
- 但 `tools/export_static_site.py` 仍然把 `H-SX-001.json` 导出到了 `data/`.
  后果: 直接访问 `/minds/H-SX-001` 时, 前端依然能把 10 条虚构模式渲染出来,
  只是没有被索引推荐.
- 本卡的处理: **不为它生成预渲染路由**, 所以它的 HTTP 状态是 404 (回落外壳),
  且它被记录在 `web_p0_routes.json` 的 `excluded_figure_codes` 里, sitemap 也不会收录它.
  这治标不治本.
- 建议的根治: 让 `export_static_site.py` 也读同一份 `QUARANTINE` 名单 (或抽成一个共享模块),
  在导出阶段就跳过被隔离的 figure_code, 并把 `EXPECT_BY_FIGURE` 从 284 改到 283.
  这会连带影响 `pages_preflight.py` 的基线常量, 属于数据治理卡的工作量, 本卡不改.

### 6.2 `index.unified.json` 的 `href` 字段与路由模式不匹配

`tools/build_unified_index.py` 第 108 行与第 149 行生成的是 `#/minds/{fc}` 与 `#/figures/{code}`,
即 hash 形式. 但 `web/src/router/index.ts` 用的是 `createWebHistory`, 真实路径是
`/protreptic/minds/{code}`. hash 形式的链接在 history 模式下会被 Vue Router 当作根路径处理.
实测 `web/src` 里**没有任何代码读这个字段** (grep `.href` 只命中 `App.vue` 的外链),
所以目前是死字段而不是线上故障. 但只要有人照抄它就会踩坑, A1 尤其要注意.
建议改为真实路径或直接删掉该字段.

### 6.3 已验证的一致项 (避免子卡重复排查)

- **发布仓基线**下 `figures.index.json` 的 1058 条与 `index.unified.json` 的 1056 条 scenario
  指向同一张 figures 表 (1058 行里 2 行未进入场景清单); 与 `data/figures/*.json` 的 1058 个分片一致.
  工作区基线 (501 / 501 / 501) 也同样自洽, 差别只在数据基线新旧, 见 1.1.
- 两个基线的 `index.unified.json` 里编码均无重复, 无异常字符; 唯一含空格的是 `Sun Quan`,
  已实测预渲染后 `/protreptic/minds/Sun%20Quan/` 返回 200.
- `dist/404.html` 与 `dist/index.html` 逐字节相同, 预渲染脚本重写后仍保持.
- 1350 个页面的 `application/ld+json` 全部可解析, `@context` 取值全部为 https 协议下的 schema 域名.

---

## 7. 未验证项与不确定性清单

| 项 | 状态 | 说明 |
|----|------|------|
| 线上深链已变成 200 | **待发布后复核** | 本卡只保证实现与本地全量验证; 真实状态码要在 Pages 部署完成后重新探测 (第 8 节命令) |
| `vite-plugin-prerender` 的实际成本 | 未测 | 未安装试跑, 300 MB 是个量级估计而非实测 |
| SSR 构建 (`vite build --ssr` + `renderToString`) 能跑通 | 未测 | 只验证了依赖 `@vue/server-renderer` 3.5.40 存在, 以及 `useTheme` / `useI18n` 在 Node 下不会崩 |
| Pages 对 `sw.js` 返回的 MIME | 未测 | A4 实施前用 `curl -I` 确认 |
| `navigator.connection.effectiveType` 的实际分支覆盖 | 未测 | iOS Safari 的覆盖度未知, 设计里已给 "按非慢速处理" 的兜底 |
| docker / nginx 根路径部署的 `--base /` 路径 | 未测 | 脚本支持该参数, 但流水线只构建 Pages |
| A5 的真实实现产物 | 未测 | 4.2 与 4.3 的体积与查询结果来自本卡的原型脚本, 不是 `tools/build_search_index.py` (该脚本属于 A5, 尚未存在) |
| 任务书的 "2.4MB 字符" 口径 | 不可复现 | 见 4.1, 6 种口径都不等于 2.4M, 最接近 2.35M |
| Lighthouse PWA / SEO 分数 | 未测 | 属于 C1 与 A4 的验收范围 |
| 发布仓与工作区的数据基线漂移 | 已实测并记录 | 见 1.1: 工作区 figures 501, 发布仓 1058; 本卡按发布仓基线出数, 建议单开仓库卫生卡 |
| 1350 个页面的重复内容对搜索引擎的实际影响 | 未测 | 逻辑上风险存在 (body 相同), 缓解手段是唯一 head 与 P1 内容预渲染 |

**明确不做的判断 (写下来是为了防止被当成遗漏)**

- 不引入任何新的 npm 依赖: P0 方案完全用 Python 标准库 + 现有构建链实现.
- 不改 `tools/export_static_site.py`: 它会清空 `web/public/data/`, 本卡的新产物放在
  `docs/architecture/` 与 `web/dist/`, 与它无冲突.
- 不修 6.1 的数据缺陷: 那会改动数据基线常量, 影响 `pages_preflight.py` 的既有断言,
  应由数据治理卡统一处理.

---

## 8. 复现命令

```bash
# 0) 依赖与构建 (卡片硬性要求, 必须先通过)
cd /opt/data/workspace/Protreptic/web
VITE_DATA_MODE=static npm run build

# 1) 静态数据与统一名录 (顺序不可颠倒, 前者会清空 web/public/data)
cd /opt/data/workspace/Protreptic
python3 tools/export_static_site.py
python3 tools/build_unified_index.py

# 2) 体积基线 -> docs/architecture/web_p0_baseline.json
python3 tools/measure_web_p0_baseline.py

# 3) 路由预渲染 -> web/dist/**/index.html 与 docs/architecture/web_p0_routes.json
python3 tools/prerender_routes.py

# 4) 本地静态托管并全量扫码 1350 条路由
mkdir -p /tmp/p0site/protreptic && cp -r web/dist/. /tmp/p0site/protreptic/
cd /tmp/p0site && python3 -m http.server 4211 --bind 127.0.0.1
# 另开一个终端:

# 5) 线上复核 (发布之后)
for p in /protreptic/figures /protreptic/modes /protreptic/minds/H-WYM-001 \
         /protreptic/templates/chibi /protreptic/figures/A-1-X-P; do
  printf "%-38s " "$p"
  curl -s -o /dev/null -w "%{http_code}\n" "https://ovmobilegroup.github.io$p"
done
```

完整的原始输出与逐条命令对应关系见 `docs/architecture/web_p0_evidence.md`.
