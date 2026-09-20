# Phase42-Z4 证据：D5 收口（生卒年取值面 + 英文镜像口径）

> 卡：`t_c66b11ff`（[Phase42-Z4] D5 收口：补 56 figure 生卒年 + 修 _en 字段盲区 + 如实标注残留）
> 日期：2026-09-21 · 规则唯一实现：`tools/credibility_gate.py` · 方案文档：`docs/planning/credibility_framework.md` §10.6
> 纪律：本文所有数字都来自下面贴出的**真实命令与原始输出**；补不到日期的 figure 一律**明确列为无日期**，
> 不算「已覆盖」。

---

## 0. 结论摘要（先说人话）

| 指标 | 修复前（Phase41-Z3） | 修复后（Phase42-Z4） |
|---|---|---|
| 生卒年取值键 | 265 | **616** |
| 可判定模式（figure 有生卒年） | 1132 | **2318** |
| 扫描到的 4 位年份 token | 2110 | **8557** |
| `tokens=0` 模式 | 2292 / 2888 = **79.4%** | 1546 / 2888 = **53.5%** |
| └ 「该 figure 无生卒年」 | 1756 | **570** |
| └ 「文本无 4 位年份」 | 536 | **976** |
| `clean` | 595 | **1341** |
| `undetermined` | 2292 | **1546** |
| `conflict` | 1 | **1（无新增）** |
| 人工抽检真矛盾 | — | 32 条边界候选逐条判读：**0 条真矛盾**（唯一上报项 M-NEW-007 为误报） |

**仍然不可判定的部分（不淡化）**：55 个 figure / 570 条模式无日期（48 个无 figure 文件 + 7 个有文件但缺字段）；
117 条「有生卒年但年份只落在未扫描字段」（`era` 106 / `representative_figures` 9 / `key_quote_context*` 4 /
`domain_*` 2 / `modern_applications_en` 1）；`verification` 字段的年份是审计时间戳，**不纳入**。

---

## 1. 修复前原始输出（`git show HEAD:tools/credibility_gate.py`，即 Phase41-Z3 版本）

```text
$ python3 /tmp/z4before/tools/credibility_gate.py --data-path data/modes_data.json --legacy-report
--- D5 时间线矛盾（生卒年 × 文本年份，Phase40-Z2）---
  生卒年可用人物: 265 个（data/figures/*.json，含字符串/公元前纪年解析）
  可判定模式: 1132 条（figure 有生卒年）
  扫描到的 4 位年份 token: 2110 个
  conflict             1
  clean              595
  undetermined      2292
  不可判定（逐类计数，禁止当成「零缺陷」）:
    out-of-window                                              206
    name-not-in-context                                         44
    field-not-claim                                             24
    source-marker                                                1
  D5 命中（本人叙述字段里的年份落在生卒年之外）:
    M-NEW-007  representative_cases_zh=1749  动差一半：牛顿未解决，Clairaut 1749 年以摄动级数升阶解决——方法误差而非理
  说明: 判定顺序 = 生卒年可用 -> 4 位年份 -> 生涯带 [生年-40, 卒年+30] -> 字段为本人叙述字段 -> 年份与人物名同现(±20 字) -> 无文献/余波/背景标记。任一环不满足即进「不可判定」并给出理由。
```

> 该版本 `load_figure_lifespans()` 的取值键 = `doc["figure_code"] or doc["code"] or doc["id"]` 的第一个非空值；
> `parse_year_value()` 只认 `约?前N` / `约?-N`。`D5_SCAN_FIELDS` 只含中文字段。

## 2. 修复后原始输出

```text
$ python3 tools/credibility_gate.py --legacy-report
--- D5 时间线矛盾（生卒年 × 文本年份，Phase40-Z2 / Phase42-Z4）---
  生卒年装载: data/figures/*.json 扫 347 个文件 → 可用取值键 616 个；年份不完整/不可解析 53 个文件；键冲突丢弃 3 个键
    键冲突丢弃: Modern         data/figures/H-AN-001.json:birth_year/death_year[1900, 1970] vs data/figures/H-CHB-001.json:birth_year/death_year[1904, 1989]
    键冲突丢弃: Han            data/figures/H-BG-001.json:birth_year/death_year[32, 92] vs data/figures/H-HAN-001.json:birth_year/death_year[-100, 180]
    键冲突丢弃: H-MZ-001       data/figures/H-MZ-001.json:birth_year/death_year[1890, 1990] vs data/figures/H-MZ-001_modes.json:birth_year/death_year[-372, -289]
  生卒年可用人物: 616 个（data/figures/*.json，含字符串/公元前纪年解析）
  可判定模式: 2318 条（figure 有生卒年）
  扫描到的 4 位年份 token: 8557 个
  conflict             1
  clean             1341
  undetermined      1546
  tokens=0 的成因拆分（禁止把「无生卒年」读成「已覆盖 / 零缺陷」）:
    no-four-digit-year-in-text                                 976
    no-lifespan-for-figure                                     570
  不可判定（逐类计数，禁止当成「零缺陷」）:
    out-of-window                                              521
    name-not-in-context                                        163
    field-not-claim                                             61
    source-marker                                               10
    background-marker                                            2
  D5 命中（本人叙述字段里的年份落在生卒年之外）:
    M-NEW-007  representative_cases_zh=1749  动差一半：牛顿未解决，Clairaut 1749 年以摄动级数升阶解决——方法误差而非理
  说明: 判定顺序 = 生卒年可用 -> 4 位年份 -> 生涯带 [生年-40, 卒年+30] -> 字段为本人叙述字段 -> 年份与人物名同现(±20 字) -> 无文献/余波/背景标记。任一环不满足即进「不可判定」并给出理由。
  取文本口径（Phase42-Z4）: 中英镜像字段同扫 —— definition_zh, process_zh, representative_cases_zh, definition_en, process_en, representative_cases_en, source_chapter, key_quote_zh, key_quote_en
```

`tokens=0` 的成因拆分是本期的关键改动之一：修复前这个数字把「文本里没有年份」与「该 figure 没有生卒年」
混成一本账，读起来像「已覆盖」——现在两者分开计数。

## 3. 补数清单（可重入，逐条 provenance）

```text
$ python3 tools/backfill_lifespans.py
=== 生卒年补数（Phase42-Z4）===
扫描: data/figures/*.json 347 个文件
取值面: 旧口径 266 个键 → 新口径 616 个键（+350）
键冲突丢弃: 3 个键
  丢 Modern       data/figures/H-AN-001.json:birth_year/death_year[1900, 1970]  vs  data/figures/H-CHB-001.json:birth_year/death_year[1904, 1989]
  丢 Han          data/figures/H-BG-001.json:birth_year/death_year[32, 92]  vs  data/figures/H-HAN-001.json:birth_year/death_year[-100, 180]
  丢 H-MZ-001     data/figures/H-MZ-001.json:birth_year/death_year[1890, 1990]  vs  data/figures/H-MZ-001_modes.json:birth_year/death_year[-372, -289]
有文件的年份不可用: 53 个文件（birth-after-death, missing-birth-or-death-field, year-not-parseable）
模式侧覆盖: figure 111 → 230 个 / 模式 1132 → 2318 条（全库 2888 条）
本次修复新覆盖 figure: 119 个（逐条 provenance）
仍然无日期 figure: 55 个（模式 570 条）—— 明确列出，不算已覆盖
清单已写: data/audit/lifespan_backfill.json
```

- 完整机读清单：`data/audit/lifespan_backfill.json`（逐 figure 的 `birth_year` / `death_year` / `provenance`，
  键冲突、无日期清单，以及 `--check` 用的比对基准）。
- **无日期 figure 的完整名单**（48 个无文件）：``, `AMP`, `ARR`, `BAI`, `BAN`, `CAI`, `Cusanus`, `DUM`, `GIB`, `GUA`, `H-GHZ-001`, `H-YC-001`, `Hippocrates`, `HuoQuBing`, `Kautilya`, `LAN`, `LIN`, `LIQ`, `LIS`, `LUO`, `LiuXiu`, `OHM`, `OUY`, `OdaNobunaga`, `P24F`, `P25F`, `P26F`, `PUS`, `Phase27Final`, `Ptolemy`, `QIU`, `SUS`, `Shotoku`, `TAN`, `TDL`, `TIN`, `TOU`, `TY`, `VOL`, `Vesalius`, `WEN`, `WUC`, `YAN`, `ZAN`, `ZEN`, `ZHU`, `ZKU`, `ZuXuan`
  （其中 `P24F` / `P25F` / `P26F` / `Phase27Final` / `H-P23F-001` 是 D1 隔离人物，共 50 条模式，本就不进公开产物；
  另有 30 条模式 `figure_code` 为空串。）
- **有文件但缺 `birth_year`/`death_year` 的 7 个 figure**（不猜、不补造）：
- `H-DY-001`（`data/figures/H-DY-001.json`，每个 10 条模式）
- `H-DZS-001`（`data/figures/H-DZS-001.json`，每个 10 条模式）
- `H-FEI-001`（`data/figures/H-FEI-001.json`，每个 10 条模式）
- `H-JSX-001`（`data/figures/H-JSX-001.json`，每个 10 条模式）
- `H-MIY-001`（`data/figures/H-MIY-001.json`，每个 10 条模式）
- `H-MKS-001`（`data/figures/H-MKS-001.json`，每个 10 条模式）
- `H-P23F-001`（`data/figures/H-P23F-001.json`，每个 10 条模式）

## 4. 人工抽检：过滤器必须裁决的**全部**边界候选（32 条）

判定标准（先写清）：D5 意义上的「真矛盾」= **该年份是本人自己的行事年份**且落在本人有生之年之外。
他人（学生、后继者、批评者）的年份、卒后事件与余波、所引文献 / 案件 / 版本的出版年、背景年代
（「1960 年代」）、以及非年份的数值（「2000 万英尺·磅」）一律算「非矛盾」。

候选面来源：朴素规则（本人叙述字段里的年份落在生卒年之外，无任何过滤）全库 **622 个 token / 190 条模式**，
其中「年份与人物名同现」因而必须进入最终裁决的只有下表 32 条。

| # | 模式 | figure | 年份 | 生卒年 | 字段 | D5 结论 | 上下文摘句 | 人工判读 |
|---|---|---|---|---|---|---|---|---|
| 1 | M-ARC-002 | H-ARC-001 | 1906 | -287–-212 | definition_zh | out-of-window（抑制） | 1906 年重见天日的《方法》揭示了阿基米德工作 | 文献重现年：阿基米德《方法》抄本 1906 年重见天日 → 非本人行事 |
| 2 | M-ATK-010 | H-ATK-001 | 1960 | 1881–1938 | representative_cases_zh | background-marker（抑制） | 约束解释权的制度容器被军队长期征用——自1960年起军方多次以『守护凯末尔主义』为由干预 | 卒后政治史：1960 年起军方以「守护凯末尔主义」干预 → 非本人行事 |
| 3 | M-BEN-010 | H-BEN-001 | 1838 | 1748–1832 | representative_cases_zh | source-marker（抑制） | 人体系的运转：鲍林最终主编《边沁文集》(1838-1843) 十一卷，密尔早年为其做编辑 | 遗稿出版年：鲍林主编《边沁文集》1838–1843 → 非本人行事 |
| 4 | M-BEN-010 | H-BEN-001 | 1843 | 1748–1832 | representative_cases_zh | source-marker（抑制） | 转：鲍林最终主编《边沁文集》(1838-1843) 十一卷，密尔早年为其做编辑——作者不 | 同上（同一句的另一端年份）→ 非本人行事 |
| 5 | M-CW-007 | H-CW-001 | 1866 | 1780–1831 | representative_cases_zh | out-of-window（抑制） | 把克劳塞维茨'训练+任务式指挥'落地——1866/1870年战役中普军各级指挥官在失去联 | 后人实践：1866/1870 年普军战役 → 非本人行事 |
| 6 | M-ECL-003 | ECL | 1200 | 1043–1099 | representative_cases_zh | out-of-window（抑制） | 死后复利：《熙德之歌》（约 1200 年）把他的三本账合成一部民族史诗——' | 卒后史诗：《熙德之歌》约 1200 年 → 非本人行事 |
| 7 | M-ECL-009 | ECL | 1200 | 1043–1099 | definition_zh | out-of-window（抑制） | 、他的宽恕有仪式记录；《熙德之歌》（约 1200 年，他死后约一个世纪）并非官方委托的宣 | 同上（文中自注「他死后约一个世纪」）→ 非本人行事 |
| 8 | M-HAM-004 | H-HAM-001 | 1819 | 1755–1804 | definition_zh | source-marker（抑制） | 事实，最终是马歇尔在麦卡洛克诉马里兰案（1819）用汉密尔顿的论证原文给默示权力盖了宪法 | 身后判例：麦卡洛克诉马里兰案 1819 → 非本人行事 |
| 9 | M-HAM-004 | H-HAM-001 | 1819 | 1755–1804 | representative_cases_zh | source-marker（抑制） | 麦卡洛克诉马里兰(1819)：马歇尔判词直接沿用汉密尔顿论证，'必 | 同上（另一字段同一事实）→ 非本人行事 |
| 10 | M-HAM-006 | H-HAM-001 | 1812 | 1755–1804 | definition_zh | source-marker（抑制） | 现承诺。信用的复利效应随后覆盖战争开支：1812年战争、内战（蔡斯直接复刻汉密尔顿框架发 | 身后战争：1812 年战争 → 非本人行事 |
| 11 | M-HAR-005 | H-HAR-001 | 1661 | 1578–1657 | representative_cases_zh | name-not-in-context（抑制） | 毛细血管预言（1628-1661）：哈维的『组织孔隙』作为署名期票，被马 | 后人追认期（哈维 1657 卒，文中「1628-1661」为预言被追认的时段）；被 name-not-in-context 抑制 → 非矛盾，但属口径漏报风险（§10.6 第 3 条） |
| 12 | M-HER-010 | HER | 1910 | 1860–1904 | representative_cases_zh | background-marker（抑制） | 其不同时期文本——'谁解释赫茨尔'成为 1910 年代运动的中心议程 | 背景年代：1910 年代运动的中心议程 → 非本人行事 |
| 13 | M-HER-010 | HER | 1949 | 1860–1904 | definition_zh | out-of-window（抑制） | 级剧场事件（维也纳 1904、赫茨尔山 1949）→'完成遗愿'成为各派共用的动员语法— | 卒后事件：1949 年赫茨尔山迁葬 → 非本人行事 |
| 14 | M-HER-010 | HER | 1949 | 1860–1904 | representative_cases_zh | out-of-window（抑制） | 灰带回那个国家'——1904 年遗嘱在 1949 年以国家规格兑现（赫茨尔山迁葬），遗愿 | 同上（另一字段同一事实）→ 非本人行事 |
| 15 | M-HRC-006 | HRC | 1833 | 1738–1822 | representative_cases_zh | source-marker（抑制） | 约翰·赫歇尔南天巡天（1833-1838）：带家族望远镜赴好望角，四年 | 其子之事：约翰·赫歇尔 1833–1838 南天巡天 → 非本人行事 |
| 16 | M-HRC-006 | HRC | 1838 | 1738–1822 | representative_cases_zh | source-marker（抑制） | 约翰·赫歇尔南天巡天（1833-1838）：带家族望远镜赴好望角，四年测绘南天— | 同上 → 非本人行事 |
| 17 | M-HRC-010 | HRC | 1888 | 1738–1822 | representative_cases_zh | out-of-window（抑制） | NGC 星表（1888）对赫歇尔编号的直接继承：家族观测成为今 | 后人星表：NGC 星表（1888）→ 非本人行事 |
| 18 | M-HZX-008 | H-HZX-001 | 1990 | 1610–1695 | representative_cases_zh | out-of-window（抑制） | 清代摊丁入亩后火耗、捐输再起；1990年代秦晖命名'黄宗羲定律'，成为分析中国 | 后人命名：1990 年代秦晖命名「黄宗羲定律」→ 非本人行事 |
| 19 | M-JENNER-004 | Jenner | 1885 | 1749–1823 | representative_cases_zh | out-of-window（抑制） | 巴斯德1885年狂犬病减毒疫苗：把琴纳的'借用自然减毒 | 他人成果：巴斯德 1885 年狂犬病疫苗 → 非本人行事 |
| 20 | M-JENNER-010 | Jenner | 1980 | 1749–1823 | representative_cases_zh | out-of-window（抑制） | 琴纳1801年的预言与1980年WHO宣布天花消灭——182年的目标- | 后人兑现：1980 年 WHO 宣布天花消灭 → 非本人行事 |
| 21 | M-JENNER-010 | Jenner | 1988 | 1749–1823 | representative_cases_zh | out-of-window（抑制） | 根除脊髓灰质炎运动（1988-）：延续琴纳目标函数的现代远征，卡在' | 后人运动：1988 年起根除脊髓灰质炎 → 非本人行事 |
| 22 | M-KD-010 | H-KD-001 | 1945 | 1724–1804 | representative_cases_zh | out-of-window（抑制） | 重述康德第一条款的强形式）→联合国宪章（1945）与《世界人权宣言》（1948，'人是目 | 后世影响：联合国宪章（1945）→ 非本人行事 |
| 23 | M-NEW-002 | H-NEW-001 | 1758 | 1643–1727 | representative_cases_zh | out-of-window（抑制） | 牛顿以计算精确回敬：Halley 彗星 1758 回归是判决书 | 身后预言兑现：Halley 彗星 1758 回归（牛顿卒于 1727）→ 非本人行事 |
| 24 | M-NEW-007 | H-NEW-001 | 1749 | 1643–1727 | representative_cases_zh | CONFLICT（上报） | 动差一半：牛顿未解决，Clairaut 1749 年以摄动级数升阶解决——方法误差而非理 | **上报为 conflict**：Clairaut 1749 年以摄动级数解决（句子自称「牛顿未解决」）→ 他人成果，**误报** |
| 25 | M-QJS-002 | QJS | 1819 | 1208–1268 | representative_cases_zh | out-of-window（抑制） | 文献中的'秦九韶算法'与 Horner（1819）重名：同一嵌套求值思想早于西方 570 | 他人重名：Horner（1819）→ 非本人行事 |
| 26 | M-SAU-009 | SAU | 1996 | 1857–1913 | representative_cases_zh | out-of-window（抑制） | 校勘学的实战检验：1996 年发现的索绪尔手稿（普鲁士图书馆藏笔记 | 遗稿重现：1996 年发现索绪尔手稿 → 非本人行事 |
| 27 | M-SCH-007 | H-SCH-001 | 1957 | 1883–1950 | representative_cases_zh | source-marker（抑制） | 唐斯《民主的经济理论》(1957)：把熊彼特的竞争定义形式化为『政党=追 | 他人著作：唐斯《民主的经济理论》(1957) → 非本人行事 |
| 28 | M-SCH-009 | H-SCH-001 | 1954 | 1883–1950 | definition_zh | source-marker（抑制） | 熊彼特 1954 年《经济分析史》与《资本主义、社会主义 | 遗著出版年：熊彼特 1954 年《经济分析史》→ 非本人行事 |
| 29 | M-TLY-007 | H-TLY-001 | 1990 | 1912–1954 | representative_cases_zh | out-of-window（抑制） | 学框架——他们在教科书中明言图灵是先驱；1990年代遗传算法、2010年代深度强化学习（ | 后人学科：1990 年代遗传算法 → 非本人行事 |
| 30 | M-TLY-007 | H-TLY-001 | 2010 | 1912–1954 | representative_cases_zh | out-of-window（抑制） | 中明言图灵是先驱；1990年代遗传算法、2010年代深度强化学习（AlphaGo）逐条兑 | 后人学科：2010 年代深度强化学习 → 非本人行事 |
| 31 | M-TLY-008 | H-TLY-001 | 1990 | 1912–1954 | representative_cases_zh | out-of-window（抑制） | 物—丙二酸反应）在实验室复现了图灵斑图，1990年代起斑马鱼 stripes、鸟喙皱纹、 | 后人实验：1990 年代斑马鱼斑图 → 非本人行事 |
| 32 | M-WAT-005 | WAT | 2000 | 1736–1819 | representative_cases_zh | out-of-window（抑制） | 成为行业标尺：早期瓦特机 duty 约 2000 万英尺·磅/蒲式耳，后继 Cornis | 数值误读：「duty 约 2000 万英尺·磅/蒲式耳」不是年份 → 非本人行事 |

**判读结论**：真矛盾 **0 条**；被抑制的 31 条全部是卒后余波 / 遗著与文献出版年 / 背景年代 / 他人成果
（抑制精度 31/31）；唯一上报项 `M-NEW-007` 是**误报**（Clairaut 1749 年的成果，句子自称「牛顿未解决」）——
即上报精度 **0/1**。

## 5. 另抽 12 条 `name-not-in-context` + 6 条 `out-of-window`（原始输出）

```text
$ python3 /tmp/z4_sample.py     # 抽检脚本：按 reason 取前 N 条，打印上下文
name-not-in-context 共 163 条，抽 12 条：
  M-HEG-005        H-HEG-001    representative_cases_zh  y=1844  life=[1770, 1831] names=['黑格尔']
      ctx: 的纪律性是异化向教养转化的枢纽。马克思《1844年手稿》的异化劳动四规定（产品异化、劳动
  M-HEG-005        H-HEG-001    representative_cases_en  y=1844  life=[1770, 1831] names=['黑格尔']
      ctx: enated labor in the 1844 Manuscripts inherit
  M-TLY-006        H-TLY-001    representative_cases_zh  y=1980  life=[1912, 1954] names=['图灵']
      ctx: 评级均按表现划界，意识问题留待哲学；塞尔1980年'中文房间'正是对该悬置策略的正面进攻
  M-TLY-006        H-TLY-001    representative_cases_en  y=1980  life=[1912, 1954] names=['图灵']
      ctx: estion—and Searle's 1980 Chinese Room was a 
  M-TLY-007        H-TLY-001    representative_cases_zh  y=1980  life=[1912, 1954] names=['图灵']
      ctx: 。这条路线在其后四十年几乎无人跟进，直到1980年代萨顿与巴托建立强化学习的数学框架——
  M-TLY-008        H-TLY-001    representative_cases_zh  y=1980  life=[1912, 1954] names=['图灵']
      ctx: 检验形态发生素是否存在，理论沉睡三十年；1980年代化学实验（CSTR 中的氯离子—碘化
  M-TLY-008        H-TLY-001    representative_cases_en  y=1980  life=[1912, 1954] names=['图灵']
      ctx: d chemically in the 1980s and biologically s
  M-ONO-001        H-ONO-001    representative_cases_zh  y=2000  life=[1912, 1990] names=['大野耐一']
      ctx: 1950年危机后丰田'削减2000人、日产缩至820台'倒逼出小批量柔性生
  M-LSZ-010        H-LSZ-001    representative_cases_zh  y=1596  life=[1518, 1593] names=['李时珍']
      ctx: 金陵本与江西本的版本接力：1596年金陵本刊行、1603年江西本翻刻——初
  M-LSZ-010        H-LSZ-001    representative_cases_zh  y=1603  life=[1518, 1593] names=['李时珍']
      ctx: 江西本的版本接力：1596年金陵本刊行、1603年江西本翻刻——初刻与翻刻的版本链使书躲
  M-LSZ-010        H-LSZ-001    representative_cases_en  y=1596  life=[1518, 1593] names=['李时珍']
      ctx:  edition printed in 1596, the Jiangxi reprin
  M-LSZ-010        H-LSZ-001    representative_cases_en  y=1603  life=[1518, 1593] names=['李时珍']
      ctx:  Jiangxi reprint in 1603—first printing and 
--- out-of-window 抽 6 条 ---
  M-IBR-008        H-IBR-001    representative_cases_zh  y=1270  life=[1126, 1198]
      ctx: 智统一论》逐条反驳（主张理智随个体多），1270/1277年大谴责把相关命题列入禁条——
  M-KD-010         H-KD-001     representative_cases_zh  y=1920  life=[1724, 1804]
      ctx: 设计。该方案的兑现链清晰可辨：国际联盟（1920）与《非战公约》（1928，'废弃以战争
  M-TLY-007        H-TLY-001    representative_cases_zh  y=1990  life=[1912, 1954]
      ctx: 学框架——他们在教科书中明言图灵是先驱；1990年代遗传算法、2010年代深度强化学习（
  M-TLY-008        H-TLY-001    representative_cases_zh  y=1990  life=[1912, 1954]
      ctx: 物—丙二酸反应）在实验室复现了图灵斑图，1990年代起斑马鱼 stripes、鸟喙皱纹、
  M-XN-005         H-XN-001     representative_cases_zh  y=1854  life=[1916, 2001]
      ctx: 构与布尔的逻辑代数完全同构——这是布尔在1854年提出、几乎无人问津的体系。他不仅建立对
  M-SQ-008         H-SQ-001     representative_cases_zh  y=1973  life=[-145, -86]
      ctx: 帛书平反（1973年马王堆出土）：《战国纵横家书》十六篇书

```

逐条判读：均**非本人矛盾**（他人著作与成果、遗著刊行、后人事件、背景年代、数值误读）。
注意 `M-HAR-005` 那条是**口径的漏报风险**：模式名写「威廉·哈维」，而上下文只出现「哈维」，
±20 字窗口内名字不严格相等 → 被 `name-not-in-context` 抑制（已如实写进 §10.6 的盲区清单）。

## 6. 负对照自测（34 项全绿）

```text
$ python3 tools/test_credibility_d45.py
[PASS] G 生卒年解析（int/字符串/约前/负号）
[PASS] G2 夹具人物生卒年装载
[PASS] A D5 矛盾样本必被检出
[PASS] A2 check_d5_timeline_conflict 返回警告文案
[PASS] B D5 干净样本必须 clean（不误报）
[PASS] C 误报控制①：年份不与人物名同现 -> 不判矛盾
[PASS] D 误报控制②：余波标记 -> 不判矛盾
[PASS] E 误报控制③：离生卒年过远 -> 不判矛盾
[PASS] F 无生卒年 -> undetermined 且理由明确
[PASS] M0 field_text 统一取文本口径（str/list/嵌套/None/缺字段/bool/数字）
[PASS] M1 D5 list 载荷里的矛盾年份必被检出（修字段类型盲区）
[PASS] M2 负对照：同一年份放在 str 载荷也必须被检出（两种载荷等价）
[PASS] M3 两种载荷的证据一致（year=1699 / field 相同）
[PASS] M4 process_zh 为 list 且含 None -> 仍被扫描且不崩
[PASS] M5 五字段全 None -> undetermined/no-four-digit-year，不静默放过
[PASS] M6 模式缺 figure_name -> 回退 data/figures 的名字后仍能检出
[PASS] H D4 不符样本必被检出（mismatch）
[PASS] I D4 干净样本必须 matched（不误报）
[PASS] Q D4 key_quote_zh 为 list -> 仍可核且 matched（旧写法 unchecked no-quote）
[PASS] Q2 D4 source_chapter/key_quote_zh 均为 list -> 仍判 mismatch
[PASS] J 误报控制：coverage=partial -> 不可核（不得判 mismatch）
[PASS] K 无缓存条目 -> unchecked 且理由明确
[PASS] L 端到端：坏样本必须在 gate 报告里报出 D4 + D5
[PASS] L2 端到端：干净样本不得报 D4/D5
[PASS] T 端到端：list 载荷的年份必须在 gate 报告里报 D5（引文 matched，不得误报 D4）
[PASS] Z0 生卒年解析扩到公元前写法（约公元前330 / 公元前275 / 空串）
[PASS] Z1 英文镜像字段 representative_cases_en 里的矛盾年份必被检出
[PASS] Z4 年份只在英文镜像字段时 token 仍计入（不再静默 tokens=0）
[PASS] Z2 负对照：英文卒后余波标记 -> 不得判矛盾（afterlife-marker）
[PASS] Z3 负对照：英文文献 / 出版标记 -> 不得判矛盾（source-marker）
[PASS] Z5 取值键：人名键与代码键都登记，时代名键不登记
[PASS] Z6 「约公元前330」式纪年进 lifespan（不再被判无生卒年）
[PASS] Z5b 同键不同生卒年 -> 整体丢弃并在诊断里如实报告
[PASS] Z7 backfill_lifespans.py --check 对当前数据 exit 0（补数清单可重入不漂移）

34/34 passed

```

本卡验收指定的负对照 = `Z1`：把年份放进 `representative_cases_en` 且满足其它强信号 → **必被检出**
（实测 `status=conflict`，`field=representative_cases_en`）；配套 `Z4` 证明「年份只在英文镜像字段时
token 仍计入，不是静默 0」；`Z2`/`Z3` 证明英文句里的 `after his death` / `published` 不会变成假阳性。

## 7. 下游接线与一致性

```text
$ python3 tools/build_audit_findings.py --write
findings entries: 156        # 与修复前一致（D5 conflict 仍 1 条）
$ git diff data/audit/findings.json | grep -E '^[+-]'  # 只有 audit_meta 的 D5 计数
      "figures_with_lifespan": 265 -> 616
      "undetermined": 2292 -> 1546
$ python3 tools/verify_findings.py --hard-fail --data-path data/modes_data.json   # exit 0
$ python3 tools/apply_verification_status.py --check                              # 无漂移（suspect 23 不变）
```

- 构建顺序按卡要求跑过：`build_figures_db → export_static_site → build_unified_index → apply_site_counts`
  （2798 条模式 × 278 位人物，未变）。`api/protreptic.db` 是 CI 现场重建件（§9.3 排除项），改动已还原，
  不入本次提交。
- `docs/architecture/static_data_manifest.json` 被 `export_static_site.py` 刷新：它此前是**过期**的
  （记的 `data/modes_data.json` sha256 是 Phase41-Z3 之前的），本次一并对齐。

## 8. 复现命令（一条不漏）

```text
python3 tools/backfill_lifespans.py --check
python3 tools/credibility_gate.py --legacy-report
python3 tools/credibility_gate.py --hard-fail --data-path data/modes_data.json
python3 tools/test_credibility_d45.py
python3 tools/verify_findings.py --hard-fail --data-path data/modes_data.json
python3 tools/apply_verification_status.py --check
python3 tools/check_repo_parity.py
```

## 9. 双仓同步与 CI

（见下方「运行记录」一节的真实命令输出）
