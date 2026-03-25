'use client'

import { useState, useEffect } from 'react'
import AffiliateCard from './AffiliateCard'

interface Product {
  platform: 'taobao' | 'jd' | 'pinduoduo'
  originalLink: string
  title: string
  image?: string
  price?: string
  coupon?: string
  commission?: string
}

interface AffiliateGridProps {
  products: Product[]
  columns?: 1 | 2 | 3
  showFilter?: boolean
}

/**
 * 联盟商品网格展示组件
 * 支持筛选、排序、批量展示
 */
export default function AffiliateGrid({
  products,
  columns = 2,
  showFilter = false,
}: AffiliateGridProps) {
  const [filter, setFilter] = useState<'all' | 'taobao' | 'jd'>('all')
  const [sortBy, setSortBy] = useState<'default' | 'price_low' | 'price_high'>('default')

  // 筛选商品
  const filteredProducts = products.filter((product) => {
    if (filter === 'all') return true
    return product.platform === filter
  })

  // 排序商品
  const sortedProducts = [...filteredProducts].sort((a, b) => {
    if (sortBy === 'price_low') {
      return parseFloat(a.price || '0') - parseFloat(b.price || '0')
    } else if (sortBy === 'price_high') {
      return parseFloat(b.price || '0') - parseFloat(a.price || '0')
    }
    return 0
  })

  // 获取列数对应的 Tailwind 类名
  const getColumnClass = () => {
    switch (columns) {
      case 1:
        return 'grid-cols-1'
      case 2:
        return 'grid-cols-1 md:grid-cols-2'
      case 3:
        return 'grid-cols-1 md:grid-cols-2 lg:grid-cols-3'
      default:
        return 'grid-cols-1 md:grid-cols-2'
    }
  }

  return (
    <div className="my-8">
      {/* 筛选和排序工具栏 */}
      {showFilter && (
        <div className="mb-6 flex flex-wrap items-center justify-between gap-4">
          <div className="flex gap-2">
            <button
              onClick={() => setFilter('all')}
              className={`rounded-md px-4 py-2 text-sm font-medium transition-all ${
                filter === 'all'
                  ? 'bg-blue-500 text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              全部
            </button>
            <button
              onClick={() => setFilter('taobao')}
              className={`rounded-md px-4 py-2 text-sm font-medium transition-all ${
                filter === 'taobao'
                  ? 'bg-orange-500 text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              淘宝
            </button>
            <button
              onClick={() => setFilter('jd')}
              className={`rounded-md px-4 py-2 text-sm font-medium transition-all ${
                filter === 'jd'
                  ? 'bg-red-500 text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              京东
            </button>
          </div>

          <select
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value)}
            className="rounded-md border border-gray-300 px-4 py-2 text-sm focus:ring-2 focus:ring-blue-500 focus:outline-none"
          >
            <option value="default">默认排序</option>
            <option value="price_low">价格从低到高</option>
            <option value="price_high">价格从高到低</option>
          </select>
        </div>
      )}

      {/* 商品网格 */}
      <div className={`grid ${getColumnClass()} gap-4`}>
        {sortedProducts.map((product, index) => (
          <AffiliateCard key={index} {...product} />
        ))}
      </div>

      {/* 统计信息 */}
      {showFilter && (
        <div className="mt-4 text-center text-sm text-gray-500">
          共 {sortedProducts.length} 件商品
          {filter !== 'all' && `（已筛选：${filter === 'taobao' ? '淘宝' : '京东'}）`}
          {sortBy !== 'default' &&
            ` | 排序：${sortBy === 'price_low' ? '价格从低到高' : '价格从高到低'}`}
        </div>
      )}
    </div>
  )
}
