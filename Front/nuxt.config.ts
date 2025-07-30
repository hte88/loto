// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: true },
  modules: ['@nuxt/image', '@nuxt/ui'],
   runtimeConfig: {
    public: {
      BASE_URL: process.env.NUXT_BASE_URL,
    }
  }
})
