#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将 stock-analysis 目录中的 HTML 文章转换为 Markdown 格式
"""

import os
import re
from pathlib import Path

def extract_article_info(html_content):
    """从 HTML 中提取文章信息"""
    
    # 提取标题
    title_match = re.search(r'<title>(.*?)</title>', html_content)
    title = title_match.group(1) if title_match else "未命名文章"
    # 清理 Markdown 标记
    title = title.replace('```markdown...', '深度分析')
    
    # 提取描述
    desc_match = re.search(r'<meta name="description" content="(.*?)">', html_content, re.DOTALL)
    description = desc_match.group(1) if desc_match else ""
    # 清理 Markdown 标记
    description = re.sub(r'```markdown\n*', '', description)
    description = re.sub(r'^#\s*', '', description).strip()
    
    # 提取标签
    keywords_match = re.search(r'<meta name="keywords" content="(.*?)">', html_content)
    keywords_str = keywords_match.group(1) if keywords_match else ""
    keywords = [k.strip() for k in keywords_str.split(',')]
    
    # 提取发布日期
    date_match = re.search(r'发布于 (\d{4}-\d{2}-\d{2})', html_content)
    pub_date = date_match.group(1) if date_match else "2026-03-31"
    
    # 提取正文内容（清理 HTML 标签和 Markdown 标记）
    content_match = re.search(r'<div class="article-content">(.*?)</div>\s*</div>\s*</div>', html_content, re.DOTALL)
    if content_match:
        content = content_match.group(1)
        # 移除所有 HTML 标签
        content = re.sub(r'<[^>]+>', '', content)
        # 清理 Markdown 代码块标记
        content = re.sub(r'```markdown\n*', '', content)
        content = re.sub(r'```\s*$', '', content)
        # 清理多余的 HTML 实体
        content = content.replace('&gt;', '>')
        content = content.replace('&lt;', '<')
        content = content.replace('&amp;', '&')
        # 清理多余的空行
        content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
    else:
        content = ""
    
    return {
        'title': title,
        'description': description,
        'keywords': keywords,
        'pub_date': pub_date,
        'content': content.strip()
    }

def create_markdown_file(article_dir, output_dir):
    """将 HTML 文章转换为 Markdown 文件"""
    
    html_file = article_dir / 'index.html'
    if not html_file.exists():
        return False
    
    # 读取 HTML 文件
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # 提取文章信息
    article_info = extract_article_info(html_content)
    
    # 创建 Markdown 内容
    md_content = f"""---
title: "{article_info['title']}"
description: "{article_info['description']}"
pubDate: {article_info['pub_date']}
category: "Stock Analysis"
tags: [{', '.join([f'"{k}"' for k in article_info['keywords']])}]
---

{article_info['content']}
"""
    
    # 写入 Markdown 文件
    md_file = output_dir / 'index.md'
    with open(md_file, 'w', encoding='utf-8') as f:
        f.write(md_content)
    
    print(f"✓ 转换成功：{md_file}")
    return True

def main():
    """主函数"""
    base_dir = Path('/Users/zzw868/PycharmProjects/PythonProject/public/stock-analysis')
    
    # 获取所有文章目录
    article_dirs = [d for d in base_dir.iterdir() if d.is_dir() and d.name != '.DS_Store']
    
    print(f"找到 {len(article_dirs)} 篇文章目录")
    
    # 转换每篇文章
    for article_dir in article_dirs:
        print(f"\n处理：{article_dir.name}")
        create_markdown_file(article_dir, article_dir)
    
    print("\n✅ 所有文章转换完成！")

if __name__ == '__main__':
    main()
