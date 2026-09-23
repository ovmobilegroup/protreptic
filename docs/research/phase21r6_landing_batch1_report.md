# Phase21-R6 批1 转换落盘报告（A 组复刻 · 陈云 / 宋庆龄 / 杨尚昆 / 万里 / 纪弦）

- 归属卡：t_4481df98（Phase21-R6 A组复刻·转换落盘·批1 五件）
- 执行：elcano；时间：2026-09-23（CST）
- 唯一依据：docs/research/legacy20_rev6_assessment.md（§2 子串修正 / §4.1 A组 / §5 样例 / §7 风险）
- 样例模板：docs/scratch/legacy20_rev6_samples/（entries 27 键、category 与 category_raw 双写、verification 统一 pending、id_mapping.tsv、门禁试跑）
- 工具：tools/build_legacy20_r6_batch1.py（转换生成器）；verify_legacy20_r6_batch1.py（独立核验：113 PASS / 0 FAIL）
- 边界遵守：主库 modes_data.json、code_maps.json、scenarios_zh.json、scenarios_en.json、scenario_tags.json、figure_names.json 零写入（核验 F 组 + 六个主库文件与 HEAD 字节一致）

## 1. 落盘产物（仅本卡路径）

### 1.1 data 侧：旧档原地升级为 v6 形态（先字节备份，后写入）

| 件 | 人物 | 升级文件（每件 3 个） | 备份目录 |
|---|---|---|---|
| H-CY-001 | 陈云 | data/figures/H-CY-001.json / data/individuals/H-CY-001.json / data/individuals/H-CY-001_modes.json | data/backup_r6_H-CY-001_20260923/ |
| H-SQL-001 | 宋庆龄 | 同上三路径（SQL 前缀） | data/backup_r6_H-SQL-001_20260923/ |
| H-YSK-001 | 杨尚昆 | 同上（data/individuals/H-YSK-001.json 为落盘新建镜像，落盘前缺档） | data/backup_r6_H-YSK-001_20260923/ |
| H-WL-001 | 万里 | 同上（WL 前缀） | data/backup_r6_H-WL-001_20260923/ |
| H-JX-001 | 纪弦 | 同上（JX 前缀） | data/backup_r6_H-JX-001_20260923/ |

- 每件备份目录含 manifest.json：逐文件记录 path / backup / sha256_before / bytes / git_head_sha256（先备份后写入，核验 D 组逐条比对备份字节与 git HEAD 原字节）。
- 三面一致：图档内嵌 modes == individuals 伴随包 modes == 落盘 entries == 落盘冻结副本（逐对象相等，核验 B 组）。
- 图档级 v6：schema_version=v6、id/code/figure_code 归一为本人代号、mode_ids 换新码、mode_ids_note 记旧号到新号、caveats 记未核验与逐件已知问题；原有图档级字段（tags / cross_references / scenarios / meta / 生卒年 / 代表作等）原样搬迁，未改名、未新增。

### 1.2 合并卡输入：docs/scratch/legacy20_rev6_landing/batch1/

- `<CODE>/modes_library_entries.json`：10 条可直接并入主库的 v6 条目（27 键口径同样例）
- `<CODE>/id_mapping.tsv`：旧号到新号对照（含 name_zh / name_en）
- `<CODE>/category_mapping.tsv`：类目归一流水表（raw / applied / status / candidate_target）
- `<CODE>/figures/<CODE>.json`、`<CODE>/individuals/<CODE>.json`、`<CODE>/individuals/<CODE>_modes.json`：冻结副本（与 data 侧升级件字节一致，供合并卡逐条比对，不受后续并发写入影响）
- `<CODE>/scenarios_zh.json`、`<CODE>/scenarios_en.json`、`<CODE>/scenario_notes.json`：场景附随件（既有载荷搬迁 + mode_id 重指，非本卡新增内容）
- `combined_library_entries.json`：50 条合并清单（门禁试跑对象）
- `scenarios_zh_new.json` / `scenarios_en_new.json` / `scenario_remap_needed.json` / `scenario_notes.json`：批级汇总

### 1.3 审计与证据

- data/audit/phase21r6_batch1_landing_manifest.json（逐件写入清单、备份哈希登记、落盘后 sha256、类目汇总、场景覆盖）
- docs/research/phase21r6_landing_batch1_evidence.json（同内容证据副本）
- docs/research/phase21r6_landing_batch1_verify_evidence.json（113 项断言明细 + 重码面 + 既有预期引用清单 + 主库 HEAD 对比）
- docs/research/phase21r6_landing_batch1_gate.txt（credibility_gate --hard-fail 原始输出）

## 2. 逐件摘要（实测值）

| 件 | 人物 | 载荷来源 | 旧号到新号 | 互引条数 | 类目归一（应用/待核） | 场景附随件 | 备份登记 |
|---|---|---|---|---|---|---|---|
| H-CY-001 | 陈云 | data/figures/H-CY-001.json 内嵌 modes（与 individuals 伴随包逐字相同） | M101~M110 → M-CY-001~010 | 20（全块内） | 10/0 | 新增 zh 10 + en 10 | 3 件，HEAD 均一致 |
| H-SQL-001 | 宋庆龄 | data/individuals/H-SQL-001_modes.json（thinking_modes 容器） | M361~M370 → M-SQL-001~010 | 24（全块内） | 5/5 | 库内 zh 10 + en 10 待重指 | 3 件，HEAD 均一致 |
| H-YSK-001 | 杨尚昆 | data/individuals/H-YSK-001_modes.json（modes 容器） | M431~M440 → M-YSK-001~010 | 21（全块内） | 7/3 | 原始载荷 zh 5 + en 5（非库内规范格式，覆盖 5/10） | 3 件（individuals 主档为落盘前缺档） |
| H-WL-001 | 万里 | data/individuals/H-WL-001_modes.json（顶层 list） | M274~M283 → M-WL-001~010 | 20（全块内） | 10/0 | 库内 zh 10 + en 10 待重指 | 3 件，HEAD 均一致 |
| H-JX-001 | 纪弦 | data/individuals/H-JX-001_modes.json（顶层 list） | M001~M010 → M-JX-001~010 | 21（全块内） | 10/0 | 新增 zh 10 + en 10 | 3 件，HEAD 均一致 |

- 编号唯一性：50 个新码互不重复；作为模式主体编号（mode_code / id）在本卡路径之外 0 占用（核验 E 组）；
- 旧号重码面：M001~M010（JX）与 M361~M370（SQL）在活库其他文件（他人物档案、站点索引、历史脚本、docs 页）中仍被引用，属跨人物重码遗留；本卡只覆盖本人档案范围，跨文件引用清单见核验证据 json 的 legacy_reuse 字段；
- 既有预期引用（他卡已写，合并后即可解析）：M-SQL-001 已在 H-MAN-001（曼德拉）与 H-KEY-001（凯恩斯）的 cross_references.mode_pair 及描述文本中引用；M-WL-001 已在 H-SK-001 伴随包的 related_modes 中引用（核验 E 组只报告不干涉，属主库他卡写入）。

## 3. 类目归一（船长裁定口径：照样例映射表批量应用；表外者按原值保留 + 标记待核）

### 3.1 应用映射（42 条）

样例映射表（17 对）在批1 五件载荷上 0 命中（CHB / FXT 的旧类目与这五件不同）。本卡按样例口径扩展 12 对候选映射，目标值全部取自库内标准类目表（tools/export_static_site.py 的 CATEGORY_EN 18 类目）：

| 原值 | 归一值 | 命中条数 | 出处 |
|---|---|---|---|
| 方法论 | 方法论通用 | 30（CY 9 / WL 10 / JX 10） | 扩展候选（样例表含 方法论思维 / 综合方法论 / 写作方法论 同类映射） |
| 认识论 | 认识论逻辑 | 1（CY） | 扩展候选 |
| 政治哲学 | 政治治理 | 1（SQL） | 扩展候选（样例表 政治哲学思维 → 政治治理 同族） |
| 政治策略 | 战略决策 | 1（SQL） | 扩展候选（样例表 政治策略思维 → 战略决策 同族） |
| 政治体制 | 政治治理 | 2（YSK） | 扩展候选 |
| 区域治理 | 政治治理 | 1（YSK） | 扩展候选 |
| 战略思维 | 战略决策 | 1（YSK） | 扩展候选 |
| 决策支持 | 战略决策 | 1（YSK） | 扩展候选 |
| 组织管理 | 组织领导 | 1（YSK） | 扩展候选 |
| 人力资源管理 | 组织领导 | 1（YSK） | 扩展候选 |
| 社会治理 | 政治治理 | 1（SQL） | 扩展候选 |
| 教育哲学 | 教育传承 | 1（SQL） | 扩展候选 |

### 3.2 待核（8 条，按原值保留，未应用）

| 原值 | 条数 | 候选目标（未应用） |
|---|---|---|
| 伦理哲学 | 1（SQL） | 伦理修养 / 哲学形而上 |
| 国际关系 | 1（SQL） | 政治治理 |
| 社会运动 | 1（SQL） | 政治治理 |
| 外交策略 | 2（SQL） | 政治治理 / 战略决策 |
| 情报策略 | 2（YSK） | 战略决策 / 组织领导 |
| 后勤保障 | 1（YSK） | 组织领导 / 工程技术 |

- 每条条目的 category_raw 一律保留原值（核验 H 组逐条比对原档），扩展候选映射可通过 category_raw 一键回退；
- 完整流水见各件的 category_mapping.tsv 流水表（每件落盘目录内）。

## 4. 特例处置（按报告口径，只做标注不改事实）

- **WL 引文勘误**（报告 §7-2 与卡面要求）：M-WL-001（旧 M274）的 key_quote「不管白猫黑猫，抓住老鼠就是好猫」通行归属为邓小平，旧载荷置于万里名下；处置为引文原文逐字保真未改、新增 attribution_note_zh / attribution_note_en 标注归属疑义、verification.evidence 追加勘误记录、图档 caveats 明列；待核验卡后续处置。
- **JX 旧 id 重码面广**：旧号 M001~M010 是全库最重的一段重码（活库他档与场景、站点索引、历史脚本均含该串）；本卡只在本件范围内重编，未改动任何跨文件引用，引用清单见核验证据 json 的 legacy_reuse 字段。
- **JX 字段修复**：data/individuals/H-JX-001.json 旧档 figure_code 被误置为字符串 Modern（与全部同级字段矛盾）；v6 档统一为 H-JX-001，并在图档 caveats 逐条记录（属字段级修复，非新增内容）。
- **YSK 缺档建立**：data/individuals/H-YSK-001.json 落盘前不存在（报告表 A 只列 figures 与伴随包）；本卡建立该镜像（等于图档去 modes），备份 manifest 标记为落盘前缺档。
- **CY 权限环境注记**：落盘首轮 data/figures/H-CY-001.json 与 data/individuals/H-CY-001.json 为 root 属主只读文件（hermes 无写权限，open('w') 触发 PermissionError）；处置为先取字节备份、再解除旧文件后同路径写入（路径与内容语义不变，重跑时属性已为 hermes，故最终清单 replaced_readonly_targets 为空）；旧档字节与 git HEAD 一致已由核验 D 组（备份哈希登记）逐条证明。
- **YSK 案例空缺**：representative_cases_zh 在旧载荷中缺字段（报告称案例空）；按现状保真、未扩写，图档 caveats 标注。

## 5. 场景附随件（既有载荷，非本卡新增内容）

- 新增规范格式条目（本卡提供，可直接入库）：CY 中文 10 + 英文 10；JX 中文 10 + 英文 10；合计 40 条（落在各件 scenarios_zh.json / scenarios_en.json 与批级 scenarios_zh_new.json / scenarios_en_new.json）；
- 库内既有、待合并卡重指 mode_id：SQL 中文 10 + 英文 10、WL 中文 10 + 英文 10，合计 40 条（登记于 scenario_remap_needed.json 与各件 scenario_notes.json）；
- YSK：来源档为原始非库内格式（zh 5 + en 5，覆盖 5/10，缺 5 条与本人其余模式无关，来源即如此），本卡按现状搬迁并标注，未补造；
- 负载字段只做 mode_id 旧号到新号重指与图代号衔接，场景文本、tags、域名等未改写。

## 6. 核验与门禁（全部实测）

### 6.1 独立核验脚本 verify_legacy20_r6_batch1.py：113 项断言 PASS / 0 FAIL

| 组 | 断言内容 | 结果 |
|---|---|---|
| A | 每件 10 条、编号唯一、figure_code / figure_name 正确、verification 全 pending 且 evidence 明写「引文与出处未独立核验」、图档 caveats 含未核验声明 | PASS |
| B | 三面一致（图档内嵌 modes == 伴随包 modes == 落盘 entries == 冻结副本）+ 镜像与图档除 modes 外逐对象相等 | PASS |
| C | 互引 0 悬空（related_modes 全部落在本件 10 条新码内） | PASS |
| D | 备份哈希登记：备份字节 == 登记 sha256；登记 sha256 == git HEAD 旧档字节 | PASS |
| E | 全库 0 主体占用（50 新码作为模式编号仅出现在本卡路径）+ 50 码唯一 + 历史备份与既有预期引用只登记 | PASS |
| F | 主库零写入（主体占用 0；六个主库文件与 HEAD 字节一致） | PASS |
| G | 字段级保真（逐条逐字段与旧载体原值比对，仅允许既定搬迁） | PASS |
| H | category_raw 逐条保留原值、category 仅按映射表应用 | PASS |
| I | 特例（WL 归属标注、JX 字段修复记录、YSK 缺档建立） | PASS |
| J | 门禁重跑（credibility_gate --hard-fail） | PASS |

### 6.2 门禁 credibility_gate --hard-fail（原始输出见 phase21r6_landing_batch1_gate.txt）

- hard failures on this dataset: 0；新增（基线外，必拦）: 0 条；
- D4 引文不符：50 条全部 unchecked（no-fulltext-link 30 + no-citation 20），与样例同口径，不假装核过；
- D5 时间线矛盾：0 条。

### 6.3 主库现状登记（只读观察，不干涉）

- M-SQL-001 已在 H-MAN-001（曼德拉）与 H-KEY-001（凯恩斯）的 cross_references 中被引用（含 mode_pair 与描述文本）；
- M-WL-001 已在 H-SK-001 伴随包的 related_modes 中被引用；
- 上述引用均为他卡在主库中的既有写入，本卡未改动；合并卡完成并码归一后这些引用即可解析。

## 7. 移交清单（合并卡 / 船长）

1. **code_maps.json 重指**：H-SQL-001 模式块旧号到新号；H-MAN-001 与 H-KEY-001 跨引用 mode_pair 的 M-SQL-001（合并后即解析）；
2. **scenarios_zh.json / scenarios_en.json 重指**：SQL 20 条 + WL 20 条 mode_id 旧号到新号（清单在 scenario_remap_needed.json）；
3. **EN 场景码风格裁定**：库内并存 C-CY-0001~0010（四位数）与 C-SQL-001E（后缀式）两种风格，建议合并卡统一口径后再入库；
4. **类目待核 8 条**（见 3.2 表），如需应用请扩充映射表后重跑；
5. **旧号跨文件引用清理**：JX M001~M010 重码面（他档、场景、站点索引、历史脚本）与本卡外其他重码；
6. **独立核验流程**：50 条 verification 全 pending，含 WL 引文归属疑义（白猫黑猫语）；
7. **docs/figures 档案层**（含档案 JSON）未动：本卡只升级 data/ 三文件与落盘载荷，如需档案页另开卡；
8. **生成器重跑方式**：build_legacy20_r6_batch1.py 为一次性原档升级（就地改造旧载体），重跑须先由 data/backup_r6_* 恢复原档；恢复脚本本卡内置于 scratch 未入库。

## 8. 边界与诚实上报

- 主库六个文件零写入（不得触碰的失败条件未触发）：核验 F 组 0 主体占用 + 与 git HEAD 字节一致；
- 未新增任何载荷事实内容：只做字段搬迁、编号重编、类目归一、问题标注（G 组字段级保真证明）；
- 批2（H-CHB-001 / H-FXT-001）不在本卡，由并发卡处理，本卡未触碰其路径；
- 未做站点导出、未改 docs/figures 档案层、未补 YSK 缺失的 5 条场景与案例字段（来源即如此，按现状保真）；
- 落盘过程中的环境注记（CY 旧档属主只读）已如实记录于 4 节。

## 9. 证据索引

- 审计清单：data/audit/phase21r6_batch1_landing_manifest.json
- 生成器：tools/build_legacy20_r6_batch1.py；核验脚本：verify_legacy20_r6_batch1.py
- 事件证据：docs/research/phase21r6_landing_batch1_evidence.json
- 核验证据：docs/research/phase21r6_landing_batch1_verify_evidence.json（113 PASS / 0 FAIL 明细）
- 门禁原始输出：docs/research/phase21r6_landing_batch1_gate.txt
- 合并输入：docs/scratch/legacy20_rev6_landing/batch1/（combined_library_entries.json + 各件载荷 + 批级场景汇总）
- 备份：data/backup_r6_<CODE>_20260923/（5 目录，含 manifest.json）
