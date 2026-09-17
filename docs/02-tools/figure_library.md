# 历史人物思维模式库查询工具（figure_library）

> 把 Protreptic 的核心资产——**284 位历史人物 × 每人 10 条专属思维模式 = 2868 条**——接入可查询的产品层。

## 为什么有这个工具

项目早期产品层（CLI/Web/每日卡片）只接入了少量数据（39 条场景），
而八轮挖掘沉淀的 2868 条人物专属模式一直没被产品层读到。
本工具把两者打通：用户现在可以按人物、按模式、按关键词、按类目自由检索全部资产。

## 数据

- 数据文件：`data/modes_data.json`（2868 条，21MB）
- 人物名映射：`data/figure_names.json`
- 人物档案：`data/figures/*.json`

每条模式包含：模式名（中/英）、定义（中/英，含史实例证）、操作步骤（中/英）、
关键概念、出处章节、原话、史实案例、现代应用、相关模式、18 个规范类目。

## 命令行用法

```bash
# 库统计
python3 tools/figure_library.py --stats

# 列出全部历史人物（284 位）
python3 tools/figure_library.py -L

# 查看某位人物的全部 10 条思维模式
python3 tools/figure_library.py -f H-INM-001        # 稻盛和夫
python3 tools/figure_library.py -f INM              # 短码模糊匹配亦可

# 查看单条模式详情
python3 tools/figure_library.py -m M-DKR-009        # 笛卡尔·暂行道德准则法

# 按关键词搜索（名称/定义/概念/类目）
python3 tools/figure_library.py -s 矛盾

# 按类目列出
python3 tools/figure_library.py -c 军事战略

# 英文输出 / 导出 JSON
python3 tools/figure_library.py -f H-INM-001 --lang en
python3 tools/figure_library.py -f H-INM-001 -e json
```

## 在其他代码中使用

```python
from tools.figure_library import FigureLibrary

lib = FigureLibrary()
lib.figures()              # 全部人物 code
lib.figure("H-INM-001")    # 某人物全部模式
lib.mode("M-DKR-009")      # 单条模式
lib.search("矛盾")          # 关键词搜索
lib.stats()                # 统计
```

## 已接入的产品出口

| 出口 | 状态 |
|------|------|
| CLI `thinking_mode_selector.py -c <CODE>` | ✅ 未命中场景时回退查询本库 |
| 每日思维卡片（cron 14b3dfbb，每早 8 点） | ✅ prompt 已指向本库 |
| API `/api/v1/figures/{code}/modes` 等 | ✅ 数据已入 `thinking_modes` 表（2858 条） |
| Web 前端 | ⏳ 待接新接口 |

## API 接口（FastAPI）

装载数据：

```bash
cd api && python load_v6.py
```

接口：

- `GET /api/v1/thinking-modes` — 列表/筛选（`?category=&figure=&q=&limit=&offset=`）
- `GET /api/v1/thinking-modes/stats` — 统计
- `GET /api/v1/thinking-modes/{mode_code}` — 单条详情
- `GET /api/v1/figures/{code}/modes` — 某人物全部模式
