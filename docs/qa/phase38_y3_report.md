# Phase38-Y3 交付报告：UI 可信度徽章 + 统计页（四态如实展示）

- 卡片：`t_7b36ec62`（Phase38-Y3，执行 pigafetta）
- 开发仓：/opt/data/workspace/Protreptic（master）
- 发布仓：/opt/data/release/Protreptic-publish（origin main → GitHub Pages）
- 线上：https://ovmobilegroup.github.io/protreptic
- 上游交付：`t_c0c1c380`（Phase38-Y2 出处链接注入 + verification 四态落地）

## 0 结论（一句话）

三项任务全部落地，且**每条结论都能用命令复现**：四态徽章在真机 DOM 里按 `data-credibility` 可查，
统计页四个数字与 `data/meta.json` 逐项相同（含合计 2798），空态（公开口径 suspect=0）如实显示、不隐藏、
不美化，可点链接覆盖率照实给出 28.6% 并写明「远未到 100%」。

## 1 交付清单（绝对路径 / 体积 / 前 12 位 sha256）

| 产物 | 体积 | sha256(12) |
|---|---|---|
| web/src/components/CredibilityBadge.vue（新，四态徽章唯一实现） | 4602 B | 162d5b82570e |
| web/src/views/CredibilityView.vue（新，/credibility 统计页） | 12116 B | 26c173e0fff6 |
| web/src/components/SourceCitation.vue（徽章移出，变纯出处渲染器） | 1837 B | e39dc81167ff |
| web/src/views/MindView.vue（模式卡加徽章） | 10250 B | 3f45d24515a3 |
| web/src/components/DailyModeCard.vue（每日卡加徽章） | 8618 B | 6dc972b32227 |
| web/src/views/CompareView.vue（对比卡加徽章） | 21923 B | a4ef114df2df |
| web/src/router/index.ts（/credibility 路由） | 5656 B | 6dab553af62c |
| web/src/App.vue（导航 + 页脚入口；断点 lg→xl） | 7986 B | 01583f3b73c3 |
| web/src/generated/siteCounts.ts（生成物：四态 + 覆盖率数字） | 2655 B | 99d26edc92ea |
| tools/site_counts.py（四态/覆盖率的唯一取数入口） | 22706 B | b05a0c3d8dfa |
| tools/gen_web_site_counts.py（注入 SPA 运行时数字） | 10374 B | b17d002122c7 |
| tools/prerender_routes.py（/credibility 静态 head） | 15661 B | b30b6e630009 |
| docs/architecture/web_p0_routes.json（路由清单 1349 条，static 9） | 681153 B | dd5c664b8b90 |
| web/public/sitemap.xml（1350 条，含 /credibility） | 211252 B | d15b6858bb8e |
| docs/qa/phase38_y3/credibility-page.png（四态页截图） | 298011 B | e83604fd7183 |
| docs/qa/phase38_y3/minds-Bach-badges.png（真实三态同框截图） | 625110 B | 7e5d57b78fa1 |
| docs/qa/phase38_y3/daily-card.png（每日一模式徽章截图） | 331739 B | 0263983b9b5b |
| docs/qa/phase38_y3/dom-evidence.json（四态徽章 DOM 原文） | 6702 B | 8e4a0e4a09aa |
| docs/qa/phase38_y3/page-text-zh.txt / page-text-en.txt（页面最终文案原文） | — | — |
| docs/qa/phase38_y3_report.md（本报告） | — | — |

## 2 任务 1：模式卡可信度徽章（四态）

### 2.1 实现（唯一一处）

`web/src/components/CredibilityBadge.vue` 是四态的**唯一实现**：所有调用点都用它，别处不许再写一套文案或符号。

| status | 符号 + 文案 | 视觉 | 悬浮说明（真实字段拼接） |
|---|---|---|---|
| `verified` | `✓ 已核验` | 玉绿 | 可信度：已核验 —— 出处可达，且有可点链接 |
| `pending` | `○ 待核验` | 灰 | 可信度：待核验 —— 尚未核验（schema 缺省态） |
| `suspect` | `⚠ 存疑` | 琥珀（显眼，不美化） | 可信度：存疑 —— 命中缺陷规则，待复核 |
| `unverifiable` | `— 一手材料` | 灰 | 可信度：一手材料 —— 口述/信札等本质不可链接，诚实标注 |

两条诚实约定写进了组件：

1. **字段缺失不猜状态**：`verification` 为空、或 `status` 不在四态内 → 不渲染徽章（少一个标记 ≠ 编一个状态），
   绝不把「没数据」渲染成 `pending`。
2. **悬浮说明只拼真实字段**：`method / evidence / checked_at / checker` 缺哪个写「未记录」，不补故事。

### 2.2 接入点（一条模式只显示一个徽章）

- `/minds/:code` 模式卡：`MindView.vue` 卡片头部（模式名那一行）。
- 每日一模式卡：`DailyModeCard.vue` 编号/分类那一行。
- 跨人物对比卡：`CompareView.vue` 领域/分类 chip 行（以前只在有出处时才有徽章，现在与出处是否存在解耦）。
- `SourceCitation.vue` **移出**徽章，改成纯出处渲染器：否则一条模式会因为「徽章 + 出处块」出现两个徽章，
  而出处为空的模式反而一个都没有。Y2 的三处调用点同步去掉 `:verification` 传参。

### 2.3 真机 DOM 证据（四态）

命令（浏览器真机，非静态推断）：把 `web/dist` 挂到 `http://127.0.0.1:8137/protreptic/` 后取 DOM。

```
# 统计页四态图例（同一组件、同一 props 形状）
https://…/protreptic/credibility/  →  [data-credibility] × 8（4 图例 + 4 卡片头部）
  verified      mark=✓  text=✓已核验     chip=border-jade-400/45 bg-jade-400/10 text-jade-200
  pending       mark=○  text=○待核验     chip=border-white/15 bg-white/[.04] text-parchment/60
  suspect       mark=⚠  text=⚠存疑       chip=border-amber-400/70 bg-amber-400/15 text-amber-200
  unverifiable  mark=—  text=—一手材料   chip=border-white/15 bg-white/[.04] text-parchment/60

# 真实模式卡（/minds/KUB/，10 条模式）
  article [data-credibility] = 10，by state = {"verified": 10}
  样例 outerHTML（节选）：
  <span class="… border-jade-400/45 bg-jade-400/10 text-jade-200" data-credibility="verified"
        data-credibility-mark="✓"
        title="可信度：已核验 —— 出处可达，且有可点链接
  核验方式: link-resolved
  证据: https://zh.wikisource.org/wiki/%E5%85%83%E5%8F%B2
  核验时间: 2026-09-20
  核验人: phase38-y2"><span aria-hidden="true" class="font-mono">✓</span><span>已核验</span></span>

# 真实三态同框（/minds/Bach/，10 条：pending 6 / verified 1 / unverifiable 3）
  同一帧内可见：✓已核验(top=195) · —一手材料(top=911) · ○待核验(top=1648)
  unverifiable 的 tooltip：证据: source_links.json 登记为不可链接 type=unverifiable key=《音乐的奉献》
  pending 的 tooltip：证据: no-citation: 出处无可链接引文

# 每日一模式（/daily/）
  article [data-credibility] = 1，state = pending（当天那条的实测状态）
```

**suspect 的边界（如实说明）**：公开口径 suspect 为 0 条，因此**没有任何一条公开模式卡会渲染 ⚠**；
四态里的 `suspect` 由统计页的四态图例渲染（同一组件、同一 props 形状），17 条源库存疑全部落在隔离记录里，
按设计不进公开产物——这一点写在统计页正文里，不在报告里悄悄略过。

### 2.4 截图路径

- /opt/data/workspace/Protreptic/docs/qa/phase38_y3/credibility-page.png（四态图例 + 四个数字卡，整页）
- /opt/data/workspace/Protreptic/docs/qa/phase38_y3/minds-Bach-badges.png（✓ / — / ○ 三态同框，真实数据）
- /opt/data/workspace/Protreptic/docs/qa/phase38_y3/daily-card.png（每日一模式卡徽章）

## 3 任务 2：站点统计入口（`/credibility`）

### 3.1 入口

- 新路由 `/credibility`（`web/src/router/index.ts`，`seoKind: static`）。
- 顶部导航新增「可信度 / Credibility」；**导航断点从 `lg` 提到 `xl`**：再加一个入口后写死 lg 会在 1024px 撑出横向滚动，
  1280px 下 9 个链接实测 816px、最后一项右边界 1078px，右侧控件从 1238px 开始，不冲突（实测数据见 §5.6）。
- 页脚新增「可信度统计」入口 + 一行四态数字（数字同样来自生成物，不写死）。
- 预渲染 `dist/credibility/index.html` 深链直接 200，并进入 `sitemap.xml`。

### 3.2 取数链（只有一条，不写死、不 fetch 第二份）

```
data/modes_data.json  --(tools/apply_verification_status.py)-->  verification 四态
        |
        v
tools/export_static_site.py  -->  web/public/data/meta.json  counts.verification / counts.citation_links
        |
        +--> tools/site_counts.py::load_verification / load_citation_links   （唯一取数入口，缺键即 exit 1）
                |                        |
                |                        +--> tools/prerender_routes.py  -->  /credibility 的静态 head 标题/描述
                v
        tools/gen_web_site_counts.py  -->  web/src/generated/siteCounts.ts（字面量）
                                                |
                                                v
                                     CredibilityView.vue / CredibilityBadge.vue / App.vue 页脚
```

`tools/apply_site_counts.py` 在构建末期扫描整棵 `dist/**`（2714 个文件）：出现第二种口径立即红。
本次实测 `dist 扫描 2714 个文件零违规；docs 产品门面页 6 个零违规`。

### 3.3 页面内容（四块）

1. 四态数字卡：**已核验 911（32.6%）· 待核验 1547（55.3%）· 存疑 0（0.0%）· 一手材料 340（12.2%）**。
2. 空态说明：公开口径 suspect=0 时**显式**说明「这是实测结果，不是省略」，并给出源库 17 条存疑的去向。
3. 可点链接覆盖率：去重级 1147/4005（28.6%）、出现级 1165/4064、带引文模式 911/2154 至少一个可点，
   并写明「覆盖率远未到 100%：宁可不可点，也不伪造 URL」。
4. 判定口径 + 数字来源（含 `data/meta.json` 直链）+ 尚未做清单（D4/D5 未接入）。

### 3.4 统计数字与 `meta.json` 逐项比对（页面 DOM vs 部署产物）

在页面里 `fetch('/protreptic/data/meta.json')` 后与 DOM 逐项比：

```
状态            DOM     meta.json   equal
verified        911     911         true
pending         1547    1547        true
suspect         0       0           true
unverifiable    340     340         true
四态合计         2798    2798 (counts.verification.published_total)   true
覆盖率文案      「去重级引文 1147 / 4005」「911 / 2154」与 counts.citation_links 一致 = true
（源库口径 meta 值：verified 911 / pending 1579 / suspect 17 / unverifiable 351，合计 2858；隔离 60）
```

## 4 任务 3：诚实原则（页面最终文案原文）

以下为 `/credibility` 页面 `main` 区渲染出来的**最终文案原文**（zh，取自真机 DOM `innerText`）：

```
CREDIBILITY 统计页
可信度统计

这一页如实公布每条模式的核验状态：已核验、待核验、存疑、一手材料。 存疑比假装全对更可信。

发布口径合计 2798 条模式摘要（站上打得开的那些）；源库口径 2858 条，其中 60 条隔离记录不进公开产物，也不计入下列四态。

✓ 已核验  32.6%  911   出处可达，且构建期解析出可点链接
○ 待核验  55.3%  1547  尚未核验（schema 缺省态）
⚠ 存疑    0.0%   0     命中缺陷规则，待复核 —— 显眼标注，不美化
— 一手材料 12.2% 340   口述 / 信札等本质不可链接，诚实标注而非硬造链接

公开口径「存疑」当前为 0 条 —— 这是实测结果，不是省略：源库口径另有 17 条存疑，全部落在隔离记录里，
按 D3 豁免条款只服务复核与回滚，不进公开产物。

可点链接覆盖率
去重级引文 1147 / 4005 条有真实可达的链接（28.6%）；出现级引文段 1165 / 4064 有链接；
911 / 2154 条带引文的模式至少有一个可点出处。
覆盖率远未到 100%：解析不到链接的出处保持纯文本，宁可不可点，也不伪造 URL。

四态怎么判
✓ 已核验  出处可达 + 构建期解析到可点链接
○ 待核验  尚未核验，schema 缺省态
⚠ 存疑    命中 D1–D5 之一，待复核
— 一手材料 口述 / 信札 / 档案等本质不可链接
判定规则与处置口径见仓库 docs/planning/credibility_framework.md §1 与 §3。

数字从哪来
唯一来源：部署产物 data/meta.json 的 counts.verification。 data/meta.json
SPA 侧数字由 tools/gen_web_site_counts.py 在构建前注入（本页不写死、不 fetch 第二份）。
静态 head 的四态数字由 tools/prerender_routes.py 用同一份 meta.json 现算；两处不一致，构建立刻失败。
尚未做（如实列出）
D4 引文与原文逐字比对、D5 时间线机检仍缺输入，未接入流水线 —— 因此「已核验」只声称出处可达，不声称引文已逐字核对。
链接源覆盖面有限：被引书名绝大多数尚无链接源，覆盖率见上。
```

英文版同页（`page-text-en.txt`）逐句对应，如
`Public "suspect" currently equals 0 — that is a measurement, not an omission: the source scope holds 17 more suspect records, all inside quarantined figures, excluded from public output.`

**没有出现**：把 0 说成「无问题」、把覆盖率说成「全部可点」、把隔离记录混进发布口径。

## 5 自检证据（命令 + 输出）

### 5.1 SPA 构建（必修）

```
$ cd web && VITE_DATA_MODE=static npm run build
> vue-tsc && vite build
vite v5.4.21 building for production...
✓ 144 modules transformed.
dist/index.html                   3.66 kB │ gzip:   2.08 kB
dist/assets/index-uLX7QpAY.css   50.37 kB │ gzip:   9.43 kB
dist/assets/index-BGkPoJqG.js   352.62 kB │ gzip: 129.51 kB
✓ built in 5.18s
```

（期间修掉一处真实类型错误：`siteCounts.ts` 是 `as const` 字面量类型，`v.published.verified === 0` 这种空态判断
被 vue-tsc 判为「类型无交集」。修法是显式把生成物放宽为 `number` 类型别名——
不是删掉空态分支，空态判断必须留在运行时。）

### 5.2 构建链（顺序：build_figures_db → export_static_site → build_unified_index → …）

```
== 1 build_figures_db ==     （重建 figures 库）
== 2 export_static_site ==   [核验] verification 四态 (公开口径):
                             verified=911 / pending=1547 / suspect=0 / unverifiable=340 / total=2798
                             [OK] 隔离名单零泄漏（H-P23F-001, H-SX-001, P24F, P25F, P26F, Phase27Final；被剔模式 60 条）
                             [OK] 产物 1345 个文件；figures=1057 modes(发布)=2798 by-figure=278
== 3 build_daily_index ==    [daily] 模式 2798 条 / 人物 278 位
== 4 build_unified_index ==  total=1333 figures=278 scenarios=1055
== 5 gen_web_site_counts ==  已最新 (2798 x 278)
== 6 npm build ==            见 §5.1
== 7 prerender_routes ==     [prerender] base=/protreptic/ routes=1349；wrote 1349 index.html
                             route manifest -> docs/architecture/web_p0_routes.json
== 8 apply_site_counts ==    收口完成: 2798 条模式 × 278 位人物
                             dist 扫描 2714 个文件零违规；docs 产品门面页 6 个零违规
== 9 build_sitemap ==        entries=1350；by kind {"static": 9, …}
== 10 build_sw ==            [sw] BUILD_ID=e5426fa31874 DATA_REV=20260920041332
== 11 pages_preflight --stage dist ==  [OK] stage=dist：全部断言通过
CHAIN-OK
```

### 5.3 生成物与静态 head 一致

```
$ python3 tools/gen_web_site_counts.py
[counts] 可信度四态 (发布口径 2798): 已核验 911 / 待核验 1547 / 存疑 0 / 一手材料 340
[counts] 可点链接覆盖率: 去重级 1147/4005, 出现级 1165/4064, 带引文模式 911/2154 至少一个可点
$ python3 tools/gen_web_site_counts.py --check
[counts] web/src/generated/siteCounts.ts 已是当前口径 (2798 x 278)

$ grep -o "<title>[^<]*</title>" web/dist/credibility/index.html
<title>可信度统计 - 已核验 911 / 待核验 1547 / 存疑 0 / 一手材料 340 | Protreptic 思想典藏</title>
$ grep -o 'name="description" content="[^"]*"' web/dist/credibility/index.html
name="description" content="发布口径 2798 条模式摘要的核验状态：已核验 911、待核验 1547、存疑 0、一手材料 340
（源库另有 60 条隔离记录不进公开产物）；数据取自 data/meta.json。"

$ grep -o "https://ovmobilegroup.github.io/protreptic/credibility" web/public/sitemap.xml
https://ovmobilegroup.github.io/protreptic/credibility
$ grep -o "https://ovmobilegroup.github.io/protreptic/credibility" web/dist/sitemap.xml
https://ovmobilegroup.github.io/protreptic/credibility
$ grep -o '"path": "credibility"' docs/architecture/web_p0_routes.json
"path": "credibility"          （路由清单 16455 行，routes=1349，static 9）
```

### 5.4 真机 DOM 与 meta.json 比对

见 §2.3 与 §3.4：四态数字 DOM == meta.json（4/4 equal，合计 2798），覆盖率文案与 `counts.citation_links` 一致。

### 5.5 全链回归（三道门 + 预检，本卡现场重跑）

```
$ python3 tools/credibility_gate.py --hard-fail
--- 新增（基线外，必拦）: 0 条 ---
warnings (D4/D5, 非阻断): 17
[OK] hard-fail: 无新增硬失败（存量 527 条已冻结）-> exit 0

$ python3 tools/verify_source_links.py --hard-fail
  ::warning::UNREACHABLE 《基督教的本质》 -> https://zh.wikipedia.org/wiki/…
  ::warning::UNREACHABLE 《新疆生产建设兵团志》 -> https://zh.wikipedia.org/wiki/…
  ::warning::UNREACHABLE 《海岳名言》 -> https://zh.wikisource.org/wiki/…
[OK] hard-fail: 无新增坏链（存量 0 条已冻结）-> exit 0

$ python3 tools/verify_findings.py --hard-fail
--- 其他警告（不阻断）: 1 条 ---
  ::warning:: these mode codes are harvested twice by get_all_modes … ['M-ASM-001' … 'M-ASM-010']
[OK] hard-fail: 无新增硬失败（存量 0 条已冻结）-> exit 0

$ python3 tools/pages_preflight.py --stage dist
[OK] stage=dist：全部断言通过
```

（连接层 UNREACHABLE 只算警告：CI 网络抖动不该把发布链打红，口径见 credibility_framework.md §7。）

### 5.6 导航断点实测（1280/1024/1440）

```
1024px: docScroll 1014 == clientW 1014（无横向溢出）；桌面导航隐藏、可横向滚动的入口显示，/credibility 可达
1280px: 桌面导航 9 个链接，链接行 816px，无溢出；最后一项右边界 1078px，右侧控件起点 1238px
1440px: 同上，无溢出
```

## 6 两仓同步 / push / CI 台账

（本节在推送与 CI 结束后补写真实 run 号；未补写前不得声称 CI 绿。）

## 7 未做与边界（如实清单）

1. **公开口径 suspect = 0**：四态里的 ⚠ 只由统计页图例渲染，没有真实公开模式卡会显示 ⚠（17 条源库存疑在隔离记录里，按设计不进公开产物）。
2. **引文逐字比对（D4）与时间线机检（D5）未接入**：因此 `verified` 只声称「出处可达 + 有可点链接」，不声称引文已逐字核对。
3. **链接覆盖率未提升**：本次只做展示（去重级 1147/4005 = 28.6%，与 Y2 相同），没有新增链接源。
4. **`gen_web_site_counts.py --check` 未接进 CI**：目前靠 Pages 流水线里的生成步骤 + `apply_site_counts` 的交叉校验兜底，`--check` 仍是本地自检口径。
5. **`/credibility` 无静态正文快照**：与 /daily、/concepts、/graph、/compare、/api 同口径，只预渲染 head（无 JS 的 UA 读到标题与描述，正文靠 JS）。
6. **api/protreptic.db 不提交**：CI 现场重建，字节不确定（沿用 Y1/Y2 处置）。
7. **统计页不做「按人物/按机构」下钻**：只给四态总量与覆盖率，不新增筛选维度（避免与 /figures、/modes 口径分叉）。
