# Phase21-W11 CI 存量红修复报告（卡 t_0ec6fb57）

- 卡：`t_0ec6fb57`（bustamante；船长 2026-09-24 08:10 派发）；父卡 `t_bda44643`（W5 修复链尾，done 放行）
- 边界：仅刷新 `data/audit/lifespan_backfill.json`（两仓）+ 本报告/证据；**零数据内容改动**；未动 markdown-lint 存量红（另项）；未动 QA/W4/W5/W7/W9 在途件
- 单写者预检（开工时扫 `/opt/data/kanban/boards/protreptic/kanban.db`）：同仓在跑 = W7 `t_d24e11bc`（elcano，写面=根目录 json / tools/json 杂物，其卡明示不写 `data/modes_data.json`）+ W8S2B1 QA `t_a407cb32`（espinosa，只读核验）；开工时两仓工作树干净、无 index.lock —— 与本卡写面（`data/audit/**`）不相交，按「最小写面、只碰本卡文件」推进
- 一句话结论：两仓清单刷新完成（盘上 476 → 576 键）；`--check` 两仓 rc=0；`test_credibility_d45.py` **38/38**（Z7 由红转绿）；两仓 byte-same；提交/镜像/push 完成；CI 复验见 §四（回执补记回填）

## 零、基线复现与参考值对账

开工基线（两仓同漂移，先复现再修）：

| 仓 | `python3 tools/backfill_lifespans.py --check`（开工时） |
|---|---|
| 工作仓 | rc=1 ——「清单过期：盘上 476 个取值键 / 现场重算 576 个 —— 请跑 python3 tools/backfill_lifespans.py 刷新」 |
| 发布仓 | rc=1 —— 同文案 |

参考值对账（船长干跑参考 575/303/22/358、清单 sha `012695d6…` → 本次实测 576/304/23/361、sha `f70cff92…`）：

| 口径 | 干跑参考（08:03 探针） | 本次刷新（实测） | 差因（逐条） |
|---|---|---|---|
| 取值键 | 575 | 576 | +`H-AZJ-001`（安子介，有可用生卒年） |
| 有日期 figure | 303 | 304 | 同上（+1） |
| 无日期 figure | 22 | 23 | +`H-SHF-001`（沈复，reason=`missing-birth-or-death-field`） |
| 扫描文件 | 358 | 361 | +`H-AZJ-001.json` / `H-AZJ-001_modes.json` / `H-SHF-001.json`（R9 链在探针后落盘） |

排除 3 件新落盘文件后，探针清单与本次实测**零差异**（0 增 0 删 0 值变更）——差异全部来自新数据，非口径漂移。

## 一、刷新与验证（完成合同 1-3）

1. **两仓分别刷新**（写模式 `python3 tools/backfill_lifespans.py`，两仓输出一致）：
   - 扫描 `data/figures/*.json` **361** 个文件；取值面：旧口径 312 → 新口径 **576** 键（+264）
   - 键冲突丢弃 1 个（`H-MZ-001`：KEPT `H-MZ-001.json[1890,1990]` / DROPPED `H-MZ-001_modes.json[-372,-289]`；存量既有行为，本次未变）
   - 有文件年份不可用 49 个（birth-after-death / missing-birth-or-death-field / year-not-parseable）
   - 模式侧覆盖：figure 157 → **304** 个 / 模式 1611 → **3081** 条（全库 3331 条）；仍无日期 **23** 个 figure（250 条模式；no-figure-file 16 / missing-birth-or-death-field 7）
2. **`git diff --stat` 断言**：两仓均**仅 1 个文件** = `data/audit/lifespan_backfill.json`（833 行：+591 / −242）；工作仓未跟踪报告/证据文件不计。✅（刷新后、落报告前实测）
3. **`--check` 终态**：两仓 rc=0 ——「[OK] 清单新鲜：576 个取值键、304 个 figure 有日期、23 个无日期，逐字节一致」
4. **d45 自测**：`python3 tools/test_credibility_d45.py` → **38/38 PASS rc=0**（此前 37/38，唯一红点 Z7 转 PASS）；Z7 语义 = `backfill_lifespans.py --check` 对当前数据 exit 0（可重入不漂移）
5. **两仓清单 byte-same**：
   - sha256（工作仓）= sha256（发布仓）= `f70cff92f54bd6f96674e36acd0e6fae834cec46bd94aa5baf23021f7d1735b9`；`cmp` 逐字节相等 ✅
   - 参考/历史值：探针版 sha `012695d6e65f04e031504bcc60de7c3ebff88bb1b4c41941a92d27f8823c996d`（575/303/22/358，已被新落盘数据超越，如上）；本卡前盘上旧清单（Phase46-R 版）sha `286479b5ba37fe45275fe7ab04fdc129ba4160e3210aceaf4a9752d9853577ee`
   - 旧清单（Phase46-R 版）→ 新清单全量对账：keys_available 476 → 576（+100）、有日期 figure 230 → 304（+74）、无日期 55 → 23（−32）、扫描文件 330 → 361、modes_total 2888 → 3331、modes_covered 2318 → 3081；**键 0 删除**；`newly_covered_figures` 147 个（相对旧口径；逐条 provenance 见清单本体）

## 二、本地预跑 CI 链（供 CI 对照）

| CI 步骤 | 本地命令 | 结果 |
|---|---|---|
| 可信度门 · 新增违规必红 | `python3 tools/credibility_gate.py --hard-fail --data-path data/modes_data.json` | rc=0（存量 524 冻结 / 新增 0） |
| 链接源核验 · 新增坏链必红 | `python3 tools/verify_source_links.py --hard-fail` | rc=0（存量 0 / 新增 0；连接层警告 169 条不计违规） |
| 负对照自测（内含 1/3） | `python3 tools/test_credibility_gate_modes.py` | 7/7 passed rc=0 |
| 负对照自测（内含 2/3） | `python3 tools/test_credibility_gate.py` | 6/6 passed rc=0 |
| 负对照自测（内含 3/3） | `python3 tools/test_credibility_d45.py` | **38/38 passed rc=0** |
| findings 自检 · 新增硬失败必红 | `python3 tools/verify_findings.py --hard-fail --data-path data/modes_data.json` | rc=0（新增 0） |
| findings 自检 · 两档八项 | `python3 tools/test_verify_findings_modes.py` | 8/8 passed rc=0 |
| 两仓一致性机检 · 19 项 | `python3 tools/test_check_repo_parity.py` | 19/19 passed rc=0 |
| Run Python tests | `python3 tools/test_thinking_mode_selector.py`（tools 目录下） | ALL TESTS PASSED (11) rc=0 |

（vue-tsc / lint 两项未复跑：本次零 web 改动；船长已预跑全绿。）

## 三、三件套（提交 / 镜像 / push）

- 工作仓提交：`<WS_SHA>`（3 件：`data/audit/lifespan_backfill.json` + 本报告 + 证据）
- 发布仓镜像提交：`<PB_SHA>`（同 3 件，byte-exact）
- push：`<OLD_SHA>..<PB_SHA>` rc=0；`git ls-remote origin main` == `<PB_SHA>` ✅
- 网络备注：本机 LAN HTTPS 代理对 GitHub 的 TLS 隧道本轮间歇失败（curl 35 / unexpected eof），push 与 API 查询走**直连 + 重试**完成

## 四、CI 复验（核心验收）—— 回执补记回填

- 对 sha `<PB_SHA>` 的 ci-cd.yml run：见 `回执补记`（报告文末 / 卡面 comment）
- 「可信度门 · 负对照自测（D3 豁免两方向 + 两档七项）」步骤：见补记

## 五、边界与遗留

- markdown-lint 工作流存量红（备份目录 H-ZX-001.md）：另项，本卡未动
- R9/W8/W9 后续合并落盘后本清单可能再现漂移：已知，收口阶段再刷一次即可（本卡已按卡面要求只做一次刷新）
- 未碰 W7/W8S2B1 在途路径；本卡唯一数据面写操作 = `data/audit/lifespan_backfill.json` 再生成（内容 100% 由现场重算产出）
