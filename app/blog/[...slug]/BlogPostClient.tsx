'use client'

import 'css/prism.css'
import 'katex/dist/katex.css'

// Polyfill for process.env to support pliny/mdx-components
if (typeof window !== 'undefined' && !(window as any).process) {
  (window as any).process = {
    env: {
      NODE_ENV: 'development',
    },
  }
}

import { components } from '@/components/MDXComponents'
import { MDXLayoutRenderer } from 'pliny/mdx-components'
import type { Authors, Blog } from 'contentlayer/generated'
import PostSimple from '@/layouts/PostSimple'
import PostLayout from '@/layouts/PostLayout'
import PostBanner from '@/layouts/PostBanner'

const defaultLayout = 'PostLayout'
const layouts = {
  PostSimple,
  PostLayout,
  PostBanner,
}

interface BlogPostClientProps {
  post: Blog
  authorDetails: Array<{ name: string }>
  next?: any
  prev?: any
}

export default function BlogPostClient({ post, authorDetails, next, prev }: BlogPostClientProps) {
  const jsonLd = post.structuredData
  jsonLd['author'] = authorDetails.map((author) => {
    return {
      '@type': 'Person',
      name: author.name,
    }
  })

  const Layout = layouts[post.layout || defaultLayout]

  return (
    <>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
      />
      <Layout content={post} authorDetails={authorDetails} next={next} prev={prev}>
        <MDXLayoutRenderer code={post.body.code} components={components} toc={post.toc} />
      </Layout>
    </>
  )
}
