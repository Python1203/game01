"""
VIP 内容分层与动态赔率系统 - 完整集成测试
测试所有新增模块的功能和数据流
"""
import os
import sys
from datetime import datetime


def test_vip_data_models():
    """测试 VIP 数据模型"""
    print("\n" + "="*60)
    print("📦 测试 VIP 数据模型")
    print("="*60)
    
    from src.vip_data_models import (
        BasicMatchData, InjuryInfo, H2HStats, 
        AIModelPrediction, VIPMatchAnalysis
    )
    
    # 创建基础比赛数据
    basic = BasicMatchData(
        match_id="test_001",
        home_team="Arsenal",
        away_team="Chelsea",
        league="英超",
        commence_time=datetime.now().isoformat(),
        status="scheduled",
        basic_odds={"home": 2.1, "draw": 3.4, "away": 3.5}
    )
    print(f"✓ 创建基础比赛数据：{basic.home_team} vs {basic.away_team}")
    
    # 创建伤停信息
    injury = InjuryInfo(
        player_name="Bukayo Saka",
        team="Arsenal",
        position="forward",
        injury_type="Hamstring injury",
        severity="moderate",
        expected_return="2026-04-15"
    )
    print(f"✓ 创建伤停信息：{injury.player_name}")
    
    # 创建 H2H 统计
    h2h = H2HStats(
        total_matches=10,
        home_wins=4,
        away_wins=3,
        draws=3,
        home_goals=15,
        away_goals=12,
        over_2_5_goals=7,
        under_2_5_goals=3,
        both_scored=6
    )
    print(f"✓ 创建 H2H 统计：共 {h2h.total_matches} 场交锋")
    
    # 创建 AI 预测
    ai_pred = AIModelPrediction(
        model_version="v2.5",
        confidence_level=75.5,
        predicted_outcome="home_win",
        predicted_score="2-1",
        home_win_prob=0.55,
        draw_prob=0.25,
        away_win_prob=0.20,
        recommended_bet="Asian Handicap",
        recommended_pick="Arsenal -0.5",
        value_rating=4.0,
        reasoning="Arsenal 主场作战，且 Chelsea 后防核心伤缺"
    )
    print(f"✓ 创建 AI 预测：置信度 {ai_pred.confidence_level:.1f}%")
    
    # 创建完整的 VIP 分析
    analysis = VIPMatchAnalysis(
        match_id="test_001",
        basic_data=basic,
        injuries=[injury],
        h2h_stats=h2h,
        ai_prediction=ai_pred,
        home_form=["W", "D", "W", "W", "L"],
        away_form=["L", "W", "D", "W", "W"]
    )
    
    print(f"✓ 创建 VIP 分析数据包")
    print(f"  - VIP 内容：{'是' if analysis.is_vip_content() else '否'}")
    print(f"  - 关键洞察：{len(analysis.get_key_insights())} 条")
    
    return analysis


def test_sports_data_api():
    """测试体育赛事数据采集"""
    print("\n" + "="*60)
    print("⚽ 测试 API-Football 数据采集")
    print("="*60)
    
    try:
        from src.sports_data_api import FootballDataAPI
        
        api = FootballDataAPI()
        
        # 1. 获取赛程
        print("\n📅 获取赛程...")
        fixtures = api.get_fixtures(limit=5)
        print(f"✓ 获取到 {len(fixtures)} 场比赛")
        
        if fixtures:
            fixture = fixtures[0]
            print(f"  示例：{fixture['teams']['home']['name']} vs {fixture['teams']['away']['name']}")
        
        # 2. 获取伤停信息
        print("\n🏥 获取伤停信息...")
        injuries = api.get_injuries()
        print(f"✓ 获取到 {len(injuries)} 条伤停")
        
        if injuries:
            injury = injuries[0]
            print(f"  示例：{injury.player_name} ({injury.team}) - {injury.injury_type}")
        
        # 3. 获取球队近况
        print("\n📊 获取球队近况...")
        if fixtures:
            team_id = fixtures[0]['teams']['home']['id']
            form = api.get_team_form(team_id, last=5)
            print(f"✓ 球队近况：{form}")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败：{e}")
        return False


def test_odds_cps_module():
    """测试赔率对比与 CPS 模块"""
    print("\n" + "="*60)
    print("🎲 测试赔率聚合与 CPS 系统")
    print("="*60)
    
    try:
        from src.odds_cps_module import OddsAggregator, GeoAffiliateRecommender, ValueBetFinder
        
        # 1. 赔率聚合
        print("\n📊 测试赔率聚合...")
        aggregator = OddsAggregator()
        comparisons = aggregator.get_odds_comparison(sport="soccer_epl", limit=3)
        print(f"✓ 获取到 {len(comparisons)} 场比赛的赔率对比")
        
        if comparisons:
            comp = comparisons[0]
            print(f"  比赛：{comp.home_team} vs {comp.away_team}")
            print(f"  最佳主胜：{comp.best_home_odds.bookmaker_name} - {comp.best_home_odds.home_odds:.2f}")
            print(f"  最佳客胜：{comp.best_away_odds.bookmaker_name} - {comp.best_away_odds.away_odds:.2f}")
        
        # 2. 区域化推荐
        print("\n🌍 测试区域化推荐...")
        recommender = GeoAffiliateRecommender()
        us_recs = recommender.recommend_for_region("US")
        uk_recs = recommender.recommend_for_region("UK")
        print(f"✓ 美国用户推荐：{', '.join(us_recs[:3])}")
        print(f"✓ 英国用户推荐：{', '.join(uk_recs[:3])}")
        
        # 3. 价值注发现
        print("\n💎 测试价值注发现...")
        finder = ValueBetFinder()
        if comparisons:
            sample_predictions = {"home": 0.55, "draw": 0.25, "away": 0.20}
            value_bets = finder.find_value_bets(comparisons[0], sample_predictions)
            
            if value_bets:
                print(f"✓ 发现 {len(value_bets)} 个价值注机会:")
                for bet in value_bets[:2]:
                    print(f"  - {bet.bet_type}: {bet.bookmaker} 赔率 {bet.odds:.2f} (优势 {bet.edge*100:.1f}%)")
            else:
                print(f"ℹ️ 暂无符合条件的价值注")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败：{e}")
        return False


def test_cache_manager():
    """测试缓存管理器"""
    print("\n" + "="*60)
    print("💾 测试智能缓存系统")
    print("="*60)
    
    try:
        from src.cache_manager import SmartCache, DataPrefetcher
        
        # 1. 基本缓存操作
        print("\n📦 测试缓存读写...")
        cache = SmartCache()
        
        # 写入缓存
        test_data = {"odds": [1.95, 2.10, 3.50], "timestamp": datetime.now().isoformat()}
        cache.set("test:odds:001", test_data, "odds")
        print("✓ 写入缓存数据")
        
        # 读取缓存
        cached = cache.get("test:odds:001")
        print(f"✓ 读取缓存：{cached is not None}")
        
        # 统计信息
        stats = cache.get_stats()
        print(f"✓ 缓存统计：{stats['total_entries']} 条目，{stats['total_size_mb']:.2f} MB")
        
        # 2. 预取器
        print("\n🔄 测试数据预取...")
        prefetcher = DataPrefetcher(cache)
        # 这里需要真实的 data_collector，暂时跳过
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败：{e}")
        return False


def test_vip_page_builder():
    """测试 VIP 页面构建器"""
    print("\n" + "="*60)
    print("🎨 测试 VIP 页面构建器")
    print("="*60)
    
    try:
        from src.vip_page_builder import VIPPageBuilder
        
        # 先创建测试数据
        analysis = test_vip_data_models()
        
        builder = VIPPageBuilder(output_dir="./public/test-vip")
        
        # 为不同等级用户构建页面
        for tier in ["free", "vip_basic", "vip_premium"]:
            print(f"\n📄 为 {tier.upper()} 用户生成页面...")
            filepath = builder.build_vip_match_page(analysis, user_tier=tier)
            print(f"✓ 生成页面：{filepath}")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败：{e}")
        return False


def run_all_tests():
    """运行所有测试"""
    print("\n" + "="*60)
    print("🚀 VIP 内容分层与动态赔率系统 - 完整测试")
    print("="*60)
    print(f"⏰ 测试时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    results = {}
    
    # 1. 测试数据模型
    analysis = test_vip_data_models()
    results["data_models"] = True
    
    # 2. 测试数据采集
    results["sports_api"] = test_sports_data_api()
    
    # 3. 测试赔率 CPS
    results["odds_cps"] = test_odds_cps_module()
    
    # 4. 测试缓存管理
    results["cache"] = test_cache_manager()
    
    # 5. 测试页面构建
    results["page_builder"] = test_vip_page_builder()
    
    # 总结
    print("\n" + "="*60)
    print("📊 测试结果汇总")
    print("="*60)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    print(f"\n✅ 通过：{passed}/{total} 个模块")
    
    for module, result in results.items():
        icon = "✅" if result else "❌"
        print(f"  {icon} {module}: {'通过' if result else '失败'}")
    
    if passed == total:
        print("\n🎉 所有测试通过！系统已准备就绪。")
        return 0
    else:
        print("\n⚠️ 部分测试失败，请检查相关模块。")
        return 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
