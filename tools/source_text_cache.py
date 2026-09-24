#!/usr/bin/env python3
"""source_text_cache.py -- D4 (引文不符) 的原文缓存读取 + 子串核验规则 (唯一实现).

数据来源
    data/audit/source_texts.json    索引: key -> {url, status, file, chars, sha256, ...}
    data/audit/source_texts/<x>.txt 纯文本原文 (由 tools/fetch_source_texts.py 抓取)
    索引缺失 = 缓存未建: 一律按 "无可用文本" 处理 (unchecked), 不假装核过.

匹配规则 (与 docs/planning/credibility_framework.md 第 10.2 节逐字一致)
    N0 归一化: 只保留 CJK 汉字 / 拉丁字母 / 数字, 丢掉空白与一切标点 (全半角差异不影响匹配).
    N1 片段: 把 key_quote_zh 按标点切成句片段, 取归一化后长度 >= MIN_FRAGMENT (默认 8) 的片段,
             由长到短最多取 MAX_FRAGMENTS (默认 8) 个; 全部片段都短于阈值 -> quote-too-short
             (不可核验, 计入统计, 不判不符 -- 短句在长文里偶然命中率太高, 判了就是误报).
    N2 命中: 任一片段在归一化后的原文里出现 -> matched.
    N3 落空: 所有片段都找不到 -> mismatch (D4 命中, 写审计清单, 走 suspect).
    N4 无文本: 引文没有可用的缓存文本 (index-page / fetch-failed / http-error / 未抓 / 非原文类
             链接) -> unchecked, 并记下具体理由 (no-cache-entry / cache-not-ok:<status> /
             no-citation / no-fulltext-link / cache-missing).

诚实边界 (写进报告的局限, 不许含糊)
    * 只对 "source_chapter 里出现书名号引文" 且 "该引文解析到原文类链接" 且 "缓存覆盖整部作品
      (coverage=single-page|complete)" 的模式可核; 其余一律 unchecked 并给理由
      (含 coverage=partial 的 "只抓了部分篇章"), 不许静默放过.
    * 归一化后匹配是**字面子串**判定: 繁简差异 / 异体字 / 引文经过改写的意译都不会命中
      -- 报出来的 mismatch 是 "字面不符", 不等于 "伪造" (处置仍为复核).
"""

from __future__ import annotations

import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
INDEX_PATH = REPO_ROOT / "data" / "audit" / "source_texts.json"
TEXT_DIR = REPO_ROOT / "data" / "audit" / "source_texts"

MIN_FRAGMENT = 8
MAX_FRAGMENTS = 8
FULLTEXT_TYPES = ("wikisource", "gutenberg", "ctext")

_KEEP = re.compile(r"[0-9A-Za-z\u4e00-\u9fff]+")
_SPLIT = re.compile(r"[^\w\u4e00-\u9fff]+", re.UNICODE)


def normalize(text) -> str:
    """N0: 只保留汉字/字母/数字 (去空白与标点)."""
    if not isinstance(text, str):
        return ""
    return "".join(_KEEP.findall(text))


def fragments(quote, min_len: int = MIN_FRAGMENT, limit: int = MAX_FRAGMENTS):
    """N1: 引文 -> 归一化片段 (由长到短, 去重, 只留够长的)."""
    if not isinstance(quote, str):
        return []
    parts = []
    for raw in _SPLIT.split(quote):
        norm = normalize(raw)
        if len(norm) >= min_len and norm not in parts:
            parts.append(norm)
    parts.sort(key=len, reverse=True)
    return parts[:limit]


class SourceTextCache:
    """原文缓存: 索引 + 懒加载文本 (按需读文件, 内存里按 key 缓存)."""

    def __init__(self, index_path=None, text_dir=None, root=None):
        self.index_path = Path(index_path) if index_path else INDEX_PATH
        self.text_dir = Path(text_dir) if text_dir else TEXT_DIR
        self.entries = {}
        self.present = False
        self._texts = {}
        if self.index_path.is_file():
            try:
                doc = json.loads(self.index_path.read_text(encoding="utf-8"))
                self.entries = dict((e.get("key"), e) for e in doc.get("entries", []))
                self.present = True
            except Exception:
                self.entries = {}
                self.present = False
        if root:
            self.text_dir = Path(root) / "data" / "audit" / "source_texts"

    def usable_keys(self):
        """可用于 D4 子串核验的 key：抓取成功 **且覆盖整部作品**。

        coverage 口径（tools/fetch_source_texts.py）：
            single-page  单页即全文            -> 可核
            complete     目录 + 全部子页        -> 可核
            partial      目录 + 前 N 个子页     -> **不可核**（缓存没覆盖全篇，
                         在部分文本里找不到引文无法证明「引文不符」，判了就是误报）
        """
        return sorted(k for k, e in self.entries.items()
                      if e.get("status") in ("ok", "ok-shared")
                      and (e.get("coverage") in ("single-page", "complete")))

    def text_for(self, key):
        """取某 key 的归一化原文；不可用（含 coverage=partial）返回 None。"""
        if key in self._texts:
            return self._texts[key]
        entry = self.entries.get(key) or {}
        if self.status_of(key) not in ("ok",):
            self._texts[key] = None
            return None
        rel = entry.get("file")
        if not rel:
            self._texts[key] = None
            return None
        path = Path(rel)
        if not path.is_absolute():
            path = REPO_ROOT / rel
        if not path.is_file():
            self._texts[key] = None
            return None
        self._texts[key] = normalize(path.read_text(encoding="utf-8"))
        return self._texts[key]

    def converted_text_for(self, key):
        """取某 key 的 zh-cn 转换副本（N0 归一化后）；不可用或不完整一律返回 None

        Phase21-W5 扩能：索引条目 zh_cn 元数据须 complete=True 且 failed_chunks=0
        才可用（不完整的转换副本绝不当作全文参与比对，宁可退回 script-mismatch 守卫）

        R7① 加固（t_0dc95522）：此前只查 complete 旗标，complete 被硬写时带回退块的
        副本仍会被采用；现在 failed_chunks>0 一律拒用（与文档口径一致）。
        """
        entry = self.entries.get(key) or {}
        meta = entry.get("zh_cn") or {}
        try:
            failed = int(meta.get("failed_chunks") or 0)
        except (TypeError, ValueError):
            failed = -1  # 不可解析 -> 视为不完整，拒用
        if not (meta.get("complete") and failed == 0 and meta.get("file")):
            return None
        path = Path(meta["file"])
        if not path.is_absolute():
            path = REPO_ROOT / meta["file"]
        if not path.is_file():
            return None
        return normalize(path.read_text(encoding="utf-8"))

    def status_of(self, key):
        entry = self.entries.get(key)
        if entry is None:
            return "no-cache-entry"
        status = entry.get("status") or "unknown"
        if status == "partial" or (status in ("ok", "ok-shared")
                                   and entry.get("coverage") not in ("single-page", "complete")):
            return "partial-coverage(缓存未覆盖整部作品)"
        return status


def cache_status_for_citations(link_infos, cache: SourceTextCache):
    """从 "已解析引文列表" (source_link_index.resolve_citation 的输出) 推出可核性.

    返回 (status, key, reason):
        status in {checkable, unchecked}
    """
    if not link_infos:
        return "unchecked", None, "no-citation"
    fulltext = [r for r in link_infos
                if (r.get("source_type") or "") in FULLTEXT_TYPES and (r.get("url") or "").strip()]
    if not fulltext:
        return "unchecked", None, "no-fulltext-link"
    for r in fulltext:
        key = r.get("key")
        st = cache.status_of(key)
        if st == "ok":
            return "checkable", key, "cache-ok"
    first = fulltext[0]
    st = cache.status_of(first.get("key"))
    return "unchecked", first.get("key"), "cache-not-ok:" + st


# 简 -> 繁 常见字对（只用于**检测繁简不一致**，不做字形转换；见 N5）。
# 检测规则：引文里出现简体字 s，而原文里只出现对应繁体字 t（简体的 s 不在原文里）
# 且这种信号 >= SIMP_TRAD_MIN_HITS 个 -> 判「繁简不一致」，标不可核。
# 为什么不做转换：转换需要完整的简繁映射表（opencc 级），手搓表会把「未命中」变成
# 假命中；宁可如实说「繁简不同，字面比对无意义」，也不做一个不完整的转换器。
SIMP_TRAD_PAIRS = (('胜', '勝'), ('后', '後'), ('战', '戰'), ('孙', '孫'), ('传', '傳'), ('习', '習'), ('录', '錄'), ('伤', '傷'), ('论', '論'), ('语', '語'), ('汉', '漢'), ('书', '書'), ('无', '無'), ('与', '與'), ('为', '爲'), ('这', '這'), ('时', '時'), ('发', '發'), ('国', '國'), ('学', '學'), ('会', '會'), ('个', '個'), ('将', '將'), ('万', '萬'), ('门', '門'), ('见', '見'), ('说', '說'), ('长', '長'), ('义', '義'), ('药', '藥'), ('经', '經'), ('断', '斷'), ('脉', '脈'), ('汤', '湯'), ('阴', '陰'), ('阳', '陽'), ('证', '證'), ('卫', '衛'), ('骑', '騎'), ('怀', '懷'), ('虑', '慮'), ('权', '權'), ('变', '變'), ('实', '實'), ('势', '勢'), ('谋', '謀'), ('计', '計'), ('敌', '敵'), ('备', '備'), ('观', '觀'), ('众', '眾'), ('军', '軍'), ('赵', '趙'), ('齐', '齊'), ('韩', '韓'), ('吴', '吳'), ('陈', '陳'), ('郑', '鄭'), ('鲁', '魯'), ('礼', '禮'), ('乐', '樂'), ('诗', '詩'), ('词', '詞'), ('记', '記'), ('议', '議'), ('识', '識'), ('达', '達'), ('远', '遠'), ('迟', '遲'), ('遗', '遺'), ('铁', '鐵'), ('银', '銀'), ('钱', '錢'), ('页', '頁'), ('显', '顯'), ('题', '題'), ('风', '風'), ('飞', '飛'), ('马', '馬'), ('鸟', '鳥'), ('龙', '龍'), ('鱼', '魚'), ('麦', '麥'), ('黄', '黃'), ('点', '點'), ('热', '熱'), ('灯', '燈'), ('炼', '煉'), ('环', '環'), ('现', '現'), ('产', '產'), ('业', '業'), ('东', '東'), ('华', '華'), ('叶', '葉'), ('岁', '歲'), ('归', '歸'), ('当', '當'), ('尝', '嘗'), ('团', '團'), ('园', '園'), ('图', '圖'), ('场', '場'), ('坏', '壞'), ('坚', '堅'), ('报', '報'), ('担', '擔'), ('拥', '擁'), ('择', '擇'), ('挂', '掛'), ('换', '換'), ('据', '據'), ('检', '檢'), ('楼', '樓'), ('欢', '歡'), ('济', '濟'), ('浅', '淺'), ('温', '溫'), ('满', '滿'), ('湾', '灣'), ('灵', '靈'), ('灾', '災'), ('灭', '滅'), ('兽', '獸'), ('医', '醫'), ('乡', '鄉'), ('亲', '親'), ('儿', '兒'), ('头', '頭'), ('帅', '帥'), ('师', '師'), ('应', '應'), ('废', '廢'), ('广', '廣'), ('庆', '慶'), ('库', '庫'), ('张', '張'), ('强', '強'), ('征', '徵'), ('従', '從'), ('从', '從'), ('优', '優'), ('伟', '偉'), ('侦', '偵'), ('侧', '側'), ('俭', '儉'), ('债', '債'), ('倾', '傾'), ('储', '儲'), ('偿', '償'), ('兑', '兌'), ('兰', '蘭'), ('关', '關'), ('兴', '興'), ('养', '養'), ('农', '農'), ('冲', '衝'), ('决', '決'), ('况', '況'), ('净', '淨'), ('准', '準'), ('凉', '涼'), ('减', '減'), ('凑', '湊'), ('击', '擊'), ('刘', '劉'), ('则', '則'), ('刚', '剛'), ('创', '創'), ('别', '別'), ('剂', '劑'), ('划', '劃'), ('剧', '劇'), ('办', '辦'), ('务', '務'), ('动', '動'), ('劲', '勁'), ('劳', '勞'), ('勋', '勳'), ('协', '協'), ('单', '單'), ('卖', '賣'), ('厂', '廠'), ('历', '歷'), ('厉', '厲'), ('压', '壓'), ('厌', '厭'), ('厅', '廳'), ('县', '縣'), ('参', '參'), ('双', '雙'), ('叙', '敘'), ('叠', '疊'), ('号', '號'), ('叹', '嘆'), ('听', '聽'), ('启', '啟'), ('员', '員'), ('呜', '嗚'), ('咏', '詠'), ('响', '響'), ('哑', '啞'), ('唤', '喚'), ('喷', '噴'), ('围', '圍'), ('圣', '聖'), ('块', '塊'), ('坛', '壇'), ('坝', '壩'), ('坟', '墳'), ('坠', '墜'), ('垄', '壟'), ('垒', '壘'), ('垦', '墾'), ('墙', '牆'), ('壮', '壯'), ('声', '聲'), ('壳', '殼'), ('处', '處'), ('复', '復'), ('够', '夠'), ('夹', '夾'), ('夺', '奪'), ('奋', '奮'), ('奖', '獎'), ('妇', '婦'), ('妈', '媽'), ('娱', '娛'), ('婴', '嬰'), ('婶', '嬸'), ('宁', '寧'), ('宝', '寶'), ('审', '審'), ('宫', '宮'), ('宽', '寬'), ('宾', '賓'), ('对', '對'), ('寻', '尋'), ('导', '導'), ('寿', '壽'), ('尔', '爾'), ('尘', '塵'), ('尽', '盡'), ('层', '層'), ('属', '屬'), ('屿', '嶼'), ('岂', '豈'), ('岗', '崗'), ('岛', '島'), ('峡', '峽'), ('崭', '嶄'), ('巩', '鞏'), ('币', '幣'), ('帐', '帳'), ('帘', '簾'), ('帜', '幟'), ('带', '帶'), ('帮', '幫'), ('庄', '莊'), ('庐', '廬'), ('庙', '廟'), ('庞', '龐'), ('开', '開'), ('异', '異'), ('弃', '棄'), ('弥', '彌'), ('彻', '徹'), ('径', '徑'), ('忆', '憶'), ('忧', '憂'), ('态', '態'), ('怜', '憐'), ('总', '總'), ('恳', '懇'), ('恶', '惡'), ('恼', '惱'), ('悦', '悅'), ('悬', '懸'), ('惊', '驚'), ('惧', '懼'), ('惨', '慘'), ('惩', '懲'), ('惯', '慣'), ('愿', '願'), ('懒', '懶'), ('戏', '戲'), ('户', '戶'), ('扑', '撲'), ('执', '執'), ('扩', '擴'), ('扫', '掃'), ('扬', '揚'), ('护', '護'), ('拟', '擬'), ('拢', '攏'), ('挚', '摯'), ('损', '損'), ('挤', '擠'), ('挥', '揮'), ('捞', '撈'), ('摆', '擺'), ('携', '攜'), ('摄', '攝'), ('摊', '攤'), ('撑', '撐'), ('攒', '攢'), ('数', '數'), ('旧', '舊'), ('昙', '曇'), ('晓', '曉'), ('暂', '暫'), ('术', '術'), ('机', '機'), ('杀', '殺'), ('杂', '雜'), ('条', '條'), ('来', '來'), ('杨', '楊'), ('极', '極'), ('构', '構'), ('枪', '槍'), ('标', '標'), ('栏', '欄'), ('树', '樹'), ('样', '樣'), ('欧', '歐'), ('歼', '殲'), ('残', '殘'), ('殴', '毆'), ('毁', '毀'), ('气', '氣'), ('汇', '匯'), ('汹', '洶'), ('沟', '溝'), ('没', '沒'), ('沪', '滬'), ('泪', '淚'), ('泽', '澤'), ('洁', '潔'), ('洒', '灑'), ('浇', '澆'), ('浊', '濁'), ('测', '測'), ('浏', '瀏'), ('浑', '渾'), ('浓', '濃'), ('湿', '濕'), ('滤', '濾'), ('滨', '濱'), ('滚', '滾'), ('滞', '滯'), ('滥', '濫'), ('潜', '潛'), ('濒', '瀕'), ('灿', '燦'), ('炉', '爐'), ('烂', '爛'), ('烛', '燭'), ('烟', '煙'), ('烦', '煩'), ('烧', '燒'), ('焕', '煥'), ('爱', '愛'), ('爷', '爺'), ('牍', '牘'), ('牵', '牽'), ('状', '狀'), ('犹', '猶'), ('狈', '狽'), ('独', '獨'), ('狭', '狹'), ('狮', '獅'), ('猎', '獵'), ('猪', '豬'), ('猫', '貓'), ('献', '獻'), ('玛', '瑪'), ('珠', '宝'), ('琐', '瑣'), ('瑶', '瑤'), ('电', '電'), ('畅', '暢'), ('疗', '療'), ('痒', '癢'), ('瘫', '癱'), ('皱', '皺'), ('盐', '鹽'), ('监', '監'), ('盖', '蓋'), ('盘', '盤'), ('盗', '盜'), ('着', '著'), ('睁', '睜'), ('睐', '睞'), ('瞒', '瞞'), ('矫', '矯'), ('矿', '礦'), ('码', '碼'), ('砚', '硯'), ('础', '礎'), ('硕', '碩'), ('确', '確'), ('碍', '礙'), ('祸', '禍'), ('离', '離'), ('种', '種'), ('积', '積'), ('称', '稱'), ('稳', '穩'), ('穷', '窮'), ('窃', '竊'))
SIMP_TRAD_MIN_HITS = 2


def script_mismatch_hits(quote, source_text):
    """引文（简）vs 原文（繁）的不一致信号数。"""
    if not quote or not source_text:
        return 0
    hits = 0
    for simp, trad in SIMP_TRAD_PAIRS:
        if simp in quote and trad in source_text and simp not in source_text:
            hits += 1
    return hits


def check_quote(quote, source_text, min_len: int = MIN_FRAGMENT):
    """N2/N3: 引文 vs 归一化原文 -> (result, detail).

    result in {matched, mismatch, script-mismatch, quote-too-short}; detail 是命中的片段或最长片段.
    """
    frags = fragments(quote, min_len=min_len)
    if not frags:
        return "quote-too-short", ""
    if not source_text:
        return "quote-too-short", frags[0]
    for frag in frags:
        if frag in source_text:
            return "matched", frag
    # N5 繁简守卫：原文是繁体、引文是简体时，字面比对没有意义 -> 不判不符（误报控制）
    if script_mismatch_hits(quote, source_text) >= SIMP_TRAD_MIN_HITS:
        return "script-mismatch", frags[0]
    return "mismatch", frags[0]


def load_cache(**kwargs) -> SourceTextCache:
    return SourceTextCache(**kwargs)
