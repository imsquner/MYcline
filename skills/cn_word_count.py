#!/usr/bin/env python3
"""MYcline 中文纯字数统计工具
使用方法: python cn_word_count.py <文件路径>
统计规则: 只统计纯汉字(\u4e00-\u9fff), 不包含标点、英文字母、数字、格式标记
比赛/文章字数标准通常以此为准。
"""
import re
import sys

def count_cn_chars(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    # 去掉标题行
    content = re.sub(r'^#.*\n', '', content, flags=re.MULTILINE)
    # 去掉Markdown格式符号
    content = content.replace('**', '').replace('*', '')
    # 去掉主讲人标记
    content = re.sub(r'【.*?】', '', content)
    content = re.sub(r'（.*?）', '', content)
    content = content.strip()
    # 只提取纯汉字
    cn_chars = re.findall(r'[\u4e00-\u9fff]', content)
    return len(cn_chars)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        result = count_cn_chars(sys.argv[1])
        print(f'纯汉字字数: {result}')
    else:
        print('用法: python cn_word_count.py <文件路径>')
