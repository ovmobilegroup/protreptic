# Phase21-R8 王祥（H-HZX-002） 文档归档报告（卡 t_557aeac1 收尾补交；卡 t_a8f544f5 补全）

- 执行：pigafetta｜日期：2026-09-24｜工作仓：/opt/data/workspace/Protreptic｜发布仓：/opt/data/release/Protreptic-publish
- 本件状态：原文档卡 t_557aeac1 仅落 1 行占位（提交 dc9fe529，30 B，sha256 f1f0f28e…）；本版由收尾补交卡 t_a8f544f5 逐节补全，并补入登记链提交 sha 与镜像/push 回执节。
- 版本轨迹：v1（WS1 b004ec01 / P1 4fefa6f / push 04837b3..4fefa6f；页＋报告＋证据 3 件）→ v2 本版（回执补记：§六 parity run1、§七 v1 精确回执；v2 轮的 WS2/P2/push2 精确值见卡 t_a8f544f5 metadata 与卡评论）。
- 产出：docs/figures/H-HZX-002.md（九节档案，首次提交，93 行 / 6,509 B / sha256 9c7094f9…）；本报告；归档证据 docs/research/phase21r8_wangxiang_archive_evidence.json；（既有，bc3824f4）生成器 build_hzx002_archive.py 与验收脚本 verify_hzx002_archive.py；QA 交付物 19 件镜像（发布仓 docs/qa/）。
- 边界：本卡零数据/主库改动（工作仓提交白名单仅 3 件 docs 层文件；名单外 0）；页内容按 R8-A 产物**原样**提交（未改一字节）——页内陈述行与数据面实况的差异如实登记于第六节（发现项登记，未伪修）。

## 一、任务与范围

按卡面七步逐条落实：

1. 预检（git status 确认档案页 untracked、93 行、断言脚本可复跑）→ 第二节与第四节；
2. 报告补全（本节至第九节全文，含登记链各提交 sha 与镜像/push 回执节）→ 本件；
3. 白名单提交（页＋报告＋证据，署名 magallanes，注明「卡 t_557aeac1 收尾补交」）→ 第七节；
4. 发布仓镜像（档案页＋报告＋QA 证据/报告，按先例）→ 第五、七节；
5. parity 复核（本链路路径逐字节）＋ push 发布仓 main ＋ 回执 sha → 第六、七节；
6. 回执补记进报告并二次提交/镜像 → 第七节（v2 轮）；
7. 站点/展示层按先例复核 → 第六节。

## 二、归档前状态（归档时点实测）

- 档案页 docs/figures/H-HZX-002.md：untracked（`git log -- docs/figures/H-HZX-002.md` 为空 = 从未提交）；93 行 / 6,509 B / sha256 9c7094f9c68dcf14ca94a233b5e70a373c7e496587756b4cb2fdadd2f1bb3bed。
- 生成器/验收脚本（已提交）：bc3824f433ec1db6ae7fff074c15ece8e0a17df6（build_hzx002_archive.py sha256 d3f1742c… / verify_hzx002_archive.py sha256 31c9d23d…）；报告占位：dc9fe52942e8ece57c38519763b3061176288237（30 B）。
- QA 交付物（已提交）：ae72a7d25c0df0b29abbf5c6350237649e297855（20 件 = 报告＋独立脚本＋证据 json/txt＋自检＋门禁/链条日志 15 件；零夹带）＋收尾回执 e9fdddec161a64d1cb4f0126e74ecd989ef3d826；口径 177 PASS / 0 FAIL / 0 SKIP；反向注入自检 10/10。
- 发布仓缺件：档案页、归档报告、QA 19 件（parity run0 基线中本链 21 条 MISSING_IN_PUBLISH）。
- 核验状态：本件 10/10 条 verification.status=pending（0 条自称 verified；独立核验流程见 QA 卡）。

### 登记链（全链 git 实测）

| 段 | 卡 | 工作仓提交 | 备注 |
|---|---|---|---|
| R6B 归档 | t_f3aabe2c | d33e1122f45e530b96a9bf86fd4c7f9482aca45d | 3 件入 _duplicates；figure_names 清档 |
| R7 落源研究 | t_b5454647 | 5c18391858fc0cd546c3c045ccd65b4870ec4482 | 发布仓镜像 646a9c7 |
| R8 A1 重建落盘 | t_5c183962 | 1fe4c451aa48acb673960a7d3ac25844dd21b717 | M-WX-001~010＋figure 修正稿；独立核验 58 PASS/0 FAIL |
| R8 A2 合并入库 | t_8c521af7 | d95a7b53c9a9802818a13c5dd4b65774329003b7 | 回执 v2 68d6e0b0ce934752c884aaee3631bbce43914315；发布仓镜像 9c4ff9e / dab8213 |
| R8 A3 QA 验收 | t_b92cc1cf | ae72a7d25c0df0b29abbf5c6350237649e297855 | 回执 e9fdddec161a64d1cb4f0126e74ecd989ef3d826 |
| R8 文档归档 | t_557aeac1 | bc3824f433ec1db6ae7fff074c15ece8e0a17df6（工具）＋dc9fe52942e8ece57c38519763b3061176288237（占位报告） | 页/报告补交归本卡 |
| 收尾补交 | t_a8f544f5（本卡） | WS1/WS2 见第七节 | 镜像 P1/P2 ＋ push 见第七节 |

## 三、归档动作（九节档案结构说明）

1. 生成器 build_hzx002_archive.py（幂等）：自 v6 载荷装配——data/figures/H-HZX-002.json（图档）＋ data/individuals/H-HZX-002_modes.json（伴随包）；内置护栏断言三组：模式数 10/10、图档内嵌模式 == 伴随包（逐对象全等）、编号 M-WX-001~010 顺序；任一失败 exit 1 不落盘；页字节不变判 IDEMPOTENT（不写）。
2. 页面九节结构（各节来源）：
   - 一 历史定位（fig.historical_significance，逐字）；
   - 二 核心思想（fig.core_thoughts，10 条）；
   - 三 十大思维模式（M-WX-001~010，题名/定义；图档内嵌与伴随包双面同体）；
   - 四 现代场景应用（现为「缺项登记」行——见第六节 D1）；
   - 五 现代应用（现为「缺项登记」行——见 D2）；
   - 六 跨引用（现为「缺项登记」行——见 D3）；
   - 七 标签（fig.tags，15 项）；
   - 八 独特成就（fig.influence）；
   - 九 QA 验收记录（4 行：登记链、核验口径、缺项登记、归档动作——见 D4/D5/D6）。
3. 先例对照：体例对齐 R6 A 组（build_legacy20_r6_archive.py，ee992a42）、曾子（t_6c7e070a）、罗瑞卿（t_d9cb98bb）。差异点（如实登记）：§四/五/六 为缺项登记行而非实体内容；§九 无头部登记链块、无计数台账、无逐条 evidence、未含提交号——对照 luorq/R6 体例属欠完备（详见第六节 D6）。
4. 幂等与复跑：见第四节。

## 四、验证证据（复跑实测）

- 复跑① 生成器幂等：`python3 build_hzx002_archive.py` → 「基本断言通过」＋「== IDEMPOTENT ==（字节不变）」，exit 0；前/后 sha256 均为 9c7094f9…（页字节未动）。
- 复跑② 文档层验收：`python3 verify_hzx002_archive.py` → 「验证通过」，exit 0（断言项：标题、九节标题齐备、M-WX- 模式 10/10、登记链行在）。
- 断言口径注（如实登记）：验收脚本为**结构级**断言，不覆盖 §四/五/六/§九 陈述行与数据面的一致性——该盲区已在第六节 D 项登记（根因同注）。
- QA 侧引述（不重跑；QA 卡已带收尾回执 e9fdddec）：177 PASS / 0 FAIL / 0 SKIP；反向注入 10/10；门禁 credibility / verify_findings / verify_source_links --hard-fail exit 0；apply_verification_status --check 漂移 19 条如实登记（本链 9 条 pending 不回填属纪律(4)）。
- QA 镜像 19 件 sha256 台账：见证据 json `qa_mirror.sha256`（逐件）；两仓 byte-exact 见第七节。

## 五、QA 产物镜像说明

- 镜像集合（19 件，byte-exact）：
  - docs/qa/phase21r8_wangxiang_qa_report.md（038de9f5…）
  - docs/qa/phase21r8_wangxiang_qa_evidence.json（ed69be46…）/ qa_evidence.txt（e84bc31d…）
  - docs/qa/phase21r8_wangxiang_qa_selftest.json（6b80f6e1…）
  - docs/qa/phase21r8_wangxiang_qa_gates/ 15 件（chain1~5 现场链条、frozen_chain* 冻结链条、gate_apply_verification_status / gate_credibility_gate / gate_verify_findings / gate_verify_source_links、parity_check_repo；逐件 sha256 见证据 json）。
- 先例：曾子 QA 证据已在发布仓 docs/qa/（phase20R_zengzi_qa_evidence.txt＋qa_report.md）；R6 QA 交付物 8 件镜像（74a52b1）；本卡按同一口径收口本链 QA 交付物（QA 卡自身边界为「镜像与 push 归合并/收尾卡」）。
- 脚本镜像面判定（按先例并在本报告说明）：仓根脚本（build_hzx002_archive.py / verify_hzx002_archive.py / verify_hzx002_qa_espinosa.py）不进站点构建图（parity 边界以 docs/** 与构建图 tools 清单为准；仓根非 docs 面），按罗瑞卿报告 §六先例**不镜像**——本卡维持。

## 六、两仓一致性（站点/展示层、parity 与内容一致性核验）

### 站点/展示层（按先例复核）
- mkdocs.pages.yml：docs_dir: docs；exclude_docs: archive/；无 nav（mkdocs 按文件树自动导航）→ docs/figures/*.md 属站点构建图。
- 发布仓 .github/workflows/pages.yml 含 `mkdocs build -f mkdocs.pages.yml`（第 236 行）→ 镜像 push 后触发 Pages 构建；回滚方式 revert 镜像提交（禁 --force）。结论与罗瑞卿先例一致。

### parity 实测（tools/check_repo_parity.py --json；快照以 git 实测为准）
- run0（镜像前基线）：DIFF 315 = 6 内容差（W5 链工具/数据在制）＋309 仅工作仓；本链 21 条在列（页 untracked 1 ＋ 报告 1 ＋ QA 19）。
- run1（镜像与 push1 后快照）：DIFF 305 = 6 内容差（W5 工具/数据在制）＋299 仅工作仓；本链 22 路径 0 差（run0 基线 21 条全数消除；证据 json 新增件两仓同体）；残差归因见下。
- run2（终测，P2 后）：见卡 t_a8f544f5 完成回执 metadata（parity_run_final）与卡评论。
- 残差归因（run1，非本链）：luorq QA/复核 19 件（untracked，其中 11 件为 run0 后新增）；W4 4 件；W5 链 282 件（6 内容差＋docs/scratch 271＋docs/research 3＋data/audit 2）。

### 内容一致性核验（本卡新做；发现项如实登记，未伪修）

对照数据面实况逐项复核（2026-09-24 实测），页内五处陈述与实况不符：

- D1（页 L70，§四）「本件在 data/scenarios_zh.json 中无 C-WX 规范场景条目」→ 实况：C-WX-001~010 在库（10 条，mode_code 覆盖 M-WX-001~010；scenarios_en 侧 C-WX-001E~010E 10 条）。
- D2（页 L74，§五）「模式级 modern_applications_zh 空」→ 实况：10 条模式（图档内嵌与伴随包两面）modern_applications_zh 各 4 条非空。
- D3（页 L78，§六）「code_maps.figures.H-HZX-002.cross_references 为空」→ 实况：非空，1 条（target_figure_code=H-ZX-001，relation_type=comparison；d95a7b53 已入库）。
- D4（页 L92，§九）「缺项登记：图档无 historical_significance｜无 core_thoughts｜无 influence｜tags 为 null」→ 实况：四字段全在（210 字 / 10 条 / 126 字 / 15 项）；且本页 §一/§二/§七/§八 自身即逐字自这些字段装配——页内自相矛盾。
- D5（页 L93，§九）「归档动作：旧世代档案页字节归档至 data/figures/_duplicates/H-HZX-002_legacy_docs_page.md」→ 实况：该文件不存在（全仓 find 0 命中）；R6B 归档为 3 件（H-HZX-002_figures.json 8c40067c… / H-HZX-002_figures_modes.json 1e3e97d4… / H-HZX-002_research_phase20.md 8b63cda2…）；archive_recommendation.json 明记 site_docs_page=「无」→ 本页属首次装配（同 R6 JX/YSK 先例不建归档件）。
- D6（体例/规格缺口，§九）：未含 commit 链登记（文档卡 t_557aeac1 卡面明文要求「含 5c183918、A1/A2/A3 各卡提交」）；无头部登记链块、计数台账、逐条 evidence、口径备注（对照罗瑞卿/R6 体例）。
- 根因（分析，非修复）：生成器 §四/五/六 与 §九 缺项行系硬编码模板文本（不读数据面、无条件输出）；验收脚本仅结构断言——两类断言均未覆盖「陈述行与数据面一致性」，缺陷未被拦截。修复属内容修改（需改生成器与验收脚本，超出本卡「原样补交＋零数据改动」边界）——建议由船长裁定路由修正卡：缺项行改数据驱动（条件输出）、验收脚本增陈述性断言、§九 补 commit 链登记。

## 七、提交与推送回执（v2 补记）

- v1（页＋报告＋证据 3 件）：工作仓 WS1＝b004ec017c5958a855e5a6f3aa39d9c18b46b195（名单 3 件精确、名单外 0）；发布仓 P1＝4fefa6f9ec977da81806a69fe6ba1a5f5c615860（22 件：页＋报告＋证据＋QA 19，逐件 cmp byte-exact 22/22）；push＝04837b3..4fefa6f main -> main（rc=0；ls-remote origin/main＝4fefa6f 复核一致）。
- v2（回执补记；报告＋证据 2 件）：工作仓 WS2、发布仓 P2、push2 的精确 sha 与区间见卡 t_a8f544f5 完成回执 metadata（ws_commit_v2 / publish_commit_v2 / push_v2）与两仓 git log（v2 轮提交信息含「v2 回执补记」）。
- 工作仓 master push：不适用（环境事实：远端仅 main；dry-run 为全量历史上传，master 历史含 440.19 MB blob 1ff8dcb9:api/triton/_C/libtriton.so，服务端 100 MB pre-receive 拒绝；phase45_acceptance.md / link_coverage.md §10.1 在案——同 t_2d15bd2e 先例）。
- 精确 sha 与 push 区间另见卡 t_a8f544f5 完成回执 metadata（ws_commit_v1/v2、publish_commit_v1/v2、push_v1/v2、remote_main）与两仓 git log（提交信息含「卡 t_557aeac1 收尾补交」）。

## 八、文件与验收命令（真实路径）

- 页面：docs/figures/H-HZX-002.md（93 行 / 6,509 B / sha256 9c7094f9…）
- 生成器：build_hzx002_archive.py → `python3 build_hzx002_archive.py`（幂等；输出「基本断言通过」「IDEMPOTENT」）
- 验收：verify_hzx002_archive.py → `python3 verify_hzx002_archive.py`（输出「验证通过」）
- 本报告：docs/research/phase21r8_wangxiang_archive_report.md
- 证据：docs/research/phase21r8_wangxiang_archive_evidence.json
- QA 交付物：docs/qa/phase21r8_wangxiang_qa_report.md / qa_evidence.json / qa_evidence.txt / qa_selftest.json / qa_gates/（15 件）
- 上游链路（只读）：docs/research/phase21r7_wangxiang_sourcing_report.md/.json；docs/research/phase21r6B_evidence.json；docs/scratch/legacy20_r6b/H-HZX-002/（corrections / corrected_record / redo_checklist / archive_recommendation）；docs/research/phase21r8_wangxiang_rebuild_report.md、landing_evidence.json、gate.txt；docs/research/phase21r8_wangxiang_merge_report.md、merge_evidence.json/.txt；verify_hzx002_qa_espinosa.py（QA 卡第二实现）
- 先例：build_legacy20_r6_archive.py / verify_legacy20_r6_archive.py（R6，ee992a42）；build_luorq_r8_archive.py / verify_luorq_r8_archive.py（t_d9cb98bb）

## 九、开放项与建议

1. 【页内容缺陷 D1–D6（第六节）】建议船长裁定路由：修正卡改生成器缺项行数据驱动＋验收脚本增陈述性断言＋§九补 commit 链登记；本卡原样补交、未伪修。
2. QA 侧遗留（属 QA 卡边界，未伪修）：冻结 worktree 留痕（~/.cache/wxqa_frozen_wt@d95a7b53，可 git worktree remove）；verifstatus 19 条漂移含他卡码（本链 9 条维持 pending 不回填属纪律(4)）。
3. 发布仓 parity 残差（run1：305 条）全属他链在制（luorq QA/复核 19、W4 4、W5 282）；本链 0 残差；建议各链收尾卡按同模板收口。
4. 远端 Pages：镜像 push 将触发构建；异常回滚 revert（禁 --force）。
