/**
 * 淘宝 API 签名验证工具
 * 用于生成可在线验证的签名信息
 */

import crypto from 'crypto'

// 配置
const APP_KEY = '35292826'
const APP_SECRET = 'a728f67b7dd1ecc65d1f17dcb04d953f'

// 测试参数
const params = {
  app_key: APP_KEY,
  method: 'taobao.time.get',
  timestamp: '2026-03-25 18:09:42',
  v: '2.0',
  format: 'json',
}

// 方法 1: 当前实现
function generateSignV1(params: Record<string, string>, secret: string): string {
  const sortedKeys = Object.keys(params).sort()
  
  let signString = secret
  sortedKeys.forEach(key => {
    if (params[key] !== undefined && params[key] !== null) {
      signString += key + params[key]
    }
  })
  signString += secret
  
  return crypto.createHash('md5').update(signString, 'utf8').digest('hex').toUpperCase()
}

// 方法 2: 尝试不同的拼接方式
function generateSignV2(params: Record<string, string>, secret: string): string {
  const sortedKeys = Object.keys(params).sort()
  
  // 不添加首尾 secret
  let signString = ''
  sortedKeys.forEach(key => {
    if (params[key] !== undefined && params[key] !== null) {
      signString += key + '=' + params[key] + '&'
    }
  })
  signString = signString.slice(0, -1) // 去掉最后的&
  
  console.log('V2 签名字符串:', signString)
  return crypto.createHash('md5').update(secret + signString + secret, 'utf8').digest('hex').toUpperCase()
}

// 方法 3: 先 URL 编码再签名
function generateSignV3(params: Record<string, string>, secret: string): string {
  const sortedKeys = Object.keys(params).sort()
  
  let signString = secret
  sortedKeys.forEach(key => {
    if (params[key] !== undefined && params[key] !== null) {
      const encodedValue = encodeURIComponent(params[key])
      signString += key + encodedValue
    }
  })
  signString += secret
  
  console.log('V3 签名字符串:', signString)
  return crypto.createHash('md5').update(signString, 'utf8').digest('hex').toUpperCase()
}

// 运行测试
console.log('='.repeat(60))
console.log('淘宝 API 签名验证工具')
console.log('='.repeat(60))
console.log()
console.log('测试参数:')
Object.entries(params).forEach(([key, value]) => {
  console.log(`  ${key}: ${value}`)
})
console.log()

const sign1 = generateSignV1(params, APP_SECRET)
console.log('方法 1 (当前实现) 签名:', sign1)

const sign2 = generateSignV2(params, APP_SECRET)
console.log('方法 2 (带=和&) 签名:', sign2)

const sign3 = generateSignV3(params, APP_SECRET)
console.log('方法 3 (URL 编码) 签名:', sign3)

console.log()
console.log('='.repeat(60))
console.log('请使用以下链接进行在线验证:')
console.log('https://open.taobao.com/signatureTool.htm')
console.log('='.repeat(60))
