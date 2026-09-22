# Phase 20 QA 验收报告 — 程颐 (Cheng Yi, H-CHI-001)

- 验收卡：`t_66fa11a9`（espinosa，Phase 20 数据质量验收）
- 上游合并卡：`t_c64453b8`（barbosa 数据合并收口，commit `a497c57a`）
- 复核对象：commit `a497c57a`（父 `235935cb`）的工作区 canonical 数据；本次 QA 的修复提交另附
- 结论：**PASS**（经验收热修：1 类缺陷 / 2 处，已修复并复验）

## 一、验收方法

三份脚本相互独立、全部对同一份工作区 canonical 数据运行：

| 脚本 | 来源 | 断言数 | 结果 |
|---|---|---|---|
| `verify_chengyi_phase20.py` | 入库复核（Phase 20 入库存档） | 29 | 29/29 PASS |
| `verify_chengyi_indep.py` | 下游合并复核（barbosa） | 401 | 401/401 PASS |
| `qa_chengyi_deep.py` | **本卡新增独立深检** | 81 | 81/81 PASS |

本卡深检补齐上游两份脚本的覆盖盲区：

1. **语言纯净度全嵌套扫描**：上游 `scan()` 只在 dict 层匹配 `*_en` / `*_zh` 键，列表字段
   （`process_zh/en`、`representative_cases_zh/en`、`modern_applications_zh/en`）内部的字符串
   漏检；本卡按叶子节点全量扫描，并覆盖 `key_concepts`。
2. **源档 ↔ 库内全字段比对**：上游脚本显式比对 14 个字段，本卡比对源档除 `id` / `mode_code`
   外的**全部 21 个内容字段**（含 `category` / `level` / `priority` / `domain_*` /
   `related_modes` / `representative_figures`），逐模式逐字。
3. **交叉引用目标码全足迹核验**：上游只查 `code_maps` 与图档，**源研究档
   `data/individuals/H-CHI-001_modes.json` 的 `cross_references` 从未被任何脚本检查**——
   本次缺陷即由此处发现。
4. 图档双镜像（字节/内容）、tags 去重与关键词覆盖、场景双语配对、`scenario_tags` 20 条、
   `figure_names` 注册、`code_maps` 结构。

## 二、验收与修复

### 2.1 主项：合并忠实性（复核上游 barbosa 的核心修复）— 通过

- 源档 `data/individuals/H-CHI-001_modes.json` ↔ 库内 `M-CHI-001~010`：**21 个内容字段
  逐模式逐字一致，0 处差异**（源档除 `id` / `mode_code` 外的全部字段）。
- 库内额外字段严格为 `figure_code` / `verification`；库内无字段缺失。
- 库内 10 条模式正文已恢复源档全文（此前为首轮入库的精简改写文本），与同批兄弟图档
  （程颢/周敦颐/黄宗羲/张载等逐步全文入库）体例一致。
- 源档 ↔ 库内语言纯净度：中文字段 0 处未译英文、英文字段 0 处中文污染（全嵌套扫描）。

### 2.2 本次发现并修复的缺陷（1 类 / 2 处）

**缺陷：源研究档 `data/individuals/H-CHI-001_modes.json` 的 `cross_references` 目标人物码错误**
（图档与 `code_maps` 已在 `3d504236` 更正，源研究档被漏改，导致档案三处不一致）：

| 条目 | 修复前（HEAD `a497c57a`） | 修复后 | 说明 |
|---|---|---|---|
| 程颐 ↔ 程颢（complementary_methods） | `H-CH-001` | `H-CHE-001` | `H-CH-001` 是程颢 Phase 21 基础版**旧码**，`data/figure_names.json` 与 `data/code_maps.json` 中均无此键 → 悬空引用（`docs/figures/H-CH-001.md` 仅存旧档，`data/figures/H-CH-001.json` 不存在） |
| 程颐 ↔ 黄宗羲（critical_inheritance） | `H-ZHX-001` | `H-HZX-001` | `H-ZHX-001` 实为**朱熹**（`data/figure_names.json` = 朱熹）→ 描述文本讲黄宗羲却指向朱熹，**指向错人**（比悬空更隐蔽：脚本的"已注册"检查会放过） |

修复后源研究档 4 条交叉引用全部指向已注册且语义正确的人物码，且与图档
`data/figures/H-CHI-001.json`、`data/individuals/H-CHI-001.json`、`data/code_maps.json`
的 `cross_references` 目标码序列完全一致。修复仅改动 2 行，未触碰任何正文。

### 2.3 其余验收项 — 全部通过

- 10 条 `M-CHI-001~010` 在库且 `figure_code = H-CHI-001`；`related_modes` 无悬空；
  全库具名 mode_id 无重复。
- 图档双镜像 `data/figures/H-CHI-001.json` / `data/individuals/H-CHI-001.json` **字节一致**；
  `tags` 25 条无重复、覆盖 10 模式关键词（`主敬涵养` 去重 26→25 已生效）。
- 双语场景 `C-CHI-001~010` / `C-CHI-001E~010E` 齐备且 `mode_code` 一一对应、无混排污染；
  `scenario_tags` 20 条（zh 10 + en 10）无重复。
- `code_maps.figures["H-CHI-001"]` 注册完整（mode_ids 10 / tags 10 / xrefs 4），根级无重复注册。
- `data/figure_names.json` 已注册 `"H-CHI-001": "程颐"`，与 `"H-CHE-001": "程颢"` 并列。

## 三、非本卡范围（历史基线，供编排参考）

1. **`data/figure_names.json` 存在大量非规范键**（本卡扫描：1100 键中数百条为 `XxxCOHORT`
   式键、`H-HZX-001_modes` / `H-HZX-001_MODES` 式误写键、裸数字/人名键）。与程颐无关，
   但会污染"索引注册完整性"类断言——建议单开全库索引净化卡。
   另注：`verify_chengyi_indep.py` 第 133 项 `figure_names 无重复键` 的断言体是
   `len(json.dumps(fn)) > 0`（恒真），属**空断言**，不具备检查力。
2. **图档 `protreptic_mapping` / `mode_evidence` 为空**：`H-CHI-001` 与 `H-CHE-001` 均为
   `{}` / `[]`，而周敦颐/朱熹/陆九渊已填充。属同批体例差异而非回归；补齐需新增研究内容，
   超出数据质量验收范围，如需统一建议单开卡。
3. **`docs/figures/H-CHI-001.md` 仍为入库期骨架件**（约 4.9KB，含截断「...」），
   且缺第三镜像 `docs/figures/H-CHI-001.json`——已由上游明确交给归档卡 `t_c7ad2319`
   （本卡子卡，pigafetta）按程颢同例重建，不构成本卡阻塞。
4. 库内 `None` id 历史条目 400 条、全库中英混排存量、`data/backup_merge_*` 备份目录噪声，
   均为跨批次历史基线。

## 四、仓库状态告警（非数据缺陷，但会造成误提交）

验收时发现 **git 暂存区（index）停留在被弃用的首轮构造版本**：`data/modes_data.json`、
`data/figures/H-CHI-001.json`、`data/individuals/H-CHI-001_modes.json`（污染版）、
`data/figure_names.json`（缺 H-CHI-001 注册）以及 `verify_chengyi_indep.py` /
`apply_chengyi_fulltext_merge.py` 的暂存删除，均为 `87e02a5c` 重跑前的残留。
工作区文件本身与 HEAD 一致，但**任何不加 pathspec 的 `git commit` 都会把污染版正文回写进库**。
本次 QA 提交因此使用 `git commit --only <paths>` 定点提交，未触碰暂存区其他内容；
建议编排侧在无并行写者时执行 `git reset`（不改工作区）清理该残留。

## 五、复现

```
cd /opt/data/workspace/Protreptic
python3 verify_chengyi_phase20.py    # 29/29 PASS
python3 verify_chengyi_indep.py      # 401/401 PASS
python3 qa_chengyi_deep.py           # 81/81 PASS
```

## 六、给归档卡 `t_c7ad2319`（pigafetta）的交接

- 库内正文已是源档全文（10 模式 / 73 内容字段），`docs/figures/H-CHI-001.md` 请按
  `docs/figures/H-CHE-001.md`（29.8KB 完整档案）体例重建，并补第三镜像
  `docs/figures/H-CHI-001.json`（三处 SHA256 一致）。
- **交叉引用请以修复后的源档为准**：程颢 `H-CHE-001`、周敦颐 `H-ZDY-001`、张载 `H-ZZ-001`、
  黄宗羲 `H-HZX-001`（勿再使用 `H-CH-001` / `H-ZHX-001`）。
- `data/figure_names.json` 的 `H-CHI-001` 注册已由上游完成，无需重复处理。
