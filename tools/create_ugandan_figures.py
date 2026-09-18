#!/usr/bin/env python3

import json
import os

def create_ugandan_figures():
    """Create Milton Obote and Idi Amin figures (UG-OBO-001, UG-MUS-001)"""
    
    # Milton Obote (UG-OBO-001)
    obote_data = {
        "code": "UG-OBO-001",
        "name_zh": "奥博特/乌干达/独裁/阿敏/战争/米尔顿/阿波罗/穆塞韦尼",
        "name_en": "Obote/Uganda/Dictatorship/Amin/War/Milton/Apollo/Museveni",
        "core_mode": "M574 后殖民独裁循环/阿敏/长期战争/米尔顿统治",
        "wiki_id": "Milton_Obote;Idi_Amin;Uganda_independence;East_African;War",
        "nationality": "乌干达",
        "civilization_sphere": "撒哈拉以南非洲/东非",
        "time_period_standardized": "1925-2013",
        "primary_language": "英语",
        "intellectual_tradition": "后殖民政治/独裁主义/非洲民族主义/东非政治/帝国主义遗产",
        "description_zh": "米尔顿·阿波罗·奥博特（1925-2013），乌干达政治家，1962年-1966年和1980-1985年担任乌干达总理。他领导乌干达独立，建立了一党制乌干达人民议会党，倡导泛非主义和非洲社会主义。后因阿明独裁政权被推翻，1980年重新执政，但长期的独裁循环和与伊迪·阿明的战争导致乌干达持续动荡。",
        "description_en": "Milton Apollo Obote (1925-2013), Ugandan politician, served as Prime Minister of Uganda from 1962 to 1966 and from 1980 to 1985. He led Uganda's independence, established the one-party Uganda Peoples Congress, advocated Pan-Africanism and African socialism. Later due to Idi Amin's dictatorship, he was overthrown, returned to power in 1980, but the long-term dictatorship cycle and war with Idi Amin caused continued turmoil in Uganda.",
        "reason_zh": "奥博特是乌干达独立和建国的重要领导人，但长期的独裁统治和与阿明政权的战争，体现了东非国家后殖民时期的独裁循环和政治动荡。他的统治反映了帝国主义遗产和非洲民族主义的复杂性。",
        "reason_en": "Obote was an important leader of Uganda's independence and nation-building, but long-term dictatorship and war with Idi Amin's regime reflected the dictatorship cycle and political turmoil in post-colonial East Africa. His rule reflected the complexity of imperialist legacy and African nationalism.",
        "modes": [574],
        "steps_zh": [
            "乌干达独立运动建立：1952年乌干达民族联盟建立/奥博特领导独立斗争/奠定乌干达独立基础",
            "一党制建国：1962年乌干达独立/建立乌干达人民议会党/建立一党制政治体系/巩固权力",
            "独裁政权建立：1966-1966年总统权力巩固/建立独裁政权/镇压反对派/控制国家",
            "与阿明战争：1971-1979年伊迪·阿明政变/奥博特领导反阿明斗争/乌干达长期战争/持续动荡"
        ],
        "steps_en": [
            "Uganda independence movement establishment: 1952 Uganda National Congress established/Obote led independence struggle/foundations laid for Uganda independence",
            "One-party state establishment: 1962 Uganda independence/established Uganda Peoples Congress/one-party political system/consolidated power",
            "Dictatorship establishment: 1966-1966 President power consolidation/established dictatorship/repressed opposition/controlled country",
            "War with Idi Amin: 1971-1979 Idi Amin coup/Obote led anti-Amin struggle/Uganda long-term war/continued turmoil"
        ],
        "expected_zh": "建立乌干达独立和一党制政治体系，但长期独裁和战争反映了后殖民时期的政治动荡和帝国主义遗产的复杂性。",
        "expected_en": "Establishing Uganda's independence and one-party political system, but long-term dictatorship and war reflected the political turmoil and complexity of imperialist legacy in post-colonial period.",
        "case_zh": "1925 出生/1952 成立民族联盟/1962 乌干达独立/1966 建立独裁政权/1971 阿明政变/1985 重新执政/1979 卸任/独裁战争/乌干达动荡/奥博特/永存。",
        "case_en": "1925 birth/1952 Uganda National Congress established/1962 Uganda independence/1966 established dictatorship/1971 Idi Amin coup/1985 returned to power/1979 resigned/dictatorship war/Uganda turmoil/Obote/endures.",
        "era": "1925-2013",
        "historical_domains": ["政治", "军事", "社会", "经济", "思想"],
        "domains": ["协作", "系统", "分析", "创意", "运营"],
        "gender": "男",
        "ethnicity": "乌干达"
    }
    
    # Idi Amin (UG-MUS-001)
    amin_data = {
        "code": "UG-MUS-001",
        "name_zh": "穆塞韦尼/乌干达/游击/长期/反同/东非共同体/约韦里/长期",
        "name_en": "Museveni/Uganda/Guerrilla/Long-term/Homophobia/EASTAFRICANCOMMUNITY/Yoweri/Long-term",
        "core_mode": "M575 游击长期/反同性恋/区域霸权/长期统治/约韦里",
        "wiki_id": "Idi_Amin;Yoweri_Museveni;Uganda_NRM;Dictatorship;East_African_Community",
        "nationality": "乌干达",
        "civilization_sphere": "撒哈拉以南非洲/东非",
        "time_period_standardized": "1941-至今",
        "primary_language": "英语",
        "intellectual_tradition": "军事政权/民族主义/反帝国主义/东非政治/恐怖统治/经济掠夺",
        "description_zh": "伊迪·阿明（1941-至今），乌干达前总统，1971-1979年在位。他曾是一名逃兵，后通过政变上台，建立极权独裁政权，以残暴和反犹太主义闻名。长期统治期间，乌干达经济崩溃，人权状况极度恶化。1990年后转为民主政治，但早期独裁统治对乌干达造成了深远影响。",
        "description_en": "Idi Amin (1941-present), former President of Uganda, ruled from 1971 to 1979. He was a former soldier who staged a coup d'état and established a repressive dictatorship. Known for brutality and anti-Semitism, his 8-year rule saw the collapse of Uganda's economy and severe human rights abuses. Though Uganda returned to democracy after 1990, his early dictatorship left deep scars on the nation.",
        "reason_zh": "阿明是乌干达历史上最残暴的独裁者之一，其统治体现了后殖民时期的政治腐败和军事政权的极端性。他长期执政，造成了巨大的人道主义灾难，对东非政治产生了深远影响。",
        "reason_en": "Amin was one of Uganda's most brutal dictators, his rule embodied the extreme nature of post-colonial political corruption and military regimes. His long-term dictatorship caused huge humanitarian disasters and had profound impact on East African politics.",
        "modes": [575],
        "steps_zh": [
            "逃兵生涯：1950-1960 加入乌干达军队/政治动荡时期/逃兵生涯/军事生涯开始",
            "政变上台：1971 乌干达政变/阿明领导政变/建立独裁政权/开始残暴统治",
            "恐怖统治时期：1971-1979 长期独裁/残暴统治/镇压反对派/经济崩溃/人权灾难",
            "过渡到民主：1990-1992 国际压力/内部反对/过渡到民主/民主政治重建/经济恢复"
        ],
        "steps_en": [
            "Soldier career: 1950-1960 joined Uganda military/political turmoil period/soldier career/military career start",
            "Coup d'état rise: 1971 Uganda coup d'état/Amin led coup established dictatorship/began brutal rule",
            "Terror rule period: 1971-1979 long-term dictatorship/brutal rule/repressed opposition/economic collapse/humanitarian disaster",
            "Transition to democracy: 1990-1992 international pressure/internal opposition/transition to democracy/democratic political reconstruction/economic recovery"
        ],
        "expected_zh": "建立极端独裁政权，造成巨大的人道主义灾难，但最终被国际压力和内部反对所推翻，乌干达走向民主。",
        "expected_en": "Established extreme dictatorship, caused huge humanitarian disasters, but was overthrown by international pressure and internal opposition, Uganda moved toward democracy.",
        "case_zh": "1941 出生/1971 政变上台/1971-1979 恐怖统治/1979 被推翻/1986 过渡到民主/恐怖统治/独裁政权/永存/影响深远/穆塞韦尼/永存。",
        "case_en": "1941 birth/1971 coup d'état rise/1971-1979 terror rule/1979 overthrown/1986 transition to democracy/terror rule/dictatorship/endures/profound impact/Museveni/endures.",
        "era": "1941-至今",
        "historical_domains": ["政治", "军事", "社会", "经济", "人权"],
        "domains": ["协作", "系统", "分析", "创意", "运营"],
        "gender": "男",
        "ethnicity": "乌干达"
    }
    
    # Write files
    for data in [obote_data, amin_data]:
        filename = f"/opt/data/workspace/Protreptic/{data['code']}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Created {filename}")
    
    return [obote_data, amin_data]

if __name__ == "__main__":
    create_ugandan_figures()