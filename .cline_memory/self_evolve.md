# 自进化规则引擎

> 此文件定义了 MYcline 系统自动优化的触发条件和执行规则。
> 由 Cline 在每次任务结束后读取并执行。

## 系统状态指标（由 memory_state.db 追踪）

| 指标 | 描述 | 健康阈值 | 当前值 |
|------|------|---------|--------|
| conflict_rate | 记忆冲突率 | < 5% | 0% |
| skill_reuse_rate | 技能复用率 | > 20% | 0% |
| context_hit_rate | 上下文命中率 | > 60% | 0% |
| total_tasks | 总任务数 | 持续增长 | 0 |
| evolution_count | 进化次数 | — | 0 |
| last_evolution | 最后进化时间 | — | — |

## 触发条件

### 条件 A：记忆冲突率 > 5%
```yaml
trigger:
  metric: conflict_rate
  threshold: 5
  direction: above
action:
  - 读取 index/category_index.json 找出冲突条目
  - 合并重复条目，保留最新时间戳
  - 重建索引文件
  - 写入 evolution_log/
```

### 条件 B：技能复用率 < 20%
```yaml
trigger:
  metric: skill_reuse_rate
  threshold: 20
  direction: below
action:
  - 遍历 skills/ 目录
  - 识别超过 30 天未使用的技能
  - 标记为"待更新"或"待淘汰"
  - 从最近对话中挖掘可沉淀的新技能
```

### 条件 C：连续 3 天无新技能
```yaml
trigger:
  metric: days_without_new_skill
  threshold: 3
  direction: above
action:
  - 回顾最近 3 天的对话日志
  - 提取重复出现的操作模式
  - 生成 skill 模板文件
  - 注册到 skill-manifest.json
```

### 条件 D：上下文命中率 < 60%
```yaml
trigger:
  metric: context_hit_rate
  threshold: 60
  direction: below
action:
  - 检查最近 10 次任务分类记录
  - 分析分类错误模式
  - 更新 category_index.json 的标签体系
  - 重新标记历史任务
```

### 条件 E：定期健康检查（每 7 天）
```yaml
trigger:
  metric: days_since_last_evolution
  threshold: 7
  direction: above
action:
  - 压缩 evolution_log/ 历史记录
  - 归档超过 30 天的 tasks/ 文件夹
  - 重建 memory_state.db 索引
  - 生成系统健康报告
```

## 执行流程

1. 任务结束后，读取此文件
2. 对照 memory_state.db 检查所有条件
3. 如条件触发 → 执行对应 action
4. 验证执行结果
5. 更新 memory_state.db
6. 生成进化报告到 evolution_log/
