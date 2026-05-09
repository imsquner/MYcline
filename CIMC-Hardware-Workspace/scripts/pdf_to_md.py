"""
PDF 转 Markdown 提取工具
用途：将 CIMC 原始资料中的 PDF 提取文本内容，转为 MD 格式存入参考资料目录
依赖：pip install pdfminer.six
"""

import os
import sys
from pdfminer.high_level import extract_text

# 源文件路径
SOURCE_DIR = r"C:\Users\ziming\Desktop\cimc"
# 输出目录（相对于本脚本）
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "参考资料")

# 需要转换的核心 PDF 文件列表
TARGET_FILES = {
    "GD30DC1354_Datasheet_Rev1.0.pdf": "GD30DC1354_Datasheet.md",
    "GD30AD3344_Datasheet_Rev1.1.pdf": "GD30AD3344_Datasheet.md",
    "GD30AD3344_EVB用户指南_Rev.A.pdf": "GD30AD3344_EVB用户指南.md",
    "GD32F470 Development Kit V2.0 原理图.pdf": "GD32F470_DevKit原理图.md",
}

def convert_pdf_to_md(pdf_path, md_path):
    """提取 PDF 文本并保存为 MD"""
    print(f"正在转换: {os.path.basename(pdf_path)}")
    try:
        text = extract_text(pdf_path)
        if not text.strip():
            print(f"  ⚠️  {os.path.basename(pdf_path)} 未能提取到文本内容（可能为纯图形PDF）")
            return False
        
        # 写入 MD 文件
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(f"# {os.path.basename(pdf_path).replace('.pdf','')}\n\n")
            f.write(f"> 来源: `{os.path.basename(pdf_path)}`\n")
            f.write(f"> 提取时间: 2026-05-07\n")
            f.write(f"> ⚠️ 注意: 文本由 PDF 自动提取，图表/公式可能丢失或错位\n\n")
            f.write("---\n\n")
            f.write(text)
        
        print(f"  ✅ 已保存: {md_path}")
        return True
    except Exception as e:
        print(f"  ❌ 转换失败: {e}")
        return False

def main():
    # 创建输出目录
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    success = 0
    failed = 0
    
    for pdf_name, md_name in TARGET_FILES.items():
        pdf_path = os.path.join(SOURCE_DIR, pdf_name)
        md_path = os.path.join(OUTPUT_DIR, md_name)
        
        if not os.path.exists(pdf_path):
            print(f"  ⚠️ 源文件不存在: {pdf_path}")
            failed += 1
            continue
        
        if convert_pdf_to_md(pdf_path, md_path):
            success += 1
        else:
            failed += 1
    
    print(f"\n完成: {success} 成功, {failed} 失败")

if __name__ == "__main__":
    main()
