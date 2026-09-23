# Phase21-R8 C组遗留微收口：figure_names Modern 键清档 + 2 处悬空互引清除（卡 t_8183b8fd）

- 日期：2026-09-23（CST）；执行：elcano（工作仓 /opt/data/workspace/Protreptic）
- 授权 / 依据：卡面（magallanes）——R7 核名卡 t_261185a8 船长裁定 C 组 6 件（H-AN-001/H-LC-001/H-YE-001/H-ZOU-001/H-HAN-001/H-MODERN-002）维持归档后的遗留微收口（R7 报告 §4.1/§4.3 口径）；唯一依据 docs/research/phase21r7_cgroup_identity_report.md §3.1/§3.2/§3.5/§4 + 同名 .json；R6C 报告第八节口径
- 纪律：先取证后动手；前置条件（零活跃读者）核验通过才动手；逐键最小改动；备份而非删除；不碰 modes_data.json / 登记条目本身 / _duplicates
- 结论：**三项全部落地并闭环**——3 件数据逐键微改（删除行 2+5+5，新增行 0）；后像 0 残留；其余字段逐字节未动（语义等价 + 唯一块文本替换双证）；门禁四连 exit 0；站点链五步复跑 exit 0 且产物逐字段同前；两仓 parity 见 §7

## 1. 处置总表

| # | 路径 | 动作 | 前像 sha256（前 16） | 后像 sha256（前 16） | 行变化 |
|---|---|---|---|---|---|
| ① | data/figure_names.json | 清档机制键 Modern / MODERN → 「安子介」（旧管道遍历顺序定胜产物） | fa4b43d41a8c450e | 6c6c347eaa17e8eb | -2 / +0 |
| ② | data/code_maps.json | H-CY-001（陈云）cross_references 清除 target=H-LC-001 条目（原「陆沉侧重方法论层面的深度思维技术...」） | df62a33f96717026 | 29c133eb607b89c4 | -5 / +0 |
| ③ | data/individuals/H-BG-001.json | cross_references 清除 target=H-HAN-001 条目（原「班固与沈幅同处东汉时期...」）+ 末项逗号收口 | f374af6b7937dc2e | f8a9ae4aeaa5b6bd | -5 / +0 |

判定口径：三处互引/机制键所指向的件（H-LC-001 陆沉、H-HAN-001 沈幅、H-AN-001 安子）均经 R7 核名卡裁定**维持归档**（载荷零复用），故悬空互引与旧管道机制键一并收口；编号登记条目本身（figures/code_maps 条目、modes_data）一律未动。

## 2. 前置条件核验（① 零活跃读者）

卡面 ① 前置条件：「确认零活跃读者（grep 全仓代码面；credibility_framework.md 记载为遍历顺序定胜产物）——如查得任何代码读者，停下并报告，勿删」。核验四路：

1. **字面键 grep（全仓代码面）**：*.py/*.js/*.ts/*.sh/*.html/*.yml/*.yaml/*.toml 全扫（排除 .git / backup / node_modules / web_dist / site_docs）——**以字面键 Modern/MODERN 读取 figure_names.json 者 0 处**。命中项全为「era 时代字面量」（generate_tags / add_batch* / process_final_batch* / merge_* / translate_figure / api/routes/tags.py 时代枚举）或「文档注释/脏值分类清单」（credibility_gate.py 第 442-461 行、backfill_lifespans.py 第 12-14 行、audit_figure_fields.py 第 232/300 行——记载的正是该键系旧管道「13 个文件 figure_code 都写 Modern、胜者由遍历顺序决定」的争用产物）。
2. **读者面清点**：全仓加载 figure_names.json 的脚本 52 个 = 构建图 2 个（tools/figure_library.py、tools/build_unified_index.py）+ 一次性合并/归档/QA/verify 脚本 50 个。消费方式均为「以 figure code 为键查询映射」，**无字面键读取，无对 Modern 的数据遍历**。
3. **数据可达性**：data/modes_data.json 全部模式 figure_code 为 Modern/MODERN 者 **0 条**；活跃 data/figures/ 目录 figure_code=Modern 者 **0 件**（仅 _duplicates 归档件与备份）；data/individuals/ 侧有 3 件旧档 figure_code=Modern（H-WU-001 李达 / H-MODERN-001 陆一波 / H-QXS-001 钱学森），但 data/individuals **不在站点链/构建图读序**，其读者仅 parity 树走查与一次性脚本。
4. **解析模拟（526 码逐一）+ 前后实测**：复刻 figure_library 解析链与 build_unified_index 口径，对 526 个查询码（modes_data figure_code + figures 文件码）逐码解析——**前/后解析结果变化 0 条**；合并映射差异仅 Modern/MODERN 两键自身。实测读者运行：build_unified_index.py 产物 web/public/data/index.unified.json 前后 sha256 同为 21f028bcb61a1274...；figure_library.py --stats（3271 模式 / 322 人物）与 -L（322 位）前后逐字一致。

→ **前置条件成立：零活跃读者**（证据全文见 data/audit/phase21r8_cgroup_residual_evidence.json 的 reader_analysis；grep 原始输出留档于本卡运行 scratch）。

## 3. 逐项处置（前像 → 修改 → 后像复核）

### ①②③ 共同动作口径
- 前像：sha256 + bytes + git blob + 末次实质提交逐件登记（见证据 pre_images）；三件前像与发布仓同名现役件**逐字节同体**（改动前复核实测）。
- 修改：文本级「唯一块删除」（每处删除块在源文件内 count==1 唯一命中，命中失败即中止）——除目标块外**逐字节未动**（新增行 0）。
- 后像复核：0 残留（grep 复扫）；语义等价（后像 == 前像按目标键/条目差集）；json.loads 通过。

## 4. 备份与恢复（归档而非删除）

| 备份目录 | 内容 | 校验 |
|---|---|---|
| data/backup_phase21r8_cgroup_residual_20260923/ | figure_names.json.before、code_maps.json.before、H-BG-001.json.before + README.md（指纹表与恢复法） | 三件 copy 后 sha256 与前像**逐字节相等**（BYTE-EXACT 实测） |

恢复法：`cp data/backup_phase21r8_cgroup_residual_20260923/<f>.before <原路径>`；或 `git show <blob> > <原路径>`（blob：1d071b88... / 711c3e50... / fcc976ce...）。

## 5. 后像核验（0 残留 / 最小差异）

- 残留复扫（grep）：figure_names 精确键 `"Modern":`=0、`"MODERN":`=0；code_maps `H-LC-001`=0；H-BG-001 `H-HAN-001`=0、`沈幅`=0。
- `git diff --numstat`：0 +5（code_maps）／0 +2（figure_names）／0 +5（H-BG-001）——**新增行 0**，删除行恰为三处块。
- 语义等价：figure_names 后像 == 前像逐键去 2 键；code_maps 后像 == 前像（H-CY-001.cross_references[1:] 口径）；H-BG-001 后像 == 前像去该条目——三件全 PASS（独立核验脚本 r8c_verify.py：ALL-PASS）。

## 6. 门禁四连（改动后复跑）

| 门禁 | 结果 |
|---|---|
| `credibility_gate.py --hard-fail` | **exit 0**（存量冻结；D4/D5 非阻断提示照旧） |
| `verify_findings.py --hard-fail` | **exit 0**（2 条既有非阻断警告：audit sha 过期 / M-ASM 双采） |
| `apply_verification_status.py --check` | **exit 0**（库中状态逐条一致；公开 3211 + 隔离 60 = 3271） |
| `verify_source_links.py --hard-fail` | **exit 0**（UNREACHABLE 为既有存量警告） |

## 7. 站点链与两仓 parity（镜像 / 推送）

### 7.1 站点链（涉及面判定 + 复跑）

- 判定：data/figure_names.json 在构建图读序（tools/build_unified_index.py，pages.yml build job 步骤）——**涉及，复跑**；data/code_maps.json、data/individuals/H-BG-001.json 不在任何构建链读序（构建图工具零命中）。
- 复跑（改动后）：export_static_site → gen_web_site_counts（siteCounts.ts 未改动 3201 x 316）→ apply_site_counts（dist 扫描 1367 件零违规）→ build_daily_index（3201 条）→ pages_preflight --stage data：**五步全 exit 0**。
- 前后一致性：docs/architecture/static_data_manifest.json 两次链条运行**仅 generated_at 不同、counts/products/sources 逐字段全同**；build_unified_index 产物 index.unified.json 前后 sha256 相同。链条自身触发的 manifest 时间戳漂移已 `git checkout` 回滚，本卡提交不含非本卡改动。

### 7.2 两仓 parity 与镜像推送

- 工具：`tools/check_repo_parity.py`（两仓 1825 件，改动前实测 1825/1825 逐字节一致、仅单侧 4 条=本卡新备份目录未镜像）。
- 镜像：三个数据件 + 备份目录 + 证据 + 本报告同步发布仓（/opt/data/release/Protreptic-publish）；推送：发布仓 → 远端 main（工作仓无推送目标，依 R5/R6/R7 先例为本地提交）。
- 终态 parity 与 push 回执：见 §10 收尾回执（补记）。

## 8. 未处置清单（范围外发现，留船长/编排裁定）

1. **同一悬空互引的镜像/页面层副本**（卡面 ②③ 仅点名 code_maps 与 individuals/H-BG-001）：
   - H-LC-001 残留：data/individuals/H-CY-001.json（cross_references[0] + related_figures）、data/figures/H-CY-001.json（同二处）、docs/figures/H-CY-001.md；
   - H-HAN-001 残留：docs/figures/H-BG-001.md。
   上述件未在授权范围 → **未动**；如需同口径收口建议另卡。
2. **工具内历史文字**（非数据引用）：tools/audit_figure_fields.py（第 80/91 行 H-HAN-001 说明表）、scripts/validate_bg.py（第 66 行 NOTE，非构建图）——未动。
3. figure_names 其余 `Modern*` 机制键（14 键）与 data/individuals 三件旧 `figure_code=Modern` 字段：属其他清理线（tools/audit_figure_fields.py 脏值清单），未动。

## 9. 证据与复核路径

- `data/audit/phase21r8_cgroup_residual_evidence.json`（本卡结构化证据：前/后像、逐键删文、备份、读者分析、核验、门禁、站点链、parity、提交）。
- `data/backup_phase21r8_cgroup_residual_20260923/`（三件 byte-exact 前像 + README 指纹/恢复法）。
- 独立复核：① 三件后像 sha256 对照 §1 表；② `git show <blob>` 由历史复现前像；③ grep 复扫三处 0 残留；② 解析模拟脚本口径见证据 reader_analysis.simulation。

## 10. 收尾回执（补记）

- 工作仓交付提交（round 1：三件数据 + 备份目录 + 证据 + 本报告）：**10ddc66f**（2026-09-23 20:50:16 +0800）；round 1 交付件 sha256：报告 ac9cab42...（10013B）、证据 d857a87f...（10836B）。
- 发布仓镜像提交：**f1b02f3**（20:50:24 +0800）；推送回执：`646a9c7..f1b02f3  main -> main`；fetch 实测 origin/main == f1b02f3（ahead=0）。
- 终态 parity 复检（round 1 镜像后、本补记前时点）：**exit 1**；两仓 1831 条逐字节一致 1831；仅单侧 17 条（仅工作仓）= 兄弟 R8 卡在制未跟踪件（王祥 H-HZX-002 落地与 azj345 处置）；**本卡全部路径零差异**。
- 收尾口径：工作仓无 upstream/推送目标（remote.origin 仅 fetch）→ 推送 = 发布仓 → 远端 main；工作仓为本地提交（依 R5/R6/R7 先例）。
- 本补记（round 2：回执 + 证据 v2 同步）的提交号与推送回执、以及最终态 parity 数值：见 kanban 完成交接（t_8183b8fd metadata）与本卡评论。

---
*生成：elcano / t_8183b8fd；方法论：先取证后动手、前置条件（零活跃读者）先验、逐键最小改动、备份而非删除、读者影响以「解析模拟 + 前后实测」双证。*
