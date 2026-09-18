# 国际化 Schema v5.0

## 概述

支撑 Phase 9-12 全球补全扩展的完整数据模型，覆盖 15+ 文明圈、90+ 国家/地区、300+ 国际人物、51 个新思维模式 (M215-M265)。

---

## 15 核心字段 (必填)

| 字段名 | 类型 | 说明 | 示例 |
|--------|------|------|------|
| `code` | string | 唯一标识，格式 `{PREFIX}-{TOPIC}-{NNN}` | `PK-EDU-001` |
| `name_zh` | string | 中文姓名+专题 | `穆罕默德·伊克巴尔：伊斯兰哲学复兴` |
| `name_en` | string | 英文姓名+专题 | `Muhammad Iqbal: Islamic Philosophical Revival` |
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
| `modes` | array[int] | 思维模式 ID (1-265)，≥3个，≥1个新模式 | `[237, 215, 149, 1, 153]` |

---

## 7 核心国际化字段 (必填，继承 v3/v4)

| 字段名 | 类型 | 说明 | 示例 |
|--------|------|------|------|
| `nationality` | string | 国籍/文明归属 | `Pakistan` |
| `civilization_sphere` | string | 文明圈 | `Islamic/South Asian` |
| `time_period_standardized` | string | 标准化时期 | `1877-1938` |
| `wiki_id` | string | Wikipedia ID | `Muhammad_Iqbal` |
| `primary_language` | string | 主要语言 | `Urdu` |
| `intellectual_tradition` | string | 思想传统 | `Islamic Modernism` |
| `cross_cultural_impact` | string | 跨文化影响 | `Pakistan's national poet` |

---

## 14 可选字段 (按需非空，v5 扩展至 14 个)

### Phase 8 继承字段 (6 个)

| 字段名 | 类型 | 触发条件 | 说明 |
|--------|------|----------|------|
| `polar_region` | boolean/string | 极地/北极圈人物 | `Arctic` / `Subarctic` / `Antarctic` |
| `island_nation` | boolean/string | 岛屿国家人物 | `Pacific` / `Caribbean` / `Atlantic` |
| `nomadic_heritage` | boolean/string | 游牧传承人物 | `Mongol` / `Bedouin` / `Sami` / `Tuareg` |
| `oral_tradition` | string | 口述传统非空时 | 授权来源/文献引用 |
| `resource_curse_mitigation` | boolean/string | 资源型经济体人物 | 是/否/实践 |
| `climate_adaptation` | boolean/string | 气候前线人物 | 是/否/实践 |

### Phase 9-12 新增字段 (8 个)

| 字段名 | 类型 | 触发条件 | 说明 |
|--------|------|----------|------|
| `legal_system` | string | 所有国际人物 | 法律传统：<br>`普通法` / `大陆法` / `伊斯兰法` / `习惯法` / `混合` |
| `education_tradition` | string | 教育影响力人物 | 教育传统：<br>`儒家` / `伊斯兰` / `西方` / `土著` / `革命` / `自学` |
| `scientific_contribution` | boolean/string | 科学/技术人物 | 科学贡献标识：<br>`是` / `否` / `领域`（如数学、物理、医学） |
| `artistic_legacy` | boolean/string | 艺术/文学人物 | 艺术遗产标识：<br>`是` / `否` / `流派`（如现代主义、魔幻现实主义） |
| `environmental_stewardship` | boolean/string | 环保/自然资源人物 | 环境管理：<br>`是` / `否` / `实践`（如保护主义、可持续发展） |
| `gender_role_innovation` | boolean/string | 性别平等/女性人物 | 性别角色创新：<br>`是` / `否` / `描述`（如女权主义先驱、性别平等实践） |
| `diaspora_network_type` | string | 侨民/流亡人物 | 侨民网络类型：<br>`劳动` / `知识` / `资本` / `文化` / `政治` |
| `digital_adaptation` | string | 数字时代/技术人物 | 数字化适应：<br>`先驱` / `跟随` / `滞后` / `跳跃` |

---

## 字段组合规则 (v5 扩展)

### 法律系统与文明圈映射

| 文明圈 | 典型法律系统 | 示例国家/地区 |
|--------|-------------|--------------|
| Anglosphere | 普通法 | UK, US, CA, AU, NZ, IN, PK, BD, SG, MY |
| Western Europe | 大陆法 | FR, DE, IT, ES, PT, NL, BE, AT, CH |
| Islamic | 伊斯兰法 | SA, IQ, IR, EG, MA, ID, MY, BD, PK |
| East Asian | 大陆法/习惯法混合 | CN, TW, KR, JP, VN |
| Latin America | 大陆法 | BR, AR, CL, PE, CO, MX, VE, CU |
| Sub-Saharan Africa | 普通法/大陆法/习惯法混合 | ZA, NG, KE, GH, ET, TZ, CD |
| Indigenous | 习惯法 | 原住民社区、口述传统社会 |

### 教育传统与思维模式偏好

| 教育传统 | 偏好思维模式 | 典型人物 |
|----------|------------|----------|
| 儒家 | M149 (儒商传承), M10 (系统思维) | 孔子、朱熹、王阳明 |
| 伊斯兰 | M161 (哈里发治理), M164 (民族建国) | 伊本·沙乌德、尼雷尔 |
| 西方 | M1 (批判性思维), M2 (系统思维) | 笛卡尔、康德、杜威 |
| 土著 | M185 (口述传统治理), M187 (酋长制共治) | 马赛长老、阿散蒂王 |
| 革命 | M192 (游击解放治理), M193 (后冲突民主修复) | 卡斯特罗、切·格瓦拉 |
| 自学 | M158 (通才整合), M165 (离散叙事书写) | 富兰克林、林肯 |

### 科学贡献与艺术遗产标识

| 类型 | 科学贡献标识 | 艺术遗产标识 | 跨领域模式 |
|------|-------------|-------------|-----------|
| 纯科学 | `是` + `领域` | 否 | M158 (通才整合) |
| 纯艺术 | 否 | `是` + `流派` | M165 (离散叙事书写) |
| 文艺复兴式 | `是` + `领域` | `是` + `流派` | M158 + M165 |
| 工程技术 | `是` + `工程技术` | 否 | M160 (生态链主) |
| 人文社科 | 否 | `是` + `思想流派` | M1 (批判性思维) |

### 侨民网络类型与应用场景

| 侨民网络类型 | 典型场景 | 偏好模式 |
|-------------|----------|----------|
| `劳动` | 劳务输出、劳工侨民 | M164 (民族建国) |
| `知识` | 学者、专业人士侨民 | M158 (通才整合), M165 (离散叙事书写) |
| `资本` | 商业侨民、投资移民 | M153 (儒商传承) |
| `文化` | 艺术家、文化侨民 | M165 (离散叙事书写) |
| `政治` | 流亡政府、政治侨民 | M164 (民族建国), M172 (少数派生存外交) |

### 数字化适应与时代特征

| 数字化适应 | 时代特征 | 典型人物/模式 |
|-----------|----------|--------------|
| `先驱` | 数字时代开创者 | 比尔·盖茨、乔布斯 (M158) |
| `跟随` | 快速适应者 | 现代企业家 (M160) |
| `滞后` | 传统领域但数字化转型 | 传统行业转型者 (M168) |
| `跳跃` | 跳过模拟时代直接数字化 | 非洲移动支付、东南亚电商 (M241-M250) |

---

## JSON 示例 (v5 完整)

```json
{
  "code": "PK-EDU-001",
  "name_zh": "穆罕默德·伊克巴尔：伊斯兰哲学复兴",
  "name_en": "Muhammad Iqbal: Islamic Philosophical Revival",
  "description_zh": "伊克巴尔是巴基斯坦国父、诗人、哲学家，提出'自我'（Khudi）概念，融合伊斯兰哲学与现代西方思想，为巴基斯坦建国提供思想基础。",
  "description_en": "Iqbal was Pakistan's national poet, philosopher, and politician who proposed the concept of 'Khudi' (Selfhood), synthesizing Islamic philosophy with modern Western thought, providing the ideological foundation for Pakistan's creation.",
  "reason_zh": "代表南亚伊斯兰现代主义，展示了伊斯兰思想与西方哲学的创造性对话，对巴基斯坦建国和伊斯兰世界有深远影响。",
  "reason_en": "Represents South Asian Islamic modernism, demonstrating creative dialogue between Islamic thought and Western philosophy, with profound impact on Pakistan's creation and the Islamic world.",
  "steps_zh": [
    "研究伊克巴尔的诗歌《秘密与自我》和《东方的信息》",
    "分析其'自我'概念与西方哲学（尼采、柏格森）的对话",
    "探讨伊斯兰现代主义在印度次大陆的发展",
    "评估其'两个民族'理论对巴基斯坦建国的历史作用",
    "总结伊克巴尔思想在当代伊斯兰世界的适用性"
  ],
  "steps_en": [
    "Study Iqbal's poetry 'Asrar-e-Khudi' and 'Bang-e-Dra'",
    "Analyze the dialogue between his concept of 'Khudi' and Western philosophy (Nietzsche, Bergson)",
    "Explore Islamic modernism in the Indian subcontinent",
    "Evaluate the historical role of his 'Two-Nation Theory' in Pakistan's creation",
    "Summarize the applicability of Iqbal's thought in the contemporary Islamic world"
  ],
  "expected_zh": "掌握伊克巴尔的核心哲学概念，理解伊斯兰现代主义在南亚的发展路径，评估其对巴基斯坦建国和伊斯兰思想史的影响。",
  "expected_en": "Master Iqbal's core philosophical concepts, understand the development path of Islamic modernism in South Asia, and evaluate its impact on Pakistan's creation and Islamic intellectual history.",
  "case_zh": "伊克巴尔在 1930 年阿拉哈巴德穆斯林联盟年会上提出'印度西北部穆斯林自治国家'构想，成为巴基斯坦建国的思想源头。",
  "case_en": "In his 1930 Allahabad Muslim League presidential address, Iqbal proposed the concept of an 'autonomous Muslim state in northwestern India', becoming the ideological source for Pakistan's creation.",
  "modes": [237, 215, 149, 1, 153],
  "nationality": "Pakistan",
  "civilization_sphere": "Islamic/South Asian",
  "time_period_standardized": "1877-1938",
  "wiki_id": "Muhammad_Iqbal",
  "primary_language": "Urdu",
  "intellectual_tradition": "Islamic Modernism",
  "cross_cultural_impact": "Pakistan's national poet, influenced Islamic revival worldwide",
  "legal_system": "普通法",
  "education_tradition": "伊斯兰",
  "scientific_contribution": "否",
  "artistic_legacy": "是: 诗歌/哲学",
  "environmental_stewardship": "否",
  "gender_role_innovation": "否",
  "diaspora_network_type": "知识",
  "digital_adaptation": "滞后"
}
```

---

## 质量校验规则 (v5)

### 1. 可选字段触发条件

- `legal_system`: **所有国际人物必填**
- `education_tradition`: 教育、哲学、思想领域人物必填
- `scientific_contribution`: 科学、技术、医学、工程领域人物必填
- `artistic_legacy`: 文学、艺术、音乐、建筑领域人物必填
- `environmental_stewardship`: 环保、自然资源、气候变化、极地人物必填
- `gender_role_innovation`: 女性人物、性别平等、女权主义人物必填
- `diaspora_network_type`: 侨民、流亡、跨文化人物必填
- `digital_adaptation`: 20 世纪后期至今人物推荐填写

### 2. 枚举值校验

- `legal_system`: 必须为 `普通法`, `大陆法`, `伊斯兰法`, `习惯法`, `混合` 之一
- `education_tradition`: 必须为 `儒家`, `伊斯兰`, `西方`, `土著`, `革命`, `自学` 之一
- `scientific_contribution`: 必须为 `是`, `否`, 或 `领域:xxx` 格式
- `artistic_legacy`: 必须为 `是`, `否`, 或 `流派:xxx` 格式
- `environmental_stewardship`: 必须为 `是`, `否`, 或 `实践:xxx` 格式
- `gender_role_innovation`: 必须为 `是`, `否`, 或 `描述:xxx` 格式
- `diaspora_network_type`: 必须为 `劳动`, `知识`, `资本`, `文化`, `政治` 之一
- `digital_adaptation`: 必须为 `先驱`, `跟随`, `滞后`, `跳跃` 之一

### 3. 字段一致性校验

- 双语字段（`_zh` / `_en`）必须成对存在
- `modes` 数组必须包含 ≥1 个 M215-M265 新模式
- 新模式与现有 265 模式余弦相似度 < 0.3 (人工抽检)
- `code` 必须遵循 `{PREFIX}-{TOPIC}-{NNN}` 格式

---

## 版本历史

| 版本 | 日期 | 主要变更 |
|------|------|----------|
| v3.0 | Phase 7 | 7 核心国际化字段 |
| v4.0 | Phase 8 | 6 新增可选字段（极地/岛屿/游牧/口述/资源/气候） |
| v5.0 | Phase 9-12 | **8 新增可选字段（法律/教育/科学/艺术/环保/性别/侨民/数字）**，总计 22 字段 |
