# Protreptic 结构变更指南 v6.0

## 概述
记录 Phase 13-16 全球补全结构变更，为 elcano、serrano、马里亚诺后续批量同步做准备。

---

## 文件清单 (5 个结构文档)

| 文件 | 描述 | 版本 |
|------|------|------|
| `international_schema_v6.md` | 数据模型 Schema，15 核心 + 8 国际化 + 16 可选字段 | v6 |
| `code_prefix_registry_v5.csv` | 95+ 新前缀注册 (AM/AZ/CY/GE/GT/MD/ME/MN/MY/NI/OM/SV/XK/YE 等) | v5 |
| `batch_plan_v4.md` | 12 批次推进计划 (Batch 17-28)，96 位人物 | v4 |
| `modes_expansion_v4.md` | 95 个新思维模式 (M262-M356) | v4 |
| `quality_checklist_v4.md` | 质检清单，22+ 检查项 | v4 |

### 补充参考

| 文件 | 描述 |
|------|------|
| `code_maps_v6.md` | CODE_MAP 和 CODE_MAP_EN 更新说明 |
| `scenarios_v6.md` | scenarios_zh/en.json 和 scenario_tags.json 更新说明 |

---

## 数据模型变更 (v5 → v6)

### 新增核心字段
| 字段 | 类型 | 说明 |
|------|------|------|
| `legacy_type` | string | 遗产类型：cultural/political/scientific/artistic/military |

### 新增可选字段
| 字段 | 类型 | 说明 |
|------|------|------|
| `regional_integration` | string | 区域一体化：EU/ASEAN/AU/MERCOSUR/CIS/SCO/GCC/CARICOM/ECOWAS/SAARC/无 |
| `conflict_resolution_mechanism` | string | 冲突解决：和解委员会/真相委员会/过渡正义/联邦主义/权力分享/国际仲裁/谈判调解/抵抗革命 |

### 可选字段枚举扩展
- `education_tradition`: 新增 `东正教`, `中亚`, `高加索`, `东南亚`
- `legal_system`: 文明圈映射扩展 (Eastern Orthodox, Post-Soviet, Pacific, etc.)

---

## 批次推进计划 (v4)

### 12 个批次概览
| Batch | 主题 | 前缀 | 人物数 | 新模式 |
|-------|------|------|--------|--------|
| 17 | 高加索核心 | GE/AM/AZ/MD | 8 | M262-M269 |
| 18 | 中亚五国 | KZ/UZ/KG/TJ/TM | 8 | M270-M277 |
| 19 | 蒙古/东亚 | MN/VN/LA/KH/TH/MM | 8 | M278-M285 |
| 20 | 东南亚群岛 | MY/ID/PH/SG/BN/TL | 8 | M286-M293 |
| 21 | 南亚小国 | NP/BT/LK/MV/YE/OM/KW | 8 | M294-M301 |
| 22 | 海湾核心 | SA/BH/QA/AE/JO/LB/SY | 8 | M302-M309 |
| 23 | 西非深层 | NG/KE/TZ/ZW/ZA/ET/GH | 8 | M310-M317 |
| 24 | 非洲法语区 | SN/CI/CO/EC/BO/PY/UY/AR | 8 | M318-M325 |
| 25 | 拉美补全 | CL/MX/GT/SV/NI/CU/HT/DO | 8 | M326-M333 |
| 26 | 北美补全 | CA/US/JM/GL/SA | 8 | M334-M341 |
| 27 | 战争史补全 | TR/IQ/SY/NG/ZA/ET/CO/ID | 8 | M342-M349 |
| 28 | 边缘文明补全 | IQ/NG/KE/TZ/ZW/ZA/ET/GH | 8 | M350-M357 |

> **注意**: Batch 26-28 中存在 95+ 新前缀，但 96 位人物中有部分重复前缀 (如 IQ/NG/KE/TZ/ZW/ZA/ET/GH)
> 这些重复旨在为 elcano 等研究者提供补全选项。最终人物数保持在 96。

### 依赖链
```
serrano → albo架构(Schema v6/前缀v5/模式v4/质检v4)
    → Batch 17 (GE/AM/AZ/MD) → Batch 18 (KZ/UZ/KG/TJ/TM) → ... → Batch 28
```

---

## 新模式定义 (v4)

### 领域分布
| 领域 | 模式范围 | 数量 |
|------|----------|------|
| 高加索/东正教 | M262-M273 | 12 |
| 东南亚/南海 | M274-M285 | 12 |
| 湖顿/南亚 | M286-M301 | 16 |
| 非洲/西撒哈拉 | M310-M325 | 16 |
| 拉美/中美洲 | M326-M341 | 16 |
| 北美/极地 | M334-M341 | 8 |
| 战争史/中东 | M342-M350 | 9 |
| 边缘文明 | M350-M357 | 8 |

### 模式元数据要求
每个新模式必须包含:
1. **ID** (M262-M356)
2. **名称** (中英文双语)
3. **定义** (200-300 字)
4. **步骤** (5-6 个可执行步骤)
5. **应用场景**
6. **关联人物**

---

## 质检清单 (v4)

### 新增检查项
- `legacy_type` 字段逻辑一致性校验
- `regional_integration` 填写时，区域与 nationality 匹配
- `conflict_resolution_mechanism` 填写时，应与人物历史活动一致
- 新模式 M262-M356 覆盖验证 (≥1 个新模式 per 人物)
- 95+ 新前缀全部注册在 code_prefix_registry_v5.csv

### 校验脚本
```bash
# Schema 校验
python3 check_schema_v6.py --input <json_file>

# 质检清单执行
python3 quality_checklist_v4.py --all --verbose
```

---

## 实施计划

### 阶段 1: 结构文档产出 (已完成)
- [x] international_schema_v6.md
- [x] code_prefix_registry_v5.csv (95 个新前缀)
- [x] batch_plan_v4.md (12 批次, 96 人)
- [x] modes_expansion_v4.md (95 个新模式 M262-M356)
- [x] quality_checklist_v4.md (22+ 检查项)
- [x] code_maps_v6.md (更新说明)
- [x] scenarios_v6.md (更新说明)

### 阶段 2: 交付给 elcano
- elcano 读取 batch_plan_v4.md，逐批次执行 96 位人物研究
- elcano 生成 96 个人物 JSON 文件
- elcano 更新 scenarios_zh/en.json, scenario_tags.json, code_maps.json

### 阶段 3: 验收
- 5 个结构文档审阅通过
- 96 位人物 JSON 通过 Schema v6 校验
- 4 主数据文件同步完成
- 95+ 前缀全部注册
- 95 个新模式 (M262-M356) 定义完整