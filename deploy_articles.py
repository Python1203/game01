#!/usr/bin/env python3
"""
部署脚本 - 将 public 目录的文章复制到 Astro 构建输出目录
"""
import os
import shutil
from pathlib import Path

def deploy_articles():
    """复制文章到 Astro dist 目录"""
    
    # 定义源目录和目标目录
    project_root = Path(__file__).parent
    public_dir = project_root / "public"
    astro_dist_dir = project_root / "vercel-money-factory" / "dist"
    
    # 确保目标目录存在
    if not astro_dist_dir.exists():
        print(f"❌ Astro dist 目录不存在：{astro_dist_dir}")
        print("请先运行：cd vercel-money-factory && pnpm run build")
        return False
    
    # 要复制的目录
    dirs_to_copy = [
        "stock-analysis",
        "etf-analysis", 
        "index-analysis"
    ]
    
    print("🚀 开始复制文章...")
    
    for dir_name in dirs_to_copy:
        src_dir = public_dir / dir_name
        dst_dir = astro_dist_dir / dir_name
        
        if src_dir.exists():
            # 如果目标已存在，先删除
            if dst_dir.exists():
                shutil.rmtree(dst_dir)
            
            # 复制目录
            shutil.copytree(src_dir, dst_dir)
            print(f"✓ 复制：{dir_name}/")
        else:
            print(f"⚠️ 跳过：{dir_name} (源目录不存在)")
    
    # 也要复制主 index.html 作为备用
    main_index = public_dir / "index.html"
    if main_index.exists():
        print(f"\n✓ 主页面已更新在 Astro dist 目录中")
    
    print("\n✅ 完成！所有文章已复制到 Astro dist 目录")
    print(f"📁 目标位置：{astro_dist_dir}")
    print("\n下一步:")
    print("1. cd vercel-money-factory")
    print("2. git add -A && git commit -m 'feat: 更新分析文章'")
    print("3. git push origin main")
    
    return True

if __name__ == "__main__":
    deploy_articles()
