// Global polyfill for process.env to support client-side components
// This prevents "process is not defined" errors in the browser
// CRITICAL: Do NOT access process.env here - values are injected by webpack DefinePlugin
// Only create minimal process object to prevent runtime errors

if (typeof window !== 'undefined' && !(window as any).process) {
  ;(window as any).process = {
    env: {
      NODE_ENV: 'development',
    },
  }
}

export {}
