import json

# Load existing data
with open('scenarios_zh.json', 'r', encoding='utf-8') as f:
    zh = json.load(f)
with open('scenarios_en.json', 'r', encoding='utf-8') as f:
    en = json.load(f)
with open('code_maps.json', 'r', encoding='utf-8') as f:
    cm = json.load(f)

# New entries to add (based on v2 research file)
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
    },
    {
        "code": "H-CDX-133",
        "name_zh": "陈独秀：新文化运动激进破局者 / 启蒙旗手 / 早期中共总书记 / 从激进到反思的思想轨迹",
        "name_en": "Chen Duxiu: Radical Trailblazer of New Culture Movement / Enlightenment Standard-Bearer / Early CCP General Secretary / Intellectual Trajectory from Radicalism to Reflection",
        "description_zh": "新青年/新文化运动/五四运动/早期中共/托派/反思",
        "description_en": "New Youth/New Culture Movement/May Fourth/Early CCP/Trotskyism/Reflection",
        "modes": [37, 11, 23, 36, 5],
        "reason_zh": "核心思维：在「孔家店压制、列强入侵、旧学垄断」三重死局中，用「破」字当头的激进启蒙策略——创办《新青年》发起「打倒孔家店、提倡德先生赛先生」总攻，以「文学革命/思想革命/道德革命」三大革命并进，打破文言垄断、推行白话文、引入科学民主两面旗帜；早期主导建党、领导五四、主持一大，将「马克思主义+中国工人运动」落地为可操作的革命纲领；晚年转向托洛茨基主义又在狱中反思「个人崇拜/极左/民主缺失」，完成从「激进破局者」到「反思型启蒙者」的思想跃迁。",
        "reason_en": "Core Thinking: In the triple deadlock of 'Confucian Orthodoxy Suppression + Foreign Invasion + Old Learning Monopoly', employed radical enlightenment strategy led by 'Destruction' — Founded New Youth launching 'Down with Confucian Shop, Welcome Mr. Democracy and Mr. Science' general offensive, advancing 'Literary Revolution + Ideological Revolution + Moral Revolution' triple revolution simultaneously, breaking Classical Chinese monopoly, promoting Vernacular Chinese, introducing Science & Democracy twin banners; Early leadership in Party founding, May Fourth leadership, presiding 1st Congress, landing 'Marxism + Chinese Workers Movement' into operable revolutionary program; Late-life turn to Trotskyism then prison reflection on 'Personality Cult / Ultra-Leftism / Democratic Deficit', completing intellectual leap from 'Radical Trailblazer' to 'Reflective Enlightener'.",
        "steps_zh": [
            "第1步：知行合一/致良知——以「破」字当头，亲身投入《新青年》创办、五四运动领导、建党主持，以身试法",
            "第2步：灵活策略法——「文学革命/思想革命/道德革命」三革命并进，兼用白话文/科学/民主三重工具破除旧学垄断",
            "第3步：自然选择法——在「马克思主义+工人运动」与「安那其/自由主义/国粹派」竞争中，以「建党+领导工运」组合胜出，完成范式跃迁",
            "第4步：蛰伏积势思维——狱中反思「个人崇拜/极左/民主缺失」，从「激进破局者」跃迁为「反思型启蒙者」，完成思想二次创业"
        ],
        "steps_en": [
            "Step 1: Unity of Knowledge and Action — Led with 'Destruction', personally founding New Youth, leading May Fourth, presiding 1st Congress, embodying praxis",
            "Step 2: Flexible Strategy — 'Literary/Ideological/Moral Revolution' triple advance, wielding Vernacular/Science/Democracy triple tools to break Old Learning monopoly",
            "Step 3: Natural Selection — In competition among 'Marxism+Workers Movement' vs 'Anarchism/Liberalism/Nationalism', 'Party Founding + Labor Leadership' combination won, achieving paradigm leap",
            "Step 4: Dormant Accumulation — Prison reflection on 'Personality Cult/Ultra-Leftism/Democratic Deficit', leap from 'Radical Trailblazer' to 'Reflective Enlightener', completing second intellectual entrepreneurship"
        ],
        "expected_zh": [
            "《新青年》创办，白话文运动发起，五四运动思想先驱",
            "中共一大主持，早期总书记，建党奠基",
            "晚年反思个人崇拜/极左/民主缺失，思想跃迁",
            "启蒙思想家→革命实践家→反思型批评家三重身份"
        ],
        "expected_en": [
            "Founded New Youth, Launched Vernacular Movement, Intellectual Pioneer of May Fourth",
            "Presided 1st CCP Congress, Early General Secretary, Party Founding Cornerstone",
            "Late-Life Reflection on Personality Cult/Ultra-Leftism/Democratic Deficit, Intellectual Leap",
            "Triple Identity: Enlightenment Thinker → Revolutionary Practitioner → Reflective Critic"
        ],
        "case_zh": "1915 创办《青年杂志》(后改《新青年》)，「打倒孔家店、提倡德先生赛先生」启蒙总动员；1917 提出「文学革命」主张，推动白话文取代文言文；1919 五四运动思想总指挥；1921 中共一大主持，当选首任总书记，领导早期工运(安源路矿工人罢工、京汉铁路工人罢工)；1927 八七会议后被撤职，转向托洛茨基主义；1932 被捕入狱，狱中写《更正党内几个错误主张的意见》、《给中央的信》反思「个人崇拜/极左/民主集中制异化」；出狱后隐居江苏丹徒，病逝前仍写《我的最后意见》呼吁「民主、自由、法治」。",
        "case_en": "1915 Founded Youth Magazine (renamed New Youth), 'Down with Confucian Shop, Welcome Mr. Democracy and Mr. Science' enlightenment mobilization; 1917 Proposed 'Literary Revolution', drove Vernacular replacing Classical Chinese; 1919 Intellectual Commander of May Fourth; 1921 Presided 1st CCP Congress, elected 1st General Secretary, led early labor movements (Anyuan Coal Mine Strike, Peking-Hankou Railway Strike); 1927 Post-August 7th Conference removed, turned to Trotskyism; 1932 Arrested, wrote 'Opinions on Correcting Several Erroneous Views in Party' and 'Letter to Central Committee' reflecting on 'Personality Cult/Ultra-Leftism/Democratic Centralism Alienation'; Post-release lived in seclusion in Dantu, Jiangsu, final writing 'My Last Opinions' appealing for 'Democracy, Freedom, Rule of Law'."
    },
    {
        "code": "H-LDZ-134",
        "name_zh": "李大钊：马克思主义中国化图书馆员先驱 / 北大图书馆员→马克思主义传播者 / 五四运动北方总指挥",
        "name_en": "Li Dazhao: Pioneer of Marxism Sinicization as Librarian / Peking University Librarian→Marxism Propagator / Northern Commander of May Fourth Movement",
        "description_zh": "马克思主义传播/五四运动/北大图书馆/苏联考察/共产主义小组/中国化先声",
        "description_en": "Marxism Propagation/May Fourth/PKU Library/Soviet Visit/Communist Groups/Sinicization Pioneer",
        "modes": [17, 24, 25, 12, 8],
        "reason_zh": "核心思维：以「图书馆员」身份将「马克思主义」从「书架理论」转化为「中国革命工具包」——利用北大图书馆馆长身份，系统引进、翻译、整理马克思主义文献(《共产党宣言》首译、 《资本论》导读)；创办《新青年》马克思主义专号、组建「马克思学说研究会」、创办「共产主义小组」，完成「理论引进→本土化解读→组织落地」三级跃迁；1924 赴苏联考察归来，提出「马克思主义中国化」早期设想；五四运动北方总指挥，将「理论传播」转化为「街头动员」；主张「农民是革命主力」，为「农村包围城市」埋下思想种子。",
        "reason_en": "Core Thinking: Transformed 'Marxism' from 'Library Theory' to 'Chinese Revolutionary Toolkit' via 'Librarian' identity — Leveraged PKU Library Director position to systematically introduce, translate, curate Marxist texts (1st translation of Communist Manifesto, Capital guide); Founded New Youth Marxism Special Issue, organized Marxism Research Society, formed Communist Groups, completing 'Theory Introduction → Localized Interpretation → Organizational Landing' three-level leap; 1924 Soviet Visit returned with early 'Marxism Sinicization' conception; May Fourth Northern Commander turned 'Theory Propagation' into 'Street Mobilization'; Argued 'Peasants are Revolutionary Main Force', planting intellectual seed for 'Rural Encirclement of Cities'.",
        "steps_zh": [
            "第1步：抽象归纳法——从海量马克思主义文献中提炼「阶级斗争/剩余价值/历史唯物主义」核心概念包，生成「马克思主义入门工具包」",
            "第2步：多元思维模型——将「历史唯物主义/剩余价值理论/阶级斗争」转化为可向工人/农民/学生讲授的「三大法宝」讲授模块",
            "第3步：系统思维法——构建「译介(文献)→研究会(解读)→小组(组织)→运动(动员)」四级传播系统，形成理论到行动的闭环",
            "第4步：独立自主法——1924 赴苏考察后，不照搬共产国际指令，首提「马克思主义中国化」，坚持「中国革命道路中国人自己走」"
        ],
        "steps_en": [
            "Step 1: Abstract Induction — Extract 'Class Struggle/Surplus Value/Historical Materialism' core concept package from vast Marxist literature, generate 'Marxism Starter Kit'",
            "Step 2: Multi-Model Thinking — Convert 'Historical Materialism/Surplus Value/Class Struggle' into 'Three Lectures' teachable to Workers/Peasants/Students",
            "Step 3: Systems Thinking — Build 'Translation (Texts) → Research Society (Interpretation) → Groups (Organization) → Movement (Mobilization)' 4-level propagation system, closing Theory-to-Action loop",
            "Step 4: Independence — Post-1924 Soviet Visit, refused to copy Comintern directives, first proposed 'Marxism Sinicization', insisting 'Chinese Revolution Path Walked by Chinese'"
        ],
        "expected_zh": [
            "《共产党宣言》中文首译，《资本论》导读普及",
            "创办《新青年》马克思主义专号，组建马克思学说研究会/共产主义小组",
            "五四运动北方总指挥，理论转化为街头动员",
            "首提「马克思主义中国化」，为毛泽东思想埋下种子"
        ],
        "expected_en": [
            "1st Chinese Translation of Communist Manifesto, Capital Guide Popularization",
            "Founded New Youth Marxism Special Issue, Organized Marxism Research Society/Communist Groups",
            "May Fourth Northern Commander, Theory Converted to Street Mobilization",
            "First Proposed 'Marxism Sinicization', Planting Seeds for Mao Zedong Thought"
        ],
        "case_zh": "1918 任北大图书馆长，利用馆藏优势系统引进马克思主义文献；1919 《新青年》刊登《我的马克思主义观》，系统介绍历史唯物主义/阶级斗争/剩余价值理论；1920 组建「马克思学说研究会」、创办共产主义小组，陈独秀南陈北李相约建党；1924 赴苏联考察第六次共产国际大会，实地考察苏联建设，归国后撰写《俄国革命的胜利及其教训》，提出「马克思主义中国化」早期思想；1926 三一八惨案后发表《民众的胜利》，坚持「民众运动不可阻挡」；1927 张作霖下令通缉，躲入苏联使馆；1928 被张作霖逮捕，绞刑执行，临刑前高呼「铁肩担道义，妙手著文章」。",
        "case_en": "1918 Became PKU Library Director, leveraged collection advantage to systematically introduce Marxist texts; 1919 New Youth published 'My View of Marxism', systematically introducing Historical Materialism/Class Struggle/Surplus Value; 1920 Organized Marxism Research Society, formed Communist Groups, South Chen North Li agreed on Party Founding; 1924 Visited USSR for 6th Comintern Congress, inspected Soviet Construction, returned writing 'Victory of Russian Revolution and Its Lessons', proposed early 'Marxism Sinicization'; 1926 Post-March 18 Massacre wrote 'Victory of the Masses', insisted 'Mass Movement Unstoppable'; 1927 Wanted by Zhang Zuolin, hid in Soviet Embassy; 1928 Arrested by Zhang Zuolin, executed by strangulation, final words 'Iron Shoulders Bear Moral Duty, Skillful Hands Write Articles'."
    },
    {
        "code": "H-PDH-135",
        "name_zh": "粟裕：运动战大师 / 华东野战军司令员 / \"四大歼灭战\"指挥官 / 游击战→运动战转型典范",
        "name_en": "Su Yu: Master of Mobile Warfare / Commander of East China Field Army / Commander of Four Major Annihilation Campaigns / Paradigm of Guerrilla-to-Mobile Warfare Transition",
        "description_zh": "运动歼灭/游击战/四大歼灭战/孟良崮/济南/淮海/渡江/弱势非对称作战",
        "description_en": "Mobile Annihilation/Guerrilla Warfare/Four Major Annihilation Campaigns/Menglianggu/Jinan/Huaihai/Crossing Yangtze/Weak Asymmetric Warfare",
        "modes": [35, 16, 15, 14, 12],
        "reason_zh": "核心思维：创立「游击战积累优势→运动战集中歼灭」非对称作战完整范式——在「敌强我弱、装备差 10 倍、无重武器」条件下，用「十六字诀」积累「兵源、弹药、干部、根据地」四要素；再用「运动歼灭法」设计「诱敌深入→侧背包围→分割包围→逐个歼灭」四步法，指挥孟良崮、济南、淮海、渡江四大歼灭战，以少胜多歼灭国民党正规军 100 万+；总结「战争艺术=时间艺术+空间艺术+兵力艺术」三维模型。",
        "reason_en": "Core Thinking: Created 'Guerrilla Accumulation → Mobile Warfare Concentrated Annihilation' complete asymmetric warfare paradigm — Under 'Enemy Strong/Us Weak, Equipment 10x Gap, No Heavy Weapons', used 'Sixteen-Character Formula' to accumulate 'Troop Sources, Ammunition, Cadres, Base Areas' four elements; Then used 'Mobile Annihilation' designing 'Lure Deep → Flank Encirclement → Segment Encirclement → Sequential Annihilation' four-step method, commanding Menglianggu, Jinan, Huaihai, Yangtze Crossing four major annihilation campaigns, outnumbered annihilating 1M+ KMT Regulars; Summarized 'War Art = Time Art + Space Art + Force Art' 3D model.",
        "steps_zh": [
            "第1步：蛰伏积势——建立「装备/兵力/补给/指挥/情报」五维劣势清单，拒绝「精神胜利法」自我欺骗",
            "第2步：游击积累四要素——用「游击战十六字诀」设计「敌进我退(保存兵源)→敌驻我扰(获取弹药)→敌疲我打(培养干部)→敌退我追(扩大根据地)」四阶段积累算法",
            "第3步：运动歼灭四步法——用「运动歼灭法」+「战争重心法」设计「识别重心(主力师/补给线)→诱敌分散→侧背集中→分割歼灭」四步标准动作",
            "第4步：时空兵力三维计算——用「系统思维法」建立「时间窗口(行军/休整/作战)×空间走廊(山地/平原/河网)×兵力比(局部 3:1)」三维决策模型",
            "第5步：统一战线法——设计「俘虏→教育→编入/释放→瓦解敌军士气」转化链，将歼灭战战果放大为战略心理攻势"
        ],
        "steps_en": [
            "Step 1: Dormant Accumulation — Build 5-dim disadvantage inventory 'Equipment/Troops/Logistics/Command/Intel', Reject 'Spiritual Victory' Self-Deception",
            "Step 2: Guerrilla Accumulation 4 Elements — 'Sixteen-Character Formula' designs 'Enemy Advances We Retreat (Preserve Troops) → Enemy Halts We Harass (Acquire Ammo) → Enemy Tires We Strike (Train Cadres) → Enemy Retreats We Pursue (Expand Base)' 4-Stage Accumulation Algorithm",
            "Step 3: Mobile Annihilation 4-Step — 'Mobile Annihilation' + 'War Center of Gravity' designs 'Identify Center of Gravity (Main Force Division/Supply Line) → Lure Dispersal → Flank Concentration → Segment Annihilation' 4 Standard Moves",
            "Step 4: Time-Space-Force 3D Calculation — 'Systems Thinking' builds 'Time Window (March/Rest/Combat) × Space Corridor (Mountain/Plain/River Network) × Force Ratio (Local 3:1)' 3D Decision Model",
            "Step 5: United Front — Design 'Prisoner → Education → Incorporate/Release → Disintegrate Enemy Morale' Conversion Chain, Amplifying Annihilation Results into Strategic Psychological Offensive"
        ],
        "expected_zh": [
            "创立「游击战积累优势→运动战集中歼灭」完整非对称作战范式",
            "孟良崮战役全歼整编 74 师、济南战役 8 天攻克坚城、淮海战役歼灭 55 万、渡江战役 100 万大军过江",
            "以少胜多歼灭国民党正规军 100 万+",
            "总结「战争艺术=时间艺术+空间艺术+兵力艺术」三维模型"
        ],
        "expected_en": [
            "Created Complete Asymmetric Warfare Paradigm: 'Guerrilla Accumulation → Mobile Warfare Concentrated Annihilation'",
            "Menglianggu: Annihilated Reorganized 74th Division; Jinan: 8 Days Captured Fortress; Huaihai: Annihilated 550k; Yangtze Crossing: 1M Troops Crossed",
            "Outnumbered Annihilated 1M+ KMT Regulars",
            "Summarized 'War Art = Time Art + Space Art + Force Art' 3D Model"
        ],
        "case_zh": "苏中七战七捷(1943-1944)：面对「据点围困、重兵压境」，粟裕用「诱敌深入→侧背包围→分割歼灭」运动战雏形，以 3 万兵力歼敌 5 万+，确立「运动战」核心地位。孟良崮战役(1947)：识别「整编 74 师=敌重心」，用「佯攻→迂回→合围→歼灭」四步法 4 天全歼王牌师。淮海战役(1948-1949)：统帅 60 万大军，用「分割包围→逐个歼灭」歼灭 55 万国军，决胜中原。渡江战役(1949)：100 万大军「分途同进、多点渡江」，3 天突破长江天险，直捣南京。",
        "case_en": "Central China 7 Victories (1943-44): Facing 'Strongpoint Encirclement, Heavy Troop Pressure', Su used 'Lure Deep → Flank Encirclement → Segment Annihilation' mobile warfare prototype, 30k troops annihilated 50k+ enemy, establishing Mobile Warfare core status. Menglianggu (1947): Identified 'Reorganized 74th Division = Enemy Center of Gravity', used 'Feint → Outflank → Encircle → Annihilate' 4-step method annihilated elite division in 4 days. Huaihai (1948-49): Commanded 600k, 'Segment Encirclement → Sequential Annihilation' annihilated 550k KMT, Decided Central China. Yangtze Crossing (1949): 1M Troops 'Multi-Route Simultaneous Crossing', 3 Days Breached Yangtze Barrier, Captured Nanjing."
    },
    {
        "code": "H-WZ-136",
        "name_zh": "王选：激光照排系统发明人 / 汉字信息处理之父 / \"死磕\"工程化典范",
        "name_en": "Wang Xuan: Inventor of Laser Phototypesetting System / Father of Chinese Information Processing / Paradigm of 'Relentless Perseverance' Engineering",
        "description_zh": "激光照排/汉字信息处理/字模设计/光学系统/计算机控制/排版软件/三个面向/产学研模式",
        "description_en": "Laser Phototypesetting/Chinese Info Processing/Font Design/Optical System/Computer Control/Typesetting Software/Three Orientations/Industry-University-Research Model",
        "modes": [1, 36, 38, 6, 34],
        "reason_zh": "核心思维：用「笨功夫」攻克汉字信息处理「皇冠上的明珠」——主持研制「华光激光照排系统」，从字模设计(7000 字×200 字体)、光学系统、计算机控制、排版软件全链路自主攻关，历时 12 年、修改 200 多版、试制 50 多台样机，打破日美垄断让中国印刷成本降低 90%；提出「三个面向」(面向生产、面向应用、面向国际)工程化标准，建立「院所-工厂-用户」三位一体产学研模式。",
        "reason_en": "Core Thinking: Used 'Relentless Perseverance' to Conquer 'Crown Jewel of Chinese Information Processing' — Led development of 'HuaGuang Laser Phototypesetting System', full-chain independent breakthrough from Font Design (7000 chars × 200 fonts), Optical System, Computer Control, Typesetting Software; 12 Years, 200+ Versions, 50+ Prototypes, Broke Japan-US Monopoly, Reduced Chinese Printing Cost by 90%; Proposed 'Three Orientations' (Production/Application/International) Engineering Standards, Established 'Institute-Factory-User' Trinity Industry-University-Research Model.",
        "steps_zh": [
            "第1步：矛盾分析法——识别「字模生成、光学聚焦、实时控制」三大核心矛盾，锁定「7000 汉字实时高质量成像」为主矛盾",
            "第2步：笨功夫/死磕到底——将每大模块拆解为「日更制度→复盘闭环→负面清单→传承文档」四项标准动作，建立 200+ 子任务看板",
            "第3步：摸石头过河——设计「周迭代→月评测→季度定型」三级验证节奏，用「印刷质量指标(字模清晰度/套印精度/速度)」硬指标做红绿灯",
            "第4步：统一战线法——组织「中科院做理论、工厂做工艺、报社做试用」三方联合攻关，利益捆绑共担风险",
            "第5步：制度化制衡——推动「GB/T 编码标准、字模数据标准、接口协议标准」三大国家标准落地，以标准定生态、防锁定"
        ],
        "steps_en": [
            "Step 1: Contradiction Analysis — Identify 'Font Generation, Optical Focusing, Real-time Control' 3 Core Contradictions, Lock '7000 Chinese Characters Real-time High-Quality Imaging' as Principal Contradiction",
            "Step 2: Relentless Perseverance — Decompose Each Major Module into 'Daily Update → Retrospective Closure → Negative Checklist → Legacy Documentation' 4 Standard Actions, Build 200+ Sub-task Kanban",
            "Step 3: Crossing River by Feeling Stones — Design 'Weekly Iteration → Monthly Evaluation → Quarterly Finalization' 3-Level Verification Rhythm, Use 'Print Quality Metrics (Font Clarity/Registration Precision/Speed)' Hard Metrics as Traffic Lights",
            "Step 4: United Front — Organize 'CAS Theory + Factory Process + Newspaper Trial' Tripartite Joint Attack, Interest Binding Shared Risk",
            "Step 5: Institutional Checks — Push 'GB/T Encoding Standard, Font Data Standard, Interface Protocol Standard' 3 National Standards, Standard-Setting Ecosystem, Anti-Lock-in"
        ],
        "expected_zh": [
            "研制「华光激光照排系统」，打破日美垄断",
            "中国印刷成本降低 90%",
            "提出「三个面向」工程化标准",
            "建立「院所-工厂-用户」三位一体产学研模式"
        ],
        "expected_en": [
            "Developed HuaGuang Laser Phototypesetting System, Broke Japan-US Monopoly",
            "Chinese Printing Cost Reduced by 90%",
            "Proposed 'Three Orientations' Engineering Standards",
            "Established 'Institute-Factory-User' Trinity Industry-University-Research Model"
        ],
        "case_zh": "1975 年启动激光照排研究，面对「字模生成、光学聚焦、实时控制」三大核心难题，王选带领团队用「笨功夫」攻关：字模设计从 0 到 7000 字×200 字体，光学系统试制 50 多台，控制系统修改 200 多版；1985 年「华光一号」定型，1988 年「华光二号」达到国际先进水平，打破日美垄断；印刷成本从每千字 200 元降至 20 元；推动 GB 2312/GBK/GB 18030 编码标准、字模数据标准、接口协议标准落地，确立「院所-工厂-用户」产学研生态。",
        "case_en": "1975 Launched Laser Phototypesetting Research, Facing 'Font Generation, Optical Focusing, Real-time Control' 3 Core Challenges, Wang Led Team with 'Relentless Perseverance': Font Design 0→7000 chars×200 fonts, Optical System 50+ Prototypes, Control System 200+ Versions; 1985 'HuaGuang No.1' Finalized, 1988 'HuaGuang No.2' Reached International Advanced Level, Broke Japan-US Monopoly; Printing Cost from 200 RMB/1000 chars → 20 RMB; Pushed GB 2312/GBK/GB 18030 Encoding Standards, Font Data Standards, Interface Protocol Standards, Established 'Institute-Factory-User' Industry-University-Research Ecosystem."
    },
    {
        "code": "H-YLP-137",
        "name_zh": "袁隆平：杂交水稻之父 / \"两系法\"突破者 / 粮食安全战略科学家",
        "name_en": "Yuan Longping: Father of Hybrid Rice / 'Two-Line Method' Breakthrough Pioneer / Strategic Scientist of Food Security",
        "description_zh": "杂交水稻/三系法/两系法/不育系/超级稻/亩产破千公斤/粮食安全/良种繁推体系",
        "description_en": "Hybrid Rice/Three-Line/Two-Line/Male Sterile/Super Hybrid/1000kg per Mu/Food Security/Seed Extension System",
        "modes": [1, 36, 23, 24, 41],
        "reason_zh": "核心思维：在「水稻自花授粉、杂种优势利用难」的生物学铁律下，用「找野败→育保持→配组配→试制种」四步法攻克「三系法」；再用「两系法」(利用光温敏核不育系) 突破「恢复系难找」瓶颈，实现「任意品种均可作父本」，将杂交制种成本降低 50%、亩产突破 900kg→1000kg→1200kg 三级台阶；建立「国家级-省级-县级」三级良种繁推体系，覆盖 2 亿亩/年，直接养活 8000 万+人口/年。",
        "reason_en": "Core Thinking: Under Biological Iron Law 'Rice Self-Pollinating, Heterosis Hard to Exploit', Used 'Find Wild Abortive → Breed Maintainer → Match Restorer → Trial Seed Production' 4-Step Method to Crack 'Three-Line Method'; Then 'Two-Line Method' (Using Photo-Thermo-Sensitive Male Sterile Lines) Broke 'Restorer Hard to Find' Bottleneck, Achieved 'Any Variety Can Be Male Parent', Reduced Hybrid Seed Cost 50%, Yield Broke 900kg→1000kg→1200kg Three Tiers; Built 'National-Provincial-County' Three-Level Seed Extension System, Covering 200M Mu/Year, Directly Feeding 80M+ People/Year.",
        "steps_zh": [
            "第1步：矛盾分析法——定位「自花授粉=主矛盾、不育系=关键杠杆」，在「主矛盾的非本质环节」(光温敏感性) 找到突破口",
            "第2步：笨功夫/死磕到底——建立「年种万份组合→逐粒观察→逐代筛选→负面清单归档」育种流水线，30 年累计杂交组合 20 万+",
            "第3步：两系法降维打击——用「自然选择法」+「间断均衡法」利用「环境诱导不育」这一「短暂剧变机制」，绕过「基因型恢复系」刚性约束，实现「全品种可配」范式跃迁",
            "第4步：驿站制/信息流速——建立「育种→试验→示范→推广→反馈」五级流速体系，将新品种从「育成」到「大面积推广」周期从 8 年压缩至 3 年"
        ],
        "steps_en": [
            "Step 1: Contradiction Analysis — Locate 'Self-Pollination = Principal Contradiction, Male Sterile Line = Key Leverage', Find Breakthrough in 'Non-Essential Aspect of Principal Contradiction' (Photo-Thermo Sensitivity)",
            "Step 2: Relentless Perseverance — Build 'Annual 10k+ Crosses → Grain-by-Grain Observation → Generation-by-Generation Screening → Negative Checklist Archive' Breeding Pipeline, 30 Years 200k+ Hybrid Combinations",
            "Step 3: Two-Line Method Dimensional Strike — 'Natural Selection' + 'Punctuated Equilibrium' Leverage 'Environment-Induced Sterility' 'Brief Catastrophe Mechanism', Bypass 'Genotypic Restorer' Rigid Constraint, Achieve 'All Varieties Can Be Male Parent' Paradigm Leap",
            "Step 4: Relay Station/Info Flow — Build 'Breeding → Trial → Demonstration → Extension → Feedback' 5-Level Flow System, Compress New Variety 'Breeding → Mass Extension' Cycle from 8 Years to 3 Years"
        ],
        "expected_zh": [
            "攻克「三系法」，建立杂交水稻技术体系",
            "「两系法」突破恢复系瓶颈，制种成本降 50%",
            "超级稻亩产三级跳：900→1000→1200kg",
            "三级良种繁推体系覆盖 2 亿亩/年，养活 8000 万+人口/年"
        ],
        "expected_en": [
            "Cracked 'Three-Line Method', Established Hybrid Rice Technical System",
            "'Two-Line Method' Broke Restorer Bottleneck, Seed Cost Reduced 50%",
            'Super Hybrid Rice Yield Three Tiers: 900→1000→1200kg per Mu',
            'Three-Level Seed Extension System Covers 200M Mu/Year, Feeds 80M+ People/Year'
        ],
        "case_zh": "1973 年利用「野败稻」攻克「三系法」，确立杂交水稻技术体系；1980 年代提出「两系法」构想，利用「光温敏核不育系」突破「恢复系难找」瓶颈，实现「全品种可配」；1990 年代推进「超级稻」工程，亩产三级跳：900kg→1000kg→1200kg；建立「国家级-省级-县级」三级良种繁推体系，覆盖 2 亿亩/年，直接养活 8000 万+人口/年；杂交水稻推广面积累计超 10 亿亩，直接养活数亿人口。",
        "case_en": "1973 Used 'Wild Abortive Rice' to Crack 'Three-Line Method', Established Hybrid Rice Technical System; 1980s Proposed 'Two-Line Method', Leveraged 'Photo-Thermo-Sensitive Male Sterile Lines' to Break 'Restorer Hard to Find' Bottleneck, Achieved 'All Varieties Can Be Male Parent'; 1990s Advanced 'Super Hybrid Rice' Project, Yield Three Tiers: 900→1000→1200kg/Mu; Built 'National-Provincial-County' Three-Level Seed Extension System, Covering 200M Mu/Year, Directly Feeding 80M+ People/Year; Hybrid Rice Cumulative Extension > 1 Billion Mu, Directly Feeding Hundreds of Millions."
    },
    {
        "code": "H-LYY-138",
        "name_zh": "屠呦呦：青蒿素发现者 / 中西医结合药物筛选范式创始人 / 诺贝尔奖得主",
        "name_en": "Tu Youyou: Discoverer of Artemisinin / Founder of TCM-Western Medicine Drug Screening Paradigm / Nobel Laureate",
        "description_zh": "青蒿素/疟疾/中药单体/结构确证/合成类似物/临床验证/民族药物现代化/诺贝尔生理学或医学奖",
        "description_en": "Artemisinin/Malaria/TCM Monomer/Structure Confirmation/Synthetic Analogs/Clinical Validation/Ethnic Drug Modernization/Nobel Physiology or Medicine",
        "modes": [25, 1, 5, 34],
        "reason_zh": "核心思维：在「单一化合物筛选失败、传统方剂成分复杂、提取工艺不可控」三重死局中，用「文献考据+化学分离+药效验证」三重交叉验证法：从《肘后备急方》「青蒿一握，以水二升渍，绞取汁, 尽服之」获启发，改「沸水煎」为「低温乙醚提取」保留热稳定性差的活性成分，提取率从 0%→95%；建立「中药单体→结构确证→合成类似物→临床验证」全链路标准，开创「民族医药现代化」新范式，挽救全球数千万生命。",
        "reason_en": "Core Thinking: In Triple Deadlock of 'Single Compound Screening Failed, Traditional Formula Components Complex, Extraction Process Uncontrollable', Used 'Literature Excavation + Chemical Separation + Efficacy Verification' Triple Cross-Validation: From Handbook of Prescriptions for Emergencies 'One Handful of Artemisia, Soaked in 2 Liters Water, Wring Juice, Drink All' got Inspiration, Changed 'Boiling Water Decoction' to 'Low-Temperature Ether Extraction' Retaining Heat-Labile Active Ingredient, Extraction Rate 0%→95%; Established 'TCM Monomer → Structure Confirmation → Synthetic Analogs → Clinical Validation' Full-Chain Standard, Pioneered 'Ethnic Medicine Modernization' New Paradigm, Saved Tens of Millions of Lives Globally.",
        "steps_zh": [
            "第1步：抽象归纳法——从 2000+ 古方中提炼「疟疾/间歇热/寒热」关键词，建立「方剂-症候-成分」三维检索库，锁定 380 个候选方剂",
            "第2步：矛盾分析法——定位「高温煎煮=主矛盾破坏活性成分」，反向设计「低温/非极性溶剂/快速分离」反常规工艺，打破「水煎」路径依赖",
            "第3步：实事求是——设计「小鼠/猴子/人体」三物种、「单体/合剂/合成类似物」三形态、「体内/体外/临床」三场景交叉验证矩阵，消除单点偶然",
            "第4步：制度化制衡——将「提取工艺SOP、质控标准、临床方案、专利布局」打包为可移植「青蒿素技术包」，支撑全球推广"
        ],
        "steps_en": [
            "Step 1: Abstract Induction — From 2000+ Ancient Formulas Extract 'Malaria/Intermittent Fever/Chill-Heat' Keywords, Build 'Formula-Symptom-Ingredient' 3D Retrieval Library, Lock 380 Candidate Formulas",
            "Step 2: Contradiction Analysis — Locate 'High-Temp Decoction = Principal Contradiction Destroying Active Ingredient', Reverse-Design 'Low-Temp/Non-Polar Solvent/Quick Separation' Counter-Conventional Process, Break 'Water Decoction' Path Dependence",
            "Step 3: Seek Truth from Facts — Design 'Mice/Monkeys/Humans' 3 Species, 'Monomer/Compound/Synthetic Analogs' 3 Forms, 'In Vivo/In Vitro/Clinical' 3 Scenarios Cross-Validation Matrix, Eliminate Single-Point Chance",
            "Step 4: Institutional Checks — Package 'Extraction Process SOP, QC Standards, Clinical Protocol, Patent Layout' into Portable 'Artemisinin Tech Package', Support Global Rollout"
        ],
        "expected_zh": [
            "青蒿素提取率 0%→95%，挽救全球数千万生命",
            "建立「中药单体→结构确证→合成类似物→临床验证」全链路标准",
            "开创「民族医药现代化」新范式",
            "2015 获诺贝尔生理学或医学奖"
        ],
        "expected_en": [
            "Artemisinin Extraction Rate 0%→95%, Saved Tens of Millions of Lives Globally",
            "Established 'TCM Monomer → Structure Confirmation → Synthetic Analogs → Clinical Validation' Full-Chain Standard",
            "Pioneered 'Ethnic Medicine Modernization' New Paradigm",
            "2015 Nobel Prize in Physiology or Medicine"
        ],
        "case_zh": "1969 年「523 任务」启动，屠呦呦带领课题组从 2000+ 古方中筛选；从《肘后备急方》「青蒿一握，以水二升渍，绞取汁, 尽服之」获启发，改「沸水煎」为「低温乙醚提取」保留热稳定性差的活性成分，提取率从 0%→95%；建立「中药单体→结构确证→合成类似物→临床验证」全链路标准，开创「民族医药现代化」新范式，挽救全球数千万生命；2015 获诺贝尔生理学或医学奖。",
        "case_en": "1969 'Project 523' Launched, Tu Led Team Screening 2000+ Ancient Formulas; From Handbook of Prescriptions 'One Handful Artemisia, Soaked in 2 Liters Water, Wring Juice, Drink All' Got Inspiration, Changed 'Boiling Water Decoction' to 'Low-Temp Ether Extraction' Retaining Heat-Labile Active Ingredient, Extraction Rate 0%→95%; Established 'TCM Monomer → Structure Confirmation → Synthetic Analogs → Clinical Validation' Full-Chain Standard, Pioneered 'Ethnic Medicine Modernization' Paradigm, Saved Tens of Millions Globally; 2015 Nobel Physiology or Medicine."
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
with open('scenarios_en.json', 'w', encoding