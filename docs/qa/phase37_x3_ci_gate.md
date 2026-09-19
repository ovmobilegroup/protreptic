# Phase37-X3 交付报告：CI 接入可信度门两档（存量债务不阻断 + 新增违规必红）

卡：`t_b74ae78b`（acurio）。上游必读：发布仓 `docs/qa/phase36_acceptance.md`（QA6 终审）。
本报告只贴**自己跑出来的原始命令与输出**，不采信任何自述。

| 项 | 值 |
| --- | --- |
| 报告快照 | `2026-09-19 23:05 CST` 量级（CI run 时间为 UTC，见各 run） |
| 工作仓 `master` | `cba921a8`（本地仓，无 remote 分支） |
| 发布仓 `main` | `7d6af41`（= `origin/main`，`ahead=0`，详见 §7） |
| 线上 | 仍是本次门接入后构建并部署的产物（run #1 / #3 部署 job 均 success） |

## 1. 终审结论

**本卡四项验收全部闭环**：

| # | 验收项 | 判定 | 证据 |
| --- | --- | --- | --- |
| 1 | gate 两档（`--legacy-report` / `--hard-fail`，存量基线冻结、新增即拦） | **PASS** | §3、§4；自测 7/7 |
| 2 | gate（含 `verify_source_links.py`）接进发布仓 CI | **PASS** | §5：`pages.yml` 构建前 4 步 + `ci-cd.yml` test job 3 步 |
| 3 | 两端自证：存量绿 / 注入新增必红 / 移除复绿 | **PASS** | §6：3 次真实 run（`1f16271` 绿 → `21b8392` 红 → `7d6af41` 绿） |
| 4 | `--data-path` 失效修掉（两份数据 → 不同结论） | **PASS** | §8：同一命令换数据文件得到 527/0 与 528/1 |

## 2. 交付物（绝对路径）

工作仓 `/opt/data/workspace/Protreptic`：

```text
/opt/data/workspace/Protreptic/tools/credibility_baseline.py            新增：两档判定内核（指纹/基线/分类）
/opt/data/workspace/Protreptic/tools/credibility_gate.py                改：--legacy-report/--hard-fail/--write-baseline/--baseline + resolve_repo_root()
/opt/data/workspace/Protreptic/tools/verify_source_links.py             改：同构两档 + 并发核验 + 连接层失败只算警告
/opt/data/workspace/Protreptic/tools/test_credibility_gate_modes.py     新增：两档七项自测（可复跑）
/opt/data/workspace/Protreptic/data/audit/credibility_baseline.json     新增：527 条存量硬失败基线（526 指纹）
/opt/data/workspace/Protreptic/data/audit/source_links_baseline.json    新增：存量坏链基线
/opt/data/workspace/Protreptic/.github/workflows/pages.yml              改：旧 3 步（必红写法）换成 4 步两档
/opt/data/workspace/Protreptic/docs/planning/credibility_framework.md   改：新增 §7 两档口径
/opt/data/workspace/Protreptic/docs/qa/phase37_x3_ci_gate.md            本报告
```

发布仓 `/opt/data/release/Protreptic-publish`（线上唯一来源）同名路径已同步，另加：

```text
/opt/data/release/Protreptic-publish/.github/workflows/pages.yml        改：构建前插入 4 步门（含 paths 触发）
/opt/data/release/Protreptic-publish/.github/workflows/ci-cd.yml        改：test job 插入两档门 + 负对照自测
```

`tools/credibility_gate.py` 现为**两卡同文件**（X1 的 D3 豁免 + X3 的两档模式），
两仓 sha256 均为 `45a3082aa9e6…`（§7）。

## 3. 两档口径

| 档位 | 语义 | 退出码 |
| --- | --- | --- |
| 默认（无档位参数） | 严格口径（历史行为）：任何硬失败 exit 1 | 0 / 1 |
| `--legacy-report` | 存量（基线内）+ 新增都逐条列出，**只报告不阻断** | 恒 0 |
| `--hard-fail` | 基线内只报告（`::notice`）；基线外任何一条硬失败 | 无新增 0 / 有新增 1 / 基线缺失 2 |
| `--write-baseline` | 用当前硬失败重新冻结基线（改基线必须显式跑） | 0 |

- 基线文件：`data/audit/credibility_baseline.json`
  （`schema=protreptic.credibility_baseline/v1`，`generated_at=2026-09-19T14:30:15+00:00`，
  `counts={"total":527,"D1":60,"D2":9,"D3":0,"D6":457,"distinct_fingerprints":526,"modes_with_findings":202}`，
  `data_sha256=bf168171af42…`）。
- **指纹 = `mode_code|规则|规则内稳定键`**：D1→`figure_code`，D2→伪造书名，D3→命中的污染正则，
  D6→`字段+被引用的 code 主体`。
  这样「改存量条目的说明文字」不产生假新增（§4 第 4 项），而「新模式 / 新 figure_code /
  新伪造书名 / 新污染 / 新悬空引用」必然指纹不同 -> 拦。
- 连接层失败（curl `000` / 超时）在 `verify_source_links.py --hard-fail` 下**只算警告**：
  CI 的网络抖动不该把发布链打红；确定性坏链（4xx/5xx）才进存量/新增判定。
- **负对照不能当 CI 步骤**：`--negative-test` 的成功语义就是 `exit 1`（QA6 §4.2 已实测），
  故 workflow 里不再调用它，改用两个自测守护其语义（§4）。

## 4. 本地自测（可复跑）

```bash
$ cd /opt/data/workspace/Protreptic && python3 tools/test_credibility_gate_modes.py
[PASS] 1 存量态 --hard-fail exit 0
[PASS] 2 存量态 --legacy-report exit 0 且列出存量
[PASS] 3 新增 D3 坏样本 -> exit 1 且 ::error::NEW
[PASS] 4 改写存量引用说明文字 -> 仍 exit 0
[PASS] 5 基线缺失 -> exit 2（fail-closed）
[PASS] 6 --data-path 两份数据结论不同
[PASS] 7 --write-baseline 重新冻结后可继续跑 exit 0

7/7 passed
```

X1 的 D3 豁免自测（同一门槛的另一半，未回退）：

```bash
$ python3 tools/test_credibility_gate.py
[PASS] A 已隔离 figure 的污染出处不报 D3
[PASS] B 公开 figure 的污染出处必报 D3
[PASS] C --no-d3-exemption 严格模式必报 D3
[PASS] D --negative-test 注入坏样本必 exit 1
[PASS] E 干净公开记录必须 exit 0
[PASS] F 真实源库 D3 计数为 0

6/6 passed
```

链接源新增坏链方向（本地注入一条必然 404 的 URL）：

```text
--- 存量坏链（基线内，冻结）: 1 条 ---
  ::notice::LEGACY [DEAD 404] 《天学初函》 -> https://archive.org/details/tienhocsinhuan
--- 新增坏链（基线外，必拦）: 1 条 ---
  ::error::NEW [DEAD 404] 《QA37-X3 注入坏链样本》 -> https://ovmobilegroup.github.io/protreptic/qa37-x3-definitely-404/
[FAIL] hard-fail: 1 条新增坏链（基线外）-> exit 1（存量 1 条已冻结）
```

## 5. 发布仓 workflow 新增片段（证明真接进去了）

`pages.yml`：`paths` 增加门相关文件；构建链**之前**插入 4 步（门红 -> 后面全部 skip，坏数据上不了线）：

```yaml
      # ---- Phase37-X3：可信度门（存量冻结 / 新增即拦）----
      - name: 可信度门 · 存量清单（不阻断）
        run: python3 tools/credibility_gate.py --legacy-report --data-path data/modes_data.json

      - name: 可信度门 · 新增违规必红
        run: python3 tools/credibility_gate.py --hard-fail --data-path data/modes_data.json

      - name: 链接源核验 · 存量清单（不阻断）
        if: always()
        run: python3 tools/verify_source_links.py --legacy-report

      - name: 链接源核验 · 新增坏链必红
        if: always()
        run: python3 tools/verify_source_links.py --hard-fail
```

`ci-cd.yml`（`test` job，push/PR 都过门）：

```yaml
      - name: 可信度门 · 新增违规必红
        run: python3 tools/credibility_gate.py --hard-fail --data-path data/modes_data.json

      - name: 链接源核验 · 新增坏链必红
        run: python3 tools/verify_source_links.py --hard-fail

      - name: 可信度门 · 负对照自测（D3 豁免两方向 + 两档七项）
        run: |
          set -euo pipefail
          python3 tools/test_credibility_gate_modes.py
          if [ -f tools/test_credibility_gate.py ]; then
            python3 tools/test_credibility_gate.py
          else
            echo "::notice::tools/test_credibility_gate.py 尚未入库，本步跳过（Phase37-X1 落地后自动生效）"
          fi
```

命中的 workflow 数（QA6 §4.1 的 0/4 已消除）：

```text
PUB pages.yml     4 步 gate 调用
PUB ci-cd.yml     2 步 gate 调用 + 1 步负对照自测
PUB quality-gate.yml / markdown-lint.yml  未接（不需要：前者判线上产物，后者判 markdown 格式）
```

## 6. 三次真实 CI run（原样日志）

### 6.1 run #1 · 存量态必须绿 —— `1f16271`

```text
Deploy to GitHub Pages  run=35449380499  head=1f16271  conclusion=success
  构建 SPA + 文档站 :: success（步骤：可信度门·存量清单 success / 可信度门·新增违规必红 success /
                              链接源核验·存量清单 success / 链接源核验·新增坏链必红 success）
  部署 :: success
Protreptic CI/CD        run=35449380455  head=1f16271  Test (Python + TypeScript) :: success
  （步骤：可信度门·新增违规必红 success / 链接源核验·新增坏链必红 success / 负对照自测 success）
```

关键日志行（`gh run view 35449380499 --log`）：

```text
resolved data path:     data/modes_data.json (exists=True)
resolved baseline path: /home/runner/work/protreptic/protreptic/data/audit/credibility_baseline.json (exists=True)
hard failures on this dataset: 527
baseline frozen at 2026-09-19T14:30:15+00:00 (total=527, fingerprints=526, D1=60 D2=9 D3=0 D6=457)
--- 存量（基线内，冻结）: 527 条 [D1=60 D2=9 D3=0 D6=458] ---
--- 新增（基线外，必拦）: 0 条 ---
[OK] legacy-report: 存量 527 条 / 新增 0 条 —— 只报告，不阻断 (exit 0)
[OK] hard-fail: 无新增硬失败（存量 527 条已冻结）-> exit 0
Summary: 39 OK, 1 dead, 0 unreachable, 10 unverifiable
--- 存量坏链（基线内，冻结）: 1 条 ---
--- 新增坏链（基线外，必拦）: 0 条 ---
[OK] hard-fail: 无新增坏链（存量 1 条已冻结）-> exit 0
```

### 6.2 run #2 · 注入 1 条新增 D3 坏样本必须红 —— `21b8392`

注入内容（**最小 6 行 diff**，只加一条模式，未改任何存量记录）：

```json
    {
      "mode_code": "M-QA37-X3-BAD-001",
      "figure_code": "H-WYM-001",
      "name_zh": "QA37-X3 注入坏样本（仅用于 CI 红态自证，随后移除）",
      "source_chapter": "Phase 21 入库与修复提交链（双镜像 sha256 记录：茅以升 96bdd4c4）"
    },
```

```text
Deploy to GitHub Pages  run=35449867707  head=21b8392  conclusion=failure
  构建 SPA + 文档站 :: failure
    可信度门 · 存量清单（不阻断）   -> success
    可信度门 · 新增违规必红         -> failure     <== 门在这里断链
    链接源核验 · 存量清单（不阻断） -> success
    链接源核验 · 新增坏链必红       -> success
    重建 figures 数据库 / 构建静态数据分片 / … / 构建 SPA / … / 断言合并产物 -> skipped（共 26 步）
  部署 :: skipped                                  <== 坏数据没有上线
Protreptic CI/CD        run=35449867706  head=21b8392  Test (Python + TypeScript) :: failure
    可信度门 · 新增违规必红         -> failure     <== 同一道门在 ci-cd 也红
```

关键日志行（`gh run view 35449867707 --log`）：

```text
hard failures on this dataset: 528
--- 存量（基线内，冻结）: 527 条 [D1=60 D2=9 D3=0 D6=458] ---
--- 新增（基线外，必拦）: 1 条 ---
##[error]NEW M-QA37-X3-BAD-001|D3|sha256 | [M-QA37-X3-BAD-001] D3 出处污染: source_chapter 匹配污染模式 'sha256' -> Phase 21 入库与修复提交链（双镜像 sha256 记录：茅以升 96bdd4c4）
[FAIL] hard-fail: 1 条新增硬失败（基线外）-> exit 1（存量 527 条已冻结）
```

同一 push 上另有两个 workflow 也红，**原因逐条查明（不混为一谈）**：

| workflow | run | 结论 | 归因（原始证据） |
| --- | --- | --- | --- |
| Quality Gate | `35449901416` | failure | 连带：`数据校验` job 的 `构建静态数据分片`（`tools/export_static_site.py`）失败 —— 注入样本只有 4 个字段，导出脚本读不到必需字段。**同一 workflow 在 `1f16271` 上 3 次全 success**（`35449711417`/`35449467257`/`35449382880`），故与本卡的门无关 |
| CI（markdown-lint） | `35449867775` | failure | **存量红，非本卡引入**：`docs/qa/phase37_x2_evidence.md:9:16 MD038` 与 `:378:42 MD009`；上一次 push `99dd4d7` 的 run `35449304642` 是**同样两条**错误 |

补充：另做本地对照——把注入样本做成**完整记录拷贝**（29 字段，只改 `mode_code`/`figure_code`/`source_chapter`）：

```text
gate exit: 1
--- 新增（基线外，必拦）: 1 条 ---
  ::error::NEW M-QA37-X3-WELLFORMED-001|D3|sha256 | [M-QA37-X3-WELLFORMED-001] D3 出处污染: ...
[FAIL] hard-fail: 1 条新增硬失败（基线外）-> exit 1（存量 527 条已冻结）
```

即「形态合法的新增违规」同样只有门会红，Quality Gate 的连带只源于上面那个 4 字段的最小样本。

### 6.3 run #3 · 移除注入后必须复绿 —— `7d6af41`

```text
Deploy to GitHub Pages  run=35450145225  head=7d6af41  conclusion=success
  构建 SPA + 文档站 :: success
  部署 :: success
Protreptic CI/CD        run=35450145229  head=7d6af41  Test (Python + TypeScript) :: success
```

关键日志行：

```text
--- 存量（基线内，冻结）: 527 条 [D1=60 D2=9 D3=0 D6=458] ---
--- 新增（基线外，必拦）: 0 条 ---
[OK] hard-fail: 无新增硬失败（存量 527 条已冻结）-> exit 0
Summary: 38 OK, 1 dead, 1 unreachable, 10 unverifiable
--- 存量坏链（基线内，冻结）: 1 条 ---
[OK] hard-fail: 无新增坏链（存量 1 条已冻结）-> exit 0
```

## 7. 两仓同步与 push

```bash
$ cd /opt/data/release/Protreptic-publish && git status -sb
## main...origin/main            # 无 [ahead N]

$ git log --oneline -4
7d6af41 QA37-X3 移除注入的坏样本，恢复存量基线态（预期 CI 复绿）
21b8392 QA37-X3 注入 1 条新增 D3 坏样本（M-QA37-X3-BAD-001，仅用于 CI 红态自证）
1f16271 Phase37-X3: CI 接入可信度门两档（存量冻结/新增即拦）+ 链接源核验两档 + 526 指纹基线（发布仓同步）
99dd4d7 Phase37-X2: 证据报告补齐（push 后回读 dev/pub/origin 三方 sha256 一致）

$ sha256sum tools/credibility_gate.py     # 两仓
45a3082aa9e688eaef3d3d860c555066826a74ef3cde31893b4e14cdc04dea2e  （工作仓与发布仓一致）
$ sha256sum data/modes_data.json          # 两仓
bf168171af42f8148c3adecbbc1a71258522676355357f6466acdcb25f2e61cb  （与基线 data_sha256 相同）
```

> 工作仓 `master` 在 GitHub 上没有对应分支（`git ls-remote --heads origin` 只有 `main`），
> 故「push」只作用于发布仓 `main`；工作仓为本地仓 + 本地提交 `cba921a8`。

## 8. `--data-path` 修复证据（两份数据 → 不同结论）

修的是什么：QA5 §4.3 说 `args.data_path` 被解析却没用；W3 修了读取，但**白名单与基线仍取脚本所在仓**，
于是「拿 A 仓白名单判 B 仓数据」。现在 `--data-path` 的语义补全为：
**数据 / 白名单（`tools/_quarantine.py`）/ 默认基线（`data/audit/credibility_baseline.json`）三者同仓**
（`resolve_repo_root()` 由 `<root>/data/modes_data.json` 反推 root），并把解析结果打印出来可核。

```bash
$ cd /opt/data/workspace/Protreptic
$ python3 tools/credibility_gate.py --hard-fail --data-path data/modes_data.json
resolved data path:     data/modes_data.json (exists=True)
resolved baseline path: /opt/data/workspace/Protreptic/data/audit/credibility_baseline.json (exists=True)
hard failures on this dataset: 527
--- 存量（基线内，冻结）: 527 条 [D1=60 D2=9 D3=0 D6=458] ---
--- 新增（基线外，必拦）: 0 条 ---
[OK] hard-fail: 无新增硬失败（存量 527 条已冻结）-> exit 0

$ python3 tools/credibility_gate.py --hard-fail --data-path /tmp/x3probe/ws_injected.json   # 同一命令，换数据文件
hard failures on this dataset: 528
--- 存量（基线内，冻结）: 527 条 [D1=60 D2=9 D3=0 D6=458] ---
--- 新增（基线外，必拦）: 1 条 ---
  ::error::NEW M-QA37-X3-BAD-001|D3|sha256 | [M-QA37-X3-BAD-001] D3 出处污染: ...
[FAIL] hard-fail: 1 条新增硬失败（基线外）-> exit 1（存量 527 条已冻结）
```

`tools/verify_source_links.py` 同样接受 `--links-path` / `--baseline`，自测第 6 项固定断言「两份数据结论不同」。

## 9. 遗留与建议（如实列出）

1. **markdown-lint 存量红**（`docs/qa/phase37_x2_evidence.md` 两处：MD038 / MD009）——归 X2，
   本卡未触碰该文件；修复后 `CI` workflow 才会复绿。
2. **`tools/verify_findings.py` 未接进 CI**（X2 的接口通知）。它天然是「新增即拦」语义，
   且把 `findings.json` 的 summary 与**现算**库对照，`data/modes_data.json` 一变就报过期 ——
   接入前需要先决定「过期算红还是算警告」，否则会制造新一轮存量红。建议单独一卡决定。
3. **基线需要显式维护**：修掉存量债务后跑 `--write-baseline` 重新冻结（未被冻结的旧条目只会
   以 `::warning::STALE` 出现在报告里，不会拦人）；反之**放宽基线必须走 PR 复核**。
4. **`--legacy-report` 恒 exit 0**：它是清单/审计档，不承担拦人职责；拦人一律靠 `--hard-fail`。
