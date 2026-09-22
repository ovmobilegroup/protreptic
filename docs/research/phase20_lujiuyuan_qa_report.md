# Phase 20 QA 验收报告：陆九渊（Lu Jiuyuan, H-LJY-001）

- 任务: `t_42c77bc7`（QA 审查，espinosa）→ 下游 `t_6d79091d`（文档归档，pigafetta）
- 入库提交: `6830059b`（父 `98d7ddd1`）；上游复核: `t_75c396cb`（barbosa，PASS / 零改动）
- 验收基线: `git show 6830059b` 结构 + 工作区落盘内容（含本卡热修）
- 结论: **PASS（经热修）** —— 结构、索引、场景、镜像、档案全部达标；新发现并修复 **1 类 / 5 处** 内容缺陷

---

## 一、脚本结果

| 脚本 | 环境 | 结果 |
|---|---|---|
| 上游 `verify_lujiuyuan_phase20.py`（51 项） | 冻结快照 `6830059b`（git archive） | 51/51 PASS |
| 上游 `verify_lujiuyuan_phase20.py` | 工作区（本卡修复后） | 全 PASS |
| 复核卡 `verify_ljy_indep.py`（74 项，barbosa） | 工作区 | 74/74 PASS |
| 本卡独立 `verify_ljy_qa_espinosa.py`（98 项） | 工作区（本卡修复后） | **98/98 PASS** |
| 本卡独立 `verify_ljy_qa_espinosa.py` | 修复前工作区（反向验证） | 97 PASS / **1 FAIL**（3.1 命中 5 处残留）✓ 判据有效 |

独立脚本在写入仓库前**先对修复前状态复跑并复现缺陷**，确认判据非空转；修复后复跑归零。

## 二、复核确认（无争议项）

1. 库内模式 2908 == `total`；新增恰为 `M-LJY-001~010`，`mode_code`、`figure_code=H-LJY-001`、`research_mode_id=M-LUJ-00n` 一一对应；主库无 `M-LUJ` 派生条目。
2. 提交面 13 个文件；共享大文件均为纯追加（`modes_data` 唯一删除行是 `total` 2898→2908）。
3. 每条模式 v6 字段完备（名称/定义/领域/流程/关键概念/引证/案例/现代应用/verification），中英定义非同串。
4. `data/individuals/H-LJY-001_modes.json` 的 `thinking_modes_v6_phase20` 与主库**逐字段零差异**；Phase 21 `thinking_modes` 原样保留 10 条。
5. 图档三镜像（`data/figures` ↔ `data/individuals` ↔ `docs/figures`）15226 B、SHA256 `8a61a691…cde8` 一致；`thinking_mode_count=10`、`mode_ids`、`mode_evidence`、`protreptic_mapping` 全覆盖。
6. `docs/figures/H-LJY-001.md` 33831 B，10 模式全字段（定义/流程/案例/现代应用）与库内**逐字一致**，含双语场景索引，无 TODO/省略号。
7. 场景 `C-LJY-001~010`（zh）/`C-LJY-001E~010E`（en）各 10 条，`mode_code` 与模式名一一对应，英文内容零中文。
8. `scenario_tags` 新增 20 条（zh/en 各 10），无重复，后缀与 `language` 一致。
9. `code_maps.figures` 207→208，仅新增 `H-LJY-001`（`mode_ids` 十法 / `tags` 十法 / 3 条交叉引用）；`cross_references` 目标 `H-ZHX-001`（朱熹）/`H-CHE-001`（程颢）/`H-DZS-001`（董仲舒）均可解析，无本卡新增悬空引用。
10. `figure_names` 唯一登记 `H-LJY-001 → 陆九渊`，无 `H-LUJ` 残留；`H-WYM-001`（王阳明）档案反向回引 `H-LJY-001`，陆王闭环成立。
11. 编码裁定正确：研究稿派生码 `H-LUJ-001` 与库内 canonical `H-LJY-001` 冲突，按「同一人物不得双码」落库，`research_mode_id` + 图档 `phase20` 溯源块保留 1:1 映射。

## 三、新发现缺陷（1 类 / 5 处，已修复）

**类别：英文字段（`_en`）中残留未译中文（中英混排污染）**

| 模式 | 字段 | 修复前 | 修复后 |
|---|---|---|---|
| M-LJY-005 | `process_en[0]` | …the correct direction of**志向** | …the correct direction of **aspiration** |
| M-LJY-007 | `representative_cases_en[2]` | …grounds itself in daily**伦理** | …grounds itself in **the moral relations of daily life** |
| M-LJY-008 | `representative_cases_en[1]` | Lu's**尊德性** priority stance | Lu's **'honoring moral nature' (zun dexing)** priority stance |
| M-LJY-008 | `representative_cases_en[2]` | reading**尊德性** as completely excluding… | reading **'honoring moral nature'** as completely excluding… |
| M-LJY-009 | `representative_cases_en[2]` | …original mind in daily**伦理** | …original mind in **daily moral practice** |

- 波及面：同 5 处文本存在于**三处镜像**（`data/modes_data.json`、`data/individuals/H-LJY-001_modes.json` 的 v6 块、`docs/figures/H-LJY-001.md`），合计 15 行，本次三处同步修复。
- 术语对齐：`aspiration` 与 M-LJY-005 `definition_en`（"if one's aspiration is righteousness…"）一致；`'honoring moral nature' (zun dexing)` 与 M-LJY-008 `definition_en` 既有译法一致；`daily moral practice` 与 M-LJY-009 `definition_en`（"its function is daily moral practice"）一致。故为**回填既有术语**，非新增译名。
- **根因**：上游研究稿 `data/individuals/phase20_lujiuyuan_research.md` 的中文正文已修复（稿内无 `志向`），但库内英文正文由**修复前的早期英译草稿**派生，落地报告第 5 节记录的「英中混排修复」只覆盖研究稿，未覆盖主库/图档/档案 md 的英文字段，形成「源已修、库未修」的传播缺口。
- 三份既有验收脚本（上游 51 项、复核 74 项）均未覆盖「`_en` 字段零 CJK」判据，因此此前全部 PASS；本卡独立脚本第 3.1 项补齐该判据。

## 四、遗留（非本卡引入，不阻塞）

- `H-ZHX-001`（朱熹）尚未在 `code_maps.figures` 注册（其 `data/figures/H-ZHX-001.json` 与 `docs/figures/H-ZHX-001.md` 存在）——属朱熹卡范围，本卡 xref 目标可解析，不构成悬空。
- 上游研究稿 `data/individuals/phase20_lujiuyuan_research.md` 抬头仍署 `H-LUJ-001`；库内码映射已由图档 `phase20` 溯源块与落地报告记录（WARN 级，建议后续补注）。
- **全库同类残留（跨卡系统性问题，供编排决策）**：`data/modes_data.json` 中 `_en` 字段含中文的模式共 **510 处 / 115 个 figure**（如 LISHIMIN 22、H-MIY-001 20、H-ATK-001 20）；Phase 20 同批已收口者仅 H-LJY-001 / H-ZDY-001 / H-CHI-001 / H-CHE-001 / H-HZX-001 / H-STR-001 等，**`H-WYM-001` 另存 1 处**（遗留旧码 `M383`「心外无物法」`process_en[1]`："meaning is**赋予** by the mind"）。建议由编排者统一派一轮「全库 `_en` CJK 清理」专项卡，而非逐卡零散修补。
- hotspot: `data/modes_data.json`（16.9 MB）与 `data/individuals/H-LJY-001_modes.json` 为多卡共享大文件；本卡仅做**定长局部替换**（字符串级，不整写文件），提交前核对 `git status` 确认无他人未提交改动被夹带。

## 五、工件

- `verify_ljy_qa_espinosa.py`（仓库根目录，98 项独立断言；修复前复跑可复现 5 处缺陷）
- 本报告 `docs/research/phase20_lujiuyuan_qa_report.md`
- 修复面：`data/modes_data.json`、`data/individuals/H-LJY-001_modes.json`、`docs/figures/H-LJY-001.md`（各 5 行，3 文件共 15 行）
