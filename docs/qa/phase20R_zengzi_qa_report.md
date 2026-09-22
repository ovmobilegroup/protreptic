# Phase20R 曾子 (H-ZX-001) 数据质量验收 QA 报告（独立验收）

- **验收卡**: t_8ceed107（espinosa，Phase20R 补做 4/5 QA 卡）
- **验收对象链**: 研究卡 t_6c92966b（serrano）→ 落地卡 t_4a9c2c2e（elcano，commit `4f447608`）→ 合并卡 t_16ebe5c9（barbosa，commit `da4b240e` + 报告补注 `a7666151`）
- **验收基准**: 验收启动时点工作区快照；主库五件 sha256 与合并 manifest `sha256_after` 逐一相等（§1），合并前备份件 sha256 与 `sha256_before` 逐一相等
- **方法**: 独立第二实现 `verify_zengzi_qa_espinosa.py`（**83 断言 / 10 组（0、A~I）**，不 import 上游脚本、不采信上游自述；只读）＋ 原典抽样复核（ctext.org / 维基文库公开底本）＋ 上游三脚本命令级复跑
- **结论（验收对象提交时点）: PASS —— 83 PASS / 0 FAIL / 5 INFO；0 项数据缺陷，0 处数据热修**（对合并快照 `da4b240e` 状态的独立复跑：上游 66/31/26 与 83 断言全绿）
- **验收后并发回归警示（P1，§5.4）**: 本卡提交窗口内，共享热点被在途卡（收尾卡 t_ea3a32e5）写入，**M-ZX-001~010 的 `verification` 字段在库内被整体改写**（定稿四类状态与留证 note 被替换为 phase38-y2 自动扫描口径），致“四面同体”与合并卡 66/66 复跑在**工作区现行状态**下命中 FAIL。该写入非本验收对象链所为，修复权属归 t_ea3a32e5 范围；本卡已在证据包 §5 与报告 §5.4 完整留证，并在该卡评论中报知。
- **口径更新留证 2 处**（§5.2）：上游引用面白名单并入本卡 QA 产物；QA 产物入库（两者均已在提交注记中说明，断言本体未动）

---

## 1. 验收快照与对账（0 组断言 / 14 项）

| 文件 | 计数（实测） | sha256(16) 实测 | 对账 |
|---|---|---|---|
| `data/modes_data.json` | 3152 条 | `9d9c98c5547a7edd` | == manifest.after ✓（备份 `83be45b5bf63185f` == before ✓） |
| `data/code_maps.json` | figures 212 | `b4a6cf13d35d8c57` | == manifest.after ✓（备份 `b7e590e76d1661e7` ✓） |
| `data/scenarios_zh.json` | 2183 条 | `65a85dba9f51ea70` | == manifest.after ✓（备份 `f99c5a6259adc584` ✓） |
| `data/scenarios_en.json` | 2183 条 | `af6ee58fe810305c` | == manifest.after ✓（备份 `bb9bfc28d800f203` ✓） |
| `data/scenario_tags.json` | 7278 条 | `5d36fae364674a96` | == manifest.after ✓（备份 `ce5557e5d9c014fa` ✓） |
| 图档三镜像 `data/figures/H-ZX-001.json` / `data/individuals/H-ZX-001.json` / `docs/figures/H-ZX-001.json` | 91,153 B ×3 | `ba2ad769f5ba7eef` ×3 | 三镜像同 sha ✓；与落地 manifest `mirrors.sha256` 一致 ✓ |

- 备份基准目录：`/opt/data/kanban/boards/protreptic/workspaces/t_16ebe5c9/backup_merge_H-ZX-001_20260922_230038`（5 件，逐件 sha 对账通过）。

## 2. 十条模式逐条核验（卡要求①；A 组 16 断言）

### 2.1 结构与字段

- A1~A9：库内 `M-ZX-001~010` 恰 10 条、按序；26 个必备字段逐条非空；`id == mode_code`；`research_mode_id` 溯源 M230~M239 1:1；`figure_code/figure_name` 逐条 = `H-ZX-001/曾子`；`related_modes` 全为新号（零旧号残链）；`verification.status` 逐条就位（4 类：`quote-verified` ×7、`source-verified-corrected` ×1（007）、`corrected-fabricated-quote` ×1（009）、`corrected-misattribution` ×1（010））；`attribution_note_zh/en` 10 条齐备。
- A11：出处章名 10 条逐字精确（含 007 补全为《论语·泰伯》＋《孝经·开宗明义章》＋补充《礼记·檀弓上》）。

### 2.2 原典抽样复核（公开底本逐字对照；A10/A10b 离线复核 32 串）

| 模式 | 引文（节选） | 对照底本（本次复核） | 结果 |
|---|---|---|---|
| M-ZX-001 | 此谓诚于中，形于外，故君子必慎其独也。／莫见乎隐，莫显乎微，故君子慎其独也。 | 维基文库《禮記/大學》诚意章；《禮記/中庸》首章 | 逐字一致 ✓ |
| M-ZX-002 | 古之欲明明德于天下者，先治其国……致知在格物。 | 维基文库《禮記/大學》经文 | 逐字一致 ✓ |
| M-ZX-003 | 夫孝，德之本也，教之所由生也。／夫孝者，天下之大经也。／孝有三：大孝尊亲，其次不辱，其下能养。／身者，亲之遗体也。 | 维基文库《今文孝經》开宗明义章；《大戴禮記/曾子大孝》 | 逐字一致 ✓ |
| M-ZX-004 | 参乎！吾道一以贯之。……夫子之道，忠恕而已矣。 | 维基文库《論語/里仁第四》15 章 | 逐字一致 ✓ |
| M-ZX-005 | 吾日三省吾身：为人谋而不忠乎？与朋友交而不信乎？传不习乎？ | ctext.org《論語·學而》4 章 | 逐字一致 ✓ |
| M-ZX-006 | 士不可以不弘毅，任重而道远。仁以为己任，不亦重乎？死而后已，不亦远乎？ | ctext.org《論語·泰伯》7 章 | 逐字一致 ✓ |
| M-ZX-007 | 启予足！启予手！《诗》云：战战兢兢，如临深渊，如履薄冰。／身体发肤，受之父母，不敢毁伤，孝之始也。 | ctext.org《論語·泰伯》4 章（诗句同见维基文库《今文孝經》诸侯章）；《今文孝經》开宗明义章 | 一致 ✓（诗经二句在《孝经·诸侯章》得以独立互证） |
| M-ZX-008 | 可以托六尺之孤，可以寄百里之命，临大节而不可夺也。君子人与？君子人也。 | ctext.org《論語·泰伯》6 章 | 逐字一致 ✓ |
| M-ZX-009 | 先王见教之可以化民也……示之以好恶，而民知禁。／其教不肃而成，其政不严而治。 | 维基文库《今文孝經》三才章 | 一致 ✓（“其教不肃而成，其政不严而治”在 009 定义/证例/（同章）三处口径一致） |
| M-ZX-010 | 鸟之将死，其鸣也哀；人之将死，其言也善。君子所贵乎道者三：动容貌，斯远暴慢矣；正颜色，斯近信矣；出辞气，斯远鄙倍矣。笾豆之事，则有司存。 | ctext.org《論語·泰伯》4 章（孟敬子章） | 逐字一致 ✓ |

- 抽样覆盖率：10/10 条模式各至少 1 条引文经**独立公开底本**逐字复核；合计核串 32 条（其中 24 条为 `key_quote_zh` 严格面断言，8 条为定义/证例面补充串）。
- 底本处置说明：ctext.org 对《孝经》两章启用反爬（返回告警页），已改用**维基文库《今文孝經》**等价公开底本完成复核，并保留同上对照记录。
- 归属标注侧抽样：`《史记·仲尼弟子列传》`“孔子以为能通孝道，故授之业，作孝经”、`韩愈《原道》/朱熹《中庸章句序》`道统叙事、`《庄子·天下》`“内圣外王”术语、`朱熹《论语集注》`“尽己之谓忠，推己之谓恕”等均按“传统归属/后世建构/注疏语”标注（见 `attribution_notes` 6 条与各模式 `attribution_note_zh/en`），未发现误植为曾子原语的情况；`Q562 → Q1207671` 误码仅存修正记录。

### 2.3 旧伪文 / 误引清零（A12~A15）

- `君子所乎民者` / `则民亦如是乎`（M238 伪造引文）、`匡人其如予何` / `天之未丧斯文也`（M239 误引《子罕》孔子语）、`不欺暗室`（后世成语）：在 10 条模式的**活动字段**（名称/定义/出处/概念/引文/步骤/应用/相关）**0 命中**；全部写入修正记录留证（`correction_zh`（009/010）+ 图档 `corrections_log`）。
- 替换后的定稿引文（三才章五事、孟敬子章）已在 A10/A10b 逐字在位。

## 3. 全库完整性（卡要求②；B/C/D/E 组 22 断言）

- **四面逐字同体**（B1，强判据 deep-equal）：库内 10 条 == 图档内嵌 `thinking_modes` == `data/individuals/H-ZX-001_modes.json` 正本 `modes` == 伴随包 `thinking_modes_v6_phase20`（含 `correction_zh` 在内的 32 键逐字全等，无一字段松散）。
- 图档面：`mode_ids`/`mode_id_mapping`/`modes` 字段与定稿一致；`thinking_modes` 恰 10 条；`thinking_mode_count=10`；`protreptic_mapping` 覆盖 10 ids；`mode_evidence` 10 条；`tags` 59 条（≥40）；`modern_value_zh/en` 各 7 条；`attribution_notes` 6 条；`corrections_log` 10 条；反混淆块 4 目标 + `no-content-contamination`。
- **0 重复 id**（F1）：全库 2,752 个非空模式 id 无重复；400 条 `None-id` 条目为历史遗留（before == after，零新增，与备份逐项一致）；`M-ZX-NNN` 全库恰 10 条。
- 场景面（C 组）：zh/en 各 10 条（C-ZX-001~010 / C-ZX-001E~010E），结构 == 先例 8 字段；标题/正文/应用域与模式条目**逐字段一致**（正文模板断言通过）；zh/en 条目内容同体（仅 `code` 异，与 H-ZXC 先例一致）；`M-ZX-` 引用收敛于本 20 条（无越界场景）。
- 标签面（D 组）：20 条 4 键 `{mode_code, tag, figure_code, language}` 与 H-ZXC/H-DZ/H-WFZ 先例同构；标签名 == 模式名 + `_zh`/`_en`；覆盖 10 模式 × 双语双向 1:1；无重复；其他图 0 条 M-ZX 标签。
- 登记面（E 组）：`code_maps.figures.H-ZX-001` 3 键定稿；`mode_ids` == 定稿 10 号；`tags` == 10 模式中文名（按序）；交叉引用 3 条（H-KZ-001 继承 / H-MZ-001 学脉 / H-ZHX-001 道统）与图档逐条一致；**零悬空**（双判据可达）；`M-ZX-` 模式号仅 H-ZX-001 登记（全局无第二占用者）。

## 4. 旧号与僵尸清零（卡要求③；F 组 14 断言）

- **旧号 M230-M239**：不作任何条目 id 复活（F4）；`research_mode_id` 面恰 10 次且全部落在本 10 条（F5）；10 条活动字段零旧号（F6；唯一豁免：M-ZX-008 `verification.note` 中出现 “M236” 系旧稿说明留证，属约定允许字段）。
- **僵尸 Gen F**：`M-ZS-*` 0 条；主库六件（含 figure_names）`H-ZS-001` 0 命中（F11）；`data/individuals/H-ZS-001*`、`docs/figures/H-ZS-001.md`、根副本、旧脚本等 15 件全部归档于 `data/figures/_duplicates/**` 且**归档字节 sha 匹配**、源件已移除（F13；仅 2 件 staging 为“已替代/已改码”例外，记录在落地 manifest）；staging 改码 `C-ZX-001~010 / C-ZX-001E~010E`、零 GenF 残留（F14）。
- **编号避让**：`M311-M318` 8 条现属顾炎武（H-GYW-001），曾子侧不回收（F7）；`H-ZS-001` 键已从 figure_names 删除（F9，避让朱升研究 H-ZS-001~004）；figure_names 曾子映射仅 `H-ZX-001` 系三键、无第二规范码（F10）。
- **旧数字码**：`H-ZZ-166/H-ZZ-222` 在主库 `code_maps.json`/`figure_names.json` 0 命中（F12；`tools/` 层遗留别名属残留清单 #14/#15 记录项，未动）。

## 5. 命令级复现上游证据（卡要求④；H/I 组 7 断言）

### 5.1 三脚本复跑（QA 时点，同一工作区状态）

| 脚本 | 结果 | 断言数 |
|---|---|---|
| `verify_hzx_merge_phase20R.py` | `== RESULT: 66 PASS / 0 FAIL ==` | 66（含内嵌复跑上游两脚本） |
| `verify_hzx_phase20R.py` | `== RESULT: 31 PASS / 0 FAIL ==` | 31 |
| `verify_hzx_landing.py` | `== RESULT: 26 PASS / 0 FAIL ==` | 26 |

- 三段原始输出随本报告附证据文件 `docs/qa/phase20R_zengzi_qa_evidence.txt`。
- 合并 manifest 计数 vs 库内实测：modes 3152 / code_maps 212 / scenarios 2183+2183 / tags 7278 **全部一致**（I4）。

### 5.2 口径更新留证（2 处，断言本体未动）

1. **引用面白名单并入 QA 产物**（本卡）：上游两脚本的 `M-ZX-001` 引用面检查（`grep --include=*.json --include=*.md`）会命中本卡产物 `docs/qa/phase20R_zengzi_qa_report.md`。按落地上游先例（“产品并入引用面”），将 `./docs/qa/phase20R_zengzi_qa_report.md`、`./verify_zengzi_qa_espinosa.py` 并入白名单；**“零越界写入”语义不变**，其余断言未动。复跑后仍 66/66、31/31 全绿。
2. **合并卡既有 2 处口径更新**（da4b240e 内，已在上游报告留证）：phase20R 上游脚本引用面白名单并入主库写入面；landing 脚本 “main library untouched” 断言更新为“主库已携带 M-ZX-001~010”。本卡逐项核对语义，判定为**合理且必要**（落地时点断言 vs 合并后事实），无异议。

### 5.4 验收后并发漂移复核与并发回归警示（P1）

**背景**：主库五件是本批多卡共享热点（合并报告已标注 hotspot），在途收尾卡 t_ea3a32e5 的“verification 归位 / 重建推送”等工作在 QA 提交窗口内继续写入工作区。

**复核方法与结论**（证据：`docs/qa/phase20R_zengzi_qa_evidence.txt` §5）：

| 面 | 工作区 vs 合并提交 `da4b240e` | 判定 |
|---|---|---|
| M-ZX-001~010 条目（库内） | **差异：10 条 `verification` 字段被整体改写** | 回归 ✗ |
| code_maps `H-ZX-001` 条目 | 零差异 | 通过 ✓ |
| `C-ZX-*` 场景（zh/en） | 零差异 | 通过 ✓ |
| `H-ZX-001` 标签 20 条 | 零差异 | 通过 ✓ |

- 改写内容：定稿 `verification`（`quote-verified` / `source-verified-corrected` / `corrected-fabricated-quote` / `corrected-misattribution` ＋ `checked_on`/`method`/`note` 留证）→ `{"status": "pending"|"verified", "method": "auto-scan"|"link-resolved", "evidence": "unresolved: 引文未在 source_links.json 建立链接源"|维基文库链接, "checked_at", "checker": "phase38-y2"}`。
- 影响：① **四面逐字同体被破坏**（individuals 正本/图档三镜像未同步改写，仅有主库副本被改，非对称）；② 定稿修正留证（如 M-ZX-009 伪造引文替换、M-ZX-005 三省注、M-ZX-008 旧稿说明）在**库内视图**丢失；③ 合并卡核验复跑由 66/66 降为 **59 PASS / 7 FAIL**（4 项属该回归：A10/A11 三面同体、A17/A17b verification 枚举与修正留证；3 项 E1/E3/E4 系并发卡库级写入 [+20/-10 条] 致“纯追加台账”相对合并前备份不再全等）。
- 本卡独立脚本复跑：**78 PASS / 3 FAIL / 7 INFO**，3 项 FAIL（0.4 漂移零差异、B1 四面同体、H1 合并脚本 66 复跑）全部由同一根因触发，其余 78 项（含原典复核、旧号/僵尸清零、场景/标签/登记面）仍全绿。
- **处置**：本卡不热修他卡在途写入（避免与其在途状态互踩）。修复建议（供 t_ea3a32e5/编排裁定）：(a) 将 Phase20R 定稿条目（M-ZX-*）排除于自动 `verification` 归位之外（其 verification 属定稿留证字段），或 (b) 若全域标准化为既定口径，则需同步改写正本与三镜像、并在两处 manifest / 验收口径留证后复跑上游脚本至全绿。任一方案落地后，本卡脚本即可复跑验证恢复。

### 5.3 证据链自证

- 合并脚本指纹：证据包附录 A 全文 sha256 == manifest `merge_script_sha256` `176d692e2ff1bc4049a6aee38b7769b3fa6ce1d035f5ad4e3bd298d6b20fbd84`（I1 通过，附录全文 9,603 字符）。
- 证据包含 dry-run 幂等护栏与 `ABORT` 记录（重跑护栏有效）、含 66/31/26 三段结果（I2/I3）。

## 6. 问题清单

- **P0（阻断）：无。**
- **P1（须修，验收后并发回归）**: 1 项 —— M-ZX-001~010 库内 `verification` 字段被在途卡 t_ea3a32e5 改写，破坏四面同体与定稿留证（详见 §5.4）。归属该卡/编排裁定，非本验收对象链缺陷。
- **0 处数据热修**（对验收对象：独立验收未发现任何需修正缺陷，数据面零写入）。
- **P2 观察项（非阻塞，记录/交接）**：
  1. `legacy_field_aliases` 为说明性留证字段（10 条独有，库内其余 0 处）；真实别名 `process`/`modern_applications` 同载于条目，无消费风险。
  2. 图档 `source_files` 含非路径描述项（“phase20_zengzi_QA报告见 final 第 5 节”）；任何修正须同步三镜像与两处 manifest，收益小于风险，**本卡不改**（建议随 5/5 文档卡或收尾卡顺带处理）。
  3. `modes_data.total=2948` 与 `len(modes)=3152` 漂移（194 为 Phase21-R 恢复 + 10 为本批）——合并卡已留交接，建议收尾卡 t_ea3a32e5 一次性裁定。
  4. 发布仓未镜像本批（`4f447608`/`da4b240e`）、站点计数锚点 3132/304 待更新——收尾卡 t_ea3a32e5 范围。
  5. 根目录旧档 `modes_data.json`（101 图块汇编，含曾子旧号块）仍在，为残留清单 #16 未闭环项——建议编排另立清理卡复核归宿。

## 7. 证据与复现

- 独立验收脚本：`verify_zengzi_qa_espinosa.py`（仓库根，83 断言 / 10 组）。复现命令：
  - 合并快照工作区（验收时点；五件 sha256 == manifest.after）：`python3 verify_zengzi_qa_espinosa.py` → `== QA RESULT: 83 PASS / 0 FAIL / 5 INFO ==`（exit 0；原始输出见证据包 §2）
  - 验收后并发漂移工作区（现状）：同命令 → `78 PASS / 3 FAIL / 7 INFO`（3 FAIL 为同一并发回归根因；原始输出见证据包 §5.2）
  - 上游三脚本：`python3 verify_hzx_merge_phase20R.py`（66）／`python3 verify_hzx_phase20R.py`（31）／`python3 verify_hzx_landing.py`（26）
- 证据文件：`docs/qa/phase20R_zengzi_qa_evidence.txt`（QA 全量输出 + 上游三段原始输出 + 快照 sha256 台账 + 本卡变更清单）。
- 引用：`data/audit/phase20R_zengzi_merge_manifest.json`、`data/audit/phase20R_zengzi_landing_manifest.json`、`docs/research/phase20R_zengzi_merge_report.md`、`docs/research/phase20R_zengzi_merge_evidence.txt`、`docs/research/phase20R_zengzi_landing_report.md`、`docs/research/phase20R_zengzi_residual_inventory.md`、`docs/research/phase20_zengzi_research_final.md`。

## 8. 边界（本卡未做 / 明示）

- 未改任何数据面文件（0 热修）：主库五件在本卡提交中**零写入**（提交仅涉本卡产物与两处口径注释）。
- 未改 `docs/figures/H-ZX-001.md` 与展示层（归 5/5 文档归档卡 t_6c7e070a / 收尾卡）。
- 未镜像发布仓、未改站点计数锚点（收尾卡 t_ea3a32e5）。
- 未动根目录旧档 `modes_data.json`（残留清单 #16）与 `tools/` 层旧别名记录项（#14/#15）。

---
*Phase20R 补做·QA 卡 t_8ceed107（espinosa）· 2026-09-22 · 结论：验收对象提交时点 PASS（83/0/5）；验收后并发回归 1 项 P1（§5.4，归属收尾卡 t_ea3a32e5）*
