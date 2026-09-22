# Phase 20 文档归档报告：程颢（Cheng Hao, H-CHE-001）

- 任务: t_dbb56a30（pigafetta）← 上游 QA: t_3f363cbe（espinosa，43 项 42 PASS / 1 WARN / 0 FAIL）
- 时间: 2026-09-22 13:47 CST
- 人物码: H-CHE-001（canonical）/ 上游研究稿: `docs/research/phase20_chenghao_research.md`
- 数据落地提交: c06d438a（10 模式 M-CHE-001~010、10+10 双语场景、scenario_tags +20、code_maps 注册）
- 本卡验收脚本: `qa_chenghao_archive.py`（34 项，全 PASS，见第 5 节）

## 一、归档范围与结论

上游代码/数据层已由 QA 卡验收通过，本卡只处理「人可读文档层」与「登记表一致性」，不重复数据返工。

| 项 | 归档前 | 归档后 |
|---|---|---|
| `docs/figures/H-CHE-001.md` | 6,337B / 160 行，模式定义被截断为「…」，第四节「跨引用」只有标题无内容，无「入库说明」 | 29,797B / 366 行，10 个模式全字段（中英定义逐字、原文依据、操作步骤、案例、当代应用、关联模式）+ 跨引用 + 入库说明 |
| `docs/figures/H-CHE-001.json` | **缺失**（同批周敦颐/荷马均有 json 镜像） | 已建立，与 `data/figures`、`data/individuals` 三处 SHA256 一致 |
| `data/figure_names.json` | `"H-CH-001": "程颢"`（旧码别名，canonical 码 H-CHE-001 **未登记**） | `"H-CHE-001": "程颢"`，旧码别名移除 |
| `docs/research/phase20_summary.md` | 理学脉络表：周敦颐/程颢/程颐 三行均为「暂缺」；数据来源清单缺三人 | 三行填入已核验的模式区间与映射；数据来源、下一步同步更正 |
| `CHANGELOG.md` | 无程颢条目 | 新增 Phase 20 程颢归档条目 |

结论：**H-CHE-001 文档层缺口已补齐，文档 ↔ 数据双向逐字一致，34 项检查全 PASS。**

## 二、修复的文档缺陷（3 项）

### 缺陷 1：人物档案 md 为「骨架件」（P1，直接影响站点）

`docs/figures/H-CHE-001.md` 由数据入库提交 c06d438a 生成，10 个模式的定义均被截断（以「…」结尾），第四节「跨引用」为空标题，且不含入库说明。站点按 `docs/figures/*.md` 渲染人物页，等于对外发布了 10 条残缺定义。

**修复**：以 `data/modes_data.json` 中 `figure_code == H-CHE-001` 的 10 条模式为唯一数据源，按同批 `docs/figures/H-ZDY-001.md` 的档案体例重建（模式小节字段：英文名 / 类别·层级·优先级 / 领域 / 出处 / 定义 / 定义(EN) / 关键概念 / 原文依据(中英) / 操作步骤(中英) / 代表性案例 / 当代应用 / 关联模式）。生成脚本一次成型、无人工改写，故可保证与库内逐字一致（见第 5 节检查项）。

### 缺陷 2：docs JSON 镜像缺失（P2，破坏镜像体例）

同期人物档案体例为「data/figures + data/individuals + docs/figures 三处字节镜像」（周敦颐 H-ZDY-001、荷马 H-HOM-001 均已具备）。H-CHE-001 缺 `docs/figures/H-CHE-001.json`。

**修复**：`cp` 建立镜像并校验 SHA256 三者一致（`40aa4b20d188…`）。

### 缺陷 3：人物名登记表仍指旧码（P1，跨库命名一致性）

`data/figure_names.json` 中程颢登记在已删除的旧码 `H-CH-001` 下，canonical 码 H-CHE-001 反而不在表内（上游 QA 报告第 3.2 节曾把该行列入「旧码遗留」）。该表被 `tools/figure_library.py`、`tools/build_unified_index.py` 作为**第一优先级**人名解析源，旧码条目会让工具按不存在的文件解析程颢。

**修复**：将 `"H-CH-001": "程颢"` 改为 `"H-CHE-001": "程颢"`（原位替换，不新增重复别名；校验：全表「程颢」仅 1 次、`H-CH-001` 已不在表中）。替换后解析回退链仍可覆盖旧码：`figure_library._load_figure_names()` 会从 `data/figures/*.json` 补全 code→name。

## 三、跨引用（已核验双向可达）

| 目标 | 关系 | 说明 |
|---|---|---|
| H-ZZ-001 张载 | debate_on_settling_the_nature | 张载问「定性未能不动，犹累于外物」，程颢答以《定性书》 |
| H-ZDY-001 周敦颐 | teacher_inheritance_and_inversion | 周敦颐令二程「寻孔颜乐处」，程颢答为「仁者浑然与物同体」 |

两项目标在 `data/figures/` 均有实体文件，且 `data/figures/H-ZDY-001.json` 有对程颢的反向引用（teacher_of_disciples），双向闭合。

## 四、未解决遗留（非本卡引入，已定位归属）

上游 QA 报告第 3.2 节指出：c06d438a 删除 `data/figures/H-CH-001.json` 后留下旧码残留。当前残留清单（本卡改动后重新扫描）：

| 残留 | 位置 | 归属 |
|---|---|---|
| 陆九渊跨引用 `target_figure_code = H-CH-001` | `data/figures/H-LJY-001.json`、`data/individuals/H-LJY-001.json`、`data/individuals/H-LJY-001_modes.json`、`data/code_maps.json`（H-LJY-001 条目） | 已在陆九渊流水线内：t_3f82e962（elcano 数据入库）、t_75c396cb（barbosa 合并）、t_42c77bc7（espinosa QA） |
| 孤儿文件 `data/individuals/H-CH-001.json`、`H-CH-001_modes.json`、`docs/figures/H-CH-001.md`（21KB） | 仓库根 | 无归属卡，已另建清理卡（见 completion metadata） |
| 审计/备份/历史报告中的旧码文本 | `data/audit/*`、`data/backup_merge_*`、`docs/research/phase20_chenghao_qa_report.md`、`phase20_chenghao_merge_report.md` | 历史留痕，不改 |
| `data/figures/H-LJY-001.json` 引用 H-CH-001（陆九渊文档同步） | `docs/figures/H-LJY-001.md` | 随陆九渊卡处理 |

另：`data/figure_names.json` 同为共享登记表，程颐（H-CHI-001）也**未登记 canonical 码**（同批周敦颐已登记），属程颐卡范围，本卡未代改，已在完成摘要中标注。

## 五、验收证据

`python3 qa_chenghao_archive.py`（仓库根目录，34 项）：

- 数据层（6）：模式数量 10、ID 连续唯一、名称唯一、必填字段无空缺、英文字段无中文污染、`total` 字段自洽（2898 == len(modes)）
- 镜像层（5）：fig mode_ids 与库一致、tags 10、cross_references 2、individuals↔figures 一致、docs JSON 镜像字节一致
- 文档层（8）：md 存在且 >20KB、10 个模式小节齐全、定义/定义(EN) 逐字等于库内、模式正文无截断省略号、跨引用齐全、含入库说明、头部含模式清单
- 登记层（5）：code_maps 注册 + mode_ids 一致 + tags 非空 + 两目标可达；figure_names canonical 登记、旧码已除、无重复别名
- 场景层（7）：中文场景 10、英文场景 10、按 mode_code 一一配对、标题与模式名一致、scenario_tags 20 条覆盖 10 个 mode_code、中英各 10

结果：**PASS 34 / WARN 0 / FAIL 0**（退出码 0）。

## 六、协作与热点

- **hotspot: `data/figure_names.json`** —— 全库共享人物名登记表，多个 Phase 20 卡同时写入；本卡仅原位替换 1 行，合并时若与程颐/陆九渊卡冲突，取「两人各自 canonical 码登记 + 旧码移除」的并集即可。
- **hotspot: `docs/research/phase20_summary.md`** —— Phase 20 汇总文档，理学脉络表被多卡更新；本卡仅更正周敦颐/程颢/程颐三行（数据来源：`data/modes_data.json` 实测模式区间）。
- 未改动共享大文件 `data/modes_data.json`、`data/code_maps.json`（工作区内有并发 worker 的在飞改动，本卡只读校验）。
