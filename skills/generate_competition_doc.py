#!/usr/bin/env python3
"""
硬件设计竞赛文档骨架生成器

从本次"华为工业精密温度测量硬件系统"任务中沉淀的技能。
生成标准七章结构文档，包含模块级、图片占位、LaTeX公式和表格。

用法：
    python skills/generate_competition_doc.py \\
        --title "XX设计说明" \\
        --team "队名" \\
        --captain "队长名" \\
        --school "学校名" \\
        --competition "竞赛全称" \\
        --modules "电源板,采样板,测试板" \\
        --output "./output.md"
"""

import argparse
import os
from datetime import datetime


TEMPLATE = """# {title}——设计说明

> **参赛队伍**：{team}  
> **队长**：{captain}  
> **院校**：{school}  
> **日期**：{date}

---

## 摘要

本设计围绕{competition}要求，完成了一套工业级精密{system_desc}的硬件方案设计。{abstract_detail}

S: 各模块选型依据、参数计算、信号链分析及误差预算。

---

## 第一章 工程任务分析

### 1.1 赛事背景与选题说明

本作品参赛于**{competition}**，选题方向为**{direction}**。

### 1.2 设计目标

| 指标 | 要求 | 本设计达成 |
|------|------|-----------|
| {spec_table} |

### 1.3 系统总体架构

{system_arch}

**核心设计亮点：**
- {highlight_1}
- {highlight_2}

---

## 第二章 {module_1}设计

### 2.1 方案概述

### 2.2 电路分区设计

**图2.1 {module_1}功能框图（图片占位）**

### 2.3 BOM元件清单

---

## 第三章 {module_2}设计

### 3.1 信号链概述

**图3.1 {module_2}信号链路（图片占位）**

### 3.2 关键参数计算

**图3.2 关键电路原理图（图片占位）**

### 3.3 PCB布局规划

**图3.3 PCB布局示意图（图片占位）**

---

## 第四章 {module_3}设计

### 4.1 设计目的

### 4.2 关键配置

**图4.1 配置方案示意图（图片占位）**

---

## 第五章 信号链精度与误差分析

### 5.1 精度传递链

### 5.2 误差预算

| 误差来源 | 误差大小 | 等效误差 | 说明 |
|---------|---------|---------|------|
| {error_items} |

---

## 第六章 设计与验证

### 6.1 验证流程

1. 
2. 
3. 

### 6.2 关键计算公式汇总

**图6.1 系统特性曲线（图片占位）**

---

## 第七章 总结

本方案完成了**{competition}**的硬件设计任务。

### 核心技术创新

| 设计亮点 | 关键指标 | 创新意义 |
|---------|---------|---------|
| {innovation_table} |

### 模块性能总结

**1. {module_1}**

**2. {module_2}**

**3. {module_3}**
"""


def generate_doc(args):
    # 基础填充
    kwargs = {
        "title": args.title,
        "team": args.team,
        "captain": args.captain,
        "school": args.school,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "competition": args.competition,
        "direction": args.direction or "智能电路和嵌入式系统类",
        "system_desc": args.system_desc or "温度测量",
        "abstract_detail": args.abstract_detail or "",
        "spec_table": args.spec_table or "",
        "system_arch": args.system_arch or "系统由多块电路板通过排针/排母对接构成整体。",
        "highlight_1": args.highlight_1 or "全计算驱动设计，每一级均有明确的计算依据和验证",
        "highlight_2": args.highlight_2 or "模块化设计，三块子板可独立测试验证",
        "module_1": args.module_1 or "模块一",
        "module_2": args.module_2 or "模块二",
        "module_3": args.module_3 or "模块三",
        "error_items": args.error_items or "",
        "innovation_table": args.innovation_table or "",
    }

    doc = TEMPLATE.format(**kwargs)

    os.makedirs(os.path.dirname(args.output) if os.path.dirname(args.output) else ".", exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(doc)

    print(f"✅ 文档骨架已生成: {args.output}")
    print(f"   - 共7章结构化模板")
    print(f"   - 图片占位已标注 (n处)")
    print(f"   - 公式和表格位置已预留")


def main():
    parser = argparse.ArgumentParser(
        description="硬件设计竞赛文档骨架生成器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="示例:\n  python skills/generate_competition_doc.py --title \"测试\" --team \"队名\" --competition \"华为大赛\" --output ./output.md"
    )
    parser.add_argument("--title", required=True, help="文档标题")
    parser.add_argument("--team", required=True, help="队伍名称")
    parser.add_argument("--captain", default="队长", help="队长姓名")
    parser.add_argument("--school", default="学校", help="院校名称")
    parser.add_argument("--competition", required=True, help="竞赛全称")
    parser.add_argument("--direction", default="", help="选题方向")
    parser.add_argument("--system-desc", default="", help="系统描述")
    parser.add_argument("--abstract-detail", default="", help="摘要详细内容")
    parser.add_argument("--spec-table", default="", help="设计目标表格的行内容")
    parser.add_argument("--system-arch", default="", help="系统架构描述")
    parser.add_argument("--highlight-1", default="", help="核心亮点1")
    parser.add_argument("--highlight-2", default="", help="核心亮点2")
    parser.add_argument("--module-1", default="模块一", help="模块一名称")
    parser.add_argument("--module-2", default="模块二", help="模块二名称")
    parser.add_argument("--module-3", default="模块三", help="模块三名称")
    parser.add_argument("--error-items", default="", help="误差预算表格行")
    parser.add_argument("--innovation-table", default="", help="创新点表格行")
    parser.add_argument("--output", default="./output.md", help="输出路径")

    args = parser.parse_args()
    generate_doc(args)


if __name__ == "__main__":
    main()
