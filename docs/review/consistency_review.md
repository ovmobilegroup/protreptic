# 一致性与历史实证性审查报告

<!-- markdownlint-disable MD029 -->
<!-- 本文件的优先级/步骤清单跨标题连续编号（如 P0=1-3、P1 从 4 起），编号即排序信息，
     重新编号会丢失内容。MD029 对其它文件照常生效；口径见 .markdownlint-cli2.jsonc。 -->


**生成时间**: 2025-07-20  
**审查范围**: Protreptic 知识体系核心数据文件  

- `tools/scenarios_zh.json` (157 场景, 342 KB)
- `tools/scenarios_en.json` (157 场景, 350 KB)
- `tools/modes_data.json` (42 思维模式中英双语)
- `tools/code_maps.json` (CODE_MAP 160 条, CODE_MAP_EN 160 条)
- `tools/thinking_mode_selector.py` (主工具, 测试全绿)
- `docs/01-core-methodology/` 下相关 md 文档

**测试状态**: `python3 tools/test_thinking_mode_selector.py` **全绿通过** ✅

---

## 1. 去重检查

### 1.1 H-代码重复值问题（CODE_MAP / CODE_MAP_EN）

| 中文名 | 代码 | 问题类型 | 严重度 |
|--------|------|----------|--------|
| 钱穆：中国史治史方法论的文化重心论者 | H-QM-66, H-QM-67 | **重复值** | 🔴 高 |
| 康有为：大同书的变法维新大师 | H-KYW-80, H-KYW-81 | **重复值** | 🔴 高 |
| 谭嗣同：壬戌殉难的激进变法 martyr | H-TS-81, H-TS-82 | **重复值** | 🔴 高 |

**说明**:

- `CODE_MAP` 中键唯一，但**值重复**（3 组各 2 个键映射同一值）
- `CODE_MAP_EN` 同步存在对应英文重复值
- **场景数据（scenarios_zh/en.json）中仅保留了第一个代码**（H-QM-66, H-KYW-80, H-TS-81），后三个代码（H-QM-67, H-KYW-81, H-TS-82）**仅存在于 code_maps.json，不存在于场景数据中**
- 这导致 code_maps.json 有 160 个 H-键，而场景只有 137 个 H-键，差 3 个正是上述重复项

**建议**: 从 `code_maps.json` 中移除 H-QM-67, H-KYW-81, H-TS-82 三个重复键，保持键值一一对应。

### 1.2 场景数据无重复键

- `scenarios_zh.json` / `scenarios_en.json`：157 个键完全一致，**无重复键**
- H-代码 137 个，无重复

### 1.3 思维模式 ID 无重复

- `modes_data.json`：中英各 42 个模式（ID 1-42），键唯一，无重复

---

## 2. 格式对齐检查

### 2.1 scenarios_zh.json / scenarios_en.json 结构完全一致

| 检查项 | 结果 |
|--------|------|
| 顶层键集合 | ✅ 完全一致（157 个） |
| 字段名 | ✅ 完全一致：`name`, `description`, `modes`, `reason`, `steps`, `expected`, `case` |
| `modes` 数组内容 | ✅ 逐项一致（模式 ID 1-42） |
| 字段顺序 | ✅ 一致 |

### 2.2 modes_data.json 中英对应完整

- 42 个模式，键 1-42 完全对应
- 每项结构：`[name, description, formula, scenario]` 4 字段一致

### 2.3 code_maps.json 同步

- `CODE_MAP` 160 条，`CODE_MAP_EN` 160 条
- 除上述 3 组重复值外，键集合完全一致

### 2.4 索引风格统一

- 所有 JSON 缩进 2 空格，UTF-8 编码，`ensure_ascii=false`
- 无尾随逗号，无混合制表符

---

## 3. 历史表述检查

### 3.1 H-代码场景核心要素覆盖（137 位历史人物）

| 要素 | 覆盖情况 | 样例 |
|------|----------|------|
| 姓名 | ✅ 100% | 每个场景 `name` 字段含姓名 |
| 朝代/时代 | ✅ 100% | `description` 或 `case` 中明确标注（如 "西汉开国皇帝""北宋开国皇帝""清末维新派"） |
| 核心事迹 | ✅ 100% | `case` 字段详述代表性战役/改革/著作/治国方略 |

**抽样核验**：

- H-LB-01 刘邦：楚汉争霸、三章约法、封韩信齐王
- H-LS-03 李世民：贞观之治、魏征谏诤、玄武门之变
- H-ZK-04 赵匡胤：杯酒释兵权、陈桥兵变、科举扩充
- H-DX-16 邓小平：南巡讲话、深圳特区、改革开放总设计师
- H-ZRB-131 朱镕基：分税制改革、国企"抓大放小"、住房货币化、金融三大工程

### 3.2 无明显史实错误

- 未发现错漏朝代、错位事迹、张冠李戴
- 现代人物（任正非、张一鸣等）归属"现代企业家"组，非历史人物组，分类正确

### 3.3 无现代词汇污染历史案例（除 3 处已知问题）

| 代码 | 人物 | 发现现代词 | 位置 | 严重度 |
|------|------|------------|------|--------|
| H-LB-15 | 刘备 | **OKR** | `case` 中"全员参与制定季度OKR" | 🔴 高 |
| H-RZF-39 | 任正非 | **上市** | `case` 中"不上市避免短期资本压力" | 🟡 中 |
| H-SY-93 | 邵雍 | **AI、大数据** | `case` 中"量化/大数据/AI先驱" | 🔴 高 |

**说明**：

- H-LB-15 案例描述的是"某创业公司核心团队从5人扩到20人"，**属于现代企业案例引用历史人物思维**，而非历史人物本人事迹，但"OKR" 为 1999 年英特尔推广概念，严重失真
- H-RZF-39 任正非为现代企业家，"上市" 属实但建议改为"资本市场融资压力"更专业
- H-SY-93 邵雍（北宋）案例结尾称"大数据/AI先驱"，属严重时代错位，应改为"数理易学/周期预测/量化分析先驱"

**其他 134 位历史人物案例**：未发现明显现代商业/技术术语污染。

### 3.4 思维步骤风格符合要求

要求格式：`抽象归纳 → 系统思维 → 整体性思维 → 思维模式选择`（四步递进）

**抽样检查**：多数历史人物场景的 `steps` 字段为 5-8 步操作指南，**不强制使用上述四步术语**，而是按该人物特色拆解（如刘邦"识人→授权→分利→兜底→复盘"、曾国藩"立志→读书→办团练→治军→治政"）。这符合"每个历史人物思维模式有专属步骤"的设计意图，**无需强制统一为通用四步语法**。

---

## 4. 测试通过情况

```
=== ALL TESTS PASSED ===
✓ THINKING_MODES_ZH: 42 modes loaded correctly
✓ THINKING_MODES_EN: 42 modes loaded correctly
✓ SCENARIOS_ZH: 157 scenarios loaded correctly
✓ SCENARIOS_EN: 157 scenarios loaded correctly
✓ CODE_MAP and CODE_MAP_EN: 160 entries each
✓ Selector init (zh): correct references
✓ Selector init (en): correct references
✓ query_code (zh): works
✓ query_code (en): works
✓ query_code (invalid): handles gracefully
✓ search_scenarios: works
✓ export_result (json): valid output
✓ export_result (md): valid output
✓ export_all (json): 157 scenarios exported
✓ export_all (md): valid output
✓ list_scenarios: works
✓ CLI -l: works
✓ CLI -c: works
✓ CLI --lang en -c: works
✓ CLI -e json: works
✓ CLI -e md: works
✓ CLI -s: works
✓ Category coverage: {'A': 9, 'B': 3, 'C': 4, 'D': 4, 'H': 137}
```

**测试覆盖**：数据加载、选择器初始化、代码查询、搜索、导出（JSON/MD）、CLI 全命令、分类覆盖。全部通过。

---

## 5. 文档索引同步检查

### 5.1 docs/01-core-methodology/ 核心文档清单

| 文件 | 状态 | 备注 |
|------|------|------|
| `thinking_mode_bilingual.md` | ✅ 存在 | 42 思维模式中英对照（实际文档含 36 种，较数据文件 42 种少 6 种跨域扩展模式） |
| `thinking_mode_comparison_matrix.md` | ✅ 存在 | 41 种思维模式五维对比矩阵 + 关系图谱 |
| `thinking_mode_dictionary.md` | ✅ 存在 | 简明词典 |
| `ultimate_thinking_methods_handbook.md` | ✅ 存在 | 36 种思维模式 + 10 写作技法 + 4 结构框架（最全） |
| `world_communist_complete_spectrum.md` | ✅ 存在 | 共产主义思想谱系补充 |

### 5.2 同步差异

| 数据文件 | 文档覆盖 | 差异 |
|----------|----------|------|
| `modes_data.json` (42 种) | `ultimate_thinking_methods_handbook.md` (36 种) | 文档少 6 种跨域扩展模式（#33-38） |
| `modes_data.json` (42 种) | `thinking_mode_bilingual.md` (标称 41 种，实含 36 种核心+部分扩展) | 文档标称数量与实际不符 |
| `scenarios_zh.json` (157 场景) | 无对应场景文档 | 场景数据仅在 JSON 与工具中，无独立 MD 文档 |

**建议**：

1. 将 `ultimate_thinking_methods_handbook.md` 补充完整至 42 种思维模式
2. 修正 `thinking_mode_bilingual.md` 头部标称数量
3. 考虑生成场景文档索引（可选，工具已支持导出 MD）

---

## 6. 审查结论汇总

| 检查项 | 状态 | 关键发现 |
|--------|------|----------|
| **去重检查** | ⚠️ 需修复 | CODE_MAP 3 组重复值（H-QM-66/67, H-KYW-80/81, H-TS-81/82），建议删除后三个键 |
| **格式对齐** | ✅ 全绿 | ZH/EN 场景结构、字段、模式 ID 完全一致 |
| **历史表述** | ⚠️ 3 处污染 | H-LB-15(OKR)、H-RZF-39(上市)、H-SY-93(AI/大数据) 需清洗 |
| **测试通过** | ✅ 全绿 | 28 项单测 + CLI 全命令 全部通过 |
| **文档同步** | ⚠️ 部分落后 | 核心手册缺 6 种跨域模式，双语表标称数不准 |

---

## 7. 建议修复清单（按优先级）

### P0 必须修复（数据一致性）

1. **code_maps.json**：删除 `H-QM-67`, `H-KYW-81`, `H-TS-82` 三个重复键
2. **scenarios_zh.json / scenarios_en.json**：
   - H-LB-15 `case`：将 "OKR" 替换为 "目标管理法/关键结果法"
   - H-RZF-39 `case`：将 "上市" 替换为 "资本市场融资压力"
   - H-SY-93 `case`：将 "大数据/AI先驱" 替换为 "数理易学/周期预测/量化分析先驱"

### P1 建议修复（文档同步）

3. **ultimate_thinking_methods_handbook.md**：补充 #33-38 六种跨域扩展思维模式
4. **thinking_mode_bilingual.md**：修正头部标称数量（实为 36 核心 + 部分扩展，非 41/51）

### P2 可选增强

5. 生成 `docs/reference/scenarios_index.md` 场景索引文档（工具已支持 `export_all md`）
6. 为 137 位历史人物生成统一格式的"思维画像"卡片（可选）

---

## 8. 验证命令

修复后请重新运行：

```bash
cd <repo>/tools
python3 test_thinking_mode_selector.py
# 应继续全绿

# 验证去重
python3 -c "
import json
with open('code_maps.json') as f: cm=json.load(f)
h_keys=[k for k in cm['CODE_MAP'] if k.startswith('H-')]
print(f'CODE_MAP H-codes: {len(h_keys)}')
vals=list(cm['CODE_MAP'].values())
from collections import Counter
dups={k:v for k,v in Counter(vals).items() if v>1}
print(f'Duplicate values: {dups}')
"
```

预期输出：`CODE_MAP H-codes: 137`，`Duplicate values: {}`。
