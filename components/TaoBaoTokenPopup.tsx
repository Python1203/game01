'use client'

import React, { useState, useEffect } from 'react'
import siteMetadata from '@/data/siteMetadata'

interface TaoBaoTokenPopupProps {
  token?: string // 淘口令（可选，优先使用）
  taobaoLink?: string // 淘宝链接（可选，会自动提取或生成口令）
  title?: string
  message?: string
  autoShow?: boolean // 是否自动显示，默认 true
  delay?: number // 延迟显示时间（毫秒），默认 500ms
}

const TaoBaoTokenPopup: React.FC<TaoBaoTokenPopupProps> = ({
  token,
  taobaoLink,
  title = '淘口令已复制',
  message,
  autoShow = true,
  delay = 500,
}) => {
  const [isWechat, setIsWechat] = useState(false)
  const [showModal, setShowModal] = useState(false)
  const [copied, setCopied] = useState(false)
  const [displayToken, setDisplayToken] = useState<string>('')

  useEffect(() => {
    // 1. 判断是否为微信环境
    const ua = window.navigator.userAgent.toLowerCase()
    const isWX = ua.indexOf('micromessenger') !== -1
    setIsWechat(isWX)

    if (isWX && autoShow) {
      // 2. 准备淘口令
      const finalToken = token || generateTokenFromLink(taobaoLink) || getDefaultToken()
      setDisplayToken(finalToken)

      // 3. 延迟执行复制
      const timer = setTimeout(() => {
        handleAutoCopy(finalToken)
      }, delay)

      return () => clearTimeout(timer)
    }
  }, [token, taobaoLink, autoShow, delay])

  /**
   * 从淘宝链接生成简易淘口令
   */
  const generateTokenFromLink = (link?: string): string | null => {
    if (!link) return null
    
    try {
      const url = new URL(link)
      const params = new URLSearchParams(url.search)
      const id = params.get('id') || params.get('itemId')
      
      if (id) {
        // 生成类似 "CZ0001 xxxxxx" 的格式
        const randomCode = Math.random().toString(36).substring(2, 8).toUpperCase()
        return `CZ${randomCode} ${id}`
      }
    } catch {
      // 不是有效 URL
    }
    
    return null
  }

  /**
   * 获取默认淘口令（从配置或子组件传入）
   */
  const getDefaultToken = (): string => {
    // 这里可以接入你的默认口令逻辑
    return 'CZ0001 DEFAULT'
  }

  const handleAutoCopy = async (tokenToCopy: string) => {
    try {
      // 优先使用现代 Clipboard API
      if (navigator.clipboard && navigator.clipboard.writeText) {
        await navigator.clipboard.writeText(tokenToCopy)
        setCopied(true)
        setShowModal(true)
      } else {
        // 兼容旧版浏览器
        copyWithExecCommand(tokenToCopy)
      }
    } catch (err) {
      console.error('复制失败:', err)
      // 即使失败也显示弹窗
      setShowModal(true)
    }
  }

  const copyWithExecCommand = (text: string) => {
    const textArea = document.createElement('textarea')
    textArea.value = text
    textArea.style.position = 'fixed'
    textArea.style.left = '-9999px'
    textArea.style.top = '0'
    document.body.appendChild(textArea)
    textArea.select()
    
    try {
      const successful = document.execCommand('copy')
      if (successful) {
        setCopied(true)
        setShowModal(true)
      } else {
        setShowModal(true)
      }
    } catch (err) {
      console.error('执行 copy 命令失败:', err)
      setShowModal(true)
    }
    
    document.body.removeChild(textArea)
  }

  const handleClose = () => {
    setShowModal(false)
  }

  const handleManualCopy = () => {
    if (displayToken) {
      copyWithExecCommand(displayToken)
      alert('复制成功！')
    }
  }

  const openTaobaoApp = () => {
    if (taobaoLink) {
      // 尝试唤起淘宝 App
      window.location.href = taobaoLink
    } else {
      // 没有链接时，提示用户手动打开
      alert('请手动打开手机淘宝 APP')
    }
  }

  // 非微信环境或不显示弹窗时返回 null
  if (!isWechat || !showModal) return null

  return (
    <div style={styles.overlay} onClick={handleClose}>
      <div style={styles.modal} onClick={(e) => e.stopPropagation()}>
        <div style={styles.icon}>📋</div>
        <h3 style={styles.title}>{title}</h3>
        
        {copied ? (
          <div style={styles.successBox}>
            <div style={styles.checkIcon}>✓</div>
            <p style={styles.successText}>已复制到剪贴板</p>
          </div>
        ) : (
          <div style={styles.tokenBox}>
            <p style={styles.tokenLabel}>淘口令：</p>
            <p style={styles.token}>{displayToken}</p>
            <button style={styles.copyButton} onClick={handleManualCopy}>
              点击复制
            </button>
          </div>
        )}
        
        <p style={styles.tips}>{message || '请切换至【手机淘宝】APP 即可查看宝贝'}</p>
        
        <div style={styles.footer}>
          {taobaoLink && (
            <button 
              style={{...styles.primaryButton, ...styles.secondaryButton}} 
              onClick={openTaobaoApp}
            >
              打开淘宝
            </button>
          )}
          <button style={styles.primaryButton} onClick={handleClose}>
            我知道了
          </button>
        </div>
      </div>
    </div>
  )
}

// 样式定义
const styles: Record<string, React.CSSProperties> = {
  overlay: {
    position: 'fixed',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    backgroundColor: 'rgba(0, 0, 0, 0.7)',
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    zIndex: 9999,
    backdropFilter: 'blur(2px)',
  },
  modal: {
    width: '85%',
    maxWidth: '400px',
    backgroundColor: '#fff',
    borderRadius: '16px',
    padding: '24px',
    textAlign: 'center',
    boxShadow: '0 10px 40px rgba(0, 0, 0, 0.3)',
    animation: 'slideIn 0.3s ease-out',
  },
  icon: {
    fontSize: '48px',
    marginBottom: '12px',
  },
  title: {
    fontSize: '20px',
    fontWeight: '600',
    color: '#333',
    margin: '0 0 16px 0',
  },
  successBox: {
    backgroundColor: '#f0f9ff',
    border: '1px solid #bae6fd',
    borderRadius: '8px',
    padding: '16px',
    marginBottom: '16px',
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
  },
  checkIcon: {
    width: '32px',
    height: '32px',
    borderRadius: '50%',
    backgroundColor: '#0284c7',
    color: '#fff',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    fontSize: '18px',
    fontWeight: 'bold',
    marginBottom: '8px',
  },
  successText: {
    color: '#0284c7',
    fontSize: '14px',
    fontWeight: '500',
    margin: 0,
  },
  tokenBox: {
    backgroundColor: '#fff7ed',
    border: '2px dashed #fb923c',
    borderRadius: '8px',
    padding: '16px',
    marginBottom: '16px',
  },
  tokenLabel: {
    fontSize: '12px',
    color: '#9ca3af',
    margin: '0 0 8px 0',
  },
  token: {
    color: '#ff5000',
    fontWeight: 'bold',
    fontSize: '16px',
    fontFamily: 'monospace',
    marginBottom: '12px',
    margin: '0 0 12px 0',
    wordBreak: 'break-all',
  },
  copyButton: {
    backgroundColor: '#ff5000',
    color: '#fff',
    border: 'none',
    padding: '8px 20px',
    borderRadius: '20px',
    fontSize: '14px',
    cursor: 'pointer',
    fontWeight: '500',
  },
  tips: {
    fontSize: '14px',
    color: '#6b7280',
    lineHeight: '1.6',
    margin: '0 0 20px 0',
  },
  footer: {
    display: 'flex',
    gap: '12px',
    justifyContent: 'center',
  },
  primaryButton: {
    backgroundColor: '#ff5000',
    color: '#fff',
    border: 'none',
    padding: '12px 30px',
    borderRadius: '24px',
    fontSize: '16px',
    cursor: 'pointer',
    fontWeight: '600',
    flex: 1,
    maxWidth: '150px',
  },
  secondaryButton: {
    backgroundColor: '#3b82f6',
  },
}

export default TaoBaoTokenPopup
