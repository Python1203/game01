"""
VIP 内容页面构建器
生成包含 VIP 专属内容、动态赔率对比和 CPS 链接的 HTML 页面
"""
import os
from typing import Dict, List, Optional
from datetime import datetime
from src.vip_data_models import VIPMatchAnalysis, DataType, CONTENT_ACCESS


class VIPPageBuilder:
    """VIP 内容页面构建器"""
    
    def __init__(self, output_dir: str = "./public"):
        self.output_dir = output_dir
        self.template_cache = {}
        
        # 确保输出目录存在
        os.makedirs(output_dir, exist_ok=True)
        os.makedirs(f"{output_dir}/vip", exist_ok=True)
    
    def build_vip_match_page(self, analysis: VIPMatchAnalysis, user_tier: str = "free") -> str:
        """
        构建比赛分析页面
        Args:
            analysis: VIP 比赛分析数据
            user_tier: 用户等级 ("free", "vip_basic", "vip_premium")
        """
        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{analysis.basic_data.home_team} vs {analysis.basic_data.away_team} - VIP 分析</title>
    <meta name="description" content="专业足球比赛分析，包含伤停信息、历史交锋数据和 AI 预测">
    {self._generate_css()}
</head>
<body>
    {self._generate_header(analysis)}
    
    <div class="container">
        <!-- 基础信息 (所有用户可见) -->
        {self._generate_basic_info(analysis.basic_data)}
        
        <!-- VIP 内容区域 -->
        <div class="vip-content-section">
            {self._generate_vip_access_gate(analysis, user_tier)}
        </div>
        
        <!-- 动态赔率对比 -->
        {self._generate_odds_comparison_section(analysis)}
        
        <!-- CPS 行动号召 -->
        {self._generate_cta_section(analysis)}
    </div>
    
    {self._generate_footer()}
    {self._generate_scripts()}
</body>
</html>
"""
        
        # 写入文件
        slug = f"{analysis.basic_data.home_team.lower()}-vs-{analysis.basic_data.away_team.lower()}"
        dir_path = f"{self.output_dir}/vip/{slug}"
        os.makedirs(dir_path, exist_ok=True)
        
        filepath = f"{dir_path}/index.html"
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        
        return filepath
    
    def _generate_css(self) -> str:
        """生成 CSS 样式"""
        return """
<style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #f5f7fa; }
    .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
    
    /* Header */
    header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 40px 0; }
    .match-header { text-align: center; }
    .teams { display: flex; align-items: center; justify-content: center; gap: 40px; margin: 30px 0; }
    .team { text-align: center; }
    .team-name { font-size: 1.5em; font-weight: bold; margin-top: 10px; }
    .vs { font-size: 2em; font-weight: bold; opacity: 0.8; }
    
    /* 基础信息卡片 */
    .basic-info-card { background: white; border-radius: 12px; padding: 30px; margin: 30px 0; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
    .info-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-top: 20px; }
    .info-item { text-align: center; padding: 15px; background: #f8f9fa; border-radius: 8px; }
    .info-label { color: #666; font-size: 0.9em; margin-bottom: 5px; }
    .info-value { font-size: 1.3em; font-weight: bold; color: #333; }
    
    /* VIP 内容区域 */
    .vip-section { background: white; border-radius: 12px; padding: 30px; margin: 30px 0; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
    .vip-badge { display: inline-block; background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white; padding: 6px 16px; border-radius: 20px; font-size: 0.85em; font-weight: bold; margin-bottom: 15px; }
    
    /* 赔率对比 */
    .odds-comparison { margin: 30px 0; }
    .odds-table { width: 100%; border-collapse: collapse; background: white; border-radius: 8px; overflow: hidden; }
    .odds-table th { background: #667eea; color: white; padding: 15px; text-align: left; }
    .odds-table td { padding: 15px; border-bottom: 1px solid #eee; }
    .best-odds { background: #d4edda !important; font-weight: bold; }
    .odds-bookmaker { display: flex; align-items: center; gap: 10px; }
    .bet-button { background: #28a745; color: white; padding: 8px 20px; border-radius: 5px; text-decoration: none; display: inline-block; transition: background 0.3s; }
    .bet-button:hover { background: #218838; }
    
    /* 价值注提示框 */
    .value-bet-alert { background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white; padding: 25px; border-radius: 12px; margin: 30px 0; }
    .value-bet-alert h3 { margin-bottom: 15px; font-size: 1.3em; }
    .value-bet-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 15px; }
    .value-bet-item { background: rgba(255,255,255,0.2); padding: 15px; border-radius: 8px; }
    
    /* 伤停信息 */
    .injury-list { list-style: none; }
    .injury-item { padding: 15px; border-left: 4px solid #dc3545; background: #fff5f5; margin: 10px 0; border-radius: 4px; }
    .injury-player { font-weight: bold; font-size: 1.1em; }
    .injury-details { color: #666; margin-top: 5px; }
    
    /* CTA 按钮 */
    .cta-box { text-align: center; padding: 40px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 12px; margin: 30px 0; }
    .cta-button { display: inline-block; background: white; color: #667eea; padding: 15px 40px; border-radius: 30px; text-decoration: none; font-weight: bold; font-size: 1.1em; margin: 10px; transition: transform 0.3s; }
    .cta-button:hover { transform: translateY(-2px); }
    
    /* 响应式 */
    @media (max-width: 768px) {
        .teams { flex-direction: column; gap: 20px; }
        .info-grid { grid-template-columns: 1fr; }
    }
</style>
"""
    
    def _generate_header(self, analysis: VIPMatchAnalysis) -> str:
        """生成页面头部"""
        return f"""
<header>
    <div class="container">
        <div class="match-header">
            <h1>🏆 {analysis.basic_data.league}</h1>
            <div class="teams">
                <div class="team">
                    <div class="team-name">{analysis.basic_data.home_team}</div>
                </div>
                <div class="vs">VS</div>
                <div class="team">
                    <div class="team-name">{analysis.basic_data.away_team}</div>
                </div>
            </div>
            <p>⏰ 比赛时间：{datetime.fromisoformat(analysis.basic_data.commence_time).strftime('%Y-%m-%d %H:%M')}</p>
        </div>
    </div>
</header>
"""
    
    def _generate_basic_info(self, basic_data) -> str:
        """生成基础信息卡片"""
        return f"""
<div class="basic-info-card">
    <h2>📊 比赛信息</h2>
    <div class="info-grid">
        <div class="info-item">
            <div class="info-label">联赛</div>
            <div class="info-value">{basic_data.league}</div>
        </div>
        <div class="info-item">
            <div class="info-label">比赛时间</div>
            <div class="info-value">{datetime.fromisoformat(basic_data.commence_time).strftime('%m/%d %H:%M')}</div>
        </div>
        <div class="info-item">
            <div class="info-label">比赛状态</div>
            <div class="info-value">{basic_data.status}</div>
        </div>
        {self._generate_score_display(basic_data)}
    </div>
</div>
"""
    
    def _generate_score_display(self, basic_data) -> str:
        """生成比分显示"""
        if basic_data.home_score is not None and basic_data.away_score is not None:
            return f"""
        <div class="info-item">
            <div class="info-label">当前比分</div>
            <div class="info-value">{basic_data.home_score} - {basic_data.away_score}</div>
        </div>
"""
        return ""
    
    def _generate_vip_access_gate(self, analysis: VIPMatchAnalysis, user_tier: str) -> str:
        """生成 VIP 内容访问门控"""
        vip_content = []
        
        # 1. 伤停信息 (VIP_BASIC)
        if analysis.injuries:
            if user_tier in ["vip_basic", "vip_premium"]:
                vip_content.append(self._generate_injuries_section(analysis.injuries))
            else:
                vip_content.append(self._generate_lock_teaser("伤停信息", "vip_basic"))
        
        # 2. H2H 统计 (VIP_PREMIUM)
        if analysis.h2h_stats:
            if user_tier == "vip_premium":
                vip_content.append(self._generate_h2h_section(analysis.h2h_stats))
            else:
                vip_content.append(self._generate_lock_teaser("历史交锋", "vip_premium"))
        
        # 3. AI 预测 (VIP_PREMIUM)
        if analysis.ai_prediction:
            if user_tier == "vip_premium":
                vip_content.append(self._generate_ai_prediction_section(analysis.ai_prediction))
            else:
                vip_content.append(self._generate_lock_teaser("AI 预测", "vip_premium"))
        
        return '\n'.join(vip_content)
    
    def _generate_injuries_section(self, injuries: List) -> str:
        """生成伤停信息区域"""
        injuries_html = "<ul class='injury-list'>"
        
        for injury in injuries:
            severity_icon = {"severe": "🔴", "moderate": "🟡", "minor": "🟢"}.get(injury.severity, "⚪")
            injuries_html += f"""
            <li class="injury-item">
                <div class="injury-player">{severity_icon} {injury.player_name}</div>
                <div class="injury-details">
                    <strong>球队:</strong> {injury.team} | 
                    <strong>位置:</strong> {injury.position} | 
                    <strong>伤情:</strong> {injury.injury_type}
                    {f' | <strong>预计回归:</strong> {injury.expected_return}' if injury.expected_return else ''}
                </div>
            </li>
"""
        
        injuries_html += "</ul>"
        
        return f"""
<div class="vip-section">
    <span class="vip-badge">🔒 VIP BASIC</span>
    <h2>🏥 伤停信息中心</h2>
    {injuries_html}
</div>
"""
    
    def _generate_h2h_section(self, h2h_stats) -> str:
        """生成 H2H 统计区域"""
        return f"""
<div class="vip-section">
    <span class="vip-badge">💎 VIP PREMIUM</span>
    <h2>⚔️ 历史交锋统计</h2>
    <div class="info-grid">
        <div class="info-item">
            <div class="info-label">总场次</div>
            <div class="info-value">{h2h_stats.total_matches}</div>
        </div>
        <div class="info-item">
            <div class="info-label">主队胜</div>
            <div class="info-value">{h2h_stats.home_wins}</div>
        </div>
        <div class="info-item">
            <div class="info-label">平局</div>
            <div class="info-value">{h2h_stats.draws}</div>
        </div>
        <div class="info-item">
            <div class="info-label">客队胜</div>
            <div class="info-value">{h2h_stats.away_wins}</div>
        </div>
        <div class="info-item">
            <div class="info-label">大球 (2.5+)</div>
            <div class="info-value">{h2h_stats.over_2_5_goals}</div>
        </div>
        <div class="info-item">
            <div class="info-label">双方进球</div>
            <div class="info-value">{h2h_stats.both_scored}</div>
        </div>
    </div>
</div>
"""
    
    def _generate_ai_prediction_section(self, prediction) -> str:
        """生成 AI 预测区域"""
        confidence_color = {
            "high": "#28a745",
            "medium": "#ffc107",
            "low": "#dc3545"
        }.get(prediction.risk_level, "#6c757d")
        
        return f"""
<div class="vip-section">
    <span class="vip-badge">🤖 VIP PREMIUM</span>
    <h2>🧠 AI 智能预测</h2>
    <div class="info-grid">
        <div class="info-item">
            <div class="info-label">预测结果</div>
            <div class="info-value">{prediction.predicted_outcome.replace('_', ' ').title()}</div>
        </div>
        <div class="info-item">
            <div class="info-label">置信度</div>
            <div class="info-value" style="color: {confidence_color}">{prediction.confidence_level:.0f}%</div>
        </div>
        <div class="info-item">
            <div class="info-label">推荐投注</div>
            <div class="info-value">{prediction.recommended_pick or 'N/A'}</div>
        </div>
        <div class="info-item">
            <div class="info-label">价值评分</div>
            <div class="info-value">{'⭐' * int(prediction.value_rating)}</div>
        </div>
    </div>
    <div style="margin-top: 20px; padding: 15px; background: #f8f9fa; border-radius: 8px;">
        <strong>📝 分析理由:</strong>
        <p style="margin-top: 10px; line-height: 1.6;">{prediction.reasoning}</p>
    </div>
</div>
"""
    
    def _generate_lock_teaser(self, content_type: str, required_tier: str) -> str:
        """生成锁定内容提示"""
        tier_names = {
            "vip_basic": "VIP Basic",
            "vip_premium": "VIP Premium"
        }
        
        return f"""
<div class="vip-section" style="text-align: center; padding: 60px 20px;">
    <span class="vip-badge">🔒 {tier_names.get(required_tier, 'VIP')}</span>
    <h2>🔐 解锁{content_type}</h2>
    <p style="margin: 20px 0; color: #666;">
        升级到{tier_names.get(required_tier, 'VIP')}会员，获取{content_type.lower()}权限
    </p>
    <a href="/vip/subscribe" class="cta-button">立即升级</a>
</div>
"""
    
    def _generate_odds_comparison_section(self, analysis: VIPMatchAnalysis) -> str:
        """生成赔率对比区域"""
        # 这里可以集成 odds_cps_module 的数据
        return """
<div class="section">
    <h2>🎲 实时赔率对比</h2>
    <p style="color: #666; margin-bottom: 20px;">数据来源：Bet365, Pinnacle, William Hill 等主流博彩公司</p>
    
    <table class="odds-table">
        <thead>
            <tr>
                <th>博彩公司</th>
                <th>主胜</th>
                <th>平局</th>
                <th>客胜</th>
                <th>操作</th>
            </tr>
        </thead>
        <tbody>
            <tr class="best-odds">
                <td><strong>Bet365 ⭐</strong></td>
                <td>1.95</td>
                <td>3.60</td>
                <td>4.20</td>
                <td><a href="#" class="bet-button">立即投注</a></td>
            </tr>
            <tr>
                <td>Pinnacle</td>
                <td>1.92</td>
                <td>3.55</td>
                <td>4.10</td>
                <td><a href="#" class="bet-button">立即投注</a></td>
            </tr>
            <tr>
                <td>William Hill</td>
                <td>1.90</td>
                <td>3.65</td>
                <td>4.00</td>
                <td><a href="#" class="bet-button">立即投注</a></td>
            </tr>
        </tbody>
    </table>
</div>
"""
    
    def _generate_cta_section(self, analysis: VIPMatchAnalysis) -> str:
        """生成 CTA 区域"""
        key_insights = analysis.get_key_insights()
        
        insights_html = ""
        if key_insights:
            insights_html = "<ul style='text-align: left; max-width: 600px; margin: 20px auto;'>"
            for insight in key_insights:
                insights_html += f"<li style='margin: 10px 0;'>{insight}</li>"
            insights_html += "</ul>"
        
        return f"""
<div class="cta-box">
    <h2>🎯 获取专业投注建议</h2>
    <p style="margin: 20px 0;">加入 VIP 会员，获取专家分析和高胜率推荐</p>
    {insights_html}
    <a href="/vip/pricing" class="cta-button">查看会员方案</a>
    <a href="/go/telegram" class="cta-button">✈️ 加入 Telegram 频道</a>
</div>
"""
    
    def _generate_footer(self) -> str:
        """生成页面底部"""
        return """
<footer style="text-align: center; padding: 40px 0; color: #666; margin-top: 60px;">
    <div class="container">
        <p>&copy; 2026 VIP 体育分析。All rights reserved.</p>
        <p style="margin-top: 10px; font-size: 0.9em; color: #999;">
            免责声明：本网站内容仅供参考，不构成投注建议。请理性博彩，未满 18 岁禁止参与。
        </p>
    </div>
</footer>
"""
    
    def _generate_scripts(self) -> str:
        """生成 JavaScript 脚本"""
        return """
<script>
// 动态更新赔率
async function updateOdds() {
    try {
        const response = await fetch('/api/latest-odds');
        const data = await response.json();
        // 更新赔率显示...
    } catch (error) {
        console.error('更新赔率失败:', error);
    }
}

// 每 30 秒更新一次
setInterval(updateOdds, 30000);

// 页面加载时执行一次
updateOdds();
</script>
"""


if __name__ == "__main__":
    # 测试代码
    from vip_data_models import BasicMatchData, VIPMatchAnalysis
    
    print("\n🎨 测试 VIP 页面构建器\n")
    
    # 创建测试数据
    basic_data = BasicMatchData(
        match_id="test_001",
        home_team="Manchester City",
        away_team="Liverpool",
        league="英超",
        commence_time=datetime.now().isoformat(),
        status="scheduled"
    )
    
    analysis = VIPMatchAnalysis(
        match_id="test_001",
        basic_data=basic_data
    )
    
    # 构建页面
    builder = VIPPageBuilder()
    filepath = builder.build_vip_match_page(analysis, user_tier="free")
    
    print(f"✓ 生成 VIP 页面：{filepath}")
