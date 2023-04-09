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
               evalOutput: './pages/evalOutput.html',
            },
            output: {
               entryFileNames: 'static/js/[name]-[hash].js',
               chunkFileNames: 'static/js/[name]-[hash].js',
               assetFileNames: ({ name }) => {
                  if (/\.(gif|jpe?g|png|svg)$/.test(name ?? '')) {
                     return 'static/images/[name]-[hash].[ext]';
                  }

                  if (/\.css$/.test(name ?? '')) {
                     return 'static/css/[name]-[hash].[ext]';
                  }

                  return 'static/[name]-[hash].[ext]';
               },
            },
         },
      }
   }
})
