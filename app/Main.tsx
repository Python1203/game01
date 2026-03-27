'use client'

import '@/lib/process-polyfill'

import Link from '@/components/Link'
import Tag from '@/components/Tag'
import siteMetadata from '@/data/siteMetadata'
import { formatDate } from 'pliny/utils/formatDate'
import NewsletterForm from 'pliny/ui/NewsletterForm'
import Image from 'next/image'
import { useState, useEffect } from 'react'

const MAX_DISPLAY = 5

export default function Home({ posts }) {
  const [mounted, setMounted] = useState(false)

  useEffect(() => {
    setMounted(true)
  }, [])

  // 服务端和客户端都渲染相同的内容，避免水合错误
  // 只在客户端添加交互功能
  return (
    <>
      {/* Welcome Section */}
      <div className="divide-y divide-gray-200 dark:divide-gray-700">
        <div className="space-y-2 pt-6 pb-8 md:space-y-5">
          <h1 className="text-3xl leading-9 font-extrabold tracking-tight text-gray-900 sm:text-4xl sm:leading-10 md:text-6xl md:leading-14 dark:text-gray-100">
            精选文章
          </h1>
          <p className="text-lg leading-7 text-gray-500 dark:text-gray-400">
            {siteMetadata.description}
          </p>
          
          {/* 置顶标识 */}
          <div className="mt-4 inline-flex items-center space-x-2 bg-gradient-to-r from-primary-500 to-primary-600 text-white px-4 py-2 rounded-full text-sm font-medium shadow-md">
            <svg className="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
              <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
            </svg>
            <span>精心挑选 · 品质推荐</span>
          </div>
          
          {/* Author Info Card */}
          <div className="mt-8 p-6 bg-gray-50 dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700">
            <div className="flex items-center space-x-4">
              <div className="relative w-16 h-16 flex-shrink-0">
                <Image
                  src="/static/images/avatar.png"
                  alt="888 - Founder & CEO"
                  width={64}
                  height={64}
                  className="rounded-full"
                />
              </div>
              <div>
                <h2 className="text-xl font-bold text-gray-900 dark:text-gray-100">
                  888
                </h2>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  创始人 & CEO @ 888 Technology Studio
                </p>
                <div className="mt-2 flex space-x-3">
                  <Link
                    href="https://github.com/Python1203"
                    className="text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200"
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    GitHub
                  </Link>
                  <Link
                    href="https://linktr.ee/zzw868"
                    className="text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200"
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    LinkedIn
                  </Link>
                  <Link
                    href="https://linktr.ee/zzw868"
                    className="text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200"
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    Twitter
                  </Link>
                  <Link
                    href="/about"
                    className="text-primary-500 hover:text-primary-600 dark:text-primary-400 dark:hover:text-primary-300 font-medium"
                  >
                    了解更多 →
                  </Link>
                </div>
              </div>
            </div>
          </div>
        </div>
        {posts.length === 0 ? (
          <p className="py-12 text-gray-500 dark:text-gray-400">No posts found.</p>
        ) : (
          <ul className="divide-y divide-gray-200 dark:divide-gray-700">
            {posts.slice(0, MAX_DISPLAY).map((post, index) => {
              const { slug, date, title, summary, tags, image, author, readingTime: postReadingTime } = post
              
              // 计算阅读时间（如果没有预计算）
              const readingTimeMinutes = postReadingTime ? Math.round(postReadingTime.minutes) : 5
              
              // 判断是否为置顶文章
              const isFeatured = index === 0
              
              return (
                <li key={slug} className={`py-8 ${isFeatured ? 'bg-gradient-to-r from-primary-50 to-white dark:from-primary-900/20 dark:to-transparent -mx-4 px-4 rounded-lg' : ''}`}>
                  <article className="group relative">
                    {/* 置顶标签 */}
                    {isFeatured && (
                      <div className="absolute -top-3 left-4 z-10">
                        <span className="inline-flex items-center space-x-1 bg-primary-500 text-white text-xs font-bold px-3 py-1 rounded-full shadow-lg">
                          <svg className="h-3 w-3" fill="currentColor" viewBox="0 0 20 20">
                            <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                          </svg>
                          <span>TOP 1</span>
                        </span>
                      </div>
                    )}
                    <div className="space-y-2 xl:grid xl:grid-cols-4 xl:gap-x-6 xl:space-y-0">
                      {/* 日期和元信息 */}
                      <div className="flex flex-col space-y-4 xl:col-span-1">
                        <dl>
                          <dt className="sr-only">Published on</dt>
                          <dd className="text-sm leading-6 font-medium text-gray-500 dark:text-gray-400">
                            <time dateTime={date} suppressHydrationWarning>
                              {formatDate(date, siteMetadata.locale)}
                            </time>
                          </dd>
                        </dl>
                        
                        {/* 阅读时间 */}
                        <div className="flex items-center space-x-2 text-xs text-gray-500 dark:text-gray-400">
                          <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                          </svg>
                          <span>{readingTimeMinutes} 分钟阅读</span>
                        </div>
                        
                        {/* 作者信息 */}
                        {author && (
                          <div className="flex items-center space-x-2 text-xs text-gray-500 dark:text-gray-400">
                            <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                            </svg>
                            <span>{author}</span>
                          </div>
                        )}
                      </div>
                      
                      {/* 文章内容 */}
                      <div className="space-y-4 xl:col-span-3">
                        <div className="space-y-3">
                          {/* 标题 */}
                          <h2 className="text-2xl leading-8 font-bold tracking-tight group-hover:text-primary-500 transition-colors duration-200">
                            <Link
                              href={`/blog/${slug}`}
                              className="text-gray-900 dark:text-gray-100"
                            >
                              {title}
                            </Link>
                          </h2>
                          
                          {/* 标签 */}
                          {tags && tags.length > 0 && (
                            <div className="flex flex-wrap gap-2">
                              {tags.map((tag) => (
                                <Tag key={tag} text={tag} />
                              ))}
                            </div>
                          )}
                          
                          {/* 摘要 */}
                          <div className="prose prose-gray dark:prose-invert max-w-none">
                            <p className="text-gray-600 dark:text-gray-300 line-clamp-3">
                              {summary}
                            </p>
                          </div>
                        </div>
                        
                        {/* 阅读更多链接 */}
                        <div className="flex items-center justify-between">
                          <Link
                            href={`/blog/${slug}`}
                            className="inline-flex items-center text-primary-500 hover:text-primary-600 dark:hover:text-primary-400 font-medium transition-colors duration-200"
                            aria-label={`Read more: "${title}"`}
                          >
                            阅读全文
                            <svg className="ml-2 h-4 w-4 transform group-hover:translate-x-1 transition-transform duration-200" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                            </svg>
                          </Link>
                        </div>
                      </div>
                    </div>
                  </article>
                </li>
              )
            })}
          </ul>
        )}
      </div>
      {posts.length > MAX_DISPLAY && (
        <div className="flex justify-end text-base leading-6 font-medium">
          <Link
            href="/blog"
            className="text-primary-500 hover:text-primary-600 dark:hover:text-primary-400"
            aria-label="All posts"
          >
            All Posts &rarr;
          </Link>
        </div>
      )}
      {siteMetadata.newsletter?.provider && (
        <div className="flex items-center justify-center pt-4">
          <NewsletterForm />
        </div>
      )}
    </>
  )
}
