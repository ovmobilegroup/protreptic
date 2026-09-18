import json

# Load existing code maps
with open('code_maps.json', 'r', encoding='utf-8') as f:
    code_maps = json.load(f)

CODE_MAP = code_maps['CODE_MAP']
CODE_MAP_EN = code_maps['CODE_MAP_EN']

# Add 7 new historical figures
CODE_MAP.update({
    "H-HF-33": "韩非：法家集大成的制度设计师",
    "H-WAS-34": "王安石：不避浮云的变法改革家",
    "H-ZZD-35": "张之洞：中体西用的洋务运动集大成者",
    "H-HS-36": "胡适：大胆假设小心求证的实验主义先驱",
    "H-LX-37": "鲁迅：横眉冷对千夫指的解构大师",
    "H-QXS-38": "钱学森：系统工程之父的大系统观",
    "H-RZF-39": "任正非：活下去的灰度管理大师",
})

CODE_MAP_EN.update({
    "H-HF-33": "Han Fei: Legalist Master System Designer",
    "H-WAS-34": "Wang Anshi: Reformer Who Feared No Clouds",
    "H-ZZD-35": "Zhang Zhidong: Self-Strengthening Master of Chinese Essence Western Utility",
    "H-HS-36": "Hu Shi: Bold Hypothesis Careful Verification Experimentalism Pioneer",
    "H-LX-37": "Lu Xun: Cold Eyed Deconstruction Master",
    "H-QXS-38": "Qian Xuesen: Systems Engineering Father of Large Systems View",
    "H-RZF-39": "Ren Zhengfei: Survival-First Grey Zone Management Master",
})

# Save
with open('code_maps.json', 'w', encoding='utf-8') as f:
    json.dump({"CODE_MAP": CODE_MAP, "CODE_MAP_EN": CODE_MAP_EN}, f, ensure_ascii=False, indent=2)

print("Code maps updated!")
print(f"CODE_MAP: {len(CODE_MAP)} entries")
print(f"CODE_MAP_EN: {len(CODE_MAP_EN)} entries")