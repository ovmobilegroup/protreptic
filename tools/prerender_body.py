"""tools/prerender_body.py -- Phase30-A2: 关键路由的静态正文快照.

背景 (Phase30-A0 之后的实测):
    tools/prerender_routes.py 只重写 head: 深链 404 变 200, 每路由的
    title / description / canonical / JSON-LD 都在静态 HTML 里. 但 body 仍是空的
    <div id="app"></div>, 正文要等站点脚本渲染出来: 线上实测 /protreptic/figures
    的静态体只有 2611 字节, 不执行 JS 的 UA (搜索爬虫 / 社交预览 / curl 类监测)
    拿到的是一个空白页.

本模块做什么:
    为关键路由生成一份静态正文快照, 直接写进 <div id="app">. 于是
      - 无 JS 的 UA 能读到标题与正文文本;
      - 有 JS 的浏览器在脚本启动前先看到这份快照, 脚本启动后被 Vue 覆盖
        (web/src/main.ts 在 mount 前清空 #app, 所以不会出现两份正文并存);
      - 不使用 createSSRApp / hydrate, 因此不存在 hydration mismatch.

覆盖范围 (与卡片验收对齐):
    - /figures /modes /templates 三个列表壳;
    - 7 个模板页: 正文取 dist/templates/*.md, 与前端 marked 用的是同一份 markdown;
    - 人物页 (CI 传 --body-persons all, 覆盖全部人物页; 本地默认按模式条数排序的前 40 名): 正文取
      dist/data/modes/by-figure/{code}.json 的定义 / 步骤 / 概念 / 出处 / 原话.
    其余路由仍按 A0 只做 head, 一样返回 200.

约定:
    - 快照只用 web/src 里已经出现过的 class (Tailwind 只扫 src/**, 新造的类不会被
      编译出样式), 观感与真实页面接近, 细节布局交给站点脚本渲染的那一份;
    - 文本一律中文, 与 SPA 默认 locale 一致;
    - 数据缺失只跳过对应片段, 不抛异常; 由 prerender_routes.py 的自检决定是否放行.
"""

from __future__ import annotations

import html
import json
import re
from pathlib import Path

BODY_ATTR = "data-prerender=\"v1\""
APP_SHELL = "<div id=\"app\"></div>"
TAG_RE = re.compile(r"<[^>]+>")
WS_RE = re.compile(r"\s+")


def esc(text) -> str:
    return html.escape(str(text if text is not None else ""), quote=False)


def truncate(text, limit: int) -> str:
    text = WS_RE.sub(" ", str(text or "")).strip()
    return text if len(text) <= limit else text[: limit - 1] + "…"


def pick(value) -> str:
    """前端 MindView 的 pick(): 字段可能是数组, 取第一个非空值."""
    if isinstance(value, list):
        for item in value:
            if item:
                return str(item)
        return ""
    return "" if value is None else str(value)


def as_list(value) -> list:
    if isinstance(value, list):
        return [str(v) for v in value if v not in (None, "")]
    if isinstance(value, str):
        text = value.strip()
        if text.startswith("["):
            try:
                parsed = json.loads(text)
            except Exception:
                parsed = None
            if isinstance(parsed, list):
                return [str(v) for v in parsed if v not in (None, "")]
        return [x.strip() for x in text.split("\n") if x.strip()]
    return []


def inline(text: str) -> str:
    out = esc(text)
    out = re.sub(r"`([^`]+)`", r"<code>\1</code>", out)
    out = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", out)
    out = re.sub(r"~~([^~]+)~~", r"<del>\1</del>", out)
    out = re.sub(r"(?<!\*)\*([^*\n]+)\*(?!\*)", r"<em>\1</em>", out)
    out = re.sub(r"!\[([^\]]*)\]\(([^)\s]+)\)", r"<img src=\"\2\" alt=\"\1\" />", out)
    out = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", r"<a href=\"\2\">\1</a>", out)
    return out


def _table_cells(line: str) -> list:
    s = line.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|"):
        s = s[:-1]
    return [c.strip() for c in s.split("|")]


def _is_table_sep(line: str) -> bool:
    s = line.strip()
    if "|" not in s or "-" not in s:
        return False
    return re.match(r"^[|\s:\-]+$", s) is not None


def md_to_html(md: str) -> str:
    """GFM 子集 -> HTML. 支持标题 / 段落 / 有序无序列表 / 引用 / 表格 / 围栏代码 / 分隔线.

    前端用 marked 渲染模板页; 这里不引依赖 (CI 的 prerender 步骤只有标准库), 只做
    模板 markdown 实际用到的子集, 覆盖不到的原样输出文本, 不会丢内容.
    """
    lines = (md or "").replace("\r\n", "\n").split("\n")
    out = []
    i = 0
    total = len(lines)
    while i < total:
        s = lines[i].strip()
        if not s:
            i += 1
            continue
        if s.startswith("```"):
            lang = s[3:].strip()
            i += 1
            buf = []
            while i < total and not lines[i].strip().startswith("```"):
                buf.append(lines[i])
                i += 1
            i += 1
            cls = " class=\"language-%s\"" % esc(lang) if lang else ""
            out.append("<pre><code%s>%s</code></pre>" % (cls, esc("\n".join(buf))))
            continue
        m = re.match(r"^(#{1,6})\s+(.*)$", s)
        if m:
            lvl = len(m.group(1))
            out.append("<h%d>%s</h%d>" % (lvl, inline(m.group(2)), lvl))
            i += 1
            continue
        if re.match(r"^(-{3,}|\*{3,}|_{3,})$", s):
            out.append("<hr />")
            i += 1
            continue
        if s.startswith("|") and i + 1 < total and _is_table_sep(lines[i + 1]):
            head = _table_cells(s)
            i += 2
            rows = []
            while i < total and lines[i].strip().startswith("|"):
                rows.append(_table_cells(lines[i]))
                i += 1
            parts = ["<table><thead><tr>"]
            for cell in head:
                parts.append("<th>%s</th>" % inline(cell))
            parts.append("</tr></thead><tbody>")
            for row in rows:
                parts.append("<tr>")
                for cell in row:
                    parts.append("<td>%s</td>" % inline(cell))
                parts.append("</tr>")
            parts.append("</tbody></table>")
            out.append("".join(parts))
            continue
        if s.startswith(">"):
            buf = []
            while i < total and lines[i].strip().startswith(">"):
                buf.append(lines[i].strip()[1:].strip())
                i += 1
            out.append("<blockquote>%s</blockquote>" % md_to_html("\n".join(buf)))
            continue
        um = re.match(r"^[-*+]\s+(.*)$", s)
        om = re.match(r"^(\d+)[.)]\s+(.*)$", s)
        if um or om:
            ordered = om is not None
            items = []
            while i < total:
                cur = lines[i].strip()
                if ordered:
                    m2 = re.match(r"^(\d+)[.)]\s+(.*)$", cur)
                    item = m2.group(2) if m2 else None
                else:
                    m2 = re.match(r"^[-*+]\s+(.*)$", cur)
                    item = m2.group(1) if m2 else None
                if item is not None:
                    items.append(item)
                    i += 1
                    continue
                if not cur or cur.startswith("#") or cur.startswith("|") or cur.startswith("```") or cur.startswith(">"):
                    break
                if re.match(r"^[-*+]\s+", cur) or re.match(r"^\d+[.)]\s+", cur):
                    break
                if items:
                    items[-1] = items[-1] + " " + cur
                    i += 1
                    continue
                break
            tag = "ol" if ordered else "ul"
            out.append("<%s>%s</%s>" % (tag, "".join("<li>%s</li>" % inline(x) for x in items), tag))
            continue
        buf = [s]
        i += 1
        while i < total:
            nxt = lines[i].strip()
            if not nxt or nxt.startswith("#") or nxt.startswith("|") or nxt.startswith("```") or nxt.startswith(">"):
                break
            if re.match(r"^[-*+]\s+", nxt) or re.match(r"^\d+[.)]\s+", nxt):
                break
            if re.match(r"^(-{3,}|\*{3,}|_{3,})$", nxt):
                break
            buf.append(nxt)
            i += 1
        out.append("<p>%s</p>" % inline(" ".join(buf)))
    return "\n".join(out)


def _strip_frontmatter(text: str) -> str:
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            nxt = text.find("\n", end + 1)
            if nxt != -1:
                return text[nxt + 1:]
    return text


def render_template(tid: str, md_text: str) -> str:
    text = _strip_frontmatter(md_text or "")
    m = re.search(r"^#\s+(.+)$", text, re.M)
    title = m.group(1).strip() if m else tid.upper()
    body = re.sub(r"^#\s+.+\n?", "", text, count=1, flags=re.M)
    head = "<div class=\"pt-container pb-20 pt-8\"><article class=\"pt-panel overflow-hidden\">"
    head += "<header class=\"relative overflow-hidden border-b border-white/[0.08] px-7 py-8 sm:px-10 sm:py-10\">"
    head += "<div class=\"relative mb-3 flex flex-wrap items-center gap-2\">"
    head += "<span class=\"pt-code\">%s</span><span class=\"pt-chip-gold\">复盘模板</span></div>"
    head += "<h1 class=\"pt-h1 !text-3xl sm:!text-4xl\">%s</h1></header><div class=\"pt-prose px-7 py-8 sm:px-10 sm:py-10\">"
    head += "%s</div></article></div>"
    return head % (esc(tid.upper()), esc(title), md_to_html(body))


def _mode_block(idx: int, mode: dict) -> list:
    parts = ["<article class=\"pt-panel p-7\">"]
    parts.append("<div class=\"mb-4 flex flex-wrap items-center gap-2\">")
    badge = "<span class=\"grid h-7 w-7 place-items-center rounded-full border border-gold-500/40"
    badge += " bg-gold-500/10 font-mono text-xs font-bold text-gold-300\">%d</span>"
    parts.append(badge % (idx + 1))
    name = pick(mode.get("name_zh")) or pick(mode.get("name_en")) or str(mode.get("mode_code") or "")
    parts.append("<h2 class=\"pt-h3 text-parchment\">%s</h2>" % esc(name))
    domain = truncate(pick(mode.get("domain_zh")), 60)
    if domain:
        parts.append("<span class=\"pt-chip-jade ml-auto\">%s</span>" % esc(domain))
    parts.append("</div>")
    definition = pick(mode.get("definition_zh"))
    if definition:
        parts.append("<p class=\"leading-relaxed text-parchment/70\">%s</p>" % esc(definition))
    steps = as_list(mode.get("process_zh"))
    if steps:
        parts.append("<h3 class=\"mb-2 mt-4 text-xs uppercase tracking-wider text-parchment/40\">操作步骤</h3>")
        parts.append("<ol class=\"space-y-2\">")
        for j, step in enumerate(steps):
            parts.append("<li class=\"flex gap-3 text-sm text-parchment/65\">"
                         "<span class=\"font-mono text-gold-400/70\">%d.</span><span>%s</span></li>" % (j + 1, esc(step)))
        parts.append("</ol>")
    concepts = as_list(mode.get("key_concepts"))
    if concepts:
        parts.append("<div class=\"mt-4 flex flex-wrap items-center gap-2\">")
        for concept in concepts[:8]:
            parts.append("<span class=\"pt-chip-mute\">%s</span>" % esc(concept))
        parts.append("</div>")
    source = pick(mode.get("source_chapter"))
    if source:
        parts.append("<p class=\"mt-4 text-sm text-parchment/55\">出处：%s</p>" % esc(source))
    quote = pick(mode.get("key_quote_zh"))
    if quote:
        parts.append("<p class=\"mt-2 text-sm text-gold-200/90\">原话：%s</p>" % esc(quote))
    for label, key in (("代表案例", "representative_cases_zh"), ("现代应用", "modern_applications_zh")):
        items = as_list(mode.get(key))
        if not items:
            continue
        parts.append("<h3 class=\"mb-2 mt-4 text-xs uppercase tracking-wider text-parchment/40\">%s</h3>" % label)
        parts.append("<ul class=\"space-y-2\">")
        for item in items[:3]:
            parts.append("<li class=\"flex gap-3 text-sm text-parchment/65\"><span>%s</span></li>" % esc(item))
        parts.append("</ul>")
    parts.append("</article>")
    return parts


def render_person(payload: dict, max_modes: int = 12) -> str:
    code = str(payload.get("figure_code") or "")
    name = payload.get("figure_name") or code
    modes = payload.get("modes") or []
    count = payload.get("count") or len(modes)
    parts = ["<div class=\"pt-container pb-20 pt-8\">"]
    parts.append("<header class=\"pt-panel relative mb-8 overflow-hidden p-7\">")
    parts.append("<div class=\"mb-3 flex flex-wrap items-center gap-2\">")
    parts.append("<span class=\"pt-code\">%s</span>" % esc(code))
    parts.append("<span class=\"pt-chip-jade\">%d 条模式</span>" % count)
    parts.append("</div>")
    parts.append("<h1 class=\"pt-h1 !text-4xl sm:!text-5xl\">%s</h1>" % esc(name))
    parts.append("<p class=\"mt-3 text-sm text-parchment/55\">以下为该历史人物的思维模式档案，含定义、操作步骤、出处与原话。</p>")
    parts.append("</header>")
    parts.append("<div class=\"space-y-6\">")
    for idx, mode in enumerate(modes[:max_modes]):
        parts.extend(_mode_block(idx, mode))
    parts.append("</div>")
    if len(modes) > max_modes:
        parts.append("<p class=\"mt-6 text-sm text-parchment/55\">其余 %d 条模式由站点脚本渲染后显示。</p>" % (len(modes) - max_modes))
    parts.append("</div>")
    return "".join(parts)


def render_figures_shell(unified: dict, sample: int = 60) -> str:
    items = unified.get("items") or []
    figures = [it for it in items if it.get("type") == "figure"]
    scenarios = [it for it in items if it.get("type") == "scenario"]
    picked = figures[:sample]
    parts = ["<div class=\"pt-container pb-16 pt-10\">"]
    parts.append("<section class=\"relative mb-10\">")
    parts.append("<div class=\"mb-3 flex items-center gap-3\"><span class=\"pt-hairline w-10\"></span>"
                 "<span class=\"pt-code\">思想名录 · 人物 × 场景</span></div>")
    parts.append("<h1 class=\"pt-h1\"><span class=\"pt-gradient-text\">以人为鉴，明得失</span></h1>")
    parts.append("<p class=\"mt-4 max-w-2xl text-base leading-relaxed text-parchment/70\">"
                 "%d 位历史人物的思维方法与 %d 个现代处境场景，汇成同一份可检索的名录——每条都有出处与操作步骤，中英双语。</p>" % (len(figures), len(scenarios)))
    parts.append("<div class=\"mt-6 flex flex-wrap items-center gap-2\">")
    parts.append("<span class=\"pt-chip-gold\">人物 %d</span>" % len(figures))
    parts.append("<span class=\"pt-chip-jade\">场景 %d</span>" % len(scenarios))
    parts.append("</div></section>")
    parts.append("<section class=\"pt-panel p-7\">")
    parts.append("<h2 class=\"pt-h3 text-parchment\">人物名录（静态快照前 %d 位）</h2>" % len(picked))
    parts.append("<ul class=\"mt-4 space-y-2\">")
    for it in picked:
        parts.append("<li class=\"flex flex-wrap items-center gap-2\"><span class=\"pt-code\">%s</span>"
                     "<span class=\"text-parchment/85\">%s</span>"
                     "<span class=\"pt-chip-mute\">%s 条模式</span></li>" % (esc(it.get("code")), esc(it.get("name") or it.get("code")), esc(it.get("n_modes") or 0)))
    parts.append("</ul>")
    parts.append("<p class=\"mt-5 text-sm text-parchment/55\">完整名录共 %d 条（人物 %d + 场景 %d），含检索、类型切换与筛选，由站点脚本渲染后显示。</p>" % (len(items), len(figures), len(scenarios)))
    parts.append("</section></div>")
    return "".join(parts)


def render_modes_shell(dist: Path, sample: int = 60, shards: int = 8) -> str:
    modes = []
    for i in range(shards):
        f = dist / "data" / "modes" / ("index-%d.json" % i)
        if not f.is_file():
            continue
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            continue
        if isinstance(data, list):
            modes.extend(data)
    cats = {}
    for m in modes:
        c = pick(m.get("category")) or "未分类"
        cats[c] = cats.get(c, 0) + 1
    top_cats = sorted(cats.items(), key=lambda kv: (-kv[1], kv[0]))[:12]
    picked = sorted(modes, key=lambda m: str(m.get("mode_code") or ""))[:sample]
    parts = ["<div class=\"pt-container pb-16 pt-10\">"]
    parts.append("<section class=\"relative mb-10\">")
    parts.append("<div class=\"mb-3 flex items-center gap-3\"><span class=\"pt-hairline w-10\"></span>"
                 "<span class=\"pt-code\">思维模式库 · 可执行方法</span></div>")
    parts.append("<h1 class=\"pt-h1\"><span class=\"pt-gradient-text\">把案例拆成可复用的方法</span></h1>")
    parts.append("<p class=\"mt-4 max-w-2xl text-base leading-relaxed text-parchment/70\">"
                 "共 %d 条思维模式，每条含定义、操作步骤、出处与原话，中英双语。</p>" % len(modes))
    parts.append("</section>")
    parts.append("<section class=\"pt-panel p-7\">")
    parts.append("<h2 class=\"pt-h3 text-parchment\">分类分布（静态快照）</h2>")
    parts.append("<div class=\"mt-4 flex flex-wrap items-center gap-2\">")
    for c, n in top_cats:
        parts.append("<span class=\"pt-chip-mute\">%s %d</span>" % (esc(c), n))
    parts.append("</div></section>")
    parts.append("<section class=\"pt-panel mt-6 p-7\">")
    parts.append("<h2 class=\"pt-h3 text-parchment\">模式样例（按编号前 %d 条）</h2>" % len(picked))
    parts.append("<ul class=\"mt-4 space-y-2\">")
    for m in picked:
        parts.append("<li class=\"flex flex-wrap items-center gap-2\"><span class=\"pt-code\">%s</span>"
                     "<span class=\"text-parchment/85\">%s</span>"
                     "<span class=\"text-sm text-parchment/55\">%s · %s</span></li>" % (esc(m.get("mode_code") or m.get("id")), esc(pick(m.get("name_zh"))), esc(pick(m.get("figure_name"))), esc(truncate(pick(m.get("domain_zh")), 40))))
    parts.append("</ul>")
    parts.append("<p class=\"mt-5 text-sm text-parchment/55\">完整 %d 条（含检索与分类筛选）由站点脚本渲染后显示。</p>" % len(modes))
    parts.append("</section></div>")
    return "".join(parts)


def render_templates_shell(entries: list, note: str = "") -> str:
    parts = ["<div class=\"pt-container pb-16 pt-10\">"]
    parts.append("<section class=\"relative mb-10\">")
    parts.append("<div class=\"mb-3 flex items-center gap-3\"><span class=\"pt-hairline w-10\"></span>"
                 "<span class=\"pt-code\">复盘模板库 · 历史案例工具</span></div>")
    parts.append("<h1 class=\"pt-h1\"><span class=\"pt-gradient-text\">把历史决策现场转成复盘清单</span></h1>")
    parts.append("<p class=\"mt-4 max-w-2xl text-base leading-relaxed text-parchment/70\">"
                 "把赤壁、隆中对等 %d 个历史经典案例转化为可直接套用的复盘模板。</p>" % len(entries))
    parts.append("</section>")
    parts.append("<section class=\"pt-panel p-7\"><h2 class=\"pt-h3 text-parchment\">模板清单</h2>")
    parts.append("<ul class=\"mt-4 space-y-2\">")
    for tid, title in entries:
        parts.append("<li class=\"flex flex-wrap items-center gap-2\"><span class=\"pt-code\">%s</span>"
                     "<span class=\"text-parchment/85\">%s</span></li>" % (esc(str(tid).upper()), esc(title)))
    parts.append("</ul>")
    parts.append("<p class=\"mt-5 text-sm text-parchment/55\">每个模板含适用场景、标准化步骤与检查清单，正文由站点脚本渲染后显示。</p>")
    parts.append("</section></div>")
    return "".join(parts)


def inject_body(shell: str, body_html: str) -> str:
    """把快照写进 #app. Vue 的 createApp 不会自动清空容器, 所以 main.ts 在 mount
    之前先清空 #app, 保证不会出现静态快照与渲染结果两份正文并存."""
    if APP_SHELL not in shell:
        raise ValueError("index.html 里找不到 <div id=\"app\"></div> 锚点")
    block = "<div id=\"app\"><div %s>%s</div></div>" % (BODY_ATTR, body_html)
    return shell.replace(APP_SHELL, block, 1)


def plain_text(markup: str) -> str:
    return WS_RE.sub(" ", TAG_RE.sub(" ", markup or "")).strip()


def collect_bodies(routes: list, dist: Path, persons: int | None = 40, max_modes: int = 12) -> dict:
    """关键路由 -> 静态正文快照. 生成清单:
      /figures /modes /templates 列表壳 + 7 个模板页 + 人物页 (persons 条).
    persons=None 时覆盖全部人物页; persons=0 时不生成人物页快照.
    数据缺失只跳过, 不抛异常."""
    bodies = {}
    tpl_dir = dist / "templates"
    tpl_entries = []
    for route in routes:
        if route.get("type") != "template":
            continue
        tid = route["path"].rsplit("/", 1)[-1]
        tpl_entries.append((tid, route.get("name") or tid))
        f = tpl_dir / ("%s.md" % tid)
        if not f.is_file():
            continue
        bodies[route["path"]] = render_template(tid, f.read_text(encoding="utf-8"))
    paths = {r["path"] for r in routes}
    unified_path = dist / "data" / "index.unified.json"
    if "figures" in paths and unified_path.is_file():
        try:
            unified = json.loads(unified_path.read_text(encoding="utf-8"))
        except Exception:
            unified = {}
        if unified.get("items"):
            bodies["figures"] = render_figures_shell(unified)
    if "modes" in paths:
        shell = render_modes_shell(dist)
        if shell:
            bodies["modes"] = shell
    if "templates" in paths and tpl_entries:
        bodies["templates"] = render_templates_shell(tpl_entries)
    ranked_all = sorted([r for r in routes if r.get("type") == "person"],
                    key=lambda r: (-(r.get("n_modes") or 0), r["path"]))
    ranked = ranked_all if persons is None else ranked_all[: max(0, persons)]
    for route in ranked:
        f = dist / "data" / "modes" / "by-figure" / ("%s.json" % route.get("code"))
        if not f.is_file():
            continue
        try:
            payload = json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            continue
        bodies[route["path"]] = render_person(payload, max_modes=max_modes)
    return bodies


def check_bodies(dist: Path, routes: list, min_chars: int = 200) -> list:
    """自检: 声明了正文快照的路由必须真的带上标记, 且纯文本长度不低于 min_chars."""
    bad = []
    for route in routes:
        if not route.get("body"):
            continue
        f = dist / route["path"] / "index.html"
        if not f.is_file():
            bad.append("%s: 文件缺失" % route["path"])
            continue
        text = f.read_text(encoding="utf-8")
        if BODY_ATTR not in text:
            bad.append("%s: 没有正文快照标记" % route["path"])
            continue
        if len(plain_text(text)) < min_chars:
            bad.append("%s: 正文纯文本不足 %d 字" % (route["path"], min_chars))
    return bad
