# Phase21-R9 沈复（H-SHF-001）重做链 · QA 独立验收报告（卡 t_83e0d68d）

- 日期：2026-09-24
- 验收对象：Phase21-R9 沈复重做链 1/4~3/4 全链产物（t_d78053e7 素材包 → t_b6d4c0ee 重建落盘 → t_a7d233f0 合并入主库，其余为链尾归档卡 t_7e5afcbb）
- 独立口径：全部判据重回原始文件——git 对象、工作树现值、合并前备份前像、重建落盘包（A1）、素材见证副本、站点产物、发布仓 git 对象；被验收方自述数字仅作对照登记，不作任何判据来源。
- 执行：`python3 verify_shenfu_qa_espinosa.py`（终轮全量：75 PASS / 0 FAIL / 5 INFO；证据 `phase21r9_shenfu_qa_evidence.json`，日志 16 件在 `phase21r9_shenfu_qa_logs/`，含修复前证据留痕）。

## 0 结论

**判定：PASS（终轮 75 PASS / 0 FAIL / 5 INFO）**，含 1 项 QA 闭合热修（发布仓补镜像链残留 2 件，见 §3）。

分组项表（80 行断言）：

| 组 | 范围 | 结果 |
| --- | --- | --- |
| A | 链与提交面（备份/现值/血缘/落盘包/归档/零夹带） | 8 PASS |
| B | 模式条目与 figure 逐条核对（10 条逐条 + 注册面 + 场景面 + 顶层块） | 30 PASS |
| C | 引文与见证面（35 条独立复算 + 清单核验） | 6 PASS |
| D | 站链面（preflight/新鲜 export/计数/扫描/隔离/锚点） | 10 PASS |
| E | parity / 镜像 / push 面 | 5 PASS + 1 INFO（E02b 工作树漂移登记） |
| F | 边界面（纯追加证明/邻居/并集护栏/代码面/旧壳/文档门面/备份） | 12 PASS + 1 INFO（F06b 存量行登记） |
| X | 交叉回归与门禁复跑（链自有脚本 + 四门禁独立执行） | 4 PASS + 3 INFO（X01/X02 白名单漂移、X02b 回滚登记） |

修复前命中（留痕）：E01/E02 FAIL——同一根因：发布仓缺链自身产物 2 件（§3）。修复后终轮 0 FAIL。

## 1 取证面与基线

- 工作仓 HEAD：8c486442（验收期间他卡继续落提交，链血缘不受影响）；发布仓 HEAD：54df4c4（本卡闭合热修提交，见 §3）。
- 链提交：e0a98aa8（素材包）→ 59bc5471 + a515badd（重建落盘）→ 5a657b81 + 906a0bee + c3cceb19（合并/回执/核验）→（兄弟卡后续 a96302f1/5ce7f6ad/8c486442，未触本链数据面）。
- 链产物集合（5 提交并集）83 件；合并前备份 `data/backup_merge_H-SHF-001_20260924_093849/`（六件前像 + ledger，未入库，按设计）。

## 2 分组明细（关键实证）

### A 链与提交面（8/8）
- 备份六件前像 sha256 与合并清单 inputs 6/6 一致；工作树现值与 after（清单/证据）6/6 一致，且逐件等于 5a657b81 blob、HEAD 与工作树零漂移。
- 血缘 e0a98aa8→59bc5471→5a657b81→906a0bee→c3cceb19→HEAD 全链可达；主提交 5a657b81 变更集恰好预期 24 件（extra=[] missing=[]，零夹带）；后续提交（含兄弟卡）未再触碰六件主库。
- 落盘包九件 sha256 9/9；figure/individuals 与 landing 冻结副本逐字节一致；归档旧件 H-HAN-001 三件 sha256 3/3 未动。

### B 模式条目与 figure 逐条（30/30）
- 10 条 M-SHF-001~010 逐条 deep-equal：主库 == 落盘 A1 entries == figure 档 modes == individuals modes == modes_library_entries（B02×10、B03）。
- figure 档：mode_ids 10、thinking_mode_count 10、生年 1763、caveats 8、core_thoughts 逐条含对应模式码；code_maps 注册 mode_ids/tags/xrefs 与图档逐字、xref 目标已注册（0 悬空）；figure_names 唯一映射 H-SHF-001→沈复（1085 键）；顶层块 H-SHF-001 与 top_block_proposal 逐字（23 键，位于 modes 前）。
- 场景面：zh 10 条逐条复算命中（title/application_area 取条目 modern_applications_*、text 按模板规则逐字重算）；en 10 条与 zh 同体仅 code 后缀（含 text_en 复算）；tags 20 条块连续、先 zh 后 en、figure_code 全为 H-SHF-001。

### C 引文与见证面（6/6）
- 素材报告引文 35 条（自有正则抽取）以自有强归一独立复算：35/35 命中见证副本（含芸字前缀回落口径记录）；`quote_verification_final.json` 35/35 全 found；`witness_sha256.txt` 清单 35 件逐件 sha256+size 全对；10 条 key_quote_zh 与 figure 精选引语均可回溯见证。

### D 站链面（10/10）
- `pages_preflight --stage data` 复跑 exit 0；**新鲜 export 逐字节复现已入库 web/public/data**（1358 件，meta 仅时间戳字段差异、daily 两件归 build_daily_index 口径，D05 单独校验）；计数 figures=1027 / dedup=3301 / published=3241 / 隔离=60 / by-figure=320 全复现。
- `gen_web_site_counts --check` exit 0（siteCounts.ts = 3241×320，源 3301）；`build_daily_index --check` exit 0（daily total 3241 / figure_count 320）；dist 1377 文件 + docs 产品门面 6 页扫描零违规；隔离 60 条 0 泄漏（含 figures.index 无隔离图码）；两脚本锚点 EXPECT_MODES/EXPECT_BY_FIGURE/EXPECT_FIGURES 一致且与实测相符。

### E parity / 镜像 / push（5 PASS + 1 INFO）
- parity（终轮实跑）：53 条差异逐条归因，**沈复链面 0 命中**（50 MISSING_IN_PUBLISH + 3 CONTENT_DIFF 全部为他卡在制，见 §5）；本卡 QA 产物 16 条在提交/镜像后消除。
- 镜像：链集合 83 件在发布仓逐字节齐备（82 原镜像 + 1 件由本卡热修补镜像；E02 match=83 missing=[] diff=[]，按工作仓 HEAD blob 口径）；2ec3af3/6d8797d/3b6874f 三镜像提交均在发布仓 HEAD 血缘内，2ec3af3 恰 81 件且六件数据 blob 与 after sha 一致。
- push：`git ls-remote origin main` 实测 = e6d133c4…（含链镜像 3b6874f 血缘）；发布仓工作树链面全净。

### F 边界面（12 PASS + 1 INFO）
- 纯追加证明（六件）：modes_data 前缀 3301 条逐字相等 + 尾插 10 条 + 新键仅 H-SHF-001 + total 随动；code_maps/figure_names/scenarios_zh/en/scenario_tags 均为「公共部分逐字未动 + 增量追加」。
- 邻居与并集：首 10 / 尾前 10 条目逐字未动；M-AZJ-001~010 与 H-AZJ-001 块/注册全在位（兄弟卡并集未受损）。
- 代码面扫描：43 命中全落白名单分类（本链面 50…含 web/public/data 站点面；兄弟链面 5；他卡扫描清单 1），0 意外；旧壳 H-HAN-001 零唤醒、旧码 M351~M358 零复用。
- 文档门面：figure_library.md 首行与 docs/index.md 首行已收口 320/3241；备份目录保持未入库。

## 3 修复前命中与 QA 闭合热修

- 命中（修复前）：E01/E02 FAIL——`docs/research/phase21r9_shenfu_sourcing_report.json/.md`（素材包 t_d78053e7 产物，经 e0a98aa8 入库，docs/** 属 parity 构建边界）未随合并卡镜像进入发布仓（2ec3af3 = 81 件 = 链集合 83 − 2），parity 报 MISSING_IN_PUBLISH ×2。
- 处置：本卡以 QA 闭合热修补镜像——逐字节复制 + 提交 **54df4c4**（发布仓），修复后 E02 链集合 83/83 byte-exact、parity 链面 0 命中。修复前/后证据分别留痕（`phase21r9_shenfu_qa_logs/evidence_before_fix.json` 与终轮 evidence）。
- 判据校准说明：修复后首全量轮出现 3 项 FAIL（D03 时间戳/产物边界口径、E01/E02 对共享生成件 `docs/architecture/static_data_manifest.json` 的并发侧写未归因），经判据修正（v1.1：时间戳掩码 + 产物分工口径 + 镜像比较改用 HEAD blob + 并发在制归因 + 自身侧写自动回滚）后终轮全绿；该 3 项均非链数据缺陷，判定过程与前后两轮全量留痕。

## 4 归因、残留与观察项

1. parity 终轮 53 条：16 条为本卡 QA 产物（提交/镜像后消除）；37 条为他卡在制——W8 Stage2 批1（24：recount/source_texts/booklist/sourcing 报告）、W4（6：qa_evidence/qa_report/fix_manifest/names_recon）、W6/W10 文档（4）、tools（3：build_source_links/source_link_index/fetch_source_texts，他卡在制改动）。清单见证据与日志。
2. X01/X02（链自有脚本交叉回归复跑，仅登记不判）：当前 73/1 与 51/2——失败点为他卡后续产物（AZJ 证据、W4 evidence）与本卡 QA 脚本落入其白名单外（G01/F05），非数据缺陷；本卡以 F04 分类白名单口径复核为 0 意外。是否扩展白名单交链尾卡/链主裁量。
3. docs/index.md 正文行「283 位人物…2848 条」为存量（前像同文；apply_site_counts 判定式不覆盖该措辞），非本链引入。
4. 存量 H-BG-001→H-HAN-001 悬空互引已由 R8 卡 t_8183b8fd（10ddc66f）清除，本轮实测 0 残留。
5. 并发写者：验收期间 t_02007da8（AZJ QA）与 t_def07a84/t_70a8cbce（elcano）在本工作区在制写入；本卡对自身侧写（scratch export 的共享 manifest、交叉回归复跑的链证据文件）已自动回滚（D03b/X02b），对他卡在制只登记不动。

## 5 承接（链尾卡 t_7e5afcbb 提示）

- 复核发布仓补镜像 2 件（§3，54df4c4）与本卡 QA 产物镜像；
- 九节档案登记本卡与修复记录；若要消除 §4.2 白名单漂移可选择性扩展（非必须）。

## 6 产物与回执

- 产物：`verify_shenfu_qa_espinosa.py`；`docs/research/phase21r9_shenfu_qa_evidence.json`；`docs/research/phase21r9_shenfu_qa_logs/`（16 件日志 + 修复前证据）；本报告。
- 工作仓提交 / 发布仓镜像 / push 回执：见 §7 补记与卡回执（metadata）。
