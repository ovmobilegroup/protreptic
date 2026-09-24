# Phase21-W8 Stage2 批1 工具/管道：书级归并重扫口径修复 + 批1 fetch 素材包。

卡号 `t_70a8cbce`（Phase21-W8 Stage2 批1）；上游书单 `t_6ed4fe0d`（commit 20b13092）。
生成：2026-09-24 13:36（本地时区）。 产线：W5 pilot 修复链口径。

## 一、概述。

1. **候选生成口径修复（build_source_links 侧）**：旧口径按「条目内去重 + 篇章跨度」计数，书级被引 >= 3 而单跨度 < 3 的书（《论衡》类）从未成为候选（pilot 报告 §2.1 根因条）。 新口径 = 扫全部书名号原始跨度（不去重）→ 按中点「·」首段归并为书级 → 计数始终在书级。
2. **批1 fetch 素材包**：按书单抓 17 抓取项（16 部书；二程遗书与河南程氏遗书共源）主源全文入本地缓存（独立索引，零主库写），并对批1 各书全部 mode 引文逐条对照，产出 quote / variant（异文）/ null（查无）/ cross-lang 四档结论。

关键数字（[实测-本卡]）：

| 项 | 数 | 说明 |
|---|---|---|
| 对账 baseline hot68 | 68 | baseline 20b13092（modes 3291）复扫；与书单 hot68 逐名一致：True |
| 对账 dedup 口径 | 59 | 条目内去重口径（书单备注的 59）|
| live 复扫 | 70 | 工作区 modes 3311；相对 hot68 增量 安子介先生生平, 浮生六记 |
| 批1 条目 | 18 | 17 书 + 现代诗（否定记录）|
| 逐条引文 | 154 | mode 级；跨度实例 159；null 中近似档 28 |
| quote（命中） | 3 | 原文逐字（空白/标点归一）|
| variant（异文） | 20 | 繁简差：引文侧 zh-hant 或 zh-cn 副本命中 |
| null（查无） | 57 | 两副本未见（含否定记录 8 条）|
| cross-lang | 74 | 跨语言书，留语义对照档 |
| 负对照 | 16 | 单字符扰动，假阳性 0 |

## 二、输入与基线。

- 书单：`docs/research/phase21w8_stage2_batch1_booklist.json`（sha256-16 `ca46eb42471c35fc`；hot68 全量 rows、batch1 18 项、method 段口径）。
- 素材包源：`data/modes_data.json` 快照 `736aab3b4164973d`（modes 3311；工作区含在途 R9 落盘）。
- 缓存索引：`data/audit/source_texts_w8_stage2_batch1.json`（本卡独立索引；不改动 `data/audit/source_texts.json` 与 `data/source_links.json`）。
- 逐页清单：`tools/manifests/w8_stage2_batch1_texts.json`（17 抓取项；现代诗 fetch=none 不抓）。
- 上游参考：`docs/research/phase21w5_wangchong_sourcing_report.md`、`docs/research/phase21w5_wangchong_archive_report.md` §2.1（根因条）。

## 三、方法。

**3.1 候选口径修复**：新增 `source_link_index.extract_refs_raw`（保序、不去重）与 `build_source_links.count_citations`（书级归并；span/book 双计数）；候选门槛 = 书级被引 >= min 且无任何 candidate_key 在索引中。 复核：`python3 tools/build_source_links.py --bookcount-report --modes-spec REV:data/modes_data.json`。

**3.2 全文抓取**：`tools/fetch_batch1_texts.py`（新）按 manifest 抓取：子页枚举三模式（`links`/`allpages`/`list`），正文两通道（`raw`=action=raw；`render`=action=parse，用于 ProofreadPage 转写页与多列页）。 coverage：complete/partial/single-page；缺页登记 `pages_failed`；中文书另产 zh-cn 转换副本（D4 层）。 缓存只在 `data/audit/`（零 modes_data 写）。

**3.3 逐条对照**：`tools/build_batch1_sourcing_pack.py`（新）逐条比 `key_quote_zh`：quote（逐字，空白/标点归一，省略号分段）。variant（繁简：引文整批转 zh-hant 或 zh-cn 副本命中）。null（未见；附 elsewhere 与近似诊断：句命中 n/m、3 字窗比例）。cross-lang（非中文源不适用逐字对读）。 负对照 = 逐书抽 2 条做单字符扰动必查无；`weak` 标 < 6 字短引文。

## 四、执行结果。

**4.1 候选口径对账（[实测-本卡]）**。

- baseline（`20b13092:data/modes_data.json`，modes 3291）：书级名 2086、跨度名 2403；新口径 >=3 未解析 **68 本**（与书单 hot68 逐名一致：True）；旧口径 59 本；差集 9 本：世界报, 大诰, 学说汇纂, 战史, 班师议, 琵琶行, 瑜伽师地论, 禹贡, 马可。
- live（工作区，modes 3311）：新口径 70 本 / 旧口径 61 本；相对 hot68 增量 安子介先生生平, 浮生六记（在途 R9 卡新增 mode，非口径回归）。
- 结论：68 本漏收根因已修复且可复核；差集方向 = 旧口径只漏不收（new_only 9 本、old_only 0 本）。

**4.2 缓存状态（逐本 [实测-本卡]）**。

| 书 | rank | 主源 | 抓取 | 通道 | 状态 | 覆盖 | 子页 ok/枚举 | chars | zh-cn | 逐条 | 分档 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 春秋繁露 | 1 | 春秋繁露 | action=raw 逐页 | raw | ok | complete | 17/17 | 73419 | yes | 10 | q2/v2/n6/x0 |
| 理想国 | 2 | The Republic of Plato | action=render (raw 为 stub) | render | ok | complete | 11/11 | 869588 | - | 10 | q0/v0/n0/x10 |
| 陆九渊集 | 3 | 象山先生全集 (四部叢刊本) | action=render 逐页 | render | ok | complete | 39/39 | 278151 | - | 10 | q1/v1/n8/x0 |
| 庄子注 | 4 | 荘子注 (四庫全書本) | action=raw 逐页 | render | ok | complete | 11/11 | 302754 | - | 10 | q0/v3/n7/x0 |
| 老子注 | 5 | 道德經 (王弼本) | action=raw | render | ok | single-page | 0/0 | 32760 | yes | 10 | q0/v2/n8/x0 |
| 俄狄浦斯王 | 6 | Οιδίπους Τύραννος | action=raw | raw | ok | single-page | 0/0 | 56126 | - | 8 | q0/v0/n0/x8 |
| 伊利亚特 | 7 | Ιλιάς | action=render 逐卷 | render | ok | complete | 24/24 | 725855 | - | 9 | q0/v0/n0/x9 |
| 奥德赛 | 8 | Οδύσσεια | action=render 逐卷 | render | ok | complete | 24/24 | 574959 | - | 8 | q0/v0/n0/x8 |
| 河南程氏遗书 | 9 | 二程遺書 | action=raw 逐页 | raw | ok | complete | 25/25 | 192261 | - | 9 | q0/v0/n9/x0 |
| 二程遗书 | 10 | 二程遺書 | action=raw 逐页 | raw | ok-shared | complete | 25/25 | 192261 | - | 8 | q0/v5/n3/x0 |
| 战争史 | 11 | History of the Peloponnesian War | action=raw 逐卷 | raw | ok | complete | 8/8 | 1177087 | - | 9 | q0/v0/n0/x9 |
| 形而上学 | 12 | Metaphysics (Ross, 1908) | action=render (raw 为 stub) | render | ok | complete | 14/14 | 340880 | - | 7 | q0/v0/n0/x7 |
| 文史通义 | 13 | 文史通義 | action=raw 逐页 | raw | ok | complete | 9/9 | 203256 | yes | 8 | q0/v5/n3/x0 |
| 奥林匹克回忆录 | 14 | Mémoires olympiques | action=render 逐章 | render | ok | complete | 25/25 | 708864 | - | 8 | q0/v0/n0/x8 |
| 诗学 | 15 | The Poetics translated by S. H. Butcher | action=render (raw 为 stub) | render | ok | complete | 9/9 | 122003 | - | 8 | q0/v0/n0/x8 |
| 现代诗 | 16 | None | None | - | none-negative | - | - | None | - | 8 | q0/v0/n8/x0 |
| 太极图说 | 17 | 太極圖說 | action=raw | raw | index-page | - | 0/0 | 332 | yes | 7 | q0/v2/n5/x0 |
| 安提戈涅 | 18 | Αντιγόνη | action=raw | raw | ok | single-page | 0/0 | 46375 | - | 7 | q0/v0/n0/x7 |

索引 counts：{"ok": 15, "ok-shared": 1, "index-page": 1}；负对照 16 条、假阳性 0；weak 0；引文整批转 zh-hant：n=72 complete=True。

**4.3 逐条引文结论**（全量在报告 JSON 的 `quotes` 段）。

null（57 条；近似档 28 条 = 部分短句逐字命中、余为改写/拼合）：

- `M-DZS-001` 董仲舒《春秋繁露》：天之道，人之道一也。；句命中 0/1；3 字窗 0.5；最长连续 0.0
- `M-DZS-002` 董仲舒《春秋繁露》：《春秋》大一统者，天地之常经，古今之通谊也。；句命中 0/1；3 字窗 0.333；最长连续 0.235
- `M-DZS-004` 董仲舒《春秋繁露》：性有善质，而未能以为善也。；句命中 0/1；3 字窗 0.889；最长连续 0.0；近似档
- `M-DZS-007` 董仲舒《春秋繁露》：阳尊阴卑，天之制也。；句命中 0/1；3 字窗 0.667；最长连续 0.0
- `M-DZS-008` 董仲舒《春秋繁露》：质朴之谓性，性非教化不成。；句命中 0/1；3 字窗 0.333；最长连续 0.0
- `M-DZS-009` 董仲舒《春秋繁露》：承天意以从事。；句命中 0/1；3 字窗 0.5；最长连续 0.0
- `M-LJY-003` H-LJY-001《陆九渊集》：学苟知本，六经皆我注脚。；句命中 0/1；3 字窗 0.25；最长连续 0.0
- `M-LJY-004` H-LJY-001《陆九渊集》：易简工夫终久大，支离事业竟浮沉。；句命中 0/1；3 字窗 0.75；最长连续 0.571；近似档
- `M-LJY-005` H-LJY-001《陆九渊集》：学者之大病，在于无志。志苟立矣，则无往而不成功。；句命中 0/2；3 字窗 0.222；最长连续 0.2
- `M-LJY-006` H-LJY-001《陆九渊集》：先立乎其大者，则其小者不能夺也。；句命中 0/1；3 字窗 0.833；最长连续 0.714；近似档
- `M-LJY-007` H-LJY-001《陆九渊集》：或问：先生之学当自何处入？曰：不过切己自反，改过迁善。；句命中 0/2；3 字窗 0.75；最长连续 0.364；近似档
- `M-LJY-008` H-LJY-001《陆九渊集》：《易》赞乾坤之简易，曰：'易知易从，有亲有功，可久可大。'然则学无二事，无二道，；句命中 1/2；3 字窗 0.872；最长连续 0.561；近似档
- `M-LJY-009` H-LJY-001《陆九渊集》：心之体甚大，若能尽我之心，便与天同。；句命中 0/1；3 字窗 0.769；最长连续 0.533；近似档
- `M-LJY-010` H-LJY-001《陆九渊集》：或问：先生何不著书？对曰：六经注我，我注六经。；句命中 1/2；3 字窗 0.625；最长连续 0.667；近似档
- `M-GX-002` H-GX-001《庄子注》：夫小大虽殊，而放于自得之场，则物任其性，事称其能，各当其分，逍遥一也。；句命中 0/1；3 字窗 0.852；最长连续 0.483；近似档
- `M-GX-003` H-GX-001《庄子注》：天下莫不相与为彼我，而彼我均于自得。故独化之足对，非资待之所得。；句命中 0/2；3 字窗 0.615；最长连续 0.429；近似档
- `M-GX-004` H-GX-001《庄子注》：各安其天性，各用其能，则天机自张，无为而成。；句命中 0/1；3 字窗 0.75；最长连续 0.278
- `M-GX-007` H-GX-001《庄子注》：夫命行事变，不舍昼夜……推而极之，则今之所谓命者，皆吾之分也。；句命中 0/1；3 字窗 0.783；最长连续 0.4；近似档
- `M-GX-008` H-GX-001《庄子注》：夫庄子之言，不可以一途诘之……要其会归，遗其所寄。；句命中 0/1；3 字窗 0.556；最长连续 0.45；近似档
- `M-GX-009` H-GX-001《庄子注》：夫小大虽殊，而放于自得之场，则物任其性，事称其能，各当其分，逍遥一也。；句命中 0/1；3 字窗 0.852；最长连续 0.483；近似档
- `M-GX-010` H-GX-001《庄子注》：是以涉有物之域，虽复罔两，未有不独化于玄冥者也。故造物者无主，而物各自造。；句命中 1/2；3 字窗 0.767；最长连续 0.438；近似档
- `M-WB-001` H-WB-001《老子注》：《周易略例》：'义苟在健，何必马乎？类苟在顺，何必牛乎？'——乾之义在刚健，不必；句命中 0/3；3 字窗 0.0；最长连续 0.057
- `M-WB-003` H-WB-001《老子注》：《老子指略》：'老子之书，其几乎可一言而蔽之。噫！崇本息末而已矣。'；句命中 1/3；3 字窗 0.13；最长连续 0.12
- `M-WB-005` H-WB-001《老子注》：《周易·复卦注》：'天地虽大，富有万物，雷动风行，运化万变，寂然至无，是其本矣。；句命中 0/1；3 字窗 0.074；最长连续 0.103
- `M-WB-006` H-WB-001《老子注》：《周易略例·明彖》：'物无妄然，必由其理。统之有宗，会之有元，故繁而不乱，众而不；句命中 0/2；3 字窗 0.0；最长连续 0.065
- `M-WB-007` H-WB-001《老子注》：《老子注》二十九章：'圣人达自然之性，畅万物之情，故因而不为，顺而不施。'；句命中 0/1；3 字窗 0.808；最长连续 0.5；近似档
- `M-WB-008` H-WB-001《老子注》：《老子注》三十八章：仁义之教本于自然；失道而后德、失德而后仁——本失则末伪。；句命中 0/1；3 字窗 0.464；最长连续 0.333
- `M-WB-009` H-WB-001《老子注》：《老子注》三十八章：'以无为用，则得其母，故能己不劳焉而物无不理。'；句命中 0/1；3 字窗 0.833；最长连续 0.5；近似档
- `M-WB-010` H-WB-001《老子注》：《老子指略》：'名以定形，混成无形，不可得而定……言之者失其常，名之者离其真。'；句命中 0/1；3 字窗 0.481；最长连续 0.448；近似档
- `M-CHI-001` H-CHI-001《河南程氏遗书》：性即理也，何谓性？曰：天道焉而行乎人者也，谓之道。在天为命，在义为理，在人为性，；句命中 1/3；3 字窗 0.641；最长连续 0.512；近似档
- `M-CHI-002` H-CHI-001《河南程氏遗书》：涵养须用敬，进学则在致知。敬则自虚静，不可把虚静唤做敬。君子庄敬日强，安肆日偷。；句命中 2/3；3 字窗 0.625；最长连续 0.382；近似档
- `M-CHI-003` H-CHI-001《河南程氏遗书》：须是今日格一件，明日格一件，积习既多，然后脱然有贯通处。；句命中 0/1；3 字窗 0.864；最长连续 0.458；近似档
- `M-CHI-005` H-CHI-001《河南程氏遗书》：散之在万殊，万殊原于一理。理一分殊。；句命中 0/2；3 字窗 0.077；最长连续 0.2
- `M-CHI-006` H-CHI-001《河南程氏遗书》：须是今日格一件，明日格一件，积习既多，然后脱然有贯通处。；句命中 0/1；3 字窗 0.864；最长连续 0.458；近似档
- `M-CHI-007` H-CHI-001《河南程氏遗书》：人心私欲也，道心天理也。……无人欲即皆天理矣。饿死事极小，失节事极大。；句命中 1/3；3 字窗 0.577；最长连续 0.357；近似档
- `M-CHI-008` H-CHI-001《河南程氏遗书》：学莫先于致知。致知在格物。……能知则能行，行是知的结果。；句命中 1/3；3 字窗 0.4；最长连续 0.318
- `M-CHI-009` H-CHI-001《河南程氏遗书》：《大学》，孔氏之遗书，而初学入德之门也。……凡看文字，先须晓其文义，然后可求其意；句命中 1/2；3 字窗 0.621；最长连续 0.516；近似档
- `M-CHI-010` H-CHI-001《河南程氏遗书》：敬以直内，义以方外。敬义夹持，上下立矣。……合内外之道也。；句命中 2/3；3 字窗 0.7；最长连续 0.455；近似档
- `M-CHE-001` H-CHE-001《二程遗书》：吾学虽有所受，天理二字却是自家体贴出来。；句命中 0/1；3 字窗 0.188；最长连续 0.167
- `M-CHE-005` H-CHE-001《二程遗书》：性即理也，何止性，天道也。；句命中 0/1；3 字窗 0.5；最长连续 0.0
- `M-CHE-010` H-CHE-001《二程遗书》：君子之学，必至圣人而后己。不至圣人而自己者，皆弃也。；句命中 0/2；3 字窗 0.5；最长连续 0.273
- `M-ZXC-002` H-ZXC-001《文史通义》：《尚书》圆而神，其于史也，可谓天之至矣；撰述欲其圆而神，记注欲其方以智也。迁书体；句命中 0/2；3 字窗 0.9；最长连续 0.357；近似档
- `M-ZXC-003` H-ZXC-001《文史通义》：能具史识者，必知史德。德者何？谓著书者之心术也。当慎辨于天人之际，尽其天而不益以；句命中 3/4；3 字窗 0.882；最长连续 0.556；近似档
- `M-ZXC-009` H-ZXC-001《文史通义》：凡为古文辞者，必敬以恕。临文必敬，非修德之谓也；论古必恕，非宽容之谓也。敬非修德；句命中 1/3；3 字窗 0.906；最长连续 0.379；近似档
- `M-JX-001` H-JX-001《现代诗》：现代诗是横的移植，不是纵的继承。；句命中 0/1
- `M-JX-002` H-JX-001《现代诗》：新诗是知性的强调。；句命中 0/1
- `M-JX-003` H-JX-001《现代诗》：现代诗是纯粹的诗，区别於散文的诗。；句命中 0/1
- `M-JX-004` H-JX-001《现代诗》：存在主义是现代诗的源流。；句命中 0/1
- （另有 9 条见 JSON）

跨语言档（74 条，留语义对照）：理想国 10; 俄狄浦斯王 8; 伊利亚特 9; 奥德赛 8; 战争史 9; 形而上学 7; 奥林匹克回忆录 8; 诗学 8; 安提戈涅 7。

## 五、证据。

| 文件 | sha256-16 | bytes |
|---|---|---|
| tools/build_source_links.py | 0b363e04bc6e00e7 | 33374 |
| tools/source_link_index.py | b2c6074a61f753ff | 10795 |
| tools/fetch_batch1_texts.py | e072f4d645402b3c | 14149 |
| tools/build_batch1_sourcing_pack.py | 450d0e752732b9a2 | 17756 |
| tools/verify_batch1_sourcing_delivery.py | b94cc3a41ae53309 | 6212 |
| tools/build_batch1_sourcing_report.py | 910f1a5f7a0b186d | 19554 |
| tools/fetch_source_texts.py | 6b534db72ee00148 | 24766 |
| tools/manifests/w8_stage2_batch1_texts.json | 9f5823e5897630f5 | 9186 |
| data/audit/source_texts_w8_stage2_batch1.json | 24464156391bf86b | 86569 |
| data/audit/phase21w8_stage2_batch1_recount_baseline.json | 1cc8ff3bee740153 | 376529 |
| data/audit/phase21w8_stage2_batch1_recount_live.json | 6ddffad6c8631ad4 | 377566 |
| docs/research/phase21w8_stage2_batch1_booklist.json | ca46eb42471c35fc | 41293 |

报告两件（本文与 `.json`）为本次生成产物，自指校验和不列入上表；最终 sha256 以提交回执为准。

复现命令（[实测-本卡]）：。

- 口径对账：`python3 tools/build_source_links.py --bookcount-report --modes-spec 20b13092:data/modes_data.json --bookcount-json data/audit/phase21w8_stage2_batch1_recount_baseline.json`
- live 复扫：`python3 tools/build_source_links.py --bookcount-report --bookcount-json data/audit/phase21w8_stage2_batch1_recount_live.json`
- 抓取（增量）：`python3 tools/fetch_batch1_texts.py`（--dry-run 先枚举；--force 重抓）
- 素材包：`python3 tools/build_batch1_sourcing_pack.py`
- 独立核验：`python3 tools/verify_batch1_sourcing_delivery.py`

## 六、核验。

独立核验 `tools/verify_batch1_sourcing_delivery.py` 现跑输出（全文见 `data/audit/phase21w8_stage2_batch1_verify.log`）：。

```
PASS  C1 对账 baseline hot68 == 书单 hot68（逐名）  n=68
PASS  C2 live 为 hot68 超集且差集已登记  delta=['安子介先生生平', '浮生六记']
PASS  C3 dedup 口径数已登记（baseline）  hot_old=59
PASS  C4 verdict 取值域合法
PASS  C5 quotes_total 统计自洽  154
PASS  C6 各书逐条数之和 == 总数  154
PASS  C7 verdict 分项计数自洽  {'null': 57, 'variant': 20, 'quote': 3, 'cross-lang': 74}
PASS  C8 批1 十八书齐备  18
PASS  C9 负对照零假阳性  controls=16
PASS  C10 跨语言书结论全为 cross-lang  bad=[]
PASS  C11 中文书无 cross-lang 结论  bad=[]
PASS  C12 索引 counts 与 entries 重算一致  {'ok': 15, 'ok-shared': 1, 'index-page': 1}
PASS  C13 缓存文件 sha256 与索引登记一致  ok=21 bad=0 missing=0
PASS  C14 manifest 应抓书全部有索引条目  missing=[]
PASS  C15 现代诗为否定记录（fetch=none，无缓存条目）
PASS  C16 素材包快照 sha == 现文件 sha（读侧零写实证）  sha16=736aab3b4164973d mtime=12:32:08
----
TOTAL 16 PASS / 0 FAIL
```

零主库写入实证：本卡写盘仅限 tools/、data/audit/（缓存与对账）、docs/research/（报告）；`data/modes_data.json` 本卡全程只读（sha/mtime 恒定，见核验 C16 与提交回执）。

## 七、残留与风险。

- 抓取覆盖：轮内残留 partial/failed 书及缺页见四.2 表与索引 pages_failed；已跑补页修复（只补缺页），修复后原文变更的 zh-cn 副本标 stale。
- 庄子注（四庫全書本）：转录页为节录且含生僻/异体字（𩔖/㫖/㸃/荘/徃 等），逐字对读系统性受限（null 的 3 字窗 <= 0.17）；建议另立异体字归一轮或改判「待核」档。
- 老子注：本轮主源为「道德經（王弼本）」白文（无注文）；引文多为《老子注》《老子指略》《周易略例》注文（源外），null 为正确结论；下游需另抓王弼注全本。
- 太极图说：整篇为短篇（331 字符全文），MIN_CHARS=2000 阈值将整篇误标 index-page（非缺页）；对照按全文进行。
- 春秋繁露：《举贤良对策》类引文源在漢書卷056（非繁露），null 正确；繁露内部引文多为改写/拼合（3 字窗 0.33-0.89，其中近似档可作待核）。
- 跨语言 74 条：逐字对读不适用，建议入「语义对照」档（口径待船长裁定）；现代诗 8 条 = 否定记录。
- 双键同源：《河南程氏遗书》与《二程遗书》共源一文件（manifest shared_from），对账按各自 label 计。
- 跨度实例 159 vs mode 级 154：同 mode 多次引同一书时按 mode 去重。
- 字窗/句命中仅为辅助信号（近似档判定），不作为逐字结论。
- 通道教训：含模板注文的页面（四庫 {{SK notes}}、王弼注文标记）走 raw（wikitext）会被 raw_to_text 整段剥离 {{...}} 而丢注文；本轮实测改判 render：庄子注（注文恢复）、老子注（王弼注文恢复，11,099->32,836 字符）；后续批次遇注文含模板的书先实测通道再抓。
- render 通道带出的页面外壳（首行 mw-parser-output 断标签、页尾公有领域块）已由 tools/clean_batch1_cache_chrome.py 清理并重算 sha（9 书 20 文件）；对读为子串匹配，清理不改正文。

## 八、下一步与路由。

- 链接入库卡（下游）：以本报告 68 本对账 + 候选口径修复为准，扩 `data/source_links.json` 并跑全链。
- 素材包档位固定（quote/variant/null/cross-lang）供 Stage2 后续批次复用。
- 跨语言语义对照档、四庫异体字归一、王弼注本换源：待船长裁定/另立卡。

## 九、附链。

- 本卡：`t_70a8cbce`（Phase21-W8 Stage2 批1）；上游 `t_6ed4fe0d`（书单，commit 20b13092）；子卡 `t_b85ae14a`。
- 参考：`docs/research/phase21w5_wangchong_sourcing_report.md`、`docs/research/phase21w5_wangchong_archive_report.md` §2.1。

## 十、提交回执。

- 主提交：`ce1dc46b`（2026-09-24T11:29+08:00）；独立核验：16 PASS / 0 FAIL (tools/verify_batch1_sourcing_delivery.py)。
- 零主库写入：`data/modes_data.json` sha16 `6f3f4580397614f5`，mtime 2026-09-24 09:38:49 +0800（本卡全程未写）。
- 成品 sha16：
    - `docs/research/phase21w8_stage2_batch1_sourcing_report.md` `f4abf8d41e3e35ff`
    - `docs/research/phase21w8_stage2_batch1_sourcing_report.json` `8bcccff7c6299b94`
    - `data/audit/source_texts_w8_stage2_batch1.json` `24464156391bf86b`
    - `data/audit/phase21w8_stage2_batch1_recount_baseline.json` `1cc8ff3bee740153`
    - `data/audit/phase21w8_stage2_batch1_recount_live.json` `6ddffad6c8631ad4`
    - `tools/manifests/w8_stage2_batch1_texts.json` `9f5823e5897630f5`

