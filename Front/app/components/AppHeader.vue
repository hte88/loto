<script setup lang="ts">
import { ref } from 'vue'

const navigation = [
    { name: 'Home', href: '/' },
    { name: 'Stats', href: '/stats' }
]

const mobileMenuOpen = ref(false)
</script>
<template>
    <header class="absolute inset-x-0 top-0 z-50 text-white bg-primary-600 border-b-2 border-primary-600">
        <nav class="flex items-center justify-between p-6 lg:px-8" aria-label="Global">
            <div class="flex lg:flex-1">
                <a href="#" class="-m-1.5 p-1.5 font-bold text-2xl">
                    <span class="sr-only">Loto Cheat</span>
                    LOTO CHEAT
                </a>
            </div>
            <div class="flex lg:hidden">
                <button
                    type="button"
                    class="-m-2.5 inline-flex items-center justify-center rounded-md p-2.5"
                    @click="mobileMenuOpen = true"
                >
                    <span class="sr-only">Open main menu</span>
                </button>
            </div>
            <div class="hidden lg:flex lg:gap-x-12">
                <a
                    v-for="item in navigation"
                    :key="item.name"
                    :href="item.href"
                    class="text-sm/6 font-semibold"
                    >{{ item.name }}</a
                >
            </div>
            <div class="hidden lg:flex lg:flex-1 lg:justify-end"></div>
        </nav>
    </header>
</template>
