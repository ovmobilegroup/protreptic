#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase21-R6C 产物构建器（卡 t_4a9cf2cb；只读数据层，仅写产物文件）

输入（构建时点）：
  docs/scratch/legacy20_r6c/r6c_archive_manifest.json        （执行脚本产出）
  docs/scratch/legacy20_r6c/removed_registrations.json       （执行脚本产出）
  docs/scratch/legacy20_rev6_landing/batch1|batch2/*/id_mapping.tsv （A 组）
  docs/scratch/legacy20_r6b/{H-WZ-001/H-DYM-001/H-HZX-002}/*        （B 组）
  docs/research/legacy20_rev6_assessment.md                  （口径）
  data/{figure_names,code_maps,scenarios_zh,scenarios_en,modes_data}.json（复核）

输出：
  docs/research/phase21r6C_archive_report.md
  docs/research/phase21r6C_pending_identity.json
  docs/research/phase21r6C_luorq_isolation_note.md
  docs/research/phase21r6C_archive_evidence.json
  data/audit/phase21r6_id_mapping_ledger.tsv  及 .json

用法：python3 build_r6c_products.py [--manifest PATH] [--outdir DIR] [--quiet]
"""
import argparse
import glob
import hashlib
import json
import os
import re

ROOT = "/opt/data/workspace/Protreptic"
SK = "docs/scratch/legacy20_r6c"
DATE = "2026-09-23"
CARD = "t_4a9cf2cb"

CODES = ["H-AN-001", "H-LC-001", "H-YE-001", "H-ZOU-001", "H-HAN-001", "H-MODERN-002", "H-LUORQ-001"]
NAME_ZH = {
    "H-AN-001": "安子", "H-LC-001": "陆沉", "H-YE-001": "叶筱", "H-ZOU-001": "邹文献",
    "H-HAN-001": "沈幅", "H-MODERN-002": "大云", "H-LUORQ-001": "罗瑞卿",
}
# 评估口径（docs/research/legacy20_rev6_assessment.md 2026-09-23 版；§4.3 及总表）
ASSESS = {
    "H-AN-001": dict(verdict="不可", disposition="归档；若保留另立研究卡",
                     root="身份未能核实：库内 0 条、git 无合并提交、docs 无独立研究件",
                     renumber="暂不分配；M-AN-（0 碰撞）",
                     basis="载荷 10 条全字段，但出处《辩证论》《历史观》《实践观》均不可落源；定义均 59.9 字，模板化"),
    "H-LC-001": dict(verdict="不可", disposition="归档；若保留另立研究卡",
                     root="疑似旧世代虚构人物：库内、docs、git 均无独立证据；来源《沉潜之道》不可落源",
                     renumber="暂不分配；M-LC-（0 碰撞）",
                     basis="载荷 10 条（定义均 73.6 字）；案例为现代咨询口吻，来源不明"),
    "H-YE-001": dict(verdict="不可", disposition="归档或整卡替换",
                     root="无人名证据：phase46 报告列为 name_mismatch，文件内无人名证据",
                     renumber="暂不分配；M-YE-（0 碰撞）",
                     basis="载荷 10 条（定义均 54 字，引文与案例空）；出处《现代政治理论选集》不可落源"),
    "H-ZOU-001": dict(verdict="不可", disposition="归档；若保留另立研究卡",
                      root="零出处内容不可核：公开检索无独立证据；项目内仅自产文档互引",
                      renumber="暂不分配；M-ZOU-（0 碰撞）",
                      basis="载荷 10 条（定义均 46.8 字，引文、出处、案例全空）；docs/figures/H-ZOU-001.md 为同批自产件"),
    "H-HAN-001": dict(verdict="不可", disposition="归档；若保留另立研究卡",
                      root="身份与生卒不符：生卒记录 -100 至 180 与人物不符（phase46 已记疑似沈复）；公开检索无此人此作",
                      renumber="暂不分配；M-HAN-（0 碰撞）",
                      basis="载荷 8 条不足 10（引文与案例空，出处《捕鱼记》）；定义均 41.5 字"),
    "H-MODERN-002": dict(verdict="不可", disposition="归档或立项",
                         root="元数据虚标 10 条：项目内大云仅指《大云经》，无此人证据",
                         renumber="暂不分配；若立项 M-DAYUN-（0 碰撞）",
                         basis="三个文件均 0 条载荷（仅元数据，thinking_mode_count 却写 10）；无内容可查"),
    "H-LUORQ-001": dict(verdict="不可", disposition="载荷隔离归档，另立项重做研究",
                        root="串档：载荷内容实为陆有（诗词政治文学主题），与罗瑞卿完全不符",
                        renumber="H-LUORQ-001 + M-LUORQ-（0 碰撞，载荷须全新）",
                        basis="罗瑞卿真实（1906-1978，docs 页自述一致）；载荷归属他人，不可用；图档自述 M351-M360 与载荷 M311-M320 不符"),
}
# 归档目标文件名（执行脚本 FILES 的 target 列；用于从 manifest 反查 target）
EXTERNAL = {
    "data/figures": "figures", "data/individuals": "individuals", "docs/figures": "archive_page",
}


def sha256b(b):
    return hashlib.sha256(b).hexdigest()


def read_bytes(rel):
    return open(os.path.join(ROOT, rel), "rb").read()


def load_json(rel):
    return json.loads(read_bytes(rel).decode("utf-8"))


def ids_of(rel):
    """从归档（或任意）JSON 文本提取 M 编号集合（有序）。"""
    text = read_bytes(rel).decode("utf-8", "replace")
    out = []
    for m in re.finditer(r"M\d{2,4}", text):
        if m.group(0) not in out:
            out.append(m.group(0))
    return out


def pad_range(prefix, lo, hi):
    return ["%s%03d" % (prefix, i) for i in range(lo, hi + 1)]


class Builder(object):
    def __init__(self, manifest_path, outdir, removed_path=None):
        self.manifest = json.load(open(manifest_path, encoding="utf-8"))
        self.removed = load_json(removed_path or os.path.join(SK, "removed_registrations.json"))
        self.outdir = outdir
        self.auditdir = outdir or ""
        self.products = []
        self.warnings = []

    # ---------- 输出 ----------
    def emit(self, rel, text):
        path = os.path.join(self.outdir, rel) if self.outdir else os.path.join(ROOT, rel)
        d = os.path.dirname(path)
        if d and not os.path.isdir(d):
            os.makedirs(d)
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
        self.products.append({"path": rel, "bytes": len(text.encode("utf-8")),
                              "sha256": sha256b(text.encode("utf-8"))})

    # ---------- A 组：批1/批2 id_mapping ----------
    def rows_A(self):
        rows = []
        dirs = sorted(glob.glob(os.path.join(ROOT, "docs/scratch/legacy20_rev6_landing/batch[12]/*/id_mapping.tsv")))
        batch_of = {1: "t_4481df98", 2: "t_2d5112c6"}
        for path in dirs:
            rel = os.path.relpath(path, ROOT)
            batch = 1 if "/batch1/" in rel else 2
            lines = open(path, encoding="utf-8").read().splitlines()
            header = lines[0].split("\t")
            ncols = len(header)
            assert header[0] == "legacy_id" and header[1] == "v6_id", rel
            for i, ln in enumerate(lines[1:], start=2):
                if not ln.strip():
                    continue
                cells = ln.split("\t")
                legacy, v6 = cells[0], cells[1]
                name_zh = cells[2] if ncols > 2 else ""
                m = re.match(r"M-([A-Z0-9]+)-", v6)
                code = "H-%s-001" % m.group(1) if m else ""
                rows.append(dict(figure_code=code, name_zh=name_zh, legacy_id=legacy, new_id=v6,
                                 disposition="迁入并统一重编（v6 复刻）", group="A",
                                 source_card=batch_of[batch], source_ref="%s L%d" % (rel, i),
                                 status="已落盘（批%d，已提交）" % batch, notes=""))
        return rows

    # ---------- B 组：r6b 交接件 ----------
    def rows_B(self):
        rows = []
        wz = os.path.join(ROOT, "docs/scratch/legacy20_r6b/H-WZ-001/id_mapping.tsv")
        lines = open(wz, encoding="utf-8").read().splitlines()
        for i, ln in enumerate(lines[1:], start=2):
            if not ln.strip():
                continue
            c = ln.split("\t")
            legacy, v6 = c[0], c[1]
            disp = c[6] if len(c) > 6 else ""
            rows.append(dict(figure_code="H-WZ-001", name_zh="王震", legacy_id=legacy, new_id=v6,
                             disposition=disp or "迁入并统一重编", group="B",
                             source_card="t_f3aabe2c", source_ref="docs/scratch/legacy20_r6b/H-WZ-001/id_mapping.tsv L%d" % i,
                             status="B 收口在制（本表按 r6b 交接件登记）", notes=""))
        dyn_ids = pad_range("M", 11, 20)
        for j, lid in enumerate(dyn_ids):
            rows.append(dict(figure_code="H-DYM-001", name_zh="董宇明", legacy_id=lid, new_id="—（归档，无新号）",
                             disposition="归档（R2 归位后状态；由 B 收口执行）", group="B",
                             source_card="t_f3aabe2c",
                             source_ref="docs/scratch/legacy20_r6b/H-DYM-001/archive_manifest.json（M11~M20 区间）",
                             status="B 收口在制（本表按 r6b 交接件登记）", notes="载荷为 AI/科技类；归档不保留新号"))
        hzx_ids = pad_range("M", 301, 310)
        for lid in hzx_ids:
            rows.append(dict(figure_code="H-HZX-002", name_zh="王祥", legacy_id=lid, new_id="—（归档/待重做，B 收口裁定）",
                             disposition="归档或按换码重做（assessment 建议换码 H-WX-001）", group="B",
                             source_card="t_f3aabe2c",
                             source_ref="docs/scratch/legacy20_r6b/H-HZX-002/archive_recommendation.json（M301~M310）",
                             status="B 收口在制（本表按 r6b 交接件登记）", notes="内容重做待船长裁定；重做不以换码为前提"))
        # WZ 两枚特殊旧码（M391 归档 / M392 重编）如不在 tsv 中，单独补登
        have = set(r["legacy_id"] for r in rows if r["figure_code"] == "H-WZ-001")
        for lid, dish, note in [("M391", "归档（王震档 10 条之外，另案）", "见 r6b collision_scan.json（28 文件涉及）"),
                                ("M392", "迁入并统一重编（M-WZ-011）", "见 r6b 交接件")]:
            if lid not in have:
                rows.append(dict(figure_code="H-WZ-001", name_zh="王震", legacy_id=lid,
                                 new_id=("—（归档，无新号）" if lid == "M391" else "M-WZ-011"),
                                 disposition=dish, group="B", source_card="t_f3aabe2c",
                                 source_ref="docs/scratch/legacy20_r6b/（id_mapping/交接件）",
                                 status="B 收口在制（本表按 r6b 交接件登记）", notes=note))
        rows.sort(key=lambda r: (r["figure_code"], r["legacy_id"]))
        return rows

    # ---------- C 组：从归档件提取旧号 ----------
    def read_cached(self, rel_target, rel_source):
        for rel in (rel_target, rel_source):
            p = os.path.join(ROOT, rel)
            if os.path.exists(p):
                return read_bytes(rel).decode("utf-8", "replace")
        return ""

    def rows_C(self):
        tmap = {}
        for ent in self.manifest["files"]:
            m = re.search(r"H-([A-Z0-9]+)-\d{3}", ent["source"])
            if not m or m.group(0) not in CODES:
                continue
            code = m.group(0)
            role = "figures"
            if "/individuals/" in ent["source"]:
                role = "individuals" if "_modes" not in ent["source"] else "individuals_modes"
            elif ent["source"].endswith(".md"):
                role = "archive_page"
            text = self.read_cached(ent["target"], ent["source"])
            ids = []
            for mm in re.finditer(r"M\d{2,4}", text):
                if mm.group(0) not in ids:
                    ids.append(mm.group(0))
            tmap.setdefault(code, []).append(dict(role=role, target=ent["target"], ids=ids))
        rows = []
        self.item_payload = {}
        for code in CODES:
            recs = tmap.get(code, [])
            by_role = {r["role"]: r for r in recs}
            union = []
            for r in recs:
                for i in r["ids"]:
                    if i not in union:
                        union.append(i)
            union.sort()
            payload_ids = by_role.get("individuals_modes", {}).get("ids", [])
            summary = self.summarize(code, by_role, union, payload_ids)
            self.item_payload[code] = summary
            for lid in union:
                roles = sorted(r["role"] for r in recs if lid in r["ids"])
                notes = "档位：" + ",".join(roles)
                if code == "H-LUORQ-001" and lid in payload_ids:
                    notes += "（载荷内容为陆有，隔离归档）"
                if code == "H-MODERN-002":
                    notes += "（仅编号声明，无载荷）"
                rows.append(dict(figure_code=code, name_zh=NAME_ZH[code], legacy_id=lid,
                                 new_id="—（归档；暂不分配）" if code != "H-LUORQ-001" else "—（归档；重做须另立项，载荷全新）",
                                 disposition=ASSESS[code]["disposition"], group="C", source_card=CARD,
                                 source_ref="本卡归档件（%s）" % ",".join(os.path.basename(r["target"]) for r in recs),
                                 status="已归档（本卡）", notes=notes))
        return rows

    def collapse(self, ids):
        nums = []
        for x in ids:
            m = re.match(r"^(M)(\d+)$", x)
            if m:
                nums.append((m.group(1), int(m.group(2))))
        if not nums:
            return ", ".join(ids)
        nums.sort(key=lambda t: t[1])
        out = []
        start = prev = nums[0][1]
        for _, n in nums[1:]:
            if n == prev + 1:
                prev = n
                continue
            out.append("M%03d" % start if start == prev else "M%03d-M%03d" % (start, prev))
            start = prev = n
        out.append("M%03d" % start if start == prev else "M%03d-M%03d" % (start, prev))
        extra = [x for x in ids if not re.match(r"^M\d+$", x)]
        return ", ".join(out + extra)

    def summarize(self, code, by_role, union, payload_ids):
        parts = ["旧号 %s（%d 个）" % (self.collapse(union), len(union))]
        if "individuals_modes" in by_role:
            parts.append("载荷 %d 条" % len(by_role["individuals_modes"]["ids"]))
        else:
            parts.append("无载荷件")
        if code == "H-MODERN-002":
            parts.append("元数据虚标 10（无载荷）")
        if code == "H-LUORQ-001":
            parts.append("载荷内容为陆有（串档，隔离归档）")
        return "；".join(parts)

    # ---------- 复扫 ----------
    SKIP_DIR_PARTS = (".git", "__pycache__", "node_modules", "site_docs", "_duplicates", "backup_", ".venv")
    def scan_residuals(self):
        roots = ["data", "tools", "web/public", "docs"]
        hits = []
        for root in roots:
            for dirpath, dirnames, filenames in os.walk(os.path.join(ROOT, root)):
                if any(p in dirpath for p in self.SKIP_DIR_PARTS):
                    dirnames[:] = []
                    continue
                dirnames[:] = [d for d in dirnames if not any(p in d for p in self.SKIP_DIR_PARTS)]
                for fn in filenames:
                    if fn.endswith((".pyc", ".png", ".jpg", ".svg", ".woff", ".woff2", ".ttf")):
                        continue
                    p = os.path.join(dirpath, fn)
                    rel = os.path.relpath(p, ROOT)
                    try:
                        text = open(p, "rb").read().decode("utf-8", "replace")
                    except Exception:
                        continue
                    found = [c for c in CODES if c in text]
                    if not found:
                        continue
                    sample = ""
                    for ln in text.splitlines():
                        if any(c in ln for c in found):
                            sample = ln.strip()[:160]
                            break
                    hits.append(dict(path=rel, codes=found, layer=self.classify(rel), sample=sample))
        hits.sort(key=lambda h: (h["layer"], h["path"]))
        return hits

    def classify(self, rel):
        if "legacy20_r6c" in rel or "phase21r6C" in rel or "phase21r6_id_mapping_ledger" in rel:
            return "本卡产物"
        if rel.startswith("docs/qa/") or rel.startswith("docs/research/") or rel.startswith("docs/planning/") or rel.startswith("docs/architecture/"):
            return "历史报告层"
        if rel.startswith("docs/scratch/"):
            return "交接/工作层"
        if rel.startswith("docs/"):
            return "文档层"
        return "活跃层"

    # ---------- 全库查重 ----------
    def collect_codeset(self, obj, out, keynames=("mode_code", "mode_ids", "id_list", "ids")):
        if isinstance(obj, dict):
            for k, v in obj.items():
                if k in keynames:
                    if isinstance(v, str):
                        out.add(v)
                    elif isinstance(v, list):
                        for x in v:
                            if isinstance(x, str):
                                out.add(x)
                self.collect_codeset(v, out, keynames)
        elif isinstance(obj, list):
            for x in obj:
                self.collect_codeset(x, out, keynames)
        return out

    def dedupe(self, rows):
        new_ids = [r["new_id"] for r in rows if r["new_id"].startswith("M-")]
        dup = sorted(set(x for x in new_ids if new_ids.count(x) > 1))
        modes = self.collect_codeset(load_json("data/modes_data.json"), set())
        cmap = self.collect_codeset(load_json("data/code_maps.json"), set())
        # code_maps 归属核对：只看 mode_ids 子树；正文/交叉引用提及另计为邻接登记
        collisions = []
        adjacent = []
        cm = load_json("data/code_maps.json")
        figs = cm.get("figures", {})
        nset = set(new_ids)
        for fig_key, sub in figs.items():
            own = sub.get("mode_ids", []) if isinstance(sub, dict) else []
            ownset = set(x for x in own if isinstance(x, str))
            for x in sorted(ownset & nset):
                owner = "H-" + re.match(r"M-([A-Z0-9]+)-", x).group(1) + "-001"
                if owner != fig_key:
                    collisions.append(dict(id=x, found_under=fig_key, expected_owner=owner))
            blob = json.dumps(sub, ensure_ascii=False)
            seen_adj = set()
            for mm in re.finditer(r"M-[A-Z0-9]+-\d{3}", blob):
                x = mm.group(0)
                if x in nset and x not in ownset and x not in seen_adj:
                    seen_adj.add(x)
                    adjacent.append(dict(id=x, mentioned_under=fig_key))
        return dict(new_ids_total=len(new_ids), unique=(len(dup) == 0), duplicates=dup,
                    in_modes_data=sum(1 for x in new_ids if x in modes), in_code_maps=sum(1 for x in new_ids if x in cmap),
                    collisions=collisions, adjacent_count=len(adjacent), adjacent_mentions=adjacent[:80])

    # ---------- 产物：待身份清单 ----------
    def emit_pending(self):
        items = []
        for code in ["H-AN-001", "H-LC-001", "H-YE-001", "H-ZOU-001", "H-HAN-001", "H-MODERN-002"]:
            a = ASSESS[code]
            items.append({
                "code": code,
                "name_card": NAME_ZH[code],
                "name_registered": self.removed["figure_names"].get(code, ""),
                "identity_status": "未能核实",
                "assessment_verdict": a["verdict"],
                "disposition": a["disposition"],
                "evidence_basis": a["root"],
                "payload": self.item_payload.get(code, ""),
                "keep_condition": "若保留须另立研究卡：先给出权威身份与可落源出处，再谈 v6 复刻；归档件不得直接复用",
                "renumber_plan": a["renumber"],
                "notes": a["basis"],
            })
        doc = {"schema": "protreptic.r6c_pending_identity/v1", "card": CARD, "date": DATE,
               "title": "待权威身份清单（C 组 6 件）",
               "criteria": "docs/research/legacy20_rev6_assessment.md §4.3：身份未能核实（库内/git/docs 无独立证据）判归档并单列",
               "items": items}
        self.emit("docs/research/phase21r6C_pending_identity.json", json.dumps(doc, ensure_ascii=False, indent=2) + "\n")

    # ---------- 产物：罗瑞卿隔离说明 ----------
    def emit_isolation(self):
        a = ASSESS["H-LUORQ-001"]
        lines = []
        lines.append("# 罗瑞卿载荷隔离说明（R6C，卡 %s）\n" % CARD)
        lines.append("日期：%s；依据：docs/research/legacy20_rev6_assessment.md §2/§4.3/§7\n" % DATE)
        lines.append("## 事实\n")
        lines.append("- 归档代码：H-LUORQ-001（登记名：罗瑞卿）。罗瑞卿本体真实（1906-1978），且 docs 页自述与史实一致。")
        lines.append("- **名实不符（串档）**：载荷（%s）内容人物为**陆有**、主题为诗词政治文学（assessment 原文），与罗瑞卿完全不符，不可用。" % self.item_payload.get("H-LUORQ-001", ""))
        lines.append("- 编号自相矛盾：图档件自述 M351-M360；载荷件实际为 M311-M320（与安子侧旧号段同形，属旧世代重码面）。")
        lines.append("- 线上痕迹：docs/figures/H-LUORQ-001.md（自产页）随件撤下（见报告线上变化节）。")
        lines.append("\n## 隔离处置（本卡执行）\n")
        lines.append("- 载荷字节件归档入 data/figures/_duplicates/H-LUORQ-001_individuals_modes_ISOLATED_crossfile.json（隔离命名，防被当作罗瑞卿载荷复用）。")
        lines.append("- 全部 4 件（figures/individuals/individuals_modes/docs 页）sha256 登记于 docs/research/phase21r6C_archive_evidence.json。")
        lines.append("\n## 另立项说明（重做研究要点；供船长排卡）\n")
        lines.append("- 建议编号：沿用 H-LUORQ-001 + M-LUORQ-（当前 0 碰撞；载荷须全新，禁止复用隔离件内容）。")
        lines.append("- 前置条件：先做独立文献研究，锁定罗瑞卿的权威生平与可落源材料（文档/文选），再按 R6 复刻口径落 10 条。")
        lines.append("- 禁止事项：不得以隔离件（陆有内容）改名充数；不得仅改人物名而保留原载荷。")
        lines.append("- 参考先例：本件与整卡替换类（YE）不同，罗瑞卿身份真实，问题在载荷归属，故走研究重做而非另一人改名。")
        lines.append("")
        self.emit("docs/research/phase21r6C_luorq_isolation_note.md", "\n".join(lines))

    # ---------- 产物：映射账本 ----------
    def ledger_sources(self):
        srcs = [os.path.join(SK, "r6c_archive_manifest.json"), os.path.join(SK, "removed_registrations.json"),
                "docs/research/legacy20_rev6_assessment.md"]
        srcs += sorted(glob.glob(os.path.join(ROOT, "docs/scratch/legacy20_rev6_landing/batch[12]/*/id_mapping.tsv")))
        srcs += ["docs/scratch/legacy20_r6b/H-WZ-001/id_mapping.tsv",
                 "docs/scratch/legacy20_r6b/H-DYM-001/archive_manifest.json",
                 "docs/scratch/legacy20_r6b/H-HZX-002/archive_recommendation.json",
                 "docs/scratch/legacy20_r6b/collision_scan.json"]
        out = []
        for s in srcs:
            rel = os.path.relpath(s, ROOT) if os.path.isabs(s) else s
            p = os.path.join(ROOT, rel)
            out.append({"path": rel, "sha256": sha256b(open(p, "rb").read()) if os.path.exists(p) else "MISSING"})
        return out

    def emit_ledger(self, rows, dedupe):
        cols = ["figure_code", "name_zh", "legacy_id", "new_id", "disposition", "group",
                "source_card", "source_ref", "status", "notes"]
        def clean(x):
            return str(x).replace("\t", " ").replace("\n", " ")
        lines = ["\t".join(cols)]
        for r in rows:
            lines.append("\t".join(clean(r[c]) for c in cols))
        tsv = "\n".join(lines) + "\n"
        self.emit("data/audit/phase21r6_id_mapping_ledger.tsv", tsv)
        counts = {}
        for r in rows:
            counts[r["group"]] = counts.get(r["group"], 0) + 1
        doc = {"schema": "protreptic.r6_id_mapping_ledger/v1", "card": CARD, "date": DATE,
               "position_rationale": "先例检查：仓内无既有总账本；审计清单惯例位为 data/audit/（已有 phase21r6_batch1_landing_manifest.json、phase21r6_batch2_backup_manifest.json、phase20R_* 系列）；故账本取 data/audit/phase21r6_id_mapping_ledger.tsv（同名 .json 为伴随件）。",
               "columns": cols, "counts": dict(sorted(counts.items())), "total": len(rows),
               "columns_note": "name_zh：A 组与 H-WZ-001 行为模式名（tsv 原样）；其余行为件名（人物/件）",
               "dedupe": dedupe,
               "recompute_recipe": [
                   "A 组：逐件读 docs/scratch/legacy20_rev6_landing/batch1|batch2/<code>/id_mapping.tsv（第 2 列 v6_id 直取）",
                   "B 组：H-WZ-001/id_mapping.tsv 直取；H-DYM-001 与 H-HZX-002 为区间登记（M11~M20 / M301~M310，见 r6b 交接件）",
                   "C 组：从本卡 manifest 所列归档件文本提取 M 编号并集（figures/individuals/individuals_modes 三档位）",
                   "全库查重：新号唯一性 + 与 modes_data（mode_code）及 code_maps（mode_ids）占用计数 + code_maps 归属核对（collision 必空）",
               ],
               "sources": self.ledger_sources(), "rows": rows}
        self.emit("data/audit/phase21r6_id_mapping_ledger.json", json.dumps(doc, ensure_ascii=False, indent=2) + "\n")

    # ---------- 产物：证据 ----------
    def emit_evidence(self, dedupe, residual):
        m = self.manifest
        ev = {"schema": "protreptic.r6c_archive_evidence/v1", "card": CARD, "date": DATE,
              "inputs": self.ledger_sources(),
              "archive_manifest_ref": os.path.join(SK, "r6c_archive_manifest.json"),
              "removed_registrations_ref": os.path.join(SK, "removed_registrations.json"),
              "archives": m["files"], "shared_file_sha": m["shared"],
              "modes_data_freeze": m["modes_data_freeze"],
              "removed_counts": {"figure_names": len(self.removed["figure_names"]),
                                 "code_maps": len(self.removed["code_maps"]),
                                 "scenarios": dict((k, len(v)) for k, v in self.removed["scenarios"].items())},
              "removed_figure_names_verbatim": self.removed["figure_names"],
              "online_visibility_changes": self.online_changes(),
              "item_payload": self.item_payload, "dedupe": dedupe, "residual_scan": residual,
              "products": list(self.products), "notes": [
                  "撤下登记项逐字原文（figure_names/code_maps/scenarios 条目）见 docs/scratch/legacy20_r6c/removed_registrations.json（sha256 于本文件 inputs 列表）",
                  "归档位：data/figures/_duplicates/（R2 先例命名）",
                  "复扫域：data/、tools/、web/public/、docs/（排除 .git/__pycache__/site_docs/_duplicates/backup_*）；扫描时点=产物写入后、提交前；evidence 自身为登记载体不列自身",
              ]}
        self.emit("docs/research/phase21r6C_archive_evidence.json", json.dumps(ev, ensure_ascii=False, indent=1) + "\n")

    def online_changes(self):
        out = []
        for ent in self.manifest["files"]:
            if ent["source"].startswith("docs/figures/"):
                code = os.path.basename(ent["source"]).replace(".md", "")
                title = ""
                for ln in self.read_cached(ent["target"], ent["source"]).splitlines():
                    if ln.startswith("# "):
                        title = ln[2:].strip()
                        break
                out.append({"page": ent["source"], "archived_to": ent["target"], "title": title,
                            "site_url_effect": "文档站 /figures/%s/ 页随重建消失（mkdocs 源为该文件）" % code})
        return out

    # ---------- 判定口径 ----------
    def verdict_of(self, rel):
        if rel == "data/modes_data.json":
            return "合并卡负责面（冻结值登记；顶层 H-LUORQ-001 块待裁定）"
        if rel.startswith("data/audit/"):
            if "phase21r6_id_mapping_ledger" in rel:
                return "本卡证据（映射账本）"
            return "审计历史件（既有清单，留痕）"
        if ".bak" in rel:
            return "备份件（历史留痕）"
        if "H-MODERN-003" in rel:
            return "他件引用（H-MODERN-003 与 MODERN-002 相关）→ 待其收口处置"
        if rel.startswith("tools/"):
            return "工具内嵌历史名单/注释（留痕，不动）"
        if rel.startswith("docs/figures/"):
            return "文档层互引（随重建以现盘为准；如需重指另卡）"
        if rel.startswith("docs/"):
            if "legacy20_r6c" in rel or "phase21r6C" in rel:
                return "本卡产物（证据/报告）"
            if rel.startswith("docs/scratch/"):
                return "交接/工作层（生成件，留痕）"
            return "历史报告层（留痕，不动作）"
        if rel.startswith("data/figures/H-CY-001") or rel.startswith("data/individuals/H-CY-001"):
            return "他件引用（H-CY-001 cross_references）→ 待其收口重指"
        if "H-BG-001" in rel:
            return "他件引用（H-BG-001）→ 待其收口重指"
        if rel.startswith("data/asia/"):
            return "asia 旧命名空间（历史，留痕）"
        if rel.startswith("web/public/"):
            return "生成镜像（随重建消除；当前构建未见）"
        return "登记在案（未归类，待裁定）"

    def role_sha_line(self, code):
        parts = []
        for ent in self.manifest["files"]:
            if code not in ent["source"]:
                continue
            role = "figures"
            if "/individuals/" in ent["source"]:
                role = "modes" if "_modes" in ent["source"] else "individuals"
            elif ent["source"].endswith(".md"):
                role = "docs 页"
            parts.append("%s %s" % (role, ent["sha256"][:8]))
        return "；".join(parts)

    # ---------- 产物：报告 ----------
    def emit_report(self, rows, dedupe, residual):
        L = []
        A = L.append
        counts = {}
        for r in rows:
            counts[r["group"]] = counts.get(r["group"], 0) + 1
        A("# Phase21-R6C 归档报告：C 组 7 件（卡 %s）" % CARD)
        A("")
        A("- 日期：%s" % DATE)
        A("- 依据：docs/research/legacy20_rev6_assessment.md（§4.3 C 组裁决、§2 子串修正、§7 编号预案）；先例：docs/qa/phase21r2_cleanup_report.md（R2 清档）")
        A("- 边界：主库 modes_data.json 零写入（合并卡负责）；发布仓镜像由合并卡统一收敛；本卡提交仅本卡路径。")
        A("")
        A("## 一、结论摘要")
        A("")
        A("- 7 件全部清档：22 个字节件（data 19 件 + docs 3 页）移入 data/figures/_duplicates/（R2 先例命名），逐件 sha256 登记，未删字节。")
        A("- 自件登记撤下：figure_names 9 键、code_maps 3 条目、scenarios_zh+en 各 30 条（逐字留档，见证据文件与 removed_registrations.json）。")
        A("- 罗瑞卿载荷隔离归档（串档防复用）+ 另立项说明（docs/research/phase21r6C_luorq_isolation_note.md）。")
        A("- 待权威身份清单 6 件：本报告第五节 + docs/research/phase21r6C_pending_identity.json。")
        A("- 映射账本：data/audit/phase21r6_id_mapping_ledger.tsv/.json（A %d + B %d + C %d = %d 行）；全库查重复核见第六节。" % (counts.get("A", 0), counts.get("B", 0), counts.get("C", 0), len(rows)))
        A("- 线上可见变化：3 个 docs 页撤下（第四节）；站点计数链不受影响（C 组不在 figures 计数链内）。")
        A("- 核验：verify_phase21r6C_archive.py；活跃层复扫逐条登记（第八节），核验断言零未登记残留。")
        A("")
        A("## 二、归档明细（7 件 × 22 字节件）")
        A("")
        for code in CODES:
            a = ASSESS[code]
            A("### %s（%s）" % (code, NAME_ZH[code]))
            A("")
            A("- 载荷摘要：%s" % self.item_payload.get(code, ""))
            A("- 裁决/处置：%s（assessment）" % a["disposition"])
            A("- 归档件 sha256（前 8 位）：%s" % self.role_sha_line(code))
            A("")
        A("完整 sha256、字节数与逐件源/目标路径见 docs/research/phase21r6C_archive_evidence.json（archives 段）。")
        A("")
        A("## 三、登记层撤下（自件；逐字留档）")
        A("")
        A("### figure_names.json（9 键）")
        A("")
        A("| 键 | 值 |")
        A("|---|---|")
        for k, v in sorted(self.removed["figure_names"].items()):
            A("| %s | %s |" % (k, v))
        A("")
        A("### code_maps.json（3 条目）")
        A("")
        for k, v in sorted(self.removed["code_maps"].items()):
            mids = v.get("mode_ids", [])
            xr = v.get("cross_references", [])
            A("- %s：mode_ids %d 个（%s）；cross_references %s" % (k, len(mids), ("%s 至 %s" % (mids[0], mids[-1])) if mids else "无", ("有（随条目撤下）" if xr else "无")))
        A("")
        A("### scenarios_zh.json / scenarios_en.json（各 30 条，按 figure_id 扫描撤下）")
        A("")
        for f, d in sorted(self.removed["scenarios"].items()):
            byfig = {}
            for k, v in d.items():
                byfig.setdefault(v.get("figure_id", "?"), []).append(k)
            for fig, keys in sorted(byfig.items()):
                A("- %s：%s 共 %d 条（键名 %s 至 %s）" % (f, fig, len(keys), sorted(keys)[0], sorted(keys)[-1]))
        A("")
        A("撤下原文逐字（含 title/description 等全字段）见 docs/scratch/legacy20_r6c/removed_registrations.json；如需回填，按该文件原样恢复（键级操作、可精确重放）。")
        A("")
        A("## 四、线上可见变化清单")
        A("")
        A("| docs 页（撤下） | 页题 | 站点影响 |")
        A("|---|---|---|")
        for oc in self.online_changes():
            A("| %s | %s | %s |" % (oc["page"], oc["title"], oc["site_url_effect"]))
        A("")
        A("- 站点计数链不受影响：figures/场景计数源自 api/protreptic.db（tools/json 输入），C 组 7 件均不在其中（按码查 DB 为空集）；本卡未触碰计数链。")
        A("- site_docs/ 为本地生成镜像（未跟踪）：撤下的 3 页与搜索索引残留随下一次重建自然消失。")
        A("- 发布仓镜像（publish）由合并卡统一收敛；本卡改动清单见证据文件，供收敛核对。")
        A("")
        A("## 五、待权威身份清单（6 件）")
        A("")
        A("单列标准（assessment §4.3）：身份未能核实（库内/git/docs 无独立证据）。")
        A("")
        A("| 代码 | 卡面名 | 登记名（撤下前） | 裁决 | 未能核实依据 | 载荷摘要 |")
        A("|---|---|---|---|---|---|")
        for code in ["H-AN-001", "H-LC-001", "H-YE-001", "H-ZOU-001", "H-HAN-001", "H-MODERN-002"]:
            a = ASSESS[code]
            A("| %s | %s | %s | %s | %s | %s |" % (code, NAME_ZH[code], self.removed["figure_names"].get(code, ""), a["verdict"], a["root"], self.item_payload.get(code, "")))
        A("")
        A("- 机读版：docs/research/phase21r6C_pending_identity.json（含 keep_condition 与 renumber_plan；M-AN-/M-LC-/M-YE-/M-ZOU-/M-HAN-/M-DAYUN- 区间当前 0 碰撞，保留须先立研究卡）。")
        A("")
        A("## 六、映射账本与全库查重复核")
        A("")
        A("- 位置先例检查：仓内无既有总账本；审计清单惯例位为 data/audit/（已有 phase21r6_batch1_landing_manifest.json、phase21r6_batch2_backup_manifest.json、phase20R_* 系列）。")
        A("- 账本：data/audit/phase21r6_id_mapping_ledger.tsv（同名 .json 含 sources sha256 与复算方法）。")
        A("- 行数：A 组 %d（批1/批2 id_mapping 汇总）；B 组 %d（r6b 交接件登记，B 收口在制）；C 组 %d（本卡归档段）。" % (counts.get("A", 0), counts.get("B", 0), counts.get("C", 0)))
        A("- 全库查重：新号 %d 个，唯一性 %s；modes_data 占用 %d、code_maps 占用 %d；归属碰撞 %d（须为 0）。" % (dedupe["new_ids_total"], "通过" if dedupe["unique"] else "失败", dedupe["in_modes_data"], dedupe["in_code_maps"], len(dedupe["collisions"])))
        A("- 交叉引用邻接：新号被他件正文提及 %d 处（批1 登记的 cross_references 邻接口径；邻接非占用，明细见账本 .json 的 adjacent_mentions）。" % dedupe.get("adjacent_count", 0))
        A("- 旧世代重码说明（归档不换号之由）：C 组旧号段相互重码（LC/YE/ZOU 同处 M401-M410 面；AN/MODERN-002 与既有 M001-M010 面同形；LUORQ 载荷 M311-M320 与图档自述 M351-M360 不符）；assessment 处置为「暂不分配」，账本 new_id 记归档标记。")
        A("- 复算方法：见账本 .json 的 recompute_recipe；逐行 source_ref 可回溯到批1/批2 tsv 行号。")
        A("")
        A("## 七、罗瑞卿载荷隔离")
        A("")
        A("- 载荷（M311-M320）内容实为陆有（诗词政治文学），与罗瑞卿名实不符；按 assessment 做隔离归档（归档件名含 ISOLATED 标记）+ 另立项说明。")
        A("- 详见：docs/research/phase21r6C_luorq_isolation_note.md（含重做前置条件与禁止事项）。")
        A("")
        A("## 八、活跃层复扫报告（残留逐条登记）")
        A("")
        A("- 复扫域：data/、tools/、web/public/、docs/（排除 .git、__pycache__、site_docs、_duplicates、backup_*）；扫描时点=本卡产物写入后、提交前（登记含本卡产物层；evidence 自身为登记载体，不列自身）。")
        A("- 分层：活跃层（data 常规、tools、web/public）/ 历史报告层 / 交接层（docs/scratch）/ 文档层；本卡产物层单列。")
        A("")
        A("| 层 | 文件 | 含码 | 首行样本（截断） | 判定 |")
        A("|---|---|---|---|---|")
        for h in residual:
            A("| %s | %s | %s | %s | %s |" % (h["layer"], h["path"], ",".join(h["codes"]), h["sample"][:80].replace("|", "\\|"), self.verdict_of(h["path"])))
        A("")
        A("- 判定口径：他件引用=留待该件收口重指；历史/交接层=留痕不动作；本卡产物=本卡证据；工具内嵌名单=历史注释（改动超本卡范围）；modes_data 顶层块=合并卡负责面（本卡零写入）。")
        A("- 「活跃层零悬空」验收口径 = 自件登记项与档案件零残留 + 上表逐条登记，核验脚本断言「实际残留 == 登记集合」（零未登记残留）。")
        A("")
        A("## 九、核验与证据")
        A("")
        A("- 核验脚本：verify_phase21r6C_archive.py（A 归档登记 / B 活跃层零悬空 / C 账本可复算 / D 清单与证据完整性）。")
        A("- 运行输出：docs/scratch/legacy20_r6c/verify_output.txt（提交后重跑留证）。")
        A("- 证据文件：docs/research/phase21r6C_archive_evidence.json（archives / removed / online / dedupe / residual / products）。")
        A("- 执行脚本与原始记录：docs/scratch/legacy20_r6c/ 下 {apply_r6c_archive.py, build_r6c_products.py, r6c_archive_manifest.json, removed_registrations.json}。")
        A("")
        A("## 十、遗留与待裁定")
        A("")
        A("- 发布仓镜像收敛：由合并卡统一执行（本卡改动记录于证据文件，供对齐）。")
        A("- B 收口口径通报：归档件 figure_names 机制键按 R2 先例清档（本卡已对 C 组执行）；H-DYM-001/H-HZX-002 同类键建议同口径，由其收口卡执行。")
        A("- 他件引用（如 H-CY-001 → H-LC-001 的 cross_references）留待该件收口时重指；本卡不改他件。")
        A("- modes_data.json 顶层 H-LUORQ-001 块：合并卡负责面，本卡零写入；随后续卡裁定。")
        A("- site_docs 本地镜像残留：重建后消失（未跟踪，不入提交）。")
        A("- LUORQ 重做另立项（建议单开研究卡；前置条件见隔离说明）。")
        A("")
        self.emit("docs/research/phase21r6C_archive_report.md", "\n".join(L) + "\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", default=os.path.join(SK, "r6c_archive_manifest.json"))
    ap.add_argument("--outdir", default=None)
    ap.add_argument("--removed", default=None)
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()
    b = Builder(args.manifest, args.outdir or "", args.removed)
    rows = b.rows_A() + b.rows_B() + b.rows_C()
    dedupe = b.dedupe(rows)
    b.emit_pending()
    b.emit_isolation()
    b.emit_ledger(rows, dedupe)
    # 复扫在产物写入后进行：登记含本卡产物层（evidence 自身为登记载体，不列入自身）
    residual = b.scan_residuals()
    b.emit_report(rows, dedupe, residual)
    b.emit_evidence(dedupe, residual)
    if not args.quiet:
        print("=== R6C 产物构建完成 ===")
        for k in ("A", "B", "C"):
            print("rows[%s] = %d" % (k, sum(1 for r in rows if r["group"] == k)))
        print("total = %d; unique=%s collisions=%d; residual files=%d" % (len(rows), dedupe["unique"], len(dedupe["collisions"]), len(residual)))
        for p in b.products:
            print("  %-70s %8d B  %s" % (p["path"], p["bytes"], p["sha256"][:10]))


if __name__ == "__main__":
    main()
