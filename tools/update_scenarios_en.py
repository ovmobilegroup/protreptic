import json

# Load existing scenarios
with open('scenarios_en.json', 'r', encoding='utf-8') as f:
    scenarios_en = json.load(f)

# New English scenarios for historical figures
new_scenarios_en = {
    "H-LB-01": {
        "name": "Liu Bang: Emperor's Delegation Mastery",
        "description": "How to trust talent, share rewards, provide safety net, build lasting dynasty",
        "modes": [33, 6, 11, 13, 1],
        "reason": "Liu Bang's 'Three Heroes' all surpassed him (Zhang Liang strategy, Xiao He governance, Han Xin command), yet he founded the Han dynasty. Great leaders don't micromanage; they hold the strategic reins. Identify talent, set strategy, share rewards, provide safety net — the CEO's core capabilities.",
        "steps": [
            "Step 1: Identify talent — Look for 'ability to deliver' not 'loyalty/pedigree/connections'",
            "Step 2: Delegate — Only make 'irreplaceable decisions': direction, people, resource allocation, bottom lines",
            "Step 3: Share rewards — Make benefit distribution explicit: equity, bonuses, honor, security",
            "Step 4: Safety net — Build fault tolerance: controlled experiment cost, failure protection, shared success",
            "Step 5: Review — Quarterly 'person-role fit' assessment, dynamic adjustment"
        ],
        "expected": [
            "Core role person-role fit >90%",
            "Founder liberated from micromanagement",
            "Team autonomous delivery significantly improved"
        ],
        "case": "Liu Bang employing Han Xin: Han Xin was initially a Chu army courier, joined Han then faced execution for a crime, Xiao He chased him down at night to recommend. Liu Bang didn't ask about background, didn't hold past against him, valued his 'peerless national talent'. Appointed Grand General, gave seals, troops, strategic autonomy. Enfeoffed as King of Qi, gave highest honor and real benefits. After Pengcheng defeat didn't blame, instead added territory and troops. Result: Han Xin pacified Yan/Zhao east, struck Qi, destroyed Chu west, established the great Han empire."
    },
    "H-LX-02": {
        "name": "Liu Xiu: Pragmatic Restoration of Guangwu",
        "description": "Second entrepreneurship in existing market: steady > aggressive, hearts > territory",
        "modes": [5, 21, 34, 8, 6, 1],
        "reason": "Liu Xiu ended Wang Mang's chaos, created 'Guangwu Restoration'. Pragmatic truth-seeking, benevolent governance, risk control. Second entrepreneurship in existing market core: steady > aggressive, hearts > territory.",
        "steps": [
            "Step 1: Seek truth from facts — No boasting, no exaggeration, no overreach",
            "Step 2: Benevolent governance — Pacify Tongma/Chimei, abolish cruel officials, light taxes",
            "Step 3: Institutional checks — Wine cup releasing military power, three-way power division, Shangshu Tai decision-making",
            "Step 4: Personal handling of affairs — Diligent in governance, reviewing memorials, strict supervision of officials",
            "Step 5: Risk control — No exhaustive warfare, recuperation, keep reserves"
        ],
        "expected": [
            "Social order rapidly restored",
            "Population and economy grow steadily",
            "Foundation for 200 years of Eastern Han"
        ],
        "case": "Guangwu Restoration: Liu Xiu rose from Wang Mang's chaos with 'pacifying people' as core. Not pursuing quick victory, first stabilized Hebei base, then gradually recovered the empire. Treated surrendered generals well (e.g. Tongma/Chimei), no post-settlement settling. Established 'Three Excellencies no power, Nine Ministers divide duties, Shangshu Tai decides' checks system. Personally reviewed memorials, strictly supervised official corruption. Result: population recovered from 20M to 50M, known as 'Guangwu Restoration'."
    },
    "H-LS-03": {
        "name": "Li Shimin: Systematic Zhenguan Governance",
        "description": "Building error-correction mechanisms matters more than personal brilliance",
        "modes": [33, 12, 10, 21, 18, 5, 34],
        "reason": "Li Shimin accepted advice humbly, Wei Zheng remonstrated 200+ times; perfected imperial exams,府兵制; established 'ruler-minister co-governance' error correction. Error-correction mechanisms matter more than personal brilliance.",
        "steps": [
            "Step 1: Strategic delegation — Only make irreplaceable decisions, delegate professional matters to professionals",
            "Step 2: Open speech channels — Set remonstrance officials, open Yanying Hall dialogues, reward frankness, protect dissent",
            "Step 3: Institutional design — Perfect imperial exams,府兵制,租调庸制, legal codes",
            "Step 4: Self-restraint — 'Copper mirror adjusts attire; history mirror knows rise/fall; people mirror knows gain/loss'",
            "Step 5: Dynamic adjustment — Regularly review institutional execution deviations, promptly patch loopholes"
        ],
        "expected": [
            "Political clarity, economic prosperity, ethnic integration",
            "Systems outlive individual lifecycles",
            "Become benchmark for future golden ages"
        ],
        "case": "Zhenguan Governance: After Xuanwu Gate Incident, Li Shimin didn't purge dissenters but absorbed Fang Xuanling, Du Ruhui, Wei Zheng etc. Set up remonstrance system, Wei Zheng remonstrated 200+ times, all accepted. Perfected imperial exams, 府兵制, legal codes, established 'ruler-minister co-governance'. Self-restraint: halted palace construction, reduced meals/music, lenient punishments/light taxes. Result: households from 2M to 3.8M, grain 3-4 qian per dou, doors unbarred at night."
    },
    "H-ZK-04": {
        "name": "Zhao Kuangyin: Institutional Checks via Wine Banquet",
        "description": "Using systems to solve trust problems — don't guard against people, guard against system loopholes",
        "modes": [34, 40, 28, 32, 12, 8],
        "reason": "Zhao Kuangyin learned from Five Dynasties warlordism, wine cup releasing military power, three yamen dividing command, Privy Council checks. Systems solve principal-agent problems: don't guard people, guard system loopholes.",
        "steps": [
            "Step 1: Identify core risk — Military power decentralization is root cause of dynastic collapse",
            "Step 2: Gentle stripping — Wine cup releasing power, treat ministers well, lifetime wealth, don't kill meritorious officials",
            "Step 3: Three powers separation — Command (three yamen)/Deployment (Privy Council)/Administration (three ministries) separated",
            "Step 4: Civilian control of military — Dispatch civil officials to monitor armies, rotate generals, professionalize imperial guards",
            "Step 5: Interest binding — High salaries, hereditary honors, family wealth, bind elite interests to dynasty"
        ],
        "expected": [
            "Northern Song no internal rebellions, no warlordism",
            "Civil official group stable governance 300 years",
            "System cost far lower than personal rule cost"
        ],
        "case": "Wine Cup Releasing Military Power: 961 Zhao Kuangyin banqueted Shi Shouxin et al. 'Life is short, why not retire to fields'. Next day generals petitioned to resign military commands, reassigned as military governors, granted massive gold and fields. Then established Privy Council for deployment, three yamen divide command, rotate generals, civil officials monitor armies. Result: Northern Song 300 years no warlord chaos, civil official governance became institution."
    },
    "H-CJ-05": {
        "name": "Genghis Khan: Meritocracy and Information Velocity",
        "description": "Organizational competition is fundamentally information velocity competition",
        "modes": [18, 41, 12, 28, 15, 3],
        "reason": "Thousand-household/ten-thousand-household system, Great Yassa, relay stations. Meritocracy, rule of law in military, intelligence systems. Organization = talent density × collaboration efficiency × information velocity.",
        "steps": [
            "Step 1: Meritocracy — Ignore background, only ability, promote exceptionally, reward immediately",
            "Step 2: Rule of law in military — Great Yassa written law, clear rewards/punishments, military orders like mountains",
            "Step 3: Intelligence system — Relay stations covering empire, merchant intelligence, scout networks",
            "Step 4: Power separation — Thousand/tenthousand household system, imperial guards direct, four great ordos enfeoffed",
            "Step 5: Religious tolerance — Don't interfere with beliefs, absorb diverse cultures, reduce governance costs"
        ],
        "expected": [
            "Established largest contiguous land empire in history",
            "Military mobility/information speed crushed contemporary civilizations",
            "Multi-ethnic fusion governance model continues today"
        ],
        "case": "Mongol Empire Rise: Genghis Khan unified Mongol tribes, established thousand/tenthousand household system breaking tribal boundaries. Relay stations every 25-30km, information travels 400km/day, far exceeding contemporary Song/Jin. Great Yassa established 'stealing 99+ horses death penalty' etc. Four great ordos enfeoffed meritorious officials but retained central deployment authority. Result: Spanning Eurasia, established largest contiguous land empire in human history."
    },
    "H-ZY-06": {
        "name": "Zhu Yuanzhang: Extreme Risk Control and Power Concentration",
        "description": "Strong control in startup phase, need delegation in maturity — he didn't do the latter",
        "modes": [28, 32, 1, 14, 8, 35],
        "reason": "Abolished Chancellor, Embroidered Uniform Guard, Hongwu Governance. Strong control in startup, need delegation in maturity — he failed at the latter, causing later rigidity. Negative case: over-control kills organizational evolution.",
        "steps": [
            "Step 1: Abolish Chancellor — One person handles six ministries, decision efficiency max but bottleneck is self",
            "Step 2: Embroidered Uniform Guard terror rule — Govern by punishment, eyes/ears, fear-driven",
            "Step 3: Severe laws — Major cases frequent, collective punishment extensive, officials dare not act",
            "Step 4: Grassroots empathy — Tax relief/disaster relief, military farming, limit large landlord annexation",
            "Step 5: Succession dilemma — Abolished Crown Prince, enfeoffed princes, ultimately Jingnan Coup usurpation"
        ],
        "expected": [
            "Short-term: Social order rebuilt, economy rapid recovery",
            "Long-term: Bureaucracy rigidified, innovation drive exhausted, border defense weakened",
            "Lesson: Over-control kills organizational evolution capacity"
        ],
        "case": "Hongwu Governance: Zhu Yuanzhang abolished Chancellor, personally managed six ministries, established Embroidered Uniform Guard surveillance, four major cases killed tens of thousands. Officials 'dare not speak, dare not move, dare not act'. Economically tax relief/disaster relief, military farming, limit annexation, population from 60M to 100M. But abolishing Chancellor caused emperor overload, Embroidered Uniform Guard cruel officials rampant, border defense weakened by over-centralization. Mid-Ming cabinet system alleviated but institutional rigidity already set."
    },
    "H-HT-07": {
        "name": "Huang Taiji: Strategic Succession Pivot for Second Generation",
        "description": "Change the game rules rather than keep playing the old game",
        "modes": [33, 8, 23, 6, 12],
        "reason": "Eight Banners reform, Mongol→Manchu, Chongde era name, Six Ministries, Han officials in Manchu posts. Second-gen succession core: change game rules not keep playing old game.",
        "steps": [
            "Step 1: Culture reshape — 'Mongol'→'Manchu', build new collective identity",
            "Step 2: Institutional innovation — Six Ministries, Inner Three Academies, Eight Banners incorporate Han/Mongol armies",
            "Step 3: Talent fusion — Han officials in Manchu posts, imperial exams, surrendered generals reused (Hong Chengchou etc)",
            "Step 4: Strategic pivot — From plunder to governance, cavalry to firearms, nomadism to agriculture",
            "Step 5: Brand rebuild — 'Chongde' era name, 'Great Qing' state name, legitimacy narrative reconstruction"
        ],
        "expected": [
            "Later Jin→Great Qing, from tribal alliance to imperial monarchy",
            "Pre-entry already possessed org/system/cultural capacity to rule China",
            "Foundation for Shunzhi entry, Kang-Qian golden age"
        ],
        "case": "Later Jin to Great Qing: Huang Taiji succeeded facing 'few Jurchens, many Hans, strong Mongols' triple pressure. 'Mongol'→'Manchu' reshape ethnic identity. Six Ministries mimic Ming, Inner Three Academies control policy, Eight Banners incorporate Han/Mongol armies. Imperial exams restored, surrendered generals reused (Hong Chengchou/Kong Youde), firearms battalion established. Chongde year 1 'Great Qing', legitimacy narrative upgraded from 'Mandate' to 'Chongde'. Result: Pre-entry already possessed organizational/systemic/cultural capacity to rule China."
    },
    "H-ZL-08": {
        "name": "Zhuge Liang: Systems Engineer's Systems Thinking",
        "description": "Strategy decomposed to tactics, standardized operating procedures",
        "modes": [1, 12, 14, 29, 7, 28, 8],
        "reason": "Longzhong Plan, Six Northern Expeditions, Wooden Ox/Flowing Horse. Systems engineering: strategy→tactics, standardized procedures, risk prediction with redundancy.",
        "steps": [
            "Step 1: Strategic positioning — Longzhong: Jing/Yi hold→two-prong north→central plains decision",
            "Step 2: Standardized processes — Military pledge, collective responsibility, tuntian system, Wooden Ox/Flowing Horse logistics standards",
            "Step 3: Risk prediction — 'Death before victory', multi-route dispersion, retreat contingencies",
            "Step 4: Resource coordination — 'Strict military discipline', clear rewards/punishments, militia+regular army combination",
            "Step 5: Succession solidification — 'Memorial on Expedition' entrustment, Jiang Wan/Fei Yi inherit, Jiang Wei inherits mantle"
        ],
        "expected": [
            "Weak Shu Han repeatedly threatened strong Cao Wei",
            "Army discipline/logistics/combat standardization ahead of era",
            "Management thought influences modern project management"
        ],
        "case": "Longzhong Plan & Six Expeditions: Liu Bei three visits, Zhuge Liang Longzhong Plan mapped 'Jing/Yi hold→two-prong north→central plains decision'. Established 'military pledge/collective responsibility/tuntian/wooden ox' standardized system. Six expeditions though not unified, repeatedly reached Chang'an vicinity, exhausted Cao Wei. Deathbed entrustment to Jiang Wan/Fei Yi/Jiang Wei, Shu Han regime continued 29 years."
    },
    "H-SY-09": {
        "name": "Sima Yi: Dormant Accumulation - Weak Player's Survival",
        "description": "Don't fight unprepared battles, don't fight unsure battles, don't fight unprofitable battles",
        "modes": [35, 3, 11, 16, 1, 28],
        "reason": "Sima Yi survived Cao Cao, Cao Pi, Cao Rui, Cao Fang four reigns, held ground against Zhuge Liang's expeditions waiting for supply exhaustion/illness; Gaoping Tombs coup seized power. When momentum not ours, dormant wait; when momentum ours, thunder strike.",
        "steps": [
            "Step 1: Honest strength assessment — Gap>5x defense, 2-5x dormant, <2x counterattack",
            "Step 2: Intelligence network — Job postings/financing/product/executive changes all monitored",
            "Step 3: Probe actions — Small experiments validate hypotheses, don't reveal intent",
            "Step 4: Single-point breakthrough — Meet 'I strong/he weak/high value/replicable' four conditions",
            "Step 5: Stop-loss retreat trigger — Prevent gambler's fallacy, 3 consecutive weeks core metric<plan 30%→retreat"
        ],
        "expected": [
            "Weak player survival rate significantly improved",
            "Key battle win rate >70%",
            "Organization preserves core seed in winter"
        ],
        "case": "Countering Zhuge Liang's expeditions: Cao Zhen/Sima Yi rotated defense, Sima Yi 'firm walls clear fields, no engagement'. Collected intelligence, grasped Shu logistics only 100 days, Zhuge Liang ill. Zhuge Liang died, Sima Yi pursued, Jiang Wei retreated, established Wei initiative. Gaoping Tombs: Cao Shuang went outing, Sima Yi closed doors accumulated long, one-strike seizure, established Jin foundation."
    },
    "H-ZG-10": {
        "name": "Zeng Guofan: Compound Diligence Ultimate Form",
        "description": "Slow-witted early bird, diligence compensates clumsiness — time is compounding's strongest lever, 'dumb effort' is compounding's strongest principal",
        "modes": [36, 32, 10, 18, 21, 8, 35],
        "reason": "Mediocre talent, repeatedly failed exams, yet 'sought benevolence got benevolence', Xiang Army system, Self-Strengthening, self-cultivation family governance statecraft. Compounding's strongest lever is time, strongest principal is 'dumb effort'.",
        "steps": [
            "Step 1: Anchor core skill — Pick 1 'moat skill' (10yr valid, hard to replace, high compounding)",
            "Step 2: Daily update system — ≥1hr/day deep practice (no fragments, no entertainment, only hard bones)",
            "Step 3: Review loop — Daily(15min)+Weekly(1h)+Monthly(half day)+Yearly(full day)",
            "Step 4: Dumb effort negative list — No crash courses, no 'instant mastery' books, no speed techniques",
            "Step 5: Inheritance mechanism — Teach others, you truly understand; disciple graduates, you're free"
        ],
        "expected": [
            "Personal brand becomes strongest moat",
            "Family/org century-long inheritance",
            "Time stands on your side"
        ],
        "case": "Zeng Guofan Xiang Army: Didn't recruit bandits, only farmers/scholars; didn't fight quick wins, only built long siege; didn't grab credit, only sought steady. Compounding: Xiang Army became late Qing strongest army; Zeng family century talents; management thought influential today. Contrast: Huai Army/Westernization sought fast/foreign/clever, ultimately failed due to weak foundation."
    },
    "H-WY-11": {
        "name": "Wang Yangming: Unity of Knowledge and Action",
        "description": "True knowledge is action, inaction is non-knowledge — eliminate knowledge-action gap",
        "modes": [37, 27, 21, 5, 30],
        "reason": "Dragon Field enlightenment: 'Way of sages, my nature sufficient, seeking externally was error.' Deng Xiaoping 'black cat white cat, catching mice is good cat' — practice sole truth criterion. Zeng Guofan 'sought benevolence got benevolence', daily diary reflection. Know but don't act, merely don't know.",
        "steps": [
            "Step 1: Cognitive audit — List 'I believe correct but haven't acted' cognitions",
            "Step 2: MVA design — Each cognition maps to 'minimum viable action' (cost<1hr/100yuan)",
            "Step 3: Execution commitment — Public pledge + accountability partner + deadline",
            "Step 4: Review loop — 24hr post-action record 'expected vs actual + deviation cause + cognitive correction'",
            "Step 5: Conscience calibration — Weekly ask 'This thing done right? Conscience at peace?'"
        ],
        "expected": [
            "Knowledge-action gap converges to <10%",
            "Individual/team execution qualitative leap",
            "Build reusable 'unity of knowledge and action' muscle memory"
        ],
        "case": "Wang Yangming pacifying Ning Prince: 'Conscience is military strategy, benevolent is invincible' — no need military books, conscience at moment is best decision. 43 days, few vs many, mind undistracted, conscience at moment is best decision. Deng Xiaoping Southern Tour: 'Black cat white cat, catching mice is good cat' — practice sole truth criterion. Zeng Guofan diary: 'sought benevolence got benevolence', daily reflection on knowledge-action gap."
    },
    "H-SZ-12": {
        "name": "Sun Yat-sen: Three Principles Systemic Framework",
        "description": "Ideology × Party-building × Army-building × Nation-building — complete revolutionary engineering system",
        "modes": [42, 3, 6, 22, 17],
        "reason": "Nationalism/Democracy/Livelihood Three Principles, Party/Army/Nation three great projects. Systemic framework: ideology guides direction, party solves leadership, army solves violence, nation solves governance.",
        "steps": [
            "Step 1: Program first — Three Principles: Nationalism(anti-imperial)/Democracy(anti-feudal)/Livelihood(equal land rights)",
            "Step 2: Party leadership — Tongmenghui/KMT: program/system/discipline/organ",
            "Step 3: Army violence — Whampoa Academy/Northern Expedition/Party commands gun/political military training both",
            "Step 4: Nation governance — Political tutelage/constitutionalism/five-power constitution/local autonomy/national economy",
            "Step 5: Premier's will — 'Revolution not yet succeeded, comrades must still strive', inheritance mechanism"
        ],
        "expected": [
            "Overthrew 2000-year monarchy, established Asia's first republic",
            "Ideology influenced entire East Asian revolutionary movements",
            "Limitation: Idealism lacks execution, over-reliance on external forces"
        ],
        "case": "Xinhai Revolution: Sun Yat-sen overseas fundraising, domestic uprisings, Soviet alliance, Whampoa military, Northern Expedition unification. Three Principles: Nationalism(expel Tartars/restore China)/Democracy(establish republic/equal land rights)/Livelihood(equal land/regulate capital). Party: Tongmenghui→KMT, program/system/discipline/organ. Army: Whampoa/Northern Expedition/Party commands gun/political training both. Nation: Tutelage→Constitutionalism→Five-power constitution/local autonomy/national economy. Result: Overthrew 2000-year monarchy, established Asia's first republic."
    },
    "H-LB-13": {
        "name": "Lin Biao: Concentrated Command and Mobile Warfare",
        "description": "Military genius ≠ political wisdom, lacks strategic self-reflection",
        "modes": [15, 3, 11, 16, 14],
        "reason": "Pingxingguan, Liaoshen Campaign, Lin Biao Military Writings. Concentrated command, mobile warfare, tactical innovation. Military genius ≠ political wisdom, lacks strategic self-reflection.",
        "steps": [
            "Step 1: Concentrate forces — 'Roar with horizontal sword unify combined/large units/regular war', concentrate superior forces",
            "Step 2: Mobile warfare — Avoid enemy main, lure deep, concentrate annihilate, don't cling to cities",
            "Step 3: Tactical innovation — 'One fast two steady three precise fierce', night combat/flanking/encirclement/annihilation",
            "Step 4: Political army building — 'Three-Eight style', officer-soldier equality, political work lifeline",
            "Step 5: Strategic self-reflection absence — Lin Biao incident: military genius walked into political abyss, lacked meta-cognition"
        ],
        "expected": [
            "Military campaign win rate extremely high (Pingxingguan/Liaoshen/Pingjin)",
            "Army building model systematic output (political work/three-eight style)",
            "Lesson: Tactical perfection cannot compensate strategic blindness"
        ],
        "case": "Liaoshen Campaign: Lin Biao commanded Northeast Field Army, 'Jinzhou first, then Changchun, finally Jinzhou'. Jinzhou: 170k troops encircled/annihilated 100k elite, 31 hours battle. Pingjin: Encircled Fu Zuoyi 350k, negotiation/psyops/military pressure three-pronged, peaceful liberation of Beiping. Lin Biao Military Writings: 'Concentrate troops, mobile warfare, quick decision, no city attachment'. But Lin Biao incident: military genius walked into political abyss, lacked strategic self-reflection."
    },
    "H-CY-14": {
        "name": "Chen Yun: Birdcage Economy and Boundary Thinking",
        "description": "Market in plan — freedom maximized within boundaries",
        "modes": [39, 19, 28, 5, 8],
        "reason": "Three magic weapons, economic regulation. Birdcage economy: plan is cage, market is bird, bird flies in cage. Freedom maximized within boundaries. Over-caution limited reform speed.",
        "steps": [
            "Step 1: Set cage — Core indicators/ratios/red lines (grain/cotton/oil/exchange rate/interest rate/credit scale)",
            "Step 2: Fly in cage — Price/output/variety/channel/body market pricing",
            "Step 3: Dynamic adjustment — 'Loosen a bit, tighten a bit', fiscal contracting/tax-for-profit/dual-track",
            "Step 4: Financial discipline — 'Money bag' centralized, audit supervision/violation punished",
            "Step 5: Boundary thinking — 'Market in plan', clear boundaries maximize freedom"
        ],
        "expected": [
            "Economic stable transition, avoid shock therapy side effects",
            "Financial discipline strict, inflation controlled",
            "Limitation: Over-caution limited reform speed, missed optimal window"
        ],
        "case": "Three magic weapons: 1950s fiscal contracting→1980s profit-for-tax→1993 tax-sharing. Dual-track: planned price/market price coexist, dual-track→unification. Regulation: 1988 anti-inflation 'tighten'→1990s soft landing. Financial discipline: Audit Office/national audit/violation punished. Birdcage economy: Plan is cage, market is bird, bird flies in cage — clear boundaries maximize freedom."
    },
    "H-LB-15": {
        "name": "Liu Bei: Hearts & Minds Alignment via Benevolence",
        "description": "Benevolence as foundation, three visits to thatched cottage, entrustment at Baidi",
        "modes": [6, 21, 18, 13, 1],
        "reason": "Teams aren't ready just by hiring. Mass line ensures hearing real voices, united front integrates differences, MBO aligns goals.",
        "steps": [
            "Step 1: Deep understanding — 1-on-1 deep interviews each member, ask: what you excel at? want to do? worry about?",
            "Step 2: Find consensus — Identify core values overlap, find 'greatest common divisor' as team culture cornerstone",
            "Step 3: Set goals — Joint OKRs, not top-down decomposition, challenging but achievable",
            "Step 4: Build mechanisms — Weekly: sync progress/expose issues/mutual help; Retros: victory retro/failure retro/all retro",
            "Step 5: Continuous iteration — Quarterly review: culture healthy? goals aligned? Adjust: people/process/incentives"
        ],
        "expected": [
            "Team cohesion significantly improved",
            "Goal alignment >90%",
            "Per capita output +30%+"
        ],
        "case": "Startup core team expanded from 5 to 20. Mass line: founder 1-on-1 each, found 'tech debt' biggest pain. United front: established 'user value first, tech excellence, radical transparency' three values. MBO: all participate quarterly OKRs, weekly public progress. Result: 6 months delivered 3 core versions, zero major incidents, team satisfaction 4.8/5."
    },
    "H-DX-16": {
        "name": "Deng Xiaoping: Crossing River by Feeling Stones",
        "description": "Three favorables one-veto, SEZ pilot, Southern Tour speeches",
        "modes": [38, 5, 8, 35, 11, 37, 29],
        "reason": "Reform not blueprint but evolution tree. Deng: SEZ first (Shenzhen/Zhuhai/Shantou/Xiamen)→coastal→inland. Chen Yun: 'birdcage economy' — market in plan, freedom in boundaries. Zhu Rongji: SOE 'grasp large release small', finance 'one bank three commissions', housing monetization phased pilots. Reform not blueprint but evolution tree.",
        "steps": [
            "Step 1: Three favorables one-veto — Productivity/national power/living standards? No=direct veto",
            "Step 2: Pilot design — Clear hypothesis, single variable, controllable cost, reversible",
            "Step 3: Red-green light eval — Monthly data review, quarterly field research, semi-annual decision review",
            "Step 4: Rollout rhythm — Seed<10%→Validation<30%→Scale<60%→Full",
            "Step 5: Experience solidification — Success cases→standard toolkits→training systems→platform capabilities"
        ],
        "expected": [
            "Reform stable transition, avoid shock therapy side effects",
            "Experience replicable, scalable, platformable",
            "Lesson: Political reform lagged economic reform"
        ],
        "case": "Shenzhen SEZ: 1979 established Shenzhen/Zhuhai/Shantou/Xiamen SEZs, 'special policies flexible measures'. Shenzhen from fishing village to GDP>HK, foreign investment, processing trade, shareholding reform. 1984 expanded to 14 coastal cities, 1988 Hainan province. 1992 Southern Tour→full rollout, 'basic line 100 years unchanged'. Result: Established market economy, GDP avg 9.5% growth."
    },
    "H-LB-17": {
        "name": "Liu Bei: Team Building via Benevolence",
        "description": "Three visits to cottage, entrustment at Baidi, benevolence as foundation",
        "modes": [6, 21, 18, 13, 1],
        "reason": "Teams aren't ready just by hiring. Mass line ensures hearing real voices, united front integrates differences, MBO aligns goals.",
        "steps": [
            "Step 1: Deep understanding — 1-on-1 deep interviews each member, ask: what you excel at? want to do? worry about?",
            "Step 2: Find consensus — Identify core values overlap, find 'greatest common divisor' as team culture cornerstone",
            "Step 3: Set goals — Joint OKRs, not top-down decomposition, challenging but achievable",
            "Step 4: Build mechanisms — Weekly: sync progress/expose issues/mutual help; Retros: victory retro/failure retro/all retro",
            "Step 5: Continuous iteration — Quarterly review: culture healthy? goals aligned? Adjust: people/process/incentives"
        ],
        "expected": [
            "Team cohesion significantly improved",
            "Goal alignment >90%",
            "Per capita output +30%+"
        ],
        "case": "Liu Bei three visits to Zhuge Liang, Longzhong Plan established 'Jing/Yi hold→two-prong north→central plains decision' grand strategy. Entrustment at Baidi: 'lord-minister utmost sincerity'. Guan Yu Zhang Fei 'enemy of ten thousand' but willing to follow. Peach Garden oath: 'not same birth but wish same death'. Result: Shu Han one of three kingdoms, weak but lasted 43 years, Liu Bei benevolent image eternal."
    }
}

# Add to scenarios_en
scenarios_en.update(new_scenarios_en)

# Save updated scenarios_en.json
with open('scenarios_en.json', 'w', encoding='utf-8') as f:
    json.dump(scenarios_en, f, ensure_ascii=False, indent=2)

print(f"Updated scenarios_en.json: {len(scenarios_en)} total scenarios")