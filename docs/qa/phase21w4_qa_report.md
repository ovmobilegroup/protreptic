# Phase21 W4 名录修复·独立 QA 报告（卡 t_8bad8d98）

- QA：espinosa（第二实现·不信任自述）｜前置链：t_536073f4（fix）→ t_ee203180（清档）→ t_33240de8（fix2 补正）
- 日期：2026-09-24｜核验时点：工作仓 HEAD=2de84904（fix2 终版；v3 复跑时点见 §九）/ 发布仓 origin/main=c646f41a5c4fc65027d403cf448c847fc4756060
- 见证器：`verify_phase21w4_qa_espinosa.py`（77,374 B，纯 stdlib，可复跑；v3 起含板面并发漂移归因，见 §九）｜证据：`docs/qa/phase21w4_qa_evidence.json`｜日志：`docs/qa/phase21w4_qa_run_final.log`

## 一、结论（先说结果）

**总判定：PASS（通过）。全量复跑 137 项断言 / 0 FAIL / 0 SKIP（约 250s）。v3 复跑（板面并发下，10:23）：140 断言 / 0 FAIL / 44 DRIFT 登记（292s），归因明细见 §九/§十。**
所有判据一律取 git 对象、原始文件字节与工具实跑输出（含 ws+pb 两仓、含 gitignored 全仓二进制扫描），未采信上游自述或报告结论。

逐项吻合：21 码 name 回填（14 层逐码终表）｜SG/MY 旧草稿 + RW-KAG-1..27 全链 0 残留｜JP-SAS-001/UZ-ULU-001 重键完整｜备份 byte-exact（fix 11/11、fix2 4/4、rwkag 89/89 + 抽样 9/27）｜计数自洽（1027/1358/1359/1342/3221）｜W4 窗口 135 路径零越界/零删除｜门禁 6 工具 rc=0 + 上游见证器复跑｜官方 parity 2395 逐字节 + 远端回执复核（git fetch 实测）｜H-MZ-001 R1/R3 一致｜G 类终态｜R2 zh 补正链（fix2 范围）四项全核。

如实登记 4 项注记（均非链缺陷、非返工项）：注记 A 上游见证器 QA 自体命中；注记 B `minds/H-WC-001` body_text_chars 4210→4209 未在 W4 报告逐键登记（QA 独立根因）；注记 C R-d 两异常目录与链账务不符（已不在，无数据影响）；注记 D B-a 已由船长裁定（转 t_def07a84）。

## 二、产物（must_write 对应）

| 产物 | 路径 | 校验 |
|---|---|---|
| 独立见证器（可复跑断言） | `verify_phase21w4_qa_espinosa.py` | `python3 verify_phase21w4_qa_espinosa.py [--quick]`，exit 0/1 |
| 证据 JSON（逐条断言+计数+环境） | `docs/qa/phase21w4_qa_evidence.json` | 137 断言全记录 |
| 全量运行日志 | `docs/qa/phase21w4_qa_run_final.log` | 与证据同源 |

## 三、范围与口径

- W4 窗口 = `40320e37..2de84904`，10 提交：
  - fix 链（t_536073f4）：e7be5cc6（名录修复主体）、8ca52c04 / 9ed628e8 / 37545ac7（回执 v2/v3/v4）；
  - 清档链（t_ee203180）：33762c4e（清档主体）、4aa62574 / 8a0ac56d（回执 v2/v3）；
  - 补正链（t_33240de8）：00bc34a2（R2 zh 扩展位落盘）、489b72c3 / 2de84904（回执 v2/v3）。
- 发布仓回执面：da1e9bc→c646f41a（10 提交全量复核）。
- 方法：第二实现；不 import 任何 tools/* 模块；一切从 git 对象（BASE=40320e37、EE=8a0ac56d、HEAD、PB=origin/main）逐字节重演；全仓扫描覆盖工作仓 27,658 件 / 发布仓 9,342 件（含 gitignored）。
- 实测计数基线（采 elcano 补记口径）：figures 1027 / routes 1358 / sitemap 1359 / unified 1342(318+1024) / modes 3221；verification 4 态 949/1897/35/340。

## 四、逐项核验（对照卡要点 ①–⑨ + ⓪）

### ① 21 码 name 回填 —— 14 层逐码终表 21/21
16 H-*（zh）+ SG-LEE-001 / MY-MAH-001 / RW-KAG-001 + JP-SAS-001 / UZ-ULU-001（重键）= 21 码，对 manifest 目标值逐字核对：
zh 场景名、en 场景名、DB（figures.name）、figures.index、shard、unified、route name/title、sitemap URL，以及发布仓对应 6 面 —— **14 层 × 21 码全部 21/21**。
（zh 侧 19 码改 name：16 回填缺键 + SG 回填 + MY 纠错「Mahathir Mohamad→马哈蒂尔」+ RW 回填；en 侧 18 码改 name：MY en 无变化。）

### ② 残件与清档 —— 全仓 0 残留
- ws 全仓 27,658 件扫描：live=0；命中全在登记豁免类（backup 115、report 10、site_docs 6、release-frozen 4、qa 1、audit 1、validation-report 1、verifier 2）。web/public + web/dist 零命中。
- pb 全仓 9,342 件扫描：live=0（同豁免类；verifier=0）。pb web/public + web/dist 零命中。
- `api/protreptic.db`（两仓）字节级零旧键残留。
- 27 码终态：ws 的 tools/json 草稿、根双胞、figures 分片与 pb 对应面**均不存在**；归档 `docs/research/_archive/RW-KAG_1-27_archive.json` 27 码 × per_code_fragments 齐全。

### ③ 重键 JP-SAS-001 / UZ-ULU-001 —— 引用完整、旧键 0 残留、路由/sitemap 一致
- 新键在所有 live 面引用完整（zh/en/sitemap/routes/unified/pb_zh/pb_sitemap 逐面 ≥1）。
- 旧键（SG-Lee-001 / MY-Mah-001 / JP-Sas-001 / UZ-Ulu-001 + RW-KAG-1..27）全仓 0 残留（见②）。
- routes/sitemap 集合精确：移除 31 旧路径、新增 `figures/JP-SAS-001`、`figures/UZ-ULU-001`（sitemap 同步）。
- 条目迁移保真：JP/UZ 条目内容除 `code`+`name` 外逐字节一致（允许增量仅此两项，与新键自洽）。

### ④ 备份复核（sha256 + 逐字节 + 抽样 ≥30%）
- fix 备份 11/11：`sha256sum -c` 全 OK；每件与 BASE(40320e37) git 对象**逐字节一致（tracked 11/11 identical）**。
- fix2 备份 4/4：MANIFEST 全 OK；`scenarios_zh` 备份 == EE(8a0ac56d) git 对象字节全等（2,981,559 B；sha256 9727c8ea…）；`fields_before` 4 字段 before-sha 复算吻合、after 值均在落盘件内；EE→HEAD 全文件仅 **4 处 × 2 字节**差异（偏移 645896 / 646238 / 647667 / 651342），目标名在同样 4 处就位；全文件 毛先念=0、李先念=34。
- rwkag 备份 89/89：MANIFEST 全 OK；可溯源的 60 件与 preimage(8ca52c04) git 对象一致；**分层抽样 9/27（33%）**：draft / 根双胞 / 分片三类片段逐字节重算全对；场景条目「live 无 / 备份有」、code_maps_en 键「live 无 / 备份有」抽 9 全对；双胞与草稿 byte_same 断言成立。
- 偏移口径勘误复核：fields_before 记录的 `occurrence_byte_offsets`=[286319, 286587, 287618, 290371] 经 QA 独立重算确认为**码点偏移**（换算至真字节 [645895, 646237, 647666, 651341] 吻合），与船长勘误登记一致，非返工项。

### ⑤ 计数自洽
DB / figures.index / meta / static_data_manifest / 统一索引 / 路由 / sitemap / 锚点：
1027 / 1027 / 3221 / 318 / 1342=318+1024 / 1358 / 1359；
EXPECT_FIGURES=1027（export+preflight）、MIN_SITEMAP_ENTRIES=1359（ci_data_check）、siteCounts 4 态 949/1897/35/340 与 meta 一致；scenarios zh/en 键各 1040。

### ⑥ 其他码零变化（越界=硬伤）
- W4 窗口 135 个变更路径全部分类核对：**无越界文件，零 tracked 删除**。
- zh：仅 19 码 name + JP/UZ 重键；无其他字段/条目改动。
- en：18 码 name + H-LXN-001 5 字段（name/name_en/description_en/reason_en/case_en）+ JP/UZ 重键。
- EE→HEAD：仅 H-LXN-001 一条深变化（4 个 zh 扩展位），其余 1039 条目零变动；en 未动。
- 未触碰（断言 forbidden=[]）：`data/modes_data.json`、`data/figure_names.json`、`CHANGELOG.md`、`data/individuals/`、`docs/figures/`、其他期报告（phase20/21r8/21w5/21w6 等）。

### ⑦ 门禁复跑 + parity 重现 + 远端回执复核
- credibility_gate --hard-fail rc=0；verify_source_links --hard-fail rc=0（200.8s，含网络检查，存量冻结口径）；verify_findings --hard-fail rc=0；ci_data_check 24/24 PASS；pages_preflight --stage data / dist rc=0。
- 上游见证器复跑：`verify_w4fix2_lxn.py` 全量 26/26 PASS；`verify_rwkag_clear.py` 全量 20/21（唯一 FAIL=scan.ws.live_zero 命中本 QA 见证器自身，见注记 A）。
- 官方 parity（tools/check_repo_parity.py）实测：共同 2395 件 = 逐字节 2395；单侧 7 = 6 件 R-a 存量文档 + 1 件本 QA 证据（rc=1 为 R-a 已知口径；QA 产物类见注记 E）。
- 远端复核（git fetch 实测）：origin/main=c646f41a（与回执一致）；10 个发布仓回执提交全部为 origin/main 祖先；scenarios_zh / fix2 报告 / 见证器远端 blob 与本地工作树逐字节一致（remote scenarios_zh=8b218e71…）。

### ⑧ H-MZ-001 键面与 R3 裁决一致性
- R1 回填：name=晏阳初 / Y. C. James Yen（场景 zh/en、figure_names、figures 分片 names/style_name；分片 vs BASE 字节不变）。
- R3 保留：`figure_name`=孟子 在 zh/en 场景保留；孟子伴随包 8 件（individuals/figures/tools/文档，含 phase20_moci_research.md）窗口内零改动（tracked 8/8 vs BASE 一致）。
- 场景条目 delta 精确 = name only（zh+en）。

### ⑨ G 类终态（错名、文件名）
- 错名：zh 全文件 毛先念=0、李先念=34；en 文件 0；仅余 zh 场景 H-LXN-001 的 4 个 en 字段残留 Mao Xiannian——即 B-a（已裁定，转 t_def07a84，本卡不处理仅登记）。
- 保留面：根 `H-LXN-001.json`（4+4 处旧名，vs BASE 不变）、`docs/figures/H-LXN-001.md`（2 处纠错注记）、`CHANGELOG.md`（1 处历史记录）均为有意保留（R-b/R-c/R-e）。
- 文件名：ws+pb `data/` 全树无异常名（含换行/`<`）；`xue_mu_qiao_H-XMQ-151_modes.json`、`gong_yu_H-GY-152_modes.json` 正常名件两仓均在；R-d 两异常目录差异见注记 C。

### ⓪ R2 zh 扩展位补正链（fix2 范围，卡要点⓪四项）
1. 落盘核验：`scenarios_zh.json $.H-LXN-001` 的 name_zh / description_zh / reason_zh / case_zh = 李先念（逐字节）；其余 1039 条目零变更；4×2B 最小 diff、同长 2,981,559 B；sha256 9727c8ea→8b218e71。
2. 复跑计数零变化：1027/1358/1359/1342/3221（实测基线）+ 门禁/parity（见⑦）零新差异。
3. 报告一致性：fix_report §2.2 补正注记在 HEAD 存在、EE 不存在（fix2 新增）；fix2 报告口径「after=before 为落盘前实录」+ sha 转换与实测一致。
4. 口径勘误链：执行卡原报告「同批改」措辞与证据实录（before=after）不符 → 已补正落盘；QA 确认父证据 `r2_scenarios_zh_extras` 未抹去原始差异记录（before==after 保留，含原「毛先念」先像）。

**本 QA 未发现需返工项。**

## 五、注记与偏差登记（如实列明）

- **注记 A（上游见证器 QA 自体命中）**：`verify_rwkag_clear.py` 的 `scan.ws.live_zero` 仅命中本 QA 见证器自身（fixture 必然包含旧键样本）；其豁免表 `allowed_hit` 覆盖 docs/qa/** 与两枚链见证器（按名），未含本文件。**非链缺陷**——上游 21/21 为 QA 前状态，QA 后预期 20/21。建议（非返工）：后续把 QA 见证器列入豁免或置于 docs/qa/。
- **注记 B（body_text_chars 逐键精度差，未登记）**：`minds/H-WC-001` 4210→4209。QA 独立根因：W5-B(18405015) 将王充 10 条改为 9 已核验+1 存疑，重建徽章文本 10×3字 → 9×3+2字，净 -1 字符（实测复现：live=4209 / 预 W5 态=4210）。W4 回执已按「收敛族」登记，该逐键差未单列；建议 t_616e4991 或后续补一句（非返工）。
- **注记 C（R-d 两异常目录账务差异）**：链报告注册「未删、待交接」；实测两目录已不在（data/asia/individuals mtime 2026-09-24 06:36:53），数据面无影响（空目录；正常名件完好）。QA 登记差异，建议后续账务补一笔（非返工）。
- **注记 D（B-a）**：en 侧 4× Mao Xiannian（tools/json/scenarios_zh.json）——船长裁定=修复，已派 t_def07a84（门控=本 QA done 后放行，位于 t_616e4991 之前）。本卡仅登记「已裁定、由 t_def07a84 承接」。
- **注记 E（QA 产物类差异，预期）**：本 QA 的脚本/报告/证据/日志为工作仓单侧。提交前 parity 单侧=7（+docs/qa 证据）；提交后实测=8（6 件 R-a 存量 + docs/qa 证据/报告 2 件；rc=1 为 R-a 已知口径）。属 QA 产物类，非链缺陷；镜像/入库由后续卡按惯例处理（工作仓不设 push 义务）。
- **环境注记**：verify_source_links 输出含若干 `::warning`（网络不可达/存量冻结），rc=0；verify_findings 含 2 处 warning（模式重复 harvest），非硬失败。

## 六、复跑方法

```bash
cd /opt/data/workspace/Protreptic
python3 verify_phase21w4_qa_espinosa.py            # 全量 140 断言（约 290s，含网络检查；板面并发期含漂移登记）
python3 verify_phase21w4_qa_espinosa.py --quick    # 离线 132 断言（约 25s）
# 证据可导出：--evidence <path>（默认 docs/qa/phase21w4_qa_evidence.json）
```

## 七、判据索引（关键 git 面）

- BASE=40320e37（W4 窗口起点）｜EE=8a0ac56d（清档终态）｜HEAD=2de84904（fix2 终版）
- PB=release/Protreptic-publish，origin/main=c646f41a5c4fc65027d403cf448c847fc4756060
- 备份：`data/backup_phase21w4_fix_20260924`（11）｜`data/backup_phase21w4_fix2_20260924`（5）｜`data/backup_phase21w4_rwkag_clear_20260924`（93，MANIFEST 89）
- 归档：`docs/research/_archive/RW-KAG_1-27_archive.json`｜报告：phase21w4_fix_report / rwkag_clear_report / fix2_report

## 八、提交回执（v2 补记）

- QA 产物入库（工作仓 master，**本地**，工作仓不设 push 义务）：**h1=17bfa994**（报告+证据+见证器 3 件；`.log` 命中 .gitignore 未入库，磁盘留存）；**h2=5891cecc**（提交后回执：证据更新 + §八/注记E 实测口径）；**h3=本次补记**（见证器 v2：E 段 QA 提交容差；与本节同提交，见 git log 末条）。
- 提交后终跑（v2）：全量 **137 断言 / 0 FAIL（286s）**；E 段含 QA 提交显式容差（commits = 10 + 1 QA-only；EE..HEAD = 10 + 3 QA 件）；parity 复跑 nums=['2395','2395','8','8','0']（6 R-a + docs/qa 2 件）；ws-only core n=33（=30+3 QA 件）；上游见证器同口径 20/21（QA 自体命中，见注记 A）。
- 证据/日志已同步更新到提交后状态（`docs/qa/phase21w4_qa_evidence.json` / `docs/qa/phase21w4_qa_run_final.log`）。
- QA 产物容差为**显式断言**（QA_ARTIFACTS / allowed_extra / QA_W_ALLOWED），非静默豁免；若出现 QA 产物之外的差异仍会 FAIL。


## 九、v3 复跑补记（板面并发·漂移归因，2026-09-24）

- 背景：v2 终跑（08:04）后，共享工作仓持续被多张并行卡写入（R9 安子介/沈复合并链、W8 批1、R9 各回执等）。08:40 复跑出现的 6 项「窗口类」FAIL 经逐项定位 = 提交夹带（外来提交触碰 W4 标记面 = 0，仅窗口枚举口径过严），非 W4 链缺陷；其后并发度进一步上升（合并卡在制改共享数据面 + 构建产物重建窗口），v2 口径下产生「在途漂移」类误报。
- v3 见证器三级漂移归因（均为显式断言，非静默豁免；W4 不变量一律保持严格 pin）：
  1. 提交级：BASE..HEAD 允许「10 W4 提交（保序）+ QA 产物提交 + 外来提交」；外来提交仅当触碰 W4 标记面（phase21w4 备份/归档/报告、两枚链见证器）时判 FAIL。终跑实测：n=32 = 10 W4 + 3 QA + 19 外来，`extra_bad=[]`（外来触碰标记面 = 0）。
  2. 文件级：单侧/多余/内容差文件必须可归因（外来提交触碰、工作区在途脏改、构建产物重建）；归因判定取实时 git 状态（不依赖启动快照），归因不了的仍 FAIL。终跑实测：ws-only 核集 n=57 / new=27 / unattributed=[]；pb-only other_n=31 / unattributed=[]；parity 内容差 2 件全部归因。
  3. 窗口级：W4/fix2 窗口判据 pin 到 fix2 终态提交 2de84904（HEAD_CLAIM）（scenarios_zh 后态 sha pin=8b218e71）；发布仓 pin 取 origin/main 祖先核对并记录实测 bit（终跑 pb_head=e6d133c4）。
- 终跑（2026-09-24 10:23:58，工作仓 HEAD=8c486442，发布仓 e6d133c4）：**140 断言 / 0 FAIL / 44 DRIFT 登记 / 292s**（rc=0）。
  - 漂移构成：A 2 / F 2 / G 40；按类：board-rebuild 42（构建产物随板面重建）+ dirty 2（在途脏改）；明细见证据 JSON `drifts` 字段（逐条含 path 与归因依据）。
  - 瞬态注记：`web/public/data/index.unified.json`（构建产物，未入库）自 09:25 起处于并发重建窗口内缺失。A 段对其读取回退 pb 副本并登记；F 段两枚门禁（ci_data_check / verify_w4fix2_lxn）对该缺失的失败按「板面重建」归因登记（详见 drifts）。该文件缺失不影响 W4 判据——W4 判据全部取 git 对象与 pin 面。
  - 竞态补记：v3 首跑（10:16）曾因「运行中途提交/新文件 vs 启动快照」竞态产生 2 项失败样例（合并卡新脚本、parity common 2395→2498 增长）；已改为实时归因并放宽 common≥2395 自洽断言，终跑复证 0 FAIL。另修 worktree 检查首行路径解析（`strip()`→`rstrip()`，显示层瑕疵）。
- v2 语义保留：注记 A（上游见证器 QA 自体命中）继续有效；注记 E 的单侧口径随板面（终跑 miss=25：6 R-a 存量 + QA 产物 + 外来在制）同步演化，归因判定不变。

## 十、v3 提交回执

- 入库（工作仓 master，本地；工作仓不设 push 义务）：**h4=c1fe9024**（见证器 v3 + 报告 §九/§十 + 证据/日志；3 文件，+836/−166）。
- 提交后终跑（v3 口径，2026-09-24 10:30:26，工作仓 HEAD=c1fe9024）：全量 **140 断言 / 0 FAIL / 45 DRIFT 登记（274s，rc=0）**；窗口 n=33 = 10 W4 + 4 QA（含 h4）+ 19 外来，`extra_bad=[]`；证据/日志已同步提交后状态。**h5=本次补记**（报告 §十 + 证据）。
