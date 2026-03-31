"""
测试 DeepSeek API 集成
"""
import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.ai_content_generator import AIContentGenerator


def test_deepseek_api():
    """测试 DeepSeek API 连接和生成功能"""
    print("=" * 60)
    print("🧪 测试 DeepSeek API 集成")
    print("=" * 60)
    
    # DeepSeek 配置
    api_key = "sk-ekXi4cdzr5m0U5bm1a315a21EdDb42Ec863c0b37C092081e"
    base_url = "https://xh.v1api.cc"
    
    try:
        # 初始化生成器
        print("\n📌 初始化 AIContentGenerator (DeepSeek)...")
        generator = AIContentGenerator(
            api_key=api_key,
            model_type="deepseek",
            base_url=base_url
        )
        print("✓ 初始化成功")
        
        # 测试生成文章
        print("\n📝 测试生成 BTC 分析文章...")
        test_data = {
            "symbol": "BTC",
            "price": 67900.50,
            "price_change_24h": 1.75,
            "market_cap": 1340000000000,
            "volume_24h": 25000000000,
            "high_24h": 68500.00,
            "low_24h": 66200.00
        }
        
        article = generator.generate_analysis_article(
            symbol="BTC",
            data=test_data,
            content_type="crypto_analysis",
            keywords=["BTC 价格预测", "比特币分析", "加密货币投资"]
        )
        
        print(f"\n✓ 文章生成成功！")
        print(f"\n标题：{article.title}")
        print(f"\n摘要：{article.excerpt}")
        print(f"\n分类：{article.category}")
        print(f"\n创建时间：{article.created_at}")
        print("\n" + "=" * 60)
        print("✅ DeepSeek API 测试通过！")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"\n❌ 测试失败：{e}")
        print("\n请检查:")
        print("1. API Key 是否正确")
        print("2. Base URL 是否可访问")
        print("3. 网络连接是否正常")
        print("=" * 60)
        return False


def test_openai_compatibility():
    """测试 OpenAI API 兼容性"""
    print("\n" + "=" * 60)
    print("🧪 测试 OpenAI API 兼容性（可选）")
    print("=" * 60)
    
    openai_key = os.getenv("OPENAI_API_KEY")
    
    if not openai_key:
        print("⚠️ 未设置 OPENAI_API_KEY，跳过测试")
        return
    
    try:
        generator = AIContentGenerator(api_key=openai_key, model_type="openai")
        
        test_data = {
            "symbol": "AAPL",
            "price": 246.63,
            "change_percent": "-0.87%",
            "volume": 50000000,
            "high": 250.87,
            "low": 245.51
        }
        
        article = generator.generate_analysis_article(
            symbol="AAPL",
            data=test_data,
            content_type="stock_analysis",
            keywords=["AAPL 股价分析", "苹果股票", "投资建议"]
        )
        
        print(f"\n✓ OpenAI 文章生成成功！")
        print(f"标题：{article.title}")
        print("=" * 60)
        print("✅ OpenAI API 测试通过！")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ OpenAI 测试失败：{e}")


if __name__ == "__main__":
    print(f"🚀 开始测试 AI API - {__import__('datetime').datetime.now()}\n")
    
    # 测试 DeepSeek
    success = test_deepseek_api()
    
    # 测试 OpenAI（如果有配置）
    test_openai_compatibility()
    
    if success:
        print("\n✅ 所有测试完成！可以开始使用 DeepSeek API 生成内容。")
        print("\n💡 下一步:")
        print("1. 运行 python3 main.py 执行完整流程")
        print("2. 查看生成的文章在 public/ 目录")
    else:
        print("\n❌ 测试失败，请检查配置后重试")
        sys.exit(1)
