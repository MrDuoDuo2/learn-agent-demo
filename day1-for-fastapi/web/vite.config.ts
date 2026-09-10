import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    port: 5173,
    proxy: {
      // 所有 /api 开头的请求，转发到后端
      '/api': {
        target: 'http://localhost:8000', // 后端服务地址
        changeOrigin: true, // 修改源，解决跨域
        rewrite: (path) => path.replace(/^\/api/, ''), // 去掉请求路径里的 /api 前缀
      }
    }
  },
})
