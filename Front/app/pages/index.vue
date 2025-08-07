<script setup lang="ts">
//import state from '../stats.json'
import type { CheckboxGroupItem } from '@nuxt/ui'

const config = useRuntimeConfig()

const isDrawerOpen = ref(false)

/* const { data } = useFetch('api/draws/', {
     key:'get-draws',
  method: 'GET',
    baseURL: config.public.BASE_URL
}) */

/* const { execute } = useFetch('api/draws/bulk', {
    key:'post-draws',
    method: 'POST',
    baseURL: config.public.BASE_URL,
    body: state
}) */
/* const { execute } = useFetch('api/draws/generate', {
    key:'post-draws-generate',
    method: 'POST',
    baseURL: config.public.BASE_URL,
    body: {}
}) */

/*
const { data: weights, execute: execWeights } = useFetch('api/draws/weights', {
    key: 'get-draws-weights',
    method: 'GET',
    baseURL: config.public.BASE_URL
}) */

const lotteryConfig = ref({
    start_date: '1976-01-01',
    end_date: '2025-09-01',
    shouldBalanceEvenOdd: true,
    favorEven: 60, // 60–40%

    shouldBalanceHighLow: true,
    favorHigh: 50, // 50%

    shouldAvoidLogicalSequences: true,
    sequenceTolerance: 2, // 2 consecutive numbers are acceptable

    shouldAvoidRoundNumbers: true,
    roundNumberTolerance: 2, // Max 2 round numbers per grid

    includeNumbers: [],
    excludeNumbers: [],
    shouldCheckExistence: true,
    shouldEvaluateScore: true,
    shouldGenerateLucky: true, // weighted selection by past frequency
    favorLucky: 6,
    excludeLucky: [],
    gridsToGenerate: 1,
    numbersToGenerate: 5,
    includedSources: ["loto", "super", "grand"]
})

const { data: dgenerate, execute: execGenerate } = useFetch('api/draws/generate', {
    key: 'post-draws-generate',
    baseURL: config.public.BASE_URL,
    method: 'POST',
    immediate: false,
    watch: false,
    body: lotteryConfig
    /* transform: (dgenerate) =>
        dgenerate.map((it) => ({
            ...it,
            numbers: Array.isArray(it.numbers) ? it.numbers.join('-') : it.numbers
        })) */
})

function execute() {
    isDrawerOpen.value = false
    execGenerate()
}

onMounted(() => {
    /*  execFrequency()
    execWeights()
    execGenerate() */
    // execute()
})

const numbers = ref<CheckboxGroupItem[]>(Array.from({ length: 49 }, (_, i) => i + 1))
const luckNumbers = ref<CheckboxGroupItem[]>(Array.from({ length: 10 }, (_, i) => i + 1))

const result = computed(() => dgenerate.value ?? [])
/* const first = computed(() => result.value?.[0]?.numbers.split('-') ?? [])
const firstLucky = computed(() => result.value?.[0]?.lucky_number.toString() ?? '') */
const visibleItems = ref(new Set())

const animateResults = async () => {
    visibleItems.value.clear()

    for (let lineIndex = 0; lineIndex < result.value.length; lineIndex++) {
        // Animer les numéros de la ligne
        for (let numIndex = 0; numIndex < result.value[lineIndex].numbers.length; numIndex++) {
            await new Promise((resolve) => setTimeout(resolve, 50))
            visibleItems.value.add(`${lineIndex}-${numIndex}`)
        }

        // Animer le numéro chance
        await new Promise((resolve) => setTimeout(resolve, 50))
        visibleItems.value.add(`${lineIndex}-lucky`)

        await new Promise((resolve) => setTimeout(resolve, 100))
        visibleItems.value.add(`${lineIndex}-info`)

        // Pause avant la ligne suivante
        if (lineIndex < result.value.length - 1) {
            await new Promise((resolve) => setTimeout(resolve, 100))
        }
    }
}

// Déclencher après le fetch
watch(
    () => result.value,
    () => {
        if (result.value.length > 0) {
            animateResults()
        }
    },
    { immediate: true }
)
</script>

<template>
    <div class="h-screen pt-20">
        <div
            class="w-full max-w-(--ui-container) mx-auto px-4 sm:px-6 lg:px-8 flex flex-col lg:grid gap-16 sm:gap-y-24 lg:items-center !pb-20 py-24 sm:py-32 lg:py-40"
        >
            <div class="text-center">
                <h1
                    class="text-pretty tracking-tight font-bold text-5xl sm:text-7xl bg-gradient-to-r from-blue-500 to-rose-400 bg-clip-text text-transparent"
                >
                    Loto Cheat
                </h1>
                <p class="text-lg sm:text-xl/8 text-muted text-pretty mt-6">
                    commodo. Elit sunt amet fugiat veniam occaecat.
                </p>
            </div>
            <div class="flex flex-col gap-4 w-4xl mx-auto">
                <section class="justify-center flex">
                    <UDrawer
                        v-model:open="isDrawerOpen"
                        direction="right"
                        title="don't delete me"
                        description="don't delete me"
                        :handle="false"
                        :dismissible="false"
                        :ui="{ container: 'bg-black-500' }"
                    >
                        <UButton
                            label="Configuration"
                            variant="subtle"
                            size="xl"
                            trailing-icon="i-lucide-cog"
                        />
                        <template #title />
                        <template #description />
                        <template #header>
                            <div class="flex flex-row justify-between items-center">
                                <h2 class="text-xl font-semibold">Configuration</h2>
                                <UButton
                                    color="neutral"
                                    variant="ghost"
                                    icon="i-lucide-x"
                                    @click="isDrawerOpen = false"
                                />
                            </div>
                        </template>
                        <template #body>
                            <LotoForm v-model="lotteryConfig" @on-submit="execute()" />
                        </template>
                    </UDrawer>
                </section>

                <div
                    v-for="(
                        { numbers, lucky_number, score, total_draws_used }, lineIndex
                    ) in result"
                    :key="lineIndex"
                    class="flex flex-row gap-4 mx-auto w-fit"
                >
                    <!-- Numéros principaux -->
                    <UCheckbox
                        v-for="(num, numIndex) in numbers"
                        :key="`${lineIndex}-${num}`"
                        v-show="visibleItems.has(`${lineIndex}-${numIndex}`)"
                        class="fade-in"
                        indicator="hidden"
                        variant="card"
                        :label="String(num)"
                        :ui="{
                            root: 'size-14',
                            base: 'justify-center flex',
                            wrapper: 'h-full',
                            label: 'justify-center items-center h-full flex'
                        }"
                    />

                    <!-- Numéro chance -->
                    <UCheckbox
                        v-show="visibleItems.has(`${lineIndex}-lucky`)"
                        class="fade-in"
                        indicator="hidden"
                        variant="card"
                        :label="String(lucky_number)"
                        :ui="{
                            root: 'size-14 ml-4',
                            base: 'justify-center flex',
                            wrapper: 'h-full',
                            label: 'justify-center items-center h-full flex'
                        }"
                    />
                    <ul v-show="visibleItems.has(`${lineIndex}-info`)" class="text-xs flex flex-col justify-center">
                        <li><b>Tirage :</b> {{ numbers.join(' ') }} {{ lucky_number }}</li>
                        <li><b>Score:</b> {{ score }}</li>
                        <li>Calculé sur <b>{{ total_draws_used }}</b> tirages</li>
                    </ul>
                </div>

                <!-- <section class="flex justify-between gap-4">
                    <div class="flex-1">
                        <UCheckboxGroup
                            v-model="first"
                            indicator="hidden"
                            variant="card"
                            :default-value="first"
                            :items="numbers"
                            :ui="{
                                fieldset: 'flex flex-wrap flex-row',
                                item: 'size-14 content-center'
                            }"
                        />
                    </div>
                    <div class="w-32">
                        <URadioGroup
                            v-model="firstLucky"
                            indicator="hidden"
                            variant="card"
                            :default-value="firstLucky"
                            :items="luckNumbers"
                            :ui="{
                                fieldset: 'flex flex-wrap flex-row',
                                item: 'size-14 content-center'
                            }"
                        />
                    </div>
                </section> -->

                <!-- <section v-if="result.length > 0">
                    <CommonsTableStat :data="result" />
                </section> -->
            </div>
        </div>
    </div>
</template>
<style scoped>
.fade-in {
    animation: fadeInUp 0.4s ease-out;
}

@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(20px) scale(0.8);
    }
    to {
        opacity: 1;
        transform: translateY(0) scale(1);
    }
}
</style>
