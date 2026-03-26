import { sortPosts, allCoreContent } from 'pliny/utils/contentlayer'
import { allBlogs } from 'contentlayer/generated'
import Main from './Main'

export default async function Page() {
  const sortedPosts = sortPosts(allBlogs)
  const allPosts = allCoreContent(sortedPosts)
  
  // 只保留两篇精选文章并置顶
  const featuredSlugs = ['taobao-alcohol-rankings-2026', 'digital-products-roundup']
  const featuredPosts = allPosts.filter(post => 
    featuredSlugs.includes(post.slug.split('/').pop() || '')
  )
  
  // 按指定顺序排列（酒水排行榜第一，数码产品第二）
  const orderedPosts = featuredSlugs.map(slug => 
    featuredPosts.find(post => post.slug.split('/').pop() === slug)
  ).filter(Boolean)
  
  return <Main posts={orderedPosts} />
}
