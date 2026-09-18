import json

# Load existing scenarios
with open('scenarios_zh.json', 'r', encoding='utf-8') as f:
    scenarios_zh = json.load(f)

with open('scenarios_en.json', 'r', encoding='utf-8') as f:
    scenarios_en = json.load(f)

# Add 3 missing historical figures
new_scenarios_zh = {
    "H-LY-18": {
        "name": "刘裕：寄奴北伐的实干兴邦",
        "description": "布衣起家、两次北伐、收复中原、元嘉之治基石",
        "modes": [4, 11, 23, 28, 16],
        "reason": "刘裕出身微贱（小名寄奴），以'实干兴邦'著称。两次北伐收复洛阳长安，虽最终因子孙无力守成而失地，但其'识时务、敢决断、重后勤、建制度'的思维模式，是资源极度匮乏条件下创业成功的典范。",
        "steps": [
            "第1步：农村包围城市——从刘牢之部下起家，积累军事资本，不贪大求全",
            "第2步：自然选择法——北伐南燕、后秦，试错验证，保留适合的战法（水陆并进）",
            "第3步：灵活策略法——刘穆之掌后方粮草，刘裕专心前线指挥，文武分工极致",
            "第4步：冗余备份法——北伐前预置粮草、船只、马匹，建立多路补给线，关键节点有Plan B",
            "第5步：游击战十六字诀——面对强敌慕容超、姚泓，避实击虚，诱敌深入再集中歼灭"
        ],
        "expected": [
            "两次北伐分别耗时3个月、6个月，以少胜多收复黄河以南",
            "建立'刘穆之治内、刘裕治外'的文武双全治理模式",
            "为元嘉之治（子刘义隆在位）积累了制度、人才、财富基础"
        ],
        "case": "刘裕北伐南燕（409-410）：南燕慕容德占青徐，刘裕水陆并进，刘穆之'转漕万计'解决后勤。慕容超骄傲轻敌，刘裕诱敌出城野战歼灭，攻广固城用土山、楼车、地道多重手段，3个月灭南燕。北伐后秦（416-417）：分三路，水军顺流直捣长安，姚泓束手就擒。虽因长子刘义符无能、刘义真守长安失策，终丢失洛阳长安，但'元嘉之治'仍建立在其遗产上。"
    },
    "H-ZG-19": {
        "name": "赵构：苟且偏安的权力平衡术",
        "description": "御驾亲征vs绍兴和议、杀岳飞保皇权、南宋延续153年",
        "modes": [20, 31, 11, 28, 35],
        "reason": "赵构面临'金军强、主战派强、皇权弱'三重困境。其核心思维是'权力平衡术'：用博弈论在主战/主和、武将/文臣、皇权/相权之间动态平衡。虽被千古骂为'苟且偏安'，但南宋延续153年、最终被蒙古而非金灭亡，说明其战略底线守住了。",
        "steps": [
            "第1步：博弈论思维——分析金/主战派/秦桧/皇权四方博弈矩阵，找到纳什均衡：杀岳飞换和议",
            "第2步：框架效应法——将'割地称臣'重构为'岁币换和平、保宗庙社稷'，降低决策心理成本",
            "第3步：灵活策略法——早期亲征督战（建康/临安），中期借秦桧制衡韩世忠等大将，晚期废秦桧防相权过重",
            "第4步：冗余备份法——建立御营、江上、四川三大军事体系，防单一将领尾大不掉",
            "第5步：蛰伏积势思维——绍兴和议后30年'偏安一隅'，实则积蓄国力、完善海防、等待北方乱世"
        ],
        "expected": [
            "皇权稳固：文臣武将皆不敢越雷池一步",
            "财政可持续：岁币仅占财政收入5%左右，换取80年和平",
            "延续153年：比北宋更久，最终由蒙古灭亡而非金"
        ],
        "case": "绍兴和议（1141）：岳飞北伐收复郑州/洛阳，金主亮求和附加条件'必杀岳飞'。赵构手札密旨十二道召岳飞回，秦桧以'莫须有'弑岳于风波亭。和议内容：宋称臣、纳岁币25万两、界淮河大散关。赵构同时解除韩世忠/张俊兵权，三大将'杯酒释兵权'。结果：南宋获得80年休养生息，海防经营（刘锜/李宝）为后来抗蒙奠基。"
    },
    "H-YS-20": {
        "name": "袁世凯：北洋体系的现代化困局",
        "description": "小站练兵、废科举兴学堂、洪宪帝制133天、北洋分裂",
        "modes": [38, 8, 34, 40, 23],
        "reason": "袁世凯是'旧官僚做新军事、旧权谋搞新现代化'的悲剧人物。其核心矛盾：用传统权谋（制衡/收买/称帝）驾驭现代化组织（北洋新军/铁路/电报/新式教育），最终导致体制内部分裂、外部革命党联合、帝制梦碎。教训：现代化组织需要现代化治理，权谋不能替代制度。",
        "steps": [
            "第1步：摸石头过河/实验主义——小站练兵（1895）模仿德制，聘德籍教官，建立中国第一支现代化新军",
            "第2步：渐进改革法——废科举（1905）兴学堂，派留学生，设法部/学部，推动法制/教育现代化",
            "第3步：制度化制衡/杯酒释兵权——北洋六镇'镇统制'制，文官监军，轮换防区，防将领尾大不掉",
            "第4步：三衙分兵/权力制衡架构——军政/军令/参谋三分离（仿日德制），但大总统统帅权独揽，形成'权力倒金字塔'",
            "第5步：自然选择法——洪宪帝制（1915-1916）作为'终极实验'，市场反应剧烈（护国战争/退出国联/北洋分裂），133天终止"
        ],
        "expected": [
            "军事现代化：北洋新军成辛亥革命/早期抗战中坚",
            "制度遗产：法制/教育/财政/工业体系雏形",
            "悲剧结局：称帝破坏共和合法性，北洋军阀分裂祸乱中国20年"
        ],
        "case": "小站练兵→北洋六镇（1895-1911）：袁世凯在天津小站仿德制练兵，聘德教官，建'营/连/排/班'编制，设军需/军法/军医处。1901-1904扩编六镇（镇=师），每镇1.2万人，装备德式毛瑟枪/克虏伯炮。辛亥革命时北洋军战力碾压革命军，迫清廷退位。但袁世凯依靠'人治制衡'（提拔亲信/联姻/分封督军）而非'制度制衡'，称帝后冯国璋/段祺瑞/曹锟等镇统制纷纷倒戈，北洋分裂为直/皖/奉系，军阀混战20年。"
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
    "H-LY-18": {
        "name": "Liu Yu: Pragmatic State-Building of a Self-Made Emperor",
        "description": "Rose from cloth-clad origins, two northern expeditions, recovered Central Plains, foundation of Yuanjia Prosperity",
        "modes": [4, 11, 23, 28, 16],
        "reason": "Liu Yu rose from humble origins (childhood name 'Jinu' - entrusted slave), known for 'pragmatic state-building'. Two northern expeditions recovered Luoyang and Chang'an. Though descendants lost the gains, his mindset of 'reading the situation, daring to decide, prioritizing logistics, building systems' is a paradigm of entrepreneurial success under extreme resource constraints.",
        "steps": [
            "Step 1: Encircle Cities from Countryside — Started under Liu Laozhi, accumulated military capital, no overreach",
            "Step 2: Natural Selection — Northern expeditions vs Southern Yan/Later Qin, trial and error, retained what worked (amphibious warfare)",
            "Step 3: Flexible Strategy — Liu Muji managed rear logistics, Liu Yu focused on front command, ultimate civil-military division",
            "Step 4: Redundancy Backup — Pre-positioned grain/ships/horses before expeditions, established multiple supply lines, Plan B at key nodes",
            "Step 5: Guerrilla 16-Character Tactics — Against strong foes Murong Chao/Yao Hong, avoided strength, lured deep, concentrated annihilation"
        ],
        "expected": [
            "Two expeditions took 3 and 6 months respectively, recovered Yellow River south with fewer troops",
            "Established 'Liu Muji governs interior, Liu Yu commands exterior' dual-track governance model",
            "Laid institutional/talent/wealth foundation for Yuanjia Prosperity (son Liu Yilong's reign)"
        ],
        "case": "Northern Expedition vs Southern Yan (409-410): Murong De occupied Qing/Xu. Liu Yu amphibious advance, Liu Muji 'transported ten thousand hu'. Murong Chao arrogant, Liu Yu lured into field battle annihilation, besieged Guanggu with earth mounds/siege towers/tunnels, destroyed in 3 months. vs Later Qin (416-417): Three-pronged, navy sailed straight to Chang'an, Yao Hong surrendered. Though lost Luoyang/Chang'an later due to incompetent sons, Yuanjia Prosperity still built on his legacy."
    },
    "H-ZG-19": {
        "name": "Zhao Gou: The Art of Power Balance in Compromised Survival",
        "description": "Personal campaign vs Shaoxing Treaty, killed Yue Fei to secure throne, Southern Song lasted 153 years",
        "modes": [20, 31, 11, 28, 35],
        "reason": "Zhao Gou faced triple dilemma: strong Jin, strong pro-war faction, weak imperial power. Core mindset: 'power balance art' — used game theory to dynamically balance pro-war/pro-peace, generals/civilians, imperial/ministerial power. Though cursed as 'ignoble compromise', Southern Song lasted 153 years and fell to Mongols not Jin, proving strategic bottom line held.",
        "steps": [
            "Step 1: Game Theory — Analyzed 4-player matrix (Jin/pro-war/Qin Hui/imperial), found Nash equilibrium: kill Yue Fei for treaty",
            "Step 2: Framing Effect — Reframed 'cede land/submit' as 'annual tribute for peace, save ancestral temples', lowered psychological cost",
            "Step 3: Flexible Strategy — Early personal campaign (Jiankang/Lin'an), mid used Qin Hui to check Han Shizhong et al, late purged Qin Hui to prevent ministerial overreach",
            "Step 4: Redundancy Backup — Established three military systems (Imperial/Jiangshang/Sichuan), prevented single warlord tail-wagging",
            "Step 5: Dormant Accumulation — 30 years 'partial peace' post-Shaoxing, actually accumulated strength, built naval defense, waited for northern chaos"
        ],
        "expected": [
            "Imperial power secured: no civilian/general dared cross line",
            "Fiscal sustainable: tribute ~5% of revenue, bought 80 years peace",
            "Lasted 153 years: longer than Northern Song, fell to Mongols not Jin"
        ],
        "case": "Shaoxing Treaty (1141): Yue Fei recovered Zhengzhou/Luoyang, Jin Emperor Liangzuo demanded 'must kill Yue Fei'. Zhao Gou issued 12 hand-edicts recalling Yue, Qin Hui executed him at Fengbo Pavilion on 'trumped-up charges'. Treaty: Song as vassal, 250k taels annual tribute, boundary Huai/Dasan Pass. Zhao Gou simultaneously stripped Han Shizhong/Zhang Jun of commands — three generals 'cup of wine releasing military power'. Result: 80 years recuperation, naval defense (Liu Qi/Li Bao) laid foundation for later Mongol resistance."
    },
    "H-YS-20": {
        "name": "Yuan Shikai: Modernization Trap of the Beiyang System",
        "description": "Xiaozhan drills, abolished exams for schools, Hongxian monarchy 133 days, Beiyang fragmentation",
        "modes": [38, 8, 34, 40, 23],
        "reason": "Yuan Shikai was a tragic figure: 'old mandarin doing new military, old intrigue driving new modernization'. Core contradiction: using traditional intrigue (balance/co-option/self-coronation) to drive modern organizations (Beiyang Army/railways/telegraph/modern education), leading to internal fragmentation, external revolutionary alliance, monarchy dream shattered. Lesson: modern organizations need modern governance; intrigue cannot substitute systems.",
        "steps": [
            "Step 1: Crossing River by Feeling Stones — Xiaozhan drills (1895) copied German model, hired German instructors, built China's first modern army",
            "Step 2: Gradual Reform — Abolished imperial exams (1905) for modern schools, sent students abroad, created Ministry of Law/Education, pushed legal/educational modernization",
            "Step 3: Institutional Checks — Beiyang Six Divisions 'division commander' system, civilian supervisors, rotated garrisons, prevented warlord tail-wagging",
            "Step 4: Three Yamen Division / Power Balance Architecture — Military admin/command/staff separated (copied Japan/Germany), but President held supreme command, forming 'inverted power pyramid'",
            "Step 5: Natural Selection — Hongxian Monarchy (1915-1916) as 'ultimate experiment', market reacted violently (National Protection War/League withdrawal/Beiyang split), terminated in 133 days"
        ],
        "expected": [
            "Military modernization: Beiyang Army became backbone of Xinhai/early resistance",
            "Institutional legacy: legal/educational/fiscal/industrial embryonic systems",
            "Tragic end: monarchy destroyed republican legitimacy, Beiyang warlords split, 20 years chaos"
        ],
        "case": "Xiaozhan Drills → Beiyang Six Divisions (1895-1911): Yuan at Tianjin Xiaozhan copied German model, German instructors, established battalion/company/platoon/squad structure, created quartermaster/military law/medical corps. 1901-1904 expanded to Six Divisions (division=corps), 12k each, equipped with Mauser/Krupp. Xinhai: Beiyang crushed revolutionaries, forced Qing abdication. But Yuan relied on 'personal balance' (promote cronies/marriage alliances/grant governorships) not 'systemic checks'. Monarchy triggered Feng Guozhang/Duan Qirui/Cao Kun etc. to defect, Beiyang split into Zhili/Anhui/Fengtian cliques, 20 years warlord chaos."
    }
}

# Add to English scenarios
scenarios_en.update(new_scenarios_en)

with open('scenarios_en.json', 'w', encoding='utf-8') as f:
    json.dump(scenarios_en, f, ensure_ascii=False, indent=2)

print(f"Updated scenarios_en.json: {len(scenarios_en)} total scenarios")