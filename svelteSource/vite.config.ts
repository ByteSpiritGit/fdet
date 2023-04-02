import { defineConfig } from 'vite'
import { svelte } from '@sveltejs/vite-plugin-svelte'

export default defineConfig(({ command, mode, ssrBuild }) => {
   return {
      plugins: [svelte()],
      base: "./",
      build: {
         emptyOutDir: true,
         outDir: "../frontend/templates",
         assetsDir: "static",
         rollupOptions: {
            input: {
               main: './index.html',
               oldEval: './pages/oldEval.html',
            },
         },
      }
   }
})
