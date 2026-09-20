# Phase40-Z2 验收报告：D4/D5 真实现 + 方案文档不夸大

日期：2026-09-20 ｜ 执行：san-martin ｜ 项目仓：`/opt/data/workspace/Protreptic`（master）
发布仓：`/opt/data/release/Protreptic-publish`（origin main）

## 0. 起因（船长独立核验，源码证据）

* `tools/credibility_gate.py::check_d4_quote_mismatch` docstring 自述
  `This is a placeholder - full implementation requires fetching source text.`，
  实际只判「有引文但出处为空」。
* `tools/credibility_gate.py::check_d5_timeline_conflict` docstring `Placeholder - ...`，
  函数体 `return []`（**完全未实现**）。
* 而 `docs/planning/credibility_framework.md` 第 1 节当时把 D4/D5 列为「已实现检查」= **文档失真**。

## 1. 交付

| 文件 | 变更 |
|---|---|
| `tools/source_text_cache.py` | **新增**：D4 的原文缓存读取 + 子串核验规则（N0–N5，唯一实现） |
| `tools/fetch_source_texts.py` | **新增**：按 `source_links.json` 抓原文类链接 → `data/audit/source_texts.json` + `source_texts/*.txt` |
| `tools/credibility_gate.py` | **改**：D4/D5 从空壳改为真实现；gate 报告新增 D4/D5 覆盖 / 命中 / 不可核逐类统计 |
| `tools/build_audit_findings.py` | **改**：新增 `D4_quote_mismatch` / `D5_timeline_conflict` findings + `audit_meta.d4_d5_report` |
| `tools/verify_findings.py` | **改**：`SUMMARY_KEYS` 与锚点规则支持两个新 defect（D4 锚点在 `key_quote_zh`、D5 锚点在本人叙述字段且含 4 位年份） |
| `tools/test_credibility_d45.py` | **新增**：15 项负对照自测（含 3 条误报控制） |
| `tools/check_repo_parity.py` | **改**：TOOL_FILES 纳入 Phase40-Z2 工具链（随两仓同步） |
| `data/audit/source_texts.json` + `data/audit/source_texts/*.txt` | **新增**：96 条原文缓存（3.2 MB） |
| `data/audit/findings.json` | **改**：155 条（新增 D4_quote_mismatch 22 条） |
| `data/modes_data.json` | **改**：`verification.status` 按既有口径推进（warn → suspect 22 条） |
| `docs/planning/credibility_framework.md` | **改**：第 1 节 D4/D5 行改写为真实实现程度 + 新增第 10 节（实现 / 覆盖 / 误报控制 / 局限） |
| 发布仓 `.github/workflows/ci-cd.yml` | **改**：test job 接 `tools/test_credibility_d45.py` |

## 2. 抓取原文（命令 + 原始输出）

```
$ python3 tools/fetch_source_texts.py --force --max-subpages 12
source_links: /opt/data/workspace/Protreptic/data/source_links.json (382 key)
原文类待抓 (types=ctext,gutenberg,wikisource): 96 条
  [ok]        http=200 chars=84287  cov=complete    subs=[3, 3]  《传习录》
  [partial]   http=200 chars=757    cov=partial     subs=[0, 56] 《东游记》
  [partial]   http=200 chars=223    cov=partial     subs=[0, 23] 《论语》
  [ok]        http=200 chars=7021   cov=single-page subs=[0, 0]  《论动体的电动力学》
  …
索引写入 …/data/audit/source_texts.json (96 条; {"ok": 43, "ok-shared": 2, "fetch-failed": 2, "partial": 38, "index-page": 11})
```

要点：wikisource 走 `action=raw`；目录页顺子页抓（《传习录》3 卷 → `complete`）；
分卷数超过上限（如《论语》23 卷、《五灯会元》20 卷）**不去抓**，如实标 `partial`（D4 视为不可核）；
ctext 有 Cloudflare 挑战页 → `http-error`（未伪造）。

## 3. D4/D5 负对照自测

```
$ python3 tools/test_credibility_d45.py
[PASS] G 生卒年解析（int/字符串/约前/负号）
[PASS] G2 夹具人物生卒年装载
[PASS] A D5 矛盾样本必被检出
[PASS] A2 check_d5_timeline_conflict 返回警告文案
[PASS] B D5 干净样本必须 clean（不误报）
[PASS] C 误报控制①：年份不与人物名同现 -> 不判矛盾
[PASS] D 误报控制②：余波标记 -> 不判矛盾
[PASS] E 误报控制③：离生卒年过远 -> 不判矛盾
[PASS] F 无生卒年 -> undetermined 且理由明确
[PASS] H D4 不符样本必被检出（mismatch）
[PASS] I D4 干净样本必须 matched（不误报）
[PASS] J 误报控制：coverage=partial -> 不可核（不得判 mismatch）
[PASS] K 无缓存条目 -> unchecked 且理由明确
[PASS] L 端到端：坏样本必须在 gate 报告里报出 D4 + D5
[PASS] L2 端到端：干净样本不得报 D4/D5

15/15 passed
```

（既有自测同时复跑：`test_credibility_gate.py` 6/6、`test_credibility_gate_modes.py` 7/7。）

## 4. 全库跑一次（命令 + 原始输出）

```
$ python3 tools/credibility_gate.py --data-path data/modes_data.json
=== CREDIBILITY GATE ===
Total modes checked: 2888
Hard failures (D1/D2/D3/D6): 527
  of which D3 出处污染: 0
Warnings (D4/D5): 92

--- D4 引文不符（真子串核验，Phase40-Z2）---
  可核面: 缓存 key 可用 38 个 (index present=True)；参与判定的模式 2888 条
  matched              1
  mismatch            22
  quote-too-short     69
  unchecked         2796
  不可核理由分布（unchecked/quote-too-short 逐类计数）:
    no-fulltext-link                               1585
    no-citation: 出处里没有书名号引文                     647
    cache-not-ok:partial-coverage(缓存未覆盖整部作品)    409
    no-quote                                         72
    all-fragments-shorter-than-min(8)                 69
    script-mismatch(原文繁体 vs 引文简体: 字面比对无意义)     65
    substring-not-found                               22
    cache-not-ok:index-page                           18
    substring-found                                    1
  D4 命中样例:
    M-LZ-005   key=《焚书》      最长片段=不以孔子之是非为是非
    M-SW-004   key=《孙子兵法》   最长片段=对抗中最贵的资产是提问权
    M-HS-006   key=《新思潮的意义》 最长片段=新思潮的唯一目的是再造文明
    M-EIN-003  key=《论动体的电动力学》 最长片段=就在于它竟然可以被理解

--- D5 时间线矛盾（生卒年 × 文本年份，Phase40-Z2）---
  生卒年可用人物: 265 个（data/figures/*.json，含字符串/公元前纪年解析）
  可判定模式: 1132 条（figure 有生卒年）
  扫描到的 4 位年份 token: 1252 个
  clean              512
  undetermined      2376
  不可判定（逐类计数，禁止当成「零缺陷」）:
    out-of-window                                               67
    field-not-claim                                             24
    name-not-in-context                                         13
  D5 命中: 0 条（本次全库扫描无「通过全部过滤」的矛盾）
```

## 5. 误报控制的两条实测证据（本卡重点）

1）**D5 朴素规则会误报**：把「年份落在生卒年之外」直接判矛盾，全库得到 **34 个 token / 20 条模式**，
逐条核对**全部**是余波/文献/背景：

```
M-AE-007  H-AE-001 1480-1521 definition_zh 1522 …1522年9月6日维多利亚号返抵塞维利亚…
M-NEW-007 H-NEW-001 1643-1727 source_chapter 1729 …Machin《月球理论》(1729)…
M-WATT-009 Watt 1736-1819 source_chapter 1868 …麦克斯韦1868年论文《论调速器》…
M-FEYNMAN-005 Feynman 1918-1988 source_chapter 1992 …Gleick (1992), Genius…
M-KANGXI-004 KangXi 1654-1722 source_chapter 1640 …沙俄自1640年代侵扰黑龙江流域…
```

2）**D4 繁简差异会误报**：wikisource 原文繁体 vs 模式引文简体，未加守卫时 `mismatch 87`；
加入 `script-mismatch` 守卫（411 组简繁字对，命中 ≥2 组即判「脚本不同」）后 `mismatch 22`，
剩余逐条为真·字面不符。

## 6. findings / verification 接线

```
$ python3 tools/build_audit_findings.py --write
findings entries: 155
  D1_pseudo_figure: 60        D2_fabricated_source: 10
  D3_source_contamination: 6  D4_empty_quote: 17
  D4_quote_mismatch: 22       D5_timeline_conflict: 0
  D6_orphan_reference: 40     D7_duplicate_definition: 0
[OK] wrote …/data/audit/findings.json

$ python3 tools/verify_findings.py --hard-fail --data-path data/modes_data.json
hard failures on this findings file: 0
[OK] hard-fail: 无新增硬失败（存量 0 条已冻结）-> exit 0

$ python3 tools/apply_verification_status.py --write --checked-at 2026-09-20 --checker phase40-z2
D4/D5 命中: 39 条模式 {"D4_quote_without_source": 17, "D4_quote_mismatch": 22}
四态（全库 2868 条）:  verified 889 / pending 1589 / suspect 39 / unverifiable 351
四态（公开口径 2808 条）: verified 889 / pending 1557 / suspect 22 / unverifiable 340
与库中现状态相比的变更: verified -> suspect=22
[OK] 自洽断言: 四态求和等于模式条数; verified 的 evidence 全部回查到索引 url (145 个不同 url)
[OK] 公开口径求和自洽: 公开 2808 加隔离 60 等于全库 2868

$ python3 tools/apply_verification_status.py --check
[OK] --check: 库中状态与本规则逐条一致
```

即：**D4/D5 命中按既有口径（warn → suspect）进四态**，且四态计数自洽（无新增状态类别）。

## 7. 两仓同步 / CI

（提交哈希、`git status -sb` 无 ahead、CI 结论见交接摘要与下方「同步实测」。）
