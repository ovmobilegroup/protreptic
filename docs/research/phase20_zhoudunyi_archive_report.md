# Phase 20 文档归档报告：周敦颐（Zhou Dunyi, H-ZDY-001）

- 任务: t_d88ee5b6（pigafetta）← 上游数据/QA: t_0e566445（espinosa，独立深检 21/21 PASS、修复差异 22/22 PASS）
- 时间: 2026-09-22 14:35 CST
- 人物码: H-ZDY-001（canonical）/ 上游研究稿: `docs/research/phase20_zhoudunyi_research.md`（研究稿派生码 H-ZHO-001）
- 数据落地提交: `564a5f58`（elcano, t_a7fc5052，10 模式 M-ZDY-001~010 + 10+10 双语场景 + scenario_tags +20 + code_maps 注册）
- 验收热修提交: `dc15c89a`（修复中英混排/字符缺陷 10 类 11 处，三镜像同步）+ 报告 `98d7ddd1` / `65ead7c9` / `235935cb`
- 本卡验收脚本: `qa_zhoudunyi_archive.py`（56 项：54 PASS / 1 WARN / 0 FAIL）

## 一、归档范围与结论

数据层已由上游卡验收通过，本卡只处理「人可读文档层」与「登记表/镜像一致性」，不重复数据返工。

| 项 | 归档前 | 归档后 |
|---|---|---|
| `docs/figures/H-ZDY-001.md` | 53,244B / 289 行；模式小节缺 `领域`（中英）、`研究稿ID` 溯源、`操作步骤(EN)`、`代表性案例(EN)`、`当代应用(EN)`；无双语场景索引、无现代价值节；入库说明仅 4 条 | 75,835B / 524 行；10 条模式全字段中英齐全、逐字等于库内；新增「四、双语场景索引（10 对）」「六、现代价值（5 条）」；入库说明升级为「七、入库说明与 QA 验收记录」 |
| `docs/figures/H-ZDY-001.json` | 已存在 | 保持（三镜像 SHA256 一致，本卡逐项复核） |
| `data/figure_names.json` | 已登记 canonical 码 H-ZDY-001→周敦颐，无旧码 H-ZHO-001 | 无需改动（本卡复核确认） |
| `docs/research/phase20_summary.md` | 周敦颐行已由程颢归档卡填入模式区间与映射 | 无需改动（本卡复核数据与库内实测一致） |
| `CHANGELOG.md` | 无周敦颐归档条目 | 新增 Phase 20 周敦颐归档条目 |
| `build_zhoudunyi_archive.py` / `qa_zhoudunyi_archive.py` | 缺失 | 生成器（库数据驱动、幂等）+ 56 项验收脚本 |

结论：**H-ZDY-001 文档层与库内数据双向逐字一致，章节体例与同批最新档案（H-LJY-001）对齐，56 项检查 0 FAIL。**

## 二、本次修复/补齐的文档缺陷（5 类）

### 缺陷 1：模式小节缺双语字段（P1，影响站点可读性与对外一致性）
`docs/figures/H-ZDY-001.md` 每条模式只有中文正文，缺 `领域`（中英）与 `操作步骤(EN)`/`代表性案例(EN)`/`当代应用(EN)`；而同批 `H-LJY-001.md`（14:09 归档）已含全套中英字段。对照库内 `data/modes_data.json`，这些字段全部存在且非空——即文档层比数据层少了约 40% 的可发布内容。

**修复**：以库内字段为唯一数据源补齐（`domain_zh/domain_en`、`process_en`、`representative_cases_en`、`modern_applications_en`），不改写任何既有中文正文（生成器内置「既有行保留」安全网 + 逐字校验）。

### 缺陷 2：缺研究稿 ID 溯源行（P2，可追溯性）
模式小节未标注 `research_mode_id`（M-ZHO-*）。上游为研究稿派生码 H-ZHO-001 落库统一改码 H-ZDY-001 的典型案例，缺少逐条溯源会让「研究稿→库内码」的映射只留在提交信息里。

**修复**：在 `类别` 行尾追加 `| **研究稿ID**: M-ZHO-00N`（与 H-LJY-001 体例一致，10 条模式全覆盖）。

### 缺陷 3：无双语场景索引（P2，场景层无法从文档侧核验）
库内已有 `C-ZDY-001~010 / C-ZDY-001E~010E` 双语场景与 20 条 `scenario_tags`，但档案 md 未列任何场景。

**修复**：新增「四、双语场景索引」，按 `scenarios_zh/en.json` 逐对列出（标题中文名 + `text_zh` + `text_en` 逐字，10 对）。

### 缺陷 4：无现代价值章节（P3，图档字段未落到人读层）
图档 `data/figures/H-ZDY-001.json` 的 `modern_value_zh`（5 条）在 md 中完全未体现。

**修复**：新增「六、现代价值」，逐条取自图档 `modern_value_zh`。

### 缺陷 5：入库说明未含 QA 验收轨迹（P3）
原「五、入库说明」仅记录入库总量与 ID 映射，未记录验收热修、脚本与报告位置，读者无法从档案回溯"这条内容被谁验过、怎么验的"。

**修复**：升级为「七、入库说明与 QA 验收记录」，补记落地/热修提交号、验收报告路径、三镜像 SHA 一致、库总量口径（2898→2908 的原因）、两个独立脚本。

## 三、跨引用（已核验）

档案 md 第五节列 3 条跨引用，与 `code_maps.json` 的 `figures.H-ZDY-001.cross_references` 完全一致（描述逐字）：

| 目标 | 关系 | 反向引用状态 |
|---|---|---|
| H-ZZ-001 张载 | contemporary_complementary_ontology | 单向（张载档案未回引周敦颐，属张载卡范围） |
| H-CHE-001 程颢 | teacher_of_disciples | 双向（程颢档案回引 H-ZDY-001） |
| H-CHI-001 程颐 | teacher_of_disciples | 双向（程颐档案回引 H-ZDY-001） |

## 四、未解决遗留（非本卡引入，已定位归属）

| 遗留 | 位置 | 归属/性质 |
|---|---|---|
| 图档 JSON 跨引用集合 ≠ code_maps 集合：图档为 H-ZZ-001/H-WB-001/H-GX-001，code_maps 与 md 为 H-ZZ-001/H-CHE-001/H-CHI-001 | `data/figures/H-ZDY-001.json`、`data/individuals/H-ZDY-001.json`、`docs/figures/H-ZDY-001.json`（三镜像字节一致） | **库级既有基线**：实测 173/364 人物图档存在同类偏差；上游 QA 卡已裁定保留（"figure-json xref set != code_maps xref set (baseline 19/205)"）。本卡不代改，避免推翻上游验收结论 |
| H-WB-001 / H-GX-001 未在 `code_maps.figures` 注册（图档文件存在） | `data/code_maps.json` | 库级基线（未注册跨引用目标共 529 个，含大量历史别名），需专项卡统一 |
| 张载（H-ZZ-001）单向引用周敦颐，未回引 | `data/figures/H-ZZ-001.json`、`code_maps.H-ZZ-001` | 张载卡范围，本卡未代改 |
| `docs/figures/*.json` 镜像覆盖率 62/364，而 md 覆盖 213 | `docs/figures/` | 库级体例缺口（历史人物未建 JSON 镜像），非本卡引入 |
| 工作区并发改动：`data/modes_data.json`、`data/figure_names.json`、`data/figures|individuals/H-CHI-001*.json` 在本次运行期间被程颐卡（a497c57a 系列）持续写入 | 共享大文件 | 本卡提交走 hash-object/commit-tree/update-ref 管道，仅落自己的 5 个文件，未卷入任何在飞改动 |
| 仓库索引滞后：`docs/research/phase20_zhoudunyi_qa_evidence.txt` 处于「已暂存删除」而工作区文件与 HEAD blob 字节一致（SHA 10ad5b99…） | 仓库索引 | 上游卡管道提交留下的索引陈旧状态，本卡未动该文件、未动索引 |
| 未跟踪备份目录 `data/backup_merge_H-ZDY-001_20260922_*`（3 个） | 仓库根 | 上游合并备份，建议归档卡统一清理或加 .gitignore（本卡未删） |

## 五、验收证据

`python3 qa_zhoudunyi_archive.py`（仓库根目录，56 项）：

- 数据层（11）：模式 10 条 / ID 连续唯一 / 中文名唯一 / 优先级 1~10 / 必填字段（含中英 20 项）无空缺 / 英文字段无中文污染 / 中文叙述无未译英文夹杂 / `total` 自洽（2908） / 每条 `verification=verified` / `research_mode_id` M-ZHO-* 全保留 / phase20 映射表一致
- 镜像层（7）：mode_ids 与库一致 / thinking_mode_count=10 / tags≥40 / individuals↔figures 字节一致 / docs JSON 与两者字节一致 / 跨引用目标图档存在 / 跨引用集合一致性（WARN，库级基线）
- 文档层（24）：md>70KB / 10 模式小节 / 章节一~七齐全 / 头部模式区间 / 中英定义·原文依据·操作步骤·代表性案例·当代应用逐条逐字 / 领域行中英 / 研究稿ID 行 / 关键概念·关联模式 / 无截断省略号 / 双语场景索引 10 对逐字 / 现代价值逐条 / 跨引用说明 / QA 记录节
- 登记层（6）：code_maps 注册 + mode_ids + tags + 目标可达；figure_names canonical / 无旧码 / 无重复别名
- 场景层（7）：中英场景各 10 / mode_code 配对 / 标题与模式名一致 / scenario_tags 20 条覆盖 10 模式，中英各 10
- 报告（1）：本报告存在

结果：**PASS 54 / WARN 1（库级基线）/ FAIL 0**（退出码 0）。

生成器幂等性：`python3 build_zhoudunyi_archive.py` 二次运行输出 `已是归档体例（UNCHANGED）`，md SHA256 不变（`875f5d580b7b4cc7f0d6e0c953840514347d06413dce1f9a4a526154d609bfa3`）。

回归核验：上游数据层脚本 `python3 qa_zhoudunyi_deep.py` 仍为 21 PASS（本卡未触碰 modes_data/图档数据）。

## 六、协作与热点

- **hotspot: `data/modes_data.json`** —— 多卡并发整文件重写（本卡运行期间程颐卡持续写入）；本卡只读，不提交。
- **hotspot: `data/figure_names.json`** —— 全库共享登记表，程颢/程颐/陆九渊卡并发写入；本卡只读校验（无需改动）。
- **hotspot: `docs/figures/H-ZDY-001.md`** —— 上游热修（dc15c89a）与本卡归档先后改写同一文件；本卡在其 HEAD 版本上做纯增量补齐，未删改任何既有行（生成器安全网可证）。
