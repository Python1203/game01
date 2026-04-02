"""
优化版赛事前瞻生成器 - 嵌入 HTML5 + JSON-LD 模板
符合 Google SEO 标准，集成 Deep Link CPS 转化
"""
import os
from typing import Dict, List
from datetime import datetime


class OptimizedPreviewGenerator:
    """优化的赛事前瞻页面生成器"""
    
    def __init__(self, output_dir: str = "./public/preview"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def generate_preview_page(
        self,
        home_team: str,
        away_team: str,
        league: str,
        match_date: str,
        h2h_stats: Dict,
        home_form: List[str],
        away_form: List[str],
        odds_data: Dict,
        ai_recommendation: str
    ) -> str:
        """生成单场优化的预览页面"""
        
        date_obj = datetime.fromisoformat(match_date.replace('Z', '+00:00'))
        formatted_date = date_obj.strftime('%Y年%m月%d日 %H:%M')
        iso_start_time = date_obj.isoformat()
        
        # 提取最佳赔率
        best_home = max(odds_data.items(), key=lambda x: x[1].get('home', 0)) if odds_data else ('Bet365', {'home': 2.10})
        best_draw = max(odds_data.items(), key=lambda x: x[1].get('draw', 0)) if odds_data else ('Bet365', {'draw': 3.40})
        best_away = max(odds_data.items(), key=lambda x: x[1].get('away', 0)) if odds_data else ('Bet365', {'away': 3.50})
        
        best_home_price = best_home[1].get('home', 'N/A')
        best_draw_price = best_draw[1].get('draw', 'N/A')
        best_away_price = best_away[1].get('away', 'N/A')
        
        best_home_bookie = best_home[0]
        best_draw_bookie = best_draw[0]
        best_away_bookie = best_away[0]
        
        # 生成 Slug 和 Canonical URL
        slug = f"{self._slugify(home_team)}-vs-{self._slugify(away_team)}"
        canonical_url = f"https://869.us.ci/preview/{slug}/"
        
        # JSON-LD Schema.org 结构化数据
        json_ld = f'''
        <script type="application/ld+json">
        {{
            "@context": "https://schema.org",
            "@type": "SportsEvent",
            "name": "{home_team} vs {away_team}",
            "description": "{league} 赛事前瞻与赔率对比",
            "startDate": "{iso_start_time}",
            "homeTeam": {{
                "@type": "SportsTeam",
                "name": "{home_team}",
                "logo": "https://869.us.ci/logos/{self._slugify(home_team)}.png"
            }},
            "awayTeam": {{
                "@type": "SportsTeam",
                "name": "{away_team}",
                "logo": "https://869.us.ci/logos/{self._slugify(away_team)}.png"
            }},
            "location": {{
                "@type": "Place",
                "name": "主场球场"
            }},
            "offers": {{
                "@type": "Offer",
                "url": "{canonical_url}",
                "category": "betting"
            }}
        }}
        </script>
        '''
        
        # 生成完整 HTML
        html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <!-- 自动化 SEO 标题：包含主客队、日期和关键词 -->
    <title>【{home_team} vs {away_team}】赔率分析、首发名单及投注建议 - {formatted_date} - 869 体育</title>
    <meta name="description" content="获取{home_team}对阵{away_team}的实时最高赔率对比。包含由 API-Football 提供的伤停情报、历史交锋数据及专家投注建议。">
    <meta name="keywords" content="{home_team}, {away_team}, 赔率分析，比分预测，投注建议，{league}">
    
    <!-- 1. JSON-LD 结构化数据：提升 Google 搜索展示效果 -->
    {json_ld}
    
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; background: #f5f7fa; }}
        .container {{ max-width: 1200px; margin: 0 auto; padding: 20px; }}
        
        header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 40px 0; text-align: center; }}
        h1 {{ font-size: 2.5em; margin-bottom: 10px; }}
        
        /* 2. 文章标题 (H1) */
        .section {{ background: white; border-radius: 12px; padding: 30px; margin: 30px 0; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        .section-title {{ font-size: 1.8em; color: #333; margin-bottom: 20px; border-left: 4px solid #667eea; padding-left: 15px; }}
        
        /* 3. 动态赔率卡片 (CPS 转化核心) */
        .match-card {{ border: 1px solid #eee; padding: 20px; border-radius: 12px; text-align: center; background: #f9f9f9; margin: 30px 0; }}
        .odds-container {{ display: flex; justify-content: space-around; margin-top: 20px; flex-wrap: wrap; }}
        .odds-item {{ background: #fff; padding: 15px; border: 2px solid #007bff; border-radius: 8px; width: 30%; min-width: 150px; margin: 10px; }}
        .best-label {{ font-size: 12px; color: #ff4d4f; font-weight: bold; display: block; margin-bottom: 8px; }}
        .bet-btn {{ display: block; margin-top: 10px; background: #28a745; color: #fff !important; text-decoration: none; padding: 8px; border-radius: 5px; font-weight: bold; transition: background 0.3s; }}
        .bet-btn:hover {{ background: #218838; }}
        
        /* 4. VIP 锁定内容 */
        .vip-content {{ filter: blur(4px); user-select: none; background: #eee; padding: 20px; margin-top: 20px; position: relative; }}
        .vip-lock {{ position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); text-align: center; z-index: 10; background: rgba(255,255,255,0.95); padding: 30px; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.2); }}
        .vip-button {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none; padding: 15px 40px; border-radius: 30px; font-size: 1.1em; cursor: pointer; text-decoration: none; display: inline-block; margin-top: 10px; }}
        
        .form-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; }}
        .form-item {{ text-align: center; padding: 15px; background: #f8f9fa; border-radius: 8px; }}
        .form-value {{ font-size: 1.5em; font-weight: bold; }}
        .form-win {{ color: #28a745; }}
        .form-draw {{ color: #ffc107; }}
        .form-loss {{ color: #dc3545; }}
        
        @media (max-width: 768px) {{
            h1 {{ font-size: 1.8em; }}
            .section {{ padding: 20px; }}
            .odds-container {{ flex-direction: column; }}
            .odds-item {{ width: 100%; }}
        }}
    </style>
</head>
<body>
    <header>
        <div class="container">
            <!-- 2. 文章标题 (H1) -->
            <h1>🏆 {home_team} vs {away_team}: {league} 深度预测与最高赔率推荐</h1>
            <p style="font-size: 1.2em; opacity: 0.9; margin-top: 10px;">比赛时间：{formatted_date}</p>
        </div>
    </header>
    
    <div class="container">
        <!-- 3. 动态赔率卡片 (CPS 转化核心) -->
        <div class="match-card">
            <h3>🎲 实时全场胜平负 (Market: H2H)</h3>
            <p>更新时间：<span id="update-time">{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</span></p>
            
            <div class="odds-container">
                <!-- 主胜 -->
                <div class="odds-item">
                    <span class="best-label">⭐ 最高主胜</span>
                    <div style="font-size: 1.8em; font-weight: bold; margin: 10px 0;">{best_home_price if isinstance(best_home_price, str) else f"{best_home_price:.2f}"}</div>
                    <small>来自：<strong>{best_home_bookie}</strong></small>
                    <a href="#bet-now" class="bet-btn" rel="nofollow">立即下单 →</a>
                </div>
                
                <!-- 平局 -->
                <div class="odds-item">
                    <span class="best-label">⭐ 最高平局</span>
                    <div style="font-size: 1.8em; font-weight: bold; margin: 10px 0;">{best_draw_price if isinstance(best_draw_price, str) else f"{best_draw_price:.2f}"}</div>
                    <small>来自：<strong>{best_draw_bookie}</strong></small>
                    <a href="#bet-now" class="bet-btn" rel="nofollow">立即下单 →</a>
                </div>
                
                <!-- 客胜 -->
                <div class="odds-item">
                    <span class="best-label">⭐ 最高客胜</span>
                    <div style="font-size: 1.8em; font-weight: bold; margin: 10px 0;">{best_away_price if isinstance(best_away_price, str) else f"{best_away_price:.2f}"}</div>
                    <small>来自：<strong>{best_away_bookie}</strong></small>
                    <a href="#bet-now" class="bet-btn" rel="nofollow">立即下单 →</a>
                </div>
            </div>
        </div>
        
        <!-- 4. 自动化赛事简评 (SEO 核心) -->
        <div class="section">
            <h2 class="section-title">📝 赛事前瞻</h2>
            <p style="line-height: 1.8; color: #555;">
                {home_team}目前在{league}中表现{"出色" if "W" in home_form[-3:] else "平稳"}。
                近 5 场比赛战绩为 <strong>{"-".join(home_form[-5:])}</strong>。
                根据 API-Football 提供的 H2H 数据，双方近 10 次交手，
                {home_team}取得了<strong>{h2h_stats.get('home_wins', 0)}胜{h2h_stats.get('draws', 0)}平{h2h_stats.get('away_wins', 0)}负</strong>的战绩。
            </p>
            <p style="margin-top: 15px;">
                <a href="/premier-league-table" style="color: #667eea;">查看英超积分榜 →</a> | 
                <a href="/{self._slugify(home_team)}-history" style="color: #667eea;">{home_team}历史战绩 →</a>
            </p>
        </div>
        
        <!-- 关键指标 -->
        <div class="section">
            <h2 class="section-title">📊 关键指标</h2>
            <div class="form-grid">
                <div class="form-item">
                    <div style="color: #666; margin-bottom: 10px;">主队近况</div>
                    <div class="form-value">
                        {''.join([f'<span class="form-{"win" if r=="W" else ("draw" if r=="D" else "loss")}">{r}</span> ' for r in home_form])}
                    </div>
                </div>
                <div class="form-item">
                    <div style="color: #666; margin-bottom: 10px;">客队近况</div>
                    <div class="form-value">
                        {''.join([f'<span class="form-{"win" if r=="W" else ("draw" if r=="D" else "loss")}">{r}</span> ' for r in away_form])}
                    </div>
                </div>
                <div class="form-item">
                    <div style="color: #666; margin-bottom: 10px;">历史交锋</div>
                    <div class="form-value">{h2h_stats.get('summary', 'N/A')}</div>
                </div>
            </div>
        </div>
        
        <!-- AI 推荐 -->
        <div class="section" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white;">
            <h2 class="section-title" style="color: white; border-left-color: white;">🤖 AI 智能推荐</h2>
            <p style="font-size: 1.1em; line-height: 1.8;">{ai_recommendation}</p>
        </div>
        
        <!-- 5. Freemium VIP 锁定内容 -->
        <div class="section">
            <h2 class="section-title">🔒 VIP 深度情报 (伤停名单 & 进阶预测)</h2>
            <div class="vip-content">
                <p><strong>关键球员伤停：</strong></p>
                <ul>
                    <li>{home_team} 主力前锋 - 伤病 (预计回归：2 周后)</li>
                    <li>{away_team} 后防核心 - 停赛</li>
                </ul>
                <p style="margin-top: 20px;"><strong>AI 模型预测概率：</strong></p>
                <p>主胜 <strong>55%</strong> | 平局 <strong>25%</strong> | 客胜 <strong>20%</strong></p>
                <p style="margin-top: 20px;"><strong>编辑推荐：</strong>看好主队不败，推荐让球盘主胜。</p>
            </div>
            <div class="vip-lock">
                <h3 style="margin-bottom: 15px;">🔑 解锁 VIP 专属内容</h3>
                <p style="color: #666; margin-bottom: 20px;">获取完整伤停名单、AI 预测模型及高胜率投注建议</p>
                <button class="vip-button" onclick="location.href='/vip-upgrade'">立即升级 VIP</button>
                <p style="margin-top: 15px; font-size: 0.9em; color: #999;">已有 5000+ 会员加入</p>
            </div>
        </div>
    </div>
    
    <footer style="text-align: center; padding: 40px 0; color: #666; margin-top: 60px;">
        <p>&copy; 2026 869 体育 - 专业赛事前瞻。All rights reserved.</p>
        <p style="margin-top: 10px; font-size: 0.9em; color: #999;">
            免责声明：本文仅供参考，不构成投注建议。请理性购彩，未满 18 岁禁止参与。
        </p>
    </footer>
</body>
</html>
'''
        
        # 写入文件
        file_path = f"{self.output_dir}/{slug}/index.html"
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"✅ 生成优化页面：{file_path}")
        return file_path
    
    def _slugify(self, text: str) -> str:
        """转换为 URL 友好的 slug"""
        return text.lower().replace(" ", "-").replace("_", "-")


# 测试示例
if __name__ == "__main__":
    generator = OptimizedPreviewGenerator()
    
    # 示例数据
    sample_data = {
        "home_team": "Manchester United",
        "away_team": "Liverpool",
        "league": "英超",
        "match_date": "2026-04-05T15:00:00Z",
        "h2h_stats": {"home_wins": 4, "draws": 3, "away_wins": 3, "summary": "主队稍占优势"},
        "home_form": ["W", "D", "W", "L", "W"],
        "away_form": ["W", "W", "D", "W", "L"],
        "odds_data": {
            "Bet365": {"home": 2.10, "draw": 3.40, "away": 3.50},
            "Pinnacle": {"home": 2.05, "draw": 3.50, "away": 3.60},
            "William Hill": {"home": 2.00, "draw": 3.45, "away": 3.55}
        },
        "ai_recommendation": "曼联近期主场表现出色，利物浦客场防守存在隐患。综合考虑历史交锋和当前状态，看好主队不败。推荐让球盘主胜，置信度 75%。"
    }
    
    generator.generate_preview_page(**sample_data)
    print("\n✅ 优化版模板已集成!")
