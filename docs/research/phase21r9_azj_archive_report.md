# Phase21-R9 安子介（H-AZJ-001） 文档归档报告（卡 t_08b3a1c0）

- 执行：pigafetta｜日期：2026-09-24｜工作仓：/opt/data/workspace/Protreptic｜发布仓：/opt/data/release/Protreptic-publish
- 产出：docs/figures/H-AZJ-001.md（九节档案，首次装配）；生成器 build_azj_r9_archive.py（幂等，内置逐字断言）；文档层独立验收 verify_azj_r9_archive.py（第二实现＋反向注入自检）；本报告与证据 docs/research/phase21r9_azj_archive_evidence.json
- 边界：本卡只写文档层与归档产物，零数据改动（modes_data.json / scenarios / tags / 注册面等仅读不写）；上游链数据面提交、镜像与 push 已归各链卡（见第三节登记链）。

## 一、任务与范围

按卡面要求逐条落实：

1. 链级执行档案（研究→重建→合并→QA→收口全记录）→ 见第三节与页面头部/第九节；
2. 模式/引文登记 → 见第三节第 3 条（10 模式 × 引文 × 出处 × 见证逐条登记）与页面第三节/第九节；
3. 双仓归档与校验 → 见第六节（本卡镜像 3 件，parity 本卡路径 0 差）；
4. 发布面复核（站点条目可访问）→ 见第七节；
5. 完成报告给真实路径（提交 SHA，文件路径，验收命令）→ 见第八、九节。

## 二、归档前状态（归档时点实测）

- 链五段齐备：R9 研究（t_1aa06d0c）→ 重建（t_58ebf9c2）→ 合并（t_ce457734）→ QA（t_02007da8）→ 本卡归档；11 个链提交号 git cat-file 实测均为 commit（见证据 chain_commits）。
- 旧件状态：H-AZJ-345 判死清档（R8：t_3de0af0e 处置核定 / t_3669eb4a 执行 / t_ff294775 独立验收 / t_6acd458b 发布面补正）；8 片段＋ledger 字节冻结于 data/figures/_duplicates/（sha 逐件复算一致）；docs/figures/ 下无在册旧页 → 本页为 R9 重做后首次装配。
- 现场计数（归档时点 canonical）：modes=3311（含兄弟链沈复 +10 并入）；total=3311；code_maps=216；scenarios_zh=2213；scenarios_en=2213；scenario_tags=7538；figure_names=1085。
- 本件条目实测：M-AZJ-001~010 位于主库 modes 索引 [3291:3301]（尾部 10 条为 M-SHF-001~010）；顶层块 H-AZJ-001 位于 modes 键前（23 键，== top_block_proposal 逐字）；注册面 code_maps/figure_names 逐字一致；场景面零注册（三件 0 条）。

## 三、归档动作

1. 生成器 build_azj_r9_archive.py：自 9+ 真值源逐字装配；内置护栏八组（四面同体｜编号｜诚实 pending｜场景零注册登记｜禁字 19 项零残留（载荷面＋生成页）｜注册面｜顶层块｜旧件字节冻结）；任一断言失败即 exit 2 不落盘；--dry-run 支持。
2. 页面 docs/figures/H-AZJ-001.md：55,305 B / 353 行 / sha256 944a860c759978495da9ed671da8b481b8143182eda505270748271f051f1c5c；九节结构（一 历史定位｜二 核心思想｜三 十大思维模式｜四 现代场景应用（本链零注册——登记）｜五 现代应用｜六 跨引用｜七 标签｜八 独特成就｜九 QA 验收记录）；头部含 R9 登记链（五段卡号/执行者/提交号/报告路径）与授权/旧件处置链；caveats 逐条；缺项登记声明。
3. 模式/引文登记（10 条，页面第三节与第九节逐条）：每条含 引文（key_quote zh/en）／出处（source_chapter 含引据与见证编号）／关键概念／步骤／案例／现代应用／类目（category＋category_raw 原值留证）／核验状态（pending）／evidence（素材包逐字口径＋tier 标注）。见证：W01–W11 存证 11 件（sha256 见素材包第六小节）；引文 10/10 与素材包 quotes 逐字（落盘卡与 QA 卡双重独立复算）。
4. 先例对照：体例对齐 R8 罗瑞卿归档（build_luorq_r8_archive.py / verify_luorq_r8_archive.py，卡 t_d9cb98bb）与 R9 沈复归档（卡 t_7e5afcbb）；差异点：① 场景面为「零注册登记」章节（本链场景面零写入，如实登记，不伪写）；② 新增「授权/旧件处置链」登记行；③ 引文含繁体原貌（W07）与讲话转述口径（W01），逐字保留未改写。
5. 幂等实测：二次运行 IDEMPOTENT（字节不变）；--dry-run 通过（0 B -> 55,305 B）。

## 四、验证证据

- 文档层独立验收：python3 verify_azj_r9_archive.py → 371 CHECKS / 371 PASS / 0 FAIL（第二实现，不导入生成器）。
- 反向注入自检：python3 verify_azj_r9_archive.py --inject-test → 18/18 捕获（计数篡改、figure_names 台账篡改、total 篡改、标题码篡改、模式块删除、引文截断、定义篡改、禁字注入、假 verified、节删除、evidence 篡改、caveat 删除、出处篡改、链提交篡改、跨引用对照篡改、归档动作删除、场景登记位篡改、执行者篡改）。
- 禁字：19 项零残留（生成页内；载荷面由生成器断言）。
- 四面同体：图档内嵌 = 伴随包 = figures 伴包 = 主库 10 条 = landing combined = modes_library_entries，逐对象全等；图档 == 个体档（除 modes）。
- 台账（归档时点 canonical）：见第二节现场计数（md / 报告 / 证据三处互证）。
- git 链核对：11 个链提交 cat-file 实测为 commit；旧件 8 片段 sha256 与 ledger 逐件一致、_duplicates 恰 9 件。

## 五、QA 分级发现承接（如实登记）

- F1 口径差（不阻断）：M-AZJ-009 category_raw 与素材包 JSON theme 字段不一致；落库取 md 口径（与 category_mapping.tsv 一致）；本页第三节按「原值留证」口径逐字登记，未改库；建议后续 sourcing 勘误统一。
- F2/F3/F4/F5 登记项 → 本页第九节逐条登记（构建产物面 / DB 非链面 / 尾换行口径 / 远端时移）。
- 无未闭合缺陷：QA 复核批 61 PASS / 0 FAIL / 5 INFO（rc=0）。

## 六、两仓一致性（parity 实测）

- 展示层性质：docs/figures/*.md 属 mkdocs 文档层（docs 目录进站点构建，mkdocs.pages.yml；发布仓驱动 Pages），故按先例镜像至发布仓。
- parity（tools/check_repo_parity.py --json）三跑：
  - 跑1 归档前基线：diffs=43（only_workspace=38 ＋ content_diff=5）；AZJ 归属 0（差异全部为他链在制：W4/W6/W8/W10、source-link 工具、兄弟卡 SHF 归档在制）。
  - 跑2 页落盘后（镜像前）：diffs=44（only_workspace=39）；本卡新增 1 条 = MISSING_IN_PUBLISH docs/figures/H-AZJ-001.md。
  - 跑3 提交后（镜像前）：diffs=44 / only_workspace=41 / AZJ=3 条；跑4 镜像后（P1）：diffs=46 / only_workspace=38 / content_diff=8 / AZJ=0（本卡三路径 0 差；复测见第十一节）。
- 本卡镜像范围：页 ＋ 报告 ＋ 证据 三件（docs 下，进构建图）；生成器与验收脚本为仓根工具（不进构建图，按 parity 边界规则与 R6/R8 先例不镜像）。

## 七、发布面复核（站点条目可访问）

- 工作仓站点数据面：web/public/data/modes/by-figure/H-AZJ-001.json（66,893 B；count=10，摘要面 == 主库）在盘（构建产物面，部署链重建）。
- 远端复核（v2 补记实测）：raw.githubusercontent.com 三路径 http=200 且字节 SAME（见证据 publish_checks）。
- 发布仓谱系：本卡镜像提交属 origin/main 谱系（merge-base 实证）；Pages 工作流（pages.yml paths 含 docs/**）随 push 触发重建，站点条目（页面 ＋ data 分片）由 CI 生成。
- 站点条目口径：docs 层页面经 mkdocs 构建于 /protreptic/docs/**；数据分片由 export_static_site.py 于 CI 生成（本次 push 后重建）。

## 八、提交与推送回执（v2 补记精确 SHA）

- 工作仓提交：WS1 = 85bf7547（白名单 5 件：页/生成器/验收脚本/报告 v1/证据 v1；+1217）；v2 本件（报告＋证据 2 件）SHA 见卡 t_08b3a1c0 回执。
- 发布仓镜像：P1 = 74ea060（对齐 WS1，3 件 byte-exact；+460）；v2 镜像 P2 见卡回执。
- 推送与远端一致：git push origin main = 06c0637..74ea060（rc=0）；git ls-remote origin main = 74ea0602067873944279f328be9d3d1ae1f4519d（推送时点复核一致）。

## 九、文件与验收命令（真实路径）

- 页面：docs/figures/H-AZJ-001.md
- 生成器：build_azj_r9_archive.py（python3 build_azj_r9_archive.py [--dry-run]）
- 验收：verify_azj_r9_archive.py（python3 verify_azj_r9_archive.py [--inject-test]）
- 报告：docs/research/phase21r9_azj_archive_report.md
- 证据：docs/research/phase21r9_azj_archive_evidence.json
- 上游链路（只读）：docs/research/phase21r9_anzijie_sourcing_report.md / phase21r9_azj_rebuild_report.md / phase21r9_azj_merge_report.md / phase21r9_azj_qa_report.md（证据 qa_evidence.json/.txt）；data/figures/_duplicates/H-AZJ-345_ledger.json
- 归档先例：build_luorq_r8_archive.py / verify_luorq_r8_archive.py（R8，卡 t_d9cb98bb）。

## 十、开放项与建议

- F1：建议后续 sourcing 勘误统一素材包 JSON theme 字段（或注明以 md 口径为准）——不改库。
- 场景面：本链零注册为设计口径；如需场景应用建议另立卡（不阻断本档）。
- 数据面更新（主库/注册面）后，本页可由生成器幂等重跑刷新（台账随动；报告与证据需同步）。
- 回滚口径：镜像提交 revert（禁 --force）；本页为站点点位新增（发布仓 push 触发 Pages 构建）。

## 十一、回执补记（v2）：提交 / 镜像 / 推送 / 发布面实测

- 工作仓提交 WS1 = 85bf7547（5 件：页/生成器/验收脚本/报告 v1/证据 v1；+1217 行）；v2 本件（报告＋证据 2 件）SHA 见卡 t_08b3a1c0 回执。
- 发布仓镜像 P1 = 74ea060（3 件 byte-exact，对齐 WS1；+460 行）；v2 镜像 P2 见卡回执（同以 cmp + sha256 复核 byte-exact）。
- 推送：git push origin main → 06c0637..74ea060（rc=0）；git ls-remote origin main = 74ea0602067873944279f328be9d3d1ae1f4519d（推送时点复核一致）。
- 远端复核（raw）：raw.githubusercontent.com/protreptic/main 三路径 http=200 且字节 SAME —— 页 55,305 B（sha256 944a860c759978495da9ed671da8b481b8143182eda505270748271f051f1c5c）／报告 9,156 B／证据 2,094 B。
- 发布面（Pages）：Deploy to GitHub Pages 随 push 触发（74ea060：run 35952071648，构建中）；文档站点根 https://ovmobilegroup.github.io/protreptic/docs/ 现状 200（既有构建）；本页条目 https://ovmobilegroup.github.io/protreptic/docs/figures/H-AZJ-001/ 于构建完成后可访问（最终状态见卡回执）。
- CI 基线说明：workflow CI（markdown-lint）与 Protreptic CI/CD（可信度门负对照自测）为全仓近期全部 push 的既有失败基线（实证：946afe03 / 2397eeec / 0e5702c3 / 78bac29d / 0dda13ab / d0c7306c / 19e8f58b / 06c06374 等均 failure），与本卡无关；本卡 SHA 的 Quality Gate 两跑均 success。
- parity 复测（v2 提交后）：见卡回执（跑5；预期本卡路径 0 差）。
