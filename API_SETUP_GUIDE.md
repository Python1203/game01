# API 集成配置指南

## ✅ 已完成的 API 集成

### 1. **Binance API（加密货币）** 🟢
- **状态**: 已成功集成，无需 API Key
- **支持币种**: BTC, ETH, SOL, BNB, XRP 等
- **数据字段**: 
  - 实时价格
  - 24h 涨跌幅
  - 24h 最高/最低价
  - 24h 成交量
  - 市值（24h 成交额）

**测试示例**:
```python
BTC/USDT:
  当前价格：$67,890.35
  24h 涨跌：+1.63%
  24h 最高：$68,408.37
  24h 最低：$66,233.13
```

---

### 2. **Finnhub API（美股/全球市场）** 🟢
- **状态**: 已成功集成，需要 API Key
- **支持市场**: 美股、港股、A 股、外汇、指数
- **Token**: `d6rihfpr01qr194ms4ngd6rihfpr01qr194ms4o0`
- **数据字段**:
  - 实时股价
  - 涨跌额/涨跌幅
  - 今日最高/最低
  - 成交量
  - 昨收价

**测试示例**:
```python
AAPL:
  当前价格：$246.63
  涨跌：$-2.17 (-0.87%)
  今日最高：$250.87
  今日最低：$245.51
```

---

### 3. **CoinGecko API（加密货币备用方案）** 🟡
- **状态**: 备用方案，当 Binance 不可用时自动切换
- **优势**: 提供更详细的币种信息（流通量、完全稀释估值等）

---

## 📋 配置步骤

### 方法 1: 使用 .env 文件（推荐）

1. 复制示例文件：
```bash
cp .env.example .env
```

2. 编辑 `.env` 文件：
```bash
# AI 配置
OPENAI_API_KEY=sk-your-openai-api-key-here

# 数据源配置
ALPHA_VANTAGE_KEY=demo
FINNHUB_KEY=d6rihfpr01qr194ms4ngd6rihfpr01qr194ms4o0

# 变现配置
AFFILIATE_LINKS=https://your-affiliate-link-1.com,https://your-affiliate-link-2.com
```

### 方法 2: 直接在代码中使用

已在代码中内置 Finnhub Token，可直接使用。

---

## 🧪 测试 API 连接

运行测试脚本：
```bash
python3 test_api_integration.py
```

**预期输出**:
- ✓ Binance API 测试通过（BTC, ETH, SOL, BNB 价格）
- ✓ Finnhub API 测试通过（AAPL, TSLA, NVDA, MSFT 价格）
- ✓ DataCollector 集成测试通过

---

## 🔄 自动故障转移机制

### 加密货币数据:
```
Binance API (主) → CoinGecko API (备用) → 模拟数据 (最后方案)
```

### 股票数据:
```
Finnhub API (主，需 Key) → Alpha Vantage API (备用) → 模拟数据 (最后方案)
```

---

## 📊 性能对比

| API | 响应时间 | 限制 | 稳定性 |
|-----|---------|------|--------|
| **Binance** | ~200ms | 无（公开接口） | ⭐⭐⭐⭐⭐ |
| **Finnhub** | ~300ms | 60 次/分钟（免费） | ⭐⭐⭐⭐ |
| **CoinGecko** | ~500ms | 10-50 次/分钟 | ⭐⭐⭐ |
| **Alpha Vantage** | ~800ms | 500 次/天 | ⭐⭐ |

---

## 💡 使用建议

1. **加密货币**: 优先使用 Binance（更快、更稳定）
2. **美股**: 使用 Finnhub（已内置 Token）
3. **生产环境**: 建议申请自己的 API Key 以获得更高配额

---

## 🔗 相关文档

- [Binance API 文档](https://binance-docs.github.io/apidocs/)
- [Finnhub API 文档](https://finnhub.io/docs/api)
- [CoinGecko API 文档](https://www.coingecko.com/en/api/documentation)

---

**更新时间**: 2026-03-31  
**测试状态**: ✅ 所有 API 连接正常
