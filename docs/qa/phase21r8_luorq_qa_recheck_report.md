# Phase21-R8 罗瑞卿链 QA 尾项 复验报告（卡 t_65998945）

- 卡: t_65998945（espinosa）—— 「[Phase21-R8 罗瑞卿链 QA 尾项] 场景面复验（补交后）＋QA 产物入库＋镜像＋push」
- 上游链: QA t_8773cb6b（done, 103 PASS / 12 FAIL / 17 INFO）→ 收尾补交 t_2d15bd2e（done, 0cbf6ab6 / a119ad9c）→ 文档归档 t_d9cb98bb（done, 63a0e463 / 408f7ebf / e8b5c12e）
- 边界: 只读复验为主；**零数据改**（未改六件数据、未碰他卡在途件、未引用被验收方自述作结论）
- 生成: 2026-09-24（CST）；本报告 v1 为主提交（§1~§8），v2 为回执补记（§9）

## 1. 基线与复验窗口

| 项 | 值 |
|---|---|
| 工作仓 | /opt/data/workspace/Protreptic（master，dir 工作区） |
| 复验窗口 | 2026-09-24 01:25 ~ 01:53（Run A/B/C 三跑） |
| Run C 时点工作仓 HEAD | a92c92d45871（porcelain 46 行） |
| Run C 时点发布仓 HEAD | d4456ab93efe（porcelain 0 行） |
| 远端 | origin/main = 以 §9 回执为准（git ls-remote 实测） |

窗口内他卡提交推进（如实登记，不属本卡）：t_a8f544f5（王祥链收尾 b004ec01 / P1、4cbde565 v2）、t_9f3ccb2c（W5 收尾 a92c92d4）等。
本链数据面不受影响：K6 复测（工具实算）确认六件数据 工作树 == HEAD == 0cbf6ab6 提交 == merge manifest.after，且 0cbf6ab6..HEAD 数据路径 0 提交。

链内提交（以 git 对象实算为准）：
- 0cbf6ab6（t_2d15bd2e #1，21 件）→ 发布仓 ec0a06b（39 件）
- a119ad9c（t_2d15bd2e #2，4 件）→ 发布仓 fee63a3（4 件）
- 63a0e463（t_d9cb98bb，5 件）→ 发布仓 2b3681d（3 件；根工具 2 件按该卡声明边界不镜像）
- 408f7ebf / e8b5c12e（t_d9cb98bb v2/v3）→ 发布仓 58a45cb / 04837b3

## 2. 预检：t_2d15bd2e 终态核实（K 系列，19 项全 PASS）

脚本：`verify_luorq_chain_recheck_espinosa.py`（第二实现；结论一律取 git 对象 / 远端 ref / 文件实算，不引用被验收方自述）
证据：`docs/qa/phase21r8_luorq_qa_recheck_evidence/chain_commits_verify.json / .txt`

| 判据 | 结论 | 实测 |
|---|---|---|
| K1 提交文件集 == 声明白名单 | PASS | 0cbf6ab6 = 21 件，名单外 0 / 缺失 0 |
| K2 提交 × 镜像逐件字节相等 | PASS | 21/21（ec0a06b）、4/4（fee63a3）、3/3（2b3681d） |
| K3 镜像侧新增件与工作仓对应件 byte-exact | PASS | 18/18（A1 落盘包随链收敛） |
| K4 回执表 sha256 == git 实算 | PASS | 21/21（工作仓表）、39/39（镜像表） |
| K5 push 回执 | PASS | 远端 main 含 ec0a06b / fee63a3 / 2b3681d（ancestry 实测） |
| K5b 工作仓 master push | PASS（环境事实） | 远端仅 refs/heads/main，无 refs/heads/master |
| K6 零数据改动 | PASS | 六件数据 工作树==HEAD==0cbf6ab6==manifest.after；数据路径 0 后续提交 |
| K7 文档归档页 | PASS | docs/figures/H-LUORQ-001.md 两仓 byte-exact（sha256 17cb095e… / 64,447 B / 426 行） |
| K8 两仓 parity 复测 | 见 §9 | 本卡 QA 产物面 0 残留（镜像后复跑为准） |

## 3. 场景面复验：原 12 FAIL 逐条处置

三跑口径（证据互不覆盖）：
- **Run A** `runA_prefix_judge/`（判据修正前，补交后状态，含门禁）：108 PASS / 14 FAIL —— 用于复现原 FAIL 并定位归因；
- **Run B** `runB_judge_v2/`（F1~F5 修正后，含门禁）：116 PASS / 6 FAIL —— 中间态（A07 省略号片段残余）；
- **Run C** 本目录 `result.json/.txt`（F1~F6 完整修正后，含门禁）：**118 PASS / 4 FAIL** —— 本卡复验结论。

Run C 残留 4 FAIL = A05×3（口径差异议，见下）+ G01c（在制件未入库/未镜像，属运行态、由 §9 镜像后 parity 回执闭环）。

| # | 原 FAIL（run1） | Run A | Run B | Run C | 处置 | 证据（Run C 实测） |
|---|---|---|---|---|---|---|
| 1 | A03 M-LUORQ-004 引文见证 0 件 | FAIL | PASS | PASS | 判据修正闭环 | 强归一化命中原件 xuoba/ch064.txt（W20/ch064） |
| 2 | A03 M-LUORQ-005 引文见证 0 件 | FAIL | PASS | PASS | 判据修正闭环 | 命中原件 xuoba/ch054.txt（W20/ch054） |
| 3 | A05 M-LUORQ-004 source_chapter 无书名号 | FAIL | FAIL | FAIL | 异议（口径差，交链主） | 见 §8-1 |
| 4 | A05 M-LUORQ-005 同 | FAIL | FAIL | FAIL | 异议（口径差） | 见 §8-1 |
| 5 | A05 M-LUORQ-008 同 | FAIL | FAIL | FAIL | 异议（口径差） | 见 §8-1 |
| 6 | A07 引号片段越界（×2） | FAIL | FAIL | PASS | 判据修正闭环 | 两片段按省略号切段后逐段见于素材包 json（W20/ch053「民警…」；ch063「郭兴福教学法…」） |
| 7 | B01 W15 sha 不一致 | FAIL | PASS | PASS | 判据修正闭环 | W15 注册行 sha256 693329e6… == 本地副本实算；19/19 见证件全命中 |
| 8 | B05 白名单 2 条不可回溯 | FAIL | PASS | PASS | 判据修正闭环 | 两条逐字见于素材包 json（boundary W8 / core 四环闭环） |
| 9 | C_ScenExist 场景 zh=0/en=0 | FAIL | PASS | PASS | 判据修正闭环 | 实测 zh=10 / en=10（内层字典） |
| 10 | E03a 同 | FAIL | PASS | PASS | 判据修正闭环 | zh=10 |
| 11 | E03b 同 | FAIL | PASS | PASS | 判据修正闭环 | en=10 |
| 12 | G01b 镜像清单悬空 19 | PASS | PASS | PASS | **门禁跑通即闭环** | 19 件待镜像项全部可归属（在差异清单或已同步），0 悬空 |

小结：原 12 FAIL 中 **9 条经判据修正后闭环（数据面实证通过）**、**3 条（A05×3）为口径差异议**（本卡不改数据，交链主裁定）。

**run1 结论修正登记**：run1 对 C/E 的「merge 未落地」归因不成立——run1 时点工作树已是合并后态（E01=3291 / E04a LUORQ 标签 20 / E06=1083 均为 run1 实测），C/E 恒 0 系嵌套结构判据缺陷（对补交前/后均恒 0），与合并落地无关。run1 其余结论（D 段、H 段、E01/E02/E04~E09、B02~B04 等）复验维持。

## 4. 判据修正 v2（F1~F6，已固化进脚本并在证据登记）

| # | 判据 | 缺陷（修正前） | 修正 |
|---|---|---|---|
| F1 | A03 见证路径 | `W20/ch064` 章号取错组（用 W 组号 → xuoba/ch20.txt 不存在） | 改用 ch 组号（xuoba/ch064.txt） |
| F2 | B01 注册解析 | 跨行非贪婪正则：W14 行无 sha256 → 吞并后行 W15 的 sha，「W15 未登记」假象 | 行域解析（行内 **Wxx** + 行内 sha256） |
| F3 | A07 扫描面 | 仅 md §三 quotes；json quotes.text 来源片段误报越界 | 扫描面扩展至素材包 json |
| F4 | B05 回溯面 | 同上（json core/boundary 条目误报缺失） | 同上 |
| F5 | C/E/G02 场景面 | 场景字典为嵌套结构，原扫顶层键恒 0 | 下钻内层字典 scenarios_zh/en |
| F6 | A07 省略号片段 | 整段子串匹配，带「……」的片段恒不命中 | 按省略号切段、逐段追溯 |

修正影响与纪律：修正前口径证据（run1，t_8773cb6b）**冻结保留**于 `docs/qa/phase21r8_luorq_qa_evidence/`（未改动）；修正后复验证据为本目录。修正不改数据、不放松数据面要求（均为把「按声明口径应扫到而没扫到」改成「扫得到」），并把修正前后两态都留证（Run A vs Run B/C）。

## 5. 链内提交产物复核

见 §2（K 系列 19/19 PASS）。附加登记：
- t_d9cb98bb 根工具 2 件（`build_luorq_r8_archive.py` / `verify_luorq_r8_archive.py`）未镜像发布仓——该卡报告内明示「仓根工具不进构建图、按 parity 边界不镜像」，属已声明边界，非漂移；本卡如实登记。
- ec0a06b 镜像 39 件 = 白名单 21 件 + A1 落盘包 18 件；K2/K3 全量逐件 byte-exact 通过（无抽查）。

## 6. 门禁与两仓 parity 回执

Run C 门禁复跑（同仓库状态，完整日志见 `phase21r8_luorq_qa_recheck_gates/`）：
- F01 credibility_gate --hard-fail exit 0
- F02 verify_findings --hard-fail exit 0
- F03 verify_source_links --hard-fail exit 0（活链复扫）
- F04 apply_verification_status --check：exit=1 如实登记（非硬门禁，按设计）
- F05 pages_preflight --stage data exit 0
- F06 gen_web_site_counts --check exit 0

F03 时点性登记：Run A/B 时点 F03 exit=1（新增坏链《申辩篇》→ zh.wikipedia 500/慢响应，非本链）；Run C 同一门户复扫恢复 exit 0 → 判为时点性（网络/服务端 5xx），非数据面缺陷；如后续复跑再现，移交链接面例行处置。

两仓 parity（Run C）：G01b PASS（0 悬空）；G02a PASS（发布仓 H-LUORQ-001 注册全有，无半截镜像态：fn/cm 在册 + 场景在册）；G01c 运行态 FAIL——差异为**本卡在制件**（QA 证据/门禁未入库未镜像，运行中必然存在）→ 由 §9 镜像后 parity 复测闭环。G01 差异总数 96，95 条为非 LUORQ 面他卡在途（主为 data/backup_phase21r8_azj345_clear_20260923/** 清档卡 t_3669eb4a 在制等），逐条登记于 result.json G01 段。

## 7. QA 产物入库（工作仓提交）

以王祥 QA（ae72a7d2）先例为口径：evidence + gates + selftest + 脚本 + 报告。入库件目（44 件 = 清单 43 件 + 清单自身；含两跑证据与 K 系列证据）：
- 脚本 2 件：`verify_luorq_qa_espinosa.py`（含 v2 判据修正 F1~F6）、`verify_luorq_chain_recheck_espinosa.py`
- run1 产物（t_8773cb6b 冻结件）5 件：`docs/qa/phase21r8_luorq_qa_evidence/result.{json,txt}`、`docs/qa/phase21r8_luorq_qa_gates/gate_{credibility_gate,verify_findings}.txt`、`docs/qa/phase21r8_luorq_qa_selftest.json`
- 复验产物：`docs/qa/phase21r8_luorq_qa_recheck_evidence/**`（Run C 结果 + Run A/B 冻结 + K 系列证据）、`docs/qa/phase21r8_luorq_qa_recheck_gates/**`、`docs/qa/phase21r8_luorq_qa_recheck_selftest.json`、本报告
- 不入库：`_inject_tmp/`（H06 注入派生件 24MB×2，可复算，已清理）；精确 SHA 清单见 §9 与 `artifacts_sha256.json`

## 8. 异议与遗留清单

1. **A05×3（口径差，交链主裁定）**：M-LUORQ-004/005/008 的 `source_chapter` 为讲话/会议/事件类来源、无书名号，严格口径（书名号+年份）下不达。依据：库内 682/3174 条同类（无书名号）、同链 王祥/黄宗羲 10/10 亦无年份、链内门禁自计 `no-citation=3`（phase21r8_luorq_gate.txt）。建议 (a) 增口径说明认可事件类来源；或 (b) 链主裁定后另开补正卡（本卡按「不改数据」不动作）。
2. run1 结论修正登记（C/E ×3 归因），见 §3 小结。
3. 注入临时件 `_inject_tmp/`（×2，24MB）不入库：可复算（重跑脚本自动重建），已清理以免 parity 面残留（只清本链 QA 临时件）。
4. 他卡在途（不属本卡范围）：AZJ-345 清档（t_3669eb4a/t_ff294775）、W5 链、王祥链收尾（t_a8f544f5）——parity 差异逐条归属，如实登记。
5. F03 时点性坏链（《申辩篇》）登记，见 §6。

## 9. 回执补记（提交 / 镜像 / push / parity）

（v2 补记）
