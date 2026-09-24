import json, os

json_dir = "/opt/data/workspace/Protreptic/tools/json"

def write_persona(code, name_zh, name_en, desc_zh, desc_en, reason_zh, reason_en,
                  steps_zh, steps_en, expected_zh, expected_en, case_zh, case_en,
                  modes_list, nationality, civ_sphere, time_period, wiki_id,
                  primary_lang, intel_tradition, cross_impact, legacy_type,
                  legal_sys, edu_trad, sci_contrib, art_legacy, env_stew, gender_inn):
    data = {
        "code": code,
        "name_zh": name_zh,
        "name_en": name_en,
        "description_zh": desc_zh,
        "description_en": desc_en,
        "reason_zh": reason_zh,
        "reason_en": reason_en,
        "steps_zh": steps_zh,
        "steps_en": steps_en,
        "expected_zh": expected_zh,
        "expected_en": expected_en,
        "case_zh": case_zh,
        "case_en": case_en,
        "modes": modes_list,
        "nationality": nationality,
        "civilization_sphere": civ_sphere,
        "time_period_standardized": time_period,
        "wiki_id": wiki_id,
        "primary_language": primary_lang,
        "intellectual_tradition": intel_tradition,
        "cross_cultural_impact": cross_impact,
        "legacy_type": legacy_type,
        "legal_system": legal_sys,
        "education_tradition": edu_trad,
        "scientific_contribution": sci_contrib,
        "artistic_legacy": art_legacy,
        "environmental_stewardship": env_stew,
        "gender_role_innovation": gender_inn
    }
    path = os.path.join(json_dir, f"{code}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  Written: {path}")
    return path

# === M416: ZA-MAN-001 - Nelson Mandela ===
write_persona(
    "ZA-MAN-001", "\u7eb3\u5c14\u68ee\u00b7\u66fc\u5fb7\u62c9", "Nelson Mandela",
    "\u7eb3\u5c14\u68ee\u00b7\u66fc\u5fb7\u62c9\uff081918-2013\uff09\u5357\u975e\u53cd\u79cd\u65cb\u9694\u9769\u547d\u5bb6\u3001\u653f\u6cbb\u5bb6\uff0c\u9996\u4efb\u9ed1\u4eba\u603b\u7edf\uff081994-1999\uff09\uff0c\u5965\u5c14\u00b7\u5e86\u548c\u5956\u5f97\u4e3b\u3002\u4ed6\u5c06ANC\u4ece\u6b66\u88c5\u6597\u4e89\u8f6c\u5411\u771f\u76f8\u89e3\u548c\uff0c\u521b\u9020\"\u5f69\u8679\u56fd\u5bb6\"\uff0cM416\u601d\u7ef4\u6a21\u5f0f\u6700\u9ad8\u8c61\u5f81\u3002",
    "Nelson Mandela (1918-2013) South African anti-apartheid revolutionary and politician, first black president (1994-1999), Nobel Peace Prize laureate. Transformed ANC from armed struggle to truth and reconciliation, creating 'Rainbow Nation'.",
    "\u66fc\u5fb7\u62c9\u4ee3\u8868M416\u771f\u76f8\u89e3\u548c/\u5f69\u8679\u56fd\u5bb6/\u9053\u5fb7\u6743\u5a01\u300227\u5e74\u76d1\u7981\u540e\u9009\u62e9\u5bbd\u6073\uff0cTRC\u673a\u5236\u66ff\u4ee3\u590d\u62a5\uff0c\u907f\u514d\u5185\u6218\uff0c\u9053\u5fb7\u6743\u5a01\u6210\u5168\u7403\u8303\u5f0f\u3002",
    "Mandela embodies M416 Truth and Reconciliation/Rainbow Nation/Moral Authority. 27 years imprisonment followed by forgiveness over revenge, TRC replacing retribution, preventing civil war.",
    ["\u7814\u7a76\u79d1\u8428\u65cf\u90e8\u843d\u6210\u957f\u4e0eANC\u653f\u6cbb\u89c9\u9192", "\u5206\u67901964\u7f57\u672c宀\u5c9b27\u5e74\u76d1\u7981\u6218\u7565", "\u63a2\u8ba8TRC\u5bbd\u6073\u673a\u5236\u8bbe\u8ba1", "\u8bc4\u4f30'\u5f69\u8679\u56fd\u5bb6'\u5efa\u6784", "\u603b\u7ed3\u9053\u5fb7\u6743\u5a01\u5bf9\u8f6c\u578b\u6b63\u4e49\u8d21\u732e"],
    ["Study Xhosa tribal upbringing and ANC awakening", "Analyze 27 years Robben Island (1964) strategy", "Explore TRC forgiveness mechanism design", "Evaluate 'Rainbow Nation' construction", "Summarize moral authority contribution to transitional justice"],
    "\u638c\u63e1M416\u590d\u6742\u601d\u7ef4\uff0c\u5c06\u4e2a\u4eba\u521b\u4f24\u8f6c\u5316\u4e3a\u5236\u5ea6\u6027\u5bbd\u6073\u3002",
    "Master M416 complex thinking, transforming personal trauma into institutionalized forgiveness.",
    "1964\u7f57\u672c宀\u5c9b\uff1b1990\u83b7\u91ca\uff1b1993\u5965\u00b7\u5e86\u548c\u5956\uff1b1994\u9009\u4e3e\uff1b1995TRC\u3002M416\u8303\u5f0f\u3002",
    "1964 Robben Island; 1990 release; 1993 Nobel Peace; 1994 election; 1995 TRC. M416 paradigm.",
    [416, 417, 332], "South Africa", "Sub-Saharan African",
    "1918-2013", "Nelson_Mandela;African_National_Congress;Robben_Island;TRC;Rainbow_Nation",
    "Xhosa/English", "Anti-Apartheid Political Thought / Transitional Justice",
    "Truth commission; moral authority; Rainbow Nation", "political", "\u6df7\u5408\u6cd5",
    "\u897f\u65b9\u4e0e\u975e\u6d32\u878d\u5408", "\u5426", "\u6587\u5316\u8c61\u5f81", "\u5426", "\u5987\u5974\u89e3\u653e"
)

print("Done with ZA-MAN-001")