# 🧠 MYcline — 自进化个人 AI 系统

> **让你的 Cline 越用越懂你，越用越强大**
>
> 一套开箱即用的自进化架构，基于 VS Code + Cline + DeepSeek-v4 构建。
> 每次对话都是系统自我完善的机会。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
![Platform: VS Code](https://img.shields.io/badge/Platform-VS%20Code-blue)
![Model: DeepSeek](https://img.shields.io/badge/Model-DeepSeek--v4--flash-green)
![Status: Active](https://img.shields.io/badge/Status-Active-brightgreen)

---

## 📖 目录

- [为什么需要 MYcline？](#-为什么需要-mycline)
- [核心特性](#-核心特性)
- [快速开始](#-快速开始)
- [架构总览](#-架构总览)
- [核心机制详解](#-核心机制详解)
  - [1. 任务分类系统](#1-任务分类系统)
  - [2. Prompt 仓库](#2-prompt-仓库)
  - [3. 自进化记忆](#3-自进化记忆)
  - [4. 技能沉淀](#4-技能沉淀)
  - [5. 工作流系统](#5-工作流系统)
- [定制你的系统](#-定制你的系统)
- [设计理念](#-设计理念)
- [参考与致谢](#-参考与致谢)
- [许可证](#-许可证)

---

## 🤔 为什么需要 MYcline？

### 痛点

**Cline 原生虽强，但每次对话都是「空杯心态」:**

| 问题 | 表现 |
|------|------|
| ❌ **无记忆** | 每次都要重新描述项目背景、技术栈偏好 |
| ❌ **无分类** | 不管写代码、写文档还是做分析，都用同一套提示 |
| ❌ **无进化** | 犯过的错误下次还会再犯，没有「教训沉淀」 |
| ❌ **无复用** | 写过的脚本、工具方法散落在对话历史里，再也找不到 |
| ❌ **无结构** | 项目文件混乱，不同任务的产出混在一起 |

### MYcline 的解法

| 问题 | MYcline 方案 |
|------|-------------|
| ✅ **有记忆** | `.cline_memory/` 自动记录身份、技术栈、历史任务 |
| ✅ **有分类** | 每次请求先分类→加载对应 prompt→精准执行 |
| ✅ **有进化** | 每次任务结束后检查冲突率、复用率，自主优化 |
| ✅ **有沉淀** | 可复用的脚本自动存入 `skills/` |
| ✅ **有结构** | 每次任务生成独立文件夹，清晰可追溯 |

---

## ✨ 核心特性

### 🔄 全自动任务分类

```
你说："帮我写个 React 组件"
系统自动识别 → coding/frontend
加载对应 prompt → 按前端规范执行
```

无需手动指定类别，系统根据请求内容自动归类。

### 🧩 分类 Prompt 仓库

```
prompts/
├── coding/         编程类（前端/后端/调试/重构）
├── writing/        写作类（文章/文档）
├── analysis/       分析类（代码审查/图片识别）
├── learning/       学习类（概念解释）
└── personal/       个人事务（待扩充）
```

每个分类有专属的执行规范，输出格式统一。

### 🧠 自进化记忆系统

- **动态身份画像**：`identity.json` 随着使用自动更新
- **技术栈偏好**：`tech-stack.json` 记录你常用的框架和工具
- **历史任务索引**：`category_index.json` 按分类记录所有任务
- **自优化规则**：`self_evolve.md` 定义触发条件，AI 自主执行优化

### 📦 技能沉淀机制

执行过程中生成的脚本和方法，可一键注册到 `skills/` 库，下次直接复用。

### ⚙️ 清晰的工作流

| 命令 | 功能 |
|------|------|
| `/new-task` | 启动新任务 |
| `/search-memory` | 搜索历史记忆 |
| `/review-session` | 总结对话，更新记忆 |
| `/evolve-check` | 手动触发自进化检查 |
| `/show-stats` | 显示系统健康指标 |

---

## 🚀 快速开始

### 前置条件

- **VS Code** + [Cline 插件](https://marketplace.visualstudio.com/items?itemName=saoudrizwan.claude-dev) 已安装
- **DeepSeek-v4-flash** API Key 已配置（或其他兼容模型）
- **Git** 已安装（用于后续版本管理）

### 第一步：克隆项目

```bash
git clone https://github.com/你的用户名/MYcline.git
cd MYcline
```

> 也可以直接下载 ZIP 包解压到桌面。

### 第二步：配置全局规则

创建文件 `C:\Users\你的用户名\Documents\Cline\Rules\mycline-core.md`：

```markdown
# MYcline 核心系统规则

> MYcline 是自进化个人 AI 系统的主工作区。

## 核心行为
1. 任务开始前：先分类 → 加载对应 prompt → 生成 task_prompt.md 给用户确认
2. 任务结束后：记录产出 → 更新记忆 → 检查是否需要自进化
3. 可复用脚本 → 存入 skills/ 并注册到 skill-manifest.json
4. 关键决策 → 记录到 tasks/当前任务/ 的日志中
5. 优先使用 .cline_memory/ 中的历史信息辅助决策
6. 对话简洁、专业，避免多余的社交性用语
```

### 第三步：填写个人信息

复制模板文件，填入你的信息：

```bash
# 复制身份模板
cp .cline_memory/core_rules/__identity_template.json .cline_memory/core_rules/identity.json

# 复制技术栈模板
cp .cline_memory/core_rules/__tech-stack_template.json .cline_memory/core_rules/tech-stack.json

# 复制分类索引模板
cp .cline_memory/index/__category_index_template.json .cline_memory/index/category_index.json
```

在 `identity.json` 中填写：

```json
{
  "name": "你的名字",
  "alias": "你的昵称",
  "role": "你的角色",
  "system_version": "MYcline v1.0",
  "base_model": "DeepSeek-v4-flash",
  "platform": "Cline 中文版 (VS Code)",
  "preferences": {
    "language": "zh-CN",
    "code_style": "clean, modular",
    "comment_language": "中文"
  }
}
```

### 第四步：重启 VS Code

Cline 会自动加载 `.clinerules/` 中的所有规则文件以及全局的 `mycline-core.md`。

### 第五步：开始使用

你现在可以直接在 Cline 中提问了。系统会自动分类、加载 prompt、生成 task_prompt 供你确认。

---

## 🏗 架构总览

```
MYcline/
│
├── .clinerules/                   ← 【Cline 原生】工作区规则（自动加载）
│   ├── 00-core-identity.md       ← 核心身份定义
│   ├── 01-task-classification.md ← 任务分类系统
│   ├── 02-memory-protocol.md     ← 记忆读写协议
│   ├── 03-evolution-rules.md     ← 自进化触发规则
│   ├── 04-output-format.md       ← 输出规范
│   └── workflows/                ← 工作流（/new-task, /search-memory...）
│
├── .cline_memory/                 ← 【核心】自进化记忆系统
│   ├── self_evolve.md            ← AI 自主优化规则引擎
│   ├── core_rules/               ← 高置信度知识（身份/技术栈/代码规范）
│   ├── evolution_log/            ← 优化历史记录
│   └── index/                    ← 分类索引 + 向量索引
│
├── prompts/                       ← 【核心】分类 Prompt 仓库
│   ├── coding/                   ← 编程类（前端/后端/调试/重构）
│   ├── writing/                  ← 写作类（文章/文档）
│   ├── analysis/                 ← 分析类（代码审查/图片识别）
│   ├── learning/                 ← 学习类（概念解释）
│   └── personal/                 ← 个人事务类
│
├── tasks/                         ← 每次任务的工作文件夹
├── skills/                        ← 可复用脚本库
├── mcp_config/                    ← MCP 服务器配置（可选）
│
├── MYCLINE_ARCHITECTURE.md        ← 完整架构文档
├── README.md                      ← 本文件
└── .gitignore                     ← 隐私文件排除规则
```

---

## 🔧 核心机制详解

### 1. 任务分类系统

每次对话自动执行以下流程：

```
你的输入 → 分类识别 → 加载 Prompt → 查询记忆
               ↓
         生成 task_prompt.md → 你确认 → 执行
               ↓
         更新记忆 + 检查自进化
```

**分类规则**（定义在 `01-task-classification.md`）：

| 主类别 | 关键词 | 子类 |
|--------|--------|------|
| coding | 写代码、bug、重构、前端、后端 | frontend, backend, debug, refactor |
| writing | 文章、文档、翻译、报告 | article, documentation, translate |
| analysis | 审查代码、数据分析、图片识别 | code-review, data-analysis, image-analysis |
| learning | 解释、教程、概念、研究 | explain, tutorial, research |
| personal | 笔记、决策、规划 | notes, decision, plan |
| system | 配置、安装、部署 | setup, config, deploy |

### 2. Prompt 仓库

每个分类的 prompt 文件包含：

- **执行前确认清单**：需要你提供哪些信息
- **执行规范**：具体的操作步骤和标准
- **输出结构**：最终交付的格式要求

示例——`prompts/coding/frontend.md` 部分内容：

```markdown
# 前端开发 Prompt

## 执行前确认
- 框架选择（React/Vue/其他）
- 组件类型（页面/通用组件/工具函数）
- 样式方案（CSS/Tailwind/Styled-components）

## 执行规范
1. 组件使用函数式 + Hooks
2. Props 使用 TypeScript 接口定义
3. 样式优先使用 Tailwind 工具类
...
```

### 3. 自进化记忆

**数据流**：

```
每轮对话
    │
    ▼
┌─────────────────────────────┐
│ 检查 self_evolve.md 条件    │
│                             │
│ 冲突率 > 5% → 重建索引      │
│ 复用率 < 20% → 优化技能     │
│ 连续3天无新技能 → 挖掘沉淀   │
│ 每7天 → 完整健康检查        │
└─────────────────────────────┘
```

**触发条件表**：

| 条件 | 阈值 | 动作 | 来源 |
|------|------|------|------|
| 记忆冲突率 | > 5% | 重建索引，去重合并 | memory_state.db |
| 技能复用率 | < 20% | 检查并更新 skills/ | memory_state.db |
| 无新技能天数 | >= 3 | 从对话历史挖掘新技能 | 文件时间戳 |
| 上下文命中率 | < 60% | 优化分类标签体系 | memory_state.db |
| 距上次进化 | >= 7天 | 完整记忆压缩+健康报告 | memory_state.db |
| 用户主动触发 | /evolve-check | 立即执行全部检查 | 用户输入 |

### 4. 技能沉淀

当你在某个任务中写了一个可复用的脚本或工具方法，系统会：

1. 将其存入 `skills/` 目录
2. 注册到 `skill-manifest.json`
3. 后续相似任务自动提示可复用

### 5. 工作流系统

通过 Cline 输入框输入命令触发：

**`/new-task`**
```
启动新任务流程：
1. 分类识别 → 2. 加载 prompt → 3. 生成 task_prompt
→ 4. 你确认 → 5. 执行 → 6. 更新记忆
```

**`/search-memory`**
```
搜索历史记忆：
1. 读取 category_index.json
2. 按分类/关键词匹配合适的历史任务
```

**`/review-session`**
```
总结当前会话：
1. 汇总本次对话的关键信息
2. 更新 identity.json / tech-stack.json 中的偏好
3. 写入 evolution_log/
```

---

## 🎨 定制你的系统

### 添加新分类的 Prompt

如果你想添加一个系统目前没有的分类（如 `writing/translate.md`）：

1. 在对应目录下创建 `.md` 文件
2. 更新 `01-task-classification.md` 的分类表
3. 重启 VS Code 使其生效

### 修改输出风格

编辑 `04-output-format.md` 即可调整 Cline 的回复风格，所有对话自动生效。

### 添加自定义工作流

在 `.clinerules/workflows/` 下创建新的 `.md` 文件即可注册新的命令。

### 集成 MCP 服务器

如果需要连接外部 API，在 `mcp_config/` 下配置 MCP 服务器，Cline 会自动加载。

---

## 💡 设计理念

### 系统不是建成的，是长出来的

MYcline 的核心哲学：**不要一次性设计一个完美的系统，而是让系统在使用中自我完善。**

- **最小化初始设计**：只搭建骨架（规则+目录+模板）
- **最大化使用积累**：真正的价值来自每次对话的数据沉淀
- **自动化优化**：AI 自主检测问题并修复，无需人工干预

### 借鉴但非复制

MYcline 参考了以下开源项目的设计理念：

| 项目 | 启发点 |
|------|--------|
| **mem0** | 向量嵌入检索 + 记忆重要性评分 |
| **MemGPT/Letta** | 分层上下文管理（工作记忆↔长期记忆） |
| **AutoGPT** | JSON 记忆 + 技能沉淀机制 |
| **LangGraph** | 检查点持久化 + 状态回溯 |
| **EverMemOS** | 事件链聚合 + 日志压缩 |

**不同之处**：MYcline 完全基于 Cline 的 `.clinerules` 和 `.cline_memory` 原生机制实现，不需要额外安装 Python 包或运行独立的服务进程。它是对 Cline 能力的**增强**，而非替代。

---

## 📝 参考与致谢

- [Cline](https://github.com/cline/cline) — VS Code 上的 AI 编程助手
- [DeepSeek](https://deepseek.com/) — 强大的中文大语言模型
- [mem0](https://github.com/mem0ai/mem0) — 记忆层设计参考
- [MemGPT/Letta](https://github.com/letta-ai/letta) — 分层记忆管理
- [AutoGPT](https://github.com/Significant-Gravitas/AutoGPT) — 技能沉淀机制
- [LangGraph](https://github.com/langchain-ai/langgraph) — 状态管理设计

---

## 📄 许可证

本项目基于 MIT 许可证开源。详见 [LICENSE](LICENSE) 文件。

---

> **用 MYcline，让你的 Cline 从「对话工具」进化为「个人 AI 伙伴」。**
>
> 如果你觉得这个项目有帮助，欢迎 ⭐ Star 和 Fork！
