'use client'

import { useState, useEffect } from 'react'
import {
  PlatformType,
  convertTaobaoLink,
  convertJdLink,
  detectPlatform,
} from '@/utils/affiliateConverter'

interface AffiliateCardProps {
  platform: 'taobao' | 'jd' | 'pinduoduo'
  originalLink: string
  title: string
  image?: string
  price?: string
  coupon?: string
  commission?: string
}

/**
 * 联盟导购卡片组件
 * 根据用户设备自动切换展示形式（PC 端直接跳转，移动端唤起 APP）
 */
export default function AffiliateCard({
  platform,
  originalLink,
  title,
  image,
  price,
  coupon,
  commission,
}: AffiliateCardProps) {
  const [platformType, setPlatformType] = useState<PlatformType>('pc')
  const [convertedLink, setConvertedLink] = useState<string>('')
  const [copySuccess, setCopySuccess] = useState(false)

  useEffect(() => {
    // 检测设备类型
    const detected = detectPlatform()
    setPlatformType(detected)

    // 转换联盟链接
    if (platform === 'taobao') {
      setConvertedLink(convertTaobaoLink(originalLink, detected))
    } else if (platform === 'jd') {
      setConvertedLink(convertJdLink(originalLink, detected))
    }
  }, [platform, originalLink])

  // 复制链接到剪贴板（用于淘口令）
  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(convertedLink)
      setCopySuccess(true)
      setTimeout(() => setCopySuccess(false), 2000)
    } catch (err) {
      console.error('复制失败:', err)
    }
  }

  // 跳转到联盟链接
  const handleJump = () => {
    window.open(convertedLink, '_blank')
  }

  // 获取平台配色
  const getPlatformStyle = () => {
    switch (platform) {
      case 'taobao':
        return {
          bg: 'bg-orange-50',
          border: 'border-orange-500',
          text: 'text-orange-600',
          button:
            'bg-gradient-to-r from-orange-500 to-red-500 hover:from-orange-600 hover:to-red-600',
        }
      case 'jd':
        return {
          bg: 'bg-red-50',
          border: 'border-red-500',
          text: 'text-red-600',
          button: 'bg-gradient-to-r from-red-500 to-red-600 hover:from-red-600 hover:to-red-700',
        }
      case 'pinduoduo':
        return {
          bg: 'bg-red-50',
          border: 'border-red-400',
          text: 'text-red-500',
          button: 'bg-gradient-to-r from-red-500 to-pink-500 hover:from-red-600 hover:to-pink-600',
        }
      default:
        return {
          bg: 'bg-gray-50',
          border: 'border-gray-500',
          text: 'text-gray-600',
          button: 'bg-gradient-to-r from-gray-500 to-gray-600',
        }
    }
  }

  const style = getPlatformStyle()

  return (
    <div
      className={`my-6 rounded-lg border-l-4 p-4 ${style.border} ${style.bg} shadow-md transition-all duration-300 hover:shadow-lg`}
    >
      <div className="flex flex-col gap-4 sm:flex-row">
        {/* 商品图片 */}
        {image && (
          <div className="h-32 w-full flex-shrink-0 sm:w-32">
            <img
              src={image}
              alt={title}
              className="h-full w-full rounded-md object-cover"
              loading="lazy"
            />
          </div>
        )}

        {/* 商品信息 */}
        <div className="flex-1">
          <h3 className="mb-2 text-lg font-bold text-gray-800">{title}</h3>

          {/* 价格和优惠券 */}
          <div className="mb-3 flex flex-wrap items-center gap-3">
            {price && <span className="text-2xl font-bold text-red-600">¥{price}</span>}
            {coupon && (
              <span className="rounded-full bg-red-500 px-2 py-1 text-sm text-white">
                券¥{coupon}
              </span>
            )}
            {commission && (
              <span className="rounded bg-gray-200 px-2 py-1 text-xs text-gray-500">
                佣¥{commission}
              </span>
            )}
          </div>

          {/* 操作按钮 */}
          <div className="flex flex-wrap gap-2">
            {platformType === 'mobile' ? (
              <>
                {/* 移动端：复制口令 + 打开 APP */}
                <button
                  onClick={handleCopy}
                  className={`rounded-md px-4 py-2 text-sm font-medium text-white transition-all ${style.button}`}
                >
                  {copySuccess ? '已复制' : '一键复制'}
                </button>
                <button
                  onClick={handleJump}
                  className="rounded-md border-2 border-current px-4 py-2 text-sm font-medium transition-all hover:opacity-80"
                >
                  立即打开
                </button>
              </>
            ) : (
              /* PC 端：直接购买 */
              <button
                onClick={handleJump}
                className={`rounded-md px-6 py-2 font-medium text-white transition-all ${style.button}`}
              >
                立即购买
              </button>
            )}
          </div>

          {/* 提示信息 */}
          {platformType === 'mobile' && (
            <p className="mt-2 text-xs text-gray-500">
              💡 点击「一键复制」后打开淘宝/京东 APP 即可查看详情
            </p>
          )}
        </div>
      </div>
    </div>
  )
}
