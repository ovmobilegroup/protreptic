# Phase21-R8 王祥重做链 QA 独立验收报告

- 卡: `t_b92cc1cf`(profile espinosa) | 验收对象: 重建卡 `t_5c183962`(A1, 提交 1fe4c451) + 合并卡 `t_8c521af7`(A2, 提交 d95a7b53 / 回执 68d6e0b0)
- 日期: 2026-09-24 (CST) | 结论: **PASS**(177 PASS / 0 FAIL / 0 SKIP; 反向注入 10/10; 门禁四项复跑全绿/如实登记)
- 独立脚本(第二实现): `verify_hzx002_qa_espinosa.py` | 证据: `docs/qa/phase21r8_wangxiang_qa_evidence.json`(+ `.txt`) | 自检: `docs/qa/phase21r8_wangxiang_qa_selftest.json` | 门禁原始输出: `docs/qa/phase21r8_wangxiang_qa_gates/`

## §1 口径与方法(不采信上游自述)

```
期望值来源(更上游, 一次源): R7 素材包 JSON(P01-P16) / R6B 修正稿 corrected_record / R7 归档登记 sha /
  A2 合并提交 d95a7b53 的 git 对象 / 现网字节(sha256)
被验对象在"冻结态"评估: FROZEN_WX = d95a7b53(数据面合并提交, 68d6e0b0 仅回执文档)
现场态(工作区现状, 含他卡在制)仅作漂移登记, 不回滚不清场
A1/A2 的报告与核验脚本仅作线索, 不作判据; 全部断言为重算/逐字节比对
```

分组: A/B/D/E/F 数据面(116) + S 上游冻结面(29) + C 见证复核(7) + G 门禁(5) + H 站点(11) + I 两仓 parity(8) + J 自检(1) = **177 PASS / 0 FAIL / 0 SKIP**。

## §2 反向注入自检(判据有效性, J)

10 项注入对 10 个核心判据逐一必须"基线 PASS→注入 FAIL", 最终 **10/10 命中**。

本轮修复了两处判据弱点(修复前 8/10, 修复后 10/10, 均为判据灵敏度问题, 非数据缺陷):

- **注入3(主库条数 -1) 未触发**。根因: D1 只查 `len(modes) >= 3281`, 而工作区因他卡在途增量(`M-LUORQ-*`)实际 3291 条, 弹 1 条仍过阈值。修法: D1 收紧为「本链 10 条计入主库计数(逐码可查)」, 注入目标改为删除一条本链条目, 修复后必拦。
- **注入5(标签语言改错) 未触发**。根因: 注入改的是 `scenario_tags` 尾元素, 但尾部已是他卡(`H-LUORQ-001`)标签, 改不动本链。修法: 注入定位到最后一条本链(`figure_code==H-HZX-002`)标签, 修复后必拦。

即: 判据集合在"库里存在他卡在途增量"的真实并发条件下依然逐一有效。

## §3 要点对照(卡片五要点)

### ① 10 条逐条核验: quote 与 R7 素材包逐字 + 见证复核
- B 组 60 项: 10 条 `key_quote_zh` 与素材包 P01-P16 逐字全等(001→P01, 002→P02, ..., 009→P09, 010→P10 等); 引文归属经"按旧号 M301~M310 独立推导候选素材"复核, 全部落回 R7 候选集; 英文引文非空无 CJK; 「」片段全部可溯源(素材包子串/异文/概念标签), 越界 0。
- C 组 7 项(现网/缓存): **W1 维基文库《晋书》卷三十三 raw 复核 P01-P12 逐字 12/12**; W1 用字方向(基字 未/灸/覆 在, 异字 末/炙/復 不在); **W3 汉典古籍卷三十三 抽样 7 条逐字 7/7**(P01,P02,P04,P07,P09,P10,P12); W3 与 W1 用字一致; W5《二十四孝》P14 诗赞+P15 正文; W4《搜神記》卷十一 P16 王祥条全文; W2 四库本卷033 异文方向相反(末/炙/復 在)。报告见证 W1/W3 两项(卡片明示)均独立重取复核, 取文含缓存留痕。

### ② 全库完整性: 王祥视图五面一致、0 重复 id
- D 组: modes_data 主库本链 10 条逐字等于落盘 entries; 全库 `mode_code`/`id` 字段 0 重复; 合成码口径重复集与合并前基线全等(唯一重复对 M-ODANOBUN-* 属既有双表示); code_maps(figure) 十码/十名/互引 0 悬空/3 键; figure_names=王祥; scenarios_zh/en 各 +10 键="C-WX-001~010(/E)", 8 键集/题名/码/模板复算/应用域全对; scenario_tags +20(每模式 zh+en 各一, 命名全对); figure/individuals/_modes 三面同体; 五面(主库/figure/code_maps/scenarios/tags)王祥码集一致 == M-WX-001~010; 落盘镜像与主数据面字节相等。

### ③ 旧号与僵尸
- M301~M310 在活动编码空间 0 复现(D4), 新增 10 条内 M30x 仅存留证字段 `legacy_mode_id` 等, 越界 0(D6); 旧题旨/旧定义句/旧自造句/伪占位在活动数据面 0 命中(E1-E3); **归档三件 `data/figures/_duplicates/H-HZX-002*` sha256 与 R7 登记一致、未变**(E4: 8c40067c/1e3e97d4/8b63cda2...); 三卡提交均未触碰归档件(E5)。

### ④ 船长裁定执行抽查
- F1 M-WX-001 题旨=侍疾尝药法(锚 P01); F2 M-WX-002 更名为卧冰求鲤法; F3 M-WX-008 题旨=立身五本:信德孝悌让且独立成目; F4 M-WX-009 子项降级(元代/二十四孝/无 宋以降 断言); F5 A08 中性表述(长揖晋王, 无司马昭 断言); **F6 底本用字: 006 作 灸 非 炙 / 008 作 覆 非 復**; F7/F8 异文 V1-V3 登记于条目备注与 figure caveats; F9/F10 场景前缀 C-WX 落盘前 0 占用、全库无变体前缀。

### ⑤ 门禁复跑 + 站点计数 + 两仓 parity
- G1 credibility_gate --hard-fail exit 0(新增基线外 0 条); G2 verify_findings --hard-fail exit 0; G3 verify_source_links --hard-fail exit 0; G4 apply_verification_status --check 如实登记漂移 19 条(本链 9 条纪律(4) 不回填 + 他卡在制追加; 未跑 --write); G5 本链 10 条在库仍全 pending。
- H **冻结态复现**(临时 worktree @ d95a7b53, 不改主工作区): export_static_site exit 0 且 `figures=1057 modes(源)=3271 modes(发布)=3211 隔离剔除=60 by-figure=317`; gen_web_site_counts + siteCounts.ts=3211x317; meta.json 3271/3211/317/1057/60; 锚点 EXPECT_MODES=3271 / EXPECT_BY_FIGURE=317 / EXPECT_FIGURES=1057 两处一致; build_daily_index=3211/317/317; pages_preflight --stage data 全部断言通过。
- I 两仓 parity: 官方机检本链路径零差异; 本链路径集(边界内 30 件)两仓 HEAD 字节一致; 发布仓 HEAD 祖先链含 9c4ff9e/dab8213; 远端 origin/main 含 dab8213d5bfd; 差异全为在制未跟踪/待镜像件, 归属登记见证据。

## §4 现场漂移登记(他卡在制, 不回滚)

- 主库/注册面现场=合并提交态 + 罗瑞卿卡(t_bf2d9b82)在制追加: modes +10(M-LUORQ-*; 本链前缀 3281 条逐对象全等) / code_maps +1 / figure_names +1 / scenarios_zh+en 各 +10 / scenario_tags +20; 本链前缀键序/条目全等(D5L/D7L/D10L/D11L/D12L/D16L)。
- 站点现场态=他卡复跑产出 3221 x 318(与现场 meta 自洽, Hl1/Hl2); 合并面六件 sha 相对 A2 manifest 漂移登记(S2L/S4L, 逐提交列示); 本链入库对象现场字节未动(D19L/S4c)。
- 发布仓镜像/push 属合并卡边界(9c4ff9e/dab8213 已在远端), 另 4 条 parity 残余为他卡未跟踪在制文件, 非本链。

## §5 边界与遗留

- 冻结 worktree 留在 `~/.cache/wxqa_frozen_wt` @ d95a7b53(审计留痕; 主仓 .git/worktrees 增一条登记), 可按需 `git worktree remove`。
- Hf2b: 冻结 worktree 无本地 dist, `apply_site_counts` exit=1 属工作区态差异, 已存证非缺陷(主工作区在先复跑 exit=0)。
- G4 漂移 19 条明细含他卡码(如 M-WC-*), 权威归属待各自卡收口; 本链 9 条维持 pending 不回填属纪律(4)如实登记。

## §6 证据清单

```
verify_hzx002_qa_espinosa.py                            # 独立脚本(第二实现, --selftest 支持反向注入)
docs/qa/phase21r8_wangxiang_qa_evidence.json / .txt     # 177 项断言全量留证(含 anchor sha)
docs/qa/phase21r8_wangxiang_qa_selftest.json            # 反向注入 10/10
docs/qa/phase21r8_wangxiang_qa_gates/gate_*.txt         # 四门禁原始输出
docs/qa/phase21r8_wangxiang_qa_gates/chain1..5_*.txt    # 现场态链条复跑留档(在先)
docs/qa/phase21r8_wangxiang_qa_gates/frozen_chain*_*.txt# 冻结态链条复现输出
docs/qa/phase21r8_wangxiang_qa_gates/parity_check_repo.txt
```

## §7 提交回执

- 工作仓提交: `ae72a7d2`(20 件 = 报告 + 独立脚本 + 证据 json/txt + 自检 json + 门禁/链条日志 15 件; 4246 insertions; 定点添加零夹带, 他卡在制改动未入库)。
- 主库/归档未动(本卡零数据面写入); 发布仓镜像与 push 归合并卡(t_08bbb73d 边界), 本卡零触碰。
- 本报告与证据在提交 `ae72a7d2` 处冻结; 现场态若继续演进, 以本卡证据 json 的前缀全等/漂移登记为准。

## §8 复跑指引

```
python3 verify_hzx002_qa_espinosa.py            # 全量(默认含门禁与站点, 网络不可达走缓存)
python3 verify_hzx002_qa_espinosa.py --selftest # 仅反向注入(离线)
QA_FROZEN_WT=/path/to/wt python3 verify_hzx002_qa_espinosa.py --no-network
```
