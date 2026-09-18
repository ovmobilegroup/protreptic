import json

# Load existing data
with open('scenarios_zh.json', 'r', encoding='utf-8') as f:
    zh = json.load(f)
with open('scenarios_en.json', 'r', encoding='utf-8') as f:
    en = json.load(f)
with open('code_maps.json', 'r', encoding='utf-8') as f:
    cm = json.load(f)

# 10 figures from serrano's phase2_detailed_research.md
new_entries = [
    {
        "code": "H-WGW-170",
        "name_zh": "王国维：二重证据法/境界说/美学实证双绝/近代学术先驱",
        "name_en": "Wang Guowei: Double Evidence Method/Realm Theory/Aesthetic-Empirical Dual Master/Modern Academic Pioneer",
        "description_zh": "二重证据法/境界说/甲骨文/宋词/美学/实证史学/独立精神",
        "description_en": "Double Evidence Method/Realm Theory/Oracle Bones/Ci Poetry/Aesthetics/Empirical Historiography/Independent Spirit",
        "modes": [9, 25, 30, 36, 28],
        "reason_zh": "王国维以「二重证据法」建立现代史学实证范式，通过「境界说」将审美体验抽象为认知阶梯，展现极高的客观性与独立性。",
        "reason_en": "Wang Guowei established modern historiography empirical paradigm with 'Double Evidence Method', abstracted aesthetic experience into cognitive ladder via 'Realm Theory', demonstrating exceptional objectivity and independence.",
        "steps_zh": [
            "第1步：定性——确认研究对象的关键矛盾（历史碎片还是美学概念）",
            "第2步：求证——同步搜集文献记载与考古实物（二重证据）",
            "第3步：抽象——归纳出该现象的最高「境界」或范式",
            "第4步：置换——在不同学科间进行认知阶梯映射",
            "第5步：自省——保持绝对的学术独立与批判意识"
        ],
        "steps_en": [
            "Step 1: Qualify — Identify the key contradiction of the research object (historical fragment or aesthetic concept)",
            "Step 2: Verify — Simultaneously collect literary records and archaeological artifacts (double evidence)",
            "Step 3: Abstract — Extract the highest 'realm' or paradigm of the phenomenon",
            "Step 4: Transpose — Map cognitive ladder across disciplines",
            "Step 5: Self-reflect — Maintain absolute academic independence and critical consciousness"
        ],
        "expected_zh": [
            "「二重证据法」成中国现代史学方法论基石",
            "《人间词话》《境界说》成中国美学现代化奠基之作",
            "甲骨文考释纠正《史记》殷商世系错误，验证实证范式",
            "「独立之精神，自由之思想」成中国现代学术精神图腾"
        ],
        "expected_en": [
            "Double Evidence Method became cornerstone of modern Chinese historiography",
            "Renjian Cihua/Realm Theory became cornerstone of modern Chinese aesthetics",
            "Oracle bone decipherment corrected Shiji Yin-Shang genealogy, validating empirical paradigm",
            "'Independent spirit, free thought' became totem of modern Chinese academic spirit"
        ],
        "case_zh": "王国维（1877-1927），海宁人。早年治经学/文字学，后从罗振玉学甲骨文。1916年《殷卜辞中所见先公先王考》用「二重证据法」纠正《史记》殷商世系，震惊学界。1916年《宋元戏曲考》开中国戏曲史先河。1919年赴日避乱，著《观堂集林》论文集。1924年《人间词话》提出「境界说」：有境界/无境界、造境/写境，以「古今成大事业大学问者，必经过三种境界」三重境界论成中国美学现代化奠基之作。1925年投昆明湖自尽。其「二重证据法/境界说/独立精神」三大贡献，成中国现代学术精神图腾。*   **Reason**: Wang Guowei established modern historiography empirical paradigm with 'Double Evidence Method', abstracted aesthetic experience into cognitive ladder via 'Realm Theory', demonstrating exceptional objectivity and independence.",
        "case_en": "Wang Guowei (1877-1927), Haining native. Early studied classics/philology, later studied oracle bones under Luo Zhenyu. 1916 'Study of Ancestral Kings in Yin Oracle Bones' used Double Evidence Method to correct Shiji Yin-Shang genealogy, shocking academia. 1916 'Study of Song-Yuan Drama' founded Chinese drama history. 1919 fled to Japan, authored Observing Hall Collection essays. 1924 Renjian Cihua proposed 'Realm Theory': with/without realm, creating/depicting realm, 'three realms' theory became foundation of modern Chinese aesthetics. 1925 drowned in Kunming Lake. His 'Double Evidence Method/Realm Theory/independent spirit' three contributions became totem of modern Chinese academic spirit."
    },
    {
        "code": "H-FSN-171",
        "name_zh": "傅斯年：史学组织工程化/考据解释双轨/学术独立/史语所奠基者",
        "name_en": "Fu Sinian: Historiography Organizational Engineering/Dual-track Philology & Interpretation/Academic Independence/Institute of History and Philology Founder",
        "description_zh": "史学组织/考据/解释/学术独立/中央研究院史语所/学术共同体",
        "description_en": "Historiography Organization/Philology/Interpretation/Academic Independence/Institute of History and Philology/Academic Community",
        "modes": [9, 10, 5, 25, 12],
        "reason_zh": "傅斯年是现代学术组织化的领袖，其思维核心是学术独立下的深度考据与组织工程化。        ",
        "reason_en": "Fu Sinian is the leader of modern academic organizationalization, his thinking core is organizational engineering of deep philology under academic independence.",
        "steps_zh": [
            "第1步：构架——建立标准化的学术共同体组织（史语所）",
            "第2步：搜集——穷尽所有原始史料（上穷碧落下黄泉）",
            "第3步：考据——对史料进行严格的真伪与内容辨析",
            "第4步：解释——基于考据事实进行严谨的叙事构建",
            "第5步：维护——坚持学术独立，抵御外部政治与门户干预"
        ],
        "steps_en": [
            "Step 1: Architecture — Build standardized academic community organization (Institute of History and Philology)",
            "Step 2: Collection — Exhaust all primary historical sources (search heaven and earth)",
            "Step 3: Philology — Rigorously verify authenticity and content of historical materials",
            "Step 4: Interpretation — Construct rigorous narrative based on philological facts",
            "Step 5: Maintenance — Uphold academic independence, resist external political and factional interference"
        ],
        "expected_zh": [
            "创立中央研究院史语所，成中国现代史学最高研究基地",
            "确立「考据与解释双轨并行」史学方法论范式",
            "「上穷碧落下黄泉」成治学精神图腾",
            "「学术独立」成中国现代学术共同体制度基因"
        ],
        "expected_en": [
            "Founded Institute of History and Philology, Academia Sinica, China's premier modern historiography research base",
            "Established 'dual-track philology and interpretation' historiography methodology paradigm",
            "'Search heaven and earth' became scholarly spirit totem",
            "'Academic independence' became institutional gene of modern Chinese academic community"
        ],
        "case_zh": "傅斯年（1896-1950），辽阳人。早年五四运动领袖，后留学英国爱丁堡大学。1928年创立中央研究院历史语言研究所，任首任所长。建「上穷碧落下黄泉」治学精神，立「搜集/整理/考据/解释/出版」五步法标准化史学工程流程。建「可靠的最低限度的知识」史学标准，推动甲骨/青铜器/竹简/敦煌文书系统整理。主编《历史语言研究所集刊》三十余年，成中国现代史学最高学术平台。坚持学术独立，抗战拒日伪聘用，战后抵制政治干预学术。其「组织工程/考据双轨/学术独立」三重贡献，成中国现代学术共同体制度基因。",
        "case_en": "Fu Sinian (1896-1950), Liaoyang native. Early May Fourth leader, later studied at Edinburgh University. 1928 founded Institute of History and Philology, Academia Sinica, served as first director. Established 'search heaven and earth' scholarly spirit, established 'collect/organize/philology/interpret/publication' five-step standardized historiography engineering workflow. Established 'reliable minimum knowledge' historiography standard, drove systematic collation of oracle bones/bronze inscriptions/bamboo slips/Dunhuang manuscripts. Edited Bulletin of Institute of History and Philology for 30+ years, becoming China's premier modern historiography platform. Upheld academic independence, refused Japanese puppet appointments during war, resisted political interference post-war. His 'organizational engineering/philology dual-track/academic independence' triple contribution became institutional gene of modern Chinese academic community."
    },
    {
        "code": "H-JX-172",
        "name_zh": "贾诩：复杂博弈中的非对称自保与长效声誉管理",
        "name_en": "Jia Xu: Asymmetric Self-Preservation & Long-term Reputation Management in Complex Games",
        "description_zh": "谋士/博弈/自保/声誉管理/曹操/张绣/李傕/郭汜/曹丕/魏",
        "description_en": "Strategist/Game Theory/Self-Preservation/Reputation Management/Cao Cao/Zhang Xiu/Li Jue/Guo Si/Cao Pi/Wei",
        "modes": [13, 11, 20, 33, 34],
        "reason_zh": "贾诩是三国中最懂得自保的战略家，其每一步都经过极致的博弈测算，以非对称博弈实现生存最大化。",
        "reason_en": "Jia Xu is the most self-preservation-savvy strategist in Three Kingdoms, each move calculated via extreme game-theoretic calculation, achieving survival maximization via asymmetric games.",
        "steps_zh": [
            "第1步：感知——评估环境中的各方利益与风险边界",
            "第2步：计算——构建非对称博弈模型，寻找最优生存路径",
            "第3步：施策——通过间接手段施加影响，减少自身暴露",
            "第4步：声誉——主动管理毁誉，将不可知性转化为保护色",
            "第5步：执行——果断切断关联，全身而退"
        ],
        "steps_en": [
            "Step 1: Perception — Assess interests and risk boundaries of all parties in environment",
            "Step 2: Calculation — Build asymmetric game theory model, find optimal survival path",
            "Step 3: Strategy — Exert influence through indirect means, minimize self-exposure",
            "Step 4: Reputation — Actively manage reputation, turn unpredictability into camouflage",
            "Step 5: Execution — Decisively sever connections, retreat intact"
        ],
        "expected_zh": [
            "董卓死后一语点醒凉州兵，致长安易主，自身毫发无损",
            "建议张绣降曹，背刺袁绍，保全军团",
            "劝曹丕立世子，避免储位之争",
            "死前遗嘱「后事勿厚葬」，极致声誉管理"
        ],
        "expected_en": [
            "After Dong Zhuo's death, one sentence awakened Liangzhou army, causing Chang'an power shift, himself unharmed",
            "Advised Zhang Xiu to surrender to Cao Cao, betraying Yuan Shao, preserving army",
            "Advised Cao Pi to establish heir, avoiding succession struggle",
            "Deathbed will 'no lavish burial', ultimate reputation management"
        ],
        "case_zh": "贾诩（147-223），武威姑臧人。董卓死，李傕/郭汜作乱，贾诩劝李傕「关中四塞，地利可守」，稳住局面。董卓死后，李傕/郭汜内讧，贾诩劝李傕迎天子还长安，避免长安易主。后投张绣，建议降曹操，反攻袁绍。官渡之战前，建议曹操攻袁。曹丕立世子之争，贾诩一言定储位。死前遗令「后事勿厚葬」。其「非对称博弈/声誉管理/极致自保」三重技艺，成三国最极致生存保全型谋士范式，影响司马懿/刘伯温/曾国藩生存智慧全版图。",
        "case_en": "Jia Xu (147-223), Wuwei Güzang native. After Dong Zhuo's death, Li Jue/Guo Si rebelled, Jia Xu advised Li Jue 'Guanzhong four passes, terrain defensible', stabilizing situation. After Dong Zhuo's death, Li Jue/Guo Si infighting, Jia Xu advised Li Jue to welcome Emperor back to Chang'an, preventing power vacuum. Later served Zhang Xiu, advised surrender to Cao Cao, counterattack Yuan Shao. Before Guandu, advised Cao Cao to attack Yuan. Cao Pi succession crisis, Jia Xu's one sentence settled heir. Deathbed will 'no lavish burial'. His 'asymmetric games/reputation management/ultimate self-preservation' triple art became Three Kingdoms' ultimate survival preservation strategist paradigm, influencing Sima Yi/Liu Bowen/Zeng Guofan survival wisdom entire landscape."
    },
    {
        "code": "H-WXZ-173",
        "name_zh": "王羲之：书法心性化/永字八法/兰亭集序/技艺道化/东晋第一书圣",
        "name_en": "Wang Xizhi: Calligraphy as Mind-Cultivation/Eight Principles of Yong/Lanting Preface/Technique-to-Dao/Eastern Jin First Calligraphy Sage",
        "description_zh": "书法/永字八法/兰亭集序/心性修养/技法道化/永字八法/书圣",
        "description_en": "Calligraphy/Eight Principles of Yong/Lanting Preface/Mind-Cultivation/Technique-to-Dao/Calligraphy Sage",
        "modes": [36, 37, 23, 25, 37],
        "reason_zh": "王羲之将书法从技术升维为心性修养，以「永字八法」标准化基础笔法，以《兰亭集序》实现技法与心境完美合一。",
        "reason_en": "Wang Xizhi elevated calligraphy from technique to mind-cultivation, standardized basic strokes via 'Eight Principles of Yong', achieved perfect unity of technique and state-of-mind in 'Lanting Preface'.",
        "steps_zh": [
            "第1步：刻意练习——通过永字八法对基础笔法进行极致死磕",
            "第2步：临摹——通过海量临摹掌握先贤的核心结构",
            "第3步：脱离——摆脱对技法的执念，转向「笔意」",
            "第4步：融合——将自然美学融入笔触，实现技法自然化",
            "第5步：重构——在不同作品中实现技法与个性的动态平衡"
        ],
        "steps_en": [
            "Step 1: Deliberate Practice — Extreme deliberate practice of basic strokes via Eight Principles of Yong",
            "Step 2: Copying — Master core structures of masters through massive copying",
            "Step 3: Transcendence — Detach from technique obsession, turn to 'brush intention'",
            "Step 4: Fusion — Fuse natural aesthetics into strokes, achieving technique naturalization",
            "Step 5: Reconstruction — Achieve dynamic balance of technique and personality across works"
        ],
        "expected_zh": [
            "《兰亭集序》誉为「天下第一行书」，技法与心境完美合一",
            "「永字八法」成中国书法基础笔法标准化范本",
            "「平常心是道/行住坐卧/柴米油盐」生活禅范式影响宋明理学/王阳明心学/现代正念疗法",
            "成中国书法技艺道化/心性化/标准化奠基范式"
        ],
        "expected_en": [
            "Lanting Preface hailed as 'World's First Running Script', perfect unity of technique and state-of-mind",
            "Eight Principles of Yong became Chinese calligraphy basic strokes standardization paradigm",
            'Ordinary mind is Way/walking-standing-sitting-lying/firewood-rice-oil-salt' life-Chan paradigm influencing Song-Ming Neo-Confucianism/Wang Yangming Mind School/modern mindfulness therapy",
            "Became Chinese calligraphy technique-to-Dao/mind-cultivation/standardization foundational paradigm"
        ],
        "case_zh": "王羲之（303-361），琅琊临沂人。幼习书，师卫夫人，得笔法精髓。著《笔阵图》阐述笔法要诀。创「永字八法」：侧/勒/努/趯/策/掠/啄/磋八法，标准化基础笔法。永和九年（353）会稽山阴兰亭修禊，醉书《兰亭集序》：「寄寓形骸之内/纵观宇宙之外/視聽之所及/信可樂也」，以「不谋而合/信手拈来」之妙，实现技法与心境完美合一。创「平常心是道/行住坐卧/柴米油盐」生活禅范式，影响马祖「日面佛/月面佛」、百丈「清规」、黄檗「心佛」、赵州「狗子佛性」、云门「干屎橛」、法眼「文殊」、永嘉「证道歌」、圭峰「宗镜录」、延寿「宗镜录」、宋明周敦颐/程颢程颐/张载/朱熹/陆九渊/王阳明「致良知」、现代卡巴金「正念减压疗法/MBSR」。其「破权威/去阶级/去文字/回生活」四重颠覆，成中国佛教平民化/本土化/现代化奠基范式。",
        "case_en": "Wang Xizhi (303-361), Langya Linyi native. Young studied calligraphy, learned from Lady Wei, mastered brush essence. Authored Brush Array Diagram expounding brush essence. Created 'Eight Principles of Yong': ce/le/nu/ce/ce/lue/zhuo/cuo eight methods, standardizing basic strokes. 353 CE Yonghe 9, Lanting purification gathering, drunkenly wrote Lanting Preface: 'lodge body within universe/overlook cosmos/where sight and hearing reach/indeed joyful', with 'unplanned coincidence/brush follows mind' marvel, achieving technique-state unity. Created 'ordinary mind is Way/walking-standing-sitting-lying/firewood-rice-oil-salt' life-Chan paradigm, influencing Mazu 'sun-face Buddha/moon-face Buddha', Baizhang 'Pure Rules', Huangbo 'mind-Buddha', Zhaozhou 'dog Buddha-nature', Yunmen 'dry shit stick', Fayan 'Manjushri', Yongjia 'Enlightenment Song', Guifeng 'Zongjing Lu', Yanshou 'Zongjing Lu', Song-Ming Zhou Dunyi/Cheng Hao-Cheng Yi/Zhang Zai/Zhu Xi/Lu Jiuyuan/Wang Yangming 'unity of knowledge and action', modern Kabat-Zinn 'MBSR'. His 'break authority/remove class/remove text/return life' quadruple subversion became Chinese calligraphy technique-to-Dao/mind-cultivation/standardization foundational paradigm."
    },
    {
        "code": "H-ZH-174",
        "name_zh": "郑和：七下西洋/大规模物流信息符号联动/明代海洋组织工程/郑和下西洋",
        "name_en": "Zheng He: Seven Voyages/Massive Logistics-Information-Symbol Linkage/Ming Maritime Organizational Engineering/Seven Voyages",
        "description_zh": "七下西洋/物流/信息/外交/宝船/船队/明代海洋/组织工程",
        "description_en": "Seven Voyages/Logistics/Information/Diplomacy/Treasure Ships/Fleet/Ming Maritime/Organizational Engineering",
        "modes": [41, 6, 12, 28, 28],
        "reason_zh": "郑和以「商贸/军事/外交」三位一体目标，建立超大规模船队标准化补给链、驿站制信息流、外交仪式软实力输出，成明代超大规模组织首席执行官。",
        "reason_en": "Zheng He established triple 'trade/military/diplomacy' objectives, building massive fleet standardized supply chains, relay-station information flows, diplomatic ritual soft power output, becoming Ming's mega-organization CEO.",
        "steps_zh": [
            "第1步：顶层——明确商贸/军事/外交三位一体目标",
            "第2步：物流——建立超大规模船队标准化补给链条",
            "第3步：信息——利用驿站与海流规律建立高效信息流速",
            "第4步：联动——将外交仪式转化为文化与软实力输出",
            "第5步：复盘——根据航海成果对补给与安全体系进行冗余修正"
        ],
        "steps_en": [
            "Step 1: Top-level — Clarify triple 'trade/military/diplomacy' objectives",
            "Step 2: Logistics — Build massive fleet standardized supply chain",
            "Step 3: Information — Utilize relay stations and ocean currents for efficient information flow",
            "Step 4: Linkage — Convert diplomatic rituals into cultural and soft power output",
            "Step 5: Review — Redundancy correction of supply and safety systems per voyage results"
        ],
        "expected_zh": [
            "七下西洋两万里，构建明代海洋势力圈",
            "宝船/马船/粮船/坐船/水船/战船六级船队编制标准化",
            "驿站制/海流规律成高效信息流速体系",
            "外交仪式转化文化软实力，成明代海洋组织工程巅峰"
        ],
        "expected_en": [
            "Seven voyages 20,000 li, built Ming maritime power sphere",
            "Treasure/horse/grain/passenger/water/war ships six-tier fleet standardization",
            "Relay stations/ocean currents became high-efficiency information flow system",
            "Diplomatic rituals converted to cultural soft power, Ming maritime organizational engineering peak"
        ],
        "case_zh": "郑和（1371-1433），昆阳人，原名马三宝。永乐三年（1405）奉命下西洋，至宣德八年（1433）止，七下西洋，历28年，足迹遍布东南亚/南亚/中东/东非三十余国。统帅宝船/马船/粮船/坐船/水船/战船六级船队，规模最大时船队200余艘，官兵2.7万余人。建「驿站制/海流规律」双重信息网，建「官方/民间/宗教」三重外交渠道。著《郑和航海图》《瀛涯胜览》等航海志。其「商贸/军事/外交三位一体/标准化物流/驿站信息流/外交软实力」四维融合，成明代超大规模组织工程巅峰，影响郑和/郑芝龙/郑成功/现代远洋物流/海洋外交全版图。",
        "case_en": "Zheng He (1371-1433), Kunyang native, original name Ma Sanbao. Yongle 3 (1405) commissioned westward voyages, until Xuande 8 (1433) stop, seven voyages, 28 years, footprint across 30+ Southeast/South/West Asia/East Africa countries. Commanded treasure/horse/grain/passenger/water/war ships six-tier fleet, peak 200+ ships, 27,000+ personnel. Built 'relay stations/ocean currents' dual information network, built 'official/folk/religious' triple diplomatic channels. Authored Zheng He Nautical Charts/Yingya Shenglan etc. His 'trade-military-diplomacy triad/standardized logistics/relay information flow/diplomatic soft power' four-dimensional fusion became Ming mega-organization engineering peak, influencing Zheng He/Zheng Zhilong/Zheng Chenggong/modern ocean logistics/maritime diplomacy entire landscape."
    },
    {
        "code": "H-XZ-175",
        "name_zh": "玄奘：大唐西域记/大乘起信论/法相唯识/翻译标准化/佛教考据学奠基",
        "name_en": "Xuanzang: Great Tang Records on Western Regions/Mahayana Awakening Faith/Faxiang Weishi/Translation Standardization/Buddhist Philology Foundation",
        "description_zh": "大唐西域记/成唯识论/法相唯识宗/佛经翻译/翻译标准化/佛教考据学/丝路考察",
        "description_en": "Great Tang Records on Western Regions/Cheng Weishi Lun/Faxiang Weishi School/Buddhist Translation/Translation Standardization/Buddhist Philology/Silk Road Survey",
        "modes": [25, 1, 28, 34, 38],
        "reason_zh": "玄奘以「实地求法-版本校勘-体系翻译-学派建构」四重工程，将印度佛学体系化、标准化、中国化，成中国佛教学术化/考据化/体系化奠基工程。",
        "reason_en": "Xuanzang engineered 'field dharma-seeking/version collation/systematic translation/school construction' quadruple project, systematizing/standardizing/Sinicizing Indian Buddhism, becoming Chinese Buddhism academicization/philologization/systematization foundational project.",
        "steps_zh": [
            "第1步：实事求是法——十七年万里西行，以「实地走访/文献采集/版本收集/口诀请受」四重求法法门，获梵文原本六百五十七部",
            "第2步：抽象归纳法——著《大唐西域记》十二卷，以「地理/风俗/佛教/语言/历史/政治」六维田野调查模板，成中国最早丝路考察学/佛教地理学奠基之作",
            "第3步：系统思维法——建立「梵文原文-字句对照-分工翻译-集体审定-义理阐释」五阶段翻译标准化流程",
            "第4步：摸石头过河/实验主义——集印度十大论师唯识思想，著《成唯识论》十卷，确立「三性/三无性/八识/二无我/五位百法」法相唯识宗理论大厦",
            "第5步：制度化制衡——推动法相宗成唐代官方认可大宗，以《成唯识论》为核心教材，建立「闻/思/修」三慧次第修学体系"
        ],
        "steps_en": [
            "Step 1: Seeking Truth from Facts — 17-year 10,000-mile westward journey, 'field visit/document collection/version gathering/oral instruction receiving' four dharma-seeking methods, obtained 657 Sanskrit originals",
            "Step 2: Abstract Induction — Authored 12-volume Great Tang Records on Western Regions via 'geography/customs/Buddhism/language/history/politics' six-dimensional fieldwork template, founding China's earliest Silk Road survey/Buddhist geography",
            "Step 3: Systems Thinking — Established 'Sanskrit source-word-by-word collation-team translation-collective review-doctrinal exposition' five-stage translation standardization process, translated 75 texts 1335 volumes including Cheng Weishi Lun/Sandhinirmocana/Mahaprajnaparamita",
            "Step 4: Crossing River by Feeling Stones — Synthesized India's ten great Yogacara masters into 10-volume Cheng Weishi Lun, establishing 'three natures/three non-natures/eight consciousnesses/two non-selfs/five stages hundred dharmas' Faxiang Weishi school theoretical edifice",
            "Step 5: Institutional Checks — Promoted Faxiang school as Tang-state recognized sect, centered on Cheng Weishi Lun as core textbook, established 'hearing/contemplation/cultivation' three-wisdom sequential cultivation system"
        ],
        "expected_zh": [
            "万里西行十七年，遍访印度百余国，获梵文原本六百五十七部",
            "《大唐西域记》成中国最早丝路考察学/佛教地理学奠基之作",
            "十九年译出75部1335卷，建立五阶段翻译标准化流程",
            "《成唯识论》确立法相唯识宗「三性/三无性/八识/二无我/五位百法」理论大厦"
        ],
        "expected_en": [
            "17-year 10,000-mile westward journey, visited 100+ Indian kingdoms, obtained 657 Sanskrit originals",
            "Great Tang Records on Western Regions became China's earliest Silk Road survey/Buddhist geography foundation",
            "19 years translated 75 texts 1335 volumes, establishing five-stage translation standardization process",
            "Cheng Weishi Lun established Faxiang Weishi 'three natures/three non-natures/eight consciousnesses/two non-selfs/five stages hundred dharmas' theoretical edifice"
        ],
        "case_zh": "玄奘（602-664），洛阳偃师人，十三岁出家，研《般若/中观/俱舍/因明/戒律》五大论。629年毅然西行，经高昌/铁勒/撒马尔罕/大月氏/迦湿弥罗/中天竺/那烂陀寺，求法十七年，得梵本六百五十七部；645返长安，太宗诏著《大唐西域记》十二卷，以「国/都/俗/物/佛/语」六维模板记录百三十余国地理/风俗/佛教/语言，成中国最早丝路考察学奠基之作。主持大慈恩寺译场十九年，译《成唯识论》《解深密经》《大般若经》等75部1335卷，建立「梵本对照/分工翻译/集体审定/义理阐释」五阶段标准化流程。集十大论师唯识精华，著《成唯识论》十卷，确立「遍计所执/依他起成/圆成实」三性、「三无性/八识/二无我/五位百法」法相唯识宗理论大厦，成中国佛教学术化/考据化/体系化奠基工程。",
        "case_en": "Xuanzang (602-664), Luoyang Yanshi native, ordained at 13, studied Prajna/Madhyamaka/Abhidharmakosha/Pramana/Vinaya five great treatises. 629 westward journey via Gaochang/Tiele/Samarqand/Da Yuezhi/Kashmir/Central India/Nalanda, 17-year dharma-seeking, obtained 657 Sanskrit originals; 645 returned Chang'an, Taizong ordered Great Tang Records on Western Regions 12 volumes, recording 130+ kingdoms via 'capital/customs/products/Buddhism/language/history' six-dimensional template, founding China's earliest Silk Road survey. Led Great Ci'en Temple Bureau 19 years, translated 75 texts 1335 volumes including Cheng Weishi Lun/Sandhinirmocana/Mahaprajnaparamita, establishing 'Sanskrit collation/team translation/collective review/doctrinal exposition' five-stage standardized process. Synthesized ten great masters' Yogacara essence into 10-volume Cheng Weishi Lun, establishing 'parikalpita/paratantra/parinishpanna' three natures, 'three non-natures/eight consciousnesses/two non-selfs/five stages hundred dharmas' Faxiang Weishi theoretical edifice, becoming Chinese Buddhist academicization/philologization/systematization foundational project."
    },
    {
        "code": "H-LZC-176",
        "name_zh": "李自成：游击战术在政权动员中的原型实践及其短板效应",
        "name_en": "Li Zicheng: Peasant Uprising Mobilization/Guerrilla Warfare Prototype/Political Power Shortboard",
        "description_zh": "李自成/农民起义/游击战/政权动员/分田地均贫富/北洋体系/明清交替",
        "description_en": "Li Zicheng/Peasant Uprising/Guerrilla Warfare/Political Mobilization/Divide Land Equalize Wealth/Beiyang System/Ming-Qing Transition",
        "modes": [4, 3, 16, 9, 15],
        "reason_zh": "李自成以「分田地/均贫富」为核心动员口号，以「游击战十六字诀」建立非对称作战体系，但将游击动员模式直接转化为政权管理模式导致治理崩塌。",
        "reason_en": "Li Zicheng mobilized with 'divide land/equalize wealth' core slogan, built asymmetric warfare system via 'Sixteen-Character Guerrilla Formula', but directly converting guerrilla mobilization model into governance model caused governance collapse.",
        "steps_zh": [
            "第1步：动员——利用不平等的土地分配矛盾进行核心动员",
            "第2步：游击——通过十六字诀在机动中消灭敌方主力",
            "第3步：扩张——快速占据关键节点，通过动员扩大规模",
            "第4步：政权——将游击动员模式直接转化为政权管理模式",
            "第5步：审计——评估动员基础上的政权维持成本与风险"
        ],
        "steps_en": [
            "Step 1: Mobilization — Leverage unequal land distribution contradiction for core mobilization",
            "Step 2: Guerrilla — Eliminate enemy main force via mobility with Sixteen-Character Formula",
            "Step 3: Expansion — Rapidly occupy key nodes, expand scale via mobilization",
            "Step 4: Regime — Directly convert guerrilla mobilization model into governance model",
            "Step 5: Audit — Assess regime maintenance costs and risks on mobilization basis"
        ],
        "expected_zh": [
            "「分田地/均贫富」口号在起义初期的极大成功",
            "游击战十六字诀建立非对称作战完整体系",
            "「游击动员模式→政权管理模式」直接转化导致治理崩塌",
            "成农民起义动员/政权建设短板效应双重典型范式"
        ],
        "expected_en": [
            "'Divide land/equalize wealth' slogan enormous success in uprising early stage",
            "Sixteen-Character Formula established complete asymmetric warfare system",
            "'Guerrilla mobilization model → governance model' direct conversion caused governance collapse",
            "Peasant uprising mobilization/regime building shortboard effect dual paradigm"
        ],
        "case_zh": "李自成（1606-1645），陕西米脂人。早年驿卒，饥荒起义，立「闯王」号。以「迎闯王/不纳粮」口号动员，推「分田地/均贫富」土地政策，以「打富济贫/开仓放粮」动员底层。用「敌进我退/敌驻我扰/敌疲我打/敌退我追」游击战十六字诀，建「分散/集中/运动/歼灭」机动作战体系。1644年入北京，建大顺政权，但「进京后骄奢淫逸/土地政策未落实/军纪败坏/失民心」四十五天亡国。其「游击动员模式→政权管理模式」直接转化失败，成农民起义动员成功/政权建设短板双重典型范式，影响毛泽东/朱德/彭德怀/林彪/粟裕/陈毅/刘伯承/贺龙/陈赓/徐向前/聂荣臻/叶剑英革命战争/政权建设双重教训全版图。",
        "case_en": "Li Zicheng (1606-1645), Mizhi Shaanxi native. Early courier, famine sparked uprising, styled 'Dashuai Wang'. Mobilized with 'Welcome Dashuai/No Tax' slogan, promoted 'Divide Land/Equalize Wealth' land policy, mobilized bottom via 'Strike Rich Relief Poor/Open Granaries'. Used 'Enemy Advance We Retreat/Enemy Halt We Harass/Enemy Tire We Attack/Enemy Retreat We Pursue' Sixteen-Character Formula, built 'dispersal/concentration/maneuver/annihilation' mobile warfare system. 1644 entered Beijing, established Dashun regime, but 'arrogance/land policy unimplemented/military discipline collapsed/lost popular support' forty-five days fell. His 'guerrilla mobilization model → governance model' direct conversion failure became peasant uprising mobilization success/regime building shortboard dual paradigm, influencing Mao Zedong/Zhu De/Peng Dehuai/Lin Biao/Su Yu/Chen Yi/Liu Bocheng/He Long/Chen Geng/Xu Xiangqian/Nie Rongzhen/Ye Jianying revolutionary war/regime building dual lesson entire landscape."
    },
    {
        "code": "H-HX-177",
        "name_zh": "黄兴：军事统筹与革命事业的组织纽带建设",
        "name_en": "Huang Xing: Military Coordination & Revolutionary Organization Nexus Builder",
        "description_zh": "光复会/同盟会/军事统筹/革命组织/黄花岗/辛亥革命/陆军小学/湖南自立军",
        "description_en": "Restoration Society/Tongmenghui/Military Coordination/Revolutionary Organization/Huanghuagang/Xinhai Revolution/Army Primary School/Hunan Self-Reliance Army",
        "modes": [3, 6, 14, 11, 35],
        "reason_zh": "黄兴在「革命军事/组织建设/政治妥协」三维空间中，以「军事统筹/组织纽带/战略妥协」三重角色，完成从「刺客/军官/统帅/政治家」的四重身份跃迁。",
        "reason_en": "Huang Xing completed quadruple identity leap from 'assassin/officer/commander/statesman' via triple roles of 'military coordination/organizational nexus/strategic compromise' in 'revolutionary military/organizational construction/political compromise' three-dimensional space.",
        "steps_zh": [
            "第1步：调研——客观评估革命实战中的军事与人力资源",
            "第2步：组织——构建革命军队的职业化、标准化纲领",
            "第3步：博弈——在关键时刻进行政治妥协，以实现整体利益",
            "第4步：传递——有序进行组织权力的接力与延续",
            "第5步：审视——在革命实战中不断修整军事与统战布局"
        ],
        "steps_en": [
            "Step 1: Research — Objectively assess military and human resources in revolutionary practice",
            "Step 2: Organization — Build revolutionary army professionalization/standardization framework",
            "Step 3: Game Theory — Strategic compromise at critical moments for overall interest",
            "Step 4: Transmission — Orderly organizational power relay and continuity",
            "Step 5: Review — Continuously adjust military and united front layout in practice"
        ],
        "expected_zh": [
            "创办湖南自立军/光复会/同盟会，成革命军事组织奠基者",
            "黄花岗起义虽败犹荣，「七十二烈士」成革命精神图腾",
            "武昌起义军事统筹，极度困难下稳住局势，成辛亥成功关键",
            "「军事统筹/组织纽带/战略妥协」三维融合，成近代革命军事组织典范"
        ],
        "expected_en": [
            "Founded Hunan Self-Reliance Army/Restoration Society/Tongmenghui, revolutionary military organization founder",
            "Huanghuagang Uprising defeat with honor, '72 Martyrs' became revolutionary spirit totem",
            "Wuchang Uprising military coordination stabilized situation in extreme difficulty, key to Xinhai success",
            "Three-dimensional fusion 'military coordination/organizational nexus/strategic compromise', modern revolutionary military organization paradigm"
        ],
        "case_zh": "黄兴（1874-1916），长沙人。早年创岳云学社/华兴会，后合并为光复会。1905年同盟会成立，任副总裁兼军政部长。创办湖南自立军，编练新军，建立革命军事训练体系。1911年黄花岗起义失败，题「赤子心」勒石。辛亥革命武昌起义，黄兴率敢死队攻打清军，指挥革命军作战，统筹军事/政治/外交三线，成辛亥革命军事统筹核心。民国成立任陆军总长/国务总理，推军队国家化/政党化。其「军事统筹/组织纽带/战略妥协」三维融合，成近代革命军事组织典范。",
        "case_en": "Huang Xing (1874-1916), Changsha native. Early founded Yueyun Society/Huaxing Society, merged into Restoration Society. 1905 Tongmenghui founded, Vice President & Military Minister. Founded Hunan Self-Reliance Army, trained New Army, established revolutionary military training system. 1911 Huanghuagang Uprising failed, inscribed 'Red Son Heart' on stone. Xinhai Revolution Wuchang Uprising, Huang Xing led Dare-to-Die Corps, commanded revolutionary army, coordinated military/political/diplomatic three lines, became Xinhai Revolution military coordination core. ROC founded served as Army Chief/Prime Minister, pushed army nationalization/partization. His 'military coordination/organizational nexus/strategic compromise' triple fusion became modern revolutionary military organization paradigm."
    },
    {
        "code": "H-SJR-178",
        "name_zh": "宋教仁：议会政治的制度化建设与法治架构设计",
        "name_en": "Song Jiaoren: Parliamentary Politics Institutionalization & Legal Framework Design",
        "description_zh": "同盟会/国民党/议会政治/法治/制度化/选举/内阁制/宋案",
        "description_en": "Tongmenghui/Kuomintang/Parliamentary Politics/Rule of Law/Institutionalization/Elections/Cabinet System/Song Case",
        "modes": [42, 32, 34, 6, 35],
        "reason_zh": "宋教仁在「革命/建设/改革」三个历史阶段跨越百年，以「革命伴侣-独立政治人-国家名誉主席」三重身份完成「私人-公共-国家」三重超越——「孙中山伴侣」期以「翻译/记录/宣传/外交」四重角色参与革命顶层设计；「中共党员」期以「妇女解放/儿童福利/人权倡导/党内民主」四大议题推动制度建设；「国家名誉主席」期以「和平统一/对外友好/文化交流/人道主义」四大外交工程服务国家战略。其「忠于革命-忠于真理-忠于人民」三重忠诚统一，成中国近代女性政治觉醒与国家建设深度融合典范。",
        "reason_en": "Song Jiaoren spanned century across 'revolution/construction/reform' three historical phases, achieved 'private-public-state' triple transcendence via 'revolutionary partner-independent political figure-state honorary chair' triple identity — 'Sun Yat-sen partner' phase participated in revolutionary top-design via 'translation/recording/publicity/diplomacy' four roles; 'CCP member' phase advanced institutional building via 'women liberation/child welfare/human rights advocacy/party democracy' four issues; 'State Honorary Chair' phase served national strategy via 'peaceful unification/international friendship/cultural exchange/humanitarianism' four diplomatic engineering projects. Her 'loyal to revolution-loyal to truth-loyal to people' triple loyalty unity became paradigm of modern Chinese women's political awakening deeply fused with nation-building.",
        "steps_zh": [
            "第1步：统一战线法——以「革命伴侣/翻译/记录/宣传」四重角色参与孙中山革命顶层设计，建立「革命理论-实践-传播」三位一体工作法",
            "第2步：群众路线法——推动「妇女解放/儿童福利/人权倡导」三大议题，以「立法/组织/宣传/监督」四维推进制度建设",
            "第3步：三民主义/体系化纲领——以「国家名誉主席」身份推动「和平统一/对外友好/文化交流/人道主义」四大外交工程",
            "第4步：批评与自我批评——坚持「党内民主/言论自由/监督制衡」原则，在文革等政治运动中坚守原则、保护同志",
            "第5步：总体性思维——将「革命/建设/改革」三阶段、「私人/公共/国家」三层面、「女性/中国人/世界公民」三重身份深度融合，成跨世纪女性政治觉醒典范"
        ],
        "steps_en": [
            "Step 1: United Front — As 'revolutionary partner/translator/recorder/publicist' four roles participated in Sun Yat-sen's revolutionary top-design, building 'theory-practice-dissemination' trinity work method",
            "Step 2: Mass Line — Advanced 'women liberation/child welfare/human rights' three issues via 'legislation/organization/publicity/supervision' four-dimensional institutional advancement",
            "Step 3: Three Principles Systemic Framework — As 'State Honorary Chair' drove 'peaceful unification/international friendship/cultural exchange/humanitarianism' four diplomatic engineering projects",
            "Step 4: Criticism and Self-Criticism — Upheld 'party democracy/free speech/supervision checks' principles, stood firm during Cultural Revolution and other movements, protected comrades",
            "Step 5: Systems Thinking — Deeply fused 'revolution/construction/reform' three phases, 'private/public/state' three levels, 'woman/Chinese/global citizen' three identities, becoming cross-century paradigm of women's political awakening"
        ],
        "expected_zh": [
            "孙中山革命伴侣，参与《三民主义》阐释与革命顶层设计",
            "中国妇女解放运动先驱，推动《婚姻法》颁布（废除包办/买卖婚姻、确立婚姻自由/男女平等）、创办中国福利会/托儿所/少年宫",
            "国家名誉主席，推动中美建交/和平统一/对外友好外交",
            "「革命-建设-改革」百年跨越，成中国近代女性政治觉醒与国家建设深度融合典范"
        ],
        "expected_en": [
            "Sun Yat-sen's revolutionary partner, participated in Three Principles interpretation and revolutionary top-design",
            "Pioneer of China's women's liberation, drove Marriage Law (abolished arranged/mercantile marriage, established marriage freedom/gender equality), founded China Welfare Institute/nurseries/children's palaces",
            "State Honorary Chair, drove Sino-US normalization/peaceful unification/international friendship diplomacy",
            "Century spanning 'revolution-construction-reform', paradigm of modern Chinese women's political awakening fused with nation-building"
        ],
        "case_zh": "宋庆龄（1893-1981），宋氏三姐妹二女，1915随孙中山赴日，任英文秘书/翻译/记录员，参与《建国方略》编辑；1924孙中山病危时记录《总理遗嘱》；1927「二七」惨案后发表《为七二惨案宣言》断与国民党；1949任中央人民政府副主席/全国妇联主席，推动《婚姻法》颁布（废除包办/买卖婚姻、确立婚姻自由/男女平等）、创办中国福利会/托儿所/少年宫；1954任全国人大常委会副委员长，推动妇女/儿童/人权立法；1966文革遭软禁仍坚持「党内民主/言论自由」原则，保护大批知识分子；1981病危入党，任国家名誉主席，推动中美建交/和平统一/对外友好。其「革命伴侣→独立政治人→国家名誉主席」三重跃迁，跨越「革命/建设/改革」百年，成中国女性政治觉醒与国家建设深度融合典范。",
        "case_en": "Soong Ching-ling (1893-1981), second of Soong sisters, 1915 accompanied Sun Yat-sen to Japan as English secretary/translator/recorder, edited 'National Reconstruction Guidelines'; 1924 recorded 'Premier's Testament' at Sun's deathbed; 1927 published 'Declaration on March 18 Massacre' breaking with KMT; 1949 Vice Chair of Central People's Govt/ACWF Chair, drove Marriage Law (abolished arranged/mercantile marriage, established marriage freedom/gender equality), founded China Welfare Institute/nurseries/children's palaces; 1954 NPC Standing Committee Vice Chair, advanced women/children/human rights legislation; 1966 Cultural Revolution house arrest yet upheld 'party democracy/free speech' principles, protected numerous intellectuals; 1981 deathbed CCP membership, State Honorary Chair, drove Sino-US normalization/peaceful unification/international friendship. Her 'revolutionary partner→independent political figure→state honorary chair' triple leap spanning 'revolution/construction/reform' century became paradigm of modern Chinese women's political awakening deeply fused with nation-building."
    },
    {
        "code": "H-WYN-179",
        "name_zh": "王亚南：知识移植与话语体系自主化的方法论工程",
        "name_en": "Wang Yanan: Knowledge Transplantation & Discourse System Autonomy Methodology Engineering",
        "description_zh": "政治经济学/教材体系/价格改革/改革风险决策/死磕范式跃迁/知识移植/话语自主",
        "description_en": "Political Economy/Textbook System/Price Reform/Reform Risk Decision Framework/Paradigm Leap of Dead-End/ Knowledge Transplantation/Discourse Autonomy",
        "modes": [19, 20, 25, 28, 35],
        "reason_zh": "王亚南在「马克思主义中国化/价格改革理论/教材体系建设」三大战场，以「翻译-消化-本土化改良-工程化落地」四阶段知识移植法，完成中国经济学话语体系自主化建设。",
        "reason_en": "Wang Yanan on three battlefields 'Marxism Sinicization/price reform theory/textbook system construction', accomplished Chinese economics discourse system autonomy via four-stage knowledge transplantation method 'translate-digest-localize-improve-engineering implementation'.",
        "steps_zh": [
            "第1步：抽象归纳法——从《资本论》等经典中提炼「价值/价格/剩余价值/分配/再生产」核心概念簇，生成经济学教材建模框架",
            "第2步：摸石头过河/实验主义——编《政治经济学》教材采用「分类→实测→实验→定型」四阶段法，六万卷覆盖「品种/土壤/水肥/工具/病虫/收获」六大农事体系",
            "第3步：摸石头过河/实验主义——主持「价格改革理论」研究，引入「边际思维/损失厌恶/双系统思维」行为经济学视角，建立改革风险决策框架",
            "第4步：制度化制衡——推动《政治经济学》作为「技术标准/教学教材/专利前身/技术转移协议」四重功能文本，以文本固化技术、防止技术失传/垄断/流失",
            "第5步：总体性思维——将「翻译/消化/本土化/工程化」四系统耦合，形成「翻译→消化→本土化→工程化」全链路知识移植范式"
        ],
        "steps_en": [
            "Step 1: Abstract Induction — Extract 'value/price/surplus value/distribution/reproduction' core concept clusters from Capital and other classics, generating economics textbook modeling framework",
            "Step 2: Crossing River by Feeling Stones — Compiled Political Economy textbook via 'categorize→field test→experiment→finalize' four-stage method, 60k volumes covering 'variety/soil/fertilizer/tools/pests/harvest' six agricultural systems",
            "Step 3: Crossing River by Feeling Stones — Led 'price reform theory' research, introduced 'marginal thinking/loss aversion/dual-system thinking' behavioral economics perspectives, establishing reform risk decision framework",
            "Step 4: Institutional Checks — Positioned Political Economy as 'technical standard/textbook/patent precursor/technology transfer agreement' quadruple-function document, solidifying technology via text, preventing loss/monopoly/leakage",
            "Step 5: Systems Thinking — Couple 'translation/digestion/localization/engineering' four systems into 'translation→digestion→localization→engineering' full-chain knowledge transplantation paradigm"
        ],
        "expected_zh": [
            "《政治经济学》六万卷成中国首部经济学教材百科全书",
            "价格改革理论奠基与改革风险决策框架，成中国改革开放理论奠基",
            "「翻译→消化→本土化→工程化」四阶段知识移植法，成中国学科话语自主化范式",
            "被誉为「中国经济学教科书之父」"
        ],
        "expected_en": [
            "Political Economy 60k volumes became China's first economics textbook encyclopedia",
            "Price reform theory foundation & reform risk decision framework, foundation of China's reform opening theory",
            "Four-stage 'translation→digestion→localization→engineering' knowledge transplantation method, Chinese discipline discourse autonomy paradigm",
            "Hailed as 'Father of Chinese Economics Textbooks'"
        ],
        "case_zh": "王亚南（1905-1997），绍兴山阴人。1904赴日留学，习经济学，归国任教。1920年代编《政治经济学》教材，建立「价值/价格/剩余价值/分配/再生产」中文经济学词汇体系；1940年代研《价格理论》，引入「边际/机会成本/弹性」概念，奠定中国价格理论基础；1950年代主持「价格改革」研究，建立「风险/收益/边际/机会成本」决策框架，为改革开放价格双轨制/市场化定价奠基；1970年代主编《政治经济学》教材，六万卷系统总结「水稻/小麦/棉花/桑蚕/水利/农具/肥料/病虫」八大体系，引入「轮作/间作/绿肥/选种」科学农法。被李约瑟誉为「中国经济学教科书之父」，其「翻译→消化→本土化→工程化」四阶段知识移植法，成中国学科话语自主化范式。",
        "case_en": "Wang Yanan (1905-1997), Shaoxing Shanyn native. 1904 studied in Japan, learned economics, returned to teach. 1920s compiled Political Economy textbook, established Chinese economic vocabulary 'value/price/surplus value/distribution/reproduction'; 1940s researched Price Theory, introduced 'marginal/opportunity cost/elasticity' concepts, founding China's price theory; 1950s led 'price reform' research, established 'risk/return/marginal/opportunity cost' decision framework, founding reform era dual-track pricing/market pricing; 1970s edited Political Economy textbook, 60k vols systematically summarizing 'rice/wheat/cotton/mulberry/water/implements/fertilizer/pests' eight systems, introducing 'crop rotation/intercropping/green manure/seed selection' scientific farming. Hailed by Joseph Needham as 'Father of Chinese Economics Textbooks', his 'translation→digestion→localization→engineering' four-stage knowledge transplantation became Chinese discipline discourse autonomy paradigm."
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

print(f"✅ Added {len(new_entries)} missing Phase 2 figures")