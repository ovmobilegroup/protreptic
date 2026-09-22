# Phase 20 落地报告：章学诚 (Zhang Xuecheng, H-ZXC-001) 数据入库

- **本卡**: t_43a3ef20（[Phase 20] 落地实现：章学诚 数据入库，assignee: elcano）
- **上游研究卡**: t_2c3626f4（[Phase 20] 深度研究，产出 10 条 v6 模式 M359~M368，报告 `phase20_zhangxuecheng_research.md`）
- **下游卡**: t_7326611d（barbosa，数据合并复核）
- **落地 commit**: `6e429676`（13 文件，+3555/−713）
- **落地时间**: 2026-09-22 15:39（TS=20260922_153920）
- **验收脚本**: `verify_zhangxuecheng_phase20.py` → **74/74 PASS**
- **落地前备份**: `workspaces/t_43a3ef20/backup_merge_H-ZXC-001_20260922_153920/`（9 个文件逐项可比对）

## 一、编码裁定

| 维度 | 研究稿（上游） | 库内 canonical（本次落库） |
|---|---|---|
| figure 码 | `H-ZXC-001` | `H-ZXC-001`（`data/figure_names.json` 唯一映射 `"H-ZXC-001": "章学诚"`，无第二编码） |
| 模式 ID | `M359` ~ `M368` | `M-ZXC-001` ~ `M-ZXC-010` |
| 场景 ID | `C-ZXC-001` ~ `C-ZXC-010` | `C-ZXC-001` ~ `C-ZXC-010` / `C-ZXC-001E` ~ `C-ZXC-010E` |

- 上游 figure 码与库内既有码一致（不同于戴震/王阳明等卡需 rebase 码的情形）；模式 ID 统一为库内规范的 figure 前缀编码 `M-ZXC-*`（与 M-DZ / M-WFZ / M-WYM / M-LJY / M-ZDY 等近期入库同构）。
- 每条模式的 `research_mode_id` 字段保留原始 ID（M359~M368），1:1 映射表写入图档 `phase20.mode_id_mapping`（M359→M-ZXC-001 … M368→M-ZXC-010）。
- 原始编号 M359~M368 同时是 Phase 21 建档编号（见第四节），本次以 v6 版内容为准，建档版保留于档案载体，不覆盖。

## 二、主库写入清单（before → after，均为纯追加、零删除、零改写）

| 文件 | 变更 | 计数 |
|---|---|---|
| `data/modes_data.json` | +10 条模式（M-ZXC-001~010，追加于 modes 末尾） | 2938 → 2948（`total` 同步） |
| `data/code_maps.json` | `figures.H-ZXC-001` 首次注册（mode_ids 10 / tags 10 / cross_references 3） | figures 210 → 211 |
| `data/scenarios_zh.json` | +10（C-ZXC-001~010） | 2163 → 2173 |
| `data/scenarios_en.json` | +10（C-ZXC-001E~010E） | 2163 → 2173 |
| `data/scenario_tags.json` | +20（zh/en 各 10，覆盖 0 条旧的 H-ZXC 标签） | 7238 → 7258 |
| `data/figures/H-ZXC-001.json` | 图档主档更新（见第三节） | 15161 → 16712 字节 |
| `data/individuals/H-ZXC-001.json` | 二镜像同步（并入 figures 主档专有字段 20 项）；内联 `modes`（完整条目）规范为 ID 列表（与 H-DZ-001 镜像同构），完整建档条目存于 `H-ZXC-001_modes.json`（内容零丢失，备份比对） | 37136 → 16712 字节 |
| `docs/figures/H-ZXC-001.json` | 三镜像**本次新建**（此前缺失） | 新增 16712 字节 |
| `data/individuals/H-ZXC-001_modes.json` | +`thinking_modes_v6_phase20` / `modes_ref` / `phase20_note`（legacy `modes` 逐字未动） | 32978 → 72975 字节 |
| `data/individuals/phase20_zhangxuecheng_research.md` | 上游研究稿原样归档（附件 SHA256 一致） | 新增 10681 字节 |
| `docs/figures/H-ZXC-001.md` | Phase 20 档案重建（七节结构） | 14723 → 46120 字节 |

场景条目结构对齐近期入库（`code/mode_code/title_zh/title_en/text_zh/text_en/application_area_zh/application_area_en`），scenario_tags 结构对齐 H-DZ/H-WFZ/H-WYM/H-LJY（`{mode_code, tag, figure_code, language}`）。

## 三、图档三镜像

- `data/figures/H-ZXC-001.json` ⇄ `data/individuals/H-ZXC-001.json` ⇄ `docs/figures/H-ZXC-001.json`
- 三处 SHA256 一致：`c69dafc8940c017b965d44efb84518c25396d1d212116897f87d4f0352d38778`
- 字段更新：`mode_ids`/`modes`（M-ZXC-001~010）、`thinking_mode_count=10`、`mode_evidence`（10 条，按 Phase 20 模式重写，含 source_chapter 与中英引证）、`protreptic_mapping`（10 类目 → 10 模式，1:1）、`tags`（57 → 80；原有 57 条**零丢失**，新增 23 条 = 10 中英模式名中的新增项 + 人物/学派/典籍标签）、`phase20` 溯源块（research→library 映射）、`source_files`（+研究稿两件）、`mode_ids_note`。
- 未动正文：`core_thoughts`（7 项）、`historical_significance`、`unique_thing`、`influence`、`modern_value_zh` 与落地前逐字一致（备份比对，验收项 #52）。
- 交叉引用 3 条（保留原语义）：`H-DZ-001`（戴震，comparison）、`H-GYW-001`（顾炎武，comparison）、`H-HZX-001`（黄宗羲，influence）；双判据（code_maps 注册 或 data/figures 存在）全部可达，无悬空（H-GYW-001 未注册 code_maps 但有图档）。

## 四、Phase 21 建档数据的保全

`data/individuals/H-ZXC-001_modes.json` 的 `modes`（M359~M368，10 条）与 `data/individuals/H-ZXC-001.json` 落地前的内联 modes 逐字一致；本次未覆盖 `modes`，只新增 `thinking_modes_v6_phase20`（= 主库 10 条 v6 模式，逐字一致）与 `modes_ref`/`phase20_note`。主库**不含** M359~M368 编号条目（验收项 #23）；建档版与 v6 版的差异仅为 v6 新增 `representative_cases_en` 与 `representative_figures` 两个字段，其余字段逐字相同。

## 五、上游研究稿语言纯度修复（4 处）

| 模式 | 字段 | 修复前 | 修复后 |
|---|---|---|---|
| M-ZXC-004 | representative_cases_en | `…disdain for historiographical论作` | `…disdain for works of historiographical judgment` |
| M-ZXC-006 | representative_cases_en | `…a comprehensive historiographical梳理 through…` | `…a comprehensive historiographical survey through…` |
| M-ZXC-007 | representative_cases_en | `Proposed设立 'zhi ke'…` | `Proposed establishing 'zhi ke'…` |
| M-ZXC-009 | modern_applications_zh | `代码评审与学术评审中的 steelman 原则` | `代码评审与学术评审中的钢人论证原则（先重构对方最强论证再评判）` |

修复后全量扫描：M-ZXC-* 及 C-ZXC-* 无 `_en` 夹中文 / `_zh` 夹 3+ 拉丁词残留（验收项 #11/#22/#30/#31）。

## 六、Phase 20 档案 md 重建

`docs/figures/H-ZXC-001.md`：14723 → 46120 字节，七节结构（历史定位 / 核心思想 / 十大思维模式 / 双语场景索引 / 跨引用 / 现代价值 / 入库说明与 QA 验收记录），与 H-DZ-001、H-WFZ-001、H-LJY-001 同构；模式定义中英与库内逐字一致（验收项 #58）。头部登记链已补全：库内模式区间、上游研究稿路径与卡号（t_2c3626f4）、落地 commit `6e429676`、本卡号与验收结果（74/74 PASS）。

## 七、独立验收

```
cd /opt/data/workspace/Protreptic && python3 verify_zhangxuecheng_phase20.py
CHECK RESULT: 74/74 PASS
```

覆盖：库内模式条目（1~16）、源研究档一致性（17~24）、双语场景（25~31）、scenario_tags（32~36）、code_maps（37~40）、图档与三镜像（41~55）、档案 md（56~62）、全库级一致性（63~68）、归档与计数（69~72）。

## 八、遗留与热点

- **热点（多卡共享大文件）**：`data/modes_data.json`、`data/code_maps.json`、`data/scenario_tags.json`、`data/scenarios_zh.json`、`data/scenarios_en.json`——本卡仅追加自身足迹（+10 模式 / +1 figure / +20 标签 / 各 +10 场景），未改动他人数据（与备份逐项比对）。
- **Sep-9 遗留件（未动）**：`merge_zxc.py`、`qa_zxc_final.py` 与 `data/*_entry_H-ZXC-001.json` 三件是 Phase 21 时代为 章学诚 准备的合并件（当时未执行）。本次 Phase 20 落地已用 canonical 码完成同一批数据的合并；该旧脚本若再执行，会在 `assert key not in data`（code_maps 已注册 H-ZXC-001）处即失败，不会重复写入。建议由维护卡统一废弃或改写，本卡未动以免越权。
- **既有库级现象（非本卡引入）**：全库 400 条匿名模式（`id` 为 null）落地前后均为 400，未受影响。
