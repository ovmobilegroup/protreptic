# Phase36-QA6 独立复验报告（4 项阻塞是否真闭环）

卡：`t_bfd47996`（espinosa）。上游：`t_9d4f3531`（Phase36-W4）；W1/W2/W3 见 §2–§4。
必读依据：`docs/qa/phase35_acceptance.md`（QA5 终审，逐项原始命令与输出）。
方法：**自己跑命令、只贴原始输出、自造样本**；不采信任何工人自述。

复验快照（本报告判定基准，单一时间点）：

| 项 | 值 |
| --- | --- |
| 本地时间 | `Sat Sep 19 19:12:56 CST 2026` |
| 工作仓 `/opt/data/workspace/Protreptic` | branch `master` @ `c3da04bb` |
| 发布仓 `/opt/data/release/Protreptic-publish` | branch `main` @ `2db123a`（`git status -sb` 无 ahead） |
| 线上产物 | `meta.json` `generated_at=2026-09-19T10:26:22+00:00`，sources.modes_data.json sha256=`bf168171…` |

## 1. 终审结论：**不可发布（FAIL）**

| # | 复验项 | 判定 | 依据 |
| --- | --- | --- | --- |
| 1 | W1 · D3 源库（归零 / 豁免口径） | **FAIL** | 源库仍 6 条；豁免条款**未落地到 gate**（自造样本：豁免名单仍被报 D3） |
| 2 | W2 · `findings.json` 证据一一对应 + 自检脚本 | **FAIL** | 标识错位已修（M393/394/395 逐字吻合）；但**无任何自检脚本**、证据与计数陈旧、H-SX-001 只列 3/10 |
| 3 | W3 · 四 workflow 接入 gate + 坏样本必红 | **FAIL** | 发布仓四个 workflow **0 命中**；工作仓仅 `pages.yml` 1/4；照抄接入会**把 Pages 永久打红**（exit 1 / 533） |
| 4 | W4 · 两仓字节级一致 | **FAIL** | QA5 点名的 7 个文件已 equal；但全量比对仍有 **44/2363 共同 tracked 文件 hash 不同**（含 `.github/workflows/pages.yml`） |
| 5 | 全局 · 线上 404 / 计数自洽 / ahead / CI | **PASS** | §6：6 个伪人物 URL 全 404、分片 2798 自洽且 sha 全等、ahead=0、四 workflow 最新 run 全 success |

判定逻辑：线上面（5）成立；但 W1（源库 D3）与 W3（CI 门）**均未完环**，W2/W4 各有硬缺口。
按本卡「任一硬门不过即不可发布」口径 -> **不可发布**。

## 2. W1 · D3 源库

### 2.1 全量扫描（gate 的 D3 正则，仅 `source_chapter`）

```bash
$ cd /opt/data/workspace/Protreptic && python3 /tmp/qs36/d3scan.py data/modes_data.json
total modes: 2888
D3 source_chapter hit modes: 6
figures: {'H-P23F-001': 3, 'P25F': 1, 'P26F': 2}
pattern freq: {'[0-9a-f]{8,}': 5, '提交链': 1}
   ('M-P23F-001', 'H-P23F-001', '[0-9a-f]{8,}', 'Phase 21 入库提交链（boards 仓 git log：H-PGR-001 至 H-MYS-001 系列）；merge_payload 规范（workspaces/t_83774645/notes）；M-ZKZ-001 缺陷修复提交（4a89ae4：三处 related_modes 粘连 id 的显式修复）；《')
   ('M-P23F-002', 'H-P23F-001', '提交链', 'Phase 21 入库与修复提交链（ 记录：茅以升 、竺可桢 -> 等）； 的 embedded==lib 校验段；docs-as-code 与静态站点生成器的工程实践')
   ('M-P23F-009', 'H-P23F-001', '[0-9a-f]{8,}', 'Phase 21 提交信息基线句式（1112->1122 等，见 1f08fe0/f4e1034/9c512e6/e2fd3e2/5f65d16）；验收脚本的计数断言；归档复检的 git 对象基线验证（t_750d3584 报告）；复式记账与数据仓库行数对账传统')
   ('M-P25F-006', 'P25F', '[0-9a-f]{8,}', 'Phase 25 研究卡开工实践（t_954a5264 工作区的 check_existing.py/findmo.py/pref*.py/cm*.py 探查脚本序列——先探查后撰写的真实脚本链）；Phase 21 事故先例：商君 M381-390 撞号、H-WZ-001 串题、H-LZ-001 误占 M301-310')
   ('M-P26F-001', 'P26F', '[0-9a-f]{8,}', '事故与教训：t_4b51be46（郭守敬研究卡误交付张衡 payload 事件）及其 references/lessons-t_4b51be46.md 四条教训；制度化落地：本批次各研究卡 qa_payload_*.py 的第 25 项任务卡身份交叉断言与第 26 项跨人物污染断言（如同期案例人物卡 t_f53')
   ('M-P26F-004', 'P26F', '[0-9a-f]{8,}', '本批次完整四卡链实例：同期案例人物（研究卡）（研究）-> t_d818de96（入库 71759c9）-> t_8266fab1（独立 QA 24/24）-> t_e83a3d7f（文档归档 4e3fc46）；邻卡人物链 -> t_b07597ef（6ed5afd）-> t_e1aff2e9 -> t_96e1c4b1；德雷克 t')
```

对照 QA5 §3.2 的 29 条：**清理生效（29->6），但未归零**；剩余 6 条全部挂在已隔离伪人物（H-P23F-001 / P25F / P26F）名下，公开人物 0 条。

### 2.2 豁免口径核验（自造样本，不采信文档自述）

`docs/planning/credibility_framework.md` 第 34 / 96–97 行声称：

```text
| | | **豁免条款**：已隔离（D1）的伪人物 figure 允许保留源库工程痕迹…机检方式：D3 gate 跳过 quarantined figure 的模式，仅对公开人物进行 source_chapter 扫描。
  D3 出处污染    -> 硬 FAIL（正则扫描 source_chapter，**豁免已隔离 figure**）
  | | *豁免逻辑*：跳过 quarantined figure（H-P23F-001/P24F/P25F/P26F/Phase27Final）的模式，仅对公开人物扫描
```

自建两套夹具（各放一份 `tools/credibility_gate.py` + `tools/_quarantine.py` + 自写 `data/modes_data.json`）：

```bash
$ cd /tmp/qs36/fxa && python3 tools/credibility_gate.py    # 夹具 A：豁免名单人物 H-P23F-001 带 sha256 出处
=== CREDIBILITY GATE ===
Total modes checked: 2
Hard failures (D1/D2/D3/D6): 2
  ::error::[M-EXEMPT-QA6-001] D1 伪人物: figure_code=H-P23F-001 在隔离名单中
  ::error::[M-EXEMPT-QA6-001] D3 出处污染: source_chapter 匹配污染模式 'sha256' -> Phase 21 入库与修复提交链（双镜像 sha256 记录：茅以升 96bdd4c4）
[FAIL] Gate failed with 2 hard failures
EXIT_A=1

$ cd /tmp/qs36/fxb && python3 tools/credibility_gate.py    # 夹具 B：公开人物 H-CLEAN-001 带同样污染
  ::error::[M-NONEXEMPT-QA6-001] D3 出处污染: source_chapter 匹配污染模式 'sha256' -> …
[FAIL] Gate failed with 1 hard failures
EXIT_B=1
```

结论：**「非豁免必报」PASS**；**「豁免不报」FAIL** —— 代码 `check_d3_pollution(mode)` 没有任何 quarantine 参数，`run_gate()` 对所有模式一律跑 D3，文档里的豁免逻辑在代码中不存在。且 `check_d1_fake_figure` 对隔离名单**硬 FAIL**，因此 gate 在源库上永远不可能通过。

### 2.3 gate 全量跑（源数据）

```bash
$ cd /opt/data/workspace/Protreptic && python3 tools/credibility_gate.py --data-path data/modes_data.json
...
[FAIL] Gate failed with 533 hard failures
EXIT=1
```

判定 **FAIL**。

## 3. W2 · `findings.json` 证据与自检

### 3.1 全量逐条回源（9 条）

```text
modes index size: 2858        # 源库 d['modes'] 内 mode_code 可索引数
--- M-P23F-001 D1_pseudo_figure - EXISTS   figure_code=H-P23F-001
--- M-P23F-002 D3_source_contamination - EXISTS   figure_code=H-P23F-001
--- M-P24F-001 D1_pseudo_figure - EXISTS   figure_code=P24F
--- M-P25F-001 D1_pseudo_figure - EXISTS   figure_code=P25F
--- M-P26F-001 D1_pseudo_figure - EXISTS   figure_code=P26F
--- M-P27F-001 D1_pseudo_figure - EXISTS   figure_code=Phase27Final
--- M393 D2_fabricated_source - EXISTS   figure_code=H-SX-001   source_chapter=《苏咸子·权变篇》
--- M394 D2_fabricated_source - EXISTS   figure_code=H-SX-001   source_chapter=《苏咸子·纵横篇》
--- M395 D2_fabricated_source - EXISTS   figure_code=H-SX-001   source_chapter=《苏咸子·言术篇》
```

QA5 阻塞项 #4（`M-SX-001`–`M-SX-010` 指向不存在记录）已修：三个 code 在源库**逐字存在**，evidence 引文与 `source_chapter` 完全相同：

```bash
$ python3 /tmp/qs36/verify_findings.py
--- finding M393 D2_fabricated_source - EXISTS
  figure_code: H-SX-001 | name_zh: 审时度势法
  source_chapter: 《苏咸子·权变篇》
    frag in source_chapter: 《苏咸子·权变篇》 -> True      # 逐字吻合
--- finding M394 … 《苏咸子·纵横篇》 -> True
--- finding M395 … 《苏咸子·言术篇》 -> True
```

### 3.2 但有四个硬缺口

（a）**证据陈旧**：`M-P23F-002` 的 evidence 引用「双镜像 sha256 记录：茅以升 96bdd4c4、竺可桢 1c034c51->46cd3d26 等」，该段文字已被 W1 的清理（`6237ecf6`）从源库删除：

```text
  source_chapter: Phase 21 入库与修复提交链（ 记录：茅以升 、竺可桢 -> 等）； 的 embedded==lib 校验段…
    frag in source_chapter: 双镜像 sha256 记录：茅以升 96bdd4c4、竺可桢 1c034c51-> -> False
```

（b）**summary 计数与源库现状不符**（自算，gate 正则口径）：

```text
get_all_modes 口径总数: 2888          # findings.audit_meta.total_modes_count 写 2838
当前 D1(隔离人物模式数): 60           # summary 写 50
当前 D2(《苏咸子》模式数): 10         # summary 写 10  ✓
当前 D3(源库工程痕迹模式数): 6 ['M-P23F-001','M-P23F-002','M-P23F-009','M-P25F-006','M-P26F-001','M-P26F-004']   # summary 写 19
```

（c）**清单覆盖不全**：源库《苏咸子》共 **10 条**（`M393`–`M402`），`findings.json` 只列 3 条（`M393/M394/M395`），summary 却写 `D2_fabricated_source: 10`：

```text
源库《苏咸子》模式: 10
   M393 《苏咸子·权变篇》   M394 《苏咸子·纵横篇》   M395 《苏咸子·言术篇》
   M396 《苏咸子·权变篇》   M397 《苏咸子·虚实篇》   M398 《苏咸子·利益篇》
   M399 《苏咸子·情报篇》   M400 《苏咸子·主动篇》   M401 《苏咸子·合纵篇》
   M402 《苏咸子·时势篇》
findings 条数: 9 | 其中 H-SX-001: 3
```

（d）**「自检脚本」不存在**：全仓（含发布仓）搜索，**没有任何脚本以 `data/audit/findings.json` 为输入**（`grep -rln "findings" --include=*.py` 只命中 `scan_phase35.py`，而它输出的是 `workspace/phase35_findings.json`，不读 findings）。把不存在 code 注入副本后，无任何脚本会报错：

```text
injected bogus code M-QA6-NONEXISTENT-999 into a COPY: /tmp/qs36/fxc/findings_bad.json
（无脚本以 findings.json 为输入）
```

判定：**标识错位 PASS，其余 FAIL** -> 本项整体 **FAIL**。

## 4. W3 · CI 门

### 4.1 四个 workflow 的 gate 调用计数

```bash
$ for w in pages.yml ci-cd.yml quality-gate.yml markdown-lint.yml; do
    echo "PUB $w: $(grep -c 'credibility_gate\|verify_source_links' $PUB/$w) 命中"
    echo "WS  $w: $(grep -c 'credibility_gate\|verify_source_links' $WS/$w) 命中"
  done
PUB pages.yml: 0 命中        WS  pages.yml: 5 命中
PUB ci-cd.yml: 0 命中        WS  ci-cd.yml: 0 命中
PUB quality-gate.yml: 0 命中  WS  quality-gate.yml: 0 命中
PUB markdown-lint.yml: 0 命中 WS  markdown-lint.yml: 0 命中

$ grep -rni "credibility\|source_links\|gate" /opt/data/release/Protreptic-publish/.github/workflows/
（仅命中 quality-gate.yml 的注释与 `name: Quality Gate`，无任何 gate 调用）
```

**发布仓（线上唯一来源）0/4；工作仓 1/4。** 卡面要求「确认四个 workflow 里确有 gate 调用」未满足。

### 4.2 自造坏样本 -> gate 会红，但 CI 不会

机制本体可用（§2.2 夹具 B：污染 -> exit 1）。CI 侧不可能红，因为**没有任何 workflow 调用它**。进一步实测：把工作仓 `pages.yml` 里那三条命令原样跑一遍（源数据），**全部非 0**，即 W3 若真同步进发布仓，Pages 会永久红、部署 skip：

```bash
$ python3 tools/credibility_gate.py --data-path data/modes_data.json
[FAIL] Gate failed with 533 hard failures          EXIT=1

$ python3 tools/credibility_gate.py --negative-test --data-path data/modes_data.json
[OK] Negative test PASSED: D3 pollution correctly caught -> exit 1     EXIT=1
```

注意第二条：负对照的**成功**语义就是 `exit 1`，把它当 CI 步骤（要求 exit 0）语法上必然红 —— W3 的 CI 接入即使同步过去也是坏的。

判定 **FAIL**。

## 5. W4 · 两仓字节级一致（全量，不只抽 5 个）

```bash
$ python3 /tmp/qs36/tworepo.py     # git ls-files + 逐文件 sha256
WS branch: master | PUB branch: main
tracked WS(master): 3832 | tracked PUB(main): 3041
common: 2363 | common_hash_different: 44 | common_missing_on_disk: 0
only_ws: 1469 | only_pub: 678
hash_diff_buckets: {'.github/**': 1, '<root>': 1, 'api/**': 5, 'docs/**': 32, 'scripts/**': 5}
```

44 个 hash 不同的文件（全量列表）：

```text
.github/workflows/pages.yml                 Dockerfile.web
api/database.py  api/load_data.py  api/load_v6.py  api/rebuild_semantic_index.py  api/semantic_search.py
docs/00-quick-start/thinking_mode_quick_start.md   docs/02-tools/figure_library.md
docs/06-ai-collaboration/thinking_mode_ai_templates.md   docs/07-coaching/*.md (4)
docs/09-evolution/*.md (4)   docs/10-community/thinking_community_ops_plan.md
docs/architecture/v7_validate.py  docs/architecture/web_pages_migration_assessment.md
docs/batch_import_56_runbook.md  docs/figures/H-AN-001.md  docs/figures/H-CY-001.md
docs/figures/phase20_wangxiang_research.md  docs/islam_phase2_review_report.md
docs/phase20_gai_zi_research.md  docs/planning/file_checklist.md  docs/planning/phase4_summary.md
docs/research/*.md (10)   docs/review/*.md (3)
scripts/append_scenarios.py  scripts/append_scenarios_en.py  scripts/check_none.py
scripts/fix_scenarios.py  scripts/verify_scenarios.py
```

单侧文件结构差异：`only_ws` 1469，绝大多数是工作仓根目录 1256 个 `XX-XXX-001.json` 旧副本与怪名遗留；`only_pub` 678，主要是 `data/intl_figures/**`（工作仓把国际人物放在根目录、发布仓挪到 `data/`）。

QA5 阻塞项 #2 点名的文件：**全部已一致**

```text
data/modes_data.json                    ws=bf168171af42 pub=bf168171af42 equal=True
data/audit/findings.json                ws=f1a91c6c0a78 pub=f1a91c6c0a78 equal=True
data/source_links.json                  ws=e1e1bf71f515 pub=e1e1bf71f515 equal=True
tools/credibility_gate.py               ws=7bfcc7dd4958 pub=7bfcc7dd4958 equal=True
tools/_quarantine.py                    ws=1faff7d57bf6 pub=1faff7d57bf6 equal=True
tools/verify_source_links.py            ws=064c32ad0465 pub=064c32ad0465 equal=True
tools/migrate_verification_schema.py    ws=31011866cc1b pub=31011866cc1b equal=True
.github/workflows/pages.yml             ws=6d1ef5cd3ffb pub=b8a4b936463d equal=False   <- 工作仓含 gate 步骤，发布仓无
```

判定：**「影响线上的点名文件同步发布仓」PASS；「两仓字节级一致」FAIL**（44 个共同文件 hash 不同，其中 `.github/workflows/pages.yml` 正是线上发布链本体）。本项整体 **FAIL**。

## 6. 全局

### 6.1 线上伪人物 URL（6 个 + 1 个真人物对照）

```bash
$ for u in H-P23F-001 P24F P25F P26F Phase27Final H-SX-001 H-WYM-001; do
    echo -n "$u -> "; curl -s -o /dev/null -w '%{http_code}\n' --max-time 20 …/minds/$u/; done
H-P23F-001 -> 404
P24F -> 404
P25F -> 404
P26F -> 404
Phase27Final -> 404
H-SX-001 -> 404
H-WYM-001 -> 200          # 真人物仍 200，排除「/minds 整体塌掉」
```

### 6.2 线上计数自洽 + 分片 sha 全等

```bash
$ python3 /tmp/qs36/shard_sha.py
  modes/index-0.json: entries=379/379 bytes=98002/98002 sha_match=True
  modes/index-1.json: entries=336/336  ... sha_match=True
  modes/index-2.json: entries=340/340  ... sha_match=True
  modes/index-3.json: entries=340/340  ... sha_match=True
  modes/index-4.json: entries=345/345  ... sha_match=True
  modes/index-5.json: entries=350/350  ... sha_match=True
  modes/index-6.json: entries=355/355  ... sha_match=True
  modes/index-7.json: entries=353/353  ... sha_match=True
sum entries: 2798 | published: 2798 | meta shard count: 2798
shards ok: 8 bad: 0
figures.index.json sha_match: True count: 1057
$ python3 /tmp/qs36/online_check.py
counts: {"figures":1057,"figure_shards":1057,"mode_summaries":2858,"mode_summaries_published":2798,
         "modes_quarantined":60,"mode_index_shards":8,"mode_by_figure_shards":278,"modes_raw":2868,
         "modes_deduped":2858,"modes_duplicates_dropped":0,"modes_empty_mode_code_dropped":10,
         "modes_without_figure_code":0}
index.unified counts = {"total":1333,"figures":278,"scenarios":1055,"with_modes":1297}
figures == mode_by_figure_shards: True
```

线上产物 D3 扫描（8 个摘要分片 + 名录 + 人物索引，全量抓取）：

```text
  modes/index-0..7.json / index.unified.json / figures.index.json: D3关键词命中=0  隔离模式code出现=[]
TOTAL D3 hits across published products: 0
```

`meta.json.sources['data/modes_data.json'].sha256 = bf168171af42…`，与两仓当前 `data/modes_data.json` sha256 **相同** —— 线上产物就是当前数据构建的。

### 6.3 发布仓 ahead

```bash
$ cd /opt/data/release/Protreptic-publish && git status -sb && git fetch -q origin && git status -sb
## main...origin/main
ahead_count=0
behind=0
```

### 6.4 四个 workflow 最新 run（逐个贴 job）

```text
workflow='Deploy to GitHub Pages' run=77 head=ad30ff8 event=push conclusion=success jobs=2
    - 构建 SPA + 文档站 :: success
    - 部署 :: success
workflow='Protreptic CI/CD'       run=87 head=2db123a event=push conclusion=success jobs=6
    - Test (Python + TypeScript) :: success / Build API Docker Image :: success /
      Build Web Docker Image :: success / Notify :: success / Deploy to Staging :: skipped /
      Deploy to Production :: skipped
workflow='Quality Gate'           run=65 head=ba624d3 event=workflow_run conclusion=success jobs=3
    - Lighthouse 预算门 / 线上死链检测 / 数据校验 :: success
workflow='CI'                     run=87 head=2db123a event=push conclusion=success jobs=1
    - markdown-lint :: success
```

### 6.5 硬纪律 #4/#5（适用性）

```bash
$ git log --oneline 11cdbdce..HEAD -- web/    -> 空
web changes: 0 个提交
```

QA5 之后无任何前端改动 -> `cd web && VITE_DATA_MODE=static npm run build` 本次**不适用**；数据文件未变（`data/modes_data.json` sha256 与线上 `meta.json.sources` 相同），构建顺序纪律亦无触发场景。

判定 **PASS**。

## 7. 复验未通过清单（阻塞项）

1. **W1 · D3 源库未归零且豁免未落地**：`data/modes_data.json` 仍有 6 条模式 `source_chapter` 命中 D3 正则（全挂在 H-P23F-001 / P25F / P26F 名下）；`credibility_framework.md` 写的「gate 跳过 quarantined figure」在 `tools/credibility_gate.py` 里**不存在**（自造样本证明豁免名单仍被报 D3）。二选一：真清 0，或改代码实现豁免。
2. **W3 · gate 未接入任何 CI（线上仓 0/4）**，且照抄工作仓写法接入会因 **D1 硬 FAIL（源库必然 533 条）** 与 `--negative-test` **exit 1 语义反置**两条同时把 Pages 打红。
3. **W4 · 两仓字节级一致未达**：全量比对 44/2363 共同 tracked 文件 hash 不同（含 `.github/workflows/pages.yml`），另有 1469 / 678 单侧文件。点名的 7 个数据/工具文件已一致，但「字节级一致」作为纪律项未闭环。
4. **W2 · 审计清单陈旧且无自检**：`findings.json` 的 evidence 仍引用已被 W1 删除的原文（M-P23F-002）、summary 计数（D1=50 / D3=19 / total_modes_count=2838）与源库现状（60 / 6 / 2888）不符、H-SX-001 只列 3/10，且**全仓无任何脚本消费/校验该文件**（注入不存在 code 无人报错）。
5. **过程性风险（非缺陷，需知会）**：本报告结论绑定 `c3da04bb`（工作仓）/ `2db123a`（发布仓）/ `2026-09-19 19:12 CST` 的线上快照；报告本身位于 `docs/qa/`，其推送会触发一次新的 Pages run。
