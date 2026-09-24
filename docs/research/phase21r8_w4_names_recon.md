# Phase21 W4 名录字段核对: 16 个 H-* 空名 + 异常码族分类矩阵 (零库写)

- 卡号: t_24b92f58  日期: 2026-09-23  执行: serrano
- 工作仓: `/opt/data/workspace/Protreptic`  发布仓: `/opt/data/release/Protreptic-publish`
- 纪律: 零库写: 本卡仅写 docs/research/phase21r8_w4_names_recon.{md,json}; 未改任何库/数据/站点文件
- 产物: `docs/research/phase21r8_w4_names_recon.md` + `docs/research/phase21r8_w4_names_recon.json`

## 一, 结论速览

1. **16 个 H-* 空名全部给出可核名字证据链**: 15 条为纯人名可解析 (①), 1 条 (H-MZ-001) 为三主张冲突, 需船长裁定 (②). 无一条判 无法解析; 所有名字均引自仓内既有数据源 (逐条见第四节).
2. **根因单一且全量可证**: `tools/build_figures_db.py` 只读 legacy 条目的 `name` / `name_en` 键; 563 条 legacy 条目用旧 schema `name_zh` / `name_en`, 键缺失导致 DB 名字为空, 下游 (shard / figures.index.json / index.unified.json / 预渲染页 / sitemap) 逐层继承. 跨 1057 码零反例 (第三节).
3. **空名底数对账**: DB figures 1057 行 = figures.index.json 1057 条; 其中空名 563 = 16 个 H-* + 547 个非 H (场景命名空间, 第六节). 发布仓统一索引 1359 条 = 304 figure + 1055 scenario; 562 条 scenario 的 name 回落为 code (547 非 H + 15 个 H-*).
4. **H-HLG-001 例外**: release/dist 统一索引中它是 figure 路由 (已解析为华罗庚, 10 条模式, 正文已预渲染); 本卡对其处置对象是被遮蔽的 scenario 空行.
5. **异常码族 5 个**: SG / MY 混大小写重复对, JP / UZ 单侧混大小写 (缺规范码), RW-KAG-1..27 模板占位废件族 (27 件在链死件) + RW-KAG-001 待回填. 逐族见第五节.
6. **既有卡映射**: 14 组 Phase19 批次链 + Phase46-R (已修 data/figures 层同类缺陷) + Phase30/31 名录治理先例; 代表卡 7 张 (第七节). 本卡零修复动作, 仅出矩阵.

## 二, 四层对账底数 (零库写实测)

| 层 | 路径 | 条数 | 空名 | 说明 |
|---|---|---|---|---|
| 主库 | `api/protreptic.db` figures 表 | 1057 | 563 | 工作仓/发布仓同值 |
| 轻索引 | `web/public/data/figures.index.json` | 1057 | 563 | 与 DB 同码集 (逐码相等) |
| 分片 | `web/public/data/figures/*.json` | 1057 | 563 | 16 件与发布仓逐字节一致 |
| 统一索引 | 发布仓 `web/public/data/index.unified.json` | 1359 | name=code 的 scenario 562 条 | 304 figure + 1055 scenario |

本次空名口径: **H-* 16 条 + 非 H 547 条 = 563 条**.

## 三, 根因链: 装载器键漂移 (name vs name_zh)

> 跨全量 1057 码零反例: 有名 494 行 100% 具备 legacy name 键; 空名 563 行 100% 无 name 键 (552 条 name_zh-only + 11 条无任何名字键)

| 关系 | 计数 | 判定 |
|---|---|---|
| DB 有名 且 legacy 有 name 键 | 494 | 正常装载路径 |
| DB 空名 且 legacy 只有 name_zh | 552 | 键漂移受害面 (含 15 个 H-* + 537 非 H) |
| DB 空名 且 legacy 无任何名字键 | 11 | 源头即无名字 (10 个南部非洲批次 + H-MZ-001) |

代码证据 (行号):
- `tools/build_figures_db.py:87`
- `tools/export_static_site.py:438,545-547`
- `tools/build_unified_index.py:139`

零反例双向核验: 有名 494 行 100% 有 name 键; 空名 563 行 100% 无 name 键 (named_bad = 0 条).

## 四, 16 个 H-* 空名逐码矩阵

### 4.1 名字证据 (全部引自仓内既有源, 零臆造)

| code | 名字 (zh) | 名字 (en) | 证据源 (首选) | 补强证据 |
|---|---|---|---|---|
| H-HYP-145 | 黄炎培 | Huang Yanpei | tools/json/scenarios_zh.json name_zh + tools/code_maps_en.json | companion `huang_yanpei_H-HYP-145_modes.json`; scenarios_en name_en |
| H-WYX-146 | 吴有训 | Wu Youxun | tools/json/scenarios_zh.json name_zh + tools/code_maps_en.json | companion `wu_you_xun_H-WYX-146_modes.json`; scenarios_en name_en |
| H-WX-147 | 王选 | Wang Xuan | tools/json/scenarios_zh.json name_zh + tools/code_maps_en.json | companion `wang_xuan_H-WX-147_modes.json`; scenarios_en name_en |
| H-YLP-148 | 袁隆平 | Yuan Longping: Hybrid Rice Two-Line System & the Agricultural 'Compound-Diligence' Paradigm Shift | tools/json/scenarios_zh.json name_zh + tools/code_maps_en.json | companion `yuan_longping_H-YLP-148_modes.json`; scenarios_en name_en |
| H-SY-149 | 粟裕 | Su Yu | tools/json/scenarios_zh.json name_zh + tools/code_maps_en.json | companion `su_yu_H-SY-149_modes.json`; scenarios_en name_en |
| H-XMQ-151 | 薛暮桥 | Xue Muqiao | tools/json/scenarios_zh.json name_zh + tools/code_maps_en.json | companion `xue_mu_qiao_H-XMQ-151_modes.json`; scenarios_en name_en; docs/figures/H-XMQ-151.md |
| H-CY-159 | 陈毅 | Chen Yi: Four-in-One Guerrilla Base-Area Construction in Subei/Central China, New Fourth Army United Front, and the '... | tools/json/scenarios_zh.json name_zh + tools/code_maps_en.json | companion `chenyi_H-CY-159_modes.json`; scenarios_en name_en |
| H-LXN-347 | 李先念 | Li Xiannian: The 'Iron Abacus' Economic Coordination, Base-Area Currency Innovation and the 'Stability-First Developm... | tools/json/scenarios_zh.json name_zh + tools/code_maps_en.json | companion `lixiannian_H-LXN-347_modes.json`; scenarios_en name_en |
| H-LXN-001 | 李先念 (legacy 草稿误作 毛先念) | Mao Xiannian | tools/json/scenarios_zh.json name_zh | scenarios_en name_en; docs/figures/H-LXN-001.md |
| H-IKD-160 | 伊本·赫勒敦 | Ibn Khaldun: The 'Ilm al-'Umran' Systems Sociology of Civilizational Rise-and-Fall & the Dialectical Paradigm of Dyna... | tools/json/scenarios_zh.json name_zh + tools/code_maps_en.json | companion `ibnkhaldun_H-IKD-160_modes.json`; scenarios_en name_en |
| H-ISC-362 | 阿维森纳（伊本·西那） | Avicenna (Ibn Sina): Systematic Corpus of the Canon of Medicine, Ontological Metaphysics and the 'Rationality-Revelat... | tools/json/scenarios_zh.json name_zh | scenarios_en name_en |
| H-GHZ-163 | 安萨里 | Al-Ghazali: The Four-in-One Paradigm of Theological-Sufi Synthesis, Philosophical Critique, and the Epistemology of C... | tools/json/scenarios_zh.json name_zh | companion `ghazali_H-GHZ-163_modes.json`; figure_names=安萨里; scenarios_en name_en; data/individuals/H-GHZ-163.json; do... |
| H-SUF-364 | 鲁米（贾拉勒丁·鲁米） | Rumi (Jalal al-Din Rumi): Poetic Mysticism's Universal Transformation, Grief-to-Love Alchemy and the 'Love' Ontology ... | tools/json/scenarios_zh.json name_zh | scenarios_en name_en |
| H-ZEL-001 | 周恩来 | Zhou Enlai | tools/json/scenarios_zh.json name_zh | scenarios_en name_en; docs/figures/H-ZEL-001.md |
| H-HLG-001 | 华罗庚 | Hua Luogeng | tools/json/scenarios_zh.json name_zh | figure_names=华罗庚; scenarios_en name_en; data/figures/H-HLG-001.json; docs/figures/H-HLG-001.md |
| H-MZ-001 | 晏阳初 / 孟子 / 墨子 (3 主张冲突, 待裁) | - | - | figure_names=晏阳初; data/individuals/H-MZ-001.json; data/figures/H-MZ-001.json; docs/figures/H-MZ-001.md |

### 4.2 现状证据 / 归类 / 建议动作

| code | DB 行 | shard | 轻索引 n | 发布统一索引 | sitemap | 归类 | 建议动作 | 既存卡 (④) |
|---|---|---|---|---|---|---|---|---|
| H-HYP-145 | id 134 / 空 | `web/public/data/figures/H-HYP-145.json` | 5 | scenario / name=H-HYP-145 | /figures/H-HYP-145/ x1 | ①可解析 | 回填 name_zh 为人名; 与 H-YYP-001 (现役命名行) 双码并存, 需船长裁定归一(保留其一, 另一遮蔽/归档), 不得两码同名并存 | 7 张: t_402214fb, t_604bbe41, t_1c079099 ... |
| H-WYX-146 | id 135 / 空 | `web/public/data/figures/H-WYX-146.json` | 5 | scenario / name=H-WYX-146 | /figures/H-WYX-146/ x1 | ①可解析 | 回填 name_zh 为人名; 同人另存 H-WYX-189/249 两条命名行, 去重纳入归一裁定 | 6 张: t_1a4d7d3d, t_774157f1, t_d0459bc1 ... |
| H-WX-147 | id 136 / 空 | `web/public/data/figures/H-WX-147.json` | 5 | scenario / name=H-WX-147 | /figures/H-WX-147/ x1 | ①可解析 | 回填 name_zh 为人名; 注意档名别名 H-WX-001 (docs/figures/H-WX-001.md), 归一裁定同批处理 | 6 张: t_33bd44f1, t_ffabbc87, t_663e6b4f ... |
| H-YLP-148 | id 137 / 空 | `web/public/data/figures/H-YLP-148.json` | 0 | scenario / name=H-YLP-148 | /figures/H-YLP-148/ x1 | ①可解析 | 回填 name_zh 为人名; 与 P4-ENG-004 归一裁定 | 6 张: t_8b5092b9, t_e7653d02, t_50dbd4d2 ... |
| H-SY-149 | id 138 / 空 | `web/public/data/figures/H-SY-149.json` | 5 | scenario / name=H-SY-149 | /figures/H-SY-149/ x1 | ①可解析 (现役人码已存在) | 回填或遮蔽: 该人物现役 payload 在 SUY; 本码与 H-SY-001 改名悬案 (phase19_summary.md L208/L476) 合并裁定 | 5 张: t_295a26ee, t_81cee7ca, t_a1555e53 ... |
| H-XMQ-151 | id 140 / 空 | `web/public/data/figures/H-XMQ-151.json` | 5 | scenario / name=H-XMQ-151 | /figures/H-XMQ-151/ x1 | ①可解析 | 回填 name_zh 为人名; 与 H-XMQ-299 归一裁定 | 6 张: t_3473280a, t_c90b812d, t_2752ca7f ... |
| H-CY-159 | id 148 / 空 | `web/public/data/figures/H-CY-159.json` | 0 | scenario / name=H-CY-159 | /figures/H-CY-159/ x1 | ①可解析 | 回填 name_zh 为人名; 建议另裁 H-CY 前缀归属 (陈云 H-CY-001 vs 陈毅 H-CY-159) 避免检索串档 | 6 张: t_3d85e587, t_3e6a5fe2, t_877edf3d ... |
| H-LXN-347 | id 368 / 空 | `web/public/data/figures/H-LXN-347.json` | 0 | scenario / name=H-LXN-347 | /figures/H-LXN-347/ x1 | ①可解析 | 回填 name_zh 为人名; 三码 (001/158/347) 归一裁定 | 6 张: t_elcano_elcano_batch_3_1787640880_2, t_9b8de959, t_d54dccae ... |
| H-LXN-001 | id 369 / 空 | `web/public/data/figures/H-LXN-001.json` | 5 | scenario / name=H-LXN-001 | /figures/H-LXN-001/ x1 | ①可解析 (附缺陷: 草稿错名未改) | 回填 name_zh 为人名; 同时修正 tools/json/H-LXN-001.json 与 scenarios_en 的错名键值 (phase19 L210/L477 已记录应改, 至今未落实) | 5 张: t_9b8de959, t_d54dccae, t_20869629 ... |
| H-IKD-160 | id 1001 / 空 | `web/public/data/figures/H-IKD-160.json` | 0 | scenario / name=H-IKD-160 | /figures/H-IKD-160/ x1 | ①可解析 (现役人码已存在) | 回填或遮蔽; 与 IKH 归一裁定 | 6 张: t_2a948786, t_b576841d, t_19440c82 ... |
| H-ISC-362 | id 1002 / 空 | `web/public/data/figures/H-ISC-362.json` | 0 | scenario / name=H-ISC-362 | /figures/H-ISC-362/ x1 | ①可解析 (现役人码已存在) | 回填或遮蔽; 与 H-ISN-001 归一裁定 | 2 张: t_elcano_elcano_batch_3_1787640880_2, t_serrano_阿维森纳_629779_1 ... |
| H-GHZ-163 | id 1003 / 空 | `web/public/data/figures/H-GHZ-163.json` | 0 | scenario / name=H-GHZ-163 | /figures/H-GHZ-163/ x1 | ①可解析 (现役人码已存在) | 回填 name_zh; 与 H-GHZ-001 归一裁定; 译名统一问题 (安萨里/加扎利/阿斋逊) 并入 Phase46-R 待裁清单第 3 条 | 2 张: t_elcano_elcano_batch_3_1787640880_2, t_e3f8cf8f ... |
| H-SUF-364 | id 1004 / 空 | `web/public/data/figures/H-SUF-364.json` | 0 | scenario / name=H-SUF-364 | /figures/H-SUF-364/ x1 | ①可解析 (无现役码, 全族最脆弱) | 回填/重建: 该人物无现役 figure 码, 无命名行, 无 figure_names 键; 仅存批次草稿 + H-RUM-365 companion. 建议按研究卡重建(或回填后进归一) | 2 张: t_elcano_elcano_batch_3_1787640880_2, t_serrano_鲁米_629779_3 ... |
| H-ZEL-001 | id 1045 / 空 | `web/public/data/figures/H-ZEL-001.json` | 5 | scenario / name=H-ZEL-001 | /figures/H-ZEL-001/ x1 | ①可解析 (现役人码已存在) | 回填或遮蔽; 与 ZhouEnLai 归一裁定; 同族另有 H-ZEL-153/306/325/332 四条命名行 | 6 张: t_24520b5d, t_27610c96, t_54a58cbc ... |
| H-HLG-001 | id 1046 / 空 | `web/public/data/figures/H-HLG-001.json` | 4 | figure / name=华罗庚 | /figures/H-HLG-001/ x0 | ①可解析 (本身即现役人码) | 无需回填名字 (人路由已正常); 处置对象=被遮蔽的 scenario 空行: 建议与 figures.index/DB 中的同名空行清档(保留 figure 行) | 6 张: t_53063e87, t_82d5994e, t_4d805d88 ... |
| H-MZ-001 | id 1056 / 空 | `web/public/data/figures/H-MZ-001.json` | 0 | scenario / name=H-MZ-001 | /figures/H-MZ-001/ x1 | ②是人·需核名 (三主张冲突待裁) | 船长裁定单一归属并清理键面: figure_names(H-MZ-001->晏阳初) vs 伴随包 H-MZ-001_modes(孟子) vs phase20_moci_research.md L142(墨子); Phase46-R ... | 2 张: t_6c92966b, t_e3f8cf8f ... |

说明: 全部 16 码 DB name_zh/name_en 为空串, shard 名字/描述为空, steps 为空; 15 码在预渲染路由表 `docs/architecture/web_p0_routes.json` 中为 scenario 且 body_text_chars=0 (空页), 仅 H-HLG-001 为 person (正文 16536 字符).

### 4.3 逐码备注 (现役别码 / 裁量点)

- **H-HYP-145** (黄炎培): 现役别码: H-YYP-001; 备注: 无 modes_data/figure_names 注册; tools/json/H-HYP-145.json 与 companion 均为 01 批次草稿
- **H-WYX-146** (吴有训): 现役别码: H-WYX-189 / H-WYX-249; 备注: figure_names 无该人名键; docs/figures/H-WYX-001.md 为 Phase19 命名别名档
- **H-WX-147** (王选): 现役别码: 无同人命名行 (H-WX-274 为王兴, 非同一人); 备注: 
- **H-YLP-148** (袁隆平): 现役别码: P4-ENG-004 (命名行); 备注: 
- **H-SY-149** (粟裕): 现役别码: SUY (现役 figure, 10 模式); 备注: Phase27 链已按 SuYuGeneral 重做入库 (t_e99041fc); 本码属历史残件
- **H-XMQ-151** (薛暮桥): 现役别码: H-XMQ-299 (命名行); 备注: docs/figures/H-XMQ-151.md 与 site_docs 预渲染页在; figure_names 无键
- **H-CY-159** (陈毅): 现役别码: 无现役模式载荷 (注意: H-CY-001 的 DB 行为陈云, 前缀族内易混); 备注: Phase19 链 (t_3d85e587 等) 标题称 H-CY-001, 但该码 DB 行现为陈云场景行 (figure_names: H-CY-001 -> 陈云) -- 标题与数据不一致, 需在裁定中说明
- **H-LXN-347** (李先念): 现役别码: H-LXN-158 (命名行) / H-LXN-001 (同族 husk); 备注: phase19_summary.md L210 以本件 companion 为正确数据源; batch_new_figures_research.md L573 有完整素材
- **H-LXN-001** (李先念 (legacy 草稿误作 毛先念)): 现役别码: H-LXN-158 / H-LXN-347; 备注: Phase19 全链 done (研究/落地/合并/QA/归档); docs/figures/H-LXN-001.md 与 site 预渲染页在
- **H-IKD-160** (伊本·赫勒敦): 现役别码: IKH (现役 figure, 10 模式); 备注: figure_names: IKH/IbnKhaldun/H-IKH-001 -> 该人名
- **H-ISC-362** (阿维森纳（伊本·西那）): 现役别码: H-ISN-001 (现役 figure, 10 模式); 备注: 无 companion 文件; 名字证据仅在 tools/json/scenarios_zh/en.json 与 code_maps_en
- **H-GHZ-163** (安萨里): 现役别码: H-GHZ-001 (现役 figure, 10 模式); 备注: 注册层最厚: figure_names(GHZ-163/GHZ-001)/code_maps(7)/data/individuals/docs/site 页均在; Phase46-R 报告第 5 节 #3 记录与 H-AlGhazal...
- **H-SUF-364** (鲁米（贾拉勒丁·鲁米）): 现役别码: H-RUM-365 (companion 深挖件称本码为 主卡); 备注: data/asia/individuals/rumi_H-RUM-365_modes.json 自述 同一人物主卡 H-SUF-364
- **H-ZEL-001** (周恩来): 现役别码: ZhouEnLai (现役 figure, 10 模式); 备注: Phase19 全链 done; docs/figures/H-ZEL-001.md 与 site 页在
- **H-HLG-001** (华罗庚): 现役别码: H-HLG-001 自身 (figure 路由在线正常); 备注: 唯一同时存在 figure 路由 (/minds/H-HLG-001, 10 模式) 与空 scenario 行的码; 空行只影响轻索引/DB 面向
- **H-MZ-001** (晏阳初 / 孟子 / 墨子 (3 主张冲突, 待裁)): 现役别码: 晏阳初->H-YC-001 (现役 figure); 孟子->H-MZ-165 (命名行) + H-MZ-001_modes 伴随键; 墨子->H-MO-001; 备注: data/figures/H-MZ-001.json(晏阳初 1890-1990) 与 data/figures/H-MZ-001_modes.json(孟子 前372-289) 同键冲突; data/individuals/H-MZ...

## 五, 异常码族矩阵

### SG 混大小写重复对

- 归类: ③异常码族 (重复对) + 名字可解析 (李光耀 / Lee Kuan Yew)
- 建议动作: 归一: 保留规范大写码并回填 name_zh, 清/遮蔽混大小写码(方向由船长裁); 与现役 H-LKY-001 的关系同步裁定
- 证据:
  - DB id 1024 / 687; shards 皆空名; modes [34,12,20,31] vs [303,10,157,153] (两代批次各带自身模式链接)
  - tools/json/SG-Lee-001.json name_zh=李光耀 (01 批次草稿); tools/json/SG-LEE-001.json name_zh=李光耀 (M639 新模草稿)
  - tools/PHASE_13_16_GLOBAL_COMPLETION_PLAN.md L85 登记 SG-LEE-001=李光耀/M303
  - 现役人码 H-LKY-001 (figure, 10 模式; figure_names LeeKuanYew/LEEKUANYEW/LKY/H-LKY-001)

| code | DB id | DB 名字 | modes | 轻索引 n | 统一索引 | legacy name_zh | tools/json 草稿 |
|---|---|---|---|---|---|---|---|
| SG-Lee-001 | 1024 |  | [34, 12, 20, 31] | 4 | scenario / SG-Lee-001 | 李光耀：从第三世界到第一世界的『实用主义治国术』与长期战略工程化范式 | 是 |
| SG-LEE-001 | 687 |  | [303, 10, 157, 153] | 4 | scenario / SG-LEE-001 | 李光耀/新加坡/从第三世界到第一/法治：从第三世界到第一与法治精英 | 是 |

### MY 混大小写重复对

- 归类: ③异常码族 (重复对 + 字段错位: 英文装入 name_zh) + 名字可解析 (马哈蒂尔)
- 建议动作: 归一: 保留大写码并回填中文名(修正英文入 name_zh 错位), 清/遮蔽混大小写码; 无现役人码, 建议回填后进站点
- 证据:
  - DB id 1025 (空名, 4 模式) / 1038 (name_zh=name_en=Mahathir Mohamad 英文入中文位, 0 模式)
  - tools/json/MY-Mah-001.json name_zh=马哈迪·穆罕默德...; tools/json/MY-MAH-001.json name_zh=马哈蒂尔
  - tools/PHASE_13_16_GLOBAL_COMPLETION_PLAN.md L69 登记 MY-MAH-001=马哈蒂尔/M292

| code | DB id | DB 名字 | modes | 轻索引 n | 统一索引 | legacy name_zh | tools/json 草稿 |
|---|---|---|---|---|---|---|---|
| MY-Mah-001 | 1025 |  | [34, 12, 20, 31] | 4 | scenario / MY-Mah-001 | 马哈迪·穆罕默德：从殖民医生到现代化推动者的『科技民族主义』与后殖民治理范式 | 是 |
| MY-MAH-001 | 1038 | Mahathir Mohamad | [] | 0 | scenario / Mahathir Mohamad | - | 是 |

### JP 单侧混大小写

- 归类: ③异常码族 (单侧混大小写, 缺规范码) + 名字可解析 (西乡隆盛)
- 建议动作: 码规范化 + 回填; 无现役人码
- 证据:
  - DB id 1026 (空名, 3 模式); JP-SAS-001 不存在 (全链实测缺失)
  - tools/json/JP-Sas-001.json name_zh=西乡隆盛; tools/json/scenarios_zh.json 同名条目
  - name_en 附注 recorded as batch plan 记录差异

| code | DB id | DB 名字 | modes | 轻索引 n | 统一索引 | legacy name_zh | tools/json 草稿 |
|---|---|---|---|---|---|---|---|
| JP-Sas-001 | 1026 |  | [19, 31, 7] | 3 | scenario / JP-Sas-001 | 西乡隆盛：从萨摩武士到明治维新『西南战争』的『武士道复兴法』与道德政治工程化范式 | 是 |

### UZ 单侧混大小写

- 归类: ③异常码族 (单侧混大小写, 缺规范码) + 名字可解析 (乌鲁格别克)
- 建议动作: 码规范化 + 回填; 无现役人码
- 证据:
  - DB id 1027 (空名, 3 模式); UZ-ULU-001 不存在
  - tools/json/UZ-Ulu-001.json name_zh=乌鲁格别克
  - 同前缀其它码 (UZ-KAR/TEM/MED/SILK/EMP/AUT-001) 均为大写规范

| code | DB id | DB 名字 | modes | 轻索引 n | 统一索引 | legacy name_zh | tools/json 草稿 |
|---|---|---|---|---|---|---|---|
| UZ-Ulu-001 | 1027 |  | [34, 12, 20] | 3 | scenario / UZ-Ulu-001 | 乌鲁格别克：萨马尔罕天文台的『科学革命法』与伊斯兰文艺复兴治理范式 | 是 |

### RW-KAG 无零填充序号族

- 归类: ③非人 (死件·模板占位废件 27 件) + 同族保留件需回填 (RW-KAG-001=卡加梅)
- 建议动作: 整族清档: 27 件模板废件走在链清除 (DB/shards/figures.index/unified/sitemap, 先备份后清除); RW-KAG-001 保留并回填 name_zh
- 证据:
  - DB id 951-977 (RW-KAG-1..27) + 844 (RW-KAG-001); 全部空名; shards/figures.index/unified/sitemap 在链
  - tools/json/RW-KAG-1..27: 模板占位内容 (name_zh=安第斯/南锥体/中美洲历史人物N; description=第N位历史人物...; wiki_id=Figure_N;Andean;South_American;Central_American; 与 RW(卢旺达) 前缀不符)
  - tools/json/RW-KAG-001: 真实人物条目 name_zh=卡加梅/卢旺达/...(M576)

| code | DB id | DB 名字 | modes | 轻索引 n | 统一索引 | legacy name_zh | tools/json 草稿 |
|---|---|---|---|---|---|---|---|
| RW-KAG-1 | 951 |  | [584] | 1 | scenario / RW-KAG-1 | 安第斯/南锥体/中美洲历史人物1 | 是 |
| RW-KAG-2 | 952 |  | [525] | 1 | scenario / RW-KAG-2 | 安第斯/南锥体/中美洲历史人物2 | 是 |
| RW-KAG-27 | 977 |  | [576] | 1 | scenario / RW-KAG-27 | 安第斯/南锥体/中美洲历史人物27 | 是 |
| RW-KAG-001 | 844 |  | [576] | 1 | scenario / RW-KAG-001 | 卡加梅/卢旺达/种族灭绝/重建/强人/奇迹/保罗/卡加梅 | 是 |

## 六, 547 个非 H 空名 (背景核对)

- 总数 547; 其中 legacy 有 name_zh 的 537 条, 无名字键的 10 条 (南部非洲批次: BW-KHA-001, NA-NUJ-001, SZ-MSW-001, ZW-MUG-001, ZA-ZUM-001, BW-MAS-001, LS-MOS-001, MG-RAV-001, NA-GEO-001, ZW-CHA-001).

| 严格分类 | 计数 | 含义 |
|---|---|---|
| code_as_name | 104 | legacy name_zh 即代码本身 (占位行, desc 多为 待补充信息, 计 108 条) |
| name_title | 230 | 人名+主题 题名式 (含人名可提取) |
| topic_slash | 169 | 关键词串 (斜杠分隔主题, 非人名) |
| plain_name | 34 | 纯人名 (如 ZA-MAN-001 纳尔逊-曼德拉, ES-FRA-001 佛朗哥等) |
| empty_name_zh | 10 | legacy 亦无名字键 |

- 国家前缀 Top12: RW=28, US=16, JP=14, IL=14, IN=12, AU=12, TR=12, DE=11, KR=9, IR=9, UK=8, RU=8
- 口径: 547 为场景命名空间 (国家/主题码) 空名行, 全部由同一装载器键漂移造成; 其中 537 条 legacy 有 name_zh (人名/题名/主题串), 10 条 (南部非洲批次) legacy 亦无名字键. 此族不含 H-* 人码, 属场景侧字段治理, 与 16 H-* 人名恢复分开处置

## 七, 与既有卡重叠映射 (④)

| 卡号 | 标题 | 状态 | 重叠面 |
|---|---|---|---|
| t_e3f8cf8f | [Phase46-R] figure 文件字段缺陷审计与修复 | done | data/figures 层字段缺陷 (empty_name/bad_code/错名/重复); 待人工 7 条含 H-MZ-001 键冲突, H-AlGhazali-001 译名 |
| t_34a97fec | [Phase31-R4R5] 脏人物名清理 + QUARANTINE 名单共享 | done | 名录脏名清理先例 (线上口径) |
| t_dd99310c | [Phase30-C1-fix] 公开名录脏数据 | done | index.unified 脏行修复先例 (模板占位行) |
| t_261185a8 | [Phase21-R7 C组核名] 待核身份研究 | done | 核名方法论/证据链口径 |
| t_8183b8fd | [Phase21-R8 C组遗留] 微收口 | done | figure_names 清档先例 |
| t_151265db | [Phase21-R7 旁项] 根目录/发布仓旧档残留调查与处置 | done | tools/json 旧档 (含本卡涉及的 SG-Lee/MY-Mah/JP-Sas/UZ-Ulu/RW-KAG/H-MZ-001 草稿) 现状=legacy_draft/uncertain(untouched) |
| t_3669eb4a | [Phase21-R8 遗留清档] H-AZJ-345 在链残件全链清除 | todo | 在链清除流程先例 (本卡 27 件 RW 模板废件可复用同流程) |

- 16 码各自的 Phase19/Phase27 批次链卡号已逐码列在 JSON `matrix[].cards` (本节只列跨卡代表).
- 16 码对应的归档批次卡 (archived): `t_elcano_elcano_batch_1_1787640880_0` (黄炎培/薛暮桥/吴有训/王选/袁隆平/粟裕), `t_elcano_elcano_batch_2_1787640880_1` (周恩来/华罗庚等), `t_elcano_elcano_batch_3_1787640880_2` (李先念/陈毅/伊本-赫勒敦/阿维森纳/加扎利/鲁米).

## 八, 建议动作清单 (供船长切修复卡, 本卡不执行)

1. **回填卡 (A 类, 人名恢复)**: 按第四节 4.1 证据回填 15 码的 name_zh/name_en (含 shard/DB/轻索引全链), 同时按裁定结果处理现役别码归一.
2. **归一裁定卡 (B 类, 双码并存)**: H-HYP-145 vs H-YYP-001; H-WYX-146 vs 189/249; H-YLP-148 vs P4-ENG-004; H-XMQ-151 vs 299; H-LXN-001/158/347; H-ZEL-001 vs 153/306/325/332; H-HLG-001 空行 vs figure 行; H-GHZ-163 vs H-GHZ-001; H-ISC-362 vs H-ISN-001; H-IKD-160 vs IKH; H-SY-149 vs SUY.
3. **H-MZ-001 专项裁定卡 (C 类)**: 三主张 (晏阳初/孟子/墨子) + 键面 (H-MZ-001_modes 伴随包 vs 主文件) 清理, 并入 Phase46-R 待裁第 5 条.
4. **H-SUF-364 重建/回填卡 (D 类)**: 鲁米全族最脆弱 (无现役码, 无注册键).
5. **异常码族治理卡 (E 类)**: SG/MY 重复对归一 + 字段错位修正; JP/UZ 码规范化; RW-KAG-1..27 在链清除 (27 件, 先备份后清, 流程复用 H-AZJ-345 清档卡).
6. **场景侧 547 空名治理卡 (F 类, 可选)**: 统一按 legacy name_zh 回填或按国家批次补名 (避免站点继续以代码为名).
7. **微修卡 (G 类)**: `tools/json/H-LXN-001.json` 与 `scenarios_en` 错名 (phase19 L210/L477 已记录); `data/asia/individuals` 含换行符的异常目录名.

## 九, 核验方法与复跑要点

- 本地脚本全量对账 DB/figures.index/shard/unified/legacy 五层 (脚本与输出留档 scratch/w4)
- 两仓 parity: 16 分片与 figures.index.json 逐字节一致 (sha256)
- git status --short 本卡前后对照 (仅新增本报告 2 件)

- 两仓 parity: 16 件分片 + figures.index.json 与发布仓逐字节一致; figures.index.json sha256 前16: `f0eded8cd6b59245`.
- 本卡零库写: 仅新增本报告 2 件; 对账脚本与原始输出留档于执行机 scratch (scratch/w4/).

## 十, 开放项 (待船长裁定)

1. H-MZ-001 三主张裁定 (晏阳初/孟子/墨子)
2. H-SUF-364 无现役码, 是否重建
3. H-SY-149 改名悬案 (H-SY-001) 与新残件处置
4. JP/UZ 规范码命名 (JP-SAS-001/UZ-ULU-001 是否采用)
5. 547 场景侧空名: 统一回填 legacy name_zh 或按国家批次补名
6. RW-KAG 27 件清档执行卡 (在链清除+备份)
7. tools/json/H-LXN-001.json 错名修正
8. data/asia/individuals 内异常目录名 (含换行符) 清理

