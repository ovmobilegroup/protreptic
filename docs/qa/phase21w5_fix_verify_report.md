# Phase21 W5「修复·独立复验」报告（卡 t_30d57ff2）

- 卡：`t_30d57ff2`（espinosa）｜上游＝数据修复卡 `t_0dc95522`（done）｜下游＝文书侧卡 `t_bda44643`（本卡 done 后放行）
- 口径：**不采信任何自述**；一切判定取自 git 对象、盘上文件、工具现跑。复核时工作仓 HEAD=`b5967043`（W8 QA 卡 `t_e727be57` 于本卡执行期间提交——非本卡面，未触碰）；本卡面提交 `3238a262`/`77931445` 均为 HEAD 祖先；发布仓 `/opt/data/release/Protreptic-publish`。
- **结论：PASS**（逐项判定表见 §1；登记更正项 3 条见 §5；交付物提交/镜像/push 回执见 §7）。
- 一句话：10 条处置逐条实落（20 处字段改动＋4 条注记，三面一致、全库零越界）；zh_cn 副本＝工具如实产物且重建可复现、元数据如实、写/读口防线成立；四门禁现跑与修复卡冻结输出逐字节一致；006/008/009 结论链两向推演成立；C1/P1/C2/P2 镜像 byte-exact、parity 现跑零差异。发现的 3 处差异全在**报告表述/数字**层面（低危，§5 登记），不影响数据终态与门禁结论。

## 1. 逐项判定表

| # | 核验项 | 判定 | 关键证据（全部现跑，见 §2） |
|---|---|---|---|
| 1 | 10 条处置落盘逐条核验 | **PASS**（附 3 处定位取词口径差登记） | git 对象 diff＝20 处字段改动（md 11/ind 7/fg 2）＋1 处已登记的状态翻转；全库扫描仅 9 条 M-WC 条目变化、非 M-WC 变化 0；每处新文本均定位到见证（底本/抽本/副本 16 点中 15 点逐列一致＋1 点 needle 宽度差；章节边界 7/7 落体内） |
| 2 | zh_cn 元数据（如实/采用一致/无再硬写） | **PASS** | 落盘副本＝工具产物逐字节相等（d26e86f4）；独立重建逐字节复现；3 回退块清零、証 3→0；chunks 34/failed 0/complete true 与文件实测一致；读口注入 4/4 拒用正确（含事故形态 complete&failed>0） |
| 3 | 重跑复核（四门禁＋四态自洽） | **PASS**（附警告数表述差 1 条登记） | gate exit 0 / warnings 27、D4 11-26-118-3176；verify_findings exit 0 新增 0；avs --check exit 0 无漂移；t45 37/38（仅 Z7 存量）；四态 1019/1887/54/351（3311）与公开 3251＋隔离 60 两口径独立复算自洽 |
| 4 | M-WC-006/008/009 结论链 | **PASS** | 旗标终态＝完整 → 沿用：gate d4_scan 006=matched(copy)/008=matched(copy)/009=quote-too-short；反事实注入不完整态 → 拒用、006/008 降级 unchecked（与 U4 设计一致） |
| 5 | 提交/镜像/push 三件套 | **PASS** | C1 3238a262（11 件）、P1 ade87b2 11/11 byte-exact；C2 77931445、P2 58f361d 2/2 byte-exact；两提交均为 origin/main 祖先；parity 现跑零差异（2583/2583） |
| 6 | 报告数字与 git 实况抽查 | **PASS（附登记）** | 抽查 30+ 项：C1/C2/P1/P2、11 件、1123/235、findings 168→167、D4 27→26、四态前后、gate 28→27、t45、artifact sha 10/10、status inputs 3 sha、幂等 4 项——全部对齐；3 处低危差异见 §5 |
| 7 | R8 勘误（§0 概数 9 vs §2 表列 10） | **完成** | 勘误附注已增补至 `docs/qa/phase21w5_wangchong_qa_report.md` 文末（原文未改；依据＝§2 表 10 行：真差异 6＋口径差 4） |

## 2. 逐项证据明细

### 2.1 项 1：10 条处置落盘（git 对象＋见证）

- 比对基准：`b8be2986`（C1 父提交）到 `3238a262`（C1）。全库 3311 条模式结构 diff：
  - 变化条目＝9 条（M-WC-002…010；M-WC-001 按卡未改字）；字段级改动 21 处＝**20 处处置字段**（md 11 / ind 7 / fg 2）＋1 处 `verification` 翻转（M-WC-009 suspect->verified，属四态重跑应用变更，已在 §四 status json `changes_vs_library` 登记）。
  - 20 处与证据 JSON `A_changes.items` 逐字一致（file/id/field/before/after 全同；`changes_table.json` 同）。
  - 注记实测＝**4 条**（md：`correction_zh` x1 @002 ＋ `key_quote_context_zh` x3 @005/007/010）；005/007/010 引文未替换（仅注记并登记 A1 候选）；与卡 7) 及 A1「标存疑＋注记」一致。
- 无越界：非 M-WC 条目变化 0；顶层非 modes 块变化 0；figures 结构 diff 仅 2 处 source_chapter；individuals 结构 diff 仅 7 处（引文 5＋篇目 2）；findings 168 减到 167（移除 1＝M-WC-009 旧锚、新增 0；summary 仅 D4_quote_mismatch 27 减到 26 与 total）；source_texts.json 仅《论衡》zh_cn 的 4 个字段（chunks/converted_at/sha256/chars）。
- 见证定位（我独立计算 行:列/偏移，与报告及证据对照）：
  - 底本/副本 16 点：15 点逐列一致；差异 1 点＝004 取词宽度（证据 needle「莫明於」在 2573:335 / 全句「事莫明於有效」起点 2573:334——同一位置同一依据）。
  - 抽本（witness/raw）7 点：5 点逐列一致；差异 2 点＝67: 10:346（取「莫明於」）vs 10:345（全句）；66: 10:95（取「皆稟元氣」）vs 10:90（全句）——均属 needle 取词口径（短词起点），见证存在性不受影响。
  - 章节边界：7/7 见证偏移落于所声称章节体内（/23 62083 在 [58162,62610) 内；/28 79696 在 [79691,88011) 内；/54 163043、163532 在 [163043,166738) 内；/62 187616 在 [186283,190359) 内；/66 205510 在 [205423,207248) 内；/67 207581 在 [207248,209191) 内）。
- 无证据改字：20 处 after 全部有见证；002「追」来自底本校改标记 `（迢）〔追〕`（底本与副本两侧校勘符号均保留、未抹除；该条 D4 为 quote-too-short，不受形态影响）。
- A1 依据对照（`docs/research/phase21w5_wangchong_sourcing_report.md` §二）：002/003/004/006/008/009 与 A1 处置建议一致；005/007/010 注记文案与 A1「查无＋候选」逐项对应；004「《证验》篇名不存在、该句出自《薄葬篇第六十七》」经复核（85 章名表无证验；该句位于 /67 体内）。
- 附：R8 QA 断言复跑脚本现跑（`verify_wangchong_pilot_qa_espinosa.py`）＝OK 2 / REPRO 9 / UNEXPECTED 10——UNEXPECTED 全部为「数据已被修复」的预期翻转（含「10 条引文/篇目已与基线不同」、副本 sha/旗标、回退块、証残留、四态）；REPRO 9 项全部属于 **landing 历史文档**面（改述类），均在下游文书侧卡 `t_bda44643` 修订清单内（逐条映射：A1/A2/A3/A4/A6/B/tee）。

### 2.2 项 2：zh_cn 转换副本与元数据

- 「元数据 vs 工具如实产物」对测：修复卡 scratch 产物 `new_zhcn.txt` 与落盘副本 `data/audit/source_texts/6f2e2e4e124df80a.zh-cn.txt` **逐字节相等**（sha256 `d26e86f4…`、789872 B、265736 字符）。
- 重建可复现（我独立复算）：以备份旧副本替换 3 区间 [79745,87745)/[167803,175803)/[255883,263883) 为新重转块（chunk_10/21/32_new.txt，各 8008 字符），重建结果与落盘副本**逐字节相等**；3 个旧回退块与 raw 对应切片逐字节相等（真回退）；新块可与 raw 区分（真转换）；`証` 3 降到 0、`证` 20 升到 24。
- 元数据如实：chunks=34（=ceil(265736/8000)）、failed_chunks=0、complete=true、converted_at=2026-09-24T04:17:22+00:00、chars/sha 与盘上文件实测一致；E 自检 W5 盘上实测 5 条 zh_cn 条目 0 违规（含逐条 sha/chars 复算）。
- 采用一致性（U4）＋注入探针（现跑）：`converted_text_for()` 现要求 complete 且 failed_chunks==0；注入 `complete=true&failed=3`（R8 事故形态）拒用（None）；`complete=false` 拒用；failed 不可解析拒用；正常条目取到 TEXT(210848)。gate 现跑该副本被采用（copy 命中 9 条，含 M-WC-006/008）。
- 无再硬写：工具 diff 仅「写口断言三件套＋自检旗标（fetch_source_texts.py，+97 行）」与「读侧 failed_chunks==0 加固（source_text_cache.py，9 行）」；元数据取值全部来自计算（sha/chars 由产物算出、chunks 由分块常数、converted_at 由转换时刻）；`--self-check-zh-cn-meta` 现跑 5/5 PASS（含两条负向注入必炸）。

### 2.3 项 3：重跑复核（四门禁）与四态

- 现跑输出（scratch rerun/，与 t_0dc95522 frozen_* 输出**逐字节一致**）：
  - `credibility_gate.py --hard-fail`：**exit 0**；存量 524 冻结、新增 0；warnings(D4/D5) **28 降到 27**；D4 matched 11 / mismatch **27 降到 26** / quote-too-short 117 升到 118 / unchecked 3176；副本理由：found 9 / not-found 2 降到 1（剩 1＝M-WB-008《老子注》面）。
  - `verify_findings.py --hard-fail`：**exit 0**；hard 0、新增 0；基线 total=0（冻结位 2026-09-19T15:20:44+00:00）；其他警告 2 条（M-ASM 双收 存量；audit_meta.modes_file_sha256 滞后——见 §5）。
  - `apply_verification_status.py --check`：**exit 0**；「库中状态与本规则逐条一致」、无漂移。
  - `test_credibility_d45.py`：**37/38**；唯一 FAIL＝Z7（backfill_lifespans 清单 476 vs 576，存量，归 W11 卡 t_0ec6fb57）。
- 四态两口径（我独立复算，独立于工具）：全库 verified 1019 / pending 1887 / suspect 54 / unverifiable 351，和=3311；公开 1019/1855/37/340，和=3251；隔离 60；3251+60=3311。与工具逐值一致；S1 交 S2 重叠 28 降到 27；verified evidence URL 153 个。

### 2.4 项 4：M-WC-006/008/009 结论链（按旗标终态推演）

- 推演（完整 -> 沿用）：现盘 zh_cn complete=true 且 failed_chunks=0，且副本实测为真完整（0 回退块）⇒ 沿用：gate d4_scan 现跑 006=matched（substring-found(zh-cn converted copy)，detail 人未生在元气之中）、008=matched（copy，detail 以为贤圣所言皆无非）、009=quote-too-short（all-fragments-shorter-than-min(8)）。
- 第二实现复核（我自写归一化＋片段切分，独立于工具实现）：006 可用片段「人未生在元气之中」（copy 命中、raw 不命中）；008 可用片段「以为贤圣所言皆无非」（copy 命中、raw 不命中）；009 无 8 字以上片段 -> quote-too-short。结论一致。
- 反事实推演（不完整 -> 降级）：注入 complete=true&failed_chunks=3 或 complete=false -> converted_text_for 拒用 -> 006/008 落 script-mismatch -> unchecked（降级）；009 亦不会经副本比对。与 U4 设计及 R8 QA §3.1(2) 倒查要求一致。
- 与 t_0dc95522 实况对照：现盘＝沿用态；报告 §二.6／证据 `d4_conclusion_chain`／gate 计数（copy found 9 / not-found 1；剩 1 条＝M-WB-008，非论衡面）全部一致。

### 2.5 项 5：提交／镜像／push／parity

- 工作仓：C1=`3238a262`（11 件＝7 data＋2 tools＋2 文档；1123 insertions／235 deletions）；C2=`77931445`（2 件刷面）；对象存在，盘上文件与 C1/C2 blob 逐字节一致（无漂移；复核期间 W5 面文件未被任何卡触碰）。
- 发布仓：P1=`ade87b2` 与 C1 逐件「11/11 byte-exact」；P2=`58f361d` 与 C2「2/2 byte-exact」；父提交 `20d36f0` 存在。
- push／ls-remote：现跑 ls-remote＝`88cc86a`（＝本地 publish HEAD；`88cc86a` 为 W8 QA 卡 t_e727be57 的镜像提交，晚于本卡回执时点；本卡两笔 push `20d36f0..ade87b2`、`ade87b2..58f361d` 的落地由祖先链 88cc86a->58f361d->ade87b2->20d36f0 证明）。
- parity 现跑（tools/check_repo_parity.py）：**零差异**（both_sides 2583／identical 2583／单侧 0；exit 0）。修复卡 §七「本卡面 CONTENT_DIFF=0（0/11）、MISSING=0（0/11）」经我逐件跨仓 sha256 复核对齐（11/11＋回执轮 2/2）；其记录的 parity 残余 3 项（W8 批1 面在途件）已由 W8 QA 卡提交并镜像收口（非本卡面）。
- 备份目录 data/backup_merge_W5FIX_20260924_121533 存在（未入库，与声明一致）。

### 2.6 项 6：报告数字抽查（30+ 项）与登记差异

- 全部对齐项（抽查）：C1/C2/P1/P2 sha、11 件清单、1123/235、findings 168->167、D4 mismatch 27->26、四态前后（1018/1887/55/351 -> 1019/1887/54/351；公开 suspect 38->37）、gate warnings 28->27、t45 37/38、artifact sha 10/10（modes 736aab3b、findings 5527607、status 7da1810d、副本 d26e86f4、tools 两件、报告/证据）、status json inputs 3 sha＋counts（modes bytes 24894309、source_links 391/178/172、findings d4_d5_modes 54）、§六 幂等 4 项（land_ten SET=0/SKIP=20 与 restore_marks RESTORED=0 经只读复算复核；apply_zhcn ALREADY 由脚本逻辑＋终态核验；avs 复跑 exit 0）。
- 登记差异 3 条（低危，详见 §5）：(a) verify_findings 警告数；(b) 注记条数 4 vs 五条；(c) 定位取词口径 2 处。
- 备注：修复卡 §七 记录的「ls-remote=58f361d／parity 2581/2578」为**时点态**；其后远端已推进至 88cc86a（他卡镜像）、parity 边界文件数随 W8 QA 提交增至 2583——均属外部推进，与回执时点陈述相容。

## 3. R8 勘误（项 7）

- 已增补「勘误附注」于 `docs/qa/phase21w5_wangchong_qa_report.md` 文末（原文一字未改；勘误附注为唯一增补）。
- 内容：§0 概数「9 条（真差异 6／口径差 3）」与 §2 表列 10 行（真差异 6／口径差 4）不一致；勘误为「10 条：真差异 6、口径差 4」；依据＝表行计数（#1…#10）与「类别」列逐行取值。
- 随本卡提交并镜像发布仓（回执见 §7）。

## 4. 结论

- **总判定：PASS。** 数据终态、工具防线、门禁、结论链、提交／镜像／push 五面全部成立且可独立复现。
- 登记更正项 3 条（§5）均在**报告表述／数字层面**（低危），不影响任何数据文件、门禁 exit 与结论链；供船长路由至文书侧／后续卡顺带更正。
- 本卡边界：只读复验＋本报告／证据／勘误三件文书交付；未改任何 data/**（复核期零数据写入）。

## 5. 登记更正项（供船长路由；低危）

1. 【fix_data_report §零 行】verify_findings「警告 1（M-ASM 双收，存量）」——实测为**2 条**（M-ASM 双收 存量 ＋ audit_meta.modes_file_sha256 滞后：由本卡自身写入序列「先重跑 findings、后 avs --write」产生，属非阻断警告）。建议：更正为 2 条并注明第二条成因；可选后续卡以 build_audit_findings.py --write 刷新 audit_meta 使归零（或登记为已知形态）。
2. 【fix_data_report §一／kanban 交接 metadata】注记条数：§一 同段「4 条注记」与「五条注记」自相矛盾；实测与证据 JSON `notes_added` 均为 **4 条**（md correction_zh x1 ＋ key_quote_context_zh x3）。建议以 4 条统一。
3. 【fix_data_report §一 表／evidence 定位列】取词口径差 2 处：004 底本列 2573:335（取「莫明於」）vs 全句起点 2573:334；006 抽本列 10:95（取「皆稟元氣」）vs 全句 10:90。同一位置、见证与依据不变。建议统一标注 needle 或加口径说明。

## 6. 复现命令（只读）

- 本卡脚本与输出：`/opt/data/profiles/espinosa/cache/scratch/t30d57ff2/`（diff_faces.py、wholelib2.py、verify_witness.py、verify_chain.py、rebuild_verify.py、fourstate.py、mirror_check.py、status_and_sha.py；rerun/ 四门禁与 R8 复跑输出）。
- 关键命令（仓库根）：
  - python3 tools/credibility_gate.py --hard-fail
  - python3 tools/verify_findings.py --hard-fail
  - python3 tools/apply_verification_status.py --check
  - python3 tools/test_credibility_d45.py
  - python3 tools/fetch_source_texts.py --self-check-zh-cn-meta
  - python3 tools/check_repo_parity.py
