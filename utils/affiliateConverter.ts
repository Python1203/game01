/**
 * 淘宝联盟和京东联盟链接转换工具
 * 支持二合一链接、淘口令生成、移动端跳转逻辑
 */

export type PlatformType = 'pc' | 'mobile' | 'wechat'

interface AffiliateLinkConfig {
  pid: string // 推广位 ID
  unionId?: string // 联盟 ID
}

// 配置信息（从环境变量读取）
const TAOBAO_CONFIG: AffiliateLinkConfig = {
  pid: process.env.NEXT_PUBLIC_TAOBAO_PID || '',
  unionId: process.env.NEXT_PUBLIC_TAOBAO_UNION_ID,
}

const JD_CONFIG: AffiliateLinkConfig = {
  pid: process.env.NEXT_PUBLIC_JD_PID || '',
  unionId: process.env.NEXT_PUBLIC_JD_UNION_ID,
}

/**
 * 检测设备类型
 */
export function detectPlatform(): PlatformType {
  if (typeof window === 'undefined') return 'pc'

  const ua = navigator.userAgent.toLowerCase()
  const isWeChat = /micromessenger/i.test(ua)
  const isMobile = /mobile|android|iphone|ipad|phone/i.test(ua)

  if (isWeChat) return 'wechat'
  if (isMobile) return 'mobile'
  return 'pc'
}

/**
 * 检测是否为 iOS 设备
 */
export function isIOS(): boolean {
  if (typeof window === 'undefined') return false
  return /iphone|ipad|ipod/i.test(navigator.userAgent)
}

/**
 * 淘宝链接转换
 * @param originalUrl 原始商品链接
 * @param platform 目标平台
 * @returns 转换后的联盟链接或淘口令
 */
export function convertTaobaoLink(originalUrl: string, platform: PlatformType = 'pc'): string {
  if (!originalUrl) return ''

  // 提取商品 ID
  const itemId = extractTaobaoItemId(originalUrl)
  if (!itemId) return originalUrl

  // 根据平台返回不同格式
  if (platform === 'wechat') {
    // 微信环境：返回短链接或淘口令
    return generateTaoKouLing(itemId, originalUrl)
  } else if (platform === 'mobile') {
    // 移动端：返回二合一链接（短链 + 淘口令）
    return generateMobileLink(itemId, originalUrl, 'taobao')
  } else {
    // PC 端：返回标准联盟链接
    return generateTaobaoAffiliateLink(itemId, originalUrl)
  }
}

/**
 * 京东链接转换
 * @param originalUrl 原始商品链接
 * @param platform 目标平台
 * @returns 转换后的联盟链接
 */
export function convertJdLink(originalUrl: string, platform: PlatformType = 'pc'): string {
  if (!originalUrl) return ''

  // 提取商品 SKU
  const sku = extractJdSku(originalUrl)
  if (!sku) return originalUrl

  if (platform === 'wechat') {
    // 微信环境：返回 CPC 链接
    return generateJdCpcLink(sku, originalUrl)
  } else if (platform === 'mobile') {
    // 移动端：返回短链
    return generateJdMobileLink(sku, originalUrl)
  } else {
    // PC 端：返回标准联盟链接
    return generateJdAffiliateLink(sku, originalUrl)
  }
}

/**
 * 提取淘宝商品 ID
 */
function extractTaobaoItemId(url: string): string | null {
  const patterns = [/id=(\d+)/, /\/item\.htm\?id=(\d+)/, /a\.html\/(\d+)/]

  for (const pattern of patterns) {
    const match = url.match(pattern)
    if (match) return match[1]
  }

  return null
}

/**
 * 提取京东 SKU
 */
function extractJdSku(url: string): string | null {
  const patterns = [/\/(\d+)\.html/, /sku=(\d+)/, /product=(\d+)/]

  for (const pattern of patterns) {
    const match = url.match(pattern)
    if (match) return match[1]
  }

  return null
}

/**
 * 生成淘宝联盟链接（PC 端）
 */
function generateTaobaoAffiliateLink(itemId: string, originalUrl: string): string {
  const pid = TAOBAO_CONFIG.pid
  if (!pid) return originalUrl

  // 阿里妈妈通用链接格式
  return `https://s.click.taobao.com/t?e=${encodeURIComponent(JSON.stringify({ item_id: itemId, pvid: pid, app_pvid: pid }))}&p=${pid}`
}

/**
 * 生成淘口令（微信/移动端）
 */
function generateTaoKouLing(itemId: string, originalUrl: string): string {
  // 简化版淘口令生成（实际应调用阿里 API）
  const shortUrl = `https://m.tb.cn/${generateShortCode(itemId)}`
  return `¥${shortUrl}¥ 打开淘宝查看`
}

/**
 * 生成移动端二合一链接
 */
function generateMobileLink(
  itemId: string,
  originalUrl: string,
  platform: 'taobao' | 'jd'
): string {
  if (platform === 'taobao') {
    // 淘宝移动端短链
    return `https://m.intl.taobao.com/item/detail.html?id=${itemId}`
  } else {
    // 京东移动端短链
    return `https://m.jd.com/product/${itemId}.html`
  }
}

/**
 * 生成京东联盟链接（PC 端）
 */
function generateJdAffiliateLink(sku: string, originalUrl: string): string {
  const pid = JD_CONFIG.pid
  if (!pid) return originalUrl

  return `https://union-click.jd.com/jdc?e=${encodeURIComponent(JSON.stringify({ p: `${pid}_${sku}` }))}&to=${encodeURIComponent(originalUrl)}`
}

/**
 * 生成京东 CPC 链接（微信）
 */
function generateJdCpcLink(sku: string, originalUrl: string): string {
  return `https://cps.360buy.com/link?sku=${sku}&unionId=${JD_CONFIG.unionId}`
}

/**
 * 生成京东移动端链接
 */
function generateJdMobileLink(sku: string, originalUrl: string): string {
  return `https://item.m.jd.com/product/${sku}.html`
}

/**
 * 生成短代码（用于淘口令）
 */
function generateShortCode(itemId: string): string {
  // 简化的短代码生成逻辑
  const chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
  let result = ''
  let hash = simpleHash(itemId)

  for (let i = 0; i < 8; i++) {
    result += chars[hash % chars.length]
    hash = Math.floor(hash / chars.length)
  }

  return result
}

/**
 * 简单的哈希函数
 */
function simpleHash(str: string): number {
  let hash = 0
  for (let i = 0; i < str.length; i++) {
    const char = str.charCodeAt(i)
    hash = (hash << 5) - hash + char
    hash = hash & hash
  }
  return Math.abs(hash)
}

/**
 * 深度链接唤醒 APP（移动端）
 */
export function openApp(platform: 'taobao' | 'jd', url: string): void {
  if (typeof window === 'undefined') return

  const scheme = platform === 'taobao' ? 'tbopen://' : 'openapp.jdmobile://'
  const fallbackUrl = platform === 'taobao' ? 'https://m.taobao.com' : 'https://m.jd.com'

  // 尝试唤醒 APP
  window.location.href = scheme

  // 如果唤醒失败，跳转到 H5
  setTimeout(() => {
    window.location.href = fallbackUrl
  }, 2000)
}

/**
 * 复制到剪贴板辅助函数
 */
export async function copyToClipboard(text: string): Promise<boolean> {
  try {
    await navigator.clipboard.writeText(text)
    return true
  } catch (err) {
    console.error('复制失败:', err)

    // 降级方案
    const textarea = document.createElement('textarea')
    textarea.value = text
    document.body.appendChild(textarea)
    textarea.select()
    document.execCommand('copy')
    document.body.removeChild(textarea)

    return true
  }
}
