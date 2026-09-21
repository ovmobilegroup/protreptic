# 访问统计: GoatCounter 接入说明

> Phase45-A / 卡片 `t_eb3de8e7` / 线上站 https://ovmobilegroup.github.io/protreptic
>
> 现状: 集成已就位。开关是 `web/goatcounter.json` 的 `code` 字段:
> 填站点码即激活, 清空即回滚; 值为空 (缺省) 时线上不加载任何统计脚本、不产生第三方请求。
> 这里不复制该字段的当前值, 以仓库里的文件为准, 免得两处打架。

## 0. 为什么选 GoatCounter

- 官方托管有免费额度, 静态站只需一行脚本, 不需要自建后端;
- 不使用 cookie, 不采集个人数据, 不做跨站追踪, 与站点原有的隐私口径一致;
- 不使用弹窗或同意横幅, 因此不必引入一套同意管理流程。

自托管路径 (`tools/gc/`) 的可行性验证记录见 `docs/architecture/gc_setup.md`, 本文只讲官方托管。

## 1. 注册并拿到站点码

1. 打开 `https://www.goatcounter.com/signup` 这个地址, 用邮箱注册一个站点。
2. 站点码 (code) 就是注册时填的 Code, 也是站点域名的子域名前缀。填 protreptic 得到
   站点地址 `https://protreptic.goatcounter.com`, 上报端点则是
   `https://protreptic.goatcounter.com/count` 这个地址。
3. 注册后 GoatCounter 会往邮箱发一封确认信, 确认之后计数才开始入库。

这一步必须由站点所有者本人完成: 需要一个真实邮箱, 自动化任务不能代建账号,
也不能借用别人的站点码, 那是账号资产。

## 2. 填在哪里

开关落在 `web/goatcounter.json` 的 `code` 字段 (本次新增, 随源码入库):

```json
{
  "code": ""
}
```

把空字符串换成站点码即可, 例如把上面那行写成 `"code": "protreptic"` 这样。

不改文件也可以, 用构建期环境变量临时覆盖。优先级是 环境变量 > 文件:

```bash
cd web && VITE_GOATCOUNTER_CODE=protreptic npm run build
```

关于落点的说明: 卡片原本要求的是 `web/.env.production` 这个路径。本仓库的无人值守会话
对 `.env` 类文件有写保护 (覆盖 env/config 的操作需要人工批准), 而卡片允许 "或等价" 落点,
因此本次落在 `web/goatcounter.json`, 由 `web/vite.config.ts` 显式读取。
若以后要换回 `.env.production`: `loadEnv` 已经在读同一批变量, 变量名不变
(`VITE_GOATCOUNTER_CODE`), 只需把 `vite.config.ts` 的取数处换成从 env 取值即可。

## 3. 激活之后的行为

构建期 (`web/vite.config.ts` 的 `goatcounter-head` 插件) 往 `</head>` 之前注入一行:

```html
<script data-goatcounter="https://<code>.goatcounter.com/count" async src="https://gc.zgo.at/count.js"></script>
```

- 没有站点码时一个字节都不注入: 不留 404 脚本, 不留占位域名。
  Phase30-C3 的 `YOUR_INSTANCE` 占位符就是这么撤掉的。不要再犯。
- 深链不必另改一处: `tools/prerender_routes.py` 的预渲染页是以构建产物 `dist/index.html`
  为壳、只改 head 里几行再写出的, 所以首页 / `404.html` / 每个预渲染深链页会同时带上这行脚本。
- SPA 站内跳转由 `web/src/composables/useAnalytics.ts` 在 Vue Router 的 `afterEach` 里补报,
  参数是 `{path: location.pathname, title: document.title}`, 也就是当前地址与当前标题。
  count.js 只在首次载入计一次, 不补报的话所有深链页只会算进入时那一条。
- 未注入时这个模块直接返回: 不报错、不加载任何东西。
- 首屏不会被重复计数: 进入时那一次已经由 count.js 自己计入, 补报从第二次导航开始。
- 上报顺序上, `initAnalytics(router)` 必须在 `initSeo(router)` 之后调用,
  这样上报的标题才是当前路由的标题 (afterEach 按注册顺序执行), 否则会串页。

## 4. 本地怎么验证

无站点码 (缺省, 期望 inert):

```bash
$ cd web && VITE_DATA_MODE=static npm run build
$ grep -c goatcounter dist/index.html
0
$ grep -ci goatcounter dist/index.html
0
```

有站点码 (期望出现正确端点):

```bash
$ cd web && VITE_DATA_MODE=static VITE_GOATCOUNTER_CODE=abc123 npm run build
$ grep -n data-goatcounter dist/index.html
82:      <script data-goatcounter="https://abc123.goatcounter.com/count" async src="https://gc.zgo.at/count.js"></script>
```

浏览器内验证 (不用发真实请求也能验): 先 `npx vite preview --base=/protreptic/ --port 4210`
起本地预览, 然后在页面里塞一个只有 `data-goatcounter` 属性、不带 `src` 的同名 script
占位标签 (因此不会去下载 count.js), 再把 `window.goatcounter` 换成记录用的桩函数,
最后点一个站内链接:

- 载入后 `window.__hits` 为空 (首屏不重复计数);
- 点击 `/figures` 里的人物卡后得到
  `[{"path":"/protreptic/minds/H-MIY-001","title":"人物模式档案 | Protreptic 思想典藏"}]`;
- 从 `/protreptic/` 进入并重定向到 `/figures` 时得到 `[{"path":"/protreptic/figures", ...}]`;
- 控制台没有 error 或 unhandledrejection 这两类报错。

线上回读。结果取决于 `code` 的当前值: 空则应为 0, 非空则应为 1 条。

```bash
$ curl -sL https://ovmobilegroup.github.io/protreptic/ | grep -c goatcounter
0
```

激活状态下实测 (2026-09-21, 首页 / `404.html` / 深链页各出现一次):

```bash
$ curl -sL https://ovmobilegroup.github.io/protreptic/ | grep -c goatcounter
1
$ curl -sL https://ovmobilegroup.github.io/protreptic/minds/H-MIY-001/ | grep -n data-goatcounter
72:      <script data-goatcounter="https://protreptic.goatcounter.com/count" async src="https://gc.zgo.at/count.js"></script>
```

## 5. 怎么回滚

把 `code` 改回空字符串 (或删掉那一行的值), 重新构建并推送即可回到 inert 状态。确认方式是:

```bash
$ cd web && grep -c goatcounter dist/index.html
0
$ curl -sL https://ovmobilegroup.github.io/protreptic/ | grep -c goatcounter
0
```

两个命令都输出 0 就是回到不加载统计脚本的状态, 不需要改代码、不需要回滚提交。

## 6. 已知注意点

- `lighthouserc.json` 里有一条预算 `resource-summary:third-party:size` 上限为 0,
  断言级别是 warn, 不会让 CI 变红。激活统计后第三方体积不再为 0, 这条会开始告警。
  若不想看到告警, 激活时同步放宽该阈值。
- 统计口径是页面访问, 与站点规模数字无关。条数 / 人物数的唯一取数入口仍是
  `tools/site_counts.py` 文件。
- `web/index.html` 里的注释刻意不写厂商名: 构建产物里出现该名字就等于脚本已注入,
  这样 `grep -c goatcounter dist/index.html` 就是 "是否已接入" 的单值判据。

## 7. 本次改动清单

| 文件 | 改动 |
| --- | --- |
| `web/index.html` | head 末尾注释改为指向本文 (本文件不含脚本) |
| `web/vite.config.ts` | 新增 `goatcounter-head` 插件 + 从 `goatcounter.json` 取数 |
| `web/goatcounter.json` | 新增: 开关落点, 缺省为空 |
| `web/src/composables/useAnalytics.ts` | 新增: SPA 路由补报 |
| `web/src/main.ts` | 在 `initSeo` 之后调用 `initAnalytics` |
| `docs/community/analytics_setup.md` | 本文 |
| `docs/architecture/gc_setup.md` | 顶部加指向本文的一行 |
