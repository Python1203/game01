import { Authors, allAuthors } from 'contentlayer/generated'
import { MDXLayoutRenderer } from 'pliny/mdx-components'
import AuthorLayout from '@/layouts/AuthorLayout'
import { coreContent } from 'pliny/utils/contentlayer'
import { genPageMetadata } from 'app/seo'

export const metadata = genPageMetadata({ title: 'About' })

export default function Page() {
  const author = allAuthors.find((p) => p.slug === 'default') as Authors
  
  // Fallback if author not found
  if (!author) {
    return (
      <div className="py-12 text-center">
        <h1 className="text-3xl font-bold">About Page</h1>
        <p className="mt-4">Author information not available.</p>
      </div>
    )
  }
  
  const mainContent = coreContent(author)

  return (
    <>
      <AuthorLayout content={mainContent}>
        <MDXLayoutRenderer code={author.body?.code || ''} />
      </AuthorLayout>
    </>
  )
}
