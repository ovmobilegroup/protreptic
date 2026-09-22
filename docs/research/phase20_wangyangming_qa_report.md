# Phase 20 QA 验收报告：王阳明（Wang Yangming, H-WYM-001）

- 任务: `t_cdbbb2d9`（QA 审查，espinosa）→ 下游 `t_f7d8763d`（文档归档，pigafetta）
- 被验收提交: `5956dd8b`（Phase 20 数据入库，elcano / t_6077a578；父 `48ff3736`）；上游独立复核: `t_f40f63aa`（barbosa，PASS / 零改动 / 84-84）
- 验收基线: `git show 5956dd8b` 结构 + 工作区落盘内容（含本卡热修）
- 结论: **PASS（经热修）** —— 结构、索引、场景、镜像、档案全部达标；新发现并修复 **5 类 / 14 处** 数据缺陷（每条三镜像同步）+ 图档 4 条 + 研究稿引用 2 处

---

## 一、脚本结果

| 脚本 | 环境 | 结果 |
|---|---|---|
| 上游 `verify_wangyangming_indep.py`（84 项，barbosa） | 冻结快照（git archive，48ff3736 vs 5956dd8b） | 84/84 PASS（本卡复跑确认） |
| 上游 `verify_wangyangming_phase20.py`（60 项，elcano） | 冻结快照 `5956dd8b` | 60/60 PASS（上游记录） |
| 本卡独立 `verify_wym_qa_espinosa.py`（165 项） | 工作区（本卡修复后） | **165/165 PASS** |
| 本卡独立 `verify_wym_qa_espinosa.py` | 修复前镜像（反向验证） | 145 PASS / **18 FAIL**（判据非空转，全部命中真实缺陷类） |

独立脚本在写入仓库前**先对修复前镜像复跑并复现缺陷**（3.1 / 3.2 / 9.0 / 9.1 / 10.1 / 10.2 / 10.4 共 18 项 FAIL），修复后复跑归零。

## 二、复核确认（无争议项）

1. 库内模式 `M-WYM-001~010` 恰 10 条，`mode_code`、`figure_code=H-WYM-001`、`research_mode_id=M-WAN-00n` 一一对应；遗留旧码 `M381~M389` 原样在库。
2. 每条模式 v6 字段完备（名称/定义/领域/流程/关键概念/引证/案例/现代应用/verification），中英定义非同串。
3. `data/individuals/H-WYM-001_modes.json` 的 `thinking_modes_v6_phase20` 与主库**逐字段零差异**；Phase 21 建档 `modes` 10 条原样保留。
4. 图档三镜像（`data/figures` ↔ `data/individuals` ↔ `docs/figures`）SHA256 一致（`adbc1916…`，19721 B）；`thinking_mode_count=10`、`mode_ids`、`mode_evidence` 10 条、`protreptic_mapping` 全覆盖、`phase20` 溯源块 `H-WAN-001 → H-WYM-001` 正确。
5. `docs/figures/H-WYM-001.md` 46173 B，10 模式核心字段与库内**逐字一致**，含双语场景索引，无 TODO。
6. 场景 `C-WYM-001~010`（zh）/`C-WYM-001E~010E`（en）各 10 条，`mode_code` 与十法名一一对应，英文内容零中文。
7. `scenario_tags` 20 条（zh/en 各 10），无重复，后缀与 `language` 一致。
8. `code_maps.figures.H-WYM-001`：`mode_ids` 十法、`tags` 十法、6 条交叉引用目标均可解析（`H-ZHX-001`/`H-LJY-001`/`H-KZ-001`/`H-HZX-001`/`H-DZS-001`/`H-SMQ-001`）。
9. `figure_names` 唯一登记 `H-WYM-001 → 王阳明`，无 `H-WAN-001` 残留。
10. 编码裁定正确：研究稿派生码 `H-WAN-001/M-WAN-*` 统一为库内既有码 `H-WYM-001/M-WYM-*`（`research_mode_id` + 图档 `phase20` 溯源块 + `modes_ref` 保留 1:1 映射）。
11. 遗留旧码 `M381~M389`（含 `M383` 心外无物法）的 `_en` 字段中英混排已在本次热修中收口（见三-E），遗留模式无其他 CJK 残留。

## 三、新发现缺陷（5 类 / 14 处，已修复；三镜像同步）

**A 类：英文字段粘连/缺空格（8 处）**

| 模式 | 字段 | 修复前 | 修复后 |
|---|---|---|---|
| M-WYM-003 | `definition_en` | …to all affairs**,so** that… | …to all affairs**, so** that… |
| M-WYM-003 | `definition_en` | …accord with liangzhi**.**This is… | …accord with liangzhi**.** This is… |
| M-WYM-003 | `representative_cases_en[0]` | When asked **aboutGewu** (investigating…) | When asked **about Gewu** (investigating…) |
| M-WYM-003 | `representative_cases_en[1]` | …the true secret **ofGewu**… | …the true secret **of Gewu**… |
| M-WYM-006 | `definition_en` | …good and evil**;Gewu**… / …good and evil**,Gewu**… | …good and evil**; Gewu**… / …good and evil**, Gewu**… |
| M-WYM-006 | `key_quote_en` | …discerns good and evil**;Gewu**… | …discerns good and evil**; Gewu**… |
| M-WYM-006 | `process_en[3]` | **PracticeGewu** in promoting good… | **Practice Gewu** in promoting good… |

**B 类：中文字段内嵌未译英文（2 处）**

| 模式 | 字段 | 修复前 | 修复后 |
|---|---|---|---|
| M-WYM-003 | `process_zh[3]` | Bring all actions into accord with the demands of liangzhi | 使一切行为皆符合良知的要求 |
| M-WYM-009 | `process_zh[3]` | Let each thing attain its proper place under the mind's illumination | 使每一事物在心的观照下各得其位 |

**C 类：来源章节归属错误（2 处，随 D 类共 3 处）**

| 模式 | 字段 | 修复前 | 修复后 | 核证 |
|---|---|---|---|---|
| M-WYM-003 | `source_chapter` | 《传习录》卷下 | 《传习录》卷中 | 引文出《答顾东桥书》（中卷），全本定位核到 |
| M-WYM-007 | `source_chapter` | 《传习录》卷下 | 《传习录》卷上 | "人须在事上磨…"出陆澄录〔9〕（上卷），全本定位核到 |

**D 类：不可溯源引文替换（1 处）**

M-WYM-004（念念察识法）原 `key_quote_zh/en` 与 `source_chapter` 整体替换：

- 原引文（**_已删除_**，留档备查）："念念存此良心，庶几可以涵育滋润，薰陶浃漑，而无我有私欲之害矣。" / "If one continuously preserves this innate knowing in each thought, one may nurture and nourish it, cultivate and permeate it, and avoid the harm of having selfish desires."（原注《传习录》卷中）
- 核证过程：该引文在《传习录》全本（85784 字）、《王阳明全集》（Gutenberg pg25142，961460 字）及多轮网络检索（"念念存此""存此良""涵育滋润""浃漑"等 6 组片段）中**均无法检出**；"涵育滋润""浃漑"尚非王阳明文本用语（全集仅见"涵育薰陶"于公移/书信）。判定：**不可溯源**。
- 替换为（可溯源、同主题、卷上·陆澄录〔51〕）："善念发而知之，而充之；恶念发而知之，而遏之。" / "When a good thought arises, one knows it and expands it; when an evil thought arises, one knows it and restrains it."
- `source_chapter`：卷中 → **卷上**（随替换同步订正）。

**E 类：遗留旧码英文字段中文残留（1 处；LJY QA 报告 §4 已挂号，本卡收口）**

- `M383`（心外无物法）`process_en[1]`："Understand that meaning is**赋予** by the mind" → "Understand that meaning is **given** by the mind"（与其中文 `process_zh[1]`"理解事物的意义由心赋予"对齐）。

**图档同步（4 条 × 3 镜像）**：`mode_evidence` 的 `M-WYM-003`（卷下→卷中）、`M-WYM-004`（引文整体替换 + 卷中→卷上）、`M-WYM-006`（`evil;Gewu` 补空格）、`M-WYM-007`（卷下→卷上）；`evidence_zh/en` 与 `source` 两语均同步，三镜像 SHA256 保持一致。

**研究稿引用订正（2 处）**：`data/individuals/phase20_wangyangming_research.md`："人须在事上磨…"出处 卷下→**卷上**；"吾平生讲学，只是致良知三字"非《传习录》语（全集检得于家书），出处由"《传习录》卷下"订正为"**《王阳明全集·寄正宪男》**"。

## 四、引文溯源核对（本卡重点，逐条语料定位）

| 模式 | 引文首句 | 语料定位（章节) | 判定 |
|---|---|---|---|
| M-WYM-001 | 心即理也。天下又有心外之事，心外之理乎？ | 传习录全本 · 上卷·徐爱录 | ✓ |
| M-WYM-002 | 知是行的主意，行是知的功夫… | 传习录全本 · 上卷·徐爱录 | ✓ |
| M-WYM-003 | 致吾心之良知于事事物物也… | 传习录全本 · 中卷·答顾东桥书 | ✓ |
| M-WYM-004 | 善念发而知之，而充之… | 传习录全本 · 上卷·门人陆澄录 | ✓（本卡替换后） |
| M-WYM-005 | 圣人之道，吾性自足… | 王阳明全集 · 年谱（龙场悟道） | ✓ |
| M-WYM-006 | 无善无恶心之体… | 传习录卷下/王畿《天泉证道纪》作"无善无恶**是**心之体"；两版本并存于文献与通行引用 | ✓（异文放行） |
| M-WYM-007 | 人须在事上磨，方立得住… | 传习录全本 · 上卷·门人陆澄录〔9〕 | ✓（本卡订正卷上） |
| M-WYM-008 | 圣人可学而至。 | 传习录全本 · 上卷·门人薛侃录 | ✓ |
| M-WYM-009 | 你未看此花时… | 传习录全本 · 下卷·门人黄省曾录〔28〕 | ✓ |
| M-WYM-010 | 此心光明，亦复何言。 | 王阳明全集 · 年谱（南安遗言） | ✓ |

- 语料：传习录全本缓存（www.youyoume.com，85784 字）与《王阳明全集》（Project Gutenberg pg25142，961460 字）；脚本以去标点归一 + 繁简映射检索，语料路径可用环境变量覆盖，缺失时降级 WARN。
- 观察项（非阻塞，未改动）：`representative_cases_zh[1]` 中部分对白为情境化改写（如 M-WYM-002"他不知，只是不会"、M-WYM-007"且就此事理会"），非逐字原文；该字段为案例叙述而非引文字段，建议后续批次统一校准口径。

## 五、遗留（非本卡引入，不阻塞）

- **全库 `_en` 字段 CJK 残留（系统性）**：LJY QA 报告统计全库 510 处 / 115 figure；其中 H-WYM-001 的 1 处（遗留旧码 `M383`）**本卡已收口**，其余仍建议由编排者派专项卡统一清理。
- `H-ZHX-001`（朱熹）、`H-KZ-001`（孔子）未在 `code_maps.figures` 注册（图档文件存在，本卡 xref 目标可解析）——属基线状态（barbosa 复核 metadata 同口径），非本卡范围。
- **hotspot / 提交时序记录**：`data/modes_data.json`（23.2 MB）为多卡共享大文件。本卡修复期间并行批次（章学诚 H-ZXC-001）正在途写库；本卡对 modes_data 的 15 行热修**已随其数据入库提交 `6e429676`（15:47）一并入库**（该提交同时含 M-ZXC-001~010 与 total 2938→2948 更新）；本卡提交仅含其余 6 个 WYM 文件 + 报告 + 脚本，未再触碰共享大文件，未夹带并行批次改动。下游归档/复核如需核对，两处提交均需查看。
- 库总量注记：被验收提交 `5956dd8b` 时库 2918 模式；QA 期间他卡推进至 2948（戴震 +10、章学诚 +10），与本卡无关。

## 六、工件

- `verify_wym_qa_espinosa.py`（仓库根目录，165 项独立断言；修复前镜像复跑可复现 18 FAIL）
- 本报告 `docs/research/phase20_wangyangming_qa_report.md`
- 修复面（6 文件 + 2 新增）：
  - `data/individuals/H-WYM-001_modes.json`（13 行）、`docs/figures/H-WYM-001.md`（13 行）、`data/figures/H-WYM-001.json` + `data/individuals/H-WYM-001.json` + `docs/figures/H-WYM-001.json`（各 8 行，三镜像）、`data/individuals/phase20_wangyangming_research.md`（2 行）
  - `data/modes_data.json`（15 行，已随 `6e429676` 入库）
