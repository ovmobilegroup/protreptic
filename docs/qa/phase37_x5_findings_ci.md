# Phase37-X5 交付报告：`verify_findings.py` 接进 CI（两档口径 + 计数过期归属）

| 项 | 值 |
|---|---|
| 卡号 | `t_fd9210a5`（父卡 `t_b74ae78b` = Phase37-X3） |
| 来源 | `docs/qa/phase37_x3_ci_gate.md` §9.2「`tools/verify_findings.py` 未接进 CI」 |
| 作业仓 | 开发仓 `/opt/data/workspace/Protreptic`；发布仓 `/opt/data/release/Protreptic-publish`（origin `main`，驱动 Pages 与 CI） |
| 报告快照 | dev sha 见 §7（两仓字节一致；CI run 时间为 UTC） |

## 1. 要解决的问题（原样来自 X3 §9.2）

1. `verify_findings.py` 的 E 类检查把 `findings.json` 的 summary 与**现算**库对照，
   `data/modes_data.json` 一变（sha256 变化）它就报「过期」—— 而该文件每次数据更新都会变，
   照抄接进 CI = **每次数据改动都红**。
2. gate 用的是「基线冻结 + 新增即拦」两档（`data/audit/credibility_baseline.json`），
   `verify_findings.py` 当时只有「新增即拦」一档，缺「存量不阻断」的表达。

## 2. 交付物（两仓字节一致的文件）

| 文件 | 内容 | sha256 |
|---|---|---|
| `tools/verify_findings.py` | 两档（`--legacy-report` / `--hard-fail` / `--write-baseline`）+ 指纹 + E 降级为警告 | `a5ed85852cbba2a25b40a499a00f31d3786c158c5f74cca7822c00f231eb9456` |
| `tools/test_verify_findings_modes.py`（新） | 八项自测（负对照语义的机检守护） | `653e5c060dcf71674184bc12b8171063e1e68a0f1da05fdd9cb943e5cdf949fb` |
| `data/audit/findings_baseline.json`（新） | findings 硬失败基线（当前 0 条，fail-closed） | `a84dd590a83c0d01d46451e4d526d3279c7f7ee2f68538dcc6e975c757e81ea2` |
| `docs/planning/credibility_framework.md` | 新增 §8（两档 + 计数过期归属 + 接线位置） | `129b7d3b146591c4a3dcbec62df6d67e242bb276d22e2a6df5999c065b894014` |
| `docs/qa/phase37_x5_findings_ci.md`（新，本文件） | 命令 + 原始输出 + CI run 证据 | 见 §6 |
| 发布仓 `.github/workflows/ci-cd.yml` | `test` job 新增 2 步（与 X3 的门相邻） | `8c78537901760c8125e731b5676eef80528feab142eb547b244baabc8cc0b287` |

**未动** `pages.yml`（发布仓 sha256 保持 `615e22699c6b61656a79311037109bf6afa4203162f52c8b35ee1064369d779a`，本卡未触碰）——
发布链已由 X3 的两道门守住，多一道「过期判定」会把部署打红（正是本卡要避免的事故模式）。

## 3. 两档口径（与 `credibility_gate.py` 同构）

| 档位 | 语义 | 退出码 |
|---|---|---|
| `--legacy-report` | 存量（基线内）+ 新增都逐条列出，只报告不阻断 | 恒 `0` |
| `--hard-fail` | 基线内只报告（`::notice::LEGACY`）；**基线外任何一条硬失败** | 无新增 `0` / 有新增 `1` / 基线缺失 `2` |
| `--write-baseline` | 用当前硬失败重新冻结基线 | `0` |

指纹 = `规则|规则内稳定键`：A 结构 → 归一化消息；B 不存在 → `mode_code=值` / `figure_code=值`；
C 锚点 → 归一化消息（**引号内的值被抹掉**，改锚点文字不产生假新增）；D 自洽 → `summary.字段名`。

**如实说明：基线当前为空（0 条）**。冻结当时 `findings.json` 在 A–D 上**没有**任何硬失败
（见 §5 干净态输出 `hard failures on this findings file: 0`），所以 `entries: []`。
这不是「没接」：机制在位、`--hard-fail` 生效、基线缺失即 `exit 2`（fail-closed）；
`--write-baseline` 路径也已由自测第 6 项验证（冻结后该条不再拦）。
将来若出现可接受的历史遗留，必须显式跑 `--write-baseline` 并在报告说明。

硬失败的构成（源库现状 133 条 findings）：

- A 结构（findings 非空列表 / 必备字段） = 0
- B code 存在性（mode_code / figure_code 必须在库里）= 0
- C 锚点可定位（anchor 在库原文 + evidence 里） = 0
- D 自洽（summary 计数 == findings 列表逐条计数） = 0
- E 计数新鲜度（summary vs 现算） = 0（且已降级为警告，见 §4）

## 4. 「计数过期」（E 类）的归属决策：**警告，不是新增违规**

| 归属 | 后果 | 判定 |
|---|---|---|
| 算新增违规（红） | `modes_data.json` 每次数据更新 sha256 都变，summary 必然过期 → **每次数据改动都红**，并强迫每次无关数据提交都额外刷新 findings 才能绿 | 否决 |
| **算警告（不红）** | CI 只打印 `::warning::计数过期(E) ... 刷新：python3 tools/build_audit_findings.py --write`；坏数据仍由 `credibility_gate --hard-fail` 拦 | **采用** |

理由一句话：**坏数据归 `credibility_gate`，清单新鲜度归人**。E 的职责是提示刷新，不是拦人；
真正拦人的是 A–D（清单说谎：引用了不存在的 code、锚点在库里找不到）。
实现上 E 的消息统一带前缀 `计数过期(E)`，两档打印里单独一节（`--- 计数过期（警告，不阻断）---`），
既不进基线、也不影响退出码。该决策已写进 `docs/planning/credibility_framework.md` §8.2。

## 5. 本地验收（命令 + 原始输出，发布仓目录下执行）

### 5.1 干净态 `--hard-fail` → exit 0

```
$ python3 tools/verify_findings.py --hard-fail --data-path data/modes_data.json
=== VERIFY FINDINGS · 存量/新增两档 ===
mode: hard-fail
resolved findings path: /opt/data/release/Protreptic-publish/data/audit/findings.json (exists=True)
resolved data path:     data/modes_data.json (exists=True)
resolved baseline path: /opt/data/release/Protreptic-publish/data/audit/findings_baseline.json (exists=True)
hard failures on this findings file: 0
baseline frozen at 2026-09-19T15:20:44+00:00 (total=0, fingerprints=0, A=0 B=0 C=0 D=0)
baseline data_sha256:     bf168171af42f8148c3adecbbc1a71258522676355357f6466acdcb25f2e61cb
current  data_sha256:     bf168171af42f8148c3adecbbc1a71258522676355357f6466acdcb25f2e61cb

--- 存量（基线内，冻结）: 0 条 [A=0 B=0 C=0 D=0] ---

--- 新增（基线外，必拦）: 0 条 ---
  (none)

--- 计数过期（警告，不阻断）: 0 条 ---
  (none)

--- 其他警告（不阻断）: 1 条 ---
  ::warning::E: these mode codes are harvested twice by get_all_modes (present both in the top-level modes array and inside a figure node): ['M-ASM-001', 'M-ASM-002', 'M-ASM-003', 'M-ASM-004', 'M-ASM-005', 'M-ASM-006', 'M-ASM-007', 'M-ASM-008', 'M-ASM-009', 'M-ASM-010']

[OK] hard-fail: 无新增硬失败（存量 0 条已冻结）-> exit 0
exit=0
```

### 5.2 注入 / 移除 / 基线缺失 / 计数过期 / 存量冻结：八项自测 8/8

注入不存在的 code、移除后复绿、基线缺失 fail-closed、冻结后存量不阻断、冻结态下再注入必红、
计数过期只警告 —— 全部由 `tools/test_verify_findings_modes.py` 机检（可复跑）：

```
$ python3 tools/test_verify_findings_modes.py
[PASS] 1 干净态 --hard-fail exit 0
[PASS] 2 干净态 --legacy-report exit 0 且两档分节都在
[PASS] 3 注入不存在的 mode_code -> exit 1 且 ::error::NEW
[PASS] 4 移除注入（原始 findings）-> 复绿 exit 0
[PASS] 5 基线缺失 -> exit 2（fail-closed）
[PASS] 6 冻结注入态后 -> 存量不阻断 exit 0
[PASS] 7 冻结态下再注入第二条坏 code -> exit 1
[PASS] 8 计数过期只警告不红（E 归属：警告）

8/8 passed
exit=0
```

第 3 项的实际注入形态：把 `findings[0].mode_code` 改成库里不存在的 `M-QA37-X5-SELFTEST-BAD`，
`--hard-fail` 输出 `::error::NEW B|M-QA37-X5-SELFTEST-BAD|mode_code=M-QA37-X5-SELFTEST-BAD | ...`
并 `exit 1`；第 4 项换回原始 `findings.json` 立即复绿。真实 CI 上的同一结论见 §6。

### 5.3 回归：X3 的两个自测未受影响

```
$ python3 tools/test_credibility_gate_modes.py
7/7 passed
$ python3 tools/test_credibility_gate.py
6/6 passed
```

## 6. CI 接线与真实 run 证据

发布仓 `ci-cd.yml` 的 `test` job 新增两步（紧跟 X3 的「可信度门 · 负对照自测」之后）：

```yaml
      - name: findings 自检 · 新增硬失败必红
        run: python3 tools/verify_findings.py --hard-fail --data-path data/modes_data.json

      - name: findings 自检 · 两档八项（含计数过期只警告）
        run: python3 tools/test_verify_findings_modes.py
```

<!-- CI-EVIDENCE -->

## 7. 两仓同步与 parity

<!-- PARITY -->

## 8. 遗留与建议（如实列出）

1. **空基线需要显式维护**：`findings_baseline.json` 当前 0 条；一旦将来把某类 findings 硬失败
   当作可接受存量，必须跑 `--write-baseline` 并在 PR 里说明（放宽基线要走复核）。
2. **E 类只警告，不追债**：数据更新后 findings.json 的 summary 会过期，CI 只提示刷新；
   刷新是维护动作，不拦合并。若某天要求「清单必须永远新鲜」，需要单独一卡把刷新接到数据入库流水线。
3. **`ci-cd.yml` 只在发布仓修改**：开发仓的 workflow 副本自 X3 起即为历史分叉
   （dev 的 `ci-cd.yml` 不含 X3 的门），本卡不扩大分叉、也不动 `pages.yml`；
   两仓字节一致的是 §2 表里的工具/数据/文档文件。
4. **markdown-lint 存量红**（`docs/qa/phase37_x2_evidence.md`，归 X2）与本卡无关，未触碰。
