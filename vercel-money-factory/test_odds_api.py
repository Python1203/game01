"""
测试 The Odds API - 检查真实返回数据
"""
import requests
import json

API_KEY = "3838a6272cab9b49dac3d9f646fbca4b"

# 测试英超赛事
url = f"https://api.the-odds-api.com/v4/sports/soccer_epl/odds?regions=uk&markets=h2h&apiKey={API_KEY}"

print("🔍 正在请求 The Odds API...")
response = requests.get(url, timeout=15)

print(f"\n状态码：{response.status_code}")

if response.status_code == 200:
    data = response.json()
    print(f"\n✅ 成功获取到 {len(data)} 场比赛")
    
    if len(data) > 0:
        print("\n" + "="*60)
        print("第一场比赛详情:")
        print("="*60)
        match = data[0]
        print(f"比赛 ID: {match['id']}")
        print(f"主队：{match['home_team']}")
        print(f"客队：{match['away_team']}")
        print(f"比赛时间：{match['commence_time']}")
        print(f"体育项目：{match['sport_title']}")
        
        if match.get('bookmakers'):
            print(f"\n博彩公司数量：{len(match['bookmakers'])}")
            
            # 显示第一个博彩公司的详细赔率
            first_bookmaker = match['bookmakers'][0]
            print(f"\n{first_bookmaker['title']} 的赔率:")
            if first_bookmaker.get('markets'):
                for market in first_bookmaker['markets']:
                    print(f"  市场：{market['key']}")
                    for outcome in market.get('outcomes', []):
                        print(f"    - {outcome['name']}: {outcome['price']}")
        
        # 保存完整数据到文件
        with open('test_odds_response.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"\n💾 完整数据已保存到：test_odds_response.json")
else:
    print(f"\n❌ 请求失败：{response.text}")
