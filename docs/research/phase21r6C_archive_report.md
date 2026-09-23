# Phase21-R6C 归档报告：C 组 7 件（卡 t_4a9cf2cb）

- 日期：2026-09-23
- 依据：docs/research/legacy20_rev6_assessment.md（§4.3 C 组裁决、§2 子串修正、§7 编号预案）；先例：docs/qa/phase21r2_cleanup_report.md（R2 清档）
- 边界：主库 modes_data.json 零写入（合并卡负责）；发布仓镜像由合并卡统一收敛；本卡提交仅本卡路径。

## 一、结论摘要

- 7 件全部清档：22 个字节件（data 19 件 + docs 3 页）移入 data/figures/_duplicates/（R2 先例命名），逐件 sha256 登记，未删字节。
- 自件登记撤下：figure_names 9 键、code_maps 3 条目、scenarios_zh+en 各 30 条（逐字留档，见证据文件与 removed_registrations.json）。
- 罗瑞卿载荷隔离归档（串档防复用）+ 另立项说明（docs/research/phase21r6C_luorq_isolation_note.md）。
- 待权威身份清单 6 件：本报告第五节 + docs/research/phase21r6C_pending_identity.json。
- 映射账本：data/audit/phase21r6_id_mapping_ledger.tsv/.json（A 100 + B 32 + C 78 = 210 行）；全库查重复核见第六节。
- 线上可见变化：3 个 docs 页撤下（第四节）；站点计数链不受影响（C 组不在 figures 计数链内）。
- 核验：verify_phase21r6C_archive.py；活跃层复扫逐条登记（第八节），核验断言零未登记残留。

## 二、归档明细（7 件 × 22 字节件）

### H-AN-001（安子）

- 载荷摘要：旧号 M001-M010（10 个）；载荷 10 条
- 裁决/处置：归档；若保留另立研究卡（assessment）
- 归档件 sha256（前 8 位）：figures 3c3f110c；individuals 4f6bf0e4；modes 724b705a；docs 页 326145b3

### H-LC-001（陆沉）

- 载荷摘要：旧号 M401-M410（10 个）；载荷 10 条
- 裁决/处置：归档；若保留另立研究卡（assessment）
- 归档件 sha256（前 8 位）：figures ff985b80；individuals 66bd05b4；modes 4816fc61

### H-YE-001（叶筱）

- 载荷摘要：旧号 M401-M410（10 个）；载荷 10 条
- 裁决/处置：归档或整卡替换（assessment）
- 归档件 sha256（前 8 位）：figures cb1929d3；modes c7f9ecdd

### H-ZOU-001（邹文献）

- 载荷摘要：旧号 M401-M410（10 个）；载荷 10 条
- 裁决/处置：归档；若保留另立研究卡（assessment）
- 归档件 sha256（前 8 位）：figures 646bb167；modes 509da08f；docs 页 1efbd7b5

### H-HAN-001（沈幅）

- 载荷摘要：旧号 M351-M358（8 个）；载荷 8 条
- 裁决/处置：归档；若保留另立研究卡（assessment）
- 归档件 sha256（前 8 位）：figures 83b882fd；individuals f79d8392；modes d508cbac

### H-MODERN-002（大云）

- 载荷摘要：旧号 M001-M010（10 个）；载荷 10 条；元数据虚标 10（无载荷）
- 裁决/处置：归档或立项（assessment）
- 归档件 sha256（前 8 位）：figures 54247df5；individuals 4653ccbf；modes 165aca69

### H-LUORQ-001（罗瑞卿）

- 载荷摘要：旧号 M311-M320, M351-M360（20 个）；载荷 10 条；载荷内容为陆有（串档，隔离归档）
- 裁决/处置：载荷隔离归档，另立项重做研究（assessment）
- 归档件 sha256（前 8 位）：figures bb2a6a2a；individuals 4713aace；modes 9b0dc237；docs 页 3fa3aa3f

完整 sha256、字节数与逐件源/目标路径见 docs/research/phase21r6C_archive_evidence.json（archives 段）。

## 三、登记层撤下（自件；逐字留档）

### figure_names.json（9 键）

| 键 | 值 |
|---|---|
| H-AN-001 | 安子 |
| H-HAN-001 | 沈幅 |
| H-LC-001 | 陆沉 |
| H-LUORQ-001 | 罗瑞卿 |
| H-MODERN-002 | 大云 |
| H-YE-001 | 叶筱 |
| H-ZOU-001 | 邹文献 |
| HAN | 沈幅 |
| Han | 沈幅 |

### code_maps.json（3 条目）

- H-LUORQ-001：mode_ids 10 个（M351 至 M360）；cross_references 有（随条目撤下）
- H-MODERN-002：mode_ids 10 个（M001 至 M010）；cross_references 有（随条目撤下）
- H-ZOU-001：mode_ids 0 个（无）；cross_references 无

### scenarios_zh.json / scenarios_en.json（各 30 条，按 figure_id 扫描撤下）

- data/scenarios_en.json：H-LUORQ-001 共 10 条（键名 C-LUORQ-001E 至 C-LUORQ-010E）
- data/scenarios_en.json：H-MODERN-002 共 10 条（键名 C-MODERN-002E-001 至 C-MODERN-002E-010）
- data/scenarios_en.json：H-ZOU-001 共 10 条（键名 C-ZOU-001 至 C-ZOU-010）
- data/scenarios_zh.json：H-LUORQ-001 共 10 条（键名 C-LUORQ-001 至 C-LUORQ-010）
- data/scenarios_zh.json：H-MODERN-002 共 10 条（键名 C-MODERN-002-001 至 C-MODERN-002-010）
- data/scenarios_zh.json：H-ZOU-001 共 10 条（键名 C-ZOU-001 至 C-ZOU-010）

撤下原文逐字（含 title/description 等全字段）见 docs/scratch/legacy20_r6c/removed_registrations.json；如需回填，按该文件原样恢复（键级操作、可精确重放）。

## 四、线上可见变化清单

| docs 页（撤下） | 页题 | 站点影响 |
|---|---|---|
| docs/figures/H-AN-001.md | H-AN-001 安子介 人物档案 | 文档站 /figures/H-AN-001/ 页随重建消失（mkdocs 源为该文件） |
| docs/figures/H-ZOU-001.md | 邹文献 (Zou Wenlian) 思维模式研究报告 | 文档站 /figures/H-ZOU-001/ 页随重建消失（mkdocs 源为该文件） |
| docs/figures/H-LUORQ-001.md | 罗瑞卿 (Luo Ruiqing) 思维模式研究报告 | 文档站 /figures/H-LUORQ-001/ 页随重建消失（mkdocs 源为该文件） |

- 站点计数链不受影响：figures/场景计数源自 api/protreptic.db（tools/json 输入），C 组 7 件均不在其中（按码查 DB 为空集）；本卡未触碰计数链。
- site_docs/ 为本地生成镜像（未跟踪）：撤下的 3 页与搜索索引残留随下一次重建自然消失。
- 发布仓镜像（publish）由合并卡统一收敛；本卡改动清单见证据文件，供收敛核对。

## 五、待权威身份清单（6 件）

单列标准（assessment §4.3）：身份未能核实（库内/git/docs 无独立证据）。

| 代码 | 卡面名 | 登记名（撤下前） | 裁决 | 未能核实依据 | 载荷摘要 |
|---|---|---|---|---|---|
| H-AN-001 | 安子 | 安子 | 不可 | 身份未能核实：库内 0 条、git 无合并提交、docs 无独立研究件 | 旧号 M001-M010（10 个）；载荷 10 条 |
| H-LC-001 | 陆沉 | 陆沉 | 不可 | 疑似旧世代虚构人物：库内、docs、git 均无独立证据；来源《沉潜之道》不可落源 | 旧号 M401-M410（10 个）；载荷 10 条 |
| H-YE-001 | 叶筱 | 叶筱 | 不可 | 无人名证据：phase46 报告列为 name_mismatch，文件内无人名证据 | 旧号 M401-M410（10 个）；载荷 10 条 |
| H-ZOU-001 | 邹文献 | 邹文献 | 不可 | 零出处内容不可核：公开检索无独立证据；项目内仅自产文档互引 | 旧号 M401-M410（10 个）；载荷 10 条 |
| H-HAN-001 | 沈幅 | 沈幅 | 不可 | 身份与生卒不符：生卒记录 -100 至 180 与人物不符（phase46 已记疑似沈复）；公开检索无此人此作 | 旧号 M351-M358（8 个）；载荷 8 条 |
| H-MODERN-002 | 大云 | 大云 | 不可 | 元数据虚标 10 条：项目内大云仅指《大云经》，无此人证据 | 旧号 M001-M010（10 个）；载荷 10 条；元数据虚标 10（无载荷） |

- 机读版：docs/research/phase21r6C_pending_identity.json（含 keep_condition 与 renumber_plan；M-AN-/M-LC-/M-YE-/M-ZOU-/M-HAN-/M-DAYUN- 区间当前 0 碰撞，保留须先立研究卡）。

## 六、映射账本与全库查重复核

- 位置先例检查：仓内无既有总账本；审计清单惯例位为 data/audit/（已有 phase21r6_batch1_landing_manifest.json、phase21r6_batch2_backup_manifest.json、phase20R_* 系列）。
- 账本：data/audit/phase21r6_id_mapping_ledger.tsv（同名 .json 含 sources sha256 与复算方法）。
- 行数：A 组 100（批1/批2 id_mapping 汇总）；B 组 32（r6b 交接件登记，B 收口在制）；C 组 78（本卡归档段）。
- 全库查重：新号 111 个，唯一性 通过；modes_data 占用 100、code_maps 占用 100；归属碰撞 0（须为 0）。
- 交叉引用邻接：新号被他件正文提及 2 处（批1 登记的 cross_references 邻接口径；邻接非占用，明细见账本 .json 的 adjacent_mentions）。
- 旧世代重码说明（归档不换号之由）：C 组旧号段相互重码（LC/YE/ZOU 同处 M401-M410 面；AN/MODERN-002 与既有 M001-M010 面同形；LUORQ 载荷 M311-M320 与图档自述 M351-M360 不符）；assessment 处置为「暂不分配」，账本 new_id 记归档标记。
- 复算方法：见账本 .json 的 recompute_recipe；逐行 source_ref 可回溯到批1/批2 tsv 行号。

## 七、罗瑞卿载荷隔离

- 载荷（M311-M320）内容实为陆有（诗词政治文学），与罗瑞卿名实不符；按 assessment 做隔离归档（归档件名含 ISOLATED 标记）+ 另立项说明。
- 详见：docs/research/phase21r6C_luorq_isolation_note.md（含重做前置条件与禁止事项）。

## 八、活跃层复扫报告（残留逐条登记）

- 复扫域：data/、tools/、web/public/、docs/（排除 .git、__pycache__、site_docs、_duplicates、backup_*）；扫描时点=本卡产物写入后、提交前（登记含本卡产物层；evidence 自身为登记载体，不列自身）。
- 分层：活跃层（data 常规、tools、web/public）/ 历史报告层 / 交接层（docs/scratch）/ 文档层；本卡产物层单列。

| 层 | 文件 | 含码 | 首行样本（截断） | 判定 |
|---|---|---|---|---|
| 交接/工作层 | docs/scratch/legacy20_rev6_landing/batch1/H-CY-001/figures/H-CY-001.json | H-LC-001 | "target_figure_code": "H-LC-001", | 交接/工作层（生成件，留痕） |
| 交接/工作层 | docs/scratch/legacy20_rev6_landing/batch1/H-CY-001/individuals/H-CY-001.json | H-LC-001 | "target_figure_code": "H-LC-001", | 交接/工作层（生成件，留痕） |
| 历史报告层 | docs/planning/credibility_framework.md | H-AN-001 | 胜者由遍历顺序决定（实测 `Modern` 键上记的是 `H-AN-001` 的 1900–1970）。 | 历史报告层（留痕，不动作） |
| 历史报告层 | docs/qa/phase21R_restore_report.md | H-AN-001,H-LC-001,H-YE-001,H-ZOU-001,H-HAN-001,H-MODERN-002,H-LUORQ-001 | \| AN \| 安子 \| H-AN-001 \| H-AN-001.json(10,legacy-M###); H-AN-001_modes.json(10,leg | 历史报告层（留痕，不动作） |
| 历史报告层 | docs/qa/phase36_acceptance.md | H-AN-001 | docs/batch_import_56_runbook.md  docs/figures/H-AN-001.md  docs/figures/H-CY-001 | 历史报告层（留痕，不动作） |
| 历史报告层 | docs/qa/phase37_x4_repo_parity.md | H-AN-001 | CONTENT_DIFF           docs/figures/H-AN-001.md | 历史报告层（留痕，不动作） |
| 历史报告层 | docs/qa/phase42_z4_d5_closure.md | H-AN-001,H-HAN-001 | 键冲突丢弃: Modern         data/figures/H-AN-001.json:birth_year/death_year[1900, 197 | 历史报告层（留痕，不动作） |
| 历史报告层 | docs/qa/phase46_figure_fields.md | H-AN-001,H-YE-001,H-HAN-001 | - 朝代或时代当 code 的一律改掉: H-SW-001 战国 -> H-SW-001; H-BG-001 Han -> H-BG-001; H-AN-001 | 历史报告层（留痕，不动作） |
| 历史报告层 | docs/research/legacy20_rev6_assessment.md | H-AN-001,H-LC-001,H-YE-001,H-ZOU-001,H-HAN-001,H-MODERN-002,H-LUORQ-001 | 结论：CY、DY、LC 三件的真实载荷只看本码文件；其余 17 件经复核无此问题（AN 行的 H-HAN-001、H-GAN-001、H-MAN-001 等字样 | 历史报告层（留痕，不动作） |
| 历史报告层 | docs/research/phase20_chenghao_orphan_cleanup_evidence.json | H-AN-001,H-ZOU-001,H-LUORQ-001 | "site_docs/figures/H-AN-001/index.html", | 历史报告层（留痕，不动作） |
| 历史报告层 | docs/research/phase21r6_landing_batch1_verify_evidence.json | H-AN-001 | "E/G 旧号在活库其他文件的占用（重码面）: {\"H-JX-001\": {\"check_mode_ids.py\": 2, \"fix_wc_ids2. | 历史报告层（留痕，不动作） |
| 文档层 | docs/figures/H-BG-001.md | H-HAN-001 | ### 与沈幅的比较（H-HAN-001） | 文档层互引（随重建以现盘为准；如需重指另卡） |
| 文档层 | docs/figures/H-CY-001.md | H-LC-001 | 1. **与陆沉 (H-LC-001) 的比较关系** | 文档层互引（随重建以现盘为准；如需重指另卡） |
| 文档层 | docs/figures/H-MODERN-003.md | H-MODERN-002 | ### 与戴相龙 (H-MODERN-002) 的配套 | 他件引用（H-MODERN-003 与 MODERN-002 相关）→ 待其收口处置 |
| 本卡产物 | data/audit/phase21r6_id_mapping_ledger.json | H-AN-001,H-LC-001,H-YE-001,H-ZOU-001,H-HAN-001,H-MODERN-002,H-LUORQ-001 | "figure_code": "H-AN-001", | 本卡证据（映射账本） |
| 本卡产物 | data/audit/phase21r6_id_mapping_ledger.tsv | H-AN-001,H-LC-001,H-YE-001,H-ZOU-001,H-HAN-001,H-MODERN-002,H-LUORQ-001 | H-AN-001	安子	M001	—（归档；暂不分配）	归档；若保留另立研究卡	C	t_4a9cf2cb	本卡归档件（H-AN-001_figures.json | 本卡证据（映射账本） |
| 本卡产物 | docs/research/phase21r6C_archive_evidence.json | H-AN-001,H-LC-001,H-YE-001,H-ZOU-001,H-HAN-001,H-MODERN-002,H-LUORQ-001 | "source": "data/figures/H-AN-001.json", | 本卡产物（证据/报告） |
| 本卡产物 | docs/research/phase21r6C_archive_report.md | H-AN-001,H-LC-001,H-YE-001,H-ZOU-001,H-HAN-001,H-MODERN-002,H-LUORQ-001 | ### H-AN-001（安子） | 本卡产物（证据/报告） |
| 本卡产物 | docs/research/phase21r6C_luorq_isolation_note.md | H-LUORQ-001 | - 归档代码：H-LUORQ-001（登记名：罗瑞卿）。罗瑞卿本体真实（1906-1978），且 docs 页自述与史实一致。 | 本卡产物（证据/报告） |
| 本卡产物 | docs/research/phase21r6C_pending_identity.json | H-AN-001,H-LC-001,H-YE-001,H-ZOU-001,H-HAN-001,H-MODERN-002 | "code": "H-AN-001", | 本卡产物（证据/报告） |
| 本卡产物 | docs/scratch/legacy20_r6c/apply_r6c_archive.py | H-AN-001,H-LC-001,H-YE-001,H-ZOU-001,H-HAN-001,H-MODERN-002,H-LUORQ-001 | CODES = ["H-AN-001", "H-LC-001", "H-YE-001", "H-ZOU-001", "H-HAN-001", "H-MODERN | 本卡产物（证据/报告） |
| 本卡产物 | docs/scratch/legacy20_r6c/build_r6c_products.py | H-AN-001,H-LC-001,H-YE-001,H-ZOU-001,H-HAN-001,H-MODERN-002,H-LUORQ-001 | CODES = ["H-AN-001", "H-LC-001", "H-YE-001", "H-ZOU-001", "H-HAN-001", "H-MODERN | 本卡产物（证据/报告） |
| 本卡产物 | docs/scratch/legacy20_r6c/r6c_archive_manifest.json | H-AN-001,H-LC-001,H-YE-001,H-ZOU-001,H-HAN-001,H-MODERN-002,H-LUORQ-001 | "source": "data/figures/H-AN-001.json", | 本卡产物（证据/报告） |
| 本卡产物 | docs/scratch/legacy20_r6c/removed_registrations.json | H-AN-001,H-LC-001,H-YE-001,H-ZOU-001,H-HAN-001,H-MODERN-002,H-LUORQ-001 | "H-AN-001": "安子", | 本卡产物（证据/报告） |
| 本卡产物 | docs/scratch/legacy20_r6c/verify_output.txt | H-AN-001,H-LC-001,H-YE-001,H-ZOU-001,H-HAN-001,H-MODERN-002 | [PASS] D1 待身份清单 6 件字段齐（['H-AN-001', 'H-LC-001', 'H-YE-001', 'H-ZOU-001', 'H-HAN- | 本卡产物（证据/报告） |
| 活跃层 | data/audit/figure_field_defects.json | H-AN-001,H-LC-001,H-YE-001,H-ZOU-001,H-HAN-001,H-MODERN-002 | "file": "H-HAN-001.json", | 审计历史件（既有清单，留痕） |
| 活跃层 | data/audit/figure_field_defects_after.json | H-YE-001,H-HAN-001 | "file": "H-YE-001.json", | 审计历史件（既有清单，留痕） |
| 活跃层 | data/audit/figure_field_fix_manifest.json | H-AN-001,H-LC-001,H-YE-001,H-ZOU-001,H-HAN-001,H-MODERN-002 | "file": "H-AN-001.json", | 审计历史件（既有清单，留痕） |
| 活跃层 | data/audit/lifespan_backfill.json | H-LC-001,H-MODERN-002 | "file": "data/figures/H-LC-001.json", | 审计历史件（既有清单，留痕） |
| 活跃层 | data/audit/phase20R_zengzi_residual_scan.json | H-AN-001,H-ZOU-001,H-LUORQ-001 | "file": "site_docs/figures/H-AN-001/index.html", | 审计历史件（既有清单，留痕） |
| 活跃层 | data/audit/phase21r_audit.json | H-AN-001,H-LC-001,H-YE-001,H-ZOU-001,H-HAN-001,H-MODERN-002,H-LUORQ-001 | "figure_code": "H-AN-001", | 审计历史件（既有清单，留痕） |
| 活跃层 | data/code_maps.json | H-LC-001 | "target_figure_code": "H-LC-001", | 登记在案（未归类，待裁定） |
| 活跃层 | data/code_maps.json.bak_zz_20260910_083514 | H-LC-001,H-ZOU-001,H-MODERN-002,H-LUORQ-001 | "H-LUORQ-001": { | 备份件（历史留痕） |
| 活跃层 | data/figures/H-CY-001.json | H-LC-001 | "target_figure_code": "H-LC-001", | 他件引用（H-CY-001 cross_references）→ 待其收口重指 |
| 活跃层 | data/figures/H-MODERN-003.json | H-MODERN-002 | "target_figure_code": "H-MODERN-002", | 他件引用（H-MODERN-003 与 MODERN-002 相关）→ 待其收口处置 |
| 活跃层 | data/individuals/H-BG-001.json | H-HAN-001 | "target_figure_code": "H-HAN-001", | 他件引用（H-BG-001）→ 待其收口重指 |
| 活跃层 | data/individuals/H-CY-001.json | H-LC-001 | "target_figure_code": "H-LC-001", | 他件引用（H-CY-001 cross_references）→ 待其收口重指 |
| 活跃层 | data/individuals/phase20_anzi_research.md | H-AN-001 | - **研究编号**：H-AN-001 | 登记在案（未归类，待裁定） |
| 活跃层 | data/modes_data.json | H-LUORQ-001 | "H-LUORQ-001": { | 合并卡负责面（冻结值登记；顶层 H-LUORQ-001 块待裁定） |
| 活跃层 | data/modes_data.json.bak | H-LUORQ-001 | "H-LUORQ-001": { | 备份件（历史留痕） |
| 活跃层 | data/modes_data.json.bak_zz_20260910_083514 | H-LUORQ-001 | "H-LUORQ-001": { | 备份件（历史留痕） |
| 活跃层 | data/scenarios_en.json.bak_zz_20260910_083514 | H-ZOU-001,H-MODERN-002,H-LUORQ-001 | "figure_id": "H-MODERN-002", | 备份件（历史留痕） |
| 活跃层 | data/scenarios_zh.json.bak_zz_20260910_083514 | H-ZOU-001,H-MODERN-002,H-LUORQ-001 | "figure_id": "H-MODERN-002", | 备份件（历史留痕） |
| 活跃层 | tools/audit_figure_fields.py | H-YE-001,H-HAN-001 | "H-HAN-001.json": "name='沈幅'/en='Shen Fu'/生卒年=-100~180, 三者互不吻合; 疑似沈复(清,1763-1830 | 工具内嵌历史名单/注释（留痕，不动） |
| 活跃层 | tools/credibility_gate.py | H-AN-001 | 胜者由文件遍历顺序决定（实测 'Modern' 键上记的是 H-AN-001 的 1900-1970）。 | 工具内嵌历史名单/注释（留痕，不动） |

- 判定口径：他件引用=留待该件收口重指；历史/交接层=留痕不动作；本卡产物=本卡证据；工具内嵌名单=历史注释（改动超本卡范围）；modes_data 顶层块=合并卡负责面（本卡零写入）。
- 「活跃层零悬空」验收口径 = 自件登记项与档案件零残留 + 上表逐条登记，核验脚本断言「实际残留 == 登记集合」（零未登记残留）。

## 九、核验与证据

- 核验脚本：verify_phase21r6C_archive.py（A 归档登记 / B 活跃层零悬空 / C 账本可复算 / D 清单与证据完整性）。
- 运行输出：docs/scratch/legacy20_r6c/verify_output.txt（提交后重跑留证）。
- 证据文件：docs/research/phase21r6C_archive_evidence.json（archives / removed / online / dedupe / residual / products）。
- 执行脚本与原始记录：docs/scratch/legacy20_r6c/ 下 {apply_r6c_archive.py, build_r6c_products.py, r6c_archive_manifest.json, removed_registrations.json}。

## 十、遗留与待裁定

- 发布仓镜像收敛：由合并卡统一执行（本卡改动记录于证据文件，供对齐）。
- B 收口口径通报：归档件 figure_names 机制键按 R2 先例清档（本卡已对 C 组执行）；H-DYM-001/H-HZX-002 同类键建议同口径，由其收口卡执行。
- 他件引用（如 H-CY-001 → H-LC-001 的 cross_references）留待该件收口时重指；本卡不改他件。
- modes_data.json 顶层 H-LUORQ-001 块：合并卡负责面，本卡零写入；随后续卡裁定。
- site_docs 本地镜像残留：重建后消失（未跟踪，不入提交）。
- LUORQ 重做另立项（建议单开研究卡；前置条件见隔离说明）。

