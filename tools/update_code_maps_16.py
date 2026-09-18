import json

# Load existing code maps
with open('code_maps.json', 'r', encoding='utf-8') as f:
    code_maps = json.load(f)

CODE_MAP = code_maps['CODE_MAP']
CODE_MAP_EN = code_maps['CODE_MAP_EN']

# Add 16 new historical figures
CODE_MAP.update({
    "H-MZ-83": "墨子：兼爱非攻的逻辑工程大师",
    "H-YZ-84": "杨朱：为我贵生的生命哲学始祖",
    "H-HS-85": "惠施：十事十论的逻辑大师",
    "H-GSL-86": "公孙龙：白马非马的概念工程师",
    "H-WB-87": "王弼：得意忘象的玄学方法论大师",
    "H-GX-88": "郭象：独化任性的自然主义自由哲学家",
    "H-JK-89": "嵇康：越名教任自然的个性解放先驱",
    "H-TYM-90": "陶渊明：不为五斗米折腰的田园哲学家",
    "H-HY-91": "韩愈：原道师说的儒家复兴者",
    "H-ZDY-92": "周敦颐：太极图说的理学源头",
    "H-SY-93": "邵雍：皇极经世的数理易学大师",
    "H-YS-94": "叶适：事功经世致用的实用主义者",
    "H-CL-95": "陈亮：体用一原的实干爱国者",
    "H-DZ-96": "戴震：考据实学气论的科学精神先驱",
    "H-GZP-97": "龚自珍：换了人间的启蒙诗史家",
    "H-YF-98": "严复：天演论进化论的启蒙翻译家",
    "H-CYP-99": "蔡元培：思想自由兼容并包的大学自治大师",
})

CODE_MAP_EN.update({
    "H-MZ-83": "Mozi: Universal Love Anti-War Logic Engineering Master",
    "H-YZ-84": "Yang Zhu: For Self Value Life Life Philosophy Ancestor",
    "H-HS-85": "Hui Shi: Ten Matters Ten Arguments Logic Master",
    "H-GSL-86": "Gongsun Long: White Horse Non-Horse Concept Engineer",
    "H-WB-87": "Wang Bi: Get Meaning Forget Image Xuanxue Methodology Master",
    "H-GX-88": "Guo Xiang: Self-Transformation Naturalist Free Philosopher",
    "H-JK-89": "Ji Kang: Transcend Conventions Follow Nature Personality Liberation Pioneer",
    "H-TYM-90": "Tao Yuanming: Not Bend For Five Pecks Rice Pastoral Philosopher",
    "H-HY-91": "Han Yu: Original Way Teacher Theory Confucian Revivalist",
    "H-ZDY-92": "Zhou Dunyi: Taiji Diagram Saying Neo-Confucianism Source",
    "H-SY-93": "Shao Yong: Imperial Ultimate Book Mathematical Yijing Master",
    "H-YS-94": "Ye Shi: Practical Achievements Practical Learning Pragmatist",
    "H-CL-95": "Chen Liang: Substance Function One Source Practical Patriot",
    "H-DZ-96": "Dai Zhen: Evidential Practical Learning Qi Theory Science Spirit Pioneer",
    "H-GZP-97": "Gong Zizhen: Change World Enlightenment Poet Historian",
    "H-YF-98": "Yan Fu: Tian Yan Lun Evolution Theory Enlightenment Translator",
    "H-CYP-99": "Cai Yuanpei: Thought Freedom Inclusivity University Autonomy Master",
})

# Save
with open('code_maps.json', 'w', encoding='utf-8') as f:
    json.dump({"CODE_MAP": CODE_MAP, "CODE_MAP_EN": CODE_MAP_EN}, f, ensure_ascii=False, indent=2)

print("Code maps updated!")
print(f"CODE_MAP: {len(CODE_MAP)} entries")
print(f"CODE_MAP_EN: {len(CODE_MAP_EN)} entries")