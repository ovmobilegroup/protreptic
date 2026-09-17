# Phase 3 验收标准

**生成时间**: 2026-08-13
**当前状态**: 规划完成

## 核心指标验收

| 指标 | 目标值 | 验收方式 |
|------|--------|----------|
| 总场景数 | 231 + 45 = **276** | `python3 tools/thinking_mode_selector.py -l` |
| 历史人物 | 211 + 45 = **256** | 统计 H-* 代码数量 |
| 思维模式 | 42 种全覆盖 | 检查 modes_data.json |
| 中英双语 | 100% 对齐 | 对比 scenarios_zh/en.json |
| 单测 | 24/24 全绿 | `pytest tools/test_thinking_mode_selector.py -v` |

## 文件完整性验收

### 核心数据文件
- [ ] `tools/scenarios_zh.json` - 276 条记录，含 256 个 H-*
- [ ] `tools/scenarios_en.json` - 276 条记录，完全对齐
- [ ] `tools/code_maps.json` - CODE_MAP/CODE_MAP_EN 各 276 条
- [ ] `tools/modes_data.json` - 42 种模式，中英双语

### 文档文件
- [ ] `docs/historical_figures_thinking_modes_library.md` - 完整档案库
- [ ] `tools/three_dimensional_comparison_matrix.xlsx` - 5 工作表，256 位历史人物

### 规划/研究文档
- [x] `docs/planning/phase3_candidates.md` - 45 位候选人名单 ✓
- [ ] `docs/research/phase3_detailed_research.md` - 45 位深度调研
- [x] `docs/planning/phase3_file_checklist.md` - 本文件 ✓
- [ ] `docs/review/phase3_review_report.md` - 审查报告
- [ ] `docs/terminology/phase3_terminology.md` - 术语对照表

### 测试文件
- [ ] `tools/test_thinking_mode_selector.py` - 断言更新为 276/256

### 技能目录同步
- [ ] `~/.hermes/skills/ultimate-thinking-and-writing-methods/scripts/` 全套文件同步
- [ ] 技能目录 CLI 验证通过

## 功能冒烟测试清单

```bash
# 1. 列表查询
python3 tools/thinking_mode_selector.py -l

# 2. 单个人物双语查询（抽样 5 位新增）
python3 tools/thinking_mode_selector.py -c H-ZDY-212 --lang zh
python3 tools/thinking_mode_selector.py -c H-ZDY-212 --lang en
python3 tools/thinking_mode_selector.py -c H-EC-213 --lang zh
python3 tools/thinking_mode_selector.py -c H-EC-213 --lang en
python3 tools/thinking_mode_selector.py -c H-ZX-214 --lang zh

# 3. 关键词搜索（覆盖新增核心概念）
python3 tools/thinking_mode_selector.py -s 太极图说
python3 tools/thinking_mode_selector.py -s 致良知
python3 tools/thinking_mode_selector.py -s 明夷待访录
python3 tools/thinking_mode_selector.py -s 历史循环
python3 tools/thinking_mode_selector.py -s 非攻

# 4. 完整测试套件
pytest tools/test_thinking_mode_selector.py -v

# 5. 导出功能
python3 tools/thinking_mode_selector.py -e json -o /tmp/phase3_export.json
python3 tools/thinking_mode_selector.py -e md -o /tmp/phase3_export.md
```

## 审查报告要求

`docs/review/phase3_review_report.md` 必须包含：

1. **去重检查结果** - 无 H-* 代码冲突、无姓名重复
2. **格式对齐检查** - 字段/顺序/缩进/引号/中英对应
3. **史实准确性** - 时代/身份/事迹/步骤真实源于史料
4. **模式映射合理性** - 每人物主/辅模式精准对应 42 种定义
5. **测试结果** - 全绿截图/日志
6. **遗留问题/技术债** - 如有

## 当前进度

✅ **已完成规划**:
- 历史人物审计文件更新 (211位)
- Phase2完成情况确认 (15位P0)
- Phase3候选人物名单规划 (45位P1/P2)
- 文档框架搭建完成

🔄 **待执行**:
- 深度调研报告撰写
- 批量写入数据文件
- 审查报告
- 润色优化

## 完成定义

所有上述验收项 ✅ 通过，技能目录同步验证通过，即视为 Phase 3 完成。

---

## Phase 3 执行计划

1. **serrano** - 深度调研：45 位候选人物的详细思维模式分析
2. **elcano** - 批量写入：将调研结果写入 JSON 数据文件
3. **espinosa** - 审查：质量检查、去重验证、格式对齐
4. **pigafetta** - 润色：优化表达、完善细节、最终校验

**预计完成时间**: 2026-08-13