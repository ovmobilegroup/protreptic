# Phase30 P1 QA 报告（图谱 / 对比 / 每日 / 导出）

- 卡：`t_a8b1f78d`（[Phase30-B6] QA 审查：P1）
- 审查人：Gonzalo Gómez de Espinosa（QA worker）
- 日期：2026-09-18
- 被审对象：B2（/graph 图谱 + 相似模式 + /concepts）、B3（/compare 跨人物对比）、B4（/daily 每日一模式）、B5（模板导出 PDF/Markdown + 打印样式）
- 代码基线：workspace `d6b0e8b5`（B5）+ 本卡修复；发布基线 `86453ba`
- 线上：https://ovmobilegroup.github.io/protreptic

## 0. 方法与可复现性

| 手段 | 说明 |
| --- | --- |
| 独立数据复核 | 直接解析 `web/public/data/**` 与 `api/protreptic.db`（sqlite），**不 import 上游前端代码**，重算节点/边/概念/每日选取，再与浏览器 DOM 数字比对 |
| 真实浏览器实测 | `vite preview`（本地 4210，`VITE_DATA_MODE=static` 构建产物）+ CDP `Emulation.setEmulatedMedia('print')` 打印媒体实测 |
| 线上复核 | 直连 GitHub Pages 抓 HTTP + 浏览器 DOM（线上 bundle = `index-D1DYwfIq.js`，与 B5 提交同版） |
| 构建门 | `cd web && VITE_DATA_MODE=static npm run build` → `vue-tsc` 0 error，vite 137 modules（本卡修复后重跑通过） |

复现命令见文末 §6。

## 1. 逐项结论

| # | 检查项 | 结论 | 关键证据 |
| --- | --- | --- | --- |
| 1 | 图谱节点边数与渲染 | **PASS**（缺陷 D1 已修） | 三视图全部与预计算分片逐边对得上，见 §2.1 |
| 2 | 相似推荐命中 | **PASS** | H-WYM-001：6 个区块 / 11 条邻居，与 `similar_modes.json` 完全一致，见 §2.2 |
| 3 | 概念页跨人物 | **PASS**（缺陷 D2/D3 数据侧待跟进） | 13,288 概念 / 218 跨人物 / 284 人物 / 13,552 边，独立重算一致；`长期主义` 8 人逐条模式级证据，见 §2.3 |
| 4 | 对比视图 URL 可分享 | **PASS** | `?items=` 4 项 → 3 表 51 行；共同概念 `万物一体·3`、`经世致用·2` 与独立重算一致；刷新保持选择，见 §2.4 |
| 5 | 每日模式确定性 | **PASS** | 独立公式重算 = `M-FYJ-009`（index 778）；首页模块 3 次加载同一结果；`?date=` 三个历史日期与重算逐一对齐，见 §2.5 |
| 6 | 模板下载文件完整性 | **PASS** | 7/7 `.md` 的 sha256 与仓库源文件 `./templates/*.md` **完全相同**；页面渲染 10 表 / 13 列表，见 §2.6 |
| 7 | 打印样式实测 | **PASS**（观察 D4） | 打印媒体下：白底黑字、导航/页脚/按钮全部不可见、表格 1px 实框、表头跨页重复、正文 opacity=1，见 §2.7 |

**无一空渲染、无一数据造假**：所有 DOM 数字均由脚本从页面读出并与数据文件独立重算比对，未采信上游卡片的自述。

## 2. 逐项证据

### 2.1 /graph 图谱（人物-模式-概念 / 模式关联 / 全局网络）

- 人物-模式-概念（默认 H-WYM-001）：DOM `23` 节点 / `23` 边。
  - 结构 = 1 人物 + 10 模式（分片 `modes/by-figure/H-WYM-001.json` 的 M381–M390）+ 12 概念（按概念全域出现次数取 Top-12，`conceptLimit=12`）。
  - **逐边核对**：10 条 人物→模式；13 条 模式→概念全部命中该模式 `key_concepts`（M381→良知/致良知/心之本体/去人欲/存天理；M384→知行合一；M385→克己复礼；M388→因材施教/循序渐进；M390→权变/因地制宜 …）。无一条凭空边，无一条漏边（按同口径重算 23 条）。
- 模式关联（M-MON-008）：DOM `23` 节点 / `22` 边，与 `mode_edges.json` 邻接表**集合完全相等**（`missing=[] extra=[]`）。
- 模式关联（M-AE-008）：DOM 8 节点 / 7 边，其中 **1 条虚线**（`stroke-dasharray="4 3"`）= `similar_modes.json` 里 M-AE-008 的唯一共现邻居 M-DSF-007（共享概念「行动裁决」）；6 条实线 = related_modes 邻居。虚线/实线语义与代码注释一致。
- 全局模式网络：DOM `60` 节点 / `36` 边；把这 60 个节点放回 `mode_edges.json` 求诱导子图 = `36` 条边，**与 DOM 边数完全相等**。
- 线上同一页面同样为 23/23（人物视图），说明结构与线上一致。

### 2.2 相似模式推荐（/minds/H-WYM-001）

- 期望（`similar_modes.json`）：6 条模式有邻居，共 11 条邻居 —— `M382→M384`、`M384→M382`、`M385→M-CC-006`、`M386→M-LZ-008/M-ZZ-003/M-ZZ-004`、`M388→M-CC-004/M-CC-021`、`M390→M-LZX-007/M-SYX-008/M-ZY-002`。
- DOM：10 张模式卡 → 6 个区块有邻居、共 **11 个邻居入口**（可点击跳人物档案），其余 4 个区块显示「该模式没有预计算的相似模式」明确空态文案（不是空渲染）。
- 邻居的编号 / 名称 / 所属人物 / 共享概念（如 `M384 事上磨练法 · 王阳明 · 知行合一`）与数据逐条一致。

### 2.3 /concepts 概念索引（跨人物）

- 统计条：概念 13,288 / 跨人物（≥2 人）218 / 人物 284 / 人物-概念边 13,552 —— 独立重算 `concept_graph.json`（figure_nodes 284、concept_nodes 13,288、edges 13,552；≥2 人概念 218、单人最多 8 人）全部一致，无四舍五入式谎报。
- 详情（点击「查看跨人物用法」）：URL 同步 `?c=长期主义`；面板列出 **8 位人物**（胡适 / 李光耀 / 涩泽荣一 / 赫歇尔 / 秦九韶 / 丁肇中 / 伏打 / 周恩来）与人物级 `10 条模式` 及**模式级证据**（如 胡适 `M-HS-009 功不唐捐长期法` + 定义原文），与 `concept_graph` 中该概念的 8 个人物集合一致；非「只有一个名字的壳」。
- 数据侧问题见 D2 / D3。

### 2.4 /compare 跨人物对比与 URL 分享

- URL：`/compare/?items=H-WYM-001,H-HS-001,H-ZZ-001,H-LZ-001` → 3 张表 / 51 行 / 4 个已选 chip；刷新后选择保持（URL 即状态）。
- 共同概念区：`万物一体 · 3`、`经世致用 · 2`；把四项的 `key_concepts` 独立求交 = **恰好这 2 个**（万物一体：王阳明/张载/李贽；经世致用：张载/李贽），数量与排序均一致。
- 无法解析的编号（`H-MO-001`）显示显式提示「无法解析（编号不存在或为场景条目）」，其余项照常渲染（优雅降级，不是整页空白）。

### 2.5 /daily 每日一模式确定性

- 独立公式 `i = floor((utc_ms + 480*60000)/86400000) % total`（total=2848，Asia/Shanghai）重算：`2026-09-18 → index 778 → M-FYJ-009 时务人士监督法 / 福泽谕吉`。
- 首页（`/figures`）「今日一模式」模块：连续 3 次加载 = `2026-09-18 / M-FYJ-009`，逐字相同。
- `/daily`：显示 `2026-09-18 周五 / M-FYJ-009 / 时务人士监督法 / Men-of-the-Hour Monitor Method / 政治治理 / 人物 · 福泽谕吉` + 3 步与出处，与重算一致。
- `?date=` 三个历史日期：`2026-01-01→M-BEN-009`、`2025-12-25→M-BEN-002`、`2030-06-01→M-NOBEL-003`，与独立重算逐个相同；`?date=not-a-date` 回落今天（M-FYJ-009），不报错。
- 线上 `/daily` 同日同样为 `M-FYJ-009 / 时务人士监督法`（线上数据由 CI 重新生成，口径一致）。

### 2.6 模板下载与 Markdown 完整性

- 7 个模板：`baidi / beifa / changban / chibi / jieting / longzhong / yiling`，页面渲染 10 张表、13 个列表项、标题层级完整（H1–H3），按钮 `打印 / 导出 PDF`、`下载 Markdown · 11.8 KB` 均在。
- 下载字节流 = 服务端 `templates/{id}.md` 原文，sha256 与仓库源 `./templates/*.md`（中文文件名版本）**7/7 完全相同**；线上 `https://ovmobilegroup.github.io/protreptic/templates/longzhong.md` HTTP 200 / 12,033 B 与源文件同尺寸。
- 注意：`docs_site/docs/templates/*.md` 是**另一份过期副本**，与仓库源不一致（见 D5），不属于下载链路。

### 2.7 打印样式实测（CDP 打印媒体）

对 `/templates/longzhong/` 施加 `Emulation.setEmulatedMedia('print')` 后读计算样式：

| 断言 | 屏幕 | 打印 |
| --- | --- | --- |
| `body` 背景 | `rgb(4,6,12)` + 双径向光晕 | `rgb(255,255,255)`，`background-image: none` |
| 正文/标题颜色 | `rgb(243,236,224)` | `rgb(17,17,17)`（`.pt-prose` `rgba(17,17,17,.85)`，opacity 1） |
| `header` / `nav` | 可见 | 不可见（`getClientRects().length = 0`，可见导航链接 0 个） |
| 可见按钮 | 含「打印」「下载」等 | **0 个**（`.pt-print-hide` 5 处 `display:none`） |
| 表格单元格 | 无框 | `1px solid rgb(136,136,136)` |
| 表头 | — | `thead { display: table-header-group }`（跨页重复） |
| `.pt-print-only` | `display:none` | `display:block`，含原文链接 `…/templates/longzhong/` |

即 B5 声称的「隐藏导航/页脚/工具栏、白底黑字、表格保留边框、表头跨页重复」在真实打印媒体下**全部成立**。唯一观察：该「纸上页脚」URL 实际渲染在 article 面板内、首屏 y≈188（见 D4）。

## 3. 缺陷与处置

### D1（高，已修）模式名称以历史三元组形式渲染 —— 574/2858 条（20.1%）

- **现象**：`/graph` 模式下拉与节点标签、`/modes` 卡片、`/compare` 名称出现
  `M-MF-004 · 考据鉴定法,Connoisseur Authentication Method,鉴别方法/证据链`、
  `剪纸即兴法,Papercut-Improvisation Method,创作发生方法论/…` 这类逗号串联文本。
- **根因（三层）**：源 `data/modes_data.json` 有 574 条把 `name_zh`/`name_en` 写成 `[中文, English, 分类]` 三元组（`api/protreptic.db` 的 `thinking_modes` 同字段是干净标量）；`tools/export_static_site.py` 按 `SUMMARY_FIELDS` 原样透传；`web/src/api/modeIndex.ts` 用 `String(m.name_zh)` 归一，数组被 JS 用逗号 `toString()`，并经 `modeIndex` 扩散到所有消费方（`/modes`、`/graph`、`/compare`、搜索）。`api/compareData.ts` 的 `text()` 则用空格拼接，同源。
- **修复（本卡）**：
  1. `web/src/api/modeIndex.ts`：新增 `pickZh / pickEn`（中文取首个含汉字项、英文取首个不含汉字项并回落），`load()` 改用它；
  2. `web/src/api/compareData.ts`：`toCompareMode()` 的 `name/nameEn` 改用同口径 `firstOf/firstName`；
  3. `tools/export_static_site.py`：新增 `normalize_name_fields()`（`pick_name()` 同口径），在 `load_modes()` 后统一折平 —— CI 下次构建起**数据层**也输出标量（Pages 工作流会重跑 `export_static_site.py`）。
- **验证**：修复后实测 `/graph` 模式下拉 574 → **0** 条含逗号（共 2858 项）；`M-MF-004` 显示 `考据鉴定法`；`/modes` 120 张卡片 0 条串行文本，`剪纸即兴法,Papercut…` 已消失。工具侧用真实 574 条数据做函数级测试：574/574 折平、`name_en` 无残留汉字、2284 条标量零改写。
- **线上状态**：**已修复并线上复测归零**。push 后 Pages 部署（run 26 / `35342178368`，success）重建了全部静态数据（CI 会重跑 `export_static_site.py`，因此数据层也输出标量）：
  - 线上 bundle 由 `index-D1DYwfIq.js`（修复前，574/2858 串行）变为 `index-CE7EoPzT.js`；
  - 线上 `data/modes/index-0.json` 数组型 `name_zh` 82 → **0**（8 片合计 574 → 0）；
  - 线上 `/graph` 模式下拉含逗号选项 **574 → 0**（共 2858），`M-MF-004` 显示 `考据鉴定法`；线上 `/modes` 120 张卡片 0 条串行文本。

### D2（中，待跟进）概念页两个可疑人物名

`/concepts` 出现 `获取兵`（code `HuoQuBing`，`data/figure_names.json` 里该 code 明明是 `霍去病`）与 `非人`（`H-FEI-001`）。属名称映射层缺陷，会出现在概念页人物列表与 `+N` 展开里。

### D3（中，待跟进）已隔离的虚构人物 H-SX-001 仍从概念图谱漏出

`web/public/data/graph/concept_graph.json` 有 284 个人物节点，其中 `H-SX-001`（B4 已按「引证伪造《苏咸子》」在统一索引/每日索引里 quarantine）仍在图谱里；由于它不在 `index.unified.json`（283 人），`/concepts` 无法解析其名，直接**把编号当人名显示**（如「情报网络 3 人：米芾 / H-SX-001 / 德川家康」）。隔离只做到了索引层，图谱写层未同步。

### D4（低，待跟进）「纸上页脚」URL 不在页脚位置

`/templates/longzhong/` 里 `.pt-print-only` 元素位于 article 面板内部、首屏 y≈188，打印时出现在第一页标题附近而非纸面底部（无 `position: fixed; bottom`）。不影响「链接出现在纸上」，但与「页脚」说法不符。

### D5（低，记录）文档站模板副本与仓库源漂移

`docs_site/docs/templates/*.md`（7 份，7 月版本）与仓库源 `./templates/*.md` 内容不一致（`longzhong`：10,505 B vs 12,033 B，标题缺 emoji 前缀，diff 48 行，另有 `H-SQ-52` vs `H-SQ-22` 之类差异）。网页下载链路用的是仓库源，无功能影响；文档站展示的是旧文本。

## 4. 本卡一并提交的遗留改动（非本卡产生，已核对内容）

`git status` 中 5 个文件是上游 A7/C1 卡片遗留未提交的工作树改动，内容与本卡修复同批提交，均已复核：

| 文件 | 内容 | 判定 |
| --- | --- | --- |
| `tools/export_static_site.py` | `EXPECT_FIGURES 501 → 1058`（与本卡 D1 修复同文件） | 与 CI 实际条数一致，必要 |
| `tools/build_figures_db.py` | 跳过空 `code` 行（Sun Quan 类脏数据） | 与 C1 发现的公开名录脏数据对应 |
| `.gitignore` | 追加 `.mkdocsvenv/` | 无风险 |
| `docs/architecture/static_data_manifest.json` | A7 重建后的产物清单（06:37 UTC） | 由导出工具生成 |
| `api/protreptic.db` | A7 重建的 figures 库（38.5 MB） | 导出源，发布仓已提交同版本 |

## 5. 结论

- **P1 四项功能（图谱 / 对比 / 每日 / 导出+打印）7/7 检查项实测 PASS**，未见空渲染、未见数据夸大；所有数字均由独立重算与真实 DOM 双向验证。
- **D1 是高影响可见缺陷（20% 模式名在 3 个页面串行显示），已在本卡修复：本地构建归零 + 两仓提交 + push → Pages 部署 success → 线上复测归零**（详见 §3 D1 与 §7）。
- D2 / D3 属数据治理层（名称映射、隔离覆盖不全），不阻塞功能，但会以「人物名看起来是乱码 / 编号」的形式暴露给用户，建议紧随其后修复。
- **建议：可发布，且本轮已发布并完成线上复测**（P1 七项在线上抽查：/graph 23/23 且 0 串行、/modes 0 串行、/compare 3 表 51 行 + 共同概念 2 条、/minds 10 区块 11 邻居、/daily M-FYJ-009），C4 终审可在此基础上做 A/B/C 全站回归。

## 6. 复现

```bash
# 1) 构建门（必须 0 error；vue-tsc 会卡类型错误）
cd /opt/data/workspace/Protreptic/web && VITE_DATA_MODE=static npm run build

# 2) 本地静态预览（先确认 4210 没被别的 preview 占着 —— 旧 preview 会继续端旧 dist，最容易误判）
cd /opt/data/workspace/Protreptic/web && npx vite preview --base=/protreptic/ --port 4210 --host 127.0.0.1
curl -s http://127.0.0.1:4210/protreptic/index.html | grep -o 'assets/index-[A-Za-z0-9_-]*\.js'   # 必须等于 web/dist/assets 里的文件名
```

页面清单：`/protreptic/graph/`（三个视图 + 中心模式切 M-AE-008 看虚线）、`/protreptic/minds/H-WYM-001/`、
`/protreptic/concepts/`（点「查看跨人物用法」）、`/protreptic/compare/?items=H-WYM-001,H-HS-001,H-ZZ-001,H-LZ-001`、
`/protreptic/daily/?date=2026-01-01`、`/protreptic/templates/longzhong/`。

```bash
# 3) 名称折平回归（D1 判据：两处都必须为 0）
curl -s http://127.0.0.1:4210/protreptic/data/modes/index-0.json | grep -o '"name_zh":\[' | wc -l   # 数据层：部署前 >0 属预期，CI 重跑 export 后应为 0
#   浏览器侧：/graph 模式下拉里 textContent 含 ',' 的 option 数 = 0（修复前 574），/modes 卡片含 'Method,' 的 = 0

# 4) 数据侧独立复核（本环境 terminal 禁 python -c/heredoc，请用 browser_exec 的 Python 或写成脚本文件再跑）
#    concept_graph.json: 284 人物 / 13288 概念 / 13552 边；similar_modes: 599 有邻居、1018 边
#    daily/index.json: total=2848，i=((utc_ms+480*60000)//86400000)%total → 2026-09-18 为 778 = M-FYJ-009

# 5) 打印媒体实测：CDP Emulation.setEmulatedMedia({media:'print'}) 后读计算样式
#    断言：body 背景 #fff、header/nav 不可见、可见 button = 0、td 边框 1px solid、thead = table-header-group、.pt-print-only 可见

# 6) 模板下载完整性（服务端字节 == 仓库源）
for pair in "baidi:白帝托孤离职" "beifa:北伐复盘" "changban:长坂坡复盘" "chibi:赤壁之战复盘" \
            "jieting:街亭之战复盘" "longzhong:隆中对复盘" "yiling:夷陵之战复盘"; do
  en=${pair%%:*}; zh=${pair##*:}
  a=$(curl -s http://127.0.0.1:4210/protreptic/templates/$en.md | sha256sum | cut -d' ' -f1)
  b=$(sha256sum "/opt/data/workspace/Protreptic/templates/$zh.md" | cut -d' ' -f1)
  echo "$en $([ "$a" = "$b" ] && echo IDENTICAL || echo DIFFER)"
done
```

### 本卡测得的基线数字（供 C4 终审比对）

| 指标 | 值 |
| --- | --- |
| /graph 人物视图（默认 H-WYM-001） | 23 节点 / 23 边 |
| /graph 模式关联（M-MON-008 / M-AE-008） | 23 节点 22 边 / 8 节点 7 边（含 1 条虚线） |
| /graph 全局网络 | 60 节点 / 36 边 |
| /minds/H-WYM-001 相似模式 | 10 区块 / 6 有邻居 / 11 邻居入口 |
| /concepts | 13,288 概念 / 218 跨人物 / 284 人物 / 13,552 边 |
| /compare 4 项共同概念 | 2 条（万物一体 3 人、经世致用 2 人） |
| /daily 今日 | 2026-09-18 / 周五 / M-FYJ-009 时务人士监督法 / 福泽谕吉 |
| 模板 | 7 个 .md，与仓库源 sha256 全同 |
| D1 折平 | 574 → 0（浏览器侧）；工具函数 574/574 |


## 7. 部署与线上复测（本卡 push 后）

| 项 | 值 |
| --- | --- |
| publish 提交 | `bbcf071`（workspace 对应 `76bfe59f`，本地 dev 分支） |
| Pages 运行 | run 26 / `35342178368` → **success** |
| 线上 bundle | `index-D1DYwfIq.js`（修复前） → `index-CE7EoPzT.js`（修复后） |
| 线上数据 | `data/modes/index-0.json` 数组型 `name_zh` 82 → 0 |
| 线上 `/graph` | 人物视图 23/23；模式下拉 0/2858 串行；`M-MF-004 · 考据鉴定法` |
| 线上 `/modes` | 120 卡片 / 0 串行 |
| 线上 `/compare?items=…` | 3 表 51 行；共同概念 `万物一体 · 3`、`经世致用 · 2` |
| 线上 `/minds/H-WYM-001` | 10 区块 / 11 邻居入口 |
| 线上 `/daily` | 2026-09-18 / M-FYJ-009 时务人士监督法 |
| 线上 `/templates/longzhong.md` | 200 / 12,033 B（与仓库源同尺寸） |

**CI 红是否由本卡引入**：否。`bbcf071` 与前一提交 `86453ba`（B5）以及更早的 `7f21db6` / `4fc7d13` 在
`ci-cd.yml`（失败步骤：Run Python tests）、`markdown-lint.yml`、`quality-gate.yml` 上结论**完全一致**（均为 failure），属既有问题；
`pages.yml`（真正决定站点可用性的工作流）为 **success**。
