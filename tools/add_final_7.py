import json

# Load existing scenarios
with open('scenarios_zh.json', 'r', encoding='utf-8') as f:
    scenarios_zh = json.load(f)

with open('scenarios_en.json', 'r', encoding='utf-8') as f:
    scenarios_en = json.load(f)

# 7 final figures - Chinese
new_zh = {
    "H-HF-33": {
        "name": "韩非：法家集大成的制度设计师",
        "description": "以法为教、势法术三位一体、非人治、秦帝国制度蓝图",
        "modes": [32, 20, 19, 28, 34],
        "reason": "韩非集法家之大成，核心思维：制度设计的终极理性——以法为教替代以人为治，势法术三位一体（势=权力基础、法=规则标准、术=驭臣手段），主张废先王之教、禁私门之学、以法吏为师。其《韩非子》成秦帝国乃至中国两千年皇权制度的理论蓝图。",
        "steps": [
            "第1步：程序正义法——立法公开、执法严明、司法独立、普遍平等，法不阿贵、绳不挠曲",
            "第2步：博弈论思维——分析君臣/官民/强弱博弈矩阵，设计术驭臣、法治民、势立威的纳什均衡",
            "第3步：边际思维——计算严刑重罚的边际成本与收益，重罚轻罪提高犯罪成本至无人敢犯",
            "第4步：冗余备份法——设参伍什伍连坐法、密告奖励、官员互监，关键节点多重校验防腐败",
            "第5步：制度化制衡——因民之所利而利之、因民之所恶而恶之，以制度替代人治，防权臣尾大不掉"
        ],
        "expected": [
            "为秦始皇统一六国、建立郡县制提供理论支撑",
            "《韩非子》成中国法治思想巅峰，影响两千年帝制制度设计",
            "教训：过度依赖严刑峻法缺乏人文关怀，秦二世而亡"
        ],
        "case": "韩非孤愤著书五十五篇：有度定制度、八奸识腐败、五蠹清寄生、显学废私学、六反防异议。李斯采其废先王之教、禁私门之学、以法吏为师，秦始皇采势法术三位一体：势=皇帝绝对权威、法=严刑重罚/赏罚分明、术=驭臣手段/权衡轻重。结果：秦灭六国、建立中央集权郡县制，虽二世而亡但制度框架延续两千年。"
    },
    "H-WAS-34": {
        "name": "王安石：不避浮云的变法改革家",
        "description": "青苗/募役/保马/保甲/市易/均输/方田/科举改制、财政军事教育三位一体",
        "modes": [38, 8, 40, 28, 35],
        "reason": "王安石天变不足畏、祖宗不足法、人言不足恤，核心思维：系统性变法的极致执行力——财政（青苗/均输/市易）、军事（保马/保甲/减冗兵）、教育（改科举/废诗赋/设三舍法）三位一体变法。以摸石头过河精神在宋神宗支持下推行新法，虽因派系斗争/执行变形/神宗退守而失败，但变法不怕阻力精神千古传颂。",
        "steps": [
            "第1步：摸石头过河——青苗法试点：先在开封府界/河北路试行，政府出借贷息钱助农，验证可行再推广",
            "第2步：渐进改革法——募役法分期：先免富户差役收钱雇人、再推广至全国、最后建常平仓调节",
            "第3步：三衙分兵/权力制衡架构——三司条例司/制置三司条例司/详定役法司并行，财政/军事/行政三权分立防单一部门垄断",
            "第4步：冗余备份法——保甲/保马法：十户为保、五十户为大保、十大保为都保，农闲练兵、战时征发、平时治安，兵农合一",
            "第5步：蛰伏积势——面对司马光/苏轼等旧党激烈反对，王安石不避浮云遮望眼，坚持变法至神宗妥协罢相"
        ],
        "expected": [
            "宋神宗朝财政收入大增、禁军精锐化、科举选拔实用人才",
            "新法推行18年（1069-1085），虽元祐废新法但保甲/募役/科举改制遗留至今",
            "教训：执行层变形（青苗成高利贷）、财政依赖垄断利润、派系斗争导致改革断裂"
        ],
        "case": "青苗法（1069）：政府以常平仓钱谷春贷秋收、息二分，助农抗旱/备耕，防兼并豪强高利贷。募役法（1070）：免差役钱雇人服役，富户出钱、贫户免役、政府统管。市易法（1071）：设市易司平抑物价、抑制商人囤积。均输法（1072）：中央统一调拨财货、减中间环节耗费。保马法（1072）：十户一保、五十户一大保，农闲教阵/战时征发。方田均税（1073）：量田定等、均平税赋。改科举（1071）：废诗赋、增经义/论策、设三舍法升级选才。结果：财政盈余、军备振作、人才实用，但执行变形、派系倾轧、神宗退守导致元祐废法。"
    },
    "H-ZZD-35": {
        "name": "张之洞：中体西用的洋务运动集大成者",
        "description": "广雅书局/湖北枪炮厂/汉阳铁厂/湖北织布局/两湖书院/劝学篇、中学为体西学为用",
        "modes": [38, 34, 23, 28, 8],
        "reason": "张之洞中学为体、西学为用，核心思维：器物层面系统性现代化实验——在湖广/两广/两江总督任上，系统建设军工（湖北枪炮/汉阳铁厂/汉阳造）、纺织（湖北织布/麻纺/毛纺）、教育（广雅书局/两湖书院/留日预备/劝学篇）、实业（大冶铁矿/平煤/汉冶萍/长芦盐/轮船/电报）。师夷长技以制夷系统化，虽中体制约西用深度，但为晚清工业/教育/军事奠基。",
        "steps": [
            "第1步：摸石头过河——湖北枪炮厂（1890）：聘德籍工程师、引进克虏伯技术、建枪炮/弹药/火药三大生产线，年产汉阳造步枪万支",
            "第2步：自然选择法——汉阳铁厂（1890）：大冶铁矿+汉阳铁厂+平煤=汉冶萍煤铁联合企业，中国第一近代钢铁联合体",
            "第3步：目标管理法——教育体系：广雅书局（翻译/出版西学书籍）、两湖书院（新式学堂/留日预备/速成武备）、劝学篇（阐述中体西用理论）",
            "第4步：制度化制衡——实业管理：官督商办/官商合办/股份制试点，引入德/日管理模式、建会计/审计/股东会制度",
            "第5步：渐进改革法——劝学篇（1898）：中学为体、西学为用，体=纲常伦理/经史子集，用=格致/兵制/律例/农工/商贾，理论支撑变法自强"
        ],
        "expected": [
            "汉阳造成晚清/民国/抗战主力装备，汉冶萍成亚洲最大钢铁联企",
            "两湖书院/广雅书局成南方新式教育高地，培养大批留日/新式人才",
            "教训：中体束缚西用深度，官僚腐败/技术依赖/资本不足，辛亥后资产多流失"
        ],
        "case": "汉阳铁厂（1890-1948）：张之洞调查大冶铁矿储量3亿吨、平煤优质焦煤，决心建钢铁厂。聘德籍工程师傅维琛设计，引进西门子敞炉/轧钢机，1894年出铁。后扩轧钢/炼钢/铸造，汉阳造步枪/大炮配套。1908并入汉冶萍公司，成亚洲最大钢铁联企。广雅书局（1888）：翻译出版天演论/原富/兵制等西学书200余种，发行百万册。两湖书院（1897）：设经/史/法/理/格致五门，聘日籍教师，留日预备班输送蔡和森/任弼时等赴日留学。劝学篇（1898）：系统阐述中体西用，为戊戌变法提供理论。结果：器物现代化领先，制度文化滞后。"
    },
    "H-HS-36": {
        "name": "胡适：大胆假设小心求证的实验主义先驱",
        "description": "实验主义/逐步改良/文学革命/科学方法/容忍/自由主义",
        "modes": [38, 37, 23, 28, 35],
        "reason": "胡适大胆假设、小心求证，核心思维：杜威实验主义的中国化实践——主张多研究些问题，少谈些主义，用科学方法解决中国问题。文学革命八不主义推行白话文、新式标点、新诗体；留学/办刊/办学/译著/编史，以逐步改良替代激进革命，以容忍替代斗争。虽被激进派批投降派，但科学方法/学术自由/容忍精神成现代中国学术基因。",
        "steps": [
            "第1步：摸石头过河——文学革命（1917）：新青年发表文学改良刍议八不主义，推行白话文/新式标点/新诗体，以实验态度试错",
            "第2步：知行合一——留学归国（1910-1917）：哥大师从杜威学实验主义，归国办新青年/努力周报/独立评论，以笔代枪",
            "第3步：自然选择法——整理国故（1919-1930）：大胆假设、小心求证，用科学方法整理红楼梦/水浒/水经注/经学/哲学史，建学术规范",
            "第4步：冗余备份法——容忍与自由（1920s-1940s）：我不同意你的观点，但我誓死捍卫你说话的权利，主张学术自由/思想自由/宽容异见",
            "第5步：蛰伏积势——逐步改良（1930s-1940s）：反对激进革命/暴力斗争，主张多研究些问题、少谈些主义、以教育/法制/制度渐进改良社会"
        ],
        "expected": [
            "白话文成国语标准，现代标点/新诗体/学术规范沿用至今",
            "实验主义/学术自由/容忍精神成现代中国学术/公共讨论基因",
            "教训：逐步改良在战乱/极端年代显无力，晚年赴台学术影响力减弱"
        ],
        "case": "文学革命（1917）：胡适文学改良刍议八不主义：不讲无有之言/不滥用典故/不讲对仗/不避俗字俗语/不求对属/不尽故实/不避虚词/不求悲切。配合陈独秀/钱玄同/刘半农/周作人/鲁迅等推行白话文。整理国故（1920s）：用考据/考证/实证方法研究红楼梦考据/水浒传考/水经注疏/中国哲学史大纲，确立大胆假设、小心求证学术范式。容忍精神：1920年代反对打倒孔家店激进派，主张宽容/自由/人权，被左派批自由主义投降派。结果：科学方法/学术规范/白话文成现代学术基石。"
    },
    "H-LX-37": {
        "name": "鲁迅：横眉冷对千夫指的解构大师",
        "description": "横眉冷对/剖析国民劣根性/阿Q精神/解构传统/杂文战斗/思想启蒙",
        "modes": [30, 31, 37, 28, 35],
        "reason": "鲁迅横眉冷对千夫指、俯首甘为孺子牛，核心思维：批判性解构的最高艺术——用阿Q精神解构国民精神胜利法、用看客讽刺麻木、用祥林嫂揭露封建礼教吃人、用狂人日记解构礼教吃人本质。杂文投枪匕首直刺时弊，横眉冷对面对攻击不退缩。以解构替代建构，以诊断替代开方，成现代中国批判精神图腾。",
        "steps": [
            "第1步：认知偏差识别法——识别精神胜利法：阿Q被打儿子打老子、被羞辱我比你强、失败归因外部、以此维护脆弱自尊",
            "第2步：框架效应法——重构吃人框架：狂人日记翻开历史，这历史没有年代，歪歪斜斜的每页上都写着仁义道德几个字，我横竖睡不着，仔细看了半夜，才从字缝里看出字来，满本都写着两个字是吃人",
            "第3步：知行合一——杂文投枪：横眉冷对千夫指、俯首甘为孺子牛，面对右翼围攻/左派清算/权威压制，坚持说真话、揭黑暗",
            "第4步：自然选择法——解构国民性：阿Q正传/祥林嫂/孔乙己/药/社戏系列，系统剖析国民劣根性：麻木/自欺/奴性/势利/冷漠",
            "第5步：蛰伏积势——横眉冷对：面对国民党通缉/左联清洗/文化界围攻，战士生前便已死，何必身后更垂名，以笔为枪死战不退"
        ],
        "expected": [
            "呐喊/彷徨/野草/朝花夕拾/华盖集等成现代文学经典",
            "阿Q精神/精神胜利法/看客/吃人成解构国民性核心概念",
            "教训：纯批判缺建设性方案、晚年被意识形态裹挟、杂文易被断章取义"
        ],
        "case": "狂人日记（1918）：中国第一篇白话小说，以狂人视角解构礼教吃人：我翻开历史一查，这历史没有年代，歪歪斜斜的每页上都写着仁义道德几个字……满本都写着两个字是吃人。阿Q正传（1921）：阿Q被打倒自慰儿子打老子、被赵太爷打我比你强、革命胜利想当年造反不得，现在也造反不得，精神胜利法成国民劣根性代名词。杂文战斗：1920s-1930s与梁实秋/徐志摩/成仿吾/鲁迅/瞿秋白等论战，横眉冷对千夫指、俯首甘为孺子牛。结果：批判精神成现代中国知识分子图腾。"
    },
    "H-QXS-38": {
        "name": "钱学森：系统工程之父的大系统观",
        "description": "系统工程/大系统观/导弹航天体系化/五大发明/知识工程/思维科学",
        "modes": [12, 22, 14, 29, 28],
        "reason": "钱学森系统工程之父，核心思维：大系统观的工程化落地——从美喷气推进实验室/JPL返国，建中国导弹/航天事业从无到有。提出系统工程五大发明（系统分析/系统综合/系统优化/系统决策/系统管理），大系统观：工程系统/管理系统/社会系统/自然系统/思维系统五大类。建知识工程、思维科学，主张从娃娃抓起培养创新人才。",
        "steps": [
            "第1步：系统思维法——建系统工程学科：引入美系统工程方法论，建北京自动化所/七机部/航天五院，建立型号-系统-总体三级管理体制",
            "第2步：战争重心法——抓两弹一星核心：集中全国优势资源攻克导弹/核武器/卫星，集中力量办大事体系化推进",
            "第3步：目标管理法——钱学森班培养：西交大/国防科大设力学/控制/系统跨学科实验班，从娃娃抓起培养系统型创新人才",
            "第4步：反馈回路法——知识工程/思维科学：建知识工程处理非结构化知识、思维科学研究人脑/机器智能，预见AI时代",
            "第5步：冗余备份法——体系化冗余：导弹多型号并行/卫星多星并行/发射场多基地/测控多站点，关键节点多重备份"
        ],
        "expected": [
            "两弹一星突破美苏封锁，确立中国战略威慑地位",
            "建立完整航天工业体系：五院/四大发射场/测控网/TT&C网",
            "系统工程方法论推广至国防/经济/社会/管理，成国家重大工程标配"
        ],
        "case": "两弹一星（1956-1970）：钱学森任五院院长，建型号-系统-总体三级管理：总体部统筹、系统所分工、型号所攻关。导弹：东风1/2/3/4/5代际突破、潜射/陆基/机动多平台。核武器：596/氢弹/小型化/导弹核弹头。卫星：东方红一号/实践/风云/东方红二号。建四大发射场（酒泉/太原/西昌/文昌）、测控网/远洋测量船队。结果：中国成世界第五个自主发射卫星国家、战略威慑确立。钱学森晚年推广系统工程至经济/管理/社会，创钱学森班培养系统型人才。"
    },
    "H-RZF-39": {
        "name": "任正非：活下去的灰度管理大师",
        "description": "活下去/以客户为中心/华山论剑/灰度管理/不上市/员工持股/基础研究10%+",
        "modes": [36, 28, 23, 17, 35],
        "reason": "任正非没有成功的道路，只有不断进取的道路，核心思维：生存第一的灰度管理艺术——活下去是最高战略，以客户为中心是唯一价值源，华山论剑内部竞争淘汰平庸，灰度管理在矛盾中寻找平衡（集权/分权、标准/灵活、短期/长期）。不上市/不分红/员工持股/基础研究投入>营收10%，程控交换->通信设备->手机->5G->鸿蒙->云->数能->智驾，每代技术积累支撑下一代。",
        "steps": [
            "第1步：蛰伏积势——创业初期（1987-1995）：代理香港重庆仪器厂HJC交换机，积累首桶金、团队、渠道，不贪快、不盲目扩张",
            "第2步：自然选择法——产品线竞争（1996-2000）：华山论剑GSM/交换机/手机多线并行，市场选择胜者，淘汰平庸",
            "第3步：格局授权——以客户为中心：IPD/LTC/IFS流程变革，引进IBM/PwC顾问，以客户需求驱动研发/交付/服务全流程",
            "第4步：笨功夫/死磕到底——基础研究投入>10%营收：数学/物理/材料/算法/芯片/编译器/数据库/操作系统全栈自研",
            "第5步：三衙分兵/权力制衡架构——不上市/员工持股/委员会治理：任正非仅1%股份、否决权/任命权，轮值CEO/四大委员会/监事会制衡，防单一人/单一部门决策失误"
        ],
        "expected": [
            "从代理商->全球通信巨头，5G专利全球第一、手机出货曾全球第一",
            "年研发投入>1600亿、基础研究>10%、员工持股激励全球顶尖人才",
            "教训：制裁下生存艰难、鸿蒙生态建设道阻且长、管理复杂度随规模指数级上升"
        ],
        "case": "华为发展四阶段：1)代理商（1987-1995）：代理HJC交换机，积累资金/团队/渠道。2)自研交换机（1996-2000）：C&C08/10程控交换机打破外资垄断，农村市场切入。3)全球化/手机（2001-2010）：IPD流程引进、海外市场突围、手机终端异军突起。4)5G/全栈（2011-）：数学/物理/材料/芯片/编译器/数据库/OS/云/智驾全栈自研，5G专利全球第一。灰度管理：在矛盾中寻找平衡——集权战略/分权战术、标准流程/灵活创新、短期生存/长期投入。不上市避免短期资本压力，员工持股绑定核心人才。结果：年研发1647亿（2023），基础研究占比>10%，全球顶尖人才聚集。"
    }
}

# Add to Chinese scenarios
scenarios_zh.update(new_zh)

# Save Chinese
with open('scenarios_zh.json', 'w', encoding='utf-8') as f:
    json.dump(scenarios_zh, f, ensure_ascii=False, indent=2)

print(f"Updated scenarios_zh.json: {len(scenarios_zh)} total scenarios")

# English versions
new_en = {
    "H-HF-33": {
        "name": "Han Fei: Legalist Master System Designer",
        "description": "Law as teaching, power-law-method trinity, anti-personal-rule, Qin Empire institutional blueprint",
        "modes": [32, 20, 19, 28, 34],
        "reason": "Han Fei synthesized Legalism to its peak. Core mindset: ultimate rationality in institutional design — law as teaching replacing rule by man, power-law-method trinity (power=authority base, law=rule standard, method=minister-control technique), advocated abolish former kings teachings, ban private schools, make legal officials the teachers. His Han Feizi became theoretical blueprint for Qin Empire and 2000 years of Chinese imperial system.",
        "steps": [
            "Step 1: Procedural Justice — Public legislation, strict enforcement, independent judiciary, universal equality, law does not favor nobility, rope does not bend for curves",
            "Step 2: Game Theory — Analyzed ruler-minister/official-people/strong-weak game matrix, designed method to control ministers, law to govern people, power to establish authority Nash equilibrium",
            "Step 3: Marginal Thinking — Calculated marginal cost/benefit of severe punishment, heavy penalty for light crimes raises crime cost until none dare offend",
            "Step 4: Redundancy Backup — Five-household mutual responsibility collective liability, informant rewards, mutual official supervision, multi-layer verification at key nodes anti-corruption",
            "Step 5: Institutional Checks — Benefit what people benefit, hate what people hate, system replaces rule of man, prevents ministerial overreach"
        ],
        "expected": [
            "Provided theoretical support for Qin Shi Huang unification and commandery-county system",
            "Han Feizi became pinnacle of Chinese legalist thought, influenced 2000 years imperial institutional design",
            "Lessons: over-reliance on harsh laws lacking humanism led to Qin fall in two generations"
        ],
        "case": "Han Fei Solitary Indignation wrote 55 chapters: Youdu sets systems, Bajian identifies corruption, Wudu clears parasites, Xianxue bans private learning, Liu Fan prevents dissent. Li Si adopted abolish former kings teachings, ban private schools, make legal officials teachers. Qin Shi Huang adopted power-law-method trinity: power=emperor absolute authority, law=severe rewards punishments, method=minister control techniques. Result: Qin conquered six states, established centralized commandery-county system. Though fell in two generations, institutional framework lasted 2000 years."
    },
    "H-WAS-34": {
        "name": "Wang Anshi: Reformer Who Feared No Clouds",
        "description": "Green Sprouts/Recruitment Service/Horse Rearing/Baojia/Market Exchange/Equal Transport/Field Survey/Exam Reform — fiscal/military/education trinity",
        "modes": [38, 8, 40, 28, 35],
        "reason": "Wang Anshi heaven changes not to fear, ancestors not to follow, people words not to heed. Core mindset: extreme execution in systemic reform — fiscal (Green Sprouts/Equal Transport/Market Exchange), military (Horse Rearing/Baojia/reduce redundant troops), education (exam reform/abolish poetry/establish Three Colleges) trinity reform. With crossing river by feeling stones spirit under Emperor Shenzong support, pushed New Policies. Though failed due to factional struggle/execution distortion/emperor retreat, reform fears no resistance spirit echoes through ages.",
        "steps": [
            "Step 1: Crossing River by Feeling Stones — Green Sprouts pilot: first tested in Kaifeng/Hebei circuits lending seed money to farmers, verified viable then scaled",
            "Step 2: Gradual Reform — Recruitment Service phased: first exempt wealthy from corvee collect money to hire, then nationalize, finally build ever-normal granaries",
            "Step 3: Three Yamen Division — Three Departments Conditions Bureau/Established Three Departments Conditions Bureau/Detailed Corvee Law Bureau parallel, fiscal/military/admin three-power separation prevent single dept monopoly",
            "Step 4: Redundancy Backup — Baojia/Horse Rearing: ten households a bao, fifty a large bao, ten large bao a du bao, train in farming off-season, mobilize in war, maintain peace, soldier-farmer unity",
            "Step 5: Dormant Accumulation — Faced Sima Guang/Su Shi fierce opposition, Wang not fearing clouds blocking view, persisted reform until Emperor Shenzong compromised dismissed him"
        ],
        "expected": [
            "Shenzong reign fiscal revenue surged, imperial guards elite, exams selected practical talents",
            "New Policies ran 18 years (1069-1085), though Yuanyou abolished, Baojia/Recruitment/Exam reforms legacy remains",
            "Lessons: execution distortion (Green Sprouts became usury), fiscal reliance on monopoly profits, factional strife broke reform continuity"
        ],
        "case": "Green Sprouts (1069): gov lent ever-normal granary money/grain spring repay autumn, 2% interest, helped farmers drought/planting, prevented gentry usury. Recruitment Service (1070): exempt corvee money hire labor, wealthy pay money, poor exempt, gov manages. Market Exchange (1071): established Market Exchange Bureau stabilize prices, curb merchant hoarding. Equal Transport (1072): central unified allocation goods, reduce intermediate loss. Baojia (1072): ten households bao, fifty large bao, farm off-season train, war mobilize, peace security. Field Survey Equal Tax (1073): measure land grade, equalize tax. Exam Reform (1071): abolish poetry, add classical meaning/essay, establish Three Colleges upgrade selection. Result: fiscal surplus, military revitalized, talents practical. But execution distorted, fiscal relied on monopoly profits, factional strife led to reform collapse."
    },
    "H-ZZD-35": {
        "name": "Zhang Zhidong: Self-Strengthening Master of Chinese Essence Western Utility",
        "description": "Guangya Book Bureau/Hubei Arsenal/Hanyang Ironworks/Hubei Textile/Two Lakes Academy/Exhortation to Learning — Chinese essence Western utility",
        "modes": [38, 34, 23, 28, 8],
        "reason": "Zhang Zhidong Chinese essence Western utility. Core mindset: systematic hardware-layer modernization — as Governor of Huguang/Liangguang/Liangjiang, systematically built military industry (Hubei Arsenal/Hanyang Ironworks/Hanyang Made), textile (Hubei Textile/hemp/cotton/wool), education (Guangya Book Bureau/Two Lakes Academy/Japan preparatory/Exhortation to Learning), industry (Daye Iron Mine/Ping Coal/Hanye Ping/Changlu Salt/shipping/telegraph). Learn barbarian skills to control barbarians systematized. Though Chinese essence constrained Western utility depth, laid foundation for late Qing industry/education/military.",
        "steps": [
            "Step 1: Crossing River by Feeling Stones — Hubei Arsenal (1890): hired German engineers, imported Krupp tech, built rifle/cannon/ammunition three production lines, annual output ten thousand Hanyang Made rifles",
            "Step 2: Natural Selection — Hanyang Ironworks (1890): Daye Iron Mine + Hanyang Ironworks + Ping Coal = Hanye Ping Coal-Iron Combine, China first modern steel combine",
            "Step 3: Management by Objectives — Education system: Guangya Book Bureau (translate/publish Western books), Two Lakes Academy (modern school/Japan preparatory/rapid military), Exhortation to Learning (explicate Chinese essence Western utility theory)",
            "Step 4: Institutional Checks — Industry management: official-supervised merchant-managed/official-merchant joint/stock trial, introduced German/Japanese management, established accounting/audit/shareholder meeting systems",
            "Step 5: Gradual Reform — Exhortation to Learning (1898): Chinese essence Western utility, essence=ethics/history, utility=gezhi/military/law/agriculture/industry/commerce, theoretical support for reform"
        ],
        "expected": [
            "Hanyang Made became late Qing/Republic/resistance war main equipment, Hanye Ping became Asia largest steel combine",
            "Two Lakes Academy/Guangya Book Bureau became southern modern education highland, trained batch of Japan-returnees/modern talents",
            "Lessons: Chinese essence constrained Western utility depth, bureaucratic corruption/tech dependence/insufficient capital, post-Xinhai assets mostly lost"
        ],
        "case": "Hanyang Ironworks (1890-1948): Zhang Zhidong surveyed Daye Iron Mine 300M tons, Ping Coal quality coking coal, decided build steel works. Hired German engineer Fu Weichen design, imported Siemens open hearth/rolling mill, 1894 produced iron. Later expanded rolling/steelmelting/casting, Hanyang Made rifles/cannons supporting. 1908 merged into Hanye Ping Co, became Asia largest steel combine. Guangya Book Bureau (1888): translated/published Tian Yan Lun/Yuan Fu/Bing Zhi 200+ Western books, distributed millions. Two Lakes Academy (1897): five gates Classics/History/Law/Principles/Gezhi, hired Japanese teachers, Japan preparatory class sent Cai Hesen/Ren Bishi etc to Japan. Exhortation to Learning (1898): systematically explicated Chinese essence Western utility, theoretical support for Hundred Days Reform. Result: hardware modernization led, institutional culture lagged."
    },
    "H-HS-36": {
        "name": "Hu Shi: Bold Hypothesis Careful Verification Experimentalism Pioneer",
        "description": "Experimentalism/Gradual Reform/Literary Revolution/Scientific Method/Tolerance/Liberalism",
        "modes": [38, 37, 23, 28, 35],
        "reason": "Hu Shi bold hypothesis careful verification. Core mindset: Dewey experimentalism Chinese practice — advocated more study of problems, less talk of isms, scientific method solving China problems. Literary Revolution Eight Donts promoted vernacular/new punctuation/new poetry; study abroad/run journals/run schools/translate/compile history, gradual reform over radical revolution, tolerance over struggle. Though radicals called surrenderist, scientific method/academic freedom/tolerance became modern Chinese academic genes.",
        "steps": [
            "Step 1: Crossing River by Feeling Stones — Literary Revolution (1917): New Youth published Literary Reform Preliminary Discussion Eight Donts, promoted vernacular/new punctuation/new poetry, experimental attitude trial-error",
            "Step 2: Unity of Knowledge and Action — Returned from US (1910-1917): Columbia under Dewey studied experimentalism, returned ran New Youth/Endeavor Weekly/Independent Review, pen as gun",
            "Step 3: Natural Selection — Organizing National Heritage (1919-1930): bold hypothesis careful verification, scientific method organized Dream of Red Mansions/Water Margin/Shui Jing Zhu/Classical Studies/Philosophy History, established academic norms",
            "Step 4: Redundancy Backup — Tolerance and Freedom (1920s-1940s): I disagree with your view but defend to death your right to speak, advocated academic freedom/thought freedom/tolerance of dissent",
            "Step 5: Dormant Accumulation — Gradual Reform (1930s-1940s): opposed radical revolution/violent struggle, advocated more study problems less talk isms, education/law/system gradual social reform"
        ],
        "expected": [
            "Vernacular became national language standard, modern punctuation/new poetry/academic norms used today",
            "Experimentalism/academic freedom/tolerance became modern Chinese academic/public discourse genes",
            "Lessons: gradual reform appeared powerless in war/extreme times, later years in Taiwan academic influence faded"
        ],
        "case": "Literary Revolution (1917): Hu Shi Literary Reform Preliminary Discussion Eight Donts: no empty words/no abused allusions/no parallelism/no avoidance of vulgar chars/no rigid parallelism/no exhaustive citations/no avoidance of function words/no forced sorrow. With Chen Duxiu/Qian Xuantong/Liu Bannong/Zhou Zuoren/Lu Xun promoted vernacular. Organizing National Heritage (1920s): scientific/textual/evidential methods researched Dream of Red Mansions Evidence/Water Margin Investigation/Shui Jing Zhu Commentary/Chinese Philosophy History Outline, established bold hypothesis careful verification academic paradigm. Tolerance: 1920s opposed Down with Confucius Shop radicals, advocated tolerance/freedom/human rights, attacked by left as liberal surrenderist. Result: scientific method/academic norms/vernacular became modern academic cornerstone."
    },
    "H-LX-37": {
        "name": "Lu Xun: Cold Eyed Deconstruction Master",
        "description": "Cold stare/A-Q spirit/dissect national flaws/deconstruct tradition/essay combat/ideological enlightenment",
        "modes": [30, 31, 37, 28, 35],
        "reason": "Lu Xun cold stare at thousand accusers, bow head willing as child ox. Core mindset: supreme art of critical deconstruction — used A-Q spirit deconstruct national spiritual victory method, onlookers satirize numbness, Xianglin Sao expose feudal rites eating people, Madman Diary deconstruct rites eat people essence. Essays spear and dagger stab current ills, cold stare facing attacks unflinching. Deconstruction over construction, diagnosis over prescription, became modern Chinese critical spirit totem.",
        "steps": [
            "Step 1: Cognitive Bias Identification — Identify spiritual victory method: A-Q beaten son beats father, humiliated I am stronger than you, failure externalized, maintains fragile self-esteem",
            "Step 2: Framing Effect — Reframe eating people: Madman Diary open history no dates crooked every page writes benevolence righteousness between lines two words eat people",
            "Step 3: Unity of Knowledge and Action — Essays as weapons: cold stare at thousand accusers bow head willing as child ox, facing right-wing siege/leftist purge/authority pressure, insisted speak truth expose darkness",
            "Step 4: Natural Selection — Deconstruct national character: True Story of Ah Q/Xianglin Sao/Kong Yiji/Medicine/Village Opera series, systematically dissect national flaws: numb/self-deceit/servility/opportunism/apathy",
            "Step 5: Dormant Accumulation — Cold stare: facing KMT warrant/leftist purge/cultural siege, warrior dead before death why need posthumous fame, pen as gun fight to death"
        ],
        "expected": [
            "Call to Arms/Wandering/Wild Grass/Dawn Blossoms Plucked at Dusk/Weeds became modern literature classics",
            "A-Q spirit/spiritual victory method/onlookers/eat people became core concepts deconstructing national character",
            "Lessons: pure criticism lacks constructive solutions, late years ideologically co-opted, essays easily quoted out of context"
        ],
        "case": "Madman Diary (1918): China first vernacular novel, madman perspective deconstructed rites eat people: open history no dates crooked every page writes benevolence righteousness between lines two words eat people. True Story of Ah Q (1921): A-Q beaten son beats father, slapped by Zhao I am stronger than you, revolution won could not rebel then cannot rebel now, spiritual victory method became national flaw synonym. Essay battles: 1920s-1930s with Liang Shiqiu/Xu Zhimo/Cheng Fangwu/Lu Xun/Qu Qiubai etc, cold stare at thousand accusers bow head willing as child ox. Result: critical spirit became modern Chinese intellectuals totem."
    },
    "H-QXS-38": {
        "name": "Qian Xuesen: Systems Engineering Father of Large Systems View",
        "description": "Systems Engineering/Large Systems View/Missile Aerospace Systematization/Five Inventions/Knowledge Engineering/Thinking Science",
        "modes": [12, 22, 14, 29, 28],
        "reason": "Qian Xuesen Father of Systems Engineering. Core mindset: Large Systems View engineering implementation — returned from US Jet Propulsion Lab/JPL, built China missile/aerospace from zero. Proposed Systems Engineering five inventions (systems analysis/synthesis/optimization/decision/management), Large Systems View: engineering/management/social/natural/thinking five major categories. Built Knowledge Engineering, Thinking Science, advocated start from childhood cultivate innovative talents.",
        "steps": [
            "Step 1: Systems Thinking — Establish Systems Engineering discipline: introduced US systems engineering methodology, built Beijing Automation Inst/7th Machine Ministry/Aerospace 5th Academy, established model-system-total three-level management system",
            "Step 2: Center of Gravity — Focus Two Bombs One Satellite core: concentrated national superior resources on missiles/nuclear/satellites, concentrate strength on big things systemized advancement",
            "Step 3: Management by Objectives — Qian Xuesen Class cultivation: XJTU/NUDT established mechanics/control/systems cross-disciplinary experimental classes, start from childhood cultivate systems-type innovative talents",
            "Step 4: Feedback Loops — Knowledge Engineering/Thinking Science: built Knowledge Engineering processing unstructured knowledge, Thinking Science studying human brain/machine intelligence, foresaw AI era",
            "Step 5: Redundancy Backup — Systemic redundancy: missiles multiple models parallel/satellites multiple parallel/launch sites multiple bases/tracking multiple stations, key nodes multi-layer backup"
        ],
        "expected": [
            "Two Bombs One Satellite broke US/USSR blockade, established China strategic deterrence",
            "Built complete aerospace industry: 5th Academy/four launch sites/tracking network/TT&C",
            "Systems engineering methodology promoted to defense/economy/social/management, became national major project standard"
        ],
        "case": "Two Bombs One Satellite (1956-1970): Qian headed 5th Academy, built model-system-total three-level: Total Dept coordinated, System Inst divided labor, Model Inst tackled. Missiles: DF-1/2/3/4/5 generational breakthrough, sub-launched/land-based/mobile multi-platform. Nuclear: 596/H-bomb/miniaturized/missile warhead. Satellites: Dongfanghong-1/Practice/Fengyun/Dongfanghong-2. Built four launch sites (Jiuquan/Taiyuan/Xichang/Wenchang), tracking network/ocean tracking ships. Result: China 5th self-launch satellite nation, strategic deterrence established. Qian later promoted systems engineering to economy/management/social, created Qian Xuesen Class cultivating systems-type talents."
    },
    "H-RZF-39": {
        "name": "Ren Zhengfei: Survival-First Grey Zone Management Master",
        "description": "Survival first/Customer-centric/Huashan Duel/Grey management/No IPO/Employee ownership/Basic research 10%+",
        "modes": [36, 28, 23, 17, 35],
        "reason": "Ren Zhengfei no road to success, only endless progress. Core mindset: survival-first grey zone management art — survive is highest strategy, customer-centric sole value source, Huashan Duel internal competition eliminates mediocrity, grey management finds balance in contradictions (centralize/decentralize, standard/flexible, short/long term). No IPO/no dividends/employee ownership/basic research >10% revenue, program-controlled exchange -> telecom equipment -> handsets -> 5G -> HarmonyOS -> cloud -> digital power -> intelligent driving, each gen tech accumulation supports next.",
        "steps": [
            "Step 1: Dormant Accumulation — Early entrepreneurship (1987-1995): agented Chongqing Hongqi Instruments HJC exchange, accumulated first pot of gold/team/channels, not greedy/not blind expansion",
            "Step 2: Natural Selection — Product line competition (1996-2000): Huashan Duel GSM/exchange/handset multi-track parallel, market selects winners, eliminates mediocrity",
            "Step 3: Strategic Delegation — Customer-centric: IPD/LTC/IFS process transformation, introduced IBM/PwC consultants, customer needs drive R&D/delivery/service full cycle",
            "Step 4: Compound Diligence — Basic research >10% revenue: math/physics/materials/algorithms/chips/compilers/databases/OS full-stack self-developed",
            "Step 5: Three Yamen Division — No IPO/employee ownership/committee governance: Ren only 1% shares, veto/appointment rights, rotating CEO/four committees/board of supervisors checks balances, prevent single person/dept decision error"
        ],
        "expected": [
            "From agent to global telecom giant, 5G patents world 1, handset shipments once world 1",
            "Annual R&D >160B, basic research >10%, employee ownership attracts world-class talent",
            "Lessons: survival hard under sanctions, HarmonyOS ecosystem long road, management complexity scales exponentially"
        ],
        "case": "Huawei four phases: 1) Agent (1987-1995): agented HJC exchange, accumulated capital/team/channels. 2) Self-developed exchange (1996-2000): C&C08/10 broke foreign monopoly, rural market entry. 3) Global/Handset (2001-2010): IPD introduced, overseas breakthrough, handset terminal rose. 4) 5G/Full-stack (2011-): math/physics/materials/chips/compilers/databases/OS/cloud/intelligent driving full-stack self-developed, 5G patents world 1. Grey management: find balance in contradictions — centralize strategy/decentralize tactics, standard process/flexible innovation, short-term survival/long-term investment. No IPO avoids short-term capital pressure, employee ownership binds core talent. Result: Annual R&D 164.7B (2023), basic research >10%, world-class talent magnet."
    }
}

# Update files
scenarios_zh.update(new_zh)

with open('scenarios_zh.json', 'w', encoding='utf-8') as f:
    json.dump(scenarios_zh, f, ensure_ascii=False, indent=2)

with open('scenarios_en.json', 'w', encoding='utf-8') as f:
    json.dump({**scenarios_en, **new_en}, f, ensure_ascii=False, indent=2)

print(f"Done! ZH: {len(scenarios_zh)} EN: {len({**scenarios_en, **new_en})}")