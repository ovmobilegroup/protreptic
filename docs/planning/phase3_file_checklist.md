# Phase 3 文件修改清单

**生成时间**: 2026-08-13
**当前状态**: 规划完成

## 需修改/新增文件

### 核心数据文件

- [ ] `tools/scenarios_zh.json` - 新增 45 个 H-* 场景条目
- [ ] `tools/scenarios_en.json` - 新增 45 个 H-* 场景条目（中英对齐）
- [ ] `tools/code_maps.json` - 同步更新 CODE_MAP / CODE_MAP_EN (新增 45 条)
- [ ] `tools/modes_data.json` - 若需新增模式则更新 (优先复用现有 42 模式)

### 文档文件

- [ ] `docs/historical_figures_thinking_modes_library.md` - 重新生成完整档案库 (含 256 位历史人物)
- [ ] `tools/three_dimensional_comparison_matrix.xlsx` - 重新生成含 256 位历史人物的权重矩阵

### 规划/研究文档

- [x] `docs/planning/phase3_candidates.md` - 45 位候选人名单 ✓
- [ ] `docs/research/phase3_detailed_research.md` - 45 位深度调研报告
- [x] `docs/planning/phase3_file_checklist.md` - 本文件 ✓
- [ ] `docs/review/phase3_review_report.md` - 审查报告
- [ ] `docs/terminology/phase3_terminology.md` - 术语对照表

### 测试文件

- [ ] `tools/test_thinking_mode_selector.py` - 更新断言 (总场景数 276，历史人物 256)

### 技能目录同步

- [ ] `~/.hermes/skills/ultimate-thinking-and-writing-methods/scripts/thinking_mode_selector.py`
- [ ] `~/.hermes/skills/ultimate-thinking-and-writing-methods/scripts/scenarios_zh.json`
- [ ] `~/.hermes/skills/ultimate-thinking-and-writing-methods/scripts/scenarios_en.json`
- [ ] `~/.hermes/skills/ultimate-thinking-and-writing-methods/scripts/code_maps.json`
- [ ] `~/.hermes/skills/ultimate-thinking-and-writing-methods/scripts/modes_data.json`
- [ ] `~/.hermes/skills/ultimate-thinking-and-writing-methods/scripts/test_thinking_mode_selector.py`
- [ ] `~/.hermes/skills/ultimate-thinking-and-writing-methods/scripts/three_dimensional_comparison_matrix.xlsx`
- [ ] `~/.hermes/skills/ultimate-thinking-and-writing-methods/scripts/historical_figures_thinking_modes_library.md`

## H-* 代码分配规划

| 代码范围 | 类别 | 预计数量 |
|----------|------|----------|
| H-212 ~ H-231 | 理学/心学/考据/史学核心 | 20 |
| H-232 ~ H-236 | 史学/近代人物 | 5 |
| H-237 ~ H-241 | 军事/战略 | 5 |
| H-242 ~ H-249 | 女性 | 8 |
| H-250 ~ H-253 | 少数民族/边疆 | 4 |
| H-254 ~ H-256 | 文学/艺术 | 3 |
| **合计** | | **45** |

## 验收标准

| 指标 | 目标值 | 验收方式 |
|------|--------|----------|
| 总场景数 | 231 + 45 = **276** | `python3 tools/thinking_mode_selector.py -l` |
| 历史人物 | 211 + 45 = **256** | 统计 H-* 代码数量 |
| 思维模式 | 42 种全覆盖 | 检查 modes_data.json |
| 中英双语 | 100% 对齐 | 对比 scenarios_zh/en.json |
| 单测 | 24/24 全绿 | `pytest tools/test_thinking_mode_selector.py -v` |
| 技能目录同步验证通过 | - | CLI 验证 |

## 完成定义

所有上述验收项 ✅ 通过，技能目录同步验证通过，即视为 Phase 3 完成。

---

## 当前进度

✅ **已完成**:

- 历史人物审计文件更新 (211位)
- Phase2完成情况确认 (15位P0)
- Phase3候选人物名单规划 (45位P1/P2)

🔄 **待完成**:

- 深度调研报告
- 批量写入数据文件
- 审查报告
- 润色优化

**下一步**: serrano 深度调研 → elcano 批量写入 → espinosa 审查 → pigafetta 润色
