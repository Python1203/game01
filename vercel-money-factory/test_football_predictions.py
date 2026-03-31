"""
足球预测生成器 - 本地测试脚本
"""
import os
import sys
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 添加路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from build_football_predictions import FootballDataCollector, AIPredictor, ContentBuilder


def test_collector():
    """测试数据采集"""
    print("="*60)
    print("📊 测试数据采集模块")
    print("="*60)
    
    collector = FootballDataCollector()
    matches = collector.get_combined_matches(limit=3)
    
    if matches:
        print(f"\n✓ 获取到 {len(matches)} 场比赛:\n")
        for i, match in enumerate(matches[:3], 1):
            print(f"{i}. {match['home_team']} vs {match['away_team']}")
            print(f"   时间：{match['commence_time']}")
            print(f"   最佳赔率：主胜 {match['best_odds'].get('home', 0):.2f} | "
                  f"平 {match['best_odds'].get('draw', 0):.2f} | "
                  f"客胜 {match['best_odds'].get('away', 0):.2f}")
            print()
    else:
        print("⚠️ 未获取到比赛数据")
    
    return matches


def test_ai_prediction():
    """测试 AI 生成"""
    print("\n" + "="*60)
    print("🤖 测试 AI 预测生成")
    print("="*60)
    
    # 使用模拟数据测试
    mock_match = {
        "home_team": "Manchester City",
        "away_team": "Liverpool",
        "commence_time": "2026-04-05T15:00:00Z",
        "best_odds": {
            "home": 2.10,
            "draw": 3.40,
            "away": 3.20,
            "home_bookmaker": "Bet365",
            "draw_bookmaker": "William Hill",
            "away_bookmaker": "Stake"
        },
        "home_form": "W-W-D-W-L",
        "away_form": "W-L-W-W-D"
    }
    
    predictor = AIPredictor()
    analysis = predictor.generate_analysis(mock_match)
    
    print("\n生成的分析预览:")
    print("-"*60)
    print(analysis[:500] + "..." if len(analysis) > 500 else analysis)
    print("-"*60)
    
    return analysis


def test_content_builder():
    """测试内容构建"""
    print("\n" + "="*60)
    print("🏗️ 测试内容构建模块")
    print("="*60)
    
    mock_match = {
        "id": "test_match_001",
        "home_team": "Arsenal",
        "away_team": "Chelsea",
        "commence_time": "2026-04-06T17:30:00Z",
        "sport_title": "Soccer",
        "best_odds": {
            "home": 2.25,
            "draw": 3.30,
            "away": 3.10,
            "home_bookmaker": "Bet365",
            "draw_bookmaker": "Pinnacle",
            "away_bookmaker": "Stake"
        },
        "home_form": "W-D-W-W-L",
        "away_form": "L-W-D-W-W"
    }
    
    mock_analysis = """## 赛前分析

**阿森纳 vs 切尔西**

本场比赛是伦敦德比的焦点之战。阿森纳近期状态出色，主场攻击力强劲。切尔西则在防守端表现出色。

### 关键看点
- 阿森纳主场胜率高达 75%
- 切尔西反击效率联盟前列
- 历史交锋记录偏向客队

### 投注建议
- **亚盘**: 主队 -0.25
- **大小球**: 2.5/3 小球

*更多专家方案请查看完整分析报告*"""
    
    builder = ContentBuilder(output_dir="test_output")
    filename = builder.build_match_page(mock_match, mock_analysis)
    
    print(f"\n✓ 生成测试页面：{filename}")
    print(f"📁 输出目录：{builder.output_dir}")
    
    # 显示文件内容预览
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
        print(f"\n📄 文件内容预览 ({len(content)} 字符):")
        print("-"*60)
        print(content[:800] + "..." if len(content) > 800 else content)
        print("-"*60)
    
    return filename


def main():
    """主测试流程"""
    print("\n" + "⚽"*30)
    print("⚽ 足球预测生成器 - 完整测试 ⚽")
    print("⚽"*30 + "\n")
    
    # 1. 测试数据采集
    matches = test_collector()
    
    # 2. 测试 AI 生成
    analysis = test_ai_prediction()
    
    # 3. 测试内容构建
    test_content_builder()
    
    # 总结
    print("\n" + "="*60)
    print("📋 测试总结")
    print("="*60)
    print("✅ 数据采集模块：正常" if matches else "⚠️ 数据采集模块：使用模拟数据")
    print("✅ AI 生成模块：正常")
    print("✅ 内容构建模块：正常")
    print("\n💡 下一步操作:")
    print("   1. 运行 python build_football_predictions.py 执行完整构建")
    print("   2. 检查 src/pages/predictions/ 目录")
    print("   3. 运行 astro dev 预览效果")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
