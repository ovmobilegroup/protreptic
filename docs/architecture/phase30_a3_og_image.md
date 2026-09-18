# Phase30-A3: og:image 动态生成 (社交分享图)

目标: 线上 https://ovmobilegroup.github.io/protreptic 的每一类页面在分享到社交平台时
都有自己的一张 1200x630 分享图. Pages 上没有服务端, 所以图必须在构建期画出来.

## 1. 分工 (四个文件, 一个契约)

| 文件 | 角色 |
| --- | --- |
| tools/og_image.py | 契约: 路由到图片路径/URL 的规则 + 每张图的文案规格 (标题/副题/摘要/标签/印章字), 文案全部取自真实数据 |
| tools/build_og_images.py | 构建期用 Pillow 把规格画成 PNG, 写进 web/dist/og/**, 并写 dist/og/manifest.json |
| tools/apply_og_meta.py | 按 manifest 把 og:image / twitter:image 等标签写进每个预渲染页面的 head |
| web/src/composables/useSeo.ts | 前端镜像: SPA 站内跳转时用同一套规则更新 head |

tools/check_og_mirror.py 用 esbuild 打包真实的 useSeo.ts 在 node 里跑, 与 og_image.py
的输出逐条比对, 防止两份规则漂移 (当前 12 条用例 0 不一致).

## 2. 路径契约

```
''             -> og/site.png              站点首页
figures        -> og/pages/figures.png     /figures (modes / templates / api 同理)
minds/<code>   -> og/minds/<code>.png      人物: 姓名 + 模式数 + 时代
figures/<code> -> og/figures/<code>.png    场景: 名称 + 领域 + 关联模式数
templates/<id> -> og/templates/<id>.png    模板: 标题
其他/未知       -> og/site.png
```

文件名用 code 原值 (只允许 [A-Za-z0-9._-] 与空格, 含目录分隔符直接报错), URL 用
urllib.parse.quote, 前端用 encodeURIComponent; 实测 figures/Sun Quan 两边都给
.../og/figures/Sun%20Quan.png.

## 3. 画的内容

- 人物页: 主名 (龚自珍 这种带副题的名字按冒号拆成主名 + 副题), 时代 (最长的一条原始数据
  468 字, 先砍括号/破折号注解再截断), N 条思维模式, 领域; 没有时代数据的显示「时代待核」.
- 场景页: 名称 + 领域标签 + N 条关联模式 + 一句真实描述.
- 模板页 / 列表页 / 首页: 标题 + 规模数字 (条数取自 index.unified.json 与 meta.json).
- 版式: 深墨底 + 金 (鎏金) 与玉 (青玉) 双色 + 衬线标题 + 右侧印章方框, 与站内「思想典藏」一致.
- 体积: 真彩 PNG 单张 50-90 KB, 796 张不可接受, 所以统一 96 色中位切分 + Floyd-Steinberg 抖动,
  单张降到 17-37 KB (--colors 0 可关掉).

## 4. 字体 (不可回避的一步)

分享图要画中文, 必须把 CJK 字形打包进仓库; 完整 Noto Serif SC 单字重 11-12 MB.
tools/subset_og_font.py 用 fontTools 按「排版真正用到的字 + 常用标点 + 可打印 ASCII +
data/modes_data.json 高频字 2500 个」子集化, 产出:

- tools/assets/fonts/ProtrepticOgSerif-Regular.otf 与 -Bold.otf (各约 800 KB, 合计 1.6 MB)
- tools/assets/fonts/coverage.json (子集覆盖的字符表, 构建期用来自检)
- tools/assets/fonts/OFL-NotoSerifSC.txt (SIL OFL 1.1, 该字体无 Reserved Font Name, 允许子集化与再分发)

源字体只在重新子集化时下载, 缓存在 tools/assets/fonts/.cache/ (已 gitignore).
构建期发现新数据带来没见过的字时, build_og_images.py 会自动重跑子集化
(subset_og_font.main(chars=...), 需要 fonttools; 源字体不在缓存就联网取);
自愈失败则直接非 0 退出: 宁可不发图, 也不发带豆腐块的分享图.
实测: 场景从 501 涨到 1055 时冒出 4 个生僻字 (乍 狮 祉 蓬), 正是这条自愈路径兜住的.

## 5. CI 顺序 (.github/workflows/pages.yml)

```
build_figures_db -> export_static_site -> build_search_index -> build_graph_data
-> build_unified_index -> npm run build -> build_og_images -> prerender_routes
-> apply_og_meta -> build_sitemap -> mkdocs -> 合并 _site -> preflight merged
```

- build_og_images 必须在 npm run build 之后 (读 dist/data/index.unified.json 与 dist/templates/*.md).
- apply_og_meta 必须在 prerender_routes 之后 (预渲染会重写路由页自己的 index.html).
- 分享图那一步先 pip install "pillow==11.*"; 自动重建子集时还需要 fonttools, 同一行一起装.

## 6. 自检 (任一不过即非 0 退出, 不是静默降级)

1. build_og_images: 字形覆盖, 逐张 PNG 魔数/尺寸 1200x630/体积下限, 图片数量与名录条数对齐.
2. apply_og_meta: manifest 每条路由都要有对应 HTML; 图片必须是 dist 里 1200x630 的真 PNG;
   写完回读, 每页 og:image 必须恰好一份且取值等于 manifest 里的 URL.
3. check_og_mirror: TS 镜像与 Python 实现逐条一致.

## 7. 本地实测证据 (2026-09-18, 私有产物目录 /tmp/ptv_a3)

```
$ python3 tools/build_og_images.py --dist /tmp/ptv_a3
[og] 路由 1350 条, 文案来自 dist/data/index.unified.json + dist/templates/*.md
[og] 已生成 1350 张 (page 4, person 283, scenario 1055, site 1, template 7), 共 32.9 MB, 单张 17-37 KB
[og] manifest -> /tmp/ptv_a3/og/manifest.json            # 3m34s

$ python3 tools/prerender_routes.py --dist /tmp/ptv_a3
[prerender] wrote 1349 index.html, total 6926 KB

$ python3 tools/apply_og_meta.py --dist /tmp/ptv_a3
[ogmeta] 已写入 1350 页 og:image/twitter:image (base=/protreptic/, 尺寸 1200x630)

$ python3 tools/check_og_mirror.py
[mirror] 校验 12 条路由规则, 0 条不一致

$ curl -s -o /dev/null -w "%{http_code} %{content_type}\n" <本地静态服务>/protreptic/og/minds/H-WYM-001.png
200 image/png

$ grep -o '<meta property="og:image[^>]*>' /tmp/ptv_a3/minds/H-WYM-001/index.html
<meta property="og:image" content="https://ovmobilegroup.github.io/protreptic/og/minds/H-WYM-001.png" />
<meta property="og:image:width" content="1200" />
<meta property="og:image:height" content="630" />
<meta property="og:image:alt" content="王阳明的思维模式档案 (10 条) — Protreptic 思想典藏" />

$ grep -o '<meta name="twitter:card[^>]*>' /tmp/ptv_a3/minds/H-WYM-001/index.html
<meta name="twitter:card" content="summary_large_image" />
```

抽样对照 (页面 head 里的 URL 对磁盘文件):

| 页面 | og:image | 文件字节 |
| --- | --- | --- |
| minds/H-WYM-001 | og/minds/H-WYM-001.png | 28568 |
| figures/A-1-X-P | og/figures/A-1-X-P.png | 26053 |
| templates/chibi | og/templates/chibi.png | 26374 |
| figures | og/pages/figures.png | 29897 |
| minds/H-ZY-001 | og/minds/H-ZY-001.png | 28341 |

## 8. 踩过的坑

- script 标签自闭合: web/index.html 里 GoatCounter 那段写成 <script ... />, 而 HTML 的
  script 是 raw text 元素, 自闭合被忽略, 于是后面真正的入口
  <script type="module" src="/src/main.ts"> 被吞进上一个标签的文本里, vite build 只输出
  index.html (113 modules 变成 2 modules, 没有 assets/). 本卡顺手改成 ...></script>;
  页面上任何 script 标签都不允许自闭合.
- manifest 是唯一真源: apply_og_meta 先删掉页面里所有 og:image*/ twitter:image* / og:type
  再按 manifest 写入, 避免静态壳与注入内容出现两份 og:image.
- og:type 也分级: 人物 profile, 模板 article, 其余 website.
- era 字段最长 468 字 (一位人物的整段生平), 必须截断; domains 对场景是英文 token
  (16 个主力值 + 21 个零散值), 画图前映射成中文标签, 未收录的原样显示.
- 不在实现里臆造数据: 姓名, 时代, 身份, 描述全部来自 index.unified.json / meta.json /
  模板 markdown; 缺失就显示「时代待核」, 不猜.

## 9. 版式样例

仓库里放了 4 张成品 (docs/architecture/og_samples/): site.png (首页), mind-H-WYM-001.png (人物),
scenario-A-1-X-P.png (场景), template-chibi.png (模板). 这些图由本卡流水线生成, 可直接打开核对版式.
