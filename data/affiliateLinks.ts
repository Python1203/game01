// 联盟链接映射配置
// 用于 middleware.ts 快速重定向
import siteMetadata from './siteMetadata'

export interface AffiliateLink {
  jd: string // 京东高佣链接
  tb: string // 淘宝高佣链接
  mobilePreference?: 'jd' | 'tb' // 移动端优先选择，默认 'tb'
}

/**
 * 生成京东联盟链接（带 PID）
 * @param baseUrl - 原始商品链接
 * @returns 带联盟 ID 的京东链接
 */
function generateJdLink(baseUrl: string): string {
  const pid = siteMetadata.affiliate.jd_pid
  if (!pid || pid === 'xxxxx_xxxx_xxxx') return baseUrl
  
  try {
    const url = new URL(baseUrl)
    url.searchParams.set('unionId', pid)
    return url.toString()
  } catch {
    return baseUrl
  }
}

/**
 * 生成淘宝联盟链接（带推广位 ID）
 * @param baseUrl - 原始商品链接
 * @returns 带联盟 ID 的淘宝链接
 */
function generateTbLink(baseUrl: string): string {
  const pubId = siteMetadata.affiliate.tb_pub_id
  if (!pubId || pubId === 'mm_xxxx_xxxx_xxxx') return baseUrl
  
  try {
    const url = new URL(baseUrl)
    url.searchParams.set('pvid', pubId)
    return url.toString()
  } catch {
    return baseUrl
  }
}

export const affiliateLinks: Record<string, AffiliateLink> = {
  // 数码产品
  'iphone15-pro-max': {
    jd: generateJdLink('https://u.jd.com/xxxxx'),
    tb: generateTbLink('https://s.click.taobao.com/xxxxx'),
    mobilePreference: 'tb' // 移动端优先淘宝（可唤起 App）
  },
  'mate60-pro': {
    jd: generateJdLink('https://u.jd.com/mate60jd'),
    tb: generateTbLink('https://s.click.taobao.com/mate60tb'),
    mobilePreference: 'tb'
  },
  'macbook-pro': {
    jd: generateJdLink('https://u.jd.com/macbookjd'),
    tb: generateTbLink('https://s.click.taobao.com/macbooktb'),
    mobilePreference: 'jd'
  },
  
  // 家居电器
  'dyson-v15': {
    jd: generateJdLink('https://u.jd.com/dysonv15'),
    tb: generateTbLink('https://s.click.taobao.com/dysonv15'),
    mobilePreference: 'jd'
  },
  'xiaomi-robot': {
    jd: generateJdLink('https://u.jd.com/xiaomirobot'),
    tb: generateTbLink('https://s.click.taobao.com/xiaomirobot'),
    mobilePreference: 'tb'
  },
  
  // 美妆护肤
  'estee-lauder': {
    jd: generateJdLink('https://u.jd.com/esteelauder'),
    tb: generateTbLink('https://s.click.taobao.com/esteelauder'),
    mobilePreference: 'tb'
  },
  'sk-ii': {
    jd: generateJdLink('https://u.jd.com/skii'),
    tb: generateTbLink('https://s.click.taobao.com/skii'),
    mobilePreference: 'tb'
  },
  
  // 食品生鲜
  'nuts-gift': {
    jd: generateJdLink('https://u.jd.com/nutsgift'),
    tb: generateTbLink('https://s.click.taobao.com/nutsgift'),
    mobilePreference: 'tb'
  },
  'hairy-crab': {
    jd: generateJdLink('https://u.jd.com/hairycrab'),
    tb: generateTbLink('https://s.click.taobao.com/hairycrab'),
    mobilePreference: 'jd'
  },
  
  // 特别推荐
  'special-promotion': {
    jd: '', // 可后续补充京东链接
    tb: 'https://s.click.taobao.com/t?union_lens=lensId%3APUB%401774436689%40212b0451_1a75_19d24ab2743_9b52%4001%40eyJmbG9vcklkIjozODg1Miiwiic3BtQiiI6Il9wb3J0YWxfdjJfcGFnZXNfYWN0aXZpdHlfb2ZmaWNpYWxfaW5kZXhfaHRtIn0ie%3BeventPageId%3A20150318020016228&e=m%3D2%26s%3DFB7qDOPd4WZw4vFB6t2Z2iperVdZeJviasFb3jPCdt85Rogii3YtH1906SyIHsHU7rQJXv4XN%2FROS4pX4DGe7vc91BEt1OIeoQnnpZeZ4qNJk%2BidQOHq%2FKmrhouJzCjDvasHdZt7yHJOVPhIvNgOIJ8Jce6nkr6KO9%2BWHj%2BGqPz0IaOxq0VuD%2BTEWJdP8jmR0cbSYRNMnDhMMH5DQkFc6iPlaOGWzl4k0kVb9BOisrmS7N1y3KZkblulnNqQMzcogtwjeA8fAfXBZqoga52UCaUia9MFsgZqPQvdpAMnfQFv403QK5YGaWu2lY1hTvYR8WASGyy2ZiybOnQ5M%2FycqOspV9sCcjGEK21v76OJgw9VXRkZOvK%2FVyaa21c5k%2BY9h8tcf%2B0AdS%2BxTd%2Fs2g8%2BnN0H1fQCHAAdav38qBUePC5luSKe6iiXHR81olgUGD3NLTb6KA58HtZassZbrSK798YMXU3NNCg%2F',
    mobilePreference: 'tb'
  }
}

/**
 * 根据设备类型获取最终跳转链接
 * @param slug - 商品标识
 * @param isMobile - 是否为移动设备
 * @returns 最终跳转链接
 */
export function getFinalUrl(slug: string, isMobile: boolean): string | null {
  const link = affiliateLinks[slug]
  if (!link) return null
  
  // 使用配置文件中的默认偏好
  const defaultPreference = siteMetadata.affiliate.mobile_preference || 'tb'
  const platform = isMobile ? (link.mobilePreference || defaultPreference) : 'jd'
  return link[platform]
}
