# 郭象 (H-GX-001) Phase 21 研究成果文档归档报告

生成时间: 2026-09-08 22:40 | 归档人: Antonio Pigafetta (pigafetta) | 主库: <repo> @ commit e51bdae (GX 合并)

## 一、人物概要

- 人物: 郭象 (Guo Xiang), 约252–312, 西晋, 魏晋玄学集大成期 (崇有派, 向郭注《庄子》)
- 领域: 本体论 / 治理哲学 / 诠释方法论
- schema: v6 | figures JSON mode_ids 10 条 | thinking_mode_count = 10

## 二、10 个思维模式 (M-GX-001 ~ M-GX-010)

| 编码 | 中文名 | 英文名 | 类别 |
|---|---|---|---|
| M-GX-001 | 独化分析法 | Self-Transformation (Duhua) Analysis Method | 哲学思维 |
| M-GX-002 | 性分定位法 | Nature-Allotment Positioning Method | 方法论 |
| M-GX-003 | 相因不相生法 | Mutual Conditioning, Not Mutual Generation Method | 方法论 |
| M-GX-004 | 无为而任法 | Non-Action through Allowing Method | 方法论 |
| M-GX-005 | 名教自然合一法 | Unifying Ritual Order and Spontaneity Method | 哲学思维 |
| M-GX-006 | 迹所以迹辨析法 | Trace vs. Source-of-Trace Discrimination Method | 方法论 |
| M-GX-007 | 冥极安分法 | Resting at the Utmost of One's Allotment Method | 哲学思维 |
| M-GX-008 | 寄言出意法 | Using Words to Catch Meaning Method | 方法论 |
| M-GX-009 | 大小齐观法 | Equalizing Great and Small Method | 哲学思维 |
| M-GX-010 | 无对玄同法 | Dark Convergence beyond Opposition Method | 哲学思维 |

## 三、场景 (C-GX-001 ~ C-GX-010, 中英双语各 10 条)

| 编码 | 模式 | 中文场景标题 |
|---|---|---|
| M-GX-001 场景 | M-GX-001 | 独化截断——根因分析 |
| M-GX-002 场景 | M-GX-002 | 足性定位——人才评价 |
| M-GX-003 场景 | M-GX-003 | 相因之辨——依赖关系审计 |
| M-GX-004 场景 | M-GX-004 | 无为而任——授权设计 |
| M-GX-005 场景 | M-GX-005 | 名教即自然——制度改良 |
| M-GX-006 场景 | M-GX-006 | 迹与所以迹——标杆学习 |
| M-GX-007 场景 | M-GX-007 | 冥极安分——既成事实止损 |
| M-GX-008 场景 | M-GX-008 | 寄言出意——高语境文本解读 |
| M-GX-009 场景 | M-GX-009 | 大小齐观——反排行榜思维 |
| M-GX-010 场景 | M-GX-010 | 无对玄同——僵持议题升维 |

注: 郭象场景在 scenarios_zh/en.json 中以模式编码 (M-GX-001~010) 为 code/场景主体（应用领域如 哲学/复杂性科学/管理/个人），scenarios_zh 与 scenarios_en 各 10 条一一对应；与王弼采用 C-WB-xxx 编号体例不同，属合法变体（与 modes_data 对齐，无错位）。

## 四、标签与索引

- data/scenario_tags.json: H-GX-001 条目 10 条（第 855–923 行区间），每模式一条规范中英标签，与 modes_data 名称对齐
- code_maps.json H-GX-001: mode_ids 10 | scenarios 20 条 (zh 10 + en 10) | 跨引用 3
- 三文件 (figures JSON / code_maps / modes_data) mode_ids 完全一致: 10=10=10 ✓

## 五、跨引用 (3 条, figures JSON 与 docs/figures/H-GX-001.md 完全一致)

- H-WB-001 [ontological_reversal]: 王弼贵无 (有生于无) vs 郭象崇有 (无不能生有、独化自生)——魏晋玄学'贵无—崇有'对称两极
- H-DZS-001 [order_vs_spontaneity]: 董仲舒他律秩序 (天人感应) vs 郭象自发秩序 (物各自造)
- H-SMQ-001 [historiography_vs_philosophy]: 司马迁时间之流求贯通 vs 郭象存在之网辨条件

注: docs/figures/H-SMQ-001.md 缺失为 Phase 21 已知遗留问题（上游 QA handoff 已声明，建议单独修复卡），不影响本归档三处跨引用在 figures/code_maps 层面的有效性。

## 六、文档档案

- docs/figures/H-GX-001.md: 18,045 字符, 158 行, 覆盖全部 10 模式 (M-GX- 引用 16 处) + Protreptic 映射 + 跨人物关联 + 现代价值
- data/figures/H-GX-001.json (7.7KB), data/individuals/H-GX-001.json (10.7KB) + H-GX-001_modes.json (33.7KB)

## 七、Git 归档记录

- e51bdae Phase 21: 郭象(H-GX-001)增量合并入主库 (9 文件, +2256 行)
- af79031 / dc988de / 30cd0fb: 王弼合并与 QA（先行提交，与本归档无 GX 文件交集，已核 git status 无 GX 未提交改动）

## 八、核查结论

全部核查通过: schema v6 一致、10 模式三文件 ID 一致、中英场景 10+10 对应且场景标题与 modes_data 对齐、scenario_tags 10 条规范、code_maps 完整、文档覆盖全模式、3 跨引用一致、已提交主库 (e51bdae)、GX 文件无未提交改动。归档状态: **完成**。
