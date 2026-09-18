#!/usr/bin/env python3
'''build_daily_index.py -- Phase30-B4: 「每日一模式」的确定性索引.

产物 (两份, 同一次运行产出, 下标严格对齐):
    web/public/data/daily/index.json   74 KB raw / 12 KB gzip —— {figures, entries:[[mode_code, figure_code]]}
                                       首页「今日一模式」与 /daily 都只靠它定位「今天是哪一条」.
    web/public/data/daily/names.json   439 KB raw / 174 KB gzip —— {names:[[name_zh, name_en, category]]}
                                       names[i] 就是 entries[i] 的名称与分类; 只有 /daily 归档页会拉
                                       (首页不拉, 名称与详情走 modes/by-figure/{code}.json 那一份).

为什么拆两份
    首页为一个模块拉全量名称不值得 (174 KB gzip); 而 /daily 要回看任意历史日期, 又必须能对「总数」
    取模, 因此定位用的 entries 必须全量且便宜 —— 只存 (模式编号, 人物编号) 正好 12 KB.
    两份文件的下标由同一次运行写出, 顺序天然一致 (names[i] 属于 entries[i]).

确定性契约 (前端 web/src/api/dailyMode.ts 是同一算法的镜像, 两边必须同时改)
    index = floor((utc_millis + TZ_OFFSET_MINUTES * 60000) / 86400000) % total
    先按 Asia/Shanghai (UTC+8) 定出「第几天」, 再对模式总数取模.
    同一天内任何时刻 / 任何设备 / 任何时区打开结果一致, 跨天才变.

entries 的顺序就是选取顺序
    order = modes/by-figure/*.json 按文件名 (figure_code) 升序, 片内按 modes 数组原序.
    因此本脚本必须在 export_static_site.py 之后运行 (分片由它产出; export 会清空 web/public/data).
    顺序一旦变动 (新增人物/模式), 历史每天的选取结果都会重排 —— 这是「按日期取模」的固有性质,
    不是 bug; 产物里带 total 与 generated_at, 用于核对当时的口径.

隔离名单
    已确证虚构的人物 (tools/build_unified_index.py 的 QUARANTINE, 现为 H-SX-001) 不进本索引:
    公开名录已经把它排除, 首页/归档页更不该把它当作「今日一模式」推出来.
    名单从 build_unified_index 导入 (单一事实来源), 导入失败即报错退出, 不做本地副本.

用法
    python3 tools/build_daily_index.py
    python3 tools/build_daily_index.py --check     # 只校验数据源, 不写盘
退出码: 0 成功; 1 数据缺失 / 结构异常 / 对齐自检不过 (宁可失败, 也不产出半份索引).
'''

from __future__ import annotations

import argparse
import gzip
import json
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SCHEMA = "protreptic.daily_index/v1"
NAMES_SCHEMA = "protreptic.daily_names/v1"
TZ_LABEL = "Asia/Shanghai"
TZ_OFFSET_MINUTES = 480
MS_PER_DAY = 86400000
ALGORITHM = "index = floor((utc_millis + %d * 60000) / %d) %% total" % (TZ_OFFSET_MINUTES, MS_PER_DAY)
ORDER = "modes/by-figure/*.json 按文件名 (figure_code) 升序, 片内按 modes 原序"


def fail(msg: str) -> None:
    sys.exit("[daily] %s" % msg)


def now_iso() -> str:
    return datetime.now(timezone(timedelta(minutes=TZ_OFFSET_MINUTES))).isoformat(timespec="seconds")


def day_number(key: str) -> int:
    '''日期 -> 「第几天」. 与前端 dailyMode.ts 的 dayNumber() 同构:
    UTC 零点加 +8h 仍落在同一 UTC 日, 所以 floor(utc_midnight / 86400000) 就是该日期的天序号.'''
    try:
        d = date.fromisoformat(key)
    except ValueError:
        fail("日期格式应为 YYYY-MM-DD: %r" % key)
    return int(datetime(d.year, d.month, d.day, tzinfo=timezone.utc).timestamp() * 1000) // MS_PER_DAY


def pick_index(key: str, total: int) -> int:
    return day_number(key) % total


def dump(obj) -> str:
    return json.dumps(obj, ensure_ascii=False, separators=(",", ":"))


def write_json(path: Path, payload) -> None:
    text = dump(payload)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    print("[daily] 写出 %s  raw %.1f KB / gzip %.1f KB"
          % (path, len(text.encode("utf-8")) / 1024.0, len(gzip.compress(text.encode("utf-8"), 9)) / 1024.0))


def expected_total(data_dir: Path):
    '''meta.json (export 的产物) 里的 mode_summaries 是同一批模式 —— 对不上说明构建顺序错了.'''
    meta_path = data_dir / "meta.json"
    if not meta_path.exists():
        return None
    try:
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None
    counts = meta.get("counts") or {}
    for key in ("mode_summaries", "modes_deduped"):
        if counts.get(key):
            return int(counts[key])
    return None


def load_quarantine() -> dict:
    '''隔离名单只在 build_unified_index.py 里定义一处, 这里导入它, 不复制副本.'''
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    try:
        import build_unified_index  # noqa: E402
    except Exception as exc:  # pragma: no cover - 只有在工具链被改名/破坏时才会走到
        fail("无法导入 tools/build_unified_index.py 读取隔离名单 (%s): 拒绝在不知道隔离名单的情况下产出索引" % exc)
    return dict(getattr(build_unified_index, "QUARANTINE", {}) or {})


def load_entries(data_dir: Path):
    shard_dir = data_dir / "modes" / "by-figure"
    if not shard_dir.is_dir():
        fail("缺少 %s —— 先跑 python3 tools/export_static_site.py" % shard_dir)
    shards = sorted(p for p in shard_dir.glob("*.json"))
    if not shards:
        fail("%s 下没有分片" % shard_dir)

    quarantine = load_quarantine()
    entries, names, figures, seen = [], [], {}, {}
    excluded = []
    for shard in shards:
        try:
            payload = json.loads(shard.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            fail("%s 不是合法 JSON: %s" % (shard.name, exc))
        code = str(payload.get("figure_code") or shard.stem)
        if code in quarantine:
            excluded.append((code, len(payload.get("modes") or []), quarantine[code]))
            continue
        figures[code] = str(payload.get("figure_name") or "")
        modes = payload.get("modes") or []
        if not modes:
            fail("%s 没有 modes" % shard.name)
        for mode in modes:
            mode_code = str(mode.get("mode_code") or mode.get("id") or "")
            if not mode_code:
                fail("%s 有模式缺 mode_code" % shard.name)
            if mode_code in seen:
                fail("mode_code 重复: %s (%s / %s)" % (mode_code, seen[mode_code], shard.name))
            seen[mode_code] = shard.name
            entries.append([mode_code, code])
            names.append([str(mode.get("name_zh") or ""),
                          str(mode.get("name_en") or ""),
                          str(mode.get("category") or "")])
    if len(entries) != len(names):
        fail("entries/names 长度不一致")
    return entries, names, figures, shards, excluded


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="构建每日一模式索引 (定位索引 + 名称表)")
    parser.add_argument("--data-dir", default=str(REPO / "web" / "public" / "data"),
                        help="静态数据根目录 (默认 web/public/data)")
    parser.add_argument("--index-out", default="", help="定位索引输出 (默认 <data-dir>/daily/index.json)")
    parser.add_argument("--names-out", default="", help="名称表输出 (默认 <data-dir>/daily/names.json)")
    parser.add_argument("--check", action="store_true", help="只校验数据源与对齐, 不写盘")
    parser.add_argument("--spot", default="", help="打印某个日期 (YYYY-MM-DD) 的选取结果, 便于人工核对")
    args = parser.parse_args(argv)

    data_dir = Path(args.data_dir)
    entries, names, figures, shards, excluded = load_entries(data_dir)
    want = expected_total(data_dir)
    if want is not None and want - sum(n for _, n, _ in excluded) != len(entries):
        fail("模式条数 %d 与 meta.json 的 mode_summaries=%d 减去隔离名单 %d 条不一致: 先重跑 export_static_site.py"
             % (len(entries), want, sum(n for _, n, _ in excluded)))
    if not entries:
        fail("索引为空")

    print("[daily] 模式 %d 条 / 人物 %d 位 / 分片 %d 个" % (len(entries), len(figures), len(shards)))
    for code, n_modes, why in excluded:
        print("[daily] 隔离 %s (%d 条模式, 不进公开索引): %s" % (code, n_modes, why))
    if args.spot:
        key = args.spot
        i = pick_index(key, len(entries))
        print("[daily] %s -> index %d/%d -> %s %s (%s)"
              % (key, i, len(entries), entries[i][0], names[i][0], figures.get(entries[i][1], "")))

    if args.check:
        print("[daily] check OK (未写盘)")
        return 0

    index_path = Path(args.index_out) if args.index_out else data_dir / "daily" / "index.json"
    names_path = Path(args.names_out) if args.names_out else data_dir / "daily" / "names.json"

    write_json(index_path, {
        "schema": SCHEMA,
        "generated_by": "tools/build_daily_index.py",
        "generated_at": now_iso(),
        "tz": TZ_LABEL,
        "tz_offset_minutes": TZ_OFFSET_MINUTES,
        "ms_per_day": MS_PER_DAY,
        "algorithm": ALGORITHM,
        "order": ORDER,
        "fields": ["mode_code", "figure_code"],
        "total": len(entries),
        "figure_count": len(figures),
        "shard_count": len(shards),
        "excluded_figures": [{"code": c, "n_modes": n, "reason": w} for c, n, w in excluded],
        "names_file": "names.json",
        "figures": figures,
        "entries": entries,
    })
    write_json(names_path, {
        "schema": NAMES_SCHEMA,
        "generated_by": "tools/build_daily_index.py",
        "generated_at": now_iso(),
        "fields": ["name_zh", "name_en", "category"],
        "aligned_with": "index.json entries (同一次运行写出, names[i] 属于 entries[i])",
        "count": len(names),
        "names": names,
    })
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
