#!/usr/bin/env python3

import json
import os

def create_malawi_figure():
    """Create Joyce Banda figure (MW-BAN-001)"""
    
    banda_data = {
        "code": "MW-BAN-001",
        "name_zh": "班达/马拉维/终身/独裁/转型/乔伊斯/女性/哈钦斯/终身",
        "name_en": "Banda/Malawi/Lifelong_Dictatorship/Transformation/Joyce/Female/Hatchins/Lifelong",
        "core_mode": "M578 终身独裁/女性继任/民主转型/乔伊斯班达/女性总统",
        "wiki_id": "Joyce_Banda;Malawi_dictatorship;Female_politics;Third_term_issue;Africa_female_leaders",
        "nationality": "马拉维",
        "civilization_sphere": "撒哈拉以南非洲/南部非洲",
        "time_period_standardized": "1953-至今",
        "primary_language": "英语",
        "intellectual_tradition": "女性政治/独裁政治/民主转型/非洲女性领导/第三任争议/人民主义",
        "description_zh": "乔伊斯·班达（1953-至今），马拉维政治家，2012-2014年担任马拉维总统。她是马拉维第一位女总统，2004年开始担任副总统，2012年接替长期执政的总统，成为妇女领导的典范。她的任期期间，马拉维试图摆脱长期独裁，实现民主转型，但因执政时间短和受传统政治体制限制，最终下台。",
        "description_en": "Joyce Banda (1953-present), Malawian politician, served as President of Malawi from 2012 to 2014. She was Malawi's first female president, starting as Vice President in 2004. Banda took over from a long-term president in 2012, becoming a symbol of women's leadership in Africa. During her brief tenure, Malawi sought to break free from long-term dictatorship and transition to democracy, though traditional political constraints and her short time in office limited her impact.",
        "reason_zh": "班达是马拉维第一位女总统，象征着非洲女性领导的突破。她试图在长期独裁统治后实现民主转型，但执政时间短和传统政治体制的限制使她难以彻底改变马拉维的政治体制。
        "reason_en": "Banda was Malawi's first female president, symbolizing the breakthrough of women's leadership in Africa. She attempted to break free from long-term dictatorship and transition to democracy, but her short tenure and traditional political constraints limited her ability to fundamentally change Malawi's political system.",
        "modes": [578],
        "steps_zh": [
            "政治生涯开始：1953 出生/政治家庭背景/早期政治经历/政治道路的启动",
            "副总统生涯：2004 就任副总统/女性政治先驱/展示女性领导力/提升国际地位",
            "总统生涯：2012 就任总统/民主转型尝试/反独裁政策/女性领导力典范",
            "卸任：2014 卸任/政治转型尝试/影响马拉维民主发展/国际评价"
        ],
        "steps_en": [
            "Political career start: 1953 birth/political family background/early political experience/start of political career",
            "Vice presidential career: 2004 became Vice President/female political pioneer/showcased women's leadership/enhanced international status",
            "Presidential career: 2012 became President/democracy transformation attempt/dictatorship opposition/female leadership model",
            "Resignation: 2014 resigned/democracy transformation attempt/impacted Malawi's democratic development/international evaluation"
        ],
        "expected_zh": "马拉维第一位女总统，尝试实现民主转型，展示了女性在非洲政治中的领导潜力，但执政时间短和传统政治体制限制了她的改革效果。",
        "expected_en": "Malawi's first female president, attempting to achieve democratic transformation, demonstrated women's leadership potential in African politics, but short tenure and traditional political constraints limited her reform impact.",
        "case_zh": "1953 出生/1993 参议员/2004 副总统/2012 总统/2014 卸任/女性总统/马拉维民主/转型/班达/永存。",
        "case_en": "1953 birth/1993 Senator/2004 Vice President/2012 President/2014 resigned/female president/Malawi democracy/transformation/Banda/endures.",
        "era": "1953-至今",
        "historical_domains": ["政治", "社会", "经济", "性别", "民主"],
        "domains": ["协作", "系统", "分析", "创意", "运营"],
        "gender": "女",
        "ethnicity": "马拉维"
    }
    
    filename = f"/opt/data/workspace/Protreptic/{banda_data['code']}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(banda_data, f, ensure_ascii=False, indent=2)
    
    print(f"Created {filename}")
    return banda_data

if __name__ == "__main__":
    create_malawi_figure()