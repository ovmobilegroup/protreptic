# GoatCounter 自托管接入指南

## 概述

Protreptic 网站接入 [GoatCounter](https://www.goatcounter.com) 免费统计，自托管部署。

- **线上地址**: https://ovmobilegroup.github.io/protreptic/
- **隐私声明**: 不采集个人数据、不设 cookie、无需 consent banner
- **当前状态**: 前端脚本已注入，endpoint 指向占位符，待生产环境上线后更新

## 技术细节

### 已完成的修改

1. **web/index.html** - 主入口注入统计脚本
2. **tools/prerender_routes.py** - 预渲染脚本同步注入（1349 个路由）
3. **tools/gc/** - 自托管工具集
   - `gc` - GoatCounter v2.7.0 二进制
   - `count.js` - 统计脚本源文件
   - `init_site.sh` - 站点初始化脚本
   - `serve.sh` - 服务启动脚本
   - `download_gc.sh` - 版本更新脚本
4. **.gitignore** - 忽略二进制文件（体积过大）

### 验证清单

| 检查项 | 状态 | 备注 |
|--------|------|------|
| 前端 script 标签存在 | ✅ | `web/index.html` |
| 预渲染路由含 script | ✅ | 1349 个路由均已注入 |
| dist 构建通过 | ✅ | `npm run build` 正常 |
| prerender 运行通过 | ✅ | `python3 tools/prerender_routes.py` |

## 生产部署步骤

### 方案 A：自有 VPS（推荐）

```bash
# 1. 下载二进制
./tools/gc/download_gc.sh

# 2. 初始化站点
export GOATCOUNTER_DB=/var/lib/goatcounter/protreptic.sqlite3
./tools/gc/init_site.sh

# 3. 启动服务
export GOATCOUNTER_LISTEN=:80
./tools/gc/serve.sh
```

更新 web/index.html 和 prerender_routes.py 中的 `GC_ENDPOINT` 为真实地址。

### 方案 B：Docker 部署

```bash
docker run -d \
  --name protreptic-gc \
  -p 8080:8080 \
  -v /var/lib/goatcounter:/home/goatcounter/goatcounter-data \
  arp242/goatcounter
```

## 故障排查

- **400 错误**: URL query 编码问题，检查 script 调用格式
- **Dashboard 无数据**: 检查站点创建和 API token 权限
- **本地测试**: 已在 script settings 中设置 `"allow_local": true`
