import { defineConfig } from 'astro/config';
import vercel from '@astrojs/vercel';

export default defineConfig({
  output: 'server',
  site: 'https://869.us.ci',
  adapter: vercel(),
  compressHTML: true,
  build: {
    inlineStylesheets: 'auto'
  }
});
