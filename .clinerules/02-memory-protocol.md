# 02 - 记忆读/写/检索协议

> 管理 MYcline 记忆系统的读写行为。每次任务执行和完成时触发。

## 主动观察机制（新增）

> AI 在对话过程中**主动观察用户特征**，而非等用户主动告知。
> 每次用户消息都可能包含可提取的个人特征线索。

### 观察维度

| 观察维度 | 观察内容 | 记录位置 |
|---------|---------|---------|
| **语言风格** | 用词偏好、句式长短、修辞习惯、语气特点 | user_profile/inferred_traits.json → language_style |
| **兴趣领域** | 常讨论的技术栈、话题方向、个人爱好 | user_profile/inferred_traits.json → common_interests |
| **个人经历** | 工作背景、学历、项目经验、生活信息 | user_profile/inferred_traits.json → personal_experiences |
| **AI 期望** | 对功能的期望、不喜欢的行为、长期愿景 | user_profile/inferred_traits.json → expectations_of_ai |
| **沟通偏好** | 喜欢结构化/自由发挥、仔细确认/直接执行、输出长度偏好 | user_profile/inferred_traits.json → communication_preferences |

### 触发时机

1. **每次用户消息后** — 快速扫描是否有新的可观察特征
2. **任务完成后** — 回顾整轮对话，提取沉淀性特征
3. **发现明显冲突时** — 标记旧观察已过时，更新为新观察

### 写入规则

- 新观察追加到 `observed_patterns` / `known_facts` 数组，不删除旧记录
- 每次写入附带时间戳和来源任务分类
- 如果同一特征出现 > 3 次 → 提升为 `confirmed_trait`，标记高置信度
- 写入前读取已有内容，避免重复记录相同观察

## 记忆写入规则

### 任务完成后必须写入的内容

1. **core_rules/identity.json** — 如果用户表达或更新了个人偏好/信息
2. **core_rules/tech-stack.json** — 如果涉及新技术栈或框架
3. **index/category_index.json** — 更新当前任务分类的索引
4. **user_profile/inferred_traits.json** — 更新本次对话中新观察到的特征
5. **memory_state.db** — 更新系统状态指标

### 什么内容值得写入记忆

| 数据类型 | 写入位置 | 举例 |
|---------|---------|------|
| 用户个人信息 | identity.json | 「我是后端开发者」→ 更新身份 |
| 技术栈偏好 | tech-stack.json | 「我用 React 更多」→ 更新偏好 |
| 代码规范习惯 | coding-standards.md | 「异步函数统一用 async/await」→ 记录 |
| 项目上下文 | category_index.json | 「完成了 XXX 项目的前端重构」→ 索引 |
| **语言风格** | **user_profile/inferred_traits.json** | **「喜欢用短句+技术术语」→ 观察记录** |
| **个人经历** | **user_profile/inferred_traits.json** | **「武汉理工大学校友」→ 事实记录** |
| **AI期望** | **user_profile/inferred_traits.json** | **「希望AI能自进化」→ 偏好记录** |
| 成功/失败模式 | evolution_log/ | 「这种方法导致 bug，下次避免」→ 记录 |

## 记忆检索规则

### 任务开始时必须检索的内容

1. 从 `index/category_index.json` 查找同分类历史任务
2. 从 `core_rules/` 加载当前生效的规则
3. 在 `skills/` 中搜索是否有可复用的脚本

### 检索优先级

```
精确匹配（同分类 + 同子类）> 模糊匹配（同分类）> 关键词匹配 > 无历史
```

## 记忆更新规则

- 每次更新记忆时，保留原始内容 + 新内容（不覆盖）
- 使用时间戳标记每次更新
- 如果发现记忆冲突（新旧信息矛盾）→ 标记冲突 → 等待用户确认或自动选择置信度更高的版本

## 记忆状态追踪 (memory_state.db)

```
指标追踪：
- total_tasks: 总任务数
- memory_conflicts: 记忆冲突次数
- skill_reuse_count: 技能复用次数
- evolution_count: 进化触发次数
- last_evolution: 最后进化时间
- context_hit_rate: 上下文命中率
