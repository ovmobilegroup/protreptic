# Phase21-W5 引文落源 pilot · 工具扩能卡报告

## 1. 验收项
> ①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭ 全 PASS；37/38（Z7 存量 drift）；verify 383 OK；gate --hard-fail exit 0

---

## 2. 收尾补交说明（卡 t_9f3ccb2c，2026-09-24）

【背景】B1 工具扩能卡（t_f09365bb）与 A1 研究卡（t_5a7abc92）的工作树产物缺「仓级收口」（未提交/未镜像/未 push）；且 data/audit/source_texts.json 工作区版本被再生为仅含《论衡》1 条、counts ok:1 的窄版（危险状态：若整体提交将丢 95 条既有条目）。
【本卡处置】1) 以 HEAD 完整版（96 条）为基合并修复 source_texts.json；2) 白名单提交（tools 4 件 + data 2 件 + 本报告 + A1 报告 2 件 + 见证目录；名单外 0）；3) 发布仓镜像 + push + 回执；4) 全链回归复跑留证。零 data/modes_data.json 改动。
【预检复核备注】逐项复核（非照抄）：1) tools 4 件 / source_links.json（+8 行）/ source_texts.json（工作区窄版 1 条 vs HEAD 96 条）与实物一致；2) 缓存双件 dea899a0 已提交、发布仓未镜像未 push，与实物一致；3) 本报告文件 4 行桩实际已随 cb8601a1 提交（原登记写作「未提交」，属表述偏移，如实记录；本卡照常在其上补全并纳入白名单提交，处置不变）。

## 3. source_texts.json 合并证明（96 -> 97，零条目丢失）

| 版本 | 条目数 | 字节 | sha256 |
|---|---|---|---|
| HEAD 完整版（generated 2026-09-20T14:45:01+00:00） | 96 | 60,816 | `4a00e1341896ea545d4b6bc120a4f983cf35fd21e04c441827e820309d64bf73` |
| 工作区窄版（危险态，仅《论衡》） | 1 | 1,948 | `20bfeffdc6a456a9dacbfe67cadc5362cd182fea9090ec258ae96430cfde9a26` |
| 合并后（本卡产出） | 97 | 62,191 | `affdd78137e3fedfb7af6aedc15a6ee0c63b55033b260845c5745d6fe432d6d7` |

- 合并口径：HEAD 96 条逐条原样保留 + 插入《论衡》条目（携带完整 zh_cn 转换元数据：api=zh.wikipedia action=parse、variant=zh-cn、chunk_chars=8000、chunks=15、retries=5、failed_chunks=0、complete=true、converted_at=2026-09-23T16:00:08+00:00、副本文件 data/audit/source_texts/6f2e2e4e124df80a.zh-cn.txt 副本）。
- 插入位=全表 key 排序第 87 位（《论动体的电动力学》与《论语》之间）；合并后全表仍严格有序（机检 merged_sorted=True 通过）。
- 零丢失（程序化证明）：96/96 既有条目逐条 byte-identical（逐条 json.dumps 全等）；added=[《论衡》]，removed=[]，键面唯一无重复。
- 顶层变更 4 处（口径已声明）：generated_at 2026-09-20T14:45:01+00:00 -> 2026-09-23T16:00:08+00:00；policy 增「zh-cn 转换副本」条款；max_subpages 12 -> 95（与 2026-09-23 生成运行参数对齐；85 子页完整抓取的必要参数）；counts.ok 43 -> 44（新增《论衡》为 ok 状态；sum(counts)=97=len(entries) 不变式保持，其余键值不变）。另 schema/generated_by/min_chars 不变。
- 全文件 diff 量化：+37 行 / -4 行（4 行顶层元数据 + 33 行《论衡》条目），无其他任何行变化。

## 4. 回归复跑留证（工作仓，2026-09-24）

| 项 | 结果 |
|---|---|
| credibility_gate.py --hard-fail | exit 0：存量 524 条已冻结、新增 0 条、「无新增硬失败」（warnings D4/D5 26 条非阻断） |
| verify_source_links.py --hard-fail | exit 0：383 条核验（OK 200 共 151；UNVERIFIABLE 共 213；UNREACHABLE 共 19，非阻断存量警告）；硬失败口径「无新增坏链」 |
| test_credibility_gate.py | exit 0：6/6 passed |
| test_credibility_gate_modes.py | exit 0：7/7 passed |
| test_credibility_d45.py | 37/38（唯一 FAIL=Z7 backfill_lifespans 存量 drift：盘上 476 / 现场 575；与 B1 卡同值、非本卡引入；本卡零接触 lifespan 数据） |

## 5. 收口回执（commits / parity / push / 复跑）

- 工作仓提交（master）：`a92c92d45871a14a6f5c338409279c457eae00ae` —— 白名单 280 件（tools 4 + data 2 + 本报告 1 + A1 报告 2 + 见证 271）；暂存清单与白名单集合比对一致（计数 280、sorted diff 空），名单外 0；diffstat +19,567 / -12（见附录 A4 口径）。
- 发布仓镜像（main）：`d4456ab93efe5c273c5b6a621e52749d736a2746` —— 282 件 byte-exact（白名单 280 + 缓存双件 6f2e2e4e 正文与 zh-cn 副本；两侧 sha256 282/282 全等）；diffstat +22,534 / -12。
- push 回执：`a15d89c..d4456ab  main -> main`；`git ls-remote origin main` == `d4456ab93efe5c273c5b6a621e52749d736a2746`（推送后复核一致）。
- 工作仓 master push：不适用（环境事实，同 t_2d15bd2e 先例——远端仅 main；含 440.19MB blob 的历史被 pre-receive 拒，phase45_acceptance.md 与 link_coverage.md 10.1 在案）。
- parity（tools/check_repo_parity.py --json）：
  - 镜像前：DIFF 313 项（6 CONTENT_DIFF + 307 MISSING_IN_PUBLISH；only_workspace 计数 307 项）。
  - 镜像后：DIFF 33 项（0 CONTENT_DIFF + 33 MISSING；identical 计数 2182 项）——残留 33 项全为他链在制（luorq QA 证据与门禁 29 件 + W4 名单修复 4 件），本链文件 0 残留（机检：镜像清单与 diff 集合求交为空）。
- 回归复跑（工作仓，2026-09-24 01:38 起）：
  - credibility_gate --hard-fail：exit 0；与提交前留证逐字节一致（cmp 通过）。
  - 自测三件：test_credibility_gate 6/6、test_credibility_gate_modes 7/7、test_credibility_d45 37/38（Z7 存量），三者均与提交前逐字节一致。
  - verify_source_links --hard-fail：提交态首跑 exit 0（留证见附录 A2）；复跑 4 轮中 2 轮命中 Wikimedia 瞬时 HTTP 500（《人性论》《心血运动论》各一轮，同 URL 另轮为 OK 200 状态）判 DEAD 触发 exit 1，另 2 轮全绿（含末轮）——外网瞬态、非内容回归（与工具注释 Phase38-Y1 所述 Wikimedia 限流抖动同源）；未修改任何基线。
  - 复跑输出与抖动对照（4 轮 UNREACHABLE 计数 38 / 16 / 44 / 4 与 DEAD 500 原文）见附录 A2 节。
- 自指限制（同 t_2d15bd2e 先例）：本报告的二次补记提交 sha 与终态镜像 sha 不进入本报告，登记于卡 t_9f3ccb2c 完成回执 metadata 记录。

## 附录 A：证据原文（节选与全文，由脚本从留档文件装配）

### A1 credibility_gate.py --hard-fail 提交态跑 exit 0
节选：头 16 行 + 尾 12 行（全量 604 行 / 134425 字节）
sha256：19be5bfb5912735aec1ee8165e7e76e7c9ffb716b0dfe704e6665aed7408ee05

```text
=== CREDIBILITY GATE · 存量/新增两档 ===
mode: hard-fail
resolved data path:     /opt/data/workspace/Protreptic/data/modes_data.json (exists=True)
resolved baseline path: /opt/data/workspace/Protreptic/data/audit/credibility_baseline.json (exists=True)
hard failures on this dataset: 524
baseline frozen at 2026-09-19T14:30:15+00:00 (total=527, fingerprints=526, D1=60 D2=9 D3=0 D6=457)
baseline data_sha256: bf168171af42f8148c3adecbbc1a71258522676355357f6466acdcb25f2e61cb
current  data_sha256: 2d3eb9eaf41bc95e7870bae98ced5eeee46ff216272d6dfa444c5441c0a6a964
D3 exemption: on, exempted modes: 43

--- 存量（基线内，冻结）: 524 条 [D1=60 D2=9 D3=0 D6=455] ---
  ::notice::LEGACY M393|D1|H-SX-001 | [M393] D1 伪人物: figure_code=H-SX-001 在隔离名单中
  ::notice::LEGACY M393|D2|《苏咸子·权变篇》 | [M393] D2 伪造出处: source_chapter 包含已知伪造书名 '《苏咸子·权变篇》' -> 《苏咸子·权变篇》
  ::notice::LEGACY M394|D1|H-SX-001 | [M394] D1 伪人物: figure_code=H-SX-001 在隔离名单中
  ::notice::LEGACY M394|D2|《苏咸子·纵横篇》 | [M394] D2 伪造出处: source_chapter 包含已知伪造书名 '《苏咸子·纵横篇》' -> 《苏咸子·纵横篇》
  ::notice::LEGACY M395|D1|H-SX-001 | [M395] D1 伪人物: figure_code=H-SX-001 在隔离名单中
    ...（中段略）...
    no-lifespan-for-figure                                     240
  不可判定（逐类计数，禁止当成「零缺陷」）:
    out-of-window                                              562
    name-not-in-context                                        179
    field-not-claim                                             64
    source-marker                                               12
    background-marker                                            2
    afterlife-marker                                             1
  D5 命中（本人叙述字段里的年份落在生卒年之外）:
    M-NEW-007  representative_cases_zh=1749  动差一半：牛顿未解决，Clairaut 1749 年以摄动级数升阶解决——方法误差而非理
  说明: 判定顺序 = 生卒年可用 -> 4 位年份 -> 生涯带 [生年-40, 卒年+30] -> 字段为本人叙述字段 -> 年份与人物名同现(±20 字) -> 无文献/余波/背景标记。任一环不满足即进「不可判定」并给出理由。
  取文本口径（Phase42-Z4）: 中英镜像字段同扫 —— definition_zh, process_zh, representative_cases_zh, definition_en, process_en, representative_cases_en, source_chapter, key_quote_zh, key_quote_en
```

### A2 verify_source_links.py --hard-fail 提交态跑 exit 0
节选：头 8 行 + 尾 14 行（全量 416 行 / 34300 字节）
sha256：8024aaa66975bea0cb158c1f7629c661dbc2e28178e49dbff1a031278ac2d692

```text
Checking 383 source links... (jobs=4, max-time=10s)
  [OK 200] H-SUY-001 孙权 (183-252) -> https://zh.wikipedia.org/wiki/%E5%AD%99%E6%9D%83
  [OK 200] The History of Astronomy, Sect. II-IV (Wonder, Surprise, Admirable Systems; Newtonian system); WN Introd. & Plan; TMS VI.ii.2.17 (Man of System); Essays on Philosophical Subjects -> https://www.gutenberg.org/ebooks/3300
  [OK 200] WN I.1-3 (Division of Labour, Market Extent); WN II.3 (Productive and Unproductive Labour; Parsimony); WN IV.9 (Agricultural Systems; 'peace, easy taxes, tolerable justice' maxim); Lectures on Jurisprudence (1755 maxim) -> https://www.gutenberg.org/ebooks/3300
  [OK 200] WN I.10.c (Wages and Profit in the different Employments of Labour and Stock); WN I.11 (Rent of Land, conclusion); WN IV.2 & IV.7 (Restraints of Importation, Colonies); WN I.10.c.61 'People of the same trade...' -> https://www.gutenberg.org/ebooks/3300
  [OK 200] WN I.2 (Of the Principle which gives Occasion to the Division of Labour); TMS I.1.1 (Of Sympathy); TMS IV.1.10 (Invisible Hand); TMS III (Conscience, Impartial Spectator) -> https://www.gutenberg.org/ebooks/3300
  [OK 200] WN IV.9.51 (System of Natural Liberty, sovereign's three duties); WN V.1 (Public Works, Institutions, Education); WN V.1.f (Youth and Religious Instruction); WN III (Progress of Opulence); WN IV.7.b (Colony trade monopoly deranges capital allocation) -> https://www.gutenberg.org/ebooks/3300
  [OK 200] 《一桩事先张扬的凶杀案》 -> https://zh.wikipedia.org/wiki/%E4%B8%80%E6%A1%A9%E4%BA%8B%E5%85%88%E5%BC%A0%E6%89%AC%E7%9A%84%E8%B0%8B%E6%9D%80%E6%A1%88
    ...（中段略）...
  ::warning::UNREACHABLE 《孙子兵法》 -> https://zh.wikisource.org/wiki/%E5%AD%AB%E5%AD%90%E5%85%B5%E6%B3%95
  ::warning::UNREACHABLE 《战国策》 -> https://zh.wikipedia.org/wiki/%E6%88%B0%E5%9C%8B%E7%AD%96
  ::warning::UNREACHABLE 《报任安书》 -> https://zh.wikisource.org/wiki/%E5%A0%B1%E4%BB%BB%E5%B0%91%E5%8D%BF%E6%9B%B8
  ::warning::UNREACHABLE 《新思潮的意义》 -> https://zh.wikisource.org/wiki/%E6%96%B0%E6%80%9D%E6%BD%AE%E7%9A%84%E6%84%8F%E7%BE%A9
  ::warning::UNREACHABLE 《沉思录》 -> https://zh.wikipedia.org/wiki/%E6%B2%89%E6%80%9D%E5%BD%95
  ::warning::UNREACHABLE 《瀛涯胜览》 -> https://zh.wikisource.org/wiki/%E7%80%9B%E6%B6%AF%E5%8B%9D%E8%A6%BD
  ::warning::UNREACHABLE 《独立宣言》 -> https://zh.wikisource.org/wiki/%E7%BE%8E%E5%9B%BD%E7%8B%AC%E7%AB%8B%E5%AE%A3%E8%A8%80
  ::warning::UNREACHABLE 《精神现象学》 -> https://zh.wikipedia.org/wiki/%E7%B2%BE%E7%A5%9E%E7%8E%B0%E8%B1%A1%E5%AD%A6
  ::warning::UNREACHABLE 《罗马盛衰原因论》 -> https://zh.wikipedia.org/wiki/%E7%BD%97%E9%A9%AC%E7%9B%9B%E8%A1%B0%E5%8E%9F%E5%9B%A0%E8%AE%BA
  ::warning::UNREACHABLE 《美诺篇》 -> https://zh.wikipedia.org/wiki/%E7%BE%8E%E8%AF%BA%E7%AF%87
  ::warning::UNREACHABLE 《致命的自负》 -> https://zh.wikipedia.org/wiki/%E8%87%B4%E5%91%BD%E7%9A%84%E8%87%AA%E8%B4%9F
  ::warning::UNREACHABLE 《论义务》 -> https://zh.wikipedia.org/wiki/%E8%AE%BA%E4%B9%89%E5%8A%A1

[OK] hard-fail: 无新增坏链（存量 0 条已冻结）-> exit 0
```

复跑抖动对照（4 轮原始证据行）：

```text
run1（提交态首跑）:   [OK 200] 《人性论》 -> https://zh.wikipedia.org/wiki/%E4%BA%BA%E6%80%A7%E8%AB%96_%28%E6%9B%B8%29
run2:   ::error::NEW [DEAD 500] 《人性论》 -> https://zh.wikipedia.org/wiki/%E4%BA%BA%E6%80%A7%E8%AB%96_%28%E6%9B%B8%29
run3:   ::error::NEW [DEAD 500] 《心血运动论》 -> https://zh.wikipedia.org/wiki/%E5%BF%83%E8%A1%80%E8%BF%90%E5%8A%A8%E8%AE%BA
run4（末轮）: [OK] hard-fail: 无新增坏链（存量 0 条已冻结）-> exit 0
UNREACHABLE 计数 run1 至 run4：38 / 16 / 44 / 4
```

说明：DEAD 为外站瞬时 5xx 判据；同一 URL 在另轮为 OK 200；未修改任何基线文件。

### A3 自测全量原文（提交态）

#### test_credibility_gate 6/6
全文 8 行 / 289 字节 —— sha256：b8e8897880ba68a29b196bab1365d117af33eaf10305211a5b1373b329568912

```text
[PASS] A 已隔离 figure 的污染出处不报 D3
[PASS] B 公开 figure 的污染出处必报 D3
[PASS] C --no-d3-exemption 严格模式必报 D3
[PASS] D --negative-test 注入坏样本必 exit 1
[PASS] E 干净公开记录必须 exit 0
[PASS] F 真实源库 D3 计数为 0

6/6 passed
```

#### test_credibility_gate_modes 7/7
全文 9 行 / 374 字节 —— sha256：ba6bfef34bc5e59c77c841a50283b9d826e9af2dc9f6c7a2cc6a265b4e500b13

```text
[PASS] 1 存量态 --hard-fail exit 0
[PASS] 2 存量态 --legacy-report exit 0 且列出存量
[PASS] 3 新增 D3 坏样本 -> exit 1 且 ::error::NEW
[PASS] 4 改写存量引用说明文字 -> 仍 exit 0
[PASS] 5 基线缺失 -> exit 2（fail-closed）
[PASS] 6 --data-path 两份数据结论不同
[PASS] 7 --write-baseline 重新冻结后可继续跑 exit 0

7/7 passed
```

#### test_credibility_d45 37/38（Z7 为存量清单过期项）
全文 41 行 / 2992 字节 —— sha256：42845eeeebee6d2a031ea78bf839993ec3f7653f8e3584cd8531f15bec570c7a

```text
[PASS] G 生卒年解析（int/字符串/约前/负号）
[PASS] G2 夹具人物生卒年装载
[PASS] A D5 矛盾样本必被检出
[PASS] A2 check_d5_timeline_conflict 返回警告文案
[PASS] B D5 干净样本必须 clean（不误报）
[PASS] C 误报控制①：年份不与人物名同现 -> 不判矛盾
[PASS] D 误报控制②：余波标记 -> 不判矛盾
[PASS] E 误报控制③：离生卒年过远 -> 不判矛盾
[PASS] F 无生卒年 -> undetermined 且理由明确
[PASS] M0 field_text 统一取文本口径（str/list/嵌套/None/缺字段/bool/数字）
[PASS] M1 D5 list 载荷里的矛盾年份必被检出（修字段类型盲区）
[PASS] M2 负对照：同一年份放在 str 载荷也必须被检出（两种载荷等价）
[PASS] M3 两种载荷的证据一致（year=1699 / field 相同）
[PASS] M4 process_zh 为 list 且含 None -> 仍被扫描且不崩
[PASS] M5 五字段全 None -> undetermined/no-four-digit-year，不静默放过
[PASS] M6 模式缺 figure_name -> 回退 data/figures 的名字后仍能检出
[PASS] H D4 不符样本必被检出（mismatch）
[PASS] I D4 干净样本必须 matched（不误报）
[PASS] Q D4 key_quote_zh 为 list -> 仍可核且 matched（旧写法 unchecked no-quote）
[PASS] Q2 D4 source_chapter/key_quote_zh 均为 list -> 仍判 mismatch
[PASS] J 误报控制：coverage=partial -> 不可核（不得判 mismatch）
[PASS] K 无缓存条目 -> unchecked 且理由明确
[PASS] U2 真实命中不被误杀：简体引文 vs zh-cn 转换副本 -> matched
[PASS] U1 负对照①：迢/追式真实差异仍被抓（mismatch，不得借转换副本洗白）
[PASS] U3 负对照②：无转换副本时仍走 script-mismatch 守卫（unchecked，不判不符）
[PASS] U4 负对照③：转换副本不完整（failed_chunks>0）-> 不采用，仍走 script-mismatch 守卫
[PASS] L 端到端：坏样本必须在 gate 报告里报出 D4 + D5
[PASS] L2 端到端：干净样本不得报 D4/D5
[PASS] T 端到端：list 载荷的年份必须在 gate 报告里报 D5（引文 matched，不得误报 D4）
[PASS] Z0 生卒年解析扩到公元前写法（约公元前330 / 公元前275 / 空串）
[PASS] Z1 英文镜像字段 representative_cases_en 里的矛盾年份必被检出
[PASS] Z4 年份只在英文镜像字段时 token 仍计入（不再静默 tokens=0）
[PASS] Z2 负对照：英文卒后余波标记 -> 不得判矛盾（afterlife-marker）
[PASS] Z3 负对照：英文文献 / 出版标记 -> 不得判矛盾（source-marker）
[PASS] Z5 取值键：人名键与代码键都登记，时代名键不登记
[PASS] Z6 「约公元前330」式纪年进 lifespan（不再被判无生卒年）
[PASS] Z5b 同键不同生卒年 -> 整体丢弃并在诊断里如实报告
[FAIL] Z7 backfill_lifespans.py --check 对当前数据 exit 0（补数清单可重入不漂移）  [FAIL] 清单过期：盘上 476 个取值键 / 现场重算 575 个 —— 请跑 python3 tools/backfill_lifespans.py 刷新


37/38 passed
```

### A4 source_texts.json 合并 diff 全文（HEAD 96 条 到 合并 97 条）

#### merge diff 全文
全文 55 行 / 2609 字节 —— sha256：ac5efa58a74e41b886b58c3735f6933c32586c52e6665fc25c74ac96ddb9469a

```text
--- HEAD
+++ MERGED
@@ -2,10 +2,10 @@
   "schema": "protreptic.source_texts/v1",
   "generated_by": "tools/fetch_source_texts.py",
-  "generated_at": "2026-09-20T14:45:01+00:00",
-  "policy": "只缓存原文类链接（wikisource/gutenberg/ctext）的真实响应文本；目录页顺着子页抓并如实标 coverage（complete/partial/single-page）；抓不到或只有目录的标 index-page / fetch-failed / http-error，不伪造文本、不用二手转述补位（credibility_framework.md 第 6 节铁律 2）",
+  "generated_at": "2026-09-23T16:00:08+00:00",
+  "policy": "只缓存原文类链接（wikisource/gutenberg/ctext）的真实响应文本；目录页顺着子页抓并如实标 coverage（complete/partial/single-page）；抓不到或只有目录的标 index-page / fetch-failed / http-error，不伪造文本、不用二手转述补位（credibility_framework.md 第 6 节铁律 2）；对 coverage=complete/single-page 的抓取结果另产 zh-cn 转换副本（zh.wikipedia action=parse&contentmodel=wikitext&variant=zh-cn），转换来源、时间、分块与失败重试元数据随条目入索引（zh_cn 字段）",
   "min_chars": 800,
-  "max_subpages": 12,
+  "max_subpages": 95,
   "counts": {
-    "ok": 43,
+    "ok": 44,
     "ok-shared": 2,
     "fetch-failed": 2,
@@ -1668,4 +1668,37 @@
     },
     {
+      "key": "《论衡》",
+      "url": "https://zh.wikisource.org/wiki/%E8%AB%96%E8%A1%A1",
+      "url_fetched": "https://zh.wikisource.org/wiki/%E8%AB%96%E8%A1%A1",
+      "source_type": "wikisource",
+      "status": "ok",
+      "coverage": "complete",
+      "subpages": [
+        85,
+        85
+      ],
+      "http_code": 200,
+      "method": "wikitext",
+      "chars": 120000,
+      "bytes": 356198,
+      "sha256": "3a13c805e7a8f7beae4bdbe733511a17353a1fb48d594a1ba2b27937bf46f372",
+      "file": "data/audit/source_texts/6f2e2e4e124df80a.txt",
+      "truncated": true,
+      "zh_cn": {
+        "api": "https://zh.wikipedia.org/w/api.php",
+        "variant": "zh-cn",
+        "method": "action=parse&contentmodel=wikitext&variant=zh-cn (POST text)",
+        "chunk_chars": 8000,
+        "chunks": 15,
+        "retries": 5,
+        "failed_chunks": 0,
+        "complete": true,
+        "converted_at": "2026-09-23T16:00:08+00:00",
+        "chars": 119763,
+        "sha256": "9faa22c5171c7c2c5dcc9413d7487ac41ff0b27ab7f5662a297267ed3455f935",
+        "file": "data/audit/source_texts/6f2e2e4e124df80a.zh-cn.txt"
+      }
+    },
+    {
       "key": "《论语》",
       "url": "https://zh.wikisource.org/wiki/%E8%AB%96%E8%AA%9E",
```

（附录由脚本装配于 2026-09-24；原始留档与 sha256 见上）
