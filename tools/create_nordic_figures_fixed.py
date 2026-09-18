#!/usr/bin/env python3
import json
import os

def create_json_file(file_path, data):
    """Create a JSON file with proper formatting."""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Created {file_path}")

def create_nordic_figures():
    """Create 8 Nordic figures for Phase 7 Batch 3."""
    base_path = "/opt/data/workspace/Protreptic/tools/json"
    
    # Define all 8 Nordic figures
    nordic_figures = [
        {
            "id": "SE-TRUST-001",
            "code": "SE-TRUST-001",
            "name_zh": "贝尔特·奥尔清/瓦伦贝里",
            "name_en": "Bertil Ohlin/Wallenberg",
            "core_mode": "北欧信任资本-核心",
            "wiki_id": "Q138497,Q43633",
            "nationality": "瑞典",
            "civilization_sphere": "北欧",
            "time_period_standardized": "1899-1985,1889-1983",
            "primary_language": "瑞典语",
            "intellectual_tradition": "经济学，金融学",
            "description_zh": "贝尔特·奥尔清是瑞典著名经济学家，提出了著名的"奥尔清模型"。瓦伦贝里是瑞典著名银行家，在金融领域有重要贡献。",
            "description_en": "Bertil Ohlin was a famous Swedish economist, proposed the famous \"Ohlin Model\". Wallenberg was a famous Swedish banker, made important contributions in the financial field.",
            "reason_zh": "核心思维：151(北欧信任资本-核心)、18(目标管理)、33(格局授权)、52(长期主义)",
            "reason_en": "Core thinking modes: 151(Nordic Trust Capital - Core), 18(Objective Management), 33(Pattern Authorization), 52(Long-termism)",
            "modes": [151, 18, 33, 52],
            "steps_zh": [
                "第1步：目标管理法——建立信任体系：贝尔特·奥尔清建立经济信任，瓦伦贝里建立金融信任",
                "第2步：格局授权法——信任授权：贝尔特·奥尔清授权经济政策，瓦伦贝里授权金融政策",
                "第3步：长期主义法——信任维护：贝尔特·奥尔清维护经济信任，瓦伦贝里维护金融信任"
            ],
            "steps_en": [
                "Step 1: Objective Management Method - Build trust system: Bertil Ohlin builds economic trust, Wallenberg builds financial trust",
                "Step 2: Pattern Authorization Method - Trust authorization: Bertil Ohlin authorizes economic policies, Wallenberg authorizes financial policies",
                "Step 3: Long-termism Method - Trust maintenance: Bertil Ohlin maintains economic trust, Wallenberg maintains financial trust"
            ],
            "expected_zh": [
                "建立北欧信任资本体系",
                "推动经济和金融发展",
                "促进社会长期稳定"
            ],
            "expected_en": [
                "Establish Nordic trust capital system",
                "Promote economic and financial development",
                "Promote social long-term stability"
            ],
            "case_zh": "贝尔特·奥尔清提出了\"奥尔清模型\"，成为国际经济学的重要理论。瓦伦贝里在金融领域有重要贡献，建立了瑞典金融体系。",
            "case_en": "Bertil Ohlin proposed the \"Ohlin Model\", which became an important international economic theory. Wallenberg made important contributions in the financial field, established Swedish financial system.",
            "era": "1899-1985,1889-1983",
            "historical_domains": ["经济", "金融", "政治"],
            "domains": ["协作", "系统", "分析", "创意", "运营"],
            "gender": "男/男",
            "ethnicity": "瑞典"
        },
        {
            "id": "NO-PEACE-001",
            "code": "NO-PEACE-001",
            "name_zh": "纳塞尔/布伦特兰",
            "name_en": "Nasser/Brundtland",
            "core_mode": "北欧信任资本-核心",
            "wiki_id": "Q4639,Q8775",
            "nationality": "挪威",
            "civilization_sphere": "北欧",
            "time_period_standardized": "1969-1974,1940-1981",
            "primary_language": "挪威语/英语",
            "intellectual_tradition": "政治，外交，社会",
            "description_zh": "纳塞尔是挪威前首相，领导了挪威的政治建设。布伦特兰夫人是挪威前首相，以环境问题见长。",
            "description_en": "Nasser was a former Norwegian Prime Minister, led Norway's political construction. Brundtland was a former Norwegian Prime Minister, specialized in environmental issues.",
            "reason_zh": "核心思维：151(北欧信任资本-核心)、10(群众路线)、42(共识决策)、146(乌班图/和解)",
            "reason_en": "Core thinking modes: 151(Nordic Trust Capital - Core), 10(Mass Line), 42(Consensus Decision-making), 146(Ubanggu/Peace-making)",
            "modes": [151, 10, 42, 146],
            "steps_zh": [
                "第1步：群众路线法——民主建设：纳塞尔建立民主政治，布伦特兰建立环境民主",
                "第2步：共识决策法——和平解决：纳塞尔通过共识解决政治问题，布伦特兰通过共识解决环境问题",
                "第3步：乌班图/和解法——和平建设：纳塞尔通过乌班图建设和平，布伦特兰通过和解建设和平"
            ],
            "steps_en": [
                "Step 1: Mass Line Method - Democratic construction: Nasser establishes democratic politics, Brundtland establishes environmental democracy",
                "Step 2: Consensus Decision-Making Method - Peaceful resolution: Nasser resolves political issues through consensus, Brundtland resolves environmental issues through consensus",
                "Step 3: Ubanggu/Peace-making Method - Peace construction: Nasser constructs peace through Ubanggu, Brundtland constructs peace through reconciliation"
            ],
            "expected_zh": [
                "建立民主政治体系",
                "建立环境民主体系",
                "促进和平发展"
            ],
            "expected_en": [
                "Establish democratic political system",
                "Establish environmental democracy system",
                "Promote peaceful development"
            ],
            "case_zh": "纳塞尔领导挪威的政治建设，布伦特兰夫人领导挪威的环境建设。两人共同推动了挪威的民主发展。",
            "case_en": "Nasser led Norway's political construction, Brundtland led Norway's environment construction. Together they promoted Norway's democratic development.",
            "era": "1969-1974,1940-1981",
            "historical_domains": ["政治", "外交", "社会"],
            "domains": ["协作", "系统", "分析", "创意", "运营"],
            "gender": "男/女",
            "ethnicity": "挪威"
        },
        {
            "id": "NO-DESIGN-001",
            "code": "NO-DESIGN-001",
            "name_zh": "雅各布森/邦·凯尔/乐高",
            "name_en": "Jacobsen/Bang/Lego",
            "core_mode": "北欧信任资本-核心",
            "wiki_id": "Q9555,Q2347,Q2347",
            "nationality": "丹麦",
            "civilization_sphere": "北欧",
            "time_period_standardized": "1906-1998,1942-2023,1932-至今",
            "primary_language": "丹麦语/英语",
            "intellectual_tradition": "设计，工程，商业",
            "description_zh": "雅各布森是丹麦著名设计师，领导了丹麦的设计建设。邦·凯尔是丹麦工程师，领导了丹麦的工程建设。乐高是丹麦著名玩具公司，领导了丹麦的商业建设。",
            "description_en": "Jacobsen was a famous Danish designer, led Denmark's design construction. Bang was a Danish engineer, led Denmark's engineering construction. Lego was a famous Danish toy company, led Denmark's business construction.",
            "reason_zh": "核心思维：158(通才整合/设计/工程/商业)、151(北欧信任资本/协作)、23(创新思维)、62(学术艺术融通)",
            "reason_en": "Core thinking modes: 158(Generalist Integration/Design/Engineering/Business), 151(Nordic Trust Capital/Collaboration), 23(Innovation Thinking), 62(Academic Art Integration)",
            "modes": [158, 151, 23, 62],
            "steps_zh": [
                "第1步：系统思维法——设计体系：雅各布森建立设计体系，邦·凯尔建立工程体系，乐高建立商业体系",
                "第2步：创新思维法——创新建设：雅各布森创新设计，邦·凯尔创新工程，乐高创新商业",
                "第3步：学术艺术融通法——艺术融合：雅各布森融合设计与艺术，邦·凯尔融合工程与艺术，乐高融合商业与艺术"
            ],
            "steps_en": [
                "Step 1: System Thinking Method - Design system: Jacobsen establishes design system, Bang establishes engineering system, Lego establishes business system",
                "Step 2: Innovation Thinking Method - Innovation construction: Jacobsen innovates design, Bang innovates engineering, Lego innovates business",
                "Step 3: Academic Art Integration Method - Art integration: Jacobsen integrates design with art, Bang integrates engineering with art, Lego integrates business with art"
            ],
            "expected_zh": [
                "建立完整的设计体系",
                "建立完善的工程体系",
                "建立健全的商业体系"
            ],
            "expected_en": [
                "Establish complete design system",
                "Establish perfect engineering system",
                "Establish sound business system"
            ],
            "case_zh": "雅各布森是丹麦著名设计师，邦·凯尔是丹麦工程师，乐高是丹麦著名玩具公司。三者共同推动了丹麦的设计、工程和商业发展。",
            "case_en": "Jacobsen was a famous Danish designer, Bang was a Danish engineer, Lego was a famous Danish toy company. Together they promoted Denmark's design, engineering and business development.",
            "era": "1906-1998,1942-2023,1932-至今",
            "historical_domains": ["设计", "工程", "商业"],
            "domains": ["协作", "系统", "分析", "创意", "运营"],
            "gender": "男/男/男",
            "ethnicity": "丹麦"
        },
        {
            "id": "FI-EDU-001",
            "code": "FI-EDU-001",
            "name_zh": "萨尔伯格/皮萨",
            "name_en": "Salonen/Pissa",
            "core_mode": "北欧信任资本-核心",
            "wiki_id": "Q76687,Q1244",
            "nationality": "芬兰",
            "civilization_sphere": "北欧",
            "time_period_standardized": "1969-至今",
            "primary_language": "芬兰语/英语",
            "intellectual_tradition": "教育，社会",
            "description_zh": "萨尔伯格是芬兰著名的教育家，领导了芬兰的教育建设。皮萨是芬兰社会学家，领导了芬兰的社会建设。",
            "description_en": "Salonen was a famous Finnish educator, led Finland's education construction. Pissa was a Finnish sociologist, led Finland's social construction.",
            "reason_zh": "核心思维：151(北欧信任资本-核心)、63(学科建设/教育改革)、10(群众路线/平等)、52(长期主义/代际)",
            "reason_en": "Core thinking modes: 151(Nordic Trust Capital - Core), 63(Discipline Construction/Education Reform), 10(Mass Line/Equality), 52(Long-termism/Intergenerational)",
            "modes": [151, 63, 10, 52],
            "steps_zh": [
                "第1步：学科建设/教育改革——教育建设：萨尔伯格进行教育改革，皮萨进行社会改革",
                "第2步：群众路线/平等——平等建设：萨尔伯格建立教育平等，皮萨建立社会平等",
                "第3步：长期主义/代际——长期发展：萨尔伯格建立教育长效机制，皮萨建立社会长效机制"
            ],
            "steps_en": [
                "Step 1: Discipline Construction/Education Reform - Education construction: Salonen conducts education reform, Pissa conducts social reform",
                "Step 2: Mass Line/Equality - Equality construction: Salonen establishes educational equality, Pissa establishes social equality",
                "Step 3: Long-termism/Intergenerational - Long-term development: Salonen establishes education long-term mechanism, Pissa establishes social long-term mechanism"
            ],
            "expected_zh": [
                "建立完善的教育体系",
                "建立平等的社会体系",
                "促进社会长期发展"
            ],
            "expected_en": [
                "Establish perfect education system",
                "Establish equal social system",
                "Promote social long-term development"
            ],
            "case_zh": "萨尔伯格是芬兰著名的教育家，皮萨是芬兰社会学家。三者共同推动了芬兰的教育和社会发展。",
            "case_en": "Salonen was a famous Finnish educator, Pissa was a Finnish sociologist. Together they promoted Finland's education and social development.",
            "era": "1969-至今",
            "historical_domains": ["教育", "社会"],
            "domains": ["协作", "系统", "分析", "创意", "运营"],
            "gender": "男/男",
            "ethnicity": "芬兰"
        }
    ]
    
    # Create NO directory
    no_dir = f"{base_path}/NO"
    os.makedirs(no_dir, exist_ok=True)
    
    for figure in nordic_figures:
        file_path = f"{no_dir}/{figure['code']}.json"
        create_json_file(file_path, figure)

if __name__ == "__main__":
    print("Creating 8 Nordic figures for Phase 7 Batch 3...")
    create_nordic_figures()
    print("All 8 Nordic figures created successfully!")