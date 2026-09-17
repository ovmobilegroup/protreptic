# Phase 13-16 质检清单 v4.0

## 适用范围
适用于 Phase 13-16 全球补全批次中所有历史人物 JSON 文件的质量校验。

---

## 1. Schema 合规性校验 (international_schema_v6.md)

### 1.1 核心字段 (15 个必填)
- [ ] `code` 格式正确 (`{PREFIX}-{TOPIC}-{NNN}`)
- [ ] `name_zh` 非空，2-20 字
- [ ] `name_en` 非空，2-50 字
- [ ] `description_zh` 非空，200-500 字
- [ ] `description_en` 非空，200-500 字
- [ ] `reason_zh` 非空，50-200 字
- [ ] `reason_en` 非空，50-200 字
- [ ] `steps_zh` 非空，5-6 个步骤
- [ ] `steps_en` 非空，5-6 个步骤
- [ ] `expected_zh` 非空，50-200 字
- [ ] `expected_en` 非空，50-200 字
- [ ] `case_zh` 非空，100-300 字
- [ ] `case_en` 非空，100-300 字
- [ ] `modes` 非空数组，≥3 个，≥1 个 M262-M356 新模式

### 1.2 国际化字段 (8 个必填)
- [ ] `nationality` 非空，来自 code_prefix_registry_v5.csv
- [ ] `civilization_sphere` 非空，合法文明圈
- [ ] `time_period_standardized` 非空，YYYY-YYYY 或 YYYY 格式
- [ ] `wiki_id` 非空，维基百科条目名
- [ ] `primary_language` 非空
- [ ] `intellectual_tradition` 非空，10-50 字
- [ ] `cross_cultural_impact` 非空，50-200 字
- [ ] `legacy_type` 非空，来自 `cultural/political/scientific/artistic/military`

### 1.3 可选字段 (8 个继承 + 2 个新增)
- [ ] `legal_system` 必填 (所有人物)
- [ ] `education_tradition` 教育/哲学/思想人物必填
- [ ] `scientific_contribution` 科学/技术/医学人物必填
- [ ] `artistic_legacy` 文学/艺术/音乐/建筑人物必填
- [ ] `environmental_stewardship` 环保/自然/极地人物必填
- [ ] `gender_role_innovation` 女性/性别平等人物必填
- [ ] `diaspora_network_type` 侨民/流亡/跨文化人物必填
- [ ] `digital_adaptation` 20 世纪后期人物推荐填写
- [ ] `regional_integration` 区域一体化人物推荐填写
- [ ] `conflict_resolution_mechanism` 冲突解决/和平人物推荐填写

---

## 2. 模式映射校验 (modes_expansion_v4.md)

### 2.1 新模式覆盖
- [ ] 至少 1 个 M262-M356 新模式
- [ ] 新模式与文明圈/民族匹配
- [ ] 新模式与人物历史活动一致
- [ ] 模式总数达到 356+ (M1-M356)

### 2.2 模式区隔性
- [ ] 新模式与现有模式余弦相似度 < 0.3
- [ ] 新模式定义清晰，区隔点明确
- [ ] 新模式适用场景明确

---

## 3. 数据一致性校验 (4 主文件)

### 3.1 code_maps.json
- [ ] 所有 code 前缀在 code_prefix_registry_v5.csv 中注册
- [ ] code 前缀与 nationality 匹配
- [ ] code 前缀数量 ≥ 200

### 3.2 scenarios_zh.json / scenarios_en.json
- [ ] 每个 code 对应一个 scenario
- [ ] bilingual 字段配对完整
- [ ] modes 映射正确

### 3.3 scenario_tags.json
- [ ] 所有 code 有 tags
- [ ] tags 涵盖 civilization_sphere, legacy_type, regional_integration, conflict_resolution_mechanism

---

## 4. 双语校验

### 4.1 字段配对
- [ ] `name_zh` / `name_en` 配对存在
- [ ] `description_zh` / `description_en` 配对存在
- [ ] `reason_zh` / `reason_en` 配对存在
- [ ] `steps_zh` / `steps_en` 配对存在
- [ ] `expected_zh` / `expected_en` 配对存在
- [ ] `case_zh` / `case_en` 配对存在

### 4.2 内容一致性
- [ ] 中英文内容描述一致 (不仅翻译)
- [ ] 中英文 steps 数量一致
- [ ] 中英文 modes 数组一致

---

## 5. 去重校验

### 5.1 人物去重
- [ ] 不存在重复的 `name_zh` / `name_en`
- [ ] 不存在重复的 `wiki_id`

### 5.2 模式去重
- [ ] 不存在重复的模式定义
- [ ] 不存在模式 ID 冲突

---

## 6. 历史准确性校验

### 6.1 人物背景
- [ ] `nationality` 与 `wiki_id` 人物一致
- [ ] `time_period_standardized` 与人物生卒年份一致
- [ ] `civilization_sphere` 与人物文明背景一致

### 6.2 模式关联
- [ ] `modes` 中每个模式都与人物相关
- [ ] `steps` 与人物历史活动相关
- [ ] `case` 与人物真实事迹相关

---

## 7. 批次验收标准

### 7.1 每批次必须通过
- [ ] 8 人物 JSON 文件全部生成
- [ ] 所有人物通过 Schema v6 校验
- [ ] 8 个新模式 (M2XX-M3XX) 定义完整
- [ ] 8 个新国家/地区前缀注册

### 7.2 全阶段完成标志
- [ ] 95+ 前缀全部注册
- [ ] 95 个新模式 (M262-M356) 定义完整
- [ ] 96 位人物 JSON 文件通过 Schema v6 校验
- [ ] 4 主文件同步完成 (scenarios_zh/en, code_maps, tags)
- [ ] 5 个结构文档生成 (Schema v6, 前缀 v5, 批次 v4, 模式 v4, 质检 v4)

---

## 8. 版本历史

| 版本 | 日期 | 主要变更 |
|------|------|----------|
| v3.0 | Phase 9-12 | 51 检查项 |
| v4.0 | Phase 13-16 | **+22 检查项** (legacy_type, regional_integration, conflict_resolution_mechanism, M262-M356 新模式, 95 新前缀, 5 结构文档) |