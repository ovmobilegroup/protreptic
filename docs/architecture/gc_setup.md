# 访问统计：当前未接入（Phase31-AN 收口）

> Phase45-A: 官方托管 (GoatCounter) 的接入路径已就位, 是构建期开关、缺省 inert 状态。
> 注册 / 填值 / 本地验证 / 回滚步骤见 `docs/community/analytics_setup.md` 文件。
> 本文保留的是自托管路径与「当初为什么没接」的实测记录。

> 卡片 `t_7f963543` / 日期: 2026-09-19 / 线上: https://ovmobilegroup.github.io/protreptic
>
> 现状: **站点不加载任何统计脚本**。C3 交付时留下的占位符端点已从
> `web/index.html` 与 `tools/prerender_routes.py` 中**删除** —— 占位符不能当成已接入。

## 0. 结论

- 线上页面: 无统计脚本、无 cookie、无统计请求；代价是**没有访问量数据**。
- `tools/gc/`（GoatCounter 自托管工具链）原样保留，作为将来接入的现成路径。
- 验收（两条都期望输出 `0`）:

```
curl -sL https://ovmobilegroup.github.io/protreptic/ | grep -c goatcounter
curl -sL https://ovmobilegroup.github.io/protreptic/404.html | grep -c goatcounter
```

## 1. 为什么当前拿不到可用端点

发布通道是 GitHub Pages: 纯静态托管、没有后端，前端只能把统计打到别人家或自家另一台机器上。
三条候选路径逐条实测后都不成立:

1. **GoatCounter 官方托管（有免费额度）** —— 需要注册账号并绑定邮箱，属于站点所有者本人的账号操作，
   自动化任务无权代建，也不能借用他人站点码。2026-09-19 实测:
   - `https://demo.goatcounter.com/count?p=%2Fx&t=x` 返回 **200**（站点存在）
   - `https://ovmobilegroup.goatcounter.com/...` 返回 **400**
   - `https://protreptic.goatcounter.com/...` 返回 **400**
   - 随机构造的不存在站点 返回 **400**（与未注册同码）
   即: 两个候选站点码都未注册，而注册这一步必须由人来做。
1. **自托管（`tools/gc/` 已备好二进制与脚本）** —— 需要一台公网可达、有域名与 TLS 证书的常驻主机。
   当前构建机没有公网 HTTPS 入口、没有域名、没有 TLS 终止（`cloudflared` / `caddy` / `nginx` /
   `tailscale` / `certbot` 均未安装）。Pages 是 HTTPS，脚本指向 http 端点会被浏览器按混合内容直接拦掉。
1. **等价免费服务**（Plausible CE / Umami / Fathom / Cloudflare Web Analytics / Netlify、Vercel 自带统计等）
   —— 同样要么需要账号，要么需要自托管主机，约束与上面两条相同。

**选择撤下而不是留着**: 一个指向不存在主机的脚本不会产生任何数据，只会造成「已经在统计」的错觉，
并在每个访客的控制台里持续报错。

## 2. 以后要接入时的步骤

1. 准备入口: 自有 VPS（域名 + TLS）或官方托管的站点码（需账号）。
1. 自托管初始化与启动:

```bash
./tools/gc/download_gc.sh
export GOATCOUNTER_DB=/var/lib/goatcounter/protreptic.sqlite3
./tools/gc/init_site.sh
export GOATCOUNTER_LISTEN=:8080
./tools/gc/serve.sh          # TLS 由前置反向代理终止
```

1. 端点写回两处（必须同时改，否则只有首页有脚本、深链页没有）:
   - `web/index.html` 的 `<head>`
   - `tools/prerender_routes.py` 的 `extra`（预渲染页统一注入点）
1. 重新构建并发布:

```bash
cd web && VITE_DATA_MODE=static npm run build && cd ..
python3 tools/prerender_routes.py --body-persons all
```

   然后同步进发布仓 -> `git push origin main` -> 等 `pages.yml` 跑完。

1. 验收: 首页 HTML 出现真实端点；打开一次页面后 GoatCounter 侧出现 1 条计数。

## 3. 本次改动清单

| 文件 | 改动 |
| --- | --- |
| `web/index.html` | 删除占位符 script，只留一行注释指向本文 |
| `tools/prerender_routes.py` | 删除 `GC_ENDPOINT` 常量与 head 注入 |
| `README.md` | 「部署」章节写明未接入访问统计 |
| `docs/architecture/gc_setup.md` | 本文（状态 + 原因 + 以后接入步骤） |
| `tools/gc/*` | 保留不动（未启用） |

## 4. 隐私口径未变

原来承诺的「不采集个人数据、不设 cookie」现在更严格: 连统计脚本都没有。
将来若接入，仍需保持这一口径（GoatCounter / Plausible 一类 cookieless 方案满足）。

## 5. 自托管路径实测记录（2026-09-19，本地回环）

没有域名/公网入口，但自托管链路本身已经跑通，证明 `tools/gc/` 可用、缺口只在「一个公网 HTTPS 入口」：

```
$ mkdir -p /tmp/gc_proof1 && export GOATCOUNTER_DB=/tmp/gc_proof1/protreptic.sqlite3
$ ./tools/gc/init_site.sh
[init] db=/tmp/gc_proof1/protreptic.sqlite3
[init] done. Dashboard: ./tools/gc/gc serve --db sqlite+/tmp/gc_proof1/protreptic.sqlite3 --listen :8080

$ GOATCOUNTER_DB=/tmp/gc_proof1/protreptic.sqlite3 GOATCOUNTER_LISTEN=:8099 ./tools/gc/serve.sh   # 后台常驻

$ curl -s -o /dev/null -w "%{http_code} %{size_download}\n" http://127.0.0.1:8099/count.js
200 8940

$ curl -s -o /dev/null -w "%{http_code}\n" -A "<Chrome UA>" -e "https://protreptic.goatcounter.local/" \
    -H "Host: protreptic.goatcounter.local" "http://127.0.0.1:8099/count?p=%2Fproof&t=proof"
200                      # 无 X-Goatcounter 错误头 => 该次命中被接受

$ ./tools/gc/gc db query --db "sqlite+/tmp/gc_proof1/protreptic.sqlite3" "select * from hit_counts"
site_id  path_id  hour                 total
1        1        2026-09-18 22:00:00  1

$ ./tools/gc/gc db query --db "sqlite+/tmp/gc_proof1/protreptic.sqlite3" "select * from hit_stats"
site_id  path_id  day                  stats
1        1        2026-09-18 00:00:00  [0,0,...,1(第22小时),0]
```

结论：`count.js` 加载 → `/count` 上报 → `paths` / `hit_counts` / `hit_stats` 落库，端到端可用。
唯一缺口是线上页面必须指向 **HTTPS、公网可达** 的 GoatCounter 主机（Pages 是 HTTPS，
http 端点会被浏览器按混合内容拦掉），以及官方托管站点码需要人工注册。
因此本卡仍选「撤下占位符」；拿到域名/主机后按第 2 节接入即可。
