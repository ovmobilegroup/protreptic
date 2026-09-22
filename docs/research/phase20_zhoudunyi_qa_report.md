# Phase 20 QA 验收报告: 周敦颐 (ZhouDunyi / H-ZDY-001)

- QA 卡: `t_0e566445` (espinosa)
- 验收对象: 入库提交 `564a5f58`（Phase 20 周敦颐数据入库，父卡 `t_a7fc5052`）
- 上游复核: `t_78cac52c` (barbosa) 结构复核 PASS（`verify_zdy_indep.py` 78 项：74 PASS / 0 FAIL / 4 WARN）
- 修复提交: **`dc15c89a`**（本次 QA 热修，父提交 `3d504236`）
- 结论: **PASS（经热修）** — 修复后深检 21/21 PASS、修复差异验证 21/21 PASS

所有断言均从 **git object** 读取（`git show <sha>:<path>`），不复用工作区文件，因此
不受同仓并行卡（程颢 H-CHE-001 / 程颐 H-CHI-001 / 李觏 H-LJY-001 等正在改写
`modes_data.json`、`code_maps.json`、`figure_names.json`）影响。

## 一、验收方法（两道独立脚本）

| 脚本 | 视角 | 指向入库提交 `564a5f58` | 指向热修提交 `dc15c89a` |
|---|---|---|---|
| `verify_zdy_indep.py`（父卡，结构/完整性 78 项） | 计数、id、镜像、并发说明 | 74 PASS / 4 WARN / 0 FAIL | 69 PASS / 4 WARN / 5 FAIL |
| `qa_zhoudunyi_deep.py`（本卡，文本质量 21 项） | 混排污染、英文痕迹、模板/占位、镜像 | **4 FAIL**（见第二节） | 21 PASS / 0 FAIL |
| `qa_zhoudunyi_repair_diff.py`（本卡，修复差异 22 项） | 热修只许动编目缺陷点 | — | 22 PASS / 0 FAIL |

说明：父卡脚本指向热修提交时出现的 5 项 FAIL **全部是"相对 `SNAP^` 的合并增量"断言**
（D5/D5b 标签 +20、E7 code_maps 新增、G6/G8 只动 10 条模式/10+10 场景）。热修的父提交
`3d504236` 已包含入库成果，故增量恒为 0 —— 这是断言语义问题，不是数据缺陷；所有
**绝对型**断言（模式计数、id 唯一性、字段非空、镜像一致、无悬空新增等）全部 PASS。

## 二、发现并修复的缺陷（10 类 / 11 处文本点 / 三文件共 29 处替换）

类别 A — 中文叙述夹带未翻译英文（M-ZDY-009「几微洞察法」）

| 字段 | 原文 | 修复后 |
|---|---|---|
| `process_zh[0]` | 关键临界点正在 **approaching** | 关键临界点正在 **逼近** |
| `process_zh[1]` | 全部注意力 **bring** 到当下 | 全部注意力**带到**当下 |
| `process_zh[2]` | 正在 **emerging** 的念头 | 正在**浮现**的念头 |
| `representative_cases_zh[2]` | "几"的 **crucial** 之处 | "几"的**关键**之处 |

类别 B — 英文字符粘连 / 引号与空格错误（M-ZDY-003「诚为本体法」）

| 字段 | 原文 | 修复后 |
|---|---|---|
| `definition_en` | `objectivetruthfulness` / `normativetruthfulness` | `objective truthfulness` / `normative truthfulness` |
| `definition_en` | `the sage''s being`（双单引号） | `the sage's being` |
| `definition_en` | `denotes ' Supreme perfection`（引号后多空格） | `denotes 'Supreme perfection` |
| `representative_cases_en` | `heaven's operation istruth (cheng) … pursue thistruth` | `is truth (cheng) … pursue this truth` |

类别 C — 同形异码字符（M-ZDY-004「五性感动法」）

- `process_en[3]` 的首词为 `Attribut` + **U+0435（西里尔小写 е）**，与拉丁 `e` 视觉同形，
  常规 CJK 污染扫描与人工通读都极易漏过；已改为 `Attribute behavioral responsibility`。

类别 D — 英文错拼（M-ZDY-005「主静立极法」）

- `process_en[0]`、`process_en[2]` 的 `'quiet-vacuuous'` → `'quiet-vacuous'`
  （同模式 `definition_en` 用的正是 `quiet-vacuous`，属笔误而非术语选择）。

根因：入库前的校对只覆盖了"字段非空 / id 一致 / 镜像相等"这类结构性质，缺少
**词级与字符级**的文本校验；中译稿里混入英译残段、英译稿里丢空格与异体字母，
结构复核（父卡 78 项）本质上查不到。

## 三、修复范围与三镜像同步

- `data/modes_data.json`（11 处）
- `data/individuals/H-ZDY-001_modes.json` 的 `thinking_modes_v6_phase20` 块（11 处，与库内逐字一致）
- `docs/figures/H-ZDY-001.md`（7 处，md 侧可见的同批文本）

全库其余部分逐字节不变：除 `M-ZDY-003/004/005/009` 四条模式外无任何模式改动；
`scenarios_zh/en.json`、`scenario_tags.json`、`code_maps.json`、
`data|docs/figures/H-ZDY-001.json`、`data/individuals/H-ZDY-001.json` 均未触碰；
`individuals/*_modes.json.thinking_modes`（Phase 21 原档）逐字节保留；
库总模式 2898 与 `total` 字段不变。

## 四、保留项（WARN / 历史基线，本次未改动）

1. `figure/individuals` json 的 `cross_references` 仍含未注册目标 `H-WB-001`、`H-GX-001`
   （旧档遗留；figure-json 悬空目标全库 92 个为基线），而本次新关系只写进 `code_maps`
   （`H-ZZ-001/H-CHE-001/H-CHI-001` 均已注册）。figure-json×code_maps 目标集不一致在库内
   是常见基线（19/205），建议由后续统一清理卡处理。
2. `individuals/H-ZDY-001_modes.json.thinking_modes` 的 `mode_name_zh` 为 Phase 21 建档名
   （如"无极而太极·无形有理法"），与库内 v6 名不同；该文件定位为 Phase 21 原档保留
   （`phase20_note` 已声明），`H-ZY-001` 同例，属设计选择。
3. 全库 `*_en` 字段含 CJK 属历史基线（`modes_data.json` 内 103 处，多为其它人物）；
   H-ZDY-001 新增资产在本卡检查中为 0 处。
4. `M-ZDY-009.definition_zh` 中的 `（edge awareness）`/`（mindful awareness）` 属通行
   术语括注（库内约 4.89% 的中文字段含英文术语括注），非本次缺陷；`vacuosity` 为库内
   自洽的术语化译法（与 `stillness-vacuosity` 一致），未擅自改词。
5. 并发写提醒：验收期间同仓多卡并行提交（HEAD 由 `9d7c615d`→`3d504236`→本热修）。
   本热修用 `hash-object/commit-tree/update-ref` plumbing 以当期 HEAD 为基座提交，
   **不包含**其它卡未提交的工作区改动（避免重演"提交顺带带入他人改动"）。

## 五、复跑方式

```
cd /opt/data/workspace/Protreptic
python3 qa_zhoudunyi_deep.py                                   # 默认验 HEAD
ZDY_SNAP=564a5f58 python3 qa_zhoudunyi_deep.py                 # 验入库提交（应报 4 FAIL，复现缺陷）
python3 qa_zhoudunyi_repair_diff.py 564a5f58 dc15c89a          # 验热修只动编目缺陷点（22 PASS）
ZDY_SNAP=<full-sha> python3 <父卡>/verify_zdy_indep.py          # 结构复核（绝对断言全 PASS）
```
