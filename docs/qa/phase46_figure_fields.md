# Phase46-R: figure 文件字段缺陷审计与修复

- 卡片: t_e3f8cf8f (Phase46-R figure 文件字段缺陷审计与修复)
- 执行人: bustamante (Hermes kanban worker)
- 时间: 2026-09-21 (CST)
- 工作仓: /opt/data/workspace/Protreptic (分支 master, 本地开发分支, 无 upstream, 不作为上线来源)
- 发布仓: /opt/data/release/Protreptic-publish (分支 main, 线上唯一来源)
- 工具: tools/audit_figure_fields.py (审计), tools/fix_figure_fields.py (修复)
- 产物:
  - data/audit/figure_field_defects.json (修前审计: 四类缺陷逐文件记录 + 修复建议)
  - data/audit/figure_field_defects_after.json (修后复跑, 同一工具同一口径)
  - data/audit/figure_field_fix_manifest.json (逐文件 old -> new + 修前修后 sha256 + 每个值的文件内证据)

## 0 结论

PASS (口径: 只修字段, 不新增/删除人物内容, 引用零丢失)。四条硬判据, 全部有命令与原始输出:

1. mode -> figure 一致性自检: 模式侧无法定位的 figure_code 修前修后完全相同, 都是 34 个 code / 340 条模式 (见第 3.1 节)。本次改动没有让任何一条模式失去 figure 主体或生卒年: 丢失的取值键 150 个, 其中被模式引用的 0 个。
2. 可信度门 (CI 里 --hard-fail 那一步): exit 0; 输出与修前逐字符比对只差 2 行统计口径 (扫到的文件数, 可用取值键数), D5 判定结果 (可判定 2318 / conflict 1 / clean 1341 / undetermined 1546 / 命中 1) 与 D1/D2/D3/D6 计数完全不变 (见第 3.2 节)。
3. tools/backfill_lifespans.py 现场重算: modes_covered 2318, mode_figures_covered 230, still_no_date 55 三个口径全部不变 (见第 3.3 节)。
4. 两仓 parity: python3 tools/check_repo_parity.py 零差异 (见第 8 节)。

四类缺陷计数 (修前 -> 修后):

| 缺陷类 | 修前 | 修后 | 剩余项去向 |
| --- | --- | --- | --- |
| empty_name | 33 | 3 | 剩余 3 个全部是 *_modes.json 伴随模式包 (非 figure 文件), 见第 6 节第 2 条 |
| bad_figure_code | 223 | 1 | 剩余 1 个 H-WAT-001, 改它必丢引用, 列入待人工 (见第 5 节) |
| name_mismatch | 37 | 33 | 修掉 4 条 (3 个文件, 其中 1 对是逐字节重复件); 剩余 32 条是 detector 误报 (正文首句是身份描述语或同一人写法变体), 1 条待人工核名 |
| duplicate | 20 组 | 3 组 | 归档 17 个冗余件; 剩余 3 组 (2 组改 code 必动模式引用, 1 组同名且年份互斥) 列入待人工 |

## 1 审计口径 (写死在工具里, 可复核)

- 范围: data/figures/*.json 共 347 个 = 319 个 figure 文件 + 28 个 *_modes.json 伴随模式包。
- figure_code 规范值 = 文件名主干 H-CODE-001。依据: 仓库内已合规的 96 个文件, 250 个文件的 id 字段, 根 modes_data.json 的 figure 记录 code, 三者同形; 卡面第 2 条亦同。
- figure_name: 必须非空, 且与文件内证据 (正文首名 / figure_name_zh / name_zh / 拼音 / 英文名 / id 锚点) 一致。
- duplicate 判据 (两条并集): 归一化人名相同 或 人物名锚点相同 (figure_code 或 code 是拉丁人名, 排除 Modern / Han 一类时代词), 且内容逐字节相同或生卒年一致。
- 引用面 = tools/credibility_gate.py 的 figure_key_candidates(): code / id / figure_code / 文件名主干 四个位置登记的取值键; 改 figure_code 时若旧值仍被模式引用, 必须把旧值保留在 code 字段。

## 2 修复动作

### 2.1 字段级 (228 个文件, 逐条 old -> new 见 manifest)

empty_name 30 个 figure 文件: 回填 figure_name, 值全部来自文件内证据, 不加一个字:

- H-BG-001 -> 班固 (取 figure_name_zh)
- H-SW-001 -> 孙子 (取 figure_name_zh)
- H-JSX-001 -> 贾思勰 (该文件无 figure_name_zh / name_zh, 取 historical_significance 首名 "贾思勰(约480-约550)", 与模式侧 figure_name 一致)
- H-LZ-001 -> 李贽 (取 name_zh)
- 三个 *_modes.json 伴随包不在回填范围 (非 figure 文件), 见第 5 节

bad_figure_code 222 个文件: figure_code := 文件名主干。

- 朝代或时代当 code 的一律改掉: H-SW-001 战国 -> H-SW-001; H-BG-001 Han -> H-BG-001; H-AN-001 Modern -> H-AN-001; H-ZS-001 战国 -> H-ZS-001。
- 引用保护: 旧值若仍被模式引用, 就把旧值写进 code (credibility_gate 会登记 code 为取值键)。例 H-BAC-001: figure_code Bach -> H-BAC-001, 同时 code H-BAC-001 -> Bach, 于是模式侧 Bach (10 条) 与 H-BAC-001 (10 条) 两个键都还在。
- 少数文件的 code 与旧 figure_code 同时被模式引用时, code 只装得下一处, 于是整文件放弃: H-WAT-001 (WAT 与 Watt 各 10 条模式都在用) 列入待人工, 不半改。

name_mismatch 3 个文件 (4 条), 全部按文件内证据改:

- H-Mendel-001: 施耐庚 -> 孟德尔 (正文首句 "孟德尔(1822-1884), 奥地利奥古斯丁会修士, 遗传学之父")
- H-AlGhazali-001: 加括友 -> 阿斋逊 (正文首句 "阿斋逊(1058-1111), 伊斯兰黄金时代思想家"; 同人文件 H-GHZ-163.json 用正式名 "安萨里", 是否统一留待船长裁定, 见第 5 节)
- H-HEISENBERG-001 与 H-Heisenberg-001 (两份逐字节相同): 海瑞 -> 海森堡 (正文全文是 Werner Karl Heisenberg 1901-1976 与不确定原理, figure_pinyin 就是 He Sen Bei, 而 海瑞 是明代官员 1514-1587)

### 2.2 重复件归档 (17 个)

处置原则: 保留信息更全的一份 (字典序: 字节数 -> 键数 -> 有无模式载荷), 冗余件用 git mv 移到 data/figures/_duplicates/ (该目录不在任何 figures/*.json glob 内, 内容零丢失)。

| 归档件 (冗余) | 保留者 (更全) | 判据 |
| --- | --- | --- |
| H-Bach-001.json | H-BAC-001.json | 同一人 (Bach 1685-1750, 锚点同为 Bach); 保留件 94106 B 含 10 条模式, 冗余件 4364 B |
| H-DaVinci-001.json | H-DAV-001.json | 达芬奇 1452-1519; 90509 B vs 3426 B |
| H-Euler-001.json | H-EUL-001.json | 欧拉 1707-1783; 95189 B vs 9629 B |
| H-Feynman-001.json | H-FEYNMAN-001.json | 费曼; 两份逐字节相同, 取文件名规范的一份 |
| H-Gauss-001.json | H-GAU-001.json | 高斯 1777-1855; 97925 B vs 9852 B |
| H-Hawking-001.json | H-HAWKING-001.json | 霍金; 逐字节相同 |
| H-Heisenberg-001.json | H-HEISENBERG-001.json | 海森堡; 逐字节相同 (名字误写已在保留件上修正) |
| H-Hippocrates-001.json | H-HIPPOCRA-001.json | 希波克拉底; 逐字节相同 |
| H-LiShiMin-001.json | H-LISHIMIN-001.json | 李世民; 逐字节相同 |
| H-MarcoPolo-001.json | H-MARCOPOL-001.json | 马可波罗; 逐字节相同 |
| H-Nobel-001.json | H-NOB-001.json | 诺贝尔 1833-1896; 157335 B vs 6905 B |
| H-SJL-001.json | H-SHA-001.json | 商羯罗; 120419 B vs 42424 B (冗余件取值键 H-SJL-001 仍由其伴随包 H-SJL-001_modes.json 提供, 键面不丢) |
| H-Tokugawa-001.json | H-TOKUGAWA-001.json | 德川家康; 逐字节相同 |
| H-Watt-001.json | H-WAT-001.json | 瓦特; 82797 B vs 6018 B |
| H-WY-001.json | H-WYM-001.json | 王阳明 1472-1529; 18255 B vs 1702 B |
| H-XuGuangQi-001.json | H-XUGUANGQ-001.json | 徐光启; 逐字节相同 |
| H-ZS-001.json | H-ZX-001.json | 曾子; 24051 B vs 9565 B (冗余件取值键 H-ZS-001 与 战国 无任何模式在用, 实测可安全移走) |

归档件零丢失证明 (脚本逐件与 HEAD 版本比对 sha256): 17/17 全部 SAME, 无一例外。

## 3 引用面自检与验证证据

全部在本机实跑, 命令与原始输出如下。

### 3.1 取值键面与模式侧覆盖的对照 (引用零丢失的正面证据)

改动前的 figures 快照导出 (改动后 HEAD 已等于新状态, 故先把旧状态导出到临时目录):

```
mkdir -p /tmp/fig_before
for f in $(git -C /opt/data/workspace/Protreptic ls-tree --name-only <改动前提交>:data/figures); do
  git -C /opt/data/workspace/Protreptic show <改动前提交>:data/figures/$f > /tmp/fig_before/$f
done
python3 tools/check_figure_key_loss.py --before-dir /tmp/fig_before
```

输出:

```
gate 口径取值键: before 672 -> after 522
丢失键 150; 其中被模式引用 0 个 / 0 条模式
模式侧无法定位: before 34 个 code / 340 条模式 -> after 34 个 / 340 条
新增无法定位: []
结果: PASS(引用零丢失)
```

即: 150 个消失的取值键里, 被模式引用的 0 个; 模式侧无法定位的 figure_code 个数与条数一模一样。

### 3.2 可信度门 (CI 里跑的那一步)

```
python3 tools/credibility_gate.py --hard-fail     # 修前 / 修后各跑一次
```

两次都是 exit 0。两次输出 diff 全文只有 6 行变化, 全是 D5 的装载统计:

```
< 生卒年装载: data/figures/*.json 扫 347 个文件 -> 可用取值键 616 个; 年份不完整/不可解析 53 个文件; 键冲突丢弃 3 个键
<   键冲突丢弃: Modern ... vs ...
<   键冲突丢弃: Han    ... vs ...
> 生卒年装载: data/figures/*.json 扫 330 个文件 -> 可用取值键 476 个; 年份不完整/不可解析 52 个文件; 键冲突丢弃 1 个键
< 生卒年可用人物: 616 个
> 生卒年可用人物: 476 个
```

D5 判定结果四行 (可判定 2318 / conflict 1 / clean 1341 / undetermined 1546) 与 D1/D2/D3/D6 计数逐字符相同, D5 命中仍为 1 条。另外键冲突从 3 个降到 1 个: Modern 与 Han 两个"把时代词当 code"的冲突被规范化消除; 剩下的 H-MZ-001 与 H-MZ-001_modes.json 冲突是既有问题, 见第 5 节。

### 3.3 backfill_lifespans 现场重算 (工具自报口径)

```
python3 tools/backfill_lifespans.py
```

| 口径 | 修前 | 修后 |
| --- | --- | --- |
| modes_covered | 2318 | 2318 (不变) |
| mode_figures_covered | 230 | 230 (不变) |
| still_no_date | 55 (571 条模式) | 55 (570 条模式) |
| keys_available | 616 | 476 |
| files_without_usable_years | 53 | 52 |

三种主口径全不变, 即"能被生卒年判定的模式一条都没少"。

### 3.4 其它证据

- python3 tools/test_check_repo_parity.py -> 19/19 passed
- python3 tools/test_credibility_gate.py -> 6/6 passed
- 改动后 data/figures/*.json 全量 json.load -> 不可解析 0 个
- manifest 逐字段复核 (每个 proposed_fix 的落盘值) -> 不符 0 条
- 17 个归档件与改动前字节 sha256 比对 -> 17/17 SAME

## 4 指标变化的如实交代

本次改动唯一的指标代价是取值键面缩小, 原因已定位清楚, 不是引用丢失:

- 丢的 150 个键里, 被模式引用的 0 个。剩下 150 个全是"人名锚点键", 例如 Amundsen / Archimedes / Xenophon 这类只有 figure 文件自己在写、没有任何模式在查的写法。规范化后 figure_code 变成 H-XXX-001 形式, 这些无人引用的锚点自然消失。
- 反面: 有人引用的锚点全部保住了 (Bach / DaVinci / Euler / MarieCurie / WeiQing / Watt 等), 做法是把旧值写进 code 字段。
- 连带口径: keys_legacy (旧的一刀切取值口径) 从 266 升到 278; modes_covered_legacy 从 1132 降到 1118。后者正是"旧口径不可靠"的实例: 它按 figure_code -> code -> id 的顺序取第一个非空值, 规范化后同一个人的键换了位置, 它就少数出 14 条模式。判定一律以 figure_key_candidates 口径为准, 该口径下 2318 条不变。
- 另一处必须交代的变化: data/audit/lifespan_backfill.json 随之重新生成 (它是现场重算的派生清单, 不重算就会与库里数据自相矛盾)。

## 5 待人工裁决清单 (8 条, 脚本一律不动)

| # | 类型 | 对象 | 为什么脚本不动 | 建议 |
| --- | --- | --- | --- | --- |
| 1 | bad_figure_code | H-WAT-001.json | 取值键 WAT 与 Watt 各 10 条模式都在用, 而 code 字段只有一处可写, 改必丢一边 | 需要模式侧先把两套模式集合并 (见第 6 节), 或给 figure 文件加一个别名字段 |
| 2 | name_mismatch | H-YE-001.json | 声明名"叶筱", 但正文首名是"现代中国政治思考家"这种身份描述语, 文件内没有任何人名证据 | 需要船长给权威名与生卒年, 或整卡替换 |
| 3 | name_mismatch | H-AlGhazali-001.json | 已按正文改成"阿斋逊"(Ghazali 的音译变体), 但同人文件 H-GHZ-163.json 用的是"安萨里" | 建议统一为"安萨里", 由船长裁定后一次性改齐 |
| 4 | empty_name | H-DZS-001_modes.json | 伴随模式包不是 figure 文件, 卡面第 1 条是否含伴随包未明确 | 若要求覆盖伴随包, 需先定伴随包的字段规范 |
| 5 | empty_name | H-HZX-001_modes.json | 同上 | 同上 |
| 6 | empty_name | H-ZX-001_modes.json | 同上, 且该文件 name_zh 存的是"什么是XX"式标题, 不是人名 | 同上 |
| 7 | duplicate | H-MarieCurie-001.json | 其取值键 MarieCurie 仍被 10 条模式引用, 移走这些模式就找不到主体; 与 H-CUR-001 是同一人两套模式 | 与 #1 同一处方: 模式集合并卡 |
| 8 | duplicate | H-SQ-001.json / H-WeiQing-001.json | 同理: H-SQ-001 与 H-SMQ-001 (司马迁), H-WeiQing-001 与 H-SUN-001 (孙权) 各有一套被模式引用的模式集, 冗余文件不能直接移走 | 同上 |

## 6 与卡面前提不符 / 越出卡面范围的地方

1. 卡面说"206 个 figure_code 存的是朝代", 与实测不符: 实测非规范 223 个, 细分是 人名锚点 172 / 字段缺失 20 / 时代名 15 / 朝代 9 / 地点或时代 2 / 其它 5。卡面的 206 可能只统计了"人名锚点 + 朝代与时代名"一类口径。
2. 三个 *_modes.json 伴随模式包: 卡面第 1 条按"figure_name 为空的文件"统计会得到 33 个, 但其中 3 个是伴随模式包 (非 figure 文件)。本卡按 figure 文件口径修了 30 个, 伴随包列入待人工。
3. 34 个 figure_code (340 条模式) 在 data/figures 里没有任何主体文件: 这是上一张卡 (净缺人物候选池) 的同一批缺口, 本卡只做字段修复, 不新增人物文件。
4. 同一人物有两套模式集 (9 组): Bach/H-BAC-001, MarieCurie/H-CUR-001, DAV/DaVinci, EUL/Euler, GAU/Gauss, NOB/Nobel, H-SQ-001/H-SMQ-001, WeiQing/H-SUN-001, WAT/Watt。两边的取值键都在被模式引用, 所以本卡只归档"键面不重叠"的冗余件; 这 9 组需要一张新卡做"模式集合并 + code 统一"。
5. H-MZ-001 键冲突 (既有, 未动): H-MZ-001.json (墨子, 记录的生卒年 1890-1990) 与 H-MZ-001_modes.json (公元前 372-289) 同名同键但生卒年互斥, 其中一份年份大概率是错的。本卡不改人物内容, 仅记录。
6. 其它数据质量存疑 (已记录未动): H-HAN-001 (沈幅 / Shen Fu, 记录生卒年 -100 至 180 与人物不吻合, 疑似沈复), H-ZS-001 正文把卒年写成 1630 年 (锚点 -435), H-YE-001 见第 5 节。

## 7 未做的事

- 没有改任何人物叙述、生卒年、模式内容。
- 没有新增或删除人物 (34 个缺口不凭空补)。
- 没有把 figure_code 规范化推广到其它目录 (data/individuals 等), 卡面只要求 figures 这一层。

## 8 双仓同步与 CI 自检

- 工作仓提交: 3780e43b (master)
- 发布仓提交: fefc79b (同步 figure 修复) + 8b238f1 (仅回滚一条误入的 web/dist 构建产物改动)
- 同步方式: 按工作仓提交的 name-status 逐路径复制或删除 (A/M 复制, R 拆成 删除 + 新增), 不用 rsync 整目录, 避免把开发侧杂物带进发布仓
- 同步后自检: python3 tools/check_repo_parity.py 输出 "两仓都有 1446 条 (其中逐字节一致 1446) 仅单侧 0 条" 与 "零差异"
- 推送: git push origin main 成功 (2faefa9..fefc79b, 8b238f1), git rev-list --left-right --count origin/main...HEAD 为 0 0
- 抽查: 两仓的 H-BG-001.json (figure_name=班固, figure_code=H-BG-001), H-BAC-001.json (figure_code=H-BAC-001, code=Bach), H-Mendel-001.json (figure_name=孟德尔) 完全一致; 发布仓已无 H-DaVinci-001.json, 归档件在 data/figures/_duplicates/ 下
- 遗留说明: data/figures 下约 130 个文件在工作仓的权限位本来就是 755, 本次同步把该权限位也带进了发布仓 (内容 sha256 一致, parity 按内容判定, 不受影响)
