# 足球预测生成器 - 使用指南

## 🎯 核心功能

本系统采用**双引擎架构**：
1. **实时赔率采集引擎** - The Odds API
2. **AI 深度分析引擎** - DeepSeek AI

生成专业的足球比赛预测页面，包含实时赔率对比和 AI 分析文章。

---

## 📋 环境配置

### 1. 环境变量设置

在 `.env` 文件中配置以下变量：

```bash
# DeepSeek AI 配置
DEEPSEEK_API_KEY=sk-hhLctSyNcXyKrkcTL0i1IZ4vHQ9ELl4lQFsZuSzArDGpxVel
DEEPSEEK_BASE_URL=https://xh.v1api.cc

# 博彩 API 配置
ODDS_API_KEY=3838a6272cab9b49dac3d9f646fbca4b  # The-Odds-API
SPORTS_API_KEY=58ce01aadd6863c36e4c86d807233d25  # API-Football（可选）
```

### 2. API 配额说明

| API | 免费额度 | 建议频率 | 当前配置 |
|-----|---------|---------|---------|
| The Odds API | 500 次/月 | 每天 2 次 | ✅ 符合（60 次/月） |
| API-Football | 100 次/天 | 按需 | ✅ 可选 |
| DeepSeek AI | 按量付费 | 按需 | ✅ 充足 |

---

## 🚀 快速开始

### 本地测试

```bash
# 1. 进入目录
cd vercel-money-factory

# 2. 安装依赖
pip install -r requirements.txt

# 3. 运行测试
python3 test_football_predictions.py
```

**预期输出**:
```
⚽ 足球预测生成器 - 完整测试 ⚽

📊 测试数据采集模块
✓ 获取到 3 场比赛

🤖 测试 AI 预测生成
✓ AI 分析完成：Manchester City vs Liverpool

🏗️ 测试内容构建模块
✓ 生成页面：test_output/arsenal-vs-chelsea.md
```

### 完整构建

```bash
# 生成预测页面
python3 build_football_predictions.py

# 检查输出
ls -la src/pages/predictions/
```

### Astro 开发预览

```bash
# 启动开发服务器
npm install
npx astro dev
```

访问 `http://localhost:4321/predictions/arsenal-vs-chelsea` 查看效果

---

## 🏗️ 文件结构

```
vercel-money-factory/
├── build_football_predictions.py    # 主构建脚本
├── test_football_predictions.py     # 测试脚本
├── vercel.json                      # Vercel 配置（含 Cron）
├── src/
│   ├── components/
│   │   ├── OddsDisplay.astro        # 赔率展示组件
│   │   └── VIPPredictionBox.astro   # VIP 解锁框组件
│   ├── pages/
│   │   └── predictions/             # 生成的预测页面
│   └── layouts/
│       └── BaseLayout.astro         # 基础布局
└── dist/                            # 构建输出
```

---

## 📊 生成的页面结构

每个预测页面包含：

### 1. SEO 优化部分
```markdown
title: "Arsenal vs Chelsea Prediction & Best Betting Odds 2026"
description: "Professional Arsenal vs Chelsea prediction with real-time odds analysis..."
keywords: "Arsenal vs Chelsea, betting tips, prediction, best odds, football analysis"
```

### 2. 实时赔率对比表
| 结果 | 最佳赔率 | 博彩公司 |
|------|---------|---------|
| 主胜 | 2.25 | Bet365 |
| 平局 | 3.30 | Pinnacle |
| 客胜 | 3.10 | Stake |

→ **CTA 按钮**: "立即投注领 $1000 奖金"

### 3. AI 深度分析
- 技战术分析（阵型、关键球员、伤病）
- 赔率变化趋势
- 专业投注建议（亚盘、大小球）

### 4. VIP 变现框
→ **CTA 按钮**: "加入电报 VIP 频道"

### 5. Schema 标记
```json
{
  "@context": "https://schema.org",
  "@type": "Event",
  "name": "Arsenal vs Chelsea",
  "startDate": "2026-04-06T17:30:00Z"
}
```

---

## ⚙️ Vercel 部署

### 自动构建配置

`vercel.json`:
```json
{
  "buildCommand": "pip install -r requirements.txt && python build_football_predictions.py && astro build",
  "crons": [
    {
      "path": "/api/build",
      "schedule": "0 2,10 * * *"
    }
  ]
}
```

**构建时间**: 
- 北京时间 10:00（上午）
- 北京时间 18:00（傍晚）

**每月消耗**: ~60 次 API 配额（远低于 500 次限额）

### 手动触发部署

```bash
# 提交代码并推送
git add .
git commit -m "Update predictions"
git push origin main

# Vercel 会自动构建
```

---

## 💰 变现策略

### 双重 CTA 路径

#### A. 即时变现（博彩平台）
```html
<div class="odds-compare">
    <p>最高赔率来自 Stake: <strong>2.10</strong></p>
    <a href="/go/stake" class="btn">立即投注领 $1000 奖金</a>
</div>
```

**链接隐藏**: 使用 Cloudflare 转发
```
869.us.kg/go/stake → 你的 Affiliate 链接
```

#### B. 长线变现（VIP 社群）
```html
<div class="vip-box">
    <p>想解锁此场比赛的【必发波胆】预测吗？</p>
    <a href="/go/telegram" class="btn-tg">加入电报 VIP 频道</a>
</div>
```

**定价策略**: 首月 $99 | 续费 $49/月

---

## ⚠️ 风险控制

### 1. API 配额管理

**The Odds API**: 500 次/月
- ✅ 当前配置：每天 2 次 × 30 天 = 60 次/月
- ✅ 每次构建：获取 5 场比赛 ≈ 5 次调用
- ✅ 月度总消耗：~60 次（安全范围）

**建议**: 如需增加频率，考虑升级到付费版

### 2. 合规声明

**必须在页脚添加**:
```html
<footer>
    <p>⚠️ 博彩有风险，请理性投注 | 18+ | BeGambleAware.org</p>
    <p>Gambling involves risk. Please gamble responsibly. 18+</p>
</footer>
```

### 3. SEO 安全

**避免过度优化**:
- ✅ 关键词自然分布（密度 2-3%）
- ✅ 不使用隐藏文本
- ✅ 不堆砌关键词
- ✅ 提供真实有价值的内容

---

## 🔧 故障排除

### 问题 1: API 返回 404

**原因**: API Key 无效或端点错误

**解决**:
```bash
# 检查 API Key 是否正确
echo $ODDS_API_KEY

# 测试 API 连接
curl "https://api.the-odds-api.com/v4/sports/soccer_epl/odds?regions=uk&markets=h2h&apiKey=YOUR_KEY"
```

### 问题 2: AI 生成失败

**原因**: DeepSeek API Key 失效

**解决**:
```bash
# 检查 DeepSeek 配置
python3 -c "import os; print(os.getenv('DEEPSEEK_API_KEY'))"

# 测试 DeepSeek 连接
python3 test_deepseek.py
```

### 问题 3: Astro 构建失败

**原因**: 依赖缺失

**解决**:
```bash
# 重新安装依赖
npm install
pip install -r requirements.txt

# 清理缓存
rm -rf node_modules .astro
npm install
```

---

## 📈 性能优化

### 1. 减少 API 调用

**策略**: 缓存上次结果
```python
import json
import os

def load_cached_data():
    if os.path.exists('cached_matches.json'):
        with open('cached_matches.json', 'r') as f:
            return json.load(f)
    return None
```

### 2. 批量处理

**一次请求获取多场比赛**:
```python
matches = collector.get_combined_matches(limit=5)  # 一次 API 调用获取 5 场
```

### 3. 异步构建

**并行生成多个页面**:
```python
from concurrent.futures import ThreadPoolExecutor

with ThreadPoolExecutor() as executor:
    executor.map(build_match_page, matches, analyses)
```

---

## 🎯 成功指标

### SEO 排名追踪

**目标关键词**:
- "Best odds for [Match]"
- "[Team A] vs [Team B] prediction"
- "Football betting tips today"

**工具**: Google Search Console, Ahrefs

### 变现指标

| 指标 | 目标值 | 追踪方式 |
|------|--------|---------|
| CTR (CTA 点击率) | > 3% | Google Analytics |
| VIP 转化率 | > 1% | Telegram Bot 统计 |
| 月收入 | $500+ | Affiliate Dashboard |

---

## 📞 技术支持

遇到问题？

1. 查看测试日志：`python3 test_football_predictions.py`
2. 检查 Vercel 构建日志
3. 提交 Issue 到 GitHub

---

**更新时间**: 2026-03-31  
**版本**: v1.0.0  
**状态**: ✅ 可投入生产使用
