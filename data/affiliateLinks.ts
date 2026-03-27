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
  'fuji-gfx100-ii': {
    jd: '', // 可后续补充京东链接
    tb: 'https://s.click.taobao.com/t?e=m%3D2%26s%3DeaC%2Ba5sYb9Vw4vFB6t2Z2ueEDrYVVa64YUrQeSeIhnK53hKxp7mNFl906SyIHsHUcx6NMuQ%2BBwROS4pX4DGe7vc91BEt1OIeAp0l%2FtogXIvvSDU5KD8g6ckMvl%2BcriAg%2FgFD2Cb2HtzSmu0J2OYLCQSY28wYIhWGDTzfUZS4jc1rrakkZKnPqAtkyqhBb5%2B4HoaaUnJGJVPiT5R7M%2BfUrE0xJELmpcVjphfEY%2B7W6Vi%2F2Gggwtk4PMj9YP7JZC3H17mMd%2F9EYPNyOmv97bY0D4%2BDKwFLEd9Q5dUsQ8NYvbj%2B58h5pKGYu5UYXHAgtCa69KvR6od1T1EMlu5kMKse3g%3D%3D&union_lens=lensId%3APUB%401774575739%40212b05fb_0e45_19d2cf4e382_3552%40021hWt97BrWPHM2dpwQod4aG%40eyJmbG9vcklkIjo4MDkyNywiic3BtQiiI6Il9wb3J0YWxfdjJfcGFnZXNfcHJvbW9fc2hvcF9kZXRhaWxfaW5kZXhfaHRtIiiwiic3JjRmxvb3JJZCI6IjgwOTI3In0ie%3Bscm%3A1007.30148.329090.pub_search-item_883b1277-f6d8-4b41-b7f7-741b54a28cc5_;https%3A%2F%2Fimg.alicdn.com%2Fbao%2Fuploaded%2FO1CN012me7KO1gv1fGPrz6p_!!6000000004203-0-yinhe.jpg',
    mobilePreference: 'tb'
  },
  'huawei-mate-80-pro-max': {
    jd: '', // 可后续补充京东链接
    tb: 'https://s.click.taobao.com/t?e=m%3D2%26s%3D2jO2fgfoqr1w4vFB6t2Z2ueEDrYVVa64YUrQeSeIhnK53hKxp7mNFl906SyIHsHUiMmRO9wDtCdOS4pX4DGe7vc91BEt1OIeAp0l%2FtogXIvvSDU5KD8g6ckMvl%2BcriAg%2FgFD2Cb2HtzSmu0J2OYLCQSY28wYIhWGDTzfUZS4jc1rrakkZKnPqAtkyqhBb5%2B4HoaaUnJGJVNeHAcdRdh%2BYtY2nClrNUdaopiJ8pas%2Bvnzy0fGSbe3sNwisUomr7%2Fuo8UQ3jdRiVRkrrFd%2BItQX0%2FuprW1TdmBLeMqtJBmsqDZGL0GbiMMdy4zRWxjykkuakcnG67xjzl4FEJj62OWMg%3D%3D&union_lens=lensId%3APUB%401774575739%40212b05fb_0e45_19d2cf4e382_3551%40022I71SDx2QS8bzDRPuBWCMi%40eyJmbG9vcklkIjo4MDkyNywiic3BtQiiI6Il9wb3J0YWxfdjJfcGFnZXNfcHJvbW9fc2hvcF9kZXRhaWxfaW5kZXhfaHRtIiiwiic3JjRmxvb3JJZCI6IjgwOTI3In0ie%3Bscm%3A1007.30148.329090.pub_search-item_883b1277-f6d8-4b41-b7f7-741b54a28cc5_;https%3A%2F%2Fimg.alicdn.com%2Fi1%2F2213856588863%2FO1CN01JoUsQd2FLJScS6boX_!!2213856588863.jpg',
    mobilePreference: 'tb'
  },
  'iphone17-pro-max': {
    jd: '', // 可后续补充京东链接
    tb: 'https://s.click.taobao.com/t?e=m%3D2%26s%3DRdXZpmRA4ehw4vFB6t2Z2ueEDrYVVa64YUrQeSeIhnK53hKxp7mNFl906SyIHsHUeP1OzWF%2F2zxOS4pX4DGe7vc91BEt1OIeAp0l%2FtogXIvvSDU5KD8g6ckMvl%2BcriAg%2FgFD2Cb2HtzSmu0J2OYLCQSY28wYIhWGlWC%2BLUEi2rPuRqZVqZbGdAtkyqhBb5%2B4HoaaUnJGJVP%2FIkuGI6g2J%2FoPEhl8C8BkRFkUbuUNjUsEdmCX0p%2F1%2B1zPQhBfMNxTUMVab1vXPgc1eMMBy3yJBI%2BDKwFLEd9Q5dUsQ8NYvbj%2B58h5pKGYu6b9WxLveENMatJN3PTYhhzPZMUUR31Kpg%3D%3D&union_lens=lensId%3APUB%401774575123%40214697a2_1ab8_19d2ceb7bf2_b6df%40025hpE6R9NduDLet7blndIPC%40eyJmbG9vcklkIjo4MDY3NCwiic3BtQiiI6Il9wb3J0YWxfdjJfcGFnZXNfcHJvbW9fZ29vZHNfaW5kZXhfaHRtIiiwiic3JjRmxvb3JJZCI6IjgwNjc0In0ie%3BtkScm%3Asearch_fuzzy_selectionPlaza_site_4358_0_0_0_2_177457512348452195179%3Bscm%3A1007.30148.329090.pub_search-item_d4f66660-72bb-4c99-88bf-4ee47ef4c529_%3Bhttps%3A%2F%2Fimg.alicdn.com%2Fbao%2Fuploaded%2FO1CN01W0rnhS1jTxCGu5gXy_!!6000000004550-0-yinhe.jpg',
    mobilePreference: 'tb'
  },
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
  'macbook-air-m4': {
    jd: '', // 可后续补充京东链接
    tb: 'https://s.click.taobao.com/t?e=m%3D2%26s%3DkJrvAGGdXf9w4vFB6t2Z2ueEDrYVVa64YUrQeSeIhnK53hKxp7mNFl906SyIHsHU9OK3r0VQYcJOS4pX4DGe7vc91BEt1OIeAp0l%2FtogXIvvSDU5KD8g6ckMvl%2BcriAg%2FgFD2Cb2HtzSmu0J2OYLCQSY28wYIhWGlWC%2BLUEi2rPuRqZVqZbGdAtkyqhBb5%2B4HoaaUnJGJVP0Sb66CtFmv6GKamXLQN5NlDPyhjXZwreHDhAS32i42Mco1rcV2gLx1taTK4vPyPaqwocLtOyFR4%2BDKwFLEd9Q5dUsQ8NYvbj%2B58h5pKGYu4Bv8HDxWgDI94FOXsSgND4vfeUUl6%2F7pA%3D%3D&union_lens=lensId%3APUB%401774575123%40214697a2_1ab8_19d2ceb7bf2_b6de%40024ZioqfstafbEXnCXj4eIy1%40eyJmbG9vcklkIjo4MDY3NCwiic3BtQiiI6Il9wb3J0YWxfdjJfcGFnZXNfcHJvbW9fZ29vZHNfaW5kZXhfaHRtIiiwiic3JjRmxvb3JJZCI6IjgwNjc0In0ie%3BtkScm%3Asearch_fuzzy_selectionPlaza_site_4358_0_0_0_1_177457512348452195179%3Bscm%3A1007.30148.329090.pub_search-item_d4f66660-72bb-4c99-88bf-4ee47ef4c529_%3Bhttps%3A%2F%2Fimg.alicdn.com%2Fbao%2Fuploaded%2FO1CN01GBb7hu1HeCqhUUlys_!!6000000000782-0-yinhe.jpg',
    mobilePreference: 'tb'
  },
  
  // 家居电器
  'dyson-v15': {
    jd: generateJdLink('https://u.jd.com/dysonv15'),
    tb: generateTbLink('https://s.click.taobao.com/dysonv15'),
    mobilePreference: 'jd'
  },
  'samsung-qa85qn950fjxxz': {
    jd: '', // 可后续补充京东链接
    tb: 'https://s.click.taobao.com/t?e=m%3D2%26s%3DEsUpOmODk5lw4vFB6t2Z2ueEDrYVVa64YUrQeSeIhnK53hKxp7mNFl906SyIHsHUpFMcnztlbWBOS4pX4DGe7vc91BEt1OIeAp0l%2FtogXIvvSDU5KD8g6ckMvl%2BcriAg%2FgFD2Cb2HtzSmu0J2OYLCQSY28wYIhWGDTzfUZS4jc1rrakkZKnPqAtkyqhBb5%2B4HoaaUnJGJVM4KvGC3w%2B5PBrpr5Uk60G7vSN0VSNmkYnvg%2Fy9G8c5f6SnvR00%2F%2F3RtNq66TgU2AONwgmp5IDic0%2FuprW1TdmBLeMqtJBmsqDZGL0GbiMMdzbUPVI0z%2BVK2%2Foug9KGNEy9Gf2zmUiveQ%3D%3D&union_lens=lensId%3APUB%401774575739%40212b05fb_0e45_19d2cf4e382_354e%40023ikAtApH8JR7RQ7e22E5L9%40eyJmbG9vcklkIjo4MDkyNywiic3BtQiiI6Il9wb3J0YWxfdjJfcGFnZXNfcHJvbW9fc2hvcF9kZXRhaWxfaW5kZXhfaHRtIiiwiic3JjRmxvb3JJZCI6IjgwOTI3In0ie%3Bscm%3A1007.30148.329090.pub_search-item_883b1277-f6d8-4b41-b7f7-741b54a28cc5_%3Bhttps%3A%2F%2Fimg.alicdn.com%2Fbao%2Fuploaded%2Fi1%2F2217052187942%2FO1CN01jIhrZs28XUd2iPElj_!!2217052187942-0-scmitem361000.jpg',
    mobilePreference: 'tb'
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
