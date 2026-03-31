"""
数据采集模块
负责从各个 API 获取 Stock/Crypto/Casino 实时数据
"""
import requests
import os
from typing import Dict, List
from datetime import datetime


class DataCollector:
    """数据采集器"""
    
    def __init__(self):
        self.alpha_vantage_key = os.getenv("ALPHA_VANTAGE_KEY", "demo")
        self.finnhub_key = os.getenv("FINNHUB_KEY", "d6rihfpr01qr194ms4ngd6rihfpr01qr194ms4o0")
        self.binance_base = "https://api.binance.com/api/v3"
        self.coingecko_base = "https://api.coingecko.com/api/v3"
        
    def fetch_global_index_data(self, symbols: List[str]) -> Dict:
        """
        获取全球指数数据
        支持：^GSPC (标普 500), ^DJI (道琼斯), ^IXIC (纳斯达克), ^VIX (恐慌指数), 
             ^FTSE (富时 100), ^GDAXI (德国 DAX), ^N225 (日经 225), ^HSI (恒生)
        
        注意：Finnhub 免费版不支持指数 CFD 数据，将自动使用模拟数据
        建议：使用 ETF 替代（SPY 替代标普 500, QQQ 替代纳斯达克）
        """
        index_data = {}
        
        if not self.finnhub_key:
            print("⚠️ 未配置 Finnhub API，使用模拟指数数据")
            return self._generate_mock_index_data(symbols)
        
        for symbol in symbols:
            try:
                url = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={self.finnhub_key}"
                response = requests.get(url, timeout=10)
                data = response.json()
                
                # 检查是否是订阅限制
                if isinstance(data, dict) and "error" in data:
                    error_msg = data.get("error", "Unknown error")
                    if "subscription" in error_msg.lower():
                        print(f"⚠️ Finnhub 免费版限制：{symbol} - 使用模拟数据")
                        index_data[symbol] = self._generate_mock_index_data([symbol])[symbol]
                        continue
                
                if isinstance(data, dict) and "c" in data:
                    index_data[symbol] = {
                        "symbol": symbol,
                        "name": self._get_index_name(symbol),
                        "price": data.get("c", 0),
                        "change": round(data.get("c", 0) - data.get("pc", 0), 2),
                        "change_percent": f"{((data.get('c', 0) - data.get('pc', 0)) / data.get('pc', 1) * 100):.2f}%",
                        "volume": data.get("v", 0),
                        "high": data.get("h", 0),
                        "low": data.get("l", 0),
                        "open": data.get("o", 0),
                        "previous_close": data.get("pc", 0),
                        "timestamp": datetime.now().isoformat()
                    }
                    print(f"✓ Finnhub: {symbol} ({self._get_index_name(symbol)}) 价格 {data.get('c', 0):,.2f}")
                else:
                    raise Exception(f"Finnhub 返回异常数据：{data}")
                    
            except Exception as e:
                print(f"⚠️ Finnhub 获取指数 {symbol} 失败：{e}")
                index_data[symbol] = self._generate_mock_index_data([symbol])[symbol]
        
        return index_data
    
    def fetch_etf_data(self, symbols: List[str]) -> Dict:
        """
        获取 ETF 数据
        支持：SPY (标普 500 ETF), QQQ (纳斯达克 100 ETF), DIA (道琼斯 ETF),
             VOO (Vanguard 标普 500), ARKK (创新 ETF), IWM (罗素 2000),
             GLD (黄金 ETF), SLV (白银 ETF), USO (原油 ETF), TLT (20 年 + 国债 ETF)
        """
        etf_data = {}
        
        if not self.finnhub_key:
            print("⚠️ 未配置 Finnhub API，无法获取 ETF 数据")
            return self._generate_mock_etf_data(symbols)
        
        for symbol in symbols:
            try:
                url = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={self.finnhub_key}"
                response = requests.get(url, timeout=10)
                data = response.json()
                
                if isinstance(data, dict) and "c" in data:
                    etf_data[symbol] = {
                        "symbol": symbol,
                        "name": self._get_etf_name(symbol),
                        "price": data.get("c", 0),
                        "change": round(data.get("c", 0) - data.get("pc", 0), 2),
                        "change_percent": f"{((data.get('c', 0) - data.get('pc', 0)) / data.get('pc', 1) * 100):.2f}%",
                        "volume": data.get("v", 0),
                        "high": data.get("h", 0),
                        "low": data.get("l", 0),
                        "open": data.get("o", 0),
                        "previous_close": data.get("pc", 0),
                        "fifty_two_week_high": data.get("h52W", 0),
                        "fifty_two_week_low": data.get("l52W", 0),
                        "timestamp": datetime.now().isoformat()
                    }
                    print(f"✓ Finnhub: {symbol} ({self._get_etf_name(symbol)}) 价格 ${data.get('c', 0):,.2f}")
                else:
                    raise Exception(f"Finnhub 返回异常数据：{data}")
                    
            except Exception as e:
                print(f"⚠️ Finnhub 获取 ETF {symbol} 失败：{e}")
                etf_data[symbol] = self._generate_mock_etf_data([symbol])[symbol]
        
        return etf_data
    
    def _get_index_name(self, symbol: str) -> str:
        """获取指数名称"""
        index_names = {
            "^GSPC": "标普 500 指数",
            "^DJI": "道琼斯工业平均指数",
            "^IXIC": "纳斯达克综合指数",
            "^VIX": "CBOE 波动率指数 (恐慌指数)",
            "^FTSE": "富时 100 指数",
            "^GDAXI": "德国 DAX 指数",
            "^N225": "日经 225 指数",
            "^HSI": "恒生指数",
            "^SSEC": "上证指数",
            "^BSESN": "印度孟买 Sensex 指数"
        }
        return index_names.get(symbol, symbol)
    
    def _get_etf_name(self, symbol: str) -> str:
        """获取 ETF 名称"""
        etf_names = {
            "SPY": "SPDR 标普 500 ETF",
            "QQQ": "Invesco 纳斯达克 100 ETF",
            "DIA": "SPDR 道琼斯工业平均 ETF",
            "VOO": "Vanguard 标普 500 ETF",
            "ARKK": "ARK 创新 ETF",
            "IWM": "iShares 罗素 2000 ETF",
            "GLD": "SPDR 黄金信托",
            "SLV": "iShares 白银信托",
            "USO": "United 原油基金",
            "TLT": "iShares 20 年 + 美国国债 ETF",
            "VTI": "Vanguard 全美市场 ETF",
            "EFA": "iShares MSCI EAFE ETF",
            "EEM": "iShares MSCI 新兴市场 ETF",
            "XLF": "金融精选行业 SPDR",
            "XLK": "科技精选行业 SPDR",
            "XLV": "医疗保健精选行业 SPDR",
            "XLE": "能源精选行业 SPDR"
        }
        return etf_names.get(symbol, symbol)
    
    def _generate_mock_index_data(self, symbols: List[str]) -> Dict:
        """生成模拟指数数据"""
        import random
        index_data = {}
        
        base_prices = {
            "^GSPC": 5200, "^DJI": 39000, "^IXIC": 16500, "^VIX": 15,
            "^FTSE": 7800, "^GDAXI": 18000, "^N225": 40000, "^HSI": 17000
        }
        
        for symbol in symbols:
            base = base_prices.get(symbol, 1000)
            index_data[symbol] = {
                "symbol": symbol,
                "name": self._get_index_name(symbol),
                "price": round(base * random.uniform(0.98, 1.02), 2),
                "change": round(random.uniform(-100, 100), 2),
                "change_percent": f"{random.uniform(-2, 2):.2f}%",
                "volume": random.randint(100000000, 1000000000),
                "high": round(base * 1.01, 2),
                "low": round(base * 0.99, 2),
                "open": round(base * random.uniform(0.99, 1.01), 2),
                "previous_close": round(base, 2),
                "timestamp": datetime.now().isoformat()
            }
        
        return index_data
    
    def _generate_mock_etf_data(self, symbols: List[str]) -> Dict:
        """生成模拟 ETF 数据"""
        import random
        etf_data = {}
        
        base_prices = {
            "SPY": 520, "QQQ": 450, "DIA": 390, "VOO": 480,
            "ARKK": 50, "IWM": 200, "GLD": 190, "SLV": 23,
            "USO": 75, "TLT": 95
        }
        
        for symbol in symbols:
            base = base_prices.get(symbol, 100)
            etf_data[symbol] = {
                "symbol": symbol,
                "name": self._get_etf_name(symbol),
                "price": round(base * random.uniform(0.98, 1.02), 2),
                "change": round(random.uniform(-5, 5), 2),
                "change_percent": f"{random.uniform(-2, 2):.2f}%",
                "volume": random.randint(1000000, 50000000),
                "high": round(base * 1.01, 2),
                "low": round(base * 0.99, 2),
                "open": round(base * random.uniform(0.99, 1.01), 2),
                "previous_close": round(base, 2),
                "fifty_two_week_high": round(base * 1.15, 2),
                "fifty_two_week_low": round(base * 0.85, 2),
                "timestamp": datetime.now().isoformat()
            }
        
        return etf_data
    
    def fetch_stock_data(self, symbols: List[str]) -> Dict:
        """
        获取股票行情数据
        优先使用 Finnhub API (支持全球市场)，备用 Alpha Vantage
        """
        stock_data = {}
        
        # 尝试使用 Finnhub API
        if self.finnhub_key:
            for symbol in symbols:
                try:
                    url = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={self.finnhub_key}"
                    response = requests.get(url, timeout=10)
                    data = response.json()
                    
                    if isinstance(data, dict) and "c" in data:
                        # Finnhub 返回格式：{"c":175.5,"h":176.0,...}
                        stock_data[symbol] = {
                            "symbol": symbol,
                            "price": data.get("c", 0),  # Current price
                            "change": round(data.get("c", 0) - data.get("pc", 0), 2),  # Change
                            "change_percent": f"{((data.get('c', 0) - data.get('pc', 0)) / data.get('pc', 1) * 100):.2f}%",
                            "volume": data.get("v", 0),  # Volume
                            "high": data.get("h", 0),  # High
                            "low": data.get("l", 0),  # Low
                            "timestamp": datetime.now().isoformat()
                        }
                        print(f"✓ Finnhub: {symbol} 价格 ${data.get('c', 0):,.2f}")
                    else:
                        raise Exception(f"Finnhub 返回异常数据：{data}")
                        
                except Exception as e:
                    print(f"⚠️ Finnhub 获取 {symbol} 失败：{e}")
                    stock_data[symbol] = self._generate_mock_stock_data(symbol)
            
            return stock_data
        else:
            print("⚠️ 未配置 Finnhub API，使用 Alpha Vantage")
        
        # 备用：Alpha Vantage
        for symbol in symbols:
            try:
                # 使用 Alpha Vantage 的 Global Quote 接口
                url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={self.alpha_vantage_key}"
                response = requests.get(url, timeout=10)
                data = response.json()
                
                if "Global Quote" in data:
                    quote = data["Global Quote"]
                    stock_data[symbol] = {
                        "symbol": symbol,
                        "price": float(quote.get("05. price", 0)),
                        "change": float(quote.get("09. change", 0)),
                        "change_percent": quote.get("10. change percent", "0%"),
                        "volume": int(quote.get("06. volume", 0)),
                        "high": float(quote.get("02. high", 0)),
                        "low": float(quote.get("03. low", 0)),
                        "timestamp": datetime.now().isoformat()
                    }
                else:
                    print(f"⚠️ 无法获取 {symbol} 数据，使用模拟数据")
                    stock_data[symbol] = self._generate_mock_stock_data(symbol)
                    
            except Exception as e:
                print(f"❌ 获取 {symbol} 股票数据失败：{e}")
                stock_data[symbol] = self._generate_mock_stock_data(symbol)
        
        return stock_data
    
    def fetch_crypto_data(self, symbols: List[str]) -> Dict:
        """
        获取加密货币数据
        优先使用 Binance API (更稳定，无需 API Key)，备用 CoinGecko
        """
        crypto_data = {}
        
        # 尝试使用 Binance API
        for symbol in symbols:
            try:
                # Binance 格式：BTCUSDT, ETHUSDT
                binance_symbol = f"{symbol}USDT"
                url = f"{self.binance_base}/ticker/24hr?symbol={binance_symbol}"
                response = requests.get(url, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    crypto_data[symbol] = {
                        "symbol": symbol,
                        "name": symbol,
                        "price": float(data["lastPrice"]),
                        "market_cap": float(data.get("quoteVolume", 0)),  # 24h 成交额
                        "volume_24h": float(data.get("volume", 0)),
                        "price_change_24h": float(data.get("priceChangePercent", 0)),
                        "high_24h": float(data.get("highPrice", 0)),
                        "low_24h": float(data.get("lowPrice", 0)),
                        "circulating_supply": 0,  # Binance 不提供流通量
                        "timestamp": datetime.now().isoformat()
                    }
                    print(f"✓ Binance: {symbol} 价格 ${float(data['lastPrice']):,.2f}")
                else:
                    raise Exception(f"Binance API 返回错误：{response.status_code}")
                    
            except Exception as e:
                print(f"⚠️ Binance 获取 {symbol} 失败，切换到 CoinGecko: {e}")
                # 回退到 CoinGecko
                crypto_data.update(self._fetch_from_coingecko([symbol]))
        
        return crypto_data
    
    def _fetch_from_coingecko(self, symbols: List[str]) -> Dict:
        """从 CoinGecko 获取加密货币数据（备用方案）"""
        crypto_data = {}
        
        id_mapping = {
            "BTC": "bitcoin",
            "ETH": "ethereum",
            "SOL": "solana",
            "BNB": "binancecoin",
            "XRP": "ripple"
        }
        
        crypto_ids = [id_mapping.get(sym, sym.lower()) for sym in symbols]
        
        try:
            url = f"{self.coingecko_base}/coins/markets?vs_currency=usd&ids={','.join(crypto_ids)}"
            response = requests.get(url, timeout=10)
            data = response.json()
            
            for coin in data:
                symbol = coin["symbol"].upper()
                crypto_data[symbol] = {
                    "symbol": symbol,
                    "name": coin["name"],
                    "price": coin["current_price"],
                    "market_cap": coin["market_cap"],
                    "volume_24h": coin["total_volume"],
                    "price_change_24h": coin["price_change_percentage_24h"],
                    "high_24h": coin["high_24h"],
                    "low_24h": coin["low_24h"],
                    "circulating_supply": coin["circulating_supply"],
                    "timestamp": datetime.now().isoformat()
                }
                
        except Exception as e:
            print(f"❌ CoinGecko 获取数据失败：{e}")
            for symbol in symbols:
                crypto_data[symbol] = self._generate_mock_crypto_data(symbol)
        
        return crypto_data
    
    def fetch_casino_odds(self) -> Dict:
        """
        获取赌场/博彩赔率数据
        可以使用 The-Odds-API 或其他博彩 API
        这里提供示例框架
        """
        casino_data = {}
        
        try:
            # 示例：使用 The-Odds-API
            odds_api_key = os.getenv("ODDS_API_KEY", "")
            if odds_api_key:
                url = (
                    f"https://api.the-odds-api.com/v4/sports/upcoming/odds?"
                    f"regions=us&markets=h2h&apiKey={odds_api_key}"
                )
                response = requests.get(url, timeout=10)
                data = response.json()
                
                for event in data[:10]:  # 限制数量
                    casino_data[event["id"]] = {
                        "event_name": event["home_team"] + " vs " + event["away_team"],
                        "sport": event["sport_title"],
                        "commence_time": event["commence_time"],
                        "odds": event["bookmakers"][0]["markets"][0]["outcomes"] if event["bookmakers"] else [],
                        "timestamp": datetime.now().isoformat()
                    }
            else:
                print("⚠️ 未配置博彩 API，使用模拟数据")
                casino_data = self._generate_mock_casino_data()
                
        except Exception as e:
            print(f"❌ 获取博彩数据失败：{e}")
            casino_data = self._generate_mock_casino_data()
        
        return casino_data
    
    def _generate_mock_stock_data(self, symbol: str) -> Dict:
        """生成模拟股票数据 (用于测试)"""
        import random
        base_price = random.uniform(100, 500)
        return {
            "symbol": symbol,
            "price": round(base_price, 2),
            "change": round(random.uniform(-10, 10), 2),
            "change_percent": f"{random.uniform(-5, 5):.2f}%",
            "volume": random.randint(1000000, 10000000),
            "high": round(base_price * 1.05, 2),
            "low": round(base_price * 0.95, 2),
            "timestamp": datetime.now().isoformat()
        }
    
    def _generate_mock_crypto_data(self, symbol: str) -> Dict:
        """生成模拟加密货币数据 (用于测试)"""
        import random
        prices = {"BTC": 45000, "ETH": 2500, "SOL": 120, "BNB": 350, "XRP": 0.65}
        base_price = prices.get(symbol, 100)
        return {
            "symbol": symbol,
            "name": symbol,
            "price": base_price * random.uniform(0.95, 1.05),
            "market_cap": base_price * random.randint(1000000, 10000000),
            "volume_24h": base_price * random.randint(100000, 1000000),
            "price_change_24h": random.uniform(-10, 10),
            "high_24h": base_price * 1.1,
            "low_24h": base_price * 0.9,
            "circulating_supply": random.randint(10000000, 100000000),
            "timestamp": datetime.now().isoformat()
        }
    
    def _generate_mock_casino_data(self) -> Dict:
        """生成模拟博彩数据 (用于测试)"""
        import random
        teams = ["Lakers", "Warriors", "Celtics", "Heat", "Bulls"]
        data = {}
        
        for i in range(5):
            home = teams[random.randint(0, 4)]
            away = teams[random.randint(0, 4)]
            while away == home:
                away = teams[random.randint(0, 4)]
            
            event_id = f"event_{i}"
            data[event_id] = {
                "event_name": f"{home} vs {away}",
                "sport": "Basketball",
                "commence_time": datetime.now().isoformat(),
                "odds": [
                    {"name": home, "price": random.uniform(1.5, 2.5)},
                    {"name": away, "price": random.uniform(1.5, 2.5)}
                ],
                "timestamp": datetime.now().isoformat()
            }
        
        return data
