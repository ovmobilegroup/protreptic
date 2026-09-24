# Phase21-W7 清档合批·独立 QA 报告（卡 t_06511a5a / espinosa）

- 被验收：t_d24e11bc（W7 遗留清档合批）产物 -- ws `f61f055d` + `7714c9d1`；pb `c167cb5`（已推 origin/main）
- 日期：2026-09-24　独立面：一切自原始数据与 git 对象重演；不采信上游自述与报告结论（先例 t_ff294775 / t_8bad8d98）
- 校验器：`tools/verify_phase21w7_cleanup_qa_espinosa.py`（20 断言；`--quick` 19 断言模式）

## 0. 结论：PASS

20/20 独立断言全过（full rc=0）；分层抽样 303 件逐件复跑 0 失配；隔离副本 12 步（8 链 + 4 门禁）rc=0；见证器 10/18 与上游一致且 8 项 FAIL 已逐项独立归因（见证器陈旧，非回归）；提交面 3 笔无越界。发现 5 件均为低危/登记类，无硬伤。

## 1. 方法与独立面

- 全量重导（非抽样采信）：分类 JSON（1351 条） x 备份树（ws 1309 / pb 674） x git 对象（e5ddd13f^ / f61f055d^ / c167cb5^） x 发布仓 x 工作表。
- 隔离副本：`scratch/qa_w7/iso`（989MB，排除 .git/node_modules/venv），链与门禁在副本内复跑，零污染主仓。
- 引用复扫：双层（含 gitignored 工作树）全库正则 + token 边界/解析判定，ws+pb 双面。
- 零写入边界：仅新增 3 件本卡 QA 产物（本报告 .md/.json + 校验器脚本），其余零改动。

## 2. (1) 分类裁定复核（分层抽样 + 逐件复跑）

| 层 | 全量 | 抽样 | 占比 | 逐件复跑 | 结果 |
|---|---|---|---|---|---|
| 根数据件 | 632 | 125（含全部 22 无孪生件） | 19.8% | 备份前像 sha256==git blob + HEAD 缺席 | 0 失配 |
| tools/json | 670 | 129（含全部 21 子目录件） | 19.3% | 同上（子目录件 basename 归位核验） | 0 失配 |
| 异常名杂物 | 6 | 6（全查） | 100% | 备份/内容/残留痕迹 | 5 有据 + 1 登记（见 F1） |
| R7 件 | 5 | 5（全查） | 100% | 三面缺席（ws/pb/原路径）+ 备份归属 | 全过 |
| backup 目录 | 33 | 33（全查） | 100% | 存在性 + 归属（30 tracked / 3 未跟踪登记） | 全过 |
| 保留件 | 5 | 5（全查） | 100% | ws/pb 在场 + byte-equal | 全过 |

- 抽样合计 303 件；校验器复跑模式另行抽样 237 件（根 125 / tj 112，阈值 >=95/>=101 满足）。
- canonical/孪生对照为**全量**逐条复核（非抽样）：根面 byte-equal 声明 1079 条 ok=1079；工具面 1162 条 ok=1141 + 21 条子目录 basename 归位核销 = 1162，false=0；发布侧同路径 670/670；22 件无孪生逐件给出 basis 并与全域同名搜索对照（命中均为归档/备份类，非现役读者）。
- 裁定站得住脚：抽样件 basis 均为「字节孪生 byte-equal」或「零构建价值+零指向根件读者」类，逐件复跑与 canonical 对照一致。

## 3. (2) 删除面全量（byte-exact 前像 + MANIFEST + 裁定依据）

- tracked 1309 = 根 632 + tools/json 670 + `, ` 1 + 异常目录内 6；异常目录本体 5 个未跟踪树随删。
- 前像 byte-exact（QA 全量重启 `git cat-file --batch` 复核）：ws 1309/1309、pb 674/674（含 R7 同族补录 4 件），0 mismatch / 0 missing；缺席复核 ws+pb 全过。
- MANIFEST 逻辑 1983 行（sha256 + rel + size）逐行验证：1984 物理行 = 8 件非常规名折算（7 件含空格 + 1 件含换行名占 2 行），0 缺件、0 坏值。
- 裁定依据：分类 1351 条逐件条目化（根/异常/工具面/R7/备份目录/保留），6 件嵌套杂物按目录级 basis 覆盖（F2 已登记）。
- 可回滚性：`cp -a` 备份树即还原（保结构）。

## 4. (3) 保留面与构建图

- parity 工具现跑：边界自检通过（pages.yml 16 构建步骤 / 30 触发器全被清单覆盖）；两仓 4580 条，逐字节一致 4579，仅单侧 0；唯一 CONTENT_DIFF = `docs/architecture/static_data_manifest.json`（他卡在途构建产物，非本卡面）。rc=1（<=2，未触碰边界告警）。
- 保留件：`.markdownlint.json` / `lighthouserc.json` / `tools/json/{scenarios_zh,scenarios_en,scenario_tags}.json` 两仓在场且 byte-equal。
- 隔离副本链 8 步 rc=0：build_figures_db -> export_static_site -> gen_web_site_counts -> build_daily_index -> pages_preflight(data) -> build_search_index -> build_graph_data -> build_unified_index；产物断言全过（1357 件 / figures=1027 / 发布口径 modes=3241 / 隔离 60 / by-figure=320）。

## 5. (4) 全仓残留复扫（含 gitignored）

- LIVE 面命中 ws=955 行（tools 915 / scripts 20 / api 7 / web-other 7 / cli_tests 6；web/src 与 .github 0）。
- **硬残留 0**：即「引用指向本卡删除面路径且不可解析」-- 构建图内 0 条；LIVE 面全部经 token 边界 + 解析判定：解析至现存件 23 处（如 data/、tools/json 保留件）、预存陈旧 5 处（api/cli_tests 引 `tools/<name>` 旧路径，e5^ 前即缺失，非本卡所为，登记）。
- 构建图内 12 处命中全部无害：build_figures_db find() 回退候选 / check_repo_parity 自身文档 / 两件保留 JSON 自内容。
- 其余大数命中（ws: audit 5210 / root-other 3377 / backup 2598 / docs 2136 / site_docs 1866 / release 203 / data-other 145 / web-product 7 / root-config 2）全在 archival 类：分类与回执登记、备份镜像、旧快照、docs 提及、一次性脚本（逐类样例见证据 JSON）。

## 6. (5) 门禁/链复跑 + parity 实测 + 见证器 + 计数自洽

- 隔离副本 12 步 rc=0（8 链 + credibility_gate --hard-fail / verify_source_links --hard-fail / verify_findings --hard-fail / apply_verification_status --check）；计数与上游声明一致：figures 1027 / 隔离 60 / 发布 3241 / unified 1344（320+1024）/ search 16 分片。
- parity 实测：4580/4580（一致 4579，单侧 0，1 CONTENT_DIFF 归他卡）。
- 见证器 `verify_azj345_clear.py`：**10/18**（与上游一致）。8 项 FAIL 逐项独立归因（见 F4）：4 项计数类为锚陈旧（1056/1056/1388/1371 -> 现 1027/1027/1359/1344，W4 链重锚），4 项 live_zero/products 类为 r9 合法重落地 H-AZJ-001 推翻前提（实测产物含 H-AZJ-345=0 / H-AZJ-001=2）；`registry.zero_12`、`reverse.others_intact`、`archive.*`、`parity.key_files` 等 10 项 PASS。
- 计数自洽：窗口 e5ddd13f^..HEAD 删除 == 删除面 1309（精确相等）；本卡 3 笔提交新增全在面内（1984 + 4 + 1988）；工作区 tracked 差与删除面逐件对账一致（`git diff-tree` 集合等式，见校验器 A1）。

## 7. (6) 执行卡提交面审查（越界=硬伤）

| 提交 | 删除 | 新增 | 修改 | 结论 |
|---|---|---|---|---|
| ws f61f055d | 6（异常条目精确命中） | 1984（备份树 1980 + 分类 2 + 报告/证据 2） | 0 | 无越界 |
| ws 7714c9d1 | 0 | 4（pb R7 同族前像 4） | 1（MANIFEST 恰 4 行） | 无越界 |
| pb c167cb5 | 674（pb 全量） | 1988（BK 1984 + audit 2 + report 2） | 0 | 无越界 |

- 方向：ws master（本地） -> pb main（本地） -> 同推 github origin/main；pb 本地 HEAD 与 ls-remote 一致（含 c167cb5）。
- 镜像 byte-exact 抽验：分类 2 件 / 报告 2 件 / MANIFEST 共 5/5 ws==pb。

## 8. (7) 报告 pair 复核

- 上游报告 md / 证据 json / 分类 pair 与实测全量交叉，条目数 1351 一致；数字除 F3 所述时态滞后外全部吻合。
- 分类 md 与 json 对读抽核一致（根/异常/R7 层）。

## 9. 发现（全部低危/登记，无硬伤）

- F1（登记）：`(echo #!` 目录本体在备份树与登记表无痕迹（为内容片段级证据），维持如实登记；无处置建议。
- F2（登记）：6 件嵌套杂物按目录级 basis 覆盖，未逐件条目化（不构成数据风险，建议后续分类模板补充 dir->files 映射）。
- F3（低危）：上游报告/证据 pair 写于 f61f055d 时态（1979 行 / pb 670），+4 补录（7714c9d1）后未回填（终态 1983 / 674）。补录事实已由提交消息与完成元数据记录；建议下游文档卡（t_95764335）补注记。
- F4（低危）：见证器陈旧 10/18（锚 1056/1056/1388/1371 vs 现 1027/1027/1359/1344；r9 H-AZJ-001 合法重落地）。建议重锚或退役迁移，交船长处置。
- F5（低危）：MANIFEST 含 8 件非常规名（7 空格 + 1 换行），`sha256sum -c` 不可朴素消费；解析器需按「末段 size + 前段 rel」容错（本卡校验器已实现），回滚用 `cp -a` 不受影响。

## 10. 复跑

```
python3 tools/verify_phase21w7_cleanup_qa_espinosa.py           # full: 20/20 PASS, rc=0
python3 tools/verify_phase21w7_cleanup_qa_espinosa.py --quick   # quick: 19/19 PASS
```

## 11. 回执

（提交面实测补记见 commit B；本报告与其 JSON 同批镜像发布仓，byte-exact。）
