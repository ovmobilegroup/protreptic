# Phase 20 程颐 (H-CHI-001) 数据入库 + 合并校验报告

日期: 2026-09-22
负责人: elcano (kanban t_caa7ba47, [Phase 20] 落地实现: 程颐 数据入库)
上游研究: t_7ab0747b（研究稿 /opt/data/workspace/Protreptic/data/individuals/phase20_chengyi_research.md）
下游: t_c64453b8 数据合并（barbosa）→ 验收子卡

## 一、入库产物（库内 canonical 码）

| 项目 | 内容 |
|---|---|
| 图档码 | H-CHI-001（程颐 / Cheng Yi，伊川先生） |
| 思维模式 | M-CHI-001 ~ M-CHI-010（10 条 v6，全部 figure_code=H-CHI-001） |
| 模式名 | 性即理法 / 主敬涵养法 / 格物穷理法 / 体用一源法 / 理一分殊法 / 渐进贯通法 / 存理灭欲法 / 先知后行法 / 经学入德法 / 内外一理法 |
| 双语场景 | C-CHI-001 ~ C-CHI-010（zh）+ C-CHI-001E ~ C-CHI-010E（en），共 20 条 |
| 场景标签 | scenario_tags 新增 20 条（figure_code=H-CHI-001，10 zh + 10 en） |
| code_maps | figures.H-CHI-001 注册（mode_ids + tags + cross_references） |
| 图档文件 | data/figures/H-CHI-001.json（镜像 data/individuals/H-CHI-001.json）、docs/figures/H-CHI-001.md |
| 库规模 | 模式总数 2878 → 2888（本次入库），当前 HEAD 合计 2898（含后续周敦颐批次） |

## 二、验收结果

独立验收脚本：`verify_chengyi_phase20.py`（仓库根目录），**29/29 PASS**：

1. M-CHI-001~010 全部在库；库 total=2898 与 modes 长度一致
2. 每条模式含中英名称、中英定义、中英流程、关键概念、源文引证、代表案例、现代应用、verification
3. M-CHI 全批无英中混排污染（_en 字段无中文 / _zh 字段无英文）
4. 源研究档 data/individuals/H-CHI-001_modes.json 10 模式、无混排污染
5. 双语场景 zh 10 条 + en 10 条，mode_code 与模式一一对应，双语无混排
6. scenario_tags 20 条且覆盖 M-CHI-001~010
7. code_maps figure 注册完整、交叉引用无悬空
8. related_modes 无悬空引用
9. 图档 JSON 与文档 md 覆盖 10 模式、无混排污染

## 三、本次修复（在上一运行崩溃后的重跑中完成）

上一运行（run 9644）在 `git commit` 时被 API 中断，提交已落地（927f7d7f），但复核发现 4 类缺陷并修复：

1. **英中混排污染 12 处（库）+ 9 处（源研究档）**：M-CHI-003/006 的 `definition_en` / `process_en` / `key_quote_en` 内含「贯通」，M-CHI-001/003/006 的 zh 字段内含 "pure and good" / "unseen" / "for"（其中 `key_quote_zh`「在人 for性」为讹字，已按《河南程氏遗书》原文更正为「在人为性，主于身为心」）。→ 清理后 EN 字段 0 命中、ZH 字段 0 命中。
2. **悬空交叉引用 2 处**：`data/figures/H-CHI-001.json` 与 `data/code_maps.json` 中 target_figure_code = `H-CH-001`（程颢 Phase 21 基础版旧码，已由 H-CHE-001 取代并从 code_maps 移除）→ 更正为 `H-CHE-001`，悬空引用归零。
3. **代表案例字段缺失 9 条**：M-CHI-002~010 缺 `representative_cases_zh/en`（同批 CHE/ZDY/HZX 均有），已依上游研究稿 data/individuals/H-CHI-001_modes.json 回填（每模式 3 条中英对照，与 M-CHI-001 既有精简体例一致），并在 verification 中记录 `case_backfill`。
4. **图档双镜像缺失**：新增 data/individuals/H-CHI-001.json（与 data/figures/H-CHI-001.json 内容一致），对齐「图档双镜像」条约定。

## 四、非本次范围的历史遗留（供编排与后续批次参考）

- `data/modes_data.json` 中 id 为 None 的历史条目 400 条（旧批次遗留），与本次入库无关。
- 全库 `_en`/`_zh` 字段混排污染存量较大（跨约 1155 处，主要在既有人物与场景文件），本次仅清理 H-CHI-001 自身足迹；建议单开一张「全库双语字段语言净化」卡统一处理。
- `data/backup_merge_H-CHE-001_20260922_122743/` 为程颢合并期备份目录，随上一运行被一并提交（仓库体积噪声），本次未删除以免影响并行中的程颢/周敦颐工作流。

## 五、复现命令

```
cd /opt/data/workspace/Protreptic
python3 verify_chengyi_phase20.py     # 29/29 PASS
```

## 六、给下游（barbosa t_c64453b8）的提示

- 本次提交只包含 H-CHI-001 足迹文件，未触碰并行中的其他工作者改动（data/figure_names.json、docs/figures/H-CHE-001.md、docs/research/phase20_summary.md 等未提交变更不在本卡范围内）。
- 增量核对要点：modes_data 中 M-CHI-001~010 十条 + scenario_tags 20 条 + scenarios zh/en 各 10 条 + code_maps figure 1 条 + 图档双镜像 + 文档 md。

---

## 七、下游数据合并复核与收口（barbosa t_c64453b8，2026-09-22）

复核对象：commit `3d504236`（上游入库复核与修复），工作区 canonical 文件逐项独立核验
（脚本 `verify_chengyi_indep.py`，**401 项断言 401 PASS / 0 FAIL**；上游脚本
`verify_chengyi_phase20.py` **29/29 PASS**）。复核中发现并修复 3 类缺陷：

### 7.1 合并不忠实：库内正文为首轮撰写的精简改写文本（主要缺陷）

- 现象：库内 M-CHI-001~010 的 `definition_zh` 平均 **57 字**，而源档
  `data/individuals/H-CHI-001_modes.json` 全文平均 **149 字**；`key_quote_en`
  被截断（如 M-CHI-001 丢失「在天为命，在义为理，在人为性，主于身为心」的后半句），
  `representative_cases_zh/en` 被改写为短句，`process_*` 被删减。
- 同批兄弟图档对照（库内 `definition_zh` 均值）：程颢 103.6 / 周敦颐 393.6 / 黄宗羲 136.3 /
  张载 155.2 / 萨达特 219.8 / 南泉普愿 258.8 —— 均为源档全文逐字入库（程颢 90 个内容字段中
  87 个与源档逐字一致），**程颐是唯一被精简改写的批次**。
- 定位：精简文本仅存在于库内，由首轮入库提交 `927f7d7f` 写入，源档与研究稿均无此文本；
  上游复核（`3d504236`）只修了污染/悬空引用/案例回填，未发现正文被改写。
- 修复：以源档全文重建库内 M-CHI-001~010 的 73 个内容字段（`apply_chengyi_fulltext_merge.py`，
  幂等，写盘前自检），保留库内 `figure_code` / `verification`，并入源档的
  `representative_figures` 字段。修复后源档与库内 21 个内容字段逐字一致（`verify_chengyi_indep.py`
  逐模式断言）。

### 7.2 源档残留 10 处中英混排污染

上游称已清理「源研究稿 9 处」，但 `data/individuals/H-CHI-001_modes.json` 仍残留：
M-CHI-003/006 的 `process_*`（'unseen' 与 '贯通'）、M-CHI-004/006/009 的
`representative_cases_en`（'困境' / '贯通' / '入门经典'）、M-CHI-009 `process_en`（'入门经典'）。
本次按上游 idiom 清理（贯通→thorough comprehension、困境→predicament、入门经典→gateway classic、
'unseen'→未见），清理后源档 0 命中（未清理直接把源档并入主库会把污染重新引入）。

### 7.3 索引与图档收口

- `data/figure_names.json` 缺 canonical 映射 `"H-CHI-001": "程颐"`（其兄程颢 `H-CHE-001` 与
  周敦颐 `H-ZDY-001` 均已注册），下游 `tools/figure_library.py` 只能回落到 figures/*.json 推断。
  本次补注册（与 `"H-CHE-001": "程颢"` 并列）。
- `data/figures/H-CHI-001.json` 及其镜像 `data/individuals/H-CHI-001.json` 的 `tags` 中
  `"主敬涵养"` 重复 1 次（26 条含 1 重复），与兄弟图档（程颢/周敦颐 tags 无重复）不一致；
  已去重（26→25，保留首次出现），双镜像字节保持一致（md5 相同）。
- `verify_chengyi_phase20.py` 第 2 项断言硬编码 `== 2898`，在并行入库（库已增长到 2908）后
  会误报 FAIL；改为 `total == len(modes) and len(modes) >= 2898` 的自洽断言。

### 7.4 复现

```
cd /opt/data/workspace/Protreptic
python3 verify_chengyi_indep.py        # 401/401 PASS
python3 verify_chengyi_phase20.py      # 29/29 PASS
```

### 7.5 留给下游（QA t_66fa11a9 / 归档 t_c7ad2319）

- `docs/figures/H-CHI-001.md` 仍为入库期骨架件（定义文字取自被改写前的库内文本，尾部以「...」
  截断）。本次已把库内正文恢复为源档全文，md 需由归档卡按程颢同例重建为完整档案
  （含中英全文 + `docs/figures/H-CHI-001.json` 第三镜像）。
- 库内 `None` id 历史条目 400 条、全库中英混排存量为历史基线，不在本卡范围。
- 本卡提交仅含 H-CHI-001 足迹文件；并行卡片的未提交改动（陆九渊入库等）未被夹带。
