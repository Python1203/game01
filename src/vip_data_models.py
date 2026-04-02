"""
VIP 内容分层数据模型
支持基础免费层和 VIP 订阅层的数据结构
"""
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from datetime import datetime


@dataclass
class BasicMatchData:
    """基础比赛数据 (免费层)"""
    match_id: str
    home_team: str
    away_team: str
    league: str
    commence_time: str
    status: str  # "scheduled", "live", "finished"
    
    # 实时比分
    home_score: Optional[int] = None
    away_score: Optional[int] = None
    
    # 基础统计
    possession: Optional[Dict[str, int]] = None  # 控球率
    shots_on_target: Optional[Dict[str, int]] = None  # 射正
    shots_off_target: Optional[Dict[str, int]] = None  # 射偏
    corners: Optional[Dict[str, int]] = None  # 角球
    yellow_cards: Optional[Dict[str, int]] = None  # 黄牌
    red_cards: Optional[Dict[str, int]] = None  # 红牌
    
    # 基础赔率
    basic_odds: Optional[Dict[str, float]] = None  # {home: 1.85, draw: 3.5, away: 4.2}


@dataclass
class InjuryInfo:
    """伤停信息 (VIP 专属)"""
    player_name: str
    team: str
    position: str  # "forward", "midfielder", "defender", "goalkeeper"
    injury_type: str
    expected_return: Optional[str] = None
    severity: str = "minor"  # "minor", "moderate", "severe"
    is_suspended: bool = False  # 是否停赛
    suspension_reason: Optional[str] = None  # 停赛原因


@dataclass
class H2HStats:
    """历史交锋统计 (VIP 专属)"""
    total_matches: int
    home_wins: int
    away_wins: int
    draws: int
    home_goals: int
    away_goals: int
    over_2_5_goals: int  # 大球次数
    under_2_5_goals: int  # 小球次数
    both_scored: int  # 双方都进球次数
    
    # 最近 N 场交锋
    recent_matches: List[Dict] = field(default_factory=list)
    
    # 特殊统计
    home_advantage: Dict = field(default_factory=dict)


@dataclass
class AIModelPrediction:
    """AI 预测模型建议 (VIP 专属)"""
    model_version: str
    confidence_level: float  # 0-100
    predicted_outcome: str  # "home_win", "draw", "away_win"
    predicted_score: Optional[str] = None  # "2-1"
    
    # 概率分布
    home_win_prob: float = 0.0
    draw_prob: float = 0.0
    away_win_prob: float = 0.0
    
    # 进球预测
    over_2_5_prob: float = 0.0
    under_2_5_prob: float = 0.0
    btts_prob: float = 0.0  # Both Teams To Score
    
    # 推荐投注类型
    recommended_bet: Optional[str] = None  # "Asian Handicap", "Over/Under", etc.
    recommended_pick: Optional[str] = None  # 具体推荐
    value_rating: float = 0.0  # 价值评分 0-5 星
    
    # 风险分析
    risk_level: str = "medium"  # "low", "medium", "high"
    reasoning: str = ""


@dataclass
class VIPMatchAnalysis:
    """VIP 比赛分析完整数据包"""
    match_id: str
    
    # 基础数据 (公开)
    basic_data: BasicMatchData
    
    # VIP 专属数据
    injuries: List[InjuryInfo] = field(default_factory=list)
    h2h_stats: Optional[H2HStats] = None
    ai_prediction: Optional[AIModelPrediction] = None
    
    # 球队近况
    home_form: List[str] = field(default_factory=list)  # ["W", "D", "W", "L", "W"]
    away_form: List[str] = field(default_factory=list)
    
    # 高级统计
    advanced_stats: Dict = field(default_factory=dict)
    
    # 元数据
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def is_vip_content(self) -> bool:
        """判断是否为 VIP 内容"""
        return bool(self.injuries or self.h2h_stats or self.ai_prediction)
    
    def get_key_insights(self) -> List[str]:
        """获取关键洞察"""
        insights = []
        
        # 伤停影响
        key_injuries = [i for i in self.injuries if i.severity in ["moderate", "severe"]]
        if key_injuries:
            for injury in key_injuries:
                insights.append(
                    f"⚠️ 关键伤停：{injury.player_name} ({injury.team}) - {injury.injury_type}"
                )
        
        # H2H 趋势
        if self.h2h_stats:
            if self.h2h_stats.home_wins > self.h2h_stats.away_wins * 2:
                insights.append(f"📊 历史交锋：主队占据绝对优势")
            elif self.h2h_stats.over_2_5_goals > self.h2h_stats.total_matches * 0.7:
                insights.append(f"📊 进球趋势：近期交锋多为大球")
        
        # AI 预测
        if self.ai_prediction and self.ai_prediction.confidence_level >= 70:
            insights.append(
                f"🤖 AI 预测：{self.ai_prediction.predicted_outcome.replace('_', ' ').title()} "
                f"(置信度 {self.ai_prediction.confidence_level:.0f}%)"
            )
        
        return insights


@dataclass
class TeamNews:
    """球队新闻 (VIP 专属)"""
    team: str
    news_type: str  # "injury", "suspension", "tactical", "transfer"
    headline: str
    description: str
    impact_level: str = "low"  # "low", "medium", "high"
    published_at: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class LineupPrediction:
    """预计首发阵容 (VIP 专属)"""
    team: str
    formation: str  # "4-3-3", "4-4-2", etc.
    
    goalkeeper: List[str] = field(default_factory=list)
    defenders: List[str] = field(default_factory=list)
    midfielders: List[str] = field(default_factory=list)
    forwards: List[str] = field(default_factory=list)
    
    confidence: float = 0.0  # 预测置信度
    last_updated: str = field(default_factory=lambda: datetime.now().isoformat())


# 数据类型枚举
class DataType:
    FREE = "free"
    VIP_BASIC = "vip_basic"
    VIP_PREMIUM = "vip_premium"


# 内容访问权限配置
CONTENT_ACCESS = {
    "basic_match_data": DataType.FREE,
    "live_score": DataType.FREE,
    "basic_statistics": DataType.FREE,
    
    "injuries": DataType.VIP_BASIC,
    "suspensions": DataType.VIP_BASIC,
    "team_news": DataType.VIP_BASIC,
    
    "h2h_history": DataType.VIP_PREMIUM,
    "ai_prediction": DataType.VIP_PREMIUM,
    "lineup_prediction": DataType.VIP_PREMIUM,
    "advanced_stats": DataType.VIP_PREMIUM,
    "value_bets": DataType.VIP_PREMIUM,
}
