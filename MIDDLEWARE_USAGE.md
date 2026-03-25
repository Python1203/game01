# 联盟链接跳转中间件使用指南

## 📋 概述

本项目使用 Next.js Middleware + Edge Function 实现极速的联盟链接跳转，在请求到达页面之前完成重定向，避免页面闪烁。

## 🚀 核心优势

- ⚡ **零延迟** - Edge Function 在 CDN 边缘节点执行，毫秒级响应
- 📱 **智能识别** - 自动区分 PC/移动端，优化跳转策略
- 🔧 **易维护** - 配置文件集中管理所有联盟链接
- 🎯 **SEO 友好** - 不影响正文页面的搜索引擎索引

## 📁 文件结构

```
├── middleware.ts              # Next.js 中间件（Edge Function）
├── data/
│   └── affiliateLinks.ts     # 联盟链接映射配置
└── app/
    └── blog/
        └── [...slug]/
            └── page.tsx      # 博客文章页面
```

## 🔗 使用方式

### 1. 在 MDX 文章中使用

```mdx
import { AffiliateCard } from '@/components/MDXComponents'

## 推荐商品

<AffiliateCard
  platform="jd"
  originalLink="https://item.jd.com/123456.html"
  title="iPhone 15 Pro Max"
  image="/static/images/iphone15.jpg"
  price="8499"
  coupon="500"
  commission="254.97"
/>

<!-- 或使用短链接 -->
[立即购买](/go/iphone15-pro-max)
```

### 2. 组件内部自动转换

`AffiliateCard` 组件已集成跳转逻辑，点击按钮会自动触发：

```typescript
// 组件内部逻辑
const handleJump = () => {
  // 直接跳转到 /go/slug，由 middleware 处理最终重定向
  window.location.href = `/go/${productSlug}`
}
```

## ⚙️ 配置说明

### 添加新商品链接

编辑 `data/affiliateLinks.ts`：

```typescript
export const affiliateLinks: Record<string, AffiliateLink> = {
  'new-product': {
    jd: 'https://u.jd.com/your-jd-link',
    tb: 'https://s.click.taobao.com/your-tb-link',
    mobilePreference: 'tb' // 移动端优先淘宝
  }
}
```

### 设备识别逻辑

```typescript
// middleware.ts 中的识别规则
const isMobile = /Android|iPhone|iPad|iPod/i.test(userAgent)

// 移动端优先策略
const finalUrl = isMobile 
  ? link.mobilePreference || 'tb'  // 默认淘宝（可唤起 App）
  : 'jd'                           // PC 端京东
```

## 🌐 路由规则

### matcher 配置

```typescript
export const config = {
  matcher: '/go/:path*', // 仅拦截 /go/ 开头的路径
}
```

### 支持的格式

- ✅ `/go/iphone15-pro-max` - 单个商品
- ✅ `/go/mate60-pro` - 中划线分隔
- ✅ `/go/dyson-v15` - 品牌 + 型号
- ❌ `/blog/go/xxx` - 不在根目录，不会被拦截

## 📊 性能对比

| 方案 | 响应时间 | 用户体验 | SEO 影响 |
|------|---------|---------|---------|
| **Middleware** | ~10ms | ⭐⭐⭐⭐⭐ | 无影响 |
| 前端跳转 | ~200ms | ⭐⭐⭐ | 无影响 |
| API 中转 | ~100ms | ⭐⭐⭐⭐ | 无影响 |

## 🔍 调试技巧

### 1. 本地测试

```bash
# 启动开发服务器
yarn dev

# 测试跳转
curl -v http://localhost:3000/go/iphone15-pro-max
```

### 2. 查看 User-Agent

```bash
# 模拟移动端
curl -A "iPhone" http://localhost:3000/go/iphone15-pro-max

# 模拟桌面端
curl -A "Mozilla/5.0 (Windows NT 10.0)" http://localhost:3000/go/iphone15-pro-max
```

### 3. Middleware 日志

在 `middleware.ts` 中添加调试输出：

```typescript
console.log('Redirecting:', { slug, isMobile, finalUrl })
```

查看日志：

```bash
# 开发环境
tail -f .next/server/middleware.js.map
```

## 🛠️ 高级用法

### 1. 动态佣金追踪

```typescript
// middleware.ts
if (url.pathname.startsWith('/go/')) {
  const slug = url.pathname.replace('/go/', '')
  const link = affiliateLinks[slug]
  
  // 添加追踪参数
  const trackingParams = new URLSearchParams({
    source: 'blog',
    device: isMobile ? 'mobile' : 'desktop',
    timestamp: Date.now().toString()
  })
  
  const finalUrl = `${link}?${trackingParams.toString()}`
  return NextResponse.redirect(new URL(finalUrl))
}
```

### 2. A/B 测试分流

```typescript
// 根据用户 ID 或其他特征分流
const userId = request.cookies.get('user_id')?.value
const shouldRedirectToJd = userId && parseInt(userId) % 2 === 0

const finalUrl = shouldRedirectToJd ? link.jd : link.tb
```

### 3. 地域限制

```typescript
// 根据 IP 或地理位置分流
const country = request.geo?.country || 'US'
if (country === 'CN') {
  // 中国大陆用户
  return NextResponse.redirect(new URL(link.tb))
} else {
  // 海外用户
  return NextResponse.redirect(new URL(link.international))
}
```

## ⚠️ 注意事项

1. **环境变量** - 敏感链接可通过环境变量管理
   ```typescript
   jd: process.env.JD_IPHONE15_URL || 'default-url'
   ```

2. **缓存策略** - Middleware 会被 Edge 缓存，修改配置后需等待生效
   ```bash
   # 清除缓存（生产环境）
   vercel --prod
   ```

3. **错误处理** - 未匹配的商品应返回 404 或重定向到文章页
   ```typescript
   if (!finalUrl) {
     return NextResponse.next() // 继续访问原页面
   }
   ```

## 📈 数据监控

建议接入分析工具追踪跳转效果：

```typescript
// middleware.ts
if (finalUrl) {
  // 发送事件到分析平台
  waitUntil(
    fetch('https://analytics.example.com/api/event', {
      method: 'POST',
      body: JSON.stringify({ slug, isMobile, timestamp: Date.now() })
    })
  )
  return NextResponse.redirect(new URL(finalUrl))
}
```

## 🔗 参考资料

- [Next.js Middleware 官方文档](https://nextjs.org/docs/app/building-your-application/routing/middleware)
- [Edge Functions 最佳实践](https://vercel.com/docs/functions/edge-functions)
- [User-Agent 识别库](https://github.com/faisalman/ua-parser-js)
