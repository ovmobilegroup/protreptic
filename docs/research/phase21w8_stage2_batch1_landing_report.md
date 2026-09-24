# Phase21-W8 Stage2 批1 · 主库落地报告（卡 t_b85ae14a）

- 任务：`t_b85ae14a`（父卡 `t_70a8cbce` 素材包 → 本卡落地；子卡 `t_e727be57` QA）
- 输入：`docs/research/phase21w8_stage2_batch1_sourcing_report.md/.json`、`phase21w8_stage2_batch1_booklist.json`、`data/audit/source_texts_w8_stage2_batch1.json`（17 条缓存 +154 条逐条 verdict）
- 规则面：`docs/planning/credibility_framework.md`（S1~S4 四态 / D4 引文不符）；`data/audit/verification_status.json`
- 生成时间：2026-09-24（CST）

## 0. 结论总览

批1 处置已按「先备份后落地」入主库，落盘可复核（逐条账本），重跑/站链/parity/push 证据齐：

1. **链接入库**：8 部中文书（lang=lzh）写入 `data/source_links.json`（383→391 key；url/canonical_title/provider/checked_at 全部取实测值）。
2. **缓存合并**：批1 独立索引 17 条条目并入 `data/audit/source_texts.json`（97→114 条；sha256/file 原样搬，不重写字段）。
3. **四态重算**：`pending→verified 69`、`pending→suspect 3`、其他 0；包外模式零翻面（单卡面）。全库 verified 949→**1018**、suspect 52→**55**、pending 1959→**1887**。
4. **findings 登记（真差异）**：165→168 条，`D4_quote_mismatch` 24→27（+3：M-WB-003 / M-WB-004 / M-WB-008，锚点在库引文内逐字可定位）。
5. **门禁四连全绿**：credibility_gate --hard-fail（存量 524 基线内 / 新增 0）、verify_findings --hard-fail（新增 0）、apply_verification_status --check（零漂移）、verify_source_links --hard-fail（0 坏链）。
6. **站链复跑 + 构建**：export→daily→preflight(data)→unified→gen_counts→npm build→apply_site_counts→preflight(dist) 全过；站面计数同步（可点链接引用 1230→1304）。
7. **独立核验**：`tools/verify_batch1_landing.py --with-gates` **20 PASS / 0 FAIL**。
8. **零越界**：未动素材包外任何模式的判定；R9 两卡（elcano）为 M-AZJ/M-SHF 20 条打的自定义印记被状态工具覆盖后**已从备份原样回填**（§6）。

## 1. 前置预检

| 项 | 实测 |
| --- | --- |
| 工作仓 | `/opt/data/workspace/Protreptic`（HEAD `bf52ee4c` 起点） |
| 单写者 | 写窗口内在跑卡 = pigafetta×3（W4/R9 文档归档·只镜像）；数据面写者仅本卡（t_0dc95522 排队未启动） |
| 备份 | `data/backup_merge_W8B1_20260924_113742/`（5 件 + MANIFEST.json，sha256 逐件登记；不入库、parity 排除） |
| 幂等 | `tools/apply_w8_stage2_batch1_landing.py` 干跑→写盘；重跑=ABORT（冲突）或跳过（已一致），实测重跑 +0 key/+0 条 |

备份清单（落盘前 sha16）：`modes_data.json 6f3f4580397614f5`、`source_links.json 9df3d1fd210b2926`、
`source_texts.json c4aba5ff870f375e`、`findings.json b73e32806f7c910b`、`verification_status.json 32661224820d4230`。

## 2. 逐条处置（素材包 154 条 · 136 mode）

### 2.1 处置口径（三条）

- **已核条目（quote 3 + variant 22 = 25 条）：不改字。** 逐字/繁简/节引对读结论入账本，见证位（`evidence.file` + `snippet`）逐条随行；素材包未给出处置建议，库内引文与底本差异均为繁简、节引、标点级（对读后命中），无见证支持的改字一律不做。
- **查无条目（null 55 条）：不改引文，逐条登记类别（源外/近似/无近似/否定记录）。** D4 判定按既有实现（`credibility_gate.d4_scan`）复算：批1 查无条目绝大多数落入 D4「不可核」档（quote-too-short / script-mismatch / cache-not-ok），按「如实不可核」口径登记——**不假装核过，也不虚报不符**；真差异仅 3 条（§2.3）。
- **跨语言条目（74 条）：不建链接、不改状态、留语义对照档。** 中文引文对非中文原文（英/古希腊/法文）不适用逐字对读，口径待船长裁定（§8-1）；本卡不动 source_links、不动四态。

### 2.2 分类统计（账本 `dispositions_summary`）

| 处置类别 | 条数 |
| --- | --- |
| 核中·逐字（不改字） | 3 |
| 核中·繁简对读（不改字） | 18 |
| 核中·节引/标点差（不改字） | 4 |
| 查无·待核（近似档） | 26 |
| 查无·待核（无近似命中） | 13 |
| 查无·源外（王弼他著，非本底本） | 4 |
| 查无·源外（对策类，源在漢書卷056） | 4 |
| 否定记录·无合法全文源（未抓，不伪造） | 8 |
| 跨语言·语义对照（待裁定） | 74 |
| **合计** | **154** |

书级备注（抓取通道/覆盖/查无主因）见账本 `books`（18 行）与素材包 §七。

### 2.3 三条 D4 真差异（findings 登记）

| mode | 出处 | 登记结论 | 说明 |
| --- | --- | --- | --- |
| M-WB-003 | 《老子注》 | D4_quote_mismatch | 引文出自《老子指略》（王弼他著，非本底本收录）：按出处《老子注》字面判定登记（源外），待复核 |
| M-WB-004 | 《老子注》 | D4_quote_mismatch | 底本繁体/引文简体；素材包为「繁简对读命中（去冠名后）」，D4 按全文含冠名做字面判定判不符——两者判定对象范围不同，均指向复核；复核时以素材包见证为准 |
| M-WB-008 | 《老子注》 | D4_quote_mismatch | 三十八章撮述（改写档），底本无逐字段落；登记为待复核 |

处置：S1 规则下三模式状态 `pending→suspect`；findings 条目含锚点（`anchor`）与证据，`verify_findings` 全量锚点可定位（§4）。

### 2.4 为什么全批「零改字」

- 已核 25 条的差异全部是**对读级**差异（繁简/节引/标点），引文与底本实质一致；
- 查无 55 条属于**源外或底本限制**（非伪引）：王弼他著 8、对策类 4、异体字/节录受限（庄子注 6）等，改字没有底本依据；
- 素材包（W8-2）未给出逐条处置建议、本卡无新增抓取 → 不做无见证支持的改动（W5 先例：缺见证支持的改动一律不做）；
- 结果：库内引文面**零改动**（`key_quote_zh` 未增删改），改动集中在链接/缓存/状态/findings 四处，逐条可对账。

## 3. 链接入库与缓存合并

**链接**（8 部中文书；`fetch_mode`/coverage 取批1 缓存索引，confidence 同 W5 先例 0.9）：

```
《春秋繁露》      ok     complete    https://zh.wikisource.org/wiki/春秋繁露
《陆九渊集》      ok     complete    .../象山先生全集_(四部叢刊本)
《庄子注》        ok     complete    .../莊子注_(四庫全書本)
《老子注》        ok     complete    .../道德經_(王弼本)        (single-page)
《河南程氏遗书》  ok     complete    .../二程遺書
《二程遗书》      ok     complete    .../二程遺書（同源同文件）
《文史通义》      ok     complete    .../文史通義
《太极图说》      index-page complete .../太極圖說（MIN_CHARS 阈值误标；对照按全文）
```

- 链接存活实测（run 时）：6/8 `[OK 200]`；《文史通义》《太极图说》当时 `UNREACHABLE`（连接层抖动，策略内为警告非坏链）→ 立即 curl 重试**均回 200**（§附录 A.3）。
- 跨语言 9 部书**零链接**（口径待裁定）：理想国 / 俄狄浦斯王 / 伊利亚特 / 奥德赛 / 战争史 / 形而上学 / 奥林匹克回忆录 / 诗学 / 安提戈涅。

**缓存**（17 条 = 16 部书 + 二程同源一文件）：并入 `data/audit/source_texts.json`，`sha256`/`file`/`coverage`/`zh_cn` 元数据原样；D4 链唯一入口自此可判全书为繁体/异体者（批1 新增可核 key 16 个，总可核 39→55）。

## 4. 门禁与四态

### 4.1 门禁四连（重跑）

| 门 | 结果 |
| --- | --- |
| `credibility_gate.py --hard-fail` | exit 0；存量 524（基线内，冻结）/ **新增 0**；警告 28（D4/D5，均非阻断） |
| `verify_findings.py --hard-fail` | exit 0；基线内 0 / **新增 0**；警告 1（M-ASM 重复收割，历史基线） |
| `apply_verification_status.py --check` | exit 0；**逐条零漂移**（自洽：四态求和=3311；verified 证据回查 153 url） |
| `verify_source_links.py --hard-fail` | exit 0；146 OK / **0 dead** / 32 unreachable（策略内警告）/ 213 unverifiable |

D4 面（`credibility_gate` 现算）：缓存可用 key **55**（+16）；参与判定 3331；matched **11**（+7）、mismatch **27**（+3）、quote-too-short 117、unchecked 3176。

### 4.2 四态变化（before → after）

| 口径 | verified | pending | suspect | unverifiable | 合计 |
| --- | --- | --- | --- | --- | --- |
| 全库（3311） | 949 → **1018** | 1959 → **1887** | 52 → **55** | 351 → 351 | 3311 |
| 公开（3251，隔离 60） | 949 → **1018** | 1927 → **1855** | 35 → **38** | 340 → 340 | 3251 |

翻面来源：8 部中文书链接入库后 69 条 pending 解析到可达链接（S2=link-resolved）；3 条 D4 命中转 suspect（S1 优先）。**包外模式零翻面**（`verify_batch1_landing` ⑩）。

### 4.3 站面计数同步（`web/src/generated/siteCounts.ts`，构建前注入）

| 项 | before → after |
| --- | --- |
| 已核验（发布口径） | 949 → **1018** |
| 待核验（发布口径） | 1917 → **1845** |
| 存疑（发布口径） | 35 → **38** |
| 带引文模式有链接 | 974 → **1046**（+72 = 批1 CN mode 数） |
| 可点引用 / 未解析引用 | 1230/2336 → **1304/2262** |

## 5. 站链复跑（五步 + 数据面同步 + 构建）

1. `export_static_site.py` → 1357 文件；figures 1027 / modes(源) 3301 / published 3241 / by-figure 320；隔离命中 0。
2. `build_daily_index.py` → 3241 条 / 320 位 / 分片 320。
3. `pages_preflight.py --stage data` → 全过。
4. `build_unified_index.py` → 1344（figures 320 / scenarios 1024）。
5. `gen_web_site_counts.py` → siteCounts.ts 更新（§4.3）。
6. `cd web && npm run build`（vue-tsc + vite）→ OK（dist/assets 重新内联计数）。
7. `apply_site_counts.py` → manifest 一致；**dist 1378 文件零违规；docs 产品门面页 6 个零违规**。
8. `pages_preflight.py --stage dist` → 全过（index/404 逐字节相同）。

## 6. 工具行为观察（他卡印记保护）

`tools/apply_verification_status.py --write` 会**重建全部** verification 块。本卡实测：它把 R9 两卡（elcano）为
M-AZJ-001~010 / M-SHF-001~010 写的自定义块（`method=phase21r9-*-landing` + 素材包证据串）覆盖为通用
`auto-scan` 块。本卡处理：状态写盘后立即以**备份回填**（`apply_w8_stage2_batch1_landing.py --preserve-stamps`；
规则 = 状态未变而块内容变化者原样恢复，仅 20 条命中，逐条留痕），回填后 `--check` 仍零漂移（该检查只比 status）。
同时回填了 `verification_status.json` 报告里过期的输入哈希（`--refresh-status-report`）。

建议（不本卡实施）：给 `apply_verification_status.py` 增加「含自定义 method 的条目跳过重写」选项，避免同类覆盖（另立卡）。

## 7. 提交与镜像（提交后见 §9 回执）

- 工作仓：本卡白名单选择性提交（不动他卡在制件）。
- 发布仓 `/opt/data/release/Protreptic-publish`：镜像件 = **本卡白名单 + W8 链落盘包（W8-1/W8-2 的 docs/data/缓存/工具）+ 本报告/账本/证据**，逐件 sha256 byte-exact。
- push 后 `ls-remote` 复核回执。

## 8. 残留与待裁定

1. **跨语言 74 条口径待船长裁定**（不建链接/不改状态为当前冻结态；语义对照档 = 账本逐条 + 素材包 note）。
2. 庄子注 6 条查无受四庫异体字/SKchar 限制；改写档是否另立卡或改判待核（素材包残留 ②）。
3. 太极图说 `index-page` 误标（MIN_CHARS 阈值）——本卡未动工具阈值（越界）；如需 D4 可核另立小卡。
4. 源外 8 条（《老子指略》/《周易略例》4 + 《举贤良对策》4）可按需另抓底本（另立卡）。
5. M-WB-004 复核建议：繁简守卫（N5）配对阈值偏保守，去冠名后应可判 matched（登记为待复核，不改现状）。
6. `apply_verification_status` 块覆盖行为（§6）。

## 附录 A：证据 JSON
`docs/research/phase21w8_stage2_batch1_landing_evidence.json`（输入/产物 sha256、门禁输出、站链、核验 20 PASS、镜像/push 回执）。

## 附录 B：文件 SHA256（落盘前 → 后）

| 文件 | before sha16 | after sha16 |
| --- | --- | --- |
| data/modes_data.json | 6f3f4580397614f5 | 75932c9f2d48d136 |
| data/source_links.json | 9df3d1fd210b2926 | dc0aebf0c2bbdadc |
| data/audit/source_texts.json | c4aba5ff870f375e | daf6d882907126a5 |
| data/audit/findings.json | b73e32806f7c910b | 0292f0580ab03293 |
| data/audit/verification_status.json | 32661224820d4230 | 22944f54fb5e51a2 |
| web/src/generated/siteCounts.ts | 4e8e99110830a807 | a698abe698bb3db3 |
| data/audit/phase21w8_stage2_batch1_landing_ledger.json | — | 84ff028da6bee8d4 |

## 附录 C：新增/改动工具

- `tools/apply_w8_stage2_batch1_landing.py`（新增；链接入库 + 缓存合并 + `--preserve-stamps` + `--refresh-status-report`，幂等）
- `tools/build_batch1_landing_ledger.py`（新增；154 条账本生成 + 自检）
- `tools/verify_batch1_landing.py`（新增；20 项独立核验，`--with-gates` 复跑门禁）

## 9. 提交回执（最终）

### 工作仓（/opt/data/workspace/Protreptic；本地 master 无远端上游，按惯例不 push）

- **落地主提交：`004332b4`**「Phase21-W8 Stage2批1 t_b85ae14a 主库落地…」= 13 件白名单（数据 5 + 账本 + siteCounts + static_data_manifest + 报告/证据 + 3 工具；提交 stat 名单外 0）。
- 提交后复核：modes_data 相对父提交变更块 = **72**（69 verified + 3 suspect；包外 0；M-AZJ/M-SHF 20 条 elcano 印记零改动）；findings 仅 +3 条 D4_quote_mismatch。
- 回执补记提交：本文件 §9 更新与证据镜面刷新随第二次提交入库（sha 见 git log / 看板回执）。

### 发布仓（/opt/data/release/Protreptic-publish → origin/main = github.com/ovmobilegroup/protreptic）

- **镜像提交：`023a794`**「镜像: Phase21-W8 Stage2批1 t_b85ae14a 主库落地（对齐工作仓 004332b4）」= **50 件 byte-exact**（本卡 13 件 + W8 链落盘包 37 件：批1 缓存 23 txt / 索引 / 素材包与书单 / recount / submission / 6 工具 / w8 manifest）；staged 50 与清单逐件相等，名单外 0。
- **push：`7f03402..023a794  main -> main`**（git push 输出）。
- **ls-remote 复核：`023a79488b94c779d44e882590384cddbabfc792 refs/heads/main` == 本地 HEAD**（一致）。

### parity 复跑（tools/check_repo_parity.py --json）

- 本链面：**W8 链 42 项 diff 全部闭合**；**新增 diff 0**。
- 余项 2（`docs/research/candidates_v5_research.md`、`docs/research/phase21w10_coverage_report.md`）= **他链在制件**（W10 / candidates 链各自镜像），非本卡面。
- 边界面：both_sides **2577 件全数 identical**（工作仓 vs 发布仓逐件 sha256 相等）。

### 独立核验与链接存活

- `tools/verify_batch1_landing.py --with-gates` → **20 PASS / 0 FAIL**（含 credibility_gate / verify_findings / --check / preflight 四连复跑 rc=0）。
- 链接存活：run 时 6/8 `OK 200`；《文史通义》《太极图说》unreachable（连接层抖动）经 curl 重试**回 200**（见证据 JSON `link_liveness`）。
