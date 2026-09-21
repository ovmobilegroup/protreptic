# Phase44 验收复验报告（QA9）

- 卡片：`t_942cd36a` · `[Phase44-QA9] 复验：README 可读性 + 许可正确性 + 贡献入口可达`
- 复验人：espinosa（独立复验，全部命令自跑，只贴原始输出）
- 复验时间：2026-09-21 10:59 CST
- 复验对象：workspace `85fc174d301cdd1042d92f7ded79344cbcd27fd2` / publish `dacb1f40d9d9bbfa75d34930e1796d44109ec8aa`
- 线上：https://ovmobilegroup.github.io/protreptic

## 结论

**可发布（PASS）** —— 4 项检查全部 PASS，无谎报、无空渲染、无互相矛盾的许可声明。

| # | 检查项 | 判定 |
|---|---|---|
| 1 | README 首屏可读 + 无 Phase 开头 + 链接逐个 200 | **PASS** |
| 2 | 双许可文件齐备 + CC 正文官方逐字 + 全库无矛盾声明 | **PASS** |
| 3 | 线上贡献入口可达（页脚 + /api） | **PASS** |
| 4 | 两仓 parity 零差异 + ahead=0 + CI 全绿 | **PASS** |

观察项 3 条见文末（均非阻塞，不构成本次 FAIL）。

---

## 1. README 可读性

### 1.1 首屏能看懂「这是什么项目」

```
$ sed -n '1,10p' README.md
# Protreptic · 思维养成系统

> **把「历史上的人怎么想问题」变成你今天能照着做的步骤。**
> 在线站点（免安装，打开即用）：**https://ovmobilegroup.github.io/protreptic/**

[![站点](https://img.shields.io/badge/...)](https://ovmobilegroup.github.io/protreptic/)
[![代码许可: MIT](...)](LICENSE)
[![内容许可: CC BY-SA 4.0](...)](LICENSE-CONTENT)
```

首屏即给出：一句话定位 + 在线站点链接 + 双许可徽章；紧接着是「## 这是什么 / ## 规模 / ## 可信度 / ## 站点能做什么」。**PASS**（首次访问者无需任何前置知识即可理解）

### 1.2 不再以 Phase 变更日志开头

```
$ grep -n -i "phase" README.md
141:项目从 2026-07 起按阶段推进（Phase 1 → Phase 44）：先写思维方法与写作技法手册，再逐位归档历史人物档案，随后转入工程化 ——
```

全文仅第 141 行「研究历程」一节提到 Phase，且位于文末叙述段落，**不以变更日志开头**。**PASS**

### 1.3 文中链接逐个 curl 验 200

```
$ python3 qa9_links2.py          # 抽取 README 全部 17 个 markdown 链接，逐个 curl -L
200 https://img.shields.io/badge/...（在线站点徽章）
200 https://img.shields.io/badge/...（代码许可徽章）
200 https://img.shields.io/badge/...（内容许可徽章）
200 https://ovmobilegroup.github.io/protreptic/docs/06-ai-collaboration/thinking_mode_agent_prompt/
200 https://ovmobilegroup.github.io/protreptic/docs/00-quick-start/thinking_mode_quick_start/
200 https://ovmobilegroup.github.io/protreptic/docs/
200 https://ovmobilegroup.github.io/protreptic/docs/04-training/thinking_mode_gym/
200 https://raw.githubusercontent.com/ovmobilegroup/protreptic/main/CONTRIBUTING.md
200 https://raw.githubusercontent.com/ovmobilegroup/protreptic/main/.github/ISSUE_TEMPLATE/bug.md
200 https://raw.githubusercontent.com/ovmobilegroup/protreptic/main/.github/ISSUE_TEMPLATE/feature.md
200 https://raw.githubusercontent.com/ovmobilegroup/protreptic/main/.github/ISSUE_TEMPLATE/case.md
200 https://raw.githubusercontent.com/ovmobilegroup/protreptic/main/.github/PULL_REQUEST_TEMPLATE.md
200 https://raw.githubusercontent.com/ovmobilegroup/protreptic/main/CODE_OF_CONDUCT.md
200 https://raw.githubusercontent.com/ovmobilegroup/protreptic/main/LICENSE
200 https://raw.githubusercontent.com/ovmobilegroup/protreptic/main/LICENSE-CONTENT
200 https://raw.githubusercontent.com/ovmobilegroup/protreptic/main/CHANGELOG.md
404 https://raw.githubusercontent.com/ovmobilegroup/protreptic/main/docs/qa   <-- 目录，raw 不服务目录

NON200 count: 1
```

唯一 404 是 `docs/qa/`（README 中写作目录链接），**raw.githubusercontent 本就不服务目录**，属取证方式问题而非死链：

```
$ curl -s -o /dev/null -w "%{http_code}\n" -L "https://github.com/ovmobilegroup/protreptic/tree/main/docs/qa"
200
```

结论：17/17 个链接真实可达。**PASS**

### 1.4 README 数字与线上口径一致（防「数字对不上」）

```
$ curl -sL https://ovmobilegroup.github.io/protreptic/data/meta.json   # 解析 counts
counts = {"figures": 1057, "mode_by_figure_shards": 278, "mode_summaries": 2858,
          "mode_summaries_published": 2798, "modes_quarantined": 60,
          "verification": {"published": {"verified": 888, "pending": 1547, "suspect": 23, "unverifiable": 340}}}
```

线上 /figures 页真实渲染（浏览器 DOM 回读，非源码）：

```
278 位历史人物的思维方法，与 1055 个现代处境场景，汇成同一份可检索的名录，每条都有出处与操作步骤，中英双语。
人物 278 / 场景 1055 / 1297 条含模式  ·  1333 条
```

README「规模」表：278 位 / 2798 条 / 隔离 60 / 场景 1055 / 模板 7 —— 与线上一致（2798+60=2858 自洽；线上 /templates 页回读「7 个核心复盘模板」）。**PASS**

---

## 2. 许可正确性

### 2.1 两份许可文件均在，README 说清适用范围

```
$ ls -la LICENSE LICENSE-CONTENT
-rw------- LICENSE           1606 bytes
-rw-r--r-- LICENSE-CONTENT  21513 bytes
```

```
$ sed -n '113,120p' README.md
| **代码**：`web/`、`tools/`、`api/`、`scripts/` 及构建/CI 脚本 | **MIT** | [LICENSE](LICENSE) |
| **内容与数据**：`docs/` 下的文档、`data/` 与模式数据、复盘模板文本 | **CC BY-SA 4.0** | [LICENSE-CONTENT](LICENSE-CONTENT) |
- 代码（MIT）：可自由使用、修改、分发、商用，保留版权声明即可
- 内容（CC BY-SA 4.0）：可自由共享与改编（含商用），但需**署名**并以**相同方式共享**；官方正文见 https://creativecommons.org/licenses/by-sa/4.0/legalcode
```

LICENSE 首行 `MIT License`，并在文末附「适用范围说明（以上文字不是许可条款，也不构成对上方 MIT 条款的任何修改）」；LICENSE-CONTENT 明示适用于 `docs/`、`data/` 与模式数据、`web/public/templates/` 复盘模板文本，代码不适用本许可。**PASS**

### 2.2 CC 正文是否为官方原文（逐字核对）

```
$ curl -sL https://creativecommons.org/licenses/by-sa/4.0/legalcode.txt -o cc_official.txt
$ wc -c cc_official.txt ; sha256sum cc_official.txt
20138 cc_official.txt
28a9529c7d0bb4dc51f4bf5c116a3d16ef247a052f7591466768ddf563fd1cf5  cc_official.txt
```

（与 LICENSE-CONTENT 中自述的官方正文 sha256 `28a9529c7d0bb4dc51f4bf5c116a3d16ef247a052f7591466768ddf563fd1cf5` **完全一致**）

逐字比对（LICENSE-CONTENT 第 26 行起 428 行 vs 官方 428 行）：

```
local total lines 453, official 428, offset(local 0-based)=25
### 段 1-12 行: MATCH=True    sha256(official段)=8b7c0628305a34f2 / sha256(local段)=8b7c0628305a34f2
### 段 56-75 行: MATCH=True   sha256(official段)=c28ffe7622a76697 / sha256(local段)=c28ffe7622a76697
### 段 409-428 行: MATCH=True sha256(official段)=406e52b584d7e966 / sha256(local段)=406e52b584d7e966
整段(第26行起至文件末尾) exact match = True
```

抽查 3 段（开篇 1-12 行、正文 56-75 行、结尾 409-428 行）全部 MATCH，**且不止抽查：整段 428 行与官方 legalcode.txt 逐字节相同**。LICENSE-CONTENT 中另有「许可摘要（非法律文本，仅供快速了解）」区块，已明确标注为非法律文本、法律上以官方 legalcode 原文为准 —— 不存在自编法律条款。**PASS**

### 2.3 全库是否还有互相矛盾的许可声明

```
$ grep -rn -E "(MIT|CC BY-SA)" --include=*.md --include=*.yml --include=*.vue --include=*.html . | grep -E "全部|整个仓库|所有内容|覆盖|代码|内容"
./docs/00-quick-start/installation-guide.md:107  代码（web/ tools/ api/）按 MIT
./docs/00-quick-start/installation-guide.md:108  内容与数据（docs/ 文档与模式数据）按 CC BY-SA 4.0
./docs/index.md:86  代码（web/ tools/ api/）：MIT License
./docs/index.md:87  内容与数据（本站文档与模式数据）：CC BY-SA 4.0
./CONTRIBUTING.md:66-70  代码 MIT / 内容与数据 CC BY-SA 4.0（按改动范围）
./.github/PULL_REQUEST_TEMPLATE.md:37  本仓库为双许可：代码 MIT / 内容与数据 CC BY-SA 4.0
./web/src/App.vue:150  代码 MIT · 内容 CC BY-SA 4.0
./mkdocs.pages.yml:123  copyright: © 2025 Protreptic Project Team · 代码 MIT / 内容 CC BY-SA 4.0
./README.md:115-120  （对照表 + 理由）
```

全部 9 处均为**按范围双许可**表述，未见「MIT 覆盖全部」与「CC BY-SA 覆盖全部」并存。

针对卡片点名的对象：

```
$ grep -n -E "许可|LICENSE|MIT|开源协议" docs/10-community/thinking_community_ops_plan.md
789:*许可：CC BY-SA 4.0*
```

运营方案第 789 行「许可：CC BY-SA 4.0」是**该文档自身的页脚署名**（该文件位于 `docs/`，按双许可属内容侧，CC BY-SA 4.0 正确）；第 709 行「明确 CC BY-SA 4.0 协议 + 来源标注要求」是社区内容贡献的风险应对，同样指内容侧。**未见「CC BY-SA 覆盖全部（含代码）」的矛盾声明。PASS**

---

## 3. 贡献入口可达（从线上页面抓取）

### 3.1 线上页脚（浏览器渲染 DOM 回读，非源码猜测）

```
$ 打开 https://ovmobilegroup.github.io/protreptic/ ，读 footer DOM
footer innerText:
以史为鉴，知兴替；以人为鉴，明得失。
Protreptic · 2798 条思维模式 × 278 位历史人物 · 中英双语
已核验 888 · 待核验 1547 · 存疑 23 · 一手材料 340
可信度统计 · GitHub · 参与贡献 · 代码 MIT · 内容 CC BY-SA 4.0

footer 内链接：
https://github.com/ovmobilegroup/protreptic                                | GitHub
https://github.com/ovmobilegroup/protreptic/blob/main/CONTRIBUTING.md      | 参与贡献
```

### 3.2 线上 /api「OPEN SOURCE」区块

```
$ 打开 https://ovmobilegroup.github.io/protreptic/api ，读 section DOM
OPEN SOURCE / 参与贡献
本知识库开源，欢迎贡献：补充案例、纠正出处、提议新思维模式、补充译文。
--links--
https://github.com/ovmobilegroup/protreptic/blob/main/CONTRIBUTING.md | 贡献指南 | target=_blank rel=noopener
https://github.com/ovmobilegroup/protreptic/issues/new/choose         | 提交 issue | target=_blank rel=noopener
```

### 3.3 抓到的链接 curl 验可达

```
200 https://github.com/ovmobilegroup/protreptic/blob/main/CONTRIBUTING.md
200 https://github.com/ovmobilegroup/protreptic/issues/new/choose
200 https://github.com/ovmobilegroup/protreptic/issues/new?template=bug.md
200 https://github.com/ovmobilegroup/protreptic/issues/new?template=feature.md
200 https://github.com/ovmobilegroup/protreptic/issues/new?template=case.md
```

issue 模板实体文件在库内：

```
$ ls .github/ISSUE_TEMPLATE/
bug.md  case.md  feature.md
$ ls .github/
ISSUE_TEMPLATE/  PULL_REQUEST_TEMPLATE.md  dependabot.yml  workflows/
```

线上 bundle 亦含该入口（`assets/index-ClCsRHsF.js`，364625 bytes）：`CONTRIBUTING.md` ×2、`issues/new/choose` ×1、「参与贡献」×2、`代码 MIT` ×1。**PASS**

---

## 4. 全局：parity / ahead / CI

### 4.1 两仓字节级一致

```
$ python3 tools/check_repo_parity.py
[boundary] workspace = /opt/data/workspace/Protreptic
[boundary] publish   = /opt/data/release/Protreptic-publish
[stats] 两仓都有 1434 条（其中逐字节一致 1434）｜仅单侧 0 条（仅工作仓 0 · 仅发布仓 0）
[OK] 零差异：1434 个构建图文件两仓逐字节一致（sha256）
parity rc=0
```

### 4.2 ahead=0

```
$ cd /opt/data/release/Protreptic-publish && git status -sb
## main...origin/main          <- 无 [ahead N]
```

（workspace 侧为 `## master`，该仓为本地开发仓，未设上游跟踪；发布口径以上述 publish 仓为准。）

### 4.3 CI 全绿（job 数）

```
$ curl -s .../commits/dacb1f40d9d9bbfa75d34930e1796d44109ec8aa/check-runs
total_count 15
  线上死链检测 (sitemap + 站内链接) | completed | success
  Lighthouse 预算门 | completed | success
  数据校验 (schema + sitemap 一致性) | completed | success
  部署 | completed | success
  Deploy to Staging | completed | skipped        <- 设计上按条件跳过
  Deploy to Production | completed | skipped     <- 设计上按条件跳过
  Notify | completed | success
  数据校验 (schema + sitemap 一致性) | completed | success
  Lighthouse 预算门 | completed | success
  线上死链检测 (sitemap + 站内链接) | completed | success
  构建 SPA + 文档站 | completed | success
  Build API Docker Image | completed | success
  Build Web Docker Image | completed | success
  Test (Python + TypeScript) | completed | success
  markdown-lint | completed | success
jobs: 15   non-success: [('Deploy to Staging','skipped'), ('Deploy to Production','skipped')]

$ curl -s .../actions/runs?head_sha=dacb1f4...
total_count 5   全部 success：
  CI | push | success
  Deploy to GitHub Pages | push | success
  Protreptic CI/CD | push | success
  Quality Gate | workflow_run | success
  Quality Gate | workflow_run | success
```

**15 个 job：13 success + 2 skipped（by design）+ 0 failure；5 个 workflow run 全 success。PASS**

---

## 5. 观察项（非阻塞，不计入 FAIL）

**观察 1 —— `web/index.html` 源码仍硬编码旧口径（两仓同）**：第 14/21 行为「2848 条思维模式 × 283 位历史人物」，而线上实际为 2798 × 278（CI 构建时由 `tools/apply_site_counts.py` 重写 dist，故线上正确、线上 meta description 回读为「2798 条思维模式 × 278 位历史人物」）。属源码卫生遗留，建议单独排期。

```
$ grep -n -E "条思维模式|位历史人物" web/index.html
14:          content="2848 条思维模式 × 283 位历史人物：每条都有出处、操作步骤与现代应用。以人为鉴，明得失。" />
21:    <meta property="og:description" content="2848 条思维模式 × 283 位历史人物 · 中英双语" />
$ curl -sL https://ovmobilegroup.github.io/protreptic/ | grep -o -E '<meta name="description"[^>]*>'
<meta name="description" content="2798 条思维模式 × 278 位历史人物：每条都有出处、操作步骤与现代应用。以人为鉴，明得失。" />
```

**观察 2 —— `docs/planning/community_launch_assessment.md` 为时点评估，结论已过期且在线可读**：其第 27/84/110 行仍写「LICENSE（MIT）与运营方案（CC BY-SA）二选一，全库统一」「README 陈旧」。Phase44 已按双许可落地、README 已重写，该文未随之更新；该页线上可达（`/docs/planning/community_launch_assessment/` → 200）。建议在文首加「已归档，结论被 Phase44-C1/C2 取代」标注。**这不构成许可矛盾**（运营方案写 CC BY-SA 系指内容侧，与双许可一致），只是过期结论。

**观察 3 —— README 数字来源脚注略微不精确**：README 写「数字口径来源：部署产物 `data/meta.json` 的 `counts`」。实测 `counts` 含 figures=1057 / mode_by_figure_shards=278 / mode_summaries_published=2798 / modes_quarantined=60，但「场景 1055」「模板 7」不在 `counts` 里（来自 /figures 与 /templates 页口径）。数字本身与线上一致，仅脚注可再精确为「meta.json + 统一名录页」。

---

## 附：取证脚本与原始产物

- 链接抽取 + curl：`/opt/data/profiles/espinosa/cache/scratch/qa9_links2.py`
- CC 逐字比对：`qa9_cc.py` / `qa9_cc2.py` / `qa9_cc3.py` / `qa9_cc_spot.py`；官方正文：`cc_official.txt`
- 线上回读产物：`live_index.html` / `live_bundle.js` / `live_meta.json` / `figs.json`
- CI 原始 JSON：`checks.json` / `runs.json`
