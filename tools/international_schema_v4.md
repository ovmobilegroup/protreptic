# 国际化 Schema v4.0

## 概述

支撑 Phase 8 全球扩展的完整数据模型，覆盖 12 文明圈、40+ 国家/地区、140+ 国际人物、15-20 个新思维模式 (M159-M178)。

---

## 15 核心字段 (必填)

| 字段名 | 类型 | 说明 | 示例 |
|--------|------|------|------|
| `code` | string | 唯一标识，格式 `{PREFIX}-{TOPIC}-{NNN}` | `SA-WAH-001` |
| `name_zh` | string | 中文姓名+专题 | `伊本·沙乌德：瓦哈比伊斯兰教法治理` |
| `name_en` | string | 英文姓名+专题 | `Ibn Saud: Wahhabi Islamic Governance` |
| `description_zh` | string | 中文描述 (200-500字) | ... |
| `description_en` | string | 英文描述 | ... |
| `reason_zh` | string | 选择理由 (中文) | ... |
| `reason_en` | string | 选择理由 (英文) | ... |
| `steps_zh` | array[string] | 执行步骤 5-6 步 (中文) | `["步骤1", "步骤2", ...]` |
| `steps_en` | array[string] | 执行步骤 (英文) | `["Step 1", "Step 2", ...]` |
| `expected_zh` | string | 预期成果 (中文) | ... |
| `expected_en` | string | 预期成果 (英文) | ... |
| `case_zh` | string | 实战案例 (中文) | ... |
| `case_en` | string | 实战案例 (英文) | ... |
| `modes` | array[int] | 思维模式 ID (1-178)，≥3个，≥1个新模式 | `[167, 149, 1, 153]` |

---

## 7 核心国际化字段 (必填，继承 v3)

| 字段名 | 类型 | 说明 | 示例 |
|--------|------|------|------|
| `nationality` | string | 国籍/文明归属 | `Saudi Arabia` |
| `civilization_sphere` | string | 文明圈 | `Islamic/Arab` |
| `time_period_standardized` | string | 标准化时期 | `1902-1953` |
| `wiki_id` | string | Wikipedia ID | `Ibn_Saud` |
| `primary_language` | string | 主要语言 | `Arabic` |
| `intellectual_tradition` | string | 思想传统 | `Wahhabi/Salafi` |
| `cross_cultural_impact` | string | 跨文化影响 | `Modern Islamic state formation` |

---

## 6 新增可选字段 (按需非空，Phase 8 新增)

| 字段名 | 类型 | 触发条件 | 说明 |
|--------|------|----------|------|
| `polar_region` | boolean/string | 极地/北极圈人物 | `Arctic` / `Subarctic` / `Antarctic` |
| `island_nation` | boolean/string | 岛屿国家人物 | `Pacific` / `Caribbean` / `Atlantic` |
| `nomadic_heritage` | boolean/string | 游牧传承人物 | `Mongol` / `Bedouin` / `Sami` / `Tuareg` |
| `oral_tradition` | string | 口述传统非空时 | 授权来源/文献引用，如 `社区授权: 马赛长老会议 2023` |
| `resource_curse_mitigation` | string | 资源诅咒缓解实践者 | 具体措施，如 `主权财富基金/透明化倡议/收益分配法` |
| `climate_adaptation` | string | 气候适应实践者 | 具体智慧，如 `海平面上升应对/永久冻土建筑/珊瑚礁修复` |

---

## 4 原有可选字段 (保留，按需填写)

| 字段名 | 类型 | 触发条件 |
|--------|------|----------|
| `spiritual_tradition` | string | 宗教/精神传统核心人物 |
| `colonial_history` | string | 殖民历史直接相关人物 |
| `diaspora_influence` | string | 侨民/流散影响力人物 |
| `indigenous_knowledge_system` | string | 原住民知识体系传承者 (需配合 oral_tradition 授权标注) |

---

## 验证规则 (零容忍)

1. **Schema 完整性**：100% 文件包含所有 15 核心字段 + 7 国际化字段
2. **双语完整性**：所有 `_zh` / `_en` 字段成对存在且非空
3. **模式覆盖**：`modes` 数组 ≥3 个 ID，且包含 ≥1 个 M159-M178 新模式
4. **代码格式**：严格遵循 `{PREFIX}-{TOPIC}-{NNN}`，三位数补全
5. **去重规则**：
   - 核心成就期归属地原则
   - 双重记录显式标注 (如 `dual_record: ["DE", "US"]`)
   - 侨民规则全量适用：侨居国为主、原籍国为辅
   - 原住民知识授权标注：`indigenous_knowledge_system` 非空时必须有 `oral_tradition` 授权来源
6. **前缀一致性**：`code` 前缀必须在 `code_prefix_registry_v3.csv` 中注册

---

## 文件命名规范

- 路径：`Protreptic/tools/json/{PREFIX}-{TOPIC}-{NNN}.json`
- 示例：`SA-WAH-001.json`、`CA-MUL-001.json`、`MN-NOM-001.json`
