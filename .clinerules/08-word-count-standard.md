# 08 - 中文纯字数统计标准（更正）

> 每次统计中文文章字数时，必须使用此规则，**绝不能用PowerShell的Measure-Object**。

## 统计标准

中文文章/比赛宣讲稿的"字数" = **纯汉字字数**（只统计`\u4e00-\u9fff`范围内的汉字）

**不统计的内容：**
- 标点符号（。，、！？""''等）
- 英文字母和数字（a-z, A-Z, 0-9）
- Markdown格式标记（**, *, #等）
- 主讲人标签（【甲】【乙】【合】等）

## 正确统计方法

### 方法一：使用 skills/cn_word_count.py（推荐）

```bash
python skills/cn_word_count.py <文件路径>
```

### 方法二：Node.js 单行命令

```bash
node -e "const fs=require('fs');let t=fs.readFileSync('文件路径','utf8');t=t.replace(/^#.*\n/m,'').replace(/\*\*/g,'').replace(/【.*?】/g,'').replace(/（.*?）/g,'').trim();console.log('纯汉字字数:'+t.match(/[\u4e00-\u9fff]/g).length)"
```

### 方法三：Python 单行命令

```bash
python -c "import re;t=open('文件路径','r',encoding='utf-8').read();t=re.sub(r'^#.*\n','',t);t=re.sub(r'【.*?】','',t);t=re.sub(r'（.*?）','',t);t=t.replace('**','').strip();print('纯汉字字数:'+str(len(re.findall(r'[\u4e00-\u9fff]',t))))"
```

## 🚨 严格禁止的命令

```bash
# ❌ 绝对不要用！这个会把中文字符算成多字节，结果翻倍
Get-Content file.md | Measure-Object
# ❌ 也绝对不要用 PowerShell 做任何中文字数统计
```

## 字数换算参考

| 实际需要 | 纯汉字数 |
|---------|---------|
| 5分钟宣讲 | ~1100字 |
| 8分钟宣讲 | ~1500-1700字 |
| 比赛要求1500字 | 纯汉字达到1500即合格 |
