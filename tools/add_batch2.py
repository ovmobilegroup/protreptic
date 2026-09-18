#!/usr/bin/env python3
"""
Add Batch 2 (20 figures) to Protreptic data files
"""
import json

def load_json(path):
    with open(path, 'r') as f:
        return json.load(f)

def save_json(data, path):
    with open(path, 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def main():
    # Load batch2 candidates
    with open('batch2_candidates.json', 'r') as f:
        candidates = json.load(f)
    
    print(f"Loading {len(candidates)} Batch 2 candidates...")
    
    # Load existing data files
    scenarios_zh = load_json('scenarios_zh.json')
    scenarios_en = load_json('scenarios_en.json')
    code_maps = load_json('code_maps.json')
    scenario_tags = load_json('scenario_tags.json')
    
    # English translations for each candidate
    en_data = {
        "H-ZEL-332": {
            "name": "Zhou Enlai: United Front Integration and Diplomatic Icebreaking - Triple-Integration Premier Diplomacy",
            "description": "United Front, Diplomatic Strategy, Government Operations",
            "reason": "Zhou Enlai founded New China's diplomacy. United Front (Mode 10) shown in Bandung Conference and Sino-US icebreaking uniting all unitable forces. Three Disciplines Eight Points (Mode 42) shown in diplomatic discipline, confidentiality, work style. Mass Line (Mode 6) shown in grassroots research, listening to all sides. Strategic Delegation (Mode 33) shown in talent identification, strategy setting, reward sharing, safety nets.",
            "steps": [
                "Step 1: Analyze international balance of power - identify principal and secondary contradictions",
                "Step 2: Seek greatest common divisor - unite all unitable forces (United Front)",
                "Step 3: Establish strict discipline system - diplomatic confidentiality, work style, procedure (Three Disciplines)",
                "Step 4: Identify talent, set strategy, share rewards, provide safety nets - diplomatic talent configuration: strategists, executors, coordinators complementary",
                "Step 5: Flexible maneuvering strategy - struggle for unity within unity, unity within struggle",
                "Step 6: Establish long-term working mechanisms - diplomatic archives, archive management, experience inheritance"
            ],
            "expected": [
                "Seize strategic initiative in complex international environment",
                "Build credible, controllable, efficient diplomatic work system",
                "Core secrets zero leakage, bottom lines zero breach"
            ],
            "case": "1971-1972 Sino-US icebreaking: Zhou Enlai led Kissinger's secret visit, Nixon visit, Shanghai Communique. United Front: unite Third World, attract US pragmatists, isolate Soviet hardliners. Strict discipline: diplomatic staff absolute confidentiality, Kissinger visit known to only 5 people beforehand. Modern applications: cross-border negotiations, alliance building, crisis PR, government relations management."
        },
        "H-LSQ-333": {
            "name": "Liu Shaoqi: Party Building Organizational Line Engineering and On the Cultivation of Communist Party Members",
            "description": "Party Building, Organizational Management, Discipline",
            "reason": "Liu Shaoqi engineered the Party's organizational line. In 'On the Cultivation of Communist Party Members', he quantified party member standards, development procedures, organizational life systems. United Front (Mode 10) in party united front work. Three Disciplines Eight Points (Mode 42) in party discipline. Mass Line (Mode 6) in connecting with masses. Criticism & Self-Criticism (Mode 2) as core cultivation method.",
            "steps": [
                "Step 1: Define party member standards - quantify party member development procedures, probation periods, obligations and rights",
                "Step 2: Establish organizational line - democratic centralism, criticism and self-criticism, organizational life system",
                "Step 3: Party intra-law system - Party Constitution, Guidelines, Regulations, Rules four-level regulatory system",
                "Step 4: Discipline execution tiered - violations tiered handling, appeal review, rights protection",
                "Step 5: Development procedures standardized - recommendation for party membership, acceptance of probationary members, regularization assessment full process",
                "Step 6: Party member standards quantified - qualified party member standards concrete, measurable, assessable"
            ],
            "expected": [
                "Build standardized party organizational system",
                "Form party intra-law system",
                "Establish qualified party member assessment standards"
            ],
            "case": "'On the Cultivation of Communist Party Members' quantified party member standards. Democratic centralism, criticism/self-criticism, organizational life system. Modern applications: organizational building, party intra-law, cadre management, discipline building."
        },
        "H-PDH-334": {
            "name": "Peng Dehuai: Army Discipline / Three Disciplines Eight Points Practitioner and Hundred Regiments Offensive Command Art",
            "description": "Military Discipline, Mass Line Military, Asymmetric Warfare",
            "reason": "Peng Dehuai practiced Three Disciplines Eight Points (Mode 42) as absolute army discipline. Mass Line Military (Mode 10) in Hundred Regiments Offensive: officer-soldier unity, military-civilian unity, disintegrate enemy. Strategic Foresight (Mode 1) in not fighting unprepared battles. Contradiction Analysis (Mode 7) in concentrating forces for annihilation warfare.",
            "steps": [
                "Step 1: Establish absolute discipline - Three Disciplines Eight Points implemented to every soldier",
                "Step 2: Mass line militarized - officer-soldier unity, military-civilian unity, disintegrate enemy forces",
                "Step 3: Lie in wait and accumulate power - no battle without preparation, no battle without assurance, no battle without gain",
                "Step 4: Single-point breakthrough - concentrate superior forces, mobile annihilation, win with less",
                "Step 5: Stop-loss retreat - preserve strength in strategic transfer, no greedy merit or rash advance",
                "Step 6: Experience inheritance - 'Peng Dehuai Military Writings' compilation, military thought inheritance"
            ],
            "expected": [
                "Build highly disciplined people's army",
                "Form mobile annihilation warfare theory",
                "Establish mass line military practice"
            ],
            "case": "Hundred Regiments Offensive: Peng commanded 105 regiments attacking Japanese transportation lines. Mass line: mobilize masses, coordinate local forces. Discipline: Three Disciplines Eight Points as behavioral baseline. Modern applications: army building, discipline building, asymmetric warfare, crisis management."
        },
        "H-LRH-335": {
            "name": "Luo Ronghuan: Political Work / Army Building / Three Disciplines Eight Points Institutionalization Builder",
            "description": "Political Work, Army Building, Discipline System",
            "reason": "Luo Ronghuan built the political work system: political commissar system, political departments, party committee system. Three Disciplines Eight Points (Mode 42) institutionalized: discipline into regulations, assessment normalized. United Front (Mode 10) applied in army: unite all unitable forces. Strategic Delegation (Mode 33) in talent identification, strategy setting, reward sharing, safety nets. Army regularization: military ranks, conscription, training outlines.",
            "steps": [
                "Step 1: Establish political work system - political commissar system, political departments, party committee system",
                "Step 2: Three Disciplines Eight Points institutionalized - discipline regulation, assessment normalized",
                "Step 3: United Front in army application - unite all unitable forces",
                "Step 4: Strategic delegation - identify talent, set strategy, share rewards, provide safety nets, build army cadre echelons",
                "Step 5: Army regularization construction - military rank system, conscription system, military training outlines",
                "Step 6: Army building experience inheritance - 'Luo Ronghuan Military Political Works' compilation"
            ],
            "expected": [
                "Establish complete political work system",
                "Three Disciplines Eight Points become institutionalized norms",
                "Army regularization construction foundation"
            ],
            "case": "Political commissar system, political departments, party committee system established. Three Disciplines Eight Points into regulations. Modern applications: army building, political work, discipline building, organizational management."
        },
        "H-YDZ-336": {
            "name": "Yang Dezhi: Troop Rectification / Discipline Construction / Three Disciplines Eight Points Practice Promoter",
            "description": "Troop Rectification, Discipline Construction, Mobile Warfare",
            "reason": "Yang Dezhi enforced Three Disciplines Eight Points (Mode 42) at company and platoon levels. Mobile Annihilation (Mode 16): concentrate superior forces, piecemeal annihilation, mobile warfare. Contradiction Analysis (Mode 1): identify principal contradiction, concentrate forces to solve key problems. United Front (Mode 9): unite all unitable forces, isolate enemy. Troop rectification: rectification and reorganization, ideological education, style rectification.",
            "steps": [
                "Step 1: Strict discipline - Three Disciplines Eight Points implemented to companies and platoons",
                "Step 2: Mobile annihilation method - concentrate superior forces, annihilate piece by piece, mobile warfare",
                "Step 3: Contradiction analysis - identify principal contradiction, concentrate forces to solve key problems",
                "Step 4: United front - unite all unitable forces, isolate enemy",
                "Step 5: Troop rectification - ideological education, style rectification, organizational consolidation",
                "Step 6: Experience inheritance - 'Yang Dezhi Memoirs' compilation, military thought inheritance"
            ],
            "expected": [
                "Build highly disciplined combat troops",
                "Form mobile annihilation warfare practice",
                "Establish troop rectification methodology"
            ],
            "case": "Yang Dezhi's troop rectification emphasized Three Disciplines Eight Points at grassroots. Mobile annihilation warfare: concentrate superior forces, annihilate enemy piece by piece. Modern applications: army building, discipline construction, combat command, troop management."
        },
        "H-QXS-337": {
            "name": "Qian Xuesen: Father of Systems Engineering's Three Decades Forging Rocketry",
            "description": "Systems Engineering, Aerospace, Long-termism",
            "reason": "Qian Xuesen founded Chinese Systems Engineering, led 'Two Bombs One Satellite'. Compound Diligence (Mode 36): three decades incognito, building aerospace from zero. Seek Truth from Facts (Mode 7): everything from reality, rejecting Soviet model blind following. Mental Models (Mode 17): cross-disciplinary fusion of mechanics, cybernetics, systems theory. Systems Thinking (Mode 12): aerospace engineering as holistic large-system design.",
            "steps": [
                "Step 1: Anchor core skills - mechanics + cybernetics + systems theory, build cross-disciplinary knowledge system",
                "Step 2: Daily update discipline - daily reading, note-taking, engineering thinking, persisted for decades",
                "Step 3: Review loop - each engineering phase summary, forming 'Systems Engineering' textbook",
                "Step 4: Negative list - reject exaggeration, reject unrealistic metrics, reject politics-over-technology",
                "Step 5: Inheritance mechanism - build aerospace talent pipeline: Qian Xuesen -> Tu Shou'e -> new gen chief designer system",
                "Step 6: Systems integration - integrate subsystems (missiles, satellites, tracking, launch) into macro-system"
            ],
            "expected": [
                "Build China's autonomous aerospace engineering system",
                "Form Systems Engineering discipline and talent pipeline",
                "Achieve leap from zero to world-advanced level"
            ],
            "case": "'Two Bombs One Satellite' project: Qian submitted 'Suggestions on Establishing China's Defense Aviation Industry' in 1956, created Fifth Academy system. Systems Engineering: missiles, satellites, launch vehicles, tracking, launch sites as five major integrated systems. Compound Diligence: from 1956 DF-1 failure to 1970 Dong Fang Hong I launch, 14 years breakthrough. Modern applications: large-scale complex engineering, cross-disciplinary R&D, autonomous controllable tech systems."
        },
        "H-DJX-338": {
            "name": "Deng Jiaxian: Two Bombs One Satellite / Hidden Name / Tempered Steel",
            "description": "Nuclear Physics, National Defense Technology, Long-termism",
            "reason": "Deng Jiaxian incognito for 28 years leading nuclear weapons theory. Compound Diligence (Mode 36): decades of nuclear physics breakthrough. United Front (Mode 9): coordinating physics, chemistry, metallurgy, mechanics, electronics multi-disciplinary collaboration. Systems Thinking (Mode 12): nuclear weapons as large system theory design, engineering realization, test verification. Holistic Thinking (Mode 22): integrating nuclear undertaking into national strategic whole.",
            "steps": [
                "Step 1: Accept national strategic mission - incognito, farewell family, enter Northwest",
                "Step 2: Build multi-disciplinary attack system - physics, chemistry, metallurgy, mechanics, electronics coordination",
                "Step 3: Conquer core theoretical problems - explosion mechanics, radiation hydrodynamics, equation of state",
                "Step 4: Organize thousands of underground nuclear tests - from atmospheric to underground, atomic to hydrogen bomb",
                "Step 5: Establish quality assurance system - zero-defect management, full-process traceability",
                "Step 6: Cultivate nuclear successors - build echelons, inherit core technology"
            ],
            "expected": [
                "Achieve atomic/hydrogen bomb breakthrough in extremely short time",
                "Build complete nuclear weapon R&D system and talent echelons",
                "Provide nuclear shield for national strategic security"
            ],
            "case": "1958 Deng Jiaxian appointed Institute 9 Director, began nuclear weapons theory. 1964 Oct 16 first atomic bomb success, 1967 Jun 17 first hydrogen bomb success. Zero to H-bomb in only 32 months (US/USSR took 7/4 years respectively). Compound Diligence: decades incognito, hand-calculated formulas, ran simulations. Modern applications: core tech breakthrough, cross-disciplinary collaboration, autonomous strategic projects."
        },
        "H-HLG-339": {
            "name": "Hua Luogeng: Mathematical Self-Taught Talent and Optimal Selection/Multi-Objective Planning/Math Popularization Education",
            "description": "Mathematics, Optimization Theory, Math Education",
            "reason": "Hua Luogeng self-taught in mathematics, pioneered optimal selection method and multi-objective planning. Compound Diligence (Mode 36): lifelong daily practice of mathematical thinking. Mental Models (Mode 17): mathematics + operations research + systems engineering cross-disciplinary fusion. Gradual Reform (Mode 8): math popularization from elite to masses. Abstract Induction (Mode 25): extracting optimization theory from concrete production problems.",
            "steps": [
                "Step 1: Anchor core skills - number theory + optimization theory + applied mathematics, build cross-disciplinary knowledge system",
                "Step 2: Daily update discipline - daily formula derivation, problem analysis, note-taking, persisted for life",
                "Step 3: Review loop - each research topic summary, forming optimal selection method, multi-objective planning theory",
                "Step 4: Negative list - reject pure theory without application, reject research detached from reality, reject formalism",
                "Step 5: Inheritance mechanism - Hua Luogeng Math Class, Youth Class, math popularization education system",
                "Step 6: Cross-domain fusion - math + operations research + systems engineering + agricultural meteorology + industrial optimization"
            ],
            "expected": [
                "Establish China's optimization theory and operations research",
                "Form math popularization education system",
                "Achieve math + industry/agriculture/national defense cross-domain application"
            ],
            "case": "Hua Luogeng optimal selection method applied to production scheduling, resource allocation. Multi-objective planning theory. Math class, youth class, math popularization. Modern applications: mathematical research, optimization theory, operations research, math education popularization."
        },
        "H-ZKZ-340": {
            "name": "Zhu Kezhen: Meteorology Foundation / Phenological Observation / Statistical Laws / Physical Mechanisms / Dual-Network Fusion Observation System",
            "description": "Meteorology, Phenology, Observation Systems, Science Education",
            "reason": "Zhu Kezhen founded Chinese meteorology. Compound Diligence (Mode 36): decades of phenological observation. Seek Truth from Facts (Mode 7): observation data as basis, statistical laws + physical mechanisms dual verification. Crossing River by Feeling Stones (Mode 38): from single station to national network, from manual to automated. Systems Thinking (Mode 12): conventional observation network + special observation network, ground-based + space-based fusion.",
            "steps": [
                "Step 1: Establish observation network - national meteorological station layout, standardized observation norms",
                "Step 2: Phenological observation - phenophases, crop growth stages, natural phenomena long-term recording",
                "Step 3: Statistical law analysis - climate variability, periodicity, trends, extreme value analysis",
                "Step 4: Physical mechanism research - atmospheric circulation, radiation balance, water vapor transport, thermodynamic processes",
                "Step 5: Dual-network fusion observation system - conventional observation net + special observation net, ground-based + space-based fusion",
                "Step 6: Science education / talent cultivation - Zhejiang Univ president 13 years, Seeking Truth motto, general + professional + character trinity"
            ],
            "expected": [
                "Establish China's modern meteorological observation system",
                "Found phenology and climate change research",
                "Build science education talent cultivation system"
            ],
            "case": "Zhu Kezhen founded Chinese meteorology. Phenological observation network, climate change research. Zhejiang Univ president: 'Seeking Truth' motto. Modern applications: meteorology, climate change research, agricultural meteorology, science education management."
        },
        "H-YYY-341": {
            "name": "Tu Youyou: Artemisinin Discovery / Chinese-Western Medicine Integration / Triple Cross-Verification / Traditional Medicine Modernization",
            "description": "Pharmacology, Traditional Medicine Modernization, Drug Development",
            "reason": "Tu Youyou discovered artemisinin. Compound Diligence (Mode 36): decades of persistent research. United Front (Mode 9): coordinating phytochemistry, pharmacology, clinical medicine multi-disciplinary collaboration. Engineering Standardization (Mode 23): extraction process, quality standards, clinical norms, technology package standardization. Seek Truth from Facts (Mode 7): theory from experimental data, rejecting dogmatism.",
            "steps": [
                "Step 1: Literature research - consulted ancient texts 'Handbook of Prescriptions for Emergencies' etc., 380 prescriptions, 2000+ single remedies",
                "Step 2: Chemical separation - isolate and purify active ingredients from artemisia annua, structure determination",
                "Step 3: Efficacy verification - in vitro/in vivo experiments, toxicity testing, clinical observation",
                "Step 4: Triple cross-verification - chemical structure, pharmacological activity, clinical efficacy triple confirmation",
                "Step 5: Traditional medicine modernization - traditional knowledge + modern scientific methods, standardized production",
                "Step 6: Technology package standardization - extraction process, quality standards, clinical norms, promotion application"
            ],
            "expected": [
                "Achieve artemisinin breakthrough saving millions of lives globally",
                "Establish traditional medicine modernization methodology",
                "Win Nobel Prize in Physiology or Medicine"
            ],
            "case": "Tu Youyou consulted 380 ancient prescriptions, isolated artemisinin from artemisia annua. Triple verification: chemical structure, pharmacological activity, clinical efficacy. Nobel Prize 2015. Modern applications: drug development, Chinese-Western medicine integration, traditional medicine modernization, global health."
        },
        "H-BYB-342": {
            "name": "Bo Yibo: Economic System Reform / Crossing River by Feeling Stones / Gradual Reform Pilot-First",
            "description": "Economic Reform, Gradualism, Pilot-First Approach",
            "reason": "Bo Yibo as vice premier supported rural reform pilots. Gradual Reform (Mode 8): small steps, pilot-first. Crossing River by Feeling Stones (Mode 38): Three Favorables one-veto, SEZ pilots. Birdcage Economy/Boundary Thinking (Mode 39): loosening farmers' bonds (loosening birdcage) while holding planned economy bottom line (not breaking public ownership). Seek Truth from Facts (Mode 7): from reality, not books or superiors.",
            "steps": [
                "Step 1: Find entry point - farmers' pain point is hunger, production team contract to household",
                "Step 2: Small-scale pilots - Anhui Fengyang, Sichuan Guanghan, no nationwide rollout",
                "Step 3: Red-green light evaluation - Three Favorables (productive forces, national power, people's livelihood) as criteria",
                "Step 4: Experience solidification - summarize pilot experience, form replicable policy documents",
                "Step 5: Gradual rollout - from Anhui/Sichuan nationwide, each step not exceeding 50% of existing scale",
                "Step 6: Institutionalization - write into law, include in Central No.1 Document, establish long-term mechanism"
            ],
            "expected": [
                "Dramatic increase in farmer per capita income",
                "Consecutive years of grain output growth",
                "Form replicable reform methodology"
            ],
            "case": "1978-1982 Anhui Xiaogang Village, Sichuan Guanghan pilot household contract responsibility. Bo Yibo supported: 'Farmers need to eat, policy must allow.' Three Favorables evaluation passed. 1982 Central No.1 Document affirmed household contract legality. 1984 nationwide rollout. Modern applications: reform pilot design, policy red-green light evaluation, gradual innovation management."
        },
        "H-WL-343": {
            "name": "Wan Li: Rural Reform Pilot 'Crossing River by Feeling Stones' and Household Responsibility System",
            "description": "Rural Reform, Economic System, Pilot-First Approach",
            "reason": "Wan Li as Anhui Party Secretary boldly supported Fengyang, Chuxian farmers' 'household contract responsibility'. Gradual Reform (Mode 8): small steps, pilot-first. Crossing River by Feeling Stones (Mode 38): Three Favorables one-veto, SEZ pilot. Birdcage Economy/Boundary Thinking (Mode 39): loosening farmers' bonds (loosening birdcage) while holding planned economy bottom line (not breaking public ownership).",
            "steps": [
                "Step 1: Find entry point - farmers' pain point is hunger, production team contract to household",
                "Step 2: Small-scale pilots - Anhui Fengyang, Sichuan Guanghan, no nationwide rollout",
                "Step 3: Red-green light evaluation - Three Favorables (productive forces, national power, people's livelihood) as criteria",
                "Step 4: Experience solidification - summarize pilot experience, form replicable policy documents",
                "Step 5: Gradual rollout - from Anhui/Sichuan nationwide, each step not exceeding 50% of existing scale",
                "Step 6: Institutionalization - write into law, include in Central No.1 Document, establish long-term mechanism"
            ],
            "expected": [
                "Dramatic increase in farmer per capita income",
                "Consecutive years of grain output growth",
                "Form replicable reform methodology"
            ],
            "case": "1978-1982 Anhui Xiaogang Village, Sichuan Guanghan pilot household contract responsibility. Wan Li supported: 'Farmers need to eat, policy must allow.' Three Favorables evaluation passed. 1982 Central No.1 Document affirmed household contract legality. 1984 nationwide rollout. Modern applications: reform pilot design, policy red-green light evaluation, gradual innovation management."
        },
        "H-TJY-344": {
            "name": "Tian Jiyun: Fiscal System Reform / Contract Responsibility System / Fiscal Contracting Responsibility",
            "description": "Fiscal Reform, Contract System, Fiscal Responsibility",
            "reason": "Tian Jiyun promoted fiscal contracting responsibility system. Gradual Reform (Mode 8): pilot-first. Crossing River by Feeling Stones (Mode 38): Three Favorables evaluation. Seek Truth from Facts (Mode 5): revenue increase and expenditure reduction, incentive mechanisms, local enthusiasm. Procedural Justice (Mode 32): fiscal contracting written into law, hierarchical fiscal system established.",
            "steps": [
                "Step 1: Fiscal contracting pilots - Shandong, Jiangsu etc. fiscal contracting to household",
                "Step 2: Red-green light evaluation - revenue increase expenditure reduction, incentive mechanisms, local enthusiasm",
                "Step 3: Experience solidification - summarize contracting experience, form fiscal system reform documents",
                "Step 4: Gradual rollout - from pilot provinces nationwide",
                "Step 5: Institutionalization - fiscal contracting written into law, establish hierarchical fiscal system",
                "Step 6: Dynamic adjustment - adjust sharing ratios, expenditure responsibilities based on economic development"
            ],
            "expected": [
                "Mobilize local fiscal enthusiasm",
                "Establish hierarchical fiscal system",
                "Form gradual fiscal reform methodology"
            ],
            "case": "Fiscal contracting pilots in Shandong, Jiangsu etc. Three Favorables evaluation of contracting effects. Fiscal contracting written into law, hierarchical fiscal system established. Modern applications: fiscal system reform, hierarchical fiscal system, gradual reform."
        },
        "H-AZJ-345": {
            "name": "An Zijie: Opening Up / SEZ Construction / Crossing River by Feeling Stones",
            "description": "Opening Up, SEZ Construction, Gradual Reform",
            "reason": "An Zijie participated in Shenzhen SEZ construction. Gradual Reform (Mode 8): pilot-first. Crossing River by Feeling Stones (Mode 38): Three Favorables evaluation of SEZ effects. Birdcage Economy/Boundary Thinking (Mode 39): export-oriented, attract foreign investment, technology import. United Front (Mode 10): unite overseas Chinese, Hong Kong/Macau compatriots, foreign investors.",
            "steps": [
                "Step 1: Find entry point - export foreign exchange, attract foreign investment, technology import",
                "Step 2: Small-scale pilots - Shenzhen, Zhuhai, Shantou, Xiamen four SEZs",
                "Step 3: Red-green light evaluation - Three Favorables evaluate SEZ effectiveness",
                "Step 4: Experience solidification - summarize SEZ experience, form replicable policies",
                "Step 5: Gradual expansion - coastal open cities, Yangtze Delta, Pearl River Delta, Min Delta",
                "Step 6: Institutionalization - SEZ legislative power, foreign investment laws, customs supervision system"
            ],
            "expected": [
                "Build China's first generation SEZs",
                "Attract foreign investment and technology",
                "Form opening up gradual methodology"
            ],
            "case": "Shenzhen, Zhuhai, Shantou, Xiamen four SEZs. Three Favorables evaluation passed. Coastal open cities, Yangtze Delta, Pearl River Delta, Min Delta expansion. Modern applications: SEZ construction, opening up policy, gradual reform."
        },
        "H-CY-346": {
            "name": "Chen Yun: Birdcage Economy / Market in Plan / Financial Discipline Iron Abacus",
            "description": "Economic System Design, Plan and Market, Financial Discipline",
            "reason": "Chen Yun proposed 'Birdcage Economy': market is bird, plan is cage, bird flies in cage. Birdcage Economy/Boundary Thinking (Mode 39): precisely defines market-plan boundary. Seek Truth from Facts (Mode 5): 'not from books, not from superiors, only from reality', opposing Great Leap Forward exaggeration. Procedural Justice (Mode 32): financial discipline, audit supervision, procedural compliance.",
            "steps": [
                "Step 1: Set cage boundaries - define mandatory planned indicators (grain/cotton/oil, construction scale, credit scale)",
                "Step 2: Fly bird in cage - guidance indicators (light industry, commerce, services) market-regulated",
                "Step 3: Dynamic adjustment - adjust cage size and mesh density based on economic operations",
                "Step 4: Financial discipline - audit supervision, budget constraints, violations punished",
                "Step 5: Boundary thinking - neither full planning nor complete liberalization",
                "Step 6: Experience solidification - form inheritable macro-control methodology"
            ],
            "expected": [
                "Avoid both planning rigidity and market失控",
                "Establish hard constraint of financial discipline",
                "Form China-characteristic macro-control methodology"
            ],
            "case": "1950s Chen Yun chaired economic work: 'Market in plan'. 1956 'On Grain Purchase Issues' proposed birdcage metaphor. 1979 chaired financial work: 'Birdcage should be appropriately larger'. Modern applications: macro-prudential management, regulatory sandboxes, financial opening pace, SOE reform boundaries."
        },
        "H-LXN-347": {
            "name": "Li Xiannian: Financial Discipline / Macro Control / Iron Abacus / Price Stability",
            "description": "Financial Discipline, Macro Control, Price Management",
            "reason": "Li Xiannian chaired financial work emphasizing financial discipline. Birdcage Economy/Boundary Thinking (Mode 39): macro control three treasures - currency, fiscal, credit policies coordinated. Seek Truth from Facts (Mode 5): prevent overheating and inflation, timely tighten credit, compress construction scale. Procedural Justice (Mode 32): price stability - overall price level stability, important commodity price control. Target Management (Mode 40): establish economic monitoring early warning - regular analysis of price, credit, forex indicators.",
            "steps": [
                "Step 1: Financial discipline - audit supervision, budget constraints, violations punished",
                "Step 2: Macro control three treasures - currency, fiscal, credit policies coordinated",
                "Step 3: Prevent overheating and inflation - timely tighten credit, compress construction scale",
                "Step 4: Establish economic monitoring early warning - regular analysis of price, credit, forex indicators",
                "Step 5: Price stability - overall price level stable, important commodity price control",
                "Step 6: Experience solidification - form inheritable financial management methodology"
            ],
            "expected": [
                "Build macro control policy coordination mechanism",
                "Establish hard constraint of financial discipline",
                "Form China-characteristic price management methodology"
            ],
            "case": "Li Xiannian 'iron abacus' financial management. Macro control three treasures: currency, fiscal, credit. Price stability as core goal. Modern applications: macro control, financial discipline, price management, risk prevention financial policy."
        },
        "H-QGH-348": {
            "name": "Qiao Guanhua: Diplomacy / UN / UN Seat Restoration / Diplomatic Rhetoric / Language Genius",
            "description": "Diplomacy, UN Affairs, Diplomatic Rhetoric",
            "reason": "Qiao Guanhua led UN seat restoration. Relay Station/Information Velocity (Mode 41): establish diplomatic intelligence network, intelligence collection channels. United Front (Mode 10): unite Third World countries, break isolation. Mass Line (Mode 6): grassroots diplomatic research, listen to all sides. Seek Truth from Facts (Mode 7): diplomatic rhetoric based on facts, not empty talk.",
            "steps": [
                "Step 1: Relay station coverage - establish diplomatic intelligence network, intelligence collection channels",
                "Step 2: Caravan intelligence - use diplomatic channels to collect international situation, countries' positions intelligence",
                "Step 3: Scout network - dispatch experts, scholars, journalists multi-point breakthrough",
                "Step 4: Travel 400 li per day - optimize information transmission process, shorten decision reaction time",
                "Step 5: Intelligence feedback - diplomatic intelligence guides negotiation strategy, diplomatic rhetoric, international statements",
                "Step 6: Experience inheritance - 'Qiao Guanhua Memoirs', diplomatic rhetoric collection, diplomatic thought inheritance"
            ],
            "expected": [
                "Restore China's lawful seat in UN",
                "Build diplomatic intelligence work system",
                "Form distinctive diplomatic rhetoric style"
            ],
            "case": "1971 UN General Assembly Resolution 2758 restored China's seat. Qiao's rhetoric: 'This is a victory for the peoples of the world.' Modern applications: diplomatic strategy, intelligence work, UN diplomacy, multilateral negotiation."
        },
        "H-SQL-349": {
            "name": "Soong Ching-ling: Three Disciplines Eight Points Practitioner of Internationalism",
            "description": "International Humanitarianism, Women's Movement, Discipline Building",
            "reason": "Soong Ching-ling lived by Three Disciplines Eight Points (Mode 42): mass line, self-reliance, criticism/self-criticism. United Front (Mode 10): unite all patriotic forces, international anti-fascist united front. Criticism & Self-Criticism (Mode 2): dare to say no to errors, lifelong adherence to truth. Mass Line (Mode 6): grassroots women/children work, founding welfare institutions.",
            "steps": [
                "Step 1: Define core interests - women/children rights, national independence, world peace",
                "Step 2: Identify allies and opponents - distinguish revolutionary/reformist/reactionary, unite middle forces",
                "Step 3: Establish independent supervision - Women's Federation autonomy, financial transparency, democratic evaluation",
                "Step 4: Build feedback communication channels - deep into grassroots women, hear real demands",
                "Step 5: Establish co-governance norms - democratic centralism, minority obeys majority, individual obeys organization",
                "Step 6: Continuous execution evaluation - regular women's congress, performance evaluation, rectification implementation"
            ],
            "expected": [
                "Become lifelong practitioner of Three Disciplines Eight Points",
                "Promote international understanding and support for Chinese revolution",
                "Lay foundation for women/children welfare undertakings"
            ],
            "case": "Soong Ching-ling founded China Welfare Institute: nurseries, kindergartens, hospitals, publications. Wartime organized international aid to China, protected children. Post-1949 served as Vice Chairperson, Honorary Chairperson. Modern applications: NGO governance, international humanitarianism, women's rights legislation, discipline benchmark."
        },
        "H-DYC-350": {
            "name": "Deng Yingchao: Women's Movement / Political Diplomacy / Party Democracy / Zhou Enlai Partner / Women's Political Awakening",
            "description": "Women's Movement, Political Diplomacy, Party Democracy",
            "reason": "Deng Yingchao promoted women's liberation: marriage autonomy, labor equality, education rights, political participation. United Front (Mode 10): accompanied Zhou Enlai diplomatic activities, international women's organizations. Three Disciplines Eight Points (Mode 42) in family, work practice. Criticism & Self-Criticism (Mode 2): democratic life meetings, rectification campaigns. Family tradition inheritance: Zhou Enlai Deng Yingchao family tradition - integrity, frugality, strict self-discipline.",
            "steps": [
                "Step 1: Women's liberation - marriage autonomy, labor equality, education rights, political participation",
                "Step 2: Political diplomacy - accompany Zhou Enlai diplomatic activities, international women's organizations activities",
                "Step 3: Party democracy - criticism and self-criticism, democratic life meetings, rectification campaigns",
                "Step 4: Discipline building - Three Disciplines Eight Points in family, work practice",
                "Step 5: Family tradition inheritance - Zhou Enlai Deng Yingchao family tradition: integrity, frugality, strict self-discipline",
                "Step 6: Women's political awakening - women's political participation, legislative rights protection, international women's movement"
            ],
            "expected": [
                "Promote women's rights legislation",
                "Participate in international women's movement",
                "Establish integrity family tradition benchmark"
            ],
            "case": "Deng Yingchao promoted Marriage Law, women's political participation. Accompanied Zhou Enlai diplomatic visits. Democratic life meetings, criticism/self-criticism. Modern applications: women's rights, political diplomacy, discipline building, family tradition inheritance."
        },
        "H-FXT-351": {
            "name": "Fei Xiaotong: Differential Mode / Unity in Diversity / From the Soil / Seek Truth from Facts",
            "description": "Sociological Theory, Ethnology, Empirical Research",
            "reason": "Fei Xiaotong's 'From the Soil', 'Peasant Life in China' based on fieldwork. Mental Models (Mode 17): anthropology+sociology+economics+history cross-disciplinary. Criticism & Self-Criticism (Mode 2): post-Cultural Revolution re-evaluation of early views, public correction. Abstract Induction (Mode 25): extracting 'differential mode', 'unity in diversity' core concepts from concrete villages. Seek Truth from Facts (Mode 7): theory from field data, rejecting dogmatism.",
            "steps": [
                "Step 1: Deep into field frontline - long-term village residence, participant observation, language learning",
                "Step 2: Collect raw ethnographic data - kinship, economy, politics, religion, customs",
                "Step 3: Abstract inductive core concepts - differential mode, from kinship to locality, unity in diversity",
                "Step 4: Cross-disciplinary theory integration - anthropology+sociology+economics+history",
                "Step 5: Dare self-criticism correction - post-Cultural Revolution re-evaluate early research limits",
                "Step 6: Build China's own sociology - theory linked to practice, serve national construction"
            ],
            "expected": [
                "Build China-localized sociological theory system",
                "Propose differential mode, unity in diversity core concepts",
                "Provide theoretical support for ethnic policy, urbanization, rural revitalization"
            ],
            "case": "'Peasant Life in China', 'From the Soil' based on 1930s Kaixiangong village fieldwork. Fei noted Chinese society is 'differential mode' not Western 'group format'. Later proposed 'unity in diversity' Chinese nation pattern theory, guiding ethnic identification and regional autonomy. Modern applications: rural revitalization planning, ethnic region development, social impact assessment, public policy fieldwork."
        }
    }
    
    # Add each candidate
    for c in candidates:
        code = c['code']
        
        # Chinese version
        desc_zh = c.get('unique_thinking', '')
        reason_zh = f"{c['name_zh']}的核心思维贡献：{c.get('unique_thinking', '')}。结合相关思维模式框架，分析其在相关领域的卓越贡献和思想方法。"
        steps_zh = c.get('proposed_steps', [])
        expected_zh = c.get('applications', [])
        case_zh = f"{c['name_zh']}的核心实践：{'；'.join(c.get('applications', []))}"
        era = c.get('era', 'Modern')
        
        scenarios_zh[code] = {
            "name": f"{c['name_zh']}：{c.get('unique_thinking', '')}",
            "description": desc_zh,
            "modes": c['core_modes'],
            "reason": reason_zh,
            "steps": steps_zh,
            "expected": expected_zh,
            "case": case_zh,
            "era": era
        }
        
        # English version - use pre-translated data
        en = en_data.get(code, {})
        if en:
            scenarios_en[code] = {
                "name": en['name'],
                "description": en['description'],
                "modes": c['core_modes'],
                "reason": en['reason'],
                "steps": en['steps'],
                "expected": en['expected'],
                "case": en['case'],
                "era": era
            }
        else:
            # Fallback
            scenarios_en[code] = {
                "name": f"{c['name_en']}: {c.get('unique_thinking', '')}",
                "description": c.get('unique_thinking', ''),
                "modes": c['core_modes'],
                "reason": f"{c['name_en']}'s core thinking contribution: {c.get('unique_thinking', '')}. Combined with relevant thinking mode framework, analyzing their outstanding contributions and thinking methods in related fields.",
                "steps": [s.replace('第', 'Step ').replace('步：', ': ') for s in steps_zh],
                "expected": [e.replace('跨国', 'Cross-border').replace('联盟', 'Alliance').replace('危机', 'Crisis').replace('政府', 'Government').replace('军队', 'Military').replace('纪律', 'Discipline').replace('建设', 'Building').replace('管理', 'Management').replace('外交', 'Diplomacy').replace('谈判', 'Negotiation') for e in expected_zh],
                "case": f"{c['name_en']}'s core practice: {'; '.join(expected_zh)}",
                "era": era
            }
        
        # code_maps
        code_maps['CODE_MAP'][code] = c['name_zh']
        code_maps['CODE_MAP_EN'][code] = c['name_en']
        
        # scenario_tags
        scenario_tags['tags'][code] = {
            "code": code,
            "name_zh": c['name_zh'],
            "name_en": c['name_en'],
            "era": c['era'],
            "historical_domains": c['historical_domains'],
            "domains": c['domains'],
            "core_modes": c['core_modes'],
            "gender": c['gender'],
            "ethnicity": c['ethnicity']
        }
        
        print(f"  Added {code}: {c['name_zh']}")
    
    # Update metadata in scenario_tags
    scenario_tags['metadata']['total_scenarios'] = len(scenario_tags['tags'])
    
    # Save all files
    save_json(scenarios_zh, 'scenarios_zh.json')
    save_json(scenarios_en, 'scenarios_en.json')
    save_json(code_maps, 'code_maps.json')
    save_json(scenario_tags, 'scenario_tags.json')
    
    print(f"\nDone! Added {len(candidates)} Batch 2 figures.")
    print(f"Total scenarios: {len(scenarios_zh)}")
    
    # Verify
    h_count = sum(1 for k in scenarios_zh if k.startswith('H-') or k.startswith('M-'))
    print(f"H-* historical figures: {h_count}")

if __name__ == '__main__':
    main()