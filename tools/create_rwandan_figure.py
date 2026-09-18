#!/usr/bin/env python3

import json
import os

def create_rwandan_figure():
    """Create Paul Kagame figure (RW-KAG-001)"""
    
    kagame_data = {
        "code": "RW-KAG-001",
        "name_zh": "卡加梅/卢旺达/种族灭绝/重建/强人/奇迹/保罗/卡加梅",
        "name_en": "Kagame/Rwanda/Genocide/Rebuild/Strength/Miracle/Paul/Kagame",
        "core_mode": "M576 种族灭绝重建/强人发展/奇迹叙事/保罗模式/卢旺达奇迹",
        "wiki_id": "Paul_Kagame;Rwandan_genocide;Post-genocide_reconstruction;East_African;Miracle_growth",
        "nationality": "卢旺达",
        "civilization_sphere": "撒哈拉以南非洲/中非",
        "time_period_standardized": "1957-至今",
        "primary_language": "英语",
        "intellectual_tradition": "军事领导/国家重建/发展经济学/安全主义/种族和解/技术主导发展",
        "description_zh": "保罗·卡加梅（1957-至今），卢旺达总统，1994年至今在位。他是一位退休的卢旺达空军少校，在1994年胡图族图西族冲突后接管政府，实施了大胆的国家重建和经济发展政策。成功实现快速经济发展，被称为'非洲奇迹'的领导者。",
        "description_en": "Paul Kagame (1957-present), President of Rwanda, has been in power since 1994. A retired Rwandan Air Force officer, he took over after the 1994 Hutu-Tutsi conflict and implemented bold national reconstruction and economic development policies. Successfully achieved rapid economic development, he is regarded as a leader of the 'African Miracle'.",
        "reason_zh": "卡加梅是卢旺达国家重建的领导者，通过安全主义和技术主导发展实现了‘非洲奇迹’。他在后种族灭绝时期成功重建国家，成为东非最成功的执政者之一。他的发展模式体现了强人领导的效率和安全与发展的平衡。",
        "reason_en": "Kagame was the leader of Rwanda's national reconstruction, achieving the 'African Miracle' through securityism and technology-dominated development. He successfully rebuilt the nation in the post-genocide period and is one of East Africa's most successful rulers. His development model reflected the efficiency of strongman leadership and the balance between security and development.",
        "modes": [576],
        "steps_zh": [
            "卢旺达解放战争：1990-1994 卢旺达爱国阵线战争/卡加梅军事领导/推翻胡图族政府/结束种族灭绝",
            "后种族灭绝重建：1994-2000 接管政府/安全重建/种族和解/基础设施建设/国际合作",
            "经济奇迹时期：2000-2020 快速经济发展/技术主导发展/基础设施建设/吸引外国投资/成为‘非洲奇迹’",
            "长期执政：2020-至今 再次当选/继续发展政策/巩固权力/维护国家稳定/地区领导地位"
        ],
        "steps_en": [
            "Rwandan liberation war: 1990-1994 Rwandan Patriotic Front war/Kagame military leadership/overthrew Hutu government/ended genocide",
            "Post-genocide reconstruction: 1994-2000 took over government/security reconstruction/ethnic reconciliation/infrastructure construction/international cooperation",
            "Economic miracle period: 2000-2020 rapid economic development/technology-dominated development/infrastructure construction/foreign investment attraction/become 'African Miracle'",
            "Long-term rule: 2020-present re-elected/continuous development policy/consolidated power/maintained national stability/regional leadership"
        ],
        "expected_zh": "成功实现快速经济发展，被称为'非洲奇迹'。卡加梅是后种族灭绝时期卢旺达最成功的执政者之一，其发展模式为非洲国家提供了榜样。",
        "expected_en": "Successfully achieved rapid economic development, known as the 'African Miracle'. Kagame is one of Rwanda's most successful rulers in the post-genocide period, and his development model provides an example for African nations.",
        "case_zh": "1957 出生/1990 解放战争/1994 推翻政府/1994 就任总统/1999 再次当选/2005 再次当选/2020 再次当选/快速发展/非洲奇迹/卡加梅/强人领导/卢旺达复兴/永存。",
        "case_en": "1957 birth/1990 liberation war/1994 overthrew government/1994 became president/1999 re-elected/2005 re-elected/2020 re-elected/rapid development/African Miracle/Kagame/strongman leadership/Rwanda reconstruction/endures.",
        "era": "1957-至今",
        "historical_domains": ["政治", "经济", "社会", "军事", "思想"],
        "domains": ["协作", "系统", "分析", "创意", "运营"],
        "gender": "男",
        "ethnicity": "图西族"
    }
    
    filename = f"/opt/data/workspace/Protreptic/{kagame_data['code']}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(kagame_data, f, ensure_ascii=False, indent=2)
    
    print(f"Created {filename}")
    return kagame_data

if __name__ == "__main__":
    create_rwandan_figure()