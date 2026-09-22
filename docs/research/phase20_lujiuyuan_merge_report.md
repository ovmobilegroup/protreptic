# Phase 20 落地实现报告：陆九渊（Lu Jiuyuan, H-LJY-001）

- 任务: t_3f82e962 (elcano) ← 上游研究 t_ed837a88
- 时间: 20260922_140937
- 研究稿编码: H-LUJ-001 / M-LUJ-001~010 → 库内编码: **H-LJY-001 / M-LJY-001~010**
- 下游: t_75c396cb（barbosa 增量合并复核）→ t_42c77bc7（espinosa QA）

## 一、编码裁定（关键决策）

库内 `陆九渊` 的 canonical code 为 **H-LJY-001**，证据链：

1. `data/figure_names.json` 第 581 行唯一映射 `"H-LJY-001": "陆九渊"`；
2. `data/figures/H-LJY-001.json`、`data/individuals/H-LJY-001.json`、`data/individuals/H-LJY-001_modes.json`、
   `docs/figures/H-LJY-001.md` 均已存在（Phase 21 建档，commit 709ba6ee）；
3. `data/figures/H-LJY-001.json` 的 `core_thoughts` 十项恰为 *心即理法 / 宇宙本体法 / 发明本心法 /
   易简工夫法 / 义利之辨法 / 先立其大法 / 切己自反法 / 尊德性为先法 / 本体即用法 / 六经注我法* ——
   与上游研究稿 M-LUJ-001~010 一一对应（同序），说明图档本就为该研究脉络所建；
4. 邻卡文档 `docs/research/phase20_chenghao_archive_report.md`（第 58 行）已把「H-LJY-001 → H-CH-001 悬空引用」
   归入「陆九渊流水线 t_3f82e962 / t_75c396cb / t_42c77bc7」，即编排层已认定 H-LJY-001 为本卡产物码。

研究稿自动派生码 `H-LUJ-001` 与同一人物既有编码冲突，**同一人物不得双码**，故落库统一采用 `H-LJY-001`，
模式 ID 统一为 `M-LJY-001~010`，并以每条模式的 `research_mode_id` 字段完整保留研究稿原始 ID（M-LUJ-*），
图档另设 `phase20` 溯源块记录 `research_code H-LUJ-001 → library_code H-LJY-001` 及 1:1 映射表。
（与同批周敦颐 H-ZHO-001→H-ZDY-001 的处理完全一致。）

## 二、写入清单

| 文件 | 变更 |
|---|---|
| `data/modes_data.json` | +10 条 M-LJY-001~010（figure_code=H-LJY-001）；`total` 2898 → **2908** |
| `data/code_maps.json` | 注册 `figures["H-LJY-001"]`（mode_ids 10 + tags 10 + cross_references 3），figures 207→208 |
| `data/scenarios_zh.json` | `scenarios_zh` +10 条 C-LJY-001~010（2133） |
| `data/scenarios_en.json` | `scenarios_en` +10 条 C-LJY-001E~010E（2133） |
| `data/scenario_tags.json` | +20 条（zh/en 各 10，figure_code=H-LJY-001），7168→7188 |
| `data/figures/H-LJY-001.json` | mode_ids/modes/mode_evidence/protreptic_mapping/tags/source_files 更新 + `mode_ids_note` + `phase20` 溯源块 + 交叉引用修复 |
| `data/individuals/H-LJY-001.json` | 与上同步（**字节镜像**，补 `figure_name` 字段） |
| `docs/figures/H-LJY-001.json` | `data/figures` 字节镜像（新建；三处 SHA256 一致） |
| `data/individuals/H-LJY-001_modes.json` | 新增 `thinking_modes_v6_phase20`（10 条库内格式）+ `modes_ref` + `phase20_note`；**Phase 21 建档 `thinking_modes` 原样保留** |
| `docs/figures/H-LJY-001.md` | 重建为 Phase 20 研究档案（14KB → 48KB，10 模式全字段中英逐字 + 双语场景索引 + 交叉引用 + 入库说明） |
| `data/individuals/phase20_lujiuyuan_research.md` | 上游研究稿归档（数据层可溯源） |
| `verify_lujiuyuan_phase20.py` | 独立验收脚本（仓库根目录，**51/51 PASS**） |

备份：工作区内 `backup_merge_H-LJY-001_20260922_140937/`（9 个文件，未写入仓库以免体积噪声）。

## 三、模式 ID 映射

| 研究稿 | 库内 | 模式名（中 / 英） |
|---|---|---|
| M-LUJ-001 | M-LJY-001 | 心即理法 / Mind-As-Principle Method |
| M-LUJ-002 | M-LJY-002 | 宇宙本体法 / Cosmic-Body Method |
| M-LUJ-003 | M-LJY-003 | 发明本心法 / Discovering Original Mind Method |
| M-LUJ-004 | M-LJY-004 | 易简工夫法 / Easy-and-Simple Cultivation Method |
| M-LUJ-005 | M-LJY-005 | 义利之辨法 / Righteousness-vs-Interest Discrimination Method |
| M-LUJ-006 | M-LJY-006 | 先立其大法 / First-Establish-the-Great Method |
| M-LUJ-007 | M-LJY-007 | 切己自反法 / Self-Reflection Method |
| M-LUJ-008 | M-LJY-008 | 尊德性为先法 / Honoring Moral Nature First Method |
| M-LUJ-009 | M-LJY-009 | 本体即用法 / Substance-As-Function Method |
| M-LUJ-010 | M-LJY-010 | 六经注我法 / Six Classics As Footnotes Method |

## 四、跨引用（均已修复，双向可达）

| 目标 | 关系 | 修复说明 |
|---|---|---|
| `H-ZHX-001` 朱熹 | lineage_inheritance_and_inversion | **H-ZX-001 → H-ZHX-001**：`H-ZX-001` 已被曾子占用（figure_names 第 532 行），原引用指向「曾子」为错码；朱熹（1130-1200）方为鹅湖之辩对手 |
| `H-CHE-001` 程颢 | spiritual_ancestry | **H-CH-001 → H-CHE-001**：程颢 canonical 码为 H-CHE-001，旧码 H-CH-001 已随 c06d438a 删除 |
| `H-DZS-001` 董仲舒 | inner_vs_outer_authority | 不变；已在 code_maps 注册，双向对照成立 |

反向引用：`data/figures/H-WYM-001.json`（王阳明）已回引 `H-LJY-001` —— 陆王心学上下游闭合。

## 五、研究稿文字修复（11 处）

| 类型 | 处数 | 内容 |
|---|---|---|
| 英中混排（`_en` 字段残留中文） | 6 字段 | M-LUJ-003 `广泛`→extensive；M-LUJ-004 `浮沉`两次；M-LUJ-005 `志向`三次→aspiration；M-LUJ-006 `分歧`→divergence；M-LUJ-009 `不可分割`→indivisible |
| 专名误译 | 8 处 | `Egg Lake`→`Goose Lake`（鹅湖之会，5 处）；`Jinmen`→`Jingmen`（荆门，3 处） |
| 注音错误 | 2 处 | M-LUJ-002 `(Yuzhou-Wuxin Method)`→`(Yuzhou Benti Method)`；M-LUJ-009 `(Tiyong Yiji Method)`→`(Benti Jiyong Method)` |

修复后：M-LJY-* 全部 `_en` 字段无 CJK、`_zh` 字段无 3 字母以上拉丁词（脚本第 9/10 项断言）。

## 六、验收要点（`python3 verify_lujiuyuan_phase20.py`，51/51 PASS）

1. 库内 10 条 M-LJY-001~010；`total=2908 == len(modes)`；figure_code 全为 H-LJY-001
2. 每条含中英名称/定义/流程/关键概念/源文引证/代表案例/现代应用 + research_mode_id + verification
3. 语言纯度：M-LJY-* 与场景、源研究档均无混排
4. 源研究档与主库条目逐字一致；Phase 21 `thinking_modes` 保留未动
5. 场景 zh/en 各 10，mode_code 与模式一一对应，标题与模式名一致
6. scenario_tags 20 条覆盖 10 个 mode_code（zh/en 各 10）
7. code_maps 注册 + mode_ids/tags 一致 + 交叉引用无悬空
8. 图档三处镜像 SHA256 一致；`mode_evidence`/`protreptic_mapping` 覆盖 10 模式
9. 档案 md > 20KB、10 模式定义中英逐字等于库内、无「…」截断
10. related_modes 无悬空；全库具名 mode_id 无重复；figure_names 唯一登记、无 H-LUJ 派生码残留

## 七、遗留与提示（非本卡范围）

- `H-ZHX-001`（朱熹）尚未在 `data/code_maps.json` 注册（其图档文件存在）——属朱熹卡范围；
  本卡验收脚本对交叉引用采用「code_maps 注册 **或** `data/figures/<code>.json` 存在」双判据。
- 提交时发现仓库索引（index）中存在**回退 dc15c89a（周敦颐验收热修）的陈旧暂存内容**
  （`data/modes_data.json`、`data/individuals/H-ZDY-001_modes.json`、`docs/figures/H-ZDY-001.md` 及
  `qa_zhoudunyi_deep.py` 的删除）。工作区内容正确（等同 HEAD + 本次新增），本卡已用
  `git restore --staged` 将该陈旧暂存清出索引、未触碰任何工作区文件，并以 pathspec 精确保交本次足迹。
- `api/data/`、`web/`、`tools/` 下的数据副本未同步（同批 Phase 20 卡均只写 `data/` 与 `docs/`），
  其同步由专门的一致性卡统一处理。
- hotspot: `data/modes_data.json`、`data/code_maps.json`、`data/figure_names.json` 为多卡共享大文件，
  本卡仅追加自身足迹（+10 模式 / +1 figure / 未改 figure_names）。

## 八、复现命令

```
cd /opt/data/workspace/Protreptic
python3 verify_lujiuyuan_phase20.py     # 51/51 PASS
```
