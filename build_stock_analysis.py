"""
美股分析更新生成器
专门为美股分析页面生成"即将推出"的更新文章
"""
import os
from datetime import datetime
from typing import List, Dict
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 导入模块
from src.data_collector import DataCollector
from src.ai_content_generator import AIContentGenerator, Article
from src.affiliate_injector import AffiliateInjector
from src.page_builder import PageBuilder


class StockAnalysisUpdater:
    """美股分析更新器"""
    
    def __init__(self, output_dir: str = "./public"):
        self.output_dir = output_dir
        self.symbols = ["AAPL",  ]
        
        # 确保输出目录存在
        os.makedirs(f"{output_dir}/stock-analysis", exist_ok=True)
    
    def generate_coming_soon_articles(self) -> List[Article]:
        """生成"即将推出"系列文章"""
        articles = []
        
        # 检测 AI 配置
        deepseek_key = os.getenv("DEEPSEEK_API_KEY")
        deepseek_base = os.getenv("DEEPSEEK_BASE_URL")
        openai_key = os.getenv("OPENAI_API_KEY")
        
        if deepseek_key:
            api_key = deepseek_key
            model_type = "deepseek"
            base_url = deepseek_base
            print("✓ 使用 DeepSeek AI 模型")
        elif openai_key:
            api_key = openai_key
            model_type = "openai"
            base_url = os.getenv("OPENAI_BASE_URL")
            print("✓ 使用 OpenAI AI 模型")
        else:
            print("⚠️ 未配置 AI API，使用模板内容")
            return self._generate_template_articles()
        
        # 初始化组件
        collector = DataCollector()
        generator = AIContentGenerator(api_key=api_key, model_type=model_type, base_url=base_url)
        injector = AffiliateInjector(
            affiliate_links=os.getenv("AFFILIATE_LINKS", "").split(","),
            binance_link=os.getenv("BINANCE_AFFILIATE_LINK")
        )
        
        # 采集股票数据
        print("\n📊 采集股票数据...")
        stock_data = collector.fetch_stock_data(symbols=self.symbols)
        print(f"✓ 采集到 {len(stock_data)} 条股票数据")
        
        # 生成文章
        print("\n✍️ 生成'即将推出'系列文章...")
        for symbol, data in stock_data.items():
            # 构建特殊的提示词，强调"即将推出"
            article = self._generate_single_article(
                symbol=symbol,
                data=data,
                generator=generator,
                injector=injector
            )
            articles.append(article)
            print(f"✓ 生成：{symbol} 深度分析")
        
        return articles
    
    def _generate_single_article(
        self,
        symbol: str,
        data: Dict,
        generator: AIContentGenerator,
        injector: AffiliateInjector
    ) -> Article:
        """生成单只股票的"即将推出"文章"""
        
        # 使用标准的 stock_analysis 类型，但在内容中强调"即将推出"
        article = generator.generate_analysis_article(
            symbol=symbol,
            data=data,
            content_type="stock_analysis",
            keywords=[
                f"{symbol}股价分析",
                f"{symbol}走势预测",
                "美股投资",
                "股票分析报告",
                "即将推出更多深度内容"
            ]
        )
        
        # 在标题中添加"即将推出"标识
        original_title = article.title
        article.title = f"【即将推出】{original_title}"
        
        # 在内容开头添加预告框
        coming_soon_box = f"""
> 🚀 **更多精彩即将推出**
> 
> 我们正在为您准备更深入的 {symbol} 分析报告，包括：
> - 📊 详细的技术面分析
> - 💰 机构持仓变化
> - 🔍 产业链深度调研
> - 📈 多场景价格预测
> 
> 敬请期待！
"""
        
        article.content = coming_soon_box + "\n\n" + article.content
        
        # 注入变现链接
        injected_content = injector.inject_links(article)
        article.content = injected_content
        
        # 更新 slug，添加到 stock-analysis 目录
        article.slug = f"stock-analysis/{symbol.lower()}-{datetime.now().strftime('%Y%m%d')}"
        
        return article
    
    def _generate_template_articles(self) -> List[Article]:
        """生成模板文章（无 AI 时使用）"""
        articles = []
        
        for symbol in self.symbols:
            content = f"""
# 【即将推出】{symbol} 深度分析报告

## 🚀 更多精彩即将推出

我们正在为您准备更深入的 {symbol} 分析报告，敬请期待！

## 当前市场数据

- **当前价格**: ${self._get_mock_price(symbol):.2f}
- **更新时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}

## 即将包含的内容

### 📊 技术面分析
- 支撑位与阻力位
- 均线系统分析
- MACD、RSI 等技术指标

### 💰 基本面分析
- 财务报表解读
- 估值水平分析
- 行业地位评估

### 🔍 资金流向
- 北向资金动向
- 机构持仓变化
- 大股东增减持

### 📈 价格预测
- 短期走势判断
- 中期目标价位
- 长期投资价值

---

💡 **立即开始投资 {symbol}**: [点击这里开通账户](https://your-affiliate-link.com)

> ⚠️ **风险提示**: 股市有风险，投资需谨慎。本文仅供参考，不构成投资建议。
"""
            
            article = Article(
                title=f"【即将推出】{symbol} 深度分析报告",
                slug=f"stock-analysis/{symbol.lower()}-{datetime.now().strftime('%Y%m%d')}",
                content=content,
                excerpt=f"{symbol} 深度分析即将推出，敬请期待...",
                keywords=[f"{symbol}分析", f"{symbol}预测", "美股投资"],
                category="stock_analysis",
                symbol=symbol,
                created_at=datetime.now().isoformat()
            )
            
            articles.append(article)
        
        return articles
    
    def _get_mock_price(self, symbol: str) -> float:
        """获取模拟价格"""
        mock_prices = {
            "AAPL": 246.63,
            "TSLA": 175.34,
            "NVDA": 138.07,
            "MSFT": 420.45,
            "GOOGL": 175.35,
            "META": 563.92,
            "AMZN": 180.75,
            "AMD": 125.34
        }
        return mock_prices.get(symbol, 100.0)
    
    def build_update_page(self, articles: List[Article]) -> str:
        """构建更新页面"""
        
        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>美股分析更新 - 热门投资信号</title>
    <meta name="description" content="最新美股分析报告，深度分析 AAPL、TSLA、NVDA 等热门股票">
    <meta name="keywords" content="美股分析，股票报告，投资建议">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }}
        .container {{ max-width: 1200px; margin: 0 auto; padding: 20px; }}
        header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 40px 0; }}
        .back-link {{ color: white; text-decoration: none; }}
        h1 {{ font-size: 2em; margin-top: 10px; }}
        .update-banner {{ background: #fff3cd; border: 2px solid #ffc107; border-radius: 8px; padding: 20px; margin: 30px 0; text-align: center; }}
        .update-banner h2 {{ color: #856404; margin-bottom: 10px; }}
        .update-banner p {{ color: #856404; }}
        .article-list {{ margin: 40px 0; }}
        .article-item {{ border: 1px solid #ddd; border-radius: 8px; padding: 20px; margin-bottom: 20px; transition: all 0.3s; }}
        .article-item:hover {{ box-shadow: 0 5px 15px rgba(0,0,0,0.1); transform: translateY(-2px); }}
        .article-item h2 {{ color: #667eea; margin-bottom: 10px; }}
        .article-item a {{ text-decoration: none; color: inherit; }}
        .badge {{ display: inline-block; padding: 4px 12px; border-radius: 20px; font-size: 0.8em; background: #e3f2fd; color: #1976d2; margin-right: 10px; }}
        footer {{ text-align: center; padding: 30px 0; color: #666; margin-top: 60px; }}
    </style>
</head>
<body>
    <header>
        <div class="container">
            <a href="/" class="back-link">← 返回首页</a>
            <h1>📈 美股分析更新</h1>
        </div>
    </header>
    
    <div class="container">
        <div class="update-banner">
            <h2>🚀 全新改版即将上线</h2>
            <p>我们正在为您准备更深入的美股分析报告，包含技术面、基本面、资金流向等多维度分析</p>
        </div>
        
        <div class="article-list">
            {''.join([f'''
            <div class="article-item">
                <a href="/{article.slug}/index.html">
                    <span class="badge">即将推出</span>
                    <h2>{article.title}</h2>
                    <p>{article.excerpt}</p>
                </a>
            </div>
            ''' for article in articles])}
        </div>
    </div>
    
    <footer>
        <p>&copy; {datetime.now().year} 热门投资信号</p>
    </footer>
</body>
</html>
"""
        
        filepath = f"{self.output_dir}/stock-analysis/index.html"
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"✓ 更新页面已生成：{filepath}")
        return filepath


def main():
    """主函数"""
    print("="*60)
    print("📈 美股分析更新生成器")
    print("="*60)
    
    updater = StockAnalysisUpdater()
    
    # 生成文章
    articles = updater.generate_coming_soon_articles()
    print(f"\n✓ 共生成 {len(articles)} 篇文章")
    
    # 构建更新页面
    updater.build_update_page(articles)
    
    # 构建文章详情页
    builder = PageBuilder(output_dir="./public")
    for article in articles:
        builder.build_article_page(article)
        print(f"✓ 生成文章页面：{article.slug}")
    
    print("\n" + "="*60)
    print("✅ 美股分析更新完成！")
    print("="*60)


if __name__ == "__main__":
    main()
