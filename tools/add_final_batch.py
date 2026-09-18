import json

# Load existing data
with open('scenarios_zh.json', 'r', encoding='utf-8') as f:
    zh = json.load(f)
with open('scenarios_en.json', 'r', encoding='utf-8') as f:
    en = json.load(f)
with open('code_maps.json', 'r', encoding='utf-8') as f:
    cm = json.load(f)

# New entries to add (final 3 high-priority figures)
new_entries = [
    {
        "code": "H-KZ-142",
        "name_zh": "孔子：儒家创始人 / 仁礼中庸 / 教育思想 / 六艺 / 三千弟子 / 春秋笔法",
        "name_en": "Confucius: Founder of Confucianism / Ren-Li-Zhongyong / Education Thought / Six Arts / Three Thousand Disciples / Spring and Autumn Annals",
        "description_zh": "仁/礼/中庸/孝悌/忠恕/君子/正名/因材施教/有教无类/编诗书定礼乐制春秋",
        "description_en": "Ren/Li/Zhongyong/Filial Piety/Loyalty-Reciprocity/Junzi/Rectification of Names/Teaching by Aptitude/Universal Education/Editing Classics",
        "modes": [1, 5, 6, 22, 37],
        "reason_zh": "核心思维：在「礼崩乐坏、百家争鸣」的春秋乱世，以「仁者爱人、礼治天下」构建伦理政治体系——「克己复礼为仁」将道德内化为自我约束，「君君臣臣父父子子」确立角色伦理秩序，「因材施教/有教无类」打破贵族教育垄断，创立「士」阶层流动通道；《春秋》笔法「微言大义」确立史学褒贬法，奠定中国两千年正统思想基石。",
        "reason_en": "Core Thinking: In the Spring-Autumn chaos of 'Collapsed Rites, Contending Schools', built ethical-political system with 'Ren loves people, Li governs world' — 'Self-restraint returns to Li is Ren' internalizes morality as self-discipline; 'Ruler-Ruler, Minister-Minister, Father-Father, Son-Son' establishes role ethics; 'Teaching by Aptitude, Universal Education' breaks aristocratic education monopoly, creates 'Shi' class mobility channel; Spring and Autumn Annals 'Subtle Words Great Meaning' establishes historical praise-blame method, laying China's 2000-year orthodox thought foundation.",
        "steps_zh": [
            "第1步：矛盾分析法——识别「礼崩乐坏」为主矛盾，主矛盾主方面为「统治合法性缺失/伦理秩序瓦解」，以「仁/礼」双轮驱动重构秩序",
            "第2步：实事求是法——不造玄虚、不谈怪力乱神，专注「人伦日用」切身道德实践，「不知生焉知死」拒绝形而上投机",
            "第3步：统一战线法——「三千弟子七十二贤」，不问出身贵贱、贫富贤愚，以「有教无类」聚合跨阶层共同体，以「因材施教」实现个性化培养",
            "第4步：总体性思维法——构建「仁-礼-乐-书-易-春秋」六经体系，将伦理/政治/教育/历史/音乐/占卜融为一体，形成可传承的文明基因库",
            "第5步：知行合一/致良知——「吾十有五而志于学...七十而从心所欲不逾矩」，以身试法，道德修养从「志学」到「不逾矩」的全生命周期践行"
        ],
        "steps_en": [
            "Step 1: Contradiction Analysis — Identify 'Collapsed Rites' as principal contradiction, main aspect 'Lost Legitimacy/Ethical Order Collapse', dual-drive reconstruction with 'Ren/Li'",
            "Step 2: Seek Truth from Facts — No metaphysics, no supernatural, focus on 'Daily Human Ethics' concrete practice, 'Not knowing life, how know death' rejecting metaphysical speculation",
            "Step 3: United Front — '3000 Disciples 72 Worthies', regardless of origin/status/wealth, 'Universal Education' aggregates cross-class community, 'Teaching by Aptitude' enables individualized cultivation",
            "Step 4: Systems Thinking — Build 'Ren-Li-Music-Book-Changes-Spring Autumn' Six Classics system, integrating Ethics/Politics/Education/History/Music/Divination into inheritable civilizational gene bank",
            "Step 5: Unity of Knowledge and Action — 'At 15 set heart on learning... at 70 follow heart without transgressing', embodying praxis, moral cultivation full lifecycle from 'Aspire to Learn' to 'Not Transgressing'"
        ],
        "expected_zh": [
            "创立儒家学派，确立「仁/礼/中庸」核心价值体系",
            "「有教无类/因材施教」开启平民教育先河",
            "《春秋》确立史学褒贬法，两千年正统思想奠基",
            "弟子遍布诸国，形成「士」阶层流动通道，改变中国社会结构"
        ],
        "expected_en": [
            "Founded Confucianism, Established 'Ren/Li/Zhongyong' Core Value System",
            "'Universal Education/Teaching by Aptitude' Opened Commoner Education Pioneer",
            "Spring Autumn Annals Established Historical Praise-Blame Method, 2000-Year Orthodox Foundation",
            "Disciples Across States, Formed 'Shi' Class Mobility Channel, Changed Chinese Social Structure"
        ],
        "case_zh": "鲁定公问政：「君使臣以礼，臣事君以忠」——孔子将「君臣」关系从「权力服从」重利」重构为「礼义互惠」。齐景公问政：「君君臣臣父父子子」——以「名正言顺」重构角色伦理。子路问事鬼神：「未能事人，焉能事鬼」——拒绝神权干预世俗政治。颜渊问仁：「克己复礼为仁」——将道德内化为自我约束机制。子贡问「一言而可以终身行之者乎」：「己所不欲勿施于人」——黄金法则作为普世伦理算法。编《诗》《书》、定《礼》《乐》、修《春秋》，系统整理文明遗产。临终前「吾其尝为东周之史乎」，以史自任，完成文明基因传递。",
        "case_en": "Duke Ding of Lu Asked Governance: 'Ruler employs minister with Li, minister serves ruler with loyalty' — Confucius reconstructed 'Ruler-Minister' from 'Power Obedience' to 'Mutual Li-Righteousness'. Duke Jing of Qi Asked Governance: 'Ruler-Ruler, Minister-Minister, Father-Father, Son-Son' — 'Rectification of Names' reconstructs role ethics. Zilu Asked About Spirits: 'Cannot serve people, how serve spirits' — Rejected theocracy interfering secular politics. Yan Yuan Asked Ren: 'Self-restraint returns to Li is Ren' — Moral internalized as self-constraint mechanism. Zigong Asked 'One Word for Life': 'What you don't want, don't do to others' — Golden Rule as Universal Ethics Algorithm. Edited Poetry/Books, Fixed Rites/Music, Repaired Spring Autumn, systematically organized civilizational heritage. Before death: 'I once served as Historian of Eastern Zhou', took history as mission, completed civilizational gene transmission."
    },
    {
        "code": "H-LXN-143",
        "name_zh": "李先念：经济战略预判家 / \"调整改革\"总设计师 / 金融体系建设者 / 八届三中全会\"八字方针\"主持者",
        "name_en": "Li Xiannian: Economic Strategic Foresight Master / 'Readjustment Reform' Chief Architect / Financial System Builder / Presider of 8th Plenum 'Eight-Character Policy'",
        "description_zh": "八字方针/调整巩固充实提高/国民经济比例关系/财政金融体制改革/利改税/央行专业化",
        "description_en": "Eight-Character Policy/Readjustment Consolidation Enrichment Improvement/National Economic Proportions/Fiscal Financial Reform/Profit-to-Tax/Central Bank Professionalization",
        "modes": [7, 19, 38, 39, 34],
        "reason_zh": "核心思维：在「大跃进后经济崩溃、三年困难、文革动荡」三重冲击下，主持「八字方针(调整、巩固、充实、提高)」「国民经济比例关系」「财政金融体制改革」三大战略工程：用「战略预判」识别「投资过热→比例失衡→通胀→崩溃」传导链，设计「压缩基本建设规模、调整产品结构、下放企业权力」三招组合拳；创立「利改税、分灶吃饭、央行专业化」财政金融现代化框架，为 90 年代朱镕基改革预埋制度种子。",
        "reason_en": "Core Thinking: Under Triple Shock of 'Post-Great Leap Economic Collapse, Three-Year Difficulty, Cultural Revolution Turmoil', Presided 'Eight-Character Policy (Readjust, Consolidate, Enrich, Improve)', 'National Economic Proportional Relations', 'Fiscal Financial System Reform' Three Strategic Projects: Used 'Strategic Foresight' to Identify 'Investment Overheating → Proportional Imbalance → Inflation → Collapse' Transmission Chain, Designed 'Compress Basic Construction Scale, Adjust Product Structure, Devolve Enterprise Power' Three-Punch Combo; Created 'Profit-to-Tax, Separate Kitchen Eating, Central Bank Professionalization' Fiscal Financial Modernization Framework, Planting Institutional Seeds for 1990s Zhu Rongji Reforms.",
        "steps_zh": [
            "第1步：战略预判法——监测「投资增速/物价指数/货币供给/财政赤字」四大先行指标，建立「红绿灯预警阈值」(如基本建设投资增速>20%触发红灯)",
            "第2步：边际思维——计算「压缩基本建设 1 元→释放流动资金/农业/轻工/出口创汇」边际收益排序，优先配置高边际收益领域",
            "第3步：摸石头过河——设计「扩大企业自主权(生产/销售/用工/财务/投资)→亏损自负/盈利留成→税利分流」试点包，在「鸟笼」内放飞",
            "第4步：鸟笼经济/边界思维——推动「利改税、分灶吃饭、央行剥离商业职能→专业银行分设→间接调控工具(存准/利率/再贴现)建立」三步走，为市场化利率奠基",
            "第5步：制度化制衡——推动「央行剥离商业职能→专业银行分设→间接调控工具建立」三步走，为市场化利率奠基"
        ],
        "steps_en": [
            "Step 1: Strategic Foresight — Monitor 'Investment Growth/CPI/Money Supply/Fiscal Deficit' Four Leading Indicators, Build 'Traffic Light Warning Thresholds' (e.g. Basic Construction Investment Growth >20% Triggers Red Light)",
            "Step 2: Marginal Thinking — Calculate 'Compress Basic Construction 1 Yuan → Release Working Capital/Agriculture/Light Industry/Export Forex' Marginal Benefit Ranking, Prioritize High Marginal Return Sectors",
            "Step 3: Crossing River by Feeling Stones — Design 'Expand Enterprise Autonomy (Production/Sales/Labor/Finance/Investment) → Loss Self-Borne/Profit Retained → Tax-Profit Sharing' Pilot Package, Release Within 'Birdcage'",
            "Step 4: Birdcage Economy/Boundary Thinking — Push 'Profit-to-Tax, Separate Kitchen Eating, Central Bank Strips Commercial Functions → Specialized Banks Separated → Indirect Control Tools (RRR/Interest Rate/Rediscount) Established' Three-Step Walk, Laying Foundation for Market Interest Rates",
            "Step 5: Institutional Checks — Push 'Central Bank Strips Commercial Functions → Specialized Banks Separated → Indirect Control Tools Established' Three-Step, Laying Foundation for Market Interest Rates"
        ],
        "expected_zh": [
            "「八字方针」三年国民经济初步好转，财政由赤字转盈余",
            "「国民经济比例关系」建立投资/消费/积累/消费黄金比例",
            "「利改税/分灶吃饭/央行专业化」财政金融现代化框架落地",
            "为 90 年代朱镕基「利改税、分灶吃饭、央行专业化」预埋制度种子"
        ],
        "expected_en": [
            "'Eight-Character Policy' Three Years Economy Initially Improved, Fiscal Deficit Turned Surplus",
            "'National Economic Proportions' Established Investment/Consumption/Accumulation Golden Ratio",
            "'Profit-to-Tax/Separate Kitchen Eating/Central Bank Professionalization' Fiscal Financial Modernization Framework Landed",
            "Planted Institutional Seeds for 1990s Zhu Rongji 'Profit-to-Tax, Separate Kitchen Eating, Central Bank Professionalization'"
        ],
        "case_zh": "1961 年任国务院副总理分管财经，面对「大跃进后经济崩溃、三年困难」：主持制定「八字方针」，压缩基本建设投资从 389 亿→130 亿，钢铁产量从 1866 万吨→800 万吨，财政赤字三年消除；1979 年主持「八届三中全会」确立「调整、巩固、充实、提高」八字方针，压缩基本建设 500 亿，下放企业「生产、销售、用工、财务、投资」五大权力；1980 年代主持「利改税」试点，「分灶吃饭」财政包干，「央行剥离商业职能」建立中国人民银行专业化，为 90 年代金融体制改革预埋种子。",
        "case_en": "1961 Became Vice Premier in Charge of Finance, Facing 'Post-Great Leap Collapse, Three-Year Difficulty': Presided 'Eight-Character Policy', Compressed Basic Construction Investment 38.9B→13B, Steel Output 18.66M→8M Tons, Fiscal Deficit Eliminated in Three Years; 1979 Presided 8th Plenum 'Eight-Character Policy', Compressed Basic Construction 50B, Devolved Enterprises 'Production/Sales/Labor/Finance/Investment' Five Powers; 1980s Presided 'Profit-to-Tax' Pilot, 'Separate Kitchen Eating' Fiscal Contracting, 'Central Bank Strips Commercial Functions' Established PBOC Professionalization, Planting Seeds for 1990s Financial Reform."
    },
    {
        "code": "H-CY-144",
        "name_zh": "陈毅：山东游击战创建者 / 华东野战军政委 / 外交部长 / \"诗军外交\"跨界实践者",
        "name_en": "Chen Yi: Founder of Shandong Guerrilla Warfare / Political Commissar of East China Field Army / Foreign Minister / 'Poet-Soldier Diplomacy' Cross-Domain Practitioner",
        "description_zh": "游击战/根据地建设/三三制政权/统一战线/外交诗词/山东根据地/华东野战军/诗军外交",
        "description_en": "Guerrilla Warfare/Base Area Construction/Three-Thirds Regime/United Front/Diplomatic Poetry/Shandong Base Area/East China Field Army/Poet-Soldier Diplomacy",
        "modes": [16, 22, 6, 31, 17],
        "reason_zh": "核心思维：创立「游击根据地建设=政权建设+武装建设+经济建设+文化建设」四位一体模式：在山东「敌强我弱、地盘碎片化」条件下，用「游击战十六字诀」积累力量，同步推行「抗日民主政权(三三制)→统一战线(抗日联合会)→根据地经济(公债/合作社/统购统销)→文化动员(抗日剧团/壁报/识字班)」四大支柱；外交转型期用「诗军外交」——以诗人身份软化外交硬度，用「陈毅诗稿」作为破冰文化符号，在日内瓦/万隆/联大舞台实现「文化破冰→政治对话→外交突围」跨界复用。",
        "reason_en": "Core Thinking: Created 'Guerrilla Base Construction = Regime Building + Armed Building + Economic Building + Cultural Building' Four-in-One Model: In Shandong 'Enemy Strong/Us Weak, Territory Fragmented', used 'Sixteen-Character Formula' to accumulate power, simultaneously pushed 'Anti-Japanese Democratic Regime (Three-Thirds System) → United Front (Anti-Japanese Union) → Base Economy (Public Bonds/Cooperatives/Unified Purchase-Sale) → Cultural Mobilization (Anti-Japanese Drama Troupes/Wall Posters/Literacy Classes)' Four Pillars; Diplomatic Transition used 'Poet-Soldier Diplomacy' — Poet identity softens diplomatic hardness, used 'Chen Yi Poems' as ice-breaking cultural symbols, achieving 'Cultural Ice-Breaking → Political Dialogue → Diplomatic Breakthrough' cross-domain reuse at Geneva/Bandung/UNGA.",
        "steps_zh": [
            "第1步：游击战十六字诀——设计「敌进我退(保存核心)→敌驻我扰(切断交通)→敌疲我打(建立政权)→敌退我追(连片根据地)」四阶段空间织网算法",
            "第2步：总体性思维——将「政权/武装/经济/文化」四系统耦合，建立「政权供给人员→武装保卫政权→经济供养武装→文化凝聚人心」正反馈闭环",
            "第3步：统一战线三三制——推行「共产党/非党进步分子/中间派」各 1/3 政权组成，最大化根据地政治包容度",
            "第4步：框架效应法——将「将军/诗人/外交官」三重身份重构为「文化使者」单一框架，用诗作/书法/幽默作为「非官方外交货币」",
            "第5步：多元思维模型——将「军事指挥→政治建设→经济管理→文化传播→外交谈判」五域能力建立「核心能力迁移矩阵」，实现人才跨域复用"
        ],
        "steps_en": [
            "Step 1: Sixteen-Character Formula — Design 'Enemy Advances We Retreat (Preserve Core) → Enemy Halts We Harass (Cut Transport) → Enemy Tires We Strike (Establish Regime) → Enemy Retreats We Pursue (Connect Base Areas)' 4-Stage Spatial Weaving Algorithm",
            "Step 2: Systems Thinking — Couple 'Regime/Armed/Economy/Culture' Four Systems, Build 'Regime Supplies Personnel → Armed Guards Regime → Economy Supports Armed → Culture Cohesion' Positive Feedback Loop",
            "Step 3: United Front Three-Thirds System — Implement 'CPC/Non-Party Progressives/Intermediates' Each 1/3 Regime Composition, Maximize Base Political Inclusivity",
            "Step 4: Framing Effect — Reconstruct 'General/Poet/Diplomat' Triple Identity into 'Cultural Envoy' Single Frame, Use Poems/Calligraphy/Humor as 'Unofficial Diplomatic Currency'",
            "Step 5: Multi-Model Thinking — Build 'Core Capability Transfer Matrix' across 'Military Command → Political Building → Economic Management → Cultural Transmission → Diplomatic Negotiation' Five Domains, Enable Cross-Domain Talent Reuse"
        ],
        "expected_zh": [
            "创立「游击根据地=政权+武装+经济+文化」四位一体建设模式",
            "山东根据地从零建成 500 万人口根据地，华东野战军成长为 60 万主力",
            "外交部长任内：1954 日内瓦会议、1955 万隆会议、联大恢复合法席位",
            "「陈毅诗稿」成为非官方外交货币，创立「诗军外交」跨界范式"
        ],
        "expected_en": [
            "Created 'Guerrilla Base = Regime+Armed+Economy+Culture' Four-in-One Construction Model",
            "Shandong Base from Zero to 5M Population Base, East China Field Army Grew to 600k Main Force",
            "Foreign Minister Tenure: 1954 Geneva, 1955 Bandung, UN Restoration of Legitimate Seat",
            "'Chen Yi Poems' Became Unofficial Diplomatic Currency, Founded 'Poet-Soldier Diplomacy' Cross-Domain Paradigm"
        ],
        "case_zh": "1938 年率新四军支队东进抗日，面对「敌强我弱、地盘碎片化」：用「游击战十六字诀」织网，1940 年黄桥决战以少胜多确立苏中根据地；1941-1943 「苏中七战七捷」确立华中根据地核心地位；建立「三三制」抗日民主政权，推行「公债/合作社/统购统销」根据地经济，组建「抗日剧团/识字班/壁报」文化动员。1954 日内瓦会议：以「将军诗人」形象破冰，用《过十六家岭》等诗作软化西方封锁心理；1955 万隆会议：用「和平共处五项原则」诗意表达破解冷战对峙；1971 联大恢复席位：以「诗人外交」软实力配合原则立场硬实力，实现外交全面突围。",
        "case_en": "1938 Led New Fourth Army Eastward, Facing 'Enemy Strong/Us Weak, Territory Fragmented': Used 'Sixteen-Character Formula' Weaving Net, 1940 Huangqiao Battle Fewer Defeated More Established Su-Zhong Base; 1941-43 'Su-Zhong Seven Victories' Established Huazhong Base Core; Established 'Three-Thirds' Anti-Japanese Democratic Regime, Implemented 'Public Bonds/Cooperatives/Unified Purchase-Sale' Base Economy, Organized 'Anti-Japanese Drama Troupes/Literacy Classes/Wall Posters' Cultural Mobilization. 1954 Geneva: 'General-Poet' Image Ice-Breaking, Used 'Crossing Sixteen Ridges' Poems to Soften Western Blockade Psychology; 1955 Bandung: 'Five Principles of Peaceful Coexistence' Poetic Expression Broke Cold War Confrontation; 1971 UN Restoration: 'Poet Diplomacy' Soft Power Complemented Principle Hard Power, Achieved Comprehensive Diplomatic Breakthrough."
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

print("✅ Added 3 final high-priority figures")