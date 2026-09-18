# Phase30-A4 · PWA：manifest + service worker（离线可用）

> 卡片：`t_7c611d72`（elcano）· 线上：https://ovmobilegroup.github.io/protreptic
> 前置：[Phase30-A0] `docs/architecture/web_p0_architecture.md` 第 3 节给出了 issue 规格，
> 本文只记录**真正落地的实现、实测数字与诚实边界**。

## 1. 产物（真实落盘路径）

| 文件 | 作用 |
|------|------|
| `/opt/data/workspace/Protreptic/web/public/manifest.webmanifest` | 深色版 manifest（theme_color/background_color = `#04060c`） |
| `/opt/data/workspace/Protreptic/web/public/manifest-light.webmanifest` | 浅色版 manifest（`#f8f5f0`），与深色版**只有这两个颜色不同** |
| `/opt/data/workspace/Protreptic/web/public/icons/icon-{192,512}.png` | `purpose=any`，不透明深墨 + 鎏金框 + 「思」 |
| `/opt/data/workspace/Protreptic/web/public/icons/icon-maskable-{192,512}.png` | `purpose=maskable`，外框收到 66% 见方留安全区 |
| `/opt/data/workspace/Protreptic/web/public/icons/apple-touch-icon.png` | 180×180，iOS 主屏 |
| `/opt/data/workspace/Protreptic/web/public/favicon.svg` | 与图标同款（原来是与站点设计无关的靛蓝罗盘） |
| `/opt/data/workspace/Protreptic/web/sw.template.js` | service worker 模板（占位符由构建期注入）**不在 public/ 下** |
| `/opt/data/workspace/Protreptic/tools/build_sw.py` | 注入 `BUILD_ID`/`DATA_REV`/预缓存清单，产出 `web/dist/sw.js` |
| `/opt/data/workspace/Protreptic/tools/build_pwa_icons.py` | 画图标（Pillow，4× 超采样），自带尺寸/不透明/字形覆盖自检 |
| `/opt/data/workspace/Protreptic/web/src/composables/useServiceWorker.ts` | 注册 / 更新 / 离线状态 / 版本号 |
| `/opt/data/workspace/Protreptic/web/src/components/OfflineNotice.vue` | 断网提示 + 新版本提示 |
| `/opt/data/workspace/Protreptic/web/src/views/NotFoundView.vue` + `router/index.ts` catch-all | 未收录路径兜底页（noindex、无 canonical） |

`web/dist/sw.js` 与 `web/dist/sw.build.json` 是**构建产物**（不入库），线上对应 `/protreptic/sw.js`。

### 为什么模板文件不放 `web/public/`

放 `public/` 会被 Vite 原样拷成 `dist/sw.template.js` —— 线上多一份带 `__BUILD_ID__`
占位符的死文件。模板属于构建工具链，放在 `web/sw.template.js`，默认路径写在
`tools/build_sw.py` 里。

## 2. 缓存契约

```
protreptic-shell-<BUILD_ID>    index.html / assets/* / favicon.svg / manifest* / icons/* / templates/*.md
protreptic-data-<DATA_REV>     data/**（含 install 期尽力预缓存的三个索引文件）
```

* `BUILD_ID` = `dist/assets/*` 文件名串接后的 sha256 前 12 位；`DATA_REV` = `dist/data/meta.json` 的 `generated_at`（纯数字 14 位）。
* `activate` 删除所有 `protreptic-` 前缀但不在当前名单里的缓存；`install` 里 `skipWaiting()`、`activate` 里 `clients.claim()`。
* 页面**不自动 reload**：新版接管后只把 `updateReady` 置真，由右下角提示「新版本已就绪，刷新」。
* scope 只能是 `/protreptic/`（Pages 不能下发 `Service-Worker-Allowed`）；manifest 里 `start_url`/`scope` 用相对 `./`，由浏览器按 manifest URL 解析 —— 这样 docker/nginx 的根路径部署（`VITE_BASE=/`）不用改文件。

### 请求策略

| 请求 | 策略 |
|------|------|
| `mode === 'navigate'` | **network-first**（4 s 超时）。拿到任何响应就原样返回，**包括 Pages 对未收录路径的真 404**；只有网络真失败时才回退缓存的 `index.html` 并**构造 200**（地址栏 URL 不变，Vue Router 按真实路径渲染，数据再走缓存） |
| `data/**` | cache-first（命中即返回，未命中成功请求写入 data 缓存） |
| 其余同源 `BASE` 之下 | cache-first（`og/**` 等运行时顺带缓存） |
| 非 GET / 跨域 / 带 `Range` | 不拦截 |

## 3. 体积实测（发布仓基线，2026-09-18 构建）

| 集合 | 内容 | gzip |
|------|------|------|
| **T1 安装期预缓存** | shell 107.7 KB（index+assets+favicon+manifest×2）+ 图标 80.5 KB + 模板 41.6 KB + 索引 152.7 KB（figures.index/unified/meta） | **384.3 KB**（raw 1144.1 KB） |
| **T2 激活后预热** | T1 + `modes/index-0..7.json` 1114.7 KB | **1499.0 KB** |
| `sw.js` 自身 | 11.4 KB raw | **4.5 KB** |
| 单次深链增量 | 一个人的 `modes/by-figure/{code}.json` | 中位约 28 KB |

**取舍（回应 A0 评论里的问题）**：8 个模式分片**不并入 install**，仍走「激活后后台预热」。
理由：install 期多 1.11 MB 会让首访（尤其移动端）付出一次不可见的下载成本，而
「装完就能离线查模式库」并不是本卡的验收条件。代价是**安装后立刻拔网只能保证
`/figures`、`/templates/*` 可用**，`/modes` 需要预热完成（1.11 MB）或用户访问过一次。
这一点由 UI 如实呈现：离线提示里直接写「模式分片已缓存 N/8」（`WARM_STATUS` 按需向 SW 取数）。

## 4. 离线行为（实测）

同一浏览器：先在线加载一次 → 停掉本地 Pages 模拟服务器（连接被拒 = 真断网）→ 直接地址栏深链。

| 路由 | 离线结果 | 依据 |
|------|----------|------|
| `/protreptic/figures` | ✅ 24 张卡片、计数 283/1055 正常 | 索引三件套在 data 缓存 |
| `/protreptic/modes` | ✅ 120 张卡片，2858 条 | 预热分片 |
| `/protreptic/templates`、`/templates/chibi` | ✅ 7 个模板 / 赤壁模板正文 5284 字 | 模板 md 预缓存 |
| `/protreptic/minds/H-WYM-001` | ✅ 王阳明 10 条模式（**在线访问过一次**） | 运行时缓存 by-figure 分片 |
| 未收录路径 `/protreptic/no-such-page/` | ✅ 兜底页「这一页不在典藏里」，`robots=noindex,follow`、无 canonical | catch-all 路由 |
| 从未在线打开过的 `/minds/{code}`、`/figures/{code}` | ⚠️ 显示「未找到该人物的模式档案」 | 对应分片不在缓存（诚实边界，见下） |

**诚实边界**：`data/modes/by-figure/*`（284 个，合计 8.1 MB gzip）与 `data/figures/*`
（1058 个）**不预缓存**，只有访问过一次才会进 data 缓存。因此「离线可用的深度」=
索引级浏览全量可用 + 细节页按访问历史可用。前端在缺失时给出的是明确的「未找到」，
不是空白页。

## 5. 验收实测

**Lighthouse 11.7.1（PWA 类别）**：`PWA = 1.0`，加权项全过
（`installable-manifest` / `maskable-icon` / `splash-screen` / `themed-omnibox` /
`content-width` / `viewport`）；`runWarnings: []`。
命令：

```bash
CHROME_PATH=<chrome-headless-shell> npx lighthouse@11.7.1 \
  http://127.0.0.1:4451/protreptic/ --only-categories=pwa \
  --chrome-flags="--no-sandbox --disable-dev-shm-usage" \
  --output=json --output-path=/tmp/a4/lh-pwa.json --quiet
```

**CDP installability**（Lighthouse 装即用同源判定）：`Page.getInstallabilityErrors -> []`，
`Page.getAppManifest -> errors: []`，`scope` 被解析成 `http://127.0.0.1:4451/protreptic/`
（相对 `./` 生效）。

**注册与缓存**（浏览器实测）：

* `navigator.serviceWorker.controller.scriptURL = /protreptic/sw.js`，scope `/protreptic/`；
* 首次装完：`caches = [protreptic-shell-<BUILD_ID>, protreptic-data-<DATA_REV>]`，
  shell 18 项（11 关键 + 7 模板）、data 11 项（3 索引 + 8 预热分片）；
* **升级不卡旧缓存**：换 BUILD_ID 后重载 → 旧 `protreptic-shell-<旧ID>` 被删除，
  新 shell 就位，`protreptic-data-<DATA_REV>`（未变）保留；页面照常渲染，
  右下角出现「新版本已就绪，刷新」；点刷新后提示消失、页面正常。

**接入既有预算门**：发布仓 `.github/workflows/quality-gate.yml` 的 lighthouse job 跑
`@lhci/cli autorun`（配置 `lighthouserc.json`），原先只收集
performance / accessibility / best-practices / seo。本卡把 `pwa` 加进 `onlyCategories`，
并加一条**非阻塞**断言 `categories:pwa >= 1`（`warn`）—— 线上部署完成后这道门会持续
盯住安装能力，配错 manifest/图标会立刻在报告里显形，但不会因为尚未部署而把 CI 弄红。

## 6. 顺手修掉的两个真问题（同一类坑）

1. **`tools/prerender_routes.py` 注入自闭合 `<script .../>`** —— HTML 解析器把
   `<script>` 当 raw text 元素，自闭合标签被忽略，其后所有标签（含入口 module
   script）被吞成脚本文本。实测后果：**1350 个预渲染页全部空白**（`<body>` 里连
   `#app` 都没有）。改成 `<script ...></script>`。同一个坑 `web/index.html` 上
   踩过一次（Phase30-A3 修复），这次是同一类问题的第二处。
   `tools/build_sw.py` 现在会在构建期断言 `dist/index.html`、`dist/figures/index.html`、
   `dist/modes/index.html` 里存在 `<div id="app">` 且没有自闭合 `<script/>`：
   SW 的离线外壳就是这个 `index.html`，它必须真的能挂载。
2. **索引文件必须进 data 缓存**：最初把 `figures.index.json` / `index.unified.json` /
   `meta.json` 一起塞进 shell 缓存，但页面请求走的是 `cacheFirst(DATA_CACHE)` ——
   装了却用不上。实测症状：离线 `/figures` 计数 `人物 0 / 场景 0`、`暂无结果`。
   现在 install 期把三个索引写进 `DATA_CACHE`（仍不阻塞安装）。

## 7. 主题色随浅深色

manifest 是静态文件，`theme_color` 无法按主题变；静态托管也没有服务端可以按 cookie 出不同 manifest。
做法：

* `index.html` 里 `<link rel="manifest" href="/manifest.webmanifest" id="pt-manifest">`；
* 首屏内联脚本在**首次绘制前**按 `localStorage['protreptic-theme']` 把 href 换成
  `manifest-light.webmanifest`、把 `<meta name="theme-color">` 换成 `#f8f5f0`（用
  `document.baseURI` 拼路径，根路径部署同样正确）；
* `useTheme.ts` 的 `apply()` 在同一处同步 `#pt-theme-color` 与 manifest href，切换主题立即生效。

## 8. CI 接线（`.github/workflows/pages.yml`）

* `paths:` 增加 `tools/build_sw.py`、`tools/build_pwa_icons.py`；
* **Step B2.6**（在 `prerender_routes.py` / `apply_og_meta.py` 之后，sitemap 之前）：
  `python3 tools/build_sw.py` —— 此时 `dist/assets`、`dist/data`、`dist/icons`、`dist/templates` 都已就位；
* 合并成 `_site/` 后新增断言：`_site/sw.js`、两个 manifest、`icons/icon-512.png` 必须存在，
  并跑 `python3 tools/build_sw.py --check`（比对 dist 现状与 `sw.build.json`）。

### `build_sw.py` 自带断言（任一不过非 0 退出）

1. `dist/assets` 里必须有 `.js` 与 `.css`（空 assets = 入口 script 被吞）；
2. 预缓存清单里每个 URL 必须真实存在；图标、模板、`modes/index-*.json` 都不能少；
3. 注入后不允许残留 `__XXX__` 占位符；
4. 外壳/预渲染页必须可挂载（见第 6 节第 1 条）。

## 9. 本地复现

```bash
python3 tools/build_pwa_icons.py --check                    # 图标产物自检
cd web && VITE_DATA_MODE=static npm run build               # vue-tsc + vite（VITE_DATA_MODE 必须带上）
cd .. && python3 tools/build_sw.py                          # 注入 -> web/dist/sw.js
python3 tools/build_sw.py --check                           # 与 dist 比对
# 私有副本 + Pages 式静态服务（缺文件回落 404.html，状态码 404）
python3 tools/prerender_routes.py --dist <copy> --routes-out /tmp/routes.json --no-body
python3 tools/build_sw.py --dist <copy>
```

`tools/build_sw.py --dist <dir> --base /` 支持 docker/nginx 的根路径部署；
`web/nginx.conf` 已给 `sw.js` 与两个 manifest 加 `Cache-Control: no-cache`
（原先 `\.js$` 会被 `expires 1y; immutable` 命中，service worker 会被缓存一年）。
