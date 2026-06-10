// @ts-check
import { defineConfig } from 'astro/config';

// https://astro.build/config
export default defineConfig({
  // Easy headers for dev server (no Gulp or custom server needed).
  // These were originally for the WASM browser node; for the pure stream client
  // they are optional but kept for compatibility if you want to re-enable browser node.
  server: {
    headers: {
      'Cross-Origin-Opener-Policy': 'same-origin',
      'Cross-Origin-Embedder-Policy': 'require-corp',
    }
  }
});
