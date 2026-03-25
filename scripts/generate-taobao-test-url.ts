/**
 * 生成完整的淘宝 API 请求 URL
 * 可以直接在浏览器中打开测试
 */

import crypto from 'crypto'

const APP_KEY = '35292826'
const APP_SECRET = 'a728f67b7dd1ecc65d1f17dcb04d953f'

// 格式化时间戳
const now = new Date()
const year = now.getFullYear()
const month = String(now.getMonth() + 1).padStart(2, '0')
const day = String(now.getDate()).padStart(2, '0')
const hours = String(now.getHours()).padStart(2, '0')
const minutes = String(now.getMinutes()).padStart(2, '0')
const seconds = String(now.getSeconds()).padStart(2, '0')
const timestamp = `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`

// 参数
const params = {
  app_key: APP_KEY,
  method: 'taobao.time.get',
  timestamp: timestamp,
  v: '2.0',
  format: 'json',
}

// 生成签名
const sortedKeys = Object.keys(params).sort()
let signString = APP_SECRET
sortedKeys.forEach(key => {
  if (params[key] !== undefined && params[key] !== null) {
    signString += key + params[key]
  }
})
signString += APP_SECRET

const sign = crypto.createHash('md5').update(signString, 'utf8').digest('hex').toUpperCase()
params.sign = sign

// 构建 URL
const url = new URL('https://eco.taobao.com/router/rest')
Object.entries(params).forEach(([key, value]) => {
  url.searchParams.append(key, String(value))
})

console.log('='.repeat(60))
console.log('淘宝 API 测试 URL')
console.log('='.repeat(60))
console.log()
console.log('签名字符串:')
console.log(signString)
console.log()
console.log('生成的签名:')
console.log(sign)
console.log()
console.log('完整 URL:')
console.log(url.toString())
console.log()
console.log('请在浏览器中打开此 URL 进行测试')
console.log('或者使用 curl 命令:')
console.log(`curl "${url.toString()}"`)
console.log('='.repeat(60))
