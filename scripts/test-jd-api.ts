/**
 * 京东联盟 API 测试脚本
 * 
 * 使用方法：
 * npx tsx scripts/test-jd-api.ts
 */

// 手动加载环境变量
import { config } from 'dotenv'
import { resolve } from 'path'

config({ path: resolve(__dirname, '../.env.local') })

import { getJDItemList, testJDAPI } from '../lib/jd-api'

async function runTests() {
  console.log('='.repeat(60))
  console.log('🔍 开始测试京东联盟 API')
  console.log('='.repeat(60))
  console.log()

  // 测试 1: 基础连接测试
  console.log('【测试 1】基础连接测试...')
  try {
    const connected = await testJDAPI()
    if (connected) {
      console.log('✅ 连接成功！')
    } else {
      console.log('❌ 连接失败！请检查 API 密钥配置')
    }
  } catch (error) {
    console.log('❌ 连接异常:', (error as Error).message)
  }
  console.log()

  // 测试 2: 获取商品列表
  console.log('【测试 2】获取热门商品列表...')
  try {
    const startTime = Date.now()
    const products = await getJDItemList({ limit: 5 })
    const duration = Date.now() - startTime
    
    console.log(`⏱️  耗时：${duration}ms`)
    console.log(`📦 获取到 ${products.length} 个商品`)
    
    if (products.length > 0) {
      console.log('\n前 3 个商品:')
      products.slice(0, 3).forEach((product, index) => {
        console.log(`\n${index + 1}. ${product.title}`)
        console.log(`   价格：¥${product.price}`)
        console.log(`   佣金：${product.commissionRate}%`)
        console.log(`   图片：${product.picUrl ? '✅' : '❌'}`)
        console.log(`   链接：${product.promoCode ? '✅' : '❌'}`)
      })
    } else {
      console.log('⚠️  未获取到商品，可能是 API 限制或参数问题')
    }
  } catch (error) {
    console.log('❌ 获取商品失败:', (error as Error).message)
  }
  console.log()

  // 测试 3: 搜索特定商品
  console.log('【测试 3】搜索 "手机"...')
  try {
    const startTime = Date.now()
    const products = await getJDItemList({ keyword: '手机', limit: 3 })
    const duration = Date.now() - startTime
    
    console.log(`⏱️  耗时：${duration}ms`)
    console.log(`📦 获取到 ${products.length} 个商品`)
    
    if (products.length > 0) {
      console.log('\n商品列表:')
      products.forEach((product, index) => {
        console.log(`${index + 1}. ${product.title} - ¥${product.price}`)
      })
    }
  } catch (error) {
    console.log('❌ 搜索失败:', (error as Error).message)
  }
  console.log()

  // 测试 4: 价格区间筛选
  console.log('【测试 4】价格区间筛选 (1000-3000 元)...')
  try {
    const products = await getJDItemList({ 
      minPrice: 1000, 
      maxPrice: 3000, 
      limit: 3 
    })
    
    console.log(`📦 获取到 ${products.length} 个商品`)
    
    if (products.length > 0) {
      products.forEach((product, index) => {
        console.log(`${index + 1}. ${product.title} - ¥${product.price}`)
      })
    }
  } catch (error) {
    console.log('❌ 筛选失败:', (error as Error).message)
  }
  console.log()

  console.log('='.repeat(60))
  console.log('✅ 测试完成！')
  console.log('='.repeat(60))
}

// 运行测试
runTests().catch(console.error)
