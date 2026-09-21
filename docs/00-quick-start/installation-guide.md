# Protreptic 安装和使用指南

> 这个项目不需要安装，不需要配置环境，打开就能用。
> 下面分两种情况：只是想读文档，和想让 AI 自动调用。

---

## 情况1：我只是想读文档

**零安装，30秒开始。**

### 方式A：在 GitHub 上直接看

1. 打开项目页面：`https://github.com/你的用户名/Protreptic`
2. 点击 `docs/00-quick-start/thinking_mode_quick_start.md`
3. 开始阅读

**优点**：不用下载，随时随地看
**缺点**：不能离线用

### 方式B：下载到本地看

```bash
# 1. 克隆项目
git clone https://github.com/你的用户名/Protreptic.git
cd Protreptic

# 2. 用任意 Markdown 阅读器打开 docs/ 目录
# 推荐工具：
#   - VS Code（免费）：code Protreptic/
#   - Typora（付费）：typora docs/
#   - Obsidian（免费）：打开 Protreptic/ 文件夹
#   - 浏览器：直接双击 docs/00-quick-start/thinking_mode_quick_start.md
```

**优点**：可以离线用，搜索更快
**缺点**：需要下载

---

## 情况2：我想让 AI 自动调用思维模式

这个项目的核心能力是 **78种思维模式**，但 AI 不会自动知道。你需要告诉它。

### 方法A：复制 System Prompt（最简单）

1. 打开 `docs/06-ai-collaboration/thinking_mode_agent_prompt.md`
2. 找到"完整 System Instruction"部分
3. 复制那段文字
4. 粘贴到你常用的 AI 工具的"自定义指令"或"System Prompt"设置里

**支持的 AI 工具**：

- ChatGPT → Settings → Custom Instructions → System Prompt
- Claude → System Prompt 设置
- Gemini → System Instructions
- 任何支持 System Prompt 的 AI 平台

**效果**：以后每次对话，AI 都会自动用思维模式分析你的问题

### 方法B：用对话模板（最灵活）

1. 打开 `docs/06-ai-collaboration/thinking_mode_ai_templates.md`
2. 选一个模板（比如 TM-01 问题诊断）
3. 复制"填空格式"部分
4. 填好空，发给任意 AI

**效果**：一次性获得结构化分析，不需要配置

### 方法C：让 AI 工具自动调用（高级用法）

如果你经常用同一个 AI 工具，可以把思维模式体系配置为"内置能力"。

**ChatGPT** → Settings → Custom Instructions → System Prompt → 粘贴 Agent Prompt
**Claude** → System Prompt 设置 → 粘贴 Agent Prompt
**Gemini** → System Instructions → 粘贴 Agent Prompt

效果：每次对话，AI 自动用思维模式分析你的问题。

---

## 常见问题

### Q: 我需要用 Python 吗？

**不需要。** 所有文档都是 Markdown 格式，任何文本编辑器都能打开。

### Q: 我需要用 Node.js 吗？

**不需要。** 没有前端，没有后端，纯文档。

### Q: 我需要数据库吗？

**不需要。** 所有数据都在 `.md` 文件里。

### Q: 更新后怎么同步？

```bash
cd Protreptic
git pull origin main
```

### Q: 我可以商用吗？

**可以。** 但要看你用的是哪一部分：

- **代码**（`web/`、`tools/`、`api/` 等）按 **MIT**：自由使用、修改、分发。
- **内容与数据**（`docs/` 文档与模式数据）按 **CC BY-SA 4.0**：同样可商用，但需**署名**并以**相同方式共享**。

适用范围见 [LICENSE](https://github.com/ovmobilegroup/protreptic/blob/main/LICENSE)
与 [LICENSE-CONTENT](https://github.com/ovmobilegroup/protreptic/blob/main/LICENSE-CONTENT)。

### Q: 我可以贡献吗？

可以。详见 [CONTRIBUTING.md](CONTRIBUTING.md)

---

## 快速参考

| 你想做什么 | 怎么做 | 需要装东西吗 |
|-----------|--------|------------|
| 读文档 | 打开 GitHub 或克隆到本地 | 不需要 |
| 让 AI 自动分析 | 复制 System Prompt 到 AI 设置 | 不需要 |
| 让 AI 一次性分析 | 复制对话模板发给 AI | 不需要 |
| 更新项目 | `git pull` | 不需要 |

---

*Protreptic — 引导人们走向智慧的劝勉*
