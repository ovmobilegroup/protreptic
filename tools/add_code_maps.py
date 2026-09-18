import json

# Read existing code_maps.json
with open('/opt/data/workspace/Protreptic/tools/code_maps.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

CODE_MAP = data['CODE_MAP']
CODE_MAP_EN = data['CODE_MAP_EN']

# Add the 8 missing South Asia scenarios
# Format: "CODE": "Title/description in zh", "CODE": "Title/description in en"

# These entries should go after PK-JIN-001 (index 263 in the list)
# But since JSON doesn't guarantee order, we just add them to the dict

# CODE_MAP entries (Chinese)
CODE_MAP['PK-ISL-001'] = '真纳/巴基斯坦建国'
CODE_MAP['PK-SUF-001'] = '苏菲/信德/����普圣人'
CODE_MAP['BD-LIB-001'] = '穆吉布/孟加拉解放'
CODE_MAP['LK-CIV-001'] = '斯里兰卡内战/泰米尔'
CODE_MAP['NP-HIM-001'] = '尼��尔喜马拉雅/��尔��'
CODE_MAP['AF-TRI-001'] = '阿富��部落/杜兰线'
CODE_MAP['MV-ISL-001'] = '马尔代夫/海平面/伊斯兰'
CODE_MAP['BT-GNH-001'] = '不丹国民幸福总值'

# CODE_MAP_EN entries (English)
CODE_MAP_EN['PK-ISL-001'] = "Jinnah: Pakistan Independence/Two-Nation Theory/Islamic Constitutionalism/Muslim League/Jinnah Spirit"
CODE_MAP_EN['PK-SUF-001'] = "Sufi Saints of Sindh/Punjab: Islamic Mysticism/Spiritual Consensus/Regional Sufi Orders"
CODE_MAP_EN['BD-LIB-001'] = "Mujibur Rahman: Bangladesh Liberation/Bengali Nationalism/War of Independence/Father of the Nation"
CODE_MAP_EN['LK-CIV-001'] = "Sri Lankan Civil War/Tamil Tigers: Tamil Eelam/Self-Determination/Armed Struggle/Post-Conflict"
CODE_MAP_EN['NP-HIM-001'] = "Nepal Himalaya/Gurkha: Mountain Kingdom Unification/Highland Ecology/Gurkha Military Tradition"
CODE_MAP_EN['AF-TRI-001'] = "Afghan Tribes/Durand Line: Transnational Tribal Federation/Traditional Border/Pashtunwali Code"
CODE_MAP_EN['MV-ISL-001'] = "Maldives/Sea Level Rise/Islamic Republic: Climate Existential Diplomacy/Islamic Governance/Island Nation Survival"
CODE_MAP_EN['BT-GNH-001'] = "Bhutan GNH: Gross National Happiness/Holistic Governance/Wellbeing Metrics/Buddhist Development Model"

# Write back
data['CODE_MAP'] = CODE_MAP
data['CODE_MAP_EN'] = CODE_MAP_EN

with open('/opt/data/workspace/Protreptic/tools/code_maps.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Added 8 entries. CODE_MAP: {len(CODE_MAP)}, CODE_MAP_EN: {len(CODE_MAP_EN)}")