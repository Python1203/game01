"""
全球指数与 ETF 分析更新生成器
专门为全球指数和 ETF 页面生成"即将推出"的更新文章
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


class IndexETFUpdater:
    """全球指数与 ETF 更新器"""
    
    def __init__(self, output_dir: str = "./public"):
        self.output_dir = output_dir
        
        # 全球主要指数
        self.indices = [
            "^GSPC",  # 标普 500
            "^DJI",   # 道琼斯
            "^IXIC",  # 纳斯达克
            "^VIX",   # 恐慌指数
            "^FTSE",  # 富时 100
            "^GDAXI", # DAX
            "^N225",  # 日经 225
            "^HSI"    # 恒生
        ]
        
        # 热门 ETF
        self.etfs = [
            "SPY",    # 标普 500 ETF
            "QQQ",    # 纳斯达克 100 ETF
            "DIA",    # 道琼斯 ETF
            "GLD",    # 黄金 ETF
            "TLT",    # 20 年 + 国债 ETF
            "VTI",    # 全美市场 ETF
            "EFA",    # 发达市场 ETF
            "EEM",    # 新兴市场 ETF
            "XLF",    # 金融行业 ETF
            "XLK"     # 科技行业 ETF
        ]
        
        # 确保输出目录存在
        os.makedirs(f"{output_dir}/index-analysis", exist_ok=True)
        os.makedirs(f"{output_dir}/etf-analysis", exist_ok=True)
    
    def generate_all_articles(self) -> tuple:
        """生成所有指数和 ETF 文章"""
        index_articles = []
        etf_articles = []
        
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
        
        # 采集指数数据
        print("\n📊 采集全球指数数据...")
        index_data = collector.fetch_global_index_data(symbols=self.indices)
        print(f"✓ 采集到 {len(index_data)} 个指数数据")
        
        # 采集 ETF 数据
        print("\n💼 采集 ETF 数据...")
        etf_data = collector.fetch_etf_data(symbols=self.etfs)
        print(f"✓ 采集到 {len(etf_data)} 个 ETF 数据")
        
        # 生成指数文章
        print("\n✍️ 生成'即将推出'系列文章...")
        for symbol, data in index_data.items():
            article = self._generate_index_article(
                symbol=symbol,
                data=data,
                generator=generator,
                injector=injector
            )
            index_articles.append(article)
            print(f"✓ 生成：{data['name']} ({symbol})")
        
        # 生成 ETF 文章
        for symbol, data in etf_data.items():
            article = self._generate_etf_article(
                symbol=symbol,
                data=data,
                generator=generator,
                injector=injector
            )
            etf_articles.append(article)
            print(f"✓ 生成：{data['name']} ({symbol})")
        
        return index_articles, etf_articles
    
    def _generate_index_article(
        self,
        symbol: str,
        data: Dict,
        generator: AIContentGenerator,
        injector: AffiliateInjector
    ) -> Article:
        """生成单个指数的"即将推出"文章"""
        
        article = generator.generate_analysis_article(
            symbol=symbol,
            data=data,
            content_type="index_analysis",
            keywords=[
                f"{data['name']}走势",
                "全球市场展望",
                "宏观经济分析",
                "指数投资策略",
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
> 我们正在为您准备更深入的 {data['name']} 分析报告，包括：
> - 📊 全球经济形势分析
> - 💰 央行政策解读
> - 🔍 资金流向监测
> - 📈 多周期技术预测
> 
> 敬请期待！
"""
        
        article.content = coming_soon_box + "\n\n" + article.content
        
        # 注入变现链接
        injected_content = injector.inject_links(article)
        article.content = injected_content
        
        # 更新 slug
        article.slug = f"index-analysis/{symbol.lower().replace('^', '')}-{datetime.now().strftime('%Y%m%d')}"
        
        return article
    
    def _generate_etf_article(
        self,
        symbol: str,
        data: Dict,
        generator: AIContentGenerator,
        injector: AffiliateInjector
    ) -> Article:
        """生成单个 ETF 的"即将推出"文章"""
        
        article = generator.generate_analysis_article(
            symbol=symbol,
            data=data,
            content_type="etf_analysis",
            keywords=[
                f"{data['name']}配置建议",
                "ETF 投资策略",
                "资产配置",
                "被动投资",
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
> 我们正在为您准备更深入的 {data['name']} 分析报告，包括：
> - 📊 持仓结构深度解析
> - 💰 费用率对比分析
> - 🔍 历史回测数据
> - 📈 配置比例建议
> 
> 敬请期待！
"""
        
        article.content = coming_soon_box + "\n\n" + article.content
        
        # 注入变现链接
        injected_content = injector.inject_links(article)
        article.content = injected_content
        
        # 更新 slug
        article.slug = f"etf-analysis/{symbol.lower()}-{datetime.now().strftime('%Y%m%d')}"
        
        return article
    
    def _generate_template_articles(self) -> tuple:
        """生成模板文章（无 AI 时使用）"""
        index_articles = []
        etf_articles = []
        
        # 生成指数模板文章
        index_names = {
            "^GSPC": "标普 500",
            "^DJI": "道琼斯工业平均",
            "^IXIC": "纳斯达克综合",
            "^VIX": "恐慌指数",
            "^FTSE": "富时 100",
            "^GDAXI": "德国 DAX",
            "^N225": "日经 225",
            "^HSI": "恒生指数"
        }
        
        for symbol in self.indices:
            name = index_names.get(symbol, symbol)
            content = f"""
# 【即将推出】{name} 指数深度分析报告

## 🚀 更多精彩即将推出

我们正在为您准备更深入的 {name} 分析报告，敬请期待！

## 当前市场数据

- **当前点位**: {self._get_mock_index_price(symbol):,.2f}
- **更新时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}

## 即将包含的内容

### 🌍 宏观经济分析
- 全球经济形势
- 主要央行政策
- 地缘政治影响

### 📊 技术面分析
- 长期趋势判断
- 关键支撑/阻力位
- 成交量分析

### 💰 资金流向
- 北向资金动向
- 机构持仓变化
- ETF 资金流入流出

### 📈 投资策略
- 定投策略建议
- 风险控制方案
- 资产配置比例

---

💡 **立即开始投资 {name}**: [点击这里开通账户](https://your-affiliate-link.com)

> ⚠️ **风险提示**: 市场有风险，投资需谨慎。本文仅供参考，不构成投资建议。
"""
            
            article = Article(
                title=f"【即将推出】{name} 指数深度分析报告",
                slug=f"index-analysis/{symbol.lower().replace('^', '')}-{datetime.now().strftime('%Y%m%d')}",
                content=content,
                excerpt=f"{name} 指数深度分析即将推出，敬请期待...",
                keywords=[f"{name}分析", "全球市场", "指数投资"],
                category="index_analysis",
                symbol=symbol,
                created_at=datetime.now().isoformat()
            )
            
            index_articles.append(article)
        
        # 生成 ETF 模板文章
        etf_names = {
            "SPY": "标普 500 ETF",
            "QQQ": "纳斯达克 100 ETF",
            "DIA": "道琼斯 ETF",
            "GLD": "黄金 ETF",
            "TLT": "20 年 + 国债 ETF",
            "VTI": "全美市场 ETF",
            "EFA": "发达市场 ETF",
            "EEM": "新兴市场 ETF",
            "XLF": "金融行业 ETF",
            "XLK": "科技行业 ETF"
        }
        
        for symbol in self.etfs:
            name = etf_names.get(symbol, symbol)
            content = f"""
# 【即将推出】{name} ({symbol}) 投资配置分析

## 🚀 更多精彩即将推出

我们正在为您准备更深入的 {name} 分析报告，敬请期待！

## 当前市场数据

- **当前价格**: ${self._get_mock_etf_price(symbol):.2f}
- **更新时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}

## 即将包含的内容

### 📊 基金概况
- 持仓结构分析
- 前十大重仓股
- 行业分布比例

### 💰 费用与表现
- 管理费率对比
- 历史收益率
- 跟踪误差分析

### 🔍 投资价值
- 估值水平分析
- 风险收益比
- 适合人群定位

### 📈 配置建议
- 核心仓位配置
- 卫星仓位配置
- 再平衡策略

---

💡 **立即开始投资 {name}**: [点击这里开通账户](https://your-affiliate-link.com)

> ⚠️ **风险提示**: 市场有风险，投资需谨慎。本文仅供参考，不构成投资建议。
"""
            
            article = Article(
                title=f"【即将推出】{name} ({symbol}) 投资配置分析",
                slug=f"etf-analysis/{symbol.lower()}-{datetime.now().strftime('%Y%m%d')}",
                content=content,
                excerpt=f"{name} 深度分析即将推出，敬请期待...",
                keywords=[f"{symbol}分析", "ETF 投资", "资产配置"],
                category="etf_analysis",
                symbol=symbol,
                created_at=datetime.now().isoformat()
            )
            
            etf_articles.append(article)
        
        return index_articles, etf_articles
    
    def _get_mock_index_price(self, symbol: str) -> float:
        """获取模拟指数价格"""
        mock_prices = {
            "^GSPC": 5200.0,
            "^DJI": 39000.0,
            "^IXIC": 16500.0,
            "^VIX": 15.0,
            "^FTSE": 7800.0,
            "^GDAXI": 18000.0,
            "^N225": 40000.0,
            "^HSI": 17000.0
        }
        return mock_prices.get(symbol, 1000.0)
    
    def _get_mock_etf_price(self, symbol: str) -> float:
        """获取模拟 ETF 价格"""
        mock_prices = {
            "SPY": 520.0,
            "QQQ": 450.0,
            "DIA": 390.0,
            "GLD": 190.0,
            "TLT": 95.0,
            "VTI": 280.0,
            "EFA": 78.0,
            "EEM": 42.0,
            "XLF": 42.0,
            "XLK": 210.0
        }
        return mock_prices.get(symbol, 100.0)
    
    def build_update_pages(self, index_articles: List[Article], etf_articles: List[Article]):
        """构建更新页面"""
        
        # 构建全球指数更新页面
        index_html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>全球指数分析更新 - 热门投资信号</title>
    <meta name="description" content="最新全球指数分析报告，深度分析标普 500、道琼斯、纳斯达克等主要指数">
    <meta name="keywords" content="全球指数，美股分析，投资建议">
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
            <h1>🌍 全球指数分析更新</h1>
        </div>
    </header>
    
    <div class="container">
        <div class="update-banner">
            <h2>🚀 全新改版即将上线</h2>
            <p>我们正在为您准备更深入的全球指数分析报告，包含宏观经济、技术面、资金流向等多维度分析</p>
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
            ''' for article in index_articles])}
        </div>
    </div>
    
    <footer>
        <p>&copy; {datetime.now().year} 热门投资信号</p>
    </footer>
</body>
</html>
"""
        
        index_filepath = f"{self.output_dir}/index-analysis/index.html"
        with open(index_filepath, 'w', encoding='utf-8') as f:
            f.write(index_html)
        print(f"✓ 全球指数更新页面已生成：{index_filepath}")
        
        # 构建 ETF 分析更新页面
        etf_html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ETF 分析更新 - 热门投资信号</title>
    <meta name="description" content="最新 ETF 分析报告，深度分析 SPY、QQQ、GLD 等热门 ETF">
    <meta name="keywords" content="ETF 分析，资产配置，投资建议">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }}
        .container {{ max-width: 1200px; margin: 0 auto; padding: 20px; }}
        header {{ background: linear-gradient(135deg, #2196F3 0%, #21CBF3 100%); color: white; padding: 40px 0; }}
        .back-link {{ color: white; text-decoration: none; }}
        h1 {{ font-size: 2em; margin-top: 10px; }}
        .update-banner {{ background: #e3f2fd; border: 2px solid #2196F3; border-radius: 8px; padding: 20px; margin: 30px 0; text-align: center; }}
        .update-banner h2 {{ color: #1565C0; margin-bottom: 10px; }}
        .update-banner p {{ color: #1565C0; }}
        .article-list {{ margin: 40px 0; }}
        .article-item {{ border: 1px solid #ddd; border-radius: 8px; padding: 20px; margin-bottom: 20px; transition: all 0.3s; }}
        .article-item:hover {{ box-shadow: 0 5px 15px rgba(0,0,0,0.1); transform: translateY(-2px); }}
        .article-item h2 {{ color: #2196F3; margin-bottom: 10px; }}
        .article-item a {{ text-decoration: none; color: inherit; }}
        .badge {{ display: inline-block; padding: 4px 12px; border-radius: 20px; font-size: 0.8em; background: #e3f2fd; color: #1976d2; margin-right: 10px; }}
        footer {{ text-align: center; padding: 30px 0; color: #666; margin-top: 60px; }}
    </style>
</head>
<body>
    <header>
        <div class="container">
            <a href="/" class="back-link">← 返回首页</a>
            <h1>💼 ETF 分析更新</h1>
        </div>
    </header>
    
    <div class="container">
        <div class="update-banner">
            <h2>🚀 全新改版即将上线</h2>
            <p>我们正在为您准备更深入的 ETF 分析报告，包含持仓分析、费用对比、配置建议等专业内容</p>
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
            ''' for article in etf_articles])}
        </div>
    </div>
    
    <footer>
        <p>&copy; {datetime.now().year} 热门投资信号</p>
    </footer>
</body>
</html>
"""
        
        etf_filepath = f"{self.output_dir}/etf-analysis/index.html"
        with open(etf_filepath, 'w', encoding='utf-8') as f:
            f.write(etf_html)
        print(f"✓ ETF 分析更新页面已生成：{etf_filepath}")
        
        return index_filepath, etf_filepath


def main():
    """主函数"""
    print("="*60)
    print("🌍 全球指数与 ETF 分析更新生成器")
    print("="*60)
    
    updater = IndexETFUpdater()
    
    # 生成文章
    index_articles, etf_articles = updater.generate_all_articles()
    print(f"\n✓ 共生成 {len(index_articles)} 篇指数文章 + {len(etf_articles)} 篇 ETF 文章")
    
    # 构建更新页面
    updater.build_update_pages(index_articles, etf_articles)
    
    # 构建文章详情页
    builder = PageBuilder(output_dir="./public")
    
    print("\n📄 生成指数文章页面...")
    for article in index_articles:
        builder.build_article_page(article)
        print(f"✓ 生成：{article.slug}")
    
    print("\n📄 生成 ETF 文章页面...")
    for article in etf_articles:
        builder.build_article_page(article)
        print(f"✓ 生成：{article.slug}")
    
    print("\n" + "="*60)
    print("✅ 全球指数与 ETF 分析更新完成！")
    print(f"📊 指数文章：{len(index_articles)} 篇")
    print(f"💼 ETF 文章：{len(etf_articles)} 篇")
    print("="*60)


if __name__ == "__main__":
    main()
