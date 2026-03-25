# 淘宝联盟 & 京东联盟导购组件使用指南

## 核心功能

✅ **多平台自动适配** - PC 端直接跳转，移动端复制口令 + 唤起 APP  
✅ **淘口令支持** - 微信环境自动生成淘口令  
✅ **二合一链接** - 移动端短链 + 口令组合  
✅ **佣金追踪** - 自动添加推广位 PID  

---

## 在 MDX 文章中使用

### 基础用法

```mdx
import { AffiliateCard } from '@/components/MDXComponents'

<AffiliateCard
  platform="taobao"
  originalLink="https://item.taobao.com/item.htm?id=123456789"
  title="【李佳琦推荐】进口零食大礼包"
  image="/static/images/product-1.jpg"
  price="99.9"
  coupon="20"
  commission="15.8"
/>
```

### 京东商品示例

```mdx
<AffiliateCard
  platform="jd"
  originalLink="https://item.jd.com/987654321.html"
  title="京东自营 苹果 iPhone 15 Pro Max"
  image="/static/images/iphone15.jpg"
  price="8999"
  coupon="500"
  commission="269.97"
/>
```

---

## 配置环境变量

在项目根目录创建 `.env.local` 文件：

```bash
# 淘宝联盟配置
NEXT_PUBLIC_TAOBAO_PID=mm_123456789_12345678_1234567890
NEXT_PUBLIC_TAOBAO_UNION_ID=123456

# 京东联盟配置
NEXT_PUBLIC_JD_PID=1234567890_1234567890
NEXT_PUBLIC_JD_UNION_ID=123456
```

---

## 组件 Props 说明

| Prop | 类型 | 必填 | 说明 |
|------|------|------|------|
| `platform` | `'taobao' \| 'jd' \| 'pinduoduo'` | ✅ | 电商平台 |
| `originalLink` | `string` | ✅ | 原始商品链接（非联盟链接） |
| `title` | `string` | ✅ | 商品标题 |
| `image` | `string` | ❌ | 商品图片 URL |
| `price` | `string` | ❌ | 商品价格 |
| `coupon` | `string` | ❌ | 优惠券金额 |
| `commission` | `string` | ❌ | 预估佣金 |

---

## 变现逻辑

### 1. PC 端用户
- 点击「立即购买」→ 打开带 PID 的联盟链接 → 自动追踪佣金

### 2. 移动端用户
- 点击「一键复制」→ 复制淘口令到剪贴板
- 点击「立即打开」→ 唤醒淘宝/京东 APP → 自动弹出商品

### 3. 微信环境
- 自动生成短淘口令，避免链接被屏蔽
- 提示用户复制后打开 APP

---

## 高级用法：批量展示

```mdx
<div className="grid grid-cols-1 md:grid-cols-2 gap-4">
  <AffiliateCard
    platform="taobao"
    originalLink="https://..."
    title="商品 A"
    price="59.9"
  />
  <AffiliateCard
    platform="jd"
    originalLink="https://..."
    title="商品 B"
    price="129"
  />
</div>
```

---

## 注意事项

⚠️ **不要直接在文章里贴原始链接**  
- 所有联盟链接都应该通过组件处理
- 避免用户手动修改 PID 跳单
- 提高转化率（视觉引导更强）

⚠️ **淘口令有效期**  
- 建议每 30 天更新一次淘口令
- 可接入阿里妈妈 API 实现动态生成

⚠️ **移动端体验优化**  
- 组件已自动检测设备类型
- 无需手动区分 PC/移动端文案

---

## 效果预览

### PC 端
```
┌─────────────────────────────────────┐
│ 📱 [商品图片]  【李佳琦推荐】...     │
│               ¥99.9  券¥20          │
│               [立即购买]            │
└─────────────────────────────────────┘
```

### 移动端
```
┌─────────────────────────────────────┐
│ 📱 [商品图片]  【李佳琦推荐】...     │
│               ¥99.9  券¥20          │
│               [一键复制][立即打开]  │
│ 💡 点击后打开淘宝 APP 即可查看详情   │
└─────────────────────────────────────┘
```

---

## 技术架构

```
MDX 文章
    ↓
<AffiliateCard /> (MDX Component)
    ↓
detectPlatform() → 判断设备类型
    ↓
convertTaobaoLink() / convertJdLink() → 转换联盟链接
    ↓
渲染不同 UI（PC 直链 / 移动端复制 + 唤起）
```

---

## 扩展建议

1. **接入官方 API** - 对接阿里妈妈和京东联盟 API，实现实时查询佣金、生成短链
2. **数据统计** - 添加点击统计，分析转化率
3. **选品库** - 建立内部选品数据库，统一管理商品信息
4. **自动化** - 定时任务自动更新失效链接

---

## 参考资料

- [淘宝联盟开放平台](https://pub.alimama.com/)
- [京东联盟开放平台](https://union.jd.com/)
- [淘口令生成原理](https://blog.csdn.net/article/details/xxx)
