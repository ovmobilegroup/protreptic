# International Figures Quality Checklist Version 2.0

## Overview

This document contains quality standards and checklists for international historical figures in the Protreptic system, specifically for Phase 7 Batch 2 (India + Persia/Iran figures).

## Quality Standards

### 1. Bilingual Completeness

|- [x] All figures have both Chinese (zh) and English (en) versions
|- [x] Chinese and English names are accurate translations
|- [x] Descriptions, reasoning, and case studies are available in both languages
|- [x] Mode names are translated appropriately
|- [x] Historical periods are standardized across languages
|- [x] New international fields (nationality, civilization_sphere, etc.) are populated

### 2. Historical Accuracy

|- [x] All figures have verifiable historical sources
|- [x] Wikipedia QIDs are provided for cross-referencing
|- [x] Historical periods are accurate and well-defined
|- [x] Nationality and civilization sphere are correctly identified
|- [x] Primary language of historical documents is specified

### 3. Mode Coverage Requirements

|- [x] Each figure covers at least 1 zero-coverage thinking mode
|- [x] Mode assignments are accurate and relevant to the figure's historical contribution
|- [x] Cross-disciplinary thinking modes are encouraged
|- [x] Mode diversity across nationalities is maintained
|- [x] Mode names are culturally appropriate

### 4. Code Prefix System

|- [x] International prefixes follow consistent format: {PREFIX}-{TOPIC}-{NNN}
|- [x] Korean figures use KR- prefix
|- [x] Brazilian figures use BR- prefix
|- [x] Other international prefixes properly registered
|- [x] Prefixes are unique and non-overlapping
|- [x] IN- prefix for India figures
|- [x] IR- prefix for Persia/Iran figures

### 5. Quality Metrics

|- [x] Data structure follows international_schema_v3.md requirements
|- [x] All mandatory fields are present (code, name_zh, name_en, core_mode, era, country, etc.)
|- [x] Optional fields are appropriately populated when available
|- [x] Historical domains and thinking domains are correctly categorized
|- [x] Gender and ethnicity are accurately represented

### 6. Cross-National De-duplication

|- [x] Figures with similar historical periods across countries are flagged for review
|- [x] Cross-cultural influence cases are clearly attributed
|- [x] Migration of historical figures between countries is documented
|- [x] Similar historical contributions are distinguished by context and era

### 7. Phase 7 Batch 2 Specific Requirements

|- [x] Create 8 Indian figures (IN- prefix) and 8 Persian/Iranian figures (IR- prefix)
|- [x] Each figure must include at least one new mode (146-158)
|- [x] Follow Phase 7 Special Requirements in international_schema_v3.md
|- [x] Ensure zero-coverage mode distribution
|- [x] Update scenarios_zh.json and scenarios_en.json
|- [x] Update code_maps.json with IN and IR prefixes
|- [x] Update scenario_tags.json with IN and IR categories

## Implementation Guidelines

### For New Figures

1. Research historical accuracy thoroughly using multiple sources
2. Verify Wikipedia QID availability
3. Determine appropriate thinking modes based on historical contribution
4. Ensure bilingual completeness before submission
5. Follow international prefix registry for code assignment (IN-/IR-)

### For Quality Review

1. Cross-reference historical information with authoritative sources
2. Verify mode assignments with historical contribution analysis
3. Check for duplicates with existing international figures
4. Ensure cultural appropriateness of mode names and descriptions
5. Validate completeness of required fields

### For Maintenance

1. Regularly update historical information as new research emerges
2. Review and update mode assignments based on evolving understanding
3. Maintain cross-national consistency in data structure
4. Update quality checklist based on review findings

## Quality Assurance Process

### Step 1: Initial Validation

|- Verify all required fields are present
|- Check bilingual completeness
|- Validate historical accuracy
|- Ensure mode coverage requirements are met
|- Verify zero-coverage mode inclusion
|- Check Phase 7 specific requirements

### Step 2: Cross-Validation

|- Check for duplicates with existing figures
|- Verify cross-national consistency
|- Validate schema compliance
|- Ensure quality standards compliance
|- Check cross-cultural influence attribution

### Step 3: Final Review

|- Comprehensive quality assessment
|- Stakeholder feedback incorporation
|- Documentation update
|- Process improvement identification
|- Phase 7 Batch 2 completion verification

## Quality Metrics and KPIs

### Quantitative Metrics

|- **Completeness Score**: % of required fields populated (>95%)
|- **Bilingual Accuracy**: % of fields with complete zh/en versions (>99%)
|- **Historical Accuracy**: % of figures with verified Wikipedia QIDs (>100%)
|- **Mode Coverage**: % of figures with zero-coverage modes (>100%)
|- **Schema Compliance**: % of files following schema v3.0 (>100%)
|- **Phase 7 Completion**: All 16 files created and validated (100%)

### Qualitative Metrics

|- Historical significance depth and accuracy
|- Thinking mode relevance and cultural appropriateness
|- Cross-cultural influence documentation quality
|- Implementation step practicality and clarity
|- Expected outcomes measurability and achievability
