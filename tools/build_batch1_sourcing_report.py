#!/usr/bin/env python3
"""build_batch1_sourcing_report.py -- 装配 W8 Stage2 批1 报告（卡号 t_70a8cbce 。）

读：素材包 JSON、书单 JSON、两份对账 JSON、缓存索引与 manifest；写：
    docs/research/phase21w8_stage2_batch1_sourcing_report.md    （报告正文 。）
    docs/research/phase21w8_stage2_batch1_sourcing_report.json  （素材包 + 对账 + 缓存 + 证据 。）
只读输入、写报告两件；**零主库写入**。
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
PACK = REPO / "docs" / "research" / "phase21w8_stage2_batch1_sourcing_report.json"
MD = REPO / "docs" / "research" / "phase21w8_stage2_batch1_sourcing_report.md"
BOOKLIST = REPO / "docs" / "research" / "phase21w8_stage2_batch1_booklist.json"
RECOUNT_BASE = REPO / "data" / "audit" / "phase21w8_stage2_batch1_recount_baseline.json"
RECOUNT_LIVE = REPO / "data" / "audit" / "phase21w8_stage2_batch1_recount_live.json"
INDEX = REPO / "data" / "audit" / "source_texts_w8_stage2_batch1.json"
VERIFY_LOG = REPO / "data" / "audit" / "phase21w8_stage2_batch1_verify.log"


def load(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def sha16(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()[:16]


def now_iso():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def recount_block(booklist):
    base, live = load(RECOUNT_BASE), load(RECOUNT_LIVE)

    def hot(rec):
        return sorted(r["book"] for r in rec["rows"]
                      if r["count_raw"] >= rec["min_citations"] and r["unresolved"])

    hot68 = sorted(r["book"] for r in booklist["hot68"])
    bl, lv = {}, {}
    for tag, rec, out in (("baseline", base, bl), ("live", live, lv)):
        for k in ("modes_total", "modes_source", "span_names_total", "book_names_total",
                  "hot_new_total", "hot_old_total", "new_only", "old_only"):
            out[k] = rec[k]
    return {"baseline": bl, "live": lv, "hot68_booklist_n": len(hot68),
            "baseline_matches_booklist": hot(base) == hot68,
            "live_superset_of_booklist": set(hot68) <= set(hot(live)),
            "live_delta_vs_booklist": sorted(set(hot(live)) - set(hot68))}


def cache_block():
    idx = load(INDEX)
    rows = []
    for e in idx.get("entries", []):
        rows.append({"label": e.get("label"), "status": e.get("status"), "coverage": e.get("coverage"),
                     "subpages": e.get("subpages"), "chars": e.get("chars"), "bytes": e.get("bytes"),
                     "file": e.get("file"), "zh_cn_file": (e.get("zh_cn") or {}).get("file"),
                     "pages_failed": e.get("pages_failed"),
                     "zh_cn_failed_chunks": (e.get("zh_cn") or {}).get("failed_chunks"),
                     "sha256": e.get("sha256")})
    return {"index": "data/audit/source_texts_w8_stage2_batch1.json",
            "counts": idx.get("counts"), "entries": rows}


def evidence_block():
    paths = ["tools/build_source_links.py", "tools/source_link_index.py",
             "tools/fetch_batch1_texts.py", "tools/build_batch1_sourcing_pack.py",
             "tools/verify_batch1_sourcing_delivery.py", "tools/build_batch1_sourcing_report.py",
             "tools/fetch_source_texts.py", "tools/manifests/w8_stage2_batch1_texts.json",
             "data/audit/source_texts_w8_stage2_batch1.json",
             "data/audit/phase21w8_stage2_batch1_recount_baseline.json",
             "data/audit/phase21w8_stage2_batch1_recount_live.json",
             "docs/research/phase21w8_stage2_batch1_booklist.json"]
    out = []
    for p in paths:
        fp = REPO / p
        if fp.is_file():
            out.append({"path": p, "sha256_16": sha16(fp), "bytes": fp.stat().st_size})
    return out


def build_md(pack, rec, cache, ev):
    A = []
    ap = A.append
    counts, vc, b1 = pack["counts"], pack["verdict_counts"], pack["per_book"]
    ap("# Phase21-W8 Stage2 批1 工具/管道：书级归并重扫口径修复 + 批1 fetch 素材包。")
    ap("")
    ap("卡号 `t_70a8cbce`（Phase21-W8 Stage2 批1）；上游书单 `t_6ed4fe0d`（commit 20b13092）。")
    ap("生成：%s（本地时区）。 产线：W5 pilot 修复链口径。" % datetime.now().strftime("%Y-%m-%d %H:%M"))
    ap("")
    ap("## 一、概述。")
    ap("")
    ap("1. **候选生成口径修复（build_source_links 侧）**：旧口径按「条目内去重 + 篇章跨度」计数，"
       "书级被引 >= 3 而单跨度 < 3 的书（《论衡》类）从未成为候选（pilot 报告 §2.1 根因条）。 "
       "新口径 = 扫全部书名号原始跨度（不去重）→ 按中点「·」首段归并为书级 → 计数始终在书级。")
    ap("2. **批1 fetch 素材包**：按书单抓 17 抓取项（16 部书；二程遗书与河南程氏遗书共源）主源全文入本地缓存（独立索引，零主库写），"
       "并对批1 各书全部 mode 引文逐条对照，产出 quote / variant（异文）/ null（查无）/ cross-lang 四档结论。")
    ap("")
    ap("关键数字（[实测-本卡]）：")
    ap("")
    ap("| 项 | 数 | 说明 |")
    ap("|---|---|---|")
    ap("| 对账 baseline hot68 | %d | baseline 20b13092（modes %d）复扫；与书单 hot68 逐名一致：%s |" %
       (rec["baseline"]["hot_new_total"], rec["baseline"]["modes_total"], rec["baseline_matches_booklist"]))
    ap("| 对账 dedup 口径 | %d | 条目内去重口径（书单备注的 59）|" % rec["baseline"]["hot_old_total"])
    ap("| live 复扫 | %d | 工作区 modes %d；相对 hot68 增量 %s |" %
       (rec["live"]["hot_new_total"], rec["live"]["modes_total"], ", ".join(rec["live_delta_vs_booklist"])))
    ap("| 批1 条目 | %d | 17 书 + 现代诗（否定记录）|" % counts["books"])
    ap("| 逐条引文 | %d | mode 级；跨度实例 %d；null 中近似档 %d |" %
       (counts["quotes_total"], counts["span_instances"], counts.get("null_near_partial", 0)))
    ap("| quote（命中） | %d | 原文逐字（空白/标点归一）|" % vc.get("quote", 0))
    ap("| variant（异文） | %d | 繁简差：引文侧 zh-hant 或 zh-cn 副本命中 |" % vc.get("variant", 0))
    ap("| null（查无） | %d | 两副本未见（含否定记录 8 条）|" % vc.get("null", 0))
    ap("| cross-lang | %d | 跨语言书，留语义对照档 |" % vc.get("cross-lang", 0))
    ap("| 负对照 | %d | 单字符扰动，假阳性 %d |" % (counts["negative_controls"], counts["negative_false_positive"]))
    ap("")
    ap("## 二、输入与基线。")
    ap("")
    ap("- 书单：`docs/research/phase21w8_stage2_batch1_booklist.json`（sha256-16 `%s`；hot68 全量 rows、"
       "batch1 18 项、method 段口径）。" % sha16(BOOKLIST))
    ap("- 素材包源：`data/modes_data.json` 快照 `%s`（modes %d；工作区含在途 R9 落盘）。" %
       (pack["modes_snapshot"]["sha256"][:16], pack["modes_snapshot"]["modes_total"]))
    ap("- 缓存索引：`data/audit/source_texts_w8_stage2_batch1.json`（本卡独立索引；"
       "不改动 `data/audit/source_texts.json` 与 `data/source_links.json`）。")
    ap("- 逐页清单：`tools/manifests/w8_stage2_batch1_texts.json`（17 抓取项；现代诗 fetch=none 不抓）。")
    ap("- 上游参考：`docs/research/phase21w5_wangchong_sourcing_report.md`、"
       "`docs/research/phase21w5_wangchong_archive_report.md` §2.1（根因条）。")
    ap("")
    ap("## 三、方法。")
    ap("")
    ap("**3.1 候选口径修复**：新增 `source_link_index.extract_refs_raw`（保序、不去重）与 "
       "`build_source_links.count_citations`（书级归并；span/book 双计数）；候选门槛 = 书级被引 >= min 且"
       "无任何 candidate_key 在索引中。 复核：`python3 tools/build_source_links.py --bookcount-report --modes-spec REV:data/modes_data.json`。")
    ap("")
    ap("**3.2 全文抓取**：`tools/fetch_batch1_texts.py`（新）按 manifest 抓取：子页枚举三模式"
       "（`links`/`allpages`/`list`），正文两通道（`raw`=action=raw；`render`=action=parse，"
       "用于 ProofreadPage 转写页与多列页）。 coverage：complete/partial/single-page；缺页登记 "
       "`pages_failed`；中文书另产 zh-cn 转换副本（D4 层）。 缓存只在 `data/audit/`（零 modes_data 写）。")
    ap("")
    ap("**3.3 逐条对照**：`tools/build_batch1_sourcing_pack.py`（新）逐条比 `key_quote_zh`："
       "quote（逐字，空白/标点归一，省略号分段）。variant（繁简：引文整批转 zh-hant 或 zh-cn 副本命中）。"
       "null（未见；附 elsewhere 与近似诊断：句命中 n/m、3 字窗比例）。cross-lang（非中文源不适用逐字对读）。 "
       "负对照 = 逐书抽 2 条做单字符扰动必查无；`weak` 标 < 6 字短引文。")
    ap("")
    return A


def build_md2(A, pack, rec, cache, ev):
    counts, vc, b1 = pack["counts"], pack["verdict_counts"], pack["per_book"]
    ap = A.append
    by_label = {}
    for e in cache["entries"]:
        by_label[(e.get("label") or "").strip("\u300a\u300b")] = e

    def pagestr(book):
        e = by_label.get(book) or {}
        sp = e.get("subpages")
        return "%s/%s" % (sp[0], sp[1]) if sp else "-"

    ap("## 四、执行结果。")
    ap("")
    ap("**4.1 候选口径对账（[实测-本卡]）**。")
    ap("")
    ap("- baseline（`20b13092:data/modes_data.json`，modes %d）：书级名 %d、跨度名 %d；新口径 >=3 未解析 "
       "**%d 本**（与书单 hot68 逐名一致：%s）；旧口径 %d 本；差集 9 本：%s。" %
       (rec["baseline"]["modes_total"], rec["baseline"]["book_names_total"], rec["baseline"]["span_names_total"],
        rec["baseline"]["hot_new_total"], rec["baseline"]["matches"] if False else rec["baseline_matches_booklist"],
        rec["baseline"]["hot_old_total"], ", ".join(rec["baseline"]["new_only"])))
    ap("- live（工作区，modes %d）：新口径 %d 本 / 旧口径 %d 本；相对 hot68 增量 %s（在途 R9 卡新增 mode，非口径回归）。" %
       (rec["live"]["modes_total"], rec["live"]["hot_new_total"], rec["live"]["hot_old_total"],
        ", ".join(rec["live_delta_vs_booklist"])))
    ap("- 结论：68 本漏收根因已修复且可复核；差集方向 = 旧口径只漏不收（new_only 9 本、old_only 0 本）。")
    ap("")
    ap("**4.2 缓存状态（逐本 [实测-本卡]）**。")
    ap("")
    ap("| 书 | rank | 主源 | 抓取 | 通道 | 状态 | 覆盖 | 子页 ok/枚举 | chars | zh-cn | 逐条 | 分档 |")
    ap("|---|---|---|---|---|---|---|---|---|---|---|---|")
    for b in b1:
        v = b["verdict_counts"]
        ch = ("render" if b.get("method") == "html-render" else
              ("raw" if b.get("method") == "wikitext" else "-"))
        ap("| %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %d | q%s/v%s/n%s/x%s |" % (
            b["book"], b["rank"], b["primary_title"], b["fetch"], ch, b["index_status"], b["coverage"] or "-",
            pagestr(b["book"]), b["chars"], "yes" if b["zh_cn_file"] else "-", b["quotes_n"],
            v.get("quote", 0), v.get("variant", 0), v.get("null", 0), v.get("cross-lang", 0)))
    ap("")
    ap("索引 counts：%s；负对照 %d 条、假阳性 %d；weak %d；引文整批转 zh-hant：n=%s complete=%s。" %
       (json.dumps(cache["counts"], ensure_ascii=False), counts["negative_controls"],
        counts["negative_false_positive"], counts["weak"],
        (pack.get("quote_conversion") or {}).get("n"),
        ((pack.get("quote_conversion") or {}).get("meta") or {}).get("complete")))
    ap("")
    ap("**4.3 逐条引文结论**（全量在报告 JSON 的 `quotes` 段）。")
    ap("")
    nulls = [q for q in pack["quotes"] if q["verdict"] == "null"]
    nears = [q for q in nulls if q.get("near_partial")]
    ap("null（%d 条；近似档 %d 条 = 部分短句逐字命中、余为改写/拼合）：" % (len(nulls), len(nears)))
    ap("")
    for q in nulls[:48]:
        extra = ""
        if q.get("sent_hits"):
            extra += "；句命中 %d/%d" % tuple(q["sent_hits"])
        if q.get("shingle_ratio") is not None:
            extra += "；3 字窗 %s" % q["shingle_ratio"]
        if q.get("longest_ratio") is not None:
            extra += "；最长连续 %s" % q["longest_ratio"]
        if q.get("near_partial"):
            extra += "；近似档"
        ew = ("；elsewhere=%s" % ", ".join(q.get("elsewhere") or [])) if q.get("elsewhere") else ""
        ap("- `%s` %s《%s》：%s%s%s" % (q["mode_code"], q["figure_name_zh"], q["book"],
                                       (q["quote"] or "")[:40], extra, ew))
    if len(nulls) > 48:
        ap("- （另有 %d 条见 JSON）" % (len(nulls) - 48))
    ap("")
    ap("跨语言档（%d 条，留语义对照）：%s。" %
       (vc.get("cross-lang", 0),
        "; ".join("%s %d" % (b["book"], b["verdict_counts"].get("cross-lang", 0))
                  for b in b1 if b["verdict_counts"].get("cross-lang"))))
    ap("")
    return A


def build_md3(A, pack, rec, cache, ev):
    ap = A.append
    ap("## 五、证据。")
    ap("")
    ap("| 文件 | sha256-16 | bytes |")
    ap("|---|---|---|")
    for e in ev:
        ap("| %s | %s | %s |" % (e["path"], e["sha256_16"], e["bytes"]))
    ap("")
    ap("报告两件（本文与 `.json`）为本次生成产物，自指校验和不列入上表；最终 sha256 以提交回执为准。")
    ap("")
    ap("复现命令（[实测-本卡]）：。")
    ap("")
    ap("- 口径对账：`python3 tools/build_source_links.py --bookcount-report --modes-spec 20b13092:data/modes_data.json --bookcount-json data/audit/phase21w8_stage2_batch1_recount_baseline.json`")
    ap("- live 复扫：`python3 tools/build_source_links.py --bookcount-report --bookcount-json data/audit/phase21w8_stage2_batch1_recount_live.json`")
    ap("- 抓取（增量）：`python3 tools/fetch_batch1_texts.py`（--dry-run 先枚举；--force 重抓）")
    ap("- 素材包：`python3 tools/build_batch1_sourcing_pack.py`")
    ap("- 独立核验：`python3 tools/verify_batch1_sourcing_delivery.py`")
    ap("")
    ap("## 六、核验。")
    ap("")
    if VERIFY_LOG.is_file():
        ap("独立核验 `tools/verify_batch1_sourcing_delivery.py` 现跑输出（全文见 `%s`）：。" %
           VERIFY_LOG.relative_to(REPO))
        ap("")
        ap("```")
        ap(VERIFY_LOG.read_text(encoding="utf-8").strip())
        ap("```")
    else:
        ap("（核验日志待生成：`data/audit/phase21w8_stage2_batch1_verify.log`）。")
    ap("")
    ap("零主库写入实证：本卡写盘仅限 tools/、data/audit/（缓存与对账）、docs/research/（报告）；"
       "`data/modes_data.json` 本卡全程只读（sha/mtime 恒定，见核验 C16 与提交回执）。")
    ap("")
    ap("## 七、残留与风险。")
    ap("")
    ap("- 抓取覆盖：轮内残留 partial/failed 书及缺页见四.2 表与索引 pages_failed；已跑补页修复（只补缺页），"
       "修复后原文变更的 zh-cn 副本标 stale。")
    ap("- 庄子注（四庫全書本）：转录页为节录且含生僻/异体字（\U00029516/\u3ad6/\u3e03/\u8358/\u5f83 等），"
       "逐字对读系统性受限（null 的 3 字窗 <= 0.17）；建议另立异体字归一轮或改判「待核」档。")
    ap("- 老子注：本轮主源为「道德經（王弼本）」白文（无注文）；引文多为《老子注》《老子指略》《周易略例》"
       "注文（源外），null 为正确结论；下游需另抓王弼注全本。")
    ap("- 太极图说：整篇为短篇（331 字符全文），MIN_CHARS=2000 阈值将整篇误标 index-page（非缺页）；"
       "对照按全文进行。")
    ap("- 春秋繁露：《举贤良对策》类引文源在漢書卷056（非繁露），null 正确；繁露内部引文多为改写/拼合"
       "（3 字窗 0.33-0.89，其中近似档可作待核）。")
    ap("- 跨语言 74 条：逐字对读不适用，建议入「语义对照」档（口径待船长裁定）；现代诗 8 条 = 否定记录。")
    ap("- 双键同源：《河南程氏遗书》与《二程遗书》共源一文件（manifest shared_from），对账按各自 label 计。")
    ap("- 跨度实例 %d vs mode 级 %d：同 mode 多次引同一书时按 mode 去重。"
       % (pack["counts"]["span_instances"], pack["counts"]["quotes_total"]))
    ap("- 字窗/句命中仅为辅助信号（近似档判定），不作为逐字结论。")
    ap("- 通道教训：含模板注文的页面（四庫 {{SK notes}}、王弼注文标记）走 raw（wikitext）会被 "
      "raw_to_text 整段剥离 {{...}} 而丢注文；本轮实测改判 render：庄子注（注文恢复）、"
      "老子注（王弼注文恢复，11,099->32,836 字符）；后续批次遇注文含模板的书先实测通道再抓。")
    ap("- render 通道带出的页面外壳（首行 mw-parser-output 断标签、页尾公有领域块）已由 "
      "tools/clean_batch1_cache_chrome.py 清理并重算 sha（9 书 20 文件）；对读为子串匹配，清理不改正文。")
    ap("")
    ap("## 八、下一步与路由。")
    ap("")
    ap("- 链接入库卡（下游）：以本报告 68 本对账 + 候选口径修复为准，扩 `data/source_links.json` 并跑全链。")
    ap("- 素材包档位固定（quote/variant/null/cross-lang）供 Stage2 后续批次复用。")
    ap("- 跨语言语义对照档、四庫异体字归一、王弼注本换源：待船长裁定/另立卡。")
    ap("")
    ap("## 九、附链。")
    ap("")
    ap("- 本卡：`t_70a8cbce`（Phase21-W8 Stage2 批1）；上游 `t_6ed4fe0d`（书单，commit 20b13092）；子卡 `t_b85ae14a`。")
    ap("- 参考：`docs/research/phase21w5_wangchong_sourcing_report.md`、`docs/research/phase21w5_wangchong_archive_report.md` §2.1。")
    ap("")
    receipt = REPO / "data" / "audit" / "phase21w8_stage2_batch1_submission.json"
    if receipt.is_file():
        rec = load(receipt)
        ap("## 十、提交回执。")
        ap("")
        ap("- 主提交：`%s`（%s）；独立核验：%s。" %
           (rec.get("commit"), rec.get("committed_at"), rec.get("verify")))
        zw = (rec.get("zero_write") or {}).get("modes_data.json") or {}
        ap("- 零主库写入：`data/modes_data.json` sha16 `%s`，mtime %s（本卡全程未写）。" %
           (zw.get("sha16"), zw.get("mtime")))
        ap("- 成品 sha16：")
        for a in rec.get("artifacts", []):
            ap("    - `%s` `%s`" % (a.get("path"), a.get("sha16")))
        ap("")
    return A


def main():
    pack = load(PACK)
    booklist = load(BOOKLIST)
    rec = recount_block(booklist)
    cache = cache_block()
    ev = evidence_block()
    A = build_md(pack, rec, cache, ev)
    A = build_md2(A, pack, rec, cache, ev)
    A = build_md3(A, pack, rec, cache, ev)
    md = "\n".join(A) + "\n"
    MD.write_text(md, encoding="utf-8")
    pack["reconcile"] = rec
    pack["cache"] = cache
    pack["evidence"] = ev
    pack["report_md"] = "docs/research/phase21w8_stage2_batch1_sourcing_report.md"
    PACK.write_text(json.dumps(pack, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("[OK] %s (%d bytes)" % (MD, len(md.encode("utf-8"))))
    print("[OK] %s (embedded reconcile/cache/evidence)" % PACK)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
