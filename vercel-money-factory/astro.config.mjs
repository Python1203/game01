import { defineConfig } from 'astro/config';

export default defineConfig({
  output: 'static',
  site: 'https://869.us.ci',
  compressHTML: true,
  build: {
    inlineStylesheets: 'auto'
  }
});
