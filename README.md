# Protreptic · 思维模式库

> **2868 条思维模式 · 284 位历史人物 · 中英双语**
>
> 遇到问题不知道用什么方法？查一查历史上有谁遇到过类似问题、他怎么想的——
> 每个人的方法都有出处、可执行步骤和现代应用。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Modes](https://img.shields.io/badge/modes-2868-blue.svg)](data/modes_data.json)
[![Figures](https://img.shields.io/badge/figures-284-green.svg)](data/figures)

---

## 这是什么

一座**历史人物的思维方法库**。从古今中外 284 位人物（孔子到费曼、李世民到乔布斯）
身上，各提炼出 10 条**可操作的思维方法**，共 2868 条，中英双语。

每条模式包含：

- **名称**（中/英）
- **定义**（60-150 字，含该人物的史实例证）
- **操作步骤**（4-6 步，可执行）
- **关键概念**
- **出处**（具体到著作章节，如《谈谈方法》第三部分）
- **原话**（名言引文）
- **史实案例**
- **现代应用**

不是鸡汤：每条都能追溯到原始文本或事件，都有可执行的步骤。

---

## 快速开始

把仓库克隆下来即可查询，**无需安装任何东西**。

```bash
# 库统计（2868 条 / 284 人 / 18 类目）
python3 tools/figure_library.py --stats

# 列出全部历史人物
python3 tools/figure_library.py -L

# 查看某位人物的全部 10 条思维模式
python3 tools/figure_library.py -f H-INM-001        # 稻盛和夫
python3 tools/figure_library.py -f H-WYM-001        # 王阳明

# 查看单条模式详情
python3 tools/figure_library.py -m M-DKR-009        # 笛卡尔·暂行道德准则法

# 关键词搜索
python3 tools/figure_library.py -s 矛盾

# 按类目列出
python3 tools/figure_library.py -c 军事战略

# 英文输出
python3 tools/figure_library.py -f H-INM-001 --lang en
```

作为 Python 模块使用：

```python
from tools.figure_library import FigureLibrary

lib = FigureLibrary()
lib.figures()              # 全部人物 code
lib.figure("H-INM-001")    # 某人物的全部模式
lib.mode("M-DKR-009")      # 单条模式
lib.search("矛盾")          # 关键词搜索
lib.stats()                # 统计
```

---

## 经典思维方法示例

**笛卡尔 · 暂行道德准则法**（《谈谈方法》第三部分）
> 知识地基拆除期间生活不能停摆：① 服从所在国法律与习俗；② 一旦决定即如箭在弦，犹豫比选错更消耗；③ 只改变自己的欲望而非世界的秩序。

**稻盛和夫 · 会计学经营检验法**（《稻盛和夫的实学：经营与会计》）
> 把会计改造成经营的中枢神经：每条数字背后必须有实物对应，每件实物必须有数字对应——看不见数字的现场是谣言，看不见现场的数字是谎言。

**孙子 · 庙算先胜五事七计法**（《孙子兵法·计篇》）
> 战前先算：道、天、地、将、法五事，与七个维度敌我对比——多算胜，少算不胜。

更多见 `data/figures/` 下各人物档案。

---

## 仓库结构

```
data/
  modes_data.json        核心资产：2868 条模式
  figure_names.json      人物名映射
  figures/               284 位人物档案（JSON + Markdown）
  intl_figures/          国际人物补充档案
tools/
  figure_library.py      查询工具（CLI + 可导入模块）
  thinking_mode_selector.py  场景选择器（含人物模式回退查询）
  json/                  场景与模式数据
api/                     FastAPI 服务（SQLite + 语义检索）
web/                     Vue 前端
docs/                    文档（快速入门/方法论/工具/训练/教练）
```

---

## 数据模型

```json
{
  "mode_code": "M-DKR-009",
  "figure_code": "H-DKR-001",
  "figure_name": "笛卡尔",
  "name_zh": "暂行道德准则法",
  "name_en": "Provisional Morality Method",
  "category": "伦理修养",
  "definition_zh": "知识地基拆除期间生活不能停摆……",
  "process_zh": ["识别处于'根基悬置期'的领域", "为该领域配备临时操作准则", "..."],
  "source_chapter": "《谈谈方法》第三部分",
  "key_quote_zh": "……",
  "representative_cases_zh": ["……"],
  "modern_applications_zh": ["……"]
}
```

---

## API（可选）

```bash
cd api
pip install -r requirements.txt
python load_v6.py        # 装载 2868 条模式进数据库
uvicorn api.main:app --reload
```

接口：`/api/v1/thinking-modes`、`/api/v1/thinking-modes/stats`、
`/api/v1/figures/{code}/modes`、`/api/v1/thinking-modes/{mode_code}`。

---

## 许可

MIT License — 见 [LICENSE](LICENSE)。

本项目收录的思想方法均为对公有领域历史文献与公开史实的整理与分析。
