# Phase 20 落地实现报告: 周敦颐 (ZhouDunyi, H-ZDY-001)

- 任务: t_a7fc5052 (elcano) ← 上游研究 t_f43f4e59 (serrano)
- 时间: 20260922_132519
- 研究稿编码: H-ZHO-001 / M-ZHO-001~010 → 库内编码: H-ZDY-001 / M-ZDY-001~010

## 一、编码裁定

库内 `周敦颐` 的 canonical code 为 **H-ZDY-001**（证据：data/figure_names.json 唯一映射
"H-ZDY-001"→"周敦颐"；data/figures/H-ZDY-001.json、data/individuals/H-ZDY-001*.json、
docs/figures/H-ZDY-001.md 均已存在，且 figure 内 mode_evidence/modes 指向 M-ZDY-001~010）。
研究稿自动派生码 H-ZHO-001 与既有编码冲突，同一人物不得双码，故落库统一采用 H-ZDY-001，
并以 `research_mode_id` 字段完整保留研究稿原始 ID 以便溯源。

## 二、写入清单

| 文件 | 变更 |
|---|---|
| data/modes_data.json | +10 条 M-ZDY-001~010（figure_code=H-ZDY-001）；修正 `total` 字段 → 2898 |
| data/code_maps.json | 注册 figures["H-ZDY-001"]（mode_ids 10 + tags 10 + cross_references 3） |
| data/scenarios_zh.json | +10 条 C-ZDY-001~010 |
| data/scenarios_en.json | +10 条 C-ZDY-001E~010E |
| data/scenario_tags.json | +20 条（zh/en 各 10） |
| data/figures/H-ZDY-001.json | mode_ids/modes/mode_evidence/protreptic_mapping/tags/source_files 更新 |
| data/individuals/H-ZDY-001.json | 同上（同步镜像） |
| data/individuals/H-ZDY-001_modes.json | 新增 `thinking_modes_v6_phase20`（Phase 21 原始 thinking_modes 保留） |
| docs/figures/H-ZDY-001.md | Phase 20 研究档案（10 模式全文） |
| docs/figures/H-ZDY-001.json | data/figures 字节镜像 |

备份: data/backup_merge_H-ZDY-001_20260922_132519/

## 三、跨引用（均已存在于 code_maps）

- H-ZZ-001 张载 — 同代本体论互补
- H-CHE-001 程颢 — 受业弟子（寻孔颜乐处）
- H-CHI-001 程颐 — 受业弟子（主敬涵养/性即理之转进）

## 四、ID 映射

- M-ZHO-001 → M-ZDY-001（无极而太极法）
- M-ZHO-002 → M-ZDY-002（动静互根法）
- M-ZHO-003 → M-ZDY-003（诚为本体法）
- M-ZHO-004 → M-ZDY-004（五性感动法）
- M-ZHO-005 → M-ZDY-005（主静立极法）
- M-ZHO-006 → M-ZDY-006（万物各一太极法）
- M-ZHO-007 → M-ZDY-007（阴阳五行贯通法）
- M-ZHO-008 → M-ZDY-008（原始反终法）
- M-ZHO-009 → M-ZDY-009（几微洞察法）
- M-ZHO-010 → M-ZDY-010（无欲静虚法）

## 五、验证要点

- modes_data.json `total` 与 len(modes) 一致
- M-ZDY-* / M-ZHO-* 无重复 ID，无 figure_code 冲突
- 场景 zh/en 一一配对（C-ZDY-00N ↔ C-ZDY-00NE）
- code_maps 注册且 cross_references 目标均已注册
- figure mode_ids == modes_data 中 figure_code={FIG_CODE} 的模式集合
