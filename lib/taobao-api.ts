/**
 * 淘宝联盟 API 调用工具类（HTTP 方式）
 * 
 * 官方文档：https://open.taobao.com/doc.htm?docId=23466&docType=1
 */

import crypto from 'crypto'

/**
 * 生成淘宝 API 签名
 * 
 * 签名规则（根据淘宝官方文档）：
 * 1. 将所有参数按参数名 ASCII 码排序
 * 2. 拼接成 keyvalue 形式（注意：没有=和&）
 * 3. 在首尾分别加上 app_secret
 * 4. MD5 加密后转大写
 * 
 * 示例：
 * params: {app_key: "123", method: "test"}
 * secret: "abc"
 * signString = "abc" + "app_key123" + "methodtest" + "abc"
 */
function generateSign(params: Record<string, string>, appSecret: string): string {
  // 按参数名 ASCII 码排序
  const sortedKeys = Object.keys(params).sort()
  
  // 打印调试信息
  console.log('【签名参数】')
  console.log('排序后的参数:', sortedKeys)
  
  // 拼接字符串 - 关键：key+value，不是 key=value
  let signString = appSecret
  sortedKeys.forEach(key => {
    if (params[key] !== undefined && params[key] !== null && params[key] !== '') {
      signString += key + String(params[key])
    }
  })
  signString += appSecret
  
  console.log('签名字符串:', signString)
  
  // MD5 签名并转大写
  const sign = crypto.createHash('md5').update(signString, 'utf8').digest('hex').toUpperCase()
  console.log('生成的签名:', sign)
  
  return sign
}

/**
 * 调用淘宝联盟 API
 */
async function callTaoBaoAPI(method: string, params: Record<string, any>) {
  const appKey = process.env.TAOBAO_APP_KEY
  const appSecret = process.env.TAOBAO_APP_SECRET
  
  if (!appKey || !appSecret) {
    throw new Error('淘宝 API 密钥未配置')
  }

  // 格式化时间戳为淘宝要求的格式：yyyy-MM-dd HH:mm:ss
  const now = new Date()
  const year = now.getFullYear()
  const month = String(now.getMonth() + 1).padStart(2, '0')
  const day = String(now.getDate()).padStart(2, '0')
  const hours = String(now.getHours()).padStart(2, '0')
  const minutes = String(now.getMinutes()).padStart(2, '0')
  const seconds = String(now.getSeconds()).padStart(2, '0')
  const timestamp = `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`

  // 基础参数
  const baseParams = {
    app_key: appKey,
    method: method,
    timestamp,
    v: '2.0',
    format: 'json',
    sign_method: 'md5', // 添加签名方法参数
    ...params,
  }
  
  // 打印原始参数用于调试
  console.log('\n【原始参数】')
  console.log('app_key:', appKey)
  console.log('app_secret:', appSecret.substring(0, 8) + '***')
  console.log('timestamp:', timestamp)
  console.log('method:', method)

  // 生成签名
  const sign = generateSign(baseParams, appSecret)
  baseParams.sign = sign

  try {
    // 构建 URL
    const url = new URL('https://eco.taobao.com/router/rest')
    Object.entries(baseParams).forEach(([key, value]) => {
      url.searchParams.append(key, String(value))
    })

    console.log('调用淘宝 API:', method, url.toString())

    // 发送请求
    const response = await fetch(url.toString(), {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
      // 超时 10 秒
      signal: AbortSignal.timeout(10000),
    })

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    const data = await response.json()
    
    // 检查错误响应
    if (data.error_response) {
      throw new Error(`淘宝 API 错误：${data.error_response.msg || data.error_response.sub_msg}`)
    }

    return data
  } catch (error) {
    console.error('淘宝 API 调用失败:', error)
    throw error
  }
}

/**
 * 获取淘宝客商品详情
 * @param {string} itemId - 商品 ID
 * @returns {Promise<Object>} 商品信息
 */
export async function getTaoBaoItemDetail(itemId: string) {
  try {
    const result = await client.execute('taobao.tbk.item.info.get', {
      num_iid: itemId,
      platform: 1 // 1:PC, 2:无线
    })

    if (result && result.tbk_item_info_get_response) {
      const item = result.tbk_item_info_get_response.result.data[0]
      return {
        id: item.item_id,
        title: item.title,
        picUrl: item.pict_url,
        price: parseFloat(item.zk_final_price || item.reserve_price),
        commissionRate: parseFloat(item.commission_rate || '0'),
        promoCode: await generateTaoBaoLink(itemId), // 生成淘口令或转链
        platform: 'taobao' as const,
        categoryId: item.category_id,
        shopTitle: item.shop_title,
      }
    }

    throw new Error('未找到商品信息')
  } catch (error) {
    console.error('淘宝联盟 API 调用失败:', error)
    throw error
  }
}

/**
 * 获取淘宝客商品列表
 * @param {Object} options - 查询参数
 * @returns {Promise<Array>} 商品列表
 */
export async function getTaoBaoItemList(options: {
  q?: string // 搜索关键词
  cat?: string // 分类 ID
  startPrice?: number
  endPrice?: number
  limit?: number
}) {
  try {
    const { q, cat, startPrice, endPrice, limit = 20 } = options

    // 调用官方 API: taobao.tbk.dg.material.optional
    const queryParams: Record<string, string> = {
      q: q || '',
      cat: cat || '',
      start_price: startPrice?.toString() || '',
      end_price: endPrice?.toString() || '',
      page_size: Math.min(limit, 40).toString(), // 最多 40 条
      page_no: '1',
      platform: '1', // 1:PC, 2:无线，全部：空
    }
    
    // 过滤掉空参数（不参与签名）
    Object.keys(queryParams).forEach(key => {
      if (queryParams[key] === '') {
        delete queryParams[key]
      }
    })
    
    console.log('查询参数:', queryParams)
    
    const result = await callTaoBaoAPI('taobao.tbk.dg.material.optional', queryParams)

    if (result && result.result_list) {
      const items = result.result_list.map_data || []
      
      // 批量生成转链链接
      const products = await Promise.all(
        items.map(async (item: any) => ({
          id: item.item_id,
          title: item.title,
          picUrl: item.pict_url,
          price: parseFloat(item.zk_final_price || item.reserve_price || '0'),
          commissionRate: parseFloat(item.commission_rate || '0'),
          promoCode: await generateTaoBaoLink(item.item_id, item.click_url),
          platform: 'taobao' as const,
          categoryId: item.category_id,
          shopTitle: item.shop_title,
        }))
      )

      return products
    }

    return []
  } catch (error) {
    console.error('获取淘宝商品列表失败:', error)
    throw error
  }
}

/**
 * 生成淘口令或转链链接
 * @param itemId - 商品 ID
 * @param originalUrl - 原始链接（可选）
 * @returns {Promise<string>} 淘口令或链接
 */
async function generateTaoBaoLink(itemId: string, originalUrl?: string): Promise<string> {
  try {
    // 如果有原始链接，直接返回
    if (originalUrl) {
      return originalUrl
    }

    // 调用短链生成 API: taobao.tbk.sc.material.optional
    const adzoneId = process.env.NEXT_PUBLIC_TAOBAO_ADZONE_ID || '123456789' // 默认值
    
    const result = await callTaoBaoAPI('taobao.tbk.sc.material.optional', {
      material_id: itemId,
      adzone_id: adzoneId,
    })

    if (result && result.result_list) {
      const clickUrl = result.result_list.map_data[0]?.click_url
      
      if (clickUrl) {
        // 可以尝试生成淘口令（需要额外调用）
        try {
          const tklResult = await callTaoBaoAPI('taobao.tbk.password.create', {
            text: `【${itemId}】${clickUrl}`,
            ext: itemId,
          })

          if (tklResult && tklResult.data) {
            return tklResult.data.content // 返回淘口令
          }
        } catch (tklError) {
          console.warn('生成淘口令失败，使用普通链接:', tklError)
        }

        return clickUrl // 返回转链后的链接
      }
    }

    return `CZ0001 ${itemId}` // 默认格式
  } catch (error) {
    console.error('生成淘口令失败:', error)
    return `CZ0001 ${itemId}`
  }
}

/**
 * 测试 API 连接
 */
export async function testTaoBaoAPI(): Promise<boolean> {
  try {
    // 简单调用测试连通性：taobao.time.get
    await callTaoBaoAPI('taobao.time.get', {})
    console.log('✅ 淘宝联盟 API 连接成功')
    return true
  } catch (error) {
    console.error('❌ 淘宝联盟 API 连接失败:', (error as Error).message)
    return false
  }
}
