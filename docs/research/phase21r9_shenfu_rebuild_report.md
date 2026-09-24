# Phase21-R9 沈复 H-SHF-001 重建落盘报告

- 卡：t_b6d4c0ee（Phase21-R9 沈复重做链；链条：素材包 t_d78053e7 -> 本卡 -> 合并卡）
- 日期：2026-09-24
- 素材包（SHF-1）：docs/research/phase21r9_shenfu_sourcing_report.md / .json（见证 W1-W30；引文 35/35 逐条落源）
- 落盘生成器：tools/build_phase21r9_shenfu.py；独立核验：verify_phase21r9_shenfu.py
- 结论：10 模式 M-SHF-001~010 落盘完成；主库零写入；独立核验 74 PASS / 0 FAIL；credibility gate --hard-fail exit 0

## 0. 核验摘要

| 面 | 结果 |
| --- | --- |
| 条目 | M-SHF-001~010，10 条；全部全新码（legacy_mode_id 全空、零复用） |
| 引文 | 35/35 为素材包 §三 quotes 子串且全覆盖于条目文本；10/10 key_quote 见证强归一化命中 |
| 见证索引 | 35 件副本 sha256 全对；复跑 verify_quotes.py 得 QUOTES 35/35 OK |
| 查重 | M-SHF/H-SHF 外部 0 碰撞；主库登记面 12 件 0 命中（零库写） |
| 归档 | H-HAN-001 系列 3 件 sha256 未变（字节冻结、不唤醒、不引用） |
| 片段白名单 | 11 条，全部可回溯素材包 md/json |
| 差异裁定 | 素材包 §八 14 条逐条落实（见 §3.1） |
| 场景 | 本链零搬迁；新前缀 C-SHF-001~010 建议、全库 0 占用 |
| 独立核验 | 74 PASS / 0 FAIL（docs/research/phase21r9_shenfu_verify_evidence.json） |
| 门禁 | credibility gate --hard-fail：0 硬失败、exit 0；数据面 sha256 前缀 b44d8f885a8371a0 |

## 1. 落盘产物清单（12 件，sha256 全量）

| 产物 | sha256 |
| --- | --- |
| `data/figures/H-SHF-001.json` | `592a422bce86102dfc1b7f2a9515a71c969c41756cfca35bd689f1c86d79fe14` |
| `data/individuals/H-SHF-001.json` | `0c7f889b4524f1a4a31c24a22725f44ea65ad750376411534ac9c94172c90c43` |
| `data/individuals/H-SHF-001_modes.json` | `7c27ef5c884790ba9b3a119927f025ac610c66ae368757f23bbe22df95f72bdd` |
| `docs/scratch/legacy20_r9_shenfu_landing/category_mapping.tsv` | `d8333894832a9dec6da44ebd3dfd565eae4009af8c8ac0616240c9847188968a` |
| `docs/scratch/legacy20_r9_shenfu_landing/combined_library_entries.json` | `b44d8f885a8371a09ac261b03600c209ab5015dc89f1a2eee1c29b115244b471` |
| `docs/scratch/legacy20_r9_shenfu_landing/figures/H-SHF-001.json` | `592a422bce86102dfc1b7f2a9515a71c969c41756cfca35bd689f1c86d79fe14` |
| `docs/scratch/legacy20_r9_shenfu_landing/id_mapping.tsv` | `97938593ddc3f2983383edb6c63e5705a41d36cd264044d555a2023ce4541f42` |
| `docs/scratch/legacy20_r9_shenfu_landing/individuals/H-SHF-001.json` | `0c7f889b4524f1a4a31c24a22725f44ea65ad750376411534ac9c94172c90c43` |
| `docs/scratch/legacy20_r9_shenfu_landing/individuals/H-SHF-001_modes.json` | `7c27ef5c884790ba9b3a119927f025ac610c66ae368757f23bbe22df95f72bdd` |
| `docs/scratch/legacy20_r9_shenfu_landing/modes_library_entries.json` | `f465806ab53a0d1a53b16f679d42fa4762354e66d4cc7112405f9746aff1edfa` |
| `docs/scratch/legacy20_r9_shenfu_landing/scenario_notes.json` | `7f01d533e83638a7c1f8337f97438bed9852064f25f7e3974ac0ad46a8be63cb` |
| `docs/scratch/legacy20_r9_shenfu_landing/top_block_proposal.json` | `44e25f05265c939245424da1bdc485bdd847d3038d534a02d508990bf2de591e` |

冻结副本位于 docs/scratch/legacy20_r9_shenfu_landing/，与 data 侧逐字节一致（核验 A04-A06；A13 复核 evidence 与 manifest 同字节）。

## 2. 逐条结果（10 条）

| # | 代码 | 命名 | 类目 | key 引文 | 来源标记 | 字数 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | M-SHF-001 | 实录真情法 | 文艺审美 | q2 | 同前（W8@116） | 39 |
| 2 | M-SHF-002 | 物外之趣法 | 文艺审美 | q1 | 卷二·闲情记趣开篇（W8@33） | 38 |
| 3 | M-SHF-003 | 独出己见法 | 认识论逻辑 | q1 | 卷四·浪游记快（W8@89；句接「余游幕三十年来」段） | 47 |
| 4 | M-SHF-004 | 就事论事法 | 方法论通用 | q1 | 卷二（W8@3599） | 32 |
| 5 | M-SHF-005 | 布衣菜饭法 | 伦理修养 | q2 | 卷一（W8@4996） | 30 |
| 6 | M-SHF-006 | 情之所钟法 | 心理洞察 | q1 | 卷一（W8@3955） | 34 |
| 7 | M-SHF-007 | 知己同心法 | 伦理修养 | q1 | 卷一（W8@4150） | 34 |
| 8 | M-SHF-008 | 坎坷自省法 | 心理洞察 | q1 | 卷三·坎坷记愁开篇（W8@33） | 39 |
| 9 | M-SHF-009 | 得画意法 | 文艺审美 | q1 | 卷二（W8@793） | 11 |
| 10 | M-SHF-010 | 浪游心得法 | 方法论通用 | q1 | 卷四（W8@57） | 38 |

### 2.1 引文全文（10 条 key_quote 与出处）

**M-SHF-001 实录真情法**

> 所愧少年失学，稍识之无，不过记其实情实事而已，若必考订其文法，是责明于垢鉴矣。
>
> —— 同前（W8@116）

**M-SHF-002 物外之趣法**

> 余忆童稚时，能张目对日，明察秋毫。见藐小微物，必细察其纹理，故时有物外之趣。
>
> —— 卷二·闲情记趣开篇（W8@33）

**M-SHF-003 独出己见法**

> 余凡事喜独出己见，不屑随人是非，即论诗品画，莫不存人珍我弃、人弃我取之意，故名胜所在，贵乎心得
>
> —— 卷四·浪游记快（W8@89；句接「余游幕三十年来」段）

**M-SHF-004 就事论事法**

> 贫士起居服食以及器皿房舍，宜省俭而雅洁，省俭之法曰“就事论事”。
>
> —— 卷二（W8@3599）

**M-SHF-005 布衣菜饭法**

> 君画我绣，以为诗酒之需。布衣菜饭，可乐终身，不必作远游计也。
>
> —— 卷一（W8@4996）

**M-SHF-006 情之所钟法**

> 余曰：“始恶而终好之，理之不可解也。”芸曰：“情之所钟，虽丑不嫌。”
>
> —— 卷一（W8@3955）

**M-SHF-007 知己同心法**

> 其癖好与余同，且能察眼意，懂眉语，一举一动，示之以色，无不头头是道。
>
> —— 卷一（W8@4150）

**M-SHF-008 坎坷自省法**

> 人生坎坷何为乎来哉？往往皆自作孽耳，余则非也，多情重诺，爽直不羁，转因之为累。
>
> —— 卷三·坎坷记愁开篇（W8@33）

**M-SHF-009 得画意法**

> 全在会心者得画意乃可。
>
> —— 卷二（W8@793）

**M-SHF-010 浪游心得法**

> 惜乎轮蹄征逐，处处随人，山水怡情，云烟过眼，不道领略其大概，不能探僻寻幽也。
>
> —— 卷四（W8@57）

## 3. 裁定执行记录

### 3.1 素材包 §八 差异 14 条落实对照

| # | 事项 | 差异要点 | 本链落实 |
| --- | --- | --- | --- |
| 1 | 卷二·点缀盆中花石 | 甲：维基文库底本「邪可以入画」（W8）；乙：通行本「小景可以入画」（W27＋检索快照） | 主选「会心者得画意」「戒匠气」两句作骨架；异文句以校注尾注双注登记（M-SHF-009 尾注；caveats 第 6 条） |
| 2 | 杨引传序开头 | 甲：W18「—书」/W19「-书」；乙：通行「一书」 | 本链未引杨序全句；口径登记：如需引用，自「余于郡城冷摊得之」起 |
| 3 | 王韬跋 | 甲：弢园本「笔墨之间/山水林树」；乙：独悟庵本「笔墨间/水石林树」 | 本链未引王跋；口径登记：如需引用，按 W17 含校记原样呈现 |
| 4 | 王跋人名缺字 | 甲：W18「杨□补」；乙：「杨甦补」（杨引传） | 本链不涉该缺字引文；口径登记：缺字处注 □ 为「甦」（杨甦补） |
| 5 | 潘麐生名 | 甲：W18 误「潘麖生」；乙：通行「潘麐生」 | 采用「潘麐生」写名（M-SHF-009 用例；序诗句源 W18） |
| 6 | 管贻葄/管贻萼 | 甲：诗题者实名管贻葄；乙：常被误作其堂弟管贻萼 | 本链未出现该人名面；口径登记：如引用一律「管贻綄」（W30 辨正） |
| 7 | 卷五篇名 | 甲：《中山记历》（W29/W15）；乙：《中山纪历》（W18 序） | 图鉴篇目主用《中山记历》并加注（H-SHF-001 representative_works / caveats） |
| 8 | 卷六篇名 | 甲：初版「养生记道」；乙：足本改「养生记逍」 | 伪作鉴定按两题并存登记（初版《养生记道》、足本《养生记逍》；W15 辨正），不升格为真迹文本 |
| 9 | 芸诗句 | 甲：正文「秋侵人影瘦，霜染菊花肥」；乙：管诗引「秋深人瘦菊花肥」 | 两式各归出处：正文句与管诗引分列、不混用（caveats 第 6 条；M-SHF-005 用例） |
| 10 | 陈寅恪引文 | 甲：W22 学术源；乙：W21 媒体转引（标点微异） | 以 W22 学术源为准；W21 作同源转引另注（M-SHF-001 用例 attr 已标「转引：W22」） |
| 11 | 生卒写法 | 甲：维基「1763年12月26日—？」；乙：工具书「1763～?」 | 只写年（1763）；精确日仅以「折算」注出现（historical_significance 注文） |
| 12 | 卷五/卷六性质 | 甲：维基文库「偽續/軼」；乙：旧说「已佚」 | 两层表述：卷五/卷六原佚、现传系伪续（caveats 第 4 条） |
| 13 | 林语堂评语中译 | 甲：「中国文学中最可爱的女人」（流通）；乙：「中国文学中所记的女子中最为可爱的一个」（W16）/「中国文学上一个最可爱的女人」（W10 引汉英对照本序） | 评语一律标转引与版本；英文原文未成证、不入正文（M-SHF-005 用例；caveats 第 5 条） |
| 14 | 卷五伪续抄源 | 甲：李鼎元《使琉球记》（W23 主流）；乙：「赵介山所著《使琉球记》」（W15） | 卷五伪续抄源登记：主用李鼎元说，如需引注按异说加注；本链未落该文本面 |

### 3.2 旧件与旧码处置

- H-HAN-001 系列 3 件维持 data/figures/_duplicates/ 归档：不唤醒、不引用、字节零改动；sha256 复核见 §5.1 的 H 组。
- 本链全程未复用任何旧码；M-351 至 M-358 面在数据与落地件零出现。旧场景载荷不存在，处置记录为空集（I 组核验）。

### 3.3 归属与引文口径

- 转引层（林语堂评语、陈寅恪引文、俞平伯序、胡不归小引等）一律保留转引链、不升格为沈复原文；评语英文原文未成证，不引。
- 卷五/卷六红线：原佚、现传系伪续；任何题材不采其文本（caveats 第 4 条）。
- 「名复」标疑似并注；序释层口径登记。

## 4. 片段白名单登记（11 条）

| 片段 | 归属 | 登记理由 |
| --- | --- | --- |
| 「如实」 | M-SHF-001 | 素材包语句（非引文段；构建期已核为素材包 md/json 子串） |
| 「心之所向」 | M-SHF-002 | 素材包语句（非引文段；构建期已核为素材包 md/json 子串） |
| 「心之所向，则或千或百」 | M-SHF-002 | 素材包语句（非引文段；构建期已核为素材包 md/json 子串） |
| 「唯两齿微露」 | M-SHF-005 | 素材包语句（非引文段；构建期已核为素材包 md/json 子串） |
| 「心证」 | M-SHF-006 | 素材包语句（非引文段；构建期已核为素材包 md/json 子串） |
| 「丑学」 | M-SHF-006 | 素材包语句（非引文段；构建期已核为素材包 md/json 子串） |
| 「同癖好、同耳目」 | M-SHF-007 | 素材包语句（非引文段；构建期已核为素材包 md/json 子串） |
| 「女扮男装」 | M-SHF-007 | 素材包语句（非引文段；构建期已核为素材包 md/json 子串） |
| 「性格」 | M-SHF-008 | 素材包语句（非引文段；构建期已核为素材包 md/json 子串） |
| 「邪可以入画」 | M-SHF-009 | 素材包语句（非引文段；构建期已核为素材包 md/json 子串） |
| 「冒雪登楼」 | M-SHF-010 | 素材包语句（非引文段；构建期已核为素材包 md/json 子串） |

## 5. 核验与门禁结果

### 5.1 独立核验

核验脚本 verify_phase21r9_shenfu.py 共 74 项：A 文件与解析 13、B 条目不变量 9、C 引文对包 11、D 见证强归一化 11、E 见证 sha 2、F 片段白名单与禁字 5、G 查重与残留 3、H 归档与主库 6、I 场景与命题件 3、J figure 层 8、K 报告 3；合计 74 PASS、0 FAIL、0 WARN；终轮复跑明细存 verify_evidence.json 与核验输出。

### 5.2 门禁与引文复跑

- credibility gate --hard-fail：数据面 = 落盘包 combined_library_entries.json；0 硬失败、exit 0；D3 豁免生效、豁免 0 条；数据面 sha256 = b44d8f885a8371a09ac261b03600c209ab5015dc89f1a2eee1c29b115244b471；gate.txt 存全文。
- 引文复跑：witness/verify_quotes.py 输出 QUOTES 35/35 OK；quote_verification_final.json sha256 复跑前后一致；无漂移、无就地覆盖。

## 6. 边界与遗留

### 6.1 合并卡范围（本卡不执行）

- M-SHF-001~010 入 data/modes_data.json（先备份后合并）
- figure 注册：code_maps / figure_names / scenario_tags / scenarios（zh+en）
- 顶层块 H-SHF-001 按 top_block_proposal.json 新增（原块缺失则新增）

### 6.2 登记面

- docs/figures/H-BG-001.md 存在 1 处 H-HAN-001 文字提及；grep -c 复核 = 1，与素材包 isolation 登记一致；随合并卡或清理卡处理。
- 素材包 open_items.pending_decisions 6 项（009c 用字、王跋双版本呈现、伪续呈现层级、卒年表述模板、梅逸直引一手、「名复」标疑似）均已按 §3.1 双注或口径登记。
- 素材包 §1.6 疑史料《海国记》与琉球之行各说按转引层登记，不升格。

### 6.3 未动面

- 主库 12 件（modes_data / code_maps / code_maps_en / scenario_tags / scenarios_zh / scenarios_en / figure_names 及 tools 副本）、归档 3 件、备份面；均零写入；复核见 H 组。

## 7. 证据与产物路径

- data/figures/H-SHF-001.json；data/individuals/H-SHF-001.json、H-SHF-001_modes.json
- data/audit/phase21r9_shenfu_landing_manifest.json；docs/research/phase21r9_shenfu_landing_evidence.json（同字节副本）
- docs/scratch/legacy20_r9_shenfu_landing/（九件：entries / combined / figure / individuals 两件 / id_mapping / category_mapping / scenario_notes / top_block_proposal）
- tools/build_phase21r9_shenfu.py；verify_phase21r9_shenfu.py
- docs/research/phase21r9_shenfu_verify_evidence.json；docs/research/phase21r9_shenfu_gate.txt；本报告

## 8. 提交回执

- 工作仓提交：59bc5471；19 件、8521 行新增，为本链主提交。
- 提交后复跑：独立核验 74 PASS 与 0 FAIL（终轮）；见证副本零漂移；引文复跑 35/35 全部通过。
- 回执补记提交：本节更新与核验证据刷新随之入库

