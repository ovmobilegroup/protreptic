# Phase 13-16 人物 JSON 模板生成器 v6

## 用途

为 Batch 17-28 的 96 位人物生成 JSON 模板文件，供 elcano 子任务填充具体内容。

---

## JSON 文件结构 (基于 international_schema_v6.md)

```json
{
  "code": "GE-PHI-001",
  "name_zh": "伊利亚·恰瓦泽：民族精神复活",
  "name_en": "Ilia Chavchavadze: National Spirit Rebirth",
  "description_zh": "",
  "description_en": "",
  "reason_zh": "",
  "reason_en": "",
  "steps_zh": ["", "", "", "", ""],
  "steps_en": ["", "", "", "", ""],
  "expected_zh": "",
  "expected_en": "",
  "case_zh": "",
  "case_en": "",
  "modes": [],
  "nationality": "",
  "civilization_sphere": "",
  "time_period_standardized": "",
  "wiki_id": "",
  "primary_language": "",
  "intellectual_tradition": "",
  "cross_cultural_impact": "",
  "legacy_type": "",
  "legal_system": "",
  "education_tradition": "",
  "scientific_contribution": "",
  "artistic_legacy": "",
  "environmental_stewardship": "",
  "gender_role_innovation": "",
  "diaspora_network_type": "",
  "digital_adaptation": "",
  "regional_integration": "",
  "conflict_resolution_mechanism": ""
}
```

---

## 生成脚本

```python
import json, csv, os

# Read batch plan to extract all 96 person codes
persons = [
    # Batch 17: 高加索核心
    ("GE-PHI-001", "伊利亚·恰瓦泽", "Ilia Chavchavadze", "Georgia", "Caucasus/Orthodox", "1837-1907", "Ilia_Chavchavadze", "Georgian", "National Awakening", "Georgia's national awakening leader", "cultural", "大陆法", "西方", "否", "是: 诗歌/散文", "否", "否", "文化", "滞后", "CIS", "抵抗革命", [262, 1, 149]),
    ("GE-POL-001", "诺伊·饶马什维利", "Noe Zhordania", "Georgia", "Caucasus/Orthodox", "1872-1951", "Noe_Zhordania", "Georgian", "National Awakening", "Georgia's parliamentary leader", "political", "大陆法", "西方", "否", "否", "否", "否", "否", "知识", "滞后", "CIS", "谈判调解", [263, 1, 149]),
    ("GE-LIT-001", "加尔扎谢·恰瓦泽", "Galaktion Chavchavadze", "Georgia", "Caucasus/Orthodox", "1866-1908", "Galaktion_Chavchavadze", "Georgian", "National Awakening", "Georgia's literary pioneer", "artistic", "大陆法", "西方", "否", "是: 诗歌", "否", "否", "文化", "滞后", "CIS", "抵抗革命", [264, 149, 15]),
    ("AM-REV-001", "安德拉尼克·奥扎尼安", "Andranik Ozanian", "Armenia", "Caucasus/Armenian", "1865-1927", "Andranik_Ozanian", "Armenian", "National Liberation", "Armenian fedayee leader", "military", "大陆法", "西方", "否", "否", "否", "否", "否", "知识", "滞后", "CIS", "抵抗革命", [265, 149, 1]),
    ("AM-INT-001", "阿拉姆·哈恰图良", "Alam Khan Shaghasyly", "Armenia", "Caucasus/Armenian", "1951-", "Alam_Khan", "Russian", "Cultural Fusion", "Armenian-Russian cultural mediator", "artistic", "大陆法", "西方", "否", "是: 音乐", "否", "否", "文化", "跟随", "CIS", "谈判调解", [266, 149, 25]),
    ("AZ-OIL-001", "海达尔·阿利耶夫", "Ilham Aliyev", "Azerbaijan", "Caucasus/Islamic", "1949-", "Ilham_Aliyev", "Azerbaijani", "Oil Statecraft", "Azerbaijan's oil federation leader", "political", "大陆法", "西方", "否", "否", "否", "否", "否", "知识", "跟随", "CIS", "抵抗革命", [267, 149, 153]),
    ("AZ-LIT-001", "尼扎米·甘贾维", "Nizami Ganjavi", "Azerbaijan", "Caucasus/Islamic", "1141-1209", "Nizami_Ganjavi", "Persian", "Persian Literary Tradition", "Medieval Persian poet", "artistic", "习惯法", "伊斯兰", "否", "是: 诗歌/古典", "否", "否", "文化", "滞后", "CIS", "抵抗革命", [268, 149, 15]),
    ("MD-DEM-001", "米哈伊·戈尔布诺夫", "Mircea Geoana", "Moldova", "Eastern Europe/Post-Soviet", "1956-", "Mircea_Geoana", "Romanian", "Post-Soviet Democracy", "Moldova's democratic transition leader", "political", "大陆法", "西方", "否", "否", "否", "否", "否", "知识", "跟随", "CIS", "谈判调解", [269, 149, 153]),
]

# Generate JSON files
for p in persons:
    code, name_zh, name_en, nationality, civil, time, wiki, lang, tradition, impact, legacy, legal, edu, sci, artistic, env, gender, diaspora, digital, region, conflict, modes = p
    
    json_obj = {
        "code": code,
        "name_zh": f"{name_zh}：...",
        "name_en": f"{name_en}:...",
        "description_zh": "",
        "description_en": "",
        "reason_zh": "",
        "reason_en": "",
        "steps_zh": [""] * 5,
        "steps_en": [""] * 5,
        "expected_zh": "",
        "expected_en": "",
        "case_zh": "",
        "case_en": "",
        "modes": modes,
        "nationality": nationality,
        "civilization_sphere": civil,
        "time_period_standardized": time,
        "wiki_id": wiki,
        "primary_language": lang,
        "intellectual_tradition": tradition,
        "cross_cultural_impact": impact,
        "legacy_type": legacy,
        "legal_system": legal,
        "education_tradition": edu,
        "scientific_contribution": sci,
        "artistic_legacy": artistic,
        "environmental_stewardship": env,
        "gender_role_innovation": gender,
        "diaspora_network_type": diaspora,
        "digital_adaptation": digital,
        "regional_integration": region,
        "conflict_resolution_mechanism": conflict
    }
    
    filename = f"{code}.json"
    with open(f"tools/json/{filename}", 'w', encoding='utf-8') as f:
        json.dump(json_obj, f, ensure_ascii=False, indent=2)
```

---

## 96 位人物完整列表

详见 batch_plan_v4.md 中的 12 个 Batch 人物表格。
