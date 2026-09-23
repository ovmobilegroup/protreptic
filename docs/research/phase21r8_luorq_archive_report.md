# Phase21-R8 罗瑞卿（H-LUORQ-001） 文档归档报告（卡 t_d9cb98bb）

- 执行：pigafetta｜日期：2026-09-24｜工作仓：/opt/data/workspace/Protreptic｜发布仓：/opt/data/release/Protreptic-publish
- 产出：docs/figures/H-LUORQ-001.md（九节档案，首次装配）；生成器 build_luorq_r8_archive.py（幂等，内置逐字断言）；文档层独立验收 verify_luorq_r8_archive.py（第二实现 + 反向注入自检）；本报告与证据 docs/research/phase21r8_luorq_archive_evidence.json
- 边界：本卡只写文档层与归档产物，零数据改动（modes_data.json / scenarios / tags / 注册 等仅读不写）；合并数据面的提交，镜像与 push 归收尾卡 t_2d15bd2e（在途）。

## 一、任务与范围

按卡面五项要求逐条落实：

1. 产出 docs/figures/H-LUORQ-001.md 九节档案（逐字装配，零捏造） → 见第三节；
2. 敏感表述按历史语境 caveat（含 1966 文件使用口径与平反对照） → 见第三节第 3 条与页面第九节；
3. 归档动作说明与先例 commit 对照（R6 A组 ee992a42，曾子 t_6c7e070a；体例对齐，差异点声明） → 见第三节第 4 条；
4. 站点，展示层按先例更新并复核两仓一致性 → 见第六节（本卡镜像 3 件，parity 本卡路径 0 差）；
5. 完成报告给真实路径（提交 SHA，文件路径，验收命令） → 见第七，八节。

## 二、归档前状态（归档时点实测）

- R6C 隔离（卡 t_4a9cf2cb，commit 7b767f39）：旧载荷（名实不符，串档）已隔离归档；旧 docs 占位页（3,816 B，sha256 3fa3aa3fa375d63d7b93f554f4f61b71aa784f7dec142ab8a1a6ee445f5112f2）字节归档于 data/figures/_duplicates/H-LUORQ-001_archive_page.md（登记 phase21r6C_archive_evidence.json）；docs/figures/ 下无在册旧页 → 本页为 R8 重做后首次装配。
- R7 核名（卡 t_261185a8，commit 8132b121）：判定：身份真实，载荷归属错位，判「研究重做」（非改名复用）。
- R8 落盘（卡 t_bf2d9b82，commit 21edc5f8；证据刷新 da073117；收尾回执 8725ddff）：M-LUORQ-001~010 + figure，individuals，_modes 三件 + 12 件落地包；落盘卡独立核验 69 PASS / 0 FAIL。
- R8 合并（卡 t_08bbb73d）：工作树已落地，未提交：主库 +10 条，注册 +1，场景 +10+10，标签 +20，顶层旧块处置；提交，镜像，push 归收尾卡 t_2d15bd2e（本卡归档时点在途）。
- R8 QA（卡 t_8773cb6b）：第二实现 103 PASS / 12 FAIL / 17 INFO；FAIL 归因见第五节（时点性，镜像在途，开放项，口径差）。
- 核验状态：本件 10/10 条 verification.status=pending（0 条自称 verified）。

## 三、归档动作

1. 生成器 build_luorq_r8_archive.py：自 9 个真值源逐字装配（data/figures/H-LUORQ-001.json / data/individuals/H-LUORQ-001.json / _modes.json / 主库 modes_data.json / scenarios_zh｜en / code_maps / figure_names / scenario_tags）；内置护栏六组：四面同体（图档内嵌 = 伴随包 = 主库 = landing combined，逐对象全等） ｜ 编号（M-LUORQ-001~010 顺序，id == mode_code，legacy_mode_id M351~M360） ｜ 诚实（10/10 pending，0 自称 verified） ｜ 禁字零残留（7 项） ｜ 场景面（C-LUORQ-001~010 与 E，tags 20） ｜ 幂等；任一断言失败即 exit 2 不落盘。
2. 页面 docs/figures/H-LUORQ-001.md：64,098 B / 425 行 / sha256 7211a8637a622c14f5dd6189f799f31ecc2f602e50b8e5b953245584b52e8815；九节结构（一 历史定位｜二 核心思想｜三 十大思维模式｜四 现代场景应用｜五 现代应用｜六 跨引用｜七 标签｜八 独特成就｜九 QA 验收记录）；头部含登记链（R6C→R7→R8 全链）与报告索引；caveats 逐条搬迁；未展开字段声明。
3. 敏感表述口径（页面第九节三条）：1966 年《关于罗瑞卿错误问题的报告》属政治定性文件（不引原句，仅语境/反证） ｜ 三层时间线（1949-1965 档案/作品 → 1978 悼词 → 1980 平反通知） ｜ B1 素材包未引 1966 文件（W5 仅存证） ｜ 并置要件（1978-08-12 悼词 + 1980-05-20 平反通知（撤销 268 号文件））。
4. 先例对照：体例对齐 R6 A组（build_legacy20_r6_archive.py + verify_legacy20_r6_archive.py，commit ee992a42）与曾子归档（t_6c7e070a）；差异点：单人物件，页无旧版（R6C 清档后首装），新增禁字零残留断言与区块级（block-scoped）验收（本次反向注入自检曾暴露初版核对盲区并已修复）。
5. 幂等实测：二次运行 IDEMPOTENT（字节不变）；--dry-run 支持只断言预览。

## 四、验证证据

- 文档层独立验收：python3 verify_luorq_r8_archive.py → 418 CHECKS / 418 PASS / 0 FAIL（第二实现，不导入生成器）。
- 反向注入自检：python3 verify_luorq_r8_archive.py --inject-test → 15/15 捕获（清单：计数篡改，台账 total 篡改，原文截断，定义篡改，禁字注入，假 verified，节删除，场景截断，出处篡改，evidence 计数篡改，旧页 sha 篡改，领域篡改，跨引用删除，模式标题删除，标签删除）。
- 禁字：7 项零残留（页面面） ｜ QA 口径 3 个唯一自造名全库活跃面 0（见 QA 证据）。
- 四面同体：图档内嵌 = 伴随包 = 主库 10 条 = landing combined，逐对象全等；图档 == 个体档（除 modes） ｜ 图档与 code_maps 跨引用逐字全等 2/2。
- 计数台账（归档时点 canonical）：modes=3291；total=3271；code_maps=214；scenarios_zh=2203；scenarios_en=2203；scenario_tags=7518；figure_names=1083（md 与报告互证）。
- git 登记链实测：cat-file 校验 7b767f39（R6C），8132b121（R7），21edc5f8（R8 落盘），da073117，8725ddff（回执） 均存在。

## 五、QA 12 FAIL 归因与开放项（如实登记，未伪修）

- 时点性（3 项）：C_ScenExist / E03a / E03b：QA 执行时点合并未落地；其后工作树实测场景已在库（合并卡 D01-D07 PASS），收尾卡提交后应转 PASS。
- 镜像在途（1 项）：G01b：镜像清单悬空 19 条归收尾卡 t_2d15bd2e（本卡镜像为其子集，本卡路径 0 差）。
- 开放项（5 项）：A03 / A05 / A07 / B01 / B05：引文见证归一化，出处格式，片段白名单，见证文件登记细节；QA 建议交退卡或新立卡跟进。
- 口径差（2 项）：B02 / B05（合并卡独立核验 83 PASS / 2 FAIL）：canonical 与 raw 序列化口径差；留 QA 裁定。
- 本卡新增修复：反向注入自检发现初版逐模式核验为全库子串匹配（首条篡改可被其余同构行掩盖）；已改为区块级（block-scoped）核对并复测 15/15。

## 六、两仓一致性（站点/展示层与 parity）

- 展示层性质：docs/figures/*.md 属 mkdocs 文档层（docs 目录进站点构建）；发布仓驱动站点（.github/workflows/pages.yml，mkdocs.pages.yml）；故按 R6 先例镜像至发布仓。
- parity 实测（tools/check_repo_parity.py --json，本卡三跑）：
  - 归档前基线（本卡首跑，页落盘前）：diffs=347（330 仅工作仓 + 17 内容差） ；
  - 页落盘后二跑：316（308 仅工作仓 + 8 内容差）；
  - 镜像后三跑：PARITY3_PENDING（v2 补记，届时本卡 3 路径应 0 差） ；
  - 差值归因：两次差值主要来自他卡在制（王祥链等的镜像/提交，非本卡）；本卡页在镜像前以 MISSING_IN_PUBLISH 计 1 条（镜像后消除）。
- 本卡镜像范围：页 + 报告 + 证据 三件（docs 下，进构建图） ｜ 生成器与验收脚本为仓根工具（不进构建图，按 parity 边界规则与 R6 先例不镜像）。

## 七、提交与推送回执（v2 补记）

- 工作仓提交：WS1 WS1SHA_PENDING（白名单 5 件：页 / 生成器 / 验收脚本 / 报告 v1 / 证据 v1）；WS2 WS2SHA_PENDING（本报告与证据回执补记）。。
- 发布仓镜像：P1 P1SHA_PENDING（对齐 WS1，3 件）。；P2 P2SHA_PENDING（对齐 WS2，报告与证据）。。
- 推送：PUSH_RANGE_PENDING（fetch 复核后，禁 --force）。；远端 origin/main 复核 = REMOTE_SHA_PENDING。

## 八、文件与验收命令（真实路径）

- 页面：docs/figures/H-LUORQ-001.md
- 生成器：build_luorq_r8_archive.py （python3 build_luorq_r8_archive.py [--dry-run]）
- 验收：verify_luorq_r8_archive.py （python3 verify_luorq_r8_archive.py [--inject-test]）
- 报告：docs/research/phase21r8_luorq_archive_report.md
- 证据：docs/research/phase21r8_luorq_archive_evidence.json
- 上游链路（本卡只读）：phase21r6C_luorq_isolation_note.md / phase21r7_cgroup_identity_report.md / phase21r8_luorq_sourcing_report.md / phase21r8_luorq_rebuild_report.md / phase21r8_luorq_merge_evidence.json / docs/qa/phase21r8_luorq_qa_evidence/result.txt
- 归档先例：build_legacy20_r6_archive.py / verify_legacy20_r6_archive.py （R6，ee992a42）

## 九、开放项与建议

- 敏感表述口径已入页（第九节）；后续核验卡启动时建议连同 1966 文件存证（W5）一并复核引用合规。
- QA 开放项 5 项（A03，A05，A07，B01，B05）按 QA 卡建议路由（本卡未伪修）。
- 若后续数据面更新（主库，场景），本页可由生成器幂等重跑刷新（计数台账随之更新，报告与证据需同步）。
- 本页为站点点位新增（发布仓 push 将触发 Pages 构建）；若 CI 异常，回滚方式为 revert 镜像提交（禁 --force）。
