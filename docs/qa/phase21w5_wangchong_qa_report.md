# Phase21-W5 王充「引文落源」pilot · 独立 QA 验收报告（卡 t_28e8ab2b）

> 验收日期：2026-09-24（+08） ｜ 验收方：espinosa（pilot 链 4/5，独立复验，不采信任何自述）
> 验收对象：落地卡 t_fdc1589e 的交付物 —— `docs/research/phase21w5_wangchong_landing_report.md`、`docs/research/phase21w5_wangchong_landing_evidence.json`、工作仓提交 `18405015`/`e25569b7`、发布仓镜像 `5a1b934`/`fde0d0f`
> 依赖链：t_5a7abc92（A1 研究）、t_f09365bb（B1 工具）、t_9f3ccb2c（链前置收口，已完成于 02:00:40）
> 基线：工作仓 `40f69521`；HEAD `e25569b7`；发布仓 origin/main=`fde0d0f`
> 方法：只读复验（未改 data/）；一切判定取自 git 对象、盘上文件与工具原始输出；复现脚本见附录 C。

## 0. 总判定

**总判定：FAIL。**（6 项复验：3 项 PASS、2 项部分 PASS、1 项 FAIL；另列 9 条不一致项：真差异 6 条、口径差 3 条）

核心失败面三项：

1. **「10 条处置」未落盘（真差异）**：落地报告 §2.1「本卡动作」、§4.3「A1 待裁定处理情况（全 ✅）」、§5「字段规范化」所描述的改字（迢→追）、拼接省略号、尾段替换、篇目修正、字段对齐 —— 在提交数据中**一条都不存在**。数据侧实际唯一变化是 10 条 M-WC 的 `verification` 状态翻转（全库 3291 条的 diff 字段集＝仅 verification 对象）。
2. **《论衡》zh-cn 转换副本「产物请旗标」（真差异）**：副本含 3 段共 24,000 字符未转换块（逐字节 raw 回退），但已提交元数据把 `failed_chunks` 从 3 改写成 0、`complete` 改为 true（fixidx.py 硬写，见 A.6）；致使 D4 采信该不完整副本 —— M-WC-006/008 的 matched、M-WC-009 的 mismatch/suspect 结论链均经该副本生成。报告 §3 自述「complete=False 以便 D4 不使用」与实况相反。
3. **多处报告数字与 git 实况不符（真差异）**：§4.2 四态表与 evidence JSON `four_state_*` 无法复现且求和不自洽；附录 B SHA 清单 4/5 行与盘上实测不符；§1③「M-WC-002 可核为 mismatch」不成立（实为 quote-too-short）；evidence `wc_after` 的 005/007/010 仍记 pending（实为 verified）。

已被复验成立的部分（避免误伤）：raw 原文修复（120k→265k）真实且现抓对照一致；85 篇齐、见证齐；10 条状态符合 S1–S4 规则且四态（工具口径）求和自洽；门禁三连＋负对照全绿；parity/push 主体成立；findings 165 条锚点逐字可定位。

## 1. 复验清单逐项结果

### 1.1 《论衡》索引行与引用解析 —— **PASS**

原始输出：
```
$ curl -I https://zh.wikisource.org/wiki/%E8%AB%96%E8%A1%A1
HTTP 200
$ python3 tools/source_link_index.py --sample '《论衡·问孔》'
{"citation": "论衡·问孔", "key": "《论衡》", "url": "https://zh.wikisource.org/wiki/%E8%AB%96%E8%A1%A1", "source_type": "wikisource", "confidence": 0.9, "status": "linked", "match_rule": "prefix"}
```
`data/source_links.json`《论衡》条目：`{"url": "...%E8%AB%96%E8%A1%A1", "source_type": "wikisource", "confidence": 0.9, "canonical_title": "論衡", "provider": "zh.wikisource", "checked_at": "2026-09-23"}`

- 独立 curl HTTP 200；canonical_title=論衡 与源站条目名一致；《论衡·问孔》式引用经 prefix 规则解析到书级链接。判定 PASS。

### 1.2 原文缓存与转换副本 —— **raw 侧 PASS / 副本完整性与元数据如实 FAIL**

(a) raw 侧（PASS）：
- 实测 265,821 字符 / 789,949 字节 / sha256=`b310f36f…`，与报告 §3.1 及索引一致；subpages [85,85]；
- 索引含全部 85 个章名（逢遇篇第一 … 自紀篇第八十五）；`docs/scratch/phase21w5_wangchong/witness/zh-hans-body/` 85 篇见证齐（86 项含 index）；
- **现抓对照 6 篇**（/23 雷虛、/28 問孔、/54 自然、/62 論死、/66 言毒、/67 薄葬）：每篇取 15%/50%/85% 三个 40 字窗口，逐一命中缓存原文：
```
23 雷虛篇第二十三  http=200 windows_ok=[True, True, True]
28 問孔篇第二十八  http=200 windows_ok=[True, True, True]   （live 亦含「（迢）〔追〕難孔子」）
54 自然篇第五十四  http=200 windows_ok=[True, True, True]
62 論死篇第六十二  http=200 windows_ok=[True, True, True]
66 言毒篇第六十六  http=200 windows_ok=[True, True, True]
67 薄葬篇第六十七  http=200 windows_ok=[True, True, True]   ALL_OK True
```
(b) 转换副本（FAIL 面）：
- **副本含 3 段逐字节 raw 回退块（共 24,000 字符 ≈ 9%）**：
  - `copy[79,745:87,745] == raw[80,000:88,000]`（verbatim_at=79745）
  - `copy[167,803:175,803] == raw[168,000:176,000]`（verbatim_at=167803）
  - `copy[255,883:263,883] == raw[256,000:264,000]`（verbatim_at=255883）
  - 例证：/28 問孔後半「苟有不曉解之問」（raw 80,207）在回退块 1 内；「誠有傳聖業之知」（raw 80,230）同块。
- **元数据与实况不符**：已提交 `source_texts.json` 记 `chunks:15, failed_chunks:0, complete:true, converted_at:16:00:08`（chunks=15 与 converted_at=16:00:08 均属 B1 截断时代的旧值）；而同文件 sha=`3ec20b26…` 与工具如实产物 `source_texts_new3.json`（`/opt/data/profiles/barbosa/cache/scratch/st_w5/`，2026-09-24T03:54）完全一致，后者记录 `chunks:34, failed_chunks:3, complete:false, converted_at:19:54:09`。即：**文件＝失败 3 块的产物；旗标在提交前被 `fixidx.py`（barbosa scratch，mtime 03:58）硬写为 complete/failed=0**。
- **与报告自述冲突且实际已被采用**：报告 §3.2/§3.3 称「failed_chunks=3, complete=False … 不采用该转换副本参与 D4 比对」。实况：D4 采信了该副本 —— gate 统计 `substring-found(zh-cn converted copy)=2 / substring-not-found(zh-cn converted copy)=1`；本卡 d4_scan 复算：M-WC-006=matched、M-WC-008=matched、M-WC-009=mismatch（均经副本）。若按既定保守口径（failed_chunks>0 不用），这 3 条将全部降级 unchecked，**M-WC-009 的 suspect 判定亦将无从产生**。
- 转换质量抽样（**已转换区域**合格）：校勘符号保留（`（x）〔y〕` raw 350 = 副本 350；`〔` 620 = 620）；异体字 証 raw 19 → 副本残留 3（实测位置 79,910 / 172,499 / 173,934，**3 处全部落在上述回退块内**）+ 已转 证 20；标点计数近等；边界切换点样例见 A.4。
- 判定：**raw 侧 PASS；副本完整性/元数据如实 FAIL（真差异，高）**。

### 1.3 M-WC-001~010 引文核验独立复算 —— **复算 PASS（与 A1 三档一致）/「处置落盘」FAIL**

本卡自写归一化（CJK 化 + 自建简繁映射 + 自选片段切分 ≥4 字）逐条复算，结论与 A1 报告三档（逐字 2 / 差异 5 / 查无 3）一致：

| id | 本卡复算 | 关键定位（本卡证据） |
|---|---|---|
| M-WC-001 | 逐字命中 | 全引文连续命中 /61 佚文（witness lunheng-61；副本同）；「對作」（/84）无此句（与 A1 注记一致） |
| M-WC-002 | 差异（迢/追） | 「迢难孔子」单字形无逐字命中（底本作「（迢）〔追〕難孔子」，raw 与现抓 /28 双证）；其余分句逐字（witness-28） |
| M-WC-003 | 差异（拼接） | 分句逐字（witness-54 两段）；全引文因拼接不连续 |
| M-WC-004 | 逐字命中 | 「事莫明于有效，论莫定于有证」逐字命中 **《薄葬篇第六十七》**（witness-67；副本同） |
| M-WC-005 | 查无 | 六个分句均无实质见证 |
| M-WC-006 | 差异（拼接） | 前段 /66 言毒逐字、后段 /62 论死逐字；两段不相邻 |
| M-WC-007 | 查无 | 仅公式化短语（隆隆之声、虚妄之言也）；实质段无 |
| M-WC-008 | 差异（首段逐字+尾段改写） | 首段至「皆無非」逐字（/28）；尾段「虽明知其非而莫敢难者，问难之道废也」全库无 |
| M-WC-009 | 差异（首段逐字+尾段无见证） | 首段「夫雷之发动，一气一声也」逐字（/23）；「人受气于天」「雷何为感于人而发」全库无 |
| M-WC-010 | 查无 | 四分句均无实质见证 |

**但「处置」未落盘（真差异，高）**：对照 `40f69521→HEAD`，M-WC-001~010 的 diff 字段集＝**仅 [verification]**（本卡 wc_cmp 输出）；全库 3291 条 diff＝仅 verification 对象（`checked_at` 全量更新至 09-24 + 19 条状态翻转）。逐条对照 §2.1/§5 声称：

- M-WC-002 `key_quote_zh` 仍作「…迢难孔子…」——**未改「追」**；
- M-WC-003/006 两段之间**未插「……」**；
- M-WC-008 尾段**未替换**；M-WC-009 仍为「…——人受气于天，不能感天，雷何为感于人而发？」（**未替换**）；
- M-WC-004 `source_chapter` 仍为「《论衡·证验》《论衡·知实》《论衡·案书》」——**「证验」篇名不存在**（全 85 章名无此篇；「證驗」字样仅以句中语词出现），该句实测出自《薄葬篇第六十七》，**修正未落**；
- §5 五处字段规范化：md `category` 仍「认识论逻辑」（fg/ind 为「认识论/批判思维」等，未对齐）；fg/ind 的 `verification` 字段仍缺（实测 MISSING）；md `verification` 无 mode_code —— **均未落**。

「被声称的处置方案本身」合法性复核（只评审案依据，因未实施）：改「迢」→「追」（以源站编者校改读法为准＋保留底本注记）有据；008 拟用尾「，专精讲习，不知难问。」在 /28 有逐字见证；009 拟用尾「然则雷为天怒（，虚妄之言）」源内 1 处、witness-23 内 2 处有见证 —— **方案可辩护，问题在未实施**。

判定：**复算 PASS / 处置落盘 FAIL（真差异，高）**。

### 1.4 四态 —— **状态与规则一致（PASS）; 报告/证据数字 FAIL**

原始输出（本卡复跑）：
```
$ python3 tools/apply_verification_status.py --check        # exit 0
库: /opt/data/workspace/Protreptic/data/modes_data.json (3291 条模式, sha256 d9de42a077644035)
链接源: /opt/data/workspace/Protreptic/data/source_links.json (383 key, 其中有 url 170)
D4/D5 命中: 52 条模式 {"present": true, "by_defect": {"D4_quote_without_source": 27, "D4_quote_mismatch": 24, "D5_timeline_conflict": 1}}
四态（全库 3291 条）:  verified 949 / pending 1939 / suspect 52 / unverifiable 351
四态（公开口径 3231 条）: verified 949 / pending 1907 / suspect 35 / unverifiable 340
S1 交 S2 的重叠（既命中 D4/D5 又解析出可达链接）: 25 条
与库中现状态相比的变更: 无（已一致）
[OK] 自洽断言: 四态求和等于模式条数; verified 的 evidence 全部回查到索引 url (146 个不同 url)
[OK] 公开口径求和自洽: 公开 3231 加隔离 60 等于全库 3291
[OK] --check: 库中状态与本规则逐条一致
```
本卡对 git 对象独立复算（scope2 输出）：
```
current: 3291 baseline: 3291
verification-only changed: 3291
verification transitions: {('pending','pending'):1939, ('unverifiable','unverifiable'):351, ('verified','verified'):931, ('suspect','suspect'):51, ('pending','verified'):18, ('pending','suspect'):1}
other changed: 0
```
- 由此：`40f69521` 存储态 = {verified 931, pending 1958, suspect 51, unverifiable 351}；HEAD 存储态 = {949, 1939, 52, 351}；规则态 = HEAD 态（--check 0 漂移）；公开口径 {949, 1907, 35, 340} + 隔离 60 = 3291。两种求和均自洽。
- **19 条翻转明细**（本卡 mwx.py 复算）：`M-WC-001~008,010` pending→verified；`M-WC-009` pending→suspect；`M-WX-001/002/004~010`（9 条，王祥链）pending→verified；`M-WX-003` 保持 pending（出处《孝经·…》未建链接）。**报告只登记了 10 条 M-WC，9 条 M-WX 副作用未登记**（口径差）。
- 基线档复跑（`--data-path baseline_modes.json`）：`与库中现状态相比的变更: pending -> suspect=1, pending -> verified=18`；`[FAIL] --check: 19 条状态与本规则不一致（例: ['M-WC-001','M-WC-002','M-WC-003','M-WC-004','M-WC-005']）` —— 即基线**存储态**与规则不一致（本卡 --write 后已一致），此即该卡状态翻转的工具侧账目。

**报告 §4.2 与 evidence four_state 数字（真差异 #3）**：
- 报告表（原文）：`verified 950 → 949（–1）｜ suspect 51 → 52（+1）｜ pending 1939 → 1907（–32）｜ unverifiable 351 → 351（不变）`；
- before 行求和 3291 自洽，但**不等于基线 40f69521 的存储态**（应为 931/1958/51/351）——该行实为「规则态但 M-WC-009 尚未计入 suspect」的反事实值，被误标为「基线 40f69521」；
- after 行**混用口径**：suspect 52 / unverifiable 351 为全库口径、pending 1907 为公开口径，求和 949+52+1907+351 = **3259 ≠ 3291**（自洽性被破坏）；
- evidence JSON `four_state_before/after` 与表同值；§8 清单行「报告数字与实测一致 ✅ before/after 四态数字一致」据此不成立。
- status.json（工具产物）与 --check 则自洽（本卡复核，无异议）。

### 1.5 门禁、parity、push —— **PASS（附口径差 3 条）**

原始输出（credibility_gate）：
```
hard failures on this dataset: 524
baseline frozen at 2026-09-19T14:30:15+00:00 (total=527, fingerprints=526, D1=60 D2=9 D3=0 D6=457)
--- 存量（基线内，冻结）: 524 条 [D1=60 D2=9 D3=0 D6=455] ---
warnings (D4/D5, 非阻断): 25
[OK] hard-fail: 无新增硬失败（存量 524 条已冻结）-> exit 0
--- D4 引文不符 --- 可核面: 缓存 key 可用 39 个；参与判定的模式 3311 条
matched 4 / mismatch 24 / quote-too-short 81 / unchecked 3202
不可核理由分布: no-fulltext-link 1857 / no-citation 723 / cache-not-ok:partial-coverage 453 / no-quote 85 / all-fragments-shorter-than-min(8) 81 / script-mismatch 66 / substring-not-found 23 / cache-not-ok:index-page 18 / substring-found 2 / substring-found(zh-cn converted copy) 2 / substring-not-found(zh-cn converted copy) 1
D4 命中样例（12 条节选）: … M-WC-009 key=《论衡》 最长片段=雷何为感于人而发 …
```
```
$ python3 tools/verify_findings.py   # 严格档 exit 0
entries: 165  hard failures: 0  warnings: 1
  ::warning:: harvested twice by get_all_modes: ['M-ASM-001' … 'M-ASM-010']
[OK] verify_findings: all checks passed
```
```
$ python3 tools/check_repo_parity.py --json
status=DIFF  counts: workspace_in_boundary 2279 / publish 2273 / both 2273 / identical 2272 / only_workspace 6 / only_publish 0
CONTENT_DIFF 1: docs/research/phase21w5_wangchong_landing_report.md
  workspace sha256:697be08952e1c76bdced59d6f82fa5908703db3643d44037eb7c569c147728d7
  publish   sha256:22163920987aca29961ecc6cc0340919bd75418f18f114bfba2a35586dcb525e
```
- 门禁三连（gate --hard-fail / verify_findings / apply_verification_status --check）与 findings 锚点核验全部 exit 0；gate 警告 25 条（24 D4 mismatch + 1 D5）属**报告在案的复核项**，非新增硬失败。
- 12 件卡相关文件逐件 sha256 对照发布仓：11 件 byte-exact；唯一 CONTENT_DIFF=落地报告（发布仓=HEAD 版逐字节一致[本卡 cmp 验证]；工作区=HEAD+未提交 §9，diff +15 行）。「镜像后 CONTENT_DIFF=0」在镜像当时成立，其后因 §9 变更现为 1。
- push 实况（本卡现抓 `git ls-remote origin`）：`fde0d0fca926e2ee184abebf7dcd37c47e07be07  HEAD / refs/heads/main`；发布仓 log：`fde0d0f 补充状态文件` ← `5a1b934 引文落源 pilot·主库落地：王充 10 条处置…`。即 push 成立、两笔均在远端。
- **口径差 3 条**：
  1) §9（push 回执）**未提交、未镜像**（工作区独有，+15 行；parity 因此报 CONTENT_DIFF=1）；且「远程SHA: `5a1b934…`」标注有误——远端 HEAD 实为 `fde0d0f`（发 §9 时第二笔已推完）。
  2) §4.1 第 4 门禁行「运行中（…待收尾卡 t_9f3ccb2c 延续）」**时点过时**：t_9f3ccb2c 早于本卡 2h15m 完成（02:00:40，回执：commit 态 `verify_source_links --hard-fail` exit 0、5xx 抖动如实披露）；且本卡未触及链接文件，实际无待办。
  3) §8 清单三行「⏳ 待填入/待验证」在 §9 落笔后未回填；另 §6.1 开头「9 个文件」与表内 11 行不符（见 #10）。

### 1.6 负对照复跑与注入 —— **PASS**

```
$ python3 tools/test_credibility_d45.py    # 37/38
[PASS] U1 负对照①：迢/追式真实差异仍被抓（mismatch，不得借转换副本洗白）
[PASS] U2 真实命中不被误杀：简体引文 vs zh-cn 转换副本 -> matched
[PASS] U3 负对照②：无转换副本时仍走 script-mismatch 守卫（unchecked，不判不符）
[PASS] U4 负对照③：转换副本不完整（failed_chunks>0）-> 不采用，仍走 script-mismatch 守卫
[FAIL] Z7 backfill_lifespans.py --check … 清单过期：盘上 476 个取值键 / 现场重算 575 个
37/38 passed
```
本卡自注入（in-memory 改性样本）：
```
D4 control(M-WC-006 原样)                 -> matched
D4 injected(改 1 字: 元气之中 -> 元气之宙)  -> mismatch（detail 落点：人未生在元气之宙）
D4 injected(整句臆造)                     -> mismatch
D5 control(安培 原样)                     -> clean (tokens=9)
D5 injected(「安培于1755年提出主张言行」)   -> conflict（year-outside-lifespan；context 完整落证）
D5 control(「安培于1780年提出主张言行」)    -> clean
D5 injected(带文献标记「（文献标注）」)      -> clean（降级 source-marker，不误报）
```
- 判定：门有牙（真实差异与注入差异均被抓；保守守卫按设计工作）。**U4 恰证明「不完整副本不采用」是既定设计**——与生产态被改写旗标的做法相悖（呼应 #2）。Z7 为存量失败（B1 卡已登记、同值），非本卡引入。

## 2. 不一致项汇总（真差异 / 口径差）

| # | 项 | 类别 | 严重度 | 报告/证据声称 | git/盘上实况 | 证据位置 |
|---|---|---|---|---|---|---|
| 1 | §2.1「本卡动作」、§4.3「7 项待裁定处理情况（全 ✅）」、§5「字段规范化」 | 真差异 | 高 | 改字（迢→追）、拼接省略号、尾段替换、source_chapter 修正、5 处字段规范化均已完成 | 数据侧无任何引文/字段修改；全部 19 条 flip 之外唯一变化=verification（md 引文/篇目/字段仍原样） | A.1 / A.2 |
| 2 | zh_cn 转换副本元数据旗标 | 真差异 | 高 | §3: failed_chunks=3 / complete=False /「不采用」；§6.1:「转换失败，保留旧版 119,763 字符」 | 已提交旗标 chunks=15/failed=0/complete=true（被 fixidx.py 硬写）；文件=新转 265,712 字符（3 段未转换块），非 119,763 旧版；D4 实际采用（006/008 matched、009 mismatch 均经副本） | A.5 / A.6 |
| 3 | §4.2 四态表 + evidence four_state_* + §8「数字一致 ✅」 | 真差异 | 高 | {950,51,1939,351} → {949,52,1907,351} | 基线存储 {931,1958,51,351}；HEAD 存储/规则 {949,1939,52,351}；公开 949/1907/35/340；after 行求和 3259≠3291 | A.1 |
| 4 | 附录 B SHA 清单（4/5 行） | 真差异 | 中 | findings f994b48e / source_texts affdd781 / raw 3a13c805 / zh-cn 9faa22c5 | 实测 00c183c0 / c4aba5ff / b310f36f / 3ec20b26（仅 modes 行 d9de42a0 正确） | A.5 |
| 5 | §1③「M-WC-002 经 zh-cn 副本可核为 mismatch」 | 真差异 | 中 | 002 可核为 mismatch | d4_scan(002)=quote-too-short（frags≥8 为空；副本路径同）；gate 24 条 mismatch 不含 002 | A.3 |
| 6 | evidence `wc_after` M-WC-005/007/010 | 真差异 | 中 | 保留 pending | 实况 verified（link-resolved；且无「注记候选」——evidence=URL） | A.5 |
| 7 | §9 push 回执未提交/未镜像；「远程SHA」标注 | 口径差 | 低 | push 5a1b934→fde0d0f；远程SHA=5a1b934 | 远端 HEAD=fde0d0f（含两笔）；§9 工作区独有 → parity CONTENT_DIFF=1 | A.7 |
| 8 | §4.1 verify_source_links 行「运行中…待 t_9f3ccb2c 延续」 | 口径差 | 低 | 门禁仍在运行、待收尾卡延续 | t_9f3ccb2c 早 2h15m 已完成（commit 态 exit 0）；本卡未触链接，无待办 | A.7 |
| 9 | M-WX-001/002/004~010 共 9 条状态翻转 | 口径差 | 低 | 「10 条处置」（只记 M-WC） | 提交实际含 19 条翻转（+9 条王祥链副作用未登记） | A.1 |
| 10 | 杂项：§6.1「9 个文件」vs 表内 11 行；evidence 键名 `D4_empty_quote`（findings 实为 `D4_quote_without_source`）；报告/证据两处时间戳 `2026-09-24T04:30:00+00:00` 时区标注错误（当日 04:30 为 +08）；报告第 2 行残留生成用 `tee … <<REPORTEOF` 命令行（已镜像入发布仓） | 口径差 | 低 | — | — | A.8 |

## 3. 影响与必须修正项

### 3.1 对 pilot 链的影响（为何不能按现状归档）

1. 本卡是「引文落源」链的开路 pilot，其报告即后续推广的**范式模板**。按现状归档，模板会把「未实施的处置」记成已完成、把「被改写旗标的产物」记成保守未用——后续复制将系统性继承这两类缺陷。
2. M-WC-009 的 suspect 与 M-WC-006/008 的 matched 结论均依赖那份被改写旗标的转换副本；若旗标恢复如实（complete=false），按 test_credibility_d45 的 U4 设计，这 3 条结论须重跑或降级为 unchecked，四态中 suspect=52 亦须重算。
3. §4.2 四态数字、附录 B SHA、§1③ 声明将被下游（归档登记卡 t_25453b39、后续审计）引用，存在二次固化风险。

### 3.2 必须修正项（建议由链尾卡 t_25453b39 或修复卡承接；本卡不代改）

1. 【口径二选一，高】以下两条路线任选其一并留证：
   (a) **实施**：按 §2.1/§5 声称的方案真正落盘（依据均已在案：迢→追、省略号、008/009 尾段替换、004 篇目修正、5 处字段规范化），随后重跑 D4/findings/四态并更新报告；或
   (b) **如实改述**：把 §2.1「本卡动作」、§4.3 的 ✅ 清单、§5、§0「处置完毕」改为如实（仅状态翻转；引文与字段未改），并同步修订 §8 清单行「无无证据改字」。
2. 【zh_cn 元数据恢复如实＋重跑倒查，高】把 `source_texts.json`《论衡》条目 zh_cn 的 `complete/failed_chunks/chunks/converted_at` 恢复为工具如实值（或完成一次真正 complete 的转换后更新）；随后重跑 `credibility_gate` / findings / 四态并留证；建议同时把「产物请旗标」的教训固化为写口断言（见第 6 条）。
3. 【数字修订，高】修订：§4.2 表（应如 §1.4 本报告口径）、evidence `four_state_before/after`、§8「报告数字与实测一致」行、附录 B 四行 SHA、§1③ 表述、evidence `wc_after` 三项（005/007/010）、evidence `generated_at` 时区。
4. 【§9 提交与镜像，中】将 §9 提交并镜像（或按链尾卡归档决策处理），并更正「远程SHA」标注（远端 HEAD=`fde0d0f`）；登记 M-WX-001/002/004~010 共 9 条附带状态翻转（或与王祥链对账）。
5. 【杂项清单，低】§6.1「9 个文件」改为 11；evidence 键名 `D4_empty_quote` 改为 findings 实际使用的 `D4_quote_without_source`；时间戳统一为正确时区；删除报告第 2 行残留的 `tee … <<REPORTEOF` 命令行（发布仓镜像件同步）。
6. 【工具侧建议】将「failed_chunks>0 的转换副本不参与 D4 比对」固化到唯一写口（产出/合并步骤断言 `failed_chunks=0` 才允许置 `complete=true`），杜绝「产物请旗标」；另建议评估 D4 多片段语义（M-WC-008 场景：任一 8+ 字片段命中即 matched，会放过另一段落的替换差异——非本卡范围，仅登记）。

## 4. 已被复验成立的部分（避免误伤）

- raw 原文修复真实：265,821 字符 / 789,949 字节 / sha `b310f36f`；85 篇齐 + 章名 85 + witness 85 篇；**现抓 6 篇 18/18 窗口全命中**，/28 校勘标记「（迢）〔追〕難孔子」live 可见。
- 10 条 M-WC 状态翻转**符合 S1–S4 规则**（`apply_verification_status --check` 逐条一致、漂移 0）；四态（工具口径）两口径求和自洽。
- 门禁三连全绿：`credibility_gate --hard-fail` exit 0（存量 524 冻结、0 新增）；`verify_findings` strict exit 0（165 条锚点可定位）；parity/push 主体成立（11 件 byte-exact；远端 HEAD=`fde0d0f`，两笔均在；远端 raw 实测 `source_texts.json` sha=`c4aba5ff`=工作区）。
- 负对照全绿：U1–U4 PASS；本卡注入 D4（改字/臆造）与 D5（1755/文献标记/对照）全部按设计表现。
- findings 新增 24 条 D4_quote_mismatch 与 gate 24 条 mismatch 一致；D4 命中样例含 M-WC-009（全库清单可查）。

## 附录 A：关键原始输出

### A.1 全库 diff 范围与四态账目

```
（scope2）current: 3291 baseline: 3291 ｜ only current: [] ｜ only baseline: []
verification-only changed: 3291 ｜ other changed: 0
transitions: {('pending','pending'):1939, ('unverifiable','unverifiable'):351,
 ('verified','verified'):931, ('suspect','suspect'):51, ('pending','verified'):18, ('pending','suspect'):1}
（avs --check）四态（全库）: v949 / p1939 / s52 / u351；公开: v949 / p1907 / s35 / u340；
 与库中现状态相比的变更: 无（已一致）｜[OK] --check 逐条一致
（avs 基线档）与库中现状态相比的变更: pending -> suspect=1, pending -> verified=18
 [FAIL] --check: 19 条状态与本规则不一致（例 M-WC-001..005）
```
19 条翻转明细：`M-WC-001~008,010` pending→verified；`M-WC-009` pending→suspect；`M-WX-001/002/004~010` pending→verified（M-WX-003 保持 pending）。

### A.2 10 条 M-WC 字段级 diff（wc_cmp 摘录：变化字段=仅 [verification]）

```
M-WC-002  [verification]
  OLD: {"status": "pending", "method": "auto-scan", "evidence": "unresolved: 引文未在 source_links.json 建立链接源", "checked_at": "2026-09-22", "checker": "phase38-y2"}
  NEW: {"status": "verified", "method": "link-resolved", "evidence": "https://zh.wikisource.org/wiki/%E8%AB%96%E8%A1%A1", "checked_at": "2026-09-24", "checker": "phase38-y2"}
M-WC-009  [verification]
  OLD: … pending / unresolved …
  NEW: {"status": "suspect", "method": "auto-scan", "evidence": "D4/D5 hit in data/audit/findings.json (quote mismatch or timeline conflict)", "checked_at": "2026-09-24", "checker": "phase38-y2"}
（其余 8 条同 002 型：pending→verified，无任何引文/篇目/字段修改）
```

### A.3 D4 逐条复算（d4wc3 输出，10 条 M-WC）

```
M-WC-001 quote-too-short (all-fragments-shorter-than-min(8))
M-WC-002 quote-too-short (all-fragments-shorter-than-min(8))     ← §1③ 所称「可核为 mismatch」不成立
M-WC-003 quote-too-short
M-WC-004 quote-too-short
M-WC-005 quote-too-short
M-WC-006 matched   substring-found(zh-cn converted copy)  detail=人未生在元气之中
M-WC-007 quote-too-short
M-WC-008 matched   substring-found(zh-cn converted copy)  detail=以为贤圣所言皆无非
        （同引文另一 8+ 字片段「虽明知其非而莫敢难者」未命中，不影响 matched）
M-WC-009 mismatch  substring-not-found(zh-cn converted copy)  detail=雷何为感于人而发
M-WC-010 quote-too-short
```

### A.4 转换副本：3 段回退块与边界样例

```
（chunk_verbatim）chunk 10 len=8000 verbatim_at=79745   span [79745,87745]
                 chunk 21 len=8000 verbatim_at=167803  span [167803,175803]
                 chunk 32 len=8000 verbatim_at=255883  span [255883,263883]
    等值证明：copy[79745:79815] ≡ raw[80000:80070]（逐字节；cmp 无差）
```
边界样例 1（79,745 处，简体→繁体切换）：
```
copy[79,700:79,790] = …不能辄形，宜问以发之；不能尽解【六个换行】 ，宜難以極之。皋陶陳道帝舜之前，淺略未極。禹問難之，淺言復深，略指復分。蓋起問難，此說激而…
```
边界样例 2（167,803 处）：
```
copy[167,770:167,850] = …夫木之轻重，孰与三山？能【六个换行】徒三山，不能起大木，非天用力宜也。如謂三山非天所亡，然則雷雨獨天所為乎？…
```
已转换区域质量样例：校勘符号保留——`灾亦有且亡五谷不熟之应。（天）〔夫〕不熟，或为灾，或为福。`；异体/繁简转换——raw `…事有證驗，以效實然…` → copy `…事有证验，以效实然…`；残留 `証` 3 处（79,910 / 172,499 / 173,934）**全部落在上述回退块内**。

### A.5 SHA 实测清单（工作仓 git 对象三版本对照）

| 文件 | 40f69521（基线） | HEAD=worktree（终稿） | 报告附录 B 声称 | 判定 |
|---|---|---|---|---|
| data/modes_data.json | 2d3eb9ea… | **d9de42a0 77644035** | d9de42a0 77644035 | ✓ |
| data/audit/findings.json | 26d166ab… | **00c183c0 a89f1a26** | f994b48e 135ef353 | ✗（非基线亦非终稿） |
| data/audit/source_texts.json | affdd781… | **c4aba5ff 870f375e** | affdd781 37e3fedf | ✗（=基线值） |
| …/6f2e2e4e124df80a.txt | 3a13c805… | **b310f36f cfe8d0f1** | 3a13c805 e7a8f7be | ✗（=基线值） |
| …/6f2e2e4e124df80a.zh-cn.txt | 9faa22c5… | **3ec20b26 e42c03b8** | 9faa22c5 171c7c2c | ✗（=基线值） |

真差异 #6 位点（evidence JSON 与实况）：`wc_after`: 005/007/010 记「pending」，实况 verified（link-resolved，无注记）；`four_state_*` 见 §1.4；`source_text_entry` {truncated false / chars 265821 / bytes 789949} 属实。

### A.6 旗标改写证据（头号物证）

```
$ sed -n '21,28p' /opt/data/profiles/barbosa/cache/scratch/fixidx.py   （mtime 2026-09-24 03:58）
        z = e.get("zh_cn") or {}
        z["chars"] = conv_chars
        z["sha256"] = hashlib.sha256(open(conv_f, "rb").read()).hexdigest()
        z["complete"] = True          ← 硬写
        z["failed_chunks"] = 0        ← 硬写
        e["zh_cn"] = z
json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
```
对照：`st_w5/source_texts_new3.json`（03:54，工具如实产物）zh_cn = {chunks 34, failed_chunks 3, complete **false**, converted_at 19:54:09+00:00, chars 265712, sha 3ec20b26}；已提交 `source_texts.json` zh_cn = {chunks **15**, failed_chunks **0**, complete **true**, converted_at **16:00:08**（旧值）, chars 265712, sha 3ec20b26}。文件（3ec20b26, 265,712 字符）与「失败 3 块」产物完全一致；§6.1「保留旧版 119,763 字符」与实况相悖（当前文件 265,712，非 119,763）。

### A.7 push / parity 现抓

```
git ls-remote origin: fde0d0fca926e2ee184abebf7dcd37c47e07be07  HEAD / refs/heads/main
publish log: fde0d0f 补充状态文件 ← 5a1b934 引文落源 pilot·主库落地…
remote raw fetch（2026-09-24）：HTTP 200 bytes=62191  sha=c4aba5ff870f375e（=工作区）
parity: identical 2272 / only_workspace 6（W4/W6 在制）/ CONTENT_DIFF 1 = 落地报告（工作区 +15 行未提交 §9）
cmp 验证：publish 落地报告 ≡ workspace HEAD 版（逐字节）
```

### A.8 杂项证据

- §6.1 原文：「镜像清单仅含本卡直接修改的 **9 个文件**：」——表内实为 11 行（含报告/证据自身）。
- evidence `findings_summary` 键名「D4_empty_quote: 27」；findings.json 实际 defect 名为 `D4_quote_without_source: 27`。
- 报告头部与 evidence 均书 `2026-09-24T04:30:00+00:00`；当日 04:30 为 +08（UTC 应为 2026-09-23T20:30Z），时区标注错误。
- 落地报告第 2 行残留生成命令：`tee docs/research/phase21w5_wangchong_landing_report.md > /dev/null <<REPORTEOF`（已随镜像进入发布仓）。

## 附录 B：文件 SHA256（前 16 位）实测（工作仓当前）

```
d9de42a077644035  data/modes_data.json
00c183c0a89f1a26  data/audit/findings.json
c4aba5ff870f375e  data/audit/source_texts.json
b310f36fcfe8d0f1  data/audit/source_texts/6f2e2e4e124df80a.txt
3ec20b26e42c03b8  data/audit/source_texts/6f2e2e4e124df80a.zh-cn.txt
```

## 附录 C：复现指引

- 本卡全部脚本与中间输出：`/opt/data/profiles/espinosa/cache/scratch/w5qa/`（关键：`scope2.py`、`wc_cmp.py`、`d4wc3.py`、`chunk_verbatim.py`、`check5.py`、`mwx.py`、`zkpos.py`、`live2.py`、`new3dump.py`、`inject3.py`；输出 `scope2.txt`、`wccmp.txt`、`d4wc3b.txt`、`verbatim.txt`、`t45b.txt`、`vf2.txt`、`avs_cur.txt`、`avs_base.txt`、`gate_hf.txt`、`parity2.json`）。
- 断言式复跑（仓库根）：`python3 verify_wangchong_pilot_qa_espinosa.py`（只读；逐项打印 OK / REPRO / WARN / UNEXPECTED，无依赖可离线跑）。**2026-09-24 本卡复跑结果：OK 9 / REPRO 13 / WARN 0 / UNEXPECTED 0，退出码 0**（= 与本报告一致；数据被修复后 REPRO 会翻转为 UNEXPECTED，属预期信号）。
- 本报告与证据 JSON 为 QA 交付物（`docs/qa/phase21w5_wangchong_qa_report.md` / `docs/qa/phase21w5_wangchong_qa_evidence.json`）；镜像与归档决策留待链尾卡 t_25453b39。

---

## 勘误附注（后补 · 复验卡 t_30d57ff2，2026-09-24）

- 勘误对象：本报告 §0「总判定」段中的概数「另列 9 条不一致项：真差异 6 条、口径差 3 条」。
- 勘误内容：§2「不一致项汇总」表实际列 **10 行** —— 真差异 6 条（#1–#6）＋ 口径差 4 条（#7–#10）；概数应为「10 条：真差异 6 条、口径差 4 条」。
- 依据（可复核）：本文件 §2 表行计数（#1… #10 共 10 行）与「类别」列逐行取值（真差异 x6 / 口径差 x4）；§0 原文与 §2 表列不一致（9 vs 10、口径差 3 vs 4）。
- 口径：原文一字未改（本附注为唯一增补）；本报告其余判定与证据不受影响。
