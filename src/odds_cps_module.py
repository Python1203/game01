"""
动态赔率对比与 CPS 变现模块
实现多维度赔率聚合、智能 CPS 嵌入和区域化推荐
"""
import os
import requests
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass


@dataclass
class BookmakerOdds:
    """博彩公司赔率数据"""
    bookmaker_name: str
    home_odds: float
    away_odds: float
    draw_odds: Optional[float] = None  # 足球等才有平局
    
    # CPS 链接模板
    affiliate_link_template: Optional[str] = None
    
    # 区域限制
    restricted_regions: List[str] = None
    
    def __post_init__(self):
        if self.restricted_regions is None:
            self.restricted_regions = []


@dataclass
class OddsComparison:
    """赔率对比结果"""
    match_id: str
    home_team: str
    away_team: str
    commence_time: str
    sport: str
    
    # 各家博彩公司赔率
    bookmakers: List[BookmakerOdds]
    
    # 最佳赔率
    best_home_odds: Optional[BookmakerOdds] = None
    best_draw_odds: Optional[BookmakerOdds] = None
    best_away_odds: Optional[BookmakerOdds] = None
    
    # 平均赔率
    avg_home_odds: float = 0.0
    avg_draw_odds: float = 0.0
    avg_away_odds: float = 0.0
    
    # 赔率差异
    home_odds_variance: float = 0.0
    away_odds_variance: float = 0.0


@dataclass
class ValueBet:
    """价值注机会"""
    match_id: str
    bet_type: str  # "home", "draw", "away"
    bookmaker: str
    odds: float
    implied_probability: float  # 赔率隐含概率
    model_probability: float  # 模型预测概率
    edge: float  # 优势 (model_prob - implied_prob)
    confidence: str  # "low", "medium", "high"
    recommended_stake: float  # 推荐投注比例 (%)
    
    @property
    def is_value(self) -> bool:
        """是否为价值注"""
        return self.edge > 0.05  # 5% 以上的优势


class OddsAggregator:
    """赔率聚合器"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("ODDS_API_KEY", "")
        self.base_url = "https://api.the-odds-api.com/v4"
        
        # 博彩公司配置
        self.bookmakers_config = {
            "bet365": {
                "name": "Bet365",
                "affiliate_base": "https://affiliate-tracking.bet365.com/redirect?link={match_id}",
                "regions": ["uk", "eu", "au"]
            },
            "pinnacle": {
                "name": "Pinnacle",
                "affiliate_base": "https://www.pinnacle.com/en/football/{match_id}",
                "regions": ["us", "eu", "asia"]
            },
            "williamhill": {
                "name": "William Hill",
                "affiliate_base": "https://sports.williamhill.com/betting/{match_id}",
                "regions": ["uk", "eu"]
            },
            "draftkings": {
                "name": "DraftKings",
                "affiliate_base": "https://sportsbook.draftkings.com/leagues/football/{match_id}",
                "regions": ["us"]
            },
            "fanduel": {
                "name": "FanDuel",
                "affiliate_base": "https://sportsbook.fanduel.com/football/{match_id}",
                "regions": ["us"]
            },
            "unibet": {
                "name": "Unibet",
                "affiliate_base": "https://www.unibet.com/betting/sports/filter/football/{match_id}",
                "regions": ["eu", "au"]
            }
        }
    
    def get_odds_comparison(self, sport: str = "soccer_epl", limit: int = 10) -> List[OddsComparison]:
        """
        获取赔率对比数据
        Args:
            sport: 体育项目 ID (如 soccer_epl, basketball_nba)
            limit: 返回比赛数量
        """
        comparisons = []
        
        try:
            # 获取赔率数据
            url = f"{self.base_url}/sports/{sport}/odds"
            params = {
                "regions": "us,uk,eu",  # 多区域
                "markets": "h2h,spreads,totals",  # 多种玩法
                "apiKey": self.api_key
            }
            
            response = requests.get(url, params=params, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                
                for match in data[:limit]:
                    comparison = self._process_match_data(match)
                    if comparison:
                        comparisons.append(comparison)
                        
        except Exception as e:
            print(f"❌ 获取赔率对比失败：{e}")
        
        return comparisons
    
    def _process_match_data(self, match: Dict) -> Optional[OddsComparison]:
        """处理单场比赛的赔率数据"""
        try:
            bookmakers = []
            
            # 提取各家博彩公司赔率
            for bookmaker_data in match.get("bookmakers", []):
                bookie_key = bookmaker_data["key"]
                bookie_name = bookmaker_data["title"]
                
                # 获取胜平负赔率
                markets = bookmaker_data.get("markets", [])
                h2h_market = next((m for m in markets if m["key"] == "h2h"), None)
                
                if not h2h_market:
                    continue
                
                outcomes = h2h_market["outcomes"]
                home_outcome = next((o for o in outcomes if o["name"] == match["home_team"]), None)
                away_outcome = next((o for o in outcomes if o["name"] == match["away_team"]), None)
                draw_outcome = next((o for o in outcomes if o["name"] == "Draw"), None)
                
                if not home_outcome or not away_outcome:
                    continue
                
                # 创建博彩公司对象
                bookie = BookmakerOdds(
                    bookmaker_name=bookie_name,
                    home_odds=home_outcome["price"],
                    draw_odds=draw_outcome["price"] if draw_outcome else None,
                    away_odds=away_outcome["price"],
                    affiliate_link_template=self._get_affiliate_link(bookie_key),
                    restricted_regions=self.bookmakers_config.get(bookie_key, {}).get("regions", [])
                )
                bookmakers.append(bookie)
            
            if not bookmakers:
                return None
            
            # 创建赔率对比对象
            comparison = OddsComparison(
                match_id=match["id"],
                home_team=match["home_team"],
                away_team=match["away_team"],
                commence_time=match["commence_time"],
                sport=match["sport_title"],
                bookmakers=bookmakers
            )
            
            # 计算最佳赔率和平均值
            self._calculate_best_odds(comparison)
            
            return comparison
            
        except Exception as e:
            print(f"❌ 处理比赛数据失败：{e}")
            return None
    
    def _calculate_best_odds(self, comparison: OddsComparison):
        """计算最佳赔率和统计信息"""
        if not comparison.bookmakers:
            return
        
        # 找出最佳赔率
        comparison.best_home_odds = max(
            comparison.bookmakers, 
            key=lambda b: b.home_odds
        )
        comparison.best_away_odds = max(
            comparison.bookmakers,
            key=lambda b: b.away_odds
        )
        
        if comparison.bookmakers[0].draw_odds is not None:
            comparison.best_draw_odds = max(
                [b for b in comparison.bookmakers if b.draw_odds is not None],
                key=lambda b: b.draw_odds
            )
        
        # 计算平均赔率
        comparison.avg_home_odds = sum(b.home_odds for b in comparison.bookmakers) / len(comparison.bookmakers)
        comparison.avg_away_odds = sum(b.away_odds for b in comparison.bookmakers) / len(comparison.bookmakers)
        
        if comparison.bookmakers[0].draw_odds is not None:
            comparison.avg_draw_odds = sum(
                b.draw_odds for b in comparison.bookmakers if b.draw_odds is not None
            ) / len([b for b in comparison.bookmakers if b.draw_odds is not None])
        
        # 计算赔率差异
        comparison.home_odds_variance = self._calculate_variance([b.home_odds for b in comparison.bookmakers])
        comparison.away_odds_variance = self._calculate_variance([b.away_odds for b in comparison.bookmakers])
    
    def _calculate_variance(self, values: List[float]) -> float:
        """计算方差"""
        if len(values) < 2:
            return 0.0
        mean = sum(values) / len(values)
        return sum((x - mean) ** 2 for x in values) / len(values)
    
    def _get_affiliate_link(self, bookmaker_key: str) -> str:
        """获取 CPS 链接模板"""
        config = self.bookmakers_config.get(bookmaker_key, {})
        return config.get("affiliate_base", "")


class GeoAffiliateRecommender:
    """区域化博彩商推荐器"""
    
    def __init__(self):
        # 区域与博彩商映射
        self.region_bookmakers = {
            "US": ["draftkings", "fanduel", "betmgm", "caesars"],
            "UK": ["bet365", "williamhill", "ladbrokes", "coral"],
            "EU": ["bet365", "pinnacle", "unibet", "bwin"],
            "AU": ["bet365", "sportsbet", "tab", "unibet"],
            "ASIA": ["pinnacle", "sbobet", "dafabet"],
            "CA": ["sports_interaction", "playnow", "bet365"]
        }
        
        # 默认推荐 (全球通用)
        self.default_bookmakers = ["bet365", "pinnacle", "unibet"]
    
    def recommend_for_region(self, user_region: str = None, ip_address: str = None) -> List[str]:
        """
        根据用户区域推荐博彩商
        Args:
            user_region: 用户区域代码 (如 "US", "UK")
            ip_address: IP 地址 (用于地理位置定位，可选)
        """
        # 如果提供了 IP 地址，可以尝试地理定位
        if ip_address and not user_region:
            user_region = self._geolocate_ip(ip_address)
        
        # 获取推荐的博彩商
        if user_region and user_region in self.region_bookmakers:
            return self.region_bookmakers[user_region]
        
        return self.default_bookmakers
    
    def _geolocate_ip(self, ip_address: str) -> Optional[str]:
        """通过 IP 地址定位地理位置 (简化版)"""
        # 实际项目中可以使用 ipapi.com 或类似服务
        # 这里仅作示例
        if ip_address.startswith("192.168"):
            return "US"  # 本地测试
        return None
    
    def generate_affiliate_link(self, bookmaker_key: str, match_id: str, user_region: str = None) -> str:
        """生成带区域参数的 CPS 链接"""
        # 获取推荐列表
        recommended = self.recommend_for_region(user_region)
        
        if bookmaker_key not in recommended:
            # 如果不是首选推荐，使用备选
            bookmaker_key = recommended[0] if recommended else self.default_bookmakers[0]
        
        # 生成链接
        aggregator = OddsAggregator()
        template = aggregator._get_affiliate_link(bookmaker_key)
        
        if template:
            return template.replace("{match_id}", match_id)
        
        return ""


class ValueBetFinder:
    """价值注发现工具"""
    
    def __init__(self, model_accuracy: float = 0.65):
        """
        Args:
            model_accuracy: 模型预测准确率 (用于计算置信度)
        """
        self.model_accuracy = model_accuracy
    
    def find_value_bets(
        self, 
        odds_comparison: OddsComparison,
        model_predictions: Dict[str, float]
    ) -> List[ValueBet]:
        """
        寻找价值注机会
        Args:
            odds_comparison: 赔率对比数据
            model_predictions: 模型预测概率 {"home": 0.45, "draw": 0.30, "away": 0.25}
        """
        value_bets = []
        
        # 检查主胜
        if odds_comparison.best_home_odds:
            implied_prob = 1.0 / odds_comparison.best_home_odds.home_odds
            model_prob = model_predictions.get("home", 0)
            edge = model_prob - implied_prob
            
            if edge > 0.05:  # 5% 优势阈值
                value_bet = ValueBet(
                    match_id=odds_comparison.match_id,
                    bet_type="home",
                    bookmaker=odds_comparison.best_home_odds.bookmaker_name,
                    odds=odds_comparison.best_home_odds.home_odds,
                    implied_probability=implied_prob,
                    model_probability=model_prob,
                    edge=edge,
                    confidence=self._calculate_confidence(edge),
                    recommended_stake=self._calculate_stake(edge)
                )
                value_bets.append(value_bet)
        
        # 检查平局
        if odds_comparison.best_draw_odds and "draw" in model_predictions:
            implied_prob = 1.0 / odds_comparison.best_draw_odds.draw_odds
            model_prob = model_predictions.get("draw", 0)
            edge = model_prob - implied_prob
            
            if edge > 0.05:
                value_bet = ValueBet(
                    match_id=odds_comparison.match_id,
                    bet_type="draw",
                    bookmaker=odds_comparison.best_draw_odds.bookmaker_name,
                    odds=odds_comparison.best_draw_odds.draw_odds,
                    implied_probability=implied_prob,
                    model_probability=model_prob,
                    edge=edge,
                    confidence=self._calculate_confidence(edge),
                    recommended_stake=self._calculate_stake(edge)
                )
                value_bets.append(value_bet)
        
        # 检查客胜
        if odds_comparison.best_away_odds:
            implied_prob = 1.0 / odds_comparison.best_away_odds.away_odds
            model_prob = model_predictions.get("away", 0)
            edge = model_prob - implied_prob
            
            if edge > 0.05:
                value_bet = ValueBet(
                    match_id=odds_comparison.match_id,
                    bet_type="away",
                    bookmaker=odds_comparison.best_away_odds.bookmaker_name,
                    odds=odds_comparison.best_away_odds.away_odds,
                    implied_probability=implied_prob,
                    model_probability=model_prob,
                    edge=edge,
                    confidence=self._calculate_confidence(edge),
                    recommended_stake=self._calculate_stake(edge)
                )
                value_bets.append(value_bet)
        
        # 按优势排序
        value_bets.sort(key=lambda x: x.edge, reverse=True)
        
        return value_bets
    
    def _calculate_confidence(self, edge: float) -> str:
        """计算置信度"""
        if edge > 0.15:
            return "high"
        elif edge > 0.10:
            return "medium"
        else:
            return "low"
    
    def _calculate_stake(self, edge: float) -> float:
        """计算推荐投注比例 (凯利公式简化版)"""
        # 简化版：优势越大，投注比例越高
        base_stake = 1.0  # 基础 1%
        additional = min(edge * 10, 4.0)  # 最多追加到 5%
        return base_stake + additional


if __name__ == "__main__":
    # 测试代码
    print("\n🎲 测试赔率聚合与 CPS 系统\n")
    
    aggregator = OddsAggregator()
    
    # 1. 获取赔率对比
    comparisons = aggregator.get_odds_comparison(sport="soccer_epl", limit=3)
    print(f"✓ 获取到 {len(comparisons)} 场比赛的赔率对比")
    
    if comparisons:
        comp = comparisons[0]
        print(f"\n📊 比赛：{comp.home_team} vs {comp.away_team}")
        print(f"   最佳主胜赔率：{comp.best_home_odds.bookmaker_name} - {comp.best_home_odds.home_odds:.2f}")
        print(f"   最佳客胜赔率：{comp.best_away_odds.bookmaker_name} - {comp.best_away_odds.away_odds:.2f}")
    
    # 2. 测试区域化推荐
    recommender = GeoAffiliateRecommender()
    us_recommendations = recommender.recommend_for_region("US")
    uk_recommendations = recommender.recommend_for_region("UK")
    
    print(f"\n🌍 区域推荐:")
    print(f"   美国用户：{', '.join(us_recommendations)}")
    print(f"   英国用户：{', '.join(uk_recommendations)}")
    
    # 3. 测试价值注发现
    finder = ValueBetFinder()
    sample_predictions = {"home": 0.55, "draw": 0.25, "away": 0.20}
    
    if comparisons:
        value_bets = finder.find_value_bets(comparisons[0], sample_predictions)
        if value_bets:
            print(f"\n💎 发现 {len(value_bets)} 个价值注机会:")
            for bet in value_bets:
                print(f"   - {bet.bet_type}: {bet.bookmaker} 赔率 {bet.odds:.2f} (优势 {bet.edge*100:.1f}%)")
