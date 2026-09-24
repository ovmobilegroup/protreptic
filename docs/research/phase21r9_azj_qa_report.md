# Phase21-R9 安子介（H-AZJ-001）重做链 独立 QA 验收报告

- 卡片：t_02007da8《[Phase21-R9 安子介重做] QA 独立验收（不信任自述）》（profile espinosa）
- 对象：AZJ-1/2/3 全链（sourcing 素材包 → landing 落盘 → 重建 → 合并入库 → 站链 → 镜像/推送）；上游衔接沈复链（t_a7d233f0）
- 日期：2026-09-24（CST）
- 核验脚本：`verify_azj_qa_espinosa.py`（随件；独立实现，不引用被验收方脚本结论）
- 结论：**通过（PASS）**。闭合前终跑 **61 PASS / 0 FAIL / 6 INFO**，rc=0。
- 证据：`docs/research/phase21r9_azj_qa_evidence.json` / `.txt`（同批 61 项明细，逐项可复核）

## 0 方法（不信任自述）

1. 判据全部取自原始事实面：git 对象（`rev-parse`/`cat-file`/blob sha）、文件实算（sha256/bytes）、数据库（sqlite 只读）、远端实测（`git ls-remote`、`raw.githubusercontent.com`）。
2. 重建复现：从合并前备份 `data/backup_merge_H-AZJ-001_20260924_092502/` 按 entries 重放写盘，与卡面 after 字节级比对（D04）。
3. 链式对账：以兄弟卡（沈复）提交面为中继，验证 before/after 交接与"末次写者"口径（D05/D10）。
4. 站链复跑：隔离目录重跑 `tools/export_static_site.py`（1358 产物逐字节比对，E05）+ `tools/pages_preflight.py --stage data`（E06）。
5. 检查器灵敏度自检：反向注入 7 类篡改（编号/引文/前缀/位置/块位移/图档码/计数）全部被捕获（H01 7/7）。
6. QA 期间修正了自身判据的 5 处实现缺陷（场景面链式口径、domain 压缩规则复刻、sha 前缀长度、figure tags 口径、远端前移鲁棒性），修正后终跑 0 FAIL。上述属判据实现问题，如实登记，非被验收对象缺陷。

## 1 逐项结论总表

| 组 | 面 | 结论 |
|---|---|---|
| A | 输入链（素材包/见证/落盘包/数据件 == git 提交版本） | 6/6 PASS |
| B | +10 条逐条核对（内容/来源/编号 vs figure/三面/素材包/见证） | 11/11 PASS + 1 INFO |
| C | 图档 figure / 顶层块 / 注册面（code_maps、figure_names） | 9/9 PASS |
| D | 合并算术与纯追加（备份/重建复现/链式口径） | 11/11 PASS |
| E | 站链（重算/复跑/隔离）与 parity | 9/9 PASS + 3 INFO |
| F | 推送与镜像实证（ls-remote / PB tree / raw） | 10/10 PASS + 1 INFO |
| G | 边界抽查（旧假件零残留 / 未动他人物 / 禁用面） | 4/4 PASS + 1 INFO |
| H | 反向注入自检（检查器灵敏度） | 1/1 PASS |
| 合计 | | **61 PASS / 0 FAIL / 6 INFO** |

## 2 关键实证摘录

### 2.1 +10 条（B 组）
- 编号/顺序/优先级/legacy 空/归属：M-AZJ-001~010、priority 1..10、figure_code=H-AZJ-001（10/10）。
- 同体：主库条目 == data/figures/H-AZJ-001.json == figure_modes == individuals_modes == landing 两面（逐条有序，10/10）。
- 来源-引文：key_quote_zh 与素材包 quotes 逐字一致 10/10 且每条见证文本命中 10/10。
- 来源-指向：source_chapter 含「AZJ-1 素材包」+ 本条码 + 引文见证在内，所引编号均在册（10/10）。
- 类目：category ∈ 标准 18 类；category_raw == 素材包 §二 主题域行（md 为准、去空格）（10/10；另见 §3 F1 口径差 1 项）。
- 命名：name_zh == 素材包名主干，全名在 id_mapping.tsv（10/10）。
- 内容非空：中英定义/流程/案例/现代应用齐（10/10）。
- 禁用标记：19 项旧载荷（H-AZJ-345 语料）在本 10 条零出现（10/10）。
- 引号片段「」/『』100 处（唯一 74）全部可回溯素材包/见证（miss 0）。
- 全库 M-AZJ 恰 10 条；条目 related_modes 引用全部可解析。

### 2.2 合并链（D 组）
- 备份 == before == git 5a657b81^（六件，6/6）；现行工作区 == git HEAD 提交版本（6/6）。
- 重建复现：before + entries 重放出的三写件 sha+bytes 与卡面 after 完全一致（modes_data / code_maps / figure_names 全 true）。
- 纯追加：现行前 3291 条与备份逐对象全等；AZJ 10 条落于 [3291:3301] 且逐字 == entries；尾部 10 条 = 兄弟卡 M-SHF-001~010。
- 场景三件零写入（before==after==兄弟 before）；兄弟卡 union_guard M-AZJ 10→10 守恒。
- 序列化口径：三写件现行均无尾换行（cm/fn 由前态有尾换行统一，见 §3 F4 注记）。

### 2.3 站链与 parity（E 组）
- meta.counts 重算一致：figures=1027 / published=3241 / by-figure=320 / 隔离 60 / 去重 3301 / raw 3311 / 空码剔除 10。
- 四态计数一致：published verified 949 / suspect 35 / unverifiable 340 / pending 1917。
- 门面口径一致：siteCounts.ts / docs（index.md、figure_library.md）/ PWA manifest×2 / daily index（3241 x 320）。
- by-figure 分片 H-AZJ-001：10 条、摘要面 == 主库、domain 压缩 == export 清洗规则（首段标签，>30 字符或含句读回落 category 短标签）。
- export 隔离复跑：1358 产物逐字节 == web/public/data（0 失配）；preflight --stage data exit 0。
- parity：本链残留 0（现行 53 条差异全部为他链在制）；两仓点试 13 件（数据件/门面/报告/脚本）逐字节一致。
- DB：figures 行数 1027 == meta；H-AZJ-001 0 行（DB 非合并卡链条面，先例一致，见 §3 F3）。

### 2.4 推送与镜像（F 组）
- 发布仓 AZJ 链提交链完整：fe250fd → 78246d4 → e6d133c（^ 逐级相符，三提交题均为 AZJ 镜像）。
- e6d133c ∈ 发布仓谱系 ∧ ∈ origin/main 谱系（merge-base 实证）；收口时点 ls-remote == e6d133c（链回执 + 本卡前轮实测），当晚他卡续推至 2397eeec（见 §3 F5 时移登记）。
- PB 树 91 件 azj/anzijie 命名文件全部逐字节 == 工作仓；e6d133c 树 blob 抽验 8 件零失配。
- raw.githubusercontent.com 抽验 5 件：http=200 且逐字节 SAME（远端发布面）。
- 回执提交 602a5d47 / a96302f1 / 5ce7f6ad / 8c486442 均在库。

### 2.5 边界（G 组）
- H-AZJ-345 live 面 0 命中（主库六件/站点数据/dist/DB/tools json/docs figures 全空；544 命中全为豁免/登记/快照类，见证据 G02 分类）。
- R8 清档基线对比：零移除、新增 21 件全部为受控登记件、无 live 面新增。
- 禁用面（19 项标记于 figure+条目+顶层块+code_maps）零出现。
- 链提交面：602a5d47 / a96302f1 文件清单全部 AZJ 链文件，零夹带其他人物/他链。

## 3 发现与分级

### F1【口径差·登记·不阻断】M-AZJ-009 category_raw 与素材包 JSON theme 字段不一致
- 事实：素材包 §二 md 主题域行 = 「教育资助 / 学术激励 / 学界与业界互动」（3 段）；素材包 JSON `theme` = 「教育资助/学术激励」（2 段）；落库 `category_raw` = 3 段（去空格）。
- 判定：口径差——素材包 md/json 内部不一致；落库取 md 口径、与 `category_mapping.tsv` 一致，无虚构、无越界；其余 9/10 条 md/JSON/落库三方一致。
- 建议：后续 sourcing 勘误统一素材包 JSON theme 字段（或注明 md 为准）。不影响本次验收。

### F2【登记】PB `web/public/data/**` 非 parity 镜像面
- PB by-figure 目录为旧代次快照（318 件 vs 工作仓 320 件；无 AZJ/SHF 分片）；parity EXCLUDE_RULES 明确排除（构建产物，部署侧再生成）。非本链承诺面，先例一致。

### F3【登记】`api/protreptic.db` 无合并卡模式（H-AZJ-001 0 行）
- DB 非合并卡链条面（R8 先例：M-LUORQ/M-WX 亦 0）；注册面 = code_maps + figure_names + data/figures 分片。

### F4【口径注记】三写件序列化尾换行
- modes_data 保持"无尾换行"；code_maps/figure_names 由前态"有尾换行"→ after"无尾换行"，与 modes_data 口径统一。属序列化口径注记，非缺陷（D11）。

### F5【时移登记】远端/发布仓在他卡推送后前移
- 收口时点 ls-remote == e6d133c（链回执与本卡前轮实测）；2026-09-24 当晚由他卡（t_83e0d68d 回执补记、shenfu 链）续推至 2397eeec；merge-base 实证 e6d133c 在谱系内。
- 未发现真差异（0 项）：+10 条内容/来源/编号、合并算术、站链口径、镜像/推送面全部实证一致。

## 4 复现（证据可复核）

```
cd /opt/data/workspace/Protreptic
python3 verify_azj_qa_espinosa.py     # 终跑预期：61 PASS / 0 FAIL / 6 INFO，rc=0
# 可选：AZJQA_REBUILD=<station rebuild 目录> 指向站链隔离复跑产物
# 复跑会重写 docs/research/phase21r9_azj_qa_evidence.json/.txt
#   （他链在制差异计数随环境波动，属预期；语义面断言不受影响）
python3 tools/check_repo_parity.py --json   # 复核 parity 计数
```

## 5 回执（receipts）

- 工作仓闭合提交：<A>（本报告 + 证据 json/txt + 核验脚本，4 件）
- 发布仓镜像：<B>；push <range1>；ls-remote 复核
- 闭合后复核跑：61 PASS / 0 FAIL / 6 INFO rc=0 → 证据刷新；补记提交 <C>；镜像 <D>；push <range2>

（本节随镜像后补记更新；最终完成回执见卡片 t_02007da8 completion。）
