# Phase21-R9 沈复（H-SHF-001） 文档归档报告（卡 t_7e5afcbb）

- 执行：pigafetta｜日期：2026-09-24｜工作仓：/opt/data/workspace/Protreptic｜发布仓：/opt/data/release/Protreptic-publish
- 产出：docs/figures/H-SHF-001.md（九节档案，首次装配）。生成器 build_shf_r9_archive.py（幂等，内置逐字断言）。文档层独立验收 verify_shf_r9_archive.py（第二实现 + 反向注入自检 15/15）。本报告与证据 docs/research/phase21r9_shenfu_archive_evidence.json
- 边界：本卡只写文档层与归档产物，零数据改动（modes_data.json / scenarios / tags / 注册 等仅读不写）。上游链（研究/落盘/合并/QA）提交与镜像快照见第二、六、七节。

## 一、任务与范围

按卡面落实：
1. 九节档案＋登记链（同 R9 标准：链级档案、登记、双仓归档校验、发布面复核）（见第三、六节）；
2. 链级档案与登记：全链五段（研究..重建..合并..QA..归档）卡号/执行者/提交号/报告路径入页头部与第九节，见第三节第 1、2 条；
3. 据实登记、零数据改动：QA 记录照实（74/0、53/0、75/0/5 与闭合热修 54df4c4）入页第九节，见第三节第 3 条；
4. 提交＋镜像＋完成回执，见第七节与 kanban 回执；
5. 完成合同（档案落盘可溯源；登记链完整）：页/报告/证据提交与镜像，精确 SHA 见第七节。

## 二、归档前状态（归档时点实测）

- R7 核名（卡 t_261185a8）：旧件判「虚名空壳、无存世文献依据」，裁定维持归档（不唤醒、不改名、不迁载荷）。旧模式码段 M351..M358 零复用（登记 docs/scratch/legacy20_r9_shenfu_landing/id_mapping.tsv）。此前无在册旧页，本页为首次装配。
- R9 研究（卡 t_d78053e7，提交 e0a98aa8）：素材包（10 条模式逐条落源，引文 35/35 终跑）＋身份证据链＋查重 0 占用；见证副本 35 件随件入库；零库写。
- R9 重建落盘（卡 t_b6d4c0ee，提交 59bc5471、a515badd）：figure/individuals 三件＋冻结副本九件＋生成器与核验脚本；独立核验 74 PASS / 0 FAIL；引文 35/35 见证复核；主库零写入。
- R9 合并入主库（卡 t_a7d233f0，提交 5a657b81、906a0bee、c3cceb19）：主库 +10（modes 3301..3311、total 随动）、注册 code_maps 215..216 / figure_names 1084..1085、场景 +10+10、标签 +20（7518..7538）、顶层块 23 键；站链五步；门禁四项 exit 0；独立核验 53 PASS / 0 FAIL。
- R9 QA 独立验收（卡 t_83e0d68d，提交 95c044aa、c2d5820a）：终轮 75 PASS / 0 FAIL / 5 INFO（80 行断言；判据全部重回原始取证）。含 1 项闭合热修（发布仓补链自身产物 2 件，提交 54df4c4）。QA 卡产物镜像 946afe0，push 收口 e6d133c..2397eee。
- 核验状态：本件 10/10 条 verification.status=pending（0 条自称 verified）。
- 归档时点 git（实测）：工作仓 HEAD bf52ee4c（本卡 WS1；期间他卡亦落提交）。发布仓 HEAD 19e8f58（本卡 P1；镜像前为 d0c7306）。本卡提交/镜像/推送全量回执见第七节。

## 三、归档动作

1. 生成器 build_shf_r9_archive.py：自 11 个真值源逐字装配（data/figures/H-SHF-001.json / data/individuals/H-SHF-001.json / _modes.json / 主库 modes_data.json / scenarios_zh|en / code_maps / figure_names / scenario_tags / landing combined / modes_library_entries / top_block_proposal）；护栏九组：四面同体（图档内嵌 = 伴随包 = 主库 = landing combined = modes_library_entries，逐对象全等）｜编号（M-SHF-001..010 顺序、id == mode_code、legacy_mode_id 全空）｜诚实（10/10 pending、0 自称 verified）｜禁字 18 项零残留｜场景面（C-SHF-001..010 与 E、tags 20）｜注册面（figure_names / code_maps 与图档逐字）｜顶层块（== proposal 且位于 modes 键前）｜旧件 sha（三件字节冻结）｜幂等；任一断言失败即 exit 2 不落盘。
2. 页面 docs/figures/H-SHF-001.md：55,646 B / 439 行 / sha256 f9a0af91b4400af6b9119b22830ad4f792f0a472841c23b901f8ca33d5ec1429；九节结构（一 历史定位｜二 核心思想｜三 十大思维模式｜四 现代场景应用｜五 现代应用｜六 跨引用｜七 标签｜八 独特成就｜九 QA 验收记录）；头部含登记链（五段全链）、报告索引、caveats 8 条逐条搬迁、卒年失考注记（约 1808 年以后在世，下限不明）；第九节含 QA 记录、红线口径七条、缺项登记五项、计数台账。
3. QA 记录照实入页（第九节）：75 PASS / 0 FAIL / 5 INFO、74 PASS / 0 FAIL、53 PASS / 0 FAIL、闭合热修 54df4c4（链集合 83/83）；残留与观察项（parity 53 条归因、X01/X02 白名单漂移 73/1 与 51/2、index.md 存量行）。红线与口径七条（卷五六伪续 / 卒年失考 / 「名复」并注 / 转引层 / 用字异文 / 描述性标签 / 图像素材）。
4. 先例对照：体例对齐 R8 罗瑞卿（build_luorq_r8_archive.py + verify_luorq_r8_archive.py，卡 t_d9cb98bb）与 R8 王祥（build_hzx002_archive.py，卡 t_557aeac1）。差异点：本件为「换人重做」新件（旧件维持归档，无页面级旧页清理动作）；禁字 18 项（含旧模式码段 M351..M358）；新增反向注入自检 15 类。
5. 幂等实测：二次运行 IDEMPOTENT（字节不变）。--dry-run 只断言预览（首跑 0 B..55,646 B）。

## 四、验证证据

- 文档层独立验收：python3 verify_shf_r9_archive.py，结果 141 CHECKS / 141 PASS / 0 FAIL（第二实现，不导入生成器；区块级 block-scoped 核对）。
- 反向注入自检：python3 verify_shf_r9_archive.py --inject-test，结果 15/15 捕获（清单：台账 total 篡改、台账 modes 篡改、引文截断、禁字注入、假 verified、节删除、场景截断、出处篡改、模式标题篡改、标签删除、跨引用删除、缺项删行、登记链 sha 篡改、卒年注记篡改、evidence 条数篡改）。
- 禁字：18 项零残留（页面面）＋旧模式码段 M351..M358 零出现。
- 四面同体：图档内嵌 = 伴随包 = 主库 10 条 = landing combined = modes_library_entries 逐对象全等；图档 == 个体档（除 modes 外逐字）。图档与 code_maps 跨引用逐字全等 3/3。
- 计数台账（归档时点 canonical）：modes=3311; total=3311; code_maps=216; scenarios_zh=2213; scenarios_en=2213; scenario_tags=7538; figure_names=1085（页面 md 与本报告互证）。
- git 登记链实测：cat-file 校验 e0a98aa8 / 59bc5471 / a515badd / 5a657b81 / 906a0bee / c3cceb19 / 95c044aa / c2d5820a 均存在（归档时点）。
- 证据 JSON：docs/research/phase21r9_shenfu_archive_evidence.json（141/141、页 sha256、台账；字段见文件）。

## 五、残留与观察项（如实登记，未伪修）

- parity（QA 卡终轮）：53 条差异逐条归因，沈复链面 0 命中（16 条 QA 产物提交/镜像后消除；37 条他卡在制）。本卡归档时点复跑快照见第六节。
- X01/X02 链自有脚本白名单漂移（73/1、51/2）：他卡产物与 QA 脚本落入其白名单外，非数据缺陷；本卡不扩展白名单（QA 注：非必须），按观察项登记。
- docs/index.md 存量行「283 位人物..2848 条」：前像同文、非本链引入（QA 报告 §4.3 已登记）。
- H-BG-001 至 H-HAN-001 悬空互引：已由 R8 卡 t_8183b8fd 清除，0 残留。
- 并发写者：归档期间 t_02007da8、t_def07a84、t_70a8cbce 等在制；本卡只读数据面、只写文档层与归档产物。

## 六、两仓一致性（双仓归档校验与发布面复核）

- 展示层性质：docs/figures/*.md 属 mkdocs 文档层（docs 目录进站点构建）；发布仓驱动站点（.github/workflows/pages.yml、mkdocs.pages.yml）；按 R6/R8 先例镜像至发布仓。
- 发布面复核（QA 承接项）：
  - 复核 1：QA 闭合热修 2 件（docs/research/phase21r9_shenfu_sourcing_report.json / .md）已在发布仓（54df4c4，byte-exact）。QA E02 链集合 83/83。
  - 复核 2：QA 产物镜像 19 件（946afe0）在发布仓 HEAD 血缘内（QA 回执实测）。发布仓工作树链面全净。
- 本卡 parity 实测（tools/check_repo_parity.py --json，两跑快照）：
  - 快照 1（页落盘后、镜像前）：diffs=46（41 MISSING_IN_PUBLISH + 5 CONTENT_DIFF）；其中本卡 2 件（页、证据）；他卡在制 44 件（W8 Stage2 批1 28 件；W4 6 件；W6 2 件；W10 1 件；candidates_v5 1 件；AZJ 页 1 件；内容差 5 件：web_p0_routes / tools x3 / sitemap）。
  - 快照 2（镜像后）：diffs=44（39 MISSING_IN_PUBLISH + 5 CONTENT_DIFF）；本卡归零（SHF 链面 0 命中）；仅余他卡在制（同上 44 件明细）。
  - 双边计数：both_sides 2530..2532、identical 2525..2527（+2 = 本卡页/证据镜像入库）。
- 本卡镜像范围：页、证据（P1）、报告（P2）三件（docs 下，进构建图）｜生成器与验收脚本为仓根工具（不进构建图，按 parity 边界规则与 R6/R8 先例不镜像）。
- 发布面注意：push 触发 Pages 构建；回滚方式为 revert 镜像提交（禁 --force）。

## 七、提交与推送回执（补记）

- 工作仓提交：WS1 bf52ee4c1de49757746fa921850b7714308378df（白名单四件：页 / 生成器 / 验收脚本 / 证据；定向暂存、零夹带、零数据改动）；回执补记提交 WS2（本报告）。
- 发布仓镜像：P1 19e8f58b15a8cb2a2714a2523a6b6c6393a5bcf0（页/证据 2 件 byte-exact，sha256 双侧一致）；回执补记镜像 P2（本报告）。
- 推送：d0c7306..19e8f58（origin main，rc=0；推送前 fetch 复核，禁 --force）。推送后 git ls-remote 实测 = 19e8f58b15a8cb2a2714a2523a6b6c6393a5bcf0，与本地发布仓 HEAD 一致。
- 自指说明：WS2 / P2 / 第二次 push 的精确 SHA 以本报告提交时点自指，见 kanban 卡 t_7e5afcbb 完成回执 metadata（ws_commit_v2 / publish_commit_v2 / push_v2）与两仓 git log（提交信息含「归档报告」字样）。发布仓工作树全净复核（快照）。

## 八、文件与验收命令（真实路径）

- 页面：docs/figures/H-SHF-001.md
- 生成器：build_shf_r9_archive.py（python3 build_shf_r9_archive.py [--dry-run]）
- 验收：verify_shf_r9_archive.py（python3 verify_shf_r9_archive.py [--inject-test] [--no-evidence]）
- 报告：docs/research/phase21r9_shenfu_archive_report.md
- 证据：docs/research/phase21r9_shenfu_archive_evidence.json
- 上游链路（本卡只读）：phase21r9_shenfu_sourcing_report.md / .json、phase21r9_shenfu_rebuild_report.md、phase21r9_shenfu_merge_report.md、phase21r9_shenfu_qa_report.md、phase21r9_shenfu_qa_evidence.json、phase21r9_shenfu_qa_logs/
- 归档先例：build_luorq_r8_archive.py / verify_luorq_r8_archive.py（R8 罗瑞卿，卡 t_d9cb98bb）、build_hzx002_archive.py / verify_hzx002_archive.py（R8 王祥，卡 t_557aeac1）

## 九、开放项与建议

- 核验卡启动时建议连同素材包见证 35 件一并复核引用合规（与链 QA 承接一致）。
- 白名单漂移（X01/X02）如需消除可选择性扩展，非必需；本卡未动链自有脚本。
- 若后续数据面更新（主库/场景），本页可由生成器幂等重跑刷新（计数台账随之更新，报告与证据需同步）。
- 发布仓 push 将触发 Pages 构建；若 CI 异常，按 revert 镜像提交回滚（禁 --force）。
