# 🚀 5 分钟快速部署指南

## 前提条件

- ✅ GitHub 账号
- ✅ Vercel 账号 (免费)
- ✅ OpenAI API Key
- ✅ Python 基础

---

## 步骤 1: 准备代码 (2 分钟)

### 1.1 初始化 Git 仓库

```bash
cd /Users/zzw868/PycharmProjects/PythonProject

# 初始化 git
git init

# 添加所有文件
git add .

# 提交
git commit -m "Initial commit: Stock/Crypto/Casino 自动化系统"
```

### 1.2 推送到 GitHub

```bash
# 创建新仓库 (在 GitHub 上)
# 访问 https://github.com/new 创建仓库

# 然后执行
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git branch -M main
git push -u origin main
```

---

## 步骤 2: 配置 Vercel (3 分钟)

### 2.1 导入项目

1. 登录 [vercel.com](https://vercel.com)
2. 点击 **"Add New Project"**
3. 选择 **"Import Git Repository"**
4. 找到刚才的仓库，点击 **"Import"**

### 2.2 设置环境变量

在 Vercel 项目设置页面，添加以下环境变量:

| Name | Value | 获取方式 |
|------|-------|---------|
| `OPENAI_API_KEY` | `sk-...` | https://platform.openai.com/api-keys |
| `ALPHA_VANTAGE_KEY` | `demo` 或你的 key | https://www.alphavantage.co/support/#api-key |
| `AFFILIATE_LINKS` | `https://your-link.com` | 你的推广链接 |

### 2.3 首次部署

1. 点击 **"Deploy"**
2. 等待构建完成 (约 1-2 分钟)
3. 看到 ✅ 表示成功

---

## 步骤 3: 配置自动触发 (2 分钟)

### 3.1 获取 Deploy Hook URL

1. 在 Vercel 项目页面 → **Settings** → **Git**
2. 找到 **"Deploy Hooks"**
3. 点击 **"Create Deploy Hook"**
4. 命名 (如 "Auto Trigger")
5. 复制生成的 URL

格式：`https://api.vercel.com/v1/integrations/deploy/prj_xxx/xxx`

### 3.2 配置 GitHub Secrets

1. 在 GitHub 仓库页面 → **Settings**
2. 左侧 → **Secrets and variables** → **Actions**
3. 点击 **"New repository secret"**
4. 添加:
   - Name: `VERCEL_DEPLOY_HOOK`
   - Value: 刚才复制的 URL

### 3.3 启用 GitHub Actions

1. 在 GitHub 仓库页面 → **Actions**
2. 如果是第一次使用，点击 **"I understand my workflows, go ahead and enable them"**
3. 你会看到 "Trigger Vercel Deploy" workflow
4. 默认每 6 小时自动执行

---

## 步骤 4: 测试验证 (1 分钟)

### 4.1 手动触发部署

```bash
# 方法 1: 在 GitHub Actions 页面手动运行
# 进入 Actions → Trigger Vercel Deploy → Run workflow

# 方法 2: 本地 curl 测试
curl -X POST YOUR_VERCEL_DEPLOY_HOOK_URL
```

### 4.2 检查部署状态

1. 访问 Vercel Dashboard
2. 查看最新部署状态
3. 点击预览链接查看网站

### 4.3 本地测试 (可选)

```bash
# 安装依赖
pip install openai requests python-dotenv

# 复制环境变量
cp .env.example .env
# 编辑 .env 填入你的 API Key

# 运行测试
python test_local.py
```

---

## 🎉 完成!

现在你已经拥有:

- ✅ 自动运行的内容生成系统
- ✅ 每 6 小时自动更新内容
- ✅ 全球 CDN 加速访问
- ✅ 零服务器维护成本

---

## 💡 优化建议

### 调整更新频率

编辑 `.github/workflows/deploy.yml`:

```yaml
# 每小时更新
schedule:
  - cron: '0 * * * *'

# 每天更新
schedule:
  - cron: '0 0 * * *'
```

### 降低成本

1. **减少 AI 调用**: 每次生成少量文章
2. **降低更新频率**: 从每小时改为每天
3. **使用 GPT-3.5**: 比 GPT-4 便宜 10 倍

### 提高收益

1. **增加关键词覆盖**: 生成更多长尾关键词文章
2. **优化 CTA 位置**: A/B 测试不同位置
3. **多渠道变现**: 混合多个 Affiliate 项目

---

## ⚠️ 常见问题

### Q: 构建超时怎么办？

A: Vercel 免费版限制 60 秒，可以:
1. 减少每次生成的文章数量
2. 升级到 Pro ($20/月，900 秒限制)
3. 优化代码减少 API 调用时间

### Q: API 额度不够怎么办？

A: 
- Alpha Vantage 免费 500 次/天 → 缓存数据
- OpenAI 按量付费 → 控制生成数量
- 考虑升级 API 套餐

### Q: 如何查看错误日志？

A:
```bash
# 安装 Vercel CLI
npm install -g vercel

# 查看日志
vercel logs your-deployment-url
```

---

## 📊 预期效果

### 成本结构

| 项目 | 费用 |
|------|------|
| Vercel | $0 (免费版够用) |
| OpenAI | ~$5-20/月 (取决于生成量) |
| 域名 | $10-15/年 (可选) |
| **总计** | **~$10-30/月** |

### 收益潜力

假设:
- 每天生成 10 篇文章
- 每篇文章带来 5 次点击
- 转化率 2%
- 平均佣金 $50

**月收入预估**: $150-500+

---

## 🔗 相关资源

- [Vercel 文档](https://vercel.com/docs)
- [GitHub Actions 文档](https://docs.github.com/en/actions)
- [OpenAI API 文档](https://platform.openai.com/docs)
- [Alpha Vantage API](https://www.alphavantage.co/documentation/)

---

**🎯 下一步**: 开始部署，遇到问题随时查看 README.md 中的详细说明!
