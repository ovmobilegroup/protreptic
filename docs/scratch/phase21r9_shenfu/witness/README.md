# Phase21-R9 沈复见证副本（卡片 t_d78053e7；零库写）
- 用途：核验 docs/research/phase21r9_shenfu_sourcing_report.md 全部引文（强归一子串比对）。
- 文件：34 件＋ia_search_fs6j.json；sha256 全值见 witness_sha256.txt（历次抓取时点 2026-09-24，工具 curl/browser）。
- 对应关系：raw_juan1..6=维基文库繁体底本；hans_plain_juan1..6=同源 zh-hans 转换副本（正文比对基准）；其余按文件名与报告 §六.1 见证表对应。
- 复跑：python3 verify_quotes.py  → 打印命中统计并生成 quote_verification_final.json。
- 声明：本目录为证据副本，非库文件；不入 data/，不改登记表；重建卡仅消费报告与 JSON。
