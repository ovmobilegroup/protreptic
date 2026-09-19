# Phase37-X4 交付报告：两仓一致性口径按构建图重定义并执行

- 卡：`t_376fb4aa`（[Phase37-X4] 按构建图重定义并执行「两仓一致」标准，替换 Phase36-W4 过宽口径）
- 日期：2026-09-19
- 两仓：workspace `/opt/data/workspace/Protreptic`（`master`）· publish `/opt/data/release/Protreptic-publish`（`origin main`，驱动 https://ovmobilegroup.github.io/protreptic）
- 产物：
  - `tools/check_repo_parity.py`（可复跑机检脚本，两仓同源）
  - `docs/planning/credibility_framework.md` §9「两仓一致性口径：按构建图推导（Phase37-X4）」
  - 本报告

## 1. 结论（一句话）

Phase36-W4 的验收口径「两仓 **2363 个 tracked 文件全字节一致**」**是错的**（开发仓 vs 发布仓角色不同：
`Dockerfile.web` / `api/*.py` / `.github/workflows/*` / 部分 `docs/*` 本就允许不同）。本卡改为
**「凡进入站点构建图或线上站点的文件必须字节一致」**，按发布仓 `.github/workflows/pages.yml` 推导出
**1307 个**构建图文件，逐文件 sha256 比对 → 修平 **35 处真实差异** → **两仓 1307 个文件全等（机检 exit 0）**；
不一致时的检出能力用「人为改 1 个文件 → CONTENT_DIFF + exit 1」实测自证。

## 2. 构建图文件集（推导依据）

推导链与清单见 `docs/planning/credibility_framework.md` §9.2。要点：

| # | 依据 | 纳入 |
|---|---|---|
| 1 | pages.yml build job 的 16 个 `python3 tools/<x>.py` 步骤 | 16 个构建脚本 |
| 2 | 其本地 import 闭包 | `tools/site_counts.py`、`tools/_quarantine.py`、`tools/credibility_baseline.py` |
| 3 | `on.push.paths` 的 tools/* 触发项 | `prerender_body.py`、`og_image.py`、`build_pwa_icons.py`、`subset_og_font.py` |
| 4 | `ci-cd.yml` test job 的门脚本 | `tools/verify_findings.py` |
| 5 | 脚本读的数据/资源 | `data/**`、`tools/json/scenarios_{zh,en}.json`、`tools/json/scenario_tags.json`、`tools/scenario_tags.json`、`tools/assets/fonts/**` |
| 6 | `mkdocs build -f mkdocs.pages.yml` | `docs/**`（除 `exclude_docs: archive/`）、`docs_overrides/**`、`mkdocs.pages.yml` |
| 7 | `npm run build`（Vite） | `web/**` |
| 8 | 机检脚本自身 | `tools/check_repo_parity.py` |

边界是**可机检**的：脚本每次运行现场解析 `pages.yml` 的构建步骤与 `paths` 触发器，任何新增而未被清单覆盖
→ `exit 2`「边界过期」（见 §5 实测）。

## 3. 机检脚本 `tools/check_repo_parity.py`

```
python3 tools/check_repo_parity.py            # 人读报告；--json 机读；--list 打印纳入/排除清单
退出码：0 = 零差异；1 = 有差异；2 = 边界过期 / 环境不满足
```

实现要点：`git ls-files` 枚举**跟踪文件**（未跟踪/被 .gitignore 的构建产物天然不进集合；新增文件需先
`git add`）；逐文件 sha256；缺一侧报 `MISSING_IN_WORKSPACE` / `MISSING_IN_PUBLISH`，内容不同报
`CONTENT_DIFF`；排除规则每条都带理由（§9.3）。

## 4. 修平的 35 处真实差异（逐条给方向与依据）

修复前实测（`python3 tools/check_repo_parity.py`，退出码 1）：

```
[boundary] workspace = /opt/data/workspace/Protreptic
[boundary] publish   = /opt/data/release/Protreptic-publish
[boundary] pages.yml 构建步骤 16 个 / paths 触发器 30 条 —— 均已被清单覆盖（边界自检通过）
[boundary] 纳入边界：workspace 1303 / publish 1304；排除：workspace 27 / publish 677
[DIFF] 35 处差异：
   CONTENT_DIFF           docs/00-quick-start/thinking_mode_quick_start.md
   CONTENT_DIFF           docs/02-tools/figure_library.md
   CONTENT_DIFF           docs/06-ai-collaboration/thinking_mode_ai_templates.md
   CONTENT_DIFF           docs/07-coaching/thinking_mode_coach_guide.md
   CONTENT_DIFF           docs/07-coaching/thinking_mode_evolution_portfolio.md
   CONTENT_DIFF           docs/07-coaching/thinking_mode_journal.md
   CONTENT_DIFF           docs/09-evolution/knowledge_system_evolution.md
   CONTENT_DIFF           docs/09-evolution/knowledge_system_navigation.md
   CONTENT_DIFF           docs/09-evolution/thinking_knowledge_update_guide.md
   CONTENT_DIFF           docs/09-evolution/thinking_skills_usage_guide.md
   CONTENT_DIFF           docs/10-community/thinking_community_ops_plan.md
   MISSING_IN_WORKSPACE   docs/_config.yml
   CONTENT_DIFF           docs/architecture/v7_validate.py
   CONTENT_DIFF           docs/architecture/web_pages_migration_assessment.md
   CONTENT_DIFF           docs/batch_import_56_runbook.md
   MISSING_IN_PUBLISH     docs/figures/CD-CD-001_朝代人物档案.md
   CONTENT_DIFF           docs/figures/H-AN-001.md
   CONTENT_DIFF           docs/figures/H-CY-001.md
   CONTENT_DIFF           docs/figures/phase20_wangxiang_research.md
   MISSING_IN_WORKSPACE   docs/index.md
   CONTENT_DIFF           docs/islam_phase2_review_report.md
   CONTENT_DIFF           docs/phase20_gai_zi_research.md
   CONTENT_DIFF           docs/planning/file_checklist.md
   CONTENT_DIFF           docs/planning/phase4_summary.md
   CONTENT_DIFF           docs/research/candidates_research.md
   CONTENT_DIFF           docs/research/phase20_chaodai_archive_report.md
   CONTENT_DIFF           docs/research/phase20_dongzhongshu_archive_report.md
   CONTENT_DIFF           docs/research/phase20_kongzi_archive_report.md
   CONTENT_DIFF           docs/research/phase20_kuizi_archive_report.md
   CONTENT_DIFF           docs/research/phase20_lizhe_archive_report.md
   CONTENT_DIFF           docs/research/phase20_wangchong_archive_report.md
   CONTENT_DIFF           docs/research/phase2_detailed_research.md
   CONTENT_DIFF           docs/review/blockers_20250726.md
   CONTENT_DIFF           docs/review/consistency_review.md
   CONTENT_DIFF           docs/review/qa_report_20250726.md
```

方向判定（**逐条判角色**，不是无条件单向覆盖）：

| 类别 | 数量 | 方向 | 依据（原始证据） |
|---|---|---|---|
| 内容差异：发布仓侧已完成「个人引用 / 本机绝对路径清理」 | 32 | **publish → workspace** | 32 个文件在 workspace@HEAD 里共命中 `/opt/data/workspace/Protreptic` **76** 处、`figo` **17** 处、`/opt/data/kanban/...` **10** 处；发布仓同文件命中 **0 / 0 / 0**（改为 `<repo>` / `Protreptic` / `<internal>` 占位）。例：`docs/02-tools/figure_library.md` 的 `/opt/data/venvs/protreptic-api/bin/python load_v6.py` → `python load_v6.py`；`docs/review/consistency_review.md` 的 markdownlint 说明改成与实际编号一致 |
| `docs/index.md`、`docs/_config.yml` 只存在于发布仓 | 2 | **publish → workspace** | 二者是文档站**首页**与 Jekyll 时代配置；`tools/pages_preflight.py:236` 明确断言 `docs/index.md` 与 `_site/docs/index.html` 的对应关系，`tools/apply_site_counts.py` 把 `docs/index.md` + `docs/02-tools/**` 当产品门面页硬门——workspace 缺它们等于缺首页 |
| `docs/figures/CD-CD-001_朝代人物档案.md` 只存在于 workspace | 1 | **workspace → publish** | 它是被**已发布**页面 `docs/research/phase20_chaodai_archive_report.md` 引用的归档人物档案页，属 `docs/**`（进构建、上线）；发布仓缺它 = 线上少一页。内容实测无内部路径/个人引用（`grep -n "/opt/data\|figo"` 0 命中），可直接发布 |

同步完成后重跑（workspace 侧）：

```
[boundary] 纳入边界：workspace 1307 / publish 1307；排除：workspace 27 / publish 677
[OK] 零差异：1307 个构建图文件两仓逐字节一致（sha256）
```

发布仓侧同一条命令（在 publish 目录内跑，`--workspace` 默认解析为自身）同样 `[OK] 零差异`、退出码 0。

## 5. 检出能力自证（人为破坏 → 必须红）

### 5.1 改 1 个文件 → CONTENT_DIFF + exit 1

```
$ printf "\nTAMPER-X4-TEST\n" >> docs/review/qa_report_20250726.md
$ python3 tools/check_repo_parity.py
[DIFF] 1 处差异：
   CONTENT_DIFF           docs/review/qa_report_20250726.md
EXIT=1
$ cp <publish>/docs/review/qa_report_20250726.md docs/review/qa_report_20250726.md   # 还原
$ python3 tools/check_repo_parity.py
[OK] 零差异：1307 个构建图文件两仓逐字节一致（sha256）   EXIT=0
```

### 5.2 边界过期 → exit 2（新增构建步骤没进清单）

```
# 造一个假发布仓：pages.yml 里多一个 `run: python3 tools/fake_new_step.py`
$ python3 tools/check_repo_parity.py --publish /tmp/x4/fakepub
[FAIL] 边界过期：pages.yml 有构建步骤不在本清单 → 请更新 tools/check_repo_parity.py
        未纳入: tools/fake_new_step.py
EXIT=2
```

即：**边界不是一张口头清单，它跟着 workflow 走**；将来谁往 `pages.yml` 加步骤，机检立刻报「边界过期」。

## 6. 排除清单（供 QA 复核）

完整清单与理由见 `docs/planning/credibility_framework.md` §9.3；数量实测：publish 侧排除 **677**
（637 `data/intl_figures/**` + 34 `docs/archive/**` + 5 `web/dist/**` + 1 `*.bak*`），workspace 侧排除 **27**
（12 `*.bak*` + 10 `data/backup_merge_*` + 3 `data/merge_staging_*` + `data/all_sources.json` +
`data/semantic_index.faiss`），另有两仓都不跟踪的 `web/public/data/**`、`tools/assets/fonts/.cache/**`。

其中**唯一需要 QA 关注的口径判断**：`data/intl_figures/**`（**637 个文件只在发布仓**）。按本卡标准
「进入构建图或线上站点」判定为**排除**，证据：`grep -rIl "intl_figures" tools/ .github/ web/src/` **0 命中**
—— 没有任何构建步骤/前端读它，不进站点。若 QA 采更严的「数据源留档」口径，处置是单向补齐：
`cp -r <publish>/data/intl_figures <workspace>/data/` 并提交（不在本卡范围，未擅自扩大改动面）。

`pages.yml` 的 30 条 `paths` 触发器里，仅 2 条不属构建图，理由写死在脚本 `EXCLUDED_TRIGGERS`：
`.github/workflows/pages.yml`（编排本身；两仓职责不同）、`api/protreptic.db`（CI Step 0 由
`build_figures_db.py` 清表重建；实测两仓 sha 相同但 committed 内容不进构建结果）。

## 7. 双仓同步与 push

| 仓 | commit | 内容 | push | `git status -sb` |
|---|---|---|---|---|
| publish | `7629f9e`（同步提交；其后为报告修订提交 `869c86d` 等，末次以 `git log -1 -- docs/qa/phase37_x4_repo_parity.md` 为准） | 32 个 docs 保持发布仓版本 + `docs/figures/CD-CD-001_朝代人物档案.md` 新增 + `tools/check_repo_parity.py` + §9 + 本报告 | `d25d4a7..7629f9e  main -> main` | `## main...origin/main`（**无 `[ahead N]`**，`rev-parse HEAD == origin/main`） |
| workspace | `a6e183ce`（同步提交；其后为报告修订提交 `4ca6f6e6` 等，末次以 `git -C <workspace> log -1 -- docs/qa/phase37_x4_repo_parity.md` 为准） | 34 个 docs 回灌 + `docs/index.md` + `docs/_config.yml` + `tools/check_repo_parity.py` + §9 + 本报告 | 无 upstream（`master` 为本地开发分支，远端只有 `refs/heads/main`，实测 `git ls-remote origin` 仅 HEAD/main；X3/X5 亦同） | `## master`（无 upstream 标记） |

说明：workspace 的 `master` **没有也不打算 push**（远端只有 `main` 一条分支；X3/X5 亦同）。
本卡纪律「push 后无 [ahead N]」在 **发布仓 main** 上验证。

## 8. 遗留 / 风险（如实记录）

1. **`data/intl_figures/**` 口径**（§6）：本卡按构建图判定排除；若 QA 要更严口径，需单向补齐 637 个文件。
2. **本机绝对路径清理只覆盖了 32 个文件**：其余发布文档里仍有类似痕迹（例：`docs/architecture/web_p0_architecture.md`
   `docs/architecture/phase30_a4_pwa.md` 仍写 `/opt/data/workspace/Protreptic/...`，**两仓一致**因而不属
   「漂移」，但属「公开面清理」欠账）。属另一条工作线，本卡不动。
3. **`docs/planning/credibility_framework.md` 是并发热点**：并行卡 Phase37-X5（`t_fd9210a5`）刚在同一文件
   追加了 §8；本卡只在文件**末尾追加 §9**，且提交前复核了 §8 仍在（`grep -n "^## "` 实测 0–8 节齐全）。
4. **机检不看未跟踪文件**（设计如此）：若某卡新增构建图文件而没 `git add`，机检当次不会报；`git add` 后即纳入。
5. **发布仓 markdown-lint 仍是存量红（与本卡无关，未动）**：本地同版本实测
   `npx markdownlint-cli2@0.11.0 --config .markdownlint.json "**/*.md"` → `Summary: 2 error(s)`（233 个文件），
   两条都在 `docs/qa/phase37_x2_evidence.md`（`:9:16` MD038、`:378:42` MD009，X3 报告已记录）。本卡改动的
   34 个 md 单独实测：`npx --yes markdownlint-cli2@0.11.0 --config .markdownlint.json <34 个文件>` →
   `Linting: 31 file(s)`（`docs/figures/**` 被配置排除）、**`Summary: 0 error(s)`** —— 没新增 lint 债。
   没去改别人的**证据文档**（原始输出里的空格属证据，第三方不宜代改）。

## 9. 最终验证（真实 CI run + 线上回读）

push `7629f9e`（发布仓 main）触发的 GitHub Actions（`api.github.com/repos/ovmobilegroup/protreptic/actions/runs` 读回）：

| run id | 工作流 | 结论 | 关键步骤 |
|---|---|---|---|
| 35451940858 | Deploy to GitHub Pages | **success** | build job **32 步全绿**（可信度门两档 → 链接核验两档 → 重建 db → export → 计数模块 → 每日索引 → data 断言 → 检索/图谱/统一索引 → SPA 构建 → dist 断言 → og 图 → 预渲染 → og meta → 计数收口 → sw → sitemap → **mkdocs 文档站** → 合并 SPA+docs → 产物断言）；deploy job success |
| 35451940861 | Protreptic CI/CD | **success** | test job 15 步全绿（可信度门·新增违规必红、链接核验·新增坏链必红、负对照自测、findings 两档自检）；API / Web 镜像构建 success |
| 35452121048 | Quality Gate | **success** | workflow_run 触发 |
| 35451940887 | CI（markdown-lint） | failure | **存量红，非本卡引入**：本地同版本复现同一结论（仅 `docs/qa/phase37_x2_evidence.md` 两条：`:9:16` MD038、`:378:42` MD009）；本卡 34 个 md 单独 lint = `Summary: 0 error(s)`。该红在 `d25d4a7` / `9235ba6` / `7d6af41` 上同样存在 |

线上回读（原始命令与输出）：

```
$ curl -s -o /dev/null -w "%{http_code} %{size_download}\n" -L <url>
https://ovmobilegroup.github.io/protreptic/                                200 4373
https://ovmobilegroup.github.io/protreptic/docs/                           200 166640   # 文档站首页（<title>Protreptic · 思想典藏</title>）
https://ovmobilegroup.github.io/protreptic/docs/figures/CD-CD-001_%E6%9C%9D%E4%BB%A3%E4%BA%BA%E7%89%A9%E6%A1%A3%E6%A1%88/   200 187395   # 本次新上线的归档档案页 = 反向同步生效
https://ovmobilegroup.github.io/protreptic/minds/H-P23F-001/               404 4340     # 伪人物深链仍 404（未回退）
https://ovmobilegroup.github.io/protreptic/figures/                        200 16968
https://ovmobilegroup.github.io/protreptic/data/meta.json                  200 3115
```

计数仍成立（线上 `/data/meta.json`，`generated_at = 2026-09-19T15:29:28+00:00` = 本次构建现场）：

```
mode_summaries_published: 2798      mode_by_figure_shards: 278
modes_raw: 2868                     modes_deduped: 2858      modes_quarantined: 60
sources["data/modes_data.json"].sha256 = bf168171af42f8148c3adecbbc1a71258522676355357f6466acdcb25f2e61cb   # 与 X1 记录一致
```

机检在最终状态下重跑（两仓各跑一次）：`[OK] 零差异：1308 个构建图文件两仓逐字节一致（sha256）`，退出码 0。

**关于卡片纪律 #4（前端改动须 `cd web && VITE_DATA_MODE=static npm run build`）**：本卡**未改 `web/**`**
（`git diff --name-only` 无 `web/` 前缀路径），本地 npm build 不适用；线上发布链里的同类构建**在 CI 真跑并全绿**
（Pages run 35451940858 的 step 17「构建 SPA」= `npm ci && npm run build`（`VITE_DATA_MODE=static`）+ step 18 dist 断言）。
