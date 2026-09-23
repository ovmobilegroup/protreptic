# Phase21-R6 A 组·文档归档报告（卡 t_aad01d0e, pigafetta）

- 任务: [Phase21-R6] A组复刻·文档归档（10 页）
- 口径依据: `docs/research/legacy20_rev6_assessment.md`（§2 子串修正 / §4.1 A 组 / §5 样例 / §7 风险）
- 体例先例: `docs/figures/H-YLS-001.md`、`docs/figures/H-SJM-001.md`（九节档案）；曾子归档（卡 t_6c7e070a: 登记链 + 幂等 + 逐字断言）
- 生成器: `build_legacy20_r6_archive.py`（幂等，内置逐字断言；输出字节可复现）
- 独立验收: `verify_legacy20_r6_archive.py`（独立第二实现，不 import 生成器；含反向注入自检）
- 证据: `docs/research/phase21r6_archive_evidence.json`（页面 sha 台账 / 归档件 sha / 冻结时点 / parity / 镜像回执）
- git 提交: `__GIT_COMMIT__`；发布仓镜像: `__MIRROR_STATE__`

## 一、任务与范围

A 组 10 件（CHB 陈伯达 / CY 陈云 / DYC 邓颖超 / FXT 费孝通 / JX 纪弦 / KKQ 康克清 / LWH 李维汉 / SQL 宋庆龄 / WL 万里 / YSK 杨尚昆）在 `docs/figures/` 的档案页，以 v6 载荷为唯一真值源转换为九节档案（只读、逐字、零捏造）。
- 范围内（本卡写入）: `docs/figures/H-XX-001.md` ×10（转换装配）；`data/figures/_duplicates/H-XX-001_legacy_docs_page.md` ×8（旧页字节归档，先归档后写入）。
- 范围外（未动）: `data/modes_data.json`、`data/code_maps.json`、`data/scenarios_zh.json`、`data/scenarios_en.json`、`data/scenario_tags.json`、`data/figure_names.json`（主库五面零写入）；`data/figures/H-XX-001.json`、`data/individuals/H-XX-001_modes.json`（载荷零写入）；QA 判据与发布动作属他卡职责。
- 交付: 10 页档案、生成器、独立验收脚本、本报告、证据明细。

## 二、归档前状态（诊断）

A 组 10 件中 8 件存在旧世代档案页（体例不一，共 5 种模板），2 件落盘前即无档案页:

| 件 | 旧页 | 字节 | 旧页首行 | 旧页段式 |
|---|---|---|---|---|
| H-CHB-001 | 有 | 6,770 | `# 陈伯达 (Chen Boda) 思维模式研究报告` | 基本信息/历史地位/核心思想/十项核心思维模式/…（9 段） |
| H-CY-001 | 有 | 15,101 | `# H-CY-001 陈云 人物档案` | 基本信息/核心思维模式/双语场景案例/…（7 段） |
| H-DYC-001 | 有 | 15,894 | `# Phase 20 邓颖超(H-DYC-001)深度研究报告` | 一~十二（12 段，Phase20 深度研究报告体例） |
| H-FXT-001 | 有 | 7,236 | `# 费孝通 (H-FXT-001) — 研究档案` | 基本信息/代表著作/思维模式映射/…（11 段） |
| H-JX-001 | 无 | — | — | — |
| H-KKQ-001 | 有 | 6,533 | `# 康克清 (Kang Keqing) 思维模式研究报告` | 基本信息/历史地位/十项核心思维模式/…（10 段） |
| H-LWH-001 | 有 | 8,249 | `# 李维汉 (Li Weihan) 思维模式研究报告` | 基本信息/历史地位/十项核心思维模式/…（10 段） |
| H-SQL-001 | 有 | 9,334 | `# 宋庆龄 (Soong Ching-ling) 思维模式研究报告` | 基本信息/十项核心思维模式/Phase20 归档/…（11 段） |
| H-WL-001 | 有 | 19,734 | `# 万里（现代）人物档案卡片` | 基础信息/思维操作流程（十步法）/…（9 段） |
| H-YSK-001 | 无 | — | — | — |

（JX/YSK 两件落盘前即无档案页，属首次装配；不建归档件。）

旧页与 v6 载荷的系统性偏差（本卡转换所处理的）: 旧号体系未重编（如 M211、M341、M001 等跨人物重码）、无九节结构、无登记链与 pending 诚实口径、双语引文与场景覆盖不一、类目未归一。

## 三、归档动作（转换规则）

1. 旧页字节归档（先归档后写入）: 8 件旧页整体字节另存至 `data/figures/_duplicates/H-XX-001_legacy_docs_page.md`（未删字节，sha256 登记于页内 §九 与本报告 §八）；JX/YSK 无旧页，不建归档件（页面明示「首次装配」）。
2. 九节装配（字段映射口径，逐页头部同款明示）:
   - 一 历史定位 ← `historical_significance`；二 核心思想 ← `core_thoughts`（无则 `unique_thinking`，逐页标注）；三 十大思维模式 ← `data/individuals/H-XX-001_modes.json` 全字段（定义/原文+EN/出处/关键概念/领域/步骤/案例/现代应用/关联模式/类目/核验/legacy_mode_id 等；YSK 另含思维要诀/现代对照/常见陷阱；WL 另含归属标注）；
   - 四 现代场景应用 ← 场景库 `scenarios_zh`/`scenarios_en`（C-XX-001~010 与 E 版双语）；五 现代应用 ← 各模式 `modern_applications_zh`；六 跨引用 ← `code_maps.figures.H-XX-001.cross_references`；七 标签 ← `tags`；八 独特成就 ← `influence`；九 QA 验收记录 ← 登记链/pending 口径/evidence 原文/缺项登记/计数台账/归档动作。
3. 编号与类目: 模式新号 `M-<COD>-001 ~ 010`（旧号保留于 `legacy_mode_id` 与页面「旧号 … 重编」行）；类目显示归一值 `category`，原值 `category_raw` 同行留证。
4. 诚实口径: 100/100 条 `verification.status=pending` 逐条落页；evidence 原文按件去重后全量落 §九；0 条自称 verified 记录；源档空字段按「（空）」呈现并逐页登记缺项（含头部字段缺、场景缺、模式级空字段）。
5. 未逐条搬迁字段（按现状保真、页面列出字段名）: CHB 1 项（`protreptic_mapping`）；DYC 9 项（`figure_description_zh/en`、`historical_context`、`intellectual_heritage`、`key_contributions`、`major_achievements`、`modern_relevance`、`personal_background`、`thinking_characteristics`）；FXT 2 项（`figure_description`、`figure_description_en`）；KKQ 6 项（`cross_mode_analysis`、`figure_description`、`figure_description_en`、`historical_context`、`modern_relevance`、`protreptic_mapping`）；其余 6 件无。
6. 幂等: 生成器二次运行打印 `IDEMPOTENT`（10 页字节不变）；dry-run 校验为独立验收脚本内置判据之一。

## 四、验证证据

- 逐页断言: **3022 PASS / 0 FAIL**（`verify_legacy20_r6_archive.py`，exit 0）。覆盖: 九节结构与段序/空行；头部全部字段逐字；§三 10 模式全字段逐字（空字段以「（空）」计数核验）；§四 场景双语逐字；§五/§六/§七/§八 逐字；§九 登记链五段（卡号/执行者/提交号）、pending 口径、evidence 原文、缺项登记、计数台账、归档 sha 复核；尾随空白仅来自源档；无三重换行/无替换符/末行换行。
- 反向注入自检: **11/11 捕获**（台账数字篡改、定义逐字篡改、删出处行、伪造 verified 标记、隐藏缺项、删段题、改归档 sha 值、删对照登记行、伪造空引文、清理尾随空格、引文尾字篡改）。
- 冻结时点复核: 8 件归档件 sha256 与冻结提交 `5c3db0cd` 下 `docs/figures/` 旧页 blob 逐字节全等（8/8）；由验收脚本独立经 `git show` 复取核验。
- 幂等复核: 生成器 dry-run 零改写（验收脚本内置复跑）。
- 逐字细节登记: 宋庆龄 2 处 EN 场景描述按源档原样保留尾随空格（保真未清理；验收以「尾随空白仅来自源档值」判据覆盖）。
- 存量差异登记（未裁决，页内 §六/§九 同款标注）: 图档 `cross_references` 与 `code_maps` 同名条目差异——CHB 2/3、DYC 3/3、KKQ 3/3（KKQ 且条数 3→2）；悬空引用——CY → `H-LC-001`、SQL → `H-MZD-001`/`H-ZET-001`（历史存量，合并/QA 已登记）。

## 五、两仓 parity（差数不增）

- 口径: `tools/check_repo_parity.py --json`（工作仓 vs 发布仓，边界内文件）。
- 开工前水位: 8 条 diff（全部为 QA 卡交付物未镜像: `docs/qa/phase21r6_qa_report.md`、`docs/qa/phase21r6_qa_evidence.json`、`docs/qa/phase21r6_qa_gates/` 下 6 件；属他卡职责，本卡未动）。
- 本卡改动峰值: 26 条 = 开工水位 8 + 本卡在制 18（8 页内容差异 + 2 页新增缺件 + 8 件归档件新增缺件；过程中如实登记）。
- 镜像动作: 本卡路径 20 件（10 页 + 8 归档件 + 本报告 + 证据）镜像至发布仓；提交 `__MIRROR_COMMIT__`；推送 main 后 __PUSH_STATE__。
- 收口水位: __POST_PARITY__ 条（开工水位 8；本卡路径全部收敛，差数不增；余量为 QA 卡交付物，建议收尾卡镜像，见 §七）。

## 六、与同批体例对齐

- 九节结构（一 历史定位 至 九 QA 验收记录）与 `docs/figures/H-YLS-001.md`、`docs/figures/H-SJM-001.md` 对齐；头部元数据块（编号/世代/来源/载荷/字段映射/登记链/报告索引/caveats）齐备。
- 与曾子件差异: 曾子为单件「迁移+截断」；本组为 10 件「v6 载荷九节全量装配」，登记链含评估/落盘/合并/QA/归档五段。
- 双语: 原文 EN 引用行与场景 EN 行保留；页面语言以中文为主（同先例）。

## 七、遗留与建议

1. 悬空引用 3 条（`H-LC-001`、`H-MZD-001`、`H-ZET-001` 三处）与 CHB/DYC/KKQ 三件存量 xref 差异——未裁决，建议裁决/修订卡处理。
2. QA 卡 8 件未镜像（parity 余量）: `docs/qa/phase21r6_qa_report.md`、`docs/qa/phase21r6_qa_evidence.json`、`docs/qa/phase21r6_qa_gates/` 下 6 件（`gate_apply_verification_status.txt`、`gate_credibility_gate.txt`、`gate_verify_findings.txt`、`gate_verify_source_links.txt`、`pages_preflight_data.txt`、`parity_json.txt` 诸件）；建议收尾卡统一镜像收敛为 0 条。
3. 100/100 pending 引文与出处核验——核验另立卡（本卡未伪 verified 标记）。
4. 未展开字段（CHB/DYC/FXT/KKQ 共 18 项）——如需页面展示另立卡。
5. 旧页归档件 `.bak` 变体: 曾子先例含 `.bak_zengzi_fix.md` 变体；本组无 `.bak` 变体（单版本）。

## 八、附: 计数台账与 sha 台账

- canonical 计数（逐页 §九 同值）: modes=3271; total=3162; code_maps=212; scenarios_zh=2183; scenarios_en=2183; scenario_tags=7478; figure_names=1083 共七面。
- 页面 sha256（10 件）与归档 sha256（8 件）: 见 `docs/research/phase21r6_archive_evidence.json`（pages 与 legacy_archived 两段）；验收脚本 `--sha-out` 可复算。
- 归档件字节: CHB 6,770 / CY 15,101 / DYC 15,894 / FXT 7,236 / KKQ 6,533 / LWH 8,249 / SQL 9,334 / WL 19,734 字节。
