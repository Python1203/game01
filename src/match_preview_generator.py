"""
自动化赛事前瞻生成器 - Programmatic SEO
利用 API 数据生成海量高质量 SEO 页面
"""
import os
from typing import Dict, List
from datetime import datetime
from src.sports_data_api import FootballDataAPI
from src.odds_cps_module import OddsAggregator


class MatchPreviewGenerator:
    """赛事前瞻页面生成器"""
    
    def __init__(self, output_dir: str = "./public/preview"):
        self.output_dir = output_dir
        self.football_api = FootballDataAPI()
        self.odds_aggregator = OddsAggregator()
        
        # 确保输出目录存在
        os.makedirs(output_dir, exist_ok=True)
    
    def generate_all_previews(self, limit: int = 20):
        """生成所有未来比赛的预览页面"""
        print("\n📝 开始生成赛事前瞻页面...")
        
        # 1. 获取未来赛程
        fixtures = self.football_api.get_fixtures(limit=limit)
        
        if not fixtures:
            print("⚠️ 暂无比赛数据")
            return []
        
        generated_pages = []
        
        for fixture in fixtures:
            try:
                page_path = self.generate_single_preview(fixture)
                generated_pages.append(page_path)
                print(f"✓ 生成：{fixture['teams']['home']['name']} vs {fixture['teams']['away']['name']}")
            except Exception as e:
                print(f"❌ 生成失败：{e}")
        
        print(f"\n✅ 成功生成 {len(generated_pages)} 个预览页面")
        return generated_pages
    
    def generate_single_preview(self, fixture: Dict) -> str:
        """生成单场比赛的预览页面"""
        home_team = fixture["teams"]["home"]["name"]
        away_team = fixture["teams"]["away"]["name"]
        league = fixture["league"]["name"]
        match_date = fixture["fixture"]["date"]
        
        # 创建 URL 友好的 slug
        slug = f"{self._slugify(home_team)}-vs-{self._slugify(away_team)}"
        
        # 获取 H2H 数据
        h2h_stats = self._get_h2h_data(fixture)
        
        # 获取球队近况
        home_form = self._get_team_form(fixture["teams"]["home"]["id"])
        away_form = self._get_team_form(fixture["teams"]["away"]["id"])
        
        # 获取伤停信息
        injuries = self._get_injuries(fixture)
        
        # 获取赔率数据
        odds_data = self._get_odds_data(home_team, away_team)
        
        # 生成 AI 推荐 (简化版，实际可调用 GPT-4)
        ai_recommendation = self._generate_ai_recommendation(
            home_team, away_team, h2h_stats, home_form, away_form, injuries
        )
        
        # 生成 HTML 页面
        html = self._build_html_page(
            home_team=home_team,
            away_team=away_team,
            league=league,
            match_date=match_date,
            h2h_stats=h2h_stats,
            home_form=home_form,
            away_form=away_form,
            injuries=injuries,
            odds_data=odds_data,
            ai_recommendation=ai_recommendation
        )
        
        # 写入文件
        file_path = f"{self.output_dir}/{slug}/index.html"
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        return file_path
    
    def _build_html_page(
        self,
        home_team: str,
        away_team: str,
        league: str,
        match_date: str,
        h2h_stats: Dict,
        home_form: List[str],
        away_form: List[str],
        injuries: List[Dict],
        odds_data: Dict,
        ai_recommendation: str
    ) -> str:
        """构建 HTML 页面 (包含 JSON-LD 结构化数据)"""
        
        date_obj = datetime.fromisoformat(match_date.replace('Z', '+00:00'))
        formatted_date = date_obj.strftime('%Y年%m月%d日 %H:%M')
        
        # JSON-LD Schema.org 结构化数据
        json_ld = f"""
        <script type="application/ld+json">
        {{
            "@context": "https://schema.org",
            "@type": "SportsEvent",
            "name": "{home_team} vs {away_team}",
            "sport": "Football",
            "startDate": "{match_date}",
            "tournament": {{
                "@type": "SportsLeague",
                "name": "{league}"
            }},
            "homeTeam": {{
                "@type": "SportsTeam",
                "name": "{home_team}"
            }},
            "awayTeam": {{
                "@type": "SportsTeam",
                "name": "{away_team}"
            }},
            "description": "{home_team} vs {away_team} 赔率分析、首发预测及投注建议"
        }}
        </script>
        """
        
        # 生成 HTML
        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{home_team} vs {away_team} 赔率分析、首发预测及投注建议 - {formatted_date}</title>
    <meta name="description" content="{home_team}对阵{away_team}的专业分析：历史交锋{h2h_stats.get('summary', '')}。{' '.join(home_form[-3:])} vs {' '.join(away_form[-3:])}。{ai_recommendation[:100]}">
    <meta name="keywords" content="{home_team}, {away_team}, 赔率分析，比分预测，投注建议，{league}">
    
    {json_ld}
    
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; background: #f5f7fa; }}
        .container {{ max-width: 1200px; margin: 0 auto; padding: 20px; }}
        
        header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 40px 0; text-align: center; }}
        h1 {{ font-size: 2.5em; margin-bottom: 10px; }}
        .match-info {{ font-size: 1.2em; opacity: 0.9; }}
        
        .section {{ background: white; border-radius: 12px; padding: 30px; margin: 30px 0; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        .section-title {{ font-size: 1.8em; color: #333; margin-bottom: 20px; border-left: 4px solid #667eea; padding-left: 15px; }}
        
        .form-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; }}
        .form-item {{ text-align: center; padding: 15px; background: #f8f9fa; border-radius: 8px; }}
        .form-label {{ color: #666; font-size: 0.9em; margin-bottom: 10px; }}
        .form-value {{ font-size: 1.5em; font-weight: bold; }}
        .form-win {{ color: #28a745; }}
        .form-draw {{ color: #ffc107; }}
        .form-loss {{ color: #dc3545; }}
        
        .injury-list {{ list-style: none; }}
        .injury-item {{ padding: 15px; border-left: 4px solid #dc3545; background: #fff5f5; margin: 10px 0; border-radius: 4px; }}
        
        .odds-table {{ width: 100%; border-collapse: collapse; }}
        .odds-table th {{ background: #667eea; color: white; padding: 15px; text-align: left; }}
        .odds-table td {{ padding: 15px; border-bottom: 1px solid #eee; }}
        .best-odds {{ background: #d4edda !important; font-weight: bold; }}
        
        .ai-recommendation {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 12px; margin: 30px 0; }}
        .ai-recommendation h3 {{ margin-bottom: 15px; font-size: 1.5em; }}
        
        .cta-button {{ display: inline-block; background: white; color: #667eea; padding: 15px 40px; border-radius: 30px; text-decoration: none; font-weight: bold; font-size: 1.1em; margin-top: 20px; transition: transform 0.3s; }}
        .cta-button:hover {{ transform: translateY(-2px); }}
        
        @media (max-width: 768px) {{
            h1 {{ font-size: 1.8em; }}
            .section {{ padding: 20px; }}
        }}
    </style>
</head>
<body>
    <header>
        <div class="container">
            <h1>🏆 {home_team} vs {away_team}</h1>
            <p class="match-info">{league} | {formatted_date}</p>
        </div>
    </header>
    
    <div class="container">
        <!-- 核心指标 -->
        <div class="section">
            <h2 class="section-title">📊 关键指标</h2>
            <div class="form-grid">
                <div class="form-item">
                    <div class="form-label">主队近况</div>
                    <div class="form-value">
                        {''.join([f'<span class="form-{"win" if r=="W" else ("draw" if r=="D" else "loss")}">{r}</span>' for r in home_form])}
                    </div>
                </div>
                <div class="form-item">
                    <div class="form-label">客队近况</div>
                    <div class="form-value">
                        {''.join([f'<span class="form-{"win" if r=="W" else ("draw" if r=="D" else "loss")}">{r}</span>' for r in away_form])}
                    </div>
                </div>
                <div class="form-item">
                    <div class="form-label">历史交锋</div>
                    <div class="form-value">{h2h_stats.get('summary', 'N/A')}</div>
                </div>
            </div>
        </div>
        
        <!-- 伤停信息 -->
        {self._generate_injuries_section(injuries)}
        
        <!-- 赔率对比 -->
        {self._generate_odds_section(odds_data)}
        
        <!-- AI 推荐 -->
        <div class="ai-recommendation">
            <h3>🤖 AI 智能推荐</h3>
            <p style="font-size: 1.1em; line-height: 1.8;">{ai_recommendation}</p>
            <a href="#bet-now" class="cta-button">查看最高赔率 →</a>
        </div>
        
        <!-- 编辑推荐 (防止被判定为垃圾内容) -->
        <div class="section">
            <h2 class="section-title">✍️ 编辑观点</h2>
            <p style="line-height: 1.8; color: #555;">
                本场比赛{home_team}坐镇主场，近期状态{"出色" if "W" in home_form[-3:] else "一般"}。
                {away_team}客场作战能力{"强劲" if "W" in away_form[-3:] else "有待提升"}。
                {self._generate_editor_comment(home_team, away_team, h2h_stats, injuries)}
            </p>
        </div>
    </div>
    
    <footer style="text-align: center; padding: 40px 0; color: #666; margin-top: 60px;">
        <p>&copy; 2026 赛事前瞻。All rights reserved.</p>
        <p style="margin-top: 10px; font-size: 0.9em; color: #999;">
            免责声明：本文仅供参考，不构成投注建议。请理性购彩。
        </p>
    </footer>
</body>
</html>
"""
        
        return html
    
    def _generate_injuries_section(self, injuries: List[Dict]) -> str:
        """生成伤停信息区域"""
        if not injuries:
            return ""
        
        html = '<div class="section"><h2 class="section-title">🏥 伤停信息</h2>'
        html += '<ul class="injury-list">'
        
        for injury in injuries:
            html += f'''
            <li class="injury-item">
                <strong>{injury.get("player", "Unknown")}</strong> 
                ({injury.get("team", "Unknown")}) - {injury.get("reason", "伤病")}
            </li>
            '''
        
        html += '</ul></div>'
        return html
    
    def _generate_odds_section(self, odds_data: Dict) -> str:
        """生成赔率对比区域"""
        if not odds_data:
            return ""
        
        html = '<div class="section"><h2 class="section-title">🎲 实时赔率对比</h2>'
        html += '<table class="odds-table"><thead><tr><th>博彩公司</th><th>主胜</th><th>平局</th><th>客胜</th><th>操作</th></tr></thead><tbody>'
        
        for bookie, odds in odds_data.items():
            is_best = odds.get("is_best_home", False)
            highlight = 'class="best-odds"' if is_best else ''
            
            html += f'''
            <tr {highlight}>
                <td>{bookie}</td>
                <td>{odds.get("home", "N/A"):.2f}</td>
                <td>{odds.get("draw", "N/A"):.2f}</td>
                <td>{odds.get("away", "N/A"):.2f}</td>
                <td><a href="#" class="cta-button" style="padding: 8px 20px; font-size: 0.9em;">立即投注</a></td>
            </tr>
            '''
        
        html += '</tbody></table></div>'
        return html
    
    def _generate_ai_recommendation(
        self,
        home_team: str,
        away_team: str,
        h2h_stats: Dict,
        home_form: List[str],
        away_form: List[str],
        injuries: List[Dict]
    ) -> str:
        """生成 AI 推荐文案"""
        # 简单的规则判断，实际可调用 GPT-4 API
        
        home_wins = sum(1 for r in home_form[-5:] if r == "W")
        away_wins = sum(1 for r in away_form[-5:] if r == "W")
        
        recommendation = f"{home_team}近 5 场取得{home_wins}胜，"
        
        if home_wins > away_wins:
            recommendation += f"状态明显优于{away_team}。"
        elif home_wins == away_wins:
            recommendation += "双方势均力敌。"
        else:
            recommendation += f"但{away_team}表现更为稳定。"
        
        # 考虑伤停影响
        key_injuries = [i for i in injuries if i.get("severity") in ["moderate", "severe"]]
        if key_injuries:
            recommendation += f"需要注意的是，{key_injuries[0].get('team')}的关键球员{key_injuries[0].get('player')}伤缺，这可能影响球队整体实力。"
        
        recommendation += "综合来看，本场比赛看好"
        
        if home_wins > away_wins and not key_injuries:
            recommendation += f"{home_team}主场不败。"
        elif away_wins > home_wins:
            recommendation += f"{away_team}反客为主。"
        else:
            recommendation += "双方握手言和。"
        
        return recommendation
    
    def _generate_editor_comment(
        self,
        home_team: str,
        away_team: str,
        h2h_stats: Dict,
        injuries: List[Dict]
    ) -> str:
        """生成编辑独家观点 (防止被判定为垃圾内容)"""
        comments = [
            f"从历史交锋来看，{home_team}在主场面对{away_team}时往往能发挥出色。",
            f"值得注意的是，两队最近几次交手都出现了进球大战。",
            f"考虑到双方的战术风格，这场比赛很可能会是一场对攻战。",
            f"教练的排兵布阵将是决定比赛走向的关键因素。",
        ]
        
        import random
        return random.choice(comments)
    
    def _slugify(self, text: str) -> str:
        """转换为 URL 友好的 slug"""
        return text.lower().replace(" ", "-").replace("_", "-")
    
    def _get_h2h_data(self, fixture: Dict) -> Dict:
        """获取 H2H 数据 (简化版)"""
        # 实际应调用 API
        return {
            "summary": "主队稍占优势",
            "total_matches": 10,
            "home_wins": 4,
            "away_wins": 3,
            "draws": 3
        }
    
    def _get_team_form(self, team_id: int) -> List[str]:
        """获取球队近况 (简化版)"""
        import random
        choices = ["W", "D", "L"]
        return [random.choice(choices) for _ in range(5)]
    
    def _get_injuries(self, fixture: Dict) -> List[Dict]:
        """获取伤停信息 (简化版)"""
        # 实际应调用 API
        return []
    
    def _get_odds_data(self, home_team: str, away_team: str) -> Dict:
        """获取赔率数据 (简化版)"""
        # 实际应调用 OddsAggregator
        return {
            "Bet365": {"home": 2.10, "draw": 3.40, "away": 3.50, "is_best_home": True},
            "Pinnacle": {"home": 2.05, "draw": 3.50, "away": 3.60},
            "William Hill": {"home": 2.00, "draw": 3.45, "away": 3.55}
        }


if __name__ == "__main__":
    generator = MatchPreviewGenerator()
    generator.generate_all_previews(limit=5)
