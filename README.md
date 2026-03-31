# Stock/Crypto/Casino 热门流量全自动流水线

## 📋 项目简介

这是一个基于 Python + Vercel 的自动化内容生成系统，专为 Stock/Crypto/Casino 领域的流量变现设计。

### 核心特性

- ✅ **自动化数据采集**: 从多个 API 获取实时行情数据
- ✅ **AI 内容生成**: 使用 GPT-4 生成 SEO 优化的投资分析文章
- ✅ **智能变现**: 自动注入 Affiliate Links
- ✅ **静态站点生成**: 构建 HTML 页面并部署到全球 CDN
- ✅ **零服务器成本**: 利用 Vercel Serverless 架构

---

## 🚀 快速开始

### 1. 环境准备

```bash
# 安装依赖
pip install openai requests python-dotenv
```

### 2. 配置环境变量

创建 `.env` 文件:

```bash
# AI 配置
OPENAI_API_KEY=your_openai_api_key_here

# 数据源配置
ALPHA_VANTAGE_KEY=demo  # 或使用付费 key
FINNHUB_KEY=d6rihfpr01qr194ms4ngd6rihfpr01qr194ms4o0  # 美股/全球市场数据
ODDS_API_KEY=3838a6272cab9b49dac3d9f646fbca4b  # The-Odds-API（博彩赔率）
SPORTS_API_KEY=58ce01aadd6863c36e4c86d807233d25  # API-Football/Basketball

# 变现配置
AFFILIATE_LINKS=https://your-affiliate-link-1.com,https://your-affiliate-link-2.com
BINANCE_AFFILIATE_LINK=https://www.binance.com/activity/referral-entry/CPA?ref=CPA_007OA94MQ0  # 币安返佣链接（加密货币专用）
```

### 3. 本地测试

```bash
# 运行主程序
python main.py
```

---

## 🏗️ 架构说明

### 工作流程

```
定时触发器 → Vercel Deploy Hook → Build Server
    ↓
拉取代码 → 运行 Python 脚本
    ↓
① 采集数据 → ② AI 生成 → ③ 注入链接 → ④ 构建页面
    ↓
部署到 CDN → 用户访问
```

### 目录结构

```
.
├── main.py                 # 主入口
├── src/
│   ├── data_collector.py   # 数据采集模块
│   ├── ai_content_generator.py  # AI 内容生成
│   ├── affiliate_injector.py    # 变现链接注入
│   └── page_builder.py     # 页面构建器
├── public/                 # 生成的静态页面 (自动创建)
├── vercel.json            # Vercel 配置
├── requirements.txt       # Python 依赖
└── README.md
```

---

## ⚙️ Vercel 部署配置

### 步骤 1: 创建 Vercel 账号

访问 [vercel.com](https://vercel.com) 注册账号

### 步骤 2: 连接 GitHub 仓库

1. 将代码推送到 GitHub
2. 在 Vercel Dashboard 点击 "New Project"
3. 导入 GitHub 仓库

### 步骤 3: 配置环境变量

在 Vercel 项目设置中添加:

- `OPENAI_API_KEY`: OpenAI API 密钥
- `ALPHA_VANTAGE_KEY`: Alpha Vantage API 密钥
- `AFFILIATE_LINKS`: 变现链接 (逗号分隔)
- `BINANCE_AFFILIATE_LINK`: 币安返佣链接（加密货币文章专用）

### 步骤 4: 获取 Deploy Hook URL

1. 进入 Vercel 项目 → Settings → Git
2. 复制 "Deploy Hook" URL
3. 保存备用

格式：`https://api.vercel.com/v1/integrations/deploy/prj_xxx/xxx`

---

## ⏰ 配置定时触发

### 方案 1: GitHub Actions (推荐)

创建 `.github/workflows/deploy.yml`:

```yaml
name: Trigger Vercel Deploy

on:
  schedule:
    - cron: '0 */6 * * *'  # 每 6 小时执行一次
  workflow_dispatch:       # 允许手动触发

jobs:
  trigger:
    runs-on: ubuntu-latest
    steps:
      - name: Trigger Vercel Deploy Hook
        run: curl -X POST ${{ secrets.VERCEL_DEPLOY_HOOK }}
```

**配置步骤:**

1. 在 GitHub 仓库创建 `.github/workflows/deploy.yml`
2. 在 GitHub Settings → Secrets 添加 `VERCEL_DEPLOY_HOOK`
3. Commit 并推送

### 方案 2: 在线 Cron 服务

使用免费的 Cron 工具:

- [cron-job.org](https://cron-job.org) - 免费版每分钟 1 次
- [EasyCron](https://easycron.com) - 免费版每 15 分钟 1 次

配置示例:
```
URL: https://api.vercel.com/v1/integrations/deploy/prj_xxx/xxx
Method: POST
Schedule: */30 * * * *  (每 30 分钟)
```

### 方案 3: 自建触发器

使用 Python 脚本 + 服务器 crontab:

```python
# trigger_deploy.py
import requests

def trigger():
    url = "YOUR_VERCEL_DEPLOY_HOOK_URL"
    response = requests.post(url)
    print(f"Status: {response.status_code}")

if __name__ == "__main__":
    trigger()
```

```bash
# crontab -e
0 */6 * * * /usr/bin/python3 /path/to/trigger_deploy.py
```

---

## 💰 变现策略

### Affiliate Programs 推荐

#### 股票/ETF
- **Robinhood**: https://robinhood.com/us/en/support/articles/affiliate-program/
- **Webull**: https://www.webull.com/affiliate
- **TD Ameritrade**: https://www.tdameritrade.com/affiliate

#### 加密货币
- **Binance**: https://www.binance.com/en/affiliate
- **Coinbase**: https://www.coinbase.com/earn
- **Kraken**: https://www.kraken.com/features/affiliate

#### 博彩
- **Bet365**: https://affiliates.bet365.com/
- **888 Casino**: https://www.888affiliates.com/
- **DraftKings**: https://partners.draftkings.com/

### 优化建议

1. **链接位置**: 在文章高潮部分自然插入 CTA
2. **A/B 测试**: 使用不同文案测试转化率
3. **合规性**: 添加免责声明和风险提示
4. **多样化**: 混合使用多个平台链接降低风险

---

## 📡 API 集成说明

### 已集成的 API

#### 1. **股票/市场数据**
- **Finnhub API**: 美股、港股、A 股、指数数据
  - Token: `d6rihfpr01qr194ms4ngd6rihfpr01qr194ms4o0`
  - 配额：60 次/分钟（免费版）
  - 文档：https://finnhub.io/docs/api

- **Alpha Vantage**: 备用股票数据源
  - Key: `demo`（建议申请免费 Key：500 次/天）
  - 文档：https://www.alphavantage.co

#### 2. **加密货币数据**
- **Binance API**: 实时币价、24h 涨跌幅
  - 无需 API Key（公开接口）
  - 配额：无限制
  - 文档：https://binance-docs.github.io/apidocs/

- **CoinGecko**: 备用加密货币数据
  - 无需 API Key（免费版）
  - 配额：10-50 次/分钟
  - 文档：https://www.coingecko.com/en/api/documentation

#### 3. **博彩/体育数据** ✅ 新增
- **The-Odds-API**: 综合赔率数据
  - Key: `3838a6272cab9b49dac3d9f646fbca4b`
  - 配额：**500 次/天**（免费版）
  - 支持：MLB, NBA, NFL, NHL, NCAA, 足球等
  - 文档：https://the-odds-api.com/

- **API-Football/Basketball**: 实时体育赛事
  - Key: `58ce01aadd6863c36e4c86d807233d25`
  - 支持：足球、篮球等多种体育项目
  - 文档：https://www.api-football.com/documentation

### API 使用策略

| API | 每日限额 | 建议调用频率 | 用途 |
|-----|---------|-------------|------|
| The-Odds-API | 500 次 | 每 6-8 小时 1 次 | 博彩赔率分析 |
| API-Football | 不限 | 按需 | 实时赛事数据 |
| Finnhub | 60 次/分钟 | 按需 | 股票/指数行情 |
| Binance | 不限 | 按需 | 加密货币价格 |

### 构建频率建议

根据 The-Odds-API 的配额（500 次/天），推荐：

```yaml
# GitHub Actions cron 配置
- cron: '0 */6 * * *'  # 每 6 小时一次（每天 4 次，每次约 50 次调用 = 200 次/天）
- cron: '0 */8 * * *'  # 每 8 小时一次（每天 3 次，更保守）
```

### 测试 API 连接

```bash
# 测试所有 API
python3 test_casino_apis.py

# 测试股票/加密 API
python3 test_api_integration.py
```

详细配置指南请查看：[CASINO_API_SETUP.md](./CASINO_API_SETUP.md)

---

## 📊 性能优化

### 成本控制

| 项目 | 免费额度 | 优化策略 |
|------|---------|---------|
| Vercel | 100GB/月 | 压缩图片，减少构建频率 |
| OpenAI | 按量付费 | 使用 GPT-3.5-turbo 降低成本 |
| Alpha Vantage | 500 次/天 | 缓存数据，合并请求 |
| CoinGecko | 10-50 次/分 | 批量获取，避免重复 |

### SEO 优化

1. **关键词研究**: 使用 Ahrefs/Semrush 发现高价值关键词
2. **Meta 标签**: 每篇文章包含独特的 title/description
3. **内部链接**: 相关文章互相链接
4. **页面速度**: 静态 HTML + CDN 确保秒开
5. **移动友好**: 响应式设计

---

## 🔧 常见问题

### Q1: 构建失败怎么办？

检查 Vercel 构建日志:
```bash
# 查看错误信息
vercel logs your-deployment-id
```

常见原因:
- API Key 失效 → 更新环境变量
- 依赖缺失 → 检查 `requirements.txt`
- 超时 → 优化代码或升级 Vercel 套餐

### Q2: 如何增加生成频率？

修改 GitHub Actions cron 表达式:
```yaml
# 每小时执行一次
- cron: '0 * * * *'

# 每 30 分钟执行一次
- cron: '*/30 * * * *'
```

### Q3: 如何扩展支持更多市场？

在 `data_collector.py` 中添加新的数据源:

```python
def fetch_forex_data(self, pairs: List[str]) -> Dict:
    """获取外汇数据"""
    # 实现逻辑
    pass
```

---

## 📈 扩展功能

### 待开发功能

- [ ] 添加更多数据源 (Forex, Commodities)
- [ ] 集成 Claude/Mistral 等多模型
- [ ] 自动生成图表和技术分析
- [ ] 多语言支持
- [ ] 用户评论系统
- [ ] 邮件订阅功能
- [ ] Analytics 数据追踪

---

## ⚠️ 法律合规

### 重要声明

1. **投资建议免责**: 网站内容仅供参考，不构成投资建议
2. **风险提示**: 必须包含明确的风险警示
3. **Affiliate 披露**: 声明可能获得佣金
4. **版权合规**: 确保数据源允许商业使用
5. **地区限制**: 某些地区可能禁止博彩推广

### 建议措施

- 在页脚添加免责声明
- 遵守 FTC 关于 Affiliate 披露的规定
- 咨询法律专业人士确保合规

---

## 🤝 贡献与反馈

欢迎提交 Issue 和 Pull Request!

---

## 📄 许可证

MIT License

---

## 📬 联系方式

如有问题请提交 Issue 或联系开发者。

---

**🎯 关键结论**: 这套架构的核心价值在于**零边际成本扩张**——每篇文章的生成成本约$0.02，但可能带来持续的被动收入。成功的关键是**持续输出高质量内容** + **精准的关键词选择**。
