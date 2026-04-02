# VIP 系统快速参考卡片

## 🚀 快速启动命令

```bash
# 1. 运行完整测试
python3 test_vip_system.py

# 2. 查看生成的页面
open ./public/test-vip/vip/arsenal-vs-chelsea/index.html

# 3. 检查缓存状态
python3 -c "from src.cache_manager import SmartCache; c=SmartCache(); print(c.get_stats())"
```

---

## 📦 核心模块导入速查

```python
# VIP 数据模型
from src.vip_data_models import (
    BasicMatchData,      # 基础比赛数据
    InjuryInfo,          # 伤停信息
    H2HStats,            # 历史交锋
    AIModelPrediction,   # AI 预测
    VIPMatchAnalysis     # 完整分析
)

# 体育 API
from src.sports_data_api import FootballDataAPI, BasketballDataAPI

# 赔率与 CPS
from src.odds_cps_module import (
    OddsAggregator,           # 赔率聚合
    GeoAffiliateRecommender,  # 区域推荐
    ValueBetFinder            # 价值注发现
)

# 缓存管理
from src.cache_manager import (
    SmartCache,        # 智能缓存
    DataPrefetcher,    # 数据预取
    N8NAutomation      # N8N 集成
)

# 页面构建
from src.vip_page_builder import VIPPageBuilder
```

---

## 💡 常用代码片段

### 创建 VIP 分析
```python
basic = BasicMatchData(
    match_id="match_001",
    home_team="Arsenal",
    away_team="Chelsea",
    league="英超",
    commence_time=datetime.now().isoformat()
)

analysis = VIPMatchAnalysis(
    match_id="match_001",
    basic_data=basic,
    injuries=[injury],
    h2h_stats=h2h,
    ai_prediction=ai_pred
)
```

### 获取赔率对比
```python
aggregator = OddsAggregator()
comparisons = aggregator.get_odds_comparison(
    sport="soccer_epl",
    limit=5
)
```

### 生成页面
```python
builder = VIPPageBuilder()
filepath = builder.build_vip_match_page(
    analysis, 
    user_tier="vip_premium"
)
```

### 使用缓存
```python
cache = SmartCache()

# 写入
cache.set("key", data, "odds")

# 读取
data = cache.get("key")
```

---

## 🎯 API 配额参考

| API | 免费额度 | 建议频率 | 缓存 TTL |
|-----|---------|---------|---------|
| The-Odds-API | 500/天 | 每 5 分钟 | 5 分钟 |
| API-Football | 100/天 | 每小时 | 60 分钟 |
| Finnhub | 60/分钟 | 按需 | 30 分钟 |

---

## 🔑 环境变量配置

```bash
# .env 文件
SPORTS_API_KEY=your_api_key_here
ODDS_API_KEY=your_odds_key_here
N8N_WEBHOOK_URL=https://your-n8n.com/webhook
```

---

## 📊 会员层级定价

| 层级 | 价格 | 内容 | 目标用户 |
|------|------|------|---------|
| Free | $0 | 比分、赛程 | 普通用户 |
| VIP Basic | $29/月 | 伤停、新闻 | 业余爱好者 |
| VIP Premium | $99/月 | H2H、AI 预测、价值注 | 专业玩家 |

---

## 🎨 页面组件速览

```
VIP 页面结构:
├── Header (比赛头部)
├── Basic Info Card (基础信息)
├── VIP Section (VIP 内容区)
│   ├── Injuries (伤停 - VIP Basic)
│   ├── H2H Stats (H2H-VIP Premium)
│   └── AI Prediction (AI 预测 - VIP Premium)
├── Odds Comparison (赔率对比)
└── CTA Section (行动号召)
```

---

## ⚠️ 常见错误处理

```python
# API 403 错误
try:
    fixtures = api.get_fixtures()
except Exception as e:
    print(f"API 错误：{e}")
    fixtures = []  # 返回空数据

# 缓存未命中
cached = cache.get("key")
if not cached:
    # 从 API 重新获取
    data = fetch_from_api()
    cache.set("key", data, "odds")
```

---

## 📈 关键指标监控

```python
# 每日追踪
metrics = {
    "vip_conversions": 15,      # VIP 转化数
    "cps_clicks": 234,          # CPS 点击数
    "value_bet_hit_rate": 0.72, # 价值注命中率
    "cache_hit_rate": 0.85,     # 缓存命中率
    "api_calls_saved": 450      # 节省的 API 调用
}
```

---

## 🔗 文档索引

- **详细指南**: `VIP_SYSTEM_GUIDE.md`
- **实施总结**: `VIP_IMPLEMENTATION_SUMMARY.md`
- **测试脚本**: `test_vip_system.py`
- **源码位置**: `src/*.py`

---

**更新日期**: 2026-04-02  
**版本**: v1.0.0
