# Phase 20 QA 验收报告：王夫之（Wang Fuzhi, H-WFZ-001）

- 任务: `t_ef2f2b30`（QA 审查，espinosa）→ 下游 `t_916357e9`（文档归档，pigafetta）
- 入库提交: `04a77491`（父 `830e3ccb`）；上游复核: `t_5626cc36`（barbosa，PASS / 零改动）
- 验收基线: 冻结快照 `git worktree @ 04a77491`（读 commit object，规避同仓并发写）+ 工作区（本卡热修后）
- 结论: **PASS（经热修）** —— 结构、索引、场景、镜像、档案全部达标；新发现并修复 **4 类 / 15 处** 文本缺陷（跨 6 文件 12 行）

---

## 一、脚本结果

| 脚本 | 环境 | 结果 |
|---|---|---|
| 上游 `verify_wangfuzhi_phase20.py`（68 项） | 修复前快照 `04a77491` | 68/68 PASS（未命中本次缺陷：判据缺口证据） |
| 上游 `verify_wangfuzhi_phase20.py` | 修复后快照（`04a77491` + 热修） | 68/68 PASS |
| 复核卡 `verify_wfz_indep.py`（64 项，barbosa） | （t_5626cc36 记录） | 64/64 PASS |
| 本卡独立 `verify_wfz_qa_espinosa.py`（状态组 64 项 + 增量组 12 项） | 修复后快照（`--parent 830e3ccb`） | **76/76 PASS** |
| 本卡独立 `verify_wfz_qa_espinosa.py`（反向验证） | 修复前快照 `04a77491` | **67/76**，恰好命中 9 项缺陷断言（6.5 + 8.1~8.8）✓ 判据非空转 |
| 本卡独立 `verify_wfz_qa_espinosa.py`（状态组） | 工作区（本卡修复后） | **64/64 PASS** |

独立脚本在写入仓库前**先对修复前快照复跑并复现缺陷**（9 项 FAIL），修复后复跑归零（76/76），确认判据有效。上游与复核脚本均未覆盖本次缺陷类别，故此前全部 PASS。

## 二、复核确认（无争议项）

1. 提交面 13 文件，与同批 Phase 20 单卡体例逐项同构（LJY/WYM 同 13 件）；共享大文件纯追加（`modes_data.json` 唯一删除行为 `total` 2918→2928）。
2. 库内模式 2918→2928 == `total`；新增恰为 `M-WFZ-001~010`；`mode_code == id`、`figure_code=H-WFZ-001`、`research_mode_id=M-WAN-00n` 一一对应；主库无 `M-WAN` 派生 ID 条目（M-WAN 仅作溯源字段，恰 10 条）。
3. 既有 2918 条模式逐字未变（canonical dump SHA256 前缀 `eee6b6ea…`，父/子一致）；既有场景 2143+2143、既有标签 7198、既有 code_maps 208 条全部逐字未变，零回归。
4. 每条模式 v6 字段集与先例 `M-LJY-001` 完全一致（27 键）；要素齐备：5 关键概念 / 4 步流程（中英）/ 3 代表案例（中英）/ 3 现代应用（中英）/ 双语定义引证 / verification 块。
5. 语言纯度：`M-WFZ-*` 全字段 `_en` 无 CJK、`_zh` 无拉丁词（严格判据亦零命中）；双语场景、tags、图档 `mode_evidence` 同验为零污染。
6. `data/individuals/H-WFZ-001_modes.json` 的 `thinking_modes_v6_phase20` 与主库**逐字一致**；Phase 21 建档 `modes`（M321~M330）保留，相对父提交仅差本卡 3 处定点纯度修复（10.12 项专门判据）。
7. 图档三镜像（`data/figures` ↔ `data/individuals` ↔ `docs/figures`）**16,889 B、SHA256 `aa4eedb10546…160c` 一致**；`mode_ids`/`modes`/`thinking_mode_count` 覆盖 10；`phase20` 溯源块记录 `H-WAN-001 → H-WFZ-001` 及 1:1 映射表；`mode_evidence` 引证与其 `key_quote_*`/`source_chapter` 逐字对齐；`protreptic_mapping` 覆盖 10。
8. `docs/figures/H-WFZ-001.md` 53,330 B：10 模式**全字段**（名称/定义/流程/案例/应用/引证/研究稿 ID/关联模式，中英）逐字等于库内；双语场景索引 20 条；省略号仅出现于古籍引证行；无 TODO/替换字符。
9. 场景 `C-WFZ-001~010`（zh）/`C-WFZ-001E~010E`（en）各 10 条：`mode_code` 顺序绑定、标题=模式名、`text_*` 构造式一致（标题+场景串接）、中英镜像字段逐字互等、纯度零污染。
10. `scenario_tags` 7198→7218（+20，zh/en 各 10）：键集/后缀/`language` 三向一致，全库无重复条目。
11. `code_maps.figures` 208→209 仅新增 `H-WFZ-001`；键集与近期 Phase 20 体例（H-LJY/H-WYM/H-CHE/H-ZDY）一致；`mode_ids` 10 / `tags` 10 模式名 / xref 2 条（黄宗羲、顾炎武）目标可达，且与图档 xref 逐字一致。
12. `figure_names` 唯一映射 `H-WFZ-001 → 王夫之`，无 `H-WAN` 派生码登记；全库新增引文与场景文本唯一性检查通过。

## 三、新发现缺陷（4 类 / 15 处，已修复）

### 类别 1：图档罗马化拼写错误（1 处文本 × 3 镜像）

| 文件 | 字段 | 修复前 | 修复后 |
|---|---|---|---|
| 三镜像 | `courtesy_name` | `Master Chuanshan (Shuanshan)` | `Master Chuanshan` |

- 依据：同文件内 `Chuanshan` 出现 4 处（`intellectual_tradition`、tag `Chuanshan School`、`description_en` 等）互证；`Shuanshan` 非任何通行罗马化（船山 = Chuanshan / Ch'uan-shan）。
- 根因：继承自 Phase 21 建档版 `data/figures/H-WFZ-001.json`（父提交即如此）；本次合并将其同步进三镜像，成为唯一权威值。上游三份脚本均未对 `courtesy_name` 做罗马化校验。

### 类别 2：图档罗马化订正（2 处文本 × 3 镜像）

| 字段 | 修复前 | 修复后 | 依据 |
|---|---|---|---|
| `description_en` | `courtesy name E'nong` | `courtesy name E-nong` | 与记录内规范字段 `style_name: "E-nong"` 及档案 md `style: E-nong` 统一（库内既有方案，不改方案本身） |
| `description_en` | `pseudonym Jiazhai` | `pseudonym Jiangzhai` | 姜斋 = Jiāngzhāi（zh.wikipedia 注「拼音：Jiāngzhāi」、chinaknowledge「style Jiangzhai」）；`Jiazhai` 为缺 `ng` 拼写 |

- 观察（不改）：字「而农」学界通行转写为 `Ernong`（en.wikipedia / chinaknowledge）；库内 `E-nong` 为既有方案，本卡仅统一内部一致性，是否全局改为 `Ernong` 建议由后续统一决策。

### 类别 3：英文语法错误（1 处文本 × 3 面：主库 / 源档 v6 / 档案 md）

| 位置 | 修复前 | 修复后 |
|---|---|---|
| `M-WFZ-001 representative_cases_en[1]` | `…the most fuller state of qi` | `…the fullest state of qi` |

- 本卡新增英译内容（`most` + 比较级双重比较错误）；三面同步修复。

### 类别 4：M321~M330 档案块中文夹英文残留（3 处文本 × 源档）

| 模式 | 字段 | 修复前 | 修复后 |
|---|---|---|---|
| M323 | `representative_cases_zh[0]` | `…——水同而水日新， Entities stay while their constituents renew every instant` | `…——水同而水日新`（半成品英译残片截除） |
| M324 | `modern_applications_zh[0]` | `…以史为据而非以古为 Ideal` | `…以史为据而非以古为理想`（对照同条英文 `rather than idealizing antiquity` 回填） |
| M329 | `modern_applications_zh[0]` | `…警惕 buzzword 替代真实判断` | `…警惕空泛时髦术语替代真实判断`（回填该块旧存档 `backups_merge_H-SJM-001_20260909_071433/modes_data.json:16984` 中存在的清理文本） |

- 根因：M321~M330 为 Phase 21 建档档案块（按策略保留、不混库），早期英译脚本的半成品残留长期未清；上游/复核脚本的纯度扫描仅覆盖 `M-WFZ-*`（主库 10 条），**未覆盖档案块**，形成「已 PASS 却带缺陷」的判据盲区。
- 本卡脚本 6.5 项补齐档案块纯度判据（判据说明：以“含小写的拉丁词”为违规、通行全大写缩写如 KPI 不判违规——与全库既有体例一致；对 `M-WFZ-*` 另以更严格判据复核亦零命中）。
- 保留策略不变：档案块仍不混入主库；仅 3 处定点纯度修复（10.12 项判据固定为「父提交 + 本卡 3 处定点修复」）。

**落盘明细**：6 文件 / 12 行（三镜像各 2 行、`modes_data.json` 1 行、`H-WFZ-001_modes.json` 4 行、档案 md 1 行）；提交前已逐行核对 diff 仅含预期改动（hunks-clean 校验通过）。

## 四、遗留与观察（非本卡引入，不阻塞）

- 上游研究稿 `phase20_wangfuzhi_research.md` 中 M-WAN-004 引文作「性者生理也」，库内作「性者，生理也」——标点微差（信息级）。
- 合并报告称档案 md 省略号「2 行」，实为 1 行（「……」为两个连续 U+2026）——表述级，数据本身一致（该行确为古籍引证行）。
- 存量 `data/scenarios_zh.json` 中 `C-IKH-008` 1 处 U+FFFD 替换字符：父提交已有，非本卡范围。
- 全库 `code_maps` 存量悬空 xref 6 条（H-DZS-001→GZ-XZ-001；H-SQL-001→H-MZD-001/H-ZET-001；H-SX-001/H-SY-001→H-QINSHI-001；H-SY-001→vs_hanfeizi）：与父提交同为 6 条，本卡零新增。
- `H-GYW-001`（顾炎武）未在 `code_maps.figures` 注册（其图档存在，xref 可解析）——上游已注记，属顾炎武卡范围。
- hotspot: `data/modes_data.json`（23 MB）等共享大文件为多卡并发写面；本卡仅做**定长局部替换**（字符串级，不整写文件），提交前核对 `git status`/diff 确认无他人未提交改动被夹带。

## 五、工件

- 独立验收脚本：`verify_wfz_qa_espinosa.py`（仓库根目录，76 项）
- 本报告：`docs/research/phase20_wangfuzhi_qa_report.md`
- 热修提交：本报告同批提交（6 文件 12 行 + 脚本 + 报告）

## 六、复现命令

```
python3 verify_wfz_qa_espinosa.py <REPO> [--parent 830e3ccb]
# 修复后快照: 76/76 PASS；修复前快照: 67/76（9 项缺陷断言命中）
```
