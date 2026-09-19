# Phase37-QA7 终审：按更正后的标准独立复验（自造样本，不信自述）

- 卡：`t_130ab852`（espinosa）。上游父卡：`t_376fb4aa`（Phase37-X4）、`t_c39a6828`（Phase37-X2）。
- 同时复核 `t_d16e6ee2`（X1）、`t_b74ae78b`（X3）、`t_fd9210a5`（X5）的交付物（报告 + 产物 + CI）。
- 必读依据：发布仓 `docs/qa/phase36_acceptance.md`（QA6 终审，逐项原始命令与输出）。
- 方法：**自己跑命令、只贴原始输出、自造样本**；任何结论都能用本报告里的命令原样复现。不采信工人自述。

复验快照（本报告判定基准，单一时间点）：

| 项 | 值 |
| --- | --- |
| 本地时间 | `Sun Sep 20 00:19:09 CST 2026` |
| 工作仓 `/opt/data/workspace/Protreptic` | `master` @ `e665c756`（`git status -sb` 干净：`## master`） |
| 发布仓 `/opt/data/release/Protreptic-publish` | `main` @ `7eeb56a` == `origin/main`（无 `[ahead N]`） |
| 线上 | `https://ovmobilegroup.github.io/protreptic`（`data/meta.json` 200，见 3.5） |
| 关键文件 sha256（两仓逐字节相同） | `data/modes_data.json bf168171af42f814…`、`data/audit/findings.json 726be6f4171d08ed…`、`data/audit/credibility_baseline.json ed7c3a56b7ebbe64…`、`tools/credibility_gate.py 45a3082aa9e688ea…`、`tools/verify_findings.py a5ed85852cbba2a2…`、`tools/check_repo_parity.py ddda6dede86b5d01…`、`docs/planning/credibility_framework.md dfe2b0e64a1384a0…` |

说明：本卡执行了 **CI 红态自证**（向发布仓 `main` 推入 1 条自造新增 D3 坏样本，验证 CI 真变红，随后移除）。注入与移除的提交是 `a588c4a` / `7eeb56a`，两者之间数据文件临时偏离工作仓，已复原（见 3.3；`data/modes_data.json` 现已回到 `bf168171af42…`，机检 `exit 0`）。

## 1. 终审结论：不可发布（FAIL）

| # | 复验项 | 判定 | 依据 |
| --- | --- | --- | --- |
| 1 | X1 · D3 源库（归零 / 豁免名录精确 + 白名单两个方向） | **PASS** | 3.1：公开人物命中 **0**；6 条命中全在 `tools/_quarantine.py` 的 QUARANTINE 内；自造夹具证明「豁免不报 / 非豁免必报 / 严格模式必报」 |
| 2 | X2 · `findings.json` 自检（塞坏 code 必 red + H-SX-001 全 10 条） | **PASS** | 3.2：注入不存在 code / figure_code / 坏锚点 / 缺字段 **四种注入全 exit 1**；我自己 grep 出源库《苏咸子》10 条，与 findings 的 D2 十条同集合；自测 8/8 |
| 3 | X3 · CI 门（自造新增 D3 → CI 真红；存量态真绿；发布仓确有门） | **PASS** | 3.3：`a588c4a` → Pages 门步骤 failure、其后 24 步 + 部署全 skipped；`7eeb56a` → Pages success、部署 success；发布仓 `pages.yml` 7 处 / `ci-cd.yml` 8 处命中，工作仓 `ci-cd.yml` 0 处 |
| 4 | X4 · 两仓一致（新标准 = 构建图口径） | **PASS** | 3.4：`check_repo_parity.py` 两仓 `[OK] 零差异：1308 个构建图文件`；边界自证 exit 2、内容漂移 exit 1、缺一侧 exit 1、复原 exit 0；排除项我独立复核（`data/intl_figures/**` 无任何读者等） |
| 5 | 全局（6 伪人物 404 / 计数自洽 / ahead=0 / **CI run 全 success**） | **FAIL** | 3.5：前三条 PASS（6/6 404、分片与 by-figure 双向求和均 2798、ahead=0），但 **`CI`（markdown-lint）自 `d644470` 起每个 head 都是 failure**，当前 head `7eeb56a` 仍是 failure，且**归 Phase37-X2 的交付文件** |

判定逻辑：本卡「任一硬门不过即 FAIL」。1–4 全过；第 5 项里「CI 全绿」这一条**不成立且可复现**，故终审 **不可发布**。

**唯一阻塞是什么（不要误读成整套体系有问题）**：`docs/qa/phase37_x2_evidence.md` 的两行 markdown 格式错误（MD038 / MD009），本地用与 CI 同版本工具逐字复现（3.5.4）。修掉这 2 行，`CI` workflow 立即复绿，本卡即可转为「可发布」。其余 4 项与线上站点均无损（Pages 构建全绿、6 个伪人物深链仍 404）。

## 2. 对船长更正口径的表态

**认同。** 本卡明确写出：Phase36-W4 的「两仓 2363 个 tracked 文件全字节一致」是**判错了口径**；开发仓与发布仓是同一仓库的两条分支，`Dockerfile.web` / `api/**` / `.github/workflows/*` / 部分 `docs/*` / 根目录遗留副本本就按角色不同，不是数据漂移。项目原本的纪律只针对 **`data/` 与线上部署产物**。

本阶段起我采用的验收口径 = X4 在 `docs/planning/credibility_framework.md` 第 9 节写下的那一条：

> 凡**进入站点构建图或线上站点**的文件，两仓必须逐字节一致（sha256）。

并且我做了**独立判断**（不是照抄 X4 的结论）：边界不是一张口头清单，它跟着发布仓 `pages.yml` 走 —— 我往假发布仓的 workflow 里加一个构建步骤，机检立刻 `exit 2` 点名未纳入的步骤（3.4.3）；排除项里唯一有争议的 `data/intl_figures/**`（637 个文件只在发布仓），我自己 grep 确认 `tools/` + `.github/` + `web/src/` + `data/` + `mkdocs.pages.yml` **除机检脚本自身外 0 命中**，即没有任何构建步骤/前端读它，判定「不进站点」站得住（3.4.4）。

一句提醒：第 9 节正文写的「两仓各 **1307** 个构建图文件」比实测少 1（实测 **1308**，X4 报告自己的同步后输出也是 1308）。属文档陈旧 1 个数，不影响判定，建议顺手改成 1308。

## 3. 逐项复验（命令 + 原始输出）

### 3.1 X1 · D3 源库：归零还是豁免？豁免名录是否精确？gate 白名单两个方向

#### 3.1.1 全库源库扫描（我自己的扫描器，不复用 gate 的代码路径）

```bash
$ cat > /tmp/qa7/d3scan.py <<'PYEOF'
import json, re, sys, collections
D3_PATTERNS = [r"sha256", r"[0-9a-f]{8,}", r"双镜像", r"qa_postmerge", r"入库复检",
               r"工作树", r"提交链", r"修复提交", r"脚本名", r"pipeline", r"ci/cd", r"github actions"]
def all_modes(data):
    modes = list(data.get("modes") or [])
    for k, v in data.items():
        if isinstance(v, dict) and isinstance(v.get("modes"), list):
            modes += v["modes"]
    return [m for m in modes if isinstance(m, dict)]
data = json.load(open(sys.argv[1], encoding="utf-8"))
QUAR = set(["H-SX-001","H-P23F-001","P24F","P25F","P26F","Phase27Final"])
hits = []
for m in all_modes(data):
    src = m.get("source_chapter", "")
    srcs = src if isinstance(src, list) else ([src] if isinstance(src, str) else [])
    for s in srcs:
        for p in D3_PATTERNS:
            if re.search(p, str(s), re.IGNORECASE):
                hits.append((m.get("mode_code"), m.get("figure_code"), p)); break
print("total modes:", len(all_modes(data)))
print("D3 hit modes:", len(hits))
print("figures:", dict(collections.Counter(h[1] for h in hits)))
print("hits on NON-exempt figures:", len([h for h in hits if str(h[1]) not in QUAR]))
for h in sorted(hits): print("  ", h)
PYEOF
$ python3 /tmp/qa7/d3scan.py /opt/data/workspace/Protreptic/data/modes_data.json
total modes: 2888
D3 hit modes: 6
figures: {'H-P23F-001': 3, 'P25F': 1, 'P26F': 2}
hits on NON-exempt figures: 0
   ('M-P23F-001', 'H-P23F-001', '[0-9a-f]{8,}')
   ('M-P23F-002', 'H-P23F-001', '提交链')
   ('M-P23F-009', 'H-P23F-001', '[0-9a-f]{8,}')
   ('M-P25F-006', 'P25F', '[0-9a-f]{8,}')
   ('M-P26F-001', 'P26F', '[0-9a-f]{8,}')
   ('M-P26F-004', 'P26F', '[0-9a-f]{8,}')
```

结论：**公开人物面 0 条**（这才是豁免口径要保证的事实）；6 条全部属于 D1 已隔离 figure。

#### 3.1.2 用 gate 自己跑（默认档 / 严格档 / 两档）

```bash
$ cd /opt/data/workspace/Protreptic
$ python3 tools/credibility_gate.py --data-path data/modes_data.json | head -14
=== CREDIBILITY GATE ===
resolved data path: data/modes_data.json
Total modes checked: 2888
Hard failures (D1/D2/D3/D6): 527
  of which D3 出处污染: 0
Warnings (D4/D5): 17
D3 exemption: on
D3-exempted modes (D1 quarantined figures, not scanned): 43
  exempted mode_codes: M-P23F-001, …, M402
  by figure: H-P23F-001=9, H-SX-001=10, P24F=6, P25F=5, P26F=7, Phase27Final=6
  whitelist source: tools/_quarantine.py QUARANTINE = ['H-P23F-001', 'H-SX-001', 'P24F', 'P25F', 'P26F', 'Phase27Final']

$ python3 tools/credibility_gate.py --no-d3-exemption --data-path data/modes_data.json | grep -E "Hard failures|of which D3"
Hard failures (D1/D2/D3/D6): 533
  of which D3 出处污染: 6

$ python3 tools/credibility_gate.py --hard-fail --data-path data/modes_data.json | tail -3
[OK] hard-fail: 无新增硬失败（存量 527 条已冻结）-> exit 0
```

豁免面是**如实公布**的（打印了 43 个 mode_code 与 6 个 figure），不是静默跳过；严格档能把 6 条 D3 重新现形（豁免可关）。

#### 3.1.3 自造夹具：白名单两个方向 + 严格方向（不复用 X1 的自测脚本）

我自己造了一个独立夹具仓 `/tmp/qa7/fx1`（自己的 `tools/_quarantine.py`，只隔离 `H-QA7-QUAR`；自己的两条模式数据），把「同一段污染出处」分别挂在隔离人物与公开人物名下：

```bash
$ cd /tmp/qa7/fx1 && python3 tools/credibility_gate.py --data-path data/modes_data.json
=== CREDIBILITY GATE ===
Total modes checked: 2
Hard failures (D1/D2/D3/D6): 2
  of which D3 出处污染: 1
D3 exemption: on
D3-exempted modes (D1 quarantined figures, not scanned): 1
  exempted mode_codes: M-QA7-EXEMPT-001
  by figure: H-QA7-QUAR=1
  whitelist source: tools/_quarantine.py QUARANTINE = ['H-QA7-QUAR']

--- HARD FAILURES (blocking) ---
  ::error::[M-QA7-EXEMPT-001] D1 伪人物: figure_code=H-QA7-QUAR 在隔离名单中
  ::error::[M-QA7-PUBLIC-001] D3 出处污染: source_chapter 匹配污染模式 'sha256' -> Phase 21 入库与修复提交链（双镜像 sha256 记录：茅以升 96bdd4c4）
[FAIL] Gate failed with 2 hard failures
EXIT=1

$ python3 tools/credibility_gate.py --no-d3-exemption --data-path data/modes_data.json | grep -E "of which D3|exemption"
  of which D3 出处污染: 2
D3 exemption: off (--no-d3-exemption)
```

四个方向全部成立：**隔离项不报 D3 / 公开项必报 D3 / 严格档两项都报 / 白名单取自夹具自己的仓**（打印的 `QUARANTINE = ['H-QA7-QUAR']` 证明 `--data-path` 的「数据 + 白名单同仓」语义真的生效，不是拿真仓名单判夹具）。

X1 自带的机检我也跑了（防回流守护在库）：

```bash
$ python3 tools/test_credibility_gate.py
[PASS] A 已隔离 figure 的污染出处不报 D3
[PASS] B 公开 figure 的污染出处必报 D3
[PASS] C --no-d3-exemption 严格模式必报 D3
[PASS] D --negative-test 注入坏样本必 exit 1
[PASS] E 干净公开记录必须 exit 0
[PASS] F 真实源库 D3 计数为 0
6/6 passed   EXIT=0
$ python3 tools/test_credibility_gate_modes.py
[PASS] 1..7 全过
7/7 passed   EXIT=0
```

判定 **PASS**。（附带说明：源库上 gate 仍 `exit 1` / 527 条硬失败 —— 那是 D1=60 / D2=9 / D6=458 的**存量债务**，由 X3 的两档门「存量冻结、新增即拦」承接；本项只承诺并证明「D3 公开面为 0、豁免精确、可机检、可关闭、豁免面如实公布」。）

### 3.2 X2 · findings.json：自检脚本真的会拦吗？H-SX-001 真的列全 10 条吗？

#### 3.2.1 干净态与自测

```bash
$ cd /opt/data/workspace/Protreptic && python3 tools/verify_findings.py --hard-fail --data-path data/modes_data.json
mode: hard-fail
resolved findings path: /opt/data/workspace/Protreptic/data/audit/findings.json (exists=True)
resolved baseline path: /opt/data/workspace/Protreptic/data/audit/findings_baseline.json (exists=True)
hard failures on this findings file: 0
baseline frozen at 2026-09-19T15:20:44+00:00 (total=0, fingerprints=0, A=0 B=0 C=0 D=0)
（存量 0 条 / 新增 0 条 / 计数过期 0 条）
[OK] hard-fail: 无新增硬失败（存量 0 条已冻结）-> exit 0
HARDFAIL_EXIT=0

$ python3 tools/test_verify_findings_modes.py
[PASS] 1..8 全过 -> 8/8 passed   EXIT=0
```

注意：`findings_baseline.json` 现在是**空基线（0 条）**，脚本自己打印了这一点（`total=0`），没有假装有存量；基线缺失时 `exit 2`（fail-closed）也由自测第 5 项守着。

#### 3.2.2 自造注入（我自己写注入器，四种破坏各打一次）

```bash
$ cd /opt/data/workspace/Protreptic && python3 /tmp/qa7/inject_test.py
=== case B: 不存在 mode_code ===        exit = 1
     ::error::NEW B|M-QA7-BAD-CODE-001|mode_code=M-QA7-BAD-CODE-001 | B: [M-QA7-BAD-CODE-001] mode_code 'M-QA7-BAD-CODE-001' does not exist in the source library
     [FAIL] hard-fail: 1 条新增硬失败（基线外）-> exit 1（存量 0 条已冻结）
=== case B2: 不存在 figure_code exit = 1
     ::error::NEW B|M-P23F-001|figure_code=H-QA7-NO-SUCH-FIGURE | figure_code 'H-QA7-NO-SUCH-FIGURE' does not exist in the source library
=== case C: 锚点不可定位 exit = 1
     ::error::NEW C|[M-P23F-001] anchor not found verbatim in modes_data.json: 'QA7-ANCHOR-NOT-IN-LIBRARY-XYZ'
     ::error::NEW C|[M-P23F-001] anchor is not quoted inside evidence: 'QA7-ANCHOR-NOT-IN-LIBRARY-XYZ'
     ::error::NEW C|[M-P23F-001] D1 anchor must equal the record figure_code ('H-P23F-001')
     [FAIL] hard-fail: 3 条新增硬失败（基线外）-> exit 1
=== case A: 缺 evidence 字段 exit = 1
     ::error::NEW A|findings[0] (M-P23F-001) missing field 'evidence'
     [FAIL] hard-fail: 2 条新增硬失败（基线外）-> exit 1
```

**「塞坏 code → exit 1」成立**，而且我把「不存在 figure_code / 锚点不可回源 / 结构缺字段」也各打了一次，全部 exit 1。

「计数过期」（E 类）是否真的只警告？我**不篡改 findings 的 summary**（那样会同时触发 D 自洽硬失败，测不出 E），改为**换一份现算不同的库**：

```bash
$ python3 /tmp/qa7/e_test.py      # 复制库并追加 1 条隔离 figure 模式，使现算 D1=61 / total=134
exit = 0
   --- 计数过期（警告，不阻断）: 2 条 ---
     ::warning::计数过期(E) summary.D1_pseudo_figure = 60 而现算 modes_stale.json 得 61 —— 刷新：python3 tools/build_audit_findings.py --write
     ::warning::计数过期(E) summary.total = 133 而现算得 134 —— 刷新：python3 tools/build_audit_findings.py --write
   [OK] hard-fail: 无新增硬失败（存量 0 条已冻结）-> exit 0
```

E 确实**只警告、不影响退出码** —— X5 的归属决策（坏数据归 gate、清单新鲜度归人）在行为上成立。

#### 3.2.3 H-SX-001 是否真列全 10 条（我自己 grep 源库对账）

```bash
$ python3 /tmp/qa7/findings_check3.py
条目数: 133 by defect: {'D1_pseudo_figure': 60, 'D2_fabricated_source': 10, 'D3_source_contamination': 6, 'D4_quote_without_source': 17, 'D6_orphan_reference': 40}

D2 rows: 10
   M393 H-SX-001 | 《苏咸子·权变篇》 | anchor= 《苏咸子·权变篇》
   M394 H-SX-001 | 《苏咸子·纵横篇》
   M395 H-SX-001 | 《苏咸子·言术篇》
   M396 H-SX-001 | 《苏咸子·权变篇》
   M397 H-SX-001 | 《苏咸子·虚实篇》
   M398 H-SX-001 | 《苏咸子·利益篇》
   M399 H-SX-001 | 《苏咸子·情报篇》
   M400 H-SX-001 | 《苏咸子·主动篇》
   M401 H-SX-001 | 《苏咸子·合纵篇》
   M402 H-SX-001 | 《苏咸子·时势篇》

D2 codes sorted: ['M393','M394','M395','M396','M397','M398','M399','M400','M401','M402']
expected M393..M402: True
源库《苏咸子》codes: ['M393',…,'M402']  |  findings D2 == 源库苏咸子: True

summary 对照: D1 60/60, D2 10/10, D3 6/6, D4 17/17, D6 40/40, total 133/133
```

（源库侧独立复核：`grep -o "《苏咸子[^》]*》" data/modes_data.json | sort | uniq -c` 共 10 处，`《苏咸子·权变篇》` 出现 2 次，合计 10 条。）

判定 **PASS**。另注：条目里用的 defect 名是 `D4_quote_without_source`，summary 的键是 `D4_empty_quote` —— 这不是漏洞，`verify_findings.py` 里有显式映射表 `SUMMARY_KEYS = {"D4_empty_quote": "D4_quote_without_source", …}`，D 自洽检查按映射比对，实测通过。

### 3.3 X3/X5 · CI 门：发布仓真有门吗？自造新增 D3 真能让 CI 变红吗？存量态真绿吗？

#### 3.3.1 发布仓 workflow 确有 gate 调用（0/4 的 QA6 旧账）

```bash
$ cd /opt/data/release/Protreptic-publish
$ for w in pages.yml ci-cd.yml quality-gate.yml markdown-lint.yml; do echo "PUB $w: $(grep -c 'credibility_gate\|verify_source_links\|verify_findings' .github/workflows/$w) 命中"; done
PUB pages.yml: 7 命中
PUB ci-cd.yml: 8 命中
PUB quality-gate.yml: 0 命中
PUB markdown-lint.yml: 0 命中

$ cd /opt/data/workspace/Protreptic
$ for w in pages.yml ci-cd.yml quality-gate.yml markdown-lint.yml; do echo "WS  $w: $(grep -c 'credibility_gate\|verify_source_links\|verify_findings' .github/workflows/$w) 命中"; done
WS  pages.yml: 6 命中
WS  ci-cd.yml: 0 命中
WS  quality-gate.yml: 0 命中
WS  markdown-lint.yml: 0 命中
```

**门确实在发布仓（线上唯一来源），不是只挂在工作仓**。发布仓 `pages.yml` 的 4 步门在构建链**之前**（第 106–117 行），`ci-cd.yml` 的 test job 另有门 + 负对照自测 + findings 两档。quality-gate / markdown-lint 不接门是**有理由的不接**：前者判线上产物，后者判 markdown 格式。

#### 3.3.2 存量态：本地 gate 与 findings 都应 exit 0

```bash
$ cd /opt/data/release/Protreptic-publish
$ sha256sum data/modes_data.json
bf168171af42f8148c3adecbbc1a71258522676355357f6466acdcb25f2e61cb  data/modes_data.json
$ python3 tools/credibility_gate.py --hard-fail --data-path data/modes_data.json | tail -2
[OK] hard-fail: 无新增硬失败（存量 527 条已冻结）-> exit 0
```

#### 3.3.3 自造 1 条新增 D3 → 推上发布仓 main（commit `a588c4a`），验证 CI 真变红

我造的不是 4 字段的最小样本，而是**形态合法的完整记录**（复制一条 29 字段的公开人物模式，只改 `id` / `mode_code` / `name_zh` / `name_en` / `source_chapter`），这样能**把红态归因到门本身**，而不是归因到「样本太瘦导致导出脚本崩」。

```bash
$ git log --oneline -1
a588c4a QA37-QA7 注入 1 条新增 D3 坏样本（M-QA37-QA7-BAD-001，仅用于终审 CI 红态自证，随后移除）
$ git push origin main
   1943a9f..a588c4a  main -> main

$ python3 tools/credibility_gate.py --hard-fail --data-path data/modes_data.json | tail -4   # 本地预演
--- 新增（基线外，必拦）: 1 条 ---
  ::error::NEW M-QA37-QA7-BAD-001|D3|sha256 | [M-QA37-QA7-BAD-001] D3 出处污染: source_chapter 匹配污染模式 'sha256' -> Phase 21 入库与修复提交链（双镜像 sha256 记录：茅以升 96bdd4c4）
[FAIL] hard-fail: 1 条新增硬失败（基线外）-> exit 1（存量 527 条已冻结）
```

真实 CI（GitHub Actions，`gh api` 读回，run id / head / 结论）：

```text
35453595990 Deploy to GitHub Pages  a588c4a  failure
35453595975 Protreptic CI/CD        a588c4a  failure
35453595960 CI (markdown-lint)      a588c4a  failure   <- 存量红，见 3.5.4
35453628608 Quality Gate            a588c4a  failure   <- 连带：注入样本改了现算条数 2859 != 2858
```

Pages run `35453595990` 的**逐步**结论（原样）：

```text
JOB 构建 SPA + 文档站 completed/failure
   5. 可信度门 · 存量清单（不阻断） -> success
   6. 可信度门 · 新增违规必红 -> failure        <== 门在这里断链
   7. 链接源核验 · 存量清单（不阻断） -> success
   8. 链接源核验 · 新增坏链必红 -> success
   9. 重建 figures 数据库 -> skipped
  10. 构建静态数据分片 -> skipped
  …（11–30 全部 skipped：SPA 构建 / 文档站 / 合并产物断言）
  31. Setup Pages -> skipped
  32. Upload Pages artifact -> skipped
JOB 部署 completed/skipped                      <== 坏数据没有上线
```

门步骤的关键日志（`gh run view 35453595990 --log`，原样）：

```text
构建 SPA + 文档站  可信度门 · 新增违规必红   hard failures on this dataset: 528
构建 SPA + 文档站  可信度门 · 新增违规必红   --- 存量（基线内，冻结）: 527 条 [D1=60 D2=9 D3=0 D6=458] ---
构建 SPA + 文档站  可信度门 · 新增违规必红   ##[error]NEW M-QA37-QA7-BAD-001|D3|sha256 | [M-QA37-QA7-BAD-001] D3 出处污染: source_chapter 匹配污染模式 'sha256' -> Phase 21 入库与修复提交链（双镜像 sha256 记录：茅以升 96bdd4c4）
构建 SPA + 文档站  可信度门 · 新增违规必红   [FAIL] hard-fail: 1 条新增硬失败（基线外）-> exit 1（存量 527 条已冻结）
```

`ci-cd` run `35453595975` 的 `Test (Python + TypeScript)` 步骤序列（原样）：第 4 步「可信度门 · 新增违规必红」failure，其后 5–15 步（链接核验、负对照自测、findings 两档自检、Python 测试、TS 类型检查…）**全部 skipped**，`Build */Deploy *` job 全 skipped。

**结论：门真的有牙，而且是「坏数据上不了线」（部署 job skipped），不是「红了但照样发」。**

#### 3.3.4 移除注入后复绿（commit `7eeb56a`）

```bash
$ git checkout 1943a9f -- data/modes_data.json && sha256sum data/modes_data.json
bf168171af42f8148c3adecbbc1a71258522676355357f6466acdcb25f2e61cb  data/modes_data.json
$ git commit -m "QA37-QA7 移除注入的坏样本，恢复存量基线态（预期 CI 复绿）" && git push origin main
   a588c4a..7eeb56a  main -> main
$ git status -sb
## main...origin/main          # 无 [ahead N]
```

真实 CI（head `7eeb56a`）：

```text
35453736462 Deploy to GitHub Pages  7eeb56a  success   （构建 job 36/36 success + 部署 job 3/3 success）
35453994796 Quality Gate            7eeb56a  success
35453736507 Protreptic CI/CD        7eeb56a  Test (Python + TypeScript) job success（workflow 其余 job：Build Web Docker success；Build API Docker 仍在 in_progress，见 3.5.5）
35453736476 CI (markdown-lint)      7eeb56a  failure   <- 存量红，唯一未清项
```

红→绿闭环成立（`a588c4a` 红 → `7eeb56a` 绿），且**线上未被污染**：注入期间 Pages 部署 job skipped，移除后线上 `data/meta.json` 200、6 个伪人物深链仍 404（3.5.1）。

判定 **PASS**。

### 3.4 X4 · 两仓一致性（新标准）：机检复核 + 我对边界的独立判断

#### 3.4.1 两个方向各跑一次（脚本在各自仓内都是同一份字节）

```bash
$ cd /opt/data/workspace/Protreptic && python3 tools/check_repo_parity.py
[boundary] pages.yml 构建步骤 16 个 / paths 触发器 30 条 —— 均已被清单覆盖（边界自检通过）
[boundary] 纳入边界：workspace 1308 / publish 1308；排除：workspace 27 / publish 677
[OK] 零差异：1308 个构建图文件两仓逐字节一致（sha256）
EXIT=0

$ cd /opt/data/release/Protreptic-publish && python3 tools/check_repo_parity.py --workspace /opt/data/workspace/Protreptic
[OK] 零差异：1308 个构建图文件两仓逐字节一致（sha256）      EXIT=0
```

（口径注：上面两个数字是本报告入库**之前**的实测值；本报告自身也是构建图文件，提交后机检边界变成 **1309 / 1309，仍零差异、exit 0** —— 见 7 节。）

要点：**在发布仓里跑必须显式带 `--workspace`**。不带的话脚本把 workspace 解析成自身，两次跑的是同一个仓（输出里会打印 `workspace = /opt/data/release/Protreptic-publish`），那是**同义反复、不算核验** —— X4 报告 4 节写「发布仓侧同一条命令同样零差异」时没说明这一点，我按显式 `--workspace` 重跑后才认可。

#### 3.4.2 逐文件 sha256（与线上/构建链直接相关的关键文件）

```bash
$ for f in data/modes_data.json data/audit/findings.json data/audit/credibility_baseline.json \
           tools/credibility_gate.py tools/verify_findings.py tools/check_repo_parity.py \
           docs/planning/credibility_framework.md; do …; done
data/modes_data.json                  dev=bf168171af42f814 pub=bf168171af42f814 same
data/audit/findings.json              dev=726be6f4171d08ed pub=726be6f4171d08ed same
data/audit/credibility_baseline.json  dev=ed7c3a56b7ebbe64 pub=ed7c3a56b7ebbe64 same
tools/credibility_gate.py             dev=45a3082aa9e688ea pub=45a3082aa9e688ea same
tools/verify_findings.py              dev=a5ed85852cbba2a2 pub=a5ed85852cbba2a2 same
tools/check_repo_parity.py            dev=ddda6dede86b5d01 pub=ddda6dede86b5d01 same
docs/planning/credibility_framework.md dev=dfe2b0e64a1384a0 pub=dfe2b0e64a1384a0 same
```

#### 3.4.3 检出能力自证（我在一个**一次性克隆**上做，不污染真仓）

```bash
$ git clone --no-hardlinks /opt/data/release/Protreptic-publish /tmp/qa7/fakepub
$ python3 /tmp/qa7/boundary_test.py
[1] 未改动的假仓: 0 [OK] 零差异：1308 个构建图文件两仓逐字节一致（sha256）
[2] pages.yml 多一个构建步骤 -> exit 2
[3] 改边界内 docs/index.md 一行 -> exit 1
      CONTENT_DIFF           docs/index.md
[4] 删掉边界内 docs/_config.yml -> exit 1
      MISSING_IN_PUBLISH     docs/_config.yml
[5] 复原后: 0 [OK] 零差异：1308 个构建图文件两仓逐字节一致（sha256）

$ python3 /tmp/qa7/boundary_test2.py
exit = 2
   [FAIL] 边界过期：pages.yml 有构建步骤不在本清单 → 请更新 tools/check_repo_parity.py
           未纳入: tools/qa7_fake_new_step.py
```

「边界跟着 workflow 走」这一条是**真的**：以后谁往 `pages.yml` 加构建步骤，机检立刻 exit 2 点名。

#### 3.4.4 我对「文件集边界是否合理」的独立判断

不是照抄 X4 的排除清单，我自己从发布仓 `pages.yml` 反查，逐项核了四件事：

1. **`data/intl_figures/**`（637 个，只在发布仓）被排除是否合理？** —— 我自己 grep：

   ```bash
   $ grep -rIl "intl_figures" tools/ .github/ web/src/ data/ mkdocs.pages.yml | grep -v check_repo_parity.py
   （空）
   ```

   除机检脚本自己的排除规则注释外 **0 命中** —— 没有任何构建步骤/前端读它。判定「不进构建图、不上线」，排除合理。（若船长要更严的「数据源留档」口径，处置是单向 `cp -r <publish>/data/intl_figures <workspace>/data/` 并提交，X4 已在报告 6 节列出，未擅自扩大改动面。）

2. **`docs/archive/**`（34 个）被排除是否合理？** —— `mkdocs.pages.yml` 实测有 `exclude_docs: archive/`（第 31–33 行），mkdocs 不构建它。合理。

3. **根目录遗留副本（`modes_data.json` / `scenarios_zh.json` / `code_maps.json` …）不进边界是否合理？** —— 构建脚本读的是 `data/**` 与 `tools/**` 下的同名文件：`tools/build_figures_db.py` 的 `find()` 候选顺序是 `tools/json/scenarios_zh.json` → `tools/scenarios_zh.json`，**根目录副本不在候选里**。合理。

4. **有没有漏掉「进入线上站点」的文件？有没有把角色性差异错误纳入？** —— 边界里**没有** `Dockerfile.*` / `docker-compose.yml` / `api/**` / `.github/**` / `tests/` / `cli_tests/` / `scripts/` / `docs_site/**`（后者是更早的独立文档站工程，`mkdocs.pages.yml` 注释明确不用它，我 grep 确认 `docs_site` 只出现在注释里）。这些正是 QA6 判「44/2363 不一致」的那批角色性差异 —— 新口径把它们请出边界是对的。反向我抽查了根目录非边界但两仓同字节的工具配置（`lighthouserc.json f9c8e853a7bf`、`.markdownlint.json d81862721b6a`、`.markdownlint-cli2.jsonc b66a2e8087ac`、`README.md 4262a8df5a97`），两仓一致，不存在「该纳而未纳」的实际漂移。

判定 **PASS**，并且**明确认同**这个口径（见第 2 节）。

### 3.5 全局：线上 404 / 计数自洽 / ahead / CI 全绿

#### 3.5.1 6 个伪人物 URL（+1 个真人物对照）

```bash
$ for u in H-P23F-001 P24F P25F P26F Phase27Final H-SX-001 H-WYM-001; do printf "%s -> " "$u"; \
    curl -s -o /dev/null -w "%{http_code}\n" --max-time 25 "https://ovmobilegroup.github.io/protreptic/minds/$u/"; done
H-P23F-001 -> 404
P24F -> 404
P25F -> 404
P26F -> 404
Phase27Final -> 404
H-SX-001 -> 404
H-WYM-001 -> 200          # 真人物仍 200，排除「/minds 整体塌掉」
```

**6/6 全 404**，且这一结论在**注入期间与清除后各测一次**（3.3.3 / 3.3.4 之后），均未回退。

#### 3.5.2 线上计数自洽（我自己写的抓取脚本，不复用工人脚本）

```bash
$ python3 /tmp/qa7/online_counts2.py
counts: {"figures":1057,"figure_shards":1057,"mode_summaries":2858,"mode_summaries_published":2798,
         "modes_quarantined":60,"mode_index_shards":8,"mode_by_figure_shards":278,"modes_raw":2868,
         "modes_deduped":2858,"modes_duplicates_dropped":0,"modes_empty_mode_code_dropped":10,
         "modes_without_figure_code":0}
  index-0..7 entries: 379 + 336 + 340 + 340 + 345 + 350 + 355 + 353
sum entries: 2798 | published: 2798 | equal: True
figures.index.json count: 1057 | meta.figures: 1057 | equal: True
index.unified counts: {"total":1333,"figures":278,"scenarios":1055,"with_modes":1297}
meta.sources sha modes_data: bf168171af42f8148c3adecbbc1a71258522676355357f6466acdcb25f2e61cb
meta.generated_at: 2026-09-19T15:47:40+00:00

$ python3 /tmp/qa7/byfig4.py      # modes/by-figure/{figure_code}.json 278 片逐个抓
by-figure 分片数: 278 | 条目合计: 2798 | 期望 2798: True
count 字段与 modes 长度不符的片: []

$ python3 /tmp/qa7/published_scan.py
分片模式条目数: 2798 == published: 2798 True
分片中出现的 figure_code 数: 278 | 隔离 figure 命中: []
隔离 mode_code 命中: []
内容字段 D3 命中（source_chapter/引文/名称）: {}
```

三路自洽：**8 个摘要分片求和 = 278 个 by-figure 分片求和 = `meta.mode_summaries_published` = 2798**；`meta.sources` 的 sha 与两仓当前 `data/modes_data.json` **相同**（线上产物就是当前数据构建的）；**隔离人物/隔离模式在公开分片里 0 出现**。

关于「线上有没有工程痕迹」：我对线上产物做**无差别正则扫描**（不限定字段）共命中 33 处，逐条看过，**全部无害**：

```text
pattern [0-9a-f]{8,}  hits=17   全部落在 data/meta.json 自己的 sha256 校验字段里（例：sources["data/modes_data.json"].sha256 = bf168171…）
pattern sha256        hits=14   同上，是 meta.json 的键名
pattern pipeline      hits=2    两条**合法的英文模式名**：Liturgical-Cycle Pipeline Method / Miracle-Year Parallel-Pipeline Method
```

即：**按内容字段（`source_chapter` / 引文 / 名称）扫描 D3 命中 0**；meta.json 里的哈希是构建清单自身的完整性校验，不属于「出处污染」。QA6 报的「0 命中」按字段口径成立，我的无差别扫描把边界条件也钉死了。

#### 3.5.3 发布仓 ahead

```bash
$ cd /opt/data/release/Protreptic-publish && git fetch -q origin && git status -sb
## main...origin/main
$ git rev-parse --short HEAD; git rev-parse --short origin/main
7eeb56a
7eeb56a
```

**ahead=0 / behind=0**（我的注入与移除两次提交都已推上去，没有把仓库留在本地未推的状态）。

#### 3.5.4 CI run 全 success？**不成立** —— 这是本次终审唯一的 FAIL，且有完整归因

按 workflow 名逐个读回（`gh api .../actions/runs`，head = 当前 `7eeb56a`）：

```text
35453736462 Deploy to GitHub Pages  7eeb56a  success    构建 job 36/36 success + 部署 job 3/3 success
35453994796 Quality Gate            7eeb56a  success
35453736507 Protreptic CI/CD        7eeb56a  Test (Python + TypeScript) success（workflow 未结束，见 3.5.5）
35453736476 CI (markdown-lint)      7eeb56a  failure     <== 不绿
```

`CI` 的失败内容（`gh run view 35453736476 --log-failed`，原样）：

```text
markdown-lint  Linting: 233 file(s)
markdown-lint  Summary: 2 error(s)
markdown-lint  ##[error]docs/qa/phase37_x2_evidence.md:9:16 MD038/no-space-in-code Spaces inside code span elements [Context: "`2026-09-19 22:37:04 `"]
markdown-lint  ##[error]docs/qa/phase37_x2_evidence.md:378:42 MD009/no-trailing-spaces Trailing spaces [Expected: 0 or 2; Actual: 1]
markdown-lint  ##[error]Failed with exit code: 1
```

**归因（我不接受「存量红、与本阶段无关」这一说法）**：我用 API 逐 head 拉了一遍 `CI` 的历史，找到了红的**起点**：

```text
35453243072 1943a9f failure     35452346752 10351a6 failure     35449380462 1f16271 failure
35452800588 271da53 failure     35452191400 3a559ce failure     35449304642 99dd4d7 failure
35452448733 9171dce failure     35451940887 7629f9e failure     35449247908 d644470 failure  <== 第一次红
35452411833 869c86d failure     35451691981 d25d4a7 failure     35449092265 9f95113 success  <== 最后一次绿
                                                                35438661051 2db123a success（QA6 快照 head，绿）
```

```bash
$ cd /opt/data/release/Protreptic-publish && git log --diff-filter=A --format="%h %ci %s" -- docs/qa/phase37_x2_evidence.md
d644470 2026-09-19 22:36:05 +0800 Phase37-X2: findings.json 自检脚本 + 补 H-SX-001 全 10 条 + 计数刷新（发布仓同步）
```

即：**`9f95113` 还绿；`d644470`（Phase37-X2 引入 `docs/qa/phase37_x2_evidence.md`）起，此后每一次 push 的 `CI` 都是红**，两条 error 从头到尾都落在这一个文件上。属**本阶段引入的回归**，不是 Phase36 存量。本地用与 CI 同版本工具逐字复现（不是 CI 环境怪癖）：

```bash
$ cd /opt/data/release/Protreptic-publish && npx --yes markdownlint-cli2@0.11.0 --config .markdownlint.json "docs/qa/phase37_x2_evidence.md"
markdownlint-cli2 v0.11.0 (markdownlint v0.32.1)
Linting: 1 file(s)
Summary: 2 error(s)
docs/qa/phase37_x2_evidence.md:9:16 MD038/no-space-in-code Spaces inside code span elements [Context: "`2026-09-19 22:37:04 `"]
docs/qa/phase37_x2_evidence.md:378:42 MD009/no-trailing-spaces Trailing spaces [Expected: 0 or 2; Actual: 1]

$ sed -n '9p' docs/qa/phase37_x2_evidence.md | cat -A
| local time | `2026-09-19 22:37:04 ` |$
$ awk 'NR==378' docs/qa/phase37_x2_evidence.md | cat -A
Snapshot of this run: 2026-09-19 22:37:04 $          <- 行末一个多余空格
```

**修法（2 行）**：第 9 行把代码 span 内的首尾空格去掉（`2026-09-19 22:37:04`）；第 378 行删掉行末空格。**我没有代改 X2 的证据文档**（原始输出里的空格是证据，第三方不宜代改，沿用 X4 报告 8.5 的处理惯例）—— 该文件属 `docs/qa/**`，属发布仓构建图（`docs/**` → mkdocs），因此**它的 lint 红也直接落在发布链的仓库上**。

#### 3.5.5 一处如实说明：`Protreptic CI/CD` 在 `7eeb56a` 上 workflow 尚未结束

```text
CI/CD 7eeb56a: in_progress
JOB Test (Python + TypeScript)  completed/success     <- 门与自检所在 job，已绿
JOB Build Web Docker Image      completed/success
JOB Build API Docker Image      in_progress           <- 镜像构建较慢，仍在跑
```

本报告判定用的是**门所在的 test job（success）**与 `Pages`（success）；workflow 级结论在我截稿时仍 `in_progress`，不做「全绿」的推测。对照：同一条链在 X5 的 `1943a9f`（存量态）上 `Protreptic CI/CD 35453243048 success`、`Deploy to Pages 35453243025 success` —— 存量态绿是成立的。

#### 3.5.6 补记（提交后回读，覆盖 3.5.5 截稿后的变化）

3.5.5 里 `Protreptic CI/CD` 在 `7eeb56a` 上还 `in_progress`（Build API Docker Image 未跑完）。提交本科报告后再回读一次，事实如下（同一 API，原样）：

```text
35453736507 Protreptic CI/CD       7eeb56a  success    <- 3.5.5 截稿后跑完，仍是 success
35453994796 Quality Gate           7eeb56a  success
35454743787 Deploy to GitHub Pages 1e98705  success    构建 SPA + 文档站 success + 部署 success
35454743774 Protreptic CI/CD       1e98705  success
35454922502 Quality Gate           1e98705  success
35454743793 CI (markdown-lint)     1e98705  failure    Summary: 2 error(s) —— 仍是、且仅是 phase37_x2_evidence.md 的同两条
```

两点值得记下：

1. `1e98705` = 本报告入库后的 head，`CI` 的失败内容**仍是同 2 条**（MD038 `:9:16` + MD009 `:378:42`，全在 `docs/qa/phase37_x2_evidence.md`）—— 反过来证明**本报告自身在 CI 里 0 lint 错误**（本地同版本 `markdownlint-cli2 v0.11.0` 也是 `Summary: 0 error(s)`）。
2. 本报告每次 push 都会触发新一轮 run（`docs/**` 在 `pages.yml` 的 `paths` 内），所以「报告自身的 head」永远晚一轮；判定基准请以 3.5.4 / 3.5.6 里带 run id 的原始结论为准。

结论不变：除 `CI`（markdown-lint）外全绿；`CI` 的红 = 2 行，归 Phase37-X2，修掉即全绿。

## 4. 阻塞项与建议（可执行的通过/驳回意见）

| # | 阻塞项 | 归属 | 处置 |
| --- | --- | --- | --- |
| 1 | `CI`（markdown-lint）自 `d644470` 起持续红，2 条 error 全在 `docs/qa/phase37_x2_evidence.md`（`:9:16` MD038、`:378:42` MD009） | **Phase37-X2（`t_c39a6828`）的交付文件** | 改这 2 行（去掉 code span 内空格 / 去掉行末空格）→ 两仓同步 → push → `CI` 复绿 → 本卡可从「不可发布」翻为「可发布」 |
| 2 | `docs/planning/credibility_framework.md` 第 9.2 节写「两仓各 **1307** 个」，实测 **1308** | X4 文档陈旧 1 个数 | 顺手改成 1308（不构成阻塞） |

其余 4 项硬门**全过**，不需要返工。**驳回理由只有一条**：把「CI run 全 success」当作本卡全局硬门来读的话，它现在不成立；而这条不成立是可以 2 行修掉的，所以别的结论都不该被牵连。

## 5. 附加发现（非本次 4 项硬门，但属公开面欠账，交船长决策）

1. **构建图内的 `docs/**` 仍有本机绝对路径**（X4 报告 8.2 已如实记为「公开面清理欠账」，我复核了量级）：

   ```bash
   $ cd /opt/data/release/Protreptic-publish && grep -rIl "/opt/data/" docs/ | wc -l      # 27 个文件
   $ grep -rIo "/opt/data/[a-z/]*" docs/ | wc -l                                          # 202 处
   $ curl -s -o /dev/null -w "%{http_code}\n" https://ovmobilegroup.github.io/protreptic/docs/architecture/web_p0_architecture/
   200
   ```

   27 个 `docs/*.md`（含历次 QA 报告与 architecture 文档）里的 `/opt/data/workspace…` 路径**已随文档站上线**。两仓一致（非漂移），但它属「公开面不该出现的内部路径」，建议单独开一张清理卡（同时会顺带解决文档站上的内部工程细节外泄）。
2. **`data/intl_figures/**` 637 个文件只在发布仓**：本口径下不进构建图、不上线，无风险；若要「数据源留档」口径需单向补齐（X4 已给出命令）。
3. **`docs/qa/**` 全部会进文档站**（实测 `/docs/qa/phase36_acceptance/`、`/docs/qa/phase37_x2_evidence/` 都 200）：QA 报告里的原始日志、sha256、内部事件 id 属内部审计材料，是否该全线公开，值得船长定一次口径。

## 6. 复跑入口（一句话一条）

```bash
cd /opt/data/workspace/Protreptic
python3 /tmp/qa7/d3scan.py data/modes_data.json                    # D3: 6 条全豁免 / 公开面 0
python3 tools/credibility_gate.py --data-path data/modes_data.json # of which D3 出处污染: 0
python3 tools/credibility_gate.py --no-d3-exemption --data-path data/modes_data.json  # 6
python3 tools/test_credibility_gate.py && python3 tools/test_credibility_gate_modes.py   # 6/6 + 7/7
python3 tools/verify_findings.py --hard-fail --data-path data/modes_data.json            # exit 0
python3 tools/test_verify_findings_modes.py                                              # 8/8
python3 tools/check_repo_parity.py                                                       # 1308 零差异
cd /opt/data/release/Protreptic-publish && python3 tools/check_repo_parity.py --workspace /opt/data/workspace/Protreptic
git status -sb                                                    # 无 [ahead N]
```

## 7. 交付与同步（本卡产物）

| 产物 | 绝对路径 |
| --- | --- |
| 本报告 | `/opt/data/workspace/Protreptic/docs/qa/phase37_acceptance.md` |
| 本报告（发布仓副本） | `/opt/data/release/Protreptic-publish/docs/qa/phase37_acceptance.md` |
| CI 红态自证脚本（临时） | `/tmp/qa7/inject.py`、`/tmp/qa7/inject_test.py`、`/tmp/qa7/e_test.py`、`/tmp/qa7/boundary_test.py`、`/tmp/qa7/d3scan.py` |
| CI 红态自证提交（发布仓） | `a588c4a`（注入，已移除）→ `7eeb56a`（移除，当前 head，`data/modes_data.json` 已回到 `bf168171af42…`） |

同步记录（发布仓 push 后；本报告入库使构建图文件数 1308 → 1309）：

```text
## main...origin/main          # 无 [ahead N]
HEAD == origin/main
data/modes_data.json 两仓 sha 均为 bf168171af42f8148c3adecbbc1a71258522676355357f6466acdcb25f2e61cb
python3 tools/check_repo_parity.py -> [OK] 零差异：1309 个构建图文件两仓逐字节一致（sha256），exit 0
（工作仓与发布仓各跑一次，含 --workspace 显式指向；本报告两仓逐字节一致，用 `sha256sum` 复核相等 —— 本报告不做自指哈希，改一次内容就变）
```

硬纪律适用性：本卡**未改 `web/**`、未改构建脚本、未改数据**（`data/modes_data.json` 仅在自证期间临时注入并已复原），故 `cd web && VITE_DATA_MODE=static npm run build` 不适用；构建顺序纪律（`build_figures_db → export_static_site → build_unified_index → apply_site_counts`）无触发场景。本报告文件本身进入构建图（`docs/**`），因此**两仓同字节同步 + 机检 exit 0** 已按纪律执行。
