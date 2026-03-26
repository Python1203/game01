#!/usr/bin/env python3
"""
清理 Next.js 静态导出产生的中文目录
只保留 URL 编码的目录以避免客户端预取 404 错误
"""

import os
import re
import sys

def is_chinese_directory(name):
    """检查目录名是否包含中文字符"""
    # 匹配任何非 ASCII 字符（包括中文）
    return bool(re.search(r'[^\x00-\x7F]', name))

def clean_directories(base_path):
    """清理 tags 目录下的中文目录"""
    tags_dir = os.path.join(base_path, 'out', 'tags')
    
    if not os.path.exists(tags_dir):
        print(f"目录不存在：{tags_dir}")
        return
    
    deleted_count = 0
    for item in os.listdir(tags_dir):
        item_path = os.path.join(tags_dir, item)
        
        # 只处理目录，跳过文件
        if not os.path.isdir(item_path):
            continue
        
        # 跳过 index.html 和 index.txt（虽然在根目录）
        if item in ['index.html', 'index.txt']:
            continue
        
        # 检查是否包含中文字符
        if is_chinese_directory(item):
            try:
                import shutil
                shutil.rmtree(item_path)
                print(f"  已删除：{item}")
                deleted_count += 1
            except Exception as e:
                print(f"  删除失败 {item}: {e}", file=sys.stderr)
    
    print(f"\n共删除 {deleted_count} 个中文目录")

if __name__ == '__main__':
    if len(sys.argv) > 1:
        base_path = sys.argv[1]
    else:
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    clean_directories(base_path)
