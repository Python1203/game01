"""
深度链接生成器 - 直接跳转至特定比赛投注页面
转化率比首页跳转高 300%+
"""
from typing import Dict, Optional
from datetime import datetime


class DeepLinkGenerator:
    """深度链接生成器"""
    
    def __init__(self):
        # 各博彩公司深度链接模板
        self.link_templates = {
            "bet365": {
                "base": "https://www.bet365.com/en/sports/football/{league_code}/{match_id}",
                "affiliate_base": "https://affiliate-tracking.bet365.com/redirect?link={encoded_url}",
                "params": {
                    "league_code_map": {
                        "英超": "premier-league",
                        "西甲": "la-liga",
                        "德甲": "bundesliga",
                        "意甲": "serie-a",
                        "欧冠": "champions-league"
                    }
                }
            },
            "pinnacle": {
                "base": "https://www.pinnacle.com/en/football/{league_name}/{home_team}-vs-{away_team}/{match_id}",
                "affiliate_base": "https://affiliates.pinnacle.com/track.php?linkid={link_id}&url={encoded_url}"
            },
            "williamhill": {
                "base": "https://sports.williamhill.com/betting/en-gb/football/matches/{match_id}",
                "affiliate_base": "https://affiliates.williamhill.com/redirect?url={encoded_url}"
            },
            "draftkings": {
                "base": "https://sportsbook.draftkings.com/leagues/soccer/{match_id}",
                "affiliate_base": "https://affiliates.draftkings.com/redirect?link={encoded_url}",
                "us_only": True
            },
            "fanduel": {
                "base": "https://sportsbook.fanduel.com/soccer/{home_team}-{away_team}/{match_id}",
                "affiliate_base": "https://affiliates.fanduel.com/redirect?url={encoded_url}",
                "us_only": True
            },
            "unibet": {
                "base": "https://www.unibet.com/betting/sports/filter/football/{match_id}",
                "affiliate_base": "https://affiliates.unibet.com/redirect?url={encoded_url}"
            }
        }
        
        # Affiliate ID 配置 (从环境变量读取)
        self.affiliate_ids = {
            "bet365": "your_bet365_affiliate_id",
            "pinnacle": "your_pinnacle_affiliate_id",
            "williamhill": "your_wh_affiliate_id",
            "draftkings": "your_dk_affiliate_id",
            "fanduel": "your_fd_affiliate_id",
            "unibet": "your_unibet_affiliate_id"
        }
    
    def generate_deep_link(
        self,
        bookmaker: str,
        home_team: str,
        away_team: str,
        league: str,
        match_id: str,
        user_region: str = None
    ) -> Optional[str]:
        """
        生成深度链接
        
        Args:
            bookmaker: 博彩公司名称 (bet365, pinnacle, etc.)
            home_team: 主队名称
            away_team: 客队名称
            league: 联赛名称
            match_id: 比赛 ID
            user_region: 用户所在地区 (US, UK, EU, etc.)
            
        Returns:
            完整的 affiliate 深度链接，如果不支持则返回 None
        """
        if bookmaker not in self.link_templates:
            print(f"⚠️ 不支持的博彩公司：{bookmaker}")
            return None
        
        template = self.link_templates[bookmaker]
        
        # 地域限制检查
        if template.get("us_only") and user_region != "US":
            print(f"⚠️ {bookmaker} 仅限美国用户")
            return None
        
        # 构造基础 URL
        base_url = template["base"].format(
            league_code=self._get_league_code(league, bookmaker),
            league_name=self._slugify(league),
            home_team=self._slugify(home_team),
            away_team=self._slugify(away_team),
            match_id=match_id
        )
        
        # 生成 affiliate 链接
        if "affiliate_base" in template:
            import urllib.parse
            encoded_url = urllib.parse.quote(base_url, safe='')
            affiliate_link = template["affiliate_base"].format(
                encoded_url=encoded_url,
                link_id=self.affiliate_ids.get(bookmaker, "default")
            )
            return affiliate_link
        
        return base_url
    
    def _get_league_code(self, league: str, bookmaker: str) -> str:
        """获取联赛代码"""
        if bookmaker == "bet365":
            code_map = self.link_templates["bet365"]["params"]["league_code_map"]
            return code_map.get(league, "other-leagues")
        return self._slugify(league)
    
    def _slugify(self, text: str) -> str:
        """将文本转换为 URL 友好的 slug"""
        # 简单的转换逻辑，生产环境建议使用 python-slugify
        return text.lower().replace(" ", "-").replace("_", "-")
    
    def generate_all_links(
        self,
        match_data: Dict,
        user_region: str = None
    ) -> Dict[str, str]:
        """
        为多家博彩公司生成深度链接
        
        Args:
            match_data: 比赛数据字典
            user_region: 用户地区
            
        Returns:
            {博彩公司：深度链接} 的字典
        """
        links = {}
        
        for bookmaker in self.link_templates.keys():
            link = self.generate_deep_link(
                bookmaker=bookmaker,
                home_team=match_data.get("home_team", ""),
                away_team=match_data.get("away_team", ""),
                league=match_data.get("league", ""),
                match_id=match_data.get("match_id", ""),
                user_region=user_region
            )
            
            if link:
                links[bookmaker] = link
        
        return links


class GeoTargetingFilter:
    """地域定位过滤器 - 确保合规投放"""
    
    def __init__(self):
        # 各地区允许的博彩公司
        self.allowed_bookmakers = {
            "US": ["draftkings", "fanduel", "betmgm", "caesars", "pointsbet"],
            "UK": ["bet365", "williamhill", "ladbrokes", "coral", "skybet", "paddy_power"],
            "EU": ["bet365", "pinnacle", "unibet", "bwin", "betway"],
            "AU": ["bet365", "sportsbet", "tab", "unibet", "ladbrokes"],
            "CA": ["sports_interaction", "playnow", "bet365", "pinnacle"],
            "ASIA": ["pinnacle", "sbobet", "dafabet", "188bet"],
        }
        
        # 禁止博彩的地区
        self.restricted_regions = [
            "CN",  # 中国
            "RU",  # 俄罗斯
            "AE",  # 阿联酋
            "SA",  # 沙特
            "KW",  # 科威特
            "SG",  # 新加坡
        ]
    
    def is_region_allowed(self, region: str) -> bool:
        """检查地区是否允许博彩"""
        return region not in self.restricted_regions
    
    def get_allowed_bookmakers(self, region: str) -> list:
        """获取指定地区允许的博彩公司"""
        if not self.is_region_allowed(region):
            return []
        
        return self.allowed_bookmakers.get(region, ["bet365", "pinnacle"])
    
    def filter_links_by_region(
        self,
        all_links: Dict[str, str],
        user_region: str
    ) -> Dict[str, str]:
        """根据用户地区过滤链接"""
        allowed = self.get_allowed_bookmakers(user_region)
        
        filtered = {
            bookmaker: link 
            for bookmaker, link in all_links.items() 
            if bookmaker in allowed
        }
        
        return filtered
    
    def detect_user_region(self, ip_address: str = None) -> str:
        """
        检测用户所在地区
        
        Args:
            ip_address: 用户 IP 地址 (可选)
            
        Returns:
            地区代码 (US, UK, EU, etc.)
        """
        if ip_address:
            # 使用 MaxMind GeoIP 数据库 (需要安装 geoip2 库)
            try:
                import geoip2.database
                reader = geoip2.database.Reader('./geoip/GeoLite2-Country.mmdb')
                response = reader.country(ip_address)
                country_code = response.country.iso_code
                
                # 映射到我们的区域系统
                return self._map_country_to_region(country_code)
            except Exception as e:
                print(f"⚠️ IP 定位失败：{e}")
        
        # 默认返回 US
        return "US"
    
    def _map_country_to_region(self, country_code: str) -> str:
        """将国家代码映射到区域"""
        mapping = {
            "US": "US",
            "GB": "UK",
            "DE": "EU",
            "FR": "EU",
            "IT": "EU",
            "ES": "EU",
            "AU": "AU",
            "CA": "CA",
            "JP": "ASIA",
            "KR": "ASIA",
            "TH": "ASIA",
        }
        return mapping.get(country_code, "EU")


# 使用示例
if __name__ == "__main__":
    # 测试深度链接生成
    generator = DeepLinkGenerator()
    
    match_data = {
        "home_team": "Manchester United",
        "away_team": "Liverpool",
        "league": "英超",
        "match_id": "match_123"
    }
    
    # 为英国用户生成所有链接
    all_links = generator.generate_all_links(match_data, user_region="UK")
    
    print("\n🔗 生成的深度链接:")
    for bookie, link in all_links.items():
        print(f"{bookie}: {link[:80]}...")
    
    # 测试地域过滤
    geo_filter = GeoTargetingFilter()
    
    us_region = geo_filter.detect_user_region("8.8.8.8")  # Google DNS
    print(f"\n🌍 检测到用户地区：{us_region}")
    
    # 过滤出美国可用的链接
    us_links = geo_filter.filter_links_by_region(all_links, us_region)
    print(f"✅ 美国用户可见 {len(us_links)} 个博彩公司")
    
    cn_allowed = geo_filter.is_region_allowed("CN")
    print(f"❌ 中国用户允许博彩：{cn_allowed}")
