# Phase30-C4 followup：两条存量红 CI 收口（R1 markdown-lint / R2 ci-cd Python 测试）

卡：`t_5505e042`（父卡 `t_f79fe23e` Phase30-C4 终审）
仓：dev `/opt/data/workspace/Protreptic`（master，本地）/ publish `/opt/data/release/Protreptic-publish`（origin main，驱动 CI）
日期：2026-09-18

---

## 0. 一句话结论

两条长期红都不是"文档/数据写坏了"，而是**门在守错的东西**：

* R1：`globs: "**/*.md"` 把生成/镜像/归档的 Markdown 也拉进门 → 红线噪声埋掉真实信号；
* R2：测试读的是**陈年副本** `tools/scenarios_zh.json`（39 键），真数据早就在
  `api/protreptic.db`（1057 行）→ 断言对着旧数据写死 `1008`，怎么调都对不上。

收口后：markdown-lint **0 error**（213 文件，人工维护文档全量口径保留）；
`Protreptic CI/CD` 的 `Run Python tests` 步骤 **success**。

---

## 1. R1 markdown-lint

### 1.1 实测基线（publish HEAD `07f9983`，run 35349687441 failure，23s）

本地用与 CI 相同的 action 版本复现（`DavidAnson/markdownlint-cli2-action@v14`
= markdownlint-cli2 **v0.11.0** / markdownlint v0.32.1）：

```
$ npx --yes markdownlint-cli2@0.13.0 "**/*.md"        # 首次复现（无 ignore，含 node_modules）
Summary: 12020 error(s)   （553 files）
  MD032 blanks-around-lists    6993
  MD022 blanks-around-headings 3455      （两条占 87%）
  MD009 401 / MD031 282 / MD029 234 / MD056 196 / MD055 155 / MD047 148 / …
```

违规分布说明"门守错了对象"：

| 范围 | 违规数 | 性质 |
|------|--------|------|
| `docs/figures/**`（3376）+ `data/figures/**`（2153） | 5529 | 人物档案的数据层产物 / 镜像副本 |
| `docs/historical_figures_thinking_modes_library.md` | 1430 | 数据层图书馆的镜像文档 |
| `web/public/templates/**`（69）+ `web/dist/**`（69） | 138 | 静态站模板副本 / 构建产物 |
| 其余人工维护文档 | 4923 | ← **只有这部分该由门守** |

### 1.2 口径选择：A + B（收敛 + 清零）

* **A（收敛）**：`.markdownlint-cli2.jsonc` 的 `ignores` 排除
  `node_modules` / `site-packages` / `web/dist` / `web/public/templates` /
  `data/figures` / `docs/figures` / `docs/historical_figures_thinking_modes_library.md` /
  `release/**` / `docs_site/**` / `site_docs/**` 等归档与旧站构建产物。每条 ignore 都能说出"谁生成它"。
* **B（清零）**：剩下的人工维护文档（`docs/**`、`tools/**`、`data/individuals/**`、
  `CHANGELOG.md`、`README.md`、根目录研究笔记…）逐条清到 0。

收敛掉的 7097 条（59%）都是"修了也会被下一次生成覆盖"的产物；
**门的牙留在 213 个人工维护文件上**，不是靠关规则变绿。

### 1.3 修复明细（内容无损优先）

| 规则 | 处理 |
|------|------|
| MD022/MD032/MD031/MD009/MD047/MD030/MD012 | `--fix` 自动修（补空行、去尾随空格）—— 178 + 45 文件 |
| MD055（154 条，`thinking_mode_journal.md`） | 根因是模板块被误插的围栏提前关掉，238-243 行的"假表格"成了全文第一个表，把表的 pipe 风格判反了。删掉误插围栏（块本应 187→316 一整块），154 条一次性消失 |
| MD056 双语对照表（153 行） | 行内多出的第 3 格用 `\|` 合并进第 2 格 —— 英文原文此前**在渲染时被静默丢弃**，现在可见 |
| MD056 表格列数 | `comparison_matrix` 表头多一列（5→4）；`phase2_candidates` 33 行末列粘连（`**已写入** H-XXX` 拆成两列）；`candidates_v2_research.md` 结尾被截断的残行补成全列并标注"待补" |
| MD028（89 条） | 引用块内部空行 → `>`（渲染等价，语义不再歧义） |
| MD001（10 条） | `bilingual.md` Part II/III 的模式标题 `####`→`###`；`weekly_thinking_training.md` 周标题 `#`→`##` |
| MD051（10 条） | 目录锚点与真实标题对齐；顺带发现 `thinking_knowledge_update_guide.md` 目录 4-6 项**指向不存在的章节**（版本管理/激励机制错位），改为真实标题 |
| MD003（2 条） | `*（继续下一章…）*` 紧跟 `---` 会被解析成 setext 标题（真渲染缺陷），补空行 |
| MD035/MD050/MD042 | 占位下划线改全角、`#__` 转义、README 空链接徽章去掉空 `()` |
| MD029（36 条） | 真错号（重复/missing）改正；**跨标题连续编号**的 8 个文件（P0/P1 清单、Phase 步骤清单）用 `<!-- markdownlint-disable MD029 -->` 定点豁免 —— 编号是排序信息，重编号=删内容 |

### 1.4 验收

```
$ npx --yes markdownlint-cli2@0.11.0 "**/*.md"     # 与 CI action 同版本
Linting: 213 file(s)
Summary: 0 error(s)
```

CI：`CI`（markdown-lint）run **35357372422 success（15s）**，此前 4 次 push 全红。

### 1.5 踩坑记录（重要）

`markdownlint-cli2` **v0.13 与 v0.11 行为不同**，必须用 CI 的版本验收：

1. v0.11.0 用 `JSON.parse` 读 `.markdownlint-cli2.jsonc` —— **不能有注释**，
   否则 `SyntaxError: Expected double-quoted property name in JSON`
   （本卡首次推送 run 35356433406 就是栽在这，11s 失败）。
   → 配置改为严格 JSON，口径说明全部搬进 `docs/ci/markdown_lint_policy.md`。
2. v0.13 的 `overrides`（按文件覆盖 markdownlint 规则）在 v0.11 不生效
   → MD029 改用行内指令 `<!-- markdownlint-disable MD029 -->`。

---

## 2. R2 ci-cd.yml 的 Run Python tests

### 2.1 实测基线

run 35351886853 / 35349687510，步骤 `Run Python tests`：

```
File "tools/test_thinking_mode_selector.py", line 40, in test_scenarios_zh
    assert len(SCENARIOS_ZH) == 1008
AssertionError: Expected 1008, got 39
```

### 2.2 根因链

* `thinking_mode_selector.py` 里 `load_json('scenarios_zh.json')` 按 `__file__` 解析 →
  CI `cd tools` 后读到的是 **`tools/scenarios_zh.json`（39 键）**；
  仓库根的 `scenarios_zh.json` 是另一份 93 键、schema 也不同的旧清单。
* **真数据**：`api/protreptic.db` → `figures` 表 **1057 行**（全站共用：`web/public/data/**`、
  `index.unified.json`、质量门 `tools/ci_data_check.py`）。不是数据丢了，是 selector 看错文件。
* 断言里的 1008 / 370 historical / 44 P4 / 25 P5 / 455 international 是从更早的数据形态抄下来的，
  与现数据完全脱节。

### 2.3 改动

* `tools/thinking_mode_selector.py`：场景 / `CODE_MAP` / `SCENARIO_TAGS` 全部改为
  从 `api/protreptic.db` 派生（`_find_db()` 解析顺序与 `figure_library` 同构；
  db 列的 JSON 文本用 `_as_list` 兜底）；`_mode_name()` 兜底解析（db 里有目录中不存在的
  引用，含 `M*`），CLI 不再 KeyError。
* 删除 `tools/scenarios_zh.json`、`tools/scenarios_en.json`（陈旧副本）。
* `tools/test_thinking_mode_selector.py` **重写为 11 条派生/语义断言**：

| 断言 | 内容 |
|------|------|
| 单一数据源 | 场景 code 集合必须等于 db `figures` 的 code 集合；`tools/scenarios_*.json` 不得复活 |
| 口径交叉校验 | `index.unified.json` 的 `counts.total/scenarios` 与 `items` 自洽，且其每个场景 code ⊆ 场景库 |
| code 卫生 | 无空白/占位符（回归 Phase30-C1 的 `code="Sun Quan"`、`"code field"` 脏数据） |
| 名称 | 每个场景都有可显示名称（缺名退化为 code，不出现空串） |
| 双语 | 中英键集一致、`modes` 一致、`CODE_MAP*` 与数据源同步 |
| modes | 结构合法；覆盖率 ≥95%；悬空引用只允许在**显式已知清单**内（新悬空立刻红） |
| 模式目录 | `modes_data.json` 中英键集一致（不写死 618） |
| CLI | `-c/-s/-l/-e json/-e md/-t` 端到端，期望值全部从数据里取 |

* `.github/workflows/ci-cd.yml`：在 `Run Python tests` 前加
  `python3 tools/build_unified_index.py`（`web/public/data/` 已 gitignore，不入库），
  让"与发布口径一致"的断言在 CI 里真的跑起来，而不是被 skip。

### 2.4 验收输出

```
$ cd tools && python3 test_thinking_mode_selector.py
✓ 单一数据源: 1057 个场景全部来自 api/protreptic.db（无 scenarios_*.json 副本）
✓ 口径一致: index.unified.json scenarios=1055 ⊆ 场景库 1057（同一数据源 api/protreptic.db）
✓ code 卫生: 1057 个 code 全部合法（无空白/占位符）
✓ 名称: 494/1057 个场景有真实名称（其余退化为 code，属数据层待补）
✓ 双语: 1057 个场景中英齐全，modes 一致，CODE_MAP 与数据源同步
✓ modes: 1021/1057 场景有模式（覆盖 96.6%），475 个模式引用，悬空 18 个（均在已知清单内）
✓ 模式目录: 625 个模式键（中英一致），可解析数字模式 618 个
✓ CLI -c: A-1-X-P 中英查询正常
✓ CLI -s: 关键词 复杂 命中 A-1-X-P
✓ CLI -l/-e: 列表 399 行，导出 JSON 1057 条 / Markdown 正常
✓ CLI -t: historical_domains=政治 命中 AE-ZAY-001

=== ALL TESTS PASSED (11) ===
```

CI：`Protreptic CI/CD` → job `Test (Python + TypeScript)` **success**。

---

## 3. 顺带暴露并修掉的第三条（B5）

`Test` 步骤变绿后，之前被它挡住的下游 job 才第一次真正运行：
`Build API Docker Image` 报

```
ERROR: failed to build: dockerfile parse error on line 18:
       FROM requires either one or three arguments
```

根因：`Dockerfile.api` 的 `RUN python -c "` 之后是**裸换行**，Dockerfile 把下一行
`from sentence_transformers import SentenceTransformer` 当成指令（`from` → `FROM`）。
改为单条 `RUN`（`\` 续行）。这正是本卡主题的又一例证：**红会掩盖下游真实失败**。

---

## 4. 遗留（不属本卡，供后续排卡）

R1/R2 收口后暴露出的**数据层**问题（与终审报告 §6 的 R3-R9 同层，勿塞进本卡）：

| # | 事项 | 证据 |
|---|------|------|
| F1 | `figures` 表 563/1057 行是**只有 code + modes 的残行**（无中英文名、无描述），网站/选择器只能显示 code | 测试输出"名称: 494/1057" |
| F2 | 36 行没有任何思维模式（`P5-*/H-*/MM-*` 等） | 测试输出"1021/1057 有模式" |
| F3 | 18 个模式引用在模式目录里不存在：`562-567/569`、`M218-M227`、`M571` | 测试输出"悬空 18 个"（已列入 KNOWN 清单，新悬空会立刻红） |
| F4 | 仓库根 `scenarios_zh.json`/`scenarios_en.json`（93 键、列表 schema、无 CI 消费者）与 `tools/code_maps.json`、`tools/scenario_tags.json` 已不再被 selector 读取，仍是口径混淆源 | 本卡只删了被 selector 直接喂食的两份 |
| F5 | `docs/archive/research/**` 等历史研究文档只存在于 publish 仓，dev 仓缺失（两仓不是同一棵树） | `comm -23 dev pub` 1691 行 / `comm -13` 678 行 |

复跑命令（与 CI 同版本）：

```bash
npx --yes markdownlint-cli2@0.11.0 "**/*.md"          # 期望 0 error（publish 213 / dev 224 文件）
python3 tools/build_unified_index.py && cd tools && python3 test_thinking_mode_selector.py
```
