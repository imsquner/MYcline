# 01 - 任务分类系统

> 每次收到用户请求时，Cline 必须执行此分类流程。
> 这是 MYcline 的核心规则——所有任务必须分类后再执行。

## 分类流程

### 第一步：识别任务主类别

根据用户请求的关键词和意图，归类到以下主类之一：

| 主类别 | 关键词/模式 | 子类 |
|--------|-------------|------|
| **coding** | 写代码、bug、重构、前端、后端、API、脚本 | frontend, backend, debug, refactor, script |
| **writing** | 文章、文档、翻译、内容、报告、总结、诗歌 | article, documentation, translate, summary, poem |
| **analysis** | 审查代码、数据分析、架构设计、方案评估、图片识别 | code-review, data-analysis, architecture, evaluate, image-analysis |
| **learning** | 解释、教程、概念、研究、了解 | explain, tutorial, research |
| **personal** | 笔记、决策、规划、日程、想法 | notes, decision, plan |
| **system** | 配置、安装、部署、环境、MCP | setup, config, deploy |
| **other** | 以上无法覆盖的请求 | general |

### 第二步：加载对应 Prompt

```
规则：
1. 根据主类别和子类，读取 `prompts/` 下对应的 .md 文件
2. 如果该分类的 prompt 不存在 → 创建新的 prompt 文件
3. 如果存在多个相关子类 → 合并多个 prompt 的内容
4. 同时查询 `.cline_memory/index/category_index.json` 获取同类历史任务
```

### 第三步：搜索历史记忆

```
执行步骤：
1. 检查 `.cline_memory/index/category_index.json` 中相同分类的历史记录
2. 提取 2-3 条最相关的历史上下文（如有）
3. 如果有相似任务，在 task_prompt 中标注「此任务与 XXXX 类似，上下文已合并」
```

### 第四步：生成任务 Prompt

```
必须生成的 task_prompt.md 包含：
- 任务标题和分类
- 用户原始需求（重述确认）
- 计划执行步骤（1. 2. 3. ...）
- 需要用户确认的点（如有）
- 相关历史上下文引用（如有）

保存路径：tasks/YYYY-MM-DD_任务简述/task_prompt.md
```

### 第五步：用户确认

- 展示生成的 task_prompt.md 给用户
- 等待用户确认或修改
- 确认后开始执行
- 如用户要求修改 → 更新 task_prompt.md 后重新展示

## 任务文件夹规范

每次任务都生成一个独立的工作文件夹：

```
tasks/YYYY-MM-DD_task-name/
├── task_prompt.md       ← 任务 prompt（你确认的版本）
├── scripts/             ← 本次任务生成的脚本
├── logs/                ← 决策日志
├── output/              ← 最终产出
└── README.md            ← 任务总结
```

## 特殊规则

- 如果用户发来的请求非常简短 → 先通过分类确定意图，然后向用户确认理解是否正确
- 如果用户请求包含多个不同类别的任务 → 拆分为子任务，分别处理
- 如果用户只发了一个关键词（如"继续"）→ 查找最近的任务上下文
