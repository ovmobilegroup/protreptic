import json

with open('scenarios_en.json', 'r', encoding='utf-8') as f:
    en = json.load(f)

with open('scenarios_zh.json', 'r', encoding='utf-8') as f:
    zh = json.load(f)

with open('modes_data.json', 'r', encoding='utf-8') as f:
    modes = json.load(f)

en_modes = modes['en']

# The 8 missing entries from Chinese that need English translations
# I'll create high-quality translations following the existing style

new_entries = {
    "H-MZD-150": {
        "name": "Mao Zedong: Chief Architect of New Democratic Revolution and Engineering of Systemic Program",
        "description": "Revolutionary Program Engineering / Ideology × Party-Building × Army-Building × Nation-Building Four-Dimensional Closure / Contradiction Analysis / Encircle Cities from Countryside / United Front / Institutional Checks & Balances",
        "modes": [42, 1, 6, 4, 34],
        "reason": "Mao Zedong engineered the 'Ideology × Party-Building × Army-Building × Nation-Building' four dimensions into a reusable complete revolutionary engineering system: program first defines nature, party-building solves leadership core, army-building solves violent seizure of power, nation-building solves governance consolidation — forming a 'Program → Organization → Violence → Governance' closure, with each link having operable strategic-tactical modules (e.g., 'Encircle Cities from Countryside' solves army-building implementation, 'United Front' solves party-building expansion, 'New Democratic Program' solves nation-building definition).",
        "steps": [
            "Step 1: Program Defines Nature — Use 'Principal Contradiction Analysis' (Mode 1) to lock historical stage nature, extract minimum viable program (e.g., New Democracy's five tasks)",
            "Step 2: Core Organization — Use 'United Front' (Mode 6) to build 'core layer + alliance layer + intermediate layer' three-tier organizational architecture, solving legitimacy source of leadership",
            "Step 3: Violence Engineering — Use 'Encircle Cities from Countryside' (Mode 4) + 'Mobile Warfare' (Mode 15) to design asymmetric violent seizure path, modularizing strategic defense/stalemate/counteroffensive three stages",
            "Step 4: Governance Consolidation — Use 'Institutional Checks & Balances' (Mode 34) + 'Holistic Thinking' (Mode 22) to convert revolutionary dividends into state governance system, establishing 'party-government-military-civilian-academic, east-west-south-north-center party-government-military-civilian-academic' full-coverage architecture",
            "Step 5: Retrospective Iteration — Use 'Seek Truth from Facts' (Mode 5) to establish 'practice → cognition → re-practice → re-cognition' spiral-up epistemological closure, preventing dogmatism"
        ],
        "expected": [
            "Established New Democratic Revolution complete engineering system: program-organization-violence-governance four-dimensional closure",
            "Created 'Encircle Cities from Countryside' asymmetric warfare paradigm, winning national power from position of weakness",
            "Built 'United Front' three-tier organizational architecture, maximizing political inclusiveness and mobilization capacity",
            "Designed 'Institutional Checks & Balances' state governance architecture, converting revolutionary dividends into governance capacity",
            "Provided 'Revolutionary Program Engineering' benchmark: ideology first, party-building core, army-building violence, nation-building governance"
        ],
        "case": "1921-1949 New Democratic Revolution: 1921 party founding established 'ideology' program; 1927 August 1 Nanchang Uprising launched 'army-building', 1927 Autumn Harvest Uprising then Jinggangshan established 'Encircle Cities from Countryside' line; 1935 Zunyi Conference established core leadership, Anti-Japanese War 'United Front' expanded to whole nation; 1945 7th Congress established Mao Zedong Thought guiding position; 1946-1949 Three Major Campaigns 'Mobile Warfare' annihilated KMT main forces; 1949 New CPPCC convened 'nation-building' defined, established 'party-government-military-civilian-academic, east-west-south-north-center party-government-military-civilian-academic' governance architecture. Full process 'program defines nature → core organization → violence engineering → governance consolidation' four steps, each with reusable tactical modules."
    },
    
    "H-XMQ-151": {
        "name": "Xue Muqiao: Price Reform Theory Foundation and Reform Risk Decision Framework",
        "description": "Price Dual-Track System / Law of Value / Loss Aversion Framework / Compensation Mechanism / Information Velocity Monitoring / Market Socialist Economics",
        "modes": [26, 19, 38, 39, 41],
        "reason": "Xue Muqiao introduced the 'price = information + incentive' information-theory perspective into planned economy reform: proposed 'price dual-track system' (planned price + market price coexisting), 'law of value is socialist economic law', and pioneered using 'loss aversion' framework to explain reform resistance — reform creates dispersed, long-term gains while losses are concentrated and immediate, therefore must design 'compensation mechanisms' and 'gradual fault tolerance' to offset loss aversion. His 'necessary losses vs unnecessary losses' distinction became the core heuristic for reform risk decision-making.",
        "steps": [
            "Step 1: Loss Ledger Modeling — Use 'Loss Aversion Thinking' (Mode 26) to list 'immediate loss ledger' for each reform stakeholder (quantify money/power/status losses), identify 'concentrated loss groups'",
            "Step 2: Compensation Mechanism Design — Use 'Marginal Thinking' (Mode 19) to design 'targeted compensation / transitional placement / benefit sharing', making marginal gains ≥ marginal losses for loss groups",
            "Step 3: Dual-Track Fault Tolerance Channel — Use 'Crossing River by Feeling Stones' (Mode 38) to open 'planned track + market track' parallel channels, allowing market track to experiment within 'birdcage' (Mode 39), planned track as safety net",
            "Step 4: Information Velocity Monitoring — Use 'Relay Station / Information Velocity' (Mode 41) to build 'price signal → enterprise decision → resource reallocation → feedback to center' high-frequency feedback loop, compressing reform signal transmission delay to monthly level",
            "Step 5: Necessary Loss Differentiation — Establish 'necessary losses (inevitable in system transition) vs unnecessary losses (design flaws / execution deviations)' discrimination standard, dynamically adjust reform tempo"
        ],
        "expected": [
            "Founded price reform theory: dual-track system, law of value, price = information + incentive",
            "Created reform risk decision framework: loss aversion modeling → compensation mechanism → dual-track fault tolerance → information velocity monitoring",
            "'Necessary losses vs unnecessary losses' becomes core heuristic for reform decision-making",
            "Fills Mode 26 'Loss Aversion Thinking' zero-coverage gap; reinforces single-point Modes 39/41"
        ],
        "case": "1980s Price Reform: Xue Muqiao advocated 'price dual-track system' — retain planned prices for livelihood/key projects, simultaneously release market prices by supply-demand. 1984 'Report on Price Reform' established 'planned track planned price, off-plan track market price' dual-track parallel. Facing 'price rise → public dissatisfaction → reform resistance' loss aversion dynamics, designed 'wages linked to price index', 'price subsidies' compensation mechanisms; used 'birdcage economy' to set price fluctuation bounds; established 'monthly price monitoring → quarterly policy fine-tuning' high-frequency feedback loop. 1992 dual-track merger completed, price reform soft landing, avoided 'shock therapy' social upheaval."
    },
    
    "H-ZEL-153": {
        "name": "Zhou Enlai: Diplomatic Breakthrough · United Front Unity · Government Operation Trinity State Governance Engineering",
        "description": "Diplomatic Ten Principles / United Front Sixteen-Character Guideline / Zhou Three Meetings / Three-Level Meeting System / Three-Level Responsibility Chain / Diplomatic Asset Compounding / Systemic Program / Game Theory / Relay Station / Institutional Checks & Balances",
        "modes": [42, 20, 6, 41, 34],
        "reason": "Zhou Enlai constructed 'Diplomatic Breakthrough → United Front Unity → Government Operation' trinity state governance engineering system: diplomatically used 'seek common ground while reserving differences, mutual benefit and win-win' Five Principles to break Cold War blockade, achieving 'break non-intercourse → establish relations → expand domains' three-stage breakthrough; united front used 'long-term coexistence, mutual supervision, heart-to-heart, honor-disgrace shared' sixteen-character guideline to bring democratic parties/business-religious/overseas Chinese into 'patriotic united front'; government used 'Zhou Three Meetings, State Council Executive Meetings, Special Briefings' three-level meeting system, standardizing 'Premier responsibility, Minister responsibility, Section Chief responsibility' three-level responsibility chain, achieving 'decision-execution-feedback' high-frequency closure.",
        "steps": [
            "Step 1: Breakthrough Anchors Consensus — Use 'Game Theory Thinking' (Mode 20) to identify opponent's 'core interests non-negotiable, non-core interests exchangeable' boundary, use 'seek common ground' to anchor minimum consensus set",
            "Step 2: United Front Concentric Circle Expansion — Use 'United Front' (Mode 6) to design 'core layer (Communist Party) → alliance layer (democratic parties/business/religious) → intermediate layer (overseas/intellectuals) → outer layer (opposition convertibles)' four-layer expansion algorithm",
            "Step 3: Government Operation Three-Level Meetings — Use 'Relay Station / Information Velocity' (Mode 41) to build 'Zhou Three Meetings (strategic/daily) → Executive Meetings (tactical/weekly) → Special Briefings (specialized/monthly)' three-level information velocity tiered system, decision delay < 24h",
            "Step 4: Three-Level Responsibility Chain — Use 'Institutional Checks & Balances' (Mode 34) + 'Procedural Justice' (Mode 32) to solidify 'Premier decides-Minister executes-Section Chief implements' into 'countersignature system, first-inquiry system, time-limited completion system' three major procedural locks",
            "Step 5: Diplomatic Asset Compounding — Use 'Feedback Loops' (Mode 29) to convert each diplomatic achievement (establish relations/agreements/statements) into 'legal text → domestic law synchronization → execution monitoring → next round negotiation leverage' positive feedback loop"
        ],
        "expected": [
            "Led Geneva Conference (1954), Bandung Conference (1955), China-US Breakthrough (1971-1972), China-Japan Normalization (1972) diplomatic breakthroughs",
            "Established 'Patriotic United Front' sixteen-character guideline, incorporating democratic parties/business/religious/overseas Chinese",
            "Created 'Zhou Three Meetings / Executive Meetings / Special Briefings' three-level government operation system, decision delay < 24 hours",
            "Established 'Premier-Minister-Section Chief' three-level responsibility chain: countersignature/first-inquiry/time-limited completion",
            "Mode 42 second candidate, cross-validates 'Revolutionary Program Engineering'; reinforces Modes 20/41/34"
        ],
        "case": "1954 Geneva Conference: Zhou Enlai used 'seek common ground while reserving differences' Five Principles to break Cold War blockade, achieved 'break non-intercourse → establish relations' breakthrough, established relations with 14 countries. 1955 Bandung Conference: proposed 'seek common ground' principle, promoted Afro-Asian unity. 1971-1972 China-US Breakthrough: used 'Game Theory' to identify US 'core interest = anti-Soviet, non-core = Taiwan status' boundary, designed 'Shanghai Communique' ambiguity on Taiwan issue anchoring minimum consensus. Domestic government operation: 1953-1976 chaired 2000+ Zhou Three Meetings, Executive Meetings, built 'Premier decides → Minister executes → Section Chief implements' three-level chain, countersignature ensures cross-department coordination, first-inquiry solves buck-passing, time-limited completion compresses decision delay. Diplomatic achievement conversion: each establishment/agreement → legal text → domestic law sync (e.g., 'Law on Application of Laws to Foreign-Related Civil Relations') → execution monitoring → next round negotiation leverage, forming positive feedback loop."
    },
    
    "H-ZKZ-154": {
        "name": "Zhu Kezhen: Meteorology Foundation and Science-Education for Nation Dual Paradigm",
        "description": "Phenomenological Observation / Statistical Regularity / Physical Mechanism / Dual-Network Fusion Observation System / Zhejiang University President 13 Years / Seeking Truth Motto / General+Professional+Character Trinity / Wartime Education Resilience",
        "modes": [41, 25, 12, 22, 35],
        "reason": "Zhu Kezhen fused 'phenomenological observation + statistical regularity + physical mechanism' three-layer methodology into 'Chinese-style Earth System Science': presided over compilation of 'Chinese Climatology', 'Chinese Flora', established 'National Meteorological Station Network + Plant Phenological Observation Network' dual-network fusion observation system; ran Zhejiang University 'four years resistance war, seven years exile, education never ceased', created 'general education + professional education + character education' trinity university model, proposed 'Seeking Truth' motto and implemented as 'seek truth from facts → be practical and realistic → demand thorough accountability' three-level execution standard.",
        "steps": [
            "Step 1: Observation Network Weaving — Use 'Relay Station / Information Velocity' (Mode 41) to design 'national-provincial-county-township' four-level meteorological/phenological observation network, node coverage > 90%",
            "Step 2: Multi-Source Data Fusion — Use 'Abstract Induction' (Mode 25) to fuse 'instrument observation + phenological records + documentary history + agricultural proverbs' four-source data, cross-verify correct single-source bias",
            "Step 3: Regularity-Mechanism Dual Verification — Use 'Systems Thinking' (Mode 12) to bidirectionally anchor statistical regularities (e.g., phenological period vs accumulated temperature relationship) with physical mechanisms (light-temperature-water coupling models), improving prediction interpretability",
            "Step 4: General-Professional-Character Trinity — Use 'Holistic Thinking' (Mode 22) to design 'general foundation (humanities) + professional depth (STEM/agriculture/medicine) + character cultivation (seeking truth spirit)' three-dimensional talent model, curriculum/evaluation/management three-matched",
            "Step 5: Exile Education Resilience — Use 'Dormant Accumulation' (Mode 35) + 'Guerrilla 16-Character Tactics' (Mode 16) to convert 'relocation = change track, destruction = reconstruction, resource scarcity = focus core' into organizational survival algorithm"
        ],
        "expected": [
            "Presided over compilation of 'Chinese Climatology', 'Chinese Flora', founding modern Chinese meteorology/geography",
            "Built 'National Meteorological Station Network + Plant Phenological Observation Network' dual-network fusion system, node coverage > 90%",
            "Ran Zhejiang University 13 years 'four years resistance war, seven years exile, education never ceased', created 'general + professional + character' trinity university model",
            "'Seeking Truth' motto implemented as three-level execution standard: seek truth from facts → be practical and realistic → demand thorough accountability",
            "Mode 41 reinforces second candidate; Mode 16 low-frequency reinforcement; Modes 22/25 high-frequency core reinforcement"
        ],
        "case": "1936-1949 Zhejiang University Westward Relocation: Zhu Kezhen served as ZJU president 13 years, led faculty/students from Hangzhou → Anhui Anqing → Jiangxi Taixing/Jiande → Fujian Yong'an/Jianou → Zhejiang Jiangshan/Lishui → back to Hangzhou, traversed 7 provinces, 2000+ km journey, 7 years duration. 'Exile without ceasing education': established 'mobile library, mobile laboratory, mobile specimen museum' mobile teaching system. Observation network building: 1941 presided over 'Chinese Meteorological Society', 'National Meteorological Station Network', wartime used 'Phenological Observation Network' (farmers recording flowering/harvest/frost phenological periods) to fill instrument observation gaps, forming 'instrument + phenology' dual-network fusion. Seeking Truth implementation: curriculum 'general compulsory (humanities 30%) + professional core + practical internship' three modules; evaluation 'process assessment (daily 40%) + summative assessment (final 60%)'; management 'college autonomy + school affairs openness + student autonomy' three-governance fusion."
    },
    
    "H-HLG-155": {
        "name": "Hua Luogeng: Mathematical Self-Taught Talent and Applied Mathematics Engineering Full-Chain Autonomous Paradigm",
        "description": "Self-Taught Success / Optimization Method / Multi-Objective Programming / Mathematical Mechanization / Hua Luogeng Math Class / Youth Class / Juvenile Class / Mathematics Popularization / Engineering Implementation",
        "modes": [9, 17, 38, 7],
        "reason": "Hua Luogeng created 'self-study → research → popularization → application' mathematics full-chain autonomous paradigm: junior high dropout self-studied to world-class, proposed 'mathematize, mathematize, re-mathematize' application trilogy, launched 'Optimization Method (Golden Section Method)', 'Multi-Objective Programming', 'Mathematical Mechanization' three major application engineering, pushing mathematics from 'court game' to 'productivity tool'; established 'Hua Luogeng Math Class → Youth Class → USTC Juvenile Class' talent screening chain, changing China's basic science talent selection ecology.",
        "steps": [
            "Step 1: Self-Study Shortest Path — Use 'Self-Reliance' (Mode 9) to design 'classic textbook intensive reading → core problem self-proof → frontier literature reproduction → open problem attack' four-stage self-study map, skipping non-essential courses",
            "Step 2: Methodology Toolization — Use 'Mental Models' (Mode 17) to extract 'analogy method, induction method, extremum principle, symmetry, invariants' as reusable mathematical toolbox, open to non-mathematicians",
            "Step 3: Optimization Algorithm Landing — Use 'Crossing River by Feeling Stones' (Mode 38) to push 'Golden Section Method / 0.618 Method' from theory to chemical/metallurgical/agricultural sites, 'one factory one policy' on-site tuning, speaking with output ratio",
            "Step 4: Talent Funnel Screening — Use 'Strategic Foresight' (Mode 7) to design 'interest test → ability test → mentor system → international competition' four-level funnel, using 'Juvenile Class' to compress talent growth cycle 5-8 years",
            "Step 5: Mathematics Popularization Engineering — Promote 'mathematize, mathematize, re-mathematize' trilogy: theoretical mathematization → applied mathematization → popularized mathematization, establishing complete conversion chain from basic research to productivity"
        ],
        "expected": [
            "Junior high dropout self-studied to world-class mathematician, proving 'self-study shortest path' reusable",
            "Launched Optimization Method (Golden Section), Multi-Objective Programming, Mathematical Mechanization three major application engineering",
            "Pushed mathematics from 'court game' to 'productivity tool': chemical/metallurgical/agricultural on-site tuning",
            "Built 'Hua Luogeng Math Class → Youth Class → USTC Juvenile Class' talent screening chain, changing basic science selection ecology",
            "Mode 9 third candidate, reinforces 'basic science autonomy' scenario; Mode 17 low-frequency reinforcement; Mode 7 low-frequency reinforcement"
        ],
        "case": "1930s Cambridge Study: Hua Luogeng junior high graduate, self-studied advanced math to world-class, 1936 to Cambridge under Hardy researching analytic number theory, published 'On Waring's Problem' classic papers. 1950s Optimization Method promotion: brought Golden Section from theory into chemical plants 'catalyst ratio optimization', metallurgical plants 'sintering batch optimization', agriculture 'fertilizer dosage optimization', each factory on-site tuning weeks, output ratio up 20-50%. 1970s Mathematical Mechanization: proposed 'machine proving geometric theorems' direction, founded China automated reasoning field. 1978 founded 'Hua Luogeng Math Class' → 1985 'USTC Juvenile Class': designed 'interest test → ability test → mentor system → international competition' four-level funnel, compressed talent growth cycle 5-8 years, cultivated Tian Gang, Zhu Xiping, Chen Xiaoxu and other math leaders."
    },
    
    "H-TYY-156": {
        "name": "Tu Youyou: Artemisinin Discovery and Chinese-Western Medicine Integration Drug Screening Paradigm Founder",
        "description": "Artemisin / Literature Textual Research / Chemical Separation / Efficacy Verification / Triple Cross-Validation / Ethnic Medicine Modernization / Nobel Prize / Technical Package Standardization",
        "modes": [25, 1, 5, 34],
        "reason": "Tu Youyou in the triple deadlock of 'single compound screening failure, traditional formula components complex, extraction process uncontrollable', used 'literature textual research + chemical separation + efficacy verification' triple cross-validation method: inspired by 'Handbook of Prescriptions for Emergencies' 'one handful of qinghao, soaked in two liters of water, wring out juice, drink all', changed 'boiling water decoction' to 'low-temperature ether extraction' preserving heat-labile active ingredient, extraction rate 0% → 95%; established 'TCM monomer → structure confirmation → synthetic analogs → clinical verification' full-chain standard, pioneering 'ethnic medicine modernization' new paradigm, saving tens of millions of lives globally.",
        "steps": [
            "Step 1: Literature Mining Targeting — Use 'Abstract Induction' (Mode 25) to extract 'malaria / intermittent fever / chills-fever' keywords from 2000+ ancient prescriptions, build 'formula-symptom-ingredient' three-dimensional retrieval library, locked 380 candidate formulas",
            "Step 2: Process Reverse Engineering — Use 'Contradiction Analysis' (Mode 1) to locate 'high-temperature decoction = principal contradiction destroying active ingredient', reversely design 'low-temperature / non-polar solvent / rapid separation' unconventional process, breaking 'water decoction' path dependence",
            "Step 3: Triple Cross-Validation — Use 'Seek Truth from Facts' (Mode 5) to design 'mouse/monkey/human' three-species, 'monomer/compound/synthetic analogs' three-forms, 'in-vivo/in-vitro/clinical' three-scenarios cross-validation matrix, eliminating single-point coincidence",
            "Step 4: Standardized Transfer Package — Use 'Institutional Checks & Balances' (Mode 34) to package 'extraction process SOP, quality control standards, clinical protocol, patent layout' as transferable 'Artemisinin Technical Package', supporting global rollout",
            "Step 5: Team Collaboration Mechanism — 'Project 523 Office' cross-institute/cross-discipline/cross-region collaboration: TCM Institute / Drug Institute / Beijing TCM Hospital / Guangzhou Military Region / Yunnan/Hainan bases, established 'weekly sync, monthly summary, quarterly evaluation' rhythm"
        ],
        "expected": [
            "Inspired by 'Handbook of Prescriptions for Emergencies', changed boiling water decoction to low-temperature ether extraction, artemisinin extraction rate 0% → 95%",
            "Established 'TCM monomer → structure confirmation → synthetic analogs → clinical verification' full-chain standard, pioneering ethnic medicine modernization paradigm",
            "Triple cross-validation matrix (3 species × 3 forms × 3 scenarios) eliminates single-point coincidence, confirms efficacy",
            "Artemisinin technical package standardized transfer, supports global rollout, saved tens of millions of lives, 2015 Nobel Prize in Physiology or Medicine",
            "Provides 'traditional knowledge modernization' benchmark paradigm: literature research + process breakthrough + cross-validation + standardized package"
        ],
        "case": "1969-1972 'Project 523' Campaign: 60+ units nationwide, 500+ people invested in single compound screening, 40,000+ compounds total wipeout. Tu Youyou team 'TCM Group' alternative path: consulted 2000+ ancient formulas, built 'formula-symptom-ingredient' retrieval library, locked 380 candidates. From Ge Hong 'Handbook of Prescriptions for Emergencies' 'one handful qinghao, water soak wring juice' inspired: traditional 'water decoction' high temperature destroys active ingredient, reversely designed 'low-temperature ether extraction' (bp 34.6°C) preserving artemisinin. Oct 4, 1971 extraction rate broke 95%. Established 'mouse/rhesus monkey/human' × 'monomer/compound/synthetic analogs' × 'in-vivo/in-vitro/clinical' 27-cell validation matrix, eliminated coincidence. 1977 artemisinin structure confirmed (unique peroxide bridge), 1980s synthetic analogs artesunate/dihydroartemisinin. Packaged 'extraction process SOP + quality standards + clinical protocol + patent layout' as technical package, WHO global rollout, 2000+ saved estimated tens of millions of lives. 2015 Nobel Prize."
    },
    
    "H-LSQ-157": {
        "name": "Liu Shaoqi: Party-Building Organizational Line Engineering and Intra-Party Rule of Law System Construction",
        "description": "Party-Building Engineering / Organizational Line / On the Cultivation of Communist Party Members / Secure Inside Repel Outside / Democratic Centralism / Party Member Standards Quantification / Development Procedure Standardization / Organizational Life Systematization / Discipline Execution Grading",
        "modes": [42, 10, 32, 34],
        "reason": "Liu Shaoqi engineered 'Party Building' into 'Organizational Line → Discipline Construction → Cadre Management → Intra-Party Rule of Law' four major standardized subsystems: presided over drafting 'Party Constitution' (7th Congress) establishing 'Democratic Centralism' organizational principle; wrote 'On the Cultivation of Communist Party Members' decomposing 'Party Spirit Cultivation' into 'Standpoint, Viewpoint, Method, Style, Discipline' five-dimensional assessable indicators; created 'Secure Inside Repel Outside' intra-party struggle strategy — 'Secure Inside' uses 'Criticism & Self-Criticism' (Mode 10) to resolve internal contradictions, 'Repel Outside' uses 'United Front' to isolate external enemies; promoted 'Report on Party Building Issues' establishing 'Party Member Standards, Development Procedures, Organizational Life, Disciplinary Sanctions' four major institutional frameworks.",
        "steps": [
            "Step 1: Party Member Standards Quantification — Use 'Criticism & Self-Criticism' (Mode 10) to decompose 'Communist Party Member Conditions' into 'Political Firmness, Theoretical Level, Mass Work Ability, Clean Self-Discipline, Vanguard Exemplary Role' five-dimensional scorecard",
            "Step 2: Development Procedure Standardization — Use 'Procedural Justice' (Mode 32) to design 'Application → Investigation → Admission → Probation → Full Membership → Assessment' six-stage standard process, each stage with 'Investigator, Investigation Form, Investigation Period, Assessment Standard' four fixes",
            "Step 3: Organizational Life Systematization — Use 'Institutional Checks & Balances' (Mode 34) to solidify 'Three Meetings One Class (Branch Congress / Branch Committee / Party Group Meeting / Party Class), Democratic Life Meeting, Organizational Life Meeting' three major rigid systems, absence rate incorporated into assessment",
            "Step 4: Discipline Execution Grading — Use 'Framing Effect' (Mode 31) to classify disciplinary violations into 'Political/Organizational/Integrity/Mass/Work/Life' six categories, four grades (Warning/Serious Warning/Removal from Post/Expulsion), establishing 'Violation → Sanction → Appeal → Review' procedural closure",
            "Step 5: Secure Inside Repel Outside Strategy — Internal uses 'Criticism & Self-Criticism' to resolve non-antagonistic contradictions, external uses 'United Front' to isolate enemies, forming 'Intra-Party Democracy + Iron Discipline' dialectical unity"
        ],
        "expected": [
            "Presided over drafting 'Party Constitution' (7th Congress) establishing 'Democratic Centralism' organizational principle, founding party-building organizational line",
            "'On the Cultivation of Communist Party Members' quantified 'Party Spirit Cultivation' into five assessable indicators, becoming party member education classic",
            "Created 'Secure Inside Repel Outside' intra-party struggle strategy: Secure Inside uses Criticism & Self-Criticism, Repel Outside uses United Front",
            "Promoted 'Report on Party Building Issues' establishing Party Member Standards/Development Procedures/Organizational Life/Disciplinary Sanctions four major institutional frameworks",
            "Mode 42 third candidate, reinforces 'Party Building Engineering'; Modes 10/32 low-frequency reinforcement"
        ],
        "case": "1945 7th Congress: Liu Shaoqi delivered 'Report on Amending Party Constitution', presided over drafting new 'Party Constitution' formally establishing 'Democratic Centralism' as organizational principle, clarifying party member 'voluntary admission, individual admission, branch absorption' standard. 1939 'On the Cultivation of Communist Party Members' published: decomposed 'Communist Party Member Cultivation' into 'Marxist Standpoint, Dialectical Materialist Viewpoint, Linking Reality Method, Close to Masses Style, Strict Discipline' five dimensions, each with concrete behavioral anchors (e.g., 'no private gain, no fear of sacrifice, no special privileges'). 1943 'Report on Party Building Issues': systematically expounded 'Party Member Standards, Development Procedures, Organizational Life, Disciplinary Sanctions' four major systems. 1956 8th Congress: promoted 'Intra-Party Supervision Regulations (Draft)', 'Party Member Rights Guarantee Regulations (Draft)', established 'Violation → Sanction → Appeal → Review' procedural closure. 'Secure Inside Repel Outside' practice: Yan'an Rectification used 'Criticism & Self-Criticism' to resolve Dogmatism/Empiricism/Subjectivism internal contradictions; Anti-Japanese War used 'United Front' to isolate Wang Jingwei surrender faction, win over middle forces."
    },
    
    "H-PDH-152": {
        "name": "Peng Dehuai: Military Practice of Mass Line and Hundred Regiments Offensive Command Art",
        "description": "Mass Line Militarization / Hundred Regiments Offensive / Korean War / Peng Dehuai Training Outline / Officer-Soldier Unity / Military-Civilian Unity / Enemy Disintegration",
        "modes": [2, 6, 31, 34],
        "reason": "Peng Dehuai internalized 'Mass Line' from political work into 'Military Training / Combat Command / Logistics Support' full-chain operating system: created 'Officer-Soldier Unity, Military-Civilian Unity, Enemy Disintegration' three major military mass line principles; designed 'Hundred Regiments Offensive' with 'Dispersed Guerrilla → Concentrated Attack → Dispersed Concealment' rhythm mobilizing 200k civilian workers; Korean War 'One Against Ten' relied on 'Concealed Engineering, Tunnel Warfare, Night Maneuver' to convert US firepower superiority into 'Cannot Hit, Cannot Find, High Consumption' strategic burden; wrote 'Peng Dehuai Training Outline' standardizing 'Mass Line' into 12 training outlines.",
        "steps": [
            "Step 1: Officer-Soldier Unity Core — Use 'Mass Line' (Mode 2) to implement 'Same Food Same Quarters Same Training' as 'Officers Lead Digging Tunnels, Commanders First to Charge' observable behavioral standards, eliminating privilege barriers",
            "Step 2: Military-Civilian Unity Mobilization — Use 'United Front' (Mode 6) to design 'Civilian Worker Department Establishment → Rations Local Procurement → Wounded Local Placement → Intelligence All-Citizen Soldiers' four-in-one mobilization system, turning populace into 'Logistics Department'",
            "Step 3: Enemy Disintegration Psychological Warfare — Use 'Framing Effect' (Mode 31) to design 'Shout/Leaflet/Release Prisoners/Kind Treatment of POWs' four-layer rhetoric framework, reconstructing 'US Military Invincible' into 'Going Home Is Glory' narrative",
            "Step 4: Training Outline Standardization — Use 'Institutional Checks & Balances' (Mode 34) to solidify 'Mass Line' into '12 Outlines, 48 Indicators, Assessment Red-Green Lights' standard system, preventing 'Formalism / Campaign-Style Rectification' rebound",
            "Step 5: Campaign Command Art — Combine 'Contradiction Analysis' (Mode 1) to identify enemy-own principal contradiction, use 'Mobile Warfare' (Mode 15) to concentrate superior forces for piecemeal annihilation"
        ],
        "expected": [
            "Created complete 'Mass Line Militarization' operating system: Officer-Soldier Unity, Military-Civilian Unity, Enemy Disintegration three principles",
            "Commanded Hundred Regiments Offensive: mobilized 200k civilian workers, Dispersed Guerrilla → Concentrated Attack → Dispersed Concealment,震慑日军",
            "Korean War 'One Against Ten': Concealed Engineering / Tunnel Warfare / Night Maneuver neutralized US firepower superiority",
            "Wrote 'Peng Dehuai Training Outline' standardizing Mass Line into 12 outlines, 48 indicators",
            "Fills Mode 2 'Mass Line' low-frequency (only 4 people) gap; provides 'Military Mass Line' benchmark case"
        ],
        "case": "1940 Hundred Regiments Offensive: Peng Dehuai commanded 105 regiments, 400k troops, used 'Dispersed Guerrilla → Concentrated Attack → Dispersed Concealment' three-phase rhythm, mobilized 200k civilian workers, destroyed Tongpu/Zhengtai/Shide/Daoqing railways 470+ km, destroyed 1000+ bridges/tunnels, annihilated 20k+ Japanese/puppet troops. 1950-1953 Korean War: facing '20-year equipment gap, 10x firepower superiority' US military, relied on 'Concealed Engineering (tunnel depth 10m+), Night Maneuver (40km daily march), Mobile Warfare (local 3:1 concentration)' to convert US 'Air-Ground Integrated Firepower Superiority' into 'Cannot Hit, Cannot Find, High Consumption' strategic burden, forcing US to sign armistice. 1953 'Peng Dehuai Training Outline' promulgated: 12 outlines covering Political/Military/Physical/Technical/Tactical/Service/Logistics/Medical/Equipment/Management/Assessment/Reward-Punishment, transforming 'Mass Line' from slogan into assessable standards."
    }
}

# Remove the old H-PDH-130 entry
if 'H-PDH-130' in en:
    del en['H-PDH-130']
    print("Removed H-PDH-130")

# Add the new entries
for key, entry in new_entries.items():
    en[key] = entry
    print(f"Added {key}: {entry['name']}")

# Save
with open('scenarios_en.json', 'w', encoding='utf-8') as f:
    json.dump(en, f, ensure_ascii=False, indent=2)

print(f"\nTotal EN entries now: {len(en)}")