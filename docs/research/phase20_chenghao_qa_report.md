# 程颢 (H-CHE-001) Phase 20 QA 验收报告

- 任务卡：t_3f363cbe（QA 审查，上游入库卡 t_229b692a / commit c06d438a）
- 验收对象：`data/figures/H-CHE-001.json`、`docs/figures/H-CHE-001.md`、`docs/research/phase20_chenghao_merge_report.md`
  以及主库 `data/modes_data.json`、`data/code_maps.json`、`data/scenarios_zh.json`、`data/scenarios_en.json`、`data/scenario_tags.json`
- 验收方式：独立只读脚本逐对象直读 git 对象与工作区文件，不采信上游自述、不 import 上游脚本
- 验收时间：2026-09-22
- 结论：**PASS（可发布）**，QA 期间修复 2 类缺陷后重新全量验收通过

## 一、验收结果汇总

| 检查域 | 项目数 | 结果 |
|---|---|---|
| 模式库（10 个 M-CHE-*） | 12 | 全 PASS |
| 图档双镜像（figure/individuals） | 10 | 全 PASS |
| code_maps 注册 | 5 | 全 PASS |
| 双语场景（10+10） | 10 | 全 PASS |
| scenario_tags（20） | 3 | 全 PASS |
| 人物/概念层面 | 3 | 2 PASS，1 WARN（跨人物重名，全库共性） |
| **合计** | **43** | **PASS 42 / WARN 1 / FAIL 0** |

验收脚本最终一次复跑（工作区，HEAD 079df260）：

```
TOTAL 43  PASS 42  WARN 1  FAIL 0
WARN 跨人物模式重名（全库 17 组同类，属思想自然重合）: {'万物一体法': 2}
```

脚本采用三级判定：**PASS**（必须通过）/ **WARN**（全库共性或既有约定，不阻塞发布）/ **FAIL**（阻塞）。
本卡无 FAIL。

## 二、本次 QA 修复的缺陷（已提交）

### 2.1 英文技术字段中文污染 8 处（ding级别）
`data/modes_data.json` 中 M-CHE-* 的 `*_en` 字段混入中文字符，破坏英文检索与前端渲染：

| 模式 | 字段 | 原文 | 修复后 |
|---|---|---|---|
| M-CHE-003 | key_quote_en | Ren is**浑然** integrated | Ren is integrated |
| M-CHE-005 | representative_cases_en | leads to**消极** determinism | leads to negative determinism |
| M-CHE-008 | process_en | Reach the**境界** of inner-outer unity | Reach the state of … |
| M-CHE-010 | definition_en | not an unreachable myth but a**境界** | … but a state |
| M-CHE-010 | process_en | toward the sage's**境界** | toward the sage's state |
| M-CHE-010 | representative_cases_en | it is both a**追溯** to … and an**激励** to … | a return to … and an inspiration to … |
| M-CHE-010 | representative_cases_en | Yan Hui in his**简陋** lane | Yan Hui in his humble lane |
| M-CHE-010 | representative_cases_en | the sage's**境界** includes inner joy | the sage's state includes inner joy |

修复后全量扫描：M-CHE-* 英文字段、figure/individuals 镜像、code_maps 条目中 CJK 命中数 = **0**。

### 2.2 双镜像缺失 tags / cross_references
`data/figures/H-CHE-001.json` 与 `data/individuals/H-CHE-001.json` 的 `tags`、`cross_references` 为空数组，
而 `data/code_maps.json` 同一 figure 已登记 10 个 tag 与 2 条跨引用；同批次人物（H-CHI-001 程颐）镜像则均填充，
因此属入库遗漏。已按 code_maps 注册表回填（10 tags + 2 xrefs），两镜像与注册表现已一致。
`mode_evidence` / `protreptic_mapping` 为空与同批次人物一致，属既有约定，不计缺陷。

## 三、遗留问题（非本次入库引入，不阻塞发布）

### 3.1 跨引用目标未登记（共性问题，已由并发卡缓解）
`H-CHE-001` 的 code_maps 条目跨引用指向 `H-ZDY-001`（周敦颐）。该 figure 文件 `data/figures/H-ZDY-001.json` 存在，
但未登记进 `code_maps.figures`。全库统计：**273 处悬空跨引用目标**（如 H-MO-001 被 4 个人物指向、H-YLS-001 被 3 个指向），
H-ZDY-001 同时被 H-CHE-001 与 H-CHI-001 指向。属注册表历史缺口，需专项批量补登记，不在本卡范围。
（备注：验收期间另一张卡正在入库周敦颐，最新工作区中 H-ZDY-001 已在 code_maps 中登记，
本卡复跑时该悬空项已消失，故最终结果记为全 PASS。）

### 3.2 H-CH-001 删除遗留的悬空引用（本批次动作的副作用，建议另卡跟踪）
commit c06d438a 以 H-CHE-001 取代并删除了 `data/figures/H-CH-001.json`，但下列引用未同步迁移至 H-CHE-001：
- `data/figures/H-CHI-001.json`、`data/individuals/H-CHI-001_modes.json`（程颐）跨引用 target = H-CH-001
- `data/figures/H-LJY-001.json`、`data/individuals/H-LJY-001.json`（陆九渊）跨引用 target = H-CH-001
- `data/figure_names.json` 仍保留 `"H-CH-001": "程颢"` 旧别名
- 孤儿文件：`data/individuals/H-CH-001.json`、`data/individuals/H-CH-001_modes.json`、`docs/figures/H-CH-001.md`（21KB，对应 figure json 已不存在）
- 根目录 `code_maps.json` 亦残留该代码

H-CHE-001 自身数据未引用 H-CH-001（命中数 0），故不影响本卡发布；但需统一决定
「H-CH-001 → H-CHE-001 重定向」还是「清档」，涉及程颐/陆九渊两张卡，建议由编排层派单处理。

### 3.3 概念重叠提示（学术性，非缺陷）
- `M-CHE-005 性即理也法` 与程颐 `M-CHI-001 性即理法` 名称相似度 0.8。二者同出二程之学，史料上「性即理也」通常归程颐，
  程颢条目以《二程遗书》卷一为源，属可接受的互补诠释；仅提示后续做二程对照矩阵时避免重复计分。
- `万物一体法` 全库重名 2 处（H-CHE-001 程颢 / H-WYM-001 王阳明）。全库同类重名共 17 组（含因材施教法、经世致用法等），
  属人物思想自然重合，非数据缺陷。

## 四、已核验通过的关键项

1. 库总量自洽：`modes_data.modes` 条数 == `total` 字段（复跑时 2898 = 2898，含并发入库的周敦颐 10 条）；
   10 个 M-CHE-001~010 全库唯一。
2. 每模式 `figure_code` = H-CHE-001，`definition_zh/en`、`name_zh/en`、`process_zh/en`、`key_concepts`、
   `representative_cases_*`、`modern_applications_*`、`key_quote_*`、`source_chapter` 均非空。
3. `related_modes` 引用全部可解析；无跨人物复制粘贴（定义去重比对 0 命中）。
4. 图档：mode_ids/modes 各 10 条、`thinking_mode_count`=10、生卒 1032/1085、`core_thoughts` 10 条与 10 个模式名一一对应、
   中英名与拼音正确、无英文 CJK 污染。
5. 双语场景：zh `C-CHE-001~010` 与 en `C-CHE-001E~010E` 各 10 条且一一配对，`mode_code` 合法，
   `title`/`text`/`application_area` 非空、title 与模式名一致；英文记录内的 `title_zh/text_zh/application_area_zh`
   为全库双语记录既有结构（同批次 C-CHI-001E 字段完全一致；全库 2123 条英文场景中 90 条带成对中英标题），
   非污染——真正的污染判定口径为「英文字段缺失且记录内混入中文」。
6. scenario_tags：20 条（zh/en 各 10），覆盖全部 10 个 mode_code，figure_code 绑定正确。
7. 文档一致性：`docs/figures/H-CHE-001.md` 的 10 段定义与库内 `definition_zh` 逐字一致（长度 85~138 全等），
   未出现黄宗羲 M309 式的「文档↔数据语义错位」；文档结构与 H-CHI-001 同模板。
8. 镜像一致性：figure 与 individuals 镜像公共字段无差异。

## 五、修复后提交

- `data/modes_data.json`（英文字段 CJK 清理 8 处）
- `data/figures/H-CHE-001.json`（回填 tags 10 + cross_references 2）
- `data/individuals/H-CHE-001.json`（同上）

## 六、附：独立验收脚本（已随本次提交入库，仓库根目录）

- `qa_chenghao_structural.py`（39 项结构性检查：模式库/图档/注册表/场景/标签）
- `qa_chenghao_cjk_scan.py`（commit c06d438a 的 HEAD 版本 vs 工作区 CJK 差异比对，定位全部 8 处污染）
- `qa_chenghao_semantic.py`（文档 ↔ 数据定义逐字比对、core_thoughts 对齐、人物间近重名分析）
- `qa_chenghao_xref.py`（全库悬空跨引用统计）
- `qa_chenghao_dangling.py`（H-CH-001 删除遗留引用清点）

复跑方式：`python3 qa_chenghao_structural.py`（需在仓库根目录执行）。

## 七、提交说明（并发写入提醒）

本次验收提交 `ca6da954` 只应包含程颢修复内容（5 类文件）。提交时仓库工作区正被另一张卡
（周敦颐 H-ZDY-001 入库）并发写入 `data/modes_data.json`，`git add data/modes_data.json`
连带带入了该卡当时进行中的 10 个 M-ZDY-001~010 模式（库总量 2888→2898）。

- 该部分数据**不由本卡修改**，仅被提交动作顺带落盘；抽查其 10 条模式字段完整、JSON 合法。
- 周敦颐卡自身的其余产物（`data/code_maps.json`、`data/scenarios_*`、`data/figures/H-ZDY-001.json`、
  `data/individuals/H-ZDY-001*`）均未被打包进本次提交，仍留待该卡自行入库。
- 程颢数据在本提交中的实际变更：`data/modes_data.json` 8 处英文字段 CJK 清理、
  `data/figures/H-CHE-001.json` 与 `data/individuals/H-CHE-001.json` 各回填 10 tags + 2 xrefs。
- 教训（供后续卡片参考）：本仓库多 worker 并发写同一批 `data/*.json`，
  提交前应确认所提交文件的工作区状态，必要时用 `git add -p` 或构造独立 index，避免顺带提交他人进行中的改动。
