#!/usr/bin/env python3

import json
import os

def create_burundi_figure():
    """Create Pierre Nkurunziza figure (BI-NKU-001)"""
    
    nkurunziza_data = {
        "code": "BI-NKU-001",
        "name_zh": "恩库伦齐扎/布隆迪/内战/跑步/第三任/东非/皮埃尔/恩库伦齐扎",
        "name_en": "Nkurunziza/Burundi/Civil_War/Third_Term/East_African/Pierre/Nkurunziza",
        "core_mode": "M577 内战跑步总统/第三任危机/东非一体化/跑步外交",
        "wiki_id": "Pierre_Nkurunziza;Burundi_civil_war;East_African_community;Third_term_presidency",
        "nationality": "布隆迪",
        "civilization_sphere": "撒哈拉以南非洲/中非",
        "time_period_standardized": "1964-2020",
        "primary_language": "法语/基富拉语",
        "intellectual_tradition": "宗教政治/总统主义/非洲民族主义/东非政治/第三任争议/和平外交/体育外交",
        "description_zh": "皮埃尔·恩库伦齐扎（1964-2020），布隆迪政治家，2005-2020年担任布隆迪总统。他是一位牧师出身的政治家，通过体育和跑步被誉为'跑步总统'。在任期间，布隆迪结束了长期的内战，实现了政治稳定，但第三任任期引发争议。",
        "description_en": "Pierre Nkurunziza (1964-2020), Burundian politician, served as President of Burundi from 2005 to 2020. A pastor-turned-politician, he was known as 'President of the Running' due to his passion for sports and running. During his tenure, Burundi ended long-term civil war and achieved political stability, but his third-term candidacy sparked controversy.",
        "reason_zh": "恩库伦齐扎是布隆迪结束内战的领导者，通过宗教政治和体育外交实现了国家统一。他的'跑步总统'形象成为和平外交的象征，但第三任任期引发了政治争议。",
        "reason_en": "Nkurunziza was the leader who ended Burundi's civil war, achieving national unity through religious politics and sports diplomacy. His 'running president' image became a symbol of peaceful diplomacy, but his third-term candidacy sparked political controversy.",
        "modes": [577],
        "steps_zh": [
            "宗教政治生涯：1964-1993 牧师生涯/宗教教育/政治生涯开始/宗教政治背景",
            "政治崛起：1993-2005 参议院议员/政治斗争/总统候选人/政治崛起",
            "总统生涯：2005-2010 就任总统/结束内战/国家重建/体育外交/跑步总统",
            "第三任任期：2010-2020 连任总统/第三任任期争议/政治稳定/东非领导/国际地位提升"
        ],
        "steps_en": [
            "Religious political career: 1964-1993 Pastor career/religious education/political career start/religious political background",
            "Political rise: 1993-2005 Senator/political struggle/presidential candidate/political rise",
            "Presidential career: 2005-2010 became President/ended civil war/national reconstruction/sports diplomacy/running president",
            "Third term: 2010-2020 re-elected President/third term controversy/political stability/East African leadership/international status enhancement"
        ],
        "expected_zh": "结束布隆迪长期内战，实现国家统一和稳定。恩库伦齐扎的'跑步总统'形象成为和平外交的象征，但第三任任期引发了政治争议。",
        "expected_en": "Ended Burundi's long-term civil war, achieving national unity and stability. Nkurunziza's 'running president' image became a symbol of peaceful diplomacy, but his third-term candidacy sparked political controversy.",
        "case_zh": "1964 出生/1964 宗教教育/1993 参议院/2005 就任总统/2010 连任/2020 卸任/结束内战/跑步总统/布隆迪重建/永存。",
        "case_en": "1964 birth/1964 religious education/1993 Senator/2005 became President/2010 re-elected/2020 resigned/ended civil war/running president/Burundi reconstruction/endures.",
        "era": "1964-2020",
        "historical_domains": ["政治", "社会", "经济", "宗教", "体育"],
        "domains": ["协作", "系统", "分析", "创意", "运营"],
        "gender": "男",
        "ethnicity": "布隆迪"
    }
    
    filename = f"/opt/data/workspace/Protreptic/{nkurunziza_data['code']}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(nkurunziza_data, f, ensure_ascii=False, indent=2)
    
    print(f"Created {filename}")
    return nkurunziza_data

if __name__ == "__main__":
    create_burundi_figure()