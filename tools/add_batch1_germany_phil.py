#!/usr/bin/env python3
import json

# Load existing scenarios
base_path = "/opt/data/workspace/Protreptic/tools"

with open(base_path + '/scenarios_zh.json', 'r', encoding='utf-8') as f:
    scenarios_zh = json.load(f)

with open(base_path + '/scenarios_en.json', 'r', encoding='utf-8') as f:
    scenarios_en = json.load(f)

with open(base_path + '/code_maps.json', 'r', encoding='utf-8') as f:
    code_maps = json.load(f)

# 4 more figures (8 total now) - continue with remaining German philosophers
new_additional = {
    "EU-DE-PHIL-001": {
        "name": "康德：实践理性/道德哲学/先验唯心主义/批判力/全球伦理",
        "description": "康德提出实践理性/道德哲学/先验唯心主义/批判力/全球伦理",
        "modes": [8, 6, 1, 5, 24],
        "reason": "康德'实践理性'、'categorical imperative'、'先验唯心主义'、'批判力'、'全球伦理'，核心思维：批判哲学方法论与实践理性革命——哥德巴赫/现象学/先验辩证/实践理性/全球伦理发展三大支柱，康德成为现代哲学奠基者/伦理学家。",
        "steps": [
            "第1步：抽象归纳法——先验批判创制：从感性直观/理解范畴/判断力批判出发，建立先验哲学",
            "第2步：系统思维法——实践理性方法论：先验辩证/现象学/先验唯心主义/批判力发展",
            "第3步：矛盾分析法——传统形而上学危机：神学/形而上学/经验论局限",
            "第4步：知行合一——实践理性：categorical imperative/普遍法则/目的性/自由/尊重人格三位一体",
            "第5步：蛰伏积势——全球伦理发展：katholikos/和平理性/世界公民/全球伦理"
        ],
        "expected": [
            "先验批判成现代哲学基石/伦理学/先验唯心主义/批判力影响现代哲学",
            "实践理性/道德哲学/先验唯心主义/批判力发展三大支柱/影响现代伦理学",
            "教训：极端理性主义/先验唯心主义局限/晚年思想变化/影响后世"
        ],
        "case": "康德一生：1742年出生康尼斯堡/1755年柏林大学博士/1781年《纯粹理性批判》/1788年《实践理性批判》/1795年《判断力批判》/1800年《人类理性限界的界限》/1804年《未来形而上学导论》。先验批判/实践理性/判断力批判三大批判。1795年《道德形而上学基础》提出categorical imperative。1804年《人类理性限界的界限》提出全球伦理。结果：康德是先验批判/实践理性/批判哲学奠基者/现代哲学之父。"
    },
    "EU-DE-PHIL-002": {
        "name": "黑格尔：辩证法/历史哲学/绝对精神/逻辑学/体系构建者",
        "description": "黑格尔提出辩证法/历史哲学/绝对精神/逻辑学/体系构建者",
        "modes": [8, 6, 1, 5, 24],
        "reason": "黑格尔'辩证法'、'绝对精神'、'历史哲学'、'逻辑学'、'体系构建'，核心思维：辩证法方法论与历史哲学革命——辩证法/绝对精神/历史哲学/逻辑学/体系构建发展三大支柱，黑格尔成为客观唯心主义大师/历史哲学家。",
        "steps": [
            "第1步：抽象归纳法——辩证法创制：Thesis/Antithesis/Synthesis三段论，矛盾/对立/统一方法",
            "第2步：系统思维法——历史哲学方法论：绝对精神/历史哲学/辩证法/逻辑学/体系构建发展",
            "第3步：矛盾分析法——传统哲学危机：黑格尔/谢林/费希特局限/绝对精神"
        ],
        "expected": [
            "辩证法成现代哲学方法论基石/历史哲学/绝对精神/逻辑学/体系构建影响后世",
            "辩证法/绝对精神/历史哲学/逻辑学/体系构建发展三大支柱/影响现代哲学",
            "教训：客观唯心主义局限/辩证法被滥用/影响马克思主义"
        ],
        "case": "黑格尔一生：1770年出生斯图加特/1795年柏林大学博士/1800年《精神现象学》/1807年《逻辑学》/1816年《哲学全书》/1820年《法哲学》/1821年《历史哲学》/1831年《弟子讲义》。精神现象学/逻辑学/哲学全书三大体系。辩证法Thesis/Antithesis/Synthesis。绝对精神WeiSein/Dasein/Sein。结果：黑格尔是辩证法大师/客观唯心主义宗师/历史哲学家。"
    },
    "EU-DE-PHIL-003": {
        "name": "马克思：历史唯物主义/政治经济学/阶级斗争/唯物史观/社会革命理论者",
        "description": "马克思提出历史唯物主义/政治经济学/阶级斗争/唯物史观/社会革命理论者",
        "modes": [8, 6, 1, 5, 24],
        "reason": "马克思'历史唯物主义'、'政治经济学'、'阶级斗争'、'唯物史观'、'社会革命'，核心思维：唯物史观方法论与社会革命理论革命——历史唯物主义/政治经济学/阶级斗争/唯物史观/社会革命发展三大支柱，马克思成为现代社会主义奠基者/社会革命理论家。",
        "steps": [
            "第1步：抽象归纳法——唯物史观创制：经济基础/上层建筑/阶级斗争/社会革命/历史唯物主义",
            "第2步：系统思维法——政治经济学方法论：历史唯物主义/政治经济学/阶级斗争/唯物史观/社会革命发展",
            "第3步：矛盾分析法——传统哲学危机：形而上学/唯心主义/资产阶级思想"
        ],
        "expected": [
            "历史唯物主义成社会科学方法论基石/政治经济学/阶级斗争/唯物史观/社会革命影响后世",
            "历史唯物主义/政治经济学/阶级斗争/唯物史观/社会革命发展三大支柱/影响现代社会科学",
            "教训：历史唯物主义局限/经济决定论/阶级斗争被滥用"
        ],
        "case": "马克思一生：1818年出生特里尔/1841年《资本论》/1859年《政治经济学批判》/1867年《共产党宣言》/1871年《法兰西内战》/1875年《哥达纲领批判》/1883年去世。资本论/政治经济学批判/共产党宣言三大著作。历史唯物主义/政治经济学/阶级斗争/唯物史观/社会革命。结果：马克思是历史唯物主义/政治经济学/阶级斗争奠基者/现代社会主义之父。"
    },
    "EU-DE-PHIL-004": {
        "name": "海德格尔：存在论/现象学/技术哲学/此在/人的存在解读者",
        "description": "海德格尔提出存在论/现象学/技术哲学/此在/人的存在解读者",
        "modes": [8, 6, 1, 5, 24],
        "reason": "海德格尔'存在论'、'现象学'、'技术哲学'、'此在'、'人的存在'，核心思维：存在论/现象学/技术哲学/此在/人的存在解读革命——存在论/现象学/技术哲学/此在/人的存在解读发展三大支柱，海德格尔成为当代哲学大师/存在论家。",
        "steps": [
            "第1步：抽象归纳法——存在论创制：Dasein/Being/存在/此在/人的存在解读",
            "第2步：系统思维法——现象学方法论：存在论/现象学/技术哲学/此在/人的存在解读发展",
            "第3步：矛盾分析法——传统哲学危机：形而上学/实体论/人的存在"
        ],
        "expected": [
            "存在论/现象学成当代哲学方法论基石/技术哲学/此在/人的存在解读影响后世",
            "存在论/现象学/技术哲学/此在/人的存在解读发展三大支柱/影响当代哲学",
            "教训：存在论局限/技术哲学被滥用/黑格尔主义影响"
        ],
        "case": "海德格尔一生：1889年出生メッツ/1909年神学院毕业/1911年《论时间的本质》/1927年《存在与时间》/1935年《林中漫步》/1938年《论技术》/1941年《诗耶/诗》的赋/1945年《可能性的存在》/1956年《流动的诗篇》/1976年去世。存在与时间/林中漫步/论技术三大著作。存在论/现象学/技术哲学/此在/人的存在解读。结果：海德格尔是存在论/现象学/技术哲学奠基者/当代哲学大师。"
    }
}

# Add to existing scenarios
for code, data in new_additional.items():
    # Create English version with simpler naming
    if code.startswith('EU-DE-PHIL-'):
        phil_number = int(code.split('-')[2])  # Get number after EU-DE-PHIL
        if phil_number == 1:
            name_en = "Kant: Practical Reason/Moral Philosophy/A Priori Idealism/Critical Philosophy/Global Ethics"
        elif phil_number == 2:
            name_en = "Hegel: Dialectics/Historical Philosophy/Absolute Spirit/Logic/System Builder"
        elif phil_number == 3:
            name_en = "Marx: Historical Materialism/Political Economy/Class Struggle/Materialist Historiography/Social Revolution Theorist"
        elif phil_number == 4:
            name_en = "Heidegger: Existentialism/Phenomenology/Technology Philosophy/Dasein/Human Existence Interpreter"
        else:
            name_en = f"German Philosopher {phil_number}"
            
        scenarios_en[code] = {
            "name": name_en,
            "description": data["description"],
            "modes": data["modes"],
            "reason": data["reason"],
            "steps": data["steps"],
            "expected": data["expected"],
            "case": data["case"]
        }

# Add to Chinese scenarios
scenarios_zh.update(new_additional)

# Save updated scenarios
with open(base_path + '/scenarios_zh.json', 'w', encoding='utf-8') as f:
    json.dump(scenarios_zh, f, ensure_ascii=False, indent=2)

with open(base_path + '/scenarios_en.json', 'w', encoding='utf-8') as f:
    json.dump(scenarios_en, f, ensure_ascii=False, indent=2)

print(f"Added 4 more German philosophers: EU-DE-PHIL-001 to EU-DE-PHIL-004")
print(f"Total ZH scenarios now: {len(scenarios_zh)}")
print(f"Total EN scenarios now: {len(scenarios_en)}")