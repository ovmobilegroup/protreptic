import json

# Load existing scenarios
with open('scenarios_en.json', 'r', encoding='utf-8') as f:
    scenarios_en = json.load(f)

# 8 final paradigm figures - English
new_en = {
    "H-GZ-60": {
        "name": "Guan Zhong: Hegemon Maker's State Machine Engineer",
        "description": "Assisted Duke Huan of Qi to Hegemony / Nine Alliances of Lords / Guanzi Light-Heavy Chapters / System Engineering / Incentive Design",
        "modes": [33, 19, 34, 40, 35],
        "reason": "Guan Zhong 'Respected Father', core mindset: systems engineering of hegemonic strategy — assisted Duke Huan of Qi, unified the realm once, nine alliances of lords, without chariots. Authored 'Guanzi' Light-Heavy Chapters, established 'Light-Heavy' economic regulation, 'Tithe Tax' system, 'Govern State by Rites' ritual system, 'Five Households as Xuan' grassroots governance. Transformed hegemony construction into replicable state operation code, became Spring-Autumn Hegemon Maker.",
        "steps": [
            "Step 1: Strategic Delegation — Assisted Duke Huan to Hegemony: 'Guan Zhong as Chancellor, Duke Huan Hegemon', clear ruler-minister division, chancellor power maximized",
            "Step 2: Marginal Thinking — Light-Heavy Regulation: 'Circulate surplus/deficit, stabilize prices, meet state needs', state regulates supply/demand, stabilizes prices",
            "Step 3: Institutional Checks — Grassroots Governance: 'Five households as Xuan, ten Xuan as Li, four Li as Lian, ten Lian as Xiang, ten Xiang as Bi, ten Bi as County', grassroots self-governance network",
            "Step 4: Incentive Mechanism — Clear Rewards Punishments: 'Merit rewarded above, crime punished below', appoint by merit, break aristocratic heredity",
            "Step 5: United Front — Respect King Repel Barbarians: 'Respect Zhou Court, Repel Four Barbarians', cohesion of lords through legitimacy, legitimacy construction"
        ],
        "expected": [
            "Duke Huan hegemony, nine alliances, one unification, institutionalized hegemony",
            "Guanzi Light-Heavy chapters became Chinese economics ancestor, grassroots governance template continued two thousand years",
            "Lessons: Guan Zhong died, Qi chaos, Duke Huan starved, system dependent on worthy minister, lacks self-correction mechanism"
        ],
        "case": "Guan Zhong Assisted Qi (685-645 BC): Duke Huan enthroned, Guan Zhong returned to Qi, three years Qi greatly governed. Light-Heavy: 'State poor then collect, state rich then disperse', state regulates grain/salt/currency prices. Tithe Tax: 'One in ten tax', replaced well-field system. Grassroots governance: Xuan-Li-Lian-Xiang-Bi-County five levels, self-governance/mutual-aid/supervision. Military Merit Rank: battle merit enfeoffment, broke hereditary nobility. Respect King Repel Barbarians: Zhaoling Meeting, Chu King asked about tripod, Duke Huan retreated him by ritual. Result: Qi Hegemon, Lords submit, Qi declined after Guan Zhong death."
    },
    "H-SQ-61": {
        "name": "Sima Qian: Historiography Methodology Founder of Ultimate Heaven-Human",
        "description": "Records of the Grand Historian / Biographical Style / Ultimate Heaven-Human Through Ancient-Modern Changes / Writing in Resentment / Humanistic Narrative",
        "modes": [22, 25, 29, 28, 35],
        "reason": "Sima Qian 'Investigate Heaven-Human boundary, penetrate ancient-present changes, form one school of thought', core mindset: historiographical narrative methodological self-awareness and humanistic concern — created Biographical Style (Basic Annals/Hereditary Houses/Biographies/Treatises/Tables), 'investigate the obscure, probe the profound', 'narrate not create', 'write in resentment'. Maps individual fate onto era changes, establishes historian subjectivity through 'Grand Historian Self-Prefation'.",
        "steps": [
            "Step 1: Abstract Induction — Biographical Style Creation: Basic Annals/Hereditary Houses/Biographies/Treatises/Tables five forms, people-centered, events as threads, breaks chronological limitations",
            "Step 2: Systems Thinking — Ultimate Heaven-Human: Investigate Heaven-Human relationship, natural law & social development interaction, historical philosophy dimension",
            "Step 2: Holistic Thinking — Through Ancient Present Changes: Vertical penetrate three thousand years up-down, horizontal encompass politics/economy/culture/military, identify historical evolution laws",
            "Step 3: Thinking Mode Selection — Write in Resentment: 'King Wen confined expanded Zhou Changes, Confucius distressed made Spring Autumn', adversity transforms to creation",
            "Step 4: Thinking Mode Selection — Historian Subjectivity: 'Grand Historian Self-Prefation' establishes historian as active agent not passive recorder"
        ],
        "expected": [
            "'Records of Grand Historian' became Chinese historiography peak, biographical style continued two millennia",
            "'Investigate Heaven-Human'/'Through Ancient Present'/'Form One School' became historiography methodology three realms",
            "Lessons: Castration trauma/individual vs power/historical truth vs political pressure"
        ],
        "case": "Records of Grand Historian (104-91 BC): Sima Qian inherited father Sima Tan 'Grand Historian' post, suffered castration for defending Li Ling, 'not yet completed my work, death not in my heart'. 130 chapters, 520k characters: 12 Basic Annals, 10 Tables, 8 Treatises, 30 Hereditary Houses, 70 Biographies. Biographical style: people as center, events as thread. 'Investigate Heaven-Human, penetrate ancient present, form one school'. Self-preface: 'Investigate Heaven-Human boundary, penetrate ancient present changes, become one school'. Result: Biographical style continued two millennia, 'investigate heaven-human/through ancient present/form one school' became historiography three realms."
    },
    "H-ZX-62": {
        "name": "Zhu Xi: Neo-Confucianism Systematizer of Cognitive Framework",
        "description": "Neo-Confucianism Compendium / Investigate Things Extend Knowledge / Four Books Chapter Annotations / Knowledge System Construction",
        "modes": [22, 25, 18, 28, 35],
        "reason": "Zhu Xi 'investigate things to extend knowledge, knowledge complete then intention sincere', core mindset: Neo-Confucianism system building and cognitive framework standardization — authored 'Neo-Confucianism Compendium', 'Four Books Chapter Annotations', established 'Investigate Things Extend Knowledge -> Sincere Intention -> Rectify Mind -> Cultivate Self -> Regulate Family -> Govern State -> Pacify World' cognitive chain. 'Investigate Things' as epistemological starting point, 'Extend Knowledge' as cognitive deepening, built complete ontology/epistemology/methodology system. 'Zhu Xi Learning' became imperial examination standard 600+ years.",
        "steps": [
            "Step 1: Abstract Induction — Principle Qi Theory: 'Principle one, manifestations many', 'Qi as vessel, Principle as master', built ontological foundation",
            "Step 2: Systems Thinking — Investigate Things Extend Knowledge: 'Investigate things to extend knowledge, knowledge complete then intention sincere', cognitive chain: things->knowledge->intention->mind->self->family->state->world",
            "Step 3: Management by Objectives — Four Books Standardization: 'Great Learning/Doctrine of Mean/Analects/Mencius' chapter annotations, unified thought standard, imperial exam standard 600+ years",
            "Step 4: Thinking Mode Selection — Method of Reading: 'Read thoroughly, think deeply', 'step by step, read thoroughly think deeply', cognitive methodology",
            "Step 5: Dormant Accumulation — Late Year Compilation: 'Reflections on Things at Hand' with Lu Zuqian, 'Zhu Xi Language Classified', 'Song Yuan Learning Cases', knowledge system late-year fixed"
        ],
        "expected": [
            "'Four Books Chapter Annotations' became imperial exam standard 600+ years, 'Zhu Xi Learning' official orthodoxy",
            "Principle Qi/Investigate Things/Cognitive Chain built Chinese philosophy epistemology system",
            "Lessons: System closed/emphasize inner sage neglect outer king/late Ming Wang Yangming 'Mind Learning'反叛"
        ],
        "case": "Zhu Xi Neo-Confucianism (1130-1200): Zhu Xi youth studied Cheng Brothers Neo-Confucianism, middle age compiled 'Four Books Chapter Annotations', 'Reflections on Things at Hand' with Lu Zuqian, 'Song Yuan Learning Cases'. Principle Qi: 'Principle one manifestations many', 'Qi vessel Principle master'. Investigate Things: 'Investigate things extend knowledge', cognitive chain start. Four Books: Great Learning/Doctrine of Mean/Analects/Mencius chapter annotations, imperial exam standard 1313-1905. Song Yuan Learning Cases: compiled Cheng/Zhu/Zhang/Lu/Ye/Luo etc learning cases. Result: Zhu Xi Learning official orthodoxy 600+ years, Wang Yangming 'Mind Learning' rebellion."
    },
    "H-LZY-63": {
        "name": "柳宗元：政治改革思维的批判性写作者",
        "description": "封建论/非国语/辨诬/制度批判/公共政策/思想解放",
        "modes": [30, 31, 37, 28, 35],
        "reason": "柳宗元'此心常向日、不用看花开'，核心思维：制度批判与思想解放的批判性写作——永贞革新失败后贬柳州、著《封建论》破'周公制礼作乐'神话、论证郡县制优于封建制、《非国语》破'天命'神话、《辨诬》自辩政治清白。'天地无全功、圣贤无全能、万物无全用'、相对主义/历史主义/批判理性主义。",
        "steps": [
            "第1步：认知偏差识别法——破封建神话：《封建论》'周公制礼作乐、非治天下之长策'、论证郡县制优于封建制、制度层面批判",
            "第2步：框架效应法——破天命神话：《非国语》'天之生民、必立之君、非为君生民也'、民本主义/契约论雏形",
            "第3步：知行合一——辨诬自明：永贞革新失败、贬柳州、《辨诬》逐条驳斥诬陷、思想清白、知识分子尊严",
            "第4步：自然选择法——思想相对主义：'天地无全功、圣贤无全能、万物无全用'、否定绝对真理/绝对权威/绝对完美",
            "第5步：蛰伏积势——柳州治理：柳州刺史、兴水利/办学堂/医百姓/平蛮乱/《柳河东集》传世、知行合一"
        ],
        "expected": [
            "《封建论》成中国制度批判经典、《辨诬》成知识分子尊严宣言",
            "相对主义/历史主义/批判理性主义成中国思想解放源头",
            "教训：改革失败/贬谪生涯/晚年孤独/思想超前未被采纳"
        ],
        "case": "封建论（803）：柳宗元永贞革新失败贬邵州、后徙柳州。《封建论》'三代已上、治出于一；三代已下、治出于二'、论证郡县制优于封建制、破'周公制礼作乐'神话。非国语（805）：'天之生民、必立之君、非为君生民也'、民本主义/契约论雏形。辨诬（814）：逐条驳斥'柳宗元谋反/附会革新党'诬陷、思想清白。柳州治理：兴水利/办学堂/医百姓/平蛮乱/《柳河东集》传世。结果：制度批判/民本思想/相对主义成中国思想解放源头。"
    },
    "H-WFZ-65": {
        "name": "王夫之：历史循环论的实学巨擘",
        "description": "船山遗书/读通鉴论/历史循环律/实学精神/本土现代性",
        "modes": [7, 1, 23, 28, 35],
        "reason": "王夫之'兴、者、其、其、其、其、衰、者、其、其、其、其'，核心思维：历史循环律与实学精神的本土现代性——明亡清立后隐居著述，《船山遗书》百卷、《读通鉴论》论历史循环律。'治天下者、不患人之不我信、患吾不能信人'、'势、非天也、非地也、人为之也'。'六经注我、我注六经'、实学精神/经世致用/反对空谈性命。",
        "steps": [
            "第1步：战略预判法——历史循环律：'兴、者、其、其、其、其、衰、者、其、其、其、其'、周期性/必然性/人为可控/识别兴衰节点",
            "第2步：矛盾分析法——势非天非地人为：'势、非天也、非地也、人为之也'、历史进程人为可塑、非宿命论",
            "第3步：自然选择法——六经注我我注六经：'六经注我、我注六经'、经典解释权回归主体、建立主体性解释学",
            "第4步：抽象归纳法——实学精神：'治天下者、不患人之不我信、患吾不能信人'、反对空谈性命/经世致用/实学为本",
            "第5步：蛰伏积势——船山遗书百卷：明亡清立后隐居石船山、著《船山遗书》《读通鉴论》《黄书》《楚辞集注》百卷、精神独立"
        ],
        "expected": [
            "历史循环律/势论/实学精神/本土现代性成中国近代思想三大资源",
            "影响谭嗣同/梁启超/毛泽东/近代启蒙/革命/现代化思想",
            "教训：明亡痛定思痛/理论封闭/缺制度设计/晚年孤独"
        ],
        "case": "读通鉴论（1660s）：王夫之读司马光《资治通鉴》作论、论历史循环律。兴：'其生也、勤俭敬畏、其衰也、奢侈骄淫'、周期律。势：'势、非天也、非地也、人为之也'、历史人为可塑。六经注我：'六经注我、我注六经'、主体性解释学。实学：'治天下者、不患人之不我信、患吾不能信人'、经世致用。船山遗书：百卷/经/史/子/集/哲学/文学/史学/全覆盖。结果：历史循环律/实学/本土现代性成近代思想资源。"
    },
    "H-CYK-66": {
        "name": "陈寅恪：独立精神自由思想的学术方法论大师",
        "description": "独立之精神自由之思想/考据与解释/柳如是别传/元白诗笺/学术方法论",
        "modes": [37, 22, 25, 28, 35],
        "reason": "陈寅恪'独立之精神、自由之思想'、核心思维：学术方法论的独立性与自由度——'考据与解释'双轮驱动、'不盲从权威、不盲从经典、不盲从习惯'。《柳如是别传》史料/文学/哲学三位一体、《元白诗笺证稿》诗史互证、《隋唐制度渊源略论》制度演变。《金明馆丛稿二编》'吾平生事业、在此二书'、《陈寅恪先生访谈录》'独立之精神、自由之思想'。",
        "steps": [
            "第1步：知行合一——考据与解释双轮：考据（史料搜集/考证/辨伪存真）、解释（理论建构/意义阐释/现代转换）、双轮驱动/缺一不可",
            "第2步：系统思维法——独立精神自由思想：'不盲从权威、不盲从经典、不盲从习惯'、学术自主性/思想自由度/方法论自觉",
            "第3步：抽象归纳法——柳如是别传/元白诗笛：史料/文学/哲学三位一体/诗史互证/制度演变/微观史写法/大历史视野",
            "第4步：思维模式选择——学术方法论传承：'吾平生事业、在此二书'、师承王国维/罗振玉/决裂罗振玉/师承陈垣/培养余嘉锡/叶榭/徐复观/高明/学术薪火相传",
            "第5步：蛰伏积势——晚年反思：'吾平生所受于先生者、推而广之'、师承王国维/决裂罗振玉/津门病逝/遗嘱'必不使中国亡于吾手'、精神遗产"
        ],
        "expected": [
            "《柳如是别传》/《元白诗笺证稿》/《隋唐制度渊源略论》成学术经典",
            "独立精神/自由思想/考据解释双轮/学术薪火相传成中国学术方法论标杆",
            "教训：晚年眼盲/家国破碎/学术孤独/独立精神代价高昂"
        ],
        "case": "柳如是别传（1950s）：陈寅恪晚年口述、罗纮整理。柳如是：秦淮名妓/钱谦益妻/明清易代/忠贞/才情/悲剧。史料：诗词/书信/传记/档案/墓志/三位一体。文学：才女/诗词/书画/风流。哲学：忠义/节操/女性/命运/时代。元白诗笺（1930s）：元稹/白居易诗作/史料/考证/互证/制度演变/诗史互证。隋唐制度渊源略论（1940s）：三省六部/九寺五监/选举/赋税/兵制/制度演变/制度史学。结果：独立精神/自由思想/考据解释双轮成中国学术方法论标杆。"
    },
    "H-QM-68": {
        "name": "钱穆：中国史治史方法论的文化重心论者",
        "description": "国史大纲/治史三要/文化重心/中国历代政治得失/通识教育",
        "modes": [22, 25, 38, 28, 35],
        "reason": "钱穆'识大体、知纲领、通古今之变'，核心思维：治史方法论与文化重心论的双重贡献——《国史大纲》'文化重心下移'（士大夫→士绅→平民/政治/经济/文化三维互证）、《中国历代政治得失》汉/唐/宋/明/清五代政治得失/制度演变/得失互补、《治史三要》'识大体、知纲领、通古今之变'治史三要。'读史使人明智'、'读中国史、使人爱中国'、通识教育先驱。",
        "steps": [
            "第1步：抽象归纳法——文化重心下移：士大夫→士绅→平民/政治/经济/文化三维互证/文化重心作为历史分期核心指标",
            "第2步：系统思维法——国史大纲体系：先秦/秦汉/魏晋南北朝/隋唐/宋元/明清/六大篇/文化重心/政治/经济/社会/思想/五维互证",
            "第3步：自然选择法——治史三要：'识大体、知纲领、通古今之变'、治史方法论三要素/大体/纲领/变迁",
            "第4步：反馈回路法——中国历代政治得失：汉/唐/宋/明/清五代/选举/赋税/兵制/得失互补/制度演变/无完美制度/动态权衡",
            "第5步：蛰伏积势——晚年迁台/传承：晚年迁台/《八十忆双亲》/师生薪火/余英时/高华/许倬云/葛兆光/学术薪火相传"
        ],
        "expected": [
            "《国史大纲》/《治史三要》/《中国历代政治得失》成中国史学三大基石",
            "文化重心下移/治史三要/得失论成中国史学三大方法论基石",
            "教训：文化保守主义/晚年迁台/政治倾向争议/学术与政治张力"
        ],
        "case": "国史大纲（1940s）：文化重心下移：士大夫→士绅→平民/政治/经济/文化三维互证。治史三要（1950s）：'识大体、知纲领、通古今之变'。中国历代政治得失（1952）：汉/唐/宋/明/清五代/选举/赋税/兵制/得失互补/制度演变/无完美制度/动态权衡。晚年迁台（1967）：《八十忆双亲》/师生薪火/余英时/高华/许倬云/葛兆光。结果：治史方法论/文化重心/得失论成中国史学三大基石。"
    },
    "H-LQC-67": {
        "name": "梁启超：新史学与变法思维的启蒙先驱",
        "description": "中国历史研究法/新民说/变法维新/饮冰室合集/启蒙思想",
        "modes": [22, 25, 38, 28, 35],
        "reason": "梁启超'少年中国说'、'新民说'、'中国历史研究法'，核心思维：新史学方法论与变法启蒙的双重突破——著《中国历史研究法》创'新史学'：'史者、考之于古、以验之今、以征之未来'。《新民说》'欲新中国、必先新民'、公民意识/公德/公共精神。《饮冰室合集》百卷、戊戌变法/百日维新/谭嗣同/谭延闿/徐佛苏/逃亡日本/办《清议报》《新民丛报》。'革命非杀人放火、革命乃旧制改良'。",
        "steps": [
            "第1步：抽象归纳法——新史学三纲：'史者、考之于古、以验之今、以征之未来'、考/验/征三步法/史学功能再定位",
            "第2步：系统思维法——新民说体系：新民/新道德/新学问/新宗教/新文学/新艺术/新生活/新国家/全方位新民培育/公民社会建构",
            "第3步：自然选择法——变法实践：戊戌变法/强学会/时务报/当官/逃亡/办报/新民丛报/启蒙/激进/保守/三派博弈/百日维新/六君子/流亡",
            "第4步：反馈回路法——饮冰室合集：百卷/诗文/论说/史学/哲学/政治/文学/自述/反思/百年再版/影响鲁迅/胡适/毛泽东/启蒙一代",
            "第5步：蛰伏积势——晚年反思：'吾以所受于先生者、推而广之'、师承康有为/决裂康有为/津门病逝/遗嘱'必不使中国亡于吾手'、精神遗产"
        ],
        "expected": [
            "《中国历史研究法》成新史学纲领/《新民说》成启蒙运动纲领/《饮冰室合集》成近代思想宝库",
            "新史学/新民说/变法/启蒙四大贡献/影响鲁迅/胡适/毛泽东/一代知识分子",
            "教训：激进与保守张力/变法失败/流亡生涯/思想转向复杂/晚年佛教倾向"
        ],
        "case": "中国历史研究法（1922）：'考之于古、验之于今、征之于未来'、三步法/新史学纲领。新民说（1902）：新民/新道德/新学问/新宗教/新文学/新艺术/新生活/新国家/全方位新民。戊戌变法（1898）：强学会/时务报/百日维新/六君子/梁逃日本。饮冰室合集（1920s-1930s）：百卷/诗文/论说/史学/哲学/政治/文学/自述/反思。晚年：'吾以所受于先生者、推而广之'、决裂康有为/津门病逝。结果：新史学/新民说/变法/启蒙四大贡献、影响鲁迅/胡适/毛泽东一代知识分子。"
    }
}

# Add to Chinese scenarios
scenarios_zh.update(new_zh)

# Save
with open('scenarios_zh.json', 'w', encoding='utf-8') as f:
    json.dump(scenarios_zh, f, ensure_ascii=False, indent=2)

print(f"Updated scenarios_zh.json: {len(scenarios_zh)} total scenarios")