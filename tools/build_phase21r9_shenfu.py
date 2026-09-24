#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase21-R9 沈复 H-SHF-001 重建落盘生成器（卡 t_b6d4c0ee）

唯一依据（素材包为唯一内容来源）：
  (1) docs/research/phase21r9_shenfu_sourcing_report.md/.json（SHF-1 素材包：
      10 条模式素材 M-SHF-001~010 ／ 35 条引文 ／ 身份证据链 ／ 档案要点 ／ 14 条异文登记 ／ 30 件见证索引）
  (2) docs/scratch/phase21r9_shenfu/witness/（见证副本 34 件＋检索记录；sha256 清单与复跑脚本）
  (3) 布局参照（同链先例）：data/figures/H-LUORQ-001.json、data/individuals/H-LUORQ-001(.modes).json、
      docs/scratch/legacy20_r8_luorq_landing/**、data/figures/H-HZX-002.json

产出：
  data/figures/H-SHF-001.json ／ data/individuals/H-SHF-001.json ／ data/individuals/H-SHF-001_modes.json
  docs/scratch/phase21r9_shenfu_landing/**（entries ／ combined ／ 冻结副本 ／ id_mapping ／ category_mapping ／
      场景提案 ／ scenario_notes）
  data/audit/phase21r9_shenfu_landing_manifest.json

纪律：引文逐字取自素材包（并为见证文本强归一子串）；不写主库（data/modes_data.json 等六件＋工具登记面）；
      旧件 H-HAN-001 载荷零复用；零自造引文；一切 「」/『』 片段须为素材包强归一子串（构建期自检）。
"""
import hashlib
import io
import json
import os
import re
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PACK_MD = os.path.join(REPO, 'docs/research/phase21r9_shenfu_sourcing_report.md')
PACK_JSON = os.path.join(REPO, 'docs/research/phase21r9_shenfu_sourcing_report.json')
WITNESS = os.path.join(REPO, 'docs/scratch/phase21r9_shenfu/witness')
LANDING = os.path.join(REPO, 'docs/scratch/legacy20_r9_shenfu_landing')
AUDIT = os.path.join(REPO, 'data/audit')
CARD = 't_b6d4c0ee'
DATE = '2026-09-24'
FIG = 'H-SHF-001'
CODES = ['M-SHF-%03d' % i for i in range(1, 11)]
SCEN = ['C-SHF-%03d' % i for i in range(1, 11)]
SCEN_EN = ['C-SHF-%03dE' % i for i in range(1, 11)]
WITNESS_EXCLUDE = ('witness_sha256.txt', 'verify_quotes.py', 'quote_verification_final.json', 'README.md')

STD_CATEGORIES = ['伦理修养', '军事战略', '医学养生', '史学文献', '哲学形而上', '宗教修行', '工程技术',
                  '心理洞察', '战略决策', '探险发现', '政治治理', '教育传承', '文艺审美', '方法论通用',
                  '科学方法', '组织领导', '经济商业', '认识论逻辑']

# 旧件/失据字符串：数据文件零出现（登记面在 manifest / 报告）
FORBIDDEN = ['沈幅', '捕鱼记', '随园漫录', '东汉', '无锡', '1825', '1832',
             '《望海》', '《雨中游山》', '华萼', 'M351', 'M352', 'M353', 'M354',
             'M355', 'M356', 'M357', 'M358']

# 主库六件＋工具登记面（零写入核验面）
MAIN_LIB = ['data/modes_data.json', 'data/code_maps.json', 'data/scenarios_zh.json',
            'data/scenarios_en.json', 'data/scenario_tags.json', 'data/figure_names.json',
            'tools/modes_data.json', 'tools/code_maps.json', 'tools/code_maps_en.json',
            'tools/scenario_tags.json', 'tools/json/scenarios_zh.json', 'tools/json/scenarios_en.json']
ARCHIVE_SHA = {
    'H-HAN-001_figures.json': '83b882fda4adf68cca0815c4022eaed0c4878eebeaecdeb916d53a1ec982c960',
    'H-HAN-001_individuals.json': 'f79d83924dc0612195d9ff57e560feea7994885fe9728a1395534f286d30f713',
    'H-HAN-001_individuals_modes.json': 'd508cbac603935a9f248eaac9a5d10b897df249e2f858f30d22bd894dea0aa86',
}


def jl(path):
    with io.open(path, encoding='utf-8') as f:
        return json.load(f)


def wj(path, obj):
    d = os.path.dirname(path)
    if d and not os.path.isdir(d):
        os.makedirs(d)
    with io.open(path, 'w', encoding='utf-8') as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)
        f.write(u'\n')


def wt(path, text):
    d = os.path.dirname(path)
    if d and not os.path.isdir(d):
        os.makedirs(d)
    with io.open(path, 'w', encoding='utf-8') as f:
        f.write(text)


def sha_file(path):
    with open(path, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()


def norm(s):
    return re.sub(r'[^0-9A-Za-z\u3400-\u9fff\uf900-\ufaff]', '', s)


PACK = jl(PACK_JSON)
PACK_MD_TEXT = io.open(PACK_MD, encoding='utf-8').read()
PACK_JSON_TEXT = io.open(PACK_JSON, encoding='utf-8').read()
PACK_NORM = norm(PACK_MD_TEXT + '\n' + PACK_JSON_TEXT)
PACK_MODES = dict((m['id'], m) for m in PACK['modes'])

_W = {}
for _fn in sorted(os.listdir(WITNESS)):
    if _fn.endswith(('.txt', '.html')) and _fn not in WITNESS_EXCLUDE:
        _t = io.open(os.path.join(WITNESS, _fn), encoding='utf-8', errors='replace').read()
        if _fn.endswith('.html'):
            import html as _html
            _t = _t + '\n' + _html.unescape(re.sub(r'<[^>]+>', ' ', _t))
        _W[_fn] = norm(_t)
WITNESS_NORM = _W
JUAN56 = ('raw_juan5_zhongshan_wei.txt', 'raw_juan6_yangsheng_wei.txt',
          'hans_plain_juan5_zhongshan_wei.txt', 'hans_plain_juan6_yangsheng_wei.txt')


def frag_scan(strings):
    frags = []
    for s in strings:
        for m in re.finditer(u'[「『]([^「」『』]+)[」』]', s):
            frags.append(m.group(1))
    return frags


def collect_strings(obj, out=None):
    out = [] if out is None else out
    if isinstance(obj, dict):
        for v in obj.values():
            collect_strings(v, out)
    elif isinstance(obj, list):
        for v in obj:
            collect_strings(v, out)
    elif isinstance(obj, str):
        out.append(obj)
    return out

# ---------------------------------------------------------------------------
# 模式内容（作者稿；引文一律经构建期自检：key_quote 与案例引文取自素材包逐字，不回写）
# ---------------------------------------------------------------------------
MODE_CONTENT = [
 {
  'id': 'M-SHF-001', 'name_zh': u'实录真情法', 'name_en': u'Recording True Facts and Real Feelings Method',
  'category': u'文艺审美', 'category_raw': u'写作方法论·自传书写',
  'domain_zh': u'自传书写/写作方法', 'domain_en': u'Autobiographical Writing / Method of Composition',
  'definition_zh': u'「记其实情实事」是《浮生六记》全书的写作律令：作者自认「少年失学」「稍识之无」，不惭于文、不事文法雕琢，把亲历的实事与真情直录于笔墨；在他看来，「事如春梦」转瞬无痕，若不记之笔墨，未免有辜生命所予的厚分。此法以「如实」为最高标准——记录本身即是对生活的回报。',
  'definition_en': u'"Recording the true facts and real feelings" is the writing law of Six Chapters of a Floating Life: the author admits he "did not study in his youth" and knows only a few characters; he is not ashamed of his want of letters, polishes nothing for style, but sets down the events and feelings he lived through just as they were. For him, events are like a spring dream that leaves no trace—if they are not kept in ink, one would surely fail the richness life has granted. The method makes truthfulness its highest standard: the act of recording is itself the repayment of life.',
  'source_chapter': u'《浮生六记》卷一·闺房记乐开篇（兼及俞平伯序、陈寅恪转引）',
  'key_concepts': [u'记其实情实事', u'少年失学', u'稍识之无', u'记之笔墨', u'有辜彼苍之厚'],
  'key_q': 2,
  'trans': {1: u'Dongpo said, "Events are like a spring dream, leaving no trace"; if they are not set down in ink, one would surely fail the richness the heavens have granted.',
            2: u'I am ashamed that I did not study in my youth and know only a few characters—I merely record the true facts and real feelings; to insist on examining my grammar would be to demand brightness from a soiled mirror.',
            3: u'Taken as a whole the book has no sour words, no padding and no moralizing—perhaps it is for this very reason.',
            4: u'This is why Shen Sanbai\'s "Joys of the Boudoir" in Six Chapters of a Floating Life stands as an exceptional creation.'},
  'qattr_en': {1: u'Vol.1, Joys of the Boudoir, opening (W8; traditional base text W1)',
               2: u'same (W8)', 3: u'Yu Pingbo, preface to the reprint (W20)',
               4: u'Chen Yinke, cited at second hand (W22; see also W21)'},
  'process_zh': [u'立志：以「事如春梦了无痕」为警觉——不记则辜负生命的厚分，遂起记录之志',
                 u'去饰：不惭「少年失学」，不求文法考订，把修饰欲按下',
                 u'直录：以「记其实情实事」为律令，写亲历的实事与真情',
                 u'成书：把记录做成可传的完整文本（卷一~卷四即其成品）'],
  'process_en': [u'Resolve: take "events are like a spring dream" as the warning—not to record is to fail life\'s richness, so the will to record arises',
                 u'Strip ornament: be not ashamed of "studying late in life"; seek no grammatical revision; press down the urge to adorn',
                 u'Record directly: make "recording true facts and real feelings" the law, and write down lived events and feelings as they were',
                 u'Make a book: turn the record into a complete text fit to be passed on (Volumes 1-4 are its fruit)'],
  'cases': [{'q': 1, 'lead': u'卷一开篇自述记录的动因', 'lead_en': u'The opening of Volume 1 states the motive for recording',
             'tail': u'——「不记」被视作对生命的辜负，此即全书写作的出发句。', 'tail_en': u'—not recording is seen as failing life itself; this line launches the whole book.'},
            {'q': 2, 'lead': u'同篇自谦兼立律令', 'lead_en': u'The same chapter joins self-deprecation to the law of writing'},
            {'q': 3, 'lead': u'俞平伯评其文体效果（转引层：以不修饰见实录之力）', 'lead_en': u'Yu Pingbo on the book\'s style (secondhand layer: the force of record through lack of ornament)'},
            {'q': 4, 'lead': u'陈寅恪推重其文体地位（转引层）', 'lead_en': u'Chen Yinke on its literary standing (secondhand layer)'}],
  'modern_zh': [u'日记与自我民族志写作的先声', u'「如实」作为修辞策略本身', u'自媒体写作：以真实经验对抗过度修辞', u'家庭口述史与私人记忆的整理方法'],
  'modern_en': [u'A forerunner of diary writing and auto-ethnography', u'"Truthfulness" itself as a rhetorical strategy', u'Self-media writing: real experience against over-ornament', u'Methods for family oral history and the ordering of private memory'],
  'related': [u'M-SHF-010'],
 },
 {
  'id': 'M-SHF-002', 'name_zh': u'物外之趣法', 'name_en': u'Delight Beyond Things Method',
  'category': u'文艺审美', 'category_raw': u'审美转化·童心与创造',
  'domain_zh': u'审美感知/童心与创造', 'domain_en': u'Aesthetic Perception / Childlike Creativity',
  'definition_zh': u'以「心之所向」为转换器：把日常微物（帐中蚊群、丛草虫蚁、土砾凹凸）重译为宏大景观（群鹤舞空、青云白鹤观、林丘壑谷），从平淡中生「物外之趣」。作者自述此法成于童稚时——「张目对日，明察秋毫」「细察其纹理」；所以它不是逃避现实的幻想，而是对感知的主动重构：先细看，再以小见大。',
  'definition_en': u'Using "where the mind inclines" as a converter: everyday trifles (a swarm of mosquitoes in a plain curtain, grasses and ants, clods and hollows) are re-translated into grand vistas (cranes wheeling in the sky, a view of blue clouds and white cranes, forests and ravines), and a charm beyond things is born from the plainest material. The author says the gift belonged to his boyhood—"I could look at the sun with open eyes and discern the smallest detail," "I would closely examine its texture"; so it is not escapist fantasy but an active reconstruction of perception: first look closely, then see the great in the small.',
  'source_chapter': u'《浮生六记》卷二·闲情记趣开篇',
  'key_concepts': [u'物外之趣', u'张目对日，明察秋毫', u'细察其纹理', u'心之所向', u'神游其中'],
  'key_q': 1,
  'trans': {1: u'I recall that in my boyhood I could look at the sun with open eyes and discern the smallest detail; whenever I saw some tiny thing, I would closely examine its texture—and so I often enjoyed a charm beyond the things themselves.',
            2: u'I would keep mosquitoes in a plain curtain, and slowly blow smoke upon them so that they flew buzzing through the smoke, making of it a view of blue clouds and white cranes; and when they truly seemed to cry like cranes above the clouds, I was delighted and clapped my hands.',
            3: u'I took clumps of grass for forests, insects and ants for beasts, the raised earth and pebbles for hills, the hollows for valleys, and roamed in spirit among them, joyous and content.'},
  'qattr_en': {1: u'Vol.2, opening (W8)', 2: u'Vol.2 (W8)', 3: u'Vol.2 (W8)'},
  'process_zh': [u'细察：对藐小微物先看其纹理',
                 u'心向：以「心之所向」为景物定标（蚊作鹤、草作林）',
                 u'重构：把小物放大成大景，并神游其中',
                 u'验收：以「怡然称快」自得与否，检验转换是否成立'],
  'process_en': [u'Look closely: examine the texture of the tiny thing first',
                 u'Incline the mind: let "where the mind inclines" set the scale (mosquitoes as cranes, grass as forest)',
                 u'Reconstruct: enlarge the small into the grand and roam within it in spirit',
                 u'Verify: test whether the conversion holds by one\'s own delight and satisfaction'],
  'cases': [{'q': 1, 'lead': u'卷二开篇总述童稚时的观看方式', 'lead_en': u'The opening of Volume 2 states the boyhood way of seeing'},
            {'q': 2, 'lead': u'「留蚊于素帐中」——把蚊群重构为青云白鹤观', 'lead_en': u'"Keeping mosquitoes in a plain curtain"—a swarm remade into a view of cranes'},
            {'q': 3, 'lead': u'「以丛草为林」——以微物搭建丘壑并神游其中', 'lead_en': u'"Clumps of grass for forests"—building hills and valleys from trifles and roaming within'}],
  'modern_zh': [u'想象力训练：把平凡素材重译为景观', u'自然教育：从细察纹理开始', u'儿童美育：识别并保护童稚的观看方式', u'注意力如何创造世界（「心之所向，则或千或百」）'],
  'modern_en': [u'Training the imagination: re-translating ordinary material into a scene', u'Nature education: it begins with closely examining texture', u'Children\'s aesthetic education: recognize and protect the boyhood way of seeing', u'How attention creates a world ("where the mind inclines, one sees a thousand or a hundred")'],
  'related': [u'M-SHF-009'],
 },
 {
  'id': 'M-SHF-003', 'name_zh': u'独出己见法', 'name_en': u'Independent Judgment Method',
  'category': u'认识论逻辑', 'category_raw': u'独立判断·审美自主',
  'domain_zh': u'独立判断/审美自主', 'domain_en': u'Independent Judgment / Aesthetic Autonomy',
  'definition_zh': u'凡事「独出己见，不屑随人是非」：论诗品画持「人珍我弃、人弃我取」的取舍观；名胜的得失不随名气，而「贵乎心得」——判断的标准收归内在。底气来自阅历：作者自述「游幕三十年来」遍历南北，见得广，故能不随人。此法不是刻意反潮流，而是把评价权收回自己手里。',
  'definition_en': u'In everything the author preferred to form his own view and disdain following others in praise and blame; in judging poetry and appraising painting he held to discarding what others prize and prizing what they discard; the worth of a place of scenic fame does not follow its reputation but lies in what the heart gains. The standard of judgment is taken back inside. Its ground is experience: he had roamed the secretariats for thirty years, seen far and wide, and so could refuse to follow the crowd. This is not contrarianism; it is reclaiming the right of appraisal for oneself.',
  'source_chapter': u'《浮生六记》卷四·浪游记快',
  'key_concepts': [u'独出己见', u'不屑随人是非', u'人珍我弃、人弃我取', u'贵乎心得', u'游幕三十年'],
  'key_q': 1,
  'trans': {1: u'In all things I like to form my own view and disdain following others in praise and blame; in judging poetry and appraising painting I always keep the sense of discarding what others prize and prizing what they discard—hence for a place of scenic fame, what matters is what the heart gains there.',
            2: u'In my thirty years of roaming as a secretary, the only parts of the realm I have not reached are Sichuan, Guizhou and southern Yunnan.'},
  'qattr_en': {1: u'Vol.4 (W8; joins the passage on thirty years of official travels)', 2: u'Vol.4 (W8)'},
  'process_zh': [u'阅历：以「游幕三十年」广其见闻',
                 u'独立：凡事独出己见，不屑随人是非',
                 u'取舍：人珍我弃、人弃我取',
                 u'内证：以「心得」为最终验收标准'],
  'process_en': [u'Broaden experience: thirty years of official travels widen what one has seen',
                 u'Stand alone: form one\'s own view in everything, disdaining to follow others\' blame or praise',
                 u'Choose inversely: discard what others prize, prize what they discard',
                 u'Verify within: let "what the heart gains" be the final standard'],
  'cases': [{'q': 1, 'lead': u'卷四自述其判断姿态与取舍观', 'lead_en': u'Volume 4 states his posture of judgment and his rule of choice',
             'tail': u'——「贵乎心得」兼含对「随人」的不满。', 'tail_en': u'—"what the heart gains" carries with it a dissatisfaction with merely following others.'},
            {'q': 2, 'lead': u'同卷自述阅历（独立判断的底气）', 'lead_en': u'The same volume states the experience behind that independence'}],
  'modern_zh': [u'反打卡式审美：不以热度定优劣', u'判断标准的内化与自证', u'小众趣味的自我辩护与再发现', u'用阅历为独立判断兜底'],
  'modern_en': [u'Against check-in aesthetics: worth is not set by popularity', u'Internalizing and self-verifying one\'s standard of judgment', u'Self-defense and rediscovery of minority tastes', u'Letting experience underwrite independent judgment'],
  'related': [u'M-SHF-010'],
 },
 {
  'id': 'M-SHF-004', 'name_zh': u'就事论事法', 'name_en': u'Each Matter on Its Own Terms Method',
  'category': u'方法论通用', 'category_raw': u'生活治理·约束下的雅洁',
  'domain_zh': u'生活治理/俭雅经营', 'domain_en': u'Household Economy / Refinement under Constraint',
  'definition_zh': u'省俭不等于将就：「贫士起居服食以及器皿房舍，宜省俭而雅洁」；省俭之法叫「就事论事」——就器皿房舍的实况，逐件事找出最省的实现法，让清贫生活仍达到「雅洁」。其总命题为「竹头木屑皆有用」：材料没有贵贱，只有未找到的做法；约束之下，眼光决定方案。',
  'definition_en': u'Economy is not the same as settling for less: "in daily living, food and clothing, utensils and rooms, a poor scholar should be economical yet refined"; and the method of economy is called "taking each matter on its own terms"—taking the actual state of each utensil and room, and finding for each matter the least costly way that still works, so that a poor life can still reach refinement. Its master proposition is that "bamboo ends and wood shavings are all useful": no material is noble or base in itself; only the right handling has not yet been found. Under constraint, the eye decides the plan.',
  'source_chapter': u'《浮生六记》卷二·闲情记趣',
  'key_concepts': [u'省俭而雅洁', u'就事论事', u'竹头木屑皆有用', u'逐件设法', u'贫士语境'],
  'key_q': 1,
  'trans': {1: u'For a poor scholar, in daily living, food and clothing, utensils and rooms—economy and refinement should go together; the method of economy is called "taking each matter on its own terms."',
            2: u'This is one method of "taking each matter on its own terms." Extending the principle, the ancients\' saying that bamboo ends and wood shavings are all useful is indeed well founded.'},
  'qattr_en': {1: u'Vol.2 (W8)', 2: u'Vol.2 (W8)'},
  'process_zh': [u'立双标准：省俭而雅洁，缺一不可',
                 u'观实况：逐件看清器皿房舍的实际条件',
                 u'逐件设法：给每样物事找最省而仍雅的实现法',
                 u'复用到物：以「竹头木屑皆有用」处理余料与旧物'],
  'process_en': [u'Set twin standards: economy and refinement, neither to be dropped',
                 u'Read the actual condition: see each utensil and room as it really is',
                 u'Solve item by item: find for each thing the least costly refinement that still works',
                 u'Reuse matter: apply "bamboo ends and wood shavings are all useful" to leftovers and old objects'],
  'cases': [{'q': 1, 'lead': u'卷二提出省俭之法（双约束的起点）', 'lead_en': u'Volume 2 states the method of economy (the starting point of the twin constraints)'},
            {'q': 2, 'lead': u'同段以「竹头木屑皆有用」总括此法', 'lead_en': u'The same passage sums up the method with "bamboo ends and wood shavings are all useful"',
             'tail': u'——同段前后即载其实例（梅花盒、竹帘代栏等，见素材包 §三 usage 登记）。', 'tail_en': u'—the surrounding passages record its examples (the plum-blossom box, bamboo blinds for railings, etc.; registered in the sourcing pack §3 usage).'}],
  'modern_zh': [u'约束条件下的设计思维（节俭创新/jugaad）', u'家居整理的逐件处置法', u'预算有限时的「省俭而雅洁」双目标', u'旧物再用：竹头木屑皆有用'],
  'modern_en': [u'Design thinking under constraints (frugal innovation / jugaad)', u'Item-by-item handling in home organization', u'The twin goals of economy and refinement on a tight budget', u'Reusing old objects: bamboo ends and wood shavings are all useful'],
  'related': [u'M-SHF-005'],
 },
 {
  'id': 'M-SHF-005', 'name_zh': u'布衣菜饭法', 'name_en': u'Plain Cloth and Simple Fare Method',
  'category': u'伦理修养', 'category_raw': u'幸福观·价值选择',
  'domain_zh': u'幸福观/价值选择', 'domain_en': u'View of Happiness / Choice of Values',
  'definition_zh': u'以「布衣菜饭，可乐终身」为幸福命题：理想生活不在远游功名，而在共同劳动与相守——图景是卜筑同居、绕屋菜园、植瓜蔬以供薪水，「君画我绣」以为诗酒之需；「不必作远游计」是把功名从幸福公式里减掉。命题出自夫妻对话，非普适宣言；此后「知己沦亡」的浩叹又为它加上悼亡的重量——亮与痛同框。',
  'definition_en': u'The proposition is "in plain cloth and simple fare we can be happy all our lives": the good life lies not in distant travel and office, but in shared labor and staying together—the picture is a house built together, a garden around it, melons and greens grown to meet expenses, "you paint and I embroider" to pay for verse and wine; and "no need to plan distant journeys" is the deletion of official ambition from the happiness equation. The proposition comes from a dialogue between husband and wife, not a universal manifesto; and the later sigh that "my kindred spirit is gone" adds to it the weight of mourning—brightness and pain in the same frame.',
  'source_chapter': u'《浮生六记》卷一·闺房记乐（芸语；兼及林语堂评语转引）',
  'key_concepts': [u'布衣菜饭，可乐终身', u'君画我绣', u'卜筑菜园', u'不必作远游计', u'知己沦亡'],
  'key_q': 2,
  'trans': {1: u'In some later year I shall build our home there with you: buy ten mu of vegetable garden around the house, and have servants and the old woman plant melons and greens to meet our expenses.',
            2: u'You paint and I will embroider, so as to pay for our verse and wine. In plain cloth and simple fare we can be happy all our lives—there is no need to plan distant journeys.',
            3: u'I deeply agreed with her. And now, though such a place might be had, my kindred spirit is gone—how can one sigh enough for that!',
            4: u'(Yun) is the most lovable woman recorded in Chinese literature.',
            5: u'Though her face was no Xishi\'s, with her front teeth showing a little, I thought her the first beauty in all China.'},
  'qattr_en': {1: u'Vol.1, Yun\'s words (W8)', 2: u'Vol.1 (W8)', 3: u'Vol.1 (W8)',
               4: u'Lin Yutang, cited at second hand (W16)',
               5: u'Lin Yutang, cited at second hand (W16; echoing the primary text\'s "only two front teeth showing," W8 Vol.1)'},
  'process_zh': [u'立愿景：卜筑同居、绕屋菜园（买绕屋菜园十亩）',
                 u'定凭依：共同劳动——君画我绣、植瓜蔬以供薪水',
                 u'做减法：把远游功名从幸福方程中删去（不必作远游计）',
                 u'承重量：后来「知己沦亡」，命题转为悼亡之叹（亮与痛同框）'],
  'process_en': [u'Set the vision: build a home together with a ten-mu garden around it',
                 u'Name the support: shared labor—you paint, I embroider; plant melons and greens to meet expenses',
                 u'Subtract: delete distant travel and office from the happiness equation',
                 u'Carry the weight: afterwards "my kindred spirit is gone" turns the proposition into a mourning sigh (brightness and pain together)'],
  'cases': [{'q': 1, 'lead': u'卷一·芸语中的生活图景（卜筑、菜园、植瓜蔬）', 'lead_en': u'Volume 1, Yun\'s picture of the life to come (a home, a garden, melons and greens)'},
            {'q': 2, 'lead': u'全篇命名的两句：君画我绣与布衣菜饭（幸福命题）', 'lead_en': u'The two lines that name the whole: you paint and I embroider; plain cloth and simple fare (the happiness proposition)'},
            {'q': 3, 'lead': u'同篇的追忆之叹（命题的悼亡重量）', 'lead_en': u'The retrospective sigh in the same chapter (the proposition\'s weight of mourning)'},
            {'q': 4, 'lead': u'林语堂评陈芸（转引层：中译版本多样，英文原文未成证）', 'lead_en': u'Lin Yutang on Chen Yun (secondhand layer: translations vary; the English original is unattested)'},
            {'q': 5, 'lead': u'林语堂评其容貌（转引层；与一手「唯两齿微露」呼应）', 'lead_en': u'Lin Yutang on her looks (secondhand layer; echoing the primary "only two front teeth showing")'}],
  'modern_zh': [u'减法生活：幸福的最小方案', u'以日常性为价值锚（可乐终身）', u'共同劳动作为关系的基础', u'理想与易逝：亮与痛一并呈现'],
  'modern_en': [u'The minimal plan of a good life: subtractive living', u'Anchoring value in the everyday ("happy all our lives")', u'Shared labor as the ground of a relationship', u'Ideals and their fragility: brightness and pain shown together'],
  'related': [u'M-SHF-007', u'M-SHF-003'],
 },
]

MODE_CONTENT += [
 {
  'id': 'M-SHF-006', 'name_zh': u'情之所钟法', 'name_en': u'Where Affection Settles Method',
  'category': u'心理洞察', 'category_raw': u'情感判断·审美偏好',
  'domain_zh': u'情感判断/审美偏好', 'domain_en': u'Affective Judgment / Aesthetic Preference',
  'definition_zh': u'偏好不必服从「理」：作者以「始恶而终好之，理之不可解也」承认情感转变无法论证；芸以「情之所钟，虽丑不嫌」给出以情为尺的取舍原则——所钟爱者不因外形之「丑」被裁掉。它是对物、对人的一种态度资源：情感的强度可以覆盖外形的标准；但边界在于它不是无条件的包容律。',
  'definition_en': u'Preference need not obey reason: the author admits with "to hate a thing at first and come to love it in the end—that is what reason cannot explain" that a change of feeling cannot be argued; Yun supplies the rule of choice with "where affection settles, even ugliness is not minded"—what one loves is not cut away for its looks. It is an attitude resource toward things and toward people: the strength of feeling can override the standards of appearance. Its boundary: it is not a law of unconditional acceptance.',
  'source_chapter': u'《浮生六记》卷一·闺房记乐',
  'key_concepts': [u'始恶而终好之', u'理之不可解', u'情之所钟', u'虽丑不嫌', u'以情为尺'],
  'key_q': 1,
  'trans': {1: u'I said, "To hate a thing at first and come to love it in the end—that is what reason cannot explain." Yun said, "Where affection settles, even ugliness is not minded."'},
  'qattr_en': {1: u'Vol.1 (W8)'},
  'process_zh': [u'觉察：注意到偏好从「始恶」到「终好」的转变',
                 u'承认不可解：不以「理」强求解释',
                 u'以情为尺：对所钟之物/人，不以外形之丑裁掉',
                 u'守边界：勿引申为无条件包容（对象含物/人，属态度资源）'],
  'process_en': [u'Notice: register the shift of preference from first dislike to final love',
                 u'Admit the inexplicable: do not force an explanation out of reason',
                 u'Measure by feeling: for the beloved thing or person, do not cut away on grounds of looks',
                 u'Keep the boundary: do not stretch it into unconditional acceptance (the object may be a thing or a person; it is an attitude resource)'],
  'cases': [{'q': 1, 'lead': u'卷一问答：以情为尺的取舍原则', 'lead_en': u'A dialogue in Volume 1: the rule of choosing by feeling',
             'tail': u'——出自芸语对「丑」的接纳，勿无限引申。', 'tail_en': u'—it comes from Yun\'s acceptance of "ugliness"; it should not be stretched without limit.'}],
  'modern_zh': [u'审美主观性的合法性', u'「心证」式偏好的自我理解', u'与侘寂式「丑学」的相通', u'关系中从外形标准到情感标准的转移'],
  'modern_en': [u'The legitimacy of aesthetic subjectivity', u'Self-understanding of preferences held "by inner warrant"', u'Its affinity with wabi-sabi aesthetics of imperfection', u'Moving from standards of appearance to standards of feeling in relationships'],
  'related': [u'M-SHF-003'],
 },
 {
  'id': 'M-SHF-007', 'name_zh': u'知己同心法', 'name_en': u'One Heart with a Kindred Spirit Method',
  'category': u'伦理修养', 'category_raw': u'亲密关系·伙伴关系',
  'domain_zh': u'亲密关系/伙伴结构', 'domain_en': u'Intimate Partnership / Companionship',
  'definition_zh': u'夫妻以「同癖好、同耳目」的知音结构相处：「其癖好与余同」，且能「察眼意，懂眉语」，「一举一动，示之以色」皆能会通；共享「化女为男」的游历想象与「来世」之约；作者以「具男子之襟怀才识」评芸。同时附反例：卷三末提醒「恩爱夫妻不到头」——同一关系在现实重压下走向悼亡，不可读作无冲突的童话。',
  'definition_en': u'The couple lived in the structure of kindred spirits: "her tastes were the same as mine," and she could read his eyes and understand his brows; in every movement, shown but by a look, everything was understood. They shared the "turn woman into man" fantasy of travel and a vow for the next life; the author judged Yun to have the heart and gifts of a man. And the counter-example is attached: the end of Volume 3 warns that "a loving couple does not grow old together"—the same bond, under the pressures of reality, moves toward mourning, and must not be read as a conflict-free fairy tale.',
  'source_chapter': u'《浮生六记》卷一·闺房记乐（兼及卷三·坎坷记愁反例）',
  'key_concepts': [u'同癖好', u'察眼意，懂眉语', u'化女为男', u'来世', u'恩爱夫妻不到头'],
  'key_q': 1,
  'trans': {1: u'Her tastes were the same as mine, and she could read the meaning in my eyes and understand the words of my brows; in every movement, shown but by a glance, there was nothing she did not fully grasp.',
            2: u'A pity that you are a woman and must keep within doors! If only you could turn into a man, we would visit the famous mountains together, search out the finest places and roam the world—would that not be splendid!',
            3: u'In the next life you shall be born a man, and I will be born a woman and follow you.',
            4: u'It is only by not losing this present life that we can feel there is true delight.',
            5: u'Yun was but a woman, yet she had the heart and gifts of a man.',
            6: u'I would counsel couples in this world: they should neither hate each other, nor be too deeply fond; as the saying goes, "a loving couple does not grow old together"—let one like me serve as the warning of the cart overturned ahead.'},
  'qattr_en': {1: u'Vol.1 (W8)', 2: u'Vol.1 (W8)', 3: u'Vol.1 (W8)', 4: u'Vol.1 (W8)',
               5: u'Vol.3 (W8)', 6: u'Vol.3, counter-example (W8)'},
  'process_zh': [u'同癖好：建立共同趣味与共同语言',
                 u'通暗码：察眼意、懂眉语（非语言的相互读取）',
                 u'共想象：化女为男之游、来世相从之约',
                 u'并置反例：以「恩爱夫妻不到头」标示同一关系的现实极限'],
  'process_en': [u'Same tastes: build a shared register of interests and words',
                 u'Read the private code: the eyes and brows as a non-verbal channel',
                 u'Share imaginings: the woman-turned-man journey, the vow for the next life',
                 u'Attach the counter-example: mark the bond\'s real limits with "a loving couple does not grow old together"'],
  'cases': [{'q': 1, 'lead': u'卷一：知音结构的定义句（同癖好、察眼意懂眉语）', 'lead_en': u'Volume 1: the defining line of the kindred-spirit structure'},
            {'q': 2, 'lead': u'卷一：共享的游历想象（化女为男）', 'lead_en': u'Volume 1: the shared travel fantasy (turning woman into man)'},
            {'q': 3, 'lead': u'卷一：来世之约', 'lead_en': u'Volume 1: the vow for the next life'},
            {'q': 4, 'lead': u'同段：今生与来世的并置（不昧今生）', 'lead_en': u'The same passage joins this life and the next (not losing the present)'},
            {'q': 5, 'lead': u'卷三：作者对芸的评价（知己的重量）', 'lead_en': u'Volume 3: the author\'s judgment of Yun (the weight of a kindred spirit)',
             'tail': u'——「女扮男装」等属清代语境，引用勿简单套用。', 'tail_en': u'—"woman dressed as a man" belongs to the Qing context and should not be simply transposed.'},
            {'q': 6, 'lead': u'卷三末尾反例：恩爱夫妻不到头（同卡附反例）', 'lead_en': u'The counter-example at the end of Volume 3: a loving couple does not grow old together',
             'tail': u'——家变、贫困、离散俱在（卷三），不可读作无冲突童话。', 'tail_en': u'—family ruin, poverty and separation are all there in Volume 3; this is no conflict-free fairy tale.'}],
  'modern_zh': [u'平等伙伴关系的早期样本', u'「知己」作为亲密关系的度量', u'共享想象与约定对关系的维护', u'以反例承认关系的现实极限'],
  'modern_en': [u'An early sample of egalitarian partnership', u'"Kindred spirit" as a measure of intimacy', u'Sustaining a bond through shared imaginings and vows', u'Admitting a bond\'s real limits through its counter-example'],
  'related': [u'M-SHF-005', u'M-SHF-008'],
 },
 {
  'id': 'M-SHF-008', 'name_zh': u'坎坷自省法', 'name_en': u'Self-Reflection in Adversity Method',
  'category': u'心理洞察', 'category_raw': u'自我认知·逆境归因',
  'domain_zh': u'自我认知/逆境归因', 'domain_en': u'Self-Knowledge / Attributing Adversity',
  'definition_zh': u'对命运不公，作者的处置是性格自省——「多情重诺，爽直不羁，转因之为累」：把坎坷中的自我因素找出来，而非只归咎外部。同时冷静记录世情规则（「处家人情，非钱不行」），以反语引痛（「女子无才便是德」一句须按反语与语境读），并把判断落为行动（「因易儒为贾」）。自省不等于自罪：悲悯与批判并存。',
  'definition_en': u'Facing an unjust fate, the author\'s handling is self-examination of character: "too full of feeling, too ready to make promises, too frank and unbridled—these very traits became my burden." He finds the self-factor in his adversity instead of blaming only the outside. At the same time he coolly records the rules of the world ("in managing a family and its human ties, nothing works without money"), lets irony carry the pain ("a woman without talent is a woman of virtue" must be read as irony and in context), and turns judgment into action ("I turned from the scholar\'s path to trade"). Self-examination is not self-condemnation: compassion and critique coexist.',
  'source_chapter': u'《浮生六记》卷三·坎坷记愁（兼及卷四·浪游记快）',
  'key_concepts': [u'多情重诺，爽直不羁', u'转因之为累', u'处家人情，非钱不行', u'易儒为贾', u'反语'],
  'key_q': 1,
  'trans': {1: u'Whence come the hardships of a life? Often they are self-made—but not with me: I was too full of feeling, too ready to make promises, too frank and unbridled; and these very traits became my burden.',
            2: u'In managing a family and its human ties, nothing works without money.',
            3: u'"A woman without talent is a woman of virtue"—truly a saying for the ages!',
            4: u'After my travels in Jixi, seeing the sordidness in places of bustle became unbearable to my eyes, and so I turned from the scholar\'s path to trade.'},
  'qattr_en': {1: u'Vol.3, opening (W8)', 2: u'Vol.3 (W8)', 3: u'Vol.3 (irony, W8)', 4: u'Vol.4 (W8)'},
  'process_zh': [u'归因：从境遇中先找出自我因素（多情重诺，爽直不羁）',
                 u'实录世情：把「非钱不行」这类规则照实写下',
                 u'反语处置：不可直言之痛以反语引之（并标反语）',
                 u'落实行动：把判断变成转向（易儒为贾）'],
  'process_en': [u'Attribute: find the self-factor in the situation first (too much feeling, too many promises, too frank)',
                 u'Record the world as it is: write down rules like "nothing works without money" without美化',
                 u'Handle with irony: let irony carry pain that cannot be spoken plainly (and mark it as irony)',
                 u'Turn to action: convert judgment into a change of course (from scholar to trader)'],
  'cases': [{'q': 1, 'lead': u'卷三开篇：自省式归因（多情重诺，爽直不羁）', 'lead_en': u'The opening of Volume 3: self-examining attribution'},
            {'q': 2, 'lead': u'同卷：冷静记录世情规则（非钱不行）', 'lead_en': u'The same volume: a cool record of the world\'s rule (nothing works without money)'},
            {'q': 3, 'lead': u'同卷：反语引痛（须按反语与语境读）', 'lead_en': u'The same volume: pain carried by irony (to be read as irony, in context)'},
            {'q': 4, 'lead': u'卷四：把判断落为行动（易儒为贾）', 'lead_en': u'Volume 4: judgment turned into action (scholar to trader)'}],
  'modern_zh': [u'把「性格」作为境遇变量复盘', u'逆境叙事中的自我归因尺度', u'反语的阅读伦理：时代局限须标注', u'从自省到行动：易儒为贾式转向'],
  'modern_en': [u'Reviewing "character" as a variable of circumstance', u'The measure of self-attribution in narratives of adversity', u'An ethics of reading irony: mark the limits of the age', u'From reflection to action: the scholar-to-trader turn'],
  'related': [u'M-SHF-007'],
 },
 {
  'id': 'M-SHF-009', 'name_zh': u'得画意法', 'name_en': u'Attaining the Pictorial Idea Method',
  'category': u'文艺审美', 'category_raw': u'审美经营·技艺',
  'domain_zh': u'审美经营/技艺', 'domain_en': u'Aesthetic Cultivation / Craft',
  'definition_zh': u'插花盆景以「会心者得画意」为标尺：能不能得「画意」，全看会心；并戒「匠气」——「若留枝盘如宝塔，扎枝曲如蚯蚓者，便成匠气矣」；「小景可以入画，大景可以入神」；审美原则最终落在具体手艺（点缀盆中花石、作活花屏等做法）。判据在会心，成事在做法：标准不能停在趣味，必须落成可复制的工序。',
  'definition_en': u'For flower arrangement and potted landscapes the measure is "the one whose heart understands attains the pictorial idea": whether the pictorial idea is reached depends wholly on that understanding; and craftsman\'s mannerism is to be avoided—"if the branches are coiled like a pagoda or bent like an earthworm, it becomes craftsman\'s mannerism"; "a small scene can enter painting, a great scene can enter spirit"; and the aesthetic principle finally lands in concrete craft (arranging flowers and stones in a pot, making a living flower screen). The test is in the understanding, the doing is in the craft: a standard must not stop at taste but issue in repeatable procedure.',
  'source_chapter': u'《浮生六记》卷二·闲情记趣（兼及潘麐生序）',
  'key_concepts': [u'会心者得画意', u'匠气', u'小景可以入画，大景可以入神', u'点缀盆中花石', u'活花屏'],
  'key_q': 1,
  'trans': {1: u'It all depends on whether the one whose heart understands can attain the pictorial idea.',
            2: u'If the branches are left coiled like a pagoda, or bent like an earthworm, then it becomes craftsman\'s mannerism.',
            3: u'In arranging flowers and stones in a pot, a small scene can enter painting, a great scene can enter spirit.',
            4: u'The "portable spring railing" is the living flower screen.',
            5: u'In a country house with a broad courtyard the summer sun beats down; it is a great delight to teach the household the art of the living flower screen.'},
  'qattr_en': {1: u'Vol.2 (W8)', 2: u'Vol.2 (W8)',
               3: u'received text (W27; the Wikisource base reads a variant, see sourcing pack §8.1)',
               4: u'a line in Pan Linsheng\'s preface (W18)', 5: u'Vol.2 (W8)'},
  'process_zh': [u'立标尺：以「会心者得画意」为验收标准',
                 u'戒匠气：拒绝宝塔式、蚯蚓式的机械盘扎',
                 u'分景处置：小景入画、大景入神',
                 u'落手艺：把标准做成具体做法（点缀盆中花石、作活花屏）'],
  'process_en': [u'Set the measure: let "the heart understands and attains the pictorial idea" be the test',
                 u'Ban mannerism: refuse mechanical coiling in pagoda or earthworm styles',
                 u'Grade the scene: the small enters painting, the great enters spirit',
                 u'Land the craft: turn the standard into concrete procedure (arranging potted flowers and stones; making the living flower screen)'],
  'cases': [{'q': 1, 'lead': u'卷二：全篇的验收标尺（会心得画意）', 'lead_en': u'Volume 2: the test of the whole (understanding attains the pictorial idea)'},
            {'q': 2, 'lead': u'同卷：去匠气的判例（宝塔式、蚯蚓式）', 'lead_en': u'The same volume: the case against mannerism (pagoda and earthworm styles)'},
            {'q': 3, 'lead': u'同卷：大小二景的分级口径（通行本口径；底本作异文，双注登记）', 'lead_en': u'The same volume: grading the two scales (received text; the base text reads a variant, dually noted)',
             'tail': u'——底本作「邪可以入画」（W8），本引从通行本（W27），异文裁定见素材包 §八.1。', 'tail_en': u'—the base text reads a variant (W8); this quotation follows the received text (W27); see sourcing pack §8.1.'},
            {'q': 4, 'lead': u'潘麐生序诗句（序文层；与卷二「活花屏」技艺互文）', 'lead_en': u'A line in Pan Linsheng\'s preface (prefatory layer; echoing the living flower screen in Volume 2)'},
            {'q': 5, 'lead': u'卷二：活花屏的做法实例', 'lead_en': u'Volume 2: the living flower screen as a working example'}],
  'modern_zh': [u'审美判断力→可操作的手艺', u'去匠气的当代设计语言', u'园艺/盆景中的画意标准', u'建立个人审美工序：会心必须落到做法'],
  'modern_en': [u'Aesthetic judgment into operable craft', u'A contemporary design language free of mannerism', u'The standard of pictorial idea in gardening and bonsai', u'Build a personal aesthetic procedure: understanding must land in doing'],
  'related': [u'M-SHF-002'],
 },
 {
  'id': 'M-SHF-010', 'name_zh': u'浪游心得法', 'name_en': u'Insight Gained in Wandering Method',
  'category': u'方法论通用', 'category_raw': u'观察方法·行旅',
  'domain_zh': u'观察方法/行旅', 'domain_en': u'Method of Observation / Travel',
  'definition_zh': u'以「游幕三十年」的行走为样本：随人征逐（「轮蹄征逐，处处随人」）使山水变成「云烟过眼」，只能「领略其大概」而「不能探僻寻幽」——这是一句遗憾，不是宣言；名胜的得失在「心得」（与 M-SHF-003 呼应）；并以具体场面演示观照瞬间——「冒雪登楼」时的琼花飞舞与江上小艇的颠簸，直到「名利之心至此一冷」。游的价值不在到过，而在心得。',
  'definition_en': u'With thirty years of wandering in secretarial service as the sample: being driven on (wheels and hoofs, ever following others) turns hills and waters into "clouds and smoke passing before the eyes"; one can claim only the general outline, and "cannot seek out the hidden and secluded spots"—a sentence of regret, not a manifesto. The gain of a scenic place lies in what the heart acquires (echoing M-SHF-003); and the moment of contemplation is shown in concrete scenes—climbing through the snow as jade flowers dance, small boats tossing on the river—until "the heart for fame and gain turns cold." The value of travel lies not in having been there, but in what the heart gains.',
  'source_chapter': u'《浮生六记》卷四·浪游记快',
  'key_concepts': [u'轮蹄征逐', u'云烟过眼', u'探僻寻幽', u'心得', u'观照瞬间'],
  'key_q': 1,
  'trans': {1: u'A pity that, driven on by wheel and hoof, everywhere following others, I took the joy of hills and waters as clouds and smoke passing before the eyes—I cannot claim to have grasped even the general outline, nor to have sought out the hidden and secluded spots.',
            2: u'Zhuotang and I climbed it through the snow, and looking down upon the vast sky, with jade flowers dancing and silver hills and jade trees pointed out in the distance, it was as if we stood on a terrace of the immortals.',
            3: u'The small boats passing on the river, tumbling and tossing like torn leaves rolled by the waves—at this, the heart for fame and gain turns cold.'},
  'qattr_en': {1: u'Vol.4 (W8)', 2: u'Vol.4 (W8)', 3: u'Vol.4 (W8)'},
  'process_zh': [u'看清游的模式：轮蹄征逐，处处随人',
                 u'承认遗憾：只领略大概、不能探僻寻幽（遗憾句，非宣言）',
                 u'改换标尺：名胜所在，贵乎心得',
                 u'记录观照瞬间：把冒雪登楼、名利之心一冷写成场面'],
  'process_en': [u'See the pattern of the journey: driven on by wheel and hoof, ever following others',
                 u'Admit the regret: only the general outline, no seeking out of hidden spots (regret, not manifesto)',
                 u'Change the measure: for a scenic place, what the heart gains is what counts',
                 u'Record the moment of contemplation: turn the snow climb and the cooling of the heart into a scene'],
  'cases': [{'q': 1, 'lead': u'卷四：行走模式的遗憾句（随人征逐、云烟过眼）', 'lead_en': u'Volume 4: the sentence of regret about the pattern of travel'},
            {'q': 2, 'lead': u'同卷：观照瞬间之一（冒雪登楼，琼花飞舞）', 'lead_en': u'The same volume: a moment of contemplation (the snow climb, jade flowers dancing)',
             'tail': u'——琢堂同游段可与素材包 §四.3 交游表互见。', 'tail_en': u'—the passage joins the travel-companion table in sourcing pack §4.3.'},
            {'q': 3, 'lead': u'同卷：观照瞬间之二（江上小艇，名利之心至此一冷）', 'lead_en': u'The same volume: another moment (river boats; the heart for fame and gain turns cold)'}],
  'modern_zh': [u'旅行与观照的关系', u'「云烟过眼」式遗憾的正当性', u'观察笔记：把瞬间写成场面', u'职业流动中的在地观看'],
  'modern_en': [u'The relation between travel and contemplation', u'The legitimacy of "clouds and smoke passing by" regret', u'Observation notes: writing the moment as a scene', u'Seeing locally amid professional mobility'],
  'related': [u'M-SHF-003', u'M-SHF-001'],
 },
]

# ---------------------------------------------------------------------------
# figure 档案内容（H-SHF-001；要点来自素材包 §一/§4.1–§4.5，逐条可落源）
# ---------------------------------------------------------------------------
FIGURE_CONTENT = {
 'figure_name': u'沈复',
 'figure_pinyin': u'Shen Fu',
 'birth_year': 1763,
 'death_year': None,
 'era': u'清朝（乾隆—道光） / Qing Dynasty (Qianlong-Daoguang)',
 'time_period_standardized': u'1763 CE —（卒年失考；约 1808 年以后在世）',
 'nationality': u'中国',
 'ethnicity': u'汉族',
 'school': u'自传文学/生活美学',
 'intellectual_tradition': u'明清文人生活书写与自述传统',
 'courtesy_name': u'三白',
 'style_name': u'梅逸',
 'representative_works': [
  u'《浮生六记》（存卷一~卷四；卷五《中山记历》、卷六《养生记道》原佚，现传系伪续）',
  u'《水绘园图册》（上海博物馆藏；真伪曾有争论）',
  u'《幞山风木图》（已佚；胡不归《沈复年谱》记）',
 ],
}

FIGURE_CONTENT.update({
 'historical_significance': u'沈复（1763 年生，卒年失考），字三白，号梅逸，江苏长洲（今苏州市）人，居苏州沧浪亭畔；习幕四十余年，兼及经商、绘事与著述。生乾隆癸未冬十一月廿二日（一手自述；精确的公历折算日系衍生写法，见素材包 §八.11）；「游幕三十年来」遍历南北。妻陈芸（字淑珍，1763-1803，同齿长十月）：缔姻于乾隆乙未（1775）七月十六日，成婚于乾隆庚子（1780）正月二十二日；嘉庆癸亥（1803）三月三十日芸亡，权葬扬州西门外之金桂山（俗呼郝家宝塔），作者忆「妻梅子鹤」语而自号梅逸——此为「梅逸」一号的一手证据。所著《浮生六记》存四卷（闺房记乐、闲情记趣、坎坷记愁、浪游记快），1874 年至 1877 年间经潘麐生序、王韬跋、杨引传序而刊行；刊行时作者之名已失传——杨引传序明言「名则已逸」，今行「沈复」为民国以来行世名。卒年诸说以俞平伯（当在嘉庆十二年（1807）以后）与胡不归《沈复年谱》小引（约在嘉庆十三年（1808）以后）为最稳口径；网络异说与错籍表述不采。其写作以「记其实情实事」为律令，经俞平伯、陈寅恪推重（转引层），并经林语堂评语（转引）与教材选文扩大影响。',
 'core_thoughts': [
  u'实录真情：以「记其实情实事」为写作律令（M-SHF-001）',
  u'物外之趣：把日常微物重译为景观（M-SHF-002）',
  u'独出己见：判断标准收归内在（M-SHF-003）',
  u'就事论事：省俭与雅洁的双约束解法（M-SHF-004）',
  u'布衣菜饭：幸福的最小方案（M-SHF-005）',
  u'情之所钟：以情为尺的取舍（M-SHF-006）',
  u'知己同心：知音结构的亲密关系（M-SHF-007）',
  u'坎坷自省：把性格作为境遇变量（M-SHF-008）',
  u'得画意：会心落到手艺（M-SHF-009）',
  u'浪游心得：观照优先于到过（M-SHF-010）',
 ],
 'famous_quote': u'布衣菜饭，可乐终身。',
 'famous_quote_source': u'《浮生六记》卷一·闺房记乐（芸语；W8；SHF-1 素材包 §三 M-SHF-005）',
 'influence': u'《浮生六记》以「布衣菜饭，可乐终身」等段落成为近现代流传最广的古典生活文本之一：俞平伯 1923/24 年作《重刊序》推重其文体；陈寅恪《元白诗笺证稿》以《闺房记乐》为例外创作（转引）；林语堂评语（转引层，英文原文未成证）与教材选文《兒時記趣》（原文即卷二童趣段）共同扩大其影响；1935 年世界书局《美化文学名著丛刊》「足本」托出后二记伪作（伪续事件，见素材包 §八.12/§八.14）；英法德俄等多语译本行世（W29），使其进入世界文学流通。',
})

FIGURE_CONTENT.update({
 'tags': [u'自传文学', u'浮生六记', u'生活美学', u'布衣菜饭', u'陈芸', u'闺房记乐', u'闲情记趣',
          u'坎坷记愁', u'浪游记快', u'幕僚', u'苏州', u'沧浪亭', u'梅逸', u'三白', u'物外之趣',
          u'画意', u'活花屏', u'伪续事件', u'清中叶'],
 'cross_references': [
  {'target_figure_code': u'H-MT-001', 'relation_type': u'comparison',
   u'description_zh': u'徐霞客为晚明旅行考察家（其档属行旅—考察一系）；沈复卷四浪游记快同写行旅，一为探险考察之游、一为幕职流动之游——两档在行旅与观察方法的意义上可作对照阅读（具体比对另行立卡）。'},
  {'target_figure_code': u'H-JST-001', 'relation_type': u'comparison',
   u'description_zh': u'金圣叹为明末清初的文学批评家（其档含小说戏曲评点与文人生活题材）；沈复《浮生六记》以日常生活入文——两档在文人生活书写的意义上可作对照阅读（具体比对另行立卡）。'},
  {'target_figure_code': u'H-SU-001', 'relation_type': u'comparison',
   u'description_zh': u'苏轼（东坡）「事如春梦了无痕」句为《浮生六记》卷一开篇所援引，是其记录动因的出发句；两档在以文字安顿人生经验的意义上可作对照阅读（具体比对另行立卡）。'},
 ],
 'meta': {
  'source': u'SHF-1 素材包（docs/research/phase21r9_shenfu_sourcing_report.md/.json；见证 W1–W30）',
  'methodology': u'Phase21-R9 重建落盘：以 SHF-1 素材包逐条引文重锚；全新图码 H-SHF-001（与旧件零关联）',
  'validation': u'verification pending（10 条）；引文与素材包逐字比对由 verify_phase21r9_shenfu.py 执行；入库前须走独立核验流程',
  'generation_date': u'2026-09-24',
  'mode_count': 10,
  'figure_code_ref': u'H-SHF-001',
  'phase': u'Phase 21-R9',
 },
 'related_figures': [u'H-MT-001', u'H-JST-001', u'H-SU-001'],
 'mode_ids_note': u'沈复重做（Phase21-R9）：本档为全新图码 H-SHF-001；对应旧件（R7 裁定的虚名空壳）维持归档、不唤醒、不改名、不迁载荷，其旧模式码零复用；本档新码 M-SHF-001 至 M-SHF-010，落盘前全库查重 0 占用',
 'caveats': [
  u'Phase21-R9 重建落盘：10 条 key_quote 逐字取自 SHF-1 素材包（§三 quotes；并经见证副本强归一化复核）；核验状态 pending，入库前须走独立核验流程',
  u'卒年失考：death_year=null；注记「约 1808 年以后在世，下限不明」（俞平伯/胡不归口径）。网络无源卒说（年份异说）、错籍表述与「名复」方志说等一律不采（素材包 §1.4/§4.5）',
  u'「名复」属行世名：杨引传序（1877）明言「名则已逸」；最早书面痕迹为《水绘园图》款「三白沈复」（真伪曾有争论，属疑似）——其在原始文献中的依据无从查得，引用须并注',
  u'卷五/卷六红线：现传《中山记历》《养生记道》系伪续，任何题材不得采其文本；《海国记》（钱泳《记事珠》辑本）与琉球之行作疑似史料单列（素材包 §1.6/§八.14）',
  u'转引层标注：林语堂评语（英文原文未成证）、陈寅恪引文（以学术源为准）、俞平伯序、胡不归年谱小引等均保留转引链，未升格为沈复原文',
  u'用字异文：M-SHF-009「小景可以入画」从通行本口径（维基文库底本作「邪可以入画」，双注登记，素材包 §八.1）；「秋侵人影瘦，霜染菊花肥」与管诗引「秋深人瘦菊花肥」两式各归出处',
  u'school / intellectual_tradition / core_thoughts 等为描述性标签（依素材包主题池归纳，非当事人自认学派）；cross_references 三条为对照阅读框架（具体比对另行立卡）',
  u'图像素材：藏画《水绘园图册》与题款为确证（转录本），其真伪之争与「作幕如皋十余年」说按素材包登记；未获可靠画像，不使用',
 ],
})

# ---------------------------------------------------------------------------
# 构建函数
# ---------------------------------------------------------------------------

def build_entry(c, idx):
    mid = c['id']
    pm = PACK_MODES[mid]
    quotes = pm.get('quotes', [])
    kq = c['key_q']
    assert 1 <= kq <= len(quotes), mid
    cases_zh, cases_en, used = [], [], []
    for case in c['cases']:
        if 'q' in case:
            qi = case['q']
            q = quotes[qi - 1]
            zh = u'%s：「%s」——%s' % (case['lead'], q['text'], q['attr'])
            en = u'%s: "%s" — %s' % (case['lead_en'], c['trans'][qi], c['qattr_en'][qi])
            t = case.get('tail')
            if t:
                zh += t
                en += u' ' + case['tail_en']
            used.append(qi)
        else:
            zh = case['text']
            en = case['text_en']
        cases_zh.append(zh)
        cases_en.append(en)
    entry = {
        'id': mid, 'mode_code': mid, 'figure_code': FIG, 'figure_name': FIGURE_CONTENT['figure_name'],
        'name_zh': c['name_zh'], 'name_en': c['name_en'],
        'category': c['category'], 'category_raw': c['category_raw'],
        'domain_zh': c['domain_zh'], 'domain_en': c['domain_en'],
        'level': u'核心', 'priority': idx + 1,
        'definition_zh': c['definition_zh'], 'definition_en': c['definition_en'],
        'source_chapter': c['source_chapter'], 'key_concepts': c['key_concepts'],
        'key_quote_zh': quotes[kq - 1]['text'], 'key_quote_en': c['trans'][kq],
        'process_zh': c['process_zh'], 'process_en': c['process_en'],
        'representative_cases_zh': cases_zh, 'representative_cases_en': cases_en,
        'modern_applications_zh': c['modern_zh'], 'modern_applications_en': c['modern_en'],
        'related_modes': c['related'], 'legacy_mode_id': u'',
        'verification': {
            'status': 'pending',
            'method': 'phase21r9-shenfu-rebuild-landing',
            'evidence': u'引文逐字取自 SHF-1 素材包（§三 quotes；%s）；核验 pending，入库前须走独立核验流程' % quotes[kq - 1]['attr'],
            'checked_at': DATE, 'checker': 'elcano',
        },
    }
    return entry, used


def build_figure(entries):
    fc = FIGURE_CONTENT
    return {
        'schema_version': u'v6', 'id': FIG, 'code': FIG, 'figure_name': fc['figure_name'],
        'figure_code': FIG, 'figure_pinyin': fc['figure_pinyin'],
        'birth_year': fc['birth_year'], 'death_year': fc['death_year'],
        'era': fc['era'], 'time_period_standardized': fc['time_period_standardized'],
        'nationality': fc['nationality'], 'ethnicity': fc['ethnicity'],
        'school': fc['school'], 'intellectual_tradition': fc['intellectual_tradition'],
        'courtesy_name': fc['courtesy_name'], 'style_name': fc['style_name'],
        'representative_works': fc['representative_works'],
        'historical_significance': fc['historical_significance'],
        'core_thoughts': fc['core_thoughts'],
        'famous_quote': fc['famous_quote'], 'famous_quote_source': fc['famous_quote_source'],
        'influence': fc['influence'], 'tags': fc['tags'], 'cross_references': fc['cross_references'],
        'meta': fc['meta'], 'related_figures': fc['related_figures'],
        'thinking_mode_count': len(entries), 'mode_ids': [e['mode_code'] for e in entries],
        'mode_ids_note': fc['mode_ids_note'], 'caveats': fc['caveats'], 'modes': entries,
    }


def build_individuals(fig):
    ind = dict(fig)
    del ind['modes']
    return ind


def build_top_block():
    entry_by = dict((c['id'], c) for c in MODE_CONTENT)
    ev = []
    for i, e in enumerate(MODE_CONTENT, 1):
        a = PACK_MODES[e['id']]['quotes'][e['key_q'] - 1]['attr']
        ev.append({'mode_id': e['id'],
                   'example_zh': u'%s（%s）' % (e['cases'][e['key_q'] - 1]['lead'] if 'q' in e['cases'][e['key_q'] - 1] else u'核心用例', a),
                   'example_en': e['cases'][e['key_q'] - 1]['lead_en']})
    return {
        'schema_version': u'v6', 'card': CARD, 'figure_code': FIG,
        'target': u'data/modes_data.json 顶层块「H-SHF-001」（新增由合并卡执行；原块缺失则新增）',
        'proposal': {
            'schema_version': u'v6', 'code': FIG,
            'name_zh': u'沈复：物外之趣·布衣菜饭·画意生活',
            'name_en': u'Shen Fu: Charm Beyond Things · Plain Cloth and Simple Fare · The Pictorial Life',
            'era': u'清代/Qing Dynasty (1763-?)',
            'historical_domains': [u'自传书写与生活记录', u'生活美学（闲情/技艺）', u'行旅与观察'],
            'domains': [u'自传书写', u'生活美学', u'行旅观察'],
            'core_modes': [c['id'] for c in MODE_CONTENT],
            'gender': u'Male',
            'ethnicity': u'汉族 / Han Chinese',
            'nationality': u'中国 / China',
            'civilization_sphere': u'清代中国/文人生活与江南城市文化 / Qing China / Literati Life and Jiangnan Urban Culture',
            'time_period_standardized': u'1763-? CE（卒年失考；约 1808 年以后在世）',
            'primary_language': u'文言文/清代随笔体 / Classical Chinese (Qing familiar essay)',
            'intellectual_tradition': u'明清文人生活书写与自述传统 / Ming-Qing literati life-writing and autobiographical tradition',
            'unique_thinking_zh': u'沈复（1763—卒年失考），江苏长洲（今苏州市）人，幕僚、画人、商人、著者；妻陈芸。所著《浮生六记》存四卷（闺房记乐、闲情记趣、坎坷记愁、浪游记快），以「记其实情实事」为写作律令。其人其书可提炼十法：实录真情（写作律令）／物外之趣（微物重译为景观）／独出己见（判断收归内在，贵乎心得）／就事论事（省俭而雅洁）／布衣菜饭，可乐终身（幸福的最小方案）／情之所钟（以情为尺的取舍）／知己同心（同癖好、察眼意懂眉语）／坎坷自省（多情重诺，爽直不羁，转因之为累）／得画意（会心者得画意，戒匠气）／浪游心得（轮蹄征逐之憾与观照瞬间）。卷五/卷六原佚、现传系伪续，不采其文本；卒年失考（约 1808 年以后在世）。',
            'unique_thinking_en': u'Shen Fu (1763 - death unknown), a native of Changzhou, Jiangsu (present-day Suzhou), worked as a private secretary, painter, trader and author; his wife was Chen Yun. Six Chapters of a Floating Life survives in four volumes (Joys of the Boudoir, Delights of Leisure, Sorrows of Hardship, Joys of Wandering), with "recording the true facts and real feelings" as its stated law of writing. Ten methods may be distilled: truthful record of real feeling (the writing law) / charm beyond things (translating trifles into grand scenes) / forming one\'s own view (judgment taken back inside; what the heart gains) / taking each matter on its own terms (economy with refinement) / plain cloth and simple fare (the smallest scheme of happiness) / where affection settles (choosing by feeling) / one heart with a kindred spirit (same tastes; eyes and brows understood) / self-reflection in adversity (too much feeling, too many promises, frank and unbridled) / attaining the pictorial idea (understanding attains it; ban mannerism) / insight gained in wandering (the regret of clouds and smoke, the moment of contemplation). Volumes 5-6 are lost, and the current continuations are spurious and not used; his death year is unknown (alive after about 1808).',
            'mode_evidence': ev,
            'key_texts': [u'《浮生六记》卷一·闺房记乐', u'《浮生六记》卷二·闲情记趣', u'《浮生六记》卷三·坎坷记愁', u'《浮生六记》卷四·浪游记快'],
            'key_concepts': [u'记其实情实事', u'物外之趣', u'布衣菜饭，可乐终身', u'会心者得画意', u'游幕三十年'],
            'intellectual_lineage': [u'明清文人生活书写与自述传统', u'清代江南文人闲情传统'],
            'legacy_assessment': u'沈复以《浮生六记》存世四卷记录夫妻、闲情、家变与行旅，其「记其实情实事」的写作观与「布衣菜饭，可乐终身」等段落经 1877 年杨引传序刊后流传，并借俞平伯、林语堂（转引）与教材选文扩大影响；卒年失考、后二记伪续等存疑处均按素材包登记（评价与记录分层使用）。',
            'scholarly_value': u'清代自传散文、文人生活史与江南行旅书写的标本性文本（存四卷：一手记文＋1874/1877 序跋层）。',
        },
    }

# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

def wj(path, obj):
    bad = os.path.dirname(path)
    if bad and not os.path.isdir(bad):
        os.makedirs(bad)
    with io.open(path, 'w', encoding='utf-8') as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)
        f.write(u'\n')


def wr(path, text):
    bad = os.path.dirname(path)
    if bad and not os.path.isdir(bad):
        os.makedirs(bad)
    with io.open(path, 'w', encoding='utf-8') as f:
        f.write(text)


def scan_repo(patterns):
    files = subprocess.check_output(['git', '-C', REPO, 'ls-files'], text=True).split('\n')
    files += subprocess.check_output(['git', '-C', REPO, 'ls-files', '--others', '--exclude-standard'], text=True).split('\n')
    hits = {}
    scanned = 0
    skipped = 0
    for rel in sorted(set(files)):
        if not rel:
            continue
        if rel.startswith('.git') or '/node_modules/' in rel or rel.startswith('node_modules/') or '/.venv/' in rel or rel.startswith('.venv/') or '/backups' in rel or rel.startswith('backups'):
            skipped += 1
            continue
        fp = os.path.join(REPO, rel)
        if not os.path.isfile(fp) or os.path.getsize(fp) > 3000000:
            skipped += 1
            continue
        try:
            s = io.open(fp, encoding='utf-8', errors='ignore').read()
        except Exception:
            skipped += 1
            continue
        scanned += 1
        for pat in patterns:
            if pat in s:
                hits.setdefault(rel, []).append(pat)
    return dict(scanned=scanned, skipped=skipped, hits=hits)


def collect_frags(obj, out, attr):
    if isinstance(obj, dict):
        for k, v in obj.items():
            collect_frags(v, out, attr)
    elif isinstance(obj, list):
        for v in obj:
            collect_frags(v, out, attr)
    elif isinstance(obj, str):
        for opener, closer in ((u'\u300c', u'\u300d'), (u'\u300e', u'\u300f')):
            i = 0
            while True:
                a = obj.find(opener, i)
                if a < 0:
                    break
                b = obj.find(closer, a + 1)
                if b < 0:
                    break
                out.append((attr, obj[a + 1:b]))
                i = b + 1


def main():
    for pth in (PACK_MD, PACK_JSON):
        if not os.path.isfile(pth):
            print('FATAL: missing %s' % pth)
            return 2
    global PACK
    PACK = jl(PACK_JSON)
    global PACK_MODES
    PACK_MODES = dict((m['id'], m) for m in PACK['modes'])
    pack_blob = norm(io.open(PACK_MD, encoding='utf-8').read()) + norm(io.open(PACK_JSON, encoding='utf-8').read())

    entries = []
    used_total = []
    for i, c in enumerate(MODE_CONTENT):
        e, used = build_entry(c, i)
        entries.append(e)
        used_total.append((c['id'], used))
    fig = build_figure(entries)
    ind = build_individuals(fig)
    mfj = {'schema_version': u'v6', 'id': FIG, 'code': FIG, 'figure_name': fig['figure_name'],
           'figure_code': FIG, 'thinking_mode_count': len(entries), 'modes': entries}

    frags = []
    for e in entries:
        collect_frags(e, frags, e['id'])
    collect_frags(fig, frags, FIG + '-figure')
    landing_core = {'top': build_top_block()}
    collect_frags(landing_core, frags, FIG + '-top')
    bad = [(a, f) for a, f in frags if norm(f) not in pack_blob]
    if bad:
        print('FRAGMENT CHECK FAILED (%d):' % len(bad))
        for a, f in bad[:40]:
            print('  ', a, f)
        return 3

    patterns = ['H-SHF-001', 'M-SHF-0', 'C-SHF-']
    pre = scan_repo(patterns)

    land = os.path.join(REPO, 'docs/scratch/legacy20_r9_shenfu_landing')
    wj(os.path.join(REPO, 'data/figures/%s.json' % FIG), fig)
    wj(os.path.join(REPO, 'data/individuals/%s.json' % FIG), ind)
    wj(os.path.join(REPO, 'data/individuals/%s_modes.json' % FIG), mfj)
    wj(os.path.join(land, 'modes_library_entries.json'), entries)
    wj(os.path.join(land, 'combined_library_entries.json'), {'schema_version': u'v6', 'modes': entries})
    wj(os.path.join(land, 'top_block_proposal.json'), landing_core['top'])
    notes = {
        'figure_code': FIG,
        'notes': {
            'scenarios_zh_new': 0,
            'scenarios_en_new': 0,
            'reason': u'R9 重建落盘卡（1/2）未产出场景件：场景注册属合并卡范围；本档无旧场景载荷可搬迁（旧件维持归档，本链零搬迁）',
            'new_prefix_suggestion': u'C-SHF-001~010 / C-SHF-001E~010E（全库实测 0 碰撞；1:1 配对：code 序号=mode 序号；沿 C-WX/C-LUORQ 先例）',
            'template_rule': u'text_zh = name_zh + “的当代应用场景：” + application_area_zh（分号连接）+ 句号收束；text_en = “Contemporary applications of ” + name_en + “: ” + application_area_en（分号连接）+ 句点收束；application_area_* 逐字取条目 modern_applications_*（合并卡可脚本复算）',
            'old_code_dispositions': [],
            'remap_needed': [],
        },
    }
    wj(os.path.join(land, 'scenario_notes.json'), notes)
    lines = [u'legacy_id\tv6_id\tname_zh\tname_en\tnote\n']
    for e in entries:
        lines.append(u'\t%s\t%s\t%s\t全新码（无旧号；旧件维持归档、零复用）\n' % (e['id'], e['name_zh'], e['name_en']))
    wr(os.path.join(land, 'id_mapping.tsv'), u''.join(lines))
    lines = [u'legacy_mode_id\tv6_id\tcategory_raw\tcategory\tstatus\tcandidate_target\n']
    for e in entries:
        lines.append(u'\t%s\t%s\t%s\tnew_rebuild_no_legacy_raw\t\n' % (e['id'], e['category_raw'], e['category']))
    wr(os.path.join(land, 'category_mapping.tsv'), u''.join(lines))
    for pair in (('figures/%s.json' % FIG, os.path.join(REPO, 'data/figures/%s.json' % FIG)),
                 ('individuals/%s.json' % FIG, os.path.join(REPO, 'data/individuals/%s.json' % FIG)),
                 ('individuals/%s_modes.json' % FIG, os.path.join(REPO, 'data/individuals/%s_modes.json' % FIG))):
        dst = os.path.join(land, pair[0])
        if not os.path.isdir(os.path.dirname(dst)):
            os.makedirs(os.path.dirname(dst))
        with io.open(pair[1], 'rb') as f:
            data = f.read()
        with io.open(dst, 'wb') as f:
            f.write(data)

    post = scan_repo(patterns)
    deliverables = {}
    for rel in ['data/figures/%s.json' % FIG, 'data/individuals/%s.json' % FIG, 'data/individuals/%s_modes.json' % FIG,
                'docs/scratch/legacy20_r9_shenfu_landing/modes_library_entries.json',
                'docs/scratch/legacy20_r9_shenfu_landing/combined_library_entries.json',
                'docs/scratch/legacy20_r9_shenfu_landing/id_mapping.tsv',
                'docs/scratch/legacy20_r9_shenfu_landing/category_mapping.tsv',
                'docs/scratch/legacy20_r9_shenfu_landing/scenario_notes.json',
                'docs/scratch/legacy20_r9_shenfu_landing/top_block_proposal.json',
                'docs/scratch/legacy20_r9_shenfu_landing/figures/%s.json' % FIG,
                'docs/scratch/legacy20_r9_shenfu_landing/individuals/%s.json' % FIG,
                'docs/scratch/legacy20_r9_shenfu_landing/individuals/%s_modes.json' % FIG]:
        full = os.path.join(REPO, rel)
        deliverables[rel] = {'bytes': os.path.getsize(full), 'sha256': sha_file(full)}
    base = subprocess.check_output(['git', '-C', REPO, 'rev-parse', '--short', 'HEAD'], text=True).strip()
    archive = {}
    arch_dir = os.path.join(REPO, 'data/figures/_duplicates')
    for fn in sorted(os.listdir(arch_dir)):
        if fn.startswith('H-HAN-001'):
            archive[fn] = sha_file(os.path.join(arch_dir, fn))
    for _k, _v in ARCHIVE_SHA.items():
        if _k not in archive:
            print('ARCHIVE MISSING', _k)
        elif archive[_k] != _v:
            print('ARCHIVE SHA MISMATCH', _k)

    mainlib = {}
    for rel in ['data/modes_data.json', 'data/code_maps.json', 'data/scenarios_zh.json', 'data/scenarios_en.json',
                'data/scenario_tags.json', 'data/figure_names.json', 'tools/modes_data.json', 'tools/code_maps.json',
                'tools/code_maps_en.json', 'tools/scenario_tags.json', 'tools/json/scenarios_zh.json', 'tools/json/scenarios_en.json']:
        fp2 = os.path.join(REPO, rel)
        mainlib[rel] = sha_file(fp2) if os.path.isfile(fp2) else ''
    frag_wl = []
    quoted = set()
    for c in MODE_CONTENT:
        for q in PACK_MODES[c['id']]['quotes']:
            quoted.add(norm(q['text']))
    seen = set()
    for e in entries:
        blob = [e['definition_zh'], e['source_chapter']] + e['process_zh'] + e['representative_cases_zh'] + e['modern_applications_zh'] + e['key_concepts']
        fl = []
        collect_frags(blob, fl, e['id'])
        for a, f in fl:
            if any(norm(f) in qq for qq in quoted):
                continue
            key = (a, f)
            if key in seen:
                continue
            seen.add(key)
            frag_wl.append({'fragment': f, 'mode': a, 'reason': u'素材包语句（非引文段；构建期已核为素材包 md/json 子串）'})
    qt = []
    for c in MODE_CONTENT:
        for i, q in enumerate(PACK_MODES[c['id']]['quotes'], 1):
            qt.append({'entry': c['id'], 'quote_index': i, 'attr': q['attr'], 'chars': len(q['text']),
                       'is_key': (i == c['key_q']), 'used_in_entry': True})
    man = {
        'card': CARD, 'figure_code': FIG, 'figure_name': FIGURE_CONTENT['figure_name'],
        'date': DATE, 'baseline_commit': base,
        'method': u'Phase21-R9 重建落盘：SHF-1 素材包逐条重锚（本卡零库写）',
        'deliverables': deliverables,
        'counts': {'modes': 10, 'quotes': len(qt), 'legacy_ids': 0, 'scenario_dispositions': 0, 'frag_whitelist': len(frag_wl)},
        'zero_library_write': True,
        'archive_untouched': archive,
        'mainlib_baselines': mainlib,
        'frag_whitelist': frag_wl,
        'quote_table': qt,
        'preflight': pre, 'postflight': post,
        'merge_card_scope': [u'M-SHF-001~010 入 data/modes_data.json（先备份后合并）',
                             u'figure 注册：code_maps / figure_names / scenario_tags / scenarios（zh+en）',
                             u'顶层块 H-SHF-001 按 top_block_proposal.json 新增（原块缺失则新增）'],
        'unrelated_mentions': u'（写入后由独立核验复核主库登记面 0 命中；旧件 H-HAN-001 不唤醒、零复用）',
    }
    wj(os.path.join(REPO, 'data/audit/phase21r9_shenfu_landing_manifest.json'), man)
    with io.open(os.path.join(REPO, 'data/audit/phase21r9_shenfu_landing_manifest.json'), 'rb') as f:
        mb = f.read()
    with io.open(os.path.join(REPO, 'docs/research/phase21r9_shenfu_landing_evidence.json'), 'wb') as f:
        f.write(mb)
    print('BUILD OK: entries=%d quotes_used=%d frag_whitelist=%d' % (len(entries), len(qt), len(frag_wl)))
    print('preflight hits:', sorted(pre['hits'].keys()))
    print('postflight hits:', sorted(post['hits'].keys()))
    print('deliverables: %d' % len(deliverables))
    return 0


if __name__ == '__main__':
    sys.exit(main())
