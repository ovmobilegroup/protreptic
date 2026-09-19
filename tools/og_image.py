#!/usr/bin/env python3
"""og_image.py -- Phase30-A3 社交分享图 (og:image) 的共享契约.

为什么要单独一个模块
    「哪条路由用哪张分享图」必须有三处完全一致的答案:
      1) tools/build_og_images.py       构建期把 PNG 画进 dist/og/ 并写 dist/og/manifest.json
      2) tools/prerender_routes.py      给每个预渲染页面写 og:image / twitter:image 时查 manifest
      3) web/src/composables/useSeo.ts  SPA 站内跳转后更新 head (TypeScript 侧的镜像)
    规则只写在这里一份; 前端那份是镜像, 改动必须两边同时改.

路径契约 (route path 一律不带 base、不带首尾斜杠)
    ''            -> og/site.png              站点首页
    figures       -> og/pages/figures.png     /figures 列表
    modes         -> og/pages/modes.png       /modes 列表
    templates     -> og/pages/templates.png   /templates 列表
    api           -> og/pages/api.png         /api 列表
    minds/<code>  -> og/minds/<code>.png      人物: 姓名 + 模式数 + 时代
    figures/<code>-> og/figures/<code>.png    场景: 名称 + 领域 + 模式数
    templates/<id>-> og/templates/<id>.png    模板: 标题
    其他/未知      -> og/site.png

    文件名用原始编码 (只允许 [A-Za-z0-9._-] 与空格, 实测全库只有 "Sun Quan" 带空格);
    URL 由 urllib.parse.quote 做百分号编码, 前端用 encodeURIComponent 得到同一结果.

排版字段的来源
    文案全部来自 index.unified.json / meta.json / 模板 markdown 的真实字段, 不臆造人名、时代或描述;
    时代字段最长的一条实测 468 字, 一律先截断再排版 (short_era).
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from urllib.parse import quote

SITE_ORIGIN = "https://ovmobilegroup.github.io"
SITE_NAME = "Protreptic 思想典藏"
SITE_TAGLINE = "以人为鉴，明得失"
SITE_HOST_LABEL = "ovmobilegroup.github.io/protreptic"
OG_WIDTH = 1200
OG_HEIGHT = 630
OG_DIR = "og"
DEFAULT_BASE = "/protreptic/"
MANIFEST_NAME = "manifest.json"

# 路由里 code 的允许字符: 目录分隔符绝对不允许 (会写到 dist/og 之外), 空格允许 (URL 里编码)
UNSAFE_CODE_CHARS = set('/\\:*?"<>|\x00')

# 领域 token -> 中文标签. 全库实测 37 个取值 (16 个主力 + 21 个零散), 未收录的原样显示.
DOMAIN_ZH = {
    "Operational": "行动", "Analytical": "分析", "Systems": "系统", "Strategic": "战略",
    "Personal": "个人", "Ethics": "伦理", "Collaborative": "协作", "Governance": "治理",
    "Military": "军事", "Literature_Arts": "文史", "Philosophy": "哲学", "Science_Tech": "科技",
    "Economics": "经济", "Historiography": "史学", "Education": "教育", "Creative": "创造",
    "Religion": "宗教", "statecraft": "治国", "Natural Philosophy": "自然哲学",
    "Critical Thinking": "批判思维", "Logic": "逻辑", "Epistemology": "认识论",
    "political_philosophy": "政治哲学", "religion": "宗教", "diplomacy": "外交",
    "institutional_design": "制度设计", "military_strategy": "军事战略",
    "gunpowder_warfare": "火器战法", "feudal_reform": "变法", "economics": "经济",
    "political science": "政治学", "ethics": "伦理", "astronomy": "天文",
    "mathematics": "数学", "geography": "地理", "anatomy": "解剖", "medicine": "医学",
}

# 装饰性字符 (emoji / 箭头 / 变体选择符): 分享图字体不含这些字形, 排版前直接剥掉.
# 注意: 只剥这些区间; 汉字/拉丁字母缺字形会让构建失败, 不允许静默丢弃.
DECORATIVE_RANGES = (
    (0x1F000, 0x1FAFF),
    (0x2190, 0x21FF),
    (0x2300, 0x23FF),
    (0x25A0, 0x27BF),
    (0x2B00, 0x2BFF),
    (0x3030, 0x3030),
    (0xFE00, 0xFE0F),
    (0xFE30, 0xFE4F),
    (0x200D, 0x200D),
    (0x20E3, 0x20E3),
)

_SPLIT_RE = re.compile(r"\s*[：:]\s*|\s+[—-]{1,2}\s+")


def is_decorative(ch: str) -> bool:
    code = ord(ch)
    if ch in ("\u200d", "\ufe0f"):
        return True
    return any(lo <= code <= hi for lo, hi in DECORATIVE_RANGES)


def strip_decorative(text: str) -> str:
    return "".join(ch for ch in (text or "") if not is_decorative(ch))


def truncate(text: str, limit: int) -> str:
    text = re.sub(r"\s+", " ", strip_decorative(text or "")).strip()
    if len(text) <= limit:
        return text
    return text[: max(1, limit - 1)].rstrip() + "…"


def split_title(name: str, main_limit: int = 20) -> tuple:
    """「龚自珍：换了人间的启蒙诗史家」这类名字拆成主名 + 副题, 主名过长时不再拆."""
    name = re.sub(r"\s+", " ", strip_decorative(name or "")).strip()
    if not name:
        return "", ""
    parts = _SPLIT_RE.split(name, maxsplit=1)
    if len(parts) == 2 and parts[0].strip() and len(parts[0].strip()) <= main_limit:
        return parts[0].strip(), truncate(parts[1], 34)
    return truncate(name, 26), ""


def short_era(era: str, limit: int = 26) -> str:
    """时代字段截断: 先砍括号/破折号之后的长注解, 再按字数截断."""
    era = re.sub(r"\s+", " ", strip_decorative(era or "")).strip()
    if not era:
        return ""
    for sep in ("（", "(", "；", ";", "——", "—", "：", ":"):
        head = era.split(sep, 1)[0].strip()
        if head and len(head) >= 2:
            era = head
            break
    return truncate(era, limit)


def domain_labels(tokens, limit: int = 3) -> list:
    out = []
    for token in tokens or []:
        label = DOMAIN_ZH.get(str(token), str(token).strip())
        if label and label not in out:
            out.append(label)
        if len(out) >= limit:
            break
    return out


def og_rel_path(route_path: str) -> str:
    """路由路径 -> dist 内相对路径 (斜杠分隔, 未做百分号编码)."""
    path = str(route_path or "").strip("/")
    if not path:
        return "%s/site.png" % OG_DIR
    head, _, tail = path.partition("/")
    if not tail:
        if head in ("daily", "figures", "modes", "templates", "api"):
            return "%s/pages/%s.png" % (OG_DIR, head)
        return "%s/site.png" % OG_DIR
    if "/" in tail:
        return "%s/site.png" % OG_DIR
    for ch in tail:
        if ch in UNSAFE_CODE_CHARS:
            raise ValueError("route code 含不安全字符: %r" % route_path)
    if head == "minds":
        return "%s/minds/%s.png" % (OG_DIR, tail)
    if head == "figures":
        return "%s/figures/%s.png" % (OG_DIR, tail)
    if head == "templates":
        return "%s/templates/%s.png" % (OG_DIR, tail)
    return "%s/site.png" % OG_DIR


def og_url(route_path: str, base: str = DEFAULT_BASE) -> str:
    """og:image / twitter:image 用的绝对 URL (已百分号编码, 与前端 encodeURIComponent 对齐)."""
    base = base if base.endswith("/") else base + "/"
    return SITE_ORIGIN + base + quote(og_rel_path(route_path), safe="/")


def page_url(route_path: str, base: str = DEFAULT_BASE) -> str:
    base = base if base.endswith("/") else base + "/"
    path = str(route_path or "").strip("/")
    if not path:
        return SITE_ORIGIN + base
    return SITE_ORIGIN + base + quote(path, safe="/") + "/"


def load_template_titles(templates_dir) -> list:
    """模板 markdown 的 h1 当作分享图标题 (与 prerender_routes.md_title_desc 同源同规则)."""
    out = []
    for md in sorted(Path(templates_dir).glob("*.md")):
        title = md.stem
        for line in md.read_text(encoding="utf-8").splitlines():
            s = line.strip()
            if s.startswith("# "):
                title = truncate(strip_decorative(s[2:]), 22)
                break
        out.append((md.stem, title))
    return out


def unified_counts(index: dict, meta: dict = None) -> dict:
    items = list(index.get("items") or [])
    persons = sum(1 for i in items if i.get("type") == "figure")
    scenarios = sum(1 for i in items if i.get("type") == "scenario")
    modes = 0
    if isinstance(meta, dict):
        counts = meta.get("counts") or {}
        # 站点口径 = 真正发布出去的模式摘要条数（modes/index-*.json 的合计）。
        # modes_raw(2868) 是未去重的源记录；mode_summaries(2858) 里还含 10 条被隔离的
        # 伪造模式（H-SX-001 M393-M402）—— 站上搜不到也打不开，不能拿它们当门面数字。
        # 字段缺失时逐级回落，老产物仍能出图。
        for key in ("mode_summaries_published", "mode_summaries", "modes_deduped", "modes_raw"):
            if counts.get(key):
                modes = int(counts[key])
                break
    if not modes:
        modes = sum(int(i.get("n_modes") or 0) for i in items)
    return {"persons": persons, "scenarios": scenarios, "modes": modes,
            "register": persons + scenarios}


def build_specs(index: dict, meta, templates_dir) -> list:
    """所有分享图的文案规格.

    [{route, kind, kicker, title, subtitle, summary, chips, seal, code, alt, image}]
    """
    counts = unified_counts(index, meta)
    specs = []

    def add(route, kind, kicker, title, subtitle, summary, chips, seal, code, alt):
        specs.append({
            "route": route, "kind": kind, "kicker": kicker, "title": title,
            "subtitle": subtitle, "summary": summary,
            "chips": [c for c in chips if c], "seal": seal, "code": code, "alt": alt,
        })

    add(
        "", "site", "思想典藏 · Archive of Minds",
        "Protreptic 思想典藏", "历史人物思维模式库 · 中英双语",
        "每条都有出处、操作步骤与现代应用。以人为鉴，明得失。",
        ["%d 条思维模式" % counts["modes"],
         "%d 位历史人物" % counts["persons"],
         "%d 个现代场景" % counts["scenarios"]],
        "思", "", "%s — %d 条思维模式 × %d 位历史人物" % (SITE_NAME, counts["modes"], counts["persons"]),
    )
    add(
        "daily", "page", "每日一模式 · 日期取模",
        "每日一模式", "一天一条思维模式，同一天重复打开结果一致",
        "按「这一天是第几天 mod 模式总数」选出：谁都不掷骰子，因此可复现、可回看任意历史日期。",
        ["日期取模 · 同一天恒定", "可回看任意历史日期"],
        "日", "", "每日一模式 — 按日期取模选一条思维模式，同一天重复打开结果一致",
    )
    add(
        "figures", "page", "统一名录 · 人物与场景",
        "历史人物库", "人物与场景的统一检索入口，中英双语",
        "每条都有出处、操作步骤与现代应用；支持按类型、时代、领域筛选，也可直接搜索。",
        ["%d 位历史人物" % counts["persons"], "%d 个现代场景" % counts["scenarios"],
         "%d 条名录" % counts["register"]],
        "鉴", "", "历史人物库 — %d 位历史人物 + %d 个现代场景" % (counts["persons"], counts["scenarios"]),
    )
    add(
        "modes", "page", "可执行方法总览",
        "思维模式库", "从历史案例里提炼的思维模式总览",
        "每条模式都有定义、操作步骤、出处与原话，可直接拿去用在今天的决策里。",
        ["%d 条思维模式" % counts["modes"], "定义 · 步骤 · 出处 · 原话"],
        "式", "", "思维模式库 — %d 条可执行方法" % counts["modes"],
    )
    add(
        "templates", "page", "历史案例 · 复盘工具",
        "复盘模板库", "把经典历史案例转成可直接套用的复盘模板",
        "赤壁、隆中对、白帝城托孤等 7 个案例，每个都拆成可勾选的复盘清单。",
        ["7 个历史经典案例", "可直接套用"],
        "复", "", "复盘模板库 — 7 个历史经典案例的复盘模板",
    )
    add(
        "api", "page", "静态数据 · 无后端",
        "API 文档", "Protreptic 静态数据分片与数据结构说明",
        "全部数据以 JSON 分片发布，无需服务器即可二次开发；结构说明与字段含义见页面。",
        ["JSON 分片", "无需服务器"],
        "数", "", "Protreptic API 文档 — 静态数据分片说明",
    )

    for item in index.get("items") or []:
        code = str(item.get("code") or "")
        name = str(item.get("name") or code)
        n_modes = int(item.get("n_modes") or 0)
        main, sub = split_title(name)
        summary = truncate(item.get("description") or "", 96)
        if item.get("type") == "figure":
            era = short_era(item.get("era") or "")
            chips = [("时代 · %s" % era) if era else "时代待核",
                     "%d 条思维模式" % n_modes] + domain_labels(item.get("domains"))
            add("minds/%s" % code, "person", "历史人物 · 思维模式档案", main, sub, summary, chips,
                main[:1], code, "%s的思维模式档案（%d 条）— %s" % (name, n_modes, SITE_NAME))
        else:
            labels = domain_labels(item.get("domains"))
            era = short_era(item.get("era") or "")
            chips = [("领域 · %s" % " · ".join(labels)) if labels else "现代场景",
                     "%d 条关联模式" % n_modes]
            if era:
                chips.append("时代 · %s" % era)
            add("figures/%s" % code, "scenario", "现代场景 · 关联模式档案", main, sub, summary, chips,
                main[:1], code,
                "%s（%s）关联的 %d 条思维模式 — %s" % (name, code, n_modes, SITE_NAME))

    for tid, title in load_template_titles(templates_dir):
        main, sub = split_title(title)
        add("templates/%s" % tid, "template", "历史案例 · 复盘模板", main,
            sub or "把历史决策现场转成可直接套用的复盘清单", "",
            ["复盘模板", "可直接套用"], main[:1], tid,
            "复盘模板：%s — %s" % (title, SITE_NAME))

    seen = set()
    for spec in specs:
        spec["image"] = og_rel_path(spec["route"])
        if spec["image"] in seen:
            raise ValueError("分享图路径重复: %s" % spec["image"])
        seen.add(spec["image"])
    return specs


def spec_chars(specs: list) -> set:
    """排版要用到的全部字符 (供字体子集化与字形自检使用). 新增字段必须一并加进来."""
    chars = set()
    for spec in specs:
        for field in ("title", "subtitle", "summary", "kicker", "seal", "code", "alt"):
            chars |= set(str(spec.get(field) or ""))
        for chip in spec.get("chips") or []:
            chars |= set(str(chip))
    return chars


def load_json(path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))
