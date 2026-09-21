#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_figure_key_loss.py - 改 figure 文件前后, 取值键面与模式侧覆盖的对照自检 (Phase46-R)

用法:
    python3 tools/check_figure_key_loss.py --before-dir <改动前的 figures 目录副本>

口径完全照 tools/credibility_gate.py 的 figure_key_candidates(): code / id / figure_code / 文件名主干
四个位置登记的取值键。判定标准: 改动后 (1) 没有任何被模式引用的取值键丢失; (2) 模式侧无法定位的
figure_code 不增加。任何一条不满足即 exit 1。
"""
import argparse
import collections
import importlib.util
import json
import os
import pathlib
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_AFTER = os.path.join(REPO, "data", "figures")
MODES = os.path.join(REPO, "data", "modes_data.json")


def _load_gate():
    spec = importlib.util.spec_from_file_location("cg", os.path.join(REPO, "tools", "credibility_gate.py"))
    cg = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cg)
    return cg


def collect(cg, fig_dir):
    keys = collections.defaultdict(list)
    for fn in sorted(os.listdir(fig_dir)):
        if not fn.endswith(".json"):
            continue
        p = pathlib.Path(os.path.join(fig_dir, fn))
        try:
            doc = json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            continue
        for k in cg.figure_key_candidates(p, doc):
            keys[k].append(fn)
    return keys


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--before-dir", required=True, help="改动前的 figures 目录副本")
    ap.add_argument("--after-dir", default=DEFAULT_AFTER, help="改动后的 figures 目录(默认 data/figures)")
    args = ap.parse_args()

    cg = _load_gate()
    modes = json.load(open(MODES, encoding="utf-8"))["modes"]
    mode_fc = collections.Counter(str(m.get("figure_code") or "") for m in modes)

    k0 = collect(cg, args.before_dir)
    k1 = collect(cg, args.after_dir)
    print("gate 口径取值键: before %d -> after %d" % (len(k0), len(k1)))

    lost = sorted(k for k in k0 if k not in k1)
    live = [(k, mode_fc.get(k, 0)) for k in lost if mode_fc.get(k, 0) > 0]
    print("丢失键 %d; 其中被模式引用 %d 个 / %d 条模式" % (len(lost), len(live), sum(n for _, n in live)))
    for k, n in sorted(live, key=lambda x: -x[1]):
        print("   [LIVE-LOST] %-20s modes=%d  was in %s" % (k, n, k0[k][:2]))

    def missing(keys):
        return [(c, n) for c, n in mode_fc.items() if c and c not in keys and c.upper() not in keys]

    m0, m1 = missing(k0), missing(k1)
    print("模式侧无法定位: before %d 个 code / %d 条模式 -> after %d 个 / %d 条" % (
        len(m0), sum(n for _, n in m0), len(m1), sum(n for _, n in m1)))
    newly = [x for x in m1 if x not in m0]
    print("新增无法定位:", newly)

    bad = bool(live) or bool(newly)
    print("结果:", "FAIL(有引用丢失)" if bad else "PASS(引用零丢失)")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
