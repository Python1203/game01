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
