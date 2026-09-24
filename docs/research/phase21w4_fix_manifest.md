# Phase21 W4 名录修复/处置执行清单与干跑影响面（零库写）
- 卡号: t_10a42b2a  日期: 2026-09-23  执行: serrano
- 工作仓: `/opt/data/workspace/Protreptic`  发布仓(只读对账): `/opt/data/release/Protreptic-publish`
- 依据: `docs/research/phase21r8_w4_names_recon.md/.json` + 本卡【船长裁定】R1-R12; 与裁定矛盾处一律入「八、待船长复核」, 未自行改判
- 纪律: 零库写 -- 本卡仅写 `docs/research/phase21w4_fix_manifest.{md,json}` 与 scratch `/opt/data/cache/scratch/w4_manifest/`; 未改任何 live 数据/代码/站点, 未建备份目录, 未执行清档
- 下游: 执行卡 t_536073f4 (elcano) 逐条落地; RW-KAG 清档独立卡 t_ee203180; 门控于 W5 链尾 t_25453b39

## 一, 结论速览（数字全部实测）
1. 干跑（按 `tools/build_figures_db.py:71-108` 装载规则模拟编辑后源, 与现行 `api/protreptic.db` 全量 1057 码逐码对账零失配）: figures 行 **1057 -> 1028**（清档 29 行）; 双名全空行 **563 -> 514**（18 行回填转有名 + 29 行清档消失 + JP/UZ 旧码 2 行随重键消失、新码 2 行有名生成）。
2. 受影响码 = **50**: 16 个 H-* 回填 + SG/MY/JP/UZ/RW-KAG-001 五族 + RW-KAG-1..27; 其余 **1007 码零变化**（干跑逐码 diff 证明: changed 仅 19 码 + added 2 + removed 31）。
3. 重键空位已证实: JP-SAS-001 / UZ-ULU-001 在 scenarios_zh/en、data/scenarios_*、DB、figures.index、shard、统一索引、sitemap、docs 全链均不存在（全仓 rg 引用仅命中 recon 报告自身 2 件）-> 重键无唯一约束冲突。
4. 清档将消失 29 行 = SG-Lee-001(id 1024) + MY-Mah-001(id 1025) + RW-KAG-1..27(id 951..977); RW 27 码在 `data/modes_data.json` 的 figure_code 命中 = 0 -> by-figure 分片数(318)与 EXPECT_MODES/EXPECT_BY_FIGURE 均不受影响, 仅 EXPECT_FIGURES 1057->1028 需双处锚点同提交更新（见 8-6）。
5. H-MZ-001 en 取证结论: `data/figures/H-MZ-001.json` style_name = **"Y. C. James Yen"**（该文件 figure_name=晏阳初, 1890-1990）; zh=晏阳初（三源多数）; 孟子伴随包与 phase20 墨子引用按 R3 保留现状+登记冲突。
6. G类实测纠偏: `data/asia/individuals/` 两个「含换行符文件名」实测为**空目录**（非文件, 0 字节, git 不跟踪）-> R11 两分支均无适用对象, 建议 rmdir, 列待复核（8-3）。
## 二, a) 逐码现状表（全源节点实测; 完整逐节点现值见同名 .json `a_status`）
### 2.1 源层现值
| code | DB(id/名/模式) | scen_zh.name | scen_zh.name_zh | scen_en.name | code_maps_en | figure_names | 草稿(name_zh|name_en) | data/figures | companion |
|---|---|---|---|---|---|---|---|---|---|
| H-HYP-145 | id 134 / 空 / [9, 38, 37, 3 |  | 黄炎培 |  | '黄炎培: 职业教育救国与三自自主闭环' |  | '黄炎培'/'Huang Yanpei' | - | Y |
| H-WYX-146 | id 135 / 空 / [9, 5, 25, 37 |  | 吴有训 |  | 'Wu Youxun: 中国现代物理学奠基与实验自主范式' |  | '吴有训'/'Wu Youxun' | - | Y |
| H-WX-147 | id 136 / 空 / [1, 36, 38, 6 |  | 王选 |  | 'Wang Xuan: 激光照排系统与汉字信息处理死磕典范' |  | '王选'/'Wang Xuan' | - | Y |
| H-YLP-148 | id 137 / 空 / [] |  | 袁隆平：杂交水稻两系法与农业死磕范式跃迁 |  | 'Yuan Longping: Hybrid RiceTwo |  | '袁隆平'/'Yuan Longping' | - | Y |
| H-SY-149 | id 138 / 空 / [35, 16, 15,  |  | 粟裕 |  | {'name_zh': '粟裕：以纵深战略为内核的中国人民解 |  | '粟裕'/'Su Yu' | - | Y |
| H-XMQ-151 | id 140 / 空 / [26, 19, 38,  |  | 薛暮桥 |  | '薛暮桥: 价格改革理论奠基与改革风险决策框架' |  | '薛暮桥'/'Xue Muqiao' | - | Y |
| H-CY-159 | id 148 / 空 / [] |  | 陈毅：苏北/华中游击根据地四位一体建设、新四军统战与「诗军外交」跨界范式 |  | 'Chen Yi: 山东游击根据地建设与诗军外交跨界实践' |  | - | - | Y |
| H-LXN-347 | id 368 / 空 / [] |  | 李先念：「铁算盘」经济统筹、根据地币制创新与「以稳促建」宏观调控范式 |  | 'Li Xiannian: Financial Discip |  | - | - | Y |
| H-LXN-001 | id 369 / 空 / [7, 19, 38, 3 |  | 毛先念 |  |  |  | '毛先念'/'Mao Xiannian' | - | - |
| H-IKD-160 | id 1001 / 空 / [] |  | 伊本·赫勒敦：文明盛衰的『伊尔姆·乌姆兰』系统社会学与王朝周期辩证范式 |  | 'Ibn Khaldun: Systems Sociolog |  | - | - | Y |
| H-ISC-362 | id 1002 / 空 / [] |  | 阿维森纳（伊本·西那）：医学百科全书的体系建构、形而上学本体论与「理性-启示」调 |  |  |  | - | - | - |
| H-GHZ-163 | id 1003 / 空 / [] |  | 加扎利：神学—苏菲综合、哲学批判与「确定性」认识论的四位一体范式 |  |  | '安萨里' | - | - | Y |
| H-SUF-364 | id 1004 / 空 / [] |  | 鲁米（贾拉勒丁·鲁米）：诗歌神秘主义的普世转化、丧妻之痛与「爱」的本体论范式 |  |  |  | - | - | - |
| H-ZEL-001 | id 1045 / 空 / [42, 20, 6,  |  | 周恩来 |  |  |  | '周恩来'/'Zhou Enlai' | - | - |
| H-HLG-001 | id 1046 / 空 / [9, 17, 38,  |  | 华罗庚 |  |  | '华罗庚' | '华罗庚'/'Hua Luogeng' | Y | - |
| H-MZ-001 | id 1056 / 空 / [] |  |  |  |  | '晏阳初' | / | Y/style_name='Y. C. James Yen' | - |
| SG-Lee-001 | id 1024 / 空 / [34, 12, 20, |  | 李光耀：从第三世界到第一世界的『实用主义治国术』与长期战略工程化范式 |  |  |  | '李光耀：从第三世界到第一世界的『实用主义治国术』与长期战略 | - | - |
| SG-LEE-001 | id 687 / 空 / [303, 10, 157 |  | 李光耀/新加坡/从第三世界到第一/法治：从第三世界到第一与法治精英 |  | 'Lee Kuan Yew/Singapore/From T |  | '李光耀'/'Lee Kuan Yew' | - | - |
| MY-Mah-001 | id 1025 / 空 / [34, 12, 20, |  | 马哈迪·穆罕默德：从殖民医生到现代化推动者的『科技民族主义』与后殖民治理范式 |  |  |  | '马哈迪·穆罕默德：从殖民医生到现代化推动者的『科技民族主义 | - | - |
| MY-MAH-001 | id 1038 / 空 / [] | Mahathir Mohamad |  | Mahathir Mohamad |  |  | '马哈蒂尔'/'Mahathir' | - | Y |
| JP-Sas-001 | id 1026 / 空 / [19, 31, 7] |  | 西乡隆盛：从萨摩武士到明治维新『西南战争』的『武士道复兴法』与道德政治工程化范式 |  |  |  | '西乡隆盛：从萨摩武士到明治维新『西南战争』的『武士道复兴法 | - | - |
| UZ-Ulu-001 | id 1027 / 空 / [34, 12, 20] |  | 乌鲁格别克：萨马尔罕天文台的『科学革命法』与伊斯兰文艺复兴治理范式 |  |  |  | '乌鲁格别克：萨马尔罕天文台的『科学革命法』与伊斯兰文艺复兴 | - | - |
| RW-KAG-001 | id 844 / 空 / [576] |  | 卡加梅/卢旺达/种族灭绝/重建/强人/奇迹/保罗/卡加梅 |  | 'Kagame/Rwanda/Genocide/Rebuil |  | '卡加梅/卢旺达/种族灭绝/重建/强人/奇迹/保罗/卡加梅' | - | - |
| RW-KAG-1 | id 951 / 空 / [584] |  | 安第斯/南锥体/中美洲历史人物1 |  | 'Andean/South_American/Central |  | '安第斯/南锥体/中美洲历史人物1'/'Andean/Sou | - | - |
| RW-KAG-2 | id 952 / 空 / [525] |  | 安第斯/南锥体/中美洲历史人物2 |  | 'Andean/South_American/Central |  | '安第斯/南锥体/中美洲历史人物2'/'Andean/Sou | - | - |
| RW-KAG-3 | id 953 / 空 / [524] |  | 安第斯/南锥体/中美洲历史人物3 |  | 'Andean/South_American/Central |  | '安第斯/南锥体/中美洲历史人物3'/'Andean/Sou | - | - |
| RW-KAG-4 | id 954 / 空 / [514] |  | 安第斯/南锥体/中美洲历史人物4 |  | 'Andean/South_American/Central |  | '安第斯/南锥体/中美洲历史人物4'/'Andean/Sou | - | - |
| RW-KAG-5 | id 955 / 空 / [584] |  | 安第斯/南锥体/中美洲历史人物5 |  | 'Andean/South_American/Central |  | '安第斯/南锥体/中美洲历史人物5'/'Andean/Sou | - | - |
| RW-KAG-6 | id 956 / 空 / [559] |  | 安第斯/南锥体/中美洲历史人物6 |  | 'Andean/South_American/Central |  | '安第斯/南锥体/中美洲历史人物6'/'Andean/Sou | - | - |
| RW-KAG-7 | id 957 / 空 / [561] |  | 安第斯/南锥体/中美洲历史人物7 |  | 'Andean/South_American/Central |  | '安第斯/南锥体/中美洲历史人物7'/'Andean/Sou | - | - |
| RW-KAG-8 | id 958 / 空 / [590] |  | 安第斯/南锥体/中美洲历史人物8 |  | 'Andean/South_American/Central |  | '安第斯/南锥体/中美洲历史人物8'/'Andean/Sou | - | - |
| RW-KAG-9 | id 959 / 空 / [543] |  | 安第斯/南锥体/中美洲历史人物9 |  | 'Andean/South_American/Central |  | '安第斯/南锥体/中美洲历史人物9'/'Andean/Sou | - | - |
| RW-KAG-10 | id 960 / 空 / [587] |  | 安第斯/南锥体/中美洲历史人物10 |  | 'Andean/South_American/Central |  | '安第斯/南锥体/中美洲历史人物10'/'Andean/So | - | - |
| RW-KAG-11 | id 961 / 空 / [521] |  | 安第斯/南锥体/中美洲历史人物11 |  | 'Andean/South_American/Central |  | '安第斯/南锥体/中美洲历史人物11'/'Andean/So | - | - |
| RW-KAG-12 | id 962 / 空 / [517] |  | 安第斯/南锥体/中美洲历史人物12 |  | 'Andean/South_American/Central |  | '安第斯/南锥体/中美洲历史人物12'/'Andean/So | - | - |
| RW-KAG-13 | id 963 / 空 / [593] |  | 安第斯/南锥体/中美洲历史人物13 |  | 'Andean/South_American/Central |  | '安第斯/南锥体/中美洲历史人物13'/'Andean/So | - | - |
| RW-KAG-14 | id 964 / 空 / [580] |  | 安第斯/南锥体/中美洲历史人物14 |  | 'Andean/South_American/Central |  | '安第斯/南锥体/中美洲历史人物14'/'Andean/So | - | - |
| RW-KAG-15 | id 965 / 空 / [530] |  | 安第斯/南锥体/中美洲历史人物15 |  | 'Andean/South_American/Central |  | '安第斯/南锥体/中美洲历史人物15'/'Andean/So | - | - |
| RW-KAG-16 | id 966 / 空 / [575] |  | 安第斯/南锥体/中美洲历史人物16 |  | 'Andean/South_American/Central |  | '安第斯/南锥体/中美洲历史人物16'/'Andean/So | - | - |
| RW-KAG-17 | id 967 / 空 / [509] |  | 安第斯/南锥体/中美洲历史人物17 |  | 'Andean/South_American/Central |  | '安第斯/南锥体/中美洲历史人物17'/'Andean/So | - | - |
| RW-KAG-18 | id 968 / 空 / [543] |  | 安第斯/南锥体/中美洲历史人物18 |  | 'Andean/South_American/Central |  | '安第斯/南锥体/中美洲历史人物18'/'Andean/So | - | - |
| RW-KAG-19 | id 969 / 空 / [580] |  | 安第斯/南锥体/中美洲历史人物19 |  | 'Andean/South_American/Central |  | '安第斯/南锥体/中美洲历史人物19'/'Andean/So | - | - |
| RW-KAG-20 | id 970 / 空 / [560] |  | 安第斯/南锥体/中美洲历史人物20 |  | 'Andean/South_American/Central |  | '安第斯/南锥体/中美洲历史人物20'/'Andean/So | - | - |
| RW-KAG-21 | id 971 / 空 / [582] |  | 安第斯/南锥体/中美洲历史人物21 |  | 'Andean/South_American/Central |  | '安第斯/南锥体/中美洲历史人物21'/'Andean/So | - | - |
| RW-KAG-22 | id 972 / 空 / [599] |  | 安第斯/南锥体/中美洲历史人物22 |  | 'Andean/South_American/Central |  | '安第斯/南锥体/中美洲历史人物22'/'Andean/So | - | - |
| RW-KAG-23 | id 973 / 空 / [568] |  | 安第斯/南锥体/中美洲历史人物23 |  | 'Andean/South_American/Central |  | '安第斯/南锥体/中美洲历史人物23'/'Andean/So | - | - |
| RW-KAG-24 | id 974 / 空 / [554] |  | 安第斯/南锥体/中美洲历史人物24 |  | 'Andean/South_American/Central |  | '安第斯/南锥体/中美洲历史人物24'/'Andean/So | - | - |
| RW-KAG-25 | id 975 / 空 / [530] |  | 安第斯/南锥体/中美洲历史人物25 |  | 'Andean/South_American/Central |  | '安第斯/南锥体/中美洲历史人物25'/'Andean/So | - | - |
| RW-KAG-26 | id 976 / 空 / [596] |  | 安第斯/南锥体/中美洲历史人物26 |  | 'Andean/South_American/Central |  | '安第斯/南锥体/中美洲历史人物26'/'Andean/So | - | - |
| RW-KAG-27 | id 977 / 空 / [576] |  | 安第斯/南锥体/中美洲历史人物27 |  | 'Andean/South_American/Central |  | '安第斯/南锥体/中美洲历史人物27'/'Andean/So | - | - |
### 2.2 链上产物现值（工作仓; 发布仓只读对账数值在 .json `a_status[].release`）
| code | figindex(name_zh/n_modes) | shard | 统一索引(发布,type/name) | 路由 web_p0_routes | sitemap | docs/figures md |
|---|---|---|---|---|---|---|
| H-HYP-145 |  / 5 | Y | scenario / H-HYP-145 | - | figures | - |
| H-WYX-146 |  / 5 | Y | scenario / H-WYX-146 | - | figures | - |
| H-WX-147 |  / 5 | Y | scenario / H-WX-147 | - | figures | - |
| H-YLP-148 |  / 0 | Y | scenario / H-YLP-148 | - | figures | - |
| H-SY-149 |  / 5 | Y | scenario / H-SY-149 | - | figures | - |
| H-XMQ-151 |  / 5 | Y | scenario / H-XMQ-151 | - | figures | Y |
| H-CY-159 |  / 0 | Y | scenario / H-CY-159 | - | figures | - |
| H-LXN-347 |  / 0 | Y | scenario / H-LXN-347 | - | figures | - |
| H-LXN-001 |  / 5 | Y | scenario / H-LXN-001 | - | figures | Y |
| H-IKD-160 |  / 0 | Y | scenario / H-IKD-160 | - | figures | - |
| H-ISC-362 |  / 0 | Y | scenario / H-ISC-362 | - | figures | - |
| H-GHZ-163 |  / 0 | Y | scenario / H-GHZ-163 | - | figures | Y |
| H-SUF-364 |  / 0 | Y | scenario / H-SUF-364 | - | figures | - |
| H-ZEL-001 |  / 5 | Y | scenario / H-ZEL-001 | - | figures | Y |
| H-HLG-001 |  / 4 | Y | figure / 华罗庚 | - | minds | Y |
| H-MZ-001 |  / 0 | Y | scenario / H-MZ-001 | - | figures | Y |
| SG-Lee-001 |  / 4 | Y | scenario / SG-Lee-001 | - | figures | - |
| SG-LEE-001 |  / 4 | Y | scenario / SG-LEE-001 | - | figures | - |
| MY-Mah-001 |  / 4 | Y | scenario / MY-Mah-001 | - | figures | - |
| MY-MAH-001 | Mahathir / 0 | Y | scenario / Mahathir Mohamad | - | figures | - |
| JP-Sas-001 |  / 3 | Y | scenario / JP-Sas-001 | - | figures | - |
| UZ-Ulu-001 |  / 3 | Y | scenario / UZ-Ulu-001 | - | figures | - |
| RW-KAG-001 |  / 1 | Y | scenario / RW-KAG-001 | - | figures | - |
| RW-KAG-1 |  / 1 | Y | scenario / RW-KAG-1 | - | figures | - |
| RW-KAG-2 |  / 1 | Y | scenario / RW-KAG-2 | - | figures | - |
| RW-KAG-3 |  / 1 | Y | scenario / RW-KAG-3 | - | figures | - |
| RW-KAG-4 |  / 1 | Y | scenario / RW-KAG-4 | - | figures | - |
| RW-KAG-5 |  / 1 | Y | scenario / RW-KAG-5 | - | figures | - |
| RW-KAG-6 |  / 1 | Y | scenario / RW-KAG-6 | - | figures | - |
| RW-KAG-7 |  / 1 | Y | scenario / RW-KAG-7 | - | figures | - |
| RW-KAG-8 |  / 1 | Y | scenario / RW-KAG-8 | - | figures | - |
| RW-KAG-9 |  / 1 | Y | scenario / RW-KAG-9 | - | figures | - |
| RW-KAG-10 |  / 1 | Y | scenario / RW-KAG-10 | - | figures | - |
| RW-KAG-11 |  / 1 | Y | scenario / RW-KAG-11 | - | figures | - |
| RW-KAG-12 |  / 1 | Y | scenario / RW-KAG-12 | - | figures | - |
| RW-KAG-13 |  / 1 | Y | scenario / RW-KAG-13 | - | figures | - |
| RW-KAG-14 |  / 1 | Y | scenario / RW-KAG-14 | - | figures | - |
| RW-KAG-15 |  / 1 | Y | scenario / RW-KAG-15 | - | figures | - |
| RW-KAG-16 |  / 1 | Y | scenario / RW-KAG-16 | - | figures | - |
| RW-KAG-17 |  / 1 | Y | scenario / RW-KAG-17 | - | figures | - |
| RW-KAG-18 |  / 1 | Y | scenario / RW-KAG-18 | - | figures | - |
| RW-KAG-19 |  / 1 | Y | scenario / RW-KAG-19 | - | figures | - |
| RW-KAG-20 |  / 1 | Y | scenario / RW-KAG-20 | - | figures | - |
| RW-KAG-21 |  / 1 | Y | scenario / RW-KAG-21 | - | figures | - |
| RW-KAG-22 |  / 1 | Y | scenario / RW-KAG-22 | - | figures | - |
| RW-KAG-23 |  / 1 | Y | scenario / RW-KAG-23 | - | figures | - |
| RW-KAG-24 |  / 1 | Y | scenario / RW-KAG-24 | - | figures | - |
| RW-KAG-25 |  / 1 | Y | scenario / RW-KAG-25 | - | figures | - |
| RW-KAG-26 |  / 1 | Y | scenario / RW-KAG-26 | - | figures | - |
| RW-KAG-27 |  / 1 | Y | scenario / RW-KAG-27 | - | figures | - |
注: 16 H-* 全部 DB name_zh/name_en = 空串、shard 名字为空; 发布统一索引 15 码为 scenario/name=码本身, H-HLG-001 例外为 figure/name=华罗庚（人路由已正常, 本卡仍按 R1 回填其 scenario 侧空名）。

## 三, b) 编辑清单 (逐码 file + JSON 路径 + old->new 逐字; 机器可读版见 .json `b_edits`)
### 3.1 R1 -- 16 个 H-* 回填 name (scenarios_zh/en 双文件; 现均无 `name` 键, old=<键不存在>)
| code | tools/json/scenarios_zh.json $.<code>.name | tools/json/scenarios_en.json $.<code>.name | 证据 |
|---|---|---|---|
| H-HYP-145 | <键不存在> -> `黄炎培` | <键不存在> -> `Huang Yanpei` | scenarios_zh name_zh=黄炎培 + code_maps_en + 草稿 + companion |
| H-WYX-146 | <键不存在> -> `吴有训` | <键不存在> -> `Wu Youxun` | scenarios_zh name_zh=吴有训 + code_maps_en + 草稿 + companion |
| H-WX-147 | <键不存在> -> `王选` | <键不存在> -> `Wang Xuan` | scenarios_zh name_zh=王选 + code_maps_en + 草稿 + companion |
| H-YLP-148 | <键不存在> -> `袁隆平` | <键不存在> -> `Yuan Longping` | scenarios_zh name_zh=袁隆平 + 草稿 name_en=Yuan Longping + companion |
| H-SY-149 | <键不存在> -> `粟裕` | <键不存在> -> `Su Yu` | scenarios_zh name_zh=粟裕 + code_maps_en + 草稿 + companion |
| H-XMQ-151 | <键不存在> -> `薛暮桥` | <键不存在> -> `Xue Muqiao` | scenarios_zh name_zh=薛暮桥 + 草稿 + companion + docs/figures md |
| H-CY-159 | <键不存在> -> `陈毅` | <键不存在> -> `Chen Yi` | scenarios_zh 长串冒号前 + code_maps_en + companion |
| H-LXN-347 | <键不存在> -> `李先念` | <键不存在> -> `Li Xiannian` | scenarios_zh 长串冒号前 + code_maps_en + companion |
| H-LXN-001 | <键不存在> -> `李先念` | <键不存在> -> `Li Xiannian` | R2 修正后 name_zh=李先念 + docs/figures md |
| H-IKD-160 | <键不存在> -> `伊本·赫勒敦` | <键不存在> -> `Ibn Khaldun` | scenarios_zh 长串冒号前 + code_maps_en + companion |
| H-ISC-362 | <键不存在> -> `阿维森纳(伊本·西那)` | <键不存在> -> `Avicenna (Ibn Sina)` | scenarios_zh 长串冒号前=阿维森纳(伊本·西那) |
| H-GHZ-163 | <键不存在> -> `安萨里` | <键不存在> -> `Al-Ghazali` | figure_names=安萨里 + companion + docs/figures md (scen 长串首段=加扎利, 译名冲突见 8-4) |
| H-SUF-364 | <键不存在> -> `鲁米(贾拉勒丁·鲁米)` | <键不存在> -> `Rumi (Jalal al-Din Rumi)` | scenarios_zh/en 长串冒号前 |
| H-ZEL-001 | <键不存在> -> `周恩来` | <键不存在> -> `Zhou Enlai` | scenarios_zh name_zh=周恩来 + 草稿 + docs/figures md |
| H-HLG-001 | <键不存在> -> `华罗庚` | <键不存在> -> `Hua Luogeng` | figure_names=华罗庚 + 发布统一索引 figure 行 + 草稿 |
| H-MZ-001 | <键不存在> -> `晏阳初` | <键不存在> -> `Y. C. James Yen` | 三源多数=晏阳初; en=data/figures/H-MZ-001.json style_name=Y. C. James Yen |
口径注记 (依 R8): 仅新增/设置 `name` 键为短名; 各码既有 `name_zh`/`name_en` 长串 (人名:题名 形) 本轮保留不动, 「长形归一」登记为可选后续项。
### 3.2 R2/R11 -- H-LXN-001 错名修正 (毛先念/Mao Xiannian -> 李先念/Li Xiannian)
R2 字面范围 (执行卡直接执行):
| file | JSON 路径 | old | new |
|---|---|---|---|
| tools/json/H-LXN-001.json | $.name_zh | 毛先念 | 李先念 |
| tools/json/H-LXN-001.json | $.name_en | Mao Xiannian | Li Xiannian |
| tools/json/scenarios_en.json | $.H-LXN-001.name_en | Mao Xiannian | Li Xiannian |
实测同码其余错名位点 (键位实测确认; 处置建议已给, 归属见 8-1):
| file | 位点 | 现值 | 建议 |
|---|---|---|---|
| tools/json/scenarios_zh.json | $.H-LXN-001.name_zh / description_zh / reason_zh / case_zh | 毛先念 x4 | 同批改 李先念 (待复核 1) |
| tools/json/scenarios_en.json | $.H-LXN-001.description_en / reason_en / case_en | Mao Xiannian x3 | 随 R2 [scenarios_en 同步] 一并替换 |
| tools/json/H-LXN-001.json | $.description_zh/reason_zh/case_zh + $.description_en/reason_en/case_en | 毛先念 x3 + Mao Xiannian x3 | 随 R2 [修错名] 一并替换 |
| docs/figures/H-LXN-001.md | 正文 x2 | 毛先念 x2 | 建议同批改 (随 mkdocs 重建 site_docs 页); 待复核 1 |
| H-LXN-001.json (仓库根目录) | name_zh/name_en/description_*/reason_*/case_* | 毛先念 x4 + Mao Xiannian x4 | 本轮不动 (根目录遗留, 归 R7 旁项); 待复核 1 |
| CHANGELOG.md | 历史条目 x1 | 毛先念 | 不改写历史 |
### 3.3 R4/R5 -- SG / MY 重复对归一
- **SG**: 保留 `SG-LEE-001`, 回填 name (zh: <无>->`李光耀`; en: <无>->`Lee Kuan Yew`); `SG-Lee-001` 全链清档 (先备份后清), 位点: scenarios_zh/en 整条 + tools/json/SG-Lee-001.json 草稿 + DB id1024 + shard + figures.index 条目 + web/dist + web_p0_routes 条目 + sitemap 条目 + 发布仓镜像 (归合并卡)。
- **MY**: 保留 `MY-MAH-001`, 修正 name 错位 (zh: `Mahathir Mohamad` -> `马哈蒂尔`; en: 保持 `Mahathir Mohamad`); `MY-Mah-001` 全链清档 (先备份后清), 位点同 SG (DB id1025)。
### 3.4 R6/R7 -- JP / UZ 重键 + 回填 + 旧码全链清档
| 项 | old 码 | new 码 | zh 终值 | en 终值 |
|---|---|---|---|---|
| R6 | JP-Sas-001 | JP-SAS-001 | 西乡隆盛 | Saigō Takamori (en 剥副题: 去冒号后全部 + 尾注 [recorded as 笹木儿 in batch plan]) |
| R7 | UZ-Ulu-001 | UZ-ULU-001 | 乌鲁格别克 | Ulugh Beg |
完整操作序列 (两码同构): (1)备份 (2)scenarios_zh/en 键重命名 (整条迁移不改内容) (3)新键条目设 name (4)删旧码草稿 tools/json/<old>.json (5)重建链 build_figures_db -> export_static_site -> build_unified_index -> prerender_routes -> build_sitemap (旧码分片/索引/sitemap 条目消失, 新码生成) (6)rg 旧码复核 = 0 残留 (报告/备份类除外)。
### 3.5 R9 -- RW-KAG-001 回填
- tools/json/scenarios_zh.json $.RW-KAG-001.name: <无>->`卡加梅`; tools/json/scenarios_en.json $.RW-KAG-001.name: <无>->`Paul Kagame` (证据: 草稿 name_zh=卡加梅/卢旺达/..., en 长串含 Paul/Kagame; 依 R8 取短名)。
### 3.6 R10 -- RW-KAG-1..27 全链清档 (执行卡 t_ee203180; 本卡仅清单+扫描+备份模板)
- 27 码: RW-KAG-1 .. RW-KAG-27 (DB id 951..977, 全部空名, 各带 1 条占位模式)。
- 每码清档位点: scenarios_zh/en 整条; tools/code_maps_en.json 键 (占位值 Andean/South_American/Central_American_Historical_Figure_N, 27 条, 归属见 8-5); tools/json/<code>.json 草稿; DB 行; shard; figures.index 条目; web/dist; web_p0_routes 条目; sitemap 条目; 发布仓镜像 (tools/json x27 + shard x27, 归合并卡)。
- modes_data.json figure_code 命中 = 0 (实测) -> 不触及模式库与 by-figure 计数。
### 3.7 R11 G类 -- H-LXN-001.json 错名 (见 3.2) + 两异常文件名 (见 8-3 实测纠偏)
### 3.8 重建链与同提交更新清单 (执行卡按序)
1. 备份 (第 6 节模板)。
2. 编辑 tools/json/scenarios_zh.json / scenarios_en.json (3.1-3.6) + tools/json/H-LXN-001.json (R2) + 删清档码草稿。
3. **同提交锚点**: tools/export_static_site.py L74 `EXPECT_FIGURES = 1057 -> 1028`; tools/pages_preflight.py L25 同改 (EXPECT_MODES=3281 / EXPECT_BY_FIGURE=318 / EXPECT_MODE_INDEX_SHARDS=8 不变)。
4. 重建链: `python3 tools/build_figures_db.py` (api/protreptic.db, 跟踪文件需提交) -> `tools/export_static_site.py` (web/public/data/** gitignore + docs/architecture/static_data_manifest.json 跟踪需提交) -> `gen_web_site_counts.py` (siteCounts.ts figures=318 口径不变, 预期零 diff) -> `build_daily_index.py` -> `pages_preflight.py --stage data` -> `build_search_index.py` / `build_graph_data.py` -> `build_unified_index.py` -> 可信度/链接门 -> web `npm run build` -> `pages_preflight.py --stage dist` -> `prerender_routes.py --body-persons all` (docs/architecture/web_p0_routes.json 跟踪需提交) -> `apply_og_meta.py` / `apply_site_counts.py` / `build_sw.py` -> `build_sitemap.py` (web/public/sitemap.xml 跟踪需提交) -> mkdocs (site_docs/)。
5. 计数文案残留引用 (实测 rg 1057): `web/src/api/static.ts` L13/L15 注释两处、`web/src/views/ApiDocsView.vue` L11 文案两处 -- 同提交更新建议项 (待船长裁量, 8-6)。
6. 发布仓镜像提交归合并卡 (与 t_08bbb73d 同模式)。

## 四, c) 干跑影响面 (不落 live; 脚本/输出留档 scratch, 可复跑)
| 指标 | before | after |
|---|---|---|
| figures 行数 | 1057 | 1028 |
| 双名全空行 | 563 | 514 |
| 有名行 | 494 | 514 |
| 新增码 | - | JP-SAS-001, UZ-ULU-001 |
| 消失码 (清档+重键旧码) | - | 31 (清档 29: SG-Lee-001/MY-Mah-001/RW-KAG-1..27; 重键旧码 2: JP-Sas-001/UZ-Ulu-001) |
| 名字变化码 | - | 19 (16 H-* + SG-LEE-001 + MY-MAH-001 + RW-KAG-001) |
| 其余码 | - | 1007 码零变化 (逐码 diff) |
| 唯一约束 | - | 重键新码全链不存在 [OK]; 源 zh/en 键集各 1070 (zh 独有 H-ZZ-001, en 独有 H-ZZ-168, 系既有不对称, 本轮不涉) |
| 模拟保真度 | - | sim(before) 与现行 DB 逐码 name 零失配; modes 列仅 H-MZ-001 一码口径差 (DB modes=[] vs 源 mode_codes=M201~M210, 装载器读 `modes` 键, 行为一致) |

干跑复跑: `cd /opt/data/cache/scratch/w4_manifest && python3 dryrun.py` (只读, 输出 dryrun_result.json)

## 五, d) 全仓引用扫描 (rg; 工作仓全仓含 web/public / tools / docs / 根目录; 发布仓只读对账)

方法: `rg --no-ignore -o -c -P "<code>(?![0-9])" -g !.git -g !node_modules .` (RW-KAG-1 加数字边界防误配 RW-KAG-10+)。逐码 file:count 全量在 .json `d_reference_scan.per_code_file_counts`

处置标注结论:

- **需同提交更新** (链上活文件): tools/json/scenarios_zh.json / tools/json/scenarios_en.json / tools/json/<code>.json (受影响草稿) / tools/code_maps_en.json (RW 27 键, 8-5) / api/protreptic.db / docs/architecture/web_p0_routes.json / web/public/sitemap.xml / docs/architecture/static_data_manifest.json / docs/figures/H-LXN-001.md (R2 项, 待复核) / web/src/api/static.ts 与 web/src/views/ApiDocsView.vue (1057 计数文案)
- **随重建自动收敛** (gitignore 产物, 不入提交): web/public/data/** / web/dist/** / site_docs/**
- **发布仓镜像** (只读对账, 归合并卡): tools/json 受影响件 / web/public/data/figures 受影响分片 / web/public/sitemap.xml / api/protreptic.db / docs/figures 受影响 md
- **不可解->不改** (历史/报告/备份): docs/research/** / docs/qa/** / CHANGELOG.md / data/backup_* 快照 / data/audit/** / release/v2.0.0 归档镜像 / 根目录历史脚本 (integrate_huang.py 等)
- **不可解->待复核**: 根目录 H-LXN-001.json / docs/figures/H-LXN-001.md (若船长裁 R2 不含文档页)

JP-SAS-001 / UZ-ULU-001 全链不存在性: 全仓引用仅 `docs/research/phase21r8_w4_names_recon.{md,json}` (recon 报告自身); 其余全链无 -> 重键无冲突

## 六, e) 备份清单模板 (文件全列表 + sha256 口径; 实测现值, 机器可读在 .json `e_backup_templates`)

- `data/backup_phase21w4_fix_<日期>/`: 备份第 3 节全部编辑对象与重建产物基线 -- 11 件 (scenarios_zh/en 双源 + H-LXN-001/SG-Lee-001/MY-Mah-001/JP-Sas-001/UZ-Ulu-001 五草稿 + api/protreptic.db + web_p0_routes.json + sitemap.xml + static_data_manifest.json)
- `data/backup_phase21w4_rwkag_clear_<日期>/`: 备份 RW-KAG 27 码清档对象 -- 60 件 (code_maps_en + scenarios_zh/en + DB + routes + sitemap + 27 草稿 + 27 shard)
- 口径: 逐文件记录 `bytes` + `sha256` (备份前后各记一次, 双向校验); DB 件全量拷贝。执行卡建目录时以本清单为验收基准

| # | 归属 | 文件 | bytes | sha256(前16) |
|---|---|---|---|---|
| 1 | phase21w4_fix | tools/json/scenarios_zh.json | 3038171 | c240aa300812af6d |
| 2 | phase21w4_fix | tools/json/scenarios_en.json | 2288761 | 018aadd45918d72d |
| 3 | phase21w4_fix | tools/json/H-LXN-001.json | 7208 | f1eea2d7e76b92db |
| 4 | phase21w4_fix | tools/json/SG-Lee-001.json | 11352 | e51028809f5d3b99 |
| 5 | phase21w4_fix | tools/json/MY-Mah-001.json | 11295 | a122002d4fa30251 |
| 6 | phase21w4_fix | tools/json/JP-Sas-001.json | 11461 | c8c0634ba737ccbf |
| 7 | phase21w4_fix | tools/json/UZ-Ulu-001.json | 11338 | 2906ee68f62b5147 |
| 8 | phase21w4_fix | api/protreptic.db | 38490112 | 6014c9c5b5c29898 |
| 9 | phase21w4_fix | docs/architecture/web_p0_routes.json | 681153 | dd5c664b8b909f32 |
| 10 | phase21w4_fix | web/public/sitemap.xml | 211252 | d15b6858bb8e9a18 |
| 11 | phase21w4_fix | docs/architecture/static_data_manifest.json | 3748 | 16a806dc580c4561 |
| 12 | phase21w4_rwkag_clear | tools/code_maps_en.json | 86424 | b1893a9bbc8d04ad |
| 13 | phase21w4_rwkag_clear | tools/json/scenarios_zh.json | 3038171 | c240aa300812af6d |
| 14 | phase21w4_rwkag_clear | tools/json/scenarios_en.json | 2288761 | 018aadd45918d72d |
| 15 | phase21w4_rwkag_clear | api/protreptic.db | 38490112 | 6014c9c5b5c29898 |
| 16 | phase21w4_rwkag_clear | docs/architecture/web_p0_routes.json | 681153 | dd5c664b8b909f32 |
| 17 | phase21w4_rwkag_clear | web/public/sitemap.xml | 211252 | d15b6858bb8e9a18 |
| 18 | phase21w4_rwkag_clear | tools/json/RW-KAG-1.json | 1432 | 2120355120f0f2fe |
| 19 | phase21w4_rwkag_clear | tools/json/RW-KAG-2.json | 1435 | 3103ad783371c227 |
| 20 | phase21w4_rwkag_clear | tools/json/RW-KAG-3.json | 1435 | 742f2d53fed02535 |
| 21 | phase21w4_rwkag_clear | tools/json/RW-KAG-4.json | 1429 | 1918f330d1591279 |
| 22 | phase21w4_rwkag_clear | tools/json/RW-KAG-5.json | 1435 | 84a4827b363656a8 |
| 23 | phase21w4_rwkag_clear | tools/json/RW-KAG-6.json | 1435 | 000c2d607a6b5769 |
| 24 | phase21w4_rwkag_clear | tools/json/RW-KAG-7.json | 1435 | 1e362a2388ad1805 |
| 25 | phase21w4_rwkag_clear | tools/json/RW-KAG-8.json | 1438 | 13880403dbc7cead |
| 26 | phase21w4_rwkag_clear | tools/json/RW-KAG-9.json | 1426 | 7ec87be792552ec2 |
| 27 | phase21w4_rwkag_clear | tools/json/RW-KAG-10.json | 1457 | 710fc6055105215e |
| 28 | phase21w4_rwkag_clear | tools/json/RW-KAG-11.json | 1448 | ffe141ee68abe121 |
| 29 | phase21w4_rwkag_clear | tools/json/RW-KAG-12.json | 1442 | 03cf7b91fd9027b3 |
| 30 | phase21w4_rwkag_clear | tools/json/RW-KAG-13.json | 1451 | a1042e95d21b07cc |
| 31 | phase21w4_rwkag_clear | tools/json/RW-KAG-14.json | 1451 | d4fcc859077366aa |
| 32 | phase21w4_rwkag_clear | tools/json/RW-KAG-15.json | 1448 | 554af070902db49e |
| 33 | phase21w4_rwkag_clear | tools/json/RW-KAG-16.json | 1442 | fa66603dd8d000e0 |
| 34 | phase21w4_rwkag_clear | tools/json/RW-KAG-17.json | 1451 | c75b01b31ba2bd35 |
| 35 | phase21w4_rwkag_clear | tools/json/RW-KAG-18.json | 1451 | 979a8809384b4b9f |
| 36 | phase21w4_rwkag_clear | tools/json/RW-KAG-19.json | 1451 | 5e69edbe852557b0 |
| 37 | phase21w4_rwkag_clear | tools/json/RW-KAG-20.json | 1445 | 7be55f3338f87f55 |
| 38 | phase21w4_rwkag_clear | tools/json/RW-KAG-21.json | 1445 | 26ac7123b5f595c1 |
| 39 | phase21w4_rwkag_clear | tools/json/RW-KAG-22.json | 1448 | 99282b3000d7bfcb |
| 40 | phase21w4_rwkag_clear | tools/json/RW-KAG-23.json | 1460 | 0e31431a3193e4fa |
| 41 | phase21w4_rwkag_clear | tools/json/RW-KAG-24.json | 1451 | 146d8613611506cc |
| 42 | phase21w4_rwkag_clear | tools/json/RW-KAG-25.json | 1451 | 16905f79e43fca62 |
| 43 | phase21w4_rwkag_clear | tools/json/RW-KAG-26.json | 1442 | c6251272182f07c8 |
| 44 | phase21w4_rwkag_clear | tools/json/RW-KAG-27.json | 1451 | 08a82355892d8a77 |
| 45 | phase21w4_rwkag_clear | web/public/data/figures/RW-KAG-1.json | 316 | cd3eef6c7ef1cf06 |
| 46 | phase21w4_rwkag_clear | web/public/data/figures/RW-KAG-2.json | 316 | 8bbdfde983f1b874 |
| 47 | phase21w4_rwkag_clear | web/public/data/figures/RW-KAG-3.json | 316 | 5fecfa1df055d740 |
| 48 | phase21w4_rwkag_clear | web/public/data/figures/RW-KAG-4.json | 316 | af645b35359463d8 |
| 49 | phase21w4_rwkag_clear | web/public/data/figures/RW-KAG-5.json | 316 | da631698837c5bd3 |
| 50 | phase21w4_rwkag_clear | web/public/data/figures/RW-KAG-6.json | 316 | d8a428fff357cdec |
| 51 | phase21w4_rwkag_clear | web/public/data/figures/RW-KAG-7.json | 316 | 4de6db9a8d9c7963 |
| 52 | phase21w4_rwkag_clear | web/public/data/figures/RW-KAG-8.json | 316 | 71e324c9f89fb782 |
| 53 | phase21w4_rwkag_clear | web/public/data/figures/RW-KAG-9.json | 316 | deba79c50e57718e |
| 54 | phase21w4_rwkag_clear | web/public/data/figures/RW-KAG-10.json | 317 | d1e52aa292240a8f |
| 55 | phase21w4_rwkag_clear | web/public/data/figures/RW-KAG-11.json | 317 | 5ba8e8bdf20cce22 |
| 56 | phase21w4_rwkag_clear | web/public/data/figures/RW-KAG-12.json | 317 | 1bd71f4fad623d24 |
| 57 | phase21w4_rwkag_clear | web/public/data/figures/RW-KAG-13.json | 317 | 16ddaac0cd9a20ba |
| 58 | phase21w4_rwkag_clear | web/public/data/figures/RW-KAG-14.json | 317 | 18ceb8b422f5aea0 |
| 59 | phase21w4_rwkag_clear | web/public/data/figures/RW-KAG-15.json | 317 | a76e179c2c7cbaac |
| 60 | phase21w4_rwkag_clear | web/public/data/figures/RW-KAG-16.json | 317 | b61bc092b32f0dba |
| 61 | phase21w4_rwkag_clear | web/public/data/figures/RW-KAG-17.json | 317 | dc587803f68ef900 |
| 62 | phase21w4_rwkag_clear | web/public/data/figures/RW-KAG-18.json | 317 | 8e5ea7aaa22cbfdb |
| 63 | phase21w4_rwkag_clear | web/public/data/figures/RW-KAG-19.json | 317 | eed56cf3341973de |
| 64 | phase21w4_rwkag_clear | web/public/data/figures/RW-KAG-20.json | 317 | 49ca5759a3aca956 |
| 65 | phase21w4_rwkag_clear | web/public/data/figures/RW-KAG-21.json | 317 | 9ed3455202d458b3 |
| 66 | phase21w4_rwkag_clear | web/public/data/figures/RW-KAG-22.json | 317 | dcad3fa1f08b71a6 |
| 67 | phase21w4_rwkag_clear | web/public/data/figures/RW-KAG-23.json | 317 | 49a299a1342de4af |
| 68 | phase21w4_rwkag_clear | web/public/data/figures/RW-KAG-24.json | 317 | 241cce5bb8191536 |
| 69 | phase21w4_rwkag_clear | web/public/data/figures/RW-KAG-25.json | 317 | ea54a655da6ae386 |
| 70 | phase21w4_rwkag_clear | web/public/data/figures/RW-KAG-26.json | 317 | 44dda416ff99b1ab |
| 71 | phase21w4_rwkag_clear | web/public/data/figures/RW-KAG-27.json | 317 | 3cc326b31b80de9c |

## 七, f) 目标值终表 (执行卡与 QA 卡对照基准; 一码一行)

| code | 处置 | zh 终值 | en 终值 |
|---|---|---|---|
| H-HYP-145 | 回填 | 黄炎培 | Huang Yanpei |
| H-WYX-146 | 回填 | 吴有训 | Wu Youxun |
| H-WX-147 | 回填 | 王选 | Wang Xuan |
| H-YLP-148 | 回填 | 袁隆平 | Yuan Longping |
| H-SY-149 | 回填 | 粟裕 | Su Yu |
| H-XMQ-151 | 回填 | 薛暮桥 | Xue Muqiao |
| H-CY-159 | 回填 | 陈毅 | Chen Yi |
| H-LXN-347 | 回填 | 李先念 | Li Xiannian |
| H-LXN-001 | 回填 | 李先念 | Li Xiannian |
| H-IKD-160 | 回填 | 伊本·赫勒敦 | Ibn Khaldun |
| H-ISC-362 | 回填 | 阿维森纳(伊本·西那) | Avicenna (Ibn Sina) |
| H-GHZ-163 | 回填 | 安萨里 | Al-Ghazali |
| H-SUF-364 | 回填 | 鲁米(贾拉勒丁·鲁米) | Rumi (Jalal al-Din Rumi) |
| H-ZEL-001 | 回填 | 周恩来 | Zhou Enlai |
| H-HLG-001 | 回填 | 华罗庚 | Hua Luogeng |
| H-MZ-001 | 回填 | 晏阳初 | Y. C. James Yen |
| SG-LEE-001 | 保留+回填 | --清除-- | --清除-- |
| SG-Lee-001 | 清除 | --清除-- | --清除-- |
| MY-MAH-001 | 保留+修正 | --清除-- | --清除-- |
| MY-Mah-001 | 清除 | --清除-- | --清除-- |
| JP-SAS-001 | 新键(旧 JP-Sas-001 清) | --清除-- | --清除-- |
| UZ-ULU-001 | 新键(旧 UZ-Ulu-001 清) | --清除-- | --清除-- |
| RW-KAG-001 | 保留+回填 | --清除-- | --清除-- |
| RW-KAG-1 | 清除 | --清除-- | --清除-- |
| RW-KAG-2 | 清除 | --清除-- | --清除-- |
| RW-KAG-3 | 清除 | --清除-- | --清除-- |
| RW-KAG-4 | 清除 | --清除-- | --清除-- |
| RW-KAG-5 | 清除 | --清除-- | --清除-- |
| RW-KAG-6 | 清除 | --清除-- | --清除-- |
| RW-KAG-7 | 清除 | --清除-- | --清除-- |
| RW-KAG-8 | 清除 | --清除-- | --清除-- |
| RW-KAG-9 | 清除 | --清除-- | --清除-- |
| RW-KAG-10 | 清除 | --清除-- | --清除-- |
| RW-KAG-11 | 清除 | --清除-- | --清除-- |
| RW-KAG-12 | 清除 | --清除-- | --清除-- |
| RW-KAG-13 | 清除 | --清除-- | --清除-- |
| RW-KAG-14 | 清除 | --清除-- | --清除-- |
| RW-KAG-15 | 清除 | --清除-- | --清除-- |
| RW-KAG-16 | 清除 | --清除-- | --清除-- |
| RW-KAG-17 | 清除 | --清除-- | --清除-- |
| RW-KAG-18 | 清除 | --清除-- | --清除-- |
| RW-KAG-19 | 清除 | --清除-- | --清除-- |
| RW-KAG-20 | 清除 | --清除-- | --清除-- |
| RW-KAG-21 | 清除 | --清除-- | --清除-- |
| RW-KAG-22 | 清除 | --清除-- | --清除-- |
| RW-KAG-23 | 清除 | --清除-- | --清除-- |
| RW-KAG-24 | 清除 | --清除-- | --清除-- |
| RW-KAG-25 | 清除 | --清除-- | --清除-- |
| RW-KAG-26 | 清除 | --清除-- | --清除-- |
| RW-KAG-27 | 清除 | --清除-- | --清除-- |

注: H-MZ-001 en 取证 = `data/figures/H-MZ-001.json` style_name = `Y. C. James Yen` (R8 指定取证口径)

## 八, 待船长复核 (实测与裁定矛盾/字面未覆盖项; 未自行改判)

1. **H-LXN-001 错名实测面 > R2 字面**: R2 只列 tools/json/H-LXN-001.json + scenarios_en; 实测 scenarios_zh.json 同码 name_zh/description_zh/reason_zh/case_zh 亦为 [毛先念] 4 处, docs/figures/H-LXN-001.md 2 处, 根目录 H-LXN-001.json 8 处。建议: scenarios_zh 与 docs/figures md 随 R2 同批修正 (否则 name=李先念 与 name_zh=毛先念 同条并存); 根目录副本归 R7 旁项不动。请裁定
2. **H-MZ-001 scenarios 条目 figure_name=孟子**: R1 回填 name=晏阳初 后, 同条 `figure_name` 键仍=孟子 (scenarios_zh/en 双文件); R3 只点名伴随包 H-MZ-001_modes 与 phase20 墨子引用 [保留现状]。该键是否属保留范围请裁定 (本清单默认不动, 仅登记)
3. **R11 两异常文件名实测为空目录**: 即文件名末尾接换行符加 `<` 的 `xue_mu_qiao_H-XMQ-151_modes.json` 与 `gong_yu_H-GY-152_modes.json` 两项, 实测均为 directory/0 字节/无内容/git 不跟踪, 字节比对无对象, R11 [重复件->备份后删除 / 非重复->规范重命名] 两分支均不适用。建议 rmdir (无备份内容, 证据=本节 + find/stat 实测)。请裁定
4. **H-GHZ-163 译名冲突**: R1 zh 终值=安萨里 (figure_names 键), 但 scenarios_zh 现长串首段=[加扎利]; recon 已将译名统一归 Phase46-R 待裁清单第 3 条。本清单按 R1 用 安萨里, 译名冲突继续挂 Phase46-R
5. **RW-KAG-1..27 的 code_maps_en 27 条键**: R10 字面 [全链清档] 未点名注册键; 27 键值均为 Andean/South_American/Central_American_Historical_Figure_N 占位串 (与 RW 卢旺达前缀不符, 属同批废件)。建议随清档同批删除 (已列入备份模板)。请确认
6. **EXPECT_FIGURES 锚点双改**: 清档后 figures 1057->1028, tools/export_static_site.py L74 与 tools/pages_preflight.py L25 两处 `EXPECT_FIGURES = 1057 -> 1028` 为清档必然伴生 (不双改则 Pages 门必红); R1-R12 字面未列。另 web/src/api/static.ts / ApiDocsView.vue 中 1057 计数文案两处属建议同批。请确认

## 九, R12 本轮不做 (登记)

- F类 547 场景侧空名回填 (其中 537 legacy 有 name_zh, 10 南部非洲批次无名字键); 装载器键回退 (name_zh fallback); 多码深度去重 (周恩来 x5 等)。均登记待用户口径, 本清单不动

## 十, 复跑要点与 scratch 留档

- scratch: `/opt/data/cache/scratch/w4_manifest/` -- `live_state.json` (全源节点现状探针输出, probe_master.py) / `scan_agg.json` (全仓引用扫描聚合, scan_run.py/scan_agg.py + scans/work/*.txt 原始输出) / `dryrun_result.json` (干跑, dryrun.py) / `edits.json` / `backup_templates.json` / `manifest_payload.json`
- 复跑顺序: `python3 probe_master.py` -> `python3 scan_run.py && python3 scan_agg.py` -> `python3 dryrun.py`, 数字应与第四节一致 (源基线 sha256: scenarios_zh `c240aa30...`, scenarios_en `018aadd4...`; figures.index.json sha256 前16 `f0eded8cd6b59245`)
- 本卡 git 前后对照: 仅新增 docs/research/phase21w4_fix_manifest.{md,json} 两件 (零 live 写验证)

