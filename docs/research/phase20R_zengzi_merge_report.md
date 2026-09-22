# Phase20R 合并报告：曾子 (H-ZX-001) 增量合并入主库

- **本卡**: t_16ebe5c9（[Phase20R 曾子补做] 数据合并，assignee: barbosa）
- **上游**: 落地卡 t_4a9c2c2e（elcano，commit `4f447608`）；研究卡 t_6c92966b（serrano）
- **下游**: QA 卡 t_8ceed107（espinosa）；文档归档卡 t_6c7e070a（pigafetta）
- **合并时间**: 2026-09-22 23:00（TS=20260922_230038）
- **合并脚本**: `merge_hzx_phase20R.py`（sha256 `176d692e...bd84`，全文见证据包附录 A）
- **合并前备份**: `/opt/data/kanban/boards/protreptic/workspaces/t_16ebe5c9/backup_merge_H-ZX-001_20260922_230038`（5 件）
- **核验**: `verify_hzx_merge_phase20R.py` **66/66 PASS**；上游回归 `verify_hzx_phase20R.py` 31/31、`verify_hzx_landing.py` 26/26

## 一、合并清单（before 到 after；纯追加、零删除、零改写）

| 文件 | 变更 | 计数 | sha256 (before 到 after) |
|---|---|---|---|
| `data/modes_data.json` | +10 条模式 M-ZX-001~010（`figure_code=H-ZX-001`，`research_mode_id` M230~M239 溯源保留） | 3142 到 3152 | `83be45b5` 到 `9d9c98c5` |
| `data/code_maps.json` | `figures.H-ZX-001` 首次注册（mode_ids 10 / tags 10 / cross_references 3） | 211 到 212 | `b7e590e7` 到 `b4a6cf13` |
| `data/scenarios_zh.json` | +10（C-ZX-001~010） | 2173 到 2183 | `f99c5a62` 到 `65a85dba` |
| `data/scenarios_en.json` | +10（C-ZX-001E~010E） | 2173 到 2183 | `bb9bfc28` 到 `af6ee58f` |
| `data/scenario_tags.json` | +20（zh/en 各 10，覆盖全部 10 mode_code） | 7258 到 7278 | `ce5557e5` 到 `5d36fae3` |

命令级：`git diff --stat` = 5 files changed, **1451 insertions(+), 0 deletions**。完整 sha256 台账见 `data/audit/phase20R_zengzi_merge_manifest.json`。

## 二、结构裁定（与本批先例 H-ZXC / H-DZ / H-WFZ / H-WYM / H-LJY 同构）

1. **模式条目**：逐字取自落地卡正本 `data/individuals/H-ZX-001_modes.json` 的 `modes` 十条（v6 全字段 + 落地留证字段 `attribution_note_zh/en`、`correction_zh`、`verification`，及 `legacy_field_aliases` 兼容别名）。库内 == 图档内嵌 `thinking_modes` == individuals 正本，**三面逐字同体**（核验 A10/A11）；`research_mode_id` 保留 M230~M239，与图档 `phase20.mode_id_mapping` 1:1。
2. **场景条目**：8 字段（`code/mode_code/title_zh/title_en/text_zh/text_en/application_area_zh/application_area_en`）；staging 的 `figure_code`、`tags_zh`、`tags_en` 按先例不落主库（标签由 `scenario_tags` 承载）。
3. **标签**：4 键 `{mode_code, tag, figure_code, language}`；`tag` = 模式中文名 + `_zh` / 英文名 + `_en`。
4. **code_maps**：3 键 `{mode_ids, tags, cross_references}`；交叉引用与图档逐条一致（H-KZ-001 继承 / H-MZ-001 学脉 / H-ZHX-001 道统），双判据可达（H-KZ-001、H-ZHX-001 未注册 code_maps 但有 `data/figures` 图档；H-MZ-001 两处皆在），**零悬空**。

## 三、唯一性与旧号禁令

- **新 id 零重复**：全库 `M-ZX-*` 0 到 10（无他人占用；落地前全库扫描 M-ZX-* 与 M-ZS-* 均 0 命中）；`C-ZX-*` 场景键 0 到 20；code_maps 新增唯一键 `H-ZX-001`。既有重复 id 集合 before == after（**零新增**）。
- **旧号禁令**：新增足迹（模式现役字段、双语场景、标签、code_maps 条目）零 `M230-M239` / `M-ZS-` / `H-ZS-001` / `M311-M318`；M230~M239 仅作为 `research_mode_id` 溯源字段出现（落地裁定授权，与图档映射表一致）。
- **未触碰的旧号遗留**（历史件，非本卡足迹）：根目录旧档 `modes_data.json`（101 人物块汇编，含曾子旧号块）、`data/figures/_duplicates/`、`backups/`、旧研究稿，均属落地卡残留清单 #16/#27 记录项。

## 四、纯追加证明（备份逐项比对）

- 模式：3142 到 3152；既有条目**前缀逐字全等**（0 改写）。
- code_maps：既有 211 figure 条目逐一全等；新增键仅 H-ZX-001。
- 场景：中英各 2173 到 2183；既有键逐一全等。
- 标签：7258 到 7278；既有 7258 条逐一全等（前缀全等）。
- 五文件 sha256 全部变更；增量 diff 零删除行。
- 合并脚本幂等护栏：已写入后重跑在第 2 步 preflight 即 ABORT（见证据包第 2 节）。

## 五、核验与回归

- 本卡独立核验脚本 verify_hzx_merge_phase20R.py：66/66 PASS
  （A 模式 19 项 / B 场景 13 项 / C 标签 7 项 / D code_maps 7 项 / E 库级与备份比对 10 项 / F 图档与登记 7 项 / G 引用面 1 项 / H 上游回归 2 项）。
- 上游脚本按合并后口径更新 2 处（先例：落地卡对引用面白名单的口径更新，其余断言未动）：
  - phase20R 上游核验脚本：引用面白名单并入主库写入面与本卡产物，31/31 通过。
  - landing 上游核验脚本：main library untouched 断言（落地卡时点口径）更新为主库已携带 M-ZX-001~010（合并卡 t_16ebe5c9），26/26 通过。
- 图档三镜像 sha256（ba2ad769 前缀，e08161b3 后缀）本卡零改写，与落地 manifest 记录一致。

## 六、遗留与热点
- 热点（多卡共享大文件）：五件主库共享文件，本卡仅追加自身足迹、未改他人条目（备份比对逐项全等）。
- 站点计数锚点（工具层，待站点链条卡）：export_static_site 与 pages_preflight 的 EXPECT_MODES 3132 应随重建更新为 3142（去重口径）、EXPECT_BY_FIGURE 304 更新为 305；先例：Phase 20 各合并卡 +10 未改锚点，由 Phase21-R 于 2026-09-22 收敛 +80 并更新为 3132/304。
- 两仓 parity：workspace 当前领先发布仓（含落地卡与合并卡改动）；发布仓镜像与 push 属发布/站点卡范围，本卡未写发布仓。
- total 字段：库内 total 2948 与 len(modes) 3152 并存（漂移 204，其中 194 为 Phase21-R 恢复未回填、10 为本批）；本卡零写入该字段，如需归一建议由收尾卡一次性裁定。
- 另卡记录项（本卡未动）：web 层 H-ZZ-166 与 H-ZZ-222 数字码映射（残留清单 #13）；H-LJY-001 与 H-PGR-001 对 H-ZX-001 的交叉引用核对（#19/#20）。

## 七、证据

- docs/research/phase20R_zengzi_merge_evidence.txt（命令级证据：dry-run 幂等护栏、三脚本输出、sha256 台账、git diff 片段、合并脚本全文）
- data/audit/phase20R_zengzi_merge_manifest.json（机器可读清单：计数、前后 sha256、备份 sha256、纯追加证明）
- 合并前备份（5 件）：备份目录见本报告头部，可由合并卡工作区随任务附件保留。
- 残留清单 #16 未闭环（交接项）：根目录旧档 modes_data.json（610KB 级、101 图块汇编、内嵌曾子旧号块 M230-M239）原记 action 为「由落地卡 t_4a9c2c2e rebase 到 M-ZX-001~010」，落地卡只隔离了根副本 H-ZX-001.json 与 H-ZX-001_modes.json，未动该档。本卡按「主库=data 目录五文件」口径零写入该档，旧号禁令按新增足迹执行（现役字段零旧号）。该档为独立历史汇编件（列表结构，与主库 dict 结构不同），建议由编排另立清理卡复核 #16 归宿。
