import json

# Load existing data
with open('scenarios_zh.json', 'r', encoding='utf-8') as f:
    zh = json.load(f)
with open('scenarios_en.json', 'r', encoding='utf-8') as f:
    en = json.load(f)
with open('code_maps.json', 'r', encoding='utf-8') as f:
    cm = json.load(f)

# New entries to add
new_entries = [
    {
        "code": "H-PDH-130",
        "name_zh": "彭德怀：群众路线军事实践者 / 百团大战指挥 / 抗美援朝统帅 / \"彭德怀训练大纲\"创立者",
        "name_en": "Peng Dehuai: Military Practitioner of Mass Line / Commander of Hundred Regiments Offensive / Commander-in-Chief of Korean War / Founder of Peng Dehuai Training Outline",
        "description_zh": "群众路线/百团大战/抗美援朝/训练大纲/军事民主",
        "description_en": "Mass Line/Hundred Regiments Offensive/Korean War/Training Outline/Military Democracy",
        "modes": [2, 6, 31, 34],
        "reason_zh": "核心思维：将「群众路线」从政治工作内化为「军事训练/作战指挥/后勤保障」全链条操作体系——「官兵一致、军民一致、瓦解敌军」三大军事群众路线原则；百团大战以「分散游击→集中攻击→分散隐蔽」节奏动员 20 万民工支前；抗美援朝「以一敌十」依靠「隐蔽工程、坑道作战、夜间机动」将美军火力优势转化为「打不动、找不着、消耗大」战略负担；《彭德怀训练大纲》将「群众路线」标准化为 12 条训练大纲。",
        "reason_en": "Core thinking: Internalized 'Mass Line' from political work into full-chain military operations — 'unity of officers and soldiers, unity of army and people, disintegration of enemy forces' three principles; Hundred Regiments Offensive mobilized 200,000 civilian workers with 'dispersed guerrilla → concentrated attack → dispersed concealment' rhythm; Korean War '1 vs 10' relied on 'tunnel warfare, night maneuver' to convert US firepower superiority into strategic burden; Peng Dehuai Training Outline standardized 'Mass Line' into 12 training syllabi.",
        "steps_zh": [
            "第1步：群众路线法——将「同吃同住同训练」落实为「军官带头挖坑道、指挥员第一个冲锋」可观测行为标准，消除特权隔阂",
            "第2步：统一战线法——设计「民工部编制→口粮就地筹集→伤员就地安置→情报全民皆兵」四位一体动员体系，将百姓变「后勤部」",
            "第3步：框架效应法——设计「喊话/传单/放虏/善俘」四重话术框架，将「美军不可战胜」重构为「回家才是荣耀」叙事",
            "第4步：制度化制衡——将「群众路线」固化为「12 条大纲、48 项指标、考核红绿灯」标准体系，防止「形式主义/突击整顿」反弹"
        ],
        "steps_en": [
            "Step 1: Mass Line — Implement 'same food, same quarters, same training' as observable behavior 'officers dig tunnels first, commanders charge first', eliminating privilege gaps",
            "Step 2: United Front — Design 'Civilian Labor Department + local grain requisition + local casualty care + universal intelligence' 4-in-1 mobilization system, turning populace into 'logistics department'",
            "Step 3: Framing Effect — Design 'shouting/leaflets/release prisoners/humane treatment' 4-layer discourse framework, reframing 'US invincible' into 'going home is glory' narrative",
            "Step 4: Institutional Checks — Solidify 'Mass Line' into '12 syllabi, 48 indicators, assessment traffic lights' standard system, preventing 'formalism/campaign-style' relapse"
        ],
        "expected_zh": [
            "建立可复制的「群众路线军事化」标准体系",
            "百团大战歼敌 2 万+、动员民工 20 万+",
            "抗美援朝以伤亡比 1:2 实现战略平衡",
            "训练大纲成为建军史标杆，后世「官兵一致」标准动作"
        ],
        "expected_en": [
            "Establish replicable 'militarized mass line' standard system",
            "Hundred Regiments Offensive: 20,000+ enemy casualties, 200,000+ civilians mobilized",
            "Korean War: 1:2 casualty ratio achieving strategic stalemate",
            "Training Outline becomes benchmark in army-building history, 'unity of officers and soldiers' standardized"
        ],
        "case_zh": "百团大战（1940）：面对日军「围困据点、切断补给」战术，彭德怀用「群众路线法」设计「民工部编制→口粮就地筹集→伤员就地安置→情报全民皆兵」四位一体动员体系，20 万民工支前，以「分散游击→集中攻击→分散隐蔽」节奏 18 天毁铁路 470 公里、公路 1500 公里、桥梁 260 座，歼敌 2 万+。抗美援朝（1950-1953）：依靠「隐蔽工程、坑道作战、夜间机动」将美军火力优势转化为「打不动、找不着、消耗大」战略负担，编写《彭德怀训练大纲》将「群众路线」标准化为 12 条大纲、48 项指标。",
        "case_en": "Hundred Regiments Offensive (1940): Facing Japanese 'strongpoint encirclement, supply cutoff' tactics, Peng designed 'Civilian Labor Dept + local grain + local casualty care + universal intelligence' 4-in-1 mobilization, 200k civilians supported, 'dispersed guerrilla → concentrated attack → dispersed concealment' rhythm destroyed 470km railway, 1500km highway, 260 bridges in 18 days, 20k+ enemy casualties. Korean War (1950-1953): Relied on 'tunnel warfare, night maneuver' to convert US firepower superiority into 'can't hit, can't find, high consumption' strategic burden; authored Peng Dehuai Training Outline standardizing 'Mass Line' into 12 syllabi, 48 indicators."
    },
    {
        "code": "H-ZEL-131",
        "name_zh": "周恩来：外交/统战/政府建设体系总设计师 / \"周恩来外交十大原则\" / 政务运作工程化大师",
        "name_en": "Zhou Enlai: Chief Architect of Diplomatic/United Front/Government Systems / Zhou Enlai's Ten Diplomatic Principles / Master of Government Operations Engineering",
        "description_zh": "求同存异/统一战线/政府运作/周三会议/三级责任链",
        "description_en": "Seek Common Ground/United Front/Government Operations/Weekly Wednesday Meetings/Three-Level Responsibility Chain",
        "modes": [42, 20, 6, 41, 34],
        "reason_zh": "核心思维：构建「外交破冰→统战联合→政府运作」三位一体国家治理工程体系——外交上用「求同存异、互利共赢」五项原则破解冷战封锁，实现「破交往→建关系→扩领域」三阶段突围；统战上用「长期共存、互相监督、肝胆相照、荣辱与共」十六字方针将民主党派/工商界/宗教界/海外侨胞纳入「爱国统一战线」；政府上用「周三会议、国务院常务会议、专题汇报」三级会议体系，将「总理负责制、部长负责制、科长负责制」三级责任链条标准化，实现「决策-执行-反馈」高频闭环。",
        "reason_en": "Core thinking: Built 'Diplomatic Breakthrough → United Front Union → Government Operations' trinity national governance engineering system — Diplomacy: 'Seek Common Ground, Mutual Benefit' Five Principles broke Cold War blockade, achieving 'Break Contact → Establish Relations → Expand Domains' three-stage breakthrough; United Front: 'Long-term Coexistence, Mutual Supervision, Heart-to-Heart, Share Honor and Disgrace' 16-character policy integrated democratic parties/business/religious/overseas Chinese into 'Patriotic United Front'; Government: 'Wednesday Meetings, Executive Meetings, Special Briefings' three-tier meeting system standardized 'Premier Responsibility, Minister Responsibility, Section Chief Responsibility' three-level accountability chain, achieving 'Decision-Execution-Feedback' high-frequency closure.",
        "steps_zh": [
            "第1步：博弈论思维——识别对手「核心利益不可让、非核心利益可交换」边界，用「求同存异」锚定最小共识集合",
            "第2步：统一战线法——设计「核心层(共产党)→同盟层(民主党派/工商/宗教)→中间层(海外/知识分子)→外围层(对立面可争取者)」四层扩展算法",
            "第3步：驿站制/信息流速——建立「周三会议(战略/日)→常务会议(战术/周)→专题汇报(专项/月)」三级信息流速分层体系，决策延迟<24h",
            "第4步：制度化制衡+程序正义法——将「总理决策-部长执行-科长落实」固化为「会签制、首问制、限时办结制」三大程序锁",
            "第5步：反馈回路——将每次外交成果(建交/协定/声明)转化为「法律文本→国内法同步→执行监测→下一轮谈判筹码」正反馈回路"
        ],
        "steps_en": [
            "Step 1: Game Theory — Identify opponent's 'core interests non-negotiable, non-core interests exchangeable' boundary, anchor minimum consensus with 'Seek Common Ground'",
            "Step 2: United Front — Design 'Core Layer (CPC) → Alliance Layer (Democratic Parties/Business/Religion) → Middle Layer (Overseas/Intellectuals) → Peripheral Layer (Opposition Winnable)' 4-layer expansion algorithm",
            "Step 3: Relay Station/Info Flow — Build 'Wednesday Meeting (Strategy/Daily) → Executive Meeting (Tactical/Weekly) → Special Briefing (Special/Monthly)' 3-tier info flow hierarchy, decision latency < 24h",
            "Step 4: Institutional Checks + Procedural Justice — Solidify 'Premier Decides → Minister Executes → Section Chief Implements' into 'Countersignature System, First-Ask System, Time-Limit Completion System' three procedural locks",
            "Step 5: Feedback Loop — Convert each diplomatic outcome (Recognition/Agreement/Declaration) into 'Legal Text → Domestic Law Sync → Execution Monitoring → Next Round Negotiation Leverage' positive feedback loop"
        ],
        "expected_zh": [
            "外交破冰：1972 中美破冰、1978 中日友好条约、建交 100+ 国",
            "统战同心圆：民主党派/工商/宗教/海外侨胞全纳入爱国统一战线",
            "政府运作：三级会议体系/三级责任链/会签制/首问制/限时办结制标准化",
            "外交资产复利化：每次成果转化为下轮谈判筹码"
        ],
        "expected_en": [
            "Diplomatic Breakthrough: 1972 US-China Rapprochement, 1978 Sino-Japanese Treaty, 100+ Diplomatic Relations",
            "United Front: Democratic Parties/Business/Religion/Overseas Chinese all integrated into Patriotic United Front",
            "Governance: 3-tier Meeting System / 3-tier Accountability / Countersignature/First-Ask/Time-Limit Systems Standardized",
            "Diplomatic Asset Compounding: Each Outcome Converted to Next Round Leverage"
        ],
        "case_zh": "1971-1972 中美破冰：面对「反华包围圈」封锁，周恩来用「博弈论思维」识别尼克松「需中国制衡苏联/需越战脱身」核心需求，用「求同存异」锚定「台湾问题暂搁置、上海公报共同声明」最小共识集合；1954 日内瓦会议/1955 万隆会议：用「统一战线法」设计「核心层→同盟层→中间层→外围层」四层扩展，建立「和平共处五项原则」国际法准则；政府日常：周三会议(战略/日)→常务会议(战术/周)→专题汇报(专项/月)三级信息流速分层，决策延迟<24h。",
        "case_en": "1971-1972 US-China Rapprochement: Facing 'Anti-China Encirclement', Zhou used Game Theory to identify Nixon's 'Need China to Counter USSR / Need Vietnam Exit' core needs, anchored 'Taiwan Issue Shelved + Shanghai Communique Joint Statement' minimum consensus with 'Seek Common Ground'. 1954 Geneva/1955 Bandung: United Front designed 'Core → Alliance → Middle → Peripheral' 4-layer expansion, established 'Five Principles of Peaceful Coexistence' international law norms. Daily Governance: Wednesday Meetings (Strategy/Daily) → Executive Meetings (Tactical/Weekly) → Special Briefings (Special/Monthly) 3-tier info flow, decision latency < 24h."
    },
    {
        "code": "H-LSQ-132",
        "name_zh": "刘少奇：党建组织路线奠基人 / 《论共产党员的修养》 / \"安内攘外\"党内法治建设者",
        "name_en": "Liu Shaoqi: Founder of Party Building Organizational Line / On the Cultivation of Communist Party Members / 'Internal Stability, External Resistance' Party Rule-of-Law Builder",
        "description_zh": "党的建设/组织路线/党员修养/安内攘外/党内法治/纪律处分",
        "description_en": "Party Building/Organizational Line/Party Member Cultivation/Internal Stability/Party Rule of Law/Disciplinary Sanctions",
        "modes": [42, 10, 32, 34],
        "reason_zh": "核心思维：将「党的建设」工程化为「组织路线→纪律建设→干部管理→党内法治」四大标准化子系统——主持起草《党章》(七大)确立「民主集中制」组织原则；编写《论共产党员的修养》将「党性修养」拆解为「立场、观点、方法、作风、纪律」五维可考核指标；创立「安内攘外」党内斗争策略——「安内」用「批评与自我批评」(模式 10) 解决内部矛盾、「攘外」用「统一战线」隔离外部敌人；推动《关于建党问题的报告》确立「党员标准、发展程序、组织生活、纪律处分」四大制度框架。",
        "reason_en": "Core thinking: Engineered 'Party Building' into 'Organizational Line → Discipline Construction → Cadre Management → Party Rule of Law' four standardized subsystems — Drafted Party Constitution (7th Congress) establishing 'Democratic Centralism' organizational principle; Authored On the Cultivation of Communist Party Members decomposing 'Party Spirit Cultivation' into 'Standpoint, Viewpoint, Method, Style, Discipline' five assessable dimensions; Created 'Internal Stability, External Resistance' intra-party struggle strategy — 'Internal Stability' uses 'Criticism and Self-Criticism' (Mode 10) for internal contradictions, 'External Resistance' uses 'United Front' to isolate external enemies; Advanced Report on Party Building Issues establishing 'Party Member Standards, Recruitment Procedures, Organizational Life, Disciplinary Sanctions' four institutional frameworks.",
        "steps_zh": [
            "第1步：批评与自我批评——将「共产党员条件」拆解为「政治坚定性、理论水平、群众工作能力、廉洁自律、先锋模范作用」五维评分卡",
            "第2步：程序正义法——设计「申请→考察→接收→预备→转正→考核」六阶段标准流程，每阶段有「考察人、考察表、考察期、考核标准」四定",
            "第3步：制度化制衡——固化「三会一课(支部大会/支委会/党小组会/党课)、民主生活会、组织生活会」三大刚性制度，缺席率纳入考核",
            "第4步：框架效应法——将违纪行为分「政治/组织/廉洁/群众/工作/生活」六大类、四档次(警告/严重警告/撤销职务/开除党籍)，建立「违纪-处分-申诉-复核」程序闭环"
        ],
        "steps_en": [
            "Step 1: Criticism & Self-Criticism — Decompose 'Communist Party Member Qualifications' into 'Political Firmness, Theoretical Level, Mass Work Ability, Integrity, Vanguard Role' 5-dimension scorecard",
            "Step 2: Procedural Justice — Design 'Application → Investigation → Admission → Probation → Full Membership → Assessment' 6-stage standard process, each stage has 'Investigator, Investigation Form, Investigation Period, Assessment Standard' four fixed elements",
            "Step 3: Institutional Checks — Solidify 'Three Meetings One Class (Branch Congress/Branch Committee/Party Group Meeting/Party Class), Democratic Life Meeting, Organizational Life Meeting' three rigid systems, absentee rate included in assessment",
            "Step 4: Framing Effect — Categorize Violations into 'Political/Organizational/Integrity/Mass/Work/Life' 6 categories, 4 tiers (Warning/Serious Warning/Removal/Expulsion), Build 'Violation → Sanction → Appeal → Review' Procedural Closure"
        ],
        "expected_zh": [
            "《党章》(七大)确立民主集中制组织原则",
            "《论共产党员的修养》成为党性教育教科书",
            "《关于建党问题的报告》确立党员标准/发展程序/组织生活/纪律处分四大框架",
            "安内攘外策略：安内靠批评与自我批评、攘外靠统一战线"
        ],
        "expected_en": [
            "Party Constitution (7th Congress) Established Democratic Centralism Organizational Principle",
            "On the Cultivation of Communist Party Members Became Party Spirit Education Textbook",
            "Report on Party Building Issues Established 4 Frameworks: Member Standards/Recruitment/Org Life/Discipline",
            "Internal Stability/External Resistance Strategy: Internal via Criticism & Self-Criticism, External via United Front"
        ],
        "case_zh": "1945 七大起草《党章》确立「民主集中制」；1939 《论共产党员的修养》将「党性修养」量化为五维指标；1942 延安整风中推行「批评与自我批评」解决内部矛盾；1948 《关于建党问题的报告》系统阐述「组织路线服务于政治路线」；1956 八大推动《关于建党问题的报告》确立「安内攘外」党内斗争策略——「安内」靠批评与自我批评解决内部矛盾，「攘外」靠统一战线隔离外部敌人。",
        "case_en": "1945 7th Congress drafted Party Constitution establishing 'Democratic Centralism'; 1939 On the Cultivation of Communist Party Members quantified 'Party Spirit' into 5 dimensions; 1942 Yan'an Rectification implemented 'Criticism & Self-Criticism' for internal contradictions; 1948 Report on Party Building Issues systematically expounded 'Organizational Line Serves Political Line'; 1956 8th Congress advanced Report establishing 'Internal Stability/External Resistance' intra-party struggle strategy — Internal via Criticism & Self-Criticism, External via United Front isolation."
    }
]

# Add to zh and en
for entry in new_entries:
    code = entry["code"]
    zh[code] = {
        "name": entry["name_zh"],
        "description": entry["description_zh"],
        "modes": entry["modes"],
        "reason": entry["reason_zh"],
        "steps": entry["steps_zh"],
        "expected": entry["expected_zh"],
        "case": entry["case_zh"]
    }
    en[code] = {
        "name": entry["name_en"],
        "description": entry["description_en"],
        "modes": entry["modes"],
        "reason": entry["reason_en"],
        "steps": entry["steps_en"],
        "expected": entry["expected_en"],
        "case": entry["case_en"]
    }
    cm["CODE_MAP"][code] = entry["name_zh"]
    cm["CODE_MAP_EN"][code] = entry["name_en"]

# Save files
with open('scenarios_zh.json', 'w', encoding='utf-8') as f:
    json.dump(zh, f, ensure_ascii=False, indent=2)
with open('scenarios_en.json', 'w', encoding='utf-8') as f:
    json.dump(en, f, ensure_ascii=False, indent=2)
with open('code_maps.json', 'w', encoding='utf-8') as f:
    json.dump(cm, f, ensure_ascii=False, indent=2)

print("✅ Added 3 new figures")