import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// Dentro de Docker la API se llama "api"; fuera de Docker, localhost.
const apiTarget = process.env.API_PROXY_TARGET || 'http://localhost:8000'

export default defineConfig({
  plugins: [vue()],
  server: {
    host: '0.0.0.0',
    port: 5173,
    watch: { usePolling: true }, // necesario para detectar cambios en Windows + Docker
    proxy: {
      // Todo lo que empiece por /api se envía a FastAPI (evita problemas de CORS)
      '/api': {
        target: apiTarget,
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ''),
      },
    },
  },
})
