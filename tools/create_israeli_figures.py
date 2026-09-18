#!/usr/bin/env python3
import json
import os

def create_json_file(file_path, data):
    """Create a JSON file with proper formatting."""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Created {file_path}")

def create_israeli_figures():
    """Create 8 Jewish/Israeli figures for Phase 7 Batch 3."""
    base_path = "/opt/data/workspace/Protreptic/tools/json"
    
    # Define all 8 Israeli/Jewish figures
    israel_figures = [
        {
            "id": "IL-HAVR-001",
            "code": "IL-HAVR-001",
            "name_zh": "迈蒙尼德/拉希/托萨福特",
            "name_en": "Maimonides/Rashi/Tosafists",
            "core_mode": "塔木德辩证-核心",
            "wiki_id": "Q9568,Q11832,Q505",
            "nationality": "犹太",
            "civilization_sphere": "犹太",
            "time_period_standardized": "1135-1204",
            "primary_language": "拉丁语/希伯来语",
            "intellectual_tradition": "犹太神学，托斯塔法",
            "description_zh": "迈蒙尼德（1135-1204）是犹太教最伟大的哲学家和法学家，撰写了《米字塔》。拉希（1040-1105）是犹太圣经解释学先驱。托萨法特学者（12-13世纪）对托拉进行了重要注释。三者共同构成了犹太教的解释学传统。",
            "description_en": "Maimonides (1135-1204) was one of the greatest Jewish philosophers and codifiers of Jewish law, author of the Mishneh Torah. Rashi (1040-1105) was the preeminent medieval commentator on the Torah and Talmud. The Tosafists (12th-13th centuries) were medieval Talmudists who produced important commentaries. Together they formed the foundation of Jewish textual interpretation.",
            "reason_zh": "核心思维：150(塔木德辩证-核心)、69(文献比较)、12(系统思维)、58(实验验证/医学哲学)。迈蒙尼德/拉希/托萨福特共同体现了塔木德辩证的核心精神，推动了犹太教的系统化发展。",
            "reason_en": "Core thinking modes: 150(Talmudic Dialectics - Core), 69(Literary Comparison), 12(Systematic Thinking), 58(Experimental Verification/Medical Philosophy). Maimonides/Rashi/Tosafists together embody the core spirit of Talmudic dialectics, promoting the systematization of Jewish thought.",
            "modes": [150, 69, 12, 58],
            "steps_zh": [
                "第1步：系统思维法——建立犹太教体系：迈蒙尼德建立法律体系，拉希建立解释体系，托萨福特建立注释体系",
                "第2步：文献比较法——跨文献比较：比较托拉、塔木德、吉索等文本",
                "第3步：实验验证法——实践验证：验证法律解释的实践效果",
                "第4步：塔木德辩证法——辩证思维：使用辩证法解决法律问题"
            ],
            "steps_en": [
                "Step 1: System Thinking Method - Build Jewish system: Maimonides establishes legal system, Rashi establishes interpretive system, Tosafists establishes commentary system",
                "Step 2: Literature Comparison Method - Cross-document comparison: Compare Torah, Talmud, Gemara etc. texts",
                "Step 3: Experimental Verification Method - Practice verification: Verify legal interpretation practical effects",
                "Step 4: Talmudic Dialectics - Dialectical thinking: Use dialectical method to solve legal problems"
            ],
            "expected_zh": [
                "建立完整的犹太教法律体系",
                "完善犹太教解释学传统",
                "推动犹太教的长期发展"
            ],
            "expected_en": [
                "Establish complete Jewish legal system",
                "Perfect Jewish hermeneutic tradition",
                "Promote long-term development of Judaism"
            ],
            "case_zh": "迈蒙尼德撰写《米字塔》，成为犹太法律权威。拉希的注释成为犹太教文本解释的标准。托萨法特学者的注释丰富了犹太教的文本理解。 三者共同构成了犹太教的解释学传统。",
            "case_en": "Maimonides authored Mishneh Torah, becoming the authority on Jewish law. Rashi's commentaries became the standard for Jewish text interpretation. The Tosafists' commentaries enriched Jewish textual understanding. Together they formed the foundation of Jewish hermeneutics.",
            "era": "1135-1204",
            "historical_domains": ["神学", "法学", "哲学"],
            "domains": ["协作", "系统", "分析", "创意", "运营"],
            "gender": "男",
            "ethnicity": "犹太"
        },
        {
            "id": "IL-ZION-001",
            "code": "IL-ZION-001",
            "name_zh": "赫茨尔/本-古里安",
            "name_en": "Herzl/Ben-Gurion",
            "core_mode": "战略预判",
            "wiki_id": "Q80444,Q10037",
            "nationality": "以色列",
            "civilization_sphere": "犹太",
            "time_period_standardized": "1860-1973",
            "primary_language": "希伯来语/英语",
            "intellectual_tradition": "犹太复国主义，民族主义",
            "description_zh": "赫茨尔是现代犹太复国主义之父，撰写了《犹太国家》。本-古里安是以色列第一任总理，领导以色列建国和国防建设。两人共同推动了现代以色列国家的建立和犹太复国主义的实现。",
            "description_en": "Herzl was the father of modern political Zionism, author of \"Der Judenstaat\" (The Jewish State). Ben-Gurion was Israel's first Prime Minister, leading the establishment of the State of Israel and its defense. Together they promoted the creation of modern Israel and the realization of Zionist ideals.",
            "reason_zh": "核心思维：1(战略预判)、67(战略敏捷)、37(知行合一)、153(儒商传承/民族建设)。赫茨尔和本-古里安共同体现了战略预判和知行合一的精神，推动了犹太民族的建国大业。",
            "reason_en": "Core thinking modes: 1(Strategic Foresight), 67(Strategic Agility), 37(Know-Act Integration), 153(Ju-Shang Inheritance/Nation Building). Herzl and Ben-Gurion together embody the spirit of strategic foresight and know-act integration, promoting the Jewish national renaissance.",
            "modes": [1, 67, 37, 153],
            "steps_zh": [
                "第1步：战略预判法——制定建国大计：赫茨尔预判犹太复国主义需求，本-古里安预判以色列国防需求",
                "第2步：战略敏捷法——灵活应对：赫茨尔通过政治活动建国，本-古里安通过军事行动捍卫国家",
                "第3步：知行合一——实施建国战略：赫茨尔的政治努力，本-古里安的建国实践",
                "第4步：儒商传承——民族建设：继承民族智慧，建设现代国家",
                "第5步：长期主义——维护国家：确保以色列的长期发展和安全"
            ],
            "steps_en": [
                "Step 1: Strategic Foresight - Formulate national plan: Herzl anticipates Zionist needs, Ben-Gurion anticipates Israel defense needs",
                "Step 2: Strategic Agility - Flexible response: Herzl promotes nation through political activities, Ben-Gurion defends nation through military actions",
                "Step 3: Know-Act Integration - Implement nation-building strategy: Herzl's political efforts, Ben-Gurion's nation-building practice",
                "Step 4: Ju-Shang Inheritance - National construction: Inherit national wisdom, build modern nation",
                "Step 5: Long-termism - Maintain nation: Ensure Israel's long-term development and security"
            ],
            "expected_zh": [
                "建立现代以色列国家，实现犹太复国主义",
                "建立强大的国防体系，确保国家安全",
                "推动犹太民族的复兴和民族复兴"
            ],
            "expected_en": [
                "Establish modern State of Israel, realize Zionist dream",
                "Build strong defense system, ensure national security",
                "Promote Jewish national revival and national renaissance"
            ],
            "case_zh": "赫茨尔通过《犹太国家》一书，推动了犹太复国主义运动。 本-古里安领导以色列建国，制定了国家的基本政策。 两人共同推动了现代以色列的建立和犹太民族的复兴。",
            "case_en": "Herzl promoted the Zionist movement through \"Der Judenstaat\". Ben-Gurion led the establishment of the State of Israel and formulated its basic policies. Together they promoted the establishment of modern Israel and Jewish national revival.",
            "era": "1860-1973",
            "historical_domains": ["政治", "民族", "建国"],
            "domains": ["协作", "系统", "分析", "创意", "运营"],
            "gender": "男",
            "ethnicity": "以色列"
        },
        {
            "id": "IL-SCI-001",
            "code": "IL-SCI-001",
            "name_zh": "爱因斯坦/奥本海默/费曼",
            "name_en": "Einstein/Oppenheimer/Feynman",
            "core_mode": "塔木德辩证/物理直觉",
            "wiki_id": "Q2254,Q565,Q1471",
            "nationality": "美国",
            "civilization_sphere": "欧美国",
            "time_period_standardized": "1879-1955",
            "primary_language": "德语/英语",
            "intellectual_tradition": "物理学，量子力学",
            "description_zh": "爱因斯坦创立相对论，奥本海默领导曼哈顿计划，费曼发展量子电动力学。三者共同推动了现代物理学的发展。",
            "description_en": "Einstein founded relativity theory, Oppenheimer led Manhattan Project, Feynman developed quantum electrodynamics. Together they promoted modern physics development.",
            "reason_zh": "核心思维：150(塔木德辩证/物理直觉)、58(实验验证)、23(创新思维)、158(通才整合/费曼)",
            "reason_en": "Core thinking modes: 150(Talmudic Dialectics/Physics Intuition), 58(Experimental Verification), 23(Innovation Thinking), 158(Generalist Integration/Feynman)",
            "modes": [150, 58, 23, 158],
            "steps_zh": [
                "第1步：系统思维法——物理理论体系：爱因斯坦建立相对论，奥本海默建立核物理体系，费曼建立量子电动力学",
                "第2步：实验验证法——理论验证：验证相对论的实验效果，验证核裂变的实验效果，验证量子电动力学的实验效果",
                "第3步：创新思维法——理论创新：爱因斯坦创新相对论，奥本海默创新核武器，费曼创新量子电动力学",
                "第4步：通才整合法——多学科融合：整合物理学、化学、工程学"
            ],
            "steps_en": [
                "Step 1: System Thinking Method - Physics theory system: Einstein establishes relativity theory, Oppenheimer establishes nuclear physics system, Feynman establishes quantum electrodynamics",
                "Step 2: Experimental Verification Method - Theory verification: Verify relativity theory experimental effects, verify nuclear fission experimental effects, verify quantum electrodynamics experimental effects",
                "Step 3: Innovation Thinking Method - Theory innovation: Einstein innovates relativity theory, Oppenheimer innovates nuclear weapons, Feynman innovates quantum electrodynamics",
                "Step 4: Generalist Integration Method - Multi-disciplinary integration: Integrate physics, chemistry, engineering"
            ],
            "expected_zh": [
                "建立现代物理学理论体系",
                "推动核物理学发展",
                "促进量子力学发展"
            ],
            "expected_en": [
                "Establish modern physics theoretical system",
                "Promote nuclear physics development",
                "Promote quantum mechanics development"
            ],
            "case_zh": "爱因斯坦创立相对论，奥本海默领导曼哈顿计划，费曼发展量子电动力学。三者共同推动了现代物理学的发展。",
            "case_en": "Einstein founded relativity theory, Oppenheimer led Manhattan Project, Feynman developed quantum electrodynamics. Together they promoted modern physics development.",
            "era": "1879-1955",
            "historical_domains": ["物理", "核", "量子"],
            "domains": ["协作", "系统", "分析", "创意", "运营"],
            "gender": "男/男/男",
            "ethnicity": "美国"
        },
        {
            "id": "IL-PSY-001",
            "code": "IL-PSY-001",
            "name_zh": "弗洛伊德/弗兰克尔/卡尼曼",
            "name_en": "Freud/Erickson/Cannon",
            "core_mode": "塔木德辩证/精神分析",
            "wiki_id": "Q1026,Q83554,Q36323",
            "nationality": "奥地利/美国",
            "civilization_sphere": "欧美国",
            "time_period_standardized": "1856-1939,1890-1980,1871-1945",
            "primary_language": "德语/英语",
            "intellectual_tradition": "精神分析，存在主义心理学，人本主义心理学",
            "description_zh": "弗洛伊德创立精神分析，弗兰克尔创立存在主义心理学，卡尼曼创立现代认知心理学。三者共同推动了心理学的发展。",
            "description_en": "Freud founded psychoanalysis, Frankl founded existential psychology, Cannon founded modern cognitive psychology. Together they promoted psychological development.",
            "reason_zh": "核心思维：150(塔木德辩证/精神分析)、27(双系统/卡尼曼)、30(认知偏差)、63(学科建设/心理学)",
            "reason_en": "Core thinking modes: 150(Talmudic Dialectics/Psychoanalysis), 27(Dual System/Cannon), 30(Cognitive Bias), 63(Discipline Construction/Psychology)",
            "modes": [150, 27, 30, 63],
            "steps_zh": [
                "第1步：系统思维法——心理学体系：弗洛伊德建立精神分析体系，弗兰克尔建立存在主义心理学体系，卡尼曼建立认知心理学体系",
                "第2步：实验验证法——理论验证：验证精神分析的实验效果，验证存在主义心理学的实验效果，验证认知心理学的实验效果",
                "第3步：认知偏差法——偏差识别：识别精神分析中的认知偏差，识别存在主义心理学中的认知偏差，识别认知心理学中的认知偏差",
                "第4步：学科建设法——学科发展：建立精神病学学科，建立存在主义心理学学科，建立认知心理学学科"
            ],
            "steps_en": [
                "Step 1: System Thinking Method - Psychology system: Freud establishes psychoanalysis system, Frankl establishes existential psychology system, Cannon establishes cognitive psychology system",
                "Step 2: Experimental Verification Method - Theory verification: Verify psychoanalysis experimental effects, verify existential psychology experimental effects, verify cognitive psychology experimental effects",
                "Step 3: Cognitive Bias Recognition Method - Bias recognition: Recognize cognitive biases in psychoanalysis, recognize cognitive biases in existential psychology, recognize cognitive biases in cognitive psychology",
                "Step 4: Discipline Construction Method - Discipline development: Establish psychiatry discipline, establish existential psychology discipline, establish cognitive psychology discipline"
            ],
            "expected_zh": [
                "建立完整的心理学理论体系",
                "推动心理学的学科建设",
                "促进心理学的长期发展"
            ],
            "expected_en": [
                "Establish complete psychology theoretical system",
                "Promote psychology discipline construction",
                "Promote long-term development of psychology"
            ],
            "case_zh": "弗洛伊德创立精神分析，弗兰克尔创立存在主义心理学，卡尼曼创立现代认知心理学。三者共同推动了心理学的发展。",
            "case_en": "Freud founded psychoanalysis, Frankl founded existential psychology, Cannon founded modern cognitive psychology. Together they promoted psychological development.",
            "era": "1856-1939,1890-1980,1871-1945",
            "historical_domains": ["心理", "精神", "认知"],
            "domains": ["协作", "系统", "分析", "创意", "运营"],
            "gender": "男/男/男",
            "ethnicity": "奥地利/美国"
        },
        {
            "id": "IL-TECH-001",
            "code": "IL-TECH-001",
            "name_zh": "摩尔/埃利森/瓦滕伯格",
            "name_en": "Moore/Ellis/Wattenberg",
            "core_mode": "自主研发/芯片/数据库",
            "wiki_id": "Q9686,Q895,Q491063",
            "nationality": "美国",
            "civilization_sphere": "欧美国",
            "time_period_standardized": "1929-2023,1929-2022,1950-至今",
            "primary_language": "英语",
            "intellectual_tradition": "计算机科学，数据库系统，芯片设计",
            "description_zh": "摩尔提出摩尔定律，埃利森创立数据库系统，瓦滕伯格创立大数据分析平台。三者共同推动了计算机科学的发展。",
            "description_en": "Moore proposed Moore's Law, Ellis established database system, Wattenberg founded big data analysis platform. Together they promoted computer science development.",
            "reason_zh": "核心思维：51(自主研发/芯片/数据库)、67(战略敏捷)、47(价值对话/商业生态)",
            "reason_en": "Core thinking modes: 51(Autonomous Research/Chip/Database), 67(Strategic Agility), 47(Value Dialogue/Business Ecosystem)",
            "modes": [51, 67, 47],
            "steps_zh": [
                "第1步：自主研发法——技术创新：摩尔创新芯片设计，埃利森创新数据库系统，瓦滕伯格创新大数据分析平台",
                "第2步：灵活策略法——商业模式创新：摩尔建立芯片公司，埃利森建立数据库公司，瓦滕伯格建立大数据公司",
                "第3步：价值对话法——用户共创：数据库用户参与设计，大数据用户参与优化，芯片用户参与测试"
            ],
            "steps_en": [
                "Step 1: Autonomous Research Method - Technological Innovation: Moore innovates chip design, Ellis innovates database system, Wattenberg innovates big data analysis platform",
                "Step 2: Flexible Strategy Method - Business Model Innovation: Moore establishes chip company, Ellis establishes database company, Wattenberg establishes big data company",
                "Step 3: Value Dialogue Method - User Co-creation: Database users participate in design, big data users participate in optimization, chip users participate in testing"
            ],
            "expected_zh": [
                "建立自主创新的技术生态系统",
                "推动计算机科学发展",
                "促进技术商业化"
            ],
            "expected_en": [
                "Establish autonomous innovation technology ecosystem",
                "Promote computer science development",
                "Promote technology commercialization"
            ],
            "case_zh": "摩尔提出摩尔定律，埃利森创立数据库系统，瓦滕伯格创立大数据分析平台。三者共同推动了计算机科学的发展。",
            "case_en": "Moore proposed Moore's Law, Ellis established database system, Wattenberg founded big data analysis platform. Together they promoted computer science development.",
            "era": "1929-2023,1929-2022,1950-至今",
            "historical_domains": ["计算机", "数据库", "大数据"],
            "domains": ["协作", "系统", "分析", "创意", "运营"],
            "gender": "男/男/男",
            "ethnicity": "美国"
        },
        {
            "id": "IL-MIL-001",
            "code": "IL-MIL-001",
            "name_zh": "达扬/拉宾/内塔尼亚胡",
            "name_en": "Dayan/Rabin/Netanyahu",
            "core_mode": "战略预判",
            "wiki_id": "Q622,Q652,Q3394",
            "nationality": "以色列",
            "civilization_sphere": "犹太",
            "time_period_standardized": "1915-1976,1922-1995,1949-至今",
            "primary_language": "希伯来语/英语",
            "intellectual_tradition": "军事战略，外交，政治",
            "description_zh": "达扬是著名的军事战略家，拉宾是前总理，内塔尼亚胡是现任总理。三者共同推动了以色列的国防建设。",
            "description_en": "Dayan is famous military strategist, Rabin was former Prime Minister, Netanyahu is current Prime Minister. Together they promoted Israel's defense construction.",
            "reason_zh": "核心思维：1(战略预判)、20(博弈论)、40(三衙分兵/军政分离)、67(战略敏捷)",
            "reason_en": "Core thinking modes: 1(Strategic Foresight), 20(Game Theory), 40(Three-gate Separation/Military-Civilian Separation), 67(Strategic Agility)",
            "modes": [1, 20, 40, 67],
            "steps_zh": [
                "第1步：战略预判法——国防建设：达扬预判军事需求，拉宾预判外交需求，内塔尼亚胡预判政治需求",
                "第2步：博弈论法——策略博弈：达扬进行军事博弈，拉宾进行外交博弈，内塔尼亚胡进行政治博弈",
                "第3步：三衙分兵法——军政分离：达扬负责军事，拉宾负责外交，内塔尼亚胡负责政治",
                "第4步：战略敏捷法——灵活应对：达扬灵活应对军事挑战，拉宾灵活应对外交挑战，内塔尼亚胡灵活应对政治挑战"
            ],
            "steps_en": [
                "Step 1: Strategic Foresight - Defense construction: Dayan anticipates military needs, Rabin anticipates diplomatic needs, Netanyahu anticipates political needs",
                "Step 2: Game Theory Method - Strategic game: Dayan conducts military game, Rabin conducts diplomatic game, Netanyahu conducts political game",
                "Step 3: Three-gate Separation Method - Military-civilian separation: Dayan responsible for military, Rabin responsible for diplomacy, Netanyahu responsible for politics",
                "Step 4: Strategic Agility Method - Flexible response: Dayan flexibly responds to military challenges, Rabin flexibly responds to diplomatic challenges, Netanyahu flexibly responds to political challenges"
            ],
            "expected_zh": [
                "建立强大的国防体系",
                "推动外交建设",
                "促进政治建设"
            ],
            "expected_en": [
                "Build strong defense system",
                "Promote diplomatic construction",
                "Promote political construction"
            ],
            "case_zh": "达扬是著名的军事战略家，拉宾是前总理，内塔尼亚胡是现任总理。三者共同推动了以色列的国防建设。",
            "case_en": "Dayan is famous military strategist, Rabin was former Prime Minister, Netanyahu is current Prime Minister. Together they promoted Israel's defense construction.",
            "era": "1915-1976,1922-1995,1949-至今",
            "historical_domains": ["军事", "外交", "政治"],
            "domains": ["协作", "系统", "分析", "创意", "运营"],
            "gender": "男/男/男",
            "ethnicity": "以色列"
        },
        {
            "id": "IL-LIT-001",
            "code": "IL-LIT-001",
            "name_zh": "阿格农/奥兹/格罗斯曼",
            "name_en": "Agnon/Oz/Grossman",
            "core_mode": "魔幻现实/犹太叙事",
            "wiki_id": "Q144,Q138535,Q78378",
            "nationality": "以色列",
            "civilization_sphere": "犹太",
            "time_period_standardized": "1888-1970,1913-1999,1926-至今",
            "primary_language": "希伯来语/英语",
            "intellectual_tradition": "文学，叙事，魔幻现实主义",
            "description_zh": "阿格农是诺贝尔文学奖得主，奥兹是著名作家，格罗斯曼是当代小说家。三者共同推动了犹太文学的发展。",
            "description_en": "Agnon is Nobel laureate in literature, Oz is famous writer, Grossman is contemporary novelist. Together they promoted Jewish literary development.",
            "reason_zh": "核心思维：155(魔幻现实/犹太叙事)、150(塔木德辩证/文本解读)、62(学术艺术融通)",
            "reason_en": "Core thinking modes: 155(Magical Realism/Jewish Narrative), 150(Talmudic Dialectics/Text Interpretation), 62(Academic Art Integration)",
            "modes": [155, 150, 62],
            "steps_zh": [
                "第1步：系统思维法——文学体系：阿格农建立叙事体系，奥兹建立魔幻现实主义体系，格罗斯曼建立当代小说体系",
                "第2步：塔木德辩证法——文本解读：阿格农解读文本，奥兹解读文本，格罗斯曼解读文本",
                "第3步：学术艺术融通法——艺术融合：阿格农融合文学与哲学，奥兹融合文学与历史，格罗斯曼融合文学与社会"
            ],
            "steps_en": [
                "Step 1: System Thinking Method - Literary system: Agnon establishes narrative system, Oz establishes magical realism system, Grossman establishes contemporary novel system",
                "Step 2: Talmudic Dialectics Method - Text interpretation: Agnon interprets text, Oz interprets text, Grossman interprets text",
                "Step 3: Academic Art Integration Method - Art integration: Agnon integrates literature with philosophy, Oz integrates literature with history, Grossman integrates literature with society"
            ],
            "expected_zh": [
                "建立完整的文学体系",
                "推动魔幻现实主义发展",
                "促进犹太文学发展"
            ],
            "expected_en": [
                "Establish complete literary system",
                "Promote magical realism development",
                "Promote Jewish literary development"
            ],
            "case_zh": "阿格农是诺贝尔文学奖得主，奥兹是著名作家，格罗斯曼是当代小说家。三者共同推动了犹太文学的发展。",
            "case_en": "Agnon is Nobel laureate in literature, Oz is famous writer, Grossman is contemporary novelist. Together they promoted Jewish literary development.",
            "era": "1888-1970,1913-1999,1926-至今",
            "historical_domains": ["文学", "叙事", "魔幻现实主义"],
            "domains": ["协作", "系统", "分析", "创意", "运营"],
            "gender": "男/男/男",
            "ethnicity": "以色列"
        },
        {
            "id": "IL-DIAS-001",
            "code": "IL-DIAS-001",
            "name_zh": "斯皮诺萨/马克思/阿伦特",
            "name_en": "Spinoza/Marx/Arendt",
            "core_mode": "塔木德辩证/哲学",
            "wiki_id": "Q1153,Q1549,Q2237",
            "nationality": "国际",
            "civilization_sphere": "世界",
            "time_period_standardized": "1632-1677,1818-1883,1906-1975",
            "primary_language": "拉丁语/德语/英语",
            "intellectual_tradition": "哲学，政治学，社会学",
            "description_zh": "斯皮诺萨是理性主义哲学家，马克思是政治经济学家，阿伦特是政治哲学家。三者共同推动了哲学和社会科学的发展。",
            "description_en": "Spinoza is rationalist philosopher, Marx is political economist, Arendt is political philosopher. Together they promoted philosophy and social science development.",
            "reason_zh": "核心思维：150(塔木德辩证/哲学)、153(儒商传承/流散智慧)、54(文明史观)",
            "reason_en": "Core thinking modes: 150(Talmudic Dialectics/Philosophy), 153(Ju-Shang Inheritance/Diaspora Wisdom), 54(Civilization History View)",
            "modes": [150, 153, 54],
            "steps_zh": [
                "第1步：系统思维法——哲学体系：斯皮诺萨建立理性主义哲学，马克思建立政治经济学，阿伦特建立政治哲学",
                "第2步：塔木德辩证法——哲学辩证：斯皮诺萨进行哲学辩证，马克思进行政治辩证，阿伦特进行社会辩证",
                "第3步：儒商传承法——智慧传承：斯皮诺萨传承智慧，马克思传承智慧，阿伦特传承智慧"
            ],
            "steps_en": [
                "Step 1: Systems Thinking Method - Philosophy system: Spinoza establishes rationalist philosophy, Marx establishes political economy, Arendt establishes political philosophy",
                "Step 2: Talmudic Dialectics Method - Philosophy dialectic: Spinoza conducts philosophy dialectic, Marx conducts political dialectic, Arendt conducts social dialectic",
                "Step 3: Ju-Shang Inheritance Method - Wisdom inheritance: Spinoza inherits wisdom, Marx inherits wisdom, Arendt inherits wisdom"
            ],
            "expected_zh": [
                "建立完整的哲学体系",
                "推动政治经济学发展",
                "促进社会科学发展"
            ],
            "expected_en": [
                "Establish complete philosophy system",
                "Promote political economy development",
                "Promote social science development"
            ],
            "case_zh": "斯皮诺萨是理性主义哲学家，马克思是政治经济学家，阿伦特是政治哲学家。三者共同推动了哲学和社会科学的发展。",
            "case_en": "Spinoza is rationalist philosopher, Marx is political economist, Arendt is political philosopher. Together they promoted philosophy and social science development.",
            "era": "1632-1677,1818-1883,1906-1975",
            "historical_domains": ["哲学", "政治学", "社会学"],
            "domains": ["协作", "系统", "分析", "创意", "运营"],
            "gender": "男/男/女",
            "ethnicity": "国际"
        }
    ]
    
    # Create IL directory
    il_dir = f"{base_path}/IL"
    os.makedirs(il_dir, exist_ok=True)
    
    for figure in israel_figures:
        file_path = f"{il_dir}/{figure['code']}.json"
        create_json_file(file_path, figure)

if __name__ == "__main__":
    print("Creating 8 Israeli/Jewish figures for Phase 7 Batch 3...")
    create_israeli_figures()
    print("All 8 Israeli/Jewish figures created successfully!")