#!/usr/bin/env python3
"""
Batch 2: Mao Zedong 6 Phases
Codes: M-JGS-280 through M-WN-285
"""
import json

with open('scenarios_zh.json', 'r', encoding='utf-8') as f:
    zh = json.load(f)
with open('scenarios_en.json', 'r', encoding='utf-8') as f:
    en = json.load(f)
with open('code_maps.json', 'r', encoding='utf-8') as f:
    cm = json.load(f)

figures = [
    {
        'code': 'M-JGS-280',
        'name_zh': '毛泽东·井冈山期 (1927-1929)：星星之火/农村包围城市/武装割据/建立根据地',
        'name_en': 'Mao Zedong · Jinggangshan Period (1927-1929): Spark/ Rural Encirclement/ Armed Separation/ Base Building',
        'desc_zh': '秋收起义后上井冈山，创立第一个农村革命根据地，确立"工农武装割据"道路，提出"星星之火，可以燎原"，以弱胜强开辟中国革命新道路。',
        'desc_en': 'After Autumn Harvest Uprising, went to Jinggangshan, established first rural revolutionary base, established "worker-peasant armed separation" path, proposed "a single spark can start a prairie fire", weak-over-strong opened new path for Chinese revolution.',
        'modes': [4, 3, 6, 14, 15],
        'reason_zh': '毛泽东在井冈山期以"农村包围城市"战略破解城市革命失败困局，建立"工农武装割据"新型政权形式，创"三大纪律八项注意"军民关系新模式，成中国革命战略转折/根据地建设/军队建设三维奠基。',
        'reason_en': 'Mao Zedong in Jinggangshan period broke urban revolution deadlock with "rural encirclement of cities" strategy, established "worker-peasant armed separation" new regime form, created "Three Disciplines Eight Points" new civil-military model, becoming Chinese revolution strategic turning/base building/army building three-dimensional foundation.',
        'steps_zh': ['战略转折：放弃城市起义路线，转向农村包围城市，确立农民为革命主力', '根据地建立：宁冈/茅坪/大柏地/龙市/苏家埠五大据点，建政权/分土地/武装割据', '军队建设：确立"党指挥枪/三大纪律八项注意/官兵平等/开展群众工作"建军原则', '统一战线：联合袁文才/王佐部队，实行"打土豪/分田地"土地政策，巩固工农联盟', '思想奠基：《井冈山斗争》《星星之火可以燎原》确立农村包围城市理论雏形'],
        'steps_en': ['Strategic Pivot: Abandon urban uprising line, turn to rural encirclement, establish peasants as revolutionary main force', 'Base Establishment: Five strongholds Ninggang/Maoping/Dabai/Longshi/Sujiabu, build regime/distribute land/armed separation', 'Army Building: Establish "party commands gun/Three Disciplines Eight Points/officer-soldier equality/mass work" army building principles', 'United Front: Unite Yuan Wencai/Wang Zuo troops, implement "strike landlords/distribute land" land policy, consolidate worker-peasant alliance', 'Ideological Foundation: "Struggle in Jinggangshan"/"Single Spark Can Start Prairie Fire" establish rural encirclement theory prototype'],
        'expected_zh': '成中国革命农村包围城市/武装割据/红军建设三维奠基，井冈山根据地成为中国革命摇篮',
        'expected_en': 'Become Chinese revolution rural encirclement/armed separation/Red Army building three-dimensional foundation, Jinggangshan base becomes cradle of Chinese revolution',
        'case_zh': '1927年9月秋收起义后上井冈山，1928年4月朱德/陈毅部队会师，建立湘赣边界根据地。1929年1月下井冈山，留下"星星之火可以燎原""工农武装割据""三大纪律八项注意"三大遗产。影响朱德/彭德怀/林彪/陈毅/贺龙/粟裕军事/根据地/统战全版图。',
        'case_en': 'Went to Jinggangshan after Autumn Harvest Uprising Sept 1927, Zhu De/Chen Yi forces joined April 1928, established Hunan-Jiangxi border base. Left Jinggangshan Jan 1929, left three legacies: "single spark can start prairie fire"/"worker-peasant armed separation"/"three disciplines eight points". Influenced Zhu De/Peng Dehuai/Lin Biao/Chen Yi/He Long/Su Yu military/base/united front entire map.'
    },
    {
        'code': 'M-CZ-281',
        'name_zh': '毛泽东·长征期 (1934-1936)：战略转移/遵义会议/确立领袖/四渡赤水/战略大转移',
        'name_en': 'Mao Zedong · Long March Period (1934-1936): Strategic Transfer/ Zunyi Conference/ Leadership Established/ Four Crossings Chishui/ Strategic Great Transfer',
        'desc_zh': '第五次反围剿失败后被迫长征，遵义会议确立领袖地位，指挥四渡赤水/巧渡金沙江/飞渡泸定桥/爬雪山/过草地，完成二万五千里战略大转移，保存革命火种。',
        'desc_en': 'Forced into Long March after 5th Encirclement failure, Zunyi Conference established leadership, commanded Four Crossings Chishui River/clever crossing Jinsha River/forced crossing Luding Bridge/climbing snow mountains/crossing grasslands, completed 25,000 li strategic great transfer, preserved revolutionary spark.',
        'modes': [3, 14, 15, 16, 11],
        'reason_zh': '毛泽东在长征期以遵义会议确立核心领导地位，指挥四渡赤水等军事奇迹，完成二万五千里战略大转移，将红军从灭亡边缘带到陕北，成中国革命生死存亡/军事指挥/领袖确立三维转折。',
        'reason_en': 'Mao Zedong in Long March period established core leadership at Zunyi Conference, commanded military miracles like Four Crossings Chishui, completed 25,000 li strategic great transfer, brought Red Army from brink of destruction to Shaanxi, becoming Chinese revolution life-death/military command/leadership establishment three-dimensional turning point.',
        'steps_zh': ['遵义确立：1935年1月遵义会议结束"左"倾统治，确立毛泽东核心领导地位，成革命生死转折', '四渡赤水：大渡河/金沙江/乌江/赤水河四渡赤水，运动战/佯攻/迂回/诱敌，甩开数十万追兵', '巧渡金沙江：佯攻宜宾/实渡上江/渡口/诱敌西进/主力东渡，神兵天降渡江南', '飞渡泸定桥/爬雪山/过草地：敢死队飞夺泸定桥，翻越夹金山/查拉山等大雪山，穿越草地死生不渝', '陕北落脚：1935年10月到达吴起镇，1936年10月到达保安，完成战略大转移，保存革命火种'],
        'steps_en': ['Zunyi Establishment: Jan 1935 Zunyi Conference ended "left" rule, established Mao core leadership, revolutionary life-death turning', 'Four Crossings Chishui: Dadu/Jinsha/Wu/Chishui rivers four crossings, maneuver/feint/detour/lure, shook off hundreds of thousands pursuers', 'Clever Jinsha Crossing: Feint Yibin/real cross Shangjiang/ferry/lure enemy west/main force east cross, divine troops cross south', 'Seize Luding Bridge/Climb Snow Mountains/Cross Grasslands: Daredevil squad seized Luding Bridge, crossed Jiajin/Chala snow mountains, traversed grasslands life-death unwavering', 'Shaanbei Foothold: Oct 1935 reached Wuqi Town, Oct 1936 reached Baoan, completed strategic great transfer, preserved revolutionary spark'],
        'expected_zh': '成中国革命生死存亡/军事指挥艺术/领袖地位确立三维转折，长征成中国革命史诗/精神图腾',
        'expected_en': 'Become Chinese revolution life-death/military command art/leadership establishment three-dimensional turning, Long March becomes Chinese revolutionary epic/spirit totem',
        'case_zh': '1934年10月中央红军长征出发，8.6万人出发，到陕北仅7000余人。遵义会议/四渡赤水/巧渡金沙江/飞渡泸定桥/爬雪山/过草地，二万五千里。其"遵义确立/运动战/战略转移/精神图腾"四大算子，成中国革命生死转折/军事指挥/领袖确立三维教科书。',
        'case_en': 'Oct 1934 Central Red Army Long March departure, 86K departed, only 7K reached Shaanxi. Zunyi/Four Crossings Chishui/Clever Jinsha/Seize Luding/Climb Snow/Cross Grasslands, 25,000 li. Four operators: Zunyi establishment/maneuver war/strategic transfer/spirit totem, becoming Chinese revolution life-death turning/military command/leadership textbook.'
    },
    {
        'code': 'M-YA-282',
        'name_zh': '毛泽东·延安期 (1935-1947)：整风运动/大生产运动/党的建设/统一战线/延安整风',
        'name_en': 'Mao Zedong · Yan\'an Period (1935-1947): Rectification/ Great Production/ Party Building/ United Front/ Yan\'an Rectification',
        'desc_zh': '在延安十三年，领导整风运动确立马克思主义指导地位，发动大生产运动实现经济自给，建立党的思想/组织/作风建设体系，推动抗日民族统一战线，为全国胜利奠基。',
        'desc_en': 'In 13 years in Yan\'an, led Rectification Movement establishing Marxism guiding position, launched Great Production Movement achieving economic self-sufficiency, built party ideology/organization/style building system, promoted Anti-Japanese National United Front, laid foundation for nationwide victory.',
        'modes': [10, 6, 18, 26, 28],
        'reason_zh': '毛泽东在延安期以整风运动统一全党思想/确立毛泽东思想指导地位，以大生产运动破解经济封锁/实现自给自足，以党的建设/统一战线/军事斗争三位一体，成中国革命根据地治理/党的建设/统一战线三维集大成。',
        'reason_en': 'Mao Zedong in Yan\'an period unified party thinking with Rectification/established Mao Zedong Thought guiding position, broke economic blockade with Great Production/achieved self-sufficiency, party building/united front/military struggle trinity, becoming Chinese revolutionary base governance/party building/united front three-dimensional synthesis.',
        'steps_zh': ['整风运动：1942-1944年反主观主义/宗派主义/党八股，实现全党马克思主义思想统一，确立毛泽东思想指导地位', '大生产运动：1939年发动"自己动手/丰衣足食"，南泥湾屯田/纺织/造纸/制盐，破解经济封锁实现自给', '党的建设：《论联合政府》《党内通知》确立思想/组织/作风三大建设，批评与自我批评/民主集中制/群众路线制度化', '统一战线：抗日民族统一战线/民主联盟/知识分子政策，争取中间势力/孤立顽固派/团结一切可以团结的力量', '军事斗争：百团大战/延安保卫战/陕甘宁保卫战，游击战/运动战/根据地巩固，为反攻奠基'],
        'steps_en': ['Rectification Movement: 1942-1944 anti-subjectivism/sectarianism/party jargon, achieved party-wide Marxism ideological unity, established Mao Zedong Thought guiding position', 'Great Production Movement: 1939 launched "do it yourself/food and clothing", Nanniwan land reclamation/textile/papermaking/salt, broke economic blockade achieved self-sufficiency', 'Party Building: "On Coalition Government"/"Inner-Party Circular" established ideology/org/style three constructions, criticism-self-criticism/democratic centralism/mass line institutionalized', 'United Front: Anti-Japanese National United Front/democratic league/intellectual policy, win middle forces/isolate diehards/unite all uniteable forces', 'Military Struggle: Hundred Regiments Offensive/Yan\'an Defense/Shaanganning Defense, guerrilla/maneuver/base consolidation, laid foundation for counteroffensive'],
        'expected_zh': '成中国革命根据地治理/党的建设/统一战线三维集大成，延安成革命圣地/毛泽东思想形成地',
        'expected_en': 'Become Chinese revolutionary base governance/party building/united front three-dimensional synthesis, Yan\'an becomes revolutionary holy land/Mao Zedong Thought birthplace',
        'case_zh': '1935年10月到达陕北，1947年3月撤离延安。整风/大生产/党建/统战/军事五大支柱。《实践论》《矛盾论》《新民主主义论》《论联合政府》等哲学/政治著作集中产出。其"整风统一思想/大生产破封锁/党建制度化/统战最大化/军事保根据地"五大算子，成中国革命根据地/党建/统战三维教科书。',
        'case_en': 'Oct 1935 reached Shaanbei, Mar 1947 left Yan\'an. Rectification/Great Production/Party Building/United Front/Military five pillars. "On Practice"/"On Contradiction"/"New Democracy"/"On Coalition Government" philosophy/political works concentrated output. Five operators: rectification unify thought/great production break blockade/party building institutionalize/united front maximize/military defend base, becoming Chinese revolutionary base/party building/united front three-dimensional textbook.'
    },
    {
        'code': 'M-JG-283',
        'name_zh': '毛泽东·建国初期 (1949-1957)：新民主主义/工业化/土地改革/抗美援朝/读书笔记',
        'name_en': 'Mao Zedong · Early PRC (1949-1957): New Democracy/ Industrialization/ Land Reform/ Resist US Aid Korea/ Reading Notes',
        'desc_zh': '新中国成立后，确立新民主主义过渡总路线，推进土地改革/工业化/三大改造，领导抗美援朝保家卫国，大量阅读马列经典/中国历史/哲学著作，撰写大量读书笔记，为国家建设奠基。',
        'desc_en': 'After PRC founding, established New Democracy transition general line, advanced land reform/industrialization/three major transformations, led Resist US Aid Korea defending homeland, extensively read Marxist classics/Chinese history/philosophy, wrote massive reading notes, laid foundation for nation building.',
        'modes': [1, 22, 18, 14, 25],
        'reason_zh': '毛泽东建国初期以新民主主义总路线统领国家建设，土地改革消灭封建地主阶级，抗美援朝确立国际地位，工业化奠定工业基础，大量读书笔记体现理论联系实际，成新中国政治/经济/军事/思想四维奠基。',
        'reason_en': 'Mao Zedong early PRC period led nation building with New Democracy general line, land reform eliminated feudal landlord class, Resist US Aid Korea established international status, industrialization laid industrial foundation, massive reading notes embodied theory-practice unity, becoming new China politics/economy/military/thought four-dimensional foundation.',
        'steps_zh': ['新民主主义：确立"由新民主主义到社会主义"过渡总路线，没收官僚资本/没收地主土地/保护民族工商业', '土地改革：1950年《土地改革法》颁布，3亿农民分得7亿亩土地，消灭封建地主阶级/解放生产力', '抗美援朝：1950-1953年"保家卫国"，志愿军与美军对决，确立新中国国际地位/打破美军不可战胜神话', '工业化建设：一五计划/156项重点工程/苏援项目，钢铁/机械/能源/化工/国防工业体系初步建立', '读书笔记：大量阅读马列/中国史/哲学/经济学，撰写《政治经济学读书笔记》《中国史读书笔记》等，理论联系实际'],
        'steps_en': ['New Democracy: Establish "New Democracy to Socialism" transition general line, confiscate bureaucrat capital/landlord land/protect national industry-commerce', 'Land Reform: 1950 Land Reform Law promulgated, 300M peasants received 700M mu land, eliminated feudal landlord class/unleashed productivity', 'Resist US Aid Korea: 1950-1953 "defend homeland", Volunteers vs US forces, established new China international status/broke US invincibility myth', 'Industrialization: First Five-Year Plan/156 key projects/Soviet aid, steel/machinery/energy/chemical/defense industrial system preliminarily established', 'Reading Notes: Extensively read Marxist/Chinese history/philosophy/economics, wrote "Political Economy Reading Notes"/"Chinese History Reading Notes", theory-practice unity'],
        'expected_zh': '成新中国政治/经济/军事/思想四维奠基，土地改革/抗美援朝/工业化/理论创新四大支柱',
        'expected_en': 'Become new China politics/economy/military/thought four-dimensional foundation, land reform/resist US aid Korea/industrialization/theoretical innovation four pillars',
        'case_zh': '1949年开国大典，1950年土地改革法/抗美援朝，1953年一五计划/三大改造，1956年高级知识分子问题/十大关系。读书笔记贯穿始终，1950-1976年读书笔记超百万字。其"新民主主义/土地改革/抗美援朝/工业化/读书笔记"五大算子，成新中国建设/理论创新/实践探索三维教科书。',
        'case_en': '1949 founding ceremony, 1950 Land Reform Law/Resist US Aid Korea, 1953 First Five-Year/Three Transformations, 1956 intellectuals/ten relations. Reading notes throughout, 1950-1976 reading notes >1M words. Five operators: new democracy/land reform/resist US aid/industrialization/reading notes, becoming new China construction/theoretical innovation/practical exploration three-dimensional textbook.'
    },
    {
        'code': 'M-TS-284',
        'name_zh': '毛泽东·探索期 (1958-1965)：大跃进/人民公社/反右派/读书笔记/经济调整',
        'name_en': 'Mao Zedong · Exploration Period (1958-1965): Great Leap Forward/ People\'s Communes/ Anti-Rightist/ Reading Notes/ Economic Adjustment',
        'desc_zh': '探索中国社会主义建设道路，发动大跃进/人民公社运动，反右派斗争扩大化，八届八中全会/七千人大会/陶铸/刘少奇/邓小平主导经济调整，读书笔记持续不断。',
        'desc_en': 'Explored Chinese socialist construction path, launched Great Leap Forward/People\'s Communes, Anti-Rightist enlarged, 8th Plenum/7000 Cadres Conference/Tao Zhu/Liu Shaoqi/Deng Xiaoping led economic adjustment, reading notes continued.',
        'modes': [24, 19, 1, 34, 25],
        'reason_zh': '毛泽东探索期以大跃进/人民公社追求超英赶美，反右派扩大化打击异己，经济调整/七千人大会/读书笔记体现纠错能力，成中国社会主义探索/大跃进教训/经济调整/理论坚持四维复杂图景。',
        'reason_en': 'Mao Zedong exploration period pursued surpass UK/catch US with Great Leap/People\'s Communes, Anti-Rightist enlarged struck dissenters, economic adjustment/7000 Cadres/reading notes embodied correction ability, becoming Chinese socialist exploration/Great Leap lesson/economic adjustment/theoretical persistence four-dimensional complex landscape.',
        'steps_zh': ['大跃进：1958年"超英赶美"，钢铁翻番/卫星田/大炼钢铁/浮夸风/通报风，造成严重经济困难', '人民公社：1958年建立人民公社，工农兵学商合一/食堂/供给制/家庭解体，严重破坏生产秩序', '反右派：1957年反右/1959年庐山会议打彭德怀，打击党内民主/知识分子/军队将领', '经济调整：1961年八届八中全会"调整/巩固/充实/提高"，1962年七千人大会刘少奇/邓小平主导调整，三年困难期基本结束', '读书笔记：持续阅读政治经济学/哲学/军事/历史，读书笔记体现理论思考与实践反思'],
        'steps_en': ['Great Leap Forward: 1958 "surpass UK/catch US", steel doubling/satellite fields/backyard furnaces/exaggeration/communique wind, caused severe economic difficulties', 'People\'s Communes: 1958 established communes, industry-agriculture-military-study-commerce unity/canteens/supply system/family dissolution, severely disrupted production order', 'Anti-Rightist: 1957 Anti-Rightist/1959 Lushan Conference struck Peng Dehuai, struck intra-party democracy/intellectuals/military generals', 'Economic Adjustment: 1961 8th Plenum "adjust/consolidate/enrich/improve", 1962 7000 Cadres Liu Shaoqi/Deng Xiaoping led adjustment, three difficult years basically ended', 'Reading Notes: Continuous reading political economy/philosophy/military/history, reading notes embody theoretical thinking and practical reflection'],
        'expected_zh': '成中国社会主义探索/大跃进教训/经济调整/理论坚持四维复杂图景，大跃进/公社/反右/调整四大历史事件',
        'expected_en': 'Become Chinese socialist exploration/Great Leap lesson/economic adjustment/theoretical persistence four-dimensional complex landscape, Great Leap/Communes/Anti-Right/Adjustment four major historical events',
        'case_zh': '1958年大跃进/人民公社，1959年庐山会议，1960-1961年三年困难期，1961年八届八中全会调整，1962年七千人大会。其"大跃进/人民公社/反右派/经济调整/读书笔记"五大算子，成中国社会主义建设探索/错误教训/纠偏能力/理论坚持四维复杂教科书。',
        'case_en': '1958 Great Leap/People\'s Communes, 1959 Lushan Conference, 1960-61 Three Difficult Years, 1961 8th Plenum Adjustment, 1962 7000 Cadres. Five operators: Great Leap/People\'s Communes/Anti-Rightist/Economic Adjustment/Reading Notes, becoming Chinese socialist construction exploration/error lessons/correction ability/theoretical persistence four-dimensional complex textbook.'
    },
    {
        'code': 'M-WN-285',
        'name_zh': '毛泽东·晚年/文革期 (1966-1976)：文化大革命/理论遗产/诗词外交/九个决策/接班安排',
        'name_en': 'Mao Zedong · Late Years/Cultural Revolution (1966-1976): Cultural Revolution/ Theoretical Legacy/ Poetry Diplomacy/ Nine Decisions/ Succession Arrangement',
        'desc_zh': '发动文化大革命，理论遗产《毛泽东思想》确立指导地位，诗词外交开启中美关系，晚年"九个决策"(接触日本/接触美国/调整经济/批陈整风/反击右倾/安排接班/医疗卫生/科技发展/对外开放)，完成历史使命。',
        'desc_en': 'Launched Cultural Revolution, theoretical legacy "Mao Zedong Thought" established guiding position, poetry diplomacy opened China-US relations, late years "Nine Decisions" (contact Japan/contact US/adjust economy/Criticize Chen Rectify/anti-rightist/succession/healthcare/sci-tech/opening up), completed historical mission.',
        'modes': [33, 34, 42, 26, 28],
        'reason_zh': '毛泽东晚年以文化大革命探索防修防变，诗词外交(水调歌头/念奴娇/沁园春)开启中美破冰，"九个决策"系统安排后事，理论遗产《毛泽东思想》写入党章，成中国政治运动/外交突破/理论定型/接班安排四维终局。',
        'reason_en': 'Mao Zedong late years explored anti-revision with Cultural Revolution, poetry diplomacy (Swimming/Water Melody/Nian Nu Jiao/Qin Yuan Chun) opened China-US ice-breaking, "Nine Decisions" systematically arranged succession, theoretical legacy "Mao Zedong Thought" written into Party Constitution, becoming Chinese political movement/diplomatic breakthrough/theory finalization/succession four-dimensional endgame.',
        'steps_zh': ['文化大革命：1966-1976年"以阶级斗争为纲"，红卫兵/造反派/武斗/军管/清理阶级队伍，严重动荡十年', '理论遗产：1969年九大/1973年十大将毛泽东思想写入党章，确立指导地位，形成完整理论体系', '诗词外交：1972年尼克松访华/毛泽东会见/水调歌头·游泳/念奴娇·鸟儿问答/沁园春·长沙，诗词开启中美破冰', '九个决策：接触日本/接触美国/调整经济/批陈整风/反击右倾翻案风/安排接班(华国锋)/医疗卫生(赤脚医生)/科技发展(四个现代化)/对外开放', '接班安排：指定华国锋为接班人/"你办事我放心"，遗体火化/纪念堂/功过三七开评价'],
        'steps_en': ['Cultural Revolution: 1966-1976 "class struggle as key", Red Guards/rebels/armed fights/military control/cleanse class queues, severe turmoil ten years', 'Theoretical Legacy: 1969 9th Congress/1973 10th Congress wrote Mao Zedong Thought into Party Constitution, established guiding position, formed complete theoretical system', 'Poetry Diplomacy: 1972 Nixon visit/Mao meeting/Water Melody Swimming/Nian Nu Jiao Birds Q&A/Qin Yuan Chun Changsha, poetry opened China-US ice-breaking', 'Nine Decisions: Contact Japan/contact US/adjust economy/Criticize Chen Rectify/anti-rightist reversal/succession(Hua Guofeng)/healthcare(barefoot doctors)/sci-tech(Four Modernizations)/opening up', 'Succession Arrangement: Designated Hua Guofeng successor/"you handle affairs I rest assured", cremation/memorial hall/merits-faults 70-30 evaluation'],
        'expected_zh': '成中国政治运动/外交突破/理论定型/接班安排四维终局，文革/诗词外交/理论遗产/接班四大历史遗产',
        'expected_en': 'Become Chinese political movement/diplomatic breakthrough/theory finalization/succession four-dimensional endgame, Cultural Revolution/poetry diplomacy/theoretical legacy/succession four major historical legacies',
        'case_zh': '1966年五一六通知发动文革，1972年尼克松访华/中美联合公报，1976年9月9日逝世。其"文革/诗词外交/理论遗产/接班安排/九个决策"五大算子，成中国政治运动/外交突破/理论定型/权力传承四维终局教科书。',
        'case_en': '1966 May 16 Circular launched Cultural Revolution, 1972 Nixon visit/China-US Joint Communique, died Sep 9 1976. Five operators: Cultural Revolution/poetry diplomacy/theoretical legacy/succession/nine decisions, becoming Chinese political movement/diplomatic breakthrough/theory finalization/power succession four-dimensional endgame textbook.'
    }
]

for fig in figures:
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

print(f'Added {len(figures)} Mao Zedong phases')
print(f'Total ZH: {len(zh)}, H-: {sum(1 for k in zh if k.startswith("H-") or k.startswith("M-"))}')
print(f'Total EN: {len(en)}, H-: {sum(1 for k in en if k.startswith("H-") or k.startswith("M-"))}')
print(f'CODE_MAP: {len(cm["CODE_MAP"])}')