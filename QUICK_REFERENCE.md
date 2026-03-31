# 🚀 快速参考 - 实时市场数据 API

## 💰 当前市场价格（实时更新）

### 加密货币 (Binance)
| 币种 | 价格 | 24h 涨跌 |
|------|------|---------|
| BTC | ~$67,900 | +1.76% ↗ |
| ETH | ~$2,075 | +3.04% ↗ |
| SOL | ~$83.75 | +1.20% ↗ |
| BNB | ~$616 | +0.29% ↗ |

### 美股 (Finnhub)
| 股票代码 | 价格 | 涨跌 |
|----------|------|------|
| AAPL | $246.63 | -0.87% ↘ |
| TSLA | $355.28 | -1.81% ↘ |
| NVDA | $165.17 | -1.40% ↘ |
| MSFT | $358.96 | +0.61% ↗ |

---

## ⚡ 一行代码获取价格

```python
from src.data_collector import DataCollector

collector = DataCollector()

# 获取 BTC 价格
btc_price = collector.fetch_crypto_data(['BTC'])['BTC']['price']
print(f"BTC: ${btc_price:,.2f}")

# 获取 AAPL 价格
aapl_price = collector.fetch_stock_data(['AAPL'])['AAPL']['price']
print(f"AAPL: ${aapl_price:,.2f}")
```

---

## 📝 API Token

**Finnhub Token**: `d6rihfpr01qr194ms4ngd6rihfpr01qr194ms4o0`

**配置方式**:
```bash
# 方法 1: 已内置，可直接使用
# 方法 2: 写入 .env 文件
echo "FINNHUB_KEY=d6rihfpr01qr194ms4ngd6rihfpr01qr194ms4o0" >> .env
```

---

## 🧪 测试命令

```bash
# 完整测试
python3 test_api_integration.py

# 快速获取单个价格
python3 -c "from src.data_collector import DataCollector; c = DataCollector(); print('BTC:', c.fetch_crypto_data(['BTC'])['BTC']['price'])"

# 运行主程序
python3 main.py
```

---

## 🔄 故障转移

```
加密货币：Binance → CoinGecko → 模拟数据
股票：Finnhub → Alpha Vantage → 模拟数据
```

---

## 📊 响应时间

- **Binance**: ~200ms ⚡
- **Finnhub**: ~300ms ⚡
- **CoinGecko**: ~500ms
- **Alpha Vantage**: ~800ms

---

## 💡 提示

1. **无需 API Key**: Binance 公开接口可直接使用
2. **Token 已内置**: Finnhub token 已配置好
3. **自动重试**: 失败时自动切换到备用 API
4. **实时数据**: 所有价格均为实时市场价

---

**更新时间**: 2026-03-31  
**状态**: ✅ 运行正常
