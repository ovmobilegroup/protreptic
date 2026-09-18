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

# 4 German theoretical figures - EU-DE-SCI
new_science = {
    "EU-DE-SCI-001": {
        "name": "爱因斯坦：相对论/理论物理/思想实验/全球影响力/现代物理学奠基者",
        "description": "爱因斯坦提出相对论/理论物理/思想实验/全球影响力/现代物理学奠基者",
        "modes": [9, 14, 11, 1, 25],
        "reason": "爱因斯坦'相对论'、'质能转换'、'光电效应'、'波粒二象性'、'不确定性原理'，核心思维：理论物理学方法论革命与现代科学范式转变——广义相对论重写时空观，狭义相对论挑战绝对时间/空间，光电效应开启量子时代，思维实验成为科学方法论新模式，理论物理学从宏观世界走向微观世界，成现代物理学奠基者。",
        "steps": [
            "第1步：抽象归纳法——相对论创制：从迈克尔逊-莫雷实验出发，提出光速不变，推导出时空新观念",
            "第2步：系统思维法——理论物理学方法论：突破经典力学框架，建立场论/量子论框架",
            "第3步：矛盾分析法——经典力学的危机：牛顿力学无法解释水星近日点/光行差/光电效应",
            "第4步：知行合一——科学方法论：思维实验/直观想象/数学推导三位一体，提出质能方程E=mc2",
            "第5步：蛰伏积势——全球影响力：布拉韦伊斯实验室/普林斯顿物理学系/原子弹顾问/诺贝尔物理学奖"
        ],
        "expected": [
            "相对论成现代物理学基石、颠覆了300年经典力学时空观",
            "量子力学/粒子物理学/宇宙学发展三个支柱/影响现代科技",
            "教训：政治动荡/犹太裔身份/语言障碍/早期职业不稳定影响成就"
        ],
        "case": "爱因斯坦一生两次欧洲旅程：1905年专利局职员/1914年普林斯顿物理学教授/1933年美国/纽黑文Princeton。1905年'奇迹之年'发表五篇文章：光电效应论文/布朗运动论文/相对论论文/质能转换论文/布索理论论文。1915年完成广义相对论。1919年英国日全食实验验证引力透镜。1932年《统一场论》出版。结果：爱因斯坦成为现代物理学奠基者/相对论英雄/科学普及者/和平主义者。"
    },
    "EU-DE-SCI-002": {
        "name": "普朗克：量子理论/理论物理/能量量子化/热力学/现代物理学奠基者",
        "description": "普朗克提出量子理论/理论物理/能量量子化/热力学/现代物理学奠基者",
        "modes": [9, 14, 11, 1, 25],
        "reason": "普朗克'量子化'、'能量离散性'、'黑体辐射定律'、'热力学第二定律'、'能量守恒'，核心思维：能量连续性向离散性的革命——普朗克1900年通过量子化手段解决黑体辐射问题，引入能量量子化概念，开启微观世界新纪元，量子力学从此诞生，现代物理学分为宏观经典/微观量子两大阵营，普朗克成为现代物理学奠基者。",
        "steps": [
            "第1步：抽象归纳法——量子化创制：从黑体辐射问题出发，提出能量E=hν，引入量子化概念",
            "第2步：系统思维法——理论物理学方法论：古典热力学/统计力学向量子统计学转变",
            "第3步：矛盾分析法——经典热力学局限：经典理论无法解释黑体辐射谱/维恩位移/瑞利-吉布斯危机",
            "第4步：知行合一——科学方法论：数学方法/实验验证/理论构建三位一体，完成黑体辐射定律",
            "第5步：蛰伏积势——量子力学发展：爱因斯坦光电效应/玻尔原子模型/德布罗意波/薛定谔方程"
        ],
        "expected": [
            "量子理论成为现代物理学基础、微观世界认识革命",
            "量子统计学/薛定谔方程/狄拉克理论发展三大支柱/量子科技影响",
            "教训：量子学说早期被忽视/20年才被广泛认可/两次诺贝尔奖/坚持科学真理"
        ],
        "case": "普朗克一生：1877年出生柏林/1894年柏林大学博士/1900年黑体辐射论文/1908年玻尔原子模型/1911年慕尼黑大学/1922年诺贝尔物理学奖。1900年'量子化'概念诞生/1904年发明频率ν/1905年提出能量量子化/1911年建立量子力学基础。1913年加入物理学会/1922年获诺贝尔奖/1938年退休/1947年逝世。普朗克实验室/普朗克研究所/普朗克量子光学研究所。结果：普朗克是量子理论之父/现代物理学奠基者/科学方法论典范。"
    },
    "EU-DE-SCI-003": {
        "name": "马克斯·玻尔扎诺：微积分/级数理论/极限论证/数学方法论/数学基础",
        "description": "马克斯·玻尔扎诺提出微积分/级数理论/极限论证/数学方法论/数学基础",
        "modes": [9, 14, 11, 1, 25],
        "reason": "马克斯·玻尔扎诺'严格数学化'、'实数理论'、'极限论证'、'微积分基础'、'数学基础'，核心思维：数学方法论革命与数学基础建设——严格定义实数/无穷/极限/连续，解决微积分概念模糊问题，建立现代数学基础，实分析/复分析/拓扑学/度量空间发展三大支柱，玻尔扎诺成为现代数学奠基者。",
        "steps": [
            "第1步：抽象归纳法——实数理论创制：严格定义实数/无穷/极限/连续，解决算术/代数/几何难题",
            "第2步：系统思维法——数学方法论：微积分/级数/函数论/方程论/拓扑学/度量空间发展",
            "第3步：矛盾分析法——数学危机：黎卡利/伯努利/柯西/魏尔斯特拉斯等方法混乱/概念模糊",
            "第4步：知行合一——数学基础：严格证明/逻辑推理/数学公理化三位一体，解决数学危机",
            "第5步：蛰伏积势——数学发展：黎卡利/柯西/魏尔斯特拉斯/庞加莱/希尔伯特/现代数学发展"
        ],
        "expected": [
            "实数论/微积分学成为现代数学基础/实分析/复分析/拓扑学发展三大支柱",
            "极限论证/严格数学化/数学方法论成数学教育标准/影响数学训练",
            "教训：学术孤立/贫困出身/健康问题/不被认可/坚持科学真理"
        ],
        "case": "玻尔扎诺一生：1791年出生托伦蒂/1809年维也纳大学博士/1815年《概率论新方法》/1826年《实数论》/1848年退休/1856年去世。1815年'严格概率论'、1826年'实数论'、1830年'严格微积分'建立。1848年科学院主席/1849年维也纳大学教授/1856年去世。玻尔扎诺-维达马克思主义/玻尔扎诺综合定理/玻尔扎诺不等式/玻尔扎诺-魏尔斯特拉斯定理。结果：玻尔扎诺是实分析/微积分学奠基者/数学方法论先驱/数学基础建设者。"
    },
    "EU-DE-SCI-004": {
        "name": "翁贝托·埃科：符号学/诠释学/百科全书式写作/符号人类学/人类学思想",
        "description": "翁贝托·埃科提出符号学/诠释学/百科全书式写作/符号人类学/人类学思想",
        "modes": [9, 14, 11, 1, 25],
        "reason": "翁贝托·埃科'符号人类学'、'诠释学'、'百科全书式写作'、'符号结构'、'意义生产'，核心思维：符号学方法论与人类学思想革命——符号学/结构主义/解构主义发展三大支柱，从符号/结构/意义到人类学思想/文化研究/符号人类学，埃科成为20世纪伟大的文化思想家/学者/作家。",
        "steps": [
            "第1步：抽象归纳法——符号学创制：从《考古学中的符号学》到《标志设计与符号学》",
            "第2步：系统思维法——诠释学方法论：结构主义/解构主义/现象学/符号人类学发展",
            "第3步：矛盾分析法——文化危机：工业化/现代化/符号危机/意义危机/文化危机",
            "第4步：知行合一——百科全书式写作：知识结构化/符号化/标准化/百科全书出版",
            "第5步：蛰伏积势——符号人类学发展：《论神话的起源》/《图画代码》/《符号人类学》/《历史中的符号学》"
        ],
        "expected": [
            "符号学/诠释学成现代人文科学三大支柱/影响文化研究/符号人类学",
            "百科全书式写作/符号人类学/符号结构成文化思想方法论标准/影响文学理论",
            "教训：学术多元化/跨学科融合/符号学发展/文化批评/学术影响"
        ],
        "case": "翁贝托·埃科一生：1924年出生都灵/1945年军校/1946年大学学习/1947年研究生/1959年《考古学中的符号学》/1964年《普通符号学》/1975年《符号人类学》/1980年《图画代码》/1984年《历史中的符号学》/1988年《七号星期五》/1994年《盗版者》/1999年去世。1935年《数据和符号》/1947年《文学的结构》/1959年《考古学中的符号学》/1964年《普通符号学》/1975年《符号人类学》/1980年《图画代码》/1984年《历史中的符号学》。结果：埃科是符号学之父/诠释学大师/符号人类学先驱/学者型小说家。"
    }
}

# Add to existing scenarios
for code, data in new_science.items():
    # Create English version with simpler naming
    if code.startswith('EU-DE-SCI-'):
        sci_number = int(code.split('-')[3])  # Get number after EU-DE-SCI-001
        if sci_number == 1:
            name_en = "Einstein: Relativity/Theoretical Physics/Thought Experiments/Global Influence/Founding Father of Modern Physics"
        elif sci_number == 2:
            name_en = "Planck: Quantum Theory/Theoretical Physics/Energy Quantization/Thermodynamics/Founding Father of Modern Physics"
        elif sci_number == 3:
            name_en = "Bolzano: Calculus/Sequence Theory/Limit Proofs/Mathematical Method/Founding Father of Modern Mathematics"
        elif sci_number == 4:
            name_en = "Eco: Semiotics/Interpretations/Encyclopedia-Style Writing/Symbolic Anthropology/Humanistic Thought"
        else:
            name_en = f"German Science Figure {sci_number}"
            
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
scenarios_zh.update(new_science)

# Save updated scenarios
with open(base_path + '/scenarios_zh.json', 'w', encoding='utf-8') as f:
    json.dump(scenarios_zh, f, ensure_ascii=False, indent=2)

with open(base_path + '/scenarios_en.json', 'w', encoding='utf-8') as f:
    json.dump(scenarios_en, f, ensure_ascii=False, indent=2)

print(f"Added 4 German science figures: EU-DE-SCI-001 to EU-DE-SCI-004")
print(f"Total ZH scenarios now: {len(scenarios_zh)}")
print(f"Total EN scenarios now: {len(scenarios_en)}")