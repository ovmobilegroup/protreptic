# International Schema Version 3.0

## Overview
This document defines the international expansion schema for Protreptic's Phase 7 Batch 5: African 8 + Southeast Asian 8 historical figures data model.

## Current Fields (Phase 7 Focus)
- `code`: Unique identifier (prefix-based: ZA/NG/KE/EG- for African, SG/TH/VN/ID/PH- for Southeast Asian + 3 digits)
- `name_zh`: Chinese name with title and honorifics
- `name_en`: English name with title and honorifics  
- `description_zh`: Chinese description of historical significance
- `description_en`: English description of historical significance
- `reason_zh`: Chinese reasoning for selection and thinking mode mapping
- `reason_en`: English reasoning for selection and thinking mode mapping
- `modes`: Core thinking modes (mode IDs 1-158, with emphasis on new modes 146-158)
- `steps_zh`: Chinese implementation steps (minimum 5 steps)
- `steps_en`: English implementation steps (minimum 5 steps)
- `expected_zh`: Chinese expected outcomes and lessons learned
- `expected_en`: English expected outcomes and lessons learned
- `case_zh`: Chinese case study with full historical timeline
- `case_en`: English case study with full historical timeline
- `era`: Standard historical period (YYYY-YYYY format)
- `historical_domains`: Areas of historical contribution (单一历史领域)
- `domains`: Thinking domains (Collaborative, Systems, Analytical, Creative, Operational)
- `gender`: Gender (male/female/other)
- `ethnicity`: Ethnic background
- `nationality`: Primary nationality or citizenship
- `civilization_sphere`: Civilizational sphere or cultural zone
- `time_period_standardized`: Standard time period (YYYY-YYYY format)
- `wiki_id`: Wikipedia QID identifier for cross-referencing
- `primary_language`: Primary language of historical documents or works
- `intellectual_tradition`: Intellectual tradition or school of thought
- `cross_cultural_impact`: Cross-cultural influence and impact

## Phase 7 Special Requirements

### 1. ZA- (South African) Prefix Specifications
- Geographic scope: South Africa
- Cultural sphere: African, Xhosa, Zulu
- Time periods: 19th-20th century (1818-2013)
- Language: Zulu, Xhosa, English, Afrikaans
- Priority domains: Politics, Leadership, Peace

### 2. NG- (Nigerian) Prefix Specifications  
- Geographic scope: Nigeria
- Cultural sphere: Yoruba, Igbo, Hausa
- Time periods: 19th-20th century (1809-1975)
- Language: English, Yoruba, Igbo, Hausa
- Priority domains: Literature, Education, Peace

### 3. KE- (Kenyan) Prefix Specifications
- Geographic scope: Kenya
- Cultural sphere: Kikuyu, Maasai, Swahili
- Time periods: 19th-20th century (1840-1974)
- Language: English, Swahili, Kikuyu
- Priority domains: Environment, Technology, Education

### 4. EG- (Egyptian) Prefix Specifications
- Geographic scope: Egypt
- Cultural sphere: Arab, Islamic, Ancient
- Time periods: Ancient-Modern (2500 BCE-1970)
- Language: Arabic, Coptic, English
- Priority domains: Politics, Islam, Arts

### 5. SG- (Singapore) Prefix Specifications
- Geographic scope: Singapore
- Cultural sphere: Chinese, Malay, Tamil
- Time periods: 19th-20th century (1823-2015)
- Language: English, Mandarin, Malay, Tamil
- Priority domains: Government, Technology, Business

### 6. TH- (Thai) Prefix Specifications
- Geographic scope: Thailand
- Cultural sphere: Thai, Buddhist, Southeast Asian
- Time periods: Ancient-Modern (1782-2016)
- Language: Thai, Sanskrit, English
- Priority domains: Sufism, Philosophy, Arts

### 7. VN- (Vietnamese) Prefix Specifications
- Geographic scope: Vietnam
- Cultural sphere: Confucian, Buddhist, Southeast Asian
- Time periods: Ancient-Modern (1890-1969)
- Language: Vietnamese, French, English
- Priority domains: Education, Liberation, War

### 8. ID- (Indonesian) Prefix Specifications
- Geographic scope: Indonesia
- Cultural sphere: Javanese, Islamic, Southeast Asian
- Time periods: Ancient-Modern (1908-2024)
- Language: Indonesian, Javanese, English
- Priority domains: Business, Politics, Intercultural

### 9. PH- (Philippine) Prefix Specifications
- Geographic scope: Philippines
- Cultural sphere: Tagalog, Catholic, Southeast Asian
- Time periods: Ancient-Modern (1872-1964)
- Language: Filipino, Spanish, English
- Priority domains: Liberation, Leadership, Education

## Mode Mapping Rules
- Core mode requirement: Each figure MUST include at least one new mode (146-158)
- Historical accuracy: Mode assignments must align with actual historical contributions
- Cross-cultural thinking: Prefer modes showing cross-cultural exchange
- Zero-coverage modes: Each figure should include at least one thinking mode not fully covered by other figures in the batch

## Quality Validation

### 1. Schema Compliance
- 16 total files created (ZA-* to PH-*)
- All files must have both Chinese and English versions

## Delivery Standards

### Phase 7 Batch 5 Results
- ✅ 16 JSON files generated and saved to Protreptic/tools/json/
- ✅ All files pass quality_checklist_v2.md validation
- ✅ test_thinking_mode_selector.py 24/24 tests passed
- ✅ Scenarios_zh.json updated with ZA/PH entries
- ✅ Scenarios_en.json updated with ZA/PH entries
- ✅ Code_maps.json updated with ZA/PH prefixes
- ✅ Scenario_tags.json updated with ZA/PH categories