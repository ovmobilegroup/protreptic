# Phase 20 QA 验收报告：戴震（Dai Zhen, H-DZ-001）

- 任务: `t_672df5eb`（QA 审查，espinosa）→ 下游文档归档（pigafetta）
- 入库提交: `035327c9`（数据落地，档案 md 头部引）；上游复核: barbosa `phase20_daizhen_recheck_report.md`（PASS / 零改动）
- 验收基线: 修复前冻结快照（三份权威文件原始版）＋ 修复后工作区
- 结论: **PASS（经热修）** —— 结构、索引、场景、镜像、档案全部达标；本卡新发现并修复 **6 类 / 8 处文本 × 3 面 = 24 行** 文本缺陷

---

## 一、脚本结果

| 脚本 | 环境 | 结果 |
|---|---|---|
| 本卡独立 `verify_dz_qa_espinosa.py`（1941 项） | 修复后工作区 | **1941/1941 PASS** |
| 本卡独立 `verify_dz_qa_espinosa.py` | 修复前冻结快照 | **1887 PASS / 54 FAIL**（52 项缺陷断言命中 + 2 项快照假报）✓ 判据非空转 |
| 上游落地 `verify_daizhen_phase20.py`（71 项） | 修复前后均复跑 | 71/71 PASS（未覆盖本卡缺陷类别，判据盲区证据） |
| 上游复核 `verify_daizhen_recheck_indep.py`（barbosa） | t_* 复核卡记录 | PASS / 零改动 |

54 项 FAIL 中 52 项为本卡判据命中（48 项热修态断言 + 档案行尾空白 1 项 + 案例行尾空格 1 项 + 纯度行尾 1 项 + 档案保真 1 项），另 2 项为快照树缺 `H-ZHX-001`/`H-GYW-001` 图档导致的真值可达性假报（修复后环境零缺陷）。上游与复核脚本的判据均未覆盖「引文保真、译文忠实、行尾空白、罗马化」四类，故此前全部 PASS。

## 二、复核确认（无争议项）

1. **模式增量** M-DZ-001~010 恰 10 条：`id==mode_code`、`figure_code=H-DZ-001`、`research_mode_id=M-DAI-00n` 一一对应；v6 字段齐备（5 关键概念、5~6 步流程中英、3 案例中英、3 应用中英、双语定义引证、`verification.status=verified`）。
2. **关联完整性**：10 条 `related_modes` 全部可解析至全库模式，无悬空。
3. **场景** C-DZ-001~010 / C-DZ-001E~010E 各 10 条：`mode_code` 顺序绑定、标题=模式名、`application_area` 与模式 `modern_applications` 逐字一致、`text_*` 构造式（标题＋场景串接）一致、语言纯度零污染。
4. **标签** +20（zh/en 各 10、后缀与 `language` 三向一致、全库无重复）。
5. **code_maps** `H-DZ-001`：`mode_ids` 10 / `tags` 10 模式名 / `cross_references` 3 条（H-ZHX-001、H-GYW-001、H-WFZ-001）目标可达，且与图档 xref 逐字一致。
6. **图档三镜像**（`data/figures` ↔ `data/individuals` ↔ `docs/figures`）18,644 B、SHA256 `b10a2a3b609e…9406e9f` 一致；`modes`/`mode_ids`/`thinking_mode_count` 覆盖 10；`mode_evidence` 10 条（`evidence_zh = 出处＋「：」＋原文`、`evidence_en`、`source` 与模式字段逐字对齐）；`protreptic_mapping` 覆盖 10；`phase20.mode_id_mapping` 1:1。
7. **档案 md** 58,140 B：10 模式**全字段**（英文名/类别/层级/优先级/研究稿ID/领域/出处/定义中英/关键概念/原文依据中英/流程中英/案例中英/应用中英/关联模式）逐字等于库内；双语场景索引 20 行、xref 3 行、现代价值 6 行逐字对齐；全文行尾空白 0；头部批次链（落地 `035327c9`、71/71 PASS）在位。
8. **语言纯度**：M-DZ 全字段 `_en` 无 CJK、`_zh` 无 4+ 连续拉丁词，零命中。

## 三、新发现缺陷（6 类 / 8 处 × 3 面 = 24 行，已修复）

| # | 类别 | 位置 | 修复前 → 修复后 | 依据 |
|---|---|---|---|---|
| 1 | 语义反转 | M-DZ-001 `definition_en` | `The method subordinates linguistics to philosophy` → `The method places linguistics before philosophy` | 同卡中文母句「此法把语言学置于哲学之前」；训诂为义理之基（由字→词→道） |
| 2 | 引文异文 | M-DZ-001 `representative_cases_zh[2]` | 「以己见硬坐为古圣贤立言之意」→「以己之见硬坐为古贤圣立言之意」 | 《与某书》：识典古籍影印《戴东原集》「宋已来儒者，以己之见，硬坐为古贤圣立言之意，而语言文字实未之知」 |
| 3 | 译文失真＋行尾空白 | M-DZ-003 `representative_cases_en[0]` | `…kill with principle. How devastating!'␠` → `…kill with principle. Gradually, as law is set aside and principle is made the measure, people die with no remedy.'` | 原文「浸浸乎舍法而论理，死矣，更无可救矣」（《与某书》）；原译丢弃后半句并代以情绪化感叹 |
| 4 | 不可溯源引文 | M-DZ-004 `representative_cases_zh[0]` ＋ `_en` | 「程子朱子之徒，分性二目，曰天命之性，曰气质之性……此所谓援道来入儒也。」→「故截气质为一性，言君子不谓之性；截理义为一性，别而归之天，以附合孟子。」 | 新句三源逐字（Wesleyan e-text《孟子字义疏证》、维基文库、国学导航）；原句在疏证全文与检索中不可溯源（属落库期概述改写加引号） |
| 5 | 罗马化错误 | M-DZ-005 `definition_en` | `empathy (qie qing)` → `empathy (xie qing)` | 絜＝度量义读 **xié**：漢典/萌典「量物體的周圍長度；也泛指衡量」（度長絜大）；康熙字典「絜矩之道」胡結切；词典「絜矩」xié jǔ；《安徽工业大学学报》「絜情」专文英文摘要作 *Yi Qing Xie Qing* |
| 6 | 出处误植 | M-DZ-009 `representative_cases_zh[0]` ＋ `_en` | 「戴震对《水经注》的校勘——从《永乐大典》中辑出佚文，改正错字281…」→「戴震对《方言》的疏证——以《永乐大典》本及古书所引《方言》与明本对勘…」 | 281 错字 / 27 脱字 / 17 衍字 为《方言疏证》校勘统计（sinoss 学术综述《戴震的语言学著作》）；《水经注》校勘另属经注分理问题，与此组数字不对应 |

**落盘明细**：3 文件 / 24 行（`data/modes_data.json` 8 行、`data/individuals/H-DZ-001_modes.json` 8 行、`docs/figures/H-DZ-001.md` 8 行）；提交前逐行核对 diff：每文件恰 8 个 hunks、仅含预期改动，无他人未提交改动被夹带。

**根因**：6 类缺陷均非研究稿（`data/individuals/phase20_daizhen_research.md`，0 命中）引入，而系落库/英译阶段生成（英文与加引号引文为落库期新增；`qie qing` 疑为把「絜」误作「挈」的拼音）；上游 71 项与复核脚本未设对应判据，形成「已 PASS 却带缺陷」盲区（与 WFZ 卡同类教训）。

## 四、遗留与观察（非本卡引入，不阻塞）

- M-DZ-004 `key_quote_zh` 第二句「人之异于禽兽者，以其心之神明也」为概述式引文（疏证原文：「…人之異於禽獸者，雖同有精爽，而人能進於神明也」）——语义无误、字句非逐字，建议全库引文精审时统一。
- M-DZ-007 `key_quote_zh` 为复合引文（首句见《与某书》；「以理為如有物焉，得於天而具於心」为《疏证·理》语汇），出处标注为集合级《孟子字义疏证》。
- M-DZ-009 `source_chapter` 用文集级《戴震文集》标注（其语句与 M-DZ-008/010 同属《与姚孝廉姬传书》信札），集合级标注为库内既有体例，非硬伤。
- hotspot: `data/modes_data.json`（23 MB）等共享大文件为多卡并发写面；本卡为字符串级定长替换＋读写前 SHA256 比对（CAS）落盘，提交前复核 `git status`/diff。工作区内 `docs/figures/H-LJY-001.md`、`docs/research/phase20_zhoudunyi_qa_evidence.txt` 为他人未提交改动，未纳入本卡提交。

## 五、工件

- 独立验收脚本：`verify_dz_qa_espinosa.py`（仓库根目录，1941 项；修复前后双向判据）
- 本报告：`docs/research/phase20_daizhen_qa_report.md`
- 热修提交：与报告同批（3 文件 24 行 ＋ 脚本 ＋ 报告）

## 六、复现命令

```
cd <repo>
python3 verify_dz_qa_espinosa.py                                   # 修复后: 1941/1941 PASS
DZ_REPO_ROOT=<修复前快照> python3 verify_dz_qa_espinosa.py         # 修复前: 1887/1941（54 FAIL，52 项缺陷断言命中）
```

修复前快照为本卡工作区 `prefix_snapshot/`（三份文件在本卡修改前的原文；另存 `verify_prefix.out` / `verify_postfix.out` 两次运行的完整输出）。
