# Phase 20 落地实现报告：王阳明（Wang Yangming, H-WYM-001）

- 任务: t_6077a578 (elcano) ← 上游研究 t_18e6db0b (serrano)
- 时间: 20260922_143757
- 研究稿编码: H-WAN-001 / M-WAN-001~010 → 库内编码: **H-WYM-001 / M-WYM-001~010**
- 下游: t_f40f63aa（barbosa 增量合并复核）→ t_cdbbb2d9（espinosa QA）

## 一、编码裁定（关键决策）

库内 `王阳明` 的 canonical code 为 **H-WYM-001**，模式 ID 前缀为 **M-WYM-**，证据链：

1. `data/figure_names.json` 唯一映射 `"H-WYM-001": "王阳明"`；
2. `data/code_maps.json` `figures["H-WYM-001"]` 已注册（figure_name=王阳明，birth/death 1472/1529，school=阳明心学）；
3. `data/figures/H-WYM-001.json`、`data/individuals/H-WYM-001.json`、`data/individuals/H-WYM-001_modes.json`、
   `docs/figures/H-WYM-001.md` 均已存在（Phase 21 建档，commit 9c074ddd / 9e0b8787）；
4. 图档 Phase 21 建档即使用 `M-WYM-001~010`（`modes` / `mode_evidence` 十项），
   且 commit `91832eb6`（"Fix M381-M390 mode ID conflict … align H-WYM-001 code_maps to **M-WYM-001~010** (file prefix)"）
   已由编排层裁定王阳明的模式前缀为 `M-WYM-`，把数字码 M381-M390 让给 Islamic/MENA 语料。

研究稿自动派生码 `H-WAN-001` / `M-WAN-*` 与同一人物既有编码冲突（同一人物不得双码），且 `M-WAN-` 前缀
在本批中同时被其他 card 误用（邻卡 王夫之 t_25de07b9 亦产出 M-WAN-001~010，属批次共性问题），
故落库统一采用 `H-WYM-001` / `M-WYM-001~010`，以每条模式的 `research_mode_id` 字段完整保留研究稿原始 ID
（M-WAN-*），图档另设 `phase20` 溯源块记录 `research_code H-WAN-001 → library_code H-WYM-001` 及 1:1 映射表。
（与同批 陆九渊 H-LUJ-001→H-LJY-001、周敦颐 H-ZHO-001→H-ZDY-001 处理完全一致。）

## 二、写入清单

| 文件 | 变更 |
|---|---|
| `data/modes_data.json` | +10 条 M-WYM-001~010（figure_code=H-WYM-001）；`total` 2908 → **2918** |
| `data/code_maps.json` | `figures["H-WYM-001"]` 重注册（mode_ids 10 + tags 10 模式名 + cross_references 6），figures 208 不变 |
| `data/scenarios_zh.json` | `scenarios_zh` +10 条 C-WYM-001~010（2133 → 2143） |
| `data/scenarios_en.json` | `scenarios_en` +10 条 C-WYM-001E~010E（2133 → 2143） |
| `data/scenario_tags.json` | 旧 10 条 H-WYM-001 条目（mode_id 错指 M403-M412、旧模式名）替换为 20 条新条目；7188 → **7198** |
| `data/figures/H-WYM-001.json` | mode_ids/modes/mode_evidence/core_thoughts/protreptic_mapping/tags/modern_value + `mode_ids_note` + `phase20` 溯源块 + 交叉引用修复；并入 individuals 档案专有字段（biography/core_concepts/key_works/tags_en） |
| `data/individuals/H-WYM-001.json` | 与上 **字节镜像**（三处 SHA256 一致） |
| `docs/figures/H-WYM-001.json` | `data/figures` 字节镜像（**新建**） |
| `data/individuals/H-WYM-001_modes.json` | 新增 `thinking_modes_v6_phase20`（10 条库内格式）+ `modes_ref` + `phase20_note`；Phase 21 建档 `modes` 原样保留 |
| `docs/figures/H-WYM-001.md` | 由 Phase 21 骨架重建为 Phase 20 研究档案（16KB → **46KB**，10 模式全字段中英逐字 + 双语场景索引 + 交叉引用 + 入库说明） |
| `data/individuals/phase20_wangyangming_research.md` | 上游研究稿归档（数据层可溯源） |
| `verify_wangyangming_phase20.py` | 独立验收脚本（仓库根目录，**60/60 PASS**） |

备份：工作区内 `backup_merge_H-WYM-001_20260922_143757/`（9 个文件，未写入仓库以免体积噪声）。

## 三、模式 ID 映射

| 研究稿 | 库内 | 模式名（中 / 英） | 类别 |
|---|---|---|---|
| M-WAN-001 | M-WYM-001 | 心即理法 / Mind-Is-Principle Method | 本体论 |
| M-WAN-002 | M-WYM-002 | 知行合一法 / Unity-of-Knowing-and-Acting Method | 认识论 |
| M-WAN-003 | M-WYM-003 | 致良知法 / Extending-Innate-Knowing Method | 工夫论 |
| M-WAN-004 | M-WYM-004 | 念念察识法 / Discerning-Each-Thought Method | 工夫论 |
| M-WAN-005 | M-WYM-005 | 龙场悟本法 / Longchang Enlightenment Method | 认识论 |
| M-WAN-006 | M-WYM-006 | 四句教心法 / Four-Sentence Teaching Method | 工夫论 |
| M-WAN-007 | M-WYM-007 | 事上磨练法 / Tempering-in-Affairs Method | 工夫论 |
| M-WAN-008 | M-WYM-008 | 人人成圣法 / Everyone-Becomes-Sage Method | 境界论 |
| M-WAN-009 | M-WYM-009 | 心外无物法 / Nothing-Outside-Mind Method | 本体论 |
| M-WAN-010 | M-WYM-010 | 此心光明法 / This-Mind-Is-Luminous Method | 境界论 |

## 四、跨引用（6 条，全部可达）

| 目标 | 关系 | 说明 |
|---|---|---|
| `H-ZHX-001` 朱熹 | vs | **H-ZX-001 → H-ZHX-001**：`H-ZX-001` 在 `figure_names` 中为「曾子」（误码），朱熹 canonical 码为 `H-ZHX-001`；原描述本即「心即理 vs 性即理」之朱王对照 |
| `H-LJY-001` 陆九渊 | inheritance | 陆王心学上下游闭合（逆引用见 `data/figures/H-LJY-001.json`，同批已建立） |
| `H-KZ-001` 孔子 | inheritance | 儒家仁学一以贯之 |
| `H-HZX-001` 黄宗羲 | philosophical_debate | 阳明学→刘宗周→黄宗羲的思想链 |
| `H-DZS-001` 董仲舒 | vs | 内在权威 vs 外在权威 |
| `H-SMQ-001` 司马迁 | comparison | 探究焦点由外在天命转向人的世界 |

## 五、上游研究稿缺陷修复（10 处）

| 类型 | 处数 | 内容 |
|---|---|---|
| 英中混排（`_en` 字段残留中文） | 8 处 | M-WAN-003 `definition_en`「使一切行为皆符合良知。」、`process_en[3]`「使一切行为皆符合良知要求」、`key_quote_en`「to使 all things…」；M-WAN-005 `representative_cases_en[0]`「sudden贯通」；M-WAN-007 `process_en[1]`「nor逃避 affairs」、`process_en[3]`「the境界 of stability」、`representative_cases_en[1]`「not逃避 affairs」；M-WAN-009 `process_en[3]`「使事物在心之观照下各得其所」 |
| 中文串英（`_zh` 字段残留英文） | 1 处 | M-WAN-009 `representative_cases_zh[2]`「意义和 value」→「意义和价值」 |
| 英文粘连 | 1 处 | M-WAN-005 `representative_cases_en[1]`「meaning ofGewu」→「meaning of Gewu」 |

修复后：M-WYM-* 全部 `_en` 字段无 CJK、`_zh` 字段无 3 字母以上拉丁词（脚本第 10/11 项断言）。

## 六、验收要点（`python3 verify_wangyangming_phase20.py`，60/60 PASS）

1. 库内 10 条 M-WYM-001~010；`total=2918 == len(modes)`；figure_code 全为 H-WYM-001
2. 每条含中英名称/定义/流程/关键概念/源文引证/代表案例/现代应用 + `research_mode_id` + `verification`
3. 语言纯度：M-WYM-* 与 C-WYM 场景均无混排；上游 10 处缺陷零残留
4. 源研究档（individuals `thinking_modes_v6_phase20`）与主库条目逐字一致；Phase 21 `modes` 保留未动
5. 场景 zh/en 各 10，`mode_code` 与模式一一对应，标题与模式名一致
6. scenario_tags 20 条覆盖 10 个 mode_code（zh/en 各 10），旧 M403-M412 错码条目已清除
7. code_maps 注册 + mode_ids/tags 一致 + 6 条交叉引用无悬空
8. 图档三处镜像 SHA256 一致；`mode_evidence`/`protreptic_mapping`/`core_thoughts` 覆盖 10 模式
9. 档案 md 46KB > 20KB、10 模式定义中英逐字等于库内、无「…」截断
10. `related_modes` 无悬空；全库具名 mode_id 无重复；`figure_names` 唯一登记、无 H-WAN 派生码

## 七、遗留与提示（非本卡范围）

- `data/modes_data.json` 中遗留的数字码条目 **M381-M390（figure_code=H-WYM-001，王阳明旧浅层模式）** 不在本卡处理范围：
  按 commit `91832eb6` 的裁定这批数字码属 Islamic/MENA 语料（"Keep tools/modes_data.json M381-390 intact"），
  且被 `H-EUC-001` / `H-TXZ-001` / `H-ARC-001` 等图档的 `related_modes` 引用（改动会引入悬空）。
  本卡零触碰，已列入待裁定清单供编排层统一归一化。
- `data/figure_names.json` 存在历史重复登记：`"H-WY-001": "王阳明"` 与 `"明": "王阳明"`（非本卡产物，
  无任何文件引用 H-WY-001），本卡未改动该文件；如需清理建议单开一致性卡。
- `api/data/`、`web/`、`site_docs/`、`tools/` 下的数据副本未同步（同批 Phase 20 卡均只写 `data/` 与 `docs/`）。
- hotspot: `data/modes_data.json`、`data/code_maps.json`、`data/scenario_tags.json` 为多卡共享大文件，
  本卡仅追加自身足迹（+10 模式 / 1 figure 条目 / 20 标签）。

## 八、复现命令

```
cd /opt/data/workspace/Protreptic
python3 verify_wangyangming_phase20.py     # 60/60 PASS
```
