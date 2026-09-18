import json

# Load existing code maps
with open('code_maps.json', 'r', encoding='utf-8') as f:
    code_maps = json.load(f)

CODE_MAP = code_maps['CODE_MAP']
CODE_MAP_EN = code_maps['CODE_MAP_EN']

# Add 16 new historical figures
CODE_MAP.update({
    "H-LZ-100": "老子：道家创始的无为而治大师",
    "H-ZZ-101": "庄子：逍遥游齐物论的认知自由大师",
    "H-HF-102": "韩非：法家集大成的术势法政治工程师",
    "H-SW-103": "孙武：兵法诡道的全胜战略大师",
    "H-FZY-104": "范仲淹：先天下之忧而忧的士大夫担当典范",
    "H-OYX-105": "欧阳修：史学古文三上的知识生产大师",
    "H-XQJ-106": "辛弃疾：词中豪放的实学爱国者",
    "H-WTX-107": "文天祥：零丁洋忠义的道德绝对主义者",
    "H-GZY-108": "郭子仪：九朝元老单骑见可汗的危机管理大师",
    "H-ZJZ-109": "张居正：一条鞭法万历中兴的高压改革首辅",
    "H-HR-110": "海瑞：刚正不阿击奸疏的清官标杆",
    "H-WG-111": "王艮：良知即事日用即道的平民儒学大师",
    "H-ZTY-112": "章太炎：国学革命佛学训诂的跨学科大师",
    "H-LSP-113": "刘师培：国粹史学革命辨书的学术规范大师",
    "H-QXT-114": "钱玄同：语言学音韵新文化白话文的实验主义者",
    "H-LBN-115": "刘半农：语言学实验白话诗女性主义的实验先驱",
})

CODE_MAP_EN.update({
    "H-LZ-100": "Laozi: Daoist Founder of Wu Wei Governance Master",
    "H-ZZ-101": "Zhuangzi: Free Roaming Equalizing Things Cognitive Freedom Master",
    "H-HF-102": "Han Fei: Legalism Culmination Power Law Technique Political Engineer",
    "H-SW-103": "Sun Wu: Art of War Deception Full Victory Strategy Master",
    "H-FZY-104": "Fan Zhongyan: First World Worry Last World Joy Scholar-Official Responsibility Model",
    "H-OYX-105": "Ouyang Xiu: Historiography Ancient Prose Three Ups Knowledge Production Master",
    "H-XQJ-106": "Xin Qiji: Ci Poetry Heroic Practical Learning Patriot",
    "H-WTX-107": "Wen Tianxiang: Lingding Yang Loyalty Moral Absolutist",
    "H-GZY-108": "Guo Ziyi: Nine Dynasties Elder Single Horse See Khan Crisis Management Master",
    "H-ZJZ-109": "Zhang Juzheng: Single Whip Law Wanli Revival High Pressure Reform Chief Minister",
    "H-HR-110": "Hai Rui: Upright Incorruptible Strike Corrupt Memorial Clean Official Benchmark",
    "H-WG-111": "Wang Gen: Innate Knowledge Is Matter Daily Use Is Way Commoner Confucianism Master",
    "H-ZTY-112": "Zhang Taiyan: Sinology Revolution Buddhism Exegesis Interdisciplinary Master",
    "H-LSP-113": "Liu Shipei: Sinology Historiography Revolution Exegesis Academic Standard Master",
    "H-QXT-114": "Qian Xuantong: Linguistics Phonology New Culture Vernacular Experimentalist",
    "H-LBN-115": "Liu Bannong: Linguistics Experimental Vernacular Poetry Feminism Experimental Pioneer",
})

# Save
with open('code_maps.json', 'w', encoding='utf-8') as f:
    json.dump({"CODE_MAP": CODE_MAP, "CODE_MAP_EN": CODE_MAP_EN}, f, ensure_ascii=False, indent=2)

print("Code maps updated!")
print(f"CODE_MAP: {len(CODE_MAP)} entries")
print(f"CODE_MAP_EN: {len(CODE_MAP_EN)} entries")