# Phase41-Z3 验收报告：D4/D5 字段类型盲区修复（list 载荷曾被整段跳过）

日期：2026-09-21 ｜ 执行：san-martin ｜ 项目仓：`/opt/data/workspace/Protreptic`（master）
发布仓：`/opt/data/release/Protreptic-publish`（origin main）

## 0. 起因（船长独立核验，可复现）

Phase40-Z2 把 D5 从 `return []` 空壳改成了真代码，方向对，但**在真实数据上形同虚设**：

```
$ sed -n '333,338p' tools/credibility_gate.py     # Phase41-Z3 修复前的 HEAD f9a60b48
    for field in D5_CLAIM_FIELDS + ("source_chapter", "key_quote_zh"):
        text = mode.get(field)
        if not isinstance(text, str):
            continue          # <- 非字符串字段被整段跳过
```

而真实数据的字段类型（`tools/credibility_gate.py::D45_TEXT_FIELDS` 全库 2888 条模式实测，
命令见第 8 节 `field_types.py`）：

| 字段 | str | list | None | 说明 |
|---|---|---|---|---|
| `definition_zh` | 2888 | 0 | 0 | 唯一稳定是字符串 |
| `process_zh` | 20 | **2808** | 60 | 年份集中字段，被整段跳过 |
| `representative_cases_zh` | 102 | **2546** | 240 | 年份集中字段，被整段跳过 |
| `source_chapter` | 2808 | 30 | 50 | list 条目此前取文本口径不一致 |
| `key_quote_zh` | 2816 | 17 | 55 | list 条目此前直接判 `no-quote` |

修复前全库实测（同第 8 节 `compare.py` 的 BEFORE 段）：

```
status: undetermined 2376 / clean 512   (conflict = 0)
tokens=0 的模式: 2376 / 2888 = 82.3%
```

## 1. 交付

| 文件 | 变更 |
|---|---|
| `tools/credibility_gate.py` | **改**：新增 `D45_TEXT_FIELDS` / `_text_atoms()` / `_text_of()` / `field_text_atoms()` / `field_text()` / `iter_field_text()`；D5 改为按**原子文本**扫描；D4 的引文与出处统一走 `field_text()`；D3 豁免登记的 `has_source` 统一；`load_figure_lifespans()` 带上 `figure_name` 供名字回退 |
| `tools/test_credibility_d45.py` | **改**：15 项扩到 **25 项**，新增 list/str/None 三态一致（M0–M6）、D4 list 载荷（Q/Q2）、端到端 list 载荷（T） |
| `data/audit/findings.json` | **改**：156 条（D5_timeline_conflict 从 0 增到 1；D4_quote_mismatch 22 不变） |
| `data/audit/verification_status.json` | **改**：四态口径更新（全库 suspect 39 -> 40） |
| `data/modes_data.json` | **改**：`verification.status` 按既有规则推进（verified -> suspect 1 条：`M-NEW-007`） |
| `docs/planning/credibility_framework.md` | **改**：第 1 节 D4/D5 行补第 41 期口径；第 10 节改为「修复后的真实覆盖 + 残留盲区」 |
| `docs/qa/phase41_z3_d4_d5_field_types.md` | **新增**：本报告 |

## 2. 修复内容

### 2.1 统一取文本口径（D4/D5 共用，规则唯一实现）

```python
D45_TEXT_FIELDS = ("definition_zh", "process_zh", "representative_cases_zh",
                   "source_chapter", "key_quote_zh")

_text_atoms(value)        # str -> [str]；list/tuple/set -> 逐层展开成各元素；None/bool -> []；标量 -> [str(v)]
field_text_atoms(mode, f) # 原子文本列表
field_text(mode, f)       # 原子之间按行 join -> 单块文本（D4 的引文/出处、报告与统计用）
iter_field_text(mode, fs) # [(field, atom)]，逐个原子文本（D5 的扫描口径）
```

**不再有任何 `isinstance(text, str) -> continue` 式整段跳过**；list / str / None 三种载荷
在 D5 上判定等价（负对照 M1/M2/M3 + 端到端 T 钉住）。

### 2.2 为什么按「原子」扫而不是把 list join 成一个大字符串

自测 M1 当场抓到反例：夹具 `["背景铺陈一句", "1699年测试人物主持重修书院"]` 若 join 成
`"背景铺陈一句\n1699年测试人物主持重修书院"` 再扫，1699 的 ±20 字上下文窗口会跨到前一条元素，
命中 `D5_EXCLUDE_BACKGROUND` 里的「背景」-> **真矛盾被降级成 `background-marker` 不可判定**；
反过来后一条元素里的人名也会替前一条元素里的年份「背书」。按原子文本扫描后窗口不越元素边界。

### 2.3 名字回退

模式缺 `figure_name`（实测 30 条）时，此前名字为空 -> 窗口内年份一律 `name-not-in-context`。
现在回退到 `data/figures/*.json` 的 `figure_name`（`load_figure_lifespans()` 携带）。
当前全库这 30 条的模式侧与 figure 侧**都没有**可用姓名（0 例受益），属防御性修复，如实记录。

## 3. 修复前后对照（关键指标）

命令：`python3 /opt/data/profiles/san-martin/cache/scratch/z3/compare.py`
（同一个 `data/modes_data.json`，BEFORE 用 `git show HEAD:tools/credibility_gate.py` 的旧模块）

| 指标 | 修复前（f9a60b48） | 修复后（Phase41-Z3） | 变化 |
|---|---|---|---|
| 扫到的 4 位年份 token 总数 | 1252 | **2110** | +858（+68.5%） |
| `tokens=0` 模式数 | 2376 / 2888 = **82.3%** | 2292 / 2888 = **79.4%** | -84 条 |
| status `clean` | 512 | **595** | +83 |
| status `undetermined` | 2376 | 2292 | -84 |
| status `conflict` | 0 | **1** | +1 |
| 其中「人物有生卒年」子集 `tokens=0` | 620 / 1132 = 54.8% | **536 / 1132 = 47.3%** | -84 |
| 其中「人物无生卒年」子集 `tokens=0` | 1756 / 1756 | 1756 / 1756 | 不变 |

**诚实结论：`tokens=0` 只从 82.3% 降到 79.4%，没有「大幅下降」——任务书预期的降幅没有出现，
原因不是修得不对，而是 82% 这个数字的主体本来就不是字段类型盲区**：

* 1762 条（全库 61.0%）的 figure **没有可用生卒年**（`no-lifespan-for-figure`），
  D5 按设计一律 `undetermined`（另有 6 条隔离/占位 figure 同理）——这**另一条盲区**与 list 载荷无关；
* 修复真正影响的是「有生卒年」子集里的 84 条（620 -> 536）；
* 余下 536 条确实有生卒年、且五个扫描字段里**真的一个 4 位年份都没有**（第 7 节给出交叉核验）。

## 4. 新检出的 conflict：1 条，人工复核为**误报**

全库新检出 **1 条** conflict（`data/audit/findings.json` defect=`D5_timeline_conflict`）：

```
M-NEW-007 [H-NEW-001] 牛顿 生卒=1643-1727  生涯带=[1603, 1757]
  field=representative_cases_zh  （list 载荷，修复前整段跳过）
  year=1749
  context=动差一半：牛顿未解决，Clairaut 1749 年以摄动级数升阶解决——方法误差而非理
            论误差...
  判读=误报：1749 年是**他人（Clairaut）在牛顿卒后**完成的成果，句子本身明确写「牛顿未解决」。
        D5 现行规则只检查「年份与本人名同现」，无法区分「同年出现的他人姓名」，
        故该条属**规则已知盲区导致的误报**，不是数据错误。
```

线上口径更新（`tools/apply_verification_status.py --write`）：`verified -> suspect` **1 条**，即 `M-NEW-007`
（全库 suspect 39 -> 40，公开口径 suspect 22 -> 23）。该条在公开页面上显示为「存疑待复核」，
属既有语义（`suspect` = 命中 D1–D5 之一、待复核），**未做静默压制**。

**误报率如实写**：本次新检出的 conflict 只有 1 条，人工复核判定为误报 ——
即**上报集合的精度 0/1（1 条全部误报）**。其余候选见下节。

## 5. 误报复核：窗口内候选 45 条逐条人工判读

除上表 1 条 conflict 外，全库还有 **45 条**「年份落在生涯带内、字段属本人叙述字段」的候选
被 `name-not-in-context`（44 条）/ `source-marker`（1 条）降级。逐条判读结果：**45/45 确非矛盾**。

| 降级理由 | 条数 | 人工判读为「确非矛盾」 |
|---|---|---|
| `name-not-in-context` | 44 | 44 |
| `source-marker` | 1 | 1 |
| 合计 | 45 | **45/45 确非矛盾** |

### 5.1 45 条候选逐条判读表

（判定降级理由 = `d5_scan` 给出的 reason；人工判读 = 本次逐条读上下文后的结论）

| # | mode_code | 人物 | 生卒 | 字段 | 年份 | 判定降级理由 | 人工判读 |
|---|---|---|---|---|---|---|---|
| 1 | `M-AE-007` | 麦哲伦 | 1480-1521 | `definition_zh` | 1522 | `name-not-in-context` | 确非矛盾：卒后返航/航行完成（1521 卒） |
| 2 | `M-AE-007` | 麦哲伦 | 1480-1521 | `representative_cases_zh` | 1522 | `name-not-in-context` | 确非矛盾：卒后返航完成 |
| 3 | `M-AE-008` | 麦哲伦 | 1480-1521 | `representative_cases_zh` | 1522 | `name-not-in-context` | 确非矛盾：1519-1522 航程整体叙述 |
| 4 | `M-AE-008` | 麦哲伦 | 1480-1521 | `definition_zh` | 1529 | `name-not-in-context` | 确非矛盾：卒后条约（萨拉戈萨 1529） |
| 5 | `M-AE-008` | 麦哲伦 | 1480-1521 | `definition_zh` | 1529 | `name-not-in-context` | 确非矛盾：卒后条约 |
| 6 | `M-AE-008` | 麦哲伦 | 1480-1521 | `representative_cases_zh` | 1529 | `name-not-in-context` | 确非矛盾：卒后条约 |
| 7 | `M-AE-009` | 麦哲伦 | 1480-1521 | `definition_zh` | 1529 | `name-not-in-context` | 确非矛盾：卒后条约定价 |
| 8 | `M-AE-009` | 麦哲伦 | 1480-1521 | `representative_cases_zh` | 1529 | `name-not-in-context` | 确非矛盾：卒后条约定价 |
| 9 | `M-AE-010` | 麦哲伦 | 1480-1521 | `representative_cases_zh` | 1522 | `name-not-in-context` | 确非矛盾：卒后返航（维多利亚号 18 人） |
| 10 | `M-AQU-001` | 阿奎那 | 1225-1274 | `representative_cases_zh` | 1277 | `name-not-in-context` | 确非矛盾：卒后 1277 谴责（1274 卒） |
| 11 | `M-CUR-008` | 居里夫人 | 1867-1934 | `representative_cases_zh` | 1962 | `name-not-in-context` | 确非矛盾：身后制度（法国科学院 1962） |
| 12 | `M-CUR-010` | 居里夫人 | 1867-1934 | `definition_zh` | 1935 | `name-not-in-context` | 确非矛盾：他人事件（其女 1935 获诺奖） |
| 13 | `M-CUR-010` | 居里夫人 | 1867-1934 | `representative_cases_zh` | 1935 | `name-not-in-context` | 确非矛盾：他人事件（伊蕾娜 1935） |
| 14 | `M-CYP-009` | 蔡元培 | 1868-1940 | `representative_cases_zh` | 1948 | `name-not-in-context` | 确非矛盾：身后制度兑现（1948 首届院士） |
| 15 | `M-DAR-006` | 达尔文 | 1809-1882 | `representative_cases_zh` | 1903 | `name-not-in-context` | 确非矛盾：后人验证（1903 巨型天蛾） |
| 16 | `M-DAR-009` | 达尔文 | 1809-1882 | `representative_cases_zh` | 1903 | `name-not-in-context` | 确非矛盾：后人验证（1903 Xanthopan） |
| 17 | `M-EIN-006` | 爱因斯坦 | 1879-1955 | `representative_cases_zh` | 1982 | `name-not-in-context` | 确非矛盾：后人实验（1982 阿斯佩） |
| 18 | `M-EIN-009` | 爱因斯坦 | 1879-1955 | `definition_zh` | 1964 | `name-not-in-context` | 确非矛盾：他人（贝尔 1964） |
| 19 | `M-EIN-009` | 爱因斯坦 | 1879-1955 | `representative_cases_zh` | 1964 | `name-not-in-context` | 确非矛盾：他人（贝尔 1964） |
| 20 | `M-EIN-009` | 爱因斯坦 | 1879-1955 | `definition_zh` | 1982 | `name-not-in-context` | 确非矛盾：后人实验（1982） |
| 21 | `M-EIN-009` | 爱因斯坦 | 1879-1955 | `representative_cases_zh` | 1982 | `name-not-in-context` | 确非矛盾：后人实验（1982） |
| 22 | `M-HAR-003` | 哈维 | 1578-1657 | `representative_cases_zh` | 1661 | `name-not-in-context` | 确非矛盾：他人卒后发现（1661 马尔皮基） |
| 23 | `M-HAR-005` | 哈维 | 1578-1657 | `definition_zh` | 1661 | `name-not-in-context` | 确非矛盾：后人验证（1661 毛细血管） |
| 24 | `M-HAR-005` | 哈维 | 1578-1657 | `representative_cases_zh` | 1661 | `source-marker` | 确非矛盾：后人验证（1661） |
| 25 | `M-HAR-005` | 哈维 | 1578-1657 | `representative_cases_zh` | 1661 | `name-not-in-context` | 确非矛盾：后人验证（1661） |
| 26 | `M-HEG-005` | 黑格尔 | 1770-1831 | `representative_cases_zh` | 1844 | `name-not-in-context` | 确非矛盾：他人文献（马克思 1844 手稿） |
| 27 | `M-KEY-005` | 约翰·梅纳德·凯恩斯 | 1883-1946 | `representative_cases_zh` | 1970 | `name-not-in-context` | 确非矛盾：后世史实（1970 年代） |
| 28 | `M-KEY-006` | 约翰·梅纳德·凯恩斯 | 1883-1946 | `representative_cases_zh` | 1971 | `name-not-in-context` | 确非矛盾：后世事件（1971 尼克松冲击） |
| 29 | `M-KEY-006` | 约翰·梅纳德·凯恩斯 | 1883-1946 | `representative_cases_zh` | 1972 | `name-not-in-context` | 确非矛盾：他人提案（托宾税 1972） |
| 30 | `M-KEY-009` | 约翰·梅纳德·凯恩斯 | 1883-1946 | `representative_cases_zh` | 1970 | `name-not-in-context` | 确非矛盾：后世史实（1970 年代） |
| 31 | `M-KEY-009` | 约翰·梅纳德·凯恩斯 | 1883-1946 | `representative_cases_zh` | 1976 | `name-not-in-context` | 确非矛盾：后世事件（1976 IMF 危机） |
| 32 | `M-LH-001` | 利德尔·哈特 | 1895-1970 | `representative_cases_zh` | 1864 | `name-not-in-context` | 确非矛盾：他人战例（1864 谢尔曼战役，且早于生年 31 年） |
| 33 | `M-LSZ-010` | 李时珍 | 1518-1593 | `representative_cases_zh` | 1596 | `name-not-in-context` | 确非矛盾：身后刊刻（1596 金陵本） |
| 34 | `M-LSZ-010` | 李时珍 | 1518-1593 | `representative_cases_zh` | 1603 | `name-not-in-context` | 确非矛盾：身后翻刻（1603 江西本） |
| 35 | `M-MENDEL-010` | 施耐庚 | 1822-1884 | `representative_cases_zh` | 1900 | `name-not-in-context` | 确非矛盾：身后再发现（1900 三人独立 rediscovery） |
| 36 | `M-NEW-008` | 牛顿 | 1643-1727 | `representative_cases_zh` | 1607 | `name-not-in-context` | 确非矛盾：他人观测数据（1607/1531/1682 彗星） |
| 37 | `M-NEW-008` | 牛顿 | 1643-1727 | `representative_cases_zh` | 1742 | `name-not-in-context` | 确非矛盾：他人卒年（Halley 卒于 1742） |
| 38 | `M-ONO-001` | 大野耐一 | 1912-1990 | `representative_cases_zh` | 2000 | `name-not-in-context` | 确非矛盾：非年份数字（削减 2000 人） |
| 39 | `M-SYS-002` | 孙中山 | 1866-1925 | `representative_cases_zh` | 1928 | `name-not-in-context` | 确非矛盾：身后史实（1928 训政） |
| 40 | `M-SYS-007` | 孙中山 | 1866-1925 | `representative_cases_zh` | 1930 | `name-not-in-context` | 确非矛盾：身后制度（1930 宣誓条例） |
| 41 | `M-SYS-009` | 孙中山 | 1866-1925 | `definition_zh` | 1928 | `name-not-in-context` | 确非矛盾：身后史实（1928 训政纲领） |
| 42 | `M-SYS-009` | 孙中山 | 1866-1925 | `representative_cases_zh` | 1928 | `name-not-in-context` | 确非矛盾：身后史实（1928） |
| 43 | `M-TLY-006` | 图灵 | 1912-1954 | `representative_cases_zh` | 1980 | `name-not-in-context` | 确非矛盾：他人（塞尔 1980 中文房间） |
| 44 | `M-TLY-007` | 图灵 | 1912-1954 | `representative_cases_zh` | 1980 | `name-not-in-context` | 确非矛盾：后人框架（1980 年代强化学习） |
| 45 | `M-TLY-008` | 图灵 | 1912-1954 | `representative_cases_zh` | 1980 | `name-not-in-context` | 确非矛盾：后人实验（1980 年代 CSTR） |

### 5.2 上下文附录（原文截断 150 字，供复核）

| # | 上下文（原文截断 150 字） |
|---|---|
| 1 | 目标。这是'使命大于创始人'的极限案例：1522年9月6日维多利亚号返抵塞维利亚，18名 |
| 2 | 月弃特立尼达号留守蒂多雷（两船并一船），1522年5月绕行好望角时仅存维多利亚号——'减 |
| 3 | 地球成球说的实证终局：1519-1522年维多利亚号自东向西环球一周，'大地是否 |
| 4 | 、香料群岛方位（间接引发《萨拉戈萨条约》1529），行动的信息密度远高于论辩；其三，以实 |
| 5 | 结论的条约化——航行事实随后被写进条约（1529年萨拉戈萨线），把行动裁决转化为制度裁决 |
| 6 | 以西'从双边口水战变成坐标问题，直接催生1529年《萨拉戈萨条约》（西班牙以35万杜卡特 |
| 7 | 即谈判筹码；其四，接受缝隙的定价终局——1529年西班牙以35万杜卡特效仿'出售'群岛权 |
| 8 | 中无法再纯以法理论群岛——先占事实改变了1529年条约的价格（35万杜卡特） |
| 9 | 加费塔逐名记录幸存者（维多利亚号18人于1522年9月6日返抵塞维利亚，次日凌晨赤足持烛 |
| 10 | 反例警示：1277年巴黎宗教当局谴责二百余条命题，其中多条 |
| 11 | 验在她生前未被充分制度化（法国科学院直至1962年才首次接纳女性），后来者无法直接继承其 |
| 12 | 的学生曾来此受训，其中包括其女儿伊蕾娜（1935年再获诺奖）；其三，以标准品与术语占住学 |
| 13 | 出包括伊蕾娜·约里奥-居里在内的下一代，1935年人工放射性诺奖是建制化产出的直接兑现 |
| 14 | 谋研究之自由与学术之独立'，虽因时局迟至1948年才选出首届院士，但制度设计在他任内已定 |
| 15 | 一英尺的蜜距，必存在相应长喙的传粉者——1903 年发现的巨型天蛾为该预言背书（他本人据 |
| 16 | 年 Hermann Müller 报告、1903 年发现巨型天蛾 Xanthopan m |
| 17 | ，逼出『纠缠』概念；薛定谔同年命名之——1982年阿斯佩实验与2022年诺贝尔奖是论战遗 |
| 18 | 不同的问题被搅成一团，双方各攻一个。贝尔1964年把 EPR 的概念区分写成不等式，19 |
| 19 | 贝尔1964：把 EPR 概念区分写成可实验的不等式 |
| 20 | 64年把 EPR 的概念区分写成不等式，1982年实验裁决：局部实在论出局，但『实在性』 |
| 21 | 1982阿斯佩实验与2022诺奖：局部性出局，而 |
| 22 | 结构证词读错一处，整体地图就留一个污点；1661年马尔皮基发现毛细血管后才补上，说明互证 |
| 23 | 留给后来的探索者的礼物（后人的确领走了：1661年马尔皮基用显微镜在蛙肺中看到毛细血管， |
| 24 | 毛细血管预言（1628-1661）：哈维的『组织孔隙』作为署名期票，被马 |
| 25 | 有小通道』而不虚构其形态——克制使预言在1661年恰好对上毛细血管，不因过度具体而作废 |
| 26 | 的纪律性是异化向教养转化的枢纽。马克思《1844年手稿》的异化劳动四规定（产品异化、劳动 |
| 27 | 流断裂）先于长期愿景杀死公司（反面警示：1970年代以'菲利普斯曲线长期权衡'为名长期维 |
| 28 | 27年，为战后重建提供货币秩序；其解体（1971尼克松冲击）恰始于凯恩斯警告的投机资本流 |
| 29 | 托宾税提议（1972）：对短期外汇交易征税增加投机摩擦——凯 |
| 30 | 科书式相机干预与退出条款前置（反面警示：1970年代各国把'相机干预'固化为准自动的赤字 |
| 31 | 贝弗里奇社会保险=西欧混合经济标准配置；1976年IMF危机后撒切尔-里根回摆恰验证'退 |
| 32 | 1864年谢尔曼亚特兰大战役：不以正面强攻约瑟夫 |
| 33 | 金陵本与江西本的版本接力：1596年金陵本刊行、1603年江西本翻刻——初 |
| 34 | 江西本的版本接力：1596年金陵本刊行、1603年江西本翻刻——初刻与翻刻的版本链使书躲 |
| 35 | 1900年三位科学家独立 rediscovery |
| 36 | y 周期预测：以平方反比计算 1531/1607/1682 三次彗星同轨，预测 1758 |
| 37 | 16 年后预测兑现（Halley 卒于 1742） |
| 38 | 1950年危机后丰田'削减2000人、日产缩至820台'倒逼出小批量柔性生 |
| 39 | 1928年后国民党以《训政纲领》进入训政，却无限 |
| 40 | 首开元首对民宣誓先河，后经《宣誓条例》（1930）制度化 |
| 41 | 不继承『还政』，托管就退化为永久占领——1928 年后的史实证明了这一点。方法上这意味着 |
| 42 | 反例警示：1928《训政纲领》接管政权后，训政无限延长、宪 |
| 43 | 评级均按表现划界，意识问题留待哲学；塞尔1980年'中文房间'正是对该悬置策略的正面进攻 |
| 44 | 。这条路线在其后四十年几乎无人跟进，直到1980年代萨顿与巴托建立强化学习的数学框架—— |
| 45 | 检验形态发生素是否存在，理论沉睡三十年；1980年代化学实验（CSTR 中的氯离子—碘化 |

## 6. 负对照：list 载荷与 str 载荷判定等价

```
$ python3 tools/test_credibility_d45.py
... 25/25 passed
```

关键项（新增 10 项，扩自 Phase40-Z2 的 15 项）：

| 项 | 断言 | 结果 |
|---|---|---|
| M0 | `field_text` 三态口径：str / list / 嵌套 list / None / 缺字段 / bool / 数字 标量 | PASS |
| M1 | 年份在 **list** 载荷里（晚于卒年 + 窗口内 + 与人物名同现）-> 必须判 conflict | PASS |
| M2 | **负对照**：同一年份放在 **str** 载荷 -> 同样被判 conflict（两种载荷等价） | PASS |
| M3 | 两种载荷的 conflict 证据一致（year=1699 / field 相同） | PASS |
| M4 | `process_zh` 是 list 且含 None 元素 -> 仍被扫描且不崩 | PASS |
| M5 | 五个字段全 None -> `undetermined` / `no-four-digit-year`，不静默放过 | PASS |
| M6 | 模式缺 `figure_name` -> 回退 `data/figures` 的名字后仍能检出 | PASS |
| Q | D4 `key_quote_zh` 为 list -> 仍可核（matched），旧写法直接 `unchecked no-quote` | PASS |
| Q2 | D4 `source_chapter` + `key_quote_zh` 均为 list -> 仍判 mismatch | PASS |
| T | 端到端：list 载荷的坏样本必须在 gate 报告的 D5 明细里报出（且引文 matched 不得误报 D4） | PASS |

`M4` 夹具刻意避开含「自」字的措辞：`D5_EXCLUDE_BACKGROUND` 里有单字 `自`（亲自 / 自己 / 自…），
会把窗口内的真矛盾降级成 `background-marker` —— 见第 7 节残留盲区。

## 7. 残留盲区（如实写，不夸大覆盖）

1. **人物无生卒年 = D5 的最大盲区（1762 / 2888 = 61.0%）**：`no-lifespan-for-figure` 的模式
   一律不可判定。要收口必须补 `data/figures/*.json` 的生卒年（当前 291 个 figure 文件里
   仅 265 个可解析出成对生卒年）。
2. **有生卒年但五个扫描字段无 4 位年份的 536 条**：交叉核验（第 8 节 `fields_year.py`）显示，
   这 536 条里含 4 位年份的**其它字段**只有：`verification`（2888 条全有，是核验时间戳 2026 年，
   非叙述年份）/ `era`（99 条，是 figure 的生卒泳道串）/ `representative_figures`（6 条）/
   `representative_cases_en`（4 条）/ `definition_en`（1 条）/ `key_quote_context*`（5 条）。
   **未扫描的中文叙述字段是 `modern_applications_zh`（9 条含年份）、`application_zh`（2 条）**——
   本期**没有**把它们并入 `D5_CLAIM_FIELDS`（口径变更需单独的误报评估），如实记为残留盲区。
3. **他人姓名的年份归属无法区分**：第 4 节的 `M-NEW-007` 就是这一类误报
   （「牛顿未解决，Clairaut 1749 年解决」）。可行的下一步是「年份与谁的名字更近就归谁」的
   邻近归属法，本期**未实现**（需先做误报评估）。
4. **单字排除标记过宽**：`D5_EXCLUDE_BACKGROUND` 含 `自`、`起`、`前后`；`D5_EXCLUDE_AFTER`
   含 `之后`/`以后`/`遗`。当前全库没有命中（第 3 节 `background-marker` = 0 条），属**潜在**
   假阴性来源（同现过滤在它之前已挡掉绝大多数），自测 M4 记录了这个边界。
5. **名单 / 阈值是启发式**：生涯带 `[生年-40, 卒年+30]`、名字窗口 ±20 字、`D5_EXCLUDE_*` 都是
   写死的启发式，会漏真矛盾也会放过真矛盾 —— D5 的产出是**候选复核清单，不是终审判决**。
6. **D4 的可核面仍只有 38 个 key**（见第 9 节数据），list 载荷修复只把 17 条 list 型
   `key_quote_zh` 从 `no-quote` 移到了**其它同样不可核**的桶（`no-fulltext-link` +6、
   `no-citation` +11），`matched` 1 / `mismatch` 22 不变 —— **没有假装核过**。

## 8. 线上口径更新（保持自洽）

```
$ python3 tools/credibility_gate.py --legacy-report     # exit 0（WARN 不阻断）
  D4: matched 1 / mismatch 22 / quote-too-short 69 / unchecked 2796
  D5: 生卒年可用人物 265 / 可判定模式 1132 / 年份 token 2110
      conflict 1 / clean 595 / undetermined 2292
      不可判定逐类: out-of-window 206 / name-not-in-context 44 / field-not-claim 24 / source-marker 1

$ python3 tools/build_audit_findings.py --write
  findings entries: 156   (D4_quote_mismatch 22 / D5_timeline_conflict 1)

$ python3 tools/apply_verification_status.py --write
  四态（全库 2868 条）: verified 888 / pending 1589 / suspect 40 / unverifiable 351
  四态（公开口径 2808 条）: verified 888 / pending 1557 / suspect 23 / unverifiable 340
  与库中现状态相比的变更: verified -> suspect = 1 条（M-NEW-007）

$ python3 tools/apply_verification_status.py --check     # exit 0（无漂移）
$ python3 tools/verify_findings.py --hard-fail --data-path data/modes_data.json   # exit 0（无新增硬失败）
$ python3 tools/credibility_gate.py --hard-fail --data-path data/modes_data.json  # exit 0
```

计数口径说明（避免两处数字打架）：gate 扫 **2888** 条（`get_all_modes` 会把 `M-ASM-001..010`
从顶层数组与 figure 节点**收割两次**，`verify_findings.py` 的 E 警告逐条列出）；
`apply_verification_status.py` 按 `mode_code` 去重，口径是 **2868** 条。两者都如实打印。

## 9. 复现命令清单

```
# 字段类型实测（第 0 节表）
python3 /opt/data/profiles/san-martin/cache/scratch/z3/field_types.py
# 修复前后对照（第 3 节）
python3 /opt/data/profiles/san-martin/cache/scratch/z3/compare.py
# 窗口内候选与 conflict 明细（第 4/5 节）
python3 /opt/data/profiles/san-martin/cache/scratch/z3/review2.py
# 残留盲区交叉核验（第 7 节第 2 条）
python3 /opt/data/profiles/san-martin/cache/scratch/z3/fields_year.py
# 朴素规则候选面（用于对照误报面大小）
python3 /opt/data/profiles/san-martin/cache/scratch/z3/naive.py
# 负对照自测（第 6 节）
python3 tools/test_credibility_d45.py
```

脚本落在会话 scratch（`/opt/data/profiles/san-martin/cache/scratch/z3/`），**不随仓发布**；
关键数字与原始输出已逐段落进本报告。
