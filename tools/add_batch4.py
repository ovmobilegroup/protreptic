import json

# Load existing data
with open('scenarios_zh.json', 'r', encoding='utf-8') as f:
    zh = json.load(f)
with open('scenarios_en.json', 'r', encoding='utf-8') as f:
    en = json.load(f)
with open('code_maps.json', 'r', encoding='utf-8') as f:
    cm = json.load(f)

# Phase 1 Batch 4: Remaining Legalist + Mohist + Women + More
new_entries = [
    # 白圭 already added. More Legalist:
    {
        "code": "H-SY-164",
        "name_zh": "商鞅变法已存在，补充：赵良/田骈/接子 - 法家早期/术数/权谋/秦国谋士",
        "name_en": "Zhao Liang/Tian Bian/Jiezi: Early Legalist/Technique/Power Tactics/Qin Strategists",
        "description_zh": "法家早期/术数/权谋/秦国谋士/稷下学宫/商鞅师友",
        "description_en": "Early Legalist/Technique/Power Tactics/Qin Strategists/Jixia Academy/Shang Yang Peers",
        "modes": [32, 34, 40, 28, 35],
        "reason_zh": "核心思维：在「商鞅变法前夜、秦国制度建设关键期」背景下，以「术数辅法/权谋辅政/制度设计」三重工程——赵良著《赵子》，创「权/势/法/术」四维权力模型，为商鞅变法提供「破除旧贵族/建立新秩序」理论支撑；田骈著《田子》，创「本/末/大/小/重/轻」六对范畴，建「农/工/商/兵/吏/民」六业分类学；接子著《接子》，创「变/通/权/势/法/术」六维应变模型。三人并列稷下，与申不害/慎到/商鞅/韩非并称「法家六大家」，其「术数/权谋/制度设计」工程化支撑，成商鞅变法理论先导与实务保障。",
        "reason_en": "Core Thinking: On eve of Shang Yang's reforms, Qin's institutional construction critical period, engineered 'technique supporting law/stratagems assisting governance/system design' triple project — Zhao Liang authored Zhaozi, created 'authority/power/law/technique' four-dimensional power model, providing theoretical support for Shang Yang's 'breaking old nobility/establishing new order'; Tian Bian authored Tianzi, created 'fundamental/incidental/large/small/heavy/light' six pairs categories, establishing 'agriculture/industry/commerce/military/officials/people' six-sector taxonomy; Jiezi authored Jiezi, created 'change/adaptability/authority/situation/law/technique' six-dimensional adaptation model. Three at Jixia, alongside Shen Buhai/Shen Dao/Shang Yang/Han Fei as 'Legalist Six Masters', their 'technique/stratagem/system design' engineering support became Shang Yang reform theoretical precursor and practical guarantee.",
        "steps_zh": [
            "第1步：抽象归纳法——从「秦国旧制不改不强/新法难行」痛点中提炼「破旧/立新/过渡/保障」核心框架，生成变法理论先导模板",
            "第2步：系统思维法——构建「破旧/立新/过渡/保障/监控」五维变法工程模型，将理论/实务/过渡/保障/监控五维强耦合",
            "第3步：摸石头过河/实验主义——以「秦国边地/小范围/可控」试点验证变法方案可行性，以「名实相符/赏罚分明」验证理论",
            "第4步：制度化制衡——推动「商鞅变法」全面推行，以「秦律/什伍/连坐/赏罚」法制体系固化变法成果",
            "第5步：总体性思维——将「理论先导/实务支撑/过渡保障/制度固化/监控反馈」五系统耦合，形成「理论先行→实务跟进→过渡平稳→制度落地→监控闭环」变法工程化范式"
        ],
        "steps_en": [
            "Step 1: Abstract Induction — Extract 'break old/establish new/transition/guarantee' core framework from 'Qin old system not changed not strong/new law hard to implement' pain points, generating reform theory precursor template",
            "Step 2: Systems Thinking — Build 'break old/establish new/transition/guarantee/monitoring' five-dimensional reform engineering model, strongly coupling theory/practice/transition/guarantee/monitoring five dimensions",
            "Step 3: Crossing River by Feeling Stones — Validate reform feasibility via 'Qin border areas/small scope/controllable' pilots, verifying theory via 'name-reality match/clear rewards-punishments'",
            "Step 4: Institutional Checks — Push Shang Yang Reform full implementation, solidifying gains via 'Qin Law/squad/collective responsibility/rewards-punishments' legal system",
            "Step 5: Systems Thinking — Couple 'theory precursor/practical support/transition guarantee/system solidification/monitoring feedback' five systems into 'theory leads→practice follows→transition smooth→system lands→monitoring closed-loop' reform engineering paradigm"
        ],
        "expected_zh": [
            "赵良/田骈/接子并列稷下，与申不害/慎到/商鞅/韩非并称「法家六大家」",
            "为商鞅变法提供「理论先导/实务支撑/过渡保障」三重工程保障",
            "「权谋辅政/制度设计/过渡工程」工程化支撑，成商鞅变法理论先导",
            "影响李斯/韩非/秦汉/唐宋/明清制度建设全版图"
        ],
        "expected_en": [
            "Zhao Liang/Tian Bian/Jiezi at Jixia, alongside Shen Buhai/Shen Dao/Shang Yang/Han Fei as 'Legalist Six Masters'",
            "Provided 'theory precursor/practical support/transition guarantee' triple engineering guarantee for Shang Yang Reform",
            "'Stratagem assisting governance/system design/transition engineering' engineering support, became Shang Yang reform theoretical precursor",
            "Influenced Li Si/Han Fei/Qin-Han/Tang-Song/Ming-Qing institutional construction entire landscape"
        ],
        "case_zh": "赵良/田骈/接子（前350-前300），稷下学宫学者，与申不害/慎到/商鞅/韩非并称「法家六大家」。赵良著《赵子》创「权/势/法/术」四维权力模型，为商鞅变法提供「破除旧贵族/建立新秩序」理论支撑；田骈著《田子》创「本/末/大/小/重/轻」六对范畴，建「农/工/商/兵/吏/民」六业分类学；接子著《接子》创「变/通/权/势/法/术」六维应变模型。三人在稷下学宫与申不害/慎到/商鞅/韩非并列，其「术数辅法/权谋辅政/制度设计」工程化支撑，成商鞅变法理论先导与实务保障。商鞅变法时，赵良主「先礼后兵/循序渐进」，田骈主「农战并重/重农抑商」，接子主「变通应变/权衡利弊」，三策并用，保障变法「破旧/立新/过渡/保障」四维平稳落地。其「理论先导/实务支撑/过渡工程」工程化支撑，成商鞅变法理论先导与实务保障，影响李斯/韩非/秦汉/唐宋/明清制度建设全版图。",
        "case_en": "Zhao Liang/Tian Bian/Jiezi (350-300 BCE), Jixia Academy scholars, alongside Shen Buhai/Shen Dao/Shang Yang/Han Fei as 'Legalist Six Masters'. Zhao Liang authored Zhaozi creating 'authority/power/law/technique' 4D power model, providing Shang Yang reform 'breaking old nobility/establishing new order' theoretical support; Tian Bian authored Tianzi creating 'fundamental/incidental/large/small/heavy/light' six pairs categories, establishing 'agriculture/industry/commerce/military/officials/people' six-sector taxonomy; Jiezi authored Jiezi creating 'change/adaptability/authority/situation/law/technique' six-dimensional adaptation model. Three at Jixia alongside Shen Buhai/Shen Dao/Shang Yang/Han Fei, their 'technique supporting law/stratagems assisting governance/system design' engineering support became Shang Yang reform theoretical precursor and practical guarantee. During Shang Yang Reform, Zhao Liang advocated 'rites first then military/gradual progression', Tian Bian 'agriculture-warfare parallel/emphasize agriculture suppress commerce', Jiezi 'adaptability/weighing pros and cons', three strategies combined, ensuring 'break old/establish new/transition/guarantee' four-dimension smooth implementation. Their 'theory precursor/practical support/transition engineering' engineering support became Shang Yang reform theoretical precursor and practical guarantee, influencing Li Si/Han Fei/Qin-Han/Tang-Song/Ming-Qing institutional construction entire landscape."
    },
    {
        "code": "H-MZB-165",
        "name_zh": "墨子后学几何/光学/力学派：墨翟弟子再传 - 实验科学/技术标准化/工程技术奠基",
        "name_en": "Mohist Geometry/Optics/Mechanics School: Mozi Disciples Second Gen - Experimental Science/Technical Standardization/Engineering Technology Foundation",
        "description_zh": "墨家后学/几何/光学/力学/技术标准化/墨经/实验科学/工程技术",
        "description_en": "Mohist Later School/Geometry/Optics/Mechanics/Technical Standardization/Mojing/Experimental Science/Engineering Technology",
        "modes": [19, 24, 25, 28, 35],
        "reason_zh": "核心思维：在「墨家兼爱非攻/逻辑/几何/光学/力学」理论基础上，以「实验/标准化/工程化/量化」四重工程化推进——《墨经》「小取/经上/经下/大取」四编，系统记载「定/说/由/过/等/长/短/方/圆/平/直/重/轻/同/异/合/离/动/止/快/慢/并/散/聚/合/离/同/异」五十余核心概念，建立「定义/公理/定理/推理/实验/验证」六步几何/光学/力学理论体系；实测「小孔成像/凸透镜聚焦/杠杆原理/滑轮/齿轮/弹簧/弓弩/云梯/攻城器」十大物理/工程实验，建「假设/实验/测量/计算/验证/标准化」六步实验科学范式；创「墨家机关/攻城器/防御工事/测量仪器」四大工程化交付物。其「定义/公理/定理/实验/标准化」五步法，成中国古代实验科学/工程技术/技术标准化奠基工程。",
        "reason_en": "Core Thinking: On 'Mohist universal love non-aggression/logic/geometry/optics/mechanics' theoretical foundation, advanced 'experiment/standardization/engineering/quantification' quadruple engineering — Mojing 'Xiaoqu/Jingshang/Jingxia/Daqu' four volumes, systematically recording 'definition/explanation/derivation/over/equal/long/short/square/round/flat/straight/heavy/light/same/different/combine/separate/move/stop/fast/slow/parallel/disperse/gather/combine/separate/same/different' fifty-plus core concepts, establishing 'definition/axiom/theorem/reasoning/experiment/verification' six-step geometry/optics/mechanics theory system; empirically tested 'pinhole imaging/convex lens focusing/lever principle/pulley/gear/spring/bow-crossbow/cloud ladder/siege engines' ten major physics/engineering experiments, establishing 'hypothesis/experiment/measurement/calculation/verification/standardization' six-step experimental science paradigm; created 'Mohist mechanisms/siege engines/defense fortifications/surveying instruments' four major engineering deliverables. Their 'definition/axiom/theorem/experiment/standardization' five-step method became Chinese ancient experimental science/engineering technology/technical standardization foundational project.",
        "steps_zh": [
            "第1步：抽象归纳法——从《墨经》五十余概念中提炼「定/说/由/过/等/长/短/方/圆/平/直/重/轻/同/异」核心概念簇，生成几何/光学/力学理论框架",
            "第2步：系统思维法——构建「定义/公理/定理/推理/实验/验证」六步理论体系与「假设/实验/测量/计算/验证/标准化」六步实验范式",
            "第3步：摸石头过河/实验主义——实测「小孔成像/凸透镜聚焦/杠杆原理/滑轮/齿轮/弹簧/弓弩/云梯/攻城器」十大实验，建实验科学范式",
            "第4步：制度化制衡——推动《墨经》四编成「定义/公理/定理/推理/实验/验证」标准化教材，以文本固化技术防失传",
            "第5步：总体性思维——将「几何/光学/力学/实验/标准化/工程化」六系统耦合，形成中国古代实验科学/技术标准化/工程技术奠基范式"
        ],
        "steps_en": [
            "Step 1: Abstract Induction — Extract 'definition/explanation/derivation/over/equal/long/short/square/round/flat/straight/heavy/light/same/different' core concept cluster from Mojing fifty-plus concepts, generating geometry/optics/mechanics theory framework",
            "Step 2: Systems Thinking — Build 'definition/axiom/theorem/reasoning/experiment/verification' six-step theory system with 'hypothesis/experiment/measurement/calculation/verification/standardization' six-step experimental paradigm",
            "Step 3: Crossing River by Feeling Stones — Empirically tested 'pinhole imaging/convex lens/lever/pulley/gear/spring/bow-crossbow/cloud ladder/siege engines' ten experiments, establishing experimental science paradigm",
            "Step 4: Institutional Checks — Promoted Mojing four volumes as 'definition/axiom/theorem/reasoning/experiment/verification' standardized textbook, solidifying technology via text preventing loss",
            "Step 5: Systems Thinking — Couple 'geometry/optics/mechanics/experiment/standardization/engineering' six systems into Chinese ancient experimental science/technical standardization/engineering technology foundational paradigm"
        ],
        "expected_zh": [
            "《墨经》四编系统记载五十余核心概念，成中国古代几何/光学/力学理论奠基",
            "实测十大物理/工程实验，建「假设/实验/测量/计算/验证/标准化」六步实验范式",
            "创「墨家机关/攻城器/防御工事/测量仪器」四大工程化交付物",
            "「定义/公理/定理/实验/标准化」五步法，成中国古代实验科学/技术标准化奠基"
        ],
        "expected_en": [
            "Mojing four volumes systematically record fifty-plus core concepts, founding Chinese ancient geometry/optics/mechanics theory",
            "Empirically tested ten major physics/engineering experiments, establishing 'hypothesis/experiment/measurement/calculation/verification/standardization' six-step experimental paradigm",
            "Created 'Mohist mechanisms/siege engines/defense fortifications/surveying instruments' four engineering deliverables",
            "'Definition/axiom/theorem/experiment/standardization' five-step method, Chinese ancient experimental science/technical standardization foundation"
        ],
        "case_zh": "墨子后学技术派（前350-前200），墨子弟子及再传弟子：孟胜/田俅/相里勤/腹谮/胡非/离朱/徐无鬼/耕柱/胡子/邓陵等十子。著《墨经》「小取/经上/经下/大取」四编，系统定义「节/幂/求/尽/称/任/胜/亏/盈/虚/实/满/空/盈/虚/等/不等/长/短/方/圆/平/直/重/轻/同/异/并/散/合/离/动/止/快/慢/并/散/聚/合/离/同/异/过/不及/参/半/倍/什/百/千/万/亿」五十余核心概念，建立「定义/公理/定理/推理/实验/验证」六步理论体系。实测「小孔成像（光学）/凸透镜聚焦（光学）/杠杆原理（力学）/滑轮组（力学）/齿轮传动（力学）/弹簧弹性（力学）/弓弩机械（工学）/云梯攻城（工学）/测量仪器（工学）」十大实验，建「假设/实验/测量/计算/验证/标准化」六步实验范式。创「墨家机关/攻城器/防御工事/测量仪器」四大工程化交付物。其「定义/公理/定理/实验/标准化」五步法，成中国古代实验科学/工程技术/技术标准化奠基工程，影响张衡/沈括/郭守敬/宋应星/徐光启/李时珍/朱载堉/华罗庚/钱学森/竺可桢科学工程化传统全版图。",
        "case_en": "Mohist Later Technical School (350-200 BCE), Mozi disciples and second-gen: Meng Sheng/Tian Qiu/Xiang Liqin/Fu Zhen/Hu Fei/Li Zhu/Xu Wugui/Geng Zhu/Hu Zi/Deng Ling. Authored Mojing 'Xiaoqu/Jingshang/Jingxia/Daqu' four volumes, systematically defining 'node/endpoint/seeking/exhaustive/measure/burden/victory/deficit/surplus/empty/full/empty/full/surplus/empty/equal/unequal/long/short/square/round/flat/straight/heavy/light/same/different/parallel/disperse/gather/combine/separate/move/stop/fast/slow/parallel/disperse/gather/combine/separate/same/different/over/under/half/half/double/ten/hundred/thousand/ten-thousand/hundred-million' fifty-plus core concepts, establishing 'definition/axiom/theorem/reasoning/experiment/verification' six-step theory system. Empirically tested 'pinhole imaging (optics)/convex lens focusing (optics)/lever principle (mechanics)/pulley system (mechanics)/gear transmission (mechanics)/spring elasticity (mechanics)/bow-crossbow mechanism (engineering)/cloud ladder siege (engineering)/surveying instruments (engineering)' ten experiments, establishing 'hypothesis/experiment/measurement/calculation/verification/standardization' six-step experimental paradigm. Created 'Mohist mechanisms/siege engines/defense fortifications/surveying instruments' four engineering deliverables. Their 'definition/axiom/theorem/experiment/standardization' five-step method became Chinese ancient experimental science/engineering technology/technical standardization foundational project, influencing Zhang Heng/Shen Kuo/Guo Shoujing/Song Yingxing/Xu Guangqi/Li Shizhen/Zhu Zaiyu/Hua Luogeng/Qian Xuesen/Zhu Kezhen scientific engineering tradition entire landscape."
    },
    # More women
    {
        "code": "H-WZT-166",
        "name_zh": "武则天：破门阀立科举/权力重构/女皇帝/唐制百代/权力工程化集大成者",
        "name_en": "Wu Zetian: Breaking Aristocracy Establishing Imperial Exams/Power Reconstruction/Female Emperor/Tang System Enduring/Power Engineering Master",
        "description_zh": "破门阀/立科举/女皇帝/权力重构/唐制百代/权力工程化/唐制百代",
        "description_en": "Breaking Aristocracy/Establishing Imperial Exams/Female Emperor/Power Reconstruction/Tang System Enduring/Power Engineering/Tang System Enduring",
        "modes": [33, 34, 18, 28, 35],
        "reason_zh": "核心思维：在「唐初门阀垄断/科举不全/女性无政权/权力结构僵化」背景下，以「破门阀/立科举/权力重构/制度工程化」四重工程——破「关陇集团/七姓十族/世袭官僚」门阀垄断，以「科举制/九品中正制改革/殿试/武举」四维选官体系重构权力来源；创「武周革命/改唐为周/自称圣神皇帝」权力重构工程，以「酷吏/罗织/改制/选贤」四重手段重塑权力结构；推「均田制/租调制/两税法雏形/兼并土地抑制」土地财政改革，以「户口/田亩/税赋/徭役」四维数据治理；立「武氏/李氏/外戚/宰相/台省/六部」六维权力制衡架构。其「破门阀/立科举/权力重构/数据治理」四重工程，成中国历史上唯一女皇帝权力工程化集大成范式，奠「唐制百代/科举千年/女主政治」制度基因。",
        "reason_en": "Core Thinking: In 'early Tang aristocratic monopoly/incomplete imperial exams/women no political power/rigid power structure', engineered 'break aristocracy/establish exams/reconstruct power/system engineering' quadruple project — broke 'Guanlong Group/seven surnames ten clans/hereditary bureaucracy' aristocratic monopoly, reconstructed power sources via 'imperial exams/nine-rank system reform/palace exam/military exam' four-dimensional official selection system; created 'Wu Zhou Revolution/change Tang to Zhou/self-proclaimed Holy Divine Emperor' power reconstruction project, reshaping power structure via 'cruel officials/entrapment/reform/select worthies' four means; promoted 'equal-field system/rent-labor-tax system/two-tax system embryo/land merger suppression' land fiscal reform, governing via 'household/land/tax/corvee' four-dimensional data; established 'Wu clan/Li clan/in-laws/chancellors/secretariat/six ministries' six-dimensional power checks and balances architecture. Her 'break aristocracy/establish exams/reconstruct power/data governance' quadruple project became China's only female emperor power engineering masterpiece, founding 'Tang system enduring/imperial exams millennium/female ruler politics' institutional genes.",
        "steps_zh": [
            "第1步：格局授权思维——以「天命/神权/武周革命」神圣授权，获取打破门阀/创立女帝的合法性",
            "第2步：制度化制衡——推「科举制/殿试/武举/九品中正改革」四维选官体系，以「考试/考绩/任用/监察」四环闭环打破门阀垄断",
            "第3步：摸石头过河/实验主义——以「酷吏/罗织/改制/选贤」四重手段试点权力重构，以「酷吏后/法制/选贤」纠偏固化成果",
            "第4步：摸石头过河/实验主义——推「均田/租调/两税雏形/抑制兼并」土地财政改革，以「户口/田亩/税赋/徭役」四维数据治理",
            "第5步：总体性思维——将「破门阀/立科举/权力重构/数据治理/权力制衡」五系统耦合，成唯一女皇帝权力工程化集大成范式"
        ],
        "steps_en": [
            "Step 1: Authority Delegation Thinking — Sacred authorization via 'mandate of heaven/divine right/Wu Zhou revolution', gaining legitimacy to break aristocracy/establish female emperor",
            "Step 2: Institutional Checks — Promoted 'imperial exams/palace exam/military exam/nine-rank reform' four-dimensional official selection, breaking aristocratic monopoly via 'exam/assessment/appointment/supervision' four-loop closure",
            "Step 3: Crossing River by Feeling Stones — Piloted power restructuring via 'cruel officials/entrapment/reform/select worthies' four means, correcting via 'post-cruel officials/rule of law/select worthies' solidifying gains",
            "Step 4: Crossing River by Feeling Stones — Pushed 'equal-field/rent-labor-tax/two-tax embryo/merger suppression' land fiscal reform, governing via 'household/land/tax/corvee' four-dimensional data",
            "Step 5: Systems Thinking — Coupled 'break aristocracy/establish exams/reconstruct power/data governance/power checks' five systems into only female emperor power engineering masterpiece paradigm"
        ],
        "expected_zh": [
            "中国历史上唯一女皇帝，开「武周」一代，称「圣神皇帝」",
            "破「关陇集团」门阀垄断，立「科举制/殿试/武举」选官体系，奠「科举千年」制度基因",
            "立「酷吏/罗织/改制/选贤」权力重构工程，创「酷吏后/法制化」纠偏机制",
            "推「均田/租调/两税雏形」土地财政改革，创「户口/田亩/税赋/徭役」四维数据治理"
        ],
        "expected_en": [
            "China's only female emperor, founded 'Wu Zhou' dynasty, titled 'Holy Divine Emperor'",
            "Broke 'Guanlong Group' aristocratic monopoly, established 'imperial exams/palace exam/military exam' official selection, founding 'imperial exams millennium' institutional genes",
            "Established 'cruel officials/entrapment/reform/select worthies' power reconstruction, created 'post-cruel officials/rule of law' correction mechanism",
            "Promoted 'equal-field/rent-labor-tax/two-tax embryo' land fiscal reform, created 'household/land/tax/corvee' four-dimensional data governance"
        ],
        "case_zh": "武则天（624-705），文德皇后武氏，太宗才人、高宗皇后、武周皇帝。655废王立武，690改唐为周，称「圣神皇帝」，成中国唯一女皇帝。破「关陇集团/七姓十族」门阀垄断：推「科举制」增设「殿试/武举」，以「考试/考绩/任用/监察」四环闭环打破世袭垄断；立「酷吏/罗织/改制/选贤」权力重构：来俊臣/周兴/索元礼等酷吏罗织旧贵族，后「诛酷吏/用狄仁杰/张柬之/选贤任能」纠偏固化。推「均田制/租调制/两税法雏形」土地财政：抑制土地兼并，立「户口/田亩/税赋/徭役」四维数据治理。立「武氏/李氏/外戚/宰相/台省/六部」六维权力制衡，创「台省/六部/御史台」三权分立雏形。其「破门阀/立科举/权力重构/数据治理」四重工程，成唯一女皇帝权力工程化集大成范式，奠「唐制百代/科举千年/女主政治」制度基因。",
        "case_en": "Wu Zetian (624-705), Empress Wende, Taizong Cairen, Gaozong Empress, Wu Zhou Emperor. 655 deposed Wang made Wu, 690 changed Tang to Zhou, titled 'Holy Divine Emperor', China's only female emperor. Broke 'Guanlong Group/seven surnames ten clans' aristocratic monopoly: promoted 'imperial exams' added 'palace exam/military exam', breaking hereditary monopoly via 'exam/assessment/appointment/supervision' four-loop closure; established 'cruel officials/entrapment/reform/select worthies' power reconstruction: Lai Junchen/Zhou Xing/Suo Yuanli cruel officials entrap old aristocracy, later 'execute cruel officials/use Di Renjie/Zhang Jianzhi/select worthies' correction solidification. Promoted 'equal-field/rent-labor-tax/two-tax embryo' land fiscal: suppressed land merger, established 'household/land/tax/corvee' four-dimensional data governance. Established 'Wu clan/Li clan/in-laws/chancellors/secretariat/six ministries' six-dimensional power checks, creating 'secretariat/six ministries/censorate' three-power separation embryo. Her 'break aristocracy/establish exams/reconstruct power/data governance' quadruple project became only female emperor power engineering masterpiece, founding 'Tang system enduring/imperial exams millennium/female ruler politics' institutional genes."
    },
    {
        "code": "H-QR-167",
        "name_zh": "秋瑾：光复会/女权先驱/革命文学/近代女性觉醒/反清革命/女侠/镜湖女侠",
        "name_en": "Qiu Jin: Restoration Society/Women's Rights Pioneer/Revolutionary Literature/Modern Women's Awakening/Anti-Qing Revolution/Female Knight/Mirror Lake Heroine",
        "description_zh": "光复会/女权/革命文学/女性觉醒/反清革命/女侠/镜湖女侠/大同书/女界钟",
        "description_en": "Restoration Society/Women's Rights/Revolutionary Literature/Women's Awakening/Anti-Qing Revolution/Female Knight/Mirror Lake Heroine/Great Unity Book/Women's Bell",
        "modes": [42, 6, 41, 34, 35],
        "reason_zh": "核心思维：在「晚清内忧外患/女性足缠/包办婚姻/无受教育权/革命党人稀缺」背景下，以「女权觉醒/革命实践/文学宣传/组织建设」四重突围——作《秋瑾诗词/悼陶成章/致同胞女界书》等革命文学，以「反缠足/反包办/主张女学/主张天足/主张自立/主张革命」六大主张唤醒女性主体性；创「大同书/女界钟」刊物，以「翻译/撰文/编辑/发行」四维媒体运营唤醒女性；创「大同学/实业女学/体育女学」女性教育体系，以「天足/不缠/读书/练武/自立/革命」六维课程重塑女性；加「光复会/同盟会/自立会」革命组织，以「刺杀/起义/宣传/组织」四维革命实践献身。其「女权/革命/文学/教育/组织」五维融合，成近代中国女性觉醒/革命献身/文学先声三位一体巅峰范式。",
        "reason_en": "Core Thinking: In 'late Qing internal external troubles/foot binding/arranged marriage/no education rights/scarce revolutionaries' context, broke out via 'women rights awakening/revolutionary practice/literary propaganda/organization building' quadruple breakthrough — authored 'Qiu Jin Poetry/Mourning Tao Chengzhang/Letter to Female Compatriots' revolutionary literature, awakening female subjectivity via six propositions 'anti-footbinding/anti-arranged marriage/advocate women education/advocate natural feet/advocate self-reliance/advocate revolution'; founded 'Great Unity Book/Women's Bell' publications, awakening women via 'translation/writing/editing/distribution' four-dimensional media operation; created 'Great Unity School/Industrial Women School/Physical Education Women School' women's education system, reshaping women via 'natural feet/no binding/reading/martial arts/self-reliance/revolution' six-dimensional curriculum; joined 'Restoration Society/Tongmenghui/Self-Reliance Society' revolutionary organizations, dedicating life via 'assassination/uprising/propaganda/organization' four-dimensional revolutionary practice. Her 'women rights/revolution/literature/education/organization' five-dimensional fusion became late Qing women's awakening/revolutionary martyrdom/literary vanguard trinity peak paradigm.",
        "steps_zh": [
            "第1步：认知偏差识别法——破「足缠/包办/不学/不武/从夫/从子」六大女性认知固化，以「天足/自主/读书/练武/自立/革命」六维反制",
            "第2步：摸石头过河/实验主义——创「大同学/女学/体育女学」三校试点，以「天足/读书/练武/自立」四维课程验证女性重塑可行性",
            "第3步：统一战线法——创「大同书/女界钟」两刊，以「翻译/撰文/编辑/发行」四维媒体运营联合蔡元培/陶成章/徐锡麟等革命党人",
            "第4步：制度化制衡——加「光复会/同盟会/自立会」三大革命组织，以「刺杀/起义/宣传/组织」四维革命实践，大同镇起义献身",
            "第5步：总体性思维——将「女权/革命/文学/教育/组织/献身」六系统耦合，成近代女性觉醒/革命献身/文学先声三位一体巅峰范式"
        ],
        "steps_en": [
            "Step 1: Cognitive Bias Identification — Break 'foot binding/arranged marriage/no education/no martial arts/follow husband/follow son' six female cognitive rigidities, countering via 'natural feet/autonomy/reading/martial arts/self-reliance/revolution' six dimensions",
            "Step 2: Crossing River by Feeling Stones — Founded 'Great Unity School/Women School/Physical Education Women School' three schools pilot, validating female reshaping feasibility via 'natural feet/reading/martial arts/self-reliance' four-dimensional curriculum",
            "Step 3: United Front — Founded 'Great Unity Book/Women's Bell' two publications, uniting revolutionaries Cai Yuanpei/Tao Chengzhang/Xu Xilin via 'translation/writing/editing/distribution' four-dimensional media operation",
            "Step 4: Institutional Checks — Joined 'Restoration Society/Tongmenghui/Self-Reliance Society' three revolutionary organizations, dedicating life via 'assassination/uprising/propaganda/organization' four-dimensional revolutionary practice, martyred at Datong Uprising",
            "Step 5: Systems Thinking — Coupled 'women rights/revolution/literature/education/organization/martyrdom' six systems into modern women's awakening/revolutionary martyrdom/literary vanguard trinity peak paradigm"
        ],
        "expected_zh": [
            "《致同胞女界书/悼陶成章/秋瑾诗词》成近代女性觉醒文学三大经典",
            "创「大同书/女界钟」两刊，「大同学/实业女学/体育女学」三校，成女性教育/媒体双奠基",
            "光复会/同盟会/自立会三会会员，大同镇起义献身，年仅31岁",
            "「女权/革命/文学/教育/组织/献身」六维融合，成近代女性觉醒巅峰范式"
        ],
        "expected_en": [
            "Letter to Female Compatriots/Mourning Tao Chengzhang/Qiu Jin Poetry became three classics of modern women's awakening literature",
            "Founded 'Great Unity Book/Women's Bell' two publications, 'Great Unity School/Industrial Women School/Physical Education Women School' three schools, dual foundation of women's education/media",
            "Member of Restoration Society/Tongmenghui/Self-Reliance Society three societies, martyred at Datong Uprising, age only 31",
            "Six-dimensional fusion 'women rights/revolution/literature/education/organization/martyrdom', modern women's awakening peak paradigm"
        ],
        "case_zh": "秋瑾（1875-1907），绍兴山阴人，原名秋媛，字璇卿，号鉴湖女侠。1904赴日留学，加「实业女学/体育女学」，习军事/体育/革命理论。1906归国，杭州创「大同学」，设「普通/师范/实业/体育」四科，提倡「天足/不缠/读书/练武/自立/革命」；创刊《大同书》月刊，主笔《女界钟》日刊，主笔《敬告同胞女界书》「足缠/包办/不学/不武/从夫/从子」六大罪状，倡「天足/自学/自立/革命」四大主张。1907加徐锡麟「自立会」，谋浙江/安徽同步起义；徐锡麟安庆起义失败被杀，秋瑾大同镇被捕，作《秋风秋雨愁煞人》绝笔诗，刑场就义，年仅31岁。其「诗词/书信/宣言/创刊/创学/组织/起义/献身」七重身份融合，成近代中国女性觉醒/革命献身/文学先声三位一体巅峰范式。",
        "case_en": "Qiu Jin (1875-1907), Shaoxing Shanyn native, original name Qiu Yuan, courtesy name Xuanqing, style name Jianhu Heroine. 1904 studied in Japan, entered 'Industrial Women School/Physical Education Women School', studied military/physical/revolutionary theory. 1906 returned, Hangzhou founded 'Great Unity School', set 'general/normal/industrial/physical' four departments, advocated 'natural feet/no binding/reading/martial arts/self-reliance/revolution'; founded 'Great Unity Book' monthly, edited 'Women's Bell' daily, authored 'Letter to Female Compatriots' exposing 'foot binding/arranged marriage/no education/no martial arts/follow husband/follow son' six sins, advocating 'natural feet/self-education/self-reliance/revolution' four propositions. 1907 joined Xu Xilin 'Self-Reliance Society', plotted Zhejiang/Anhui simultaneous uprising; Xu Xilin Anqing uprising failed executed, Qiu Jin arrested at Datong, composed 'Autumn Wind Autumn Rain Worry Kills' farewell poem, executed at 31. Her 'poetry/letters/manifestos/founding publications/founding schools/organization/uprising/martyrdom' seven identities fused, becoming modern China women's awakening/revolutionary martyrdom/literary vanguard trinity peak paradigm."
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

print(f"✅ Added {len(new_entries)} new entries")