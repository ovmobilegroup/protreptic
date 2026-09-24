# Phase21-W9-fix 独立 QA 复验报告（espinosa / 卡 t_28a29244）

**结论：PASS。** 修复卡 t_d7faccc5 的成果经独立全链复验全部复现：504 条真名持久回填（DB / figures.index / 分片 / unified 四面）、重建不回落（源侧从零 + 副本复跑 + 旧装载器因果对照）、ten/104 残留登记、web/public/data 索引面处置（1359→0 仅索引面、盘上保留）、门禁 / parity / 双仓逐字节 / push 收口。E1 / F11 / F12 三项上游缺陷态断言按船注 B 裁定修订（见 §6，修订断言实测全过）；无硬伤；另登记 5 项低危观察（§7）。

- 复核对象：修复链 ws **108e2826 → 47f9852d → 49ac3832 → b7a6bfad**（父 **6f298ca1**；HEAD = b7a6bfad）；发布线 **ac33cba5 → 2586040c → 368493b5 → 4b79cb27**；push a7ba7f29..4b79cb27；**origin/main = 4b79cb27 = pb HEAD**。
- 方法（不信任自述）：git 对象 / 提交树 pin + 盘上现读 + 工具现跑（隔离副本 / 隔离 --out，禁动主库）+ 独立重算；写入边界 = QA 产物 + scratch 隔离副本（唯一工具副作用已快照复原，§7-O3）。
- 产出：本报告 + `docs/qa/phase21w9_fclass_fix_qa_evidence_espinosa.json` + `verify_w9_fclass_fix_qa_espinosa.py`（终跑 **33 PASS / 0 FAIL / 2 INFO**）。

## 0. 修复卡自述 vs 独立实测（一句话表）

| 修复卡自述 | 独立实测 | 判定 |
| --- | --- | --- |
| 504 真名回填四面（DB/index/分片/unified） | 源侧从零重建 ×2 + 主库副本复跑：1017/10；127 件分层抽样四面 0 失配；全库 1027 行 0 臆造 | PASS |
| 重建不回落（RNBW） | 父装载器同源 → 514 空；新装载器 → 10 空；两次从零确定性；同文件幂等；主库副本重建 20 列行级全等 | PASS |
| ten=待核名 10 / code_as_name=104 登记 | 与独立重导（514=504+10；400+104）逐项一致；提交件 == 盘上；无来源名臆造 | PASS |
| web/public/data 索引面 1359→0（仅索引、盘上保留） | ls-files=0；T0 清单 1359 行 sha 与父提交 blob 1359/1359 全等；盘上 1385（+26 站链产物）；0 缺失 | PASS |
| 站链 8 步 / 五闸 / parity / push | parity 4593/4593 逐字节一致、0 单侧；七路门禁 rc=0；隔离重导出 1358/1358 等值；隔离 unified byte-equal；ls-remote == pb HEAD == 4b79cb27 | PASS |
| 独立校验 A-H 34 断言 PASS | 本卡复跑 verify_w9_fclass_fix.py：A-H 34 断言全 PASS | 复现 |

## 1. 卡面六项逐项结果表

| # | 卡面要求 | 方法 | 结果 |
| --- | --- | --- | --- |
| 1 | 重建不回落独立重演（隔离副本，禁动主库） | 从零重建 ×2 + 同文件幂等 + 主库副本复跑 + 旧装载器因果对照 | PASS（§2） |
| 2 | 回填逐条抽样 ≥100（真名 ≥80 + 占位 ≥20） | 100 真名 + 26 占位 + AE-FED-001 焦点 = 127 件 × 四处面 | PASS（§3） |
| 3 | ten 与 104 登记件 | 逐项对独立重导 + 无臆造扫描 + 提交面核对 | PASS（§4） |
| 4 | 提交面（父→HEAD 全量审阅 / web 索引面 / hygiene） | 逐提交集合 + 14 件 allowlist + H-*/W7/web 边界 + 镜像逐件对照 | PASS（§5） |
| 5 | 收口面复跑（parity / 门禁四件 / 复算 / 双仓 / push） | 全部现跑（含隔离重导出、unified 隔离重建） | PASS（§5.5-5.6） |
| 6 | E 组裁定 | 缺陷态断言修订 + 理由 + 反放水保障 | 裁定成立（§6） |

## 2. 重建不回落（详证）

- **(a) 源侧从零重建 ×2**：`python3 tools/build_figures_db.py --out <隔离>/fz_a.db|fz_b.db` → 均 rc=0，1027 行 / 1017 有名 / 空名 10；空名集 == TEN；两次行全等（确定性）。
- **(b) 同文件复跑（幂等）**：稳定全等。
- **(c) 主库副本复跑**：cp 主库 → `--out` 重建 → 20 列行级 == 主库快照 == 从零产物（三者全等；重建不回落实测成立）。
- **(d) 因果对照（持久性来源）**：父提交装载器（6f298ca1 版）在同源上跑 → **513/514**；新装载器 → **1017/10** ⇒ 持久性来源 = 装载器键回退（`name → name_zh / name_en`），**非直改 DB 单点**；源文件（scenarios_zh/en、tags）在父→HEAD 零改动且 worktree == blob。
- **(e) 修复 diff 实证**：`tools/build_figures_db.py` / `api/load_data.py` 仅加双读回退（各 1 处）；`tools/export_static_site.py` 仅 gzip 预算 50→80KB 与规则文本 —— 均与「源侧持久」口径相符。

## 3. 回填抽样（详证）

- 独立重导父快照：空名 514 = 可回填 504（400 真名 + 104 code 占位）+ 10 无来源；10 == ten 名单 —— 与修复卡分解口径完全一致。
- 抽样规则：按 code 排序后确定性均匀散布；**100 真名 + 26 占位 + AE-FED-001 焦点 = 127 件**。
- 四面核对（DB name_zh/name_en、分片 name_zh/name_en、figures.index name_zh、unified name）：**0 失配**。
- **全库防臆造**：1027 行逐一与源侧（scenarios_zh/en 双读口径）比对：zh 失配 0 / en 失配 0 / 空名而有源 0。
- **占位不冒充真名**：104 行四面仍 name==code；ten 四处面（DB/分片/index/unified）无任何真名泄漏。
- 焦点件 **AE-FED-001**：DB / 分片 / figures.index / unified 四面均为真名（与 legacy 全等）。

## 4. 登记件（详证）

- 残留登记件已入提交：`data/audit/phase21w9_fclass_residual_registry.json`（HEAD blob == 盘上；sha256 f1feda75...）。
- **ten**：count 10 / status 待核名 / codes == 独立重导 / 全部名字字段为空；note 声明候选线索（draft 文件等）未采纳。
- **code_as_name**：count 104 / status 占位待补名 / codes == 独立重导 104 / 无重复。
- **before-list 保真**：`data/audit/phase21w9_web_public_data_index_before.txt` 1359 行、sha256 b123f3f0...（与卡面记录一致）；路径集 == 提交移除集；**且与父提交 blob 1359/1359 逐件 sha 全等**（T0 快照保真）。

## 5. 提交面（详证）

### 5.1 修复 diff（父→HEAD）全量审阅
- 全量 = **M7 A7 D1359**（14 件改动 + 1359 移出）；A/M 并集 == 14 件 allowlist（无夹带）；逐提交集合：v1=108e2826（M7/A7/D1359）；v2=47f9852d 4 件（生成器/登记/证据/报告）；v3=49ac3832 2 件（证据/报告）；v4=b7a6bfad 1 件（登记）。
- 越界核验：**H-* 面零动**（DB 372 行 0 差 / 372 分片父 blob == 盘 / index 372 项等）；**W7 删除面未回滚**（fix A/M ∩ e5ddd13f 的 1303 删除 = 0；40 件抽样在盘/树均缺）。

### 5.2 web/public/data 索引面处置
- T0 = 1359 件（== before-list）；处置后 ls-files=**0**；盘上 **1385**（+26 = daily 2 + search 17 + graph 7）；0 缺失；852 件字节未动、507 件为回填再生（504 分片 + figures.index + index.unified + meta.json）。.gitignore 生效（check-ignore rc=0）。
- 方法注：上游以 `git update-index --force-remove --stdin` 实施（仅索引面等价变体，已在修复报告 §六登记）；实测效果与卡面要求一致。

### 5.3 提交 hygiene
- 工作区干净（仅历史备份 untracked）；各提交均为显式路径白名单；无他卡在途文件夹带。

### 5.4 镜像逐件对照（ws → pb）
- 108e2826→ac33cba5 **13/13**；47f9852d→2586040c **4/4**；49ac3832→368493b5 **2/2**；b7a6bfad→4b79cb27 **1/1** —— 全部逐字节全等。

### 5.5 收口面现跑
- **parity rc=0**：边界两仓各 4593、identical 4593、单侧 0/0（static_data_manifest.json 归零）。
- **门禁七跑 rc=0**：credibility_gate --legacy-report / --hard-fail；verify_source_links --legacy-report / --hard-fail；verify_findings --hard-fail；apply_verification_status --check；ci_data_check。
- **复算**：figures.index sha 3c99c19a...、figures 聚合 95c2b41e...（1027 件）、unified counts {1344,320,1024} 且隔离重建 **byte-equal**；manifest 自洽（db sha / figures agg / index sha）+ gzip **65571B ≤ 80KB**；routes name==code **114**（=104+10；父 514 → 头 114）。
- **站链补充**：pages_preflight --stage data rc=0；gen_web_site_counts --check rc=0；build_daily_index --check rc=0；隔离重导出 **1358/1358 等值**（0 差 0 单侧）；search 16 分片 byte-equal（meta 仅时间戳）。

### 5.6 push 面
- ls-remote（ws / pb 两仓现查）main = **4b79cb27** = pb HEAD；ws 侧 remote-tracking 缓存陈旧（4bda4bdc，非实测依据，§7-O4）。

## 6. E 组裁定（E1 / F11 / F12）

裁定：三项均为**缺陷态断言**，与「504 持久回填 + ten/104 登记」正确终态冲突；以终态为准修订断言。理由与实测：

| 旧断言 | 修复态下旧断言失败原因（实测） | 裁定 | 修订断言 | 修订实测 |
| --- | --- | --- | --- | --- |
| E1：非 H 空名 == 0（worktree AND rebuild） | worktree=10 / rebuild=10（ten 无来源，==0 须臆造填名——被禁止） | 修订 | E1'：两侧空名集**== TEN 精确集合** | PASS |
| F11：figures 聚合==6391856f 且 index==65a7cdc6 | 聚合 95c2b41e / index 3c99c19a（合法回填必然改变两面哈希） | 修订 | F11'：H-* 面零动（DB/372 分片/index）+ parity 边界两仓一致 | PASS |
| F12：pb 从未引用/不持有 e5ddd13f | 对象经 pb 本地 master 快照分支存在；修复链回执消息合法提及该号 | 修订 | F12'：e5ddd13f **非发布线祖先**（origin/main，is_ancestor rc=1） | PASS |

**反放水保障**：① 零臆造（全库 1027 行逐行 0 失配，S3/S4 全绿）；② 修订断言先于实测定义、可证伪、与结论无关；③ 旧断言原样保留于上游校验器，仅以本表理由替代；④ 未改动任何上游 QA 产物；⑤ 无人为填名、无凑绿项。

上游校验器复跑（修复态）：**12 PASS / 3 FAIL / 2 INFO**（F1-F10 全 PASS；FAIL = F11/F12/E1，恰为本表三项）。
本卡校验器（含裁定修订）：**33 PASS / 0 FAIL / 2 INFO**。
校验器差异（相对上游，详见脚本文档头）：F11→F11'、F12→F12'、E1→E1' 三项替代 + 新增 W/R/S/G/B/C 六组（窗口事实 / 重演 / 抽样 / 登记 / 边界 / 收口）；上游 F1-F10 事实断言不重复。

## 7. 低危观察与登记

- **O1**：graph 产物**逐文件内嵌 generated_at** → 字节级不可复现（语义等价已证：模除时间戳全等）；工具不在修复面，非本卡缺陷。
- **O2**：search/meta.json 仅时间戳差异（16/16 分片 byte-equal）。
- **O3**：`tools/export_static_site.py` 恒写 `docs/architecture/static_data_manifest.json`（`--out` 不豁免）→ 本卡校验器已快照 / 复原（C5b PASS；仓库现状与提交一致）。后续 QA 跑隔离导出时注意此副作用。
- **O4**：ws origin/main remote-tracking 缓存陈旧（4bda4bdc）；实测以 ls-remote 为准（== 4b79cb27）。
- **O5**：pb 对象库经**非发布线**本地 master 快照分支含 e5ddd13f（F12x）；记录，不判缺陷。

## 8. 复现

    cd /opt/data/workspace/Protreptic
    python3 verify_w9_fclass_fix_qa_espinosa.py --with-reexport --with-remote   # 33 PASS / 0 FAIL / 2 INFO
    python3 verify_w9_fclass_qa_espinosa.py                                     # 上游：12 PASS / 3 FAIL / 2 INFO（三项已裁定）
    python3 verify_w9_fclass_fix.py                                             # 修复卡 A-H 34 断言全 PASS
    python3 tools/check_repo_parity.py --json                                   # rc=0 / 4593 逐字节一致
    python3 tools/build_figures_db.py --out /tmp/fz.db                          # 重建不回落（副本）

- 中间证据（隔离副本与现跑产物）：`/opt/data/profiles/espinosa/cache/scratch/w9fixqa/`（s4_replay / s5_sampling / s9_closure / s10_chain / s11_graph_iso / final_verifier_run.json / upstream_verifier_at_fix.json）。

## 9. 提交回执（本 QA 卡 t_28a29244）

- （A 阶段提交后回填于 B 阶段：ws 提交号 / pb 镜像号 / push 区间 / ls-remote 实测 / 各件 sha 终值。）
