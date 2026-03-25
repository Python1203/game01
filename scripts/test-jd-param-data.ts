/**
 * 测试京东 API 签名中 param_data 的处理
 */

import crypto from 'crypto'
import { config } from 'dotenv'
import { resolve } from 'path'

config({ path: resolve(__dirname, '../.env.local') })

const APP_KEY = process.env.JD_APP_KEY || ''
const APP_SECRET = process.env.JD_APP_SECRET || ''
const ACCESS_TOKEN = process.env.JD_ACCESS_TOKEN || ''

console.log('='.repeat(60))
console.log('🔍 测试 param_data 在签名中的处理')
console.log('='.repeat(60))
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

async function testWithParamData() {
  console.log('【测试 1】param_data 参与签名')
  console.log()
  
  const timestamp = new Date().toISOString()
  const requestBody = {
    positionId: '',
    key: '',
    categoryId: 0,
    pageSize: 10,
    pageIndex: 1,
  }
  
  // param_data 参与签名
  const baseParamsWithParamData = {
    method: 'jd.union.open.goods.list.query',
    access_token: ACCESS_TOKEN,
    app_key: APP_KEY,
    timestamp: timestamp,
    v: '1.0',
    format: 'json',
    param_data: JSON.stringify(requestBody),
  }
  
  const signWithParamData = generateJDSign(baseParamsWithParamData, APP_SECRET)
  baseParamsWithParamData.sign = signWithParamData
  
  console.log('签名:', signWithParamData)
  console.log()
  
  try {
    const response = await fetch('https://api.jd.com/routerjson', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(baseParamsWithParamData),
    })
    
    const data = await response.json()
    
    if (data.error_response) {
      console.log('❌ 错误:', data.error_response.zh_desc)
    } else {
      const goodsList = data.jd_union_open_goods_list_query_response?.result?.goodsList || []
      console.log(`✅ 成功！获取到 ${goodsList.length} 个商品`)
    }
  } catch (error) {
    console.error('请求失败:', error)
  }
}

async function testWithoutParamDataInSign() {
  console.log()
  console.log('【测试 2】param_data 不参与签名（仅用于传递）')
  console.log()
  
  const timestamp = new Date().toISOString()
  const requestBody = {
    positionId: '',
    key: '',
    categoryId: 0,
    pageSize: 10,
    pageIndex: 1,
  }
  
  // 签名时不包含 param_data
  const baseParamsForSign = {
    method: 'jd.union.open.goods.list.query',
    access_token: ACCESS_TOKEN,
    app_key: APP_KEY,
    timestamp: timestamp,
    v: '1.0',
    format: 'json',
  }
  
  const sign = generateJDSign(baseParamsForSign, APP_SECRET)
  
  // 实际请求时添加 param_data
  const baseParamsWithParamData = {
    ...baseParamsForSign,
    sign: sign,
    param_data: JSON.stringify(requestBody),
  }
  
  console.log('签名:', sign)
  console.log()
  
  try {
    const response = await fetch('https://api.jd.com/routerjson', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(baseParamsWithParamData),
    })
    
    const data = await response.json()
    
    if (data.error_response) {
      console.log('❌ 错误:', data.error_response.zh_desc)
    } else {
      const goodsList = data.jd_union_open_goods_list_query_response?.result?.goodsList || []
      console.log(`✅ 成功！获取到 ${goodsList.length} 个商品`)
    }
  } catch (error) {
    console.error('请求失败:', error)
  }
}

async function testSimpleTimeAPI() {
  console.log()
  console.log('【测试 3】简单时间 API (无 param_data)')
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
  
  const sign = generateJDSign(baseParams, APP_SECRET)
  baseParams.sign = sign
  
  console.log('签名:', sign)
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
    
    console.log('完整响应:')
    console.log(JSON.stringify(data, null, 2))
    
    if (data.error_response) {
      console.log()
      console.log('❌ 错误信息:')
      console.log('  代码:', data.error_response.code)
      console.log('  中文:', data.error_response.zh_desc)
      console.log('  英文:', data.error_response.en_desc)
      console.log('  请求 ID:', data.error_response.request_id)
    } else if (data.jd_time_get_response) {
      console.log('✅ 成功！当前时间:', data.jd_time_get_response)
    }
  } catch (error) {
    console.error('请求失败:', error)
  }
}

async function runAllTests() {
  await testWithParamData()
  await testWithoutParamDataInSign()
  await testSimpleTimeAPI()
  
  console.log()
  console.log('='.repeat(60))
  console.log('✅ 调试完成！')
  console.log('='.repeat(60))
}

runAllTests().catch(console.error)
