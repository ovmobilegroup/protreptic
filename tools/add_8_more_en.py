import json

# Load existing scenarios
with open('scenarios_en.json', 'r', encoding='utf-8') as f:
    scenarios_en = json.load(f)

# 8 more paradigm figures - English
new_en = {
    "H-SQ-51": {
        "name": "Shang Yang: Legalist Engineering of the State Machine",
        "description": "Wood Trust Establishment / Collective Responsibility Law / Military Merit Rank System / Abolish Well-Field Open Fields / Qin Enrichment Strengthening",
        "modes": [32, 19, 34, 40, 35],
        "reason": "Shang Yang 'law does not favor nobility, rope does not bend for curves'. Core mindset: Legalist thought engineering implementation and state machine manufacturing — served Qin Xiaogong as chancellor, promoted 'Wood Trust Establishment' building government credibility, 'Collective Responsibility Law' implementing joint liability, 'Military Merit Rank System' establishing merit-based ennoblement, 'Abolish Well-Field Open Fields' releasing land productivity, 'Emphasize Agriculture Restrain Commerce' concentrating resources for war. Transformed Legalist thought into operable state operation code, manufactured 'Qin System' the strongest state machine in Chinese history.",
        "steps": [
            "Step 1: Institutional Checks — Wood Trust Establishment: move wood reward fifty gold, build government credibility, 'orders execute prohibitions' foundation",
            "Step 2: Marginal Thinking — Collective Responsibility Law: ten households five households as groups, mutual supervision, concealment not reported same crime, reduce supervision cost",
            "Step 3: Incentive Mechanism — Military Merit Rank: one head one rank, twenty rank system, merit-based ennoblement, break hereditary nobility salaries",
            "Step 4: Institutional Checks — Abolish Well-Field Open Fields: recognize land private ownership, allow trade, state direct taxation, release productivity",
            "Step 5: Strategic Delegation — Professional Division: Shang Yang manages law, Sima Cuo manages army, Gan Long/Du Zhi assist, Qin Xiaogong 'use Shang Jun law, state rich army strong'"
        ],
        "expected": [
            "Qin from weak to strong, unification six states foundation, 'Qin System' became two thousand years imperial model",
            "Collective Responsibility/Military Merit/Open Fields/County System became standard institutional configuration for dynasties",
            "Lessons: Legalism heavy punishment light virtue, Shang Yang torn by chariots, Qin fell in two generations, system rigidity lacked flexibility"
        ],
        "case": "Shang Yang Reforms (356/350 BC): Qin Xiaogong issued 'seek worthy order', Shang Yang entered Qin. First year laws: Wood Trust, Abolish Well-Field, Open Fields, Collective Responsibility, Military Merit Rank, Emphasize Agriculture Restrain Commerce, Standardize Weights Measures, Abolish Hereditary, Establish County System. Second year laws: Household Registration, Reward Farming Weaving, Restrict Merchants, Population Registration. Result: Qin rich state strong army, Wei ceded Hexi, Chu submitted service, six states dared not face east. Shang Yang torn by chariots but laws not abolished, Qin unified six states established 'Qin System'."
    },
    "H-SQ-52": {
        "name": "Su Qin: Strategic Diplomatic Architect of Vertical Alliance Against Qin",
        "description": "Six States Chancellor Seals / Vertical Alliance Against Qin / Diplomatic Game / Interest Binding / Strategic Alliance",
        "modes": [6, 20, 11, 28, 35],
        "reason": "Su Qin 'wore six states chancellor seals', core mindset: strategic alliance construction under asymmetric game — facing strong Qin pressure, created 'Vertical Alliance' strategy: weak unite weak against strong, interest bind six states, common military defense. 'Vertical Alliance means combine six states following to resist Qin', used Qin 'greedy insatiable' psychology, manufactured 'Qin attacks one state, five states rescue' situation. Used tongue as weapon, interest as bond, constructed multi-party checks system.",
        "steps": [
            "Step 1: Contradiction Analysis — Identify Principal Contradiction: Qin strength primary threat, six states division secondary contradiction, Vertical Alliance solves secondary to resist primary",
            "Step 2: United Front — Interest Binding: six states common military/intelligence/diplomacy/economy, Qin attacks one state five states rescue, share intelligence resources",
            "Step 3: Game Theory — Diplomatic Game: separately lobbied six states monarchs ministers, tailored interest plans, used Qin greed manufactured fear",
            "Step 4: Flexible Strategy — Vertical Horizontal Conversion: Vertical fails then Horizontal, adapt to situation, retreat to advance, maintain strategic initiative",
            "Step 5: Institutional Checks — Six States Alliance Mechanism: set alliance leader/alliance pact/common military expenses/intelligence sharing/violation punishment, prevent unilateral betrayal"
        ],
        "expected": [
            "Vertical Alliance maintained 15 years, Qin dared not pass Hangu Pass 15 years, six states relatively safe",
            "Strategic Alliance/Multilateral Diplomacy/Interest Binding became diplomatic textbook case",
            "Lessons: Vertical Alliance loose/lacks core execution/internal suspicion/ultimately broken by Zhang Yi Horizontal each individually crushed"
        ],
        "case": "Vertical Alliance Against Qin (333-318 BC): Su Qin lobbied Yan/Zhao/Han/Wei/Qi/Chu six states, wore six states chancellor seals. Vertical Alliance Pact: Qin attacks one state five states rescue, common military/diplomacy/economy. Qin Huiwen King feared, dared not leave Hangu Pass 15 years. Zhang Yi countered Vertical with Horizontal: induced Han/Wei/Qi/Chu/Yan/Zhao each separately peace with Qin, six states Vertical Alliance collapsed. Su Qin died in Qi, torn by chariots but 'Su Zi' name eternal."
    },
    "H-ZY-53": {
        "name": "Zhang Yi: Horizontal Alliance Breaker Counter-Diplomacy Master",
        "description": "Horizontal Breaks Alliance / Divide and Conquer / Interest Division / Qin Strategy / Counter Game",
        "modes": [6, 20, 11, 28, 35],
        "reason": "Zhang Yi 'Horizontal' broke Su Qin 'Vertical', core mindset: counter-game and divide-conquer art — facing six states Vertical strong alliance, created 'Horizontal' strategy: defeat individually, interest inducement, divide and conquer. 'Horizontal means connect Qin horizontal to combine six states', used six states 'unequal interests/insufficient trust/fear Qin' psychology, lobbied state by state, separate peace. Used 'interest' as blade, 'trust' as bait, precisely dismantled strong alliance.",
        "steps": [
            "Step 1: Game Theory — Identify Ally Cracks: six states interest demands differ/historical grievances/geopolitical competition/power disparity, precise profiling",
            "Step 2: United Front — Interest Division: state by state inducement (territory/passage/marriage/title), separate peace, cut off ally support",
            "Step 3: Flexible Strategy — Retreat to Advance: first show strength then weakness, create urgency, force individual decision",
            "Step 4: Framing Effect — Reframing Choice: 'Serve Qin then peace, not Qin then danger', reframe 'Vertical' as 'self-destruction', 'Horizontal' as 'only way out'",
            "Step 5: Institutional Checks — State by State Treaties: separate treaties/non-aggression/mutual benefit/Qin guarantee/gradual annexation"
        ],
        "expected": [
            "Horizontal successfully dissolved Vertical, Qin defeated six states individually, laid unification foundation",
            "Counter-Alliance/Divide-Conquer/Individual Defeat became Game Theory/Diplomatic Strategy textbook",
            "Lessons: Short-term interest inducement long-term strategic mistake, six states short-sighted/lacked strategic resolve"
        ],
        "case": "Horizontal Breaks Vertical (318-312 BC): Zhang Yi lobbied Han/Wei/Qi/Chu/Yan/Zhao. Persuaded Han: 'Serve Qin then avoid troops, gain Yiyang', Han first peace. Persuaded Wei: 'Serve Qin then avoid troops, gain Hexi', Wei peace. Induced Qi: 'Serve Qin then restore mandate, gain Song/Wei'. Induced Chu: 'Serve Qin then restore Shang/Yu', Chu peace. Yan/Zhao successively submitted. Vertical completely dissolved, Qin defeated individually, ultimately unified six states. Zhang Yi 'tongue gains supremacy', 'tongue labor strong than hundred thousand armies'."
    },
    "H-XH-54": {
        "name": "Xiao He: Xiao Rules Cao Follows Logistics Supply Administrative System Founder",
        "description": "Xiao Rules Cao Follows / Logistics Guarantee / Legal Drafting / Talent Recommendation / Succession Mechanism",
        "modes": [28, 34, 18, 17, 35],
        "reason": "Xiao He 'Xiao Rules Cao Follows, Good Beginning Good End'. Core mindset: logistics determines war victory administrative system design — Chu-Han contention 'Xiao He governs Guanzhong, supplies Liu Bang north campaign never cuts grain', drafted 'Qin Law' as Han Law foundation, recommended Han Xin/Zhang Cang/Chen Ping core talents, established 'Worthy Upright' inspection system, built ancestral temples/palaces/rituals. 'Good Beginning Good End', not compete merit, not boast ability, left retreat routes and backups for Liu Bang.",
        "steps": [
            "Step 1: Redundancy Backup — Logistics Guarantee: Guanzhong granaries/transfer lines/transfer ships/transfer carts/transfer soldiers, multiple lines parallel, ensure frontline absolute advantage",
            "Step 2: Institutional Checks — Legal Drafting: adopt Qin Law remove harsh policies, establish Han Law nine chapters, Xiao Rules Cao Follows, legal stability/continuity/predictability",
            "Step 3: Strategic Delegation — Talent Recommendation: Han Xin 'peerless national talent' strong recommendation, Zhang Cang established law calendar, Chen Ping strategized, Chen Ping/Zhou Bo entrusted succession, talent pipeline construction",
            "Step 4: Strategic Delegation — Succession Mechanism: 'Worthy Upright' inspection system, virtue as basis/talent as supplement, established official selection/evaluation/promotion system",
            "Step 5: Dormant Accumulation — Rear Construction: Guanzhong base/population recovery/economic recovery/military production/intelligence network, provide strategic depth for frontline"
        ],
        "expected": [
            "Chu-Han War Liu Bang 'frontline never cuts grain', logistics advantage became victory key",
            "'Xiao Rules Cao Follows' became Chinese administrative/legal/personnel system cornerstone, continued four hundred years",
            "Lessons: Over-centralization/Lack innovation mechanism/Late years suspicion Han Xin/Systemic rigidity risks"
        ],
        "case": "Chu-Han Logistics War (206-202 BC): Liu Bang north campaign Xiang Yu, Xiao He garrisoned Guanzhong. Grain dispatch: Shaanxi/Henan/Shandong three lines parallel, water land parallel, dedicated personnel, daily clearing. Law: adopted Qin Law, removed harsh, established nine chapters, later 'Xiao Rules Cao Follows' idiom. Talent: Han Xin appointed general, Zhang Cang established law, Chen Ping strategy. Entrustment: Liu Bang deathbed 'state pillars, Chen Ping wisdom surplus, Jiang Hou firm, can entrust great matters', Zhou Bo/Chen Ping eliminated Lu clan established Wen. Result: Han four hundred years foundation, Xiao He merit immeasurable."
    },
    "H-LY-55": {
        "name": "Liu Yan: Fiscal Financial Engineering Salt Iron Canal Transport Master",
        "description": "Ever-Normal Granaries / Salt Iron Transport / Water Land Canal Transport / Fiscal Scheduling / Macro Regulation",
        "modes": [19, 29, 28, 34, 35],
        "reason": "Liu Yan 'out enter have nothing, connect have nothing, state sufficient, family given people sufficient'. Core mindset: fiscal financial engineering and supply chain management master — Tang Daizong/Dezong eras Degree Pay/Salt Iron/Transport Commissioner, created 'Ever-Normal Granaries' stabilize prices, reformed 'Salt Law' monopoly zoning/ticket salt/official supervision merchant transport, built 'Water Land Canal Transport' annual transport million dan, established 'Ever-Normal/Salt Iron/Transport' trinity fiscal system. 'Out enter have nothing, connect have nothing' state macro regulation/micro incentives both emphasized, annual fiscal revenue increase million guan.",
        "steps": [
            "Step 1: Marginal Thinking — Salt Law Innovation: abolished official salt production/changed merchant boiling salt/official collect tax/ticket salt circulation/regional monopoly/crackdown private salt, annual salt profit million guan",
            "Step 2: Institutional Checks — Canal Transport System: water land parallel/dedicated canal boats/canal warehouses/canal soldiers/protect canal army/quota fixed time/annual transport million dan/guarantee Chang'an Luoyang grain supply",
            "Step 3: Feedback Loops — Ever-Normal Granaries: bumper year low price purchase/famine year high price sell/stabilize prices/protect farmers/stabilize market/prevent merchant hoarding",
            "Step 4: Natural Selection — Water Land Parallel: Bian River/Yellow River/Sea transport three lines parallel/mutual backup/risk dispersion/ensure supply security",
            "Step 5: Strategic Delegation — Professional Division: Liu Yan dedicated finance, not military/not power struggle, Degree Pay/Salt Iron/Transport three departments separate, professionals do professional work"
        ],
        "expected": [
            "Tang mid-late fiscal recovery, annual revenue from million guan to ten million guan, supported pacify rebellions/resist foreign",
            "Salt Law/Canal Transport/Ever-Normal Granaries became Tang Song fiscal standard, influenced Song/Yuan/Ming/Qing fiscal systems",
            "Lessons: Relied on personal talent/Lack institutionalization/Dezong suspicion caused death/Posterity Salt Law problems abundant"
        ],
        "case": "Liu Yan Salt Law (760s-780s): Abolished official production, introduced merchants, official collect tax, ticket salt circulation, regional monopoly, annual salt profit million guan. Canal Transport: Bian River/Yellow River/Sea transport three lines, dedicated canal boats ten thousand, canal soldiers hundred thousand, annual transport million dan, protect canal army five thousand. Ever-Normal Granaries: Capital/Eastern Capital/Guanfu/Henan/Hebei establish granaries, harvest low price purchase, famine high price sell, annual low price purchase million dan. Result: Tang Dezong reign fiscal annual income ten million guan, supported pacify Zhu Ci/Li Xilie/Zhexi rebellions."
    },
    "H-QJG-56": {
        "name": "Qi Jiguang: Military Training System Asymmetric Warfare Master",
        "description": "Mandarin Duck Formation / Discipline Construction / Firearms Application / Anti-Wokou Combat / Military System Reform / Record of Military Effectiveness",
        "modes": [15, 11, 40, 28, 35],
        "reason": "Qi Jiguang 'born in worry, die in comfort'. Core mindset: military training systematization and asymmetric warfare practice — Anti-Wokou 'Mandarin Duck Formation' (long short weapons combination/collective tactics/mutual cover), 'Discipline strict, not slightest violation', 'Firearms combine cold weapons' (Folangji/Shenjichong/Huoqiang/Huoqian), compiled 'Record of Military Effectiveness'/'Actual Record of Training Troops' systematized military training/tactics/equipment/psychology. 'General in planning not courage, soldiers in quality not quantity', established China's most scientific military training system.",
        "steps": [
            "Step 1: Mobile Warfare — Mandarin Duck Formation: twelve person squad/long short weapons combination/front back left right mutual cover/collective charge/break enemy scattered braves",
            "Step 2: Institutional Checks — Discipline Construction: 'General orders like mountain, not slightest violation' clear rewards punishments/establish military law/collective responsibility/generals share hardship/establish absolute obedience",
            "Step 3: Natural Selection — Firearms Application: Folangji/Shenjichong/Huoqiang/Huoqian/Cold hot weapons combination/remote firepower suppression/close cold weapons decision",
            "Step 4: Strategic Delegation — Military System Reform: Recruitment system replaces Guards system/professional soldiers/professional training/evaluation promotion/eliminate mediocrity/establish modern army prototype",
            "Step 5: Dormant Accumulation — Writing Books: 'Record of Military Effectiveness' eighteen volumes/'Actual Record of Training Troops'/Systematized training/tactics/equipment/psychology/became military textbook"
        ],
        "expected": [
            "Anti-Wokou great victory/Pacified Fujian/Guangdong/Zhejiang Wokou troubles/Mandarin Duck Formation became China ancient most scientific tactics",
            "'Record of Military Effectiveness' became Ming Qing military textbook/Influenced Li Chengliang/Li Rusong/Later military training",
            "Lessons: Guards system stubborn/Firearms backward/Reform obstructed/Late years impeached dismissed"
        ],
        "case": "Anti-Wokou Mandarin Duck Formation (1555-1567): Qi Jiguang trained 'Mandarin Duck Formation', twelve person squad/long short weapons/collective tactics/mutual cover. Fujian/Guangdong/Zhejiang consecutive battles all victorious, Wokou 'hear wind lose courage'. Firearms: Folangji (Portuguese cannon)/Shenjichong (multi-barrel firearm)/Huoqian/Cold hot weapons combination. Discipline: 'Not slightest violation', people welcomed. Compiled 'Record of Military Effectiveness'/'Actual Record of Training Troops' systematized training/tactics/equipment/camp/orders/flags/firearms/water combat/vehicle combat. Result: Southeast Wokou pacified, Military training systematization became China ancient peak."
    },
    "H-LSZ-57": {
        "name": "Li Shizhen: Pharmaceutical Systematization Empirical Pharmacology Giant",
        "description": "Compendium of Materia Medica / Distinguish False Correct Errors / Classification Grading / Experimental Verification / Knowledge Engineering",
        "modes": [25, 1, 29, 28, 35],
        "reason": "Li Shizhen 'distinguish false correct errors, extensively study classics, personally experience practice', Core mindset: pharmaceutical knowledge systems engineering and empirical pharmacology — 27 years, traversed famous mountains/collected herbs/verified prescriptions, authored 'Compendium of Materia Medica' 52 volumes, 1892 drugs/11096 prescriptions/1160 illustrations. 'Distinguish False Correct Errors' corrected predecessors errors, 'Classification Grading' established paper classification system (16 categories/60 classes/1892 species), 'Personal Practice Verification' empirical verification/distinguish true false/correct errors. 'Syndrome Differentiation Treatment/Formula Syndrome Matching' clinical guidance, established pharmaceutical knowledge engineering standard.",
        "steps": [
            "Step 1: Abstract Induction — Classification Grading: 16 categories (Water/Fire/Earth/Metal/Stone/Grass/Wood/Fruit/Vegetable/Grain/Beast/Bird/Scale/Shell/Insect/Utensil/Human)/60 classes/1892 species/established drug classification science standard",
            "Step 2: Seek Truth from Facts — Distinguish False Correct Errors: Cited 900+ ancient texts/verified origin/distinguished true false/corrected predecessors errors/Such as 'Ginseng not warm/Aconite not hot/Mercury toxic'",
            "Step 3: Natural Selection — Personal Practice Verification: Traversed famous mountains/collected herbs/verified prescriptions/oral taste/skin test/observed reactions/recorded toxicity/established empirical pharmacology data",
            "Step 4: Feedback Loops — Formula Syndrome Correspondence: 11096 prescriptions/Syndrome determines formula/Same disease different treatment/Different diseases same treatment/Clinical guidance/Established Formula Syndrome Matching knowledge base",
            "Step 5: Dormant Accumulation — Knowledge Engineering: 52 volumes/11096 prescriptions/1160 illustrations/Index/Retrieval/Cross-reference/Established Pharmaceutical Knowledge Engineering Standard/Inherited To Present"
        ],
        "expected": [
            "'Compendium of Materia Medica' became World Pharmacology Classic/Darwin/Linnaeus Cited/Translated Multiple Languages/Pharmacology Classification Standard",
            "Classification Science/Empirical Pharmacology/Knowledge Engineering/Clinical Guidance Became TCM/Modern Pharmacology Dual Foundation",
            "Lessons: Theoretical System Closed/Lack Chemical Composition Analysis/Lack Pharmacokinetics/Modern Needs Combine Pharmacology Verification"
        ],
        "case": "Compendium Compilation (1552-1578): Li Shizhen Read Ten Thousand Volumes, Traversed Famous Mountains, Personally Practice Verification. Classification: Water/Fire/Earth/Metal/Stone/Grass/Wood/Fruit/Vegetable/Grain/Beast/Bird/Scale/Shell/Insect/Utensil/Human Sixteen Categories. Distinguish False: Corrected 'Ginseng Great Tonic' Misuse/'Aconite Great Hot' Misuse/'Mercury Longevity' Fallacy. Experiment: Personally Tasted Hundred Herbs/Recorded Toxicity/Established Dosage/Toxicity Data. Prescriptions: 11096/Syndrome Differentiation Treatment/Clinical Practical. Publication Translated Latin/English/French/German/Japanese/Russian/Linnaeus 'Species Plantarum' Cited/Darwin 'Origin of Species' Referenced."
    },
    "H-JSX-58": {
        "name": "Jia Sixie: Agricultural Systems Engineering Technical Standardization Pioneer",
        "description": "Essential Techniques for the Welfare of the People / Eighteen Volumes / Agricultural Seasons Climate / Variety Breeding / Tool Improvement / Technical Standardization",
        "modes": [25, 24, 29, 28, 35],
        "reason": "Jia Sixie 'Ancient Times, People Rich Customs Thick, By Agriculture Then Harvest'. Core Mindset: Agricultural Systems Engineering and Technical Standardization Encyclopedia — Northern Wei/Eastern Wei/Northern Qi Three Dynasties, Authored 'Essential Techniques for the Welfare of the People' Eighteen Volumes, Ninety-Two Chapters, Three Hundred Seventy Thousand Characters. Covers Agricultural Seasons/Climate/Soil/Varieties/Tillage/Irrigation/Fertilization/Harvest/Storage/Processing/Animal Husbandry/Fish Farming/Brewing/Vinegar/Medicine/Disaster Avoidance/Corvee Avoidance. 'Agricultural Seasons Not Lost, Land Utilization Exhausted, Human Effort Exhausted, Varieties Good, Land Fertile, Sowing Time, Seedlings Uniform, Weeds Removed, Ripe Harvest, Early Storage, Good Storage' Twelve Character Formula, Established Agricultural Technical Standardization System.",
        "steps": [
            "Step 1: Abstract Induction — Agricultural Seasons Climate: Twenty-Four Solar Terms/Seventy-Two Pentads/Agricultural Proverbs/Phenological Indicators/Guide Sowing/Harvest/Management/Established Agricultural Time Standard System",
            "Step 2: Systems Thinking — Full Industry Chain: Planting/Breeding/Processing/Storage/Circulation/Consumption/Full Chain Coverage/Established Agricultural Full Industry Chain Knowledge System",
            "Step 3: Natural Selection — Variety Breeding: Wheat/Rice/Millet/Foxtail Millet/Bean/Hemp/Mulberry/Fruit/Vegetable/Medicine/Hundred Plus Crops/Selection/Breeding/Introduction/Established Variety Resource Bank",
            "Step 4: Feedback Loops — Tool Improvement: Curved Shaft Plow/Tube Cart/Water Wheel/Mill/Threshing/Winnowing/Tool Standardization/Operation Standardization/Efficiency Improvement/Technology Diffusion",
            "Step 5: Dormant Accumulation — Practical Encyclopedia: Agriculture/Forestry/Animal Husbandry/Sideline/Fishery/Medical/Engineering/Commerce/Eighteen Volumes/Ninety-Two Chapters/Three Hundred Seventy Thousand Characters/Established Agricultural Practical Encyclopedia Standard"
        ],
        "expected": [
            "'Essential Techniques for the Welfare of the People' Became World Agronomy Classic/Translated Multiple Languages/Influenced East Asia/Europe Agriculture/Agricultural Technical Standardization Ancestor",
            "Agricultural Time Standard/Variety Bank/Tool Standard/Operation Procedure/Full Industry Chain Knowledge System Became Agricultural Technical Standardization Ancestor",
            "Lessons: Theory Leads Practice/Lack Mechanization/Lack Chemical Fertilizer Pesticide/Modern Needs Combine Modern Agricultural Science Verification"
        ],
        "case": "Essential Techniques Compilation (530s-540s): Jia Sixie Three Dynasties Official, Visited Farmers, Field Survey. Eighteen Volumes: Land System/Agricultural Time/Field Family/Sow Grain/Sow Millet/Sow Rice/Sow Bean/Sow Vegetable/Fruit/Tree Arts/Forest/Animal Husbandry Horse/Animal Husbandry Cattle/Animal Husbandry Sheep/Animal Husbandry Pig/Animal Husbandry Chicken/Animal Husbandry Fish/Brewing/Vinegar/Medicine/Avoid Disaster/Avoid Corvee. Twelve Character Formula: 'Agricultural Time Not Lost, Land Utilization Exhausted, Human Effort Exhausted, Varieties Good, Land Fertile, Sow Time, Seedlings Uniform, Weeds Removed, Ripe Harvest, Early Harvest, Storage Firm, Good Storage'. Translated: Tang Translated Into Japan/Song Published/Ming Qing Reprinted/Modern Translated English/French/German/Japanese/Korean/Became World Agronomy Classic."
    },
    "H-WZ-59": {
        "name": "Wei Zheng: Political Supervision Admonition System Designer",
        "description": "Copper Mirror / Two Hundred Plus Remonstrances / Fang Du Complement / Political Feedback / Ruler Minister Co-Governance",
        "modes": [10, 21, 34, 28, 35],
        "reason": "Wei Zheng 'Use Copper as Mirror Can Straighten Clothes; Use History as Mirror Can Know Rise Fall; Use Person as Mirror Can Know Gain Loss', Core Mindset: Political Supervision System and Feedback Loop Design — Tang Taizong 'Good Chancellor', Submitted Remonstrances Two Hundred Plus, 'Fang Plans Du Decides Wei Zheng Supplements Gaps', Established 'Remonstrant Official System/Seal Rebuttal System/Request Remonstrance System', Political Feedback Loop Systematized. 'Gentleman Loves People With Virtue, Petty Person Loves With Indulgence', Dared Direct Remonstrance/Avoided Powerful/Death Remonstrance Not Yield. 'Use History as Mirror Can Know Rise Fall', Established Historical Experience Feedback Mechanism.",
        "steps": [
            "Step 1: Institutional Checks — Remonstrant Official System: Established Remonstrance Doctor/Supplement Omissions/Collect Remnants/Full-time Remonstrance/Grade/Authority/Procedure/Systematized",
            "Step 2: Feedback Loops — Seal Rebuttal System: Secretariat Chancellery Seal Rebuttal/Return Violating Edicts/Force Reconsideration/Prevent Impulsive Decisions/Power Checks",
            "Step 3: Holistic Thinking — Request Remonstrance System: Taizong Established 'Yan Ying Hall Audience'/Regular Face-to-Face Remonstrance/Ruler Minister Dialogue/Psychological Contract/Trust Building",
            "Step 4: Systems Thinking — Historical Feedback: 'Use History as Mirror Can Know Rise Fall', Compiled 'Compendium of Books for Governing'/'Zhenguan Political Essentials'/Historical Experience Feedback Decision",
            "Step 5: Strategic Delegation — Fang Du Complement: Fang Xuanling Plans/Du Ruhui Decides/Wei Zheng Remonstrates/Three Legged Tripod/Complement Complement/Ruler Minister Co-Governance Model"
        ],
        "expected": [
            "Zhenguan Governance/Taizong Accepts Remonstrance/Wei Zheng Remonstrates Two Hundred Plus/Political Supervision Systematized/Ruler Minister Co-Governance Model",
            "Remonstrant/Seal Rebuttal/Request Remonstrance/Historical Mirror Four Major Political Supervision Systems/Influenced Song/Ming/Qing/Modern Supervisory System",
            "Lessons: Taizong Late Years Disliked Remonstrance/Wei Zheng Death Destroyed Stele/System Depends on Monarch Self-Awareness/Lacks Mandatory Enforcement Power"
        ],
        "case": "Wei Zheng Remonstrated Taizong (627-643): Two Hundred Plus Remonstrances/Ten Proposed Ten Followed/Ten Death Ten Survival. Remonstrated Stop Fengshan/Remonstrated Exempt Palace Women/Remonstrated Reduce Taxes/Remonstrated Cautious Punishments/Remonstrated Accept Remonstrance. Taizong 'I Have Wei Zheng, Therefore Not Dare Do Wrong'. Wei Zheng Died, Taizong 'Use Copper as Mirror Can Straighten Clothes; Use History as Mirror Can Know Rise Fall; Use Person as Mirror Can Know Gain Loss'. Compiled 'Compendium of Books for Governing' Fifty Volumes/'Zhenguan Political Essentials' Forty Volumes. Fang Plans Du Decides Wei Zheng Remonstrates, Three Legged Tripod. Result: Zhenguan Governance Became Historical Golden Age Benchmark."
    }
}

# Add to scenarios
scenarios_en.update(new_en)

with open('scenarios_en.json', 'w', encoding='utf-8') as f:
    json.dump(scenarios_en, f, ensure_ascii=False, indent=2)

print(f"Updated scenarios_en.json: {len(scenarios_en)} total scenarios")