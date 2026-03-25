/**
 * 京东 API 深度调试脚本
 * 详细记录请求和响应的每个细节
 */

import crypto from 'crypto'
import { config } from 'dotenv'
import { resolve } from 'path'

config({ path: resolve(__dirname, '../.env.local') })

// 配置信息
const APP_KEY = process.env.JD_APP_KEY || ''
const APP_SECRET = process.env.JD_APP_SECRET || ''
const ACCESS_TOKEN = process.env.JD_ACCESS_TOKEN || ''

console.log('='.repeat(60))
console.log('🔍 京东 API 深度调试工具')
console.log('='.repeat(60))
console.log()
console.log('【配置信息】')
console.log('AppKey:', APP_KEY)
console.log('AppSecret:', APP_SECRET.substring(0, 8) + '***')
console.log('Access Token:', ACCESS_TOKEN.substring(0, 16) + '***')
console.log()

// 生成签名函数
function generateJDSign(params: Record<string, string>, secret: string): string {
  const sortedKeys = Object.keys(params).sort()
  
  let signString = secret
  sortedKeys.forEach(key => {
    if (params[key] !== undefined && params[key] !== null) {
      signString += key + params[key]
    }
  })
  signString += secret
  
  return crypto.createHash('md5').update(signString).digest('hex').toUpperCase()
}

// 测试时间 API（最简单）
async function testTimeAPI() {
  console.log('【测试 1】调用基础时间 API (jd.time.get)...')
  console.log()
  
  const timestamp = new Date().toISOString()
  const baseParams = {
    method: 'jd.time.get',
    access_token: ACCESS_TOKEN,
    app_key: APP_KEY,
    timestamp: timestamp,
    v: '1.0',
    format: 'json',
  }
  
  // 生成签名
  const sign = generateJDSign(baseParams, APP_SECRET)
  baseParams.sign = sign
  
  console.log('【请求参数】')
  console.log(JSON.stringify(baseParams, null, 2))
  console.log()
  console.log('生成的签名:', sign)
  console.log()
  
  try {
    const response = await fetch('https://api.jd.com/routerjson', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(baseParams),
    })
    
    const data = await response.json()
    
    console.log('【HTTP 状态码】')
    console.log(response.status, response.statusText)
    console.log()
    
    console.log('【完整响应】')
    console.log(JSON.stringify(data, null, 2))
    console.log()
    
    if (data.error_response) {
      console.log('❌ 错误信息:')
      console.log('  代码:', data.error_response.code)
      console.log('  中文:', data.error_response.zh_desc)
      console.log('  英文:', data.error_response.en_desc)
      console.log('  请求 ID:', data.error_response.request_id)
    } else if (data.jd_time_get_response) {
      console.log('✅ 成功！当前服务器时间:', data.jd_time_get_response)
    }
    
  } catch (error) {
    console.error('❌ 请求失败:', error)
  }
}

// 测试商品列表 API
async function testGoodsListAPI() {
  console.log()
  console.log('【测试 2】调用商品列表 API (jd.union.open.goods.list.query)...')
  console.log()
  
  const timestamp = new Date().toISOString()
  const requestBody = {
    positionId: '',
    key: '',
    categoryId: 0,
    priceFrom: undefined,
    priceTo: undefined,
    pageSize: 10,
    pageIndex: 1,
  }
  
  const baseParams = {
    method: 'jd.union.open.goods.list.query',
    access_token: ACCESS_TOKEN,
    app_key: APP_KEY,
    timestamp: timestamp,
    v: '1.0',
    format: 'json',
    param_data: JSON.stringify(requestBody),
  }
  
  // 生成签名
  const sign = generateJDSign(baseParams, APP_SECRET)
  baseParams.sign = sign
  
  console.log('【请求体 param_data】')
  console.log(JSON.stringify(requestBody, null, 2))
  console.log()
  console.log('【完整参数】')
  console.log('method:', baseParams.method)
  console.log('access_token:', ACCESS_TOKEN.substring(0, 16) + '***')
  console.log('app_key:', APP_KEY)
  console.log('timestamp:', timestamp)
  console.log('sign:', sign)
  console.log()
  
  try {
    const response = await fetch('https://api.jd.com/routerjson', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(baseParams),
    })
    
    const data = await response.json()
    
    console.log('【HTTP 状态码】')
    console.log(response.status, response.statusText)
    console.log()
    
    console.log('【完整响应】')
    console.log(JSON.stringify(data, null, 2))
    console.log()
    
    if (data.error_response) {
      console.log('❌ 错误信息:')
      console.log('  代码:', data.error_response.code)
      console.log('  中文:', data.error_response.zh_desc)
      console.log('  英文:', data.error_response.en_desc)
      console.log('  请求 ID:', data.error_response.request_id)
    } else if (data.jd_union_open_goods_list_query_response) {
      const goodsList = data.jd_union_open_goods_list_query_response.result?.goodsList || []
      console.log(`✅ 成功！获取到 ${goodsList.length} 个商品`)
      
      if (goodsList.length > 0) {
        console.log()
        console.log('【前 3 个商品】')
        goodsList.slice(0, 3).forEach((item: any, index: number) => {
          console.log(`${index + 1}. ${item.skuInfo?.skuName} - ¥${item.priceInfo?.price}`)
        })
      }
    }
    
  } catch (error) {
    console.error('❌ 请求失败:', error)
  }
}

// 运行所有测试
async function runAllTests() {
  await testTimeAPI()
  await testGoodsListAPI()
  
  console.log()
  console.log('='.repeat(60))
  console.log('✅ 调试完成！')
  console.log('='.repeat(60))
}

runAllTests().catch(console.error)
