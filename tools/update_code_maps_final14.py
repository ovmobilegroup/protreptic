import json

# Load existing code maps
with open('code_maps.json', 'r', encoding='utf-8') as f:
    code_maps = json.load(f)

CODE_MAP = code_maps['CODE_MAP']
CODE_MAP_EN = code_maps['CODE_MAP_EN']

# Add 14 new historical figures
CODE_MAP.update({
    "H-QY-116": "屈原：离骚楚辞的爱国悲剧诗人",
    "H-SQ-117": "司马迁：史记太史公自序的史学方法论奠基者",
    "H-BG-118": "班固：汉书百代史法的断代史大师",
    "H-LZY-119": "刘向刘歆：别录七略的目录学文献学奠基者",
    "H-CL-120": "蔡伦：造纸术改良的技术工程化大师",
    "H-ZH-121": "张衡：地动仪浑天仪的科学工程集大成者",
    "H-CL-122": "葛洪：抱朴子内外篇的炼丹药学科学先驱",
    "H-SJM-123": "孙思邈：千金方医圣的临床医学工程化大师",
    "H-LSZ-124": "李时珍：本草纲目药学系统化的实证药理学巨擘",
    "H-XQK-125": "徐霞客：游记地理学实地考察的科学考察先驱",
    "H-SYS-126": "宋应星：天工开物中国百科全书的技术工程百科大师",
    "H-PSL-127": "蒲松龄：聊斋志异志怪小说的社会批判现实主义先驱",
    "H-CXQ-128": "曹雪芹：红楼梦家族系统论的悲剧美学大师",
    "H-WJZ-129": "吴敬梓：儒林外史科举讽刺的现实主义讽刺大师",
})

CODE_MAP_EN.update({
    "H-QY-116": "Qu Yuan: Patriotic Tragic Poet of Li Sao Chu Ci",
    "H-SQ-117": "Sima Qian: Records of Grand Historian Self-Prefation Historiography Methodology Founder",
    "H-BG-118": "Ban Gu: Book of Han Dynastic History Law Dynastic History Master",
    "H-LZY-119": "Liu Xiang Liu Xin: Separate Records Seven Categories Cataloging Philology Founders",
    "H-CL-120": "Cai Lun: Papermaking Improvement Technology Engineering Master",
    "H-ZH-121": "Zhang Heng: Seismoscope Armillary Sphere Scientific Engineering Culmination",
    "H-CL-122": "Ge Hong: Baopuzi Inner Outer Chapters Alchemy Pharmacology Science Pioneer",
    "H-SJM-123": "Sun Simiao: Thousand Gold Formula Medical Sage Clinical Medicine Engineering Master",
    "H-LSZ-124": "Li Shizhen: Compendium Materia Medica Pharmacology Systematization Empirical Pharmacology Giant",
    "H-XQK-125": "Xu Xiake: Travel Notes Geography Field Investigation Scientific Investigation Pioneer",
    "H-SYS-126": "Song Yingxing: Heavenly Creations Chinese Encyclopedia Technology Engineering Encyclopedia Master",
    "H-PSL-127": "Pu Songling: Strange Stories Supernatural Fiction Social Critical Realism Pioneer",
    "H-CXQ-128": "Cao Xueqin: Dream Red Chamber Family Systems Theory Tragedy Aesthetics Master",
    "H-WJZ-129": "Wu Jingzi: Scholars Unofficial History Imperial Exam Satire Realism Satire Master",
})

# Save
with open('code_maps.json', 'w', encoding='utf-8') as f:
    json.dump({"CODE_MAP": CODE_MAP, "CODE_MAP_EN": CODE_MAP_EN}, f, ensure_ascii=False, indent=2)

print("Code maps updated!")
print(f"CODE_MAP: {len(CODE_MAP)} entries")
print(f"CODE_MAP_EN: {len(CODE_MAP_EN)} entries")