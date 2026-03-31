"""
博彩 API 测试脚本
测试 The-Odds-API 和 API-Football/Basketball
"""
import os
import sys
from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()

# 导入数据采集模块
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from src.data_collector import DataCollector


def test_odds_api():
    """测试 The-Odds-API"""
    print("="*60)
    print("🎲 测试 The-Odds-API")
    print("="*60)
    
    api_key = os.getenv("ODDS_API_KEY", "")
    print(f"API Key: {api_key[:10]}...{api_key[-5:]}")
    
    if not api_key:
        print("❌ 未配置 ODDS_API_KEY")
        return
    
    # 测试 API 连接
    try:
        import requests
        url = f"https://api.the-odds-api.com/v4/sports/upcoming/odds?regions=us&markets=h2h&apiKey={api_key}"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✓ 连接成功！获取到 {len(data)} 场赛事")
            
            if data:
                print(f"\n📊 前 3 场赛事示例:")
                for i, event in enumerate(data[:3], 1):
                    print(f"\n{i}. {event['sport_title']}: {event['away_team']} @ {event['home_team']}")
                    print(f"   比赛时间：{event['commence_time']}")
                    
                    if event.get('bookmakers'):
                        bookmaker = event['bookmakers'][0]
                        print(f"   博彩公司：{bookmaker['title']}")
                        
                        if bookmaker.get('markets'):
                            outcomes = bookmaker['markets'][0]['outcomes']
                            for outcome in outcomes:
                                print(f"   - {outcome['name']}: {outcome['price']}")
            
            print(f"\n✅ The-Odds-API 测试通过!")
            print(f"💡 剩余额度检查：每天 500 次限额，建议每天运行 2-3 次构建")
        else:
            print(f"❌ 请求失败：HTTP {response.status_code}")
            print(f"响应内容：{response.text[:200]}")
            
    except Exception as e:
        print(f"❌ 测试失败：{e}")


def test_sports_api():
    """测试 API-Football/Basketball"""
    print("\n" + "="*60)
    print("⚽ 测试 API-Football/Basketball")
    print("="*60)
    
    api_key = os.getenv("SPORTS_API_KEY", "")
    print(f"API Key: {api_key[:10]}...{api_key[-5:]}")
    
    if not api_key:
        print("❌ 未配置 SPORTS_API_KEY")
        return
    
    # 测试 API 连接（足球）
    try:
        import requests
        url = "https://v3.football.api-sports.io/fixtures?live=all"
        headers = {"x-apisports-key": api_key}
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            results = data.get('results', 0)
            print(f"✓ 连接成功！当前有 {results} 场进行中赛事")
            
            if data.get('response'):
                print(f"\n📊 前 3 场直播赛事示例:")
                for i, fixture in enumerate(data['response'][:3], 1):
                    home = fixture['teams']['home']['name']
                    away = fixture['teams']['away']['name']
                    goals_home = fixture['goals']['home']
                    goals_away = fixture['goals']['away']
                    minute = fixture['fixture']['status']['elapsed']
                    
                    print(f"\n{i}. {away} {goals_away} - {goals_home} {home}")
                    print(f"   联赛：{fixture['league']['name']}")
                    print(f"   时间：{minute}'")
            
            print(f"\n✅ API-Football 测试通过!")
        else:
            print(f"❌ 请求失败：HTTP {response.status_code}")
            print(f"响应内容：{response.text[:200]}")
            
    except Exception as e:
        print(f"❌ 测试失败：{e}")


def test_data_collector():
    """测试 DataCollector 的 fetch_casino_odds 方法"""
    print("\n" + "="*60)
    print("🏆 测试 DataCollector 集成")
    print("="*60)
    
    collector = DataCollector()
    
    try:
        casino_data = collector.fetch_casino_odds()
        
        if casino_data:
            print(f"\n✓ 成功获取 {len(casino_data)} 场赛事赔率数据")
            
            # 显示前 3 场
            for i, (event_id, data) in enumerate(list(casino_data.items())[:3], 1):
                print(f"\n{i}. {data['event_name']} ({data['sport']})")
                print(f"   来源：{data.get('source', 'Unknown')}")
                print(f"   时间：{data['commence_time']}")
                
                if data.get('odds'):
                    print(f"   赔率:")
                    for outcome in data['odds'][:3]:
                        print(f"   - {outcome['name']}: ${outcome['price']:.2f}")
        else:
            print("\n⚠️ 未获取到真实数据，使用模拟数据")
        
        print(f"\n✅ DataCollector 集成测试完成!")
        
    except Exception as e:
        print(f"❌ 集成测试失败：{e}")
        import traceback
        traceback.print_exc()


def main():
    """主测试流程"""
    print("\n" + "🎰"*30)
    print("🎰 博彩 API 完整测试 🎰")
    print("🎰"*30 + "\n")
    
    # 1. 测试 The-Odds-API
    test_odds_api()
    
    # 2. 测试 API-Football
    test_sports_api()
    
    # 3. 测试 DataCollector 集成
    test_data_collector()
    
    # 总结
    print("\n" + "="*60)
    print("📋 测试总结")
    print("="*60)
    print("✅ The-Odds-API: 已配置 (3838a6272cab9b49dac3d9f646fbca4b)")
    print("✅ API-Football: 已配置 (58ce01aadd6863c36e4c86d807233d25)")
    print("\n💡 使用建议:")
    print("   - The-Odds-API: 每日 500 次限额，适合每 6-8 小时运行一次")
    print("   - API-Football: 支持足球/篮球等多种体育项目")
    print("   - 建议每天运行 2-3 次构建，完全在额度范围内")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
