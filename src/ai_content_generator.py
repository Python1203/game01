"""
AI 内容生成模块
支持 OpenAI/Claude/DeepSeek 等多种 AI 模型
"""
import openai
import requests
from typing import Dict, List
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Article:
    """文章数据结构"""
    title: str
    slug: str
    content: str
    excerpt: str
    keywords: List[str]
    category: str
    symbol: str
    created_at: str


class AIContentGenerator:
    """AI 内容生成器"""
    
    def __init__(self, api_key: str, model_type: str = "openai", base_url: str = None):
        """
        初始化 AI 内容生成器
        
        Args:
            api_key: API 密钥
            model_type: 模型类型 ("openai" 或 "deepseek")
            base_url: API 基础 URL（DeepSeek 需要）
        """
        self.api_key = api_key
        self.model_type = model_type
        
        if model_type == "deepseek":
            self.base_url = base_url or "https://xh.v1api.cc"
            self.model = "deepseek-chat"
        else:  # openai
            openai.api_key = api_key
            if base_url:
                openai.api_base = base_url
            self.model = "gpt-4-turbo-preview"
    
    def generate_analysis_article(
        self,
        symbol: str,
        data: Dict,
        content_type: str,
        keywords: List[str]
    ) -> Article:
        """
        生成市场分析文章
        
        Args:
            symbol: 标的符号 (如 AAPL, BTC)
            data: 市场数据
            content_type: 内容类型 (stock_analysis/crypto_analysis/casino_review)
            keywords: SEO 关键词列表
        """
        
        # 构建提示词
        prompt = self._build_prompt(symbol, data, content_type, keywords)
        
        try:
            # 根据模型类型调用不同的 API
            if self.model_type == "deepseek":
                response = self._call_deepseek_api(prompt)
            else:
                response = self._call_openai_api(prompt)
            
            content = response['content']
            
            # 生成标题和摘要
            title = self._extract_title(content, symbol)
            excerpt = self._generate_excerpt(content)
            slug = self._generate_slug(symbol, content_type)
            
            return Article(
                title=title,
                slug=slug,
                content=content,
                excerpt=excerpt,
                keywords=keywords,
                category=content_type,
                symbol=symbol,
                created_at=datetime.now().isoformat()
            )
            
        except Exception as e:
            print(f"❌ AI 生成失败：{e}")
            # 返回模板文章
            return self._generate_template_article(symbol, data, content_type, keywords)
    
    def _call_deepseek_api(self, prompt: str) -> Dict:
        """调用 DeepSeek API"""
        # 确保 base_url 没有末尾的斜杠
        base = self.base_url.rstrip('/')
        url = f"{base}/v1/chat/completions"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": "你是一位专业的金融分析师，擅长股票、加密货币和博彩市场的深度分析。"
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.7,
            "max_tokens": 2000
        }
        
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            if 'choices' in result and len(result['choices']) > 0:
                content = result['choices'][0]['message']['content']
                return {'content': content}
            else:
                raise Exception(f"DeepSeek API 返回异常：{result}")
                
        except requests.exceptions.HTTPError as e:
            error_detail = response.text if 'response' in locals() else str(e)
            raise Exception(f"DeepSeek API 请求失败 ({response.status_code}): {error_detail}")
        except requests.exceptions.RequestException as e:
            raise Exception(f"DeepSeek API 网络错误：{e}")
        except Exception as e:
            raise Exception(f"DeepSeek API 解析错误：{e}")
    
    def _call_openai_api(self, prompt: str) -> Dict:
        """调用 OpenAI API"""
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": self._get_system_instruction("stock_analysis")
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=2000
        )
        
        content = response.choices[0].message.content
        return {'content': content}
    
    def _build_prompt(
        self,
        symbol: str,
        data: Dict,
        content_type: str,
        keywords: List[str]
    ) -> str:
        """构建 AI 提示词"""
        
        if content_type == "stock_analysis":
            prompt = f"""
请为股票 {symbol} 撰写一篇专业的投资分析文章。

【实时数据】
- 当前价格：${data.get('price', 0)}
- 涨跌幅：{data.get('change_percent', '0%')}
- 成交量：{data.get('volume', 0):,}
- 最高价：${data.get('high', 0)}
- 最低价：${data.get('low', 0)}

【SEO 关键词】
{', '.join(keywords)}

【文章要求】
1. 标题吸引人，包含 {symbol} 和核心观点
2. 开篇有吸引力的摘要 (50-80 字)
3. 分析当前价格走势和技术指标
4. 提供投资建议和风险提示
5. 字数 800-1200 字
6. 使用 Markdown 格式，包含小标题

请生成专业、客观的分析内容。
"""
        
        elif content_type == "crypto_analysis":
            prompt = f"""
请为加密货币 {symbol} 撰写一篇深度分析文章。

【实时数据】
- 当前价格：${data.get('price', 0)}
- 24h 涨跌：{data.get('price_change_24h', 0):.2f}%
- 市值：${data.get('market_cap', 0):,}
- 24h 成交量：${data.get('volume_24h', 0):,}
- 24h 最高：${data.get('high_24h', 0)}
- 24h 最低：${data.get('low_24h', 0)}

【SEO 关键词】
{', '.join(keywords)}

【文章要求】
1. 标题具有吸引力，包含 {symbol} 和价格预测
2. 摘要概括核心观点 (50-80 字)
3. 分析链上数据和市场情绪
4. 技术面分析和支撑/阻力位
5. 短期和长期价格预测
6. 字数 800-1200 字，Markdown 格式

请生成专业、深入的加密货币分析。
"""
        
        else:  # casino/betting
            prompt = f"""
请撰写一篇赌场/博彩相关的推荐文章。

【数据】
{data}

【SEO 关键词】
{', '.join(keywords)}

【文章要求】
1. 介绍平台特色和优势
2. 说明奖金和优惠活动
3. 用户体验评价
4. 安全和可靠性分析
5. 注册和使用指南
6. 字数 600-1000 字，Markdown 格式

请生成吸引人的推荐内容。
"""
        
        return prompt
    
    def _get_system_instruction(self, content_type: str) -> str:
        """获取系统指令"""
        
        instructions = {
            "stock_analysis": """你是一位专业的股票分析师，拥有 CFA 资格，擅长技术面和基本面分析。
你的写作风格专业但不失亲和力，善于用数据说话，同时提醒投资风险。""",
            
            "crypto_analysis": """你是一位资深的加密货币分析师，熟悉区块链技术和 DeFi 生态。
你的分析深入透彻，善于结合链上数据和市场情绪，提供客观的投资建议。""",
            
            "casino_review": """你是一位经验丰富的博彩行业专家，熟悉各大平台和游戏规则。
你的推荐真实可信，注重用户体验和安全性，善于发现优惠活动的价值。"""
        }
        
        return instructions.get(content_type, instructions["stock_analysis"])
    
    def _extract_title(self, content: str, symbol: str) -> str:
        """从内容中提取或生成标题"""
        # 简单实现：使用前 50 个字符作为标题
        lines = content.strip().split('\n')
        for line in lines:
            if line.strip() and not line.startswith('#'):
                return f"{symbol} 深度分析：" + line[:50] + "..."
        
        return f"{symbol} 投资分析报告 - {datetime.now().strftime('%Y-%m-%d')}"
    
    def _generate_excerpt(self, content: str) -> str:
        """生成摘要"""
        # 提取第一段作为摘要
        paragraphs = [p for p in content.split('\n\n') if p.strip()]
        if paragraphs:
            excerpt = paragraphs[0].strip()
            return excerpt[:150] + "..." if len(excerpt) > 150 else excerpt
        
        return content[:150] + "..."
    
    def _generate_slug(self, symbol: str, content_type: str) -> str:
        """生成 URL 友好的 slug"""
        date_str = datetime.now().strftime("%Y%m%d")
        type_map = {
            "stock_analysis": "stock-analysis",
            "crypto_analysis": "crypto-analysis",
            "casino_review": "casino-review"
        }
        
        return f"{type_map.get(content_type, 'analysis')}/{symbol.lower()}-{date_str}"
    
    def _generate_template_article(
        self,
        symbol: str,
        data: Dict,
        content_type: str,
        keywords: List[str]
    ) -> Article:
        """生成模板文章 (当 AI 调用失败时使用)"""
        
        templates = {
            "stock_analysis": f"""# {symbol} 投资分析报告

## 核心观点

{symbol} 当前价格为 ${data.get('price', 0)}, 涨跌幅为 {data.get('change_percent', '0%')}。本文将为您深入分析该股票的投资价值。

## 市场表现

根据最新数据，{symbol} 今日成交量达到 {data.get('volume', 0):,}, 显示市场活跃度较高。

## 技术分析

从技术面来看，该股目前处于关键位置，投资者应密切关注后续走势。

## 投资建议

**风险提示**: 股市有风险，投资需谨慎。本文仅供参考，不构成投资建议。
""",
            
            "crypto_analysis": f"""# {symbol} 加密货币深度分析

## 市场行情

{symbol} 当前价格为 ${data.get('price', 0)}, 24 小时涨跌幅为 {data.get('price_change_24h', 0):.2f}%。

## 链上数据

市值达到 ${data.get('market_cap', 0):,}, 显示出强劲的市场信心。

## 价格预测

短期内，{symbol} 可能会在 ${data.get('low_24h', 0)} - ${data.get('high_24h', 0)} 区间震荡。

## 风险提示

加密货币波动性极大，请做好风险管理。
""",
            
            "casino_review": f"""# 热门博彩平台推荐

## 平台特色

我们为您精选了市场上最优质的博彩平台，提供最佳赔率和用户体验。

## 优惠活动

新用户注册即可享受丰厚欢迎奖金。

## 安全保证

所有推荐平台均持有合法牌照，资金安全可靠。
"""
        }
        
        content = templates.get(content_type, templates["stock_analysis"])
        
        return Article(
            title=f"{symbol} 分析报告",
            slug=f"template/{symbol.lower()}",
            content=content,
            excerpt=content.split('\n')[2:4],
            keywords=keywords,
            category=content_type,
            symbol=symbol,
            created_at=datetime.now().isoformat()
        )
