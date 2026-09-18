import json

# Load existing scenarios
with open('scenarios_zh.json', 'r', encoding='utf-8') as f:
    scenarios_zh = json.load(f)

with open('scenarios_en.json', 'r', encoding='utf-8') as f:
    scenarios_en = json.load(f)

# Add 6 more high-value historical figures
new_scenarios_zh = {
    "H-WZ-27": {
        "name": "武则天：破门阀立科举的权力重构者",
        "description": "唯一女皇、废九品中正制改科举、酷吏治豪强、晚年禅位李显",
        "modes": [33, 34, 18, 28, 35],
        "reason": "武则天以女性身份在唐朝夺取皇权，核心思维：破旧立新的权力重构——废九品中正制建科举制打破门阀垄断、用酷吏(来俊臣/周兴)击碎关陇贵族、建立密告/制衡体系防权臣尾大、晚年主动禅位李显保唐祚延续。权力获取/行使/传递全链路设计。",
        "steps": [
            "第1步：格局授权——破除'女主内男主外'定势，废九品中正制建科举，唯才是举",
            "第2步：制度化制衡——设密告/酷吏/控鹤监制度，专治关陇贵族/权臣，防单一集团垄断",
            "第3步：目标管理法——'以官代政'考核官员实绩，殿最法奖惩分明，建立绩效导向官僚体系",
            "第4步：冗余备份法——武承嗣/武三思/狄仁杰/姚崇/宋璟多重人才梯队，防单一依赖",
            "第5步：蛰伏积势——晚年张柬之等五王政变，主动禅位李显，保唐祚、保武氏家族、保性命"
        ],
        "expected": [
            "科举制延用1300年，打破门阀垄断，平民上升通道打开",
            "唐朝中后期中兴(开元盛世)人才储备奠基",
            "教训：酷吏滥杀寒士、家族腐败、权力过度集中导致晚年政变"
        ],
        "case": "废九品中正立科举(655-690)：《周礼》设六科举人，武举/制举/算学等多元选拔。狄仁杰/姚崇/宋璟/张说皆科举出身。酷吏制衡贵族：来俊臣《罗织经》打击关陇集团，但滥杀无辜。晚年神龙政变(705)：张柬之/桓彦范等五王兵变，武则天病重被迫禅位李显(唐中宗)，唐祚复辟，武氏家族获保全。'周唐革命'虽失败，但科举/监察/制衡制度成唐宋基石。"
    },
    "H-YZ-28": {
        "name": "雍正：密折军机处的极致执行力",
        "description": "密折制度、摊丁入亩/火耗归公、军机处雏形、雍正八年高强度统治",
        "modes": [38, 40, 19, 28, 35],
        "reason": "雍正'九龙夺嫡'上位，核心思维：制度微创新的极致执行力——创密折制度直达基层绕过六部、摊丁入亩/火耗归公解决财政黑洞、军机处雏形实现'天下事天下人办'、雍正八年日批万言折、亲阅万卷书。以个人超高强度工作补偿制度不完善，但留下中央集权顶峰。",
        "steps": [
            "第1步：摸石头过河——密折制度试点：允许封疆大吏直接奏报，雍正亲批硃批，绕过六部/内阁信息失真",
            "第2步：渐进改革法——摊丁入亩(1724)：将人头税并入土地税，'以地为主'，减轻贫苦百姓负担，杜绝豪强隐匿人口",
            "第3步：制度化制衡——火耗归公(1725-1729)：将征收成本'火耗'纳入公项统一管理，禁止层层盘剥，年增财政收入百万两",
            "第4步：三衙分兵/权力制衡架构——军机处雏形(1729)：设军机大臣直隶皇帝，'天下事天下人办'，绕过内阁/六部，决策时效从月级降至日级",
            "第5步：蛰伏积势——雍正八年(1730-1735)日批万言折，亲阅万卷书，以个人极致勤勉维系庞大帝国运转"
        ],
        "expected": [
            "财政收入从3000万两增至6000万两，火耗归公成清代财政基石",
            "军机处成清代最高决策机构，延续至清亡",
            "教训：极度依赖皇帝个人勤勉，乾隆继位后懈怠导致制度退化；文字狱寒士气"
        ],
        "case": "密折制度(1723-1735)：雍正命田文镜/李卫/年羹尧等封疆大吏'有事即奏，毋拘时日'。雍正亲阅亲批，硃批万言，如'卿奏悉朕懂了'。军机处成立(1729)：因准噶尔噶尔丹策零用兵紧急，雍正在乾清宫西暖阁设军机处，张廷玉/鄂尔泰/鄂敏/蒋廷锡等轮值当值，'凡军国大事，皆于此议决'。摊丁入亩：全国丁银并入地亩银征收，'以地为主'，豪强无法隐匿人口。火耗归公：规定火耗归公项，按亩征收，解决'火耗无定额、层层盘剥'弊端。结果：雍正八年清朝达到中央集权巅峰。"
    },
    "H-ZZ-29": {
        "name": "左宗棠：区域军工体系的边疆治理者",
        "description": "湘军/新疆收复/福建船政/兰州织造/兰州机器局/台海防御",
        "modes": [4, 38, 23, 28, 35],
        "reason": "左宗棠'以儒生将相'，核心思维：区域军工体系的边疆治理者——湘军打太平天国/捻军/同治陕甘回变、收复新疆(左次东/右次西/中路三路并进)、创福建船政局/兰州织造局/兰州机器局/甘肃布政使司、设台海防御体系。'器物层面现代化+区域资源统筹+战略纵深经营'三位一体。",
        "steps": [
            "第1步：农村包围城市——湘军起家：'不招募流寇只招农夫读书人'，打太平天国/捻军/陕甘回变，建立'左家军'品牌",
            "第2步：摸石头过河——福建船政局(1866)：聘法籍工程师未尔/魏汉等，建船台/铸炮厂/绘图院/学堂，中国第一艘蒸汽军舰'万年清'下水",
            "第3步：自然选择法——收复新疆(1876-1877)：左次东(刘锦棠)/右次西(苏元春)/中路(金顺)三路并进，阿古伯逃亡，新疆建省设巡抚",
            "第4步：三衙分兵/权力制衡架构——兰州军工体系：兰州织造局(军需被服)/兰州机器局(军械修造)/兰州铸炮局/甘肃布政使司，军民融合自给自足",
            "第5步：冗余备份法——台海防御(1884-1885)：法军侵台，左督两江/闽浙，建金门/厦门/澎湖/基隆炮台，组招宝山海军，法军退守"
        ],
        "expected": [
            "新疆收复、建省设巡抚，版图完整保全",
            "福建船政/兰州军工成清代洋务运动标杆",
            "教训：器物现代化未触动制度根基，甲午海战船政舰队全军覆没"
        ],
        "case": "收复新疆(1876-1877)：左宗棠'先北后南、缓进急战'，筹饷1200万两(外债/关税/厘金/捐输)，刘锦棠北路速进、苏元春西路稳进、金顺中路策应。阿古伯部内讧逃亡，清军兵不血刃收复北疆、南疆。1884年新疆建省，左任首任巡抚。福建船政(1866-1894)：建成船台18座、铸炮厂/绘图院/学堂，造军舰40余艘(如'扬威'/'超勇'/'济安'/'飞云')，培养严复/萨镇冰/刘步蟾等海军人才。兰州机器局(1872)：仿造克虏伯炮、雷明顿枪、子弹/火药生产线，陕甘回变/新疆收复军需自给。"
    },
    "H-ZJ-30": {
        "name": "张謇：状元办实业的乡土建设先驱",
        "description": "状元办实业/大生纱厂/南通模式/教育救国/慈善/自治/红十字会",
        "modes": [38, 23, 18, 28, 35],
        "reason": "张謇'状元办实业'，核心思维：士绅转型实业家的乡土建设——大生纱厂(1895)中国第一家现代棉纺厂、南通模式'实业/教育/慈善/自治'四位一体、创办通州师范/纺织/农业/医学四专门学校、创中国第一个民办博物馆/图书馆/剧场、发起中国红十字会、推动南通乡村自治。'实业为本、教育为基、慈善为翼、自治为纲'四维共振。",
        "steps": [
            "第1步：摸石头过河——大生纱厂(1895)：变卖家产/筹集洋款/聘日籍技师/引进英国普拉特纺纱机，'官督商办'模式，首年即盈利",
            "第2步：自然选择法——'大生'生态圈：大生二厂/三厂/四厂、大生面粉/油脂/丝厂/机器/轮船/银行/商场，产业链闭环",
            "第3步：目标管理法——教育救国：通州师范(1902)中国第一所现代师范、纺织/农业/医学专门学校、启秀女子小学/女子师范、南通大学前身",
            "第4步：制度化制衡——慈善/自治：启秀慈善院(收养弃婴/鳏寡孤独)、通州红十字会(中国第一红十字)、南通县自治局(中国第一县级自治)、启秀公园/博物馆/图书馆/剧场",
            "第5步：蛰伏积势——'实业为本、教育为基、慈善为翼、自治为纲'，以实业利润反哺教育/慈善/自治，南通成'江海第一县'"
        ],
        "expected": [
            "大生纱厂运营至1956年公私合营，60年未倒闭，民营企业奇迹",
            "南通成中国近代化县域样板，教育/慈善/自治/实业四维领先",
            "教训: 依赖张謇个人威望/家族资源，后世缺乏制度化传承机制"
        ],
        "case": "大生纱厂(1895-1956)：张謇中状元后弃官办厂，筹银30万两，引进英国纺纱机1纺机，雇工2000人，首年利润8万两。后建二厂/三厂/四厂，配套面粉/油脂/丝厂/机器/轮船/银行/商场，产业链闭环。教育：通州师范(1902)中国第一现代师范，后建纺织/农业/医学专门，南通大学前身。慈善：启秀慈善院收养弃婴万余。自治：南通县自治局(1909)中国第一县级自治，张謇任自治局长。红十字：发起中国红十字会(1904)任副会长。南通模式:'实业为本、教育为基、慈善为翼、自治为纲'。"
    },
    "H-FL-31": {
        "name": "范蠡：三迁三散的财富周期大师",
        "description": "辅佐勾践卧薪尝胆/灭吴/功成身退/三次创业/三次散财/商圣",
        "modes": [35, 36, 23, 28, 33],
        "reason": "范蠡'商圣'，核心思维：财富周期律与身退隐的最高境界——辅佐勾践'卧薪尝胆'十年生聚十年教训灭吴、功成身退'鸟尽弓藏'改名赤松子游齐、二次创业致富再散财改名陶朱公游陶、三次创业于陶/楚再散财。'货贱伤农、货贵伤商、通其有无、使平其准'，掌握财富积累/保全/传承/放弃全周期。",
        "steps": [
            "第1步：蛰伏积势——卧薪尝胆(前494-前473)：范蠡/文种献'十年聚十年教训'策，勾践卧薪尝胆，范蠡主理国政/军需/外交，文种主军事",
            "第2步：全胜思维——灭吴(前473)：范蠡'以逸待劳/水战为主'策，越军水陆并进，吴王夫差自杀，越复国",
            "第3步：格局授权——功成身退(前473)：范蠡'鸟尽弓藏、良犬烹'觉悟，献平吴策书予文种，携家财改名赤松子游齐，文种果被烹",
            "第4步：自然选择法——三迁三散：齐国相三年散财去陶→陶朱公致富散财去楚→楚相三月散财隐居。每次'致富→散财→隐退'完美闭环",
            "第5步：多元思维模型——商圣理论：'货贱伤农、货贵伤商、通其有无、使平其准'，逆周期操作、薄利多销、诚信立本、知进退"
        ],
        "expected": [
            "辅佐勾践灭吴成霸业，功成身退保全性命家族",
            "三次创业三次散财，每次都能在新环境从零致富",
            "《陶朱公书》/《范子计然》成中国商业智慧经典，影响胡雪岩/荣毅仁/马云"
        ],
        "case": "卧薪尝胆灭吴(前494-前473)：越王勾践会稽之耻，范蠡献'十年生聚十年教训'策。范蠡主理国政：劝农桑/修兵甲/积粮草/选将练兵/修好邻国/间谍渗透。文种主军事：卧薪尝胆/苦练水军。越军水陆并进，吴王夫差北伐齐国后方空虚，越军乘虚入吴，夫差自杀。范蠡献《平吴策》予文种，劝文种退避不听被烹。范蠡携家财改名游齐→陶→楚，三次致富三次散财。商圣理论影响胡雪岩'红顶商人'、荣毅仁'红色资本家'、马云'让天下没有难做的生意'。"
    },
    "H-GZ-32": {
        "name": "郭子仪：九朝元老的危机收拾大师",
        "description": "安史之乱收复两京/朔方军/回纥单骑见可汗/九朝元老/家族百年传承",
        "modes": [35, 6, 28, 33, 36],
        "reason": "郭子仪'汾阳王'，核心思维：危机收拾与多朝生存的最高艺术——安史之乱率朔方军收复长安/洛阳、单骑见回纥可汗化敌为友、历事玄宗/肃宗/代宗/德宗/顺宗/宪宗/穆宗/敬宗/文宗九朝、'令仪门庆、子孙满堂'家族百年传承。'大节不夺、细行不矜'，在权力更迭/军阀割据/外敌入侵中始终掌握军权且保全性命家族。",
        "steps": [
            "第1步：蛰伏积势——朔方军建设(740s)：郭子仪任朔方节度使，招募降户/突厥/党项杂胡，建'朔方军'精锐十万，屯田/练兵/修堡垒",
            "第2步：运动歼灭法——收复两京(757/759)：安史之乱，郭子仪/李光弼联合，先收长安(757)，后收洛阳(757)，史朝义败亡，唐祚中兴",
            "第3步：统一战线法——单骑见回纥(765)：回纥/吐蕃十万围奉天，郭子仪单骑出城见回纥可汗，以'大唐天子之臣'义气感化，回纥回师助唐击吐蕃",
            "第4步：格局授权——九朝元老：历玄/肃/代/德/顺/宪/穆/敬/文九帝，官至尚书令/太尉/中书令/汾阳王，'大节不夺、细行不矜'，权倾天下而不失君心",
            "第5步：笨功夫/死磕到底——家族传承：八子七婿皆显贵，孙郭奕/曾孙郭承嘏等科第相继，家族百年'令仪门庆'，成唐代第一望族"
        ],
        "expected": [
            "安史之乱收复两京，唐祚延续150年",
            "单骑见回纥化解十万大军围城，外交/军事/心理三级胜利",
            "家族百年显贵，子孙科第相继，成唐代第一望族",
            "教训：过度依赖个人威望/君主信任，制度化薄弱，德宗猜忌晚年罢兵权"
        ],
        "case": "安史之乱收复两京(757-759)：安禄山反，郭子仪/李光弼守朔方，防安史南下。肃宗即位灵武，郭任元帅联合李光弼/回纥/吐谷浑等十万大军。首收长安(757)：安庆绪弃长安逃洛阳，郭入长安迎肃宗还京。再收洛阳(759)：史朝义固守洛阳，郭/李合围，回纥叶护仆固怀恩助战，史朝义自杀河北。单骑见回纥(765)：吐蕃/回纥十万围奉天(乾陵)，郭子仪单骑数十骑出城见回纥叶护，以'汝背约负义'义正词严，回纥感动回师助击吐蕃。九朝元老：玄宗避蜀、肃宗灵武、代宗广德、德宗建中、顺宗永贞、宪宗元和、穆宗长庆、敬宗宝历、文宗太和，郭子仪始终掌兵权、保性命、全家族。"
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
    "H-WZ-27": {
        "name": "Wu Zetian: Power Restructurer Who Broke Aristocracy with Imperial Exams",
        "description": "Only female emperor, abolished nine-rank system for exams, cruel officials vs aristocrats, late abdication",
        "modes": [33, 34, 18, 28, 35],
        "reason": "Wu Zetian seized imperial power as a woman in Tang. Core mindset: power restructuring by breaking old and establishing new — abolished nine-rank system to create imperial exams breaking aristocratic monopoly, used cruel officials (Lai Junchen/Zhou Xing) to crush Guanlong aristocracy, established informant/checks system to prevent ministerial overreach, late in life abdicated to Li Xian preserving Tang dynasty. Full chain design of power acquisition/exercise/transfer.",
        "steps": [
            "Step 1: Strategic Delegation — Broke 'female inside male outside' dogma, abolished nine-rank for exams, merit-only",
            "Step 2: Institutional Checks — Informant/cruel official/Control Crane Monitor systems, targeted Guanlong aristocracy/ministers, prevented single group monopoly",
            "Step 3: Management by Objectives — 'Official substitution for politics' performance appraisal, rewards/punishments clear, built performance-oriented bureaucracy",
            "Step 4: Redundancy Backup — Wu Chengsi/Wu Sansi/Di Renjie/Yao Chong/Song Jing multi-layer talent pipeline, no single dependency",
            "Step 5: Dormant Accumulation — Late Zhang Jianzhi five-king coup, voluntarily abdicated to Li Xian, preserved Tang, Wu clan, own life"
        ],
        "expected": [
            "Imperial exams lasted 1300 years, broke aristocratic monopoly, opened commoner mobility",
            "Talent reserve for Tang mid-late revival (Kaiyuan Prosperity) established",
            "Lessons: cruel officials killed innocents, clan corruption, over-centralization led to late coup"
        ],
        "case": "Abolished nine-rank for exams (655-690): Created six exam categories per 'Rites of Zhou', military/legal/math exams diverse selection. Di Renjie/Yao Chong/Song Jing/Zhang Yue all exam graduates. Cruel officials vs aristocrats: Lai Junchen 'Raozhi Jing' crushed Guanlong clique but killed innocents. Late Shenlong Coup (705): Zhang Jianzhi/Huan Yanfan five kings mutiny, Wu Zetian ill forced abdicate to Li Xian (Tang Zhongzong), Tang restored, Wu clan preserved. 'Zhou-Tang Revolution' failed but exams/supervision/checks systems became Tang-Song foundation."
    },
    "H-YZ-28": {
        "name": "Yongzheng: Extreme Execution via Secret Memorials & Grand Council",
        "description": "Secret memorial system, head tax into land tax, fire loss归公, Grand Council embryo, 8 years high-intensity rule",
        "modes": [38, 40, 19, 28, 35],
        "reason": "Yongzheng won 'Nine Dragons succession'. Core mindset: extreme execution via institutional micro-innovation — created secret memorial system reaching grassroots bypassing Six Ministries, head tax into land tax / fire loss归公 solved fiscal black holes, Grand Council embryo achieved 'empire affairs by empire people', 8 years daily reviewing ten-thousand-word memorials. Compensated institutional imperfection with personal ultra-high-intensity work, but left peak of centralization.",
        "steps": [
            "Step 1: Crossing River by Feeling Stones — Secret memorial pilot: allowed governors direct memorial, Yongzheng personal vermilion review, bypassed Six Ministries/Grand Secretariat info distortion",
            "Step 2: Gradual Reform — Head tax into land tax (1724): merged poll tax into land tax, 'land as basis', reduced poor burden, prevented gentry hiding population",
            "Step 3: Institutional Checks — Fire loss归公 (1725-1729): collection costs 'fire loss' into public items unified management, banned layer-by-layer exploitation, annual fiscal increase million taels",
            "Step 4: Three Yamen Division — Grand Council embryo (1729): Grand Council ministers direct to emperor, 'empire affairs by empire people', bypassed Grand Secretariat/Six Ministries, decision latency from monthly to daily",
            "Step 5: Dormant Accumulation — 8 years (1730-1735) daily reviewing ten-thousand-word memorials, personally reading ten-thousand volumes, maintained massive empire by personal ultra-diligence"
        ],
        "expected": [
            "Fiscal revenue 30M to 60M taels, fire loss归公 became Qing fiscal cornerstone",
            "Grand Council became Qing supreme decision body, lasted till dynasty end",
            "Lessons: extreme reliance on emperor personal diligence, Qianlong succession led to slack and system decay; literary inquisition chilled scholars"
        ],
        "case": "Secret memorials (1723-1735): Yongzheng ordered Tian Wenjing/Li Wei/Nian Gengyao 'memorial anytime, no time restriction'. Yongzheng personal review, vermilion comments ten-thousand words. Grand Council (1729): Dzungar Galdan Tsering emergency, Yongzheng in Qianqing Palace west warm pavilion set Grand Council, Zhang Tingyu/E'ertai/E Min/Jiang Tingxi rotated duty, 'all imperial affairs decided here'. Head tax into land tax: national poll tax merged into land tax, 'land as basis', gentry couldn't hide population. Fire loss归公: standardized fire loss into public items, per mu collection, solved 'fire loss no standard, layer exploitation'. Result: 8 years Qing reached centralization peak."
    },
    "H-ZZ-29": {
        "name": "Zuo Zongtang: Regional Military-Industrial System for Frontier Governance",
        "description": "Xiang Army/Xinjiang recovery/Fuzhou Shipyard/Lanzhou Textile/Lanzhou Arsenal/Taiwan defense",
        "modes": [4, 38, 23, 28, 35],
        "reason": "Zuo Zongtang 'Confucian general-minister'. Core mindset: regional military-industrial system for frontier governance — Xiang Army vs Taiping/Nian/Shensi-Gansu Hui revolt, recovered Xinjiang (three-pronged), created Fuzhou Shipyard/Lanzhou Textile/Lanzhou Arsenal/Gansu Administration. 'Hardware modernization + regional resource integration + strategic depth management' trinity.",
        "steps": [
            "Step 1: Encircle Cities from Countryside — Xiang Army origin: 'recruit only farmer-scholars not bandits', vs Taiping/Nian/Hui revolt, built 'Zuo Family Army' brand",
            "Step 2: Crossing River by Feeling Stones — Fuzhou Shipyard (1866): hired French engineers Verney/Wei Han, built slipways/foundry/drawing academy/school, China's first steam warship 'Wannianqing' launched",
            "Step 3: Natural Selection — Xinjiang recovery (1876-1877): Eastern route (Liu Jintang)/Western route (Su Yuanchun)/Central route (Jin Shun) three-pronged, Agubo fled, Xinjiang province established",
            "Step 4: Three Yamen Division — Lanzhou military-industrial: Lanzhou Textile (military clothing)/Lanzhou Arsenal (arms repair)/Lanzhou Cannon Foundry/Gansu Administration, civil-military fusion self-sufficient",
            "Step 5: Redundancy Backup — Taiwan defense (1884-1885): French invasion, Zuo supervised Liangjiang/Fujian-Zhejiang, built Kinmen/Xiamen/Penghu/Keelung batteries, organized Zhaobaoshan navy, French withdrew"
        ],
        "expected": [
            "Xinjiang recovered, province established, territorial integrity preserved",
            "Fuzhou Shipyard/Lanzhou military-industrial became Self-Strengthening benchmarks",
            "Lessons: hardware modernization without institutional root caused Shipyard fleet annihilation in Sino-Japanese War"
        ],
        "case": "Xinjiang recovery (1876-1877): Zuo 'north first south south, slow advance quick fight', raised 12M taels (foreign loan/customs/lijin/donations). Liu Jintang eastern route speed, Su Yuanchun western route steady, Jin Shun central coordination. Agubo faction fled, Qing troops bloodless recovery north/south Xinjiang. 1884 Xinjiang province, Zuo first governor. Fuzhou Shipyard (1866-1894): 18 slipways, foundry/drawing academy/school, built 40+ warships (Yangwei/Chaoyong/Jian'an/Feyun), trained Yan Fu/Sa Zhenbing/Liu Buchan. Lanzhou Arsenal (1872): copied Krupp cannon/Remington rifle, bullet/powder lines, supplied Hui revolt/Xinjiang campaigns."
    },
    "H-ZJ-30": {
        "name": "Zhang Jian: Scholar-Turned-Industrialist & Rural Reconstruction Pioneer",
        "description": "Jinshi turned industrialist / Dasheng Cotton Mill / Nantong Model / Education salvation / Charity / Self-governance / Red Cross",
        "modes": [38, 23, 18, 28, 35],
        "reason": "Zhang Jian 'Jinshi turned industrialist'. Core mindset: gentry-to-industrialist rural reconstruction — Dasheng Cotton Mill (1895) China's first modern cotton mill, Nantong Model 'Industry/Education/Charity/Self-governance' quad, founded Tongzhou Normal/Textile/Agriculture/Medical four specialized schools, China's first private museum/library/theater, initiated China Red Cross, promoted Nantong rural self-governance. 'Industry as root, Education as base, Charity as wing, Self-governance as discipline' four-dimensional resonance.",
        "steps": [
            "Step 1: Crossing River by Feeling Stones — Dasheng Cotton Mill (1895): sold family assets/raised foreign capital/hired Japanese technicians/imported British Platt frames, 'official supervision merchant management' model, profitable year one",
            "Step 2: Natural Selection — Dasheng ecosystem: Mill 2/3/4, Dasheng Flour/Oil/Silk/Machinery/Shipping/Bank/Commerce, vertical integration closed loop",
            "Step 3: Management by Objectives — Education salvation: Tongzhou Normal (1902) China's first modern normal, Textile/Agriculture/Medical specialized, Qixiu Girls Primary/Normal, Nantong University predecessor",
            "Step 4: Institutional Checks — Charity/Self-governance: Qixiu Charity Home (abandoned infants/widowed), Tongzhou Red Cross (China's first), Nantong County Self-governance (China's first county-level), Qixiu Park/Museum/Library/Theater",
            "Step 5: Dormant Accumulation — 'Industry root, Education base, Charity wing, Self-governance discipline', industrial profits reinvested into education/charity/self-governance, Nantong became 'first county of Jianghai'"
        ],
        "expected": [
            "Dasheng Cotton Mill operated till 1956 public-private merger, 60 years never failed, private enterprise miracle",
            "Nantong became China's modern county benchmark, education/charity/self-governance/industry four-dimensional leadership",
            "Lessons: relied on Zhang Jian personal prestige/family resources, later lacked institutionalized succession mechanism"
        ],
        "case": "Dasheng Cotton Mill (1895-1956): Zhang Jian top scholar abandoned office for factory, raised 300k taels, imported British spinning frames, 2000 workers, first year profit 80k taels. Later Mill 2/3/4, supporting Flour/Oil/Silk/Machinery/Shipping/Bank/Commerce, vertical integration. Education: Tongzhou Normal (1902) China's first modern normal, later Textile/Agriculture/Medical, Nantong University predecessor. Charity: Qixiu Charity Home adopted 10k+ abandoned infants. Self-governance: Nantong County Self-governance (1909) China's first county-level, Zhang served head. Red Cross: initiated China Red Cross (1904) VP. Nantong Model: 'Industry root, Education base, Charity wing, Self-governance discipline'."
    },
    "H-FL-31": {
        "name": "Fan Li: Three Migrations Three Distributions Wealth Cycle Master",
        "description": "Assisted Goujian sleeping on firewood tasting gall / destroyed Wu / success then retired / three ventures / three distributions / Merchant Sage",
        "modes": [35, 36, 23, 28, 33],
        "reason": "Fan Li 'Merchant Sage'. Core mindset: wealth cycle law & supreme art of retirement — assisted Goujian 'sleeping on firewood tasting gall' ten years accumulation ten years instruction destroyed Wu, success then retired 'birds gone bow hidden' renamed Chisongzi to Qi, second venture wealthy then distributed renamed Tao Zhu Gong in Tao, third venture in Tao/Chu then distributed. 'Cheap grain hurts farmers, dear grain hurts merchants, connect surplus deficit, make level' mastered full cycle of wealth accumulation/preservation/inheritance/renunciation.",
        "steps": [
            "Step 1: Dormant Accumulation — Sleeping on firewood tasting gall (494-473 BC): Fan Li/Wen Zhong proposed 'ten years accumulate ten years instruct', Goujian slept on firewood tasted gall, Fan Li managed state affairs/military logistics/diplomacy, Wen Zhong military",
            "Step 2: Total Victory Mindset — Destroyed Wu (473 BC): Fan Li 'rested await labor / naval warfare main' strategy, Yue naval/land combined, Wu King Fucha suicide, Yue restored",
            "Step 3: Strategic Delegation — Success then retired (473 BC): Fan Li 'birds gone bow hidden, good dog cooked' realization, submitted 'Pacify Wu Strategy' to Wen Zhong, took family wealth renamed Chisongzi to Qi, Wen Zhong refused retreat and was cooked",
            "Step 4: Natural Selection — Three migrations three distributions: Qi prime minister three years distributed wealth to Tao -> Tao Zhu Gong wealthy distributed to Chu -> Chu prime minister three months distributed and hidden. Each 'enrich -> distribute -> retire' perfect loop",
            "Step 5: Mental Models — Merchant Sage theory: 'Cheap grain hurts farmers, dear grain hurts merchants, connect surplus deficit, make level', counter-cyclical operation, thin margin high volume, integrity foundation, know advance retreat"
        ],
        "expected": [
            "Assisted Goujian destroyed Wu achieved hegemony, success retired preserved life family",
            "Three ventures three distributions, each time zero-to-wealth in new environment",
            "'Tao Zhu Gong Shu'/'Fan Zi Jiran' became Chinese commercial wisdom classics, influenced Hu Xueyan/Hong Yiren/Ma Yun"
        ],
        "case": "Sleeping on firewood tasting gall destroyed Wu (494-473 BC): Goujian Kuaiji humiliation, Fan Li proposed 'ten years accumulate ten years instruct'. Fan Li managed state: encouraged agriculture/repaired weapons/stored grain/selected generals trained/improved neighbor relations/spy infiltration. Wen Zhong military: slept on firewood tasted gall/hard trained navy. Yue naval/land combined, Fucha north expedition Qi left rear empty, Yue exploited vacuum entered Wu, Fucha suicide. Fan Li submitted 'Pacify Wu Strategy' to Wen Zhong, urged Wen Zhong retire not listened got cooked. Fan Li took family wealth renamed to Qi->Tao->Chu, three enrichments three distributions. Merchant Sage theory influenced Hu Xueyan 'Red-top Merchant'/Rong Yiren 'Red Capitalist'/Ma Yun 'make business easy everywhere'."
    },
    "H-GZ-32": {
        "name": "Guo Ziyi: Nine-Dynasty Elder & Crisis Recovery Master",
        "description": "An-Shi Rebellion recovered two capitals / Shuofang Army / Uyghur single-horse met Khagan / Nine-dynasty elder / Family century legacy",
        "modes": [35, 6, 28, 33, 36],
        "reason": "Guo Ziyi 'Fenyang King'. Core mindset: crisis recovery & multi-dynasty survival supreme art — An-Shi Rebellion led Shuofang Army recovered Chang'an/Luoyang, single-horse met Uyghur Khagan turned enemy to friend, served Xuan/Sui/Dai/De/Shun/Xian/Mu/Jing/Wen nine emperors, 'family celebrations, descendants full halls' century family legacy. 'Great integrity uncompromised, minor conduct not boasted', always held military power and preserved life family amid power transitions/warlord separatism/foreign invasions.",
        "steps": [
            "Step 1: Dormant Accumulation — Shuofang Army build (740s): Guo Ziyi as Shuofang Jiedushi, recruited surrender households/Turkic/Party Qiang mixed tribes, built 'Shuofang Army' elite 100k, tuntian/training/fortresses",
            "Step 2: Mobile Warfare — Recovered two capitals (757/759): An-Shi Rebellion, Guo Ziyi/Li Guangbi united, first took Chang'an (757), then Luoyang (757), Shi Chaoyi defeated, Tang restored",
            "Step 3: United Front — Single-horse met Uyghur (765): Uyghur/Tibet 100k besieged Fengtian, Guo Ziyi single-horse out met Uyghur Khagan, as 'Great Tang subject' righteousness moved, Uyghur returned helped Tang hit Tibet",
            "Step 4: Strategic Delegation — Nine-dynasty elder: through Xuan/Sui/Dai/De/Shun/Xian/Mu/Jing/Wen nine emperors, offices Shangshu Ling/Tawei/Zhongshu Ling/Fenyang King, 'great integrity uncompromised, minor conduct not boasted', power tilted heaven yet kept emperor trust",
            "Step 5: Compound Diligence — Family legacy: eight sons seven sons-in-law all prominent, grandson Guo Yi/great-grandson Guo Chengyi etc. imperial exams successive, family century 'family gates celebrating', became Tang first prestigious clan"
        ],
        "expected": [
            "An-Shi Rebellion recovered two capitals, Tang extended 150 years",
            "Single-horse met Uyghur resolved 100k siege, diplomacy/military/psychology triple victory",
            "Family century prominent, descendants imperial exams successive, became Tang first prestigious clan",
            "Lessons: over-reliance on personal prestige/emperor trust, weak institutionalization, Dezong suspicion late years stripped command"
        ],
        "case": "An-Shi Rebellion recovered two capitals (757-759): An Lushan rebelled, Guo Ziyi/Li Guangbi held Shuofang preventing An Shi south. Suzong enthroned Lingwu, Guo commander-in-chief united Li Guangbi/Uyghur/Tuyuhun etc 100k. First took Chang'an (757): An Qingxu abandoned Chang'an fled Luoyang, Guo entered Chang'an welcomed Suzong back. Then took Luoyang (759): Shi Chaoyi held Luoyang, Guo/Li besieged, Uyghur Yehu Pugu Huai'en assisted, Shi Chaoyi suicide Hebei. Single-horse met Uyghur (765): Tibet/Uyghur 100k besieged Fengtian (Qianling), Guo Ziyi single-horse dozens cavalry out met Uyghur Yehu, 'you violated treaty betrayed righteousness' righteous words, Uyghur moved returned helped hit Tibet. Nine-dynasty elder: Xuan fled Shu, Suzong Lingwu, Dai Guangde, De Jianzhong, Shun Yongzhen, Xian Yuanhe, Mu Changqing, Jing Baoli, Wen Taihe, Guo Ziyi always held military power, kept life, preserved family."
    }
}

# Add to English scenarios
scenarios_en.update(new_scenarios_en)

with open('scenarios_en.json', 'w', encoding='utf-8') as f:
    json.dump(scenarios_en, f, ensure_ascii=False, indent=2)

print(f"Updated scenarios_en.json: {len(scenarios_en)} total scenarios")