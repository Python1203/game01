const { withContentlayer } = require('next-contentlayer2')

const withBundleAnalyzer = require('@next/bundle-analyzer')({
  enabled: process.env.ANALYZE === 'true',
})

// You might need to insert additional domains in script-src if you are using external services
const ContentSecurityPolicy = `
  default-src 'self';
  script-src 'self' 'unsafe-eval' 'unsafe-inline' giscus.app analytics.umami.is;
  style-src 'self' 'unsafe-inline';
  img-src * blob: data:;
  media-src *.s3.amazonaws.com;
  connect-src *;
  font-src 'self';
  frame-src giscus.app
`

const securityHeaders = [
  // https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP
  {
    key: 'Content-Security-Policy',
    value: ContentSecurityPolicy.replace(/\n/g, ''),
  },
  // https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Referrer-Policy
  {
    key: 'Referrer-Policy',
    value: 'strict-origin-when-cross-origin',
  },
  // https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Frame-Options
  {
    key: 'X-Frame-Options',
    value: 'DENY',
  },
  // https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Content-Type-Options
  {
    key: 'X-Content-Type-Options',
    value: 'nosniff',
  },
  // https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-DNS-Prefetch-Control
  {
    key: 'X-DNS-Prefetch-Control',
    value: 'on',
  },
  // https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Strict-Transport-Security
  {
    key: 'Strict-Transport-Security',
    value: 'max-age=31536000; includeSubDomains',
  },
  // https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Feature-Policy
  {
    key: 'Permissions-Policy',
    value: 'camera=(), microphone=(), geolocation=()',
  },
]

const output = process.env.EXPORT ? 'export' : undefined
const basePath = process.env.BASE_PATH || undefined
const unoptimized = process.env.UNOPTIMIZED ? true : undefined

/**
 * @type {import('next/dist/next-server/server/config').NextConfig}
 **/
module.exports = () => {
  const plugins = [withContentlayer, withBundleAnalyzer]
  return plugins.reduce((acc, next) => next(acc), {
    output,
    basePath,
    reactStrictMode: true,
    eslint: {
      ignoreDuringBuilds: true,
    },
    typescript: {
      ignoreBuildErrors: true,
    },
    trailingSlash: true,
    turbopack: {
      root: process.cwd(),
      rules: {
        '*.svg': {
          loaders: ['@svgr/webpack'],
          as: '*.js',
        },
      },
    },
    pageExtensions: ['ts', 'tsx', 'js', 'jsx', 'md', 'mdx'],
    images: {
      remotePatterns: [
        {
          protocol: 'https',
          hostname: 'picsum.photos',
        },
      ],
      unoptimized,
    },
    async headers() {
      return [
        {
          source: '/(.*)',
          headers: securityHeaders,
        },
      ]
    },
    webpack: (config, options) => {
      config.module.rules.push({
        test: /\.svg$/,
        use: ['@svgr/webpack'],
      })

      // Define process.env for client-side components
      config.resolve.fallback = {
        ...config.resolve.fallback,
        fs: false,
        path: false,
        os: false,
        crypto: false,
      }

      // Polyfill process.env for client-side components
      config.plugins.push(
        new options.webpack.DefinePlugin({
          'process.env.NEXT_PUBLIC_JD_PID': JSON.stringify(process.env.NEXT_PUBLIC_JD_PID || ''),
          'process.env.NEXT_PUBLIC_JD_POSITION_ID': JSON.stringify(process.env.NEXT_PUBLIC_JD_POSITION_ID || ''),
          'process.env.NEXT_PUBLIC_JD_APP_KEY': JSON.stringify(process.env.NEXT_PUBLIC_JD_APP_KEY || ''),
          'process.env.NEXT_PUBLIC_TAOBAO_PID': JSON.stringify(process.env.NEXT_PUBLIC_TAOBAO_PID || ''),
          'process.env.NEXT_PUBLIC_TAOBAO_UNION_ID': JSON.stringify(process.env.NEXT_PUBLIC_TAOBAO_UNION_ID || ''),
          'process.env.NEXT_PUBLIC_TAOBAO_ADZONE_ID': JSON.stringify(process.env.NEXT_PUBLIC_TAOBAO_ADZONE_ID || ''),
          'process.env.NEXT_PUBLIC_BASE_PATH': JSON.stringify(process.env.NEXT_PUBLIC_BASE_PATH || ''),
          'process.env.BASE_PATH': JSON.stringify(process.env.BASE_PATH || ''),
          'process.env.NEXT_UMAMI_ID': JSON.stringify(process.env.NEXT_UMAMI_ID || ''),
          'process.env.NEXT_PUBLIC_GISCUS_REPO': JSON.stringify(process.env.NEXT_PUBLIC_GISCUS_REPO || ''),
          'process.env.NEXT_PUBLIC_GISCUS_REPOSITORY_ID': JSON.stringify(process.env.NEXT_PUBLIC_GISCUS_REPOSITORY_ID || ''),
          'process.env.NEXT_PUBLIC_GISCUS_CATEGORY': JSON.stringify(process.env.NEXT_PUBLIC_GISCUS_CATEGORY || ''),
          'process.env.NEXT_PUBLIC_GISCUS_CATEGORY_ID': JSON.stringify(process.env.NEXT_PUBLIC_GISCUS_CATEGORY_ID || ''),
          'process.env.NODE_ENV': JSON.stringify(process.env.NODE_ENV || 'development'),
        })
      )

      return config
    },
  })
}
