# Phase21-R8 王祥 H-HZX-002 重建落盘报告

- 卡号：t_5c183962（Phase21-R8；前置卡 t_8c521af7 / t_b92cc1cf）
- 日期：2026-09-23　执行：elcano
- 唯一依据：docs/research/phase21r7_wangxiang_sourcing_report.md / .json（重制素材包 P01-P16、锚 A01-A12、异文 V1/V2/V3）
- 结论：10 条 M-WX-001~010 与 figure 修正稿（H-HZX-002）已落盘；独立核验 58 PASS / 0 FAIL（含新增锚登记一致性组 I2）；门禁 credibility_gate --hard-fail exit 0（新增硬失败 0 条）；全库编码 0 碰撞；主库零写入；归档三件 sha256 未变。

## 1. 落盘产物清单（含 sha256）

| # | 路径 | bytes | sha256 |
|---|------|-------|--------|
| 1 | data/figures/H-HZX-002.json | 47232 | eb7b7f5c1c691439c51039132ff7980eecaddcd8a320124985da4400d90f69cb |
| 2 | data/individuals/H-HZX-002.json | 5667 | c98a8e8047576d37ab79df68216df197031c7138694bbd42050828a88c13821a |
| 3 | data/individuals/H-HZX-002_modes.json | 41696 | ddc9bcbf8c5f6688056624381b8a0a9679d7f3d9f420f3bdc315c1919842ffdf |
| 4 | docs/scratch/legacy20_r8_wangxiang_landing/figures/H-HZX-002.json | 47232 | eb7b7f5c1c691439c51039132ff7980eecaddcd8a320124985da4400d90f69cb |
| 5 | docs/scratch/legacy20_r8_wangxiang_landing/individuals/H-HZX-002.json | 5667 | c98a8e8047576d37ab79df68216df197031c7138694bbd42050828a88c13821a |
| 6 | docs/scratch/legacy20_r8_wangxiang_landing/individuals/H-HZX-002_modes.json | 41696 | ddc9bcbf8c5f6688056624381b8a0a9679d7f3d9f420f3bdc315c1919842ffdf |
| 7 | docs/scratch/legacy20_r8_wangxiang_landing/modes_library_entries.json | 40837 | e2b9f472c13e6826244dbb31d9afa6a02fb90b910aafaf979ae4f26bdbc9c143 |
| 8 | docs/scratch/legacy20_r8_wangxiang_landing/combined_library_entries.json | 41593 | d1229dd0b3ea49411867ee6d324c45e74db890f84d2eb2cbabdefa2db81d7a9d |
| 9 | docs/scratch/legacy20_r8_wangxiang_landing/id_mapping.tsv | 1115 | c25c20263d2a4bec88ad9bbe4a51cad62ebf4e70f29c49eba08c4dc60c8c17f6 |
| 10 | docs/scratch/legacy20_r8_wangxiang_landing/category_mapping.tsv | 737 | 699ec04f7bdf0ea549e20af02d9efedb83ac7002683b370892eefa70ee00dd3f |
| 11 | docs/scratch/legacy20_r8_wangxiang_landing/scenario_notes.json | 565 | 4192034f155b913d425633ded48b28bee849e46275eb26b58a00966ee62c9949 |

产出证据双份：`data/audit/phase21r8_wangxiang_landing_manifest.json` 与 `docs/research/phase21r8_wangxiang_landing_evidence.json`（同内容，本报告数值取自该清单）；核验证据 `docs/research/phase21r8_wangxiang_verify_evidence.json`；门禁原始输出 `docs/research/phase21r8_wangxiang_gate.txt`。

## 2. 逐条结果（P 编号 / 锚 / quote 核验）

| 新码 | 题旨 | 锚（类型） | P 编号 | 旧号 | key_quote 逐字核验 |
|------|------|------------|--------|------|--------------------|
| M-WX-001 | 侍疾尝药法 | A04（传记锚） | P01 | M301 | ✔ 与素材包逐字一致 |
| M-WX-002 | 卧冰求鲤法 | A01（传记锚） | P02 | M302 | ✔ 与素材包逐字一致 |
| M-WX-003 | 孝道至上法 | —（义理出处（非传记锚）） | P13 | M303 | ✔ 与素材包逐字一致 |
| M-WX-004 | 以身许物法 | A01（传记锚） | P02 | M304 | ✔ 与素材包逐字一致 |
| M-WX-005 | 孝道循环法 | A03（传记锚） | P04 | M305 | ✔ 与素材包逐字一致 |
| M-WX-006 | 求而得之法 | A02（传记锚） | P03 | M306 | ✔ 与素材包逐字一致 |
| M-WX-007 | 修心养性法 | A04（传记锚） | P05 | M307 | ✔ 与素材包逐字一致 |
| M-WX-008 | 立身五本：信德孝悌让 | A09（传记锚） | P07 | M308 | ✔ 与素材包逐字一致 |
| M-WX-009 | 孝道传世法 | A10（传记锚） | P09 | M309 | ✔ 与素材包逐字一致 |
| M-WX-010 | 功德圆满法 | A11（传记锚） | P11 | M310 | ✔ 与素材包逐字一致 |

锚字段口径说明：

- M-WX-003 为义理出处（《孝经》章句，P13），不占 A01-A12 传记锚；evidence 中记为「义理出处为《孝经·开宗明义章第一》（可落源；非传记锚）」。
- M-WX-004 复用 A01 同段（P02 unknowns 段），记为「A01 同段复用」；M-WX-007 为 A04 段内后续（P05）；M-WX-010 为 A11 及其邻段（P11）。
- M-WX-002（P02，主锚 A01）与 M-WX-009（P09，主锚 A10）另有辅锚 A12《二十四孝》诗赞，见锚点登记 aux_used_by。

### 2.1 引文全文（10 条，逐字取自素材包）

- M-WX-001（P01，《晋书》卷三十三·王祥传）：父母有疾，衣不解帶，湯藥必親嘗。
- M-WX-002（P02，《晋书》卷三十三·王祥传（辅：元·郭居敬《全相二十四孝诗选》「卧冰求鲤」））：母常欲生魚，時天寒冰凍，祥解衣將剖冰求之，冰忽自解，雙鯉躍出，持之而歸。
- M-WX-003（P13，《孝经·开宗明义章第一》）：夫孝，德之本也，教之所由生也。／身體髮膚，受之父母，不敢毀傷，孝之始也；立身行道，揚名於後世，以顯父母，孝之終也。
- M-WX-004（P02，《晋书》卷三十三·王祥传）：母常欲生魚，時天寒冰凍，祥解衣將剖冰求之，冰忽自解，雙鯉躍出，持之而歸。
- M-WX-005（P04，《晋书》卷三十三·王祥传）：有丹柰結實，母命守之，每風雨，祥輒抱樹而泣。其篤孝純至如此。
- M-WX-006（P03，《晋书》卷三十三·王祥传）：母又思黃雀灸，復有黃雀數十飛入其幕，復以供母。
- M-WX-007（P05，《晋书》卷三十三·王祥传）：每使掃除牛下，祥愈恭謹。
- M-WX-008（P07，《晋书》卷三十三·王祥传·遗令）：夫言行可覆，信之至也；推美引過，德之至也；揚名顯親，孝之至也；兄弟怡怡，宗族欣欣，悌之至也；臨財莫過乎讓：此五者，立身之本。
- M-WX-009（P09，《晋书》卷三十三·王览附传（辅：元·郭居敬《全相二十四孝诗选》「卧冰求鲤」））：祥臨薨，以刀授覽，曰：「汝後必興，足稱此刀。」覽後奕世多賢才，興於江左矣。
- M-WX-010（P11，《晋书》卷三十三·王祥传（传末）；《晋书》卷三十三·史臣曰）：泰始五年薨，詔賜東園秘器，朝服一具，衣一襲，錢三十萬，布帛百匹。……明年，策諡曰元。

要点：M-WX-002 引文本传作「剖冰」（P02），辅锚 A12/P14《二十四孝》诗赞用「臥冰」——两存为异文注记（不改主表述）；P16《搜神記》卷十一仅作旁证，未入 key_quote。

## 3. 裁定执行记录（船长裁定 10 项，逐项落实）

1. 条数=10，编号 M-WX-001~010（落盘前全库编码集查重：0 碰撞）
2. M-WX-001（原 M301）换题旨「侍疾尝药法」，锚 A04/P01；禁用旧题旨（数据文件零使用，仅证据登记）
3. M-WX-002（原 M302）更名「卧冰求鲤法」，主锚 A01/P02 + 辅锚 A12/P14/P15
4. M-WX-008（原 M308）改题「立身五本：信德孝悌让」（遗令五者），锚 A09/P07/P08，独立成目不并入 M-WX-009；禁用旧题旨（数据文件零使用，仅证据登记）
5. M-WX-009（原 M309）子项降级为「元代教材化见《二十四孝》」（A12/P14）
6. 其余 003/004/005/006/007/010 按报告 §4 路线逐条锚定（素材 A03-A11/P03-P13）
7. 底本=W1/W3 通行本用字（未/灸/覆）；V1-V3 异文于 evidence/备注登记，不擅改字
8. A08 标签用中性表述「长揖晋王」+ evidence 注记（原文「及武帝爲晉王」按《晋书》用例武帝=司馬炎）
9. figure 层以 corrected_record.json 为基线（字休徵/汉末至西晋/孝道儒家/works 清空生效）；figure 码维持 H-HZX-002
10. key_quote 逐字取自 P 系列；source_chapter 用可落源格式（《晋书》卷三十三·王祥传 等）；旧自造句零保留

## 4. 异文登记（V1/V2/V3）

| 异文 | 条目 | 底本用字（本档） | 异文 | 登记位置 |
|------|------|------------------|------|----------|
| V1 | 漢未遭亂 未/末 | 未（W1/W3 通行本） | 末（W2 四库全书本） | 未入本卡条目（A05 未引用）；登记于本证据与 figure caveats |
| V2 | 黃雀灸 灸/炙 | 灸（W1/W3 通行本） | 炙（W2 四库全书本、W4 搜神記） | M-WX-006 representative_cases 备注 + 本证据 |
| V3 | 言行可覆 覆/復 | 覆（W1/W3 通行本） | 復（W2 四库全书本） | M-WX-008 representative_cases 备注 + 本证据 |

## 5. 锚点登记（A01-A12）

| 锚 | 内容 | 主用条目 | 辅用条目 | 落源判定 |
|----|------|----------|----------|----------|
| A01 | 卧冰求鲤 | M-WX-002、M-WX-004 | — | 可落源 |
| A02 | 黄雀入幕 | M-WX-006 | — | 可落源 |
| A03 | 抱树守柰 | M-WX-005 | — | 可落源 |
| A04 | 侍疾 | M-WX-001、M-WX-007 | — | 可落源 |
| A05 | 避乱隐居 | — | — | 可落源 |
| A06 | 治州政绩与民谣 | — | — | 可落源 |
| A07 | 三老讲学 | — | — | 可落源 |
| A08 | 长揖晋王 | — | — | 可落源 |
| A09 | 遗令五者（立身之本） | M-WX-008 | — | 可落源 |
| A10 | 佩刀授览（家族传承） | M-WX-009 | — | 可落源 |
| A11 | 史评 | M-WX-010 | — | 可落源 |
| A12 | 二十四孝诗赞 | — | M-WX-002、M-WX-009 | 可落源 |

A08 说明：标签按船长裁定用中性表述「长揖晋王」；原文「及武帝爲晉王」按《晋书》用例武帝=司馬炎（R7 报告 §8-2）；该锚未入素材包，未作引文入条目，登记于此

锚登记与实际锚定的一致性由核验脚本 I2 组逐锚比对（登记 used_by 与条目实际锚定集合相等；A12 辅证覆盖 M-WX-002 / M-WX-009）。

## 6. 核验与门禁结果

- 独立核验脚本 verify_phase21r8_wangxiang.py：58 PASS / 0 FAIL。分组：A 产物与编号 / B 三面一致 / C 互引交叉 / D 引文逐字 / E 全库 0 碰撞 / F 主库零写入 / G 字段完整 / H 底本与异文 / I 裁定执行 / I2 锚登记一致性 / J 归档件未动 / K 门禁。
- 引文口径：10 条 key_quote_zh 全部逐字命中素材包；条目内「」引文片段全部为素材包字符串子串，白名单外 0 条（白名单仅含模式名/锚名/自撰术语：亲当其难、亲自去求、亲自在场、以身许之、以身许物、卧冰、卧冰求鲤、求而得之、黄雀入幕）。
- 门禁：credibility_gate --hard-fail → exit 0；hard failures 0；新增（基线外，必拦）0 条；D4 引文真子串核验 10 条 unchecked（理由：缓存未覆盖整部作品 9 / no-fulltext-link 1，如实记录，非缺陷声明）；D5 时间线 0 命中、10 条 undetermined（无 4 位年份 token）。
- 全库编码查重：M-WX-001~010 在本卡路径与已知规划文档之外 0 主体占用；旧号 M301~M310 在图档内仅出现于 legacy_mode_id / mode_ids_note 字段（结构级核验，id_mapping.tsv 10 行对照齐全）。
- 主库零写入：data/modes_data.json、data/code_maps.json、data/scenarios_zh.json、data/scenarios_en.json、data/scenario_tags.json、data/figure_names.json 六件 0 占用；核验时六件工作区与 HEAD 字节一致。
- 归档件未动：data/figures/_duplicates/ 下 H-HZX-002_figures.json、H-HZX-002_figures_modes.json、H-HZX-002_research_phase20.md 三件 sha256 与 R7 报告登记逐件一致（未改动、未删除、未镜像）。
- 互引：条目间 related_modes 22 条链接全部落本件新码，0 悬空；cross_references 目标 H-ZX-001 在 code_maps 已注册。

## 7. 边界与遗留（不属本卡）

1. 场景附随件：scenarios_zh/en、scenario_tags 注册属合并卡（2/4）；C-HZX-001~010 场景码已被 H-HZX-001（黄宗羲）占用，王祥场景接入前须另定前缀（候选见 docs/scratch/legacy20_r8_wangxiang_landing/scenario_notes.json）。
2. figure 层待核项：卒年异说、wiki_id、别名残留（修正稿 _pending_verification 登记）另卡处理，本卡未处置。
3. 发布仓镜像与 push：由合并卡收敛（本卡不含发布仓写入）。
4. 禁用旧题旨字符串策略：两处旧题旨字符串仅出现于证据登记的禁止记录处，数据文件零使用（zombie_scan 逐件核验为空）。
5. 版本用字：底本从 W1/W3 通行本（未/灸/覆）；异文 V1-V3 登记不擅改字（见 §4）。

## 8. 证据与产物路径

- 生成器：tools/build_phase21r8_wangxiang.py（落盘前全库查重 + 逐字断言 + zombie_scan + 清单/证据生成）
- 核验器：verify_phase21r8_wangxiang.py（58 项，读产物与素材包独立复核）
- 证据：data/audit/phase21r8_wangxiang_landing_manifest.json、docs/research/phase21r8_wangxiang_landing_evidence.json、docs/research/phase21r8_wangxiang_verify_evidence.json、docs/research/phase21r8_wangxiang_gate.txt
- 冻结副本与合并卡输入：docs/scratch/legacy20_r8_wangxiang_landing/（figures/、individuals/、modes_library_entries.json、combined_library_entries.json、id_mapping.tsv、category_mapping.tsv、scenario_notes.json）

