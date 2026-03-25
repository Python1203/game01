'use client'

import React, { useState, useEffect } from 'react'
import AllianceCard from './AllianceCard'

interface Product {
  id: string
  title: string
  picUrl: string
  price: number
  commissionRate: number
  promoCode: string
  platform: 'taobao' | 'jd'
  categoryId?: string
  shopTitle?: string
}

interface AllianceGridProps {
  showFilter?: boolean
  limit?: number
}

const AllianceGrid: React.FC<AllianceGridProps> = ({ 
  showFilter = true, 
  limit = 20 
}) => {
  const [products, setProducts] = useState<Product[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  
  // 筛选状态
  const [platform, setPlatform] = useState<'all' | 'taobao' | 'jd'>('all')
  const [minPrice, setMinPrice] = useState<string>('')
  const [maxPrice, setMaxPrice] = useState<string>('')

  // 加载商品数据
  useEffect(() => {
    const fetchProducts = async () => {
      try {
        setLoading(true)
        setError(null)
        
        const params = new URLSearchParams({
          platform,
          limit: limit.toString(),
        })
        
        if (minPrice) params.append('minPrice', minPrice)
        if (maxPrice) params.append('maxPrice', maxPrice)
        
        const response = await fetch(`/api/alliance/products?${params.toString()}`)
        
        if (!response.ok) {
          throw new Error('获取商品失败')
        }
        
        const data = await response.json()
        setProducts(data.products)
      } catch (err) {
        console.error('Fetch error:', err)
        setError(err instanceof Error ? err.message : '未知错误')
      } finally {
        setLoading(false)
      }
    }

    // 防抖处理
    const timer = setTimeout(fetchProducts, 300)
    return () => clearTimeout(timer)
  }, [platform, minPrice, maxPrice, limit])

  // 计算统计数据
  const totalCommission = products.reduce((sum, p) => {
    return sum + (p.price * p.commissionRate / 100)
  }, 0)

  return (
    <div style={styles.container}>
      {/* 筛选工具栏 */}
      {showFilter && (
        <div style={styles.filterBar}>
          <div style={styles.filterGroup}>
            <label style={styles.filterLabel}>平台:</label>
            <select
              value={platform}
              onChange={(e) => setPlatform(e.target.value as typeof platform)}
              style={styles.select}
            >
              <option value="all">全部</option>
              <option value="taobao">淘宝</option>
              <option value="jd">京东</option>
            </select>
          </div>

          <div style={styles.filterGroup}>
            <label style={styles.filterLabel}>价格:</label>
            <input
              type="number"
              placeholder="最低"
              value={minPrice}
              onChange={(e) => setMinPrice(e.target.value)}
              style={styles.input}
            />
            <span style={styles.separator}>-</span>
            <input
              type="number"
              placeholder="最高"
              value={maxPrice}
              onChange={(e) => setMaxPrice(e.target.value)}
              style={styles.input}
            />
          </div>

          <div style={styles.stats}>
            <span style={styles.statItem}>共 {products.length} 个商品</span>
            <span style={styles.statItem}>
              预估总佣金：¥{totalCommission.toFixed(2)}
            </span>
          </div>
        </div>
      )}

      {/* 加载状态 */}
      {loading && (
        <div style={styles.loadingContainer}>
          <div style={styles.spinner}></div>
          <p style={styles.loadingText}>正在加载商品...</p>
        </div>
      )}

      {/* 错误提示 */}
      {error && (
        <div style={styles.errorContainer}>
          <p style={styles.errorText}>❌ {error}</p>
        </div>
      )}

      {/* 商品列表 */}
      {!loading && !error && products.length === 0 && (
        <div style={styles.emptyContainer}>
          <p style={styles.emptyText}>暂无商品</p>
        </div>
      )}

      {/* 商品网格 */}
      {!loading && !error && products.length > 0 && (
        <div style={styles.grid}>
          {products.map((product) => (
            <AllianceCard key={product.id} item={product} />
          ))}
        </div>
      )}
    </div>
  )
}

// 样式定义
const styles: Record<string, React.CSSProperties> = {
  container: {
    maxWidth: '1200px',
    margin: '0 auto',
    padding: '20px',
  },
  filterBar: {
    backgroundColor: '#fff',
    padding: '20px',
    borderRadius: '12px',
    marginBottom: '20px',
    boxShadow: '0 2px 8px rgba(0, 0, 0, 0.05)',
    display: 'flex',
    flexWrap: 'wrap',
    gap: '20px',
    alignItems: 'center',
  },
  filterGroup: {
    display: 'flex',
    alignItems: 'center',
    gap: '8px',
  },
  filterLabel: {
    fontSize: '14px',
    color: '#666',
    fontWeight: '500',
  },
  select: {
    padding: '8px 12px',
    border: '1px solid #ddd',
    borderRadius: '6px',
    fontSize: '14px',
    cursor: 'pointer',
    outline: 'none',
  },
  input: {
    width: '100px',
    padding: '8px 12px',
    border: '1px solid #ddd',
    borderRadius: '6px',
    fontSize: '14px',
    outline: 'none',
  },
  separator: {
    color: '#999',
  },
  stats: {
    marginLeft: 'auto',
    display: 'flex',
    gap: '16px',
    fontSize: '13px',
  },
  statItem: {
    color: '#666',
    padding: '4px 8px',
    backgroundColor: '#f5f5f5',
    borderRadius: '4px',
  },
  loadingContainer: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    padding: '60px 20px',
    backgroundColor: '#fff',
    borderRadius: '12px',
  },
  spinner: {
    width: '40px',
    height: '40px',
    border: '4px solid #f3f3f3',
    borderTop: '4px solid #ff5000',
    borderRadius: '50%',
    animation: 'spin 1s linear infinite',
  },
  loadingText: {
    marginTop: '16px',
    color: '#999',
    fontSize: '14px',
  },
  errorContainer: {
    padding: '20px',
    backgroundColor: '#fee',
    borderRadius: '8px',
    textAlign: 'center',
  },
  errorText: {
    color: '#c33',
    fontSize: '14px',
    margin: 0,
  },
  emptyContainer: {
    padding: '60px 20px',
    backgroundColor: '#fff',
    borderRadius: '12px',
    textAlign: 'center',
  },
  emptyText: {
    color: '#999',
    fontSize: '16px',
    margin: 0,
  },
  grid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fill, minmax(350px, 1fr))',
    gap: '20px',
  },
}

export default AllianceGrid
