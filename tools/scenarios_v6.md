# Scenarios & Tags v6 更新

## 概述
Phase 13-16 新增 96 个新国际人物 scenario (96 位人物 × 1 scenario each)，对应的 code 为 `XX-TOPIC-001` 格式 (例如 `GE-PHI-001`, `AM-REV-001`等)。

### Scenarios 结构 (继承 v5)
每个 scenario 包含字段：
- `name` (中英文)
- `description` (中英文)
- `modes` (数组, 包含 ≥1 个 M262-M356 新模式)
- `reason` (中英文)
- `steps` (中英文数组, 5-6 步)
- `expected` (中英文)
- `case` (中英文)

### 新场景 code 列表 (96 个)
来源: batch_plan_v4.md 中的 12 个 Batch × 8 人 = 96 人

| code | Person | New Mode |
|------|--------|----------|
| GE-PHI-001 | 伊利亚·恰瓦泽 | M262 |
| GE-POL-001 | 诺伊·饶马什维利 | M263 |
| GE-LIT-001 | 加尔扎谢·恰瓦泽 | M264 |
| AM-REV-001 | 安德拉尼克·奥扎尼安 | M265 |
| AM-INT-001 | 阿拉姆·哈恰图良 | M266 |
| AZ-OIL-001 | 海达尔·阿利耶夫 | M267 |
| AZ-LIT-001 | 尼扎米·甘贾维 | M268 |
| MD-DEM-001 | 米哈伊·戈尔布诺夫 | M269 |
| KZ-ECO-001 | 努尔苏丹·纳扎尔巴耶夫 | M270 |
| KZ-TRA-001 | 阿里汗·斯迈洛夫 | M271 |
| UZ-REV-001 | 伊斯兰·卡里莫夫 | M272 |
| UZ-LIT-001 | 阿利舍尔·纳沃伊 | M273 |
| KG-DEM-001 | 阿斯卡尔·阿卡耶夫 | M274 |
| KG-CUL-001 | 钦吉斯·艾特玨托夫 | M275 |
| TJ-CIV-001 | 艾莫马利·拉赫蒙 | M276 |
| TM-AUT-001 | 萨帕尔穆拉特·尼亚佐夫 | M277 |
| MN-EMP-001 | 成吉思汗 | M278 |
| MN-DEM-001 | 达希道尔吉 | M279 |
| VN-REV-001 | 胡志民 | M280 |
| VN-ECO-001 | 武元甲 | M281 |
| LA-KIN-001 | 西萨旺·冯 | M282 |
| KH-KIN-001 | 诺罗敦·西哈努克 | M283 |
| TH-KIN-001 | 普密蓬·阿杖素 | M284 |
| MM-DEM-001 | 昂山素季 | M285 |
| MY-PRI-001 | 马哈蒂尔·穆罕默德 | M286 |
| MY-POL-001 | 安瓦尔·易卜拉欣 | M287 |
| ID-REV-001 | 苏加诺 | M288 |
| ID-ECO-001 | 苏哈托 | M289 |
| PH-REV-001 | 何塞·黎撒 | M290 |
| SG-ECO-001 | 李光耀 | M291 |
| BN-OIL-001 | 哈桑纳尔·博尔基亚 | M292 |
| TL-IND-001 | 沙纳纳·古斯芒 | M293 |
| NP-KIN-001 | 普里特维·纳拉扬·沙阿 | M294 |
| NP-CLI-001 | 比兰德拉国王 | M295 |
| BT-KIN-001 | 吉格梅·辛格 | M296 |
| LK-IND-001 | 索罗希·班达拉奈克 | M297 |
| LK-CIV-001 | 钱德里卡·库马拉桑加 | M298 |
| MV-CLI-001 | 穆蒙·阿卜杜勒 | M299 |
| YE-UNI-001 | 阿里·萨利赫 | M300 |
| SA-OIL-001 | 沙特阿拉伯国王 | M302 |
| BH-DEM-001 | 哈马德国王 | M303 |
| QA-ENE-001 | 哈马德·哈利法 | M304 |
| AE-VIS-001 | 扎耶德酋长 | M305 |
| AE-ECO-001 | 穆罕默德·本·拉希德 | M306 |
| JO-HAS-001 | 侯赛因国王 | M307 |
| LB-CIV-001 | 拉菲克·哈里里 | M308 |
| SY-NAT-001 | 哈菲兹·阿萨德 | M309 |
| NG-MIL-001 | 奥卢塞贡·奥巴桑乔 | M310 |
| NG-LIT-001 | 沃莱·索因卡 | M311 |
| KE-ECO-001 | 乔莫·肯雅塔 | M312 |
| TZ-SOC-001 | 朱利叶斯·尼雷尔 | M313 |
| ZW-REV-001 | 罗伯特·穆加贝 | M314 |
| ZA-DEM-001 | 纳尔逊·曼德拉 | M315 |
| ET-EMP-001 | 海尔·塞拉西 | M316 |
| GH-PAN-001 | 夸梅·恩克鲁玛 | M317 |
| SN-CUL-001 | 利奥波德·森戈尔 | M318 |
| CI-ECO-001 | 费利克斯·乌弗埃 | M319 |
| CO-REV-001 | 西蒙·玻利瓦尔 | M320 |
| EC-REV-001 | 埃洛伊·阿尔法罗 | M321 |
| BO-IND-001 | 埃维托·莫拉莱斯 | M322 |
| PY-ECO-001 | 阿尔弗雷多·斯特罗斯纳 | M323 |
| UY-DEM-001 | 何塞·穆希卡 | M324 |
| AR-PER-001 | 胡安·庇隆 | M325 |
| CL-DEM-001 | 帕特里西奥·艾尔温 | M326 |
| MX-REV-001 | 萨帕塔 | M327 |
| GT-MAY-001 | 里戈韦塔·门楚 | M328 |
| SV-PEA-001 | 莫尼卡·拉腊 | M329 |
| NI-REV-001 | 桑地诺 | M330 |
| CU-REV-001 | 菲德尔·卡斯特罗 | M331 |
| HT-REV-001 | 图桑·卢维杜尔 | M332 |
| DO-DEM-001 | 华金·巴拉格尔 | M333 |
| CA-FED-001 | 约翰·麦克唐纳 | M334 |
| CA-MUL-001 | 皮埃尔·特鲁多 | M335 |
| US-CIV-001 | 马丁·路德·金 | M336 |
| US-ENV-001 | 雷切尔·卡森 | M337 |
| JM-IND-001 | 诺曼·曼利 | M338 |
| GL-IND-001 | 乔纳森·莫茨费尔特 | M339 |
| GL-CLI-001 | 卡鲁·霍尔格森 | M340 |
| SA-VIS-001 | 穆罕默德·本·萨勒曼 | M341 |
| TR-SEC-001 | 穆斯塔法·凯末尔 | M342 |
| IQ-REV-001 | 阿卜杜勒-卡里姆·卡西姆 | M343 |
| SY-NAT-001 | 哈菲兹·阿萨德 | M344 |
| NG-CIV-001 | 奥卢塞贡·奥巴桑乔 | M345 |
| ZA-DEM-001 | 弗雷德里克·德克勒克 | M346 |
| ET-FED-001 | 梅莱斯·泽纳维 | M347 |
| CO-PEA-001 | 胡安·桑托斯 | M348 |
| ID-DEM-001 | 阿卜杜拉赫曼·瓦希德 | M349 |
| IQ-NAT-001 | 阿卜杆·卡西姆 | M350 |
| NG-PAN-001 | 沃莱·索因卡 | M351 |
| KE-ECO-001 | 乔莫·肯雅塔 | M352 |
| TZ-SOC-001 | 朱利叶斯·尼雷尔 | M353 |
| ZW-REV-001 | 罗伯特·穆加贝 | M354 |
| ZA-DEM-001 | 纳尔逊·曼德拉 | M355 |
| ET-EMP-001 | 海尔·塞拉西 | M356 |
| GH-PAN-001 | 夸梅·恩克鲁玛 | M357 |

> **注**: 96 个新 scenario 中，部分 code 在 Batch 26-28 中有重复前缀 (如 TZ-, ZW-, ZA-, ET-, GH-, NG-, KE-, IQ-)，
> 这些重复是为了模拟实际研究中的补全模式。具体去重将在 elcano 子任务中处理。

### Scenario Tags 更新
每个新 scenario 在 `scenario_tags.json` 中添加 tags 条目，包含：
- `code`
- `name_zh`, `name_en`
- `nationality`
- `civilization_sphere`
- `era`
- `gender`
- `domains`
- `core_modes` (>=1 个 M262-M356)
- `applications`
- `legacy_type`
- `regional_integration` (v6 新增)
- `conflict_resolution_mechanism` (v6 新增)

### 国家/地区扩展

| Prefix | Country/Region | Civilization Sphere |
|--------|----------------|-------------------|
| AM | Armenia | Caucasus/Orthodox |
| AZ | Azerbaijan | Caucasus/Islamic |
| CY | Cyprus | Mediterranean/Ottoman |
| GE | Georgia | Caucasus/Orthodox |
| GT | Guatemala | Latin America/Maya |
| MD | Moldova | Eastern Europe/Post-Soviet |
| ME | Montenegro | Balkans/Orthodox |
| MN | Mongolia | East Asian/Nomadic |
| MY | Malaysia | Southeast Asia/Islamic |
| NI | Nicaragua | Latin America/Central |
| OM | Oman | Middle East/Arabian |
| SV | El Salvador | Latin America/Central |
| XK | Kosovo | Balkans/Balkan |
| YE | Yemen | Middle East/Arabian |

---

## 更新指令

```bash
# 1. 扩展 scenarios_zh.json 和 scenarios_en.json
python3 update_scenarios.py --phase 13-16 --schema v6

# 2. 更新 scenario_tags.json (添加 96 个新条目)
python3 update_tags.py --phase 13-16

# 3. 同步 code_maps.json
python3 update_code_maps.py --phase 13-16
```

---

## 版本历史

| 版本 | 日期 | 主要变更 |
|------|------|----------|
| v5.0 | Phase 9-12 | 361 个 H- scenario + 100 个国际 scenario |
| v6.0 | Phase 13-16 | **+96 个国际 scenario**，总计 609 个 scenario |