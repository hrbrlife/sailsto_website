import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { nodePolyfills } from 'vite-plugin-node-polyfills';

export default defineConfig({
  plugins: [
    react(),
    nodePolyfills({
      // Для Vite 7 важно явно включить эти модули
      include: ['buffer', 'stream', 'util', 'process'],
      globals: {
        Buffer: true,
        global: true,
        process: true,
      },
    }),
  ],
  resolve: {
    alias: {
      // Это критично для библиотек Metaplex
      stream: 'stream-browserify',
      buffer: 'buffer',
    },
  },
  optimizeDeps: {
    esbuildOptions: {
      // Дополнительная гарантия для глобальных переменных в Vite 7
      define: {
        global: 'globalThis',
      },
    },
  },
});
