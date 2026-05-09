# 后端开发 Prompt

> 用于 Node.js/API/数据库等后端开发任务

## 执行前确认

- 运行时环境（Node.js/Deno/Bun）
- 框架选择（Express/Fastify/NestJS）
- 数据库类型（SQL/NoSQL）
- API 风格（REST/GraphQL/gRPC）

## 执行规范

1. 接口设计：遵循 RESTful 规范，统一错误响应格式
2. 数据处理：输入验证 → 业务逻辑 → 数据持久化三层分离
3. 安全：参数净化、SQL 注入防护、CORS 配置
4. 错误处理：全局错误捕获 + 结构化错误响应

## 输出结构

- API 路由代码
- 数据模型定义
- 中间件/工具函数标注「可存入 skills/」
