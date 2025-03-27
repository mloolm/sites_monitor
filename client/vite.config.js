import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import vuetify from 'vite-plugin-vuetify';
import { VitePWA } from 'vite-plugin-pwa';

export default defineConfig({
  plugins: [
    vue(),
    vuetify({ autoImport: true }),
    VitePWA({
      registerType: 'autoUpdate',
      manifest: {
        name: 'Sites monitoring app',
        short_name: 'SiteMon',
        description: 'Website monitoring - availability, response time, SSL certificate, problem notifications, reminders about SSL certificate expiration',
        theme_color: 'rgba(13,110,253,0.12)',
        background_color: '#ffffff',
        display: 'standalone',
        icons: [
          {
            src: '/img/icons/web-app-manifest-192x192.png',
            sizes: '192x192',
            type: 'image/png'
          },
          {
            src: '/img/icons/web-app-manifest-512x512.png',
            sizes: '512x512',
            type: 'image/png'
          }
        ]


      },
      workbox: {
        globPatterns: ['**/*.{js,css,html,png,jpg,svg}'],
      },
      devOptions: {
        enabled: true,
        type: 'module',
      },
      injectRegister: false,

    })
  ],
  server: {
    host: '0.0.0.0',
    port: 5173,
    strictPort: true,
    proxy: {
      '/api': {
        target: 'http://backend:8000',
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
