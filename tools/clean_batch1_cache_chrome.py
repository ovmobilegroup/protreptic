#!/usr/bin/env python3
"""clean_batch1_cache_chrome.py -- 清掉 W8 批1 缓存里 render 通道带出的页面外壳。

render（action=parse）通道转换后，页面头尾会残留：首行 `mw-parser-output"...dir="ltr">`
断标签，及页尾「公有领域」许可块（简/繁/英文三种形式）。 本工具只动 W8 批1 独立索引
登记的缓存文件：清理后重算 sha256/字符数并回写 `data/audit/source_texts_w8_stage2_batch1.json`。
对读是子串匹配，清理只去掉外壳、不改正文；**零主库写入**。"""
from __future__ import annotations

import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
INDEX = REPO / "data" / "audit" / "source_texts_w8_stage2_batch1.json"
HEAD_RE = re.compile(r'^mw-parser-output[^\n]*\n+')
TAIL_MARKS = [
    "\u6b64\u4f5c\u54c1\u5728\u5168\u4e16\u754c\u90fd\u5c5e\u4e8e\u516c\u6709\u9886\u57df",
    "\u6b64\u4f5c\u54c1\u5728\u5168\u4e16\u754c\u90fd\u5c6c\u65bc\u516c\u6709\u9818\u57df",
    "\u516c\u6709\u9886\u57df",
    "Public domain",
]


def clean_text(t):
    t = HEAD_RE.sub("", t)
    m = re.search(r"\n+Public domain[^\n]*\s*$", t)
    if m:
        t = t[:m.start()]
    for mk in TAIL_MARKS[:2]:
        i = t.rfind(mk)
        if i != -1 and (len(t) - i) < 400:
            t = t[:i]
    t = re.sub(r"\s+$", "", t) + "\n"
    return t


def main():
    doc = json.loads(INDEX.read_text(encoding="utf-8"))
    touched = 0
    for e in doc.get("entries", []):
        pairs = [(e, e.get("file")), (e.get("zh_cn") or {}, (e.get("zh_cn") or {}).get("file"))]
        for meta, f in pairs:
            if not f:
                continue
            p = REPO / f
            if not p.is_file():
                continue
            t = p.read_text(encoding="utf-8")
            c = clean_text(t)
            if c != t:
                p.write_text(c, encoding="utf-8")
                touched += 1
            raw = c.encode("utf-8")
            import hashlib
            meta["sha256"] = hashlib.sha256(raw).hexdigest()
            meta["chars"] = len(c)
            meta["bytes"] = len(raw)
        if e.get("pages"):
            pass
    INDEX.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("[OK] cleaned files=%d; index sha/chars updated -> %s" % (touched, INDEX))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
