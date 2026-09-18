# web_p0_architecture.md 的取证记录

本文件记录 `web_p0_architecture.md` 里每个数字对应的命令与原始输出.
环境: Node v26.5.1 / npm 11.17.0 / vite 5.4.21 / Python 3.13; 时间 2026-09-18.

## E1 线上 HTTP 状态码

```
$ for p in /protreptic/ /protreptic/figures /protreptic/modes /protreptic/minds/H-MO-001 \
           /protreptic/figures/H-MO-001 /protreptic/templates /protreptic/templates/ \
           /protreptic/templates/chibi.md /protreptic/data/meta.json /protreptic/404.html; do
    printf "%-40s " "$p"; curl -s -o /dev/null -w "%{http_code}\n" "https://ovmobilegroup.github.io$p"
  done

/protreptic/                             200
/protreptic/figures                      404   (响应体 2094 B, 等于 SPA 外壳)
/protreptic/modes                        404
/protreptic/minds/H-MO-001               404
/protreptic/figures/H-MO-001             404
/protreptic/templates                    301   (location: .../protreptic/templates/)
/protreptic/templates/                   404
/protreptic/templates/chibi.md           200   (size 13162, text/markdown)
/protreptic/data/meta.json               200   (size 2889, application/json)
/protreptic/404.html                     200   (size 2094, 与 index.html 相同)
```

## E2 前端代码与依赖环境

```
$ ls node_modules/@vue/
compiler-core compiler-dom compiler-sfc compiler-ssr compiler-vue2 devtools-api
language-core reactivity runtime-core runtime-dom server-renderer shared

$ ls node_modules | grep -iE "prerender|puppeteer|playwright|ssg|jsdom"
(无匹配)

$ grep '"version"' node_modules/vue-router/package.json node_modules/@vue/server-renderer/package.json \
      node_modules/vue/package.json node_modules/vite/package.json
vue-router 4.6.4 / @vue/server-renderer 3.5.40 / vue 3.5.40 / vite 5.4.21
```

## E3 required build

```
$ cd web && VITE_DATA_MODE=static npm run build
> vue-tsc && vite build
vite v5.4.21 building for production...
transforming... ✓ 112 modules transformed.
dist/index.html                   1.88 kB │ gzip:  1.11 kB
dist/assets/index-BRFwtcFp.css   41.69 kB │ gzip:  7.80 kB
dist/assets/index-Dmk-GL4Z.js   255.52 kB │ gzip: 92.34 kB
✓ built in 4.62s     real 0m9.225s
```

## E4 体积基线

```
$ python3 tools/measure_web_p0_baseline.py
figures.index.json       157.3 KB raw /   32.3 KB gzip
index.unified.json       360.3 KB raw /  109.5 KB gzip
modes/index-*.json      2556.5 KB raw / 1114.7 KB gzip
modes/by-figure/*.json    19.9 MB raw /    8.1 MB gzip  median  27.9 KB gzip
figures/*.json             1.5 MB raw /    0.5 MB gzip  median   1.1 KB gzip
app shell                297.1 KB raw /   99.2 KB gzip
prerendered route dirs  795 ( 2448.8 KB raw)
-> docs/architecture/web_p0_baseline.json
```

补充 (同一脚本的 json 产物): by-figure p90 41.5 KB gzip; figures p90 1.8 KB gzip;
`modes/index-0..7.json` 单片 gzip 依次为 155.0 / 137.4 / 145.6 / 138.5 / 137.1 / 134.1 / 127.5 / 139.5 KB;
`meta.json` gzip 1.4 KB.

## E5 语料口径

```
$ python3 (逐字段统计 284 个 by-figure 分片的 2858 条模式)
ZH 全字段字符 = 3629083
EN 全字段字符 = 8653082
ALL           = 12282165
definition_zh+process_zh+cases_zh+apps_zh+domain_zh = 2351782  (2.35M, 最接近任务书的 2.4M)
definition_zh+process_zh+cases_zh+apps_zh            = 2070781
definition_zh+process_zh+cases_zh+apps_zh+quote_zh+concepts+source = 2645177
ZH 正文(排除元数据字段) = 3024167
```

## E6 检索索引体积矩阵

见 `web_p0_architecture.md` 4.2 的两张表. 补充: 全字段集 (14 字段, 中英) 的 JSON 差值方案
= 10.54 MB raw / 4.11 MB gzip (24 片); 带词频权重的二进制方案 = 5.01 MB gzip.
推荐规格的 doc_id 对齐实测:

```
doc_id 空间 = 2858 (modes/index-0..7.json 顺序拼接)
by-figure 有而 index 无: 0
index 有而 by-figure 无: 0
tokens 99016
N=12  TOTAL_gz= 738KB max=74KB min=45KB
N=16  TOTAL_gz= 741KB max=59KB min=37KB
N=24  TOTAL_gz= 740KB max=42KB min=21KB
```

## E7 路由预渲染

发布的基线由 CI 现场重建 (见 E14), 因此预渲染在发布仓基线上取证:

```
$ cd /opt/data/release/Protreptic-publish
$ python3 tools/build_figures_db.py          # CI Step 0
  figures 表重建完成: 1058 行 -> api/protreptic.db
$ python3 tools/export_static_site.py        # CI Step A
  产物 1352 个文件; figures=1058 modes=2858 by-figure=284; index gzip 33.8 KB <= 50.0 KB
$ python3 tools/build_unified_index.py       # CI Step A2
  total=1339  figures=283  scenarios=1056  with_modes=1303; 体积 436.3 KB

$ time python3 tools/prerender_routes.py --dist web/dist --routes-out docs/architecture/web_p0_routes.json
[prerender] base=/protreptic/ routes=1350
[prerender] excluded figure codes (not in public register): H-SX-001
[prerender] wrote 1350 index.html, total 3888 KB
real 0m0.348s
```

`web_p0_routes.json` 头部:

```
count            = 1350
total_html_bytes = 3981599
counts_by_type   = {static:4, person:283, scenario:1056, template:7}
excluded_figure_codes = ["H-SX-001"]
```

工作区本地基线上同样跑通 (795 条 / 2497 KB / 0.27 s), 见 E14 的基线差异说明.

## E8 本地托管下的状态码全量扫描

```
$ mkdir -p /tmp/p0site1/protreptic && cp -r web/dist/. /tmp/p0site1/protreptic/
$ cd /tmp/p0site1 && python3 -m http.server 4211 --bind 127.0.0.1
$ python3 sweep.py
routes=1350  status={200: 1350}  failures: 0
```

定点:

```
/protreptic/                             200
/protreptic/figures                      301
/protreptic/figures/                     200
/protreptic/modes                        301
/protreptic/modes/                       200
/protreptic/templates                    301
/protreptic/templates/                   200
/protreptic/templates/chibi              301
/protreptic/templates/chibi/             200
/protreptic/figures/A-1-X-P/             200
/protreptic/minds/Sun%20Quan/            200
/protreptic/data/meta.json               200
/protreptic/no-such-page                 404
```

## E9 结构化数据完整性

```
$ python3 verify_ld.py
files=1350  ld_ok=1350  canonical=1350  bad=0
@type histogram {'CreativeWork': 1060, 'Article': 7, 'Person': 283}
```

## E10 预渲染产物体积

```
prerendered pages=1350  raw=3888KB  gzip=1674KB  avg_raw=2949B
web/dist 文件合计 29152912 B (29.2 MB; 预渲染前约 25.2 MB)
$ cmp web/dist/404.html web/dist/index.html   -> 相同
```

## E14 发布仓基线与工作区基线的差异

```
$ python3 tools/build_figures_db.py            # 在发布仓跑
  figures 表重建完成: 1058 行
$ ls -la api/protreptic.db (发布仓)            -> 1671168 B
$ ls -la api/protreptic.db (工作区)            -> 38490112 B (2026-09-17 20:29)

$ sha256sum data/modes_data.json (两边)
  782e48cc388a14c8e2b802e0ee9c579944c3d316bdb9ff1c5bb73acd91763043   (相同)

$ git ls-files data | wc -l
  发布仓 1407   /   工作区 795
$ git ls-files tools | wc -l
  发布仓 777    /   工作区 1025
$ git ls-files tools | grep -vE "^tools/[A-Za-z0-9._/-]+$" | wc -l
  工作区 29 个 tracked 路径名字里带 shell 残留 (例如 tools/' 与 "tools/$"), 发布仓 0 个

发布仓基线: figures 1058 -> 公开名录 1339 -> 预渲染 1350 条
工作区基线: figures  501 -> 公开名录  784 -> 预渲染  795 条
```

线上实测 (2026-09-18):

```
$ curl -s https://ovmobilegroup.github.io/protreptic/data/index.unified.json | head -c 160
{"schema":"protreptic.unified_index/v1","counts":{"total":1339,"figures":283,"scenarios":1056,...}
$ curl -s https://ovmobilegroup.github.io/protreptic/data/meta.json
  counts.figures = 1058, generated_at = 2026-09-18T01:59:07+00:00

$ curl -s https://api.github.com/repos/ovmobilegroup/protreptic/actions/runs?per_page=3
  35297502381  Deploy to GitHub Pages  completed success  d1d4399d
  35297502340  CI                     completed failure  d1d4399d
  35297502332  Protreptic CI/CD       completed failure  d1d4399d

$ curl -s .../actions/runs/35297502381/jobs   (成功的 Pages 发布, 步骤清单)
  重建 figures 数据库 / 构建静态数据分片 / 构建统一索引 / 断言静态数据基线 /
  构建 SPA / 断言 dist 产物 / 安装文档站工具链 / 构建文档站 / 合并 SPA + 文档站 /
  断言合并产物 / Setup Pages / Upload Pages artifact   全部 success
```

## E11 检索功能验证 (原型脚本)

```
良知      -> M381 王阳明 11, M-NKR-004 恩克鲁玛 9, M-ASHOKA-005 阿育王 6
战略 决策  -> M-MYS-008 茅以升 19, M-GUE-006 切-格瓦拉 14, M-LH-010 利德尔-哈特 13
联盟 合作  -> M-BISMARCK-007 俾斯麦 9, M-GAN-002 甘地 9, M-CHU-005 丘吉尔 8
王阳明    -> M381 王阳明 8, M382 王阳明 8, M383 王阳明 8
心之本体  -> M-ST-001 石涛 13, M381 王阳明 9, M-LZH-003 李泽厚 9
decision  -> M-YSS-010 李舜臣 8, M-BELISARI-007 贝利撒留 4
decis     -> []            (拉丁前缀缺口, 见 4.6)
```

## E12 数据一致性核对

```
by-figure 284 / figures shards 501 / figures.index 501
unified figures 283 / unified scenarios 501
by-figure minus unified figures: ['H-SX-001']
unified figures minus by-figure: []
figures.index minus unified scenarios: []
unified scenarios minus figures.index: []
figures.index vs figures shards diff: [] (0)
index.unified.json counts = {'total': 784, 'figures': 283, 'scenarios': 501, 'with_modes': 760}
codes with space: 1  ['Sun Quan']
duplicate codes: 0
```

## E13 CI 变更校验

```
$ uv run --with pyyaml python3 yamlcheck.py
steps: ['Checkout','Set up Node 20','Set up Python 3.12','构建静态数据分片',
        '断言静态数据基线(meta.json 条数)','构建 SPA','断言 dist 产物',
        '路由预渲染 深链 200','安装文档站工具链','构建文档站',
        '合并 SPA + 文档站到 _site','断言合并产物','Setup Pages','Upload Pages artifact']
paths has prerender: True
```
