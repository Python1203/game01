"""
API-Football/Basketball 深度数据集成
实现伤停预警、历史交锋 (H2H) 分析等 VIP 功能
"""
import os
import requests
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from .vip_data_models import (
    InjuryInfo, H2HStats, TeamNews, LineupPrediction, 
    BasicMatchData, VIPMatchAnalysis
)


class FootballDataAPI:
    """API-Football 数据采集器"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("SPORTS_API_KEY", "")
        self.base_url = "https://v3.football.api-sports.io"
        self.headers = {"x-apisports-key": self.api_key} if self.api_key else {}
        
    def get_fixtures(self, league: str = None, live: bool = False, limit: int = 10) -> List[Dict]:
        """获取比赛赛程"""
        try:
            if live:
                url = f"{self.base_url}/fixtures?live=all"
            elif league:
                # 获取特定联赛的比赛
                url = f"{self.base_url}/fixtures?league={league}&season={datetime.now().year}"
            else:
                # 获取近期比赛
                today = datetime.now()
                tomorrow = today + timedelta(days=1)
                url = f"{self.base_url}/fixtures?from={today.strftime('%Y-%m-%d')}&to={tomorrow.strftime('%Y-%m-%d')}"
            
            response = requests.get(url, headers=self.headers, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                return data.get("response", [])[:limit]
            else:
                print(f"⚠️ API-Football 请求失败：{response.status_code}")
                return []
                
        except Exception as e:
            print(f"❌ 获取赛程失败：{e}")
            return []
    
    def get_injuries(self, team_id: int = None, player_id: int = None) -> List[InjuryInfo]:
        """
        获取伤停信息 (VIP 专属)
        Args:
            team_id: 球队 ID (可选)
            player_id: 球员 ID (可选)
        """
        injuries = []
        
        try:
            url = f"{self.base_url}/injuries?"
            if team_id:
                url += f"team={team_id}"
            elif player_id:
                url += f"player={player_id}"
            else:
                # 获取所有伤停 (限制数量)
                url += "search=common"
            
            response = requests.get(url, headers=self.headers, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                for item in data.get("response", []):
                    injury = InjuryInfo(
                        player_name=item.get("player", {}).get("name", "Unknown"),
                        team=item.get("team", {}).get("name", "Unknown"),
                        position=item.get("player", {}).get("position", "Unknown"),
                        injury_type=item.get("type", "Injury"),
                        expected_return=item.get("expected", None),
                        severity=self._assess_injury_severity(item.get("type", "")),
                        is_suspended=False
                    )
                    injuries.append(injury)
                    
        except Exception as e:
            print(f"❌ 获取伤停信息失败：{e}")
        
        return injuries
    
    def get_h2h(self, team1_id: int, team2_id: int, last: int = 10) -> H2HStats:
        """
        获取历史交锋数据 (VIP 专属)
        Args:
            team1_id: 主队 ID
            team2_id: 客队 ID
            last: 最近 N 场比赛
        """
        try:
            url = f"{self.base_url}/fixtures/h2h?teams={team1_id}-{team2_id}&last={last}"
            response = requests.get(url, headers=self.headers, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                fixtures = data.get("response", [])
                
                # 统计 H2H 数据
                h2h = H2HStats(
                    total_matches=len(fixtures),
                    home_wins=0,
                    away_wins=0,
                    draws=0,
                    home_goals=0,
                    away_goals=0,
                    over_2_5_goals=0,
                    under_2_5_goals=0,
                    both_scored=0,
                    recent_matches=[]
                )
                
                for fixture in fixtures:
                    goals_home = fixture["goals"]["home"]
                    goals_away = fixture["goals"]["away"]
                    
                    # 更新统计
                    h2h.home_goals += goals_home if goals_home else 0
                    h2h.away_goals += goals_away if goals_away else 0
                    
                    # 判断胜负
                    if goals_home > goals_away:
                        h2h.home_wins += 1
                    elif goals_away > goals_home:
                        h2h.away_wins += 1
                    else:
                        h2h.draws += 1
                    
                    # 大小球统计
                    total_goals = (goals_home or 0) + (goals_away or 0)
                    if total_goals > 2.5:
                        h2h.over_2_5_goals += 1
                    else:
                        h2h.under_2_5_goals += 1
                    
                    # 双方进球统计
                    if goals_home and goals_away:
                        h2h.both_scored += 1
                    
                    # 记录最近比赛
                    h2h.recent_matches.append({
                        "date": fixture["fixture"]["date"],
                        "home_team": fixture["teams"]["home"]["name"],
                        "away_team": fixture["teams"]["away"]["name"],
                        "score": f"{goals_home}-{goals_away}",
                        "winner": "home" if goals_home > goals_away else ("away" if goals_away > goals_home else "draw")
                    })
                
                # 计算主场优势
                h2h.home_advantage = {
                    "home_win_rate": h2h.home_wins / h2h.total_matches if h2h.total_matches > 0 else 0,
                    "avg_goals_per_match": (h2h.home_goals + h2h.away_goals) / h2h.total_matches if h2h.total_matches > 0 else 0
                }
                
                return h2h
                
        except Exception as e:
            print(f"❌ 获取 H2H 数据失败：{e}")
        
        # 返回默认数据
        return H2HStats(total_matches=0, home_wins=0, away_wins=0, draws=0, 
                       home_goals=0, away_goals=0, over_2_5_goals=0, under_2_5_goals=0)
    
    def get_team_form(self, team_id: int, last: int = 5) -> List[str]:
        """获取球队近况 (如 ["W", "D", "W", "L", "W"])"""
        form = []
        
        try:
            url = f"{self.base_url}/fixtures?team={team_id}&last={last}"
            response = requests.get(url, headers=self.headers, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                for fixture in data.get("response", []):
                    teams = fixture["teams"]
                    goals = fixture["goals"]
                    
                    # 判断当前球队是否为主队
                    is_home = teams["home"]["id"] == team_id
                    team_goals = goals["home"] if is_home else goals["away"]
                    opponent_goals = goals["away"] if is_home else goals["home"]
                    
                    if team_goals > opponent_goals:
                        form.append("W")
                    elif team_goals == opponent_goals:
                        form.append("D")
                    else:
                        form.append("L")
                        
        except Exception as e:
            print(f"❌ 获取球队近况失败：{e}")
        
        return form or ["N/A"] * last
    
    def get_lineups(self, fixture_id: int) -> Optional[LineupPrediction]:
        """获取比赛阵容"""
        try:
            url = f"{self.base_url}/fixtures/{fixture_id}/lineups"
            response = requests.get(url, headers=self.headers, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                # 处理阵容数据
                # ... (简化处理)
                
        except Exception as e:
            print(f"❌ 获取阵容失败：{e}")
        
        return None
    
    def _assess_injury_severity(self, injury_type: str) -> str:
        """评估伤病严重程度"""
        severe_keywords = ["knee", "ankle", "fracture", "ligament", "acl"]
        moderate_keywords = ["muscle", "hamstring", "groin", "thigh"]
        
        injury_lower = injury_type.lower()
        
        if any(kw in injury_lower for kw in severe_keywords):
            return "severe"
        elif any(kw in injury_lower for kw in moderate_keywords):
            return "moderate"
        else:
            return "minor"


class BasketballDataAPI:
    """API-Basketball 数据采集器 (类似结构)"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("SPORTS_API_KEY", "")
        self.base_url = "https://v1.basketball.api-sports.io"
        self.headers = {"x-apisports-key": self.api_key} if self.api_key else {}
    
    def get_games(self, live: bool = False, limit: int = 10) -> List[Dict]:
        """获取篮球比赛"""
        try:
            if live:
                url = f"{self.base_url}/games?live=all"
            else:
                today = datetime.now().strftime("%Y-%m-%d")
                url = f"{self.base_url}/games?date={today}"
            
            response = requests.get(url, headers=self.headers, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                return data.get("response", [])[:limit]
                
        except Exception as e:
            print(f"❌ 获取篮球比赛失败：{e}")
        
        return []


# 统一的数据采集接口
class SportsDataCollector:
    """体育赛事数据采集器 (统一接口)"""
    
    def __init__(self):
        self.football_api = FootballDataAPI()
        self.basketball_api = BasketballDataAPI()
    
    def get_vip_match_analysis(self, match_id: str, sport: str = "football") -> Optional[VIPMatchAnalysis]:
        """
        获取 VIP 比赛分析数据包
        Args:
            match_id: 比赛 ID
            sport: 体育类型 ("football" 或 "basketball")
        """
        if sport == "football":
            return self._get_football_vip_analysis(match_id)
        elif sport == "basketball":
            return self._get_basketball_vip_analysis(match_id)
        return None
    
    def _get_football_vip_analysis(self, match_id: str) -> Optional[VIPMatchAnalysis]:
        """获取足球 VIP 分析"""
        # 实现逻辑...
        pass
    
    def _get_basketball_vip_analysis(self, match_id: str) -> Optional[VIPMatchAnalysis]:
        """获取篮球 VIP 分析"""
        # 实现逻辑...
        pass


if __name__ == "__main__":
    # 测试代码
    collector = FootballDataAPI()
    
    print("\n📊 测试 API-Football 数据采集\n")
    
    # 1. 获取赛程
    fixtures = collector.get_fixtures(live=False, limit=5)
    print(f"✓ 获取到 {len(fixtures)} 场比赛")
    
    # 2. 获取伤停信息
    injuries = collector.get_injuries()
    print(f"✓ 获取到 {len(injuries)} 条伤停信息")
    
    # 3. 示例：获取特定比赛的 H2H
    if fixtures and len(fixtures) >= 2:
        team1 = fixtures[0]["teams"]["home"]["id"]
        team2 = fixtures[0]["teams"]["away"]["id"]
        
        h2h = collector.get_h2h(team1, team2, last=5)
        print(f"✓ H2H 统计：共 {h2h.total_matches} 场交锋")
        print(f"  - 主队胜：{h2h.home_wins}, 客队胜：{h2h.away_wins}, 平局：{h2h.draws}")
