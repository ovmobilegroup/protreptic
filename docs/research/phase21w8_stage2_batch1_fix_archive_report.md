# Phase21-W8 Stage2 批1 素材包端修复链档案报告（卡 t_e01c8aa0；修复链尾·文档侧）

- 卡：t_e01c8aa0（pigafetta）｜日期：2026-09-24｜角色：修复链尾·文档侧（修复档案 + 登记链 + 双仓归档）
- 工作仓：/opt/data/workspace/Protreptic（master，本地面）｜发布仓：/opt/data/release/Protreptic-publish（origin/main 面）
- 链：t_2ce1e334（素材包端修复）-> t_a407cb32（独立 QA 复核）-> t_e01c8aa0（本档；登记链刷新）
- 上游钉：修复前锚点 1c00ca8a（父链档案 t_098d8ff6 交付面）；修复提交 A 68fd5569 / B 5705b030；QA 提交 A e7bb276c / B 46c29cbc
- 生成器：build_w8_stage2_batch1_fix_archive.py（幂等；--check 复跑校验）｜独立验收：verify_w8_stage2_batch1_fix_archive.py

## 一、概述

本档将 Phase21 W8 Stage2 批1 素材包端修复链（修复 t_2ce1e334 -> 独立 QA t_a407cb32 -> 文档侧 t_e01c8aa0）的提交链、回执、分级缺陷处置与计数终值装配为九节档案，并完成登记链刷新、双仓归档校验与发布面复核（本卡 = 修复链尾·文档侧）。

- 链级结论（引用上游 + 本卡实测）：QA 分级 F1/F2 已修复并产物再生（计数终值 quote 3 / variant 20 / null 57 / cross-lang 74 条；核中 25->23）、F4 表述收紧落地；QA 复核 PASS（t_a407cb32：双锚点 POST 33/33 + PRE 32/32 + 全扫 36/36 + push 面 35/35；五面全绿）；父链档案（t_098d8ff6）三处登记（§4.5 / §5.1 / §7）随终态刷新，父链独立验收由 30 PASS / 2 FAIL 收口为 33/33 全 PASS（本卡实测）。
- 计数前后对照（本卡独立重算 == 修复回执「引用」）：v1 55 / 22 / 3 / 74 -> F1 单跑 58 / 19 / 3 / 74；F2 单跑 54 / 23 / 3 / 74 -> 终 57 / 20 / 3 / 74（null / variant / quote / cross-lang）；核中 25->23（见证 21->20 + 节引 4->3）；6 行变更、其余 148 行逐字段全等。
- 本卡四件产物：本报告（九节）/ 幂等生成器 build_w8_stage2_batch1_fix_archive.py / 独立验收 verify_w8_stage2_batch1_fix_archive.py / 证据 JSON（docs/research/phase21w8_stage2_batch1_fix_archive_evidence.json 文件）。
- 镜像面（发布仓）：本档报告 + 验收脚本 + 证据 + 父链刷新三件（报告 / 验收 / 证据）随镜像入发布仓（byte-exact + push + ls-remote 复核 通过）；两生成器仅工作仓面（先例体例）。
- 纪律：据实登记；零数据改动（本链零主库写，本卡只新增文档与工具并刷新父链档案登记面）；X 产物（素材包重算报告 / 落地报告 / 工具）仅引用终值、不改其内容。

## 二、背景

### 2.1 修复缘由（引上游 QA）

- 上游 QA（t_e727be57）对 W8 Stage2 批1 全链复核 PASS，另登记素材包端两项真差异（F1 省略号分段 early-return；F2 标点归一集缺 U+FE30 等）与一项口径差（F4 见证位 21/25），建议另卡修正；父链档案（t_098d8ff6）§7 R7-R9 照登为残留（含预计值），处置去向 = 本修复链。
- 船长加注（09-24 13:26）派修复链三卡（t_2ce1e334 -> t_a407cb32 -> t_e01c8aa0；单写者纪律，挂父链 done 后放行）。

### 2.2 链上三卡与时序

| 卡 | 角色 | 执行 | 状态 | 完成时点（CST） | 产物 |
| --- | --- | --- | --- | --- | --- |
| t_2ce1e334 | 素材包端修复（单写者） | elcano | done | 09-24 13:47（收尾提交时点） | 工具修 F1/F2 + 素材包报告再生 + 落地报告 §2.1 收紧 + 回执 |
| t_a407cb32 | 独立 QA 复核（不信任自述） | espinosa | done | 09-24 15:17（回执补记时点） | QA 报告 + QA 证据 + 双锚点校验器 |
| t_e01c8aa0 | 文档侧（修复档案 + 登记链） | pigafetta | running | （本卡） | 本档四件 + 父链登记链刷新四件（含生成器） |

### 2.3 处置口径（引述）

- 等价最小改动：只改 matcher 分段语义（各段全命中）与归一集补两字（U+FE30 / U+3000），不扩面、不改判定档位定义。
- 单写者与零数据：修复面仅文档两报告 + 工具 + 回执（data/audit 内仅回执一件）；不写主库、不动账本（landing ledger）与链接 / 缓存 / 四态。
- 登记链刷新口径（本卡）：父链档案仅刷登记面（§一 计数终值行、§4.5 / §4.6 / §5.1 / §7 登记与指纹、§9.2 / §9.3 指引行），正文其余据实不动。

## 三、方法

### 3.1 取证原则

- 事实来源与口径：一律取 git 对象（短号解析全号 / 日期 / 文件名单）、文件字节（sha256 摘要）、脚本实跑输出；不采信卡面或报告自述（QA 同口径）。
- 引用面与实测面分列：凡引用上游（修复回执 / QA 报告 / 父链档案）之数字均标「引用」；本卡实测者标「实测」。

### 3.2 镜像与发布口径

- 镜像判定 = byte-exact（两仓 sha256 相等）；发布仓侧同时做提交级 blob 逐件对照（镜像提交对齐工作仓对应提交）。
- 发布面复核 = (1) 链件两仓 byte-exact + (2) 提交级 blob 对照 + (3) push 面 ls-remote + (4) 线上站点抽验（时点值）。

### 3.3 生成口径（幂等）

- 本报告由 build_w8_stage2_batch1_fix_archive.py 逐字段装配（生成时实测）；--check 复跑校验（打印 IDEMPOTENT 字样）。
- 归一规则（--check 时替换后比对）：(1) 两仓 HEAD 观测行；(2) ls-remote / parity 观测行；(3) 本档件 sha16 行；(4) §5.1 表内 sha16 列；(5) 线上抽验时点行。其余全文逐字节比对。
- 回执区（第四.8 节）为提交后回填区：v1 落盘时为占位，v2（回执补记）回填 v1 实测值；终态以卡面完成 metadata 为准（先例体例）。

### 3.4 验收口径（第二实现）

- verify_w8_stage2_batch1_fix_archive.py 为第二实现（不 import 生成器）：独立读取本报告、两仓文件、git 对象与链上数据逐项断言。
- 段目 A 至 G 如下：A 档案结构；B 双仓面（byte-exact + 提交级 blob）；C 提交链（逐条 git 实测 + 锚点 + 对齐）；D 链数据面（sha16 登记复核 / 计数重算 / 6 行归因 / 三段一致性）；E 记录面（F0-F6 / 回执区 / 父链收口）；F 反向注入自检；G 链复核（QA 校验器三锚点复跑，可选 push 面）。

### 3.5 纪律声明

- 零数据改动：本卡提交面只含 docs/research 两件新增 + 两个新增根级脚本 + 父链刷新四件（档案报告 / 验收脚本 / 证据 / 生成器）；未触碰 data、web、tools 内既有件。
- 据实登记：父链刷新前后值、计数终值、窗口内他卡在途状态，一律钉锚登记，不吸收窗口外状态。

## 四、执行（登记链）

### 4.1 卡片链（3 卡）

| 卡 | 角色 | 执行 | 状态 | 对应提交（本链） | 产物 |
| --- | --- | --- | --- | --- | --- |
| t_2ce1e334 | 素材包端修复（单写者） | elcano | done | 68fd5569 + 5705b030 | 工具 + 素材包报告 md/json + 落地报告 §2.1 + 回执 |
| t_a407cb32 | 独立 QA 复核（不信任自述） | espinosa | done | e7bb276c + 46c29cbc | QA 报告 + QA 证据 + 双锚点校验器 |
| t_e01c8aa0 | 文档侧（修复档案 + 登记链；本卡） | pigafetta | running | （本卡回执区） | 本档四件 + 父链刷新四件 |

### 4.2 工作仓提交登记（修复链 4 笔）

| 仓 | commit | 全号 | 日期 | 卡 | 文件数 | 本档注 |
| --- | --- | --- | --- | --- | --- | --- |
| ws | `68fd5569` | `68fd5569dd18c57b2b21600fd7cb29186fef1867` | 09-24 13:41 | t_2ce1e334 | 5 | 素材包端修复主提交（5 件） |
| ws | `5705b030` | `5705b030a486593982442ce2c94cae829c41e8df` | 09-24 13:47 | t_2ce1e334 | 1 | 回执补记（1 件） |
| ws | `e7bb276c` | `e7bb276c4a0155d1b5693a2fc844d955aa8fa8bb` | 09-24 15:14 | t_a407cb32 | 3 | 独立 QA 主提交（3 件） |
| ws | `46c29cbc` | `46c29cbc39c54ee6933851c2d89b556546d2c2f6` | 09-24 15:17 | t_a407cb32 | 2 | QA 回执补记（2 件） |

### 4.3 发布仓提交登记（镜像 4 笔）

| 仓 | commit | 全号 | 日期 | 对齐工作仓 | 文件数 | 本档注 |
| --- | --- | --- | --- | --- | --- | --- |
| pb | `9afe48e` | `9afe48e279ea492154cca7306b3ac0e05db9bf67` | 09-24 13:41 | `68fd5569` | 5 | 镜像 5 件（byte-exact） |
| pb | `5b693bb` | `5b693bb91498a1fea95435c4d4a1911f59b7dfff` | 09-24 13:47 | `5705b030` | 1 | 镜像 1 件（byte-exact） |
| pb | `0b86fd2` | `0b86fd22432bbe52858ced1300a39a57487a063d` | 09-24 15:14 | `e7bb276c` | 3 | 镜像 3 件（byte-exact） |
| pb | `27c2074` | `27c207417b055a7c5b939cec5e1f635e30f84ae5` | 09-24 15:17 | `46c29cbc` | 2 | 镜像 2 件（byte-exact） |

### 4.4 链产物清单（登记面）

#### 4.4.1 修复面（5 件；ws 68fd5569 / pb 9afe48e）

- tools/build_batch1_sourcing_pack.py —— F1 分段全命中 + F2 归一集补 U+FE30 / U+3000（逐行 diff 见回执 tool.diff_unified 字段）。
- docs/research/phase21w8_stage2_batch1_sourcing_report.json / .md —— 产物再生（计数终值 57 / 20 / 3 / 74；6 行字段重导）。
- docs/research/phase21w8_stage2_batch1_landing_report.md —— §2.1 F4 表述收紧（校订注记，引上游 QA 报告）。
- data/audit/phase21w8_stage2_batch1_sourcing_fix_receipt.json —— 修复回执（计数分解 / 6 行归因 / 40 候选扫描 / 父链影响声明 / 提交面实测）。

#### 4.4.2 QA 面（3 件；ws e7bb276c / pb 0b86fd2）

- docs/research/phase21w8_stage2_batch1_sourcing_fix_qa_report_espinosa.md —— 双锚点第二实现复核报告（五面全绿：缺陷面 / 结论面 / 计数面 / 回页面 / 提交面）。
- docs/research/phase21w8_stage2_batch1_sourcing_fix_qa_evidence_espinosa.json —— QA 结构化证据。
- tools/verify_batch1_sourcing_fix_qa_espinosa.py —— 双锚点校验器（PRE / POST / scan / remote 四模式；只读）。

#### 4.4.3 父链登记链刷新面（4 件；本卡）

- docs/research/phase21w8_stage2_batch1_archive_report.md —— §一 计数终值行 / §4.5 已闭合项与指纹 / §4.6 刷新指引 / §5.1 脚注 / §7 R7-R9 处置落档 / §9.2-§9.3 指引（刷新前后对照见 §5.2）。
- verify_w8_stage2_batch1_archive.py —— E1 指纹值刷新（74e443cf3f5e6614）+ 新增 E4 登记链检查。
- docs/research/phase21w8_stage2_batch1_archive_evidence.json —— 刷新重生成（本轮 33/33 全 PASS 收口）。
- build_w8_stage2_batch1_archive.py —— 生成器 pin 与登记文本刷新（ws-only 面）。

### 4.5 F0-F6 全部分级缺陷处置状态（表）

| 编号 | 级别 / 出处 | 内容摘要 | 处置状态 | 落点与证据 |
| --- | --- | --- | --- | --- |
| F0（QA 报告 §3 口径；= 账本 QA-F3） | 真差异·账本端（已修正） | four_state.before 陈旧口径（932 / 1828 / 51，modes 3162 口径） | 已修正（上游 QA t_e727be57；corrections QA-C0） | 账本 corrections[0] + 报告 §4.2 / 证据 four_state / status_flips 三向一致 |
| F1（= 账本 QA-F1） | 真差异·素材包端 | matcher 省略号分段 early-return；M-GX-007 / M-WB-010 / M-ZDY-005 尾段失配 | 已修复（t_2ce1e334；分段全命中 + 重算） | 三行落 null（近似档 0.400 / 0.448 / 0.364）；单跑核中 25->22 相符；见 §4.6 |
| F2（= 账本 QA-F2） | 真差异·素材包端 | 归一集缺 U+FE30 / U+3000；M-ZXC-008 / M-LJY-002 | 已修复（t_2ce1e334；补两字 + 重算） | 40 候选全扫仅两枚翻转；单跑 null 55->54 / variant 22->23 相符；见 §4.6 |
| F3（账本 findings 口径；内容 = QA 报告 §3 之 F0） | 同 F0 行（编号两口径并存，照实登记） | four_state.before 陈旧口径（同 F0） | 已修正（同上；QA 卡内规范为 corrections[0].id = QA-C0） | 账本 findings QA-F3 原文 + QA 报告 §4 复核指纹表 |
| F4 | 口径差·表述面 | 素材包报告 §2.1「见证位逐条随行」实为 21/25（4 条节引型无单点见证） | 表述收紧（t_2ce1e334；落地报告 §2.1 校订注记） | 终值见证 20 + 节引 3；上游 QA 复核确认 |
| F5 | 窗口差 | 链接复核时点分布变化（173/5 vs 146/32）+ 并发窗口在途 | 登记（钉锚处理；不吸收窗口外状态） | QA 报告 §2 窗口注记；本档 §七 R3 |
| F6（= 账本 QA-F6；含 corrections QA-C1 / QA-C2） | 真差异·账本端 + 工具（已修正） | 书级列键格式缺陷；links_added 空映射 | 已修正（上游 QA；数据修实 + 工具根因修复） | link True 8 / cache True 17 / URL 8；重生成不复现 |

- 口径注记：F0 / F3 同项两编号（QA 报告与证据用 F0；账本 findings 用 QA-F3），本表并列登记；F1 / F2 / F4 由本修复链执行，F0 / F3 / F6 由上游 QA 卡内修正。

### 4.6 计数前后对照（素材包 154 条；本卡独立重算）

| 阶段 | null | variant | quote | cross-lang | 注 |
| --- | --- | --- | --- | --- | --- |
| v1（修复前） | 55 | 22 | 3 | 74 | 1c00ca8a 面（git 对象实测） |
| F1 单跑 | 58 | 19 | 3 | 74 | 分段全命中（3 行 variant 转 null） |
| F2 单跑（FE30；补 U3000 同值） | 54 | 23 | 3 | 74 | 补字（ZXC-008 null 转 variant；LJY-002 路径升级无计数差） |
| 终（F1 + F2） | 57 | 20 | 3 | 74 | == 报告 JSON verdict_counts（本卡重算） |

- 核中（quote + variant）25->23：见证 21->20 + 节引 4->3（core_stats 本卡重算）。
- 6 行变更明细：M-GX-007 / M-WB-010 / M-ZDY-005（variant 转 null）；M-ZXC-008（null 转 variant zh-hant）；M-LJY-002（sent-composite 转 zh-hant 直击）；M-DZS-006（evidence 窗刷新，判档不变）。
- 其余 148 行逐字段全等（本卡按 git 对象 v1 与磁盘 v2 全字段比对）；quote 154/154 与 quote_hant 无差异。
- 负对照 16 条零假阳性（v1 / v2 两轮）；近似档 null_near_partial = 28（报告 JSON counts 实测）。

### 4.7 本卡动作与镜像集

- 本卡四件：docs/research/phase21w8_stage2_batch1_fix_archive_report.md（本报告）/ build_w8_stage2_batch1_fix_archive.py（生成器；ws-only）/ verify_w8_stage2_batch1_fix_archive.py（第二实现）/ docs/research/phase21w8_stage2_batch1_fix_archive_evidence.json（证据）。
- 父链刷新四件（随本卡提交）：档案报告 / 验收脚本 / 证据（均随镜像）+ 生成器（ws-only 面）。
- 镜像集（发布仓）：本档报告 + 验收脚本 + 证据 + 父链报告 / 验收 / 证据 = 6 件（byte-exact 与 push 面）。

### 4.8 提交 / 镜像 / push 回执（本卡；回执区）

- stage：v1（回执初版；v2 回执补记随 B 笔回填）
- ws_commit_v1：`97cc5b0969a682387b5f6eb225a7c268d20e9b6d`（8 件：本档四件 + 父链刷新四件）
- pb_commit_v1：`fbb4844f8dd101c880c978ac206bafe980ac033f`（镜像 6 件：本档报告/验收/证据 + 父链报告/验收/证据）
- push_v1：ok（e32cb3b4..fbb4844f）
- ws_commit_v2：回执补记提交（报告 v2 + 生成器回填 + 证据 v2；全号随卡面完成 metadata）
- pb_commit_v2：回执补记镜像（报告 v2 + 证据 v2；全号随卡面完成 metadata）
- push_v2：ok（推送后 ls-remote 与发布仓 HEAD 一致；随卡面完成 metadata）
- 终态回执（v2 提交与镜像 sha、ls-remote、校验器终跑）：以卡面完成 metadata 为准（先例体例）。

## 五、证据

### 5.1 链关键件 sha256（双仓对照，生成时点）

| 链件 | 本档注 | 工作仓 sha16 | 发布仓 sha16 | 判定 |
| --- | --- | --- | --- | --- |
| `docs/research/phase21w8_stage2_batch1_sourcing_report.md` | 修复面·产物再生（F1/F2） | `72b1927c17a58a9e` | `72b1927c17a58a9e` | 等于（byte-exact） |
| `docs/research/phase21w8_stage2_batch1_sourcing_report.json` | 修复面·产物再生（F1/F2） | `17265dd82fe6665a` | `17265dd82fe6665a` | 等于（byte-exact） |
| `tools/build_batch1_sourcing_pack.py` | 修复面·matcher 与归一集（F1/F2） | `450d0e752732b9a2` | `450d0e752732b9a2` | 等于（byte-exact） |
| `docs/research/phase21w8_stage2_batch1_landing_report.md` | 修复面·表述收紧（F4） | `74e443cf3f5e6614` | `74e443cf3f5e6614` | 等于（byte-exact） |
| `data/audit/phase21w8_stage2_batch1_sourcing_fix_receipt.json` | 修复面·回执 | `1a62e38355ca1eb9` | `1a62e38355ca1eb9` | 等于（byte-exact） |
| `docs/research/phase21w8_stage2_batch1_sourcing_fix_qa_report_espinosa.md` | QA 面·报告 | `5b926b3e702c6927` | `5b926b3e702c6927` | 等于（byte-exact） |
| `docs/research/phase21w8_stage2_batch1_sourcing_fix_qa_evidence_espinosa.json` | QA 面·证据 | `c221ed5883a962da` | `c221ed5883a962da` | 等于（byte-exact） |
| `tools/verify_batch1_sourcing_fix_qa_espinosa.py` | QA 面·双锚点校验器 | `2508a3a8c6b3718c` | `2508a3a8c6b3718c` | 等于（byte-exact） |
| `docs/research/phase21w8_stage2_batch1_archive_report.md` | 父链刷新·档案报告 | `3b30af2b9aec5cfa` | `3b30af2b9aec5cfa` | 等于（byte-exact） |
| `verify_w8_stage2_batch1_archive.py` | 父链刷新·验收脚本 | `b09f29fc207268f9` | `b09f29fc207268f9` | 等于（byte-exact） |
| `docs/research/phase21w8_stage2_batch1_archive_evidence.json` | 父链刷新·证据 | `6ed4202c6ff54bd8` | `6ed4202c6ff54bd8` | 等于（byte-exact） |

### 5.2 修复面刷新前后对照（4 件；父链面 -> 终值）

| 件 | 刷新前 sha16（父链交付面） | 终值 sha16（生成时点） | 注 |
| --- | --- | --- | --- |
| `docs/research/phase21w8_stage2_batch1_sourcing_report.md` | `e2445bb03922f280` | `72b1927c17a58a9e` | F1/F2/F4 修复随 t_2ce1e334 |
| `docs/research/phase21w8_stage2_batch1_sourcing_report.json` | `a64351a47116dede` | `17265dd82fe6665a` | F1/F2/F4 修复随 t_2ce1e334 |
| `docs/research/phase21w8_stage2_batch1_landing_report.md` | `886a7c90c560e727` | `74e443cf3f5e6614` | F1/F2/F4 修复随 t_2ce1e334 |
| `tools/build_batch1_sourcing_pack.py` | `f35c19da3f64e5c8` | `450d0e752732b9a2` | F1/F2/F4 修复随 t_2ce1e334 |

- 父链登记链刷新（本卡）：档案报告 / 验收脚本 / 证据 / 生成器四件；刷新后父链独立验收由 30 PASS / 2 FAIL 收口为 33/33 全 PASS（本卡实测）。
- 父链复核指纹（修正后）：`74e443cf3f5e6614`（引 QA t_a407cb32 复核；随父链档案 §4.5 登记链复核转绿）。

### 5.3 本档件（生成时点；镜像状态见 §4.8）

- 报告（本件）：docs/research/phase21w8_stage2_batch1_fix_archive_report.md —— 本文件（sha16 随回执回填演进；镜像状态见 §4.8）。
- 生成器：`b321091f9cc1797d`（sha16；ws-only 面）
- 验收脚本：`40a6d5239ce66e05`（sha16）
- 证据：docs/research/phase21w8_stage2_batch1_fix_archive_evidence.json —— 由验收脚本生成（指纹见其 fingerprints 段）。

### 5.4 git 对账与 parity（生成时点观测）

- 工作仓 HEAD（生成时点）：`97cc5b0969a682387b5f6eb225a7c268d20e9b6d`
- 发布仓 HEAD（生成时点）：`fbb4844f8dd101c880c978ac206bafe980ac033f`
- ls-remote（生成时点）：`fbb4844f8dd101c880c978ac206bafe980ac033f`（origin/main）
- parity（生成时点）：status=NOT_RUN；counts={}

### 5.5 发布面线上抽验（时点值）

- 发布面抽验（时点值）：首页 HTTP 200；可信度页 HTTP 200（标记命中=True）；meta.json HTTP 200（verified=?）
- 检查时点：2026-09-24 16:40（CST）

## 六、核验

### 6.1 上游 QA 复核判定（t_a407cb32；引用）

- 五面全绿（引 QA 报告与 QA 证据）：缺陷面（F1/F2/F4 逐项复核）、结论面（计数终值 57 / 20 / 3 / 74 与核中 25->23）、计数面（三段一致性：F1 单跑 / F2 单跑 / 终值）、回页面（at-message 回执相符）、提交面（ws/pb 四笔镜像 + push 面复核）。
- QA 复核判词（引用）：PASS（素材包端修复链复核通过；无新增未闭合项）。

### 6.2 本卡独立验收（第二实现）

- verify_w8_stage2_batch1_fix_archive.py 段目 A-G 实跑（全 PASS；结论见证据 JSON 与卡面完成 metadata）：A 档案结构 / B 双仓面 / C 提交链 / D 链数据面（含 6 行归因重算）/ E 记录面（含父链收口）/ F 反向注入自检 / G 链复核（QA 校验器三锚点复跑）。
- 反向注入自检：六类注入（删标题 / 镜像不符 / 提交号篡改 / sha16 篡改 / 计数篡改 / 回执篡改）逐类捕获（须 6 / 6）。

### 6.3 双仓归档复核（本卡）

- 链关键件两仓 sha256 全等（§5.1 表 11 件逐件；本链面 0 差异）。
- 提交级 blob 对照：pb 9afe48e -> ws 68fd5569（5 件）；pb 5b693bb -> ws 5705b030（1 件）；pb 0b86fd2 -> ws e7bb276c（3 件）；pb 27c2074 -> ws 46c29cbc（2 件）。
- push 面：发布仓 HEAD 与 origin/main 一致（ls-remote；见 §5.4 生成时点观测）。
- 线上站抽验（时点值）：见 §5.5。

### 6.4 父链验收收口复核（30/32 -> 33/33）

- 父链独立验收（verify_w8_stage2_batch1_archive.py，刷新后）：33 PASS / 0 FAIL（本卡实测；E1 指纹与 E4 登记链检查随父链刷新转绿）。
- 旧态对照：30 PASS / 2 FAIL（父链交付面；§5.2 与父链装饰面登记）。

## 七、残留与账务登记

- R1（跨语言 74 条口径）：待船长裁定（引父链档案 §7）；本链未触碰。照登。
- R2（父链其余残留）：引父链档案 §7 逐条照登（R2-R6 与 R10 类 ws-only 件按先例不镜像）。本链未触碰。
- R3（F5 窗口差）：链接复核时点分布变化 + 并发窗口在途（钉锚处理；引 QA §2 窗口注记与父链档案 §7）。
- R4（并发窗口注记）：本卡窗口内多链在途（W7 / W9 / W11 等）；本链提交面一律以本链提交对象复核，不吸收窗口外状态。
- R5（零数据改动声明）：本链零主库写（素材包端仅文档与工具）；本卡只新增文档与工具、并刷新父链档案登记面。
- R6（登记链落点索引）：父链档案 §4.5 / §4.6 / §5.1 / §7 + 本档 §4.5 / §4.6；全链留痕见本报告（路径见 §9.2）。

## 八、下一步

- W8S2B1 修复链闭环（本档为链尾）：归档面收口；批2 及后续批次按设计文档续跑（引父链档案 §八）。
- 父链其余残留（跨语言 74 条待裁定等）移交后续处置（引父链档案 §7）。
- 本档四件 + 父链刷新四件随本卡提交入双仓（v1 / v2 回执见 §4.8）。

## 九、附链

### 9.1 提交全号索引

| 对 | 工作仓 | 发布仓 | 卡 | 注 |
| --- | --- | --- | --- | --- |
| 1 | `68fd5569`（68fd5569dd18c57b2b21600fd7cb29186fef1867） | `9afe48e`（9afe48e279ea492154cca7306b3ac0e05db9bf67） | t_2ce1e334 | 素材包端修复主提交（5 件） |
| 2 | `5705b030`（5705b030a486593982442ce2c94cae829c41e8df） | `5b693bb`（5b693bb91498a1fea95435c4d4a1911f59b7dfff） | t_2ce1e334 | 回执补记（1 件） |
| 3 | `e7bb276c`（e7bb276c4a0155d1b5693a2fc844d955aa8fa8bb） | `0b86fd2`（0b86fd22432bbe52858ced1300a39a57487a063d） | t_a407cb32 | 独立 QA 主提交（3 件） |
| 4 | `46c29cbc`（46c29cbc39c54ee6933851c2d89b556546d2c2f6） | `27c2074`（27c207417b055a7c5b939cec5e1f635e30f84ae5） | t_a407cb32 | QA 回执补记（2 件） |

- 修复前锚点：`1c00ca8a`（父链档案 t_098d8ff6 交付面）。

### 9.2 文档与证据路径

- 本报告：docs/research/phase21w8_stage2_batch1_fix_archive_report.md
- 生成器：build_w8_stage2_batch1_fix_archive.py（ws-only 面）
- 验收：verify_w8_stage2_batch1_fix_archive.py
- 证据：docs/research/phase21w8_stage2_batch1_fix_archive_evidence.json
- 上游链：修复回执（data/audit/phase21w8_stage2_batch1_sourcing_fix_receipt.json）/ QA 报告与证据（docs/research/phase21w8_stage2_batch1_sourcing_fix_qa_report_espinosa.md 等）/ 父链档案（docs/research/phase21w8_stage2_batch1_archive_report.md）

### 9.3 复跑命令

- 幂等：python3 build_w8_stage2_batch1_fix_archive.py --check（打印 IDEMPOTENT 字样）
- 验收：python3 verify_w8_stage2_batch1_fix_archive.py（可选参数：--with-remote、--with-live、--with-chain-repro、--json-out 等）
- 链复核：python3 tools/verify_batch1_sourcing_fix_qa_espinosa.py（默认 POST 面；--at 1c00ca8a 为 PRE 面；--scan 为全扫面；--with-remote 为 push 面）

### 9.4 台账登记（随完成提交）

- /opt/data/cache/protreptic_work_backlog.md：本卡完成后追加行（链闭环 + 双仓提交 / 镜像号 + 验收结论）。

