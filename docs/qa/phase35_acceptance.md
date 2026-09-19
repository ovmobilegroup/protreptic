# Phase35-QA5 独立复验报告（止血效果 + 机制负对照）

卡：`t_819c938f`（espinosa）。上游：`t_13c3b090`（Phase35-V1 止血）、`t_02f916f5`（V2 审计）、`t_70b62dd8`（V3 机制）。
必读依据：`docs/planning/credibility_framework.md`、`docs/qa/phase33_acceptance.md`、`docs/qa/phase34_acceptance.md`。
方法：**自己跑命令、只贴原始输出**；机制项**自造样本**做负/正对照，不采信任何工人自述。

## 0. 复验窗口内的真实情况（先读这一段）

本卡起跑（15:43）到判定（16:47）之间，发布仓被**并行卡 `t_3e0d222c`（Phase35-V1FIX / elcano）连续改写**：
`d8c809c → 1025b3e → ca650ae → 2e3e7a6 → 72a3195`。因此本报告分两个时点取证，**判定以 T2 为准**：

| 时点 | 发布仓 HEAD | Pages 最新 run | 线上 5 个伪人物 URL |
| --- | --- | --- | --- |
| T1（16:00 前，V1 声称完成态） | `d8c809c` | run70 **failure**（部署 skipped） | **全部 200**（止血未到线上） |
| T2（16:47，本报告判定基准） | `72a3195` | run74 **success**（2 job 全 success） | **全部 404**（止血已到线上） |

T1 的证据保留在 §2.1：它证明 V1 的「已隔离、发布仓已推送」当时**并未生效于线上**。

## 1. 终审结论：**不可发布（FAIL）**

| # | 复验项 | 判定 | 依据 |
| --- | --- | --- | --- |
| 1 | V1 止血（T2 线上直取：5 个伪人物 URL / 名录 / 计数 / by-figure 分片） | **PASS** | §2 |
| 2 | 线上部署产物与 `meta.json` 自洽（sha256 逐分片） | **PASS** | §2.3 |
| 3 | D3 出处污染（线上部署产物全量） | **PASS**（仅 `meta.json` 14 处 `sha256`，判明为产物校验清单） | §3.1 |
| 4 | D3 出处污染（`data/modes_data.json` 源库） | **FAIL**（29 条模式仍带工程痕迹出处） | §3.2 |
| 5 | V3 机制负对照（自造 D3 样本 / 干净集） | **PASS**（exit 1 / exit 0） | §4 |
| 6 | V3 门接入 CI（能否阻止回归） | **FAIL**（四个 workflow 无一调用） | §4.3 |
| 7 | V2 审计 `findings.json` 抽样复核 | **FAIL**（3 条中 1 条证据标识错位） | §5 |
| 8 | 两仓字节级一致 | **FAIL**（`data/modes_data.json` 分歧；5 个交付物只在工作仓） | §6.1 |
| 9 | 发布仓 `ahead=0` | **PASS** | §6.2 |
| 10 | 四个 workflow 最新 run 全 success（贴 job 数） | **PASS**（run74/82/62/82，job 2/6/3/1） | §6.3 |

判定逻辑：线上面（1/2/3/5/9/10）在 T2 已经成立，V1 止血**事实上已上线**；但**硬性纪律仍未满足**：
D3 源库未归零（4）、门未接入 CI（6）、审计证据有一处标识错位（7）、两仓非字节一致（8）。
按本卡「任一硬门不过即不可发布」的口径，终审 **不可发布**。

## 2. V1 止血：线上直取

### 2.1 T1（发布仓 `d8c809c`，Pages run70 FAILURE）

```bash
$ for u in H-P23F-001 P24F P25F P26F Phase27Final H-SX-001; do \
    echo "$u -> $(curl -s -o /dev/null -w '%{http_code}' https://ovmobilegroup.github.io/protreptic/minds/$u/)"; done
H-P23F-001 -> 200
P24F -> 200
P25F -> 200
P26F -> 200
Phase27Final -> 200
H-SX-001 -> 404
```

```bash
$ curl -s https://ovmobilegroup.github.io/protreptic/data/meta.json | grep -o '"counts":{[^}]*}'
{"figures":1057,...,"mode_summaries_published":2848,"modes_quarantined":10,...,"mode_by_figure_shards":283,...}
```

```bash
$ for c in H-P23F-001 P24F P25F P26F Phase27Final; do \
    echo "$c -> $(grep -o "$c" online_index.unified.json | wc -l)"; done
H-P23F-001 -> 2
P24F -> 2
P25F -> 2
P26F -> 3
Phase27Final -> 2
```

```bash
$ for code in H-P23F-001 P24F P25F P26F Phase27Final; do \
    echo "$code http_len=$(curl -s .../data/modes/by-figure/$code.json | wc -c) d3_hits=..."; done
H-P23F-001 http_len=79564 d3_hits=42
P24F      http_len=55305 d3_hits=35
P25F      http_len=67960 d3_hits=47
P26F      http_len=53367 d3_hits=19
Phase27Final http_len=55852 d3_hits=36
```

Pages run70（head `d8c809c`）job 明细（GitHub API `runs/35428849131/jobs`）：

```text
构建 SPA + 文档站 ... 首页计数口径收口 | failure
                    生成 service worker (sw.js) ... 断言合并产物 | skipped
部署 | skipped
```

### 2.2 T2（发布仓 `72a3195`，Pages run74 SUCCESS）

```bash
$ date; for u in H-P23F-001 P24F P25F P26F Phase27Final H-SX-001 H-WYM-001; do \
    echo "$u -> $(curl -s -o /dev/null -w '%{http_code}' https://ovmobilegroup.github.io/protreptic/minds/$u/)"; done
Sat Sep 19 16:47:49 CST 2026
H-P23F-001 -> 404
P24F -> 404
P25F -> 404
P26F -> 404
Phase27Final -> 404
H-SX-001 -> 404
H-WYM-001 -> 200          # 真人物仍 200，排除「/minds 整体塌掉」
```

```bash
$ curl -s .../data/meta.json | grep -o '"mode_summaries_published":[0-9]*,...'
"mode_summaries_published":2798,"modes_quarantined":60,"mode_index_shards":8,"mode_by_figure_shards":278
$ curl -s .../manifest.webmanifest | grep -o '"description": "[^"]*"'
"description": "2798 条思维模式 × 278 位历史人物：每条都有出处、操作步骤与现代应用，中英双语，可离线查阅。"
$ curl -s .../data/index.unified.json | grep -o '"counts":{[^}]*}'
"counts":{"total":1333,"figures":278,"scenarios":1055,"with_modes":1297}
$ for c in H-P23F-001 P24F P25F P26F Phase27Final; do echo "$c -> $(grep -o "$c" /tmp/qa5e_index.json | wc -l)"; done
H-P23F-001 -> 0 / P24F -> 0 / P25F -> 0 / P26F -> 0 / Phase27Final -> 0
$ curl -s -o /dev/null -w '%{http_code}\n' .../data/modes/by-figure/P24F.json
404
```

判定：**PASS**。5 个伪人物 URL、by-figure 分片均 404，名录（`index.unified.json`）不含这些 code，门面口径为 2798 × 278。

### 2.3 人物总数与 `meta.json` 自洽（线上产物级）

对线上 `meta.json` 的 `products.*.sha256` 逐个回算（本地重算 sha256 与 `counts` 逐项比）：

```text
modes/index-0.json count_local=379 meta_count=379 sha_match=True
modes/index-1.json count_local=336 meta_count=336 sha_match=True
modes/index-2.json count_local=340 meta_count=340 sha_match=True
modes/index-3.json count_local=340 meta_count=340 sha_match=True
modes/index-4.json count_local=345 meta_count=345 sha_match=True
modes/index-5.json count_local=350 meta_count=350 sha_match=True
modes/index-6.json count_local=355 meta_count=355 sha_match=True
modes/index-7.json count_local=353 meta_count=353 sha_match=True
sum online mode shard entries = 2798   meta mode_summaries_published = 2798
figures.index sha match: True count 1057    meta counts.figures = 1057
```

线上 278 个 by-figure 分片全量抓取，与发布仓本地构建逐字节比：

```text
TOTAL=278 SAME=278 NOTSAME=
```

判定：**PASS**。人物总数 = 278（`counts.mode_by_figure_shards`），与 `index.unified.json` 的 `counts.figures=278`、`meta.json` 自洽。

## 3. D3 出处污染全量扫描

扫描词：`sha256|qa_postmerge|双镜像|入库复检|提交哈希`（另用 gate 的 D3 正则做了源库复核）。

### 3.1 线上部署产物（T2，`generated_at_local=2026-09-19T08:24:56`）

```text
online_figures.index.json hits=0
online_index.unified.json hits=0
online_meta.json hits=14        # ← 保留项：sources/products 的 sha256 校验清单
online_modes_index-0..7.json hits=0
TOTAL=14
```

同类扫描 278 个 by-figure 分片（全量抓取后本地 grep）：

```text
TOTAL=278 SAME=278 NOTSAME=     # 顺带完成字节比对
$ cat /tmp/qa5d/*.json | grep -o -E "sha256|qa_postmerge|双镜像|入库复检|提交哈希" | wc -l
0
```

判定：**PASS**。唯一保留的 14 处 `sha256` 是 `meta.json` 的产物完整性清单，**逐条判明为保留项**。

### 3.2 `data/modes_data.json` 源库（gate 的 D3 正则，仅看 `source_chapter`）

```text
D3 (gate regexes, source_chapter only): 29
  among quarantined figures: 29
  among NON-quarantined: 0
  figures involved: {'Phase27Final': 8, 'P25F': 7, 'P26F': 6, 'H-P23F-001': 4, 'P24F': 4}
  pattern freq: {'[0-9a-f]{8,}': 24, 'sha256': 8, 'qa_postmerge': 6, '入库复检': 6, '修复提交': 3, '双镜像': 3, '提交链': 2}
```

任务指定五词（整条记录，含 `name_zh`）：29 条命中；只看 `source_chapter`：16 条命中，分布在 5 个伪人物名下，**真实人物 0 条**。

实物样例（`M-P27F-007`，源库原文）：

```text
双镜像先例：库萨卡 figures/H-CUS-001.json sha256 1b9991e9 'data/ 与 docs/ 字节全等'；林彪卡 021295f8 双镜像；
入库复检先例：qa_postmerge 脚本'payload 与 DB/figure 逐字段一致'断言（朱可夫 t_6fa604a5 等提交信息）；...
```

判定：**FAIL**。这 29 条的图都是已隔离伪人物，但它们**仍在源库文件里**——本卡口径是「源库与线上产物命中数目标归零」。

## 4. V3 机制：自造样本负对照

不看 `--negative-test` 自述分支，**自建两套夹具**（`/tmp/qa5/gate_neg`、`/tmp/qa5/gate_pos`，各自放一份 `tools/credibility_gate.py` + `_quarantine.py` + 自写 `data/modes_data.json`）：

```bash
$ cd /tmp/qa5/gate_neg && python3 tools/credibility_gate.py; echo "EXIT_NEG=$?"
=== CREDIBILITY GATE ===
Total modes checked: 1
Hard failures (D1/D2/D3/D6): 1
  ::error::[M-QA5-NEG-001] D3 出处污染: source_chapter 匹配污染模式 'sha256' -> Phase 21 入库与修复提交链（双镜像 sha256 记录：茅以升 96bdd4c4…）
[FAIL] Gate failed with 1 hard failures
EXIT_NEG=1

$ cd /tmp/qa5/gate_pos && python3 tools/credibility_gate.py; echo "EXIT_POS=$?"
=== CREDIBILITY GATE ===
Total modes checked: 2
Hard failures (D1/D2/D3/D6): 0
[OK] Gate passed (no hard failures)
EXIT_POS=0
```

真实数据全量跑：

```bash
$ cd /opt/data/workspace/Protreptic && python3 tools/credibility_gate.py; echo "EXIT=$?"
Total modes checked: 2888
Hard failures (D1/D2/D3/D6): 556
[FAIL] Gate failed with 556 hard failures
EXIT=1
```

判定：机制**本体可用**（负对照 exit 1、正对照 exit 0）。但发现两个缺陷：

### 4.3 门未接入 CI + `--data-path` 失效

```bash
$ grep -rn "credibility_gate\|source_links\|verify_source_links" \
    /opt/data/release/Protreptic-publish/.github/workflows/ /opt/data/workspace/Protreptic/.github/workflows/
（无输出）
```

`tools/credibility_gate.py` 里 `args.data_path` 被解析却从未使用（`load_modes_data()` 读死模块常量 `DATA_PATH`），
即**无法指向别的产物**做校验；再加上四个 workflow 无一调用它，该机制当前**不能阻止任何回归**。判定 **FAIL**。

`source_links.json` 抽样（8 条，自行 curl）：

```text
200  https://ctext.org/wiki.pl?if=gb&chapter=605807
200  https://ctext.org/wiki.pl?if=gb&chapter=244105
200  https://ctext.org/wiki.pl?if=gb&chapter=228642
200  https://ctext.org/wiki.pl?if=gb&chapter=535437
200  https://www.gutenberg.org/ebooks/3300
200  https://ctext.org/wiki.pl?if=gb&chapter=678905
200  https://ctext.org/wiki.pl?if=gb&chapter=252250
000  https://openlibrary.org/search?q=Tokugawa+shogunate   # 换 %20 编码重试 4 次仍 000
```

7/8 → 200；openlibrary 那条 4 次重试全 `000`（连接层失败，非 404，判为本机代理侧网络问题，**不计入链接源缺陷**）。

## 5. V2 审计 `findings.json` 抽样复核

抽 3 条，**独立回源复核证据是否成立**：

| 抽样 | 结论 | 复核方式与原文 |
| --- | --- | --- |
| `M-P23F-001` D1 伪人物 | **成立** | 源库 `figure_name="Phase23收尾整合"`，`source_chapter` 为「Phase 21 入库提交链（boards 仓 git log…）」「M-ZKZ-001 缺陷修复提交（4a89ae4…）」 |
| `M-P23F-002` D3 出处污染 | **成立（逐字吻合）** | 源库 `source_chapter` = 「Phase 21 入库与修复提交链（双镜像 sha256 记录：茅以升 96bdd4c4、竺可桢 1c034c51→46cd3d26 等）；verify_mys.py 的 embedded==lib 校验段…」 |
| `M-SX-001` D2 伪造出处 | **不成立（标识错位）** | 源库里**不存在** `mode_code = M-SX-001`；`《苏咸子》` 10 条的 code 实际是 `M393`–`M402`（`figure_code=H-SX-001`）。缺陷为真，但 `findings.json` 的 `mode_code` 指向不存在的记录 |

```text
$ M-SX-001 lookup -> None
modes containing 苏咸子: 10
   ('M393','H-SX-001','《苏咸子·权变篇》') ... ('M402','H-SX-001','《苏咸子·时势篇》')
```

判定：**FAIL**（3 抽样中 1 条证据标识错位，下游按 code 定位会落空）。
另：`data/audit/findings.json` 不在发布仓（见 §6.1），审计清单实际未随产物分发。

## 6. 全局

### 6.1 两仓字节级一致（`72a3195` 时点）

```text
data/modes_data.json                         DIFF      # 主数据！见下
tools/_quarantine.py                         SAME
tools/export_static_site.py                  SAME
tools/pages_preflight.py                     SAME
tools/apply_site_counts.py                   SAME
tools/site_counts.py                         SAME
web/src/composables/useSeo.ts                SAME
web/public/manifest.webmanifest              SAME
web/public/manifest-light.webmanifest        SAME
.github/workflows/pages.yml                  SAME
api/protreptic.db                            SAME
docs/qa/credibility_audit.md                 SAME
tools/credibility_gate.py                    only-workspace
data/source_links.json                       only-workspace
data/audit/findings.json                     only-workspace
tools/migrate_verification_schema.py         only-workspace
tools/verify_source_links.py                 only-workspace
```

```bash
$ echo "verification field: ws=$(grep -o '\"verification\"' $WS/data/modes_data.json | wc -l) rel=$(grep -o '\"verification\"' $REL/data/modes_data.json | wc -l)"
verification field: ws=2888 rel=20
```

判定：**FAIL**。V3 的 `verification` 字段（2888 条）与四件机制交付物**未同步进发布仓**，主数据文件两仓不一致。

### 6.2 发布仓 ahead

```bash
$ git -C /opt/data/release/Protreptic-publish status -sb
## main...origin/main
$ git -C /opt/data/release/Protreptic-publish rev-parse --short HEAD
72a3195
```

判定：**PASS**（无 `[ahead N]`，工作树干净）。

### 6.3 四个 workflow 最新 run（head `72a3195`，逐个贴 job）

| workflow | run | 结论 | job（名/结论） |
| --- | --- | --- | --- |
| `pages.yml`「Deploy to GitHub Pages」 | 74 | success | 构建 SPA + 文档站 success；部署 success（共 2） |
| `ci-cd.yml`「Protreptic CI/CD」 | 82 | success | Test success；Build Web Docker success；Build API Docker success；Notify success；Deploy to Staging skipped；Deploy to Production skipped（共 6） |
| `quality-gate.yml`「Quality Gate」 | 62 | success | 线上死链检测 success；数据校验 success；Lighthouse 预算门 success（共 3） |
| `markdown-lint.yml`「CI」 | 82 | success | markdown-lint success（共 1） |

判定：**PASS**（T1 时点曾是 pages FAILURE / markdown-lint FAILURE，见 §0）。

## 7. 阻塞项（复验未通过清单）

1. **D3 源库未归零**：`data/modes_data.json` 中 29 条模式的 `source_chapter` 仍含工程痕迹（`sha256` / 提交哈希 / `双镜像` / `qa_postmerge` / `入库复检`），全部挂在 5 个已隔离伪人物名下。要么从源库清除，要么在 `credibility_framework.md` 里把「隔离即豁免」写成明文口径（当前口径是归零）。
2. **两仓非字节一致**：`verification` 字段（2888 条）与 `tools/credibility_gate.py`、`data/source_links.json`、`data/audit/findings.json`、`tools/migrate_verification_schema.py`、`tools/verify_source_links.py` 只在工作仓。
3. **机制未接入 CI**：四个 workflow 无一调用 `credibility_gate.py` / `verify_source_links.py`，且该门的 `--data-path` 参数被解析后未生效。
4. **审计证据标识错位**：`findings.json` 用 `M-SX-001`–`M-SX-010` 指代 `《苏咸子》` 10 条，源库实际 code 为 `M393`–`M402`。
5. **过程性风险（非缺陷，但需知会）**：复验期间发布仓被 `t_3e0d222c` 连续改写 4 次（`d8c809c`→`72a3195`），T1 的「线上未止血」与 T2 的「已止血」是同一条流水线的两个瞬间；本报告结论绑定 `72a3195` 与 `2026-09-19 16:47` 的线上快照。
