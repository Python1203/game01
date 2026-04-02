"""
完整闭环链路：数据接口 -> 内容生成 -> CPS 转化
每小时自动运行，抓取赛程、生成页面、填充赔率、追踪转化
"""
import os
import json
from datetime import datetime, timedelta
from typing import List, Dict
from src.sports_data_api import FootballDataAPI
from src.odds_cps_module import OddsAggregator, GeoAffiliateRecommender
from src.deep_link_generator import DeepLinkGenerator, GeoTargetingFilter
from src.match_preview_generator import MatchPreviewGenerator
from src.cache_manager import SmartCache


class ConversionPipeline:
    """数据->内容->转化 完整流水线"""
    
    def __init__(self):
        self.football_api = FootballDataAPI()
        self.odds_aggregator = OddsAggregator()
        self.preview_generator = MatchPreviewGenerator()
        self.deep_link_gen = DeepLinkGenerator()
        self.geo_filter = GeoTargetingFilter()
        self.cache = SmartCache()
        
        # 统计数据
        self.stats = {
            "fixtures_fetched": 0,
            "pages_generated": 0,
            "odds_updated": 0,
            "deep_links_created": 0
        }
    
    def run_full_pipeline(self):
        """执行完整闭环流程"""
        print("\n" + "="*60)
        print("🔄 开始执行数据->内容->转化闭环")
        print("="*60)
        
        # Step 1: 抓取未来 48 小时赛程
        print("\n📅 Step 1: 抓取未来赛程...")
        fixtures = self._fetch_upcoming_fixtures(hours=48)
        self.stats["fixtures_fetched"] = len(fixtures)
        print(f"✓ 获取到 {len(fixtures)} 场比赛")
        
        if not fixtures:
            print("⚠️ 暂无比赛数据")
            return
        
        # Step 2: 为每场比赛生成预览页面
        print("\n📝 Step 2: 生成赛事前瞻页面...")
        preview_pages = []
        
        for fixture in fixtures:
            try:
                page_path = self.preview_generator.generate_single_preview(fixture)
                preview_pages.append({
                    "fixture": fixture,
                    "page_path": page_path
                })
                self.stats["pages_generated"] += 1
                print(f"✓ 生成：{fixture['teams']['home']['name']} vs {fixture['teams']['away']['name']}")
            except Exception as e:
                print(f"❌ 生成失败：{e}")
        
        # Step 3: 获取实时赔率并注入页面
        print("\n🎲 Step 3: 获取实时赔率...")
        odds_data = self.odds_aggregator.get_odds_comparison(
            sport="soccer_epl",
            limit=len(fixtures)
        )
        self.stats["odds_updated"] = len(odds_data)
        print(f"✓ 更新 {len(odds_data)} 场比赛的赔率")
        
        # Step 4: 生成深度链接并创建 CPS 追踪
        print("\n🔗 Step 4: 生成深度链接...")
        
        for page_info in preview_pages:
            fixture = page_info["fixture"]
            
            # 为多家博彩公司生成深度链接
            match_data = {
                "home_team": fixture["teams"]["home"]["name"],
                "away_team": fixture["teams"]["away"]["name"],
                "league": fixture["league"]["name"],
                "match_id": str(fixture["fixture"]["id"])
            }
            
            # 生成所有链接 (不同地区)
            all_links = {}
            for region in ["US", "UK", "EU"]:
                links = self.deep_link_gen.generate_all_links(match_data, user_region=region)
                
                # 地域过滤
                filtered_links = self.geo_filter.filter_links_by_region(links, region)
                
                if filtered_links:
                    all_links[region] = filtered_links
                    self.stats["deep_links_created"] += len(filtered_links)
            
            # 缓存链接数据供页面使用
            cache_key = f"deep_links:{match_data['match_id']}"
            self.cache.set(cache_key, all_links, policy_name="odds")
        
        # Step 5: 生成汇总索引页面
        print("\n📄 Step 5: 生成汇总索引...")
        self._generate_index_page(preview_pages)
        
        # Step 6: 输出统计报告
        self._print_summary_report()
        
        print("\n✅ 完整闭环流程执行完毕!")
        print("="*60)
    
    def _fetch_upcoming_fixtures(self, hours: int = 48) -> List[Dict]:
        """获取未来 N 小时的赛程"""
        # 实际应调用 API，这里简化处理
        fixtures = self.football_api.get_fixtures(limit=20)
        
        # 过滤未来时间
        now = datetime.now()
        future_fixtures = []
        
        for fixture in fixtures:
            try:
                match_time = datetime.fromisoformat(fixture["fixture"]["date"].replace('Z', '+00:00'))
                if now <= match_time <= now + timedelta(hours=hours):
                    future_fixtures.append(fixture)
            except:
                continue
        
        return future_fixtures
    
    def _generate_index_page(self, preview_pages: List[Dict]) -> str:
        """生成汇总索引页面"""
        html = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>今日赛事前瞻 - 专业足球预测与赔率分析</title>
    <meta name="description" content="提供最新足球赛事前瞻分析，包含历史交锋、伤停信息、实时赔率和 AI 预测">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: sans-serif; background: #f5f7fa; }
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 40px 0; text-align: center; }
        h1 { font-size: 2.5em; margin-bottom: 10px; }
        .match-list { margin: 40px 0; }
        .match-item { background: white; border-radius: 12px; padding: 20px; margin: 20px 0; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .match-item h2 { color: #667eea; margin-bottom: 10px; }
        .match-meta { color: #666; margin-bottom: 15px; }
        .read-more { display: inline-block; background: #667eea; color: white; padding: 10px 25px; border-radius: 5px; text-decoration: none; }
        .read-more:hover { background: #5568d3; }
    </style>
</head>
<body>
    <header>
        <div class="container">
            <h1>🏆 今日赛事前瞻</h1>
            <p>专业足球预测与赔率分析</p>
            <p style="margin-top: 10px; opacity: 0.8;">更新时间：""" + datetime.now().strftime('%Y-%m-%d %H:%M') + """</p>
        </div>
    </header>
    
    <div class="container">
        <div class="match-list">
"""
        
        for page_info in preview_pages:
            fixture = page_info["fixture"]
            home = fixture["teams"]["home"]["name"]
            away = fixture["teams"]["away"]["name"]
            league = fixture["league"]["name"]
            date = fixture["fixture"]["date"][:16].replace('T', ' ')
            
            html += f"""
            <div class="match-item">
                <h2>{home} vs {away}</h2>
                <p class="match-meta">{league} | {date}</p>
                <a href="/preview/{self._slugify(home)}-vs-{self._slugify(away)}/index.html" class="read-more">查看完整分析 →</a>
            </div>
"""
        
        html += """
        </div>
    </div>
    
    <footer style="text-align: center; padding: 40px 0; color: #666; margin-top: 60px;">
        <p>&copy; 2026 赛事前瞻。All rights reserved.</p>
    </footer>
</body>
</html>
"""
        
        index_path = f"{self.preview_generator.output_dir}/index.html"
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"✓ 生成索引页面：{index_path}")
        return index_path
    
    def _print_summary_report(self):
        """打印统计报告"""
        print("\n📊 执行统计:")
        print(f"  - 抓取赛程：{self.stats['fixtures_fetched']} 场")
        print(f"  - 生成页面：{self.stats['pages_generated']} 个")
        print(f"  - 更新赔率：{self.stats['odds_updated']} 场")
        print(f"  - 创建链接：{self.stats['deep_links_created']} 个")
        
        # 预估收益
        estimated_cpc = 0.50  # 每次点击平均佣金
        estimated_ctr = 0.03  # 3% 点击率
        
        if self.stats['pages_generated'] > 0:
            monthly_views = self.stats['pages_generated'] * 30 * 10  # 假设每页日均 10 次浏览
            monthly_clicks = monthly_views * estimated_ctr
            monthly_revenue = monthly_clicks * estimated_cpc
            
            print(f"\n💰 预估月收益:")
            print(f"  - 月浏览量：~{monthly_views:,}")
            print(f"  - 月点击量：~{monthly_clicks:,.0f}")
            print(f"  - 月佣金收入：~${monthly_revenue:,.2f}")


# 定时任务入口
if __name__ == "__main__":
    pipeline = ConversionPipeline()
    pipeline.run_full_pipeline()
