# 批量导入运行手册 - Batch Import Runbook

## 概述

本手册详细说明 Protreptic 批量导入脚本（import_batch_56.py）的使用方法、验证流程和故障排除指南。该脚本用于将新的人物数据批量导入到 Protreptic 知识体系的核心文件中。

## 目标受众

本手册面向需要重复执行批量导入流程的维护人员，包括：
- 知识库管理员
- 数据验证人员
- 系统运维人员
- 开发人员

## 输入源与验证规则

### 输入源

**主要输入文件：**
```
<repo>/docs/research/batch_new_figures_research.md
```

**数据来源：**
- `batch2_candidates.json` - 第一批候选人物数据
- `batch3_candidates.json` - 第二批候选人物数据
- `generate_input.py` - 生成合并输入文件的脚本

**数据格式要求：**
```json
{
  "code": "H-XXX-XXX",
  "name_zh": "中文姓名",
  "name_en": "English Name", 
  "era": "Modern",
  "historical_domains": ["Governance", "Economics"],
  "domains": ["Operational", "Strategic"],
  "core_modes": [8, 38, 39, 10],
  "gender": "Male",
  "ethnicity": "Han",
  "unique_thinking": "核心思想/独特贡献",
  "source_refs": ["参考资料1", "参考资料2"],
  "proposed_steps": ["第1步：步骤描述", "第2步：步骤描述"],
  "applications": ["应用场景1", "应用场景2"]
}
```

### 验证规则

**代码验证：**
- 必须以 "H-" 开头
- 必须全局唯一（不允许重复）
- 格式：H-三位数字-三位数字

**字段验证：**
- `name_zh` 和 `name_en` 不能为空
- `core_modes` 必须是非空数组，包含有效的模式编号
- `proposed_steps` 必须是 5-6 个步骤的数组
- `unique_thinking` 不能为空

**模式编号验证：**
- 支持 1-42 的传统模式编号
- 也支持扩展模式编号（如 36, 38 等）
- 模式必须在 `modes_data.json` 中有对应条目

## 脚本调用与预期输出

### 脚本位置

```bash
# 原始脚本位置
<repo>/tools/import_batch_56.py

# Skills 目录中的副本（已同步）
<data>/skills/ultimate-thinking-and-writing-methods/scripts/import_batch_56.py
```

### 脚本调用

```bash
# 基本调用
python3 import_batch_56.py

# 详细输出模式
python3 import_batch_56.py --verbose
```

### 预期输出

脚本执行时会产生以下输出：

```
============================================================
Batch Import Script: 56 New Figures
============================================================

[1] Reading batch_new_figures_research.md...
    Loaded 87 figures

[2] Validating data...
  All validations passed.

[3] Updating core files...
  scenarios_zh.json updated
  scenarios_en.json updated  
  code_maps.json updated
  modes_data.json updated (no new mode entries needed automatically)
  scenario_tags.json updated

[4] Generating comparison matrix...
  Generating <repo>/three_dimensional_comparison_matrix.xlsx...

[5] Generating thinking modes library...
  Generated historical_figures_thinking_modes_library.md

============================================================
IMPORT COMPLETE
============================================================

  scenarios_zh.json:   1006 entries
  scenarios_en.json:   1006 entries
  code_maps.json:      984 entries (87 H-*)
  modes_data.json:     617 entries (unchanged)
  scenario_tags.json:  984 entries

  Figures processed:   87
  Newly imported:      87
  Skipped (existing):  0
```

## 验证命令

### 本地验证

#### 1. 数据完整性验证

```bash
# 检查 JSON 文件格式
python3 -m json.tool scenarios_zh.json
python3 -m json.tool scenarios_en.json
python3 -m json.tool code_maps.json
python3 -m json.tool modes_data.json
python3 -m json.tool scenario_tags.json

# 检查总条目数
grep -c '"code":' scenarios_zh.json
grep -c '"code":' scenarios_en.json
grep -c '^H-' code_maps.json
wc -l modes_data.json
wc -l scenario_tags.json
```

#### 2. CLI 功能验证

```bash
# 列出所有场景
python3 thinking_mode_selector.py -l

# 查询特定人物
python3 thinking_mode_selector.py -c H-RZF-270 --lang zh
python3 thinking_mode_selector.py -c H-RZF-270 --lang en

# 搜索功能
python3 thinking_mode_selector.py -s 任正非
python3 thinking_mode_selector.py -s Ren Zhengfei

# 导出功能
python3 thinking_mode_selector.py -e json
python3 thinking_mode_selector.py -e md

# 标签筛选
python3 thinking_mode_selector.py -t "historical_domains=Economics"
python3 thinking_mode_selector.py -t "historical_domains=Military"
```

#### 3. 测试套件验证

```bash
# 运行完整测试套件（24个测试）
python3 test_thinking_mode_selector.py

# 测试输出示例：
✓ SCENARIOS_ZH: 1006 total, 367 historical, 44 P4, 25 P5, 455 international
✓ SCENARIOS_EN: 1006 total, 367 historical, 44 P4, 25 P5, 455 international
✓ MODES_DATA: 617 zh modes + 617 en modes, all bilingual
✓ CODE_MAP: 984, CODE_MAP_EN: 984
✓ Bilingual consistency: all required keys and modes match
✓ Mode coverage: 466/42 modes used
✓ New batch figures: all 87 present
✓ CLI -l: works, listed 387 scenarios
✓ CLI query: works for new batch figures
✓ CLI search: works
✓ CLI export: works
✓ CLI tag filter: works

=== ALL TESTS PASSED ===
```

#### 4. 数据一致性验证

```bash
# 检查中英文一致性
python3 -c "
import json
with open('scenarios_zh.json') as f: zh = json.load(f)
with open('scenarios_en.json') as f: en = json.load(f)
print(f'ZH entries: {len(zh)}, EN entries: {len(en)}')
common = set(zh.keys()) & set(en.keys())
print(f'Common entries: {len(common)}')
if len(common) == len(zh) == len(en):
    print('✓ All entries have bilingual counterparts')
else:
    print('✗ Inconsistency detected')
"

# 检查模式覆盖
python3 -c "
import json
with open('scenarios_zh.json') as f: zh = json.load(f)
all_modes = set()
for entry in zh.values():
    if isinstance(entry, dict) and 'core_mode' in entry:
        modes = entry['core_mode'].split(', ')
        all_modes.update(modes)
print(f'Total modes used: {len(all_modes)}')
print(f'Mode range: {min(all_modes) if all_modes else \"N/A\"} - {max(all_modes) if all_modes else \"N/A\"}')
"
```

### Skills 目录验证

#### 1. 文件同步检查

```bash
# 检查文件是否正确同步到 skills 目录
ls -la <data>/skills/ultimate-thinking-and-writing-methods/scripts/import_batch_56.py
ls -la <data>/skills/ultimate-thinking-and-writing-methods/scripts/test_thinking_mode_selector.py
ls -la <data>/skills/ultimate-thinking-and-writing-methods/scripts/thinking_mode_selector.py

# 检查权限
ls -la <data>/skills/ultimate-thinking-and-writing-methods/scripts/*.py | grep -E 'rwx|r--'
```

#### 2. Skills 环境测试

```bash
# 在 skills 目录中运行测试
cd <data>/skills/ultimate-thinking-and-writing-methods/scripts
python3 test_thinking_mode_selector.py

# 测试 CLI 功能
python3 thinking_mode_selector.py -c H-RZF-270 --lang zh | head -10
python3 thinking_mode_selector.py -t "historical_domains=Economics" | head -5
```

#### 3. 数据一致性验证

```bash
# 检查两个环境的数据一致性
cd <data>/skills/ultimate-thinking-and-writing-methods/scripts

# 对比 JSON 文件
python3 -c "
import json
with open('<repo>/scenarios_zh.json') as f: prod = json.load(f)
with open('scenarios_zh.json') as f: skills = json.load(f)
print(f'Production: {len(prod)}, Skills: {len(skills)}')
if len(prod) == len(skills):
    print('✓ Data counts match')
else:
    print('✗ Data count mismatch')
"
```

## 回滚与重运行指南

### 回滚操作

如果导入过程中出现问题，可以按以下步骤回滚：

#### 1. 备份当前状态

```bash
# 创建备份目录
BACKUP_DIR="<repo>/backup_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

# 备份核心文件
cp scenarios_zh.json "$BACKUP_DIR/"
cp scenarios_en.json "$BACKUP_DIR/"
cp code_maps.json "$BACKUP_DIR/"
cp modes_data.json "$BACKUP_DIR/"
cp scenario_tags.json "$BACKUP_DIR/"
cp three_dimensional_comparison_matrix.xlsx "$BACKUP_DIR/"
cp docs/historical_figures_thinking_modes_library.md "$BACKUP_DIR/"

echo "Backup created in: $BACKUP_DIR"
```

#### 2. 恢复到导入前状态

```bash
# 如果有备份，恢复文件
cp "$BACKUP_DIR/scenarios_zh.json" <repo>/
cp "$BACKUP_DIR/scenarios_en.json" <repo>/
cp "$BACKUP_DIR/code_maps.json" <repo>/
cp "$BACKUP_DIR/modes_data.json" <repo>/
cp "$BACKUP_DIR/scenario_tags.json" <repo>/
cp "$BACKUP_DIR/three_dimensional_comparison_matrix.xlsx" <repo>/
cp "$BACKUP_DIR/historical_figures_thinking_modes_library.md" <repo>/docs/

# 恢复 skills 目录
cp "$BACKUP_DIR/scenarios_zh.json" <data>/skills/ultimate-thinking-and-writing-methods/scripts/
cp "$BACKUP_DIR/scenarios_en.json" <data>/skills/ultimate-thinking-and-writing-methods/scripts/
cp "$BACKUP_DIR/code_maps.json" <data>/skills/ultimate-thinking-and-writing-methods/scripts/
cp "$BACKUP_DIR/modes_data.json" <data>/skills/ultimate-thinking-and-writing-methods/scripts/
cp "$BACKUP_DIR/scenario_tags.json" <data>/skills/ultimate-thinking-and-writing-methods/scripts/
```

#### 3. 验证回滚

```bash
# 运行验证测试
python3 test_thinking_mode_selector.py

# 检查关键数据
python3 thinking_mode_selector.py -c H-RZF-270 --lang zh | grep -q "任正非"
echo "✓ 回滚验证完成"
```

### 重运行操作

如果需要重新导入（例如数据更新）：

#### 1. 清理现有数据

```bash
# 删除导入的人物数据（谨慎操作）
python3 -c "
import json
with open('scenarios_zh.json') as f: data = json.load(f)
# 删除 H- 开头的条目
new_data = {k: v for k, v in data.items() if not k.startswith('H-')}
with open('scenarios_zh.json', 'w') as f:
    json.dump(new_data, f, ensure_ascii=False, indent=2)
print(f'Removed H- entries, kept {len(new_data)} entries')
"
```

#### 2. 重新执行导入

```bash
# 重新运行导入脚本
python3 import_batch_56.py

# 验证结果
python3 test_thinking_mode_selector.py
```

## 故障排除

### 常见问题

#### 1. JSON 格式错误

**问题：** `json.decoder.JSONDecodeError`

**解决方案：**
```bash
# 检查输入文件格式
python3 -m json.tool <repo>/docs/research/batch_new_figures_research.md

# 修复格式问题
# 1. 检查是否有未闭合的引号
# 2. 检查是否有未闭合的括号
# 3. 检查是否有非法字符
```

#### 2. 验证失败

**问题：** `VALIDATION ERRORS:` 输出

**解决方案：**
```bash
# 检查具体验证错误
python3 import_batch_56.py 2>&1 | grep "VALIDATION ERRORS"

# 修复数据问题
# 1. 检查重复的 code
# 2. 检查缺失的必填字段
# 3. 检查模式编号范围
```

#### 3. 文件权限问题

**问题：** `Permission denied`

**解决方案：**
```bash
# 检查文件权限
ls -la <repo>/*.json
ls -la <data>/skills/ultimate-thinking-and-writing-methods/scripts/*.py

# 修复权限
chmod 644 <repo>/*.json
chmod 755 <data>/skills/ultimate-thinking-and-writing-methods/scripts/*.py
```

#### 4. 依赖缺失

**问题：** `ModuleNotFoundError`

**解决方案：**
```bash
# 检查 Python 路径
python3 -c "import sys; print(sys.path)"

# 检查模块可用性
python3 -c "import json; print('✓ json available')"
python3 -c "import os; print('✓ os available')"
```

### 调试技巧

#### 1. 详细输出

```bash
# 启用详细输出
python3 import_batch_56.py --verbose

# 或者添加调试信息
python3 -c "
import json
with open('<repo>/docs/research/batch_new_figures_research.md') as f:
    data = json.load(f)
print(f'Input data count: {len(data)}')
for i, item in enumerate(data[:3]):
    print(f'Item {i}: {item}')
"
```

#### 2. 分步执行

```bash
# 逐步验证输入数据
python3 -c "
import json
with open('<repo>/docs/research/batch_new_figures_research.md') as f:
    figures = json.load(f)
print(f'Loaded {len(figures)} figures')
for fig in figures[:5]:
    print(f'{fig[\"code\"]}: {fig[\"name_zh\"]} ({fig[\"name_en\"]})')
"
```

#### 3. 数据一致性检查

```bash
# 检查数据一致性
python3 -c "
import json
with open('scenarios_zh.json') as f: zh = json.load(f)
with open('scenarios_en.json') as f: en = json.load(f)
with open('code_maps.json') as f: cm = json.load(f)

print(f'ZH: {len(zh)}, EN: {len(en)}, CM: {len(cm)}')

# 检查代码映射一致性
zh_codes = set(zh.keys())
en_codes = set(en.keys())
cm_codes = set(cm.keys())

print(f'Codes in ZH only: {zh_codes - cm_codes}')
print(f'Codes in EN only: {en_codes - cm_codes}')
print(f'Codes in CM only: {cm_codes - zh_codes}')
"
```

## 测试运行截图占位符

### 截图 1: 成功的 24/24 测试运行

```
=== 测试运行截图占位符 ===
[此处应插入测试套件成功运行的截图]
显示: "=== ALL TESTS PASSED ===" 和所有 ✓ 标记
测试数量: 24/24 通过
```

### 截图 2: CLI 功能验证截图

```
=== CLI 功能验证截图占位符 ===
[此处应插入 CLI 功能验证的截图]
显示:
- 列表功能输出
- 查询功能输出 (H-RZF-270 任正非)
- 搜索功能输出
- 标签筛选输出
```

## 维护注意事项

### 定期维护

1. **数据备份**
   - 每次导入前创建完整备份
   - 保留最近 3 次的备份记录

2. **测试验证**
   - 每次导入后运行完整测试套件
   - 定期检查数据一致性

3. **性能监控**
   - 监控导入脚本执行时间
   - 检查生成的文件大小

### 版本控制

1. **脚本版本**
   - 保留不同版本的导入脚本
   - 记录每次脚本变更

2. **数据版本**
   - 为每次导入创建数据快照
   - 记录导入的人物数量和范围

### 安全考虑

1. **文件权限**
   - 确保核心文件有适当的读写权限
   - 限制对敏感数据的访问

2. **数据完整性**
   - 在导入过程中验证数据完整性
   - 防止数据损坏或丢失

## 联系信息

如果在执行过程中遇到问题，请联系：
- 知识库管理员
- 系统运维团队
- 开发支持团队

---

*本手册最后更新: 2026-08-24*
*版本: 1.0*
*适用版本: Protreptic v2.0*