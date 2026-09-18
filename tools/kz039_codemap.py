import json

# Read existing code_maps.json
with open('/opt/data/workspace/Protreptic/data/code_maps.json', 'r') as f:
    code_maps = json.load(f)

# Build the H-KZ-039 entry
kz_entry = {
    "scenarios_zh": ["['战国', '秦末汉初']"],
    "scenarios_en": ["['Warring States, Late Qin-Early Han Transition']"],
    "related_modes": [
        "KZ-039-M01",
        "KZ-039-M02",
        "KZ-039-M03",
        "KZ-039-M04",
        "KZ-039-M05",
        "KZ-039-M06",
        "KZ-039-M07",
        "KZ-039-M08",
        "KZ-039-M09",
        "KZ-039-M10"
    ],
    "tags": [
        "战国",
        "秦末汉初",
        "纵横家",
        "政治博弈",
        "战略模型",
        "三分天下",
        "多极均势",
        "审时度势",
        "权变智慧",
        "游说艺术",
        "风险预判",
        "鼎足而居",
        "楚汉相争",
        "韩信",
        "战略时机"
    ]
}

# Insert at the end (code_maps is an OrderedDict-like structure)
code_maps["H-KZ-039"] = kz_entry

# Write back with proper formatting
with open('/opt/data/workspace/Protreptic/data/code_maps.json', 'w') as f:
    json.dump(code_maps, f, ensure_ascii=False, indent=2)

# Verify
with open('/opt/data/workspace/Protreptic/data/code_maps.json', 'r') as f:
    content = f.read()

assert '"H-KZ-039"' in content, "ERROR: H-KZ-039 not found in code_maps!"
print(f"SUCCESS: Added H-KZ-039 to code_maps.json")
print(f"Tags count: {len(kz_entry['tags'])}")
print(f"Related modes count: {len(kz_entry['related_modes'])}")