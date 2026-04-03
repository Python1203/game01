"""
测试 Finnhub API - 获取实时 ETF 数据
"""
import requests
import json
from datetime import datetime

FINNHUB_KEY = "d6rihfpr01qr194ms4ngd6rihfpr01qr194ms4o0"

# 测试热门 ETF
etfs = ["SPY", "QQQ", "GLD", "TLT", "DIA", "VTI", "EEM", "XLF", "XLK"]

print("="*60)
print("🔍 测试 Finnhub API - 获取实时 ETF 数据")
print("="*60)

all_data = {}

for etf in etfs:
    try:
        url = f"https://finnhub.io/api/v1/quote?symbol={etf}&token={FINNHUB_KEY}"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            if isinstance(data, dict) and "c" in data:
                current_price = data.get('c', 0)
                previous_close = data.get('pc', 0)
                change = current_price - previous_close
                change_percent = (change / previous_close) * 100
                
                etf_info = {
                    "symbol": etf,
                    "current_price": current_price,
                    "previous_close": previous_close,
                    "change": round(change, 2),
                    "change_percent": f"{change_percent:.2f}%",
                    "day_high": data.get('h', 0),
                    "day_low": data.get('l', 0),
                    "open": data.get('o', 0),
                    "volume": data.get('v', 0),
                    "52w_high": data.get('h52W', 0),
                    "52w_low": data.get('l52W', 0),
                    "timestamp": datetime.now().isoformat()
                }
                
                all_data[etf] = etf_info
                
                # 打印结果
                print(f"\n✅ {etf}:")
                print(f"   当前价格：${current_price:,.2f}")
                print(f"   涨跌：{change:+,.2f} ({change_percent:+.2f}%)")
                print(f"   成交量：{data.get('v', 0):,}")
                print(f"   52 周范围：${data.get('l52W', 0):,.2f} - ${data.get('h52W', 0):,.2f}")
            else:
                print(f"\n❌ {etf}: 返回异常数据 - {data}")
        else:
            print(f"\n❌ {etf}: HTTP {response.status_code}")
            
    except Exception as e:
        print(f"\n❌ {etf}: 请求失败 - {e}")

# 保存完整数据到文件
if all_data:
    with open('test_finnhub_etf_response.json', 'w', encoding='utf-8') as f:
        json.dump(all_data, f, indent=2, ensure_ascii=False)
    print(f"\n💾 完整数据已保存到：test_finnhub_etf_response.json")
    print(f"\n✅ 成功获取 {len(all_data)} 个 ETF 的实时数据")
else:
    print("\n❌ 未能获取任何 ETF 数据")

print("="*60)
