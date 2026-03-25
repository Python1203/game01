import { NextApiRequest, NextApiResponse } from 'next'
import { 
  recordOrder, 
  queryOrders, 
  updateOrderStatus,
  calculateCommissionStats,
  getOrdersWithPagination,
  exportOrdersToCSV,
  cleanupOldOrders,
} from '@/lib/order-tracker'

/**
 * GET /api/alliance/orders
 * 查询订单列表或统计信息
 * 
 * POST /api/alliance/orders
 * 记录新订单
 * 
 * PUT /api/alliance/orders/:id
 * 更新订单状态
 */
export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  const { method } = req
  
  switch (method) {
    case 'GET':
      return handleGet(req, res)
    
    case 'POST':
      return handlePost(req, res)
    
    case 'PUT':
      return handlePut(req, res)
    
    default:
      res.setHeader('Allow', ['GET', 'POST', 'PUT'])
      res.status(405).json({ error: `Method ${method} not allowed` })
  }
}

/**
 * GET - 查询订单或统计
 */
async function handleGet(req: NextApiRequest, res: NextApiResponse) {
  const { 
    action = 'list',
    platform,
    status,
    startDate,
    endDate,
    page,
    pageSize,
    export: shouldExport,
  } = req.query
  
  try {
    // 导出 CSV
    if (shouldExport === 'true') {
      const csv = exportOrdersToCSV()
      res.setHeader('Content-Type', 'text/csv')
      res.setHeader('Content-Disposition', 'attachment; filename=orders.csv')
      return res.send(csv)
    }
    
    // 获取统计数据
    if (action === 'stats') {
      const stats = calculateCommissionStats({
        platform: platform as any,
        startDate: startDate ? Number(startDate) : undefined,
        endDate: endDate ? Number(endDate) : undefined,
      })
      
      return res.status(200).json(stats)
    }
    
    // 获取订单列表（分页）
    if (page && pageSize) {
      const result = getOrdersWithPagination({
        page: Number(page),
        pageSize: Number(pageSize),
        platform: platform as any,
        status: status as any,
      })
      
      return res.status(200).json(result)
    }
    
    // 简单查询
    const orders = queryOrders({
      platform: platform as any,
      status: status as any,
      startDate: startDate ? Number(startDate) : undefined,
      endDate: endDate ? Number(endDate) : undefined,
    })
    
    return res.status(200).json({ orders, total: orders.length })
  } catch (error) {
    console.error('查询订单失败:', error)
    return res.status(500).json({ error: '查询订单失败' })
  }
}

/**
 * POST - 记录新订单
 */
async function handlePost(req: NextApiRequest, res: NextApiResponse) {
  try {
    const { 
      platform,
      itemId,
      itemTitle,
      price,
      commissionRate,
      userId,
      clickSource,
    } = req.body
    
    // 参数验证
    if (!platform || !itemId || !itemTitle || !price || !commissionRate) {
      return res.status(400).json({ 
        error: '缺少必要参数：platform, itemId, itemTitle, price, commissionRate' 
      })
    }
    
    const orderId = recordOrder({
      platform,
      itemId,
      itemTitle,
      orderTime: Date.now(),
      price: Number(price),
      commissionRate: Number(commissionRate),
      commission: Number(price) * Number(commissionRate) / 100,
      status: 'pending',
      userId: userId as string,
      clickSource: clickSource as string,
    })
    
    return res.status(201).json({ 
      success: true, 
      orderId,
      message: '订单记录成功' 
    })
  } catch (error) {
    console.error('记录订单失败:', error)
    return res.status(500).json({ error: '记录订单失败' })
  }
}

/**
 * PUT - 更新订单状态
 */
async function handlePut(req: NextApiRequest, res: NextApiResponse) {
  try {
    const { id } = req.query
    const { status } = req.body
    
    if (!id) {
      return res.status(400).json({ error: '缺少订单 ID' })
    }
    
    if (!status || !['pending', 'valid', 'invalid', 'settled'].includes(status)) {
      return res.status(400).json({ 
        error: '无效的状态值：pending, valid, invalid, settled' 
      })
    }
    
    const success = updateOrderStatus(id as string, status as any)
    
    if (success) {
      return res.status(200).json({ 
        success: true, 
        message: '订单状态已更新' 
      })
    } else {
      return res.status(404).json({ error: '订单不存在' })
    }
  } catch (error) {
    console.error('更新订单失败:', error)
    return res.status(500).json({ error: '更新订单失败' })
  }
}
