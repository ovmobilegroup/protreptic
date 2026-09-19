# Phase33-L1 验收报告 —— 统一「思维模式数」口径 + 重新生成分享图

任务卡：`[Phase33-L1] 统一「思维模式数」口径 + 重新生成分享图（图上文案仍是 2868）`
来源：`docs/qa/phase32_acceptance.md` 第 6.3 节 L1（QA2 用视觉模型读 `og/site.png`
实测图上写着「2868 条思维模式」，与站点文案的 2858 不同源）。

## 1. 口径决策：站点展示的数 = `mode_summaries_published`（2848）

`web/public/data/meta.json` 的 `counts` 里三档并存（原文）：

```console
$ python3 -m json.tool web/public/data/meta.json | sed -n '7,25p'
    "counts": {
        "figures": 1057,
        "figure_shards": 1057,
        "mode_summaries": 2858,
        "mode_summaries_published": 2848,
        "modes_quarantined": 10,
        "mode_index_shards": 8,
        "mode_by_figure_shards": 283,
        "modes_raw": 2868,
        "modes_deduped": 2858,
        "modes_duplicates_dropped": 0,
        "modes_empty_mode_code_dropped": 10,
        ...
```

- `modes_raw = 2868`：`data/modes_data.json` 的原始记录数（未去重）。
- `mode_summaries = modes_deduped = 2858`：按 `mode_code` 首现去重、去掉 10 条空编号后的条数。
- `mode_summaries_published = 2848`：再扣掉 `tools/_quarantine.py` 里已确证虚构的
  **H-SX-001「苏咸」的 10 条模式（M393–M402，全部引伪造典籍《苏咸子》）**。

**选择：2848（`mode_summaries_published`）**，理由有三条，都是实测不是推断：

1. **它就是站上真正能打开的条数。** `modes/index-{0..7}.json` 合计 2848，
   `search/meta.json` 的 `doc_count = 2848`、`doc_id_contract` 写着「共 2848 条」，
   `daily/index.json` 的 `total = 2848`。2858 里有 10 条站上既搜不到也打不开。
2. **口径与页面自身已经打架。** `/modes` 页面正文由加载到的索引长度渲染
   （`ModesView.vue`：`` `${modes.length} 条思维模式实例` ``），实测显示 2848；
   而同一页的 `<meta description>` 写着 2858 —— 访客在同一屏里能看到两个数字。
3. **公开产出层本来就以「隔离项不得出现」为准。** H-SX-001 不进名录 / 每日 / 图谱 /
   概念层（Phase31-R4R5）；门面数字却把它算进去，等于用伪造记录撑门面。

因此统一到 2848，而不是把站内文案改成 `modes_raw`（2868）—— 那会把未去重、
且含已确证虚构的原始记录当成产品规模来宣传。

## 2. 改前：同一份数据的三个门面数字（实测）

```console
$ grep -rn "2858\|2868" web/src web/index.html | grep -v node_modules
web/src/composables/useSeo.ts:21:  '2858 条思维模式 × 283 位历史人物：每条都有出处、操作步骤与现代应用。以人为鉴，明得失。'
web/index.html:12:          content="2858 条思维模式 × 283 位历史人物：…"
web/index.html:19:    <meta property="og:description" content="2858 条思维模式 × 283 位历史人物 · 中英双语" />
web/src/App.vue:126:            Protreptic · 2858 条思维模式 × 283 位历史人物 · 中英双语
web/src/views/DailyView.vue:110: One mode a day out of 2858 …
web/src/views/ApiDocsView.vue:12: …（8 分片，共 2858 条）
$ grep -n "modes_raw" tools/og_image.py   # 分享图取的是 2868
194:        for key in ("modes_raw", "mode_summaries", "modes_deduped"):
$ grep -n "2858\|501" tools/prerender_routes.py   # 预渲染静态页 head 也写死过
59:    ("modes", "思维模式库 - 2858 条可执行方法", "2858 条历史人物思维模式实例, …"),
58:    ("figures", "历史人物库 - 统一名录", "283 位历史人物 + 501 个现代场景, …"),   # 501 也是死数字，实际 1055
```

`og/site.png` 上的图内文字（QA2 用视觉模型读到的旧值）：`2868 条思维模式` /
`283 位历史人物` / `1055 个现代场景`。

## 3. 改后：一个来源、一个取值

单一来源 = `dist/data/meta.json` 的 `counts.mode_summaries_published`（模式数）+
`counts.mode_by_figure_shards`（人物数）+ `index.unified.json` 的 `counts.scenarios`（场景数）。

- `tools/og_image.py::unified_counts()`：取数顺序改为
  `mode_summaries_published → mode_summaries → modes_deduped → modes_raw`（逐级回落），
  分享图图内文案与 `og:image:alt` 都由它派生。
- `tools/prerender_routes.py`：`STATIC_ROUTES` 常量化死数字 → `static_routes(meta_counts, unified_counts)`，
  `/modes` 与 `/figures` 的 title/description 从产物派生（顺带把 501 修正为实测 1055）。
- `tools/apply_site_counts.py`：来源改为 `mode_summaries_published`；「页面上出现第二个
  『N 条思维模式』」从软提示改成**硬门**（非 0 退出）。
- 站点文案（description / og:description / 页脚 / hero / /daily / /api 文档 / 代码注释）
  与 `web/index.html` 里的静态 head 一并改成 2848。

> 注意区分两套常量：`tools/export_static_site.EXPECT_MODES` /
> `tools/pages_preflight.EXPECT_MODES` / `tools/ci_data_check.EXPECT_MODES = 2858` 是
> **数据完整性门**（校验 `meta.json` 与数据源是否同步），不是门面数字，保持 2858 不动；
> 三处注释已写明这一点，避免下一个人再把它们当站点口径。

## 4. 验收：逐表面核对（改后实测）

```console
$ cd web && VITE_DATA_MODE=static npm run build && cd .. && python3 tools/build_og_images.py \
  && python3 tools/prerender_routes.py --dist web/dist --routes-out /tmp/routes_l1.json --body-persons all \
  && python3 tools/apply_og_meta.py && python3 tools/apply_site_counts.py
[og] 已生成 1351 张 (page 5, person 283, scenario 1055, site 1, template 7), 共 32.9 MB, 单张 17-37 KB
[prerender] wrote 1353 index.html, total 19200 KB
[ogmeta] 已写入 1351 页 og:image/twitter:image (base=/protreptic/, 尺寸 1200x630)
[counts] 首页计数已收口: 2848 条模式 × 283 位人物 (来源 web/dist/data/meta.json)

$ grep -o '<meta[^>]*description[^>]*>' web/dist/index.html
<meta name="description" content="2848 条思维模式 × 283 位历史人物：每条都有出处、操作步骤与现代应用。以人为鉴，明得失。" />
<meta property="og:description" content="2848 条思维模式 × 283 位历史人物 · 中英双语" />
$ grep -o '<meta[^>]*image:alt[^>]*>' web/dist/index.html
<meta property="og:image:alt" content="Protreptic 思想典藏 — 2848 条思维模式 × 283 位历史人物" />
<meta name="twitter:image:alt" content="Protreptic 思想典藏 — 2848 条思维模式 × 283 位历史人物" />
$ grep -o '<title>[^<]*</title>' web/dist/modes/index.html web/dist/figures/index.html
web/dist/modes/index.html:<title>思维模式库 - 2848 条可执行方法 | Protreptic 思想典藏</title>
web/dist/figures/index.html:<title>历史人物库 - 统一名录 | Protreptic 思想典藏</title>
$ grep -o '<meta name="description" content="[^"]*"' web/dist/modes/index.html web/dist/figures/index.html
web/dist/modes/index.html:<meta name="description" content="2848 条历史人物思维模式实例, 含定义, 操作步骤, 出处与原话."
web/dist/figures/index.html:<meta name="description" content="283 位历史人物 + 1055 个现代场景, 统一检索入口."
$ grep -o "Protreptic · [0-9]* 条思维模式[^\"<]*" web/dist/assets/*.js   # 页脚
Protreptic · 2848 条思维模式 × 283 位历史人物 · 中英双语
$ grep -o "One mode a day out of [0-9]*" web/dist/assets/*.js            # /daily hero
One mode a day out of 2848
$ grep -o "查询全部 [0-9]* 条模式" web/dist/assets/*.js                  # /api 文档
查询全部 2848 条模式
$ grep -o "8 分片，共 [0-9]* 条" web/dist/assets/*.js
8 分片，共 2848 条
```

`apply_site_counts.py` 自检通过（首页里任何「N 条思维模式」都等于 2848，否则非 0 退出）。

| 表面 | 改前 | 改后 |
| --- | --- | --- |
| 首页 `<meta description>` | 2858 | 2848 |
| 首页 `og:description` | 2858 | 2848 |
| `og:image:alt` / `twitter:image:alt` | 2868 | 2848 |
| `og/site.png` 图内文字 | 2868 | 2848 |
| `/modes` 预渲染 title | 2858 | 2848 |
| `/modes` 预渲染 description | 2858 | 2848 |
| `/modes` 页面正文（`modes.length`） | 2848（本来就对） | 2848 |
| /daily hero / /api 文档 / 页脚 | 2858 | 2848 |
| SPA 默认 description（`useSeo.ts`） | 2858 | 2848 |
| `/figures` 预渲染 description（场景数） | 501 | 1055 |
| 历史人物数（全站） | 283 | 283（本来就一致） |

## 5. 重新生成的 PNG 是真读过的

对 `web/dist/og/site.png`（刚由 `tools/build_og_images.py` 重画）用视觉模型逐字转录，
图内标签为：

```text
PROTREPTIC · 思想典藏
思想典藏 · Archive of Minds
Protreptic 思想典藏
历史人物思维模式库 · 中英双语
2848 条思维模式   283 位历史人物   1055 个现代场景
每条都有出处、操作步骤与现代应用。以人为鉴，明得失。
ovmobilegroup.github.io/protreptic
```

即图内文字已是 **2848**（旧图是 2868）—— 证明改的是图片本身，不只是 HTML。
分享图清单 `web/dist/og/manifest.json` 的站点条目：

```json
{"": {"image": "og/site.png", "alt": "Protreptic 思想典藏 — 2848 条思维模式 × 283 位历史人物",
       "kind": "site", "bytes": 32676}}
```

## 6. 遗留（如实记录，不在本卡范围内）

- **历史文档不改写。** `docs/architecture/*.md`、`docs/phase2*_final_report.md`、
  `docs/qa/phase3*_acceptance.md` 里的 2858 / 2868 / 501 是当时实测的数字（迁移评估、
  P0 基线、历次验收的原始记录），本卡**故意不改**——改写历史测量值才是真的失真。
  需要对齐时，新文档以本报告的 2848 口径为准。
- **`docs/02-tools/figure_library.md`** 描述的是**源语料/本地工具**（`data/modes_data.json` 的
  2868 条、`thinking_modes` 表的 2858 行），不是站上门面数字，保留原样。
- **`figures.index.json`（1057 条）的命名**：该分片里 1055 条其实是场景 code，只有 2 条是
  人物 code，但 `ApiDocsView` 仍写着「全部人物轻量索引（1057 条）」、`data/figures/*.json`
  也仍叫 figures。属历史命名债，改它要动 `EXPECT_FIGURES` 等基线常量，另开卡处理。
- **`tools/figure_library.py` / `tools/thinking_mode_selector.py`** 注释里的 2858 指本地查询
  工具的源库规模，同样不是站点门面数字。

## 7. 复现命令清单

```console
cd /opt/data/workspace/Protreptic
python3 -m json.tool web/public/data/meta.json | sed -n '7,25p'      # 三档口径原文
cd web && VITE_DATA_MODE=static npm run build && cd ..
python3 tools/build_og_images.py
python3 tools/prerender_routes.py --dist web/dist --routes-out /tmp/routes_l1.json --body-persons all
python3 tools/apply_og_meta.py
python3 tools/apply_site_counts.py
python3 tools/pages_preflight.py --stage dist        # 注意: 该断言按 CI 顺序在 prerender 之前跑
grep -rn "2858\|2868" web/src web/index.html   # 站点文案应零命中（注释里的旧口径也已清）
python3 tools/build_og_images.py --only site         # 重画 og/site.png 后再用视觉模型读一遍
```

## 附录 A（部署后线上回读 · 2026-09-19）

### A.1 push 与部署

```console
$ cd /opt/data/release/Protreptic-publish && git -c credential.helper=/tmp/l1helper.sh push origin main
To https://github.com/ovmobilegroup/protreptic.git
   b40cbc3..f5a8a34  main -> main

$ git -C /opt/data/release/Protreptic-publish status -sb
## main...origin/main                      ← 无 [ahead N]

$ HOME=/opt/data/home /opt/data/home/.local/bin/gh run list --repo ovmobilegroup/protreptic --limit 4
completed  success  fix(counts): 统一「思维模式数」口径到发布条数 2848（Phase33-L1）  CI                       main  push  35412591398  12s
completed  success  fix(counts): 统一「思维模式数」口径到发布条数 2848（Phase33-L1）  Deploy to GitHub Pages   main  push  35412591233  3m55s
```

### A.2 线上 head 回读（curl 实际输出）

```console
$ curl -sL https://ovmobilegroup.github.io/protreptic/ | grep -o '<meta[^>]*description[^>]*>'
<meta name="description" content="2848 条思维模式 × 283 位历史人物：每条都有出处、操作步骤与现代应用。以人为鉴，明得失。" />
<meta property="og:description" content="2848 条思维模式 × 283 位历史人物 · 中英双语" />
$ curl -sL https://ovmobilegroup.github.io/protreptic/ | grep -o '<meta[^>]*image:alt[^>]*>'
<meta property="og:image:alt" content="Protreptic 思想典藏 — 2848 条思维模式 × 283 位历史人物" />
<meta name="twitter:image:alt" content="Protreptic 思想典藏 — 2848 条思维模式 × 283 位历史人物" />
$ curl -sL https://ovmobilegroup.github.io/protreptic/modes/ | grep -o '<title>[^<]*</title>'
<title>思维模式库 - 2848 条可执行方法 | Protreptic 思想典藏</title>
$ curl -sL https://ovmobilegroup.github.io/protreptic/modes/ | grep -o '<meta name="description" content="[^"]*"'
<meta name="description" content="2848 条历史人物思维模式实例, 含定义, 操作步骤, 出处与原话."
$ curl -sL https://ovmobilegroup.github.io/protreptic/figures/ | grep -o '<meta name="description" content="[^"]*"'
<meta name="description" content="283 位历史人物 + 1055 个现代场景, 统一检索入口."
$ curl -sL https://ovmobilegroup.github.io/protreptic/docs/ | grep -o '<meta name="description"[^>]*>'
<meta name="description" content="Protreptic · 思想典藏 —— 2848 条历史人物思维模式 × 283 位人物 · 中英双语">
$ JS=/protreptic/assets/index-zl7fpKWT.js
$ curl -sL https://ovmobilegroup.github.io$JS | grep -o "2848 条思维模式 × 283 位历史人物 · 中英双语"
2848 条思维模式 × 283 位历史人物 · 中英双语      # 页脚
$ curl -sL https://ovmobilegroup.github.io$JS | grep -o "One mode a day out of [0-9]*"
One mode a day out of 2848                        # /daily hero
```

### A.3 线上分享图（部署产物，不是本地文件）

```console
$ curl -sL https://ovmobilegroup.github.io/protreptic/og/site.png -o /tmp/live_site_og.png
$ ls -la /tmp/live_site_og.png
-rw-r--r-- 1 hermes hermes 32676 Sep 19 09:32 /tmp/live_site_og.png
$ sha256sum /tmp/live_site_og.png web/dist/og/site.png
96ede786505301369af208ec1a9c932118ca63ea6be5852b3e8a61a3af9b9fe0  /tmp/live_site_og.png
96ede786505301369af208ec1a9c932118ca63ea6be5852b3e8a61a3af9b9fe0  web/dist/og/site.png
# 线上文件与本地构建产物逐字节相同（32676 B）—— 线上分享图确实是重画后的那张
```

用视觉模型读**线上**这张图（`vision_analyze /tmp/live_site_og.png`），逐字转录：

```text
PROTREPTIC · 思想典藏 / 思想典藏 · Archive of Minds
Protreptic 思想典藏
历史人物思维模式库 · 中英双语
2848 条思维模式   283 位历史人物   1055 个现代场景
每条都有出处、操作步骤与现代应用。以人为鉴，明得失。
ovmobilegroup.github.io/protreptic
```

结论：门面数字在 首页 head / og:image:alt / twitter:image:alt / 分享图图内文字 /
/modes·/figures 预渲染 head / 页脚 / /daily hero / /api 文档 / docs 站 meta
九处全部是 **2848 条模式 × 283 位人物（+1055 个场景）**，只有一个口径。

### A.5 关于源码里残留的 2858 / 2868（不是口径，是「禁止说明」）

```console
$ curl -sL https://ovmobilegroup.github.io/protreptic/ | grep -o "2858\|2868" | wc -l
2
$ curl -sL https://ovmobilegroup.github.io/protreptic/ | grep -n -B1 "2868"
8-         counts.mode_summaries_published（真正发布出去、站上能打开的模式摘要条数；
9:         不是 modes_raw=2868 的源条数，也不是含 10 条隔离伪造模式的 mode_summaries=2858），

$ grep -rn "2858\|2868" web/src web/index.html
web/index.html:9:         不是 modes_raw=2868 的源条数，也不是含 10 条隔离伪造模式的 mode_summaries=2858），
```

线上首页里仅剩的两处命中都落在 `web/index.html` 的 HTML 注释中：它们在说明
`modes_raw` / `mode_summaries` **不是**站点口径 —— 页面上不显示任何数字。
`web/src/**` 的展示文案与注释里 2858/2868 **零命中**。

保留这段注释是有意的：下一个人若把 `unified_counts()` 改回 `modes_raw`，注释是唯一
写在「会被改动的那一行旁边」的警告。若不希望对外 HTML 里出现这两个数字，
删掉该注释即可（但会再次改变 `web/index.html` 外壳长度，需同步重生成
`docs/architecture/web_p0_routes.json`，见 Phase33-L23 的说明）。
