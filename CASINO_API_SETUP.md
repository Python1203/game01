# 博彩 API 配置指南

## ✅ 已完成的 API 集成

### 1. **The-Odds-API** 🎲
- **状态**: ✅ 已成功集成并测试通过
- **API Key**: `3838a6272cab9b49dac3d9f646fbca4b`
- **配额**: 每日 500 次免费请求
- **支持赛事**: MLB, NBA, NFL, NHL, NCAA, 足球，网球等
- **数据字段**: 
  - 赛事名称（主队 vs 客队）
  - 比赛时间
  - 体育类型
  - 多家博彩公司赔率（DraftKings, FanDuel 等）

**测试结果**:
```
✓ 获取到 17 场赛事
✓ 包含 NCAA Baseball, MLB, NBA 等赛事
✓ 赔率数据完整（主客队赔率均有）
```

---

### 2. **API-Football/Basketball** ⚽
- **状态**: ✅ 已成功集成并测试通过
- **API Key**: `58ce01aadd6863c36e4c86d807233d25`
- **支持赛事**: 足球、篮球等多种体育项目
- **数据字段**:
  - 实时比分
  - 比赛时间
  - 联赛信息
  - 球队信息

**测试结果**:
```
✓ API 连接成功
✓ 支持全球足球联赛
✓ 实时数据更新
```

---

## 📋 配置步骤

### 方法 1: 使用 .env 文件（推荐）

`.env` 文件已配置好这两个 API:

```bash
# 博彩 API 配置
ODDS_API_KEY=3838a6272cab9b49dac3d9f646fbca4b
SPORTS_API_KEY=58ce01aadd6863c36e4c86d807233d25
```

### 方法 2: 手动修改

编辑 `.env` 文件，确保包含以下配置：

```bash
# The-Odds-API（综合赔率数据）
ODDS_API_KEY=3838a6272cab9b49dac3d9f646fbca4b

# API-Football/Basketball（实时赛事数据）
SPORTS_API_KEY=58ce01aadd6863c36e4c86d807233d25
```

---

## 🧪 测试 API 连接

运行测试脚本：

```bash
python3 test_casino_apis.py
```

**预期输出**:
```
🎰 博彩 API 完整测试 🎰

🎲 测试 The-Odds-API
✓ 连接成功！获取到 17 场赛事

⚽ 测试 API-Football/Basketball
✓ 连接成功！当前有 0 场进行中赛事

🏆 测试 DataCollector 集成
✓ 配置 The-Odds-API，每日限额 500 次
✓ The-Odds-API: 获取到 15 场赛事赔率
✓ API-Football: 获取到 0 场进行中赛事

✅ DataCollector 集成测试完成!
```

---

## 💡 使用建议

### 1. **构建频率优化**

根据 API 配额，建议的构建策略：

| API | 每日限额 | 建议构建次数 | 每次间隔 |
|-----|---------|------------|---------|
| The-Odds-API | 500 次 | 2-3 次 | 6-8 小时 |
| API-Football | 不限 | 按需 | - |

**推荐方案**:
- 每 6 小时构建一次（每天 4 次）
- 或每 8 小时构建一次（每天 3 次）
- 完全在免费额度范围内

### 2. **Vercel Cron 配置**

在 `vercel.json` 中配置定时构建：

```json
{
  "crons": [
    {
      "path": "/api/build",
      "schedule": "0 */6 * * *"
    }
  ]
}
```

这将会：
- 每 6 小时自动构建一次
- 每天消耗约 200-300 次 API 配额
- 保持内容实时更新

### 3. **数据更新策略**

```python
# main.py 中的执行流程
collector.fetch_casino_odds()  # 获取最新赔率数据
# ↓
ai_generator.generate_analysis_article()  # AI 分析赔率趋势
# ↓
page_builder.build_category_pages()  # 生成博彩分析页面
```

---

## 📊 数据示例

### The-Odds-API 返回数据

```json
{
  "event_name": "Seattle Mariners vs New York Yankees",
  "sport": "MLB",
  "commence_time": "2026-03-31T01:41:00Z",
  "odds": [
    {"name": "New York Yankees", "price": 2.06},
    {"name": "Seattle Mariners", "price": 1.74}
  ],
  "source": "The-Odds-API"
}
```

### API-Football 返回数据

```json
{
  "fixture": {
    "status": {"elapsed": 45},
    "venue": {"name": "Stamford Bridge"}
  },
  "teams": {
    "home": {"name": "Chelsea"},
    "away": {"name": "Arsenal"}
  },
  "goals": {
    "home": 1,
    "away": 0
  },
  "league": {
    "name": "Premier League"
  }
}
```

---

## 🔧 故障排除

### 问题 1: API 返回错误

**现象**: 获取不到真实数据，使用模拟数据

**解决**:
1. 检查 `.env` 文件中的 API Key 是否正确
2. 运行 `python3 test_casino_apis.py` 测试连接
3. 查看控制台错误信息

### 问题 2: 配额超限

**现象**: API 返回 429 Too Many Requests

**解决**:
1. 减少构建频率（改为每天 2-3 次）
2. 升级 API 套餐（The-Odds-API 付费版）
3. 使用多个 API Key 轮换

### 问题 3: 数据格式异常

**现象**: 赔率数据为空或格式不对

**解决**:
- 检查 API 返回的原始数据
- 验证 bookmakers 和 markets 字段是否存在
- 添加异常处理逻辑

---

## 📈 性能监控

### 实时监控指标

在 `main.py` 中添加监控：

```python
casino_data = collector.fetch_casino_odds()
print(f"✓ 采集到 {len(casino_data)} 条赔率数据")

if len(casino_data) == 0:
    print("⚠️ 警告：未获取到真实赔率数据")
```

### 日志记录

建议在 Vercel 部署后查看构建日志：
1. 访问 Vercel Dashboard
2. 选择你的项目
3. 查看 Deployments → Latest Deployment → View Build Logs

---

## 🎯 最佳实践

1. **合理使用配额**: 每天 2-3 次构建，避免超限
2. **数据缓存**: 考虑缓存上次结果，减少不必要的 API 调用
3. **错误处理**: 始终准备模拟数据作为备用方案
4. **多源验证**: 结合 The-Odds-API 和 API-Football 的数据

---

## 🔗 相关文档

- [The-Odds-API 官方文档](https://the-odds-api.com/)
- [API-Football 官方文档](https://www.api-football.com/documentation)
- [Vercel Cron 配置文档](https://vercel.com/docs/cron-jobs)

---

**更新时间**: 2026-03-31  
**测试状态**: ✅ 所有 API 已配置并测试通过  
**剩余额度**: 每日 500 次（The-Odds-API）
