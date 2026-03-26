// Global polyfill for process.env to support client-side components
// This prevents "process is not defined" errors in the browser
// CRITICAL: Do NOT access process.env here - values are injected by webpack DefinePlugin
// Only create minimal process object to prevent runtime errors

// Initialize process polyfill at module level for both development and production
if (typeof window !== 'undefined' && !(window as any).process) {
  ;(window as any).process = {
    env: {
      // These values will be overridden by webpack DefinePlugin with actual env values
      NODE_ENV: process.env.NODE_ENV || 'production',
      NEXT_PUBLIC_BASE_PATH: process.env.NEXT_PUBLIC_BASE_PATH || '',
      NEXT_PUBLIC_JD_PID: process.env.NEXT_PUBLIC_JD_PID || '',
      NEXT_PUBLIC_JD_POSITION_ID: process.env.NEXT_PUBLIC_JD_POSITION_ID || '',
      NEXT_PUBLIC_JD_APP_KEY: process.env.NEXT_PUBLIC_JD_APP_KEY || '',
      NEXT_PUBLIC_TAOBAO_PID: process.env.NEXT_PUBLIC_TAOBAO_PID || '',
      NEXT_PUBLIC_TAOBAO_UNION_ID: process.env.NEXT_PUBLIC_TAOBAO_UNION_ID || '',
      NEXT_PUBLIC_TAOBAO_ADZONE_ID: process.env.NEXT_PUBLIC_TAOBAO_ADZONE_ID || '',
      NEXT_UMAMI_ID: process.env.NEXT_UMAMI_ID || '',
      NEXT_PUBLIC_GISCUS_REPO: process.env.NEXT_PUBLIC_GISCUS_REPO || '',
      NEXT_PUBLIC_GISCUS_REPOSITORY_ID: process.env.NEXT_PUBLIC_GISCUS_REPOSITORY_ID || '',
      NEXT_PUBLIC_GISCUS_CATEGORY: process.env.NEXT_PUBLIC_GISCUS_CATEGORY || '',
      NEXT_PUBLIC_GISCUS_CATEGORY_ID: process.env.NEXT_PUBLIC_GISCUS_CATEGORY_ID || '',
      NEXT_PUBLIC_TB_PUB_ID: process.env.NEXT_PUBLIC_TB_PUB_ID || '',
    },
  }
}

export {}
