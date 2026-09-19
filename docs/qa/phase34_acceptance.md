# Phase34-QA4 定向复验报告（manifest ×2 + docs 站 + 全产物扫描）

卡：`t_0bb56841`（espinosa）。上游：`t_d67e0ba3`（Phase34-L1B）。
必读依据：`docs/qa/phase33_acceptance.md`（QA3 终审判 **L1 FAIL**：线上两份 manifest 仍写
「2858 条思维模式」、线上 docs 工具页仍写 284 位 / 2868 条）。

本卡**只复验 L1B 的收口面**，方法沿用 QA3：**扫部署产物、不回看源码枚举**。
判定口径：站点文案统一为 **2848 条思维模式 × 283 位历史人物**
（= `web/public/data/meta.json` 的 `counts.mode_summaries_published` / `counts.mode_by_figure_shards`）。

## 0. 终审结论：**可发布（PASS）**

| # | 复验项 | 判定 | 依据小节 |
| --- | --- | --- | --- |
| 1 | 线上 `manifest.webmanifest` / `manifest-light.webmanifest` 的 description | **PASS** | §1 |
| 2 | 线上 `/docs/02-tools/figure_library/` 计数文案 | **PASS** | §2 |
| 3 | 全产物 `web/dist/**` 扫描（2858 条思维模式 / 2868 / 284 位） | **PASS**（判定式归零，残留命中逐条判明为伪命中） | §3 |
| 4 | 反向核对：主口径覆盖 description / og:description / og:image:alt / twitter:image:alt / 页脚 / hero / manifest ×2 | **PASS**（页脚为客户端渲染，见 §4.6 观测项） | §4 |
| 5 | 发布仓 `ahead=0` + Pages / CI / CI-CD / Quality Gate 最新 run success（含 job 数） | **PASS** | §5 |

判定逻辑：QA3 判 FAIL 的两处（manifest ×2、docs 页）本次实测**已归零**，
且整份部署产物在判定式上无一处旧口径；因此 L1 FAIL **已闭合**。

## 1. 线上两份 PWA manifest（从线上直取）

```bash
curl -sS https://ovmobilegroup.github.io/protreptic/manifest.webmanifest
curl -sS https://ovmobilegroup.github.io/protreptic/manifest-light.webmanifest
```

原始输出（两份的 `description` 逐字相同，此处各贴关键字段，其余为 name/icons/shortcuts）：

```json
{
  "name": "Protreptic · 思想典藏 — 历史人物思维模式库",
  "short_name": "思想典藏",
  "description": "2848 条思维模式 × 283 位历史人物：每条都有出处、操作步骤与现代应用，中英双语，可离线查阅。",
  "lang": "zh-CN",
  "start_url": "./",
  "display": "standalone",
  "background_color": "#04060c",
  "theme_color": "#04060c"
}
```

```json
{
  "description": "2848 条思维模式 × 283 位历史人物：每条都有出处、操作步骤与现代应用，中英双语，可离线查阅。",
  "background_color": "#f8f5f0",
  "theme_color": "#f8f5f0"
}
```

判定：两份 description 均为 **2848 × 283**；QA3 实测的 `2858 条思维模式` 在线上两份 manifest 中
**0 命中**。**PASS**。

## 2. 线上 docs 工具页（从线上直取）

```bash
curl -sS -o /tmp/figlib.html -w 'http_code=%{http_code} size=%{size_download}\n' \
  https://ovmobilegroup.github.io/protreptic/docs/02-tools/figure_library/
# 去掉 script/style/标签后按行读文案，再正则统计
```

原始输出（HTTP 与命中统计）：

```text
http_code=200 size=158574

### 判定式 '2858 条思维模式': 0 命中
### '2868': 3 命中（全部标注「源库/原始记录」）
### '284 位': 3 命中（全部标注「源库」）
### '2848': 5 命中
### '283 位': 4 命中
```

逐条原文（行内包含口径标注，属允许的「已说明的历史归档」）：

```text
把 Protreptic 的核心资产—— 283 位历史人物 × 站上发布 2848 条思维模式 ——接入可查询的产品层。
（源库 data/modes_data.json 的原始记录口径是 284 位 / 2868 条，两者差别见文末「计数口径」。）
数据文件： data/modes_data.json （源库原始记录 2868 条，21MB；站上发布口径 2848 条）
✅ 数据已入 thinking_modes 表（2858 条 = 源库去重口径，含 10 条站上已隔离的伪造记录；站上发布口径 2848 条）
# 列出全部历史人物（源库 284 位；站上发布口径 283 位）
计数口径（唯一来源） ¶ 对外展示的产品规模只有一个口径： 2848 条思维模式 × 283 位历史人物 。
唯一来源： web/public/data/meta.json
```

判定：页面**判定式短语**已是站点口径；残留的 `2868` / `284 位` 三处全部落在
「源库 / 原始记录」行内（L1B 决定的豁免规则），`2858` 一处落在
「源库去重口径…；站上发布口径 2848 条」的括号说明里，不属于门面文案。**PASS**。

## 3. 全产物扫描 `web/dist/**`（独立重跑整条 Pages 流水线）

为避免「本地 dist 是旧的」这一质疑，QA4 在**发布仓 HEAD 4911a21e 的隔离副本**上重跑 CI 全流水线：

```bash
D=$(cat /tmp/qa4dir.txt)                     # /tmp/qa4_<ts>，cp -a 发布仓 + 软链 node_modules
cd $D
/tmp/qa4venv/bin/python tools/build_figures_db.py
/tmp/qa4venv/bin/python tools/export_static_site.py
/tmp/qa4venv/bin/python tools/build_daily_index.py
/tmp/qa4venv/bin/python tools/pages_preflight.py --stage data
/tmp/qa4venv/bin/python tools/build_search_index.py
/tmp/qa4venv/bin/python tools/build_graph_data.py
/tmp/qa4venv/bin/python tools/build_unified_index.py
cd web && VITE_DATA_MODE=static npm run build
/tmp/qa4venv/bin/python tools/pages_preflight.py --stage dist
/tmp/qa4venv/bin/python tools/build_og_images.py
/tmp/qa4venv/bin/python tools/prerender_routes.py --body-persons all
/tmp/qa4venv/bin/python tools/apply_og_meta.py
/tmp/qa4venv/bin/python tools/apply_site_counts.py
/tmp/qa4venv/bin/python tools/build_sw.py
/tmp/qa4venv/bin/python tools/build_sitemap.py
```

关键原始输出（每步 rc=0）：

```text
[OK] stage=data：全部断言通过        figures=1057 modes=2858 published=2848 隔离命中=0 by-figure shards=283
[OK] stage=dist：全部断言通过        dist: index.html + 404.html（逐字节相同）+ data/ + /protreptic/ 前缀
[og] 已生成 1351 张 (page 5, person 283, scenario 1055, site 1, template 7), 共 32.9 MB
[prerender] base=/protreptic/ routes=1353   wrote 1353 index.html, total 19191 KB
[ogmeta] 已写入 1351 页 og:image/twitter:image (base=/protreptic/, 尺寸 1200x630)
[counts] manifest 已一致: web/public/manifest.webmanifest -> 2848 条思维模式 × 283 位历史人物…
[counts] manifest 已一致: web/public/manifest-light.webmanifest -> 2848 条思维模式 × 283 位历史人物…
[counts] manifest 已一致: web/dist/manifest.webmanifest -> 2848 条思维模式 × 283 位历史人物…
[counts] manifest 已一致: web/dist/manifest-light.webmanifest -> 2848 条思维模式 × 283 位历史人物…
[counts] 收口完成: 2848 条模式 × 283 位人物 (来源 web/dist/data/meta.json)
[counts] dist 扫描 2729 个文件零违规；docs 产品门面页 6 个零违规
[sitemap] entries=1354 (root=1)   by kind: {"person":283,"root":1,"scenario":1055,"static":8,"template":7}
```

**QA4 自己的独立正则扫描**（不依赖 `apply_site_counts.py` 的自检；该步的 2729 是「文本类」
文件数，QA4 扫的是 dist 下 **全部 4106 个文件**、78.7 MB，含 PNG 等二进制亦按字节解码后过正则）：

```text
scanned files: 4106   bytes: 78733881

### '2858 条思维模式': 0 file(s), 0 occurrence(s)
### '284 位历史人物': 0 file(s), 0 occurrence(s)
### '284 位':        0 file(s), 0 occurrence(s)
### '2858':          2 file(s), 3 occurrence(s)
### '2868':          2 file(s), 3 occurrence(s)
### 任意 '28xx 条思维模式': 7 file(s), 12 occurrence(s)   → 唯一取值为 2848
### 任意 '28x 位历史人物':  7 file(s), 19 occurrence(s)   → 唯一取值为 283
```

残留 `2858` / `2868` 命中逐条判明（**全部为伪命中，非门面文案**）：

| 文件 | 次数 | 命中上下文 | 判定 |
| --- | --- | --- | --- |
| `data/meta.json` | 2858 ×2、2868 ×1 | 数据层原始计数器字段：`"mode_summaries":2858`、`"modes_deduped":2858`、`"modes_raw":2868` | 非门面文案（数据合同字段，与 `mode_summaries_published:2848` 并存） |
| `og/manifest.json` | 2858 ×1、2868 ×2 | 均为 PNG 体积字段：`"bytes": 22858` / `28681` / `28686` | 伪命中（字节数，不是计数文案） |

正控（证明判定式有效）：同一次扫描里 `2848 条思维模式` 命中 12 次（`index.html`、`404.html`
各 2 次，JS bundle 2 次，`modes/index.html`、`og/manifest.json`、两份 manifest 各 1 次），
说明正则确实能抓到该句式 —— 不是「没扫到」而是「确实没有旧值」。**PASS**。

## 4. 反向核对：主口径覆盖各门面

### 4.1 线上 `/` 的 head（curl 实测）

```text
<meta name="description" content="2848 条思维模式 × 283 位历史人物：每条都有出处、操作步骤与现代应用。以人为鉴，明得失。" />
<meta property="og:description" content="2848 条思维模式 × 283 位历史人物 · 中英双语" />
<meta property="og:image:alt" content="Protreptic 思想典藏 — 2848 条思维模式 × 283 位历史人物" />
<meta name="twitter:image:alt" content="Protreptic 思想典藏 — 2848 条思维模式 × 283 位历史人物" />
```

命中计数：`2848 条思维模式` 4 次、`283 位历史人物` 4 次、`2858` 0 次、`2868` 0 次、`284 位` 0 次。

### 4.2 hero（线上）

```text
/figures/ hero：283 位历史人物的思维方法，与 1055 个现代处境场景，汇成同一份可检索的名录——每条都有出处与操作步骤，中英双语。
/modes/   hero：共 2848 条思维模式，每条含定义、操作步骤、出处与原话，中英双语。
```

### 4.3 og:image 链接的 alt / 线上 og manifest

```text
og manifest count: 1351   site alt: Protreptic 思想典藏 — 2848 条思维模式 × 283 位历史人物
alt strings carrying counts: 2  （站点卡 2848 × 283；/modes 卡「2848 条可执行方法」）
alt differences(local vs live): 0   （1351 条 alt 逐条相同）
alt with stale numbers: []
```

### 4.4 分享图**图上文字**读图（QA3 方法：不只信 alt，读像素）

```text
vision(live /og/site.png)  → 2848 条思维模式 / 283 位历史人物 / 1055 个现代场景
vision(live /og/pages/modes.png) → 2848 条思维模式
```

取值来自 `tools/og_image.py::unified_counts()`，它优先读 `mode_summaries_published`，
缺失才逐级回落 `mode_summaries → modes_deduped → modes_raw` —— 与站点口径同源。

### 4.5 manifest ×2

见 §1（线上实测 2848 × 283）。

### 4.6 页脚（**观测项，不计 FAIL**）

页脚文案 `Protreptic · 2848 条思维模式 × 283 位历史人物 · 中英双语` 存在于 **SPA bundle**
（`web/dist/assets/index-*.js`），即浏览器渲染后可见，口径正确。但它在 `prerender_body`
的静态快照里不出现：实测线上 `/`、`/figures/`、`/modes/`、`/templates/`、`/minds/H-WYM-001/`
五个页面文本均**不含** `以史为鉴，知兴替`（页脚首行）。这是「预渲染正文快照只覆盖
列表壳/模板/人物页的正文区块、不含全局页脚」的既有属性，**与计数口径无关**，且不含任何旧值。
如实记录，供后续卡决定是否把页脚纳入静态快照。

### 4.7 本地重建产物 == 线上产物（逐字节）

```text
index.html:               IDENTICAL 4373B   sha=ba414daafc8a（两处同值）
404.html:                 IDENTICAL 4350B   sha=71de255c226d
manifest.webmanifest:     IDENTICAL 1583B   sha=16c45e544b03
manifest-light.webmanifest: IDENTICAL 1583B sha=e10aeb4e9ca2
modes/index.html:         IDENTICAL 19965B  sha=42a8900ddd9e
figures/index.html:       IDENTICAL 16968B  sha=9fbcb62065f6
minds/H-WYM-001/index.html: IDENTICAL 28019B sha=54aaaf122a62
assets/index-*.js:        IDENTICAL 348524B  sha=23ee7d9c1baa
assets/index-*.css:       IDENTICAL 49654B   sha=4ce1c37762b1
data/meta.json:  DIFFER 仅 generated_at / generated_at_local 与 api db sha；counts 逐字段相同
og/manifest.json: DIFFER 仅 total_bytes 与 5 条 PNG bytes；1351 条 alt 全同
sw.js:           DIFFER 仅 DATA_REV = 线上 20260919030806 / 本地 20260919032921
```

结论：§3 的「全产物零违规」扫描对象与线上部署产物**同一字节**（HTML/manifest/JS/CSS 全同），
即该扫描结果对线上有效，不是本地偏样本。

## 5. 全局：发布仓与四条 workflow

### 5.1 发布仓 `ahead=0`

```bash
cd /opt/data/release/Protreptic-publish
git status -sb          # ## main...origin/main      ← 无 [ahead N]
git fetch origin -q
echo ahead=$(git rev-list --count origin/main..HEAD) behind=$(git rev-list --count HEAD..origin/main)
```

```text
ahead=0 behind=0
```

工作区仓（`/opt/data/workspace/Protreptic`）：`git status --porcelain` 输出为空（干净）。

### 5.2 四条 workflow 最新 run（HEAD 4911a21e），**含 job 数与 job 名**（防幻影 0-job）

```bash
gh run list --repo ovmobilegroup/protreptic --limit 12 \
  --json databaseId,name,conclusion,event,headSha --jq '.[] | "\(.databaseId)\t\(.name)\t\(.conclusion)\)"'
gh api repos/ovmobilegroup/protreptic/actions/runs/<id>/jobs --jq '.total_count'
gh api repos/ovmobilegroup/protreptic/actions/runs/<id> --jq '"\(.name) event=\(.event)"'
```

```text
35417672209  Deploy to GitHub Pages  success  event=push  sha=4911a21e   jobs=2
    - 构建 SPA + 文档站: success
    - 部署: success
35417672239  CI                     success  event=push  sha=4911a21e   jobs=1
    - markdown-lint: success
35417672204  Protreptic CI/CD        success  event=push  sha=4911a21e   jobs=6
    - Test (Python + TypeScript): success
    - Build Web Docker Image: success
    - Build API Docker Image: success
    - Notify: success
    - Deploy to Production: skipped
    - Deploy to Staging: skipped
35417876057  Quality Gate           success  event=workflow_run sha=4911a21e  jobs=3
    - Lighthouse 预算门: success
    - 数据校验 (schema + sitemap 一致性): success
    - 线上死链检测 (sitemap + 站内链接): success
```

run `name` 均为真实 workflow 名（不是文件路径），jobs 数均 > 0 —— 不存在 QA3 §附录 A 记录过的
「无效 workflow 文件 → 0-job 幻影失败」。**PASS**。

## 6. 未完成 / 未覆盖（如实列出）

1. 本地未跑 `pages_preflight.py --stage merged` 与 `mkdocs build`（耗时长），
   docs 侧本次改用**线上一手取页**验证（§2），覆盖面等价于此卡要求。
2. `og/**` 图片的**文字**只抽检了站点卡与 `/modes` 卡两张（§4.4）；其余 1349 张 alt 已逐条比对
   （§4.3，0 差异），图上文字未逐张 OCR。
3. §4.6 页脚静态快照缺失为既有属性，本卡不修，仅记录。

## 7. 附录：本报告的取证现场

- 隔离构建副本：`/tmp/qa4_<ts>`（发布仓 HEAD 4911a21e 的 `cp -a`，软链工作区 `node_modules`）
- 独立扫描结果（JSON）：`/tmp/qa4_scan.json`
- 线上 docs 页原文：`/tmp/figlib.html` / `/tmp/figlib.txt`
- Python 侧环境：`/tmp/qa4venv`（CPython 3.12.13 + pillow + fonttools）
