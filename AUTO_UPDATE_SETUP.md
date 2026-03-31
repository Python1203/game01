# 自动变现定时器配置指南

## 🎯 目标
实现每 4 小时自动更新行情数据并重生成网页内容

## 📋 配置步骤

### 方案一：使用 cron-job.org（推荐，免费）

#### 1️⃣ 获取 Vercel Deploy Hook URL
```
https://api.vercel.com/v1/integrations/deploy/prj_KFkupuzQ0mfriKcFV0CvrtkgsKs9/JY4klVbJha
```

**手动获取路径：**
- Vercel 控制面板 → Settings → Git
- 找到 **Deploy Hooks** 部分
- 点击 **Create Hook by Git Provider**
- 命名：`AutoUpdate`
- 复制生成的 URL

#### 2️⃣ 注册 cron-job.org
1. 访问 [https://cron-job.org](https://cron-job.org)
2. 注册免费账号
3. 登录后点击 **Create cron job**

#### 3️⃣ 配置定时任务
- **URL:** 粘贴上面的 Deploy Hook URL
- **Schedule:** 
  - `*/4 * * * *` (每 4 小时执行一次)
  - 或使用预设：`Every 4 hours`
- **Timeout:** 设置为 300 秒（5 分钟）
- **Email notifications:** 可选（失败时通知）

#### 4️⃣ 测试
- 点击 **Execute now** 立即测试
- 检查 Vercel 控制台是否触发部署

---

### 方案二：GitHub Actions（备用方案）

如果 cron-job.org 不可用，可以启用 GitHub Actions：

#### 1️⃣ 设置 Secret
在 GitHub 仓库的 **Settings → Secrets and variables → Actions** 中添加：
- **Name:** `VERCEL_DEPLOY_HOOK`
- **Value:** `https://api.vercel.com/v1/integrations/deploy/prj_KFkupuzQ0mfriKcFV0CvrtkgsKs9/JY4klVbJha`

#### 2️⃣ 启用 Actions
- 确保 `.github/workflows/deploy.yml` 存在
- Actions 默认可能是禁用的，需要手动启用一次

#### 3️⃣ 修改频率（可选）
编辑 `deploy.yml` 的 cron 表达式：
```yaml
on:
  schedule:
    # 每 4 小时执行一次
    - cron: '0 0,4,8,12,16,20 * * *'
```

---

## 🔍 验证自动化

### 检查清单
- [ ] cron-job 状态显示为 **Active**
- [ ] 下次执行时间正确
- [ ] Vercel 部署历史中有自动触发的记录
- [ ] `public/` 目录下的 HTML 文件时间戳已更新

### 监控建议
1. **第一周：** 每天检查 cron-job 是否正常执行
2. **稳定后：** 每周检查 1-2 次
3. **异常处理：** 如果连续失败，检查：
   - Deploy Hook URL 是否正确
   - Vercel 账户是否有可用额度
   - Python 脚本是否有错误

---

## 💡 优化建议

### 内容更新策略
- **币圈数据：** 每 4 小时更新（高波动）
- **美股数据：** 每日更新（盘后数据）
- **AI 分析：** 每次数据更新后重新生成

### SEO 优化
- 每次生成新页面时更新 `<lastmod>` 标签
- 添加发布时间戳到 HTML meta 标签
- 确保每个页面有唯一的 title 和 description

---

## ⚠️ 注意事项

1. **Vercel 额度限制：**
   - 免费版每月 100GB 带宽
   - 每次构建约消耗少量额度
   - 建议监控使用量

2. **API 限流：**
   - ccxt/yfinance 可能有请求限制
   - 考虑添加重试机制
   - 必要时使用付费 API

3. **错误处理：**
   - 建议在 `build.py` 中添加 try-catch
   - 失败时发送通知到邮箱

---

## 📞 快速链接

- [Vercel Deploy Hooks 文档](https://vercel.com/docs/deploy-hooks)
- [cron-job.org 教程](https://cron-job.org/en/help/)
- [GitHub Actions 调度文档](https://docs.github.com/en/actions/writing-workflows/choosing-when-your-workflow-runs/events-that-trigger-workflows#schedule)

---

**最后更新时间：** 2026-03-31  
**状态：** ✅ 待配置
