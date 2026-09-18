import json

# Load existing scenarios
with open('scenarios_zh.json', 'r', encoding='utf-8') as f:
    scenarios_zh = json.load(f)

with open('scenarios_en.json', 'r', encoding='utf-8') as f:
    scenarios_en = json.load(f)

# Add 6 more high-value historical figures
new_scenarios_zh = {
    "H-CC-21": {
        "name": "曹操：挟天子以令诸侯的实用主义霸权",
        "description": "奸雄本色、唯才是举、屯田制、短歌行、赤壁败走",
        "modes": [33, 13, 17, 4, 11],
        "reason": "曹操'治世之能臣，乱世之奸雄'。核心思维：实用主义权谋——不拘一格用人（陈群九品制）、挟正统令诸侯（汉献帝为政治资源）、屯田解决军粮（经济基础决定上层建筑）、诗词抒发雄心（短歌行/龟虽寿）。赤壁败因：战略过伸、水土不服、联盟松散。",
        "steps": [
            "第1步：格局授权——陈群创九品中正制，打破门阀垄断，唯才是举",
            "第2步：全胜思维——挟天子以令诸侯，以合法性压制割据势力，不战而屈人之兵",
            "第3步：多元思维模型——屯田制：军民分屯、租税固定、国家垄断盐铁，解决长期军粮",
            "第4步：农村包围城市——从兖州起家，逐步吞并青徐荆扬，最后统一北方",
            "第5步：灵活策略法——官渡之战烧乌巢粮草，赤壁败后'祸起萧墙'收拢人心"
        ],
        "expected": [
            "统一北方，建立曹魏政权，为西晋统一奠基",
            "九品中正制延用300年，屯田制成历代军屯蓝本",
            "教训：战略过伸（南征吴蜀）、人才断层（杀杨修/孔融）、继承制未定导致夺嫡"
        ],
        "case": "官渡之战（200）：袁绍10万vs曹操2万。曹操'袁绍多谋少决'，许攸投奔烧乌巢粮草，袁军崩溃。屯田制（196）：检括天下户口，募民屯田，收获百万斛，解决军粮。九品中正（220）：陈群建'中正官'品评人物，以德行/才能定九等，打破'上品无寒门'。赤壁（208）：轻敌、水战不利、庞统连环计、东南风、周瑜火攻，曹操'祸起萧墙'撤退。"
    },
    "H-SQ-22": {
        "name": "孙权：守成之主的平衡术与江东基业",
        "description": "19岁继业、赤壁联刘抗曹、濡须屯田、夷陵火攻、二代困境",
        "modes": [6, 20, 11, 28, 35],
        "reason": "孙权'生子当如孙仲谋'。核心思维：平衡术生存法则——内部平衡周瑜/鲁肃/吕蒙/陆逊四代都督，外部联刘抗曹/襄樊之战背刺关羽/夷陵火攻刘备。守成比创业难：父兄基业、文武集团制衡、北伐无望转守内治。",
        "steps": [
            "第1步：统一战线法——赤壁联刘备抗曹操，利用曹操'北人不习水战'弱点",
            "第2步：博弈论思维——襄樊之战：表面助关羽北伐，实则吕蒙白衣渡江偷袭荆州，关羽走麦城",
            "第3步：灵活策略法——濡须屯田：朱桓/吕范经营濡须坞，水陆并进，抗曹防线固若金汤",
            "第4步：冗余备份法——四代都督：周瑜/鲁肃/吕蒙/陆逊，文武相济，防单一将领尾大不掉",
            "第5步：蛰伏积势思维——夷陵之战（221-222）：陆逊'且住夏冬'火攻刘备七百里连营，刘备白帝城托孤"
        ],
        "expected": [
            "赤壁之战奠定三国鼎立格局",
            "荆州夺回、关羽除掉、西南边疆稳固",
            "教训：后期迷信方士、废太子立鲁王导致'二宫之争'、孙皖幼冲权臣专政"
        ],
        "case": "赤壁联盟（208）：鲁肃促成孙刘联盟，周瑜/黄盖苦肉/连环/火攻，曹操败走华容道。濡须屯田（210+）：朱桓'水则舟楫，陆则马步'，曹操20万攻濡须无功而返。吕蒙袭荆州（219）：'士别三日当刮目相待'，白衣渡江、关羽失荆州走麦城。夷陵火攻（222）：陆逊'兵贵神速'待刘备入夏，火烧连营七百里，刘备'吾弟孔明何不早言'。"
    },
    "H-KX-23": {
        "name": "康熙：少年天子的权力收割与盛世奠基",
        "description": "八岁登基、擒鳌拜、平三藩、收台湾、御驾亲征噶尔丹、科举制衡",
        "modes": [33, 35, 3, 40, 34],
        "reason": "康熙'朕自八龄即位，凡五十有二年'。核心思维：极致的权力控制术——八岁擒鳌拜（以力破巧）、平三藩（以时间换空间、分化瓦解）、收台湾（施琅水师、郑克塽归降）、三征噶尔丹（御驾亲征、后勤极致）、科举/特科制衡士大夫。盛世本质：权力高度集中+财政极度节俭+边疆最大拓展。",
        "steps": [
            "第1步：格局授权——14岁亲政擒鳌拜：满洲贵族/蒙古贵族/汉臣三方制衡，雷霆出击",
            "第2步：蛰伏积势思维——平三藩（1673-1681）：'撤藩必乱，不撤亦乱'，八年分化吴三桂/尚之信/耿精忠",
            "第3步：制度化制衡——设内阁/军机处雏形、科举复行/博学鸿词科、包衣/上三旗直属皇权",
            "第3步：三衙分兵/权力制衡架构——八旗/绿营/御前侍卫三系统，防单一军事集团尾大不掉",
            "第5步：摸石头过河——收台湾（1683）：施琅'内渡'澎湖，郑克塽降；噶尔丹三征（1690/1696/1697）御驾亲征、屯田军粮、火器制胜"
        ],
        "expected": [
            "版图：北至外兴安岭、西至鄂伦春、南至南海、东至库页岛",
            "人口：从1800万增至6000万，康乾盛世人口爆炸基础",
            "教训：晚年'阿哥党争'、闭关锁国（海禁/禁教）、财政隐悷积重难返"
        ],
        "case": "擒鳌拜（1669）：康熙14岁借'搏克'游戏名义，召鳌拜入宫，以'十四大罪'当场拿下，避免满洲贵族反弹。平三藩：吴三桂云南、尚之信广东、耿精忠福建。康熙'撤藩必乱，不撤亦乱，朕不撤亦乱'，八年分化瓦解，吴三桂孙吴世璠投降。收台湾：施琅建'福建水师'，郑克塽'孤岛无援'降。噶尔丹三征：康熙御驾亲征克鲁伦河，火器/屯田/后勤碾压准噶尔。"
    },
    "H-LH-24": {
        "name": "李鸿章：洋务派的悲剧性现代化实验",
        "description": "淮军/北洋舰队/轮船招商局/马关条约/盛宣怀合作",
        "modes": [38, 34, 40, 23, 19],
        "reason": "李鸿章'三分天下诸葛亮，成败一生李鸿章'。核心思维：器物层面的现代化实验——'师夷长技以制夷'，只引进船/炮/厂/电/铁路，不触动制度/文化/教育根基。淮军（人治）→北洋舰队（器物）→轮船招商局/电报/华盛顿电报/汉冶萍煤铁/北洋水师学堂。甲午海战（1894）彻底暴露'舰队无制度、将领无忠诚、弹药无穿甲'的系统性崩溃。",
        "steps": [
            "第1步：摸石头过河——淮军（1862）：曾国藩授意募安徽乡勇，李鸿章'以乡制乡'，湘军体制地方化",
            "第2步：制度化制衡——北洋舰队（1888）：定远/镇远两铁甲舰，但'北洋大臣'兼'直隶总督'权力过重",
            "第3步：三衙分兵/权力制衡架构——轮船招商局（1872）：官督商办，盛宣怀经营，垄断长江/沿海航运",
            "第4步：自然选择法——汉冶萍煤铁厂（1890）：大冶铁矿+汉阳铁厂+萍乡煤矿，亚洲最大钢铁联企",
            "第5步：边际思维——甲午海战（1894）：北洋舰队'弹药空心/火力不足/指挥混乱'，定远舰自沉，李鸿章赴日签马关条约"
        ],
        "expected": [
            "器物现代化：中国第一条铁路/电报/轮船/钢铁/水师",
            "制度缺失：无海军部、无统一指挥、无军法、无忠诚体系",
            "教训：'中体西用'不可持久，器物不改制度必败，留下'汉奸/卖国贼'千古骂名"
        ],
        "case": "北洋舰队兴衰（1888-1894）：李鸿章斥巨资买定远/镇远（德国伏尔铿厂），建大沽/旅顺/威海基地。但：无海军部统领，北洋大臣李鸿章兼直隶总督，经费挪作淮军军饷。定远舰主炮仅4门、副炮全无穿甲弹、丁汝昌非海军出身。黄海海战：日舰'吉野/松岛'速射炮压制，致远舰葛登弗舰击沉，定远舰自沉刘公岛。马关条约：赔银二亿两、割辽东/台湾/澎湖、开沙市/重庆/苏州/杭州通商。"
    },
    "H-JJ-25": {
        "name": "蒋介石：政军合一的权术家与战略失误",
        "description": "黄埔建军/北伐/剿共/抗战/退守台湾/威权统治",
        "modes": [35, 40, 15, 28, 34],
        "reason": "蒋介石'天下大势，分久必合，合久必分'。核心思维：政军合一的权术平衡——黄埔军校建立'党指挥枪'、北伐以'政治工作'统一军心、剿共'攘外必先安内'、抗战'以空间换时间'、退守台湾'反攻大陆'号召维持合法性。战略失误：金圆券超发→恶性通胀、军队国民党化→战力下降、土地改革不彻底→失民心。",
        "steps": [
            "第1步：蛰伏积势思维——黄埔军校（1924）：苏联援助、周恩来任政治部主任、'党指挥枪'雏形",
            "第2步：制度化制衡——北伐（1926-1928）：政治部/党代表制度、蒋介石'宁汉合流'清党、南京国民政府建立",
            "第3步：三衙分兵/权力制衡架构——剿共（1930-1934）：'围剿'五次，第五次'铁桶计划'逼长征，但张学良杨虎城西安事变逼抗战",
            "第4步：运动歼灭法——抗战（1937-1945）：'以空间换时间'、正面战场牵制日军、游击战配合、最终美援/苏联出兵日军投降",
            "第5步：冗余备份法——退守台湾（1949）：带走黄金/外汇/文物/精锐/技术人员、威权统治+美援+土地改革→亚洲四小龙基础"
        ],
        "expected": [
            "形式上完成统一（北伐/抗战胜利）",
            "实质：金圆券崩溃、军心涣散、民心丧失、大陆溃败",
            "台湾模式：威权+美援+土地改革+出口导向→经济起飞"
        ],
        "case": "剿共五次围剿（1930-1934）：前四次红军'诱敌深入/运动歼灭'破之。第五次德国顾问福克'铁桶计划'步步为营，红军被迫长征。西安事变（1936）：张学良/杨虎城兵谏，蒋介石被迫停止剿共、联共抗日。抗战：正面战场淞沪/徐州/武汉会战牵制日军主力，游击战百团大战/平型关大捷配合。金圆券（1948）：'法币/金圆券'超发，物价指数1947年1→1949年3000万，中产阶级破产。淮海战役：杜聿明/黄伯韬/黄维/刘汝明四大兵团被歼，蒋介石退守台湾。"
    },
    "H-ZD-26": {
        "name": "朱德：红军缔造者的军事民主与战略支撑",
        "description": "南昌起义/朱毛会师/长征/百团大战/十大元帅之首/总司令",
        "modes": [2, 6, 11, 15, 33],
        "reason": "朱德'朱老总'，核心思维：军事民主与战略支撑——'官兵平等/自己动手/打土豪分田地'建立红军政治优势、井冈山会师'朱毛红旗'互补（朱军事/毛政治）、长征'总司令不离前线'、百团大战'游击战规模化'、建国后'不搞权斗/专心建军'。作为'红军父亲'，提供军事专业度与道德权威，支撑毛泽东政治战略。",
        "steps": [
            "第1步：群众路线法——南昌起义（1927）：朱德陈毅率部南下，三湾改编'建立党的支部在连上'、官兵平等/自己动手",
            "第2步：统一战线法——井冈山会师（1928）：朱德/毛泽东/王尔琢/袁文才/王佐五支队伍合编,'朱毛红旗'互补",
            "第3步：灵活策略法——长征（1934-1935）：朱德任总司令/军委副主席，'不离前线/共享艰苦'，四渡赤水/飞夺泸定桥",
            "第4步：运动歼灭法——百团大战（1940）：彭德怀主帅、朱德总司令统筹，105个团20天歼日伪2.5万、破正太/石太/同蒲/平汉/晋浦路",
            "第5步：格局授权——建国后：不争权/不搞派系、专心军事现代化（海军/空军/导弹/核）、'十大元帅之首'道德权威"
        ],
        "expected": [
            "红军从零建立到百万大军，军事制度化（三大纪律八项注意/政治工作/人民战争）",
            "百团大战打破日军'治安强化'，抗战转折",
            "教训：文革受迫害、晚年'不愿多讲军事秘密'、军事思想未系统著述"
        ],
        "case": "井冈山会师（1928）：朱德率南昌起义余部+湘南起义军上井冈，毛泽东率秋收起义军上井冈。朱德军事训练/正规化，毛泽东政治动员/土地革命。王尔琢/袁文才/王佐土著武装归编。三湾改编：'支部建在连上/官兵平等/自己动手/打土豪分田地'。百团大战（1940）：朱德总司令统筹，彭德怀前线指挥，105团20天破五条铁路，日军'治安强化'破产，蒋介石电贺'全国军民之楷模'。"
    }
}

# Add to scenarios
scenarios_zh.update(new_scenarios_zh)

# Save
with open('scenarios_zh.json', 'w', encoding='utf-8') as f:
    json.dump(scenarios_zh, f, ensure_ascii=False, indent=2)

print(f"Updated scenarios_zh.json: {len(scenarios_zh)} total scenarios")

# English versions
new_scenarios_en = {
    "H-CC-21": {
        "name": "Cao Cao: Pragmatic Hegemony via Imperial Legitimacy",
        "description": "Crafty hero, meritocracy, tuntian system, short song verse, Red Cliff defeat",
        "modes": [33, 13, 17, 4, 11],
        "reason": "Cao Cao: 'capable minister in peace, crafty hero in chaos'. Core mindset: pragmatic power politics — merit-based recruitment (Chen Qun's nine-rank), using imperial legitimacy (Emperor Xian as political resource), tuntian solving military logistics (economic base determines superstructure), poetry expressing ambition (Short Song/Tortoise Longevity). Red Cliff defeat: strategic overextension, unfamiliar terrain, loose alliance.",
        "steps": [
            "Step 1: Strategic Delegation — Chen Qun created nine-rank system, broke aristocratic monopoly, merit-only",
            "Step 2: Total Victory Mindset — Held Emperor to command warlords, used legitimacy to suppress separatists without fighting",
            "Step 3: Mental Models — Tuntian system: military/civilian layers, fixed rent/tax, state salt/iron monopoly, solved long-term logistics",
            "Step 4: Encircle Cities from Countryside — Rose from Yanzhou, gradually absorbed Qing/Xu/Jing/Yang, finally unified North",
            "Step 5: Flexible Strategy — Guandu burned Wuchao granary, post-Red Cliff 'disaster from within walls' rallied morale"
        ],
        "expected": [
            "Unified North, founded Cao Wei, laid foundation for Western Jin unification",
            "Nine-rank system lasted 300 years, tuntian became model for military farming",
            "Lessons: strategic overextension (southward campaigns), talent gaps (killing Yang Xiu/Kong Rong), succession undefined causing power struggle"
        ],
        "case": "Battle of Guandu (200): Yuan Shao 100k vs Cao Cao 20k. Cao Cao 'Yuan much planning little decision', Xu You defected burned Wuchao grain, Yuan collapsed. Tuntian (196): registered households, recruited civilians, harvested millions of hu, solved military grain. Nine-rank (220): Chen Qun created 'zhongzheng officials' rating characters, nine grades by virtue/talent, broke 'high ranks no humble families'. Red Cliff (208): arrogance, naval weakness, Pang Tong chain trick, SE wind, Zhou Yu fire attack, Cao Cao 'disaster from within walls' retreated."
    },
    "H-SQ-22": {
        "name": "Sun Quan: Balance Art of the Succession Ruler",
        "description": "Inherited at 19, Red Cliff alliance, Ruxu tuntian, Yiling fire attack, second-gen dilemma",
        "modes": [6, 20, 11, 28, 35],
        "reason": "Sun Quan 'a son should be like Sun Zhongmou'. Core mindset: balance art survival — internally balanced Zhou Yu/Lu Su/Lu Meng/Lu Xun four-gen commanders, externally allied Liu vs Cao / betrayed Guan Yu at Xiangfan / Yiling fire attack on Liu Bei. Succession harder than founding: father/brother legacy, civil-military balance, northern expedition hopeless turned to internal governance.",
        "steps": [
            "Step 1: United Front — Red Cliff allied Liu Bei vs Cao Cao, exploited Cao 'northerners unskilled in naval warfare'",
            "Step 2: Game Theory — Xiangfan: superficially helped Guan Yu north, actually Lu Meng crossed river in white robes surprise Jingzhou, Guan Yu fled Maicheng",
            "Step 3: Flexible Strategy — Ruxu tuntian: Zhu Huan/Lu Fan operated Ruxu fortress, amphibious defense, Cao's 200k attack failed",
            "Step 4: Redundancy Backup — Four commanders: Zhou Yu/Lu Su/Lu Meng/Lu Xun, civil-military complement, prevent single warlord tail-wagging",
            "Step 5: Dormant Accumulation — Yiling (221-222): Lu Xun 'wait till summer/winter' fire attack on Liu Bei 700-li camps, Liu Bei entrusted at Baidi"
        ],
        "expected": [
            "Red Cliff established Three Kingdoms tripartite",
            "Jingzhou recovered, Guan Yu eliminated, southwest frontier secured",
            "Lessons: late superstition, deposed crown prince made Lu King caused 'Two Palaces Strife', Sun Hao young regents usurped power"
        ],
        "case": "Red Cliff Alliance (208): Lu Su brokered Sun-Liu alliance, Zhou Yu/Huang Gai bitter meat/chain/fire attack, Cao fled Huarong. Ruxu Tuntian (210+): Zhu Huan 'water then boats, land then horses', Cao 200k attacked Ruxu failed. Lu Meng seized Jingzhou (219): 'scholar three days must wipe eyes', white-clad crossing, Guan Yu lost Jingzhou fled Maicheng. Yiling Fire (222): Lu Xun 'army values speed' waited Liu Bei into summer, fire burned 700-li camps, Liu Bei 'my brother Kongming why not speak earlier'."
    },
    "H-KX-23": {
        "name": "Kangxi: Boy Emperor's Power Consolidation & Golden Age Foundation",
        "description": "Enthroned at 8, captured Oboi, pacified Three Feudatories, recovered Taiwan, personally campaigned Galdan, exam system balance",
        "modes": [33, 35, 3, 40, 34],
        "reason": "Kangxi 'I ascended at eight, fifty-two years reign'. Core mindset: extreme power control — captured Oboi at 14 (force over skill), pacified Three Feudatories (time for space, divide-conquer), recovered Taiwan (Shi Lang navy, Zheng Keshuang surrendered), three campaigns vs Galdan (personally led, logistics extreme), exams/special exams balanced scholar-officials. Golden age essence: highly concentrated power + extreme fiscal frugality + maximum territorial expansion.",
        "steps": [
            "Step 1: Strategic Delegation — 14 captured Oboi: Manchu nobles/Mongol nobles/Han ministers three-way balance, thunder strike",
            "Step 2: Dormant Accumulation — Three Feudatories (1673-1681): 'revoke inevitable chaos, not revoke also chaos', eight years divided Wu Sangui/Shang Zhixin/Geng Jingzhong",
            "Step 3: Institutional Checks — Inner Cabinet/Grand Council embryo, exams restored/Special Grand Exam, bondservants/Upper Three Banners direct imperial",
            "Step 4: Three Yamen Division — Eight Banners/Green Standard/Imperial Guard three systems, prevent single military group tail-wagging",
            "Step 5: Crossing River by Feeling Stones — Taiwan (1683): Shi Lang 'inner crossing' Penghu, Zheng Keshuang surrendered; Galdan three campaigns (1690/1696/1697) personally led, tuntian logistics, firearms crushed Dzungar"
        ],
        "expected": [
            "Territory: north to Outer Xingan, west to Oronchon, south to South China Sea, east to Sakhalin",
            "Population: 18M to 60M, Kang-Qian population explosion foundation",
            "Lessons: late 'Prince faction strife', closed-door (sea ban/religion ban), fiscal hidden debts"
        ],
        "case": "Captured Oboi (1669): Kangxi 14 used 'bokke' wrestling pretext, summoned Oboi, '14 great crimes' seized on spot, avoided Manchu noble backlash. Three Feudatories: Wu Sangui Yunnan, Shang Zhixin Guangdong, Geng Jingzhong Fujian. Kangxi 'revoke inevitable chaos, not revoke also chaos, I not revoke also chaos', eight years divide-conquer, Wu Sangui grandson Wu Shifan surrendered. Taiwan: Shi Lang built 'Fujian Navy', Zheng Keshuang 'isolated island no aid' surrendered. Galdan campaigns: Kangxi personally led Kerulen River, firearms/tuntian/logistics crushed Dzungar."
    },
    "H-LH-24": {
        "name": "Li Hongzhang: Tragic Modernization Experiment of Self-Strengthening",
        "description": "Huai Army/Beiyang Fleet/China Merchants Steam/Shimonoseki Treaty/Sheng Xuanhuai partnership",
        "modes": [38, 34, 40, 23, 19],
        "reason": "Li Hongzhang 'Three Kingdoms Zhuge Liang, success/failure one life Li Hongzhang'. Core mindset: material-layer modernization experiment — 'learn barbarian skills to control barbarians', only imported ships/guns/factories/electricity/railways, never touched system/culture/education roots. Huai Army (personal rule) → Beiyang Fleet (hardware) → China Merchants Steam/Telegraph/Hanyang Ironworks/Beiyang Naval Academy. First Sino-Japanese War (1894) exposed 'fleet no system, officers no loyalty, shells no armor-piercing' systemic collapse.",
        "steps": [
            "Step 1: Crossing River by Feeling Stones — Huai Army (1862): Zeng Guofan authorized Anhui militia, Li 'using locals against locals', Xiang Army system localized",
            "Step 2: Institutional Checks — Beiyang Fleet (1888): Dingyuan/Zhenyuan two ironclads, but 'Beiyang Minister'兼'Zhili Governor' power overweight",
            "Step 3: Three Yamen Division — China Merchants Steam (1872): official-supervised merchant-managed, Sheng Xuanhuai operated, monopolized Yangtze/coastal shipping",
            "Step 4: Natural Selection — Hanyang Ironworks (1890): Daye iron ore + Hanyang ironworks + Pingxiang coal, Asia's largest steel combine",
            "Step 5: Marginal Thinking — First Sino-Japanese War (1894): Beiyang Fleet 'shells hollow/firepower insufficient/command chaos', Dingyuan scuttled, Li signed Shimonoseki"
        ],
        "expected": [
            "Material modernization: China's first railway/telegraph/steamship/steel/naval force",
            "Systemic absence: no Navy Ministry, no unified command, no military law, no loyalty system",
            "Lesson: 'Chinese essence Western utility' unsustainable, hardware without software fails, left 'traitor/sellout' eternal infamy"
        ],
        "case": "Beiyang Fleet rise/fall (1888-1894): Li spent huge on Dingyuan/Zhenyuan (German Vulkan), built Dagu/Lushun/Weihai bases. But: no Navy Ministry, Beiyang Minister Li兼Zhili Governor, funds diverted to Huai Army pay. Dingyuan main guns only 4, no armor-piercing shells, Ding Ruchang not naval background. Yellow Sea Battle: Japanese 'Yoshino/Matsushima' rapid-fire guns suppressed, Zhiyuan/Fengru sunk, Dingyuan scuttled at Liu Gong Island. Shimonoseki: 200M taels indemnity, ceded Liaodong/Taiwan/Penghu, opened Shashi/Chongqing/Suzhou/Hangzhou ports."
    },
    "H-JJ-25": {
        "name": "Chiang Kai-shek: Party-Army Fusion Politician & Strategic Blunders",
        "description": "Whampoa founding/Northern Expedition/Encirclement Campaigns/War of Resistance/Retreat to Taiwan/Authoritarian Rule",
        "modes": [35, 40, 15, 28, 34],
        "reason": "Chiang 'world trend, divided long must unite, united long must divide'. Core mindset: party-army fusion power balance — Whampoa 'party commands gun', Northern Expedition 'political work' unified morale, Encirclement 'pacify interior before resist exterior', Resistance 'trade space for time', Taiwan 'counterattack mainland' slogan maintained legitimacy. Strategic blunders: Gold Yuan hyperinflation, army partisanization → combat decline, land reform incomplete → lost hearts.",
        "steps": [
            "Step 1: Dormant Accumulation — Whampoa (1924): Soviet aid, Zhou Enlai political dept director, 'party commands gun' embryo",
            "Step 2: Institutional Checks — Northern Expedition (1926-1928): Political Dept/Party Representative system, Chiang 'Ning-Han merge' purge, Nanjing Nationalist Gov established",
            "Step 3: Three Yamen Division — Encirclement (1930-1934): 'Encirclement' five times, fifth 'Iron Bucket Plan' forced Long March, but Zhang Xueliang/Yang Hucheng Xi'an Incident forced Resistance",
            "Step 4: Mobile Warfare — Resistance (1937-1945): 'trade space for time', frontal battles pinned Japanese main force, guerrilla Hundred Regiments/Pingxingguan complemented, finally US aid/Soviet entry Japanese surrendered",
            "Step 5: Redundancy Backup — Retreat Taiwan (1949): took gold/forex/artifacts/elite/technocrats, authoritarian + US aid + land reform → Asian Four Dragons foundation"
        ],
        "expected": [
            "Formally completed unification (Northern Expedition/Resistance victory)",
            "Substance: Gold Yuan collapsed, army morale disintegrated, hearts lost, mainland collapsed",
            "Taiwan model: Authoritarian + US aid + land reform + export-oriented → economic takeoff"
        ],
        "case": "Five Encirclements (1930-1934): First four Red Army 'lure deep/mobile warfare' broke. Fifth German adviser Falk 'Iron Bucket Plan' step-by-step, Red Army forced Long March. Xi'an Incident (1936): Zhang Xueliang/Yang Hucheng forced Chiang stop encirclement, United Front vs Japan. Resistance: Frontal Shanghai/Xuzhou/Wuhan pinned Japanese main force, guerrilla Hundred Regiments/Pingxingguan complemented. Gold Yuan (1948): 'Fabijin/Yuan' hyperissue, price index 1947=1 → 1949=30M, middle class bankrupted. Huaihai Campaign: Du Yuming/Huang Baitao/Huang Wei/Liu Ruming four army groups annihilated, Chiang retreated to Taiwan."
    },
    "H-ZD-26": {
        "name": "Zhu De: Red Army Founder's Military Democracy & Strategic Backbone",
        "description": "Nanchang Uprising/Zhu-Mao Meeting/Long March/Hundred Regiments/Ten Marshals First/Commander-in-Chief",
        "modes": [2, 6, 11, 15, 33],
        "reason": "Zhu De 'Commander Zhu', core mindset: military democracy & strategic support — 'officers-soldiers equality/do it yourself/fight landlords divide land' built Red Army political advantage, Jinggangshan meeting 'Zhu-Mao red flags' complementary (Zhu military/Mao political), Long March 'commander-in-chief never left front', Hundred Regiments 'guerrilla warfare scaled', post-1949 'no power struggles/focus on military building'. As 'Red Army Father', provided military professionalism & moral authority supporting Mao's political strategy.",
        "steps": [
            "Step 1: Mass Line — Nanchang Uprising (1927): Zhu/Chen led troops south, Sanwan Reorganization 'party branch in company' officers-soldiers equality/do it yourself",
            "Step 2: United Front — Jinggangshan Meeting (1928): Zhu/Mao/Wang Erzhuang/Yuan Wencai/Wang Zuo five forces merged, 'Zhu-Mao red flags' complementary",
            "Step 3: Flexible Strategy — Long March (1934-1935): Zhu Commander-in-Chief/Vice Chair Military Commission, 'never left front/shared hardships', Four Crossings Chishui/Seizing Luding Bridge",
            "Step 4: Mobile Warfare — Hundred Regiments (1940): Peng Dehuai field commander, Zhu Commander-in-Chief coordinated, 105 regiments 20 days destroyed 25k Japanese/puppet, broke Zhengtai/Shitai/Tongpu/Pinghan/Jinpu railways",
            "Step 5: Strategic Delegation — Post-1949: no power struggles/no factions, focused military modernization (navy/airforce/missile/nuclear), 'First of Ten Marshals' moral authority"
        ],
        "expected": [
            "Red Army from zero to million-strong, institutionalized (Three Disciplines Eight Points/political work/people's war)",
            "Hundred Regiments broke Japanese 'security strengthening', resistance turning point",
            "Lessons: Cultural Revolution persecuted, late years 'unwilling to speak military secrets', military thought never systematically written"
        ],
        "case": "Jinggangshan Meeting (1928): Zhu led Nanchang remnants + Hunan uprising to Jinggang, Mao led Autumn Harvest uprising to Jinggang. Zhu military training/regularization, Mao political mobilization/land revolution. Wang Erzhuang/Yuan Wencai/Wang Zuo local armed merged. Sanwan Reorganization: 'party branch in company/officers-soldiers equality/do it yourself/fight landlords divide land'. Hundred Regiments (1940): Zhu Commander-in-Chief coordinated, Peng Dehuai field command, 105 regiments 20 days broke five railways, Japanese 'security strengthening' bankrupt, Chiang wired 'national military-civilian model'."
    }
}

# Add to English scenarios
scenarios_en.update(new_scenarios_en)

with open('scenarios_en.json', 'w', encoding='utf-8') as f:
    json.dump(scenarios_en, f, ensure_ascii=False, indent=2)

print(f"Updated scenarios_en.json: {len(scenarios_en)} total scenarios")