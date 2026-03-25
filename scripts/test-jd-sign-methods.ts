/**
 * 测试不同的京东签名算法
 */

import crypto from 'crypto'

// 配置信息
const APP_KEY = 'bfaa3ef7bc6163e5582afb852e2f295c'
const APP_SECRET = 'b159dbfda0ee41ec923ae05740c08b79'
const ACCESS_TOKEN = 'ece3b6ab1c8b87a7a1eebfaa927f5d53d91d9f2130b8ec348a940752e18788e2f9b67f5e5b7b896d'

const timestamp = new Date().toISOString()

const baseParams = {
  method: 'jd.time.get',
  access_token: ACCESS_TOKEN,
  app_key: APP_KEY,
  timestamp: timestamp,
  v: '1.0',
  format: 'json',
}

console.log('='.repeat(60))
console.log('🔍 测试不同的京东签名算法')
console.log('='.repeat(60))
console.log()
console.log('基础参数:')
console.log(JSON.stringify(baseParams, null, 2))
console.log()

// 方法 1: 当前实现（secret + key+value + secret）
function generateSignV1(params: Record<string, string>, secret: string): string {
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

// 方法 2: 不包含 secret（所有参数 key+value 后接 secret）
function generateSignV2(params: Record<string, string>, secret: string): string {
  const sortedKeys = Object.keys(params).sort()
  
  let signString = ''
  sortedKeys.forEach(key => {
    if (params[key] !== undefined && params[key] !== null) {
      signString += key + params[key]
    }
  })
  signString += secret
  
  return crypto.createHash('md5').update(signString).digest('hex').toUpperCase()
}

// 方法 3: 使用=和&连接
function generateSignV3(params: Record<string, string>, secret: string): string {
  const sortedKeys = Object.keys(params).sort()
  
  let signString = secret
  sortedKeys.forEach(key => {
    if (params[key] !== undefined && params[key] !== null) {
      signString += key + '=' + params[key] + '&'
    }
  })
  signString = signString.slice(0, -1) // 移除最后一个&
  signString += secret
  
  return crypto.createHash('md5').update(signString).digest('hex').toUpperCase()
}

// 方法 4: 先 URL 编码再拼接
function generateSignV4(params: Record<string, string>, secret: string): string {
  const sortedKeys = Object.keys(params).sort()
  
  let signString = secret
  sortedKeys.forEach(key => {
    if (params[key] !== undefined && params[key] !== null) {
      signString += key + encodeURIComponent(params[key])
    }
  })
  signString += secret
  
  return crypto.createHash('md5').update(signString).digest('hex').toUpperCase()
}

// 测试所有方法
console.log('【方法 1】当前实现: secret + key+value + secret')
const sign1 = generateSignV1({...baseParams}, APP_SECRET)
console.log('签名:', sign1)
console.log()

console.log('【方法 2】所有参数 + secret')
const sign2 = generateSignV2({...baseParams}, APP_SECRET)
console.log('签名:', sign2)
console.log()

console.log('【方法 3】使用= 和& 连接')
const sign3 = generateSignV3({...baseParams}, APP_SECRET)
console.log('签名:', sign3)
console.log()

console.log('【方法 4】URL 编码后拼接')
const sign4 = generateSignV4({...baseParams}, APP_SECRET)
console.log('签名:', sign4)
console.log()

// 分析 AppKey 格式问题
console.log('='.repeat(60))
console.log('📋 AppKey 格式分析')
console.log('='.repeat(60))
console.log()
console.log('提供的 AppKey:', APP_KEY)
console.log('长度:', APP_KEY.length)
console.log('格式:', '32 位十六进制字符串 (MD5 格式)')
console.log()
console.log('常见的 AppKey 格式:')
console.log('  - 淘宝: 数字 (如 35292826)')
console.log('  - 京东: 可能是数字或字母组合')
console.log()
console.log('⚠️  疑问: 这个 AppKey 看起来像 MD5 hash，可能不是原始 AppKey')
console.log()

// 建议
console.log('='.repeat(60))
console.log('💡 建议')
console.log('='.repeat(60))
console.log()
console.log('1. 登录京东联盟后台确认正确的 AppKey')
console.log('   网址: https://union.jd.com/')
console.log()
console.log('2. 检查 ID: 303298 对应的应用详情')
console.log('   路径: 推广管理 → API 管理 → 应用管理')
console.log()
console.log('3. 参考官方文档解决方案')
console.log('   https://open.jd.com/v2/#/doc/guide?listId=533')
console.log()
