import json

# Read existing modes_data.json
with open('/opt/data/workspace/Protreptic/tools/modes_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

zh_modes = data['zh']
en_modes = data['en']

# Add Central/Eastern Europe modes M520-M533
# Based on the scenarios that use these modes, I'll create appropriate entries

new_modes_zh = {
    "520": [
        "哈布斯堡帝国多民族治理/奥地利联邦制",
        "哈布斯堡王朝统治中欧多民族帝国，通过联邦制��调德/��/��/波/克等族群，最终解体为奥��二元君主制再演变为现代奥地利联邦。",
        "帝国��张→多族群平��→����/奥��折��→一战解体→现代联邦制",
        "哈布斯堡/奥地利/多民族/联邦制/奥��折��/德意志/马��尔/��克/加利西亚/帝国解体"
    ],
    "521": [
        "克雷姆斯基/奥地利社会民主/红色维也纳",
        "奥托·克雷姆斯基领导红色维也纳，建立市政住房/社会福利/工人教育体系，在法西斯��起前展示社会民主治理模式。",
        "社会民主党��政→市政改革→住房/福利/教育→奥法内战/多尔夫斯独裁→历史遗产",
        "克雷姆斯基/红色维也纳/奥地利社民党/市政住房/社会福利/工人运动/法西斯/多尔夫斯/希特勒"
    ],
    "522": [
        "杜福尔/瑞士联邦制/直接民主/中立/激进党",
        "吉约姆-亨利·杜福尔领导激进党建立瑞士联邦国家，确立直接民主/联邦制/武装中立三大支��，成为小国生存典范。",
        "激进党革命→1848联邦��法→直接民主→武装中立→工业化/金融中心",
        "杜福尔/瑞士/联邦制/直接民主/中立/激进党/��法/多语言/小国生存/阿尔��斯"
    ],
    "523": [
        "��南/红十字/日内瓦公约/人道法",
        "亨利·杜南目击索尔费里诺��状创立红十字会，推动首个日内瓦公约，��定现代国际人道法基��。",
        "目击战场→记��索尔费里诺→红十字创立→日内瓦公约→国际人道法体系",
        "杜南/红十字/日内瓦公约/人道法/索尔费里诺/诺贝尔和平奖/瑞士/国际组织"
    ],
    "524": [
        "皮埃特/阿��策尔/瑞士农民自治/直选",
        "阿��策尔内陆两半州保留中世纪兰茨格梅因德直选传统，皮埃特家族世代参与公民直接投票决策地方事务。",
        "中世纪共同体→兰茨格梅因德→直选传统→现代半州自治→直接民主活化石",
        "阿��策尔/瑞士/兰茨格梅因德/直选/农民自治/半州/中世纪/直接民主/传统"
    ],
    "525": [
        "古斯塔夫/瓦萨/瑞典独立/瓦萨王朝/宗教改革",
        "古斯塔夫·瓦萨领导瑞典脱离卡尔马联盟，建立瓦萨王朝，推行宗教改革没收教会财产��定国家财政。",
        "起义脱离联盟→加��建立王朝→宗教改革→教会财产国有→中央集权/波罗的海��权",
        "古斯塔夫·瓦萨/瑞典/瓦萨王朝/卡尔马联盟/宗教改革/路德宗/波罗的海/中央集权"
    ],
    "526": [
        "帕尔梅/瑞典福利模式/中立/社会民主",
        "奥洛夫·帕尔梅领导瑞典社会民主党建立全民福利国家，坚持冷战中立/反越战/反种族隔离，遇��成��。",
        "社会民主��政→全民福利→冷战中立/超级大国平��→国际道德权威→遇��未破",
        "帕尔梅/瑞典/福利国家/社会民主党/中立/冷战/越战/种族隔离/遇��/道德外交"
    ],
    "527": [
        "图林/��威石油基金/代际公平/主权财富",
        "��威建立政府��老基金（石油基金），将北海石油收益转化为代际公平的主权财富，伦理投资准则全球领先。",
        "北海石油发现→��绝荷兰病→基金建立→伦理准则→代际公平/全球最大主权基金",
        "��威/石油基金/主权财富/代际公平/伦理投资/北海/荷兰病/政府��老基金/NBIM"
    ],
    "528": [
        "拉脱维亚/波罗的海之路/歌唱革命/非暴力独立",
        "1989年波罗的海之路人��连接三国，拉脱维亚通过歌唱革命非暴力��复独立，展示文化��抗力量。",
        "苏联占领→歌唱革命→波罗的海之路→非暴力��抗→独立��复→欧盟/北约入盟",
        "拉脱维亚/波罗的海之路/歌唱革命/非暴力/独立/苏联/爱沙尼亚/立����/文化��抗"
    ],
    "529": [
        "立����/维��塔斯/立����大公国/东欧��权",
        "维��塔斯大公��张立����大公国至黑海，建立东欧最大中世纪国家，格伦瓦尔德战役击败条顿��士团。",
        "大公国��张→格伦瓦尔德胜利→黑海到波罗的海→波兰联合→俄罗斯压��/��分",
        "维��塔斯/立����/大公国/格伦瓦尔德/条顿��士团/波兰/黑海/东欧/中世纪��权/雅��隆"
    ],
    "530": [
        "胡斯/布拉格/宗教改革先��/��克民族主义",
        "��·胡斯在布拉格批判教会��败，引发胡斯战争，成为宗教改革先��和��克民族身份象征，最终被火刑。",
        "布拉格大学→批判��罪��→胡斯战争→火刑��道→路德继承/��克民族符号/新教先��",
        "胡斯/布拉格/宗教改革/胡斯战争/火刑/��克/民族主义/路德/新教/查理大学"
    ],
    "531": [
        "马萨里克/��克斯洛��克建国/小国外交/民主",
        "托马什·马萨里克一战中流亡��导建国，建立��克斯洛��克民主共和国，小国在大国����中坚持议会制。",
        "流亡��导→战后建国→民主��法→小国外交/大国平��→��尼黑背��/共产政变/天����离婚",
        "马萨里克/��克斯洛��克/建国/民主/小国外交/一战/��尼黑/天����革命/哈维尔"
    ],
    "532": [
        "哈维尔/天����革命/公民社会/真理生活",
        "瓦茨拉夫·哈维尔以剧作家身份领导天����革命，提出'真理生活'哲学，从��见者到总统实现非暴力政权交接。",
        "��见者/七七��章→天����革命→非暴力政权交接→总统/真理生活→��克分离/欧盟入盟",
        "哈维尔/天����革命/��克/公民社会/真理生活/��见者/七七��章/剧作家/总统/非暴力"
    ],
    "533": [
        "奥班/��牙利非自由民主/主权/欧盟博��",
        "维克托·奥班构建非自由民主模式，以国家主权对抗欧盟自由主义��序，控制��体/司法/NGO，成为民��主义标��。",
        "青年自由派→非自由民主转型→��法修改/��体控制→欧盟��突/资金��结→主权主义/民��样本",
        "奥班/��牙利/非自由民主/主权/欧盟/民��主义/��体控制/司法改革/基督教民主/青民盟"
    ]
}

new_modes_en = {
    "520": [
        "Habsburg Multi-Ethnic Governance/Austrian Federalism",
        "The Habsburg dynasty ruled a multi-ethnic Central European empire, balancing German/Hungarian/Czech/Polish/Croatian groups through federal compromise, culminating in Austro-Hungarian dual monarchy and modern Austrian federalism.",
        "Imperial expansion→multi-ethnic balance→Ausgleich compromise→WWI dissolution→modern federalism",
        "Habsburg/Austria/multi-ethnic/federalism/Ausgleich/German/Magyar/Czech/Galicia/imperial dissolution"
    ],
    "521": [
        "Kreisky/Austrian Social Democracy/Red Vienna",
        "Bruno Kreisky led Red Vienna, establishing municipal housing/social welfare/worker education system, demonstrating social democratic governance before fascist takeover.",
        "Social Democrats govern→municipal reform→housing/welfare/education→Austrian civil war/Dollfuss dictatorship→historical legacy",
        "Kreisky/Red Vienna/Austrian SPÖ/municipal housing/social welfare/labor movement/fascism/Dollfuss/Hitler"
    ],
    "522": [
        "Dufour/Swiss Federalism/Direct Democracy/Neutrality/Radical Party",
        "Guillaume-Henri Dufour led the Radical Party to establish the Swiss federal state, entrenching direct democracy/federalism/armed neutrality as three pillars of small-state survival.",
        "Radical revolution→1848 federal constitution→direct democracy→armed neutrality→industrialization/financial center",
        "Dufour/Switzerland/federalism/direct democracy/neutrality/Radical Party/constitution/multilingual/small-state survival/Alps"
    ],
    "523": [
        "Dunant/Red Cross/Geneva Conventions/Humanitarian Law",
        "Henry Dunant witnessed Solferino carnage, founded the Red Cross, drove the first Geneva Convention, laying foundations of modern international humanitarian law.",
        "Witnessed battlefield→Memory of Solferino→Red Cross founded→Geneva Conventions→international humanitarian law system",
        "Dunant/Red Cross/Geneva Conventions/humanitarian law/Solferino/Nobel Peace Prize/Switzerland/international organization"
    ],
    "524": [
        "Piet/Appenzell/Swiss Peasant Self-Governance/Direct Election",
        "Appenzell Innerrhoden preserves the medieval Landsgemeinde direct-election tradition, with the Piet family generations participating in citizen assemblies deciding local affairs.",
        "Medieval commune→Landsgemeinde→direct election tradition→modern half-canton autonomy→living fossil of direct democracy",
        "Appenzell/Switzerland/Landsgemeinde/direct election/peasant self-governance/half-canton/medieval/direct democracy/tradition"
    ],
    "525": [
        "Gustav Vasa/Swedish Independence/Vasa Dynasty/Reformation",
        "Gustav Vasa led Sweden out of the Kalmar Union, founded the Vasa Dynasty, implemented Reformation confiscating church lands to fund the state.",
        "Rebellion secedes union→coronation founds dynasty→Reformation→church lands nationalized→centralization/Baltic hegemony",
        "Gustav Vasa/Sweden/Vasa Dynasty/Kalmar Union/Reformation/Lutheranism/Baltic Sea/centralization"
    ],
    "526": [
        "Palme/Swedish Welfare Model/Neutrality/Social Democracy",
        "Olof Palme led Swedish Social Democrats to build universal welfare state, maintained Cold War neutrality/anti-Vietnam War/anti-apartheid, assassination remains unsolved.",
        "Social Democrats govern→universal welfare→Cold War neutrality/superpower balance→international moral authority→assassination unsolved",
        "Palme/Sweden/welfare state/Social Democrats/neutrality/Cold War/Vietnam/apartheid/assassination/moral diplomacy"
    ],
    "527": [
        "Thulin/Norwegian Oil Fund/Intergenerational Equity/Sovereign Wealth",
        "Norway established the Government Pension Fund (Oil Fund), converting North Sea oil revenues into intergenerational equity sovereign wealth, with world-leading ethical investment guidelines.",
        "North Sea oil discovered→reject Dutch disease→fund established→ethical guidelines→intergenerational equity/world's largest sovereign fund",
        "Norway/oil fund/sovereign wealth/intergenerational equity/ethical investment/North Sea/Dutch disease/GPFG/NBIM"
    ],
    "528": [
        "Latvia/Baltic Way/Singing Revolution/Nonviolent Independence",
        "1989 Baltic Way human chain linked three states, Latvia restored independence through nonviolent Singing Revolution, demonstrating power of cultural resistance.",
        "Soviet occupation→Singing Revolution→Baltic Way→nonviolent resistance→independence restored→EU/NATO accession",
        "Latvia/Baltic Way/Singing Revolution/nonviolence/independence/Soviet/Estonia/Lithuania/cultural resistance"
    ],
    "529": [
        "Lithuania/Vytautas/Grand Duchy/Eastern European Hegemony",
        "Grand Duke Vytautas expanded the Grand Duchy of Lithuania to the Black Sea, creating medieval Eastern Europe's largest state, defeating Teutonic Knights at Grunwald.",
        "Grand Duchy expansion→Grunwald victory→Baltic to Black Sea→Polish union→Russian compression/partitions",
        "Vytautas/Lithuania/Grand Duchy/Grunwald/Teutonic Knights/Poland/Black Sea/Eastern Europe/medieval hegemony/Jagiellonian"
    ],
    "530": [
        "Hus/Prague/Reformation Pioneer/Czech Nationalism",
        "Jan Hus at Prague criticized church corruption, sparked Hussite Wars, became Reformation pioneer and Czech national identity symbol, ultimately burned at stake.",
        "Prague University→critique indulgences→Hussite Wars→martyrdom by fire→Luther inherits/Czech national symbol/Protestant pioneer",
        "Hus/Prague/Reformation/Hussite Wars/martyrdom/Czech/nationalism/Luther/Protestant/Charles University"
    ],
    "531": [
        "Masaryk/Czechoslovakia Founding/Small State Diplomacy/Democracy",
        "Tomas Masaryk advocated statehood in WWI exile, founded democratic Czechoslovakia, small state maintained parliamentary democracy between great powers.",
        "Exile advocacy→postwar founding→democratic constitution→small state diplomacy/great power balance→Munich betrayal/communist coup/Velvet Divorce",
        "Masaryk/Czechoslovakia/founding/democracy/small state diplomacy/WWI/Munich/Velvet Revolution/Havel"
    ],
    "532": [
        "Havel/Velvet Revolution/Civil Society/Living in Truth",
        "Vaclav Havel led Velvet Revolution as playwright, articulated 'living in truth' philosophy, transitioned from dissident to president achieving nonviolent power transfer.",
        "Dissident/Charter 77→Velvet Revolution→nonviolent power transfer→president/Living in Truth→Czech split/EU accession",
        "Havel/Velvet Revolution/Czech/civil society/Living in Truth/dissident/Charter 77/playwright/president/nonviolence"
    ],
    "533": [
        "Orban/Hungary Illiberal Democracy/Sovereignty/EU Struggle",
        "Viktor Orban built illiberal democracy model, asserting national sovereignty against EU liberal order, controlling media/judiciary/NGOs, becoming populist benchmark.",
        "Youth liberal→illiberal democratic turn→constitutional changes/media control→EU conflict/funds freeze→sovereigntism/populist template",
        "Orban/Hungary/illiberal democracy/sovereignty/EU/populism/media control/judicial reform/Christian democracy/Fidesz"
    ]
}

# Add new modes
for k, v in new_modes_zh.items():
    zh_modes[k] = v
for k, v in new_modes_en.items():
    en_modes[k] = v

data['zh'] = zh_modes
data['en'] = en_modes

# Write back
with open('/opt/data/workspace/Protreptic/tools/modes_data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Added {len(new_modes_zh)} modes (M520-M533)")
print(f"ZH modes: {len(zh_modes)}, EN modes: {len(en_modes)}")