"""
本地测试脚本
用于在部署前测试各个模块的功能
"""
import os
import sys
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 添加 src 到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from data_collector import DataCollector
from ai_content_generator import AIContentGenerator
from affiliate_injector import AffiliateInjector
from page_builder import PageBuilder


def test_data_collector():
    """测试数据采集模块"""
    print("\n" + "="*60)
    print("📊 测试数据采集模块")
    print("="*60)
    
    collector = DataCollector()
    
    # 测试股票数据
    print("\n1️⃣ 测试股票数据采集...")
    stock_data = collector.fetch_stock_data(["AAPL", "TSLA"])
    for symbol, data in stock_data.items():
        print(f"\n✓ {symbol}:")
        print(f"   价格：${data['price']}")
        print(f"   涨跌：{data['change_percent']}")
        print(f"   成交量：{data['volume']:,}")
    
    # 测试加密货币数据
    print("\n2️⃣ 测试加密货币数据采集...")
    crypto_data = collector.fetch_crypto_data(["BTC", "ETH"])
    for symbol, data in crypto_data.items():
        print(f"\n✓ {symbol}:")
        print(f"   价格：${data['price']}")
        print(f"   24h 涨跌：{data['price_change_24h']:.2f}%")
        print(f"   市值：${data['market_cap']:,}")
    
    # 测试博彩数据
    print("\n3️⃣ 测试博彩数据采集...")
    casino_data = collector.fetch_casino_odds()
    print(f"✓ 采集到 {len(casino_data)} 条赔率数据")
    
    print("\n✅ 数据采集测试完成!")
    return True


def test_ai_generator():
    """测试 AI 内容生成模块"""
    print("\n" + "="*60)
    print("✍️ 测试 AI 内容生成模块")
    print("="*60)
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("⚠️ 未配置 OPENAI_API_KEY，使用模板模式")
        api_key = "test-key"
    
    generator = AIContentGenerator(api_key=api_key)
    
    # 模拟数据
    mock_data = {
        "price": 150.25,
        "change_percent": "+2.5%",
        "volume": 10000000,
        "high": 152.0,
        "low": 148.5
    }
    
    print("\n1️⃣ 测试生成股票分析文章...")
    article = generator.generate_analysis_article(
        symbol="AAPL",
        data=mock_data,
        content_type="stock_analysis",
        keywords=["苹果股票分析", "AAPL 走势", "科技股投资"]
    )
    
    print(f"\n✓ 生成文章:")
    print(f"   标题：{article.title}")
    print(f"   Slug: {article.slug}")
    print(f"   摘要：{article.excerpt[:80]}...")
    print(f"   字数：{len(article.content)}")
    
    print("\n2️⃣ 测试生成加密货币文章...")
    crypto_article = generator.generate_analysis_article(
        symbol="BTC",
        data={
            "price": 45000,
            "price_change_24h": 3.5,
            "market_cap": 900000000000,
            "volume_24h": 30000000000,
            "high_24h": 46000,
            "low_24h": 44000
        },
        content_type="crypto_analysis",
        keywords=["比特币价格预测", "BTC 分析", "加密货币投资"]
    )
    
    print(f"\n✓ 生成文章:")
    print(f"   标题：{crypto_article.title}")
    print(f"   摘要：{crypto_article.excerpt[:80]}...")
    
    print("\n✅ AI 内容生成测试完成!")
    return [article, crypto_article]


def test_affiliate_injector(articles):
    """测试 Affiliate Link 注入模块"""
    print("\n" + "="*60)
    print("💰 测试 Affiliate Link 注入模块")
    print("="*60)
    
    affiliate_links = [
        "https://example.com/affiliate1",
        "https://example.com/affiliate2"
    ]
    
    injector = AffiliateInjector(affiliate_links=affiliate_links)
    
    print("\n1️⃣ 测试向股票文章注入链接...")
    injected_content = injector.inject_links(articles[0])
    link_count = injected_content.count("](https://")
    print(f"✓ 注入后链接数量：{link_count}")
    print(f"✓ 文章长度：{len(injected_content)} 字符")
    
    print("\n2️⃣ 测试向加密货币文章注入链接...")
    injected_content2 = injector.inject_links(articles[1])
    link_count2 = injected_content2.count("](https://")
    print(f"✓ 注入后链接数量：{link_count2}")
    
    print("\n✅ Affiliate Link 注入测试完成!")
    return True


def test_page_builder(articles):
    """测试页面构建模块"""
    print("\n" + "="*60)
    print("🏗️ 测试页面构建模块")
    print("="*60)
    
    builder = PageBuilder(output_dir="./test_public")
    
    print("\n1️⃣ 构建首页...")
    homepage_path = builder.build_homepage(articles=articles)
    print(f"✓ 首页路径：{homepage_path}")
    
    print("\n2️⃣ 构建文章详情页...")
    for article in articles:
        article_path = builder.build_article_page(article)
        print(f"✓ 生成页面：{article_path}")
    
    print("\n3️⃣ 构建分类页面...")
    category_paths = builder.build_category_pages(articles=articles)
    for path in category_paths:
        print(f"✓ 分类页面：{path}")
    
    total_pages = builder.get_page_count()
    print(f"\n📊 总计生成 {total_pages} 个页面")
    
    print("\n✅ 页面构建测试完成!")
    return True


def main():
    """运行所有测试"""
    print("\n" + "="*60)
    print("🧪 Stock/Crypto/Casino 自动化系统 - 本地测试")
    print("="*60)
    
    try:
        # 1. 测试数据采集
        test_data_collector()
        
        # 2. 测试 AI 内容生成
        articles = test_ai_generator()
        
        # 3. 测试 Affiliate Link 注入
        test_affiliate_injector(articles)
        
        # 4. 测试页面构建
        test_page_builder(articles)
        
        print("\n" + "="*60)
        print("✅ 所有测试通过！系统已准备好部署!")
        print("="*60)
        
        print("\n📋 下一步操作:")
        print("1. 检查生成的测试页面：ls -la test_public/")
        print("2. 安装 Vercel CLI: npm install -g vercel")
        print("3. 部署到 Vercel: vercel --prod")
        print("4. 配置 GitHub Actions 自动触发")
        
    except Exception as e:
        print(f"\n❌ 测试失败：{e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
