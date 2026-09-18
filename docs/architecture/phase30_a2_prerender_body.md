# Phase30-A2 关键路由静态正文快照 (深链 200 且正文非空)

> 卡片 `t_adfda959` / 负责人: elcano / 日期: 2026-09-18
> 仓库: `/opt/data/workspace/Protreptic` (前端 `web/`) ; 发布仓 `/opt/data/release/Protreptic-publish`
> 线上: https://ovmobilegroup.github.io/protreptic
>
> **基线说明**: 工作区与发布仓的数据基线不一致 (见 `web_p0_architecture.md` 1.1)。
> 本文每个数字都标注它来自哪个基线, 不做跨基线的混用。

## 0. 结论

| `tools/prerender_routes.py` | 改 | 新增 `--body-persons` (默认 40) / `--body-max-modes` (默认 12) / `--no-body`; 写盘自检加"快照标记 + 纯文本至少 200 字"; 路由清单加 `body_count` / `body_total_bytes` / `body_routes` |
| `web/src/main.ts` | 改 | 挂载前清空 `#app`, 避免静态快照与渲染结果并存 |
| `.github/workflows/pages.yml` | 改 | `paths` 加 `tools/prerender_body.py`; 预渲染步骤补注释 |
| `docs/architecture/web_p0_routes.json` | 改 | 重新生成 (发布仓 / CI 基线, 1350 路由, 带 `body_*` 字段) |

## 4. 复现与实测命令

```
# 1) 数据与前端构建 (顺序不能变: export 会清空 web/public/data)
python3 tools/export_static_site.py
python3 tools/build_search_index.py
python3 tools/build_unified_index.py
cd web && VITE_DATA_MODE=static npm run build && cd ..
python3 tools/pages_preflight.py --stage dist
# 2) 预渲染 (head + 关键路由正文快照)
python3 tools/prerender_routes.py
```

# 3) 静态托管深链复核 (Pages 的目录回落语义与 http.server 一致)

mkdir -p /tmp/serve && ln -sfn "$PWD/web/dist" /tmp/serve/protreptic
cd /tmp/serve && python3 -m http.server 8100   # 另一终端
curl -s -o /dev/null -w "%{http_code}\\n" http://127.0.0.1:8100/protreptic/minds/ARR/

```

实测输出 (节选):

```

[prerender] 正文快照 50 条, 共 1852 KB
[prerender] base=/protreptic/ routes=1350
[prerender] wrote 1350 index.html, total 5742 KB

OK  figures              http=200 snapshot=True  plain_chars=1463
OK  modes                http=200 snapshot=True  plain_chars=3065
OK  templates/chibi      http=200 snapshot=True  plain_chars=5029
OK  minds/ARR            http=200 snapshot=True  plain_chars=6911
OK  figures/A-1-X-P      http=200 snapshot=False plain_chars=37
[summary] checked=19 not200=0 missing_snapshot=0 short=0

```

浏览器复核 (Chromium, `/protreptic/minds/AMU/`): `snapshot_after_mount=false`, `has_nav=true`,
`articles=10`, `h1=["阿蒙森"]`, `text_len=18626`。

## 5. 未覆盖 / 下一步 (建议, 本卡不做)

- `/figures/{code}` 场景详情 1056 条与其余 243 个人物页仍是 head-only: 复用 `prerender_body.py`
  加一个 `render_scenario()` 并按同样的限量策略 (例如前 30 条) 即可, 单页预计 3 到 8 KB;
- 发布后需在线上复测同一张 URL 清单 (本地已验证同构产物, 但线上 Pages 行为 [未验证]);
- 发布仓与工作区的数据基线漂移仍在 (A0 1.1 节), 修它属于仓库卫生卡。

## 6. 提交与发布状态

本会话没有 `gh` CLI 与远端凭据, `git push` 不可用, 推送需要人工或带凭据的会话执行;
Pages 发布在推送后由 `.github/workflows/pages.yml` 自动完成。
