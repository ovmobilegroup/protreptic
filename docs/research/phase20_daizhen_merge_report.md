# Phase 20 落地实现报告：戴震（Dai Zhen, H-DZ-001）

- 任务: t_d5d770a7 (elcano) ← 上游研究 t_d2b15144
- 时间: 20260922_152128
- 研究稿编码: H-DAI-001 / M-DAI-001~010 → 库内编码: **H-DZ-001 / M-DZ-001~010**
- 下游: t_1a8c3e43（barbosa 增量合并复核）→ t_672df5eb

## 一、编码裁定（关键决策）

库内 `戴震` 的 canonical code 为 **H-DZ-001**，证据链：

1. `data/figure_names.json` 唯一映射 `"H-DZ-001": "戴震"`（`H-DAI-*` 在该表中无任何登记）；
2. `data/figures/H-DZ-001.json`、`data/individuals/H-DZ-001.json`、
   `data/individuals/H-DZ-001_modes.json`、`docs/figures/H-DZ-001.md` 均已存在（Phase 21 建档）；
3. `data/figures/H-DZ-001.json` 的 `core_thoughts` 七项（理存于欲 / 以理杀人批判 / 由词通道 / 分理说 /
   血气心知 / 解蔽去私 / 气化即道）与上游研究稿五条主线一一对应（方法论、本体论、伦理学、人性论、政治哲学）；
4. 上游研究稿自动派生码 `H-DAI-001` 系「戴 + 拼音首字母」机械派生，与库内既有编码冲突，
   **同一人物不得双码**。

故落库统一采用 `H-DZ-001`，模式 ID 统一为 `M-DZ-001~010`，每条模式以 `research_mode_id`
字段完整保留研究稿原始 ID（`M-DAI-*`），图档另设 `phase20` 溯源块记录
`research_code H-DAI-001 → library_code H-DZ-001` 及 1:1 映射表。
（与同批陆九渊 H-LUJ-001→H-LJY-001、王夫之 H-WAN-001→H-WFZ-001 的处理完全一致。）

## 二、写入清单

| 文件 | 变更 |
|---|---|
| `data/modes_data.json` | +10 条 M-DZ-001~010（figure_code=H-DZ-001）；`total` 2928 → **2938** |
| `data/code_maps.json` | 首次注册 `figures["H-DZ-001"]`（mode_ids 10 + tags 10 + cross_references 3），figures 209→210 |
| `data/scenarios_zh.json` | `scenarios_zh` +10 条 C-DZ-001~010（2153→2163） |
| `data/scenarios_en.json` | `scenarios_en` +10 条 C-DZ-001E~010E（2153→2163） |
| `data/scenario_tags.json` | +20 条（zh/en 各 10，figure_code=H-DZ-001），7218→7238 |
| `data/figures/H-DZ-001.json` | mode_ids/modes/mode_evidence/protreptic_mapping/tags/source_files 更新 + `mode_ids_note` + `phase20` 溯源块；**figure_code 缺陷修复**（见第六节） |
| `data/individuals/H-DZ-001.json` | 与上同步（**字节镜像**，并合入 individuals 专有字段 `meta`） |
| `docs/figures/H-DZ-001.json` | `data/figures` 字节镜像（**新建补齐第三镜像**；三处 SHA256 一致） |
| `data/individuals/H-DZ-001_modes.json` | 新增 `thinking_modes_v6_phase20`（10 条库内格式）+ `modes_ref` + `phase20_note`；**Phase 21 建档 `modes`（M331~M340）原样保留** |
| `docs/figures/H-DZ-001.md` | 重建为 Phase 20 研究档案（13.3KB → 57.8KB：10 模式全字段中英逐字 + 双语场景索引 + 交叉引用 + 入库说明） |
| `data/individuals/phase20_daizhen_research.md` | 上游研究稿归档（数据层可溯源，3436 字节） |
| `verify_daizhen_phase20.py` | 独立验收脚本（仓库根目录，**71/71 PASS**） |
| `docs/research/phase20_daizhen_merge_report.md` | 本报告 |

备份：工作区内 `backup_merge_H-DZ-001_20260922_152128/`（9 个文件，未写入仓库以免体积噪声）。

## 三、模式 ID 映射

| 研究稿 | 库内 | 模式名（中 / 英） | 类别 |
|---|---|---|---|
| M-DAI-001 | M-DZ-001 | 由字通道法 / Word-to-Way Method (Etymology as Path to Truth) | 方法论 |
| M-DAI-002 | M-DZ-002 | 气化流行法 / Qi-Circulation Method (Cosmology as Continuous Process) | 本体论 |
| M-DAI-003 | M-DZ-003 | 理存欲中法 / Principle-in-Desire Method (Rejection of Desire-Suppression) | 伦理学 |
| M-DAI-004 | M-DZ-004 | 血气心知法 / Blood-Qi-Mind-Knowing Method (Natural Human Nature Theory) | 人性论 |
| M-DAI-005 | M-DZ-005 | 絜情平欲法 / Empathic Equilibrium Method (Measuring Emotion for Justice) | 伦理学 |
| M-DAI-006 | M-DZ-006 | 以理杀人批判法 / Anti-Principle-Killing Critique Method (Exposing Ideological Tyranny) | 政治哲学 |
| M-DAI-007 | M-DZ-007 | 体民遂欲法 / Governance-for-People Method (Understanding Emotions, Fulfilling Desires) | 政治哲学 |
| M-DAI-008 | M-DZ-008 | 十分之见法 / Complete Evidence Method (The Standard of Thorough Verification) | 方法论 |
| M-DAI-009 | M-DZ-009 | 实证归纳法 / Empirical Induction Method (Evidence-Based Research) | 方法论 |
| M-DAI-010 | M-DZ-010 | 汉宋兼采法 / Han-Song Synthesis Method (Eclectic Scholarship) | 方法论 |

图档 `protreptic_mapping`: 方法论 [M-DZ-001,008,009,010]；本体论 [M-DZ-002]；伦理学 [M-DZ-003,005]；
人性论 [M-DZ-004]；政治哲学 [M-DZ-006,007]。

## 四、跨引用（原有三条，均可达）

| 目标 | 关系 | 说明 |
|---|---|---|
| `H-ZHX-001` 朱熹 | comparison | 朱以理为超验本体、戴把理还原为情欲之条理；`data/figures/H-ZHX-001.json` 已落地 |
| `H-GYW-001` 顾炎武 | influence | 顾开清代考据先河、戴承其路数并把考据提升为哲学重建；`data/figures/H-GYW-001.json` 已落地 |
| `H-WFZ-001` 王夫之 | comparison | 同重建理欲关系、路径不同（气学形上学 vs 训诂经验方法）；code_maps 已注册 |

本次未引入新交叉引用，未修改任何 xref 目标码（无错码需修复）。

## 五、研究稿文字修复（19 个字段、21 处）

| 编号 | 字段 | 修复 |
|---|---|---|
| 1 | M-DZ-001 `representative_cases_en[0]` | `(理): starting` → `(principle): starting`；`to its本义` → `to its original sense` |
| 2 | M-DZ-002 `process_en[3]` | `(生生)` → `(shengsheng)` |
| 3 | M-DZ-002 `representative_cases_en[2]` | `'shengsheng' (生生)` → `'shengsheng' (generative becoming)` |
| 4 | M-DZ-005 `definition_en` | `seeking of公正 balance` → `seeking of a fair balance` |
| 5 | M-DZ-005 `representative_cases_en[0]` | `rational法则` → `rational rules` |
| 6 | M-DZ-006 `representative_cases_en[0]` | `more可怕` → `more terrifying`；`the外衣 of moral legitimacy` → `the cloak of moral legitimacy` |
| 7 | M-DZ-006 `representative_cases_en[1]` | `which恰恰 proves` → `which precisely proves` |
| 8 | M-DZ-006 `modern_applications_en[2]` | `Boundary辨析` → `Boundary discrimination` |
| 9 | M-DZ-007 `definition_en` | `suppress the百姓` → `suppress the people`；`the百姓's real emotions` → `the people's real emotions` |
| 10 | M-DZ-007 `key_quote_en` | `weighting desires轻重` → `weighing desires as heavy or light` |
| 11 | M-DZ-007 `process_en[0]` | `understand the百姓's` → `understand the people's` |
| 12 | M-DZ-008 `definition_en` | `—贯通古今,` → `— spanning ancient and modern,`；`theories to裁其优` → `theories to judge the better` |
| 13 | M-DZ-008 `key_quote_en` | `theories to裁其优` → `theories to judge the better` |
| 14 | M-DZ-008 `representative_cases_en[1]` | `is正是 the practice` → `is precisely the practice` |
| 15 | M-DZ-009 `representative_cases_en[0]` | `首创 the yin-yang entrance mutual transformation theory` → `pioneering the yin-yang-ru mutual transformation theory`；`analysis of大量文献, not凭空构拟` → `analysis of a large body of texts, not groundless reconstruction` |
| 16 | M-DZ-009 `representative_cases_en[1]` | `empirical功夫` → `empirical craftsmanship` |
| 17 | M-DZ-010 `definition_en` | `the包容性 and openness` → `the inclusiveness and openness` |
| 18 | M-DZ-010 `process_en[0]` | `each school's学说` → `each school's doctrine` |
| 19 | M-DZ-010 `process_en[1]` | `each school's学说` → `each school's doctrine` |

修复后：M-DZ-* 全部 `_en` 字段无 CJK、`_zh` 字段无 3 字母以上拉丁词（脚本第 11/12/13 项断言）。

## 六、镜像缺陷修复（本卡额外发现）

`data/individuals/H-DZ-001.json` 的 `figure_code` 原值为 **`"Qing"`**（Phase 21 建档遗留误值，应为
`H-DZ-001`）。本次合并以 `data/figures/H-DZ-001.json` 为主档（主档 `figure_code` 正确），
`individuals` 专有字段仅做「主档缺失才并入」，故三镜像统一为 `H-DZ-001`；
验收脚本第 52 项以备份逐项比对确认该修复（backup=`Qing` → now=`H-DZ-001`）。

## 七、验收要点（`python3 verify_daizhen_phase20.py`，71/71 PASS）

1. 库内 10 条 M-DZ-001~010；`total == len(modes)`（2928→2938）；figure_code 全为 H-DZ-001
2. 每条含中英名称/定义/流程/关键概念/源文引证/代表案例/现代应用 + research_mode_id + verification
3. 语言纯度：M-DZ-* 与双语场景、源研究档均无混排；21 处研究稿污染字符串在库内绝迹、22 个修复后字符串在位
4. 源研究档与主库条目逐字一致；Phase 21 建档 M331~M340 原样保留且未混入主库
5. 场景 zh/en 各 10，mode_code 一一对应，标题与模式名一致
6. scenario_tags 20 条覆盖 10 个 mode_code（zh/en 各 10，无重复）
7. code_maps 注册 + mode_ids/tags 一致 + 交叉引用无悬空
8. 图档三处镜像 SHA256 一致；`mode_evidence`/`protreptic_mapping` 覆盖 10 模式；
   原有 50 条 tags、core_thoughts 七项、historical_significance/unique_thing/influence/modern_value_zh
   正文**零改动**（与备份逐字比对）
9. 档案 md > 20KB、10 模式定义中英逐字等于库内、含 20 条双语场景索引、无 TODO/替换字符；
   省略号行（1 行，古籍引文内）逐字来自库内数据（非截断）
10. related_modes 无悬空；全库具名 mode_id 无重复；figure_names 唯一登记、无 H-DAI 派生码残留；
    individuals 图档 `figure_code` 缺陷已修复

## 八、遗留与提示（非本卡范围）

- `H-ZHX-001`（朱熹）、`H-GYW-001`（顾炎武）尚未在 `data/code_maps.json` 注册（其图档文件存在）——
  属对应人物卡范围；本卡验收脚本对交叉引用采用「code_maps 注册 **或** `data/figures/<code>.json` 存在」双判据。
- 上游研究稿（`phase20_daizhen_research.md`，3436 字节）为附件**原样归档**，未增补模式索引；
  模式级内容以 `H-DAI-001_modes.json`（随研究稿同批产出）及各库内条目为准。
- `api/data/`、`web/`、`tools/` 下的数据副本未同步（同批 Phase 20 卡均只写 `data/` 与 `docs/`），
  其同步由专门的一致性卡统一处理。
- hotspot: `data/modes_data.json`、`data/code_maps.json`、`data/scenario_tags.json` 为多卡共享大文件，
  本卡仅追加自身足迹（+10 模式 / +1 figure / +20 标签 / **未改** figure_names）。
- 本卡提交基线为 `51a74059`（陆九渊文档归档），提交仅含本卡 13 个文件足迹（paths 精确指定）。

## 九、复现命令

```
cd /opt/data/workspace/Protreptic
python3 verify_daizhen_phase20.py     # 71/71 PASS
```
