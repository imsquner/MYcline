# /new-task — 启动新任务

此工作流用于启动一个标准化的新任务流程。

## 执行步骤

1. **分类用户请求**
   - 分析用户输入，确定主类别和子类
   - 参考 `01-task-classification.md` 的分类表

2. **加载分类 prompt**
   - 检查 `prompts/` 对应分类是否有 .md 文件
   - 如有多个相关子类，合并内容
   - 如无对应 prompt，创建新的

3. **查询历史记忆**
   - 读取 `.cline_memory/index/category_index.json`
   - 查找同分类历史任务，提取 2-3 条最相关上下文

4. **创建任务文件夹**
   - 格式：`tasks/YYYY-MM-DD_任务简述/`
   - 创建子目录：scripts/ logs/ output/

5. **生成 task_prompt.md**
   - 包含：任务标题、分类、用户需求重述、执行计划、待确认点、历史引用
   - 保存到任务文件夹

6. **向用户展示 prompt**
   - 等待用户确认或修改
   - 确认后开始执行
