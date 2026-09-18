# Phase31 遗留清理 · QA 终审报告

- 卡片：`t_850cd9e7`（[Phase31-QA] 遗留清理终审）· 审查人：espinosa
- 日期：2026-09-19
- 被审对象：R3 / R4R5 / R8R9 / R6 / R7 / ANALYTICS 六项，以及双仓同步与 CI 状态
- 取证方式：**全部独立实测**，不照抄工人自述。数据侧在发布仓的干净克隆 `/tmp/qa31work/pub`（HEAD=1001606）与
  「发布仓 + 工作区未提交改动」克隆 `/tmp/qa31work/pubfix` 上重跑整条构建链；
  打印侧用 CDP `Page.printToPDF` 自己重新生成 7 份 PDF 并用 pypdf 逐页量坐标；线上侧用 curl + 真实浏览器读 DOM。
- **终审结论：不可发布（FAIL）。** 1 项阻塞（发布仓 HEAD 的 Pages/Quality Gate 构建必失败）+
  1 项部分失败（R6 打印页脚）+ 2 项遗留缺陷（隔离人物在模式摘要层残留、markdown-lint 新增 11 错）。

## 0. 逐项结论

| 项 | 结论 | 一句话 |
| --- | --- | --- |
| R3 domain 语义污染 | PASS | by-figure 与 index 两份产物 `len(domain_zh)>30` 均为 0（修前源数据 1411 条） |
| R4R5 脏名 + 图谱隔离 | PASS（有遗留） | concept_graph 人物 283、图谱/名录/线上深链均无 H-SX-001；但模式摘要层仍残留它 |
| R8R9 硬编码计数 | PASS | `web/src` 中 2868/1058/284 零命中；页脚/hero/API 三处数字与 meta.json 一致 |
| R6 打印页脚 | **FAIL（部分）** | 页脚确实出现在每一页，但坐标落在**正文框内**（不是纸张底部 margin 区），且与正文文字重叠 |
| R7 归档模板副本 | PASS | 7/7 份与源 `templates/*.md` 逐字节一致；归档目录不在发布仓，线上零影响 |
| ANALYTICS 占位符 | PASS | 线上首页/404/深链 HTML 中 `YOUR_INSTANCE` 与 `goatcounter` 均为 0 |
| 发布仓 ahead | PASS | `## main...origin/main`，无 `[ahead N]` |
| CI（Pages / Quality Gate / CI） | **FAIL** | Pages 构建 `[FAIL] by-figure 分片数 284 != 283`；Quality Gate 同一根因；CI 的 markdown-lint 新增 11 错 |
| CI/CD（ci-cd.yml） | PASS | run 35403851190 四个 job 全 success |

## R3 · domain_zh 语义污染（PASS）

修前基线由源数据独立复算（不经工人脚本）：

```console
$ python3  # 读 /opt/data/workspace/Protreptic/data/modes_data.json
源 modes_data.json 去重 2858 条, 原始 len(domain_zh)>30 = 1411
```

发布仓 + 工作区未提交改动（`/tmp/qa31work/pubfix`）重跑构建链后，对**产物**逐条统计：

```console
$ cd /tmp/qa31work/pubfix && python3 tools/build_figures_db.py && python3 tools/export_static_site.py
  domain 字段清洗       2628 条（散文/长值 -> 首个 '/' 片段或 category 短标签），清洗后 len(domain_zh) > 30 的条数 = 0
  [OK] 产物 1350 个文件（索引 1 + figures 1057 + modes 索引 8 + by-figure 283 + meta 1）
  [OK] figures=1057 modes=2858 by-figure=283
export_exit=0

# 独立统计（不用工人的脚本，直接读产物 JSON）
by-figure: shards=283 modes=2848 len(domain_zh)>30 = 0 max_len=30
index-shards: modes=2858 len>30 = 0
```

结论：1411 / 2858（49.4%）-> 0；index 与 by-figure 同源同口径，PASS。

## R4R5 · 脏人名清理 + 隔离名单共享（PASS，但有残留泄漏）

```console
$ cd /tmp/qa31work/pubfix && python3 tools/build_graph_data.py
  模式图: 3288 节点, 6663 边
  概念图: 283 人物, 13261 概念, 13522 边
```

独立读 `web/public/data/graph/concept_graph.json`：

```console
concept_graph keys: ['schema', 'generated_at', 'figure_nodes', 'concept_nodes', 'edges', 'stats']
  figure_nodes: list len=283
concept_graph 含 'H-SX-001': False | 含 '苏咸': False
unified index counts: {"total": 1338, "figures": 283, "scenarios": 1055, "with_modes": 1302}
源数据仍保留 H-SX-001: True     （隔离作用于公开产出层，可回滚）
```

线上侧（真实 HTTP）：

```console
live /minds/H-SX-001/            -> 404
live /data/index.unified.json    -> figures=283
```

`/concepts` 所需的 `concept_graph.json` 人物数 = 283、无 H-SX-001，与 R4R5 验收线一致，PASS。

**残留泄漏（如实记录，非本项验收线）**：隔离只做在 by-figure 分片与名录/图谱/每日三层，
`modes/index-{0..7}.json`（模式摘要索引，/modes 与 /compare 的数据源）**仍含该人物 10 条模式**：

```console
# 本地新构建产物里仍含隔离人物的文件
{"modes/index-1.json": [2, 2], "modes/index-2.json": [2, 2], "modes/index-3.json": [2, 2],
 "modes/index-5.json": [2, 2], "modes/index-6.json": [1, 1], "modes/index-7.json": [1, 1]}
# key -> (H-SX-001 出现次数, 苏咸 出现次数)

# 线上（当前部署版本）
curl -s -o /dev/null -w '%{http_code}' https://ovmobilegroup.github.io/protreptic/data/modes/by-figure/H-SX-001.json
200
{"figure_code":"H-SX-001","figure_name":"苏咸","count":10,"modes":[{"mode_code":"M393","name_zh":"审时度势法", ...
```

即：虚构人物「苏咸」的分片在**线上仍可被直接抓取**（1 个 by-figure 分片 + 6 个模式摘要分片），
`/minds/H-SX-001/` 虽然 404，但 /modes 列表仍会显示这 10 条模式及其署名。

## R8R9 · 硬编码计数（PASS）

```console
grep -rEn '2868' web/src              -> 0 命中
grep -rEn '1058' web/src              -> 0 命中
grep -rEn '284' web/src           -> 0 命中
grep -rEn '2858' web/src          -> 12 命中（注释 + 展示文案，与产物口径一致）
grep -rEn '1055' web/src          -> 2 命中（FiguresView hero 文案，与 unified index 一致）
```

三处展示数字与产物比对（meta.json 取自同一次构建）：

```console
meta.json counts: {"figures": 1057, "figure_shards": 1057, "mode_summaries": 2858,
  "mode_index_shards": 8, "mode_by_figure_shards": 283, "modes_raw": 2868, "modes_deduped": 2858}

App.vue:126        Protreptic · 2858 条思维模式 × 283 位历史人物 · 中英双语      -> 2858 / 283
useSeo.ts:21       2858 条思维模式 × 283 位历史人物                              -> 2858 / 283
FiguresView.vue:15 283 位历史人物的思维方法，与 1055 个现代处境场景              -> 283 / 1055（unified index figures/scenarios）
ApiDocsView.vue:10,12,13  1057 条 / 2858 条 / 283 片                            -> figures.index 1057 / modes 2858 / by-figure 283
```

线上真实 DOM 复核（首页 footer 文本）：

```console
'以史为鉴，知兴替；以人为鉴，明得失。

Protreptic · 2858 条思维模式 × 283 位历史人物 · 中英双语

GitHub
·
MIT License'
/figures 渲染：h1='以人为鉴，明得失'  人物 283 / 场景 1055 / 1302 条含模式   articles=25
/minds/H-WYM-001：h1='王阳明' articles=10
/templates/chibi：h1='⚔️ 赤壁之战复盘模板' .pt-prose=1
```

无空渲染，三处数字与产物一致，PASS。

## R6 · 打印页脚坐标（FAIL，部分）

方法：自建 `web/dist`（`cd web && VITE_DATA_MODE=static npm run build` 通过）-> `vite preview --base=/protreptic/ --port 4210`
-> CDP `Page.printToPDF`（A4，页边距按 `style.css` 的 `@page: 16mm 14mm 18mm 14mm`）逐份生成 7 个模板 PDF
-> pypdf `visitor_text` 逐页算「文字原点距纸张顶」坐标（A4 高 841.9pt，正文框 45.4pt..790.9pt）。

```console
--- r6_beifa.pdf: pages=12 paper=841.92pt content_box=45.4..790.9pt-from-top
    page1:  footer y=736.5pt (259.8mm) IN_CONTENT_BOX 54.4pt above content bottom; nearest body text above gap=72.0pt
    page7:  footer y=736.5pt (259.8mm) IN_CONTENT_BOX 54.4pt above content bottom; nearest body text above gap=11.3pt; same-band non-footer lines=14
    page12: footer y=736.5pt (259.8mm) IN_CONTENT_BOX 54.4pt above content bottom; nearest body text above gap=288.0pt
（其余 6 份同值：chibi 10 页 / changban 12 / jieting 11 / longzhong 10 / yiling 13 / baidi 8，页页 y=736.5pt）
```

逐页细看（同一 y 带上同时出现的正文行）：

```console
=== r6_longzhong.pdf page6 ===
       y= 731.2 x= 126.0  >12 / 单品模型跑通 / 第二阶段门条件：单店 …
FOOTER y= 736.5 x= 69.7  Protreptic ·  |  复盘模板  |  LONGZHONG · https://…/templates/longzhong/

=== r6_baidi.pdf page2 ===
       y= 738.0 x= 104.2  制
FOOTER y= 736.5 x= 69.7  Protreptic · 复盘模板 BAIDI · https://…
```

判定依据与结论：

1. **「页脚出现在每一页」这一条 PASS**：7 份模板、全部 87 页，页脚均在页底同一 y，且不再是「只在第一页顶部」的旧 bug。
2. **「页脚落在纸张底部 margin 区」这一条 FAIL**：实测 y=736.5pt = 距纸张底 105.4pt(37.2mm)，
   比正文框底边（790.9pt）还高 54.4pt —— 它在**正文框内**，不在 18mm 下边距区里。
   原因是 `position: fixed` 的 `bottom: 18mm` 相对**正文框**而非纸张计算：正文框底边离纸边已有 18mm，
   页脚再上移 18mm，实际离纸边 36mm。
3. **与正文重叠**：页脚是 fixed 元素、不占流，正文照常在它所在的 y 带排版。7 份模板中有
   **5 份共 7 页**出现正文行与页脚同一 y 带（chibi p7、baidi p2/p4、changban p4/p8、jieting p5、longzhong p6、yiling p4/p6），
   最近的一例正文基线与页脚基线只差 1.5pt（baidi p2「制」738.0 vs 页脚 736.5），即字形覆盖。
4. **与工人自述不一致**：R6 卡 metadata 写 `footer on all pages at y=745.5pt (in bottom margin, 45.4pt above content bottom, no overlap)`。
   745.5pt 复测不出来 —— 用同一套量法去量**它自己留下的产物** `/tmp/r6/final3_*.pdf` 也是 `y=736.5pt`（7/7 份），
   且 45.4pt 那个数字本身就说明它在正文框内（790.9−736.5≈54，790.9−745.5≈45）；「no overlap」与第 3 点矛盾。

影响面：仅打印/导出 PDF 路径，不影响网页浏览与发布产物完整性；但它**没有达成 R6 的目标**（页脚进纸面页脚区、不压正文），
按「如实发现」原则记为 FAIL，不计入发布阻塞。

## R7 · 归档模板副本（PASS）

```console
docs_site/docs/templates/ 逐字节对比（源 templates/*.md 为中文名，归档为英文 slug）
longzhong.md <- 隆中对复盘.md     src=12040B arc=12040B identical=True  sha=732403f63b88
baidi.md     <- 白帝托孤离职.md   src= 8809B arc= 8809B identical=True  sha=16be7789555b
chibi.md     <- 赤壁之战复盘.md   src=13166B arc=13166B identical=True  sha=8fa8f593dd74
beifa.md     <- 北伐复盘.md       src=14530B arc=14530B identical=True  sha=98957478c6d8
jieting.md   <- 街亭之战复盘.md   src=13998B arc=13998B identical=True  sha=259efe012ba9
yiling.md    <- 夷陵之战复盘.md   src=15851B arc=15851B identical=True  sha=df208c801427
changban.md  <- 长坂坡复盘.md     src=16384B arc=16384B identical=True  sha=609067e39c16
R7 结果: 7 份里逐字节一致 = 7
发布仓是否存在 docs_site: False
```

线上真正被 SPA 读取的模板（`web/public/templates/*.md`，7 份）工作区与发布仓也逐份 SAME。
`mkdocs.pages.yml` 的 `docs_dir: docs`（不是 `docs_site/docs`），归档目录不参与 Pages 构建 -> 线上零影响，PASS。

## ANALYTICS · 占位符（PASS）

```console
$ curl -s https://ovmobilegroup.github.io/protreptic/ -o live_home.html
live home        http=200 bytes=3857    YOUR_INSTANCE=0  goatcounter=0
live 404.html    http=200               YOUR_INSTANCE=0  goatcounter=0
live templates/chibi/  http=200         YOUR_INSTANCE=0  goatcounter=0
```

按 AN 卡选定的 (b) 方案（撤下占位符），线上无 `YOUR_INSTANCE` 残留；`goatcounter` 计数为 0，即当前线上**没有**访问统计
（自托管链路只在本地闭环验证过，缺公网 HTTPS 入口，见 `docs/architecture/gc_setup.md` §5）。这是既定选择，PASS。

## 双仓同步与 CI（FAIL）

```console
$ git -C /opt/data/release/Protreptic-publish status -sb
## main...origin/main                      <- 无 [ahead N]，发布仓与 origin/main 同步
$ git -C /opt/data/release/Protreptic-publish log --oneline -1
1001606 docs(analytics): Phase31-AN 补充自托管链路本地实测记录（tools/gc 端到端计数落库）
```

```console
$ gh run list --repo ovmobilegroup/protreptic --limit 8
failure   Quality Gate                  workflow_run  35403875661   1m35s
failure   Deploy to GitHub Pages        push          35403851223     24s     <- HEAD 1001606
success   Protreptic CI/CD              push          35403851190   ~17m     <- 四 job 全 success
failure   CI                            push          35403851187     18s
success   Quality Gate                  workflow_run  35402271779
success   Deploy to GitHub Pages        push          35401866786   5m21s    <- 线上当前版本 b61b253
```

Pages 失败原文（run 35403851223，与 Quality Gate 的 data-check job 35403875661 同一处）：

```console
  modes/by-figure/         284 片  raw 17.16 MB / gzip 7.30 MB
  meta.json   counts={"figures": 1057, ..., "mode_by_figure_shards": 284, ...}
== 验收断言 ==
  [FAIL] by-figure 分片数 284 != 283
失败 FAILED
##[error]Process completed with exit code 1.
```

CI 失败原文（run 35403851187，markdown-lint job）：

```console
Linting: 215 file(s)
Summary: 11 error(s)
docs/architecture/gc_setup.md:64             MD032/blanks-around-lists
docs/qa/phase31_r7_template_archive_sync.md: 10 处 MD022/MD031/MD032
Failed with exit code: 1
```

即：**Phase31 本轮新增的 2 个文档把 markdown-lint 从旧基线拉红**（不是历史遗留）。ci-cd.yml 本身全绿。

### 阻塞根因（已定位到行）

发布仓 HEAD（1001606）的 `tools/export_static_site.py` 只把常量改小、没有在分组处过滤隔离人物；
过滤代码只存在于**工作区未提交**的版本里（mtime 06:46，晚于 R4R5 的发布仓提交 e411d51@06:34）：

```console
$ diff /opt/data/workspace/Protreptic/tools/export_static_site.py /opt/data/release/Protreptic-publish/tools/export_static_site.py
50,52d49
< sys.path.insert(0, str(Path(__file__).resolve().parent))
< from _quarantine import is_quarantined  # noqa: E402
433d429
<     quarantined_shards = 0
435,437d430
<         if is_quarantined(fc):
<             quarantined_shards += 1
<             continue
```

工作区未提交改动清单（与发布仓逐一比对）：

```console
DIFFERS  tools/export_static_site.py     <- 阻塞修复本体
DIFFERS  tools/pages_preflight.py        <- 与 build_daily_index 配套的口径改动
DIFFERS  tools/build_daily_index.py
DIFFERS  api/protreptic.db  docs/architecture/static_data_manifest.json  docs/architecture/web_p0_routes.json
SAME     data/modes_data.json  data/figure_names.json  data/figures/H-HuoQuBing-001.json
SAME     tools/_quarantine.py  tools/build_graph_data.py  tools/build_unified_index.py  tools/ci_data_check.py  tools/prerender_routes.py
```

把这三个文件覆盖到发布仓克隆后重跑，构建链全绿（证明修复确实有效、只差提交）：

```console
$ cd /tmp/qa31work/pubfix && python3 tools/build_figures_db.py && python3 tools/export_static_site.py
  [OK] figures=1057 modes=2858 by-figure=283        export_exit=0
$ python3 tools/build_daily_index.py
[daily] 模式 2848 条 / 人物 283 位 / 分片 283 个
$ python3 tools/pages_preflight.py --stage data
[OK] stage=data：全部断言通过                     preflight_exit=0
```

（对照：干净克隆 `/tmp/qa31work/pub` 上跑同一个 export 必失败 `[FAIL] by-figure 分片数 284 != 283`。）

## 终审结论

**不可发布。** 当前发布仓 HEAD（1001606）的 Pages 构建与 Quality Gate `data-check` 100% 失败，
线上仍停留在上一版成功部署 b61b253（其 `data/meta.json` 仍是 `mode_by_figure_shards:284`，
且 `/data/modes/by-figure/H-SX-001.json` 在线上 200 可取），本轮 R4R5 的隔离只做了一半。

放行条件（全部满足才可判「可发布」）：

1. 把工作区未提交的 `tools/export_static_site.py`（by-figure 分组加 `is_quarantined` 跳过）
   与其配套的 `tools/pages_preflight.py`、`tools/build_daily_index.py` 提交并 `git push origin main` 到发布仓，
   让 pages.yml 转绿（本地已验证可通过，见上）。
2. 顺手收口 markdown-lint：本阶段新增的 `docs/architecture/gc_setup.md`、
   `docs/qa/phase31_r7_template_archive_sync.md` 补空行（MD022/MD031/MD032）。
3. 重新部署后复测线上 `data/meta.json` 的 `mode_by_figure_shards` 应为 283，
   且 `/data/modes/by-figure/H-SX-001.json` 应变 404。

遗留（不阻塞发布，但应记入 Phase32）：

- R6 打印页脚在正文框内且与正文重叠（见 R6 节），需要 `bottom` 用负值或用 `@page` 页脚盒子重新定位。
- 隔离人物在 `modes/index-*.json` 模式摘要层残留 10 条（/modes、/compare 仍可见「苏咸」署名），
  隔离的适用范围应从「分片/名录/图谱」扩展到「模式摘要层」，或在前端按 `figure_code` 二次过滤。
- 线上目前完全没有访问统计（选项 b 的代价），如需真实数据仍需公网 HTTPS 入口。
