# Phase21-W5 引文落源 pilot · 工具扩能卡报告

## 1. 验收项
> ①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭ 全 PASS；37/38（Z7 存量 drift）；verify 383 OK；gate --hard-fail exit 0

---

## 2. 收尾补交说明（卡 t_9f3ccb2c，2026-09-24）

【背景】B1 工具扩能卡（t_f09365bb）与 A1 研究卡（t_5a7abc92）的工作树产物缺「仓级收口」（未提交/未镜像/未 push）；且 data/audit/source_texts.json 工作区版本被再生为仅含《论衡》1 条、counts ok:1 的窄版（危险状态：若整体提交将丢 95 条既有条目）。
【本卡处置】1) 以 HEAD 完整版（96 条）为基合并修复 source_texts.json；2) 白名单提交（tools 4 件 + data 2 件 + 本报告 + A1 报告 2 件 + 见证目录；名单外 0）；3) 发布仓镜像 + push + 回执；4) 全链回归复跑留证。零 data/modes_data.json 改动。
【预检复核备注】逐项复核（非照抄）：1) tools 4 件 / source_links.json（+8 行）/ source_texts.json（工作区窄版 1 条 vs HEAD 96 条）与实物一致；2) 缓存双件 dea899a0 已提交、发布仓未镜像未 push，与实物一致；3) 本报告文件 4 行桩实际已随 cb8601a1 提交（原登记写作「未提交」，属表述偏移，如实记录；本卡照常在其上补全并纳入白名单提交，处置不变）。

## 3. source_texts.json 合并证明（96 -> 97，零条目丢失）

| 版本 | 条目数 | 字节 | sha256 |
|---|---|---|---|
| HEAD 完整版（generated 2026-09-20T14:45:01+00:00） | 96 | 60,816 | `4a00e1341896ea545d4b6bc120a4f983cf35fd21e04c441827e820309d64bf73` |
| 工作区窄版（危险态，仅《论衡》） | 1 | 1,948 | `20bfeffdc6a456a9dacbfe67cadc5362cd182fea9090ec258ae96430cfde9a26` |
| 合并后（本卡产出） | 97 | 62,191 | `affdd78137e3fedfb7af6aedc15a6ee0c63b55033b260845c5745d6fe432d6d7` |

- 合并口径：HEAD 96 条逐条原样保留 + 插入《论衡》条目（携带完整 zh_cn 转换元数据：api=zh.wikipedia action=parse、variant=zh-cn、chunk_chars=8000、chunks=15、retries=5、failed_chunks=0、complete=true、converted_at=2026-09-23T16:00:08+00:00、副本文件 data/audit/source_texts/6f2e2e4e124df80a.zh-cn.txt 副本）。
- 插入位=全表 key 排序第 87 位（《论动体的电动力学》与《论语》之间）；合并后全表仍严格有序（机检 merged_sorted=True 通过）。
- 零丢失（程序化证明）：96/96 既有条目逐条 byte-identical（逐条 json.dumps 全等）；added=[《论衡》]，removed=[]，键面唯一无重复。
- 顶层变更 4 处（口径已声明）：generated_at 2026-09-20T14:45:01+00:00 -> 2026-09-23T16:00:08+00:00；policy 增「zh-cn 转换副本」条款；max_subpages 12 -> 95（与 2026-09-23 生成运行参数对齐；85 子页完整抓取的必要参数）；counts.ok 43 -> 44（新增《论衡》为 ok 状态；sum(counts)=97=len(entries) 不变式保持，其余键值不变）。另 schema/generated_by/min_chars 不变。
- 全文件 diff 量化：+37 行 / -4 行（4 行顶层元数据 + 33 行《论衡》条目），无其他任何行变化。

## 4. 回归复跑留证（工作仓，2026-09-24）

| 项 | 结果 |
|---|---|
| credibility_gate.py --hard-fail | exit 0：存量 524 条已冻结、新增 0 条、「无新增硬失败」（warnings D4/D5 26 条非阻断） |
| verify_source_links.py --hard-fail | exit 0：383 条核验（OK 200 共 151；UNVERIFIABLE 共 213；UNREACHABLE 共 19，非阻断存量警告）；硬失败口径「无新增坏链」 |
| test_credibility_gate.py | exit 0：6/6 passed |
| test_credibility_gate_modes.py | exit 0：7/7 passed |
| test_credibility_d45.py | 37/38（唯一 FAIL=Z7 backfill_lifespans 存量 drift：盘上 476 / 现场 575；与 B1 卡同值、非本卡引入；本卡零接触 lifespan 数据） |
