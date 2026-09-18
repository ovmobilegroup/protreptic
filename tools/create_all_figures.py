#!/usr/bin/env python3

import json

def create_all_remaining_figures():
    """Create all remaining East/Southern African figures using direct file creation"""
    
    figures = [
        # KE-MOI-001 - Daniel Moi
        {
            "code": "KE-MOI-001",
            "name_zh": "摩伊/肯尼亚/独裁/单一党/族群/继任/基巴基/丹尼尔",
            "name_en": "Moi/Kenya/Dictatorship/Single_Party/Clan/Inheritance/Kibaki/Daniel",
            "core_mode": "M571 单一党独裁/族群利益/和平交权/基巴基/丹尼尔统治",
            "nationality": "肯尼亚",
            "civilization_sphere": "撒哈拉以南非洲/东非",
            "time_period_standardized": "1924-至今",
            "primary_language": "英语",
            "description_zh": "丹尼尔·莫伊（1924-至今），肯尼亚前总统，1978-2002年在位。他是一位肯尼亚政治家，前教师，1964年成为肯尼亚总理，1978年接替肯雅塔，继续执政，倡导肯雅塔的政策。他建立了一党制肯尼亚人民党，长期执政，控制了肯尼亚的政治。他的统治时期，肯尼亚经历了经济增长和政治稳定，但也存在权力继承问题。",
            "description_en": "Daniel Moi (1924-present), former President of Kenya, served from 1978 to 2002. He was a Kenyan politician and former teacher, became Prime Minister in 1964, succeeded Kenyatta in 1978, continued Kenyatta's policies. He established the Kenya African National Union as a one-party state, ruling Kenya for decades. His rule saw economic growth and political stability, but also power succession issues.",
            "reason_zh": "莫伊是肯尼亚长期执政的总统，通过一党制和控制权继承，保持了肯尼亚的稳定。他的统治体现了后殖民时期的权力巩固和政治控制，但也限制了民主的发展。",
            "reason_en": "Moi was Kenya's long-ruling president, maintaining stability through one-party rule and controlled succession. His rule exemplified post-colonial power consolidation and political control, but limited democratic development.",
            "steps_zh": [
                "政治生涯开始：1924 出生/肯尼亚政治家/前教师/政治道路的启动",
                "独立后政治：1964 成为总理/肯尼亚独立后/继续执政/稳定政治",
                "长期执政：1978 就任总统/建立一党制/长期统治/保持稳定",
                "权力交接：2002 卸任/和平权力交接/基巴基接任/民主过渡"
            ],
            "steps_en": [
                "Political career start: 1924 birth/Kenyan politician/former teacher/start of political career",
                "Post-independence politics: 1964 became Prime Minister/Kenya independence/continuing rule/stable politics",
                "Long-term rule: 1978 became President/established one-party rule/long-term rule/maintained stability",
                "Power transition: 2002 resigned/peaceful power transition/Kibaki succeeded/democratic transition"
            ],
            "expected_zh": "建立稳定的政治体系，通过和平过渡实现权力交接。莫伊是肯尼亚后殖民时期的典型统治者，保持了国家的稳定，但限制了民主的发展。",
            "expected_en": "Established a stable political system, achieving peaceful power transition. Moi was a typical post-colonial ruler in Kenya, maintaining stability but limiting democratic development.",
            "case_zh": "1924 出生/1964 总理/1978 总统/2002 卸任/肯尼亚独立/莫伊/一党制/权力交接/肯尼亚稳定/永存。",
            "case_en": "1924 birth/1964 Prime Minister/1978 President/2002 resigned/Kenya independence/Moi/one-party rule/power transition/Kenya stability/endures.",
            "era": "1924-至今",
            "historical_domains": ["政治", "社会", "经济", "民族", "民主"],
            "domains": ["协作", "系统", "分析", "创意", "运营"],
            "gender": "男",
            "ethnicity": "肯尼亚"
        },
        # TZ-MKP-001 - Benjamin Mkapa
        {
            "code": "TZ-MKP-001",
            "name_zh": "姆卡帕/坦桑尼亚/改革/私有化/东非共同体/本杰明/威廉",
            "name_en": "Mkapa/Tanzania/Reform/Privateization/East_African_Community/Benjamin/William",
            "core_mode": "M573 改革私有化/区域一体化/私有化/东非共同体",
            "nationality": "坦桑尼亚",
            "civilization_sphere": "撒哈拉以南非洲/东非",
            "time_period_standardized": "1934-2020",
            "primary_language": "斯瓦希里语/英语",
            "description_zh": "本杰明·姆卡帕（1934-2020），坦桑尼亚前总统，1995-2005年在位。他是一位坦桑尼亚政治家，曾任外交部长、总理，曾领导坦桑尼亚实施经济改革，推行私有化政策，促进了坦桑尼亚的经济发展。他倡导东非共同体一体化，支持区域合作。",
            "description_en": "Benjamin Mkapa (1934-2020), former President of Tanzania, served from 1995 to 2005. He was a Tanzanian politician, served as Foreign Minister and Prime Minister, led Tanzania to implement economic reforms, promoted privatization policies, promoted Tanzanian economic development. He advocated East African Community integration, supported regional cooperation.",
            "reason_zh": "姆卡帕是坦桑尼亚经济改革的领导者，通过私有化政策促进了经济发展，支持东非共同体一体化，体现了坦桑尼亚对区域合作的支持。",
            "reason_en": "Mkapa was the leader of Tanzania's economic reforms, promoting economic development through privatization policies, advocated East African Community integration, supported regional cooperation.",
            "steps_zh": [
                "政治生涯开始：1934 出生/坦桑尼亚政治家/外交部长/政治道路的启动",
                "总理生涯：1975-1995 担任总理/领导国家建设/稳定政治",
                "总统生涯：1995-2005 就任总统/实施经济改革/私有化政策/促进发展",
                "卸任后：2005-2020 退休生活/继续支持东非合作/国际评价"
            ],
            "steps_en": [
                "Political career start: 1934 birth/Tanzanian politician/Foreign Minister/start of political career",
                "Prime ministerial career: 1975-1995 served as Prime Minister/led nation-building/stable politics",
                "Presidential career: 1995-2005 became President/economic reforms/privatization policies/promoted development",
                "Post-retirement: 2005-2020 retired life/continuous support for East African cooperation/international evaluation"
            ],
            "expected_zh": "通过经济改革和私有化政策促进坦桑尼亚经济发展，支持东非共同体一体化，推动区域合作。",
            "expected_en": "Promoted Tanzanian economic development through economic reforms and privatization policies, advocated East African Community integration, promoted regional cooperation.",
            "case_zh": "1934 出生/1975 总理/1995 总统/2005 卸任/坦桑尼亚改革/姆卡帕/私有化/东非合作/坦桑尼亚发展/永存。",
            "case_en": "1934 birth/1975 Prime Minister/1995 President/2005 resigned/Tanzanian reform/Mkapa/privatization/East African cooperation/Tanzanian development/endures.",
            "era": "1934-2020",
            "historical_domains": ["政治", "经济", "社会", "外交", "区域合作"],
            "domains": ["协作", "系统", "分析", "创意", "运营"],
            "gender": "男",
            "ethnicity": "坦桑尼亚"
        },
        # ZA-MAN-001 - Nelson Mandela
        {
            "code": "ZA-MAN-001",
            "name_zh": "曼德拉/南非/反种隔/真相和解/彩虹/纳尔逊/罗本岛/马迪巴",
            "name_en": "Mandela/South_Africa/Anti-apartheid/Truth_and_Reconciliation/Rainbow/Nelson/Roberts_Island/Madiba",
            "core_mode": "M580 真相和解/彩虹国家/道德权威/罗本岛/马迪巴精神",
            "nationality": "南非",
            "civilization_sphere": "撒哈拉以南非洲/南部非洲",
            "time_period_standardized": "1918-2013",
            "primary_language": "英语",
            "description_zh": "纳尔逊·曼德拉（1918-2013），南非前总统，1990-1999年在位。他是一位南非政治家和反种族隔离斗士，领导南非非洲国民大会党，领导反对种族隔离的斗争，1990年担任总统，开始了南非的转型和真相与和解进程。他是一位具有道德权威的领导者，被誉为'彩虹国家'的象征。",
            "description_en": "Nelson Mandela (1918-2013), former President of South Africa, served from 1990 to 1999. He was a South African politician and anti-apartheid revolutionary, led the African National Congress to fight against apartheid, led the struggle against apartheid, became President in 1990, began South Africa's transition and truth and reconciliation process. He was a leader with moral authority, known as the symbol of the 'Rainbow Nation'.",
            "reason_zh": "曼德拉是南非反种族隔离斗争的领导者，通过真相与和解进程实现了国家的转型。他是一位具有道德权威的领导者，被誉为'彩虹国家'的象征，体现了南非的民族和解和民主精神。",
            "reason_en": "Mandela was the leader of South Africa's anti-apartheid struggle, achieved national transition through truth and reconciliation process. He was a leader with moral authority, known as the symbol of the 'Rainbow Nation', embodied South Africa's national reconciliation and democratic spirit.",
            "steps_zh": [
                "反种族斗争：1944-1962 加入非洲国民大会党/领导反种族斗争/组织地下活动",
                "长期监狱斗争：1962-1990 长期监禁/领导反种族斗争/保持斗争精神",
                "总统生涯：1990-1999 就任总统/领导国家转型/真相与和解/建立彩虹国家",
                "国际评价：1999-2013 退休生活/国际和平活动/道德权威/影响全球"
            ],
            "steps_en": [
                "Anti-apartheid struggle: 1944-1962 joined African National Congress/led anti-apartheid struggle/organized underground activities",
                "Long-term imprisonment struggle: 1962-1990 long-term imprisonment/led anti-apartheid struggle/maintained fighting spirit",
                "Presidential career: 1990-1999 became President/led national transition/truth and reconciliation/established Rainbow Nation",
                "International evaluation: 1999-2013 retired life/international peace activities/moral authority/global influence"
            ],
            "expected_zh": "通过真相与和解实现了南非的民族和解，建立了民主国家。曼德拉是南非自由和民主精神的象征，在全球具有道德权威。",
            "expected_en": "Achieved national reconciliation through truth and reconciliation, established democratic nation. Mandela was the symbol of South Africa's freedom and democracy, had moral authority globally.",
            "case_zh": "1918 出生/1944 加入非洲国民大会党/1962 长期监禁/1990 就任总统/1999 卸任/南非反种族/曼德拉/真相和解/彩虹国家/永存。",
            "case_en": "1918 birth/1944 joined African National Congress/1962 long-term imprisonment/1990 became President/1999 resigned/South Africa anti-apartheid/Mandela/truth and reconciliation/Rainbow Nation/endures.",
            "era": "1918-2013",
            "historical_domains": ["政治", "社会", "经济", "民族", "道德"],
            "domains": ["协作", "系统", "分析", "创意", "运营"],
            "gender": "男",
            "ethnicity": "南非"
        },
        # ZA-MBK-001 - Thabo Mbeki
        {
            "code": "ZA-MBK-001",
            "name_zh": "姆贝基/南非/艾滋/非洲复兴/津巴布韦调解/塔博/非洲复兴",
            "name_en": "Mbeki/South_Africa/AIDS/African_Renaissance/Zimbabwe_Mediation/Thabo/African_Renaissance",
            "core_mode": "M581 非洲复兴/艾滋争议/区域调解/非洲文艺复兴/塔博外交",
            "nationality": "南非",
            "civilization_sphere": "撒哈拉以南非洲/南部非洲",
            "time_period_standardized": "1942-至今",
            "primary_language": "英语",
            "description_zh": "塔博·姆贝基（1942-至今），南非前总统，2004-2009年在位。他是一位南非政治家，曾任外交部长、总统，在任期间，他倡导非洲复兴，提出了‘非洲复兴’理论，支持津巴布韦等非洲国家的民主转型。他在应对艾滋病问题上引发了争议，但也促进了非洲的区域合作和文化复兴。",
            "description_en": "Thabo Mbeki (1942-present), former President of South Africa, served from 2004 to 2009. He was a South African politician, served as Foreign Minister, President, advocated African Renaissance, proposed 'African Renaissance' theory, supported democratic transition of Zimbabwe and other African countries. He was controversial in addressing AIDS issues, but also promoted African regional cooperation and cultural revival.",
            "reason_zh": "姆贝基是南非政治家，倡导非洲复兴，提出了'非洲复兴'理论，支持非洲国家的民主转型。他的理论和政策体现了非洲自主发展和文化复兴的思想，但也引发了关于艾滋病问题的争议。",
            "reason_en": "Mbeki was a South African politician, advocated African Renaissance, proposed 'African Renaissance' theory, supported democratic transition of Zimbabwe and other African countries. His theory and policies reflected African self-development and cultural revival thinking, but also sparked controversy on AIDS issues.",
            "steps_zh": [
                "政治生涯开始：1942 出生/南非政治家/外交部官员/政治道路的启动",
                "外交部长生涯：1994-2004 担任外交部长/领导外交事务/促进国际地位",
                "总统生涯：2004-2009 就任总统/倡导非洲复兴/提出复兴理论/支持地区合作",
                "卸任后：2009-至今 退休生活/继续支持非洲发展/国际评价"
            ],
            "steps_en": [
                "Political career start: 1942 birth/South African politician/Foreign Ministry official/start of political career",
                "Foreign Minister career: 1994-2004 served as Foreign Minister/led diplomatic affairs/promoted international status",
                "Presidential career: 2004-2009 became President/advocated African Renaissance/proposed Renaissance theory/promoted regional cooperation",
                "Post-retirement: 2009-present retired life/continuous support for African development/international evaluation"
            ],
            "expected_zh": "倡导非洲复兴，提出了'非洲复兴'理论，支持非洲国家的民主转型。姆贝基的理论体现了非洲自主发展和文化复兴的思想，但也引发了争议。",
            "expected_en": "Advocated African Renaissance, proposed 'African Renaissance' theory, supported democratic transition of Zimbabwe and other African countries. Mbeki's theory and policies reflected African self-development and cultural revival thinking.",
            "case_zh": "1942 出生/1994 外交部长/2004 总统/2009 卸任/南非政治/姆贝基/非洲复兴/文艺复兴/塔博外交/永存。",
            "case_en": "1942 birth/1994 Foreign Minister/2004 President/2009 resigned/South African politics/Mbeki/African Renaissance/cultural revival/Thabo/endures.",
            "era": "1942-至今",
            "historical_domains": ["政治", "经济", "社会", "文化", "外交"],
            "domains": ["协作", "系统", "分析", "创意", "运营"],
            "gender": "男",
            "ethnicity": "南非"
        },
        # ZA-ZUM-001 - Jacob Zuma
        {
            "code": "ZA-ZUM-001",
            "name_zh": "祖马/南非/腐败/国家捕获/祖鲁/德班/雅各布/国家捕获",
            "name_en": "Zuma/South_Africa/Corruption/State_Capture/Zulu/Durban/Jacob/State_Capture",
            "core_mode": "M582 国家捕获/祖鲁民族/腐败深渊/祖鲁化/德班港",
            "nationality": "南非",
            "civilization_sphere": "撒哈拉以南非洲/南部非洲",
            "time_period_standardized": "1942-至今",
            "primary_language": "祖鲁语/英语",
            "description_zh": "雅各布·祖马（1942-至今），南非前总统，2009-2018年在位。他是一位南非政治家，祖鲁族人，1999-2005年担任国防部长，2005-2009年担任副总统，2009-2018年担任总统。他在执政期间，南非爆发了严重的腐败和国家捕获事件，导致政府信任危机。他的祖鲁民族主义政策也引发了争议。
            "description_en": "Jacob Zuma (1942-present), former President of South Africa, served from 2009 to 2018. He was a South African politician, Zulu, served as Minister of Defense from 1999 to 2005, Vice President from 2005 to 2009, President from 2009 to 2018. During his tenure, South Africa experienced serious corruption and state capture incidents, leading to government trust crisis. His Zulu nationalist policies also sparked controversy.",
            "reason_zh": "祖马是南非政治家，在执政期间，南非爆发了严重的腐败和国家捕获事件，导致政府信任危机。他的祖鲁民族主义政策也引发了争议。他的统治体现了南非政治体系中的深层次腐败问题。",
            "reason_en": "Zuma was a South African politician, during his tenure, South Africa experienced serious corruption and state capture incidents, leading to government trust crisis. His Zulu nationalist policies also sparked controversy. His rule reflected the deep-rooted corruption problems in the South African political system.",
            "steps_zh": [
                "政治生涯开始：1942 出生/祖鲁族人/政治家/政治道路的启动",
                "国防部长生涯：1999-2005 担任国防部长/领导国防事务/提升国际地位",
                "副总统生涯：2005-2009 担任副总统/协助总统/积累执政经验",
                "总统生涯：2009-2018 就任总统/爆发腐败事件/国家捕获危机/信任危机"
            ],
            "steps_en": [
                "Political career start: 1942 birth/Zulu/T politician/political career start",
                "Defense Minister career: 1999-2005 served as Defense Minister/led defense affairs/promoted international status",
                "Vice presidential career: 2005-2009 served as Vice President/assisted President/accumulated governing experience",
                "Presidential career: 2009-2018 became President/corruption incidents/state capture crisis/trust crisis"
            ],
            "expected_zh": "在执政期间，南非爆发了严重的腐败和国家捕获事件，导致政府信任危机。祖马的统治体现了南非政治体系中的深层次腐败问题。",
            "expected_en": "During his tenure, South Africa experienced serious corruption and state capture incidents, leading to government trust crisis. Zuma's rule reflected the deep-rooted corruption problems in the South African political system.",
            "case_zh": "1942 出生/1999 国防部长/2005 副总统/2009 总统/2018 卸任/南非政治/祖马/腐败/国家捕获/祖鲁化/永存。",
            "case_en": "1942 birth/1999 Defense Minister/2005 Vice President/2009 President/2018 resigned/South African politics/Zuma/corruption/state capture/Zulu/endures.",
            "era": "1942-至今",
            "historical_domains": ["政治", "经济", "社会", "法律", "文化"],
            "domains": ["协作", "系统", "分析", "创意", "运营"],
            "gender": "男",
            "ethnicity": "南非"
        },
        # ZW-MUG-001 - Robert Mugabe
        {
            "code": "ZW-MUG-001",
            "name_zh": "穆加贝/津巴布韦/土地/独裁/通胀/钻石/罗伯特/马拉维/马拉维",
            "name_en": "Mugabe/Zimbabwe/Land/Dictatorship/Inflation/Diamonds/Robert/Malawi/Malawi",
            "core_mode": "M583 土地革命/恶性通胀/钻石诅咒/马拉维钻石/土地掠夺",
            "nationality": "津巴布韦",
            "civilization_sphere": "撒哈拉以南非洲/南部非洲",
            "time_period_standardized": "1924-2019",
            "primary_language": "英语",
            "description_zh": "罗伯特·穆加贝（1924-2019），津巴布韦前总统，1980-2017年在位。他是一位津巴布韦政治家，前教师，领导津巴布韦独立，成立了津巴布韦非洲民族联盟党（目前名为津巴布韦非洲国民联盟党）。他倡导土地改革，实施了‘土地革命’，导致了通货膨胀和经济衰退。他的长期独裁统治对津巴布韦造成了深远的影响。",
            "description_en": "Robert Mugabe (1924-2019), former President of Zimbabwe, served from 1980 to 2017. He was a Zimbabwean politician, former teacher, led Zimbabwe's independence, established the Zimbabwe African National Union Party (currently Zimbabwe African National Union-Patriotic Front Party). He advocated land reform, implemented 'land revolution', leading to inflation and economic recession. His long-term dictatorship had a profound impact on Zimbabwe.",
            "reason_zh": "穆加贝是津巴布韦独立运动的领导者，通过土地改革和‘土地革命’建立了津巴布韦国家。他的长期独裁统治导致经济衰退和通货膨胀，对津巴布韦造成了深远的影响。他的统治体现了后殖民时期的政治腐败和经济问题。",
            "reason_en": "Mugabe was the leader of Zimbabwe's independence movement, established Zimbabwe through land reform and 'land revolution'. His long-term dictatorship led to economic recession and inflation, had a profound impact on Zimbabwe. His rule reflected the post-colonial political corruption and economic problems.",
            "steps_zh": [
                "独立运动领导：1960-1980 津巴布韦非洲民族联盟建立/穆加贝领导独立/实现独立/建立新国家",
                "总统生涯：1980-2000 就任总统/实施土地改革/开始‘土地革命’/巩固权力",
                "长期执政：2000-2017 长期独裁/实施土地政策/经济衰退/国际孤立",
                "下台：2017 被废黜/结束独裁/国际评价/津巴布韦未来"
            ],
            "steps_en": [
                "Independence movement leadership: 1960-1980 Zimbabwe African National Union established/Mugabe led independence/achieved independence/established new nation",
                "Presidential career: 1980-2000 became President/implemented land reform/began 'land revolution'/consolidated power",
                "Long-term rule: 2000-2017 long-term dictatorship/implemented land policies/economic recession/international isolation",
                "Deposition: 2017 deposed/ended dictatorship/international evaluation/Zimbabwe future"
            ],
            "expected_zh": "通过土地改革建立了津巴布韦国家，但长期独裁统治导致经济衰退和通货膨胀，对津巴布韦造成了深远的影响。",
            "expected_en": "Established Zimbabwe through land reform, but long-term dictatorship led to economic recession and inflation, had a profound impact on Zimbabwe.",
            "case_zh": "1924 出生/1960 成立津巴布韦非洲民族联盟/1980 就任总统/2017 被废黜/津巴布韦独立/穆加贝/土地改革/经济衰退/永存。",
            "case_en": "1924 birth/1960 established Zimbabwe African National Union/1980 became President/2017 deposed/Zimbabwe independence/Mugabe/land reform/economic recession/endures.",
            "era": "1924-2019",
            "historical_domains": ["政治", "经济", "社会", "民族", "文化"],
            "domains": ["协作", "系统", "分析", "创意", "运营"],
            "gender": "男",
            "ethnicity": "津巴布韦"
        },
        # BW-KHA-001 - Festus Mogae
        {
            "code": "BW-KHA-001",
            "name_zh": "卡马/博茨瓦纳/钻石/民主/传统/塞雷茨/塞雷茨/钻石民主",
            "name_en": "Khama/Botswana/Diamonds/Democracy/Tradition/Seretsi/Seretsi/Diamond_Democracy",
            "core_mode": "M584 钻石民主/传统酋长/发展奇迹/塞雷茨模式/资源管理",
            "nationality": "博茨瓦纳",
            "civilization_sphere": "撒哈拉以南非洲/南部非洲",
            "time_period_standardized": "1939-至今",
            "primary_language": "英语",
            "description_zh": "费斯图斯·卡马（1939-至今），博茨瓦纳前总统，1998-2008年在位。他是一位博茨瓦纳政治家，前警察，1998-2008年担任总统。博茨瓦纳在他的领导下，通过钻石资源实现了快速经济发展，成为非洲的成功典范。他的传统酋长制度和民主制度相结合，形成了独特的‘钻石民主’模式。",
            "description_en": "Festus Mogae (1939-present), former President of Botswana, served from 1998 to 2008. He was a Botswanan politician, former police, served as President from 1998 to 2008. Under his leadership, Botswana achieved rapid economic development through diamond resources, became a model in Africa. His traditional chieftaincy system and democracy combined, forming a unique 'diamond democracy' model.",
            "reason_zh": "卡马是博茨瓦纳政治家，通过钻石资源实现了快速经济发展，成为非洲的成功典范。他的传统酋长制度和民主制度相结合，形成了独特的‘钻石民主’模式。",
            "reason_en": "Mogae was a Botswanan politician, achieved rapid economic development through diamond resources, became a model in Africa. His traditional chieftaincy system and democracy combined, formed a unique 'diamond democracy' model.",
            "steps_zh": [
                "警察生涯：1939 出生/警察出身/政治道路的启动/领导能力培养",
                "政治生涯开始：1970 首次当选/政治生涯开始/积累执政经验/提升地位",
                "总统生涯：1998-2008 就任总统/领导国家建设/钻石经济发展/成功典范",
                "卸任后：2008-至今 退休生活/继续支持博茨瓦纳发展/国际评价"
            ],
            "steps_en": [
                "Police career: 1939 birth/police background/political career start/leadership ability cultivation",
                "Political career start: 1970 first elected/political career start/accumulated governing experience/promoted status",
                "Presidential career: 1998-2008 became President/led nation-building/diamond economic development/model in Africa",
                "Post-retirement: 2008-present retired life/continuous support for Botswana development/international evaluation"
            ],
            "expected_zh": "通过钻石资源实现了快速经济发展，成为非洲的成功典范。卡马的传统酋长制度和民主制度相结合，形成了独特的‘钻石民主’模式。",
            "expected_en": "Achieved rapid economic development through diamond resources, became a model in Africa. Mogae's traditional chieftaincy system and democracy combined, formed a unique 'diamond democracy' model.",
            "case_zh": "1939 出生/1970 首次当选/1998 总统/2008 卸任/博茨瓦纳成功/卡马/钻石民主/传统制度/发展奇迹/永存。",
            "case_en": "1939 birth/1970 first elected/1998 President/2008 resigned/Botswana success/Mogae/diamond democracy/traditional system/development miracle/endures.",
            "era": "1939-至今",
            "historical_domains": ["政治", "经济", "社会", "文化", "传统"],
            "domains": ["协作", "系统", "分析", "创意", "运营"],
            "gender": "男",
            "ethnicity": "博茨瓦纳"
        },
        # NA-NUJ-001 - Sam Nujoma
        {
            "code": "NA-NUJ-001",
            "name_zh": "努乔马/纳米比亚/解放/斯瓦普/种族/和解/萨姆/努乔马/解放",
            "name_en": "Nujoma/Namibia/Liberation/Swapo/Race/Reconciliation/Sam/Nujoma/Liberation",
            "core_mode": "M585 解放运动/种族和解/沙漠国家/斯瓦普/萨姆精神",
            "nationality": "纳米比亚",
            "civilization_sphere": "撒哈拉以南非洲/南部非洲",
            "time_period_standardized": "1929-至今",
            "primary_language": "英语/翁胡姆语",
            "description_zh": "萨姆·努乔马（1929-至今），纳米比亚前总统，1990-2005年在位。他是一位纳米比亚政治家，前士兵，领导纳米比亚独立运动，成立了斯瓦普党（西南非洲人民组织），领导纳米比亚从南非殖民统治中解放出来，成为首任总统。",
            "description_en": "Sam Nujoma (1929-present), former President of Namibia, served from 1990 to 2005. He was a Namibian politician, former soldier, led Namibia's independence movement, established SWAPO (Southwest Africa People's Organization), led Namibia to liberation from South African colonial rule, became the first President.",
            "reason_zh": "努乔马是纳米比亚独立运动的领导者，领导纳米比亚从南非殖民统治中解放出来。他是一位前士兵，通过斯瓦普党领导了国家的解放和独立。",
            "reason_en": "Nujoma was the leader of Namibia's independence movement, led Namibia to liberation from South African colonial rule. He was a former soldier, led the country's liberation through SWAPO.",
            "steps_zh": [
                "解放运动领导：1960-1990 斯瓦普党建立/努乔马领导独立/从南非殖民统治中解放出来",
                "总统生涯：1990-2005 就任总统/领导国家建设/促进发展/巩固独立",
                "长期执政：2005-2015 退休生活/继续支持纳米比亚发展/国际评价",
                "国际地位：至今 国际和平活动/支持非洲解放/全球影响"
            ],
            "steps_en": [
                "Liberation movement leadership: 1960-1990 SWAPO established/Nujoma led independence/liberated from South African colonial rule",
                "Presidential career: 1990-2005 became President/led nation-building/promoted development/consolidated independence",
                "Long-term retirement: 2005-2015 retired life/continuous support for Namibian development/international evaluation",
                "International status: present international peace activities/support African liberation/global influence"
            ],
            "expected_zh": "领导纳米比亚独立运动，从南非殖民统治中解放出来。努乔马是一位前士兵，通过斯瓦普党领导了国家的解放和独立。",
            "expected_en": "Led Namibia's independence movement, led Namibia to liberation from South African colonial rule. Nujoma was a former soldier, led the country's liberation through SWAPO.",
            "case_zh": "1929 出生/1960 成立斯瓦普党/1990 总统/2005 卸任/纳米比亚解放/努乔马/独立运动/斯瓦普/永存。",
            "case_en": "1929 birth/1960 established SWAPO/1990 President/2005 resigned/Namibia liberation/Nujoma/independence movement/SWAPO/endures.",
            "era": "1929-至今",
            "historical_domains": ["政治", "军事", "社会", "经济", "民族"],
            "domains": ["协作", "系统", "分析", "创意", "运营"],
            "gender": "男",
            "ethnicity": "纳米比亚"
        }
    ]
    
    # Create all files
    for i, figure in enumerate(figures):
        filename = f"/opt/data/workspace/Protreptic/{figure['code']}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(figure, f, ensure_ascii=False, indent=2)
        print(f"Created {filename}")
    
    print(f"Successfully created {len(figures)} remaining historical figure JSON files!")
    return figures

if __name__ == "__main__":
    create_all_remaining_figures()