# 🧠 MYcline — 你的自进化个人 AI 架构

> 基于 Cline (.clinerules/.cline_memory) + DeepSeek-v4 的个人 AI 系统
> 融合 mem0/MemGPT/AutoGPT/LangGraph 等顶级开源项目的最佳实践

---

## 一、系统架构总览

```
MYcline/                           ← 你的桌面工作区
│
├── .clinerules/                   ← 【Cline 原生】工作区规则（自动加载所有 .md）
│   ├── 00-core-identity.md       ← 核心身份/技术栈定义
│   ├── 01-task-classification.md ← 任务分类系统（最重要的规则）
│   ├── 02-memory-protocol.md     ← 记忆读/写/检索协议
│   ├── 03-evolution-rules.md     ← 自进化触发规则
│   ├── 04-output-format.md       ← 输出规范
│   └── workflows/                ← 【Cline 原生】工作流目录
│       ├── new-task.md           ← /new-task 启动新任务
│       ├── search-memory.md      ← /search-memory 查询记忆
│       └── review-session.md     ← /review-session 会话总结
│
├── .cline_memory/                 ← 【核心】自进化记忆数据库
│   ├── self_evolve.md            ← AI 自主架构优化的规则引擎
│   ├── core_rules/               ← 高置信度知识规则
│   │   ├── identity.json         ← 你的身份画像（自动更新）
│   │   ├── tech-stack.json       ← 技术栈偏好
│   │   └── coding-standards.md   ← 代码规范沉淀
│   ├── memory_state.db           ← SQLite 状态跟踪表
│   ├── evolution_log/            ← 优化历史记录
│   │   └── YYYY-MM-DD-HHmmss.md
│   └── index/
│       ├── vector_index.json     ← 记忆向量索引
│       └── category_index.json   ← 分类索引
│
├── prompts/                       ← 【核心】Prompt 仓库（按分类）
│   ├── base_prompt.md            ← 基础系统提示
│   ├── coding/                   ← 编程类 prompt
│   │   ├── frontend.md
│   │   ├── backend.md
│   │   ├── debug.md
│   │   └── refactor.md
│   ├── writing/                  ← 写作类 prompt
│   │   ├── article.md
│   │   └── documentation.md
│   ├── analysis/                 ← 分析类 prompt
│   │   ├── code-review.md
│   │   └── image-analysis.md
│   ├── learning/                 ← 学习类 prompt
│   │   └── explain-concept.md
│   └── personal/                 ← 个人事务类（待扩充）
│
├── tasks/                         ← 每次任务的工作文件夹
│   └── YYYY-MM-DD_task-name/     ← 自动生成（含 prompt + 脚本 + 产出）
│       ├── task_prompt.md
│       ├── scripts/
│       └── output/
│
├── skills/                        ← 【可复用】脚本/Skill 库
│   └── skill-manifest.json       ← Skill 注册清单
│
└── mcp_config/                    ← MCP 服务器配置（可选，待创建）
    ├── mcp.json
    └── servers/
```

---

## 二、核心机制

### 2.1 任务分类系统（每次对话自动触发）

当你提出请求时，系统通过以下流程处理：

```
你的输入 "帮我写一个 React 组件"
       │
       ▼
┌─────────────────────────────────────┐
│  步骤 1: 任务分类                   │
│  ┌─────────────────────────────┐   │
│  │ 类别: coding/frontend       │   │
│  │ 子类: React 组件            │   │
│  │ 复杂度: 中等                │   │
│  └─────────────────────────────┘   │
├─────────────────────────────────────┤
│  步骤 2: 加载对应 prompt           │
│  → prompts/coding/frontend.md      │
│  → 合并历史相似任务上下文           │
├─────────────────────────────────────┤
│  步骤 3: 生成任务 prompt 给你审阅   │
│  → tasks/YYYY-MM-DD_xxx/task_prompt.md │
│  → 你确认后开始执行                 │
├─────────────────────────────────────┤
│  步骤 4: 执行过程中                 │
│  → 生成脚本 → 存入 skills/         │
│  → 记录关键决策 → 更新记忆         │
├─────────────────────────────────────┤
│  步骤 5: 任务结束                   │
│  → 更新 core_rules/                 │
│  → 写入 evolution_log/              │
│  → 更新 memory_state.db             │
└─────────────────────────────────────┘
```

### 2.2 记忆自进化机制

```
┌───────────────────┐
│  每轮对话结束后    │
└────────┬──────────┘
         ▼
┌──────────────────────────────────────────────┐
│  检查 self_evolve.md 中的触发条件              │
│                                              │
│  📊 memory_state.db 指标:                    │
│  ├─ 记忆冲突率 (conflict_rate)               │
│  ├─ 技能复用率 (skill_reuse_rate)            │
│  ├─ 上下文命中率 (context_hit_rate)          │
│  └─ 进化计数器 (evolution_count)             │
└──────────────────┬───────────────────────────┘
         ▼
┌──────────────────────────────────────────────┐
│  条件触发 → AI 自主执行优化                    │
│                                              │
│  冲突率 > 5%   → 重建记忆索引/去重合并        │
│  技能复用率 < 20% → 优化 skill 注册/模板      │
│  连续3天无新技能 → 从对话中挖掘潜在技能        │
│  上下文命中率 < 60% → 优化分类标签            │
│  每7天一次      → 执行完整记忆压缩/归档        │
└──────────────────┬───────────────────────────┘
         ▼
┌──────────────────────────────────────────────┐
│  执行结果                                    │
│  → 更新 memory_state.db                      │
│  → 生成 evolution_log/YYYY-MM-DD.md          │
│  → 输出优化摘要给你确认                       │
└──────────────────────────────────────────────┘
```

### 2.3 Cline Rules 协调方案

| 层级 | 位置 | 用途 | 管理方式 |
|------|------|------|---------|
| **全局 Rules** | `Documents\Cline\Rules\` | 所有项目通用的基础行为 | mycline-core.md 手动维护 |
| **工作区 Rules** | `MYcline/.clinerules/` | 本系统的核心规则（任务分类、记忆协议、进化规则） | 由 AI 和用户共同维护 |
| **工作流** | `MYcline/.clinerules/workflows/` | 可重复执行的自动化流程 | AI 自动编写更新 |
| **Prompt 仓库** | `MYcline/prompts/` | 分类后的任务 prompt 模板 | 用户/AI 持续扩充 |

**关键原则**：
- `.clinerules/` 中的规则是 Cline **每次对话自动加载**的，所以放最常用、最核心的行为指令
- `prompts/` 中的 prompt 是**按需加载**的，通过规则中的指令让 Cline 自己去读取
- 每次新任务，Cline 先通过 rules 知道「要怎么做」，再通过 prompts/ 知道「具体怎么做这个类别」

---

## 三、对话流程规范

### 每次请求的标准流程

1. **任务分类** → Cline 识别请求属于哪个类别
2. **Prompt 生成** → 加载对应分类 prompt + 合并历史记忆 → 生成 `task_prompt.md`
3. **用户确认** → 展示 prompt，你确认细节后开始执行
4. **执行与记录** → 执行过程中自动记录关键信息
5. **任务文件夹** → `tasks/YYYY-MM-DD_taskname/` 存放所有产出
6. **技能沉淀** → 可复用的脚本/方法存入 `skills/`
7. **记忆更新** → 更新 `core_rules/`、`memory_state.db`
8. **自我检视** → 检查是否需要触发自进化流程

### 工作流触发方式

| 命令 | 功能 |
|------|------|
| `/new-task` | 启动新任务（分类→生成 prompt→执行） |
| `/search-memory` | 搜索历史记忆/相似任务 |
| `/review-session` | 总结当前会话，更新记忆 |
| `/evolve-check` | 手动触发自进化检查 |
| `/show-stats` | 显示系统健康指标 |

---

## 四、与 mem0/MemGPT 等项目的借鉴融合

| 项目 | 借鉴点 | MYcline 实现 |
|------|--------|-------------|
| **mem0** | 向量嵌入检索 + 重要性评分 | `.cline_memory/index/vector_index.json` + 记忆评分机制 |
| **MemGPT/Letta** | 分层上下文管理（工作记忆↔归档） | 通过 `memory_state.db` 追踪上下文窗口用量，自动归档 |
| **AutoGPT** | JSON 记忆 + 技能沉淀 | `skills/` 目录 + `skill-manifest.json` |
| **LangGraph** | 检查点持久化 + 状态回溯 | `tasks/` 目录的记录 + `evolution_log/` 回溯 |
| **Hindsight** | 记忆升级协议 | 通过 `self_evolve.md` 的触发条件 + 回顾分析 |

---

## 五、实施路线图

### Phase 1: 基础骨架 ✅（已完成）
- [x] 创建 `.clinerules/` 核心规则集
- [x] 创建 `.cline_memory/` 自进化记忆骨架
- [x] 创建 `prompts/` 分类 prompt 仓库
- [x] 创建 `skills/` 技能库
- [x] 创建 `workflows/` 工作流
- [x] 配置全局 `Documents/Cline/Rules/mycline-core.md`

### Phase 2: 记忆系统激活
- [ ] 首次运行后填充 identity.json
- [ ] 积累足够对话后启用自进化
- [ ] 完善向量检索能力

### Phase 3: 深度优化
- [ ] 基于使用数据调优分类规则
- [ ] 自定义 MCP 服务器集成
- [ ] 性能监控和缓存策略优化

---

> **核心理念**: 系统不是一次性建成的，而是在使用中「生长」出来的。
> 每次对话都是一次学习机会，MYcline 自动记录、分类、优化。
