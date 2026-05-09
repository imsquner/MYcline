# 02 — PT100 温度采样板（主板）

> **核心芯片**: GD30AD3344（ADC）
> **功能**: 完成 PT100 温度信号的调理与数字化采集，通过 SPI 总线与外部 MCU 进行数据通信

## 设计目标

- [ ] PT100 信号调理电路设计（恒流源/电桥 + 放大）
- [ ] GD30AD3344 ADC 外围电路设计
- [ ] SPI 通信接口设计（与外部 MCU 连接）
- [ ] 模拟前端滤波/保护设计
- [ ] 精度与噪声分析
- [ ] 布局布线关键要点

## 参考资料

- `C:\Users\ziming\Desktop\cimc\GD30AD3344_Datasheet_Rev1.1.pdf`
- `C:\Users\ziming\Desktop\cimc\GD30AD3344_EVB用户指南_Rev.A.pdf`
- `C:\Users\ziming\Desktop\cimc\GD30AD3344_EVB_DemoSuites_ExtRef\`（参考设计）
- 赛题 PDF 采样板需求

## 状态

🟡 **设计阶段** — 待开始
