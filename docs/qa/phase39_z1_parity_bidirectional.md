# Phase39-Z1：两仓一致性机检「双向单侧检测」加固验收证据

- 卡片：t_7c9fa8a4（san-martin）
- 日期：2026-09-20
- 机检本体：`tools/check_repo_parity.py`（随两仓在构建图内同步）
- 负对照自测：`tools/test_check_repo_parity.py`（19 项，已接进发布仓 `ci-cd.yml` 的 test job）
- 口径：`docs/planning/credibility_framework.md` 第 9.4 / 9.4.1 节
- 仓根：workspace `/opt/data/workspace/Protreptic`；publish `/opt/data/release/Protreptic-publish`

## 0. 结论（每条都有命令与输出）

- 旧口径只看索引里的已跟踪文件，对「只在单侧」的构建图文件**零报警**：实测 `--tracked-only` 对
  `docs/qa/__parity_probe__.md` 仍打印零差异、`exit 0`（第 1 节）。
- 修复后：单侧缺失（工作仓独有 / 发布仓独有，未跟踪与已跟踪都算）**必报差异并 `exit 1`**（第 2 / 3 节）；
  删掉探针即回归 `exit 0`。
- 当前真实两仓：`[stats] 两仓都有 1328 条（其中逐字节一致 1328），仅单侧 0 条`、`exit 0`（第 4 节）。
- 排除口径不回退且不静默吞掉：报告按「排除规则 与 侧别」列出条数与理由，排除项的单侧差异
  （排除集里仅工作仓 26 条 / 仅发布仓 676 条）逐条可查（第 4 节全量输出）。
- 边界自检仍有牙：往发布仓 `pages.yml` 真加一个构建步骤，`exit 2` 并点名（第 6 节）。
- 自比守卫：`workspace == publish` 时 `exit 2`，堵掉「自比恒零差异」的同族假 OK（第 8 节）。
- 自测 19/19（含旧口径复现盲区、单侧双向、排除口径、边界、自比守卫、TOOL_FILES 自洽）（第 7 节）。

## 1. 盲区复现：旧口径（只看索引）对单侧文件零报警

命令（开发仓根执行）：

```bash
printf 'probe\n' > docs/qa/__parity_probe__.md      # 只在工作仓的构建图文件（未跟踪）
python3 tools/check_repo_parity.py --tracked-only   # 旧口径：只看索引里的已跟踪文件
```

输出（节选：统计行与结尾；完整输出同 §4 结构，仅末尾统计不同）：

```text
[stats] 两仓都有 1326 条（其中逐字节一致 1326）｜仅单侧 0 条（仅工作仓 0 · 仅发布仓 0）
[OK] 零差异：1326 个构建图文件两仓逐字节一致（sha256）
exit=0
```

结论：探针文件在构建图内（`docs/**`）、只在工作仓，旧口径 `exit 0`、零差异 —— 盲区复现。

## 2. 负对照 A：只在工作仓的构建图文件必须报差异（exit 1）

命令：

```bash
printf 'probe\n' > docs/qa/__parity_probe__.md
python3 tools/check_repo_parity.py                    # 新口径（默认：索引 与 未跟踪未 gitignore）
```

输出（节选：差异清单与统计；exit=1）：

```text
[DIFF] 1 处差异（文件名 + 侧别 + 理由分类）：
   MISSING_IN_PUBLISH     [仅工作仓 · 未跟踪（未 git add，尚未进入索引）]                       docs/qa/__parity_probe__.md

修法：内容差异按发布仓为准同步（cp <publish>/<path> <workspace>/<path> 反之视角色而定）；单侧缺失按角色补齐（构建图文件两边都必须有）。同步后重跑本脚本；退出码 1。
exit=1
```

删掉探针后回归：

```bash
rm docs/qa/__parity_probe__.md && python3 tools/check_repo_parity.py
```

输出（节选：末三行）：

```text
[stats] 两仓都有 1328 条（其中逐字节一致 1328）｜仅单侧 0 条（仅工作仓 0 · 仅发布仓 0）
[OK] 零差异：1328 个构建图文件两仓逐字节一致（sha256）
exit=0
```

## 3. 负对照 B：只在发布仓的构建图文件同样必须报差异（exit 1）

命令（注意：机检在开发仓根执行；从发布仓根执行且不传 `--workspace` 会被自比守卫拦下，见 §8）：

```bash
printf 'probe\n' > /opt/data/release/Protreptic-publish/docs/qa/__parity_probe_pub__.md
python3 tools/check_repo_parity.py   # 在开发仓根执行
```

输出（节选：差异清单与统计；exit=1）：

```text
[DIFF] 1 处差异（文件名 + 侧别 + 理由分类）：
   MISSING_IN_WORKSPACE   [仅发布仓 · 未跟踪（未 git add，尚未进入索引）]                       docs/qa/__parity_probe_pub__.md

修法：内容差异按发布仓为准同步（cp <publish>/<path> <workspace>/<path> 反之视角色而定）；单侧缺失按角色补齐（构建图文件两边都必须有）。同步后重跑本脚本；退出码 1。
exit=1
```

删掉探针后回归：

```bash
cd /opt/data/release/Protreptic-publish/docs/qa && rm __parity_probe_pub__.md
cd /opt/data/workspace/Protreptic && python3 tools/check_repo_parity.py
```

输出（节选：末三行）：

```text
[stats] 两仓都有 1328 条（其中逐字节一致 1328）｜仅单侧 0 条（仅工作仓 0 · 仅发布仓 0）
[OK] 零差异：1328 个构建图文件两仓逐字节一致（sha256）
exit=0
```

## 4. 修后对当前真实两仓跑一次（全量原始输出）

```bash
cd /opt/data/workspace/Protreptic && python3 tools/check_repo_parity.py
```

```text
[boundary] workspace = /opt/data/workspace/Protreptic
[boundary] publish   = /opt/data/release/Protreptic-publish
[boundary] pages.yml 构建步骤 16 个 / paths 触发器 30 条 —— 均已被清单覆盖（边界自检通过）
[boundary] 纳入边界：workspace 1328 / publish 1328；排除：workspace 27 / publish 677
[boundary] 文件集口径：索引（已跟踪）∪ 未跟踪且未被 .gitignore —— 双向单侧检测（Phase39-Z1）
[boundary] 未跟踪未提交（但已纳入机检）：workspace 2 / publish 2

-- 排除统计（publish 侧） --
    637  开发侧原始分片留档（637 个，仅发布仓有）：grep tools/ + .github/ + web/src/ 无任何读取；不参与构建、不
     34  mkdocs.pages.yml `exclude_docs: archive/` → 不构建、不上线
     13  备份文件（.bak / .bak_<tag>）
     10  入库前备份目录（开发仓独有，非构建图）
      5  前端构建产物（CI 现场 npm run build 生成；发布仓为加 .gitignore 之前的历史跟踪）
      3  merge 暂存目录（开发仓独有，非构建图）
      1  开发侧汇总实验产物，无构建步骤读取
      1  开发侧 FAISS 索引二进制（无构建步骤读取；语义检索为 api/ 侧）

-- 排除规则 × 侧别（排除项不参与差异判定；单侧差异一并列出理由，不静默吞掉） --
   pattern                            ws    pub      仅ws     仅pub
   data/intl_figures/*                 0    637        0      637
      └ 开发侧原始分片留档（637 个，仅发布仓有）：grep tools/ + .github/ + web/src/ 无任何读取；不参与构建、不上线，故不纳入（如要按「源库留档」更严口径纳入，删掉本规则并执行 publish→workspace 同步）
   data/backup_merge_*/*              10      0       10        0
      └ 入库前备份目录（开发仓独有，非构建图）
   data/merge_staging_*/*              3      0        3        0
      └ merge 暂存目录（开发仓独有，非构建图）
   */node_modules/*                    0      0        0        0
      └ 依赖目录（.gitignore）
   *.bak*                             12      1       11        0
      └ 备份文件（.bak / .bak_<tag>）
   data/all_sources.json               1      0        1        0
      └ 开发侧汇总实验产物，无构建步骤读取
   data/semantic_index.faiss           1      0        1        0
      └ 开发侧 FAISS 索引二进制（无构建步骤读取；语义检索为 api/ 侧）
   docs/archive/*                      0     34        0       34
      └ mkdocs.pages.yml `exclude_docs: archive/` → 不构建、不上线
   web/dist/*                          0      5        0        5
      └ 前端构建产物（CI 现场 npm run build 生成；发布仓为加 .gitignore 之前的历史跟踪）
   web/public/data/*                   0      0        0        0
      └ 静态数据产物（tools/export_static_site.py 现场生成；.gitignore 已声明）
   tools/assets/fonts/.cache/*         0      0        0        0
      └ 字体源缓存（.gitignore；只在本机重新子集化时用）
   tools/gc/gc                         0      0        0        0
      └ 开发侧工具二进制，未被任何构建步骤调用
   合计：排除 ws=27 / pub=677；其中仅单侧 702 条（仅工作仓 26 · 仅发布仓 676）

不在边界内（既不参与站点构建、也不进入线上站点）的其余路径：Dockerfile.api/Dockerfile.web、docker-compose.yml、api/**（后端 FastAPI 容器）、.github/**（CI 编排，两仓职责不同）、tests/、cli_tests/、scripts/、docs_site/**（更早的独立文档站工程，mkdocs.pages.yml 明确不用它）、kanban/、release/、backups_merge_*/、IL/、Vietnam/、assets/、templates/、scenarios/、individuals/、构建/ 等开发侧目录，以及根目录遗留副本（modes_data.json、scenarios_zh/en.json、code_maps.json、scenario_tags.json、three_dimensional_comparison_matrix.xlsx、lighthouserc.json 等）——构建步骤读的是 data/** 与 tools/** 下的同名文件（见 build_figures_db.py 的 find() 顺序）。

[stats] 两仓都有 1328 条（其中逐字节一致 1328）｜仅单侧 0 条（仅工作仓 0 · 仅发布仓 0）
[OK] 零差异：1328 个构建图文件两仓逐字节一致（sha256）
exit=0
```

## 5. JSON 口径（去重后计数与单侧数）

```bash
python3 tools/check_repo_parity.py --json
```

```json
  "counts": {
    "workspace_in_boundary": 1328,
    "publish_in_boundary": 1328,
    "both_sides": 1328,
    "identical": 1328,
    "only_workspace": 0,
    "only_publish": 0,
    "excluded_publish": 677,
    "excluded_workspace": 27
  },
  "untracked_in_boundary": {
    "workspace": 2,
    "publish": 2
```

去重后「两仓都有」1328 条（其中逐字节一致 1328），「仅单侧」0 条（仅工作仓 0 / 仅发布仓 0）。
注：本次采集时 `untracked_in_boundary` 为 2 / 2 —— 正是本卡新增的
`tools/test_check_repo_parity.py` 与本报告本身（当时尚未 `git add`）；提交后归零，机检同样看得见它们。

## 6. 边界自检回归：真给发布仓 pages.yml 加一个构建步骤

```bash
sed -i '121a\      - name: fake step probe\n        run: python3 tools/fake_new_step.py' .github/workflows/pages.yml   # 在发布仓执行
cd /opt/data/workspace/Protreptic && python3 tools/check_repo_parity.py
```

输出（exit=2，点名未纳入的步骤）：

```text
[FAIL] 边界过期：pages.yml 有构建步骤不在本清单 → 请更新 tools/check_repo_parity.py
        未纳入: tools/fake_new_step.py
exit=2
```

随后从备份还原（`diff -q` 确认与备份一致、`git status` 干净）。

## 7. 负对照自测 19/19（全量原始输出）

```bash
python3 tools/test_check_repo_parity.py
```

```text
[PASS] 1 干净态 exit 0 + 零差异  —— exit=0
[PASS] 2 合法边界不误报（16 步清单里有的构建步骤）  —— [boundary] pages.yml 构建步骤 1 个 / paths 触发器 2 条 —— 均已被清单覆盖（边界自
[PASS] 3 工作仓未跟踪新增 -> exit 1 + MISSING_IN_PUBLISH + 理由未跟踪  —— exit=1
[PASS] 9 --tracked-only（旧口径）对同一文件 exit 0 = 复现盲区  —— exit=0
[PASS] 4 删掉该文件 -> exit 0（回归）  —— exit=0
[PASS] 5 工作仓已跟踪新增 -> exit 1 + MISSING_IN_PUBLISH + 理由已跟踪  —— exit=1
[PASS] 5b 差异行同时给出侧别（仅工作仓）
[PASS] 6 发布仓单侧新增 -> exit 1 + MISSING_IN_WORKSPACE + 侧别仅发布仓  —— exit=1
[PASS] 7 两仓都有但内容不同 -> exit 1 + CONTENT_DIFF  —— exit=1
[PASS] 8 排除项不参与差异判定 -> exit 0  —— exit=0
[PASS] 8b 报告列出排除规则 × 侧别（含 docs/archive/* 与 *.bak*）
[PASS] 8c 排除合计里有「仅单侧」计数（不静默吞掉）
[PASS] 10 pages.yml 多一个构建步骤 -> exit 2 且点名  —— exit=2
[PASS] 11a 排除撞上纳入清单 -> 必须报  —— [('tools/credibility_gate.py', '该路径在纳入清单内（TOOL_FILES / BOUNDARY_FILES），却命中了排除规则')]
[PASS] 11b 排除撞上未豁免触发器 -> 必须报  —— [('data/modes_data.json', '该路径是 pages.yml 的 paths 触发器（可能改变线上），却命中了排除规则')]
[PASS] 11c EXCLUDED_TRIGGERS 里已豁免的路径 -> 不报  —— []
[PASS] 12 workspace 与 publish 同仓 -> exit 2（自比会让单侧检测恒为 0、假 OK）  —— exit=2
[PASS] 12b 换回正常两仓 -> exit 0（守卫不误伤）  —— exit=0
[PASS] 13 check_repo_parity.py 与 test_check_repo_parity.py 均在 TOOL_FILES

19/19 passed
exit=0
```

## 8. 自比守卫：从发布仓根不带参数执行

```bash
cd /opt/data/release/Protreptic-publish && python3 tools/check_repo_parity.py
```

输出（exit=2；若不拦，这里会拿发布仓和它自己比、恒零差异 = 假 OK）：

```text
[FAIL] workspace 与 publish 指向同一个仓: /opt/data/release/Protreptic-publish; 自比会让单侧检测恒为 0、输出假 OK,请显式指定另一侧的仓根
exit=2
```

## 9. 两仓同步与 CI

（提交哈希、`git status -sb` 无 ahead、CI 四个 workflow 结论由交接摘要给出。）

机检本体与自测都在构建图内（`TOOL_FILES`），因此本卡的改动受同一口径约束：两仓脚本字节一致才可能零差异。

