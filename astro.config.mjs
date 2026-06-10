// @ts-check
import { defineConfig } from 'astro/config';

// https://astro.build/config
export default defineConfig({
  // Headers for the Astro dev server only (`npm run dev`).
  // These do NOT apply to the production static build or Netlify deploy.
  // For production headers (Netlify, etc.) see netlify.toml and/or public/_headers.
  server: {
    headers: {
      'Cross-Origin-Opener-Policy': 'same-origin',
      'Cross-Origin-Embedder-Policy': 'require-corp',
    }
  }
});
