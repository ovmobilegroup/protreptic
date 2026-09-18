# Phase 9-12 质量检查单 v3.0

## 概述

支撑 Phase 9-12 全球补全扩展 (144 人、90+ 前缀、M215-M265 51 新模式) 的全维度质量红线。
继承 Phase 8 质检单 v3.0，扩展 8 个新增 Schema v5 可选字段校验。

---

## 核心红线 (零容忍，自动化校验)

### 1. Schema 完整性

- [ ] 100% JSON 文件包含 15 核心字段 (`code`, `name_zh/en`, `description_zh/en`, `reason_zh/en`, `steps_zh/en`, `expected_zh/en`, `case_zh/en`, `modes`)
- [ ] 100% JSON 文件包含 7 核心国际化字段 (`nationality`, `civilization_sphere`, `time_period_standardized`, `wiki_id`, `primary_language`, `intellectual_tradition`, `cross_cultural_impact`)
- [ ] **NEW v5**: 8 个新增可选字段按触发条件非空：
  - `legal_system` - **所有国际人物必填** (普通法/大陆法/伊斯兰法/习惯法/混合)
  - `education_tradition` - 教育/哲学/思想领域人物必填 (儒家/伊斯兰/西方/土著/革命/自学)
  - `scientific_contribution` - 科学/技术/医学/工程领域人物必填 (是/否/领域)
  - `artistic_legacy` - 文学/艺术/音乐/建筑领域人物必填 (是/否/流派)
  - `environmental_stewardship` - 环保/自然资源/气候变化/极地人物必填 (是/否/实践)
  - `gender_role_innovation` - 女性人物/性别平等/女权主义人物必填 (是/否/描述)
  - `diaspora_network_type` - 侨民/流亡/跨文化人物必填 (劳动/知识/资本/文化/政治)
  - `digital_adaptation` - 20 世纪后期至今人物推荐填写 (先驱/跟随/滞后/跳跃)

### 2. 双语完整性

- [ ] 所有 `_zh` / `_en` 字段成对存在、非空、语义对应
- [ ] `steps_zh/en` 数组长度一致 (5-6 步)
- [ ] `modes` 数组为整数 ID，中英一致

### 3. 模式覆盖

- [ ] 每人物 `modes` 数组 ≥3 个 ID
- [ ] 每人物 `modes` 包含 ≥1 个 M215-M265 新模式
- [ ] **NEW v5**: 所有模式 ID 在 1-265 范围内
- [ ] 新旧模式无冗余：新模式与现有 265 模式余弦相似度 < 0.3 (人工抽检)

### 4. 代码格式与前缀一致性

- [ ] `code` 严格遵循 `{PREFIX}-{TOPIC}-{NNN}` (三位数补全)
- [ ] `PREFIX` 必须在 `code_prefix_registry_v4.csv` 中注册且 status=active/planned
- [ ] `TOPIC` 为 3-4 大写字母 (PHIL, SCI, POL, ECO, NOM, BUD, MOD, SEM, MUL, RES, ART, NAV, HOM, CLI, COS, FED, COF, EMP, NAT, ASH, UJA, KIL, MOB, KAB, SED, GOR, COC, PEA, FRE, OIL, INC, REV, BIO, IND, DOL, TEC, HYD, AGR, WAH, VIS, CAL, DIP, CON, HAS, SEM...)

### 5. 去重规则 (跨文明圈 v2)

- [ ] **核心成就期归属地原则**：按人物核心成就发生地确定主前缀
- [ ] **双重记录显式标注**：跨文明圈重大成就者创建双重记录，`dual_record` 字段标注如 `["DE", "US"]`, `["IR", "IL"]`
- [ ] **侨民/流亡规则全量适用**：核心成就期在侨居国 → 侨居国为主 (`nationality`=侨居国)、原籍国为辅 (`diaspora_influence` 非空标注原籍)
- [ ] **原住民知识授权**：`indigenous_knowledge_system` 非空时，必须有 `oral_tradition` 字段标注授权来源 (社区名称+年份/公开文献 DOI)
- [ ] **新增去重规则 (Phase 8)**：
  - 加勒比/大西洋去重：英/法/西/荷殖民遗产人物按核心成就期岛屿归属
  - 北极/极地去重：萨米/因纽特/格陵兰跨国族群按核心成就期国家归属，双重记录标注
  - 太平洋/大洋洲去重：波利尼西亚/密克罗尼西亚/美拉尼西亚人物按核心成就期岛国归属
  - **NEW Phase 9-12**: 萨哈勒去重：跨国萨哈勒人物按核心成就期国家归属
  - **NEW Phase 9-12**: 南亚去重： Partition 历史人物按核心成就期国家归属

### 6. 历史准确性

- [ ] 姓名/生卒年/核心成就与权威文献一致 (Wikipedia/Britannica/学术专著)
- [ ] 无时代错误：不将现代概念强加历史人物 (如给孔子贴"互联网思维")
- [ ] 争议点标注多方观点 (如斯大林/毛泽东/卡斯特罗/萨达姆/阿萨德/内塔尼亚胡等)
- [ ] **NEW v5**: 法律/教育/科学/艺术/环境/性别/数字化字段的值与历史事实一致

### 7. 数据一致性 (4主文件)

- [ ] `scenarios_zh.json` / `scenarios_en.json` 条目数一致，code 完全对应
- [ ] `code_maps.json` CODE_MAP/CODE_MAP_EN 覆盖所有前缀
- [ ] `scenario_tags.json` tags 覆盖所有前缀，结构完整
- [ ] 批次内人物 100% 同步到 4 个主文件

---

## 自动化校验脚本

```bash
# 1. Schema 校验 (v5)
python tools/validate_schema_v5.py --dir tools/json/ --schema tools/international_schema_v5.md

# 2. 前缀一致性
python tools/validate_prefixes.py --registry tools/code_prefix_registry_v4.csv --dir tools/json/

# 3. 模式覆盖 (M215-M265)
python tools/validate_modes.py --dir tools/json/ --new-modes 215-265 --min-modes 3

# 4. 双语完整性
python tools/validate_bilingual.py --dir tools/json/

# 5. 去重规则
python tools/validate_dedup.py --dir tools/json/ --rules tools/quality_checklist_v3.md

# 6. 主文件一致性
python tools/validate_main_files.py --zh tools/scenarios_zh.json --en tools/scenarios_en.json --maps tools/code_maps.json --tags tools/scenario_tags.json

# 7. v5 新字段校验
python tools/validate_v5_fields.py --dir tools/json/ --required-fields legal_system --conditional-fields education_tradition,scientific_contribution,artistic_legacy,environmental_stewardship,gender_role_innovation,diaspora_network_type,digital_adaptation
```

---

## 人工抽检清单 (每批次)

| 检查项 | 抽样比例 | 标准 |
|--------|----------|------|
| 历史准确性 (姓名/年代/成就) | 100% | 权威来源一致 |
| 模式映射合理性 | 100% | 专家评审 ≥3/5 通过 |
| 双语翻译质量 | 30% | 专业翻译评分 ≥4/5 |
| 新模式触发条件 | 100% | 字段非空 ↔ 触发条件匹配 |
| 去重规则应用 | 100% | 双重记录/侨民/原住民规则零遗漏 |
| **NEW**: v5 新增字段 | 100% | 法律/教育/科学/艺术/环境/性别/数字化字段值准确 |
| **NEW**: 跨文化复用性 | 50% | 新模式在目标领域/文明中的适用性验证 |

---

## 批次通过标准

| 批次 | 必须通过项 | 可选加分项 |
|------|------------|------------|
| P0 Batch 9-11 | 核心红线 1-7 全绿、测试 24/24、4 主文件同步、v5 Schema 合规 | 新模式 M215-M220 定义质量高、跨文化洞察深 |
| P1 Batch 12-14 | 核心红线 1-7 全绿、测试 24/24、4 主文件同步、v5 Schema 合规 | 非洲/撒哈拉知识准确、资源治理案例实证 |
| P2 Batch 15-16 | 核心红线 1-7 全绿、测试 24/24、4 主文件同步、v5 Schema 合规 | 欧洲/大洋洲/极地字段实证、气候适应案例实证 |

---

## 回归测试触发条件

- 任何批次完成 → 运行完整 `test_thinking_mode_selector.py`
- 累计新增 >50 人 → 运行语义搜索索引重建 + API 冒烟测试
- Phase 9-12 全部完成 → MkDocs 文档站全量重建 + Vue 3 前端 i18n 回归
- **NEW**: Schema v5 变更 → 运行 `validate_v5_fields.py` + `validate_schema_v5.py`

---

## 5 维去重检查清单 (v3)

### 1. 历史维度

| 检查项 | 标准 |
|--------|------|
| 人名年代一致性 | 与 Wikipedia/学术文献一致 |
| 成就归属准确性 | 按核心成就期确定 |
| 去重记录完整性 | 跨文明圈成就者双重记录 |

### 2. 模式维度

| 检查项 | 标准 |
|--------|------|
| 模式 ID 范围 | 1-265 范围内 |
| 新模式覆盖 | M215-M265 在相关人物中 |
| 模式-人物映射 | 每人关联 ≥1 新模式 |
| 跨文明复用 | 新模式在目标领域适用性验证 |

### 3. 字段维度

| 检查项 | 标准 |
|--------|------|
| 必填字段完整 | 15 核心 + 7 国际化 + `legal_system` 全填 |
| 可选字段触发 | 按触发条件非空 |
| 枚举值合法 | 必须在定义范围内 |
| 字段一致性 | 双语字段成对、语义对应 |

### 4. 双语维度

| 检查项 | 标准 |
|--------|------|
| 字段成对 | `_zh` / `_en` 同时存在 |
| 语义一致 | 中英语义对应 |
| 步骤数一致 | 5-6 步相同长度 |
| 翻译质量 | 专业翻译评分 ≥4/5 (抽样 30%) |

### 5. 去重维度

| 检查项 | 标准 |
|--------|------|
| 核心成就期归属 | 按成就地确定主前缀 |
| 跨文明圈双重记录 | `dual_record` 字段标注 |
| 侨民/流亡规则 | 侨居国为主、原籍标注 |
| 原住民知识授权 | `oral_tradition` 来源标注 |
| 萨哈勒/南亚去重 | 按核心成就期国家归属 |

---

## 版本历史

| 版本 | 日期 | 主要变更 |
|------|------|----------|
| v1.0 | Phase 4 | 基础格式/双语/模式覆盖 |
| v2.0 | Phase 7 | 国际化字段/新模式 M146-M158/去重规则 v1 |
| v3.0 | Phase 8 | 6 新可选字段/20 新模式 M159-M178/去重规则 v2 |
| **v3.0** | Phase 9-12 | **8 新可选字段/51 新模式 M215-M265/去重规则 v3 (萨哈勒/南亚)/Schema v5 校验** |
