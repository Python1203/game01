"""
测试全球指数和 ETF 数据采集
"""
import sys
sys.path.insert(0, '/Users/zzw868/PycharmProjects/PythonProject')

from src.data_collector import DataCollector
from datetime import datetime


def test_global_indices():
    """测试全球指数数据"""
    print("=" * 60)
    print("🌍 测试全球指数数据采集")
    print("=" * 60)
    
    collector = DataCollector()
    
    # 主要全球指数
    indices = [
        "^GSPC",  # 标普 500
        "^DJI",   # 道琼斯
        "^IXIC",  # 纳斯达克
        "^VIX",   # 恐慌指数
        "^FTSE",  # 富时 100
        "^GDAXI", # 德国 DAX
        "^N225",  # 日经 225
        "^HSI"    # 恒生
    ]
    
    index_data = collector.fetch_global_index_data(indices)
    
    print("\n" + "=" * 60)
    print("📊 全球指数实时行情")
    print("=" * 60)
    
    for symbol, data in index_data.items():
        print(f"\n{data['name']} ({symbol})")
        print(f"  当前点位：{data['price']:,.2f}")
        print(f"  涨跌：{data['change']:+.2f} ({data['change_percent']})")
        print(f"  成交量：{data['volume']:,}")
        print(f"  最高：{data['high']:,.2f} | 最低：{data['low']:,.2f}")
    
    print("\n" + "=" * 60)
    return index_data


def test_etfs():
    """测试 ETF 数据"""
    print("=" * 60)
    print("💼 测试 ETF 数据采集")
    print("=" * 60)
    
    collector = DataCollector()
    
    # 热门 ETF
    etfs = [
        "SPY",   # 标普 500 ETF
        "QQQ",   # 纳斯达克 100 ETF
        "DIA",   # 道琼斯 ETF
        "VOO",   # Vanguard 标普 500
        "GLD",   # 黄金 ETF
        "TLT",   # 20 年 + 国债 ETF
        "ARKK",  # 创新 ETF
        "IWM"    # 罗素 2000 ETF
    ]
    
    etf_data = collector.fetch_etf_data(etfs)
    
    print("\n" + "=" * 60)
    print("📈 ETF 实时行情")
    print("=" * 60)
    
    for symbol, data in etf_data.items():
        print(f"\n{data['name']} ({symbol})")
        print(f"  当前价格：${data['price']:,.2f}")
        print(f"  涨跌：{data['change']:+.2f} ({data['change_percent']})")
        print(f"  成交量：{data['volume']:,}")
        print(f"  52 周：${data['fifty_two_week_low']:,.2f} - ${data['fifty_two_week_high']:,.2f}")
    
    print("\n" + "=" * 60)
    return etf_data


def test_full_pipeline():
    """测试完整数据采集流程"""
    print("\n" + "=" * 60)
    print("🚀 测试完整数据采集流程")
    print("=" * 60)
    
    collector = DataCollector()
    
    print("\n📊 采集各类资产数据...")
    
    # 股票
    print("\n1️⃣ 股票数据...")
    stocks = collector.fetch_stock_data(["AAPL", "TSLA", "NVDA"])
    print(f"   ✓ 采集到 {len(stocks)} 条股票数据")
    
    # 加密货币
    print("\n2️⃣ 加密货币数据...")
    crypto = collector.fetch_crypto_data(["BTC", "ETH", "SOL"])
    print(f"   ✓ 采集到 {len(crypto)} 条加密货币数据")
    
    # 全球指数
    print("\n3️⃣ 全球指数数据...")
    indices = collector.fetch_global_index_data(["^GSPC", "^DJI", "^IXIC"])
    print(f"   ✓ 采集到 {len(indices)} 条指数数据")
    
    # ETF
    print("\n4️⃣ ETF 数据...")
    etfs = collector.fetch_etf_data(["SPY", "QQQ", "GLD"])
    print(f"   ✓ 采集到 {len(etfs)} 条 ETF 数据")
    
    print("\n" + "=" * 60)
    print("✅ 完整流程测试通过！")
    print("=" * 60)
    
    # 汇总展示
    print("\n📋 数据汇总")
    print("-" * 60)
    print(f"股票：{len(stocks)} 只")
    print(f"加密货币：{len(crypto)} 种")
    print(f"全球指数：{len(indices)} 个")
    print(f"ETF: {len(etfs)} 只")
    print("-" * 60)
    print(f"总计：{len(stocks) + len(crypto) + len(indices) + len(etfs)} 个投资标的")
    
    return {
        "stocks": stocks,
        "crypto": crypto,
        "indices": indices,
        "etfs": etfs
    }


if __name__ == "__main__":
    print(f"🕒 测试时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # 1. 测试全球指数
    test_global_indices()
    
    # 2. 测试 ETF
    test_etfs()
    
    # 3. 测试完整流程
    test_full_pipeline()
    
    print(f"\n✅ 所有测试完成 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
