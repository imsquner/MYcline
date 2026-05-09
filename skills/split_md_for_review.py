#!/usr/bin/env python3
"""
split_md_for_review.py — 大文件分批处理工具

作用：将大 md 文件按章节/行数切分为小块，
      每次只处理一块，防止上下文窗口过大导致中断。
      每处理完一块自动输出进度，可随时中断继续。

用法：
  1. 首次：切分大文件
     python skills/split_md_for_review.py split <大文件路径> [--lines 每块行数]
       → 默认每块 80 行，输出到 <文件名_parts/> 目录

  2. 逐个核对：按顺序读取每块
     python skills/split_md_for_review.py next <大文件路径>
       → 显示下一块未处理的内容 + 进度

  3. 标记某块已核对
     python skills/split_md_for_review.py done <大文件路径> <块号>
       → 在 <文件名_parts/> 目录中标记该块为已核对

  4. 查看总进度
     python skills/split_md_for_review.py status <大文件路径>
"""

import sys
import os
import json
from pathlib import Path

DEFAULT_LINES = 80

def get_parts_dir(filepath):
    base = Path(filepath).stem
    parent = Path(filepath).parent
    parts_dir = parent / f"{base}_parts"
    return parts_dir

def split_file(filepath, lines_per_block=DEFAULT_LINES):
    parts_dir = get_parts_dir(filepath)
    parts_dir.mkdir(exist_ok=True)

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 按行切分
    all_lines = content.splitlines(keepends=True)
    total_lines = len(all_lines)

    # 清理旧的分块
    for old in parts_dir.glob("block_*.md"):
        old.unlink()
    if (parts_dir / "progress.json").exists():
        (parts_dir / "progress.json").unlink()

    block_count = 0
    for i in range(0, total_lines, lines_per_block):
        block_lines = all_lines[i:i+lines_per_block]
        block_num = block_count + 1
        block_file = parts_dir / f"block_{block_num:03d}.md"
        with open(block_file, 'w', encoding='utf-8') as f:
            f.writelines(block_lines)
        block_count += 1

    # 写入进度文件
    progress = {
        "total_blocks": block_count,
        "total_lines": total_lines,
        "current_block": 1,
        "done_blocks": [],
        "last_partial": False
    }
    # 检查最后一块是否太小（< lines_per_block 的 1/3）
    last_block_lines = total_lines % lines_per_block
    if last_block_lines > 0 and last_block_lines < lines_per_block / 3:
        progress["last_partial"] = True

    with open(parts_dir / "progress.json", 'w', encoding='utf-8') as f:
        json.dump(progress, f, ensure_ascii=False, indent=2)

    print(f"✅ 切分完成：{filepath}")
    print(f"   共 {total_lines} 行 → {block_count} 块")
    print(f"   每块约 {lines_per_block} 行")
    print(f"   分块目录：{parts_dir}")
    return block_count

def get_progress(filepath):
    parts_dir = get_parts_dir(filepath)
    progress_file = parts_dir / "progress.json"
    if not progress_file.exists():
        print("❌ 未找到进度文件，请先运行 split")
        return None
    with open(progress_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_progress(filepath, progress):
    parts_dir = get_parts_dir(filepath)
    with open(parts_dir / "progress.json", 'w', encoding='utf-8') as f:
        json.dump(progress, f, ensure_ascii=False, indent=2)

def show_next_block(filepath):
    progress = get_progress(filepath)
    if not progress:
        return

    total = progress["total_blocks"]
    current = progress["current_block"]
    done = set(progress["done_blocks"])

    # 找到下一个未处理的块
    while current <= total and current in done:
        current += 1

    if current > total:
        print("🎉 所有块已处理完毕！")
        return

    parts_dir = get_parts_dir(filepath)
    block_file = parts_dir / f"block_{current:03d}.md"
    if not block_file.exists():
        print(f"❌ 块文件不存在：{block_file}")
        return

    print(f"\n{'='*60}")
    print(f"📖 第 {current}/{total} 块（已核对 {len(done)} 块）")
    print(f"{'='*60}\n")
    with open(block_file, 'r', encoding='utf-8') as f:
        print(f.read())
    print(f"\n{'='*60}")
    print(f"📖 第 {current}/{total} 块结束，进度 {len(done)}/{total}")
    print(f"{'='*60}")

    # 更新 current_block 为当前显示块
    progress["current_block"] = current
    save_progress(filepath, progress)

def mark_done(filepath, block_num):
    progress = get_progress(filepath)
    if not progress:
        return

    block_num = int(block_num)
    if block_num not in progress["done_blocks"]:
        progress["done_blocks"].append(block_num)
        progress["done_blocks"].sort()

    # 自动推进 current_block
    total = progress["total_blocks"]
    next_block = block_num + 1
    while next_block <= total and next_block in progress["done_blocks"]:
        next_block += 1
    progress["current_block"] = next_block

    save_progress(filepath, progress)

    done_count = len(progress["done_blocks"])
    total_count = progress["total_blocks"]
    pct = round(done_count / total_count * 100, 1)
    print(f"✅ 第 {block_num} 块已标记为已核对")
    print(f"   进度：{done_count}/{total_count} = {pct}%")
    if next_block <= total:
        print(f"   下一块：第 {next_block} 块（运行 next 查看）")
    else:
        print(f"🎉 全部完成！")

def show_status(filepath):
    progress = get_progress(filepath)
    if not progress:
        return

    total = progress["total_blocks"]
    done = progress["done_blocks"]
    current = progress["current_block"]
    pct = round(len(done) / total * 100, 1)

    print(f"\n{'='*60}")
    print(f"📊 处理进度报告")
    print(f"{'='*60}")
    print(f"   总块数：{total}")
    print(f"   已核对：{len(done)}")
    print(f"   当前块：{current}")
    print(f"   完成率：{pct}%")
    print(f"   未完成：{total - len(done)} 块")

    # 显示每块状态
    print(f"\n   块状态：")
    for i in range(1, total + 1):
        marker = "✅" if i in done else "⬜"
        current_marker = " ← 当前" if i == current else ""
        print(f"      {marker} 第 {i:03d} 块{current_marker}")

    if len(done) == total:
        print(f"\n🎉 全部处理完毕！")
    else:
        next_undone = current
        while next_undone <= total and next_undone in done:
            next_undone += 1
        if next_undone <= total:
            print(f"\n   下一步：运行 next 查看第 {next_undone} 块")
    print(f"{'='*60}\n")

def print_usage():
    print("""用法：
  # 1. 首次：切分大文件
  python skills/split_md_for_review.py split <文件路径> [--lines 行数]
    例：python skills/split_md_for_review.py split tasks/xxx/output/大文件.md --lines 80

  # 2. 查看下一块
  python skills/split_md_for_review.py next <文件路径>

  # 3. 标记某块已核对
  python skills/split_md_for_review.py done <文件路径> <块号>

  # 4. 查看总进度
  python skills/split_md_for_review.py status <文件路径>
""")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print_usage()
        sys.exit(1)

    command = sys.argv[1]
    filepath = sys.argv[2]

    if not os.path.exists(filepath):
        print(f"❌ 文件不存在：{filepath}")
        sys.exit(1)

    if command == "split":
        lines = DEFAULT_LINES
        if "--lines" in sys.argv:
            idx = sys.argv.index("--lines")
            if idx + 1 < len(sys.argv):
                lines = int(sys.argv[idx + 1])
        split_file(filepath, lines)

    elif command == "next":
        show_next_block(filepath)

    elif command == "done":
        if len(sys.argv) < 4:
            print("❌ 请指定块号：done <文件> <块号>")
            sys.exit(1)
        mark_done(filepath, sys.argv[3])

    elif command == "status":
        show_status(filepath)

    else:
        print(f"❌ 未知命令：{command}")
        print_usage()
