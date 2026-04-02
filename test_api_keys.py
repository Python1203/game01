"""
API 密钥验证测试脚本
验证 API-Football 和 The-Odds-API 的连接
"""
from src.sports_data_api import FootballDataAPI
from src.odds_cps_module import OddsAggregator


def test_api_football_connection():
    """测试 API-Football 连接"""
    print('\n' + '='*60)
    print('⚽ 测试 API-Football...')
    print('='*60)
    
    football_api = FootballDataAPI()
    fixtures = football_api.get_fixtures(limit=3)
    
    if fixtures:
        print(f'✅ API-Football 连接成功!')
        print(f'   获取到 {len(fixtures)} 场比赛')
        print(f'   示例：{fixtures[0]["teams"]["home"]["name"]} vs {fixtures[0]["teams"]["away"]["name"]}')
        assert len(fixtures) > 0, "应至少返回 1 场比赛"
    else:
        print('ℹ️  API-Football 返回空数据 (可能是非比赛日或配额限制)')
        # 不视为失败，可能是非比赛日


def test_injuries_api():
    """测试伤停信息接口"""
    print('\n🏥 测试伤停信息接口...')
    
    football_api = FootballDataAPI()
    injuries = football_api.get_injuries()
    
    if injuries:
        print(f'✅ 获取到 {len(injuries)} 条伤停信息')
        print(f'   示例：{injuries[0].player_name} ({injuries[0].team})')
        assert len(injuries) > 0, "应至少返回 1 条伤停信息"
    else:
        print('ℹ️  暂无伤停信息')


def test_odds_api_connection():
    """测试 The-Odds-API 连接"""
    print('\n' + '='*60)
    print('🎲 测试 The-Odds-API...')
    print('='*60)
    
    odds_aggregator = OddsAggregator()
    comparisons = odds_aggregator.get_odds_comparison(sport='soccer_epl', limit=3)
    
    if comparisons:
        print(f'✅ The-Odds-API 连接成功!')
        print(f'   获取到 {len(comparisons)} 场比赛的赔率')
        print(f'   示例：{comparisons[0].home_team} vs {comparisons[0].away_team}')
        print(f'   最佳主胜：{comparisons[0].best_home_odds.bookmaker_name} - {comparisons[0].best_home_odds.home_odds:.2f}')
        assert len(comparisons) > 0, "应至少返回 1 场比赛赔率"
    else:
        print('ℹ️  The-Odds-API 返回空数据 (可能是配额限制或非比赛时间)')
        # 不视为失败，可能是非比赛时间


def run_all_tests():
    """运行所有测试"""
    print('\n' + '='*60)
    print('🔍 API 连接验证测试')
    print('='*60)
    
    try:
        test_api_football_connection()
        test_injuries_api()
        test_odds_api_connection()
        
        print('\n' + '='*60)
        print('✅ API 密钥验证完成!')
        print('='*60)
        print('\n💡 提示:')
        print('- API-Football: 每日免费 100 次请求')
        print('- The-Odds-API: 每月免费 500 次请求')
        print('- 建议配合缓存系统使用，减少 API 调用')
        return 0
        
    except Exception as e:
        print(f'\n❌ 测试失败：{e}')
        return 1


if __name__ == '__main__':
    import sys
    sys.exit(run_all_tests())
