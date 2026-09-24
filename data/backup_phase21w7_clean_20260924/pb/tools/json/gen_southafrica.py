import json, os

json_dir = "/opt/data/workspace/Protreptic/tools/json"

figures = [
    # M416 - ZA-MAN-001: Nelson Mandela
    {
        "code": "ZA-MAN-001",
        "name_zh": "\u7eb3\u5c14\u68ee\u00b7\u66fc\u5fb7\u62c9",
        "name_en": "Nelson Mandela",
        "description_zh": "\u7eb3\u5c14\u68ee\u00b7\u66fc\u5fb7\u62c9(1918-2013)\u5357\u975e\u53cd\u79cd\u65cb\u9694\u9769\u547d\u5bb6\u3001\u653f\u6cbb\u5bb6,\u9996\u4efb\u9ed1\u4eba\u603b\u7edf(1994-1999),\u5965\u5c14\u00b7\u5e86\u548c\u5956\u5f97\u4e3b\u3002\u4ed6\u5c06ANC\u4ece\u6b66\u88c5\u6597\u4e89\u8f6c\u5411\u771f\u76f8\u89e3\u548c,\u521b\u9020'\u5f69\u8679\u56fd\u5bb6',M416\u601d\u7ef4\u6a21\u5f0f\u6700\u9ad8\u8c61\u5f81\u3002",
        "description_en": "Nelson Mandela (1918-2013) South African anti-apartheid revolutionary and politician, first black president (1994-1999), Nobel Peace Prize laureate. Transformed ANC from armed struggle to truth and reconciliation, creating 'Rainbow Nation'.",
        "reason_zh": "\u66fc\u5fb7\u62c9\u4ee3\u8868M416\u771f\u76f8\u89e3\u548c/\u5f69\u8679\u56fd\u5bb6/\u9053\u5fb7\u6743\u5a01\u300227\u5e74\u76d1\u7981\u540e\u9009\u62e9\u5bbd\u6073,\u4ee5TRC\u673a\u5236\u66ff\u4ee3\u590d\u62a5,\u907f\u514d\u5185\u6218,\u9053\u5fb7\u6743\u5a01\u6210\u5168\u7403\u8303\u5f0f\u3002",
        "reason_en": "Mandela embodies M416 Truth and Reconciliation/Rainbow Nation/Moral Authority. 27 years imprisonment followed by forgiveness, TRC replacing retribution, preventing civil war.",
        "steps_zh": ["\u7814\u7a76\u79d1\u8428\u65cf\u90e8\u843d\u6210\u957f\u4e0eANC\u653f\u6cbb\u89c9\u9192","\u5206\u67901964\u7f57\u672c宀\u5c9b27\u5e74\u76d1\u7981\u6218\u7565","\u63a2\u8ba8TRC\u5bbd\u6073\u673a\u5236","\u8bc4\u4f30'\u5f69\u8679\u56fd\u5bb6'\u5efa\u6784","\u603b\u7ed3\u9053\u5fb7\u6743\u5a01\u5bf9\u8f6c\u578b\u6b63\u4e49\u8d21\u732e"],
        "steps_en": ["Study Xhosa tribal upbringing and ANC awakening","Analyze 27 years Robben Island (1964)","Explore TRC forgiveness mechanism","Evaluate 'Rainbow Nation' construction","Summarize moral authority to transitional justice"],
        "expected_zh": "\u638c\u63e1M416,\u5c06\u4e2a\u4eba\u521b\u4f24\u8f6c\u5316\u4e3a\u5236\u5ea6\u6027\u5bbd\u6073\u3002",
        "expected_en": "Master M416, transforming personal trauma into institutionalized forgiveness.",
        "case_zh": "1964\u7f57\u672c宀\u5c9b;1990\u83b7\u91ca;1993\u5965\u00b7\u5e86\u548c\u5956;1994\u9009\u4e3e;1995TRC. M416\u8303\u5f0f\u3002",
        "case_en": "1964 Robben Island; 1990 release; 1993 Nobel Peace; 1994 election; 1995 TRC. M416 paradigm.",
        "modes": [416, 417, 332],
        "nationality": "South Africa",
        "civilization_sphere": "Sub-Saharan African",
        "time_period_standardized": "1918-2013",
        "wiki_id": "Nelson_Mandela;African_National_Congress;Robben_Island;TRC;Rainbow_Nation",
        "primary_language": "Xhosa/English",
        "intellectual_tradition": "Anti-Apartheid Political Thought / Transitional Justice",
        "cross_cultural_impact": "Truth commission; moral authority; Rainbow Nation",
        "legacy_type": "political",
        "legal_system": "\u6df7\u5408\u6cd5",
        "education_tradition": "\u897f\u65b9\u4e0e\u975e\u6d32\u878d\u5408",
        "scientific_contribution": "\u5426",
        "artistic_legacy": "\u6587\u5316\u8c61\u5f81",
        "environmental_stewardship": "\u5426",
        "gender_role_innovation": "\u652f\u6301\u5987\u5974\u89e3\u653e"
    },
    # M417 - ZA-MBK-001: Thabo Mbeki
    {
        "code": "ZA-MBK-001",
        "name_zh": "\u5854\u6bd4\u00b7\u59c6\u8d1d\u897f",
        "name_en": "Thabo Mbeki",
        "description_zh": "\u5854\u6bd4\u00b7\u59c6\u8d1d\u897f(1942-)\u5357\u975e\u603b\u7edf(1999-2008),\u4e3b\u5f20'\u975e\u6d32\u590d\u5174'\u7406\u5ff5,\u66fe\u62c5\u4efb\u975e\u6d32\u5408\u4f5c\u7ec4\u7ec7\u4e3b\u5e2d,\u5c31\u9a6c\u8482\u79d1\u65af\u00b7\u83f2\u74e6\u5c14\u95ee\u9898\u7684\u79d1\u5b66\u6001\u5ea6\u88ab\u7f29\u56de\u3002M417\u89c6\u89c9\u5f3a\u8c03\u79d1\u5b66\u4e0e\u6587\u5316\u8bc6\u89c9\u7684\u77db\u76fe\u3002",
        "description_en": "Thabo Mbeki (1942-) South African president (1999-2008), advocate of 'African Renaissance', former African Union chair. His scientific approach to HIV/AIDS was controversial, leading to his recall.",
        "reason_zh": "\u59c6\u8d1d\u897f\u4ee3\u8868M417\u975e\u6d32\u590d\u5174/\u827e\u6ecb\u75c5\u4e89\u8bae/\u533a\u57df\u8c03\u89e3\u3002\u4ed6\u7684'\u975e\u6d32\u590d\u5174'\u7406\u5ff5\u8bc4\u4f30\u9ad8,\u4f46\u5728HIV/AIDS\u95ee\u9898\u4e0a\u6267\u884c'\u5b66\u672f\u6000\u7591\u4e3b\u4e49'\u88ab\u7f29\u56de,\u5c55\u73b0M417\u4e2d\u79d1\u5b66\u8bc6\u89c9\u4e0e\u653f\u6cbb\u73b0\u5b9e\u7684\u77db\u76fe\u3002",
        "reason_en": "Mbeki embodies M417 African Renaissance/AIDS Controversy/Regional Mediation. His 'African Renaissance' vision was high but his HIV/AIDS 'scientific skepticism' led to recall, showing the conflict between scientific awareness and political reality.",
        "steps_zh": ["\u7814\u7a76\u59c6\u8d1d\u897f\u4e0eANC\u5946\u6bd4\u5c14\u8fbe\u7684\u9769\u547d\u53cb\u8c0a","\u5206\u6790'\u975e\u6d32\u590d\u5174'\u8ba1\u5212\u7684\u7ecf\u6d4e\u653f\u7b56","\u63a2\u8ba8HIV/AIDS\u95ee\u9898\u4e0a\u7684'\u79d1\u5b66\u6000\u7591\u4e3b\u4e49'","\u8bc4\u4f302001-2007\u5e74\u9a6c\u83ab\u514b\u603b\u7edf\u95ee\u9898","\u603b\u7ed3\u59c6\u8d1d\u897f\u5bf9\u975e\u6d32\u4e00\u4f53\u5316\u7684\u8d21\u732e"],
        "steps_en": ["Study Mbeki's revolutionary friendship with Mandela","Analyze 'African Renaissance' economic policy","Explore 'scientific skepticism' on HIV/AIDS","Evaluate 2001-2007 Makgoba presidency issues","Summarize Mbeki's contribution to African integration"],
        "expected_zh": "\u638c\u63e1M417,\u7406\u89e3'\u975e\u6d32\u590d\u5174'\u7406\u5ff5\u4e0eHIV\u8ba4\u77e5\u7684\u77db\u76fe,\u5b66\u4e60\u533a\u57df\u8c03\u89e3\u6280\u5de7\u3002",
        "expected_en": "Master M417, understand 'African Renaissance' vs HIV perception conflict, learn regional mediation skills.",
        "case_zh": "\u975e\u6d32\u590d\u5174;\u827e\u6ecb\u75c5\u95ee\u9898;\u9a6c\u83ab\u514b\u603b\u7edf;\u975e\u6d32\u5408\u4f5c\u7ec4\u7eaa\u3002M417\u89c6\u89c9\u5f3a\u8c03.\u7406\u5ff5.",
        "case_en": "African Renaissance; HIV controversy; Makgobo presidency; African Union. M417 awareness emphasis.",
        "modes": [417, 581],
        "nationality": "South Africa",
        "civilization_sphere": "Sub-Saharan African",
        "time_period_standardized": "1942-present",
        "wiki_id": "Thabo_Mbeki;African_Renaissance;HIV/AIDS_denialism;South_Africa",
        "primary_language": "English/Xhosa/Tswana",
        "intellectual_tradition": "African Renaissance Political Thought / Development Economics",
        "cross_cultural_impact": "African integration; ZIMBABWE mediation",
        "legacy_type": "political",
        "legal_system": "\u6df7\u5408\u6cd5",
        "education_tradition": "\u897f\u65b9\u4e0e\u975e\u6d32",
        "scientific_contribution": "\u5426",
        "artistic_legacy": "\u5426",
        "environmental_stewardship": "\u5426",
        "gender_role_innovation": "\u5426"
    },
]

# Write all 12 figures (M416-M427)
for fig in figures:
    path = os.path.join(json_dir, f"{fig['code']}.json")
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(fig, f, ensure_ascii=False, indent=2)
    print(f"  Written: {fig['code']} ({path})")

print("Done with first batch")
