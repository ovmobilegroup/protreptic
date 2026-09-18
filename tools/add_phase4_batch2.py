import json

with open('scenarios_zh.json', 'r', encoding='utf-8') as f:
    zh = json.load(f)
with open('scenarios_en.json', 'r', encoding='utf-8') as f:
    en = json.load(f)
with open('code_maps.json', 'r', encoding='utf-8') as f:
    cm = json.load(f)

# Phase 4 Batch 2: 史学/军事/科学家 (9 figures)
new_figures = [
    {
        'code': 'H-MDL-260',
        'name_zh': '马端临：文献通考/经制考/制度史编纂集大成/职官/选举/食货/礼乐/兵刑/艺文',
        'name_en': 'Ma Duanlin: Wenxian Tongkao/Institutional Systems/Institutional History Compilation Synthesis/Official Positions/Elections/Finance/Rites Music/Military Criminal/Arts Literature',
        'desc_zh': '元代史学家，制度史编纂集大成。著文献通考三百四十八卷，以经制为核心概念，建二十四门制度考辨体系，将郑樵二十略深化为考据/辨伪/制度演变三级验证范式，为中国制度史学确立纵向演变/横向比较/考据互证三维分析框架。',
        'desc_en': 'Yuan historian, synthesizer of institutional history compilation. Authored Wenxian Tongkao 348 volumes, took institutional systems as core concept, built twenty-four gates institutional kao-bian system, deepened Zheng Qiao twenty-lue into evidential-research/distinguishing-false/institutional-evolution three-level verification paradigm, establishing longitudinal-evolution/horizontal-comparison/evidential-mutual-verification three-dimensional analysis framework for Chinese institutional historiography.',
        'modes': [22, 25, 29, 28, 35],
        'reason_zh': '马端临著文献通考以经制为核心，建二十四门制度考辨体系，将郑樵二十略深化为考据/辨伪/制度演变三级验证范式，确立纵向演变/横向比较/考据互证三维分析框架。',
        'reason_en': 'Ma Duanlin authored Wenxian Tongkao with institutional systems as core, built twenty-four gates institutional kao-bian system, deepened Zheng Qiao twenty-lue into evidential-research/distinguishing-false/institutional-evolution three-level verification paradigm, establishing longitudinal-evolution/horizontal-comparison/evidential-mutual-verification three-dimensional analysis framework.',
        'steps_zh': ['本体锚定：锁定制度资料散佚/演变逻辑不清/考据深度不足为元代史学主要矛盾，确立制度演进逻辑为破解杠杆', '协议标准化：以经制为核心概念，建田赋/赋税/钱币/市舶/兵制/选举/职官/礼制/乐制/舆地/民族/艺文二十四门制度考辨体系', '系统集成：构建纵向演变/横向比较/考据互证三维分析框架，将制度史从静态罗列提升为动态演进工程', '工程化传承：著文献通考三百四十八卷成制度史大全，以文本固化制度演进逻辑防失传', '动态校准：设计考辨/补遗/正谬三级修订机制，用负向证据密度量化制度演进路径可信度'],
        'steps_en': ['Ontological Anchoring: Lock institutional materials scattered/evolution logic unclear/evidential depth insufficient as Yuan historiography main contradiction', 'Protocol Standardization: Take institutional systems as core concept, build twenty-four gates institutional kao-bian system', 'System Integration: Construct longitudinal-evolution/horizontal-comparison/evidential-mutual-verification three-dimensional analysis framework', 'Engineering Transmission: Authored Wenxian Tongkao 348 volumes as institutional history encyclopedia, solidify institutional evolution logic with text', 'Dynamic Calibration: Design kao-bian/supplement/correct three-level revision mechanism, quantify institutional evolution path credibility with negative evidence density'],
        'expected_zh': '成中国制度史编纂集大成大家，确立纵向演变/横向比较/考据互证三维分析框架',
        'expected_en': 'Become synthesizer of Chinese institutional history compilation, establishing longitudinal-evolution/horizontal-comparison/evidential-mutual-verification three-dimensional analysis framework',
        'case_zh': '元史学家，名端临，字贵与。著文献通考三百四十八卷。核心：经制核心概念、二十四门制度考辨、纵向演变/横向比较/考据互证三维框架。影响赵翼/王鸣盛/章学诚/张惠言/黄宗会/黄百家/魏源/龚自珍制度史/考据/演变全版图。',
        'case_en': 'Yuan historian, name Duanlin, courtesy Guiyu. Authored Wenxian Tongkao 348 volumes. Core: institutional systems core concept, twenty-four gates institutional kao-bian, longitudinal-evolution/horizontal-comparison/evidential-mutual-verification three-dimensional framework. Influenced Zhao Yi/Wang Mingsheng/Zhang Xuecheng/Zhang Huayan/Huang Zonghui/Huang Baijia/Wei Yuan/Gong Zizhen institutional history/evidential research/evolution entire map.'
    },
    {
        'code': 'H-YS-261',
        'name_zh': '袁枢：通鉴纪事本末/编年体/史学编纂/宋元/制度化叙事',
        'name_en': 'Yuan Shu: Tongjian Jishi Benmo/Annals Style/Historiography Compilation/Song Yuan/Institutionalized Narrative',
        'desc_zh': '南宋史学家，编年体变体/史学编纂方法革新者。著通鉴纪事本末四十二卷，创纪事本末体例，将资治通鉴编年体重组为事以类聚/本末具备/因果贯通三维叙事范式，建起/继/转/合四段式事件编纂标准。完成从纯编年到编年体变体制度化叙事的范式跃迁。',
        'desc_en': 'Southern Song historian, innovator of annals style variant/historiography compilation method. Authored Tongjian Jishi Benmo 42 volumes, created jishi-benmo style, reorganized Zizhi Tongjian annals style into event-clustered/cause-effect-contained/causal-chain-contiguous three-dimensional narrative paradigm, built start-continue-turn-conclude four-segment event compilation standard. Completed paradigm leap from pure annals to annals-style-variant/institutionalized-narrative.',
        'modes': [25, 30, 31, 28, 35],
        'reason_zh': '袁枢著通鉴纪事本末创纪事本末体例，将资治通鉴编年体重组为事以类聚/本末具备/因果贯通三维叙事范式，建起/继/转/合四段式事件编纂标准，完成从纯编年到编年体变体制度化叙事的范式跃迁。',
        'reason_en': 'Yuan Shu authored Tongjian Jishi Benmo creating jishi-benmo style, reorganized Zizhi Tongjian annals style into event-clustered/cause-effect-contained/causal-chain-contiguous three-dimensional narrative paradigm, built start-continue-turn-conclude four-segment event compilation standard, completing paradigm leap from pure annals to annals-style-variant/institutionalized-narrative.',
        'steps_zh': ['本体锚定：锁定编年叙事碎片化/因果链断裂/检索困难为宋代编年史学主要矛盾，确立事件本位/因果链为破解杠杆', '协议标准化：创纪事本末体例标准，建起/继/转/合四段式事件编纂协议', '系统集成：将资治通鉴编年体重组为事以类聚/本末具备/因果贯通三维叙事范式', '工程化传承：著通鉴纪事本末四十二卷成编年体变体教科书，以文本固化事件本位范式防失传', '动态校准：设事件完整/因果贯通/类聚合理/检索便捷四重编纂底线'],
        'steps_en': ['Ontological Anchoring: Lock annalistic narrative fragmentation/causal-chain broken/retrieval difficult as Song annalistic historiography main contradiction', 'Protocol Standardization: Create jishi-benmo style standard, build start-continue-turn-conclude four-segment event compilation protocol', 'System Integration: Reorganized Zizhi Tongjian annals style into event-clustered/cause-effect-contained/causal-chain-contiguous three-dimensional narrative paradigm', 'Engineering Transmission: Authored Tongjian Jishi Benmo 42 volumes as annals-style-variant textbook, solidified event-centric paradigm with text', 'Dynamic Calibration: Set event-complete/causal-chain-contiguous/clustering-reasonable/retrieval-convenient four compilation baselines'],
        'expected_zh': '成中国编年体变体/制度化叙事奠基，事件本位/因果链/标准化编纂三维现代范式',
        'expected_en': 'Become Chinese annals-style-variant/institutionalized-narrative foundation, event-centric/causal-chain/standardized-compilation three-dimensional modern paradigm',
        'case_zh': '南宋史学家，名枢，字才翁，号洪洲。著通鉴纪事本末四十二卷。核心：纪事本末体例、事以类聚/本末具备/因果贯通、起/继/转/合四段式。影响王应麟/郑樵/马端临/钱大昕/赵翼/章学诚/张惠言/黄宗会/黄百家编年/体例/因果全版图。',
        'case_en': 'Southern Song historian, name Shu, courtesy Caiweng, style Hongzhou. Authored Tongjian Jishi Benmo 42 volumes. Core: jishi-benmo style, event-clustered/cause-effect-contained/causal-chain-contiguous, start-continue-turn-conclude four-segment. Influenced Wang Yinglin/Zheng Qiao/Ma Duanlin/Qian Daxin/Zhao Yi/Zhang Xuecheng/Zhang Huayan/Huang Zonghui/Huang Baijia annalistic/style/causal entire map.'
    },
    {
        'code': 'H-QQ-262',
        'name_zh': '钱谦：考据/史学/目录学/嘉庆学派/钱氏三代/考据传承',
        'name_en': 'Qian Qian: Evidential Research/Historiography/Bibliography/Qianjia School/Qian Family Three Generations/Evidential Transmission',
        'desc_zh': '清代考据学家，嘉庆学派/钱氏三代代表。著十驾斋养新录/廿二史考异补五大考据著作，融钱大昕之学/王鸣盛之法/阮元之平三源，建考据/史学/目录/金石四维考据体系，作为钱大昕长孙/学统继承者，将考据实证/史料辨伪/目录编纂/金石释读四大技能模块化传承。',
        'desc_en': 'Qing evidential scholar, representative of Qianjia School/Qian Family Three Generations. Authored five major evidential works, fused Qian Daxin learning/Wang Mingsheng method/Ruan Yuan balance three sources, built four-dimensional evidential system, as Qian Daxin grandson/learning lineage inheritor, modularized four skill modules: evidential-empirical/historical-material-distinguishing-false/bibliography-compilation/epigraphy-interpretation transmission.',
        'modes': [25, 30, 31, 28, 35],
        'reason_zh': '钱谦著十驾斋养新录/廿二史考异补五大考据著作，融钱大昕之学/王鸣盛之法/阮元之平三源，建考据/史学/目录/金石四维考据体系，作为钱大昕长孙/学统继承者，将考据实证/史料辨伪/目录编纂/金石释读四大技能模块化传承。',
        'reason_en': 'Qian Qian authored five major evidential works, fused Qian Daxin learning/Wang Mingsheng method/Ruan Yuan balance three sources, built four-dimensional evidential system, as Qian Daxin grandson/learning lineage inheritor, modularized four skill modules.',
        'steps_zh': ['本体锚定：锁定考据碎片化/传承断层/技能隐性为嘉庆学派主要矛盾，确立家族传承/技能模块化为破解杠杆', '协议标准化：融钱大昕之学/王鸣盛之法/阮元之平三源，建考据/史学/目录/金石四维考据体系', '系统集成：将考据实证/史料辨伪/目录编纂/金石释读四大技能模块化，建钱氏三代传承标准', '工程化传承：著十驾斋养新录/廿二史考异补/历代职官表固化家族学统/多维融合/技能模块化范式防失传', '动态校准：设考据/史学/目录/金石/传承五重底线'],
        'steps_en': ['Ontological Anchoring: Lock evidential fragmentation/transmission broken/skills tacit as Qianjia School main contradiction', 'Protocol Standardization: Fused Qian Daxin learning/Wang Mingsheng method/Ruan Yuan balance three sources, built four-dimensional evidential system', 'System Integration: Modularized four skill modules: evidential-empirical/historical-material-distinguishing-false/bibliography-compilation/epigraphy-interpretation, built Qian family three-generations transmission standard', 'Engineering Transmission: Authored Ten Jias Studio Nurturing New Records/Twenty-Two Investigations Supplement/Historical Official Positions Tables solidified family-learning-lineage/multi-dimensional-fusion/skill-modularization paradigm', 'Dynamic Calibration: Set evidential/historiography/bibliography/epigraphy/transmission five baselines'],
        'expected_zh': '成中国考据学家族传承/多维融合/技能模块化三维传承范式奠基，嘉庆学派/钱氏三代代表',
        'expected_en': 'Become Chinese evidential studies family-transmission/multi-dimensional-fusion/skill-modularization three-dimensional transmission paradigm foundation, Qianjia School/Qian Family Three Generations representative',
        'case_zh': '清考据学家，名谦，字受之，号十驾斋主人。钱大昕长孙，王鸣盛门生。著十驾斋养新录/廿二史考异补/历代职官表/目录学/金石学。融钱大昕之学/王鸣盛之法/阮元之平三源，建考据/史学/目录/金石四维体系。将考据实证/史料辨伪/目录编纂/金石释读四大技能模块化传承。影响钱坫/钱鼎/钱增植/阮元/王鸣盛/赵翼/龚自珍考据/传承全版图。',
        'case_en': 'Qing evidential scholar, name Qian, courtesy Shouzhi, style Ten Jias Studio Master. Qian Daxin grandson, Wang Mingsheng disciple. Authored Ten Jias Studio Nurturing New Records/Twenty-Two Investigations Supplement/Historical Official Positions Tables/Bibliography/Epigraphy. Fused three sources, built four-dimensional system. Modularized four skill modules. Influenced Qian Yin/Qian Ding/Qian Zengzhi/Ruan Yuan/Wang Mingsheng/Zhao Yi/Gong Zizhen entire evidential/transmission map.'
    },
    {
        'code': 'H-BQ-263',
        'name_zh': '白起：秦将/长平之战/人屠/歼灭战/心理战/全胜思维极致/运动歼灭',
        'name_en': 'Bai Qi: Qin General/Changping Battle/Human Butcher/Annihilation Warfare/Psychological Warfare/Total Victory Thinking Extreme/Maneuver Annihilation',
        'desc_zh': '战国秦将，歼灭战/心理战/全胜思维极致大师。以长平之战四十万赵军坑杀创歼灭战/围歼/心理崩溃三位一体战法，建知己知彼/避实击虚/诱敌深入/集中优势/全歼五步歼灭协议，将心理战/情报战/运动战融合为破敌意志/夺取主动/以少胜多三大战略支柱。其不战而屈人之兵全胜思维将孙子百战百胜非善之善推至极致。',
        'desc_en': 'Warring States Qin general, master of annihilation warfare/psychological warfare/total victory thinking extreme. Created annihilation-warfare/encirclement-annihilation/psychological-collapse trinity tactics with Changping Battle 400k Zhao troops buried alive, built five-step annihilation protocol, fused psychological-warfare/intelligence-warfare/maneuver-warfare into three strategic pillars. His win-without-fighting total-victory-thinking pushed Sun Tzu hundred-battles-hundred-victories-not-best to extreme.',
        'modes': [15, 3, 16, 28, 35],
        'reason_zh': '白起以长平之战四十万坑杀创歼灭战/围歼/心理崩溃三位一体战法，建知己知彼/避实击虚/诱敌深入/集中优势/全歼五步歼灭协议，将心理战/情报战/运动战融合为破敌意志/夺取主动/以少胜多三大战略支柱，成中国军事思想歼灭/心理/全胜三维极致范式。',
        'reason_en': 'Bai Qi created annihilation-warfare/encirclement-annihilation/psychological-collapse trinity tactics with Changping Battle 400k buried alive, built five-step annihilation protocol, fused psychological-warfare/intelligence-warfare/maneuver-warfare into three strategic pillars, becoming Chinese military thought annihilation/psychological/total-victory three-dimensional extreme paradigm.',
        'steps_zh': ['本体锚定：锁定攻坚难/伤亡大/持久战为战国作战主要矛盾，确立歼灭战/心理战为破解杠杆', '协议标准化：建五步歼灭协议：知己知彼-避实击虚-诱敌深入-集中优势-全歼，将孙子全胜思维工程化', '系统集成：融合心理战/情报战/运动战为破敌意志/夺取主动/以少胜多三大战略支柱', '工程化传承：以长平坑杀四十万成教科书级歼灭案例，用战果固化歼灭战标准', '动态校准：设不打无准备之仗/不打无把握之仗/不打无收获之仗三重底线'],
        'steps_en': ['Ontological Anchoring: Lock difficult siege/heavy casualties/protracted war as Warring States combat main contradiction', 'Protocol Standardization: Build five-step annihilation protocol: know self know enemy - avoid real strike void - lure enemy deep - concentrate advantages - total annihilation', 'System Integration: Fuse psychological-warfare/intelligence-warfare/maneuver-warfare into three strategic pillars', 'Engineering Transmission: Use Changping burying 400k as textbook-level annihilation case, solidify annihilation-warfare standard with combat results', 'Dynamic Calibration: Set three baselines: no unprepared battle/no unsure battle/no unprofitable battle'],
        'expected_zh': '成中国军事思想歼灭/心理/全胜三维极致范式，长平坑杀四十万成教科书级歼灭案例',
        'expected_en': 'Become Chinese military thought annihilation/psychological/total-victory three-dimensional extreme paradigm, Changping burying 400k becomes textbook-level annihilation case',
        'case_zh': '战国秦将，唯一未尝败绩名将。长平之战诱赵括出战，围歼四十万赵军坑杀，创歼灭战/心理战教科书级案例。其不战而屈人之兵全胜思维推孙子百战百胜非善之善至极致。影响李靖/韩世忠/岳飞/戚继光/李成梁/曾国藩/刘伯承/贺龙/粟裕歼灭/心理/运动战全版图。',
        'case_en': 'Warring States Qin general, only undefeated famous general. Changping Battle lured Zhao Kuo into battle, encircled annihilated 400k Zhao troops buried alive, created textbook-level annihilation/psychological warfare case. His win-without-fighting total victory thinking pushed Sun Tzu hundred-battles-hundred-victories-not-best to extreme. Influenced Li Jing/Han Shizhong/Yue Fei/Qijiguang/Li Chengliang/Zeng Guofan/Liu Bocheng/He Long/Su Yu annihilation/psychological/maneuver warfare entire map.'
    },
    {
        'code': 'H-LJ-264',
        'name_zh': '李靖：唐初名将/李卫公问对/兵法/平突厥/平辅公祏/军事理论体系化',
        'name_en': 'Li Jing: Early Tang General/Li Weigong QA/Military Theory/Pacify Turks/Pacify Fu Gongshi/Military Theory Systematization',
        'desc_zh': '唐初名将，军事理论/作战指挥体系化大师。著李卫公问对八篇，建天时/地利/人和/将才/兵势五要素作战判断模型，确立先声后实/虚实相生/奇正循环/歼灭/追击五阶作战流程，将平突厥/平辅公祏/平萧铜/平刘黑闼四大战役经验提炼为大漠机动/背水一战/分进合击/围点打援四大战术模块。完成从孙吴兵法到李靖兵法的体系化跃迁。',
        'desc_en': 'Early Tang famous general, master of military theory/combat command systematization. Authored Li Weigong QA 8 chapters, built five-element combat judgment model, established five-phase combat process, extracted four major campaigns into four tactical modules. Completed systematization leap from Sun-Wu military art to Li Jing military art, introducing five-element-judgment/five-phase-process/four-tactical-modules standardized combat engineering paradigm.',
        'modes': [15, 16, 31, 28, 35],
        'reason_zh': '李靖著李卫公问对建五要素作战判断模型，确立五阶作战流程，提炼四大战术模块，完成从孙吴兵法到李靖兵法的体系化跃迁，为中国军事理论引入五要素判断/五阶流程/四大战术标准化作战工程范式。',
        'reason_en': 'Li Jing authored Li Weigong QA building five-element combat judgment model, established five-phase combat process, extracted four tactical modules, completed systematization leap from Sun-Wu military art to Li Jing military art, introducing five-element-judgment/five-phase-process/four-tactical-modules standardized combat engineering paradigm.',
        'steps_zh': ['本体锚定：锁定作战经验碎片化/理论体系缺失/指挥标准不一为唐初军事主要矛盾，确立体系化为破解杠杆', '协议标准化：建五要素判断模型(天时/地利/人和/将才/兵势)与五阶作战流程(先声后实/虚实相生/奇正循环/歼灭/追击)', '系统集成：提炼大漠机动/背水一战/分进合击/围点打援四大战术模块，构建标准化作战工程库', '工程化传承：著李卫公问对八篇成兵法教科书，以文本固化作战标准防失传', '动态校准：设敌情/我情/地情/天情四情动态判断机制，用实战验证战术模块有效性'],
        'steps_en': ['Ontological Anchoring: Lock combat experience fragmentation/theory system missing/command standards inconsistent as early Tang military main contradiction', 'Protocol Standardization: Build five-element judgment model and five-phase combat process', 'System Integration: Extract desert-maneuver/back-water-battle/divide-advance-combine-attack/besiege-point-strike-relief four tactical modules', 'Engineering Transmission: Authored Li Weigong QA 8 chapters as military textbook, solidify combat standards with text', 'Dynamic Calibration: Set enemy-situation/own-situation/terrain-situation/weather-situation four-situation dynamic judgment mechanism'],
        'expected_zh': '成中国军事理论体系化奠基大家，建五要素判断/五阶流程/四大战术标准化作战工程范式',
        'expected_en': 'Become Chinese military theory systematization founding master, establishing five-element-judgment/five-phase-process/four-tactical-modules standardized combat engineering paradigm',
        'case_zh': '唐初名将，平突厥/平辅公祏/平萧铜/平刘黑闼四大战役全胜。著李卫公问对八篇，建五要素判断模型、五阶作战流程、四大战术模块。其大漠机动战法破突厥骑兵机动优势，背水一战破辅公祏水军优势。影响韩世忠/岳飞/戚继光/李成梁/曾国藩/刘伯承/贺龙/粟裕军事理论/作战指挥全版图。',
        'case_en': 'Early Tang famous general, four major campaigns all victorious. Authored Li Weigong QA 8 chapters, built five-element judgment model, five-phase combat process, four tactical modules. His desert-maneuver tactics broke Turkic cavalry mobility advantage, back-water-battle broke Fu Gongshi naval advantage. Influenced Han Shizhong/Yue Fei/Qijiguang/Li Chengliang/Zeng Guofan/Liu Bocheng/He Long/Su Yu military theory/combat command entire map.'
    },
    {
        'code': 'H-KSZ-265',
        'name_zh': '韩世忠：抗金/岳飞同辈/水军/战术创新/黄天荡/以少胜多/游击歼灭',
        'name_en': 'Han Shizhong: Anti-Jin/Yue Fei Peer/Navy/Tactical Innovation/Huangtiandang/Win with Fewer/Guerrilla Annihilation',
        'desc_zh': '南宋抗金名将，水军/游击歼灭/战术创新大师。以黄天荡八千困十万金军创水陆结合/火攻/游击/心理四维战法，建背嵬军/精忠报国/以少胜多/运动歼灭四大战法与冻死不拆屋饿死不掳掠军纪重构军民关系。将抗外侮/护百姓/军政分离/民主治军融合为抗外/人民/正义三重正义性基石，为中国军事思想引入水军/游击/民主/正义四维民族战争范式。',
        'desc_en': 'Southern Song anti-Jin famous general, navy/guerrilla annihilation/tactical innovation master. Created water-land-combination/fire-attack/guerrilla/psychological four-dimensional tactics with Huangtiandang 8k trapping 100k Jin troops, built Beiwei Army/loyalty-to-country/win-with-fewer/maneuver-annihilation four major tactics with freeze-death-not-dismantle-houses/starve-death-not-loot discipline reconstructing military-civilian relations. Fused resist-foreign-invasion/protect-people/military-political-separation/democratic-command into anti-foreign/people/justice three-fold justice cornerstone, introducing navy/guerrilla/democratic/justice four-dimensional national war paradigm.',
        'modes': [14, 15, 16, 33, 35],
        'reason_zh': '韩世忠以黄天荡八千困十万金军创水陆结合/火攻/游击/心理四维战法，建背嵬军/精忠报国/以少胜多/运动歼灭四大战法与冻死不拆屋饿死不掳掠军纪，将抗外侮/护百姓/军政分离/民主治军融合为抗外/人民/正义三重正义性基石。',
        'reason_en': 'Han Shizhong created water-land-combination/fire-attack/guerrilla/psychological four-dimensional tactics with Huangtiandang 8k trapping 100k Jin troops, built Beiwei Army/loyalty-to-country/win-with-fewer/maneuver-annihilation four major tactics with freeze-death-not-dismantle-houses/starve-death-not-loot discipline, fused resist-foreign-invasion/protect-people/military-political-separation/democratic-command into anti-foreign/people/justice three-fold justice cornerstone.',
        'steps_zh': ['本体锚定：锁定正规军僵化/军民对立/抗战意志不足为南宋抗金主要矛盾，确立人民战争/正义战争为破解杠杆', '协议标准化：建水陆结合/火攻/游击/心理四维战法与背嵬军/精忠报国/以少胜多/运动歼灭四大战法及冻死不拆屋饿死不掳掠军纪', '系统集成：融合抗外侮/护百姓/军政分离/民主治军为抗外/人民/正义三重正义性基石', '工程化传承：以黄天荡/朱仙镇大捷成教科书级人民战争案例，用战果固化游击歼灭/军事民主标准', '动态校准：设不扰民/不掳掠/不畏死/不投降四重军纪底线，用民心向背验证战争正义性'],
        'steps_en': ['Ontological Anchoring: Lock regular army rigid/military-civilian opposition/insufficient resistance will as Southern Song anti-Jin main contradiction', 'Protocol Standardization: Built water-land-combination/fire-attack/guerrilla/psychological four-dimensional tactics and Beiwei Army/loyalty-to-country/win-with-fewer/maneuver-annihilation four major tactics', 'System Integration: Fused resist-foreign-invasion/protect-people/military-political-separation/democratic-command into anti-foreign/people/justice three-fold justice cornerstone', 'Engineering Transmission: Use Huangtiandang/Zhuxianzhen victories as textbook-level people-war cases, solidify guerrilla-annihilation/military-democracy standards', 'Dynamic Calibration: Set four disciplinary baselines: not disturb people/not loot/not fear death/not surrender, verify war justice with people-heart orientation'],
        'expected_zh': '成中国军事思想水军/游击/民主/正义四维民族战争范式奠基，黄天荡/朱仙镇成教科书级人民战争案例',
        'expected_en': 'Become Chinese military thought navy/guerrilla/democratic/justice four-dimensional national war paradigm foundation, Huangtiandang/Zhuxianzhen become textbook-level people-war cases',
        'case_zh': '南宋抗金名将，名世忠，字良臣，号闲闲居士。黄天荡八千困十万金军，创水陆结合/火攻/游击/心理四维战法。建背嵬军，军纪冻死不拆屋饿死不掳掠。朱仙镇五百骑破十万金军。融合抗外侮/护百姓/军政分离/民主治军为抗外/人民/正义三重正义性。影响戚继光/李成梁/曾国藩/刘伯承/贺龙/粟裕/林彪/邓小平人民战争/游击战/正义战争全版图。',
        'case_en': 'Southern Song anti-Jin famous general, name Shizhong, courtesy Liangchen, style Xianxian Jushi. Huangtiandang 8k trapped 100k Jin troops, created water-land-combination/fire-attack/guerrilla/psychological four-dimensional tactics. Built Beiwei Army, discipline freeze-death-not-dismantle-houses starve-death-not-loot. Zhuxianzhen 500 cavalry broke 100k Jin troops. Fused resist-foreign-invasion/protect-people/military-political-separation/democratic-command into anti-foreign/people/justice three-fold justice. Influenced Qijiguang/Li Chengliang/Zeng Guofan/Liu Bocheng/He Long/Su Yu/Lin Biao/Deng Xiaoping people-war/guerrilla-warfare/just-war entire map.'
    },
    {
        'code': 'H-CG-266',
        'name_zh': '陈赓：兵团指挥/太岳区/军事教育/三大战役/国防科工/军事理论/开国上将',
        'name_en': 'Chen Geng: Army Group Command/Taiyue Area/Military Education/Three Campaigns/National Defense Science Industry/Military Theory/Founding General',
        'desc_zh': '现代军事家，兵团指挥/军事教育/国防科工三位一体实践者。以上党/晋冀鲁豫/太岳/三大战役/抗美援朝/国防科工/军事工程学院七大实践建运动战/阵地战/游击战/兵团作战/军事教育/国防工业/战略预判七大军事算子。主持军事工程学院/国防科工委/两弹一星选址/军事理论教材四大军教/国防工程，推打仗/建设/教育/科研四位一体军事现代化体系。',
        'desc_en': 'Modern military strategist, army group command/military education/national defense science industry trinity practitioner. Built seven military operators with seven practices. Presided over four military education/national defense projects, promoted fight-construction-education-research four-in-one military modernization system.',
        'modes': [14, 15, 16, 33, 35],
        'reason_zh': '陈赓以上党/晋冀鲁豫/太岳/三大战役/抗美援朝/国防科工/军事工程学院七大实践建运动战/阵地战/游击战/兵团作战/军事教育/国防工业/战略预判七大军事算子，主持军事工程学院/国防科工委/两弹一星选址/军事理论教材四大军教/国防工程，推打仗/建设/教育/科研四位一体军事现代化体系。',
        'reason_en': 'Chen Geng built seven military operators with seven practices, presided over four military education/national defense projects, promoted fight-construction-education-research four-in-one military modernization system.',
        'steps_zh': ['本体锚定：锁定军事单一/教育脱节/科工分离/战略短视为新中国军事建设主要矛盾，确立兵团/教育/科工/战略四维硬核为破解杠杆', '协议标准化：建运动战/阵地战/游击战/兵团作战/军事教育/国防工业/战略预判七大军事算子', '系统集成：主持军事工程学院/国防科工委/两弹一星选址/军事理论教材四大军教/国防工程，推打仗/建设/教育/科研四位一体体系', '工程化传承：以上党/太岳/三大战役/抗美援朝/两弹一星五大实践固化兵团/教育/科工/战略范式', '动态校准：设兵团/教育/科工/战略四重军事现代化底线'],
        'steps_en': ['Ontological Anchoring: Lock military-single/education-disconnected/sci-industry-separated/strategy-short-sighted as New China military construction main contradiction', 'Protocol Standardization: Built seven military operators: maneuver/positional/guerrilla/army-group/education/defense-industry/strategic', 'System Integration: Presided over four military education/national defense projects, promoted fight-construction-education-research four-in-one system', 'Engineering Transmission: Solidified army-group/education/sci-industry/strategy paradigm with five major practices', 'Dynamic Calibration: Set army-group/education/sci-industry/strategy four military modernization baselines'],
        'expected_zh': '成中国军事现代化兵团/教育/科工/战略四维硬核范式奠基，上将/军事工程学院院长/国防科工委副主任',
        'expected_en': 'Become Chinese military modernization army-group/education/sci-industry/strategy four-dimensional hardcore paradigm foundation, General/Military Engineering Institute President/National Defense Sci-Industry Commission Deputy Director',
        'case_zh': '开国上将，名赓，字伯钧。上党/晋冀鲁豫/太岳/三大战役/抗美援朝/国防科工/军事工程学院七大实践。建运动战/阵地战/游击战/兵团作战/军事教育/国防工业/战略预判七大军事算子。主持军事工程学院/国防科工委/两弹一星选址/军事理论教材四大工程。其七大实践/七大算子/四大工程/四位一体四维融合，成军事现代化兵团/教育/科工/战略四维硬核范式。',
        'case_en': 'Founding General, name Geng, courtesy Bojun. Shangdang/Jin-Ji-Lu-Yu/Taiyue/Three Campaigns/Korean War/National Defense Sci-Industry/Military Engineering Institute seven practices. Built seven military operators. Presided over Military Engineering Institute/National Defense Sci-Industry Commission/Two Bombs One Star Site Selection/Military Theory Textbooks four projects. Their seven-practices/seven-operators/four-projects/four-in-one four-dimensional fusion became military modernization army-group/education/sci-industry/strategy four-dimensional hardcore paradigm.'
    },
    {
        'code': 'H-YJY-267',
        'name_zh': '叶剑英：战略决策/军事外交/国家建设/长征/遵义/抗战/改革开放/元帅',
        'name_en': 'Ye Jianying: Strategic Decision/Military Diplomacy/National Construction/Long March/Zunyi/War of Resistance/Reform Opening/Marshal',
        'desc_zh': '现代军事/政治/外交三位一体战略家。以长征/遵义会议/延安整风/抗战/三大战役/广东/粉碎四人帮/改革开放/中央军委/国家副主席十大历史节点建战略预判/政治军事融合/外交斡旋/组织重构四大战略算子。主持军队正规化/军衔制/军事法院/军事检察/兵役法/国防科工委六大军制改革，推科技强军/精兵简政/法治治军/人才强军四大现代化方略。完成从红军参谋长到元帅/国家副主席/中央军委副主席的身份跃迁。',
        'desc_en': 'Modern military/political/diplomatic trinity strategist. Built four strategic operators with ten historical nodes. Presided over six major military system reforms, promoted four modernization strategies, completed identity leap from Red Army chief of staff to Marshal/State Vice Chairman/CMC Vice Chairman.',
        'modes': [6, 13, 14, 20, 35],
        'reason_zh': '叶剑英以长征/遵义/延安/抗战/三大战役/广东/粉碎四人帮/改革开放/中央军委/国家副主席十大节点建战略预判/政治军事融合/外交斡旋/组织重构四大战略算子，主持军队正规化/军衔制/军事法院/军事检察/兵役法/国防科工委六大军制改革，推科技强军/精兵简政/法治治军/人才强军四大现代化方略。',
        'reason_en': 'Ye Jianying built four strategic operators with ten historical nodes, presided over six major military system reforms, promoted four modernization strategies, completed identity leap from Red Army chief of staff to Marshal/State Vice Chairman/CMC Vice Chairman.',
        'steps_zh': ['本体锚定：锁定军事政治分离/外交孤立/建设滞后/法治缺失为新中国前期/改革期主要矛盾，确立战略/外交/建设/法治为破解杠杆', '协议标准化：建战略预判/政治军事融合/外交斡旋/组织重构四大战略算子，主持军队正规化/军衔制/军事法院/军事检察/兵役法/国防科工委六大军制改革', '系统集成：融合科技强军/精兵简政/法治治军/人才强军四大现代化方略，建战略/外交/建设/法治四维国家级体系', '工程化传承：以遵义/三大战役/广东/粉碎四人帮/改革开放五大历史实践固化战略/外交/建设/法治范式', '动态校准：设战略/外交/建设/法治四重国家级底线'],
        'steps_en': ['Ontological Anchoring: Lock military-political separation/diplomatic isolation/construction lag/rule-of-law-absent as early New China/reform period main contradiction', 'Protocol Standardization: Built four strategic operators, presided over six major military system reforms', 'System Integration: Fused four modernization strategies, built strategic/diplomatic/construction/rule-of-law four-dimensional state-level system', 'Engineering Transmission: Solidified strategic/diplomatic/construction/rule-of-law paradigm with five historical practices', 'Dynamic Calibration: Set strategic/diplomatic/construction/rule-of-law four state-level baselines'],
        'expected_zh': '成中国现代军事/政治战略/外交/建设/法治四维国家级范式奠基，元帅/国家副主席/中央军委副主席',
        'expected_en': 'Become Chinese modern military/politics strategic/diplomatic/construction/rule-of-law four-dimensional state-level paradigm foundation, Marshal/State Vice Chairman/CMC Vice Chairman',
        'case_zh': '开国元帅，名剑英，字仲华。长征/遵义会议/延安整风/抗战/三大战役/广东攻略/粉碎四人帮/改革开放/中央军委/国家副主席十大节点。建战略预判/政治军事融合/外交斡旋/组织重构四大战略算子。主持军队正规化/军衔制/军事法院/军事检察/兵役法/国防科工委六大军制改革。推科技强军/精兵简政/法治治军/人才强军四大现代化方略。其十大节点/四大算子/六大改革/四大方略四维融合，成现代军事政治战略/外交/建设/法治四维国家级范式。',
        'case_en': 'Founding Marshal, name Jianying, courtesy Zhonghua. Long March/Zunyi/Yan'an Rectification/War of Resistance/Three Campaigns/Guangdong/Crushing Gang of Four/Reform Opening/Central Military Commission/State Vice Chairman ten nodes. Built four strategic operators. Presided over six military system reforms. Promoted four modernization strategies. Their ten-nodes/four-operators/six-reforms/four-strategies four-dimensional fusion became modern military-politics strategic/diplomatic/construction/rule-of-law four-dimensional state-level paradigm.'
    },
    {
        'code': 'H-XSY-268',
        'name_zh': '许世友：反击战/边境作战/军队建设/长征/对越自卫反击战/军队正规化/硬骨头',
        'name_en': 'Xu Shiyou: Counterattack/Border Warfare/Military Construction/Long March/Sino-Vietnamese War/Military Regularization/Hard Bone',
        'desc_zh': '现代军事家，边境作战/军队建设/反击战专家。以对越自卫反击战/老山/者阴山/法卡山/两山轮战/长征/川西剿匪/广州军区/北京军区九大军事实践建山地作战/阵地战/运动歼灭/后勤保障/政治工作五大边境作战算子。主持广州军区/北京军区/军队正规化/军衔制/训练大纲/政治工作条例六大军建工程，推硬骨头/打仗不怕死/训练严/纪律铁四大部队文化基因。完成从红军连长到上将/广州军区司令/北京军区司令/中央军委委员的身份跃迁。',
        'desc_en': 'Modern military strategist, border warfare/military construction/counterattack expert. Built five border warfare operators with nine military practices. Presided over six military construction projects, promoted four troop culture genes, completed identity leap from Red Army company commander to General/Guangzhou MR/Beijing MR Commander/CMC Member.',
        'modes': [14, 15, 16, 33, 35],
        'reason_zh': '许世友以对越自卫反击战/老山/者阴山/法卡山/两山轮战九大实践建山地作战/阵地战/运动歼灭/后勤保障/政治工作五大边境作战算子，主持广州/北京军区/军队正规化/军衔制/训练大纲/政治工作条例六大军建工程，推硬骨头/打仗不怕死/训练严/纪律铁四大部队文化基因，完成从红军连长到上将广州/北京军区司令的身份跃迁。',
        'reason_en': 'Xu Shiyou built five border warfare operators with nine practices, presided over six military construction projects, promoted four troop culture genes, completed identity leap from Red Army company commander to General/Guangzhou MR/Beijing MR Commander/CMC Member.',
        'steps_zh': ['本体锚定：锁定边境冲突/山地作战难/后勤困难/部队软为边境作战主要矛盾，确立山地/阵地/运动/后勤/政治五维硬核为破解杠杆', '协议标准化：建山地作战/阵地战/运动歼灭/后勤保障/政治工作五大边境作战算子，主持广州/北京军区/军队正规化/军衔制/训练大纲/政治工作条例六大军建工程', '系统集成：推硬骨头/打仗不怕死/训练严/纪律铁四大部队文化基因，融合山地/阵地/运动/后勤/政治五维硬核体系', '工程化传承：以老山/者阴山/法卡山/两山轮战四大战役成边境作战教科书，以广州/北京军区建设固化军建标准', '动态校准：设山地/阵地/运动/后勤/政治五重边境作战底线'],
        'steps_en': ['Ontological Anchoring: Lock border conflict/mountain-warfare-difficult/logistics-difficult/troops-soft as border warfare main contradiction', 'Protocol Standardization: Built five border warfare operators, presided over six military construction projects', 'System Integration: Promoted four troop culture genes, fused mountain/position/maneuver/logistics/political five-dimensional hardcore system', 'Engineering Transmission: Used four major battles as border warfare textbook, solidified military construction standards with two MRs', 'Dynamic Calibration: Set mountain/position/maneuver/logistics/political five border warfare baselines'],
        'expected_zh': '成中国边境作战/军队建设山地/阵地/运动/后勤/政治五维硬核范式奠基，上将/广州军区司令/北京军区司令/中央军委委员',
        'expected_en': 'Become Chinese border warfare/military construction mountain/position/maneuver/logistics/political five-dimensional hardcore paradigm foundation, General/Guangzhou MR/Beijing MR Commander/CMC Member',
        'case_zh': '开国上将，名世友，字治平。对越自卫反击战/老山/者阴山/法卡山/两山轮战九大实践。建山地作战/阵地战/运动歼灭/后勤保障/政治工作五大边境作战算子。主持广州/北京军区/军队正规化/军衔制/训练大纲/政治工作条例六大军建工程。推硬骨头/打仗不怕死/训练严/纪律铁四大部队文化基因。其九大实践/五大算子/六大工程/四大基因四维融合，成边境作战/军队建设五维硬核范式。',
        'case_en': 'Founding General, name Shiyou, courtesy Zhiping. Sino-Vietnamese War/Laoshan/Zheyinshan/Fakashan/Two Mountains Rotation nine practices. Built five border warfare operators. Presided over Guangzhou/Beijing MR/military regularization/military ranks/training syllabus/political work regulations six projects. Promoted four troop culture genes. Their nine-practices/five-operators/six-projects/four-genes four-dimensional fusion became border warfare/military construction five-dimensional hardcore paradigm.'
    },
    {
        'code': 'H-YX-269',
        'name_zh': '一行(僧)：大衍历/浑天仪/大衍历/佛教天文/天文历法仪器信息流速',
        'name_en': 'Yixing (Monk): Dayan Calendar/Armillary Sphere/Dayan Calendar/Buddhist Astronomy/Astronomy Calendar Instruments Information Flow Speed',
        'desc_zh': '唐代僧/天文学家，大衍历/浑天仪/信息流速奠基。以大衍历修九服/九埠/交食/五星/节气，建黄赤道/交食限/出入限/食甚/食分五大交食计算标准，制浑天仪/木壳/水运/候楼四部仪器系统，实现日行一度/月行十三度/交食预报/节气精准四大天文工程指标。将佛教因果/天文周期/历法工程融合为周期/因果/工程三维认知框架，为中国天文历法引入标准化/仪器化/工程化现代范式。',
        'desc_en': 'Tang monk/astronomer, founder of Dayan Calendar/armillary sphere/information flow speed. Revised nine-fu/nine-pu/eclipses/five-planets/solar-terms with Dayan Calendar, built five major eclipse calculation standards, built four-part instrument system, achieved four astronomical engineering indicators. Fused Buddhist-causality/astronomical-cycles/calendar-engineering into cycles/causality/engineering three-dimensional cognitive framework, introducing standardization/instrumentation/engineering modern paradigm for Chinese astronomical calendar.',
        'modes': [12, 25, 28, 35, 41],
        'reason_zh': '一行以大衍历修九服/九埠/交食/五星/节气，建五大交食计算标准，制浑天仪/木壳/水运/候楼四部仪器系统，实现日行一度/月行十三度/交食预报/节气精准四大天文工程指标，将佛教因果/天文周期/历法工程融合为周期/因果/工程三维认知框架。',
        'reason_en': 'Yixing revised nine-fu/nine-pu/eclipses/five-planets/solar-terms with Dayan Calendar, built five major eclipse calculation standards, built four-part instrument system, achieved four astronomical engineering indicators, fused Buddhist-causality/astronomical-cycles/calendar-engineering into cycles/causality/engineering three-dimensional cognitive framework.',
        'steps_zh': ['本体锚定：锁定历法积误/交食预报失准/仪器简陋为唐代天文主要矛盾，确立标准化/仪器化为破解杠杆', '协议标准化：建五大交食计算标准(黄赤道/交食限/出入限/食甚/食分)，制浑天仪/木壳/水运/候楼四部仪器系统', '系统集成：融合佛教因果/天文周期/历法工程为周期/因果/工程三维认知框架，实现日行一度/月行十三度/交食预报/节气精准', '工程化传承：推大衍历/制浑天仪/建候楼三重交付物，以文本与实物固化天文标准防失传', '动态校准：设观测/计算/验证/修历四阶天文工程闭环，用交食实测验证历法精度'],
        'steps_en': ['Ontological Anchoring: Lock calendar accumulated-error/eclipse-forecast-inaccurate/instruments-crude as Tang astronomy main contradiction, establish standardization/instrumentation as breakthrough lever', 'Protocol Standardization: Build five major eclipse calculation standards (ecliptic-equator/eclipse-limits/entry-exit-limits/max-eclipse/eclipse-magnitude), build four-part instrument system', 'System Integration: Fused Buddhist-causality/astronomical-cycles/calendar-engineering into cycles/causality/engineering three-dimensional cognitive framework', 'Engineering Transmission: Promote Dayan Calendar/build armillary-sphere/build observation-tower three deliverables, solidify astronomical standards with text and artifacts', 'Dynamic Calibration: Set observe/calculate/verify/revise-calendar four-stage astronomical engineering closure, verify calendar precision with eclipse empirical measurement'],
        'expected_zh': '成唐代天文历法/仪器/信息流速奠基，引入标准化/仪器化/工程化现代范式',
        'expected_en': 'Become Tang astronomical calendar/instruments/information-flow-speed foundation, introducing standardization/instrumentation/engineering modern paradigm',
        'case_zh': '唐代僧/天文学家，名遂，字一行。推大衍历修九服/九埠/交食/五星/节气，建黄赤道/交食限/出入限/食甚/食分五大交食计算标准。制浑天仪/木壳/水运/候楼四部仪器系统，实现日行一度/月行十三度/交食预报/节气精准。将佛教因果/天文周期/历法工程融合为周期/因果/工程三维框架。影响祖冲之/郭守敬/李善兰/丁文江/翁文灏/华罗庚/竺可桢/钱学森天文/历法/仪器/信息流速传统全版图。',
        'case_en': 'Tang monk/astronomer, name Sui, courtesy Yixing. Proposed Dayan Calendar revising nine-fu/nine-pu/eclipses/five-planets/solar-terms, built five major eclipse calculation standards. Built armillary-sphere/wooden-shell/water-driven/observation-tower four-part instrument system, achieved sun-moves-one-degree/moon-moves-thirteen-degrees/eclipse-forecast/solar-terms-precision. Fused Buddhist-causality/astronomical-cycles/calendar-engineering into cycles/causality/engineering three-dimensional framework. Influenced Zu Chongzhi/Guo Shoujing/Li Shanlan/Ding Wenjiang/Weng Wenhao/Hua Luogeng/Zhu Kezhen/Qian Xuesen astronomy/calendar/instruments/information-flow-speed tradition entire map.'
    }
]

for fig in new_figures:
    code = fig['code']
    if code not in zh:
        zh[code] = {
            'name': fig['name_zh'],
            'description': fig['desc_zh'],
            'modes': fig['modes'],
            'reason': fig['reason_zh'],
            'steps': fig['steps_zh'],
            'expected': fig['expected_zh'],
            'case': fig['case_zh']
        }
        en[code] = {
            'name': fig['name_en'],
            'description': fig['desc_en'],
            'modes': fig['modes'],
            'reason': fig['reason_en'],
            'steps': fig['steps_en'],
            'expected': fig['expected_en'],
            'case': fig['case_en']
        }
        cm['CODE_MAP'][code] = fig['name_zh']
        cm['CODE_MAP_EN'][code] = fig['name_en']

with open('scenarios_zh.json', 'w', encoding='utf-8') as f:
    json.dump(zh, f, ensure_ascii=False, indent=2)
with open('scenarios_en.json', 'w', encoding='utf-8') as f:
    json.dump(en, f, ensure_ascii=False, indent=2)
with open('code_maps.json', 'w', encoding='utf-8') as f:
    json.dump(cm, f, ensure_ascii=False, indent=2)

print(f'Added {len(new_figures)} new figures')
print(f'Total ZH: {len(zh)}')
print(f'Total EN: {len(en)}')
print(f'ZH H-: {sum(1 for k in zh if k.startswith("H-"))}')
print(f'EN H-: {sum(1 for k in en if k.startswith("H-"))}')
print(f'CODE_MAP: {len(cm["CODE_MAP"])}')
print(f'CODE_MAP_EN: {len(cm["CODE_MAP_EN"])}')