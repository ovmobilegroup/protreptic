# Protreptic 可信度体系（Credibility Framework）

> 目标：把对外承诺「**每条都有出处**」从**断言**变成**可点击、可核验、有分级、有 CI 门守着的机制**。
> 状态：规划中（Phase 35 起分阶段落地）
> 依据：对本仓 `data/modes_data.json`（2858 条有效模式 / 283 位人物）的实测侦察

---

## 0. 为什么做（实测证据，非推测）

| # | 类别 | 实例 | 影响面 | 证据 |
|---|---|---|---|---|
| E1 | **伪人物**（figure 非真实历史人物） | `H-P23F-001`「Phase23收尾整合」/ `P24F` / `P25F` / `P26F` / `Phase27Final` | **5 个"人物" / 50 条模式** | 线上 `/minds/P24F` 等 5 个 URL 均 200，标题即「Phase2x收尾整合」；已进入 `index.unified.json` 名录 |
| E2 | **出处字段污染**（塞入流水线内部痕迹） | `M-P23F-002`「双镜像同构法」出处=「Phase 21 入库与修复提交链（双镜像 sha256 记录：茅以升 96bdd4c4…）」 | ≥42 条含 sha256/提交哈希/脚本名 | grep `sha256\|qa_postmerge\|双镜像\|入库复检` 命中 56 条 |
| E3 | **伪造出处**（引不存在的书） | `H-SX-001`「苏咸」引《苏咸子》 | 10 条（已隔离） | 检索证实《苏咸子》不存在 |
| E4 | 出处粒度不足 | 仅书名级（无篇/章/卷） | 1041 / 2858 = 36% | 字段统计 |
| E5 | 无页码 | 出处带页码 | 仅 25 / 2858 | 字段统计 |
| E6 | 引用面巨大且无人核对 | 被引书名 | **2169 种** | 字段统计 |
| E7 | **无核验状态字段** | — | 全部 2858 条 | schema 中不存在 verification 类字段 |

**结论**：产品最核心的承诺上，目前已确认存在 2 类真实缺陷（E1/E2 尚未止血），且缺少任何"可信度"表达机制（E7）。

---

## 1. 审计口径（Defect Taxonomy）

对每条模式定义可机检的缺陷类别：

| 代号 | 缺陷 | 判定规则（机检） | 处置 |
|---|---|---|---|
| **D1** | 伪人物 | `figure_code` 对应实体非真实历史人物（阶段标签 / 流程名 / 占位符） | 出库 + 隔离 |
| **D2** | 伪造出处 | 书名不存在于任何权威目录；或自引伪造（《X氏子》型） | 隔离 + 复核 |
| **D3** | 出处污染 | `source_chapter` 含工程痕迹：`sha256` / commit 哈希 / 脚本名 / `双镜像` / `qa_postmerge` / 工作树叙述 | 重写或隔离 |
| | | **豁免条款**：**D1 已隔离记录允许保留源库工程痕迹，以导出期过滤为准**——隔离项不进任何公开产物（名录 / 每日 / 图谱 / 概念层），源库工程痕迹只服务复核与回滚，不对外可见。<br>**名单唯一事实来源**：`tools/_quarantine.py` 的 `QUARANTINE`（当前 6 项：`H-SX-001`、`H-P23F-001`、`P24F`、`P25F`、`P26F`、`Phase27Final`）；gate **不复制名单副本**，改名单只改那一处。<br>**机检方式**：`credibility_gate.py::check_d3_pollution()` 对 `is_d3_exempt(mode, quarantine)` 为真的模式**跳过 D3 扫描**，仅对公开 figure 扫 `source_chapter`；**豁免面必须在 gate 报告里如实打印**，禁止静默跳过。<br>**可关**：`--no-d3-exemption` 关掉豁免（严格模式，连隔离项一起扫），用于审计回看。 |
| **D4** | 引文不符 | `key_quote_zh` 文本不出现于所标出处的原文 | 复核 |
| **D5** | 时间线矛盾 | 引文年代 > 人物卒年（或 < 生年） | 复核 |
| **D6** | 悬空引用 | `cross_references` / `related_modes` 指向不存在的 `mode_code` | 自动修 |
| **D7** | 重复/近重复 | 同 figure 内 definition 相似度 > 阈值；或跨 figure 文本重复 | 合并/标注 |

**审计产出物**：`docs/qa/credibility_audit.md` + 机读 `data/audit/findings.json`
（每条：`mode_code` / `figure_code` / `defect` / `evidence` / `suggested_action`），**全部可复核**。

---

## 2. 引文可点击化 · 链接源清单（Link Sources）

| 出处类型 | 数量级 | 首选链接源 | 备注 |
|---|---|---|---|
| 中文古籍（经史子集） | 868 条含古籍书名 | **ctext.org** / 维基文库 `zh.wikisource.org` | 章节级深链；《史记》《资治通鉴》《论语》等直接可定位 |
| 西文经典 | 733 条含英文 | **Project Gutenberg** / **Internet Archive** / `en.wikisource.org` | 公版书可全文定位 |
| 现代著作 | 一批 | **OpenLibrary** / 豆瓣 / 出版社页 | 仅做到书目级 |
| 事件 / 档案 | 一批（如康熙废太子、朗道考试） | 维基百科 / 博物馆·档案馆 | 链接到条目，非全文 |
| 口述 / 访谈 / 信札 | 一批 | **标注 `unverifiable` / `primary-source`** | **诚实标注不可链接，不硬造链接** |

**实现**：`data/source_links.json` —— `{book_or_event: {url, source_type, confidence}}`，
构建期把出处文本解析 → 匹配 → 生成可点击引用；解析不了的**保持纯文本并标记**。

> ⚠️ 铁律：**链接必须真实可达**（构建期 curl 校验 200），禁止猜测 URL。解析失败的**不得伪造链接**。

---

## 3. `verification_status` Schema

每条模式新增（向后兼容，缺省 `pending`）：

```json
"verification": {
  "status": "verified | pending | suspect | unverifiable",
  "method": "auto-scan | link-resolved | quote-matched | manual-review",
  "evidence": "https://ctext.org/... 或复核说明",
  "checked_at": "2026-09-19",
  "checker": "<worker-id 或 'ci'>"
}
```

| status | 含义 | UI 展示 |
|---|---|---|
| `verified` | 出处可达 + （如适用）引文匹配 | ✓ 已核验（可点击出处） |
| `pending` | 未核验（缺省） | ○ 待核验 |
| `suspect` | 命中 D1–D5 之一，待复核 | ⚠ 存疑 |
| `unverifiable` | 属口述/信札等本质不可链接类型 | — 一手材料（不可链接） |

**UI**：模式卡片 + 人物页加可信度徽章；**"存疑"比"假装全对"更可信**。
统计页诚实公布：已核 X / 待核 Y / 存疑 Z。

---

## 4. CI 门设计（防回流）

在现有预检（`EXPECT_FIGURES` 等断言）旁**并列**新增 `credibility_gate`：

```
tools/credibility_gate.py：
  D1 伪人物      → 硬 FAIL（新增即拦）
  D2 伪造出处    → 硬 FAIL
  D3 出处污染    → 硬 FAIL（正则扫描 source_chapter，**豁免已隔离 figure**）
  | | *豁免逻辑*：`is_d3_exempt()` 为真 = 该模式 `figure_code` ∈ `tools/_quarantine.py:QUARANTINE`（唯一事实来源，当前 6 项）；命中即跳过 D3。实现入口 `check_d3_pollution(mode, quarantine, apply_exemption)`。
  | | *豁免可关*：`--no-d3-exemption` → 严格模式，隔离项也扫。
  | | *自测*：`python3 tools/test_credibility_gate.py`（6 例：豁免不报 / 非豁免必报 / 严格模式必报 / 负对照必 exit 1 / 干净必 exit 0 / 真实源库 D3=0）。
  D6 悬空引用    → 硬 FAIL
  D4/D5         → WARN（写审计清单，不阻断）
```

- 接入发卡流水线：**挖矿卡入库前**必须先过 gate；不过直接 auto-block。
- 与现有 `preflight` 一样，gate 自身要有**负对照测试**（故意注入一条 D3 → 必须 exit 1）。

---

### 4.1 D3 豁免实测（Phase37-X1，命令 + 输出）

源库现状（`data/modes_data.json`，2888 条模式）：

```bash
# 默认：豁免生效（D3 只对公开 figure 扫）
python3 tools/credibility_gate.py --data-path data/modes_data.json
  Hard failures (D1/D2/D3/D6): 527
  of which D3 出处污染: 0
  D3 exemption: on
  D3-exempted modes (D1 quarantined figures, not scanned): 43
  by figure: H-P23F-001=9, H-SX-001=10, P24F=6, P25F=5, P26F=7, Phase27Final=6
  whitelist source: tools/_quarantine.py QUARANTINE = ['H-P23F-001', 'H-SX-001', 'P24F', 'P25F', 'P26F', 'Phase27Final']

# 严格模式：连隔离项一起扫（D3 反而能看见 6 条）
python3 tools/credibility_gate.py --no-d3-exemption --data-path data/modes_data.json
  of which D3 出处污染: 6

# 自测（两个方向都验，防回流）
python3 tools/test_credibility_gate.py
  6/6 passed
```

口径：**D3 在公开人物面上为 0 条**；豁免面 43 条模式、分布在 6 个 D1 隔离 figure 上，逐条可查。
严格模式下可见的 6 条 D3 命中：`M-P23F-001` / `M-P23F-002` / `M-P23F-009`（H-P23F-001）、
`M-P25F-006`（P25F）、`M-P26F-001` / `M-P26F-004`（P26F）——全部不进公开产物。

> 边界声明：本豁免**只覆盖 D3**。D1（隔离人物自身）/ D2（伪造出处）/ D6（悬空引用）在源库上仍硬 FAIL
> （上表 527 条），属**存量债务**，不是本豁免的口径问题；CI 侧「存量不阻断、新增必红」见 Phase37-X3 卡。


## 5. 分阶段路线

| 阶段 | 内容 | 产出 |
|---|---|---|
| **P35-A 止血** | 清掉 D1 伪人物（≥5 个 / 50 条）+ D3 污染出处重写 | 线上不再有「Phase2x收尾整合」人物 |
| **P35-B 审计** | 全量扫 D1–D7，出 `credibility_audit.md` + `findings.json` | 可复核的坏数据全清单 |
| **P35-C 机制** | schema 定稿 + `source_links.json` + `credibility_gate.py`（含负对照） | 机制就位 |
| **P35-D 落地** | 构建期解析出处 → 生成可点击引用 + 写入 `verification` | 线上每条出处可点 |
| **P35-E 展示** | UI 可信度徽章 + 统计页 | 「已核 X/待核 Y/存疑 Z」 |
| **P35-QA** | 独立复验（含负对照、线上实测） | 可发布/不可发布结论 |

---

## 6. 铁律（承接项目既有纪律）

1. 归因/结论必须出示原始证据；查不到就说"根因未查明"；**禁用流利故事填补证据空白**。
2. 链接必须真实可达（构建期 curl 200 校验）；**解析不了就诚实标注，不伪造**。
3. 「存疑」要如实展示，**不假装 100% 干净**。
4. 任何机检规则都要有**负对照测试**（能抓到坏样本）。
5. 两仓同步、字节级一致；push 后 `ahead=0`；CI 自证。

---

## 7. CI 两档门口径：存量冻结 / 新增即拦（Phase37-X3）

问题：源库仍有 **527 条存量硬失败**（D1 60 / D2 9 / D6 458）。`credibility_gate.py` 的默认
档位是严格口径（任何硬失败 exit 1），照抄接进 CI 的直接后果是 **Pages 永久红、部署永远 skip**
（QA6 §4.2 实测 exit 1 / 533）。修复办法不是放宽规则，而是**把「存量」和「新增」分开判**。

| 档位 | 语义 | 退出码 |
|---|---|---|
| `--legacy-report` | 存量（基线内）+ 新增都逐条列出，只报告不阻断 | 恒 `0` |
| `--hard-fail` | 基线内只报告（`::notice`）；**基线外任何一条硬失败** | 无新增 `0` / 有新增 `1` / 基线缺失 `2` |
| `--write-baseline` | 用当前硬失败重新冻结基线（改基线必须显式跑） | `0` |

- 基线文件：`data/audit/credibility_baseline.json`（入库，两仓字节一致），冻结 527 条 /
  526 个指纹，并记录冻结时的 `data_sha256`。
- **指纹 = `mode_code|规则|规则内稳定键`**：D1→`figure_code`，D2→伪造书名，D3→命中的污染
  正则，D6→`字段+被引用的 code 主体`。含义：**改存量条目的说明文字不误报**（不制造假新增），
  而**新模式 / 新 figure_code / 新伪造书名 / 新污染模式 / 新悬空引用**必拦。
- 链接源用同一套口径：`data/audit/source_links_baseline.json` 冻结存量坏链；
  `verify_source_links.py --hard-fail` 下**连接层失败（curl 000 / 超时）只算警告**，不计违规
  —— CI 的网络抖动不该把发布链打红；确定性坏链（4xx/5xx）才进「存量 / 新增」判定。
- `--data-path` 的完整语义：**数据 / 白名单（`tools/_quarantine.py`）/ 默认基线三者同仓**
  （由 `<root>/data/modes_data.json` 反推 root），避免「用 A 仓白名单判 B 仓数据」。
- **负对照不能当 CI 步骤**：`--negative-test` 的成功语义就是 `exit 1`（证明门有牙）。
  它的语义由两个自测守护：`tools/test_credibility_gate.py`（D3 豁免两方向）与
  `tools/test_credibility_gate_modes.py`（两档七项）。
- CI 接线与两次真实 run 的原始证据：见 `docs/qa/phase37_x3_ci_gate.md`。

---

## 8. findings.json 自检接进 CI 的两档口径（Phase37-X5）

`tools/verify_findings.py`（Phase37-X2 入库）此前**未接进任何 workflow**：它天然是「新增即拦」
语义，且把 `findings.json` 的 summary 与**现算**库对照，`data/modes_data.json` 一变（sha256 变）
就报「过期」—— 照抄接进 CI 会制造新一轮存量红（Phase37-X3 §9.2 已如实记录）。本节定口径。

### 8.1 两档（与 `credibility_gate.py` 同构）

| 档位 | 语义 | 退出码 |
|---|---|---|
| `--legacy-report` | 存量（基线内）+ 新增都逐条列出，只报告不阻断 | 恒 `0` |
| `--hard-fail` | 基线内只报告（`::notice::LEGACY`）；**基线外任何一条硬失败** | 无新增 `0` / 有新增 `1` / 基线缺失 `2` |
| `--write-baseline` | 用当前硬失败重新冻结基线（改基线必须显式跑） | `0` |

- 基线文件：`data/audit/findings_baseline.json`（入库，两仓字节一致），记录冻结时的
  `data_sha256` / `findings_sha256` 与指纹计数。**冻结当时源库无存量硬失败（0 条）**，
  故本文件 `entries` 为空 —— 这不是「没接」，而是「当前没有可冻结的存量债务」；
  机制在位且 fail-closed：基线缺失时 `--hard-fail` 直接 `exit 2`，不静默放行。
  将来若出现可接受的历史遗留（迁移期、一次性放宽），必须显式跑 `--write-baseline` 并在报告说明。
- **指纹 = `规则|规则内稳定键`**：A 结构 → 归一化消息（下标 + 字段名）；B 不存在 →
  `mode_code=值` / `figure_code=值`；C 锚点 → 归一化消息（**引号内的值被抹掉**，改锚点文字不产生
  假新增）；D 自洽 → `summary.字段名`。含义：**改存量条目的说明文字不误报**，
  而**新的失效引用 / 新的结构缺陷 / 新的自洽缺陷**必拦。
- `--data-path` 的完整语义与 gate 一致：由 `<root>/data/modes_data.json` 反推 root，
  默认基线取**同一仓**的 `data/audit/findings_baseline.json`。
- 基线里的路径一律写**仓内相对路径**（`data/modes_data.json`），保证 dev/pub 两仓字节一致。

### 8.2 「计数过期」（E 类）的归属：**警告，不是新增违规**（本卡决策）

`verify_findings.py` 的 A-D 是**清单自身**的硬失败（结构 / code 存在性 / 锚点可定位 / 计数自洽），
E 是**清单新鲜度**（summary 与现算库是否一致）。归属决策与理由：

| 归属 | 后果 | 判定 |
|---|---|---|
| 算新增违规（红） | `modes_data.json` 每次数据更新 sha256 都变，summary 必然过期，于是**每次数据改动都红**，并强迫每次无关数据提交都额外刷新 findings 才能绿 | 否决 |
| **算警告（不红）** | CI 只打印 `::warning::计数过期(E) ... 刷新：python3 tools/build_audit_findings.py --write`，坏数据仍由 `credibility_gate --hard-fail` 拦 | **采用** |

一句话：**坏数据归 credibility_gate，清单新鲜度归人**。E 的作用是提示刷新，不是拦人；
真正拦人的是 A-D（清单说谎：引用了不存在的 code、锚点在库里找不到）。

### 8.3 CI 接线位置

- 只接**发布仓** `ci-cd.yml` 的 `test` job（与 X3 的可信度门 / 链接核验相邻）：
  `python3 tools/verify_findings.py --hard-fail --data-path data/modes_data.json`。
- **不动** `pages.yml`：发布链已由 X3 的两道门守住，多一道「过期判定」会把部署打红
  —— 这正是本卡要避免的事故模式。
- 负对照不能当 CI 步骤（成功语义 = `exit 1`），其语义由 `tools/test_verify_findings_modes.py`
  八项守护（含「注入不存在 code 必红」「基线缺失 exit 2」「计数过期只警告不红」）。
- 原始证据（本地命令 + 真实 CI run）见 `docs/qa/phase37_x5_findings_ci.md`。

---

## 9. 两仓一致性口径：按构建图推导（Phase37-X4）

> 本章**取代** Phase36-W4 的验收口径「两仓 **2363 个 tracked 文件全字节一致**」——**那是判错了**：
> workspace 是**开发仓**、publish 是**发布仓**，`Dockerfile.web` / `api/*.py` / `.github/workflows/*`
> 与部分 `docs/*` **本来就按角色不同**，不是数据漂移。项目原本的纪律只针对 `data/` 与线上部署产物。

### 9.1 标准（本阶段起）

| 仓 | 路径 | 分支 | 角色 |
|---|---|---|---|
| workspace | `/opt/data/workspace/Protreptic` | `master` | 编辑语料 / 工具 / 文档 |
| publish | `/opt/data/release/Protreptic-publish` | `origin main` | **线上唯一事实源**，驱动 GitHub Pages |

**凡进入站点构建图或线上站点的文件，必须逐字节一致（sha256）。** 其余文件按角色各自演进。

### 9.2 构建图文件集（怎么推出来的）

| # | 推导依据（发布仓 `.github/workflows/pages.yml`） | 纳入的文件 |
|---|---|---|
| 1 | build job 的 **16** 个 `python3 tools/<x>.py` 步骤 | `tools/` 下 16 个构建脚本 |
| 2 | 这些脚本的本地 import 闭包 | `tools/site_counts.py`、`tools/_quarantine.py`、`tools/credibility_baseline.py` |
| 3 | `on.push.paths` 声明的 `tools/*`（改了就触发发布 = 可能改变线上） | `tools/{prerender_body,og_image,build_pwa_icons,subset_og_font}.py` |
| 4 | CI 门（`ci-cd.yml` 的 test job） | `tools/verify_findings.py` |
| 5 | 上述脚本读的数据 / 资源 | `data/**`、`tools/json/scenarios_{zh,en}.json`、`tools/json/scenario_tags.json`、`tools/scenario_tags.json`、`tools/assets/fonts/**` |
| 6 | `mkdocs build -f mkdocs.pages.yml` | `docs/**`（除 `exclude_docs: archive/`）、`docs_overrides/**`（`theme.custom_dir`）、`mkdocs.pages.yml` |
| 7 | `npm run build`（Vite；`web/public/**` 原样拷进 `dist/`） | `web/**` |
| 8 | 机检脚本自身（随两仓同步，以示自洽） | `tools/check_repo_parity.py` |

实测（2026-09-19 同步后）：**两仓各 1307 个构建图文件，逐字节一致**。

### 9.3 排除的文件与理由（供 QA 复核）

| 排除项 | publish | workspace | 理由（证据） |
|---|---|---|---|
| `data/intl_figures/**` | 637 | 0 | 开发侧原始分片留档；`grep -rIl` 遍 `tools/` + `.github/` + `web/src/` **无任何读取** → 不进构建、不上线 |
| `docs/archive/**` | 34 | 0 | `mkdocs.pages.yml` 的 `exclude_docs: archive/` → 不构建、不上线 |
| `web/dist/**` | 5 | 0 | 前端构建产物（CI 现场 `npm run build`）；发布仓是加 `.gitignore` 之前的历史跟踪 |
| `*.bak*` | 1 | 12 | 备份文件 |
| `data/backup_merge_*/**` | 0 | 10 | 入库前备份目录（开发仓独有） |
| `data/merge_staging_*/**` | 0 | 3 | merge 暂存目录（开发仓独有） |
| `data/all_sources.json` | 0 | 1 | 开发侧汇总实验产物，无构建步骤读取 |
| `data/semantic_index.faiss` | 0 | 1 | 开发侧 FAISS 索引二进制，无构建步骤读取 |
| `tools/gc/gc` | 0 | 1 | 开发侧工具二进制，无构建步骤调用 |
| `web/public/data/**`、`tools/assets/fonts/.cache/**` | 未跟踪 | 未跟踪 | `.gitignore` 已声明（前者由 `export_static_site.py` 现场生成） |
| `api/protreptic.db` | 1 | 1 | CI Step 0 由 `tools/build_figures_db.py` 清表重建（实测两仓 sha 相同，但 committed 内容不进构建结果） |
| `Dockerfile.{api,web}`、`docker-compose.yml`、`api/**`、`.github/**`、`tests/`、`cli_tests/`、`scripts/`、`docs_site/**`、`kanban/`、`release/`、`backups_merge_*/`、根目录遗留副本（`modes_data.json`、`scenarios_*.json`、`code_maps.json`、`three_dimensional_comparison_matrix.xlsx` …） | — | — | **角色性差异 / 非构建图**：构建步骤读的是 `data/**` 与 `tools/**` 下的同名文件（见 `build_figures_db.py::find()` 的候选顺序）；`docs_site/` 是更早的独立文档站工程（`mkdocs.pages.yml` 注释明确不用它）；`.github/**` 两仓编排职责不同（发布仓才有 Pages 触发） |

`pages.yml` 的 30 条 `paths` 触发器里只有 2 条不属于构建图，理由写死在脚本的 `EXCLUDED_TRIGGERS`：
`.github/workflows/pages.yml`（编排本身，两仓职责不同）、`api/protreptic.db`（CI 现场重建）。

### 9.4 机检：`tools/check_repo_parity.py`

```
python3 tools/check_repo_parity.py            # 人读报告
python3 tools/check_repo_parity.py --json     # 机读
python3 tools/check_repo_parity.py --list     # 打印纳入/排除清单（含理由）
退出码：0 = 零差异；1 = 有差异；2 = 边界过期 / 环境不满足
```

- 文件集 = **索引（已跟踪）∪ 未跟踪且未被 `.gitignore`**（Phase39-Z1 起，理由见 §9.4.1）；
- 逐文件 sha256：缺一侧 → `MISSING_IN_WORKSPACE` / `MISSING_IN_PUBLISH`；内容不同 → `CONTENT_DIFF`；
  每条差异都带**侧别 + 理由分类**（未跟踪 / 已跟踪 / 工作树缺失 / 内容不同），
  「并行卡未提交的在制工作」与「真漂移」一眼可分；
- **排除项不静默吞掉**：报告按「排除规则 × 侧别」列出条数与理由（含只在单侧的条数），
  另有硬自检 —— 任何被排除的路径若撞上纳入清单或 `pages.yml` 触发器 → `exit 2`；
- **边界自检**：每次运行现场解析 `pages.yml` 的构建步骤与 `paths` 触发器，若有新增而未被本清单覆盖
  → `exit 2`「边界过期」——边界跟着 workflow 走，不许静默漂移（实测：往假发布仓的 workflow 里加一个
  `python3 tools/fake_new_step.py` 步骤，脚本立刻 exit 2 并点名该步骤）。

#### 9.4.1 盲区与修复（Phase39-Z1）

船长独立核验（2026-09-20）在构建图内造了一个**只在工作仓**的文件 `docs/qa/__parity_probe__.md`，
旧脚本仍输出 `[OK] 零差异：1325 个构建图文件两仓逐字节一致`、`exit 0` —— 未报警。真实事故同型：
`docs/qa/phase38_acceptance.md` 曾只在开发仓、发布仓缺失（phase35/36/37 的报告都在发布仓）。

根因：旧口径只枚举 `git ls-files`（**索引里的已跟踪文件**）。探针与事故文件当时都还是**未跟踪**状态，
根本没进集合，所以「缺一侧」的判定分支形同虚设。同处另有两个小盲区：索引里有但工作树已被删除的文件
（两侧都记 `None` → 被跳过）、符号链接（两侧都记 `None` → 被跳过）。
第四个同族假 OK 路径：本脚本随两仓同步，在发布仓里直接跑（不传 `--workspace`）时默认 workspace
= 脚本所在仓 = publish，两侧同一目录 → 单侧检测恒为 0、输出假 OK；现加硬守卫，撞上直接 `exit 2`。

修复（Phase39-Z1）：
1. 文件集改为 **索引 ∪ 未跟踪且未被 `.gitignore`**，并区分 `tracked` / `untracked`；
2. 符号链接按「链接→目标」取指纹；索引里有而工作树缺失记 `absent`，单列一条理由；
3. 报告新增 `[stats] 两仓都有 N 条（逐字节一致 M）｜仅单侧 K 条` 与「排除规则 × 侧别」表；
4. `--tracked-only` 保留旧口径（诊断用），`--json` 增 `counts.both_sides / only_workspace /
   only_publish`、`untracked_in_boundary`、`excluded_sides`、`excluded_by_rule`。
5. 自比守卫：`workspace == publish`（realpath 比较）→ `exit 2`，不留「自比恒零差异」的假 OK；
6. `tools/test_check_repo_parity.py` 本身也纳入 TOOL_FILES（机检脚本与它的自测不得单侧漂移）。

负对照自测（铁律「任何机检规则都要有负对照测试」）：`tools/test_check_repo_parity.py`，19 项，
用两个临时 git 仓现场复现「只在工作仓（未跟踪 / 已跟踪）」「只在发布仓」「内容不同」
「排除口径不回退」「边界多一步 → exit 2」「排除撞构建图 → 必须报」，并断言旧口径 `--tracked-only`
对同一未跟踪文件 `exit 0` —— 自比守卫（`workspace == publish` → `exit 2`）与「自测脚本本身也在 TOOL_FILES 内」各一项；即盲区确实是「只看索引」造成的。已接进发布仓 `ci-cd.yml` 的 test job。

实测证据（命令 + 原始输出）：`docs/qa/phase39_z1_parity_bidirectional.md`。

### 9.5 同步纪律

1. 内容差异**逐条判角色**，默认以 **publish 为准回灌 workspace**（发布仓是线上唯一事实源，
   且已做个人引用 / 绝对路径清理）；若 workspace 的构建图文件才是新版，反向补进 publish；
2. push 后 `git status -sb` 必须无 `[ahead N]`；
3. 每次同步后重跑机检，必须 `exit 0`。

实测证据（命令 + 原始输出）：`docs/qa/phase37_x4_repo_parity.md`。
