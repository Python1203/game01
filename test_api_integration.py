"""
测试 Binance 和 Finnhub API 连接
"""
import requests
from datetime import datetime


def test_binance_api():
    """测试 Binance API（加密货币）"""
    print("=" * 60)
    print("🔍 测试 Binance API - 加密货币实时价格")
    print("=" * 60)
    
    base_url = "https://api.binance.com/api/v3"
    symbols = ["BTC", "ETH", "SOL", "BNB"]
    
    for symbol in symbols:
        try:
            binance_symbol = f"{symbol}USDT"
            url = f"{base_url}/ticker/24hr?symbol={binance_symbol}"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                price = float(data["lastPrice"])
                change_24h = float(data["priceChangePercent"])
                volume = float(data.get("volume", 0))
                high = float(data.get("highPrice", 0))
                low = float(data.get("lowPrice", 0))
                
                print(f"\n✓ {symbol}/USDT:")
                print(f"  当前价格：${price:,.2f}")
                print(f"  24h 涨跌：{change_24h:+.2f}%")
                print(f"  24h 最高：${high:,.2f}")
                print(f"  24h 最低：${low:,.2f}")
                print(f"  24h 成交量：{volume:,.0f} {symbol}")
            else:
                print(f"❌ {symbol} 请求失败：HTTP {response.status_code}")
                
        except Exception as e:
            print(f"❌ {symbol} 异常：{e}")
    
    print("\n" + "=" * 60)


def test_finnhub_api(api_key: str):
    """测试 Finnhub API（美股/全球市场）"""
    print("=" * 60)
    print("🔍 测试 Finnhub API - 股票实时行情")
    print("=" * 60)
    
    if not api_key:
        print("⚠️ 未提供 Finnhub API Key，跳过测试")
        return
    
    symbols = ["AAPL", "TSLA", "NVDA", "MSFT"]
    
    for symbol in symbols:
        try:
            url = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={api_key}"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if isinstance(data, dict) and "c" in data:
                    current_price = data.get("c", 0)
                    previous_close = data.get("pc", 0)
                    change = current_price - previous_close
                    change_percent = (change / previous_close) * 100 if previous_close else 0
                    high = data.get("h", 0)
                    low = data.get("l", 0)
                    volume = data.get("v", 0)
                    
                    print(f"\n✓ {symbol}:")
                    print(f"  当前价格：${current_price:,.2f}")
                    print(f"  涨跌：${change:+.2f} ({change_percent:+.2f}%)")
                    print(f"  今日最高：${high:,.2f}")
                    print(f"  今日最低：${low:,.2f}")
                    print(f"  成交量：{volume:,}")
                else:
                    print(f"⚠️ {symbol} 返回异常数据：{data}")
            else:
                print(f"❌ {symbol} 请求失败：HTTP {response.status_code}")
                
        except Exception as e:
            print(f"❌ {symbol} 异常：{e}")
    
    print("\n" + "=" * 60)


def test_data_collector_integration():
    """测试集成后的 DataCollector 类"""
    print("\n" + "=" * 60)
    print("🧪 测试 DataCollector 集成")
    print("=" * 60)
    
    import sys
    sys.path.insert(0, '/Users/zzw868/PycharmProjects/PythonProject')
    
    from src.data_collector import DataCollector
    
    collector = DataCollector()
    
    # 测试加密货币数据
    print("\n📊 采集加密货币数据...")
    crypto_data = collector.fetch_crypto_data(symbols=["BTC", "ETH"])
    
    for symbol, data in crypto_data.items():
        print(f"\n✓ {data.get('name', symbol)}:")
        print(f"  价格：${data['price']:,.2f}")
        print(f"  24h 涨跌：{data['price_change_24h']:+.2f}%")
        print(f"  市值：${data['market_cap']:,.0f}")
    
    # 测试股票数据
    print("\n📊 采集股票数据...")
    stock_data = collector.fetch_stock_data(symbols=["AAPL", "TSLA"])
    
    for symbol, data in stock_data.items():
        print(f"\n✓ {symbol}:")
        print(f"  价格：${data['price']:,.2f}")
        print(f"  涨跌：{data['change']}")
        print(f"  成交量：{data['volume']:,}")
    
    print("\n" + "=" * 60)
    print("✅ 集成测试完成！")
    print("=" * 60)


if __name__ == "__main__":
    print(f"🚀 开始测试 API 连接 - {datetime.now()}\n")
    
    # 1. 测试 Binance API
    test_binance_api()
    
    # 2. 测试 Finnhub API
    finnhub_key = "d6rihfpr01qr194ms4ngd6rihfpr01qr194ms4o0"
    test_finnhub_api(finnhub_key)
    
    # 3. 测试集成
    test_data_collector_integration()
    
    print(f"\n✅ 所有测试完成 - {datetime.now()}")
