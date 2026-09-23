# Phase21-W5 引文落源 pilot · 全链档案报告（卡 t_25453b39；W5 链尾·文档归档）

- 执行：pigafetta ｜ 日期：2026-09-24（CST=UTC+8）｜ 工作仓：/opt/data/workspace/Protreptic（master）｜ 发布仓：/opt/data/release/Protreptic-publish（origin `main`，GitHub=ovmobilegroup/protreptic）
- 链：A `t_5a7abc92`（研究）→ B1 `t_f09365bb`（工具）→〔链前置收口 `t_9f3ccb2c`〕→ B2 `t_fdc1589e`（主库落地；外部门控 `t_ff294775`）→ C `t_28e8ab2b`（独立 QA）→ D 本卡 `t_25453b39`（九节档案 + 登记链）
- 本卡边界：零数据/主库改动（不写 `data/**`、`tools/**`、`web/**`）；只做文档层收口与登记；上游产物按原样对待（未改一字节）。
- 关键判定留存：**QA 总判定 = FAIL**（详见 §六）；本报告按实况如实归档，不修饰、不代改。
- 时点：本卡 claim 2026-09-24 05:33:55（CST）；v1 装配/提交/镜像/push 回执见 §四.6；v2 回执补记见文末附录。
- 标注约定：`[实测-本卡]` = 本卡现场命令/文件实测；`[引述]` = 转引上游报告（均给来源）；`[未闭环]` = 待修复/待裁定项（§七）。

---

## 一、概述

本报告是 Phase21-W5「引文落源」pilot 链的**全链归档**：把成本链（研究 → 工具 → 主库落地 → 独立 QA → 文档归档）的目标、产物、判定、残留与下一步，按 git 对象、盘上文件与工具原始输出逐条登记，供后续修复卡、Stage 2 决策与站点面复核引用。

**结果摘要（全部可溯源，详见 §四/§五/§六）：**

1. **交付面成立**：《论衡》书级链接入索引（curl 200、canonical=論衡）；raw 原文缓存修复（120k 截断 → 265,821 字符 / 85 篇齐）；繁简归一缓存（raw + zh-cn 转换副本双轨）与 D4 扩能（含 U1–U4 负对照）；王充 `M-WC-001~010` 状态收口（9 verified + 1 suspect，19 条翻转）；门禁三连全绿；push 主体成立。以上均经 QA 复验成立（QA §1.1/§1.5/§1.6 与 §4 列表）。
2. **QA 判定 FAIL**：6 项复验 = 3 项 PASS、2 项部分 PASS、1 项 FAIL；不一致项 10 条（真差异 6 / 口径差 4）。核心失败面：① 落地卡声称的 10 条引文处置（改字/省略号/换尾/篇目/字段规范化）**均未落盘**（数据侧唯一变化 = verification 状态翻转）；②《论衡》zh-cn 转换副本元数据被 `fixidx.py` 硬写为 `complete=true/failed_chunks=0`（实际含 3 段未转换块），且 D4 实际采用了该副本（006/008/009 结论链依赖之）；③ 多处报告数字与 git 实况不符（§4.2 四态表、附录 B SHA、§1③、evidence `wc_after`）。6 条必须修正项待路由（§六.3 / §七）。
3. **本卡收口动作**：QA 产物 2 件（报告 + 证据 JSON）镜像发布仓；本报告装配、提交、镜像、push；两仓 parity 复核；台账（backlog）追加登记。§9 收口与数据修复**均不在本卡**（前者属船长既定动作、后者需修复卡，见 §四.3 / §七）。
4. **pilot 结论**：技术面（索引/缓存/D4/负对照/门禁）成立；**程序面因 QA FAIL 未闭环**，修复项关闭前不达「pilot 通过线」（§六.6）。Stage 2（68 本）推进为船长决策点（§八.3）。

---

## 二、背景

### 2.1 pilot 动机与根因（[引述] 设计文档 §1）

- 设计文档：`/opt/data/cache/phase21w5_citation_pilot_design.md`（船长案，2026-09-23）；判定时全库模式 3281 条（含在途 R8 合并态），`verification` 四态中 unresolved-pending **1122 条 / 230 人物**。
- 根因（代码+数据双证）：Y1 扩面候选的计数口径 = 原始跨度（含章节后缀）、每条目内去重（`tools/build_source_links.py:282` 的 `extract_refs` 不归并书级）→《论衡》书级被引 30 次、篇章跨度无任一 ≥3 → 从未成为候选、从未探源 → 王充 10 条恒为 unresolved。解析侧本支持章节→书级回落，**不对称只在候选生成侧**；全网书级被引≥3 缺索引 68 本皆属此类。
- canary 选定 H-WC-001 王充：10 条 `M-WC-001~010` 全 unresolved；《論衡》zh.wikisource pageid 44377、子页 01–85 全文可读（实测 /09 /28 /60 /61）；含繁简差异样本（/28「（迢）〔追〕難孔子」）。pilot 两处扩能 = 繁简归一缓存 + D4 扩能（转换层可关闭、必须带负对照）。

### 2.2 卡链与时序（[引述] 派发记录 + [实测-本卡] git 时间）

- 派发记录：`/opt/data/cache/scratch/phase21w5_dispatch.json`（A/B1/B2/C/D + external_parent=t_ff294775）；2026-09-23 22:07–22:08 点火。
- 时序（CST）：A 于 23:23 交付三档报告（[引述] 船长 worklog 23:5x 轮）；B1 提交 `dea899a0` 00:36:18 / `cb8601a1` 00:42:44；船长 01:40 轮取证发现「链前置收口未做 + 工作区 source_texts 为再生窄版」，派 `t_9f3ccb2c` 补交（`a92c92d4` 01:37:52 + `bd039538` 01:59:47；done 02:00:40）；外部门控 `t_ff294775`（R8 AZJ 复验）03:21:59 done，基线 `40f69521`；B2 工作仓 `18405015` 04:16:49 + `e25569b7` 04:27:18，发布仓 `5a1b934` 05:02:08 + `fde0d0f` 05:06:27，done 05:06:40；C QA 05:06:49 点火、`8b61385b` 05:33:00 提交、05:33:21 done；本卡 05:33:55 claim。
- 外部门控：B2 开跑前须等 `t_ff294775`（AZJ 链尾）done——主库单写者纪律（`t_fdc1589e` 开工时为当时唯一写 `data/modes_data.json` 的卡）。

### 2.3 pilot 通过线（[引述] 设计 §5）

①《论衡》条目 curl 200 + canonical 核实、缓存 coverage=complete；② 10 条逐条三档结论与见证定位；③ 王充 10 条四态不再 unresolved、`apply_verification_status --check` exit 0、门禁 `--hard-fail` 无新增；④ 两仓 parity 零差异、报告含 before/after 数字与全部原始证据；⑤ 负对照：真实差异仍被抓（迢→追 与注入案例）。对照见 §六.6。

---

## 三、方法

### 3.1 取证原则（本卡）

- **只读为主**：本卡不改 `data/**`、`tools/**`、`web/**`；所有结论取自 git 对象、盘上文件、工具现跑输出与远端现抓。
- **git 优先**：提交/镜像/回执以 `git rev-parse`、`git show`、`git log`、`git ls-remote`、`git cat-file` 实侧为准；不采信报告自述（QA 同口径：「不采信任何自述」）。
- **现跑取证**：`tools/check_repo_parity.py --json`、`tools/apply_verification_status.py --check`、`verify_wangchong_pilot_qa_espinosa.py`（QA 第二实现）、live curl 等均在本卡现场执行并留输出（见 §五）。
- **双人复核链**：上游数字凡本卡引用，均在「来源」栏注明出处；凡本卡能低成本直测者（四态、翻转、sha、parity、live），一律直测复核（§六.4）。

### 3.2 记录口径

- 时间统一 CST（UTC+8）；sha256 默认给前 16 位（全文核对时给足 64 位或两版本对照）。
- 三类标注：`[实测-本卡]` / `[引述]` / `[未闭环]`；不修饰、不伪修、不做无证据表述。
- 数字冲突处理：以可复现实侧为准；冲突本身作为条目登记（§六.5）。

### 3.3 收口与登记方法

- 镜像 = byte-exact 拷贝（`cp`）+ 发布仓白名单提交（只 `git add` 明列路径）；push 后 `ls-remote` 复核远端 HEAD。
- 台账登记 = append-only 追加（不改写船长既有行）；不改结构。
- 先例：QA 产物镜像与报告补全按 R8 王祥链（`t_a8f544f5`）/罗瑞卿链（`t_d9cb98bb`）体例；仓根脚本不入镜像面（罗瑞卿 §六/王祥 §五先例）。

---

## 四、执行

### 4.1 全链登记表（卡号 · commit · 回执，[实测-本卡]）

| 段 | 卡（执行者） | 工作仓提交（master） | 发布仓镜像（main） | push / 远端复核 | 备注 |
|---|---|---|---|---|---|
| A 研究 | `t_5a7abc92`（serrano） | 交付 2 件无自提交（报告自述「无 git 提交」）；2 件 + 见证 271 件由链前置收口卡补交于 `a92c92d4` | `d4456ab` | `a15d89c..d4456ab`（见左） | 三档：逐字命中 2 / 差异 5 / 查无 3（[引述] sourcing §一） |
| B1 工具 | `t_f09365bb`（elcano） | `dea899a0`（缓存双件首提）+ `cb8601a1`（报告补提）→ 补交 `a92c92d4`（tools 4 件、source_links 入键、source_texts 合并 96→97、tooling.md 补全） | `d4456ab` + `c32f669` | 同下 | 负对照 U1–U4 通过；test_credibility_d45 37/38（Z7 存量） |
| 链前置收口 | `t_9f3ccb2c`（elcano） | `a92c92d4` + `bd039538`（回执补记） | `d4456ab` + `c32f669` | push `a15d89c..d4456ab`、`70631cc..c32f669`（rc=0） | done 02:00:40；source_texts 96→97 零丢失 |
| 外部门控 | `t_ff294775`（espinosa） | `40f69521`（AZJ 复验 QA pair §9 追加） | `ef982d7` | push `de1b0eb..ef982d7` | W5 基线=40f69521；见证器 18/18 PASS（[引述]） |
| B2 主库落地 | `t_fdc1589e`（barbosa） | `18405015`（9 件）+ `e25569b7`（3 件） | `5a1b934`（11 件）+ `fde0d0f`（1 件） | ls-remote origin/main = `fde0d0f`（[实测-本卡]；两笔均含于 HEAD 祖先） | done 05:06:40；§9 未提交 → R1[未闭环] |
| C 独立 QA | `t_28e8ab2b`（espinosa） | `8b61385b`（3 件 / 913 insertions） | 本卡镜像（P1，§四.6） | 见 §四.6 | 总判定 FAIL（§六.1/6.2） |
| D 文档归档 | `t_25453b39`（pigafetta，本卡） | WS1 + WS2（§四.6） | P1 + P2（§四.6） | push1 + push2（§四.6） | 本报告 |

- 注 1：A/B1 交付物实际入仓由 `t_9f3ccb2c` 统一补交（船长 01:40 轮裁定的收口补交路径）；`a92c92d4` 单笔含 A1 报告 2 件 + 见证目录 271 件 + tools 4 件 + source_links/source_texts 变更 + tooling.md 补全，名单外 0 件、零 `modes_data` 改动（[引述] 提交信息）。
- 注 2：发布仓「11 件 / 1 件」为 `git show --stat` 实侧（`5a1b934` 11 文件、`fde0d0f` 1 文件）；落地报告 §6.1 镜像表列 11 行且未列 `phase21w5_wangchong_status.json`（后者实为第 12 件、两仓已一致 `78d1b24c`）——口径差已由 QA #10 登记。
- 注 3：全链提交完整 sha（40 位）：`a92c92d45871a14a6f5c338409279c457eae00ae` / `bd03953802cc7d18548e7c6cc780e05eb5acb38f` / `dea899a0f2991740919b2d64bf1581cf726e1891` / `cb8601a1f6b9a9d96ab69568ee3758a6e62c2850` / `184050155c40f8275476992a9485ff1a5a8f0732` / `e25569b78ee9634ac078b003be33b3d0e87ad831` / `40f69521770d60a7269497361146d42857022b57` / `8b61385b4bbccb0318da6aa04f55c15b26575b4c`；发布仓 `ef982d73bf3ed061271d49c8e715df1a00ec9750` / `d4456ab93efe5c273c5b6a621e52749d736a2746` / `c32f66955a6fb996e546b531f1e26812c1feda07` / `5a1b934735b72f463bfc605fd256f21264fc9807` / `fde0d0fca926e2ee184abebf7dcd37c47e07be07`。

### 4.2 本卡动作（时序）

1. **全链取证（只读）**：git 对象与回执、关键文件 sha256、parity 快照、`apply_verification_status --check`、QA 第二实现复跑、live 现抓（→ §五）。
2. **文档层收口**：QA 产物 2 件 byte-exact 镜像发布仓；本报告装配（含全链 commit/卡号登记、QA FAIL 与残留登记）。
3. **提交/镜像/push**：WS1/P1/push1；v2 回执补记 WS2/P2/push2（→ §四.6 / 文末附录）。
4. **台账登记**：backlog append-only 追加（→ §四.5）。
5. **复核**：parity 终测、远端复核（→ §五.3/§六）。

### 4.3 §9 状态登记（本卡未动）

- **磁盘版**（工作区未提交）= HEAD + 15 行（新增「## 9. Push 回执（最终）」节），mtime 2026-09-24 05:06:40，sha256 `697be08952e1c76b…`（[实测-本卡]）。
- **提交版**（`e25569b7`）与**发布仓版**逐字节一致，sha256 `22163920987aca29…`（[实测-本卡] 两处分别实测，cmp 一致——QA 亦已 cmp 验证）。
- QA #7（口径差）：§9 未提交/未镜像 → parity `CONTENT_DIFF=1`；且「远程SHA：`5a1b934…`」标注与远端 HEAD（`fde0d0f`）不符；QA 建议「提交并镜像 + 更正标注」。
- 船长既定处置（[引述] backlog 条目 + 计划文件）：`/opt/data/cache/scratch/phase21w5_section9_fix_plan.md`（2026-09-24 05:17:48 拟）——「QA done 后船长最简收口（commit+镜像+push）」；计划内注「§9 内容按 barbosa 落地版原样提交，不加工」。
- **本卡处置：未动**（归属船长既定动作，避免竞态/重复提交）→ 记为 R1[未闭环]。

### 4.4 站点/展示层（本卡判定：不涉及新增）

- 本卡自身不新增站点面变更。W5 的站点面变化（站点计数 3221×318、`docs/index.md`、`docs/02-tools/figure_library.md`、两 manifest）已由 B2 随 `5a1b934`/`fde0d0f` 镜像+push，并经 QA §1.5 与船长 05:55 轮复核（Pages run 35919916554 success；live meta `generated_at=2026-09-23T21:08:47Z`）。
- 本卡现抓复核（[实测-本卡]）：live 首页 HTTP/2 200；live `manifest.webmanifest` 载「3221 条思维模式 × 318 位历史人物」；live `data/meta.json` HTTP 200（3,563 B；published verified=949）。
- docs 层（含本报告与 QA 产物）属站点构建图（`mkdocs.pages.yml`；`exclude_docs: archive/`）：本卡按先例补齐镜像；镜像 push 触发 Pages 重新部署属预期。
- 脚本面：`verify_wangchong_pilot_qa_espinosa.py` 为仓根件、不进站点构建图 → 按先例**不镜像**。
- 两仓 parity 复核（收口后重测）：见 §五.3。

### 4.5 台账登记（②）

- 既有台账**存在**：`/opt/data/cache/protreptic_work_backlog.md`（船长工作循环维护；另有 `protreptic_worklog.md`）。本卡按 **append-only** 追加「W5 链尾·文档归档登记」块（报告 sha、镜像/push 回执、parity 时点、§9 归属与 R 项指引），不改写既有行。
- 派发记录：`/opt/data/cache/scratch/phase21w5_dispatch.json`（A/B1/B2/C/D + external_parent）。

### 4.6 本卡提交与推送回执（v1/v2）

- 镜像集（3 件 byte-exact）：`docs/qa/phase21w5_wangchong_qa_report.md`、`docs/qa/phase21w5_wangchong_qa_evidence.json`、`docs/research/phase21w5_wangchong_archive_report.md`（本报告）。
- v1 轮：WS1（工作仓，报告 1 件）＋ P1（发布仓，3 件）＋ push1；v2 轮（回执补记）：WS2 ＋ P2 ＋ push2。
- 精确 sha / push 区间（v1 值见文末 v2 补记；v2 值见本卡完成回执 metadata：`ws_commit_v1/v2`、`publish_commit_v1/v2`、`push_v1/v2`、`remote_main`）。
- 提交署名：magallanes（沿用先例）。

---

## 五、证据

### 5.1 关键文件 sha256（前 16 位；[实测-本卡] sha256sum / git cat-file）

```
d9de42a077644035  data/modes_data.json
00c183c0a89f1a26  data/audit/findings.json（=提交版=发布仓版）
c4aba5ff870f375e  data/audit/source_texts.json
b310f36fcfe8d0f1  data/audit/source_texts/6f2e2e4e124df80a.txt
3ec20b26e42c03b8  data/audit/source_texts/6f2e2e4e124df80a.zh-cn.txt
78d1b24caf067086  data/audit/phase21w5_wangchong_status.json（两仓一致，已对测）
54e9a88edc2e7f56  docs/research/phase21w5_wangchong_landing_evidence.json（两仓一致，已对测）
697be08952e1c76b  docs/research/phase21w5_wangchong_landing_report.md（工作区磁盘版：含未提交 §9）
22163920987aca29  docs/research/phase21w5_wangchong_landing_report.md（提交版=发布仓版）
baee6321a0c0172e  docs/qa/phase21w5_wangchong_qa_report.md（32,903 B / 343 行）
26aca060d60baf0f  docs/qa/phase21w5_wangchong_qa_evidence.json（10,102 B）
23e79944c5ee8ab2  verify_wangchong_pilot_qa_espinosa.py（仓根件；不进镜像面）
ba569fe301358549  docs/research/phase21w5_wangchong_sourcing_report.md
1c3384149b39d549  docs/research/phase21w5_wangchong_sourcing_report.json
8fb2c9e21e2f17c8  docs/research/phase21w5_tooling.md
```

### 5.2 git 三版本对照（[实测-本卡]，基线列 [引述] QA §A.5）

| 文件 | 40f69521（基线） | HEAD=e25569b7（终稿，本卡实测） | 落地报告附录 B 声称 | 判定 |
|---|---|---|---|---|
| data/modes_data.json | 2d3eb9ea… | **d9de42a0 77644035** | d9de42a0 77644035 | ✓ |
| data/audit/findings.json | 26d166ab… | **00c183c0 a89f1a26** | f994b48e 135ef353 | ✗（非基线亦非终稿；R4/NEW-1） |
| data/audit/source_texts.json | affdd781… | **c4aba5ff 870f375e** | affdd781 37e3fedf | ✗（=基线值） |
| …/6f2e2e4e124df80a.txt | 3a13c805… | **b310f36f cfe8d0f1** | 3a13c805 e7a8f7be | ✗（=基线值） |
| …/6f2e2e4e124df80a.zh-cn.txt | 9faa22c5… | **3ec20b26 e42c03b8** | 9faa22c5 171c7c2c | ✗（=基线值） |

### 5.3 两仓 parity 快照（`tools/check_repo_parity.py --json`）

- 本卡开工时（[实测-本卡]）：status=DIFF；workspace_in_boundary 2281 / publish 2273 / both 2273 / identical 2272 / only_workspace 8 / only_publish 0；差异 9 条 =
  - MISSING_IN_PUBLISH ×8 = QA 2 件（本卡收口对象）+ W4/W6 他链 6 件（`phase21r8_w4_names_recon.*`、`phase21w4_fix_manifest.*`、`phase21w6_marker_scan.*`）；
  - CONTENT_DIFF ×1 = landing report（§9 未提交 → R1）。
- 记账说明：船长 05:45/05:55 轮报「7 差异 = 6 他链 + 1 §9」——其扫描早于 QA 产物入工作仓索引（QA 提交 `8b61385b` 05:33:00），故未计 QA 2 件；口径差已消。
- 收口后终测：见文末 v2 补记（QA 2 条消除；余 = 6 他链 ± §9 1 条）。

### 5.4 `apply_verification_status --check` 现跑（[实测-本卡]，exit 0）

```
四态（全库 3291）: verified 949 / pending 1939 / suspect 52 / unverifiable 351
四态（公开 3231）: verified 949 / pending 1907 / suspect 35 / unverifiable 340
S1 交 S2 重叠: 25；与库中现状态相比的变更: 无（已一致）
[OK] 自洽断言（求和/回查 URL 146 个）；[OK] --check 逐条一致
```

### 5.5 本卡独立直测（只读脚本；输出存 scratch）

- 四态与翻转（`flips2.py`/`flips_check.py`，git 对象直读）：基线 `40f69521` = {931,1958,51,351}（sum 3291）→ HEAD `e25569b7` = {949,1939,52,351}（sum 3291）；翻转 **19 条**逐条：M-WC-001~008/010 pending→verified、M-WC-009 pending→suspect、M-WX-001/002/004~010 pending→verified（M-WX-003 不变）。
- M-WC 逐条（`mwc_check.py`）：001~008/010 = verified/link-resolved（evidence=论衡书级 URL）；009 = suspect/auto-scan（D4/D5 hit）；`checked_at` 全量 2026-09-24。
- 字符计数：raw `wc -m` = 265,821；zh-cn 副本 = 265,712；见证目录 271 件（含 zh-hans-body 86 项）。

### 5.6 站点/线上现抓（[实测-本卡]）

- live 首页 HTTP/2 200；live `manifest.webmanifest` = 「3221 条思维模式 × 318 位历史人物」；live `data/meta.json` HTTP 200（3,563 B；`generated_at=2026-09-23T21:08:47+00:00`；`verification.published.verified=949`；figures=1056）。

### 5.7 QA 侧证据（本卡复跑第二实现；[实测-本卡]）

- `verify_wangchong_pilot_qa_espinosa.py` 本卡复跑：**OK 9 / REPRO 13 / WARN 0 / UNEXPECTED 0，exit 0**（与 QA 卡记录一致；REPRO = 发现项仍在，属预期信号）。
- 门禁（[引述] QA §1.5/§1.6）：credibility_gate --hard-fail exit 0（存量 524 冻结、D4 matched 4 / mismatch 24 / quote-too-short 81 / unchecked 3202）；verify_findings 165 条 0 hard/1 warning；U1–U4 负对照与注入全绿。
- D4 副本采用：substring-found(zh-cn copy)=2 / not-found=1（006/008 matched、009 mismatch——QA 与本卡复跑均复现）。

---

## 六、核验

### 6.1 QA 复验逐项（[引述] QA §0–§1）

| 项 | QA 判定 | 要点 |
|---|---|---|
| 1 《论衡》索引行与引用解析 | **PASS** | curl 200；《论衡·问孔》→ 书级 URL（prefix）；canonical=論衡 |
| 2 原文缓存与转换副本 | raw 侧 **PASS** / 副本完整性与元数据如实 **FAIL** | raw 265,821 字符、85 篇、现抓 6 篇 18/18；副本 3 段回退块 24,000 字符 + 旗标被硬写 |
| 3 M-WC-001~010 独立复算 | **PASS**（复算）/ **FAIL**（处置落盘） | 与 A1 三档一致；10 条处置未落盘（全库 diff=仅 verification） |
| 4 四态 | **PASS**（工具一致）/ **FAIL**（报告/证据数字） | --check 0 漂移；§4.2 after 求和 3259≠3291；19 条翻转含 M-WX 9 条未登记 |
| 5 门禁、parity、push | **PASS**（附口径差 3 条） | 三连 exit 0；11 件 byte-exact；§9 CONTENT_DIFF=1；远端 HEAD=fde0d0f |
| 6 负对照复跑与注入 | **PASS** | U1–U4 + 本卡注入全按设计 |

- 登记注：§0 概数为「3 PASS / 2 部分 PASS / 1 FAIL」；上表 2/3/4 为混合判定项，概数与逐项的映射报告未逐条绑定（本卡按各节标题与 QA 卡 handoff `check_items` 登记）。

### 6.2 不一致项 10 条（[引述] QA §2 表列；可逐条溯源 QA §附录 A）

| # | 项 | 类别 | 严重度 |
|---|---|---|---|
| 1 | 10 条处置未落盘（引文/篇目/字段） | 真差异 | 高 |
| 2 | zh-cn 副本旗标硬写 + 被 D4 采用 | 真差异 | 高 |
| 3 | §4.2 四态表/evidence/§8 数字 | 真差异 | 高 |
| 4 | 附录 B SHA 4/5 行不符实测 | 真差异 | 中 |
| 5 | §1③「M-WC-002 可核为 mismatch」不实（实为 quote-too-short） | 真差异 | 中 |
| 6 | evidence `wc_after` 005/007/010 记 pending（实为 verified） | 真差异 | 中 |
| 7 | §9 未提交/未镜像 +「远程SHA」标注 | 口径差 | 低 |
| 8 | §4.1 verify_source_links 行时点过时 | 口径差 | 低 |
| 9 | M-WX-001/002/004~010 共 9 条翻转未登记 | 口径差 | 低 |
| 10 | 杂项（§6.1 计数、evidence 键名、时区、tee 残留行） | 口径差 | 低 |

- 登记注：QA 报告 §0/§1.5 概数记「口径差 3 条」，§2 表列 4 条；QA 卡 handoff 记「10 条 = 真差异 6 + 口径差 4」。本表按 §2 表列登记（R8）。

### 6.3 必须修正项 6 条（[引述] QA §3.2；路由状态 = 本卡登记）

1. 【口径二选一，高】实施 or 如实改述 10 条处置 —— **R3[未闭环]**（裁定权：船长）
2. 【zh_cn 元数据如实 + 重跑，高】—— **R2[未闭环]**（修复卡）
3. 【数字修订，高】§4.2/§8/附录 B/§1③/wc_after/时区 —— **R4[未闭环]**（修复卡）
4. 【§9 提交与镜像 + 标注更正 + M-WX 登记，中】—— **R1/R5[未闭环]**（§9=船长；登记=修复卡）
5. 【杂项清单，低】—— **R6[未闭环]**
6. 【工具侧建议，低】failed_chunks 写口断言；D4 多片段语义评估 —— **R7[未闭环]**

### 6.4 数字一致性核对（本卡逐条直测；与上游报告数字对照）

| 数字/事实 | 来源 | 本卡复核手段 | 判定 |
|---|---|---|---|
| 四态 HEAD {949,1939,52,351} | QA §1.4 / avs | avs 现跑 + git 直测 | ✓ |
| 基线存储 {931,1958,51,351} | QA §1.4 | git cat-file 40f69521 直测 | ✓ |
| 公开口径 {949,1907,35,340} | QA §1.4 | avs 现跑 | ✓ |
| 19 条翻转明细 | QA §1.4 | 直测 19 条逐条一致 | ✓ |
| 9 verified + 1 suspect（M-WC） | 落地/QA | 直测逐条一致 | ✓ |
| raw 265,821 字符 / 85 篇 | 落地 §3 / QA | wc -m + 见证计数 + QA 现抓 18/18 | ✓ |
| 副本 3 段回退块 / 残留証 3 处 | QA #2 | QA 脚本本卡复跑（REPRO 复现） | ✓ |
| 站点 3221×318 / live verified 949 | 落地 §6.2 / 船长 | live 现抓 | ✓ |
| 附录 B 4 行 SHA | 落地 §附录B | 实测不符（§5.2） | ✗（R4） |
| §4.2 表 after 求和 3259≠3291 | 落地 §4.2 | 复现（R4） | ✗ |
| wc_after 005/007/010=pending | landing evidence | 实况 verified（R4） | ✗ |
| status.json inputs.finding sha | （QA 未列） | 实测不符 f994b48e vs 00c183c0 | ✗（NEW-1） |

### 6.5 本卡复核新增登记项（QA 未覆盖）

- **NEW-1（低）**：`data/audit/phase21w5_wangchong_status.json`（两仓 byte-exact `78d1b24c`）中 `inputs.data/audit/findings.json.sha256 = f994b48e135ef353…`，与终稿实测 `00c183c0a89f1a26…` 不符——该错值同时存在于落地报告附录 B、landing evidence 与 QA 引用处，status.json 为第 4 处载体；QA 仅核其计数自洽（§1.4 注），未核 inputs 节。→ 归入 R4 修复范围。
- **NEW-2（低）**：QA 报告 §0 概数「9 条（真差异 6 / 口径差 3）」与 §2 表列 10 条（口径差 4）不一致（本卡逐行计数 §2=10 行；QA 卡 handoff 亦记 10）。→ R8。

### 6.6 pilot 通过线对照（[引述] 设计 §5 + 本卡实测）

| # | 通过线 | 实况 | 判定 |
|---|---|---|---|
| 1 | curl 200 + canonical + coverage=complete | QA #1 PASS；raw coverage complete、85 篇 | ✓ |
| 2 | 10 条三档 + 见证定位 | 三档齐、复算一致；但「处置」未落盘（R2/R3） | △ |
| 3 | 四态收口 + check exit 0 + 无新增硬失败 | 10 条不再 unresolved；均成立（M-WX 登记缺=R5） | ✓ |
| 4 | parity 零差异 + before/after 数字 | 数字不符（R4）；parity 余 6 他链 + §9（R1） | ✗ |
| 5 | 负对照全绿 | U1–U4 + 注入全绿 | ✓ |

**综合：未达通过线（与 QA 总判定 FAIL 一致）。**闭合 R1–R5 后方可复核通过（§八）。

---

## 七、残留（R 清单；路由与闭合状态）

- **R1【§9 未提交/未镜像】**（中；归属：船长既定动作）：工作区 +15 行「Push 回执（最终）」；提交/镜像/推送按 `phase21w5_section9_fix_plan.md` 执行；QA 建议顺带更正「远程SHA」标注（与船长「原样不加工」存在口径差，裁定权归船长）。闭合后 parity CONTENT_DIFF 归零（余他链 6 件）。
- **R2【zh_cn 元数据旗标被硬写】**（高；需修复卡）：`complete=true/failed_chunks=0` vs 真值 `false/3`（3 段回退块 24,000 字符；D4 实际采用之，006/008/009 结论链依赖）。恢复旗标后 3 条结论需重跑/降级，`suspect=52` 与公开口径需重算。
- **R3【10 条处置未落盘】**（高；需修复卡 + 船长口径裁定）：先定「实施 or 如实改述」，再决定改数据还是改报告叙述。
- **R4【数字/SHA 修订】**（中；需修复卡）：§4.2 四态表/§8 行/附录 B×4/§1③/wc_after×3/时区/§6.1 计数 + 本卡 NEW-1（status.json inputs）。含 QA #10 杂项中的计数项。
- **R5【M-WX 9 条副作用未登记】**（低；需修复卡）：19 条翻转仅登记 10 条；建议与王祥链（`t_a8f544f5`）对账后补登记。
- **R6【杂项】**（低）：evidence 键名 `D4_empty_quote`（=D4_quote_without_source）、tee 残留行（两仓镜像件同步）、§6.1「9 个文件」口径。
- **R7【工具侧建议】**（低）：① 缓存件写口加断言（`failed_chunks>0` 不得置 complete）；② D4 多片段语义评估。属 `tools/` 面，修复卡或后续轮评估。
- **R8【QA §0 概数 vs §2 表列】**（低；本卡复核登记=NEW-2）：建议修复轮顺带统一为 10 条（真差异 6 / 口径差 4）。
- **R9【status.json inputs.finding sha 滞后】**（低；本卡复核新增=NEW-1）：并入 R4 修复范围。
- **R10【他链 parity 残差=6 件】**（他链，非本链）：W4/W6 报告待镜像（`phase21r8_w4_names_recon.*`、`phase21w4_fix_manifest.*`、`phase21w6_marker_scan.*`）；由相应链收口，不属本卡。
- 本卡边界内未做事项（明示）：不做任何数据/主库变更；**未创建跟进卡**（修复路由归船长裁定，见 §八.1）；未触碰 §9 未提交改动；未评价 QA 结论之外的数据修复方案。

## 八、下一步

1. **修复路由（建议，供船长裁定）**：优先序 ①口径二选一（R3）→ ②zh_cn 恢复 + 重跑（R2，含 006/008/009 复核、suspect/公开口径重算）→ ③数字/SHA/status.json 修订（R4/R8/R9）→ ④杂项与登记（R5/R6）→ ⑤工具侧评估（R7）。建议拆「数据修复卡（R2/R3）+ 文书修订卡（R4–R9）」或单卡串行；均由船长派发。
2. **§9 收口（船长）**：按 `phase21w5_section9_fix_plan.md` 执行（commit → 镜像 → push）；先裁「标注更正 or 原样」。
3. **pilot 状态与 Stage 2**：pilot 未达通过线；Stage 2（68 本）推进前建议先闭合 R2/R3（影响可核性稳定性）；是否带病推进为船长决策点。
4. **链后放行**：本卡 done 即放行 W4 执行卡 `t_536073f4`（W4 链），其后为 W6/W7 链——与 W5 修复并行不冲突（单写者纪律照旧）。

## 九、附链

### 9.1 卡号索引（本链一处可查）

| 卡号 | 角色 | 执行者 | 终态 |
|---|---|---|---|
| `t_5a7abc92` | A 研究（三档） | serrano | done 23:23 |
| `t_f09365bb` | B1 工具/缓存 | elcano | done（交付转补交） |
| `t_9f3ccb2c` | 链前置收口补交 | elcano | done 02:00:40 |
| `t_ff294775` | 外部门控（R8 AZJ） | espinosa | done 03:21:59 |
| `t_fdc1589e` | B2 主库落地 | barbosa | done 05:06:40 |
| `t_28e8ab2b` | C 独立 QA | espinosa | done 05:33:21 |
| `t_25453b39` | D 文档归档（本卡） | pigafetta | 进行中→本报告交付 |

（下游：`t_536073f4` 起 W4 链，另见船长编排。）

### 9.2 文档与证据路径

- 设计/派发/计划：`/opt/data/cache/phase21w5_citation_pilot_design.md`；`/opt/data/cache/scratch/phase21w5_dispatch.json`；`/opt/data/cache/scratch/phase21w5_section9_fix_plan.md`；台账 `/opt/data/cache/protreptic_work_backlog.md`、`/opt/data/cache/protreptic_worklog.md`。
- 报告：`docs/research/phase21w5_wangchong_sourcing_report.md/.json`（A）；`docs/research/phase21w5_tooling.md`（B1）；`docs/research/phase21w5_wangchong_landing_report.md` + `docs/research/phase21w5_wangchong_landing_evidence.json` + `data/audit/phase21w5_wangchong_status.json`（B2）；`docs/qa/phase21w5_wangchong_qa_report.md` + `docs/qa/phase21w5_wangchong_qa_evidence.json`（C）；本报告（D）。
- 证据面：`data/audit/source_texts/**`（raw 85 + zh-cn 85）；见证 `docs/scratch/phase21w5_wangchong/witness/**`（271 件）；复现脚本 `verify_wangchong_pilot_qa_espinosa.py`；本卡 scratch `/opt/data/profiles/pigafetta/cache/scratch/w5arch/`（parity_now.json、avs_check.txt、qa_verify_rerun.txt、mwc_check.py/flips*.py）。
- 站点面：`docs/index.md`、`docs/02-tools/figure_library.md`、`web/public/manifest*.webmanifest`。

### 9.3 复现命令（本卡实际执行）

```
git -C /opt/data/workspace/Protreptic log --oneline -12
git -C /opt/data/workspace/Protreptic rev-parse <sha>…
git -C /opt/data/workspace/Protreptic cat-file blob 40f69521:data/modes_data.json | python3 …
python3 tools/check_repo_parity.py --json
python3 tools/apply_verification_status.py --check
python3 verify_wangchong_pilot_qa_espinosa.py
sha256sum data/modes_data.json data/audit/findings.json …
git -C /opt/data/release/Protreptic-publish ls-remote origin main
curl -s -o /dev/null -w '%{http_code}' https://ovmobilegroup.github.io/protreptic/
```

### 9.4 先例与体例参照

- 曾子 `t_6c7e070a`（Phase20R 归档）、R6 王祥 `t_557aeac1`+`t_a8f544f5`、罗瑞卿 `t_d9cb98bb`、AZJ `t_a8f544f5` 链：九节体例、QA 产物镜像、脚本不入镜像面。
- 本报告新增：QA FAIL 态全量登记（不修饰）+ 本卡复核 NEW-1/NEW-2（QA 未覆盖项）。

