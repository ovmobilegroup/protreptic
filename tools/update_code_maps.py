import json

# Load existing scenarios
with open('scenarios_zh.json', 'r', encoding='utf-8') as f:
    scenarios_zh = json.load(f)

with open('scenarios_en.json', 'r', encoding='utf-8') as f:
    scenarios_en = json.load(f)

# Update CODE_MAP with new historical figure codes
code_map_zh = {
    "A-1-X-P": "复杂战略决策", "A-1-X-R": "长期战略布局", "A-1-Y-P": "商业竞争",
    "A-1-Y-S": "市场调研", "A-1-Y-Q": "制度设计", "A-2-X-P": "投资决策",
    "A-2-Y-P": "谈判博弈", "A-2-Y-R": "长期竞争（资源紧）", "A-3-Y-R": "劣势突围",
    "B-1-Y-S": "创新突破", "B-2-Y-S": "技术攻坚", "B-1-Z-S": "产品快速迭代",
    "C-1-Y-P": "团队建设", "C-2-Y-P": "领导力提升", "C-2-Z-P": "冲突调解",
    "C-3-Y-S": "人际关系", "D-1-Y-R": "个人成长规划", "D-2-Y-R": "组织能力建设",
    "D-2-Z-P": "危机应对", "D-3-Z-P": "生死存亡",
    # New historical figures
    "H-LB-01": "刘邦：开国皇帝的格局授权",
    "H-LX-02": "刘秀：光武中兴的务实求真",
    "H-LS-03": "李世民：贞观之治的系统思维",
    "H-ZK-04": "赵匡胤：杯酒释兵权的制度化制衡",
    "H-CJ-05": "成吉思汗：唯才是举与信息流速",
    "H-ZY-06": "朱元璋：极致风控与权力集中",
    "H-HT-07": "皇太极：二代接班的战略转型",
    "H-ZL-08": "诸葛亮：系统工程师的系统思维",
    "H-SY-09": "司马懿：蛰伏积势的弱者生存法则",
    "H-ZG-10": "曾国藩：笨功夫与复利思维极致",
    "H-WY-11": "王阳明：知行合一与致良知",
    "H-SZ-12": "孙中山：三民主义与体系化纲领",
    "H-LB-13": "林彪：集中指挥与运动歼灭",
    "H-CY-14": "陈云：鸟笼经济与边界思维",
    "H-LB-15": "刘备：人心收买与利益捆绑",
    "H-DX-16": "邓小平：摸石头过河的实验主义",
    "H-LB-17": "刘备：团队建设的仁义立身",
}

code_map_en = {
    "A-1-X-P": "Complex Strategic Decision", "A-1-X-R": "Long-term Strategic Layout",
    "A-1-Y-P": "Business Competition", "A-1-Y-S": "Market Research",
    "A-1-Y-Q": "Institution Design", "A-2-X-P": "Investment Decision",
    "A-2-Y-P": "Negotiation", "A-2-Y-R": "Long-term Competition (Resources Tight)",
    "A-3-Y-R": "Breakout from Disadvantage", "B-1-Y-S": "Innovation Breakthrough",
    "B-2-Y-S": "Technical Breakthrough", "B-1-Z-S": "Product Rapid Iteration",
    "C-1-Y-P": "Team Building", "C-2-Y-P": "Leadership Development",
    "C-2-Z-P": "Conflict Mediation", "C-3-Y-S": "Interpersonal Relations",
    "D-1-Y-R": "Personal Growth Planning", "D-2-Y-R": "Organizational Capability Building",
    "D-2-Z-P": "Crisis Response", "D-3-Z-P": "Survival Crisis",
    # New historical figures
    "H-LB-01": "Liu Bang: Emperor's Delegation Mastery",
    "H-LX-02": "Liu Xiu: Pragmatic Restoration",
    "H-LS-03": "Li Shimin: Systematic Zhenguan Governance",
    "H-ZK-04": "Zhao Kuangyin: Institutional Checks via Wine Banquet",
    "H-CJ-05": "Genghis Khan: Meritocracy & Info Velocity",
    "H-ZY-06": "Zhu Yuanzhang: Extreme Risk Control",
    "H-HT-07": "Huang Taiji: Strategic Succession Pivot",
    "H-ZL-08": "Zhuge Liang: Systems Engineer Thinking",
    "H-SY-09": "Sima Yi: Dormant Accumulation Survival",
    "H-ZG-10": "Zeng Guofan: Compound Diligence",
    "H-WY-11": "Wang Yangming: Unity of Knowledge & Action",
    "H-SZ-12": "Sun Yat-sen: Three Principles System",
    "H-LB-13": "Lin Biao: Concentrated Command & Mobile Warfare",
    "H-CY-14": "Chen Yun: Birdcage Economy",
    "H-LB-15": "Liu Bei: Hearts & Minds Alignment",
    "H-DX-16": "Deng Xiaoping: Crossing River by Feeling Stones",
    "H-LB-17": "Liu Bei: Team Building via Benevolence",
}

# Save code maps
with open('code_maps.json', 'w', encoding='utf-8') as f:
    json.dump({"CODE_MAP": code_map_zh, "CODE_MAP_EN": code_map_en}, f, ensure_ascii=False, indent=2)

print("Code maps saved!")
print(f"CODE_MAP ZH: {len(code_map_zh)} entries")
print(f"CODE_MAP EN: {len(code_map_en)} entries")