import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'
import { getFinalUrl } from '@/data/affiliateLinks'

export function middleware(request: NextRequest) {
  const url = request.nextUrl
  const userAgent = request.headers.get('user-agent') || ''
  const isMobile = /Android|iPhone|iPad|iPod/i.test(userAgent)

  // 场景：拦截所有 /go/ 开头的跳转链接 (例如 /go/jd-keyboard)
  if (url.pathname.startsWith('/go/')) {
    const slug = url.pathname.replace('/go/', '')
    
    // 使用配置文件中的映射关系
    const finalUrl = getFinalUrl(slug, isMobile)
    
    if (finalUrl) {
      return NextResponse.redirect(new URL(finalUrl))
    }
  }

  return NextResponse.next()
}

// 仅拦截跳转路由，不影响正文 SEO 加载
export const config = {
  matcher: '/go/:path*',
}
