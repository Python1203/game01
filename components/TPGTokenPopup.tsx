'use client'

import React, { useState, useEffect } from 'react'

interface TPGTokenPopupProps {
  token?: string // 淘口令，例如："CZ0001 ABC1234"
  title?: string // 弹窗标题
  message?: string // 提示信息
}

const TPGTokenPopup: React.FC<TPGTokenPopupProps> = ({
  token = 'CZ0001 ABC1234',
  title = '口令已自动复制',
  message = '请切换至【手机淘宝】APP 即可查看宝贝',
}) => {
  const [isWechat, setIsWechat] = useState(false)
  const [showModal, setShowModal] = useState(false)
  const [copied, setCopied] = useState(false)

  useEffect(() => {
    // 1. 判断是否为微信环境
    const ua = window.navigator.userAgent.toLowerCase()
    const isWX = ua.indexOf('micromessenger') !== -1
    setIsWechat(isWX)

    if (isWX) {
      // 延迟一点执行，确保页面加载完成
      const timer = setTimeout(() => {
        handleAutoCopy()
      }, 500)
      return () => clearTimeout(timer)
    }
  }, [])

  const handleAutoCopy = async () => {
    try {
      // 2. 尝试复制到剪切板（优先使用现代 API）
      if (navigator.clipboard && navigator.clipboard.writeText) {
        await navigator.clipboard.writeText(token)
        setCopied(true)
        setShowModal(true)
      } else {
        // 兼容旧版浏览器的兜底方案
        const textArea = document.createElement('textarea')
        textArea.value = token
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
          }
        } catch (err) {
          console.error('执行 copy 命令失败:', err)
        }
        
        document.body.removeChild(textArea)
      }
    } catch (err) {
      console.error('复制失败:', err)
      // 即使复制失败也显示提示，让用户手动复制
      setShowModal(true)
    }
  }

  const handleClose = () => {
    setShowModal(false)
  }

  const handleManualCopy = async () => {
    try {
      if (navigator.clipboard && navigator.clipboard.writeText) {
        await navigator.clipboard.writeText(token)
        alert('复制成功！')
      }
    } catch (err) {
      console.error('手动复制失败:', err)
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
            <p style={styles.successText}>✓ 已复制到剪贴板</p>
          </div>
        ) : (
          <div style={styles.tokenBox}>
            <p style={styles.tokenLabel}>淘口令：</p>
            <p style={styles.token}>{token}</p>
            <button style={styles.copyButton} onClick={handleManualCopy}>
              点击复制
            </button>
          </div>
        )}
        
        <p style={styles.tips}>{message}</p>
        
        <div style={styles.footer}>
          <button style={styles.primaryButton} onClick={handleClose}>
            我知道了
          </button>
        </div>
      </div>
    </div>
  )
}

// 基础样式（可根据项目主题调整）
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
    marginBottom: '16px',
    margin: '0 0 16px 0',
  },
  successBox: {
    backgroundColor: '#f0f9ff',
    border: '1px solid #bae6fd',
    borderRadius: '8px',
    padding: '12px',
    marginBottom: '16px',
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
    marginBottom: '8px',
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
    transition: 'all 0.2s',
  },
  tips: {
    fontSize: '14px',
    color: '#6b7280',
    lineHeight: '1.6',
    marginBottom: '20px',
    margin: '0 0 20px 0',
  },
  footer: {
    display: 'flex',
    justifyContent: 'center',
  },
  primaryButton: {
    backgroundColor: '#ff5000',
    color: '#fff',
    border: 'none',
    padding: '12px 40px',
    borderRadius: '24px',
    fontSize: '16px',
    cursor: 'pointer',
    fontWeight: '600',
    width: '100%',
    transition: 'all 0.2s',
  },
}

export default TPGTokenPopup
