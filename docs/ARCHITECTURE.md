# 🏗️ Stock/Crypto/Casino 全自动流水线 - 架构设计文档

## 📌 核心设计理念

### 1. 无服务器化 (Serverless First)
- **零运维**: 利用 Vercel/Netlify 的自动扩缩容能力
- **按量付费**: 只为实际使用付费，无流量时零成本
- **全球 CDN**: 静态资源自动分发到全球边缘节点

### 2. 事件驱动架构 (Event-Driven)
```
外部触发器 → Deploy Hook → Build Process → Content Generation → Deployment
   ↑                                                                    ↓
   └────────────────────── 自动循环 ─────────────────────────┘
```

### 3. 模块化设计 (Modular Design)
每个功能模块独立，易于替换和扩展。

---

## 🗂️ 完整项目结构

```
PythonProject/
│
├── main.py                          # 主入口 - Vercel Build 执行
├── test_local.py                    # 本地测试脚本
├── requirements.txt                 # Python 依赖
├── vercel.json                      # Vercel 配置
├── .gitignore                       # Git 忽略文件
├── .env.example                     # 环境变量示例
│
├── src/                             # 核心模块
│   ├── __init__.py
│   ├── data_collector.py           # 数据采集
│   │   ├── fetch_stock_data()      # 股票数据 (Alpha Vantage)
│   │   ├── fetch_crypto_data()     # 加密货币 (CoinGecko)
│   │   └── fetch_casino_odds()     # 博彩赔率 (The-Odds-API)
│   │
│   ├── ai_content_generator.py     # AI 内容生成
│   │   ├── generate_analysis_article()  # 生成分析文章
│   │   ├── _build_prompt()         # 构建 AI 提示词
│   │   └── _generate_template_article() # 降级模板方案
│   │
│   ├── affiliate_injector.py       # 变现链接注入
│   │   ├── inject_links()          # 智能注入单个链接
│   │   └── smart_inject_multiple() # 多链接策略
│   │
│   └── page_builder.py             # 页面构建器
│       ├── build_homepage()        # 首页生成
│       ├── build_article_page()    # 详情页生成
│       └── build_category_pages()  # 分类页生成
│
├── .github/
│   └── workflows/
│       └── deploy.yml              # GitHub Actions 定时触发器
│
├── public/                         # 生成的静态页面 (运行时创建)
│   ├── index.html                  # 首页
│   ├── stock-analysis/
│   │   └── index.html
│   ├── crypto-analysis/
│   │   └── index.html
│   ├── casino-review/
│   │   └── index.html
│   └── {slug}/
│       └── index.html              # 文章详情页
│
└── docs/
    ├── README.md                   # 完整说明文档
    ├── DEPLOY_GUIDE.md            # 5 分钟快速部署指南
    └── ARCHITECTURE.md            # 本文件
```

---

## 🔄 完整数据流

### 阶段 1: 触发 (Triggering)

```yaml
时间：每 6 小时
触发器：GitHub Actions (cron)
动作：POST 请求到 Vercel Deploy Hook
```

**代码位置**: `.github/workflows/deploy.yml`

```yaml
on:
  schedule:
    - cron: '0 0,6,12,18 * * *'
```

---

### 阶段 2: 构建 (Building)

```yaml
平台：Vercel Build Server
环境：Python 3.9+
触发：Deploy Hook Webhook
```

**流程**:
1. Vercel 拉取 GitHub 最新代码
2. 安装 Python 依赖 (`pip install -r requirements.txt`)
3. 设置环境变量 (从 Vercel Secrets)
4. 执行 `python main.py`

**代码位置**: `main.py`

---

### 阶段 3: 数据采集 (Data Collection)

```yaml
API 源：
  - 股票：Alpha Vantage API
  - 加密货币：CoinGecko API
  - 博彩：The-Odds-API (可选)
降级：模拟数据生成
```

**代码位置**: `src/data_collector.py`

**数据结构示例**:
```python
{
    "AAPL": {
        "symbol": "AAPL",
        "price": 175.25,
        "change_percent": "+2.5%",
        "volume": 50000000,
        "high": 176.0,
        "low": 173.5,
        "timestamp": "2024-03-31T10:00:00"
    }
}
```

---

### 阶段 4: 内容生成 (Content Generation)

```yaml
模型：OpenAI GPT-4-turbo (可降级到 GPT-3.5)
输入：市场数据 + SEO 关键词
输出：800-1200 字专业分析文章
```

**代码位置**: `src/ai_content_generator.py`

**Prompt 结构**:
```
系统指令：你是一位专业的分析师...

用户输入:
【实时数据】
- 当前价格：$XXX
- 涨跌幅：X%
...

【SEO 关键词】
关键词 1, 关键词 2, ...

【文章要求】
1. 标题吸引人...
2. 分析价格走势...
3. 提供投资建议...
```

---

### 阶段 5: 变现注入 (Monetization)

```yaml
策略：基于分类的智能匹配
股票 → Robinhood/Webull 推广链接
加密货币 → Binance/Coinbase 推广链接
博彩 → Bet365/888 Casino 推广链接
```

**代码位置**: `src/affiliate_injector.py`

**注入位置**:
- 文章结尾 CTA
- 第一段落后 (赞助商)
- 中间段落 (数据来源)

---

### 阶段 6: 页面构建 (Page Building)

```yaml
输出：纯 HTML + CSS
优化：响应式设计 + 语义化标签
SEO：Meta tags + 结构化数据
```

**代码位置**: `src/page_builder.py`

**生成页面类型**:
1. **首页** (`public/index.html`)
   - 展示所有最新文章
   - 按分类分组
   - 响应式卡片布局

2. **文章详情页** (`public/{category}/{slug}/index.html`)
   - 完整文章内容
   - 内嵌 Affiliate Links
   - 面包屑导航

3. **分类页** (`public/{category}/index.html`)
   - 该分类下所有文章列表
   - 便于爬虫抓取

---

### 阶段 7: 部署 (Deployment)

```yaml
平台：Vercel
CDN: 全球边缘网络
SSL: 自动 HTTPS
缓存：自动失效机制
```

**输出**:
- 静态 HTML 文件上传到 S3
- DNS 记录更新
- CDN 缓存刷新
- 部署完成通知

---

## 🔧 关键技术选型对比

### 托管平台

| 平台 | 免费版 | Pro 版 | 优势 | 劣势 |
|------|--------|-------|------|------|
| **Vercel** | 100GB/月 | $20/月 (无限) | 生态好，易用 | 超时限制严 |
| **Netlify** | 100GB/月 | $19/月 (无限) | 构建时间长 | 功能略少 |
| **Cloudflare Pages** | 无限 | $5/月 | 便宜，带宽大 | 生态一般 |

**推荐**: Vercel (开发体验最佳)

---

### AI 模型

| 模型 | 成本/千字 | 质量 | 速度 | 推荐场景 |
|------|----------|------|------|---------|
| **GPT-4-turbo** | ~$0.03 | ⭐⭐⭐⭐⭐ | 快 | 高质量内容 |
| **GPT-3.5-turbo** | ~$0.002 | ⭐⭐⭐⭐ | 很快 | 批量生产 |
| **Claude 3** | ~$0.025 | ⭐⭐⭐⭐⭐ | 中等 | 长文分析 |

**推荐**: 初期 GPT-3.5 控制成本，后期混合使用

---

### 数据源

#### 股票数据
- **Alpha Vantage**: 免费 500 次/天 ✅
- **IEX Cloud**: 免费 5 万次/月
- **Polygon.io**: 付费，质量好

#### 加密货币
- **CoinGecko**: 免费 10-50 次/分 ✅
- **CoinMarketCap**: 免费 333 次/天
- **Binance API**: 免费，限币种

#### 博彩赔率
- **The-Odds-API**: 免费 500 次/月 ✅
- **Oddsportal**: 需爬虫

---

## 📊 性能与成本估算

### 单次执行成本

假设每次生成 10 篇文章:

| 项目 | 数量 | 单价 | 小计 |
|------|------|------|------|
| OpenAI API (GPT-3.5) | 10 篇 × 1000 字 | $0.002/千 | $0.02 |
| Alpha Vantage | 10 次 | 免费 | $0 |
| CoinGecko | 1 次 | 免费 | $0 |
| Vercel Build | 1 次 | 免费 | $0 |
| **单次总计** | | | **$0.02** |

### 月度成本 (每天 4 次)

```
$0.02 × 4 次/天 × 30 天 = $2.40/月
```

### 收益预估

假设:
- 每月生成 1200 篇文章
- 每篇文章平均 10 次浏览
- CTR 2% → 240 次点击
- 转化率 3% → 7.2 个转化
- 平均佣金 $80

**月收入**: $576
**月利润**: $573.60

**ROI**: 23900%

---

## 🛡️ 风险控制

### 1. API 限流风险

**问题**: 免费 API 有调用次数限制

**解决方案**:
```python
# 添加缓存层
@cache(ttl=3600)  # 缓存 1 小时
def fetch_stock_data(symbol):
    return api_call()

# 批量获取
def fetch_multiple_symbols(symbols):
    # 一次请求获取多个数据
    pass
```

---

### 2. 内容质量风险

**问题**: AI 生成内容可能重复或低质

**解决方案**:
```python
# 添加多样性参数
response = openai.ChatCompletion.create(
    temperature=0.8,  # 提高随机性
    presence_penalty=0.5,  # 避免重复
    frequency_penalty=0.5
)
```

---

### 3. 封号风险

**问题**: 频繁部署可能触发风控

**解决方案**:
- 降低频率 (改为每天 1-2 次)
- 使用固定 IP 的代理服务
- 准备多个账号轮换

---

### 4. 合规风险

**问题**: 金融/博彩内容可能违规

**解决方案**:
```html
<!-- 添加免责声明 -->
<footer>
  <p>⚠️ 风险提示：投资有风险，入市需谨慎</p>
  <p>本网站内容仅供参考，不构成投资建议</p>
  <p>我们可能从 affiliate links 中获得佣金</p>
</footer>
```

---

## 🚀 扩展方向

### 短期 (1-3 个月)

1. **多语言支持**
   - 添加 i18n 模块
   - 生成英文、日文、韩文内容

2. **图表集成**
   - 使用 Chart.js 绘制 K 线图
   - 技术指标可视化

3. **用户系统**
   - 邮件订阅
   - 付费会员专区

### 中期 (3-6 个月)

1. **多模型融合**
   - A/B 测试不同 AI 效果
   - 自动选择最优模型

2. **社交自动化**
   - 自动生成 Twitter 文案
   - 自动发布到 Reddit

3. **数据分析**
   - 集成 Google Analytics
   - 追踪转化率优化

### 长期 (6-12 个月)

1. **SaaS 化**
   - 开放给第三方使用
   - 按月订阅收费

2. **API 经济**
   - 将数据处理能力 API 化
   - 按调用次数收费

3. **收购退出**
   - 积累稳定现金流
   - 出售给内容农场

---

## 🎯 成功关键因素

### 1. 持续执行
- 前 3 个月可能没流量，坚持更新
- 搜索引擎需要时间收录

### 2. 关键词策略
- 专注长尾关键词 (竞争小)
- 例如："AAPL 股价分析 2024"vs"AAPL"

### 3. 用户体验
- 页面加载速度 < 3 秒
- 移动端友好
- 清晰的信息架构

### 4. 数据驱动
- 每周分析 Google Search Console
- 优化高展现低 CTR 的页面
- 淘汰无效关键词

---

## 📚 学习资源

### 技术栈
- [Vercel 官方文档](https://vercel.com/docs)
- [GitHub Actions 教程](https://docs.github.com/en/actions)
- [OpenAI Cookbook](https://cookbook.openai.com/)

### SEO
- [Google SEO 入门指南](https://developers.google.com/search/docs/beginner/seo-starter-guide)
- [Ahrefs Blog](https://ahrefs.com/blog/)

### 变现
- [Affiliate Marketing 实战](https://www.smartpassiveincome.com/affiliatemarketing/)
- [Niche Site Project](https://nichesiteproject.com/)

---

## 💬 总结

这套架构的核心优势:

✅ **极低启动成本**: <$10 即可开始  
✅ **高度自动化**: 设置后几乎无需维护  
✅ **可扩展性强**: 从一个站点扩展到一百个站点  
✅ **被动收入潜力**: 内容持续产生长尾流量  

**关键建议**: 先跑通 MVP，验证模式后再扩大规模。

---

**最后更新**: 2024-03-31  
**作者**: AI Assistant  
**许可**: MIT License
