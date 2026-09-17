# International Schema Version 2.0

## Overview
This document defines the international expansion schema for Protreptic's historical figures data model.

## Current Fields (Chinese/International Focus)
- `code`: Unique identifier (prefix-based)
- `name_zh`: Chinese name
- `name_en`: English name
- `description_zh`: Chinese description of historical significance
- `description_en`: English description of historical significance
- `reason_zh`: Chinese reasoning for selection
- `reason_en`: English reasoning for selection
- `modes`: Core thinking modes (mode IDs)
- `steps_zh`: Chinese implementation steps
- `steps_en`: English implementation steps
- `expected_zh`: Chinese expected outcomes
- `expected_en`: English expected outcomes
- `case_zh`: Chinese case study
- `case_en`: English case study
- `era`: Historical period
- `historical_domains`: Areas of historical contribution
- `domains`: Thinking domains (Collaborative, Systems, Analytical, Creative, Operational)
- `gender`: Gender
- `ethnicity`: Ethnic background

## New International Fields

### nationality
- Definition: Primary nationality or citizenship
- Chinese field name: `nationality`
- English field name: `nationality`
- Type: String
- Example: "South Korean", "Brazilian", "Chinese"
- Description: The main nationality of the historical figure

### civilization_sphere
- Definition: Civilizational sphere or cultural zone
- Chinese field name: `civilization_sphere`
- English field name: `civilization_sphere`
- Type: String
- Example: "East Asian", "Latin American", "Euro-American"
- Description: The civilizational context (Confucian, Islamic, etc.)

### time_period_standardized
- Definition: Standard historical time period (YYYY-YYYY format)
- Chinese field name: `time_period_standardized`
- English field name: `time_period_standardized`
- Type: String
- Example: "1910-1979", "1889-1934"
- Description: Standard time range for the historical figure's life/active period

### wiki_id
- Definition: Wikipedia ID for the historical figure
- Chinese field name: `wiki_id`
- English field name: `wiki_id`
- Type: String
- Example: "Q492543", "Q34662"
- Description: Wikipedia QID identifier for cross-referencing

### primary_language
- Definition: Primary language of historical documents or works
- Chinese field name: `primary_language`
- English field name: `primary_language`
- Type: String
- Example: "Korean", "Portuguese", "Chinese"
- Description: The main language used in the figure's works and documents

### intellectual_tradition
- Definition: Intellectual tradition or school of thought
- Chinese field name: `intellectual_tradition`
- English field name: `intellectual_tradition`
- Type: String
- Example: "Confucian", "Liberal", "Marxist"
- Description: The main intellectual tradition or philosophical school

## International Prefix Registry

### Korean (KR)
- Geographic scope: Korean Peninsula
- Cultural sphere: East Asian, Confucian
- Time periods: Modern era (19th-20th centuries)
- Language: Korean, Chinese

### Brazil (BR)
- Geographic scope: Brazil, Latin America
- Cultural sphere: Latin American, Portuguese
- Time periods: Modern era (19th-20th centuries)
- Language: Portuguese, Spanish

### United Kingdom (UK)
- Geographic scope: British Isles, Commonwealth
- Cultural sphere: Euro-American, Anglo-Saxon
- Time periods: Early modern to contemporary (16th-21st centuries)
- Language: English

### United States (US)
- Geographic scope: North America
- Cultural sphere: Euro-American, Modern
- Time periods: Early modern to contemporary (18th-21st centuries)
- Language: English

### Germany (EU)
- Geographic scope: German-speaking regions, Europe
- Cultural sphere: Euro-American, Enlightenment
- Time periods: Early modern to contemporary (16th-21st centuries)
- Language: German

## Code Mapping

### Korean Prefixes (KR-)
- `KR-ECON-001`: Economic transformation
- `KR-CHAE-001`: Business leadership
- `KR-CHAE-002`: Corporate innovation
- `KR-CONF-001`: Political reform
- `KR-CULT-001`: Cultural export
- `KR-TECH-001`: Technology and IT

### Brazilian Prefixes (BR-)
- `BR-NATI-001`: Monarchy and constitutional development
- `BR-MODE-001`: Independence and nation-building
- `BR-INDU-001`: Industrial development and urbanization
- `BR-AGRI-001`: Agricultural innovation and tropical development
- `BR-RESO-001`: Resource development and energy security
- `BR-SOCI-001`: Social development and welfare

## Quality Standards

### Bilingual Requirements
- All fields must have both Chinese and English versions
- English is the primary version for new entries
- Chinese version should maintain semantic equivalence

### Historical Accuracy
- All figures must have verifiable historical sources
- Wikipedia QIDs required for cross-referencing
- Historical periods must be accurately defined

### Mode Coverage
- Each figure must cover at least one zero-coverage thinking mode
- Cross-disciplinary thinking modes preferred
- Mode diversity across nationalities encouraged

### Uniqueness and De-duplication
- Cross-national de-duplication for figures of the same historical period
- Avoid duplicate entries for the same historical figure across countries
- Clear attribution for cross-cultural influence cases