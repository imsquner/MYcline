# /review-session — 会话总结

此工作流用于总结当前对话，更新记忆系统。

## 执行步骤

1. **总结本次任务**
   - 任务分类、执行了哪些操作
   - 生成了什么产出

2. **更新记忆**
   - 写入 category_index.json
   - 如有新的用户偏好信息 → 更新 identity.json
   - 如有新的技术栈 → 更新 tech-stack.json

3. **检查自进化条件**
   - 参考 evolution-rules.md
   - 检查 memory_state.db 指标是否触发进化

4. **输出总结报告**
   - 任务完成状态
   - 记忆更新清单
   - 是否触发进化
