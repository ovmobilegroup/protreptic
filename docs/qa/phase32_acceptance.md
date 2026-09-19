# Phase32 独立复验（QA2）· F1 / F2 逐项实测

- 卡片：`t_25e03e7c`（[Phase32-QA2] 独立复验 F1/F2）· 审查人：espinosa
- 日期：2026-09-19（CST）
- 被审对象：Phase32-F1（隔离名单补漏：modes 摘要索引 8 分片仍泄漏 H-SX-001）与
  Phase32-F2（首页计数口径收口 + 打印页脚改走 @page 边距盒）
- 发布仓 HEAD：`9496056`（`## main...origin/main`，无 `[ahead N]`）
- **取证方式：全部自建方法与自写工具，不照抄工人自述。**
  线上侧逐个 curl 产物 + 真实浏览器读 DOM；打印侧用 CDP `Page.printToPDF` 自己生成 7 份 PDF，
  再用自写的 pypdf 组合矩阵量测脚本逐页量坐标，并做了**负对照**（把旧 fixed 叠层页脚注入线上页面，
  验证量测方法本身能抓到"压在正文框内"的页脚）；数据侧在发布仓 HEAD 的干净克隆
  `/tmp/qa32/pub2` 上重跑整条数据链并与线上逐分片比 sha256。
- **终审结论：可发布（PASS）。** F1、F2-计数、F2-打印、全局 CI 四项全部 PASS，
  另有 3 条**非阻断遗留**如实记录在第 6 节。

## 0. 逐项结论

| 项 | 结论 | 一句话 |
| --- | --- | --- |
| F1 · 线上 8 个 modes/index-*.json | PASS | 逐个 curl，含 `H-SX-001` 的记录数全为 0（合计 2848 条） |
| F1 · by-figure / 概念图 / 统一名录 | PASS | 三者均无 H-SX-001（283 人物），线上 `/minds/H-SX-001/` 404 |
| F1 · meta.json 计数自洽 | PASS | 8 分片条数和 2848 == products.count == `mode_summaries_published`；线上条数/字节与 meta 逐片相符 |
| F1 · 预检断言未被改坏 | PASS | 自建合成产物三连测：净样本 exit 0；注入 1 条隔离记录 exit 1；篡改 published exit 1 |
| F1 · 扩展面（自加） | PASS | 检索倒排 16 片 / 图谱 3 件 / daily / sitemap / 分享图 alt 全扫，隔离串零命中 |
| F2-计数 | PASS | `grep -rn 2868 web/src web/index.html` 0 命中；线上首页 description / og:description = 2858 × 283，与 meta.json 一致 |
| F2-打印 | PASS | 自测 7 模板 76/76 页页脚 y=819.0pt（距纸底 22.9pt=8.1mm），全在下边距区，正文重叠 0 页 |
| 全局 · ahead / CI | PASS | 发布仓 ahead=0；HEAD 9496056 上 Pages / CI / CI-CD / Quality Gate 四个 run 全 success |

---

## 1. F1 · 线上逐个 curl 8 个 modes/index-*.json

```console
$ for i in 0 1 2 3 4 5 6 7; do curl -s -o "live_index-$i.json" \
    -w "index-$i http=%{http_code} bytes=%{size_download}\n" \
    "https://ovmobilegroup.github.io/protreptic/data/modes/index-$i.json"; done
index-0 http=200 bytes=99015
index-1 http=200 bytes=89733
index-2 http=200 bytes=89768
index-3 http=200 bytes=90870
index-4 http=200 bytes=91337
index-5 http=200 bytes=92723
index-6 http=200 bytes=93972
index-7 http=200 bytes=95241
```

自写统计脚本（直接 `json.loads` + 原始串计数，不用工人脚本）：

```console
$ python3 /tmp/qa32/f1_check.py
index-0: records=383 raw_H-SX-001=0 rec_H-SX-001=0 raw_苏咸=0 M393-M402=0
index-1: records=342 raw_H-SX-001=0 rec_H-SX-001=0 raw_苏咸=0 M393-M402=0
index-2: records=348 raw_H-SX-001=0 rec_H-SX-001=0 raw_苏咸=0 M393-M402=0
index-3: records=350 raw_H-SX-001=0 rec_H-SX-001=0 raw_苏咸=0 M393-M402=0
index-4: records=352 raw_H-SX-001=0 rec_H-SX-001=0 raw_苏咸=0 M393-M402=0
index-5: records=354 raw_H-SX-001=0 rec_H-SX-001=0 raw_苏咸=0 M393-M402=0
index-6: records=359 raw_H-SX-001=0 rec_H-SX-001=0 raw_苏咸=0 M393-M402=0
index-7: records=360 raw_H-SX-001=0 rec_H-SX-001=0 raw_苏咸=0 M393-M402=0
TOTAL records containing H-SX-001 = 0
```

8 片合计 2848 条，与 Phase31 记录的"修前 6 片 10 条"对比：泄漏归零。

## 2. F1 · by-figure / 概念图 / 统一名录 / 深链

```console
$ curl -s -o /dev/null -w "%{http_code}\n" \
    https://ovmobilegroup.github.io/protreptic/data/modes/by-figure/H-SX-001.json
404                     # 落到 404.html（SPA 壳），不是数据
$ curl -s -o /dev/null -w "%{http_code}\n" https://ovmobilegroup.github.io/protreptic/minds/H-SX-001/
404
$ curl -s -o /dev/null -w "%{http_code}\n" https://ovmobilegroup.github.io/protreptic/minds/H-EUC-001/
200                     # 对照：正常人物页仍是 200

$ python3 /tmp/qa32/f1_check.py      # 摘录
by-figure/H-SX-001.json is SPA fallback HTML: True
concept_graph figure_nodes = 283
concept_graph contains H-SX-001: False | contains 苏咸: False
unified counts: {'total': 1338, 'figures': 283, 'scenarios': 1055, 'with_modes': 1302}
unified items: 1338 | H-SX-001 present: False | H-EUC-001 present: True
unified 苏咸 present: False
```

浏览器层端到端（真实 DOM，非 JSON）：

```console
$ # browser_exec: goto /protreptic/modes -> document.body.innerText
{"len": 6571, "hasSX": false, "hasSuxian": false, "hasShen": false, "cards": 120,
 "sample": "… 思维模式库 |  | 2848 条思维模式实例，源自 283 位历史人物——每条都出自具体人物与具体文本 …"}
```

即 `/modes` 页面口径已是 **2848 条 / 283 位**，且页面上既无 `H-SX-001`、也无 `苏咸`、无 `审时度势法`。

## 3. F1 · meta.json 计数自洽 + 预检断言未被改坏

### 3.1 线上 meta.json 自洽性（我自己的等式，不看工人脚本）

```console
$ python3 /tmp/qa32/f1_meta_consistency.py
counts: {"figures": 1057, "figure_shards": 1057, "mode_summaries": 2858,
         "mode_summaries_published": 2848, "modes_quarantined": 10, "mode_index_shards": 8,
         "mode_by_figure_shards": 283, "modes_raw": 2868, "modes_deduped": 2858,
         "modes_duplicates_dropped": 0, "modes_empty_mode_code_dropped": 10,
         "modes_without_figure_code": 0}
per-shard counts: [383, 342, 348, 350, 352, 354, 359, 360] sum = 2848
sum == count: True
  live index-0: records=383 meta=383 match=True bytes_live=99015 bytes_meta=99015 match=True
  … （8 片全部 match=True，字节数也逐片相符）
live shard record total = 2848
mode_summaries(2858) == modes_deduped(2858): True
published = summaries - quarantined: True
index total == published: True
```

外加两条独立交叉校验：
- 线上 `meta.json` 记的源 `data/modes_data.json` sha256 = `cc43a609011a…`，与工作区/发布仓
  `data/modes_data.json` 实际 sha256 `cc43a609011a…` **一致** —— 线上数据确实由当前源导出。
- 线上 `data/search/meta.json` 记的 16 个 `.bin` sha256，与我下载到的文件**逐片一致**（无输出=全一致），
  且其 `doc_count=2848`、`sources.modes_data_sha256` 同一条。

### 3.2 预检断言可执行性（负测试，证"门没被改坏"）

不能只读脚本断言"它应该会拦"。我自建了一个最小合成产物目录
（`/tmp/qa32/negtest/tools/pages_preflight.py` + `_quarantine.py` 从发布仓 HEAD 拷来，
`web/public/data` 按 1057 figures / 8 modes 分片 2848 条 / 283 by-figure 分片 / daily 2848 条合成），
三种样本三连测：

```console
$ cd /tmp/qa32/negtest && python3 gen.py clean && python3 tools/pages_preflight.py --stage data
      figures=1057 modes=2858 published=2848 隔离命中=0 figure shards=1057 by-figure shards=283
      daily: 2848 条（by-figure 分片 2848 条）names=2848 tz=Asia/Shanghai
[OK] stage=data：全部断言通过
EXIT_A=0

$ python3 gen.py leak && python3 tools/pages_preflight.py --stage data      # 注入 1 条 H-SX-001 摘要
::error::隔离人物出现在公开摘要索引 1 条: index-0.json:M393
::error::meta.json counts.mode_summaries_published 与 modes/index-*.json 实际条数 = 2848，期望 2849
[FAIL] stage=data：2 条断言未通过
EXIT_B=1

$ python3 gen.py badpub && python3 tools/pages_preflight.py --stage data    # published 2848 -> 2850
::error::meta.json counts.mode_summaries_published 与 modes/index-*.json 实际条数 = 2850，期望 2848
[FAIL] stage=data：1 条断言未通过
EXIT_C=1
```

净样本绿、注入隔离记录红、篡改计数红 —— 预检门是活的，不是装饰。

### 3.3 发布仓 HEAD 重跑整条数据链（证"是工具修好了，不是制品被手改"）

```console
$ git clone -q /opt/data/release/Protreptic-publish /tmp/qa32/pub2 && cd /tmp/qa32/pub2
$ git log --oneline -1
9496056 ci(pages): paths 过滤补上 tools/apply_site_counts.py
$ python3 tools/build_figures_db.py && python3 tools/export_static_site.py
✅ figures 表重建完成: 1057 行
  modes/index-0.json  383 条 …  modes/index-7.json  360 条
  modes/ 合计         2848 条  raw 725.3 KB / gzip 181.9 KB
  modes/by-figure/    283 片
  meta.json counts={"figures": 1057, …, "mode_summaries": 2858, "mode_summaries_published": 2848,
                    "modes_quarantined": 10, "mode_by_figure_shards": 283, "modes_raw": 2868, …}
  [OK] 隔离名单零泄漏 (名单 H-SX-001; 被剔模式 10 条)
  [OK] figures=1057 modes(源)=2858 modes(发布)=2848 隔离剔除=10 by-figure=283
完成 OK
$ python3 tools/build_daily_index.py && python3 tools/pages_preflight.py --stage data
      figures=1057 modes=2858 published=2848 隔离命中=0 figure shards=1057 by-figure shards=283
      daily: 2848 条（by-figure 分片 2848 条）names=2848 tz=Asia/Shanghai
[OK] stage=data：全部断言通过
PREFLIGHT_EXIT=0
```

**本地新构建 vs 线上逐分片 sha256（最强证据：线上跑的就是这版工具产出的字节）**：

```console
$ python3 /tmp/qa32/local_vs_live.py
=== 本地新构建产物独立扫描（不用工人的自检脚本）===
  index-0: rows=383 H-SX-001=0 苏咸=0 M393-M402=0
  … （8 片同样全 0，合计 rows = 2848）
  modes/by-figure/H-SX-001.json: 不存在（隔离人物分片未生成 = 期望）
  daily/index.json: H-SX-001=0 苏咸=0
=== 本地新构建 vs 线上（逐分片 sha256）===
  index-0: local=1b9cdf98081eb8c1 live=1b9cdf98081eb8c1 IDENTICAL
  index-1: local=0992fe9cffe75aff live=0992fe9cffe75aff IDENTICAL
  index-2: local=5017bc5a50fe021c live=5017bc5a50fe021c IDENTICAL
  index-3: local=56bf826f354a62bb live=56bf826f354a62bb IDENTICAL
  index-4: local=115313ef79617f81 live=115313ef79617f81 IDENTICAL
  index-5: local=342b3648ad7dc25c live=342b3648ad7dc25c IDENTICAL
  index-6: local=acfb6cff27e5a732 live=acfb6cff27e5a732 IDENTICAL
  index-7: local=e476229add693565 live=e476229add693565 IDENTICAL
  本地 counts == 线上 counts : True（差异: 无）
```

### 3.4 扩展扫面（F1 只点名了 3 个产物，我把所有公开产物层扫了一遍）

```console
$ python3 /tmp/qa32/sweep2.py
=== 线上 search 倒排分片（16 片, raw 格式, doc_count=2848）===
  index-0.bin … index-15.bin : 隔离人物串命中=无 mode_code 命中=无
=== 其它线上产物 ===
  search/meta.json / graph/mode_edges.json / graph/similar_modes.json / graph/meta.json /
  sitemap.xml / index.unified.json / graph/concept_graph.json / meta.json /
  by-figure/H-EUC-001.json / daily/index.json / daily/names.json / index.html :
  隔离人物串命中=无 mode_code 命中=无
>>> 汇总: 任何线上产物含隔离人物串 = False
```

即泄漏面不止已修的三层：检索倒排、图谱三件、每日一模式、sitemap、线上首页 HTML 全部干净。

## 4. F2-计数

```console
$ cd /opt/data/workspace/Protreptic && grep -rn "2868" web/src web/index.html
grep_exit=1                      # 0 命中（覆盖 src 与 index.html 两者，上一轮 QA 只扫了 src）
$ grep -rn "2868" web --include=*.html --include=*.ts --include=*.vue --include=*.js --include=*.json \
      --exclude-dir=node_modules --exclude-dir=dist
web/public/data/meta.json:1:{…"modes_raw":2868…}      # 仅此一处，是"源原始条数"字段，正确
$ grep -rn "1058" web/src web/index.html             # 0 命中
$ grep -rn "284\b" web/src web/index.html            # 0 命中
```

线上首页 HTML（真实 HTTP）：

```console
$ curl -s -o live_index.html -w "home http=%{http_code} bytes=%{size_download}\n" \
    https://ovmobilegroup.github.io/protreptic/
home http=200 bytes=4187
$ grep -oE '<meta (name|property)="[^"]*(description|og:[a-z:]*|twitter:[a-z:]*)"[^>]*>' live_index.html
<meta name="description" content="2858 条思维模式 × 283 位历史人物：每条都有出处、操作步骤与现代应用。以人为鉴，明得失。" />
<meta property="og:description" content="2858 条思维模式 × 283 位历史人物 · 中英双语" />
<meta property="og:image:alt" content="Protreptic 思想典藏 — 2868 条思维模式 × 283 位历史人物" />
<meta name="twitter:image:alt" content="Protreptic 思想典藏 — 2868 条思维模式 × 283 位历史人物" />
```

对照 `data/meta.json`：`counts.mode_summaries=2858`、`counts.mode_by_figure_shards=283`
→ **description / og:description 两条 = 2858 × 283，与 meta.json 完全一致（本项 PASS）**。
（`og:image:alt` / `twitter:image:alt` 仍是 2868，见第 6 节遗留 L1 —— 不属本项验收线。）

SPA 运行时同一句话的交叉校验（静态 head 与运行时文案不许分叉）：

```console
$ curl -s https://ovmobilegroup.github.io/protreptic/assets/index-Jw_xJA4V.js  # 348524 bytes
   2858 条思维模式 出现 2 次
   2868 出现 0 次
   284 位历史人物 出现 0 次
   283 位历史人物 出现 3 次
```

## 5. F2-打印（自测 PDF + 自写量测 + 负对照）

**方法**：`browser_exec` 真实浏览器逐个打开线上 7 个模板页 →
CDP `Page.printToPDF(preferCSSPageSize=True, printBackground=False)` →
自写 `pypdf` 量测（组合矩阵 `y_pdf = cm[1]*tm[4] + cm[3]*tm[5] + cm[5]`，`y_from_top = 841.92 - y_pdf`，
比只取 `tm[5]` 正确；页脚判据 = 文本含线上原文 URL 或 `第 N / M 页`，且 y > 纸高-120pt）。

**坐标数字（A4 594.96 × 841.92pt；@page 下边距 18mm = 51.0pt → 正文框底 790.92pt）**：

```console
$ /tmp/qa32/venv/bin/python measure.py pdf/live_*.pdf
--- pdf/live_baidi.pdf      pages=8
    footer 覆盖页数 = 8/8    footer y_from_top: min=819.0 max=819.0
    页脚距纸底 = 22.9pt = 8.1mm      落在纸张下边距区 [790.92,841.92] : True
    最深正文行 y=771.7pt             页脚与正文最小间距 = 47.3pt      重叠页 = 无
    页码序列 = ['第1/8页', '第2/8页', '第3/8页'] … 第8/8页
--- pdf/live_beifa.pdf      pages=12   footer 12/12  y=819.0  距纸底 8.1mm  最深正文 724.5  间距 94.5  重叠 无
--- pdf/live_changban.pdf   pages=12   footer 12/12  y=819.0  距纸底 8.1mm  最深正文 766.5  间距 52.5  重叠 无
--- pdf/live_chibi.pdf      pages=10   footer 10/10  y=819.0  距纸底 8.1mm  最深正文 778.5  间距 40.5  重叠 无
--- pdf/live_jieting.pdf    pages=11   footer 11/11  y=819.0  距纸底 8.1mm  最深正文 781.5  间距 37.5  重叠 无
--- pdf/live_longzhong.pdf  pages=10   footer 10/10  y=819.0  距纸底 8.1mm  最深正文 777.0  间距 42.0  重叠 无
--- pdf/live_yiling.pdf     pages=13   footer 13/13  y=819.0  距纸底 8.1mm  最深正文 762.0  间距 57.0  重叠 无
```

汇总：**7 模板 76/76 页**（8+12+12+10+11+10+13），页脚 y 恒为 **819.0pt**，
距纸底 **22.9pt = 8.1mm**；`819.0 ≥ 790.92` → **全部落在纸张下边距区**；
最深正文行最高 781.5pt（仍在正文框底 790.9pt 之内），**页脚与正文最小间距 37.5pt，重叠页 0**。
页码由 `counter(page)/counter(pages)` 生成，逐页 `第1/8页…第8/8页` 连续。

**负对照（证明量测方法不是"永远说好"）**：向线上同一页面注入旧实现
（`.pt-print-only { position: fixed; bottom: 18mm }` + 清空 @page 边距盒 content），重新生成 PDF：

```console
$ /tmp/qa32/venv/bin/python measure.py pdf/neg_control_oldfixed_baidi.pdf
    footer 覆盖页数 = 8/8    footer y_from_top: min=735.7 max=735.7
    页脚距纸底 = 106.2pt = 37.5mm    落在纸张下边距区 [790.92,841.92] : False
    页脚与正文最小间距 = -36.0pt     正文与页脚重叠页 = [(2, 737.2, 735.7), (4, 743.2, 735.7), (5, 771.7, 735.7)]
```

同一把尺子：旧实现量出 735.7pt / 距纸底 37.5mm / 3 页压在正文上（与 F2 自述的"修前 735.7pt、
正文框内、有重叠"完全吻合），新实现量出 819.0pt / 8.1mm / 0 重叠。**结论：修的是真问题，且已上线。**

**已知限制（F2 自述，我复核 CSS 确认属实，非缺陷）**：@page 边距盒要求纸面有下边距
（打印对话框边距选"无"时页脚整块消失）；Firefox/Safari 不支持 @page 边距盒，这两种浏览器打印件上没有该行。

## 6. 全局状态与遗留

### 6.1 发布仓 / CI

```console
$ git -C /opt/data/release/Protreptic-publish status -sb
## main...origin/main                     # 无 [ahead N] → ahead=0

$ gh run list --repo ovmobilegroup/protreptic --limit 12   # HEAD 9496056 上的四个 run
Quality Gate            35410216028  workflow_run  success  2026-09-19T00:41:35Z
Protreptic CI/CD        35409917635  push          success  2026-09-19T00:36:14Z
Deploy to GitHub Pages  35409917613  push          success  2026-09-19T00:36:14Z
CI                      35409917609  push          success  2026-09-19T00:36:14Z

$ gh api …/runs/35409917613/jobs --jq '.total_count, (.jobs[]|{name,conclusion})'
2  构建 SPA + 文档站 success / 部署 success
$ gh api …/runs/35409917609/jobs --jq '.total_count, (.jobs[]|{name,conclusion})'
1  markdown-lint success
$ gh api …/runs/35410216028/jobs --jq '.total_count, (.jobs[]|{name,conclusion})'
3  数据校验 success / 线上死链检测 success / Lighthouse 预算门 success
```

无 phantom `0s` workflow（`name == path`）失败项；Quality Gate 是**真跑了 3 个 job** 的 success，
不是"无效 workflow 静默失败"。上一轮 Phase31 记的两条长期红（markdown-lint、ci-cd 的 pytest）本轮**均已转绿**。

### 6.2 双仓一致性

关键源文件逐个 sha256 对比（工作区 vs 发布仓）：`web/index.html`、`web/src/style.css`、
`web/src/views/TemplateDetailView.vue`、`tools/apply_site_counts.py`、`tools/export_static_site.py`、
`tools/pages_preflight.py`、`tools/_quarantine.py`、`.github/workflows/{pages,quality-gate}.yml`、
`tools/{build_graph_data,build_unified_index,ci_data_check,prerender_routes,thinking_mode_selector,figure_library}.py`、
`data/figure_names.json`、`data/modes_data.json` —— **全部 SAME**。

### 6.3 遗留（非阻断，不改变"可发布"结论；如实记录）

- **L1 · 分享图 alt 与图内文案仍是 2868**：线上首页 `og:image:alt` / `twitter:image:alt` =
  "…2868 条思维模式 × 283 位历史人物"，且我用 vision 读 `og/site.png` 实测图上标签为
  **「2868 条思维模式」「283 位历史人物」「1055 个现代场景」**。根因：文案由
  `tools/og_image.py::unified_counts()` 取 `counts.modes_raw`（源原始条数 2868）优先，
  与站点文案口径 `mode_summaries`（2858）不同源。属"同一份数据两个口径"，不属本卡验收线
  （验收线只点名 description / og:description），但与站内 2858 不一致，建议单独开卡统一口径
  （要么 `unified_counts` 优先取 `mode_summaries`，要么站内文案改用 `modes_raw`）。
- **L2 · `docs/architecture/web_p0_routes.json` 双仓不一致**：工作区副本 sha256 `915d3378…`、
  发布仓副本 `803eb6ae…`（工作区该文件有未提交改动）。它是预渲染步骤的**登记产物**，
  不参与线上页面数据（线上 sitemap / 路由均已实测正确），不阻断发布；但应在下一次触碰
  `tools/prerender_routes.py` 时一并同步，避免审计口径分叉。
- **L3 · 工作区仓库存在未提交改动**（`api/protreptic.db`、`data/modes_data.json`、`data/figure_names.json`、
  `data/figures/H-HuoQuBing-001.json`、`docs/architecture/web_p0_routes.json`、6 个 `tools/*.py`、1 个未跟踪脚本）。
  经 sha256 比对，其中**所有影响线上的文件与发布仓已完全一致**（见 6.2），故不影响本次发布；
  但这些改动长期悬在工作区，属卫生问题，建议在后续卡里提交或回退。

## 7. 结论

**可发布（PASS）。** F1 的四条要求（线上 8 分片零泄漏、by-figure/概念图/统一名录无它、
meta 计数自洽、预检断言未被改坏）逐条实测通过，并附扩展扫面与"本地重跑 == 线上字节"的证据；
F2 两条（计数口径收口、打印页脚落点）逐条实测通过，打印侧附带负对照证明量测有效；
发布仓 ahead=0，HEAD 上四个 CI run 全 success 且 Quality Gate 三个 job 真跑。
不达标项：无。非阻断遗留 3 条（L1 分享图口径、L2 路由登记产物、L3 工作区未提交改动），已在 6.3 写明。

### 复现命令清单

```console
# F1 线上产物
for i in 0 1 2 3 4 5 6 7; do curl -s -o live_index-$i.json -w "index-$i %{http_code} %{size_download}\n" \
  https://ovmobilegroup.github.io/protreptic/data/modes/index-$i.json; done
python3 /tmp/qa32/f1_check.py && python3 /tmp/qa32/f1_meta_consistency.py
# F1 预检负测试（自建合成产物）
cd /tmp/qa32/negtest && python3 gen.py clean|leak|badpub && python3 tools/pages_preflight.py --stage data
# F1 本地重跑 + 与线上比字节
git clone /opt/data/release/Protreptic-publish /tmp/qa32/pub2 && cd /tmp/qa32/pub2 \
 && python3 tools/build_figures_db.py && python3 tools/export_static_site.py \
 && python3 tools/build_daily_index.py && python3 tools/pages_preflight.py --stage data
python3 /tmp/qa32/local_vs_live.py
# F2 计数
grep -rn "2868" web/src web/index.html ; curl -s https://ovmobilegroup.github.io/protreptic/ | grep -oE '<meta [^>]*description[^>]*>'
# F2 打印（CDP Page.printToPDF + pypdf 逐页量坐标；负对照注入旧 fixed 页脚）
/tmp/qa32/venv/bin/python /tmp/qa32/measure.py /tmp/qa32/pdf/live_*.pdf /tmp/qa32/pdf/neg_control_oldfixed_baidi.pdf
# 全局
git -C /opt/data/release/Protreptic-publish status -sb
HOME=/opt/data/home /opt/data/home/.local/bin/gh run list --repo ovmobilegroup/protreptic --limit 12
```

证据文件（临时，随会话清理）：`/tmp/qa32/`（live_index-*.json、live_search/、pdf/、print_measure_all.txt、
neg_control_measure.txt、f1_check.py、f1_meta_consistency.py、measure.py、sweep2.py、local_vs_live.py）。
