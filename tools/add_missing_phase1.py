import json

# Load existing data
with open('scenarios_zh.json', 'r', encoding='utf-8') as f:
    zh = json.load(f)
with open('scenarios_en.json', 'r', encoding='utf-8') as f:
    en = json.load(f)
with open('code_maps.json', 'r', encoding='utf-8') as f:
    cm = json.load(f)

# Missing Phase 1 entries
new_entries = [
    {
        "code": "H-ZDL-152",
        "name_zh": "张道陵：天师道创始/符箓/道教组织化/宗教产业化先驱",
        "name_en": "Zhang Daoling: Tianshi Dao Founder/Talismans/Daoist Organization/Religious Industrialization Pioneer",
        "description_zh": "天师道/符箓/道教组织化/宗教产业化/巴蜀道教",
        "description_en": "Tianshi Dao/Talismans/Daoist Organization/Religious Industrialization/Ba-Shu Daoism",
        "modes": [33, 18, 34, 28, 35],
        "reason_zh": "核心思维：在「汉末宗法崩溃、百姓无依、巫鬼文化盛行」背景下，以「符箓治病-组织化传教-宗教产业化」三重工程。",
        "reason_en": "Core Thinking: In late Han's 'collapsed clan system, helpless populace, prevalent shamanism', engineered 'talisman healing-organized proselytization-religious industrialization' triple project.",
        "steps_zh": [
            "第1步：格局授权思维——以「老子化身/天师嫡传」神圣授权",
            "第2步：摸石头过河/实验主义——「符水治病/五斗米入教」低门槛试点",
            "第3步：制度化制衡——建「治/祭/酒/道/长」五级组织架构",
            "第4步：摸石头过河/实验主义——推广至江南/中原，网格化管理",
            "第5步：总体性思维——「神授权→组织化→产品化→传播化→产业化」范式"
        ],
        "steps_en": [
            "Step 1: Authority Delegation — Sacred authorization as 'Laozi incarnation'",
            "Step 2: Crossing River by Feeling Stones — 'Talisman water healing/five pecks rice entry' pilot",
            "Step 3: Institutional Checks — Five-tier org architecture",
            "Step 4: Crossing River by Feeling Stones — Grid management expansion",
            "Step 5: Systems Thinking — 'Divine authority→organization→productization→propagation→industrialization' paradigm"
        ],
        "expected_zh": [
            "创「五斗米道/天师道」，成本土宗教组织化鼻祖",
            "建五级组织架构，成宗教管理标准范本",
            "标准化四大宗教产品体系",
            "「低门槛-组织化-产品化」模式影响千年"
        ],
        "expected_en": [
            "Founded 'Five Pecks Rice Dao/Tianshi Dao', indigenous religion progenitor",
            "Built five-tier org architecture, religious management standard",
            "Standardized four religious product systems",
            "'Low-threshold-organization-productization' model influenced millennium"
        ],
        "case_zh": "张道陵（34-156），沛国丰人。汉桓帝永寿元年（155）于鹤鸣山著《道教本义》二十四卷，立传承谱系。创五斗米道：符水治病招信徒，入教缴五斗米。建治/祭/酒/道/长五级组织，设义舍置米肉行路者取之。科仪标准化：五色符箓、二十四科醮仪、《老子想尔注》标准经卷。其五步法成本土宗教工程化奠基范式。",
        "case_en": "Zhang Daoling (34-156), Peiguo Feng native. 155 CE at Heming Mountain authored Daoist Fundamentals 24 vols, established lineage. Founded Five Pecks Rice Dao: talisman water healing recruited followers, entry fee five pecks rice. Built five-tier org, established Yi She charity houses. Ritual standardization: five-color talismans, 24 ritual categories, Laozi Xiang'er Commentary. His five-step method became Chinese indigenous religious engineering paradigm."
    },
    {
        "code": "H-THJ-153",
        "name_zh": "陶弘景：茅山宗/本草经集注/真诰/道教理论体系化/科学道教融合先驱",
        "name_en": "Tao Hongjing: Maoshan School/Bencao Jing Jizhu/Zhen Gao/Daoist Theory Systematization/Scientific Daoist Fusion Pioneer",
        "description_zh": "茅山宗/本草经集注/真诰/道教理论体系/科学道教融合/山居/养生",
        "description_en": "Maoshan School/Bencao Jing Jizhu/Zhen Gao/Daoist Theory Systematization/Scientific Daoist Fusion/Mountain Dwelling/Health Preservation",
        "modes": [25, 19, 28, 35, 38],
        "reason_zh": "核心思维：在「道教经典散乱、药物学未系统、修行法门杂乱」南北朝，以「经典整理-药物学实证-修法体系化-山林实验」四重工程。",
        "reason_en": "Core Thinking: In Northern-Southern Dynasties' scattered Daoist classics/unsystematic pharmacology/chaotic cultivation methods, engineered quadruple project.",
        "steps_zh": [
            "第1步：抽象归纳法——提炼上清/神谱/仙阶/修法框架，生成《真诰》神谱体系",
            "第2步：实事求是法——重校《神农本草经》，增365药创三品分类法",
            "第3步：系统思维法——构建四大修法体系，标准化修行流程",
            "第4步：摸石头过河/实验主义——茅山华阳洞建四位一体道场",
            "第5步：总体性思维——五系统耦合成道教科学化全链路范式"
        ],
        "steps_en": [
            "Step 1: Abstract Induction — Extract Shangqing/divine hierarchy framework",
            "Step 2: Seeking Truth from Facts — Recollated Shennong Bencao Jing, added 365 medicines",
            "Step 3: Systems Thinking — Build four cultivation systems",
            "Step 4: Crossing River by Feeling Stones — Maoshan Huayang Cave four-in-one dao-chang",
            "Step 5: Systems Thinking — Five systems into Daoist scientification paradigm"
        ],
        "expected_zh": [
            "《真诰》二十卷成上清派神谱奠基",
            "《本草经集注》七卷增365药创三品分类，成首部实证本草巨著",
            "茅山华阳洞成四位一体道场范本",
            "《养生延命录》确立四大修法体系"
        ],
        "expected_en": [
            "Zhen Gao 20 vols became Shangqing divine hierarchy foundation",
            "Bencao Jing Jizhu 7 vols added 365 medicines, China's first empirical pharmacology masterpiece",
            "Maoshan Huayang Cave became four-in-one dao-chang paradigm",
            "Yangsheng Yanming Lu established four cultivation systems"
        ],
        "case_zh": "陶弘景（456-536），秣陵句容人，齐梁「山中宰相」。隐居茅山华阳洞三十年。《真诰》记杨羲/许迈父子仙界交流，建五层天界神谱。重校《神农本草经》，增药365种，创三品分类法，《本草经集注》成首部实证本草巨著。茅山华阳洞建四位一体道场，著《真诰/本草经集注/养生延命录/登真隐诀》，创四大修法。其五环闭环成道教理论化/科学化/体系化奠基工程。",
        "case_en": "Tao Hongjing (456-536), Moling Jurong native, Qi-Liang 'Mountain Prime Minister'. Zhen Gao 20 vols recorded Yang Xi/Xu Mi celestial communications, establishing Shangqing hierarchy. Recollated Shennong Bencao Jing, added 365 medicines, created three-grade classification, authored Bencao Jing Jizhu, China's first empirical pharmacology masterpiece. Maoshan Huayang Cave built four-in-one dao-chang, created four cultivation systems. His five-loop closure became Daoist theoretization/scientification/systematization foundational project."
    },
    {
        "code": "H-WZY-154",
        "name_zh": "王重阳：全真教创始/内丹/丘处机/蒙古西行/道教北派体系化奠基者",
        "name_en": "Wang Chongyang: Quanzhen School Founder/Internal Alchemy/Qiu Chuji/Mongol Westward Journey/Northern Daoism Systematization Founder",
        "description_zh": "全真教/内丹/丘处机/蒙古西行/道教北派/甘丹寺/辩经/考核/授衔",
        "description_en": "Quanzhen School/Internal Alchemy/Qiu Chuji/Mongol Westward Journey/Northern Daoism/Ganden Monastery/Debate/Examination/Conferment",
        "modes": [37, 21, 28, 35, 34],
        "reason_zh": "核心思维：在「金末元初道教宗派林立、内丹理论散乱、戒律废弛、出家/在家二元对立」背景下，以「内丹双修-戒律重建-出家在家融合-机构标准化」四重整合工程。",
        "reason_en": "Core Thinking: Against Jin-Yuan 'Daoist sects proliferating, internal alchemy scattered, lax discipline, monastic-lay binary', engineered quadruple integration.",
        "steps_zh": [
            "第1步：抽象归纳法——提炼内丹核心框架",
            "第2步：系统思维法——构建六阶次第与四维耦合模型",
            "第3步：摸石头过河/实验主义——活死人墓七年闭关验证",
            "第4步：制度化制衡——立全真戒律/七子传承/五职管理制",
            "第5步：总体性思维——五系统耦合成道教北派体系化范式"
        ],
        "steps_en": [
            "Step 1: Abstract Induction — Extract internal alchemy core framework",
            "Step 2: Systems Thinking — Build six-stage graduated path with four-dimensional coupling",
            "Step 3: Crossing River by Feeling Stones — Seven-year Living Dead Tomb retreat",
            "Step 4: Institutional Checks — Quanzhen Precepts/Seven Masters/five-position management",
            "Step 5: Systems Thinking — Five systems into Northern Daoism paradigm"
        ],
        "expected_zh": [
            "创全真教，成道教北派/内丹体系化奠基宗派",
            "确立内丹六阶次第与戒律体系",
            "全真七子传承制+辩经考核授衔标准化传承",
            "道观五职管理制，成道教机构标准化范本"
        ],
        "expected_en": [
            "Founded Quanzhen School, Northern Daoism/internal alchemy foundational sect",
            "Established internal alchemy six-stage graduated path and discipline system",
            "Seven Masters transmission + debate/examination/conferment standardized model",
            "Monastery five-position management, Daoist institutional standardization paradigm"
        ],
        "case_zh": "王重阳（1113-1170），咸阳人。1167甘河遇二仙传金丹秘诀，弃武从道。筑活死人墓七年闭关，悟性命双修。度马钰/谭处端/刘处玄/丘处机/王处一/郝大通/孙不二全真七子。立全真教/戒律十条/六阶内丹次第/七子传承制/辩经考核授衔/五职管理制。金世宗赐号全真教主。其五维整合成道教北派体系化奠基工程。",
        "case_en": "Wang Chongyang (1113-1170), Xianyang native. 1167 met two immortals at Ganhe, received Golden Elixir Secret. Built Living Dead Tomb seven-year retreat. 1167 initiated Seven Quanzhen Masters. Founded Quanzhen School, Precepts ten articles, six-stage internal alchemy, Seven Masters transmission, debate/examination/conferment standardization, five-position management. Jin Shizong granted Quanzhen Sect Master title. His five-dimensional integration became Northern Daoism systematization foundational project."
    },
    {
        "code": "H-QCJ-155",
        "name_zh": "丘处机：全真教二代/蒙古西行/止杀/全真教南传/道教外交/长春真人西游记",
        "name_en": "Qiu Chuji: Quanzhen Second Patriarch/Mongol Westward Journey/Stop Killing/Quanzhen South Transmission/Daoist Diplomacy/Changchun Zhenren Xiyou Ji",
        "description_zh": "全真教二代/蒙古西行/止杀/道教南传/长春真人西游记/道教外交/生死观/止杀",
        "description_en": "Quanzhen Second Patriarch/Mongol Westward Journey/Stop Killing/Quanzhen South Transmission/Changchun Zhenren Xiyou Ji/Daoist Diplomacy/Life-Death View/Stop Killing",
        "modes": [42, 41, 6, 34, 35],
        "reason_zh": "核心思维：在「蒙古铁骑南下、生灵涂炭、道教南北分裂、文化断层」关键节点，以「止杀/救民/文化传播/道教统一」四重使命。",
        "reason_en": "Core Thinking: At critical juncture of Mongol invasion/cultural rupture, undertook 'stop killing/save people/cultural transmission/Daoist unification' quadruple mission.",
        "steps_zh": [
            "第1步：统一战线法——锁定成吉思汗/耶律楚材/也里钦三大决策节点",
            "第2步：实事求是法——著《长春真人西游记》二十卷，六维模板记录中亚百三十余国",
            "第3步：灵活策略法——见成吉思汗四次进四策，获不杀为武止杀令挽救百万",
            "第4步：制度化制衡——度十八大弟子推南传统一南北，创白云观/长春宫",
            "第5步：总体性思维——六系统耦合成道教外交/文化/统一三位一体巅峰"
        ],
        "steps_en": [
            "Step 1: United Front — Lock Genghis Khan/Yelu Chucai/Yelu Ahai three key nodes",
            "Step 2: Seeking Truth from Facts — 20-vol Changchun Zhenren Xiyou Ji six-dim template",
            "Step 3: Flexible Strategy — Met Genghis Khan four times, stop-killing order saved millions",
            "Step 4: Institutional Checks — Initiated 18 disciples southward, founded Baiyun/Changchun",
            "Step 5: Systems Thinking — Six systems into Daoist diplomacy/cultural/unification trinity"
        ],
        "expected_zh": [
            "73岁万里西行两年，《西游记》成最早中亚实地考察记录",
            "四见成吉思汗获不杀为武止杀令，挽救百万生灵",
            "度十八大弟子推南传统一南北，创白云观/长春宫北派总部",
            "《西游记》六维模板成最早丝路考察学/中亚地理学奠基"
        ],
        "expected_en": [
            "73-year-old 10000-mile journey, Xiyou Ji earliest Central Asia field survey",
            "Met Genghis Khan four times, stop-killing order saved millions",
            "Initiated 18 disciples southward, unified north-south, founded headquarters",
            "Xiyou Ji six-dim template earliest Silk Road survey/Central Asia geography foundation"
        ],
        "case_zh": "丘处机（1148-1227），登州栖霞人，十九岁拜王重阳得长春子号。1219成吉思汗诏见，73岁西行两年万里返京。四见成吉思汗进六策，汗纳不杀为武止杀令免屠城百万。著《长春真人西游记》二十卷，十维模板记录中亚百三十余国。返途度十八大弟子推南传统一南北，创北京白云观/长春宫立全真派南北统一架构。其四重功绩成道教外交/文化/统一三位一体巅峰范式。",
        "case_en": "Qiu Chuji (1148-1227), Dengzhou Qixia native, 19 became Wang Chongyang disciple. 1219 Genghis Khan summoned, 73-year-old westward two years via Juyongguan/Samarkand/Hindu Kush/Amu Darya. Met Khan four times, proposed six strategies, Khan accepted 'no one not killed/non-killing as martial' stop-killing order saving millions. Authored 20-vol Changchun Zhenren Xiyou Ji recording 130+ kingdoms via ten-dimensional template. Return initiated 18 disciples southward, unified north-south Daoism. Founded Beijing Baiyun Guan/Changchun Palace, Quanzhen north-south unified architecture. His quadruple achievement became Daoist diplomacy/cultural transmission/sect unification trinity peak paradigm."
    },
    {
        "code": "H-SBH-156",
        "name_zh": "申不害：术/主/臣/权力监控/韩非源头/法家术家集大成者",
        "name_en": "Shen Buhai: Shu/Ruler/Minister/Power Monitoring/Legalist Shu School Founder/Kanfei Source",
        "description_zh": "术/主/臣/权力监控/韩非源头/韩国相/法家术家",
        "description_en": "Shu/Ruler/Minister/Power Monitoring/Legalist Shu School/Kanfei Source/Han Chancellor",
        "modes": [32, 34, 40, 28, 35],
        "reason_zh": "核心思维：在「战国弱国韩国、君主无力控制群臣、权力失控」背景下，以「术/主/臣/权力监控」四重工程。",
        "reason_en": "Core Thinking: In 'weak Han state, ruler unable to control ministers, power out of control', engineered 'shu/ruler/minister/power monitoring' quadruple project.",
        "steps_zh": [
            "第1步：抽象归纳法——提炼名/实/术/考核核心框架",
            "第2步：系统思维法——构建七维监控模型",
            "第3步：摸石头过河/实验主义——韩国相位推考绩/考功/考效三级考核",
            "第4步：制度化制衡——推申子六篇入法家经典，成法/术/势三位一体",
            "第5步：总体性思维——六系统耦合成中国古代行政管理奠基范式"
        ],
        "steps_en": [
            "Step 1: Abstract Induction — Extract name/reality/shu/assessment framework",
            "Step 2: Systems Thinking — Build seven-dimensional monitoring model",
            "Step 3: Crossing River by Feeling Stones — Han Chancellor three-tier assessment",
            "Step 4: Institutional Checks — Shenzi into Legalist classics, law/shu/power trinity",
            "Step 5: Systems Thinking — Six systems into Chinese administrative management paradigm"
        ],
        "expected_zh": [
            "创术概念，成韩非法/术/势三宝中术正统源头",
            "建名/实双轨监控，创名/责/功/效四维考核框架",
            "确立主/臣非对称权力：主持权/势/法/术，臣受名/责/刑/赏",
            "创听/察/防/制四重防控，成古代权力监控/考核奠基工程"
        ],
        "expected_en": [
            "Created shu concept, Han Fei's law/shu/power shu orthodox source",
            "Built name/reality dual-track monitoring, 4D assessment framework",
            "Established ruler/minister asymmetric power structure",
            "Created four-layer defense, ancient power monitoring/assessment foundation"
        ],
        "case_zh": "申不害（前385-前337），郑国人，韩昭侯相。著《申子》六篇创术学。核心：主执术/臣任事/名实相符/赏罚分明。建名/实双轨：臣请事为名，成事为实，名实相符则赏。主持权/势/法/术四维统御。创听/察/防/制四重防控。著《申子》六篇成韩非法/术/势三宝中术正统源头。其五维体系成中国古代权力监控/行政管理/考核体系奠基工程。",
        "case_en": "Shen Buhai (385-337 BCE), Zheng native, Han Zhaohou Chancellor. Authored 6-chapter Shenzi, founded Shu school. Core: ruler holds shu/minister handles affairs/name-reality match/clear rewards-punishments. Built name/reality dual-track. Ruler holds authority/power/law/shu four-dimensional control. Created listen/investigate/prevent/control four-layer defense. Shenzi 6 chapters became shu orthodox source of shu in Han Fei's law/shu/power three treasures. His five-dimensional system became Chinese ancient power monitoring/administrative management/assessment systems foundational project."
    },
    {
        "code": "H-SD-157",
        "name_zh": "慎到：势/法/术/法家三派/势位论/法家势派集大成者",
        "name_en": "Shen Dao: Shi/Law/Shu/Legalist Three Schools/Shi-Wei Theory/Legalist Shi School Founder",
        "description_zh": "势/法/术/法家三派/势位论/齐稷下学宫/田骈/接子/法家势派",
        "description_en": "Shi/Law/Shu/Legalist Three Schools/Shi-Wei Theory/Qi Jixia Academy/Tian Bian/Jiezi/Legalist Shi School",
        "modes": [33, 34, 40, 28, 35],
        "reason_zh": "核心思维：在「战国诸侯争霸、君主权力来源不明、法家内部分化」背景下，以「势/位/法/术」四重理论建构。",
        "reason_en": "Core Thinking: In 'Warring States lords contending, ruler power source unclear, Legalist internal division', engineered 'shi/wei/law/shu' quadruple theoretical construction.",
        "steps_zh": [
            "第1步：抽象归纳法——提炼势/位/权/势核心概念簇",
            "第2步：系统思维法——构建六维权力理论模型",
            "第3步：摸石头过河/实验主义——稷下学宫/燕/赵/韩游说验证",
            "第4步：制度化制衡——推慎子四十二篇入法家经典，成法家三派",
            "第5步：总体性思维——六系统耦合成中国古代政治权威理论奠基范式"
        ],
        "steps_en": [
            "Step 1: Abstract Induction — Extract shi/wei/power/situation core cluster",
            "Step 2: Systems Thinking — Build six-dimensional power theory model",
            "Step 3: Crossing River by Feeling Stones — Jixia Academy lobbying validating theory",
            "Step 4: Institutional Checks — Shenzi into Legalist classics, three schools complete",
            "Step 5: Systems Thinking — Six systems into Chinese power legitimacy paradigm"
        ],
        "expected_zh": [
            "创势位论，成法家势派正统源头",
            "法家三派申不害术/商鞅法/慎到势三位一体分野",
            "慎子四十二篇确立权/势/位三维权力理论模型",
            "势位论成古代权力合法性/政治权威/统治技术理论奠基工程"
        ],
        "expected_en": [
            "Created Shi-Wei Theory, Legalist Shi School orthodox source",
            "Legalist Three Schools trinity division complete Legalist theory",
            "42-chapter Shenzi established power/shi/wei 3D model",
            "Shi-Wei Theory became Chinese power legitimacy/political authority/ruling technology foundation"
        ],
        "case_zh": "慎到（前350-前275），赵国人，齐稷下学宫学者。著《慎子》四十二篇创势位论。核心：主势/主位/势位/法/术/德。主张君主合法性源于势/位而非仁/义/德，势为位势/权势/形势三势合一。著《慎子》十篇确立权/势/位三维模型。与田骈/接子并列稷下。其势位论与申不害术/商鞅法并列成法家三派分野，奠定法家完整理论分野。成中国古代权力合法性/政治权威/统治技术理论奠基工程。",
        "case_en": "Shen Dao (350-275 BCE), Zhao native, Qi Jixia Academy scholar. Authored 42-chapter Shenzi, founded Shi-Wei Theory. Core: ruler shi/ruler wei/shi wei/law/shu/de. Argued ruler legitimacy from shi/wei not ren/yi/de, shi as position power/power/situation trinity. Authored 10-chapter Shenzi establishing power/shi/wei 3D model. With Tian Bian/Jiezi at Jixia, lobbied Qi/Yan/Zhao/Han. His Shi-Wei Theory with Shen Buhai shu/Shang Yang law formed Legalist shu/law/shi three schools, establishing complete Legalist theory division. Became Chinese ancient power legitimacy/political authority/ruling technology theory foundational project."
    },
    {
        "code": "H-CWJ-163",
        "name_zh": "蔡文姬：汉末女史/胡笳十八拍/文献学/书法/女性文化传承/悲剧美学大师",
        "name_en": "Cai Wenji: Late Han Female Scholar/Hujia Shibapai/Bibliography/Calligraphy/Female Cultural Transmission/Tragic Aesthetics Master",
        "description_zh": "胡笳十八拍/文献学/书法/女性文化传承/悲剧美学/曹操/董祀/卫氏/归汉",
        "description_en": "Hujia Shibapai/Bibliography/Calligraphy/Female Cultural Transmission/Tragic Aesthetics/Cao Cao/Dong Si/Wei Shi/Return to Han",
        "modes": [25, 37, 28, 35, 38],
        "reason_zh": "核心思维：在「汉末战乱、典籍散佚、女性无书可读、文化断层」背景下，以「记忆复原/文化传承/悲剧升华/女性自我建构」四重工程。",
        "reason_en": "Core Thinking: In 'late Han warfare, scattered classics, women without books, cultural rupture', engineered quadruple project.",
        "steps_zh": [
            "第1步：抽象归纳法——提炼《后汉书》四百余卷框架建记忆复原模板",
            "第2步：摸石头过河/实验主义——作《胡笳十八拍》八母题验证悲剧美学",
            "第3步：知行合一/致良知——《悲愤诗》完成四重身份自我重构",
            "第4步：制度化制衡——推作品入乐府/诗集/文集三大文本体系",
            "第5步：总体性思维——四系统耦合成女性文献学/文化传承/悲剧美学三位一体范式"
        ],
        "steps_en": [
            "Step 1: Abstract Induction — Extract Hou Han Shu 400+ vols framework from memory",
            "Step 2: Crossing River by Feeling Stones — 18-movement Hujia Shibapai validating tragic aesthetics",
            "Step 3: Unity of Knowledge and Action — Bei Fen Shi completing quadruple identity reconstruction",
            "Step 4: Institutional Checks — Works into Yuefu/Poetry/Anthologies three text systems",
            "Step 5: Systems Thinking — Four systems into female bibliography/transmission/tragic aesthetics trinity"
        ],
        "expected_zh": [
            "背诵《后汉书》四百余卷为曹操复原失传，成最早记忆复原文献学范式",
            "《胡笳十八拍》十八首八母题升华四重创伤",
            "《悲愤诗》完成从才女/妻妾/俘虏/归汉四重身份自我重构",
            "成女性文化传承/文献学/悲剧美学三位一体奠基范式"
        ],
        "expected_en": [
            "Recited 400+ vols Hou Han Shu restored lost chapters, earliest memory restoration paradigm",
            "Hujia Shibapai 18 movements eight themes sublimating quadruple trauma",
            "Bei Fen Shi completed quadruple identity reconstruction",
            "Female cultural transmission/bibliography/tragic aesthetics trinity paradigm"
        ],
        "case_zh": "蔡文姬（177-？），陈留圉人，蔡邕女，博学善书法/数学/天文/音律。建安中被匈奴掳北地，嫁左贤王生二子。曹操重金赎回嫁董祀。曹操问家藏书四百余卷今存几何，文姬为君诵之复原《后汉书》失传篇目，成最早记忆复原文献学范式。作《胡笳十八拍》十八首八大母题，十八拍结构写尽四重创伤。作《悲愤诗》五言四大伦理张力完成四重身份自我重构。成中国女性文化传承/文献学/悲剧美学三位一体奠基范式。",
        "case_en": "Cai Wenji (177-?), Chenliu Yu native, Cai Yong daughter, broad learning. Jian'an captured by Xiongnu, married Left Virtuous King bore two sons. Cao Cao ransomed back, married Dong Si. Cao Cao asked '400+ vols how many remain?' Wenji recited Hou Han Shu 400+ vols from memory restoring lost chapters, earliest memory restoration paradigm. Composed Hujia Shibapai 18 movements eight themes with 18-beat structure writing quadruple trauma. Composed Bei Fen Shi four ethical tensions completing quadruple identity reconstruction. Female cultural transmission/bibliography/tragic aesthetics trinity paradigm."
    },
    {
        "code": "H-SGB-164",
        "name_zh": "上官婉儿：唐代女宰相/宫廷文学/制诰/书法/女性政治参与/文治政治桥梁",
        "name_en": "Shangguan Wan'er: Tang Female Chancellor/Palace Literature/Edicts/Calligraphy/Female Political Participation/Literary-Political Bridge",
        "description_zh": "女宰相/宫廷文学/制诰/书法/女性政治/唐中宗/韦后/李隆基/制诰体/婉约派",
        "description_en": "Female Chancellor/Palace Literature/Edicts/Calligraphy/Female Politics/Emperor Zhongzong/Empress Wei/Li Longji/Edict Style/Wanyue School",
        "modes": [33, 20, 28, 34, 35],
        "reason_zh": "核心思维：在「武周/唐初权力更迭、女性禁从政、宫廷文学宦官垄断」背景下，以「文学入政/制诰标准化/女性政治合法化/文治桥梁」四重工程。",
        "reason_en": "Core Thinking: In 'Wu Zhou/Tang power transition, women banned from politics, palace literature eunuch monopolized', engineered quadruple project.",
        "steps_zh": [
            "第1步：格局授权思维——才人/女官/女相三级授权跃迁获政治合法性",
            "第2步：摸石头过河/实验主义——创制诰体标准化十大公文标准化",
            "第3步：制度化制衡——推婉约派宫廷文学四美学范畴打破垄断",
            "第4步：摸石头过河/实验主义——辅佐四朝四重身份验证女性政治可行性",
            "第5步：总体性思维——五系统耦合成女性政治/公文标准化/宫廷文学三位一体范式"
        ],
        "steps_en": [
            "Step 1: Authority Delegation — Three-level authorization leap Cairen/female official/female chancellor",
            "Step 2: Crossing River by Feeling Stones — Edict Style standardization ten document types",
            "Step 3: Institutional Checks — Wanyue School four aesthetics breaking monopoly",
            "Step 4: Crossing River by Feeling Stones — Assisted four reigns validating feasibility",
            "Step 5: Systems Thinking — Five systems into female politics/document/literature trinity"
        ],
        "expected_zh": [
            "武则天赏识入宫掌制诰/批奏/宫廷文学三权，成首位实质女宰相",
            "创制诰体标准化十大公文，成唐代公文规范范本",
            "推婉约派四美学范畴打破宦官/外戚/权臣文学垄断",
            "辅佐四朝完成才人/女官/女相/文人四重身份跃迁"
        ],
        "expected_en": [
            "Wu Zetian favored, controlled edicts/memorial review/palace literature, first substantive female chancellor",
            "Created Edict Style standardization ten document types, Tang official document paradigm",
            "Promoted Wanyue School four aesthetics breaking eunuch/relatives/powerful ministers monopoly",
            "Assisted four reigns achieving Cairen/female official/female chancellor/literati leap"
        ],
        "case_zh": "上官婉儿（664-710），上官仪孙女。武则天赏识入宫为才人，掌制诰/批奏/宫廷文学三权，成首位实质女宰相。创制诰体标准化：典故/辞藻/格律/用典四维标准，十大公文标准化成唐代公文范本。推婉约派宫廷文学：柔美/含蓄/典雅/深情四美学范畴，打破宦官/外戚/权臣垄断，为李白/杜甫/王维盛唐诗坛铺路。辅佐中宗/韦后/睿宗/玄宗四朝，以文治/制诰/批奏/宫廷文学四重身份完成才人/女官/女相/文人四重跃迁。其四重工程成中国女性政治/公文标准化/宫廷文学三位一体奠基范式。",
        "case_en": "Shangguan Wan'er (664-710), Shangguan Yi granddaughter. Wu Zetian favored, entered as Cairen, controlled edicts/memorial review/palace literature, first substantive female chancellor. Created Edict Style standardization: allusion/literary grace/metrics/allusion four-dim standard, ten document types standardization becoming Tang official document paradigm. Promoted Wanyue School palace literature: gentle/subtle/elegant/deep four aesthetics breaking eunuch/relatives/powerful ministers monopoly, paving way for Li Bai/Du Fu/Wang Wei High Tang. Assisted Zhongzong/Wei Empress/Ruizong/Xuanzong four reigns, achieving Cairen/female official/female chancellor/literati quadruple leap. Her quadruple project became Chinese female politics/document standardization/palace literature trinity paradigm."
    },
    {
        "code": "H-WZT-166",
        "name_zh": "武则天：破门阀立科举/权力重构/女皇帝/唐制百代/权力工程化集大成者",
        "name_en": "Wu Zetian: Breaking Aristocracy Establishing Imperial Exams/Power Reconstruction/Female Emperor/Tang System Enduring/Power Engineering Master",
        "description_zh": "破门阀/立科举/女皇帝/权力重构/唐制百代/权力工程化/唐制百代",
        "description_en": "Breaking Aristocracy/Establishing Imperial Exams/Female Emperor/Power Reconstruction/Tang System Enduring/Power Engineering/Tang System Enduring",
        "modes": [33, 34, 18, 28, 35],
        "reason_zh": "核心思维：在「唐初门阀垄断/科举不全/女性无政权/权力结构僵化」背景下，以「破门阀/立科举/权力重构/制度工程化」四重工程。",
        "reason_en": "Core Thinking: In 'early Tang aristocratic monopoly/incomplete imperial exams/women no political power/rigid power structure', engineered quadruple project.",
        "steps_zh": [
            "第1步：格局授权思维——天命/神权/武周革命神圣授权",
            "第2步：制度化制衡——推科举制/殿试/武举/九品中正改革四维选官体系",
            "第3步：摸石头过河/实验主义——酷吏/罗织/改制/选贤四重手段试点权力重构",
            "第4步：摸石头过河/实验主义——均田/租调/两税雏形/抑制兼并土地财政改革",
            "第5步：总体性思维——五系统耦合成唯一女皇帝权力工程化集大成范式"
        ],
        "steps_en": [
            "Step 1: Authority Delegation — Sacred authorization via mandate of heaven/divine right",
            "Step 2: Institutional Checks — Imperial exams/palace exam/military exam/nine-rank reform",
            "Step 3: Crossing River by Feeling Stones — Cruel officials/entrapment/reform/select worthies pilot",
            "Step 4: Crossing River by Feeling Stones — Equal-field/rent-labor-tax/two-tax embryo land fiscal reform",
            "Step 5: Systems Thinking — Five systems into only female emperor power engineering masterpiece"
        ],
        "expected_zh": [
            "中国历史上唯一女皇帝，开武周一代，称圣神皇帝",
            "破关陇集团门阀垄断，立科举制/殿试/武举选官体系，奠科举千年基因",
            "立酷吏/罗织/改制/选贤权力重构工程，创酷吏后/法制化纠偏机制",
            "推均田/租调/两税雏形土地财政改革，创四维数据治理"
        ],
        "expected_en": [
            "China's only female emperor, founded Wu Zhou dynasty, titled Holy Divine Emperor",
            "Broke Guanlong Group aristocratic monopoly, established imperial exams/palace exam/military exam",
            "Established cruel officials/entrapment/reform/select worthies power reconstruction",
            "Promoted equal-field/rent-labor-tax/two-tax embryo land fiscal, four-dimensional data governance"
        ],
        "case_zh": "武则天（624-705），文德皇后武氏，太宗才人、高宗皇后、武周皇帝。655废王立武，690改唐为周称圣神皇帝，成唯一女皇帝。破关陇集团/七姓十族门阀垄断：推科举制增设殿试/武举，以考试/考绩/任用/监察四环闭环打破世袭垄断；立酷吏/罗织/改制/选贤权力重构：来俊臣/周兴/索元礼酷吏罗织旧贵族，后诛酷吏/用狄仁杰/张柬之/选贤任能纠偏固化。推均田制/租调制/两税法雏形土地财政：抑制兼并，立户口/田亩/税赋/徭役四维数据治理。立武氏/李氏/外戚/宰相/台省/六部六维权力制衡，创台省/六部/御史台三权分立雏形。其四重工程成唯一女皇帝权力工程化集大成范式，奠唐制百代/科举千年/女主政治制度基因。",
        "case_en": "Wu Zetian (624-705), Empress Wende, Taizong Cairen, Gaozong Empress, Wu Zhou Emperor. 655 deposed Wang made Wu, 690 changed Tang to Zhou, titled Holy Divine Emperor, China's only female emperor. Broke Guanlong Group/seven surnames ten clans aristocratic monopoly: promoted imperial exams added palace exam/military exam, breaking hereditary monopoly via exam/assessment/appointment/supervision four-loop closure; established cruel officials/entrapment/reform/select worthies power reconstruction: Lai Junchen/Zhou Xing/Suo Yuanli cruel officials entrap old aristocracy, later execute cruel officials/use Di Renjie/Zhang Jianzhi/select worthies correction solidification. Promoted equal-field/rent-labor-tax/two-tax embryo land fiscal: suppressed land merger, established household/land/tax/corvee four-dimensional data governance. Established Wu clan/Li clan/in-laws/chancellors/secretariat/six ministries six-dimensional power checks, creating secretariat/six ministries/censorate three-power separation embryo. Her quadruple project became only female emperor power engineering masterpiece, founding Tang system enduring/imperial exams millennium/female ruler politics institutional genes."
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

print(f"✅ Added {len(new_entries)} missing Phase 1 entries")