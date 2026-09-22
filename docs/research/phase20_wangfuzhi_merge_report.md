# Phase 20 落地实现报告：王夫之（Wang Fuzhi, H-WFZ-001）

- 任务: t_eb872f66 (elcano) ← 上游研究 t_25de07b9
- 时间: 20260922_145939
- 研究稿编码: H-WAN-001 / M-WAN-001~010 → 库内编码: **H-WFZ-001 / M-WFZ-001~010**
- 下游: t_5626cc36（barbosa 增量合并复核）→ t_ef2f2b30

## 一、编码裁定（关键决策）

库内 `王夫之` 的 canonical code 为 **H-WFZ-001**，证据链：

1. `data/figure_names.json` 第 587 行唯一映射 `"H-WFZ-001": "王夫之"`（`H-WAN-*` 在该表中无任何登记）；
2. `data/figures/H-WFZ-001.json`、`data/individuals/H-WFZ-001.json`、
   `data/individuals/H-WFZ-001_modes.json`、`docs/figures/H-WFZ-001.md` 均已存在
   （Phase 21 建档，后经 Phase 21 QA `1ddcb8ed`、Phase46-R 审计 `3780e43b` 修字段）；
3. 上游研究稿自动派生码 `H-WAN-001` 系「王 + 拼音首字母」机械派生，**与同批王阳明 Phase 20 研究稿
   （t_18e6db0b，同样派生为 H-WAN-001）重复**，属派生码冲突而非人物编码；
4. 任务卡 t_5626cc36 与编排层均以 figure_code=WangFuzhi / 本卡足迹为准。

故落库统一采用 `H-WFZ-001`，模式 ID 统一为 `M-WFZ-001~010`，每条模式以 `research_mode_id`
字段完整保留研究稿原始 ID（`M-WAN-*`），图档另设 `phase20` 溯源块记录
`research_code H-WAN-001 → library_code H-WFZ-001` 及 1:1 映射表。

## 二、写入清单

| 文件 | 变更 |
|---|---|
| `data/modes_data.json` | +10 条 M-WFZ-001~010（figure_code=H-WFZ-001）；`total` 2918 → **2928** |
| `data/code_maps.json` | 首次注册 `figures["H-WFZ-001"]`（mode_ids 10 + tags 10 + cross_references 2），figures 208→209 |
| `data/scenarios_zh.json` | `scenarios_zh` +10 条 C-WFZ-001~010（2143→2153） |
| `data/scenarios_en.json` | `scenarios_en` +10 条 C-WFZ-001E~010E（2143→2153） |
| `data/scenario_tags.json` | +20 条（zh/en 各 10，figure_code=H-WFZ-001），7198→7218 |
| `data/figures/H-WFZ-001.json` | mode_ids/modes/mode_evidence/protreptic_mapping/tags/source_files 更新 + `mode_ids_note` + `phase20` 溯源块 |
| `data/individuals/H-WFZ-001.json` | 与上同步（**字节镜像**，并合入 individuals 专有字段 description_zh/en、key、pseudonym） |
| `docs/figures/H-WFZ-001.json` | `data/figures` 字节镜像（**新建**；三处 SHA256 一致） |
| `data/individuals/H-WFZ-001_modes.json` | 新增 `thinking_modes_v6_phase20`（10 条库内格式）+ `modes_ref` + `phase20_note`；**Phase 21 建档 `modes`（M321~M330）原样保留** |
| `docs/figures/H-WFZ-001.md` | 重建为 Phase 20 研究档案（15.7KB → 52.3KB：10 模式全字段中英逐字 + 双语场景索引 + 交叉引用 + 入库说明） |
| `data/individuals/phase20_wangfuzhi_research.md` | 上游研究稿归档（数据层可溯源） |
| `verify_wangfuzhi_phase20.py` | 独立验收脚本（仓库根目录，**68/68 PASS**） |

备份：工作区内 `backup_merge_H-WFZ-001_20260922_145939/`（10 个文件，未写入仓库以免体积噪声）。

## 三、模式 ID 映射

| 研究稿 | 库内 | 模式名（中 / 英） | 类别 |
|---|---|---|---|
| M-WAN-001 | M-WFZ-001 | 理气相即法 / Principle-Qi Unity Method | 本体论 |
| M-WAN-002 | M-WFZ-002 | 天下惟器法 / Only Concrete Things Exist Method | 存在论 |
| M-WAN-003 | M-WFZ-003 | 日新之化法 / Daily Renewal Method | 变化论 |
| M-WAN-004 | M-WFZ-004 | 继善成性法 / Continue-Good-to-Cultivate-Nature Method | 人性论 |
| M-WAN-005 | M-WFZ-005 | 行可兼知法 / Practice-Encompasses-Knowledge Method | 认识论 |
| M-WAN-006 | M-WFZ-006 | 理在欲中法 / Principle-in-Desire Method | 价值论 |
| M-WAN-007 | M-WFZ-007 | 理势合一法 / Principle-Tendency Unity Method | 历史哲学 |
| M-WAN-008 | M-WFZ-008 | 两端一致法 / Dual-Polarities-Unity Method | 辩证法 |
| M-WAN-009 | M-WFZ-009 | 鉴古酌今法 / Examine-the-Past-to-weigh-the-Present Method | 史学方法论 |
| M-WAN-010 | M-WFZ-010 | 六经开新法 / Open-New-Face-from-Classics Method | 诠释学 |

## 四、跨引用（原有两条，均可达）

| 目标 | 关系 | 说明 |
|---|---|---|
| `H-HZX-001` 黄宗羲 | comparison | 黄重制度设计与学术史、王重形而上建构与历史哲学；code_maps 已注册 |
| `H-GYW-001` 顾炎武 | comparison | 王偏哲学思辨、顾偏实证考据；`data/figures/H-GYW-001.json` 已落地 |

本次未引入新交叉引用，未修改任何 xref 目标码（无错码需修复）。

## 五、研究稿文字修复（9 处）

| 类型 | 处数 | 内容 |
|---|---|---|
| 英中混排/粘连（`_en` 字段残留中文） | 7 字段 | M-WFZ-001 `Understand事物`→`Understand the`；M-WFZ-004 `not先天固定`→`not fixed at birth`；M-WFZ-007 `not套用`→`not mechanically applying`；M-WFZ-008 `and排斥`→`with and exclude`、`and成就`→`and complete`、`'同源异流'`→`'same source, different streams'`；M-WFZ-010 `issue a召唤`→`issue a summons` |
| 中文夹用英文（`_zh` 字段含 3+ 拉丁词） | 2 处 | M-WFZ-005 `先做MVP验证假设`→`先做最小可行产品验证假设`、`在做中学（Learning by Doing）`→`在做中学，边做边学` |

修复后：M-WFZ-* 全部 `_en` 字段无 CJK、`_zh` 字段无 3 字母以上拉丁词（脚本第 11/12/13 项断言）。

## 六、验收要点（`python3 verify_wangfuzhi_phase20.py`，68/68 PASS）

1. 库内 10 条 M-WFZ-001~010；`total == len(modes)`（2918→2928）；figure_code 全为 H-WFZ-001
2. 每条含中英名称/定义/流程/关键概念/源文引证/代表案例/现代应用 + research_mode_id + verification
3. 语言纯度：M-WFZ-* 与双语场景、源研究档均无混排
4. 源研究档与主库条目逐字一致；Phase 21 建档 M321~M330 原样保留且未混入主库
5. 场景 zh/en 各 10，mode_code 一一对应，标题与模式名一致
6. scenario_tags 20 条覆盖 10 个 mode_code（zh/en 各 10，无重复）
7. code_maps 注册 + mode_ids/tags 一致 + 交叉引用无悬空
8. 图档三处镜像 SHA256 一致；`mode_evidence`/`protreptic_mapping` 覆盖 10 模式；
   原有 49 条 tags、core_thoughts 十项、historical_significance/unique_thing 正文**零改动**（与备份逐字比对）
9. 档案 md > 20KB、10 模式定义中英逐字等于库内、含 20 条双语场景索引、无 TODO/替换字符
10. related_modes 无悬空；全库具名 mode_id 无重复；figure_names 唯一登记、无 H-WAN 派生码残留

## 七、遗留与提示（非本卡范围）

- `H-GYW-001`（顾炎武）尚未在 `data/code_maps.json` 注册（其图档文件存在）——属顾炎武卡范围；
  本卡验收脚本对交叉引用采用「code_maps 注册 **或** `data/figures/<code>.json` 存在」双判据。
- 档案 md 中 `……` 仅出现在古籍原文引证行（2 行，与 `data/modes_data.json` 逐字一致），
  系引用省略惯例，全库同类写法 343 行，非截断残留；验收脚本第 58 项按「省略号只允许出现在引证行」判定。
- `api/data/`、`web/`、`tools/` 下的数据副本未同步（同批 Phase 20 卡均只写 `data/` 与 `docs/`），
  其同步由专门的一致性卡统一处理。
- hotspot: `data/modes_data.json`、`data/code_maps.json`、`data/figure_names.json` 为多卡共享大文件，
  本卡仅追加自身足迹（+10 模式 / +1 figure / **未改** figure_names）。
- 本卡提交基线为 `830e3ccb`（含并发 QA 卡对 M-LJY 的 5 处英文字段修复），本卡 diff 内无他卡内容。

## 八、复现命令

```
cd /opt/data/workspace/Protreptic
python3 verify_wangfuzhi_phase20.py     # 68/68 PASS
```
