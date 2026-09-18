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
            "description_en": "Bertil Ohlin was a famous Swedish economist, proposed the famous "Ohlin Model". Wallenberg was a famous Swedish banker, made important contributions in the financial field.",
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
            "case_zh": "贝尔特·奥尔清提出了"奥尔清模型"，成为国际经济学的重要理论。瓦伦贝里在金融领域有重要贡献，建立了瑞典金融体系。
            "case_en": "Bertil Ohlin proposed the "Ohlin Model", which became an important international economic theory. Wallenberg made important contributions in the financial field, established Swedish financial system.",
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
            "case_zh": "纳塞尔领导挪威的政治建设，布伦特兰夫人领导挪威的环境建设。两人共同推动了挪威的民主发展。
            "case_en": "Nasser led Norway's political construction, Brundtland led Norway's environmental construction. Together they promoted Norway's democratic development.",
            "era": "1969-1974,1940-1981",
            "historical_domains": ["政治", "外交", "环境"],
            "domains": ["协作", "系统", "分析", "创意", "运营"],
            "gender": "男/女",
            "ethnicity": "挪威"
        },
        {
            "id": "DK-FLEX-001",
            "code": "DK-FLEX-001",
            "name_zh": "科尔/拉斯穆森",
            "name_en": "Kold/Rasmussen",
            "core_mode": "北欧信任资本-核心",
            "wiki_id": "Q452,Q22830",
            "nationality": "丹麦",
            "civilization_sphere": "北欧",
            "time_period_standardized": "1818-1898,1842-1932",
            "primary_language": "丹麦语",
            "intellectual_tradition": "政治，法律，社会",
            "description_zh": "科尔是丹麦政治家，领导了丹麦的政治建设。拉斯穆森是丹麦法律学者，在法律领域有重要贡献。",
            "description_en": "Kold was a Danish politician, led Denmark's political construction. Rasmussen was a Danish legal scholar, made important contributions in the legal field.",
            "reason_zh": "核心思维：151(北欧信任资本-核心)、38(摸石头过河/灵活保障制)、34(制度化制衡)、52(长期主义)",
            "reason_en": "Core thinking modes: 151(Nordic Trust Capital - Core), 38(Flexible Guarantee System), 34(Institutionalized Check-and-balance), 52(Long-termism)",
            "modes": [151, 38, 34, 52],
            "steps_zh": [
                "第1步：摸石头过河/灵活保障制——政治建设：科尔通过试错建立政治制度，拉斯穆森通过试错建立法律制度",
                "第2步：制度化制衡——制度建设：科尔建立政治制度，拉斯穆森建立法律制度",
                "第3步：长期主义——制度维护：科尔维护政治制度，拉斯穆森维护法律制度"
            ],
            "steps_en": [
                "Step 1: Flexible Guarantee System - Political construction: Kold establishes political system through trial and error, Rasmussen establishes legal system through trial and error",
                "Step 2: Institutionalized Check-and-balance - Institutional construction: Kold establishes political system, Rasmussen establishes legal system",
                "Step 3: Long-termism - System maintenance: Kold maintains political system, Rasmussen maintains legal system"
            ],
            "expected_zh": [
                "建立灵活的政治制度",
                "建立完善的法律制度",
                "促进社会长期稳定"
            ],
            "expected_en": [
                "Establish flexible political system",
                "Establish perfect legal system",
                "Promote social long-term stability"
            ],
            "case_zh": "科尔通过试错建立了丹麦政治制度，拉斯穆森通过试错建立了丹麦法律制度。两人共同推动了丹麦的制度建设。
            "case_en": "Kold established Danish political system through trial and error, Rasmussen established Danish legal system through trial and error. Together they promoted Denmark's institutional construction.",
            "era": "1818-1898,1842-1932",
            "historical_domains": ["政治", "法律", "社会"],
            "domains": ["协作", "系统", "分析", "创意", "运营"],
            "gender": "男/男",
            "ethnicity": "丹麦"
        },
        {
            "id": "FI-SISU-001",
            "code": "FI-SISU-001",
            "name_zh": "曼纳海姆/林纳斯·托瓦兹",
            "name_en": "Mannerheim/Linus Torvalds",
            "core_mode": "北欧信任资本-核心",
            "wiki_id": "Q26787,Q83198",
            "nationality": "芬兰",
            "civilization_sphere": "北欧",
            "time_period_standardized": "1867-1951,1969-至今",
            "primary_language": "芬兰语/英语",
            "intellectual_tradition": "军事，技术，开源",
            "description_zh": "曼纳海姆是芬兰著名的军事家，领导了芬兰的国防建设。林纳斯·托瓦兹是Linux内核的创始人，在技术领域有重要贡献。",
            "description_en": "Mannerheim was a famous Finnish military man, led Finland's defense construction. Linus Torvalds is the founder of Linux kernel, made important contributions in the technology field.",
            "reason_zh": "核心思维：151(北欧信任资本-核心)、35(蛰伏积势/西苏精神)、51(自主研发/Linux)、36(笨功夫/开源坚持)",
            "reason_en": "Core thinking modes: 151(Nordic Trust Capital - Core), 35(Fueled Accumulation/Sisu Spirit), 51(Autonomous Research/Linux), 36(Bedrock Adherence/Open Source Persistence)",
            "modes": [151, 35, 51, 36],
            "steps_zh": [
                "第1步：蛰伏积势/西苏精神——军事建设：曼纳海姆通过蛰伏积势建立军事制度，托瓦兹通过蛰伏积势建立开源制度",
                "第2步：自主研发/Linux——技术建设：曼纳海姆自主研发军事技术，托瓦兹自主研发Linux技术",
                "第3步：笨功夫/开源坚持——制度维护：曼纳海姆坚持军事制度，托瓦兹坚持开源制度"
            ],
            "steps_en": [
                "Step 1: Fueled Accumulation/Sisu Spirit - Military construction: Mannerheim establishes military system through fueled accumulation, Torvalds establishes open source system through fueled accumulation",
                "Step 2: Autonomous Research/Linux - Technology construction: Mannerheim autonomously develops military technology, Torvalds autonomously develops Linux technology",
                "Step 3: Bedrock Adherence/Open Source Persistence - System maintenance: Mannerheim adheres to military system, Torvalds adheres to open source system"
            ],
            "expected_zh": [
                "建立强大的国防体系",
                "建立自主创新的技术体系",
                "促进社会长期发展"
            ],
            "expected_en": [
                "Establish strong defense system",
                "Establish autonomous innovation technology system",
                "Promote social long-term development"
            ],
            "case_zh": "曼纳海姆通过蛰伏积势建立了芬兰的军事体系，林纳斯·托瓦兹通过蛰伏积势建立了Linux的开源体系。两人共同推动了芬兰的技术发展。
            "case_en": "Mannerheim established Finnish military system through fueled accumulation, Linus Torvalds established Linux open source system through fueled accumulation. Together they promoted Finland's technological development.",
            "era": "1867-1951,1969-至今",
            "historical_domains": ["军事", "技术", "开源"],
            "domains": ["协作", "系统", "分析", "创意", "运营"],
            "gender": "男/男",
            "ethnicity": "芬兰"
        },
        {
            "id": "SE-INN-001",
            "code": "SE-INN-001",
            "name_zh": "诺贝尔/卡姆普拉德/埃里克森",
            "name_en": "Nobel/Camprad/Eriksson",
            "core_mode": "自主研发/炸药/宜家/电信",
            "wiki_id": "Q1746,Q181300,Q76998",
            "nationality": "瑞典",
            "civilization_sphere": "北欧",
            "time_period_standardized": "1833-1896,1926-2018,1918-2001",
            "primary_language": "瑞典语",
            "intellectual_tradition": "科学，商业，社会",
            "description_zh": "诺贝尔创立了诺贝尔奖，卡姆普拉德创立了宜家家具，埃里克森是瑞典电信行业的领军人物。三者共同推动了瑞典的科学和商业发展。",
            "description_en": "Nobel established Nobel Prize, Camprad established IKEA furniture, Eriksson was a leader in Swedish telecommunications industry. Together they promoted Sweden's science and business development.",
            "reason_zh": "核心思维：51(自主研发/炸药/宜家/电信)、151(北欧信任资本/商业生态)、47(价值对话/用户共创)",
            "reason_en": "Core thinking modes: 51(Autonomous Research/Explosives/IKEA/Telecom), 151(Nordic Trust Capital/Business Ecosystem), 47(Value Dialogue/User Co-creation)",
            "modes": [51, 151, 47],
            "steps_zh": [
                "第1步：自主研发法——技术创新：诺贝尔创新炸药技术，卡姆普拉德创新家具技术，埃里克森创新电信技术",
                "第2步：灵活策略法——商业模式创新：诺贝尔建立科学奖，卡姆普拉德建立家具公司，埃里克森建立电信公司",
                "第3步：价值对话法——用户共创：诺贝尔用户参与设计，卡姆普拉德用户参与设计，埃里克森用户参与设计"
            ],
            "steps_en": [
                "Step 1: Autonomous Research Method - Technological Innovation: Nobel innovates explosives technology, Camprad innovates furniture technology, Eriksson innovates telecom technology",
                "Step 2: Flexible Strategy Method - Business Model Innovation: Nobel establishes science award, Camprad establishes furniture company, Eriksson establishes telecom company",
                "Step 3: Value Dialogue Method - User Co-creation: Nobel users participate in design, Camprad users participate in design, Eriksson users participate in design"
            ],
            "expected_zh": [
                "建立自主创新的技术生态系统",
                "推动科学和商业发展",
                "促进社会长期繁荣"
            ],
            "expected_en": [
                "Establish autonomous innovation technology ecosystem",
                "Promote science and business development",
                "Promote social long-term prosperity"
            ],
            "case_zh": "诺贝尔创立了诺贝尔奖，卡姆普拉德创立了宜家家具，埃里克森是瑞典电信行业的领军人物。三者共同推动了瑞典的科学和商业发展。
            "case_en": "Nobel established Nobel Prize, Camprad established IKEA furniture, Eriksson was a leader in Swedish telecommunications industry. Together they promoted Sweden's science and business development.",
            "era": "1833-1896,1926-2018,1918-2001",
            "historical_domains": ["科学", "商业", "电信"],
            "domains": ["协作", "系统", "分析", "创意", "运营"],
            "gender": "男/男/男",
            "ethnicity": "瑞典"
        },
        {
            "id": "NO-ENER-001",
            "code": "NO-ENER-001",
            "name_zh": "斯塔滕/埃克森",
            "name_en": "Støre/Ekman",
            "core_mode": "北欧信任资本-核心",
            "wiki_id": "Q39727,Q579114",
            "nationality": "挪威",
            "civilization_sphere": "北欧",
            "time_period_standardized": "1970-至今",
            "primary_language": "挪威语/英语",
            "intellectual_tradition": "政治，能源，经济",
            "description_zh": "斯塔滕是挪威现任首相，领导了挪威的能源建设。埃克森是挪威能源行业的领军人物，在能源领域有重要贡献。",
            "description_en": "Støre is current Norwegian Prime Minister, led Norway's energy construction. Ekman is a leader in Norwegian energy industry, made important contributions in the energy field.",
            "reason_zh": "核心思维：151(北欧信任资本-核心)、39(鸟笼经济/资源管理)、52(长期主义/主权基金)、12(系统思维)",
            "reason_en": "Core thinking modes: 151(Nordic Trust Capital - Core), 39(Cage Economy/Resource Management), 52(Long-termism/Sovereign Fund), 12(Systematic Thinking)",
            "modes": [151, 39, 52, 12],
            "steps_zh": [
                "第1步：鸟笼经济/资源管理——能源建设：斯塔滕进行资源管理，埃克森进行能源管理",
                "第2步：长期主义/主权基金——长期发展：斯塔滕建立主权基金，埃克森建立能源基金",
                "第3步：系统思维——系统建设：斯塔滕建立能源系统，埃克森建立能源系统"
            ],
            "steps_en": [
                "Step 1: Cage Economy/Resource Management - Energy construction: Støre conducts resource management, Ekman conducts energy management",
                "Step 2: Long-termism/Sovereign Fund - Long-term development: Støre establishes sovereign fund, Ekman establishes energy fund",
                "Step 3: Systematic Thinking - System construction: Støre establishes energy system, Ekman establishes energy system"
            ],
            "expected_zh": [
                "建立能源管理体系",
                "建立资源管理体系",
                "促进经济长期发展"
            ],
            "expected_en": [
                "Establish energy management system",
                "Establish resource management system",
                "Promote economic long-term development"
            ],
            "case_zh": "斯塔滕领导挪威的能源建设，埃克森领导挪威的资源管理。两人共同推动了挪威的能源和经济发展。
            "case_en": "Støre led Norway's energy construction, Ekman led Norway's resource management. Together they promoted Norway's energy and economic development.",
            "era": "1970-至今",
            "historical_domains": ["政治", "能源", "经济"],
            "domains": ["协作", "系统", "分析", "创意", "运营"],
            "gender": "男/男",
            "ethnicity": "挪威"
        },
        {
            "id": "DK-DES-001",
            "code": "DK-DES-001",
            "name_zh": "雅各布森/邦·凯尔/乐高",
            "name_en": "Jacobsen/Bang/K Lego",
            "core_mode": "通才整合/设计/工程/商业",
            "wiki_id": "Q8370,Q125344,Q49052",
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
            "case_zh": "雅各布森是丹麦著名设计师，邦·凯尔是丹麦工程师，乐高是丹麦著名玩具公司。三者共同推动了丹麦的设计、工程和商业发展。
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
            "case_zh": "萨尔伯格是芬兰著名的教育家，皮萨是芬兰社会学家。三者共同推动了芬兰的教育和社会发展。
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