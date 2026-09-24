# Phase21-W5 数据侧修复报告（卡 t_0dc95522）

- 卡：`t_0dc95522`（barbosa；船长 2026-09-24 派发）；父卡 `t_616e4991`（W4 链尾，已 done 放行）；子卡 `t_30d57ff2`（QA/W3 复核）
- 边界：仅 `data/**` + E 工具处（`tools/fetch_source_texts.py`、`tools/source_text_cache.py`）+ 本报告；未重写历史报告（归文书卡 `t_bda44643`）；未碰 W4/W7 在途件
- 开工预检：扫在途卡（`/opt/data/kanban/boards/protreptic/kanban.db`）→ 无并行写 `data/modes_data.json` 者；父卡 done（未触发并写 blocked）
- 一句话结论：10 条处置全部落盘（**20 处字段改动 + 4 条注记**，三面一致）；zh-cn 副本 3 个失败块重试补齐、元数据**如实更新**为完整副本（非硬写）；findings/四态/gate/verify_findings/--check 全绿；E 写口断言 + 读侧加固 5/5 + 3/3 反注入通过

## 零、四件门禁（终稿实测）

| 命令 | exit | 关键数字（before → after） |
|---|---|---|
| `python3 tools/credibility_gate.py --hard-fail` | **0** | 新增硬失败 0；warnings(D4/D5) 28 → 27；D4 matched 11 / mismatch **27 → 26** / quote-too-short 117 → 118 / unchecked 3176 |
| `python3 tools/verify_findings.py --hard-fail` | **0** | hard failures 0；新增 0；基线条目 total=0（冻结位 2026-09-19T15:20:44+00:00，data_sha256 与现状不同不影响判定）；警告 1（M-ASM 双收，存量） |
| `python3 tools/apply_verification_status.py --check` | **0** | 「库中状态与本规则逐条一致」；变更 = 无（已一致） |
| `python3 tools/test_credibility_d45.py` | 1（**预期**） | 37/38；唯一 FAIL = **Z7**（backfill_lifespans 清单存量 476 vs 576），**非本卡** |

四态 before → after（`--check` 口径，before = 开工基线 `avs_check_before.txt`）：

| 口径 | verified | pending | suspect | unverifiable | 和 |
|---|---|---|---|---|---|
| 全库 3311 | 1018 → **1019** | 1887 → 1887 | 55 → **54** | 351 → 351 | 3311（自洽） |
| 公开 3251（剔隔离 60） | 1018 → **1019** | 1855 → 1855 | 38 → **37** | 340 → 340 | 3251（自洽） |

- S1 交 S2 重叠：28 → **27**；`--write` 应用变更 = `suspect -> verified` **1 条**（M-WC-009：退出 D4/D5 命中后按 S2 解析到可达链接）
- findings 重跑：条目 **168 → 167**（`D4_quote_mismatch` 27 → 26，移除项 = M-WC-009 旧锚；**新增 0**）；其余计数不变（D1 60 / D2 10 / D3 6 / D4_quote_without_source 27 / D5 1 / D6 37 / D7 0）

## 一、A：10 条处置落盘（逐条 前→后 + 见证定位 + A1 依据）

面：`md`=`data/modes_data.json`、`fg`=`data/figures/H-WC-001_modes.json`、`ind`=`data/individuals/H-WC-001_modes.json`。
见证定位：全文底本 `data/audit/source_texts/6f2e2e4e124df80a.txt`（`行:列`）+ 逐篇抽本 `docs/scratch/phase21w5_wangchong/witness/raw/lunheng-NN.txt`；转换副本 `data/audit/source_texts/6f2e2e4e124df80a.zh-cn.txt`。A1 = `docs/research/phase21w5_wangchong_sourcing_report.md`。

| # | 条目 | 改动面 | 前 → 后 | 见证定位 | A1 依据 |
|---|---|---|---|---|---|
| 1 | M-WC-002 | md+ind `key_quote_zh` | `苟有不晓解之问，迢难孔子，…` → `…追难孔子，…`（迢→追 1 字） | 底本 `911:74`（`（迢）〔追〕難孔子`，off 80215）；抽本 `lunheng-28.txt 16:74`；副本 `1001:74`（保留校勘符号 `（迢）〔追〕难孔子`） | §M-WC-002 首选项「改字为『追』并注记底本样式」；依据：底本含（ ）〔 〕校勘符号=底本误字/校改字 |
| 2 | M-WC-003 | md+ind `key_quote_zh` | `天地合气，万物自生。天动不欲…` → `天地合气，万物自生。……天动不欲…`（拼接处插「……」） | 前段 `2004:1`（`天地合氣，萬物自生`，抽本 `lunheng-54.txt 10:3`）；后段 `2010:107`（`天動不欲以生物`，抽本 `lunheng-54.txt`） | §M-WC-003「建议在拼接处加省略号并在注中记明省略范围」；两段逐字命中 /54 自然篇 |
| 3 | M-WC-004 | md+ind+fg `source_chapter` | md/ind：`《论衡·证验》《论衡·知实》《论衡·案书》` → `《论衡·薄葬》`；fg：`《论衡·证明》…` → `《论衡·薄葬》` | 底本 `2573:335`（`事莫明於有效，論莫定於有証`）；抽本 `lunheng-67.txt 10:346`；副本 `2783:334` | §M-WC-004「修正 source_chapter：《论衡》无『证验篇』，该句出自《薄葬篇第六十七》」 |
| 4 | M-WC-006 | md+ind `key_quote_zh`；md+ind+fg `source_chapter` | 引文：`万物之生，皆禀元气。人未生在…` → `…。……人未生在…`；出处：md/ind `《论衡·谈天》《论衡·订鬼》《论衡·论死》` → `《论衡·言毒》《论衡·论死》`；fg `《论衡·谈天》《论衡·感虚》《论衡·龙虚》` → `《论衡·言毒》《论衡·论死》` | 前段 `2546:88`（`萬物之生，皆稟元氣`，抽本 `lunheng-66.txt 10:95`，言毒篇）；后段 `2355:33`（`人未生，在元氣之中`，抽本 `lunheng-62.txt 26:33`，論死篇）；副本 `2756:88` / `2549:33` | §M-WC-006「拼接处加『……』并在注/source_chapter 中补《论衡·言毒》」（跨篇两段：/66 + /62） |
| 5 | M-WC-008 | md+ind `key_quote_zh` | `…皆无非——虽明知其非而莫敢难者，问难之道废也。` → `…皆无非，专精讲习，不知难问。`（尾段替换为 /28 逐字收尾） | 底本 `905:6`（`好信師而是古`，抽本 `lunheng-28.txt 10:8`）；副本 `987:23`（`专精讲习，不知难问`） | §M-WC-008「以原文收尾替换改写句（『……皆无非，专精讲习，不知难问。』）」 |
| 6 | M-WC-009 | md+ind `key_quote_zh` | `…一气一声也——人受气于天，不能感天，雷何为感于人而发？` → `…一气一声也——然则雷为天怒，虚妄之言。` | 底本 `652:414`（`然則雷為天怒，虛妄之言`，抽本 `lunheng-23.txt 44:414`）；副本 `718:414` | §M-WC-009（尾段取 /23 见证句）；/23 候选为 A1 §M-WC-007 所列 /23『…然則雷為天怒，虛妄之言』 |
| 7 | M-WC-001 | — | **不改字**（按卡） | §M-WC-001 判定「逐字命中」（/61 佚文篇，pos=1819） | §M-WC-001「无须改字，保持现状」 |
| 8 | M-WC-005 | md 注记 | 新增 `key_quote_context_zh` | A1 §M-WC-005「六个分句全库 85 篇无一逐字命中」 | 卡 7)「005/007/010 加注记：无逐字见证 + A1 候选」 |
| 9 | M-WC-007 | md 注记 | 新增 `key_quote_context_zh` | A1 §M-WC-007「最长连续逐字片段 7 字（公式化用语），非整体见证」 | 同上 |
| 10 | M-WC-010 | md 注记 | 新增 `key_quote_context_zh` | A1 §M-WC-010「四分句全库无一逐字命中；『距师』语出 /28『難於距師』」 | 同上 |

另：M-WC-002 同时新增 md `correction_zh` 注记——

> 改字并注记底本样式：底本作「（迢）〔追〕難孔子」（圆括号=底本误字，方括号=校改字），引文取校改字「追」作「追难孔子」；见证 `docs/scratch/phase21w5_wangchong/witness/raw/lunheng-28.txt`（A1 §二·M-WC-002 首选项：改字＋保留注记）。

五条注记的字段选择（不新造字段名，沿用库内既有注记位）：
- `correction_zh`：库内先例为「引文替换/修正注记」（如 M-ZX-009/010）；
- `key_quote_context_zh`：库内先例为「引文为概括/非逐字」语境说明（180 条），与「查无档」语义一致。
- 注记落 `md`（权威库）；`fg`/`ind` 分片无该类注记字段先例，未加（避免越界扩 schema）。

诚实口径（复核要点）：
- 002 的「追」在底本中以校勘形态 `（迢）〔追〕難孔子` 存在（底本自标校改字），引文按 A1 取校改字；**未**将校勘符号从底本/副本里抹掉。该条 D4 = `quote-too-short`（全部片段 < 8 字），不受副本形态影响。
- 005/007/010 **未替换原文**（按卡只注记并登记 A1 候选原文，替换由后续裁定）。

改动前的三面现值 diff 见 `changes_table.json`（scratch）；改动=**20 处**（md 11 / ind 7 / fg 2），全部带前/后与见证。

## 二、B：zh-cn 转换副本（R2）

1. **首选路线（重试补齐 3 段失败块）**：3 个回退块（raw 偏移 8000×{10,21,32}）重试转换，均在 8 次上限内成功（`err=None`，各 8008 字符；确定性自检 chunk0 重转 == 副本头部 OK）。
2. **重建**：旧副本三区间 `[79745,87745)` / `[167803,175803)` / `[255883,263883)`（各 8000 字符，旧值=原样繁体回退块）替换为新转换块；重建结果与落盘新副本**逐字节相等**。
3. **回退残留探针**：新副本中与 raw 完全相同的 8000 字符块 = **0 个**；`証` 3 → 0（残留繁体专用字清零）；chars 265712 → 265736；sha256 `d26e86f48e1f3a5a…`。
4. **元数据如实值**（`data/audit/source_texts.json` 论衡条目 `zh_cn`）：`chunks=34 / failed_chunks=0 / complete=true / converted_at=2026-09-24T04:17:22+00:00 / chars=265736 / sha256=d26e86f4…`；写入前经过 E 的写口断言（**不是**硬写）。
5. **D4 采用一致性（U4）**：读侧要求 `complete=true 且 failed_chunks=0`（本轮加固，见 §五）；论衡副本被采用，copy 命中 9 条中含 M-WC-006/008。
6. **结论链重算（B-3，按实况）**：
   - M-WC-006：`matched`（via zh-cn 副本，命中片段 `人未生在元气之中`）
   - M-WC-008：`matched`（via 副本，命中片段 `以为贤圣所言皆无非`）
   - M-WC-009：`mismatch` → **`quote-too-short`**（降级为不可核；理由 `all-fragments-shorter-than-min(8)`，旧判为副本内字面不符，属副本含回退块所致的误判形态之一）
   - 全库副本相关计数：`substring-not-found(zh-cn converted copy)` 2 → **1**（剩余 1 条为 M-WB-008，非论衡面）

## 三、C：重跑与留证（输出全文在 scratch）

见 §零表。补充口径：
- 修前基线：`gate_before.txt` / `avs_check_before.txt`（本卡开工时采集）；
- 修后终稿：`gate_final.txt` / `verify_findings_final.txt` / `avs_check_final.txt` / `t45_final.txt`；
- D4 不可核理由分布（前后除下列外全同）：`all-fragments-shorter-than-min(8)` 117 → 118；`substring-not-found(zh-cn converted copy)` 2 → 1；`substring-not-found`(raw) 25 不变；`script-mismatch` 77 不变。
- verify_findings 的 STALE 警告 3 条（M-NKR-010×2 / M-SALADIN-006）为存量，前后一致。

## 四、D：`data/audit/phase21w5_wangchong_status.json` 同步（NEW-1）

- `inputs` 三条 sha256 **全部 = 终稿实测**：`data/modes_data.json` `736aab3b…`（bytes 24894309）/ `data/source_links.json` `dc0aebf0…`（keys 391、links_with_url 178、distinct_urls 172）/ `data/audit/findings.json` `5527607…`（d4_d5_modes 54）
- `counts` = 终稿实测：all 1019/1887/54/351、all_total 3311；published 1019/1855/37/340、published_total 3251；quarantined_total 60
- `changes_vs_library` = `{"suspect -> verified": 1}`（本轮 `--write` 实际应用的变更，如实记录）
- 报告 sha256 `7da1810d16b8092752a6405f82b10df6a4139212636ef9b708ce80aeaa218c4e`

## 五、E：R7① 写口断言（+读侧加固）

1. **写口断言**（`tools/fetch_source_texts.py`）：新增 `zh_cn_meta_violations()` / `assert_zh_cn_meta()`，在 `convert_to_zh_cn()` 返回前与 `main()` 组装条目处各调用一次；新增 `--self-check-zh-cn-meta` 自检旗标。
2. **读侧加固**（`tools/source_text_cache.py`）：`converted_text_for()` 此前只查 `complete` 旗标，现补 `failed_chunks==0` 判定（与函数文档口径一致）——**这正是 QA §1.2/§A.6 事故形态（硬写 complete=true 后被 D4 采用）的封堵点**。
3. **可复核验证输出**：
   - `python3 tools/fetch_source_texts.py --self-check-zh-cn-meta` → **5/5 PASS**，exit 0：
     - W1 `failed=0/complete=true` 通过；**W2 `failed=3/complete=true` 必炸（负向注入）**；W3 `failed=3/complete=false` 通过；W4 `failed=-1` 必炸；W5 盘上索引实测 zh_cn 条目 5 条、违规 0 条（不变量 + 副本文件 sha/chars 逐条复算）。
   - 读侧反注入探针（`probe_read_guard.py`）3/3 正确拒用：`complete=true&failed=3` → None、`complete=false` → None、`failed_chunks` 不可解析 → None；正常条目 → TEXT(210848)。

## 六、幂等与复跑

- `land_ten.py` 复跑：SET=0 / SKIP=20（全条 already）；`restore_marks.py` 复跑：RESTORED=0；`apply_zhcn.py` 复跑：ALREADY（`converted_at` 与 sha 均不漂移）；`apply_verification_status.py --check` 复跑 exit 0。
- 备份：`data/backup_merge_W5FIX_20260924_121533/`（含改前三面/索引/副本/findings/status 及 sha 清单；不入库、parity 排除）。

## 七、提交 / 镜像 / push / parity 回执

（见 §八 回执段——提交后补记）

## 八、边界外 / 未做

- M-WC-005/007/010 未替换原文（按卡只注记 + 登记 A1 候选）；M-WC-001 未改字。
- Z7（`backfill_lifespans.py --check` 清单过期）为本仓存量，归 W11 卡 `t_0ec6fb57`；本卡未动。
- `build_audit_findings.py` 摘要键名沿用 `D4_empty_quote`（存量；本卡未改工具）。
- 未碰 W4/W7 在途件与历史报告。

## 附：复现命令

```bash
# 门禁四件
python3 tools/credibility_gate.py --hard-fail
python3 tools/verify_findings.py --hard-fail
python3 tools/apply_verification_status.py --check
python3 tools/test_credibility_d45.py            # 预期 37/38（Z7 存量）

# E 断言自检
python3 tools/fetch_source_texts.py --self-check-zh-cn-meta

# D4 逐条复算（真实 gate 函数）
#   见 scratch/d4_full_after.py、d4_wc_cmp.py、probe_read_guard.py
```
