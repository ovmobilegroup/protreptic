import json

# Load existing code maps
with open('code_maps.json', 'r', encoding='utf-8') as f:
    code_maps = json.load(f)

CODE_MAP = code_maps['CODE_MAP']
CODE_MAP_EN = code_maps['CODE_MAP_EN']

# Add 13 new historical figures
CODE_MAP.update({
    "H-YH-69": "颜回：德性内圣的至乐境界",
    "H-MZ-70": "孟子：性善论的民本政治哲学家",
    "H-XZ-71": "荀子：性恶论的礼治制度设计师",
    "H-DZS-72": "董仲舒：天人三策的汉儒正统奠基者",
    "H-WC-73": "王充：论衡的批判性思维先驱",
    "H-ZZ-74": "张载：太虚即气的气一元论者",
    "H-CC-75": "程颢程颐：理学正统的理一分殊奠基者",
    "H-LJY-76": "陆九渊：心即理的心学鼻祖",
    "H-LZ-77": "李贽：童心说的反正统思想解放者",
    "H-HZX-78": "黄宗羲：明夷待访录的启蒙思想先驱",
    "H-WY-79": "魏源：海国图志的洋务运动先驱",
    "H-FGF-80": "冯桂芬：校邠庐抗议的洋务运动理论家",
    "H-KYW-81": "康有为：大同书的变法维新大师",
    "H-TS-82": "谭嗣同：壬戌殉难的激进变法 martyr",
})

CODE_MAP_EN.update({
    "H-YH-69": "Yan Hui: The Supreme Joy of Virtuous Inner Sage",
    "H-MZ-70": "Mencius: Benevolent Politics Philosopher of Innate Goodness Theory",
    "H-XZ-71": "Xunzi: Institutional Designer of Innate Badness Theory and Ritual Governance",
    "H-DZS-72": "Dong Zhongshu: Founder of Han Confucian Orthodoxy with Three Strategies on Heaven and Man",
    "H-WC-73": "Wang Chong: Critical Thinking Pioneer of Lunheng",
    "H-ZZ-74": "Zhang Zai: Qi Monist of Great Void Is Qi",
    "H-CC-75": "Cheng Hao and Cheng Yi: Founders of Neo-Confucian Orthodoxy Principle One Manifestations Many",
    "H-LJY-76": "Lu Jiuyuan: Mind Learning Ancestor of Mind Is Principle",
    "H-LZ-77": "Li Zhi: Childlike Heart Saying Anti-Orthodox Thought Liberator",
    "H-HZX-78": "Huang Zongxi: Enlightenment Pioneer of Waiting for the Visit in Obscurity",
    "H-WY-79": "Wei Yuan: Ocean Countries Atlas Pioneer of Self-Strengthening Movement",
    "H-FGF-80": "Feng Guifen: Self-Strengthening Movement Theorist of Protest from Jiaobinlu",
    "H-KYW-81": "Kang Youwei: Great Unity Book Reform and Renewal Master",
    "H-TS-82": "Tan Sitong: Radical Reform Martyr of Renxu Sacrifice",
})

# Save
with open('code_maps.json', 'w', encoding='utf-8') as f:
    json.dump({"CODE_MAP": CODE_MAP, "CODE_MAP_EN": CODE_MAP_EN}, f, ensure_ascii=False, indent=2)

print("Code maps updated!")
print(f"CODE_MAP: {len(CODE_MAP)} entries")
print(f"CODE_MAP_EN: {len(CODE_MAP_EN)} entries")