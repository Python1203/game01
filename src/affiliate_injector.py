"""
Affiliate Link 注入模块
智能插入变现链接到文章内容中
"""
from typing import List, Dict
import re


class AffiliateInjector:
    """Affiliate Link 注入器"""
    
    def __init__(self, affiliate_links: List[str]):
        self.affiliate_links = [link.strip() for link in affiliate_links if link.strip()]
        
        # 定义不同类别的推荐文案模板
        self.cta_templates = {
            "stock_analysis": [
                "\n\n💡 **立即开始投资 {symbol}**: [{broker_name} - 零佣金交易]({affiliate_link})",
                "\n\n📈 **开通股票账户**: [{broker_name} - 新手送免费股票]({affiliate_link})",
                "\n\n🎯 **把握投资机会**: [{broker_name}]({affiliate_link})"
            ],
            "crypto_analysis": [
                "\n\n💰 **立即购买 {symbol}**: [{exchange_name} - 最低手续费]({affiliate_link})",
                "\n\n🚀 **注册加密货币交易所**: [{exchange_name} - 新用户奖励]({affiliate_link})",
                "\n\n🔥 **开始数字货币投资**: [{exchange_name}]({affiliate_link})"
            ],
            "casino_review": [
                "\n\n🎰 **立即领取奖金**: [{casino_name} - 欢迎奖金高达$5000]({affiliate_link})",
                "\n\n🎲 **注册账户**: [{casino_name} - 首次存款 100% 匹配]({affiliate_link})",
                "\n\n♠️ **开始游戏**: [{casino_name}]({affiliate_link})"
            ]
        }
        
        # 合作伙伴名称映射
        self.partner_names = {
            "stock": ["Robinhood", "Webull", "TD Ameritrade", "E*TRADE"],
            "crypto": ["Binance", "Coinbase", "Kraken", "FTX"],
            "casino": ["Bet365", "888 Casino", "PokerStars", "DraftKings"]
        }
    
    def inject_links(self, article) -> str:
        """
        向文章注入 Affiliate Links
        
        Args:
            article: Article 对象
            
        Returns:
            注入后的内容
        """
        content = article.content
        category = article.category
        symbol = article.symbol
        
        if not self.affiliate_links:
            print("⚠️ 未配置 Affiliate Links")
            return content
        
        # 根据分类选择注入策略
        if category == "stock_analysis":
            injected_content = self._inject_stock_links(content, symbol)
        elif category == "crypto_analysis":
            injected_content = self._inject_crypto_links(content, symbol)
        elif category == "casino_review":
            injected_content = self._inject_casino_links(content)
        else:
            injected_content = self._inject_generic_links(content)
        
        return injected_content
    
    def _inject_stock_links(self, content: str, symbol: str) -> str:
        """向股票文章注入链接"""
        link = self.affiliate_links[0] if self.affiliate_links else "#"
        broker_name = self.partner_names["stock"][0]
        
        # 在文章结尾添加 CTA
        cta_options = self.cta_templates["stock_analysis"]
        cta_text = cta_options[0].format(
            symbol=symbol,
            broker_name=broker_name,
            affiliate_link=link
        )
        
        return content + cta_text
    
    def _inject_crypto_links(self, content: str, symbol: str) -> str:
        """向加密货币文章注入链接"""
        link = self.affiliate_links[0] if self.affiliate_links else "#"
        exchange_name = self.partner_names["crypto"][0]
        
        cta_options = self.cta_templates["crypto_analysis"]
        cta_text = cta_options[0].format(
            symbol=symbol,
            exchange_name=exchange_name,
            affiliate_link=link
        )
        
        return content + cta_text
    
    def _inject_casino_links(self, content: str) -> str:
        """向博彩文章注入链接"""
        link = self.affiliate_links[0] if self.affiliate_links else "#"
        casino_name = self.partner_names["casino"][0]
        
        cta_options = self.cta_templates["casino_review"]
        cta_text = cta_options[0].format(
            casino_name=casino_name,
            affiliate_link=link
        )
        
        return content + cta_text
    
    def _inject_generic_links(self, content: str) -> str:
        """通用链接注入"""
        if not self.affiliate_links:
            return content
        
        link = self.affiliate_links[0]
        
        # 在文章中间位置插入 (第三段后)
        paragraphs = content.split('\n\n')
        if len(paragraphs) > 3:
            insert_text = f"\n\n👉 **推荐阅读**: [点击查看我们的推荐平台]({link})\n\n"
            paragraphs.insert(3, insert_text)
            return '\n\n'.join(paragraphs)
        
        # 或者在结尾添加
        return content + f"\n\n更多信息请访问：[{link}]({link})"
    
    def smart_inject_multiple(self, article, max_links: int = 3) -> str:
        """
        智能注入多个链接
        
        Args:
            article: Article 对象
            max_links: 最大链接数量
            
        Returns:
            注入后的内容
        """
        content = article.content
        category = article.category
        
        available_links = self.affiliate_links[:max_links]
        
        if not available_links:
            return content
        
        # 在文章不同位置插入
        positions = []
        
        # 第一段落后
        paragraphs = content.split('\n\n')
        if len(paragraphs) > 1 and len(available_links) >= 1:
            positions.append(('after_first', 1))
        
        # 中间位置
        if len(paragraphs) > 3 and len(available_links) >= 2:
            positions.append(('middle', len(paragraphs) // 2))
        
        # 结尾
        if len(available_links) >= 3:
            positions.append(('end', -1))
        
        # 执行插入
        for pos_type, index in positions:
            if pos_type == 'after_first':
                link_text = f"\n💡 赞助商：[{self._get_partner_name(category)}]({available_links[0]})\n"
                paragraphs.insert(index, link_text)
            elif pos_type == 'middle':
                link_text = f"\n📊 数据来源：[{self._get_partner_name(category)}]({available_links[1]})\n"
                paragraphs.insert(index, link_text)
            elif pos_type == 'end':
                link_text = f"\n🎁 特别优惠：[{self._get_partner_name(category)} - 立即注册]({available_links[2]})\n"
                paragraphs.append(link_text)
        
        return '\n\n'.join(paragraphs)
    
    def _get_partner_name(self, category: str) -> str:
        """获取合作伙伴名称"""
        if category == "stock_analysis":
            return self.partner_names["stock"][0]
        elif category == "crypto_analysis":
            return self.partner_names["crypto"][0]
        elif category == "casino_review":
            return self.partner_names["casino"][0]
        return "合作伙伴"
