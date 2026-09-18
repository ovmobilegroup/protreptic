# Phase31 收官报告（CLOSE）——交付清单 · 实测证据 · 未达标项 · 后续建议

- 卡片：`t_8e73c660` [Phase31-CLOSE]（assignee: pigafetta）
- 上游：`t_850cd9e7` [Phase31-QA] 终审（espinosa）——结论「不可发布（FAIL）」，报告 `docs/qa/phase31_acceptance.md`（发布仓 commit 7866250）
- 阻塞收口：`t_b24ccd32` [Phase31-FIX]（san-martin）——发布仓 commit 8d15f1a，本卡完成前已落地（见 3.4 节）
- 项目仓：`/opt/data/workspace/Protreptic`（dev，分支 `master`；origin 只有 `main`，master 无上游）
- 发布仓：`/opt/data/release/Protreptic-publish`（origin `main`，**线上唯一来源**）
- 线上：https://ovmobilegroup.github.io/protreptic
- 取证原则：本报告所有数字都来自本卡现场执行的命令（第 6 节可逐条复跑）；凡引用终审结论处均标注「引自 QA 报告」，不做推断式断言。

---

## 0. 结论摘要

**Phase31 可发布。** QA 报告列出的三条放行条件已全部满足并现场复测：发布仓 `8d15f1a` 的
CI / Deploy to GitHub Pages / Quality Gate 三条工作流全部 success；线上 `data/meta.json` 的
`mode_by_figure_shards` 已从 284 变为 **283**，`/data/modes/by-figure/H-SX-001.json` 与
`/minds/H-SX-001/` 均已 **404**。

六项遗留清理的收官判定（详见第 2 节）：**R3 PASS、R4R5 PASS（有残留）、R6 FAIL（部分，不阻塞发布）、
R7 PASS、R8R9 PASS（有同类残留）、ANALYTICS PASS**。

QA 终审之所以判「不可发布」，唯一阻塞项是发布仓缺 by-figure 隔离过滤（`EXPECT_BY_FIGURE 283`
改了、`is_quarantined` 跳过没同步），该缺陷已由 `8d15f1a` 收口；本卡另发现 4 类未达标/残留项
（第 4 节），均不影响发布，建议排入 Phase32。

---

## 1. Phase31 卡片与交付物清单

| 卡片 | 负责人 | 交付物（绝对路径前缀 `/opt/data/workspace/Protreptic/`） | 现场验证 |
| --- | --- | --- | --- |
| `t_7017c954` R3 | barbosa | `tools/export_static_site.py`（26595 B，domain 清洗） | 产物 `len(domain_zh)>30` = 0（本卡复测，2.1 节） |
| `t_34a97fec` R4R5 | san-martin | `tools/_quarantine.py`（5241 B）、`data/figure_names.json`、`tools/build_graph_data.py`（13143 B）、`tools/build_unified_index.py`（6715 B） | `concept_graph` 人物 283、无 H-SX-001（本卡复测，2.2 节） |
| `t_718783a9` R6 | elcano | `web/src/style.css`（15160 B）打印页脚 | **FAIL**：页脚在正文框内且与正文重叠（4.3 节） |
| `t_a55bd669` R7 | pigafetta | `docs_site/docs/templates/*.md`（7 份，8809 至 16384 B）、`docs/qa/phase31_r7_template_archive_sync.md`（8158 B） | 7/7 与源 `templates/*.md` 逐字节一致（引自 QA 报告） |
| `t_7b9bb355` R8R9 | elcano | `web/src/App.vue`（6852 B）、`web/src/composables/useSeo.ts`、`web/src/views/FiguresView.vue`、`web/src/views/ApiDocsView.vue` | `web/src` 内 2868/1058/284 零命中（引自 QA 报告）；同类残留见 4.1 节 |
| `t_7f963543` AN | acurio | `docs/architecture/gc_setup.md`（5763 B）、`web/index.html`（撤下占位符） | 线上首页/404/深链 `YOUR_INSTANCE`=0（本卡复测，3.2 节） |
| `t_8dcd07eb` SK | bustamante | 技能 `protreptic-web-frontend` 方法论沉淀 | 各 profile 独立副本，见 4.6 节 |
| `t_850cd9e7` QA | espinosa | `docs/qa/phase31_acceptance.md`（17036 B，两仓同文） | 发布仓 7866250，远端 raw 可回读（引自 QA 报告） |
| `t_b24ccd32` FIX | san-martin | `tools/export_static_site.py`、`tools/pages_preflight.py`（9093 B）、`tools/build_daily_index.py`（10263 B） | 发布仓 8d15f1a；本卡在干净克隆上复跑全链 exit=0（3.1 节） |
| `t_8e73c660` CLOSE | pigafetta | 本报告 `docs/phase31_final_report.md` | 见第 3、7 节 |

---

## 2. R3 到 R9 逐项结论

| 项 | 卡片 | 结论 | 一句话 |
| --- | --- | --- | --- |
| R3 domain 语义污染 | `t_7017c954` | PASS | by-figure 与 index 两份产物 `len(domain_zh)>30` 均为 0（修前源数据 1411 条） |
| R4 脏人物名 | `t_34a97fec` | PASS | 公开产出层无隔离人物；名录/图谱/每日三层一致 |
| R5 隔离名单共享 | `t_34a97fec` | PASS（有残留） | 图谱与 by-figure 已隔离；`modes/index-*.json` 仍残留 10 条（4.2 节） |
| R6 打印页脚 | `t_718783a9` | **FAIL（部分）** | 页页有页脚 OK，但坐标在正文框内、与正文重叠 |
| R7 归档模板副本 | `t_a55bd669` | PASS | 7/7 逐字节一致，且不在发布仓，线上零影响 |
| R8 硬编码计数（前端） | `t_7b9bb355` | PASS | `web/src` 三处计数全部改为产物派生 |
| R9 硬编码计数（口径一致） | `t_7b9bb355` | PASS | 页脚/hero/API 三处数字与 `meta.json`、线上一致；同类残留见 4.1 节 |
| ANALYTICS 占位符 | `t_7f963543` | PASS | 线上无 `YOUR_INSTANCE`；无第三方脚本 |

### 2.1 R3 证据（本卡复测）

在发布仓 `8d15f1a` 的干净克隆 `/tmp/pt31close_1789774091/pub` 上重跑构建链后，直接读产物统计：

```
by-figure domain_zh>30: 0
by-figure 分片数: 283
meta.counts: {"figures":1057, "mode_summaries":2858, "mode_by_figure_shards":283,
              "modes_raw":2868, "modes_deduped":2858, "modes_empty_mode_code_dropped":10}
```

### 2.2 R4R5 证据（本卡复测）

```
concept_graph 人物数: 283 概念数: 13261 边数: 13522
by-figure/H-SX-001.json 存在: False
unified counts: {"total":1338, "figures":283, "scenarios":1055, "with_modes":1302}
线上 /data/modes/by-figure/H-SX-001.json -> 404    线上 /minds/H-SX-001/ -> 404
```

### 2.3 R6 证据（引自 QA 报告，本卡未复测）

QA 用自建 `web/dist` + CDP `Page.printToPDF` + `pypdf` 逐页量坐标：7 份模板全部 87 页页脚都在
`y=736.5pt`（距纸底 37.2mm），比正文框底边（790.9pt）高 54.4pt，即落在**正文框内**；5 份模板共
7 页出现正文行与页脚同 y 带，最近一例字形覆盖（baidi p2 正文 738.0pt 对页脚 736.5pt）。
根因：`position: fixed; bottom: 18mm` 相对正文框而非纸张计算。本卡未重复该实验，如实沿用 FAIL。

### 2.4 R7 证据（引自 QA 报告）

`docs_site/docs/templates/` 7 份与源 `templates/*.md` 逐字节一致（cmp identical=True），
发布仓无 `docs_site` 目录（本卡复核 ls 报路径不存在），`mkdocs.pages.yml` 的 `docs_dir: docs`，
故归档目录不参与 Pages 构建。

### 2.5 R8R9 证据（引自 QA 报告 + 本卡线上复核）

```
web/src 内 2868 / 1058 / 284 命中数: 0 / 0 / 0
线上首页 footer 文本: Protreptic · 2858 条思维模式 × 283 位历史人物 · 中英双语
```

### 2.6 ANALYTICS 证据（本卡复测）

```
live home  http=200 bytes=3857  YOUR_INSTANCE=0  goatcounter=0
```

---

## 3. 本卡现场实测证据

### 3.1 独立复跑：发布仓 8d15f1a 干净克隆，数据链全绿

```
git clone --depth 1 file:///opt/data/release/Protreptic-publish /tmp/pt31close_1789774091/pub
cd /tmp/pt31close_1789774091/pub
python3 tools/build_figures_db.py      -> exit=0  figures 表重建完成: 1057 行
python3 tools/export_static_site.py    -> exit=0  [OK] figures=1057 modes=2858 by-figure=283
python3 tools/build_daily_index.py     -> exit=0  [daily] 模式 2848 条 / 人物 283 位 / 分片 283 个
python3 tools/build_search_index.py    -> exit=0  16 个分片 + meta.json
python3 tools/build_graph_data.py      -> exit=0  模式图 3288 节点/6663 边; 概念图 283 人物; gzip 541.5 KB
python3 tools/build_unified_index.py   -> exit=0  total=1338 figures=283 scenarios=1055 with_modes=1302
python3 tools/pages_preflight.py --stage data -> exit=0  [OK] stage=data：全部断言通过
```

对照组（QA 已实测，引自 QA 报告）：同一个 export 在改造前的发布仓 HEAD `1001606` 上必失败
`[FAIL] by-figure 分片数 284 != 283`。两相对照可确认 `8d15f1a` 的修复确实生效。

### 3.2 线上抽检（curl，部署 8d15f1a 之后）

```
$ curl -s https://ovmobilegroup.github.io/protreptic/data/meta.json
  generated_at: 2026-09-18T23:25:37+00:00   mode_by_figure_shards: 283   modes_deduped: 2858
$ curl -s -o /dev/null -w '%{http_code}' <URL>
  /data/modes/by-figure/H-SX-001.json   404      <- 修复前为 200
  /data/modes/by-figure/H-WYM-001.json  200
  /minds/H-SX-001/                      404
  /minds/H-WYM-001/                     200
  /data/index.unified.json              200      counts: figures=283 scenarios=1055
  /sw.js                                200     11433 B（真 SW，非 SPA 兜底）
```

QA 报告列出的第 3 条放行条件（线上 `mode_by_figure_shards`=283 且 H-SX-001 分片转 404）**已满足**。

### 3.3 CI 工作流（提交 8d15f1a）

| 工作流 | run id | 结论 |
| --- | --- | --- |
| CI（markdown-lint） | 35405621977 | success（修复前同工作流 35405269843 = failure，11 错） |
| Deploy to GitHub Pages | 35405621983 | success（修复前 35405269795 = failure，284 != 283） |
| Quality Gate | 35405904303 | success（修复前 35405293940 = failure，同根因） |
| Protreptic CI/CD | 35405622010 | 本卡取数时刻 in_progress（前两次提交均为 success） |

### 3.4 阻塞项收口时间线

```
07:20  发布仓 HEAD = 7866250，Pages/Quality Gate 红（by-figure 284 != 283）
07:23  本卡启动；发布仓工作区出现 5 个未提交改动（san-martin 的 FIX 卡在改）
07:25  发布仓 8d15f1a 提交并 push origin main（ls-remote 回读一致）
07:25  CI 成功 / Pages 启动
07:27  Pages success
07:35  Quality Gate success
07:4x  本卡线上复测：283 / 404 / 404 全部符合放行条件
```

### 3.5 两仓状态（本卡收尾时刻）

```
$ git -C /opt/data/release/Protreptic-publish status -sb
## main...origin/main            <- 无 [ahead N]
$ git -C /opt/data/release/Protreptic-publish rev-parse HEAD   -> 8d15f1a
$ git ls-remote origin main                                    -> 8d15f1a（一致）
$ git ls-remote origin                                         -> 只有 refs/heads/main（无 master）
```

工作区仓库 master 在 origin 上没有对应分支，因此只能提交到本地、无法 push；其未提交状态见 4.5 节。

---

## 4. 未做 / 未达标项

### 4.1 R8R9 同类残留：营销计数外溢到 web/src 之外（本卡新发现，未修）

web/src 已清零，但同一句话在三个「非 web/src」位置仍是旧值（正确口径见 `App.vue`：2858 条 × 283 位）：

```
web/index.html:8    content="2868 条思维模式 × 284 位历史人物：每条都有出处、操作步骤与现代应用。"
web/index.html:15   og:description = "2868 条思维模式 × 284 位历史人物 · 中英双语"
mkdocs.pages.yml:19 site_description: 2868 条历史人物思维模式 × 284 位人物 · 中英双语
docs/index.md:3     2868 条思维模式 · 284 位历史人物 · 中英双语（该文件只在发布仓存在）
docs/index.md:6     共 2868 条，每条都有定义、操作步骤、出处、原话、史实案例与现代应用。
```

线上确认仍然可见（部署 8d15f1a 之后）：

```
$ curl -s https://ovmobilegroup.github.io/protreptic/ | grep 2868
  <meta name="description" content="2868 条思维模式 × 284 位历史人物：">
  <meta property="og:description" content="2868 条思维模式 × 284 位历史人物 · 中英双语">
$ curl -s https://ovmobilegroup.github.io/protreptic/docs/ | grep -o '2868 条[^<"]*'
  2868 条历史人物思维模式 × 284 位人物 · 中英双语
  2868 条思维模式 · 284 位历史人物 · 中英双语
```

**未修的原因**（不是没看到）：2868 是 `meta.json` 里的 `modes_raw`（去重前 2868 / 去重后 2858），
`docs/index.md:66`「`data/modes_data.json`（2868 条模式）」按原始文件口径讲并不算错；只有营销文案口径
必须用 2858 × 283。哪些位置该改、`modes_raw` 口径要不要公开，属于产品口径决策，收官卡不宜单方面拍板
（第 5 节已列为 Phase32 优先小卡，改法与位置已给全）。

### 4.2 R4R5 残留：隔离人物的模式摘要层泄漏（未修）

`8d15f1a` 之后仍可复现（本卡在干净克隆上直接读产物）：

```
modes/index-*.json 残留: {'index-1.json': [2,2], 'index-2.json': [2,2], 'index-3.json': [2,2],
                          'index-5.json': [2,2], 'index-6.json': [1,1], 'index-7.json': [1,1]}
  key -> (H-SX-001 出现次数, 苏咸 出现次数)，合计 10 条
by-figure/H-SX-001.json 存在: False    <- 分片层已隔离
```

即虚构人物「苏咸」的 10 条模式仍在 `/modes`、`/compare` 的数据源里可见署名；`/minds/H-SX-001/` 已 404、
by-figure 分片已不再生成。隔离的适用范围应从「分片 / 名录 / 图谱 / 每日」继续扩展到「模式摘要层」，
或在前端按 `figure_code` 二次过滤。

### 4.3 R6 打印页脚未达标（未修，见 2.3 节）

页脚确实出现在每一页，但仍位于正文框内（`y=736.5pt`，距纸底 37.2mm）且与 7 页正文重叠。
FIX 卡已明确把该项划出范围（需改 `web/src/style.css` 的定位方式：`bottom` 负值或 `@page` 页脚盒子），
本卡不越界处理。

### 4.4 线上仍无访问统计

AN 卡选定的方案 b 是「撤下占位符」，代价是线上 goatcounter 计数为 0：自托管链路只在本地闭环验证过，
缺公网 HTTPS 入口（`docs/architecture/gc_setup.md` 第 5 节）。这是既定选择，不是缺陷，
但要知道现在线上没有任何访问数据。

### 4.5 仓库卫生：dev 仓与 publish 仓不在同一提交状态

```
$ cd /opt/data/workspace/Protreptic && git status -sb
## master
 M api/protreptic.db            (38.4 MB 二进制)
 M data/figure_names.json  M data/figures/H-HuoQuBing-001.json  M data/modes_data.json
 M docs/architecture/gc_setup.md  M docs/architecture/static_data_manifest.json
 M docs/architecture/web_p0_routes.json
 M tools/build_daily_index.py  M tools/build_graph_data.py  M tools/build_unified_index.py
 M tools/ci_data_check.py  M tools/export_static_site.py  M tools/figure_library.py
 M tools/pages_preflight.py  M tools/prerender_routes.py  M tools/thinking_mode_selector.py
?? docs/qa/phase31_r7_template_archive_sync.md   ?? tools/_quarantine.py   ?? tools/fix_dirty_figure_names.py
```

这 16 个改动正是本轮 R3 / R4R5 / FIX 的修复本体（已随发布仓上线），却从未提交进 dev 仓：
**Phase31 阻塞项的根因就是这个「改在工作区、没进仓库」的状态**。结构上也有漂移：

```
docs/index.md      workspace 无 / publish 有（2794 B）
docs/_config.yml   workspace 无 / publish 有（223 B）
```

建议 Phase32 做一次 dev 仓对齐提交（含 `tools/_quarantine.py` 等未跟踪文件），或明确「dev 仓只作草稿区」的约定。

### 4.6 技能按 profile 分叉（未修）

`protreptic-web-frontend` 在 9 个 profile 下各有一份独立副本
（`/opt/data/profiles/<name>/skills/protreptic/protreptic-web-frontend/`）。任何 worker 写进自己副本的教训，
其他 profile 看不到，Phase31 的坑很可能因此重复踩。本卡只能更新 pigafetta 自己那份（见第 7 节）。

---

## 5. 后续建议（Phase32 排卡）

1. **P0 打印页脚重做**：`web/src/style.css` 用 `@page` 页脚盒子或负 `bottom`；验收必须是
   「CDP `Page.printToPDF` 自建 7 份 PDF + `pypdf` 逐页量坐标」并保存产物，不接受只报一个数字。
2. **P1 隔离口径扩展到模式摘要层**：`modes/index-*.json` 10 条残留（4.2 节）；
   顺带决定 `/data/modes/by-figure/H-SX-001.json` 这类旧 URL 是否做 404 兜底。
3. **P1 营销计数清零 + 口径决策**（4.1 节）：改 `web/index.html:8,15`、`mkdocs.pages.yml:19`、
   `docs/index.md:3,6` 为 2858 × 283；`docs/index.md:66` 的 `modes_raw`（2868）由 owner 决定是否改写。
4. **P2 访问统计公网入口**：给自托管 GoatCounter 一个 HTTPS 入口后再启用，否则保持现状（无数据）。
5. **P2 仓库卫生**：dev 仓对齐提交（4.5 节）；把 `docs/index.md` 等发布仓独有文件补进 dev 仓，避免下次误判。
6. **P2 技能统一**：考虑把 `protreptic-web-frontend` 做成单一来源（例如仓库 `skills/` 目录 + 各 profile 软链），
   否则每轮教训都要按 profile 重抄一遍。

---

## 6. 复跑命令（本报告所有数字均可复现）

```
# 1) 发布仓状态与 push 证据
git -C /opt/data/release/Protreptic-publish status -sb
git -C /opt/data/release/Protreptic-publish rev-parse HEAD
git ls-remote origin main

# 2) 干净克隆复跑数据链（不要在工作区跑：那里有未提交改动，会掩盖缺陷）
W=/tmp/pt31close_x; mkdir -p $W
git clone --depth 1 file:///opt/data/release/Protreptic-publish $W/pub
cd $W/pub
python3 tools/build_figures_db.py && python3 tools/export_static_site.py && python3 tools/build_daily_index.py && python3 tools/build_search_index.py && python3 tools/build_graph_data.py && python3 tools/build_unified_index.py && python3 tools/pages_preflight.py --stage data

# 3) 线上抽检
B=https://ovmobilegroup.github.io/protreptic
curl -s $B/data/meta.json | tr ',' '\n' | grep -E 'generated_at|mode_by_figure_shards'
curl -s -o /dev/null -w '%{http_code}\n' $B/data/modes/by-figure/H-SX-001.json   # 期望 404
curl -s -o /dev/null -w '%{http_code}\n' $B/minds/H-SX-001/                      # 期望 404
curl -s $B/ | grep 2868                                                          # 4.1 节残留仍在

# 4) CI 目录（gh 需指定 HOME/GH_CONFIG_DIR）
export HOME=/opt/data/home GH_CONFIG_DIR=/opt/data/home/.config/gh
/opt/data/home/.local/bin/gh run list --repo ovmobilegroup/protreptic --limit 6

# 5) markdown-lint 自检（CI 同版本）
npx --yes markdownlint-cli2@0.11.0 "docs/phase31_final_report.md" --config .markdownlint.json
```

---

## 7. 本卡变更与技能沉淀

1. 新增本报告：`/opt/data/workspace/Protreptic/docs/phase31_final_report.md`
   与 `/opt/data/release/Protreptic-publish/docs/phase31_final_report.md`（两仓同文）。
2. 技能 `protreptic-web-frontend`（pigafetta 副本）新增 6 条 Phase31 教训：
   过滤器与计数常量必须同一次提交、验证必须留下可复测的产物、`position:fixed` 页脚坐标相对正文框、
   硬编码计数会藏在 `web/index.html` / `mkdocs.pages.yml` / 文档站首页、新增文档必须本地跑 markdown-lint、
   以及本技能按 profile 分叉的风险。
3. 本卡没有动任何代码或数据：所有新发现（4.1、4.2、4.5、4.6 节）都只被记录，未被修改。
