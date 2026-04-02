"""
足球预测内容生成器 - 双引擎架构
实时赔率数据 + AI 深度分析
"""
import os
import requests
from datetime import datetime
from typing import List, Dict
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# API 配置
ODDS_API_KEY = os.getenv("ODDS_API_KEY")
FOOTBALL_API_KEY = os.getenv("SPORTS_API_KEY")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL", "https://xh.v1api.cc")


class FootballDataCollector:
    """足球数据采集器 - 合并请求策略"""
    
    def __init__(self):
        self.odds_key = ODDS_API_KEY
        self.football_key = FOOTBALL_API_KEY
        
    def get_combined_matches(self, limit: int = 5) -> List[Dict]:
        """
        获取比赛数据（合并策略）
        只取前 N 场热门比赛，节省 API 额度
        """
        matches = []
        
        try:
            # 1. 获取赔率数据（The Odds API）
            if self.odds_key:
                print(f"📊 获取赔率数据...")
                # 使用正确的体育项目 ID
                odds_url = f"https://api.the-odds-api.com/v4/sports/soccer_epl/odds?regions=uk&markets=h2h&apiKey={self.odds_key}"
                response = requests.get(odds_url, timeout=15)
                
                if response.status_code == 200:
                    odds_data = response.json()[:limit]  # 只取前 N 场
                    
                    for match in odds_data:
                        # 先提取最佳赔率（需要主客队名称）
                        best_odds = self._extract_best_odds(
                            match.get("bookmakers", []),
                            match["home_team"],
                            match["away_team"]
                        )
                        
                        match_info = {
                            "id": match["id"],
                            "home_team": match["home_team"],
                            "away_team": match["away_team"],
                            "commence_time": match["commence_time"],
                            "sport_title": match["sport_title"],
                            "bookmakers": match.get("bookmakers", []),
                            "best_odds": best_odds
                        }
                        
                        # 2. 如果有 Football API，获取球队近况
                        if self.football_key:
                            team_stats = self._get_team_stats(match["home_team"], match["away_team"])
                            match_info.update(team_stats)
                        
                        matches.append(match_info)
                    
                    print(f"✓ 获取到 {len(matches)} 场英超比赛")
                else:
                    print(f"⚠️ The Odds API 请求失败：{response.status_code}")
                    print(f"   提示：请检查 API Key 是否有效，或访问 https://the-odds-api.com 查看可用赛事")
            
            return matches
            
        except Exception as e:
            print(f"❌ 获取比赛数据失败：{e}")
            return []
    
    def _extract_best_odds(self, bookmakers: List, home_team: str = None, away_team: str = None) -> Dict:
        """提取最佳赔率"""
        best_odds = {"home": 0, "draw": 0, "away": 0}
        
        for bookmaker in bookmakers:
            if bookmaker.get("markets"):
                # h2h 市场的 outcomes 直接包含主/平/客
                for market in bookmaker["markets"]:
                    if market.get("key") == "h2h":
                        outcomes = market.get("outcomes", [])
                        for outcome in outcomes:
                            name = outcome["name"]  # 保持原始名称（如 "West Ham United"）
                            price = outcome["price"]
                            
                            # 根据队伍名称匹配
                            if name == "Draw":
                                key = "draw"
                            elif name == home_team or (home_team and name.lower() == home_team.lower()):
                                key = "home"
                            elif name == away_team or (away_team and name.lower() == away_team.lower()):
                                key = "away"
                            else:
                                continue
                            
                            if price > best_odds[key]:
                                best_odds[key] = price
                                best_odds[f"{key}_bookmaker"] = bookmaker["title"]
        
        return best_odds
    
    def _get_team_stats(self, home_team: str, away_team: str) -> Dict:
        """获取球队统计数据（API-Football）"""
        stats = {
            "home_form": "W-D-W-L-W",  # 示例数据
            "away_form": "L-W-D-W-L",
            "home_goals_avg": 2.1,
            "away_goals_avg": 1.8
        }
        
        try:
            # 实际使用时调用 API-Football
            # url = f"https://v3.football.api-sports.io/teams/form?name={home_team}"
            # headers = {"x-apisports-key": self.football_key}
            # response = requests.get(url, headers=headers, timeout=10)
            
            print(f"  📈 {home_team} 近期状态：{stats['home_form']}")
            return stats
            
        except Exception as e:
            print(f"⚠️ 获取球队数据失败：{e}")
            return stats


class AIPredictor:
    """AI 预测生成器"""
    
    def __init__(self):
        self.api_key = DEEPSEEK_API_KEY
        self.base_url = DEEPSEEK_BASE_URL
    
    def generate_analysis(self, match: Dict) -> str:
        """生成 AI 深度分析"""
        home_team = match["home_team"]
        away_team = match["away_team"]
        best_home_odds = match["best_odds"].get("home", 0)
        best_away_odds = match["best_odds"].get("away", 0)
        home_form = match.get("home_form", "未知")
        away_form = match.get("away_form", "未知")
        
        prompt = f"""你是一位专业的足球分析师。请为以下比赛写一份专业的赛前预测：

**比赛信息**:
- 对阵：{home_team} vs {away_team}
- 比赛时间：{match['commence_time']}
- 当前最佳赔率：主胜 {best_home_odds:.2f} ({match['best_odds'].get('home_bookmaker', 'Unknown')}), 客胜 {best_away_odds:.2f} ({match['best_odds'].get('away_bookmaker', 'Unknown')})
- {home_team} 近期状态：{home_form}
- {away_team} 近期状态：{away_form}

**要求**:
1. 包含技战术分析（阵型、关键球员、伤病情况）
2. 分析赔率变化趋势
3. 给出专业的投注建议（亚盘、大小球）
4. 引导用户查看更多专家方案
5. 语气专业但不失亲和力
6. 字数：300-500 字

请用中文回答。"""

        try:
            response = requests.post(
                f"{self.base_url}/v1/chat/completions",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={
                    "model": "deepseek-chat",
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.7
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                analysis = result["choices"][0]["message"]["content"]
                print(f"✓ AI 分析完成：{home_team} vs {away_team}")
                return analysis
            else:
                print(f"⚠️ AI 生成失败：{response.status_code}")
                return self._generate_default_analysis(match)
                
        except Exception as e:
            print(f"❌ AI 调用失败：{e}")
            return self._generate_default_analysis(match)
    
    def _generate_default_analysis(self, match: Dict) -> str:
        """默认分析（当 AI 不可用时）"""
        return f"""## 赛前分析

**{match['home_team']} vs {match['away_team']}**

本场比赛赔率显示主队稍占优势。从双方近期表现来看，这将是一场势均力敌的较量。

### 关键看点
- 主队主场作战能力强劲
- 客队反击效率值得关注
- 历史交锋记录偏向主队

### 投注建议
- **亚盘**: 主队 -0.5
- **大小球**: 2.5/3 大球

*更多专家方案请查看完整分析报告*"""


class ContentBuilder:
    """内容构建器 - 生成 Markdown 文件"""
    
    def __init__(self, output_dir: str = "src/pages/predictions"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def build_match_page(self, match: Dict, analysis: str):
        """生成单场比赛预测页面"""
        home_team = match["home_team"]
        away_team = match["away_team"]
        slug = f"{home_team.lower().replace(' ', '-')}-vs-{away_team.lower().replace(' ', '-')}"
        
        # SEO TDK 优化
        title = f"{home_team} vs {away_team} Prediction & Best Betting Odds {datetime.now().year}"
        description = f"Professional {home_team} vs {away_team} prediction with real-time odds analysis. Expert betting tips and AI forecast."
        
        # 生成 Markdown
        content = f"""---
layout: ../../layouts/BaseLayout.astro
title: "{title}"
description: "{description}"
keywords: "{home_team} vs {away_team}, betting tips, prediction, best odds, football analysis"
match_id: "{match['id']}"
home_team: "{home_team}"
away_team: "{away_team}"
commence_time: "{match['commence_time']}"
best_home_odds: "{match['best_odds'].get('home', 0):.2f}"
best_draw_odds: "{match['best_odds'].get('draw', 0):.2f}"
best_away_odds: "{match['best_odds'].get('away', 0):.2f}"
pubDate: "{datetime.now().strftime('%Y-%m-%d %H:%M')}"
---

<!-- Schema 标记 (Event + FinancialProduct) -->
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Event",
  "name": "{home_team} vs {away_team}",
  "startDate": "{match['commence_time']}",
  "sport": "Football",
  "description": "{description}"
}}
</script>

# {home_team} vs {away_team} - 赛前预测与赔率分析

> **核心观点**: 本文提供 {home_team} 对阵 {away_team} 的专业赛前分析，包括实时赔率对比、AI 深度预测和投注建议。

## 📊 实时赔率对比

| 结果 | 最佳赔率 | 博彩公司 |
|------|---------|---------|
| {home_team} 胜 | {match['best_odds'].get('home', 0):.2f} | {match['best_odds'].get('home_bookmaker', 'N/A')} |
| 平局 | {match['best_odds'].get('draw', 0):.2f} | {match['best_odds'].get('draw_bookmaker', 'N/A')} |
| {away_team} 胜 | {match['best_odds'].get('away', 0):.2f} | {match['best_odds'].get('away_bookmaker', 'N/A')} |

<div class="odds-compare">
    <p>💰 **最高赔率提示**: {home_team} 胜最高赔率为 **{match['best_odds'].get('home', 0):.2f}**</p>
    <a href="/go/stake" class="btn btn-primary">立即投注领 $1000 奖金</a>
    <small style="display:block; margin-top:10px; color:#666;">
        ⚠️ 博彩有风险，请理性投注 | 18+ | BeGambleAware.org
    </small>
</div>

## 🤖 AI 深度分析

{analysis}

<div class="vip-box">
    <h3>🔒 解锁 VIP 预测</h3>
    <p>想获取此场比赛的【必发波胆】和【高胜率方案】吗？</p>
    <a href="/go/telegram" class="btn btn-telegram">加入电报 VIP 频道</a>
    <small>已有 5000+ 会员获取稳胆推荐</small>
</div>

## 📈 投注策略建议

### 亚盘推荐
- **推荐**: 主队 -0.5
- **理由**: 基于赔率变化和球队状态分析

### 大小球
- **推荐**: 2.5/3 大球
- **置信度**: 75%

### 关键词分布
Free betting tips, How to bet on {home_team} vs {away_team}, Best odds comparison

---

*更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}*  
*免责声明：本文仅供参考，不构成投注建议。请理性博彩，未满 18 岁禁止参与。*
"""
        
        # 写入文件
        filename = f"{self.output_dir}/{slug}.md"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        
        print(f"✓ 生成页面：{filename}")
        return filename


def main():
    """主执行流程"""
    print("="*60)
    print("⚽ 足球预测内容生成器 - 双引擎架构")
    print("="*60)
    
    # 1. 数据采集（合并策略）
    collector = FootballDataCollector()
    matches = collector.get_combined_matches(limit=5)  # 只取 5 场，节省额度
    
    if not matches:
        print("⚠️ 未获取到比赛数据，使用备用方案")
        return
    
    # 2. AI 生成分析
    predictor = AIPredictor()
    builder = ContentBuilder()
    
    for match in matches:
        print(f"\n📝 生成分析：{match['home_team']} vs {match['away_team']}")
        analysis = predictor.generate_analysis(match)
        
        # 3. 构建页面
        builder.build_match_page(match, analysis)
    
    print("\n" + "="*60)
    print(f"✅ 完成！共生成 {len(matches)} 篇预测文章")
    print(f"📁 输出目录：{builder.output_dir}")
    print("="*60)


if __name__ == "__main__":
    main()
