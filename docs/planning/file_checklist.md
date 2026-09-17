# 文件修改清单

基于 `docs/monitoring/historical_figures_audit.md` 与 `docs/planning/candidates_shortlist.md`，新增 10 位历史人物需修改的文件清单。

---

## 需修改文件

| 文件 | 修改类型 | 说明 | 优先级 |
|------|----------|------|--------|
| `tools/scenarios_zh.json` | 新增 10 个 H-* 条目 | 追加到 JSON 尾部，H-* 代码按序分配 (H-WGW-160 至 H-WYN-169) | P0 |
| `tools/scenarios_en.json` | 同步新增英文版 | 字段结构对齐中文版，CODE_MAP_EN 同步 | P0 |
| `tools/modes_data.json` | 无需修改 | 42 个模式定义已完备，ID 1-42 连续 | - |
| `tools/code_maps.json` | 新增 CODE_MAP 映射 | CODE_MAP 与 CODE_MAP_EN 同步追加 10 条 | P0 |
| `tools/thinking_mode_selector.py` | 无需修改 | 选择器逻辑通用，自动读取 JSON | - |
| `docs/01-core-methodology/*.md` | 视新增模式决定 | 本次新增人物均映射既有 42 模式，无需新增模式文档 | - |

---

## 详细修改规格

### 1. tools/scenarios_zh.json
- 在 JSON 对象末尾追加 10 个键值对
- 键名: `H-WGW-160`, `H-FSN-161`, `H-JX-162`, `H-WXZ-163`, `H-ZH-164`, `H-XZ-165`, `H-LZC-166`, `H-HX-167`, `H-SJR-168`, `H-WYN-169`
- 值结构参考现有 H-* 条目，包含字段: `name`, `description`, `modes`, `reason`, `steps`, `expected`, `case`
- `modes` 数组引用 `modes_data.json` 中的 1-42 模式 ID

### 2. tools/scenarios_en.json
- 同步追加 10 个英文版条目
- 字段名、结构与中文版完全一致
- `name`, `description`, `reason`, `steps`, `expected`, `case` 为英文

### 3. tools/code_maps.json
- 在 `CODE_MAP` 与 `CODE_MAP_EN` 同步追加 10 条映射
- 格式: `"H-WGW-160": "王国维：人生三境界与双重证据法"` / `"H-WGW-160": "Wang Guowei: Three Realms & Double Evidence Method"`

### 4. 验收测试
```bash
cd <repo>
python3 tools/test_thinking_mode_selector.py
```
预期：全绿通过

---

## 创建的交付物文件

| 文件 | 状态 | 说明 |
|------|------|------|
| `docs/monitoring/historical_figures_audit.md` | ✅ 已创建 | 审计报告 v3：140 位历史人物、42 模式覆盖、低覆盖模式、10 位候选人 |
| `docs/planning/candidates_shortlist.md` | ✅ 已创建 | 10 位 P0 级候选人 + 详细画像 + H-* 代码分配 + 下游依赖 |
| `docs/planning/file_checklist.md` | ✅ 本文件 | 明确需修改文件列表 |

---

## 下游子代理任务分解建议

1. **数据录入代理** → `tools/scenarios_zh.json` + `tools/scenarios_en.json` 追加 10 条
2. **映射同步代理** → `tools/code_maps.json` 追加 CODE_MAP / CODE_MAP_EN
3. **验收测试代理** → 运行单测 `python3 tools/test_thinking_mode_selector.py` 全绿

各子代理依次执行，上游交付物作为下游输入上下文。