"""批量提取 PDF 内容为 Markdown 文件"""
import os, sys, subprocess, json

def extract_text_from_pdf(pdf_path):
    """使用 pdftotext 或 python pdfplumber 提取 PDF 文本"""
    try:
        import pdfplumber
        text_parts = []
        with pdfplumber.open(pdf_path) as pdf:
            for i, page in enumerate(pdf.pages):
                text = page.extract_text()
                if text:
                    text_parts.append(f"--- 第 {i+1} 页 ---\n{text}")
        return "\n\n".join(text_parts)
    except ImportError:
        # 尝试 pdftotext
        try:
            result = subprocess.run(
                ["pdftotext", pdf_path, "-"],
                capture_output=True, text=True, timeout=30
            )
            return result.stdout
        except:
            return f"[无法提取: {pdf_path}]"

def extract_basic_info(pdf_path):
    """从文件名提取基本信息"""
    basename = os.path.basename(pdf_path)
    name, ext = os.path.splitext(basename)
    return {
        "source_file": basename,
        "title": name.replace("_", " ").replace("-", " "),
        "format": ext.lower()
    }

def convert_pdf_to_md(pdf_path, output_dir):
    """将单个 PDF 转换为 MD 文件"""
    info = extract_basic_info(pdf_path)
    md_filename = info["title"].replace(" ", "_") + ".md"
    md_path = os.path.join(output_dir, md_filename)
    
    # 跳过已存在的文件
    if os.path.exists(md_path):
        print(f"  ⏩ 已存在: {md_filename}")
        return md_path
    
    text = extract_text_from_pdf(pdf_path)
    
    if text.startswith("[无法提取"):
        print(f"  ⚠️  提取失败: {os.path.basename(pdf_path)}")
        return None
    
    # 写入 MD 文件
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(f"# {info['title']}\n\n")
        f.write(f"> 源文件: {info['source_file']}\n")
        f.write(f"> 提取时间: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
        f.write("---\n\n")
        f.write(text)
    
    print(f"  ✅ 已转换: {md_filename}")
    return md_path

def main():
    # 配置路径
    src_base = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "cimc")
    dst_base = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "CIMC-Hardware-Workspace", "docs")
    
    print("=" * 50)
    print("CIMC 资料 PDF -> MD 批量转换")
    print("=" * 50)
    
    # 1. PT100 资料
    pt100_src = os.path.join(src_base, "pt100")
    pt100_dst = os.path.join(dst_base, "datasheets")
    os.makedirs(pt100_dst, exist_ok=True)
    
    print(f"\n📁 处理 PT100 资料...")
    for f in sorted(os.listdir(pt100_src)):
        if f.lower().endswith('.pdf'):
            pdf_path = os.path.join(pt100_src, f)
            convert_pdf_to_md(pdf_path, pt100_dst)
    
    # 2. PCB 设计文档
    print(f"\n📁 处理 PCB 设计文档...")
    pcb_src = os.path.join(src_base, "PCB", "1电源板")
    pcb_dst = os.path.join(dst_base, "PCB")
    os.makedirs(pcb_dst, exist_ok=True)
    
    for root, dirs, files in os.walk(pcb_src):
        for f in files:
            if f.lower().endswith('.pdf'):
                pdf_path = os.path.join(root, f)
                rel_path = os.path.relpath(root, pcb_src)
                out_dir = os.path.join(pcb_dst, rel_path) if rel_path != '.' else pcb_dst
                os.makedirs(out_dir, exist_ok=True)
                convert_pdf_to_md(pdf_path, out_dir)
    
    # 3. 竞赛题目文档
    print(f"\n📁 处理竞赛题目文档...")
    comp_dst = os.path.join(dst_base, "competition")
    os.makedirs(comp_dst, exist_ok=True)
    
    for f in sorted(os.listdir(src_base)):
        if f.endswith('.pdf'):
            pdf_path = os.path.join(src_base, f)
            convert_pdf_to_md(pdf_path, comp_dst)
    
    # 4. GD30AD3344 资料
    print(f"\n📁 处理 GD30AD3344 资料...")
    gd_dst = os.path.join(dst_base, "datasheets")
    os.makedirs(gd_dst, exist_ok=True)
    
    for root, dirs, files in os.walk(src_base):
        for f in files:
            if f.lower().endswith('.pdf') and 'GD30' in f:
                pdf_path = os.path.join(root, f)
                convert_pdf_to_md(pdf_path, gd_dst)
    
    print("\n" + "=" * 50)
    print("转换完成！")
    print("=" * 50)

if __name__ == "__main__":
    main()
