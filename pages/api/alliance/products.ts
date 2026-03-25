import { NextApiRequest, NextApiResponse } from 'next'
import { getTaoBaoItemList, testTaoBaoAPI } from '@/lib/taobao-api'
import { getJDItemList, testJDAPI } from '@/lib/jd-api'
import { withRetry, withCache } from '@/lib/api-utils'

/**
 * 淘宝联盟商品数据结构
 */
interface TaoBaoProduct {
  id: string
  title: string
  picUrl: string
  price: number
  commissionRate: number // 佣金比例 (%)
  promoCode: string // 淘口令或转链后的链接
  platform: 'taobao'
  categoryId?: string
  shopTitle?: string
}

/**
 * 京东联盟商品数据结构
 */
interface JingDongProduct {
  id: string
  title: string
  picUrl: string
  price: number
  commissionRate: number // 佣金比例 (%)
  promoCode: string // 京东短链或口令
  platform: 'jd'
  categoryId?: string
  shopTitle?: string
}

type Product = TaoBaoProduct | JingDongProduct

/**
 * 模拟商品数据（实际项目中应该调用官方 API）
 * 
 * 淘宝联盟 API: https://open.taobao.com/doc.htm?docId=23466&docType=1
 * 京东联盟 API: https://union.jd.com/open/api
 */
const mockProducts: Product[] = [
  // 淘宝商品
  {
    id: 'tb001',
    title: '2024 新款冬季加厚羽绒服女士中长款',
    picUrl: 'https://picsum.photos/seed/downjacket/300/300',
    price: 399,
    commissionRate: 20,
    promoCode: 'CZ8848 TB2024DOWN',
    platform: 'taobao',
    categoryId: '50010850',
    shopTitle: '时尚女装旗舰店'
  },
  {
    id: 'tb002',
    title: '苹果数据线 iPhone15 快充线 2 米',
    picUrl: 'https://picsum.photos/seed/cable/300/300',
    price: 39.9,
    commissionRate: 30,
    promoCode: 'CZ0001 APPLE15CABLE',
    platform: 'taobao',
    categoryId: '50025705',
    shopTitle: '数码配件专营店'
  },
  
  // 京东商品
  {
    id: 'jd001',
    title: 'Apple iPhone 15 Pro Max (256GB) 原色钛金属',
    picUrl: 'https://picsum.photos/seed/iphone15/300/300',
    price: 8999,
    commissionRate: 3,
    promoCode: 'https://u.jd.com/xxxxx',
    platform: 'jd',
    categoryId: '9987',
    shopTitle: 'Apple 京东自营旗舰店'
  },
  {
    id: 'jd002',
    title: '戴森 Dyson V15 Detect Total Clean 吸尘器',
    picUrl: 'https://picsum.photos/seed/dyson/300/300',
    price: 4990,
    commissionRate: 5,
    promoCode: 'https://u.jd.com/yyyyy',
    platform: 'jd',
    categoryId: '15901',
    shopTitle: '戴森京东自营旗舰店'
  }
]

/**
 * GET /api/alliance/products
 * 获取联盟商品列表（当前使用模拟数据）
 * 
 * Query Parameters:
 * - platform: 'taobao' | 'jd' | 'all'
 * - category: 分类 ID
 * - minPrice: 最低价格
 * - maxPrice: 最高价格
 * - limit: 返回数量限制
 * - q: 搜索关键词
 */
export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<{ products: Product[]; total: number; error?: string }>
) {
  const { 
    platform = 'all', 
    category, 
    minPrice, 
    maxPrice, 
    limit = 20,
    q
  } = req.query

  try {
    let filteredProducts = [...mockProducts]

    // 按平台筛选
    if (platform !== 'all') {
      filteredProducts = filteredProducts.filter(p => p.platform === platform)
    }

    // 按分类筛选
    if (category) {
      filteredProducts = filteredProducts.filter(p => p.categoryId === category)
    }

    // 按价格范围筛选
    if (minPrice) {
      filteredProducts = filteredProducts.filter(p => p.price >= Number(minPrice))
    }
    if (maxPrice) {
      filteredProducts = filteredProducts.filter(p => p.price <= Number(maxPrice))
    }

    // 限制返回数量
    filteredProducts = filteredProducts.slice(0, Number(limit))

    // 计算总佣金
    const totalCommission = filteredProducts.reduce((sum, product) => {
      return sum + (product.price * product.commissionRate / 100)
    }, 0)

    console.log('API Response:', {
      count: filteredProducts.length,
      platform,
      totalCommission: totalCommission.toFixed(2)
    })

    res.status(200).json({
      products: filteredProducts,
      total: filteredProducts.length
    })
  } catch (error) {
    console.error('API Error:', error)
    res.status(500).json({ 
      products: [], 
      total: 0,
      error: '获取商品失败'
    })
  }
}
