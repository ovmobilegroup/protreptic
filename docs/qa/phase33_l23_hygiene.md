# Phase33-L23 双仓卫生报告: web_p0_routes.json 同步 + 工作区未提交改动收口

卡片 t_e07221d0 / 工人 bustamante / 2026-09-19 (Asia/Shanghai)
项目仓 /opt/data/workspace/Protreptic ; 发布仓 /opt/data/release/Protreptic-publish

## 0. 结论

- L2 (登记产物双仓不一致) **已收口**: 两仓 docs/architecture/web_p0_routes.json 的 sha256
  均等于线上产物 088a99a10476986524d84f7886bfb1dd981f93d23dc1fed6d37e34c532e80e6d.
- L3 (工作区未提交改动) **本卡点名的 12 项逐项处置完毕**: 11 项提交, 1 项按 HEAD 还原 (依据见第 3 节).
  终态两仓残余 dirty 项全部属于并发运行的 Phase33-L1 (t_493e6506 / elcano) 在制品, 非本卡范围 (见第 5 节).
- 发布仓 ahead=0; 与本次改动相关的四个 workflow 全 success, 且 Quality Gate / Pages 的 job 数是 3 / 2, 不是幻影 0 job.

## 1. 判据: 哪个副本才是正确当前态

线上这份产物可以直取 (CI 把 checkout 内的 docs/ 一起 mkdocs 构建并上传), 所以判据可以硬碰硬:

    $ curl -s -o /tmp/live_routes.json -w "http=%{http_code} bytes=%{size_download}\n" \
        https://ovmobilegroup.github.io/protreptic/docs/architecture/web_p0_routes.json
    http=200 bytes=684093
    $ sha256sum /tmp/live_routes.json
    58728a5b87bf0970378e8229335ff443fe80f1d26411f7f32e5e2424822d430d   # 09:12 时刻的线上产物

本地按当前源码原地重建 (与 CI pages.yml 同一条命令), 输出与线上逐字节一致:

    $ python3 tools/prerender_routes.py --body-persons all --routes-out /tmp/ws_repro_routes.json
    [prerender] 正文快照 293 条, 共 12304 KB
    [prerender] base=/protreptic/ routes=1353
    [prerender] wrote 1353 index.html, total 18945 KB
    $ sha256sum /tmp/ws_repro_routes.json /tmp/live_routes.json
    58728a5b87bf0970378e8229335ff443fe80f1d26411f7f32e5e2424822d430d  /tmp/ws_repro_routes.json
    58728a5b87bf0970378e8229335ff443fe80f1d26411f7f32e5e2424822d430d  /tmp/live_routes.json

两个旧副本都过期, 而且过期方式不同:

- 发布仓副本 sha256 803eb6ae: body_count=50 / total_html_bytes=8541471, 是 Phase30-A2 引入 --body-persons all
  之前默认 40 时代的产物; 连路由描述文本都还是旧的 (figures 路由写 501 个现代场景, 线上写 1055 个).
- 工作区副本 sha256 915d3378: body_count=293 已经正确, 但 2 个字节统计字段取自更早的 dist 外壳
  (total_html_bytes=18939590). 用 git diff --no-index 比对, 工作区副本与本地重建只差这 2 行.

=> 正确当前态 = 能复现线上产物的那次构建 = 58728a5b (随后被并发卡的提交推到了 088a99a1, 见第 2 节).

## 2. 同步动作与 push 实况

### 2.1 第一次同步 (发布仓提交 6d2c42a)

    $ cp /tmp/live_routes.json docs/architecture/web_p0_routes.json   # 发布仓
    $ sha256sum docs/architecture/web_p0_routes.json
    58728a5b87bf0970378e8229335ff443fe80f1d26411f7f32e5e2424822d430d
    $ git commit -m "chore(arch): Phase33-L23 web_p0_routes.json 对齐线上构建产物..."
    $ HOME=/opt/data/home PATH=/opt/data/home/.local/bin:$PATH git push origin main
    To https://github.com/ovmobilegroup/protreptic.git
       21706cc..6d2c42a  main -> main
    $ git status -sb
    ## main...origin/main                 # 无 [ahead N]
    $ git rev-list --count origin/main..HEAD
    0

### 2.2 再同步 (发布仓提交 c4c0c97)

并发运行的 Phase33-L1 (elcano, t_493e6506) 提交 f5a8a34 改了 web/index.html 外壳长度,
线上登记产物随之变化。这是本文件字节与 SPA 外壳强耦合的直接证据:

    $ curl -s -o /tmp/live_routes3.json -w "http=%{http_code} bytes=%{size_download}\n" .../web_p0_routes.json
    http=200 bytes=684094
    $ sha256sum /tmp/live_routes3.json
    088a99a10476986524d84f7886bfb1dd981f93d23dc1fed6d37e34c532e80e6d
    $ git diff --no-index /tmp/live_routes3.json docs/architecture/web_p0_routes.json
    - total_html_bytes: 19660742      (旧 19399610, 1353 条路由, 约每条 +193 B 外壳增长)
    - figures 路由 description: "283 位历史人物 + 1055 个现代场景"  (旧值 501)
    body_count / body_total_bytes 未变: 293 / 12599583

已把两仓副本对齐到该新产物:

    $ HOME=/opt/data/home PATH=/opt/data/home/.local/bin:$PATH git push origin main
    To https://github.com/ovmobilegroup/protreptic.git
       f5a8a34..c4c0c97  main -> main
    $ git status -sb            # ## main...origin/main, ahead=0
    $ sha256sum docs/architecture/web_p0_routes.json \
        /opt/data/workspace/Protreptic/docs/architecture/web_p0_routes.json /tmp/live_routes3.json
    088a99a10476986524d84f7886bfb1dd981f93d23dc1fed6d37e34c532e80e6d  docs/architecture/web_p0_routes.json
    088a99a10476986524d84f7886bfb1dd981f93d23dc1fed6d37e34c532e80e6d  /opt/data/workspace/.../web_p0_routes.json
    088a99a10476986524d84f7886bfb1dd981f93d23dc1fed6d37e34c532e80e6d  /tmp/live_routes3.json

部署后回读 (第 6 节) 该文件仍是 088a99a1, 说明提交的那份等于 CI 现场生成的那份。

## 3. L3 逐文件处置

工作区 git status --porcelain 基线 (处置前):

     M api/protreptic.db
     M data/figure_names.json
     M data/figures/H-HuoQuBing-001.json
     M data/modes_data.json
     M docs/architecture/web_p0_routes.json
     M tools/build_graph_data.py
     M tools/build_unified_index.py
     M tools/ci_data_check.py
     M tools/figure_library.py
     M tools/prerender_routes.py
     M tools/thinking_mode_selector.py
    ?? tools/fix_dirty_figure_names.py

逐文件 sha256 (工作区 vs 发布仓) 后决定处置:

1. data/modes_data.json              -> 提交. 与发布仓同 sha256 cc43a609011ad059, 属发布仓已改工作区漏提交.
2. data/figure_names.json            -> 提交. 同 sha256 e31b3a2e08ce52e5.
3. data/figures/H-HuoQuBing-001.json -> 提交. 同 sha256 5f7532ee543cf606.
4. tools/build_graph_data.py         -> 提交. 同 sha256 21c83c30d53d4905.
5. tools/build_unified_index.py      -> 提交. 同 sha256 3296dadacfd3095e.
6. tools/ci_data_check.py            -> 提交. 同 sha256 8efa76d471de2a18.
7. tools/figure_library.py           -> 提交. 同 sha256 6544d8978800d770.
8. tools/prerender_routes.py         -> 提交. 同 sha256 608acecb79279045.
9. tools/thinking_mode_selector.py   -> 提交. 同 sha256 f239d91198582ca0.
10. tools/fix_dirty_figure_names.py  -> 提交 (原为未跟踪). 与发布仓已入库副本同 sha256 e2110f5927f2973f,
    幂等定点替换脚本 (获取兵 改 霍去病), 入库以便审计与复跑.
11. docs/architecture/web_p0_routes.json -> 提交. 见第 1/2 节 (由过期值收到 58728a5b, 后又收到 088a99a1).
12. api/protreptic.db                -> 按 HEAD 还原, 不提交. 依据:
    a) 它不是任何东西的唯一副本: 由 tools/build_figures_db.py 派生, CI 的 Step 0 每次现场重建,
       且 api/ 不进 Pages 产物 (_site = web/dist + site_docs), 线上没有任何页面读它.
    b) 内容无差异: 逐表全列 dump 比对 HEAD 版与工作区版, figures 1057 行 / thinking_modes 2858 行
       完全一致 (diff 0 行). 所以还原不会丢任何数据改动.
    c) 它的文件字节本来就没有唯一正确值: 同一份输入连续三次重建得到三个 sha256
       (cccd3de4 / ca86ecf8 / 3fbf8126), SQLite 的页布局随历史变化. 提交它只是噪音, 且是 38 MB blob.
    结论: 不是盲目 checkout, 是先证明内容等价、字节不可复现之后才还原.

工作区提交记录 (本地 master, 未 push):

    01cf217e chore(tools): Phase33-L23 入库 fix_dirty_figure_names.py
    ad7989af chore(hygiene): Phase33-L23 收口工作区未提交的数据/工具改动
    9d079fe5 chore(arch): Phase33-L23 web_p0_routes.json 对齐线上构建产物
    e258a797 chore(arch): Phase33-L23 web_p0_routes.json 跟随 Phase33-L1 构建再同步

## 4. 该不该 gitignore

本卡选择同步, 未改跟踪策略 (改跟踪会动到发布仓契约, 应由编排者决定)。

支持改 gitignore 的证据:

- 它是产物. manifest 自述 generated_by = tools/prerender_routes.py.
- CI 在 checkout 内重新生成后才给 build_sitemap 与 mkdocs; 线上那份也是 CI 现场生成.
- 提交的那份值从不影响线上, 只影响本地复跑与审计口径.
- 它的字节与 SPA 外壳强耦合, 必然漂移: 实测同日先差 460 KB, 又因 L1 口径修复差 261 KB.
- 漂移是默认状态, 因为 CI 不会替你提交它.

保留入库的理由:

- 它是本地 build_sitemap 的输入; 历史 QA 用它做路由登记.
- 它可复现 (本卡两次都逐字节复现), 不是随机值, 只是随构建输入变化.

## 5. 终态与残余 dirty 项

发布仓 (作业结束时实测): status -sb 显示 ## main...origin/main, ahead=0;
唯一 dirty 是 docs/qa/phase33_l1_count_unification.md, 属 elcano 在制.

工作区 (作业结束时实测): 本卡点名 12 项全部干净; 残余 dirty 全为 elcano/Phase33-L1 在制品,
共 17 项, 集中在 tools/*.py 与 web/ 下 (apply_site_counts, build_daily_index, build_search_index,
export_static_site, og_image, pages_preflight, prerender_routes, web/index.html, web/src/**).

取证: 这些文件 mtime 在本卡作业期间持续被刷新 (web/index.html 与 tools/og_image.py 于 09:13:28,
mkdocs.pages.yml 于 09:24:05), 且 t_493e6506 状态为 running.
本卡未纳入任何 elcano 在制文件: 一次误 git add -A 已用 git reset 撤销, 之后全部用显式 pathspec 提交.

## 6. CI 实况 (gh 实取)

第一次同步 6d2c42a:

- Deploy to GitHub Pages 35412072456: success, jobs = [构建 SPA + 文档站, 部署] 共 2 个, 非幻影
- CI 35412072533: success (markdown-lint)
- Protreptic CI/CD 35412072650: success, jobs = [Test (Python + TypeScript), Build API Docker Image,
  Build Web Docker Image, Notify]; Deploy to Staging/Production 为 skipped

再同步 c4c0c97:

- Deploy to GitHub Pages 35413081869: success (headSha c4c0c978), jobs 2 个
- CI 35413081951: success
- Protreptic CI/CD 35413081872: Test 与 Build Web Docker Image 成功 (Build API Docker Image 在本报告写作时仍在跑)
- Quality Gate 35413344741: success, jobs = [数据校验 (schema + sitemap 一致性),
  线上死链检测 (sitemap + 站内链接), Lighthouse 预算门] 共 3 个, 非幻影

部署后线上回读 (证明提交的那份等于 CI 现场生成的那份):

    $ curl -s -o /tmp/live_routes4.json -w "http=%{http_code} bytes=%{size_download}\n" \
        https://ovmobilegroup.github.io/protreptic/docs/architecture/web_p0_routes.json
    http=200 bytes=684094
    $ sha256sum /tmp/live_routes4.json
    088a99a10476986524d84f7886bfb1dd981f93d23dc1fed6d37e34c532e80e6d

## 7. 复现命令清单

    # 判据: 线上登记产物 vs 本地重建
    curl -s -o /tmp/live.json -w "%{http_code} %{size_download}\n" \
      https://ovmobilegroup.github.io/protreptic/docs/architecture/web_p0_routes.json
    cd /opt/data/workspace/Protreptic && python3 tools/prerender_routes.py --body-persons all \
      --routes-out /tmp/repro.json
    sha256sum /tmp/live.json /tmp/repro.json \
      /opt/data/workspace/Protreptic/docs/architecture/web_p0_routes.json \
      /opt/data/release/Protreptic-publish/docs/architecture/web_p0_routes.json

    # L3: 双仓逐文件比对 + DB 内容等价性
    git -C /opt/data/workspace/Protreptic status --porcelain --untracked-files=all
    git -C /opt/data/workspace/Protreptic show HEAD:api/protreptic.db > /tmp/db_head.db
    python3 -m sqlite3 /tmp/db_head.db "SELECT COUNT(*) FROM figures;"
    python3 -m sqlite3 /tmp/db_head.db "SELECT * FROM figures ORDER BY code;" > /tmp/a.txt
    python3 -m sqlite3 api/protreptic.db "SELECT * FROM figures ORDER BY code;" > /tmp/b.txt
    diff /tmp/a.txt /tmp/b.txt

    # 全局
    git -C /opt/data/release/Protreptic-publish status -sb
    git -C /opt/data/release/Protreptic-publish rev-list --count origin/main..HEAD
    HOME=/opt/data/home PATH=/opt/data/home/.local/bin:$PATH gh run list --repo ovmobilegroup/protreptic --limit 8

## 8. 附录: 收尾实测 (本报告自身提交与终态回读)

本报告提交: 发布仓 3ef02b8, 工作区 435cb6de.

终态两仓工作树:

- 发布仓: status -sb 为 ## main...origin/main, ahead=0, behind=0, 无 dirty 文件
- 工作区: git status --porcelain --untracked-files=all 输出为空
- L2 三处 sha256 一致 (发布仓 / 工作区 / 线上直取): 088a99a10476986524d84f7886bfb1dd981f93d23dc1fed6d37e34c532e80e6d

说明: 第 5 节写作时两仓仍有 elcano/Phase33-L1 的在制文件; 在本报告提交前后, elcano 已把那些改动
自行提交并推送, 因此终态两仓都干净。本卡从未提交任何 elcano 的文件。

本报告自身提交 3ef02b8 上的四个 workflow:

- Deploy to GitHub Pages 35413833992: success, jobs 2 个 (构建 SPA + 文档站, 部署)
- CI 35413834004: success (markdown-lint); 本地先用 npx markdownlint-cli2@0.13.0 加 .markdownlint.json 预检, 0 error
- Quality Gate 35414047354: success, jobs 3 个 (数据校验, 线上死链检测, Lighthouse 预算门)
- Protreptic CI/CD 35413834003: success, jobs = Test (Python + TypeScript) / Build Web Docker Image /
  Build API Docker Image / Notify; Deploy 两步 skipped

本报告线上地址 (curl http=200, title 已核对):

    https://ovmobilegroup.github.io/protreptic/docs/qa/phase33_l23_hygiene/
