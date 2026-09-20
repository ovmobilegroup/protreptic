# Phase38-Y2 交付报告：构建期链接注入 + verification 状态推进 + 前端渲染

卡片：`t_c0c1c380`（负责人 elcano）　日期：2026-09-20
上游：`t_d76b44c3`（Phase38-Y1，链接源 50 key -> 382 key）
依据：`docs/planning/credibility_framework.md` 第 2 节（链接源）/ 第 3 节（verification schema）

本报告所有结论都附命令与原始输出；未做到的写在最后「边界与未做」里，不粉饰。

---

## 0. 先把输入事实钉死（命令 + 输出）

```
$ python3 tools/source_link_index.py --links-path data/source_links.json
index keys: 382  (data/source_links.json)
```

```
$ python3 tools/apply_verification_status.py
库: data/modes_data.json (2868 条模式, sha256 9e08650499c56aef)
链接源: data/source_links.json (382 key, 其中有 url 169)
D4/D5 命中: 17 条模式 {"present": true, "by_defect": {"D4_quote_without_source": 17}}
```

即：索引是 382 个 key（169 条带 url / 213 条登记为不可链接），落在 `source_link_index.py` 的 R0-R3 规则上；
D4 命中 17 条、D5 = 0 条（findings.json 里 D5 是 `N/A - no figures_db.json available`）。

---

## 1. 构建期注入：出处 -> 可点引用（唯一实现在 source_link_index.py）

改的是导出链（`tools/export_static_site.py`），新增一个纯函数 `inject_citation_links(modes, index)`，
给每条模式加**两个新字段**（不改任何既有字段）：

| 字段 | 内容 | 用途 |
|---|---|---|
| `source_refs` | 每条引文的机读匹配结果 `[{citation, key, url, status, match_rule}]` | 机器消费 / QA 复核 |
| `source_parts` | 出处文本分段：纯文本段 `{text}` + 可点段 `{text, url, key}` | 前端按段渲染，不写死 HTML |

铁律落实：

* 只有 `status == linked`（索引里有非空 url）的段才带 url；`unresolved` 的引文**原样留在纯文本段**里；
* 自洽断言写死在导出里：`"".join(段文本) != source_chapter` 直接 `SystemExit`，不允许静默降级；
* 规则本身**不在导出里重写**，一律 `from source_link_index import load_index, resolve_source_chapter`（R0-R3 唯一实现）。

命令与输出（真实 run）：

```
$ python3 tools/export_static_site.py
  [出处] 注入可点引用: 2154 条模式带引文, 911 条有至少 1 个可点链接
         去重级引文 4005 条 (linked 1147 / registered-unlinkable 939 / unresolved 1919); 出现级书名号段 4064 段 (linked 1165)
```

**计数分两个层级，键名里写死，不许混着说**（这就是本卡自己先踩过的坑：第一版日志把「去重级总数 4005」
和「出现级 linked 1165」印在同一行，加起来对不上，已改成两级各自成句）：

* **去重级** `citations_*`：一条模式内同一条引文出现多次只算 1 条 —— 与 `source_link_index.py --coverage`
  的 `extract_refs` 同口径，也是 Y1 覆盖率报告的口径；`1147 + 939 + 1919 = 4005`（三态求和自洽，导出里是硬断言）；
* **出现级** `segments_*`：出处文本里每个书名号跨度算 1 段 —— 渲染层真正处理的粒度（同一本书在同一条出处里
  被引两次 = 2 段 / 1 条引文）；`1165 + 2899 = 4064`。

与 Y1 覆盖率报告的对账（`tools/source_link_index.py --coverage` 原样复跑，逐字一致）：

| 口径 | 去重级引文 | 去重级 linked | 出现级书名号段 | 出现级 linked |
|---|---|---|---|---|
| 全库 2868（Y1 覆盖率口径） | 4016 | 1147 | 4075 | 1165 |
| 公开 2798（本卡产物口径） | 4005 | 1147 | 4064 | 1165 |

差 11 条引文全部在隔离人物（60 条模式）里，且它们都不是可点链接，所以 linked 两级都不变 —— 三份数字（Y1 报告、
`--coverage`、本卡产物）因此可以逐条对上，不是「各说各话」。

---

## 2. 注入前后样本对照（同一张卡、逐字可核）

样本：`M-KUB-010`（忽必烈，figure `KUB`），出处里既有能解析的古籍、也有解析不到的事件文书。
「注入前」= 回滚 `tools/export_static_site.py` 后重跑导出到 `/tmp/before_data` 的真实产物（`git stash push -- tools/export_static_site.py`），
「注入后」= 本卡产物；两次导出**唯一差异**就是注入字段（verification 状态此时两版都已是新值，不影响对照）。

```
$ python3 /tmp/sample1.py
BEFORE keys: ['source_chapter', 'verification']
AFTER  keys: ['source_chapter', 'source_parts', 'source_refs', 'verification']
```

出处文本（两版逐字相同）：

```
《元史·世祖纪》：中统元年五月《中统建元诏》'建元表岁，示人君万世之传'；至元元年八月《至元改元诏》取《易经》'至哉坤元'之义；至元八年十一月《建国号诏》：'可建国号曰大元，盖取《易经》乾元之义'，并称'舆图之广，历古所无'；刘秉忠之议见《元史·刘秉忠传》；蒙古语中仍称'大元大蒙古国'（Dai Ön yeke Mongghol ulus）——双语双号并行的命名分层；'中统'年号本身即'中华正统'的语义宣言
```

注入后 `source_refs`（6 条引文：4 条 linked / 2 条 unresolved）：

```
{"citation": "元史·世祖纪",   "key": "《元史》",     "url": "https://zh.wikisource.org/wiki/%E5%85%83%E5%8F%B2", "status": "linked",     "match_rule": "prefix"}
{"citation": "中统建元诏",     "key": null,           "url": "",                                          "status": "unresolved", "match_rule": null}
{"citation": "至元改元诏",     "key": null,           "url": "",                                          "status": "unresolved", "match_rule": null}
{"citation": "易经",           "key": "《易经》",     "url": "https://zh.wikisource.org/wiki/%E5%91%A8%E6%98%93", "status": "linked",     "match_rule": "exact"}
{"citation": "建国号诏",       "key": "《建国号诏》", "url": "https://zh.wikisource.org/wiki/%E5%BB%BA%E5%9C%8B%E8%99%9F%E8%A9%94", "status": "linked", "match_rule": "exact"}
{"citation": "元史·刘秉忠传", "key": "《元史》",     "url": "https://zh.wikisource.org/wiki/%E5%85%83%E5%8F%B2", "status": "linked",     "match_rule": "prefix"}
```

`source_parts`（节选，展示「匹配不到就是纯文本」）：

```
[{"text":"《元史·世祖纪》","url":"https://zh.wikisource.org/wiki/%E5%85%83%E5%8F%B2","key":"《元史》"},
 {"text":"：中统元年五月"},
 {"text":"《中统建元诏》"},                      <-- unresolved，无 url，保持纯文本
 {"text":"'建元表岁，示人君万世之传'；至元元年八月"},
 {"text":"《至元改元诏》"},                      <-- unresolved，无 url，保持纯文本
 {"text":"取"},
 {"text":"《易经》","url":"https://zh.wikisource.org/wiki/%E5%91%A8%E6%98%93","key":"《易经》"},
 ...]
```

---

## 3. verification 状态推进（四态规则的唯一实现）

新增 `tools/apply_verification_status.py`（数据准备工具，不是导出链的构建步骤；`--write` 显式才落盘）。
判定顺序 = 优先级，先命中先定：

| 顺序 | 状态 | 判定 | 写入字段 |
|---|---|---|---|
| S1 | `suspect` | `mode_code` 命中 `data/audit/findings.json` 的 D4/D5（引文不符 / 时间线矛盾） | method=auto-scan |
| S2 | `verified` | 出处至少一条引文解析到**可达链接**（url 非空） | method=link-resolved, evidence=该 url |
| S3 | `unverifiable` | 出处有引文且**全部**命中索引里「已登记不可链接」（url 为空：口述 / 信札等一手材料） | method=auto-scan |
| S4 | `pending` | 其余（无书名号引文 / 引文全部 unresolved） | method=auto-scan |

两个口径必须说清（否则数字对不上会被当成说谎）：

* **为什么 S1 优先于 S2**：同一条模式既「链接可达」又「引文与原文不符」时，不应给出「已核验」。
  实测当前库 S1 与 S2 的交集 = **0 条**（下面输出里的 `S1 交 S2 的重叠`），所以这条优先级目前不改变任何一条结果；
* `suspect` 在公开口径是 **0 条**：17 条 D4 命中全部属于隔离人物（`H-P23F-001` / `P24F` / `P25F` / `P26F` / `Phase27Final`），
  它们整片不进公开产物（`tools/_quarantine.py`）。这是「0」而不是「漏判」，源库口径里 17 条逐条可查。

命令与输出：

```
$ python3 tools/apply_verification_status.py --write
四态（全库 2868 条）:        verified 911 / pending 1589 / suspect 17 / unverifiable 351
四态（公开口径 2808 条, 已剔除隔离人物）: verified 911 / pending 1557 / suspect 0 / unverifiable 340
S1 交 S2 的重叠（既命中 D4/D5 又解析出可达链接）: 0 条
与库中现状态相比的变更: pending -> suspect=17, pending -> unverifiable=351, pending -> verified=911
[OK] 自洽断言: 四态求和等于模式条数; verified 的 evidence 全部回查到索引 url (146 个不同 url)
[OK] 公开口径求和自洽: 公开 2808 加隔离 60 等于全库 2868
[OK] 已写回 data/modes_data.json （回读四态一致, bytes 22814954）

$ python3 tools/apply_verification_status.py --check      # 复跑校验：库中状态与规则逐条一致
[OK] --check: 库中状态与本规则逐条一致        （exit 0）
```

写盘影响面（防止「悄悄改了一堆东西」）：

```
$ git diff data/modes_data.json | grep '^[+-]' | grep -v '^[+-][+-]' | grep -vE '"(status|method|evidence|checked_at|checker)"' | wc -l
0
```

即：diff 里**只有** verification 的 5 个键，没有别的改动。文件字节数 22634128 -> 22814954，
格式与源文件逐字节同构（`json.dumps(..., ensure_ascii=False, indent=2)` 实测与原文件 sha256 相同，
所以没有整文件重排）。

机读产物：`data/audit/verification_status.json`（规则 / 优先级 / 输入坐标 + sha / 两个口径的四态 / 交叉校验 / 变更统计）。

---

## 4. `meta.json` 四态计数（自洽）

`tools/export_static_site.py` 的 `counts` 新增两块，并在写 meta 前做求和断言
（`published_total != mode_summaries_published` 直接 `SystemExit`，不让 meta 说谎）：

```
$ python3 tools/export_static_site.py
  [核验] verification 四态 (公开口径): verified=911 / pending=1547 / suspect=0 / unverifiable=340 / total=2798
  meta.json counts={... "verification": {"published": {"verified": 911, "pending": 1547, "suspect": 0,
      "unverifiable": 340}, "published_total": 2798, "all": {"verified": 911, "pending": 1579,
      "suspect": 17, "unverifiable": 351}, "all_total": 2858, "quarantined_total": 60},
      "citation_links": {"modes_with_citations": 2154, "modes_with_link": 911, "citations": 4005,
      "citations_linked": 1147, "citations_registered_unlinkable": 939, "citations_unresolved": 1919,
      "segments": 4064, "segments_linked": 1165}}
```

自洽关系（四条，逐条可复算）：

1. 公开口径求和 `911 + 1547 + 0 + 340 = 2798` = `counts.mode_summaries_published`（= `modes/index-*.json` 合计）；
2. 源库口径求和 `911 + 1579 + 17 + 351 = 2858` = `counts.mode_summaries`（去重口径；另有 10 条空 `mode_code` 在导出时丢弃）；
3. `all_total - published_total = 60` = `counts.modes_quarantined`；
4. `citation_links` 两级各自自洽：`1147 + 939 + 1919 = 4005`（去重级），`segments_linked 1165 <= segments 4064`（出现级）。

公开口径与「数据准备工具」口径的差异也是明的：本文件第 3 节的「公开 2808」是**源库按 figure_code 非隔离**算的
（含 10 条空 code 记录），导出的「2798」是**去掉空 code 之后真正写进分片**的条数，两者相差 10，可逐条对上。

---

## 5. 前端渲染：有链接=可点（新窗口），无链接=纯文本，排版不动

改动面（4 个文件改 + 1 个新组件）：

| 文件 | 改了什么 |
|---|---|
| `web/src/components/SourceCitation.vue` | **新增**：按 `source_parts` 分段渲染，可点段 `<a target="_blank" rel="noopener noreferrer">`，其余纯文本；可选四态徽章。全是行内元素，不新增块级盒子 |
| `web/src/views/MindView.vue` | 出处元素换成 `SourceCitation`，透传 `source_parts` / `verification` |
| `web/src/components/DailyModeCard.vue` | 同上（`/` 首页卡片与 `/daily` 共用） |
| `web/src/api/compareData.ts` | `CompareMode` 新增 `sourceParts` / `verification`（类型 `CompareSourcePart`），从 by-figure 分片读 `source_parts`，解析不到就是空数组 |
| `web/src/views/CompareView.vue` | 对照表「出处」单元格改用 `SourceCitation`（`—` 兜底不变） |

回退性质：三个调用点都写成「有 `source_parts` 就分段、没有就渲染纯文本 `source_chapter`」，
所以**旧分片 / 未注入数据下行为与改动前一致**，不是硬依赖。

### 5.1 构建通过

```
$ cd web && VITE_DATA_MODE=static npm run build
> vue-tsc && vite build
✓ 140 modules transformed.
dist/assets/index-CJgXzmD_.css   49.80 kB │ gzip:   9.35 kB
dist/assets/index_D_FkVB0g.js   341.82 kB │ gzip: 124.95 kB
✓ built in 5.06s
```

（`vue-tsc` 类型检查通过 —— 上面那条 `> vue-tsc && vite build` 没有报错）

### 5.2 本地渲染后的 DOM 片段（含 `<a href>`）

用仓库既有的预渲染步骤产出真 DOM（`python3 tools/prerender_routes.py --body-persons all`，
1348 个路由页、`total_html_bytes` 19337482 -> 19705419），再取 `/minds/KUB` 那一页的出处段落：

```
$ python3 /tmp/extract_dom.py
<p class="mt-4 text-sm text-parchment/55">出处：<a href="https://zh.wikisource.org/wiki/%E5%85%83%E5%8F%B2" target="_blank" rel="noopener noreferrer" class="text-gold-300/90 underline decoration-gold-500/40 underline-offset-2 hover:text-gold-200">《元史·世祖纪》</a>：中统元年五月《中统建元诏》'建元表岁，示人君万世之传'；至元元年八月《至元改元诏》取<a href="https://zh.wikisource.org/wiki/%E5%91%A8%E6%98%93" target="_blank" rel="noopener noreferrer" class="text-gold-300/90 underline decoration-gold-500/40 underline-offset-2 hover:text-gold-200">《易经》</a>'至哉坤元'之义；至元八年十一月<a href="https://zh.wikisource.org/wiki/%E5%BB%BA%E5%9C%8B%E8%99%9F%E8%A9%94" target="_blank" rel="noopener noreferrer" class="text-gold-300/90 underline decoration-gold-500/40 underline-offset-2 hover:text-gold-200">《建国号诏》</a>：'可建国号曰大元，盖取<a href="https://zh.wikisource.org/wiki/%E5%91%A8%E6%98%93" target="_blank" rel="noopener noreferrer" class="text-gold-300/90 underline decoration-gold-500/40 underline-offset-2 hover:text-gold-200">《易经》</a>乾元之义'，并称'舆图之广，历古所无'；刘秉忠之议见<a href="https://zh.wikisource.org/wiki/%E5%85%83%E5%8F%B2" target="_blank" rel="noopener noreferrer" class="text-gold-300/90 underline decoration-gold-500/40 underline-offset-2 hover:text-gold-200">《元史·刘秉忠传》</a>；蒙古语中仍称'大元大蒙古国'（Dai Ön yeke Mongghol ulus）——双语双号并行的命名分层；'中统'年号本身即'中华正统'的语义宣言 <span class="pt-chip-jade">已核验</span></p>
```

同一段里可直接看清两条铁律都生效：《中统建元诏》《至元改元诏》在索引里没有链接源，**保持纯文本、不给 href**。

预渲染全量统计：

```
预渲染人物页 278 个，其中 135 个的出处段落含可点链接，出处链接总数 1120
```

### 5.3 真浏览器里跑 SPA（Vue 运行时）的自证

预渲染是静态快照；为证明**运行时组件**也照同一份数据渲染，本地起静态服务器用真浏览器读了挂载后的 DOM：

```
http://127.0.0.1:8099/protreptic/minds/KUB        -> 页面内 <a href^="https://"> 32 个
http://127.0.0.1:8099/protreptic/compare?items=KUB,H-WYM-001 -> 表格内可点出处 41 个
http://127.0.0.1:8099/protreptic/               -> 当日「每日一模式」卡片：该条出处无链接源
                                                  （渲染成纯文本 + 「待核验」徽章，符合预期）
```

文本保真自检（把 SPA 渲染出的出处 `textContent` 去掉徽章后，与分片里的 `source_chapter` 逐字对比）：

```
对比 10 条出处：逐字一致 10 条，不一致 0 条
```

即：注入只是**把可点位置换成 `<a>`**，文本一个字符都没动，排版（行内元素）也没变。

---

## 6. 抽 8 条生成链接 curl 实测（证明不是死链）

```
$ python3 /tmp/curl5.py      # 从产物里随机抽 8 个不同 url（种子 38），curl -L --max-time 25
候选不同 url 总数: 159
200 160274  M-BAI-001 BAI        https://zh.wikisource.org/wiki/%E6%96%B0%E6%A8%82%E5%BA%9C
200 78904   M-HZX-004 H-HZX-001  https://zh.wikisource.org/wiki/%E6%98%8E%E5%84%92%E5%AD%B8%E6%A1%88
200 75642   M-SQ-001  H-SQ-001   https://zh.wikipedia.org/wiki/%E6%88%B0%E5%9C%8B%E7%B8%B1%E6%A9%AB%E5%AE%B6%E6%9B%B8
200 147501  M-VLL-003 VLL        https://zh.wikipedia.org/wiki/%E5%9F%8E%E5%B8%82%E8%88%87%E7%8B%97
200 85562   M-SYX-001 SYX        https://zh.wikisource.org/wiki/%E5%A4%A9%E5%B7%A5%E9%96%8B%E7%89%A9
200 63136   M-YSS-001 H-YSS-001  https://zh.wikisource.org/wiki/%E6%9D%8E%E5%BF%A0%E6%AD%A6%E5%85%AC%E5%85%A8%E6%9B%B8
200 201044  M-MF-003  H-MF-001   https://zh.wikisource.org/wiki/%E5%AE%8B%E5%8F%B2
200 234421  M-DSF-002 H-DSF-001  https://zh.wikipedia.org/wiki/%E5%8D%A1%E6%8B%89%E9%A6%AC%E4%BD%90%E5%A4%AB%E5%85%84%E5%BC%9F
```

8/8 = HTTP 200 且拿到真实正文体积（不是挑战页 / 空页）。

---

## 7. 体积代价（诚实报出来）

注入是**加法**，代价必须说清（before/after 均为真实产物，`/tmp/analyze_gz.py`）：

| 口径 | 注入前 | 注入后 | 变化 |
|---|---|---|---|
| `modes/by-figure/**` raw 合计 | 18048585 B | 19248560 B | +1199975 B（+6.6%） |
| `modes/by-figure/**` gzip 合计 | 7547022 B | 7670672 B | +123650 B（+1.6%） |
| 单片 gzip 中位 | — | — | +410 B |
| 单片 gzip 最大增量 | — | — | +3336 B |
| `modes/index-*.json` | 不变（摘要索引只有 8 个字段，不注入） | 不变 | 0 |
| `figures/**` | 不变 | 不变 | 0 |

gzip 后中位每片只多 410 B；`modes/index` 与 `figures` 完全没变（`meta.json` 里这两块的 sha256 与注入前逐字节相同）。

---

## 8. 本地全链路执行记录（按 pages.yml 的真实顺序）

| # | 命令 | 结果 |
|---|---|---|
| 1 | `python3 tools/build_figures_db.py` | ✅ figures 表重建 1057 行 —— 但**该文件重建字节不确定**（连跑两次 sha256 不同：`00952cbd…` / `6014c9c5…`），故 `git checkout -- api/protreptic.db` 回退；§9.3 本来就把 `api/protreptic.db` 排除在两仓一致性之外（CI 现场重建） |
| 2 | `python3 tools/export_static_site.py` | ✅ 产出 1345 个文件；`[出处]` 注入统计见第 1 节 |
| 3 | `python3 tools/gen_web_site_counts.py` | ✅ 已最新（2798 x 278），未改动 |
| 4 | `python3 tools/build_daily_index.py` | ✅ 模式 2798 / 人物 278 / 分片 278 |
| 5 | `python3 tools/pages_preflight.py --stage data` | ✅ `stage=data：全部断言通过`（隔离命中 0） |
| 6 | `python3 tools/build_search_index.py` | ✅ 16 个分片，总 gzip 521.9 KB |
| 7 | `python3 tools/build_graph_data.py` | ✅ 模式图 3238 节点 / 概念图 12942 概念 |
| 8 | `python3 tools/build_unified_index.py` | ✅ total=1333 figures=278 scenarios=1055 |
| 9 | `cd web && VITE_DATA_MODE=static npm run build` | ✅ vue-tsc + vite build 通过 |
| 10 | `python3 tools/pages_preflight.py --stage dist` | ✅ `stage=dist：全部断言通过` |
| 11 | `python3 tools/prerender_routes.py --body-persons all` | ✅ 1348 路由 / 19244 KB |
| 12 | `python3 tools/apply_site_counts.py` | ✅ `dist 扫描 2718 个文件零违规；docs 产品门面页 6 个零违规` |
| 13 | `python3 tools/build_sw.py` / `build_sitemap.py` | ✅ 预缓存 30 项 / sitemap 1349 条 |
| 14 | `python3 tools/credibility_gate.py --hard-fail --data-path data/modes_data.json` | ✅ exit 0（存量 527 冻结，新增 0） |
| 15 | `python3 tools/verify_source_links.py --hard-fail` | ✅ exit 0（新增坏链 0；Wikimedia 限流计 UNREACHABLE 警告，按 Phase37-X3 口径不算违规） |
| 16 | `python3 tools/verify_findings.py --hard-fail --data-path data/modes_data.json` | ✅ exit 0（先跑 `build_audit_findings.py --write` 清掉「计数过期(E)」，该次写盘 diff 只有 `scan_date` + `modes_file_sha256` 两行） |

**没跑的两步（诚实标注）**：`tools/build_og_images.py` 与 `tools/apply_og_meta.py` 需要 `pillow` / `fonttools`，
本机 `python3 -m pip` 不存在（`No module named pip`），装不了依赖，所以**只在 CI 里跑**。
这两步只写 `og:image` / `twitter:image` 与分享图文件，不碰出处渲染，也不影响本次改动的任何结论。

---

## 9. 两仓同步 · push · CI 回读（原始证据）

### 9.1 同步与机检

15 个文件从开发仓镜像进发布仓（`shutil.copy2` + 逐个 sha256 断言相等），新文件两侧都 `git add`：

```
data/audit/findings.json                         data/modes_data.json
data/audit/verification_status.json (新)          docs/architecture/static_data_manifest.json
docs/architecture/web_p0_routes.json             docs/qa/phase38_y2_link_injection.md (新)
tools/export_static_site.py                      tools/prerender_body.py
tools/apply_verification_status.py (新)           web/public/sitemap.xml
web/src/api/compareData.ts                       web/src/components/DailyModeCard.vue
web/src/components/SourceCitation.vue (新)        web/src/views/CompareView.vue
web/src/views/MindView.vue
```

```
$ python3 tools/check_repo_parity.py
[OK] 零差异：1316 个构建图文件两仓逐字节一致（sha256）
```

markdown-lint 本地复跑（CI 用的就是它，`npx markdownlint-cli2@0.13.0`）：

```
$ npx --yes markdownlint-cli2@0.13.0 "docs/qa/phase38_y2_link_injection.md"
Summary: 0 error(s)
```

### 9.2 push 与 CI

发布仓 `main` 两次 push（第二次是 §4 计数口径修正；按项目纪律不改写历史，追加提交）：

```
$ git push origin main
   88161b7..8ae8172  main -> main        （第一次：注入 + 四态 + 前端）
   8ae8172..56cae91  main -> main        （第二次：注入统计口径两级化）
$ git status -sb           ## main...origin/main       <- 无 [ahead N]
$ git rev-parse HEAD            56cae91b47a50826b50f5d1a45a5e2355464359c
$ git ls-remote origin refs/heads/main
56cae91b47a50826b50f5d1a45a5e2355464359c refs/heads/main    <- 回读一致（sha 与 ref 之间原文为制表符）
```

`56cae91` 四个工作流全绿（GitHub Actions API 回读）：

| 工作流 | run id | 结论 | 耗时（started -> updated） |
|---|---|---|---|
| Protreptic CI/CD | 35485720976 | success | 03:06:34 -> 03:16:32 |
| Deploy to GitHub Pages | 35485720982 | success | 03:06:34 -> 03:18:0x |
| CI（markdown-lint） | 35485720987 | success | 03:06:34 -> 03:06:50 |
| Quality Gate | 35485732308 | success | 03:06:53 -> 03:08:37 |

### 9.3 线上回读（部署后实测，不是「应该已经生效」）

```
$ curl -s https://ovmobilegroup.github.io/protreptic/data/meta.json
generated_at: 2026-09-20T03:13:18+00:00
verification.published: {"verified": 911, "pending": 1547, "suspect": 0, "unverifiable": 340} total 2798
verification.all     : {"verified": 911, "pending": 1579, "suspect": 17, "unverifiable": 351} total 2858
citation_links       : {"modes_with_citations": 2154, "modes_with_link": 911, "citations": 4005,
                        "citations_linked": 1147, "citations_registered_unlinkable": 939,
                        "citations_unresolved": 1919, "segments": 4064, "segments_linked": 1165}
自洽: published 求和 = 2798 == published_total 2798
自洽: citations 求和 = 4005 == citations 4005
sources sha256 modes_data.json: 9e08650499c56aef     <- 与本机 data/modes_data.json 同一份
```

```
$ curl -s https://ovmobilegroup.github.io/protreptic/data/modes/by-figure/KUB.json
mode: M-KUB-010 大哉乾元命名法
verification: {"status": "verified", "method": "link-resolved", "evidence": "https://zh.wikisource.org/wiki/%E5%85%83%E5%8F%B2", "checked_at": "2026-09-20", "checker": "phase38-y2"}
source_refs 条数: 6 其中 linked: 4
source_parts 段数: 14 可点段: 5
分段文本拼回 == source_chapter: True
```

```
$ curl -s -o /dev/null -w "%{http_code}\n" https://ovmobilegroup.github.io/protreptic/
200
$ curl -s https://ovmobilegroup.github.io/protreptic/minds/KUB/ | grep -o '<a href="https://[^"]*" target="_blank" rel="noopener noreferrer"' | wc -l
31
```

即：线上分片带 `source_refs` / `source_parts`，线上 HTML 的出处已是新窗口可点链接（`target="_blank" rel="noopener noreferrer"`），
线上 `meta.json` 的四态计数与两级注入计数都自洽。

---

## 10. 边界与未做（不粉饰）

1. **分享图两步本机没跑**：`build_og_images.py` / `apply_og_meta.py` 需要 `pillow` / `fonttools`，
   本机 `python3 -m pip` 不存在，装不了；只在 CI 里跑。这两步只写 `og:image`，不碰出处渲染。
2. **D5（时间线矛盾）仍不可机检**：`findings.json` 的 D5 是 `N/A - no figures_db.json available`，
   所以 `suspect` 这一态目前只可能来自 D4（引文无出处）。这是口径边界，不是本卡遗漏。
3. **覆盖率没有提升**：去重级仍 1147/4016 = 28.6%、被引 >=3 次书名 178/374 = 47.6%（与 Y1 一致，逐字复跑过）。
   本卡只做「注入 + 状态 + 渲染」，继续扩链接源属于后续卡的事。
4. **1919 条 unresolved 引文保持纯文本**：没有链接源就是没有，不猜 URL、不指向搜索页凑数。
5. **suspect 的公开口径是 0**：17 条 D4 命中全部落在隔离人物上，它们不进公开产物；
   源库口径 17 条在 `data/audit/verification_status.json` 里可查。展示成 0 而不是藏起来。
6. **徽章只落在模式卡片与对照表**：credibility_framework.md 第 5 节 P35-E 还提到「统计页」，
   本卡只做了模式级徽章 + `meta.json` 计数，**没有新建统计页**。
7. **没有把 `apply_verification_status.py --check` 接进 CI**：它会新增一道「状态漂移必红」的门，
   本卡不新增门（避免制造新的存量红），工具已具备 `--check`（exit 1）能力，接线留待后续卡决定。
8. **`api/protreptic.db` 没有提交**：重建字节不确定（两次 sha256 不同），§9.3 也把它排除在一致性口径外。
9. **一处 pre-existing lint**：`docs/planning/credibility_framework.md` 第 34 行在**本地新版**
   markdownlint（v0.34）下报 MD056，CI 用的 action 版本不报（Y1 的 CI 是绿的、该文件自 Phase37-X4 未改）。
   本卡不动它（不在本次改动面内），在此如实标注。
