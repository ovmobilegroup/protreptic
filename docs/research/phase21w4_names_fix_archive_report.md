# Phase21-W4 名录修复·全链档案报告（卡 t_616e4991；W4 链尾·文档归档）

- 卡：t_616e4991（pigafetta）｜日期：2026-09-24｜角色：W4 链尾·文档归档（九节档案 + 登记链）
- 工作仓：/opt/data/workspace/Protreptic（master，本地面；工作仓不设 push 义务）｜发布仓：/opt/data/release/Protreptic-publish（origin/main 面）
- 上游钉：W4 QA 窗口 40320e37..2de84904（10 提交）；fix2 终态 2de84904；B-a 终版 4e78ace6
- 生成器：build_w4_names_fix_archive.py（幂等；--check 复跑校验）｜独立验收：verify_w4_names_fix_archive.py

## 一、概述

本档将 Phase21 W4「名录修复」全链（研究 t_24b92f58 -> 清单 t_10a42b2a -> 执行 t_536073f4 / 清档 t_ee203180 -> 补正 t_33240de8 -> 独立 QA t_8bad8d98 -> 补正(B-a) t_def07a84）的 commit 链、回执与逐码终值装配为九节档案；并按船长 09-24 追加令完成 R-a 6 件、QA 2 件与根级 QA 见证器的发布仓镜像收口（byte-exact + push + parity 复核）。

- 链级结论（引用上游报告 + 本卡实测）：21 码终值全链命中；4 个清档码 + RW-KAG-1..27 全链 0 残留；JP/UZ 重键完整；QA 终判 PASS（v3 复跑 140 断言 / 0 FAIL / 45 DRIFT 登记；详见第六节）。
- 本卡四件产物：本报告（九节）/ 幂等生成器 build_w4_names_fix_archive.py / 独立验收脚本 verify_w4_names_fix_archive.py / 证据 JSON docs/research/phase21w4_names_fix_archive_evidence.json。
- 镜像面：R-a 6 件 + QA 2 件 + 根见证器 = 9 件 byte-exact 入发布仓；本档报告/证据/验收脚本随镜像。
- 本卡回执（stage=v3（回执终版））：v1 提交 af084d5f（工作仓归档主体：九节生成器 + 独立验收脚本 + 报告 v1） / 发布仓 e75dc78（发布仓镜像 11 件：R-a 6 + QA 2 + 根见证器 + 报告 v1 + 验收脚本；byte-exact） / push ok（origin/main 对齐 e75dc78cf213f4da18bafaedca93aa717b4618b2；ls-remote + fetch 对象级复核 REMOTE==LOCAL）；v2 终版见第四.7节。

## 二、背景

- 触发：Phase21 W4 名录核查发现 16 个 H-* 码场景侧空名 + 异常码族（SG/MY 大小写混写残件、JP/UZ 大小写重键、RW-KAG 模板废件）。
- 分类矩阵：docs/research/phase21r8_w4_names_recon.md/.json（t_24b92f58，零库写）。
- 处置清单 + 干跑：docs/research/phase21w4_fix_manifest.md/.json（t_10a42b2a）——受影响码 50；干跑 figures 1057 -> 1028；编辑清单 24 项；备份模板 11+60 件。
- 执行拆分：fix 卡（16 H-* 回填 + SG/MY 归一 + JP/UZ 重键 + RW-KAG-001 + G 类）与清档卡（RW-KAG-1..27）分列，单写者串行。
- 链上两次补正：t_33240de8（R2 zh 扩展位 4 处，船长核验发现原声称未落盘后补正）与 t_def07a84（B-a：scenarios_zh en 侧 4 扩展位，船长 07:45 裁定采纳）。
- 裁定：R1-R12 为船长目标态（清单卡正文），逐条执行映射见第四.5节。

## 三、方法

- 事实来源与口径：一律取 git 对象（短号解析全号/日期/题名）、文件字节（sha256）、工具实跑输出；不采信卡面或报告自述。
- 镜像口径：byte-exact（两仓 sha256 相等判定）；push 后远端复验（ls-remote 对齐 + raw 抽验）。
- 生成口径：本报告由 build_w4_names_fix_archive.py 逐字段装配（生成时实测），幂等可复跑（--check 归一生成时点 HEAD 观测行后逐字节比对，打印 IDEMPOTENT）。
- 验收口径：verify_w4_names_fix_archive.py 为第二实现（不 import 生成器），独立读取本报告、两仓文件、git 对象与上游数据逐项断言；含反向注入自检。
- 站点展示层说明（卡 ③）：本链为文档/数据修复面，不新增页面、路由或文案；两仓一致性以 byte-exact 镜像复核替代（第五.1/5.2节）。

## 四、执行（登记链）

### 4.1 卡片链（8 卡）

| 卡 | 角色 | 执行 | 状态 | 产物 | 备注 |
|---|---|---|---|---|---|
| t_24b92f58 | 研究·矩阵 | serrano | done | docs/research/phase21r8_w4_names_recon.md/.json | 16 H-* 空名 + 异常码族分类矩阵（零库写） |
| t_10a42b2a | 清单·干跑 | serrano | done | docs/research/phase21w4_fix_manifest.md/.json | 处置执行清单 + 干跑影响面 + 待船长复核 6 项（零库写） |
| t_536073f4 | 执行·fix | elcano | done | docs/research/phase21w4_fix_report.md + fix_evidence.json | 16 H-* 回填 + SG/MY 归一 + JP/UZ 重键 + RW-KAG-001 + G类（单写者） |
| t_ee203180 | 执行·清档 | elcano | done | docs/research/phase21w4_rwkag_clear_report.md/.json + evidence + _archive/RW-KAG_1-27_archive.json | RW-KAG-1..27 模板废件全链清档（先备份后清除） |
| t_33240de8 | 补正·R2 zh 扩展位 | elcano | done | docs/research/phase21w4_fix2_report.md/.json | scenarios_zh.json H-LXN-001 4 处 毛先念->李先念（4x2B 最小 diff） |
| t_8bad8d98 | 独立 QA（第二实现） | espinosa | done | docs/qa/phase21w4_qa_report.md + qa_evidence.json + verify_phase21w4_qa_espinosa.py | 终跑 140 断言 / 0 FAIL / 45 DRIFT 登记（v3） |
| t_def07a84 | 补正·B-a en 扩展位 | elcano | done | docs/research/phase21w4_fix3_report.md/.json + fix3_evidence.json | scenarios_zh.json H-LXN-001 en 侧 4 处 Mao Xiannian->Li Xiannian |
| t_616e4991 | 文档归档（本卡） | pigafetta | running | 本档四件（报告/生成器/验收脚本/证据） | 九节档案 + 登记链 + R-a 6 与 QA 2 件镜像收口 + parity 复核 |

本档另登记 W6 扫描卡 t_51db608d（serrano；phase21w6_marker_scan.md/.json 作者，R-a 面之一，随 1de660cf 入库）。

### 4.2 工作仓提交登记（19 笔；含 R-a 携带入库 1 笔）

| 仓 | commit | 全号 | 日期 | 卡 | 题名 | 本档注 |
|---|---|---|---|---|---|---|
| ws | `e7be5cc6` | `e7be5cc6aec80d998887d3c62cfac05d14d42edd` | 09-24 06:15 | t_536073f4 | Phase21 W4 t_536073f4 名录修复：16 H-* 回填 + SG/MY 清档 + JP/UZ 重键 + RW-KAG-001；21 码终值全链实测（figures 1054/sitemap 1386） | 名录修复主体（16 H-* 回填 + SG/MY 清档 + JP/UZ 重键 + RW-KAG-001；21 码终值全链实测） |
| ws | `8ca52c04` | `8ca52c046548cdf3d55e217b229731232f0b5e77` | 09-24 06:16 | t_536073f4 | Phase21 W4 t_536073f4 报告回执补记（v2）：工作仓 e7be5cc6 + 镜像 da1e9bc + push + raw 4/4 校验 | 报告回执补记（v2） |
| ws | `9ed628e8` | `9ed628e8412e1aa104d5cf623d6b66378447fa46` | 09-24 06:17 | t_536073f4 | Phase21 W4 t_536073f4 回执终版（v3）：报告 v2 镜像 8ca52c04 -> faccfbe + raw 校验 | 回执终版（v3） |
| ws | `37545ac7` | `37545ac770d6b0d3c0be4ffb40c9a404b47f70b1` | 09-24 06:18 | t_536073f4 | Phase21 W4 t_536073f4 收尾（v4）：备份清单标准化 sha256sum -c 11/11 + 发布数据面终检 1410 文件全等/残件 0 | 收尾（v4）：备份清单标准化 + 发布数据面终检 |
| ws | `33762c4e` | `33762c4e90dff6335009f8667c13b4f669ca74bc` | 09-24 06:48 | t_ee203180 | Phase21 W4 t_ee203180 RW-KAG-1..27 模板废件全链清档：删源 27x2 + code_maps 27 键 + 草稿/根双胞归档移出（R100）+ 重建归零（figures 1027 / routes 1358 / sitemap 1359 / unified 1342）+ 锚点实测 + 备份 89 件 + 归档/见证器/报告 | RW-KAG-1..27 全链清档主体（重建归零 figures 1027） |
| ws | `4aa62574` | `4aa625740b0291eb6dae2839850cbe92d5d27f0f` | 09-24 06:52 | t_ee203180 | Phase21 W4 t_ee203180 报告回执补记（v2）：工作仓 33762c4e + 发布仓 74c5522 + push e5c111a..74c5522 + parity 2388/2388 + raw 4/4 + 见证器 21/21 全量 | 报告回执补记（v2） |
| ws | `8a0ac56d` | `8a0ac56db7e961b39c98035197bc5d5676fdee2e` | 09-24 06:52 | t_ee203180 | Phase21 W4 t_ee203180 回执终版（v3）：v2=4aa62574 / 镜像=ba3b1fa / raw 3/3 OK @ba3b1fa | 回执终版（v3） |
| ws | `00bc34a2` | `00bc34a275ad35ef8c317a8f84781dc95e39fada` | 09-24 07:12 | t_33240de8 | Phase21 W4 t_33240de8 补正·R2 zh 扩展位落盘：scenarios_zh H-LXN-001 4 处 毛先念→李先念（4x2B 最小 diff/同长 2981559B）+ 全链 18 步复跑零差异 + 报告补注 + fix2 报告/证据 + 备份 5 件 + 见证器 | R2 zh 扩展位落盘主体（4x2B 最小 diff） |
| ws | `489b72c3` | `489b72c3852c6c558d8568c28fe1e4ca0a214fb6` | 09-24 07:13 | t_33240de8 | Phase21 W4 t_33240de8 报告回执补记（v2）：工作仓 00bc34a2 + 发布仓 0517b38 + push 332188d..0517b38 + parity 2395/2395 + raw 4/4 + 见证器 26/26 全量 | 报告回执补记（v2） |
| ws | `2de84904` | `2de84904bbb26ab2db0b4171f623d036bbb3ed36` | 09-24 07:14 | t_33240de8 | Phase21 W4 t_33240de8 回执终版（v3）：v2=489b72c3 / 镜像=8e4d3e6 / raw 4/4 OK @8e4d3e6 | 回执终版（v3）；W4 QA 窗口 HEAD 钉（fix2 终态） |
| ws | `17bfa994` | `17bfa9949ce7817a50a2432f969c031f0717ffc5` | 09-24 07:53 | t_8bad8d98 | Phase21 W4 t_8bad8d98 独立 QA 产物：报告+证据+见证器（全量 137 断言 0 FAIL；含 R2 zh 补正链复核/B-a 登记/未注册精度差根因） | QA 产物入库 h1（报告+证据+见证器） |
| ws | `5891cecc` | `5891ceccf2aa3ced6013c30ad0cc13c976a74c81` | 09-24 08:05 | t_8bad8d98 | Phase21 W4 t_8bad8d98 QA 回执补记（v2）：提交后终跑 137/0 全绿 + 证据/日志更新 + 报告 §八/注记E 实测口径 | QA 回执补记 h2（v2） |
| ws | `9c1fd3dd` | `9c1fd3ddf72806e2acf36d246f110c1dd299d563` | 09-24 08:05 | t_8bad8d98 | Phase21 W4 t_8bad8d98 QA 见证器 v2 入库：E 段 QA 提交容差（commits/diff-score 显式断言）+ 报告 §八 h3 补记 | QA 见证器 v2 入库 h3 |
| ws | `c1fe9024` | `c1fe9024fbe935a29b95116861c4ad22d35348a4` | 09-24 10:25 | t_8bad8d98 | Phase21 W4 t_8bad8d98 QA 见证器 v3 入库：板面并发漂移归因（提交/文件/窗口三级，实时判定）＋报告 §九/§十＋证据/日志终跑（140/0/44 登记，HEAD=8c486442） | QA 见证器 v3 入库 h4（板面并发漂移归因） |
| ws | `8d461a2e` | `8d461a2ea5dbbc446240dc13d981f68fde013a0d` | 09-24 10:30 | t_8bad8d98 | Phase21 W4 t_8bad8d98 QA 回执补记（v3）：h4=c1fe9024 入库 + 提交后终跑 140/0/45（274s，n=33=10 W4+4 QA+19 外来）＋证据同步 | QA 回执补记 h5（v3）：提交后终跑 140/0/45 |
| ws | `3f102ee1` | `3f102ee1d6014b2bd22e769db884b8ba1a1c538c` | 09-24 11:10 | t_def07a84 | Phase21 W4 补正-B-a: scenarios_zh.json H-LXN-001 en 侧 4 扩展位 Mao Xiannian->Li Xiannian 落盘 (真字节窗口 645917/646781/648210/651925; 2981559->2981555B; sha 8b218e71->e6777e7a) + fix2 报告补记 + fix3 报告/证据 + 备份 4/4 + 见证器 (34 PASS/0 FAIL) | B-a en 扩展位落盘主体（4 字段真字节窗口；2981559->2981555 B） |
| ws | `a8ec9afe` | `a8ec9afef597bbbbdff7752ed55ec655f9a9425d` | 09-24 11:12 | t_def07a84 | Phase21 W4 t_def07a84 回执补记 (v2): fix3 报告第7节回执 (工作仓 3f102ee1 / 镜像 0dda13a / push 78bac29..0dda13a / raw 6-6 / 见证器全量 39-0 / parity 42 条全归因) + 报告 json 与证据 receipts 同步 | 回执补记（v2） |
| ws | `4e78ace6` | `4e78ace62a3bbb243b13226c64f34fd3307261cf` | 09-24 11:13 | t_def07a84 | Phase21 W4 t_def07a84 回执终版 (v3): fix3 报告 第7节 回执终版 (v2 工作仓 a8ec9afe / 镜像 3cb64c3 / push 0dda13a..3cb64c3 / 远端一致) + json receipts v3 链同步 | 回执终版（v3） |
| ws | `1de660cf` | `1de660cfd5964f72313f3a4a3f38670c5e745240` | 09-24 02:14 | t_3669eb4a | [Phase21-R8 clear] H-AZJ-345 residue removal (t_3669eb4a) | R-a 6 件（recon/manifest/marker_scan 各 md+json）随 R8 clear 提交入库（工作仓侧） |

### 4.3 发布仓提交登记（13 笔）

| 仓 | commit | 全号 | 日期 | 卡 | 题名 | 本档注 |
|---|---|---|---|---|---|---|
| pb | `da1e9bc` | `da1e9bc9634f7c0b3a250241de4d21e1308fb72f` | 09-24 06:16 | t_536073f4 | 镜像: Phase21 W4 t_536073f4 名录修复（16 H-* 回填 + SG/MY 清档 + JP/UZ 重键 + RW-KAG-001）；21 码终值全链实测（figures 1054/sitemap 1386） | 镜像 v1 |
| pb | `faccfbe` | `faccfbeaaa27a98b8cb9b33de123453d50025452` | 09-24 06:16 | t_536073f4 | 镜像: Phase21 W4 t_536073f4 报告回执补记 v2（byte-exact，回执含 push da1e9bc + parity 2291/2291） | 镜像 v2 |
| pb | `7d6d1e9` | `7d6d1e9e671b8355f6288ca5c356d978fe6f9e56` | 09-24 06:17 | t_536073f4 | 镜像: Phase21 W4 t_536073f4 回执终版 v3（byte-exact） | 镜像 v3 |
| pb | `e5c111a` | `e5c111a9d36bfd6b1b806dab21b16f4ee85a9863` | 09-24 06:18 | t_536073f4 | 镜像: Phase21 W4 t_536073f4 收尾 v4（备份清单标准化 + 发布数据面终检，byte-exact） | 镜像 v4（收尾） |
| pb | `74c5522` | `74c5522ba106c5c7e6e4bf7f3fa60482aff63188` | 09-24 06:50 | t_ee203180 | 镜像: Phase21 W4 t_ee203180 RW-KAG-1..27 清档（16 件 byte-exact + 备份 93 件 + 草稿→备份归档 27 + intl 独有件移除 27 + web/dist 对齐 + 报告/证据/归档 4 件） | 镜像 v1（16 件 + 备份 93 + intl 27 + web/dist 对齐） |
| pb | `ba3b1fa` | `ba3b1fa57fc0a0631ca0a30c94cbc735826765f3` | 09-24 06:52 | t_ee203180 | 镜像: Phase21 W4 t_ee203180 报告回执补记 v2（报告对 + 证据回执区同步，byte-exact 3/3） | 镜像 v2 |
| pb | `332188d` | `332188d9ec4812711eb966be611b6ce0f812d91a` | 09-24 06:53 | t_ee203180 | 镜像: Phase21 W4 t_ee203180 回执终版 v3（byte-exact 3/3） | 镜像 v3 |
| pb | `0517b38` | `0517b387d21382307ecba168f88c6d78b542fa69` | 09-24 07:12 | t_33240de8 | 镜像: Phase21 W4 t_33240de8 R2 zh 扩展位落盘（scenarios_zh 4 处 毛先念→李先念 + 报告/证据/备份/见证器 byte-exact 10 件） | 镜像 v1（10 件 byte-exact） |
| pb | `8e4d3e6` | `8e4d3e676038a3f1888daaf8fd80d859e0d6e611` | 09-24 07:13 | t_33240de8 | 镜像: Phase21 W4 t_33240de8 回执补记（v2） | 镜像 v2 |
| pb | `c646f41` | `c646f41a5c4fc65027d403cf448c847fc4756060` | 09-24 07:14 | t_33240de8 | 镜像: Phase21 W4 t_33240de8 回执终版（v3） | 镜像 v3；QA 核验时点 origin/main |
| pb | `0dda13a` | `0dda13abc4f8f371139141a340fca5f411fdd548` | 09-24 11:10 | t_def07a84 | 镜像: Phase21 W4 补正-B-a (对齐工作仓 3f102ee1): scenarios_zh.json H-LXN-001 en 侧 4 扩展位 Mao Xiannian->Li Xiannian 落盘 + fix2 报告补记 + fix3 报告/证据/见证器 + 备份 4/4; 12 件 byte-exact | 镜像 v1（12 件 byte-exact） |
| pb | `3cb64c3` | `3cb64c3eb3333d52c5aff586b7187079eef6c5ee` | 09-24 11:12 | t_def07a84 | 镜像: t_def07a84 回执补记 v2 (对齐工作仓 HEAD): fix3 报告 第7节回执 + json/证据 receipts; 3 件 byte-exact | 镜像 v2 |
| pb | `d0c7306` | `d0c7306c5f23cfeaac039d07f6afea57a4bf7a31` | 09-24 11:13 | t_def07a84 | 镜像: t_def07a84 回执终版 v3 (对齐工作仓 4e78ace6): 3 件 byte-exact | 镜像 v3（B-a 面终版） |

- 本卡补镜像（v1/v2）见第四.7节回执；发布仓生成时点 HEAD=`d38953df890457064cf98da23c8eb624c0da4c65`。

### 4.4 逐码处置终表（16 H-* + 5 码族 + RW-KAG-1..27 = 48 码）

#### 4.4.1 16 个 H-*（R1 回填；H-LXN-001 含 R2 修正与 4 字段补正）

| 码 | zh 终值 | en 终值 | 处置 | 备注 |
|---|---|---|---|---|
| H-HYP-145 | 黄炎培 | Huang Yanpei | 回填 | scenarios_zh/en name（R1） |
| H-WYX-146 | 吴有训 | Wu Youxun | 回填 | R1 |
| H-WX-147 | 王选 | Wang Xuan | 回填 | R1 |
| H-YLP-148 | 袁隆平 | Yuan Longping | 回填 | R1 |
| H-SY-149 | 粟裕 | Su Yu | 回填 | R1 |
| H-XMQ-151 | 薛暮桥 | Xue Muqiao | 回填 | R1 |
| H-CY-159 | 陈毅 | Chen Yi | 回填 | R1 |
| H-LXN-347 | 李先念 | Li Xiannian | 回填 | R1 |
| H-LXN-001 | 李先念 | Li Xiannian | 回填+修正+补正 | R2 错名修正（毛先念/Mao Xiannian 全链 -> 李先念/Li Xiannian）；4 字段补正：zh name_zh/description_zh/reason_zh/case_zh（t_33240de8）、en name_en/description_en/reason_en/case_en（t_def07a84）；fix_report 第2.2节 补正注记 |
| H-IKD-160 | 伊本·赫勒敦 | Ibn Khaldun | 回填 | R1 |
| H-ISC-362 | 阿维森纳（伊本·西那） | Avicenna (Ibn Sina) | 回填 | R1 |
| H-GHZ-163 | 安萨里 | Al-Ghazali | 回填 | R1；译名冲突（加扎利）按裁留挂 Phase46-R |
| H-SUF-364 | 鲁米（贾拉勒丁·鲁米） | Rumi (Jalal al-Din Rumi) | 回填 | R1 |
| H-ZEL-001 | 周恩来 | Zhou Enlai | 回填 | R1 |
| H-HLG-001 | 华罗庚 | Hua Luogeng | 回填 | R1；person 型（走 /minds/ 路由与 sitemap 命中） |
| H-MZ-001 | 晏阳初 | Y. C. James Yen | 回填 | R1/R3；en 取证=data/figures/H-MZ-001.json style_name；figure_name=孟子 companion 保留现状（交 Phase46-R） |

#### 4.4.2 5 码族（SG / MY / JP / UZ / RW-KAG-001）

| 族 | 处置 | 裁定 | 说明 |
|---|---|---|---|
| SG | SG-LEE-001 保留+回填 李光耀 / Lee Kuan Yew；SG-Lee-001 全链清档 | R4 | 清档码：双源整条 + 草稿 + DB 行 + shard + 轻索引 + 统一索引 + 路由 + sitemap |
| MY | MY-MAH-001 保留+修正 马哈蒂尔（en 保持 Mahathir Mohamad）；MY-Mah-001 全链清档 | R5 | 同口径；en 名无变化（no-op，不产生 diff） |
| JP | JP-Sas-001 -> JP-SAS-001 重键+回填 西乡隆盛 / Saigō Takamori（en 取源剥副题）；旧码全链清 | R6 | 旧条目整条迁移不改内容；旧码全链 0 残留（含发布面） |
| UZ | UZ-Ulu-001 -> UZ-ULU-001 重键+回填 乌鲁格别克 / Ulugh Beg；旧码全链清 | R7 | 同 R6 口径 |
| RW-KAG-001 | 保留+回填 卡加梅 / Paul Kagame | R9 | 短名回填（scenarios_zh/en 双源） |

#### 4.4.3 RW-KAG-1..27（27 码，逐码清档）

| 码 | 处置 | 执行 | 备注 |
|---|---|---|---|
| RW-KAG-1 | 全链清档 | t_ee203180 | 双源整条 + 草稿 + 根双胞（归档移出）+ code_maps 键；备份 89 件 93/93；证据=rwkag_clear_report |
| RW-KAG-2 | 全链清档 | t_ee203180 | 双源整条 + 草稿 + 根双胞（归档移出）+ code_maps 键；备份 89 件 93/93；证据=rwkag_clear_report |
| RW-KAG-3 | 全链清档 | t_ee203180 | 双源整条 + 草稿 + 根双胞（归档移出）+ code_maps 键；备份 89 件 93/93；证据=rwkag_clear_report |
| RW-KAG-4 | 全链清档 | t_ee203180 | 双源整条 + 草稿 + 根双胞（归档移出）+ code_maps 键；备份 89 件 93/93；证据=rwkag_clear_report |
| RW-KAG-5 | 全链清档 | t_ee203180 | 双源整条 + 草稿 + 根双胞（归档移出）+ code_maps 键；备份 89 件 93/93；证据=rwkag_clear_report |
| RW-KAG-6 | 全链清档 | t_ee203180 | 双源整条 + 草稿 + 根双胞（归档移出）+ code_maps 键；备份 89 件 93/93；证据=rwkag_clear_report |
| RW-KAG-7 | 全链清档 | t_ee203180 | 双源整条 + 草稿 + 根双胞（归档移出）+ code_maps 键；备份 89 件 93/93；证据=rwkag_clear_report |
| RW-KAG-8 | 全链清档 | t_ee203180 | 双源整条 + 草稿 + 根双胞（归档移出）+ code_maps 键；备份 89 件 93/93；证据=rwkag_clear_report |
| RW-KAG-9 | 全链清档 | t_ee203180 | 双源整条 + 草稿 + 根双胞（归档移出）+ code_maps 键；备份 89 件 93/93；证据=rwkag_clear_report |
| RW-KAG-10 | 全链清档 | t_ee203180 | 双源整条 + 草稿 + 根双胞（归档移出）+ code_maps 键；备份 89 件 93/93；证据=rwkag_clear_report |
| RW-KAG-11 | 全链清档 | t_ee203180 | 双源整条 + 草稿 + 根双胞（归档移出）+ code_maps 键；备份 89 件 93/93；证据=rwkag_clear_report |
| RW-KAG-12 | 全链清档 | t_ee203180 | 双源整条 + 草稿 + 根双胞（归档移出）+ code_maps 键；备份 89 件 93/93；证据=rwkag_clear_report |
| RW-KAG-13 | 全链清档 | t_ee203180 | 双源整条 + 草稿 + 根双胞（归档移出）+ code_maps 键；备份 89 件 93/93；证据=rwkag_clear_report |
| RW-KAG-14 | 全链清档 | t_ee203180 | 双源整条 + 草稿 + 根双胞（归档移出）+ code_maps 键；备份 89 件 93/93；证据=rwkag_clear_report |
| RW-KAG-15 | 全链清档 | t_ee203180 | 双源整条 + 草稿 + 根双胞（归档移出）+ code_maps 键；备份 89 件 93/93；证据=rwkag_clear_report |
| RW-KAG-16 | 全链清档 | t_ee203180 | 双源整条 + 草稿 + 根双胞（归档移出）+ code_maps 键；备份 89 件 93/93；证据=rwkag_clear_report |
| RW-KAG-17 | 全链清档 | t_ee203180 | 双源整条 + 草稿 + 根双胞（归档移出）+ code_maps 键；备份 89 件 93/93；证据=rwkag_clear_report |
| RW-KAG-18 | 全链清档 | t_ee203180 | 双源整条 + 草稿 + 根双胞（归档移出）+ code_maps 键；备份 89 件 93/93；证据=rwkag_clear_report |
| RW-KAG-19 | 全链清档 | t_ee203180 | 双源整条 + 草稿 + 根双胞（归档移出）+ code_maps 键；备份 89 件 93/93；证据=rwkag_clear_report |
| RW-KAG-20 | 全链清档 | t_ee203180 | 双源整条 + 草稿 + 根双胞（归档移出）+ code_maps 键；备份 89 件 93/93；证据=rwkag_clear_report |
| RW-KAG-21 | 全链清档 | t_ee203180 | 双源整条 + 草稿 + 根双胞（归档移出）+ code_maps 键；备份 89 件 93/93；证据=rwkag_clear_report |
| RW-KAG-22 | 全链清档 | t_ee203180 | 双源整条 + 草稿 + 根双胞（归档移出）+ code_maps 键；备份 89 件 93/93；证据=rwkag_clear_report |
| RW-KAG-23 | 全链清档 | t_ee203180 | 双源整条 + 草稿 + 根双胞（归档移出）+ code_maps 键；备份 89 件 93/93；证据=rwkag_clear_report |
| RW-KAG-24 | 全链清档 | t_ee203180 | 双源整条 + 草稿 + 根双胞（归档移出）+ code_maps 键；备份 89 件 93/93；证据=rwkag_clear_report |
| RW-KAG-25 | 全链清档 | t_ee203180 | 双源整条 + 草稿 + 根双胞（归档移出）+ code_maps 键；备份 89 件 93/93；证据=rwkag_clear_report |
| RW-KAG-26 | 全链清档 | t_ee203180 | 双源整条 + 草稿 + 根双胞（归档移出）+ code_maps 键；备份 89 件 93/93；证据=rwkag_clear_report |
| RW-KAG-27 | 全链清档 | t_ee203180 | 双源整条 + 草稿 + 根双胞（归档移出）+ code_maps 键；备份 89 件 93/93；证据=rwkag_clear_report |

### 4.5 裁定引用 R1-R12（目标态 -> 执行/现状）

| 裁定 | 目标态 | 执行/现状 |
|---|---|---|
| R1 | 16 个 H-* 全回填 name 值（scenarios_zh/en 双文件） | t_536073f4 执行：16/16 实测命中；口径依 R8（仅新增 name 键）。 |
| R2 | H-LXN-001 连带修错名：毛先念/Mao Xiannian -> 李先念/Li Xiannian（tools/json/H-LXN-001.json + scenarios_en 同步） | t_536073f4 执行 8 字段（zh/en 各 4）；scenarios_zh 4 扩展位由 t_33240de8 补正落盘；scenarios_zh en 侧 4 扩展位由 t_def07a84 落盘（B-a）。 |
| R3 | H-MZ-001 归属=晏阳初（三源多数）；孟子伴随键与 phase20 墨子引用=保留现状+登记冲突，交 Phase46-R；本轮不删不弃不移动 | 执行保留；QA 复核 R1/R3 一致（en 取证 style_name=Y. C. James Yen）。 |
| R4 | SG：保留 SG-LEE-001 并回填（李光耀/Lee Kuan Yew）；SG-Lee-001=混写残件 -> 全链清档（先备份后清除） | 执行：回填命中 + 残件全链 0 残留（含发布面）。 |
| R5 | MY：保留 MY-MAH-001 并修正（中文位错位 -> 马哈蒂尔；en=Mahathir Mohamad）；MY-Mah-001 -> 全链清档（先备份） | 执行：同上。 |
| R6 | JP：JP-Sas-001 -> 重键 JP-SAS-001 + 回填（西乡隆盛；en 取源剥副题）；旧码全链清（先备份；references 同提交更新） | 执行：重键完整、旧码 0 残留、引用扫描 0 存活。 |
| R7 | UZ：UZ-Ulu-001 -> 重键 UZ-ULU-001 + 回填（乌鲁格别克；同 R6 口径） | 执行：同上。 |
| R8 | 短名口径：en 取证据串冒号前短名；zh 用裁定表值；长「人名:题名」形本轮不采用（登记为可选后续项） | 执行：仅新增/设置 name 键；既有 name_zh/name_en 长串保留不动。 |
| R9 | RW-KAG-001：回填（卡加梅/Paul Kagame） | 执行：scenarios_zh/en 双源短名回填命中。 |
| R10 | RW-KAG-1..27：全链清档（下游独立卡 t_ee203180 执行；清单卡只出清单+扫描+备份模板） | t_ee203180 执行：删源 27x2 + code_maps 27 键 + 草稿/根双胞归档移出 + 重建归零 figures 1027/sitemap 1359；备份 89 件 93/93。 |
| R11 | G类：修 H-LXN-001.json 错名；两异常文件名=与同名正常文件字节比对后处置（重复件->备份后删除；非重复->规范重命名） | 错名已修（t_536073f4，8 字段）；两异常项实测为空目录（非文件）-> 两分支均无适用对象；QA 实测两目录已不在（本档补记账务，见第七节）。 |
| R12 | 本轮不做（登记待用户口径）：F 类 547 场景侧回填、装载器键回退（name_zh fallback）、多码深度去重（周恩来x5 等） | 登记项（不在本链范围）；后续口径由用户裁定。 |

### 4.6 本卡动作与镜像集

- [R-a] docs/research/phase21r8_w4_names_recon.md（t_24b92f58；研究矩阵 md）：byte-exact 等同。
- [R-a] docs/research/phase21r8_w4_names_recon.json（t_24b92f58；研究矩阵 json）：byte-exact 等同。
- [R-a] docs/research/phase21w4_fix_manifest.md（t_10a42b2a；处置清单 md）：byte-exact 等同。
- [R-a] docs/research/phase21w4_fix_manifest.json（t_10a42b2a；处置清单 json）：byte-exact 等同。
- [R-a] docs/research/phase21w6_marker_scan.md（t_51db608d；W6 标记扫描 md）：byte-exact 等同。
- [R-a] docs/research/phase21w6_marker_scan.json（t_51db608d；W6 标记扫描 json）：byte-exact 等同。
- [QA] docs/qa/phase21w4_qa_report.md（t_8bad8d98；QA 报告（船长 10:58 补镜像令））：byte-exact 等同。
- [QA] docs/qa/phase21w4_qa_evidence.json（t_8bad8d98；QA 证据 JSON）：byte-exact 等同。
- [QA-见证器] verify_phase21w4_qa_espinosa.py（t_8bad8d98；根级 QA 见证器（v3，可复跑））：byte-exact 等同。
- [本档] docs/research/phase21w4_names_fix_archive_report.md（九节档案（本档主体）；随镜像）。
- [本档] docs/research/phase21w4_names_fix_archive_evidence.json（验收证据 JSON（由 verify_w4_names_fix_archive.py 生成）；随镜像）。
- [本档] verify_w4_names_fix_archive.py（独立验收脚本（第二实现；根级）；随镜像）。
- [本档] build_w4_names_fix_archive.py（幂等生成器（根级）；仅工作仓面（按先例））。
- 站点展示层：不涉及（无页面/路由/文案新增）；两仓一致性以镜像 byte-exact 复核替代（第五.1/5.2节）。

### 4.7 提交/镜像/push 回执（本卡）

- stage: v3（回执终版）
- ws_commit_v1: af084d5f（工作仓归档主体：九节生成器 + 独立验收脚本 + 报告 v1）
- pb_commit_v1: e75dc78（发布仓镜像 11 件：R-a 6 + QA 2 + 根见证器 + 报告 v1 + 验收脚本；byte-exact）
- push_v1: ok（origin/main 对齐 e75dc78cf213f4da18bafaedca93aa717b4618b2；ls-remote + fetch 对象级复核 REMOTE==LOCAL）
- ws_commit_v2: a20e4ade（报告 v2 + 验收脚本 evidence 门控）
- pb_commit_v2: 398cd8ce（报告 v2 + 验收脚本 2 件 byte-exact）
- push_v2: ok（origin/main 对齐 398cd8cea260af6a5716e9f76e201d1c44e1ba13；fetch 对象级复核 REMOTE==LOCAL）
- remote_main: （回执终版 v3 与证据提交后对齐；终态 sha 见卡面完成 metadata）
- remote_raw: fetch 对象级 REMOTE==LOCAL（v1/v2 两次 push 复核通过；v3/证据 push 同式复核）
- parity_final: diff 41 项：W4 归属（R-a 6 + QA 2）已归零、only_publish=0；归因=W8b1 在制 29 / 源链接链 4 / 审计链 3 / 生成物 3 / W10 债务 2（见 scratch/w4arch/parity_after.json）
- verify_result: ALL PASS 0 FAIL（A-E 分段全 0；含 5/5 反向注入自检）；断注明细见证据 JSON
- report_sha_v1: 34aa2565aaeb5416（报告 v1 前 16）
- report_sha_v2: d2e7e0fd019e996b（报告 v2 前 16）
- ws_commit_v3: （本次回执终版提交；sha 见卡面完成 metadata）
- pb_commit_v3: （回执终版镜像提交；sha 见卡面完成 metadata）
- push_v3: （回执终版 push 复核见卡面完成 metadata）
- 注：回执字段于 v1 提交后回填、v2 回执终版定稿；终版另见卡面完成 metadata。

## 五、证据

### 5.1 镜像集 9 件：双仓 sha256 与判定（生成时点）

| 文件 | 类别 | 工作仓 sha256(前16) | 发布仓 sha256(前16) | 判定 |
|---|---|---|---|---|
| docs/research/phase21r8_w4_names_recon.md | R-a | 1e66897bf33b90c6 | 1e66897bf33b90c6 | 等于（byte-exact） |
| docs/research/phase21r8_w4_names_recon.json | R-a | 54fe78f27e473927 | 54fe78f27e473927 | 等于（byte-exact） |
| docs/research/phase21w4_fix_manifest.md | R-a | 1886f0bfae22986d | 1886f0bfae22986d | 等于（byte-exact） |
| docs/research/phase21w4_fix_manifest.json | R-a | c6fb3d908517b6fd | c6fb3d908517b6fd | 等于（byte-exact） |
| docs/research/phase21w6_marker_scan.md | R-a | ab3c08915dd44eec | ab3c08915dd44eec | 等于（byte-exact） |
| docs/research/phase21w6_marker_scan.json | R-a | 0069cc5c0129c214 | 0069cc5c0129c214 | 等于（byte-exact） |
| docs/qa/phase21w4_qa_report.md | QA | f969ce17c331b115 | f969ce17c331b115 | 等于（byte-exact） |
| docs/qa/phase21w4_qa_evidence.json | QA | 2bf1e47f94da39a8 | 2bf1e47f94da39a8 | 等于（byte-exact） |
| verify_phase21w4_qa_espinosa.py | QA-见证器 | 043f7b956c0b8ea2 | 043f7b956c0b8ea2 | 等于（byte-exact） |

- 镜像集判定汇总：9 件全部 byte-exact 等同。

### 5.2 本档四件 sha256（生成时点）

| 文件 | 工作仓 sha256(前16) | 发布仓 sha256(前16) |
|---|---|---|
| docs/research/phase21w4_names_fix_archive_report.md | （本文件；sha 见回执节） | 9fd44b68242a500d |
| docs/research/phase21w4_names_fix_archive_evidence.json | 987b1a4451009960 | 987b1a4451009960 |
| verify_w4_names_fix_archive.py | ae9388efd4c3ac64 | ae9388efd4c3ac64 |
| build_w4_names_fix_archive.py | 48d3a1bc480be09e | - |

### 5.3 链上 pin 与当场实测计数（生成时点）

| 项 | W4 链终态 pin | 当场实测 | 说明 |
|---|---|---|---|
| figures（DB 行） | 1027 | 1027 | 与执行/清档/QA 三处报告一致；本卡复测 |
| routes（web_p0_routes.json） | 1358 | 1360 | 现值含 R9 收口 +2（船长 11:40 登记；已提交并镜像） |
| sitemap（web/public/sitemap.xml <url>） | 1359 | 1361 | 同 routes，+2 归 R9 收口 |
| unified（index.unified.json items） | 1342 | 1344 | 构建产物；现值含并行链增量（归因见第六节） |
| modes（发布面） | 3221 | （不重算） | 发布面计数值；本卡不重算（pin 引用 QA） |

### 5.4 备份 MANIFEST 复核（逐件 sha256）

| 目录 | 台账 | 复核 |
|---|---|---|
| data/backup_phase21w4_fix_20260924 | fix（t_536073f4） | 11/11 PASS |
| data/backup_phase21w4_fix2_20260924 | fix2（t_33240de8） | 4/4 PASS |
| data/backup_phase21w4_rwkag_clear_20260924 | rwkag 清档（t_ee203180） | 89/89 PASS |
| data/backup_phase21w4_fix3_20260924 | B-a（t_def07a84） | 4/4 PASS |

### 5.5 git 对账（生成时点）

- 工作仓 HEAD = `4987911b1c720530c606a0134aae7a86576c5b56`（master，本地提交面）。
- 发布仓 HEAD = `d38953df890457064cf98da23c8eb624c0da4c65`（origin/main 面，随本卡镜像推进）。
- 锚点（逐条实测可解）：
  - ws `40320e37`（40320e374564）W4 窗口起点 BASE（QA §三）
  - ws `8a0ac56d`（8a0ac56db7e9）清档终态 EE（QA §七）
  - ws `2de84904`（2de84904bbb2）fix2 终态 HEAD_CLAIM（QA 窗口 HEAD 钉）
  - ws `bf177cda`（bf177cdaa446）routes/sitemap 未提交项收口（船长 11:40 登记）
  - pb `06c0637`（06c063749186）routes/sitemap 两件收口镜像（船长 11:40 登记）

### 5.6 与上游数据逐字核对（生成时断言）

- 16 H-* 与 5 码族：`scenarios_zh.json` / `scenarios_en.json` 的 `name` 值与 4.4.1/4.4.2 终表逐字一致（guard_scenarios 断言）。
- 清档面：SG-Lee-001 / MY-Mah-001 / JP-Sas-001 / UZ-Ulu-001 / RW-KAG-1..27 在两源 0 存在（断言）。
- 错名面：`scenarios_zh.json` 全文 0 命中「毛先念 / Mao Xiannian」（R2 + B-a 落盘复核断言）。
- DB 面：`api/protreptic.db` figures 行 = 1027（pin 断言）；21 码 name_zh/name_en 抽查见证据 JSON。

## 六、核验

### 6.1 上游 QA（t_8bad8d98）判定（引用）

- 总判定 PASS；v3 复跑 140 断言 / 0 FAIL / 45 DRIFT 登记（板面并发归因，rc=0）；v2 137/0。
- 逐项吻合：21 码回填 / 清档残扫 0 / 重键完整 / 备份 byte-exact（fix 11-11、fix2 4-4、rwkag 89-89 + 抽样 9-27）/ 计数自洽 1027-1358-1359-1342-3221 / 门禁六工具 rc=0 / 官方 parity 2395 逐字节 / H-MZ-001 R1-R3 一致。
- 注记 4 项（非链缺陷）：A QA 见证器自体命中（上游 21-21 为 QA 前状态）；B body_text_chars 逐键差未登记；C 两异常目录账务差异（本档补记，见第七节）；D B-a 裁定转 t_def07a84（已完成）。
- 报告与证据：docs/qa/phase21w4_qa_report.md / docs/qa/phase21w4_qa_evidence.json（本卡随链尾镜像入库）。

### 6.2 本卡独立验收（第二实现）

- 脚本：verify_w4_names_fix_archive.py（根级；不 import 生成器）。
- 结果：ALL PASS 0 FAIL（A-E 分段全 0；含 5/5 反向注入自检）；断注明细见证据 JSON。
- 段目：A 档案结构（九节/终表/裁定齐全）；B 镜像面 byte-exact；C 提交链 git 实测；D 上表数据逐字核对 + 备份复核；E 裁定/R-a/R-b/R-c/R-d 记录；F 反向注入自检。

### 6.3 parity 复跑（本卡）

- diff 41 项：W4 归属（R-a 6 + QA 2）已归零、only_publish=0；归因=W8b1 在制 29 / 源链接链 4 / 审计链 3 / 生成物 3 / W10 债务 2（见 scratch/w4arch/parity_after.json）。
- 口径：tools/check_repo_parity.py --json；W4 归属项（R-a 6 + QA 2）由本卡归零；余项逐条归因（W8/W10/R9/他链在制与保留面）。

## 七、残留与账务登记

- **R-a（parity 镜像缺件 6 件）**：本卡收口（byte-exact 镜像 + push + parity 复跑归零）；明细见第五.1节。
- **R-b（根目录 H-LXN-001.json 错名残留）**：仍归 W7 链（船长 07:40 裁定「勿并本卡」）；本卡零触碰。
- **R-c（docs/figures/H-LXN-001.md）**：实测 2 处为「误写说明」注记、非错名正文，不改（fix_report 第六节）。
- **R-d（data/asia/individuals 两异常目录）**：manifest 第8节-3 建议 rmdir；QA 实测两目录已不在（空目录、无数据影响；mtime 2026-09-24 06:36:53）；本档补记账务，无对象可处置。
- **注记 A（QA 见证器自体命中）**：非链缺陷；上游 21-21 为 QA 前状态，QA 后 20-21 预期；建议后续豁免表收录（非返工）。
- **注记 B（body_text_chars 逐键差）**：minds/H-WC-001 4210->4209（W5-B 徽章文本变化），W4 回执按收敛族登记；本档照登（非返工）。
- **R12 登记项**：F 类 547 场景侧回填 / 装载器键回退 / 多码深度去重 -> 待用户口径。
- **W10 两文档**（candidates_v5_research.md / phase21w10_coverage_report.md）发布仓镜像缺失：归 W10 链后续收口（不在本卡 R-a 6 件口径内；船长 08:50 债务登记）。
- **B-f site_docs 陈旧构建**（Mao Xiannian 命中）：维持登记，待 CI 重建产品面（船长 07:45）。
- **船长收口登记**：2026-09-24 11:40 船长登记：fix3 报告第7节交办的「routes/sitemap 未提交项」已由船长收口（工作仓 bf177cda -> 发布仓 06c0637 -> push；R9 口径 routes 1360 / sitemap 1361，两件两仓 byte-same）。 本档登记为「船长已收口」，无需卡内动作。

## 八、下一步

- 本卡 done 后放行：t_0dc95522（W5 修复·数据侧 F1，barbosa）-> t_30d57ff2（F2 独立复验，espinosa）-> t_bda44643（F3 文书侧，pigafetta）。
- W7 链门控后置更新（t_d24e11bc -> 依赖本卡与 F3 之后）。
- 本链无卡内遗留动作；R-b/R12/W10 债务按各自主管链推进。

## 九、附链（全号索引与复跑）

### 9.1 提交全号索引

- 工作仓（W4 链 18 笔 + 携带 1 笔）：
  - e7be5cc6  e7be5cc6aec80d998887d3c62cfac05d14d42edd  09-24 06:15
  - 8ca52c04  8ca52c046548cdf3d55e217b229731232f0b5e77  09-24 06:16
  - 9ed628e8  9ed628e8412e1aa104d5cf623d6b66378447fa46  09-24 06:17
  - 37545ac7  37545ac770d6b0d3c0be4ffb40c9a404b47f70b1  09-24 06:18
  - 33762c4e  33762c4e90dff6335009f8667c13b4f669ca74bc  09-24 06:48
  - 4aa62574  4aa625740b0291eb6dae2839850cbe92d5d27f0f  09-24 06:52
  - 8a0ac56d  8a0ac56db7e961b39c98035197bc5d5676fdee2e  09-24 06:52
  - 00bc34a2  00bc34a275ad35ef8c317a8f84781dc95e39fada  09-24 07:12
  - 489b72c3  489b72c3852c6c558d8568c28fe1e4ca0a214fb6  09-24 07:13
  - 2de84904  2de84904bbb26ab2db0b4171f623d036bbb3ed36  09-24 07:14
  - 17bfa994  17bfa9949ce7817a50a2432f969c031f0717ffc5  09-24 07:53
  - 5891cecc  5891ceccf2aa3ced6013c30ad0cc13c976a74c81  09-24 08:05
  - 9c1fd3dd  9c1fd3ddf72806e2acf36d246f110c1dd299d563  09-24 08:05
  - c1fe9024  c1fe9024fbe935a29b95116861c4ad22d35348a4  09-24 10:25
  - 8d461a2e  8d461a2ea5dbbc446240dc13d981f68fde013a0d  09-24 10:30
  - 3f102ee1  3f102ee1d6014b2bd22e769db884b8ba1a1c538c  09-24 11:10
  - a8ec9afe  a8ec9afef597bbbbdff7752ed55ec655f9a9425d  09-24 11:12
  - 4e78ace6  4e78ace62a3bbb243b13226c64f34fd3307261cf  09-24 11:13
  - 1de660cf  1de660cfd5964f72313f3a4a3f38670c5e745240  09-24 02:14
- 发布仓（W4 链 13 笔）：
  - da1e9bc  da1e9bc9634f7c0b3a250241de4d21e1308fb72f  09-24 06:16
  - faccfbe  faccfbeaaa27a98b8cb9b33de123453d50025452  09-24 06:16
  - 7d6d1e9  7d6d1e9e671b8355f6288ca5c356d978fe6f9e56  09-24 06:17
  - e5c111a  e5c111a9d36bfd6b1b806dab21b16f4ee85a9863  09-24 06:18
  - 74c5522  74c5522ba106c5c7e6e4bf7f3fa60482aff63188  09-24 06:50
  - ba3b1fa  ba3b1fa57fc0a0631ca0a30c94cbc735826765f3  09-24 06:52
  - 332188d  332188d9ec4812711eb966be611b6ce0f812d91a  09-24 06:53
  - 0517b38  0517b387d21382307ecba168f88c6d78b542fa69  09-24 07:12
  - 8e4d3e6  8e4d3e676038a3f1888daaf8fd80d859e0d6e611  09-24 07:13
  - c646f41  c646f41a5c4fc65027d403cf448c847fc4756060  09-24 07:14
  - 0dda13a  0dda13abc4f8f371139141a340fca5f411fdd548  09-24 11:10
  - 3cb64c3  3cb64c3eb3333d52c5aff586b7187079eef6c5ee  09-24 11:12
  - d0c7306  d0c7306c5f23cfeaac039d07f6afea57a4bf7a31  09-24 11:13
- 锚点：
  - ws 40320e37  40320e37456413bc7721bce759207d6af76c86d3
  - ws 8a0ac56d  8a0ac56db7e961b39c98035197bc5d5676fdee2e
  - ws 2de84904  2de84904bbb26ab2db0b4171f623d036bbb3ed36
  - ws bf177cda  bf177cdaa44677bb0e80a96a49e0a000a8c79b87
  - pb 06c0637  06c063749186420eb89f57b328f255a1ad931c5f

### 9.2 台账与 scratch

- 台账：/opt/data/cache/protreptic_work_backlog.md（append 登记，append-only）。
- scratch：/opt/data/profiles/pigafetta/cache/scratch/w4arch/（parity_before/after.json、verify 输出、fs 清洗工具）。

### 9.3 复跑命令

- 幂等校验：python3 build_w4_names_fix_archive.py --check
- 独立验收：python3 verify_w4_names_fix_archive.py（证据默认写 docs/research/phase21w4_names_fix_archive_evidence.json）
- parity：python3 tools/check_repo_parity.py --json
