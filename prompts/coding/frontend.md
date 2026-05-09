# 前端开发 Prompt

> 用于 React/Vue/HTML/CSS/JS 等前端开发任务

## 执行前确认

- 项目技术栈（React/Vue/原生）
- 组件粒度（原子/分子/页面）
- 样式方案（CSS/Tailwind/Styled Components）

## 执行规范

1. 组件结构：逻辑层（hooks）+ 视图层（JSX）+ 样式层分离
2. 状态管理：优先本地 state，需要时再引入全局状态
3. 性能：避免不必要的 re-render，使用 React.memo/useMemo 按需
4. 响应式：备选移动端适配方案

## 输出结构

- 组件代码（含中文注释）
- 使用示例
- 可复用的 hooks/工具函数标注「可存入 skills/」
