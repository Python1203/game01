'use client'

import { Comments as CommentsComponent } from 'pliny/comments'
import { useState, useEffect } from 'react'
import siteMetadata from '@/data/siteMetadata'

export default function Comments({ slug }: { slug: string }) {
  const [mounted, setMounted] = useState(false)
  const [loadComments, setLoadComments] = useState(false)

  useEffect(() => {
    setMounted(true)
  }, [])

  if (!siteMetadata.comments?.provider) {
    return null
  }

  // 避免服务端和客户端渲染不一致
  if (!mounted) {
    return null
  }

  return (
    <>
      {loadComments ? (
        <CommentsComponent commentsConfig={siteMetadata.comments} slug={slug} />
      ) : (
        <button onClick={() => setLoadComments(true)}>Load Comments</button>
      )}
    </>
  )
}
