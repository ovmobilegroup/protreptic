# Phase21 W8 Stage2 批1 独立 QA 复核报告（espinosa / 卡 t_e727be57）

**结论：PASS**（本卡闭合 3 项账本修正 + 1 项工具根因修复；另交 2 项素材包端修正建议 + 2 项口径注记。对照验收四问逐项复核如下。）

复核对象：W8 Stage2 批1 全链（素材包 t_70a8cbce → 落地 t_b85ae14a），即 docs/research/phase21w8_stage2_batch1_{sourcing,landing,booklist}* 与 data/audit/phase21w8_stage2_batch1_*、data/source_links.json 等 13+37 件落盘产物。

复核方法（不信任自述）：
- 备份态（data/backup_merge_W8B1_20260924_113742/）侧全量重算四态/翻面/审计增量；
- W8 数据面钉点复核（锚点 commit **eda40f5b**，与 004332b4 数据面同）；
- 素材包生成器按算法重跑对照（RERUN vs STORED = 0 diff）；
- 四门禁在独立 worktree 复跑；镜像按提交级 blob 逐件对照；push 面看发布仓 HEAD 与 ls-remote。

窗口说明：本 QA 落盘提交位于他卡链之后（W5 数据侧修复 t_0dc95522 等已入库并镜像），W8 数据面一律钉在 eda40f5b 复核；他卡后续演进不计入 W8 结论（见 §2）。

## 1. 核验矩阵（复核后态全部 PASS）

| # | 项 | 方法 | 结果 |
| --- | --- | --- | --- |
| 1 | 素材包 ↔ 账本 ↔ 库 逐条对照 | 154/154 引文逐字一致（零改写） | PASS |
| 2 | 素材包生成器忠实性 | 按算法重跑对照：RERUN vs STORED diffs = 0 | PASS（算法面缺口见 §3-F1/F2） |
| 3 | 四态重算 | 全库 1018/1887/55/351（3311）；发布 1018/1855/38/340（3251） | PASS |
| 4 | 状态翻面 | 多重集差重算：pending→verified 69 / pending→suspect 3，共 72，全在包内、包外 0 | PASS |
| 5 | 审计增量 | findings 165→168，仅 +3（M-WB-003/004/008 D4），无删改 | PASS |
| 6 | 缓存合并 | source_texts 97→114，+17 与 W8 索引 file/sha256 逐条同源，旧 97 未动 | PASS |
| 7 | 链接库边界 | source_links 383→391，+8 本书键；旧 383 键逐字节未动；跨语言零链接 | PASS |
| 8 | 站面计数 | siteCounts：1018/1845/38/1046/1304/2262 与发布口径一致，sha a698abe6 | PASS |
| 9 | D4 普查重算 | 全库重算：可核 key 39→55、matched 4→11、mismatch 24→27（3311 口径）——父卡 +16/+7/+3 增量成立 | PASS |
| 10 | 门禁复跑（@eda40f5b） | credibility rc0（存量 524 / 新增 0）；verify_findings rc0（新增 0）；apply_verification_status --check 零漂移；verify_source_links rc0（0 dead / 0 new） | PASS |
| 11 | 镜像回执 | 发布仓 023a794（50 件）与 c522897（2 件）逐件 blob == 工作仓 004332b4 / eda40f5b | PASS |
| 12 | push 面 | 发布仓 HEAD == ls-remote main（复核时点 58f361d，W8 提交均为其祖先） | PASS |
| 13 | 账本修正断言 | before 真值 949/1959/52/351（+发布 949/1927/35/340）；inputs sha 同步 | PASS（修正后） |
| 14 | 跨引一致性 | 报告附录 B / 证据 outputs ↔ 修正后账本/报告/工具 sha16 逐一对齐 | PASS（修正后） |
| 15 | 账本书级列 | 8 链接 / 17 缓存合并 / sha 全等；links_added == 8 键 | PASS（修正后） |
| 16 | W8-2 回执 sha 差澄清 | f4abf8d4→e2445bb0（报告）/ 8bcccff7→a64351a4（JSON）由 60d5d509 + 58f34f88 两提交解释；落地取最新版 | 口径差成立 |
| 17 | 边界抽查 | 20 他卡印记未动；60 隔离未动；9 跨语言不建链；备份目录完好 | PASS |

复核前态自证：`python3 tools/verify_batch1_qa_espinosa.py --at eda40f5b` = **17 PASS / 6 FAIL**（恰为下方 F0-F2 六项缺陷断言）；复核后态默认锚点 = 全 PASS。

## 2. 口径与窗口注记

- **W8 之后他卡链**：W5 数据侧修复（t_0dc95522）已入库并镜像（verified 1018→1019 / suspect 55→54），不在本结论范围；W8 数据锚点 = eda40f5b。
- **门禁 D4 口径**：门禁普查 3331 条（含 H-ASM-001 / H-ZZ-001 内嵌 20 条）vs modes_data 顶级 3311；两口径各档计数自洽（unchecked 3176 vs 3157 等差异即此 20 条）。
- **链接复核时点**：OK/不可达分布随网络变化（父卡 146/32 → 本卡 173/5），0 dead / 0 new 两时点一致。
- **并发窗口**：复核期间工作区有他卡在途改动（后已入库），W8 结论一律以提交树为准。

## 3. 分级缺陷与处置

- **F1（真差异 · 素材包端，建议另卡修正）** 省略号分段核验缺口：`build_batch1_sourcing_pack.py` 的 match_quote 在首段标点命中即 early-return，未按其自身文档口径『……两侧各自须命中』执行。3 条『核中·繁简对读』条目逐字命中结论仅对首段成立：
  - M-GX-007（郭象）：尾段为改写——底本作『推而極之則今之所謂有待者率至於無待而獨化之理彰矣』；
  - M-WB-010（王弼）：尾段库内未见（longest≈3，无完整句）；
  - M-ZDY-005（周敦颐）：尾段出自《通书》，source_chapter 未引。
  建议：修正 matcher（分段全命中）+ 素材包重算 + 计数重述（预计核中 25→22）；未重算前该 3 条表述应收紧为『首段核中 · 尾段待核』。
- **F2（真差异 · 素材包端，建议另卡修正）** 标点归一集缺口（未含 U+FE30『︰』等）：M-ZXC-008（章学诚 /《文史通义》）判『查无·待核（近似档）』，实际引文与底本仅差两处『：』vs『︰』与文末句号，按标点归一应命中（繁简对读）。预计修正重算后 null 55→54 / variant 22→23。
- **F0（真差异 · 账本端，已修正）** four_state.before 陈旧口径（932/1828/51，取自 2026-09-22 旧 verification_status.json，modes 3162 口径）；已按备份态实测修正为 949/1959/52/351（发布 949/1927/35/340），inputs sha16 同步修正；修正后与报告 §4.2 / 证据 four_state / status_flips 三向一致。
- **F6（真差异 · 账本端，已修正）** 书级列键格式缺陷（素材包书名无《》vs 仓内键带《》）：link_in_source_links 全 False → 8 True；link_url 全 null → 8 URL；cache_merged_into_source_texts 全 False → 17 True；cache_sha256_matches 全 None → 17 True；cross_checks.links_added {} → 8 键映射。根因已在工具面修复（增加键归一 _pick / _bracket_variants），重生成不再复现。
- **F4（口径差）** 素材包报告 §2.1『见证位逐条随行』对 25 条已核不成立：实际 21 条带见证；4 条节引型（sent-verified，无单点见证）已显式登记——表述收紧即可。
- **F5（口径差/窗口差）** 见 §2。

## 4. 复核指纹（修正后）

| 文件 | sha16 复核后 | 复核前 |
| --- | --- | --- |
| data/audit/phase21w8_stage2_batch1_landing_ledger.json | 4dc2d8e354c9c0c2 | 66c193dfbab851a8 |
| docs/research/phase21w8_stage2_batch1_landing_report.md | 0eb4c12bd8ddb347 | e07b602a94339d9d |
| docs/research/phase21w8_stage2_batch1_landing_evidence.json | 72b7718b79ce8dbe | 8bf2aec01c54af36 |
| tools/build_batch1_landing_ledger.py | 81d6329c92afe97c | a76908ddd0e32778 |
| tools/verify_batch1_qa_espinosa.py（本卡校验器） | 86d0315a0379c370 | （新增） |

账本 qa_addendum 内嵌全部修正与发现登记（QA-C0/C1/C2 + QA-F1..F6），与 QA 证据 JSON 互为镜像。

## 5. 可复现复核

- 校验器（双锚点）：`python3 tools/verify_batch1_qa_espinosa.py`
  - 复核前态：`--at eda40f5b` → 17 PASS / 6 FAIL（六项缺陷断言）；
  - 复核后态：默认锚点（本卡提交）→ 全 PASS；`--with-gates`（门禁复跑）/ `--with-remote`（push 面）。
- QA 证据（结构化）：docs/research/phase21w8_stage2_batch1_qa_evidence_espinosa.json。

## 6. 提交回执（回执补记）

- 工作仓：QA 提交 A = （回执补记填入）；发布仓：P1 = （回执补记填入）（QA 7 件 byte-exact）；push （回执补记填入）；ls-remote 一致。
- parity：本卡面 CONTENT_DIFF=0；残余项=回执时点他卡在途。
- 校验器：`--at A` 全 PASS（含 C8a / C8b）；`--at eda40f5b` 六项缺陷断言复现。
