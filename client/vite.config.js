// vite.config.js
import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import { createVuePlugin } from 'vite-plugin-vuetify';



export default defineConfig({
  plugins: [
    vue(),
    createVuePlugin({ autoImport: true }),
  ],
  server: {
    host: '0.0.0.0',
    port: 5173,
    strictPort: true,
    proxy: {
      '/api': {
        target: 'http://backend:8000', // Явно указываем backend внутри Docker
        changeOrigin: true,
        secure: false,
      },
    },
  },
  build: {
    rollupOptions: {
      output: {
        entryFileNames: 'assets/[name]-[hash].js',
        chunkFileNames: 'assets/[name]-[hash].js',
        assetFileNames: 'assets/[name]-[hash].[ext]',
      },
    },
  },
});