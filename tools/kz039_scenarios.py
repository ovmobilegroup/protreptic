import json

# Read existing files
with open('/opt/data/workspace/Protreptic/data/scenarios_zh.json', 'r') as f:
    scenarios_zh = json.load(f)

with open('/opt/data/workspace/Protreptic/data/scenarios_en.json', 'r') as f:
    scenarios_en = json.load(f)

with open('/opt/data/workspace/Protreptic/data/scenario_tags.json', 'r') as f:
    scenario_tags = json.load(f)

# Check if H-KZ-039 already exists (list of dicts)
existing = [e for e in scenarios_zh if e.get("code") == "H-KZ-039"]
if existing:
    print("H-KZ-039 already exists in scenarios_zh.json")
else:
    # Add new entry to list
    kz_entry = {
        "code": "H-KZ-039",
        "name": "蒯子（蒯通）：三分鼎足的战略博弈模型",
        "core_mode": "M761 审时度势法 / Timing and Situational Awareness Method",
        "new_mode": "N/A (uses existing M761-M770)",
        "category": "Warring States / Chinese Strategy",
        "region": "East Asia",
        "country": "Zhao / Han",
        "year": -256,
    }
    
    scenarios_zh.append(kz_entry)
    
    # Build English entry for scenarios_en (also a list)
    kz_entry_en = {
        "code": "H-KZ-039",
        "name_en": "Kuai Zi (Kuai Tong): Tripartite Balance Strategic Game Model",
        "core_mode_en": "M761 Timing and Situational Awareness Method",
        "new_mode_en": "N/A (uses existing M761-M770)",
        "category_en": "Warring States / Chinese Strategy",
        "region_en": "East Asia",
        "country_en": "Zhao / Han",
        "year": -256,
    }
    
    scenarios_en.append(kz_entry_en)
    
    # Build scenario_tags (this IS a dict keyed by code)
    if "H-KZ-039" not in scenario_tags:
        kz_tags = {
            "H-KZ-039": ["战国", "秦末汉初", "纵横家", "政治博弈", "战略模型", "三分天下", 
                           "多极均势", "审时度势", "权变智慧", "游说艺术", "风险预判"]
        }
        scenario_tags.update(kz_tags)
    
    # Write back all files
    with open('/opt/data/workspace/Protreptic/data/scenarios_zh.json', 'w') as f:
        json.dump(scenarios_zh, f, ensure_ascii=False, indent=2)
    
    with open('/opt/data/workspace/Protreptic/data/scenarios_en.json', 'w') as f:
        json.dump(scenarios_en, f, ensure_ascii=False, indent=2)
    
    with open('/opt/data/workspace/Protreptic/data/scenario_tags.json', 'w') as f:
        json.dump(scenario_tags, f, ensure_ascii=False, indent=2)
    
    print("SUCCESS: Updated scenarios_zh.json, scenarios_en.json, scenario_tags.json")