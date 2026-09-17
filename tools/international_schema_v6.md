# 国际化 Schema v6.0

## 概述
支撑 Phase 13-16 全球补全扩展的完整数据模型，覆盖 20+ 文明圈、200+ 国家/地区、400+ 国际人物、95 个新思维模式 (M262-M356)。

---

## 15 核心字段 (必填)

| 字段名 | 类型 | 说明 | 示例 |
|--------|------|------|------|
| `code` | string | 唯一标识，格式 `{PREFIX}-{TOPIC}-{NNN}` | `GE-PHI-001` |
| `name_zh` | string | 中文姓名+专题 | `格鲁吉亚·伊利亚恰瓦泽：民族精神重生` |
| `name_en` | string | 英文姓名+专题 | `Ilia Chavchavadze: National Spirit Rebirth` |
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
| `modes` | array[int] | 思维模式 ID (1-356)，≥3个，≥1个新模式 | `[262, 237, 149, 1, 153]` |

---

## 8 核心国际化字段 (必填，继承 v3-v5)

| 字段名 | 类型 | 说明 | 示例 |
|--------|------|------|------|
| `nationality` | string | 国籍/文明归属 | `Georgia` |
| `civilization_sphere` | string | 文明圈 | `Caucasus/Orthodox` |
| `time_period_standardized` | string | 标准化时期 | `1837-1907` |
| `wiki_id` | string | Wikipedia ID | `Ilia_Chavchavadze` |
| `primary_language` | string | 主要语言 | `Georgian` |
| `intellectual_tradition` | string | 思想传统 | `National Awakening` |
| `cross_cultural_impact` | string | 跨文化影响 | `Georgia's national awakening leader` |
| `legacy_type` | string | 遗产类型 (Phase 13-16 新增) | `cultural/political/scientific/artistic/military` |

---

## 16 可选字段 (按需非空，v6 扩展至 16 个)

### Phase 8 继承字段 (6 个)

| 字段名 | 类型 | 触发条件 | 说明 |
|--------|------|----------|------|
| `polar_region` | boolean/string | 极地/北极圈人物 | `Arctic` / `Subarctic` / `Antarctic` |
| `island_nation` | boolean/string | 岛屿国家人物 | `Pacific` / `Caribbean` / `Atlantic` |
| `nomadic_heritage` | boolean/string | 游牧传承人物 | `Mongol` / `Bedouin` / `Sami` / `Tuareg` |
| `oral_tradition` | string | 口述传统非空时 | 授权来源/文献引用 |
| `resource_curse_mitigation` | boolean/string | 资源型经济体人物 | 是/否/实践 |
| `climate_adaptation` | boolean/string | 气候前线人物 | 是/否/实践 |

### Phase 9-12 继承字段 (8 个)

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

### Phase 13-16 新增字段 (2 个)

| 字段名 | 类型 | 触发条件 | 说明 |
|--------|------|----------|------|
| `regional_integration` | string | 区域一体化人物 | 区域组织：<br>`EU` / `ASEAN` / `AU` / `MERCOSUR` / `CIS` / `SCO` / `GCC` / `CARICOM` / `ECOWAS` / `SAARC` / `无` |
| `conflict_resolution_mechanism` | string | 冲突解决/和平人物 | 机制类型：<br>`和解委员会` / `真相委员会` / `过渡正义` / `联邦主义` / `权力分享` / `国际仲裁` / `谈判调解` / `抵抗革命` |

---

## 字段组合规则 (v6 扩展)

### 法律系统与文明圈映射 (v6 扩展)

| 文明圈 | 典型法律系统 | 示例国家/地区 |
|--------|-------------|--------------|
| Anglosphere | 普通法 | UK, US, CA, AU, NZ, IN, PK, BD, SG, MY, JM, BS, BB, GD, KN, LC, VC, TT |
| Western Europe | 大陆法 | FR, DE, IT, ES, PT, NL, BE, AT, CH, GR, CY, MT |
| Eastern Orthodox | 大陆法/混合 | RO, BG, RS, UA, BY, RU, MD, GE, AM, AZ |
| Islamic | 伊斯兰法/混合 | SA, IQ, IR, EG, MA, ID, MY, BD, PK, TR, JO, SY, LB, YE, OM, KW, BH, QA, AE |
| East Asian | 大陆法/习惯法混合 | CN, TW, KR, JP, VN, MN, KP |
| Central Asian | 大陆法/混合 | KZ, KG, TJ, TM, UZ |
| Southeast Asian | 混合 | TH, MM, LA, KH, PH, SG, MY, ID, BN, TL |
| South Asian | 混合 | IN, PK, BD, NP, BT, LK, MV |
| Latin America | 大陆法 | BR, AR, CL, PE, CO, MX, VE, CU, BO, EC, PY, UY, GT, SV, NI, HN, CR, PA, DO, HT, JM |
| Sub-Saharan Africa | 普通法/大陆法/习惯法混合 | ZA, NG, KE, GH, ET, TZ, CD, SN, CI, CM, AO, MW, ZM, ZW, BW, NA, SZ, LS, MG |
| Pacific | 混合 | AU, NZ, PG, SB, NR, FM, MH, FJ, VU, WS, TO, KI, TV, NU, PW, CK, AS, GU |
| Indigenous | 习惯法 | 原住民社区、口述传统社会 |
| Post-Soviet | 大陆法/混合 | RU, UA, BY, MD, GE, AM, AZ, KZ, KG, TJ, TM, UZ, LT, LV, EE |

### 教育传统与思维模式偏好 (v6 扩展)

| 教育传统 | 偏好思维模式 | 典型人物 |
|----------|------------|----------|
| 儒家 | M149 (儒商传承), M10 (系统思维) | 孔子、朱熹、王阳明 |
| 伊斯兰 | M161 (哈里发治理), M164 (民族建国) | 伊本·沙乌德、尼雷尔 |
| 西方 | M1 (批判性思维), M2 (系统思维) | 笛卡尔、康德、杜威 |
| 土著 | M185 (口述传统治理), M187 (酋长制共治) | 马赛长老、阿散蒂王 |
| 革命 | M192 (游击解放治理), M193 (后冲突民主修复) | 卡斯特罗、切·格瓦拉 |
| 自学 | M158 (通才整合), M165 (离散叙事书写) | 富兰克林、林肯 |
| 东正教 | M276 (正教传统治理), M277 (斯拉夫认同构建) | 伊利亚·恰瓦泽、托尔斯泰 |
| 中亚 | M278 (丝路贸易网络), M279 (游牧-定居融合) | 帖木儿、阿拜·库南巴耶夫 |
| 高加索 | M280 (山地民族自治), M281 (宗教多元共存) | 伊利亚·恰瓦泽、阿扎尔文化 |
| 东南亚 | M282 (多元文化共存), M283 (王国现代转型) | 阿努坤、拉玛五世 |

### 科学贡献与艺术遗产标识 (v6 扩展)

| 类型 | 科学贡献标识 | 艺术遗产标识 | 跨领域模式 |
|------|-------------|-------------|-----------|
| 纯科学 | `是` + `领域` | 否 | M158 (通才整合) |
| 纯艺术 | 否 | `是` + `流派` | M165 (离散叙事书写) |
| 文艺复兴式 | `是` + `领域` | `是` + `流派` | M158 + M165 |
| 工程技术 | `是` + `工程技术` | 否 | M160 (生态链主) |
| 人文社科 | 否 | `是` + `思想流派` | M1 (批判性思维) |
| 区域科学 | `是` + `区域特色科学` | 否 | M284 (区域知识整合) |
| 传统医学 | `是` + `传统医学` | 否 | M285 (传统科学现代转化) |

### 区域一体化与偏好模式 (v6 新增)

| 区域组织 | 典型场景 | 偏好模式 |
|---------|----------|----------|
| `EU` | 欧洲一体化建设 | M286 (欧盟治理), M287 (跨境合作) |
| `ASEAN` | 东南亚国家联盟 | M288 (东盟方式协商), M289 (区域经济整合) |
| `AU` | 非洲联盟 | M232 (泛非主义建国), M290 (非盟治理) |
| `MERCOSUR` | 南方共同市场 | M291 (南方共同市场治理), M292 (拉美经济一体化) |
| `CIS` | 独立国家联合体 | M293 (后苏联空间治理), M294 (俄语文化圈) |
| `SCO` | 上海合作组织 | M295 (上合组织多边外交), M296 (欧亚安全合作) |
| `GCC` | 海湾合作委员会 | M297 (海湾君主协同), M298 (能源外交) |
| `CARICOM` | 加勒比共同体 | M299 (加勒比区域治理), M300 (小国联盟外交) |
| `ECOWAS` | 西非国家经济共同体 | M301 (西非经济整合), M302 (区域维和机制) |
| `SAARC` | 南亚区域合作联盟 | M303 (南亚区域合作), M304 (跨印度洋合作) |

### 冲突解决机制与偏好模式 (v6 新增)

| 机制类型 | 典型场景 | 偏好模式 |
|---------|----------|----------|
| `和解委员会` | 种族/族群和解 | M305 (真相和解委员会), M306 (种族和解治理) |
| `真相委员会` | 历史创伤处理 | M307 (历史真相调查), M308 (集体记忆疗愈) |
| `过渡正义` | 独裁后转型 | M309 (过渡正义机制), M310 (制度化人权) |
| `联邦主义` | 多民族国家 | M311 (权力下放联邦), M312 (民族自治平衡) |
| `权力分享` | 后冲突建国 | M313 (权力分享机制), M314 (族群配额制) |
| `国际仲裁` | 领土争端解决 | M315 (国际仲裁外交), M316 (多边争端解决) |
| `谈判调解` | 持久冲突调解 | M317 (持久冲突调解), M318 (第三方外交) |
| `抵抗革命` | 殖民/压迫反抗 | M319 (非暴力抵抗), M320 (武装革命建国) |

---

## JSON 示例 (v6 完整)

```json
{
  "code": "GE-PHI-001",
  "name_zh": "格鲁吉亚·伊利亚恰瓦泽：民族精神重生",
  "name_en": "Ilia Chavchavadze: National Spirit Rebirth",
  "description_zh": "伊利亚·恰瓦泽是格鲁吉亚民族觉醒运动的领袖、诗人、作家、政治家。他领导了19世纪格鲁吉亚的文化复兴运动，通过文学、教育和政治活动唤醒民族意识，反抗俄国殖民统治，为格鲁吉亚的独立奠定基础。",
  "description_en": "Ilia Chavchavadze was a leader of the Georgian national awakening movement, poet, writer, and politician. He led the 19th-century Georgian cultural renaissance, awakening national consciousness through literature, education, and political activities, resisting Russian colonial rule and laying the foundation for Georgia's independence.",
  "reason_zh": "代表高加索地区的民族觉醒，展示了正教文明圈在殖民压迫下的文化复兴路径，对格鲁吉亚和整个高加索地区的民族认同构建有深远影响。",
  "reason_en": "Represents the national awakening in the Caucasus, demonstrating the path of cultural revival under colonial oppression in the Orthodox civilization sphere, with profound impact on national identity construction in Georgia and the entire Caucasus region.",
  "steps_zh": [
    "研究伊利亚·恰瓦泽的诗歌《英雄》《幽谷》和小说《强盗卡科》",
    "分析其民族觉醒思想与东正教传统的对话",
    "探讨19世纪高加索地区的民族复兴运动",
    "评估其创办《伊韦利亚》杂志的文化影响",
    "总结恰瓦泽思想在当代格鲁吉亚独立运动中的延续"
  ],
  "steps_en": [
    "Study Ilia Chavchavadze's poetry 'The Hero' and 'The Valley' and his novel 'Robber Kako'",
    "Analyze the dialogue between his national awakening thought and Orthodox tradition",
    "Explore the national revival movement in the Caucasus in the 19th century",
    "Evaluate the cultural impact of his founding of 'Iberia' magazine",
    "Summarize the continuity of Chavchavadze's thought in the contemporary Georgian independence movement"
  ],
  "expected_zh": "掌握恰瓦泽的核心民族复兴思想，理解高加索地区民族觉醒的发展路径，评估其对格鲁吉亚民族认同构建和独立运动的历史影响。",
  "expected_en": "Master Chavchavadze's core national revival thought, understand the development path of national awakening in the Caucasus, and evaluate his historical impact on Georgian national identity construction and the independence movement.",
  "case_zh": "伊利亚·恰瓦泽在 1869 年创办《伊韦利亚》杂志，成为格鲁吉亚民族复兴运动的核心舆论阵地，通过文学、历史和文化研究唤醒民族意识，直接推动了格鲁吉亚的语言恢复和民族认同重构。",
  "case_en": "In 1869, Ilia Chavchavadze founded 'Iberia' magazine, becoming the core public opinion platform of the Georgian national revival movement. Through literature, history, and cultural studies, he awakened national consciousness, directly promoting the restoration of Georgian language and the reconstruction of national identity.",
  "modes": [276, 262, 237, 1, 153],
  "nationality": "Georgia",
  "civilization_sphere": "Caucasus/Orthodox",
  "time_period_standardized": "1837-1907",
  "wiki_id": "Ilia_Chavchavadze",
  "primary_language": "Georgian",
  "intellectual_tradition": "National Awakening",
  "cross_cultural_impact": "Georgia's national awakening leader, influenced Caucasus nationalism",
  "legacy_type": "cultural",
  "legal_system": "大陆法",
  "education_tradition": "西方",
  "scientific_contribution": "否",
  "artistic_legacy": "是: 浪漫主义/民族文学",
  "environmental_stewardship": "否",
  "gender_role_innovation": "否",
  "diaspora_network_type": "文化",
  "digital_adaptation": "滞后",
  "regional_integration": "CIS",
  "conflict_resolution_mechanism": "抵抗革命"
}
```

---

## 质量校验规则 (v6)

### 1. 可选字段触发条件

- `legal_system`: **所有国际人物必填**
- `education_tradition`: 教育、哲学、思想领域人物必填
- `scientific_contribution`: 科学、技术、医学、工程领域人物必填
- `artistic_legacy`: 文学、艺术、音乐、建筑领域人物必填
- `environmental_stewardship`: 环保、自然资源、气候变化、极地人物必填
- `gender_role_innovation`: 女性人物、性别平等、女权主义人物必填
- `diaspora_network_type`: 侨民、流亡、跨文化人物必填
- `digital_adaptation`: 20 世纪后期至今人物推荐填写
- `regional_integration`: Phase 13-16 区域一体化人物**推荐填写**
- `conflict_resolution_mechanism`: Phase 13-16 冲突解决/和平人物**推荐填写**

### 2. 枚举值校验

- `legal_system`: 必须为 `普通法`, `大陆法`, `伊斯兰法`, `习惯法`, `混合` 之一
- `education_tradition`: 必须为 `儒家`, `伊斯兰`, `西方`, `土著`, `革命`, `自学`, `东正教`, `中亚`, `高加索`, `东南亚` 之一 (v6 扩展)
- `scientific_contribution`: 必须为 `是`, `否`, 或 `领域:xxx` 格式
- `artistic_legacy`: 必须为 `是`, `否`, 或 `流派:xxx` 格式
- `environmental_stewardship`: 必须为 `是`, `否`, 或 `实践:xxx` 格式
- `gender_role_innovation`: 必须为 `是`, `否`, 或 `描述:xxx` 格式
- `diaspora_network_type`: 必须为 `劳动`, `知识`, `资本`, `文化`, `政治` 之一
- `digital_adaptation`: 必须为 `先驱`, `跟随`, `滞后`, `跳跃` 之一
- `regional_integration`: 必须为 `EU`, `ASEAN`, `AU`, `MERCOSUR`, `CIS`, `SCO`, `GCC`, `CARICOM`, `ECOWAS`, `SAARC`, `无` 之一 (v6 新增)
- `conflict_resolution_mechanism`: 必须为 `和解委员会`, `真相委员会`, `过渡正义`, `联邦主义`, `权力分享`, `国际仲裁`, `谈判调解`, `抵抗革命` 之一 (v6 新增)

### 3. 字段一致性校验

- 双语字段（`_zh` / `_en`）必须成对存在
- `modes` 数组必须包含 ≥1 个 M262-M356 新模式
- 新模式与现有 356 模式余弦相似度 < 0.3 (人工抽检)
- `code` 必须遵循 `{PREFIX}-{TOPIC}-{NNN}` 格式
- `legacy_type` 必须与 `artistic_legacy`, `scientific_contribution` 等字段逻辑一致
- `regional_integration` 填写时，对应区域必须与 `nationality` 匹配
- `conflict_resolution_mechanism` 填写时，应与人物历史活动一致

---

## 版本历史

| 版本 | 日期 | 主要变更 |
|------|------|----------|
| v3.0 | Phase 7 | 7 核心国际化字段 |
| v4.0 | Phase 8 | 6 新增可选字段（极地/岛屿/游牧/口述/资源/气候） |
| v5.0 | Phase 9-12 | 8 新增可选字段（法律/教育/科学/艺术/环保/性别/侨民/数字），总计 22 字段 |
| v6.0 | Phase 13-16 | **2 新增核心字段（legacy_type）+ 2 新增可选字段（regional_integration, conflict_resolution_mechanism）**，总计 23 字段；支持 20+ 文明圈、95 个新模式 (M262-M356) |