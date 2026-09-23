# Phase21-R6 A组复刻-QA 独立验收报告

- 卡：t_cd63c892（espinosa）| 验收人：Gonzalo Gomez de Espinosa（独立 QA，第二实现）
- 验收对象：Phase21-R6 A 组 10 件（CHB 陈伯达 / CY 陈云 / DYC 邓颖超 / FXT 费孝通 / JX 纪弦 / KKQ 康克清 / LWH 李维汉 / SQL 宋庆龄 / WL 万里 / YSK 杨尚昆）的复刻落盘（批1/批2）与合并入主库结果
- 唯一依据：`docs/research/legacy20_rev6_assessment.md`（第2节 子串修正 / 第4.1节 A 组 / 第5节 样例 / 第7节 风险）
- 状态锚点（评审冻结）：**PRE**=`60a14a38`（合并前基线）| **MY**=`d0f1bb65`（A 组合并入主库提交 = 合并态）| **CUR**=工作区现状（验收时刻 HEAD=`5a4f4483`，B 组收口已提交并镜像）
- 方法：**第二实现** - 独立脚本 `verify_legacy20_r6_qa_espinosa.py`（本仓根目录），不引用合并卡核验输出；他卡报告/清单仅作线索，全部结论由本脚本自证。数据面主源一律取 MY 冻结态（`git show d0f1bb65:<path>`），避免与他卡并发写入竞态；门禁、站点、parity 另按现网口径复核并逐件归因。
- **结论（验收时点）：74 项断言 0 FAIL（exit 0）**；四门禁复跑 exit 0；站点链条 preflight 通过；两仓 parity 现网内容差 0；4 类「后置漂移」按归因登记（见第6节），均非合并卡缺陷。

## 1. 结果总览（按组）

| 组 | 判据（自建） | 结果 |
|---|---|---|
| A 编号唯一性 | 全库 3262 条；id/mode_code 各 0 重复；+100 齐全；新码不越界；A100 的 80 个 legacy 旧号在合并态编码空间 0 残留 | 9 PASS / 0 FAIL |
| B 逐条溯源 | 落盘清单 100 条（批1 50 + 批2 50）；合并条目等于落盘条目；备份链 sha 三方一致；内容字段逐条可溯源旧档（0 捏造）；旧号仅存留证字段 | 15 PASS / 0 FAIL |
| C 四面同体 | 图档内嵌等于伴随包等于主库（10x10）；镜像等于图档去 modes；mode_ids 001..010；存量内嵌块 code 一致 | 4 PASS / 0 FAIL |
| D 类目归一 | category/mapped 与 tsv 逐条一致；归一目标属于标准集与样例表与库内词表（0 新造）；category_raw 可溯源 | 4 PASS / 0 FAIL |
| E pending 诚实 | 100/100 pending；evidence 明写未独立核验；0 条自称 verified；缺项字段确空；WL 引文归属登记；DYC 内联重指 | 6 PASS / 0 FAIL |
| F 互引可达 | 新增 100 条 204 引用 0 悬空；全库悬空零新增（452/452）；十件 code_maps 悬空零新增（2/2）；现状 delta 归因 | 4 PASS / 0 FAIL |
| G 场景与标签 | 新增 30+30 等于落盘件（键与码归一 20 处）；重指 60 处仅 mode_id；标签净增 +200 可推导；FXT 平铺 10 改号；dict 级 40 处仅 mode_id；键集不变；0 旧号残留 | 9 PASS / 0 FAIL |
| K 现状存活 | 合并 100 条存活且逐字段未改；CUR 与 MY 的增删与改动归因登记 | 2 PASS / 0 FAIL |
| H 门禁复跑 | 四门禁（MY 态数据副本 + 现网工具）exit 0 | 4 PASS / 0 FAIL |
| I 站点计数与锚点 | 合并态锚点 git 冻结核验；现网三处同口径；分片实文件；preflight exit 0；漂移登记 | 9 PASS / 0 FAIL |
| J 两仓 parity / 发布仓 | parity 差异逐件归因（未解释 0）；合并面 12 件可归属；交付件齐；数据面五件可归属；载荷 50 件跨仓一致；发布仓干净；远端等于 HEAD | 7 PASS / 0 FAIL |

## 2. 关键证据（摘要）

- **A**：`modes` 3262 条; `dup_id` 与 `dup_mc` 均为空; `M-<COD>-001..010` 100 条齐全且 `id` 等于 `mode_code`; 新码 0 越界(他档 0 处, code_maps 0 处). A100 的 80 个 legacy 旧号在合并态编码空间 **0 残留**, 其中 20 个旧号为跨人物共号(FXT 与 LWH 共 `M341-M350`, DYC 与 KKQ 共 `M321-M330`), 已随重编全部消解.
- **B**：合并条目与批1与批2 落盘清单逐字段全等; item 文件 10x10 等于清单, `id_mapping.tsv` 与条目一致; **备份字节等于登记 sha256 等于 git 落盘前原档**(批1 以 `45c5f43a` 计, 批2 以 `d879eb9c` 计; YSK 1 件旧档申报「落盘前不存在」经 git 核验成立); 内容字段逐条溯源旧档 0 捏造(DYC 定义内联旧号 2 处经「新号回旧号」归一回溯命中); 旧号仅存留证字段(`legacy_mode_id`, `mode_ids_note`, `attribution_note`), 其余字段 0 残留. 另手核: DYC 根目录游离副本 `data/H-DYC-001_modes.json` 已不在根, 归入 `data/backup_r6_H-DYC-001_20260923/`.
- **C**：三面逐条全等(图档内嵌等于伴随包等于主库, 10 件 x 10 条); 镜像等于图档去 modes; 图档与镜像 `mode_ids` 均为 001..010 顺序; 主库内嵌 figure 块(存量 2 件 SQL 与 CHB)code 一致.
- **D**：标准集解析自 `export_static_site.CATEGORY_EN`(18 项); 100 条 `category` 与 `category_mapping.tsv` 逐条一致; 归一目标 0 新造(合法域 = 标准集与样例表与库内既有词表); `category_raw` 可溯源旧档; kept-as-is 38 条(含 CHB「文化批判思维, 哲学思维」等表外项按原值保留).
- **E**：100/100 `verification.status=pending`, evidence 明写「未独立核验」, 0 条自称 verified; `legacy_missing_fields` 所列字段确为空; `M-WL-001` 引文保真且有 `attribution_note_zh` 登记; `M-DYC-010` 定义内联旧号已重指.
- **F**：新增 100 条 `related_modes` 共 204 引用 0 悬空; 全库 `related_modes` 悬空 452(基线)与 452(合并态), **0 新增**; 十件 code_maps 悬空 2(基线, H-SQL-001 指向 H-MZD-001 与 H-ZET-001 历史存量)与 2(合并态), **0 新增**.
- **G**：`scenarios_zh` 与 `scenarios_en` 各 +30(2183 变 2213)与落盘件逐条一致(键与码归一: CY en 无 E 后缀 10 处, JX en `C-JXE-###` 中缀 10 处); 既有场景重指 60 处仅 `mode_id` 旧转新; 十件条目 0 旧号残留; `scenario_tags` 平铺 +200(7278 变 7478)且 200 条可由条目名(zh 与 en 配对)推导; FXT 平铺 10 处改号, dict 级 40 处(SQL 20 加 FXT 20)仅 `mode_id` 重指; 标签顶层键集 0 增 0 删.

## 3. 门禁复跑(MY 冻结态数据副本 + 现网工具, exit 0)

数据副本: `modes_data.json` sha256 `4ca4eda2a9c47b2d`(等于 MY 态); 工具版本 sha256 登记于证据 `shell.gate_inputs.tools_sha`.

- `credibility_gate.py --hard-fail`: **exit 0**, 新增(基线外) 0 条; 存量 524 条已冻结; 3 条「基线里已不再成立」可重冻结(提示, 不阻断).
- `verify_findings.py --hard-fail`: **exit 0**, hard failures 0; 存量 0 条(A0 B0 C0 D0); 新增 0 条; 1 条非阻断警告(重复收割类).
- `verify_source_links.py --hard-fail`: **exit 0**, 88 OK / 0 dead / 81 unreachable(连接层, 按策略计警告); 存量坏链 0, **新增坏链 0**.
- `apply_verification_status.py --check`: **exit 0**, 四态求和自洽(公开 3202 加隔离 60 等于全库 3262); verified evidence 全部回查索引 url(145 个不同 url); **库中状态与规则逐条一致(0 漂移)**.

原始输出: `docs/qa/phase21r6_qa_gates/gate_*.txt`(含命令行).

## 4. 站点计数与锚点

- **合并态(git 冻结证据)**: `tools/export_static_site.py` = 3252/316/1057; `tools/pages_preflight.py.EXPECT_MODES` = 3252; `web/src/generated/siteCounts.ts` = modes 3192 / figures 316.
- **现网自洽**: EXPECT_MODES 三处同值(export 3261 / pages 3261 / meta 3261); EXPECT_BY_FIGURE 与 EXPECT_FIGURES 与 meta.counts 一致(316/1057); `static_data_manifest` 计数等于 meta.json 计数; 分片实文件 figures/index/by-figure = 1057/8/316; `pages_preflight --stage data` 全部断言通过(exit 0).
- **漂移登记**: 合并态 3252/3192 变为现网 3261/3201, 差额恰为 B 组在制与收口的净 +9 条(raw 3262 变 3271), 归因他卡, 非合并卡缺陷.

## 5. 两仓 parity 与发布仓状态(现网口径)

- `tools/check_repo_parity.py --json`: status=DIFF; 边界内两侧共 1783 件, **identical=1783, 内容差 0**; `only_workspace=7` 即本卡 QA 交付物自身(报告, 证据, 门禁原始输出, 脚本), `only_publish=0`; 差异**未解释 0**.
- 合并面 12 件在发布仓的字节**逐件可归属**到已知态(合并态, 收尾态, 现网 HEAD `5a4f4483`); 合并交付件(报告, 证据, manifest)发布仓等于工作区; 数据面五件可归属(modes/tags 为收口态, code_maps/scenarios 含 R6C 撤下后态); **十件载荷 50 件跨仓 sha 全等**.
- 发布仓工作树干净; `origin/main` 等于发布仓 HEAD(`70c97abe`).
- 说明: 验收过程早期(B 组收口尚未提交与镜像时)曾观察到「他卡在制」类差异(+11 与 -2 条, 锚点 3252 变 3261, parity 内容差 13 件); B 组收口提交并镜像后已收敛为上述 0 内容差. 两类时点均已留痕于证据 JSON.

## 6. 现状漂移与归因(登记, 非合并卡缺陷)

1. **R6C 撤下(`7b767f39`)**: `code_maps` 215 变 212, `scenarios_zh/en` 各 2213 变 2183, `figure_names` 撤下 9 键; 由此现状新增 1 处 xref 悬空 `H-CY-001` 指向 `H-LC-001`(R6C 已在卡内观察行留痕). 合并态本身为 0 新增悬空.
2. **B 组(t_f3aabe2c)在制与收口**: `M-WZ-001..011` 等 +11, `M391/M392` 拆并为新码 -2, `M-EUC-006` 1 条改动; 净 +9 条(cur_total 3271). 合并的 100 条未被其触碰(K 组逐字段核验).
3. **站点锚点随动**: 3252/3192 变 3261/3201(见第 4 节).
4. **parity 时点差**: 见第 5 节说明.

## 7. 未做与非主张

- 未做引文逐条落源的外网核验(属复刻与验证流水线; 本卡对 pending 口径与留证字段做抽查核验).
- 未裁决, 未触碰他卡在制改动; 本卡对主库数据**只读**, 仅落盘本卡交付物(报告, 脚本, 证据).
- 全部结论由独立脚本自证; **未引用合并卡(t_10089b19)核验结论**, 其报告与 manifest 仅作线索核对目标.

## 8. 复现

```bash
cd /opt/data/workspace/Protreptic
python3 verify_legacy20_r6_qa_espinosa.py --skip-shell   # 数据面约 4 分钟
python3 verify_legacy20_r6_qa_espinosa.py                # 全链(含门禁, 站点, parity)约 15 分钟
```

- 证据: `docs/qa/phase21r6_qa_evidence.json`(74 项结果加 shell 明细)
- 门禁原始输出: `docs/qa/phase21r6_qa_gates/`(gate_*.txt / pages_preflight_data.txt / parity_json.txt)
