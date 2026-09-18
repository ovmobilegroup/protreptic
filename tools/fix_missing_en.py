import json

# Load existing scenarios
with open('scenarios_en.json', 'r', encoding='utf-8') as f:
    scenarios_en = json.load(f)

# Add missing English scenarios
new_en = {
    "H-CYK-66": {
        "name": "Chen Yinke: Independent Spirit Academic Methodology Master",
        "description": "Independent Spirit Free Thought / Evidential Research Interpretation / Liu Rushi Biography / Yuan Bai Poetry Annotations / Academic Methodology",
        "modes": [37, 22, 25, 28, 35],
        "reason": "Chen Yinke 'independent spirit, free thought', core mindset: academic methodology independence and freedom - 'evidential research and interpretation' dual drive, 'not blind follow authority, not blind follow classics, not blind follow habit'. 'Liu Rushi Biography' sources/literature/philosophy trilogy, 'Yuan Bai Poetry Annotations' poetry-history mutual verification, 'Sui Tang System Origins' institutional evolution. 'Gold Bright Hall Collection' 'my life work, in these two books', 'independent spirit, free thought'.",
        "steps": [
            "Step 1: Unity Knowledge Action - Evidential Research Interpretation Dual Wheels: Evidential Research (materials collection/verification/distinguish false preserve true), Interpretation (theory building/meaning interpretation/modern transformation), dual drive/indispensable",
            "Step 2: Systems Thinking - Independent Spirit Free Thought: 'not blind follow authority, not blind follow classics, not blind follow habit', academic autonomy/ideological freedom/methodology self-awareness",
            "Step 3: Abstract Induction - Liu Rushi Biography / Yuan Bai Poetry Annotations: sources/literature/philosophy trilogy/poetry-history mutual verification/institutional evolution/micro history writing/big history vision",
            "Step 4: Thinking Mode Selection - Academic Methodology Transmission: 'my life work, in these two books', teacher Wang Guowei/Luo Zhenyu/break Luo Zhenyu/teacher Chen Yuan/cultivate Yu Jiaying/Ye Jie/Xu Fu/Gao Ming/academic torch relay",
            "Step 5: Dormant Accumulation - Late Year Reflection: 'what I received from teacher, extended and expanded', teacher Wang Guowei/break Luo Zhenyu/teacher Chen Yuan/cultivate Yu Jiaying/Ye Jie/Xu Fu/Gao Ming/academic torch relay"
        ],
        "expected": [
            "'Liu Rushi Biography'/'Yuan Bai Poetry Annotations'/'Sui Tang System Origins' become academic classics",
            "Independent Spirit/Free Thought/Evidential Interpretation Dual Wheels/Academic Torch Relay become Chinese Academic Methodology Benchmark",
            "Lessons: late years blind/home country broken/academic loneliness/independent spirit price high"
        ],
        "case": "Liu Rushi Biography (1940s): oral/recorded by Luo Honglin/300k chars/source Liu Rushi life/Qian Qianyi/Southern Ming/Qing/women/intellectual/three-in-one source inter-verification/understanding sympathy. Yuan Bai Poetry Annotations (1930s): Yuan Zhen/Bai Juyi poems/sources/verification/mutual verification/institutional evolution/poetry-history mutual evidence. Sui Tang System Origins (1940s): three departments six ministries/nine temples five supervisions/selection/taxation/military/institutional evolution/institutional history. Late years oral/recorded by Luo Honglin/Zhu Weizheng organize. Result: independent spirit/free thought/evidential interpretation dual wheels become Chinese academic methodology benchmark."
    },
    "H-LQC-67": {
        "name": "Liang Qichao: New Historiography Reform Enlightenment Pioneer",
        "description": "Chinese History Research Method / New People Discourse / Reform Restoration / Ice Drinking Room Collection / Enlightenment Thought",
        "modes": [22, 25, 38, 28, 35],
        "reason": "Liang Qichao 'Young China Say', 'New People Say', 'Chinese History Research Method', core mindset: new historiography methodology and reform enlightenment dual breakthrough - wrote 'Chinese History Research Method' created 'new historiography': 'history is, investigate ancient, verify present, predict future'. 'New People Say' 'want new China, must first new people', citizen consciousness/public virtue/public spirit. 'Ice Drinking Room Collection' hundred volumes, 1898 reform/hundred days reform/Tan Sitong/Tan Yantong/Xu Fosu/escape Japan/run 'clear discourse report''new people monthly'. 'revolution not kill burn, revolution is old system reform'.",
        "steps": [
            "Step 1: Abstract Induction - New Historiography Three Principles: 'history is, investigate ancient, verify present, predict future', investigate/verify/predict three steps/historiography function repositioning",
            "Step 2: Systems Thinking - New People System: new people/new morality/new knowledge/new religion/new literature/new art/new life/new state/full-dimensional new people cultivation/public citizen society construction",
            "Step 3: Natural Selection - Reform Practice: 1898 reform/strong learning society/current affairs report/official/escape/run newspaper/ice drinking room collection/enlightenment/radical/conservative/three factions struggle/hundred days reform/six gentlemen/exile",
            "Step 4: Feedback Loop - Ice Drinking Room Collection: hundred volumes/poetry/prose/historiography/philosophy/politics/literature/self-description/reflection/hundred years reprint/influence Lu Xun/Hu Shi/Mao Zedong/enlightenment generation",
            "Step 5: Dormant Accumulation - Late Reflection: 'I with received from teacher, extended and expanded', teacher Kang Youwei/break Kang Youwei/Jinmen death/will 'must not let China perish in my hands', spiritual legacy"
        ],
        "expected": [
            "'Chinese History Research Method' became new historiography outline/'New People Discourse' became enlightenment movement outline/'Ice Drinking Room Collection' became modern thought treasure",
            "New historiography/new people/reform/enlightenment four major contributions/influence Lu Xun/Hu Shi/Mao Zedong/generation intellectuals",
            "Lessons: radical vs conservative tension/reform failed/exile life/thought shift complex/late years Buddhism tendency"
        ],
        "case": "Chinese history research method (1922): 'investigate ancient, verify present, predict future', three steps/new historiography outline. New people say (1902): new people/new morality/new knowledge/new religion/new literature/new art/new life/new state/full-dimensional new people. 1898 reform (1898): strong learning society/current affairs report/hundred days reform/six gentlemen/Liang escape Japan. Ice drinking room collection (1920s-1930s): hundred volumes/poetry/prose/historiography/philosophy/politics/literature/self-narration/reflection. Late years: 'I with received from teacher, extended and expanded', break Kang Youwei/Jinmen death. Result: new historiography/new people/reform/enlightenment four contributions, influence Lu Xun/Hu Shi/Mao Zedong generation intellectuals."
    }
}

# Add to English scenarios
scenarios_en.update(new_en)

with open('scenarios_en.json', 'w', encoding='utf-8') as f:
    json.dump(scenarios_en, f, ensure_ascii=False, indent=2)

print(f'Updated scenarios_en.json: {len(scenarios_en)} total scenarios')