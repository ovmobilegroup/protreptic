# Phase 20-QA 验收报告：章学诚 (Zhang Xuecheng, H-ZXC-001)

- **本卡**: t_544b2112（[Phase 20] QA审查：章学诚 数据质量验收，assignee: espinosa）
- **复核对象**: `32d5bf86`（HEAD；ZXC 数据落地 `6e429676` + 档案登记 `6061d295`，自 `6061d295` 起 ZXC 相关文件 blob 未变）
- **上游交接**: t_7326611d（barbosa 增量合并复核 92/92 PASS，零改动零提交）
- **本卡结论**: **PASS（经热修）**——独立深检 `verify_zxc_qa_espinosa.py` **114/114 PASS**（修复前 84/114，恰好命中 30 项缺陷断言，判据非空转）；热修后孤立树三口径复核：上游 `verify_zhangxuecheng_phase20.py` **74/74**、barbosa `verify_zxc_merge_indep.py` **92/92**、本卡 **114/114**。
- **方法**: 全部结论基于冻结快照 + 两版在线原文（zh.wikisource《文史通义》卷一~卷八全 8 卷、《校雠通义·叙》guoxue123 版）逐字比对，不采信上游报告结论。

## 一、独立复核范围

1. **引文核验面**：10 条 v6 模式的 `key_quote_zh/_en`（含图档 `mode_evidence`）逐句回溯到原文；对无法溯源的语句用 7 路网络检索（含整句精确检索）复核，排除冷僻篇目与异文可能。
2. **数据面一致性**：主库 `modes_data.json` ⇄ 源档 `H-ZXC-001_modes.json`（v6 块逐字一致；Phase 21 建档 legacy 块保全）⇄ 图档三镜像（SHA256 一致，`mode_evidence == 出处+「：」+引文`）⇄ 档案 `docs/figures/H-ZXC-001.md`（定义/引文中英/案例逐字一致）。
3. **回归护栏**：双语场景、scenario_tags、code_maps、figure_names、PHASE 21 源码映射（E/F 段）。
4. **语言纯度**：`_en` 无 CJK、`_zh` 无 3+ 连续拉丁词（H 段）。

## 二、脚本结果

| 口径 | 修复前 | 修复后（工作区） | 修复后（孤立树 HEAD+热修） |
|---|---|---|---|
| 本卡 `verify_zxc_qa_espinosa.py` | 84/114 PASS，**30 FAIL** | 114/114 PASS | **114/114 PASS** |
| 上游 `verify_zhangxuecheng_phase20.py` | — | 73/74（见第五节①，他卡并发所致） | **74/74 PASS** |
| barbosa `verify_zxc_merge_indep.py` | — | 92/92 PASS | **92/92 PASS** |

修复前 30 项 FAIL 全部落在本卡 21 处缺陷修正的断言上（A4/A5/A6 逐字、A10~A15 定义/案例、B1~B4 黑名单、D 段逐句溯源），无环境性误报。

## 三、新发现缺陷与热修（8 模式 21 处 × 6 面）

热修传播面：`data/modes_data.json`（+21 行）⇄ `data/individuals/H-ZXC-001_modes.json`（v6 块 +20 行，legacy 建档块按档案保全原则**未动**）⇄ 三镜像（各 +15 行）⇄ `docs/figures/H-ZXC-001.md`（+20 行）。

| # | 模式 | 字段 | 修复前 | 修复后 | 判据 |
|---|---|---|---|---|---|
| 1 | M-ZXC-002 | key_quote_zh | 「《春秋》方以智，即宪章祖述之义也」 | 「撰述欲其圆而神，记注欲其方以智也」 | 整句精确检索 0 命中；原文只有「《尚书》圆而神…」与「撰述欲其圆而神，记注欲其方以智也」（书教下），且配对为马/班（圆神/方智），无《春秋》配「方以智」之说 |
| 2 | M-ZXC-002 | key_quote_en | the Spring and Autumn is square and wise. | creative composition should be round and spiritual, documentary registration square and wise. | 同步 #1 |
| 3 | M-ZXC-002 | definition_zh | 史有二体——《尚书》圆而神，《春秋》方以智。 | 史有二体——撰述欲其圆而神，记注欲其方以智也。 | 同步 #1（定义层同源不可溯源表述） |
| 4 | M-ZXC-002 | definition_en | （yuan er shen, after the Documents）/（fang yi zhi, after the Spring and Autumn） | （yuan er shen）/（fang yi zhi） | 去掉两处不可溯源的经典归属 |
| 5 | M-ZXC-003 | key_quote_zh | …之心术也。慎辨于天人之际… | …之心术也。**当**慎辨于天人之际… | 原文作「当慎辨于天人之际，尽其天而不益以人也」（史德）；两版一致，属脱字 |
| 6 | M-ZXC-004 | key_quote_zh | 非是不为功；…非是不为密 | 非是不为**取裁**；…非是不为**按据** | 原文见答客问中：「然而独断之学，非是不为取裁；考索之功，非是不为按据」，「功/密」为改写 |
| 7 | M-ZXC-004 | key_quote_en | achieves nothing without this… | is not without its material for selection… grounds of evidence | 同步 #6，语义回正 |
| 8 | M-ZXC-004 | source_chapter | 《文史通义·答客问上》/《博约》 | 《文史通义·答客问**中**》/《博约》 | 「独断之学/考索之功」正文在答客问中（全库 7 处命中皆在中/下篇，上篇无）；后半句在博约下 |
| 9 | M-ZXC-005 | key_quote_zh | 道不离器，犹影不离形**也**。 | 道不离器，犹影不离形。 | 原文无「也」（原道中，两版一致），衍字 |
| 10 | M-ZXC-007 | key_quote_zh | 仿纪传之体而作志 | 仿纪传**正史**之体而作志 | 原文「仿纪传正史之体而作志」（方志立三书议），脱字 |
| 11 | M-ZXC-007 | key_quote_en | after the annals-biography form, | after the annals-biography form **of the standard histories**, | 同步 #10 |
| 12 | M-ZXC-008 | key_quote_zh | 「通史之修，其为用有二：一则仍守先正成法…史以事义为经，不以朝代为断」 | 「通史之修，其便有六：一曰免重复…六曰详邻事。其长有二：一曰具翦裁，二曰立家法」 | 原句「其为用有二/先正成法/事义为经」全文检索 0 命中（两版 + web）；释通原文为「其便有六…其长有二…其弊有三」 |
| 13 | M-ZXC-008 | key_quote_en | General history serves either to transmit… | Compiling a general history has six advantages… | 同步 #12 |
| 14 | M-ZXC-008 | definition_zh | 通史之修，其为用有二：一者仍守先正成法… | 通史之修，其便有六（免重复、均类例、便铨配、平是非、去抵牾、详邻事），其长有二（具翦裁、立家法）。 | 同步 #12 |
| 15 | M-ZXC-008 | definition_en | serves two aims: preserving ancestral method… | has six advantages… and two strengths… | 同步 #12 |
| 16 | M-ZXC-009 | key_quote_zh | 「敬非修德之谓，而所以执事；恕非宽容之谓，而所以论文」等改写句 | 「临文必敬，非修德之谓也；论古必恕，非宽容之谓也」+「敬非修德之谓者，气摄而不纵…恕非宽容之谓者，能为古人设身而处地也」 | 原文见文德；「而所以执事/而所以论文」检索 0 命中，属改写；修正后全句逐字可溯源（并回补「设身处地」义） |
| 17 | M-ZXC-009 | key_quote_en | Reverence is not moral cultivation but the discipline… | Reverence before the text is not moral cultivation…place oneself in the ancients' situation | 同步 #16 |
| 18 | M-ZXC-009 | representative_cases_zh[1] | 「逆其意而探其原」 | 「论古必先设身」，知其世而后论其文 | 「逆其意而探其原」检索 0 命中；文德原文「论古必先设身」 |
| 19 | M-ZXC-009 | representative_cases_en[1] | 'reversing their intent to explore their origins' | 'in judging antiquity one must first place oneself in the ancients' situation' | 同步 #18 |
| 20 | M-ZXC-010 | source_chapter | 《文史通义·原学》/《家书》 | 《文史通义·浙东学术》/《家书》 | 引文「学者不可无宗主，而必不可有门户」出自浙东学术；原学篇无此句（定义主题「救风气」另见观察④） |
| 21 | M-ZXC-010 | mode_evidence.source | 同上（镜像 2 处：evidence_zh 前缀 + source 字段） | 同上 | 证据行与出处须一致 |

> 说明：黑名单断言（B1~B4）对修正前文本在「主库 M-ZXC 条目 / 源档 v6 块 / 图档镜像 / md 模式区」四类面内要求零残留，修复后全部归零。

## 四、复核确认（无缺陷项）

- **引文逐句溯源 D 段**：10 条引文全部逐句 ⊆ 两版原文摘录（含热修后 8 条），无剩余不可溯源语句。
- **M-ZXC-001 / 006**：引文与原文一致（易教上；校雠通义·叙），出处标注成立（006 并列「互著」为模式主题篇目，引文在叙，允许）。
- **结构面**：v6 块与主库逐字一致（C2）；Phase 21 建档 legacy 块 10 条（M359~M368）按档案保全未动（C3/C4）；`mode_evidence == 出处+「：」+引文`（E5）；三镜像 SHA256 修复后 `5a8640d39de6ce05715206fa01203fd20d6a1a6d0b0d59cc588fa3d2bc4751ee`（E1）。
- **场景/标签/映射**：双语场景各 10、scenario_tags 20、code_maps（10 模式/10 标签/3 交叉引用）、figure_names 唯一映射、M359~M368→M-ZXC-001~010 映射全通过（F 段）。
- **语言纯度**：M-ZXC-001~010 全字段 0 违规（H 段；含对 `_zh` 内 3+ 连续拉丁词的新增扫描）。

## 五、遗留与观察（非阻断）

1. **共享工作区并发（环境现象，非本卡引入）**：复核期间 `data/modes_data.json` 工作区含他卡未提交新增（194 条 M-BLT/M-SQR 等 ID），致上游口径第 2 项「total == modes 长度」暂 73/74（total=2948 vs len=3142）。孤立树（HEAD+本卡热修）复跑三口径全通过（74/74、92/92、114/114），证明与本卡无关；本卡提交采用索引定点方式，**仅含 M-ZXC 条目 hunk**，未夹带他卡在途改动。
2. **Sep-9 遗留 entry 三件**（`data/modes_data_entry_H-ZXC-001.json`、`data/code_maps_entry_H-ZXC-001.json`、`data/scenario_tags_entry_H-ZXC-001.json` 及 `merge_zxc.py`/`qa_zxc_final.py`）按上游裁定未动；其中 entry 件含旧编草稿码（M359~M368）与旧版本文本，属审计遗留，不参与库内一致性面。
3. **M-ZXC-003 定义内**「慎辨于天人之际，尽其天而不益以人」为释义性缩略标签（未随引文补「当」）；引文面已修正，定义标签不影响溯源判据。
4. **M-ZXC-008 定义保留**「史以事义为经，不以朝代为界」为撰写性概括（无引号），引文面已全部替换为释通原文；如需进一步收紧可另卡处理。
5. **M-ZXC-010 定义首句**「学业将以救风气之敝…」属《家书》系文本；《文史通义》两版在线全文不含家书诸篇，**无法在线核验**（非证伪），本卡不作断言。出处面已按引文补《浙东学术》。
6. **模式名「嘉惠后学」** 为库内命名；章氏原文作「嘉惠来学」（《和州志前志列传序例下》）。命名层未动（不属本卡裁量）。

## 六、工件与复现

- 独立脚本：`verify_zxc_qa_espinosa.py`（A~H 八段共 114 项断言，修复前后均可运行）
- 复现命令（repo 根）：
  ```
  python3 verify_zxc_qa_espinosa.py        # 本卡 114/114
  python3 verify_zhangxuecheng_phase20.py  # 上游 74/74
  python3 verify_zxc_merge_indep.py        # barbosa 92/92
  ```
- 修复前/后原始输出（会话工件，未提交）：`workspaces/t_544b2112/qa_pre.out`（84/114）、`qa_post.out`（114/114）、`upstream_post.out`、`recheck_post.out`；孤立树 `/snap_post`。
