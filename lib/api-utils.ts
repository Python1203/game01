/**
 * API 调用工具类 - 提供错误处理、重试和缓存功能
 */

interface RetryOptions {
  maxRetries?: number      // 最大重试次数
  retryDelay?: number      // 重试间隔 (ms)
  backoffMultiplier?: number // 退避乘数
}

interface CacheOptions {
  enabled?: boolean        // 是否启用缓存
  ttl?: number            // 缓存时间 (秒)
  key?: string           // 自定义缓存键
}

/**
 * 带重试的异步函数执行器
 */
export async function withRetry<T>(
  fn: () => Promise<T>,
  options: RetryOptions = {}
): Promise<T> {
  const {
    maxRetries = 3,
    retryDelay = 1000,
    backoffMultiplier = 2,
  } = options

  let lastError: Error

  for (let attempt = 1; attempt <= maxRetries + 1; attempt++) {
    try {
      return await fn()
    } catch (error) {
      lastError = error as Error
      
      if (attempt <= maxRetries) {
        const delay = retryDelay * Math.pow(backoffMultiplier, attempt - 1)
        console.warn(`API 调用失败，${delay / 1000}s 后重试 (第 ${attempt}/${maxRetries} 次):`, lastError.message)
        await new Promise(resolve => setTimeout(resolve, delay))
      } else {
        console.error('API 调用最终失败:', lastError)
        throw lastError
      }
    }
  }

  throw lastError!
}

// 简单的内存缓存
const cache = new Map<string, { data: any; expires: number }>()

/**
 * 带缓存的异步函数执行器
 */
export async function withCache<T>(
  fn: () => Promise<T>,
  options: CacheOptions = {}
): Promise<T> {
  const {
    enabled = true,
    ttl = 300, // 默认缓存 5 分钟
    key,
  } = options

  if (!enabled) {
    return fn()
  }

  const cacheKey = key || `cache_${Date.now()}_${Math.random()}`

  // 检查缓存
  const cached = cache.get(cacheKey)
  if (cached && cached.expires > Date.now()) {
    console.log('命中缓存:', cacheKey)
    return cached.data as T
  }

  // 执行函数并缓存结果
  const result = await fn()
  cache.set(cacheKey, {
    data: result,
    expires: Date.now() + ttl * 1000,
  })

  console.log('更新缓存:', cacheKey)
  return result
}

/**
 * 清理过期缓存
 */
export function cleanupCache() {
  const now = Date.now()
  let count = 0
  
  cache.forEach((value, key) => {
    if (value.expires < now) {
      cache.delete(key)
      count++
    }
  })

  if (count > 0) {
    console.log(`清理了 ${count} 条过期缓存`);
  }
}

/**
 * 手动清除指定缓存
 */
export function invalidateCache(key: string) {
  cache.delete(key)
  console.log('清除缓存:', key)
}

/**
 * 获取缓存统计信息
 */
export function getCacheStats() {
  const now = Date.now()
  let validCount = 0
  let expiredCount = 0

  cache.forEach(value => {
    if (value.expires > now) {
      validCount++
    } else {
      expiredCount++
    }
  })

  return {
    total: cache.size,
    valid: validCount,
    expired: expiredCount,
  }
}
