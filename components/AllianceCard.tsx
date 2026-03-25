'use client'

import React, { useState, useEffect } from 'react'

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

interface AllianceCardProps {
  item: Product
}

const AllianceCard: React.FC<AllianceCardProps> = ({ item }) => {
  const [copied, setCopied] = useState(false)
  const [isWechat, setIsWechat] = useState(false)

  useEffect(() => {
    // 检测是否为微信环境
    const ua = window.navigator.userAgent.toLowerCase()
    const isWX = ua.indexOf('micromessenger') !== -1
    setIsWechat(isWX)
  }, [])

  const handlePromotion = async () => {
    try {
      if (item.platform === 'taobao') {
        // 淘宝：复制淘口令
        if (navigator.clipboard && navigator.clipboard.writeText) {
          await navigator.clipboard.writeText(item.promoCode)
          setCopied(true)
          
          // 显示成功提示
          if (typeof window !== 'undefined') {
            alert('淘口令已复制，请打开手机淘宝下单')
          }
          
          setTimeout(() => setCopied(false), 3000)
        } else {
          // 兼容旧版浏览器
          const textArea = document.createElement('textarea')
          textArea.value = item.promoCode
          textArea.style.position = 'fixed'
          textArea.style.left = '-9999px'
          document.body.appendChild(textArea)
          textArea.select()
          document.execCommand('copy')
          document.body.removeChild(textArea)
          
          setCopied(true)
          if (typeof window !== 'undefined') {
            alert('淘口令已复制，请打开手机淘宝下单')
          }
          
          setTimeout(() => setCopied(false), 3000)
        }
      } else if (item.platform === 'jd') {
        // 京东：微信内复制链接，非微信直接跳转
        if (isWechat) {
          if (navigator.clipboard && navigator.clipboard.writeText) {
            await navigator.clipboard.writeText(item.promoCode)
            setCopied(true)
            
            if (typeof window !== 'undefined') {
              alert('京东优惠链接已复制，请粘贴到浏览器打开')
            }
            
            setTimeout(() => setCopied(false), 3000)
          }
        } else {
          // 直接跳转京东
          window.open(item.promoCode, '_blank')
        }
      }
    } catch (err) {
      console.error('操作失败:', err)
      if (typeof window !== 'undefined') {
        alert('操作失败，请手动复制')
      }
    }
  }

  // 计算预估佣金
  const estimatedCommission = (item.price * item.commissionRate / 100).toFixed(2)

  return (
    <div style={styles.card}>
      {/* 商品图片 */}
      <div style={styles.imageWrapper}>
        <img 
          src={item.picUrl} 
          alt={item.title} 
          style={styles.image}
          loading="lazy"
        />
        {item.platform === 'taobao' && (
          <div style={styles.taobaoBadge}>淘宝</div>
        )}
        {item.platform === 'jd' && (
          <div style={styles.jdBadge}>京东</div>
        )}
      </div>

      {/* 商品信息 */}
      <div style={styles.info}>
        {/* 标题 */}
        <h4 style={styles.title}>{item.title}</h4>

        {/* 价格行 */}
        <div style={styles.priceRow}>
          <span style={styles.price}>¥{item.price.toFixed(2)}</span>
          {item.commissionRate > 0 && (
            <span style={styles.badge}>券后</span>
          )}
        </div>

        {/* 佣金信息 */}
        {item.commissionRate > 0 && (
          <div style={styles.commission}>
            <span style={styles.commissionLabel}>预估赚:</span>
            <span style={styles.commissionAmount}>¥{estimatedCommission}</span>
            <span style={styles.commissionRate}>({item.commissionRate}%)</span>
          </div>
        )}

        {/* 店铺信息 */}
        {item.shopTitle && (
          <div style={styles.shopTitle}>{item.shopTitle}</div>
        )}

        {/* 操作按钮 */}
        <button 
          onClick={handlePromotion} 
          style={{
            ...styles.btn,
            ...(copied ? styles.btnSuccess : {})
          }}
        >
          {copied ? (
            <>✓ 已复制</>
          ) : (
            <>
              {item.platform === 'taobao' ? '🛍️ 一键领券' : '🛒 去京东购买'}
            </>
          )}
        </button>
      </div>
    </div>
  )
}

// 样式定义
const styles: Record<string, React.CSSProperties> = {
  card: {
    display: 'flex',
    padding: '16px',
    borderBottom: '1px solid #f0f0f0',
    background: '#fff',
    borderRadius: '12px',
    marginBottom: '12px',
    boxShadow: '0 2px 8px rgba(0, 0, 0, 0.05)',
    transition: 'transform 0.2s, box-shadow 0.2s',
    cursor: 'pointer',
  },
  imageWrapper: {
    position: 'relative',
    flexShrink: 0,
  },
  image: {
    width: '120px',
    height: '120px',
    borderRadius: '8px',
    objectFit: 'cover',
    marginRight: '16px',
  },
  taobaoBadge: {
    position: 'absolute',
    top: '4px',
    left: '4px',
    backgroundColor: '#ff5000',
    color: '#fff',
    fontSize: '10px',
    padding: '2px 6px',
    borderRadius: '4px',
    fontWeight: 'bold',
  },
  jdBadge: {
    position: 'absolute',
    top: '4px',
    left: '4px',
    backgroundColor: '#e1251b',
    color: '#fff',
    fontSize: '10px',
    padding: '2px 6px',
    borderRadius: '4px',
    fontWeight: 'bold',
  },
  info: {
    flex: 1,
    display: 'flex',
    flexDirection: 'column',
    justifyContent: 'space-between',
    minWidth: 0, // 防止内容溢出
  },
  title: {
    fontSize: '14px',
    margin: '0 0 8px',
    color: '#333',
    overflow: 'hidden',
    textOverflow: 'ellipsis',
    display: '-webkit-box',
    WebkitLineClamp: 2,
    WebkitBoxOrient: 'vertical',
    lineHeight: '1.4',
  },
  priceRow: {
    display: 'flex',
    alignItems: 'center',
    marginBottom: '8px',
  },
  price: {
    color: '#ff5000',
    fontSize: '20px',
    fontWeight: 'bold',
  },
  badge: {
    fontSize: '10px',
    background: 'linear-gradient(90deg, #ff8a00, #ff5000)',
    color: '#fff',
    padding: '2px 6px',
    borderRadius: '4px',
    marginLeft: '8px',
    fontWeight: '500',
  },
  commission: {
    display: 'flex',
    alignItems: 'center',
    gap: '6px',
    fontSize: '12px',
    marginBottom: '8px',
  },
  commissionLabel: {
    color: '#999',
  },
  commissionAmount: {
    color: '#ff5000',
    fontWeight: 'bold',
    fontSize: '14px',
  },
  commissionRate: {
    color: '#999',
    fontSize: '11px',
  },
  shopTitle: {
    fontSize: '12px',
    color: '#666',
    marginBottom: '8px',
    overflow: 'hidden',
    textOverflow: 'ellipsis',
    whiteSpace: 'nowrap',
  },
  btn: {
    background: 'linear-gradient(90deg, #ff8a00, #ff5000)',
    color: '#fff',
    border: 'none',
    padding: '10px 20px',
    borderRadius: '20px',
    fontSize: '14px',
    fontWeight: '600',
    cursor: 'pointer',
    transition: 'all 0.2s',
    alignSelf: 'flex-start',
    outline: 'none',
  },
  btnSuccess: {
    background: 'linear-gradient(90deg, #10b981, #059669)',
  },
}

export default AllianceCard
