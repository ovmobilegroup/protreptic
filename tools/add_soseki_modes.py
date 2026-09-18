import json

with open('modes_data.json', 'r') as f:
    modes = json.load(f)

zh_modes = modes.get('zh', {})
en_modes = modes.get('en', {})

# Add 4 new modes for Soseki
new_modes = {
    '460': {
        'zh': ['猫视角文明解构', '以非人视角(猫)观察人类文明，通过拟人化讽刺将读者置于旁观者位置，解构明治文明的虚伪、荒谬与病理：洋装和服混穿、盲目崇洋、官僚腐败、知识分子迷茫。', '旁观者置换\u2192拟人化讽刺\u2192病理暴露\u2192反讽觉醒', '《我是猫》第一章：吾輩は猫である。猫眼观人类：主子珍野苦肉、梅子装西洋、迷羊学者、暴力教师\u2014全景式文明病理切片。'],
        'en': ['Cat Perspective Civilization Deconstruction', 'Observe human civilization through non-human (cat) perspective, using anthropomorphic satire to place reader as observer, deconstructing Meiji civilization hypocrisy, absurdity, pathology: Western-Japanese clothing mix, blind Western worship, bureaucratic corruption, intellectual confusion.', 'Observer substitution\u2192anthropomorphic satire\u2192pathology exposure\u2192ironic awakening', 'I Am a Cat Ch1: Wagahai wa neko de aru. Cat observes humans: master Kushami\u306e苦肉, wife Mei Westernized, scholar Meitei, violent teacher \u2014 panoramic civilization pathology slices.']
    },
    '461': {
        'zh': ['近代自我心理解剖', '通过心理实验小说完成近代主体性的拓扑解剖：师生背叛(清/津田)、父子断裂(K与父亲)、夫妻疏离(K与静)三重背叛拓扑，暴露近代伦理在传统崩解后的真空与重组。自省式叙事将读者卷入共谋结构。', '三重背叛拓扑\u2192伦理真空暴露\u2192主体性重组\u2192自省共谋', '《心》三部曲：前篇师生(清自杀)、中篇父子(K回家)、后篇夫妻(K与静信任崩塌)。老师遗书式自白将K置于审判席与忏悔室双重位置。'],
        'en': ['Modern Self Psychological Anatomy', 'Complete topological anatomy of modern subjectivity through psychological experiment fiction: triple betrayal topology of teacher-student (Sensei/K), father-son (K/father), husband-wife (K/Shizu), exposing modern ethics vacuum and reconstruction after tradition collapse. Introspective narrative draws reader into complicity structure.', 'Triple betrayal topology\u2192ethics vacuum exposure\u2192subjectivity reconstruction\u2192introspective complicity', 'Kokoro trilogy: Part1 teacher-student (Sensei suicide), Part2 father-son (K returns home), Part3 husband-wife (K/Shizu trust collapse). Sensei confessional testament places K in dual judge/confessional positions.']
    },
    '462': {
        'zh': ['then-and-now文明批评', '留学英国(1900-1902)经历的文明冲击转化为比较文明学框架：then(江户传统)与now(明治西化)的张力分析，识别表层西化/深层传统分裂、形式理性/实质非理性悖论，构建知识分子介入公共领域的方法论。', '冲击体验\u2192张力分析\u2192分裂识别\u2192方法论构建', '1900-1902 伦敦两年神经衰弱：大英博物馆阅读vs汤晒街流浪。归国后《文学论》《文明当之何》确立：文明非直线进步而是传统与现代持续张力场。'],
        'en': ['Then-and-Now Civilization Critique', 'UK study (1900-1902) civilization shock transformed into comparative civilization framework: then (Edo tradition) vs now (Meiji Westernization) tension analysis, identifying surface-Westernization/deep-tradition split, formal-rationality/substantive-irrationality paradox, building intellectual public engagement methodology.', 'Shock experience\u2192tension analysis\u2192split identification\u2192methodology construction', '1900-1902 London two years neurasthenia: British Museum reading vs Thames embankment wandering. Post-return Literary Theory / Civilization What Now established: civilization not linear progress but continuous tradition-modernity tension field.']
    },
    '463': {
        'zh': ['私小说心理实验传统', '开创我小说(私小说)传统：心理实验与自传融合、以我为实验场、读者作为观察者/共谋者、语言即心理手术刀。确立日本近代文学内省主线，影响芥川龙之介、太宰治、村上春树、东野圭吾百年传承。', '自传为材\u2192心理为法\u2192我为场\u2192语为刀\u2192百年传承', '《我是猫》开篇即私小说雏形；《心》确立心理实验范式；《明暗》未完仍展示自我分裂极限。村上春树《挪威的森林》直承漱石私小说基因。'],
        'en': ['Shishosetsu Psychological Experiment Tradition', 'Founded I-novel (Shishosetsu) tradition: autobiography as material, psychology as method, self as laboratory, language as scalpel. Established introspective mainline of modern Japanese literature, influencing Akutagawa, Dazai, Murakami, Higashino century-long inheritance.', 'Autobiography as material\u2192psychology as method\u2192self as lab\u2192language as scalpel\u2192century inheritance', 'I Am a Cat embryonic shishosetsu; Kokoro established psychological experiment paradigm; unfinished Light and Darkness shows self-split limits. Murakami Norwegian Wood directly inherits Soseki shishosetsu genes.']
    }
}

with open('modes_data.json', 'r') as f:
    modes = json.load(f)

zh_modes = modes.get('zh', {})
en_modes = modes.get('en', {})

for mid, data in new_modes.items():
    zh_modes[mid] = data['zh']
    en_modes[mid] = data['en']

modes['zh'] = zh_modes
modes['en'] = en_modes

with open('modes_data.json', 'w') as f:
    json.dump(modes, f, ensure_ascii=False, indent=2)

print(f'Added modes 460-463. Total: zh={len(zh_modes)}, en={len(en_modes)}')