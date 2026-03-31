# Astro Money Factory - 快速部署指南

## ✅ 项目结构

```
vercel-money-factory/
├── requirements.txt          # Python 依赖
├── package.json             # Node.js 配置 & 构建指令
├── build_content.py         # 内容生成脚本
├── vercel.json              # Vercel 部署配置
├── .gitignore              # Git 忽略文件
├── start.sh                # 本地启动脚本
└── src/
    ├── layouts/
    │   └── BaseLayout.astro  # SEO 布局模板（含 JSON-LD）
    └── pages/
        ├── index.astro       # 首页
        └── crypto/           # 自动生成的币种页面
            ├── btc.md
            ├── eth.md
            └── sol.md
```

---

## 🚀 一键部署流程

### 1️⃣ 推送到 GitHub

在 PyCharm 中：
```bash
git init
git add .
git commit -m "Initial commit: Astro Money Factory"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/astro-money-factory.git
git push -u origin main
```

### 2️⃣ 关联 Vercel

1. 登录 [Vercel](https://vercel.com)
2. 点击 **Add New → Project**
3. 选择 **Import Git Repository**
4. 找到你的仓库 `astro-money-factory`
5. 点击 **Import**

### 3️⃣ 配置环境变量（重要）

在 Vercel 项目设置页的 **Environment Variables** 中添加：

| 变量名 | 值 | 说明 |
|--------|-----|------|
| `OPENAI_API_KEY` | `sk-xxx` | AI 内容生成（可选） |
| `BINANCE_AFFILIATE_LINK` | `https://...` | 币安返佣链接 |

### 4️⃣ 点击 Deploy

Vercel 会自动执行：
```bash
pip install -r requirements.txt
python3 build_content.py        # 生成 3 个 MD 页面
npm install
npm run build                   # Astro 编译到 dist/
```

部署成功后，你会获得一个 `https://astro-money-factory.vercel.app` 域名。

---

## ⏰ 设置自动更新（躺平赚钱核心）

### 方案：使用 Vercel Deploy Hooks + cron-job.org

#### 步骤 1：创建 Deploy Hook

1. 在 Vercel 项目面板 → **Settings → Git**
2. 找到 **Deploy Hooks** 部分
3. 点击 **Create Hook by Git Provider**
4. 命名：`AutoUpdate`
5. 复制生成的 URL（示例）：
   ```
   https://api.vercel.com/v1/integrations/deploy/prj_xxx/yyy
   ```

#### 步骤 2：配置定时任务

1. 访问 [cron-job.org](https://cron-job.org)
2. 注册免费账号
3. 点击 **Create cron job**
4. 填写：
   - **URL:** 粘贴 Deploy Hook URL
   - **Schedule:** `0 */4 * * *` (每 4 小时)
   - **Timeout:** 300 秒

#### 效果

✅ 每 4 小时自动触发：
- Vercel 重新运行 `build_content.py`
- 采集最新行情数据
- 生成新的 HTML 页面
- Google 索引更新（SEO 友好）

---

## 🛠 本地开发测试

### 快速启动

```bash
cd vercel-money-factory
chmod +x start.sh
./start.sh
```

这会自动：
1. 安装 Python 依赖
2. 运行内容生成脚本
3. 安装 Node 依赖
4. 启动开发服务器（http://localhost:4321）

### 手动步骤

```bash
# 安装依赖
pip3 install -r requirements.txt
npm install

# 生成内容
python3 build_content.py

# 启动开发服务器
npm run dev
```

---

## 📊 SEO 优化特性

### 已集成

- ✅ **JSON-LD 结构化数据** - Google 显示价格、星级
- ✅ **Meta 标签优化** - Open Graph / Twitter Card
- ✅ **语义化 HTML** - 更好的可访问性
- ✅ **响应式设计** - 移动端友好
- ✅ **自动生成 sitemap** - Astro 插件（可选）

### 自定义建议

在 `BaseLayout.astro` 中添加：
- Google Analytics
- 社交媒体分享按钮
- 相关文章推荐

---

## 💰 变现优化

### 返佣链接植入位置

1. **文章底部 CTA**
   ```markdown
   [Click here to trade BTC on Binance with 20% cashback](YOUR_AFF_LINK)
   ```

2. **侧边栏广告位**（可在 layout 中添加）
   ```html
   <div class="affiliate-banner">
     <a href="YOUR_AFF_LINK">🎁 注册币安，领取 100 USDT 新手礼包</a>
   </div>
   ```

3. **导航栏固定链接**
   ```html
   <nav>
     <a href="/">Home</a>
     <a href="YOUR_AFF_LINK" style="color: #f7931a;">🔥 币安注册</a>
   </nav>
   ```

---

## 🔧 故障排查

### 问题 1：Vercel 构建失败

**错误信息：** `Error: Missing required file "astro.config.mjs"`

**解决：** 创建 `astro.config.mjs` 文件：
```javascript
import { defineConfig } from 'astro/config';

export default defineConfig({
  output: 'static'
});
```

### 问题 2：Python 脚本未执行

检查 `package.json` 中的 build 命令：
```json
"build": "pip install -r requirements.txt && python build_content.py && astro build"
```

确保顺序正确：先装依赖 → 跑脚本 → 编译 Astro

### 问题 3：内容未更新

- 检查 cron-job 是否正常执行
- 查看 Vercel 部署日志
- 确认 Deploy Hook URL 正确

---

## 📈 下一步优化建议

1. **接入真实 API**
   - 修改 `build_content.py` 使用 ccxt 获取实时数据
   - 集成 yfinance 采集美股行情

2. **AI 内容增强**
   - 调用 DeepSeek API 生成专业分析
   - 添加市场情绪指标

3. **SEO 扩展**
   - 添加 sitemap.xml 生成
   - 实现 robots.txt 配置

4. **性能监控**
   - 集成 Google Search Console
   - 追踪关键词排名

---

## 🎯 核心优势总结

> ✨ **这个模板的核心价值：**
> 
> 1. **自动化内容生产** - Python 脚本 + Astro SSG
> 2. **SEO 原生友好** - JSON-LD + 语义化 HTML
> 3. **零成本部署** - Vercel 免费额度
> 4. **被动收入系统** - 定时任务自动更新
> 5. **可扩展架构** - 轻松添加新股市/新语言

---

**最后更新：** 2026-03-31  
**状态：** ✅ 可直接部署
