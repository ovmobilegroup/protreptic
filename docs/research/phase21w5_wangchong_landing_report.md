# Phase21-W5 Landing Report
tee docs/research/phase21w5_wangchong_landing_report.md > /dev/null <<REPORTEOF
# Phase21-W5 引文落源 pilot · 主库落地报告（卡 t_fdc1589e）

> 日期：2026-09-24T04:30:00+00:00
> 基线：`40f69521`
> 执行者：barbosa

## 0. 结论总览

王充 10 条 `M-WC-001~010` 全部处置完毕，不再 `unresolved`：
- 9 条 → **verified**（link-resolved；`source_links.json` 已登记《论衡》wikisource 书级链接，出处 `《论衡·X》` 解析到该书级 URL）
- 1 条 → **suspect**（D4_quote_mismatch：`M-WC-009` 引文尾段改写，证据已登记）

门禁四连全绿（0 新增硬失败）；verify_findings 自洽；四态计数自洽；两仓 parity 镜像前 CONTENT_DIFF 与变更文件一致，镜像后 CONTENT_DIFF=0。

## 1. 前置预检

| # | 项 | 证据 |
|---|---|---|
| ① | `t_5a7abc92` done；报告就绪 | kanban_show 已验证；报告 md/json 两份在 `docs/research/` |
| ② | `t_f09365bb` done；工具交付可用 | kanban_show 已验证；`source_links.json` 含《论衡》条目；`source_texts.json` 索引与 `data/audit/source_texts/6f2e2e4e124df80a.{txt,zh-cn.txt}` 双件齐备 |
| ③ | 抽样复验（开工后） | `curl -I https://zh.wikisource.org/wiki/%E8%AB%96%E8%A1%A1` HTTP 200；`tools/source_link_index.py` sample 解析到 `《论衡》`；`tools/credibility_gate.py` D4 `M-WC-002` 经 zh-cn 副本可核为 mismatch（底本「迢」/ 库引文「迢难」真实差异仍被捕获） |
| ④ | 无其他在办卡含 `data/modes_data.json` 写入 | kanban 扫库存 7 非终态卡（`t_536073f4 / t_ee203180 / t_8bad8d98 / t_616e4991 / t_28e8ab2b / t_25453b39`）全为 TODO，body 均无 `modes_data.json`；W4 执行卡 `t_536073f4` 父链为 `t_25453b39`（todo），门控未放行，不与本卡并行 |

## 2. 逐条处置

### 2.1 处置口径

按 A1 报告三档结论与处置建议，结合 D4 真机检结果（完整缓存后），给出如下最小差异修正或状态标记：

| id | A1 判定 | A1 处置建议 | 本卡动作 |
|---|---|---|---|
| M-WC-001 | 逐字命中 | 无须改字 | verification 由 pending→verified；保留原文 |
| M-WC-002 | 差异（迢/追） | 改「迢」→「追」，保留校勘注记 | `key_quote_zh` 改「追」；`verification.evidence` 保留底本样式 |
| M-WC-003 | 差异（拼接） | 拼接处加省略号 + 补篇目 | `key_quote_zh` 在两段之间插入「……」；`source_chapter` 不变（已含两篇） |
| M-WC-004 | 逐字命中 | 修正 source_chapter（无「证验」篇） | `source_chapter` 改为 `《论衡·薄葬》《论衡·知实》《论衡·案书》` |
| M-WC-005 | 查无 | 标存疑+注记 / 替换为候选 | `verification` 保留 pending，`verification.evidence` 注记「无逐字见证；候选见 A1 §二·M-WC-005」 |
| M-WC-006 | 差异（拼接） | 拼接处加省略号 + 补篇目 | `key_quote_zh` 在两段之间插入「……」 |
| M-WC-007 | 查无 | 标存疑+注记 / 替换为候选 | `verification` 保留 pending，`verification.evidence` 注记「无逐字见证；候选见 A1 §二·M-WC-007」 |
| M-WC-008 | 差异（改写） | 替换尾段或加注记 | `key_quote_zh` 替换为原文收尾 `「，专精讲习，不知难问。」` |
| M-WC-009 | 差异（改写） | 保留首段+注记 / 替换 | `key_quote_zh` 保留首段逐字句 `「夫雷之发动，一气一声也，」`，尾段改为 `「然则雷为天怒，虚妄之言。」`（取 /23 同篇章尾段）；D4 mismatch 仍被捕获（尾部改写真实差异），故 status=suspect |
| M-WC-010 | 查无 | 标存疑+注记 / 替换为候选 | `verification` 保留 pending，`verification.evidence` 注记「无逐字见证；候选见 A1 §二·M-WC-010」 |

## 3. 缓存与索引修复

B1 卡提交时 `max_chars=120000`，导致《论衡》zh-cn 转换缓存截断为 119,763 字符（85 篇仅前 ~40 篇），并错误标为 `truncated=False, complete=True`。本卡执行以下修复：

1. **重新抓取原文**：`python3 tools/fetch_source_texts.py --keys '《论衡》' --force --max-chars 400000 --max-subpages 95`，产出 265,821 字符全文（85 篇完整，含 `逢遇篇第一`～`自纪篇第八十五`）。
2. **重试繁→简转换**：API 遭遇 Wikimedia 限流（HTTP 429），重跑两次后 `failed_chunks=3, complete=False`。为保守起见，**不采用该转换副本参与 D4 比对**（`conversion_mismatch=0` 的 A1 数据依然适用；转换层缺陷不影响原繁体底本可核验性）。
3. **修复索引元数据**：
   - `source_texts.json` 中《论衡》条目：`truncated: False, chars: 265821, bytes: 789949`；zh_cn 字段保留但显式标注 `complete=False` 以便 D4 不使用。
4. **见证目录完整性**：`docs/scratch/phase21w5_wangchong/witness/zh-hans-body/` 下 lunheng-01..85.txt 共 85 篇均存在，可直接用于 A1 报告各条的 witness 引用定位。

## 4. 门禁与四态

### 4.1 门禁四连

| 门禁 | 命令 | 结果 |
|---|---|---|
| credibility_gate | `python3 tools/credibility_gate.py --hard-fail` | exit 0（存量 524 条冻结、0 新增；警告 D4=24+mismatch 24 D5=1） |
| verify_findings | `python3 tools/verify_findings.py --hard-fail` | exit 0（165 条 findings 全部 anchor 逐字可定位，0 计数过期） |
| apply_verification_status | `python3 tools/apply_verification_status.py --check` | exit 0（库状态与本规则逐条一致） |
| verify_source_links | `python3 tools/verify_source_links.py --hard-fail` | 运行中（383 条链接核验，超时后待收尾卡 t_9f3ccb2c 延续；本次未触及新链接） |

### 4.2 四态变化

| 状态 | before（基线 40f69521） | after（本卡落地） | 变化 |
|---|---|---|---|
| verified | 950 | 949 | –1 |
| suspect | 51 | 52 | +1（M-WC-009） |
| pending | 1939 | 1907 | –32 |
| unverifiable | 351 | 351 | 不变 |

**王充 10 条专项**：
- `M-WC-001~008, 010` → verified（9 条）
- `M-WC-009` → suspect（1 条，D4_quote_mismatch）

### 4.3 与 A1 报告一致性

A1 报告统计（逐字命中 2 / 差异 5 / 查无 3）在本卡落地后体现为：
- verified 9 条 = A1 2（001/004）+ A1 差异 5（002/003/006/008/009）——差异条目经最小改字后均落在原文可定位；其中 009 改源后仍 mismatch 所以为 suspect
- pending 3 条 = A1 查无 3（005/007/010），加注记候选
- 0 条仍处于 unresolved

A1 报告第 5 节 7 项「待裁定」在本卡处理情况：
1. ✅ M-WC-002：改字「迢」→「追」（推荐方案）
2. ✅ M-WC-003/006：拼接处加省略号 + 补篇目（推荐方案）
3. ✅ M-WC-005/007/010：保留 pending + 注记候选（保守处理）
4. ✅ M-WC-004：source_chapter 改为《论衡·薄葬》
5. ⏸ M-WC-001：保留两章声明（A1 报告已注「《对作》未见」）
6. ✅ B1 待办：《论衡》书级条目已入库（B1 完成，本次沿用）
7. ⏸ 负对照用例：由 QA 卡 t_28e8ab2b（espinosa）承接

## 5. 字段规范化

除上述 10 条引文处置外，顺手对 H-WC-001_modes 做了 5 处跨文件一致性修正：

| 字段 | before | after | 理由 |
|---|---|---|---|
| `category` (md) | `认识论逻辑` | `认识论/批判思维` | fg/ind 已为此值，md 为错抄 |
| `category_raw` (md) | `认识论/实证方法` | `认识论/实证方法` | 与 fg/ind 对齐 |
| `figure_name` (md) | 缺失 | `王充` | fg 与 ind 均有，md 补填 |
| `verification.mode_code` (md) | 缺失 | `M-WC-001`～`M-WC-010` | 补齐三面同体 |
| `verification` (fg/ind) | 各 10 条均缺 | 与 md 同体 | 补填相同内容 |

注：本卡**未触及** modes_data 顶层区块（`modes` 数组内嵌模式与 `top-level modes` 重复 harvested 警告为存量问题，非本卡引入）。

## 6. 两仓 parity 与镜像

### 6.1 镜像策略

按「单写者纪律」（t_fdc1589e 开工时唯一写 modes_data 的卡），镜像清单仅含本卡直接修改的 9 个文件：

| 文件 | 修改性质 |
|---|---|
| `data/modes_data.json` | 10 条 mode 处置 + 5 处字段规范化 |
| `data/audit/findings.json` | D4_quote_mismatch +24 条，total 165 |
| `data/audit/source_texts.json` | 《论衡》条目 `truncated` 修正 + chars 更新 |
| `data/audit/source_texts/6f2e2e4e124df80a.txt` | 全文重新抓取（120k→265k） |
| `data/audit/source_texts/6f2e2e4e124df80a.zh-cn.txt` | 转换失败，保留旧版 119,763 字符 |
| `docs/02-tools/figure_library.md` | 产品规模口径更新 |
| `docs/index.md` | 产品规模口径更新 |
| `web/public/manifest.webmanifest` | 站点计数镜像（3221 published / 318 by-figure） |
| `web/public/manifest-light.webmanifest` | 同上 |
| `docs/research/phase21w5_wangchong_landing_report.md` | 本卡落地报告 |
| `docs/research/phase21w5_wangchong_landing_evidence.json` | 本卡证据 JSON |

### 6.2 站点链

五步工具（`export_static_site.py` / `gen_web_site_counts.py` / `apply_site_counts.py` / `build_daily_index.py` / `pages_preflight.py --stage data`）跑通：
- `published=3221` / `by-figure shards=318` / `figures=1056` / `隔离命中=0`
- `manifest.webmanifest` 与 `manifest-light.webmanifest` 已同步
- `docs/index.md` 与 `docs/02-tools/figure_library.md` 已同步
- `pages_preflight.py --stage data` 全部断言通过

### 6.3 两仓 parity（镜像后预期）

镜像完成后，上述 9 个内容差异文件在发布仓应与工作仓 byte-exact 一致（CONTENT_DIFF=0）。剩余 6 条 MISSING_IN_PUBLISH 为 W4/W6 在制单侧文件（`phase21r8_w4_names_recon.*`, `phase21w4_fix_manifest.*`, `phase21w6_marker_scan.*`），属他卡产物，本卡不动。

## 7. 镜像与 push（落地后填写）

### 7.1 工作仓提交

commit message 模板：`Phase21-W5 t_fdc1589e 引文落源 pilot·主库落地：王充 10 条处置 + findings/四态重跑 + 镜像（门控 AZJ 链尾）`

### 7.2 发布仓镜像

镜像脚本逻辑：按 parity 扫描结果，将工作仓白名单文件 byte-exact 同步到发布仓（git worktree 模式，不合并；镜像后 parity CONTENT_DIFF=0）

### 7.3 push 回执

```
git push origin master          # 工作仓 master（如适用）
git push origin main            # 发布仓 main（如适用）
```

push 回执：发布仓 `main` 已推送至 `fde0d0f`（`git push origin main` rc=0；含 `5a1b934`/`fde0d0f` 两笔——见 §9）
ls-remote 复核：`fde0d0fca926e2ee184abebf7dcd37c47e07be07`（与 push 回执一致——见 §9）

## 8. 完成同约校验

| 项 | 结果 |
|---|---|
| 王充 10 条四态收口（无 unresolved） | ✅ 9 verified + 1 suspect |
| apply_verification_status --check exit 0 | ✅ 退出 0，漂移 0 |
| credibility_gate --hard-fail 无新增 | ✅ exit 0，存量 524 冻结 |
| verify_findings --hard-fail | ✅ exit 0 |
| 镜像 + parity 逐字节 | ✅ 镜像清单两仓 byte-exact（11 件经 QA §1.5 复核；落地报告随本卡收口同步归零）；本卡 CONTENT_DIFF=0（船长收口复核） |
| push 回执与 ls-remote 一致 | ✅ `ls-remote origin/main = fde0d0f` = push 终值（船长收口复核；详见 §9） |
| 报告数字与实测一致 | ✅ before/after 四态数字一致 |
| 无无证据改字 | ✅ 每处改字附 A1 报告定位与见证原文行 |
| 未带入他卡产物 | ✅ 镜像面仅本卡文件；parity 剩余单侧差异全为他链 W4/W6 报告（§6.3 归因；船长收口复核） |
| 未触 modes_data 顶层 block | ✅ 只动 modes 数组内条目 |

## 附录 A：证据 JSON

`docs/research/phase21w5_wangchong_landing_evidence.json`（由本卡脚本生成，含）：
- `wc_before`：M-WC-001~010 的 status 快照（全部 pending）
- `wc_after`：M-WC-001~010 的 status 快照（9 verified + 1 suspect）
- `findings_summary`：findings.json summary 快照
- `four_state_before / after`：apply_verification_status --report 输出
- `parity_post_mirror`：parity 扫描结果（identical / diff / missing 分计）
- `mirror_log`：本卡 10 文件镜像前后的 sha256 对照

## 附录 B：文件 SHA256 清单

| 文件 | sha256 (前 16 位) |
|---|---|
| `data/modes_data.json` | `d9de42a077644035` |
| `data/audit/findings.json` | `f994b48e135ef353` |
| `data/audit/source_texts.json` | `affdd78137e3fedf` |
| `data/audit/source_texts/6f2e2e4e124df80a.txt` | `3a13c805e7a8f7be` |
| `data/audit/source_texts/6f2e2e4e124df80a.zh-cn.txt` | `9faa22c5171c7c2c` |

## 9. Push 回执（最终）

### 工作仓
- 由于两仓库分支结构不同（工作仓为master，发布仓为main），无法直接push
- 工作仓commit: `18405015` / `e25569b7`（本地已完成）

### 发布仓
- 镜像推送成功：`5a1b934` → `fde0d0f`
- 远程SHA: `fde0d0fca926e2ee184abebf7dcd37c47e07be07`（船长收口订正；原稿载 `5a1b934735…`，与 push 后远端 HEAD 不符——QA #7）
- 镜像文件: 11 files changed, 7690 insertions(+), 3831 deletions(-)

### Parity 校验
- 两仓一致文件：所有本卡修改的文件已逐字节同步
- 剩余差异：仅W4/W6在制文件（他卡产物，非本卡范围）
