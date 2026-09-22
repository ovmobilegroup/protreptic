# 旧世代 20 件 v6 样例复刻（scratch 产物，未入库）

- 归属卡：t_a060cd41（Phase21-R3 旧世代 20 件档案 v6 复刻评估）
- 生成时间：2026-09-22
- 生成脚本：/opt/data/profiles/albo/cache/scratch/legacy20/build_samples.py（Pod 侧 scratch，非仓库文件）
- 纪律：本目录只作评估样例，未写入 data/、未提交、未同步发布仓。

## 1. 目录结构

    H-CHB-001/                           # 陈伯达（legacy M211-M220）
      figures/H-CHB-001.json             # v6 图档（modes 内嵌 10 条，mode_ids = M-CHB-001..010）
      individuals/H-CHB-001.json         # 图档镜像（去 modes）
      individuals/H-CHB-001_modes.json   # 伴随包（10 条完整）
      modes_library_entries.json         # 可直接并入 data/modes_data.json modes 列表的 10 条
      id_mapping.tsv                     # 旧号 -> 新号 对照
    H-FXT-001/                           # 费孝通（legacy M341-M350），结构同上
    combined_library_entries.json        # 两件合并（20 条），供门禁试跑
    gate_evidence.txt                    # credibility_gate 试跑原始输出

## 2. 复刻动作（逐条可回溯）

| 动作 | 说明 |
|---|---|
| id 重编 | M211-M220 改为 M-CHB-001..010；M341-M350 改为 M-FXT-001..010。旧号全局不唯一（M341-M350 同时被费孝通 / 李维汉 / 罗荣桓块使用），必须重编 |
| figure_code | 沿用 H-CHB-001 / H-FXT-001（两码现持同名人物，无需换码） |
| related_modes | 块内引用全部改指新码；跨块引用 0 条（两件均无块外引用），未丢失信息 |
| category | 非标准类目映射到库内标准类目，原值保留在 category_raw：政治哲学思维->政治治理、政治经济学思维->经济商业、政治策略思维->战略决策、写作方法论 / 方法论思维 / 综合方法论->方法论通用、史学方法论->史学文献、社会结构分析->社会学、研究方法论->科学方法、文化认同->文艺审美、民族政策->政治治理、跨文化研究->跨文化治理 等。映射表属候选，待归并卡 / 船长确认 |
| verification | 统一 status=pending（method=legacy20-rev6-sample），evidence 明写「引文 / 出处未独立核验」；未伪造 verified |
| 字段补齐 | 仅做字段搬迁（definition / process / cases / applications / quote / 来源），未新增任何事实性内容 |

## 3. 位置与复核（t_a060cd41 第 2 次运行补记）

- 本目录已从仓库根 scratch/ 迁入 docs/scratch/（卡面要求评估产物只新增 docs/scratch）；内容未改，未入库、未提交、未同步发布仓。
- 第 2 次运行复核结论：20 条模式、20 个唯一模式编码；与库内 3132 个编码 0 碰撞、与全库文件编码 0 碰撞；图档、镜像、伴随包三处编号列表一致；模式互引 0 悬空；credibility_gate 在 hard-fail 模式下 exit 0（新增硬失败 0）。
- 口径说明：verify_findings 指向本目录子集会报 495 条新增，属基线比对噪声（其基准是全库 findings 清单），不作为样例证据；门禁输出中的 STALE 行同属该噪声。
- 遗留：合并清单中陈伯达有 1 条类目值（文化批判思维）不在映射表内，按原值保留。
