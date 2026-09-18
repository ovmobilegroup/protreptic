#!/usr/bin/env python3
"""
Batch 1: 10 Modern Entrepreneurs
Codes: H-RZF-270 through H-CW-279
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
        'code': 'H-RZF-270',
        'name_zh': '任正非：华为/狼性文化/备胎计划/生存哲学/利益分配',
        'name_en': 'Ren Zhengfei: Huawei/Wolf Culture/Spare Tire Plan/Survival Philosophy/Interest Distribution',
        'desc_zh': '华为创始人，以"狼性文化"建立危机意识组织，"备胎计划"实现供应链自主可控，"生存哲学"贯穿战略决策，"利益分配"机制激活员工创造力，成中国科技企业全球化/自主创新/组织进化三维典范。',
        'desc_en': 'Huawei founder, established crisis-aware organization with "wolf culture", achieved supply chain autonomy with "spare tire plan", "survival philosophy" guides strategic decisions, "interest distribution" mechanism激活employee creativity, becoming Chinese tech enterprise globalization/independent innovation/organizational evolution three-dimensional paradigm.',
        'modes': [1, 13, 15, 34, 18],
        'reason_zh': '任正非以"活下来"为第一要务建狼性文化，以"备胎计划"破供应链封锁，以"华为基本法"立制度宪章，以"奋斗者为本"设利益分配，成中国企业危机生存/自主创新/组织进化三维典范。',
        'reason_en': 'Ren Zhengfei built wolf culture with "survival first", broke supply chain blockade with "spare tire plan", established institutional constitution with "Huawei Basic Law", designed interest distribution with "struggler-centric", becoming Chinese enterprise crisis survival/independent innovation/organizational evolution three-dimensional paradigm.',
        'steps_zh': ['生存锚定：锁定"活下来是第一要务"为战略底线，确立危机意识为组织基因', '自主可控：启动"备胎计划"，芯片/操作系统/数据库全链路备胎，实现供应链自主可控', '制度立宪：颁布《华为基本法》确立核心价值观/组织架构/利益分配/领导力模型四大支柱', '利益分配：实行"奋斗者为本"，TUP/ESOP/分红三位一体，让听得见炮火的人分享利益', '组织进化：推行"铁三角/铁三角大代表/PDT/IFS"流程变革，打通端到端价值流'],
        'steps_en': ['Survival Anchoring: Lock "survival is the first priority" as strategic baseline, establish crisis awareness as organizational DNA', 'Autonomy & Control: Launch "Spare Tire Plan", full-stack backup for chips/OS/databases, achieve supply chain autonomy', 'Institutional Constitution: Promulgate "Huawei Basic Law" establishing four pillars: core values/org structure/interest distribution/leadership model', 'Interest Distribution: Implement "struggler-centric", TUP/ESOP/dividend trinity, let those who hear gunfire share benefits', 'Organizational Evolution: Push "Iron Triangle/Large Representative/PDT/IFS" process transformation, connect end-to-end value stream'],
        'expected_zh': '成中国科技企业全球化/自主创新/组织进化三维典范，华为年营收超7000亿、研发投入超10%、专利超10万件',
        'expected_en': 'Become Chinese tech enterprise globalization/independent innovation/organizational evolution three-dimensional paradigm, Huawei annual revenue >700B RMB, R&D >10%, patents >100K',
        'case_zh': '1987年创立华为，2018年被美列入实体清单，启动"备胎计划"麒麟芯片/鸿蒙OS/欧拉数据库全面替代，2023年Mate 60 Pro搭载麒麟9000S实现芯片突围。其"活下来"危机文化、"备胎"供应链韧性、"奋斗者"利益分配、"流程"组织进化四大算子，成中国企业全球化突围教科书。',
        'case_en': 'Founded Huawei in 1987, listed on US Entity List in 2018, launched "Spare Tire Plan" for Kirin chips/HarmonyOS/Euler DB full replacement, Mate 60 Pro with Kirin 9000S achieved chip breakthrough in 2023. Four operators: "survive" crisis culture, "spare tire" supply chain resilience, "struggler" interest distribution, "process" organizational evolution, becoming textbook for Chinese enterprise global breakout.'
    },
    {
        'code': 'H-MY-271',
        'name_zh': '马云：阿里/生态系统/信任机制/商业操作系统/使命驱动',
        'name_en': 'Jack Ma: Alibaba/Ecosystem/Trust Mechanism/Commercial Operating System/Mission-Driven',
        'desc_zh': '阿里巴巴创始人，以"让天下没有难做的生意"为使命，构建"电商+金融+物流+云计算+本地生活"全生态系统，创新"信任机制"(芝麻信用/担保交易)解决陌生人交易信任，打造"商业操作系统"赋能中小企业，成中国互联网平台/生态建设/使命驱动三维典范。',
        'desc_en': 'Alibaba founder, with mission "make it easy to do business anywhere", built full ecosystem "e-commerce+finance+logistics+cloud+local life", innovated "trust mechanism" (Sesame Credit/escrow) solving stranger transaction trust, built "commercial operating system" empowering SMEs, becoming Chinese internet platform/ecosystem construction/mission-driven three-dimensional paradigm.',
        'modes': [6, 18, 11, 32, 12],
        'reason_zh': '马云以"让天下没有难做的生意"为使命，构建电商/金融/物流/云/本地生活五位一体生态，创芝麻信用/担保交易解决信任缺失，输出商业操作系统赋能中小商家，成平台生态/信任建设/使命驱动三维典范。',
        'reason_en': 'Jack Ma with mission "make it easy to do business anywhere", built five-in-one ecosystem of e-commerce/finance/logistics/cloud/local life, created Sesame Credit/escrow solving trust deficit, output commercial OS empowering SMEs, becoming platform ecosystem/trust building/mission-driven three-dimensional paradigm.',
        'steps_zh': ['使命锚定：确立"让天下没有难做的生意"为唯一使命，所有战略决策向使命对齐', '生态构建：从电商切入，横向扩展金融(蚂蚁)/物流(菜鸟)/云计算/本地生活，形成自强化飞轮', '信任制造：创芝麻信用/担保交易/信用体系，用数据信用替代人际信任，降低交易成本', '平台赋能：输出商业操作系统(ERP/CRM/供应链/营销)，让中小商家享受大企业数字化能力', '文化传承：确立"客户第一/员工第二/股东第三"价值观，建立合伙人制度/阿里政治局传承机制'],
        'steps_en': ['Mission Anchoring: Establish "make it easy to do business anywhere" as sole mission, align all strategic decisions to mission', 'Ecosystem Construction: Enter from e-commerce, horizontally expand to finance(Ant)/logistics(Cainiao)/cloud/local life, form self-reinforcing flywheel', 'Trust Manufacturing: Create Sesame Credit/escrow/credit system, replace interpersonal trust with data credit, reduce transaction costs', 'Platform Empowerment: Output commercial OS (ERP/CRM/supply chain/marketing), let SMEs enjoy large enterprise digital capabilities', 'Culture Inheritance: Establish "customer first/employee second/shareholder third" values, build partnership system/Alibaba Politburo succession mechanism'],
        'expected_zh': '成中国互联网平台/生态建设/使命驱动三维典范，阿里GMV超万亿、年活用户超10亿、云计算亚太第一',
        'expected_en': 'Become Chinese internet platform/ecosystem construction/mission-driven three-dimensional paradigm, Alibaba GMV >1T, annual active users >1B, cloud computing Asia-Pacific #1',
        'case_zh': '1999年创立阿里巴巴，2003年淘宝击败eBay中国，2004年支付宝解决支付信任，2009年云计算/2013年菜鸟/2015年蚂蚁金服。其"使命驱动+生态共生+信任制造+文化传承"四大算子，成中国平台型企业教科书。2019年退休传承张勇/蒋凡，合伙人制度保证使命延续。',
        'case_en': 'Founded Alibaba in 1999, Taobao defeated eBay China in 2003, Alipay solved payment trust in 2004, cloud computing 2009/Cainiao 2013/Ant Financial 2015. Four operators: mission-driven + ecosystem symbiosis + trust manufacturing + culture inheritance, becoming textbook for Chinese platform enterprises. Retired in 2019 succeeded by Zhang Yong/Jiang Fan, partnership system ensures mission continuity.'
    },
    {
        'code': 'H-MHT-272',
        'name_zh': '马化腾：腾讯/产品思维/微创新/半个互联网/连接器战略',
        'name_en': 'Pony Ma: Tencent/Product Thinking/Micro-Innovation/Half the Internet/Connector Strategy',
        'desc_zh': '腾讯创始人，以"用户为本/产品思维"为核心，坚持"微创新"快速迭代，构建"社交+内容+游戏+支付+云"半个互联网生态，定位"连接器"而非平台主宰，赋能产业互联网，成中国产品驱动/生态共生/产业赋能三维典范。',
        'desc_en': 'Tencent founder, with "user-centric/product thinking" as core, insists on "micro-innovation" rapid iteration, builds "social+content+gaming+payment+cloud" half-the-internet ecosystem, positions as "connector" not platform ruler, empowers industrial internet, becoming Chinese product-driven/ecosystem symbiosis/industrial empowerment three-dimensional paradigm.',
        'modes': [11, 17, 31, 32, 18],
        'reason_zh': '马化腾以"用户为本"为产品罗盘，以"微创新"小步快跑试错，构建社交/游戏/内容/支付/云五大引擎，定位"连接器"赋能实体经济，不与合作伙伴争利，成产品驱动/生态共生/产业赋能三维典范。',
        'reason_en': 'Pony Ma with "user-centric" as product compass, "micro-innovation" rapid trial-error, builds five engines: social/gaming/content/payment/cloud, positions as "connector" empowering real economy, not competing with partners, becoming product-driven/ecosystem symbiosis/industrial empowerment three-dimensional paradigm.',
        'steps_zh': ['用户锚定：确立"用户为本"为唯一判断标准，所有产品决策从用户价值出发', '微创新：小步快跑/灰度测试/快速迭代，QQ/微信/游戏/支付/云持续微创新', '连接器定位：不做平台主宰，做"连接器"，连接用户/连接内容/连接服务/连接产业', '生态共生：游戏分账/小程序/视频号/腾讯云，与合作伙伴分享流量/技术/资本，共生共赢', '产业互联网：2018年提出"产业互联网"，以云/大数据/AI/安全赋能实体经济数字化转型'],
        'steps_en': ['User Anchoring: Establish "user-centric" as sole judgment criterion, all product decisions from user value', 'Micro-Innovation: Small steps fast run/gray testing/rapid iteration, QQ/WeChat/gaming/payment/cloud continuous micro-innovation', 'Connector Positioning: Not platform ruler, but "connector", connecting users/content/services/industries', 'Ecosystem Symbiosis: Game revenue sharing/Mini Programs/Video Accounts/Tencent Cloud, share traffic/tech/capital with partners, symbiosis', 'Industrial Internet: Proposed "Industrial Internet" in 2018, empower real economy digital transformation with cloud/big data/AI/security'],
        'expected_zh': '成中国产品驱动/生态共生/产业赋能三维典范，腾讯市值超万亿、微信月活13亿、云计算国内第二',
        'expected_en': 'Become Chinese product-driven/ecosystem symbiosis/industrial empowerment three-dimensional paradigm, Tencent market cap >1T, WeChat MAU 1.3B, cloud domestic #2',
        'case_zh': '1998年创立腾讯，QQ确立社交霸主，2011年微信重新定义移动社交，游戏/支付/云三大引擎支撑营收万亿。其"用户为本/微创新/连接器/共生"四大算子，成中国产品型企业教科书。2018年重组"两网一云"，全面拥抱产业互联网。',
        'case_en': 'Founded Tencent in 1998, QQ established social dominance, WeChat redefined mobile social in 2011, gaming/payment/cloud three engines support trillion revenue. Four operators: user-centric/micro-innovation/connector/symbiosis, becoming textbook for Chinese product-driven enterprises. 2018 reorganized "two networks one cloud", fully embracing industrial internet.'
    },
    {
        'code': 'H-LJ-273',
        'name_zh': '雷军：小米/极致性价比/铁人三项/平台战略/用户共创',
        'name_en': 'Lei Jun: Xiaomi/Extreme Cost-Performance/Ironman Triathlon/Platform Strategy/User Co-creation',
        'desc_zh': '小米创始人，以"极致性价比"重新定义硬件商业模式，"铁人三项"(极致产品/极致性价比/极致服务)为方法论，构建"手机×AIoT"双引擎平台，践行"与用户做朋友"用户共创，成中国硬件重塑/平台生态/用户共创三维典范。',
        'desc_en': 'Xiaomi founder, redefined hardware business model with "extreme cost-performance", "Ironman Triathlon" (extreme product/extreme cost-performance/extreme service) as methodology, built "phone×AIoT" dual-engine platform, practiced "make friends with users" user co-creation, becoming Chinese hardware reshaping/platform ecology/user co-creation three-dimensional paradigm.',
        'modes': [19, 18, 6, 31, 11],
        'reason_zh': '雷军以"极致性价比"打破暴利定价，"铁人三项"为产品方法论，"手机×AIoT"双引擎构建平台生态，"与用户做朋友"开创用户共创模式，成硬件商业模式重塑/平台生态/用户共创三维典范。',
        'reason_en': 'Lei Jun broke predatory pricing with "extreme cost-performance", "Ironman Triathlon" as product methodology, "phone×AIoT" dual-engine platform ecosystem, "make friends with users" pioneering user co-creation, becoming hardware business model reshaping/platform ecology/user co-creation three-dimensional paradigm.',
        'steps_zh': ['性价比锚定：确立"极致性价比"为核心价值主张，硬件净利润率永不超过5%', '铁人三项：极致产品/极致性价比/极致服务三位一体，小米手机/小米电视/小米生态链全线贯彻', '双引擎平台：手机为入口，AIoT为延伸，构建"手机×AIoT"智能生活平台', '用户共创：MIUI论坛/米粉社区/大师课/众筹，用户参与设计/测试/传播/服务全生命周期', '生态投资：投资/孵化生态链企业(九号/华米/绿米/石头/追觅)，输出品牌/渠道/供应链/管理'],
        'steps_en': ['Cost-Performance Anchoring: Establish "extreme cost-performance" as core value proposition, hardware net margin never exceed 5%', 'Ironman Triathlon: Extreme product/extreme cost-performance/extreme service trinity, Xiaomi phone/TV/ecosystem chain all-through', 'Dual-Engine Platform: Phone as entry, AIoT as extension, build "phone×AIoT" smart life platform', 'User Co-creation: MIUI forum/Mi Fan community/Master class/crowdfunding, users participate in design/testing/promotion/service full lifecycle', 'Ecosystem Investment: Invest/incubate ecosystem chain companies (Ninebot/Huami/Greenmi/Roborock/Dreame), output brand/channel/supply chain/management'],
        'expected_zh': '成中国硬件重塑/平台生态/用户共创三维典范，小米手机全球前三、AIoT设备连接数超6亿、生态链企业估值超万亿',
        'expected_en': 'Become Chinese hardware reshaping/platform ecology/user co-creation three-dimensional paradigm, Xiaomi phone global top 3, AIoT connected devices >600M, ecosystem chain valuation >1T',
        'case_zh': '2010年创立小米，MIUI论坛积累首批种子用户，2011年小米1以1999元重新定义旗舰性价比，2014年提出"手机×AIoT"，2018年上市。其"性价比/铁人三项/双引擎/共创"四大算子，成中国硬件互联网企业教科书。',
        'case_en': 'Founded Xiaomi in 2010, MIUI forum accumulated seed users, Mi 1 redefined flagship cost-performance at 1999 RMB in 2011, proposed "phone×AIoT" in 2014, IPO in 2018. Four operators: cost-performance/Ironman/dual-engine/co-creation, becoming textbook for Chinese hardware internet enterprises.'
    },
    {
        'code': 'H-WX-274',
        'name_zh': '王兴：美团/多快好省/To C 连接 To B/快速迭代/本地生活',
        'name_en': 'Wang Xing: Meituan/Fast Cheap Good Save/To C Connect To B/Rapid Iteration/Local Life',
        'desc_zh': '美团创始人，以"多快好省"重新定义本地生活服务效率，"To C连接To B"双边市场模式，"快速迭代/小步快跑"组织能力，构建"外卖+到店+到家+酒旅"本地生活超级平台，成中国O2O/双边市场/本地生活三维典范。',
        'desc_en': 'Meituan founder, redefined local life service efficiency with "fast cheap good save", "To C connects To B" two-sided market model, "rapid iteration/small steps fast run" organizational capability, built "takeaway+in-store+home+hotel-travel" local life super platform, becoming Chinese O2O/two-sided market/local life three-dimensional paradigm.',
        'modes': [15, 16, 11, 31, 18],
        'reason_zh': '王兴以"多快好省"为用户价值锚点，"外卖/到店/到家/酒旅"四大业务板块全覆盖，"骑手/商家/用户"三边市场精细运营，"算法调度/实时优化"极致效率，成O2O闭环/双边市场/本地生活三维典范。',
        'reason_en': 'Wang Xing anchored "fast cheap good save" as user value, four business blocks full coverage, "rider/merchant/user" three-sided market refined operation, "algorithm scheduling/real-time optimization" extreme efficiency, becoming O2O closure/two-sided market/local life three-dimensional paradigm.',
        'steps_zh': ['效率锚定："多快好省"为核心价值，外卖30分钟达/到店秒核销/到家准时率99%+', '双边市场：To C(用户/骑手)连接 To B(商家/供应链)，补贴/流量/工具三位一体激活两边', '快速迭代：小步快跑/灰度发布/A/B测试，周级迭代/日级发布，外卖/到店/到家/酒旅并行', '算法调度：实时订单分配/路径规划/骑手调度/商家备餐，强化学习/运筹优化极致效率', '本地生活超级平台：外卖/到店/到家/酒旅/打车/充电/医药，一站式满足用户吃喝玩乐住行'],
        'steps_en': ['Efficiency Anchoring: "Fast cheap good save" as core value, takeaway 30min/in-store instant verification/home delivery 99%+ on-time', 'Two-Sided Market: To C(user/rider) connect To B(merchant/supply chain), subsidy/traffic/tools trinity activate both sides', 'Rapid Iteration: Small steps fast run/gray release/A/B testing, weekly iteration/daily release, takeaway/in-store/home/travel parallel', 'Algorithm Scheduling: Real-time order allocation/route planning/rider dispatch/merchant prep, RL/operations research extreme efficiency', 'Local Life Super Platform: Takeaway/in-store/home/travel/ride-hailing/charging/medicine, one-stop satisfy user eat/play/live/travel'],
        'expected_zh': '成中国O2O/双边市场/本地生活三维典范，美团年交易额超万亿、骑手超700万、商家超1000万',
        'expected_en': 'Become Chinese O2O/two-sided market/local life three-dimensional paradigm, Meituan annual GMV >1T, riders >7M, merchants >10M',
        'case_zh': '2003年校内网/2008年饭否/2010年美团网，2015年大众点评合并，2018年上市。外卖/到店/到家/酒旅四轮驱动，骑手/商家/用户三边市场，算法调度极致效率。其"效率/双边/迭代/算法"四大算子，成中国本地生活平台教科书。',
        'case_en': 'Xiaonei 2003/Fanfou 2008/Meituan 2010, merged Dianping 2015, IPO 2018. Takeaway/in-store/home/travel four-wheel drive, rider/merchant/user three-sided market, algorithm scheduling extreme efficiency. Four operators: efficiency/two-sided/iteration/algorithm, becoming textbook for Chinese local life platforms.'
    },
    {
        'code': 'H-ZYM-275',
        'name_zh': '张一鸣：字节跳动/算法推荐/延迟满足/全球化/组织效率',
        'name_en': 'Zhang Yiming: ByteDance/Algorithm Recommendation/Delayed Gratification/Globalization/Org Efficiency',
        'desc_zh': '字节跳动创始人，以"算法推荐"重新定义信息分发，"延迟满足"长期主义战略，"全球化"首战即决战，"组织效率/Context not Control"管理哲学，构建"今日头条/抖音/TikTok/飞书/火山引擎"多产品矩阵，成中国算法驱动/全球化/组织进化三维典范。',
        'desc_en': 'ByteDance founder, redefined information distribution with "algorithm recommendation", "delayed gratification" long-termism, "globalization" first battle decisive, "org efficiency/Context not Control" management philosophy, built "Toutiao/Douyin/TikTok/Lark/Volcano Engine" multi-product matrix, becoming Chinese algorithm-driven/globalization/org evolution three-dimensional paradigm.',
        'modes': [17, 12, 31, 32, 18],
        'reason_zh': '张一鸣以"算法推荐"替代社交图谱重新定义内容分发，"延迟满足"坚持长期正确/短期被误解，"Context not Control"输出语境而非控制，"全球化首战即决战"TikTok一年破亿，成算法分发/长期主义/组织进化三维典范。',
        'reason_en': 'Zhang Yiming redefined content distribution with "algorithm recommendation" replacing social graph, "delayed gratification" insist long-term right/short-term misunderstood, "Context not Control" output context not control, "globalization first battle decisive" TikTok 100M in one year, becoming algorithm distribution/long-termism/org evolution three-dimensional paradigm.',
        'steps_zh': ['算法重构：以推荐算法替代订阅/社交分发，冷启动/兴趣图谱/实时反馈，信息找人而非人找信息', '延迟满足：坚持长期正确/短期被误解，抖音前两年不商业化/飞书三年打磨/TikTok先投入后收割', 'Context not Control：不发号施令，输出战略语境/目标/数据，让一线听得见炮火的人做决策', '全球化首战：TikTok"去中心化/本地化运营/算法出海"，一年用户破亿，成中国App出海标杆', '组织效率：飞书内部犹豫/OKR/文档/会议/招聘全流程数字化，人均产出行业领先'],
        'steps_en': ['Algorithm Reconstruction: Replace subscription/social distribution with recommendation algorithm, cold start/interest graph/real-time feedback, info finds people not people find info', 'Delayed Gratification: Insist long-term right/short-term misunderstood, Douyin 2 years no monetization/Lark 3 years polish/TikTok invest first harvest later', 'Context not Control: No command control, output strategic context/goals/data, let frontline who hear gunfire make decisions', 'Globalization First Battle: TikTok "decentralized/localized operation/algorithm going global", 100M users in 1 year, benchmark for Chinese App going global', 'Org Efficiency: Lark internal hesitation/OKR/docs/meetings/recruitment full-process digitalization, per-capita output industry leading'],
        'expected_zh': '成中国算法驱动/全球化/组织进化三维典范，字节营收超万亿、全球月活超30亿、飞书/火山引擎B端突围',
        'expected_en': 'Become Chinese algorithm-driven/globalization/org evolution three-dimensional paradigm, ByteDance revenue >1T, global MAU >3B, Lark/Volcano Engine B-end breakout',
        'case_zh': '2012年创立字节，2012年今日头条/2016年抖音/2017年TikTok出海/2019年飞书/2021年火山引擎。其"算法/延迟满足/语境管理/全球化"四大算子，成中国互联网企业组织进化教科书。',
        'case_en': 'Founded ByteDance 2012, Toutiao 2012/Douyin 2016/TikTok 2017/Lark 2019/Volcano Engine 2021. Four operators: algorithm/delayed gratification/context management/globalization, becoming textbook for Chinese internet enterprise org evolution.'
    },
    {
        'code': 'H-HZ-276',
        'name_zh': '黄峥：拼多多/拼团/C2M/农业上行/首善文化',
        'name_en': 'Colin Huang: Pinduoduo/Group Buying/C2M/Agriculture Upstream/First Goodness Culture',
        'desc_zh': '拼多多创始人，以"拼团/C2M"重新定义电商供需关系，"农业上行"解决卖难问题，"首善文化"(利他/长期主义/极致性价比)为文化内核，"农研科技/多多买菜"双轮驱动，成中国C2M模式/农业数字化/利他商业三维典范。',
        'desc_en': 'Pinduoduo founder, redefined e-commerce supply-demand with "group buying/C2M", "agriculture upstream" solved selling difficulty, "first goodness culture" (altruism/long-termism/extreme cost-performance) as cultural core, "agri-tech/DuoDuo Maicai" dual-wheel drive, becoming Chinese C2M model/agriculture digitalization/altruistic business three-dimensional paradigm.',
        'modes': [19, 16, 6, 32, 11],
        'reason_zh': '黄峥以"拼团"社交裂变获客，"C2M"反向定制消除中间商，"农业上行"助农增收，"首善文化"利他为本/长期主义/极致性价比，成C2M创新/农业数字化/利他商业三维典范。',
        'reason_en': 'Colin Huang acquired users via "group buying" social fission, "C2M" reverse customization eliminating middlemen, "agriculture upstream" helping farmers increase income, "first goodness culture" altruism-first/long-termism/extreme cost-performance, becoming C2M innovation/agriculture digitalization/altruistic business three-dimensional paradigm.',
        'steps_zh': ['社交裂变：以"拼团/砍一刀"社交裂变极低成本获客，下沉市场用户快速渗透', 'C2M反向定制：用户需求直接传导工厂，消除中间商/库存/营销成本，极致性价比', '农业上行：多多买菜/农研科技/产地直发，解决农产品卖难/损耗大/品控难，助农增收', '首善文化：利他为本/长期主义/极致性价比，不做短期ROI计算，只做对用户/农民/商家长期有价值的事', '农研科技：建立农业科学研究院/标准化种植/冷链物流/品牌孵化，以科技赋能农业全链路'],
        'steps_en': ['Social Fission: "Group buying/slash one cut" social fission ultra-low cost acquisition, sinking market users rapid penetration', 'C2M Reverse Customization: User demand directly to factory, eliminate middlemen/inventory/marketing costs, extreme cost-performance', 'Agriculture Upstream: DuoDuo Maicai/agri-tech/origin direct shipping, solve agri-product selling difficulty/high loss/quality control, help farmers increase income', 'First Goodness Culture: Altruism-first/long-termism/extreme cost-performance, no short-term ROI calc, only do things long-term valuable to users/farmers/merchants', 'Agri-Tech: Establish agricultural research institute/standardized planting/cold chain logistics/brand incubation, empower agriculture full chain with tech'],
        'expected_zh': '成中国C2M创新/农业数字化/利他商业三维典范，拼多多年GMV超万亿、用户超9亿、多多买菜日单量百万级',
        'expected_en': 'Become Chinese C2M innovation/agriculture digitalization/altruistic business three-dimensional paradigm, Pinduoduo annual GMV >1T, users >900M, DuoDuo Maicai daily orders million-level',
        'case_zh': '2015年创立拼多多，2018年上市，2020年黄峥退休传承陈磊。"拼团/C2M/农业上行/首善"四大算子，成中国新消费/农业数字化/利他商业教科书。',
        'case_en': 'Founded Pinduoduo 2015, IPO 2018, Huang Zheng retired 2020 succeeded by Chen Lei. Four operators: group buying/C2M/agriculture upstream/first goodness, becoming textbook for Chinese new consumption/agriculture digitalization/altruistic business.'
    },
    {
        'code': 'H-LYH-277',
        'name_zh': '李彦宏：百度/AI先行/搜索/自动驾驶/技术理想主义',
        'name_en': 'Robin Li: Baidu/AI First/Search/Autonomous Driving/Tech Idealism',
        'desc_zh': '百度创始人，以"技术理想主义"坚持AI First战略，"搜索"建立中文互联网入口，"自动驾驶/Apollo/文心一言"全栈布局AI，"技术改变世界"为使命，成中国AI先行/搜索垄断/技术理想主义三维典范。',
        'desc_en': 'Baidu founder, with "tech idealism" insisting AI First strategy, "search" established Chinese internet entry, "autonomous driving/Apollo/ERNIE Bot" full-stack AI layout, "technology changes world" as mission, becoming Chinese AI first/search monopoly/tech idealism three-dimensional paradigm.',
        'modes': [17, 12, 9, 31, 18],
        'reason_zh': '李彦宏以"技术理想主义"坚持AI First十年不动摇，"超链分析"奠基搜索霸主，"Apollo/文心一言/百度智能云"全栈AI布局，"技术改变世界"使命感贯穿始终，成AI先行/搜索入口/技术理想主义三维典范。',
        'reason_en': 'Robin Li with "tech idealism" insisted AI First for ten years unwavering, "hyperlink analysis" founded search dominance, "Apollo/ERNIE/Baidu Cloud" full-stack AI layout, "technology changes world" mission throughout, becoming AI first/search entry/tech idealism three-dimensional paradigm.',
        'steps_zh': ['技术锚定：确立"AI First"为公司战略，研发投入常年超15%，专利申请量中国第一', '搜索垄断：超链分析/中文语义理解/知识图谱，构建中文互联网最强入口护城河', '全栈AI：Apollo自动驾驶/文心大模型/百度智能云/小度助手/度目视觉，芯片/框架/模型/应用全栈自研', '技术理想主义：坚持"技术改变世界"，不追逐风口/不做低技术含量业务，只做难而正确的事', '开放生态：Apollo开源/飞桨开源/百度智能云开放，以平台思维赋能产业智能化转型'],
        'steps_en': ['Tech Anchoring: Establish "AI First" as company strategy, R&D investment >15% consistently, patent applications China #1', 'Search Monopoly: Hyperlink analysis/Chinese semantic understanding/knowledge graph, build strongest Chinese internet entry moat', 'Full-Stack AI: Apollo autonomous driving/ERNIE large model/Baidu Cloud/Xiaodu Assistant/Dumei vision, chip/framework/model/application full-stack proprietary', 'Tech Idealism: Insist "technology changes world", not chase trends/no low-tech business, only do hard but right things', 'Open Ecosystem: Apollo open source/PaddlePaddle open source/Baidu Cloud open, empower industry intelligent transformation with platform thinking'],
        'expected_zh': '成中国AI先行/搜索垄断/技术理想主义三维典范，百度Apollo累计测试里程超1亿公里、文心大模型日调用超10亿、专利申请量连续多年中国第一',
        'expected_en': 'Become Chinese AI first/search monopoly/tech idealism three-dimensional paradigm, Baidu Apollo accumulated test mileage >100M km, ERNIE daily calls >1B, patent applications China #1 for consecutive years',
        'case_zh': '2000年创立百度，2005年上市，2010年启动AI布局，2017年"All in AI"，2023年文心一言发布。其"AI First/搜索护城河/全栈自研/技术理想主义"四大算子，成中国AI企业教科书。',
        'case_en': 'Founded Baidu 2000, IPO 2005, started AI layout 2010, "All in AI" 2017, ERNIE Bot launched 2023. Four operators: AI First/search moat/full-stack proprietary/tech idealism, becoming textbook for Chinese AI enterprises.'
    },
    {
        'code': 'H-DL-278',
        'name_zh': '丁磊：网易/游戏/邮箱/养猪/网易云音乐/极致产品',
        'name_en': 'William Ding: NetEase/Gaming/Email/Pig Farming/NetEase Cloud Music/Extreme Product',
        'desc_zh': '网易创始人，以"极致产品"为核心竞争力，"免费邮箱"开启互联网普惠，"自研游戏/代理暴雪"双轮驱动游戏霸主，"网易云音乐/严选/养猪/考拉"多元化探索，"用户体验至上"为产品准则，成中国产品驱动/多元化/极致体验三维典范。',
        'desc_en': 'NetEase founder, with "extreme product" as core competitiveness, "free email" started internet inclusivity, "self-developed games/agency Blizzard" dual-wheel game dominance, "NetEase Cloud Music/Yanxuan/pig farming/Kaola" diversified exploration, "user experience supreme" as product principle, becoming Chinese product-driven/diversification/extreme experience three-dimensional paradigm.',
        'modes': [23, 11, 6, 32, 18],
        'reason_zh': '丁磊以"极致产品"为唯一标准，网易邮箱/网易游戏/网易云音乐/严选/养猪/考拉，每一个业务都做到行业极致，"不做平庸产品"为铁律，成产品驱动/多元化/极致体验三维典范。',
        'reason_en': 'William Ding with "extreme product" as sole standard, NetEase email/games/cloud music/yanxuan/pig farming/Kaola, every business done to industry extreme, "no mediocre products" as iron law, becoming product-driven/diversification/extreme experience three-dimensional paradigm.',
        'steps_zh': ['极致产品：确立"不做平庸产品"为铁律，每个业务必须做到行业前三或不做', '免费策略：网易免费邮箱/免费游戏/免费音乐，以免费重塑行业商业模式，用规模换空间', '自研+代理：自研《梦幻西游/大话西游/逆水寒》+代理《魔兽世界/守望先锋》，游戏双轮驱动', '多元化克制：邮箱/游戏/音乐/新闻/严选/养猪/考拉，每个业务独立核算/独立运营/独立品牌', '用户体验：网易云音乐社区/评论/歌单/推荐，严选供应链溯源/品控，养猪区块链溯源/黑猪肉品质'],
        'steps_en': ['Extreme Product: Establish "no mediocre products" as iron law, every business must be industry top 3 or not do', 'Free Strategy: NetEase free email/free games/free music, reshape industry business model with free, trade scale for space', 'Self-dev + Agency: Self-developed "Fantasy Westward Journey/Westward Journey/Naraka" + agency "WoW/Overwatch", game dual-wheel drive', 'Diversification with Restraint: Email/games/music/news/yanxuan/pig farming/Kaola, each business independent accounting/operation/brand', 'User Experience: NetEase Cloud Music community/comments/playlists/recommendation, Yanxuan supply chain traceability/quality control, pig farming blockchain traceability/black pork quality'],
        'expected_zh': '成中国产品驱动/多元化/极致体验三维典范，网易游戏营收超800亿、云音乐用户超8亿、严选GMV超百亿',
        'expected_en': 'Become Chinese product-driven/diversification/extreme experience three-dimensional paradigm, NetEase games revenue >80B, Cloud Music users >800M, Yanxuan GMV >10B',
        'case_zh': '1997年创立网易，1997年免费邮箱/2001年游戏/2013年云音乐/2014年严选/2017年养猪。其"极致产品/免费策略/自研+代理/多元化"四大算子，成中国产品型互联网企业教科书。',
        'case_en': 'Founded NetEase 1997, free email 1997/games 2001/cloud music 2013/yanxuan 2014/pig farming 2017. Four operators: extreme product/free strategy/self-dev+agency/diversification, becoming textbook for Chinese product-driven internet enterprises.'
    },
    {
        'code': 'H-CW-279',
        'name_zh': '程维：滴滴/出行平台/算法调度/安全体系/多边市场',
        'name_en': 'Cheng Wei: Didi/Travel Platform/Algorithm Dispatch/Safety System/Multi-sided Market',
        'desc_zh': '滴滴创始人，以"算法调度"重新定义出行效率，"多边市场"(乘客/司机/车主/车企/监管)精细平衡，"安全体系/信用分/实名认证/紧急按钮"构建信任基石，"出行+金融+车服务+自动驾驶"全生态布局，成中国算法调度/多边平台/安全信任三维典范。',
        'desc_en': 'Didi founder, redefined travel efficiency with "algorithm dispatch", "multi-sided market" (passengers/drivers/owners/OEMs/regulators) delicate balance, "safety system/credit score/real-name/emergency button" built trust foundation, "travel+finance+vehicle services+autonomous driving" full ecology layout, becoming Chinese algorithm dispatch/multi-sided platform/safety trust three-dimensional paradigm.',
        'modes': [15, 16, 31, 32, 18],
        'reason_zh': '程维以"算法调度"解决供需匹配难题，"多边市场"精细平衡乘客/司机/监管三方利益，"安全红线"零容忍构建信任体系，"出行+金融+车服务+自动驾驶"全生态闭环，成算法调度/多边市场/安全信任三维典范。',
        'reason_en': 'Cheng Wei solved supply-demand matching with "algorithm dispatch", "multi-sided market" delicately balanced passenger/driver/regulator interests, "safety red line" zero tolerance built trust system, "travel+finance+vehicle services+autonomous driving" full ecology closure, becoming algorithm dispatch/multi-sided platform/safety trust three-dimensional paradigm.',
        'steps_zh': ['算法调度：实时供需预测/订单分配/路径规划/动态定价，强化学习/运筹优化极致匹配效率', '多边平台：乘客/司机/车主/车企/监管五边市场，补贴/分成/规则/信用/安全五维平衡', '安全红线：实名认证/人脸识别/行程分享/紧急按钮/录音/安全中心/信用分，零容忍构建信任', '全生态闭环：出行(网约车/顺风车/专车/公交/代驾)+金融(滴滴金融)+车服务(加油/维修/保险/充电)+自动驾驶', '数据智能：城市交通大脑/智慧交通/碳中和/公共交通接驳，以数据赋能城市治理'],
        'steps_en': ['Algorithm Dispatch: Real-time supply-demand prediction/order allocation/route planning/dynamic pricing, RL/operations research extreme matching efficiency', 'Multi-sided Platform: Passenger/driver/owner/OEM/regulator five-sided market, subsidy/sharing/rules/credit/safety five-dimensional balance', 'Safety Red Line: Real-name/face recognition/trip sharing/emergency button/recording/safety center/credit score, zero tolerance build trust', 'Full Ecology Closure: Travel(ride-hail/carpool/premier/bus/designated)+Finance(Didi Finance)+Vehicle Services(fuel/repair/insurance/charging)+Autonomous Driving', 'Data Intelligence: City traffic brain/smart traffic/carbon neutrality/public transit connection, empower city governance with data'],
        'expected_zh': '成中国算法调度/多边市场/安全信任三维典范，滴滴日单量超3000万、注册司机超3000万、覆盖城市超400个',
        'expected_en': 'Become Chinese algorithm dispatch/multi-sided platform/safety trust three-dimensional paradigm, Didi daily orders >30M, registered drivers >30M, cities covered >400',
        'case_zh': '2012年创立滴滴，2015年快的合并，2018年顺风车事件后整改重塑安全体系，2021年上市。其"算法/多边/安全/生态"四大算子，成中国平台型出行企业教科书。',
        'case_en': 'Founded Didi 2012, merged Kuaidi 2015, rectified safety system after 2018 hitchhike incident, IPO 2021. Four operators: algorithm/multi-sided/safety/ecology, becoming textbook for Chinese platform-based travel enterprises.'
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

print(f'Added {len(figures)} modern entrepreneurs')
print(f'Total ZH: {len(zh)}, H-: {sum(1 for k in zh if k.startswith("H-"))}')
print(f'Total EN: {len(en)}, H-: {sum(1 for k in en if k.startswith("H-"))}')
print(f'CODE_MAP: {len(cm["CODE_MAP"])}')