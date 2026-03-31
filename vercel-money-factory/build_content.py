import os
from datetime import datetime

# 模拟币种数据 (实际可循环调用 ccxt)
coins = [
    {"sym": "BTC", "price": "65432.10", "change": "+2.5%"},
    {"sym": "ETH", "price": "3456.78", "change": "-1.2%"},
    {"sym": "SOL", "price": "145.20", "change": "+5.8%"}
]

def generate_md():
    os.makedirs('src/pages/crypto', exist_ok=True)
    for coin in coins:
        content = f"""---
layout: ../../layouts/BaseLayout.astro
title: "{coin['sym']} Price Prediction & Real-time Analysis {datetime.now().year}"
description: "Latest {coin['sym']} market data. Price: ${coin['price']}. Expert AI forecast inside."
symbol: "{coin['sym']}"
price: "{coin['price']}"
change: "{coin['change']}"
pubDate: "{datetime.now().strftime('%Y-%m-%d')}"
---
## Market Overview
The current price of **{coin['sym']}** is ${coin['price']}. Market sentiment is showing a {coin['change']} movement today.

## AI Prediction
Our AI model suggests that {coin['sym']} is approaching a critical resistance level. 
[Click here to trade {coin['sym']} on Binance with 20% cashback](YOUR_AFF_LINK)
"""
        with open(f"src/pages/crypto/{coin['sym'].lower()}.md", "w", encoding="utf-8") as f:
            f.write(content)

if __name__ == "__main__":
    generate_md()
