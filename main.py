"""
Stock/Crypto/Casino 全自动内容生成系统
主入口 - 被 Vercel Build 调用执行
"""
import os
import sys
from datetime import datetime
from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()

# 导入各个模块
from src.data_collector import DataCollector
from src.ai_content_generator import AIContentGenerator
from src.affiliate_injector import AffiliateInjector
from src.page_builder import PageBuilder


def main():
    """主执行流程"""
    print(f"🚀 开始执行自动化流水线 - {datetime.now()}")
    
    # 1. 初始化配置
    affiliate_links = os.getenv("AFFILIATE_LINKS", "").split(",")
    
    # 检测使用哪个 AI 模型
    deepseek_key = os.getenv("DEEPSEEK_API_KEY")
    deepseek_base = os.getenv("DEEPSEEK_BASE_URL")
    openai_key = os.getenv("OPENAI_API_KEY")
    
    if deepseek_key:
        print(f"✓ 使用 DeepSeek AI 模型")
        api_key = deepseek_key
        model_type = "deepseek"
        base_url = deepseek_base
    elif openai_key:
        print(f"✓ 使用 OpenAI AI 模型")
        api_key = openai_key
        model_type = "openai"
        base_url = os.getenv("OPENAI_BASE_URL")
    else:
        print("❌ 错误：缺少 AI API Key（OPENAI_API_KEY 或 DEEPSEEK_API_KEY）")
        sys.exit(1)
    
    # 2. 采集行情数据
    print("\n📊 步骤 1: 采集市场数据...")
    collector = DataCollector()
    
    # 采集股票数据（使用 Finnhub API）
    stock_data = collector.fetch_stock_data(symbols=["AAPL", "TSLA", "NVDA", "MSFT"])
    print(f"✓ 采集到 {len(stock_data)} 条股票数据")
    
    # 采集加密货币数据（使用 Binance API）
    crypto_data = collector.fetch_crypto_data(symbols=["BTC", "ETH", "SOL", "BNB"])
    print(f"✓ 采集到 {len(crypto_data)} 条加密货币数据")
    
    # 采集全球指数数据（新增）
    index_data = collector.fetch_global_index_data(symbols=["^GSPC", "^DJI", "^IXIC", "^VIX"])
    print(f"✓ 采集到 {len(index_data)} 条全球指数数据")
    
    # 采集 ETF 数据（新增）
    etf_data = collector.fetch_etf_data(symbols=["SPY", "QQQ", "DIA", "GLD", "TLT"])
    print(f"✓ 采集到 {len(etf_data)} 条 ETF 数据")
    
    # 采集赌场/博彩数据
    casino_data = collector.fetch_casino_odds()
    print(f"✓ 采集到 {len(casino_data)} 条赔率数据")
    
    # 3. AI 生成 SEO 文章
    print("\n✍️ 步骤 2: 生成 SEO 内容...")
    generator = AIContentGenerator(api_key=api_key, model_type=model_type, base_url=base_url)
    
    articles = []
    for symbol, data in stock_data.items():
        article = generator.generate_analysis_article(
            symbol=symbol,
            data=data,
            content_type="stock_analysis",
            keywords=[f"{symbol}股价分析", f"{symbol}走势预测", "股票投资建议"]
        )
        articles.append(article)
        print(f"✓ 生成文章：{symbol} 分析报告")
    
    for symbol, data in crypto_data.items():
        article = generator.generate_analysis_article(
            symbol=symbol,
            data=data,
            content_type="crypto_analysis",
            keywords=[f"{symbol}价格预测", f"{symbol}行情分析", "加密货币投资"]
        )
        articles.append(article)
        print(f"✓ 生成文章：{symbol} 市场分析")
    
    # 生成全球指数分析文章（新增）
    for symbol, data in index_data.items():
        article = generator.generate_analysis_article(
            symbol=symbol,
            data=data,
            content_type="index_analysis",
            keywords=[f"{data['name']}走势", "全球市场展望", "宏观经济分析"]
        )
        articles.append(article)
        print(f"✓ 生成文章：{data['name']} 分析报告")
    
    # 生成 ETF 投顾分析文章（新增）
    for symbol, data in etf_data.items():
        article = generator.generate_analysis_article(
            symbol=symbol,
            data=data,
            content_type="etf_analysis",
            keywords=[f"{data['name']}配置建议", "ETF 投资策略", "资产配置"]
        )
        articles.append(article)
        print(f"✓ 生成文章：{data['name']} 投资分析")

    # 4. 注入 Affiliate Links
    print("\n💰 步骤 3: 注入变现链接...")
    injector = AffiliateInjector(affiliate_links=affiliate_links)
    
    for article in articles:
        injected_content = injector.inject_links(article)
        article.content = injected_content
        print(f"✓ 已注入变现链接：{article.title}")
    
    # 5. 构建静态页面
    print("\n🏗️ 步骤 4: 构建静态页面...")
    builder = PageBuilder(output_dir="./public")
    
    # 生成首页
    builder.build_homepage(articles=articles)
    print("✓ 首页生成完成")
    
    # 生成文章详情页
    for article in articles:
        builder.build_article_page(article)
        print(f"✓ 文章页面生成：{article.slug}")
    
    # 生成分类页面
    builder.build_category_pages(articles=articles)
    print("✓ 分类页面生成完成")
    
    # 6. 输出统计信息
    total_articles = len(articles)
    total_pages = builder.get_page_count()
    
    print("\n" + "="*50)
    print(f"✅ 流水线执行完成!")
    print(f"📝 生成文章：{total_articles} 篇")
    print(f"📄 生成页面：{total_pages} 个")
    print(f"⏱️ 耗时：{datetime.now()}")
    print("="*50)


if __name__ == "__main__":
    main()
