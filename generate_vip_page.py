#!/usr/bin/env python3
"""
生成 Manchester City vs Liverpool 的 VIP 分析页面
"""
import sys
import os
from datetime import datetime, timedelta

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.vip_page_builder import VIPPageBuilder
from src.vip_data_models import (
    BasicMatchData, 
    VIPMatchAnalysis, 
    InjuryInfo,
    H2HStats,
    AIModelPrediction
)


def generate_man_city_vs_liverpool_page():
    """生成曼城 vs 利物浦的 VIP 分析页面"""
    
    print("\n🎨 开始生成 Manchester City vs Liverpool VIP 页面...\n")
    
    # 1. 创建基础比赛数据
    basic_data = BasicMatchData(
        match_id="epl_2026_mci_liv",
        home_team="Manchester City",
        away_team="Liverpool",
        league="英超",
        commence_time=(datetime.now() + timedelta(days=3)).replace(hour=23, minute=30).isoformat(),
        status="scheduled",
        basic_odds={"home": 2.10, "draw": 3.60, "away": 3.40}
    )
    
    # 2. 创建伤停信息 (VIP_BASIC 内容)
    injuries = [
        InjuryInfo(
            player_name="Kevin De Bruyne",
            team="Manchester City",
            position="midfielder",
            injury_type="腿筋拉伤",
            expected_return="2026-04-10",
            severity="moderate"
        ),
        InjuryInfo(
            player_name="Erling Haaland",
            team="Manchester City",
            position="forward",
            injury_type="脚踝扭伤",
            expected_return=None,
            severity="severe",
            is_suspended=False
        ),
        InjuryInfo(
            player_name="Mohamed Salah",
            team="Liverpool",
            position="forward",
            injury_type="肌肉疲劳",
            expected_return="2026-04-05",
            severity="minor"
        ),
        InjuryInfo(
            player_name="Virgil van Dijk",
            team="Liverpool",
            position="defender",
            injury_type="累积黄牌停赛",
            expected_return=None,
            severity="minor",
            is_suspended=True,
            suspension_reason="累积黄牌"
        )
    ]
    
    # 3. 创建历史交锋统计 (VIP_PREMIUM 内容)
    h2h_stats = H2HStats(
        total_matches=10,
        home_wins=4,
        away_wins=4,
        draws=2,
        home_goals=15,
        away_goals=16,
        over_2_5_goals=7,
        under_2_5_goals=3,
        both_scored=8,
        recent_matches=[
            {"date": "2025-12-01", "home": "Liverpool", "away": "Manchester City", "score": "2-0"},
            {"date": "2025-08-10", "home": "Manchester City", "away": "Liverpool", "score": "1-1"},
            {"date": "2025-04-05", "home": "Liverpool", "away": "Manchester City", "score": "3-2"},
            {"date": "2024-11-25", "home": "Manchester City", "away": "Liverpool", "score": "4-1"},
            {"date": "2024-03-10", "home": "Liverpool", "away": "Manchester City", "score": "1-1"}
        ],
        home_advantage={
            "city_home_record": "W3 D1 L1",
            "liverpool_away_record": "W2 D1 L2"
        }
    )
    
    # 4. 创建 AI 预测 (VIP_PREMIUM 内容)
    ai_prediction = AIModelPrediction(
        model_version="v3.2.1",
        confidence_level=75.5,
        predicted_outcome="draw",
        predicted_score="2-2",
        home_win_prob=38.5,
        draw_prob=28.0,
        away_win_prob=33.5,
        over_2_5_prob=68.2,
        under_2_5_prob=31.8,
        btts_prob=72.5,
        recommended_bet="Over/Under",
        recommended_pick="大 2.5 球",
        value_rating=4.0,
        risk_level="medium",
        reasoning="双方进攻火力强劲，但后防均有关键球员缺阵。考虑到 De Bruyne 和 Van Dijk 的缺席，比赛可能会更加开放。历史交锋显示最近 10 场有 7 场打出大球，且双方进球概率高达 72.5%。预计这将是一场进球大战，推荐投注大球。"
    )
    
    # 5. 创建球队近况
    home_form = ["W", "W", "D", "W", "L"]  # 曼城近 5 场
    away_form = ["W", "W", "W", "D", "W"]  # 利物浦近 5 场
    
    # 6. 创建完整的 VIP 分析对象
    analysis = VIPMatchAnalysis(
        match_id="epl_2026_mci_liv",
        basic_data=basic_data,
        injuries=injuries,
        h2h_stats=h2h_stats,
        ai_prediction=ai_prediction,
        home_form=home_form,
        away_form=away_form,
        advanced_stats={
            "expected_goals": {"home": 2.1, "away": 1.9},
            "possession_avg": {"home": 62, "away": 58},
            "shots_per_game": {"home": 18.5, "away": 16.2}
        }
    )
    
    # 7. 构建页面
    builder = VIPPageBuilder(output_dir="./public")
    
    # 生成不同用户等级的页面
    tiers = ["free", "vip_basic", "vip_premium"]
    
    for tier in tiers:
        filepath = builder.build_vip_match_page(analysis, user_tier=tier)
        print(f"✓ 生成 {tier.upper()} 用户页面：{filepath}")
    
    # 返回主页面路径（free 版本）
    main_filepath = f"./public/vip/manchester city-vs-liverpool/index.html"
    print(f"\n✅ VIP 页面生成完成！")
    print(f"📁 主页面位置：{main_filepath}")
    print(f"🔑 访问权限：")
    print(f"   - Free 用户：查看基础信息 + 锁定提示")
    print(f"   - VIP Basic：解锁伤停信息")
    print(f"   - VIP Premium：解锁全部内容包括 H2H 和 AI 预测")
    
    return main_filepath


if __name__ == "__main__":
    try:
        filepath = generate_man_city_vs_liverpool_page()
        print(f"\n✨ 成功生成 Manchester City vs Liverpool VIP 分析页面\n")
    except Exception as e:
        print(f"\n❌ 生成失败：{e}\n")
        import traceback
        traceback.print_exc()
        sys.exit(1)
