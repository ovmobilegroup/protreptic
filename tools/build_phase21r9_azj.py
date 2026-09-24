#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Phase21-R9 安子介 H-AZJ-001 重建落盘生成器（卡 t_58ebf9c2）
#
# 唯一内容来源：docs/research/phase21r9_anzijie_sourcing_report.md/.json（AZJ-1 素材包）。
# 禁止复用：H-AZJ-345「安子介（特区叙事）」判死清档件及其旧载荷号段（R8 裁定 t_3de0af0e / 清档 t_3669eb4a）。
#
# 产出：data/figures/H-AZJ-001.json、data/figures/H-AZJ-001_modes.json、
#       data/individuals/H-AZJ-001.json、data/individuals/H-AZJ-001_modes.json、
#       docs/scratch/legacy20_r9_azj_landing/**、data/audit/phase21r9_azj_landing_manifest.json
#
# 纪律：引文逐字取自素材包；疑似项保留 pending 标记不升级；主库六件零写入；不碰归档/备份字节；零自造句。
import hashlib
import io
import json
import os
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PACK_JSON = os.path.join(REPO, 'docs/research/phase21r9_anzijie_sourcing_report.json')
PACK_MD = os.path.join(REPO, 'docs/research/phase21r9_anzijie_sourcing_report.md')
LANDING = os.path.join(REPO, 'docs/scratch/legacy20_r9_azj_landing')
WITNESS = os.path.join(REPO, 'docs/scratch/phase21r9_anzijie/witness')
DATE = '2026-09-24'
FIG = 'H-AZJ-001'
FIG_NAME = u'安子介'
FIG_NAME_EN = 'Ann Tse Kai'
CODES = ['M-AZJ-%03d' % i for i in range(1, 11)]
CARD = 't_58ebf9c2'
MAIN_LIB = ['data/modes_data.json', 'data/code_maps.json', 'data/scenarios_zh.json',
            'data/scenarios_en.json', 'data/scenario_tags.json', 'data/figure_names.json']
STD_CATEGORIES = [u'伦理修养', u'军事战略', u'医学养生', u'史学文献', u'哲学形而上', u'宗教修行', u'工程技术',
                  u'心理洞察', u'战略决策', u'探险发现', u'政治治理', u'教育传承', u'文艺审美', u'方法论通用',
                  u'科学方法', u'组织领导', u'经济商业', u'认识论逻辑']
ENTRY_KEYS = ['id', 'mode_code', 'figure_code', 'figure_name', 'name_zh', 'name_en', 'category',
              'category_raw', 'domain_zh', 'domain_en', 'level', 'priority', 'definition_zh',
              'definition_en', 'source_chapter', 'key_concepts', 'key_quote_zh', 'key_quote_en',
              'process_zh', 'process_en', 'representative_cases_zh', 'representative_cases_en',
              'modern_applications_zh', 'modern_applications_en', 'related_modes', 'legacy_mode_id',
              'verification']


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


def sha_file(path):
    with open(path, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()


PACK = jl(PACK_JSON)
PACK_MD_TEXT = io.open(PACK_MD, encoding='utf-8').read()
PM = dict((m['id'], m) for m in PACK['modes'])


def QF(mid, idx):
    return PM[mid]['quotes'][idx - 1].get('text', '')


def QW(mid, idx):
    return PM[mid]['quotes'][idx - 1].get('w', 'W?')


# ---------------------------------------------------------------- 条目内容（10 条）
# qsrc=(素材包模式码, 1-based 引文序号)：key_quote_zh 即素材包该段引文原文（逐字）
AUTHOR = [
    dict(
        code='M-AZJ-001', priority=1,
        name_zh=u'汉字本位主义', name_en='Han-Character Nativism Method',
        pack_name=u'汉字本位主义：汉字是「中国第五大发明」与中华文化之根',
        category=u'教育传承', category_raw=u'语言文字学/汉字现代化/文化观',
        domain_zh=u'语言文字学/汉字现代化/文化观',
        domain_en='Chinese Character Studies / Character Modernization / Cultural Outlook',
        def_zh=u'安子介视汉字为中华文化之根与「中国第五大发明」，并把这一文化判断落成三条长期行动：以 21 本汉字学专著推进研究（1979—1995 年，政务商务间隙写成）、以《解开汉字之谜》等书向世界推广汉字、以编码法与写字机把汉字带入信息时代（与 M-AZJ-007 衔接）。素材包口径：官方讲话之转述为确证；「二十一世纪是汉字发挥威力」见词条/书目转述链，属疑似，不得作为确证引文。',
        def_en=u"Ann Tse Kai held the Chinese character to be the root of Chinese culture and China's fifth great invention, and turned that cultural judgment into three long-running lines of action: advancing research through 21 monographs on Chinese characters written between official and business duties (1979-1995), spreading the script abroad through books such as The Mystery of Chinese Characters, and carrying it into the information age through his coding method and writing machine (cf. M-AZJ-007). Source tier: the official memorial speech's rendering counts as confirmed; the line that the twenty-first century is when Chinese characters show their power appears only through encyclopedia and bibliographic transmission and remains suspected, so it must not be cited as confirmed.",
        source_chapter=u'AZJ-1 素材包 §二 M-AZJ-001；引据：廖晖《在纪念安子介先生诞辰100周年座谈会上的讲话》（2012-06-27，W01）＋W08/W09 转述',
        concepts=[u'汉字本位主义', u'中华文化之根', u'中国第五大发明', u'21 本汉字学专著', u'汉字现代化推广'],
        qsrc=('M-AZJ-001', 1),
        quote_en=u"Steeped in classical culture from childhood, he cherished a deep affection for Chinese characters and traditional Chinese culture, holding that Chinese characters are China's fifth great invention and the root of Chinese culture; for decades he devoted himself to the study of Chinese characters. In the spare moments of his busy official and business life he wrote 21 monographs on Chinese characters, sparing no effort in spreading them to the world.",
        process_zh=[
            u'立根：确立「汉字是中国第五大发明和中华文化之根」的文化判断（W01 讲话转述口径）',
            u'治学：1979—1995 年于政务商务间隙撰写 21 本汉字学专著（W01/W08）',
            u'推广：以《解开汉字之谜》《汉字易学》等向世界推广汉字（W01）',
            u'技术化：把汉字研究延伸到编码法与写字机（W01/W04；与 M-AZJ-007 衔接）',
        ],
        process_en=[
            "Fix the premise: establish the cultural judgment that Chinese characters are China's fifth great invention and the root of Chinese culture (per the official speech, W01)",
            'Research: write 21 monographs on Chinese characters amid official and business duties, 1979-1995 (W01/W08)',
            'Promote: spread Chinese characters to the world through The Mystery of Chinese Characters, Chinese Characters Made Easy and related works (W01)',
            'Technologize: extend character studies into a coding method and a writing machine (W01/W04; cf. M-AZJ-007)',
        ],
        cases_zh=[
            u'官方讲话（W01，2012-06-27）：「认为汉字是中国第五大发明和中华文化之根，几十年如一日地致力于汉字学研究」；「撰写了21本汉字学专著，不遗余力地向世界推广汉字」——「第五大发明」命题级本人原话原件未获，引用须注明系讲话转述。',
            u'官方生平与百科（W08）：「1979年至1995年，他利用繁忙的政务和商务间隙，共撰写了21本汉字学专著。」',
            u'疑似另注（W09，《解开汉字之谜》词条·内容简介）：「二十一世纪是汉字发挥威力」仅见词条/书目转述链，保留疑似标记，不得写作确证引文。',
        ],
        cases_en=[
            "Official speech (W01, 2012-06-27): holding that Chinese characters are China's fifth great invention and the root of Chinese culture, he devoted himself for decades to the study of Chinese characters; he wrote 21 monographs on Chinese characters, sparing no effort in spreading them to the world - the original first-person wording of the fifth-great-invention thesis is not available, so citations must note it is the speech's rendering.",
            'Official biography and encyclopedia (W08): from 1979 to 1995 he wrote 21 monographs on Chinese characters in the spare moments of his busy official and business life.',
            'Suspected note (W09, entry on The Mystery of Chinese Characters): the line that the twenty-first century is when Chinese characters show their power exists only through transmission chains and keeps its suspected mark; it must not be written as a confirmed quotation.',
        ],
        modern_zh=[u'数字化时代对汉字与母语文化的再定位', u'语言技术化与文脉延续的张力管理'],
        modern_en=['Repositioning the Chinese character and mother-tongue culture in the digital age',
                   'Managing the tension between language technologization and cultural continuity'],
        related=[u'M-AZJ-006', u'M-AZJ-007'],
        tier_note=u'tier=确证（官方讲话转述＋多源互证）；命题级本人原话=疑似（原件未获）',
    ),
    dict(
        code='M-AZJ-002', priority=2,
        name_zh=u'实业救国路径', name_en='Industrial Salvation through Knowledge Transfer Method',
        pack_name=u'实业救国路径：从译书启智到「三经一纬」的产业升级',
        category=u'经济商业', category_raw=u'实业经济/产业升级/知识迁移',
        domain_zh=u'实业经济/产业升级/知识迁移',
        domain_en='Industrial Economy / Industrial Upgrading / Knowledge Transfer',
        def_zh=u'把「译书启智—理论著述—技术创新—集团化」串成一条实业路径：1937 年译《间接成本之研究》洞悉中国工业与列强的差距，1947 年以 60 万字《国际贸易实务》沉淀商贸理论（马寅初作序），其后以「三经一纬」斜纹布打开南非、欧美及东南亚市场，再以集团化经营（属下公司 70 余家）完成产业升级。边界：非商科科班出身、靠自学与时代窗口，路径不可简单复制。',
        def_en=u"A chain from translated books to industrial upgrading: translating The Study of Indirect Costs in 1937 revealed how far China's industry lagged the powers; the 600,000-character International Trade Practice (1947, with a preface by Ma Yinchu) distilled commercial theory; the three-warp-one-weft twill opened markets in South Africa, Europe, America and Southeast Asia; group operation (more than 70 affiliated companies) completed the industrial upgrading. Boundary: not business-school trained, relying on self-study and a particular historical window - the path is not simply replicable.",
        source_chapter=u'AZJ-1 素材包 §二 M-AZJ-002；引据：《安子介先生生平》（新华社 2000，W02）／大公報（2009-09-19，W07）',
        concepts=[u'译书启智', u'《间接成本之研究》', u'《国际贸易实务》', u'「三经一纬」斜纹布', u'南联集团化'],
        qsrc=('M-AZJ-002', 3),
        quote_en=u"Through translating the Japanese business book The Study of Indirect Costs, he realized with a shock that China's industrial productivity lagged far behind the world powers, which planted in him the idea of using foreign economic theory to revive China's national industry. (Original in traditional Chinese.)",
        process_zh=[
            u'译介：1937 年翻译出版日文版《间接成本之研究》，洞悉工业生产力差距（W02/W07）',
            u'著述：1947 年写成 60 万字的《国际贸易实务》，马寅初作序（W02）',
            u'技术：与董事们研究设计「三经一纬」斜纹布，打开南非、欧美及东南亚市场（W02）',
            u'集团化：属下公司 70 余家，成为六七十年代香港蜚声中外的纺织集团（W02）',
        ],
        process_en=[
            'Translate: publish the translation of The Study of Indirect Costs in 1937 and recognize the productivity gap (W02/W07)',
            'Write: complete the 600,000-character International Trade Practice in 1947, prefaced by Ma Yinchu (W02)',
            'Innovate: design the three-warp-one-weft twill with fellow directors and open markets in South Africa, Europe, America and Southeast Asia (W02)',
            'Group: build more than 70 affiliated companies into a Hong Kong textile group of the 1960s-70s (W02)',
        ],
        cases_zh=[
            u'官方生平（W02）：「1937年，他翻译出版了日文版《间接成本之研究》。」',
            u'官方生平（W02）：1947 年「用三年时间撰写了60万字的《国际贸易实务》专著，著名学者马寅初先生为此书作序」；其后「他和董事们研究设计的“三经一纬”斜纹布，打开了南非、欧美及东南亚市场」；「属下公司70余家，产品远销各国，是六七十年代香港蜚声中外的纺织集团」。',
            u'港媒特稿（W07）：「他通過翻譯日本商業書籍《間接成本之研究》，驚覺中國的工業生產力遠遠落後於世界列強，遂引發他借外國經濟理論振興中國民族工業的念頭。」（繁体原文）',
        ],
        cases_en=[
            'Official biography (W02): in 1937 he published his translation of the Japanese edition of The Study of Indirect Costs.',
            'Official biography (W02): in 1947 he spent three years writing the 600,000-character monograph International Trade Practice, for which the famous scholar Ma Yinchu wrote a preface; later the three-warp-one-weft twill he and the directors designed opened the markets of South Africa, Europe, America and Southeast Asia; with more than 70 affiliated companies and products sold worldwide, it was a Hong Kong textile group renowned at home and abroad in the 1960s and 70s.',
            'Hong Kong press feature (W07): through translating the Japanese business book The Study of Indirect Costs, he realized with a shock that China\'s industrial productivity lagged far behind the world powers, which planted in him the idea of using foreign economic theory to revive China\'s national industry. (original in traditional Chinese)',
        ],
        modern_zh=[u'知识迁移与产业升级的联结', u'传统制造业的技术突破口选择', u'理论著述与经营实践的互哺'],
        modern_en=['Linking knowledge transfer to industrial upgrading',
                   'Choosing technological breakthroughs for traditional manufacturing',
                   'Mutual nourishment of theoretical writing and business practice'],
        related=[u'M-AZJ-003'],
        tier_note=u'tier=确证',
    ),
]

AUTHOR += [
    dict(
        code='M-AZJ-003', priority=3,
        name_zh=u'多语种国际游说', name_en='Multilingual Advocacy Method',
        pack_name=u'多语种国际游说：语言即竞争力',
        category=u'战略决策', category_raw=u'国际商务/语言战略',
        domain_zh=u'国际商务/语言战略', domain_en='International Business / Language Strategy',
        def_zh=u'把语言能力直接转化为谈判与游说能力：在校熟练掌握了英语后，于工作中刻苦自学日语、法语、德语和西班牙语；60 年代初香港纺织品出口受阻，他作为纺织团团长率队前往欧美国家游说，奔走于十几个国家，以当地语言发表演说打动受众，使香港纺织品一举进入欧美市场。边界：语言红利须与行业专业度结合，不可简化为「学外语=会经商」。',
        def_en=u"Turning language ability directly into negotiating and advocacy power: having mastered English at school, he taught himself Japanese, French, German and Spanish at work; when Hong Kong textile exports were blocked in the early 1960s, he led a textile mission to Europe and America as its head, travelling through more than a dozen countries and delivering speeches in local languages that moved his audiences, opening the European and American markets to Hong Kong textiles at a stroke. Boundary: the language dividend must be joined to professional expertise; it cannot be reduced to learning a foreign language and doing business.",
        source_chapter=u'AZJ-1 素材包 §二 M-AZJ-003；引据：《安子介先生生平》（新华社 2000，W02）／大公報（2009-09-19，W07）',
        concepts=[u'英语与日法德西四语自学', u'纺织团团长', u'奔走十几个国家', u'以当地语言演说', u'欧美市场突破'],
        qsrc=('M-AZJ-003', 4),
        quote_en=u"In different countries he could deliver speeches in different languages, and easily moved the hearts of local audiences. (Original in traditional Chinese.)",
        process_zh=[
            u'语言储备：校内熟练英语，工作后自学日语、法语、德语和西班牙语（W02）',
            u'危机识别：60 年代初香港纺织品出口受阻，被同行推荐为纺织团团长（W02）',
            u'跨国游说：率队奔走十几个国家，以当地语言发表演说（W02/W07）',
            u'结果：香港纺织品一举进入欧美市场（W02）',
        ],
        process_en=[
            'Language reserve: master English at school, then self-teach Japanese, French, German and Spanish at work (W02)',
            'Crisis recognition: with Hong Kong textile exports blocked in the early 1960s, peers recommend him to head the textile mission (W02)',
            'Cross-country advocacy: travel through more than a dozen countries, speaking in local languages (W02/W07)',
            'Result: Hong Kong textiles enter the European and American markets at a stroke (W02)',
        ],
        cases_zh=[
            u'官方生平（W02）：「他不仅在校读书时熟练掌握了英语，而且在工作中刻苦自学了日语、法语、德语和西班牙语，为他日后国际贸易生涯打下了良好基础。」',
            u'官方生平（W02）：60 年代初香港纺织品出口受阻，他「率队前往欧美国家游说。他备尝艰辛，先后奔走于十几个国家，使香港纺织品一举进入了欧美市场」。',
            u'港媒特稿（W07）：「他曾經試過十七天中睡了十三張床，時差之下，一天過兩個白晝或兩個夜晚也變成等閒。」「他在不同的國家，能以不同的語言發表演說，很容易便打動了當地人的心。」（繁体原文）；边界：语言红利须与专业度结合（素材包边界口径）。',
        ],
        cases_en=[
            'Official biography (W02): he not only mastered English while at school but also assiduously taught himself Japanese, French, German and Spanish at work, laying a good foundation for his later international trade career.',
            'Official biography (W02): when Hong Kong textile exports were blocked in the early 1960s, he led the mission to Europe and America; enduring great hardship, he travelled through more than a dozen countries and brought Hong Kong textiles into the European and American markets at a stroke.',
            'Hong Kong press feature (W07): in seventeen days he once slept in thirteen beds; under jet lag, a day with two daylight hours or two nights became ordinary; in different countries he could deliver speeches in different languages, and easily moved the hearts of local audiences. (original in traditional Chinese); Boundary: the language dividend must be joined to professional expertise (pack boundary).',
        ],
        modern_zh=[u'跨国经营中「多语+专业」复合人才的价值', u'区域经济体的国际化人才策略'],
        modern_en=['The value of multilingual-plus-professional talent in cross-border business',
                   'International talent strategy for regional economies'],
        related=[u'M-AZJ-002'],
        tier_note=u'tier=确证',
    ),
    dict(
        code='M-AZJ-004', priority=4,
        name_zh=u'体制内建言', name_en='Inside-the-System Advocacy Method',
        pack_name=u'体制内建言：从两局议员到基本法起草委员会副主任',
        category=u'政治治理', category_raw=u'政治参与/制度设计',
        domain_zh=u'政治参与/制度设计', domain_en='Political Participation / Institutional Design',
        def_zh=u'自港英立法局、行政局非官守议员（1970—1978）起步，历香港工业总会主席、香港贸易发展局主席，至回归过渡期出任香港基本法起草委员会副主任委员、基本法咨询委员会主任委员：先后主持了 8 次咨委会全体会议、30 余次执委会会议，向起草委员会递交了 57 份报告，完成从「殖民地体制内建言者」到制度设计参与者的身份演进。边界：政治路线随时代演进，不宜标签化；接见次数两说并存（见档案 caveats）。',
        def_en=u"From unofficial member of the Hong Kong Legislative and Executive Councils (1970-1978), through chairmanship of the Federation of Hong Kong Industries and the Hong Kong Trade Development Council, to deputy director of the Basic Law Drafting Committee and chairman of the Basic Law Consultative Committee in the transition years: he chaired 8 plenary meetings and more than 30 executive committee meetings of the Consultative Committee and submitted 57 reports to the Drafting Committee, completing the evolution from inside-the-system advocate under colonial governance to participant in institutional design. Boundary: his political line evolved with the times and should not be reduced to a label; the two accounts of the number of receptions stand side by side (see figure caveats).",
        source_chapter=u'AZJ-1 素材包 §二 M-AZJ-004；引据：廖晖讲话（2012，W01）／《安子介先生生平》（W02）／定海史志（W10）',
        concepts=[u'立法局非官守议员', u'行政局非官守议员', u'工业总会与贸发局主席', u'基本法起草委员会副主任委员', u'基本法咨询委员会主任委员'],
        qsrc=('M-AZJ-004', 4),
        quote_en=u"In July 1985 Mr Ann Tse Kai became deputy director of the Drafting Committee for the Basic Law of the Hong Kong Special Administrative Region, and in December of the same year was unanimously recommended by all sectors of Hong Kong as chairman of the Basic Law Consultative Committee.",
        process_zh=[
            u'入局：1970—1974 年任香港立法局非官守议员，1974—1978 年任行政局非官守议员（W02）',
            u'行业治理：1970—1975 年任香港工业总会主席；1975—1979 年任香港贸易发展局主席（W02）',
            u'制度设计：1985 年 7 月出任基本法起草委员会副主任委员，同年 12 月被推举为咨委会主任委员（W01）',
            u'工作留痕：主持 8 次咨委会全体会议、30 余次执委会会议，递交 57 份报告（W01）',
        ],
        process_en=[
            'Enter the councils: unofficial member of the Legislative Council 1970-1974 and of the Executive Council 1974-1978 (W02)',
            'Industry governance: chairman of the Federation of Hong Kong Industries 1970-1975; chairman of the Hong Kong Trade Development Council 1975-1979 (W02)',
            'Institutional design: deputy director of the Basic Law Drafting Committee from July 1985; recommended as chairman of the Consultative Committee that December (W01)',
            'Record of work: chairing 8 plenary and more than 30 executive meetings, submitting 57 reports (W01)',
        ],
        cases_zh=[
            u'官方生平（W02）：「1970年至1974年，任香港立法局非官守议员。1974年至1978年，任香港行政局非官守议员。」「1970年至1975年，任香港工业总会主席。」「1975年至1979年，任香港贸易发展局主席。」',
            u'官方讲话（W01）：「1985年7月，安子介先生出任香港特别行政区基本法起草委员会副主任委员，同年12月被香港各界一致推举为基本法咨询委员会主任委员。」「先后主持了8次咨委会全体会议，30余次执委会会议，向起草委员会递交了57份报告。」',
            u'两说并注（W10/W01）：W10 作「在起草基本法过程中，先后六次受到邓小平同志接见」；W01 作「邓小平、江泽民等党和国家领导同志曾先后七次亲切接见他」——并存待考，不得单取一说。',
        ],
        cases_en=[
            'Official biography (W02): from 1970 to 1974 he was an unofficial member of the Legislative Council; from 1974 to 1978 an unofficial member of the Executive Council; chairman of the Federation of Hong Kong Industries 1970-1975; chairman of the Hong Kong Trade Development Council 1975-1979.',
            'Official speech (W01): in July 1985 Mr Ann Tse Kai became deputy director of the Drafting Committee for the Basic Law of the Hong Kong Special Administrative Region, and that December was unanimously recommended by all sectors of Hong Kong as chairman of the Basic Law Consultative Committee; he chaired 8 plenary meetings and more than 30 executive committee meetings, and submitted 57 reports to the Drafting Committee.',
            'Two accounts recorded side by side (W10/W01): W10 says that in the course of drafting the Basic Law he was received six times by Comrade Deng Xiaoping; W01 says that Comrades Deng Xiaoping, Jiang Zemin and other Party and state leaders cordially received him seven times - both stand, neither may be taken alone.',
        ],
        modern_zh=[u'殖民地治理体系内「体制内建言」的空间与边界', u'制度转换期专业人士的角色转换条件'],
        modern_en=['The space and limits of inside-the-system advocacy under colonial governance',
                   'Conditions for professionals shifting roles in an institutional transition'],
        related=[u'M-AZJ-005', u'M-AZJ-010'],
        tier_note=u'tier=确证；接见次数两说（W01 七次／W10 六次）并注',
    ),
    dict(
        code='M-AZJ-005', priority=5,
        name_zh=u'「一国两制」早期理论贡献', name_en='Early One Country Two Systems Framework Method',
        pack_name=u'「一国两制」早期理论贡献：16 条建议与繁荣稳定框架',
        category=u'政治治理', category_raw=u'「一国两制」理论/政治战略',
        domain_zh=u'「一国两制」理论/政治战略', domain_en='One Country Two Systems Theory / Political Strategy',
        def_zh=u'制度变革期的「确定性供给」：1982 年应邀访问北京时提出「中英谈判应以保持香港繁荣稳定为大前提」的重要建议；1984 年在全国政协六届二次会议上提出「香港保持繁荣稳定16条」重要建议，并在香港报刊发表《保持香港繁荣之我见》等一系列文章，对稳定香港人心起到了积极作用（W01/W07 双源互证）。边界：「16 条」具体条目未在检索中获得，不得代拟内容。',
        def_en=u"Supplying certainty in an institutional transition: on an invited visit to Beijing in 1982 he proposed that China-Britain negotiations should take the maintenance of Hong Kong's prosperity and stability as the overarching premise; in 1984 he put forward at the second session of the Sixth National Committee of the CPPCC the important proposal known as the 16 points for maintaining Hong Kong's prosperity and stability, and published a series of articles including My Views on Maintaining Hong Kong's Prosperity, which played a positive role in steadying opinion in Hong Kong (two independent sources W01/W07). Boundary: the content of the 16 points was not obtained in the search and must not be invented.",
        source_chapter=u'AZJ-1 素材包 §二 M-AZJ-005；引据：廖晖讲话（2012，W01）／大公報（2009-09-19，W07，独立互证）',
        concepts=[u'中英谈判前提', u'香港保持繁荣稳定16条', u'《保持香港繁荣之我见》', u'稳定香港人心', u'1982 访京建言'],
        qsrc=('M-AZJ-005', 2),
        quote_en=u"In 1984 at the second session of the Sixth National Committee of the Chinese People's Political Consultative Conference, he put forward the important proposal of the 16 points for maintaining Hong Kong's prosperity and stability, and published a series of articles such as My Views on Maintaining Hong Kong's Prosperity in the Hong Kong press, which played a positive role in steadying opinion in Hong Kong.",
        process_zh=[
            u'设定前提：1982 年访京时提出「中英谈判应以保持香港繁荣稳定为大前提」的重要建议（W01）',
            u'提出建议：1984 年全国政协六届二次会议提出「香港保持繁荣稳定16条」重要建议（W01/W07）',
            u'撰文传播：在香港报刊发表《保持香港繁荣之我见》等一系列文章（W01）',
            u'稳定人心：上述建言与文章「对稳定香港人心起到了积极作用」（W01/W07）',
        ],
        process_en=[
            "Set the premise: propose on the 1982 visit to Beijing that China-Britain negotiations take the maintenance of Hong Kong's prosperity and stability as the overarching premise (W01)",
            'Put forward the proposal: the 16 points for maintaining Hong Kong\'s prosperity and stability at the 1984 CPPCC session (W01/W07)',
            'Publish: a series of articles including My Views on Maintaining Hong Kong\'s Prosperity in the Hong Kong press (W01)',
            'Steady opinion: the proposals and articles played a positive role in steadying opinion in Hong Kong (W01/W07)',
        ],
        cases_zh=[
            u'官方讲话（W01）：「1982年，安子介先生在应邀访问北京时提出中英谈判应以保持香港繁荣稳定为大前提的重要建议」。',
            u'官方讲话（W01）：「1984年，他在全国政协六届二次会议上提出“香港保持繁荣稳定16条”重要建议，并在香港报刊发表《保持香港繁荣之我见》等一系列文章，对稳定香港人心起到了积极作用。」',
            u'港媒独立互证（W07）：「一九八四年，即中英簽署聯合聲明的當年，他在全國政協會議上提出保持香港繁榮穩定的十六條建議，對穩定香港人心起到積極的作用。」（繁体原文）；边界：「16 条」具体条目未获，不得代拟（素材包边界口径）。',
        ],
        cases_en=[
            'Official speech (W01): in 1982, on an invited visit to Beijing, Mr Ann Tse Kai proposed that China-Britain negotiations should take the maintenance of Hong Kong\'s prosperity and stability as the overarching premise.',
            'Official speech (W01): in 1984 he put forward at the second session of the Sixth National Committee of the CPPCC the important proposal of the 16 points for maintaining Hong Kong\'s prosperity and stability, and published articles including My Views on Maintaining Hong Kong\'s Prosperity, playing a positive role in steadying opinion.',
            'Independent Hong Kong press corroboration (W07): in 1984, the year China and Britain signed the joint declaration, he proposed at the CPPCC session the sixteen points for maintaining Hong Kong\'s prosperity and stability, which played a positive role in steadying opinion. (original in traditional Chinese); Boundary: the content of the 16 points is not available and must not be drafted for him (pack boundary).',
        ],
        modern_zh=[u'制度变革期的「确定性供给」与舆论稳定策略', u'重大谈判中前提条件的设定艺术'],
        modern_en=['Supplying certainty and steadying opinion during institutional change',
                   'The art of setting premises in major negotiations'],
        related=[u'M-AZJ-004', u'M-AZJ-010'],
        tier_note=u'tier=确证（概述级；16 条条目内容未获）',
    ),
]

AUTHOR += [
    dict(
        code='M-AZJ-006', priority=6,
        name_zh=u'汉字解析教学法', name_en='Radical-Excision Teaching Method',
        pack_name=u'汉字解析教学法：「部首切除法」与对外汉字推广',
        category=u'教育传承', category_raw=u'语言文字学/教育方法/文化传播',
        domain_zh=u'语言文字学/教育方法/文化传播',
        domain_en='Chinese Character Studies / Teaching Method / Cultural Transmission',
        def_zh=u'以系统著述把汉字拆解教学法推向国际：1982 年英文版《解开汉字之谜》在香港出版、1990 年中文版，其后《劈文切字集》（1987）、《安子介现代千字文》系列（1991—1992）、《汉字易学》（1995）相继问世，把汉字拆解为部首与余部、结合字形演变与部件组合进行解析，降低外国人识字门槛（李光耀评价可证其国际影响）。边界：方法细节（「部首切除法」、170 个部首样本等）系百科词条转述，属疑似，不得写作确证级方法论定义。',
        def_en=u"Pushing a decomposition-based teaching approach onto the international stage through a systematic body of books: The Mystery of Chinese Characters (English edition 1982 in Hong Kong, Chinese edition 1990), followed by Pi Wen Qie Zi Ji (1987), the Ann Tse Kai Modern Thousand-Character Text series (1991-1992) and Chinese Characters Made Easy (1995) break characters into radicals and remainders and analyse them through script evolution and component combination, lowering the threshold for foreign learners (Lee Kuan Yew's remark attests to the international impact). Boundary: the method details (the radical-excision approach, the sample of 170 radicals and so on) come from an encyclopedia entry and remain suspected; they must not be written up as a confirmed methodological definition.",
        source_chapter=u'AZJ-1 素材包 §二 M-AZJ-006；引据：廖晖讲话（2012，W01）／百度百科《解开汉字之谜》词条（W09，转述）／百度百科「安子介」（W08）',
        concepts=[u'《解开汉字之谜》', u'《劈文切字集》', u'《安子介现代千字文》', u'《汉字易学》', u'部首切除法（疑似级）'],
        qsrc=('M-AZJ-006', 1),
        quote_en=u"In 1982 his English-language The Mystery of Chinese Characters was published in Hong Kong and drew wide attention from people and experts at home and abroad; Singapore's Senior Minister Lee Kuan Yew wittily said that if the book had been published before he began learning Chinese, he would have found Chinese easier to learn.",
        process_zh=[
            u'著述立基：1982 年英文版《解开汉字之谜》在香港出版，受海内外人士和专家广泛关注（W01）',
            u'方法成形：词条转述其「部首切除法」——把汉字拆为部首与余部、结合字形演变与部件组合解析（W09，疑似级）',
            u'体系化：先后写成中文简缩本、《劈文切字集》、《安子介现代千字文》启蒙篇、书写篇和繁简篇（W08）',
            u'国际推广：1995 年英文版《汉字易学》成为外国人学习汉字的热门书（W01）',
        ],
        process_en=[
            'Build the base: the English-language The Mystery of Chinese Characters is published in Hong Kong in 1982 and draws wide attention (W01)',
            'Method takes shape: according to the encyclopedia entry, the radical-excision approach splits characters into radical and remainder and analyses them via script evolution and component combination (W09, suspected)',
            'Systematize: Chinese abridged edition, Pi Wen Qie Zi Ji and the Ann Tse Kai Modern Thousand-Character Text series follow (W08)',
            'International promotion: the 1995 English-language Chinese Characters Made Easy becomes a popular book for foreign learners (W01)',
        ],
        cases_zh=[
            u'官方讲话（W01）：「1982年，他用英文撰写的《解开汉字之谜》在香港出版，受到海内外人士和专家广泛关注，新加坡资政李光耀曾风趣地说：“如果此书出版于我开始学习中文之前，我学习中文就会感到比较容易了。”」',
            u'官方讲话（W01）：「1995年，他用英文撰写的《汉字易学》成为外国人学习汉字的热门书。」；官方生平（W08）：「此后，又先后写成《解开汉字之谜》中文简缩本、《劈文切字集》、《安子介现代千字文》启蒙篇、书写篇和繁简篇等。」',
            u'疑似另注（W09，词条·内容简介）：「全书采用“部首切除法”解析汉字，分上下两册构建研究框架：上册从发音、部首定义及四角编码入手，分析170个部首的语义关联；下册通过字形演变、部件组合等维度，探讨笔画增减对字义的影响及汉字对称性特征」——保留疑似标记，不得据以写成确证级定义。',
        ],
        cases_en=[
            'Official speech (W01): in 1982 his English-language The Mystery of Chinese Characters was published in Hong Kong and drew wide attention from people and experts at home and abroad; Singapore Senior Minister Lee Kuan Yew wittily said that if the book had been published before he began learning Chinese, he would have found Chinese easier to learn.',
            'Official speech (W01): the 1995 English-language Chinese Characters Made Easy became a popular book for foreigners learning Chinese; official biography (W08): afterwards he also wrote the Chinese abridged edition of The Mystery of Chinese Characters, Pi Wen Qie Zi Ji, and the enlightenment, writing and traditional-simplified volumes of the Ann Tse Kai Modern Thousand-Character Text series.',
            'Suspected note (W09, entry content summary): the whole book uses the radical-excision approach to analyse characters in two volumes, the first analysing the semantic associations of 170 radicals and the second exploring stroke changes and symmetry through script evolution and component combination - it keeps its suspected mark and must not be used to write a confirmed definition.',
        ],
        modern_zh=[u'对外汉语教学的认知路径设计', u'「拆解—重组」教学法与汉字信息处理的同源关系（与 M-AZJ-007 呼应）'],
        modern_en=['Designing cognitive paths for teaching Chinese as a foreign language',
                   'The shared roots of decompose-and-recompose teaching and Chinese character information processing (cf. M-AZJ-007)'],
        related=[u'M-AZJ-001', u'M-AZJ-007'],
        tier_note=u'tier=确证（出版与推广事实）；方法细节=疑似（词条转述）',
    ),
    dict(
        code='M-AZJ-007', priority=7,
        name_zh=u'写字机与六位数编码', name_en='Six-Digit Coding and Writing Machine Method',
        pack_name=u'写字机与六位数编码：汉字信息化的原创发明',
        category=u'工程技术', category_raw=u'发明创造/知识产权/汉字现代化',
        domain_zh=u'发明创造/知识产权/汉字现代化',
        domain_en='Invention / Intellectual Property / Character Modernization',
        def_zh=u'把汉字信息化做成原创发明：1985 年发明「安子介式汉字笔形电脑编码法」——每个汉字取一个且只取一个部首赋予相应数码，将此部首「切除」后余部另赋数码，六位数字编码故无重码，纯数字键盘（0—9 加少量机能键）；并研制「安子介写字机」（显示、存储、编辑、修改、传输、打印 10 种文字）；获中、美、英、日、新加坡五国专利，以发明者姓氏命名属中国专利史首次；首台实物 2009 年由后人捐赠宁波帮博物馆。边界：属 1980 年代文字处理需求下的历史产物，历史价值大于当代实用价值。',
        def_en=u"Turning character informatization into original invention: in 1985 he invented the Ann Tse Kai-style Chinese character stroke-form computer coding method - each character takes one and only one radical, assigned a digit code, the rest after excising the radical takes another code, six digits make repetition-free codes, and the keyboard is numeric (0-9 plus a few function keys); he also developed the Ann Tse Kai writing machine (display, storage, editing, revision, transmission and printing of 10 kinds of script); the inventions obtained patents in China, the United States, Britain, Japan and Singapore, and naming by the inventor's surname was a first in Chinese patent history; the first machine was donated by his descendants to the Ningbo Bang Museum in 2009. Boundary: a historical product of 1980s word-processing needs, its historical value exceeds its current practical use.",
        source_chapter=u'AZJ-1 素材包 §二 M-AZJ-007；引据：专利文档《安子介式汉字笔形电脑编码法及其键盘》（1985-04-01 申请，W04）＋廖晖讲话（W01）＋宁波日报/中国宁波网（W05）＋维基百科（W03）',
        concepts=[u'安子介式汉字笔形电脑编码法', u'六位数字无重码', u'安子介写字机', u'五国专利', u'以发明者姓氏命名'],
        qsrc=('M-AZJ-007', 1),
        quote_en=u"The coding method of this invention is characterized in that each Chinese character takes one and only one radical to which a corresponding digit code is assigned; after this radical is excised the remainder takes another code, and the two codes together constitute the coding of this invention for the character; the keyboard of this invention is characterized in that it consists only of the single digit keys 0 to 9 and a small number of function keys governing all other functions. (Patent abstract.)",
        process_zh=[
            u'发明：1985 年发明「安子介式汉字笔形电脑编码法」——部首切除、六位数字、无重码、纯数字键盘（W04）',
            u'研制：设计「安子介写字机」，具显示、存储、编辑、修改、传输、打印 10 种文字的功能（W03）',
            u'专利：获中、美、英、日、新加坡五国专利，以发明者姓氏命名属中国专利史首次（W01/W05）',
            u'存续：首台「安子介写字机」2009 年由后人捐赠宁波帮博物馆（W05/W06/W08）',
        ],
        process_en=[
            'Invent: the Ann Tse Kai-style stroke-form computer coding method in 1985 - radical excision, six digits, repetition-free codes, numeric keyboard (W04)',
            'Develop: the Ann Tse Kai writing machine, able to display, store, edit, revise, transmit and print 10 kinds of script (W03)',
            'Patent: patents in China, the United States, Britain, Japan and Singapore; naming by the inventor\'s surname a first in Chinese patent history (W01/W05)',
            'Survive: the first machine donated by his descendants to the Ningbo Bang Museum in 2009 (W05/W06/W08)',
        ],
        cases_zh=[
            u'专利文档（W04，摘要）：「本发明的编码方法的特征是，每个汉字取一个且只取一个部首赋予相应的数码，将此部首“切除”后余下的部分赋予另一数码，这两部分数码合起来构成了此汉字的本发明的编码」；「采用把汉字分成部首和其余部分，分别按笔划规定赋予数字，组成编码，由于采用了六位数字，故无重码，此法亦给出了适用于欧美及日本文字的例子。」专利记录：申请号 CN85101817.3A；申请日/优先权 1985-04-01；公开日 1988-03-09；授权公告 CN1003890B。',
            u'官方讲话（W01）：「他还发明了“安子介汉字六位数电脑编码法”，研究设计的“安子介写字机”成功申请了中、美、英、日和新加坡等五国专利，对推广汉字、弘扬中华文化作出了积极贡献。」',
            u'新闻与百科（W05/W03）：「不仅得到中、美、英、日与新加坡５国专利，还以发明者姓氏命名，这在中国专利史上属首次。」（W05，原文全角数字５）「安子介中文写字机具有显示、存储、编辑、修改、传输、打印10种文字（包括中文和西方语言）的功能，获得中国、英国、美国、日本和新加坡共5国的发明专利」（W03）。',
        ],
        cases_en=[
            'Patent document (W04, abstract): the coding method is characterized in that each character takes one and only one radical assigned a corresponding digit code, the remainder after excising the radical takes another code, and the two together constitute the code of this invention for the character; the method divides characters into radical and remainder, assigns digits by stroke rules, and because six digits are used there are no duplicate codes, with examples also given for European, American and Japanese scripts. Patent record: application CN85101817.3A; filed 1985-04-01; published 1988-03-09; grant announcement CN1003890B.',
            'Official speech (W01): he also invented the Ann Tse Kai six-digit computer coding method for Chinese characters, and the Ann Tse Kai writing machine he designed obtained patents in China, the United States, Britain, Japan and Singapore, contributing to the promotion of Chinese characters and Chinese culture.',
            'News and encyclopedia (W05/W03): patents in China, the United States, Britain, Japan and Singapore, and naming by the inventor\'s surname, a first in Chinese patent history (W05, original uses a full-width digit 5); the Ann Tse Kai Chinese writing machine can display, store, edit, revise, transmit and print 10 kinds of script including Chinese and Western languages, and obtained invention patents in the five countries (W03).',
        ],
        modern_zh=[u'汉字信息化的早期自主技术路线', u'原创发明的国际化专利布局', u'发明物作为文化载体的叙事价值'],
        modern_en=['An early independent technological route for Chinese character informatization',
                   'International patent layout for an original invention',
                   'The narrative value of an invention as a cultural carrier'],
        related=[u'M-AZJ-001', u'M-AZJ-006'],
        tier_note=u'tier=确证（专利文档＋多源报道）',
    ),
    dict(
        code='M-AZJ-008', priority=8,
        name_zh=u'儒商传统', name_en='Scholar-Merchant Integration Method',
        pack_name=u'儒商传统：实业、学术与公益的三重身份整合',
        category=u'伦理修养', category_raw=u'企业家精神/社会贡献/文化人格',
        domain_zh=u'企业家精神/社会贡献/文化人格',
        domain_en='Entrepreneurship / Social Contribution / Cultural Character',
        def_zh=u'把实业家（南联）、学者（21 本专著）、政治参与者（全国政协副主席）与公益践行者整合为一体：以商业积累支撑学术与公益（赠送五万余册著作给全国各省市教委及有需要的贫困地区），以「我始终为香港人民服务」自任；港媒以「博学儒商」名之。边界：儒商人格具时代特殊性（20 世纪香港华人企业家群体背景），不宜过度普遍化；「博学儒商」为大公報标题用语，非官方定评。',
        def_en=u"Integrating industrialist (Nam Lian), scholar (21 monographs), political participant (vice chairman of the CPPCC National Committee) and philanthropist into one person: business accumulation supports scholarship and public welfare (more than 50,000 copies of his works donated to provincial and municipal education commissions and needy areas), and he held himself to the promise to serve the people of Hong Kong all his life; the Hong Kong press called him a learned scholar-merchant. Boundary: this scholar-merchant character is specific to its era (the 20th-century Hong Kong Chinese entrepreneur milieu) and should not be over-generalized; learned scholar-merchant is a Ta Kung Pao headline phrase, not an official verdict.",
        source_chapter=u'AZJ-1 素材包 §二 M-AZJ-008；引据：廖晖讲话（2012，W01）／大公報（2009-09-19，W07）／定海史志（W10）',
        concepts=[u'我始终为香港人民服务', u'热心公益', u'赠书五万余册', u'博学儒商（港媒用语）', u'三重身份整合'],
        qsrc=('M-AZJ-008', 1),
        quote_en=u"Mr Ann Tse Kai was devoted to public welfare all his life, held many public posts, and by his exemplary conduct kept the promise that he would always serve the people of Hong Kong.",
        process_zh=[
            u'创业立身：参与创建华南染厂、中南纺织厂、永南纺织厂，1969 年起任南联实业董事会主席（W02）',
            u'公职服务：担任香港工业总会主席、贸发局主席及立法局、行政局非官守议员等多项社会公职（W02）',
            u'公益践行：赠送五万余册著作给全国各省市教委及有需要的贫困地区（W01）',
            u'身份整合：实业家＋学者＋政治参与者统一于「我始终为香港人民服务」的自任（W01，港媒以「博学儒商」名之）',
        ],
        process_en=[
            'Build the enterprise: help found the South China Dyeing Works, the Zhongnan Textile Mill and the Wing Nam Textile Mill; chairman of Nam Lian from 1969 (W02)',
            'Public service: chairman of the Federation of Hong Kong Industries and the Trade Development Council, unofficial member of the Legislative and Executive Councils, and other public posts (W02)',
            'Philanthropy: donate more than 50,000 copies of his works to provincial and municipal education commissions and needy areas (W01)',
            'Integrate identities: industrialist, scholar and political participant united in the promise to serve the people of Hong Kong all his life (W01; the Hong Kong press called him a learned scholar-merchant)',
        ],
        cases_zh=[
            u'官方讲话（W01）：「安子介先生一生热心公益，担任过多项社会公职，以自己的模范行为践行了“我始终为香港人民服务”的诺言。」',
            u'官方讲话（W01）：「他十分关注内地的扫盲工作，赠送五万余册著作给全国各省市教委及有需要的贫困地区。」',
            u'港媒与地方志（W07/W10）：大公報标题《安子介──博學儒商 保港繁榮》引述「「你是不是中國人？中國人就要愛中國。」　這話，出自一位熟悉多國語言的中國人。」（报道级引语，未见直接采访出处）；定海史志：「他艰苦创业，服务社会，热心公益，与人为善。他虚怀若谷，勤奋好学，勇于实践，博学多才，著述丰厚。」',
        ],
        cases_en=[
            'Official speech (W01): Mr Ann Tse Kai was devoted to public welfare all his life and held many public posts, by his exemplary conduct keeping the promise that he would always serve the people of Hong Kong.',
            'Official speech (W01): he paid close attention to literacy work on the mainland, donating more than 50,000 copies of his works to provincial and municipal education commissions and needy areas.',
            'Hong Kong press and local gazetteer (W07/W10): the Ta Kung Pao headline Ann Tse Kai - Learned Scholar-Merchant, Guardian of Hong Kong\'s Prosperity quotes the line "Aren\'t you Chinese? If you are Chinese you must love China", words from a Chinese familiar with many languages (a report-level quotation with no direct interview source); the Dinghai gazetteer: he built his enterprise through hardship, served society, was devoted to public welfare and kind to others; modest and eager to learn, courageous in practice, broadly learned and prolific in writing.',
        ],
        modern_zh=[u'企业家的社会责任与个人志趣统一', u'知识型创业者的多重身份整合模型'],
        modern_en=['Uniting an entrepreneur\'s social responsibility with personal pursuits',
                   'A model of multi-identity integration for knowledge-based founders'],
        related=[u'M-AZJ-009'],
        tier_note=u'tier=确证（三源）；引语「你是不是中国人」为报道引述',
    ),
]

AUTHOR += [
    dict(
        code='M-AZJ-009', priority=9,
        name_zh=u'教育公益与学术激励', name_en='Educational Philanthropy and Academic Incentive Method',
        pack_name=u'教育公益与学术激励：安子介国际贸易研究奖',
        category=u'教育传承', category_raw=u'教育资助/学术激励/学界与业界互动',
        domain_zh=u'教育资助/学术激励/学界与业界互动',
        domain_en='Educational Endowment / Academic Incentive / Academy-Industry Interaction',
        def_zh=u'实业反哺学术的长期机制：1991 年在北京出资设立「安子介国际贸易研究奖」（对外经济贸易大学承办），颁奖典礼自 1996 年开始举办，推动中国国际贸易理论研究；并历任多所院校名誉教授（1976 年后获香港中文大学名誉法学博士，被聘为北京对外经济贸易大学、清华大学、广州对外贸易学院、江西师范大学等院校名誉教授）。奖项延续，至 2012 年已第十七届。边界：「最高学术奖」为维基转述之评价语，引用须注明口径。',
        def_en=u"A long-term mechanism of returning industry gains to scholarship: in 1991 he endowed the Ann Tse Kai International Trade Research Award in Beijing (administered by the University of International Business and Economics), with award ceremonies held from 1996 onwards, promoting research on China's international trade theory; he also served as honorary professor at several institutions (honorary Doctor of Laws from the Chinese University of Hong Kong after 1976, honorary professorships at the University of International Business and Economics, Tsinghua University, Guangzhou Institute of Foreign Trade, Jiangxi Normal University and others). The award continues, reaching its seventeenth round by 2012. Boundary: the phrase highest academic award is an evaluative rendering in the encyclopedia and must be cited with that qualifier.",
        source_chapter=u'AZJ-1 素材包 §二 M-AZJ-009；引据：廖晖讲话（2012，W01）／《安子介先生生平》（W02）／维基百科（W03，转述）',
        concepts=[u'安子介国际贸易研究奖', u'对外经济贸易大学承办', u'1996 年首颁', u'名誉教授', u'实业反哺学术'],
        qsrc=('M-AZJ-009', 1),
        quote_en=u"In 1991 he set up the Ann Tse Kai International Trade Research Award in Beijing, playing a positive role in promoting the teaching and research of international trade theory in China.",
        process_zh=[
            u'出资设立：1991 年在北京设立「安子介国际贸易研究奖」，推动中国国际贸易理论研究（W01/W02）',
            u'承办与颁奖：由对外经济贸易大学承办，颁奖典礼自 1996 年开始举办（W03，转述口径）',
            u'学术身份：获香港中文大学名誉法学博士，并任多所院校名誉教授（W02/W10）',
            u'长期延续：奖项在国内外国贸研究领域声誉卓著，至 2012 年已第十七届（W03）',
        ],
        process_en=[
            'Endow: the Ann Tse Kai International Trade Research Award is set up in Beijing in 1991 to promote research on international trade theory in China (W01/W02)',
            'Administer and award: administered by the University of International Business and Economics, with ceremonies from 1996 onwards (W03, transmission)',
            'Academic standing: honorary Doctor of Laws from the Chinese University of Hong Kong and honorary professorships at several institutions (W02/W10)',
            'Longevity: the award becomes renowned in international trade research at home and abroad, reaching its seventeenth round by 2012 (W03)',
        ],
        cases_zh=[
            u'官方讲话（W01）：「1991年，他在北京设立“安子介国际贸易研究奖”，为促进中国国际贸易理论教学研究发挥了积极作用。」',
            u'官方生平（W02）：「他还于1991年在北京设立“安子介国际贸易研究奖”，为中国国际贸易理论教学研究作出了贡献。」「1976年后，荣获香港中文大学名誉法学博士，并被聘为北京对外经济贸易大学、清华大学、广州对外贸易学院、江西师范大学等院校名誉教授。」',
            u'维基转述（W03，繁体原文）：「為推動我國在國際貿易領域的研究1991年安先生出資設立“安子介國際貿易研究獎”（簡稱“安獎”），頒獎典禮由1996年開始舉辦，在國內外國際貿易研究領域中聲譽卓著，具有較大影響力，被視為中國國際經貿領域中的最高學術獎。」——「最高学术奖」为转述评价语，引用须注明口径。',
        ],
        cases_en=[
            'Official speech (W01): in 1991 he set up the Ann Tse Kai International Trade Research Award in Beijing, playing a positive role in promoting the teaching and research of international trade theory in China.',
            'Official biography (W02): he also set up the Ann Tse Kai International Trade Research Award in Beijing in 1991, contributing to China\'s international trade theory teaching and research; after 1976 he received an honorary Doctor of Laws from the Chinese University of Hong Kong and was appointed honorary professor at the University of International Business and Economics, Tsinghua University, Guangzhou Institute of Foreign Trade, Jiangxi Normal University and other institutions.',
            'Encyclopedia transmission (W03, original in traditional Chinese): to promote research in China\'s international trade field, in 1991 Mr Ann endowed the Ann Tse Kai International Trade Research Award (the Ann Award), with ceremonies from 1996, renowned in the field at home and abroad and regarded as the highest academic award in China\'s international economics and trade field - the phrase highest academic award is a transmitted evaluative rendering and must be cited with that qualifier.',
        ],
        modern_zh=[u'个人设立学术奖项的治理与延续机制', u'实业界与学术界的制度化互动样本'],
        modern_en=['Governance and continuity mechanisms for an individually endowed academic award',
                   'A model of institutionalized interaction between industry and academia'],
        related=[u'M-AZJ-008'],
        tier_note=u'tier=确证（官方讲话＋维基＋百科）；奖项细节为维基转述（可核二手）',
    ),
    dict(
        code='M-AZJ-010', priority=10,
        name_zh=u'晚年使命', name_en='Late-Life Public Mission Method',
        pack_name=u'晚年使命：香港回归与平稳过渡的担当',
        category=u'政治治理', category_raw=u'「一国两制」实践/政治担当/生命史',
        domain_zh=u'「一国两制」实践/政治担当/生命史',
        domain_en='One Country Two Systems Practice / Political Commitment / Life History',
        def_zh=u'晚年使命：约七十岁前后（已到「從心所欲」之年）拟退政商界、全力研究汉字，因八十年代香港回归进程启动而毅然「出山」，把最后十五年投入基本法起草、咨委工作与特区筹组（历任香港基本法起草委员会副主任委员、基本法咨询委员会主任委员、香港事务顾问、特区筹委会预备工作委员会副主任委员、特区筹委会副主任委员）；1988 年因劳累过度突发心脏病，在病床上仍心系起草进度；2000-06-03 病逝香港，丧礼以国家领导人最高规格举殡（灵柩覆盖国旗）。边界：享年 87/88 两说；「国葬」为维基与港媒表述，官方通稿未用该词，引用须注明口径。',
        def_en=u"A late-life mission: at about seventy (the age of following his heart's desire) he planned to leave politics and business to study Chinese characters full time, but when the Hong Kong handover process began in the 1980s he resolutely stepped out again, devoting his last fifteen years to Basic Law drafting, consultative work and SAR preparation (deputy director of the Basic Law Drafting Committee, chairman of the Basic Law Consultative Committee, Hong Kong affairs adviser, deputy director of the Preliminary Working Committee of the SAR Preparatory Committee and of the Preparatory Committee itself); in 1988 overwork brought on a heart attack, yet in his sickbed he still worried about the drafting schedule; he died in Hong Kong on 3 June 2000, and his funeral was held with the highest protocol for a state leader, his coffin draped with the national flag. Boundary: the two accounts of his age at death, 87 and 88; the word state funeral comes from the encyclopedia and Hong Kong press, not the official communique, and citations must note this.",
        source_chapter=u'AZJ-1 素材包 §二 M-AZJ-010；引据：大公報（2009-09-19，W07）／《安子介先生生平》（W02）／廖晖讲话（W01）／维基百科（W03）',
        concepts=[u'毅然出山', u'基本法起草与咨委', u'特区筹组', u'1988 年心脏病发仍系起草进度', u'国家领导人规格举殡'],
        qsrc=('M-AZJ-010', 1),
        quote_en=u"Ann Tse Kai, already at the age of following his heart's desire, had originally intended to step down from politics and business and devote himself to the study of Chinese characters. In the end he could not follow his heart, because the 1980s set in motion the process of Hong Kong's return to the motherland, and he resolutely stepped out again. (Original in traditional Chinese.)",
        process_zh=[
            u'拟退隐：已到「從心所欲」之年，原本打算从政商界退下来，全力研究汉字（W07）',
            u'毅然出山：八十年代香港回归进程启动，他投身过渡期事务（W07）',
            u'投入：先后担任基本法起草委员会副主任委员、咨委会主任委员、香港事务顾问、特区筹委会（预备工作委员会）副主任委员（W02）',
            u'坚守：1988 年因劳累过度突发心脏病，在病床上仍心系咨委会工作与起草进度（W01）',
        ],
        process_en=[
            'Planned retirement: at the age of following his heart\'s desire he intended to leave politics and business and study Chinese characters full time (W07)',
            'Stepping out again: with the handover process under way in the 1980s he took on transition-era duties (W07)',
            'Commitment: deputy director of the Basic Law Drafting Committee, chairman of the Consultative Committee, Hong Kong affairs adviser, deputy director of the SAR Preparatory Committee and its Preliminary Working Committee (W02)',
            'Perseverance: overwork brought on a heart attack in 1988, yet in his sickbed he still cared about the consultative committee and the drafting schedule (W01)',
        ],
        cases_zh=[
            u'港媒特稿（W07）：「已到「從心所欲」之年的安子介，原本打算從政商界退下來，全力研究漢字。但是他最終未能從心所欲，因為八十年代，啟動了香港回歸祖國進程，他毅然「出山」。」（繁体原文）',
            u'官方生平（W02）：「在香港回归祖国的历程中，先后担任香港基本法起草委员会副主任委员、香港特别行政区基本法咨询委员会主任委员、香港事务顾问、香港特别行政区筹备委员会预备工作委员会副主任委员、香港特别行政区筹备委员会副主任委员。」',
            u'身后哀荣（W01/W03/W07）：W01 记「1988年，他因劳累过度突发心脏病，在病床上仍然不忘咨委会工作，关心基本法起草进度」；W03 记其丧礼以国家领导人最高规格举殡、灵柩覆盖国旗；W07 独立互证「二○○○年六月三日，全國政協副主席安子介病逝於香港。國旗披身，他的喪禮以國家最高規格進行」。边界：享年 87/88 两说、「国葬」口径须注明（见档案 caveats）。',
        ],
        cases_en=[
            'Hong Kong press feature (W07): Ann Tse Kai, already at the age of following his heart\'s desire, had originally intended to step down from politics and business and devote himself to the study of Chinese characters; in the end he could not follow his heart, because the 1980s set in motion the process of Hong Kong\'s return to the motherland, and he resolutely stepped out again. (original in traditional Chinese)',
            'Official biography (W02): in the course of Hong Kong\'s return he served successively as deputy director of the Basic Law Drafting Committee, chairman of the Basic Law Consultative Committee, Hong Kong affairs adviser, deputy director of the Preliminary Working Committee of the SAR Preparatory Committee and deputy director of the Preparatory Committee.',
            'Posthumous honours (W01/W03/W07): W01 records that in 1988 overwork brought on a heart attack and in his sickbed he still did not forget the consultative committee\'s work and the drafting schedule; W03 records that his funeral was held with the highest protocol for a state leader and his coffin draped with the national flag; W07 independently corroborates that on 3 June 2000 Vice Chairman of the CPPCC National Committee Ann Tse Kai died in Hong Kong, the national flag over him and his funeral conducted with the highest state protocol. Boundary: the two accounts of his age (87/88) and the state-funeral wording must be qualified (see figure caveats).',
        ],
        modern_zh=[u'政治人物的「二次入世」与历史机遇担当', u'制度过渡期个体的健康、意志与角色负荷管理'],
        modern_en=['A political figure\'s second entry into public life and the seizing of historical opportunity',
                   'Managing health, willpower and role load during an institutional transition'],
        related=[u'M-AZJ-004', u'M-AZJ-005'],
        tier_note=u'tier=确证（四源）；享年与「国葬」口径两说并注',
    ),
]

# ---------------------------------------------------------------- figure 档案要素
FIG_TAGS = [u'安子介', 'Ann Tse Kai', u'汉字现代化', u'解开汉字之谜', u'劈文切字集',
            u'安子介现代千字文', u'汉字易学', u'安子介式汉字笔形电脑编码法', u'安子介写字机',
            u'五国专利', u'南联实业', u'三经一纬', u'香港基本法', u'一国两制', u'全国政协副主席',
            u'大紫荆勋章', u'儒商', u'宁波帮博物馆']
FIG_CROSS_REFS = []
FIG_CAVEATS = [
    u'享年 87/88 两说：官方讣告口径 88 岁（W02/W11）；W03 信息框作 87 岁（周岁）——本档从官方口径并注两存。',
    u'接见次数两说：W01 作「先后七次」；W10 作「六次受到邓小平同志接见」——并置待考，不得单取一说。',
    u'大紫荆勋章日期两说：W01 记 1997-07-02 授予；W03 记 1997-06-25——两存。',
    u'「国葬」用词口径：W03（维基）与 W07（港媒）表述为国家领导人最高规格/「国葬」；官方通稿（W11）未用「国葬」二字——引用须注明口径。',
    u'「第五大发明」本人原话原件未获（官方讲话转述 W01）；「二十一世纪是汉字发挥威力」仅见词条/书目转述链（W09）——保留 pending，不得升级为确证引文。',
    u'写手机捐赠者表述：W05/W06 作「后代」；W08 作「孙子安宇昭」——并存（本档采「后人（孙安宇昭）」双注）。',
    u'子安如磐合作发明编码法：仅见 W10 单源——标疑似事实，不作确证。',
    u'关联人物（廖晖、周文轩、周忠继、唐翔千、董建华、霍英东等）与关联机构在库内暂无对应 figure 码，故 cross_references 为空并如实登记（待后续建链）。',
    u'疑似项与待核项集中在 AZJ-1 素材包 §五（10 项）；本档保留 pending 标记、未升级、未代拟。',
]
FIG_WORKS = [
    u'《间接成本之研究》（1937，翻译出版）',
    u'《国际贸易实务》（1947，马寅初作序）',
    u'《陆沉》（1938 初版；1988 再版）',
    u'《解开汉字之谜》（1982 英文版；1990 中文版）',
    u'《劈文切字集》（1987）',
    u'《安子介现代千字文》系列（1991—1992）',
    u'《汉字易学》（1995）',
    u'《保持香港繁荣之我见》（1984 香港报刊文章）',
]
FIG_CORE_THOUGHTS = [a['name_zh'] for a in AUTHOR]


def build_figure():
    fig = dict()
    fig['schema_version'] = 'v6'
    fig['id'] = FIG
    fig['code'] = FIG
    fig['figure_name'] = FIG_NAME
    fig['figure_code'] = FIG
    fig['figure_pinyin'] = 'Ann Tse Kai'
    fig['birth_year'] = 1912
    fig['death_year'] = 2000
    fig['era'] = u'现代/Modern Era'
    fig['time_period_standardized'] = '1912-2000'
    fig['nationality'] = u'中国'
    fig['ethnicity'] = u'汉族'
    fig['school'] = u'汉字学（汉字现代化）/ 国际贸易实务'
    fig['intellectual_tradition'] = u'汉字本位文化观/儒商传统（据 AZJ-1 素材包域标签综合）'
    fig['courtesy_name'] = ''
    fig['style_name'] = ''
    fig['representative_works'] = list(FIG_WORKS)
    fig['historical_significance'] = (
        u'安子介（Ann Tse Kai，1912-06-26—2000-06-03），浙江定海人，生于上海，杰出的社会活动家、著名爱国人士、'
        u'香港知名实业家（W01/W02/W11 官方称号）。第八、九届全国政协副主席（1993—2000），第六、七届全国政协常委；'
        u'历任香港立法局、行政局非官守议员（1970—1978）、香港工业总会主席（1970—1975）、香港贸易发展局主席（1975—1979）'
        u'（W02/W10）。回归过渡期任香港基本法起草委员会副主任委员、基本法咨询委员会主任委员等职（W01/W02），'
        u'主持 8 次咨委会全体会议、30 余次执委会会议，递交 57 份报告（W01）。文字学方面，1979—1995 年撰 21 本汉字学专著，'
        u'著《解开汉字之谜》（1982）、《劈文切字集》（1987）、《安子介现代千字文》（1991—1992）、《汉字易学》（1995）'
        u'（W01/W02/W08）；1985 年发明汉字笔形电脑编码法与「安子介写字机」，获中、美、英、日、新加坡五国专利（W04/W05/W01）；'
        u'1991 年设「安子介国际贸易研究奖」（W01/W02/W03）。身后以国家领导人最高规格举殡，灵柩覆盖国旗（W03/W07；官方通稿 W11 未用「国葬」字样）。'
    )
    fig['core_thoughts'] = list(FIG_CORE_THOUGHTS)
    fig['famous_quote'] = u'我始终为香港人民服务'
    fig['famous_quote_source'] = u'廖晖《在纪念安子介先生诞辰100周年座谈会上的讲话》（2012-06-27；W01）引其自述诺言；AZJ-1 素材包 §二 M-AZJ-008'
    fig['influence'] = (
        u'安子介以「汉字是中国第五大发明和中华文化之根」的文化判断贯通学术、实业与公共事务（W01）：文字学上以 21 本专著与'
        u'《解开汉字之谜》等书推动汉字研究与对外推广，并以编码法与写字机开启汉字信息化的早期自主技术路线（W04/W05）；'
        u'回归过渡期以「中英谈判应以保持香港繁荣稳定为大前提」（1982）与「香港保持繁荣稳定16条」（1984）等建言稳定人心（W01/W07），'
        u'并主持基本法咨询工作（W01）；1991 年设立「安子介国际贸易研究奖」形成实业反哺学术的长期机制（W01/W02/W03）。'
    )
    fig['tags'] = list(FIG_TAGS)
    fig['cross_references'] = [dict(x) for x in FIG_CROSS_REFS]
    fig['meta'] = {
        'source': u'AZJ-1 素材包（docs/research/phase21r9_anzijie_sourcing_report.md/.json；见证 W01—W11）',
        'methodology': u'Phase21-R9 重建落盘：以 AZJ-1 素材包逐条引文重锚；H-AZJ-345 判死清档件及其旧载荷零复用；疑似项保留 pending',
        'validation': u'verification pending（10 条）；引文与素材包逐字比对由 verify_phase21r9_azj.py 执行；入库前须走独立核验流程',
        'generation_date': DATE,
        'mode_count': 10,
        'figure_code_ref': FIG,
        'phase': u'Phase 21-R9',
    }
    fig['related_figures'] = [r['target_figure_code'] for r in FIG_CROSS_REFS]
    fig['thinking_mode_count'] = 10
    fig['mode_ids'] = list(CODES)
    fig['mode_ids_note'] = (
        u'安子介重做（Phase21-R9）：H-AZJ-345「安子介（特区叙事）」已判死清档，其旧载荷号段与叙事禁止复用；'
        u'本档按 AZJ-1 素材包重新立项，新码 H-AZJ-001 / M-AZJ-001~010（落盘前全库查重 0 碰撞，见 manifest preflight）。'
    )
    fig['caveats'] = list(FIG_CAVEATS)
    return fig


def entry_from_author(a):
    e = dict()
    e['id'] = a['code']
    e['mode_code'] = a['code']
    e['figure_code'] = FIG
    e['figure_name'] = FIG_NAME
    e['name_zh'] = a['name_zh']
    e['name_en'] = a['name_en']
    e['category'] = a['category']
    e['category_raw'] = a['category_raw']
    e['domain_zh'] = a['domain_zh']
    e['domain_en'] = a['domain_en']
    e['level'] = u'核心'
    e['priority'] = a['priority']
    e['definition_zh'] = a['def_zh']
    e['definition_en'] = a['def_en']
    e['source_chapter'] = a['source_chapter']
    e['key_concepts'] = list(a['concepts'])
    e['key_quote_zh'] = QF(*a['qsrc'])
    e['key_quote_en'] = a['quote_en']
    e['process_zh'] = list(a['process_zh'])
    e['process_en'] = list(a['process_en'])
    e['representative_cases_zh'] = list(a['cases_zh'])
    e['representative_cases_en'] = list(a['cases_en'])
    e['modern_applications_zh'] = list(a['modern_zh'])
    e['modern_applications_en'] = list(a['modern_en'])
    e['related_modes'] = list(a['related'])
    e['legacy_mode_id'] = ''
    e['verification'] = {
        'status': 'pending',
        'method': 'phase21r9-azj-rebuild-landing',
        'evidence': u'引文逐字取自 AZJ-1 素材包 §二 %s（quotes 第 %d 段；见证 %s）；层级：%s；核验 pending，入库前须走独立核验流程' % (
            a['qsrc'][0], a['qsrc'][1], QW(*a['qsrc']), a['tier_note']),
        'checked_at': DATE,
        'checker': 'elcano',
    }
    return e


def build_modes_file(entries):
    return {
        'schema_version': 'v6',
        'code': FIG,
        'figure_name_zh': FIG_NAME,
        'figure_name_en': FIG_NAME_EN,
        'mode_count': 10,
        'modes': entries,
    }


def fragments(text):
    out = []
    for opener, closer in ((u'\u300c', u'\u300d'), (u'\u300e', u'\u300f')):
        i = 0
        while True:
            a = text.find(opener, i)
            if a < 0:
                break
            b = text.find(closer, a + 1)
            if b < 0:
                break
            out.append(text[a + 1:b])
            i = b + 1
    return out


def frag_sources(seg, mid):
    pm = PM[mid]
    hits = []
    for i, q in enumerate(pm['quotes']):
        if seg in q.get('text', ''):
            hits.append('quotes#%d(%s)' % (i + 1, q.get('w', '')))
    for f in ('summary', 'boundary', 'modern', 'theme', 'tier', 'name'):
        v = pm.get(f, '')
        if isinstance(v, str) and seg in v:
            hits.append('pack.' + f)
    if seg in PACK_MD_TEXT:
        hits.append('pack_md')
    return hits

# ---------------------------------------------------------------- 顶层块提案（合并卡 t_ce457734 用）
TOP_BLOCK = {
    'schema_version': 'v6',
    'code': FIG,
    'name_zh': u'安子介：汉字现代化·实业升级·「一国两制」建言',
    'name_en': 'Ann Tse Kai: Chinese-Character Modernization · Industrial Upgrading · One Country Two Systems Advocacy',
    'era': u'现代/Modern Era (1912-2000)',
    'historical_domains': [u'语言文字学（汉字现代化）', u'实业经济（纺织工业、国际贸易）', u'政治（「一国两制」/基本法/政协）', u'教育公益', u'发明创造/知识产权'],
    'domains': [u'汉字现代化', u'实业与国际贸易', u'基本法与过渡期治理', u'教育公益', u'汉字信息化发明'],
    'core_modes': list(CODES),
    'gender': 'Male',
    'ethnicity': u'汉族 / Han Chinese',
    'nationality': u'中国 / China',
    'civilization_sphere': u'现代中国/香港/汉字文化与一国两制过渡治理 / Modern China / Hong Kong / Chinese Character Culture and One Country Two Systems Transition',
    'time_period_standardized': '1912-2000 CE',
    'primary_language': u'现代汉语 / Modern Mandarin',
    'intellectual_tradition': u'汉字本位文化观/儒商传统/国际贸易实务 / Han-Character Nativism / Scholar-Merchant Tradition / International Trade Practice',
    'unique_thinking_zh': (
        u'安子介（Ann Tse Kai，1912-2000），浙江定海人，香港知名实业家与文字学家，第八、九届全国政协副主席。'
        u'其思路以「汉字是中国第五大发明和中华文化之根」的文化判断为原点（W01 讲话转述口径），贯通四线：'
        u'一是文字学本体——1979—1995 年撰 21 本专著，以《解开汉字之谜》《劈文切字集》《安子介现代千字文》《汉字易学》'
        u'构建对外汉字解析与推广体系（W01/W02/W08）；二是汉字信息化——1985 年发明笔形电脑编码法与「安子介写字机」，'
        u'获五国专利、以发明者姓氏命名属中国专利史首次（W04/W05/W01）；三是实业路径——译书启智、理论著述、'
        u'「三经一纬」技术创新与南联集团化（W02/W07）；四是回归过渡期建言——1982 年提「中英谈判应以保持香港繁荣稳定为大前提」，'
        u'1984 年提「香港保持繁荣稳定16条」，并任基本法起草委副主任、咨委会主任（W01/W07）。'
        u'疑似项（「第五大发明」原话、16 条条目、接见次数、享年 87/88 等）保留 pending 并注两说。'
    ),
    'unique_thinking_en': (
        u'Ann Tse Kai (1912-2000), from Dinghai, Zhejiang, was a renowned Hong Kong industrialist and scholar of Chinese characters, '
        u'and vice chairman of the Eighth and Ninth CPPCC National Committees. His thinking starts from the cultural judgment that Chinese '
        u'characters are "China\'s fifth great invention and the root of Chinese culture" (per the official speech, W01) and runs through four lines: '
        u'(1) character scholarship - 21 monographs written 1979-1995, building a system of decomposition-based analysis and overseas promotion '
        u'through The Mystery of Chinese Characters, Pi Wen Qie Zi Ji, the Ann Tse Kai Modern Thousand-Character Text and Chinese Characters Made Easy '
        u'(W01/W02/W08); (2) character informatization - the 1985 stroke-form computer coding method and the Ann Tse Kai writing machine, patented in five '
        u'countries, with naming by the inventor\'s surname a first in Chinese patent history (W04/W05/W01); (3) an industrial path - translation, theoretical '
        u'writing, the three-warp-one-weft technical innovation and Nam Lian group operation (W02/W07); (4) transition-era advocacy - the 1982 proposal that '
        u'China-Britain negotiations take Hong Kong\'s prosperity and stability as the overarching premise, the 1984 16 points, and his posts as deputy director '
        u'of the Basic Law Drafting Committee and chairman of the Consultative Committee (W01/W07). Suspected items (the original wording of the fifth great '
        u'invention, the content of the 16 points, the number of receptions, age 87/88) keep pending marks with both accounts noted.'
    ),
    'mode_evidence': [
        {'mode_id': u'M-AZJ-001', 'example_zh': u'汉字的「中国第五大发明」与「中华文化之根」判断（W01/W08）', 'example_en': 'Chinese characters as the fifth great invention and the root of Chinese culture (W01/W08)'},
        {'mode_id': u'M-AZJ-002', 'example_zh': u'译书启智→理论著述→「三经一纬」→南联集团化（W02/W07）', 'example_en': 'From translation to theory to the three-warp-one-weft twill and group operation (W02/W07)'},
        {'mode_id': u'M-AZJ-003', 'example_zh': u'五语能力与纺织团十几国游说（W02/W07）', 'example_en': 'Five-language ability and the textile mission across a dozen countries (W02/W07)'},
        {'mode_id': u'M-AZJ-004', 'example_zh': u'两局议员→基本法起草委副主任、咨委会主任（W02/W01）', 'example_en': 'From the two councils to the Basic Law committees (W02/W01)'},
        {'mode_id': u'M-AZJ-005', 'example_zh': u'1982 访京前提建议与 1984「香港保持繁荣稳定16条」（W01/W07）', 'example_en': 'The 1982 premise proposal and the 1984 sixteen points (W01/W07)'},
        {'mode_id': u'M-AZJ-006', 'example_zh': u'《解开汉字之谜》等与「部首切除法」解析（W01/W08/W09 疑似）', 'example_en': 'The Mystery of Chinese Characters and radical-excision analysis (W01/W08/W09 suspected)'},
        {'mode_id': u'M-AZJ-007', 'example_zh': u'1985 编码法与写字机、五国专利（W04/W05/W01）', 'example_en': 'The 1985 coding method, writing machine and five-country patents (W04/W05/W01)'},
        {'mode_id': u'M-AZJ-008', 'example_zh': u'「我始终为香港人民服务」与赠书五万余册（W01/W07/W10）', 'example_en': 'Serving the people of Hong Kong and donating over 50,000 books (W01/W07/W10)'},
        {'mode_id': u'M-AZJ-009', 'example_zh': u'1991 年设立「安子介国际贸易研究奖」（W01/W02/W03）', 'example_en': 'The 1991 Ann Tse Kai International Trade Research Award (W01/W02/W03)'},
        {'mode_id': u'M-AZJ-010', 'example_zh': u'晚年「出山」与 2000 年国家领导人规格举殡（W07/W03/W01）', 'example_en': 'Stepping out again in late life; the 2000 funeral with state-level protocol (W07/W03/W01)'},
    ],
    'key_texts': [u'《间接成本之研究》（1937，译）', u'《国际贸易实务》（1947）', u'《陆沉》（1938/1988）', u'《解开汉字之谜》（1982）', u'《劈文切字集》（1987）', u'《安子介现代千字文》（1991—1992）', u'《汉字易学》（1995）', u'专利 CN85101817A（1985）'],
    'key_concepts': [u'中国第五大发明', u'汉字现代化', u'三经一纬', u'安子介写字机', u'香港保持繁荣稳定16条', u'博学儒商'],
    'intellectual_lineage': [u'汉字本位文化观（据官方讲话转述）', u'儒商传统（港媒与地方志口径）', u'国际贸易实务理论（马寅初序）'],
    'legacy_assessment': (
        u'安子介横跨实业、文字学与公共事务：文字学上以 21 本专著与对外推广著述推动汉字研究与教育（W01/W02/W08），'
        u'技术上以编码法与写字机留下汉字信息化早期自主路线（W04/W05）；公共事务上以基本法咨询工作与过渡期建言参与「一国两制」实践（W01/W02/W07）。'
        u'待核事项（疑似与两说）集中登记于 AZJ-1 素材包 §五，评估按三档分层使用。'
    ),
    'scholarly_value': u'汉字现代化与对外汉字教育、1980 年代汉字信息化发明、香港过渡期「体制内建言」与儒商型公共人物的标本性史料（W01—W11）。',
}

SCENARIO_NOTES = {
    'figure_code': FIG,
    'notes': {
        'scenarios_zh_new': 0,
        'scenarios_en_new': 0,
        'reason': u'场景注册属合并卡（t_ce457734）范围；H-AZJ-345 全链已清档（t_3669eb4a），本链无旧场景需处置（判死件含场景一律禁止复用）。',
        'old_code_dispositions': [],
        'legacy_scan': {
            'live_scenarios_zh_AZJ': 0,
            'live_scenarios_en_AZJ': 0,
            'archived_AZJ345_scenarios': u'见 data/figures/_duplicates/H-AZJ-345_*（历史证据件，保留不触，禁止复用）',
        },
    },
}


def write_top_block_proposal(path):
    obj = {
        'schema_version': 'v6',
        'card': CARD,
        'figure_code': FIG,
        'target': u'data/modes_data.json 顶层块「H-AZJ-001」（新增；H-AZJ-345 旧块已判死清档，非替换）',
        'proposal': TOP_BLOCK,
    }
    wj(path, obj)


def write_tsv(path, rows, header):
    lines = ['\t'.join(header)]
    for r in rows:
        lines.append('\t'.join(r))
    with io.open(path, 'w', encoding='utf-8') as f:
        f.write(u'\n'.join(lines) + u'\n')


# ---------------------------------------------------------------- 查重扫描
OWN_NEW = [
    'data/figures/%s.json' % FIG, 'data/figures/%s_modes.json' % FIG,
    'data/individuals/%s.json' % FIG, 'data/individuals/%s_modes.json' % FIG,
    'tools/build_phase21r9_azj.py', 'verify_phase21r9_azj.py',
    'data/audit/phase21r9_azj_landing_manifest.json',
]
OWN_PREFIXES = [
    'docs/scratch/legacy20_r9_azj_landing/', 'docs/research/phase21r9_azj_',
    'docs/scratch/phase21r9_azj_rebuild/',
]
PACK_MENTIONS = ['docs/research/phase21r9_anzijie_sourcing_report.md',
                 'docs/research/phase21r9_anzijie_sourcing_report.json']
PACK_PREFIXES = ['docs/scratch/phase21r9_anzijie/']


def classify(rel, tok):
    if rel in OWN_NEW or any(rel.startswith(p) for p in OWN_PREFIXES):
        return 'own_new'
    if rel in PACK_MENTIONS or any(rel.startswith(p) for p in PACK_PREFIXES):
        return 'azj1_pack'
    if rel.startswith('data/figures/_duplicates/') or rel.startswith('data/backup') \
            or rel.startswith('backups') or '.bak' in rel:
        return 'archive_evidence'
    if rel.startswith('release/v2.0.0/'):
        return 'release_frozen'
    if rel.startswith('docs/research/phase21r7_') or rel.startswith('docs/research/phase21r8_') \
            or rel.startswith('docs/qa/phase21r8_') or rel.startswith('data/audit/phase21r8'):
        return 'r7r8_docs'
    if rel.startswith('site_docs/'):
        return 'build_nav'
    if rel in ('api/data/semantic_index_metadata.pkl', 'data/semantic_index_metadata.pkl'):
        return 'semantic_index'
    if rel == 'protreptic.db':
        return 'offline_legacy_db'
    if rel.startswith('docs/research/_archive/'):
        return 'archive_evidence'
    if rel.startswith('docs/research/phase21r6C_') or rel.startswith('docs/research/phase21w6_'):
        return 'r7r8_docs'
    if rel.startswith('docs/architecture/') or rel.startswith('docs/review/'):
        return 'docs_history'
    if rel in ('tools/add_batch2.py', 'verify_azj345_clear.py'):
        return 'tools_history'
    return 'UNCLASSIFIED'


def scan_tokens():
    files = []
    out = subprocess.check_output(['git', '-C', REPO, 'ls-files'], text=True)
    files += [f for f in out.split('\n') if f]
    out2 = subprocess.check_output(['git', '-C', REPO, 'ls-files', '--others', '--exclude-standard'], text=True)
    files += [f for f in out2.split('\n') if f]
    res = dict(scanned=0, hits={}, buckets={}, live_hits={})
    for rel in sorted(set(files)):
        fp = os.path.join(REPO, rel)
        if not os.path.isfile(fp):
            continue
        try:
            txt = io.open(fp, encoding='utf-8', errors='ignore').read()
        except Exception:
            continue
        res['scanned'] += 1
        toks = []
        if 'M-AZJ-' in txt:
            toks.append('M')
        if 'H-AZJ-' in txt:
            toks.append('H')
        if u'安子介' in txt:
            toks.append('AZJ_TEXT')
        if toks:
            b = classify(rel, toks)
            res['hits'][rel] = dict(tokens=toks, bucket=b)
            res['buckets'].setdefault(b, []).append(rel)
        if rel in MAIN_LIB:
            live = []
            if 'AZJ' in txt:
                live.append('AZJ')
            if u'安子介' in txt:
                live.append('AZJ_TEXT')
            if live:
                res['live_hits'][rel] = live
    return res


def zero_lib_check():
    before = dict((f, sha_file(os.path.join(REPO, f))) for f in MAIN_LIB)
    return before


def assert_zero_lib(before):
    after = dict((f, sha_file(os.path.join(REPO, f))) for f in MAIN_LIB)
    bad = [f for f in MAIN_LIB if before[f] != after[f]]
    assert not bad, 'library write detected: %r' % bad
    return after


# ---------------------------------------------------------------- 引文表 / 片段登记
def quote_table(entries):
    rows = []
    for a, e in zip(AUTHOR, entries):
        mid, idx = a['qsrc']
        q = PM[mid]['quotes'][idx - 1]
        rows.append(dict(
            entry=e['id'], pack_mode=mid, quote_index=idx, witness=q.get('w', ''),
            note=q.get('note', ''), pack_chars=len(q.get('text', '')),
            key_quote_chars=len(e['key_quote_zh']),
            pack_raw_substring=(e['key_quote_zh'] in q.get('text', '')),
            tier=a['tier_note'],
        ))
    return rows


def frag_register(entries):
    reg = []
    for a, e in zip(AUTHOR, entries):
        blob = u'\n'.join([e['definition_zh'], e['source_chapter']] + e['process_zh'] +
                          e['representative_cases_zh'] + e['modern_applications_zh'] + e['key_concepts'])
        seen = []
        for f in fragments(blob):
            for s in [x for x in f.split(u'……') if x]:
                srcs = frag_sources(s, a['qsrc'][0])
                seen.append(dict(entry=e['id'], fragment=s, sources=srcs))
        reg.append(seen)
    return reg

# ---------------------------------------------------------------- 落盘与 manifest
def landing_paths():
    return [
        os.path.join(LANDING, 'modes_library_entries.json'),
        os.path.join(LANDING, 'combined_library_entries.json'),
        os.path.join(LANDING, 'id_mapping.tsv'),
        os.path.join(LANDING, 'category_mapping.tsv'),
        os.path.join(LANDING, 'scenario_notes.json'),
        os.path.join(LANDING, 'top_block_proposal.json'),
        os.path.join(LANDING, 'figures/%s.json' % FIG),
        os.path.join(LANDING, 'figures/%s_modes.json' % FIG),
        os.path.join(LANDING, 'individuals/%s.json' % FIG),
        os.path.join(LANDING, 'individuals/%s_modes.json' % FIG),
    ]


def data_paths():
    return [
        os.path.join(REPO, 'data/figures/%s.json' % FIG),
        os.path.join(REPO, 'data/figures/%s_modes.json' % FIG),
        os.path.join(REPO, 'data/individuals/%s.json' % FIG),
        os.path.join(REPO, 'data/individuals/%s_modes.json' % FIG),
    ]


def archive_files():
    root = os.path.join(REPO, 'data/figures/_duplicates')
    return [os.path.join(root, n) for n in sorted(os.listdir(root)) if 'H-AZJ-345' in n]


def main():
    summary = {}
    # 0) 主库写前指纹
    lib_before = zero_lib_check()
    # 1) 预检：全库查重（码/名）与 live 层零残留
    pf = scan_tokens()
    m_bad = [r for r, v in pf['hits'].items() if 'M' in v['tokens'] and v['bucket'] not in ('own_new', 'azj1_pack')]
    unclassified = pf['buckets'].get('UNCLASSIFIED', [])
    summary['preflight'] = dict(scanned=pf['scanned'],
                                buckets=dict((k, len(v)) for k, v in pf['buckets'].items()),
                                live_hits=pf['live_hits'], m_collisions=m_bad,
                                unclassified=unclassified)
    assert not pf['live_hits'], 'live layer AZJ residue: %r' % pf['live_hits']
    assert not m_bad, 'M-AZJ collision: %r' % m_bad
    assert not unclassified, 'unclassified AZJ hits: %r' % unclassified
    # 2) 条目组装与不变量
    entries = [entry_from_author(a) for a in AUTHOR]
    assert len(entries) == 10
    for i, (a, e) in enumerate(zip(AUTHOR, entries), 1):
        assert e['id'] == 'M-AZJ-%03d' % i, e['id']
        assert e['priority'] == i
        assert e['category'] in STD_CATEGORIES, e['category']
        assert list(e.keys()) == ENTRY_KEYS, list(e.keys())
        assert e['legacy_mode_id'] == ''
    # 3) 引文与片段核验
    qt = quote_table(entries)
    assert all(r['pack_raw_substring'] for r in qt), [r for r in qt if not r['pack_raw_substring']]
    reg = frag_register(entries)
    frag_fail = [(d['entry'], d['fragment']) for rows in reg for d in rows if not d['sources']]
    assert not frag_fail, 'fragment without source: %r' % frag_fail[:8]
    # 4) 组装 figure / individuals / modes
    fig = build_figure()
    fig['modes'] = entries
    ind = dict((k, v) for k, v in fig.items() if k != 'modes')
    mf = build_modes_file(entries)
    # 5) 数据面落盘
    wj(data_paths()[0], fig)
    wj(data_paths()[1], mf)
    wj(data_paths()[2], ind)
    wj(data_paths()[3], mf)
    # 6) 落地包
    wj(landing_paths()[0], entries)
    wj(landing_paths()[1], dict(schema_version='v6', modes=entries))
    write_tsv(landing_paths()[2], [
        ['—', a['code'], a['name_zh'], a['name_en'], a['pack_name'],
         u'重做链新码，无 legacy 号（H-AZJ-345 判死清档件号段禁止复用）'] for a in AUTHOR],
        [u'legacy_id', u'v6_id', u'name_zh', u'name_en', u'pack_name', u'note'])
    write_tsv(landing_paths()[3], [
        ['—', a['code'], a['category_raw'], a['category'], 'pack_theme_as_category_raw', ''] for a in AUTHOR],
        [u'legacy_mode_id', u'v6_id', u'category_raw', u'category', u'status', u'candidate_target'])
    wj(landing_paths()[4], SCENARIO_NOTES)
    write_top_block_proposal(landing_paths()[5])
    # 7) 冻结副本（与 data 侧逐字节一致）
    for src, dst in ((data_paths()[0], landing_paths()[6]), (data_paths()[1], landing_paths()[7]),
                     (data_paths()[2], landing_paths()[8]), (data_paths()[3], landing_paths()[9])):
        dd = os.path.dirname(dst)
        if not os.path.isdir(dd):
            os.makedirs(dd)
        with open(src, 'rb') as f:
            blob = f.read()
        with open(dst, 'wb') as f:
            f.write(blob)
        assert sha_file(src) == sha_file(dst)
    # 8) 主库写后校验
    lib_after = assert_zero_lib(lib_before)
    arch = dict((os.path.basename(p), sha_file(p)) for p in archive_files())
    # 9) manifest
    dl = {}
    for p in data_paths() + landing_paths():
        rel = os.path.relpath(p, REPO)
        dl[rel] = dict(sha256=sha_file(p), bytes=os.path.getsize(p))
    quotes_total = sum(len(m['quotes']) for m in PACK['modes'])
    man = {
        'schema_version': 'v1',
        'card': CARD,
        'figure_code': FIG,
        'figure_name': FIG_NAME,
        'date': DATE,
        'baseline_commit': subprocess.check_output(['git', '-C', REPO, 'rev-parse', '--short', 'HEAD'], text=True).strip(),
        'pack_sha256': {os.path.basename(PACK_JSON): sha_file(PACK_JSON), os.path.basename(PACK_MD): sha_file(PACK_MD)},
        'counts': dict(modes=10, quotes=quotes_total, key_quotes=10,
                       witness_texts=len([n for n in os.listdir(WITNESS) if n.startswith('W')]),
                       witness_dir_files=len(os.listdir(WITNESS)),
                       data_files=4, landing_files=10),
        'deliverables': dl,
        'preflight': summary['preflight'],
        'quote_table': qt,
        'frag_register': reg,
        'zero_library_write': dict(before=lib_before, after=lib_after, untouched=lib_before == lib_after),
        'archive_untouched': arch,
        'hard_fixes': [
            {'item': u'禁用复用', 'action': u'H-AZJ-345 判死清档件及其旧载荷号段、叙事零引用；本档全字段零出现 H-AZJ-345 内容'},
            {'item': u'疑似不升级', 'action': u'「第五大发明」原话、16 条条目、170 部首样本、「二十一世纪是汉字发挥威力」等均保留 pending/疑似标记'},
            {'item': u'两说并存', 'action': u'享年 87/88、接见六次/七次、大紫荆 1997-06-25/07-02 并注于 caveats 与相应条目'},
            {'item': u'零自造句', 'action': u'definition/process/cases 全部以素材包引文与概述为据；英文面为中文内容之译写（注明为重建卡译写）'},
        ],
    }
    wj(os.path.join(REPO, 'data/audit/phase21r9_azj_landing_manifest.json'), man)
    summary['counts'] = man['counts']
    summary['deliverables'] = sorted(dl.keys())
    summary['frag_count'] = sum(len(r) for r in reg)
    print(json.dumps(summary, ensure_ascii=False, indent=1))


if __name__ == '__main__':
    main()
