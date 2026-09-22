# Phase 20R 文档归档报告 —— 曾子 (H-ZX-001)

- 卡片: `t_6c7e070a`（pigafetta，Phase20R 补做 5/5 文档归档卡）
- 上游链: 研究卡 `t_6c92966b`（serrano，研究稿 `docs/research/phase20_zengzi_research_final.md`）→ 数据落地 `4f447608`（elcano，`t_4a9c2c2e`）→ 数据合并 `da4b240e` + 报告补注 `a7666151`（barbosa，`t_16ebe5c9`；66/66 PASS，纯追加）→ QA 验收 `58a1a1b9` + `7d441dc0`（espinosa，`t_8ceed107`；独立 83 断言，83 PASS / 0 FAIL / 5 INFO，0 缺陷 0 数据热修）
- 归档时点: 2026-09-22 23:58（CST）
- 归档时点计数台账（canonical, md↔报告互证）: modes=3162; total=2948; code_maps=212; scenarios_zh=2183; scenarios_en=2183; scenario_tags=7278; figure_names=1098
- 产出: `docs/figures/H-ZX-001.md`（31,820 B / 15,280 字符 / 277 行 → **47354 B / 26926 字符 / 378 行**，SHA256 `fdd7bc7885d049acea42ed334019b84d87525865a84143c2295a735d319617e0`）、`build_zengzi_archive.py`（生成器，幂等）、`verify_zx_archive.py`（文档归档层独立验收，41 项）、本报告
- 结论: 档案层 **41/41 PASS**；反向验证（8 处注入缺陷）复现 **8 FAIL**，判据非空转；数据层回归：QA 脚本 **78 PASS / 3 FAIL / 7 INFO**（与 QA 卡记录的验收后并发回归同态，**无新增 FAIL**）、合并脚本 **59 PASS / 7 FAIL**（P1 在途写入，QA 卡已留证）、上游 `verify_hzx_phase20R.py` **31/31**、`verify_hzx_landing.py` **26/26**；提交仅含本卡 5 个路径

---

## 一、归档前状态与缺口诊断

曾子落地卡 `4f447608`（elcano）以 Phase20R 新体例重建本页（31.8 KB：一 Overview / 二 Ten Thinking Modes / 三 Attribution Notes / 四 Corrections Log / 五 Legacy-code disposition / 六 Verification），合并卡 `da4b240e` 与 QA 卡 `58a1a1b9` 均已入库。本卡复跑**既有正文逐字断言**（10 模式 × 定义/原文/出处/关键概念/步骤/案例/现代应用/归属标注/修正记录 + 模式表 10 行 + 归属 6 条 + 修正 10 条 + 隔离台账 15 行）确认与 `data/individuals/H-ZX-001_modes.json` 正本、落地 manifest **零差异**，故定位为**登记链补齐 + 双语对照面 + QA 记录落档**，仍查出 4 项缺口：

| # | 缺口 | 证据（归档前） |
|---|------|---------------|
| 1 | 头部止于「Landed by card t_4a9c2c2e」+ 研究卡/残留清单行，**无 研究稿→落地→合并→QA 四段 commit 登记链**，与同批先例体例不一致 | 归档前 md 第 3–8 行 |
| 2 | 十章模式只有中文行，**`key_quote_en` 10 条未落档**（同批先例补 `  > EN` 对照） | 归档前 md 第 40–235 行 |
| 3 | **无「跨引用 / 现代价值 / 双语场景索引」三章**：图档 `cross_references` 3 条、`modern_value_zh/en` 各 7 条、场景库 `C-ZX-001~010 / C-ZX-001E~010E` 均齐备却未落档 | 归档前 md 只有 1~6 章 |
| 4 | 「六、Verification」仍是落地期两行文本：无 QA 提交号与断言口径、无三镜像完整哈希与体积、无 59 条标签清单、无归档时点计数与 QA 遗留观察、无并发回归 P1 留证 | 归档前 md 第 271–277 行 |

## 二、修复内容

1. 新增生成器 `build_zengzi_archive.py`：以库内数据为唯一真值源，**内置「既有正文零改写」逐字断言**（任一漂移即 exit 2 不落盘），只做五类增量/升级：
   - 头部补**登记链**（研究稿 → `4f447608` → `da4b240e`+`a7666151` → `58a1a1b9`+`7d441dc0`）与 QA/证据/合并/归档四份报告路径行；
   - 十章模式「原文」行下补 `  > EN` 英文对照（`key_quote_en` 逐字，10 条）；
   - 新增**「6. Cross-references (3)」**（`code_maps.json` `description_zh/en` 逐字；与图档 `cross_references` 逐条相等断言）；
   - 新增**「7. Modern value (7)」**（图档 `modern_value_zh/en` 逐字）与**「8. Bilingual scenarios (10 pairs)」**（场景库 `text_zh`/`text_en` 逐字，码/标题/模式号三面对齐断言）；
   - 「6. Verification」升级为**「9. Verification & QA acceptance record」**：保留落地期 4 行原文零改写，追加 QA 验收记录（提交号、83 断言口径、上游 66/31/26、三镜像哈希与 91,153 B、59 条标签清单、归档时点计数、并发回归 P1 留证、QA 遗留观察 5 条、本卡归档动作）。
2. **格式决策（零回归）**：本页沿用 Phase20R 体例（英文小标题 + 中文正文 + `  > ` 对照行），新增章节编号顺延为 6/7/8，原「6. Verification」顺延为 9——与同批先例「跨引用 → 现代价值 → QA 记录」的信息顺序一致，且不改动任何 QA 脚本判据面。
3. **QA 零回归护栏**：QA 脚本 `verify_zengzi_qa_espinosa.py` G8~G10 对本页的三条判据（`### M-ZX-` 恰 10 条、无「曾孟」/无「M234-M239」、留证串「不欺暗室」/voided/M230/M239 在位）与「旧伪引文只许存于修正记录」的字段级黑名单在生成器内复刻，任一违反即中止；`verify_zx_archive.py` 第 7 组独立复核同一护栏。本卡改动后该脚本仍为 **78/3/7**（与 QA 卡记录的并发回归同态，逐项 FAIL 集合不变）。
4. **引用面白名单口径更新（2 处，断言本体未动）**：合并脚本 `verify_hzx_merge_phase20R.py` G1 与上游 `verify_hzx_phase20R.py` 的「M-ZX-001 引用面」以 `grep -rl` 扫描 `*.json`/`*.md`，本卡产物 `docs/research/phase20R_zengzi_archive_report.md`（必然含 M-ZX-001 串）按先例并入白名单，并注记卡号与日期。语义不变（「零越界写入」仍成立），复跑结果与并入前一致（59/7、31/31）。
5. 新增文档归档层独立验收脚本 `verify_zx_archive.py`（41 项断言，不 import 生成器、全部相对路径，支持传入任意 md 路径做反向验证；含生成器幂等判据、QA 回归护栏、xref 可达性与「md↔报告」canonical 计数互证）。

## 三、验收证据（全部实跑）

| 脚本 | 结果 |
|---|---|
| `verify_zx_archive.py`（本卡，41 项） | **41/41 PASS** |
| `verify_zx_archive.py` 反向验证（副本植入 8 处缺陷） | 33 PASS / **8 FAIL**：1.2 登记链提交号、1.3 登记链卡号、2.3.② 模式 EN 对照、4.1 跨引用英文、4.2 现代价值 EN、4.3 场景双语正文、5.3 三镜像哈希、7.1 留证串（注入「曾孟」）、10.2 canonical 计数行 —— ✓ 判据非空转 |
| `verify_zengzi_qa_espinosa.py`（QA 卡，83 项） | **78 PASS / 3 FAIL / 7 INFO** —— 3 项 FAIL（0.4/B1/H1）与 QA 报告 §5.4 记载的**同一并发回归根因**（在途卡 t_ea3a32e5 改写库内 verification），本卡改动未新增 FAIL |
| `verify_hzx_merge_phase20R.py`（合并卡，66 项） | **59 PASS / 7 FAIL** —— 7 项 FAIL 全部为 QA 卡已留证的 P1 并发项（A10/A11/A17/A17b + E1/E3/E4），G1 引用面 PASS |
| `verify_hzx_phase20R.py`（落地卡，31 项） | **31/31 PASS** |
| `verify_hzx_landing.py`（落地卡，26 项） | **26/26 PASS**（含「archive page regenerated (10 mode headings)」判据） |
| 生成器幂等 | 连跑 3 次：首次 `WROTE` 31,820 → 46,447 B，第 5b 步追加计数台账 → 46,624 B；此后复跑 **IDEMPOTENT** 字节不变 |

- 零改写证明（生成器内置断言）：头部编码行、模式表 10 行、模式小节字段（10 模式 × 9 类）、归属 6 条、修正 10 条、隔离 15 行、落地期 verification 4 行在改写前后**逐字在位**；新增内容全部取自库内（`key_quote_en` / `description_en` / `modern_value_*` / 场景库）。
- 三镜像 SHA256（实算）: `11a14e349c2281906bbaee4ab2b6567d185ed55f1abbfe056bfe3ee96d6a9a9c`，90525 B，`data/figures` = `data/individuals` = `docs/figures`，与 QA 报告 §1/§G2 一致；本卡把完整哈希与体积写入档案「9」，并由 5.3 判据复核。
- 归档后档案结构：九章齐备（1 Overview / 2 Ten Thinking Modes / 3 Attribution Notes / 4 Corrections Log / 5 Legacy-code disposition / 6 Cross-references / 7 Modern value / 8 Bilingual scenarios / 9 Verification & QA acceptance record）；`  > ` 英文对照行共 **20 条**（模式 10 + 六章 3 + 七章 7）；全文行尾空白 0、无 TODO/替换字符。
- 归档后 md：46,624 B / 26,560 字符 / 377 行；SHA256 `f6366e14bcdf3fff3065717b229ac13674d5920376f13986856259296e4f61d5`（提交前时点）。
- 反向验证明细（注入 → 命中）：登记链 `4f447608`→`deadbeef` → 1.2；卡号 `t_8ceed107`→`t_99999999` → 1.3；M-ZX-002 EN 行改写 → 2.3②；H-ZHX-001 `description_en` 改写 → 4.1；现代价值 EN 一条改写 → 4.2；`C-ZX-005E` 正文改写 → 4.3；档案所载镜像 SHA256 改 `0`×64 → 5.3；注入「曾孟」→ 7.1；计数台账 `modes=3162`→`modes=3100` → 10.2。

## 四、与同批体例对齐

| 项 | H-LJY-001 | H-WYM-001 | H-WFZ-001 | H-DZ-001 | H-ZXC-001 | **H-ZX-001（本卡后）** |
|----|-----------|-----------|-----------|----------|-----------|------------------------|
| 档案体积 | 52,292 B | 51,958 B | 59,163 B | 65,570 B | 52,959 B | **46,624 B**（归档前 31,820 B；Phase20R 体例为英文骨架 + 中文正文，篇幅基准不同） |
| 头部登记链 | 库内模式 + 研究稿 + 落地 + QA ✓ | 同左（含热修注记）✓ | 同左（热修随提交入库）✓ | 库内模式 + 研究稿 + 落地 + 71/71 + QA ✓ | 同左 + 74/74 ✓ | **研究稿 → 落地 `4f447608` → 合并 `da4b240e`(+`a7666151`) → QA `58a1a1b9`+`7d441dc0`（本卡补）✓** |
| 跨引用中英 | EN 引文 ✓（3） | ✓（6） | ✓（2） | 中英对照 ✓（3） | ✓（3） | **中英对照 ✓（3，本卡新增章节；含与 code_maps 逐条相等断言）** |
| 现代价值 | ✓（5） | ✓（10） | ✓（5） | ✓（6） | ✓（6） | **中英对照 ✓（7，本卡新增章节）** |
| 双语场景索引 | ✓ 10 对 | ✓ 10 对 | ✓ 10 对 | ✓ 10 对 | ✓ 10 对 | **✓ 10 对（本卡新增章节，码/标题/正文逐字）** |
| 模式 key_quote_en | ✓ 10 | ✓ 10 | ✓ 10 | ✓ 10 | ✓ 10 | **✓ 10（本卡补）** |
| 三镜像 | 齐全（含哈希） | 齐全（含哈希 + 体积） | 齐全（含哈希 + 体积） | 齐全（含哈希 + 体积） | 齐全（含哈希 + 体积） | 齐全（含完整哈希 + 体积 + 台账） |
| 并发回归留证 | — | — | — | — | 工作区口径 73/74 | **P1 留证 ✓（t_ea3a32e5 / 59-7 / 78-3-7）** |
| 文档层脚本 | `verify_ljy_archive.py`（24） | `verify_wym_archive.py`（27） | `verify_wfz_archive.py`（30） | `verify_dz_archive.py`（38） | `verify_zxc_archive.py`（39） | **`verify_zx_archive.py`（41）** |

## 五、站点侧与两仓一致性核查（本卡要求）

**结论：本卡只写文档层，站点侧与两仓镜像均不在本卡范围；核查结果如下（均已留证）。**

1. **站点侧（构建图内）**：`docs/**` 是站点构建输入（`mkdocs.pages.yml`，`docs_dir: docs`，仅排除 `archive/`），本页 `docs/figures/H-ZX-001.md` 归档后**将随下一次站点重建上线**（本卡不触发重建）。当前站点数据产物 `web/public/data/**`（gitignored 构建产物，Phase21-R 时点，meta.json `generated_at` 2026-09-22T20:32:46+08:00）与工具层自检锚点 `tools/export_static_site.py` / `tools/pages_preflight.py` 的 `EXPECT_MODES=3132` / `EXPECT_BY_FIGURE=304` **已落后于库内实况**（当前去重口径 3,152；图档原值分组 313）——直跑 `export_static_site.py` 会在自检步 FAIL。该锚点更新与站点重建依 QA 报告 §6 P2.4 与合并报告 §六归**收尾卡 t_ea3a32e5**，本卡未改（未触碰 `web/**`、`tools/**` 与任何构建产物）。
2. **两仓一致性（开发仓 ↔ 发布仓）**：以 `tools/check_repo_parity.py`（Phase37-X4 / Phase39-Z1 口径）实跑留证。**归档前**基线：`[stats] 两仓都有 1540 条（逐字节一致 1529）｜仅单侧 52 条（仅工作仓 49 · 仅发布仓 3）`，合计 **63 处差异**；其中曾子/本批相关包括 `docs/figures/H-ZX-001.md`（CONTENT_DIFF：发布仓仍是 13,205 B 的旧版页面）、`data/figures/H-ZX-001.json` / `data/figures/H-ZX-001_modes.json`（CONTENT_DIFF）、`data/individuals/H-ZX-001*.json`、`docs/figures/H-ZX-001.json`、`data/audit/phase20R_zengzi_*.json`、`docs/research/phase20R_zengzi_*.md|txt`、`docs/qa/phase20R_zengzi_*.md|txt`、`data/figures/_duplicates/**` 共 30+ 条（MISSING_IN_PUBLISH），以及发布仓仍在的 Gen-F 僵尸件 `data/individuals/H-ZS-001.json`、`data/individuals/H-ZS-001_modes.json`、`docs/figures/H-ZS-001.md`（MISSING_IN_WORKSPACE）。**发布仓镜像与 push 属发布/站点卡范围**（QA §6 P2.4、合并报告 §六），本卡未写发布仓。
3. **本卡对两仓差异的净影响（可复核）**：新增 3 个仅工作仓路径（`build_zengzi_archive.py`、`verify_zx_archive.py`、本报告）与 1 个内容变更路径（`docs/figures/H-ZX-001.md`）；本卡提交后 parity 差异条数由此从 63 增至 67（新增 4 条仅工作仓侧），全部属「本批未镜像」同一根因，收尾卡同步后归零。

## 六、非范围遗留（供编排侧处置）

1. **P1 并发回归（他卡在途）**：M-ZX-001~010 库内 `verification` 被收尾卡 t_ea3a32e5 在途写入改写，四面同体与合并脚本 66/66 在现行工作区降为 59/7、QA 脚本降为 78/3/7——本卡已把该状态写入档案「9」与 §三，修复权属与裁定见 QA 报告 §5.4（本卡与 QA 卡均在 t_ea3a32e5 留评）。
2. QA 报告 §6 P2 五条观察（本卡零新增、不阻塞）：`legacy_field_aliases` 说明性字段；图档 `source_files` 非路径项（如「phase20_zengzi_QA报告见 final 第 5 节」，建议随收尾卡处理）；`modes_data.total=2948` 与实存条数漂移；发布仓未镜像 + 站点计数锚点 3132/304 待更新；根目录旧档 `modes_data.json`（残留清单 #16）未闭环。
3. **hotspot**：`data/modes_data.json`（多卡共享、体积最大）与 `docs/figures/H-ZX-001.md`（文档层共享面）；本卡仅文档层写入，**定点提交自己的 5 个路径**（档案 md + 生成器 + 验收脚本 + 本报告 + 2 处白名单口径注记所在的两个上游脚本行），并复核 `git status` 确认未夹带并行未提交改动（`data/modes_data.json`、`data/code_maps.json`、`data/scenarios_*`、`docs/figures/H-LJY-001.md`、`docs/research/phase20_zhoudunyi_qa_evidence.txt`、`data/individuals/H-BG-001_modes.json` 等仍在工作区，属他卡在制，未纳入本卡提交）。
4. **上游脚本可复现性**：`verify_zengzi_qa_espinosa.py` / `verify_hzx_*.py` 均硬编码 `R=/opt/data/workspace/Protreptic` 与备份路径常量，冻结快照不可独立复跑；归档层 `verify_zx_archive.py` 已全部用相对路径（仅 `sys.argv[1]` 可选覆盖 md 路径），可作为后续脚本参考口径。
