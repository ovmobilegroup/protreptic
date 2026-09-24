# Phase21-W8 Stage2 批1 全链档案报告（卡 t_098d8ff6；W8 链尾·文档归档）

- 卡：t_098d8ff6（pigafetta）｜日期：2026-09-24｜角色：W8 链尾·文档归档（九节档案 + 登记链）
- 工作仓：/opt/data/workspace/Protreptic（master，本地面；工作仓不设 push 义务）｜发布仓：/opt/data/release/Protreptic-publish（origin/main 面）
- 链：t_6ed4fe0d（书单）-> t_70a8cbce（素材包）-> t_b85ae14a（落地）-> t_e727be57（QA）-> t_098d8ff6（本档）
- 上游钉：W8 数据锚点 eda40f5b（与 004332b4 同面）；QA 提交 A b5967043 / B b0e2b0a8
- 生成器：build_w8_stage2_batch1_archive.py（幂等；--check 复跑校验）｜独立验收：verify_w8_stage2_batch1_archive.py

## 一、概述

本档将 Phase21 W8 Stage2 批1 全链（研究 t_6ed4fe0d -> 工具/素材包 t_70a8cbce -> 主库落地 t_b85ae14a -> 独立 QA t_e727be57 -> 文档归档 t_098d8ff6）的提交链、回执与逐条处置装配为九节档案，并完成链级档案、逐条处置登记、双仓归档校验与发布面复核（本卡 = W8 链尾·文档归档）。

- 链级结论（引用上游报告 + 本卡实测）：批1 处置已入主库（8 书链接、17 缓存合并、四态 69 + 3 翻面、findings 增 3 条），QA 终判 PASS（校验器 27/27；3 项账本修正 + 1 项工具根因修复闭合）；两仓归档 byte-exact 等同；push 面 ls-remote 一致；parity 差异归零。
- 素材包口径数字（引用 t_70a8cbce / t_b85ae14a 登记）：18 项（17 书 + 现代诗否定记录）、154 条 mode 引文逐条有账（quote 3 / variant 22 / null 55 / cross-lang 74 条）、负对照 16 条零假阳性；落地零改字（改动仅链接、缓存、状态、findings 四处）。
- 本卡四件产物：本报告（九节）/ 幂等生成器 build_w8_stage2_batch1_archive.py / 独立验收 verify_w8_stage2_batch1_archive.py / 证据 JSON（docs/research/phase21w8_stage2_batch1_archive_evidence.json 文件）。
- 镜像面：本档报告 + 验收脚本 + 证据随镜像入发布仓（byte-exact + push + ls-remote 复核 通过）；生成器仅工作仓面（先例体例）。
- 纪律：据实登记；零数据改动（本卡未触碰 data / web / docs/figures 内的任何数据文件；只新增文档与工具）。

## 二、背景

### 2.1 Stage2 由来与批1 定义

- W5 pilot（王充）已跑通并进入修复链；用户 2026-09-24 拍板 Stage2「开跑」。设计文档 /opt/data/cache/phase21w5_citation_pilot_design.md 第 6 节：Stage2 = 书级归并重扫 -> 逐本 resolve -> fetch -> 状态重跑，分批交付。
- 批1 = 68 本「被引 >= 3 且缺索引」书中热门 Top 集：书单定稿 18 项（17 种书 + 现代诗否定记录；159 处引文实例 / 154 条 mode 级引文）。
- 上游书单卡根因一并登记：候选生成旧口径（条目内去重 + 篇章跨度）漏收 68 本，已在 t_70a8cbce 修复为书级归并重扫（--bookcount-report；baseline 复扫 68 本与书单 hot68 逐名一致；旧口径 59；差集 9 本只漏不收）。

### 2.2 链上五卡与时序

| 卡 | 角色 | 执行 | 状态 | 完成时点（CST） | 产物 |
| --- | --- | --- | --- | --- | --- |
| t_6ed4fe0d | 启动研究·书单 | serrano | done | 09-24 09:19 | docs/research/phase21w8_stage2_batch1_booklist.md/.json |
| t_70a8cbce | 工具/管道·fetch 素材包 | elcano | done | 09-24 11:18 | docs/research/phase21w8_stage2_batch1_sourcing_report.md/.json + data/audit/source_texts_w8_stage2_batch1.json |
| t_b85ae14a | 主库落地（单写者） | barbosa | done | 09-24 12:00 | docs/research/phase21w8_stage2_batch1_landing_report.md + landing_evidence.json + data/audit/phase21w8_stage2_batch1_landing_ledger.json |
| t_e727be57 | 独立 QA（不信任自述） | espinosa | done | 09-24 13:00 | docs/research/phase21w8_stage2_batch1_qa_report_espinosa.md + qa_evidence_espinosa.json + tools/verify_batch1_qa_espinosa.py |
| t_098d8ff6 | 文档归档（本卡） | pigafetta | running | （本卡） | 本档四件（报告/生成器/验收脚本/证据） |

- 卡链派发（五卡同批）：09-24 08:01:22（各卡 created_at 同一时点）。
- 本档登记链以上表 + 第四.2 / 4.3 提交登记为准。

### 2.3 批1 语义（处置口径引述）

- 三条口径（引述落地报告 2.1 节）：①已核条目「不改字」（逐字 / 繁简 / 节引对读结论入账本）；②查无、源外、否定、跨语言逐条登记不改引文（不假装核过，也不虚报不符）；③真差异按既有 D4 流程登记（3 条）。
- 跨语言 74 条：不建链接、不改状态、留语义对照档（口径待船长裁定；本档照登）。
- 落地纪律：单写者 + 先备份后落地 + 零越界（包外零翻面；R9 两卡 20 条自定义印记回填保护）。

## 三、方法

### 3.1 取证原则

- 事实来源与口径：一律取 git 对象（短号解析全号 / 日期 / 题名）、文件字节（sha256 摘要）、工具实跑输出；不采信卡面或报告自述（QA 同口径）。
- 引用面与实测面分列：凡引用上游（素材包 / 落地 / QA 报告）之数字均标「引用」；本卡实测者标「实测」。
- 判决面不回避：QA 未闭合项（F1 与 F2）照登为残留，不因本档收敛而改写。

### 3.2 镜像与发布口径

- 镜像判定 = byte-exact（两仓 sha256 相等）；发布仓侧同时做提交级 blob 逐件对照（镜像提交对齐工作仓对应提交）。
- 发布面复核 = (1) 两仓 byte-exact + (2) 提交级 blob 对照 + (3) push 面 ls-remote + (4) 线上站点抽验（时点值）。
- 站点展示层：本链为数据与文档面（无新增页面 / 路由 / 文案）；两仓一致性以镜像 byte-exact 复核替代，另附线上抽验。

### 3.3 生成口径（幂等）

- 本报告由 build_w8_stage2_batch1_archive.py 逐字段装配（生成时实测）；--check 复跑校验。
- 归一规则（--check 时替换后比对）：(1) 两仓 HEAD 观测行；(2) parity / ls-remote 观测行；(3) 本档件 sha 行；(4) 数据面现值列（生成时点观测）。其余全文逐字节比对，打印 IDEMPOTENT 字样。
- 回执区（第四.7 节）为提交后回填区：v1 落盘时为占位，v2（回执终版）回填 v1 实测值，v2 及终态 sha 以卡面完成 metadata 为准（先例同体例）。

### 3.4 验收口径（第二实现）

- verify_w8_stage2_batch1_archive.py 为第二实现（不 import 生成器）：独立读取本报告、两仓文件、git 对象与链上数据逐项断言。
- 段目 A 至 F 如下：A 档案结构；B 镜像面（byte-exact + 提交级 blob）；C 提交链（逐条 git 实测 + 锚点）；D 链数据面（sha16 登记 / 三段 pin / 备份 / 缓存计数 / 四态与翻面重算）；E 记录面（QA 回执 / 残留 / 回执区）；F 反向注入自检。
- 自检：6 类突变注入，断言每类必被对应段捕获。

### 3.5 纪律声明

- 零数据改动：本卡提交面只含 docs/research 新增件 + 根级两个脚本；未触碰 data 与 web 与 tools 的既有件。
- 据实登记：知名不符项（如提交信息称 23 txt 而文件面实测 20 件之差）一并登记，不以卡面或提交信息转述替代实测。

## 四、执行（登记链）

### 4.1 卡片链（5 卡）

| 卡 | 角色 | 执行 | 状态 | 对应提交（本链） | 产物 |
| --- | --- | --- | --- | --- | --- |
| t_6ed4fe0d | 启动研究·书单 | serrano | done | 20b13092 | docs/research/phase21w8_stage2_batch1_booklist.md/.json |
| t_70a8cbce | 工具/管道·fetch 素材包 | elcano | done | ce1dc46b + 60d5d509 + 58f34f88 | docs/research/phase21w8_stage2_batch1_sourcing_report.md/.json + data/audit/source_texts_w8_stage2_batch1.json |
| t_b85ae14a | 主库落地（单写者） | barbosa | done | 004332b4 + eda40f5b | docs/research/phase21w8_stage2_batch1_landing_report.md + landing_evidence.json + data/audit/phase21w8_stage2_batch1_landing_ledger.json |
| t_e727be57 | 独立 QA（不信任自述） | espinosa | done | b5967043 + b0e2b0a8 | docs/research/phase21w8_stage2_batch1_qa_report_espinosa.md + qa_evidence_espinosa.json + tools/verify_batch1_qa_espinosa.py |
| t_098d8ff6 | 文档归档（本卡） | pigafetta | running | （本卡） | 本档四件（报告/生成器/验收脚本/证据） |

### 4.2 工作仓提交登记（8 笔）

| 仓 | commit | 全号 | 日期 | 卡 | 题名 | 本档注 |
| --- | --- | --- | --- | --- | --- | --- |
| ws | `20b13092` | `20b13092038ae16d0290b0434b7026f1c820e9d6` | 09-24 09:19 | t_6ed4fe0d | Phase21 W8 Stage2批1 t_6ed4fe0d 交付：热门书 Top18 书单 + 来源链预解析（68 本对账复核, 18 项逐本实测, 零库写） | 书单主提交（2 件） |
| ws | `ce1dc46b` | `ce1dc46b15da56b6d570ff341e3d9b0a40e279e0` | 09-24 11:15 | t_70a8cbce | Phase21-W8 Stage2批1 t_70a8cbce 交付：书级归并重扫口径修复(--bookcount-report, 68 本对账复现) + 批1 fetch 素材包(17 书缓存/独立索引 + 154 条逐条 quote/异文/查无 + 16 项独立核验全 PASS; 零主库写) | 素材包主交付（34 件：缓存 20 txt + 独立索引 / 素材包 / 9 工具） |
| ws | `60d5d509` | `60d5d5090fd1d0e1f587dced4dac2c72bd14bf23` | 09-24 11:16 | t_70a8cbce | Phase21-W8 Stage2批1 t_70a8cbce 回执补记：报告 §10 提交回执入库（主提交 ce1dc46b；核验 16 PASS 复跑；成品 sha16 存档） | 回执补记（4 件） |
| ws | `58f34f88` | `58f34f88ab58bbd2bdb75b6055761e72f23758ca` | 09-24 11:17 | t_70a8cbce | Phase21-W8 Stage2批1 t_70a8cbce 字段校正：§4.2 增通道列(庄子注/老子注=render 实测) + 抓取项口径澄清 + pack per_book.method | 字段校正（4 件） |
| ws | `004332b4` | `004332b43637c45447938f7b5b550fa6ce0ff8af` | 09-24 11:54 | t_b85ae14a | Phase21-W8 Stage2批1 t_b85ae14a 主库落地：8 书链接入库(source_links 383->391) + 17 缓存合并(source_texts 97->114) + 四态重跑(pending->verified 69/pending->suspect 3；全库 verified 949->1018) + findings 165->168(D4_quote_mismatch +3) + 站链/构建收口 + 逐条账本/报告/证据/核验器(20 PASS)；先备份后落地；零越界：包外零翻面 + R9 20 条印记回填保护 | 落地主提交（13 件白名单；名单外 0） |
| ws | `eda40f5b` | `eda40f5ba3c8395c6655501c153f6a69ce81651d` | 09-24 11:58 | t_b85ae14a | Phase21-W8 Stage2批1 t_b85ae14a 回执补记：报告 §9 提交回执（工作仓 004332b4 / 发布仓 023a794 / push 7f03402..023a794 / ls-remote 一致 / parity 42 项闭合 0 新增）+ 证据镜面刷新（mirror_push done + 产物 sha 重算） | 回执补记（2 件） |
| ws | `b5967043` | `b5967043d9c3b57d15d0894dad52f1e176f9b4ba` | 09-24 12:55 | t_e727be57 | Phase21-W8 Stage2批1 独立 QA 复核（卡 t_e727be57 / espinosa）：① 账本 four_state.before 修正为备份态实测 949/1959/52/351（口径对齐至 3311；原值取自 09-22 陈旧状态文件 modes 3162 口径）；② 账本书级列 link/cache 键归一修正（8 链接 / 17 合并 / sha 全等）+ cross_checks.links_added 修实（8 键）；③ 工具 build_batch1_landing_ledger.py 键归一根因修复；④ 报告附录 B / 证据 outputs 跨引刷新（账本 4dc2d8e3 / 报告 0eb4c12b）；⑤ 新增 QA 报告 + QA 证据 + 双锚点校验器（复核前 6 项缺陷断言可复现；复核后全 PASS）。 | QA 复核提交 A（7 件） |
| ws | `b0e2b0a8` | `b0e2b0a84d53c7028908885b104f6745245b3a62` | 09-24 12:59 | t_e727be57 | Phase21-W8 Stage2批1 QA 回执补记（卡 t_e727be57 / espinosa）：QA 报告 §6 提交回执（工作仓 A b5967043 / 发布仓 P1 88cc86a / push 58f361d..88cc86a / ls-remote 一致 / 校验器 --at A 27/27 全 PASS）+ 账本 corrections[0].id 规范 QA-C0 + 报告/证据跨引终版刷新（账本 84ff028da6bee8d4 / 报告 886a7c90c560e727 / 证据 0a6f5a5ae266281b / 校验器 4d55095b5776a82f）。 | QA 回执补记 B（6 件） |

- 工作仓为本地 master 面（无 push 义务）；本链 8 笔 = 书单 1 + 素材包 3 + 落地 2 与 QA 2 笔。

### 4.3 发布仓提交登记（4 笔）

| 仓 | commit | 全号 | 日期 | 卡 | 题名 | 本档注 |
| --- | --- | --- | --- | --- | --- | --- |
| pb | `023a794` | `023a79488b94c779d44e882590384cddbabfc792` | 09-24 11:56 | t_b85ae14a | 镜像: Phase21-W8 Stage2批1 t_b85ae14a 主库落地（对齐工作仓 004332b4）：本卡 13 件（链接/缓存/四态/findings/账本/报告/证据/3 工具/站面计数/manifest）+ W8 链落盘包 37 件（批1 缓存 23 txt + 素材包/书单/索引/recount/submission + 6 工具 + w8 manifest）byte-exact | 镜像 50 件（落地 13 + 链落盘包 37；含 20 txt） |
| pb | `c522897` | `c52289770a544064a36d3346f674f164cb2af4ef` | 09-24 11:58 | t_b85ae14a | 镜像: Phase21-W8 Stage2批1 t_b85ae14a 回执补记（对齐工作仓 eda40f5b）：报告 §9 回执 + 证据 mirror_push 刷面 2 件 byte-exact | 镜像 2 件（落地报告 / 证据） |
| pb | `88cc86a` | `88cc86a7ef56917216cb52972daad50114e738f2` | 09-24 12:55 | t_e727be57 | 镜像: Phase21-W8 Stage2批1 独立 QA 复核（卡 t_e727be57 / espinosa，对齐工作仓 b5967043d9c3b57d15d0894dad52f1e176f9b4ba）：账本 four_state.before 修正（949/1959/52/351）+ 书级列 link/cache 键归一修正 + cross_checks.links_added 修实 + 工具 build_batch1_landing_ledger.py 根因修复 + 报告/证据跨引刷新 + 新增 QA 报告 / QA 证据 / 双锚点校验器 — 7 件 byte-exact | 镜像 7 件（QA 面：账本 / 报告 / 证据 / 工具 / 新增 3 件） |
| pb | `384faae` | `384faaea68efa32df41a9f412e24173a7010c637` | 09-24 12:59 | t_e727be57 | 镜像: Phase21-W8 Stage2批1 QA 回执补记（卡 t_e727be57，对齐工作仓 b0e2b0a84d53c7028908885b104f6745245b3a62）：报告 §6 回执 + 账本 corrections id 规范 + 跨引终版刷新 + 校验器 F2 兼容 —— 6 件 byte-exact | 镜像 6 件（QA 回执面） |

- 发布仓 = origin/main 面（GitHub Pages 构建源）；四笔镜像分别对齐工作仓 004332b4 / eda40f5b / b5967043 / b0e2b0a8 四笔（提交级 blob 对照见第六.3 节）。
- push 链：58f361d..88cc86a..384faae 段（QA 两笔登记）；023a794 与 c522897 笔见落地回执（7f03402..023a794..c522897 区间）。

### 4.4 链产物清单（登记面）

#### 4.4.1 文档面（8 件）

- docs/research/phase21w8_stage2_batch1_booklist.md / .json —— 书单与来源链预解析（t_6ed4fe0d；含 hot68 全量 rows、batch1 18 项、method 口径）。
- docs/research/phase21w8_stage2_batch1_sourcing_report.md / .json —— 素材包报告（t_70a8cbce；含 154 条逐条结论 quotes 段与 18 项缓存状态）。
- docs/research/phase21w8_stage2_batch1_landing_report.md —— 落地报告（t_b85ae14a；结论总览 + 逐条处置 + 门禁四态 + 站链 + 附录 A/B/C + 提交回执）。
- docs/research/phase21w8_stage2_batch1_landing_evidence.json —— 落地证据（收据汇总：输入 / 产物 sha、门禁、站链、核验 20 PASS、镜像 / push 回执）。
- docs/research/phase21w8_stage2_batch1_qa_report_espinosa.md —— QA 报告（t_e727be57；核验矩阵 17 项 + 分级缺陷 + 复核指纹 + 提交回执）。
- docs/research/phase21w8_stage2_batch1_qa_evidence_espinosa.json —— QA 证据（结构化；与 QA 报告互为镜像）。

#### 4.4.2 数据与审计面（6 件）

- data/audit/phase21w8_stage2_batch1_landing_ledger.json —— 逐条账本（154 条处置 + 书级 18 + 翻面 + 四态 + cross_checks + QA addendum 全集；裁决 PASS 档）。
- data/audit/phase21w8_stage2_batch1_recount_baseline.json / _live.json —— 书级归并重扫对账（baseline 68 本 / live 70 本）。
- data/audit/phase21w8_stage2_batch1_submission.json —— 素材包提交回执（主提交 ce1dc46b；核验 16 PASS；成品 sha16 存档）。
- data/audit/source_texts_w8_stage2_batch1.json —— 批1 独立缓存索引（17 条目；零主库写）。
- data/audit/phase21w8_stage2_batch1_verify.log —— 落地核验日志（工作仓在盘；gitignore 命中 .log 规则、不入库不镜像；登记为 ws-only 观测件）。

#### 4.4.3 工具面（12 件：9 新增 + 3 修订）

- 新增（9 件）：tools/fetch_batch1_texts.py（抓取；links / allpages / list 三模式 + raw / render 双通道 + zh-cn 副本）；tools/build_batch1_sourcing_pack.py（逐条对照 quote / variant / null / cross-lang 四档）；tools/build_batch1_sourcing_report.py（报告装配）；tools/verify_batch1_sourcing_delivery.py（16 项独立核验）；tools/clean_batch1_cache_chrome.py（Chrome 缓存清理）；tools/apply_w8_stage2_batch1_landing.py（落地主体；幂等 + --preserve-stamps）；tools/build_batch1_landing_ledger.py（账本生成 + 键归一）；tools/verify_batch1_landing.py（20 项独立核验）；tools/verify_batch1_qa_espinosa.py（QA 双锚点校验器；27 断言）。
- 修订（3 件）：tools/build_source_links.py（--bookcount-report / --modes-spec）；tools/source_link_index.py（extract_refs_raw 保序不去重）；tools/fetch_source_texts.py（variant 参数；后继 W5 卡 3238a262 复改，链关键件 sha16 以 W5 后链现值为准，见 5.1 节）。
- 清单：tools/manifests/w8_stage2_batch1_texts.json（17 抓取项；其中现代诗项不抓取）。

#### 4.4.4 缓存面（20 件 txt）

- 缓存 txt（实测，ce1dc46b 新增）：20 件 = 16 部书底本 + 4 份 zh-cn 转换副本；位于 data/audit/source_texts/（sha 名 + .zh-cn 后缀）。
- 口径注记（据实登记）：023a794 提交信息称批1 缓存 23 txt，文件面实测为 20 件（差异为计数笔误，非内容差）；以实测为准。
- 与索引映射：17 索引条目 -> 16 唯一文本文件（二程遗书与河南程氏遗书共源 1 件）+ 4 zh-cn 副本；现代诗为否定记录、无文件。

#### 4.4.5 主库数据面（7 件）

| 件 | 变化（before -> after，落地面） | 说明 |
| --- | --- | --- |
| data/source_links.json | 383 -> 391 key | 8 部中文书（lang=lzh）入库；跨语言 9 部零链接 |
| data/audit/source_texts.json | 97 -> 114 条 | 批1 索引 17 条原样并入（sha256 / file 未改） |
| data/modes_data.json | 四态重跑 | pending->verified 69 / pending->suspect 3；全库 verified 949->1018 |
| data/audit/findings.json | 165 -> 168 条 | D4_quote_mismatch 24->27（M-WB-003 / M-WB-004 / M-WB-008） |
| data/audit/verification_status.json | 重跑 + 印记回填 | --check 零漂移；R9 20 条自定义块回填保护 |
| web/src/generated/siteCounts.ts | 计数同步 | 已核验 949->1018；可点引用 1230->1304 |
| docs/architecture/static_data_manifest.json | 重建 | 制品 sha / 计数（发布口径 1018 / 1845 / 38 / 340） |

#### 4.4.6 逐条处置摘要（154 条 · 引用落地报告与账本）

| 处置类别 | 条数 |
| --- | --- |
| 核中·逐字（不改字） | 3 |
| 核中·繁简对读（不改字） | 18 |
| 核中·节引 / 标点差（不改字） | 4 |
| 查无·待核（近似档） | 26 |
| 查无·待核（无近似命中） | 13 |
| 查无·源外（王弼他著，非本底本） | 4 |
| 查无·源外（对策类，源在漢書卷056） | 4 |
| 否定记录·无合法全文源（未抓，不伪造） | 8 |
| 跨语言·语义对照（待裁定） | 74 |
| 合计 | 154 |

- 翻面（本卡核验 D 段实测复算）：pending->verified 69 / pending->suspect 3 / 其他 0；包外零翻面。
- findings 增量：165 -> 168（+3 = M-WB-003 / M-WB-004 / M-WB-008；D4_quote_mismatch 增量 3 条）。
- 门禁四连（落地时复跑）：credibility_gate rc0（存量 524 / 新增 0 / 警告 28）；verify_findings rc0（新增 0）；apply_verification_status --check rc0（零漂移）；verify_source_links rc0（146 OK / 0 dead / 32 不可达 / 213 不可复核）。
- 四态（全库 3311）：949 / 1959 / 52 / 351 -> 1018 / 1887 / 55 / 351；发布口径 3251：949 / 1927 / 35 / 340 -> 1018 / 1855 / 38 / 340。
- D4 面（口径注记）：门禁现算 3331 口径 = 可核 key 55（+16）/ matched 11（+7）/ mismatch 27（+3）/ quote-too-short 117 / unchecked 3176；3311 口径独立重算 = 可核 39->55 / matched 4->11 / mismatch 24->27（QA 复核口径）。
- 站链：export 1357 件（figures 1027 / modes 3301 / published 3241 / by-figure 320）-> daily 3241 -> preflight(data) 过 -> unified 1344 -> gen_counts -> npm build 过 -> apply_site_counts（dist 1378 件 / 违规 0）-> preflight(dist) 过。

### 4.5 QA 回执登记（t_e727be57；引用 QA 报告第 1 至 6 节）

- 判定：PASS（核验矩阵 17 项复核后全 PASS；校验器 --at b5967043 = 27/27 全 PASS；复核前态 --at eda40f5b = 17 PASS / 6 FAIL，六项缺陷断言可复现）。
- 闭合修正（3 项账本 + 1 项工具根因）：
  - QA-C0：four_state.before 修正（原 932 / 1828 / 51 取自 09-22 陈旧状态文件、modes 3162 口径）-> 备份态实测 949 / 1959 / 52 / 351（发布 949 / 1927 / 35 / 340）；inputs sha16 同步修正。
  - QA-C1：书级列 link/cache 键归一（link_in_source_links 由全 False 修实 8 True；link_url 由全 null 修实 8 URL；cache_merged_into_source_texts 由全 False 修实 17 True；cache_sha256_matches 修实 17 条，原全 None 系键格式缺陷）。
  - QA-C2：cross_checks.links_added 由空对象修实 8 键映射。
  - 工具根因：build_batch1_landing_ledger.py 增键归一（_pick / _bracket_variants）；重生成不复现。
  - 跨引刷新：落地报告附录 B / 证据 outputs 跨引（账本 4dc2d8e3 / 报告 0eb4c12b 面刷新至终版）。
- 未闭合项（照登，见第七节）：QA-F1（素材包端 matcher 省略号分段 early-return；M-GX-007 / M-WB-010 / M-ZDY-005 首段核中·尾段未命中；预计核中 25->22）；QA-F2（标点归一集缺 U+FE30；M-ZXC-008 误判查无·待核；预计 null 55->54 / variant 22->23）；QA-F4（口径差：素材包报告 2.1 节见证位 21/25）。
- 复核指纹（修正后 -> 修正前）：账本 84ff028da6bee8d4（66c193dfbab851a8）；落地报告 886a7c90c560e727（e07b602a94339d9d）；落地证据 0a6f5a5ae266281b（8bf2aec01c54af36）；账本工具 81d6329c92afe97c（a76908ddd0e32778）；QA 校验器 4d55095b5776a82f（QA 卡 t_e727be57 新增）。

### 4.6 本卡动作与镜像集

- 本档四件：docs/research/phase21w8_stage2_batch1_archive_report.md（本报告）/ build_w8_stage2_batch1_archive.py（生成器；ws-only）/ verify_w8_stage2_batch1_archive.py（第二实现）/ docs/research/phase21w8_stage2_batch1_archive_evidence.json（证据）。
- 镜像集（发布仓）：报告 + 验收脚本 + 证据 = 3 件（byte-exact + push）；生成器同先例仅工作仓面。
- 站点展示层：本链为数据与文档面（无新增页面 / 路由 / 文案）；两仓一致性以镜像 byte-exact 复核替代（第六.3 节）。
- 链件镜像总表：见 5.1 节（26 件链件 + 本档件双仓 sha16 对照）。

### 4.7 提交/镜像/push 回执（本卡；回执区）

- stage：v2（回执终版；v1 实测值已回填；v2 全号以卡面完成 metadata 为准）
- ws_commit_v1：`fbc061f9e664b803f9dd49ca5111217ebb45e86b`（报告 v1 + 生成器 + 验收脚本 + 证据 v1；4 件白名单提交）
- pb_commit_v1：`1ec471a006ecf274cb4d5349f908dae3e60e479f`（镜像 3 件：报告 v1 + 验收脚本 + 证据 v1；byte-exact）
- push_v1：ok（cacd6f0..1ec471a）
- ws_commit_v2：回执终版提交（报告 v2 + 生成器回填；全号随卡面完成 metadata）
- pb_commit_v2：回执终版镜像（报告 v2；全号随卡面完成 metadata）
- push_v2：ok（推送后 ls-remote 与发布仓 HEAD 一致；随卡面完成 metadata）
- 终态回执（v2 提交与镜像 sha、ls-remote、校验器终跑）：以卡面完成 metadata 为准（先例体例）。

## 五、证据

### 5.1 链关键件 sha256（前 16 位；双仓对照，生成时点）

| 文件 | 工作仓 sha16 | 发布仓 sha16 | 判定 |
| --- | --- | --- | --- |
| docs/research/phase21w8_stage2_batch1_booklist.md | `ef6849dbb658a22a` | `ef6849dbb658a22a` | 等于（byte-exact） |
| docs/research/phase21w8_stage2_batch1_booklist.json | `ca46eb42471c35fc` | `ca46eb42471c35fc` | 等于（byte-exact） |
| docs/research/phase21w8_stage2_batch1_sourcing_report.md | `e2445bb03922f280` | `e2445bb03922f280` | 等于（byte-exact） |
| docs/research/phase21w8_stage2_batch1_sourcing_report.json | `a64351a47116dede` | `a64351a47116dede` | 等于（byte-exact） |
| docs/research/phase21w8_stage2_batch1_landing_report.md | `886a7c90c560e727` | `886a7c90c560e727` | 等于（byte-exact） |
| docs/research/phase21w8_stage2_batch1_landing_evidence.json | `0a6f5a5ae266281b` | `0a6f5a5ae266281b` | 等于（byte-exact） |
| docs/research/phase21w8_stage2_batch1_qa_report_espinosa.md | `9f52d3fcb159bf0b` | `9f52d3fcb159bf0b` | 等于（byte-exact） |
| docs/research/phase21w8_stage2_batch1_qa_evidence_espinosa.json | `3905b854769edcdc` | `3905b854769edcdc` | 等于（byte-exact） |
| data/audit/phase21w8_stage2_batch1_landing_ledger.json | `84ff028da6bee8d4` | `84ff028da6bee8d4` | 等于（byte-exact） |
| data/audit/phase21w8_stage2_batch1_recount_baseline.json | `1cc8ff3bee740153` | `1cc8ff3bee740153` | 等于（byte-exact） |
| data/audit/phase21w8_stage2_batch1_recount_live.json | `6ddffad6c8631ad4` | `6ddffad6c8631ad4` | 等于（byte-exact） |
| data/audit/phase21w8_stage2_batch1_submission.json | `de1bed5062cb66ea` | `de1bed5062cb66ea` | 等于（byte-exact） |
| data/audit/source_texts_w8_stage2_batch1.json | `24464156391bf86b` | `24464156391bf86b` | 等于（byte-exact） |
| tools/fetch_batch1_texts.py | `e072f4d645402b3c` | `e072f4d645402b3c` | 等于（byte-exact） |
| tools/build_batch1_sourcing_pack.py | `f35c19da3f64e5c8` | `f35c19da3f64e5c8` | 等于（byte-exact） |
| tools/build_batch1_sourcing_report.py | `910f1a5f7a0b186d` | `910f1a5f7a0b186d` | 等于（byte-exact） |
| tools/verify_batch1_sourcing_delivery.py | `b94cc3a41ae53309` | `b94cc3a41ae53309` | 等于（byte-exact） |
| tools/clean_batch1_cache_chrome.py | `14b74db3074f0922` | `14b74db3074f0922` | 等于（byte-exact） |
| tools/apply_w8_stage2_batch1_landing.py | `c76f048f6d4ce0e6` | `c76f048f6d4ce0e6` | 等于（byte-exact） |
| tools/build_batch1_landing_ledger.py | `81d6329c92afe97c` | `81d6329c92afe97c` | 等于（byte-exact） |
| tools/verify_batch1_landing.py | `eb775ba5a06e2130` | `eb775ba5a06e2130` | 等于（byte-exact） |
| tools/verify_batch1_qa_espinosa.py | `4d55095b5776a82f` | `4d55095b5776a82f` | 等于（byte-exact） |
| tools/manifests/w8_stage2_batch1_texts.json | `9f5823e5897630f5` | `9f5823e5897630f5` | 等于（byte-exact） |
| tools/build_source_links.py | `0b363e04bc6e00e7` | `0b363e04bc6e00e7` | 等于（byte-exact） |
| tools/source_link_index.py | `b2c6074a61f753ff` | `b2c6074a61f753ff` | 等于（byte-exact） |
| tools/fetch_source_texts.py | `6b534db72ee00148` | `6b534db72ee00148` | 等于（byte-exact） |

- 26 件含修订件 3（build_source_links / source_link_index / fetch_source_texts；后者现值为 W5 后链面）。

### 5.2 本档件（生成时点；镜像状态见第四.7 节）

- 报告（本件）：docs/research/phase21w8_stage2_batch1_archive_report.md —— 本文件（sha16 随回执回填演进；镜像状态见 4.7 节）。
- 生成器：build_w8_stage2_batch1_archive.py —— ws-only 面（sha16 `d8083561d3aeb68e`，生成时点；--check 归一本行）。
- 验收脚本：verify_w8_stage2_batch1_archive.py —— 随镜像（sha16 `031a98a12606512a`，生成时点；--check 归一本行）。
- 证据：docs/research/phase21w8_stage2_batch1_archive_evidence.json —— 随镜像刷新（sha16 `15a7d775c92ef98e`，生成时点；由验收脚本生成）。

### 5.3 备份 MANIFEST 复核（data/backup_merge_W8B1_20260924_113742）

- 5/5 逐件 sha256 复核 PASS（before 面登记）：
  - `data/audit/findings.json` = `b73e32806f7c910b`
  - `data/audit/source_texts.json` = `c4aba5ff870f375e`
  - `data/audit/verification_status.json` = `32661224820d4230`
  - `data/modes_data.json` = `6f3f4580397614f5`
  - `data/source_links.json` = `9df3d1fd210b2926`
- 备份目录不入库、parity 排除（先例）。

### 5.4 数据面三段 pin（before / after / 现值）

| 件 | before（004332b4^） | after（eda40f5b） | 现值（生成时点观测） | 注 |
| --- | --- | --- | --- | --- |
| data/modes_data.json | `6f3f4580397614f5` | `75932c9f2d48d136` | `736aab3b4164973d` | （W5 后链演进） |
| data/source_links.json | `9df3d1fd210b2926` | `dc0aebf0c2bbdadc` | `dc0aebf0c2bbdadc` | — |
| data/audit/source_texts.json | `c4aba5ff870f375e` | `daf6d882907126a5` | `87f4f9cc7c70528d` | （W5 后链演进） |
| data/audit/findings.json | `b73e32806f7c910b` | `0292f0580ab03293` | `552760746a125c1a` | （W5 后链演进） |
| data/audit/verification_status.json | `32661224820d4230` | `22944f54fb5e51a2` | `22944f54fb5e51a2` | — |
| web/src/generated/siteCounts.ts | `4e8e99110830a807` | `a698abe698bb3db3` | `a698abe698bb3db3` | — |
| docs/architecture/static_data_manifest.json | `9bf53ce4bd168421` | `abf786227c7757c6` | `abf786227c7757c6` | — |

### 5.5 git 对账与 parity（生成时点观测；--check 归一本节）

- 工作仓 HEAD（生成时点）：`fbc061f9e664b803f9dd49ca5111217ebb45e86b`（master；本地提交面）。
- 发布仓 HEAD（生成时点）：`1ec471a006ecf274cb4d5349f908dae3e60e479f`（origin/main 面）。
- ls-remote（生成时点）：`1ec471a006ecf274cb4d5349f908dae3e60e479f` 为复核时点值。
- parity（生成时点）：status=OK；both_sides=2587；identical=2587；only_workspace=0；only_publish=0 计数。
- 口径：tools/check_repo_parity.py --json（构建图边界口径；计数见上一行生成时点观测）。

### 5.6 发布面线上抽验（时点值）

- 检查时点：2026-09-24 13:02 至 13:06 CST（本卡实测）。
- 首页 https://ovmobilegroup.github.io/protreptic/ ：HTTP 200。
- 可信度统计页 /credibility/ ：HTTP 200；显示已核验 1019 / 待核验 1845 / 存疑 37 / 一手材料 340（站点口径 3241 条；等于 W8 落面 1018 / 1845 / 38 / 340 叠加 W5 后链 +1 与 -1 两处）。
- 数据制品抽验 2 件：data/figures.index.json（208,714 B；sha256 `65a7cdc65ed930f3077a1ed1b9eabc6e599345388a62a70d4a422ad82ef0c38e` 值）与 data/modes/index-0.json（111,528 B；sha256 `3e94d62c5253dcc5098e46ecdfdb9c30c71a2c5cd7b0ebd2f46a81a990a874ea` 值），与落地面 static_data_manifest.json 记录逐字节相等。
- data/meta.json：HTTP 200（3566 B；verified=1019 值）由发布仓 CI 重建，为检查时刻值。
- 说明：线上数据由发布仓 CI 重建（时点=检查时刻）；W8 链落地面以提交树为准，W5 后链演进已上线。

## 六、核验

### 6.1 上游 QA 判定（t_e727be57；引用）

- 结论 PASS；核验矩阵 17 项复核后全 PASS（素材包逐条 154/154 逐字一致；生成器重跑 0 diff；四态 1018-1887-55-351 与发布口径；翻面 72 条全在包内；审计增量 +3；缓存 +17 同源；链接 +8 边界；站面计数；D4 普查增量 +16/+7/+3；门禁复跑全绿；镜像 blob 逐件；push ls-remote；账本修正断言；跨引一致；书级列键归一；W8-2 回执 sha 澄清；边界抽查）。
- 复核方法：备份态全量重算；W8 数据锚点 eda40f5b；素材包生成器按算法重跑对照；四门禁独立 worktree 复跑；镜像按提交级 blob 对照；push 面看发布仓 HEAD 与 ls-remote 一致。
- 复核前态自证：--at eda40f5b = 17 PASS / 6 FAIL（恰为六项缺陷断言）；复核后 27 项全 PASS 收口。

### 6.2 本卡独立验收（第二实现）

- 脚本：verify_w8_stage2_batch1_archive.py（根级；不 import 生成器；段目 A 至 F 全段）。
- 结果：v2 镜像后终跑 ALL PASS 0 FAIL + 6/6 反向注入自检（v1 轮为 --receipts-pending 过渡面）；明细见证据 JSON 与卡面完成 metadata 值。
- 取证摘要：C 段 8 笔 ws 提交 + 4 笔 pb 提交逐条 git 实测（短号 / 全号 / 前缀一致）；D 段 26 件 sha16 登记复核 + 7 件三段 pin + 备份 5/5 + 缓存 txt 计数 20 + 四态与翻面独立重算（before/after git 对象解析）。

### 6.3 发布面复核（本卡）

- 双仓 byte-exact：链件 26 件 + 本档件（报告 / 验收脚本 / 证据）。
- 提交级 blob 对照：pb 四笔镜像提交（50 / 2 / 7 / 6 件）逐件对齐工作仓对应提交（004332b4 / eda40f5b / b5967043 / b0e2b0a8 等四笔），blob 相等。
- push 面：发布仓 HEAD 与 ls-remote main 一致（复核时点见 5.5 节）。
- 线上抽验：见 5.6 节（首页 / 可信度页 / 数据制品 2 件 / meta.json）。

## 七、残留与账务登记

- R1 跨语言 74 条口径待船长裁定（冻结态：不建链接 / 不改状态 / 留语义对照档）。
- R2 庄子注 6 条查无受四庫异体字 / SKchar 限制（改写档另行待核；素材包残留条）。
- R3 太极图说 index-page 误标（MIN_CHARS 阈值；本链未动工具阈值，越界回避）；如需 D4 可核另立小卡。
- R4 源外 8 条可另抓底本（《老子指略》/《周易略例》4 条 + 《举贤良对策》4 条）。
- R5 M-WB-004 繁简守卫配对阈值偏保守（去冠名后应可判 matched；登记为待复核，不改现状）。
- R6 apply_verification_status 块覆盖行为：建议另卡增「含自定义 method 的条目跳过重写」选项（落地报告 6 节；本卡不实施）。
- R7 QA-F1（素材包端）：matcher 省略号分段 early-return；M-GX-007 / M-WB-010 / M-ZDY-005 首段核中、尾段未命中；建议另卡修正 + 素材包重算（预计核中 25->22）。
- R8 QA-F2（素材包端）：标点归一集缺 U+FE30；M-ZXC-008 误判查无·待核；建议同卡一并修正（预计 null 55->54 / variant 22->23）。
- R9 QA-F4（口径差，表述面）：素材包报告 2.1 节「见证位逐条随行」实为 21/25（4 条节引型显式 null）；表述收紧即可。
- R10 verify.log（data/audit/phase21w8_stage2_batch1_verify.log）：gitignore 命中 .log，ws-only 观测件；不镜像、不阻断。
- R11 提交信息口径注记：023a794 称「批1 缓存 23 txt」与实际 20 件之差（本档 4.4.4 已登记）；非内容差。
- R12 W8 后链演进登记（不计入 W8 结论）：W5 数据侧修复 t_0dc95522（verified 1018->1019 / suspect 55->54；现值 pin 见 5.4 节）；W7 / W9 / W11 链各自推进。
- R13 parity 余项：本卡生成时点 diff 为 0（W10 两文档债务已由船长收口：工作仓 b8be2986 / 发布仓 20d36f0）。

## 八、下一步

- W8 链无卡内遗留动作（本卡为链尾归档）。
- 建议另卡（待船长裁定）：QA-F1 / F2 素材包端 matcher 修正 + 素材包重算（表述口径同步收紧）。
- 待裁定口径：跨语言 74 条（R1）。
- 后续链（各自推进）：W5 复验 t_30d57ff2 与文书侧 t_bda44643；W7 清档合批（t_d24e11bc / t_06511a5a / t_95764335）；W9 F 类回填（t_0b240eb7 / t_9ed2866a / t_9cb09b90）；W11 CI（t_0ec6fb57）。
- 批2 及后续批次：按设计文档第 6 节分批交付口径续跑（书单批次以重扫 live 集为准）。

## 九、附链（全号索引与复跑）

### 9.1 提交全号索引

- 工作仓（W8 链 8 笔）：
  - 20b13092  20b13092038ae16d0290b0434b7026f1c820e9d6  09-24 09:19
  - ce1dc46b  ce1dc46b15da56b6d570ff341e3d9b0a40e279e0  09-24 11:15
  - 60d5d509  60d5d5090fd1d0e1f587dced4dac2c72bd14bf23  09-24 11:16
  - 58f34f88  58f34f88ab58bbd2bdb75b6055761e72f23758ca  09-24 11:17
  - 004332b4  004332b43637c45447938f7b5b550fa6ce0ff8af  09-24 11:54
  - eda40f5b  eda40f5ba3c8395c6655501c153f6a69ce81651d  09-24 11:58
  - b5967043  b5967043d9c3b57d15d0894dad52f1e176f9b4ba  09-24 12:55
  - b0e2b0a8  b0e2b0a84d53c7028908885b104f6745245b3a62  09-24 12:59
- 发布仓（W8 链 4 笔）：
  - 023a794  023a79488b94c779d44e882590384cddbabfc792  09-24 11:56
  - c522897  c52289770a544064a36d3346f674f164cb2af4ef  09-24 11:58
  - 88cc86a  88cc86a7ef56917216cb52972daad50114e738f2  09-24 12:55
  - 384faae  384faaea68efa32df41a9f412e24173a7010c637  09-24 12:59
- 锚点：
  - ws 004332b4  004332b43637c45447938f7b5b550fa6ce0ff8af（落地主提交；before 锚点 = 004332b4^）
  - ws eda40f5b  eda40f5ba3c8395c6655501c153f6a69ce81651d（回执补记；W8 数据锚点）
  - ws b5967043  b5967043d9c3b57d15d0894dad52f1e176f9b4ba（QA 提交 A）
  - ws b0e2b0a8  b0e2b0a84d53c7028908885b104f6745245b3a62（QA 提交 B）
  - pb 023a794  023a79488b94c779d44e882590384cddbabfc792（50 件镜像）
  - pb 384faae  384faaea68efa32df41a9f412e24173a7010c637（QA 回执镜像；复核时点 origin/main）

### 9.2 文档与证据路径

- 本档：docs/research/phase21w8_stage2_batch1_archive_report.md / _archive_evidence.json；脚本 build_w8_stage2_batch1_archive.py / verify_w8_stage2_batch1_archive.py（根级）。
- 链上：booklist / sourcing_report / landing_report + evidence / landing_ledger / qa_report + evidence（完整清单见 4.4 节）。

### 9.3 复跑命令

- 幂等校验：python3 build_w8_stage2_batch1_archive.py --check
- 独立验收：python3 verify_w8_stage2_batch1_archive.py（证据默认写 docs/research/phase21w8_stage2_batch1_archive_evidence.json）
- 发布面线上抽验（可选）：python3 verify_w8_stage2_batch1_archive.py --with-live
- parity：python3 tools/check_repo_parity.py --json

### 9.4 台账登记

- /opt/data/cache/protreptic_work_backlog.md（append-only；本卡登记行随完成提交）。
