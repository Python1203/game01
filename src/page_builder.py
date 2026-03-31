"""
静态页面构建模块
生成 HTML 页面并输出到 public 目录
"""
import os
import json
from typing import List, Dict
from datetime import datetime


class PageBuilder:
    """页面构建器"""
    
    def __init__(self, output_dir: str = "./public"):
        self.output_dir = output_dir
        self.page_count = 0
        
        # 确保输出目录存在
        os.makedirs(output_dir, exist_ok=True)
        os.makedirs(f"{output_dir}/stock-analysis", exist_ok=True)
        os.makedirs(f"{output_dir}/crypto-analysis", exist_ok=True)
        os.makedirs(f"{output_dir}/casino-review", exist_ok=True)
    
    def build_homepage(self, articles: List) -> str:
        """构建首页"""
        
        # 分类文章
        stock_articles = [a for a in articles if a.category == "stock_analysis"]
        crypto_articles = [a for a in articles if a.category == "crypto_analysis"]
        casino_articles = [a for a in articles if a.category == "casino_review"]
        
        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>热门投资信号 - Stock/Crypto/Casino 实时分析</title>
    <meta name="description" content="提供最新的股票、加密货币和博彩投资分析，AI 驱动的智能推荐系统">
    <meta name="keywords" content="股票分析，加密货币，投资信号，AI 推荐">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; }}
        .container {{ max-width: 1200px; margin: 0 auto; padding: 20px; }}
        header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 60px 0; text-align: center; }}
        h1 {{ font-size: 2.5em; margin-bottom: 10px; }}
        .subtitle {{ font-size: 1.2em; opacity: 0.9; }}
        .section {{ margin: 40px 0; }}
        .section-title {{ font-size: 2em; margin-bottom: 20px; color: #333; border-bottom: 3px solid #667eea; padding-bottom: 10px; }}
        .article-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }}
        .article-card {{ border: 1px solid #ddd; border-radius: 8px; padding: 20px; transition: transform 0.3s; }}
        .article-card:hover {{ transform: translateY(-5px); box-shadow: 0 5px 15px rgba(0,0,0,0.1); }}
        .article-card h3 {{ color: #667eea; margin-bottom: 10px; }}
        .article-meta {{ color: #666; font-size: 0.9em; margin-bottom: 10px; }}
        .article-excerpt {{ color: #555; margin-bottom: 15px; }}
        .read-more {{ display: inline-block; background: #667eea; color: white; padding: 8px 20px; text-decoration: none; border-radius: 5px; }}
        .read-more:hover {{ background: #5568d3; }}
        footer {{ background: #333; color: white; text-align: center; padding: 30px 0; margin-top: 60px; }}
        .badge {{ display: inline-block; padding: 4px 12px; border-radius: 20px; font-size: 0.8em; margin-right: 10px; }}
        .badge-stock {{ background: #e3f2fd; color: #1976d2; }}
        .badge-crypto {{ background: #f3e5f5; color: #7b1fa2; }}
        .badge-casino {{ background: #fff3e0; color: #f57c00; }}
    </style>
</head>
<body>
    <header>
        <div class="container">
            <h1>🚀 热门投资信号</h1>
            <p class="subtitle">AI 驱动的 Stock/Crypto/Casino 智能分析平台</p>
            <p style="margin-top: 15px; opacity: 0.8;">更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
        </div>
    </header>
    
    <div class="container">
        <!-- 股票分析 -->
        <section class="section">
            <h2 class="section-title">📈 股票分析</h2>
            <div class="article-grid">
                {self._generate_article_cards(stock_articles)}
            </div>
        </section>
        
        <!-- 加密货币 -->
        <section class="section">
            <h2 class="section-title">₿ 加密货币</h2>
            <div class="article-grid">
                {self._generate_article_cards(crypto_articles)}
            </div>
        </section>
        
        <!-- 博彩推荐 -->
        <section class="section">
            <h2 class="section-title">🎰 博彩推荐</h2>
            <div class="article-grid">
                {self._generate_article_cards(casino_articles)}
            </div>
        </section>
    </div>
    
    <footer>
        <div class="container">
            <p>&copy; {datetime.now().year} 热门投资信号。All rights reserved.</p>
            <p style="margin-top: 10px; font-size: 0.9em; color: #aaa;">
                风险提示：投资有风险，入市需谨慎。本网站内容仅供参考，不构成投资建议。
            </p>
        </div>
    </footer>
</body>
</html>
"""
        
        # 写入文件
        filepath = f"{self.output_dir}/index.html"
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        
        self.page_count += 1
        return filepath
    
    def _generate_article_cards(self, articles: List) -> str:
        """生成文章卡片 HTML"""
        if not articles:
            return '<p style="color: #999; padding: 20px;">暂无文章</p>'
        
        cards_html = []
        for article in articles:
            badge_class = f"badge-{article.category.split('_')[0]}"
            badge_text = {
                "stock_analysis": "📈 股票",
                "crypto_analysis": "₿ 加密货币",
                "casino_review": "🎰 博彩"
            }.get(article.category, "📄 文章")
            
            card = f"""
                <div class="article-card">
                    <span class="badge {badge_class}">{badge_text}</span>
                    <h3>{article.title}</h3>
                    <p class="article-meta">更新时间：{article.created_at[:10]}</p>
                    <p class="article-excerpt">{article.excerpt}</p>
                    <a href="/{article.slug}/index.html" class="read-more">阅读全文 →</a>
                </div>
            """
            cards_html.append(card)
        
        return '\n'.join(cards_html)
    
    def build_article_page(self, article) -> str:
        """构建文章详情页"""
        
        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{article.title}</title>
    <meta name="description" content="{article.excerpt}">
    <meta name="keywords" content="{', '.join(article.keywords)}">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; background: #f5f5f5; }}
        .container {{ max-width: 900px; margin: 0 auto; padding: 20px; }}
        header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 40px 0; }}
        .back-link {{ display: inline-block; color: white; text-decoration: none; margin-bottom: 20px; }}
        .back-link:hover {{ text-decoration: underline; }}
        h1 {{ font-size: 2em; margin-bottom: 10px; }}
        .article-meta {{ color: rgba(255,255,255,0.9); margin-bottom: 20px; }}
        .article-content {{ background: white; padding: 40px; border-radius: 8px; margin-top: 30px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        .article-content h2 {{ color: #667eea; margin: 30px 0 15px; font-size: 1.5em; }}
        .article-content h3 {{ color: #333; margin: 25px 0 10px; font-size: 1.2em; }}
        .article-content p {{ margin-bottom: 15px; color: #333; }}
        .article-content ul, .article-content ol {{ margin: 15px 0 15px 30px; }}
        .article-content li {{ margin-bottom: 8px; }}
        .cta-box {{ background: #f0f4ff; border-left: 4px solid #667eea; padding: 20px; margin: 30px 0; border-radius: 4px; }}
        .cta-box a {{ color: #667eea; font-weight: bold; }}
        footer {{ text-align: center; padding: 40px 0; color: #666; margin-top: 60px; }}
        @media (max-width: 768px) {{
            .container {{ padding: 15px; }}
            .article-content {{ padding: 20px; }}
            h1 {{ font-size: 1.5em; }}
        }}
    </style>
</head>
<body>
    <header>
        <div class="container">
            <a href="/" class="back-link">← 返回首页</a>
            <h1>{article.title}</h1>
            <p class="article-meta">
                发布于 {article.created_at[:10]} | 
                分类：{article.category.replace('_', ' ').title()} | 
                标签：{', '.join(article.keywords)}
            </p>
        </div>
    </header>
    
    <div class="container">
        <div class="article-content">
            {self._markdown_to_html(article.content)}
        </div>
    </div>
    
    <footer>
        <div class="container">
            <p>&copy; {datetime.now().year} 热门投资信号</p>
            <p style="margin-top: 10px; font-size: 0.9em; color: #999;">
                免责声明：本网站可能包含 affiliate links，点击可能会产生佣金。
            </p>
        </div>
    </footer>
</body>
</html>
"""
        
        # 创建目录并写入文件
        dir_path = f"{self.output_dir}/{article.slug}"
        os.makedirs(dir_path, exist_ok=True)
        
        filepath = f"{dir_path}/index.html"
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        
        self.page_count += 1
        return filepath
    
    def build_category_pages(self, articles: List) -> List[str]:
        """构建分类页面"""
        filepaths = []
        
        categories = {
            "stock-analysis": [a for a in articles if a.category == "stock_analysis"],
            "crypto-analysis": [a for a in articles if a.category == "crypto_analysis"],
            "casino-review": [a for a in articles if a.category == "casino_review"]
        }
        
        for category, category_articles in categories.items():
            html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{category.replace('-', ' ').title()} - 热门投资信号</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }}
        .container {{ max-width: 1200px; margin: 0 auto; padding: 20px; }}
        header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 40px 0; }}
        .back-link {{ color: white; text-decoration: none; }}
        h1 {{ font-size: 2em; margin-top: 10px; }}
        .article-list {{ margin: 40px 0; }}
        .article-item {{ border: 1px solid #ddd; border-radius: 8px; padding: 20px; margin-bottom: 20px; }}
        .article-item h2 {{ color: #667eea; margin-bottom: 10px; }}
        .article-item a {{ text-decoration: none; color: inherit; }}
        footer {{ text-align: center; padding: 30px 0; color: #666; margin-top: 60px; }}
    </style>
</head>
<body>
    <header>
        <div class="container">
            <a href="/" class="back-link">← 返回首页</a>
            <h1>{category.replace('-', ' ').title()}</h1>
        </div>
    </header>
    
    <div class="container">
        <div class="article-list">
            {''.join([f'''
            <div class="article-item">
                <a href="/{article.slug}/index.html">
                    <h2>{article.title}</h2>
                    <p>{article.excerpt}</p>
                </a>
            </div>
            ''' for article in category_articles])}
        </div>
    </div>
    
    <footer>
        <p>&copy; {datetime.now().year} 热门投资信号</p>
    </footer>
</body>
</html>
"""
            
            filepath = f"{self.output_dir}/{category}/index.html"
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html)
            
            self.page_count += 1
            filepaths.append(filepath)
        
        return filepaths
    
    def _markdown_to_html(self, markdown_text: str) -> str:
        """简单的 Markdown 转 HTML (生产环境建议使用 markdown 库)"""
        html = markdown_text
        
        # 标题
        html = html.replace('# ', '<h2>')
        html = html.replace('\n# ', '\n</h2>\n<h2>')
        html = html.replace('## ', '<h3>')
        html = html.replace('\n## ', '\n</h3>\n<h3>')
        
        # 粗体
        html = html.replace('**', '</strong>')
        html = html.replace('**', '<strong>')
        
        # 链接
        import re
        html = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', html)
        
        # 段落
        paragraphs = html.split('\n\n')
        html = '\n\n'.join([f'<p>{p}</p>' if not p.startswith('<h') and not p.startswith('<ul') else p for p in paragraphs])
        
        return html
    
    def get_page_count(self) -> int:
        """获取生成的页面数量"""
        return self.page_count
