'use client'

import '@/lib/process-polyfill'
import NextImage, { ImageProps } from 'next/image'

// Use injected process.env value from webpack DefinePlugin for static export compatibility
const basePath = (process.env.NEXT_PUBLIC_BASE_PATH as string) || ''

const Image = ({ src, ...rest }: ImageProps) => (
  <NextImage src={`${basePath || ''}${src}`} {...rest} />
)

export default Image
