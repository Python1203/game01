"""
快速测试 AI 配置
"""
import os
from dotenv import load_dotenv
from src.ai_content_generator import AIContentGenerator

load_dotenv()

print("🔍 测试 AI 配置\n")

# 检测使用的 AI 模型
deepseek_key = os.getenv("DEEPSEEK_API_KEY")
deepseek_base = os.getenv("DEEPSEEK_BASE_URL")
openai_key = os.getenv("OPENAI_API_KEY")
openai_base = os.getenv("OPENAI_BASE_URL")

if openai_key and openai_key != "sk-your-openai-api-key-here":
    print(f"✓ 检测到 OpenAI 配置")
    print(f"  Base URL: {openai_base}")
    print(f"  API Key: {openai_key[:20]}...")
    
    try:
        print("\n📝 测试 OpenAI API 连接...")
        generator = AIContentGenerator(
            api_key=openai_key,
            model_type="openai",
            base_url=openai_base
        )
        
        article = generator.generate_analysis_article(
            symbol="AAPL",
            data={"price": 150.0, "change_percent": "+1.5%", "volume": 1000000},
            content_type="stock_analysis",
            keywords=["AAPL 分析", "股票投资"]
        )
        
        print(f"✅ OpenAI API 测试成功!")
        print(f"📄 生成标题：{article.title}")
        
    except Exception as e:
        print(f"❌ OpenAI API 测试失败：{e}")
        
elif deepseek_key:
    print(f"✓ 检测到 DeepSeek 配置")
    print(f"  Base URL: {deepseek_base}")
    print(f"  API Key: {deepseek_key[:20]}...")
    
    try:
        print("\n📝 测试 DeepSeek API 连接...")
        generator = AIContentGenerator(
            api_key=deepseek_key,
            model_type="deepseek",
            base_url=deepseek_base
        )
        
        article = generator.generate_analysis_article(
            symbol="BTC",
            data={"price": 50000.0, "price_change_24h": 2.5, "market_cap": 1000000000},
            content_type="crypto_analysis",
            keywords=["BTC 分析", "加密货币"]
        )
        
        print(f"✅ DeepSeek API 测试成功!")
        print(f"📄 生成标题：{article.title}")
        
    except Exception as e:
        print(f"❌ DeepSeek API 测试失败：{e}")
        print("\n💡 建议:")
        print("1. 如果使用第三方代理（xh.v1api.cc），建议切换到官方 API:")
        print("   DEEPSEEK_BASE_URL=https://api.deepseek.com")
        print("2. 前往 https://platform.deepseek.com/ 获取新的 API Key")
        print("3. 考虑使用 OpenAI（更稳定）")
else:
    print("❌ 错误：未找到有效的 AI API 配置")
    print("\n请编辑 .env 文件，配置以下任一选项:")
    print("1. OpenAI: OPENAI_API_KEY=sk-xxx")
    print("2. DeepSeek: DEEPSEEK_API_KEY=sk-xxx (官方 API: https://api.deepseek.com)")
