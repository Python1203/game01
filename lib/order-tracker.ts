/**
 * 联盟订单跟踪工具类
 * 
 * 用于记录和统计推广订单数据
 */

export interface OrderRecord {
  id: string              // 订单 ID
  platform: 'taobao' | 'jd'
  itemId: string          // 商品 ID
  itemTitle: string       // 商品标题
  orderTime: number       // 下单时间戳
  price: number           // 订单金额
  commissionRate: number  // 佣金比例 (%)
  commission: number      // 预估佣金
  status: 'pending' | 'valid' | 'invalid' | 'settled'
  userId?: string         // 用户 ID（可选）
  clickSource?: string    // 点击来源（可选）
}

// 内存存储订单记录（生产环境应使用数据库）
const orders = new Map<string, OrderRecord>()

/**
 * 记录新订单
 */
export function recordOrder(order: Omit<OrderRecord, 'id'>): string {
  const orderId = `${order.platform}_${Date.now()}_${Math.random().toString(36).substring(2, 9)}`
  
  const fullOrder: OrderRecord = {
    ...order,
    id: orderId,
  }
  
  orders.set(orderId, fullOrder)
  console.log('记录新订单:', orderId, fullOrder)
  
  return orderId
}

/**
 * 更新订单状态
 */
export function updateOrderStatus(orderId: string, status: OrderRecord['status']): boolean {
  const order = orders.get(orderId)
  if (!order) {
    console.error('订单不存在:', orderId)
    return false
  }
  
  order.status = status
  orders.set(orderId, order)
  console.log('更新订单状态:', orderId, status)
  
  return true
}

/**
 * 获取单个订单详情
 */
export function getOrder(orderId: string): OrderRecord | undefined {
  return orders.get(orderId)
}

/**
 * 按条件查询订单
 */
export function queryOrders(filters: {
  platform?: 'taobao' | 'jd' | 'all'
  status?: OrderRecord['status']
  startDate?: number
  endDate?: number
  userId?: string
}): OrderRecord[] {
  let result = Array.from(orders.values())
  
  // 按平台筛选
  if (filters.platform && filters.platform !== 'all') {
    result = result.filter(o => o.platform === filters.platform)
  }
  
  // 按状态筛选
  if (filters.status) {
    result = result.filter(o => o.status === filters.status)
  }
  
  // 按时间范围筛选
  if (filters.startDate) {
    result = result.filter(o => o.orderTime >= filters.startDate!)
  }
  if (filters.endDate) {
    result = result.filter(o => o.orderTime <= filters.endDate!)
  }
  
  // 按用户筛选
  if (filters.userId) {
    result = result.filter(o => o.userId === filters.userId)
  }
  
  // 按订单时间排序（最新的在前）
  result.sort((a, b) => b.orderTime - a.orderTime)
  
  return result
}

/**
 * 统计佣金数据
 */
export function calculateCommissionStats(filters?: {
  platform?: 'taobao' | 'jd' | 'all'
  startDate?: number
  endDate?: number
}): {
  totalOrders: number
  totalSales: number
  totalCommission: number
  pendingCommission: number
  settledCommission: number
} {
  const ordersList = queryOrders(filters || {})
  
  const stats = {
    totalOrders: ordersList.length,
    totalSales: 0,
    totalCommission: 0,
    pendingCommission: 0,
    settledCommission: 0,
  }
  
  ordersList.forEach(order => {
    stats.totalSales += order.price
    stats.totalCommission += order.commission
    
    if (order.status === 'settled') {
      stats.settledCommission += order.commission
    } else if (order.status === 'pending' || order.status === 'valid') {
      stats.pendingCommission += order.commission
    }
  })
  
  return stats
}

/**
 * 获取订单列表（分页）
 */
export function getOrdersWithPagination(options: {
  page: number
  pageSize: number
  platform?: 'taobao' | 'jd' | 'all'
  status?: OrderRecord['status']
}): {
  orders: OrderRecord[]
  total: number
  totalPages: number
  currentPage: number
} {
  const { page, pageSize, platform, status } = options
  
  // 查询符合条件的订单
  const allOrders = queryOrders({ platform, status })
  const total = allOrders.length
  
  // 计算分页
  const totalPages = Math.ceil(total / pageSize)
  const startIndex = (page - 1) * pageSize
  const endIndex = startIndex + pageSize
  
  // 返回分页数据
  const paginatedOrders = allOrders.slice(startIndex, endIndex)
  
  return {
    orders: paginatedOrders,
    total,
    totalPages,
    currentPage: page,
  }
}

/**
 * 导出订单数据（CSV 格式）
 */
export function exportOrdersToCSV(): string {
  const allOrders = Array.from(orders.values())
  
  // CSV 表头
  const headers = [
    '订单 ID',
    '平台',
    '商品 ID',
    '商品标题',
    '下单时间',
    '订单金额',
    '佣金比例',
    '预估佣金',
    '状态',
  ]
  
  // CSV 内容
  const rows = allOrders.map(order => [
    order.id,
    order.platform,
    order.itemId,
    order.itemTitle,
    new Date(order.orderTime).toLocaleString('zh-CN'),
    order.price.toFixed(2),
    `${order.commissionRate}%`,
    order.commission.toFixed(2),
    order.status,
  ])
  
  // 拼接 CSV
  const csvContent = [
    headers.join(','),
    ...rows.map(row => row.map(cell => `"${cell}"`).join(','))
  ].join('\n')
  
  return csvContent
}

/**
 * 清理过期订单（保留最近 90 天）
 */
export function cleanupOldOrders(daysToKeep: number = 90): number {
  const cutoffTime = Date.now() - daysToKeep * 24 * 60 * 60 * 1000
  let deletedCount = 0
  
  orders.forEach((order, orderId) => {
    if (order.orderTime < cutoffTime) {
      orders.delete(orderId)
      deletedCount++
    }
  })
  
  if (deletedCount > 0) {
    console.log(`清理了 ${deletedCount} 条过期订单`)
  }
  
  return deletedCount
}
