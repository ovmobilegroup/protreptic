# Phase37-X1 交付报告：D3 源库最终收口（豁免口径落地到 gate）

- 卡：`t_d16e6ee2`（工人 san-martin）
- 工作仓 `/opt/data/workspace/Protreptic` / 发布仓 `/opt/data/release/Protreptic-publish`
- 快照时间：`Sat Sep 19 22:31 CST 2026`
- 上游依据：发布仓 `docs/qa/phase36_acceptance.md`（QA6 终审，逐项原始命令与输出）
- 任务书二选一 → **选 B：豁免口径落地到 gate**（理由见 §3。**不改源库数据**）

## 1. 结论

| # | 验收项 | 判定 | 依据 |
|---|---|---|---|
| 1 | 全库 D3 计数（gate 口径） | **PASS：0 条硬失败** | §4.1 |
| 2 | 豁免名单 + 依据精确列出 | **PASS：43 条模式 / 6 个 D1 隔离 figure** | §2 / §4.1 |
| 3 | 自造样本 A：豁免 code 不报 D3 | **PASS** | §4.3 例 A |
| 4 | 自造样本 B：非豁免 code 必报 D3 | **PASS** | §4.3 例 B |
| 5 | 双仓同步 + push + ahead=0 | **PASS** | §5 |
| 6 | 线上计数 2798 / 278 + 6 个伪人物 URL 404 | **PASS**（数据未改，构建产物字节不变） | §6 |

## 2. D3 现状（更正任务书里的一处数字）

任务书写「船长复查：现为 **2 条**，`M-P23F-001` / `M-P23F-002`」。
实测（正则与 `tools/credibility_gate.py` 的 `D3_PATTERNS` 同源）为 **6 条**，全部挂在 D1 隔离 figure 名下：

| mode_code | figure_code | 命中正则 |
|---|---|---|
| `M-P23F-001` | `H-P23F-001` | `[0-9a-f]{8,}` |
| `M-P23F-002` | `H-P23F-001` | `提交链` |
| `M-P23F-009` | `H-P23F-001` | `[0-9a-f]{8,}` |
| `M-P25F-006` | `P25F` | `[0-9a-f]{8,}` |
| `M-P26F-001` | `P26F` | `[0-9a-f]{8,}` |
| `M-P26F-004` | `P26F` | `[0-9a-f]{8,}` |

公开人物（`figure_code` 不在隔离名单）命中 **0 条** —— 这才是豁免口径要保证的事实。

复跑命令（临时扫描器，正文内联以便 QA 复现）：

```python
# /tmp 下写 d3scan.py 后：python3 d3scan.py data/modes_data.json
import json, re, sys, collections
D3_PATTERNS = [r"sha256", r"[0-9a-f]{8,}", "双镜像", "qa_postmerge", "入库复检",
               "工作树", "提交链", "修复提交", "脚本名", "pipeline", "ci/cd", "github actions"]
def all_modes(data):
    modes = list(data.get("modes") or [])
    for k, v in data.items():
        if isinstance(v, dict) and isinstance(v.get("modes"), list):
            modes += v["modes"]
    return [m for m in modes if isinstance(m, dict)]
data = json.load(open(sys.argv[1], encoding="utf-8"))
hits = []
for m in all_modes(data):
    src = m.get("source_chapter", "")
    srcs = src if isinstance(src, list) else ([src] if isinstance(src, str) else [])
    for s in srcs:
        for p in D3_PATTERNS:
            if re.search(p, str(s), re.IGNORECASE):
                hits.append((m.get("mode_code"), m.get("figure_code"), p))
                break
print("total modes:", len(all_modes(data)))
print("D3 hit modes:", len(hits))
print("figures:", dict(collections.Counter(h[1] for h in hits)))
for h in hits:
    print("  ", h)
```

输出：

```text
total modes: 2888
D3 hit modes: 6
figures: {'H-P23F-001': 3, 'P25F': 1, 'P26F': 2}
   ('M-P23F-001', 'H-P23F-001', '[0-9a-f]{8,}')
   ('M-P23F-002', 'H-P23F-001', '提交链')
   ('M-P23F-009', 'H-P23F-001', '[0-9a-f]{8,}')
   ('M-P25F-006', 'P25F', '[0-9a-f]{8,}')
   ('M-P26F-001', 'P26F', '[0-9a-f]{8,}')
   ('M-P26F-004', 'P26F', '[0-9a-f]{8,}')
```

**持久口径**（不依赖临时脚本）：`tools/credibility_gate.py --no-d3-exemption` 会把这 6 条当硬失败列出/计数。

## 3. 为什么选 B（豁免落地）而不是 A（清源库）

1. `docs/planning/credibility_framework.md` §1 D3 行与 §4 早就写了豁免条款，但 `tools/credibility_gate.py` 里
   `check_d3_pollution(mode)` 没有任何 quarantine 参数（QA6 §2.2 自造样本已证）—— 这是**文档与实现的漂移**，
   选 B 是让实现追上文档，并补上可机检的自测。
2. 这 6 条属 D1 隔离 figure 的**源库留档**（`tools/_quarantine.py` docstring：源数据保留以便复核与回滚）。
   隔离已保证它们不进任何公开产物（QA6 §6.2：线上 8 个摘要分片 + 名录 + 人物索引 D3 命中 0）。
3. 清库不能让 gate 在源库变绿：D1（隔离人物自身）是硬 FAIL，源库必然红（见 §7）。
   所以「清 6 条」只治表，还会抹掉留档。

## 4. 验收：命令 + 原始输出

### 4.1 默认（豁免生效）· 工作仓

```bash
$ cd /opt/data/workspace/Protreptic && python3 tools/credibility_gate.py --data-path data/modes_data.json; echo EXIT=$?
=== CREDIBILITY GATE ===
resolved data path: data/modes_data.json
Total modes checked: 2888
Hard failures (D1/D2/D3/D6): 527
  of which D3 出处污染: 0
Warnings (D4/D5): 17
D3 exemption: on
D3-exempted modes (D1 quarantined figures, not scanned): 43
  by figure: H-P23F-001=9, H-SX-001=10, P24F=6, P25F=5, P26F=7, Phase27Final=6
  whitelist source: tools/_quarantine.py QUARANTINE = ['H-P23F-001', 'H-SX-001', 'P24F', 'P25F', 'P26F', 'Phase27Final']
  basis: credibility_framework.md §1 D3 豁免条款 / §4 豁免逻辑（D1 已隔离记录允许保留源库工程痕迹，以导出期过滤为准）
EXIT=1
```

豁免名册（43 条 mode_code，全部可逐个回查）：

```text
M-P23F-001..010（H-P23F-001，9 条带出处）、M-P24F-001..010（P24F，6 条）、M-P25F-003..008（P25F，5 条）、
M-P26F-001..010（P26F，7 条）、M-P27F-002..009（Phase27Final，6 条）、M393-M402（H-SX-001，10 条）
```

### 4.2 严格模式（`--no-d3-exemption`）：豁免可关，D3 立刻现形

```bash
$ python3 tools/credibility_gate.py --no-d3-exemption --data-path data/modes_data.json | grep "of which D3"
  of which D3 出处污染: 6
```

### 4.3 自造样本（两个方向都验）· `tools/test_credibility_gate.py`

```bash
$ python3 tools/test_credibility_gate.py; echo EXIT=$?
[PASS] A 已隔离 figure 的污染出处不报 D3
[PASS] B 公开 figure 的污染出处必报 D3
[PASS] C --no-d3-exemption 严格模式必报 D3
[PASS] D --negative-test 注入坏样本必 exit 1
[PASS] E 干净公开记录必须 exit 0
[PASS] F 真实源库 D3 计数为 0

6/6 passed
EXIT=0
```

夹具口径（照 QA6 §2.2 的两套夹具固化）：

- 例 A/B：同一段污染出处 `Phase 21 入库与修复提交链（双镜像 sha256 记录：茅以升 96bdd4c4）`，
  分别挂在 `H-P23F-001`（隔离）与 `H-CLEAN-TEST-001`（公开）名下 → 前者不报 D3、后者必报。
- 例 C：同一隔离夹具加 `--no-d3-exemption` → 必报。
- 例 D：`--negative-test` → `[OK] Negative test PASSED` 且 exit 1。
- 例 E：干净公开记录 → exit 0（防误报）。
- 例 F：真实源库跑 gate → `of which D3 出处污染: 0` 且报告豁免面。

### 4.4 发布仓复跑（线上唯一来源）

```bash
$ cd /opt/data/release/Protreptic-publish && python3 tools/credibility_gate.py --data-path data/modes_data.json
resolved data path: data/modes_data.json
Total modes checked: 2888
Hard failures (D1/D2/D3/D6): 527
  of which D3 出处污染: 0
D3-exempted modes (D1 quarantined figures, not scanned): 43

$ python3 tools/test_credibility_gate.py
6/6 passed
```

## 5. 改动与双仓同步（sha256 逐文件相等）

| 文件 | 变化 | sha256（两仓一致） |
|---|---|---|
| `tools/credibility_gate.py` | 新增 `is_d3_exempt()`；`check_d3_pollution(mode, quarantine, apply_exemption)`；`run_gate()` 增加第三个返回值（豁免 mode_code）并在报告里打印豁免面；新增 `--no-d3-exemption` | `45a3082aa9e688eaef3d3d860c555066826a74ef3cde31893b4e14cdc04dea2e` |
| `tools/test_credibility_gate.py`（新） | 6 例自测（豁免不报 / 非豁免必报 / 严格模式 / 负对照 / 误报 / 真实源库） | `6ebed2e7442f1e076d20c2e3d03bdd65fee415a9197bb2ca3b24d309f3c48b65` |
| `docs/planning/credibility_framework.md` | §1 D3 豁免条款改为「以 `tools/_quarantine.py` 为唯一事实来源」（旧名单漏列 `H-SX-001`，已修）；§4 补豁免逻辑 / 可关 / 自测；新增 §4.1 实测 | `c0cf43fbb9ef95f02a6eaea5f5a102142169ff7c840e0e990d224a95448fc774` |

```bash
$ sha256sum tools/credibility_gate.py tools/test_credibility_gate.py docs/planning/credibility_framework.md   # 工作仓
45a3082a...  tools/credibility_gate.py
6ebed2e7...  tools/test_credibility_gate.py
c0cf43fb...  docs/planning/credibility_framework.md
$ cd /opt/data/release/Protreptic-publish && sha256sum tools/credibility_gate.py tools/test_credibility_gate.py docs/planning/credibility_framework.md
45a3082a...  tools/credibility_gate.py
6ebed2e7...  tools/test_credibility_gate.py
c0cf43fb...  docs/planning/credibility_framework.md
```

`data/modes_data.json` **未改**（`sha256=bf168171af42f8148c3adecbbc1a71258522676355357f6466acdcb25f2e61cb`，
与线上 `meta.json.sources['data/modes_data.json'].sha256` 相同）→ 构建链无需重跑，线上产物字节不变。
硬纪律 #4（前端改动 `npm run build`）本卡不适用：`web/` 0 改动。

## 6. 线上复核（改动后）

```bash
$ curl -s -o /tmp/meta.json https://ovmobilegroup.github.io/protreptic/data/meta.json
$ python3 /tmp/meta_show.py        # 读取 /tmp/meta.json 的 counts / sources
counts = {"figures":1057,"figure_shards":1057,"mode_summaries":2858,"mode_summaries_published":2798,
          "modes_quarantined":60,"mode_index_shards":8,"mode_by_figure_shards":278,
          "modes_raw":2868,"modes_deduped":2858,"modes_duplicates_dropped":0,
          "modes_empty_mode_code_dropped":10,"modes_without_figure_code":0}
sources['data/modes_data.json'].sha256 = bf168171af42f8148c3adecbbc1a71258522676355357f6466acdcb25f2e61cb

# 8 个摘要分片条目数求和
index-0..7.json entries = 379 + 336 + 340 + 340 + 345 + 350 + 355 + 353 = 2798

$ for u in H-P23F-001 P24F P25F P26F Phase27Final H-SX-001 H-WYM-001; do
    curl -s -o /dev/null -w "$u -> %{http_code}\n" "https://ovmobilegroup.github.io/protreptic/minds/$u/"; done
H-P23F-001 -> 404
P24F -> 404
P25F -> 404
P26F -> 404
Phase27Final -> 404
H-SX-001 -> 404
H-WYM-001 -> 200     # 真人物仍 200，排除「/minds 整体塌掉」
```

发布仓 push 后 `git status -sb` 无 `[ahead N]`。

## 7. 边界声明（不许谎报）

本豁免**只覆盖 D3**。源库硬失败 527 条的构成（`run_gate()` 实算）：

| 类别 | 条数 | 处置归属 |
|---|---|---|
| D1 伪人物（隔离 figure 自身） | 60 | 存量债务，走 Phase37-X3 的「存量不阻断、新增必红」两档模式 |
| D2 伪造出处（《苏咸子》型，命中 gate 已知伪书目） | 9 | 同上（X2 在补 findings 清单与自检脚本） |
| D3 出处污染 | **0** | 本卡 |
| D6 悬空引用 | 458 | 存量债务，同上 |

因此：**源库上 gate 仍 exit 1（527 条），这是存量债务，不是本卡的口径问题**。
把豁免读成「gate 现在在源库能过」是错的。本卡只承诺并证明：**D3 在公开人物面上为 0，且豁免可机检、可关闭、豁免面如实公布**。

## 8. hotspot 声明

`tools/credibility_gate.py` 是 **X1（本卡）与 X3（两档模式 / 基线冻结）共同编辑的同一文件**。
本卡提交时该文件里已含 X3 的 `--legacy-report` / `--hard-fail` / `--write-baseline` / `resolve_repo_root()` /
`load_quarantine(root)` 管道。后续在同一文件上的改动请**不要回退** `is_d3_exempt()`、豁免面打印
（`D3-exempted modes ...`）与 `--no-d3-exemption`；它们是本卡的可机检产物，`tools/test_credibility_gate.py` 会守住。

## 9. 复跑入口（一句话）

```bash
cd /opt/data/workspace/Protreptic
python3 tools/test_credibility_gate.py                                  # 6/6 应过
python3 tools/credibility_gate.py --data-path data/modes_data.json      # of which D3 出处污染: 0
python3 tools/credibility_gate.py --no-d3-exemption --data-path data/modes_data.json   # 严格模式: 6
```
