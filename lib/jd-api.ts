/**
 * 京东联盟 API 调用工具类（HTTP 方式）
 * 
 * 官方文档：https://union.jd.com/open/api
 */

import crypto from 'crypto'

interface JDProduct {
  id: string
  title: string
  picUrl: string
  price: number
  commissionRate: number
  promoCode: string
  platform: 'jd'
  categoryId?: string
  shopTitle?: string
}

/**
 * 生成京东 API 签名
 */
function generateJDSign(params: Record<string, string>, secret: string): string {
  // 按参数名 ASCII 码排序
  const sortedKeys = Object.keys(params).sort()
  
  // 拼接字符串
  let signString = secret
  sortedKeys.forEach(key => {
    if (params[key] !== undefined && params[key] !== null) {
      signString += key + params[key]
    }
  })
  signString += secret
  
  // MD5 签名并转大写
  return crypto.createHash('md5').update(signString).digest('hex').toUpperCase()
}

/**
 * 调用京东联盟 API
 */
async function callJDAPI(method: string, params: Record<string, any>) {
  const accessToken = process.env.JD_ACCESS_TOKEN
  const appKey = process.env.JD_APP_KEY || '303298'
  const appSecret = process.env.JD_APP_SECRET || 'b159dbfda0ee41ec923ae05740c08b79'
  
  if (!accessToken) {
    throw new Error('京东 API Access Token 未配置')
  }

  // 基础参数
  const baseParams = {
    method: method,
    access_token: accessToken,
    app_key: appKey,
    timestamp: new Date().toISOString(),
    v: '1.0',
    format: 'json',
    ...params,
  }

  // 使用 appSecret 生成签名
  baseParams.sign = generateJDSign(baseParams, appSecret)

  try {
    const url = 'https://api.jd.com/routerjson'
    
    console.log('调用京东 API:', method)
    console.log('AppKey:', appKey)
    console.log('签名:', baseParams.sign)

    // 发送 POST 请求
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(baseParams),
      // 超时 10 秒
      signal: AbortSignal.timeout(10000),
    })

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    const data = await response.json()
    
    // 检查错误响应
    const errorKey = `${method.replace(/\./g, '_')}_response`
    if (data[errorKey] && data[errorKey].code) {
      throw new Error(`京东 API 错误：${data[errorKey].msg || data[errorKey].zh_desc}`)
    }

    return data
  } catch (error) {
    console.error('京东 API 调用失败:', error)
    throw error
  }
}

/**
 * 获取京东联盟商品详情
 * @param skuId - 商品 SKU ID
 * @returns 商品信息
 */
export async function getJDItemDetail(skuId: string): Promise<JDProduct | null> {
  try {
    const accessToken = process.env.JD_ACCESS_TOKEN
    
    // 构建请求参数
    const params = {
      method: 'jd.union.open.goods.query',
      access_token: accessToken,
      app_key: process.env.NEXT_PUBLIC_JD_APP_KEY,
      timestamp: new Date().toISOString(),
      v: '1.0',
      format: 'json',
    }

    // 请求体
    const requestBody = {
      skuIds: [skuId],
      queryParam: {
        fields: ['skuInfo', 'priceInfo', 'commissionInfo'],
      },
    }

    // 调用 API（实际项目中需要使用官方 SDK）
    const response = await fetch('https://api.jd.com/routerjson', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        ...params,
        param_data: JSON.stringify(requestBody),
      }),
    })

    const data = await response.json()

    if (data.jd_union_open_goods_query_response && data.jd_union_open_goods_query_response.result) {
      const goodsList = data.jd_union_open_goods_query_response.result.goodsList
      
      if (goodsList && goodsList.length > 0) {
        const item = goodsList[0]
        return {
          id: item.skuInfo.skuId,
          title: item.skuInfo.skuName,
          picUrl: item.skuInfo.imageInfo.imageList?.[0]?.url || '',
          price: parseFloat(item.priceInfo.price) || 0,
          commissionRate: parseFloat(item.commissionInfo.commission) || 0,
          promoCode: await generateJDLink(skuId),
          platform: 'jd' as const,
          categoryId: item.skuInfo.categoryInfo.category,
          shopTitle: item.shopInfo.shopName,
        }
      }
    }

    return null
  } catch (error) {
    console.error('京东联盟 API 调用失败:', error)
    throw error
  }
}

/**
 * 获取京东联盟商品列表
 * @param options - 查询参数
 * @returns 商品列表
 */
export async function getJDItemList(options: {
  keyword?: string
  categoryId?: number
  minPrice?: number
  maxPrice?: number
  limit?: number
}): Promise<JDProduct[]> {
  try {
    const { keyword, categoryId, minPrice, maxPrice, limit = 20 } = options

    // 调用官方 API: jd.union.open.goods.list.query
    const requestBody = {
      positionId: process.env.NEXT_PUBLIC_JD_POSITION_ID || '',
      key: keyword || '',
      categoryId: categoryId || 0,
      priceFrom: minPrice,
      priceTo: maxPrice,
      pageSize: Math.min(limit, 50),
      pageIndex: 1,
    }

    const result = await callJDAPI('jd.union.open.goods.list.query', {
      param_data: JSON.stringify(requestBody),
    })

    if (result && result.jd_union_open_goods_list_query_response) {
      const goodsList = result.jd_union_open_goods_list_query_response.result?.goodsList || []
      
      // 批量生成转链链接
      const products = await Promise.all(
        goodsList.map(async (item: any) => ({
          id: item.skuInfo?.skuId || '',
          title: item.skuInfo?.skuName || '',
          picUrl: item.skuInfo?.imageInfo?.imageList?.[0]?.url || '',
          price: parseFloat(item.priceInfo?.price || '0'),
          commissionRate: parseFloat(item.commissionInfo?.commission || '0'),
          promoCode: await generateJDLink(item.skuInfo?.skuId),
          platform: 'jd' as const,
          categoryId: item.skuInfo?.categoryInfo?.category,
          shopTitle: item.shopInfo?.shopName,
        }))
      )

      return products
    }

    return []
  } catch (error) {
    console.error('获取京东商品列表失败:', error)
    throw error
  }
}

/**
 * 生成京东推广链接
 * @param skuId - 商品 SKU ID
 * @returns 推广链接
 */
async function generateJDLink(skuId: string): Promise<string> {
  try {
    const accessToken = process.env.JD_ACCESS_TOKEN
    
    const requestBody = {
      materialId: skuId.toString(),
      positionId: process.env.NEXT_PUBLIC_JD_POSITION_ID,
      siteId: '',
      unionId: process.env.NEXT_PUBLIC_JD_PID,
    }

    const response = await fetch('https://api.jd.com/routerjson', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        method: 'jd.union.open.promotion.common.get',
        access_token: accessToken,
        app_key: process.env.NEXT_PUBLIC_JD_APP_KEY,
        timestamp: new Date().toISOString(),
        v: '1.0',
        format: 'json',
        param_data: JSON.stringify(requestBody),
      }),
    })

    const data = await response.json()

    if (data.jd_union_open_promotion_common_get_response && data.jd_union_open_promotion_common_get_response.result) {
      const clickURL = data.jd_union_open_promotion_common_get_response.result.clickURL
      return clickURL || `https://u.jd.com/${skuId}`
    }

    return `https://u.jd.com/${skuId}`
  } catch (error) {
    console.error('生成京东推广链接失败:', error)
    return `https://u.jd.com/${skuId}`
  }
}

/**
 * 测试 API 连接
 */
export async function testJDAPI(): Promise<boolean> {
  try {
    const accessToken = process.env.JD_ACCESS_TOKEN
    const appKey = process.env.JD_APP_KEY || '303298'
    const appSecret = process.env.JD_APP_SECRET || 'b159dbfda0ee41ec923ae05740c08b79'
    
    // 构建基础参数
    const baseParams = {
      method: 'jd.time.get',
      access_token: accessToken,
      app_key: appKey,
      timestamp: new Date().toISOString(),
      v: '1.0',
      format: 'json',
    }
    
    // 生成签名
    baseParams.sign = generateJDSign(baseParams, appSecret)
    
    console.log('测试京东 API 连接...')
    console.log('AppKey:', appKey)
    console.log('签名:', baseParams.sign)
    
    // 简单调用测试连通性
    const response = await fetch('https://api.jd.com/routerjson', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(baseParams),
    })

    const data = await response.json()
    
    if (data.jd_time_get_response) {
      console.log('✅ 京东联盟 API 连接成功！当前时间:', data.jd_time_get_response)
      return true
    }
    
    console.warn('⚠️ 京东 API 响应异常:', data)
    return false
  } catch (error) {
    console.error('❌ 京东联盟 API 连接失败:', (error as Error).message)
    return false
  }
}
